# A-Team Blueprint: Product Team → Claude Code Architecture

**Version**: 0.2.0-draft
**Data Source**: `a-team-database.yaml` (machine-parseable), `cc-component-registry.yaml` (component index)
**Purpose**: Human-readable summary with visualizations. For agentic workflows, read the YAML files directly.

---

## 1. Product Design Lifecycle (7 Phases)

```
 Phase 0       Phase 1         Phase 2          Phase 3          Phase 4        Phase 5        Phase 6
 DISCOVERY --> STRATEGY -----> ARCHITECTURE --> IMPLEMENTATION -> VALIDATION --> DEPLOYMENT --> OPERATIONS
 [Problem]     [Plan]          [Design]         [Build]          [Test]         [Ship]         [Grow]
    |              |               |                |                |              |              |
  Gate:          Gate:           Gate:            Gate:            Gate:          Gate:          Ongoing
  Problem        PRD approved    Architecture     Features done    Tests pass     Production     Continuous
  validated      Roadmap set     approved         Code reviewed    Perf met       Monitoring     improvement
```

---

## 2. Phase-Role Activation Matrix

Roles grouped by when they're most active. Read across to see which phases each role participates in.

```
                          Phase: 0   1   2   3   4   5   6
                                Dis Str Arc Imp Val Dep Ops
TIER 1: LEADERSHIP              │   │   │   │   │   │   │
  Business Strategist           X   X   .   .   .   .   X
  Product Manager               X   X   X   X   X   X   X
  Project Manager               X   X   X   X   X   X   X
                                │   │   │   │   │   │   │
TIER 2: DEFINITION              │   │   │   │   │   │   │
  Business Analyst              X   X   X   .   .   .   .
  Product Marketer              .   X   .   .   .   X   .
  UX Researcher                 X   X   X   .   X   .   .
  UX Designer                   .   X   X   X   .   .   .
  UI Designer                   .   .   X   X   .   .   .
                                │   │   │   │   │   │   │
TIER 3: ENGINEERING             │   │   │   │   │   │   │
  Software Architect            .   X   X   X   X   .   X
  Frontend/Backend Engineer     .   .   X   X   X   .   X
  Database Engineer             .   .   X   X   .   .   X
  DevOps / SRE                  .   .   X   X   .   X   X
  Security Engineer             .   .   X   X   X   .   X
  Code Reviewer                 .   .   .   X   X   .   X
  Debugger                      .   .   .   X   X   .   X
  Codebase Manager              .   .   .   X   .   .   X
                                │   │   │   │   │   │   │
TIER 4: QUALITY                 │   │   │   │   │   │   │
  QA Lead                       .   .   X   X   X   .   .
  Performance Engineer          .   .   .   .   X   .   X
                                │   │   │   │   │   │   │
TIER 5: OPERATIONS              │   │   │   │   │   │   │
  Technical Writer              .   .   .   X   X   X   X
  Data Analyst                  X   X   .   .   X   .   X
  Customer Success              .   .   .   .   .   X   X
```

---

## 3. Role → CC Component Mapping

Every role maps to exactly ONE primary CC component type. The rationale follows the decision tree:

```
Always-on behavior/standards?  --> rules/     (zero metadata cost)
Procedural "how-to" knowledge? --> skill      (1 metadata slot, lazy-loaded)
Sustained focus / own context? --> agent      (separate budget, isolated)
Repeatable workflow trigger?   --> command    (1 metadata slot)
Event-driven automation?       --> hook       (zero context cost)
Core Claude Code capability?   --> native     (no component needed)
```

### By CC Component Type

**AGENTS (11)** -- Roles requiring sustained focus, isolated context, or specialized persona:

| Role | Agent Name | Skills Loaded | Priority |
|---|---|---|---|
| Product Manager | `product-manager` | `plan-manage-project`, `plan-design-implementation` | p1 |
| UX Researcher | `ux-researcher` | -- | p2 |
| UX Designer | `ux-designer` | -- | p1 |
| Software Architect | `software-architect` | `dev-analyze-architecture` | p1 |
| Security Engineer | `security-auditor` | -- | p2 |
| Code Reviewer | `code-reviewer` | -- | p0 |
| Debugger | `debugger-specialist` | -- | p0 |
| Codebase Manager | `codebase-manager` | `dev-analyze-architecture` | p1 |
| QA Lead | `qa-lead` | -- | p1 |
| Performance Engineer | `performance-optimizer` | -- | p0 |
| Technical Writer | `tech-writer` | `doc-generate-readme` | p1 |

**SKILLS (16)** -- Roles whose knowledge is procedural, reusable, on-demand:

| Role(s) Served | Skill Name | Domain | Priority |
|---|---|---|---|
| Software Architect, Codebase Manager | `dev-analyze-architecture` | dev | p0 |
| Database Engineer | `dev-design-data-model` | dev | p1 |
| UI Designer | `dev-design-ui` | dev | p2 |
| Technical Writer | `doc-generate-readme` | doc | p0 |
| (All) | `doc-export-session` | doc | p0 |
| Software Architect, Business Analyst | `doc-design-diagram` | doc | p1 |
| Business Analyst, Product Manager | `plan-design-implementation` | plan | p0 |
| Business Strategist | `plan-apply-strategy` | plan | p1 |
| Project Manager, Product Manager | `plan-manage-project` | plan | p1 |
| Product Marketer | `plan-design-gtm` | plan | p2 |
| Data Analyst | `plan-analyze-metrics` | plan | p2 |
| (AI interaction) | `ai-engineer-prompt` | ai | p1 |
| (AI interaction) | `ai-search-docs` | ai | p0 |
| (AI interaction) | `ai-optimize-tokens` | ai | p1 |
| (AI interaction) | `ai-design-agent` | ai | p1 |
| Customer Success | `ops-manage-feedback` | ops | p2 |

**COMMANDS (3)** -- Workflow triggers:

| Workflow | Command Name | Priority |
|---|---|---|
| Git workflow | `commit-push-pr` | p0 |
| Project initialization | `init-project` | p1 |
| Phase gate transition | `advance-phase` | p2 |

**HOOKS (2)** -- Event-driven automation:

| Event | Hook Name | Priority |
|---|---|---|
| Pre-commit | `pre-commit-quality` | p1 |
| Session end | `post-session-export` | p2 |

**NATIVE** (no CC component needed):

| Role | Rationale |
|---|---|
| Frontend Engineer | Core Claude Code execution capability |
| Backend Engineer | Core Claude Code execution capability |

---

## 4. Scaling Model

How the team composition changes with team size. Each tier is additive.

### Solo Developer + AI (15 roles AI-augmented)

```
HUMAN: Business Lead + PM + Developer
AI CC: 4 rules domains, 6 skills (p0), 3 agents (p0), 1 command (p0)

rules/:  dev/, comm/                      (always-on standards)
skills:  dev-analyze-architecture          (code quality)
         doc-generate-readme               (documentation)
         doc-export-session                (session management)
         plan-design-implementation        (project planning)
         ai-search-docs                   (CC reference)
         ai-optimize-tokens               (efficiency)
agents:  code-reviewer                     (quality gate)
         debugger-specialist               (incident response)
         performance-optimizer             (optimization)
commands: commit-push-pr                   (git workflow)
```

### Small Team (3-5 people, 13 roles)

```
ADDITIVE CC:
skills:  + plan-apply-strategy, plan-manage-project, doc-design-diagram
agents:  + qa-lead, ux-designer, software-architect
```

### Medium Team (6-15 people, 20 roles)

```
ADDITIVE CC:
rules/:  + gov/, process/                 (governance, standards)
skills:  + dev-design-data-model, ai-engineer-prompt, ai-design-agent
agents:  + product-manager, codebase-manager, tech-writer
commands: + init-project
hooks:   + pre-commit-quality
```

### Enterprise (15+ people, 22 roles)

```
ADDITIVE CC:
skills:  + plan-design-gtm, plan-analyze-metrics, dev-design-ui, ops-manage-feedback
agents:  + ux-researcher, security-auditor
commands: + advance-phase
hooks:   + post-session-export
MCP:     + project management, CI/CD, monitoring integrations
```

---

## 5. Multi-Agent Architecture

### How Agents Interact in CC Runtime

```
┌──────────────────────────────────────────────────────────────────────┐
│                      HUMAN (Orchestrator Layer)                      │
│  Strategic decisions, phase gate approvals, QA oversight             │
└──────────────────────────────────┬───────────────────────────────────┘
                                   │
                                   v
┌──────────────────────────────────────────────────────────────────────┐
│                    MAIN CLAUDE CODE SESSION                          │
│                    (Lead Engineer + Router)                          │
│                                                                      │
│  ALWAYS LOADED:                                                      │
│    rules/dev/*    rules/comm/*    rules/gov/*    rules/process/*     │
│                                                                      │
│  METADATA INDEX (name + description only):                           │
│    [16 skills]  [3 commands]                                         │
│                                                                      │
│  CAPABILITIES:                                                       │
│    - Read/write project state files                                  │
│    - Spawn agents via Task tool                                      │
│    - Load skills on demand                                           │
│    - Execute commands                                                │
│    - Route work to appropriate specialist                            │
└────────┬──────────┬──────────┬──────────┬──────────┬────────────────┘
         │          │          │          │          │
    ┌────┴───┐ ┌────┴───┐ ┌───┴────┐ ┌───┴────┐ ┌──┴──────┐
    │ Agent: │ │ Agent: │ │ Agent: │ │ Agent: │ │ Agent:  │
    │ code-  │ │ qa-    │ │ soft-  │ │ debug- │ │ tech-   │
    │ review │ │ lead   │ │ ware-  │ │ ger    │ │ writer  │
    │ er     │ │        │ │ archi- │ │ spec-  │ │         │
    │        │ │        │ │ tect   │ │ ialist │ │ skills: │
    │ (self) │ │ (self) │ │        │ │        │ │ [doc-   │
    │        │ │        │ │ skills:│ │ (self) │ │ generate│
    └────────┘ └────────┘ │ [dev-  │ └────────┘ │ -readme]│
                          │ analyz │             └─────────┘
                          │ e-arch │
                          │ itectu │
                          │ re]    │
                          └────────┘

CONSTRAINTS:
  - Agents have ISOLATED context (zero cost to parent session)
  - Agents CANNOT spawn sub-agents (single nesting level)
  - Agent results return to main session as text
  - Main session routes all inter-agent coordination
```

### Agent-Skill Loading Pattern

```
Agent spawned via Task tool
    │
    ├── Agent definition (.md) loaded into agent context
    ├── skills: [skill-a, skill-b] loaded into agent context
    ├── Agent executes with its own context window
    │
    └── Returns result to main session (text only)

Cost model:
  Main session:  0 tokens (agent is isolated subprocess)
  Agent session:  agent.md + skill-a SKILL.md + skill-b SKILL.md + task work
```

---

## 6. Team Formation as Agentic Workflow

This blueprint is designed to be consumed by a "team formation" skill or command during project initialization:

```
TRIGGER: User starts new project or invokes /init-project

WORKFLOW:
  1. Read a-team-database.yaml
  2. Assess project characteristics:
     - Complexity (solo / small / medium / enterprise)
     - Domain (web app / API / data pipeline / automation / etc.)
     - Phases needed (full lifecycle or subset)
  3. Filter roles by scaling tier and relevant phases
  4. Generate project team roster:
     - Which agents to create/activate
     - Which skills to prioritize
     - Which rules to enforce
     - Which commands to enable
  5. Output: project-specific team manifest (YAML)
  6. Human reviews and approves team composition
  7. Scaffold project with approved CC components
```

This workflow would be implemented as:
- **Skill**: `ai-design-agent` (knowledge of how to compose agents)
- **Command**: `init-project` (trigger that invokes the skill and scaffolds)
- **Data**: `a-team-database.yaml` + `cc-component-registry.yaml` (read by skill)

---

## Data Files Reference

| File | Format | Purpose | Consumer |
|---|---|---|---|
| `a-team-database.yaml` | YAML | Full role roster with CC mapping, phases, scaling | Agentic workflows, team formation skill |
| `cc-component-registry.yaml` | YAML | All CC components with status, mapping, priority | Migration scripts, validation tools |
| `a-team-blueprint.md` | Markdown | Human-readable summary with visualizations | Human reference |
| `product-design-cycle.md` | Markdown | Lifecycle phases, sub-processes, deliverables | Human reference, skill references/ |
