# Component Standards

## Agent Frontmatter

- Only use CC-documented fields: `name`, `description`, `tools`, `model`, `effort`, `skills`, `context` (skills only, NOT agents)
- Do NOT use `context:` on agents — it is not a valid CC agent field (LL-15). Use `skills:` for content preloading.
- Do NOT use `disallowedTools:` — not a valid CC field. Use explicit `tools:` allow-list instead.
- Do NOT use `permissionMode:` in plugin agents — this is consumer-controlled.

## Skill Frontmatter

- Descriptions MUST be ≤250 characters. CC truncates beyond this in skill listings.
- All skills MUST have `allowed-tools:` scoped to what the skill actually needs.
- All skills MUST have `effort:` (low | medium | high) to guide CC runtime budget.
- Valid top-level fields: `name`, `description`, `argument-hint`, `allowed-tools`, `effort`, `agent`, `hooks`, `context`, `model`. Do NOT nest these under `metadata:` (LL-16).

## Plugin Architecture

- Distributable components (`agents/`, `skills/`, `commands/`) go at project root, not under `.claude/` (LL-21).
- `.claude/` retains only project config: `settings.json`, `settings.local.json`, `rules/`.
- `plugin.json` lives in `.claude-plugin/` and should NOT have custom component paths.
