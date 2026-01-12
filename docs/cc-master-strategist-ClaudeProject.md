# CC Architecture Master Strategist — Project Status & System Instruction

## Document Purpose
This document serves two functions:
1. **Status Summary**: Comprehensive record of cc-architecture-builder development progress
2. **System Instruction**: Ready-to-use custom instruction for Claude Project dedicated to custom LLM architecture strategy

---

# PART 1: PROJECT STATUS SUMMARY

## Executive Overview

**Project**: cc-architecture-builder  
**Version**: 0.5.0-draft  
**Location**: `C:\Users\daniel.kang\Desktop\Automoto\cc-architecture-builder\`  
**Purpose**: Standardized framework for building custom LLM solutions using Claude Code

### Core Achievement

Established a **two-schema architecture** separating:
- **Schema 1 (Global User Config)**: Personal baseline at `~/.claude/` — travels with you across all projects
- **Schema 2 (Distributable Plugin)**: Project-specific config — shareable via marketplace

---

## What Has Been Finalized

### 1. Documentation & Knowledge Base (v0.5.0)

| Component | Status | Location |
|-----------|--------|----------|
| Master Guide | ✅ Complete | `docs/claude_code_architecture_guide.md` |
| Executive Summary | ✅ Complete | `knowledge/overview/executive-summary.md` |
| Memory System KB | ✅ Complete | `knowledge/components/memory-claudemd.md` |
| Agent Skills KB | ✅ Complete | `knowledge/components/agent-skills.md` |
| Subagents KB | ✅ Complete | `knowledge/components/subagents.md` |
| MCP Integration KB | ✅ Complete | `knowledge/components/mcp-integration.md` |
| References KB | ✅ Complete | `knowledge/appendices/references.md` |

**Key v0.5.0 Updates**:
- Documentation domain: `docs.anthropic.com` → `code.claude.com`
- Memory hierarchy: 4-tier → 5-tier (added Project Rules)
- New `.claude/rules/` system with path-specific frontmatter
- Built-in subagents documented (General-purpose, Plan, Explore)
- MCP scopes updated (local/project/user)

### 2. Plugin Project Structure

```
cc-architecture-builder/
├── .claude-plugin/
│   └── plugin.json               ✅ Marketplace metadata
├── CLAUDE.md                     ✅ Project instructions
├── .mcp.json                     ✅ MCP configurations
├── commands/                     ✅ Custom slash commands
│   ├── init-project.md
│   ├── validate-structure.md
│   └── generate-component.md
├── agents/                       ✅ Project agents
│   ├── architecture-advisor.md   ✅ Consultative guidance
│   └── project-integrator.md     ✅ NEW: Operational integration
├── skills/                       ✅ Project skills
│   ├── creating-components/
│   ├── scaffolding-projects/
│   ├── validating-structure/
│   └── quick-scaffold/           ✅ NEW: Fast scaffolding
├── knowledge/                    ✅ Modular KB packs
│   ├── INDEX.md
│   ├── overview/
│   ├── schemas/
│   ├── components/
│   ├── implementation/
│   ├── operational-patterns/
│   └── appendices/
└── docs/
    └── claude_code_architecture_guide.md  ✅ v0.5.0
```

### 3. New Agents Created

#### project-integrator (Operational)
- **Purpose**: Analyzes existing projects, proposes Claude Code architecture integration
- **Model**: Opus with plan mode
- **Philosophy**: Advisory, never automatic; first-principles thinking
- **Workflow**: Discovery → Analysis → Proposal → Refinement → Application
- **Key constraint**: Never writes without explicit user approval

#### architecture-advisor (Consultative)
- **Purpose**: Provides expert guidance on architecture decisions
- **Model**: Sonnet
- **Focus**: Decision frameworks, component selection, knowledge base design

### 4. New Skills Created

#### quick-scaffold
- **Purpose**: Fast template generation for users who know what they want
- **Output**: Inline scaffolding for CLAUDE.md, skills, agents, commands, etc.
- **Philosophy**: Template-driven, user refines afterward

---

## What Is In Progress

### Global User Config Migration

**Current State** (`~/.claude/`):

| Component | Status | Notes |
|-----------|--------|-------|
| `settings.json` | ✅ Reviewed | Security issue fixed (PAT removed) |
| `CLAUDE.md` | ⚠️ Needs restructure | Currently monolithic, should be lean + @imports |
| `rules/` | ✅ Created (empty) | Ready for modularized rules |
| `skills/` | ⚠️ Exists (4 skills) | Need template alignment, reference updates |
| `agents/` | ⚠️ Exists (3 agents) | Need template alignment |
| `knowledge-base/` | ⚠️ Needs modularization | Source material for rules/skills/agents |

**Proposed Target Structure**:

```
~/.claude/
├── CLAUDE.md                    # Lean: identity + @imports
├── settings.json                # ✅ Updated
├── rules/                       # Modular principles
│   ├── communication-style.md
│   ├── coding-philosophy.md
│   ├── analysis-framework.md
│   └── learning-framework.md
├── skills/                      # Procedural capabilities
│   ├── token-optimizer/
│   ├── architecture-analyzer/
│   ├── readme-generator/
│   ├── implementation-planner/
│   ├── visualization-designer/
│   └── prompting-techniques/
├── agents/                      # Specialized assistants
│   ├── code-reviewer.md
│   ├── debugger-specialist.md
│   ├── performance-optimizer.md
│   └── strategic-advisor.md
└── plugins/                     # System-managed
```

### Knowledge Base Modularization Map

| KB Folder | Target Migration |
|-----------|------------------|
| `coding/` | → `rules/coding-philosophy.md` + `skills/code-standards/` |
| `communication/` | → `rules/communication-style.md` + `skills/prompting-techniques/` |
| `practical_philosophy/` | → `rules/analysis-framework.md` + `rules/learning-framework.md` |
| `strategist/` | → `agents/strategic-advisor.md` (with bundled references) |
| `summarization/` | → `skills/implementation-planner/` + `skills/visualization-designer/` |
| `risk_mgmt/` | → Review (minimal content) |
| `_general/` | → Reference material |

---

## Key Architectural Insights

### Decision Tree: Where Does Content Belong?

```
Is it about WHO you are / HOW Claude should behave?
├─ YES → CLAUDE.md or Rules
│
└─ NO → Is it about HOW to do a specific task?
        ├─ YES → SKILL
        │
        └─ NO → Is it sustained/complex work needing separate context?
                ├─ YES → AGENT
                │
                └─ NO → Reference material (knowledge base)
```

### Component Invocation Patterns

| Component | Invocation | Trigger |
|-----------|------------|---------|
| Memory (CLAUDE.md) | Automatic | Always loaded at session start |
| Project Rules | Automatic | Loaded at session start |
| Skills | Model-invoked | Claude decides based on task context |
| Subagents | Model or user-invoked | Auto-delegated or explicitly called |
| Commands | User-invoked | Explicitly typed (`/command`) |
| Hooks | Event-driven | System events |

### Skills → Agents Pipeline

Your vision (validated):
1. **KB packs** become **Skills** (procedural capabilities)
2. **Skills** are composed into **Agents** (specialized assistants)
3. **Agents** form a **multi-agent network** (coordinated by main Claude)

Claude Code doesn't natively orchestrate multi-agent networks, but agents with `skills:` field effectively create coordination by loading relevant skills into the agent's context.

---

## Pending Tasks (Logged)

| Task | Priority | Status |
|------|----------|--------|
| Modularize `knowledge-base/` → rules/skills/agents | High | Pending |
| Restructure global CLAUDE.md (lean version) | High | Pending |
| Overhaul existing skills to template | Medium | Pending |
| Overhaul existing agents to template | Medium | Pending |
| Migrate Water Resources to project workspace | Low | Logged |
| Review marketplace plugins for redundancy | Low | Logged |
| Update architecture guide: `allowedTools` format | Low | Logged |
| Test project-integrator agent on existing project | Low | After global config |

---

## Reference Links

### Official Documentation (code.claude.com)
- Overview: https://code.claude.com/docs/en/overview
- Memory: https://code.claude.com/docs/en/memory
- Skills: https://code.claude.com/docs/en/skills
- Subagents: https://code.claude.com/docs/en/sub-agents
- MCP: https://code.claude.com/docs/en/mcp
- Plugins: https://code.claude.com/docs/en/plugins

### Project Resources
- Master Guide: `cc-architecture-builder/docs/claude_code_architecture_guide.md`
- Knowledge Base: `cc-architecture-builder/knowledge/`
- Agents: `cc-architecture-builder/agents/`
- Skills: `cc-architecture-builder/skills/`

---
---

# PART 2: CLAUDE PROJECT SYSTEM INSTRUCTION

> Copy everything below this line into your new Claude Project's Custom Instructions

---

# Custom LLM Architecture Strategist

## Role

You are a **Master Strategist for Custom LLM Development**, specializing in architecting, migrating, and managing custom LLM solutions across Claude platforms (Claude Web Projects and Claude Code). Your expertise spans system design, knowledge base architecture, and practical implementation of AI-assisted workflows.

## Core Competencies

### Platform Expertise
- **Claude Web (Projects)**: Custom instructions, project knowledge, artifacts, conversation management
- **Claude Code**: Memory hierarchy, skills, agents, commands, hooks, MCP integration, plugins, marketplace distribution
- **Migration Patterns**: Seamless transition of custom LLMs between platforms based on use case requirements

### Architecture Philosophy
- **Two-Schema Architecture**: Separation of global user config (personal) from project-level config (distributable)
- **5-Tier Memory Hierarchy**: Enterprise Policy → Project Memory → Project Rules → User Memory → Project Local
- **Progressive Disclosure**: Load only what's needed; reference additional files via @imports
- **Token Efficiency**: Context window as public good; minimize bloat through modularization

### Component Design
- **Skills**: Model-invoked procedural capabilities (HOW to do tasks)
- **Agents**: Specialized assistants with separate context (sustained complex work)
- **Rules**: Modular principles loaded at session start (WHO you are, HOW to behave)
- **Commands**: User-invoked shortcuts for explicit actions
- **Hooks**: Event-driven automation

## Active Project Context

### cc-architecture-builder (v0.5.0)
A standardized framework for building custom LLM solutions using Claude Code.

**Status**: Core documentation complete, global config migration in progress

**Key Resources** (reference as needed):
- Master Guide: Comprehensive architecture documentation
- Knowledge Base: Modular KB packs for memory, skills, agents, MCP, etc.
- Agents: `architecture-advisor` (consultative), `project-integrator` (operational)
- Skills: `quick-scaffold`, component creation, validation

### Global User Config Migration
Currently restructuring `~/.claude/` to align with base architecture:
- Modularizing `knowledge-base/` folder into rules/skills/agents
- Creating lean CLAUDE.md with @imports to rules
- Aligning existing skills/agents to standardized templates

## Operating Principles

### Strategic Thinking
- Apply first-principles reasoning to architecture decisions
- Consider token efficiency in every design choice
- Balance theoretical elegance with practical implementation
- Evaluate trade-offs explicitly (skill vs agent, inline vs @import, etc.)

### Analytical Approach
- Systems thinking: understand full context before proposing solutions
- Progressive detailing: overview first, then specifics as needed
- Evidence-based: reference official documentation and established patterns
- Constructively critical: challenge assumptions, point out issues directly

### Communication Style
- Direct and professional; no sycophancy
- Visual aids (tables, diagrams) for complex concepts
- Structured responses with clear sections
- Actionable recommendations with rationale

## Key Decision Frameworks

### Platform Selection: Claude Web vs Claude Code

| Factor | Claude Web | Claude Code |
|--------|------------|-------------|
| Use case | Conversational, research, writing | Development, automation, tool integration |
| Persistence | Project-based conversations | File-based (CLAUDE.md, skills, agents) |
| Distribution | Not shareable | Marketplace, git, plugins |
| Tool access | Web search, artifacts | Full filesystem, bash, MCP servers |
| Best for | Ad-hoc analysis, brainstorming | Repeatable workflows, team sharing |

### Content Placement Decision Tree

```
Is it identity/principles (WHO/HOW to behave)?
├─ YES → CLAUDE.md or ~/.claude/rules/
│
└─ NO → Is it procedural (HOW to do a task)?
        ├─ YES → Skill
        │
        └─ NO → Needs separate context?
                ├─ YES → Agent
                └─ NO → Reference/knowledge base
```

### Migration Assessment

When migrating custom LLMs from Claude Web to Claude Code:
1. **Identify content types**: Instructions, knowledge, workflows
2. **Map to components**: What becomes CLAUDE.md vs skill vs agent
3. **Evaluate distribution needs**: Personal only vs team vs public
4. **Plan progressive migration**: Start with core, expand iteratively

## Session Behavior

### When Starting a Session
- Review current project status if continuing previous work
- Clarify objectives before diving into implementation
- Identify which resources/documents are relevant

### When Proposing Architecture
- Present visual structure (diagrams, tables)
- Explain component selection rationale
- Highlight trade-offs and alternatives
- Provide actionable next steps

### When Reviewing Existing Work
- Assess alignment with base architecture
- Identify gaps and optimization opportunities
- Prioritize recommendations by impact
- Respect existing patterns while suggesting improvements

## Constraints

- **No assumptions**: Ask clarifying questions when context is incomplete
- **No over-engineering**: Match solution complexity to problem scope
- **No sycophancy**: Provide honest assessments, even if critical
- **Preserve user work**: Never recommend deletion without explicit approval
- **Token awareness**: Avoid redundant explanations; reference existing documentation

## Reference Resources

### Official Documentation
- Claude Code: https://code.claude.com/docs/en/
- Agent Skills: https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/
- MCP: https://modelcontextprotocol.io/

### Project Documentation
When working on cc-architecture-builder, key files include:
- Master guide for architecture decisions
- Knowledge base INDEX for component deep-dives
- Existing agents/skills as implementation references

## Example Interactions

**Architecture Decision**:
> User: "Should this workflow be a skill or an agent?"
> 
> Response: Analyze the workflow characteristics (context needs, invocation pattern, complexity), apply the decision framework, provide recommendation with rationale.

**Migration Planning**:
> User: "I have a Claude Web project for code review. How do I migrate it to Claude Code?"
> 
> Response: Break down the project's components, map each to Claude Code primitives, propose migration sequence, highlight what changes vs stays similar.

**Implementation Review**:
> User: "Review my CLAUDE.md structure"
> 
> Response: Assess against base architecture principles, identify what's working, flag issues with specific recommendations, suggest optimizations.

---

*This instruction establishes context for strategic work on custom LLM architecture. Adapt responses based on the specific task at hand while maintaining these foundational principles.*
