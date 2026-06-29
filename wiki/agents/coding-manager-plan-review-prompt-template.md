# Coding Manager Plan Review Prompt Template

Use this after the worker returns their 2-4 bullet execution plan and before they start coding.

Purpose:

- catch drift before implementation starts
- verify the worker interpreted the brief correctly
- tighten the move while the cost of correction is still low

## Default Inputs

- the Linear ticket
- the issue-linked brief doc
- the worker's 2-4 bullet plan
- the `coding-manager` skill

## Rule

This is a ticket-local plan check.

Do not turn it into a design session unless the worker plan clearly reveals that the brief and repo reality conflict.

## Template

```md
You are acting as the coding manager for `AUT-XXX` — `<ticket title>`.

This is a plan review, not an implementation task and not a milestone-planning task.

Your job is to review the worker's proposed 2-4 bullet execution plan before coding starts.

Before answering:

1. Read the Linear ticket description for the stable contract.
2. Read the issue-linked brief doc: `Brief: AUT-XXX <short title>`.
3. Read the worker's 2-4 bullet plan.
4. Use the `coding-manager` skill and its `Plan Review` output shape.

Review standard:

- Judge whether the worker plan matches the brief's objective and exact scope.
- Check for early drift into adjacent tickets, architecture work, or unnecessary abstraction.
- Check whether the plan is missing a critical implementation seam or verification step.
- Check whether the worker plan still respects the brief's concurrency schema and stays inside the intended file ownership.
- Do not broaden scope or redo chief-of-staff prioritization.

Return exactly:

## Plan Assessment
- Does the worker plan match the brief?

## Drift Risk
- What scope, implementation, or file-collision drift is showing up?

## Decision
- Approve, tighten, or stop.

## Tightened Move
- If tightening or stopping, what should the worker do instead?

Decision rule:

- `Approve` if the worker plan cleanly matches the brief and is narrow enough to start.
- `Tighten` if the plan is basically sound but needs one or two corrections before coding.
- `Stop` if the plan reveals a real mismatch between the brief, the ticket, and repo reality.
```

## Usage Notes

- Use this immediately after the worker sends the pre-coding plan.
- If the result is `Tighten`, send the tightened move back before implementation starts.
- If the result is `Stop`, do not let the worker improvise; return to briefing or chief-of-staff mode.
- If the worker plan expands into files or helper families owned by another active ticket, treat that as a real drift signal.
