# CAB (cc-architecture-builder): Live Task Tracker

**Last Updated**: 2026-04-29 (Session 40 — Wave 8 Phase 2B' subtasks 1-3 complete; 4-8 pending)
**Plugin Version**: (now commit-hash keyed; no semver field — matches official plugin-dev pattern)
**Active Implementation Plans**:
- `notes/impl-plan-commands-skills-migration-2026-04-24.md` (UXL-002; Phase 3d gated on UX)
- `notes/impl-plan-kb-to-kg-2026-04-28-v2.md` (UXL-005; Phase 2A ✓ + 2B' subtasks 1-3 ✓; subtasks 4-8 next; v1 plan archived `_archive/impl-plan-kb-to-kg-2026-04-24.md`)
**Active Task**: Wave 8 Phase 2B' subtasks 4-8 (author llm-interaction-patterns card + codify temporal-neutrality rule + cross-refs + INDEX update + plan-implementation skill enrichment) — see `notes/current-task.md`

---

## Top Priorities (post Session 34)

### COMPLETED Session 34

- [X] **CLAUDE.md restructure** — template-informed, attention-optimized rewrite of both project CLAUDE.md (`2de116d`, 242→189 lines) and global `~/.claude/CLAUDE.md` (152→138 lines, not in git). Added Identity, Operating Philosophy, Anti-Patterns. Removed redundant auto-load content. Resolved bootstrap protocol conflict. Three-layer complement model formalized.

### COMPLETED Session 33

- [X] **HydroCast audit P1 close** — closed `claudemd.no_knowledge_index_ref` + 2 of 3 `knowledge.missing_frontmatter` WARN findings (3rd obviated via `_archive/` relocation). HydroCast commit `0c2d1c1`. Feat branch `feat/plugin-first-migration-2026-04-09` pushed, PR #8 opened: https://github.com/daneyon/Flood-Forecasting/pull/8. 4 persistent WARN items deferred to next full audit per user directive.

### COMPLETED Session 32

- [X] **Bootstrap Token Efficiency Restoration** — landed across Sessions 28-32. Final cost ~7,169 tokens (~82.5% reduction from 41,081 baseline; beats <10K stretch target). All 5 phases complete: P1 `8dfef75`, P2 `836f3aa`, P3 `731bea0`, P4 `30ae350`, P5 `572988e`. See `notes/impl-plan-bootstrap-efficiency-2026-04-11.md` + LL-29 in `notes/lessons-learned.md`.

### P0 — Active / Next candidates

- [ ] **HydroCast Phase D strategic comparison** (ACTIVE-P0, gated on PR #8 merge) — read-only comparison of CAB post-Session-32 3-file cascade vs HydroCast LC-08 3-layer hierarchy. Multi-agent fan-out (`general-researcher` + `cab:architecture-advisor`). Deliverable: `Flood-Forecasting/notes/cab-vs-hydrocast-state-mgmt-comparison-2026-04-11.md`. See `notes/current-task.md` for full scope + key questions + execution strategy.
- [ ] **LL-19 / LL-20 protocol counter** (ACTIVE-P0 in lessons-learned.md) — sycophantic-agreement-with-persistence-gaps recurrence pattern needs structural counter. Currently meta-lesson without enforcement layer.
- [ ] **LL-28 event-triggered dialogue-checkpoint protocol** (ACTIVE-P0) — implementation of the Session 27 candidate. **New data point from Session 33**: the HydroCast audit workstream itself was a LL-28 case study (state gap across ~4 weeks; dialogue-level discovery never persisted; parallel session auto-switched to feat branch unknowingly). Strong validation dataset for the checkpoint protocol design. Pre-requisite per Session 27 directive: at least one survived dying-session recovery test before hard-coding.

### P1 — High value, integrate this quarter

- [ ] **LL-02 / LL-12 background-write gate** (ACTIVE-P1) — pre-delegation hook detecting `run_in_background: true` + Write/Edit/NotebookEdit tool intent. Recurring failure mode since LL-02 first logged.
- [ ] **LL-08 background-output persistence verification** (ACTIVE-P1) — post-agent step that checks for expected artifact files before treating output as authoritative.
- [ ] **LL-17 worktree auto-detect** (ACTIVE-P1) — pre-commit branch context verification + worktree suggestion when concurrent-session risk detected. KB exists; programmatic surface does not.
- [ ] **LL-27 follow-on: extend `/sync-check`** for plugin↔global agent name-collision detection — highest-priority LL-27 enforcement layer (currently manual).
- [ ] **Global CLAUDE.md v2 architecture upgrade** (Session 27 origin) — re-evaluate ~200-line global memory budget after Phase D comparison.
- [ ] **Wave 9: Notes ↔ Knowledge linking implementation** (deferred from Wave 8 by scenario-analyst stress-test, Session 39) — `knowledge_refs:` frontmatter field + scanner. Wave 8 Phase 2F schema anticipates the `notes-artifact` edge type but does not implement field/scanner until repacking pressure validates the schema. Unblocked at Wave 8 completion.
- [ ] **Wave 12+: Protocol-role subagent constellation** (strategic intent captured Session 40, 2026-04-29) — design + build planner / reviewer / executor / committer subagents to complement existing verifier; align with A-team × full-stack product-design-cycle × CC extensions. Sequencing prerequisites: (1) Wave 8 KG functional, (2) Waves 9-11 skill repacking complete. See `notes/end-vision-cab-2026-04-28.md` § "Strategic Intent: Protocol-Role Subagent Constellation". Pre-Wave-12 work should preserve optionality (e.g., 2D' tail audit MUST NOT auto-DELETE `knowledge/reference/` advisory cards — they're fuel for constellation realization).

### P2 — Nice to have

- [ ] **LL-10 fresh-fetch pre-edit hook** (ACTIVE-P2) — pre-edit gate on KB files referencing official CC docs.
- [ ] **LL-25 RAS-exec / HydroCast policy propagation** — documentation alignment.
- [ ] **LL-25 CC Memory Layer Alignment KB card** — currently summarized in `filesystem-patterns.md`; may warrant dedicated reference.
- [ ] **LL-25 Dream consolidation skill concept** — mimics CC Layer 6 (Dreaming) for LL → CLAUDE.md promotion workflow.
- [ ] LL-27 follow-ons: KB card `multi-agent/agent-resolution.md`, `/validate --cab-audit` shadow-check, "CAB provides" notes in CAB's own extension registry.

---

<!-- T1:BOUNDARY — partial-read at `Read(TODO.md, limit=80)` captures Top Priorities section above this marker; everything below is backlog / deferred / archive and loads on-demand only. -->

## Active — Immediate

### Plugin-First Architecture Correction (Sessions 16-18+)

- [X] Phase 1: Audit skill R2 — plugin-architecture-aware criteria (commit `d8c0456`)
- [X] Phase 2: CAB structural migration — un-nest to root + 23 cross-ref updates (commit `01cfa2e`)
- [X] Phase 3: R2 self-audit — DEVELOPING 48%, 24 findings, 4/4 AC PASS (Session 18)
- [X] **Phase 3R: CAB R2 Remediation** (Session 19 — 5 tiers, 20/20 AC PASS)
- [X] **Re-audit**: DEVELOPING 62% (13/21), +3 pts / +14pp, 0 ERROR (Session 20)
- [X] Phase 4: RAS-exec migration + R2 audit — ALIGNED 81% (17/21), PR #2 (Session 20)
- [X] **BLOCKER RESOLVED + LL-22**: RAS-exec settings.json 3 structural errors fixed (Session 21)
- [X] **BLOCKER FULLY RESOLVED + LL-23**: RAS-exec extensions still invisible after settings fix → deeper root cause: CC plugin discovery requires explicit registration (`enabledPlugins` + `extraKnownMarketplaces`). Root-level components (plugin convention) are ONLY scanned for enabled plugins, NOT for local standalone use. Fixed: cleaned plugin.json schema, registered `ras-exec@ras-exec` globally, merged feat→main, pushed. Also loosened global settings.json deny rules (Edit/Write → prompt instead of block). (Session 22)
- [~] Phase 5: HydroCast — migration done, R2 audit done (71%), marketplace registered (Session 23)
- [X] Phase 5 P-MKT: marketplace.json created, plugin.json cleaned, global registration + marketplace clone — committed `4a93eaa` (Session 23)
- [X] Phase 5 P0: permissionMode removed from 9 agents + CLAUDE.md diagram updated — committed `711df77` (Session 23)
- [X] Phase 5 P0.5: settings.json structural fixes (sandbox nesting, stale entries) — committed `711df77` (Session 23)
- [X] **State management git-tracking reform (LL-25)** — Session 24 ✅. `.gitignore` updated, `filesystem-patterns.md` rewritten with Git Tracking Policy + CC Memory Layer Alignment + Lessons-Referenced Protocols sections, `git-foundation.md` updated, `worktree-workflows.md` references LL-25, CAB CLAUDE.md updated, template updated, new `pre-push-state-review` skill + hook scaffold created, 28 `notes/` files now tracked. All 10 ACs PASS.
- [X] **LL-25 follow-on: Pre-push hook regex refinement** — RESOLVED in `62bf4a9` (Session 26, Phase A.5). Draft markers now require label format (colon-suffix) eliminating prose false-positives. Anchored regex also added for tense markers (LL-26). Folded into tense hygiene protocol work.
- [ ] **LL-26 follow-on: Backtick-wrapped marker exclusion** — Current anchored regex still matches draft labels inside markdown code spans (e.g., documentation files discussing the markers trigger the hook). POSIX ERE lacks negative lookbehind; options: (a) second-pass `grep -v` filter for backtick-wrapped matches, (b) documentation opt-out marker, (c) awk-based pre-filter. Low priority — primary LL-26 failure mode (stale status lines) is cleanly handled.
- [ ] **LL-27 follow-on: Extend `/sync-check` for plugin↔global name-collision detection** — Current sync-check detects file differences but not the precedence-shadow case where both files exist with the same agent name. Add agent-name-collision scan between `~/.claude/agents/*.md` and all enabled plugins' `agents/*.md`. Emit WARN for collisions regardless of content delta. Highest-priority LL-27 enforcement layer.
- [ ] **LL-27 follow-on: New KB card `knowledge/operational-patterns/multi-agent/agent-resolution.md`** — Document the local → user → plugin precedence order explicitly, shadowing failure mode, detection patterns, corrective patterns. Currently implicit across multiple LLs.
- [ ] **LL-27 follow-on: Add shadow-check to `/validate --cab-audit` methodology** — Audit skill should enumerate all plugin agents and check for any same-named file at higher-precedence layers. Fold into the agent dimension scoring.
- [ ] **LL-27 follow-on: Update global `~/.claude/CLAUDE.md` Extension Registry** — Add explicit "CAB provides this — do not create a global copy" notes to `orchestrator` and `verifier` entries. Prevents future recreation of the shadow copy from operator confusion (the exact pattern that caused this incident).
- [ ] **LL-27 follow-on: Add "CAB provides" notes to CAB's own extension registry** — Mirror the above note inside CAB's CLAUDE.md so that operators reading CAB docs immediately know global copies are contraindicated.
- [ ] **LL-28 follow-on: Design event-triggered state write protocol** — Complement LL-26's phase-triggered writes. Candidate trigger events: (a) new architectural insight, (b) HITL decision point (write pending question + options before asking user), (c) investigation finding contradicting/updating prior LL/DD, (d) discovery implying new LL entry. Implementation sketch: add "dialogue checkpoint" step to `execute-task` — append 5-10 line "dialogue state" block to `progress.md` after analytical turns >N tokens OR HITL questions. Cost ~200-400 tokens/checkpoint. **Not to be hard-coded** — tag as CANDIDATE until it survives at least one real dying-session recovery test (per Session 27 user directive on iterative optimization).
- [ ] **LL-28 follow-on: Fallback recovery protocol for mid-dialogue death** — Codify the Session 27 recovery method as a reusable skill or playbook: (1) bootstrap from `notes/` first, (2) identify dying-session JSONL transcript, (3) extract last N turns, (4) synthesize coverage gap, (5) backfill discoveries into new LL entries + state files, (6) resume at the exact HITL question. Deliverable: either a new `skills/recover-from-dying-session/` skill or a new subsection in `filesystem-patterns.md`. Input to the design: Session 27 itself is a working example — use its transcript as validation dataset.
- [ ] **LL-28 follow-on: Bootstrap token cost tracking** — Per user directive (Session 27), every new protocol layer expands the cold-anchor cost. Add a standing measurement: record `bootstrap_tokens` consumed at Session start in `progress.md` header. Set a soft budget ceiling (e.g., 15% of context window) beyond which bootstrap optimization takes priority over new protocol additions. Starting data point: Session 27 bootstrap + investigation + LL drafting consumed ~70K tokens before answering the actual pending question; remaining budget 22% at state-refresh time.
- [ ] **LL-28 follow-on: Reversibility inventory** — Per user directive, every state-mgmt protocol addition must be individually revertable. Maintain an inventory table in `filesystem-patterns.md` mapping protocol → commit hash → revert command. LL-25 = `302f872`, LL-26 = `62bf4a9`, LL-27 = `436ffbd`, LL-28 candidate = TBD. This makes rollback a one-liner if any layer proves counterproductive.
- [ ] **LL-25 follow-on: RAS-exec policy propagation** — Apply tracked-notes policy to RAS-exec plugin (documentation update + verify `.gitignore` alignment). Low risk, already tracking notes on feat branches.
- [ ] **LL-25 follow-on: HydroCast policy propagation** — Same as RAS-exec. HydroCast already tracks notes on feat branches; just needs documentation alignment.
- [ ] **LL-25 follow-on: CC Memory Layer Alignment deep dive** — Potential new KB card `knowledge/operational-patterns/state-management/cc-memory-layer-alignment.md` covering the full 7-layer ↔ CAB mapping. Currently summarized in filesystem-patterns.md; may warrant dedicated reference.
- [ ] **LL-25 follow-on: Dream consolidation skill concept** — Potential skill mimicking CC Layer 6 (Dreaming) for `lessons-learned.md` → CLAUDE.md promotion workflow. Would formalize the "lessons-referenced protocols" pattern.
- [ ] Phase 5 P1: KB frontmatter (3 files) + knowledge/INDEX.md reference
- [ ] Follow-on: KB consistency pass (connected to LL-19)
- [ ] **CAB Enhancement (LL-24)**: Update audit skill + validate command + KB + templates to check marketplace.json presence

### Global CLAUDE.md v2 Architecture Upgrade (QUEUED — execute after Phase D HydroCast comparison, before HITL-4)

**Origin**: Session 27 post-compaction dialogue (2026-04-11). User asked whether the current global `~/.claude/CLAUDE.md` — freshly updated this session with the Extension Registry + LL-27 shadowing warnings — is actually the optimal master-strategist configuration, or whether the "Extension Registry" section is redundant accretion that wastes the ~200-line global-memory budget.

**Diagnosis (recorded for cold-start resume)**:

The global CLAUDE.md currently mixes four distinct content types that should be separated:

| Content type | Example | Ideal location | Current location | Drift risk |
|---|---|---|---|---|
| **Identity** (persona, values, role) | "Master strategist, no sycophancy" | CLAUDE.md | ✅ CLAUDE.md | None |
| **Framework** (heuristics, protocols) | "PLAN → REVIEW → EXECUTE → VERIFY → COMMIT" | CLAUDE.md or rules/ | ✅ CLAUDE.md | None |
| **Policy** (do/don't rules) | "Never create shadowed agent files" | rules/ (auto-loaded cascade) | ❌ CLAUDE.md Extension Registry | Low |
| **Inventory** (what exists) | "Agents: code-reviewer, debugger-specialist..." | Runtime — *never* hand-maintained | ❌ CLAUDE.md Extension Registry | **HIGH** (this is the category error that caused LL-27) |

**What's actually double-loaded**: agent/skill/command names + counts, rules list, plugin ecosystem list, output styles pointer, agent memory pointer. All of these are already injected by CC runtime at session start (visible in the system prompt's "Available Skills" and plugin description blocks). The only **unique, load-bearing content** in the Extension Registry is the LL-27 shadowing warnings + the permanent policy rule — both of which are *policy*, not inventory.

**Budget math**: Extension Registry consumes ~30 lines of a ~200-line budget (15%). Runtime already provides all inventory content. Deleting the registry returns 15% of budget to identity/philosophy/orchestration content.

**Proposal**:

1. **Delete** the Extension Registry section entirely (lines ~125-148 of current `~/.claude/CLAUDE.md`).
2. **Replace** with a compact "Plugin Hygiene Policy" block — 5-6 lines maximum, pure policy: "Before creating global `~/.claude/{agents,skills,commands}/*.md` files that collide with plugin-provided names, check plugin ownership (LL-27 shadowing risk). Identity/persona lives here; behavioral definitions live in plugins. Runtime lists actual extensions — don't mirror that state here."
3. **Optional**: Move the LL-27 shadowing rule to a new `~/.claude/rules/meta/plugin-hygiene.md` file for auto-enforcement via the rules cascade (more durable; rules cascade is a non-shadowable layer).
4. **Reinvest** the freed ~25 lines into one of:
   - Sharper orchestration heuristics (when to fan-out, when not to, anti-patterns)
   - Multi-disciplinary lens application policy (currently in `rules/process/analysis-framework.md` but the 80/20 weighting trigger isn't codified)
   - Behavioral invariants like the LL-29 candidate ("quality-over-tokens") — invariants that shape trade-offs under context pressure

**Architectural framing** (this is the deeper point, not just a token optimization):

The thing that shadowed the orchestrator in LL-27 was partly the same failure mode as hand-maintaining an inventory that diverges from filesystem reality. Fixing the Extension Registry isn't just optimization — it's correcting a category error that LL-27 itself exposed. The registry mixed Policy (shadowing warnings) with Inventory (file listings). Separating them cleanly is a structural correction.

**Candidate LL-30 (proc)**: "Hand-maintained inventories in global memory are anti-patterns because they duplicate runtime-provided state and drift." Candidate until this upgrade is executed and validated.

**Execution plan** (pre-drafted for cold-start resume):

- Phase G.1: Draft `~/.claude/CLAUDE.md` v2 side-by-side with v1, showing the removed Extension Registry and the compact Plugin Hygiene Policy replacement
- Phase G.2: Draft the reinvestment content (pick one of the 3 options above, or all three compactly)
- Phase G.3: HITL gate — user reviews v2 diff before replacing v1
- Phase G.4: Replace v1 → v2 in a dedicated commit (or branch) for easy revert
- Phase G.5: Optionally create `~/.claude/rules/meta/plugin-hygiene.md` if shadowing rule should be fully extracted
- Phase G.6: Record outcome + drop LL-30 candidate → confirmed LL if the budget reinvestment proves valuable in practice

**Why queued behind Phase D, not before**: User directive Session 27 — "queue this behind phase D that already have plans to not make you side-track again." Phase D is the next committed work. The CLAUDE.md v2 upgrade is architecturally upstream of HydroCast harmonization (which will reference CAB patterns), so the right insertion is between Phase D (comparison, read-only, doesn't need CLAUDE.md v2) and Phase E (remediation, which benefits from the updated global architecture).

**Why not before Phase D**: Phase D is a read-only comparison — CLAUDE.md v2 doesn't change what the comparison reveals. Starting with Phase D keeps the original session's momentum and avoids turning a comparison task into a CLAUDE.md rewrite task.

**Reference**: Full Session 27 dialogue captured in `notes/progress.md` Session 27 Post-Compaction Addendum. Diagnosis table + 4-column classification + architectural framing all preserved there.

### CAB R2 Remediation — Prioritized Checklist

Source: `notes/cab-audit-2026-04-09.md` (24 findings). Sequenced by impact on global orchestrator and plugin consumers.

**Tier R1: Agent Frontmatter Fixes** (affects all CAB consumers immediately)

- [X] Remove `context:` from 3 agents (architecture-advisor, orchestrator, project-integrator) — invalid field, silently ignored (LL-15)
- [X] Remove `disallowedTools:` from verifier agent — not a valid CC field
- [X] Remove `permissionMode:` from all 4 agents — plugin-restricted field

**Tier R2: CLAUDE.md Enhancements** (extension discovery + orchestrator effectiveness)

- [X] Add extension registry table (4 agents, 9 skills, 15 commands)
- [X] Add domain guidelines section
- [X] Add verification commands section
- [X] Add learned corrections section (stub → `notes/lessons-learned.md`)

**Tier R3: Skill Frontmatter Hardening** (truncation fix + tool scoping)

- [X] Shorten all 9 skill descriptions to ≤250 chars (currently 322-553)
- [X] Add `allowed-tools:` to 7 unscoped skills
- [X] Add `effort:` to 6 skills without it

**Tier R4: Settings & Plugin Distribution**

- [X] Create root `settings.json` with `{ "agent": "orchestrator" }`
- [X] Expand `.claude/settings.json` deny list (destructive git ops, shell escape)
- [X] Add sensitive path protection deny rules

**Tier R5: Project Rules**

- [X] Create `.claude/rules/` with project-scoped rules (code-style, security, domain conventions)

### Post-Remediation

- [ ] Version bump to v1.1.1 + deploy to global
- [ ] PA-01 implementation (52 findings, 6-phase plan, `notes/pa-01-global-config-audit-2026-04-06.md`) — awaiting user review + approval

### CAB Extension Improvements (LL-24 — marketplace.json awareness)

Source: Sessions 21-23 marketplace discovery investigation. CAB extensions must prevent this from recurring.

- [ ] **Audit skill**: Add `marketplace.json` presence check to plugin validation criteria (alongside plugin.json)
- [ ] **Audit skill**: Add `plugin.json` schema validation — flag non-standard fields (`cabVersion`, `domain`, `stage`, etc.)
- [ ] **Validate command**: Check marketplace.json when `project_type: plugin`
- [ ] **KB update**: Update `knowledge/distribution/` with marketplace.json requirement + full discovery chain documentation
- [ ] **Templates**: Add `marketplace.json` template to `templates/plugin/`
- [ ] **Init-plugin command**: Auto-create marketplace.json during plugin scaffolding
- [ ] **Creating-components skill**: Include marketplace.json in plugin scaffolding checklist
- [ ] **CLAUDE.md guidelines**: Add principle — defer basic CC setup/config guidance to official `plugin-dev` plugin; CAB focuses on domain-specialized architecture + operational protocols
- [ ] **Global config principle**: `extraKnownMarketplaces` reserved for cross-domain, globally-useful plugins only. Project-specific plugins use marketplace clone + `enabledPlugins` without `extraKnownMarketplaces` entry

---

## Active — R2 Deferred Findings (revisit post-remediation)

Lower-priority audit findings — quality improvements, not blocking operation.

- [ ] Split 6 oversized KB files (target ≤300 lines): hooks.md, marketplace.md, team-collaboration.md, product-design-cycle.md, cc-architecture-diagrams.md, global-user-config.md
- [ ] Update `knowledge/INDEX.md` `last_updated` date (currently 2026-04-05)
- [ ] Add `memory: user` to orchestrator and architecture-advisor agents
- [ ] Condense CLAUDE.md workflow diagrams to seed-style summaries + @import
- [ ] Add hooks configuration (SessionStart bootstrap, PreToolUse security gate) — needs design
- [ ] Add sandbox configuration to `.claude/settings.json`
- [ ] Add `## See Also` KB cross-references to 8 skills
- [ ] Add `agent: true` to multi-step investigation skills (execute-task, scaffold-project, close-session, plan-implementation, validate-structure)

---

## Active — Post-Audit Deep Dives

### Operational Enhancements

- [ ] Deep dive: state management mechanisms strategy (changelog system, programmatic lesson aggregation)
- [ ] Deep dive: standardized audit/freshness-check CC extensions (agentic protocol)
- [ ] User's external plugin reviews + potential synthesis into custom extensions
- [ ] Collect external references for state management + orchestration (user queued reminder)
- [ ] State management standardization ideas — evaluate after full audit patterns visible (user queued reminder)
- [ ] Validate existing project (e.g., HEC-RAS) with latest CAB protocols end-to-end (user queued reminder)
- [ ] deep dive: have statistical/pattern/trend analyses as additional optional/advanced verification, as part of post-eval (in addition to standalone scoring/risk classification system e.g. see 'audit-workspace' skill classification)

### Strategic — Global Orchestrator Specialization

- [ ] Strategize standardized "presets": full profile of master global orchestrator + optimally recommended domain-specialized CC extensions. Goal: holistically effective, reusable orchestrator config templates for different user archetypes/workflows (user queued 2026-04-07)
- [ ] Deep dive: `output-styles/` — strategize and populate holistically standardized, effectively generalized output styles fitting the "master strategist" global orchestrator domain-specialization (user queued 2026-04-07)
- [ ] Deep dive: `agent-memory/` — strategize and populate standardized persistent memory patterns for the global orchestrator and domain-specialist agents;  (user queued 2026-04-07)

### Strategic — CAB System Architecture

- [ ] deep dive: strategize to enhance CAB KB system design via programmatic knowledge graph architecture; sample reference (one of many) - https://www.linkedin.com/feed/update/urn:li:activity:7443676633221447680?updateEntityUrn=urn%3Ali%3Afs_updateV2%3A%28urn%3Ali%3Aactivity%3A7443676633221447680%2CFEED_DETAIL%2CEMPTY%2CDEFAULT%2Cfalse%29  (user queued 2026-04-08)
- [ ] deep dive: strategize to enhance CAB to have visualization programmatic/agentic capabilities as one of the domain specializations + design philosophy to focus on dynamic, iterative, interactive visual learning/context engineering styles (user queued 2026-04-08)
- [ ] deep dive: strategize to further explore about a potential idea of "female/male" dual system design philosophy approach where the frameworks/protocols designed here must programmatically be linked from the other side (i.e. project w/ cc-integration via CAB, that may have further questions or interest/needs to iteratively coordinate with the CAB advisory agent(s)/invokable extensions to ensure project stays aligned and maximizes to leverage the readily actionable, available CAB architectural/orchestrative capabilities/tools for most practically standardized/consistent context engineering)). Need CAB design philosophies to be more effectively programmatically transferred over to the cc-integrated project platform (codebase + cc hub) by CAB's extensions (creating + validate) (user queued 2026-04-08)
- [ ] deep dive: strategize to enhance applicable existing or create new CC agent/skill that serves as a seasoned, senior software eng that is fully/persistently context-aware of proper battle-tested, best industry recommended practices for data governance of large, comprehensive agentic OS platform project like hydrocast (Desktop\Automoto\Flood-Forecasting), with multiple standardized, systematically programmatic databases, external connectors (via api/mcp), complex knowledge graph of multiple modules all supposed to be architecturally interacting adequately as overall system process flow framing.(user queued 2026-04-08)

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

### P5: CC Trajectory Anticipation (deferred — revisit post-audit)

- [ ] Deep review of unreleased/gated CC capabilities and architectural implications
- [ ] Enhance CAB orchestration patterns to anticipate autonomous background agents
- [ ] Shift CLAUDE.md guidance toward seed instructions that survive autonomous memory consolidation
- [ ] Design backend-agnostic orchestration patterns resilient to IPC mechanism changes
- [ ] Anticipate increasingly granular permission models in plugin manifest design

---

## Completed Archive

<details>
<summary>Comprehensive CAB Self-Audit v1.0.0 → v1.1.0 ✅ (T1-T5, 2026-04-05)</summary>

### HITL-01: User Review of Pre-Audit Artifacts ✅

- [X] User review: `notes/cc-docs-investigation-2026-04-04.md` (72 delta items, 11 categories)
- [X] User review: `notes/techdebt-v2-2026-04-04.md` (56 items, 5-tier plan)
- [X] User approval to begin T1 implementation (approved 2026-04-05 with 9 directives)

### HITL-02: External Reference Investigation ✅

- [X] User provides external reference document (3 sources: X posts + TheNewStack article)
- [X] Deep investigation research + comparison report → `notes/techdebt-v3-2026-04-04.md`
- [X] User review + approval of techdebt v3 (approved 2026-04-05)
- [X] v2 + v3 merged into unified implementation plan → `notes/current-task.md`

### T1: Architectural Alignment ✅ (2026-04-05)

- [X] T1-A: Philosophy rewrite (architecture-philosophy.md, design-principles.md) — intermediary wrapper, 4-scope, 200-line, seed instructions
- [X] T1-C: Operational-patterns modularization — 3 monoliths → 9 files in 3 subdirectories
- [X] T1-01: Memory system rewrite (4-scope, auto memory, autoDream, 7-layer runtime)
- [X] T1-02: Skills frontmatter expansion (3→11+ fields, substitutions, fork, ultrathink)
- [X] T1-03: Subagents frontmatter expansion (16 fields, memory, background, isolation)
- [X] T1-04: Hooks major expansion (26 events, 4 types, if/async, CAB QA/QC patterns)
- [X] T1-05: Plugin schema expansion (userConfig, channels, LSP, bin/, CLAUDE_PLUGIN_DATA)
- [X] T1-06: Settings documentation rewrite (60+ fields, 5-level hierarchy, sandbox, auto mode)
- [X] T1-07: MCP integration update (3 server types, registry, channels, elicitation)
- [X] T1-08: Custom commands → skills migration documentation
- [X] T1-09: Effort level documented (low/medium/high official; max observed-but-undocumented)
- [X] T1-10: URL migration (docs.anthropic.com → code.claude.com, 2 legitimate exceptions)
- [X] Verification: 8/8 criteria PASS (after fixes), cross-references updated

### T2: Schema & Metadata Compliance ✅ (2026-04-05)

- [X] T2-01: source: metadata backfill (18 files updated + 14 already had source:) — all 32 KB files covered
- [X] T2-02: Frontmatter completeness (cc-architecture-diagrams.md, product-design-cycle.md) — full YAML blocks added
- [X] T2-03: Agent Verification sections (architecture-advisor, project-integrator) — all 4 agents now verified
- [X] T2-04: Agent frontmatter field updates (all 4 agents) — effort, context, permissionMode, disallowedTools
- [X] T2-05: Skill frontmatter field updates (all 7 skills) — argument-hint, effort, agent, imperative descriptions
- [X] T2-06: Create project .claude/settings.json — opus default, orchestrator agent, scoped permissions
- [X] T2-07: Knowledge INDEX.md update — master (27→32), overview (2→3), op-patterns (6→11)
- [X] T2-08: Marketplace documentation update — 8 source types, managed controls

### T3: Template & Scaffold Freshness ✅ (2026-04-05)

- [X] T3-01: settings.json.template — 60+ fields awareness, 5-level hierarchy, hooks with matcher/if/async
- [X] T3-02: plugin.json.template — userConfig, 7 component paths, full metadata
- [X] T3-03: CLAUDE.md.template (plugin) — seed-instruction style, @imports, 8 extension types
- [X] T3-04: CLAUDE.md.template (global) — @rules/ recursive, cross-project patterns
- [X] T3-05: agent.template — 16 fields in B+ tiers (3 required + 5 common + 8 advanced)
- [X] T3-06: skill.template — 13 fields in B+ tiers (2 + 4 + 7) + invocation control matrix
- [X] T3-07: command.template — deprecation notice (commands → skills migration)
- [X] T3-08: hooks.json template — NEW, 4 hook types × 4 common events, valid JSON

### T4: Structural Cleanup ✅ (2026-04-05)

- [X] T4-partial: Remove 4 old monolith files + fix 8 stale cross-references
- [X] T4-01: Fix stale frontmatter IDs in 4 files (extension-discovery, subagents, framework, team-collaboration)
- [X] T4-02: Remove duplicate product-design-cycle.md (docs/_internal/, not git-tracked)
- [X] T4-03: Clean settings.local.json — removed malformed bash fragments
- [X] T4-04: DUPLICATE files assessed — all 3 KEEP (git-foundation, security-defaults, glossary have CAB-specific value)
- [X] T4-05: STALE files evaluated — 3 removed in T1, arch-philosophy KEEP, cowork.md→stub, custom-commands KEEP
- [X] T4-06: TODO.md updated — T5-09/T5-10/T5-11 added, sync protocol marked done
- [X] T4-07: Sync protocol documented — NEW KB card: sync-protocol.md
- [X] T4-08: BRIDGE files assessed — both already have source: attribution

### T5: New Capabilities ✅ (2026-04-05)

- [X] T5-01: NEW KB card — Agent Teams (already existed from T1)
- [X] T5-02: NEW KB card — Auto Memory Patterns (COVERED: memory-claudemd.md + context-engineering.md)
- [X] T5-03: Context management section expansion (COVERED: context-engineering.md comprehensive at 141 lines)
- [X] T5-04: Plugin persistent data patterns — NEW KB card: plugin-persistent-data.md
- [X] T5-05: Output styles documentation — NEW KB card: output-styles.md
- [X] T5-06: LSP integration documentation — NEW KB card: lsp-integration.md
- [X] T5-07: Managed settings documentation (COVERED: global-user-config.md + memory-claudemd.md)
- [X] T5-08: INDEX.md final update — master 33→36, components 7→10, op-patterns 11→12
- [X] T5-09: Official `.claude/` directory schema alignment — 8 items added to global schema tree
- [X] T5-10: `/close-session` skill — standardized session state persistence + context handoff
- [X] T5-11: `/sync-check` command — automated CAB↔global drift detection

### PA-01: Global Config Audit ✅ (2026-04-06)

- [X] PA-01: intermediary sanity check of existing global CC config <-> latest enhanced CAB frameworks and protocols — INVESTIGATION COMPLETE. Report: `notes/pa-01-global-config-audit-2026-04-06.md`. 52 findings (9 ERROR, 28 ENHANCEMENT, 15 OPTIONAL), 6-phase implementation plan, 6 decision points.
- [X] ~~Establish + document sync protocol: CAB upstream → global downstream~~ → DONE (T4-07, sync-protocol.md)

</details>

<details>
<summary>P1-HOT: Initial 6-Extension Reconciliation ✅ (2026-04-03)</summary>

- [X] Merge `analyze-architecture` skill INTO CAB plugin (global → CAB, cleaned stale refs)
- [X] Merge `plan-implementation` skill + assets INTO CAB plugin (global → CAB, 3 files)
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
- [X] Create `skills/execute-task/SKILL.md` — Standard task execution protocol as model-invoked skill
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

- [X] Create plan-implementation, assessing-quality, designing-workflows, visualizing-data skills
- [X] Broaden analyze-architecture description
- [X] Verify all 8 skills load via /memory

</details>

<details>
<summary>P-LIVE: A-Team/Product-Design Integration ✅</summary>

- [X] Create reference/INDEX.md, update commands, update plan-implementation skill

</details>

<details>
<summary>P-LIVE: CAB Plugin Marketplace Test ✅</summary>

- [X] Publish, register, install, validate 14 commands + 4 agents + 5 skills
- [X] Test /validate and /integrate-existing on HEC-RAS

</details>

---

## Reference Artifacts

> Version is centralized in `.claude-plugin/plugin.json`.

| Artifact                   | Location                                                                 | Status         |
| -------------------------- | ------------------------------------------------------------------------ | -------------- |
| Implementation Plan (PFA)  | `notes/impl-plan-plugin-first-architecture-2026-04-08.md`              | Active         |
| R2 Audit Report (YAML)     | `notes/cab-audit-2026-04-09.yaml`                                      | Active         |
| R2 Audit Report (Markdown) | `notes/cab-audit-2026-04-09.md`                                        | Active         |
| PA-01 Global Config Audit  | `notes/pa-01-global-config-audit-2026-04-06.md`                        | Awaiting review |
| CC Docs Investigation      | `notes/cc-docs-investigation-2026-04-04.md`                            | Reference      |
| Techdebt v2                | `notes/techdebt-v2-2026-04-04.md`                                      | Reference      |
| Techdebt v1 (baseline)     | `notes/techdebt-2026-04-03.md`                                         | Reference      |
| Global Extensions Map      | `notes/global-extensions-map.md`                                       | Active         |
| Lessons Learned            | `notes/lessons-learned.md`                                             | Active (21 entries) |
| User's Original Comments   | `notes/my-response-to-techdebt-2026-04-03.md`                          | Reference      |
| Changelog Concept          | `notes/changelog-system-design.md`                                     | Concept        |
| Orchestration Framework    | `knowledge/operational-patterns/orchestration/framework.md`            | Active         |
| Multi-Agent Collaboration  | `knowledge/operational-patterns/multi-agent/collaboration-patterns.md` | Active         |
| Session Lifecycle          | `knowledge/operational-patterns/state-management/session-lifecycle.md` | Active         |
| Team Collaboration         | `knowledge/operational-patterns/team-collaboration.md`                 | Active         |
| Orchestrator Agent         | `agents/orchestrator.md`                                               | Active         |
| Verifier Agent             | `agents/verifier.md`                                                   | Active         |
| Knowledge Index            | `knowledge/INDEX.md`                                                   | Active         |
| plugin.json                | `.claude-plugin/plugin.json`                                           | Active         |
