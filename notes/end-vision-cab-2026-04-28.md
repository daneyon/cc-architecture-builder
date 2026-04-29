# CAB End-Vision: Agentic OS Platform via Skills-as-Modular-Software

**Status**: ACTIVE — cold-start anchor for every Wave 8-11 session bootstrap
**Origin**: Session 39 (2026-04-28) reframe; user brain-dump + synthesized direction
**Supersedes**: original "graph over existing KB" framing in `notes/impl-plan-kb-to-kg-2026-04-24.md`
**Codified in**: `knowledge/overview/architecture-philosophy.md` § "Skill Composition Model & End-Vision Architecture"

---

## User Brain-Dump (Verbatim, 2026-04-28)

> i'm not sure if this current "end-vision" UI/UX i generally have in mind for CAB or my maximized usage of CC in general will come to be useful at this stage, but I want to be transparent with you at all times during our iterative developments so we are collaboratively strategizing and executing in holistically efficient manner. If we regard CAB as another "traditional project" with a codebase, including src\, docs\, all the typical traditional codebase will consist of, where we then seamlessly integrate CC to be living alongside with the codebase to turn the project into an "agentic OS platform" (codebase + LLM CLI), each domain-specialized skill will be the live, walking, iterative/dynamic KB packs where each eventually builds up to be skill = software = modularized codebase into specific domain-specialized skillsets, so the "agentic OS platform" i keep coining will eventually effectively be merged into a single platform, where all core processors under the traditional codebase schema src\ will now be systematized into specialized CC skills (custom NL instruction for agentic reasoning in markdown and orchestration + utility scripts of the src\ + tailored KB cards into the skill's references folder programmatically). CAB is somewhat unique b/c we're jumping straight into this merged agentic OS platform vision since it didn't have an existing traditional codebase like GTA, Hydrocast projects for example. to clarify, this end-vision is not a strict requirement, and i'm not certain whether the native CC have the adequate capabilities for me to realize this practically today as well. I just wanted to have this in your purview as we push through the UX wave plan and re-thinking through many of our original/possibly outdated philosophies and system designs. i'd be curious whether you think the current skills list reflect this end-vision (aka do the existing skills and agents, along with the rules and memory, fully cover all aspects of static KB packs into agentic, readily actionables?)

## Q4 Pattern Capture (Screenshot Excerpt — for `knowledge/reference/llm-interaction-patterns.md`)

User-shared screenshot illustrates three observable patterns from boots-on-the-ground CAB usage:

1. **Imperative trigger format drives invocation reliability** — mid-session, model attention on skill descriptions degrades (lost-in-middle). The `INVOKE THIS SKILL when X. DO NOT Y -- use this skill's Z` pattern frames description as three axioms (when, prohibition, alternative) instead of one paragraph — dense, scannable, decision-shaped. Measurable improvement in auto-invocation when multiple skills compete for the same intent.
2. **Skills as thin orchestration, not re-implementation** — every skill wraps an existing importable function. Zero `scripts/` bundles unless the skill grows a multi-step shell workflow. This is CAB DP8 (wrap, don't reinvent) applied at the skill layer. If a skill grows a multi-step shell workflow, *that's* when `scripts/` earns its slot — not preemptively.
3. **Verification section as runnable contract** — each SKILL.md names the exact pytest invocation + Python-level assertion snippet that confirms the skill fired correctly. A future autonomous loop can literally execute the assertion block via subprocess — verification is machine-readable, not prose.

These are CAB-derived value-add (transformer attention mechanics → SKILL.md authoring patterns). Target codification: `knowledge/reference/llm-interaction-patterns.md` (Wave 8 Phase 2J).

---

## Synthesized Direction

### The Corrected Metaphor

Skills are **not** Python `src/` modules. The accurate analogue is **UNIX coreutil + man page + sandbox** or equivalently **autonomous microservice with NL contract**.

Concrete differences from `src/` modules:

- **No in-process function imports** → skills compose via co-activation + NL delegation, not function-call
- **Scripts are CLI subprocesses, not importable libraries** → cross-skill code reuse impossible at language level
- **State flows via filesystem** → skills coordinate via `notes/`, KB, output files (UNIX pipe analogue)

Composition semantics are **file-based**, not function-call. This is a feature, not a limit — UNIX-style composition is battle-tested; LLM-driven NL dispatch is a feature for ambiguous user intent; file-based state already lives in CAB's `notes/` discipline.

### Skills-as-Modular-Software (End State)

Each domain-specialized skill matures into a "live, walking, iterative KB pack":

- NL instruction body (interface contract)
- Orchestration scripts (`scripts/`)
- Utility scripts (deterministic logic — equivalent of `src/` functions)
- Tailored KB cards (`references/` — programmatically curated)
- Optional verification block (machine-readable proof-of-correctness)

### KG as Systematization Map

The Knowledge Graph is the agentic OS platform's **service mesh + package registry**:

- Maps which KB cards belong in which skill's `references/`
- Maps which skills compose into which agent (`governs` / `embodies` edges)
- Tracks bi-temporal supersession via git commit hash
- Powers stranded-doc detection (KB cards with no skill home)
- Powers skill-drift detection (skill referencing stale `source:` URL)
- Surfaces missing-card gaps the new framing requires

Phase 2F of Wave 8 designs the lightweight KG; Phases 9-11 progressively realize the KB → skill-pack repacking.

---

## Operational Caveats (planned-for in audit + repacking phases)

1. **Distinguish operational skills from domain skills.** `close-session`, `recover-session`, `commit-push-pr`, `commit`, `clean-gone` are pure procedures — no `references/` needed. The 5-axis audit framework classifies skills, not just KB cards.
2. **Preserve `source:` provenance during repacking.** When KB content moves into a skill's `references/`, its source URL + last-fetch metadata travel with it.
3. **Set a minimum-viable-skill threshold.** Skill earns its slot if (a) multi-step orchestration OR deterministic scripts AND (b) reusable domain knowledge OR verification contract. Single-step "ask the LLM nicely" tasks don't justify a skill.
4. **Cross-skill knowledge duplication policy.** Foundational shared content stays in `knowledge/`; skill-specialized derivations go in skill `references/`. KG tracks both edge types.
5. **Discoverability ↔ modularity tension.** Smaller skills = better progressive disclosure but worse description-based dispatch (more competition); larger skills = simpler dispatch but bigger context loads. Audit each skill's frontmatter for the imperative trigger pattern (Q4 #1) to mitigate.
6. **End-vision is multi-wave, not v1.** Wave 8 builds the systematization layer; Waves 9-11 progressively repack. Mature state is iterative.

---

## Strategic Reframing (Confirmed Session 39)

The original Wave 8 plan was bottom-up data engineering: "audit → schema → extractor → linking → viz." The reframed plan is top-down architecture:

| Old Phase Sequence | New Phase Sequence |
|---|---|
| audit (frontmatter coverage only) → schema → extractor → linking → viz | vision anchor → tiered content audit (5-axis) → audit-informed schema → extractor → linking → viz + interaction patterns card + KB authoring rule |

Vision and audit are now upstream constraints on schema design, not downstream consequences.

### Phase Layout (Wave 8 reframed — CONSOLIDATED post scenario-analyst stress-test, Session 39)

| Phase | Scope | Sessions |
|---|---|---|
| **2A** | Vision Anchoring (this artifact + KB card update) | 0.5 (DONE Session 39) |
| **2B'** | Architectural Tier Audit + Interaction Patterns Card + KB Authoring Rule (consolidated; ~10 cards in `overview/` + `schemas/` + `prerequisites/` + design-principles + kb-conventions + component-standards; produces structured-JSON audit results + new `knowledge/reference/llm-interaction-patterns.md` + temporal-neutrality rule into `kb-conventions.md`) | 1.5 |
| **2C** | Component Tier Audit (`components/` 10 cards) | 1 |
| **2D'** | Operational + Tail Audit (consolidated; `operational-patterns/` 12 + `distribution/` + `reference/` + `implementation/` + `appendices/` ≈ 22 cards) | 1 |
| **2F** | Lightweight KG Schema Design — **Schwerpunkt**. Multi-type nodes incl. `notes-artifact` edges as *anticipated-but-unimplemented*; edge taxonomy (`depends_on`, `related`, `governs`, `embodies`, `references`, `supersedes`); bi-temporal via git commit hash; JSON substrate; `kind: "other"` escape hatch. Mandatory hand-author stress gate (5-7 entries across node types) before extractor build. | 1.5 |
| **2G** | Extractor + Indexer (`hooks/scripts/kb-graph-extract.py` + `index-kb` skill integration; produces `knowledge/_graph/index.json`) | 1 |
| **HITL gate** | Post-2G review of extractor output → user decides 2I viz scope: (a) Mermaid CLI only, (b) Mermaid + HTML stub, or (c) full Mermaid + interactive HTML (D3/Cytoscape). Decision-from-data, not from speculation. | gate, not session |
| **2I** | Visualization (scope per HITL decision; Mermaid CLI minimum; HTML may defer to Wave 9 or include in this phase per user call) | 0.5-1 |

**Total**: ~7 sessions (down from ~9-11). Wave 9 unblocks at 2I completion.

**Ship gate**: Wave 8 ships when 2G + 2I render a coherent graph from real KB data. Sessions are estimate, not contract.

### Deferred to Wave 9 (per scenario-analyst stress-test, Session 39)

- **Notes ↔ Knowledge Linking implementation** (formerly Phase 2H) — `knowledge_refs:` frontmatter field + scanner. Schema *anticipates* notes-artifact edges in 2F but does not implement field/scanner until repacking pressure validates the schema. Wave 9 adopts and ships.
- **Optional HTML interactive viz** (if HITL gate selects Mermaid-only at 2I) — may earn slot in Wave 9 or later if Mermaid signal proves insufficient.

### Audit Methodology Notes (cross-cutting 2B' / 2C / 2D')

- **Output as structured JSON, not prose** — re-scoring against future axes becomes a script, not a re-audit. (Per scenario-analyst recommendation.)
- **5-axis framework**: existence justification / programmatic actionability / skill-pack home / temporal neutrality / end-vision alignment.
- **Per-card classification**: KEEP-AS-IS / MERGE / REPACK / REWRITE / DELETE / GAP. Default-NOT-keep; require justification per axis.
- **Skills audited too, not just KB cards** — operational vs. domain skill classification + minimum-viable-skill threshold validation.

### Locked Decisions (D1-D6, Session 39)

- **D1**: end-vision artifact at `notes/end-vision-cab-2026-04-28.md` (this file)
- **D2**: officially switch to "skills-as-modular-software with KG as systematization map" (corrected metaphor: skill = UNIX coreutil + man page, not Python `src/` module)
- **D3**: 5-axis audit framework — existence justification / programmatic actionability / skill-pack home / temporal neutrality / end-vision alignment. Per-card classification: KEEP-AS-IS / MERGE / REPACK / REWRITE / DELETE / GAP. Apply moderately (default-NOT-keep; require justification per axis)
- **D4**: JSON KG substrate for MVP (`knowledge/_graph/index.json`); SQLite revisit if KB > 100 files (HydroCast likely will exceed)
- **D5**: dedicated `knowledge/reference/llm-interaction-patterns.md` card + thin cross-refs from `kb-conventions.md`, `component-standards.md`, `design-principles.md` DP1
- **D6**: invoke `strategy-pathfinder:scenario-analyst` for OODA + First Principles stress-test BEFORE `/cab:plan-implementation` formalization

### Graphiti Decision (Session 39)

**Verdict**: over-build for CAB scale. Pattern-steal, not adopt-as-is.

Patterns absorbed conceptually: bi-temporal edge validity, episode-as-provenance, hybrid retrieval (semantic + BM25 + graph traversal), prescribed + emergent ontology, incremental ingestion. Skip Neo4j, skip LLM extraction, skip MCP server. Defer Graphiti reconsideration to a future wave gated on JSONL session-archive ingestion need (LL-28 territory).

### GPT-5 Schema Reference (informational)

User-shared external schema with `project-manifest.json`, `active-plan-state.json`, `processor-run-log.jsonl`, `decisions.md`, `approval-gates.md`. Selectively absorb `processor-run-log.jsonl` pattern as a future LL-28 deliverable (machine-parseable session telemetry). No wholesale schema swap — CAB stays markdown-first for human auditability + git diffability.

---

## Cross-References

- **Architecture codification**: `knowledge/overview/architecture-philosophy.md` § "Skill Composition Model & End-Vision Architecture"
- **Original Wave 8 plan (to be archived)**: `notes/impl-plan-kb-to-kg-2026-04-24.md`
- **Wave plan**: `notes/ux-log-wave-plan-2026-04-22.md` Wave 8 (now elaborated)
- **Q4 patterns target**: `knowledge/reference/llm-interaction-patterns.md` (planned Phase 2J)
- **KB authoring rule target**: `.claude/rules/kb-conventions.md` (Phase 2K — temporal-neutrality from Session 38 cont.²)
- **Lessons-Learned referenced**: LL-29 (passive-doc insufficient), LL-30 (DP8 enforcement gap), LL-25/26/27/28 family (state-mgmt protocol layers)

---

## User Preferences (cross-cutting; captured Session 39 close 2026-04-29)

- **Data format default**: AI-digestible / RAG-embeddable / parseable (JSON / YAML / JSONL / CSV). Markdown only for genuinely prose-heavy content. User reads structured formats via tooling (e.g., VS Code JSON mind-map extensions). Historical "markdown wins for human auditability" framing is overridden. Memory ref: `feedback_data_format_ai_digestible.md`.
- **Visual-learner orientation**: prefer visualization (diagrams, mind maps, force-directed graphs, interactive HTML) over text / tables / Mermaid alone for large-scale artifacts (architectural overviews, multi-phase plans, multi-agent orchestration flows). Mermaid is the floor, not default. Phase 2I HITL gate weighs richer formats higher. Memory ref: `feedback_visual_learner_preference.md`.
- **Codification candidate**: `.claude/rules/data-format-defaults.md` global rule (Phase 2B'+ candidate).

---

## Strategic Intent: Protocol-Role Subagent Constellation (Wave 12+)

**Captured 2026-04-29 during Phase 2B' verifier-output review.** User-shared pre-v1 design intent: verifier agent is one of a planned constellation of protocol-role subagents, each composed of domain-specialized skills.

### The constellation

Each phase of the standard operating protocol gets a domain-specialist subagent:

| Protocol phase | Subagent | Composed of (illustrative) | Status |
|---|---|---|---|
| PLAN | `planner` | plan-implementation skill + analyze-architecture skill + product-design-cycle KB | Not created |
| REVIEW | `reviewer` | code-review skill + assessing-quality skill + component-standards rule | Not created |
| EXECUTE | `executor` | execute-task skill + domain-specific skill packs | Not created |
| VERIFY | `verifier` | (current implementation: ad-hoc per-invocation acceptance criteria) | **Created (pre-v1)** |
| COMMIT | `committer` | commit-push-pr skill + pre-push-state-review skill + tense-hygiene check | Not created |

### Three-layer alignment intent

1. **A-team conceptual model** — domain specialists assembled per task
2. **Full-stack product-design-cycle** — Discovery → Definition → Design → Develop → Deliver stage mapping
3. **CC extensions** — skills + agents + commands + hooks programmatically composed

…all in service of end-vision: static KB → programmatic KG → readily actionable CC extensions holistically.

### Sequencing constraint (endorsement with prerequisites)

Wave 12+ candidate. Two prerequisites:

1. **Wave 8 KG functional** — subagents need queryable composition substrate; pre-KG, agents would re-implement composition logic ad-hoc
2. **Waves 9-11 skill repacking complete** — without modular skill packs (`references/` + `scripts/` + verification blocks), the constellation has no fuel; each subagent would re-implement logic

Building pre-KG / pre-repacking is DP9 anti-pattern (top-down design imposed on under-developed primitives). The verifier-only model in operation today is the simplest viable expression of the vision; preserve and let evidence drive expansion.

### A-team × lifecycle × CC-extensions mapping (richest realization)

Each lifecycle stage = subagent role + composed skills + queryable KB cluster. Currently `prioritization-frameworks.md` + `product-design-cycle.md` + `requirements-doc-guide.md` (in `knowledge/reference/`) are advisory cards. They are **fuel for future constellation realization** — Phase 2D' tail audit should NOT auto-DELETE these even if stranded-doc-shaped today.

### Operational implications for Waves 8-11

- KG schema (Phase 2F) must support `agent` as first-class node + `composes` edges (skill → agent) + `governs` edges (subagent → protocol phase) — already covered in v2 plan §4 Phase 2F node taxonomy
- Skill repacking (Waves 9-11) should produce skill packs that are **subagent-composable** (e.g., clean references/ folders, machine-readable verification blocks)
- `knowledge/reference/` advisory cards: preserve unless redundantly covered, even if stranded today
- Don't build constellation primitives prematurely; preserve optionality

### References

- `~/.claude/projects/.../memory/project_protocol_role_subagent_constellation.md` (orchestrator memory)
- `notes/TODO.md` Wave 12+ backlog
- v2 plan §4 Phase 2F node taxonomy (KG anticipates agent + plan-task as first-class nodes)
- This file's earlier Operational Caveats #1 (operational vs domain skill classification)

---

## Status & Lifecycle

- **ACTIVE** — load on every Wave 8-11 session bootstrap (cold-start anchor)
- **Update cadence**: amend as caveats are validated/invalidated by audit + repacking work
- **Supersession**: when full vision is realized (long-horizon — multi-wave, not v1) OR when subsequent reframing supersedes. Mark `status: SUPERSEDED` and add successor pointer.
