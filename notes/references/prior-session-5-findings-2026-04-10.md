# 5 Critical Findings: CC 7-Layer Memory Architecture ↔ CAB State Management

**Source**: Session `c1f13ecc-4e09-45fa-a3e3-a9517f739eae.jsonl`, assistant msg idx 136, timestamp 2026-04-10T14:06:37Z
**Recovered**: 2026-04-11 Session 28 via subagent JSONL extraction; persisted to disk 2026-04-11 Session 29 as recovery backfill
**Why this file exists**: Session 2026-04-10 produced these 5 findings during analysis of `notes/references/How Anthropic Built 7 Layers of Memory and a Dreaming System for Claude Code  (video breakdown).md`. User chose "Option C (Hybrid)" — minimal integration now, deferred items to TODO. **The deferred items never made it to TODO.md.** Session 28 had to recover them from the JSONL archive. This file closes that LL-28 failure permanently.

---

## Preamble (verbatim from source session)

> *"CC already runs a 7-layer memory system underneath our state files. Every CAB state-management decision should ask 'which CC layer is this paralleling or augmenting?' — and deliberately avoid reimplementing what CC already does. This is the 'wrapper philosophy' (LL-11) applied to runtime memory."*

---

## Finding 1 — Prompt Cache Preservation Is Paramount

> *"Nearly every design decision is made to preserve Anthropic's server-side prompt cache (~1 hour TTL)."*

**CAB implication**:
- Append-only is cache-friendly
- **Mid-file edits are cache-hostile** — they invalidate the cached prefix
- "Newest at top" pattern for updatable sections preserves cache better than mid-file inserts
- State-file writes during active sessions should flow to a dedicated top-anchored zone, not scattered inserts

---

## Finding 2 — CC Auto-Memory Explicitly Excludes CLAUDE.md

> *"The extraction prompt explicitly excludes: Anything in CLAUDE.md files."*

**CAB implication**:
- CLAUDE.md Learned Corrections = **curated / semantic / cross-session** (human-authored, high signal-density)
- CC auto-memory at `~/.claude/projects/<slug>/memory/*` = **mechanical / extracted** (pattern-mined, lower signal-density)
- CAB `lessons-learned.md` = **audit trail before promotion** to CLAUDE.md
- **No duplication between layers** — each serves a distinct curation function
- Validates CAB's Learned Corrections layer as non-duplicative with CC's Layer 5 extraction

---

## Finding 3 — Session Memory Is Already Ready-When-Needed

> *"Session memory compaction is dramatically cheaper than full compaction because the summary already exists."*

**CAB implication**:
- `progress.md` should be a **continuously-updated, ready-to-use summary** — not a session-end-only write
- When auto-compaction fires, CC references the already-maintained summary instead of triggering full re-compaction
- Cadence reframe: "maintain an always-ready summary to preempt expensive compaction" (not "update at session close")
- This is the origin of the "newest-session-at-top" proposal for `progress.md`

---

## Finding 4 — MEMORY.md-Style Hard Limits Are a Pattern

> *"Hard limits: 200 lines or 25KB — whichever is hit first."*

**CAB implication (original analysis)**:
- At the time of analysis: `progress.md` was 42KB, `TODO.md` was 27KB — both already exceed CC's own MEMORY.md limits
- By Session 28: `progress.md` ≈ 90KB, `TODO.md` ≈ 40KB (further growth)
- Original proposed budgets: `current-task.md` <100 lines; `progress.md` bounded (200/25KB); `TODO.md` unbounded by design; `lessons-learned.md` periodic pruning

**USER OVERRIDE (2026-04-10, preserved verbatim)**:

> *"for finding 4 comments, i'm a bit weary based on my personal experiences of the lack of persistence in memory/context, and is why i've optimized to our current practice to detail out as much as possible in hydrocast, where i ask to create an in-depth summary of session to transfer over instead of getting lost in the forced compaction or even the generalized summarizations. as far as file size, i'm not too concerned as these raw interaction state mgmt artifacts/conversation histories shouldn't go into the main repo anyways and be archived to be excluded before syncing. I can see the pruning protocol of the lessons-learned to be useful but again emphasize on ensuring the generalization/summarization retain valuable/minimally required context to properly refer back with full bg context and apply accordingly. I can see current-task having a specific hard-coded constraint as suggested (we're already following), but for TODO and progress, i'm fine with relatively more agentically adaptive/flexible guidance/standardization (not a prescription or hard-coded limit) for now. the key in our holistically efficient and generalized standardization of our state mgmt practices is to not necessarily 'over-build' and/or 'hard-code' things too much to restrict native CC models and agents to inefficiently orchestrate and operationalize."*

**Reconciled decision (Session 28 v2 plan)**: Only `current-task.md` has a hard limit (<100 lines). `progress.md`/`TODO.md`/`lessons-learned.md` stay agentically flexible. Fix the **read pattern**, not the **file size**.

---

## Finding 5 — Layered Defense ("Layer N prevents N+1 from firing")

> *"Each layer is progressively more expensive but more powerful, and the system is designed so cheaper layers prevent the need for more expensive ones."*

**CAB implication**: The current bootstrap reads ALL state files eagerly — should become a **cheap-to-expensive cascade**:

1. `current-task.md` — <100 lines, ALWAYS read (cheap)
2. `progress.md` — top Current Position section only, read if cross-session context needed (medium)
3. `TODO.md` — top Top Priorities section only, read if planning new work (medium)
4. `lessons-learned.md` — table summary only, read if decision matches LL categories (expensive, load-on-demand)

Each layer should gate whether the next layer is read. The assistant voluntarily cascades based on task demands, not a rigid 4-file eager load.

**USER CAVEAT (preserved verbatim)**:

> *"for finding 5, this first principles system looks good but want to clarify lessons-learned as optional is appropriate only if we properly apply the suggestion in finding 4 about having structured protocol to actually architecturally/programmatically incorporate the lessons-learned as an effective standardization of CAB frameworks and operational protocols (multiple instances of not reviewing LLs causing you to create same mistakes for example; this honestly was evident for others like TODO and progress. just need to be careful to be as holistically standardized as possible."*

**Translation**: Partial/deferred reads of `lessons-learned.md` at bootstrap are acceptable **ONLY IF** LLs are architecturally woven into the skills/hooks that govern the decisions they constrain. Otherwise "passive reference" failure mode returns (LL-12/LL-17/LL-20 recurrence).

**This caveat is load-bearing for P4** — the LL integration audit in P4 of the bootstrap efficiency plan exists specifically to address this precondition.

---

## Session 2026-04-10 Closing Synthesis (deferred items, now logged)

User chose **Option C (Hybrid)** — minimal integration that session (cache-preservation note to `filesystem-patterns.md`), defer deeper items to TODO:

- New KB card `knowledge/operational-patterns/state-management/cc-memory-layer-alignment.md` — **now folded into P4** of bootstrap efficiency plan
- `dream-consolidation` skill concept — **out of scope** for bootstrap fix; remains in TODO.md as separate follow-on
- `progress.md` "newest-session-at-top" refactor — **now folded into P2** of bootstrap efficiency plan

**The deferred items never made it to TODO.md.** The causal chain: Option C approved → deferred items not written to disk → next session starts → deferred items lost. This is LL-28 in its purest form, which is itself why this file now exists.

---

## LL-28 Meta-Lesson From Recovery

The later `d17b1e16-...` session (Session 28) *referenced* these findings but reported them as unrecoverable. **The failure mode wasn't that the data was gone — it was that the assistant in the later session didn't check the transcript archive.** CC session transcripts are filesystem-accessible at `~/.claude/projects/<slug>/*.jsonl` and fully greppable. Every previous session's content is retrievable. This is a **dormant recovery resource** CAB never explicitly leveraged.

**LL-28 fallback-recovery protocol augmentation** (to be woven into a future skill):
> "When prior-session context is missing and state files don't cover it, grep the CC session JSONL archive at `~/.claude/projects/<project-slug>/*.jsonl` as first resort before regenerating from first principles."

---

## How These Findings Map to the Bootstrap Efficiency Plan (v2)

| Finding | Where it lands in impl plan |
|---|---|
| F1 — Cache preservation / newest-at-top | P2 (convention refactor uses top-anchored boundary markers) |
| F2 — Auto-memory excludes CLAUDE.md | P4 (new `cc-memory-layer-alignment.md` KB card documents this) |
| F3 — Session memory ready-when-needed | P2 (top-section convention makes `progress.md` continuously-ready) |
| F4 — Hard limits pattern (USER-OVERRIDDEN) | P3 (only `current-task.md` hard-gated; others stay flexible per user) |
| F5 — Cheap-to-expensive cascade | P2+P3+P4 (core mental model; documented in new `bootstrap-read-pattern.md` KB card) |
| F5 caveat — LLs architecturally woven | P4 (LL integration audit exposes gap; weaving = follow-on TODO items) |
