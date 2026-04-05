---
id: security-defaults
title: Security Defaults
category: prerequisites
tags: [security, privacy, credentials, publication, checklist]
summary: Security best practices for Claude Code projects including private repository defaults, credential handling, and pre-publication review checklist.
depends_on: [git-foundation]
related: [marketplace, distributable-plugin]
complexity: foundational
last_updated: 2025-12-12
estimated_tokens: 500
source: synthesized
confidence: A
review_by: 2026-03-12
---

# Security Defaults

## Private by Default

**Critical Rule**: All repositories should be created as **private by default** during development.

```bash
# Create private repository (GitHub CLI)
gh repo create my-project --private --source=. --push

# NEVER create public repositories directly
# Only make public after security review
gh repo edit my-project --visibility public
```

## Pre-Publication Checklist

Before making any repository public or sharing with others:

| Check | Action | Status |
|-------|--------|--------|
| **Credentials** | Search for API keys, tokens, passwords | ☐ |
| **Environment files** | Ensure .env files are gitignored | ☐ |
| **Personal data** | Remove PII from knowledge base | ☐ |
| **Proprietary content** | Review CLAUDE.md for confidential instructions | ☐ |
| **Client data** | Remove any client-specific information | ☐ |
| **File history** | Check git history for accidentally committed secrets | ☐ |
| **Dependencies** | Audit MCP servers and scripts | ☐ |
| **Permissions** | Verify scripts don't have excessive permissions | ☐ |

## Files That Should NEVER Be Committed

```
# Environment variables
.env
.env.local
.env.*.local

# Cryptographic keys
*.key
*.pem
*.p12
*.pfx

# Credentials
credentials.json
secrets.json
*.token
.github_token
.anthropic_key

# Local overrides
settings.local.json
CLAUDE.local.md

# Database files (may contain sensitive data)
*.db
*.sqlite
```

## Credential Handling

### For MCP Servers

Use environment variables, never hardcode:

```json
// GOOD: Reference environment variable
{
  "mcpServers": {
    "github": {
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    }
  }
}

// BAD: Hardcoded token
{
  "mcpServers": {
    "github": {
      "headers": {
        "Authorization": "Bearer ghp_xxxxxxxxxxxx"
      }
    }
  }
}
```

### For Knowledge Base

Never include in knowledge files:
- API keys or tokens
- Database connection strings
- Password examples (even "example" ones)
- Internal URLs or IP addresses
- Client names or project codenames

## Security Review Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Development    │ ──▶ │  Security       │ ──▶ │  Publication    │
│  (Private Repo) │     │  Review         │     │  (Public Repo)  │
│                 │     │                 │     │                 │
│  All work done  │     │  Run checklist  │     │  Manual release │
│  in private     │     │  Remove secrets │     │  only after     │
│                 │     │  Audit content  │     │  verification   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Team Distribution Alternative

For team/organization distribution, consider keeping repositories private permanently:

- Use GitHub team access controls
- Share via private marketplace
- Avoid public publication entirely for internal tools

## If Secrets Were Accidentally Committed

1. **Rotate the credential immediately** — Assume it's compromised
2. **Remove from history** — Use `git filter-branch` or BFG Repo-Cleaner
3. **Force push** — Update remote with cleaned history
4. **Notify team** — Ensure everyone pulls fresh

```bash
# Using BFG Repo-Cleaner (simpler than filter-branch)
bfg --delete-files credentials.json
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

## See Also

- [Git Foundation](git-foundation.md) — Repository setup
- [Marketplace](../distribution/marketplace.md) — Distribution security
