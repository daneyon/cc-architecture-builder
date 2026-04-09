---
name: auditing-workspace
description: >-
  INVOKE THIS SKILL to audit any CC-integrated project workspace against CAB
  v1.1.0 standards. Triggers: audit workspace, check project standards, cab
  audit, review CC configuration quality, workspace health check, project
  compliance review, assess CC setup. Performs read-only 7-dimension assessment
  with scored findings and persistent YAML + markdown artifacts. Use this
  whenever the user has an existing CC project and wants to know how well it
  follows best practices — even if they just say "check my setup" or "is my
  config any good."
argument-hint: "Target path (default: cwd) and flags (e.g., '--changed-only')"
agent: true
effort: high
allowed-tools: Read, Grep, Glob, Bash
---

# Workspace Audit

Audit a CC-integrated project workspace against CAB v1.1.0 architectural
standards. This is a **read-only** assessment — no files are modified. The
output is a scored gap report with remediation guidance, persisted as artifacts
for iterative tracking.

## When to Use

- User has an existing CC-integrated project and wants a quality check
- Before starting a major project phase (baseline audit)
- After a series of changes to verify standards alignment
- Periodic health checks on CC configuration quality
- When onboarding to an unfamiliar CC project

## Instructions

Execute these phases sequentially. Never skip a phase or load all standard
packs at once (token efficiency — process one dimension at a time).

### Phase 0: Context Discovery

Understand the project before applying standards. This prevents false positives
from applying team-level expectations to a solo project.

1. **Detect project type** (determines component location convention):
   ```bash
   ls CLAUDE.md .claude/ .claude-plugin/ 2>/dev/null
   ```
   - **Plugin project**: has `.claude-plugin/plugin.json` → components at ROOT (`agents/`, `skills/`, `commands/`)
   - **Standalone project**: has `.claude/` or `CLAUDE.md` but NO `.claude-plugin/` → components under `.claude/`
   - **Not CC-integrated**: neither present → **ABORT** — suggest `/integrate-existing` instead

   Set `project_type` = `plugin` | `standalone` — carry this through ALL subsequent phases.

   > **Architecture rule**: Plugin components live at project root per CC convention.
   > `.claude/` retains project settings, rules, local overrides, and agent-memory
   > regardless of project type. Only distributable components differ in location.

2. **Read project context**:
   - `CLAUDE.md` first paragraph for domain/purpose
   - `plugin.json` for metadata, component paths, and distribution info (if plugin)
   - Count components in the correct location per `project_type`:
     - Plugin: `agents/`, `skills/`, `commands/`, `hooks/`, `knowledge/`
     - Standalone: `.claude/agents/`, `.claude/skills/`, `.claude/commands/`, `knowledge/`

3. **Determine complexity tier** (governs which criteria apply):

   | Tier | Signals |
   |------|---------|
   | **Minimal** | ≤2 total components, no knowledge dir, solo project |
   | **Standard** | 3-10 components, some knowledge, small team |
   | **Advanced** | 10+ components, knowledge base, orchestration, team |

4. **Check for prior audit**:
   ```bash
   ls notes/cab-audit-*.yaml 2>/dev/null | tail -1
   ```
   If found, load for delta comparison in Phase 3.

### Phase 1: Structural Pre-Check

Run basic structural validation before attempting quality assessment. Auditing
quality of files in the wrong location produces confusing results.

**Critical checks** (any failure blocks Phase 2):
- `CLAUDE.md` exists
- Components are in the correct location for `project_type`:
  - **Plugin**: `agents/`, `skills/`, `commands/` at project root. Components found under `.claude/` instead = ERROR (wrong convention for plugins — must be at root for CC plugin discovery)
  - **Standalone**: `.claude/agents/`, `.claude/skills/`, `.claude/commands/`. Root-level components without `.claude-plugin/plugin.json` = ERROR
- If plugin: `.claude-plugin/plugin.json` exists and is valid JSON
- If plugin: `plugin.json` does NOT have stale custom paths pointing to `.claude/` (e.g., `"agents": ".claude/agents/"`) — this is a non-standard workaround that masks the root-level convention. Severity: WARN

**Warning checks** (noted but don't block):
- `.gitignore` exists
- `README.md` exists (plugins only)
- No components inside `.claude-plugin/` directory (only `plugin.json` belongs there)
- If plugin: root `settings.json` exists with `agent` key (plugin-distributed default agent)

If critical checks fail: emit structural report and **STOP**. Recommend
`/validate --full` to fix structural issues before re-running audit.

### Phase 2: Standards Audit (7 Dimensions)

For **each dimension**, follow this protocol:

1. Read the standard pack from `references/standards/<dimension>-standards.md`
2. Read the target files from the project for this dimension
3. Evaluate each criterion against the scoring rubric
4. Score the dimension: 0 (ABSENT) / 1 (MINIMAL) / 2 (ADEQUATE) / 3 (EXEMPLARY)
5. Classify each finding: MISSING / STALE / ENHANCEMENT / CURRENT
6. Record evidence (specific files, line references, patterns found/missing)
7. Link remediation to specific KB docs

**Process dimensions sequentially** to manage token budget:

| # | Dimension | Standard Pack | Target Files (plugin) | Target Files (standalone) |
|---|-----------|--------------|----------------------|--------------------------|
| 1 | CLAUDE.md Quality | `claudemd-standards.md` | `CLAUDE.md`, `CLAUDE.local.md` | same |
| 2 | Agent Frontmatter | `agent-standards.md` | `agents/*.md` | `.claude/agents/*.md` |
| 3 | Skill Frontmatter | `skill-standards.md` | `skills/*/SKILL.md` | `.claude/skills/*/SKILL.md` |
| 4 | Settings Configuration | `settings-standards.md` | `.claude/settings.json` + root `settings.json` | `.claude/settings.json` |
| 5 | Rules Coverage | `rules-standards.md` | `.claude/rules/**/*.md` | same |
| 6 | Knowledge Structure | `knowledge-standards.md` | `knowledge/**` | same |
| 7 | Hooks Configuration | `hooks-standards.md` | `hooks/hooks.json` | hooks in `.claude/settings.json` |

For dimensions with zero applicable components at the project's complexity tier,
score as N/A rather than ABSENT. A minimal project with no agents is not
penalized for lacking agent frontmatter.

Read `references/classification-schema.md` before starting Phase 2 for the
full scoring rubric, classification definitions, and contextual tier adjustments.

### Phase 3: Synthesis + Artifact Generation

1. **Aggregate scores**: Sum dimension scores, compute percentage (0-21 scale)
2. **Classify overall**:
   - NEEDS WORK: 0-33%
   - DEVELOPING: 34-66%
   - ALIGNED: 67-89%
   - EXEMPLARY: 90-100%
3. **Rank findings** by severity (ERROR > WARN > INFO), then by dimension score (lowest first)
4. **Compute delta** if prior audit exists (per-dimension score change)
5. **Generate YAML artifact**: `notes/cab-audit-YYYY-MM-DD.yaml`
   - See `references/audit-methodology.md` for schema
6. **Generate markdown summary**: `notes/cab-audit-YYYY-MM-DD.md`
   - See `references/audit-methodology.md` for template
7. **Present console summary**: overall score, top 3 findings, artifact paths

### Output Location

All artifacts go to the **target project's** `notes/` directory (create if
needed). This keeps audit history co-located with the project.

## Flags

| Flag | Behavior |
|------|----------|
| (none) | Full 7-dimension audit |
| `--changed-only` | Re-audit only dimensions affected by files changed since last audit (uses `git diff` against last audit date) |

### `--changed-only` Behavior

```bash
# Get files changed since last audit
last_audit_date=$(grep "audit_date:" notes/cab-audit-latest.yaml | cut -d'"' -f2)
git diff --name-only --since="$last_audit_date" HEAD
```

Map changed files to dimensions (resolve paths per `project_type`):

| Changed File Pattern (plugin) | Changed File Pattern (standalone) | Re-audit Dimension |
|------------------------------|----------------------------------|-------------------|
| `CLAUDE.md` | `CLAUDE.md` | CLAUDE.md Quality |
| `agents/*` | `.claude/agents/*` | Agent Frontmatter |
| `skills/*` | `.claude/skills/*` | Skill Frontmatter |
| `.claude/settings*` or `settings.json` | `.claude/settings*` | Settings Configuration |
| `.claude/rules/*` | `.claude/rules/*` | Rules Coverage |
| `knowledge/**` | `knowledge/**` | Knowledge Structure |
| `hooks/hooks.json` or hook scripts | hooks config or scripts | Hooks Configuration |

Dimensions with no changed files retain their prior score.

## Override Mechanism

Projects can suppress specific findings by adding a `.cab-audit-ignore` file:

```yaml
# Findings to suppress (by criterion ID)
suppress:
  - agents.verification_section  # Intentionally omitted for lightweight agents
  - settings.sandbox             # Windows — sandbox not available
```

Suppressed findings appear in the report as "SUPPRESSED" with the reason, but
don't affect the score.

## Integration

- **Upstream**: `/validate --cab-audit` routes here (validate command dispatches)
- **Downstream**: Output YAML feeds into `/execute-task` for remediation planning
- **Orchestrator**: Recognizes "audit workspace" requests and invokes this skill
- **Delta tracking**: Each audit builds on prior runs for longitudinal health monitoring

## See Also

- `references/audit-methodology.md` — Formalized PA-01 workflow, artifact schemas
- `references/classification-schema.md` — Scoring rubric, classification definitions
- `references/standards/` — 7 modular standard packs (one per audit dimension)
- `knowledge/components/` — Authoritative KB sources for each dimension
