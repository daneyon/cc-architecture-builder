#!/usr/bin/env python
"""uxl-update.py — CAB UX-log tracker state-machine helper (UXL-033).

Reduces per-resolution token cost by ~30-40% vs inline Python scripts.
Also applies U-curve attention principle to the tracker itself: active
rows sort to the top, resolved rows sink to the bottom. Active work stays
in the high-attention zone when reading the CSV mid-session.

Usage:
  sort                      Re-sort CSV active-top (run anytime; idempotent)

  resolve <id> <commit> [--plan <anchor>] [--note-stdin]
                            Mark row resolved; set linked_commit + optional
                            linked_plan + optional " → RESOLVED: <note>"
                            appended to orchestrator_take. With --note-stdin,
                            reads note from stdin (supports multi-line).

  set <id> <field>=<value> [<field>=<value> ...]
                            Generic field updater. Does NOT auto-resolve.
                            Use for status transitions, manual field edits.

  enrich <id> <field> {append|prepend} --stdin
                            Append/prepend text to a field (reads from stdin).
                            Use for orchestrator_take enrichment, user_comment
                            verbatim block addition (preserves fidelity).

  show <id>                 Print a row's fields (human-readable).

Status sort order (active → resolved):
  open > triaged > planning > in-progress > deferred > superseded > wontfix > resolved

Examples:
  python hooks/scripts/uxl-update.py sort

  python hooks/scripts/uxl-update.py resolve UXL-033 abc1234 \\
    --plan "notes/impl-plan-ux-log-tracker-2026-04-22.md#uxl-033" \\
    --note-stdin <<'EOF'
  Helper script landed; active-top sort applied; CSV state-machine
  mechanics are now ~30-40% cheaper per op.
  EOF

  python hooks/scripts/uxl-update.py set UXL-011 status=triaged

  python hooks/scripts/uxl-update.py enrich UXL-018 orchestrator_take append --stdin <<'EOF'
  Additional context learned after triage: ...
  EOF

Source: UXL-033 deliverable in impl-plan-ux-log-tracker-2026-04-22.md.
When UXL-034 (state-mgmt-capture skill) lands, this script becomes a
candidate for DP2-aligned skill wrap (skills/ux-log-state-machine/scripts/).
"""

import csv
import sys
from pathlib import Path

CSV_PATH = Path("notes/ux-log-001-2026-04-22-pass-1.csv")

# Active statuses sort higher (lower key number); resolved sinks to bottom.
STATUS_ORDER = {
    "open": 0,
    "triaged": 1,
    "planning": 2,
    "in-progress": 3,
    "deferred": 4,
    "superseded": 5,
    "wontfix": 6,
    "resolved": 7,
}


def _sort_key(row):
    status_key = STATUS_ORDER.get(row["status"], 99)
    try:
        id_num = int(row["id"].split("-")[1])
    except (IndexError, ValueError):
        id_num = 99999
    return (status_key, id_num)


def load():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def save(fieldnames, rows, do_sort=True):
    if do_sort:
        rows = sorted(rows, key=_sort_key)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def find(rows, row_id):
    for r in rows:
        if r["id"] == row_id:
            return r
    raise KeyError(f"Row {row_id} not found in {CSV_PATH}")


def cmd_sort(_args):
    fieldnames, rows = load()
    save(fieldnames, rows)
    from collections import Counter

    dist = Counter(r["status"] for r in rows)
    print(f"Sorted {len(rows)} rows active-top")
    print(f"Distribution: {dict(dist)}")


def cmd_resolve(args):
    if len(args) < 2:
        sys.exit("Usage: resolve <id> <commit> [--plan <anchor>] [--note-stdin]")
    row_id = args[0]
    commit = args[1]
    plan = None
    note_stdin = False
    i = 2
    while i < len(args):
        if args[i] == "--plan":
            plan = args[i + 1]
            i += 2
        elif args[i] == "--note-stdin":
            note_stdin = True
            i += 1
        else:
            sys.exit(f"Unknown arg: {args[i]}")
    note = sys.stdin.read().strip() if note_stdin else ""
    fieldnames, rows = load()
    row = find(rows, row_id)
    row["linked_commit"] = commit
    if plan:
        row["linked_plan"] = plan
    row["status"] = "resolved"
    if note:
        row["orchestrator_take"] = (
            row["orchestrator_take"].rstrip() + " → RESOLVED: " + note
        )
    save(fieldnames, rows)
    print(f"Resolved {row_id} @ {commit}{' (note added)' if note else ''}")


def cmd_set(args):
    if len(args) < 2:
        sys.exit("Usage: set <id> <field>=<value> [<field>=<value> ...]")
    row_id = args[0]
    fieldnames, rows = load()
    row = find(rows, row_id)
    for pair in args[1:]:
        field, sep, value = pair.partition("=")
        if not sep or field not in fieldnames:
            sys.exit(f"Bad pair '{pair}' — field must be one of {fieldnames}")
        row[field] = value
    save(fieldnames, rows)
    print(f"Updated {row_id}: {', '.join(args[1:])}")


def cmd_enrich(args):
    if len(args) < 4 or args[2] not in ("append", "prepend") or args[3] != "--stdin":
        sys.exit("Usage: enrich <id> <field> {append|prepend} --stdin")
    row_id, field, mode, _ = args[:4]
    text = sys.stdin.read().strip()
    fieldnames, rows = load()
    if field not in fieldnames:
        sys.exit(f"Unknown field: {field}")
    row = find(rows, row_id)
    current = row[field].rstrip() if row[field] else ""
    if mode == "append":
        row[field] = (current + "\n\n" + text) if current else text
    else:
        row[field] = (text + "\n\n" + current) if current else text
    save(fieldnames, rows)
    print(f"Enriched {row_id}.{field} ({mode}, {len(text)} chars)")


def cmd_show(args):
    if not args:
        sys.exit("Usage: show <id>")
    fieldnames, rows = load()
    row = find(rows, args[0])
    for f in fieldnames:
        val = row[f]
        if val:
            print(f"  {f:20s}: {val[:120]}{'...' if len(val) > 120 else ''}")


COMMANDS = {
    "sort": cmd_sort,
    "resolve": cmd_resolve,
    "set": cmd_set,
    "enrich": cmd_enrich,
    "show": cmd_show,
}


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__, file=sys.stderr)
        print(f"\nCommands: {list(COMMANDS.keys())}", file=sys.stderr)
        sys.exit(1)
    COMMANDS[sys.argv[1]](sys.argv[2:])
