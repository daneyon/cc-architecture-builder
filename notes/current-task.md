# Current Task: User-side settings finalization → then Wave 8 Phase 2

**Status**: Session 38 cont. settings audit presented + structural DP8 enforcement layer LANDED (LL-30 + scaffold-project Step 0 + audit-workspace Dim 8 + design-principles DP8 extension). User must finalize settings.json + clarify shelved-hooks reference before Wave 8 Phase 2.
**Last active**: 2026-04-28 (Session 38 cont.)
**Branch**: `master` (Session 38 cont. commits pending push at session close)
**Active plan**: [notes/impl-plan-kb-to-kg-2026-04-24.md](impl-plan-kb-to-kg-2026-04-24.md)

---

## User-side actions required (do BEFORE Wave 8 Phase 2)

### 1. Verify CAB plugin auto-update now works

```bash
/plugin update cab@cab
# OR restart CC entirely
```

**Expected**: cache at `~/.claude/plugins/cache/cab/cab/` will move from `1.1.0/` semver dir to a new commit-hash dir (e.g., `0880cea/` or whatever the latest pushed commit short-hash is). The new dir should contain ALL 16 current skills with renamed verb+object pattern (analyze-architecture, audit-workspace, check-sync, close-session, commit-push-pr, create-components, execute-task, index-kb, plan-implementation, pre-push-state-review, quick-scaffold, recover-session, scaffold-project, scan-techdebt, sync-context, validate-structure).

**If verification fails**: revert via `git revert 0880cea` (rollback the schema change) and investigate further.

### 2. (Recommended) Remove orchestrator global-default from ~/.claude/settings.json

Per Wave 7 UXL-003 decision (already executed at project + project-root layers in Session 38):

```json
// Remove this line from ~/.claude/settings.json:
"agent": "orchestrator",
```

Net effect across all 3 layers: orchestrator subagent no longer auto-binds as session default; CLAUDE.md persona drives main session; subagent invokable explicitly when cross-domain delegation needed.

---

## Next Session Pickup — Wave 8 Phase 2 (after verification)

### Scope

Graph schema design — node types + edge types + serialization + documentation. Per Phase 1 findings:

1. **Multi-type node taxonomy**: `kb-card`, `skill`, `agent`, `command`, `notes-artifact`, `lesson`
2. **Edge type taxonomy**: `depends_on`, `related` (existing) + `governs`, `embodies`, `references` (new)
3. **Serialization decision**: JSON-LD (W3C standard) vs custom JSON (pragmatic)
4. **Schema documentation**: extend `knowledge/components/knowledge-base-structure.md`

### Phase 1 finding driving Phase 2

8 dangling cross-references from `knowledge/reference/` files pointed at SKILL names (`plan-implementation`, `execute-task`) — confirming KB cards already cross-reference skills as if they were nodes. Schema MUST accommodate multi-type nodes.

### Wave order reminder

Wave 5 ✓ → Wave 8 (in progress) → Wave 4 (hooks; dual-POV gated)

---

## Session 38 Closure

- **Commits this session**: `0880cea` work (5 files, 8+/10-) + this state refresh (next commit)
- **Pending push**: 2 commits (Session 38 work + state refresh)
- **Verifier**: NOT invoked (structural-only fix; verification = user runs `/plugin update`)
- **UXL log**: UXL-041 logged for DP8 wrap-and-extend refactor opportunity (deferred wave)
- **Skill count**: 16 (unchanged in Session 38)

---

## Pre-2026-04-22 Queued Work (unchanged)

- **Phase D — HydroCast ↔ CAB State-Management Comparison** — HARD-BLOCKED on PR #8

---

## Reference Artifacts

- **Wave plan**: `notes/ux-log-wave-plan-2026-04-22.md`
- **Tracker**: `notes/ux-log-001-2026-04-22-pass-1.csv` (UXL-041 added; UXL-017/006/003/023 resolved)
- **Active plans**: 2 impl-plan-* files (UXL-002, UXL-005)
- **Auto-memory**: `memory/feedback_dual_pov_check.md`
- **Plugin-dev cache (DP8 wrap target)**: `~/.claude/plugins/cache/claude-plugins-official/plugin-dev/<commit-hash>/`

<!-- T1:BOUNDARY — current-task.md is entirely T1 (<100L hard cap). -->
