---
description: Set up global user configuration in ~/.claude/
---

# New Global Configuration Command

Set up or update the global user configuration at `~/.claude/`.

## Behavior

1. **Check existing configuration**:
   - If `~/.claude/CLAUDE.md` exists, offer to review/update
   - If not, create from template

2. **Gather preferences**:
   - Communication style preferences
   - Default behaviors
   - Personal context (optional)
   - Common tools/workflows

3. **Create structure**:
   ```
   ~/.claude/
   ├── CLAUDE.md
   ├── settings.local.json (if needed)
   ├── skills/ (if personal skills desired)
   └── agents/ (if personal agents desired)
   ```

4. **Use templates** from `templates/global/`:
   - `CLAUDE.md.template`
   - `settings.local.json.template`

## Arguments

- `$1` (optional): `--update` to modify existing, `--reset` to start fresh

## Examples

```
/new-global
→ Creates or updates global config interactively

/new-global --update
→ Opens existing config for modification

/new-global --reset
→ Backs up and recreates from scratch
```

## Output

After creation:
- Show created/modified files
- Explain what each file does
- Note that changes apply to all projects
