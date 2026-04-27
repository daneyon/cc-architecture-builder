# Mode: Global (`~/.claude/` User Config Setup)

> Loaded just-in-time by `scaffold-project` router when `--mode global`.
> Sets up or updates the global user configuration that applies across
> ALL projects.

## When This Mode Fires

- User invokes `/cab:new-global` (mode shim)
- User says "set up my global Claude config" / "configure ~/.claude"
- New machine setup; first-time CAB user
- User wants to refresh existing global config

## Procedure

### Step 1: Check Existing Configuration

```bash
ls -la ~/.claude/ 2>/dev/null
test -f ~/.claude/CLAUDE.md && echo "EXISTING" || echo "FRESH"
```

Branch:
- If `~/.claude/CLAUDE.md` exists → offer to review/update (preserve user's
  customizations; suggest fields to add)
- If not → create from template (`assets/templates/claude-md-global.md`)

If `--update` arg: open existing for modification.
If `--reset` arg: back up existing → `~/.claude.backup.YYYY-MM-DD/` →
  recreate from scratch.

### Step 2: Gather Preferences (interactive)

For new setups, ask:

- Communication style preferences (terse vs verbose, code-first vs prose-first)
- Default behaviors (commit habits, verification preferences)
- Personal context (role, domain expertise — optional)
- Common tools/workflows used across projects

Inputs feed the CLAUDE.md template population.

### Step 3: Create Structure

```
~/.claude/
├── CLAUDE.md                    # Personal baseline (from template)
├── settings.json                # User-wide settings (model, permissions)
├── settings.local.json          # Personal overrides (gitignored)
├── rules/                       # Personal modular rules
│   └── .gitkeep
├── skills/                      # Personal cross-project skills
│   └── .gitkeep
└── agents/                      # Personal agents
    └── .gitkeep
```

For canonical global schema reference: `knowledge/schemas/global-user-config.md`.

### Step 4: Use Templates

From `skills/scaffold-project/assets/templates/`:

- `claude-md-global.md` → `~/.claude/CLAUDE.md`
- `settings-json.md` → `~/.claude/settings.json` (adapted for user-scope)

For 5-tier memory hierarchy understanding (this is tier 4 — User Memory):
`knowledge/components/memory-claudemd.md`.

## Arguments

- (none): Create or update interactively
- `--update`: Open existing for modification
- `--reset`: Back up + recreate from scratch

## Output

After creation:

- Show created/modified files
- Explain what each file does
- Note that changes apply to **all** projects
- Recommend `cab:check-sync` to verify no plugin↔global shadow conflicts
  exist after install of marketplace plugins

## Knowledge Anchors

- `knowledge/schemas/global-user-config.md` — canonical global schema
- `knowledge/components/memory-claudemd.md` — 5-tier memory hierarchy + how
  global CLAUDE.md fits
- `knowledge/operational-patterns/multi-agent/agent-resolution.md` —
  global vs plugin precedence (LL-27 shadowing context)
- `notes/lessons-learned.md` LL-27 — why global agent files can silently
  shadow plugin agents
