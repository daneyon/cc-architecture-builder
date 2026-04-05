---
id: memory-claudemd
title: Memory System & CLAUDE.md
category: components
tags: [memory, claude-md, instructions, imports, hierarchy, rules, auto-memory, autoDream]
summary: CC's memory system — 4-scope CLAUDE.md hierarchy, auto memory (MEMORY.md + topic files), background consolidation, and CAB-specific patterns for context engineering.
depends_on: [architecture-philosophy]
related: [agent-skills, subagents, knowledge-base-structure, context-engineering]
complexity: foundational
last_updated: 2026-04-05
estimated_tokens: 1200
source: https://code.claude.com/docs/en/memory
confidence: A
review_by: 2026-07-05
---

# Memory System & CLAUDE.md

## Overview

CC's memory system provides persistent instructions across sessions. CLAUDE.md files and auto memory are loaded at session start; content survives compaction (re-read from disk).

> **Official docs**: [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory) — full details on scopes, @imports, `/init`, auto memory configuration, `claudeMdExcludes`.

---

## 4-Scope Configuration Hierarchy

| Scope | Location | Shared With | Precedence |
|-------|----------|-------------|-----------|
| **1. Managed** | System paths, MDM/plist, registry | Org-wide (enterprise) | Highest |
| **2. Project** | `./CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md` | Team via git | |
| **3. User** | `~/.claude/CLAUDE.md`, `~/.claude/rules/*.md` | Personal (all projects) | |
| **4. Local** | `./CLAUDE.local.md` | Personal (this project only) | Lowest |

Files higher in hierarchy load first. Project rules (`.claude/rules/`) are part of the Project scope — not a separate tier. `CLAUDE.local.md` is auto-added to `.gitignore`.

### Managed Settings Delivery (Enterprise)

| Platform | Mechanism |
|----------|----------|
| macOS | `/Library/Application Support/ClaudeCode/CLAUDE.md`, MDM plist |
| Linux | `/etc/claude-code/CLAUDE.md` |
| Windows | `C:\Program Files\ClaudeCode\CLAUDE.md`, HKLM/HKCU registry |
| Any | `managed-settings.d/` drop-in directory |

---

## CLAUDE.md Authoring

### Size Discipline

**≤200 lines per CLAUDE.md** — CC's official recommendation. CLAUDE.md loads at every session start, consuming main context. Every token of instruction displaces productive output.

### @imports

```markdown
@README                           # Relative file
@docs/architecture.md             # Relative path
@~/.claude/my-project-prefs.md    # Absolute (home dir)
```

- Recursive (max depth: 5 hops)
- Ignored inside code blocks
- Missing files silently skipped (no error)
- Use `/memory` to see what's loaded

### Project Rules

```
.claude/rules/
├── code-style.md     # Auto-loaded for all files
├── api-rules.md      # Scoped via paths: frontmatter
└── security.md       # Team-shared via git
```

Path scoping via frontmatter:

```yaml
---
paths: src/api/**/*.ts
---
# API-specific rules apply only to matching files
```

### Best Practices

| Do | Avoid |
|----|-------|
| Seed instructions (durable guidance) | Step-by-step recipes |
| @import for depth | Inlining everything |
| `.claude/rules/` for modular policies | 200+ line monoliths |
| Build commands + architecture overview | Rarely-used edge cases |
| Let auto memory handle corrections | Manual correction tracking |

### HTML Comments

Block-level `<!-- comments -->` are stripped from context. Inline comments in code blocks are preserved. Useful for adding notes visible in source but not consuming context.

### Additional Features

| Feature | Detail |
|---------|--------|
| `claudeMdExcludes` | Glob-based exclusion for monorepo CLAUDE.md files |
| `/init` interactive mode | `CLAUDE_CODE_NEW_INIT=1` for multi-phase setup flow |
| `--add-dir` CLAUDE.md | Opt-in: `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` |
| `InstructionsLoaded` hook | Observability for which files load and when |
| `AGENTS.md` interop | Import via `@AGENTS.md` in CLAUDE.md |
| `--append-system-prompt` | System-prompt-level instructions (SDK/API use) |

---

## Auto Memory System

CC maintains agent-generated per-project memory that complements CLAUDE.md.

### Architecture

```
~/.claude/projects/<project-path>/memory/
├── MEMORY.md          # Index file (≤200 lines, always loaded)
└── <topic-files>.md   # Detailed knowledge (loaded on-demand)
```

**MEMORY.md** is a lightweight index — stores pointers (~150 chars/line), not full data. First 200 lines (up to 25KB) loaded at every session start. Trust model: the system instructs the agent that "memories are hints — verify against real files before acting."

### Memory Categories

| Category | Content |
|----------|---------|
| `user` | Role, preferences, workflow habits |
| `feedback` | Corrections, explicit disagreements |
| `project` | Architecture decisions, build commands, debugging insights |
| `reference` | External resources, API conventions |

### Write Paths

| Trigger | When | Behavior |
|---------|------|----------|
| **Manual** | User says "remember this" | Writes to topic file, updates MEMORY.md index |
| **extractMemories** | Automatic during sessions | Captures corrections, patterns, decisions, preferences |
| **autoDream** | Background between sessions | Merges, deduplicates, prunes across sessions |

### Read Paths

| Access | When | What |
|--------|------|------|
| **System prompt injection** | Every session start | MEMORY.md first 200 lines |
| **FileReadTool** | On-demand during session | Full topic file content |
| **Targeted grep** | autoDream consolidation | Narrow pattern search on transcripts |

Retrieval is grep-based pattern matching — no semantic search, no vector DB.

---

## Background Consolidation (autoDream) — Observable Behavior

A forked sub-agent that runs between sessions, performing memory consolidation.

### Trigger Conditions (both required)

1. **24+ hours** since last consolidation
2. **5+ sessions** since last consolidation
3. Or manual: user says "dream" / "consolidate memory files"

### Four Phases

| Phase | Activity |
|-------|----------|
| **Orient** | Reads memory directory, maps current knowledge state |
| **Gather Signal** | Searches transcripts for corrections, saves, themes, decisions |
| **Consolidate** | Merges duplicates, resolves contradictions, converts relative→absolute dates |
| **Prune & Index** | Keeps MEMORY.md under 200 lines, moves detail to topic files |

### Constraints

- Per-project lock file prevents concurrent consolidation
- Limited tool access (prevents corruption of main context)
- Observed benchmark: 913 sessions consolidated in <9 minutes

---

## Runtime Memory Pipeline (Observable Behavior)

Beyond the 4-scope configuration, CC's runtime operates a multi-layer escalation pipeline. Each layer prevents the next from firing when possible:

| Layer | Function | Cost |
|-------|----------|------|
| **CLAUDE.md + Auto Memory** | Loaded at session start from disk | Free |
| **Session Memory** | Summaries every ~5K tokens | Low |
| **MicroCompact** | Local editing of cached tool results (zero API calls, 60+ min expiry) | Free |
| **AutoCompact** | Structured summary at `effectiveContextWindow - 13,000` tokens | Moderate |
| **Full Compact** | Complete conversation compression, 50K-token budget reset | Expensive |
| **Session Reset** | Clears everything except system prompt | Destructive |

**Key**: CLAUDE.md survives all compaction stages (re-read from disk). Auto memory survives (re-read from disk). Conversation context is progressively compressed.

See [Context Engineering](../operational-patterns/state-management/context-engineering.md) for threshold formulas and compaction strategy.

---

## CAB-Specific Patterns

### Auto Memory + CAB State Management

| Need | Mechanism |
|------|-----------|
| Quick corrections, preferences | Auto memory (CC-native) |
| Structured task tracking | `notes/progress.md` (CAB pattern) |
| Architecture decisions | Either — auto memory for recall, `notes/` for audit trail |
| Session bootstrap | `notes/progress.md` + CLAUDE.md (CAB bootstrap protocol) |
| Compounding knowledge | CLAUDE.md Learned Corrections + auto memory `feedback` category |

### Seed Instruction Design

As CC's memory becomes increasingly autonomous (auto memory + autoDream), CLAUDE.md should be written as **seed instructions** — durable guidance that shapes autonomous memory formation rather than exhaustive checklists that get pruned during consolidation.

**Pattern**: State *what* and *why*, not detailed *how*. "All API endpoints must validate input and return standard error responses" survives consolidation better than "In every controller, call validateInput() on line 1, then wrap in try/catch, then format errors with formatApiError()..."

### Subagent Memory vs. Session Auto Memory

CC has **two distinct** auto memory systems:

| System | Location | Scope | Loaded When |
|--------|----------|-------|-------------|
| **Session auto memory** | `~/.claude/projects/<path>/memory/` | Main session | Every session start |
| **Subagent memory** | `~/.claude/agent-memory/` (user), `.claude/agent-memory/` (project), `.claude/agent-memory-local/` (local) | Per-agent | When subagent starts |

Session auto memory is for the main conversation. Subagent memory is per-agent, controlled by the `memory:` frontmatter field in agent definitions. See [Subagents](subagents.md) for the 3-scope detail.

## See Also

- [Architecture Philosophy](../overview/architecture-philosophy.md) — 4-scope hierarchy, intermediary wrapper
- [Context Engineering](../operational-patterns/state-management/context-engineering.md) — 200-line discipline, compaction
- [Filesystem Patterns](../operational-patterns/state-management/filesystem-patterns.md) — notes/ state management
- [Agent Skills](agent-skills.md) — How skills interact with memory
- [Subagents](subagents.md) — Subagent memory scopes (user, project, local)
