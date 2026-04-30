---
paths: "knowledge/**"
---

# Knowledge Base Conventions

- KB files MUST be ≤300 lines. Split oversized files into focused subtopics.
  - **Exception**: `knowledge/reference/**` — advisory conceptual frameworks (e.g., product-design lifecycle deep dives, requirements-doc taxonomies) may exceed 300 lines when splits would fracture cohesive content. The ≤300 line rule exists to keep *operational wrappers* skim-able during active work; reference docs are consulted on-demand and benefit from preserved depth. Splits should only occur when natural subtopic boundaries exist.
- Every KB file MUST have `source:` in YAML frontmatter citing the official reference.
- Prefer wrapper philosophy: document CAB-specific patterns and defer to official CC docs for comprehensive field listings. Wrapper files accumulate fewer errors over time (LL-11).
- Always re-fetch official CC docs in-session before modifying KB content (LL-10). Enum-type content (field values, mode lists, event counts) drifts fastest.

<!--
  ============================================================================
  2B'.5 PLACEHOLDER — Temporal-Neutrality Rule (USER TO AUTHOR)
  ============================================================================

  CONTEXT (why this rule exists):
  - Wave 8 Phase 2B' Session 40 audit (notes/audit-architectural-tier-2026-04-29.json)
    surfaced AMBIGUOUS axis on .claude/rules/component-standards.md because it carries
    inline `(LL-15)`, `(LL-21)`, `(UXL-040)`, `(UXL-039)` markers. The audit could not
    resolve to PASS/FAIL without a rule explicitly disambiguating two cases that share
    surface form but differ in semantic value:
      (a) PROVENANCE citation — "this rule exists because of LL-15" (structurally
          valuable; carries lesson-to-rule traceability that the LL-25/26/27/28
          state-management family relies on).
      (b) CAB-DEVELOPMENT-STAGE narrative — "Wave 8 introduced X", "Session 38
          added Y", "added in v2 reframe" (cruft; ages out as waves/sessions
          pass into history, polluting KB content with dated references).

  - Without disambiguation, audits trend toward over-cautious REWRITE on cards
    with provenance citations OR over-permissive KEEP on cards with stage narrative.
    Neither matches the 5-axis framework's intent.

  EDGE CASES the user should consider explicitly:
  - Wave/phase references in roadmap-context (e.g., architecture-philosophy.md
    Operational Caveats #6 says "Wave 8 onward / Waves 9-11 progressively repack").
    Currently flagged as KEEP-AS-IS-PROVISIONAL with Wave 11+ revisit. Is roadmap
    framing ACCEPTABLE in the interim, or should it be abstracted now?
  - Dated cross-refs to notes/ artifacts (e.g., "notes/end-vision-cab-2026-04-28.md").
    Dated paths become stale if artifacts are archived/superseded. Discourage,
    tolerate, or require a status-stable redirect mechanism?
  - last_updated, review_by, source-URL-with-fetch-date in frontmatter — these are
    metadata, not body content; assumed ACCEPTABLE without an explicit carve-out
    (worth confirming).
  - Wave/phase references in active-development cards (architecture-philosophy.md
    Skill Composition Model section was authored Session 39 with end-vision framing;
    references to Wave 8-11 are operationally valuable now). Distinguish from
    historical narrative?

  REFERENCES the user may cite:
  - LL-30 — DP8 enforcement gap (passive-doc insufficient; structural integration
    via skills/hooks/rules > narrative documentation)
  - 5-axis audit framework (notes/impl-plan-kb-to-kg-2026-04-28-v2.md §3) — axis 4
    "temporal_neutrality" is what this rule operationalizes
  - knowledge/reference/llm-interaction-patterns.md — sibling card (lands in same
    commit); opening blockquote pre-empts this rule by framing inline LL refs as
    PROVENANCE. Once rule lands, that blockquote becomes a worked example.
  - LL-25, LL-26, LL-27, LL-28 family — state-management lessons whose provenance
    must remain queryable (don't break their lesson-to-rule traceability).

  SUGGESTED RULE SHAPE (5-10 lines; user authors final wording):
  - Bullet-form rule following sibling conventions (300-line cap, source: required, etc.)
  - State the discipline: KB body content carries no CAB-development-stage narrative
  - Carve out provenance citations as explicitly ACCEPTABLE
  - Carve out at least the metadata + (optional) roadmap-active-context cases
  - Reference LL-30 as origin lesson
  - Optionally cite the 5-axis framework's axis 4 to anchor verdict semantics

  REPLACE THIS PLACEHOLDER + the bullet stub below with the authored rule;
  remove the comment block entirely once the rule is in place.
  ============================================================================
-->
- **Temporal-neutrality** (TODO: USER TO AUTHOR — see HTML comment above for context, edge cases, and references):
  - <!-- placeholder bullet — user authors final rule here -->

- Update `knowledge/INDEX.md` whenever KB files are added, removed, or renamed.
- **Commit message convention for tracker rows**: commits that resolve a UX-log-tracker row MUST include `[UXL-NNN]` suffix in message title (e.g., `feat(guide): add triage workflow [UXL-012]`). Enables post-commit hook to update `notes/ux-log-*.csv` row's `linked_commit` column deterministically.
- **LL ↔ tracker cross-reference convention**: when a tracker row promotes to a lessons-learned entry (`downstream_target=LL`), the LL entry's evidence section MUST reference `UXL-NNN` (origin row), and the tracker row's `orchestrator_take` MUST append `→ LL-NN` (destination). Bidirectional linkage keeps the knowledge graph reachable from either node.
