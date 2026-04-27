# Knowledge INDEX.md Template (knowledge/INDEX.md)

```markdown
---
type: index
scope: master
file_count: 0
last_updated: {{YYYY-MM-DD}}
---

# Knowledge Base Index

> {{Project domain}} — Atomized for efficient retrieval

## Quick Reference

| Category | Files | Purpose |
|----------|-------|---------|
| `overview/` | 0 | Executive summary, philosophy |
| `components/` | 0 | Component deep dives |
| `operational-patterns/` | 0 | Workflow patterns |
| `reference/` | 0 | Conceptual frameworks |

## Navigation Guide

### New to this project?
1. Start with `overview/executive-summary.md` (when created)
2. Read `overview/architecture-philosophy.md` (when created)

### Search Tips
- Use `grep` for specific terms across files
- Check INDEX.md in each category for file summaries
- Follow `related` links in file frontmatter
```

**Notes**:
- Regenerate via `index-kb` skill (`/cab:kb-index`) after KB file changes
- For KB conventions (≤300L per file, `source:` frontmatter, etc.):
  `.claude/rules/kb-conventions.md`
- For KB structure patterns: `knowledge/components/knowledge-base-structure.md`
