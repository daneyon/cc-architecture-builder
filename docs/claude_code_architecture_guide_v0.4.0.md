# Claude Code Architecture Guide

## A Comprehensive Framework for Custom LLM Development

<!-- DOCUMENT METADATA (Machine-Readable) -->
<!--
status: DRAFT
version: 0.4.0
author: Daneyon (with Claude)
last_updated: 2025-12-18
document_type: architecture_guide
primary_audience: [human, llm]
sections_complete: [executive_summary, architecture_philosophy, prerequisites_git, schema_1, schema_2, components, distribution, operational_patterns, implementation]
sections_in_progress: []
sections_placeholder: [sdk_integration, enterprise_deployment, advanced_mcp, cicd, kb_deep_dive, agents_deep_dive]
pending_reviews: []
reviewed_skills: [skill-creator, mcp-builder]
notes: Updated sections 6.2 and 6.6 based on Anthropic skill-creator and mcp-builder review
-->

> **DRAFT STATUS**: This is a living document under active development. Sections marked with `[PLACEHOLDER]` are incomplete. Last substantive edit: December 18, 2025.

**Version**: 0.4.0-draft  
**Author**: Daneyon (with Claude)  
**Last Updated**: December 18, 2025

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Architecture Philosophy](#2-architecture-philosophy)
3. [Prerequisites & Git Foundation](#3-prerequisites--git-foundation)
4. [Schema 1: Global User Configuration](#4-schema-1-global-user-configuration)
5. [Schema 2: Distributable Plugin Project](#5-schema-2-distributable-plugin-project)
6. [Component Deep Dives](#6-component-deep-dives)
   - 6.1 [Memory System (CLAUDE.md)](#61-memory-system-claudemd)
   - 6.2 [Agent Skills](#62-agent-skills) **(Updated v0.4.0)**
   - 6.3 [Subagents](#63-subagents)
   - 6.4 [Custom Commands](#64-custom-commands)
   - 6.5 [Hooks](#65-hooks)
   - 6.6 [MCP Integration](#66-mcp-integration) **(Updated v0.4.0)**
   - 6.7 [Knowledge Base Structure](#67-knowledge-base-structure)
7. [Distribution & Marketplace](#7-distribution--marketplace)
8. [Operational Patterns](#8-operational-patterns)
9. [Implementation Workflow](#9-implementation-workflow)
10. [Future Enhancements](#10-future-enhancements-placeholders) [PLACEHOLDERS]
11. [Appendix A: Glossary](#appendix-a-glossary)
12. [Appendix B: References](#appendix-b-references) **(Updated v0.4.0)**

---

## What's New in v0.4.0

This version incorporates insights from reviewing Anthropic's official example skills:

| Source | Key Insights Integrated |
|--------|------------------------|
| **skill-creator** | Three bundled resource types, degrees of freedom framework, progressive disclosure patterns, skill creation process, packaging |
| **mcp-builder** | Server naming conventions, transport selection, tool annotations, 4-phase development workflow, evaluation methodology |

**Updated Sections**:
- Section 6.2 (Agent Skills) — Comprehensive rewrite
- Section 6.6 (MCP Integration) — Added development patterns
- Appendix B (References) — Added bundled skills documentation

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
│  └── agents/                # Personal agents                                │
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
│  ├── .claude-plugin/plugin.json   # Marketplace metadata                     │
│  ├── CLAUDE.md                    # Project system instructions              │
│  ├── .mcp.json                    # MCP server configurations                │
│  ├── commands/                    # Custom slash commands                    │
│  ├── agents/                      # Project-specific subagents               │
│  ├── skills/                      # Project-specific skills                  │
│  ├── hooks/hooks.json             # Event handlers                           │
│  └── knowledge/                   # Domain knowledge base                    │
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
| **1. Enterprise Policy** | System-level CLAUDE.md | Organization-wide standards | All org users |
| **2. User Memory** | `~/.claude/CLAUDE.md` | Personal preferences (all projects) | Just you |
| **3. Project Memory** | `./CLAUDE.md` | Team-shared instructions | Team via git |
| **4. Subtree Memory** | `./subdir/CLAUDE.md` | Directory-specific context | Team via git |

**Precedence Rule**: Files higher in the hierarchy load first and take precedence.

### Invocation Patterns

| Component | Invocation Type | Trigger |
|-----------|-----------------|---------|
| **Memory (CLAUDE.md)** | Automatic | Always loaded at session start |
| **Skills** | Model-invoked | Claude autonomously decides based on task context |
| **Subagents** | Model or user-invoked | Auto-delegated or explicitly called |
| **Commands** | User-invoked | Explicitly typed (e.g., `/analyze`) |
| **Hooks** | Event-driven | Triggered by system events |

---

## 3. Prerequisites & Git Foundation

### Why Git is Foundational

Git is **architecturally required** for this framework:

| Capability | Git Dependency |
|------------|----------------|
| Plugin distribution | Marketplaces pull from git repositories |
| Team collaboration | Project CLAUDE.md and configs shared via git |
| Version control | System instructions, skills, agents all versioned |
| Parallel execution | Git worktrees enable multiple Claude Code sessions |

### Initial Setup Checklist

```bash
# 1. Initialize repository FIRST
git init

# 2. Create initial structure
mkdir -p .claude-plugin commands agents skills knowledge docs
touch CLAUDE.md README.md .gitignore

# 3. Commit
git add .
git commit -m "Initial project structure"
```

### Privacy & Security Defaults

**Critical**: Create repositories as **private by default** during development.

**Pre-publication checklist**:
- [ ] No API keys, tokens, or credentials in repository
- [ ] No personal/client data in knowledge base
- [ ] `.gitignore` excludes sensitive files
- [ ] Review all files for PII or confidential information

---

## 4. Schema 1: Global User Configuration

### Directory Structure

```
~/.claude/
├── CLAUDE.md                     # Personal baseline (always loaded)
├── settings.local.json           # Local settings overrides
├── skills/                       # Personal skills (cross-project)
│   └── your-skill/SKILL.md
└── agents/                       # Personal subagents
    └── your-agent.md
```

### CLAUDE.md (Personal Baseline)

```markdown
# Personal Configuration

## Communication Style
- Employ systems thinking and comprehensive analysis
- Provide structured overviews before detailed analysis
- Balance theoretical depth with practical applicability
- Use natural, conversational tone unless technical analysis needed

## Default Behaviors
- Ask clarifying questions before diving into complex tasks
- Provide evidence-based reasoning with citations where applicable
- Challenge assumptions constructively
```

---

## 5. Schema 2: Distributable Plugin Project

### Directory Structure

```
my-custom-llm/
├── .claude-plugin/plugin.json    # Required: marketplace metadata
├── CLAUDE.md                     # Project system instructions
├── .mcp.json                     # MCP server configurations
├── commands/                     # Custom slash commands
├── agents/                       # Project-specific subagents
├── skills/                       # Project-specific skills
├── hooks/hooks.json              # Event handlers
├── knowledge/                    # Domain knowledge base
│   ├── core/                     # Essential knowledge
│   ├── reference/                # Supporting materials
│   └── examples/                 # Calibration materials
└── docs/                         # Documentation
```

### plugin.json

```json
{
  "name": "my-custom-llm",
  "version": "1.0.0",
  "description": "Domain-specific custom LLM",
  "author": { "name": "Your Name" },
  "repository": "https://github.com/yourusername/my-custom-llm"
}
```

---

## 6. Component Deep Dives

### 6.1 Memory System (CLAUDE.md)

CLAUDE.md files serve as persistent memory—instructions that Claude reads at the start of every session.

**Import Syntax**:
```markdown
See @README.md for project overview.
@~/.claude/my-preferences.md
```

**Best Practices**:
- Be specific: "Use 2-space indentation" not "Format code properly"
- Keep total length under 500 lines
- Use `@imports` for detailed reference material

---

### 6.2 Agent Skills **(Updated v0.4.0)**

#### Overview

Skills are **model-invoked** capabilities—Claude autonomously decides when to use them based on task context and skill description.

> **Core Philosophy** (from Anthropic skill-creator): The context window is a public good. Only add context Claude doesn't already have. Challenge each piece: "Does Claude really need this?"

#### Skill Structure

```
skill-name/
├── SKILL.md              # Required
└── Bundled Resources     # Optional
    ├── scripts/          # Executable code (Python/Bash)
    ├── references/       # Documentation loaded into context as needed
    └── assets/           # Files used in output (templates, images, fonts)
```

**Bundled Resource Types**:

| Type | Purpose | Loaded Into Context? |
|------|---------|---------------------|
| `scripts/` | Executable code for deterministic operations | No (outputs only) |
| `references/` | Documentation Claude references while working | Yes (on demand) |
| `assets/` | Templates, images, fonts for output | No (used in output) |

#### SKILL.md Format

```yaml
---
name: skill-name
description: What this skill does AND when to use it. Include specific triggers. Third-person voice.
---

# Skill Name

## Overview
[1-2 sentences]

## Instructions
1. Step-by-step guidance
2. Clear procedures

## Output Format
[Expected output structure]

## References
For details, see [references/guide.md](references/guide.md)
```

**Critical**: Include ALL "when to use" information in the `description` field, not in the body. The body only loads AFTER triggering.

#### Allowed Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier (max 64 chars, lowercase+hyphens) |
| `description` | Yes | What skill does and when to use (max 1024 chars) |
| `license` | No | License reference |
| `allowed-tools` | No | Restrict which tools the skill can use |
| `metadata` | No | Custom metadata object |

#### Naming Requirements

| Field | Requirements |
|-------|-------------|
| `name` | Max 64 chars, lowercase letters/numbers/hyphens only, cannot start/end with hyphen, no `--`, no reserved words ("anthropic", "claude") |
| `description` | Max 1024 chars, non-empty, no angle brackets (< or >), third-person voice |

**Naming Convention**: Use gerund form: `processing-pdfs`, `analyzing-data`, `managing-databases`

#### Progressive Disclosure

Skills use a three-level loading model:

| Level | When Loaded | Token Cost | Content |
|-------|-------------|------------|--------|
| **Level 1: Metadata** | Always (startup) | ~100 tokens/skill | `name` and `description` |
| **Level 2: Instructions** | When skill triggered | < 5k words | SKILL.md body |
| **Level 3: Resources** | As needed | Unlimited | Bundled files, scripts |

**Key Principle**: Keep SKILL.md body under 500 lines. Split content into reference files when approaching this limit.

#### Degrees of Freedom

Match specificity to task fragility:

| Level | When to Use | Form |
|-------|-------------|------|
| **High freedom** | Multiple approaches valid | Text instructions |
| **Medium freedom** | Preferred pattern exists | Pseudocode with parameters |
| **Low freedom** | Operations fragile, consistency critical | Specific scripts |

#### What NOT to Include in Skills

Skills are for AI agents, not human users. Do NOT create:
- README.md
- INSTALLATION_GUIDE.md
- CHANGELOG.md
- User-facing documentation

#### Skill Creation Process

1. **Understand** — Gather concrete usage examples
2. **Plan** — Identify reusable resources (scripts, references, assets)
3. **Initialize** — Create structure (use `init_skill.py` if available)
4. **Edit** — Implement resources, write SKILL.md
5. **Package** — Create `.skill` file (zip format) for distribution
6. **Iterate** — Improve based on real usage

#### Packaging Skills

```bash
python scripts/package_skill.py path/to/skill-folder
# Creates: skill-name.skill (zip format)
```

---

### 6.3 Subagents

Subagents are specialized AI assistants operating in their **own context window**, preventing pollution of the main conversation.

**File Format** (`agents/domain-expert.md`):

```yaml
---
name: domain-expert
description: Description of when this subagent should be invoked
tools: Read, Grep, Glob, WebSearch
model: sonnet
---

# Agent Name

You are a specialized agent focused on [specific purpose].

## Approach
1. [Step 1]
2. [Step 2]

## Constraints
- [Constraint 1]
- [Constraint 2]
```

**Skills vs Agents**:

| Aspect | Skills | Subagents |
|--------|--------|-----------|
| **Context** | Loads into main context | Separate context window |
| **Purpose** | Procedural knowledge | Specialized assistant |
| **State** | Stateless | Can be resumed |
| **Token Impact** | Adds to main context | Preserves main context |

---

### 6.4 Custom Commands

Commands are **user-invoked** shortcuts triggered by typing `/command-name`.

**File Format** (`commands/analyze.md`):

```markdown
---
description: Brief description shown in /help
allowed-tools: Read, Write, Bash
---

# Command Instructions

Clear instructions for what Claude should do.

## Arguments
This command accepts: $ARGUMENTS
Individual args: $1, $2, $3
```

---

### 6.5 Hooks

Hooks are **event-driven** scripts that execute automatically in response to system events.

**Configuration** (`hooks/hooks.json`):

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
    ]
  }
}
```

**Available Events**: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Notification`, `Stop`, `SubagentStop`, `SessionStart`, `SessionEnd`, `PreCompact`

---

### 6.6 MCP Integration **(Updated v0.4.0)**

#### Overview

Model Context Protocol (MCP) connects Claude Code to external tools, databases, and APIs.

> **Quality Measure** (from Anthropic mcp-builder): The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks, not just how many API endpoints it covers.

#### Configuration

**Location**: `.mcp.json` at project root

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.github.com/mcp",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    }
  }
}
```

#### Transport Types

| Type | Best For | Notes |
|------|----------|-------|
| **Streamable HTTP** | Remote servers, multi-client | Recommended for production |
| **stdio** | Local integrations, CLI tools | Don't log to stdout |
| **SSE** | Legacy | Deprecated |

#### Server Naming Conventions

| Language | Format | Example |
|----------|--------|---------|
| **Python** | `{service}_mcp` | `slack_mcp`, `github_mcp` |
| **TypeScript** | `{service}-mcp-server` | `slack-mcp-server` |

#### Tool Naming Best Practices

```
# Format: {service}_{action}_{resource}
slack_send_message      # Not: send_message
github_create_issue     # Not: create_issue
```

**Why prefix?** MCP servers may be used alongside others; prefixing prevents tool name conflicts.

#### Tool Annotations

| Annotation | Type | Description |
|-----------|------|-------------|
| `readOnlyHint` | boolean | Tool does not modify environment |
| `destructiveHint` | boolean | Tool may perform destructive updates |
| `idempotentHint` | boolean | Repeated calls have no additional effect |
| `openWorldHint` | boolean | Tool interacts with external entities |

#### MCP Development Workflow (4 Phases)

1. **Research & Planning** — Understand API, study MCP docs, plan tools
2. **Implementation** — Set up project, implement infrastructure, build tools
3. **Review & Test** — Code quality, build verification, MCP Inspector testing
4. **Evaluation** — Create 10 complex test questions to verify effectiveness

#### Python Example (FastMCP)

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("example_mcp")

class SearchInput(BaseModel):
    query: str = Field(..., description="Search query", min_length=2)
    limit: int = Field(default=20, ge=1, le=100)

@mcp.tool(
    name="example_search",
    annotations={"readOnlyHint": True, "destructiveHint": False}
)
async def search(params: SearchInput) -> str:
    '''Search for items. Use when user asks to find or search.'''
    # Implementation
    pass

if __name__ == "__main__":
    mcp.run()
```

#### TypeScript Example (MCP SDK)

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "example-mcp-server",
  version: "1.0.0"
});

const SearchInput = z.object({
  query: z.string().min(2).describe("Search query"),
  limit: z.number().int().min(1).max(100).default(20)
});

server.registerTool(
  "example_search",
  {
    title: "Search Items",
    description: "Search for items.",
    inputSchema: SearchInput,
    annotations: { readOnlyHint: true, destructiveHint: false }
  },
  async (params) => { /* Implementation */ }
);
```

---

### 6.7 Knowledge Base Structure

#### Recommended Organization

```
knowledge/
├── core/                         # Essential domain knowledge
├── reference/                    # Supporting materials
├── examples/                     # Calibration materials
└── templates/                    # Reusable templates
```

#### Access Patterns

| Pattern | When to Use | Implementation |
|---------|-------------|----------------|
| **Direct Reference** | Always-needed info | `@import` in CLAUDE.md |
| **Skill Reference** | Procedural knowledge | Link in SKILL.md |
| **On-Demand** | Large reference docs | Claude reads via filesystem |
| **MCP Query** | External databases | MCP server integration |

---

## 7. Distribution & Marketplace

### Plugin Distribution Flow

```
Development → Local Testing → Security Review → Publication
(Private Repo)  (Local market)  (Run checklist)   (GitHub/Marketplace)
```

### Local Testing

```bash
# Create local marketplace
mkdir dev-marketplace && cd dev-marketplace
mkdir -p .claude-plugin my-plugin

# Add manifest
cat > .claude-plugin/marketplace.json << 'EOF'
{
  "name": "dev-marketplace",
  "plugins": [{ "name": "my-plugin", "source": "./my-plugin" }]
}
EOF

# Test in Claude Code
claude
/plugin marketplace add ./dev-marketplace
/plugin install my-plugin@dev-marketplace
```

---

## 8. Operational Patterns

### Git Worktree Parallel Execution

Git worktrees enable **parallel Claude Code sessions** on different branches:

```bash
# Create worktrees
git worktree add ../project-feature feature/auth
git worktree add ../project-hotfix hotfix/bug

# Run parallel sessions
cd ../project-feature && claude    # Terminal 1
cd ../project-hotfix && claude     # Terminal 2
```

### Session Management

```bash
claude --continue          # Resume most recent session
claude --resume abc123     # Resume specific session
```

---

## 9. Implementation Workflow

### Phase 1: Foundation
- Set up global user configuration (`~/.claude/`)
- Select migration target (existing custom LLM)

### Phase 2: Plugin Creation
- Create plugin structure
- Migrate components
- Local testing

### Phase 3: Enhancement
- Add skills, subagents, commands
- MCP integration
- Documentation

### Phase 4: Distribution
- Security review
- Publish to GitHub/marketplace
- Gather feedback, iterate

---

## 10. Future Enhancements [PLACEHOLDERS]

| Section | Status | Description |
|---------|--------|-------------|
| SDK & Programmatic Integration | Placeholder | TypeScript/Python SDK integration |
| Enterprise Deployment | Placeholder | Organization-wide configuration |
| Advanced MCP Development | Placeholder | Custom MCP server building |
| CI/CD Integration | Placeholder | GitHub Actions, automation |
| Knowledge Base Deep Dive | Placeholder | Advanced KB techniques |
| AI Agents Deep Dive | Placeholder | Agent orchestration patterns |

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **CLAUDE.md** | Memory file with persistent system instructions |
| **Skill** | Model-invoked capability packaged as SKILL.md |
| **Subagent** | Specialized AI assistant in separate context |
| **Command** | User-invoked shortcut (`/command-name`) |
| **Hook** | Event-driven script |
| **MCP** | Model Context Protocol for external tools |
| **Plugin** | Distributable package with components |
| **Progressive Disclosure** | Pattern of loading only needed content |

---

## Appendix B: References **(Updated v0.4.0)**

### Official Claude Code Documentation

| Document | URL |
|----------|-----|
| Overview | https://docs.anthropic.com/en/docs/claude-code/overview |
| Memory | https://docs.anthropic.com/en/docs/claude-code/memory |
| Skills | https://docs.anthropic.com/en/docs/claude-code/skills |
| Subagents | https://docs.anthropic.com/en/docs/claude-code/sub-agents |
| Commands | https://docs.anthropic.com/en/docs/claude-code/slash-commands |
| Hooks | https://docs.anthropic.com/en/docs/claude-code/hooks |
| MCP | https://docs.anthropic.com/en/docs/claude-code/mcp |
| Plugins | https://docs.anthropic.com/en/docs/claude-code/plugins |

### Agent Skills Documentation

| Document | URL |
|----------|-----|
| Skills Overview | https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview |
| Best Practices | https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices |

### Anthropic Example Skills (Bundled)

This project includes adapted versions of Anthropic's example skills:

| Skill | Purpose | Key Resources |
|-------|---------|---------------|
| `skills/skill-creator/` | Skill authoring guide | `references/workflows.md`, `references/output-patterns.md`, `scripts/init_skill.py` |
| `skills/mcp-builder/` | MCP server development | `reference/mcp_best_practices.md`, `reference/python_mcp_server.md`, `reference/node_mcp_server.md` |

### Model Context Protocol

| Resource | URL |
|----------|-----|
| MCP Introduction | https://modelcontextprotocol.io/introduction |
| TypeScript SDK | https://github.com/modelcontextprotocol/typescript-sdk |
| Python SDK | https://github.com/modelcontextprotocol/python-sdk |

---

## Document Information

**Version History**:
- v0.4.0-draft (December 2025): Reviewed Anthropic skill-creator and mcp-builder; updated Skills and MCP sections; added bundled skills
- v0.3.0-draft (December 2025): Added privacy/security defaults, KB placeholder, Agents placeholder
- v0.2.0-draft (December 2025): Added Git Foundation, Operational Patterns
- v0.1.0-draft (December 2025): Initial comprehensive guide

**License**: MIT License
