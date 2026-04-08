---
dimension: rules
kb_source: knowledge/components/memory-claudemd.md
last_verified: 2026-04-07
---

# Rules Coverage Audit Standards

> Source of truth: `knowledge/components/memory-claudemd.md` (Project Rules
> section). Rules are `.md` files in `.claude/rules/` auto-loaded at session
> start as part of the Project scope.

## Universal Criteria (all project tiers)

| # | Criterion | Check Method | Severity |
|---|-----------|-------------|----------|
| 1 | Rules in `.claude/rules/` (not root-level `rules/`) | Glob pattern match | ERROR |
| 2 | Files are `.md` format | File extension check | ERROR |
| 3 | No credentials or secrets in rule files | Grep for key/token/secret patterns | ERROR |
| 4 | Rules don't duplicate CLAUDE.md content verbatim | Compare content overlap | WARN |

## Contextual Criteria (by project tier)

| # | Criterion | Minimal | Standard | Advanced |
|---|-----------|---------|----------|----------|
| 5 | `paths:` frontmatter for file-scoped rules | N/A | INFO | WARN |
| 6 | Code style rules present (language-specific conventions) | N/A | INFO | WARN |
| 7 | Security policy rules present | N/A | N/A | WARN |
| 8 | Domain-specific rules present | N/A | INFO | WARN |
| 9 | Interaction/communication rules present | N/A | N/A | INFO |
| 10 | Rules organized in subdirectories for clarity | N/A | N/A | INFO |
| 11 | Rules are concise (policy, not prose — each ≤50 lines) | N/A | INFO | WARN |

## Scoring Guide

| Score | What it looks like |
|-------|-------------------|
| 0 ABSENT | No rules directory or no rule files |
| 1 MINIMAL | Rules exist but unstructured, no scoping, may duplicate CLAUDE.md |
| 2 ADEQUATE | Organized rules with relevant policies, some `paths:` scoping |
| 3 EXEMPLARY | Well-organized subdirectories, `paths:` scoping on file-specific rules, covers code style + security + domain, concise policy format, no duplication with CLAUDE.md |
