# Mode: Quick (Template-Driven Fast Scaffold)

> Loaded just-in-time by `scaffold-project` router when `--mode quick`.
> No interactive questionnaire — user already knows what they want.
> Outputs templates inline for user customization.

## When This Mode Fires

- User says "give me a CLAUDE.md template" / "skill template" /
  "agent scaffold"
- User invokes the `quick-scaffold` alias skill
- Iterative scaffolding (creating multiple skills/agents quickly)
- User wants the raw template to customize, not a guided walkthrough

## Procedure

### Step 1: Identify Scope

Ask one short question (or parse from `$ARGUMENTS`):

> "Quick scaffold — what do you need?
> Options: global config, project plugin, skill template, agent template,
> command template, hooks.json, .mcp.json, plugin.json, settings.json,
> CLAUDE.md (project), CLAUDE.md (global), knowledge INDEX."

### Step 2: Output Template

Reference the matching template file from `assets/templates/`:

| Scope request | Template file |
|---|---|
| Global config (full ~/.claude/) | (use `--mode global` instead) |
| Project plugin (full structure) | (use `--mode plugin` instead) |
| Skill template | `assets/templates/skill.md` |
| Agent template | `assets/templates/agent.md` |
| Command template | `assets/templates/command.md` |
| hooks.json | `assets/templates/hooks-json.md` |
| .mcp.json | `assets/templates/mcp-json.md` |
| plugin.json | `assets/templates/plugin-json.md` |
| settings.json | `assets/templates/settings-json.md` |
| CLAUDE.md (project) | `assets/templates/claude-md-project.md` |
| CLAUDE.md (global) | `assets/templates/claude-md-global.md` |
| Knowledge INDEX | `assets/templates/knowledge-index.md` |

Read the appropriate template file and emit its content for the user to
customize (inline or write to a file path they specify).

### Step 3: Customize + Create

User specifies what to fill in for the placeholders (`{{PLACEHOLDER}}`
syntax). Only write files when user explicitly approves the populated
content.

If full-project scaffolding requested via this mode, redirect to
`--mode plugin` or `--mode global` for the proper guided workflow with
git init + validation.

## Quick Trigger Map

| Request phrasing | Action |
|---|---|
| "Scaffold global config" | Suggest `--mode global` (full guided setup) |
| "Scaffold new project" | Suggest `--mode plugin` (full guided setup) |
| "Skill template" / "Create skill scaffold" | Output `assets/templates/skill.md` |
| "Agent template" / "Create agent scaffold" | Output `assets/templates/agent.md` |
| "CLAUDE.md template" | Ask: project or global? Output matching template |
| "Quick plugin.json" | Output `assets/templates/plugin-json.md` |

## Knowledge Anchors

- `knowledge/schemas/global-user-config.md` — global config canonical
- `knowledge/schemas/distributable-plugin.md` — plugin canonical
- `knowledge/overview/executive-summary.md` — high-level architecture context
- `knowledge/components/agent-skills.md` — skill format spec
- `knowledge/components/subagents.md` — agent format spec
- `knowledge/components/custom-commands.md` — command format spec
