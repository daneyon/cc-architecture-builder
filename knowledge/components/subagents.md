---
id: subagents
title: Subagents
category: components
tags: [subagents, delegation, context, specialized, agents, orchestration]
summary: Complete guide to subagents - specialized AI assistants operating in isolated context windows, with full frontmatter reference and CAB-specific patterns.
depends_on: [memory-claudemd, agent-skills]
related: [custom-commands, hooks, orchestration-framework, collaboration-patterns]
complexity: intermediate
last_updated: 2026-04-05
estimated_tokens: 1800
confidence: A
review_by: 2026-07-05
source: https://code.claude.com/docs/en/sub-agents
---

# Subagents

## Overview

Subagents are specialized AI assistants that operate in their **own context window**, preventing pollution of the main conversation. Claude delegates tasks automatically based on the agent's `description` field, or users invoke them explicitly.

**Source**: [Create custom subagents — Official Docs](https://code.claude.com/docs/en/sub-agents) -- authoritative reference for native behavior. This file documents CAB-specific extensions and provides a consolidated field reference.

---

## Key Constraint

Subagents **cannot spawn other subagents** (nesting depth = 1). Design delegation hierarchies accordingly -- the parent session is the only orchestration point.

---

## Subagent Locations & Precedence

Agents can be defined at 5 levels. When names conflict, the highest-priority source wins.

| Priority     | Source       | Location                              | Scope                      |
|--------------|--------------|---------------------------------------|----------------------------|
| 1 (highest)  | **Managed**  | Enterprise managed settings           | Organization-wide policy   |
| 2            | **CLI flag** | `--agents` flag (JSON)                | Session-level override     |
| 3            | **Project**  | `.claude/agents/` (standalone)        | Current project            |
| 4            | **User**     | `~/.claude/agents/`                   | All projects for this user |
| 5 (lowest)   | **Plugin**   | `agents/` at plugin root (bundled)    | When plugin is installed   |

---

## Frontmatter Field Reference (16 Fields)

Every `.md` agent file begins with a YAML frontmatter block (`---` delimiters). Below is the complete field set. The markdown body after the closing `---` serves as the agent's system prompt (instructions, constraints, verification criteria).

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Lowercase letters and hyphens. Used for invocation. |
| `description` | Yes | string | Natural-language description of when to invoke. Include "Use PROACTIVELY" for auto-delegation. |
| `tools` | No | comma-sep | Tool allowlist. Omit to inherit all parent tools. |
| `disallowedTools` | No | comma-sep | Tool denylist. Excluded even if `tools` would allow them. |
| `model` | No | enum | `sonnet`, `opus`, `haiku`, a full model ID (e.g., `claude-opus-4-6`, `claude-sonnet-4-6`), or `inherit`. Defaults to `inherit`. |
| `permissionMode` | No | enum | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`. |
| `maxTurns` | No | integer | Maximum number of agentic turns before the subagent stops. |
| `skills` | No | list | Skills to preload. **Full content** is injected at start; subagents do NOT inherit parent skills. |
| `mcpServers` | No | object | Inline MCP server definitions. Connected at agent start, disconnected at finish. Scoped to that agent. Also supports string references to existing servers. |
| `hooks` | No | object | Event-driven automation hooks for this agent's lifecycle. |
| `memory` | No | path | Persistent memory directory. Supports 3 scopes (see Memory section). |
| `background` | No | boolean | `true` to run agent in background. See Background Execution. |
| `effort` | No | enum | Reasoning effort level: `low`, `medium`, `high`, `max`. |
| `isolation` | No | enum | `worktree` for git-worktree isolation with auto-cleanup on finish. |
| `color` | No | string | Statusline color: `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan`. |
| `initialPrompt` | No | string | Prompt injected before user's first message to the agent. |

### Plugin Restrictions

Plugins that bundle agents **cannot** use these fields: `hooks`, `mcpServers`, `permissionMode`. These are reserved for user/project-level agents for security reasons.

---

## Default Subagent Setting

Configure the default subagent model/behavior globally in `settings.json`:

```json
{
  "agent": "sonnet"
}
```

The setting key is `agent` (not `defaultSubagent`).

---

## Agent Auto Memory (3 Scopes)

When the `memory:` frontmatter field is set, the subagent gets dedicated persistent memory separate from the main session's auto memory:

| `memory:` value | Storage Location | Shared | Git-tracked |
|-----------------|-----------------|--------|-------------|
| `user` | `~/.claude/agent-memory/<agent>/MEMORY.md` | Cross-project, personal | No (local) |
| `project` | `.claude/agent-memory/<agent>/MEMORY.md` | This project, team | Yes (committed) |
| `local` | `.claude/agent-memory-local/<agent>/MEMORY.md` | This machine only | No (gitignored) |

- First 200 lines (≤25KB) of each agent's `MEMORY.md` are loaded into the subagent system prompt at start
- Only created for subagents that set the `memory:` field — directories are auto-generated on first write
- Distinct from main session auto memory at `~/.claude/projects/<path>/memory/`

---

## Background Execution

```yaml
background: true
```

- Agent runs asynchronously; parent session continues working
- Grant permissions upfront since the agent runs without interactive approval
- Users can press **Ctrl+B** to background a running agent mid-execution
- Background agents report results when finished; parent is notified

---

## Worktree Isolation

```yaml
isolation: worktree
```

- Agent operates in a dedicated git worktree (separate working directory)
- Auto-cleanup: worktree is removed when the agent finishes
- Prevents file conflicts when multiple agents modify the same codebase
- See [Worktree Workflows](../operational-patterns/multi-agent/worktree-workflows.md) for setup details

---

## Auto-Compaction

Subagents auto-compact at ~95% context usage. Override with:

```bash
CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=80  # compact earlier
```

---

## Skills Preloading

```yaml
skills:
  - execute-task
  - validate-structure
```

- Listed skills have their **full content** injected into the agent's context at start
- Subagents do **not** inherit the parent session's skills -- only explicitly listed ones
- This is the primary mechanism for giving agents domain knowledge without bloating the parent context

---

## MCP Server Scoping

```yaml
mcpServers:
  my-server:
    command: npx
    args: ["-y", "my-mcp-server"]
```

- Inline MCP definitions are **connected** when the agent starts and **disconnected** when it finishes
- Scoped entirely to that agent -- no leakage to the parent session or other agents
- Use for agents that need specialized tool access (databases, APIs, etc.)

---

## Built-in Subagents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| **Explore** | Haiku | Glob, Grep, Read, limited Bash | Fast read-only codebase search and analysis |
| **Plan** | inherit | Read-only tools (Write and Edit denied) | Research codebase during plan mode |
| **General-purpose** | inherit | All tools | Complex multi-step tasks requiring exploration and action |
| **statusline-setup** | -- | -- | Configures terminal status line display |
| **Claude Code Guide** | -- | -- | Interactive onboarding and help |

---

## Managing Subagents

### /agents Command

```text
/agents
```

Interactive management: view, create, edit, delete agents and manage tool permissions.

### CLI Configuration

```bash
claude --agents '{ "code-reviewer": { "description": "...", "prompt": "...", "tools": ["Read","Grep"], "model": "sonnet" } }'
```

---

## CAB-Specific Patterns

CAB extends the native subagent model with three architectural patterns. Agent templates are in `templates/agent.template/`.

### Orchestrator Pattern

The `orchestrator` agent acts as a central router: receives tasks, classifies them, delegates to specialist agents, and synthesizes results. Set as the default agent for fully autonomous plugin operation.

```yaml
name: orchestrator
model: opus
skills: execute-task, validate-structure
```

See `agents/orchestrator.md` for the full definition.

### Verifier Pattern

The `verifier` agent provides independent validation. It runs after implementation agents complete, confirming correctness before commit. Inspired by Boris Cherny's `verify-app` pattern.

```yaml
name: verifier
description: >
  ... Use PROACTIVELY after any implementation agent finishes its work.
model: inherit
```

See `agents/verifier.md` for the full definition.

### CAB Agent Template Requirements

Every CAB agent file **must** include a `## Verification (REQUIRED)` section with concrete, runnable checks. This is enforced by the agent template (`templates/agent.template/agent.md.template`) and aligns with Tenet 2 of the orchestration framework: verification is an architectural requirement, not optional.

---

## Skills vs Subagents

| Aspect | Skills | Subagents |
|--------|--------|-----------|
| **Invocation** | Model-invoked (automatic) | Model or user-invoked |
| **Context** | Loads into main context | Separate context window |
| **Purpose** | Procedural knowledge | Specialized assistant |
| **State** | Stateless | Resumable, memory-capable |
| **Token impact** | Adds to main context | Preserves main context |
| **Nesting** | N/A | Cannot nest (depth = 1) |

## See Also

- [Agent Skills](agent-skills.md) -- Model-invoked capabilities
- [Custom Commands](custom-commands.md) -- User-invoked shortcuts
- [Hooks](hooks.md) -- Event-driven automation
- [Orchestration Framework](../operational-patterns/orchestration/framework.md) -- Delegation patterns, cost model, failure modes
- [Collaboration Patterns](../operational-patterns/multi-agent/collaboration-patterns.md) -- Multi-agent coordination
- [Worktree Workflows](../operational-patterns/multi-agent/worktree-workflows.md) -- Parallel execution with isolation
