# Current Task: Wave 8 Phase 2 (KB → KG Graph Schema Design) — AWAIT USER COMMENTS

**Status**: Session 38 closed cleanly 2026-04-28. User has signaled they will provide comments before Wave 8 Phase 2 kicks off. Do NOT auto-proceed on cold start — wait for user input first.
**Last active**: 2026-04-28 (Session 38 closed)
**Branch**: `master` (clean; all Session 38 commits pushed)
**Active plan**: [notes/impl-plan-kb-to-kg-2026-04-24.md](impl-plan-kb-to-kg-2026-04-24.md)

---

## User-side actions still pending (apply at your convenience)

### Settings.json finalization

**Apply diff** (confirmed approved):

Remove from `permissions.allow` (9 lines):
```diff
-    "Skill(commit-push-pr)",
-    "Skill(commit-push-pr:*)",
-    "Skill(cab:techdebt)",
-    "Skill(cab:techdebt:*)",
-    "Skill(execute-task)",
-    "Skill(execute-task:*)",
-    "mcp__claude_ai_Context7__resolve-library-id",
-    "mcp__claude_ai_Context7__query-docs",
-    "WebSearch",
```

Remove from `allowedTools` (2 lines):
```diff
-    "mcp__filesystem_read_file": "auto_approve",
-    "mcp__filesystem_list_directory": "auto_approve"
```

Fix or remove `additionalDirectories: ["\\tmp"]` per actual intent.

Remove from `environmentVariables` (you confirmed):
```diff
-    "RUST_LOG": "info"
```

**Defer decision**: `CLAUDE_CODE_DISABLE_TELEMETRY`. CC's native OpenTelemetry support (https://code.claude.com/docs/en/monitoring-usage) could provide token-tracking metrics that eliminate the need for CAB to build custom utility scripts (e.g., `bootstrap-cost.sh`). Aligns with DP8 wrap-and-extend. Recommend evaluating before re-adding the disable flag.

### Hooks recommendation (per your ask)

**KEEP both hooks** — both are real, functional, and complementary to sandbox:

- `bash-security-gate.sh` (PreToolUse on Bash): provides a deterministic command allowlist gate. The CC sandbox provides container-level isolation (filesystem, network); the security gate provides command-pattern denial (e.g., catches `rm -rf` patterns the sandbox might still permit inside its allowed paths). Defense in depth — they complement, don't duplicate.
- `ruff format` (PostToolUse on Write|Edit): silently no-ops on non-Python files (`2>/dev/null || true`). Useful for Python work; zero overhead for non-Python. You have `Bash(ruff check:*)` in allow → you do use ruff → keep.

---

## Wave 8 Phase 2 (next session, after your comments)

### Scope

Graph schema design — node types + edge types + serialization + documentation. Per Phase 1 findings:

1. **Multi-type node taxonomy**: `kb-card`, `skill`, `agent`, `command`, `notes-artifact`, `lesson`
2. **Edge type taxonomy**: `depends_on`, `related` (existing) + `governs`, `embodies`, `references` (new)
3. **Serialization decision**: JSON-LD (W3C standard) vs custom JSON
4. **Schema documentation**: extend `knowledge/components/knowledge-base-structure.md`

### Deferred to Wave 8 Phase 2 (or appropriate future wave)

- **KB authoring rule** (codify the lesson from Session 38 cont.²): KB artifacts must be temporally neutral — no "added on date X", "Sessions Y-Z violated", "UXL-NNN tracks" content. KB cross-references LL entries by ID (LLs are stable reference) but doesn't restate their session-specific content. Candidate addition to `.claude/rules/kb-conventions.md`.
- **OpenTelemetry-as-state-mgmt-tooling consideration** — alternative to CAB-built token-tracking utilities (DP8 wrap pattern).

### Wave order reminder

Wave 5 ✓ → Wave 8 (in progress) → Wave 4 (hooks; dual-POV gated)

---

## Session 38 Closure

Full arc summary in `notes/progress.md` Session 38 + cont./cont.²/cont.³ entries. New artifacts: LL-30 (DP8 enforcement gap), UXL-041 (DP8 wrap refactor candidates). Modified: scaffold-project Step 0, audit-workspace Dim 8, design-principles.md DP8.

## Reference

- Wave plan: `notes/ux-log-wave-plan-2026-04-22.md`
- Active plans: 2 (UXL-002 Phase 3d gated; UXL-005 Phase 2 next)
- Tracker: `notes/ux-log-001-2026-04-22-pass-1.csv`
- Plugin-dev (DP8 wrap target): `~/.claude/plugins/cache/claude-plugins-official/plugin-dev/`
- Phase D HydroCast: still PR #8 blocked

<!-- T1:BOUNDARY — current-task.md is entirely T1 (<100L hard cap). -->
