# Coding Manager Review Checklist

Use this during coding-manager acceptance review.

Purpose:

- make the coding manager behave like a senior reviewer instead of a superficial approver
- catch silent invariant bugs
- catch logic-cohesion issues before they accumulate across agent-written changes

## Core Review Standard

The coding manager is not only checking:

- "does this compile?"
- "did tests pass?"
- "does the worker sound confident?"

The coding manager must also check:

- obvious bugs
- invariant bugs
- logic cohesion with nearby code

## Review Passes

### 1. Obvious Bug Pass

Check for:

- incorrect conditionals
- wrong lookups or missing filters
- missing null/empty handling
- mismatched route validation and persistence behavior
- unhandled failure paths
- off-by-one, limit/slice, truncation, or pagination math
- displayed-subset vs reported-remainder mismatches such as `+N more` summaries that do not use the same boundary as the rendered slice
- invalid or filtered items that are skipped in rendering but still distort totals, remainder counts, or summary text
- tests that miss the main changed branch

### 2. Invariant Audit

Run this whenever the ticket touches persistence, graph edges, registry helpers, route-to-DB behavior, lifecycle semantics, or state transitions.

Ask:

1. What is the semantic identity of this record or relationship?
2. Do `resolve` / `ensure` / `create` / `update` / `delete` helpers use the same identity fields?
3. Does the schema allow states or duplicates that the code is pretending cannot happen?
4. Are there optional fields like `source`, `status`, `scope`, or ownership fields that are actually part of semantic uniqueness?
5. If an edge or row is removed or reconciled, could nearby helpers accidentally remove the wrong thing?
6. If the code renders a limited subset plus a remainder/overflow summary, do both numbers come from the same source list, filter rules, and slice boundary?

Common danger pattern:

- a field is accepted or written on create
- but ignored on resolve, ensure, update, or delete

That is a classic invariant bug and must be called out.

Additional danger pattern:

- a helper displays one subset of items
- but computes the total, remainder, or `+N more` text from successful renders instead of the actual slice boundary

That is a display/accounting invariant bug and must be called out.

### 3. Logic Cohesion Pass

Ask:

- why is this implemented this way when nearby code does it a different way?
- is this change consistent with adjacent helper families and route patterns?
- does this ticket introduce a one-off abstraction or exception where the existing code already has a pattern?
- does the worker's implementation preserve the codebase's internal logic, or does it make the system sloppier?

If a helper family exists, review the family, not just one function.

Examples:

- `resolveX`, `ensureX`, `createX`, `deleteX`
- route + registry + schema + tests for the same concept
- write path + read path + retirement path for the same state

## Decision Rule

- `Accept` only if the implementation survives all relevant passes.
- `Narrow` if the implementation mostly landed but an in-scope correction is still required.
- `Reject` if the ticket missed a core invariant or introduced a meaningful logic bug.
- `Follow-up` only when the landed ticket is still valid but revealed a separate next ticket.

## Anti-Pattern

Do not approve work with language like:

- "looks good"
- "no obvious bugs"
- "tests pass so this is fine"

Those are insufficient acceptance standards for agent-written code.
