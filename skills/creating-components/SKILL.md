---
name: creating-components
description: >-
  Scaffold individual CC components (skills, agents, commands, hooks) with proper
  frontmatter, naming, and template compliance. Triggers: add skill, add agent,
  create command, add hook, extend project with new component.
argument-hint: "Component type and name (e.g., 'skill analyzing-data' or 'agent code-reviewer')"
allowed-tools: Read, Write, Edit, Glob
effort: medium
---

# Component Creation

## Overview

This skill helps create properly structured Claude Code components (skills, agents, commands, hooks) following official specifications.

## Instructions

### Identify Component Type

| Component | User Says | Invocation | Purpose |
|-----------|-----------|------------|---------|
| Skill | "add skill", "create capability" | Model-invoked | Procedural knowledge |
| Agent | "add agent", "create assistant" | Model/user | Specialized delegation |
| Command | "add command", "create shortcut" | User-invoked | Explicit shortcuts |
| Hook | "add hook", "add automation" | Event-driven | Automated actions |

### Creating a Skill

1. **Gather information**:
   - Skill name (gerund form: `analyzing-data`)
   - What it does (for description)
   - When to trigger (for description)
   - Key instructions

2. **Create structure** (detect project type first):
   ```bash
   # Plugin project (has .claude-plugin/plugin.json):
   mkdir -p skills/{{skill-name}}
   # Standalone project:
   mkdir -p .claude/skills/{{skill-name}}
   ```

3. **Generate SKILL.md** from template:
   ```yaml
   ---
   name: {{skill-name}}
   description: {{what-it-does}}. Use when {{trigger-conditions}}.
   ---
   
   # {{Skill Title}}
   
   ## Instructions
   {{step-by-step-guidance}}
   
   ## When to Apply
   {{trigger-conditions-detailed}}
   
   ## Output Format
   {{expected-output-structure}}
   ```

4. **Validate**: Check naming rules (max 64 chars, lowercase+hyphens only)

### Creating an Agent

1. **Gather information**:
   - Agent name (lowercase-hyphens)
   - Specialization/purpose
   - Tools needed (or inherit all)
   - Model preference (sonnet/opus/haiku/inherit)

2. **Generate agent file** in `agents/`:
   ```yaml
   ---
   name: {{agent-name}}
   description: {{specialization}}. Use when {{delegation-triggers}}.
   tools: {{tool-list or omit}}
   model: {{model-alias or omit}}
   ---
   
   # {{Agent Title}}
   
   You are a specialized agent for {{purpose}}.
   
   ## Approach
   {{methodology}}
   
   ## Constraints
   {{boundaries}}
   
   ## Output Format
   {{expected-output}}
   ```

### Creating a Command

1. **Gather information**:
   - Command name (what user types after `/`)
   - What it does
   - Arguments needed
   - Tools to restrict (optional)

2. **Generate command file** in `commands/`:
   ```yaml
   ---
   description: {{brief-description-for-help}}
   allowed-tools: {{tool-list or omit}}
   ---
   
   # {{Command}} Instructions
   
   {{what-claude-should-do}}
   
   ## Arguments
   User provided: $ARGUMENTS
   First argument: $1
   Second argument: $2
   ```

### Creating a Hook

1. **Gather information**:
   - Event to hook (PreToolUse, PostToolUse, etc.)
   - Matcher pattern (which tools/actions)
   - Action type (command, validation, notification)
   - Script or command to run

2. **Update hooks/hooks.json**:
   ```json
   {
     "hooks": {
       "{{Event}}": [
         {
           "matcher": "{{pattern}}",
           "hooks": [
             {
               "type": "command",
               "command": "{{script-path}}"
             }
           ]
         }
       ]
     }
   }
   ```

## Validation Checks

After creating any component:

| Component | Validation |
|-----------|------------|
| Skill | Name ≤64 chars, lowercase+hyphens, description ≤1024 chars |
| Agent | Name unique, tools valid if specified |
| Command | File in commands/ (plugin) or .claude/commands/ (standalone), description present |
| Hook | Valid event name, script exists and executable |

## Templates Reference

- `templates/skill.template/SKILL.md.template`
- `templates/agent.template/agent.md.template`
- `templates/command.template/command.md.template`

## See Also

- `knowledge/components/agent-skills.md` — Skill deep dive
- `knowledge/components/subagents.md` — Agent deep dive
- `knowledge/components/custom-commands.md` — Command deep dive
- `knowledge/components/hooks.md` — Hooks deep dive
