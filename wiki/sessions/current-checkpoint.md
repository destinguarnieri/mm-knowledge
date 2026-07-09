# Current Checkpoint

Date: 2026-07-08 20:15 EDT

## Current State

Accepted and committed `MON-130` explicit backtest date ranges.

- Ticket: Done — https://linear.app/money-machine/issue/MON-130/critical-backtests-must-support-explicit-date-ranges-for-research
- Commit: `6367c63c` on `bug/backtest` — "Add explicit backtest date ranges for research splits."
- Includes narrow recovery follow-up: asymmetric persist fail-closed, explicit-window hydration completeness, upsert pairing guard.
- Verification: backend focused 36 passed; research_mcp run_backtest 5 passed.
- Remaining ops: apply Alembic `c2d8e9f0a1b3` in target envs; push branch when ready.

Next action: choose next Agentic Research Loop ticket now that explicit windows unblock `MON-127` (hard) and soft-unblock `MON-122` / `MON-126` / `MON-129`.

## Prior Current State


## Objective

Cohesive Agentic Research Loop implementation plan + Linear ticket re-spec, so Research MCP V2 can support `Research Process V1` end to end without ad hoc agent code.

## Current State

- 13-ticket diligence complete across the `Agentic Research Loop` Linear project (`MON-119` umbrella + children including `MON-130`).
- Shared contracts and sequencing locked (below).
- Linear ticket re-specs / description updates in flight to match the cohesive plan.
- `MON-130` narrow follow-up delta landed after coding-manager **Narrow** review (asymmetric retrieval fail-closed, explicit-range hydration completeness, upsert pairing guard). Focused tests 36/5 passed; delta handoff on Linear. Awaiting re-acceptance (**Narrow** → **Accept**) + commit.
- `MON-119` remains umbrella-only — not an implementation ticket.

## Locked Shared Contracts

- **Research root:** `wiki/research/trading/` (not `wiki/quant/research/`).
- **`project_id`:** equals the research project slug (stable identity for KB paths and MCP tools).
- **KB writeback:** lives in Research MCP (not a separate KB/document MCP facade for V1).
- **Batch ≠ grid:** batch execution and grid/suite search are distinct concepts/tools; do not collapse them.
- **Registry:** KB-first run registry (research docs / project state), with backend saved-run IDs as references — not a parallel opaque registry as source of truth.
- **`MON-130` first:** explicit date-range backtests are the hard backend prerequisite before split/process enforcement can be real.

## Sequencing

**V1 critical path**

1. `MON-130` — explicit backtest date ranges
2. `MON-128` — project state / KB writeback
3. `MON-126` — run registry, config snapshots, artifact references
4. `MON-122` — batch / grid / suite execution
5. `MON-123` ∥ `MON-120` — grid summaries/robustness analytics in parallel with artifact exports/chart packs/review notes
6. `MON-121` — handoff / promotion gates

**Early (non-blocking relative to critical path where noted)**

- `MON-85` — pull early when capacity allows (does not replace the critical path above).

**V2 robustness**

1. `MON-127` — split / quarantine / holdout enforcement
2. `MON-124` — null / random-entry and standardized baselines
3. `MON-129` — saved-run metadata filtering / tagging
4. `MON-125` — research process state machine tool

## Ticket Posture

| Ticket | Role |
|--------|------|
| `MON-119` | Umbrella only — tracking / narrative, not implementation |
| `MON-130` | Only Ready implementation ticket right now |
| Remaining children | Re-spec in flight; launch only after coding-manager launch review |

## Next Action

1. Finish Linear ticket re-specs so descriptions match the locked contracts and sequencing.
2. Then either:
   - launch / complete `MON-130` worker acceptance (acceptance tests + coding-manager accept), or
   - coding-manager launch-review `MON-128` once `MON-130` is accepted.

## Recent Context (compact)

- Earlier today: Research MCP gap analysis vs `Research Process V1`; Linear project `Agentic Research Loop` populated; `MON-130` created as hard blocker, launch-reviewed Ready, implemented locally (optional `start_ms`/`end_ms`, persist/retrieval, Research MCP forward).
- Diligence pass produced the cohesive locks and sequencing above; index routing for research process docs corrected to `wiki/research/trading/`.
