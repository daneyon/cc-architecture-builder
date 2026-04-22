---
paths: "knowledge/**"
---

# Knowledge Base Conventions

- KB files MUST be ≤300 lines. Split oversized files into focused subtopics.
  - **Exception**: `knowledge/reference/**` — advisory conceptual frameworks (e.g., product-design lifecycle deep dives, requirements-doc taxonomies) may exceed 300 lines when splits would fracture cohesive content. The ≤300 line rule exists to keep *operational wrappers* skim-able during active work; reference docs are consulted on-demand and benefit from preserved depth. Splits should only occur when natural subtopic boundaries exist.
- Every KB file MUST have `source:` in YAML frontmatter citing the official reference.
- Prefer wrapper philosophy: document CAB-specific patterns and defer to official CC docs for comprehensive field listings. Wrapper files accumulate fewer errors over time (LL-11).
- Always re-fetch official CC docs in-session before modifying KB content (LL-10). Enum-type content (field values, mode lists, event counts) drifts fastest.
- Update `knowledge/INDEX.md` whenever KB files are added, removed, or renamed.
- **Commit message convention for tracker rows**: commits that resolve a UX-log-tracker row MUST include `[UXL-NNN]` suffix in message title (e.g., `feat(guide): add triage workflow [UXL-012]`). Enables post-commit hook to update `notes/ux-log-*.csv` row's `linked_commit` column deterministically.
- **LL ↔ tracker cross-reference convention**: when a tracker row promotes to a lessons-learned entry (`downstream_target=LL`), the LL entry's evidence section MUST reference `UXL-NNN` (origin row), and the tracker row's `orchestrator_take` MUST append `→ LL-NN` (destination). Bidirectional linkage keeps the knowledge graph reachable from either node.
