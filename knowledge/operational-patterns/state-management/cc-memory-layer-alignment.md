---
id: cc-memory-layer-alignment
title: CC Memory Layer Alignment — CAB Operational Mapping
category: state-management
tags: [memory, auto-memory, subagent-memory, claude-md, 7-layer, mapping]
summary: Operational mapping of Claude Code's memory systems (CLAUDE.md + auto memory + subagent persistent memory) to CAB state architecture. Covers all 3 subagent memory scopes (user/project/local), auto-injection behavior, plugin-context restrictions, and CAB's per-agent memory adoption matrix. Complement to filesystem-patterns.md §CC Memory Layer Alignment.
depends_on: [filesystem-patterns]
related: [session-lifecycle, bootstrap-read-pattern]
complexity: intermediate
last_updated: 2026-04-22
estimated_tokens: 1800
source: https://code.claude.com/docs/en/memory (fetched 2026-04-22); https://code.claude.com/docs/en/sub-agents#enable-persistent-memory (fetched 2026-04-22); UXL-022 deliverable in impl-plan-ux-log-tracker-2026-04-22.md
confidence: A
review_by: 2026-07-22
---

# CC Memory Layer Alignment — CAB Operational Mapping

> Operational complement to [filesystem-patterns.md §CC Memory Layer
> Alignment](filesystem-patterns.md#cc-memory-layer-alignment). That section
> frames **separation of concerns** between CC's 7-layer internal memory and
> CAB's curated `notes/*.md` state. This card documents **how to configure
> each memory layer** when operating CAB extensions — especially subagent
> persistent memory which is new to CAB's awareness as of 2026-04-22 docs
> refresh (see UXL-031).

## Two Memory Systems at Main-Agent Level

CC Claude Code has two complementary memory systems at the main-session level.
Both are context (not enforced configuration).

| | CLAUDE.md files | Auto memory |
|---|---|---|
| Who writes it | You | Claude |
| Contains | Instructions + rules | Learnings + patterns |
| Scope | Project / user / org | Per git repo (worktrees share) |
| Loaded | Every session, in full | Every session, first 200L / 25KB of `MEMORY.md` |
| Use for | Coding standards, workflows, architecture | Build commands, debugging insights, preferences |

## Auto Memory Specification

- **Requires**: Claude Code v2.1.59+
- **Location**: `~/.claude/projects/<project>/memory/` — `<project>` derived
  from git repo path, so all worktrees of same repo share one directory.
  Outside a git repo, project root is used.
- **Configurable override**: `autoMemoryDirectory` setting (user or local
  settings only — rejected from project `settings.json` to prevent
  shared-project redirection to sensitive paths).
- **Enable/disable**: `autoMemoryEnabled` setting (default `true`) or
  `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` env var.
- **Structure**:
  ```
  ~/.claude/projects/<project>/memory/
  ├── MEMORY.md          # Index — auto-loaded (200L / 25KB limit)
  ├── debugging.md       # Topic file — loaded on demand
  ├── api-conventions.md # Topic file — loaded on demand
  └── ...
  ```
- **Management**: `/memory` command lists loaded files + toggles auto memory +
  provides folder-open link.

**CAB relationship**: auto memory is machine-local and git-excluded. It does
NOT replace CAB's `notes/*.md` curated state — the two serve different
purposes (CC auto-memory = ephemeral learnings; CAB `notes/` = semantic
continuity across sessions). See filesystem-patterns.md for design rationale.

## Subagent Persistent Memory (`memory:` frontmatter field)

Opt-in via the agent's YAML frontmatter:

```yaml
---
name: example-agent
description: ...
memory: project   # scopes: user / project / local
---
```

### Scope → Location Map

| Scope | Location | Use when |
|---|---|---|
| `user` | `~/.claude/agent-memory/<agent-name>/` | Subagent's learnings apply across ALL projects |
| `project` | `.claude/agent-memory/<agent-name>/` | Subagent's knowledge is project-specific + SHAREABLE via git |
| `local` | `.claude/agent-memory-local/<agent-name>/` | Project-specific but GITIGNORED (not checked in) |

**Recommended default: `project`** (per current CC docs) — enables
version-controlled team shareability.

### Behavior When `memory:` Is Set

- Subagent's **system prompt auto-injects** first 200 lines / 25KB of that
  scope's `MEMORY.md` (whichever comes first), with instructions to curate
  `MEMORY.md` if it exceeds the limit.
- **Read / Write / Edit tools auto-enabled** so the subagent can manage its
  own memory files (regardless of `tools:` allowlist).
- Memory persists across conversations — enables cross-invocation learning.

### Plugin Context Restrictions

Per current CC docs, **plugin-provided subagents silently drop**:
- `hooks:`
- `mcpServers:`
- `permissionMode:`

These are NOT restricted by the memory system, but plugin-authored agents
that need those fields must be copied to `.claude/agents/` or
`~/.claude/agents/` to take effect. `memory:` itself works in plugin agents.

## CAB Per-Agent Memory Adoption Matrix

Applied 2026-04-22 per UXL-032 execution. Decision rule: adopt `memory:` when
the agent has cross-invocation-valuable learnings that would compound over
time. Skip when agent is stateless-per-invocation by design.

| Agent | Decision | Scope | Rationale |
|---|---|---|---|
| `architecture-advisor` | ADOPT | `project` | Accumulates architecture decisions, integration case patterns, proposed config templates — shareable across CAB contributors |
| `verifier` | ADOPT | `project` | Failure signatures, recurring anti-patterns, common AC verdicts — compound into better adversarial reviews |
| `project-integrator` | ADOPT | `user` | Integration patterns repeat across projects (HydroCast, RAS-exec, future) — cross-project learnings have stronger signal than project-specific |
| `orchestrator` | SKIP | — | Stateless-per-invocation by design; state lives in `notes/*.md`. Adding agent memory would compete with (and potentially fragment) the curated `notes/` state layer |

**Policy**: orchestrator-class agents should generally NOT use `memory:` — by
CAB's architecture, semantic state is `notes/*.md` (see DP4 Orchestration +
State). Exception: when an orchestrator handles a truly stateless workflow
domain with no `notes/` artifact layer.

## Patterns

- **Prompt the subagent to consult memory**: "Review this PR, and check your
  memory for patterns you've seen before."
- **Prompt to update memory after completion**: "Now that you're done, save
  what you learned to your memory."
- **Embed memory discipline in agent system prompt**: "Update your agent
  memory as you discover codepaths, patterns, library locations, and key
  architectural decisions. Write concise notes about what you found and
  where."

## Anti-Patterns

- **Adding `memory:` to stateless agents** — bloats system prompt budget
  without payoff. Orchestrator-class agents should skip.
- **Using `local` scope when `project` would work** — local hides learnings
  from collaborators; use only for personal/sensitive learnings that
  shouldn't reach the shared repo.
- **Relying on MEMORY.md beyond its auto-load budget** — content past 200L
  or 25KB is NOT auto-loaded; it's on-demand. Keep `MEMORY.md` as an index,
  move details to topic files.
- **Duplicating CAB's `notes/` into agent memory** — these solve different
  problems (CAB `notes/` = curated project semantics; agent memory =
  per-agent cross-invocation learnings). Don't mirror.

## Related

- [filesystem-patterns.md §CC Memory Layer Alignment](filesystem-patterns.md) — separation-of-concerns design rationale
- [.claude/rules/component-standards.md §Agent Frontmatter](../../../.claude/rules/component-standards.md) — valid agent frontmatter fields (refreshed 2026-04-22 per UXL-031)
- LL-10 (fresh-fetch before KB edit) — applied to this card during authoring
- LL-11 (wrapper philosophy) — this card links to CC docs, doesn't re-state field enumeration
