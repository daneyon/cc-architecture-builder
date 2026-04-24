---
dimension: agents
kb_source: knowledge/components/subagents.md
last_verified: 2026-04-22
---

# Agent Frontmatter Audit Standards

> Source of truth: `knowledge/components/subagents.md` + `knowledge/operational-patterns/multi-agent/agent-resolution.md` (precedence + shadowing). This pack contains the CAB-specific delta checklist for agent quality assessment.

## Universal Criteria (all project tiers)

| # | Criterion | Check Method | Severity |
|---|-----------|-------------|----------|
| 1 | Agent files are `.md` in correct location: `agents/` (plugin) or `.claude/agents/` (standalone) | Glob pattern match per `project_type` | ERROR |
| 2 | `name` field present (lowercase + hyphens) | Grep frontmatter | ERROR |
| 3 | `description` field present and non-empty | Grep frontmatter | ERROR |
| 4 | Description includes auto-delegation cue ("Use when...", "Use PROACTIVELY...") | Read description content | WARN |
| 5 | No invalid field names (`allowedTools`, `context:`, `disallowed-tools`) | Grep for known-invalid fields | ERROR |
| 6 | `tools` field uses correct name (not `allowedTools`) | Grep frontmatter | ERROR |
| 7 | `model` field valid if present (`sonnet`, `opus`, `haiku`, `inherit`, or full ID) | Read + validate value | WARN |
| **15** | **No plugin↔global shadow (LL-27): for each plugin agent, verify no same-named file at `~/.claude/agents/`** | **Bash shadow scan — see `knowledge/operational-patterns/multi-agent/agent-resolution.md` §Detection** | **WARN (escalates to ERROR if content diverged AND no documented intentional-override block in the global file)** |

## Contextual Criteria (by project tier)

| # | Criterion | Minimal | Standard | Advanced |
|---|-----------|---------|----------|----------|
| 8 | `effort` field set | N/A | INFO | WARN |
| 9 | `## Verification` section in body | N/A | WARN | ERROR |
| 10 | `tools` scoped (not unlimited) | N/A | INFO | WARN |
| 11 | Body contains structured instructions (not vague) | N/A | INFO | WARN |
| 12 | `permissionMode` appropriate if set | N/A | INFO | WARN |
| 13 | `memory` field configured for persistent agents | N/A | N/A | INFO |
| 14 | No plugin-restricted fields in plugin agents (`hooks`, `mcpServers`, `permissionMode`) | ERROR | ERROR | ERROR |

## Scoring Guide

| Score | What it looks like |
|-------|-------------------|
| 0 ABSENT | No agents defined, or agents outside expected location (`agents/` for plugin, `.claude/agents/` for standalone) |
| 1 MINIMAL | Agents exist with name + description only; missing tools, effort, verification |
| 2 ADEQUATE | Good frontmatter coverage (6+ fields), description has delegation cue, no invalid fields, no shadows (or shadows are documented intentional overrides) |
| 3 EXEMPLARY | All applicable fields set, `## Verification` section, scoped tools, effort configured, no invalid fields, no shadows at any scope, description is specific and actionable |

**Shadow gating**: a plugin project with ANY unresolved shadow (no documented
override rationale) cannot reach EXEMPLARY on Agent Frontmatter dimension
regardless of per-file frontmatter quality. LL-27 enforcement is a
structural gate, not a point deduction. See
`knowledge/operational-patterns/multi-agent/agent-resolution.md` for the
full detection + remediation patterns this audit applies.
