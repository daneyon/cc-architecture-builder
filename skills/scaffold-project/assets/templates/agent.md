# Agent Template (agents/{{agent-name}}.md)

```yaml
---
name: {{agent-name}}
description: {{When to invoke this agent}}
tools: Read, Grep, Glob
model: sonnet
---

# {{Agent Name}}

You are a specialized agent focused on {{purpose}}.

## Approach
1. {{Step 1}}
2. {{Step 2}}

## Constraints
- {{Constraint 1}}
- {{Constraint 2}}

## Output Format
{{Expected output structure}}

## Verification
This agent's quality is confirmed by:
- {{Quality criterion 1}}
- {{Quality criterion 2}}
```

For valid agent frontmatter fields (do NOT use `context:` on agents per LL-15;
plugin agents do not support `permissionMode`/`hooks`/`mcpServers`):
`.claude/rules/component-standards.md` + `knowledge/components/subagents.md`.
