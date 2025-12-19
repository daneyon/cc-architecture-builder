---
id: memory-claudemd
title: Memory System (CLAUDE.md)
category: components
tags: [memory, claude-md, imports, hierarchy, instructions]
summary: CLAUDE.md memory system including file hierarchy, @import syntax, lookup behavior, and best practices for persistent instructions.
depends_on: [architecture-philosophy]
related: [agent-skills, global-user-config, distributable-plugin]
complexity: foundational
last_updated: 2025-12-12
estimated_tokens: 650
---

# Memory System (CLAUDE.md)

## Overview

CLAUDE.md files serve as **persistent memory**—instructions that Claude reads at the start of every session. They form the foundation of custom LLM behavior.

## Memory Hierarchy

Claude Code reads CLAUDE.md files from multiple locations with defined precedence:

| Tier | Location | Purpose |
|------|----------|---------|
| 1 | Enterprise policy | Organization standards |
| 2 | `~/.claude/CLAUDE.md` | Personal (all projects) |
| 3 | `./CLAUDE.md` | Project (team-shared) |
| 4 | `./subdir/CLAUDE.md` | Subtree-specific |

**Precedence**: Higher tiers load first and take precedence.

## Import Syntax

CLAUDE.md files can import additional files using `@path/to/file`:

```markdown
# Project Instructions

See @README.md for project overview.
See @docs/architecture.md for system design.

## Personal Preferences
@~/.claude/my-preferences.md
```

### Import Rules

| Rule | Description |
|------|-------------|
| Relative paths | `@docs/guide.md` — relative to current file |
| Absolute paths | `@~/.claude/prefs.md` — from home directory |
| Max depth | 5 hops (imports can import, up to 5 levels) |
| Code blocks | Imports inside code blocks are ignored |
| Missing files | Claude proceeds without error |

## Lookup Behavior

Claude reads memories **recursively from current directory upward**:

1. Starting in `foo/bar/`, Claude finds both:
   - `foo/bar/CLAUDE.md`
   - `foo/CLAUDE.md`
2. Subtree CLAUDE.md files load when Claude reads files in those directories

### View Loaded Memories

```
/memory
```

Shows all currently loaded memory files.

### Quick Add Memory

```
# some instruction to remember
```

The `#` shortcut adds to project CLAUDE.md.

## Best Practices

### Do

| Practice | Example |
|----------|---------|
| Be specific | "Use 2-space indentation" |
| Use bullet points | Individual, scannable instructions |
| Group related items | Under clear headings |
| Keep concise | Under 500 lines total |
| Use @imports | For detailed reference material |

### Don't

| Avoid | Why |
|-------|-----|
| Vague instructions | "Format code properly" — too ambiguous |
| Long paragraphs | Hard to scan, easy to miss |
| Mixed topics | Group related instructions |
| Bloated files | Move details to referenced files |
| Inline everything | Use @imports for large content |

## Template Structure

```markdown
# Project Name

## Purpose
[One-line description]

## Core Instructions
[Essential behaviors]

## Knowledge Base
See `knowledge/INDEX.md` for available resources.

## Constraints
[What NOT to do]

## Optional Imports
@~/.claude/personal-preferences.md
```

## Memory vs Skills

| Aspect | CLAUDE.md | Skills |
|--------|-----------|--------|
| Loading | Always at startup | When triggered |
| Purpose | Baseline instructions | Specific capabilities |
| Scope | Session-wide | Task-specific |
| Size | Keep small (< 500 lines) | Can be larger |

Use CLAUDE.md for always-needed instructions. Use Skills for specific procedures that should only load when relevant.

## See Also

- [Agent Skills](agent-skills.md) — Model-invoked capabilities
- [Global User Config](../schemas/global-user-config.md) — Personal CLAUDE.md
- [Architecture Philosophy](../overview/architecture-philosophy.md) — Hierarchy details
