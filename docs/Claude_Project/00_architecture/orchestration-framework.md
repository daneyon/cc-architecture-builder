# Orchestration Framework: Multi-Agent Product Development Pipeline

**Version**: 0.1.0-draft
**Purpose**: Design specification for a CC-native orchestration system that coordinates specialized agents through the product design lifecycle with filesystem-based state management and structured knowledge retrieval.

---

## Concept Overview

### The Problem

A full product development lifecycle (7 phases, 20+ disciplines, 60+ sub-processes) cannot be managed by a single agent in a single context window. The knowledge is too broad, the processes too varied, and the context too expensive to load all at once.

### The Solution Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    HUMAN ORCHESTRATOR                    │
│            (Strategic decisions, QA oversight)           │
└──────────────────────────┬──────────────────────────────┘
                           │
                           v
┌─────────────────────────────────────────────────────────┐
│              MAIN CLAUDE CODE SESSION                    │
│         (Lead Engineer + Process Coordinator)            │
│                                                         │
│  ┌─────────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │  rules/     │  │  State   │  │  Skill Metadata   │  │
│  │  (always)   │  │  Manager │  │  (registry index)  │  │
│  └─────────────┘  └──────────┘  └───────────────────┘  │
└──────────┬──────────────┬──────────────┬────────────────┘
           │              │              │
     ┌─────┴────┐   ┌────┴─────┐  ┌────┴──────┐
     │ Agent:   │   │ Agent:   │  │ Agent:    │
     │ app-     │   │ qa-lead  │  │ code-     │
     │ designer │   │          │  │ reviewer  │
     │          │   │ skills:  │  │           │
     │ skills:  │   │ [qa-*]   │  │ (self-    │
     │ [plan-*, │   └──────────┘  │ contained)│
     │  dev-*]  │                 └───────────┘
     └──────────┘
```

### Key Architectural Principles

1. **Human-in-the-loop**: Every phase gate requires human approval before proceeding
2. **Progressive disclosure**: Load only the knowledge needed for the current phase
3. **Context isolation**: Agents handle sustained work in their own context (zero parent cost)
4. **Filesystem-based state**: Project state persists across sessions via structured files
5. **Modular knowledge**: Skills are reusable knowledge packs, not monolithic procedures

---

## State Management System

### Project State File

Each project maintains a state file that tracks lifecycle progress:

```yaml
# .claude/project-state.yaml (or project-level equivalent)
project:
  name: "my-app"
  version: "0.1.0"
  created: "2026-02-14"
  last_updated: "2026-02-14"

lifecycle:
  current_phase: 1  # 0-6
  current_activity: "1.3"  # Sub-process ID

  phases:
    0:
      status: completed  # pending | in_progress | completed | skipped
      started: "2026-02-01"
      completed: "2026-02-05"
      gate_approved: true
      gate_approved_by: "human"
      deliverables:
        - name: "Problem Statement"
          path: "docs/phase-0/problem-statement.md"
          status: completed
        - name: "Feasibility Report"
          path: "docs/phase-0/feasibility.md"
          status: completed
    1:
      status: in_progress
      started: "2026-02-06"
      deliverables:
        - name: "PRD"
          path: "docs/phase-1/prd.md"
          status: in_progress
        - name: "KPI Framework"
          status: pending

  decisions:
    - id: "ADR-001"
      date: "2026-02-03"
      title: "Technology stack selection"
      decision: "React + FastAPI + PostgreSQL"
      rationale: "Team expertise, ecosystem maturity"

  risks:
    - id: "RISK-001"
      description: "Third-party API rate limits"
      severity: medium
      mitigation: "Implement caching layer"
      status: mitigated
```

### State Operations

| Operation | Trigger | Actor |
|---|---|---|
| Initialize state | New project setup | Orchestrator agent or command |
| Update phase status | Phase transition | Main session (human-approved) |
| Track deliverable | Deliverable created/updated | Agent or skill |
| Record decision | Architecture/design decision | Agent (with human approval) |
| Log risk | Risk identified | Any agent |
| Advance phase gate | Gate criteria met | Human (explicit approval) |

---

## Orchestrator Agent Design

### Agent Definition (Conceptual)

```yaml
name: orchestrator
description: >
  Product lifecycle orchestrator that coordinates specialized agents through
  development phases. Manages project state, enforces phase gates, and
  delegates work to appropriate specialists. Use when starting a new project,
  transitioning between phases, or coordinating multi-agent workflows.
tools: Read, Write, Edit, Bash, Grep, Glob, Search, Task
model: inherit
skills:
  - plan-manage-project
  - plan-design-implementation
  - plan-apply-strategy
```

### Orchestrator Responsibilities

1. **Phase Management**: Know which phase the project is in; enforce gate criteria
2. **Work Delegation**: Route tasks to appropriate agents based on phase and discipline
3. **State Tracking**: Read/write project state file; track deliverables and decisions
4. **Knowledge Routing**: Load phase-appropriate skills; avoid loading irrelevant context
5. **Human Checkpoints**: Surface decisions that require human input; never auto-advance gates

### Orchestrator Workflow

```
[User Request]
    → Orchestrator reads project-state.yaml
    → Determines current phase and activity
    → Identifies required discipline(s) for the task
    → Routes to appropriate agent(s) OR handles directly
    → Updates state with results
    → Reports back to user with next recommended action
```

### Phase-Agent Routing Map

| Phase | Primary Agent(s) | Skills Loaded | Typical Tasks |
|---|---|---|---|
| 0: Discovery | orchestrator (self) | `plan-apply-strategy` | Problem framing, feasibility |
| 1: Strategy | orchestrator + product-manager* | `plan-design-implementation`, `plan-manage-project` | PRD creation, roadmap |
| 2: Architecture | app-designer | `dev-analyze-architecture` | System design, data modeling |
| 3: Implementation | (main CC session) | -- (native) | Coding, integration |
| 4: Validation | qa-lead | (internal QA procedures) | Testing, bug triage |
| 5: Deployment | (commands + hooks) | -- | Deployment automation |
| 6: Operations | performance-optimizer, debugger-specialist | -- | Monitoring, optimization |

*Future agent; orchestrator handles PM duties until dedicated agent exists.

---

## Knowledge Retrieval Architecture

### Structured Knowledge Access (CC-Native RAG)

CC doesn't have native vector search, but achieves structured retrieval through:

```
┌──────────────────────────────────────────────────────┐
│  LAYER 1: Always Available (rules/)                   │
│  Core standards, principles, behavioral guidance      │
│  Access: Automatic at session start                   │
│  Cost: Fixed (~2-5k tokens)                           │
└──────────────────────────────────────────────────────┘
                         │
                         v
┌──────────────────────────────────────────────────────┐
│  LAYER 2: Indexed (skill metadata)                    │
│  Name + description of every available capability     │
│  Access: Automatic at session start                   │
│  Cost: Fixed (~1-2k tokens)                           │
└──────────────────────────────────────────────────────┘
                         │
                         v
┌──────────────────────────────────────────────────────┐
│  LAYER 3: On-Demand (skill content + references/)     │
│  Procedural knowledge, templates, domain docs         │
│  Access: When skill triggers or agent requests         │
│  Cost: Variable (loaded into requesting context)       │
└──────────────────────────────────────────────────────┘
                         │
                         v
┌──────────────────────────────────────────────────────┐
│  LAYER 4: Deep Knowledge (knowledge/ + MCP)           │
│  Large reference corpora, external data, APIs         │
│  Access: Explicit read or MCP query                    │
│  Cost: Variable (only relevant portions loaded)        │
└──────────────────────────────────────────────────────┘
```

### Knowledge Organization per Phase

Each phase has associated knowledge that should be accessible but NOT preloaded:

| Phase | Knowledge Type | Storage Location | Access Pattern |
|---|---|---|---|
| 0: Discovery | Market research templates, feasibility frameworks | `skill assets/` | Agent reads on demand |
| 1: Strategy | PRD templates, prioritization frameworks | `skill references/` + `assets/` | Skill loads reference; outputs from asset template |
| 2: Architecture | Design patterns, ADR templates, schema standards | `skill references/` | Agent reads relevant pattern |
| 3: Implementation | Coding standards, API patterns | `rules/` (always) + `skill references/` | Rules always loaded; patterns on demand |
| 4: Validation | Test plan templates, quality checklists | `skill references/` + `assets/` | Agent reads checklist |
| 5: Deployment | Deployment playbooks, rollback procedures | `command` content + `references/` | Command loads procedure |
| 6: Operations | Monitoring runbooks, incident templates | `skill references/` | Agent reads relevant runbook |

### Scaling Beyond Filesystem: MCP-Based RAG

When the knowledge base exceeds what filesystem-based retrieval can handle efficiently (~100+ files):

```
Option A: Vector Database MCP Server
  - Index all knowledge files into vector DB (e.g., ChromaDB, Qdrant)
  - MCP server provides semantic search tool
  - Agent queries: "Find architecture patterns for microservices"
  - Returns: Relevant chunks from knowledge base

Option B: Structured Index MCP Server
  - Maintain a structured index (INDEX.md or JSON manifest)
  - MCP server provides keyword + metadata search
  - Agent queries: "Phase 2 deliverable templates"
  - Returns: File paths matching criteria

Option C: Hybrid (Recommended for scaling)
  - Structured index for known queries (fast, deterministic)
  - Vector search for exploratory queries (flexible, semantic)
  - Both accessible via single MCP server
```

---

## Implementation Roadmap

### Phase A: Foundation (Current Focus)

- [x] Define product design cycle (7 phases, sub-processes)
- [x] Define A-team roles and CC mapping
- [x] Define naming conventions and directory schema
- [ ] Finalize and validate base architecture standardization
- [ ] Create standardized skill scaffold (SKILL.md + resource folders)
- [ ] Migrate existing skills/rules/agents to new naming

### Phase B: Core Agents

- [ ] Implement orchestrator agent definition
- [ ] Implement app-designer agent (multi-phase: discover -> define -> deliver)
- [ ] Implement qa-lead agent
- [ ] Implement codebase-manager agent
- [ ] Define agent-skill composition (which skills each agent references)

### Phase C: State Management

- [ ] Design project-state.yaml schema
- [ ] Implement state read/write in orchestrator
- [ ] Define phase gate criteria (machine-checkable where possible)
- [ ] Create phase-transition command(s)

### Phase D: Knowledge System

- [ ] Organize phase-specific knowledge into skill `references/` and `assets/`
- [ ] Create deliverable templates (PRD, SRD, ADR, etc.) in skill `assets/`
- [ ] Build structured index (`knowledge/INDEX.md`) for larger corpora
- [ ] Evaluate MCP-based RAG when knowledge exceeds filesystem scale

### Phase E: Integration & Testing

- [ ] Test orchestrator with real project workflow
- [ ] Validate agent delegation patterns
- [ ] Iterate on phase gate criteria based on usage
- [ ] Package as distributable plugin (cc-architecture-builder)

---

## CC Platform Constraints & Workarounds

| Constraint | Impact | Workaround |
|---|---|---|
| Agents cannot spawn sub-agents (single nesting) | Orchestrator cannot chain agent → agent | Main session acts as router; orchestrator advises, main session delegates |
| No native database | State management limited to filesystem | YAML/JSON state files; structured reads |
| No native vector search | Knowledge retrieval is keyword/path-based | Structured indexes; MCP for semantic search at scale |
| No self-scheduling | Agents can't auto-trigger phase transitions | Human triggers via commands or conversation |
| Metadata registry limit (~50-60) | Can't register unlimited skills | Prioritize global skills; domain-specific in plugins |
| No real-time collaboration | Agents work sequentially, not in parallel from user perspective | Design workflows for sequential handoffs; parallelize via background tasks where possible |

---

## Design Heuristics for Adding New Components

When considering whether to add a new skill, agent, or rule:

```
1. Does this capability already exist?
   - Check installed plugins first
   - Check if existing skill/agent covers it
   - If yes: extend, merge, or alias -- don't duplicate

2. How often will this be used?
   - Daily/every session → rules/ (always available)
   - Weekly/per project → skill or agent
   - Rarely/one project → project plugin, not global

3. What's the context cost?
   - Behavioral (always-on) → rules/ (budget: ~2-5k total)
   - Procedural (on-demand) → skill (budget: 1 metadata slot)
   - Sustained focus → agent (separate budget)
   - External access → MCP (separate budget)

4. Can it be generalized?
   - If yes → global config
   - If no → project plugin
   - If partially → core in global, specialization in plugin
```
