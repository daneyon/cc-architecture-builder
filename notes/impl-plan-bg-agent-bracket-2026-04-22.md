# Implementation Plan: Background-Agent Write-Failure Bracket (UXL-027 + UXL-028)

**Date**: 2026-04-22
**Owner**: orchestrator (CAB)
**Source rows**: UXL-027 (LL-02/12 pre-gate) + UXL-028 (LL-08 post-check) — Wave 2 of `notes/ux-log-wave-plan-2026-04-22.md`
**Effort**: M per row (paired execution; single plan, two phases)
**Plan scope**: self-contained; no cross-project work

---

## 0. Statement of Work (Embedded)

### 0.1 Problem

Background agents in CC silently fail to write files. The failure mode is architecturally baked-in (LL-02, 2026-04-03: "Background agents can't write files"), was documented clearly, then recurred (LL-12, 2026-04-05: explicit recurrence with token waste + `/compact` forced). The recurrence validates the thesis that **passive documentation does not prevent recurrence — structural enforcement does**.

Two orthogonal gaps exist:
- **Pre-condition (LL-02/LL-12)**: main session delegates a write-intent task to a background agent; nothing stops it at invocation time. The agent executes, claims success, produces no files.
- **Post-condition (LL-08)**: even foreground or properly-scoped background agents can claim "wrote to X" in their summary while the file is empty or missing. No post-hoc verification catches this.

Together they bracket the full failure class. Individually each leaves a hole.

### 0.2 Proposed Solution

Two paired hooks deployed via CAB's `hooks/hooks.json`:

- **UXL-027 `bg-agent-pre-gate.sh`** (PreToolUse on `Agent`): inspect `run_in_background: true` + write-intent signals; emit WARN with LL-02/LL-12 reference; do NOT hard-block in v1 (escalation path if WARN proves insufficient).
- **UXL-028 `bg-agent-post-check.sh`** (PostToolUse on `Agent`): parse agent result for claimed-file-path signals; verify each path exists on disk; emit WARN with LL-08 reference when claims don't match reality.

Both are `type: "command"` deterministic scripts per LL-14 (never `type: "prompt"` — self-policing is not independent verification).

### 0.3 Challenges & Mitigations

| Challenge | Mitigation |
|---|---|
| Main session doesn't directly see subagent's tool allowlist at Agent invocation time | Pre-gate uses heuristic pattern-match on prompt (write/create/edit/save keywords) + subagent_type read-only allowlist (Explore = read-only; general-purpose = potentially-writing); emit WARN not ERROR |
| Post-check needs to know what artifacts were expected | v1 parses agent result text for explicit path mentions (regex: `wrote to <path>`, `created <path>`, `updated <path>`); verifies each; does NOT attempt to infer intended artifacts from original prompt (too brittle) |
| False-positive on research agents that legitimately mention paths in their report | Post-check emits WARN-only; user can ignore if the mention was narrative (not a claim of authorship) |
| Hard-block would be aggressive (many valid bg research agents) | v1 = WARN via stderr + exit 0. Escalation path: exit 2 hard-block only for clear LL-02 pattern (bg + explicit write intent + write-capable tools) |

### 0.4 Timeline

Three phases, ~1 session total:
1. UXL-027 pre-gate (~30 min)
2. UXL-028 post-check (~40 min)
3. hooks.json integration + dogfood validation (~20 min)

### 0.5 KPIs

| Category | Metric | Target |
|---|---|---|
| Coverage | Hook fires on every Agent invocation | 100% |
| Pre-gate recall | WARN emits when bg + Write-capable subagent + write-intent prompt | 100% of test cases below |
| Pre-gate precision (low false-positive) | No WARN on read-only bg agents (Explore subagent_type) | ≥90% |
| Post-check recall | WARN emits when agent claims path that doesn't exist on disk | 100% of test cases |
| Post-check precision | No WARN on agents that never claimed writes | 100% |
| Determinism compliance (LL-14) | Both hooks are `type: "command"`; exit codes clear | 100% |
| Reversibility (UXL-019) | Both hooks individually revertable via single `git revert` | 100% |

---

## 1. Project Overview

### 1.1 Scope Boundaries

**In scope**:
- Two new scripts: `hooks/scripts/bg-agent-pre-gate.sh` and `hooks/scripts/bg-agent-post-check.sh`
- Updates to `hooks/hooks.json` registering both with Agent matcher
- Per-phase acceptance-criteria testing via crafted Agent invocations
- Reversibility inventory row in `filesystem-patterns.md` (UXL-019 append convention)
- CSV state-machine updates at phase completion

**Out of scope** (deferred to future UXL rows if needed):
- Hard-block escalation (WARN is v1; ERROR requires empirical evidence that WARN is ignored)
- Tool-allowlist introspection (would require reading subagent `.md` file on every hook fire — too costly)
- Integration with `ux-log-sync.sh` hook convention (UXL-011-adjacent; separate row)
- Retry-on-failure or auto-refoundation (out-of-pattern; would change CC's own behavior)

### 1.2 Assumptions

- CC's Agent tool accepts PreToolUse + PostToolUse hooks with `matcher: "Agent"` (confirmed by CC docs)
- `tool_input.run_in_background` is present in hook stdin JSON when caller specifies it (verify in Phase 1 test)
- PostToolUse hooks receive `tool_result` in stdin JSON (verify in Phase 2 test)
- Hook stderr surfaces to the caller (main agent sees it); exit 0 + stderr = WARN (non-blocking) semantics hold

### 1.3 Constraints

- LL-14: must use `type: "command"` with deterministic script (no `type: "prompt"`)
- Security rules (`.claude/rules/security.md`): atomic edits; never skip hooks mid-session
- Component standards: new files only; no changes to existing hook files except hooks.json registration
- Bash-only scripts (portable across Git Bash on Windows + Linux/macOS; match existing CAB hook conventions)

---

## 2. Requirements

### 2.1 Functional (per phase)

| ID | Feature | Acceptance Criteria |
|---|---|---|
| F001 | Pre-gate detects bg + write-intent prompt | Given `Agent(run_in_background: true, prompt: "write summary to notes/foo.md")`, when invocation fires, the hook emits WARN to stderr citing LL-02/LL-12 and referencing the prompt phrase matched |
| F002 | Pre-gate allows read-only bg research | Given `Agent(run_in_background: true, subagent_type: "Explore", prompt: "find all X")`, the hook emits NO warning (exit 0 silently) |
| F003 | Pre-gate allows foreground writes | Given `Agent(run_in_background: false, prompt: "write summary")`, no WARN (bg flag is the gate trigger) |
| F004 | Post-check verifies claimed paths | Given agent result text `"wrote to notes/foo.md"` and `notes/foo.md` does not exist, emit WARN citing LL-08 with the missing path |
| F005 | Post-check allows truthful reports | Given agent result mentions paths AND all those paths exist on disk, exit 0 silently |
| F006 | Post-check ignores narrative path mentions | Given agent result says `"the file notes/foo.md is interesting"` (no write claim), emit NO warning — distinguish `wrote to`/`created`/`updated` (write verbs) from mere mentions |
| F007 | Both hooks registered in hooks.json | `hooks.json` contains Agent matcher for both PreToolUse (pre-gate) and PostToolUse (post-check); no breaking changes to existing Bash matcher |

### 2.2 Non-Functional

| Category | Requirement | Target |
|---|---|---|
| Performance | Hook latency per Agent fire | <100ms (simple Bash grep; no network) |
| Idempotency | Re-running same hook input produces same output | 100% |
| Observability | WARN messages cite the LL and the specific trigger | 100% of WARN paths |
| Compliance (LL-14) | Script type is `"command"`, never `"prompt"` | 100% |
| Reversibility | Revert command: `git revert <single-commit>` per hook | Two atomic commits |

---

## 3. System Architecture

### 3.1 Hook Mechanics

CC's hook protocol (confirmed via existing `pre-push-state-review.sh`):
- Stdin JSON contains `tool_name`, `tool_input`, `tool_result` (PostToolUse only)
- Exit 0 = allow; exit 2 = block (stderr = reason surfaced to CC)
- Stderr on exit 0 = informational/WARN message (non-blocking; appears in CC's transcript)

### 3.2 UXL-027 Pre-Gate Logic

```
Read tool_input JSON from stdin
If tool_name != "Agent" → exit 0 silently
Extract: run_in_background (bool), subagent_type (string), prompt (string)
If run_in_background != true → exit 0 silently (foreground — not our concern)
If subagent_type in (read-only allowlist: "Explore", "general-researcher") → exit 0 silently
Match prompt against write-intent regex:
  \b(write|create|edit|save|update|commit|author|append|modify|draft|produce|generate)\b.*\.(md|txt|json|yaml|yml|csv|py|sh|js|ts|tsx|html|css|toml)\b
  OR explicit path mentions: \b(notes/|\.claude/|hooks/|skills/|agents/|commands/|knowledge/)
If match found:
  Emit WARN to stderr:
    "⚠️  [UXL-027/LL-02/LL-12] Background agent invoked with apparent write-intent prompt"
    "    Matched pattern: <pattern>"
    "    Risk: background agents silently fail to write files (documented failure mode)"
    "    Recommendation: invoke foreground (run_in_background=false) OR delegate write to main session after bg research completes"
    "    Override: set CAB_SKIP_BG_GATE=1 if intentional (e.g., validated read-only research with incidental file mentions)"
  Exit 0 (WARN-only; v1 does not hard-block)
Else exit 0 silently
```

### 3.3 UXL-028 Post-Check Logic

```
Read tool_input + tool_result JSON from stdin
If tool_name != "Agent" → exit 0 silently
Extract tool_result.content (agent's final summary text)
Parse for write-claim patterns (regex captures path):
  \bwrote (?:to )?(\S+\.\w+)\b
  \bcreated (\S+\.\w+)\b
  \bupdated (\S+\.\w+)\b
  \bsaved (?:to )?(\S+\.\w+)\b
  \bappended (?:to )?(\S+\.\w+)\b
For each captured path:
  Normalize relative to repo root
  If file does not exist on disk:
    collect into "missing" list
If missing list non-empty:
  Emit WARN to stderr:
    "⚠️  [UXL-028/LL-08] Background agent claimed file writes that did not materialize"
    "    Missing paths:"
    "      <path-1>"
    "      <path-2>"
    "    Risk: LL-08 failure mode — agent output may be authoritative-looking but non-persisting"
    "    Recommendation: re-run the write as a foreground operation; verify artifacts exist"
  Exit 0 (WARN-only)
Else exit 0 silently
```

### 3.4 hooks.json Integration

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ /* existing bash hooks */ ] },
      {
        "matcher": "Agent",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/bg-agent-pre-gate.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Agent",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/bg-agent-post-check.sh" }
        ]
      }
    ]
  }
}
```

### 3.5 Architecture Decision Records

| Decision | Options | Choice | Rationale |
|---|---|---|---|
| v1 behavior: WARN vs BLOCK | WARN (exit 0 + stderr) / HARD-BLOCK (exit 2) | WARN | Read-only bg research is legitimate + common; hard-block would be aggressive. Empirical evidence needed before escalating. |
| Write-intent detection | Prompt regex / subagent tool-allowlist inspection / both | Prompt regex + subagent-type allowlist | Tool-allowlist inspection requires reading subagent .md files on each fire (~10-50ms overhead × multiplied by bg-invocations). Regex on prompt + subagent-type check covers ~90% of cases cheaply. |
| Path claim detection | NLP / regex / explicit protocol | Regex on write-verb patterns | NLP overkill for 1-line hook; explicit protocol would require retraining agents to emit structured output. Regex is portable, deterministic, LL-14 compliant. |
| Override mechanism | Env var (CAB_SKIP_BG_GATE=1) / no override / per-tool flag | Env var | Matches existing CAB pattern (`CAB_SKIP_PREPUSH_REVIEW=1` in pre-push hook). One env var = one escape hatch; avoids feature creep. |

---

## 4. Implementation Phases

### Phase 1: UXL-027 Pre-Gate Script (~30 min)

| Task | Deliverable | Acceptance |
|---|---|---|
| 1.1 | `hooks/scripts/bg-agent-pre-gate.sh` | Bash script; LL-14 compliant (`type: "command"`); handles absent/malformed JSON gracefully |
| 1.2 | Regex test harness | Inline test block (commented) demonstrating F001, F002, F003 pass |
| 1.3 | Docstring header | Usage, input schema, exit codes, LL references, override mechanism |
| 1.4 | Commit | `feat(hook): bg-agent pre-gate [UXL-027]` |

**Gate**: F001 + F002 + F003 manually validated via test JSON inputs piped to the script.

### Phase 2: UXL-028 Post-Check Script (~40 min)

| Task | Deliverable | Acceptance |
|---|---|---|
| 2.1 | `hooks/scripts/bg-agent-post-check.sh` | Bash script; reads PostToolUse JSON; extracts write-claim paths; verifies |
| 2.2 | Regex test harness | Inline test block demonstrating F004, F005, F006 pass |
| 2.3 | Path normalization logic | Relative-to-repo-root resolution; handles `./` prefixes; Windows path variants tolerated |
| 2.4 | Docstring header | Usage, input schema, exit codes, LL references |
| 2.5 | Commit | `feat(hook): bg-agent post-check [UXL-028]` |

**Gate**: F004 + F005 + F006 manually validated.

### Phase 3: hooks.json Integration + Validation (~20 min)

| Task | Deliverable | Acceptance |
|---|---|---|
| 3.1 | Update `hooks/hooks.json` | Adds Agent matcher to PreToolUse + new PostToolUse block; existing Bash matcher unchanged |
| 3.2 | Validate JSON syntax | `python -m json.tool hooks/hooks.json` clean |
| 3.3 | Update `filesystem-patterns.md` reversibility inventory (UXL-019 convention) | Append 2 rows: UXL-027 + UXL-028 commits + revert commands |
| 3.4 | CSV state-machine updates | UXL-027 → resolved; UXL-028 → resolved; both use `hooks/scripts/uxl-update.py resolve` (UXL-033 dogfood continues) |
| 3.5 | Commit | `chore(hooks): register bg-agent bracket [UXL-027, UXL-028]` + `chore(ux-log): resolve UXL-027+028` |

**Gate**: hooks.json valid JSON; reversibility inventory current; both CSV rows marked resolved with linked_commit set.

---

## 5. Testing Strategy

Per-phase inline validation (no external test framework):

**Phase 1 fixtures** (manually piped to script):
```bash
# F001: bg + write intent → WARN expected
echo '{"tool_name":"Agent","tool_input":{"run_in_background":true,"subagent_type":"general-purpose","prompt":"write summary to notes/foo.md"}}' | hooks/scripts/bg-agent-pre-gate.sh

# F002: bg + read-only subagent → silent exit 0
echo '{"tool_name":"Agent","tool_input":{"run_in_background":true,"subagent_type":"Explore","prompt":"find all X"}}' | hooks/scripts/bg-agent-pre-gate.sh

# F003: foreground + write → silent exit 0
echo '{"tool_name":"Agent","tool_input":{"run_in_background":false,"prompt":"write summary"}}' | hooks/scripts/bg-agent-pre-gate.sh
```

**Phase 2 fixtures**:
```bash
# F004: claimed missing file → WARN
echo '{"tool_name":"Agent","tool_input":{...},"tool_result":{"content":"wrote to notes/nonexistent.md"}}' | hooks/scripts/bg-agent-post-check.sh

# F005: truthful claim (existing file) → silent exit 0
echo '{"tool_name":"Agent","tool_input":{...},"tool_result":{"content":"wrote to notes/progress.md"}}' | hooks/scripts/bg-agent-post-check.sh

# F006: narrative mention (no write verb) → silent exit 0
echo '{"tool_name":"Agent","tool_input":{...},"tool_result":{"content":"the file notes/foo.md is interesting"}}' | hooks/scripts/bg-agent-post-check.sh
```

**Phase 3 dogfood**: after hooks.json registration, the NEXT Agent invocation in this session fires the hooks live. We won't explicitly test hard against this because the gate is WARN-only; observable behavior is any `⚠️` messages in the transcript.

---

## 6. Deployment Plan

Not a deployed service — in-repo hook files. Rollout:
- Phase 3 commit = immediate effect for any CC session that pulls the updated hooks.json
- No restart required
- Rollback: `git revert` on the specific hook commit (reversibility inventory row)

---

## 7. Risk Register

| Risk | Prob | Impact | Mitigation |
|---|---|---|---|
| Hook input JSON schema drifts (CC docs vs reality) | Med | Med | Phase 1.1 includes stdin-validation with graceful fallback (missing fields → exit 0 silently) |
| False-positive WARN storm on research agents | Med | Low | F002 + F006 precision targets; read-only subagent_type allowlist; env-var override |
| Path normalization mishandles Windows backslashes | Low | Med | Accept both `/` and `\` in post-check regex; test on Git Bash |
| Regex over-matches legitimate prose | Low | Low | WARN-only in v1; no hard-block until empirical evidence justifies it |
| Performance overhead on every Agent invocation | Low | Low | Simple grep; <100ms per fire; CC's own overhead dwarfs this |

---

## 8. Acceptance Criteria (plan-level)

- [ ] F001-F007 all pass manual test fixtures
- [ ] Phase 1 commit lands `hooks/scripts/bg-agent-pre-gate.sh`
- [ ] Phase 2 commit lands `hooks/scripts/bg-agent-post-check.sh`
- [ ] Phase 3 commit updates `hooks/hooks.json` with JSON-valid content
- [ ] `filesystem-patterns.md` reversibility inventory gets 2 new rows (UXL-027, UXL-028)
- [ ] CSV shows UXL-027 + UXL-028 as `status=resolved` with linked_commit populated
- [ ] No breaking changes to existing Bash hooks (pre-push, current-task-budget)

---

## Verification Questions for User (Sign-Off Gate)

1. **WARN-only v1 vs hard-block**: OK to ship WARN (exit 0 + stderr) in v1? Hard-block escalation only if we observe WARN being routinely ignored.
2. **Subagent read-only allowlist**: I've included `Explore` + `general-researcher` as known read-only. Any others I should add (e.g., your `debugger-specialist` — it can Read/Edit/Bash per its frontmatter, so probably stays out of allowlist)?
3. **Path claim regex scope**: I'm matching write verbs + file-extension patterns. Should I also match bare paths (e.g., `notes/foo`) without extensions? Leaning no — too many false positives.
4. **Override env var**: `CAB_SKIP_BG_GATE=1` matches existing `CAB_SKIP_PREPUSH_REVIEW=1` convention. OK?
5. **Post-check WARN on ANY missing path, vs only on explicit write verbs**: current design filters by verb (F006 precision). If that proves too loose, escalate to "any path mention + missing file = WARN"?

---

## Sign-Off

Plan awaits user SME verification before Phase 1 execution begins. On approval, `/cab:execute-task` will run Phase 1 → Phase 2 → Phase 3 sequentially.
