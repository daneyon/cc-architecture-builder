---
type: index
scope: operational-patterns/state-management
file_count: 5
last_updated: 2026-04-22
---

# State Management — Index

| File | Summary |
|------|---------|
| `session-lifecycle.md` | Session resumption, context loading order, compaction cascade, context health decisions |
| `context-engineering.md` | 200-line discipline, compaction mechanics, prompt cache optimization, auto memory interaction |
| `filesystem-patterns.md` | Three-tier state hierarchy, cold-start anchors, progress files, cross-session persistence |
| `bootstrap-read-pattern.md` | Cheap-to-expensive partial-read cascade, T1 boundary markers, L1 hard gate hook, escalation criteria (P3/P4 of bootstrap efficiency task) |
| `cc-memory-layer-alignment.md` | Operational mapping of CC's memory systems (CLAUDE.md + auto memory + subagent persistent memory via `memory:` frontmatter) to CAB state architecture; per-agent memory adoption matrix (UXL-022 + UXL-032) |
