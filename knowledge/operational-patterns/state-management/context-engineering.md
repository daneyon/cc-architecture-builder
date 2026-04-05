---
id: context-engineering
title: Practical Context Engineering
category: operational-patterns/state-management
tags: [context, optimization, 200-line, compaction, prompt-cache, auto-memory, tokens]
summary: Practical context engineering patterns for CC — the 200-line discipline for CLAUDE.md, compaction mechanics, prompt cache optimization, auto memory interaction, and strategies for maximizing context efficiency.
depends_on: [architecture-philosophy, session-lifecycle]
related: [filesystem-patterns, cost-model, memory-claudemd]
complexity: intermediate
last_updated: 2026-04-05
estimated_tokens: 900
confidence: B
review_by: 2026-07-05
revision_note: "v1.0 — NEW KB card. Consolidates context engineering guidance from design-principles, session-management, and v3 observable findings."
---

# Practical Context Engineering

## Core Principle

Context engineering is curating what the model sees — not just what you ask, but the entire information environment. Every token of configuration displaces productive output.

---

## The 200-Line Discipline (CLAUDE.md Only)

CC officially recommends **≤200 lines per CLAUDE.md file**. This applies to:

| File | Constraint | Enforced By |
|------|-----------|-------------|
| CLAUDE.md (all 4 scopes) | ≤200 lines recommended | CC docs best practice |
| MEMORY.md (auto memory) | 200 lines / 25KB hard cap | System truncation |
| KB docs, skills, rules, agents | No CC-imposed limit | Loaded on-demand |
| @imported files | No CC-imposed limit | Loaded when referenced |

**Why 200 lines**: CLAUDE.md loads at every session start, consuming main context. KB files, skills, and @imports load on-demand and don't have this constraint. CAB recommends keeping KB files focused (~150-250 lines) for retrieval ergonomics, but this is a design guideline, not a platform constraint.

### Staying Under 200 Lines

1. **Seed instructions over procedures** — Write durable guidance, not step-by-step recipes. "Verify before commit" not "run npm test, then run npm lint, then run git diff..."
2. **@import for depth** — Reference detailed content: `@rules/dev/practices.md`, `@notes/progress.md`
3. **Skills for workflows** — Move repeatable procedures into skill SKILL.md files that load only when triggered
4. **Rules for scoped policies** — Use `.claude/rules/` with `paths:` frontmatter for context-specific instructions
5. **Let auto memory handle learning** — Don't manually track corrections in CLAUDE.md if auto memory is enabled

---

## Compaction Mechanics (Observable Behavior)

### Threshold Formula

```
effectiveContextWindow = contextWindowForModel - min(modelMaxTokens, 20_000)
autoCompactThreshold   = effectiveContextWindow - 13_000
warningThreshold       = effectiveContextWindow - 20_000
```

### What Survives Compaction

| Content | Survives? | How |
|---------|----------|-----|
| CLAUDE.md | ✅ Yes | Re-read from disk after compaction |
| Auto Memory (MEMORY.md) | ✅ Yes | Re-read from disk |
| Invoked skill content | ✅ Yes | Re-injected in summary |
| Non-invoked skill metadata | ❌ Partially | Descriptions may be dropped |
| Conversation details | ❌ Summarized | Compressed to structured summary |
| Tool call results | ❌ Summarized | MicroCompact edits cached results first |

### Compaction Strategy

| Context % | Action |
|----------|--------|
| <50% | Continue normally |
| 50-70% | Monitor; prepare to compact if doing heavy work |
| 70-80% | **Compact proactively**: `/compact focus on [current task]` |
| 80-90% | Auto-compact may fire; expect some context loss |
| >90% | Likely forced compaction; consider fresh session instead |

**After any compaction**: Re-read `notes/progress.md` and restate current objective. Extension awareness degrades after compaction — check skill availability before delegating.

---

## Prompt Cache Optimization

CC's prompt cache provides ~200x cost savings on cache hits at scale. Patterns that preserve cache:

**Do**:
- Keep CLAUDE.md content stable across turns (edits bust cache)
- Front-load stable instructions; dynamic content later
- Use consistent tool invocation patterns
- Batch subagent tasks within sessions (subsequent agents hit cache)

**Don't**:
- Edit CLAUDE.md mid-session (busts cache for all subsequent turns)
- Add/remove MCP servers mid-session (cache boundary shifts)
- Restructure system prompt content frequently

---

## Auto Memory Interaction

CC's auto memory system (`MEMORY.md` + topic files) operates alongside CLAUDE.md:

- **MEMORY.md** (200-line index): Loaded every session, contains pointers to topic files
- **Topic files**: Loaded on-demand via grep-based pattern matching (no vector search)
- **Write triggers**: User says "remember this", agent extracts corrections/patterns, autoDream consolidation
- **Categories**: user (preferences), feedback (corrections), project (architecture), reference (external)

**CAB integration**: Auto memory handles short-term learning and corrections. CAB's `notes/` system handles structured operational state (task tracking, progress, decision logs). They complement each other:

| Need | Use |
|------|-----|
| "Remember I prefer X" | Auto memory (CC-native) |
| "Track task progress across sessions" | `notes/progress.md` (CAB pattern) |
| "Store architectural decisions" | Either — auto memory for quick recall, `notes/` for structured audit trail |
| "Bootstrap a fresh session" | `notes/progress.md` + CLAUDE.md (CAB bootstrap protocol) |

---

## Context Budget Planning

For projects with many extensions, estimate context budget:

| Component | Approximate Cost |
|-----------|-----------------|
| CLAUDE.md (200 lines) | ~3K tokens |
| Each skill metadata | ~100 tokens |
| Each rule file (loaded) | ~500-2K tokens |
| Auto Memory (200 lines) | ~3K tokens |
| MCP tool schemas (if not deferred) | ~200 tokens/tool |
| **Remaining for actual work** | **Everything else** |

**Rule of thumb**: 10 skills + 5 rules + CLAUDE.md + auto memory ≈ 10-15K tokens of context overhead. On a 200K context window, that's ~7%. On 1M extended context, it's negligible.

## See Also

- [Session Lifecycle](session-lifecycle.md) — Context health, compaction decision framework
- [Filesystem Patterns](filesystem-patterns.md) — Persistent state that survives compaction
- [Architecture Philosophy](../../overview/architecture-philosophy.md) — 200-line discipline, progressive disclosure
- [Cost Model](../orchestration/cost-model.md) — Token economics, prompt cache details
