---
description: Add a new subagent to the current project
---

# Add Agent Command

Create a new subagent in the current project.

## Behavior

Use the `creating-components` skill to:

1. **Gather agent details**:
   - Agent name (lowercase-hyphens)
   - Specialization/expertise
   - When to delegate to this agent
   - Tools needed (or inherit all)
   - Model preference (optional)

2. **Create file** (location depends on project type):
   ```
   # Plugin project (has .claude-plugin/plugin.json):
   agents/{{agent-name}}.md
   
   # Standalone project:
   .claude/agents/{{agent-name}}.md
   ```

3. **Generate agent definition** with frontmatter and body

## Arguments

- `$1` (optional): Agent name
- `$ARGUMENTS` (optional): Brief specialization

## Examples

```
/add-agent
→ Interactive agent creation

/add-agent code-reviewer
→ Creates agent with name, asks for details

/add-agent data-analyst "Specialized in statistical analysis and visualization"
→ Creates with name and description pre-filled
```

## Configuration Options

| Option | Values | Default |
|--------|--------|---------|
| tools | Comma-separated list | Inherit all |
| model | sonnet, opus, haiku, inherit | inherit |

## Output

Show:
- Created file path
- Agent definition preview
- How to invoke (automatic delegation or explicit)
- When to use agents vs skills
