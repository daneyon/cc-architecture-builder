```markdown
# How Claude Code Manages Memory: A Deep Technical Analysis

**A comprehensive reverse-engineering of every memory and context management system inside Claude Code's leaked harness** — from lightweight token pruning to a "dreaming" system that consolidates memories while you sleep.

## 1. The Problem: Bounded Context in an Unbounded World

LLMs have a fundamental constraint: a fixed context window. Claude Code typically operates with a **200K token window** (expandable to 1M with the `[1m]` suffix). A single coding session can easily blow past this — a few file reads, some grep results, a handful of edit cycles, and you're at the limit.

Claude Code solves this with a **7-layer memory architecture** that spans from sub-millisecond token pruning to multi-hour background "dreaming" consolidation. Each layer is progressively more expensive but more powerful, and the system is designed so cheaper layers prevent the need for more expensive ones.

### Token Counting: The Foundation

Everything starts with knowing how many tokens you've used. The canonical function is `tokenCountWithEstimation()` in `src/utils/tokens.ts`:

```ts
Canonical token count = last API response's usage.input_tokens
                      + rough estimates for messages added since
```

The rough estimation uses a simple heuristic:  

- **4 bytes per token** for most text  
- **2 bytes per token** for JSON (which tokenizes more densely)  
- Images and documents get a flat **2,000 token** estimate regardless of size.

### Context Window Resolution

The system resolves the available context window through a priority chain:  
`[1m] model suffix → model capability lookup → 1M beta header → env override → 200K default`

The effective context window subtracts a **20K token reserve** for compaction output — you can't use the full window because you need room to generate the summary that saves you.

## 2. Architecture Overview: 7 Layers of Memory

Each layer is triggered by different conditions and has different costs. The system is designed so **Layer N prevents Layer N+1 from firing** whenever possible.

## 3. Layer 1: Tool Result Storage

**File:** `src/utils/toolResultStorage.ts`  
**Cost:** Disk I/O only — no API calls  
**When:** Every tool result, immediately

### The Problem

A single grep across a codebase can return 100KB+ of text. A `cat` of a large file might be 50KB. These results consume massive context and become stale within minutes as the conversation moves on.

### The Solution

Every tool result passes through a budget system before entering context.

When a result exceeds its threshold:  

- The **full result** is written to disk at `tool-results/<sessionId>/<toolUseId>.txt`  
- A **preview** (first ~2KB) is placed in context, wrapped in `<persisted-output>` tags  
- The model can later use `Read` to access the full result if needed

**ContentReplacementState: Cache-Stable Decisions**  
A critical subtlety: once a tool result is replaced with a preview, that decision is frozen in `ContentReplacementState`. On subsequent API calls, the same result gets the same preview — this ensures the prompt prefix remains byte-identical for prompt cache hits. This state even survives session resume by being persisted to the transcript.

**GrowthBook Override**  
Per-tool thresholds can be remotely tuned via the `tengu_satin_quoll` feature flag — allowing Anthropic to adjust persistence thresholds for specific tools without a code deploy.

## 4. Layer 2: Microcompaction

**File:** `src/services/compact/microCompact.ts`  
**Cost:** Zero to minimal API cost  
**When:** Every turn, before the API call

Microcompaction is the lightest-weight context relief. It doesn't summarize anything — it just clears old tool results that are unlikely to be needed.

### Three Distinct Mechanisms

**a) Time-Based Microcompact**  
**Trigger:** Idle gap since last assistant message exceeds threshold (default: 60 minutes)  
**Rationale:** Anthropic's server-side prompt cache has a ~1 hour TTL. If you haven't sent a request in an hour, the cache has expired and the entire prompt prefix will be re-tokenized from scratch. Since it's being rewritten anyway, clear old tool results first to shrink what gets rewritten.  
**Action:** Replaces tool result content with `[Old tool result content cleared]`, keeping at least the most recent N results (floor of 1).  
**Configuration:** via GrowthBook `tengu_slate_heron`.

**b) Cached Microcompact (Cache-Editing API)**  
This is the most technically interesting mechanism. Instead of modifying local messages (which would invalidate the prompt cache), it uses the API's `cache_edits` mechanism to delete tool results from the server-side cache without invalidating the prefix.

**How it works:**  

- Tool results are registered in a global `CachedMCState` as they appear  
- When the count exceeds a threshold, the oldest results (minus a "keep recent" buffer) are selected for deletion  
- A `cache_edits` block is generated and sent alongside the next API request  
- The server deletes the specified tool results from its cached prefix  
- Local messages remain unchanged — the deletion is API-layer only  

**Critical safety:** Only runs on the main thread. If forked subagents (session_memory, agent_summary, etc.) modified the global state, they'd corrupt the main thread's cache editing.

**c) API-Level Context Management (`apiMicrocompact.ts`)**  
A newer server-side approach using the `context_management` API parameter.

This tells the API server to handle context management natively — the client doesn't need to track or manage tool result clearing.

**Which Tools Are Compactable?**  
Only results from these tools get cleared:  
`FileRead`, `Bash/Shell`, `Grep`, `Glob`, `WebSearch`, `WebFetch`, `FileEdit`, `FileWrite`

Notably absent: thinking blocks, assistant text, user messages, MCP tool results.

## 5. Layer 3: Session Memory

**Files:** `src/services/SessionMemory/`  
**Cost:** One forked agent API call per extraction  
**When:** Periodically during conversation (post-sampling hook)

### The Idea

Instead of waiting until context is full and then desperately trying to summarize everything, continuously maintain notes about the conversation. Then when compaction *is* needed, you already have a summary ready — no expensive summarization call required.

### Session Memory Template

Each session gets a markdown file at `~/.claude/projects/<slug>/.claude/session-memory/<sessionId>.md` with a structured template.

### Trigger Logic

Session memory extraction fires when both conditions are met:  

- Token growth since last extraction ≥ `minimumTokensBetweenUpdate`  
- **AND** (tool calls since last extraction ≥ `toolCallsBetweenUpdates` **OR** no tool calls in the last assistant turn)

The token threshold is always required — even if the tool call threshold is met. The "no tool calls in last turn" clause captures natural conversation breaks where the model has finished a work sequence.

### Extraction Execution

The extraction runs as a forked subagent via `runForkedAgent()`:  

- `querySource: 'session_memory'`  
- Only allowed to use `FileEdit` on the memory file (all other tools denied)  
- Shares the parent's prompt cache for cost efficiency  
- Runs sequentially (via `sequential()` wrapper) to prevent overlapping extractions

### Session Memory Compaction: The Payoff

When autocompact triggers, it first tries `trySessionMemoryCompaction()`:  

- Check if session memory has actual content (not just the empty template)  
- Use the session memory markdown as the compaction summary — **no API call needed**  
- Calculate which recent messages to keep (expanding backward from `lastSummarizedMessageId` to meet minimums)  
- Return a `CompactionResult` with the session memory as summary + preserved recent messages

**Configuration:** (via GrowthBook flags)

The key insight: Session memory compaction is dramatically cheaper than full compaction because the summary already exists. No summarizer API call, no prompt construction, no output token cost. The session memory file is simply injected as the summary.

## 6. Layer 4: Full Compaction

**File:** `src/services/compact/compact.ts`  
**Cost:** One full API call (input = entire conversation, output = summary)  
**When:** Context exceeds autocompact threshold **AND** session memory compaction unavailable

### Trigger

`effective context window = context window - 20K (reserved for output)`  
`autocompact threshold = effective window - 13K (buffer)`

If `tokenCountWithEstimation(messages) > autocompact threshold` → trigger

### Circuit Breaker

After 3 consecutive failures, autocompact stops trying for the rest of the session. This was added after discovering that 1,279 sessions had 50+ consecutive failures (up to 3,272 in a single session), wasting approximately 250K API calls per day globally.

### The Compaction Algorithm

**Step 1: Pre-processing**  

- Execute user-configured PreCompact hooks  
- Strip images from messages (replaced with `[image]` markers)  
- Strip skill discovery/listing attachments (will be re-injected)

**Step 2: Generate Summary**  
The system forks a summarizer agent with a detailed prompt requesting a 9-section summary.

The prompt uses a clever two-phase output structure:  

- First: `<analysis>` block — a drafting scratchpad where the model organizes its thoughts  
- Then: `<summary>` block — the actual structured summary  

The `<analysis>` block is stripped before the summary enters context — it improves summary quality without consuming post-compact tokens.

**Step 3: Post-compact Restoration**  
After compaction, critical context is re-injected:  

- Top 5 recently-read files (5K tokens each, 50K total budget)  
- Invoked skill content (5K tokens each, 25K total budget)  
- Plan attachment (if in plan mode)  
- Deferred tool schemas, agent listings, MCP instructions  
- SessionStart hooks re-execute (restores `CLAUDE.md`, etc.)  
- Session metadata re-appended for `--resume` display

**Step 4: Boundary Message**  
A `SystemCompactBoundaryMessage` marks the compaction point.

### Partial Compaction

Two directional variants for more surgical context management:  

- `from` direction: Summarize messages **AFTER** a pivot index, keep earlier ones intact (preserves prompt cache).  
- `up_to` direction: Summarize messages **BEFORE** pivot, keep later ones (breaks cache).

### Prompt-Too-Long Recovery

If the compaction request itself hits prompt-too-long:  

- Group messages by API round via `groupMessagesByApiRound()`  
- Drop the oldest groups until the token gap is covered (or 20% of groups if gap is unparseable)  
- Retry up to 3 times  
- If all retries fail → `ERROR_MESSAGE_PROMPT_TOO_LONG` thrown

## 7. Layer 5: Auto Memory Extraction

**File:** `src/services/extractMemories/extractMemories.ts`  
**Cost:** One forked agent API call  
**When:** End of each complete query loop (model produces final response with no tool calls)

### Purpose

While Session Memory captures notes about the *current* session, Auto Memory Extraction builds **durable, cross-session knowledge** that persists in `~/.claude/projects/<path>/memory/`.

### Memory Types

Four types of memories, each with specific save criteria.

### Memory File Format

(Structured markdown per memory type)

### What NOT to Save

The extraction prompt explicitly excludes:  

- Code patterns, conventions, architecture (derivable from code)  
- Git history (use `git log`/`git blame`)  
- Debugging solutions (the fix is in the code)  
- Anything in `CLAUDE.md` files  
- Ephemeral task details

### Mutual Exclusivity with Main Agent

If the main agent already wrote memory files during the current turn, extraction is skipped. This prevents the background agent from duplicating work.

```ts
function hasMemoryWritesSince(messages, sinceUuid): boolean {
  // Scans for Edit/Write tool_use blocks targeting auto-memory paths
}
```

### Execution Strategy

The extraction prompt instructs the agent to be efficient:  

- Turn 1: Issue all `FileRead` calls in parallel  
- Turn 2: Issue all `FileWrite`/`FileEdit` calls in parallel  

### MEMORY.md: The Index

`MEMORY.md` is an index file, not a memory dump. Each entry should be one line under ~150 characters.  
Hard limits: 200 lines or 25KB — whichever is hit first.

## 8. Layer 6: Dreaming

**File:** `src/services/autoDream/autoDream.ts`  
**Cost:** One forked agent API call (potentially multi-turn)  
**When:** Background, after sufficient time and sessions have accumulated

### The Concept

Dreaming is cross-session memory consolidation — a background process that reviews past session transcripts and improves the memory directory. It's analogous to how biological memory consolidation happens during sleep.

### Gate Sequence (Cheapest Check First)

The dream system uses a cascading gate design where each check is cheaper than the next.

### The Lock Mechanism

The lock file at `<memoryDir>/.consolidate-lock` serves double duty (PID + timestamp).

### Four-Phase Consolidation

**Phase 1 — Orient**  
**Phase 2 — Gather Recent Signal**  
**Phase 3 — Consolidate**  
**Phase 4 — Prune and Index**

### Tool Constraints

Strict read-only Bash + limited edits to memory directory only.

### UI Surfacing

Dreams appear as background tasks in the footer with live progress tracking. Users can kill them.

## 9. Layer 7: Cross-Agent Communication

**Files:** `src/utils/forkedAgent.ts`, `src/tools/AgentTool/`, `src/tools/SendMessageTool/`

The **forked agent pattern** powers nearly every background operation.

Key optimizations for prompt cache sharing, agent spawning, `SendMessage` tool, persistent agent memory, and periodic agent summaries.

## 10. The Query Loop: How It All Fits Together

**File:** `src/query.ts`

## 11. Prompt Cache Optimization

One of the most sophisticated aspects of the entire system. Nearly every design decision is made to preserve Anthropic's server-side prompt cache (~1 hour TTL).

**Cache-Preserving Patterns** and **Cache Break Detection** are detailed in the original analysis.

## 12. Key Numbers

**Context Thresholds**  
**Tool Result Budgets**  
**Session Memory**  
**Compaction**  
**Dreaming**  
**Microcompact**

*(Refer to the original X post for the visual tables and diagrams accompanying these sections.)*

## 13. Design Principles

1. **Layered Defense, Cheapest First**  
2. **Prompt Cache Preservation** (obsessive)  
3. **Isolation with Sharing** (forked agents)  
4. **Circuit Breakers Everywhere**  
5. **Graceful Degradation**  
6. **Feature Flags as Kill Switches**  
7. **Mutual Exclusivity Where Needed**

---

**Source:** Reverse-engineered from Claude Code's leaked harness by @troyhua  
**Original post:** <https://x.com/troyhua/status/2039052328070734102>  
**Date:** March 31, 2026

---

**How to download:**  

1. Copy **everything** above (including the frontmatter `#` title).  
2. Paste into a new file.  
3. Save as `claude-code-memory-analysis.md`.  

Open in VS Code, Obsidian, Typora, or any Markdown viewer. Fully self-contained and ready to use! 🚀

```
