---
id: knowledge-base-structure
title: Knowledge Base Structure
category: components
tags: [knowledge-base, retrieval, indexing, organization, rag]
summary: Organization patterns for domain knowledge optimized for Claude Code retrieval. Covers atomic content structures, indexing strategies, and scaling considerations.
depends_on: [memory-claudemd]
related: [mcp-integration, agent-skills]
complexity: intermediate
last_updated: 2025-12-12
estimated_tokens: 800
revision_note: Content may be revised as Appendix C (Knowledge Base Deep Dive) finalizes.
---

# Knowledge Base Structure

> **Note**: This section provides foundational guidance. Advanced techniques (knowledge graphs, semantic indexing, atomic structures) are planned for **Appendix C: Knowledge Base Deep Dive**.

## Critical Understanding

Claude Code does **not** have built-in RAG/semantic search. Unlike Claude Web Projects where Anthropic handles retrieval, Claude Code requires explicit knowledge organization:

| Claude Web | Claude Code |
|------------|-------------|
| Upload files, automatic retrieval | Files on filesystem, explicit access |
| Semantic search built-in | grep/glob/read discovery |
| Context managed for you | You manage what Claude sees |

## Retrieval Flow

```
User Query
    │
    ▼
┌────────────────────────────────────────┐
│ 1. CLAUDE.md (loaded at session start) │
│    Points Claude to INDEX files        │
└────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────┐
│ 2. INDEX.md (Claude reads on demand)   │
│    Lists available files with summaries│
└────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────┐
│ 3. Specific files (Claude reads)       │
│    Based on relevance assessment       │
└────────────────────────────────────────┘
```

## Three-Level Framework

### Level 1: Simple (< 20 files)

```
knowledge/
├── INDEX.md              # Simple list with descriptions
├── core-concept-1.md
├── core-concept-2.md
└── examples/
    └── example-1.md
```

### Level 2: Structured (20-100 files)

```
knowledge/
├── INDEX.md                    # Master index
├── concepts/
│   ├── INDEX.md
│   └── *.md
├── procedures/
│   ├── INDEX.md
│   └── *.md
├── reference/
│   ├── INDEX.md
│   └── *.md
├── examples/
│   ├── INDEX.md
│   └── *.md
└── templates/
    ├── INDEX.md
    └── *.md
```

### Level 3: Scalable (100+ files)

Level 2 structure plus:

```
knowledge/
├── .meta/
│   ├── manifest.json       # All files with metadata
│   ├── tags.json           # Tag taxonomy
│   └── relationships.json  # File relationships
└── [Level 2 structure]
```

Plus MCP integration for semantic search.

## Atomic Content Principles

Files should be:

| Property | Why | Target |
|----------|-----|--------|
| **Self-contained** | Understandable alone | Include necessary context |
| **Single-purpose** | One concept per file | Easier relevance assessment |
| **Well-named** | Filename = content hint | Enables grep discovery |
| **Sized appropriately** | Balance context vs tokens | 200-500 lines |
| **Metadata-rich** | Frontmatter for filtering | Claude decides before full read |

## File Metadata Schema

```yaml
---
id: unique-identifier
title: Human Readable Title
category: concepts | procedures | reference | examples | templates
tags: [tag1, tag2, tag3]
summary: One-sentence description for INDEX listing.
depends_on: [prerequisite-file-ids]
related: [related-file-ids]
last_updated: 2025-12-12
complexity: foundational | intermediate | advanced
---
```

## INDEX.md Format

```markdown
---
type: index
scope: category-name
file_count: N
last_updated: 2025-12-12
---

# Category Name Index

> Brief category description

## Quick Reference

| File | Summary | Tags |
|------|---------|------|
| file-1.md | One-sentence summary | tag1, tag2 |
| file-2.md | One-sentence summary | tag1, tag3 |

## Reading Order (Recommended)

1. file-1.md — Start here
2. file-2.md — After understanding file-1

## By Complexity

### Foundational
- file-1.md

### Intermediate
- file-2.md
```

## Directory Structure Guidelines

| Directory | Purpose | Content Type |
|-----------|---------|--------------|
| `concepts/` | Foundational understanding | What things are |
| `procedures/` | How-to knowledge | How to do things |
| `reference/` | Lookup materials | Specifications, standards |
| `examples/` | Calibration materials | Sample inputs/outputs |
| `templates/` | Reusable patterns | Starting points |

## Access Patterns

| Pattern | When | Implementation |
|---------|------|----------------|
| **Direct @import** | Always-needed content | In CLAUDE.md |
| **Skill reference** | Procedural knowledge | Link in SKILL.md |
| **On-demand** | Large reference docs | Claude reads via filesystem |
| **MCP query** | Semantic search needed | Vector database MCP |

## CLAUDE.md Integration

```markdown
## Knowledge Base

Domain knowledge is organized in `knowledge/`:

- `knowledge/INDEX.md` — Master catalog
- `knowledge/concepts/` — Foundational understanding
- `knowledge/procedures/` — How-to guides
- `knowledge/reference/` — Specifications and standards

For domain questions, first consult `knowledge/INDEX.md` to identify relevant files.
```

## Scaling Decision Guide

| Situation | Recommendation |
|-----------|----------------|
| < 20 files | Level 1, direct structure |
| 20-100 files | Level 2, category indexes |
| 100+ files | Level 3, MCP semantic search |
| Frequent cross-referencing | Add relationships.json |
| Complex taxonomies | Add tags.json |

## Best Practices

1. **Always create INDEX files**: Claude needs catalogs to discover content
2. **Use consistent naming**: `kebab-case.md` throughout
3. **Include metadata**: Frontmatter enables smart filtering
4. **Keep files focused**: Split large files into atomic units
5. **Update indexes**: Regenerate when adding files
6. **Link explicitly**: No automatic semantic linking

## Anti-Patterns

| Don't | Why | Instead |
|-------|-----|---------|
| Dump files without INDEX | Claude can't discover | Create INDEX.md |
| One huge file | Token-expensive | Split into atomic units |
| Vague filenames | Hurts grep discovery | Descriptive names |
| Skip metadata | Loses filtering ability | Always add frontmatter |
| Assume semantic search | Not built-in | Use explicit structure |

## See Also

- [MCP Integration](mcp-integration.md) — For semantic search at scale
- [Memory System](memory-claudemd.md) — CLAUDE.md integration
- Appendix C: Knowledge Base Deep Dive (planned)
