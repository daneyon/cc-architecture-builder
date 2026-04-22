---
id: prioritization-frameworks
title: Prioritization Frameworks — Comparative Reference + Tiered Stack
category: reference
tags: [prioritization, rice, moscow, kano, value-effort, wsjf, ice, triage, backlog]
summary: Eight prioritization frameworks surveyed with when-wins / when-fails / data-cost evaluation, plus CAB's tiered-application stack (Value-Effort+Severity at log-time, Kano+RICE at triage, MoSCoW at promotion). Primary reference for UX-log-tracker's prioritization columns.
depends_on: []
related: [planning-implementation, product-design-cycle, ux-testing-agentic-os]
complexity: intermediate
last_updated: 2026-04-22
estimated_tokens: 3000
source: Synthesis of primary sources — McBride/Reforge (RICE), DSDM Consortium (MoSCoW), Kano (1984), SAFe (WSJF), Ellis & Brown *Hacking Growth* 2017 (ICE), Covey *7 Habits* 1989 (Eisenhower)
confidence: A
review_by: 2026-10-22
---

# Prioritization Frameworks — Comparative Reference

> CAB operational anchor for `ux-log-*.csv`'s `kano`, `rice_score`, `moscow`
> columns + `value`/`effort`/`severity` log-time fields. Also consulted by
> `planning-implementation` skill when sequencing scope. Advisory, not
> prescriptive — pick the framework whose data/context cost matches the
> decision stakes.

## TL;DR — CAB Tiered Stack

| Time in tracker lifecycle | Required / Optional | Frameworks | Columns populated |
|---|---|---|---|
| **Log time** (entry creation) | Required | Severity + Value-vs-Effort | `severity`, `value`, `effort` |
| **Triage time** (orchestrator review) | Optional where applicable | Kano (UX-surface only), RICE (when ≥3 comparable peers exist) | `kano`, `rice_score` |
| **Promotion time** (row batched into release / sprint) | Optional per-release | MoSCoW | `moscow` |

**Rationale**: log-time must be cheap (user braindump); triage time has
orchestrator attention; promotion time is a scope-bounded gate. Forcing
heavy frameworks at log time kills capture rates.

## Eight Frameworks Surveyed

| Framework | Origin | Method | Wins | Fails | Cost |
|---|---|---|---|---|---|
| **RICE** | Sean McBride, Intercom ~2018 | (Reach × Impact × Confidence) / Effort | Large backlogs needing comparative ranking; teams with historical data for impact/confidence calibration | Small backlogs (<5 items); novel domain without calibration data; GIGO if estimates fabricated | High: 4 numeric estimates per item |
| **MoSCoW** | Dai Clegg (Oracle UK → DSDM), 1994 | Must / Should / Could / Won't (scope-bounded release) | MVP scoping; release planning under fixed timeline; stakeholder alignment | As permanent row property (M/S/C/W is release-transient, not intrinsic); pure backlogs | Low: 1-of-4 pick — valid *per release only* |
| **Kano** | Noriaki Kano, 1984 | Basic / Performance / Delight classification | UX-surface where user-value curve is non-linear; reveals invisible basics | Non-UX items (infra, compliance); quantitative ranking | Med: requires user mental-model awareness |
| **Value vs. Effort (2x2)** | Generic Agile | Plot on 2x2; top-left (high value / low effort) first | Fast initial triage; resource-constrained teams | Ties within quadrants; doesn't differentiate same-quadrant items | Very low: 2 L/M/H picks |
| **WSJF** | SAFe (Dean Leffingwell, ~2011) | Cost of Delay / Job Size | Economic rationality; mature CoD estimation | CoD hard to estimate honestly; over-engineered for small teams | Very high: 4+ estimates incl. CoD |
| **ICE** | Sean Ellis / GrowthHackers ~2014 | Impact × Confidence × Ease | Growth-hacking / experimentation; simpler than RICE | Lacks Reach dimension — biases toward items affecting few users deeply | Med: 3 numeric estimates |
| **Eisenhower Matrix** | Popularized by Covey 1989; attr. Eisenhower | Urgent × Important 2x2 | Personal task management; daily/weekly triage | Feature backlogs (urgency rarely defined at feature level); team scale | Low but low-signal for product work |
| **Stack Ranking** | GE (Welch era, 1980s) | Forced-rank order 1..N | Situations demanding explicit top-N selection | Psychologically destructive at team level; no absolute value info; 17th-ranked has identical metadata to 18th | Low per-item but high cognitive overhead at full list |

## Tiered Application in Detail

### Tier 1 — Log Time: Severity + Value-vs-Effort

Every row captures at log time:
- **`severity`**: `BLOCKER` / `MAJOR` / `MINOR` / `QUESTION` / `IDEA` — impact-if-unaddressed classification
- **`value`**: L / M / H — subjective value-if-addressed
- **`effort`**: L / M / H — subjective effort-to-address

**Why both severity AND value/effort?** Severity captures
*impact-if-unaddressed*, but not *effort-to-address*. A MAJOR-severity item
that takes 2 hours is not the same as a MAJOR-severity item that takes 2
months. V/E + severity together are richer than either alone.

**Why L/M/H, not 1-10?** At log time, calibration cost of numeric scales
exceeds signal gain. L/M/H forces a 3-way decision that's fast to make and
aggregates well in triage.

### Tier 2 — Triage Time: Kano + RICE (conditional)

Orchestrator fills at triage when applicable:
- **`kano`**: `basic` / `performance` / `delight` — UX-surface rows only
- **`rice_score`**: numerical — fill when ≥3 comparable peers exist in same
  surface/category (otherwise RICE lacks comparison baseline)

**Kano — why UX-only?** Kano's three categories make sense for user-facing
experience (Must-Be for auth; Performance for response time; Delight for
onboarding touches). They don't map for infra/compliance/architecture —
forcing produces noise.

**RICE — why ≥3 peers threshold?** RICE is a *ranking* tool. With <3 peers,
there's nothing to rank against, and the score becomes a false precision
artifact. Single-item RICE is worse than no RICE.

### Tier 3 — Promotion Time: MoSCoW (per-release)

When a row is batched into an active release cycle (sprint, milestone, phase
of this plan), orchestrator assigns:
- **`moscow`**: `M` (Must) / `S` (Should) / `C` (Could) / `W` (Won't this release)

**Why promotion-only?** MoSCoW is *scope-transient* — a "Must" for Release A
may be a "Could" for Release B. Assigning at log or triage freezes the
classification against a release that doesn't yet exist. MoSCoW shines
exactly when release scope is the constraint.

## Explicitly Excluded from v1 Stack

- **WSJF** — enterprise-scale; CoD estimation overkill for CAB / small-team
  projects. Documented as option for adopters with SAFe background.
- **Eisenhower Matrix** — wrong altitude (personal-task, not product-feature
  backlog).
- **Stack Ranking** — psychologically destructive at team level; no absolute
  value info; forces ordinal comparisons where cardinal estimates are cheaper.
- **ICE** — if RICE is already available, ICE adds no unique signal. Consider
  ICE only when Reach is unmeasurable (early-stage growth experiments).

## Framework-Selection Cheat Sheet

| Situation | Use | Skip |
|---|---|---|
| Fast entry, minimal cognitive load | V/E + Severity (Tier 1) | RICE, WSJF |
| User-facing ergonomics question | Kano | WSJF, Eisenhower |
| Comparing peers in same category | RICE (≥3 peers) | Stack Ranking |
| Release-scope decision | MoSCoW | Kano (too UX-specific) |
| Personal weekly work list | Eisenhower | RICE, MoSCoW |
| Growth experiment backlog | ICE or RICE | MoSCoW, Kano |
| Large enterprise release planning | WSJF | V/E (too coarse) |

## Anti-Patterns

- **Framework-soup rows**: populating all 5 prioritization columns for every
  row kills the log-time friction budget. Tiered stack exists to prevent this.
- **Permanent MoSCoW**: assigning Must/Should/Could once and never revisiting
  — MoSCoW decays with release context. Re-evaluate per promotion cycle.
- **RICE with fabricated confidence**: if Confidence is "0.5 because I don't
  know," the resulting score is noise. Either get data or skip RICE.
- **Forcing Kano on infra rows**: a database-migration row is not basic /
  performance / delight — it's compliance or correctness. Leave Kano blank.
- **Stack-ranking full backlog**: rank-ordering 50 items consumes 50²/2
  pairwise comparisons of attention. Use RICE scores + top-N selection
  instead.

## Sources

- **RICE**: Sean McBride, Intercom engineering blog; Reforge articles
- **MoSCoW**: DSDM Consortium documentation; Agile Business Consortium
- **Kano**: Kano, N. (1984). *Attractive Quality and Must-Be Quality*.
  Journal of the Japanese Society for Quality Control, 14(2), 147–156
- **WSJF**: Scaled Agile Framework (scaledagileframework.com)
- **ICE**: Sean Ellis & Morgan Brown, *Hacking Growth* (2017), Crown Business
- **Eisenhower Matrix**: Covey, S. (1989). *The 7 Habits of Highly Effective
  People*, Free Press
- **Stack Ranking critique**: Kantor, J. & Streitfeld, D. (2015). *Inside
  Amazon: Wrestling Big Ideas in a Bruising Workplace*, NYT

## CAB-Specific Usage Guardrails

- Tracker rows SHOULD populate Tier 1 always, Tier 2 where conditions met,
  Tier 3 only when a release/sprint scopes the row in.
- `planning-implementation` skill MAY invoke this reference when sequencing
  SOW phases — apply V/E + Severity at phase level to identify minimum viable
  phase set.
- When authoring a CAB lessons-learned entry from a tracker row, the
  originating row's prioritization data becomes evidence of *priority
  stability over time* — a recurring HIGH-value / LOW-effort row becoming an
  LL is a strong promotion signal.
