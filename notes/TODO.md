# CAB (cc-architecture-builder): Live Task Tracker

**Last Updated**: 2026-04-04
**Plugin Version**: 1.0.0 (public release)
**Implementation Plan**: `~/.claude/plans/jazzy-skipping-petal.md`
**Techdebt v2**: `notes/techdebt-v2-2026-04-04.md` (56 actionable items, 5 tiers)

---

## Active — Comprehensive CAB Self-Audit (v1.0.0 → v1.01)

### HITL-01: User Review of Pre-Audit Artifacts (current gate)

- [ ] User review: `notes/cc-docs-investigation-2026-04-04.md` (72 delta items, 11 categories)
- [ ] User review: `notes/techdebt-v2-2026-04-04.md` (56 items, 5-tier plan)
- [ ] User approval to begin T1 implementation

### HITL-02: External Reference Investigation (pending user input)

- [ ] User provides external reference document
- [ ] Deep investigation research + comparison report → "techdebt v3"
- [ ] Merge findings into implementation plan

### T1: Architectural Alignment (blocking — first after HITL approval)

- [ ] T1-01: Memory system rewrite (auto memory, 200-line rec, 4 scopes)
- [ ] T1-02: Skills frontmatter expansion (3→11 fields, substitutions, fork)
- [ ] T1-03: Subagents frontmatter expansion (missing 10+ fields, memory, background)
- [ ] T1-04: Hooks major expansion (9→26 events, 1→4 types, if/async)
- [ ] T1-05: Plugin schema expansion (userConfig, channels, LSP, bin/)
- [ ] T1-06: Settings documentation rewrite (~10→60+ fields, hierarchy, sandbox)
- [ ] T1-07: MCP integration update (registry, channels, HTTP type)
- [ ] T1-08: Custom commands → skills migration documentation
- [ ] T1-09: Effort level verification (max vs high discrepancy)
- [ ] T1-10: URL migration (docs.anthropic.com → code.claude.com)

### T2: Schema & Metadata Compliance (after T1)

- [ ] T2-01: source: metadata backfill (22 files)
- [ ] T2-02: Frontmatter completeness (2 files missing entirely)
- [ ] T2-03: Agent Verification sections (2 agents)
- [ ] T2-04: Agent frontmatter field updates (all 4 agents)
- [ ] T2-05: Skill frontmatter field updates (all 7 skills)
- [ ] T2-06: Create project .claude/settings.json
- [ ] T2-07: Knowledge INDEX.md update
- [ ] T2-08: Marketplace documentation update

### T3: Template & Scaffold Freshness (after T1, parallel with T2)

- [ ] T3-01: settings.json.template update
- [ ] T3-02: plugin.json.template update
- [ ] T3-03: CLAUDE.md.template (plugin) update — 200-line guidance
- [ ] T3-04: CLAUDE.md.template (global) update
- [ ] T3-05: agent.template update (16 fields)
- [ ] T3-06: skill.template update (11 fields)
- [ ] T3-07: command.template update (or deprecation note)
- [ ] T3-08: hooks.json template (4 types)

### T4: Structural Cleanup (can start partially during T1)

- [ ] T4-01: Fix broken cross-reference in agent-skills.md
- [ ] T4-02: Remove duplicate product-design-cycle.md (internal copy)
- [ ] T4-03: Clean settings.local.json ad-hoc permissions
- [ ] T4-04: DUPLICATE files — remove/convert (git-foundation, security-defaults, glossary)
- [ ] T4-05: STALE files — evaluate 6 files for residual value
- [ ] T4-06: Restructure TODO.md (archive completed → notes/_archive/)
- [ ] T4-07: Document sync protocol (CAB upstream ↔ global downstream)
- [ ] T4-08: BRIDGE files — add source references (workflow, references)

### T5: New Capabilities (after T1)

- [ ] T5-01: NEW KB card — Agent Teams
- [ ] T5-02: NEW KB card — Auto Memory Patterns
- [ ] T5-03: Context management section expansion in session-management.md
- [ ] T5-04: Plugin persistent data patterns
- [ ] T5-05: Output styles documentation
- [ ] T5-06: LSP integration documentation
- [ ] T5-07: Managed settings documentation
- [ ] T5-08: INDEX.md final update

### Post-Audit

- [ ] Full remaining global ↔ CAB extension drift audit (Skills: assessing-quality, designing-workflows, visualizing-data, claude-docs-helper, readme-generator, token-optimizer, strategy-framework; Agents: orchestrator, code-reviewer, debugger-specialist, general-researcher)
- [ ] Establish + document sync protocol: CAB upstream → global downstream
- [ ] Deep dive: state management mechanisms strategy (changelog system, programmatic lesson aggregation)
- [ ] Deep dive: standardized audit/freshness-check CC extensions (agentic protocol)
- [ ] User's external plugin reviews + potential synthesis into custom extensions
- [ ] Version bump to v1.01 + deploy to global

---

## Active — Other Projects

### P-LIVE: HEC-RAS Project Integration (remaining items)

- [ ] Configure MCP wrapping for RASCommander
- [ ] Test multi-agent orchestration: orchestrator → domain specialist → verifier
- [ ] Evaluate RAG need based on KB file count

---

## Deferred

### P2: Template & Content Population (deferred to post-audit)

- [ ] Create deliverable templates (PRD, SRD, ADR, SOW) in skill `assets/` — project-specific
- [ ] Create phase-gate checklists (machine-parseable YAML) — project-specific
- [ ] Create project-state.yaml schema for orchestration state management

### P3: Audit & Integration (deferred)

- [ ] Audit installed plugins for overlap with custom extensions
- [ ] Document CC platform priority/conflict resolution rules as educational reference
- [ ] End-to-end test all CC extensions

### P4: Advanced Orchestration & RAG (deferred)

- [ ] Evaluate MCP-based RAG for knowledge bases exceeding ~100 files
- [ ] Test Agent Teams (experimental) for inter-agent communication
- [ ] Evaluate Koylan's context engineering marketplace plugins for complementary install
- [ ] Cowork enterprise distribution testing
- [ ] Agent evaluation framework (systematic quality measurement)
- [ ] Multi-vendor adapter (Gemini CLI / Codex compatibility — future)

---

## Completed Archive

<details>
<summary>P1-HOT: Initial 6-Extension Reconciliation ✅ (2026-04-03)</summary>

- [X] Merge `architecture-analyzer` skill INTO CAB plugin (global → CAB, cleaned stale refs)
- [X] Merge `planning-implementation` skill + assets INTO CAB plugin (global → CAB, 3 files)
- [X] Reconcile `verifier` agent (CAB authoritative → deployed to global)
- [X] Update `commit-push-pr` command (CAB authoritative → deployed to global)
- [X] Update `context-sync` command (CAB authoritative → deployed to global)
- [X] Resolve `execute-task` command (CAB authoritative → deployed to global)
</details>

<details>
<summary>HITL-01 Pre-Audit (Phase 0-3) ✅ (2026-04-04)</summary>

- [X] Phase 0: Commit file deletions (1003ef1), create _archive/, extensions map, changelog concept
- [X] Phase 1: CC docs investigation — 7 parallel agents, 72 delta items across 11 categories
- [X] Phase 2: Techdebt v2 — 56 actionable items in 5 tiers with phase gates
- [X] Phase 3: Verification — all 8 acceptance criteria PASS
</details>

<details>
<summary>P0: Schema & Naming ✅</summary>

- [X] Define product design lifecycle phases and sub-processes
- [X] Define full A-team roster with CC extension mapping
- [X] Define naming conventions for all CC extension types
- [X] Define CC global config directory schema
- [X] Define orchestration framework concept
- [X] Verify `rules/` supports recursive subdirectories (confirmed YES)
- [X] Verify `skills/` does NOT support subdirectories (confirmed)
- [X] Create A-team roster as AI-digestible database (a-team-database.yaml)
- [X] Create CC extension registry (cc-component-registry.yaml)
- [X] Revise a-team-blueprint.md with visualizations and concise summaries
- [X] Update cc-global-config-schema.md with full extension list and rules/ behavior
- [X] Create system architecture Mermaid diagram
- [X] Resolve orchestration pattern: command (trigger) + skill (knowledge) + main session (execution)
- [X] Finalize agent definition template (v0.6.0: REQUIRED Verification section, updated frontmatter)
- [X] Finalize skill scaffold template (SKILL.md frontmatter + resource folders)
- [X] Finalize command definition template (frontmatter: description + allowed-tools)
- [X] Finalize rules file template (with optional `paths:` frontmatter)
- [X] Validate naming conventions against CC runtime behavior (validated through multi-session use)
- [X] Review/refine all artifacts for consistency (v0.8.0 QA/QC complete)
</details>

<details>
<summary>P0.5: v2.0 Orchestration Upgrade ✅</summary>

- [X] Create `orchestration-framework.md` — Canonical patterns, execution protocol, failure modes, cost model, delegation templates, state management, Tenet 6 (autonomous multi-agent)
- [X] Revise `multi-agent-collaboration.md` to v2.0 — Worktrees-first, Agent Teams, effort scaling, cross-session persistence
- [X] Create verifier agent (`agents/verifier.md`) with adversarial challenge patterns
- [X] Create orchestrator agent (`agents/orchestrator.md`) with PLAN→VERIFY→COMMIT enforcement
- [X] Create `skills/executing-tasks/SKILL.md` — Standard task execution protocol as model-invoked skill
- [X] Update agent template with Verification (REQUIRED) section
- [X] Update CLAUDE.md template — Hybrid: Role, Domain Guidelines, Constraints, Guardrails, Workflows, Verification, State Management, Extension Registry
- [X] Update global CLAUDE.md template (`templates/global/CLAUDE.md.template`)
- [X] Create settings.json template (permissions.allow, PostToolUse hook, `"agent": "orchestrator"`)
- [X] Update cc-component-registry.yaml (verifier agent, hooks, experimental section)
- [X] Update knowledge/INDEX.md (file counts, new entries, version bump to v0.8.0)
- [X] Update references.md — Anthropic articles + context engineering sources
- [X] Verify all cross-file links resolve correctly
- [X] Update root CLAUDE.md with orchestration references and new commands
- [X] Bump architecture guide version to 0.8.1
- [X] Add Agentic Workflow Patterns section to human-facing guide
- [X] Integrate Mermaid diagrams into guide
- [X] Add Cowork section (distribution + enterprise)
- [X] Add HEC-RAS Appendix C domain example
</details>

<details>
<summary>P0.5: Daily Utility Commands ✅ (Boris Cherny Tips)</summary>

- [X] Create `/commit-push-pr`, `/techdebt`, `/context-sync`, `/execute-task`, `/init-plugin`, `/init-worktree` commands
- [X] Add adversarial prompt examples to verifier agent
- [X] Add security routing hook pattern to hooks KB
- [X] Add cross-device/background/plan-mode to session-management KB
- [X] Add filesystem-as-context patterns to session-management KB
- [X] Add probabilistic acknowledgment to orchestration-framework KB
</details>

<details>
<summary>P-LIVE: Global Config Migration ✅</summary>

- [X] Audit, archive, rewrite global ~/.claude/ config
- [X] Deploy agents, commands, skills, settings.json
- [X] Test orchestrator routing, commands, token overhead
</details>

<details>
<summary>P-LIVE: Skill Expansion ✅</summary>

- [X] Create planning-implementation, assessing-quality, designing-workflows, visualizing-data skills
- [X] Broaden architecture-analyzer description
- [X] Verify all 8 skills load via /memory
</details>

<details>
<summary>P-LIVE: A-Team/Product-Design Integration ✅</summary>

- [X] Create reference/INDEX.md, update commands, update planning-implementation skill
</details>

<details>
<summary>P-LIVE: CAB Plugin Marketplace Test ✅</summary>

- [X] Publish, register, install, validate 14 commands + 4 agents + 5 skills
- [X] Test /validate and /integrate-existing on HEC-RAS
</details>

---

## Reference Artifacts

> Version is centralized in `.claude-plugin/plugin.json`.

| Artifact | Location | Status |
|----------|----------|--------|
| Implementation Plan | `~/.claude/plans/jazzy-skipping-petal.md` | Active |
| CC Docs Investigation | `notes/cc-docs-investigation-2026-04-04.md` | HITL-01 review |
| Techdebt v2 | `notes/techdebt-v2-2026-04-04.md` | HITL-01 review |
| Techdebt v1 (baseline) | `notes/techdebt-2026-04-03.md` | Reference |
| Global Extensions Map | `notes/global-extensions-map.md` | Active |
| Lessons Learned | `notes/lessons-learned.md` | Active |
| User's Original Comments | `notes/my-response-to-techdebt-2026-04-03.md` | Reference |
| Changelog Concept | `notes/changelog-system-design.md` | Concept |
| Orchestration Framework | `knowledge/operational-patterns/orchestration-framework.md` | Active |
| Multi-Agent Collaboration | `knowledge/operational-patterns/multi-agent-collaboration.md` | Active |
| Session Management | `knowledge/operational-patterns/session-management.md` | Active |
| Team Collaboration | `knowledge/operational-patterns/team-collaboration.md` | Active |
| Orchestrator Agent | `agents/orchestrator.md` | Active |
| Verifier Agent | `agents/verifier.md` | Active |
| Knowledge Index | `knowledge/INDEX.md` | Active |
| plugin.json | `.claude-plugin/plugin.json` | Active |
