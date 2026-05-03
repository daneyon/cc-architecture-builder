---
description: Add a new skill to the current project
---

# Add Skill Command

Create a new agent skill in the current project.

## Behavior

Use the `create-components` skill to:

1. **Gather skill details**:
   - Skill name (verb+object recommended: `analyze-data`)
   - What it does
   - When Claude should trigger it
   - Key instructions/steps

2. **Validate name**:
   - Max 64 characters
   - Lowercase letters, numbers, hyphens only
   - No reserved words

3. **Create structure** (location depends on project type):
   ```
   # Plugin project (has .claude-plugin/plugin.json):
   skills/{{skill-name}}/
   └── SKILL.md
   
   # Standalone project:
   .claude/skills/{{skill-name}}/
   └── SKILL.md
   ```

4. **Generate SKILL.md** with proper frontmatter

## Arguments

- `$1` (optional): Skill name
- `$ARGUMENTS` (optional): Brief description

## Examples

```
/add-skill
→ Interactive skill creation

/add-skill process-pdfs
→ Creates skill with name, asks for details

/add-skill analyze-data "Statistical analysis on datasets"
→ Creates with name and description pre-filled
```

## Validation

After creation, verify:
- [ ] Name meets requirements
- [ ] Description is clear and specific
- [ ] Trigger conditions defined
- [ ] Instructions are actionable

## Output

Show:
- Created file path
- SKILL.md content preview
- How to test the skill
- Reminder about progressive disclosure for large skills
