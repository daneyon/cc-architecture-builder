# Current Task: Wave 8 — KB → Knowledge-Graph Foundation (UXL-005)

**Status**: Wave 3 + Wave 7 + Wave 5.1 LANDED. Wave 8 next per user advised order (Wave 5 → Wave 8 → Wave 4).
**Last active**: 2026-04-24 (Session 37 cont.⁴)
**Branch**: `master`
**Wave plan**: [notes/ux-log-wave-plan-2026-04-22.md](ux-log-wave-plan-2026-04-22.md)

---

## Next Session Pickup — Wave 8

### Scope (UXL-005)

KB → Knowledge-Graph standardization. Foundational architectural work. H/H effort. Unblocks UXL-004 (CAB advisor ↔ project-orchestrator agentic bridge), UXL-009 (HydroCast KB-plan pattern extraction), UXL-010 (AgentContextGraphVisualizer feasibility).

**User end-vision context** (cited multiple times across Session 37):
- "KB modularizes into programmatic knowledge graph for each domain specialized skillsets"
- "ultimately have all existing KB packs into domain specialized skillsets"
- "downstreaming wrapping design philosophy to compose the static KB assistance into readily agentic, actionable assistance"

The Phase 3c.2 `scaffold-project` router pattern (router + assets/ + Knowledge Anchors links to KB) is the **seed** for Wave 8's broader pattern.

### Pre-EXECUTE: heavy plan needed

Per F011: H/H effort + 3+ phases + plan body would exceed 80L → **execute-task DELEGATES to plan-implementation**. This wave warrants a real SOW + Implementation Plan artifact, not inline plan.

Suggested plan structure (for plan-implementation to author):
1. **Phase 1 — Audit existing KB metadata** (frontmatter coverage, depends_on/related edges, source citations)
2. **Phase 2 — Design graph schema** (node types, edge types, query patterns; learn from HydroCast's notes↔knowledge linkage if PR #8 has merged)
3. **Phase 3 — Build extractor/indexer** (parse frontmatter → emit graph; tooling: Python/jq/MCP server?)
4. **Phase 4 — Visualization surface** (renderer; format: Mermaid? interactive HTML? CLI table?)
5. **Phase 5 — Migration plan for existing KB** (which cards repack into which skill folders per Phase 3c.2 pattern)

### Pre-req consideration

Per wave plan: "Wave 6 completion preferable (UXL-025 + UXL-034 = stable state-mgmt foundation before adding KG on top)." UXL-025 is queued behind HydroCast Phase D (PR #8). UXL-034 has not started.

**Decision needed at Wave 8 PLAN gate**: proceed despite Wave 6 not being complete, OR acknowledge dependency and defer? Given the user's end-vision urgency, recommendation is to proceed — Wave 6 work can run in parallel via worktree if resources allow.

### Wave 4 (Hook Enforcers) — still gated on dual-POV check

Deferred to after Wave 8 per user's advised order.

### Wave 5.2 (UXL-016 event-triggered state-write) — parked

Waits for `recover-session` skill (UXL-017) to survive at least one real dying-session recovery use.

---

## Session 37 Closure (full arc — 5 sub-sessions)

- **Commits this session arc** (chronological):
  - `0a7bcd8` 3b.1 (skill renames + cross-ref sweep)
  - `5301325` 3b.2 (wrapper trims)
  - `b251b09` 3b state refresh
  - `7b23830` 3c.1+3c.3 (orphan promotions + F011 wiring)
  - `bcdae78` 3c state refresh
  - `6653a25` 3c.2 (hybrid merges into scaffold-project --mode router)
  - `311d6e3` 3c.2 state refresh
  - `6fd700a` notes README + 2 historical archives
  - `d1dfde3` test-pass remediation (marketplace-json template + scan-techdebt md filter)
  - `3ee74fc` Wave 7 architecture decisions (UXL-003/006/023)
  - `d524700` Wave 7 state refresh
  - `0a35bbc` Wave 5.1 recover-session skill (UXL-017)
  - (this commit) Wave 5.1 state refresh
- **Pushed through `d524700`**; `0a35bbc` + this state refresh pending push
- **Verifier PASS**: 5 independent runs across 3b, 3c.1+3c.3, 3c.2, Wave 7, Wave 5.1 — all criteria met every time
- **Skill count**: 16 (10 prior + 5 orphan promotions + 1 recover-session; quick-scaffold retained as alias)

---

## Pre-2026-04-22 Queued Work (unchanged)

- **Phase D — HydroCast ↔ CAB State-Management Comparison** — HARD-BLOCKED on HydroCast PR #8 merge

---

## Reference Artifacts

- **Wave plan**: `notes/ux-log-wave-plan-2026-04-22.md`
- **Tracker**: `notes/ux-log-001-2026-04-22-pass-1.csv` (UXL-017 now resolved)
- **Auto-memory**: `memory/feedback_dual_pov_check.md` (governing for Wave 4 hook work)

<!-- T1:BOUNDARY — current-task.md is entirely T1 (<100L hard cap). -->
