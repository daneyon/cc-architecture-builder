---
description: Create a new Claude Code plugin project with full structure
---

# New Project Command

Create a new Claude Code plugin project following the standardized architecture.

## Behavior

When invoked, initiate the project scaffolding workflow:

1. **Ask the user**:
   - Project name (will be directory name, use kebab-case)
   - Domain/purpose (what this project is for)
   - Expected knowledge base size (small/medium/large)
   - Distribution intent (personal/team/public)

2. **Based on responses, use the `scaffolding-projects` skill** to:
   - Create directory structure appropriate to complexity
   - Generate core files from templates
   - Initialize git repository
   - Provide next steps

## Arguments

- `$1` (optional): Project name
- `$2` (optional): Domain description

If arguments provided, use them. Otherwise, prompt interactively.

## Examples

```
/new-project
→ Starts interactive questionnaire

/new-project my-assistant
→ Creates "my-assistant" project, asks remaining questions

/new-project flood-analyzer "Water resources flood analysis"
→ Creates "flood-analyzer" with domain pre-filled
```

## Output

After creation, show:
- Directory tree created
- List of files with purposes
- Next steps for customization
- How to validate (`/validate`)
