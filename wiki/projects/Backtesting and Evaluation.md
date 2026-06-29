# Backtesting and Evaluation

Durable context for Money Machine's backtest/research loop.

Related:
- [[Money Machine Operating Context]]
- [[Agent Knowledge Discipline]]

## Current Focus

Backtesting correctness is a trust bottleneck for the research loop. If sizing, signal semantics, bar fetching, or metrics are wrong, downstream strategy evaluation is suspect.

## Active Correctness Themes

- Position sizing invariants: 10%, 50%, and 100% exposure should have explicit, testable behavior.
- Signal semantics: raw signal, transformed signal, flat state, and EPS sign must be distinct.
- Data fetch completeness: requests beyond provider/page limits need pagination and gap checks.
- Metric correctness: fee-only/no-trade rows must not affect win-rate accounting.
- UX/debug clarity: signal zero/flat/EPS and warmup windows should be visually inspectable.

## Linear Tickets

Created in Backtesting and Evaluation project:

- MON-97 — fee-only/no-trade rows excluded from win-rate accounting.
- MON-98 — position sizing behavior explicit/testable.
- MON-99 — raw/transformed/flat/EPS signal semantics.
- MON-100 — >2,000 bar fetch pagination and completeness checks.
- MON-101 — signal/warmup UX clarity.

## Agent Notes

Before implementation, inspect actual backtest route/service/strategy surfaces in `mm_v04`, then define invariants and targeted tests before broad edits.
