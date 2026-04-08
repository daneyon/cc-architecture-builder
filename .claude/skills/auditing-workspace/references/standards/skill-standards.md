---
dimension: skills
kb_source: knowledge/components/agent-skills.md
last_verified: 2026-04-07
---

# Skill Frontmatter Audit Standards

> Source of truth: `knowledge/components/agent-skills.md`. This pack contains
> the CAB-specific delta checklist for skill quality assessment.

## Universal Criteria (all project tiers)

| # | Criterion | Check Method | Severity |
|---|-----------|-------------|----------|
| 1 | Skills in `<name>/SKILL.md` directory structure | Glob for `*/SKILL.md` | ERROR |
| 2 | `name` field: lowercase + hyphens, ≤64 chars | Read frontmatter | ERROR |
| 3 | `description` field present and non-empty | Read frontmatter | ERROR |
| 4 | Description in imperative format ("INVOKE THIS SKILL to...", "Use this to...") | Read description text | WARN |
| 5 | Description ≤250 chars (truncation limit in skill listing) | Character count | WARN |
| 6 | No reserved words in name ("anthropic", "claude") | Name validation | ERROR |

## Contextual Criteria (by project tier)

| # | Criterion | Minimal | Standard | Advanced |
|---|-----------|---------|----------|----------|
| 7 | `argument-hint` present | N/A | WARN | WARN |
| 8 | `allowed-tools` scoped (not unlimited) | N/A | INFO | WARN |
| 9 | `effort` field set | N/A | INFO | WARN |
| 10 | `agent: true` for multi-step investigative skills | N/A | INFO | WARN |
| 11 | `## See Also` or `## References` section links to KB | N/A | INFO | WARN |
| 12 | Bundled resources in `references/`, `scripts/`, `assets/` (not root) | N/A | WARN | ERROR |
| 13 | `paths:` frontmatter used for file-scoped skills | N/A | INFO | INFO |
| 14 | Invocation control appropriate (`disable-model-invocation`, `user-invocable`) | N/A | INFO | WARN |

## Scoring Guide

| Score | What it looks like |
|-------|-------------------|
| 0 ABSENT | No skills, or SKILL.md files missing frontmatter |
| 1 MINIMAL | Skills exist with name + description but passive/vague; no argument-hint, tools unscoped |
| 2 ADEQUATE | Imperative descriptions, argument-hint present, most fields populated |
| 3 EXEMPLARY | Imperative descriptions ≤250 chars, allowed-tools scoped, effort set, agent:true where appropriate, references section, bundled resources organized |
