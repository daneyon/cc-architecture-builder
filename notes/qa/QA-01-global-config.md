# QA-01: Global User Configuration — Delta Report

**Date**: 2026-04-05
**CAB file**: `knowledge/schemas/global-user-config.md`
**Official sources**:
- https://code.claude.com/docs/en/settings (fetched successfully)
- https://code.claude.com/docs/en/configuration (404 — page does not exist; settings page covers this)
- https://code.claude.com/docs/en/memory (fetched successfully)
- https://code.claude.com/docs/en/permissions (fetched successfully)
- https://code.claude.com/docs/en/sub-agents (fetched successfully — subagent memory details)
- https://code.claude.com/docs/en/hooks (fetched successfully — hook event catalog)

## Summary

**73 items checked, 29 discrepancies found** (8 errors, 12 missing, 5 stale, 4 extra/unverifiable).

---

## Discrepancies

### ERROR (factually wrong in CAB)

| # | CAB Claim | Official Reality | Location in CAB | Fix |
|---|-----------|-----------------|-----------------|-----|
| E1 | `reasoningEffort` is the settings field name for effort level | Official field name is **`effortLevel`**, not `reasoningEffort`. Accepts `"low"`, `"medium"`, `"high"`. Written automatically by `/effort` command. Supported on Opus 4.6 and Sonnet 4.6. | Line 115, Core Settings table | Rename field from `reasoningEffort` to `effortLevel` |
| E2 | Managed settings macOS mechanism: "MDM / plist" at path `/Library/Managed Preferences/com.anthropic.claude-code.plist` | macOS managed delivery uses: (1) **Server-managed settings** from Anthropic servers, (2) **MDM** via `com.anthropic.claudecode` managed preferences domain (no hyphen in `claudecode`), (3) **File-based** at `/Library/Application Support/ClaudeCode/managed-settings.json`. The plist domain name is `com.anthropic.claudecode` not `com.anthropic.claude-code`, and the file path is not `/Library/Managed Preferences/...`. | Line 226, Managed Settings table | Update macOS row: domain = `com.anthropic.claudecode`, file path = `/Library/Application Support/ClaudeCode/managed-settings.json` |
| E3 | Managed settings Windows: registry at `HKLM\SOFTWARE\Policies\Anthropic\ClaudeCode` | Correct registry path is `HKLM\SOFTWARE\Policies\ClaudeCode` (no `\Anthropic\` segment). Also supports `HKCU\SOFTWARE\Policies\ClaudeCode` as lowest policy priority. | Line 227, Managed Settings table | Remove `Anthropic\` from registry path; add HKCU fallback note |
| E4 | Managed settings Linux: "Drop-in directory" at `/etc/claude/*.json` | Correct path is `/etc/claude-code/` (not `/etc/claude/`). File is `managed-settings.json`. Also supports `managed-settings.d/` drop-in directory with alphabetical merge. | Line 228, Managed Settings table | Fix path to `/etc/claude-code/managed-settings.json`; add drop-in dir note |
| E5 | Settings hierarchy shows 5 levels numbered 1-5, with Managed=1 (highest) and User=5 (lowest) | Official precedence is the same 5 levels but the **numbering convention is reversed** in official docs: Managed = highest, then CLI args, then Local (3), Project (4), User (5). The levels match but CAB also misses that within the managed tier there is internal precedence: server-managed > MDM/OS-level > file-based > HKCU registry. | Lines 94-99, Settings Hierarchy table | Add note about managed-tier internal precedence; note that only one managed source is used (sources do not merge across managed tiers) |
| E6 | Permission modes table lists `dontAsk` as: "Accept all except deny-listed" | Official description of `dontAsk`: "Auto-denies tools unless pre-approved via `/permissions` or `permissions.allow` rules." This is the opposite semantic — it **denies by default** and only allows pre-approved tools, not "accepts all." | Line 131, Permission Modes table | Fix dontAsk description to: "Auto-denies tools unless pre-approved via `/permissions` or `permissions.allow` rules" |
| E7 | `model` field accepts string aliases: `"sonnet"`, `"opus"`, `"haiku"` | Official docs show `model` accepts full model ID strings like `"claude-sonnet-4-6"`, not short aliases. Short aliases may work but the documented example uses full IDs. The aliases `sonnet`/`opus`/`haiku` are used in `availableModels` but `model` itself takes the model ID. | Line 113, Core Settings table | Update example value to `"claude-sonnet-4-6"` or note that aliases are convenience shortcuts |
| E8 | Hooks section references "26 events, 4 hook types" | Official docs list **29 hook events** (not 26) and 4 hook types (command, http, prompt, agent). Events include: SessionStart, InstructionsLoaded, UserPromptSubmit, PreToolUse, PermissionRequest, PermissionDenied, PostToolUse, PostToolUseFailure, Notification, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, TeammateIdle, ConfigChange, CwdChanged, FileChanged, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact, Elicitation, ElicitationResult, SessionEnd, plus 3 more. | Line 211 | Update hook event count from 26 to 29 |

### MISSING (in official docs, absent from CAB)

| # | Official Feature/Field | Source URL | Recommended Action |
|---|----------------------|------------|-------------------|
| M1 | **`attribution`** setting — customize git commit and PR attribution (replaces deprecated `includeCoAuthoredBy`) | settings page, Available Settings table | Add to Core Settings or new section |
| M2 | **`autoMemoryDirectory`** setting — custom directory for auto memory storage | settings page, Available Settings table | Add to directory structure or settings section |
| M3 | **`autoMemoryEnabled`** setting (and `/memory` command, `CLAUDE_CODE_DISABLE_AUTO_MEMORY` env var) | memory page | Add note about auto memory toggle |
| M4 | **`effortLevel`** setting (distinct from `reasoningEffort` which CAB uses) — persists effort across sessions, written by `/effort` command | settings page | Replace `reasoningEffort` with `effortLevel` (see E1) |
| M5 | **30+ additional settings fields** not mentioned in CAB: `alwaysThinkingEnabled`, `apiKeyHelper`, `autoUpdatesChannel`, `awsAuthRefresh`, `awsCredentialExport`, `cleanupPeriodDays`, `companyAnnouncements`, `defaultShell`, `disableAllHooks`, `disableAutoMode`, `disableDeepLinkRegistration`, `disabledMcpjsonServers`, `disableSkillShellExecution`, `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `env`, `fastModePerSessionOptIn`, `feedbackSurveyRate`, `fileSuggestion`, `forceLoginMethod`, `forceLoginOrgUUID`, `forceRemoteSettingsRefresh`, `httpHookAllowedEnvVars`, `allowedHttpHookUrls`, `includeCoAuthoredBy` (deprecated), `includeGitInstructions`, `language`, `otelHeadersHelper`, `outputStyle`, `plansDirectory`, `prefersReducedMotion`, `respectGitignore`, `showClearContextOnPlanAccept`, `showThinkingSummaries`, `spinnerTipsEnabled`, `spinnerTipsOverride`, `spinnerVerbs`, `statusLine`, `useAutoModeDuringPlan`, `voiceEnabled` | settings page | CAB deliberately defers to official docs for full field list — but should list count accurately (currently says "60+" which may be low); consider updating to reflect actual count |
| M6 | **Global config settings** in `~/.claude.json` (not `settings.json`): `autoConnectIde`, `autoInstallIdeExtension`, `editorMode`, `showTurnDuration`, `terminalProgressBarEnabled`, `teammateMode` | settings page, Global Config Settings table | Add a "Global Config (`~/.claude.json`) Settings" subsection or expand the existing `~/.claude.json` section |
| M7 | **Server-managed settings** — a managed settings delivery mechanism from Anthropic servers via Claude.ai admin console. CAB only mentions MDM/plist, registry, drop-in dir. | settings page | Add server-managed settings as a managed delivery mechanism |
| M8 | **`managed-settings.d/` drop-in directory** — allows fragmenting managed settings into multiple files merged alphabetically | settings page | Add to Managed Settings Delivery section |
| M9 | **`claudeMdExcludes`** setting — skip specific CLAUDE.md files by path/glob in monorepos | memory page | Add to relevant section or link |
| M10 | **`additionalDirectories`** permission setting and `--add-dir` CLI flag | settings page, Permission Settings table | Add to settings or permissions section |
| M11 | **Managed CLAUDE.md** file locations: macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`, Linux `/etc/claude-code/CLAUDE.md`, Windows `C:\Program Files\ClaudeCode\CLAUDE.md` | memory page | Add managed CLAUDE.md paths to directory structure or See Also |
| M12 | **Sandbox settings** significantly expanded beyond what CAB documents: `failIfUnavailable`, `excludedCommands`, `allowUnsandboxedCommands`, `filesystem.allowWrite`, `filesystem.denyWrite`, `filesystem.denyRead`, `filesystem.allowRead`, `filesystem.allowManagedReadPathsOnly`, `network.allowUnixSockets`, `network.allowAllUnixSockets`, `network.allowLocalBinding`, `network.httpProxyPort`, `network.socksProxyPort`, `enableWeakerNestedSandbox`, `enableWeakerNetworkIsolation`. CAB shows a simplified schema with `filesystem.allow/deny` and `network.allowedDomains/deniedDomains` that does not match official structure. | settings page, Sandbox Settings table | Update sandbox schema example to match official field names; add note about full sandbox field catalog |

### STALE (outdated in CAB)

| # | CAB Content | Current Official | Fix |
|---|------------|-----------------|-----|
| S1 | Claims "60+ settings fields" | Counting from the official Available Settings table: ~45 top-level settings + nested permission/sandbox/attribution/worktree sub-fields + 6 global config fields. The "60+" claim may be approximately correct but the number of top-level keys has grown significantly. The JSON schema at `https://json.schemastore.org/claude-code-settings.json` is the authoritative count. | Verify exact count from JSON schema; update if needed |
| S2 | Sandbox config example uses `"network": { "allowedDomains": [...], "deniedDomains": [...] }` | Official sandbox schema uses `"network": { "allowedDomains": [...] }` — there is no `deniedDomains` field in sandbox network settings. Domain denying is done via `WebFetch` deny permission rules or `network.allowManagedDomainsOnly`. | Remove `deniedDomains` from sandbox example; update to match official schema |
| S3 | Sandbox config example uses `"filesystem": { "allow": [...], "deny": [...] }` | Official sandbox filesystem fields are `allowWrite`, `denyWrite`, `denyRead`, `allowRead` — not bare `allow`/`deny`. | Update filesystem example to use official field names: `allowWrite`, `denyWrite`, `denyRead`, `allowRead` |
| S4 | CAB says `~/.claude.json` contains "UI toggles (`showTurnDuration`, `terminalProgressBarEnabled`)" — this is correct but incomplete | Also contains: `autoConnectIde`, `autoInstallIdeExtension`, `editorMode`, `teammateMode`. These are documented as "Global config settings" that must NOT go in `settings.json`. | Expand the `~/.claude.json` field list |
| S5 | `--reasoning-effort` CLI flag mentioned for per-session override | The settings field is `effortLevel`, not `reasoningEffort`. The CLI flag should be verified — the `/effort` command is the documented mechanism. | Verify CLI flag name; update to match official docs |

### EXTRA (in CAB only — may be valid CAB extension)

| # | CAB Content | Assessment |
|---|------------|------------|
| X1 | `plugins/cache/` and `plugins/data/<plugin-id>/` directory structure under `~/.claude/` | Not documented in official docs pages fetched. May be accurate internal structure but is not in public docs. **Retain as CAB extension** but mark confidence as B. |
| X2 | `work/ipc/` directory for "Agent Teams mailbox files" | Not documented in the fetched pages. Agent teams are documented elsewhere but IPC directory structure is not publicly described. **Retain as CAB extension** but mark confidence as B. |
| X3 | Behavioral note: "After 3 consecutive user denials, auto mode reverts to `default` mode for the remainder of the session" (confidence: B) | Not confirmed in fetched docs. The permissions page describes auto mode denial review (`/permissions` Recently denied tab, press `r` to retry) but does not mention the 3-denial revert. The `PermissionDenied` hook is documented. **Retain** but verify or downgrade. |
| X4 | Auto mode "2-stage AI classifier" and "system strips rules it classifies as dangerous" | Not explicitly described this way in official docs. Docs say auto mode uses "a classifier model" and "background safety checks." The 2-stage characterization is unverified. **Retain** at confidence B. |

---

## Verified Correct

The following major items in the CAB file were confirmed accurate against official documentation:

1. **Directory structure** — `~/.claude/CLAUDE.md`, `~/.claude/settings.json`, `~/.claude/rules/`, `~/.claude/skills/`, `~/.claude/commands/`, `~/.claude/agents/`, `~/.claude/projects/<project-path>/memory/`, `~/.claude/plans/` all confirmed.
2. **`keybindings.json`** — confirmed to exist at `~/.claude/keybindings.json` (from separate keybindings docs).
3. **`output-styles/`** directory — confirmed (the `outputStyle` setting references output styles).
4. **`~/.claude.json`** location — correctly placed at `~/`, not inside `.claude/`. Managed via `/config`.
5. **`settings.local.json`** for in-session permission approvals — confirmed (gitignored, local scope).
6. **Settings hierarchy 5 levels** — the 5 levels (Managed, CLI args, Local, Project, User) are correct in ordering.
7. **Merge behavior** — "Objects merge recursively. Arrays concatenate across levels. Deny rules at any level take precedence over allow rules at the same or lower level." Confirmed.
8. **Permission arrays** — `allow`, `ask`, `deny` within `permissions` object confirmed. Evaluation order: deny -> ask -> allow confirmed.
9. **Tool specifier syntax** — `Bash(git *)`, `Read(./.env)`, `mcp__*` wildcard patterns confirmed.
10. **Auto mode configuration** — `autoMode` with `environment`, `allow`, `soft_deny` arrays confirmed. Not read from shared project settings confirmed.
11. **`availableModels`** and **`modelOverrides`** settings — confirmed with correct types.
12. **Permission modes** — `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` all confirmed as valid modes.
13. **Subagent memory scopes** — `user`, `project`, `local` scopes with paths `~/.claude/agent-memory/<name>/`, `.claude/agent-memory/<name>/`, `.claude/agent-memory-local/<name>/` all confirmed.
14. **MEMORY.md loading** — "First 200 lines or 25KB" limit confirmed for both auto memory and subagent memory.
15. **`agent` setting** — confirmed: runs main thread as a named subagent.
16. **`verbose` setting** — not found as a top-level setting in the official settings table. May exist but is not in the Available Settings table. **Downgrade to unverified.**
17. **`theme` setting** — listed in CAB as a settings.json field with values `"dark"`, `"light"`, `"light-daltonized"`, `"dark-daltonized"`. Theme is stored in `~/.claude.json` per official docs ("Theme preference" in `~/.claude.json`). **Reclassified: see note below.**
18. **Worktree settings** — `worktree.symlinkDirectories` and `worktree.sparsePaths` confirmed (official uses `worktree.` prefix: `worktree.symlinkDirectories`, `worktree.sparsePaths`).
19. **Personal components** — Skills in `~/.claude/skills/` and agents in `~/.claude/agents/` available in all projects confirmed.
20. **`@` import syntax** in CLAUDE.md — confirmed with relative/absolute paths and max depth of 5 hops.

### Additional Notes on Verified Items

- **`verbose` (item 16)**: Not found in the official Available Settings table. CAB should either remove it or mark as unverified.
- **`theme` (item 17)**: The official settings page does not list `theme` in the `settings.json` Available Settings table. Theme preference is stored in `~/.claude.json` according to the settings page. CAB lists it as a `settings.json` field with values `"dark"`, `"light"`, `"light-daltonized"`, `"dark-daltonized"`. This should be moved to the `~/.claude.json` section or removed from the settings.json section.
- **Worktree field names (item 18)**: CAB uses `symlinkDirectories` and `sparsePaths` (without prefix). Official docs use `worktree.symlinkDirectories` and `worktree.sparsePaths`. The CAB table (lines 217-218) uses the short names which is acceptable if they are shown as nested under a worktree section, but should be clarified.

---

## Priority Fix Order

1. **E1** (effortLevel field name) + **E6** (dontAsk description) + **E7** (model field value) — factual errors in core settings
2. **E2/E3/E4** (managed settings paths) — all three managed delivery mechanism paths are wrong
3. **S2/S3** (sandbox schema) — field names in example code are incorrect
4. **E8** (hook count) — minor but factually wrong
5. **M1-M6** (missing settings/features) — additive improvements
6. **M7-M12** (missing infrastructure details) — lower priority additions
7. **E5** (managed tier internal precedence) — enhancement to existing correct content
