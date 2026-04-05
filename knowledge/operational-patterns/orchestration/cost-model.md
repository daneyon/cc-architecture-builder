---
id: cost-model
title: Multi-Agent Cost Model & Optimization
category: operational-patterns/orchestration
tags: [cost, tokens, optimization, prompt-cache, forked-agents, economics]
summary: Token economics for multi-agent systems, prompt cache optimization, forked agent cost patterns, and decision frameworks for when multi-agent coordination is justified.
depends_on: [orchestration-framework]
related: [delegation-templates, context-engineering, collaboration-patterns]
complexity: advanced
last_updated: 2026-04-05
estimated_tokens: 800
source: CAB-original (with observable data)
confidence: B
review_by: 2026-07-05
revision_note: "v3.0 — Added forked agent cost pattern, prompt cache optimization (observable behavior), updated economics."
---

# Multi-Agent Cost Model & Optimization

## Token Economics

| Configuration | Relative Token Cost | Notes |
|---------------|--------------------:|-------|
| Chat interaction (baseline) | 1x | Human ↔ Claude conversation |
| Single autonomous agent | ~4x | Agent with tool use and reasoning |
| Multi-agent system | ~15x | Orchestrator + specialist agents |
| Agent Teams (experimental) | ~7x per teammate | Shared coordination overhead |

Token usage alone explains ~80% of performance variance in agent systems. Before adding agents, consider whether spending equivalent tokens on a single better-prompted agent would yield comparable results.

---

## Prompt Cache Optimization (Observable Behavior)

CC implements aggressive prompt caching. At 200K tokens, a cache hit costs ~$0.003 vs ~$0.60 for a miss — a 200x difference.

**Cache architecture** (observable through billing patterns):

- System prompt has stable sections (cached globally) + dynamic sections (rebuilt per session)
- Cache-busting boundaries placed after MCP instructions so adding/removing MCP servers doesn't invalidate cached prefixes
- Permission results cached for ~1 hour (60-80% hit rate)

**Actionable optimization**:

1. **Keep CLAUDE.md stable** — frequent edits to CLAUDE.md bust the cache for every subsequent turn
2. **Front-load stable context** — rules, persistent instructions at the start; dynamic content later
3. **Minimize MCP server churn** — adding/removing servers mid-session breaks cache
4. **Use subagents for exploratory work** — their context is separate; cache-busting doesn't affect main session
5. **Prefer consistent tool usage patterns** — tool schemas are part of the cached prefix

---

## Forked Agent Cost Pattern (Observable Behavior)

Background operations (session memory extraction, auto memory writes, compaction, agent summaries) use **forked agents** that inherit the parent's system prompt + tools + message prefix. This enables ~76% cost reduction through shared prompt cache.

**CAB application**: When designing subagent delegation:

- Subagents sharing the same project CLAUDE.md benefit from prompt cache sharing
- The first subagent pays full price; subsequent subagents in the same session hit cache
- This favors batching multiple subagent tasks within a single session over spreading across sessions

---

## Cost Optimization Levers

| Lever | Impact | How |
|-------|--------|-----|
| **Effort level** | Direct token control | `low` / `medium` / `high` — match to task complexity |
| **Model selection** | Quality vs cost | Upgrading model tier often beats doubling token budget at same tier |
| **Context isolation** | Preserve main context | Subagents consume their own tokens; keeps main session lean |
| **Worktrees over Teams** | Separate budgets | Worktrees run independent sessions; Teams shares coordination overhead |
| **Progressive disclosure** | Load less upfront | Skills/knowledge on demand, not pre-loaded in rules/ |
| **Prompt cache** | 200x savings on hits | Keep system prompt stable, front-load persistent content |

---

## When Multi-Agent is Justified

Multi-agent coordination is justified when **task value exceeds token cost** AND at least one holds:

- Task requires more knowledge than fits in a single context window
- Task benefits from genuinely different expertise (not just parallelism)
- Task requires sustained work across multiple phases with different tooling
- Task failure cost is high enough to warrant evaluator-optimizer loops
- Task involves independent subtasks that can run in parallel (time savings > cost)

**Decision matrix**:

| Task Complexity | Recommended Config | Typical Cost |
|-----------------|-------------------|-------------|
| Simple fact-finding | 1 agent, 3-10 tool calls | ~4x |
| Direct comparison | 2-4 subagents, 10-15 calls each | ~15x |
| Comprehensive research | 5-10+ subagents, clear division | ~30-50x |
| Multi-phase lifecycle | Orchestrator + state management | ~50-100x |

**Cost benchmarks** (CC official): ~$6/dev/day, $100-200/dev/month with Sonnet.

> **Official docs**: [Costs](https://code.claude.com/docs/en/costs) — pricing details, context window costs, 1M extended context.

## See Also

- [Orchestration Framework](framework.md) — When to use which pattern
- [Context Engineering](../state-management/context-engineering.md) — Reducing context waste
- [Delegation Templates](delegation-templates.md) — Structuring efficient delegations
