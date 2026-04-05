---
id: product-design-cycle
title: Product Design Cycle — Universal Reference
category: reference
tags: [lifecycle, phases, deliverables, methodology, design-thinking, sdlc, lean]
summary: Generalized product/app engineering lifecycle (7 phases) with sub-processes, deliverables, and discipline mapping. Framework-agnostic synthesis of Double Diamond, SDLC, Lean Startup, Design Thinking, and Stage-Gate.
depends_on: []
related: [planning-implementation, executing-tasks]
complexity: foundational
last_updated: 2026-03-15
estimated_tokens: 1500
source: CAB-original
confidence: A
review_by: 2026-06-15
---

# Product Design Cycle: Universal Reference

**Purpose**: Generalized product/app engineering lifecycle phases with sub-processes, deliverables, and discipline mapping. Framework-agnostic synthesis of Double Diamond, SDLC, Lean Startup, Design Thinking, and Stage-Gate methodologies.

---

## Lifecycle Overview

```
Phase 0        Phase 1          Phase 2            Phase 3           Phase 4           Phase 5          Phase 6
INITIATION --> STRATEGY   -->   ARCHITECTURE  -->  IMPLEMENTATION -> VALIDATION   -->  DEPLOYMENT  -->  OPERATIONS
& DISCOVERY    & DEFINITION     & DESIGN           & BUILD           & QUALITY         & LAUNCH         & GROWTH
                                                                                                         |
                                                                                                         v
                                                                                                    [ITERATE]
                                                                                                    back to any
                                                                                                    prior phase
```

---

## Phase 0: Initiation & Discovery

**Objective**: Validate that a problem worth solving exists and is feasible to pursue.

### Sub-Processes

| # | Activity | Description | Key Deliverable(s) |
|---|----------|-------------|---------------------|
| 0.1 | Problem Identification | Frame the core problem/opportunity in measurable terms | Problem Statement |
| 0.2 | Stakeholder Mapping | Identify all parties affected by or influencing the solution | Stakeholder Register |
| 0.3 | Market & Competitive Landscape | Analyze existing solutions, gaps, and positioning opportunities | Competitive Analysis |
| 0.4 | User Discovery | Preliminary user interviews, surveys, or data analysis | User Insights Summary |
| 0.5 | Feasibility Assessment | Evaluate technical, business, and operational feasibility | Feasibility Report (T/B/O) |
| 0.6 | Scope & Charter | Define project boundaries, constraints, success criteria | SOW / Project Charter |

### Disciplines Involved

| Discipline | Role in This Phase |
|---|---|
| Business Leadership | Vision, funding approval, strategic alignment |
| Product Management | Problem framing, stakeholder coordination, scope definition |
| Business Analysis | Requirements elicitation, feasibility modeling |
| Strategy / Advisory | Market positioning, competitive differentiation |
| UX Research | Preliminary user discovery, empathy mapping |
| Engineering (Advisory) | Technical feasibility assessment |

---

## Phase 1: Strategy & Definition

**Objective**: Define WHAT to build, for WHOM, and WHY it will succeed.

### Sub-Processes

| # | Activity | Description | Key Deliverable(s) |
|---|----------|-------------|---------------------|
| 1.1 | Product Vision & Strategy | Articulate the long-term product direction and differentiators | Product Vision Document |
| 1.2 | User Research & Personas | Deep user research, persona creation, journey mapping | Personas, Journey Maps |
| 1.3 | Requirements Analysis | Functional & non-functional requirements, user stories, acceptance criteria | PRD (Product Requirements Doc) |
| 1.4 | Business Model & Value Proposition | Revenue model, pricing strategy, value proposition canvas | Business Model Canvas |
| 1.5 | Success Metrics & KPIs | Define measurable outcomes for each stakeholder group | KPI Framework |
| 1.6 | Risk Assessment & Mitigation | Identify risks (technical, market, operational) and mitigation strategies | Risk Register |
| 1.7 | Roadmap & Prioritization | Feature prioritization (RICE, MoSCoW, Kano) and phased delivery plan | Product Roadmap |
| 1.8 | Go-to-Market Strategy | Positioning, messaging, channel strategy, launch planning | GTM Brief |

### Disciplines Involved

| Discipline | Role in This Phase |
|---|---|
| Product Management | Requirements, roadmap, prioritization, PRD ownership |
| UX Research | User research, persona development, usability benchmarking |
| Business Analysis | Requirements modeling, process mapping, gap analysis |
| Strategy / Advisory | Business model, competitive positioning, risk framing |
| Product Marketing | GTM strategy, positioning, messaging, audience segmentation |
| Engineering (Advisory) | Technical constraints, effort estimation, dependency mapping |
| Project Management | Timeline, resource planning, dependency tracking |

---

## Phase 2: Architecture & Design

**Objective**: Define HOW to build it -- system structure, data flows, interfaces, and user experience.

### Sub-Processes

| # | Activity | Description | Key Deliverable(s) |
|---|----------|-------------|---------------------|
| 2.1 | System Architecture | High-level system design, component decomposition, technology selection | Architecture Decision Records (ADR), System Diagram |
| 2.2 | Data Modeling & Schema Design | Entity relationships, data flow, storage strategy, migration planning | ERD, Data Dictionary |
| 2.3 | API & Integration Design | Interface contracts, authentication, versioning, third-party integrations | API Specification (OpenAPI/Swagger) |
| 2.4 | UI/UX Design: Information Architecture | Navigation structure, content hierarchy, user flow diagrams | Sitemap, User Flows |
| 2.5 | UI/UX Design: Wireframing | Low-fidelity layouts, interaction patterns, responsive breakpoints | Wireframes |
| 2.6 | UI/UX Design: Visual Design | High-fidelity mockups, design system, component library | Design System, UI Kit |
| 2.7 | UI/UX Design: Prototyping | Interactive prototypes for validation and usability testing | Clickable Prototype |
| 2.8 | Security Architecture | Threat modeling, authentication/authorization design, compliance mapping | Threat Model, Security Spec |
| 2.9 | Infrastructure & Deployment Design | Environment strategy, CI/CD pipeline design, scaling approach | Infrastructure Diagram, SRD |
| 2.10 | Technical Specification | Detailed implementation spec bridging design to code | SRD (System Requirements Doc) |

### Disciplines Involved

| Discipline | Role in This Phase |
|---|---|
| Software Architecture / Tech Lead | System design, ADRs, technology selection |
| UX Designer | Information architecture, wireframes, user flows |
| UI Designer | Visual design, design system, high-fidelity mockups |
| Interaction Designer | Prototyping, micro-interactions, animations |
| Backend Engineering | API design, data modeling, system component design |
| Frontend Engineering | Component architecture, responsive strategy |
| Database Engineering | Schema design, query optimization strategy, migration planning |
| Security Engineering | Threat modeling, auth design, compliance |
| DevOps / SRE | Infrastructure design, CI/CD planning, environment strategy |
| Product Management | Design review, requirement validation, trade-off decisions |

---

## Phase 3: Implementation & Build

**Objective**: Translate designs into working, tested code through iterative development.

### Sub-Processes

| # | Activity | Description | Key Deliverable(s) |
|---|----------|-------------|---------------------|
| 3.1 | Sprint / Iteration Planning | Break features into tasks, estimate effort, assign work | Sprint Backlog |
| 3.2 | Environment Setup | Development, staging, production environments; toolchain configuration | Dev Environment, CI/CD Pipeline |
| 3.3 | Frontend Development | UI implementation, client-side logic, state management, responsive design | Frontend Codebase |
| 3.4 | Backend Development | Server-side logic, APIs, business rules, service layer | Backend Codebase |
| 3.5 | Database Implementation | Schema creation, migrations, seed data, query optimization | Database, Migration Scripts |
| 3.6 | Integration Development | Third-party APIs, microservice communication, data pipelines | Integration Layer |
| 3.7 | DevOps & CI/CD | Build automation, test automation, deployment pipelines, containerization | Pipeline Configuration |
| 3.8 | Code Review & Standards | Peer review, linting, style enforcement, documentation | Reviewed, Merged Code |
| 3.9 | Technical Documentation | API docs, architecture docs, inline documentation, developer guides | Technical Docs |

### Disciplines Involved

| Discipline | Role in This Phase |
|---|---|
| Frontend Engineering | UI implementation, client logic, component development |
| Backend Engineering | API implementation, business logic, service layer |
| Full-Stack Engineering | End-to-end feature implementation |
| Database Engineering | Schema implementation, migrations, query tuning |
| DevOps / SRE | CI/CD, containerization, infrastructure provisioning |
| Tech Lead | Code review, architectural guidance, technical decisions |
| QA Engineering (Embedded) | Test-driven development support, early testing |
| Technical Writing | Documentation, API reference generation |
| Project Management | Sprint tracking, impediment removal, progress reporting |

---

## Phase 4: Validation & Quality

**Objective**: Verify the product meets requirements, performs correctly, and satisfies users.

### Sub-Processes

| # | Activity | Description | Key Deliverable(s) |
|---|----------|-------------|---------------------|
| 4.1 | Test Strategy & Planning | Define testing scope, approach, tools, environments, entry/exit criteria | Test Plan |
| 4.2 | Unit Testing | Individual component/function validation | Unit Test Suite, Coverage Report |
| 4.3 | Integration Testing | Component interaction validation, API contract testing | Integration Test Suite |
| 4.4 | End-to-End Testing | Full user flow validation across system boundaries | E2E Test Suite |
| 4.5 | Regression Testing | Verify existing functionality is not broken by changes | Regression Suite |
| 4.6 | Performance & Load Testing | Response times, throughput, scalability under load | Performance Report, Benchmarks |
| 4.7 | Security Testing & Audit | Vulnerability scanning, penetration testing, OWASP compliance | Security Audit Report |
| 4.8 | Accessibility Testing | WCAG compliance, assistive technology compatibility | Accessibility Report |
| 4.9 | User Acceptance Testing (UAT) | Stakeholder/end-user validation against acceptance criteria | UAT Sign-off |
| 4.10 | Bug Triage & Resolution | Categorize, prioritize, and resolve defects | Bug Tracker, Resolution Log |

### Disciplines Involved

| Discipline | Role in This Phase |
|---|---|
| QA Lead | Test strategy, test plan ownership, quality standards |
| QA Engineering | Test execution, automation, regression |
| Performance Engineering | Load testing, bottleneck analysis, optimization |
| Security Engineering | Vulnerability assessment, penetration testing |
| UX Research | Usability testing, accessibility review |
| Product Owner | UAT coordination, acceptance sign-off |
| Engineering (All) | Bug resolution, performance fixes |

---

## Phase 5: Deployment & Launch

**Objective**: Release the product to users safely and communicate its availability effectively.

### Sub-Processes

| # | Activity | Description | Key Deliverable(s) |
|---|----------|-------------|---------------------|
| 5.1 | Pre-Production Validation | Staging environment smoke tests, data migration dry runs | Staging Validation Report |
| 5.2 | Deployment Execution | Production release via automated pipeline, database migrations | Deployed Application |
| 5.3 | Rollback Planning | Defined rollback procedures, canary/blue-green deployment strategy | Rollback Playbook |
| 5.4 | Monitoring & Alerting Setup | Application monitoring, infrastructure monitoring, log aggregation | Monitoring Dashboard |
| 5.5 | Launch Communication | Internal announcements, external marketing, press, social | Launch Communications |
| 5.6 | User Documentation & Training | User guides, onboarding flows, help center articles, training sessions | User Documentation |
| 5.7 | Post-Launch Stabilization | Hotfix readiness, war room, rapid response for launch issues | Incident Response Plan |

### Disciplines Involved

| Discipline | Role in This Phase |
|---|---|
| DevOps / SRE | Deployment execution, monitoring, rollback |
| Engineering (All) | Hotfix readiness, post-launch stabilization |
| Product Marketing | Launch communications, external messaging |
| Technical Writing | User documentation, help center |
| Project Management | Launch coordination, timeline management |
| Customer Support | User onboarding, feedback triage |
| Product Management | Launch criteria validation, stakeholder communication |

---

## Phase 6: Operations & Growth

**Objective**: Sustain, optimize, and evolve the product based on real-world usage and feedback.

### Sub-Processes

| # | Activity | Description | Key Deliverable(s) |
|---|----------|-------------|---------------------|
| 6.1 | Production Monitoring | Uptime, error rates, performance baselines, SLA tracking | Operational Dashboard |
| 6.2 | Incident Response & Debugging | Root cause analysis, incident management, post-mortems | Incident Reports, RCA |
| 6.3 | Performance Optimization | Profiling, query optimization, caching, CDN tuning | Performance Improvement Log |
| 6.4 | Analytics & Insights | Usage metrics, funnel analysis, cohort analysis, A/B testing | Analytics Dashboard, Insights Report |
| 6.5 | User Feedback Collection | In-app feedback, surveys, support tickets, NPS tracking | Feedback Synthesis |
| 6.6 | Feature Iteration & Enhancement | Prioritize improvements, build next iteration, deploy | Updated Roadmap, Release Notes |
| 6.7 | Technical Debt Management | Refactoring, dependency updates, architecture evolution | Tech Debt Register |
| 6.8 | Retrospectives & Process Improvement | Team retrospectives, process refinement, tooling improvements | Process Improvement Log |
| 6.9 | Scaling & Infrastructure Evolution | Capacity planning, horizontal/vertical scaling, cost optimization | Scaling Plan |

### Disciplines Involved

| Discipline | Role in This Phase |
|---|---|
| DevOps / SRE | Monitoring, incident response, scaling |
| Engineering (All) | Bug fixes, performance optimization, feature iteration |
| Data Analysis | Analytics, metrics, insights, A/B testing |
| Product Management | Roadmap updates, feature prioritization, retrospectives |
| Customer Support | Feedback collection, issue triage |
| Business Leadership | Strategic review, resource allocation |

---

## Cross-Phase Discipline Participation Matrix

Shows which disciplines are active (A), advisory (a), or not involved (-) in each phase:

| Discipline | Ph0 | Ph1 | Ph2 | Ph3 | Ph4 | Ph5 | Ph6 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Business Leadership | A | A | a | - | - | a | A |
| Product Management | A | A | A | a | A | A | A |
| Business Analysis | A | A | a | - | - | - | a |
| Strategy / Advisory | A | A | a | - | - | - | a |
| Product Marketing | - | A | - | - | - | A | a |
| UX Research | a | A | A | - | a | - | a |
| UX Designer | - | a | A | a | - | - | - |
| UI Designer | - | - | A | a | - | - | - |
| Interaction Designer | - | - | A | a | - | - | - |
| Software Architect / Tech Lead | a | a | A | A | a | a | A |
| Frontend Engineering | - | - | A | A | A | a | A |
| Backend Engineering | - | - | A | A | A | a | A |
| Full-Stack Engineering | - | - | A | A | A | a | A |
| Database Engineering | - | - | A | A | a | a | A |
| Security Engineering | - | - | A | a | A | a | a |
| DevOps / SRE | - | - | A | A | a | A | A |
| QA Lead | - | - | a | a | A | a | a |
| QA Engineering | - | - | - | a | A | a | a |
| Performance Engineering | - | - | a | - | A | a | A |
| Project Management | a | A | a | A | a | A | a |
| Technical Writing | - | - | - | A | - | A | a |
| Data Analysis | - | a | - | - | - | - | A |
| Customer Support | - | - | - | - | a | A | A |

`A` = Active participant, `a` = Advisory/supporting, `-` = Not involved

---

## Phase Transition Gates

Each phase transition has explicit criteria before proceeding:

| Transition | Gate Criteria |
|---|---|
| Ph0 -> Ph1 | Problem validated, feasibility confirmed, charter approved |
| Ph1 -> Ph2 | PRD approved, KPIs defined, roadmap prioritized, risks accepted |
| Ph2 -> Ph3 | Architecture reviewed, designs approved, SRD complete, security reviewed |
| Ph3 -> Ph4 | Feature-complete per sprint scope, code reviewed, CI green |
| Ph4 -> Ph5 | All critical/high bugs resolved, UAT signed off, performance acceptable |
| Ph5 -> Ph6 | Deployment successful, monitoring active, rollback tested, launch communicated |
| Ph6 -> Ph0/1 | Iteration trigger: user feedback, metric threshold, strategic pivot |

---

## Deliverable Taxonomy (Quick Reference)

| Abbreviation | Full Name | Phase(s) | Owner |
|---|---|---|---|
| SOW | Statement of Work | 0 | Business / PM |
| PRD | Product Requirements Document | 1 | Product Management |
| BRD | Business Requirements Document | 0-1 | Business Analysis |
| FRD | Functional Requirements Document | 1-2 | Business Analysis / PM |
| SRD | System Requirements Document | 2 | Engineering / Architect |
| ADR | Architecture Decision Record | 2+ | Architect / Tech Lead |
| ERD | Entity-Relationship Diagram | 2 | Database Engineering |
| GTM | Go-to-Market (Brief/Plan) | 1, 5 | Product Marketing |
| MRD | Market Requirements Document | 1 | Product Marketing |
| RCA | Root Cause Analysis | 6 | Engineering |

---

## Mapping to Claude Code Components (Generalized)

| Lifecycle Concern | CC Component Type | Rationale |
|---|---|---|
| Phase knowledge ("how to execute Phase X") | Skill | Procedural, on-demand, reusable |
| Role expertise ("think like a PM/architect") | Agent | Sustained focus, persona-driven |
| Quality standards ("always check for X") | Rules | Always-on, behavioral |
| Phase transitions ("run launch checklist") | Command | User-triggered workflow shortcut |
| External tool integration (Jira, CI/CD, etc.) | MCP | Service connector |
| Deliverable templates (PRD, SRD, etc.) | Skill assets/ | Output resources, not loaded into context |
| Domain knowledge (industry standards, etc.) | Skill references/ | On-demand context loading |
| Cross-session state (project progress, etc.) | Memory (filesystem) | Persistent state management |
