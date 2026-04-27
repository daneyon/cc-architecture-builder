---
name: index-kb
description: >-
  Regenerate INDEX.md files for a knowledge base from current file structure
  and YAML frontmatter metadata. Triggers: regenerate KB index, update INDEX.md,
  knowledge base reorganization, after KB file moves, kb hygiene check.
argument-hint: "Optional category to limit scope (e.g., 'components', 'reference')"
allowed-tools: Read, Write, Glob
---

# Regenerate Knowledge Base Indexes

## Purpose

Keeps `knowledge/INDEX.md` (root) and per-category `knowledge/{cat}/INDEX.md`
files in sync with the actual files present and their frontmatter metadata.
Hand-maintained indexes drift the moment a file is added, renamed, or
re-categorized; this skill makes regeneration a one-shot deterministic step.

## When to Invoke

- After adding new KB files
- After renaming or moving KB files
- After updating frontmatter on existing files (title, summary, tags)
- Before `/validate` or `/cab:audit-workspace` runs (clean indexes are an
  audit dimension)
- Periodically as part of KB hygiene

## Protocol

### Step 1: Scan KB Directory

```bash
# All markdown files under knowledge/, excluding INDEX.md itself
find knowledge/ -name '*.md' -not -name 'INDEX.md' | sort
```

If `$ARGUMENTS` (category) provided, scope to `knowledge/<category>/` only.

### Step 2: Extract Frontmatter

Per file, parse YAML frontmatter for these keys (per
`.claude/rules/kb-conventions.md`):

| Key | Use |
|---|---|
| `id` | Unique identifier; fallback to filename stem |
| `title` | Display name in INDEX |
| `summary` | One-line description (truncate to ~100 chars) |
| `tags` | Categorization signals |
| `complexity` | foundational / intermediate / advanced |
| `depends_on` | Prerequisites (cross-link in INDEX) |
| `related` | Related files (cross-link) |
| `source` | Citation URL (per kb-conventions LL-11) |

Files lacking required frontmatter (`source:`) get flagged in the warnings
section but are still included in the INDEX (so the warning is actionable).

### Step 3: Generate INDEX Files

**Root `knowledge/INDEX.md`**:

- Category summary table (count + brief description per category)
- Total file count
- Navigation guide pointing to per-category INDEXes
- Optional: complexity rollup (foundational vs advanced files per category)

**Per-category `knowledge/<cat>/INDEX.md`**:

- File table: title | summary | complexity | tags
- Reading-order recommendations (use `depends_on` to topo-sort)
- Cross-category links (use `related`)

### Step 4: Report

```markdown
## KB Index Regeneration — [date]

### Scanned
- N files across M categories

### Updated
- knowledge/INDEX.md
- knowledge/<cat-1>/INDEX.md
- knowledge/<cat-2>/INDEX.md
- ...

### Warnings
- N files missing `source:` frontmatter (LL-10 fresh-fetch convention)
- N files orphaned (not referenced from any other file)
- N files lacking `summary:` (used filename heuristic)
```

## Arguments

- `$1` (optional): Specific category to regenerate (`components`, `reference`,
  `operational-patterns`, `schemas`, etc.). Default: all categories.

## Verification

This skill is working correctly when:

- Generated indexes match the actual file set (no missing files, no
  references to deleted files)
- Frontmatter warnings are actionable (specific file + missing key, not
  generic "some files have issues")
- Reading-order recommendations respect `depends_on` topology
- Skill is idempotent: re-running on unchanged KB produces no diff

## Integration Points

- `commands/kb-index.md` — shim trigger preserving `/cab:kb-index`
- `.claude/rules/kb-conventions.md` — frontmatter requirements + `source:` rule
- `validate-structure` skill — validates INDEX presence/freshness as a
  structural criterion
- `audit-workspace` skill — full KB dimension audit (deeper than this skill)

## See Also

- `knowledge/INDEX.md` — current root index (regeneration target)
- `.claude/rules/kb-conventions.md` — governance for KB files this skill
  operates over
