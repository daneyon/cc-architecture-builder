---
id: marketplace
title: Distribution & Marketplace
category: distribution
tags: [marketplace, distribution, sharing, github, team]
summary: Plugin distribution patterns including local testing, GitHub publication, team configuration, and security review workflows.
depends_on: [distributable-plugin]
related: [security-defaults]
complexity: intermediate
last_updated: 2025-12-12
estimated_tokens: 650
source: https://code.claude.com/docs/en/plugins
confidence: A
review_by: 2026-03-12
---

# Distribution & Marketplace

## Overview

Claude Code plugins can be distributed through marketplaces—catalogs of available plugins that users can browse and install.

## Distribution Flow

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Development     │ ──▶ │  Local Testing   │ ──▶ │  Publication     │
│                  │     │                  │     │                  │
│  Create plugin   │     │  Local market    │     │  GitHub repo     │
│  Add components  │     │  /plugin test    │     │  Marketplace     │
│  Write docs      │     │  Iterate         │     │  Team sharing    │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

## Local Testing Workflow

### 1. Create Marketplace Structure

```bash
mkdir dev-marketplace && cd dev-marketplace
mkdir -p .claude-plugin
```

### 2. Create Marketplace Manifest

```json
// .claude-plugin/marketplace.json
{
  "name": "dev-marketplace",
  "owner": {
    "name": "Developer"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "../my-plugin",
      "description": "Plugin under development"
    }
  ]
}
```

### 3. Add and Test

```bash
claude
/plugin marketplace add ./dev-marketplace
/plugin install my-plugin@dev-marketplace
```

## GitHub Distribution

### Repository Setup

```bash
# Create PRIVATE repo by default
gh repo create my-plugin --private --source=. --push

# Only make public after security review
gh repo edit my-plugin --visibility public
```

### Marketplace Manifest

```json
// marketplace.json
{
  "name": "org-plugins",
  "owner": {
    "name": "Organization Name",
    "email": "plugins@org.com"
  },
  "plugins": [
    {
      "name": "domain-assistant",
      "source": "./plugins/domain-assistant",
      "description": "Domain-specific assistant",
      "version": "1.0.0"
    }
  ]
}
```

## Plugin Entry Schema

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Plugin identifier (kebab-case) |
| `source` | string/object | Where to fetch plugin |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Brief description |
| `version` | string | Semantic version |
| `author` | object | Author info |
| `homepage` | string | Documentation URL |
| `license` | string | SPDX identifier |
| `keywords` | array | Discovery tags |

## Source Types

### Relative Path
```json
{ "source": "./plugins/my-plugin" }
```

### GitHub Repository
```json
{
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

### Git URL
```json
{
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

## Team Configuration

### Auto-Install Plugins

Configure in `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  },
  "enabledPlugins": [
    "domain-assistant@team-tools"
  ]
}
```

### Installation Scopes

| Scope | Location | Visibility |
|-------|----------|------------|
| **local** | Project-specific | Current project |
| **project** | `.claude/plugins/` | Team via git |
| **user** | `~/.claude/plugins/` | Personal, all projects |

## Security Review Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Development    │ ──▶ │  Security       │ ──▶ │  Publication    │
│  (Private Repo) │     │  Review         │     │  (Public Repo)  │
│                 │     │                 │     │                 │
│  All work in    │     │  Run checklist  │     │  Manual release │
│  private        │     │  Remove secrets │     │  after verify   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Pre-Publication Checklist

- [ ] No API keys, tokens, or credentials
- [ ] No personal/client data in knowledge base
- [ ] `.gitignore` excludes sensitive files
- [ ] CLAUDE.md has no proprietary instructions
- [ ] All files reviewed for PII
- [ ] Dependencies audited for security
- [ ] Scripts have appropriate permissions

### Files to NEVER Commit

```
.env
*.key
*.pem
settings.local.json
CLAUDE.local.md
credentials.json
```

## CLI Commands

```bash
# Add marketplace
/plugin marketplace add owner/repo

# Browse available plugins
/plugin

# Install plugin
/plugin install plugin-name@marketplace

# List installed
/plugin list

# Remove plugin
/plugin remove plugin-name
```

## Best Practices

1. **Private by default**: Always start with private repos
2. **Version properly**: Use semantic versioning
3. **Document thoroughly**: Include README, setup guide
4. **Security review**: Run checklist before public release
5. **Test locally first**: Use local marketplace during development

## See Also

- [Security Defaults](../prerequisites/security-defaults.md)
- [Distributable Plugin Schema](../schemas/distributable-plugin.md)
- [Official Documentation](https://code.claude.com/docs/en/plugins)
