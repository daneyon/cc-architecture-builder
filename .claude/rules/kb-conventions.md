---
paths: "knowledge/**"
---

# Knowledge Base Conventions

- KB files MUST be ≤300 lines. Split oversized files into focused subtopics.
- Every KB file MUST have `source:` in YAML frontmatter citing the official reference.
- Prefer wrapper philosophy: document CAB-specific patterns and defer to official CC docs for comprehensive field listings. Wrapper files accumulate fewer errors over time (LL-11).
- Always re-fetch official CC docs in-session before modifying KB content (LL-10). Enum-type content (field values, mode lists, event counts) drifts fastest.
- Update `knowledge/INDEX.md` whenever KB files are added, removed, or renamed.
