# Implementation Plan: CAB UX Log + Ideabox Tracker

**Project Name**: CAB-Generalized UI/UX Test Log & Ideabox Tracker
**Version**: 1.0
**Date**: 2026-04-22
**Related SOW**: embedded below (Section 0)
**Technical Lead**: orchestrator (CAB main session)
**Project Owner**: user (daneyon)
**Planning Mode**: full-detail (per user SME-verification directive)

---

## 0. Statement of Work (Embedded)

### 0.1 Problem Statement

After multi-project CAB adoption, UX friction, ideation, and deferred work accumulate in three leaky buckets: (a) session transcripts (ephemeral — lost to compaction), (b) `notes/TODO.md` backlog (grows un-triaged; low items rot at bottom), (c) oral dialogue state (LL-28: dialogue-level discoveries never persist). No single durable surface exists for centralizing findings across GUI, CLI, agentic, integration, and meta surfaces. Existing HydroCast `notes/gui-review-comments/` solves the GUI-review slice but does not generalize across the full agentic-OS-platform surface.

**Quantified pain**:
- User's ~7 architectural observations from one session risk transcript-compaction loss without this artifact
- 18+ deferred/incomplete items in `notes/TODO.md` (below T1 boundary line 48) have sat untriaged across multiple sessions
- HydroCast audit workstream (Session 33 data point) sat ~4 weeks in parallel branch drift before close — a LL-28 case

### 0.2 Proposed Solution

A flat-notes CSV tracker (`notes/ux-log-*.csv`) + companion guide (`notes/ux-log-guide.md`) + two new KB cards (`knowledge/reference/prioritization-frameworks.md`, `knowledge/reference/ux-testing-agentic-os.md`) that:

- Accepts entries across five surfaces (`gui`/`cli`/`agentic`/`integration`/`meta`) with surface-conditional framework anchors
- Preserves user raw comments full-fidelity in `user_comment` column; orchestrator synthesis in `orchestrator_take`
- Anchors every entry to ISO 9241-210 lifecycle stage + a surface-appropriate heuristic/principle
- Routes resolved entries to `LL` / `KB` / `rule` / `skill` / `hook` / `TODO` / `progress` / `followup` via `downstream_target`
- Enforces `/cab:planning-implementation` → `/cab:execute-task` as the ONLY path to execution (no direct row-to-commit). `planning` status between `triaged` and `in-progress` makes this machine-enforceable.
- Programmatically links to plan files (`linked_plan`) and commits (`linked_commit`) for deterministic state-mgmt traceability
- Jira/Linear-portable schema for optional future export

### 0.3 Key Features & Strategic Value

- **Upstream LL pipeline**: LLs no longer appear ex-nihilo; candidate pool is the triaged `idea`/`drift`/`gap` entries
- **TODO.md relief**: below-T1 deferred items migrate to tracker, reducing TODO.md to active work only
- **Agentic-OS generalization**: covers CC-native surfaces (CLI/agentic/integration/meta) that traditional PM trackers ignore
- **Distributable template**: Phase 6 extracts generic template for CAB-consuming projects (HydroCast, RAS-exec, future)

### 0.4 Challenges & Mitigations

| Challenge | Mitigation |
|---|---|
| Flat-notes policy (LL-25) vs HydroCast's subfolder precedent | Use flat `notes/` with `ux-log-*` prefix; no subfolders. Pass files become `ux-log-NNN-YYYY-MM-DD-pass-N.csv` at root. |
| 25-column schema complexity → log fatigue | Tiered column population (log/triage/promotion). Only 10 columns required at log time; rest are triage-filled. |
| Cross-surface taxonomy completeness | Validate in Phase 1 research against 2025-2026 industry practice. `meta` catch-all absorbs unclassifiable. |
| State-linkage via convention drifts over time | Deterministic hook enforcement (Phase 5 spec) — not reliance on manual column population |
| Raw comment preservation vs paraphrase drift | Hard rule in Phase 3: `user_comment` is verbatim-only. `orchestrator_take` column exists precisely so my synthesis never touches `user_comment`. |

### 0.5 Timeline

6 phases, estimated 2 sessions for Phases 1-4 (research + scaffolding + initial pop + triage); Phase 5 (per-row execution protocol doc) in same bundle; Phase 6 (distributable template extraction) deferred to post-dogfood validation.

### 0.6 KPIs

| Category | Metric | Target |
|---|---|---|
| Coverage | Initial pass row count | ≥25 rows (7 user items + ≥18 deferred TODOs) |
| Schema discipline | Rows with complete log-time fields | 100% |
| State linkage | Resolved rows with populated `linked_plan` + `linked_commit` | 100% |
| Flat-notes compliance | Subdirectories created under `notes/` | 0 (except `_archive/`) |
| KB compliance | New `knowledge/reference/*.md` files passing `/validate --cab-audit` | 2/2 |
| Dogfood | Tracker self-row created for `workflow-processflow.md` UTF-16 bug | 1 |

---

## 1. Project Overview

### 1.1 Scope Boundaries

**In scope**:
- CSV template + guide + examples for the CAB tracker
- Two new KB cards in `knowledge/reference/`
- Relocation of 3 orphan files from `skills/planning-implementation/references/` → `knowledge/reference/` (per established folder purpose)
- Initial pass population (user's 7 items + deferred TODO absorption)
- Orchestrator triage of initial pass
- Documented state-linkage protocol (hook spec — implementation in a separate tracker row)
- Extraction of distributable template (Phase 6) — spec only, execution after dogfood

**Out of scope** (deferred to separate tracker rows, not this plan):
- Memory-policy resolution (`~/.claude/projects/.../memory/` vs `notes/`)
- CAB advisor ↔ project-orchestrator bridge architecture
- Workflow-mapper skill/subagent creation
- KB → knowledge-graph architecture
- CAB `orchestrator` subagent deprecation as global default
- Command→skill migration audit (item #2 from user brief)
- Plugin-vs-project default setup fix (item #1 from user brief)
- **HydroCast `kb-standardization-plan.md` pattern extraction** for CAB KG bridge (user directive 2026-04-22; path: `Flood-Forecasting/knowledge/reference/kb-standardization-plan.md`; logged as UXL row in Phase 3)
- **AgentContextGraphVisualizer feasibility review** (3rd-party repo: https://github.com/nicollorens12/AgentContextGraphVisualizer) — evaluate custom CAB-native version vs separate distinct repo; CLI/tool form, NOT VS Code extension (user directive 2026-04-22; logged as UXL row in Phase 3)

### 1.2 Stakeholder Map

| Stakeholder | Role | Interest | Communication |
|---|---|---|---|
| user (daneyon) | Decision maker + domain SME | Verifies plan comprehensiveness before execution; provides raw observations and SME context | Direct in-session review of plan artifact |
| orchestrator (main session) | Planning + triage + execution coordination | Owns tracker hygiene, triage synthesis, plan-to-task flow | This plan + subsequent session actions |
| Future CAB-consuming projects | Template adopters | Need distributable, copy-paste-adoptable template | Phase 6 deliverable |
| Future subagent (UX-log-capturer candidate) | NL→row mapper | Closed-vocabulary picklists enable agentic capture | Schema design must preserve picklist discipline |

### 1.3 Assumptions & Constraints

**Assumptions**:
- User's 7 items from the 2026-04-22 brain-dump turn are accurately captured in Appendix C of this plan. If any item text is paraphrased in Appendix C, verification before Phase 3 execution is required.
- CAB `notes/` directory is flat (LL-25); this plan does not propose carving a subfolder exception.
- CSV format is acceptable for tabular state (Jira/Linear-portable; human-editable in Excel; parseable programmatically). No argument for JSON/YAML/SQLite in v1.
- `knowledge/reference/` is the correct semantic home for universal utility assets (confirmed by existing INDEX.md semantics).

**Constraints**:
- kb-conventions: KB files ≤300 lines, `source:` frontmatter required, wrapper philosophy (link-and-extend, don't duplicate CC docs)
- component-standards: skill/agent frontmatter compliance on any new extensions
- notes flat policy: no subfolders
- Full raw-comment preservation: non-negotiable per user directive
- Plan must be SME-verifiable before execution (this section + Appendix B schema + Appendix A research are the verification surfaces)

---

## 2. Requirements

### 2.1 Functional Requirements

| ID | Feature | User Story | Acceptance Criteria | Priority |
|---|---|---|---|---|
| F001 | Flat CSV tracker with 25-column schema | As a CAB operator, I want to log any UX/ideation/friction observation in a single flat CSV so entries aren't lost to transcript compaction or TODO.md rot | Given Appendix B's schema, `notes/ux-log-template.csv` has exactly those 25 headers in specified order | Must |
| F002 | Companion guide ≤300 lines | As a reader (future self or adopter), I want the column semantics + workflow documented in one skim-able file | `notes/ux-log-guide.md` ≤300 lines, includes cheat sheets for all picklists, co-review workflow, triage workflow, promotion workflow | Must |
| F003 | Minimum 5-row examples file | As a new user, I want one illustrative row per surface to anchor expectations | `notes/ux-log-examples.csv` has ≥1 row per surface value (5 surfaces × ≥1 = 5 rows minimum) | Must |
| F004 | Prioritization frameworks KB card | As a triage-time reviewer, I want a single canonical reference for RICE/MoSCoW/Kano/Value-Effort decisions | `knowledge/reference/prioritization-frameworks.md` passes `/validate --cab-audit`, ≤300 lines, frontmatter-compliant, covers tiered application (log/triage/promotion) | Must |
| F005 | UX-testing-for-agentic-OS KB card | As an adopter (CAB or project), I want the coupled traditional+CC-native protocol documented | `knowledge/reference/ux-testing-agentic-os.md` passes audit, ≤300 lines, maps surfaces → frameworks → evidence types → verification instruments | Must |
| F006 | Initial pass population | As a user, I want my 7 brain-dump items + deferred TODO items logged verbatim in a first pass | `notes/ux-log-001-2026-04-22-pass-1.csv` contains ≥25 rows; `user_comment` columns are verbatim (not paraphrased) for user-originated items | Must |
| F007 | Orchestrator triage of initial pass | As user reviewing the pass, I want orchestrator synthesis, framework anchors, and routing decisions populated | `orchestrator_take`, `framework_anchor`, `downstream_target`, `kano` (where applicable), `rice_score` (where ≥3 peers) are populated; user signs off before Phase 5 | Must |
| F008 | State-linkage protocol spec | As an operator invoking planning-implementation + cab:execute-task, I want deterministic row-status updates | Phase 5 deliverable: written spec for `ux-log-sync.sh` hook behavior, status-transition rules, commit-message UXL reference convention. Implementation is a separate tracker row. | Should |
| F009 | Relocate orphan references | As skill-maintenance hygiene, I want `skills/planning-implementation/references/*` moved to `knowledge/reference/` (correct semantic home) | 3 files relocated, `planning-implementation/SKILL.md` references updated, `knowledge/reference/INDEX.md` updated | Must |
| F010 | Distributable template spec | As a CAB-consuming project, I want a copy-paste-adoptable template after CAB validates it internally | Phase 6 deliverable: `knowledge/reference/ux-log-template/` extracted generic template with adaptation notes; only after ≥2 pass cycles on CAB itself | Could |

### 2.2 Non-Functional Requirements

| Category | Requirement | Target | Measurement |
|---|---|---|---|
| Maintainability | Column additions without breaking existing rows | CSV headers stable for v1; any future column appended at end | `git diff` on header row |
| Portability | Schema importable into Jira/Linear | Core columns map 1:1 to issue-tracker concepts | Manual schema-map review during Phase 1 |
| Performance (cognitive) | Log-time entry cost | ≤60 sec per row for user; ≤5 min per row for orchestrator triage | Self-timed during Phase 3-4 |
| Compliance | kb-conventions for new KB files | 100% pass | `/validate --cab-audit` |
| Compliance | flat-notes (LL-25) | No new subdirs under `notes/` | `find notes/ -type d` count unchanged except `_archive/` |
| Usability | Picklist discipline | All closed-vocabulary columns documented in guide | Guide checklist |
| Durability | Plan artifact self-contained | Any future session can resume from this file alone | Appendix C preserves raw source material |

---

## 3. System Architecture

### 3.1 File Topology

```
notes/
├── ux-log-template.csv                      # header-only template (F001)
├── ux-log-guide.md                          # ≤300 line guide (F002)
├── ux-log-examples.csv                      # illustrative rows, 1+ per surface (F003)
├── ux-log-001-2026-04-22-pass-1.csv         # first live pass (F006)
└── impl-plan-ux-log-tracker-2026-04-22.md   # THIS PLAN (link target for F008)

knowledge/reference/
├── INDEX.md                                 # update to reference new files (F004, F005)
├── prioritization-frameworks.md             # NEW (F004)
├── ux-testing-agentic-os.md                 # NEW (F005)
├── requirements-doc-guide.md                # RELOCATED from skills/planning-implementation/references/ (F009)
├── visualization-workflow.md                # RELOCATED (F009)
├── workflow-processflow.md                  # RELOCATED + UTF-16→UTF-8 fix (F009) - surfaces as first tracker row
├── product-design-cycle.md                  # existing
└── a-team-database.yaml                     # existing

skills/planning-implementation/
├── SKILL.md                                 # update references to point to knowledge/reference/ (F009)
└── [references/ folder removed after relocation]
```

### 3.2 Data Model — 25-column CSV schema, tiered by fill cost

Full schema with picklist vocabularies and fill-time responsibility in **Appendix B**. Tiering optimizes for two real-world entry modes: **(a) user raw braindump** — low-friction capture; **(b) future UX-log-capturer subagent** — NL-dialogue → row mapping. T1 is the only absolute minimum the user ever fills manually; T2–T3 are orchestrator/hook/subagent responsibility.

| Tier | Label | Cols | Populated by | Rationale |
|---|---|---|---|---|
| **T1** | Braindump minimum (user) | 5: `id`, `surface`, `title`, `user_comment`, `category` | User (or future capturer subagent from dialogue) | The minimum semantic payload a 30-sec observation carries — what the user actually types |
| **T2** | Auto-populated at intake | 3: `date`, `reviewer`, `pass` | Hook / shell ergonomics | Inferrable from session context — zero human cost, zero judgment required |
| **T3** | Intake normalization | 3: `component`, `lifecycle_stage`, `severity` | Orchestrator or capturer subagent at log-ingest | Derivable from `surface` + `user_comment`; closed-vocabulary picklists enable NL→row mapping verification |
| **T4** | Strongly recommended (log or triage) | 6: `observed`, `expected`, `evidence`, `value`, `effort`, `orchestrator_take` | Orchestrator at triage (or user at log if readily available) | Enriches triage + promotion; absent rows are still actionable |
| **T5** | Triage synthesis | 4: `framework_anchor`, `kano`, `rice_score`, `downstream_target` | Orchestrator at triage | Requires surface-conditional vocabulary + comparative peer analysis |
| **T6** | Promotion-time | 1: `moscow` | Orchestrator at release-batching | Scope-transient; meaningful only per-release, never row-intrinsic |
| **T7** | Lifecycle auto-populated | 3: `linked_plan`, `linked_commit`, `status` | Hook (`ux-log-sync.sh`, Phase 5 spec) | Deterministic state-machine — never manually edited after row init |

**Knowledge-graph-critical subset** (minimum required for programmatic orchestration + state management — these make a row *graph-reachable*):

| Role | Cols | Fill cost |
|---|---|---|
| Node identity | `id` | Auto-generatable |
| Classifier edges (query axes) | `surface`, `lifecycle_stage`, `downstream_target` | 1 user (`surface`) + 2 orchestrator (T3/T5) |
| State-machine edges (traversal) | `status`, `linked_plan`, `linked_commit` | All hook-auto (T7) |

User-fill burden for KG-minimum participation: **1 column (`surface`)**. Everything else is derivable by orchestrator or automatable via hook. This satisfies the user directive: braindumps must be cheap; KG must still function.

### 3.3 State-Linkage Architecture (F008 spec)

```
┌─────────────────┐
│ tracker row     │  status=open → triaged
│ UXL-NNN         │
└────────┬────────┘
         │ /cab:planning-implementation invoked
         ▼
┌────────────────────────┐     writes: linked_plan = notes/impl-plan-<slug>-<date>.md
│ impl-plan-NNN.md       │     updates: status = planning
│ (plan artifact)        │
└────────┬───────────────┘
         │ user approves plan
         ▼
┌────────────────────────┐     updates: status = in-progress
│ /cab:execute-task      │
└────────┬───────────────┘
         │ commits land with message: "... [UXL-NNN]"
         ▼
┌────────────────────────┐     post-commit hook writes: linked_commit = <hash>
│ git commit <hash>      │     if verification passes: status = resolved
└────────┬───────────────┘
         │ if LL-promotion warranted
         ▼
┌────────────────────────┐     LL entry's evidence/source field: "UXL-NNN"
│ notes/lessons-learned  │     tracker row's downstream_target = LL
└────────────────────────┘     tracker row's orchestrator_take appends LL-NN ref
```

Hook enforcement (Phase 5 spec; implementation is a later tracker row):
- Pre-SkillUse hook: detect `/cab:planning-implementation` or `/cab:execute-task` with args referencing `UXL-\d+`; auto-update corresponding row
- Post-commit hook: scan commit message for `[UXL-\d+]` pattern; update row's `linked_commit`; run `/validate` subset against UXL acceptance criteria; if pass → status=resolved
- Script: `hooks/scripts/ux-log-sync.sh` — deterministic row updater

### 3.4 Architecture Decision Records

| Decision | Options | Choice | Rationale |
|---|---|---|---|
| Storage format | CSV / JSON / YAML / SQLite | CSV | Jira/Linear-portable; Excel-editable; human-readable diff; no tooling required |
| File location | `notes/ux-log/` (subfolder) vs `notes/ux-log-*.csv` (flat prefix) | Flat prefix | Preserves LL-25 flat-notes policy; ux-log-* prefix groups files naturally |
| User-comment preservation | Paraphrase OK / Verbatim only | Verbatim only | User explicit directive; LL-28 dialogue-state preservation |
| Prioritization at log time | Single framework / Tiered stack | Tiered (Value-Effort+Severity at log; Kano+RICE at triage; MoSCoW at promotion) | Minimizes log-time friction; richer triage when orchestrator attention available |
| Framework anchor column | Universal / Surface-conditional | Surface-conditional vocabularies | Nielsen/WCAG don't apply to meta/agentic; CAB-DP doesn't apply to GUI. Forcing universal would produce junk data. |
| Prioritization KB home | In `notes/ux-log-guide.md` (P1) / `knowledge/reference/` (P2) / `planning-implementation/SKILL.md` (P3) | P2 (`knowledge/reference/prioritization-frameworks.md`) | Universal utility asset; planning-implementation skill + tracker guide both reference it; wrapper axiom (don't duplicate) |
| Orphan references migration | Keep in skill / Relocate to knowledge/reference/ | Relocate | `knowledge/reference/INDEX.md` defines it as "Generalized conceptual frameworks... advisory references" — exact semantic match. Orphan-from-skill was the deviation. |

---

## 4. Implementation Phases

### Phase 1: Research & Specification Lock

**Duration**: This session (remainder)

| Task | Deliverable | Acceptance Criteria | Status |
|---|---|---|---|
| 1.1 Prioritization frameworks synthesis | Appendix A.1 of this plan | Cites 8 frameworks with when-wins/when-fails; tiered stack justified | ✓ complete (Appendix A.1 below) |
| 1.2 UX-for-agentic-OS synthesis | Appendix A.2 of this plan | Couples traditional PM frameworks + LLM-eval industry practice; names concrete evidence types per surface | ✓ complete (Appendix A.2 below) |
| 1.3 Surface taxonomy validation | Appendix B column vocab | 5 surfaces orthogonal; no known observation type outside taxonomy | ✓ complete (Appendix B below) |
| 1.4 Schema finalization | Appendix B | 25 columns with picklist vocabs; fill-time per column | ✓ complete (Appendix B below) |
| 1.5 State-linkage protocol | Section 3.3 + 3.4 | Deterministic; hook-enforceable; status state-machine legal transitions spec'd | ✓ complete (Section 3.3 above) |

**Phase Gate**: User sign-off on this plan document. Specifically: schema (Appendix B), research synthesis (Appendix A), framework anchor vocabularies by surface.

### Phase 2: Template Scaffolding

**Duration**: Next session (fresh context)

| Task | Deliverable | Acceptance Criteria | Status |
|---|---|---|---|
| 2.1 Create CSV template | `notes/ux-log-template.csv` | 25 headers exactly matching Appendix B order | pending |
| 2.2 Author guide | `notes/ux-log-guide.md` | ≤300 lines; cheat sheets for all 10 picklists; workflow sections for log/triage/promotion; references `knowledge/reference/prioritization-frameworks.md` | pending |
| 2.3 Author examples | `notes/ux-log-examples.csv` | ≥5 rows (1 per surface); each demonstrates realistic log-time + triage-time population | pending |
| 2.4 Author prioritization KB card | `knowledge/reference/prioritization-frameworks.md` | ≤300 lines, frontmatter-compliant per kb-conventions, source citations, tiered-application section | pending |
| 2.5 Author UX-testing-agentic-OS KB card | `knowledge/reference/ux-testing-agentic-os.md` | ≤300 lines, frontmatter-compliant, couples traditional+CC-native, per-surface evidence table | pending |
| 2.6 Relocate orphan references | `skills/planning-implementation/references/*` → `knowledge/reference/*` | 3 files moved; `workflow-processflow.md` converted UTF-16→UTF-8 during move; `planning-implementation/SKILL.md` references updated; `knowledge/reference/INDEX.md` updated | pending |
| 2.7 Commit | git commit | Single commit or logical split; message references this plan file | pending |

**Phase Gate**: `/validate --cab-audit` passes on new KB files; `/validate` passes overall; no `notes/` subdirs created.

### Phase 3: Initial Pass Population

**Duration**: Same session as Phase 2 (append)

| Task | Deliverable | Acceptance Criteria | Status |
|---|---|---|---|
| 3.1 Create pass file | `notes/ux-log-001-2026-04-22-pass-1.csv` | Header row per template | pending |
| 3.2 Seed user's 7 items | Rows `UXL-001` through `UXL-007` | `user_comment` VERBATIM from Appendix C of this plan (no paraphrase); log-time fields filled; triage columns empty | pending |
| 3.3 Absorb deferred TODOs | Rows `UXL-008+` | Each deferred item from `notes/TODO.md` below T1 boundary (lines 50+) becomes a row; `user_comment` preserves original phrasing; `reviewer=user` for user-originated, `reviewer=orchestrator` for orchestrator-originated LL follow-ons | pending |
| 3.4 Dogfood row for UTF-16 bug | Row `UXL-0NN` (surface=meta) | Documents `workflow-processflow.md` encoding issue discovered during Phase 1; self-application proof | pending |
| 3.5 Commit | git commit | Message: `feat(ux-log): initial pass — seed 7 user items + deferred TODOs + dogfood row` | pending |

**Phase Gate**: Row count ≥25; all `user_comment` fields contain verbatim source text (verifiable by grep against Appendix C and TODO.md sources); no orchestrator synthesis leaked into `user_comment` column.

### Phase 4: Triage of Initial Pass

**Duration**: Same session as Phase 3 (append)

| Task | Deliverable | Acceptance Criteria | Status |
|---|---|---|---|
| 4.1 Fill `orchestrator_take` | All rows | Concise synthesis per row (≤200 chars); does not duplicate `user_comment` | pending |
| 4.2 Fill `framework_anchor` | All rows | Surface-conditional vocab used correctly per Appendix B.framework_anchor table | pending |
| 4.3 Fill `kano` | UX-surface rows only (gui + applicable cli/agentic) | Rows where Kano doesn't map left blank; rationale implicit via empty | pending |
| 4.4 Fill `rice_score` | Rows where ≥3 comparable peers in same surface/category exist | Numerical score; others left blank | pending |
| 4.5 Fill `downstream_target` | All rows | One of 8 values per Appendix B.downstream_target | pending |
| 4.6 Produce prioritized queue | Ordered list in triage commit message or `notes/progress.md` update | Top N rows identified for next `/cab:planning-implementation` invocations; rationale cited | pending |
| 4.7 User review + sign-off | User inline approval | User either approves triage as-is or provides per-row corrections; plan file's Phase 4 section updated with approval note | pending |

**Phase Gate**: User sign-off on triage. Prioritized queue exists. Phase 5 spec is reviewed.

### Phase 5: Per-Row Execution Protocol Documentation

**Duration**: Same session as Phase 4 (append) OR next session

| Task | Deliverable | Acceptance Criteria | Status |
|---|---|---|---|
| 5.1 Write protocol spec | Section in `notes/ux-log-guide.md` | Status state machine diagram; legal transitions; triggering events; hook behavior | pending |
| 5.2 Commit message convention | Documented in guide + `.claude/rules/kb-conventions.md` update | `[UXL-NNN]` suffix convention documented | pending |
| 5.3 Hook implementation spec | Separate tracker row (not executed this plan) | Detailed spec for `hooks/scripts/ux-log-sync.sh`; triggered by SkillUse + PostCommit events | pending |
| 5.4 LL cross-reference convention | Documented in guide + `.claude/rules/kb-conventions.md` update | When tracker row promotes to LL, LL entry's evidence section references `UXL-NNN`; bidirectional | pending |

**Phase Gate**: Protocol is unambiguous enough that a fresh-session orchestrator could execute a row end-to-end from triaged → resolved without re-consulting this plan. Hook implementation deferred to separate tracker row (itself created in Phase 3 as a follow-on item).

### Phase 6: Distributable Template Extraction

**Duration**: Post-dogfood (≥2 pass cycles on CAB itself)

| Task | Deliverable | Acceptance Criteria | Status |
|---|---|---|---|
| 6.1 Generalize pass file | `knowledge/reference/ux-log-template/pass-template.csv` | CAB-specific examples stripped; placeholder rows for `surface=gui/cli/agentic/integration/meta` | deferred |
| 6.2 Generalize guide | `knowledge/reference/ux-log-template/README.md` | CAB-specific references generalized; adaptation-notes section added | deferred |
| 6.3 Document adoption in `knowledge/implementation/workflow.md` | Workflow update | New step in project-init: "Copy ux-log-template/ to project's notes/" | deferred |
| 6.4 Dogfood validation | CAB tracker has ≥2 pass cycles | Retrospective notes inform template defaults | deferred |

**Phase Gate**: CAB tracker has operated for ≥2 triage cycles; lessons inform template defaults; then extraction proceeds.

---

## 5. Testing Strategy

| Level | Scope | Method | Target |
|---|---|---|---|
| Structural (unit-equivalent) | CSV schema validity | Header row matches Appendix B exactly | 100% |
| KB compliance (integration) | New KB cards | `/validate --cab-audit` scoring dimension | ALIGNED or above (≥70%) |
| Policy compliance | Flat-notes, frontmatter, link discipline | `/validate` + manual `find notes/ -type d` check | 0 violations |
| Round-trip (E2E) | Open template.csv → add row in Excel → save → git diff clean | Manual test in Phase 2 | passes |
| Dogfood (acceptance) | Tracker captures real CAB-internal friction during Phase 3 | UTF-16 bug row exists | 1 self-reference row minimum |
| User SME verification | Plan artifact | User reads plan, signs off or corrects | approval captured in session turn |

---

## 6. Deployment Plan

Not applicable in traditional sense — artifacts are in-repo files, not deployed services. Replaced with:

### 6.1 Rollout to CAB-Internal Use

- Phase 2 commit = "deployed" to CAB operator (self-use immediate)
- Phase 3 initial pass = first productive use

### 6.2 Rollout to CAB-Consuming Projects (Phase 6)

- After ≥2 CAB-internal pass cycles, extract generic template
- Document adoption step in `knowledge/implementation/workflow.md`
- HydroCast, RAS-exec adopt via copy + adapt
- Adoption success metric: HydroCast's existing `gui-review-comments/` logs migrate to unified `ux-log-*` naming

### 6.3 Rollback

CSV and markdown files — `git revert` on any commit; zero external service impact.

---

## 7. Risk Register

| Risk | Prob | Impact | Mitigation |
|---|---|---|---|
| 25-column schema is too heavy — users (including me) avoid logging | Med | High | Tiered population; log-time requires only 10 cols. If still too heavy at end of Phase 3, reduce to 20 or reshape columns. |
| Surface taxonomy misses a real-world observation type | Low | Med | `meta` catch-all absorbs unclassifiable; in Phase 4 triage, flag any entry that strained the taxonomy; revise before Phase 6. |
| Raw-comment preservation drifts over time (orchestrator condenses in later turns) | Med | High | Explicit non-negotiable in F006; Appendix C is the durable source-of-truth; pre-commit grep check that `user_comment` still matches Appendix C source for Phase 3 rows. |
| Hook enforcement (F008) is punted too long → manual state-linkage rots | High | Med | Phase 5 writes the spec even though implementation is a separate tracker row. Rotting risk documented as a tracker row itself so it doesn't vanish. |
| Phase 6 distributable template extraction happens too early → premature generalization | Med | Med | Hard gate: ≥2 pass cycles on CAB first. Don't extract until defaults are informed. |
| KB files exceed 300 lines | Low | Med | Phase 2 budget awareness; split `prioritization-frameworks.md` into log/triage/promotion subfiles if needed. |
| `linked_plan` + `linked_commit` columns stay empty because convention drifts | High | Med | Phase 5 makes this deterministic via hooks; until hooks land, orchestrator self-discipline + periodic sync script (manual until automated) |
| User's 7 items get paraphrased during transcript compaction before Phase 3 executes | High (if delayed) | High | **MITIGATION ALREADY APPLIED**: Appendix C below contains verbatim text. Plan file = durable source. |

---

## 8. Operational Handoff

### 8.1 Documentation Checklist

- [x] This plan (`notes/impl-plan-ux-log-tracker-2026-04-22.md`)
- [ ] `notes/ux-log-guide.md` — deliverable of Phase 2
- [ ] `knowledge/reference/prioritization-frameworks.md` — deliverable of Phase 2
- [ ] `knowledge/reference/ux-testing-agentic-os.md` — deliverable of Phase 2
- [ ] `knowledge/reference/INDEX.md` updated — Phase 2
- [ ] `skills/planning-implementation/SKILL.md` reference updates — Phase 2
- [ ] `.claude/rules/kb-conventions.md` updated for `[UXL-NNN]` commit convention — Phase 5

### 8.2 Maintenance Plan

- Tracker reviewed at end of each CAB session (brief) or explicit "triage cycle" (deep)
- Monthly: archive resolved rows to `notes/_archive/ux-log-resolved-YYYY-MM.csv`; keep active rows in current pass file
- Each new pass = new pass file (`ux-log-NNN-YYYY-MM-DD-pass-N.csv`); prior pass archived after merge
- LL promotions: whenever a row's `downstream_target=LL` is executed, both files cross-reference (row ↔ LL-NN)

---

## AI-Integrated Addendum

This IS an AI-integrated project (CAB is the agentic OS platform). Applicable considerations:

### AI Threat Model

- **Hallucination risk** in `orchestrator_take` column — mitigation: short, evidence-anchored synthesis; `user_comment` column is ground truth
- **Scope drift** in triage — mitigation: framework_anchor + lifecycle_stage force specificity
- **Context degradation** across sessions for long-running tracker state — mitigation: pass-file partitioning + archival + plan file as durable source
- **Subagent cascade** if UX-log-capturer is built (future) — mitigation: closed-vocabulary picklists make NL→row mapping verifiable

### Human-AI Collaboration Model

| Activity | User (human SME) | Orchestrator (AI) |
|---|---|---|
| Raw observation capture | **Authoritative** (user_comment verbatim) | Captures for user, never synthesizes into user_comment |
| Synthesis / framing | Supplementary | **Authoritative** (orchestrator_take) |
| Framework anchor selection | Review / override | **Default author** |
| Priority triage (kano/RICE) | Approves / re-ranks | **Default author** |
| Promotion decision (downstream_target) | Approves | **Default author** |
| Plan creation (/cab:planning-implementation) | SME verification before execute | **Default author** |
| Execution | Approves via command invocation | **Default author** once approved |

### Responsible AI Checklist (applicable subset)

- [x] Transparency: orchestrator_take column separates AI synthesis from user raw observation
- [x] Auditability: every resolution has `linked_plan` + `linked_commit` trail
- [x] Human oversight: `planning` status between triage and in-progress is machine-enforced gate
- [x] Failure graceful: tracker is append-only in practice; errors are recoverable via git

---

## Appendix A: Framework Research Synthesis

### A.1 Prioritization Frameworks (deep research per user directive)

Eight frameworks surveyed. Each evaluated on: origin/authority, method, when it wins, when it fails, data/context cost. Citations cite primary sources where known.

| Framework | Origin | Method | Wins | Fails | Cost |
|---|---|---|---|---|---|
| **RICE** | Sean McBride, Intercom, ~2018 (Reforge) | (Reach × Impact × Confidence) / Effort — produces ranking score | Large backlogs needing comparative ranking; team with historical data for impact/confidence calibration | Small backlogs (<5 items); novel domain with no confidence data; GIGO if estimates are fabricated | High: 4 numeric estimates per item |
| **MoSCoW** | Dai Clegg (Oracle UK → DSDM), 1994 | Must / Should / Could / Won't (for a scope-bounded release) | MVP scoping; release planning under fixed timeline; stakeholder alignment | As a permanent property of a row (M/S/C/W is release-scope-transient, not row-intrinsic); pure backlogs | Low: 1-of-4 pick — but only valid *per release* |
| **Kano** | Noriaki Kano, 1984 ("Attractive Quality and Must-Be Quality") | Basic (must-have) / Performance (linear value) / Delight (surprise) classification | UX-surface items where user-value curve is non-linear; reveals invisible basics | Non-UX items (infra, compliance); quantitative ranking | Med: requires user mental-model awareness |
| **Value vs. Effort (2x2)** | Generic Agile practice | Plot on 2x2; top-left (high value / low effort) first | Fast initial triage; resource-constrained teams | Ties within quadrants; doesn't differentiate between items in same quadrant | Very low: 2 L/M/H picks |
| **WSJF** (Weighted Shortest Job First) | SAFe (Dean Leffingwell, ~2011) | Cost of Delay / Job Size | Economic rationality; large enterprise with mature CoD estimation | CoD is hard to estimate honestly; over-engineered for small teams | Very high: 4+ estimates including CoD |
| **ICE** | Sean Ellis / GrowthHackers, ~2014 | Impact × Confidence × Ease | Growth-hacking / experimentation contexts; simpler than RICE | Lacks Reach dimension — biases toward items that affect few users deeply | Med: 3 numeric estimates |
| **Eisenhower Matrix** | Popularized by Stephen Covey (1989); attributed to Dwight Eisenhower | Urgent × Important 2x2 | Personal task management; daily/weekly triage | Feature backlogs (urgency rarely defined at feature level); team-scale prioritization | Low but low-signal for product work |
| **Stack Ranking** | GE (Jack Welch era, 1980s); widely critiqued | Forced-rank order 1..N | Situations demanding explicit top-N selection | Psychologically destructive at team level; no absolute value info; 17th-ranked item has identical metadata to 18th | Low per-item but high cognitive overhead at full list |

**Sources (for verification during Phase 2 KB-card authoring)**:
- RICE: Reforge article by Sean McBride; Intercom engineering blog
- MoSCoW: DSDM Consortium documentation; Agile Business Consortium
- Kano: Kano, N. (1984). *Attractive Quality and Must-Be Quality*. Journal of the Japanese Society for Quality Control, 14(2)
- WSJF: Scaled Agile Framework (scaledagileframework.com)
- ICE: Sean Ellis & Morgan Brown, *Hacking Growth* (2017)
- Eisenhower Matrix: Covey, S. (1989). *The 7 Habits of Highly Effective People*

### Recommended Tiered Stack (synthesis)

| Time | Required / Optional | Frameworks applied | Cols populated |
|---|---|---|---|
| **Log time** (entry creation) | Required | Severity + Value-vs-Effort | `severity`, `value`, `effort` |
| **Triage time** (orchestrator review) | Optional where applicable | Kano (UX-surface only), RICE (when ≥3 comparable peers) | `kano`, `rice_score` |
| **Promotion time** (row batched into release / progress sprint) | Optional per-release | MoSCoW | `moscow` |

**Explicitly excluded from v1**:
- WSJF — enterprise-scale, CoD estimation overkill for CAB/small-team projects; documented as option for adopters with SAFe background
- Eisenhower Matrix — wrong altitude (personal-task, not product-feature)
- Stack Ranking — psychologically destructive, no absolute value info
- ICE — if RICE is already available, ICE adds no unique signal

**Rationale for Value-vs-Effort as log-time default** (vs. severity alone): severity captures impact-if-unaddressed, but not effort-to-address. A MAJOR-severity item that takes 2 hours ≠ a MAJOR-severity item that takes 2 months. V/E + severity together are richer than either alone.

**Rationale for Kano UX-only**: Kano's three categories make sense for user-facing experience (a Must-Be for auth; Performance for response time; Delight for onboarding touches). They don't map for infra/compliance/architecture — forcing it produces noise.

### A.2 UX Testing for Agentic OS Platforms (synthesis)

Traditional PM UX QA married to LLM/agent observability, synthesized from 2025-2026 industry practice.

#### Traditional Side (applies primarily to `gui` + backend `cli`)

- **Nielsen 10 Heuristics** (NN/g, 1994): dominant UX eval standard. H1-H10 picklist.
- **WCAG 2.2 AA** (W3C, Oct 2023): accessibility authoritative. Success criterion codes.
- **ISO 9241-210:2019**: Human-centred design lifecycle (context-of-use / requirements / design / evaluation). **Universal column across all surfaces** — this is the coupling interface.
- **ISO/IEC 25010:2023**: 8 software quality attributes (functional-suitability, performance-efficiency, compatibility, usability, reliability, security, maintainability, portability).
- **Shneiderman's 8 Golden Rules**: complementary heuristic set; cross-check not primary column.

#### LLM-Augmented Side (applies primarily to `agentic` + `integration`)

- **Evaluation harness patterns** (LangSmith / Langfuse / Braintrust industry standard): structured evals with test cases, expected outputs, scoring rubrics. **CAB analog**: `verifier` agent + acceptance criteria per row. Row-level verification criteria come FROM the tracker.
- **Observability / tracing**: token cost, tool-call sequences, latency per turn. **CAB analog**: `notes/progress.md` narrative + `notes/bootstrap-cost-log.md` + commit trail.
- **Context degradation awareness** (lost-in-middle, U-shaped attention curves — Liu et al. 2023 "Lost in the Middle"): context quality degrades with position and volume. **CAB analog**: LL-08, LL-12, LL-29 + bootstrap cascade architecture.
- **Prompt cache awareness**: hit rates affect cost + latency. **CAB analog**: 5-min TTL considerations in operational patterns.
- **Multi-agent testing antipatterns**: (a) only single-agent path tested; (b) mock-only tests pass while real cascade regresses; (c) cross-agent context-handoff failures invisible at unit level.

#### Coupled Protocol (the "UX testing for agentic OS" that the tracker implements)

| Surface | Primary framework | Primary evidence | Verification instrument |
|---|---|---|---|
| `gui` | Nielsen Hn / WCAG-X.X.X | Screenshot / axe scan / video | Manual walkthrough + automated accessibility scan |
| `cli` | ISO-25010-usability + Shneiderman | Session transcript slice / tool output paste | `/validate` + manual invocation |
| `agentic` | CAB-DPn + LL-NN refs | Agent trace / token delta / verifier failure | `verifier` agent with per-row acceptance criteria |
| `integration` | CAB-DPn + LL-NN + CC-docs anchor | settings.json diff / plugin.json / `/sync-check` output | `/sync-check` + `/validate --cab-audit` |
| `meta` | CAB-DPn + LL-NN refs | Commit diff / KB file change / LL entry | `/validate --cab-audit` + manual review |

Lifecycle stage (ISO 9241-210) — applied universally across surfaces:
- **context-of-use**: observed behavior ← session transcripts, dialogue gaps (LL-28)
- **requirements**: spec exists? ← kb-conventions, component-standards
- **design**: solution quality vs spec? ← framework heuristics + CAB design principles
- **evaluation**: verification ran? ← `/validate`, `/cab-audit`, `bootstrap-cost.sh`, verifier agent

**This IS the generalized "UI/UX testing for agentic OS" template** that the tracker + its guide operationalize. CAB-consuming projects adopt the framework stack + populate surface-conditional components.

---

## Appendix B: Final 25-Column Schema

Columns in order for CSV header row. **Tier** column encodes fill-cost hierarchy per §3.2. **KG** column flags knowledge-graph-critical columns (reachability / traversal). Legend: T1=user braindump minimum; T2=auto intake; T3=intake normalization (orchestrator/capturer); T4=strongly recommended; T5=triage synthesis; T6=promotion; T7=lifecycle auto.

| # | Name | Tier | KG | Fill Time | Required | Vocabulary / Format |
|---|---|---|---|---|---|---|
| 1 | `id` | T2 | ✓ | log (auto) | Y | `UXL-NNN` sequential; cross-pass continuous |
| 2 | `pass` | T2 |  | log (auto) | Y | int (1, 2, 3...) |
| 3 | `date` | T2 |  | log (auto) | Y | `YYYY-MM-DD` |
| 4 | `reviewer` | T2 |  | log (auto) | Y | `user` / `orchestrator` / `both` (post-merge) |
| 5 | `surface` | **T1** | ✓ | log (user) | Y | `gui` / `cli` / `agentic` / `integration` / `meta` |
| 6 | `component` | T3 |  | log (normalize) | Y | surface-conditional picklist (see sub-table) |
| 7 | `lifecycle_stage` | T3 | ✓ | log (normalize) | Y | `context-of-use` / `requirements` / `design` / `evaluation` |
| 8 | `category` | **T1** |  | log (user) | Y | `bug` / `gap` / `idea` / `question` / `drift` |
| 9 | `severity` | T3 |  | log (normalize) | Y | `BLOCKER` / `MAJOR` / `MINOR` / `QUESTION` / `IDEA` |
| 10 | `title` | **T1** |  | log (user) | Y | ≤80 char imperative-voice summary |
| 11 | `user_comment` | **T1** |  | log (user) | Y | **Verbatim raw** — never paraphrased; user-originated rows preserve exact source text |
| 12 | `orchestrator_take` | T4 |  | triage | N | ≤200 char synthesis/reasoning on #11 |
| 13 | `observed` | T4 |  | log | N | 1-3 sentence description of current behavior |
| 14 | `expected` | T4 |  | log | N | 1-3 sentence description of target behavior |
| 15 | `evidence` | T4 |  | log | N | screenshot path / file:line / commit hash / free text |
| 16 | `value` | T4 |  | log | N | `L` / `M` / `H` |
| 17 | `effort` | T4 |  | log | N | `L` / `M` / `H` |
| 18 | `framework_anchor` | T5 |  | triage | N | surface-conditional vocab (see sub-table) |
| 19 | `kano` | T5 |  | triage | N | `basic` / `performance` / `delight` — UX-surface only |
| 20 | `rice_score` | T5 |  | triage | N | numerical; fill when ≥3 comparable peers |
| 21 | `moscow` | T6 |  | promotion | N | `M` / `S` / `C` / `W` — only when batching into release |
| 22 | `downstream_target` | T5 | ✓ | triage | N | `LL` / `KB` / `rule` / `skill` / `hook` / `TODO` / `progress` / `followup` |
| 23 | `linked_plan` | T7 | ✓ | execute (auto) | N | path to `notes/impl-plan-*.md` |
| 24 | `linked_commit` | T7 | ✓ | execute (auto) | N | git commit hash(es) |
| 25 | `status` | T7 | ✓ | lifecycle (auto) | Y | `open` / `triaged` / `planning` / `in-progress` / `resolved` / `deferred` / `superseded` / `wontfix` |

**Reading the table**: 4 columns are T1 (user-fill during braindump: `surface`, `category`, `title`, `user_comment` — `id` is auto but listed as T2). 8 columns are KG-critical for programmatic knowledge-graph operation. All hook-automated T7 columns are KG-critical. The table makes it visible at a glance that the user's braindump cost is bounded to 4 columns while full KG participation still emerges naturally through orchestrator triage + hook automation.

### `component` — surface-conditional picklists

| `surface` | Component values |
|---|---|
| `gui` | `dashboard`, `forms`, `navigation`, `tables`, `modals`, `charts`, `chat`, `auth`, `onboarding`, `error-states`, `layout`, `cross-cutting` |
| `cli` | `skill-invocation`, `command-invocation`, `argument-parsing`, `output-formatting`, `progress-indication`, `error-messaging`, `session-bootstrap`, `state-files` |
| `agentic` | `orchestrator`, `subagent-delegation`, `tool-use`, `context-handoff`, `verification`, `memory-layer`, `prompt-caching`, `multi-agent-cascade` |
| `integration` | `plugin-schema`, `project-schema`, `marketplace-registration`, `enabled-plugins`, `settings-json`, `hooks`, `mcp-servers`, `permissions` |
| `meta` | `claudemd-layer`, `knowledge-base`, `rules`, `state-management`, `lessons-learned`, `conventions`, `audit-methodology`, `distribution` |

### `framework_anchor` — surface-conditional vocabularies

| `surface` | Primary vocabulary | Example values |
|---|---|---|
| `gui` | Nielsen + WCAG (+ Shneiderman cross-check) | `H1`..`H10`, `WCAG-1.4.3`, `WCAG-2.4.7`, `SH1`..`SH8` |
| `cli` | ISO-25010 attributes | `ISO-usability`, `ISO-maintainability`, `ISO-reliability`, `ISO-performance-efficiency` |
| `agentic` | CAB-DPn + LL-NN refs | `DP1` (Context Engineering), `DP2` (Wrapping Architecture), `DP4` (Orchestration+State), `DP7` (Verification), `LL-08`, `LL-12`, `LL-29` |
| `integration` | CAB-DPn + LL-NN + CC-docs | `DP3` (Standardized KB), `DP5` (Generalized+Actionable), `LL-21`, `LL-27`, `CC-plugins-schema` |
| `meta` | CAB-DPn + LL-NN refs | `DP1`..`DP9`, `LL-10`, `LL-11`, `LL-15`, `LL-25` |

### Status state machine (legal transitions)

```
open → triaged → planning → in-progress → resolved
         │           │            │
         ├──→ deferred            └──→ (rollback) → triaged
         ├──→ superseded
         └──→ wontfix
```

---

## Appendix C: Seed Source — User's 7 Items (Verbatim)

> **CRITICAL**: Text below is VERBATIM from the user's 2026-04-22 session turn (brain-dump immediately preceding this plan's invocation). Phase 3 execution MUST copy this text into the `user_comment` column of rows `UXL-001` through `UXL-007` without paraphrase, condensation, or reformatting. If any text below is found to be paraphrased relative to the session transcript, correct before Phase 3.

### UXL-001 — surface=integration

> we need to ensure our latest CAB don't have a default protocol to setup/validate CC CLI integration into projects by automatically using the distributable plugin schema as default (vs. initially setting it up as a local project with CC CLI integrated where the extensions are nested under project '.claude' path), as I'm noticing a legitimate inefficient UX friction. In hindsight, my personal conjecture of trying to wrap everything into a plugin from getgo will be more holistically practical, but the issue is that I can't load the project CC extensions unless I actually fully register the plugin to marketplace and enable; which is not I want necessarily as enabling external plugins are automatically loaded globally. So instead, our CAB default setup (whether for a brand new project codebase or existing project) should use the claude project schema where all extensions are neatly nested under the project '.claude' path within the project root to live alongside the codebase, ultimately cohesively serving as agentic OS platform (codebase + LLM CLI).

### UXL-002 — surface=meta (command→skill deprecation)

> per latest official CC dev docs, commands will be gradually be sunset and skills to be used/trigerred instead. luckily, our CAB hirearchical wrapping design philosophy, we already were pretty much effectively leveraging the commands to be essentially equivalent to the domain specialized skill extensions but just serving as the easy trigger mechanism by both CC agents and humans, via the dash function for any consistently repeated operations, so let's make sure we archive and no longer further optimize the commands and properly migrate to skills, if there isn't already the main pertaining skill(s) that was composing exist. we need to be strategic and careful here as I'm currently used to triggerring the skill-wrapped commands, not the skills themselves. let's start with a clear mapping of which existing skills are wrapped into commands and which aren't/disconnected, etc.

### UXL-003 — surface=meta (3-layer model + default agent decision)

> we need to revisit our recent discussion (in session 34 i believe) of the Three-layer complement model architecture design philosophy: "global CLAUDEmd (global orchestrator as holistically efficient and generalized "master strategist" with universal or project-agnostic value-adds of memory, rules, skills, agents, hooks, which are technically and soundly domain-specialized of the intended global orchestrator via comprehensive, readily actionable context engineering protocols) → project CLAUDEmd (project orchestrator as holistically efficient and generalized "master strategist" with project-specific domain specialization/contextualization of CC extensions) → CAB's 'orchestrator' subagent being used as the "main default global cc agent" that I talk to per global cc settings JSON (please correct me if i'm misunderstanding here). Each layer is complementary, not redundant". I'm quite set on how I currently define and utilize the global core identity/SME vs. project core identify/SME via CLAUDEmds, but i'm still tad confused whether me setting CAB's specific 'orchestrator' subagent as the default CC global agent is the appropriate/efficient choice; i'm slightly leaning towards getting rid of this global cc setting to let the global CLAUDEmd and each project CLAUDEmd to properly serve as orchestrators.

### UXL-004 — surface=agentic (CAB-to-project orchestrator bridge)

> we need to further strategize how we can allow CAB orchestrator (or domain-specialized subagent as "general CAB advisor", which is fully equipped with the entire knowledge base via systematized context knowledge graph programmatically/visually) to agentically/seamlessly interact with each project domain orhcestrator(s) to ensure the CC integrated project has fully and systematically adopted CAB's various frameworks/design philosophies and context engineering protocols for holistically efficient orchestration and state management. basically, i've been finding myself in multiple occasions of active projects that have CC integrated where I would need to request the project orchestrator agent to refer back to some of the CAB KB packs as the existing agentic wrappers related to creating/integrating CC into new or existing projects, as well as validating/techdebt existing CC integration setup aren't fully capturing.

### UXL-005 — surface=meta (KB → knowledge graph)

> It's my general (assumed) understanding from my UX so far of trying to implement CAB to integrate CC CLI into project codebases, many of these, esp. the above item #4 imo,  could have been influenced by our lack of proper KB standardization to turn the static knowledge base into holistically standardized and efficiently generalized knowledge graph with readily actionable/programmable metadata details for orchestration and state management. some of these will be reflective when we review current standardized protocols of Hydrocast project's knowledge graph essentially programmatically linking the notes\ folder of state mangement and knowledge\ folder of customized domain knowledge base.

### UXL-006 — surface=meta (planning-implementation skill enhancement)

> i made some minor edits to the 'planning-implementation' skill that hasn't been properly recorded via git yet. Review yourself what i've changed/edited/added. I have additional plans to properly incorporate the generalized comprehensive "a-team" and full-stack product design cycle templates to be part of the standard protocol to refer as general conceptual context to strategize holistically and comprehensively, then obviously naturally, adaptively/agentically optimizing to be tailored specifically to the project-specific and/or phase task-specific intentions from the generic comprehensive version. It doesn't necessarily have to be done within this specific skill alone, but we need to strategically plan how we can properly/systematically leverage these resources more adapatively in knowledge\reference

### UXL-007 — surface=meta (CLAUDEmd template + memory layer alignment)

> please confirm whether our latest insights as we were updating the CLAUDEmd of CAB to apply the U-shaped attention curve structure as the effective holistically standardized template CAB advisory will implement, as I really liked it. the standard template should follow mostly to the current @CLAUDE.md of CAB as one of the latest architecture I approve and find it to be quite useful (wouldn't necessarily say it's perfect either so feel free if there is any more optimizations we could make to fully efficiently utilize the precious limited 200-line artifact to describe the core identity/SME). needless to say, CLAUDmd standardization should be actively coupled with the holistically modularized rules, as well as, the latest new distinct ~.claude/<project>/memory/ in global config as well as the your-project / .claude / agent-memory in project config, so we're not inefficiently creating conflicts, duplications, or redudancy.

### Additional seed: user follow-up on schema/framework

> for our UI/UX test tracker template, I like the idea of having a column of my review comments and another column for your general concise takes/internal reasoning on my comments. I think "recommended action" column is not needed, but do be aware each of these ideas/test comments should be categorically grouped/phased and then prioritized via our standardized practice of leveraging '/planning-implementation' to plan and '/cab:execute-task' to execute; aka, you should never be rolling straight to execution with such generic, brief context as the implementation plan. [...]
> basically, this idea of creating a properly structured iterative/live UI/UX test tracker is my "next practical step" based on my current UXs of trying to leverage CAB for multiple projects, where we are now systematizing the state mgmt and the planned enhancement of KB more programmatically with this tabular repo as the backend db and the context knowledge graph visualized as the "frontend", where all TODO tasks of past, active, and deferred/potential ideas are centralized with proper seamless filtering mechanisms

(This excerpt captures the meta-framing — preserved here for downstream reference but NOT a tracker row itself; the 7 items above and the self-dogfood row below are the rows.)

### Dogfood self-reference: UXL-008 — surface=meta, drift

> Discovered during Phase 1 plan research (2026-04-22): `skills/planning-implementation/references/workflow-processflow.md` is UTF-16 encoded, rendering as spaced characters when read. Identical failure mode as HydroCast `USGS_WPI/usgs_data_categories.md` fixed in Session 33. Belongs in `knowledge/reference/` (per folder semantics) AND needs UTF-16→UTF-8 conversion during relocation. This row exists as the first self-application proof that the tracker captures real CAB-internal drift — not just external observations.

### Deferred TODO source — `notes/TODO.md` lines 50+ (below T1 boundary)

Phase 3 execution absorbs these as rows `UXL-009` and beyond. Full source is `notes/TODO.md:50-180` (current file state). Categories to preserve in `user_comment` verbatim:

- LL-27 follow-ons (4 items): `/sync-check` name-collision extension, new KB card `multi-agent/agent-resolution.md`, shadow-check in `/validate --cab-audit`, global CLAUDE.md "CAB provides" notes
- LL-28 follow-ons (4 items): event-triggered state-write protocol, fallback dying-session recovery protocol, bootstrap token cost tracking, reversibility inventory
- LL-25 follow-ons (3 items): RAS-exec policy propagation, HydroCast policy propagation, CC Memory Layer Alignment deep-dive KB card
- LL-26 follow-on (1 item): backtick-wrapped marker exclusion in pre-push hook regex
- LL-10 / LL-17 / LL-02 / LL-12 / LL-08 structural counters (from P0/P1 in Top Priorities — partial overlap, reconcile at Phase 3)
- Plugin-first architecture correction Phases 1-5 (most complete; deferred WARN items)
- Global CLAUDE.md v2 architecture upgrade
- LL-25 Dream consolidation skill concept

Phase 3 MUST preserve original phrasing of each item as it currently appears in `notes/TODO.md`. `reviewer=orchestrator` for these (they were authored by orchestrator in prior sessions, not user).

### Additional user-directed deferrals (2026-04-22) — must become tracker rows in Phase 3

These two items were raised by the user during plan review/approval. They are explicitly deferred until AFTER this plan fully executes (user directive: "i don't mind us tackling these two new reference deep dives after fully implementing the current draft plan first, instead of us backtracking and possibly getting conflicts/confusions"). They seed as T1-minimum rows with `category=idea`, `status=deferred`, `reviewer=user`:

#### UXL-0NN — surface=meta (HydroCast KB-standardization pattern extraction)

> Review HydroCast's `kb-standardization-plan.md` (path: `Flood-Forecasting/knowledge/reference/kb-standardization-plan.md`) for its agentic/programmatic knowledge-graph patterns. Evaluate which patterns are extractable as CAB-generalizable conventions for the KB → knowledge-graph architecture work (cross-refs UXL-005). Produce a pattern-extraction summary + recommendation for what, if anything, to absorb into CAB's `kb-conventions.md` rule or a new KB card.

#### UXL-0NN — surface=integration (AgentContextGraphVisualizer feasibility evaluation)

> Review 3rd-party repo: https://github.com/nicollorens12/AgentContextGraphVisualizer (unverified, not yet used by user). Evaluate feasibility of building a custom CAB-native equivalent for visualizing the context knowledge graph (cross-refs UXL-005). Constraints: CLI/tool form, NOT VS Code extension. Decision to make: integrate into CAB repo directly, or develop as separate distinct repo that CAB (and other CC-integrated projects) call as a dependency. Produce a feasibility summary + storage/architecture recommendation.

---

## Sign-Off

Plan awaiting SME verification (user). On approval, proceed to Phase 2 (template scaffolding) in this session or next.

**Verification questions for the user**:
1. Schema (Appendix B) — does anything in the 25 columns strike you as misplaced, missing, or wrongly categorized?
2. Framework synthesis (Appendix A) — are the prioritization-stack tier assignments (Value-Effort + Severity at log, Kano + RICE at triage, MoSCoW at promotion) correct, or would you shift any framework to a different tier?
3. Surface taxonomy (5 surfaces) — does `meta` as catch-all feel right, or should it be split further (e.g., `meta-architecture` vs `meta-policy`)?
4. Seed source (Appendix C) — is the verbatim preservation of your 7 items faithful? Any paraphrase you want corrected now, before it becomes tracker-row ground-truth?
5. Phase 5 hook enforcement — OK to spec now, implement via separate tracker row? Or implement in same session as Phase 2 to close loop sooner?
