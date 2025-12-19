---
id: agent-skills
title: Agent Skills
category: components
tags: [skills, model-invoked, SKILL.md, capabilities, progressive-disclosure]
summary: Model-invoked capabilities that Claude autonomously triggers based on task context. Covers SKILL.md format, naming requirements, and progressive disclosure patterns.
depends_on: [memory-claudemd]
related: [subagents, custom-commands]
complexity: intermediate
last_updated: 2025-12-12
estimated_tokens: 750
---

# Agent Skills

## Overview

Skills are **model-invoked** capabilities—Claude autonomously decides when to use them based on the task context and skill description. This differs from commands, which require explicit user invocation.

## Key Distinction

| Aspect | Skills | Commands |
|--------|--------|----------|
| Invocation | Model decides | User types `/command` |
| Trigger | Task context matches description | Explicit request |
| Discovery | Metadata loaded at startup | Listed in `/help` |

## File Structure

```
skills/
└── skill-name/
    ├── SKILL.md              # Required
    ├── reference/            # Optional supporting files
    │   └── detailed-guide.md
    └── scripts/              # Optional executables
        └── process.py
```

## SKILL.md Format

```yaml
---
name: skill-name
description: What this skill does and when to use it. Be specific about triggers.
---

# Skill Name

## Instructions
[Step-by-step guidance for Claude]

## When to Apply
[Specific trigger conditions]

## Output Format
[Expected structure of results]

## References
For details, see [reference/detailed-guide.md](reference/detailed-guide.md)
```

## Naming Requirements

Per official documentation:

| Field | Constraint |
|-------|------------|
| `name` | Max 64 chars |
| `name` | Lowercase letters, numbers, hyphens only |
| `name` | No XML tags |
| `name` | No reserved words ("anthropic", "claude") |
| `description` | Max 1024 chars |
| `description` | Must be non-empty |
| `description` | No XML tags |
| `description` | Third-person voice |

### Naming Convention

Use **gerund form** (verb + -ing):
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`

### Description Best Practices

```yaml
# GOOD: Specific, includes triggers
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.

# BAD: Vague
description: Helps with documents
```

## Progressive Disclosure

Skills use three-level loading to conserve tokens:

| Level | Content | When Loaded | Token Cost |
|-------|---------|-------------|------------|
| **1** | Metadata | Session start | ~100 tokens/skill |
| **2** | SKILL.md body | Skill triggered | < 5k tokens |
| **3** | Supporting files | As needed | Variable |

### Implementation

1. **Metadata always loaded**: Claude knows skill exists
2. **Instructions on trigger**: SKILL.md body read when relevant
3. **Resources on demand**: Reference files, scripts accessed as needed

Script outputs (not content) enter context—efficient for large utilities.

## Skill Locations

| Location | Scope |
|----------|-------|
| `~/.claude/skills/` | Personal (all projects) |
| `.claude/skills/` | Project (team via git) |
| `plugin/skills/` | Plugin (when installed) |

## Best Practices

1. **Keep SKILL.md under 500 lines** — Use supporting files for details
2. **Write descriptions for discovery** — Claude uses these to decide relevance
3. **Include trigger phrases** — Help Claude match to user requests
4. **Test with expected inputs** — Verify skill activates correctly
5. **Use third-person voice** — Description is injected into system prompt

## Example Skill

```yaml
---
name: analyzing-data
description: Perform statistical analysis on datasets. Use when the user asks about data analysis, statistics, trends, correlations, or has CSV/Excel files to analyze.
---

# Data Analysis

## Instructions

1. Identify data type and structure
2. Check for missing values, outliers
3. Apply appropriate statistical methods
4. Visualize results when helpful
5. Summarize findings clearly

## When to Apply

- User mentions "analyze", "statistics", "trends"
- User uploads CSV, Excel, or data files
- User asks about correlations, distributions

## Output Format

- Summary of dataset
- Key statistical measures
- Visualizations (if applicable)
- Interpretation and recommendations
```

## Skills vs Subagents

| When to Use | Skills | Subagents |
|-------------|--------|-----------|
| Adds to main context | Yes | No (separate) |
| Preserves context window | No | Yes |
| Stateless | Yes | Can resume |
| Simple capability | Preferred | Overkill |
| Complex delegation | Less suitable | Preferred |

## See Also

- [Subagents](subagents.md) — Separate context alternative
- [Custom Commands](custom-commands.md) — User-invoked alternative
- [Memory System](memory-claudemd.md) — Foundation
