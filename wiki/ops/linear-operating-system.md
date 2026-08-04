# Linear Operating System

Purpose: keep Linear usable as the operating surface for Money Machine Labs across ops, dev, and future agent work.

## Core principles

1. Team = operating surface
2. Project = finite initiative with a real outcome
3. Label = classification
4. State = execution stage
5. Backlog is storage, not an action queue
6. Agents should pull from Ready, not from raw Backlog or Triage
7. Positive net realized live P&L is the objective; tickets are costs incurred only when they unblock it
8. Closing, canceling, merging, and deferring work are positive outcomes

## Current team

- Team: Money Machine (`MON`)

## Current projects

Use projects only for real initiatives.

- VWAP Mean Reversion Research — current primary revenue initiative
- Trading System Reliability
- Dashboard V2

Completed or retired research projects remain historical in Linear. Horizon programs live on the Research Board and receive a Linear project only when they become funded finite initiatives.

Anything that does not clearly belong to a finite initiative can stay outside a project.

## Workflow states

- Triage
- Backlog
- Ready
- In Progress
- Blocked
- Done
- Canceled

Notes:
- In the Linear API, `Triage` is implemented as a backlog-type state. Operationally it is still treated as Triage.
- `Ready` means actionable now.
- `Blocked` must include the blocking reason in the issue body or comments.

## State definitions

### Triage
New, unclear, partially specified, or not yet decided.

Use when:
- an item was captured quickly
- scope is fuzzy
- priority is unknown
- it needs Destin judgment before execution

### Backlog
Valid and classified work, but not selected for immediate execution.

Use when:
- the issue is real
- labels are set
- the work is understood enough to keep
- but it is not being pulled next

### Ready
Clear enough to execute now.

A Ready issue should answer:
- what is wrong / needed
- what outcome is desired
- what system it touches
- what done looks like
- which active revenue experiment it blocks
- what current-system attempt demonstrated the blocker
- why the no-build path is insufficient

### In Progress
Actively being worked.

Rule:
- keep WIP low
- keep one primary revenue outcome active unless Destin explicitly expands WIP
- allow multiple bounded execution tasks only when they serve that outcome and do not create dependency or file collisions

### Blocked
Cannot move because of a dependency, missing information, or waiting event.

Rule:
- every Blocked issue must say what it is blocked on

### Done
The requested outcome was accepted and closed. Non-blocking ideas do not keep it open and do not automatically become follow-up issues.

### Canceled
Intentionally not doing.

## Label system

Every open issue should have:
- exactly 1 `Area/*`
- exactly 1 `Type/*`
- exactly 1 `Exec/*`
- optional `Codebase/*`
- optional Project

### Area labels

Use exactly one.

- `Area/Ops`
- `Area/Dev`
- `Area/Infra`
- `Area/Research`
- `Area/Admin`

Meaning:
- Ops = operational work, deployments, production coordination
- Dev = implementation work, app changes, productized internal tooling
- Infra = reliability, data integrity, system design, platform hardening
- Research = experiments, evaluation, studies, backtests, analysis
- Admin = non-technical company process / admin work

### Type labels

Use exactly one.

- `Type/Task`
- `Type/Bug`
- `Type/Improvement`
- `Type/Automation`
- `Type/Investigation`
- `Type/Doc`

Quick guide:
- Bug = incorrect behavior
- Task = straightforward work item
- Improvement = enhancement / refactor / better architecture
- Automation = replacing manual flow with a systemized one
- Investigation = research, debugging, evaluation, fact-finding
- Doc = documentation-only work

### Exec labels

Use exactly one.

- `Exec/Agent`
- `Exec/Human`
- `Exec/Blocked`

Meaning:
- Agent = can be moved forward by Hermes or another agent with the written context
- Human = requires Destin judgment, privileged access, or manual action
- Blocked = blocked as the current execution reality

### Codebase labels

Use when the issue touches a concrete technical surface.

Current set:
- `Codebase/Trading`
- `Codebase/Quant`
- `Codebase/Frontend`
- `Codebase/System`
- `Codebase/Strategy`
- `Codebase/Data-Pipeline`
- `Codebase/Positions`
- `Codebase/Orders`

## Project rules

A project should exist only if all of these are true:
- multiple issues roll up into it
- it has a real outcome
- it has an end condition
- it is more than a category

Do not create projects just because a repo or subsystem exists.

## Intake rules

### Default intake path
1. Record a discovery on the active outcome when it affects current execution.
2. Try the current system or no-build path before proposing infrastructure.
3. Close or ignore non-blocking ideas; conversation does not imply durable work.
4. Create an issue only after the work-creation gate passes and Destin approves the tradeoff.
5. Put approved work in `Triage`, `Backlog`, or `Ready` based on its actual state.

### Skip Triage only when
- the issue is already clear enough for Backlog or Ready
- the observed blocker, revenue link, no-build alternative, and acceptance boundary are already explicit

### Work-creation gate

Apply this gate when creating an issue or expanding an issue's scope. Do not re-run it for ordinary execution inside an already approved boundary.

Before asking Destin to approve new work, present:

1. the attempted revenue experiment and observed failure
2. the causal blocker, not a hypothetical future concern
3. the no-build or manual alternative
4. the smallest fix
5. which active or queued work should be killed, merged, or deferred in exchange

If the current system has not been attempted, default to attempting it. Do not use `Critical` unless the issue names the revenue experiment that cannot proceed and shows the blocking evidence.

## Definition of Ready

An issue is Ready only if it is specific enough that the next actor does not need a fresh discovery conversation to start.

Minimum bar:
- clear title
- short problem statement
- desired outcome
- labels set correctly
- any key constraints or acceptance notes included

## WIP rules

- Prefer 1 active human-led issue at a time
- Keep one primary revenue outcome in progress unless Destin explicitly expands WIP
- Adding another primary outcome requires closing, canceling, or demoting the current one first
- Agents should generally pull from `Ready`
- Do not start many things to feel productive

## Operating cadence

### Research synchronization closeout

Research has three state layers with different jobs:

- The per-thread wiki page holds evidence, assumptions, run pointers, and interpretation.
- The Research Board holds portfolio rank, primary/challenger/parked state, and the next decisive question.
- Linear holds funded execution and backlog state.

Agents closing material research work must:

1. update the thread living head when evidence or the next experiment changes;
2. update the Research Board in the same session when validity, monetization, portfolio state, blocker, or next decisive step changes;
3. update the linked Linear item when executable scope, state, blocker, or completion changes;
4. ensure exactly one board candidate is `primary` and exactly one corresponding revenue issue is `In Progress` unless Destin explicitly expands WIP;
5. ensure parked work has a resume condition and does not remain `In Progress` in Linear;
6. reconcile mismatches before starting unrelated work: thread evidence first, Board portfolio decision second, Linear execution state third.

Do not duplicate standard backtest tables in Linear. A run ID, decision, blocker, and next action are sufficient.

### Daily control pass (10–15 min)
Review:
- what is In Progress
- what should move to Ready today
- what is blocked
- what should be deprioritized

Output:
- 1 primary revenue outcome
- clean Ready queue
- stale items corrected
- work closed, canceled, merged, or deferred

### Twice-weekly backlog grooming (15–30 min)
Review:
- Triage -> classify or kill
- Backlog -> kill, merge, defer, or justify against the current revenue path
- split only when one accepted outcome truly requires independent execution boundaries
- promote at most the next blocking issue to Ready

### Weekly planning / review (30–45 min)
Review:
- what got done
- what changed in priority
- project health
- whether current projects are still the right ones
- what the next Ready queue should be

### Monthly strategy sync
This is not a ticket cleanup meeting.
It is for:
- current system state
- architecture and operational reality
- bottlenecks
- goals for the next 30/60/90 days
- what agents should own vs what Destin should own

## Roles

### Destin
- decides priorities
- gives direction
- handles high-judgment decisions
- executes human-required work

### Hermes
- challenges whether an issue should exist before creating it
- presents the failed attempt, no-build path, smallest fix, and deletion tradeoff
- applies labels, states, and project placement
- keeps the board clean
- proposes what should be Ready / In Progress / Blocked
- helps run backlog grooming and planning review

### Future agents
- should follow this document
- should prefer `Ready`
- should not invent new taxonomy casually
- should update issue status and comments as work changes reality

## Issue creation standard

When creating an issue, default to this structure:

Title
- specific and action-oriented

Body
- Revenue experiment blocked
- Evidence from the current-system attempt
- No-build alternative
- Problem
- Goal
- Constraints / notes
- What done looks like

Then set:
- state
- project if applicable
- `Area/*`
- `Type/*`
- `Exec/*`
- optional `Codebase/*`

## Heuristics

Use `Triage` when:
- the title is too vague on its own
- the issue implies design work before implementation
- priority is unknown

Use `Backlog` when:
- the issue is understood but not selected

Use `Ready` when:
- a competent person or agent could start now

Use `Exec/Human` when:
- it needs Destin judgment
- it affects production manually
- it involves ambiguous strategic choice

Use `Exec/Agent` when:
- a bounded next step is obvious from the issue

## Current practical rule

If a new task comes up in conversation, Hermes should:
1. test whether it blocks the active revenue outcome
2. update the active issue when it is execution context, not separate work
3. default to no ticket for hypothetical, non-blocking, duplicate, or merely attractive work
4. ask for issue approval only with the work-creation-gate evidence and deletion tradeoff
5. classify approved work without requiring Destin to manage the taxonomy
