# Worker Handoff Template

Use this when a coding agent finishes a ticket or reaches a stop condition.

Default storage:

- post the handoff as a final Linear issue comment
- use a new durable doc only if the work produced reusable cross-ticket knowledge
- use attachments only for binaries or frozen artifacts such as screenshots or exports

## Rules

- summarize outcome, do not narrate thought process
- list concrete files changed
- say what was verified and what was not
- call out unresolved risks plainly
- recommend the next move instead of ending with a vague status note
- do not restate the full diff
- if the manager requests revisions, post a final delta handoff before the ticket is accepted

## Comment opener

`Handoff: AUT-XXX`

## Final Delta Comment opener

`Final Handoff: AUT-XXX`

## Template

```md
## Outcome
- What was completed.
- Whether the ticket fully landed, partially landed, or stopped at a blocker.

## Files Changed
- `path/to/file`
- `path/to/other-file`

## Verification
- Tests run.
- Manual checks run.
- Checks not run.

## Open Issues
- Bugs, blockers, or incomplete pieces still remaining.

## Risks
- Edge cases, regressions, or assumptions to watch.

## Next Recommended Move
- The next best follow-up ticket or immediate action.
```

## Usage Notes

- `Outcome` should make it obvious whether chief-of-staff should accept, narrow, or spin follow-up work.
- `Files Changed` should be exhaustive enough for fast review.
- `Verification` should separate completed checks from skipped checks.
- `Open Issues` should include anything that would surprise the next agent.
- `Next Recommended Move` should be one concrete move, not a menu of ideas.
- If revisions happen after the first handoff, do not leave the original comment as the last worker artifact. Add a short final delta handoff summarizing what changed since review.
