# Claude Code (CC) Architecture Master Strategist — Project Status (2026-01-28 v2)

**Status Summary**: Comprehensive record of cc-architecture-builder development progress

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

| Component          | Status      | Location                                    |
| ------------------ | ----------- | ------------------------------------------- |
| Master Guide       | ✅ Complete | `docs/claude_code_architecture_guide.md`  |
| Executive Summary  | ✅ Complete | `knowledge/overview/executive-summary.md` |
| Memory System KB   | ✅ Complete | `knowledge/components/memory-claudemd.md` |
| Agent Skills KB    | ✅ Complete | `knowledge/components/agent-skills.md`    |
| Subagents KB       | ✅ Complete | `knowledge/components/subagents.md`       |
| MCP Integration KB | ✅ Complete | `knowledge/components/mcp-integration.md` |
| References KB      | ✅ Complete | `knowledge/appendices/references.md`      |

**Key v0.5.0 Updates**:

- Documentation domain: `docs.anthropic.com` → `code.claude.com`
- Memory hierarchy: 4-tier → 5-tier (added Project Rules)
- New `.claude/rules/` system with path-specific frontmatter
- Built-in subagents documented (General-purpose, Plan, Explore)
- MCP scopes updated (local/project/user)

### 2. Plugin Project Structure

Below is an example plugin project structure standard. In practice, this CC plugin folder will be under the project root directory (e.g. [project-name]/[CCplugin_name]/...), which effectively differentiates from claude code-related materials and the actual project/codebase content for efficient project management.

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
├── knowledge/                    ✅ Plugin-specific Modular KB packs (for AI/LLM)
│   ├── INDEX.md
│   ├── overview/
│   ├── schemas/
│   ├── components/
│   ├── implementation/
│   ├── operational-patterns/
│   └── appendices/
└── docs/
    └── claude_code_architecture_guide.md  ✅ Project-specific domain content (for human user)
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

## Critical Runtime Architecture Insights

> **Source**: Validated via Claude Code CLI session (2026-01-15)

### Token Budget Architecture

Understanding token costs is essential for efficient architecture design:

```
FIXED COSTS (Every Session):
┌─────────────────────────────────────────────────────┬────────────────┐
│  Component                                          │  Token Cost    │
├─────────────────────────────────────────────────────┼────────────────┤
│  System prompt base                                 │  ~2-3k         │
│  CLAUDE.md + rules/ (YOUR CONTROL)                  │  ~2-5k         │
│  Skill/Agent/Command metadata                       │  ~1-2k         │
│  MCP tool signatures                                │  ~0.5-1k/server│
├─────────────────────────────────────────────────────┼────────────────┤
│  BASELINE OVERHEAD                                  │  ~6-12k        │
└─────────────────────────────────────────────────────┴────────────────┘

VARIABLE COSTS (On-Demand):
┌─────────────────────────────────────────────────────┬────────────────┐
│  Action                                             │  Impact        │
├─────────────────────────────────────────────────────┼────────────────┤
│  Skill invocation                                   │  +Variable     │
│  (loads into MAIN context)                          │  (your cost)   │
├─────────────────────────────────────────────────────┼────────────────┤
│  Agent spawn                                        │  +0            │
│  (isolated subprocess)                              │  (agent's cost)│
├─────────────────────────────────────────────────────┼────────────────┤
│  Conversation history                               │  +Grows        │
│  (until auto-compaction)                            │                │
└─────────────────────────────────────────────────────┴────────────────┘
```

### Skill Loading Behavior (Critical Clarification)

| What | When Loaded | Where Loaded | Token Impact |
|------|-------------|--------------|--------------|
| **Skill metadata** | Session start | Main context | ~1-2 lines per skill (LOW) |
| **Skill content** | On `/skill` invocation | Main context | Variable (HIGH) |
| **Agent with skills: field** | Agent spawn | Agent's context (subprocess) | **ZERO cost to parent** |

**Key Insight**: When you spawn an agent with `skills: ["pdf", "docx"]`, those skills load into the AGENT's context, not yours. The parent conversation is unaffected. This means:

- Agents can be skill-heavy without impacting main conversation
- Loading skills into agents is "free" from parent context perspective
- Use agents liberally for skill-heavy tasks

### Runtime Layer Model

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LAYER 1: PERSISTENT MEMORY (Always in Context)                         │
│  ═══════════════════════════════════════════════════════════════════   │
│  CLAUDE.md + rules/*.md = Unified "Memory Layer"                        │
│  Token Cost: ~2-5k (YOUR CONTROL — keep lean)                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  LAYER 2: CAPABILITY REGISTRY (Metadata Only)                           │
│  ═══════════════════════════════════════════════════════════════════   │
│  Skills / Agents / Commands: name + description loaded                  │
│  Token Cost: ~1-2k (scales with count, truncates ~50-60 items)          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  LAYER 3: INVOCATION (On-Demand)                                        │
│  ═══════════════════════════════════════════════════════════════════   │
│  Skill invocation → Content loads into MAIN context                     │
│  Agent spawn → Subprocess with OWN context (isolated from parent)       │
│  Command execution → May invoke skills/spawn agents                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  LAYER 4: EXECUTION (Runtime Environments)                              │
│  ═══════════════════════════════════════════════════════════════════   │
│  Main Context (You + Claude) ←→ Agent Subprocesses ←→ MCP Servers       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## What Is In Progress

### Global User Config Migration

**Current State** (`~/.claude/`):

| Component         | Status                    | Notes                                                                                                                                                                                                                                                          |
| ----------------- | ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `settings.json` | ⚠️ may need restructure | need review after everything else has been enhanced                                                                                                                                                                                                           |
| `CLAUDE.md`     | ⚠️ Needs restructure    | Currently monolithic, should be lean to contain core principles only and other additional memory contexts via modularized rules + appropriate @imports                                                                                                        |
| `rules/`        | ⚠️ Needs restructure    | Ready for modularized rules via existing KB resources from Claude Project framework; need template creation                                                                                                                                                    |
| `skills/`       | ⚠️ Needs restructure    | Need template alignment via existing 'skill-creator' skill, reference updates                                                                                                                                                                                  |
| `agents/`       | ⚠️ Needs restructure    | Need template creation (follows general CC architect pipeline philosophy)                                                                                                                                                                                      |
| `commands/`     | ⚠️ Needs restructure   | Need template creation (follows general CC architect pipeline philosophy)                                                                                                                                                                                      |
| `roles/`        | ⚠️ TBD                  | Custom character modes beyond built-in (e.g., "max-token-efficiency" mode). Relationship to native character modes needs clarification.                                                                                                                       |

**Proposed Target Structure (w/ draft examples as reference-only)**:

```
~/.claude/
├── CLAUDE.md                    # Lean: core identity/principles + @imports
├── settings.json                # global cc setting
├── rules/                       # Modular principles (part of Memory Layer)
├── skills/                      # Procedural capabilities (lazy-loaded)
├── agents/                      # Specialized assistants (spawn as subprocess)
├── commands/                    # Workflow shortcuts
├── plugins/                     # Installed external plugins
├── mcp_[].json                  # Global/user-level MCP configs
└── [system folders]             # Auto-generated and managed by CC
```

### Knowledge Base Mapping & Modularization (global-level)

*** TBD. Need to review existing KB resources from Claude Projects and other external plugins installed beforehand, then update KB structure as well as context management standards. Once architecture is reviewed, actual contents of specific files will be reviewed.

| Size                   | Approach                                                                                                                            |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **< 20 files**   | Current approach is fine. Use `@imports` in CLAUDE.md for critical files.                                                         |
| **20-100 files** | Create `knowledge/INDEX.md` listing what exists. Use skills that reference specific files. Structure subdirectories meaningfully. |
| **100+ files**   | Consider MCP integration with a vector database for actual semantic retrieval. Folder-only approach won't scale.                    |

 **On `knowledge/` vs `docs/`** :

These serve different audiences:

* `docs/` = Documentation FOR HUMANS using your plugin (setup guides, how-to)
* `knowledge/` = Content FOR AI/CLAUDE CODE to reference when answering domain questions

---

## Key Architectural Insights

### Decision Tree: Where Does Content Belong?

```
Is it about WHO you are / HOW Claude should ALWAYS behave?
├─ YES → MEMORY LAYER (CLAUDE.md or rules/)
│        Token: ALWAYS loaded (~2-5k budget)
│
└─ NO → Is it about HOW to do a specific task?
        ├─ YES → SKILL
        │        Token: Lazy-loaded on invocation (adds to MAIN context)
        │
        └─ NO → Does it need sustained focus or separate context?
                ├─ YES → AGENT
                │        Token: ISOLATED (subprocess, free to parent)
                │
                └─ NO → Is it a repeatable workflow/shortcut?
                        ├─ YES → COMMAND
                        │        Token: Variable (may invoke skills/agents)
                        │
                        └─ NO → Reference material (knowledge base)
                                 Token: Only when @imported or read
```

### Component Invocation Patterns

| Component | Invocation | Trigger | Context Impact |
|-----------|------------|---------|----------------|
| Memory (CLAUDE.md + rules/) | Automatic | Always loaded at session start | MAIN context (fixed) |
| Skills (metadata) | Automatic | Session start | MAIN context (~1-2 lines each) |
| Skills (content) | Model-invoked or `/skill` | Task context match or explicit | MAIN context (variable) |
| Agents | Model or user-invoked | Task match or explicit | OWN context (isolated) |
| Commands | User-invoked or model-matched | `/command` or description match | Variable |
| Hooks | Event-driven | System events | Depends on hook action |

### General CC Architect Pipeline (Skills → Agents/Commands → MCP)

General hierarchical, progressive vision:

1. **KB packs** become **Skills** (procedural capabilities)
2. **Skills** are composed into **Agents** (specialized assistants with own context) or **Commands** (workflow shortcuts)
3. **Agents** can form a **multi-agent network** (coordinated by main Claude) or connect to **MCPs** (esp. when more efficient, specialized RAG framework(s) are needed)
4. For Claude Code specifically, all of this is then "wrapped" as a distributable plugin via marketplace.

Claude Code doesn't natively orchestrate multi-agent networks, but agents with `skills:` field effectively create coordination by loading relevant skills into the agent's context (at zero cost to parent).

**Design Heuristics: Skill vs Agent**

| Use SKILL when... | Use AGENT when... |
|-------------------|-------------------|
| Knowledge is reusable across contexts | Task needs sustained focus with specialized reasoning |
| Auto-invoke based on task context desired | Work benefits from isolated context |
| Content should load into MAIN context | Agent needs multiple skills without impacting parent |
| Procedural "how to" knowledge | Specialized persona with distinct workflow |
| Update once, benefit everywhere | Task may need resumption |

---

## Pending To-Do Tasks

| Task | Priority | Status |
|------|----------|--------|
| Review the latest project status and cc-architecture-builder plugin to see what is still left to officially deploy plugin to marketplace for me to start actually install to my local and use/test it "in-the-wild", so I can iteratively optimize/update the plugin as I finalize standardizing my local global config as updated base architecture. | High | Pending |
| Review other available plugin architectures and finalize first v1 of cc-architecture-builder plugin to be effectively deployed and usable in my local env | High | Pending |
| Continue restructuring global config with tested cc-architecture-builder plugin tools: Modularize global config `knowledge-base/` → rules/skills/agents/commands/etc., Restructure global CLAUDE.md (lean version), Review available marketplace plugins, Create more tailored practical commands, skills, agents, rules, etc. | Medium | Pending |
| Once global config base architecture is finalized, test all available CC tools (commands, agents, skills) as needed. E.g., test project-integrator agent on existing project, test architecture-advisor agent on a new project/app design idea | Low | Pending |
| Deeper exploration of Knowledge Base Mapping & Modularization (global-level) with tailored RAG frameworks/techniques/tools | Low | Pending |

---

## Reference Links

### Official Documentation (code.claude.com)

Use existing 'claude-docs-helper' skill to search for the latest official Claude Code docs as reference.

- Overview: https://code.claude.com/docs/en/overview
- Memory: https://code.claude.com/docs/en/memory
- Skills: https://code.claude.com/docs/en/skills, https://agentskills.io/specification
- Subagents: https://code.claude.com/docs/en/sub-agents
- MCP: https://code.claude.com/docs/en/mcp, https://modelcontextprotocol.io/
- Plugins: https://code.claude.com/docs/en/plugins

---

## Session Handoff Notes for Claude Code

**What was validated in Claude Web Project session (2026-01-28)**:

1. ✅ Two-schema architecture confirmed
2. ✅ Token budget insights from CC CLI incorporated
3. ✅ Skill lazy-loading behavior clarified (metadata vs content)
4. ✅ Agent context isolation confirmed (subprocess, zero cost to parent)
5. ✅ Decision tree updated to include Commands and token impact
6. ✅ Runtime layer model documented

**Immediate next steps for Claude Code**:

1. Review other available plugin architectures (5-6 external plugins)
2. Determine what enhancements to adopt for cc-architecture-builder
3. Finalize v1 plugin structure for deployment
4. Test plugin installation and validation in local environment

**Key files to review in cc-architecture-builder**:
- `docs/claude_code_architecture_guide.md` — Master guide
- `knowledge/INDEX.md` — KB entry point
- `agents/project-integrator.md` — Main operational agent
- `agents/architecture-advisor.md` — Consultative agent
- `skills/quick-scaffold/SKILL.md` — Fast scaffolding skill
