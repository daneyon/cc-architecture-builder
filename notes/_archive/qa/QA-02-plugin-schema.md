# QA-02: Distributable Plugin Schema -- Delta Report

**Date**: 2026-04-05
**CAB file**: `knowledge/schemas/distributable-plugin.md`
**Official sources**:
- https://code.claude.com/docs/en/plugins (Create plugins guide)
- https://code.claude.com/docs/en/plugins-reference (Complete technical reference)
- https://code.claude.com/docs/en/skills (Skills documentation)
- https://code.claude.com/docs/en/hooks (Hooks documentation)
- https://code.claude.com/docs/en/settings (Settings reference)
- https://code.claude.com/docs/en/plugin-marketplaces (Marketplace guide)
- https://code.claude.com/docs/en/discover-plugins (Plugin discovery)
- https://code.claude.com/docs/en/sub-agents (Subagents reference)
- https://code.claude.com/docs/en/output-styles (Output styles reference)
- https://code.claude.com/docs/en/common-workflows (Worktree/.worktreeinclude)

## Summary

**70+ items checked, 8 discrepancies found** (2 ERRORs, 4 MISSING, 1 STALE, 1 EXTRA flagged for review)

---

## Discrepancies

### ERROR (factually wrong in CAB)

| # | CAB Claim | Official Reality | Location in CAB | Fix |
|---|-----------|-----------------|-----------------|-----|
| E1 | Plugin directory tree shows `CLAUDE.md` at plugin root as "Project system instructions" | Official plugin structure docs (plugins-reference "Standard plugin layout") do NOT list `CLAUDE.md` as part of a plugin directory. The standard plugin layout shows: `.claude-plugin/`, `commands/`, `agents/`, `skills/`, `output-styles/`, `hooks/`, `bin/`, `settings.json`, `.mcp.json`, `.lsp.json`, `scripts/`, `LICENSE`, `CHANGELOG.md`. `CLAUDE.md` is for project-level instructions, not for distributed plugins. A plugin is consumed as a distributable package; `CLAUDE.md` is not copied to the consumer. | Lines 25 (directory tree) and 223-234 (CAB-specific structure) | Remove `CLAUDE.md` from the generic plugin directory tree. It may appear in CAB's own structure as a project file, but should not be presented as a standard plugin component. Add a note that `CLAUDE.md` is project-level, not plugin-level. |
| E2 | `claude plugin validate .` listed as a Distribution Checklist item (line 247) | The official CLI reference does NOT list `claude plugin validate` as a standalone CLI subcommand. The validation command exists as `/plugin validate .` (interactive) or is mentioned as `claude plugin validate` in marketplace troubleshooting, but it is NOT listed in the CLI commands reference section (only `install`, `uninstall`, `enable`, `disable`, `update` are listed). The docs mention validation via `/plugin validate` and `claude plugin validate` in marketplace troubleshooting context, so it likely exists but is not a documented plugin subcommand in the CLI reference. | Line 247 | Change to `/plugin validate .` as the primary form. Add note that `claude plugin validate .` may also work from CLI but is not formally in the CLI subcommands reference. |

### MISSING (in official docs, absent from CAB)

| # | Official Feature/Field | Source URL | Recommended Action |
|---|----------------------|------------|-------------------|
| M1 | **`lspServers` component path field** in plugin.json schema -- CAB lists it in the Component Paths table but does NOT include `.lsp.json` default location context. The official docs show extensive LSP server documentation including required fields (`command`, `extensionToLanguage`), optional fields (`args`, `transport`, `env`, `initializationOptions`, `settings`, `workspaceFolder`, `startupTimeout`, `shutdownTimeout`, `restartOnCrash`, `maxRestarts`), inline plugin.json declaration, and available LSP plugins. | https://code.claude.com/docs/en/plugins-reference#lsp-servers | Add a brief note or cross-reference to LSP server configuration in the Component Paths section. Consider adding minimal LSP coverage or a "See Also" link. |
| M2 | **Hook types** -- CAB only mentions `command` type hooks. Official docs list four hook types: `command`, `http`, `prompt`, and `agent`. Each has different configuration fields and behavior. | https://code.claude.com/docs/en/hooks | Add the four hook types to the hooks section or reference the hooks docs. |
| M3 | **Complete hook event list** -- Official docs list 26 hook events (SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PermissionDenied, PostToolUse, PostToolUseFailure, Notification, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, TeammateIdle, InstructionsLoaded, ConfigChange, CwdChanged, FileChanged, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact, Elicitation, ElicitationResult, SessionEnd). CAB does not cover hooks in depth (by design -- wrapper philosophy), but a brief mention or cross-reference would be valuable. | https://code.claude.com/docs/en/plugins-reference#hooks | Out of scope for this file (wrapper philosophy). The "See Also" section already links to official docs. No action required unless hook coverage is desired. |
| M4 | **`--plugin-dir` CLI flag** for local development testing. Official docs emphasize this as the primary development workflow. CAB mentions it at line 246 (`claude --plugin-dir ./my-plugin`) but uses a different syntax form in the Distribution Checklist. | https://code.claude.com/docs/en/plugins | Minor. CAB already includes this. Verify the checklist item at line 246 matches official syntax exactly: `claude --plugin-dir ./my-plugin`. Currently correct. |

### STALE (outdated in CAB)

| # | CAB Content | Current Official | Fix |
|---|------------|-----------------|-----|
| S1 | `commands/` directory described simply as "Slash commands (markdown files)" (line 33). | Official docs clarify that `commands/` is **legacy**: "Commands: Skill Markdown files (legacy; use `skills/` for new skills)". The file locations reference table in plugins-reference explicitly states commands/ is the legacy location. Skills (`skills/`) with `name/SKILL.md` structure is the current recommended approach. | Update the directory tree comment from "Slash commands (markdown files)" to "Slash commands (markdown files; legacy -- prefer `skills/` for new skills)" to match the official deprecation signal. |

### EXTRA (in CAB only -- may be valid CAB extension)

| # | CAB Content | Assessment |
|---|------------|------------|
| X1 | CAB directory tree includes `knowledge/` with `INDEX.md`, `docs/`, `README.md`, `CHANGELOG.md`, `LICENSE`, and `scripts/` as standard plugin directories (lines 42-47). | **Partially valid CAB extension.** `LICENSE` and `CHANGELOG.md` appear in the official standard plugin layout. `scripts/` also appears officially. `README.md` does not appear in the official standard layout but is mentioned as a best practice for sharing ("Add documentation: Include a README.md"). `knowledge/` and `docs/` are CAB-specific additions. These are reasonable CAB patterns but should be clearly marked as CAB extensions vs. CC native directories. Currently the tree mixes native CC directories with CAB-specific additions without differentiation. Consider adding a comment like `# CAB extension` next to `knowledge/`, `docs/`, and `README.md`. |

---

## Verified Correct

The following items were checked against official documentation and confirmed accurate:

### Directory Structure
- `.claude-plugin/plugin.json` is the manifest location (confirmed)
- `plugin.json` is the ONLY file inside `.claude-plugin/` (confirmed -- official docs warn against putting other dirs inside)
- `settings.json` at plugin root for default settings (confirmed)
- `.mcp.json` at plugin root for MCP servers (confirmed)
- `.lsp.json` at plugin root for LSP servers (confirmed)
- `commands/` at plugin root (confirmed)
- `skills/` at plugin root with `name/SKILL.md` structure (confirmed)
- `agents/` at plugin root (confirmed)
- `hooks/hooks.json` at plugin root (confirmed)
- `bin/` at plugin root for executables added to PATH (confirmed)
- `output-styles/` at plugin root (confirmed)
- All component directories at plugin root, NOT inside `.claude-plugin/` (confirmed)

### Project `.claude/` Directory (Non-Plugin)
- `CLAUDE.md` at project root (confirmed)
- `.mcp.json` at project root (confirmed)
- `.worktreeinclude` at project root (confirmed -- documented in common-workflows)
- `.claude/settings.json` (confirmed)
- `.claude/settings.local.json` (confirmed, gitignored)
- `.claude/rules/` for path-scoped rules (confirmed)
- `.claude/skills/` (confirmed)
- `.claude/commands/` (confirmed)
- `.claude/output-styles/` (confirmed)
- `.claude/agents/` (confirmed)
- `.claude/agent-memory/` with `memory: project` (confirmed in subagents docs)
- `.claude/agent-memory-local/` with `memory: local` (confirmed, gitignored)

### plugin.json Schema
- `name` is the ONLY required field (confirmed)
- `name` is kebab-case and doubles as namespace prefix (confirmed)
- `version` (semver string, optional) (confirmed)
- `description` (string, optional) (confirmed)
- `author` object with `{name, email?, url?}` (confirmed)
- `homepage` (string, optional) (confirmed)
- `repository` (string, optional) (confirmed)
- `license` (string, SPDX, optional) (confirmed)
- `keywords` (array, optional) (confirmed)

### Component Path Overrides
- `commands` (string or array, default `commands/`) (confirmed)
- `agents` (string or array, default `agents/`) (confirmed)
- `skills` (string or array, default `skills/`) (confirmed)
- `hooks` (string, array, or object, default `hooks/hooks.json`) (confirmed)
- `mcpServers` (string, array, or object, default `.mcp.json`) (confirmed)
- `lspServers` (string, array, or object, default `.lsp.json`) (confirmed)
- `outputStyles` (string or array, default `output-styles/`) (confirmed)
- Custom paths REPLACE defaults (confirmed)
- All paths relative to plugin root, prefixed with `./` (confirmed)

### userConfig
- Schema with `description` and `sensitive` fields (confirmed)
- Available as `${user_config.KEY}` in MCP/LSP configs, hook commands (confirmed)
- Non-sensitive in skill/agent content (confirmed)
- Exported as `CLAUDE_PLUGIN_OPTION_<KEY>` env vars (confirmed)
- Non-sensitive stored in `settings.json` under `pluginConfigs[<id>].options` (confirmed)
- Sensitive stored in system keychain with fallback to `~/.claude/.credentials.json` (confirmed)
- ~2 KB total limit shared with OAuth (confirmed)

### channels
- Schema with `server` and optional `userConfig` (confirmed)
- `server` must match a key in plugin's `mcpServers` (confirmed)
- Per-channel `userConfig` uses same schema as top-level (confirmed)

### Environment Variables
- `${CLAUDE_PLUGIN_ROOT}` -- absolute path to plugin install dir (confirmed)
- `${CLAUDE_PLUGIN_DATA}` -- persistent data dir at `~/.claude/plugins/data/{id}/` (confirmed)
- Both substituted inline in skill/agent content, hook commands, MCP/LSP configs (confirmed)
- Both exported to subprocesses (confirmed)
- `CLAUDE_PLUGIN_ROOT` changes on update (confirmed)
- `CLAUDE_PLUGIN_DATA` survives updates, deleted on uninstall unless `--keep-data` (confirmed)

### Plugin Namespacing
- Components namespaced as `plugin-name:component-name` (confirmed)
- Namespace prefix is the `name` field from `plugin.json` (confirmed)

### settings.json (Plugin-Level)
- Only `agent` key is supported (confirmed)
- Activates a plugin agent as the main thread (confirmed)

### CLI Commands
- `claude plugin install <plugin> [-s scope]` (confirmed)
- Scopes: `user` (default), `project`, `local` (confirmed)
- `claude plugin uninstall <plugin> [-s scope] [--keep-data]` (confirmed)
- `--keep-data` preserves `${CLAUDE_PLUGIN_DATA}` (confirmed)
- `claude plugin enable <plugin> [-s scope]` (confirmed)
- `claude plugin disable <plugin> [-s scope]` (confirmed)
- `claude plugin update <plugin> [-s scope]` with `managed` scope support (confirmed)

### Installation Scopes
- `user` scope: `~/.claude/settings.json` (confirmed)
- `project` scope: `.claude/settings.json` (confirmed)
- `local` scope: `.claude/settings.local.json` (confirmed)
- `managed` scope: managed settings, update only (confirmed)

### Plugin Caching
- Marketplace plugins copied to `~/.claude/plugins/cache` (confirmed)
- Paths outside plugin dir break after install (confirmed)
- Symlinks within plugin dir followed during copy (confirmed)
- `--plugin-dir ./my-plugin` for local dev bypasses cache (confirmed)

### Marketplace Source Types
- Relative path (`"./plugins/my-plugin"`) (confirmed)
- `github` with `repo`, `ref?`, `sha?` (confirmed)
- `url` with `url`, `ref?`, `sha?` (confirmed)
- `git-subdir` with `url`, `path`, `ref?`, `sha?` (confirmed)
- `npm` with `package`, `version?`, `registry?` (confirmed)

### Managed Plugin Controls
- `strictKnownMarketplaces` -- managed only, allowlist (confirmed)
- `blockedMarketplaces` -- managed only, blocklist checked before download (confirmed)
- `pluginTrustMessage` -- managed only, custom trust warning message (confirmed)
- `extraKnownMarketplaces` -- any scope, pre-register marketplaces (confirmed)

---

## Notes

1. The CAB file's **wrapper philosophy** (line 19) is sound -- it delegates native CC behavior to official docs and focuses on CAB-specific patterns. Most "missing" items are intentionally deferred to official docs.

2. The **confidence rating of "A"** in the frontmatter is justified -- the file is highly accurate with only minor discrepancies. After fixes, this would be a solid A.

3. The **`commands/` legacy signal** (S1) is the most impactful finding for CAB users, as it could lead to building new skills in the deprecated `commands/` pattern.

4. The **`CLAUDE.md` in plugin tree** (E1) is the most significant structural error, as it conflates project-level and plugin-level concepts.
