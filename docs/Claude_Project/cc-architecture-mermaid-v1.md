# Claude Code Architecture — Mermaid Diagrams v1.0

For rendering in tools that support Mermaid (GitHub, Notion, VS Code, etc.)

---

## Diagram 1: Runtime Layer Flow

```mermaid
flowchart TB
    subgraph L1["🧠 LAYER 1: PERSISTENT MEMORY<br/>(Always Loaded ~2-5k tokens)"]
        CLAUDE["CLAUDE.md<br/>Core Identity"]
        RULES["rules/*.md<br/>Modular Principles"]
        CLAUDE -->|"@import"| RULES
    end

    subgraph L2["📋 LAYER 2: CAPABILITY REGISTRY<br/>(Metadata Only ~1-2k tokens)"]
        SKILLS_META["Skills<br/>name + desc"]
        AGENTS_META["Agents<br/>name + desc"]
        COMMANDS_META["Commands<br/>name + desc"]
        MCP_SIG["MCP Tools<br/>signatures"]
    end

    subgraph L3["⚡ LAYER 3: INVOCATION<br/>(On-Demand)"]
        SKILL_INVOKE["/skill or auto-match<br/>→ Content loads to MAIN"]
        AGENT_SPAWN["Task match<br/>→ Agent SPAWNS"]
        CMD_EXEC["/command<br/>→ Workflow runs"]
    end

    subgraph L4["🔄 LAYER 4: EXECUTION<br/>(Runtime Environments)"]
        MAIN["MAIN CONTEXT<br/>You + Claude"]
        AGENT_A["AGENT CONTEXT A<br/>Subprocess"]
        AGENT_B["AGENT CONTEXT B<br/>Subprocess"]
        MCP_SERVER["MCP SERVERS<br/>External Tools"]
    end

    L1 --> L2
    SKILLS_META --> SKILL_INVOKE
    AGENTS_META --> AGENT_SPAWN
    COMMANDS_META --> CMD_EXEC
    
    SKILL_INVOKE -->|"Adds to YOUR context"| MAIN
    AGENT_SPAWN -->|"ZERO cost to parent"| AGENT_A
    AGENT_SPAWN -->|"ZERO cost to parent"| AGENT_B
    CMD_EXEC --> MAIN
    
    MAIN --> MCP_SERVER
    AGENT_A --> MCP_SERVER
    AGENT_B --> MCP_SERVER

    style L1 fill:#e1f5fe,stroke:#01579b
    style L2 fill:#fff3e0,stroke:#e65100
    style L3 fill:#f3e5f5,stroke:#7b1fa2
    style L4 fill:#e8f5e9,stroke:#2e7d32
```

---

## Diagram 2: Content Placement Decision Tree

```mermaid
flowchart TD
    START["🆕 New Content to Organize"] --> Q1{"Is it WHO you are<br/>or HOW you ALWAYS behave?"}
    
    Q1 -->|"✅ YES"| MEMORY["🧠 MEMORY LAYER<br/>CLAUDE.md + rules/"]
    Q1 -->|"❌ NO"| Q2{"Is it procedural<br/>HOW TO knowledge?"}
    
    Q2 -->|"✅ YES"| SKILL["📚 SKILL<br/>Lazy-loaded, reusable"]
    Q2 -->|"❌ NO"| Q3{"Needs separate context<br/>or sustained work?"}
    
    Q3 -->|"✅ YES"| AGENT["🤖 AGENT<br/>Own context, subprocess"]
    Q3 -->|"❌ NO"| REF["📄 REFERENCE ONLY<br/>Knowledge base"]
    
    MEMORY --> M_NOTE["Token: ALWAYS loaded<br/>~2-5k (keep lean!)"]
    SKILL --> S_NOTE["Token: On invocation<br/>Adds to MAIN context"]
    AGENT --> A_NOTE["Token: ISOLATED<br/>FREE to parent!"]
    
    style MEMORY fill:#e3f2fd,stroke:#1565c0
    style SKILL fill:#fff8e1,stroke:#f9a825
    style AGENT fill:#fce4ec,stroke:#c2185b
    style REF fill:#f5f5f5,stroke:#616161
```

---

## Diagram 3: Memory Precedence Hierarchy

```mermaid
flowchart BT
    subgraph MERGED["📦 MERGED MEMORY CONTEXT"]
        FINAL["Final Context<br/>(All layers combined)"]
    end
    
    L1["1️⃣ Enterprise Policy<br/>/etc/claude-code/CLAUDE.md<br/>(if exists)"]
    L2["2️⃣ Project Memory<br/>./CLAUDE.md<br/>(team-shared)"]
    L3["3️⃣ Project Rules<br/>./.claude/rules/*.md"]
    L4["4️⃣ User Memory<br/>~/.claude/CLAUDE.md<br/>(your identity)"]
    L5["5️⃣ Project Local<br/>./CLAUDE.local.md<br/>(gitignored)"]
    
    L1 --> FINAL
    L2 --> FINAL
    L3 --> FINAL
    L4 --> FINAL
    L5 --> FINAL
    
    style L5 fill:#c8e6c9,stroke:#2e7d32
    style L4 fill:#bbdefb,stroke:#1565c0
    style L3 fill:#fff9c4,stroke:#f9a825
    style L2 fill:#ffe0b2,stroke:#ef6c00
    style L1 fill:#ffcdd2,stroke:#c62828
    style FINAL fill:#e1bee7,stroke:#7b1fa2
```

---

## Diagram 4: Skill vs Agent Comparison

```mermaid
flowchart LR
    subgraph SKILL_BOX["📚 USE SKILL WHEN..."]
        direction TB
        S1["Shared across agents"]
        S2["Update once, benefit all"]
        S3["Large references/scripts"]
        S4["Domain expertise<br/>(WHAT TO KNOW)"]
    end
    
    subgraph AGENT_BOX["🤖 USE AGENT WHEN..."]
        direction TB
        A1["Unique workflow"]
        A2["Isolated context helpful"]
        A3["Loads multiple skills"]
        A4["Specialized persona<br/>(HOW TO BEHAVE)"]
    end
    
    SKILL_BOX --> EXAMPLES_S["Examples:<br/>• pdf-processing<br/>• code-standards<br/>• prompting-techniques"]
    AGENT_BOX --> EXAMPLES_A["Examples:<br/>• code-reviewer<br/>• research-analyst<br/>• project-integrator"]
    
    style SKILL_BOX fill:#fff8e1,stroke:#f9a825
    style AGENT_BOX fill:#fce4ec,stroke:#c2185b
```

---

## Diagram 5: Two-Schema Architecture

```mermaid
flowchart TB
    subgraph SCHEMA1["🏠 SCHEMA 1: Global User Config"]
        direction TB
        G_LOC["📍 ~/.claude/"]
        G_CLAUDE["CLAUDE.md"]
        G_RULES["rules/"]
        G_SKILLS["skills/"]
        G_AGENTS["agents/"]
        G_NOTE["❌ Not shareable<br/>(personal config)"]
    end
    
    subgraph SCHEMA2["📦 SCHEMA 2: Distributable Plugin"]
        direction TB
        P_LOC["📍 your-plugin/"]
        P_PLUGIN[".claude-plugin/plugin.json"]
        P_CLAUDE["CLAUDE.md"]
        P_SKILLS["skills/"]
        P_AGENTS["agents/"]
        P_KNOWLEDGE["knowledge/"]
        P_NOTE["✅ Shareable via<br/>git/marketplace"]
    end
    
    SCHEMA1 -->|"inherits"| MERGED["🔀 Merged Context<br/>when working in project"]
    SCHEMA2 -->|"supplements"| MERGED
    
    style SCHEMA1 fill:#e8f5e9,stroke:#2e7d32
    style SCHEMA2 fill:#e3f2fd,stroke:#1565c0
    style MERGED fill:#f3e5f5,stroke:#7b1fa2
```

---

## Diagram 6: Agent Spawn Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant M as Main Context
    participant A as Agent Subprocess

    U->>M: "Review this code"
    M->>M: Match → code-reviewer agent
    
    Note over M: Parent context UNCHANGED
    
    M->>A: Spawn subprocess
    
    Note over A: OWN context window
    Note over A: Loads AGENT.md
    Note over A: Loads skills: [security, standards]
    Note over A: into AGENT's context (not parent!)
    
    A->>A: Process task...
    A-->>M: Return summary only
    
    Note over M: Only summary added<br/>(minimal tokens)
    
    M-->>U: Response
```

---

## Diagram 7: Token Budget Breakdown

```mermaid
pie showData
    title "Baseline Context Budget (~6-12k tokens)"
    "System Prompt Base (~2-3k)" : 25
    "CLAUDE.md + rules/ (~2-5k)" : 35
    "Skill/Agent/Command Metadata (~1-2k)" : 20
    "MCP Tool Signatures (~0.5-1k)" : 10
    "Headroom for conversation" : 10
```

---

## Diagram 8: Global Config Directory Map

```mermaid
flowchart LR
    subgraph GLOBAL["~/.claude/"]
        direction TB
        
        subgraph MEM["🧠 Memory Layer"]
            CM["CLAUDE.md"]
            RU["rules/"]
        end
        
        subgraph REG["📋 Capability Registry"]
            SK["skills/"]
            AG["agents/"]
            CO["commands/"]
        end
        
        subgraph EXT["🔌 External"]
            PL["plugins/"]
            MC["mcp configs"]
        end
        
        SET["settings.json"]
        SYS["[system folders]"]
    end
    
    CM -->|"@import"| RU
    SK -->|"skills: []"| AG
    
    style MEM fill:#e3f2fd
    style REG fill:#fff8e1
    style EXT fill:#f5f5f5
```

