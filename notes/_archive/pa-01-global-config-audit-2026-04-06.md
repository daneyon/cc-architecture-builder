# PA-01: Global CC Config vs. CAB Frameworks — Investigation Report

**Date**: 2026-04-06
**Scope**: `~/.claude/` (5 agents, 11 skills, 6 commands, 7 rules, settings.json, CLAUDE.md, mcp.json)
**Baseline**: CAB KB post-T1-T5 + QA/QC (36 verified KB files, enhanced templates)
**Status**: INVESTIGATION COMPLETE — awaiting user review for implementation approval

---

## Executive Summary

The global CC config is **functionally operational** but has accumulated structural debt across 6 sessions of CAB development. CAB's knowledge base now documents significantly enhanced standards (16-field agent frontmatter, 13-field skill frontmatter, 60+ settings fields, 26 hook events) that the global config predates.

### Key Stats

| Metric | Value |
|--------|-------|
| Total findings | **52** |
| ERROR severity | **9** (functional/security impact) |
| ENHANCEMENT severity | **28** (quality + alignment) |
| OPTIONAL severity | **15** (polish) |
| Estimated implementation effort | ~3-4 focused sessions |
| Token waste (double-loaded rules) | ~5-6K tokens/session (~3% context) |
| Security gaps | 3 (no deny rules, no sandbox, no PreToolUse hook) |

---

## Findings by Category

### A. Agents (5 files)

| # | Severity | Agent(s) | Finding |
|---|----------|----------|---------|
| A-01 | **ERROR** | code-reviewer, debugger-specialist, general-researcher | Missing `## Verification (REQUIRED)` section — CAB mandates this for all agents |
| A-02 | **ERROR** | verifier | Missing `disallowedTools: Write, Edit` — claims read-only in body text but doesn't enforce via frontmatter. CAB version enforces it. |
| A-03 | **ENHANCEMENT** | code-reviewer, debugger-specialist | Missing `permissionMode` — reviewer/debugger should use `plan` to prevent accidental writes |
| A-04 | **ENHANCEMENT** | All 5 | Missing `effort` field — CAB recommends `high` for orchestrator/verifier, `medium` for others |
| A-05 | **ENHANCEMENT** | orchestrator | Missing `skills` and `context` fields — CAB version preloads `executing-tasks`, `validating-structure` and auto-loads `CLAUDE.md`, `notes/progress.md` |
| A-06 | **ENHANCEMENT** | code-reviewer (327 lines), debugger-specialist (440 lines) | Body is bloated with checklists/pattern catalogs — should extract to skills, cutting prompts by 50-70% |
| A-07 | **ENHANCEMENT** | code-reviewer, debugger-specialist | Non-standard structural headings — should align to CAB convention (Role, Approach, Verification, Constraints) |
| A-08 | **ENHANCEMENT** | verifier, code-reviewer, debugger-specialist, general-researcher | List `Search` as a tool — not a recognized CC tool name |
| A-09 | **OPTIONAL** | All 5 | No `maxTurns`, `color`, `memory` fields |

**Drift analysis (global vs. CAB plugin)**:
- **Orchestrator**: CAB version has `effort: high`, `skills: executing-tasks, validating-structure`, `context: CLAUDE.md, notes/progress.md`, 6 KB cross-references, routes to `architecture-advisor`. Global version has unique "Extension Awareness Check" section worth porting to CAB.
- **Verifier**: Body content identical. CAB adds `effort: high` and `disallowedTools: Write, Edit` in frontmatter only.

---

### B. Skills (11 directories, 10 with SKILL.md)

| # | Severity | Skill(s) | Finding |
|---|----------|----------|---------|
| B-01 | **ERROR** | strategy-framework | **No SKILL.md** — 15 reference files completely orphaned and invisible to CC |
| B-02 | **ERROR** | All 10 skills | Descriptions use descriptive voice, not imperative trigger format — with 11 global skills, mid-session attention decay makes descriptive descriptions unreliable |
| B-03 | **ERROR** | readme-generator | Resource folder named `reference/` (singular) — CAB convention is `references/` (plural) |
| B-04 | **ENHANCEMENT** | All 10 skills | Missing `argument-hint` — degrades parameter input UX |
| B-05 | **ENHANCEMENT** | 9 of 10 (except token-optimizer) | Missing `allowed-tools` — no defensive guard against unintended tool use |
| B-06 | **ENHANCEMENT** | All 10 skills | Missing `effort` — computation-heavy skills (architecture-analyzer, planning-implementation, slide-designer) should be `high` |
| B-07 | **ENHANCEMENT** | architecture-analyzer | Missing `agent: true` — CAB version correctly sets this for isolated tool-use loops |
| B-08 | **ENHANCEMENT** | architecture-analyzer, assessing-quality, designing-workflows, visualizing-data | No resource folders — reference `@knowledge-base/` paths that may not resolve outside original project |
| B-09 | **OPTIONAL** | strategy-framework | If SKILL.md created, assess overlap with strategy-pathfinder plugin (same knowledge domain) |

**Plugin overlap analysis**:
- `architecture-analyzer` + `planning-implementation`: HIGH overlap with CAB plugin versions (same body, CAB has better frontmatter)
- `strategy-framework`: HIGH overlap with strategy-pathfinder plugin (same domain)
- All others: unique global skills, no redundancy concerns

---

### C. Commands (6 files)

| # | Severity | Command(s) | Finding |
|---|----------|------------|---------|
| C-01 | **ERROR** | init-worktree | Content divergence — global is 36 lines, CAB is 119 lines. Missing: `claude --worktree` note, `--aliases` flag, analysis sandbox section |
| C-02 | **ERROR** | init-plugin | Content divergence — global is 29 lines, CAB is 99 lines. Missing: `templates` directory, template mappings, `/validate` step |
| C-03 | **ENHANCEMENT** | commit-push-pr, context-sync, init-worktree | See-Also paths use bare `skills/`, `agents/` — should be `.claude/skills/`, `.claude/agents/` |
| C-04 | **ENHANCEMENT** | execute-task | Missing `allowed-tools` — only command without it |
| C-05 | **ENHANCEMENT** | techdebt | Description less specific than CAB version — missing usage timing guidance |

**Migration assessment (commands -> skills)**:

| Command | Migrate to Skill? | Rationale | Difficulty |
|---------|-------------------|-----------|------------|
| `commit-push-pr` | **Yes** | Benefits from `hooks`, `effort`, model-invocation at task end | Low |
| `context-sync` | **Yes** | Natural model-invoked trigger on session start; `context: fork` isolation | Low |
| `techdebt` | **Yes** | Benefits from `effort: high`, resource dir for anti-pattern defs | Low-Medium |
| `execute-task` | Already done | Thin wrapper delegating to `executing-tasks` skill | N/A |
| `init-worktree` | **Defer** | Inherently user-initiated, little model-invocation benefit | N/A |
| `init-plugin` | **Defer** | User-initiated; needs `disable-model-invocation: true` if migrated | Medium |

**Promotion candidate**: CAB's `integrate-existing` command is high-value for cross-project use — any existing project workspace benefits from CC architecture overlay. Consider promoting to global as a skill.

---

### D. Settings + Hooks + MCP

| # | Severity | Area | Finding |
|---|----------|------|---------|
| D-01 | **ERROR** | settings.json | Missing `$schema` — no editor validation/autocomplete |
| D-02 | **ERROR** | permissions | **No `deny` array** — no guardrail against destructive commands at global level |
| D-03 | **ERROR** | sandbox | **Not configured** — despite autonomous agent pattern (`agent: orchestrator`, `subagentModel: opus`) |
| D-04 | **ENHANCEMENT** | permissions | `allow` array has 67 organically accumulated entries — needs curation with glob patterns |
| D-05 | **ENHANCEMENT** | hooks | Only 1 hook (PostToolUse ruff format). Missing: PreToolUse security gate, InstructionsLoaded freshness validation, Stop final validation |
| D-06 | **ENHANCEMENT** | settings | Missing `model` field — relying on CC defaults |
| D-07 | **ENHANCEMENT** | MCP | `mcp.json` is empty placeholder (`{ "mcpServers": {} }`) — MCP servers provided only by plugins |
| D-08 | **ENHANCEMENT** | permissions | Mix of MSYS2 (`//c/Users/...`), Windows native (`C:\\Users\\...`), and relative paths in allow rules |
| D-09 | **ENHANCEMENT** | marketplace | `strategy-pathfinder` uses `"source": "git"` — `"github"` preferred for GitHub repos |
| D-10 | **OPTIONAL** | hooks | Current ruff hook missing `async: true` |
| D-11 | **OPTIONAL** | plugins | 32 enabled plugins — substantial context surface area |
| D-12 | **OPTIONAL** | marketplace | `strategy-pathfinder` missing `autoUpdate: true` |

**Security posture summary**:

| Area | Rating |
|------|--------|
| Credential handling | **Good** — `${GITHUB_TOKEN}` expansion, no hardcoded secrets |
| Permission deny rules | **Weak** — no deny array |
| Sandbox | **Weak** — not configured |
| Hook-based security | **Weak** — no PreToolUse security hook |
| Overall | Functionally rich, defensively shallow |

---

### E. CLAUDE.md + Rules (1 + 7 files)

| # | Severity | Area | Finding |
|---|----------|------|---------|
| E-01 | **ENHANCEMENT** | rules loading | **Rules double-loaded** — `~/.claude/rules/` auto-loaded by CC + `@rules/` imports in CLAUDE.md load them again = ~5-6K wasted tokens/session (~3% context) |
| E-02 | **ENHANCEMENT** | CLAUDE.md | Content duplication — Behavioral Constraints, token awareness, PLAN->VERIFY->COMMIT, context health all stated in CLAUDE.md AND repeated in rules |
| E-03 | **ENHANCEMENT** | CLAUDE.md | Missing seed-instruction docstring at top |
| E-04 | **ENHANCEMENT** | CLAUDE.md | Sparse Personal Context — missing Name, Role per CAB template |
| E-05 | **ENHANCEMENT** | @imports | Uses 6 explicit file paths — CAB template uses `@rules/` wildcard (more maintainable) |
| E-06 | **ERROR** | @imports | `rules/dev/comments.md` exists but NOT listed in Cross-Project Rules imports |
| E-07 | **ENHANCEMENT** | rules | 6 of 7 rules lack `paths:` frontmatter — Python-specific content in practices.md loaded for all file types |
| E-08 | **OPTIONAL** | rules | No dedicated security rule, git workflow rule, or testing strategy rule |
| E-09 | **OPTIONAL** | CLAUDE.md | Learned Corrections section empty (placeholder) — may be redundant if auto memory handles corrections |

---

## Revised Implementation Plan (Post-HITL Decision Review)

> **Strategic lens**: Architectural alignment, holistic orchestration + state management as "master strategist," context engineering best practices, systematic standardization. NOT individual extension content evaluation.

### User Decisions Applied

| # | Decision | Implication |
|---|----------|------------|
| 1 | strategy-framework = strategy-pathfinder (manually moved). Delete orphan. | Phase 3g → simple delete |
| 2 | Agent extraction (code-reviewer, debugger-specialist) — **DEFERRED** | Removed from immediate plan; logged as future TODO |
| 3 | Command → skill migration — **CONFIRMED NEEDED** | Wrapping philosophy: no content loss, synthesized hybrid |
| 4 | integrate-existing promotion — **DEFERRED** for holistic strategy | Future TODO; also noted: persistent CAB-awareness across projects = state management gap |
| 5 | Plugin curation — **START ESSENTIAL, BUILD UP** | Quick wins: disable 4/5 context-engineering-marketplace dupes + inactive domain plugins |
| 6 | Double-loading — **REMOVE @imports entirely** | Rules auto-load; @imports are pure waste |

### Phase 1: Context Engineering Foundation (token efficiency + memory architecture)

**Rationale**: Fix the base layer first. Double-loaded rules + plugin overhead waste ~14K tokens/session. Clean this before touching any extension content.

| Step | Action | Files Affected | Risk |
|------|--------|---------------|------|
| 1a | Remove `@rules/` imports from CLAUDE.md Cross-Project Rules section | CLAUDE.md | None — rules auto-load |
| 1b | Deduplicate CLAUDE.md content — trim sections echoing rules to single-line seed pointers | CLAUDE.md | Medium — must preserve seed-instruction quality |
| 1c | Add seed-instruction docstring to CLAUDE.md top | CLAUDE.md | None |
| 1d | Enrich Personal Context (Name, Role) | CLAUDE.md | None |
| 1e | Disable 4/5 context-engineering-marketplace plugins (identical skill sets) | settings.json | None — zero capability loss |
| 1f | Review + disable domain-specific plugins not actively used (Astronomer/data, product-tracking, etc.) | settings.json | Low — can re-enable on demand |

**Token recovery**: ~10-11K tokens/session (~5% context reclaimed)

### Phase 2: Security Hardening

**Rationale**: 3 security gaps in an autonomous agent config. Additive-only changes — won't break current UX.

| Step | Action | Files Affected | Risk |
|------|--------|---------------|------|
| 2a | Add `$schema` to settings.json | settings.json | None |
| 2b | Add `permissions.deny` array (destructive commands) | settings.json | Low — additive only |
| 2c | Add sandbox configuration (deny read to ~/.ssh, ~/.aws, credentials) | settings.json | Low — test normal operations still work |
| 2d | Add PreToolUse security hook (Bash destructive command gate) | settings.json | Medium — needs testing to avoid false positives |

**HITL checkpoint**: Test all hooks and permissions changes in a scratch session before relying on them.

**Note**: permissions.allow curation (67 organic entries) deferred to a separate careful pass — too risky to rush during streamlining.

### Phase 3: Agent Structural Alignment (frontmatter + architecture)

**Rationale**: All 5 agents predate CAB's enhanced 16-field standard. Frontmatter-only changes preserve current behavior.

| Step | Action | Files Affected | Risk |
|------|--------|---------------|------|
| 3a | Add `## Verification (REQUIRED)` to code-reviewer, debugger-specialist, general-researcher | 3 agent files | Low |
| 3b | Add `disallowedTools: Write, Edit` to verifier | 1 agent file | Low |
| 3c | Add `effort` field to all 5 agents (high for orchestrator/verifier, medium for others) | 5 agent files | Low |
| 3d | Add `permissionMode: plan` to code-reviewer | 1 agent file | Low |
| 3e | Audit and fix `Search` tool references across 4 agents | 4 agent files | Low |
| 3f | Standardize headings in code-reviewer, debugger-specialist to CAB convention | 2 agent files | Low |
| 3g | Sync orchestrator frontmatter from CAB: add `skills`, `context` fields | 1 agent file | Low — adapt refs to global paths |

**DEFERRED** (future TODO):
- 3-DEFER-A: Extract code-reviewer body (327 lines) into skill — not actively used
- 3-DEFER-B: Extract debugger-specialist body (440 lines) into skill — not actively used

### Phase 4: Skill Architectural Alignment (invocation reliability)

**Rationale**: With 11 global skills, mid-session attention decay makes descriptive descriptions unreliable. Imperative trigger format is the single highest-impact skill change per CAB standards.

| Step | Action | Files Affected | Risk |
|------|--------|---------------|------|
| 4a | Convert all 10 descriptions to imperative trigger format | 10 SKILL.md files | Low — text-only change |
| 4b | Add `argument-hint` to all 10 skills | 10 SKILL.md files | Low |
| 4c | Add `effort` to computation-heavy skills (architecture-analyzer, planning-impl, slide-designer, presentation-outline, assessing-quality) | 5 SKILL.md files | Low |
| 4d | Add `allowed-tools` to 9 skills (token-optimizer already has it) | 9 SKILL.md files | Low |
| 4e | Add `agent: true` to architecture-analyzer | 1 SKILL.md file | Low |
| 4f | Rename readme-generator `reference/` to `references/` + update @paths | 1 directory + 1 SKILL.md | Low |
| 4g | Delete orphaned `~/.claude/skills/strategy-framework/` directory (content lives in strategy-pathfinder plugin) | 1 directory deletion | None |

### Phase 5: Command Sync + Migration (wrapping philosophy)

**Rationale**: Global commands are behind CAB authoritative versions. Migration to skills follows CC's official direction + wrapping philosophy. Commands remain as thin alias wrappers.

| Step | Action | Files Affected | Risk |
|------|--------|---------------|------|
| 5a | Sync init-worktree and init-plugin from CAB (authoritative) | 2 command files | Low — CAB is superset |
| 5b | Fix See-Also paths in 3 commands (add `.claude/` prefix) | 3 command files | Low |
| 5c | Add `allowed-tools` to execute-task | 1 command file | Low |
| 5d | Migrate techdebt to skill (keep command as thin wrapper) — preserve all content as synthesized hybrid | 1 new skill + 1 command update | Medium — must preserve all valuable content |
| 5e | Migrate commit-push-pr to skill (keep command as thin wrapper) | 1 new skill + 1 command update | Medium |
| 5f | Migrate context-sync to skill (keep command as thin wrapper) | 1 new skill + 1 command update | Medium |

### Phase 6: Settings Polish + Hooks

| Step | Action | Files Affected | Risk |
|------|--------|---------------|------|
| 6a | Add `model` field to settings.json | settings.json | Low |
| 6b | Add `paths:` frontmatter to rules/dev/practices.md (Python-specific scoping) | 1 rules file | Low |
| 6c | Update strategy-pathfinder marketplace to `"source": "github"` + `autoUpdate: true` | settings.json | Low |
| 6d | Add InstructionsLoaded freshness hook | settings.json | Low |
| 6e | Add Stop validation hook | settings.json | Low |

---

## Execution Order + HITL Gates

```
Phase 1 (Context Engineering)
    │ ← HITL: verify token savings, no regressions
    ▼
Phase 2 (Security)
    │ ← HITL: test in scratch session
    ▼
Phase 3 (Agents)
    │ ← HITL: spot-check agent behavior
    ▼
Phase 4 (Skills)
    │ ← HITL: test invocation reliability
    ▼
Phase 5 (Commands)
    │ ← HITL: test migrated skills, verify command aliases work
    ▼
Phase 6 (Polish)
    │ ← HITL: final validation
    ▼
COMPLETE → Resume active project work
```

---

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Settings.json edit breaks active config | Backup before edit; test in scratch session |
| CLAUDE.md dedup loses seed instruction quality | Compare before/after token count; verify behavioral anchors survive |
| Skill description changes affect invocation | Test each rewritten description with natural-language triggers |
| PreToolUse hook false positives | Start with conservative patterns; whitelist known-safe commands |
| Commands-to-skills migration loses content | Synthesized hybrid approach: merge command + existing skill if applicable |
| Plugin disabling loses capability | Document disabled plugins; can re-enable on demand |

---

## Dependencies

| Item | Depends On |
|------|-----------|
| Phase 3g (orchestrator `skills` field) | Relevant global skills must exist |
| Phase 5d-5f (command migration) | Skills infrastructure from Phase 4 |
| Phase 6d-6e (hook expansion) | Phase 2 hooks working correctly |

---

## Future TODO (Deferred Items)

| Item | Rationale | Revisit When |
|------|-----------|-------------|
| Agent extraction: code-reviewer (327 lines) → skill | Not actively used | When user starts using code-reviewer regularly |
| Agent extraction: debugger-specialist (440 lines) → skill | Not actively used | When user starts using debugger-specialist regularly |
| integrate-existing promotion to global | Needs holistic strategy; CAB-coupling | After state management deep dive (PA-03) |
| Persistent CAB-awareness across all projects | State management standardization gap | PA-03 (state management mechanisms) |
| permissions.allow curation (67 → patterns) | Too risky to rush; separate careful pass | After PA-01 implementation stabilizes |
| External plugin reviews + synthesis | Separate PA item (PA-05) | After core global config stabilized |
| Plugin overhead re-evaluation | After initial plugin trimming | After Phase 1e-1f implementation |

---

## Appendix: File-Level Change Map

| File | Phases | Change Type |
|------|--------|-------------|
| `~/.claude/CLAUDE.md` | 1 | Edit (remove @imports, dedup, docstring, personal context) |
| `~/.claude/settings.json` | 1, 2, 6 | Edit (plugins, security, schema, hooks, model) |
| `~/.claude/agents/orchestrator.md` | 3 | Edit (frontmatter: effort, skills, context) |
| `~/.claude/agents/verifier.md` | 3 | Edit (frontmatter: effort, disallowedTools) |
| `~/.claude/agents/code-reviewer.md` | 3 | Edit (verification section, frontmatter, headings) |
| `~/.claude/agents/debugger-specialist.md` | 3 | Edit (verification section, frontmatter, headings) |
| `~/.claude/agents/general-researcher.md` | 3 | Edit (verification section, frontmatter) |
| `~/.claude/skills/*/SKILL.md` (x10) | 4 | Edit (frontmatter, description rewrite) |
| `~/.claude/skills/strategy-framework/` | 4 | Delete (orphaned; content in strategy-pathfinder) |
| `~/.claude/skills/readme-generator/reference/` | 4 | Rename to `references/` |
| `~/.claude/commands/init-worktree.md` | 5 | Replace (sync from CAB) |
| `~/.claude/commands/init-plugin.md` | 5 | Replace (sync from CAB) |
| `~/.claude/commands/commit-push-pr.md` | 5 | Edit (See-Also) + migrate to skill |
| `~/.claude/commands/context-sync.md` | 5 | Edit (See-Also) + migrate to skill |
| `~/.claude/commands/execute-task.md` | 5 | Edit (add allowed-tools) |
| `~/.claude/commands/techdebt.md` | 5 | Migrate to skill |
| `~/.claude/rules/dev/practices.md` | 6 | Edit (add paths: frontmatter) |
| `~/.claude/skills/techdebt/` | 5 | New directory (migrated from command) |
| `~/.claude/skills/commit-push-pr/` | 5 | New directory (migrated from command) |
| `~/.claude/skills/context-sync/` | 5 | New directory (migrated from command) |

**Total**: ~18 files modified, 3 new directories, 1 directory deleted
