---
id: agent-skills
title: Agent Skills
category: components
tags: [skills, model-invoked, SKILL.md, capabilities, progressive-disclosure, scripts, references, assets]
summary: Model-invoked capabilities that Claude autonomously triggers based on task context. Covers SKILL.md format, frontmatter fields, bundled resources, progressive disclosure, and creation workflow.
depends_on: [memory-claudemd]
related: [subagents, custom-commands, mcp-integration]
complexity: intermediate
last_updated: 2025-12-18
estimated_tokens: 1200
source: Updated based on Anthropic skill-creator reference skill
---

# Agent Skills

## Overview

Skills are **model-invoked** capabilities—Claude autonomously decides when to use them based on the task context and skill description. This differs from commands, which require explicit user invocation.

> **Core Philosophy**: The context window is a public good. Skills share context with everything else Claude needs. Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this?"

## Key Distinction

| Aspect | Skills | Commands |
|--------|--------|----------|
| Invocation | Model decides | User types `/command` |
| Trigger | Task context matches description | Explicit request |
| Discovery | Metadata loaded at startup | Listed in `/help` |

## Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md              # Required
│   ├── YAML frontmatter  # name, description (required)
│   └── Markdown body     # Instructions (required)
└── Bundled Resources     # Optional
    ├── scripts/          # Executable code (Python/Bash/etc.)
    ├── references/       # Documentation loaded into context as needed
    └── assets/           # Files used in output (templates, images, fonts)
```

## SKILL.md Format

### Frontmatter (Required)

```yaml
---
name: skill-name
description: What this skill does and when to use it. Be specific about triggers. Third-person voice.
---
```

**Allowed frontmatter properties** (per validation):

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier (max 64 chars, lowercase+hyphens) |
| `description` | Yes | What skill does and when to use (max 1024 chars) |
| `license` | No | License reference (e.g., "Complete terms in LICENSE.txt") |
| `allowed-tools` | No | Restrict which tools the skill can use |
| `metadata` | No | Custom metadata object |

### Body (Required)

```markdown
# Skill Name

## Overview
[1-2 sentences explaining what this skill enables]

## Instructions
[Step-by-step guidance for Claude]

## When to Apply
[Specific trigger conditions - though better in description]

## Output Format
[Expected structure of results]

## References
For details, see [reference/detailed-guide.md](reference/detailed-guide.md)
```

## Bundled Resources

### scripts/ — Executable Code

For tasks requiring deterministic reliability or frequently rewritten code.

- **When to include**: Same code being rewritten repeatedly, or deterministic reliability needed
- **Benefits**: Token efficient, deterministic, executed without loading into context
- **Note**: Scripts may still be read by Claude for patching or environment adjustments

### references/ — Documentation

Documentation intended to be loaded into context as needed.

- **When to include**: Documentation Claude should reference while working
- **Use cases**: Database schemas, API docs, domain knowledge, detailed guides
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Information should live in SKILL.md OR references files, not both

### assets/ — Output Files

Files not loaded into context, but used in output Claude produces.

- **When to include**: Files used in final output
- **Examples**: Templates (.pptx, .docx), images, icons, fonts, boilerplate code
- **Benefits**: Claude can use files without loading them into context

## What NOT to Include in Skills

> **Important**: Skills are for AI agents, not human users.

Do NOT create extraneous documentation:
- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- User documentation

The skill should only contain information needed for an AI agent to do the job.

## Naming Requirements

| Field | Constraint |
|-------|------------|
| `name` | Max 64 chars |
| `name` | Lowercase letters, numbers, hyphens only |
| `name` | Cannot start/end with hyphen or contain `--` |
| `name` | No reserved words ("anthropic", "claude") |
| `description` | Max 1024 chars, non-empty |
| `description` | No angle brackets (< or >) |
| `description` | Third-person voice |

### Naming Convention

Use **gerund form** (verb + -ing):
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`

### Description Best Practices

```yaml
# GOOD: Specific, includes all trigger information
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.

# BAD: Vague, no triggers
description: Helps with documents
```

**Include ALL "when to use" information in the description** — not in the body. The body is only loaded after triggering, so "When to Use" sections in the body don't help Claude decide.

## Progressive Disclosure

Skills use three-level loading to conserve tokens:

| Level | Content | When Loaded | Token Cost |
|-------|---------|-------------|------------|
| **1** | Metadata (name + description) | Session start | ~100 tokens/skill |
| **2** | SKILL.md body | Skill triggered | < 5k words |
| **3** | Bundled resources | As needed | Unlimited (scripts execute without loading) |

### Progressive Disclosure Patterns

**Pattern 1: High-level guide with references**
```markdown
# PDF Processing

## Quick start
[Basic instructions with code example]

## Advanced features
- **Form filling**: See [references/forms.md](references/forms.md)
- **API reference**: See [references/api.md](references/api.md)
```

**Pattern 2: Domain-specific organization**
```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── references/
    ├── finance.md (revenue, billing)
    ├── sales.md (opportunities, pipeline)
    └── product.md (API usage, features)
```
When user asks about sales, Claude only reads sales.md.

**Pattern 3: Framework/variant organization**
```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

**Guidelines:**
- Avoid deeply nested references (keep one level deep from SKILL.md)
- Structure longer reference files with table of contents at top
- Keep SKILL.md body under 500 lines

## Degrees of Freedom

Match specificity to task fragility:

| Level | When to Use | Form |
|-------|-------------|------|
| **High freedom** | Multiple approaches valid, context-dependent | Text instructions |
| **Medium freedom** | Preferred pattern exists, some variation OK | Pseudocode, scripts with parameters |
| **Low freedom** | Operations fragile, consistency critical | Specific scripts, few parameters |

Think of Claude as exploring a path: a narrow bridge needs guardrails (low freedom), an open field allows many routes (high freedom).

## Skill Creation Process

1. **Understand** — Gather concrete usage examples
2. **Plan** — Identify reusable resources (scripts, references, assets)
3. **Initialize** — Create skill structure (use init script if available)
4. **Edit** — Implement resources, write SKILL.md
5. **Package** — Create distributable .skill file
6. **Iterate** — Improve based on real usage

## Skill Locations

| Location | Scope |
|----------|-------|
| `~/.claude/skills/` | Personal (all projects) |
| `.claude/skills/` | Project (team via git) |
| `plugin/skills/` | Plugin (when installed) |

## Skills vs Subagents

| When to Use | Skills | Subagents |
|-------------|--------|-----------|
| Adds to main context | Yes | No (separate) |
| Preserves context window | No | Yes |
| Stateless | Yes | Can resume |
| Simple capability | Preferred | Overkill |
| Complex delegation | Less suitable | Preferred |

## Packaging Skills

Skills can be packaged into `.skill` files (zip format) for distribution:

```bash
# Using skill-creator scripts
python scripts/package_skill.py path/to/skill-folder

# Creates: skill-name.skill
```

The packaging script validates before creating the package.

## See Also

- [Subagents](subagents.md) — Separate context alternative
- [Custom Commands](custom-commands.md) — User-invoked alternative
- [Memory System](memory-claudemd.md) — Foundation
- Anthropic skill-creator skill — Detailed skill creation guidance
