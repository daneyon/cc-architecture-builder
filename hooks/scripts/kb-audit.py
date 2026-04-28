#!/usr/bin/env python3
"""KB metadata audit — Phase 1 of UXL-005 (KB→KG foundation).

Enumerates knowledge/ files, extracts YAML frontmatter, reports coverage matrix +
gap list + dangling cross-references. Idempotent; re-run produces identical
output for unchanged KB.

Usage: python hooks/scripts/kb-audit.py [knowledge_root]
"""

import os, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REQUIRED = ["source"]
OPTIONAL_GRAPH = [
    "id",
    "title",
    "category",
    "tags",
    "depends_on",
    "related",
    "complexity",
]

ROOT = sys.argv[1] if len(sys.argv) > 1 else "knowledge"


def parse_frontmatter(path):
    """Return (meta dict, body) or (None, content) if no frontmatter."""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        return None, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content
    raw = parts[1]
    meta = {}
    current_key = None
    for line in raw.split("\n"):
        line = line.rstrip()
        if not line.strip():
            continue
        m = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val:
                if val.startswith("[") and val.endswith("]"):
                    meta[key] = [
                        x.strip().strip("'\"")
                        for x in val[1:-1].split(",")
                        if x.strip()
                    ]
                else:
                    meta[key] = val.strip("'\"")
                current_key = None
            else:
                meta[key] = []
                current_key = key
        elif line.startswith("  - ") and current_key:
            meta[current_key].append(line[4:].strip().strip("'\""))
    return meta, parts[2]


all_files = []
for dirpath, dirs, files in os.walk(ROOT):
    if "_archive" in dirpath or "_graph" in dirpath:
        continue
    for f in files:
        if f.endswith(".md") and f != "INDEX.md":
            p = os.path.join(dirpath, f).replace(os.sep, "/")
            all_files.append(p)

print(f"Total KB files audited: {len(all_files)}\n")

coverage = {field: 0 for field in REQUIRED + OPTIONAL_GRAPH}
missing_source = []
no_frontmatter = []
all_metas = {}

for path in all_files:
    meta, _ = parse_frontmatter(path)
    if meta is None:
        no_frontmatter.append(path)
        continue
    all_metas[path] = meta
    for field in REQUIRED + OPTIONAL_GRAPH:
        if field in meta and meta[field]:
            coverage[field] += 1
    if "source" not in meta or not meta["source"]:
        missing_source.append(path)

all_ids = set()
for meta in all_metas.values():
    if "id" in meta:
        all_ids.add(meta["id"])

dangling = []
for path, meta in all_metas.items():
    for edge_field in ["depends_on", "related"]:
        refs = meta.get(edge_field, [])
        if isinstance(refs, str):
            refs = [refs]
        for ref in refs:
            if ref and ref not in all_ids:
                dangling.append(f"{path}: {edge_field} -> {ref} (no matching id)")

total_with_fm = len(all_files) - len(no_frontmatter)
print("=== Frontmatter Coverage Matrix ===")
for field in REQUIRED + OPTIONAL_GRAPH:
    pct = 100 * coverage[field] / max(total_with_fm, 1)
    marker = "[REQUIRED]" if field in REQUIRED else ""
    print(f"  {field:20s}: {coverage[field]:3d}/{total_with_fm} ({pct:5.1f}%) {marker}")

print()
print(f"=== Files Missing Frontmatter ({len(no_frontmatter)}) ===")
for p in no_frontmatter:
    print(f"  {p}")

print()
print(f"=== Files Missing source: ({len(missing_source)}) ===")
for p in missing_source:
    print(f"  {p}")

print()
print(f"=== Dangling Cross-Refs ({len(dangling)}) ===")
for d in dangling[:30]:
    print(f"  {d}")
if len(dangling) > 30:
    print(f"  ... +{len(dangling) - 30} more")

print()
print("=== Distinct id values (graph-eligible nodes) ===")
print(f"  {len(all_ids)} unique IDs across {total_with_fm} files with frontmatter")
