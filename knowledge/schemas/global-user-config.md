---
id: global-user-config
title: Global User Configuration (Schema 1)
category: schemas
tags: [schema-1, global, user-config, claude-directory, personal]
summary: Complete specification for the global user configuration at ~/.claude/, including directory structure, CLAUDE.md baseline template, and settings.local.json configuration.
depends_on: [executive-summary, architecture-philosophy]
related: [distributable-plugin, memory-claudemd]
complexity: intermediate
last_updated: 2025-12-12
estimated_tokens: 700
---

# Global User Configuration (Schema 1)

## Purpose

Schema 1 defines your **personal baseline**—configuration that applies across ALL Claude Code projects. This includes:

- Communication preferences
- Default behaviors
- Personal skills available everywhere
- Private settings that shouldn't be shared

## Directory Structure

```
~/.claude/
├── CLAUDE.md                     # Personal baseline (always loaded)
├── settings.local.json           # Local settings overrides
│
├── skills/                       # Personal skills (cross-project)
│   ├── research-methodology/
│   │   └── SKILL.md
│   └── technical-writing/
│       └── SKILL.md
│
├── agents/                       # Personal subagents
│   └── general-researcher.md
│
└── shared-preferences/           # Reusable preference files
    └── project-preferences.md    # Template for project-specific prefs
```

## CLAUDE.md Template

```markdown
# Personal Configuration

## Communication Style
- [Your preferred communication approach]
- [Formatting preferences]
- [Tone and formality level]

## Default Behaviors
- [Standard behaviors you want everywhere]
- [Question-asking preferences]
- [Output format defaults]

## Response Structure Preferences
- [How you like information organized]
- [Length preferences]
- [Visual aid preferences (tables, diagrams)]

## Personal Context
[Optional: Background, expertise, common workflows]
```

### Example CLAUDE.md

```markdown
# Personal Configuration

## Communication Style
- Employ systems thinking and comprehensive analysis
- Provide structured overviews before detailed analysis
- Use natural, conversational tone unless technical analysis needed
- Minimize unnecessary formatting; prefer prose over bullet points

## Default Behaviors
- Ask clarifying questions before diving into complex tasks
- Use markdown artifacts for reference-ready materials
- Provide evidence-based reasoning with citations
- Challenge assumptions constructively

## Response Structure Preferences
- Executive summaries for complex topics
- Clear section headings for longer responses
- Actionable next steps where appropriate
- Tables for comparisons, diagrams for flows
```

## settings.local.json

```json
{
  "model": "sonnet",
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Bash(git *)",
      "Bash(npm *)",
      "Bash(python *)"
    ],
    "deny": []
  }
}
```

### Common Settings

| Setting | Description | Example Values |
|---------|-------------|----------------|
| `model` | Default model | `"sonnet"`, `"opus"`, `"haiku"` |
| `permissions.allow` | Pre-approved tools | `["Read", "Write", "Bash(git *)"]` |
| `permissions.deny` | Blocked tools | `["Bash(rm -rf *)"]` |

## Personal Skills

Skills in `~/.claude/skills/` are available in ALL projects.

**Use personal skills for**:
- Research methodologies
- Writing styles
- Analysis frameworks
- Personal productivity patterns

**Example**: `~/.claude/skills/research-methodology/SKILL.md`

```yaml
---
name: research-methodology
description: Systematic research and synthesis. Use when conducting research or analyzing sources.
---

# Research Methodology

## Instructions
1. Define scope and success criteria
2. Identify authoritative sources
3. Extract key claims with evidence
4. Cross-reference findings
5. Synthesize into coherent narrative
6. Document limitations
```

## Personal Agents

Agents in `~/.claude/agents/` are available in ALL projects.

**Use personal agents for**:
- General-purpose assistants
- Personal workflow automation
- Cross-domain utilities

## Connecting to Projects

Projects can optionally import personal preferences:

```markdown
# Project CLAUDE.md

## Project-Specific Instructions
[Main project instructions]

## Personal Preferences (Optional)
@~/.claude/shared-preferences/project-preferences.md
```

If the import file doesn't exist, Claude proceeds without error.

## See Also

- [Distributable Plugin](distributable-plugin.md) — Schema 2
- [Memory System](../components/memory-claudemd.md) — CLAUDE.md details
- [Agent Skills](../components/agent-skills.md) — Creating skills
