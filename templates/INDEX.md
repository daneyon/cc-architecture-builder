---
type: index
scope: templates
last_updated: 2026-04-05
---

# Templates Index

> Starter templates for scaffolding Claude Code projects and components.
> All templates use B+ Tiered Progressive Disclosure: required fields active,
> common fields commented, advanced fields in compact reference blocks.

## Overview

Templates use `{{PLACEHOLDER}}` syntax for values that should be customized during project/component creation.

## Available Templates

### Global User Configuration

Location: `global/`

| Template | Purpose |
|----------|---------|
| `CLAUDE.md.template` | Personal baseline system instructions |
| `settings.local.json.template` | Local settings overrides |

### Plugin Project

Location: `plugin/`

| Template | Purpose |
|----------|---------|
| `plugin.json.template` | Plugin manifest — metadata, component paths, userConfig |
| `CLAUDE.md.template` | Project seed instructions (target: <200 lines) |
| `settings.json.template` | Project settings — model, agent, permissions, hooks |
| `README.md.template` | User documentation |

### Components

| Template | Location | Purpose |
|----------|----------|---------|
| `SKILL.md.template` | `skill.template/` | Agent skill definition (13 fields, B+ tiered) |
| `agent.md.template` | `agent.template/` | Subagent definition (16 fields, B+ tiered) |
| `command.md.template` | `command.template/` | Custom slash command (legacy — prefer skills) |
| `hooks.json.template` | `templates/` root | Event-driven hooks (4 types, 26 events) |

## Placeholder Convention

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{PROJECT_NAME}}` | Project identifier (kebab-case) | `my-assistant` |
| `{{PROJECT_TITLE}}` | Human-readable project name | `My Assistant` |
| `{{DESCRIPTION}}` | Brief description | `Helps with X` |
| `{{AUTHOR_NAME}}` | Author's name | `Jane Doe` |
| `{{SKILL_NAME}}` | Skill identifier | `processing-pdfs` |
| `{{AGENT_NAME}}` | Agent identifier | `code-reviewer` |
| `{{COMMAND_NAME}}` | Command identifier | `analyze` |

## Usage

Templates are used by:

- `/new-project` — Uses `plugin/` templates
- `/new-global` — Uses `global/` templates
- `/add-skill` — Uses `skill.template/`
- `/add-agent` — Uses `agent.template/`
- `/add-command` — Uses `command.template/` (legacy — recommend `/add-skill` instead)

## Customization

To modify default templates:

1. Edit template files directly
2. Adjust placeholders as needed
3. Add/remove sections

Changes affect all future scaffolded projects/components.
