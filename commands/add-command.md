---
description: Add a new custom slash command to the current project
---

# Add Command Command

Create a new custom slash command in the current project.

## Behavior

Use the `creating-components` skill to:

1. **Gather command details**:
   - Command name (what user types after `/`)
   - Description (shown in `/help`)
   - What it should do
   - Arguments it accepts (if any)
   - Tool restrictions (if any)

2. **Create file** (location depends on project type):
   ```
   # Plugin project (has .claude-plugin/plugin.json):
   commands/{{command-name}}.md
   
   # Standalone project:
   .claude/commands/{{command-name}}.md
   ```

3. **Generate command file** with frontmatter and instructions

## Arguments

- `$1` (optional): Command name
- `$ARGUMENTS` (optional): Brief description

## Examples

```
/add-command
→ Interactive command creation

/add-command analyze
→ Creates /analyze command, asks for details

/add-command summarize "Generate executive summary of provided content"
→ Creates with name and description pre-filled
```

## Command Features

Commands can include:

| Feature | Syntax | Example |
|---------|--------|---------|
| All arguments | `$ARGUMENTS` | User's full input |
| Positional args | `$1`, `$2`, etc. | First, second argument |
| File reference | `@path` | Include file content |
| Bash execution | `!command!` | Run shell command |
| Thinking mode | `thinking: extended` | In frontmatter |

## Output

Show:
- Created file path
- Command file preview
- How to use: `/{{command-name}}`
- Will appear in `/help`
