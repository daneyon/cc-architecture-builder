# Component Standards

> Frontmatter and architecture rules for CC component authoring. The retrieval and invocation mechanics behind these rules — particularly description front-loading, signature parsing, and skill-trigger reliability — are documented in [`knowledge/reference/llm-interaction-patterns.md`](../../knowledge/reference/llm-interaction-patterns.md).

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

**Valid CC-documented fields** (per current docs as of 2026-04-24 refresh —
source: https://code.claude.com/docs/en/skills#frontmatter-reference):

`name`, `description`, `when_to_use`, `argument-hint`, `arguments`,
`disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`,
`effort`, `context`, `agent`, `hooks`, `paths`, `shell`.

All fields are optional per current docs; only `description` is recommended.

Notes per field / CAB-specific conventions:

- Combined `description` + `when_to_use` text is truncated at **1,536 characters** in the skill listing (per current CC docs; raised from prior 250-char cap per LL-16 refresh UXL-040). Front-load the key use case in description since char budget applies to combined text.
- `allowed-tools:` — scope to what the skill actually needs (pre-approves tools while skill is active). Accepts space-separated string or YAML list.
- `effort:` — optional; when set, overrides session level while skill is active. **CAB convention (UXL-039)**: OMIT by default so user's subscription-tier default drives (xhigh for Max on Opus 4.7; high for Pro). Set explicitly ONLY when the skill has a specific reason to floor effort (rare).
- `context: fork` — runs skill in forked subagent context per `agent:` field.
- Do NOT nest these under `metadata:` (LL-16 enforced).

## Plugin Architecture

- Distributable components (`agents/`, `skills/`, `commands/`) go at project root, not under `.claude/` (LL-21).
- `.claude/` retains only project config: `settings.json`, `settings.local.json`, `rules/`.
- `plugin.json` lives in `.claude-plugin/` and should NOT have custom component paths.
