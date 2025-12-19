---
id: subagents
title: Subagents
category: components
tags: [subagents, delegation, separate-context, agents]
summary: Specialized AI assistants operating in separate context windows for task delegation. Can be model-invoked (automatic) or user-invoked (explicit).
depends_on: [memory-claudemd]
related: [agent-skills, custom-commands]
complexity: intermediate
last_updated: 2025-12-12
estimated_tokens: 700
---

# Subagents

## Overview

Subagents are specialized AI assistants that operate in their **own context window**, preventing pollution of the main conversation. Claude can delegate tasks to subagents automatically or users can invoke them explicitly.

## Key Distinction from Skills

| Aspect | Skills | Subagents |
|--------|--------|-----------|
| **Context** | Loads into main context | Separate context window |
| **Invocation** | Model-invoked only | Model or user-invoked |
| **State** | Stateless | Can be resumed via agentId |
| **Token impact** | Adds to main context | Preserves main context |
| **Purpose** | Procedural knowledge | Specialized assistant |

## When to Use Subagents

- **Complex delegated tasks**: Research, analysis, review workflows
- **Context preservation**: Long-running tasks that would pollute main conversation
- **Specialized expertise**: Dedicated personas for specific domains
- **Parallel work**: Multiple agents working on different aspects

## File Structure

**Location**: `agents/` directory (project or personal)

```
agents/
├── code-reviewer.md
├── data-analyst.md
└── domain-expert.md
```

## Agent File Format

```yaml
---
name: agent-name
description: When this agent should be invoked (natural language)
tools: Read, Grep, Glob, Bash    # Optional: comma-separated
model: sonnet                     # Optional: sonnet, opus, haiku, inherit
---

# Agent Name

You are a specialized agent focused on [specific purpose].

## Approach
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Output Format
[Expected structure]
```

## Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase + hyphens) |
| `description` | Yes | When to invoke (Claude uses this for auto-delegation) |
| `tools` | No | Comma-separated tool list; inherits all if omitted |
| `model` | No | Model alias or 'inherit'; defaults to configured subagent model |

## Invocation Patterns

### Automatic Delegation

Claude automatically delegates based on `description` matching task context:

```
User: "Review this code for security issues"
Claude: [Delegates to security-reviewer agent if description matches]
```

### Explicit Invocation

Users can explicitly request an agent:

```
User: "Use the data-analyst agent to examine this dataset"
```

### Resuming Agents

Subagents can be resumed to continue previous work:

```
> Resume agent abc123 and continue the analysis
```

Claude displays agent ID when subagent completes.

## Example: Code Reviewer Agent

```yaml
---
name: code-reviewer
description: Reviews code for quality, security, and best practices. Use proactively after code changes or when user requests code review.
tools: Read, Grep, Glob, Bash
model: sonnet
---

# Code Reviewer

You are a senior code reviewer focused on code quality, security, and maintainability.

## Review Approach

1. **Understand context**: Read relevant files to understand the codebase
2. **Check correctness**: Verify logic, edge cases, error handling
3. **Assess security**: Look for vulnerabilities, injection risks, auth issues
4. **Evaluate style**: Check naming, formatting, documentation
5. **Consider performance**: Identify potential bottlenecks

## Output Format

Provide reviews as:
- **Summary**: Overall assessment (1-2 sentences)
- **Critical Issues**: Must-fix problems
- **Suggestions**: Improvements to consider
- **Positive Notes**: What's done well

## Constraints

- Focus on actionable feedback
- Prioritize security and correctness over style
- Be constructive, not dismissive
```

## Best Practices

1. **Write clear descriptions**: Claude uses this for auto-delegation decisions
2. **Restrict tools appropriately**: Limit to what the agent actually needs
3. **Define clear scope**: Agents should have focused expertise
4. **Use for context-heavy tasks**: Leverage separate context for large analyses
5. **Consider model selection**: Use opus for complex reasoning, haiku for simple tasks

## Performance Considerations

- **Context efficiency**: Agents preserve main context for longer sessions
- **Latency**: Subagents start fresh and may need to gather context
- **Cost**: Separate context means separate token usage

## See Also

- [Agent Skills](agent-skills.md) — Model-invoked capabilities (main context)
- [Custom Commands](custom-commands.md) — User-invoked shortcuts
- [Official Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
