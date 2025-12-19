---
id: distributable-plugin
title: Distributable Plugin Project (Schema 2)
category: schemas
tags: [schema-2, plugin, distributable, project, marketplace]
summary: Complete specification for distributable plugin projects including directory structure, plugin.json schema, CLAUDE.md template, and knowledge base organization.
depends_on: [executive-summary, global-user-config]
related: [marketplace, agent-skills, subagents]
complexity: intermediate
last_updated: 2025-12-12
estimated_tokens: 800
---

# Distributable Plugin Project (Schema 2)

## Purpose

Schema 2 defines **distributable projects**—self-contained plugins that can be shared via marketplace. These include:

- Domain-specific knowledge and expertise
- Team-shared workflows and standards
- Custom commands, skills, and agents
- Project-specific integrations

## Directory Structure

```
my-custom-llm/
├── .claude-plugin/
│   └── plugin.json               # Required: marketplace metadata
│
├── CLAUDE.md                     # Project system instructions
├── README.md                     # User documentation
├── LICENSE                       # License file
├── CHANGELOG.md                  # Version history
├── .gitignore                    # Git exclusions
│
├── .mcp.json                     # MCP server configurations
│
├── commands/                     # Custom slash commands
│   ├── analyze.md
│   ├── summarize.md
│   └── research.md
│
├── agents/                       # Project-specific subagents
│   ├── domain-expert.md
│   ├── data-analyst.md
│   └── quality-reviewer.md
│
├── skills/                       # Project-specific skills
│   └── domain-expertise/
│       ├── SKILL.md
│       └── reference/
│           └── terminology.md
│
├── hooks/                        # Event handlers
│   └── hooks.json
│
├── knowledge/                    # Domain knowledge base
│   ├── INDEX.md
│   ├── core/
│   ├── reference/
│   └── examples/
│
└── docs/                         # Human documentation
    ├── setup-guide.md
    └── user-preferences-template.md
```

## plugin.json Schema

```json
{
  "name": "my-custom-llm",
  "version": "1.0.0",
  "description": "Brief description of plugin purpose",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "repository": "https://github.com/username/my-custom-llm",
  "license": "MIT",
  "keywords": ["domain", "custom-llm", "knowledge-base"]
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique identifier (kebab-case, no spaces) |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Semantic version (e.g., "1.0.0") |
| `description` | string | Brief purpose explanation |
| `author` | object | `{name, email, url}` |
| `repository` | string | Source code URL |
| `license` | string | License identifier |
| `keywords` | array | Discovery tags |

## CLAUDE.md Template

```markdown
# [Project Name]

## Purpose
[One-line description of what this custom LLM does]

## Domain
[Specific domain this serves]

## Personal Customization (Optional)
@~/.claude/my-project-preferences.md

## Knowledge Base
See `knowledge/INDEX.md` for available resources.

## Capabilities
- [Capability 1]
- [Capability 2]

## Constraints
- [What this LLM should NOT do]
- [Boundaries and limitations]

## Available Commands
- `/command-1` — Description
- `/command-2` — Description

## When to Use Specialized Agents
- **agent-name**: When to use
```

## Knowledge Base Organization

```
knowledge/
├── INDEX.md                      # Master catalog
│
├── core/                         # Essential (always reference)
│   ├── INDEX.md
│   └── [foundational files]
│
├── reference/                    # Supporting (reference as needed)
│   ├── INDEX.md
│   └── [detailed materials]
│
└── examples/                     # Calibration (sample I/O)
    ├── INDEX.md
    └── [examples]
```

### docs/ vs knowledge/

| Folder | Purpose | Audience |
|--------|---------|----------|
| `docs/` | Plugin documentation | Human users |
| `knowledge/` | Domain content | Claude |

Keep them separate—different purposes, different audiences.

## Distribution Strategy

Projects use `@imports` for optional personalization:

```markdown
# CLAUDE.md

## Core Instructions
[Self-contained, works without imports]

## Personal Customization (Optional)
@~/.claude/my-project-preferences.md
```

**Behavior**:
- If import exists → preferences loaded
- If import missing → Claude proceeds without error
- Plugin remains functional either way

## Scaffolding Command

To create this structure:

```
/new-project my-custom-llm
```

The builder will:
1. Create directory structure
2. Generate plugin.json
3. Create template CLAUDE.md
4. Set up .gitignore
5. Initialize git repository (private)

## See Also

- [Global User Config](global-user-config.md) — Schema 1
- [Marketplace](../distribution/marketplace.md) — Distribution
- [Knowledge Base Structure](../components/knowledge-base-structure.md) — KB details
