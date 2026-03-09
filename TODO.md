# CAB (cc-architecture-builder): Live Task Tracker

**Last Updated**: 2026-03-09
**Plugin Version**: 0.8.1

---

## Completed: Base Architecture Standardization

### P0: Schema & Naming ✅

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

### P0.5: v2.0 Orchestration Upgrade ✅

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
- [X] Update references.md — Anthropic articles + context engineering sources (Koylan, Watts, Fowler/Böckeler, High Agency)
- [X] Verify all cross-file links resolve correctly
- [X] Update root CLAUDE.md with orchestration references and new commands
- [X] Bump architecture guide version to 0.8.1
- [X] Add Agentic Workflow Patterns section to human-facing guide
- [X] Integrate Mermaid diagrams into guide (Runtime Layers, Decision Tree, Token Budget, Two-Schema, Agent Spawn, Skill vs Agent)
- [X] Add Cowork section (distribution + enterprise)
- [X] Add HEC-RAS Appendix C domain example

### P0.5: Daily Utility Commands ✅ (Boris Cherny Tips)

- [X] Create `/commit-push-pr` command
- [X] Create `/techdebt` command
- [X] Create `/context-sync` command
- [X] Create `/execute-task` command
- [X] Create `/init-plugin` command
- [X] Create `/init-worktree` command
- [X] Add adversarial prompt examples to verifier agent
- [X] Add security routing hook pattern to hooks KB
- [X] Add cross-device/background/plan-mode to session-management KB
- [X] Add "Analysis Sandbox" pattern to init-worktree command
- [X] Add context health decision framework (continue/compact/fresh) to session-management KB
- [X] Add filesystem-as-context patterns to session-management KB
- [X] Add probabilistic acknowledgment to orchestration-framework KB

---

## Active: In-The-Wild Testing

### P-LIVE: Global Config Migration

- [X] **Audit current ~/.claude/** — DONE (findings documented 2026-03-09)
- [X] Archive old config to `~/.claude/_archive/` (CLAUDE-old.md, rules-old/, skills-old/, agents readme, old hooks, old commands)
- [X] Write rules files: dev/philosophy, dev/practices, dev/token-efficiency, dev/comments, dev/ai-system-design, comm/interaction, process/analysis-framework
- [X] Write new CLAUDE.md — Master Strategist & Multi-Agent Orchestrator hybrid template
- [X] Deploy agents: orchestrator, verifier, general-researcher, code-reviewer, debugger-specialist
- [X] Deploy commands: commit-push-pr, execute-task, context-sync, techdebt, init-plugin, init-worktree
- [X] Retain 4 universal skills: architecture-analyzer, claude-docs-helper, readme-generator, token-optimizer
- [X] Update settings.json: "agent": "orchestrator", PostToolUse hooks, plugin trimming (8 enabled, rest disabled)
- [X] Archive 11 empty/placeholder skill directories
- [X] Test: run `claude` and verify `/memory` shows correct load
- [ ] Test: verify orchestrator agent receives tasks by default
- [ ] Test: verify /commit-push-pr, /execute-task, /context-sync work
- [ ] Measure baseline token overhead (target: ~6-8K tokens)

### P-LIVE: Global Config — Skill Expansion (CURRENT)

- [X] Create `planning-implementation/` skill with SOW + implementation plan templates (assets/sow-template.md, assets/implementation-plan-template.md)
- [X] Create `assessing-quality/` skill for testing strategy and quality frameworks
- [X] Create `designing-workflows/` skill for process/pipeline design and automation assessment
- [X] Create `visualizing-data/` skill for visual communication (Yau+Cleveland/McGill+Munzner hybrid, Mermaid patterns, ASCII, encoding hierarchy)
- [X] Broaden `architecture-analyzer` description to include new system design (full-stack, language-agnostic)
- [X] Verify all 8 skills load correctly via `/memory`

### P-LIVE: CAB Plugin Marketplace Test

- [ ] Publish CAB plugin to GitHub (private): `gh repo create cc-architecture-builder --private --source=. --push`
- [ ] Register marketplace: `claude /plugin marketplace add https://github.com/[user]/cc-architecture-builder`
- [ ] Install: `claude /plugin install cc-architecture-builder@[user]`
- [ ] Validate all 14 commands, 4 agents, 5 skills load via `/memory`
- [ ] Test `/validate` in CAB repo itself
- [ ] Test `/integrate-existing` on HEC-RAS project (primary use case)

### P-LIVE: HEC-RAS Project Integration Test

- [ ] Use `/integrate-existing` to auto-discover HEC-RAS codebase and scaffold CC overlay
- [ ] Create domain agents (geometry-specialist, hydraulic-analyst, results-processor, qa-reviewer)
- [ ] Create domain skills (preprocessing-terrain, calibrating-model, delineating-floodplain)
- [ ] Create domain commands (run-simulation, extract-results, check-convergence)
- [ ] Create domain rules (engineering-standards, ras-conventions, data-handling)
- [ ] Create domain knowledge base (ras-fundamentals/, standards/, calibration/, reference/)
- [ ] Configure MCP wrapping for RASCommander
- [ ] Test multi-agent orchestration: orchestrator → domain specialist → verifier
- [ ] Evaluate RAG need based on KB file count

---

## Deferred

### P2: Template & Content Population (deferred to post-P-LIVE)

- [ ] Create deliverable templates (PRD, SRD, ADR, SOW) in skill `assets/` — project-specific, do per-project
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

## Reference Artifacts

| Artifact                          | Location                                                              | Version | Status                 |
| --------------------------------- | --------------------------------------------------------------------- | ------- | ---------------------- |
| Architecture Guide (human-facing) | `docs/` (to be moved outside plugin)                                | v0.8.1  | Active                 |
| Orchestration Framework           | `knowledge/operational-patterns/orchestration-framework.md`         | v2.0+   | Active                 |
| Multi-Agent Collaboration         | `knowledge/operational-patterns/multi-agent-collaboration.md`       | v2.0    | Active                 |
| Session Management                | `knowledge/operational-patterns/session-management.md`              | v2.0    | Active                 |
| Orchestrator Agent                | `agents/orchestrator.md`                                            | v1.0    | **NEW** (v0.8.0) |
| Verifier Agent                    | `agents/verifier.md`                                                | v1.1    | Revised (v0.8.1)       |
| Executing Tasks Skill             | `skills/executing-tasks/SKILL.md`                                   | v1.0    | **NEW** (v0.8.0) |
| CLAUDE.md Template (plugin)       | `templates/plugin/CLAUDE.md.template`                               | v3.0    | Revised (v0.8.0)       |
| CLAUDE.md Template (global)       | `templates/global/CLAUDE.md.template`                               | v1.0    | **NEW** (v0.8.0) |
| settings.json Template            | `templates/plugin/settings.json.template`                           | v2.0    | Revised (v0.8.0)       |
| Cowork KB                         | `knowledge/distribution/cowork.md`                                  | v1.0    | **NEW** (v0.8.0) |
| Knowledge Index                   | `knowledge/INDEX.md`                                                | v0.8.0  | Active                 |
| plugin.json                       | `.claude-plugin/plugin.json`                                        | v0.8.0  | Active                 |
| Global Config Schema              | `docs/00_architecture/cc-config-example/cc-global-config-schema.md` | v0.2.0  | Needs update to v0.8.0 |
| Component Registry                | `docs/00_architecture/cc-config-example/cc-component-registry.yaml` | v0.2.0  | Needs update to v0.8.0 |
| Boris Cherny Tips                 | Project Knowledge:`Cherny-Boris-cc-tips_2026.md`                    | —      | Reference              |
