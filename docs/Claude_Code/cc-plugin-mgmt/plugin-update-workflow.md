# Claude Code Plugin Update Workflow

## Quick Reference

### Check for Updates (Manual)

```bash
cd "C:\Users\daniel.kang\.claude\plugins\marketplaces\anthropic-agent-skills"
git fetch origin
git log HEAD..origin/main --oneline
```

If output shows commits: updates available
If no output: already up to date

### Apply Updates (Manual)

```bash
cd "C:\Users\daniel.kang\.claude\plugins\marketplaces\anthropic-agent-skills"
git pull origin main
```

OR use Claude Code command:
```
/plugin marketplace update anthropic-agent-skills
```

### Auto-Update Status

Verify auto-update is enabled:
```
/plugin → Marketplaces → anthropic-agent-skills → Check "Auto-update" toggle
```

**Default behavior:** Updates automatically on Claude Code startup (if enabled)

---

## Customization with Ongoing Updates

### Approach: Fork + Upstream Sync

**Workflow for maintaining custom modifications while receiving official updates:**

1. **Fork Strategy**
   - Fork https://github.com/anthropics/skills to your GitHub account
   - Clone your fork to plugins directory
   - Add official repo as upstream:
     ```bash
     git remote add upstream https://github.com/anthropics/skills.git
     git fetch upstream
     ```

2. **Periodic Sync**
   - Fetch official updates: `git fetch upstream`
   - Merge or rebase: `git rebase upstream/main`
   - Resolve conflicts if customizations overlap
   - Push to your fork: `git push origin main`

3. **Alternative: Feature Branch**
   - Keep `main` clean and tracking official repo
   - Create custom branch: `git checkout -b custom-modifications`
   - Periodically rebase onto updated `main`

### Approach: Overlay Configuration (Recommended)

**Best practice: Don't modify marketplace files directly**

- Create custom skills in separate directory: `C:\Users\daniel.kang\.claude\plugins\repos\my-custom-skills`
- Reference official skills but override with custom versions
- Official marketplace updates don't affect custom skills

**Add custom skill repository:**
```
/plugin marketplace add local:C:\Users\daniel.kang\.claude\plugins\repos\my-custom-skills
```

**Benefits:**
- Official updates seamless (no conflicts)
- Custom modifications isolated
- Can selectively override specific skills

---

## Troubleshooting

**Issue:** `git pull` fails with "divergent branches"
```bash
git fetch origin
git reset --hard origin/main  # ⚠ Discards local changes
```

**Issue:** Auto-update not working
- Check: `/plugin` → Marketplaces → Verify auto-update enabled
- Check: No local modifications blocking pull (`git status` should be clean)
- Manually trigger: `/plugin marketplace update anthropic-agent-skills`
