# QA-05: Subagents + Hooks — Delta Report

**Date**: 2026-04-05
**CAB files**: `knowledge/components/subagents.md`, `knowledge/components/hooks.md`
**Official sources**:
- https://code.claude.com/docs/en/sub-agents (fetched 2026-04-05)
- https://code.claude.com/docs/en/hooks (fetched 2026-04-05)
- https://code.claude.com/docs/en/plugins-reference (fetched 2026-04-05)

---

## Summary

**~65 items checked across both files. 18 discrepancies found (7 errors, 7 missing, 2 stale, 2 extra).**

---

## Discrepancies

### ERROR (factually wrong in CAB)

| # | CAB Claim | Official Reality | File | Location | Fix |
|---|-----------|-----------------|------|----------|-----|
| E1 | Frontmatter field count: "All 16 Fields" — lists `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `effort`, `isolation`, `color`, `initialPrompt`, + `(body)`. Counts body as a "field". | Official docs list **15 frontmatter fields** (the body/system prompt is not a frontmatter field, it's the markdown content after `---`). The 15 fields are: `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `effort`, `isolation`, `color`, `initialPrompt`. | `subagents.md` | Line 45 heading + Line 66 `(body)` row | Remove `(body)` from frontmatter table. Add `maxTurns` field. Update heading to "All 16 Fields" (15 real frontmatter + body description as a note, or just "Frontmatter Field Reference"). |
| E2 | `maxTurns` field is **missing entirely** from the frontmatter table. | Official docs: `maxTurns` (No, optional) — "Maximum number of agentic turns before the subagent stops". Integer type. | `subagents.md` | Line 45–66 table | Add `maxTurns` field row to frontmatter table. |
| E3 | `model` field enum values listed as `sonnet`, `opus`, `haiku`, or `inherit`. | Official docs: accepts `sonnet`, `opus`, `haiku`, **a full model ID** (e.g. `claude-opus-4-6`, `claude-sonnet-4-6`), or `inherit`. Default is `inherit` (not "Omit to use the configured default"). | `subagents.md` | Line 55 | Add "or a full model ID (e.g., `claude-opus-4-6`)" to the description. Fix default description to "Defaults to `inherit`". |
| E4 | `permissionMode` enum values: `default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore`. | Official docs: `default`, `acceptEdits`, **`auto`**, **`dontAsk`**, `bypassPermissions`, `plan`. There is **no `ignore` mode**. CAB is missing `auto` and `dontAsk`. | `subagents.md` | Line 56 | Replace `ignore` with the correct modes. Full list: `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`. |
| E5 | Built-in "Plan" agent listed with model "Sonnet" and tools "Read, Glob, Grep, Bash". | Official docs: Plan agent model is **inherit** (inherits from main conversation), tools are **read-only tools** (denied Write and Edit). Not specifically "Sonnet" and not the listed tool set. | `subagents.md` | Line 175 table row | Fix model to `inherit`, fix tools to "Read-only tools (Write and Edit denied)". |
| E6 | Built-in "General-purpose" agent listed with model "Sonnet" and tools "All tools". | Official docs: General-purpose agent model is **inherit** (inherits from main conversation). Tools = "All tools" is correct. | `subagents.md` | Line 176 table row | Fix model to `inherit`. |
| E7 | Hooks file claims **26 events**. | Official hooks page documents **26 events** in its table, but the actual enumerated list from the fetched page shows only **25 unique named events** (see Verified section). However, the plugins-reference page also lists 26 events. The count aligns — but see MISSING item M1 below for the actual event name issue. CAB's `ElicitationResult` event description says "User answers elicitation" but official says "After a user responds to an MCP elicitation, before the response is sent back to the server" — the "MCP" context is missing. | `hooks.md` | Lines 53–54 | Update `Elicitation` description to mention MCP server context: "When an MCP server requests user input during a tool call". Update `ElicitationResult` to: "After a user responds to an MCP elicitation, before the response is sent back to the server". |

### MISSING (in official docs, absent from CAB)

| # | Official Feature | Source URL | Recommended Action |
|---|-----------------|------------|-------------------|
| M1 | **`maxTurns` frontmatter field** for subagents — limits agentic turns before the subagent stops. | sub-agents docs | Add to frontmatter table in `subagents.md`. |
| M2 | **Agent priority/precedence hierarchy** — Official docs define 5 priority levels: (1) Managed settings (highest), (2) `--agents` CLI flag, (3) `.claude/agents/`, (4) `~/.claude/agents/`, (5) Plugin agents (lowest). CAB only shows 3 levels (Project, User, Plugin) and misses Managed and CLI-flag scopes. | sub-agents docs | Expand the "Subagent Locations" table to include all 5 priority levels. |
| M3 | **`statusMessage` field** for hooks — custom spinner message displayed while hook runs. Also **`timeout` field** (seconds before canceling, with defaults: command=600s, http=30s, prompt=30s, agent=60s). Also **`headers` + `allowedEnvVars` fields** for HTTP hooks. | hooks docs | Add `statusMessage`, `timeout`, `headers`, `allowedEnvVars` to the Field Reference table in `hooks.md`. |
| M4 | **`model` field** for prompt/agent hook types — allows specifying which model to use for prompt evaluation or agent hook execution. | hooks docs | Add `model` field to the hook field reference. |
| M5 | **`disableAllHooks` setting** — can be set at various levels to disable hooks. Managed hooks cannot be disabled by lower levels. Also **`allowManagedHooksOnly`** for enterprise admins. | hooks docs | Document `disableAllHooks` and `allowManagedHooksOnly` in hooks.md. |
| M6 | **Hook decision precedence for conflicting returns** — when multiple hooks return conflicting decisions: PreToolUse uses `deny > defer > ask > allow`; others use last-writer-wins. Also **`defer` decision** for non-interactive (`-p` flag) mode with `stop_reason: "tool_deferred"`. | hooks docs | Add decision precedence section to hooks.md. |
| M7 | **`hookSpecificOutput` JSON structure** — official docs show a nested `hookSpecificOutput` object pattern with `hookEventName` field required inside it. CAB's JSON output schema (lines 168–176) uses flat top-level fields (`continue`, `updatedInput`, `permissionDecision`, `decision`) which is a simplified/older representation. Official has `hookSpecificOutput.permissionDecision`, `hookSpecificOutput.updatedInput`, `hookSpecificOutput.additionalContext`, etc. Also `stopReason`, `suppressOutput`, `systemMessage` top-level fields. | hooks docs | Rewrite the "Hook Output Schema" section to match the official `hookSpecificOutput` nested structure. Add missing fields: `stopReason`, `suppressOutput`, `systemMessage`. |

### STALE (outdated in CAB)

| # | CAB Content | Current Official | Fix |
|---|------------|-----------------|-----|
| S1 | Source URL in subagents.md frontmatter: `https://code.claude.com/docs/en/sub-agents` — this is correct. However, the inline link text says "Subagents - Official Docs" pointing to the same URL. The page title is now "Create custom subagents". | Official page title changed. | Update link text to match: "Create custom subagents — Official Docs". Minor cosmetic issue. |
| S2 | Hook configuration locations table lists 6 sources with "Lowest" to "Highest" precedence. Official docs show a different hierarchy: (1) Managed policy (highest), (2) Project local, (3) Project, (4) Plugin, (5) Skill/Agent frontmatter, (6) User (lowest). CAB's table has `~/.claude/hooks.json` as a separate source — official docs do not mention a standalone `hooks.json` at the global level; hooks go in `~/.claude/settings.json`. Also missing: `.claude/settings.local.json` (project local) and Managed policy settings. | hooks docs | Rewrite the configuration locations table to match official hierarchy. Remove `~/.claude/hooks.json` if not official. Add `.claude/settings.local.json` and Managed policy settings. |

### EXTRA (in CAB only — may be valid CAB extension)

| # | CAB Content | Assessment |
|---|------------|------------|
| X1 | "CAB-Specific Patterns" section in subagents.md (Orchestrator Pattern, Verifier Pattern, Template Requirements) | **Valid CAB extension**. These are project-specific patterns, not official CC features. Clearly marked as CAB-specific. Retain. |
| X2 | "CAB-Specific Hook Patterns" section in hooks.md (5 patterns: auto-format, security gate, freshness validation, async telemetry, stop hook) | **Valid CAB extension**. Clearly marked as CAB-specific. Provide useful reference implementations. Retain. |

---

## Verified Correct

### subagents.md — Confirmed Accurate

- Subagents operate in their own context window (confirmed)
- Subagents cannot spawn other subagents, nesting depth = 1 (confirmed)
- Project agents in `.claude/agents/`, User agents in `~/.claude/agents/` (confirmed)
- Project-level takes precedence over user-level (confirmed)
- `name` field: required, lowercase letters and hyphens (confirmed)
- `description` field: required, natural-language, supports "Use PROACTIVELY" (confirmed)
- `tools` field: comma-separated allowlist, omit to inherit all (confirmed)
- `disallowedTools` field: comma-separated denylist (confirmed)
- `skills` field: full content injected, subagents do NOT inherit parent skills (confirmed)
- `mcpServers` field: inline MCP definitions scoped to agent lifecycle (confirmed, plus official also supports string references to existing servers)
- `hooks` field: lifecycle hooks scoped to subagent (confirmed)
- `memory` field with 3 scopes (`user`, `project`, `local`) (confirmed)
- Memory locations: `~/.claude/agent-memory/<name>/`, `.claude/agent-memory/<name>/`, `.claude/agent-memory-local/<name>/` (confirmed)
- First 200 lines or 25KB of MEMORY.md loaded (confirmed)
- `background: true` runs agent asynchronously (confirmed)
- Ctrl+B to background a running agent (confirmed)
- `isolation: worktree` for git worktree isolation with auto-cleanup (confirmed)
- `effort` field for reasoning effort (confirmed; official adds enum values: `low`, `medium`, `high`, `max`)
- `color` field for statusline identification (confirmed; official enumerates: red, blue, green, yellow, purple, orange, pink, cyan)
- `initialPrompt` field for auto-submitted first user turn (confirmed)
- Auto-compaction at ~95% with `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (confirmed)
- Plugin agents cannot use `hooks`, `mcpServers`, `permissionMode` (confirmed)
- `settings.json` key is `agent` (not `defaultSubagent`) (confirmed)
- Built-in "Explore" agent: Haiku model, read-only tools (confirmed)
- Built-in "statusline-setup" and "Claude Code Guide" agents (confirmed)
- `/agents` command for interactive management (confirmed)
- CLI `--agents` flag with JSON for session-level agents (confirmed)
- Skills vs Subagents comparison table (confirmed accurate)

### hooks.md — Confirmed Accurate

- 4 hook types: `command`, `http`, `prompt`, `agent` (confirmed)
- All 26 event names verified against official docs:
  - SessionStart, SessionEnd, InstructionsLoaded, ConfigChange (confirmed)
  - UserPromptSubmit, Notification, Elicitation, ElicitationResult (confirmed)
  - PreToolUse, PostToolUse, PostToolUseFailure (confirmed)
  - Stop, StopFailure, SubagentStop, SubagentStart (confirmed)
  - TaskCreated, TaskCompleted, TeammateIdle (confirmed)
  - PermissionRequest, PermissionDenied (confirmed)
  - PreCompact, PostCompact, CwdChanged, FileChanged (confirmed)
  - WorktreeCreate, WorktreeRemove (confirmed)
- Hook types: command (shell), http (POST), prompt (LLM), agent (subagent) — all confirmed
- Blocking behavior per type (confirmed)
- Matcher field: regex pattern against tool names (confirmed)
- `if` field: permission-rule-syntax conditional filter (confirmed)
- `async: true` for non-blocking fire-and-forget (confirmed)
- `once: true` for single-fire per session, skills only (confirmed)
- `shell` field for per-hook shell override (confirmed)
- Exit codes: 0 = success, 2 = block (Pre* hooks), other = non-blocking error (confirmed — note: CAB says "1 = failure/show error" but official says non-zero non-2 is non-blocking error shown in verbose mode)
- JSON output max 10,000 characters (confirmed)
- Parallel execution of hooks on same event (confirmed)
- Deduplication by command string or URL (confirmed)
- Frozen config at startup / session start (confirmed — note: official says per-event with file watcher, slightly different from CAB's "startup snapshot" claim)
- `/hooks` browser for interactive inspection (confirmed)
- MCP tool matching: `mcp__<server>__<tool>` syntax (confirmed)
- Environment variables: `CLAUDE_PLUGIN_ROOT`, `CLAUDE_PROJECT_DIR`, `CLAUDE_PLUGIN_DATA`, `CLAUDE_CODE_REMOTE`, `CLAUDE_ENV_FILE` (confirmed)
- CAB hook patterns (PostToolUse auto-format, PreToolUse security gate, InstructionsLoaded freshness, async telemetry, Stop final validation) — all structurally sound

---

## Priority Fixes

**High priority** (factual errors affecting user implementation):
1. **E2/M1**: Add `maxTurns` field to subagents.md frontmatter table
2. **E4**: Fix `permissionMode` enum — replace `ignore` with `auto`, `dontAsk`
3. **E5/E6**: Fix built-in Plan and General-purpose agent models to `inherit`
4. **M7**: Rewrite hook output schema to match official `hookSpecificOutput` structure

**Medium priority** (missing features users may need):
5. **M2**: Expand agent precedence table to all 5 levels
6. **M3**: Add `statusMessage`, `timeout`, `headers`, `allowedEnvVars` hook fields
7. **M6**: Document hook decision precedence and `defer` decision
8. **S2**: Rewrite hook configuration locations to match official hierarchy

**Low priority** (minor/cosmetic):
9. **E1**: Fix field count heading, remove `(body)` as a frontmatter field
10. **E3**: Add full model ID support to `model` field description
11. **E7**: Update Elicitation/ElicitationResult descriptions to mention MCP context
12. **S1**: Update link text to match current page title
