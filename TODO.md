# CAB (cc-architecture-builder): Live Task Tracker

**Last Updated**: 2026-02-25

---

## Active Priority: Base Architecture Standardization

### P0: Finalize Schema & Naming (Current Sprint)

- [x] Define product design lifecycle phases and sub-processes
- [x] Define full A-team roster with CC component mapping
- [x] Define naming conventions for all CC component types
- [x] Define CC global config directory schema
- [x] Define orchestration framework concept
- [x] Verify `rules/` supports recursive subdirectories (confirmed YES)
- [x] Verify `skills/` does NOT support subdirectories (confirmed)
- [x] Create A-team roster as AI-digestible database (a-team-database.yaml)
- [x] Create CC component registry (cc-component-registry.yaml)
- [x] Revise a-team-blueprint.md with visualizations and concise summaries
- [x] Update cc-global-config-schema.md with full component list and rules/ behavior
- [x] Create system architecture Mermaid diagram
- [x] Resolve orchestration pattern: command (trigger) + skill (knowledge) + main session (execution)
- [x] Finalize agent definition template (.md frontmatter + body) — **v0.6.0: REQUIRED Verification section, updated frontmatter (skills, memory, permissionMode)**
- [ ] Finalize skill scaffold template (SKILL.md frontmatter + resource folders)
- [ ] Finalize command definition template
- [ ] Finalize rules file template (with optional `paths:` frontmatter)
- [ ] Validate naming conventions against CC runtime behavior
- [ ] Review/refine all 6 artifacts for consistency and completeness

### P0.5: v2.0 Orchestration Upgrade (NEW — Feb 2026)

- [x] Create `orchestration-framework.md` — Canonical patterns, execution protocol, failure modes, cost model, delegation templates, state management
- [x] Revise `multi-agent-collaboration.md` to v2.0 — Worktrees-first, Agent Teams, effort scaling, cross-session persistence
- [x] Insert Section 7.5 Agentic Workflow Patterns into architecture guide
- [x] Create verifier agent (`agents/verifier.md`)
- [x] Update agent template with Verification (REQUIRED) section
- [x] Update CLAUDE.md template (Learned Corrections, Verification commands)
- [x] Create settings.json template (permissions.allow, PostToolUse hook)
- [x] Add settings.json configuration section to cc-global-config-schema.md
- [x] Update cc-component-registry.yaml (verifier agent, post-tool-format hook, experimental section)
- [x] Update knowledge/INDEX.md (file counts, new entries, version bump)
- [x] Update references.md with new Anthropic source URLs
- [x] Bump architecture guide version to 0.6.0
- [ ] Sync CAB abbreviation across all files (audit for "cc-architecture-builder" mentions)
- [ ] Verify all cross-file links resolve correctly
- [ ] Update CLAUDE.md root file with orchestration references

### P1: Execute Migration

- [ ] Rename existing skill directories to new naming convention
- [ ] Create standardized scaffold (SKILL.md + scripts/ + references/ + assets/) for each skill
- [ ] Rename/restructure existing rules/ directory to dev/, comm/, gov/, process/
- [ ] Rename/restructure existing agents/ to new naming
- [ ] Normalize `reference/` vs `references/` across all skills
- [ ] Move domain-specific commands to project plugins
- [ ] Move `design-agent-pipeline.md` from rules/ to ai-design-agent skill

### P2: Template & Content Population

- [ ] Create deliverable templates (PRD, SRD, ADR, SOW) in skill `assets/`
- [ ] Create phase-gate checklists (machine-parseable YAML)
- [ ] Create agent definition files for new agents (software-architect, qa-lead, product-manager, codebase-manager, ux-designer, tech-writer, security-auditor, ux-researcher)
- [ ] Populate skill SKILL.md content for placeholder skills
- [ ] Create project-state.yaml schema for orchestration state management

### P3: Audit & Integration

- [ ] Audit all installed plugins for overlap with custom components
- [ ] Resolve agent naming collisions with plugin agents
- [ ] Audit `rules/` total token footprint and condense
- [ ] Audit `CLAUDE.md` and restructure to lean version with @imports
- [ ] Document CC platform priority/conflict resolution rules as educational reference
- [ ] Test all CC tools (commands, agents, skills) end-to-end

### P4: Advanced Orchestration & RAG

- [ ] Implement orchestrator pattern: init-project command + ai-design-agent skill
- [ ] Define multi-agent session management protocols (session chaining, worktree integration)
- [ ] Evaluate MCP-based RAG for knowledge bases exceeding ~100 files
- [ ] Implement team formation workflow reading a-team-database.yaml
- [ ] Test git worktree integration with multi-agent workflows
- [ ] Test Agent Teams (experimental) for inter-agent communication use cases

---

## Reference Artifacts

| Artifact | Location | Version | Status |
|---|---|---|---|
| Product Design Cycle | `docs/Claude_Project/00_architecture/product-design-cycle.md` | v0.1.0 | Draft |
| A-Team Blueprint | `docs/Claude_Project/00_architecture/a-team-blueprint.md` | v0.2.0 | Revised |
| A-Team Database | `docs/Claude_Project/00_architecture/a-team-database.yaml` | v0.2.0 | Active |
| CC Component Registry | `docs/Claude_Project/00_architecture/cc-component-registry.yaml` | v0.3.0 | Revised (v0.6.0) |
| CC Global Config Schema | `docs/Claude_Project/00_architecture/cc-global-config-schema.md` | v0.3.0 | Revised (v0.6.0) |
| Orchestration Framework | `knowledge/operational-patterns/orchestration-framework.md` | v2.0 | **NEW** (v0.6.0) |
| Multi-Agent Collaboration | `knowledge/operational-patterns/multi-agent-collaboration.md` | v2.0 | **Revised** (v0.6.0) |
| Architecture Guide | `docs/Claude_Project/00_architecture/claude_code_architecture_guide_human-facing.md` | v0.6.0 | Revised |
| Verifier Agent | `agents/verifier.md` | v1.0 | **NEW** (v0.6.0) |
| Agent Template | `templates/agent.template/agent.md.template` | v2.0 | Revised (v0.6.0) |
| CLAUDE.md Template | `templates/plugin/CLAUDE.md.template` | v2.0 | Revised (v0.6.0) |
| settings.json Template | `templates/plugin/settings.json.template` | v1.0 | **NEW** (v0.6.0) |
| Project Status | `docs/Claude_Project/project_status_20260128_v2.md` | -- | Active |
