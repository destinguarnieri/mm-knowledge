# Linear Operating System

Purpose: keep Linear usable as the operating surface for Money Machine Labs across ops, dev, and future agent work.

## Core principles

1. Team = operating surface
2. Project = finite initiative with a real outcome
3. Label = classification
4. State = execution stage
5. Backlog is storage, not an action queue
6. Agents should pull from Ready, not from raw Backlog or Triage

## Current team

- Team: Money Machine (`MON`)

## Current projects

Use projects only for real initiatives.

- Trading System Reliability
- Backtesting and Evaluation
- Dashboard V2

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

### In Progress
Actively being worked.

Rule:
- keep WIP low
- target 1–3 active issues at a time across the whole system unless explicitly expanding capacity

### Blocked
Cannot move because of a dependency, missing information, or waiting event.

Rule:
- every Blocked issue must say what it is blocked on

### Done
Finished and good enough to close.

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
1. Capture new work
2. Put it in `Triage` unless it is already clear
3. Classify with labels
4. Move to `Backlog` if valid but not next
5. Move to `Ready` if actionable now

### Skip Triage only when
- the issue is already clear enough for Backlog or Ready
- Hermes is creating it from an already-structured conversation

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
- Keep total `In Progress` low
- Agents should generally pull from `Ready`
- Do not start many things to feel productive

## Operating cadence

### Daily control pass (10–15 min)
Review:
- what is In Progress
- what should move to Ready today
- what is blocked
- what should be deprioritized

Output:
- 1–3 clear active issues
- clean Ready queue
- stale items corrected

### Twice-weekly backlog grooming (15–30 min)
Review:
- Triage -> classify or kill
- Backlog -> improve labels / project placement
- split oversized issues
- promote a few items to Ready

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
- creates and normalizes issues
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
1. create or update the issue
2. classify it correctly
3. put it in Triage, Backlog, or Ready
4. keep the workspace consistent without requiring Destin to remember the taxonomy
