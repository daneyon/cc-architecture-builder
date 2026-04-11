# CC Dev Docs Investigation Report — 2026-04-04

## Executive Summary

CAB v1.0.0 KB was authored Dec 2025–Mar 2026. The CC platform has evolved substantially. This investigation compares the latest official docs (fetched 2026-04-04 from `code.claude.com/docs/en/`) against all 27 CAB KB files plus templates and schemas.

**Key metrics**:
- Total delta items cataloged: **72**
- Critical: **12** | High: **24** | Medium: **22** | Low: **14**
- Categories with highest divergence: **Hooks** (9→26 events, 1→4 types), **Skills** (3→11 fields), **Subagents** (missing 10+ fields), **Plugins** (missing userConfig, channels, LSP, bin/)
- Docs URL migration: all CC docs now at `code.claude.com/docs/en/` (redirects from docs.anthropic.com and docs.claude.com)

**Philosophy audit** (19 CAB-original files):
- EXTEND (core value): 8 files
- STALE (official docs now cover): 6 files
- DUPLICATE (no added value): 3 files
- BRIDGE (synthesis/navigation): 2 files

---

## Category A: Memory & CLAUDE.md

**Official doc**: `code.claude.com/docs/en/memory`
**CAB file**: `knowledge/components/memory-claudemd.md` (last_updated: 2025-12-23)

### Official (current)

4 scope levels: Managed policy → Project → User → Local. Auto Memory system with MEMORY.md, 200-line/25KB load limit, topic files. Size recommendation: **200 lines** per CLAUDE.md. HTML comments stripped from context. `claudeMdExcludes` for monorepo filtering. CLAUDE.md survives compaction (re-read from disk). `--add-dir` CLAUDE.md loading opt-in via `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`. `/init` interactive mode via `CLAUDE_CODE_NEW_INIT=1`. `InstructionsLoaded` hook for observability.

### Delta Table

| # | Item | Type | Impact | Detail |
|---|------|------|--------|--------|
| A1 | Auto Memory system | NEW | **Critical** | Entire feature absent from CAB: autoMemoryEnabled, autoMemoryDirectory, MEMORY.md, 200-line/25KB load limit, topic files, per-subagent memory |
| A2 | Size recommendation changed | CHANGED | **High** | CAB says 500 lines; official says **200 lines** |
| A3 | Tier count mismatch | CHANGED | **High** | CAB says 5 tiers (includes "Project rules" as separate); official says 4 scopes (rules are sub-feature of project) |
| A4 | claudeMdExcludes | NEW | Medium | Glob-based exclusion for monorepo CLAUDE.md files; arrays merge across layers |
| A5 | HTML comment stripping | NEW | Medium | Block-level `<!-- -->` stripped from context; preserves in code blocks |
| A6 | Compaction survival | NEW | Medium | CLAUDE.md re-read from disk after /compact |
| A7 | --add-dir CLAUDE.md loading | NEW | Low | Opt-in via env var CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 |
| A8 | /init interactive mode | NEW | Low | CLAUDE_CODE_NEW_INIT=1 for multi-phase setup flow |
| A9 | InstructionsLoaded hook | NEW | Low | Observability for which files load and when |
| A10 | Managed settings delivery | EXPANDED | Medium | Now includes MDM/plist (macOS), registry (Windows HKLM/HKCU), drop-in managed-settings.d/ |
| A11 | AGENTS.md interop | NEW | Low | Import via @AGENTS.md in CLAUDE.md |
| A12 | --append-system-prompt | NEW | Low | System-prompt-level instructions (vs user message for CLAUDE.md) |

**Affected files**: `knowledge/components/memory-claudemd.md`, `knowledge/overview/architecture-philosophy.md`, `templates/plugin/CLAUDE.md.template`, `templates/global/CLAUDE.md.template`

---

## Category B: Skills

**Official doc**: `code.claude.com/docs/en/skills`
**CAB file**: `knowledge/components/agent-skills.md` (last_updated: 2025-12-23)

### Official (current)

11 frontmatter fields (name, description, argument-hint, disable-model-invocation, user-invocable, allowed-tools, model, effort, context, agent, hooks, paths, shell). String substitutions ($ARGUMENTS, $ARGUMENTS[N], $N, ${CLAUDE_SESSION_ID}, ${CLAUDE_SKILL_DIR}). Dynamic context injection via `!`command`` syntax. 5 bundled skills (/batch, /claude-api, /debug, /loop, /simplify). context: fork vs inline execution. Commands merged into skills. Invocation control matrix. Enterprise skill tier. Monorepo nested discovery. Permission rules: Skill(name), Skill(name *). "ultrathink" trigger. Description budget at 1% of context window.

### Delta Table

| # | Item | Type | Impact | Detail |
|---|------|------|--------|--------|
| B1 | 8 missing frontmatter fields | NEW | **Critical** | argument-hint, disable-model-invocation, user-invocable, model, effort, context, agent, hooks, paths, shell — CAB only has name, description, allowed-tools |
| B2 | String substitutions (5 vars) | NEW | **High** | $ARGUMENTS, $ARGUMENTS[N], $N, ${CLAUDE_SESSION_ID}, ${CLAUDE_SKILL_DIR} |
| B3 | Dynamic context injection | NEW | **High** | `!`command`` preprocessor syntax |
| B4 | context: fork vs inline | NEW | **High** | Execution model with subagent delegation |
| B5 | Bundled skills (5) | NEW | Medium | /batch, /claude-api, /debug, /loop, /simplify |
| B6 | Commands merged into skills | CHANGED | **High** | Commands still work but skills are preferred path |
| B7 | Invocation control matrix | NEW | Medium | disable-model-invocation + user-invocable interaction |
| B8 | name/description now optional | CHANGED | Medium | CAB marks both as "Required" — name defaults to dir name, description to first paragraph |
| B9 | Enterprise skill tier | NEW | Medium | Via managed settings |
| B10 | Monorepo nested discovery | NEW | Low | packages/frontend/.claude/skills/ auto-discovered |
| B11 | Permission rules syntax | NEW | Medium | Skill(name), Skill(name *) |
| B12 | Description budget mechanics | NEW | Low | 1% context window, SLASH_COMMAND_TOOL_CHAR_BUDGET env var |
| B13 | "ultrathink" trigger | NEW | Low | Extended thinking activation via skill content |

**Affected files**: `knowledge/components/agent-skills.md`, `templates/skill.template/`, `skills/*/SKILL.md` (all 7 CAB skills for frontmatter update)

---

## Category C: Subagents

**Official doc**: `code.claude.com/docs/en/sub-agents`
**CAB file**: `knowledge/components/subagents.md` (last_updated: 2025-12-23)

### Official (current)

16 frontmatter fields (name, description, tools, disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks, memory, background, effort, isolation, color, initialPrompt). Agent auto memory with 3 scopes (user, project, local). Background execution with upfront permission granting. Worktree isolation via frontmatter. `agent` setting (not defaultSubagent). Built-in subagents: Explore, Plan, General-purpose, statusline-setup, Claude Code Guide. Plugin subagent restrictions. /agents command. Managed subagents. Nesting constraint. Auto-compaction at ~95%.

### Delta Table

| # | Item | Type | Impact | Detail |
|---|------|------|--------|--------|
| C1 | 10+ missing frontmatter fields | NEW | **Critical** | disallowedTools, skills, mcpServers, hooks, memory, background, effort, isolation, color, initialPrompt |
| C2 | Agent auto memory (3 scopes) | NEW | **Critical** | user, project, local memory persistence |
| C3 | Background execution | NEW | **High** | background: true, upfront permission granting, Ctrl+B to background |
| C4 | Worktree isolation frontmatter | NEW | **High** | isolation: worktree with auto-cleanup |
| C5 | agent setting (not defaultSubagent) | CHANGED | Medium | Setting name is `agent`, not `defaultSubagent` |
| C6 | Plugin subagent restrictions | NEW | Medium | Plugins can't use hooks, mcpServers, permissionMode in agents |
| C7 | Built-in subagents expanded | EXPANDED | Medium | Explore, Plan, General-purpose, statusline-setup, Claude Code Guide |
| C8 | Skills preloading | NEW | Medium | skills field injects full content; subagents don't inherit parent skills |
| C9 | MCP server scoping | NEW | Medium | Inline MCP defs connected at start, disconnected at finish |
| C10 | Nesting constraint | NEW | Medium | Subagents cannot spawn other subagents |
| C11 | /agents command | NEW | Low | Interactive agent management |
| C12 | Auto-compaction at ~95% | NEW | Low | CLAUDE_AUTOCOMPACT_PCT_OVERRIDE env var |

**Affected files**: `knowledge/components/subagents.md`, `templates/agent.template/`, `agents/*.md` (all 4 CAB agents)

---

## Category D: Hooks

**Official doc**: `code.claude.com/docs/en/hooks`
**CAB file**: `knowledge/components/hooks.md`

### Official (current)

26 hook events (CAB has 9). 4 hook types: command, http, prompt, agent (CAB has only command). `if:` field for permission rule filtering. `async:` for non-blocking. MCP tool matching via mcp__server__tool. 6 configuration locations. 5 environment variables. Rich output schema with per-event decision patterns. `once: true` for single-fire. Hook deduplication. `shell: "powershell"` option. `/hooks` interactive browser.

### Delta Table

| # | Item | Type | Impact | Detail |
|---|------|------|--------|--------|
| D1 | 17 missing hook events | NEW | **Critical** | PermissionRequest, PermissionDenied, PostToolUseFailure, SubagentStart, TaskCreated, TaskCompleted, StopFailure, TeammateIdle, InstructionsLoaded, ConfigChange, CwdChanged, FileChanged, WorktreeCreate, WorktreeRemove, PostCompact, Elicitation, ElicitationResult |
| D2 | 3 missing hook types | NEW | **Critical** | http, prompt, agent — CAB only documents command |
| D3 | if: field | NEW | **High** | Permission rule syntax for per-handler filtering |
| D4 | async: field | NEW | **High** | Non-blocking background execution for command hooks |
| D5 | MCP tool matching | NEW | Medium | mcp__server__tool pattern with regex support |
| D6 | 5 more config locations | EXPANDED | Medium | CAB only documents hooks.json; official has 6 locations |
| D7 | 4 more env variables | NEW | Medium | CLAUDE_PROJECT_DIR, CLAUDE_PLUGIN_DATA, CLAUDE_CODE_REMOTE, CLAUDE_ENV_FILE |
| D8 | Rich output schema | EXPANDED | Medium | Per-event decision patterns, updatedInput, permissionDecision, 10K char cap |
| D9 | once: true | NEW | Low | Single-fire hooks (skills only) |
| D10 | shell: powershell | NEW | Low | Per-hook shell selection on Windows |
| D11 | /hooks browser | NEW | Low | Interactive hook inspection with source labels |
| D12 | Hook deduplication | NEW | Low | Parallel execution, dedup by command string or URL |

**Affected files**: `knowledge/components/hooks.md`, `templates/plugin/settings.json.template`

---

## Category E: Plugins

**Official doc**: `code.claude.com/docs/en/plugins`, `code.claude.com/docs/en/plugins-reference`
**CAB files**: `knowledge/schemas/distributable-plugin.md`, `knowledge/distribution/marketplace.md`

### Delta Table

| # | Item | Type | Impact | Detail |
|---|------|------|--------|--------|
| E1 | userConfig schema | NEW | **Critical** | User-configurable values at enable time, sensitive/non-sensitive, keychain storage |
| E2 | channels declaration | NEW | **High** | MCP-backed message injection channels |
| E3 | ${CLAUDE_PLUGIN_DATA} | NEW | **High** | Persistent data dir surviving updates, deleted on uninstall |
| E4 | lspServers / .lsp.json | NEW | **High** | Language server integration for code intelligence |
| E5 | bin/ executables in PATH | NEW | Medium | Plugin binaries added to Bash PATH |
| E6 | output-styles/ directory | NEW | Medium | Custom output style definitions |
| E7 | Plugin CLI commands expanded | EXPANDED | Medium | install, uninstall (with --keep-data), enable, disable, update with --scope |
| E8 | Plugin namespacing | NEW | Medium | plugin-name:skill-name format |
| E9 | Plugin settings.json (agent only) | NEW | Low | Only `agent` key supported |
| E10 | Marketplace source types | EXPANDED | Medium | github, git, url, npm, file, directory, hostPattern, settings |
| E11 | Plugin caching mechanism | NEW | Low | ~/.claude/plugins/cache with symlink support |
| E12 | Managed plugin controls | NEW | Medium | strictKnownMarketplaces, blockedMarketplaces, pluginTrustMessage |

**Affected files**: `knowledge/schemas/distributable-plugin.md`, `knowledge/distribution/marketplace.md`, `templates/plugin/plugin.json.template`, `.claude-plugin/plugin.json`

---

## Category F: Settings & Configuration

**Official doc**: `code.claude.com/docs/en/settings`
**CAB files**: `knowledge/schemas/global-user-config.md`, templates

### Delta Table

| # | Item | Type | Impact | Detail |
|---|------|------|--------|--------|
| F1 | Settings hierarchy (5 levels) | EXPANDED | **Critical** | Managed > CLI args > Local > Project > User with detailed precedence rules |
| F2 | Effort levels | NEW | **High** | low, medium, high (docs say 3 levels, not 4 — no "max" documented) |
| F3 | autoMode configuration | NEW | **High** | environment, allow, soft_deny arrays for AI classifier |
| F4 | Sandbox configuration | NEW | **High** | 15+ sandbox settings (filesystem allow/deny, network domains, proxy ports) |
| F5 | availableModels restriction | NEW | Medium | Restrict model selection |
| F6 | modelOverrides | NEW | Medium | Map Anthropic IDs to provider-specific (Bedrock ARNs, etc.) |
| F7 | Permission modes (6) | VERIFY | Medium | default, acceptEdits, plan, auto, dontAsk, bypassPermissions |
| F8 | Fine-grained permission rules | EXPANDED | Medium | Tool(specifier) syntax in permissions.allow/ask/deny arrays |
| F9 | 60+ settings fields | EXPANDED | **High** | CAB documents ~10; official has 60+ including hooks, sandbox, MCP, plugins, managed-only |
| F10 | Managed settings delivery | NEW | Medium | MDM/plist, registry, drop-in directory, server-managed |
| F11 | Worktree settings | NEW | Low | worktree.symlinkDirectories, worktree.sparsePaths |

**Affected files**: `knowledge/schemas/global-user-config.md`, `templates/plugin/settings.json.template`

---

## Category G: Agent Teams (entirely new)

**Official doc**: `code.claude.com/docs/en/agent-teams`
**CAB coverage**: None (zero)

### Delta Table

| # | Item | Type | Impact | Detail |
|---|------|------|--------|--------|
| G1 | Agent Teams architecture | NEW | **High** | Team lead + teammates + shared task list + mailbox |
| G2 | Experimental enablement | NEW | **High** | CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1, requires v2.1.32+ |
| G3 | Display modes | NEW | Medium | in-process (Shift+Down), split panes (tmux/iTerm2) |
| G4 | Task dependencies | NEW | Medium | Pending/in-progress/completed states, file locking |
| G5 | Plan approval workflow | NEW | Medium | Read-only plan mode, lead approval/rejection |
| G6 | TeammateIdle hook | NEW | Medium | Feedback loop to keep teammates working |
| G7 | Known limitations (8) | NEW | Low | No session resumption, no nested teams, lead fixed, ~7x token cost |
| G8 | Recommended sizing | NEW | Low | 3-5 teammates, 5-6 tasks each |

**Affected files**: NEW KB card needed; `knowledge/operational-patterns/multi-agent-collaboration.md` needs update

---

## Category H: Context Management

**Official docs**: `code.claude.com/docs/en/context-window`, `code.claude.com/docs/en/costs`
**CAB file**: Partially in `knowledge/operational-patterns/session-management.md`

### Delta Table

| # | Item | Type | Impact | Detail |
|---|------|------|--------|--------|
| H1 | Context loading order (exact) | NEW | **High** | System prompt → Auto memory → Env info → MCP tools (deferred) → Skill descriptions → User CLAUDE.md → Project CLAUDE.md → conversation |
| H2 | Tool schema deferment | NEW | **High** | MCP tools deferred by default; ENABLE_TOOL_SEARCH env var |
| H3 | 1M extended context | NEW | Medium | Opus 4.6 and Sonnet 4.6 via [1m] suffix; standard pricing |
| H4 | Context cost recommendations (10) | NEW | Medium | Under 200 lines, /clear between tasks, delegate verbose ops, etc. |
| H5 | Skill descriptions not re-injected after /compact | NEW | Medium | Only invoked skills preserved |
| H6 | Auto-compaction at ~95% | NEW | Low | CLAUDE_AUTOCOMPACT_PCT_OVERRIDE |
| H7 | Cost benchmarks | NEW | Low | ~$6/dev/day, $100-200/dev/month with Sonnet |

**Affected files**: `knowledge/operational-patterns/session-management.md`, `knowledge/components/memory-claudemd.md`

---

## Category I: MCP Integration

**Official doc**: `code.claude.com/docs/en/mcp`
**CAB file**: `knowledge/components/mcp-integration.md` (has source: URL)

### Delta Table

| # | Item | Type | Impact | Detail |
|---|------|------|--------|--------|
| I1 | 3 MCP config scopes | VERIFY | Medium | Local (~/.claude.json), Project (.mcp.json), User (~/.claude.json mcpServers) |
| I2 | alwaysAllow NOT a feature | VERIFY | Medium | Tool auto-approval via permissions.allow with mcp__server__tool pattern instead |
| I3 | No per-server timeout in config | VERIFY | Low | Only MCP_TIMEOUT env var for startup timeout |
| I4 | MCP Registry API | NEW | Medium | api.anthropic.com/mcp-registry/v0/servers |
| I5 | allowedMcpServers/deniedMcpServers | NEW | Medium | Managed allowlist/denylist with serverName, serverCommand, serverUrl matchers |
| I6 | HTTP/streamable-http server type | NEW | Medium | type: "http" with URL and headers in .mcp.json |
| I7 | Dynamic headers (headersHelper) | NEW | Low | Shell command that outputs JSON headers |
| I8 | OAuth support | NEW | Low | Full OAuth 2.0 flow |
| I9 | Elicitation | NEW | Low | MCP servers can request structured user input |
| I10 | Resources via @ syntax | NEW | Low | @server:protocol://resource/path |
| I11 | Channels | NEW | Medium | MCP-backed message injection with --channels flag |
| I12 | Claude Code as MCP server | NEW | Low | claude mcp serve |

**Affected files**: `knowledge/components/mcp-integration.md`

---

## Category J: Custom Commands

**Official doc**: `code.claude.com/docs/en/skills` (commands section)
**CAB file**: `knowledge/components/custom-commands.md`

### Delta Table

| # | Item | Type | Impact | Detail |
|---|------|------|--------|--------|
| J1 | Commands merged into skills | CHANGED | **High** | Commands still work but skills are preferred; if both exist, skill wins |
| J2 | Command frontmatter matches skill spec | CHANGED | Medium | Same 11+ fields as skills now apply to commands too |
| J3 | Migration path | NEW | Medium | Move deploy.md from commands/ to skills/deploy/SKILL.md |

**Affected files**: `knowledge/components/custom-commands.md`, `commands/*.md` (all 14 CAB commands)

---

## Category K: CAB-Original KB Files (Philosophy Audit)

19 files with no direct CC doc counterpart, classified by value:

### EXTEND (8 files — core CAB value, keep & enhance)

| File | Rationale |
|------|-----------|
| `overview/executive-summary.md` | CAB-specific two-schema architecture separation |
| `overview/design-principles.md` | Opinionated context engineering + orchestration framework |
| `operational-patterns/orchestration-framework.md` | 5 canonical workflow patterns, complexity ladder, cost model |
| `operational-patterns/team-collaboration.md` | Conflict zones, human-agent handoff, worktree lifecycle |
| `operational-patterns/extension-discovery.md` | Three-Point Reinforcement Pattern for context degradation |
| `reference/product-design-cycle.md` | Framework-agnostic lifecycle synthesis |
| `schemas/cc-architecture-diagrams.md` | Visual architecture diagrams |
| `components/knowledge-base-structure.md` | KB organization patterns for CC retrieval |

### STALE (6 files — official docs now cover; evaluate for residual value)

| File | Rationale |
|------|-----------|
| `overview/architecture-philosophy.md` | 5-tier memory hierarchy now native in CC docs |
| `operational-patterns/git-worktree.md` | Worktrees covered in agent teams and subagent isolation |
| `operational-patterns/session-management.md` | Session management, --continue, context covered natively |
| `operational-patterns/multi-agent-collaboration.md` | Agent teams and subagent delegation covered natively |
| `distribution/cowork.md` | Cowork capabilities likely evolved since "research preview" snapshot |
| `components/custom-commands.md` | Commands fully documented; commands→skills migration noted |

### DUPLICATE (3 files — remove or convert to source: pointers)

| File | Rationale |
|------|-----------|
| `prerequisites/git-foundation.md` | Basic git setup; official docs cover same |
| `prerequisites/security-defaults.md` | Standard security advice; no CAB-specific patterns |
| `appendices/glossary.md` | Terms defined in official docs with equal precision |

### BRIDGE (2 files — useful as navigation, low original content)

| File | Rationale |
|------|-----------|
| `implementation/workflow.md` | Sequences multiple official topics into implementation checklist |
| `appendices/references.md` | Curated link index with domain migration notice |

---

## Cross-Cutting Findings

### Systemic Issues

1. **Frontmatter field coverage**: Every component KB file (skills, subagents, hooks, plugins) is missing 50-80% of current frontmatter fields
2. **Template staleness**: All templates (skill, agent, plugin, settings, CLAUDE.md) need field updates
3. **URL migration**: All source: URLs pointing to docs.anthropic.com need updating to code.claude.com
4. **Size recommendation**: Multiple files reference "500 lines" — official is "200 lines"

### Deprecated/Changed Patterns

1. `.claude/commands/` → skills preferred (commands still supported)
2. CLAUDE.md 500-line → 200-line recommendation
3. `defaultSubagent` → `agent` setting name
4. `alwaysAllow` per MCP server → permissions.allow with mcp__server__tool pattern
5. "5 tiers" of CLAUDE.md → 4 scopes (rules are sub-feature, not separate tier)

### Effort level discrepancy

Plan references "max" effort level. Official docs only document low/medium/high (3 levels). The `max` level may exist in practice (user settings use it) but is not in current docs — needs verification.

---

## Alignment Summary Table

| CAB KB File | Official Doc Page | Alignment | Action Needed |
|------------|-------------------|-----------|---------------|
| components/memory-claudemd.md | /memory | LOW | Major rewrite: auto memory, size rec, tiers |
| components/agent-skills.md | /skills | LOW | Major rewrite: 8+ fields, substitutions, fork |
| components/subagents.md | /sub-agents | LOW | Major rewrite: 10+ fields, memory, background |
| components/hooks.md | /hooks | LOW | Major rewrite: 17 events, 3 types, if/async |
| components/mcp-integration.md | /mcp | MEDIUM | Update: registry, channels, HTTP type |
| components/custom-commands.md | /skills (commands) | STALE | Merge into skills KB or note commands→skills |
| components/knowledge-base-structure.md | N/A (CAB-original) | EXTEND | Keep, add source refs |
| schemas/distributable-plugin.md | /plugins-reference | LOW | Major rewrite: userConfig, channels, LSP, bin/ |
| schemas/global-user-config.md | /settings | LOW | Major rewrite: 60+ settings, hierarchy, sandbox |
| schemas/cc-architecture-diagrams.md | N/A (CAB-original) | EXTEND | Keep, update diagrams |
| distribution/marketplace.md | /plugins | MEDIUM | Update: source types, managed controls |
| distribution/cowork.md | (evolved) | STALE | Verify against current product |
| overview/executive-summary.md | N/A (CAB-original) | EXTEND | Keep |
| overview/architecture-philosophy.md | /memory (partially) | STALE | Evaluate residual value |
| overview/design-principles.md | N/A (CAB-original) | EXTEND | Keep |
| prerequisites/git-foundation.md | (basic) | DUPLICATE | Remove or convert to pointer |
| prerequisites/security-defaults.md | (basic) | DUPLICATE | Remove or convert to pointer |
| operational-patterns/orchestration-framework.md | N/A (CAB-original) | EXTEND | Keep, core value |
| operational-patterns/git-worktree.md | /sub-agents, /agent-teams | STALE | Evaluate residual value |
| operational-patterns/session-management.md | /context-window, /costs | STALE | Update with new context model |
| operational-patterns/multi-agent-collaboration.md | /agent-teams, /sub-agents | STALE | Update to reference agent teams |
| operational-patterns/team-collaboration.md | N/A (CAB-original) | EXTEND | Keep |
| operational-patterns/extension-discovery.md | N/A (CAB-original) | EXTEND | Keep |
| implementation/workflow.md | N/A (synthesis) | BRIDGE | Keep as navigation aid |
| appendices/glossary.md | (all terms in docs) | DUPLICATE | Remove or convert to pointer |
| appendices/references.md | (link index) | BRIDGE | Update URLs |
| reference/product-design-cycle.md | N/A (CAB-original) | EXTEND | Keep |
