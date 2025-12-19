# Claude Code Architecture Guide

## A Comprehensive Framework for Custom LLM Development

<!-- DOCUMENT METADATA (Machine-Readable) -->
<!--
status: DRAFT
version: 0.3.0
author: Daneyon (with Claude)
last_updated: 2025-12-12
document_type: architecture_guide
primary_audience: [human, llm]
sections_complete: [executive_summary, architecture_philosophy, prerequisites_git, schema_1, schema_2, components, distribution, operational_patterns, implementation]
sections_in_progress: []
sections_placeholder: [sdk_integration, enterprise_deployment, advanced_mcp, cicd, kb_deep_dive, agents_deep_dive]
pending_reviews: [skill-creator, mcp-builder]
-->

> **DRAFT STATUS**: This is a living document under active development. Sections marked with `[PLACEHOLDER]` are incomplete. Last substantive edit: December 12, 2025.

**Version**: 0.3.0-draft  
**Author**: Daneyon (with Claude)  
**Last Updated**: December 12, 2025

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Architecture Philosophy](#2-architecture-philosophy)
3. [Prerequisites & Git Foundation](#3-prerequisites--git-foundation)
4. [Schema 1: Global User Configuration](#4-schema-1-global-user-configuration)
5. [Schema 2: Distributable Plugin Project](#5-schema-2-distributable-plugin-project)
6. [Component Deep Dives](#6-component-deep-dives)
   - 6.1 [Memory System (CLAUDE.md)](#61-memory-system-claudemd)
   - 6.2 [Agent Skills](#62-agent-skills)
   - 6.3 [Subagents](#63-subagents)
   - 6.4 [Custom Commands](#64-custom-commands)
   - 6.5 [Hooks](#65-hooks)
   - 6.6 [MCP Integration](#66-mcp-integration)
   - 6.7 [Knowledge Base Structure](#67-knowledge-base-structure)
7. [Distribution & Marketplace](#7-distribution--marketplace)
8. [Operational Patterns](#8-operational-patterns)
   - 8.1 [Git Worktree Parallel Execution](#81-git-worktree-parallel-execution)
   - 8.2 [Session Management](#82-session-management)
   - 8.3 [Multi-Agent Collaboration](#83-multi-agent-collaboration)
9. [Implementation Workflow](#9-implementation-workflow)
10. [Future Enhancements](#10-future-enhancements-placeholders)
    - 10.1 [SDK & Programmatic Integration](#101-sdk--programmatic-integration-placeholder)
    - 10.2 [Enterprise Deployment](#102-enterprise-deployment-placeholder)
    - 10.3 [Advanced MCP Development](#103-advanced-mcp-development-placeholder)
    - 10.4 [CI/CD Integration](#104-cicd-integration-placeholder)
11. [Appendix A: Glossary](#appendix-a-glossary)
12. [Appendix B: References](#appendix-b-references)
13. [Appendix C: Knowledge Base Deep Dive](#appendix-c-knowledge-base-deep-dive-placeholder) [PLACEHOLDER]
14. [Appendix D: AI Agents Deep Dive](#appendix-d-ai-agents-deep-dive-placeholder) [PLACEHOLDER]

---

## 1. Executive Summary

### Purpose

This guide establishes a standardized architecture for building custom LLM solutions using Claude Code. It addresses the separation of concerns between **personal configuration** (global settings that travel with you) and **distributable projects** (shareable plugins with domain-specific capabilities).

### Core Insight

Claude Code is not merely a coding assistant—it is a configurable AI platform with filesystem access, tool integration, and extensible capabilities. This architecture leverages Claude Code for any custom LLM use case: technical coding projects, research assistants, domain-specific knowledge bases, or educational tutors.

### Two-Schema Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ARCHITECTURE OVERVIEW                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  SCHEMA 1: GLOBAL USER CONFIGURATION                                        │
│  Location: ~/.claude/                                                        │
│  Purpose: Personal baseline, cross-project preferences                       │
│  Scope: Private to you, applies to ALL projects                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  ~/.claude/                                                                  │
│  ├── CLAUDE.md              # Your personal system instructions              │
│  ├── settings.local.json    # Local settings overrides                       │
│  ├── skills/                # Personal skills (available everywhere)         │
│  │   └── your-skill/                                                         │
│  │       └── SKILL.md                                                        │
│  └── agents/                # Personal agents                                │
│      └── your-agent.md                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ inherits / supplements
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  SCHEMA 2: DISTRIBUTABLE PLUGIN PROJECT                                      │
│  Location: ./your-project/                                                   │
│  Purpose: Domain-specific custom LLM, shareable via marketplace              │
│  Scope: Team/community distribution                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  your-plugin/                                                                │
│  ├── .claude-plugin/                                                         │
│  │   └── plugin.json        # Marketplace metadata                           │
│  ├── CLAUDE.md              # Project system instructions                    │
│  ├── .mcp.json              # MCP server configurations                      │
│  ├── commands/              # Custom slash commands                          │
│  ├── agents/                # Project-specific subagents                     │
│  ├── skills/                # Project-specific skills                        │
│  ├── hooks/                 # Event handlers                                 │
│  │   └── hooks.json                                                          │
│  ├── knowledge/             # Domain knowledge base                          │
│  └── docs/                  # Documentation                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Design Principles

| Principle | Description |
|-----------|-------------|
| **Separation of Concerns** | Global config stays personal; project config is distributable |
| **Progressive Disclosure** | Load only what's needed; reference additional files via `@imports` |
| **Convention over Configuration** | Follow official directory structures; minimize custom conventions |
| **Git-Native Workflow** | Version control everything; enable team collaboration |
| **Token Efficiency** | Keep CLAUDE.md concise; use skills/agents for complex instructions |

---

## 2. Architecture Philosophy

### The Memory Hierarchy

Claude Code implements a 4-tier memory hierarchy with clear precedence:

| Tier | Location | Purpose | Shared With |
|------|----------|---------|-------------|
| **1. Enterprise Policy** | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | Organization-wide standards | All org users |
| **2. User Memory** | `~/.claude/CLAUDE.md` | Personal preferences (all projects) | Just you |
| **3. Project Memory** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared instructions | Team via git |
| **4. Subtree Memory** | `./subdir/CLAUDE.md` | Directory-specific context | Team via git |

**Precedence Rule**: Files higher in the hierarchy load first and take precedence. Project-level files can supplement but not override enterprise/user policies.

### Invocation Patterns

Understanding how Claude Code components are triggered is critical:

| Component | Invocation Type | Trigger |
|-----------|-----------------|---------|
| **Memory (CLAUDE.md)** | Automatic | Always loaded at session start |
| **Skills** | Model-invoked | Claude autonomously decides based on task context |
| **Subagents** | Model or user-invoked | Auto-delegated or explicitly called |
| **Commands** | User-invoked | Explicitly typed (e.g., `/analyze`) |
| **Hooks** | Event-driven | Triggered by system events (PreToolUse, PostToolUse, etc.) |

### Distribution Philosophy

**Problem**: How do you share a complete working system while keeping global and project layers separate?

**Solution**: CLAUDE.md `@imports` enable optional personalization without bloating the plugin:

```markdown
# Project CLAUDE.md

## Core Instructions
[Self-contained project instructions]

## Personal Customization (Optional)
@~/.claude/project-preferences.md
```

- If the user creates `~/.claude/project-preferences.md`, their preferences are loaded
- If the file doesn't exist, Claude proceeds without it
- The plugin remains self-contained and functional out of the box

---

## 3. Prerequisites & Git Foundation

### Why Git is Foundational

Git is not merely recommended—it is **architecturally required** for this framework. Claude Code's design assumes git-based workflows:

| Capability | Git Dependency |
|------------|----------------|
| Plugin distribution | Marketplaces pull from git repositories |
| Team collaboration | Project CLAUDE.md and configs shared via git |
| Version control | System instructions, skills, agents all versioned |
| Parallel execution | Git worktrees enable multiple Claude Code sessions |
| GitHub MCP | Requires repository context |

### Initial Setup Checklist

```bash
# 1. Verify git installation
git --version

# 2. Configure identity (if not already done)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# 3. Create project directory
mkdir my-custom-llm && cd my-custom-llm

# 4. Initialize repository FIRST (before any Claude Code work)
git init

# 5. Create initial structure and commit
mkdir -p .claude-plugin commands agents skills knowledge docs
touch CLAUDE.md README.md .gitignore
git add .
git commit -m "Initial project structure"
```

### Recommended .gitignore

```gitignore
# Claude Code local files
.claude/settings.local.json
CLAUDE.local.md

# Environment and secrets
.env
.env.local
*.key
*.pem

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Dependencies (if applicable)
node_modules/
__pycache__/
*.pyc

# Build outputs
dist/
build/
```

### GitHub Repository Setup

For distribution, connect to GitHub:

```bash
# Create repo on GitHub first, then:
git remote add origin https://github.com/yourusername/my-custom-llm.git
git branch -M main
git push -u origin main
```

### Privacy & Security Defaults

**Critical**: Always create repositories as **private by default** during development.

```bash
# Using GitHub CLI (recommended for security)
gh repo create my-custom-llm --private --source=. --push

# Only make public after explicit review
gh repo edit my-custom-llm --visibility public
```

**Pre-publication checklist**:
- [ ] No API keys, tokens, or credentials in repository
- [ ] No personal/client data in knowledge base
- [ ] `.gitignore` excludes sensitive files (`.env`, `*.key`, etc.)
- [ ] CLAUDE.md contains no proprietary instructions you don't want shared
- [ ] Review all files for PII or confidential information

**Files that should NEVER be committed**:
```
.env                    # Environment variables
*.key, *.pem           # Cryptographic keys
settings.local.json    # Local settings overrides
CLAUDE.local.md        # Personal local instructions
credentials.json       # Any credential files
```

### GitHub MCP Integration

Connect Claude Code to GitHub for enhanced repository operations:

```bash
# Add GitHub MCP server
claude mcp add --transport http github https://api.github.com/mcp

# Verify connection
claude mcp list
```

Once connected, Claude can:
- Create and manage issues
- Open pull requests
- Search code across repositories
- Review commit history

### Git Workflow for Plugin Development

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   develop   │ ──▶ │   test      │ ──▶ │   review    │ ──▶ │   release   │
│             │     │             │     │             │     │             │
│ Feature     │     │ Local       │     │ PR + team   │     │ Tag version │
│ branches    │     │ marketplace │     │ review      │     │ Publish     │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

**Branch Strategy**:
- `main` — Stable, released versions
- `develop` — Integration branch for features
- `feature/*` — Individual feature development
- `release/*` — Release preparation

---

## 4. Schema 1: Global User Configuration

### Directory Structure

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
└── shared-knowledge/             # Reference materials (optional)
    ├── frameworks/
    │   └── llm_architecture_framework.md
    └── templates/
        └── analysis-template.md
```

### CLAUDE.md (Personal Baseline)

```markdown
# Personal Configuration

## Communication Style
- Employ systems thinking and comprehensive analysis
- Provide structured overviews before detailed analysis (tables, diagrams, mind maps)
- Balance theoretical depth with practical applicability
- Use natural, conversational tone unless technical analysis is explicitly needed
- Minimize unnecessary formatting; use prose over bullet points for explanations

## Default Behaviors
- Ask clarifying questions before diving into complex or ambiguous tasks
- Use markdown artifacts for reference-ready materials
- Provide evidence-based reasoning with citations where applicable
- Challenge assumptions constructively; maintain intellectual honesty

## Response Structure Preferences
- Executive summaries for complex topics
- Clear section headings for longer responses
- Actionable next steps where appropriate

## Personal Context
[Your background, expertise areas, common workflows—loaded for context]
```

### settings.local.json

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
  },
  "outputStyle": "detailed"
}
```

### Personal Skill Example

**Location**: `~/.claude/skills/research-methodology/SKILL.md`

```yaml
---
name: research-methodology
description: Systematic research and synthesis methodology. Use when conducting research, analyzing sources, or synthesizing information across multiple documents.
---

# Research Methodology Skill

## Instructions

1. **Define Scope**: Clarify research question, boundaries, and success criteria
2. **Source Identification**: Identify authoritative sources; prioritize primary sources
3. **Systematic Extraction**: Extract key claims, evidence, and methodologies
4. **Cross-Reference**: Validate findings across multiple sources
5. **Synthesis**: Integrate insights into coherent narrative
6. **Gap Analysis**: Identify limitations, contradictions, or areas for further research

## Output Format

Research outputs should include:
- Executive summary (1-2 paragraphs)
- Key findings organized by theme
- Evidence quality assessment
- Limitations and caveats
- Recommended next steps
```

---

## 5. Schema 2: Distributable Plugin Project

### Directory Structure

```
my-custom-llm/
├── .claude-plugin/
│   └── plugin.json               # Required: marketplace metadata
│
├── CLAUDE.md                     # Project system instructions
├── README.md                     # User documentation
├── LICENSE                       # License file
├── CHANGELOG.md                  # Version history
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
│           ├── terminology.md
│           └── standards.md
│
├── hooks/                        # Event handlers
│   └── hooks.json
│
├── knowledge/                    # Domain knowledge base
│   ├── core/                     # Essential knowledge (always reference)
│   │   └── .gitkeep
│   ├── reference/                # Supporting materials
│   │   └── .gitkeep
│   └── examples/                 # Sample inputs/outputs
│       └── .gitkeep
│
├── scripts/                      # Utility scripts for hooks
│   └── validate.sh
│
└── docs/
    ├── setup-guide.md
    └── user-preferences-template.md
```

### plugin.json

```json
{
  "name": "my-custom-llm",
  "version": "1.0.0",
  "description": "Domain-specific custom LLM with knowledge management and specialized agents",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "repository": "https://github.com/yourusername/my-custom-llm",
  "license": "MIT",
  "keywords": ["custom-llm", "domain-specific", "knowledge-base"]
}
```

### CLAUDE.md (Project)

```markdown
# [Project Name]

## Purpose
[One-line description of what this custom LLM does]

## Domain
[Specific domain this serves]

## Personal Customization (Optional)
@~/.claude/my-custom-llm-preferences.md

## Knowledge Base Structure
This project's knowledge is organized as:
- `knowledge/core/` — Essential domain knowledge (always reference)
- `knowledge/reference/` — Supporting materials (reference when relevant)
- `knowledge/examples/` — Sample inputs/outputs for calibration

## Capabilities
- [Capability 1]
- [Capability 2]
- [Capability 3]

## Constraints
- [What this LLM should NOT do]
- [Boundaries and limitations]

## Output Guidelines
[Preferred output structures, formats, quality standards]

## Available Commands
- `/analyze` — Structured analysis of provided content
- `/summarize` — Executive summary generation
- `/research` — Comprehensive research workflow

## When to Use Specialized Agents
- **domain-expert**: Complex domain-specific questions
- **data-analyst**: Quantitative analysis tasks
- **quality-reviewer**: Review and validation workflows
```

---

## 6. Component Deep Dives

### 6.1 Memory System (CLAUDE.md)

#### Overview

CLAUDE.md files serve as persistent memory—instructions that Claude reads at the start of every session. They form the foundation of custom LLM behavior.

#### Import Syntax

CLAUDE.md files can import additional files using `@path/to/file` syntax:

```markdown
# Project Instructions

See @README.md for project overview.
See @docs/architecture.md for system design.

## Personal Preferences
@~/.claude/my-preferences.md
```

**Rules**:
- Both relative and absolute paths are allowed
- Imports are recursive (max depth: 5 hops)
- Imports inside code blocks are ignored
- Use `/memory` command to see all loaded memory files

#### Best Practices

| Do | Don't |
|----|-------|
| Be specific: "Use 2-space indentation" | Be vague: "Format code properly" |
| Use bullet points for individual instructions | Write long paragraphs |
| Group related memories under headings | Mix unrelated instructions |
| Keep total length under 500 lines | Bloat with rarely-used instructions |
| Use `@imports` for detailed reference material | Inline everything |

#### Memory Lookup Behavior

Claude Code reads memories **recursively from current directory upward**:
- Starting in `foo/bar/`, Claude finds both `foo/bar/CLAUDE.md` and `foo/CLAUDE.md`
- Subtree CLAUDE.md files are loaded when Claude reads files in those subtrees

---

### 6.2 Agent Skills

#### Overview

Skills are **model-invoked** capabilities—Claude autonomously decides when to use them based on the task context and skill description. This differs from commands, which require explicit user invocation.

#### Skill Structure

```
skills/
└── my-skill/
    ├── SKILL.md              # Required: skill definition
    ├── reference.md          # Optional: additional reference
    └── scripts/              # Optional: executable scripts
        └── process.py
```

#### SKILL.md Format

```yaml
---
name: my-skill-name
description: Brief description of what this Skill does and when to use it. Include specific triggers and contexts.
---

# Skill Name

## Instructions
1. Step-by-step guidance
2. Clear procedures
3. Decision criteria

## When to Apply
- Specific contexts
- Trigger conditions
- Use case examples

## Output Format
[Expected output structure]

## References
For detailed specifications, see [reference.md](reference.md)
```

#### Naming Requirements

| Field | Requirements |
|-------|-------------|
| `name` | Max 64 chars, lowercase letters/numbers/hyphens only, no XML tags, no reserved words ("anthropic", "claude") |
| `description` | Max 1024 chars, non-empty, no XML tags, third-person voice |

#### Progressive Disclosure

Skills use a three-level loading model:

| Level | When Loaded | Token Cost | Content |
|-------|-------------|------------|---------|
| **Level 1: Metadata** | Always (startup) | ~100 tokens/skill | `name` and `description` from frontmatter |
| **Level 2: Instructions** | When skill triggered | < 5k tokens | SKILL.md body |
| **Level 3: Resources** | As needed | Effectively unlimited | Bundled files, scripts (output only) |

---

### 6.3 Subagents

#### Overview

Subagents are specialized AI assistants that operate in their **own context window**, preventing pollution of the main conversation. Claude can delegate tasks to subagents automatically or users can invoke them explicitly.

#### File Format

**Location**: `agents/` directory (project or personal)

```yaml
---
name: my-agent-name
description: Description of when this subagent should be invoked
tools: Read, Grep, Glob, WebSearch    # Optional: comma-separated list
model: sonnet                          # Optional: sonnet, opus, haiku, or 'inherit'
---

# Agent Name

You are a specialized agent focused on [specific purpose].

## Approach
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Output Format
[Expected output structure]
```

#### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase letters and hyphens) |
| `description` | Yes | When to invoke this agent (natural language) |
| `tools` | No | Comma-separated tool list; inherits all if omitted |
| `model` | No | Model alias or 'inherit'; defaults to configured subagent model |

#### Skills vs Agents Comparison

| Aspect | Skills | Subagents |
|--------|--------|-----------|
| **Invocation** | Model-invoked (automatic) | Model or user-invoked |
| **Context** | Loads into main context | Separate context window |
| **Purpose** | Procedural knowledge, capabilities | Specialized assistant, delegation |
| **State** | Stateless | Can be resumed with agentId |
| **Token Impact** | Adds to main context | Preserves main context |

#### Advanced Features

**Resumable Agents**: Subagents can be resumed to continue previous work:
```
> Resume agent abc123 and continue the analysis
```

**Chaining Agents**:
```
> Use code-analyzer to find issues, then use optimizer to fix them
```

---

### 6.4 Custom Commands

#### Overview

Commands are **user-invoked** shortcuts triggered by typing `/command-name`. They can execute instructions, reference files, run bash commands, or combine multiple actions.

#### File Format

**Location**: `commands/` directory

```markdown
---
description: Brief description shown in /help
allowed-tools: Read, Write, Bash    # Optional: restrict tools
---

# Command Instructions

Clear instructions for what Claude should do when this command is invoked.

## Steps
1. [Step 1]
2. [Step 2]

## Arguments
This command accepts: $ARGUMENTS

Individual args: $1, $2, $3
```

#### Command Types

| Type | Location | Scope |
|------|----------|-------|
| **Project Commands** | `.claude/commands/` | Current project |
| **Personal Commands** | `~/.claude/commands/` | All projects |
| **Plugin Commands** | `plugin/commands/` | When plugin installed |

#### Features

**Arguments**:
```markdown
# Command accepting arguments
User query: $ARGUMENTS
First arg: $1
Second arg: $2
```

**File References**:
```markdown
Analyze the code in @src/main.py
```

**Bash Execution**:
```markdown
Current branch: !git branch --show-current!
```

**Thinking Mode**:
```markdown
---
thinking: extended
---
```

#### Namespacing

Commands from different sources use namespacing to avoid collisions:
- Plugin commands: `/plugin-name:command-name`
- Project commands: `/project:command-name`
- Personal commands: `/user:command-name`

---

### 6.5 Hooks

#### Overview

Hooks are **event-driven** scripts that execute automatically in response to Claude Code system events. They enable validation, automation, and custom workflows.

#### Configuration

**Location**: `hooks/hooks.json` or inline in `plugin.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/format-code.sh"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/validate-input.sh"
          }
        ]
      }
    ]
  }
}
```

#### Available Events

| Event | Trigger | Use Cases |
|-------|---------|-----------|
| `PreToolUse` | Before Claude uses any tool | Validation, approval gates |
| `PostToolUse` | After Claude uses any tool | Formatting, logging, notifications |
| `UserPromptSubmit` | When user submits prompt | Input validation, context injection |
| `Notification` | When Claude sends notifications | Custom alerts |
| `Stop` | When Claude attempts to stop | Cleanup, final validation |
| `SubagentStop` | When subagent attempts to stop | Subagent-specific cleanup |
| `SessionStart` | Session begins | Initialization |
| `SessionEnd` | Session ends | Logging, cleanup |
| `PreCompact` | Before context compaction | State preservation |

#### Hook Output

**Simple (Exit Code)**:
- Exit 0: Success, continue
- Exit 1: Failure, show error
- Exit 2: Block action (for Pre* hooks)

**Advanced (JSON Output)**:
```json
{
  "continue": true,
  "message": "Validation passed",
  "addToPrompt": "Additional context to inject"
}
```

---

### 6.6 MCP Integration

#### Overview

Model Context Protocol (MCP) connects Claude Code to external tools, databases, and APIs through a standardized interface.

#### Configuration

**Location**: `.mcp.json` at project root

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.github.com/mcp"
    },
    "local-db": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@company/db-mcp-server"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

#### Server Types

| Type | Description | Use Case |
|------|-------------|----------|
| **HTTP** | Remote HTTP servers | Cloud services, APIs |
| **SSE** | Server-Sent Events (deprecated) | Legacy integrations |
| **stdio** | Local process servers | Custom tools, local databases |

#### Scopes

| Scope | Location | Visibility |
|-------|----------|------------|
| **Local** | Project `.mcp.json` | Current project only |
| **Project** | Checked into git | Team members |
| **User** | `~/.claude/` | All your projects |

#### Environment Variables

MCP configs support variable expansion:
- `${VAR}` — Expands to environment variable
- `${VAR:-default}` — Uses default if VAR not set

#### Adding MCP Servers

```bash
# HTTP server
claude mcp add --transport http github https://api.github.com/mcp

# stdio server
claude mcp add --transport stdio mydb -- npx -y @company/db-server

# With environment variables
claude mcp add --transport stdio secure-api \
  --env API_KEY \
  -- npx -y @company/api-server
```

---

### 6.7 Knowledge Base Structure

> **Note**: This section provides foundational guidance. A comprehensive exploration of advanced KB techniques (knowledge graphs, semantic indexing, atomic content structures, etc.) is planned for **Appendix C: Knowledge Base Deep Dive**. Content here may be revised as that exploration finalizes.

#### Recommended Organization

```
knowledge/
├── core/                         # Essential domain knowledge
│   ├── concepts.md               # Fundamental concepts
│   ├── terminology.md            # Domain vocabulary
│   └── standards.md              # Applicable standards
│
├── reference/                    # Supporting materials
│   ├── regulations/              # Regulatory documents
│   ├── methods/                  # Methodologies, procedures
│   └── data-sources/             # Data source documentation
│
├── examples/                     # Calibration materials
│   ├── inputs/                   # Sample inputs
│   ├── outputs/                  # Expected outputs
│   └── workflows/                # Example workflows
│
└── templates/                    # Reusable templates
    ├── reports/
    └── analyses/
```

#### Access Patterns

| Pattern | When to Use | Implementation |
|---------|-------------|----------------|
| **Direct Reference** | Always-needed info | `@import` in CLAUDE.md |
| **Skill Reference** | Procedural knowledge | Link in SKILL.md |
| **On-Demand** | Large reference docs | Claude reads via filesystem |
| **MCP Query** | External databases | MCP server integration |

#### Best Practices

1. **Categorize by Access Frequency**: Core = always needed; Reference = sometimes; Examples = calibration
2. **Use Consistent Naming**: lowercase-kebab-case for directories and files
3. **Include Metadata**: Frontmatter with last-updated, author, version
4. **Keep Files Focused**: One concept per file; link between files
5. **Version Control**: Track all knowledge in git

---

## 7. Distribution & Marketplace

### Plugin Distribution Flow

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Development     │ ──▶ │  Local Testing   │ ──▶ │  Publication     │
│                  │     │                  │     │                  │
│  - Create plugin │     │  - Local market  │     │  - GitHub repo   │
│  - Add components│     │  - /plugin test  │     │  - Marketplace   │
│  - Write docs    │     │  - Iterate       │     │  - Team sharing  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

### Local Testing Workflow

```bash
# 1. Create marketplace structure
mkdir dev-marketplace && cd dev-marketplace
mkdir -p .claude-plugin my-plugin

# 2. Create marketplace manifest
cat > .claude-plugin/marketplace.json << 'EOF'
{
  "name": "dev-marketplace",
  "owner": { "name": "Developer" },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./my-plugin",
      "description": "Plugin under development"
    }
  ]
}
EOF

# 3. Add and test
claude
/plugin marketplace add ./dev-marketplace
/plugin install my-plugin@dev-marketplace
```

### GitHub Distribution

```json
// marketplace.json for GitHub distribution
{
  "name": "org-plugins",
  "owner": {
    "name": "Organization Name",
    "email": "plugins@org.com"
  },
  "plugins": [
    {
      "name": "domain-assistant",
      "source": "./plugins/domain-assistant",
      "description": "Domain-specific assistant",
      "version": "1.0.0"
    }
  ]
}
```

### Team Configuration

Configure automatic plugin installation via `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  },
  "enabledPlugins": [
    "domain-assistant@team-tools"
  ]
}
```

### Security Considerations for Distribution

**Before publishing any plugin**:

| Check | Action |
|-------|--------|
| **Credentials** | Ensure no API keys, tokens, passwords in any file |
| **Personal data** | Remove any PII from knowledge base and examples |
| **Proprietary content** | Review CLAUDE.md and skills for confidential instructions |
| **Dependencies** | Audit MCP servers and scripts for security |
| **File permissions** | Ensure scripts don't have excessive permissions |

**Repository visibility workflow**:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Development    │ ──▶ │  Security       │ ──▶ │  Publication    │
│  (Private Repo) │     │  Review         │     │  (Public Repo)  │
│                 │     │                 │     │                 │
│  All work done  │     │  Run checklist  │     │  Manual release │
│  in private     │     │  Remove secrets │     │  only after     │
│                 │     │  Audit content  │     │  verification   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

**For team/organization distribution**: Consider keeping repositories private and using GitHub's team access controls rather than public publication.

---

## 8. Operational Patterns

This section covers advanced operational patterns for maximizing Claude Code efficiency in real-world workflows.

### 8.1 Git Worktree Parallel Execution

Git worktrees allow you to check out multiple branches simultaneously in separate directories, enabling **parallel Claude Code sessions** working on different aspects of your project.

#### Why Use Worktrees

| Scenario | Without Worktrees | With Worktrees |
|----------|-------------------|----------------|
| Feature + bugfix simultaneously | Switch branches, lose context | Two terminals, full context |
| Testing in isolation | Stash changes, checkout, test | Separate worktree for testing |
| Long-running analysis | Blocks other work | Dedicated worktree |
| Multi-agent collaboration | Single Claude instance | Multiple Claude instances |

#### Setup and Usage

```bash
# From your main repository
cd my-custom-llm

# Create worktree for a feature branch
git worktree add ../my-custom-llm-feature-auth feature/authentication

# Create worktree for bugfix
git worktree add ../my-custom-llm-hotfix hotfix/critical-bug

# List all worktrees
git worktree list
```

**Directory structure after worktrees**:
```
~/projects/
├── my-custom-llm/                 # Main worktree (main branch)
├── my-custom-llm-feature-auth/    # Feature worktree
└── my-custom-llm-hotfix/          # Hotfix worktree
```

#### Running Parallel Claude Code Sessions

```bash
# Terminal 1: Main development
cd ~/projects/my-custom-llm
claude

# Terminal 2: Feature work (separate session)
cd ~/projects/my-custom-llm-feature-auth
claude

# Terminal 3: Hotfix (separate session)
cd ~/projects/my-custom-llm-hotfix
claude
```

**Each session has**:
- Its own context window
- Access to branch-specific files
- Independent conversation history
- Shared access to global user config (`~/.claude/`)

#### Best Practices

1. **Name worktrees descriptively**: Include branch purpose in directory name
2. **Clean up when done**: `git worktree remove ../worktree-name`
3. **Don't checkout same branch twice**: Git prevents this, but plan accordingly
4. **Use for long-running tasks**: Analysis, research, complex refactors

#### Memory Considerations with Worktrees

Per official documentation, CLAUDE.md imports work better with worktrees than the deprecated CLAUDE.local.md approach:

```markdown
# In project CLAUDE.md
# Individual preferences via import (works across worktrees)
@~/.claude/my-project-preferences.md
```

### 8.2 Session Management

#### Resuming Sessions

```bash
# Continue most recent session in current directory
claude --continue

# Resume specific session by ID
claude --resume abc123

# List recent sessions (via interactive mode)
claude
# Then use /history or /resume
```

#### Session Persistence

Sessions are stored as JSONL transcript files. Useful for:
- Auditing conversation history
- Resuming complex multi-step work
- Sharing context with team members (carefully)

### 8.3 Multi-Agent Collaboration

Combining worktrees with subagents enables sophisticated workflows:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MULTI-AGENT ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Worktree 1 (main)          Worktree 2 (feature)                    │
│  ┌─────────────────┐        ┌─────────────────┐                     │
│  │ Claude Session  │        │ Claude Session  │                     │
│  │ ┌─────────────┐ │        │ ┌─────────────┐ │                     │
│  │ │ Main Agent  │ │        │ │ Main Agent  │ │                     │
│  │ └──────┬──────┘ │        │ └──────┬──────┘ │                     │
│  │        │        │        │        │        │                     │
│  │   ┌────┴────┐   │        │   ┌────┴────┐   │                     │
│  │   ▼         ▼   │        │   ▼         ▼   │                     │
│  │ ┌───┐    ┌───┐  │        │ ┌───┐    ┌───┐  │                     │
│  │ │Sub│    │Sub│  │        │ │Sub│    │Sub│  │                     │
│  │ │ 1 │    │ 2 │  │        │ │ 3 │    │ 4 │  │                     │
│  │ └───┘    └───┘  │        │ └───┘    └───┘  │                     │
│  └─────────────────┘        └─────────────────┘                     │
│           │                          │                               │
│           └──────────┬───────────────┘                               │
│                      ▼                                               │
│              Shared Git Repository                                   │
│              (commits, branches, PRs)                                │
└─────────────────────────────────────────────────────────────────────┘
```

**Coordination via Git**:
- Each worktree commits independently
- Merge coordination happens through PRs
- Shared knowledge base via repository

**Use Cases**:
- Parallel feature development
- Research + implementation simultaneously
- Review agent in one worktree, development in another

---

## 9. Implementation Workflow

### Phase 1: Foundation (Week 1)

```
□ Set up global user configuration
  □ Create ~/.claude/CLAUDE.md with personal baseline
  □ Configure settings.local.json with preferences
  □ Test with basic interactions

□ Choose migration target
  □ Select one custom LLM from Claude Web to migrate
  □ Document current system instructions
  □ Identify knowledge files to transfer
```

### Phase 2: Plugin Creation (Week 2)

```
□ Create plugin structure
  □ Initialize directory with standard layout
  □ Create plugin.json with metadata
  □ Write project CLAUDE.md

□ Migrate components
  □ Transfer system instructions
  □ Organize knowledge into core/reference/examples
  □ Create initial skill(s) if applicable

□ Local testing
  □ Set up local marketplace
  □ Install and test plugin
  □ Iterate based on results
```

### Phase 3: Enhancement (Week 3-4)

```
□ Add advanced components
  □ Create subagents for specialized tasks
  □ Add custom commands for common workflows
  □ Implement hooks for automation

□ MCP integration
  □ Connect GitHub MCP
  □ Add domain-specific MCPs as needed
  □ Test tool interactions

□ Documentation
  □ Write user-facing README
  □ Document setup guide
  □ Create preference template for users
```

### Phase 4: Distribution (Week 4+)

```
□ Prepare for sharing
  □ Clean up and finalize structure
  □ Version appropriately (semver)
  □ Write changelog

□ Publish
  □ Push to GitHub
  □ Add to marketplace (if using)
  □ Share with team/community

□ Maintain
  □ Gather feedback
  □ Iterate on skills/agents
  □ Update knowledge base
```

---

## 10. Future Enhancements [PLACEHOLDERS]

> **Note**: These sections are placeholders for future development. They represent identified enhancement areas that extend beyond the base architecture.

### 10.1 SDK & Programmatic Integration [PLACEHOLDER]

Integration of Claude Code capabilities into custom applications via the TypeScript/Python SDK. Covers programmatic session management, custom tool development, and embedding Claude Code in larger systems.

**Topics to cover**:
- SDK installation and authentication
- `query()` vs `ClaudeSDKClient` patterns
- Custom tool development
- Streaming vs single-message modes
- Error handling and recovery

### 10.2 Enterprise Deployment [PLACEHOLDER]

Configuration and deployment patterns for organization-wide Claude Code adoption. Covers managed policies, enterprise memory, MCP server governance, and compliance considerations.

**Topics to cover**:
- Enterprise policy CLAUDE.md deployment
- Managed MCP server configuration
- Allowlist/denylist MCP governance
- SSO/authentication integration
- Audit logging and compliance

### 10.3 Advanced MCP Development [PLACEHOLDER]

Building custom MCP servers to connect Claude Code with proprietary systems, databases, and APIs. Extends beyond basic MCP usage to server development.

**Topics to cover**:
- MCP server architecture (stdio, HTTP, SSE)
- Building servers in TypeScript/Python
- Authentication and security patterns
- Testing and debugging MCP servers
- Publishing to community

### 10.4 CI/CD Integration [PLACEHOLDER]

Automating Claude Code workflows in continuous integration and deployment pipelines. Covers GitHub Actions, GitLab CI, and headless execution patterns.

**Topics to cover**:
- GitHub Actions integration
- GitLab CI/CD configuration
- Headless mode (`claude -p`)
- Automated code review workflows
- Cost management in CI

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **CLAUDE.md** | Memory file containing system instructions that persist across sessions |
| **Skill** | Model-invoked capability packaged as SKILL.md with instructions and optional resources |
| **Subagent** | Specialized AI assistant operating in its own context window for delegated tasks |
| **Command** | User-invoked shortcut triggered by `/command-name` |
| **Hook** | Event-driven script that executes in response to system events |
| **MCP** | Model Context Protocol—standard for connecting Claude to external tools |
| **Plugin** | Distributable package containing commands, agents, skills, hooks, and MCP configs |
| **Marketplace** | Catalog of plugins available for discovery and installation |
| **Memory Hierarchy** | Tiered system of CLAUDE.md files with defined precedence |
| **Progressive Disclosure** | Pattern of loading only needed content to conserve tokens |
| **Model-Invoked** | Claude autonomously decides to use (vs. user-invoked which requires explicit trigger) |
| **Context Window** | Available token space for conversation history and instructions |
| **Token** | Unit of text processing; roughly 4 characters or 0.75 words |
| **Frontmatter** | YAML metadata at the top of markdown files (between `---` delimiters) |
| **@Import** | Syntax for including external files in CLAUDE.md (`@path/to/file`) |

---

## Appendix B: References

> **Note**: Water Resources Engineering case studies have been moved to a separate document: `case_studies_water_resources.md`

### Official Claude Code Documentation

| Document | URL | Description |
|----------|-----|-------------|
| Overview | https://docs.anthropic.com/en/docs/claude-code/overview | Getting started guide |
| Memory | https://docs.anthropic.com/en/docs/claude-code/memory | CLAUDE.md configuration |
| Skills | https://docs.anthropic.com/en/docs/claude-code/skills | Agent Skills guide |
| Subagents | https://docs.anthropic.com/en/docs/claude-code/sub-agents | Subagent configuration |
| Plugins | https://docs.anthropic.com/en/docs/claude-code/plugins | Plugin development |
| Plugins Reference | https://docs.anthropic.com/en/docs/claude-code/plugins-reference | Complete plugin schema |
| Plugin Marketplaces | https://docs.anthropic.com/en/docs/claude-code/plugin-marketplaces | Marketplace management |
| Slash Commands | https://docs.anthropic.com/en/docs/claude-code/slash-commands | Custom commands |
| Hooks | https://docs.anthropic.com/en/docs/claude-code/hooks | Event handlers |
| MCP | https://docs.anthropic.com/en/docs/claude-code/mcp | MCP integration |
| Settings | https://docs.anthropic.com/en/docs/claude-code/settings | Configuration options |
| CLI Reference | https://docs.anthropic.com/en/docs/claude-code/cli-reference | Command-line flags |

### Agent Skills Documentation

| Document | URL | Description |
|----------|-----|-------------|
| Skills Overview | https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview | Architecture and concepts |
| Best Practices | https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices | Authoring guidance |

### Model Context Protocol

| Resource | URL | Description |
|----------|-----|-------------|
| MCP Introduction | https://modelcontextprotocol.io/introduction | Protocol overview |
| MCP SDK | https://modelcontextprotocol.io/quickstart/server | Server development |
| MCP Servers | https://github.com/modelcontextprotocol/servers | Community servers |

### Supplemental Resources

| Resource | Description |
|----------|-------------|
| LLM Architecture Framework | Attached document: `llm_architecture_framework.md` |
| Custom LLM Human-Facing Guide | Attached document: `custom_llm_architecture_human_facing_guide_v_1.md` |
| Anthropic Engineering Blog | https://www.anthropic.com/engineering — Technical deep-dives |

---

## Appendix C: Knowledge Base Deep Dive [PLACEHOLDER]

> **Status**: To be developed. This appendix will provide comprehensive exploration of advanced knowledge base techniques.

**Planned content**:
- Knowledge graph integration patterns
- Semantic indexing and metadata tagging strategies
- Atomic content structures for optimal retrieval
- RAG optimization techniques for Claude Code
- Content protocols: examples, micro-templates, rubrics, decision rules, fault trees, agent role cards, lessons-learned
- Scaling strategies for large knowledge bases (100+ files)
- MCP integration with vector databases
- Benchmarking and evaluation methodologies

---

## Appendix D: AI Agents Deep Dive [PLACEHOLDER]

> **Status**: To be developed. This appendix will explore advanced agent architectures and orchestration patterns.

**Planned content**:
- Agent orchestration patterns
- Multi-agent collaboration frameworks
- Agent state management and persistence
- Hierarchical agent architectures
- Agent evaluation and monitoring
- Integration with official Anthropic skills (skill-creator, mcp-builder)
- Custom hybrid skill development
- Agent lifecycle management

---

## Document Information

**Version History**:
- v0.3.0-draft (December 2025): Added privacy/security defaults, KB deep dive placeholder, Agents deep dive placeholder, updated metadata
- v0.2.0-draft (December 2025): Added Git Foundation, Operational Patterns, Placeholder sections; restructured for modularity
- v0.1.0-draft (December 2025): Initial comprehensive guide

**Related Documents**:
- `case_studies_water_resources.md` — Domain-specific case studies for water resources engineering

**Contributing**:
This guide is intended to evolve. Feedback and contributions welcome via GitHub issues or pull requests.

**License**:
MIT License — Free to use, modify, and distribute with attribution.
