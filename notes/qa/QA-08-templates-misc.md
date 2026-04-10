# QA-08: Templates + Overview + Prerequisites + Distribution -- Delta Report

**Date**: 2026-04-05
**Files checked**: 10 templates + 7 KB files = 17 total
**Official sources fetched**:
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/plugins-reference
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/plugins
- https://code.claude.com/docs/en/plugin-marketplaces

## Summary

17 files checked against 7 official CC documentation pages. **22 discrepancies found** (8 ERROR, 6 MISSING, 5 STALE + 1 confirmed OK, 3 EXTRA).

---

## Template Discrepancies

### ERROR (factually wrong)

| # | Template | Field/Content | Official Reality | Fix |
|---|----------|--------------|-----------------|-----|
| 1 | `plugin/settings.json.template` | `"reasoningEffort": "high"` (commented) with values `low \| medium \| high` | Official settings key is `effortLevel` (not `reasoningEffort`). Values: `"low"`, `"medium"`, `"high"`. Written by `/effort` command. | Rename to `"effortLevel": "high"` |
| 2 | `plugin/settings.json.template` | `"verbose": false` (commented) | No `verbose` key exists in settings.json. No such field in official docs. | Remove this line entirely |
| 3 | `plugin/settings.json.template` | `"theme": "dark"` (commented) with values `dark \| light \| light-daltonized \| dark-daltonized` | `theme` is stored in `~/.claude.json` (global config), NOT in `settings.json`. Adding it to settings.json triggers a schema validation error per official docs. | Remove from settings.json template; optionally note in a comment that theme lives in `~/.claude.json` |
| 4 | `plugin/settings.json.template` | Permission modes comment: `default \| acceptEdits \| bypassPermissions \| plan \| ignore` | Official `defaultMode` values: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. **`ignore` is not valid**. Missing `auto` and `dontAsk`. | Replace with `default \| acceptEdits \| plan \| auto \| dontAsk \| bypassPermissions` |
| 5 | `skill.template/SKILL.md.template` | `# context: inline` (Tier 3 commented field) | `context` only accepts `fork` (run in forked subagent) or should be omitted (default = inline behavior). `inline` is not a documented value. | Change to `# context: fork` with comment `# omit for default inline behavior` |
| 6 | `agent.template/agent.md.template` | `color: "#4A90D9"` (Tier 3 example) | Official `color` field accepts named colors only: `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan`. Hex codes are not documented. | Change to `# color: blue` (or another named color) |
| 7 | `agent.template/agent.md.template` | `permissionMode: default` with values `default \| acceptEdits \| bypassPermissions \| plan \| ignore` | Official `permissionMode` values: `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`. **`ignore` is not valid**. Missing `auto` and `dontAsk`. | Replace with `default \| acceptEdits \| auto \| dontAsk \| bypassPermissions \| plan` |
| 8 | `plugin/settings.json.template` | Header comment: "Full reference: https://code.claude.com/docs/en/settings (60+ fields)" | The official settings page lists approximately 50 keys in `settings.json` plus ~5 keys in `~/.claude.json` global config. "60+ fields" is inflated if counting only settings.json. | Change to "50+ settings" or "see full reference" without a count that may go stale |

### MISSING (should be in template)

| # | Template | Missing Field | Source | Recommended Action |
|---|----------|--------------|--------|-------------------|
| 1 | `plugin/settings.json.template` | `"$schema"` line | Official docs show `"$schema": "https://json.schemastore.org/claude-code-settings.json"` for autocomplete/validation in editors | Add as first line (commented): `// "$schema": "https://json.schemastore.org/claude-code-settings.json"` |
| 2 | `plugin/plugin.json.template` | `channels` field | Official plugins-reference documents `channels` field for message injection (Telegram, Slack, Discord style) | Add commented `"channels"` section in Tier 3 area |
| 3 | `plugin/plugin.json.template` | `bin/` directory mention | Official docs: `bin/` directory at plugin root adds executables to Bash tool's PATH | Add comment noting `bin/` directory pattern |
| 4 | `agent.template/agent.md.template` | `maxTurns` field | Official subagent frontmatter includes `maxTurns` (maximum agentic turns). Template omits it entirely. | Add `# maxTurns: 20` to Tier 2 or Tier 3 section |
| 5 | `skill.template/SKILL.md.template` | `$ARGUMENTS[N]` / `$N` syntax and `${CLAUDE_SKILL_DIR}` | Official docs document indexed argument access (`$ARGUMENTS[0]`, `$0`) and `${CLAUDE_SKILL_DIR}` variable | Add brief comment in template referencing these substitution variables |
| 6 | `plugin/settings.json.template` | `permissions.ask` array | Official docs show three permission arrays: `allow`, `ask`, `deny`. Template only shows `allow` and `deny`. | Add commented `"ask": []` between allow and deny |

### STALE (outdated)

| # | Template | Content | Current Official | Fix |
|---|----------|---------|-----------------|-----|
| 1 | `plugin/settings.json.template` | Hierarchy comment: "Managed > CLI args > Local > Project > User" | Official precedence: Managed > CLI args > **Local > Project > User**. Order is correct but the official docs emphasize Local overrides Project. No error but the comment could be clearer. | Minor: already correct. Optionally add "(Local overrides Project)" for clarity |
| 2 | `skill.template/SKILL.md.template` | `# agent: false` (Tier 3) | Official docs say `agent` field specifies "Which subagent type to use when `context: fork` is set" -- it's a string (agent name), not boolean. | Change to `# agent: Explore` with comment `# subagent type when context: fork` |
| 3 | `agent.template/agent.md.template` | `effort: medium` with comment `low \| medium \| high` | Official docs add `max` as fourth option (Opus 4.6 only): `low \| medium \| high \| max` | Add `max` to the comment: `# low \| medium \| high \| max (Opus 4.6 only)` |
| 4 | `agent.template/agent.md.template` | `memory: project` with comment `user (cross-project) \| project (committed) \| local (gitignored)` | Descriptions are correct but `local` stores at `.claude/agent-memory-local/<name>/` (not `.claude/agent-memory/`). Verify comment accuracy. | Confirm `local` description -- current wording "gitignored" is accurate |
| 5 | `global/settings.local.json.template` | Contains `"Write"` in allow list | `Write` is a valid tool permission, no issue. But template lacks `Grep` and `Glob` which are commonly needed read-only tools. | Add `"Grep"` and `"Glob"` to the allow list for a more practical default |
| 6 | `INDEX.md` | Says "README.md.template" exists in plugin/ | Verified: `templates/plugin/README.md.template` exists. No action needed. | N/A -- confirmed present |

---

## KB File Discrepancies

### ERROR

| # | File | Content | Official Reality | Fix |
|---|------|---------|-----------------|-----|
| 1 | `overview/architecture-philosophy.md` | Skills have "11 frontmatter fields" (line 103) | Official skills docs list **13 frontmatter fields**: name, description, argument-hint, disable-model-invocation, user-invocable, allowed-tools, model, effort, context, agent, hooks, paths, shell | Change to "13 frontmatter fields" |
| 2 | `distribution/marketplace.md` | Lists 8 source types: `github`, `git`, `url`, `npm`, `file`, `directory`, `hostPattern`, `settings` | Official plugin-marketplaces docs list 5 plugin source types: relative path, `github`, `url` (git), `git-subdir`, `npm`. The types `file`, `directory`, `hostPattern`, `settings` are not documented as plugin source types. `hostPattern` and `pathPattern` appear only in `strictKnownMarketplaces` (managed settings restriction patterns). | Rewrite source types section: (1) replace `git` with `url`, (2) add `git-subdir`, (3) remove `file`, `directory`, `hostPattern`, `settings` from plugin source types, (4) optionally note that `hostPattern`/`pathPattern` exist in managed marketplace restrictions |

### MISSING

| # | File | Missing Content | Source | Recommended Action |
|---|------|----------------|--------|-------------------|
| 1 | `distribution/marketplace.md` | `git-subdir` source type | Official docs: sparse clone of subdirectory within git repo. Fields: `url`, `path`, `ref?`, `sha?` | Add `git-subdir` to source types table |
| 2 | `distribution/marketplace.md` | `metadata` marketplace-level field | Official docs: `metadata.description`, `metadata.version`, `metadata.pluginRoot` | Add marketplace metadata fields section |
| 3 | `distribution/marketplace.md` | `strict` field on plugin entries | Official docs: `strict` (boolean, default true) controls whether plugin.json or marketplace entry is authority for component definitions | Add `strict` to optional plugin entry fields |
| 4 | `distribution/marketplace.md` | `category` and `tags` fields | Official docs: marketplace-specific optional fields on plugin entries | Add to optional fields table |
| 5 | `distribution/marketplace.md` | CLI commands for `claude plugin marketplace add/list/remove/update` | Official docs provide full non-interactive CLI subcommands | Add CLI commands section or reference |

### STALE

| # | File | Content | Current Official | Fix |
|---|------|---------|-----------------|-----|
| 1 | `overview/executive-summary.md` | `last_updated: 2025-12-23`, `review_by: 2026-03-23` | Current date is 2026-04-05 -- past review deadline by 13 days | Update `last_updated` and `review_by` after corrections applied |
| 2 | `overview/executive-summary.md` | Memory hierarchy "5 Tiers" with separate "Enterprise Policy" and "Project Rules" tiers | Official docs describe **4 scopes**: Managed, Project, User, Local. "Enterprise Policy" = Managed scope. "Project Rules" is part of Project scope. Splitting into 5 tiers is a CAB-specific interpretation, which is fine but should acknowledge the mapping. | Add a note: "CAB expands CC's 4 official scopes into 5 operational tiers" for transparency |
| 3 | `prerequisites/git-foundation.md` | `last_updated: 2025-12-12`, `review_by: 2026-03-12` | Past review deadline by 24 days | Update timestamps after review |
| 4 | `prerequisites/git-foundation.md` | GitHub MCP command: `claude mcp add --transport http github https://api.github.com/mcp` | This command syntax should be verified against current CC CLI. The `--transport http` flag and URL may have changed. | Verify command against `claude mcp add --help` and update if needed |
| 5 | `prerequisites/security-defaults.md` | `last_updated: 2025-12-12`, `review_by: 2026-03-12` | Past review deadline by 24 days | Update timestamps after review |
| 6 | `distribution/marketplace.md` | `last_updated: 2025-12-12`, `review_by: 2026-03-12` | Past review deadline by 24 days | Update timestamps after review |

### EXTRA (in CAB but not in official -- assess whether to keep)

| # | File | Content | Assessment |
|---|------|---------|------------|
| 1 | `distribution/marketplace.md` | Source types `file`, `directory`, `hostPattern`, `settings` | These are NOT in official plugin-marketplaces docs as plugin source types. `hostPattern` appears only in `strictKnownMarketplaces`. Remove from source types or clearly label as "legacy/unverified". |
| 2 | `overview/executive-summary.md` | `.claude.json` listed at `~/` level in Schema 1 | Technically correct (`~/.claude.json` exists) but this file is not part of the `.claude/` directory structure. It's a separate app config file. Current placement is fine but could confuse users into thinking it's inside `.claude/`. | 
| 3 | `distribution/marketplace.md` | `/plugin test` command mentioned in distribution flow | No `/plugin test` command found in official docs. Official testing approach is `claude --plugin-dir ./path` or `claude plugin validate`. | Replace with official testing commands |

---

## Verified Correct

### Templates
- **hooks.json.template**: Hook event names (PreToolUse, PostToolUse, SessionStart, Stop) all correct. 4 hook types (command, http, prompt, agent) correct. 26 events count correct. Field names (`matcher`, `hooks`, `type`, `command`, `async`, `prompt`, `if`) all valid.
- **plugin/plugin.json.template**: Core fields (`name`, `version`, `description`, `author`, `repository`, `homepage`, `license`, `keywords`) all match official schema. Component paths (`commands`, `agents`, `skills`, `hooks`, `outputStyles`, `mcpServers`, `lspServers`) correct. `userConfig` with `description` and `sensitive` fields correct. `${user_config.KEY}` substitution syntax correct.
- **command.template/command.md.template**: Legacy migration notice is accurate -- skills are preferred, commands still work. Frontmatter fields (`description`, `allowed-tools`) valid.
- **plugin/CLAUDE.md.template**: 200-line discipline guidance, @imports pattern, extension registry entries, notes/ state pattern all align with official best practices.
- **global/CLAUDE.md.template**: Structure and guidance align with official memory hierarchy. `@rules/` reference pattern correct.
- **global/settings.local.json.template**: Valid settings.json structure with `model` and `permissions` fields.

### KB Files
- **overview/architecture-philosophy.md**: 4-scope memory hierarchy (Managed, Project, User, Local) matches official docs. Runtime memory pipeline description (Session Memory, MicroCompact, AutoCompact, Full Compact, Session Reset) is CAB-original operational content -- appropriate. Link-not-duplicate principle correctly applied.
- **overview/design-principles.md**: 9 principles are CAB-original strategic content. Cross-references to official docs via `source:` URLs correctly structured. Layer architecture (Persistent Memory, Extension Registry, Invocation, Execution) is valid CAB interpretation.
- **prerequisites/security-defaults.md**: Private-by-default recommendation, credential handling via environment variables, pre-publication checklist all align with security best practices. No factual errors against official docs.
- **distribution/cowork.md**: Correctly marked as Research Preview with appropriate confidence level. Forward-looking stub approach is appropriate given Cowork's beta status.

### INDEX.md
- Template INDEX accurately catalogs available templates. Placeholder conventions are consistent. Usage mapping to commands is correct. Skill fields count (13) and agent fields count (16) both verified correct.

---

## Priority Fix Order

1. **settings.json.template** -- 3 invalid fields (`reasoningEffort`, `verbose`, `theme`), wrong permission modes, missing `$schema`
2. **marketplace.md** -- Wrong source types list, missing `git-subdir`/`npm`/`metadata`/`strict`/`category`/`tags`
3. **agent.md.template** -- Wrong `color` format, wrong permission mode values, missing `maxTurns`
4. **SKILL.md.template** -- Invalid `context: inline`, wrong `agent: false` type
5. **architecture-philosophy.md** -- Wrong skill field count (11 vs 13)
6. **All stale timestamps** -- 4 files past review_by deadline
