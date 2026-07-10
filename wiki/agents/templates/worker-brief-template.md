# Managed Worker Brief

Use only when Destin explicitly requests a cold-start worker or coding-manager workflow. Normal coding work does not need this artifact.

Keep the brief short enough to read once. Put stable scope in the ticket; use this brief only for execution-critical context.

```md
# Brief: MON-XXX <title>

## Objective
- One observable outcome.

## Exact Scope
- Included code paths or artifacts.
- Explicit exclusions.

## Repo Anchors
- The smallest files, symbols, tests, or docs to inspect first.

## Semantic Contract
- Identity/dedupe: what makes records, outputs, or relationships the same or distinct.
- Failure/retry: partial-failure, atomicity, retry, and recovery expectations.
- Type contract: exact boundary shapes and consumer expectations.
- Use `Not applicable` for each item that genuinely does not apply.

## Acceptance
- Observable behavior and focused verification.
- Negative-path coverage for persistence, lifecycle, write-back, orchestration, helper-family, or typed-contract changes.

## Anti-Goal
- The adjacent work or abstraction this must not become.

## Stop Condition
- The ambiguity, repo conflict, or scope expansion that requires handback.
```

Do not add revenue-link, deletion-tradeoff, dependency, concurrency, or deliverable sections unless they materially affect this worker. Work creation must already have passed the revenue gate before briefing.
