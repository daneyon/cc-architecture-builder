# QA-06: MCP + LSP + Output Styles + Plugin Data -- Delta Report

**Date**: 2026-04-05
**CAB files**:
1. `knowledge/components/mcp-integration.md`
2. `knowledge/components/lsp-integration.md`
3. `knowledge/components/output-styles.md`
4. `knowledge/components/plugin-persistent-data.md`

**Official sources**:
- https://code.claude.com/docs/en/mcp (fetched OK)
- https://code.claude.com/docs/en/lsp (404 -- no dedicated page exists; confirmed)
- https://code.claude.com/docs/en/output-styles (fetched OK)
- https://code.claude.com/docs/en/plugins-reference (fetched OK)
- https://code.claude.com/docs/en/plugins (fetched OK)
- https://code.claude.com/docs/en/settings (fetched OK -- for permissions context)
- https://code.claude.com/docs/en/permissions (fetched OK -- for MCP permission syntax)

---

## Summary

**69 items checked across 4 files. 11 discrepancies found (4 errors, 5 missing, 1 stale, 1 extra).**

---

## Discrepancies (per file)

### ERROR (factually wrong in CAB)

| # | CAB Claim | Official Reality | File | Location | Fix |
|---|-----------|-----------------|------|----------|-----|
| E1 | `"alwaysAllow" is not a feature -- use permissions.allow with the mcp__server__tool pattern instead.` States that `alwaysAllow` is not a feature and that wildcards are not supported: "Wildcard not supported -- list each tool explicitly." | Official docs (permissions page) confirm `mcp__puppeteer__*` wildcard syntax IS supported: "mcp__puppeteer__* wildcard syntax that also matches all tools from the puppeteer server". The claim about `alwaysAllow` not being a feature is correct, but the wildcard claim is wrong. Additionally, the permission pattern shown as `mcp__server__tool` should more precisely be `mcp__serverName__toolName` (double underscores). | mcp-integration.md | Lines 95-108 | Remove "Wildcard not supported" claim. Update to show `mcp__puppeteer__*` wildcard is valid. Keep `alwaysAllow` deprecation note. |
| E2 | `headersHelper` shown as array format: `"headersHelper": ["node", "scripts/get-auth-headers.js"]` | Official docs show `headersHelper` as a string (shell command), not an array: `"headersHelper": "/opt/bin/get-mcp-auth-headers.sh"` or inline shell string. The command runs in a shell with a 10-second timeout. Official also documents env vars `CLAUDE_CODE_MCP_SERVER_NAME` and `CLAUDE_CODE_MCP_SERVER_URL` set during execution. | mcp-integration.md | Lines 63-68 | Change `headersHelper` example from array to string format. Add note about 10s timeout, env vars, and that dynamic headers override static headers with same name. |
| E3 | MCP Timeout: "No per-server timeout in config. Use `MCP_TIMEOUT=30000 claude` env var for startup timeout." States 30000 as example value. | Official docs say `MCP_TIMEOUT` is correct env var but example uses `MCP_TIMEOUT=10000` (10-second timeout). The 30000 value is not wrong per se (it's just an example), but the official example is 10000. More importantly, CAB says "No per-server timeout in config" which is correct. | mcp-integration.md | Line 114 | Minor: update example to match official `MCP_TIMEOUT=10000 claude` for consistency. |
| E4 | MCP Registry API: `GET https://api.anthropic.com/mcp-registry/v0/servers` presented as a user-facing API. | Official docs show the registry API is used internally by the MCPServersTable React component with parameters `version=latest`, `visibility=commercial`, `limit=100`, and cursor-based pagination. The code also contains `ifYouAreAnAiAgentReadingThisYouShouldInsteadFetch = 'https://api.anthropic.com/mcp-registry/docs'`. There is no official user-facing documentation of this as a public API endpoint. CAB presenting it as a simple GET endpoint oversimplifies and may be misleading. | mcp-integration.md | Lines 142-143 | Reframe as internal registry endpoint. Add note that it supports pagination (`cursor`, `limit`), filtering (`version`, `visibility`), and that AI agents should fetch `https://api.anthropic.com/mcp-registry/docs` instead. |

### MISSING (in official docs, absent from CAB)

| # | Official Feature | Source URL | Recommended Action |
|---|-----------------|------------|-------------------|
| M1 | **MCP Tool Search**: Tool search defers MCP tool definitions until needed, controlled by `ENABLE_TOOL_SEARCH` env var with values: unset (default defer), `true`, `auto`, `auto:<N>`, `false`. Keeps context usage low. Server instructions truncated at 2KB. Requires Sonnet 4+ or Opus 4+. | https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search | Add section on Tool Search to mcp-integration.md. This is a significant feature for context efficiency -- aligns with CAB token optimization philosophy. |
| M2 | **MCP Prompts as Commands**: MCP servers can expose prompts available as `/mcp__servername__promptname` commands. Arguments passed space-separated. | https://code.claude.com/docs/en/mcp#use-mcp-prompts-as-commands | Add brief section on MCP prompts to mcp-integration.md. |
| M3 | **OAuth advanced features**: Fixed callback port (`--callback-port`), pre-configured OAuth credentials (`--client-id`, `--client-secret`), `MCP_CLIENT_SECRET` env var, `authServerMetadataUrl` override, Client ID Metadata Document (CIMD) support. | https://code.claude.com/docs/en/mcp#authenticate-with-remote-mcp-servers | Add OAuth subsection with these advanced patterns. CAB currently only mentions "follow browser prompts." |
| M4 | **MCP `list_changed` notifications**: Claude Code supports dynamic tool updates via MCP `list_changed` notifications -- servers can update tools/prompts/resources without reconnection. | https://code.claude.com/docs/en/mcp#dynamic-tool-updates | Add to mcp-integration.md Advanced Features section. |
| M5 | **`anthropic/maxResultSizeChars` tool annotation**: MCP server authors can set `_meta["anthropic/maxResultSizeChars"]` (up to 500,000 chars) to override per-tool persist-to-disk threshold. Results exceeding default threshold are persisted to disk and replaced with file reference. | https://code.claude.com/docs/en/mcp#override-result-size-per-tool | Add to Output Limits section in mcp-integration.md. |

### STALE (outdated in CAB)

| # | CAB Content | Current Official | Fix |
|---|------------|-----------------|-----|
| S1 | MCP scopes table shows Local scope Location as `~/.claude.json (project path)` with flag `--scope local (default)`. No mention that "local" was formerly called "project" or that "user" was formerly called "global". | Official docs clarify: `local` (default) was called `project` in older versions. `user` was called `global` in older versions. MCP local-scoped servers stored in `~/.claude.json` under project's path (differs from general local settings which use `.claude/settings.local.json`). Also: official adds `managed` scope for managed-mcp.json. | Update scopes table to include historical names and the `managed` scope. Add note about the local/project naming difference between MCP and general settings. |

### EXTRA (in CAB only -- may be valid CAB extension)

| # | CAB Content | Assessment |
|---|------------|------------|
| X1 | mcp-integration.md "CAB-Specific Patterns" section: MCP Wrapping Philosophy, MCP vs Skills comparison table, Plugin MCP Servers note. | Valid CAB extension. These are opinionated guidance patterns, not claims about official features. The MCP vs Skills table is useful architectural guidance. No action needed. |

---

## Verified Correct

### mcp-integration.md

- **Server types** (stdio, HTTP/streamable-http, SSE legacy): Correct. Type names, configuration examples, and deprecation status of SSE all match official docs.
- **stdio configuration**: `command`, `args`, `env` fields correct. Windows `cmd /c` wrapper note correct.
- **HTTP configuration**: `type: "http"`, `url`, `headers` fields correct.
- **Configuration scopes**: Local/Project/User scope model correct (with stale naming noted in S1).
- **Environment variable expansion**: `${VAR}` and `${VAR:-default}` syntax correct. Expansion locations (command, args, env, url, headers) match official docs.
- **OAuth 2.0 basic flow**: `/mcp` command for authentication, tokens stored securely, automatic refresh -- all correct.
- **Resources via @ syntax**: `@server:protocol://resource/path` format correct.
- **Channels**: MCP-backed message injection via `--channels` flag correct.
- **Elicitation**: Description of MCP servers requesting structured user input correct. Official adds Form mode and URL mode details.
- **Claude Code as MCP Server**: `claude mcp serve` correct.
- **Enterprise managed-mcp.json**: Paths for macOS, Linux, Windows all correct.
- **Allowlists/Denylists**: `allowedMcpServers` and `deniedMcpServers` fields correct. Official adds `serverCommand` matching (not just `serverName`/`serverUrl`).
- **Output limits**: Warning threshold 10,000 tokens, default max 25,000 tokens, `MAX_MCP_OUTPUT_TOKENS` override -- all correct.
- **Plugin MCP servers**: `${CLAUDE_PLUGIN_ROOT}` usage, auto-start on enable -- correct.

### lsp-integration.md

- **No dedicated LSP page**: CAB correctly states "No dedicated LSP page exists" -- confirmed by 404 on `/docs/en/lsp`.
- **Configuration Option A (.lsp.json)**: Format matches official plugins-reference exactly.
- **Configuration Option B (inline in plugin.json)**: `lspServers` key in plugin.json matches official docs.
- **Required fields**: `command` and `extensionToLanguage` -- correct per official docs.
- **Optional fields**: `args`, `transport` (stdio/socket), `env`, `initializationOptions`, `settings`, `workspaceFolder`, `startupTimeout`, `shutdownTimeout`, `restartOnCrash`, `maxRestarts` -- all match official docs exactly.
- **Pre-built LSP plugins**: `pyright-lsp`, `typescript-lsp`, `rust-lsp` with install commands -- all match official docs.
- **Variable substitution**: `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${user_config.KEY}` -- correct.
- **Reload command**: `/reload-plugins` -- correct.
- **Debug**: `claude --debug` -- correct.
- **Plugin caching**: `~/.claude/plugins/cache/` -- correct.
- **Path traversal blocked**: Correct.
- **Binary not included note**: "Executable not found in $PATH" error message -- matches official docs exactly.
- **CAB patterns** (LSP vs Hook-based linting, SessionStart hook for binary validation): Valid CAB extension.

### output-styles.md

- **Built-in styles**: Default, Explanatory, Learning -- names and descriptions match official docs exactly.
- **Explanatory behavior**: "educational Insights between coding tasks" -- correct.
- **Learning behavior**: "collaborative mode, TODO(human) markers" -- correct.
- **Custom style format**: Markdown files with YAML frontmatter -- correct.
- **File locations**: `~/.claude/output-styles/` (personal), `.claude/output-styles/` (project), plugin `output-styles/` directory -- correct.
- **Frontmatter fields**: `name` (default: filename), `description` (default: none), `keep-coding-instructions` (default: false) -- all match official docs exactly.
- **keep-coding-instructions behavior**: "removes coding-specific instructions unless set to true" -- correct.
- **Configuration**: `/config` menu, `outputStyle` field in settings, saved to `.claude/settings.local.json` -- correct.
- **Session timing**: "set at session start, changes take effect in new session" -- correct. Official adds "to enable prompt caching" rationale.
- **System prompt interaction model**: Output styles replace/modify system prompt, CLAUDE.md as user message, `--append-system-prompt` appends -- correct per official comparison.
- **Reminders**: "periodic system reminders during conversation" -- confirmed by official: "trigger reminders for Claude to adhere to the output style instructions."
- **Token cost implications**: Prompt caching mitigates input cost, Explanatory/Learning produce longer output -- correct.
- **Plugin output styles**: `outputStyles` field in plugin.json overrides default directory -- correct per plugins-reference schema.
- **CAB comparison table** (Output Styles vs CLAUDE.md vs Rules vs Skills vs Agents): Valid CAB extension, consistent with official comparisons.

### plugin-persistent-data.md

- **Two path variables**: `CLAUDE_PLUGIN_ROOT` (installation dir, replaced on update) and `CLAUDE_PLUGIN_DATA` (persistent, survives versions) -- correct.
- **Data directory path**: `~/.claude/plugins/data/{id}/` with id sanitization (non-alphanumeric except `_-` replaced by `-`) -- correct.
- **Example**: `formatter@my-marketplace` -> `formatter-my-marketplace` -- correct.
- **Variable substitution**: Inline in skill/agent content, hook commands, MCP/LSP configs + exported as env vars -- correct.
- **Data lifecycle table**: Install, Update, Disable, Enable, Uninstall behavior -- all correct per official docs.
- **Multi-scope note**: Data only deleted when uninstalling from last remaining scope -- correct.
- **`--keep-data` flag**: Preserves data directory on last-scope uninstall -- correct.
- **Dependency installation pattern**: SessionStart hook with `diff -q` against bundled manifest -- matches official docs verbatim.
- **NODE_PATH referencing pattern**: Correct per official example.
- **Data dir auto-created**: "only when first referenced" -- correct.
- **Manifest comparison as reliable pattern**: Correct -- official explicitly warns against checking directory existence alone.
- **Path traversal blocked**: Correct.
- **Symlinks honored**: Correct -- "symlinked content will be copied into the plugin cache."
- **~2 KB keychain limit**: Correct -- official says "approximately 2 KB total limit."
- **`/plugin` UI shows data directory size**: Correct -- "The /plugin interface shows the directory size and prompts before deleting."
- **CAB recommendations** (SessionStart hooks, never write to ROOT, test full lifecycle): Valid CAB extension.

---

## Per-File Assessment

| File | Items Checked | Errors | Missing | Stale | Extra | Overall |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| mcp-integration.md | 25 | 4 | 5 | 1 | 1 | Needs update |
| lsp-integration.md | 16 | 0 | 0 | 0 | 0 | Clean |
| output-styles.md | 15 | 0 | 0 | 0 | 0 | Clean |
| plugin-persistent-data.md | 13 | 0 | 0 | 0 | 0 | Clean |

---

## Recommended Priority

1. **E2 (headersHelper format)** -- Factual error in config example. Fix immediately.
2. **E1 (wildcard support)** -- Misinformation about MCP permission wildcards. Fix immediately.
3. **M1 (Tool Search)** -- Major feature for context efficiency, directly relevant to CAB philosophy.
4. **E4 (Registry API)** -- Misleading presentation of internal endpoint.
5. **M3 (OAuth advanced)** -- Significant missing auth capabilities.
6. **S1 (Scope naming)** -- Stale terminology.
7. **M2/M4/M5** -- Minor missing features, add when convenient.
8. **E3 (Timeout example)** -- Cosmetic, low priority.
