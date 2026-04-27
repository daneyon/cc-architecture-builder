# Mode: Plugin (CAB-Compliant Plugin Scaffold)

> Loaded just-in-time by `scaffold-project` router when `--mode plugin`.
> Full plugin structure + git init + optional GitHub remote in one
> automated pass. Use when the user already knows they want a CAB plugin
> (no interactive type discovery needed).

## When This Mode Fires

- User invokes `/cab:init-plugin` (mode shim)
- User says "scaffold a new CAB plugin" / "init plugin" / "start a plugin"
- Default mode (`--mode default`) discovery determines "plugin" is the
  correct project type and switches over

## Procedure

### Step 1: Gather Project Details

Required (from arguments or interactively):

- Project name (kebab-case)
- Brief description / domain purpose
- Author name
- GitHub remote? (yes/no/private/public)

### Step 2: Create Directory Structure

```bash
mkdir -p $1/{.claude-plugin,.claude/{rules,skills},commands,agents,knowledge,hooks,notes,templates}
```

For canonical plugin schema reference: `knowledge/schemas/distributable-plugin.md`.

### Step 3: Generate Core Files from Templates

Source: `skills/scaffold-project/assets/templates/`.

| Target | Template |
|---|---|
| `.claude-plugin/plugin.json` | `plugin-json.md` |
| `.claude-plugin/marketplace.json` | (LL-24 — required for plugin discovery) |
| `CLAUDE.md` | `claude-md-project.md` |
| `.claude/settings.json` | `settings-json.md` |
| `README.md` | (project-specific; user fills) |
| `.gitignore` | (CC security defaults + `notes/` tracking policy per LL-25) |
| `.mcp.json` | `mcp-json.md` (empty scaffold) |
| `hooks/hooks.json` | `hooks-json.md` (with PostToolUse format hook + pre-push state review hook per LL-25) |
| `knowledge/INDEX.md` | `knowledge-index.md` (empty scaffold) |
| `notes/{progress,TODO,lessons-learned}.md` | (tracked seed files per LL-25) |

### Step 4: Initialize Git

```bash
cd $1
git init
git add .
git commit -m "Initial plugin structure via CAB scaffold-project --mode plugin"
```

For git/GitHub setup details: `knowledge/prerequisites/git-foundation.md`.

### Step 5: Optional GitHub Remote

If user opted in:

```bash
gh repo create $1 --private --source=. --push
```

For distribution + marketplace registration: `knowledge/distribution/marketplace.md`.

### Step 6: Validate

Invoke `validate-structure` skill (router-level common post-step) to confirm
CAB-compliance.

## Output Format

```
✓ Created plugin: $1/
  ├── .claude-plugin/plugin.json
  ├── .claude-plugin/marketplace.json
  ├── CLAUDE.md
  ├── .claude/settings.json
  ├── .gitignore
  ├── README.md
  ├── commands/
  ├── agents/
  ├── knowledge/INDEX.md
  ├── hooks/hooks.json
  └── notes/                    (tracked — state SSOT)
      ├── progress.md
      ├── TODO.md
      └── lessons-learned.md

✓ Git initialized
✓ Initial commit: "Initial plugin structure via CAB scaffold-project --mode plugin"
✓ Structure validated: PASS

Next steps:
1. Edit CLAUDE.md with your domain-specific instructions
2. Add knowledge files to knowledge/
3. Create first agent: /cab:add-agent
4. Create first skill: /cab:add-skill
5. Register marketplace + enable globally: see knowledge/distribution/marketplace.md
```

## Knowledge Anchors

- `knowledge/schemas/distributable-plugin.md` — canonical plugin structure
- `knowledge/distribution/marketplace.md` — marketplace registration + plugin enablement
- `knowledge/prerequisites/git-foundation.md` — git setup, GitHub integration patterns
- `knowledge/prerequisites/security-defaults.md` — pre-publication checklist
- `notes/lessons-learned.md` LL-23, LL-24, LL-25 — plugin discovery + marketplace + state-tracking lessons
