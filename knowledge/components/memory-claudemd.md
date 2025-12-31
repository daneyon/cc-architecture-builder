---
id: memory-claudemd
title: Memory System (CLAUDE.md)
category: components
tags: [memory, claude-md, instructions, imports, hierarchy, rules]
summary: Complete guide to Claude Code's memory system including CLAUDE.md files, project rules, imports, and the 5-tier memory hierarchy.
depends_on: [architecture-philosophy]
related: [agent-skills, subagents, knowledge-base-structure]
complexity: foundational
last_updated: 2025-12-23
estimated_tokens: 900
source: https://code.claude.com/docs/en/memory
---

# Memory System (CLAUDE.md)

## Overview

Claude Code's memory system enables persistent instructions across sessions. Memory files are automatically loaded into context when Claude Code launches.

**Source**: [Manage Claude's memory](https://code.claude.com/docs/en/memory)

---

## Memory Types (5-Tier Hierarchy)

Claude Code offers five memory locations in a hierarchical structure:

| Memory Type | Location | Purpose | Shared With |
|---|---|---|---|
| **Enterprise policy** | System paths* | Organization-wide standards | All org users |
| **Project memory** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared instructions | Team via git |
| **Project rules** | `./.claude/rules/*.md` | Modular, topic-specific instructions | Team via git |
| **User memory** | `~/.claude/CLAUDE.md` | Personal preferences (all projects) | Just you |
| **Project memory (local)** | `./CLAUDE.local.md` | Personal project-specific | Just you |

*Enterprise paths:
- macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
- Linux: `/etc/claude-code/CLAUDE.md`
- Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`

**Precedence**: Files higher in hierarchy load first and take precedence.

**Note**: `CLAUDE.local.md` files are automatically added to `.gitignore`.

---

## Project Rules (.claude/rules/)

For larger projects, organize instructions into modular files:

```
.claude/
├── CLAUDE.md           # Main project instructions
└── rules/
    ├── code-style.md   # Code style guidelines
    ├── testing.md      # Testing conventions
    └── security.md     # Security requirements
```

All `.md` files in `.claude/rules/` are automatically loaded as project memory.

### Path-Specific Rules

Rules can be scoped to specific files using YAML frontmatter:

```yaml
---
paths: src/api/**/*.ts
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
```

Rules without a `paths` field apply to all files.

### Glob Patterns

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files |
| `src/**/*` | All files under `src/` |
| `*.md` | Markdown files in root |
| `{src,lib}/**/*.ts` | TS files in src or lib |

### User-Level Rules

Personal rules that apply to all projects:

```
~/.claude/rules/
├── preferences.md    # Personal coding preferences
└── workflows.md      # Preferred workflows
```

User-level rules are loaded before project rules (project rules have higher priority).

---

## CLAUDE.md Imports

Import additional files using `@path/to/file` syntax:

```markdown
See @README for project overview.
See @docs/architecture.md for system design.

# Individual Preferences (for team projects)
@~/.claude/my-project-instructions.md
```

**Rules**:
- Both relative and absolute paths allowed
- Imports are recursive (max depth: 5 hops)
- Imports inside code blocks are ignored
- Use `/memory` command to see loaded files

**Team Tip**: Import user-specific files from home directory as an alternative to `CLAUDE.local.md` that works better across git worktrees.

---

## Memory Lookup Behavior

Claude Code reads memories recursively from current directory upward (stopping before root `/`).

**Example**: Working in `foo/bar/`:
- Claude finds both `foo/CLAUDE.md` and `foo/bar/CLAUDE.md`
- Subtree CLAUDE.md files are loaded when Claude reads files in those subtrees

---

## Commands

| Command | Purpose |
|---------|---------|
| `/memory` | View all loaded memory files |
| `/init` | Bootstrap a CLAUDE.md for your codebase |

---

## Best Practices

| Do | Don't |
|----|-------|
| Be specific: "Use 2-space indentation" | Be vague: "Format code properly" |
| Use bullet points for instructions | Write long paragraphs |
| Group related memories under headings | Mix unrelated instructions |
| Keep files under 500 lines | Bloat with rarely-used instructions |
| Use `@imports` for detailed material | Inline everything |
| Use `.claude/rules/` for modular organization | Put everything in one CLAUDE.md |

---

## Example Project Memory

```markdown
# Project Name

## Build Commands
- `npm run dev` - Start development server
- `npm test` - Run tests
- `npm run lint` - Check code style

## Code Style
- Use TypeScript strict mode
- Prefer functional components
- 2-space indentation

## Architecture
- `/src/components` - React components
- `/src/services` - API clients
- `/src/utils` - Shared utilities

## Personal Preferences (Optional)
@~/.claude/my-preferences.md
```

---

## See Also

- [Architecture Philosophy](../overview/architecture-philosophy.md) — Memory hierarchy principles
- [Agent Skills](agent-skills.md) — Model-invoked capabilities
- [Knowledge Base Structure](knowledge-base-structure.md) — Organizing domain knowledge
