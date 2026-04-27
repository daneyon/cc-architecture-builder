---
description: Regenerate knowledge base INDEX files from current content and frontmatter
allowed-tools: Read, Write, Glob
---

# KB Index Command

Shim invoking the `index-kb` skill, which regenerates `knowledge/INDEX.md`
and per-category INDEXes from current files + frontmatter.

## Arguments

- `$1` (optional): Specific category to regenerate (`components`, `reference`,
  `operational-patterns`, `schemas`, etc.). Default: all categories.

## Examples

```
/kb-index                  # Regenerate all INDEX files
/kb-index components       # Regenerate only knowledge/components/INDEX.md
```

## When to Run

- After adding, renaming, or moving KB files
- After updating frontmatter on existing files
- Before `/validate` or `/cab:audit-workspace` runs (clean indexes are an
  audit dimension)

## See Also

- `skills/index-kb/` — The workflow skill (owns all logic)
- `.claude/rules/kb-conventions.md` — KB frontmatter requirements
