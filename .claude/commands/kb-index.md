---
description: Regenerate knowledge base INDEX files from current content
---

# KB Index Command

Regenerate INDEX.md files for the knowledge base based on current file structure and metadata.

## Behavior

1. **Scan knowledge directory** for all markdown files
2. **Extract metadata** from frontmatter of each file
3. **Generate/update INDEX.md** files:
   - Root `knowledge/INDEX.md`
   - Category-level `knowledge/{{category}}/INDEX.md`

## Arguments

- `$1` (optional): Specific category to regenerate

## Examples

```
/kb-index
→ Regenerate all INDEX files

/kb-index components
→ Only regenerate knowledge/components/INDEX.md
```

## INDEX Generation

### Root INDEX.md

Generated with:
- Category summary table
- Total file count
- Navigation guide
- Per-category file listings

### Category INDEX.md

Generated with:
- File table with summaries (from frontmatter)
- Reading order recommendations
- Cross-category relationships

## Metadata Extraction

From each file's frontmatter:
- `id` — Unique identifier
- `title` — Display name
- `summary` — One-line description
- `tags` — Categorization
- `complexity` — foundational/intermediate/advanced
- `depends_on` — Prerequisites
- `related` — Related files

## Output

Show:
- Files scanned
- INDEX files created/updated
- Any files missing recommended metadata
- Warnings for orphaned files (no INDEX reference)

## Best Practice

Run `/kb-index` after:
- Adding new knowledge files
- Renaming or moving files
- Updating file metadata
- Before validating structure
