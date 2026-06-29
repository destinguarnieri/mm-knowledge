# Worker Brief Template

Use this before handing a ticket to a coding agent.

Default storage:

- create an issue-linked Linear doc for the brief
- keep the ticket description as the stable contract
- use the brief only for execution context, not ticket restatement

## Rules

- keep it short enough to read in one pass
- define one execution slice, not the whole project
- include only the context needed for this ticket
- make the anti-goal explicit
- include a concrete stop condition so the worker knows when to ask back up
- do not dump raw research notes or long architecture essays into the brief

## Naming

`Brief: AUT-XXX <short title>`

## Template

```md
# Brief: AUT-XXX <short title>

## Objective
- The one thing this ticket should accomplish.

## Why Now
- Why this ticket matters to the current milestone proof.

## Dependency State
- Which upstream tickets or artifacts this ticket depends on.
- Whether each dependency is already landed, accepted, and marked done in the source of truth.
- Whether the worker should treat any anchor as stable, blocked, or still moving.

## Exact Scope
- The concrete slice to implement now.
- What is included.
- What is explicitly not included.

## Relevant Context
- The smallest product or architecture context needed to execute well.

## Deliverable Boundary
- The exact artifact to create or edit in this ticket.
- The path or destination the worker should treat as the primary output.
- Whether repo anchors are editable implementation surfaces or read-only analysis inputs.

## Repo Anchors
- Files, routes, symbols, tests, or docs the worker should read first.

## Concurrency Schema
- `lane`: Which execution lane this ticket belongs to.
- `parallel_after`: Which tickets must land before this can safely run, if any.
- `primary_files`: The main files or modules this worker is expected to touch.
- `lock_level`: `none`, `soft`, or `hard`.
- `merge_blocker`: Whether downstream tickets should wait for this merge.

## Constraints
- Invariants, boundaries, and implementation rules to respect.

## Semantic Invariants
- Identity semantics: what makes one record, output, or edge distinct vs deduped.
- Failure semantics: what can partially fail, and whether the path must be atomic or retry-safe.
- Recovery semantics: what state must remain valid if a later write or downstream step fails.
- Type contract: exact helper/API return shape and consumer expectations when the ticket changes typed contracts.

## Acceptance Checks
- The concrete checks that determine whether this ticket is done.

## Anti-Goal
- What this ticket must not accidentally turn into.

## Stop Condition
- When the worker should stop, narrow, or hand back instead of continuing.

## Open Questions
- Questions that are still unresolved but do not block starting.
```

## Usage Notes

- `Objective` should be singular.
- `Dependency State` should name real upstream dependencies, not implied ones. If a ticket depends on another ticket landing, the brief should say whether that dependency is already satisfied in the source of truth.
- `Exact Scope` should be executable without another planning pass.
- `Deliverable Boundary` should remove ambiguity about where the work lands. If the ticket is doc-first or contract-first, name the exact doc path and say code anchors are analysis-only unless code edits are explicitly in scope.
- `Repo Anchors` should be specific enough to reduce codebase wandering.
- `Concurrency Schema` should be concrete enough to tell whether another worker can run at the same time without fake parallelism.
- `Semantic Invariants` is mandatory for persistence, lifecycle, write-back, helper-family, orchestration, or contract-shaping tickets. If identity, dedupe, failure/retry, recovery, or type expectations are missing, the ticket is not launch-ready.
- `Acceptance Checks` should be observable, not vague.
- `Acceptance Checks` should include at least one negative-path test when the ticket touches persistence, lifecycle, write-back, helper families, or typed helper/API contracts.
- `Anti-Goal` should call out the most likely drift pattern.
- `Open Questions` must not include choices that change payload shape, artifact boundary, dependency readiness, or scope. If an unresolved question would cause a cold-start worker to invent the contract, answer it before launch instead of leaving it open.
- If the brief starts reading like a spec, it is too long.
