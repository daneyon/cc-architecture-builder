# Claude Code Architecture - Visual Diagrams

**Version**: 1.0 (2026-01-28)  
**Syntax**: Validated for Mermaid 10.x+

---

## Diagram 1: CC Runtime Layer Architecture

```mermaid
flowchart TB
    subgraph L1["LAYER 1: PERSISTENT MEMORY"]
        CLAUDE["CLAUDE.md<br/>Core Identity"]
        RULES["rules/*.md<br/>Modular Principles"]
        CLAUDE -->|"@import"| RULES
    end

    subgraph L2["LAYER 2: CAPABILITY REGISTRY"]
        SKILLS_META["Skills<br/>name + description"]
        AGENTS_META["Agents<br/>name + description"]
        COMMANDS_META["Commands<br/>name + description"]
        MCP_SIG["MCP Tools<br/>signatures"]
    end

    subgraph L3["LAYER 3: INVOCATION"]
        SKILL_INVOKE["/skill or auto-match<br/>Content loads to MAIN"]
        AGENT_SPAWN["Task match<br/>Agent SPAWNS"]
        CMD_EXEC["/command<br/>Workflow runs"]
    end

    subgraph L4["LAYER 4: EXECUTION"]
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
    AGENT_SPAWN -->|"Isolated"| AGENT_A
    AGENT_SPAWN -->|"Isolated"| AGENT_B
    CMD_EXEC --> MAIN
    
    MAIN --> MCP_SERVER
    AGENT_A --> MCP_SERVER
    AGENT_B --> MCP_SERVER

    style L1 fill:#e1f5fe
    style L2 fill:#fff3e0
    style L3 fill:#f3e5f5
    style L4 fill:#e8f5e9
```

---

## Diagram 2: Content Placement Decision Tree

```mermaid
flowchart TD
    START["New Content to Organize"] --> Q1{"Is it WHO you are<br/>or HOW you ALWAYS behave?"}
    
    Q1 -->|YES| MEMORY["MEMORY LAYER<br/>CLAUDE.md + rules/"]
    Q1 -->|NO| Q2{"Is it procedural<br/>HOW TO knowledge?"}
    
    Q2 -->|YES| SKILL["SKILL<br/>Lazy-loaded, reusable"]
    Q2 -->|NO| Q3{"Needs separate context<br/>or sustained work?"}
    
    Q3 -->|YES| AGENT["AGENT<br/>Own context, subprocess"]
    Q3 -->|NO| Q4{"Repeatable workflow<br/>or shortcut?"}
    
    Q4 -->|YES| COMMAND["COMMAND<br/>User or model invoked"]
    Q4 -->|NO| REF["REFERENCE ONLY<br/>Knowledge base"]
    
    style MEMORY fill:#e3f2fd
    style SKILL fill:#fff8e1
    style AGENT fill:#fce4ec
    style COMMAND fill:#e8f5e9
    style REF fill:#f5f5f5
```

---

## Diagram 3: Skill vs Agent Decision

```mermaid
flowchart LR
    subgraph SKILL_USE["USE SKILL WHEN"]
        S1["Reusable across contexts"]
        S2["Auto-invoke desired"]
        S3["Load into MAIN context OK"]
        S4["Procedural how-to"]
        S5["Update once benefit everywhere"]
    end
    
    subgraph AGENT_USE["USE AGENT WHEN"]
        A1["Sustained focus needed"]
        A2["Isolated context beneficial"]
        A3["Load multiple skills"]
        A4["Specialized persona"]
        A5["May need resumption"]
    end
    
    SKILL_USE --> EXAMPLES_S["Examples:<br/>pdf-processing<br/>code-standards<br/>documentation-templates"]
    AGENT_USE --> EXAMPLES_A["Examples:<br/>code-reviewer<br/>research-analyst<br/>project-integrator"]
    
    style SKILL_USE fill:#fff8e1
    style AGENT_USE fill:#fce4ec
```

---

## Diagram 4: Claude Web vs Claude Code Platform Relationship

```mermaid
flowchart TB
    subgraph CW["CLAUDE WEB"]
        CW_PROJ["Project Knowledge<br/>Single files, folders"]
        CW_INST["Custom Instructions<br/>System prompt text"]
        CW_CONV["Conversation Memory<br/>Built-in persistence"]
        CW_RAG["Built-in RAG<br/>Semantic search"]
    end
    
    subgraph CC["CLAUDE CODE"]
        CC_MEM["Memory Layer<br/>CLAUDE.md + rules/"]
        CC_SKILLS["Skills<br/>Modular procedural knowledge"]
        CC_AGENTS["Agents<br/>Subprocess specialists"]
        CC_CMDS["Commands<br/>Workflow shortcuts"]
        CC_MCP["MCP Servers<br/>External tool integration"]
    end
    
    CW_PROJ -->|"Modularizes into"| CC_MEM
    CW_PROJ -->|"Becomes"| CC_SKILLS
    CW_INST -->|"Evolves into"| CC_MEM
    CW_INST -->|"Specializes as"| CC_AGENTS
    
    CC -->|"Plugin Distribution"| MARKETPLACE["Marketplace"]
    CW -->|"Not distributable"| PERSONAL["Personal Only"]
    
    style CW fill:#e3f2fd
    style CC fill:#e8f5e9
    style MARKETPLACE fill:#fff8e1
    style PERSONAL fill:#ffebee
```

---

## Diagram 5: Custom LLM Evolution Stages

```mermaid
flowchart LR
    subgraph STAGE1["STAGE 1: Claude Web"]
        W1["Single instruction file"]
        W2["Project knowledge folder"]
        W3["Conversation history"]
    end
    
    subgraph STAGE2["STAGE 2: Modularization"]
        M1["Extract identity"]
        M2["Extract principles"]
        M3["Extract procedures"]
        M4["Extract personas"]
        M5["Extract workflows"]
    end
    
    subgraph STAGE3["STAGE 3: Claude Code"]
        C1["Memory Layer"]
        C2["Capability Registry"]
        C3["MCP Integration"]
    end
    
    subgraph STAGE4["STAGE 4: Distribution"]
        D1["Marketplace publish"]
        D2["Git repository"]
        D3["Team sharing"]
    end
    
    STAGE1 --> STAGE2
    STAGE2 --> STAGE3
    STAGE3 --> STAGE4
    
    style STAGE1 fill:#e3f2fd
    style STAGE2 fill:#fff8e1
    style STAGE3 fill:#e8f5e9
    style STAGE4 fill:#f3e5f5
```

---

## Diagram 6: Two-Schema Architecture

```mermaid
flowchart TB
    subgraph SCHEMA1["SCHEMA 1: Global User Config"]
        G_CLAUDE["CLAUDE.md<br/>Personal baseline"]
        G_RULES["rules/<br/>Personal principles"]
        G_SKILLS["skills/<br/>Cross-project skills"]
        G_AGENTS["agents/<br/>Personal agents"]
    end
    
    subgraph SCHEMA2["SCHEMA 2: Distributable Plugin"]
        P_PLUGIN[".claude-plugin/<br/>Marketplace metadata"]
        P_CLAUDE["CLAUDE.md<br/>Project instructions"]
        P_SKILLS["skills/<br/>Project skills"]
        P_AGENTS["agents/<br/>Project agents"]
        P_KNOWLEDGE["knowledge/<br/>Domain KB"]
    end
    
    SCHEMA1 -->|"inherits and supplements"| SCHEMA2
    SCHEMA2 -->|"distributes via"| MARKETPLACE["Marketplace or Git"]
    SCHEMA1 -->|"travels with you"| EVERYWHERE["All Projects"]
    
    style SCHEMA1 fill:#e8f5e9
    style SCHEMA2 fill:#e3f2fd
    style MARKETPLACE fill:#fff8e1
```

---

## Diagram 7: Agent Spawn Isolation

```mermaid
sequenceDiagram
    participant User
    participant Main as Main Context
    participant Agent as Agent Subprocess
    participant MCP as MCP Server

    User->>Main: Review this code
    Main->>Main: Match code-reviewer agent
    Main->>Agent: Spawn subprocess
    Note over Agent: Own context window
    Note over Agent: Loads AGENT.md
    Note over Agent: Loads skills
    Note over Main: Context UNCHANGED
    Agent->>MCP: Tool calls
    MCP-->>Agent: Results
    Agent-->>Main: Return summary
    Note over Main: Only summary added
```

---

## Diagram 8: Token Budget Overview

```mermaid
pie showData
    title Baseline Context Budget 6-12k tokens
    "System Prompt Base" : 3
    "CLAUDE.md + rules" : 4
    "Component Metadata" : 2
    "MCP Signatures" : 1
```

---

## Usage Notes

**VS Code**: Install "Mermaid Preview" or "Markdown Preview Mermaid Support" extension

**GitHub**: Renders natively in markdown files

**Obsidian**: Enable Mermaid in settings

**Export**: Use mermaid.live for PNG/SVG export
