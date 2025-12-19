# CC Architecture Builder - Setup Guide

## Overview

CC Architecture Builder is a Claude Code plugin that helps you create properly structured Claude Code projects following standardized architecture patterns.

## Prerequisites

Before using this plugin, ensure you have:

1. **Claude Code CLI** installed and authenticated
2. **Git** installed and configured
3. **GitHub CLI** (optional, for repository creation)

## Installation

### Option 1: Local Installation (Development)

```bash
# Clone or download to local directory
cd /path/to/cc-architecture-builder

# Add as local marketplace for testing
claude
/plugin marketplace add ./
/plugin install cc-architecture-builder
```

### Option 2: From Marketplace (When Published)

```bash
claude
/plugin marketplace add {{MARKETPLACE_URL}}
/plugin install cc-architecture-builder
```

## Quick Start

### Create a New Project

```bash
claude
/new-project
```

Follow the interactive prompts to:
1. Name your project
2. Describe its purpose
3. Choose complexity level
4. Set distribution intent

### Add Components

```bash
/add-skill          # Add a new skill
/add-agent          # Add a new subagent
/add-command        # Add a new slash command
```

### Validate Structure

```bash
/validate           # Check project structure
/validate --full    # Full validation
/validate --prepublish  # Pre-publication check
```

## Available Commands

| Command | Description |
|---------|-------------|
| `/new-project` | Create new plugin project |
| `/new-global` | Set up global user config |
| `/add-skill` | Add skill to project |
| `/add-agent` | Add agent to project |
| `/add-command` | Add command to project |
| `/validate` | Validate project structure |
| `/kb-index` | Regenerate knowledge INDEX files |

## Knowledge Base

The plugin includes comprehensive documentation in `knowledge/`:

- `overview/` — Architecture concepts
- `prerequisites/` — Setup requirements
- `schemas/` — Structure specifications
- `components/` — Component deep dives
- `distribution/` — Publishing guidance
- `operational-patterns/` — Advanced workflows
- `implementation/` — Step-by-step guides

## Getting Help

- Ask for architecture advice (uses `architecture-advisor` agent)
- Check `knowledge/INDEX.md` for documentation navigation
- Run `/validate` to identify issues

## Configuration

### Personal Preferences

Create `~/.claude/cc-architect-preferences.md` to customize:
- Default project complexity
- Preferred templates
- Common configurations

### Project-Level

Each created project includes customizable:
- `CLAUDE.md` — Project instructions
- `plugin.json` — Metadata
- Component templates

## Security Notes

- All projects are scaffolded with security defaults
- Git repositories are created **private by default**
- `.gitignore` excludes sensitive files
- Run `/validate --security` before publishing
