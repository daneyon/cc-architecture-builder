---
id: extension-discovery
title: Extension Discovery & Persistence
category: operational-patterns
tags: [skills, context-degradation, reinforcement, compaction, extension-awareness]
summary: Why Claude loses awareness of available extensions mid-session, and the Three-Point Reinforcement Pattern to mitigate it. Applies to any project with 3+ skills.
depends_on: [agent-skills, session-management, orchestration-framework]
related: [memory-claudemd, multi-agent-collaboration]
complexity: intermediate
last_updated: 2026-03-26
estimated_tokens: 900
revision_note: "v1.0 — Pattern extracted from HydroCast P1-06 research. Generalized for cross-project use."
---

# Extension Discovery & Persistence

## The Problem

Claude autonomously selects skills via semantic matching against the context window. This works reliably at session start but degrades predictably as conversation grows. The result: Claude "forgets" available extensions mid-session and implements logic manually that an existing skill already handles.

This is not a bug — it's a structural consequence of how LLMs attend to context.

## Root Cause Analysis

Five compounding factors:

| Factor | Mechanism | Impact |
| ------ | --------- | ------ |
| No explicit manifest | CLAUDE.md references extensions indirectly ("see skills/ directory") | Model must discover extensions via filesystem, not direct lookup |
| Generic trigger keywords | Words like "validate", "compare", "predict" overlap with normal conversation | Model can't distinguish discussion of a concept from intent to invoke a skill |
| Lost-in-middle attention decay | Extension metadata loads after system prompt + rules (~10-15K tokens in) | Attention to skill descriptions drops as conversation context grows |
| Subagent context isolation | Delegated agents inherit CLAUDE.md but not the parent's runtime skill awareness | Subagents bypass available skills entirely |
| Compaction is lossy | No automatic refresh of extension awareness after `/compact` | Each compaction may drop skill metadata from working memory |

**Key insight**: The ~50-60 skill practical limit (documented in orchestration-framework.md) is a metadata budget constraint. The discovery problem is an *attention* constraint — even 5 skills can be forgotten if their descriptions don't create strong enough anchors.

## Solution: Three-Point Reinforcement Pattern

Mitigate attention decay by placing extension awareness at three independent reinforcement points. Each compensates for the others' failure modes:

```
Point 1: Static Declaration (CLAUDE.md)
  - Task-to-extension mapping table
  - Placed in first ~500 tokens (high-attention zone)
  - Survives initial context loading

Point 2: Behavioral Rule (rules/capabilities.md)
  - Mandatory invocation rules + anti-patterns
  - Loaded during rule evaluation phase
  - Provides "DO NOT implement X manually" guardrails

Point 3: Dynamic Re-Anchoring
  - Orchestrator Step 0: "Check extensions before executing"
  - Post-compaction re-read instruction
  - Recovers awareness after lossy compaction
```

### Why three points, not one?

Each point addresses a different phase of the context lifecycle:
- **Point 1** catches initial loading (U-shaped attention: strong at start)
- **Point 2** catches rule evaluation (separate processing phase from conversation)
- **Point 3** catches runtime degradation (compaction recovery, long sessions)

A single point placed anywhere is sufficient early in a session but fails as context grows. Three points provide redundancy without token bloat (~200 tokens total across all three).

## Implementation Guide

### Point 1: CLAUDE.md Extension Table

Add near the top of the project's CLAUDE.md, before detailed sections:

```markdown
## Available Extensions (Quick Reference)

Before executing any task, check this table. Use existing skills rather than manual implementation.

| When You Need To... | Skill | Pipeline Position |
| ------------------- | ----- | ----------------- |
| [task description]  | `skill-name` | [order context] |
```

Include an anti-pattern note:
> Do NOT implement [domain logic] manually when these skills exist. Invoke the skill instead.

### Point 2: rules/capabilities.md

Create in `.claude/rules/` with:
- Mandatory skill invocation table (task domain -> required skill -> anti-pattern)
- Delegation awareness section (so subagents know what's available)
- Post-compaction re-anchoring instruction

Keep project-specific — the skills and anti-patterns differ per project domain.

### Point 3: Orchestrator Step 0

Add to the orchestrator's classify-and-route step:
> Before delegating any task, check the project's Available Extensions table. Route to existing skills before manual execution.

This is a lightweight check — not token-heavy upfront processing.

## SKILL.md Description Format

The default skill description format ("Use when you need to...") relies on passive semantic matching. The imperative format creates stronger behavioral anchors:

```yaml
# Passive (weaker trigger, degrades mid-session):
description: >
  Use when you need to compare flood predictions. Triggers: compare, metrics, benchmark.

# Imperative (stronger trigger, survives attention decay):
description: >
  INVOKE THIS SKILL when comparing predictions across sources.
  Pipeline position: THIRD — runs after inference, before advisory.
  DO NOT compute comparison metrics manually — use this skill's modules.
```

The imperative format works because:
- "INVOKE" is an action directive, not a suggestion
- Pipeline position provides structural context (not just keywords)
- Anti-pattern ("DO NOT") creates a behavioral constraint that persists

## Design Principle

**CAB teaches the pattern; projects fill in the content.**

The Three-Point Reinforcement Pattern is generalizable to any project with skills. But the *specific content* at each point — which skills, what pipeline order, which anti-patterns — is project-domain knowledge. CAB scaffolds the structure and explains why it works. Each project adapts the content to its domain.

## See Also

- [Agent Skills](../components/agent-skills.md) — Skill structure, progressive disclosure, debugging
- [Session Management](session-management.md) — Context health, compaction guidance
- [Orchestration Framework](orchestration-framework.md) — Delegation templates, context engineering
