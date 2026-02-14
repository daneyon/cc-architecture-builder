# Claude Code Architecture — Final Visual Reference v1.0

**Synthesized from**: CC CLI conversation (Jan 15, 2026) + Claude Project session (Jan 28, 2026)  
**Version**: 1.0  
**Last Updated**: January 28, 2026

---

## Diagram 1: Runtime Layer Architecture (Primary Reference)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     CLAUDE CODE RUNTIME ARCHITECTURE                           ║
║                         Four-Layer Progressive Disclosure                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  LAYER 1: PERSISTENT MEMORY                              [ALWAYS IN CONTEXT]   │
│  ════════════════════════════════════════════════════════════════════════════  │
│                                                                                 │
│    ┌──────────────────────────────────────────────────────────────────────┐    │
│    │                                                                      │    │
│    │   CLAUDE.md ─────────────────► Core identity & principles            │    │
│    │       │                                                              │    │
│    │       └──► @rules/communication-style.md                             │    │
│    │       └──► @rules/coding-philosophy.md                               │    │
│    │       └──► @rules/analysis-framework.md                              │    │
│    │                                                                      │    │
│    │   💡 Design principle: Keep lean (~500-1000 lines max)               │    │
│    │                                                                      │    │
│    └──────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│    Token Cost: ~2-5k tokens ──► YOUR CONTROL (minimize for headroom)           │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  LAYER 2: CAPABILITY REGISTRY                            [METADATA ONLY]       │
│  ════════════════════════════════════════════════════════════════════════════  │
│                                                                                 │
│    ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐             │
│    │                 │   │                 │   │                 │             │
│    │    SKILLS       │   │    AGENTS       │   │   COMMANDS      │             │
│    │   ──────────    │   │   ──────────    │   │   ──────────    │             │
│    │   name + desc   │   │   name + desc   │   │   name + desc   │             │
│    │                 │   │                 │   │                 │             │
│    │   (content NOT  │   │   (content NOT  │   │   (content NOT  │             │
│    │    loaded yet)  │   │    loaded yet)  │   │    loaded yet)  │             │
│    │                 │   │                 │   │                 │             │
│    └─────────────────┘   └─────────────────┘   └─────────────────┘             │
│                                                                                 │
│    ┌────────────────────────────────────────────────────────────────────┐      │
│    │  MCP TOOL SIGNATURES                                               │      │
│    │  • Tool names + parameter schemas from connected servers           │      │
│    └────────────────────────────────────────────────────────────────────┘      │
│                                                                                 │
│    Token Cost: ~1-2k tokens ──► Scales with count (truncates ~50-60 items)     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              ▼                          ▼                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  LAYER 3: INVOCATION                                     [ON-DEMAND]           │
│  ════════════════════════════════════════════════════════════════════════════  │
│                                                                                 │
│    ┌────────────────────────────────────────────────────────────────────┐      │
│    │                                                                    │      │
│    │  SKILL INVOCATION                                                  │      │
│    │  ─────────────────                                                 │      │
│    │  Trigger: /skill-name OR Claude auto-matches based on task         │      │
│    │  Action:  SKILL.md content loads into MAIN context                 │      │
│    │           └── May @import references/, load scripts/               │      │
│    │  Impact:  ADDS TO YOUR context window (your token cost)            │      │
│    │                                                                    │      │
│    └────────────────────────────────────────────────────────────────────┘      │
│                                                                                 │
│    ┌────────────────────────────────────────────────────────────────────┐      │
│    │                                                                    │      │
│    │  AGENT SPAWN                                                       │      │
│    │  ───────────                                                       │      │
│    │  Trigger: User request OR Claude decides task needs specialist     │      │
│    │  Action:  Agent spawns as SUBPROCESS with OWN context window       │      │
│    │           └── Agent's AGENT.md loads into AGENT's context          │      │
│    │           └── Agent's skills: [] loads into AGENT's context        │      │
│    │  Impact:  ⚡ ZERO COST to parent context (fully isolated)          │      │
│    │                                                                    │      │
│    └────────────────────────────────────────────────────────────────────┘      │
│                                                                                 │
│    ┌────────────────────────────────────────────────────────────────────┐      │
│    │                                                                    │      │
│    │  COMMAND EXECUTION                                                 │      │
│    │  ─────────────────                                                 │      │
│    │  Trigger: /command-name (explicit user invocation)                 │      │
│    │  Action:  Command workflow executes                                │      │
│    │           └── May invoke skills (adds to main context)             │      │
│    │           └── May spawn agents (isolated context)                  │      │
│    │  Impact:  Variable based on what command invokes                   │      │
│    │                                                                    │      │
│    └────────────────────────────────────────────────────────────────────┘      │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  LAYER 4: EXECUTION                                  [RUNTIME ENVIRONMENTS]    │
│  ════════════════════════════════════════════════════════════════════════════  │
│                                                                                 │
│    ┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐       │
│    │   MAIN CONTEXT    │   │  AGENT CONTEXT A  │   │  AGENT CONTEXT B  │       │
│    │   (You + Claude)  │   │   (Subprocess)    │   │   (Subprocess)    │       │
│    │                   │   │                   │   │                   │       │
│    │ ┌───────────────┐ │   │ ┌───────────────┐ │   │ ┌───────────────┐ │       │
│    │ │ Memory Layer  │ │   │ │ Inherited Mem │ │   │ │ Inherited Mem │ │       │
│    │ ├───────────────┤ │   │ ├───────────────┤ │   │ ├───────────────┤ │       │
│    │ │ Loaded Skills │ │   │ │ AGENT.md      │ │   │ │ AGENT.md      │ │       │
│    │ ├───────────────┤ │   │ ├───────────────┤ │   │ ├───────────────┤ │       │
│    │ │ MCP Tools     │ │   │ │ Agent's Skills│ │   │ │ Agent's Skills│ │       │
│    │ ├───────────────┤ │   │ ├───────────────┤ │   │ ├───────────────┤ │       │
│    │ │ Conversation  │ │   │ │ Agent's Tools │ │   │ │ Agent's Tools │ │       │
│    │ └───────────────┘ │   │ └───────────────┘ │   │ └───────────────┘ │       │
│    └─────────┬─────────┘   └─────────┬─────────┘   └─────────┬─────────┘       │
│              │                       │                       │                  │
│              └───────────────────────┴───────────────────────┘                  │
│                                      │                                          │
│                                      ▼                                          │
│                          ┌─────────────────────┐                                │
│                          │    MCP SERVERS      │                                │
│                          │    (External)       │                                │
│                          │                     │                                │
│                          │  • Stateless calls  │                                │
│                          │  • Tool providers   │                                │
│                          │  • API bridges      │                                │
│                          │  • Vector DBs       │                                │
│                          └─────────────────────┘                                │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘


╔═══════════════════════════════════════════════════════════════════════════════╗
║                              TOKEN BUDGET SUMMARY                              ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   FIXED COSTS (Every Session):                                                ║
║   ┌─────────────────────────────────────────────────────────┬───────────────┐ ║
║   │  System prompt base                                     │  ~2-3k tokens │ ║
║   │  CLAUDE.md + rules/ (YOUR CONTROL)                      │  ~2-5k tokens │ ║
║   │  Skill/Agent/Command metadata                           │  ~1-2k tokens │ ║
║   │  MCP tool signatures                                    │  ~0.5-1k/srv  │ ║
║   ├─────────────────────────────────────────────────────────┼───────────────┤ ║
║   │  BASELINE OVERHEAD                                      │  ~6-12k tokens│ ║
║   └─────────────────────────────────────────────────────────┴───────────────┘ ║
║                                                                               ║
║   VARIABLE COSTS (On-Demand):                                                 ║
║   ┌─────────────────────────────────────────────────────────┬───────────────┐ ║
║   │  Skill invocation                                       │  +Variable    │ ║
║   │  (loads into MAIN context)                              │  (your cost)  │ ║
║   ├─────────────────────────────────────────────────────────┼───────────────┤ ║
║   │  Agent spawn                                            │  +0 (FREE!)   │ ║
║   │  (isolated subprocess with own budget)                  │  (agent cost) │ ║
║   ├─────────────────────────────────────────────────────────┼───────────────┤ ║
║   │  Conversation history                                   │  +Grows       │ ║
║   │  (until auto-compaction)                                │               │ ║
║   └─────────────────────────────────────────────────────────┴───────────────┘ ║
║                                                                               ║
║   💡 KEY DESIGN INSIGHT:                                                      ║
║   Agent spawns are "FREE" to parent context → Use skill-heavy agents          ║
║   liberally without impacting your main conversation token budget             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
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
├── CLAUDE.md ─────────────────────► PERSISTENT MEMORY: Core identity
│   │                                • Always loaded at session start
│   │                                • @imports to rules/ for modularity
│   │                                • Keep lean: ~500-1000 lines max
│   │
│   └── @rules/[topic].md ─────────► PERSISTENT MEMORY: Modular principles
│                                    • Loaded via @import chain
│                                    • Topic-specific (coding, communication, etc.)
│
├── settings.json ─────────────────► CONFIG (not in context)
│                                    • Model selection, tool permissions
│                                    • Plugin enablement, env variables
│
├── rules/ ────────────────────────► PERSISTENT MEMORY (modular)
│   ├── communication-style.md       • Interaction patterns
│   ├── coding-philosophy.md         • Development principles  
│   ├── analysis-framework.md        • Reasoning approaches
│   └── [domain].md                  • Domain-specific principles
│
├── skills/ ───────────────────────► CAPABILITY REGISTRY → ON-DEMAND CONTENT
│   └── [skill-name]/
│       ├── SKILL.md ──────────────► Entry point (frontmatter = metadata)
│       │                            • Metadata: always loaded (~1-2 lines)
│       │                            • Content: loaded on invocation
│       ├── references/ ───────────► Sub-knowledge (@imported by SKILL.md)
│       ├── scripts/ ──────────────► Executable utilities
│       └── examples/ ─────────────► Usage examples
│
├── agents/ ───────────────────────► CAPABILITY REGISTRY → SUBPROCESS SPAWN
│   └── [agent-name].md ───────────► Agent definition (or [name]/AGENT.md)
│       │                            • Metadata: name, description, model
│       │                            • skills: [] field (loads into AGENT's context)
│       │                            • Spawns with OWN context window
│       │
│       └── 💡 Agent = HOW to behave; Skills = WHAT to know
│
├── commands/ ─────────────────────► CAPABILITY REGISTRY → WORKFLOW EXECUTION
│   └── [command-name].md ─────────► Command definition
│                                    • Invoked via /command-name
│                                    • Can invoke skills, spawn agents
│
├── plugins/ ──────────────────────► EXTERNAL EXTENSIONS
│   ├── cache/ ────────────────────► Installed plugin content
│   └── marketplaces/ ─────────────► Marketplace repository clones
│                                    • Each plugin has own skills/agents/commands
│                                    • Merged into capability registry
│
└── [system-managed]/ ─────────────► AUTO-GENERATED (don't modify)
    ├── projects/                    • Project-specific settings
    ├── todos/                       • Task tracking
    ├── statsig/                     • Feature flags
    └── ...                          • Various internal state
```

---

## Diagram 3: Memory Precedence Hierarchy

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                       MEMORY PRECEDENCE HIERARCHY                              ║
║                   (Higher number = Loaded later, Can override)                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝

    PRECEDENCE │ LOCATION                    │ PURPOSE               │ SCOPE
    ═══════════╪═════════════════════════════╪═══════════════════════╪═══════════
         5     │ ./CLAUDE.local.md           │ Personal overrides    │ Gitignored
               │                             │                       │
         4     │ ~/.claude/CLAUDE.md         │ Your global identity  │ User-wide
               │ └── @~/.claude/rules/       │                       │
               │                             │                       │
         3     │ ./.claude/rules/*.md        │ Project principles    │ Project
               │                             │                       │
         2     │ ./CLAUDE.md                 │ Team-shared project   │ Project
               │                             │ instructions          │
               │                             │                       │
         1     │ /etc/claude-code/CLAUDE.md  │ Enterprise policy     │ Org-wide
               │ (if exists)                 │                       │

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │  LOADING ORDER (all layers merge into context):                         │
    │                                                                         │
    │  Enterprise → Project → Project Rules → User → Local                    │
    │      │            │            │           │        │                   │
    │      └────────────┴────────────┴───────────┴────────┘                   │
    │                              │                                          │
    │                              ▼                                          │
    │                    ┌─────────────────┐                                  │
    │                    │  MERGED MEMORY  │                                  │
    │                    │    CONTEXT      │                                  │
    │                    └─────────────────┘                                  │
    │                                                                         │
    │  💡 Later precedence can OVERRIDE earlier (e.g., local overrides user) │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
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
        │   MEMORY LAYER    │           │  knowledge (HOW TO do    │
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
```

---

## Diagram 5: Skill vs Agent Design Heuristics

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                       SKILL vs AGENT: WHEN TO USE WHICH                        ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────┬─────────────────────────────────────────┐
│         USE A SKILL WHEN...         │          USE AN AGENT WHEN...           │
├─────────────────────────────────────┼─────────────────────────────────────────┤
│                                     │                                         │
│ ✓ SHARED KNOWLEDGE                  │ ✓ UNIQUE WORKFLOW                       │
│   Multiple agents need same domain  │   Does one specific thing with          │
│   knowledge (e.g., pdf skill used   │   specialized instructions              │
│   by document-analyzer AND          │                                         │
│   report-generator agents)          │                                         │
│                                     │                                         │
│ ✓ MODULAR UPDATES                   │ ✓ ISOLATED CONTEXT BENEFICIAL           │
│   Update once, all agents benefit   │   Heavy processing shouldn't impact     │
│                                     │   your main conversation                │
│                                     │                                         │
│ ✓ LARGE REFERENCE MATERIAL          │ ✓ LOADS MULTIPLE SKILLS                 │
│   Has sub-files (references/,       │   Agent with skills: ["a", "b", "c"]    │
│   examples/) that benefit from      │   loads all into ITS context, not yours │
│   skill's folder structure          │                                         │
│                                     │                                         │
│ ✓ DOMAIN EXPERTISE (WHAT TO KNOW)   │ ✓ SPECIALIZED PERSONA (HOW TO BEHAVE)   │
│   Deep procedural knowledge that's  │   Distinct workflow, output format,     │
│   reusable across contexts          │   reasoning approach                    │
│                                     │                                         │
│ ✓ RAPID PROTOTYPING                 │ ✓ TASK MAY NEED RESUMPTION              │
│   Still figuring out what's needed; │   Agents support resumption; skills     │
│   easy to iterate on single file    │   don't                                 │
│                                     │                                         │
├─────────────────────────────────────┼─────────────────────────────────────────┤
│ EXAMPLES:                           │ EXAMPLES:                               │
│ • pdf-processing                    │ • code-reviewer                         │
│ • code-standards                    │ • research-analyst                      │
│ • documentation-templates           │ • project-integrator                    │
│ • prompting-techniques              │ • strategic-advisor                     │
└─────────────────────────────────────┴─────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│   💡 HYBRID PATTERN (RECOMMENDED)                                               │
│   ════════════════════════════════════════════════════════════════════════════ │
│                                                                                 │
│   name: code-reviewer                                                           │
│   description: Reviews code for quality and security                            │
│   model: sonnet                                                                 │
│   skills:                                                                       │
│     - security-guidance    # shared skill (WHAT TO KNOW)                        │
│     - code-standards       # shared skill (WHAT TO KNOW)                        │
│                                                                                 │
│   # Agent's AGENT.md contains:                                                  │
│   # - Review workflow steps (HOW TO BEHAVE)                                     │
│   # - Output format requirements                                                │
│   # - Specific heuristics for THIS agent                                        │
│                                                                                 │
│   Agent = HOW to behave │ Skills = WHAT to know                                 │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagram 6: Two-Schema Architecture (Global vs Plugin)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        TWO-SCHEMA ARCHITECTURE                                 ║
║               Personal (Global) vs Distributable (Plugin)                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────┐     ┌─────────────────────────────────────┐
│                                     │     │                                     │
│  SCHEMA 1: GLOBAL USER CONFIG       │     │  SCHEMA 2: DISTRIBUTABLE PLUGIN     │
│  ═════════════════════════════════  │     │  ═════════════════════════════════  │
│                                     │     │                                     │
│  Location: ~/.claude/               │     │  Location: your-plugin/             │
│  Purpose: Personal baseline         │     │  Purpose: Shareable project config  │
│  Scope: All your projects           │     │  Scope: This project only           │
│                                     │     │                                     │
│  ┌─────────────────────────────┐   │     │  ┌─────────────────────────────┐   │
│  │ CLAUDE.md (your identity)   │   │     │  │ .claude-plugin/plugin.json  │   │
│  │ rules/ (your principles)    │   │     │  │ CLAUDE.md (project memory)  │   │
│  │ skills/ (your capabilities) │   │     │  │ .claude/rules/ (proj rules) │   │
│  │ agents/ (your specialists)  │   │     │  │ skills/ (project skills)    │   │
│  │ commands/ (your shortcuts)  │   │     │  │ agents/ (project agents)    │   │
│  │ settings.json (config)      │   │     │  │ commands/ (project commands)│   │
│  └─────────────────────────────┘   │     │  │ knowledge/ (domain KB)      │   │
│                                     │     │  │ .mcp.json (project MCP)     │   │
│  NOT shareable                      │     │  └─────────────────────────────┘   │
│  (Contains your personal config)    │     │                                     │
│                                     │     │  ✓ Shareable via git/marketplace    │
└─────────────────────────────────────┘     └─────────────────────────────────────┘
                │                                           │
                │                                           │
                └───────────────┬───────────────────────────┘
                                │
                                ▼
                ┌───────────────────────────────────┐
                │                                   │
                │  WHEN WORKING IN A PROJECT:       │
                │                                   │
                │  Global components + Project      │
                │  components = MERGED CONTEXT      │
                │                                   │
                │  (Name conflicts: project wins)   │
                │                                   │
                └───────────────────────────────────┘
```

---

## Diagram 7: Agent Spawn Sequence (Context Isolation)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         AGENT SPAWN SEQUENCE                                   ║
║                  Demonstrating Context Isolation                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

    USER                    MAIN CONTEXT              AGENT SUBPROCESS
      │                          │                          │
      │  "Review this code"      │                          │
      │─────────────────────────►│                          │
      │                          │                          │
      │                    ┌─────┴─────┐                    │
      │                    │  Match →  │                    │
      │                    │  code-    │                    │
      │                    │  reviewer │                    │
      │                    └─────┬─────┘                    │
      │                          │                          │
      │                          │  SPAWN SUBPROCESS        │
      │                          │─────────────────────────►│
      │                          │                          │
      │                          │                    ┌─────┴─────┐
      │                          │                    │ OWN       │
      │                          │                    │ CONTEXT   │
      │                          │                    │ WINDOW    │
      │                          │                    ├───────────┤
      │                          │                    │• Inherited│
      │                          │                    │  memory   │
      │                          │                    │• AGENT.md │
      │                          │                    │• skills:  │
      │                          │                    │  [security│
      │                          │                    │  standards│
      │                          │                    └─────┬─────┘
      │                          │                          │
      │                    ┌─────┴─────┐                    │
      │                    │ PARENT    │                    │
      │                    │ CONTEXT   │              ┌─────┴─────┐
      │                    │ UNCHANGED │              │ Process   │
      │                    │ (0 tokens │◄─────────────│ task...   │
      │                    │  added)   │  (isolated)  └─────┬─────┘
      │                    └─────┬─────┘                    │
      │                          │                          │
      │                          │     RETURN SUMMARY       │
      │                          │◄─────────────────────────│
      │                          │                          │
      │                    ┌─────┴─────┐                    │
      │                    │ Only      │                    │
      │                    │ summary   │                    │
      │                    │ added to  │                    │
      │                    │ context   │                    │
      │                    └─────┬─────┘                    │
      │                          │                          │
      │◄─────────────────────────│                          │
      │   Response                                          │

    💡 KEY INSIGHT: Agent's skills: ["security", "standards"] 
       loads into AGENT's context, NOT yours!
       
       This means you can create skill-heavy agents 
       without impacting your main conversation budget.
```

---

## Summary: Key Architecture Principles

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      KEY ARCHITECTURE PRINCIPLES                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

1. PROGRESSIVE DISCLOSURE
   Memory (always) → Registry (metadata) → Invocation (on-demand) → Execution (isolated)
        │                  │                      │                        │
     ~2-5k tokens      ~1-2k tokens          Variable              Own context

2. LAZY LOADING
   • Skill METADATA loads at session start (~1-2 lines per skill)
   • Skill CONTENT loads only on invocation
   • Trust the lazy-loading—system is designed for this

3. CONTEXT ISOLATION
   • Agent spawns are SUBPROCESSES with OWN context windows
   • Agent's skills load into AGENT's context, not yours
   • Parent context UNCHANGED (zero token cost)

4. MEMORY UNIFICATION
   • CLAUDE.md + rules/ = unified "Memory Layer"
   • Both are persistent identity/principles at different granularity
   • Keep combined <5k tokens for headroom

5. HYBRID COMPONENT DESIGN
   • Agent = HOW to behave (workflow, persona, reasoning)
   • Skills = WHAT to know (domain knowledge, procedures)
   • Commands = explicit shortcuts (/command-name)

6. TWO-SCHEMA SEPARATION
   • Schema 1 (Global): Personal baseline, travels with you
   • Schema 2 (Plugin): Distributable, shareable via marketplace

╚═══════════════════════════════════════════════════════════════════════════════╝
```

