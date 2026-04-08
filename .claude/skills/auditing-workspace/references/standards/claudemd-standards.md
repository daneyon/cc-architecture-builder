---
dimension: claudemd
kb_source: knowledge/components/memory-claudemd.md
last_verified: 2026-04-07
---

# CLAUDE.md Quality Audit Standards

> Source of truth: `knowledge/components/memory-claudemd.md`. This pack
> contains the CAB-specific delta checklist for CLAUDE.md quality assessment.

## Universal Criteria (all project tiers)

| # | Criterion | Check Method | Severity |
|---|-----------|-------------|----------|
| 1 | `CLAUDE.md` exists | Glob for `CLAUDE.md` in project root | ERROR |
| 2 | Non-empty (>10 lines of content) | Read + line count | ERROR |
| 3 | States project purpose/role in first paragraph | Read first 20 lines | WARN |
| 4 | No credentials, API keys, or secrets | Grep for `API_KEY\|SECRET\|TOKEN\|PASSWORD` patterns | ERROR |
| 5 | Size discipline (≤200 lines recommended) | `wc -l CLAUDE.md` | WARN |

## Contextual Criteria (by project tier)

| # | Criterion | Minimal | Standard | Advanced |
|---|-----------|---------|----------|----------|
| 6 | Domain guidelines section | INFO | WARN | ERROR |
| 7 | Extension registry table (skills, agents, commands) | N/A | WARN | ERROR |
| 8 | Available commands table | N/A | WARN | ERROR |
| 9 | @imports for depth (not inlining everything) | N/A | INFO | WARN |
| 10 | Learned corrections / feedback loop section | N/A | INFO | WARN |
| 11 | Knowledge base references (points to INDEX) | N/A | WARN | ERROR |
| 12 | State management section (notes/, progress) | N/A | INFO | WARN |
| 13 | Verification commands documented | N/A | WARN | ERROR |
| 14 | Seed instruction architecture (concise anchors, not prose) | N/A | INFO | WARN |

## Scoring Guide

| Score | What it looks like |
|-------|-------------------|
| 0 ABSENT | No CLAUDE.md, or empty file |
| 1 MINIMAL | CLAUDE.md exists with basic project description, no structure |
| 2 ADEQUATE | Has purpose, domain guidelines, some extension references; minor gaps |
| 3 EXEMPLARY | Seed instruction architecture, extension registry, @imports for depth, ≤200 lines, learned corrections section, verification commands |
