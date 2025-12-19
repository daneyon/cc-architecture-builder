---
id: multi-agent-collaboration
title: Multi-Agent Collaboration
category: operational-patterns
tags: [agents, collaboration, orchestration, multi-agent, subagents]
summary: Patterns for coordinating multiple Claude agents working together on complex tasks, including subagent chaining and parallel execution.
depends_on: [subagents, git-worktree]
related: [session-management]
complexity: advanced
last_updated: 2025-12-12
estimated_tokens: 500
revision_note: Content may be expanded in Appendix D (AI Agents Deep Dive).
---

# Multi-Agent Collaboration

## Overview

Complex tasks often benefit from multiple specialized agents working together. Claude Code supports this through subagents (same session) and worktrees (parallel sessions).

## Collaboration Patterns

### Pattern 1: Sequential Subagent Chain

```
Main Agent
    │
    ├──▶ Subagent A (analyze)
    │         │
    │         ▼ results
    │
    ├──▶ Subagent B (implement based on A's analysis)
    │         │
    │         ▼ results
    │
    └──▶ Subagent C (review B's implementation)
              │
              ▼ final results
```

**Use when**: Tasks have clear sequential dependencies.

**Example prompt**:
```
Use the analyzer agent to find issues, then use the implementer 
agent to fix them, then use the reviewer agent to verify.
```

### Pattern 2: Parallel via Worktrees

```
┌─────────────────┐     ┌─────────────────┐
│ Worktree 1      │     │ Worktree 2      │
│ Claude + Agent A│     │ Claude + Agent B│
│                 │     │                 │
│ Security audit  │     │ Performance     │
│                 │     │ analysis        │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
            Merge findings in
            main worktree
```

**Use when**: Tasks can run independently.

### Pattern 3: Main Agent + Specialists

```
┌─────────────────────────────────────────┐
│              Main Agent                  │
│     (orchestrates, synthesizes)          │
└─────────────────┬───────────────────────┘
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
   ┌───────┐  ┌───────┐  ┌───────┐
   │Domain │  │Code   │  │Data   │
   │Expert │  │Review │  │Analyst│
   └───────┘  └───────┘  └───────┘
```

**Use when**: Need diverse expertise on single problem.

## Implementation

### Define Complementary Agents

```yaml
# agents/analyzer.md
---
name: analyzer
description: Analyzes code structure and identifies issues. Use as first step before implementation changes.
tools: Read, Grep, Glob
model: sonnet
---
```

```yaml
# agents/implementer.md
---
name: implementer
description: Implements fixes and improvements based on analysis. Use after analyzer provides findings.
tools: Read, Write, Edit, Bash
model: sonnet
---
```

```yaml
# agents/reviewer.md
---
name: reviewer
description: Reviews implemented changes for correctness and quality. Use as final step before committing.
tools: Read, Grep, Glob, Bash
model: opus
---
```

### Orchestration via Main Agent

In CLAUDE.md or prompts:

```markdown
## Multi-Agent Workflow

For complex changes:
1. First use **analyzer** to identify issues
2. Then use **implementer** to make changes
3. Finally use **reviewer** to verify quality

Each agent has separate context, so explicitly pass relevant 
findings between steps.
```

## Coordination via Git

Git serves as the coordination layer:

| Action | Purpose |
|--------|---------|
| Commits | Checkpoint agent work |
| Branches | Isolate parallel work |
| PRs | Review cross-agent output |
| Merge | Integrate findings |

## Context Handoff

Since subagents have separate context:

```
> Use analyzer to find security issues

[Analyzer runs, produces findings]

> Take the analyzer's findings about SQL injection in user.py 
> and use implementer to fix them

[Explicitly passing context to next agent]
```

## When to Use Each Pattern

| Situation | Pattern |
|-----------|---------|
| Sequential dependent tasks | Subagent chain |
| Independent parallel analysis | Worktree parallel |
| Single problem, multiple perspectives | Main + specialists |
| Long-running + interactive | Worktree for long-running |

## Best Practices

1. **Define clear agent boundaries**: Each agent should have focused expertise
2. **Explicit context passing**: Don't assume agents share context
3. **Use git for coordination**: Commits, branches, PRs as sync points
4. **Start simple**: Single subagent before complex chains
5. **Monitor cost**: Multiple agents = multiple token usage

## Limitations

- Subagents don't share context (must pass explicitly)
- Coordination is manual (no built-in orchestration)
- Complex chains can be token-expensive
- Debugging multi-agent issues is harder

## See Also

- [Subagents](../components/subagents.md) — Single-session agents
- [Git Worktree](git-worktree.md) — Parallel session setup
- Appendix D: AI Agents Deep Dive (planned)
