# Current Task: Wave 8 Phase 2 — KB → KG Graph Schema Design

**Status**: Wave 3 + 5.1 + 7 + 8.1 LANDED. Wave 8 Phases 2-5 multi-session ahead.
**Last active**: 2026-04-24 (Session 37 cont.⁵)
**Branch**: `master`
**Active plan**: [notes/impl-plan-kb-to-kg-2026-04-24.md](impl-plan-kb-to-kg-2026-04-24.md)

---

## Next Session Pickup — Wave 8 Phase 2

### Scope

Graph schema design — node types + edge types + serialization + documentation. Per Phase 1 findings, focus on:

1. **Multi-type node taxonomy**:
   - `kb-card` (existing 44 KB files; uses `id:` field)
   - `skill` (16 skills; uses `name:` field as ID)
   - `agent` (3 agents; uses `name:` field)
   - `command` (15 commands; uses filename stem as ID)
   - `notes-artifact` (impl-plans, lessons-learned, etc.)
   - `lesson` (LL-NN entries within lessons-learned.md — node per LL, not per file)

2. **Edge type taxonomy** (existing + new):
   - `depends_on` (KB → KB; conceptual prerequisite)
   - `related` (any → any; lateral association)
   - **`governs`** (lesson → skill/agent/command/rule; structural enforcement) — NEW
   - **`embodies`** (skill/agent/command → lesson; reverse of governs) — NEW
   - **`references`** (notes-artifact → kb-card or notes-artifact → skill; mention without semantic dependency) — NEW

3. **Serialization decision**: JSON-LD (W3C standard, semantic-web compatible) vs custom JSON (pragmatic, simpler tooling). Recommendation pending — JSON-LD preferred IF graph extends to public consumption; custom JSON if CAB-internal only.

4. **Schema documentation** target: extend `knowledge/components/knowledge-base-structure.md` with new "Multi-Type Node Schema" section (current card focuses on KB structure; this expands to whole-platform graph).

### Phase 1 finding driving Phase 2

8 dangling cross-references from `knowledge/reference/` files pointed at skill names (`plan-implementation`, `execute-task`) — confirming KB cards already cross-reference skills as if they were nodes. The schema MUST accommodate this; otherwise Phase 3 extractor would emit broken edges or require manual edge-resolution.

### Phases 3-5 preview (after Phase 2)

- **Phase 3**: build `hooks/scripts/kb-graph-extract.py`; emit `knowledge/_graph/index.json`
- **Phase 4**: notes/ ↔ knowledge/ linking convention; possibly extend `index-kb` skill
- **Phase 5**: Mermaid CLI renderer (minimum); interactive HTML (stretch)

### Wave order reminder (per user advised)

Wave 5 ✓ → Wave 8 (in progress) → Wave 4 (hooks; dual-POV gated)

---

## Session 37 Closure (full arc — 6 sub-sessions)

- **Commits this session arc** (chronological):
  - `0a7bcd8` 3b.1 (skill renames + cross-ref sweep)
  - `5301325` 3b.2 (wrapper trims)
  - `b251b09` 3b state refresh
  - `7b23830` 3c.1+3c.3 (orphan promotions + F011 wiring)
  - `bcdae78` 3c state refresh
  - `6653a25` 3c.2 (hybrid merges into scaffold-project --mode router)
  - `311d6e3` 3c.2 state refresh
  - `6fd700a` notes README + 2 historical archives
  - `d1dfde3` test-pass remediation
  - `3ee74fc` Wave 7 architecture decisions
  - `d524700` Wave 7 state refresh
  - `0a35bbc` Wave 5.1 recover-session skill
  - `cb6ee77` Wave 5.1 state refresh
  - `b88236a` Wave 8 plan + Phase 1 audit
  - (this commit) Wave 8 state refresh
- **Pushed through `cb6ee77`**; Wave 8 commits (`b88236a` + this state refresh) pending push
- **Verifier PASS**: 5 independent runs (3b, 3c.1+3c.3, 3c.2, Wave 7, Wave 5.1) — all criteria met
- **Skill count**: 16 (recover-session added in Wave 5.1)
- **Active plans**: 2 (UXL-002 Phase 3d gated; UXL-005 Phase 2 next)

---

## Pre-2026-04-22 Queued Work (unchanged)

- **Phase D — HydroCast ↔ CAB State-Management Comparison** — HARD-BLOCKED on PR #8

---

## Reference Artifacts

- **Wave plan**: `notes/ux-log-wave-plan-2026-04-22.md`
- **Active plans**: 2 impl-plan-* files (UXL-002, UXL-005)
- **Tracker**: `notes/ux-log-001-2026-04-22-pass-1.csv`
- **Audit tool**: `hooks/scripts/kb-audit.py` (re-runnable)
- **Auto-memory**: `memory/feedback_dual_pov_check.md` (Wave 4 hook gate)

<!-- T1:BOUNDARY — current-task.md is entirely T1 (<100L hard cap). -->
