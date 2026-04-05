---
name: quick-scaffold
description: >
  INVOKE THIS SKILL for fast, no-questionnaire scaffolding of Claude Code
  configurations. Triggers: quick setup, generate CLAUDE.md, scaffold structure
  fast, create template, placeholder files. Unlike scaffolding-projects, skips
  interactive discovery — user already knows what they want. Template-driven,
  user refines afterward.
argument-hint: "Scaffold target (e.g., 'global config', 'project plugin', 'skill template', 'CLAUDE.md')"
allowed-tools: Read, Write, Glob
---

# Quick Scaffold

Generate Claude Code configuration scaffolding aligned with the CAB base architecture.

## When to Use

- User already knows what they want
- Quick setup of new project structure
- Generating component templates to customize
- Creating placeholder files for iterative refinement

## Scaffolding Options

### 1. Global User Config (`~/.claude/`)

```
~/.claude/
├── CLAUDE.md                     # Personal baseline
├── settings.json                 # User settings
├── rules/                        # Personal modular rules
│   └── .gitkeep
├── skills/                       # Personal skills
│   └── .gitkeep
└── agents/                       # Personal agents
    └── .gitkeep
```

### 2. Project Plugin Config

```
project/
├── .claude-plugin/
│   └── plugin.json               # Marketplace metadata
├── CLAUDE.md                     # Project instructions
├── .claude/
│   ├── rules/                    # Modular project rules
│   └── skills/                   # Project skills
├── .mcp.json                     # MCP configurations
├── commands/                     # Slash commands
├── agents/                       # Subagents
├── hooks/
│   └── hooks.json                # Event handlers
├── knowledge/
│   └── INDEX.md                  # Knowledge base entry
└── docs/
    └── README.md
```

## Templates

### Global CLAUDE.md Template

```markdown
# Personal Configuration

## Communication Style
- [Your preferred communication patterns]
- [Response structure preferences]
- [Formatting preferences]

## Default Behaviors
- [Cross-project behaviors]
- [Tool usage preferences]

## Personal Context
- [Background, expertise areas]
- [Common workflows]

## Optional Project Customization
@~/.claude/rules/preferences.md
```

### Project CLAUDE.md Template

```markdown
# [Project Name]

## Role
You are a [domain] specialist working on [project purpose].

## Project Overview
[Brief description of what this project does]

## Key Workflows
1. [Primary workflow]
2. [Secondary workflow]
3. [Tertiary workflow]

## Technical Context
- Language/Framework: [tech stack]
- Key directories: [important paths]
- Build/Run: [common commands]

## Constraints
- [Project-specific constraints]
- [Quality standards]

## Knowledge Base
@knowledge/INDEX.md

## Personal Customization (Optional)
@~/.claude/project-preferences.md
```

### plugin.json Template

```json
{
  "name": "[project-name]",
  "version": "0.1.0",
  "description": "[Project description]",
  "author": {
    "name": "[Your Name]"
  },
  "repository": "[repo-url]",
  "keywords": [],
  "license": "MIT"
}
```

### settings.json Template (Global)

```json
{
  "model": "sonnet",
  "permissions": {
    "allow": [
      "Read",
      "Write", 
      "Edit",
      "Bash(git *)",
      "Bash(npm *)"
    ],
    "deny": []
  }
}
```

### Knowledge INDEX.md Template

```markdown
# Knowledge Base Index

## Core Documentation
- [Link to core docs]

## Reference Materials
- [Link to references]

## Examples
- [Link to examples]

## Templates
- [Link to templates]
```

### Skill Template

```yaml
---
name: [skill-name]
description: [What this skill does AND when to use it. Include trigger words.]
---

# [Skill Name]

## Purpose
[What this skill accomplishes]

## Instructions
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Examples
[Concrete examples]
```

### Agent Template

```yaml
---
name: [agent-name]
description: [When to invoke this agent]
tools: Read, Grep, Glob
model: sonnet
---

# [Agent Name]

You are a specialized agent focused on [purpose].

## Approach
1. [Step 1]
2. [Step 2]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Output Format
[Expected output structure]
```

### Command Template

```markdown
---
description: [Brief description for /help]
allowed-tools: Read, Write
---

# [Command Name]

[Instructions for what Claude should do]

## Arguments
$ARGUMENTS contains: [expected input]

## Steps
1. [Step 1]
2. [Step 2]

## Output
[Expected output format]
```

### hooks.json Template

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'File modified: $FILE_PATH'"
          }
        ]
      }
    ]
  }
}
```

### .mcp.json Template

```json
{
  "mcpServers": {}
}
```

## Usage

When user requests scaffolding:

1. **Ask scope**: "Global config, project config, or specific component?"
2. **Generate**: Provide appropriate templates inline
3. **Customize**: User specifies what to fill in
4. **Create**: Only write files when user approves

## Quick Commands

| Request | Action |
|---------|--------|
| "Scaffold global config" | Generate ~/.claude/ structure |
| "Scaffold new project" | Generate full project structure |
| "Create skill template" | Generate SKILL.md template |
| "Create agent template" | Generate agent.md template |
| "Create CLAUDE.md" | Generate appropriate CLAUDE.md |

## Reference

For architecture details, see:
- `knowledge/schemas/global-user-config.md`
- `knowledge/schemas/distributable-plugin.md`
- `knowledge/overview/executive-summary.md`
