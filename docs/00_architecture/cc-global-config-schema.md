# Claude Code Global Config Schema

**Version**: 0.2.0-draft
**Purpose**: Canonical directory structure, naming conventions, and component placement rules for the standardized `~/.claude/` global user configuration.

---

## Directory Structure

```
~/.claude/
├── CLAUDE.md                          # LEAN: core identity + @imports
├── settings.json                      # Global CC runtime settings
│
├── rules/                             # Memory Layer (always loaded)
│   ├── dev/                           #   Development standards
│   │   ├── philosophy.md
│   │   ├── practices.md
│   │   ├── comments.md
│   │   ├── token-efficiency.md
│   │   └── testing.md
│   ├── comm/                          #   Communication standards
│   │   ├── interaction.md
│   │   └── style-lexicon.md
│   ├── gov/                           #   Governance & risk
│   │   ├── responsible-ai.md
│   │   └── risk-mgmt.md
│   └── process/                       #   Workflow & analysis standards
│       ├── analysis-framework.md
│       └── agent-pipeline.md
│
├── skills/                            # Capability Registry (lazy-loaded)
│   ├── dev-analyze-architecture/      #   [dev-] Code & architecture
│   ├── dev-design-data-model/
│   ├── dev-design-ui/
│   ├── doc-generate-readme/           #   [doc-] Documentation & output
│   ├── doc-export-session/
│   ├── doc-design-diagram/
│   ├── plan-design-implementation/    #   [plan-] Planning & strategy
│   ├── plan-apply-strategy/
│   ├── plan-manage-project/
│   ├── plan-design-gtm/
│   ├── plan-analyze-metrics/
│   ├── ai-engineer-prompt/            #   [ai-] AI/LLM interaction
│   ├── ai-search-docs/
│   ├── ai-optimize-tokens/
│   ├── ai-design-agent/
│   └── ops-manage-feedback/           #   [ops-] Operations
│
├── agents/                            # Team Members (isolated context)
│   ├── code-reviewer.md
│   ├── debugger-specialist.md
│   ├── performance-optimizer.md
│   ├── software-architect.md
│   ├── codebase-manager.md
│   ├── security-auditor.md
│   ├── product-manager.md
│   ├── ux-researcher.md
│   ├── ux-designer.md
│   └── tech-writer.md
│
├── commands/                          # Workflow Triggers (user-invoked)
│   ├── commit-push-pr.md
│   ├── init-project.md
│   └── advance-phase.md
│
├── plugins/                           # Installed external plugins
│   ├── marketplaces/
│   └── [system-managed]
│
└── [system folders]                   # Auto-managed by CC runtime
    ├── memory/
    ├── exports/
    ├── projects/
    └── ...
```

---

## Naming Convention Standard

### Universal Rules (All Components)

| Rule | Constraint | Example |
|---|---|---|
| Character set | `[a-z0-9-]` only | `plan-design-implementation` |
| Word separator | Single hyphen `-` | NOT `plan--design` or `plan_design` |
| Max length | 64 chars (practical target: 30) | Most names: 15-27 chars |
| No special chars | No underscores, dots, double-hyphens | -- |
| No emoji/unicode | ASCII only | -- |

### Skills: `{domain}-{verb}-{object}`

**Pattern**: Domain prefix + imperative verb + target object

| Domain Prefix | Scope | Examples |
|---|---|---|
| `dev-` | Code, architecture, quality | `dev-analyze-architecture`, `dev-design-data-model` |
| `doc-` | Documentation, output, export | `doc-generate-readme`, `doc-export-session` |
| `plan-` | Planning, strategy, PM | `plan-design-implementation`, `plan-manage-project` |
| `ai-` | AI/LLM interaction, governance | `ai-engineer-prompt`, `ai-search-docs` |
| `ops-` | Operations, feedback, deployment | `ops-manage-feedback` |

**Future domain expansion** (when needed):

| Potential Prefix | When to Add |
|---|---|
| `data-` | When data engineering/analytics skills emerge |
| `sec-` | When security-specific skills justify their own domain |

### Skill Directory Scaffold

Every skill follows this structure:

```
{domain}-{verb}-{object}/
├── SKILL.md              # Required: YAML frontmatter + body
├── scripts/              # Executable code (deterministic tasks)
│   └── .gitkeep
├── references/           # Docs loaded into context on-demand
│   └── .gitkeep
└── assets/               # Output resources (NOT loaded into context)
    └── .gitkeep
```

**Consistency rules:**
- Always `references/` (plural), never `reference/`
- Always include all three resource folders (even if empty, with `.gitkeep`)
- No extraneous files (README.md, CHANGELOG.md, etc.) in skill directories

### Agents: `{specialization}-{role}`

Agents are team members (nouns/roles), not actions:

| Pattern | Examples |
|---|---|
| `{domain}-{role}` | `code-reviewer`, `qa-lead` |
| `{specialty}-{role}` | `debugger-specialist`, `performance-optimizer` |
| `{function}-{noun}` | `app-designer`, `codebase-manager` |

### Rules: `{domain}/{topic}.md`

Rules use short domain folder names (3-4 chars):

| Folder | Full Domain | Content Type |
|---|---|---|
| `dev/` | Development | Coding standards, practices, patterns |
| `comm/` | Communication | Interaction style, tone, formatting |
| `gov/` | Governance | AI ethics, risk management, compliance |
| `process/` | Process | Analysis frameworks, workflow standards |

**Discovery behavior (verified):**
- All `.md` files are discovered **recursively** through subdirectories
- Subdirectory organization is supported and encouraged
- Files support optional `paths:` YAML frontmatter for conditional loading
- Rules without `paths:` frontmatter apply unconditionally (always loaded)

**Key difference from skills/:**
- `rules/` = recursive subdirectory discovery (subdirectories OK)
- `skills/` = direct children only (NO intermediary folders)

### Commands: `{verb}-{object}.md`

Commands are workflow triggers (imperative):

| Pattern | Examples |
|---|---|
| `{verb}-{object}` | `commit-push-pr`, `init-project` |
| `{verb}-{scope}` | `advance-phase` |

---

## Component Placement Rules

### Decision Matrix: Where Does Content Belong?

| Question | If YES | Token Impact |
|---|---|---|
| Must Claude ALWAYS behave this way? | `rules/` | Always loaded (~2-5k total budget) |
| Is it procedural "how-to" knowledge? | `skills/` | Lazy-loaded on trigger |
| Does it need sustained focus / isolated context? | `agents/` | Separate context (zero parent cost) |
| Is it a repeatable workflow shortcut? | `commands/` | Variable (may invoke skills/agents) |
| Is it event-driven automation? | `hooks` | External (zero context cost) |
| Does it need external service access? | `MCP` | ~0.5-1k per server |
| Is it a distributable bundle? | `plugins/` | Sum of components |
| Is it reference-only material? | `skill references/` or `knowledge/` | Only when explicitly read |

### Anti-Patterns to Avoid

| Anti-Pattern | Problem | Correct Placement |
|---|---|---|
| Behavioral guidance as a skill | Wastes metadata slot; should be always-on | `rules/` |
| Sustained-focus task as a skill | Bloats main context; better isolated | `agents/` |
| Domain-specific tool in global config | Pollutes global namespace | Project plugin |
| Large reference docs in `rules/` | Inflates always-loaded token budget | `skill references/` or `knowledge/` |
| Duplicating installed plugin capabilities | Wastes metadata slots | Use plugin or create hybrid |

---

## Token Budget Guidelines

### Layer Budget Allocation

| Layer | Budget | What Counts |
|---|---|---|
| Memory Layer (`CLAUDE.md` + `rules/`) | ~2-5k tokens | All files, always loaded |
| Capability Registry (metadata) | ~1-2k tokens | Skill/command name + description (~1-2 lines each) |
| MCP Tool Signatures | ~0.5-1k per server | Tool definitions |
| **Baseline Overhead** | **~6-12k tokens** | Sum of above |

### Registry Capacity

| Item Type | Current Count | Soft Limit | Notes |
|---|---|---|---|
| Skills + Commands (personal) | ~9 | ~50-60 total | Shared budget with plugin skills |
| Plugin skills | ~33 | (included above) | document-skills, context-eng, etc. |
| **Total registry items** | **~42** | **~50-60** | ~8-18 slots remaining |
| Agents (personal) | ~3 | Separate pool | In Task tool definition |
| Plugin agents | Variable | Separate pool | agents-and-commands plugin |

### Optimization Strategies

1. Keep global skills to ~10-15 (truly universal ones only)
2. Domain-specific skills go in project plugins
3. Behavioral guidance goes to `rules/` (zero registry cost)
4. Sustained-focus work goes to `agents/` (separate budget)
5. Audit installed plugins periodically for overlap

---

## Versioning & Maintenance

| Concern | Approach |
|---|---|
| CC platform updates | Monitor official docs; update schema as CC evolves |
| Plugin conflicts | Audit quarterly; hybrid-merge when duplicate capabilities exist |
| Rules bloat | Review total token footprint; condense overlapping content |
| Skill count growth | Enforce the metadata budget ceiling; migrate to agents or plugins |
| Naming convention changes | Update this document; rename all affected components atomically |

---

## settings.json Configuration

Claude Code's `settings.json` (project-level at `.claude/settings.json` or user-level at `~/.claude/settings.json`) provides declarative configuration for permissions, hooks, environment variables, and behavioral settings.

### Key Settings for Agentic Workflows

| Setting | Scope | Purpose | Example |
|---------|-------|---------|--------|
| `agent` | Project or user | Default agent for main conversation | `"agent": "orchestrator"` |
| `permissions.allow` | Project or user | Pre-approved safe commands (team shares via git) | `["Bash(npm run test:*)"]` |
| `permissions.deny` | Project or user | Explicitly blocked commands | `["Bash(rm -rf *)"]` |
| `hooks.PostToolUse` | Project | Auto-format after Write/Edit | See settings.json template |
| `hooks.Stop` | Project | Deterministic checks at session end | Progress file update reminder |
| `env` | Project or user | Environment variables without wrapper scripts | `{"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"}` |
| `spinnerVerbs` | User | Custom spinner verbs | `["Architecting", "Analyzing"]` |

### Sandbox Configuration

The `/sandbox` command enables file and network isolation for Claude's bash commands:

| Mode | Description | Best For |
|------|-------------|----------|
| Sandbox + auto-allow | Commands run in sandbox, auto-approved | Long-running autonomous agents |
| Sandbox + regular permissions | Sandbox with normal permission prompts | Safety-sensitive projects |
| No Sandbox (default) | Standard behavior | Interactive development |

Enable via `/sandbox` in Claude Code. Sandboxing supports file and network isolation. Windows support pending.

### Effort Levels

`/model` sets the effort level, which directly controls token consumption:

| Level | Token Impact | Use When |
|-------|-------------|----------|
| Low | Fewer tokens, faster | Well-defined, repetitive tasks |
| Medium | Balanced | General development |
| High | More tokens, more intelligence | Complex architecture, debugging, planning |

Boris Cherny uses High for everything on Opus 4.6. For multi-agent cost optimization, consider using Medium for worker agents while keeping High for the orchestrator.
