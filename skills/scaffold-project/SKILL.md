---
name: scaffold-project
description: >-
  Create or extend Claude Code project structures. Five modes via --mode flag:
  default (interactive new project), plugin (CAB plugin scaffold + git +
  optional GitHub remote), integrate (overlay CC architecture onto existing
  codebase), global (set up ~/.claude/ user config), quick (template-driven
  fast scaffold, no questionnaire). Triggers: new project, scaffold, init
  plugin, integrate existing, global config, quick template, start project.
argument-hint: "Project name + optional --mode plugin|integrate|global|quick"
allowed-tools: Read, Write, Bash, Glob
---

# Scaffold Project — Multi-Mode Router

## Overview

This skill is the unified entry point for all CAB scaffolding workflows.
The `--mode` flag dispatches to mode-specific procedures defined in
`assets/mode-*.md` files (progressive disclosure — load mode body just in
time when invoked).

## Mode Comparison

| Mode | Use case | Procedure file | KB references |
|---|---|---|---|
| (default) | Interactive discovery for any new project type | `assets/mode-default.md` | `knowledge/schemas/`, `knowledge/implementation/workflow.md` |
| `--mode plugin` | New CAB-compliant plugin: full structure + git init + optional GitHub | `assets/mode-plugin.md` | `knowledge/schemas/distributable-plugin.md`, `knowledge/distribution/marketplace.md`, `knowledge/prerequisites/git-foundation.md` |
| `--mode integrate` | Overlay CC architecture onto existing project (preserves existing code) | `assets/mode-integrate.md` | `knowledge/components/`, `knowledge/operational-patterns/`, `knowledge/reference/` (a-team-database) |
| `--mode global` | Set up `~/.claude/` user config | `assets/mode-global.md` | `knowledge/schemas/global-user-config.md`, `knowledge/components/memory-claudemd.md` |
| `--mode quick` | Template-only fast scaffold; user already knows what they want | `assets/mode-quick.md` + `assets/templates/` | `knowledge/schemas/*` (templates align with schemas) |

## Dispatch Protocol

### Step 0: DP8 Pre-Flight Check (MANDATORY before any new component scaffolding)

**Before** any mode dispatches that creates a new skill / agent / command /
hook / MCP server, **explicitly verify** no existing CC capability already
covers the domain. This is the operational embodiment of LL-30 — passive
documentation of DP8 (Wrap & Extend) is insufficient; the gate must fire
before scaffolding work begins.

**Pre-flight checklist** (answer ALL before proceeding):

1. **Installed plugins**: list enabled plugins via `cat ~/.claude/settings.json | jq '.enabledPlugins | to_entries | map(select(.value == true)) | .[].key'` (or equivalent). For each enabled plugin, scan its `skills/`, `agents/`, `commands/` for domain overlap with the proposed work.
2. **Anthropic official plugins** specifically: `~/.claude/plugins/cache/claude-plugins-official/plugins/` — even if not currently enabled, check for prior art before building. `plugin-dev` is the canonical reference for plugin authoring (agent-development, command-development, hook-development, mcp-integration, plugin-settings, plugin-structure, skill-development skills + agent-creator, plugin-validator, skill-reviewer agents + create-plugin command).
3. **Native CC capabilities**: cross-check against `https://code.claude.com/docs/en/` — does CC native already do this via built-in tool / setting / hook event?
4. **MCP servers**: would wrapping an external service via MCP be more appropriate than building from scratch?

**Decision gate**:

- **Overlap found + wrappable** → STOP scaffolding new component. Either invoke the existing plugin/capability OR write a thin wrapper skill that delegates. Document the wrap in skill body.
- **Overlap found + not wrappable** (rare) → document why wrap is infeasible BEFORE proceeding. Update LL-30 with the new insight.
- **No overlap found** → proceed with scaffolding. Add a "DP8 Check Passed" note to the new skill body documenting what was checked.

**Why this gate exists**: see `notes/lessons-learned.md` LL-30 — Sessions 36-37 built 3 CAB components (`create-components`, `validate-structure`, `scaffold-project --mode plugin`) duplicating `plugin-dev`'s offering because the DP8 principle was documented but not enforced at the scaffolding entry point. UXL-041 tracks refactor candidates; this gate prevents future recurrence.

### Step 1: Common Pre-Steps (all modes)

1. Parse `$ARGUMENTS` for `--mode <name>` (default if absent).
2. Validate target path: confirm parent directory exists; confirm no
   collision with existing project (unless `--mode integrate`).
3. Confirm intent with user if mode is destructive (e.g., `--mode global`
   with existing `~/.claude/CLAUDE.md`).

### Step 2: Mode Dispatch

Read the mode-specific procedure file just-in-time:

```
Read("skills/scaffold-project/assets/mode-<mode>.md")
```

Follow the steps in that file. Each mode asset is self-contained for its
domain — common steps are router-owned (above + below), mode-specific
steps live in the asset.

### Step 3: Common Post-Steps (all modes)

1. Run structural validation: invoke `validate-structure` skill on the
   created project.
2. Report directory tree + next-step guidance to the user.
3. If git was initialized in-mode, confirm initial commit succeeded.

## Knowledge Integration

This skill is **procedural** — it executes the scaffolding. The
**conceptual depth** for each mode lives in the linked KB cards (see Mode
Comparison table). Mode assets reference KB cards rather than duplicate
their content (per CAB wrapper philosophy + LL-11):

- **What schemas look like** → `knowledge/schemas/*` (canonical specs)
- **Why each component exists** → `knowledge/components/*` (per-component deep dives)
- **How distribution works** → `knowledge/distribution/marketplace.md`
- **Git/security prerequisites** → `knowledge/prerequisites/*`

When a mode asset says "follow the plugin schema," it points at the KB
card; the mode asset itself stays procedural and short.

## Templates

Templates for `--mode quick` and shared template needs live in
`assets/templates/`:

- `claude-md-global.md`, `claude-md-project.md`
- `plugin-json.md`, `settings-json.md`
- `skill.md`, `agent.md`, `command.md`
- `hooks-json.md`, `mcp-json.md`
- `knowledge-index.md`

Templates are reusable across modes — `--mode plugin` and `--mode quick`
both reference the same `claude-md-project.md` template, eliminating
duplication.

## Verification

This skill is working correctly when:

- The `--mode` arg correctly dispatches to the matching asset file (no
  silent fallthrough to default)
- Created project structure passes `validate-structure` skill on first run
- No content from KB cards is duplicated inside mode assets — assets
  reference KB by path
- Templates are referenced (not inlined) when used by multiple modes

## Integration Points

- `commands/new-project.md` → shim invoking default mode
- `commands/init-plugin.md` → shim invoking `--mode plugin`
- `commands/integrate-existing.md` → shim invoking `--mode integrate`
- `commands/new-global.md` → shim invoking `--mode global`
- `skills/quick-scaffold/SKILL.md` → 1-line alias preserving "quick-scaffold"
  skill-name trigger; delegates to `--mode quick`
- `validate-structure` skill — invoked at common post-step; verifies
  scaffolded structure

## See Also

- `assets/mode-*.md` — per-mode procedural detail
- `assets/templates/` — reusable templates
- `knowledge/schemas/distributable-plugin.md` — canonical plugin structure
- `knowledge/schemas/global-user-config.md` — canonical global structure
- `.claude/rules/component-standards.md` — component frontmatter rules
