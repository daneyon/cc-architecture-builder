# Lessons Learned — CAB Operations Log

**Purpose**: Structured cross-session lesson persistence. Each entry captures an operational insight for future reference. This artifact feeds the planned changelog/lessons-learned compile & eval protocol.

**Template per entry**:
```yaml
- id: LL-XX
  date: YYYY-MM-DD
  category: operational | architectural | tooling | process | context-engineering
  source: {project or session context}
  lesson: "concise description"
  detail: "expanded context, evidence, rationale"
  actionable: true/false
  status: active | integrated | superseded
  integrated_to: "where applied, if any"
```

---

## Active Lessons

### LL-01: Explore agents can't access external directories
- **Date**: 2026-04-03
- **Category**: operational
- **Source**: HydroCast RAS-exec project
- **Lesson**: Explore agents are sandboxed to current project directory. Use general-purpose agents for cross-project reads.
- **Status**: active

### LL-02: Background agents can't write files
- **Date**: 2026-04-03
- **Category**: operational
- **Source**: HydroCast RAS-exec project
- **Lesson**: Background agents lack file write permissions. All artifact-writing must be in foreground. Background only for read-only research.
- **Status**: active

### LL-03: Post-compaction drops extension awareness
- **Date**: 2026-04-03
- **Category**: context-engineering
- **Source**: HydroCast RAS-exec project
- **Lesson**: After /compact, skill/agent/command awareness degrades. Re-read `notes/global-extensions-map.md` and restate current objective after any compaction.
- **Status**: active

### LL-04: Centralized state > scattered state
- **Date**: 2026-04-03
- **Category**: process
- **Source**: HydroCast RAS-exec project
- **Lesson**: All audit/session state must live in `notes/` as SSOT. Scattered state across multiple locations causes context loss across sessions.
- **Status**: active

### LL-05: Worktree agents don't auto-commit
- **Date**: 2026-04-03
- **Category**: operational
- **Source**: HydroCast RAS-exec project
- **Lesson**: Agents running in worktree isolation don't automatically commit their changes. Orchestrator must manually handle commits if worktrees are used.
- **Status**: active

### LL-06: Fan-out parallel agents for doc-heavy research
- **Date**: 2026-04-04
- **Category**: context-engineering
- **Source**: CAB comprehensive audit, Phase 1
- **Lesson**: 8 parallel foreground general-purpose agents fetched 11 CC doc categories simultaneously. Main session retained synthesis authority while agents handled context-heavy doc fetching. ~370K agent tokens consumed across subagents with zero impact on main session context. This is the orchestration framework's "fan-out → synthesize" pattern — critical for investigations that would blow through context if done inline.
- **Detail**: Each agent fetched 1-2 doc pages and compared against CAB KB. Results returned as structured reports. Main session synthesized 72 delta items into 2 primary artifacts without ever loading the raw doc pages into its own context.
- **Status**: active

### LL-07: State management artifact hierarchy
- **Date**: 2026-04-04
- **Category**: process
- **Source**: User directive during CAB audit
- **Lesson**: Three-tier state hierarchy must be maintained: (1) Implementation plan (detailed strategy, archived when superseded) → (2) TODO.md (incrementalized tasks, never delete, reorder pending to top) → (3) progress.md (live session state, can compact/reset). TODO never deletes content — completed items move to Completed Archive section. Only progress.md warrants deletions/compactions.
- **Status**: active

### LL-08: Background agent outputs must persist as artifacts
- **Date**: 2026-04-04
- **Category**: operational
- **Source**: CAB techdebt v3 strategic assessment
- **Lesson**: Background agents return results via task notification channel, but the output file on disk may be empty (likely a CC platform limitation). Any agent performing substantive analysis or planning must produce a persistent markdown artifact in the project's state management path (`notes/`). Do not rely on task notification output files for persistence or user accessibility.
- **Status**: active

---

## Pending (user has more to add)

User noted: "I have many other lessons-learned moments in bits and pieces I may later add after this full audit." This section reserved for future entries.
