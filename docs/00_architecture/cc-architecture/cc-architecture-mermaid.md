# Claude Code Architecture — Mermaid Diagrams

## Diagram 1: Runtime Layer Flow

```mermaid
flowchart TB
    subgraph L1["LAYER 1: PERSISTENT MEMORY (Always Loaded)"]
        CLAUDE[CLAUDE.md<br/>Core Identity]
        RULES[rules/*.md<br/>Modular Principles]
        CLAUDE -->|@import| RULES
    end

    subgraph L2["LAYER 2: CAPABILITY REGISTRY (Metadata Only)"]
        SKILLS_META[Skills<br/>name + description]
        AGENTS_META[Agents<br/>name + description]
        COMMANDS_META[Commands<br/>name + description]
        MCP_SIG[MCP Tools<br/>signatures]
    end

    subgraph L3["LAYER 3: INVOCATION (On-Demand)"]
        SKILL_INVOKE["/skill or auto-match<br/>→ Content loads to MAIN"]
        AGENT_SPAWN["Task match<br/>→ Agent SPAWNS"]
        CMD_EXEC["/command<br/>→ Workflow runs"]
    end

    subgraph L4["LAYER 4: EXECUTION (Runtime)"]
        MAIN[MAIN CONTEXT<br/>You + Claude]
        AGENT_A[AGENT CONTEXT A<br/>Subprocess]
        AGENT_B[AGENT CONTEXT B<br/>Subprocess]
        MCP_SERVER[MCP SERVERS<br/>External Tools]
    end

    L1 --> L2
    SKILLS_META --> SKILL_INVOKE
    AGENTS_META --> AGENT_SPAWN
    COMMANDS_META --> CMD_EXEC
    
    SKILL_INVOKE -->|"Adds to YOUR context"| MAIN
    AGENT_SPAWN -->|"Isolated (zero cost to parent)"| AGENT_A
    AGENT_SPAWN -->|"Isolated (zero cost to parent)"| AGENT_B
    CMD_EXEC --> MAIN
    
    MAIN --> MCP_SERVER
    AGENT_A --> MCP_SERVER
    AGENT_B --> MCP_SERVER

    style L1 fill:#e1f5fe
    style L2 fill:#fff3e0
    style L3 fill:#f3e5f5
    style L4 fill:#e8f5e9
```

## Diagram 2: Content Placement Decision Tree

```mermaid
flowchart TD
    START[New Content to Organize] --> Q1{Is it WHO you are<br/>or HOW you ALWAYS behave?}
    
    Q1 -->|YES| MEMORY[MEMORY LAYER<br/>CLAUDE.md + rules/]
    Q1 -->|NO| Q2{Is it procedural<br/>HOW TO knowledge?}
    
    Q2 -->|YES| SKILL[SKILL<br/>Lazy-loaded, reusable]
    Q2 -->|NO| Q3{Needs separate context<br/>or sustained work?}
    
    Q3 -->|YES| AGENT[AGENT<br/>Own context, subprocess]
    Q3 -->|NO| REF[REFERENCE ONLY<br/>Knowledge base]
    
    MEMORY -->|"Token: ALWAYS loaded"| M_NOTE["~2-5k tokens<br/>Keep lean!"]
    SKILL -->|"Token: On invocation"| S_NOTE["Adds to MAIN context"]
    AGENT -->|"Token: Isolated"| A_NOTE["FREE to parent context"]
    
    style MEMORY fill:#e3f2fd
    style SKILL fill:#fff8e1
    style AGENT fill:#fce4ec
    style REF fill:#f5f5f5
```

## Diagram 3: Skill vs Agent Decision

```mermaid
flowchart LR
    subgraph SKILL_USE["USE SKILL WHEN..."]
        S1[Reusable across contexts]
        S2[Auto-invoke desired]
        S3[Load into MAIN context OK]
        S4[Procedural 'how to']
        S5[Update once, benefit everywhere]
    end
    
    subgraph AGENT_USE["USE AGENT WHEN..."]
        A1[Sustained focus needed]
        A2[Isolated context beneficial]
        A3[Load multiple skills]
        A4[Specialized persona]
        A5[May need resumption]
    end
    
    SKILL_USE --> EXAMPLES_S[Examples:<br/>pdf-processing<br/>code-standards<br/>documentation-templates]
    AGENT_USE --> EXAMPLES_A[Examples:<br/>code-reviewer<br/>research-analyst<br/>project-integrator]
    
    style SKILL_USE fill:#fff8e1
    style AGENT_USE fill:#fce4ec
```

## Diagram 4: Global Config Structure

```mermaid
flowchart TB
    subgraph GLOBAL["~/.claude/ (Global User Config)"]
        CLAUDE_MD["CLAUDE.md<br/>Core Identity"]
        SETTINGS["settings.json<br/>Config (not in context)"]
        
        subgraph MEMORY_DIR["Memory Layer"]
            RULES_DIR["rules/<br/>Modular principles"]
        end
        
        subgraph REGISTRY["Capability Registry"]
            SKILLS_DIR["skills/<br/>Procedural knowledge"]
            AGENTS_DIR["agents/<br/>Specialists"]
            COMMANDS_DIR["commands/<br/>Workflows"]
        end
        
        subgraph EXTERNAL["External"]
            PLUGINS_DIR["plugins/<br/>Marketplace installs"]
            MCP_DIR["MCP configs"]
        end
        
        SYSTEM["[system folders]<br/>Auto-managed"]
    end
    
    CLAUDE_MD -->|"@import"| RULES_DIR
    SKILLS_DIR -->|"skills: []"| AGENTS_DIR
    
    style MEMORY_DIR fill:#e3f2fd
    style REGISTRY fill:#fff8e1
    style EXTERNAL fill:#f5f5f5
```

## Diagram 5: Token Budget Overview

```mermaid
pie showData
    title "Baseline Context Budget (~6-12k tokens)"
    "System Prompt Base" : 3
    "CLAUDE.md + rules/" : 4
    "Skill/Agent/Command Metadata" : 2
    "MCP Tool Signatures" : 1
```

## Diagram 6: Two-Schema Architecture Overview

```mermaid
flowchart TB
    subgraph SCHEMA1["SCHEMA 1: Global User Config"]
        direction TB
        G_CLAUDE["~/.claude/CLAUDE.md<br/>Personal baseline"]
        G_RULES["~/.claude/rules/<br/>Personal principles"]
        G_SKILLS["~/.claude/skills/<br/>Cross-project skills"]
        G_AGENTS["~/.claude/agents/<br/>Personal agents"]
    end
    
    subgraph SCHEMA2["SCHEMA 2: Distributable Plugin"]
        direction TB
        P_PLUGIN[".claude-plugin/plugin.json<br/>Marketplace metadata"]
        P_CLAUDE["./CLAUDE.md<br/>Project instructions"]
        P_RULES["./.claude/rules/<br/>Project rules"]
        P_SKILLS["./skills/<br/>Project skills"]
        P_AGENTS["./agents/<br/>Project agents"]
        P_KNOWLEDGE["./knowledge/<br/>Domain KB"]
    end
    
    SCHEMA1 -->|"inherits/supplements"| SCHEMA2
    SCHEMA2 -->|"distributes via"| MARKETPLACE["Marketplace<br/>or Git"]
    
    style SCHEMA1 fill:#e8f5e9
    style SCHEMA2 fill:#e3f2fd
```

## Diagram 7: Agent Spawn Isolation

```mermaid
sequenceDiagram
    participant User
    participant Main as Main Context
    participant Agent as Agent Subprocess
    participant MCP as MCP Server

    User->>Main: "Review this code"
    Main->>Main: Match → code-reviewer agent
    Main->>Agent: Spawn subprocess
    Note over Agent: Own context window
    Note over Agent: Loads AGENT.md
    Note over Agent: Loads skills: [security, standards]
    Note over Main: Context UNCHANGED
    Agent->>MCP: Tool calls
    MCP-->>Agent: Results
    Agent-->>Main: Return summary
    Note over Main: Only summary added
```

