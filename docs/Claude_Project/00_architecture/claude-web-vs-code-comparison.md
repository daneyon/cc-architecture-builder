# Claude Web vs Claude Code: Comprehensive Platform Comparison

**Purpose**: Actionable reference for optimizing custom LLM workflows across both platforms  
**Version**: 1.0 (2026-01-28)

---

## Platform Identity and Naming

| Aspect | Claude Web | Claude Code |
|--------|------------|-------------|
| **Official Name** | Claude (claude.ai) | Claude Code |
| **Access Points** | claude.ai, Claude Desktop App, Claude iOS/Android | CLI (`claude`), IDE extensions |
| **Also Known As** | "Standard Claude", "Claude Projects", "Claude Web" | "CC", "Claude Code CLI", "CC CLI" |
| **Primary Interface** | Web/App GUI with chat | Terminal/IDE with chat |
| **Target User** | General users, researchers, writers, analysts | Developers, engineers, automation builders |

---

## Core Architecture Comparison

### Custom LLM Configuration

| Capability | Claude Web | Claude Code |
|------------|------------|-------------|
| **Identity/Instructions** | Project Instructions (single text field) | CLAUDE.md + rules/ (modular files) |
| **Knowledge Base** | Project Knowledge (file uploads) | knowledge/ folder + skills/ |
| **Persistence** | Per-project, cloud-stored | File-based, local + git |
| **Modularization** | None (monolithic) | Full (rules, skills, agents, commands) |
| **Distribution** | Not shareable | Marketplace, git, plugins |
| **Version Control** | Manual (re-upload files) | Native git integration |

### Memory and Context

| Aspect | Claude Web | Claude Code |
|--------|------------|-------------|
| **Session Memory** | Conversation history (persistent) | Conversation + CLAUDE.md (session-scoped) |
| **Cross-Session Memory** | Built-in memory feature | /memory command, memory.md |
| **Project Knowledge RAG** | Built-in semantic search (hidden) | Manual (@imports) or MCP-based |
| **Context Window** | Managed automatically | Explicit (lazy-loading, token awareness) |
| **Memory Hierarchy** | Flat (instructions + knowledge) | 5-tier (Enterprise → Project → Rules → User → Local) |

---

## Feature-by-Feature Comparison

### Tools and Capabilities

| Feature | Claude Web | Claude Code |
|---------|------------|-------------|
| **Web Search** | Built-in toggle | Via MCP (e.g., Brave Search) |
| **File Creation** | Artifacts (in-chat) | Direct filesystem access |
| **Code Execution** | Analysis tool (sandboxed) | Full bash/terminal access |
| **Image Generation** | Not available | Via MCP (e.g., DALL-E) |
| **API Integration** | Limited | Full MCP ecosystem |
| **Automation** | None | Hooks (event-driven) |
| **Subagents** | None | Built-in (Plan, Explore, General) + custom |

### RAG and Knowledge Retrieval

| Aspect | Claude Web | Claude Code |
|--------|------------|-------------|
| **Retrieval Method** | Semantic search (built-in, opaque) | Manual @imports or MCP vector DB |
| **User Control** | None (automatic) | Full (explicit file references) |
| **Scalability** | Works well up to ~100 files | Requires MCP for 100+ files |
| **Customization** | Not configurable | Fully customizable |
| **Token Efficiency** | Hidden (managed by system) | Explicit (user manages budget) |

**Key Insight**: Claude Web's built-in RAG is convenient but opaque. Claude Code requires explicit knowledge management but offers full control over what gets loaded and when.

---

## Practical Scenario Comparisons

### Scenario 1: Code Review

| Step | Claude Web | Claude Code |
|------|------------|-------------|
| Setup | Upload code files to project knowledge | Files already in workspace |
| Invoke | Paste code or reference uploaded file | "Review this code" or `/code-review` |
| Execution | Single Claude response | Agent subprocess with specialized skills |
| Output | In-chat response | In-chat + potential file edits |
| Iteration | Copy-paste changes manually | Direct file modifications |
| **Friction Points** | Manual file re-upload after changes | None |

**Verdict**: Claude Code wins for iterative development workflows.

---

### Scenario 2: Research and Analysis

| Step | Claude Web | Claude Code |
|------|------------|-------------|
| Setup | Upload research docs to project | Place docs in knowledge/ folder |
| Search | "Search my documents for X" | @import or skill invocation |
| RAG Behavior | Automatic semantic retrieval | Manual file specification |
| Web Search | Toggle on, integrated | MCP tool call |
| Output | In-chat with citations | In-chat or file output |
| History | Preserved across sessions | Lost on session end (unless logged) |
| **Friction Points** | Limited control over retrieval | Extra setup for semantic search |

**Verdict**: Claude Web wins for ad-hoc research; Claude Code wins for repeatable research workflows.

---

### Scenario 3: Document Creation

| Step | Claude Web | Claude Code |
|------|------------|-------------|
| Request | "Write a report on X" | "Write a report on X" |
| Output | Artifact (in-chat panel) | File in filesystem |
| Editing | Edit artifact, re-render | Direct file edit |
| Export | Download button | Already a file |
| Templates | Must describe each time | Skills with templates |
| **Friction Points** | Artifact to download to save workflow | None |

**Verdict**: Claude Code wins for repeated document workflows; Claude Web adequate for one-off.

---

### Scenario 4: Strategic Planning and Brainstorming

| Step | Claude Web | Claude Code |
|------|------------|-------------|
| Context | Conversation history + project knowledge | CLAUDE.md + current session only |
| Multi-session | Reference past conversations naturally | Must use /memory or SESSION_LOG |
| Ideation | Good (conversational flow) | Good (but more technical feel) |
| Decision Tracking | In conversation history | Must manually log |
| Collaboration | Share project link (limited) | Git-based sharing |
| **Friction Points** | Not distributable | Context resets between sessions |

**Verdict**: Claude Web wins for strategic planning due to conversation persistence.

---

### Scenario 5: Building Custom LLM Assistants

| Step | Claude Web | Claude Code |
|------|------------|-------------|
| Define Identity | Project instructions field | CLAUDE.md |
| Add Knowledge | Upload files | Structure in knowledge/, skills/ |
| Add Capabilities | Describe in instructions | Create skills, agents, commands |
| Test | Chat in project | Chat in CLI, run commands |
| Iterate | Edit instructions, re-upload files | Edit files directly |
| Share | Cannot share | Marketplace, git clone |
| **Friction Points** | No modular structure, no sharing | More complex initial setup |

**Verdict**: Claude Code wins decisively for serious custom LLM development.

---

### Scenario 6: Automation and Workflows

| Capability | Claude Web | Claude Code |
|------------|------------|-------------|
| Scheduled Tasks | Not possible | Hooks + external schedulers |
| Event-Driven | Not possible | Hooks (pre/post commit, etc.) |
| CI/CD Integration | Not possible | Native (GitHub Actions, etc.) |
| Batch Processing | Manual | Scripted |
| **Friction Points** | Automation not supported | Requires setup |

**Verdict**: Claude Code is the only option for automation.

---

## Token and Context Management

### Claude Web (Opaque)

```
System manages everything automatically:
- Project instructions injected
- Relevant project knowledge retrieved (semantic search)
- Conversation history included
- User has NO visibility into token usage

Pros: Simple, "just works"
Cons: No control, can't optimize, can't debug retrieval failures
```

### Claude Code (Explicit)

```
User manages with full visibility:

FIXED COSTS (~6-12k tokens):
- System prompt base: ~2-3k
- CLAUDE.md + rules/: ~2-5k (YOUR CONTROL)
- Component metadata: ~1-2k
- MCP signatures: ~0.5-1k per server

VARIABLE COSTS:
- Skill invocation: Adds to MAIN context
- Agent spawn: ISOLATED (zero cost to parent)
- Conversation: Grows until compaction

Pros: Full control, can optimize, can debug
Cons: Requires understanding, manual management
```

---

## Improvement Opportunities

### Claude Web Could Learn From Claude Code

| Gap | Current State | Potential Improvement |
|-----|---------------|----------------------|
| **Modularization** | Monolithic instructions | Support rules/ equivalent |
| **Distribution** | Projects not shareable | Project templates marketplace |
| **Token Visibility** | Completely hidden | Show token usage dashboard |
| **RAG Control** | Opaque semantic search | Allow retrieval tuning |
| **Custom Tools** | Fixed tool set | User-defined tools |
| **Automation** | None | Scheduled project actions |

### Claude Code Could Learn From Claude Web

| Gap | Current State | Potential Improvement |
|-----|---------------|----------------------|
| **Conversation Persistence** | Session-scoped only | Cross-session conversation history |
| **Built-in RAG** | Manual @imports | Semantic search over knowledge/ |
| **Ease of Setup** | Requires file structure | Quick-start wizard |
| **Visual Interface** | Terminal only | GUI dashboard option |
| **Memory UX** | /memory command | Automatic relevant memory surfacing |

---

## Decision Framework: When to Use Which

### Use Claude Web When

- Brainstorming or strategic planning (conversation persistence matters)
- Research requiring semantic search over uploaded documents
- One-off document creation
- Non-technical users need access
- You don't need to share or version control the configuration
- Ad-hoc analysis without automation needs

### Use Claude Code When

- Building distributable custom LLM solutions
- Need modular, maintainable architecture
- Iterative development workflows
- Automation or event-driven actions required
- Team collaboration via git
- Token efficiency is important
- Need full control over context management
- Building reusable skills or agents

### Use Hybrid Approach When

- Strategic planning (Claude Web) then Implementation (Claude Code)
- Research phase (Claude Web) then Production automation (Claude Code)
- Prototyping instructions (Claude Web) then Modularizing to plugin (Claude Code)

---

## Migration Path: Web to Code

```
CLAUDE WEB PROJECT
├── Project Instructions ──────────────────────────────────────────────┐
│   "You are a helpful assistant that..."                             │
│                                                                      │
├── Project Knowledge ─────────────────────────────────────────────────┤
│   - guide.pdf                                                        │
│   - templates.md                                                     │
│   - examples/                                                        │
└──────────────────────────────────────────────────────────────────────┘
                                │
                                │ MODULARIZE
                                ▼
CLAUDE CODE PLUGIN
├── CLAUDE.md ← Core identity from instructions
├── rules/
│   └── principles.md ← Behavioral guidelines from instructions
├── skills/
│   └── domain-expert/ ← Procedural knowledge from guide.pdf
├── agents/
│   └── specialist.md ← Persona aspects from instructions
├── commands/
│   └── generate-doc.md ← Workflows from templates.md
└── knowledge/
    └── examples/ ← Reference material
```

---

## Summary Table

| Dimension | Claude Web | Claude Code | Winner For |
|-----------|------------|-------------|------------|
| **Ease of Use** | High | Medium | Quick tasks: Web |
| **Modularization** | None | Full | Maintainability: Code |
| **Distribution** | None | Marketplace + Git | Sharing: Code |
| **RAG** | Built-in (opaque) | Manual/MCP | Control: Code; Convenience: Web |
| **Automation** | None | Hooks + MCP | Automation: Code |
| **Conversation History** | Persistent | Session-only | Planning: Web |
| **Token Control** | Hidden | Explicit | Optimization: Code |
| **Development Iteration** | Upload/download friction | Direct file access | Development: Code |
| **Non-technical Users** | Accessible | Requires CLI comfort | Accessibility: Web |

---

## Appendix: RAG Architecture Differences

### Claude Web (Built-in, Opaque)

```
User Query
    │
    ▼
┌─────────────────┐
│ Semantic Search │ ← Black box, not configurable
│ (Anthropic RAG) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Retrieved Chunks│ ← User cannot see what was retrieved
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Claude Response │
└─────────────────┘
```

### Claude Code (Manual or MCP-based)

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Option A: Manual @imports                                               │
│ - User explicitly references files                                      │
│ - Full control, but requires knowing what to load                       │
├─────────────────────────────────────────────────────────────────────────┤
│ Option B: MCP Vector DB (e.g., Pinecone, Weaviate, Chroma)             │
│ - Semantic search via tool call                                         │
│ - User configures embedding model, chunk size, similarity threshold     │
│ - Full visibility and control                                           │
├─────────────────────────────────────────────────────────────────────────┤
│ Option C: Skill-based Retrieval                                         │
│ - Skill metadata triggers on relevant queries                           │
│ - Skill content loads procedural knowledge                              │
│ - Progressive disclosure pattern                                        │
└─────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ Claude Response │ ← User knows exactly what context was used
└─────────────────┘
```

**Key Takeaway**: Claude Code requires more effort to implement RAG but offers transparency and customization. This is a clear area where Claude Code users would benefit from built-in semantic search as an option.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-28 | Initial comprehensive comparison |
