# Component Standards

## Agent Frontmatter

**Valid CC-documented fields** (per current docs as of 2026-04-22 refresh —
source: https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields):

`name`, `description`, `tools`, `disallowedTools`, `model`, `skills`, `effort`,
`memory`, `background`, `isolation`, `color`, `initialPrompt`, `maxTurns`,
`permissionMode`, `mcpServers`, `hooks`.

Notes per field:

- `context:` — NOT a valid agent field (LL-15). Use `skills:` for content preloading. `context:` is a skill-only field.
- `disallowedTools:` — IS valid (current docs confirm). Applied first, then `tools:` resolves against remaining pool. Tool in both = removed. CAB prefers explicit `tools:` allow-list over denylist where practical (token-efficient + clearer intent).
- `memory:` — scope values `user` / `project` / `local` enable persistent subagent memory. When set, subagent system prompt auto-injects first 200L / 25KB of its `MEMORY.md`; Read/Write/Edit tools auto-enabled. Locations: `~/.claude/agent-memory/<name>/` (user), `.claude/agent-memory/<name>/` (project), `.claude/agent-memory-local/<name>/` (local/gitignored). **Recommended default: `project`** for version-control shareability.
- `permissionMode:`, `hooks:`, `mcpServers:` — valid for user/project agents BUT silently ignored on plugin agents (docs: "plugin subagents do not support the hooks, mcpServers, or permissionMode frontmatter fields"). Do NOT use these in CAB's distributable plugin agents.
- `isolation: worktree` — spawns agent in a temporary git worktree; auto-cleanup if no changes.
- `background: true` — always run this agent as a background task.
- `initialPrompt:` — auto-submitted as first user turn when agent runs as main-session agent via `--agent` or `agent` setting.

## Skill Frontmatter

- Descriptions MUST be ≤250 characters. CC truncates beyond this in skill listings.
- All skills MUST have `allowed-tools:` scoped to what the skill actually needs.
- All skills MUST have `effort:` (low | medium | high) to guide CC runtime budget.
- Valid top-level fields: `name`, `description`, `argument-hint`, `allowed-tools`, `effort`, `agent`, `hooks`, `context`, `model`. Do NOT nest these under `metadata:` (LL-16).

## Plugin Architecture

- Distributable components (`agents/`, `skills/`, `commands/`) go at project root, not under `.claude/` (LL-21).
- `.claude/` retains only project config: `settings.json`, `settings.local.json`, `rules/`.
- `plugin.json` lives in `.claude-plugin/` and should NOT have custom component paths.
