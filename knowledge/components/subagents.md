---
id: subagents
title: Subagents
category: components
tags: [subagents, delegation, context, specialized, agents]
summary: Complete guide to subagents - specialized AI assistants that operate in their own context window for task-specific workflows.
depends_on: [memory-claudemd, agent-skills]
related: [custom-commands, hooks, orchestration-framework, multi-agent-collaboration]
complexity: intermediate
last_updated: 2025-12-23
estimated_tokens: 900
source: https://code.claude.com/docs/en/sub-agents
---

# Subagents

## Overview

Subagents are specialized AI assistants that operate in their **own context window**, preventing pollution of the main conversation. Claude can delegate tasks automatically or users can invoke them explicitly.

**Source**: [Subagents](https://code.claude.com/docs/en/sub-agents)

---

## Key Benefits

| Benefit | Description |
|---------|-------------|
| **Context preservation** | Each subagent has its own context |
| **Specialized expertise** | Fine-tuned instructions for specific domains |
| **Reusability** | Share across projects and teams |
| **Flexible permissions** | Different tool access per subagent |

---

## Subagent Locations

| Type | Location | Scope | Priority |
|------|----------|-------|----------|
| **Project** | `.claude/agents/` | Current project | Highest |
| **User** | `~/.claude/agents/` | All projects | Lower |
| **Plugin** | Bundled with plugins | When installed | Varies |

When names conflict, project-level takes precedence.

---

## File Format

```yaml
---
name: my-agent-name
description: Description of when this subagent should be invoked
tools: Read, Grep, Glob, Bash    # Optional
model: sonnet                     # Optional
permissionMode: default           # Optional
skills: skill1, skill2            # Optional
---

You are a specialized agent focused on [specific purpose].

## Approach
1. [Step 1]
2. [Step 2]

## Constraints
- [Constraint 1]
- [Constraint 2]
```

---

## Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase letters and hyphens |
| `description` | Yes | When to invoke (natural language) |
| `tools` | No | Comma-separated list; inherits all if omitted |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` |
| `permissionMode` | No | `default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore` |
| `skills` | No | Skills to auto-load when agent starts |

---

## Model Selection

| Value | Behavior |
|-------|----------|
| `sonnet` | Use Sonnet model |
| `opus` | Use Opus model |
| `haiku` | Use Haiku model |
| `inherit` | Use same model as main conversation |
| (omitted) | Use configured subagent default |

---

## Managing Subagents

### Using /agents Command (Recommended)

```
/agents
```

Interactive menu to:
- View all available subagents
- Create new subagents (generate with Claude first)
- Edit existing subagents
- Delete subagents
- Manage tool permissions

### CLI-Based Configuration

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer.",
    "prompt": "You are a senior code reviewer...",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

---

## Using Subagents

### Automatic Delegation

Claude proactively delegates based on:
- Task description in request
- `description` field in subagent config
- Current context

**Tip**: Include "use PROACTIVELY" in description for more automatic use.

### Explicit Invocation

```
> Use the code-reviewer subagent to check my changes
> Have the debugger subagent investigate this error
```

---

## Built-in Subagents

### General-Purpose Subagent
- **Model**: Sonnet
- **Tools**: All tools
- **Purpose**: Complex multi-step tasks requiring exploration and action

### Plan Subagent
- **Model**: Sonnet
- **Tools**: Read, Glob, Grep, Bash
- **Purpose**: Research codebase during plan mode

### Explore Subagent
- **Model**: Haiku (fast)
- **Mode**: Read-only
- **Tools**: Glob, Grep, Read, limited Bash
- **Purpose**: Fast codebase searching and analysis

---

## Skills vs Subagents

| Aspect | Skills | Subagents |
|--------|--------|-----------|
| **Invocation** | Model-invoked | Model or user-invoked |
| **Context** | Loads into main context | Separate context window |
| **Purpose** | Procedural knowledge | Specialized assistant |
| **State** | Stateless | Can be resumed |
| **Token Impact** | Adds to main context | Preserves main context |

---

## Example: Code Reviewer

```yaml
---
name: code-reviewer
description: Expert code review specialist. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code clarity and readability
- Proper error handling
- No exposed secrets
- Good test coverage

Provide feedback by priority:
- Critical (must fix)
- Warnings (should fix)
- Suggestions (consider)
```

---

## Resumable Subagents

Subagents can be resumed to continue previous work:

```
> Use the code-analyzer agent to review auth module
[Agent completes, returns agentId: "abc123"]

> Resume agent abc123 and analyze authorization logic
[Agent continues with full previous context]
```

Useful for:
- Long-running research
- Iterative refinement
- Multi-step workflows

---

## Best Practices

| Practice | Description |
|----------|-------------|
| **Generate with Claude first** | Start by having Claude generate, then customize |
| **Design focused agents** | Single, clear responsibility |
| **Write detailed prompts** | Specific instructions, examples, constraints |
| **Limit tool access** | Only necessary tools |
| **Version control** | Check project agents into git |

---

## See Also

- [Agent Skills](agent-skills.md) — Model-invoked capabilities
- [Custom Commands](custom-commands.md) — User-invoked shortcuts
- [Plugins](https://code.claude.com/docs/en/plugins) — Bundle and share agents
- [Orchestration Framework](../operational-patterns/orchestration-framework.md) — Delegation templates, cost model, failure modes
- [Multi-Agent Collaboration](../operational-patterns/multi-agent-collaboration.md) — Coordination patterns
