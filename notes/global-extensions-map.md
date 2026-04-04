# Global CC Extensions Map

**Snapshot date**: 2026-04-04
**Source**: `~/.claude/` (C:\Users\daniel.kang\.claude\)

---

## Custom Extensions (direct in ~/.claude/)

### Agents (5)

| Agent | Model | Purpose |
|-------|-------|---------|
| `orchestrator.md` | opus | Central task router, PLAN->VERIFY->COMMIT enforcement |
| `verifier.md` | inherit | End-to-end verification, adversarial challenge |
| `code-reviewer.md` | inherit | Code quality, security, maintainability review |
| `debugger-specialist.md` | inherit | Token-efficient debugging, root cause analysis |
| `general-researcher.md` | inherit | Cross-domain research, technology evaluation |

### Skills (11)

| Skill | Summary |
|-------|---------|
| `architecture-analyzer` | Codebase analysis, system architecture design, ADRs |
| `assessing-quality` | Testing strategies, quality frameworks, acceptance criteria |
| `claude-docs-helper` | Fetch/search official CC docs from docs.claude.com |
| `designing-workflows` | Process flows, automation pipelines, orchestration patterns |
| `planning-implementation` | Project scoping, phased deliverables, SOW generation |
| `presentation-outline` | Structured outline with timing and visual strategy |
| `readme-generator` | Python project README documentation |
| `slide-designer` | HTML presentations, PowerPoint conversion |
| `strategy-framework` | References-only (no SKILL.md) — may be incomplete |
| `token-optimizer` | Token-efficient interaction for large Python scripts |
| `visualizing-data` | Diagram selection, Mermaid/ASCII/HTML rendering |

### Commands (6)

| Command | Description |
|---------|-------------|
| `commit-push-pr` | Stage, commit, push, create PR in one workflow |
| `context-sync` | Pull git log, PRs, issues into session context summary |
| `execute-task` | Standard PLAN->REVIEW->EXECUTE->VERIFY->COMMIT protocol |
| `init-plugin` | Initialize new CAB plugin with git setup |
| `init-worktree` | Set up git worktrees for parallel agent execution |
| `techdebt` | Scan for tech debt, duplication, stale TODOs |

### Rules (7)

| Path | Category |
|------|----------|
| `rules/comm/interaction.md` | Communication & interaction standards |
| `rules/dev/ai-system-design.md` | AI system design & responsible AI |
| `rules/dev/comments.md` | Comments policy |
| `rules/dev/philosophy.md` | Development philosophy |
| `rules/dev/practices.md` | Development practices |
| `rules/dev/token-efficiency.md` | Token efficiency & context management |
| `rules/process/analysis-framework.md` | Strategic analysis & orchestration |

---

## Settings (key config)

- **effortLevel**: `max`
- **agent**: `orchestrator`
- **subagentModel**: `opus`
- **respectGitignore**: `true`
- **Hooks**: PostToolUse on Write|Edit -> `ruff format $CLAUDE_FILE_PATH`
- **Status line**: `claude-hud` plugin
- **Custom marketplaces**: `cab` (daneyon/cc-architecture-builder), `strategy-pathfinder` (daneyon/strategy-pathfinder)
- **Telemetry**: disabled

---

## Enabled Plugins (40) — with Internal Extensions

### anthropic-agent-skills (2 plugins: document-skills, claude-api)

**Skills (17)**: algorithmic-art, brand-guidelines, canvas-design, claude-api, doc-coauthoring, docx, frontend-design, internal-comms, mcp-builder, pdf, pptx, skill-creator, slack-gif-creator, theme-factory, web-artifacts-builder, webapp-testing, xlsx

### cab (custom marketplace)

- **Agents (4)**: architecture-advisor, orchestrator, project-integrator, verifier
- **Commands (14)**: add-agent, add-command, add-skill, commit-push-pr, context-sync, execute-task, init-plugin, init-worktree, integrate-existing, kb-index, new-global, new-project, techdebt, validate
- **Skills (5)**: creating-components, executing-tasks, quick-scaffold, scaffolding-projects, validating-structure

### claude-hud

- **Commands (2)**: configure, setup

### code-review

- **Commands (1)**: code-review

### code-simplifier

- **Agents (1)**: code-simplifier

### hookify

- **Agents (1)**: conversation-analyzer
- **Commands (4)**: configure, help, hookify, list
- **Skills (1)**: writing-rules

### frontend-design

- **Skills (1)**: frontend-design

### claude-md-management

- **Commands (1)**: revise-claude-md
- **Skills (1)**: claude-md-improver

### skill-creator

- **Skills (1)**: skill-creator

### playground

- **Skills (1)**: playground

### firecrawl

- **Commands (1)**: skill-gen
- **Skills (1)**: firecrawl-cli

### chrome-devtools-mcp

- **Skills (4)**: a11y-debugging, chrome-devtools, debug-optimize-lcp, troubleshooting

### discord

- **Skills (2)**: access, configure

### microsoft-docs

- **Skills (3)**: microsoft-code-reference, microsoft-docs, microsoft-skill-creator

### atomic-agents

- **Skills (1)**: release

### remember

- **Skills (1)**: remember

### mcp-server-dev

- **Skills (3)**: build-mcp-app, build-mcp-server, build-mcpb

### product-tracking-skills

- **Agents (1)**: tracking-watchdog
- **Skills (7)**: product-tracking-audit-current-tracking, product-tracking-business-case, product-tracking-design-tracking-plan, product-tracking-generate-implementation-guide, product-tracking-implement-tracking, product-tracking-instrument-new-feature, product-tracking-model-product

### aws-serverless

- **Skills (4)**: api-gateway, aws-lambda, aws-lambda-durable-functions, aws-serverless-deployment

### deploy-on-aws

- **Skills (1)**: deploy

### data (Astronomer)

- **Skills (30)**: airflow, airflow-hitl, analyzing-data, annotating-task-lineage, authoring-dags, checking-freshness, cosmos-dbt-core, cosmos-dbt-fusion, creating-openlineage-extractors, debugging-dags, deploying-airflow, managing-astro-deployments, managing-astro-local-env, migrating-airflow-2-to-3, profiling-tables, setting-up-astro-project, testing-dags, tracing-downstream-lineage, tracing-upstream-lineage, troubleshooting-astro-deployments, warehouse-init, +9 dbt-specific

### sourcegraph

- **Commands (2)**: sg-file, sg-search
- **Skills (1)**: searching-sourcegraph

### postman

- **Agents (1)**: readiness-analyzer (API Readiness Analyzer)
- **Commands (8)**: codegen, docs, mock, search, security, setup, sync, test
- **Skills (3)**: agent-ready-apis, postman-knowledge, postman-routing

### coderabbit

- **Agents (1)**: code-reviewer
- **Commands (1)**: review
- **Skills (2)**: autofix, code-review

### huggingface-skills

- **Agents (1)**: AGENTS
- **Skills (12)**: hf-cli, huggingface-community-evals, huggingface-datasets, huggingface-gradio, huggingface-jobs, huggingface-llm-trainer, huggingface-paper-publisher, huggingface-papers, huggingface-tool-builder, huggingface-trackio, huggingface-vision-trainer, transformers-js

### sentry

- **Commands (1)**: seer
- **Skills (20)**: sentry-android-sdk, sentry-browser-sdk, sentry-cloudflare-sdk, sentry-cocoa-sdk, sentry-code-review, sentry-create-alert, sentry-dotnet-sdk, sentry-elixir-sdk, sentry-feature-setup, sentry-fix-issues, sentry-flutter-sdk, sentry-go-sdk, sentry-nestjs-sdk, sentry-nextjs-sdk, sentry-node-sdk, sentry-otel-exporter-setup, sentry-php-sdk, sentry-pr-code-review, sentry-python-sdk, sentry-react-native-sdk

### context-engineering-marketplace (5 plugins, shared skill set)

Plugins: agent-architecture, agent-development, agent-evaluation, cognitive-architecture, context-engineering-fundamentals
**Skills (12 each)**: advanced-evaluation, bdi-mental-states, context-compression, context-degradation, context-fundamentals, context-optimization, evaluation, filesystem-context, memory-systems, multi-agent-patterns, project-development, tool-design

### ralph-wiggum-marketer

- **Commands (4)**: ralph-cancel, ralph-init, ralph-marketer, ralph-status
- **Skills (1)**: copywriter

### strategy-pathfinder (custom marketplace)

- **Agents (5)**: competitive-analyst, implementation-planner, philosophical-advisor, scenario-analyst, spf-advisor
- **Commands (6)**: apply-framework, benchmark-decision, diagnose-risk, full-strategic-assessment, merge-guidebook, strategic-scan
- **Skills (6)**: competitive-intelligence, implementation-planning, merge-guidebook, scenario-planning, strategic-analysis, strategic-orchestration

### Behavior/style-only plugins (no filesystem extensions)

security-guidance, explanatory-output-style, learning-output-style, context7, fakechat, playwright

---

## Disabled Plugins (18)

github, vercel, pr-review-toolkit, agent-sdk-dev, commit-commands, feature-dev, greptile, example-skills, ralph-loop, clangd-lsp, serena, typescript-lsp, pyright-lsp, rust-analyzer-lsp, csharp-lsp, jdtls-lsp, superpowers, claude-code-setup, plugin-dev

---

## Totals

| Category | Count |
|----------|-------|
| Global agents | 5 |
| Global skills | 11 |
| Global commands | 6 |
| Global rules | 7 |
| Enabled plugins | 40 |
| Plugin-provided skills (deduplicated) | ~130 |
| Plugin-provided agents | ~15 |
| Plugin-provided commands | ~45 |
| Custom marketplaces | 2 |
