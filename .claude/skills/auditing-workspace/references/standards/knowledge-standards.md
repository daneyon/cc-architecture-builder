---
dimension: knowledge
kb_source: knowledge/components/knowledge-base-structure.md
last_verified: 2026-04-07
---

# Knowledge Structure Audit Standards

> Source of truth: `knowledge/components/knowledge-base-structure.md`. This
> pack contains the CAB-specific delta checklist for knowledge base quality.
> CC has no built-in RAG — knowledge must be explicitly organized for
> grep/glob/read discovery.

## Universal Criteria (all project tiers)

| # | Criterion | Check Method | Severity |
|---|-----------|-------------|----------|
| 1 | `knowledge/INDEX.md` exists if knowledge dir present | Glob | ERROR |
| 2 | INDEX.md lists all KB files with summaries | Cross-check INDEX vs actual files | WARN |
| 3 | No credentials or proprietary data in KB | Grep for sensitive patterns | ERROR |

## Contextual Criteria (by project tier)

| # | Criterion | Minimal | Standard | Advanced |
|---|-----------|---------|----------|----------|
| 4 | KB files have YAML frontmatter (id, tags, summary) | N/A | WARN | ERROR |
| 5 | `depends_on` / `related` fields in frontmatter | N/A | INFO | WARN |
| 6 | `source:` field for provenance tracking | N/A | INFO | WARN |
| 7 | `confidence:` rating (A/B/C) | N/A | INFO | INFO |
| 8 | `review_by:` date for freshness tracking | N/A | INFO | WARN |
| 9 | Atomic file sizing (≤300 lines per file) | N/A | INFO | WARN |
| 10 | No orphan KB files (every file referenced by an extension) | N/A | WARN | ERROR |
| 11 | No dead references (extension refs point to existing KB files) | N/A | WARN | ERROR |
| 12 | INDEX `file_count` matches actual file count | N/A | WARN | ERROR |
| 13 | Sub-INDEX files for subdirectories with >5 files | N/A | N/A | INFO |
| 14 | CLAUDE.md references knowledge INDEX for discovery | N/A | WARN | WARN |

## Scoring Guide

| Score | What it looks like |
|-------|-------------------|
| 0 ABSENT | No knowledge directory, or exists without INDEX |
| 1 MINIMAL | Knowledge dir + INDEX exists but INDEX is incomplete; files lack frontmatter |
| 2 ADEQUATE | INDEX accurate, most files have frontmatter, no orphans or dead refs |
| 3 EXEMPLARY | Full frontmatter (id, tags, summary, source, confidence, review_by), INDEX integrity verified, atomic sizing, no orphans/dead refs, CLAUDE.md references INDEX |
