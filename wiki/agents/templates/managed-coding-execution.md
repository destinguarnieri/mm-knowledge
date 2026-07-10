# Managed Coding Execution

Use only when Destin explicitly requests a cold-start worker or coding-manager review. Direct execution is the default.

## Launch

Inputs: approved ticket, issue-linked brief, and named repo anchors.

Return:

```md
## Decision
- Ready, tighten, or stop.

## Evidence
- Why the brief is or is not executable without inventing scope or contracts.

## Tightening Move
- The smallest required correction, or `None`.

## Worker Prompt
- If ready, the exact prompt. Otherwise `Do not launch`.
```

Ready means the worker can identify the invocation seam, scope, acceptance checks, and all applicable identity, failure/retry, recovery, type, and negative-path contracts.

## Worker Prompt

Tell the worker:

1. Read the ticket, brief, and named anchors.
2. Implement only the brief.
3. Apply relevant repository safety and invariant rules.
4. Stop if repo reality contradicts the brief or the path expands scope.
5. Verify the changed behavior and applicable negative paths.
6. Return the handoff below.

Do not require a separate pre-coding plan unless Destin asks or the worker identifies a contract conflict.

## Optional Plan Review

When explicitly requested, return:

```md
## Decision
- Approve, tighten, or stop.

## Drift
- Scope, contract, or file-ownership mismatch, or `None`.

## Tightened Move
- The smallest correction, or `None`.
```

## Worker Handoff

```md
## Outcome
- Completed, partial, or blocked.

## Files Changed
- Paths.

## Verification
- Checks run and checks not run.

## Acceptance Blockers
- In-scope blockers, or `None`.

## Work Avoided Or Deleted
- Unnecessary scope, code, process, or abstraction avoided.
```

Do not propose follow-up tickets for non-blocking observations.

## Acceptance

Inspect the ticket, brief, handoff, actual diff, relevant surrounding code, and verification evidence.

Use one manager pass by default. Select only the applicable deep-review lenses:

- obvious behavioral bugs
- identity, persistence, lifecycle, retry, recovery, and state invariants
- material mismatch with nearby helper families or subsystem patterns

For displayed subsets, pagination, truncation, or remainder labels, verify that rendered items and reported counts use the same source, filters, and slice boundary.

Return:

```md
## Decision
- Accept, narrow, or reject.

## Brief Match
- Whether objective, scope, acceptance, and anti-goal were satisfied.

## Evidence
- Code paths, tests, and verification supporting the decision.

## Acceptance Blockers
- In-scope corrections required before acceptance, or `None`.

## Non-Blocking Observations
- Observations that create no work, or `None`.

## Commit
- Commit only when Destin explicitly authorized it for this session; otherwise `Not authorized`.
```

Accept when the brief is materially satisfied and remaining observations are non-blocking. Narrow when a contained in-scope correction remains. Reject when the implementation misses the objective or violates the anti-goal.
