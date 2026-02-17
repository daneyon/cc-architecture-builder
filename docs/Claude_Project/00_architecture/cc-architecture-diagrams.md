# Claude Code Architecture — Unified Visual Reference

**Version**: 1.0 (Synthesized from multiple sessions)  
**Last Updated**: January 2026

---

## Diagram 1: Runtime Layer Architecture

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     CLAUDE CODE RUNTIME ARCHITECTURE                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│   LAYER 1: PERSISTENT MEMORY                        [Always in Context]       │
│   ════════════════════════════════════════════════════════════════════════   │
│                                                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                                                                     │    │
│   │   CLAUDE.md ──────────────► Core identity, principles, @imports     │    │
│   │        │                                                            │    │
│   │        └──► @rules/communication-style.md                          │    │
│   │        └──► @rules/coding-philosophy.md                            │    │
│   │        └──► @rules/analysis-framework.md                           │    │
│   │                                                                     │    │
│   │   Token Cost: ~2-5k tokens (YOUR CONTROL — keep lean)              │    │
│   │                                                                     │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│   LAYER 2: CAPABILITY REGISTRY                      [Metadata Only]           │
│   ════════════════════════════════════════════════════════════════════════   │
│                                                                               │
│   ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐       │
│   │                   │  │                   │  │                   │       │
│   │  SKILLS           │  │  AGENTS           │  │  COMMANDS         │       │
│   │  ───────────────  │  │  ───────────────  │  │  ───────────────  │       │
│   │  • name           │  │  • name           │  │  • name           │       │
│   │  • description    │  │  • description    │  │  • description    │       │
│   │  (content NOT     │  │  (content NOT     │  │  (content NOT     │       │
│   │   loaded yet)     │  │   loaded yet)     │  │   loaded yet)     │       │
│   │                   │  │                   │  │                   │       │
│   └───────────────────┘  └───────────────────┘  └───────────────────┘       │
│                                                                               │
│   Token Cost: ~1-2k tokens (scales with item count, truncates ~50-60)        │
│                                                                               │
│   ┌───────────────────────────────────────────────────────────────────┐      │
│   │  MCP TOOL SIGNATURES                                              │      │
│   │  • Tool names + parameter schemas from connected servers          │      │
│   │  Token Cost: ~0.5-1k per server                                   │      │
│   └───────────────────────────────────────────────────────────────────┘      │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│   LAYER 3: INVOCATION                               [On-Demand]               │
│   ════════════════════════════════════════════════════════════════════════   │
│                                                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                                                                     │    │
│   │  SKILL INVOCATION                                                   │    │
│   │  ─────────────────                                                  │    │
│   │  Trigger: /skill-name OR Claude decides based on task               │    │
│   │  Action:  SKILL.md content loads into MAIN context                  │    │
│   │           └── May @import references/, load scripts/                │    │
│   │  Impact:  Adds to YOUR context window                               │    │
│   │                                                                     │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                                                                     │    │
│   │  AGENT SPAWN                                                        │    │
│   │  ───────────                                                        │    │
│   │  Trigger: User request OR Claude decides task needs specialist      │    │
│   │  Action:  Agent spawns as SUBPROCESS with OWN context window        │    │
│   │           └── Agent's AGENT.md loads into AGENT's context           │    │
│   │           └── Agent's skills: [] loads into AGENT's context         │    │
│   │  Impact:  ZERO cost to parent context (isolated)                    │    │
│   │                                                                     │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                                                                     │    │
│   │  COMMAND EXECUTION                                                  │    │
│   │  ─────────────────                                                  │    │
│   │  Trigger: /command-name (explicit) OR Claude matches description    │    │
│   │  Action:  Command workflow executes                                 │    │
│   │           └── May invoke skills (loads into main context)           │    │
│   │           └── May spawn agents (isolated context)                   │    │
│   │  Impact:  Variable based on what command invokes                    │    │
│   │                                                                     │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│   LAYER 4: EXECUTION                                [Runtime Environments]    │
│   ════════════════════════════════════════════════════════════════════════   │
│                                                                               │
│   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│   │  MAIN CONTEXT   │    │  AGENT CONTEXT  │    │  AGENT CONTEXT  │         │
│   │  (You + Claude) │    │  (Subprocess A) │    │  (Subprocess B) │         │
│   │                 │    │                 │    │                 │         │
│   │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │         │
│   │ │ Memory      │ │    │ │ Inherited   │ │    │ │ Inherited   │ │         │
│   │ │ Layer       │ │    │ │ Memory      │ │    │ │ Memory      │ │         │
│   │ ├─────────────┤ │    │ ├─────────────┤ │    │ ├─────────────┤ │         │
│   │ │ Loaded      │ │    │ │ AGENT.md    │ │    │ │ AGENT.md    │ │         │
│   │ │ Skills      │ │    │ │ content     │ │    │ │ content     │ │         │
│   │ ├─────────────┤ │    │ ├─────────────┤ │    │ ├─────────────┤ │         │
│   │ │ MCP Tools   │ │    │ │ Agent's     │ │    │ │ Agent's     │ │         │
│   │ │             │ │    │ │ skills      │ │    │ │ skills      │ │         │
│   │ ├─────────────┤ │    │ ├─────────────┤ │    │ ├─────────────┤ │         │
│   │ │ Conversation│ │    │ │ Agent's     │ │    │ │ Agent's     │ │         │
│   │ │ History     │ │    │ │ tools       │ │    │ │ tools       │ │         │
│   │ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │         │
│   └────────┬────────┘    └────────┬────────┘    └────────┬────────┘         │
│            │                      │                      │                   │
│            └──────────────────────┴──────────────────────┘                   │
│                                   │                                          │
│                                   ▼                                          │
│                        ┌─────────────────────┐                               │
│                        │    MCP SERVERS      │                               │
│                        │    (External)       │                               │
│                        │                     │                               │
│                        │  • Stateless calls  │                               │
│                        │  • Tool providers   │                               │
│                        │  • API bridges      │                               │
│                        │  • Vector DBs       │                               │
│                        └─────────────────────┘                               │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagram 2: Global Config Directory Structure

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    GLOBAL USER CONFIG (~/.claude/)                             ║
║                         Directory ↔ Function Mapping                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

~/.claude/
│
├── CLAUDE.md ────────────────────► PERSISTENT MEMORY: Core identity
│   │                               • Always loaded at session start
│   │                               • @imports to rules/ for modularity
│   │                               • Keep lean: ~500-1000 lines max
│   │
│   └── @rules/[topic].md ────────► PERSISTENT MEMORY: Modular principles
│                                   • Loaded via @import chain
│                                   • Topic-specific (coding, communication, etc.)
│
├── settings.json ────────────────► CONFIG (not in context)
│                                   • Model selection
│                                   • Tool permissions
│                                   • Plugin enablement
│
├── rules/ ───────────────────────► PERSISTENT MEMORY (modular)
│   ├── communication-style.md      • Interaction patterns
│   ├── coding-philosophy.md        • Development principles
│   ├── analysis-framework.md       • Reasoning approaches
│   └── [domain].md                 • Domain-specific principles
│
├── skills/ ──────────────────────► CAPABILITY REGISTRY → ON-DEMAND CONTENT
│   └── [skill-name]/
│       ├── SKILL.md ─────────────► Entry point (name + description in frontmatter)
│       │                           • Metadata: always loaded (~1-2 lines)
│       │                           • Content: loaded on invocation
│       ├── references/ ──────────► Sub-knowledge (@imported by SKILL.md)
│       ├── scripts/ ─────────────► Executable utilities
│       └── examples/ ────────────► Usage examples
│
├── agents/ ──────────────────────► CAPABILITY REGISTRY → SUBPROCESS SPAWN
│   └── [agent-name].md ──────────► Agent definition
│       │                           • Metadata: name, description, model, skills
│       │                           • Spawns with OWN context window
│       │                           • skills: [] loads into AGENT's context
│       │
│       └── (Alternative: [agent-name]/AGENT.md for complex agents)
│
├── commands/ ────────────────────► CAPABILITY REGISTRY → WORKFLOW EXECUTION
│   └── [command-name].md ────────► Command definition
│                                   • Invoked via /command-name
│                                   • Can invoke skills, spawn agents
│
├── plugins/ ─────────────────────► EXTERNAL EXTENSIONS
│   ├── cache/ ───────────────────► Installed plugin content
│   └── marketplaces/ ────────────► Marketplace repository clones
│                                   • Each plugin has own skills/agents/commands
│                                   • Merged into capability registry
│
└── [system-managed]/ ────────────► AUTO-GENERATED (don't modify)
    ├── projects/                   • Project-specific settings
    ├── todos/                      • Task tracking
    ├── statsig/                    • Feature flags
    └── ...                         • Various internal state

```

---

## Diagram 3: Token Budget Summary

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         TOKEN BUDGET ARCHITECTURE                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   FIXED COSTS (Every Session)                                               │
│   ═══════════════════════════════════════════════════════════════════════  │
│                                                                             │
│   ┌─────────────────────────────────────────────────────┬────────────────┐ │
│   │  Component                                          │  Token Cost    │ │
│   ├─────────────────────────────────────────────────────┼────────────────┤ │
│   │  System prompt base                                 │  ~2-3k         │ │
│   │  CLAUDE.md + rules/ (YOUR CONTROL)                  │  ~2-5k         │ │
│   │  Skill/Agent/Command metadata                       │  ~1-2k         │ │
│   │  MCP tool signatures                                │  ~0.5-1k/server│ │
│   ├─────────────────────────────────────────────────────┼────────────────┤ │
│   │  BASELINE OVERHEAD                                  │  ~6-12k        │ │
│   └─────────────────────────────────────────────────────┴────────────────┘ │
│                                                                             │
│   ⚠️  Keep Memory Layer lean to maximize conversation headroom              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   VARIABLE COSTS (On-Demand)                                                │
│   ═══════════════════════════════════════════════════════════════════════  │
│                                                                             │
│   ┌─────────────────────────────────────────────────────┬────────────────┐ │
│   │  Action                                             │  Impact        │ │
│   ├─────────────────────────────────────────────────────┼────────────────┤ │
│   │  Skill invocation                                   │  +Variable     │ │
│   │  (loads into MAIN context)                          │  (your cost)   │ │
│   ├─────────────────────────────────────────────────────┼────────────────┤ │
│   │  Agent spawn                                        │  +0            │ │
│   │  (isolated subprocess)                              │  (agent's cost)│ │
│   ├─────────────────────────────────────────────────────┼────────────────┤ │
│   │  Conversation history                               │  +Grows        │ │
│   │  (until auto-compaction)                            │                │ │
│   └─────────────────────────────────────────────────────┴────────────────┘ │
│                                                                             │
│   💡 KEY INSIGHT: Agent spawns are "free" to parent context                 │
│      → Load skill-heavy agents without impacting main conversation          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagram 4: Component Decision Framework

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      WHERE DOES THIS CONTENT BELONG?                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

                            ┌─────────────────────┐
                            │   NEW CONTENT TO    │
                            │      ORGANIZE       │
                            └──────────┬──────────┘
                                       │
                                       ▼
                    ┌──────────────────────────────────┐
                    │  Is it WHO you are or HOW you    │
                    │  should ALWAYS behave?           │
                    └──────────────────┬───────────────┘
                                       │
                    ┌──────────────────┴───────────────┐
                    │                                  │
                   YES                                 NO
                    │                                  │
                    ▼                                  ▼
        ┌───────────────────┐           ┌──────────────────────────┐
        │                   │           │  Is it procedural        │
        │   MEMORY LAYER    │           │  knowledge (HOW to do    │
        │                   │           │  a specific task)?       │
        │  • CLAUDE.md      │           └────────────┬─────────────┘
        │  • rules/*.md     │                        │
        │                   │           ┌────────────┴─────────────┐
        │  Token: ALWAYS    │           │                          │
        │  loaded           │          YES                         NO
        └───────────────────┘           │                          │
                                        ▼                          ▼
                            ┌───────────────────┐    ┌─────────────────────────┐
                            │                   │    │  Does it need separate  │
                            │      SKILL        │    │  context or sustained   │
                            │                   │    │  complex work?          │
                            │  • Lazy-loaded    │    └────────────┬────────────┘
                            │  • Reusable       │                 │
                            │  • Can have       │    ┌────────────┴────────────┐
                            │    references/    │    │                         │
                            │    scripts/       │   YES                        NO
                            └───────────────────┘    │                         │
                                                     ▼                         ▼
                                        ┌───────────────────┐    ┌───────────────────┐
                                        │                   │    │                   │
                                        │      AGENT        │    │  REFERENCE ONLY   │
                                        │                   │    │                   │
                                        │  • Own context    │    │  • Knowledge base │
                                        │  • Can load       │    │  • Read on-demand │
                                        │    skills         │    │  • Not a component│
                                        │  • Subprocess     │    │                   │
                                        └───────────────────┘    └───────────────────┘


╔═══════════════════════════════════════════════════════════════════════════════╗
║                      SKILL vs AGENT: DETAILED HEURISTICS                       ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌───────────────────────────────────────┬───────────────────────────────────────┐
│           USE A SKILL WHEN...         │           USE AN AGENT WHEN...        │
├───────────────────────────────────────┼───────────────────────────────────────┤
│                                       │                                       │
│ • Knowledge is reusable across        │ • Task needs sustained focus with     │
│   multiple contexts                   │   specialized reasoning               │
│                                       │                                       │
│ • You want Claude to auto-invoke      │ • Work benefits from isolated         │
│   based on task context               │   context (won't pollute main)        │
│                                       │                                       │
│ • Content should load into MAIN       │ • Agent needs to load multiple        │
│   context for current conversation    │   skills without impacting parent     │
│                                       │                                       │
│ • It's procedural "how to" knowledge  │ • It's a specialized persona with     │
│                                       │   distinct workflow                   │
│                                       │                                       │
│ • Update once, benefit everywhere     │ • Task may need to be resumed         │
│                                       │   (agents support resumption)         │
│                                       │                                       │
├───────────────────────────────────────┼───────────────────────────────────────┤
│  EXAMPLES:                            │  EXAMPLES:                            │
│  • pdf-processing                     │  • code-reviewer                      │
│  • code-standards                     │  • research-analyst                   │
│  • documentation-templates            │  • project-integrator                 │
│  • prompting-techniques               │  • strategic-advisor                  │
└───────────────────────────────────────┴───────────────────────────────────────┘
```

---

## Diagram 5: Plugin Architecture (Distribution)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    DISTRIBUTABLE PLUGIN ARCHITECTURE                           ║
║                      (Schema 2: Project-Level Config)                          ║
╚═══════════════════════════════════════════════════════════════════════════════╝

your-plugin/
│
├── .claude-plugin/
│   └── plugin.json ──────────────► REQUIRED: Marketplace metadata
│                                   • name, version, description
│                                   • author, repository, keywords
│
├── CLAUDE.md ────────────────────► Project memory (team-shared)
│                                   • Project-specific instructions
│                                   • @imports to knowledge/
│
├── CLAUDE.local.md ──────────────► Personal overrides (gitignored)
│                                   • Your local preferences
│                                   • Not distributed
│
├── .claude/
│   ├── rules/ ───────────────────► Project rules (modular)
│   │   └── [topic].md              • Path-specific rules supported
│   │                               • Loaded at session start
│   │
│   └── settings.json ────────────► Project settings
│                                   • Model, permissions overrides
│
├── .mcp.json ────────────────────► Project MCP servers
│                                   • Scoped to this project
│
├── skills/ ──────────────────────► Project skills
│   └── [skill-name]/
│       └── SKILL.md
│
├── agents/ ──────────────────────► Project agents
│   └── [agent-name].md
│
├── commands/ ────────────────────► Project commands
│   └── [command-name].md
│
├── hooks/
│   └── hooks.json ───────────────► Event handlers
│
├── knowledge/ ───────────────────► Domain knowledge base
│   ├── INDEX.md                    • Entry point
│   └── [topics]/                   • Organized by topic
│
└── docs/
    └── README.md ────────────────► Documentation


╔═══════════════════════════════════════════════════════════════════════════════╗
║                      GLOBAL + PROJECT MERGE BEHAVIOR                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

When working in a project with a plugin installed:

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   MEMORY PRECEDENCE (Higher = Loaded First, Takes Priority)                 │
│   ═══════════════════════════════════════════════════════════════════════  │
│                                                                             │
│   1. Enterprise Policy     │  /etc/claude-code/CLAUDE.md (if exists)       │
│   2. Project Memory        │  ./CLAUDE.md                                  │
│   3. Project Rules         │  ./.claude/rules/*.md                         │
│   4. User Memory           │  ~/.claude/CLAUDE.md                          │
│   5. Project Local         │  ./CLAUDE.local.md                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   CAPABILITY MERGE (All visible, names can shadow)                          │
│   ═══════════════════════════════════════════════════════════════════════  │
│                                                                             │
│   Skills:   Global ~/.claude/skills/ + Project skills/ + Plugin skills/     │
│   Agents:   Global ~/.claude/agents/ + Project agents/ + Plugin agents/     │
│   Commands: Global ~/.claude/commands/ + Project commands/ + Plugin commands│
│                                                                             │
│   ⚠️ Name conflicts: Project-level shadows global-level                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Summary: What We Learned From CC CLI Conversation

| Insight | Impact on Our Architecture |
|---------|---------------------------|
| **Skill metadata vs content loading** | Confirms lazy-loading; design skill-heavy agents without parent context concern |
| **Agent subprocess isolation** | Agents with `skills:` are "free" to parent context; use liberally |
| **Memory unification** | CLAUDE.md + rules/ = unified "Memory Layer"; cleaner mental model |
| **Token budget quantification** | ~6-12k baseline; keep Memory Layer under ~5k for headroom |
| **Progressive disclosure confirmed** | Memory → Registry → Invocation → Execution is optimal |

