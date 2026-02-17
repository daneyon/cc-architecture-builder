# cc-architecture-builder: Live Task Tracker

**Last Updated**: 2026-02-15

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
- [ ] Finalize skill scaffold template (SKILL.md frontmatter + resource folders)
- [ ] Finalize agent definition template (.md frontmatter + body)
- [ ] Finalize command definition template
- [ ] Finalize rules file template (with optional `paths:` frontmatter)
- [ ] Validate naming conventions against CC runtime behavior
- [ ] Review/refine all 6 artifacts for consistency and completeness

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

---

## Reference Artifacts

| Artifact | Location | Version | Status |
|---|---|---|---|
| Product Design Cycle | `docs/Claude_Project/00_architecture/product-design-cycle.md` | v0.1.0 | Draft |
| A-Team Blueprint | `docs/Claude_Project/00_architecture/a-team-blueprint.md` | v0.2.0 | Revised |
| A-Team Database | `docs/Claude_Project/00_architecture/a-team-database.yaml` | v0.2.0 | NEW |
| CC Component Registry | `docs/Claude_Project/00_architecture/cc-component-registry.yaml` | v0.2.0 | NEW |
| CC Global Config Schema | `docs/Claude_Project/00_architecture/cc-global-config-schema.md` | v0.2.0 | Revised |
| Orchestration Framework | `docs/Claude_Project/00_architecture/orchestration-framework.md` | v0.1.0 | Draft |
| Project Status | `docs/Claude_Project/project_status_20260128_v2.md` | -- | Active |
