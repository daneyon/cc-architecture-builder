---
paths: "knowledge/**"
---

# Knowledge Base Conventions

> These rules operationalize the LLM-interaction patterns documented in [`knowledge/reference/llm-interaction-patterns.md`](../../knowledge/reference/llm-interaction-patterns.md) — consult that card for the underlying mechanics (attention, retrieval, invocation, authoring discipline, ontology, verification) these rules enforce.

- KB files MUST be ≤300 lines. Split oversized files into focused subtopics.
  - **Exception**: `knowledge/reference/**` — advisory conceptual frameworks (e.g., product-design lifecycle deep dives, requirements-doc taxonomies) may exceed 300 lines when splits would fracture cohesive content. The ≤300 line rule exists to keep *operational wrappers* skim-able during active work; reference docs are consulted on-demand and benefit from preserved depth. Splits should only occur when natural subtopic boundaries exist.
- Every KB file MUST have `source:` in YAML frontmatter citing the official reference.
- Prefer wrapper philosophy: document CAB-specific patterns and defer to official CC docs for comprehensive field listings. Wrapper files accumulate fewer errors over time (LL-11).
- Always re-fetch official CC docs in-session before modifying KB content (LL-10). Enum-type content (field values, mode lists, event counts) drifts fastest.
- **Temporal-neutrality** (LL-30 origin; operationalizes 5-axis audit framework axis 4 — `notes/impl-plan-kb-to-kg-2026-04-28-v2.md` §3): KB **body content** carries no CAB-development-stage narrative. Forms like *"Wave 8 introduced X"*, *"Session 38 added Y"*, *"added in v2 reframe"* are NOT OK — they age out as waves/sessions pass into history and pollute KB content with dated references. Three explicit carve-outs:
  - **Provenance citations OK** — inline `(LL-NN)` / `(UXL-NNN)` referenced as the rule's *reason for existence* (e.g., "this rule traces to LL-15") are structurally valuable; preserves lesson-to-rule traceability that the LL-25/26/27/28 state-management family relies on. Distinction from cruft: provenance answers *"why does this rule/section exist?"*; cruft narrates *"when in CAB development was this added?"*.
  - **Frontmatter metadata OK** — `last_updated`, `review_by`, `source` URL with fetch-date, and `revision_note` are structural metadata fields, not body content; this rule does not apply to frontmatter.
  - **Wave-anchored note marker pattern** — when wave/phase context IS operationally valuable (active-development reasoning that legitimately ages with waves), wrap in a structurally queryable blockquote: `> **Wave-anchored note** (revisit at Wave N+1): ...`. Greppable; explicit deferred-revisit semantics; covers BOTH roadmap-context AND active-development cases. Replaces what would otherwise be WEAK temporal-neutrality with ACCEPTABLE structurally-deferred.
  - **Dated cross-refs to `notes/` artifacts**: discouraged in body text (paths become stale on archive/supersession); OK in `source:` provenance fields and See Also sections where the date IS the provenance. Going-forward authoring discipline — no retrofit required for existing cards.

- Update `knowledge/INDEX.md` whenever KB files are added, removed, or renamed.
- **Commit message convention for tracker rows**: commits that resolve a UX-log-tracker row MUST include `[UXL-NNN]` suffix in message title (e.g., `feat(guide): add triage workflow [UXL-012]`). Enables post-commit hook to update `notes/ux-log-*.csv` row's `linked_commit` column deterministically.
- **LL ↔ tracker cross-reference convention**: when a tracker row promotes to a lessons-learned entry (`downstream_target=LL`), the LL entry's evidence section MUST reference `UXL-NNN` (origin row), and the tracker row's `orchestrator_take` MUST append `→ LL-NN` (destination). Bidirectional linkage keeps the knowledge graph reachable from either node.
