---
description: Initialize a new CAB plugin project with full structure, git setup, and optional GitHub remote
allowed-tools: Read, Write, Bash
---

# Init Plugin Command

Create a new CAB-compliant plugin project with the complete base architecture, initialized git repository, and optional GitHub remote.

## Behavior

1. **Gather project details** (from arguments or interactively):
   - Project name (kebab-case)
   - Brief description / domain purpose
   - Author name
   - GitHub remote? (yes/no)

2. **Create directory structure**:
   ```bash
   mkdir -p $1/{.claude-plugin,.claude/{rules,skills},commands,agents,knowledge,hooks,notes,templates}
   ```

3. **Generate core files from templates**:
   - `.claude-plugin/plugin.json` from `templates/plugin/plugin.json.template`
   - `.claude-plugin/marketplace.json` from `templates/plugin/marketplace.json.template` (LL-24)
   - `CLAUDE.md` from `templates/plugin/CLAUDE.md.template`
   - `.claude/settings.json` from `templates/plugin/settings.json.template`
   - `README.md` from `templates/plugin/README.md.template`
   - `.gitignore` (CC security defaults + `notes/` tracking policy — see LL-25)
   - `.mcp.json` (empty scaffold)
   - `hooks/hooks.json` (with PostToolUse format hook + pre-push state review hook — LL-25)
   - `knowledge/INDEX.md` (empty scaffold)
   - `notes/progress.md`, `notes/TODO.md`, `notes/lessons-learned.md` (tracked seed files, LL-25)

4. **Initialize git** (private by default):
   ```bash
   cd $1
   git init
   git add .
   git commit -m "Initial plugin structure via CAB /init-plugin"
   ```

5. **Optional GitHub remote**:
   ```bash
   gh repo create $1 --private --source=. --push
   ```

6. **Run `/validate`** to confirm structure is compliant.

## Arguments

- `$1` (required): Project name (kebab-case)
- `$2` (optional): Brief description
- `--github` or `--no-github`: Whether to create GitHub remote (default: ask)

## Examples

```
/init-plugin my-assistant
→ Interactive: asks for description, author, GitHub preference

/init-plugin flood-analyzer "Water resources flood analysis assistant"
→ Creates with name and description, asks remaining questions

/init-plugin my-tool "Dev tooling" --github
→ Full automated setup including GitHub remote
```

## Post-Creation Output

```
✓ Created project: my-assistant/
  ├── .claude-plugin/plugin.json
  ├── CLAUDE.md
  ├── .claude/settings.json
  ├── .gitignore
  ├── README.md
  ├── commands/
  ├── agents/
  ├── knowledge/INDEX.md
  ├── hooks/hooks.json
  └── notes/                        (tracked — state management SSOT)
      ├── progress.md
      ├── TODO.md
      └── lessons-learned.md

✓ Git initialized (private)
✓ Initial commit: "Initial plugin structure via CAB /init-plugin"
✓ Structure validated: PASS

Next steps:
1. Edit CLAUDE.md with your domain-specific instructions
2. Add knowledge files to knowledge/
3. Create your first agent: /add-agent
4. Create your first skill: /add-skill
```

## See Also

- `/new-project` — Guided interactive project creation (more discovery questions)
- `/validate` — Verify project structure compliance
- `/init-worktree` — Set up parallel execution worktrees
