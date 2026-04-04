# Lessons Learned — CAB Operations Log

Cross-session lesson persistence. Feeds the planned changelog/compile & eval protocol.

**Categories**: `ops` (operational) | `arch` (architectural) | `ctx` (context-engineering) | `proc` (process) | `tool` (tooling)
**Status**: `active` | `integrated` | `superseded`

---

## Active

| ID | Date | Cat | Lesson | Detail |
|----|------|-----|--------|--------|
| LL-01 | 2026-04-03 | ops | Explore agents sandboxed to current project dir | Use general-purpose agents for cross-project reads |
| LL-02 | 2026-04-03 | ops | Background agents can't write files | All artifact-writing must be foreground. Background = read-only research only |
| LL-03 | 2026-04-03 | ctx | Post-compaction drops extension awareness | Re-read `notes/global-extensions-map.md` and restate objective after any /compact |
| LL-04 | 2026-04-03 | proc | Centralized state > scattered state | All audit/session state in `notes/` as SSOT. Scattered state = context loss across sessions |
| LL-05 | 2026-04-03 | ops | Worktree agents don't auto-commit | Orchestrator must manually handle commits when using worktree isolation |
| LL-06 | 2026-04-04 | ctx | Fan-out parallel agents for doc-heavy research | Main session retains synthesis authority; subagents handle context-heavy fetching (~370K tokens across 8 agents, zero main-context impact). "Fan-out → synthesize" pattern |
| LL-07 | 2026-04-04 | proc | Three-tier state hierarchy | (1) Implementation plan → (2) TODO.md (never delete, reorder pending to top) → (3) progress.md (live state, can compact). Only progress.md warrants deletions |
| LL-08 | 2026-04-04 | ops | Background agent outputs must persist as artifacts | Task notification output files on disk may be empty. Any substantive agent analysis must write to `notes/`. Don't rely on temp output files |

## Integrated / Superseded

| ID | Date | Cat | Lesson | Resolution |
|----|------|-----|--------|------------|
| *(none yet)* | | | | |

---

## Pending

User has additional lessons-learned to add after full audit is complete.
