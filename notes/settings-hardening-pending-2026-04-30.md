# Settings Hardening — Pending Manual-Apply Diffs (2026-04-30)

**Context**: Session 41 settings hardening pass per audit findings. CAB + Global + GTA edits applied directly; HydroCast + RAS-exec are LL-13 deny-protected (`Edit(.claude/settings*)` / `Write(.claude/settings*)` in their own settings deny rules), so Claude cannot edit them automatically.

**Per the new default-deny rule** (`feedback_settings_json_default_deny_edit.md` + `.claude/rules/security.md` 6th bullet), settings.json edits require explicit user authoring/approval anyway. These two files would need manual edit even without the LL-13 self-deny.

**Apply via your IDE** (currently has these files openable). After applying, the CAB-side advisory card + verifier pass picks up the unified state.

---

## 1. HydroCast — `c:/Users/daniel.kang/Desktop/Automoto/Flood-Forecasting/.claude/settings.json`

**Change**: REMOVE `effortLevel: "high"` (line 69 currently). Lets global xhigh inherit per UXL-039.

**Diff**:

```diff
   "sandbox": {
     "enabled": true,
     "filesystem": {
       "denyRead": ["~/.ssh/*", "~/.aws/*", "~/.gnupg/*"],
       "denyWrite": ["~/.ssh/*", "~/.aws/*", "~/.claude/settings*"]
     }
   },
   "enabledPlugins": {
     "cab@cab": true
   },
-  "effortLevel": "high",
   "agent": "orchestrator",
   "subagentModel": "opus"
 }
```

**KEEP unchanged**: `agent: orchestrator` (project-specific main-thread agent), `subagentModel: opus` (subagent model override), the entire hooks block (script exists at `.claude/hooks/bash-security-gate.sh`, 1619 bytes), sandbox, enabledPlugins.

**FLAG (separate Wave 9+ alignment task; NOT part of this edit)**: HydroCast's `bash-security-gate.sh` (1619 bytes) is divergent from global's (6062 bytes). Cross-project script-drift; not blocking this edit. Captured in advisory card.

---

## 2. RAS-exec — `c:/Users/daniel.kang/Desktop/Automoto/RAS-exec/.claude/settings.json`

**Changes**: (1) REMOVE stub PreToolUse hook (security theatre — `echo 'Pre-tool check passed'` provides zero gating); global hook covers it. (2) REMOVE `effortLevel: "high"` (UXL-039).

**Diff**:

```diff
 {
   "$schema": "https://json.schemastore.org/claude-code-settings.json",
-  "effortLevel": "high",
   "agent": "ras-orchestrator",
   "permissions": {
     ...
   },
-  "hooks": {
-    "PreToolUse": [
-      {
-        "matcher": "Bash",
-        "hooks": [
-          {
-            "type": "command",
-            "command": "echo 'Pre-tool check passed'"
-          }
-        ]
-      }
-    ],
-    "SessionStart": [
-      {
-        "hooks": [
-          {
-            "type": "command",
-            "command": "echo '=== RAS-exec session started ==='"
-          }
-        ]
-      }
-    ]
-  },
   "sandbox": {
     "enabled": true
   },
   "enabledPlugins": {}
 }
```

**Note on SessionStart hook**: also a stub (`echo '=== RAS-exec session started ==='`). Removed in same diff. If session-start announcement is desired, replace with meaningful behavior; otherwise let it go.

**KEEP unchanged**: `agent: ras-orchestrator` (project-specific), permissions (allow + deny), sandbox.enabled, enabledPlugins (empty `{}`).

**Side-effect**: with hooks block fully removed, the global PreToolUse Bash security gate (`~/.claude/scripts/bash-security-gate.sh`) takes over for RAS-exec sessions — net security posture INCREASES (real gate vs. echo-stub).

---

## After applying both diffs

1. JSON-validate: `python -m json.tool <path>` should exit 0
2. Quick semantic check: ensure no allow rule was inadvertently removed; the diff is purely effortLevel + hook block removal
3. Tell me ("HydroCast applied" / "RAS-exec applied" / "both applied") and I'll re-verify + finalize the advisory card cross-references
4. Skipped or unable to apply? Also fine — flag and I'll surface alternatives (e.g., `update-config` skill for assisted edit; or accept the deferred state in the advisory card)

---

## Cumulative state once these land

| File | Status | Net effect |
|---|---|---|
| Global | ✅ allowedTools removed; permissions.ask added for settings edits | Cleaner schema; structural backstop on settings edits |
| CAB | ✅ sandbox enabled + LL-13 self-deny added | Defense-in-depth aligned with global pattern |
| GTA | ✅ sandbox + baseline deny + self-deny added | Promoted from "minimally hardened" to "moderately hardened" |
| HydroCast | ⏳ pending: effortLevel removal | UXL-039 alignment |
| RAS-exec | ⏳ pending: stub hook + effortLevel removal | Security-theatre eliminated; UXL-039 alignment |

---

**This file deletes itself once both diffs land** (delete `notes/settings-hardening-pending-2026-04-30.md` after confirming both edits applied; the advisory card at `knowledge/operational-patterns/cross-project-settings-hardening.md` becomes the canonical reference going forward).
