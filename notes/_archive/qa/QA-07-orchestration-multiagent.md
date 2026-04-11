# QA-07: Orchestration + Multi-Agent Patterns -- Delta Report

**Date**: 2026-04-05
**CAB files**:
1. `knowledge/operational-patterns/orchestration/framework.md`
2. `knowledge/operational-patterns/multi-agent/collaboration-patterns.md`
3. `knowledge/operational-patterns/multi-agent/worktree-workflows.md`
4. `knowledge/operational-patterns/multi-agent/agent-teams.md`

**Official sources**:
- https://code.claude.com/docs/en/sub-agents -- Subagent system, delegation, frontmatter, scopes, tools
- https://code.claude.com/docs/en/agent-teams -- Agent Teams (experimental), IPC, display modes, limitations
- https://code.claude.com/docs/en/common-workflows -- Worktree workflows, plan mode, parallel sessions
- https://code.claude.com/docs/en/interactive-mode -- Plan mode keyboard shortcuts, task list, permission modes
- https://code.claude.com/docs/en/settings -- Available settings (`agent`, `effortLevel`, `teammateMode`, etc.)
- https://code.claude.com/docs/en/model-config -- Effort levels, model aliases, `CLAUDE_CODE_SUBAGENT_MODEL`

---

## Summary

**55 items checked across 4 files, 14 discrepancies found** (5 ERROR, 4 MISSING, 3 STALE, 2 EXTRA requiring clarification).

---

## Discrepancies

### ERROR (factually wrong in CAB)

| # | CAB Claim | Official Reality | File | Location | Fix |
|---|-----------|-----------------|------|----------|-----|
| E1 | `framework.md` line 63: `"agent": "orchestrator"` in `~/.claude/settings.json` establishes global orchestrator default | The `agent` setting takes a **subagent name** (e.g., `"code-reviewer"`), not a role keyword like `"orchestrator"`. It makes the main thread run as that named subagent definition from `agents/*.md`. There is no built-in `"orchestrator"` agent type. | `framework.md` | Tenet 6, line 63 | Rewrite to: The `agent` setting in `settings.json` runs the main thread as a named subagent definition. CAB recommends creating an `orchestrator.md` agent definition and setting `"agent": "orchestrator"` to establish this pattern. Clarify this is a CAB convention, not a CC built-in. |
| E2 | `framework.md` line 161: "Enter plan mode (Shift+Tab twice)" | Shift+Tab **cycles** through permission modes: `default` -> `acceptEdits` -> `plan` (and any other enabled modes like `auto`). It is not always "twice" -- it depends on your current mode and which modes are enabled. From `default`, one press goes to `acceptEdits`, second to `plan`. But if `auto` mode is enabled, the cycle includes `auto` as well. | `framework.md` | Step 1: PLAN, line 161 | Change to: "Enter plan mode (cycle with Shift+Tab until plan mode indicator `pause plan mode on` appears)" or "Switch to plan mode using Shift+Tab to cycle permission modes." |
| E3 | `worktree-workflows.md` line 39: "Worktrees live in `.claude/worktrees/<name>/`" | Official docs confirm this is correct for the directory location, **but** the branch naming convention is `worktree-<name>`, not mentioned in CAB. Also, worktrees branch from `origin/HEAD` (the default remote branch), which CAB does not document. | `worktree-workflows.md` | Setup section, line 39 | Add: worktrees branch from `origin/HEAD` (configurable via `git remote set-head`). Branch is named `worktree-<name>`. Also add: worktree cleanup behavior (auto-remove if no changes; prompt if changes exist). |
| E4 | `agent-teams.md` line 56: `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` as the setup method | Official docs show the **preferred** method is via `settings.json` under the `env` key: `{"env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"}}`. The env var export works but settings.json is the documented primary method. Also, CAB says "Requires CC v2.1.32+" which is correct but should reference the official note format. | `agent-teams.md` | Setup section, line 56 | Add the settings.json method as primary. Keep env var as alternative. |
| E5 | `agent-teams.md` lines 74-76: IPC location `~/.claude/work/ipc/`, polling interval 500ms, atomic file operations | Official docs describe teams/tasks stored at `~/.claude/teams/{team-name}/config.json` and `~/.claude/tasks/{team-name}/`. The docs describe **file locking** for task claiming, **mailbox** for messaging, and **automatic message delivery** (not polling). The specific `~/.claude/work/ipc/` path and 500ms polling interval are **not documented** and appear to be CAB's inference from observable behavior. | `agent-teams.md` | IPC Mechanism section, lines 69-76 | Rewrite IPC section to match official docs: teams stored at `~/.claude/teams/`, tasks at `~/.claude/tasks/`. Use "file locking" for task claiming. Use "mailbox" for messaging with "automatic message delivery" (official language). Mark specific polling interval and IPC path as "observed behavior, not officially documented." |

### MISSING (in official docs, absent from CAB)

| # | Official Feature | Source URL | Recommended Action |
|---|-----------------|------------|-------------------|
| M1 | **Subagent frontmatter fields**: `memory` (persistent cross-session learning with user/project/local scopes), `hooks` (lifecycle hooks in subagent frontmatter), `skills` (preload skill content), `mcpServers` (scope MCP servers), `color`, `initialPrompt`, `maxTurns`, `permissionMode`, `disallowedTools` -- comprehensive field set documented but not referenced in CAB orchestration files. | sub-agents | Add a reference table or link to official frontmatter fields from `framework.md` or create a dedicated KB card for subagent configuration. Several of these fields (memory, hooks, skills, mcpServers) are significant for orchestration patterns. |
| M2 | **Subagent resume capability**: Subagents can be resumed via `SendMessage` tool (requires Agent Teams enabled). Subagent transcripts persist independently and survive main conversation compaction. Stored at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`. | sub-agents | Add to `collaboration-patterns.md` or a dedicated subagent KB card. This is important for cross-session persistence patterns. |
| M3 | **Agent Teams hooks**: `TeammateIdle`, `TaskCreated`, `TaskCompleted` hook events for quality gates. These enable enforcement of rules when teammates finish work or tasks change state. | agent-teams | Add to `agent-teams.md` under a "Quality Gates" or "Hooks" section. These are significant for CAB's verification-first approach. |
| M4 | **Plan mode**: Can be set as `defaultMode` in settings (`"permissions": {"defaultMode": "plan"}`), can be invoked via `claude --permission-mode plan`, and has a `Ctrl+G` shortcut to open the plan in a text editor for direct editing. Also, accepting a plan auto-names the session. | common-workflows, interactive-mode | Add plan mode details to `framework.md` Step 1: PLAN section, or create a dedicated plan-mode KB card. The `Ctrl+G` editor shortcut and settings-based default are particularly useful. |

### STALE (outdated in CAB)

| # | CAB Content | Current Official | Fix |
|---|------------|-----------------|-----|
| S1 | `framework.md` line 210: "Single subagent nesting depth" as a CC platform constraint | Still correct that subagents cannot spawn other subagents. However, the official docs now provide explicit workarounds: (1) chain subagents from main conversation, (2) use Skills instead, (3) use `Agent(agent_type)` syntax in `tools` field to control which subagents an `--agent` main thread can spawn. The constraint framing should include these mitigations. | Update the constraint entry to include official mitigations. |
| S2 | `agent-teams.md` line 119-126: "Coordinator Mode (Feature-Gated)" section describes coordinator mode as "not yet generally available" and "feature-gated" | The official Agent Teams docs (as of the fetched content) do **not mention coordinator mode at all**. The term does not appear. CAB may be referencing early preview information that has been removed or not yet publicly documented. This section is speculative. | Either remove the Coordinator Mode section entirely, or clearly mark it as "CAB forward-looking speculation based on early signals -- not currently in official documentation" with confidence: C. |
| S3 | `collaboration-patterns.md` line 100: "~7x token cost per teammate" | Official docs say "Agent teams use significantly more tokens than a single session" and "token costs scale linearly" with teammate count, but do **not** provide a specific multiplier like "7x". The `~7x` figure appears to be CAB's estimate. | Change to: "Significantly higher token cost per teammate (token usage scales linearly with active teammates)" and note the 7x figure as a CAB estimate, not official. Or cite source if there's a specific reference. |

### EXTRA (in CAB only -- may be valid CAB extension)

| # | CAB Content | Assessment |
|---|------------|------------|
| X1 | **Five Canonical Agentic Workflow Patterns** (Prompt Chaining, Routing, Parallelization, Orchestrator-Workers, Evaluator-Optimizer) in `framework.md` | These are **CAB-invented patterns**, not CC-native features. They are valid architectural patterns for agentic systems mapped to CC primitives. The CC implementation notes are reasonable. **Assessment: Valid CAB extension.** Ensure the doc clearly labels these as "CAB's operational patterns built on CC primitives" (which it does in the header note). No change needed. |
| X2 | **A-Team Product Design Cycle alignment** in `agent-teams.md` (Product Manager, Software Architect, UX Designer, Developer, QA/Verifier roles) | This is a **CAB-invented framework** mapping Agent Teams to product development roles. Not referenced in any CC docs. **Assessment: Valid CAB extension** -- useful conceptual mapping. Clearly labeled as CAB content. No change needed. |

---

## Verified Correct

### framework.md
- Tenet 1 (Simplicity-First Complexity Ladder): Levels 0-5 correctly represent increasing CC complexity from single prompt through Agent Teams
- Tenet 2 (Verification as Architectural Requirement): Sound architectural principle, CC-compatible
- Tenet 4 (Compounding Knowledge via CLAUDE.md): Accurately reflects CC's CLAUDE.md usage
- Tenet 5 (Token Efficiency): Accurately reflects CC context window management
- Standard Task Execution Protocol (PLAN -> REVIEW -> EXECUTE -> VERIFY -> COMMIT): Sound workflow, plan mode and auto-accept correctly referenced as CC features
- Agent Failure Mode Catalog: Practical failure modes with reasonable mitigations
- CC Platform Constraints table: Mostly accurate (single nesting depth, no native database, context window finite confirmed)

### collaboration-patterns.md
- Pattern 1 (Parallel via Git Worktrees): Correctly identified as daily driver for parallel work, matches official recommendation
- Pattern 2 (Sequential Subagent Chain): Accurately describes subagent chaining pattern
- Pattern 3 (Main Agent + Specialists): Correctly describes delegation via Agent tool
- Pattern 4 (Agent Teams): Correctly identified as experimental, requiring feature flag
- 3-5 worktrees/teammates sweet spot: Confirmed by official docs ("Start with 3-5 teammates")
- 5-6 tasks per teammate: Confirmed by official docs
- "use subagents" / "use N subagents" prompt pattern: Confirmed as valid CC usage pattern
- Cross-session persistence approaches (notes/, progress file, project-state.yaml): Valid CAB patterns
- Git as coordination layer: Sound architectural principle

### worktree-workflows.md
- `claude --worktree feature-auth` / `claude -w feature-auth` / `claude --worktree` (auto-generate): All confirmed correct
- `.worktreeinclude` file behavior (copy gitignored files into worktrees): Confirmed correct, uses `.gitignore` syntax
- Resource sharing table (git repo shared, context window independent, etc.): Confirmed correct
- Feature + Review and Parallel Analysis workflow patterns: Sound patterns
- Cleanup commands (`git worktree remove`, `git worktree prune`): Correct git commands
- Best practices (name consistently, 3-5 worktrees, color-code terminals): Confirmed by official best practices

### agent-teams.md
- Architecture diagram (Team lead + Teammates + Shared task list + Mailbox): Matches official architecture
- Team lead coordinates, assigns tasks, approves/rejects plans: Confirmed correct
- Teammates work independently in separate context windows: Confirmed correct
- Shared task list with pending/in-progress/completed states: Confirmed correct
- Display modes (in-process via Shift+Down, split panes via tmux/iTerm2): Confirmed correct
- Requires CC v2.1.32+: Confirmed correct
- No session resumption limitation: Confirmed (official: "/resume and /rewind do not restore in-process teammates")
- No nested teams: Confirmed correct
- Lead is fixed: Confirmed correct
- 3-5 teammates recommended: Confirmed correct
- 5-6 tasks per teammate sweet spot: Confirmed correct
- Subagent definitions usable for teammates (tools + model honored, skills/mcpServers not applied): Confirmed correct
- When to Use Agent Teams vs. Alternatives table: Recommendations align with official guidance

---

## Priority Fixes

1. **E1** (Critical): Fix `"agent": "orchestrator"` claim -- misleading about CC capabilities
2. **E5** (High): Rewrite IPC section to use official terminology and paths
3. **S2** (High): Remove or clearly mark Coordinator Mode section as speculative
4. **S3** (Medium): Remove specific "7x" multiplier claim or mark as estimate
5. **M1-M4** (Medium): Add missing official features to appropriate KB cards
6. **E2-E4** (Low): Minor accuracy fixes for plan mode and setup instructions
