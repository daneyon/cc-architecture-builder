#!/usr/bin/env bash
# enforce-current-task-budget.sh
#
# CAB pre-commit budget gate for notes/current-task.md. P3 deliverable of
# the bootstrap efficiency task (impl-plan-bootstrap-efficiency-2026-04-11.md).
#
# Dual-mode invocation contract:
#
#   Mode A (CC PreToolUse hook) — stdin receives tool_input JSON; script parses
#     the `command` field and filters for `git commit` invocations. Non-commit
#     tool calls exit 0 (pass-through). Registered via hooks/hooks.json.
#
#   Mode B (Git native pre-commit hook) — stdin is a tty (or empty / non-JSON);
#     script runs the budget check directly. Install via copy or symlink:
#         cp hooks/scripts/enforce-current-task-budget.sh .git/hooks/pre-commit
#         chmod +x .git/hooks/pre-commit
#     Universal enforcement — catches manual `git commit` from terminal, not
#     just CC-invoked commits. Not plugin-distributed; per-clone setup.
#
# Purpose: Enforce `notes/current-task.md <=100 lines` hard target. The file is
# the cold-start anchor — bloat breaks the partial-read bootstrap cascade that
# P2 established (T1 boundary markers in 4 state files).
#
# Counting semantics: `wc -l` over the entire file. No blank-line filter, no
# boundary-marker exclusion. Simpler is better — zero edge cases, zero drift
# between what the author sees (`wc -l`) and what the hook enforces.
#
# Budget: 100 lines hard cap. Block at 101+.
#
# Exit 0: Pass (file <=100 lines, or non-commit tool call in CC mode)
# Exit 1: Operational error (missing file, repo root, malformed input)
# Exit 2: Block (file exceeds budget) — CC reads stderr as block reason
#
# References:
#   - notes/impl-plan-bootstrap-efficiency-2026-04-11.md (P3 deliverable)
#   - notes/current-task.md (the target file)
#   - knowledge/operational-patterns/state-management/bootstrap-read-pattern.md
#   - hooks/scripts/pre-push-state-review.sh (sibling dispatcher pattern)

set -euo pipefail

BUDGET_LINES=100
TARGET_FILE="notes/current-task.md"

# Locate repo root — works whether invoked from CC plugin context or a git hook
repo_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
if [[ -z "$repo_root" ]]; then
  printf 'enforce-current-task-budget.sh: not inside a git repo\n' >&2
  exit 1
fi

run_check() {
  local path="$repo_root/$TARGET_FILE"
  if [[ ! -f "$path" ]]; then
    printf 'enforce-current-task-budget.sh: %s not found\n' "$path" >&2
    exit 1
  fi
  local lines
  lines=$(wc -l < "$path" | tr -d ' \t\r\n')
  if (( lines > BUDGET_LINES )); then
    {
      printf '\n[BLOCKED] current-task.md exceeds the cold-start budget.\n\n'
      printf '  File:       %s\n' "$TARGET_FILE"
      printf '  Lines:      %d\n' "$lines"
      printf '  Budget:     %d (hard cap, HITL-3 enforced)\n' "$BUDGET_LINES"
      printf '  Reference:  notes/impl-plan-bootstrap-efficiency-2026-04-11.md (P3)\n\n'
      printf 'current-task.md is the bootstrap anchor. Bloat here breaks the partial-read\n'
      printf 'cascade established in P2. Compress before committing:\n'
      printf '  - Move verbose task detail into the impl-plan file (link, do not mirror).\n'
      printf '  - Keep only phase status + cold-start protocol + directives here.\n'
      printf '  - See notes/session-28-recovery-2026-04-11.md Part 3\n'
      printf '    ("Impl Plan As The Real Session-Transfer Artifact").\n\n'
    } >&2
    exit 2
  fi
  exit 0
}

# Dispatch: stdin pipe (CC PreToolUse) vs stdin tty / empty / non-JSON (direct)
if [[ -t 0 ]]; then
  run_check
fi

# Stdin is piped — could be CC hook JSON or could be empty (some git hook environments)
input=$(cat 2>/dev/null || echo "")
if [[ -z "$input" ]]; then
  run_check
fi

# Extract command field from CC tool_input JSON (portable, no jq)
command=$(echo "$input" | grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"command"[[:space:]]*:[[:space:]]*"\(.*\)"/\1/' || echo "")

if [[ -z "$command" ]]; then
  # Not recognizable as CC tool_input — treat as direct invocation
  run_check
fi

# CC PreToolUse context — only act on `git commit` commands
if ! echo "$command" | grep -qE '^[[:space:]]*git[[:space:]]+commit\b'; then
  exit 0
fi

run_check
