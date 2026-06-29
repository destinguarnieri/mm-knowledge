# Money Machine Operating Context

Money Machine is a full-stack Hyperliquid trading system with separate live runtime and backtest/research subsystem.

Related:
- [[Agent Knowledge Discipline]]
- [[Backtesting and Evaluation]]

## Durable Frame

- Live runtime, account/order/position handling, strategy lifecycle, Hyperliquid client paths, performance policies, deployment, and secrets are money-sensitive.
- Backtest/research work is separate from live-money operation and should remain safely local/read-only unless explicitly authorized.
- The immediate operating bottleneck is reducing friction and trust gaps in the backtest/research loop while preserving capital-safety boundaries.

## Canonical Repo Context

Primary repo: `/Users/destinguarnieri/Desktop/codebase/mm_v04`

Mandatory agent entrypoint:
- `AGENTS.md`

Important KB/docs:
- `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/AGENTS.md`
- `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/wiki/index.md`
- `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/wiki/ops/current-checkpoint.md`
- `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/wiki/ops/session-change-log.md`
- `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/wiki/trading/money-machine-language.md`

Older repo-local `docs/` files, if present, are transitional references only. Durable docs should live in the KB.

## Execution Systems

- Linear tracks execution/backlog state.
- This wiki tracks durable synthesized context.
- QMD indexes the wiki and supporting docs for retrieval.
