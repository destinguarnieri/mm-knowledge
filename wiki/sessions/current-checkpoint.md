# Current Checkpoint

Status: in progress

Date: 2026-10-16

## Current focus

Backtest Engine V2: vectorization → multi-timeframe data → resting limits → cross margin. The current strategy is consolidated `example`, not retired `emac_cross`.

## Completed

MON-228 baseline and MON-229 separate `example_vectorized` strategy are implemented locally. Original `example.py` is unchanged. All seven configurations match baseline economics exactly at 1,024 and 10,000 bars. 163 targeted tests and scoped Ruff/mypy pass after the standalone revision. The current strategy directly inherits BacktestStrategy, owns its configuration, uses single-call EMAs and receives the engine bar index. Features agree within declared tolerances; economics remain exact on the fixtures. Prior-revision benchmarks showed 1.82–2.72 times speedup at 10K; this revision was not rebenchmarked. See [[projects/backtest-engine-v2-plan|delivery plan and evidence]] for boundaries, fallback modes, provenance, and reproduction.

## Next action

The internal reference fallbacks have now been removed at Destin’s request; unsupported configurations explicitly reject and direct users to example. Feature events are now deferred until full-output serialization: no retention flag or feature messages in the strategy bar loop, and user file layout is preserved. The latest verification passes 140 tests plus scoped Ruff/mypy. Destin is considering volatility semantics; preserve the current capped-window behavior until he selects a change. MON-234 remains the separate 96 × 50,000 upper-bound baseline blocking MON-230; neither has started. Changes remain uncommitted.

## Boundaries

No live runtime, database runs, account/order/position mutation, commit, push, or deployment. No unrelated research obligation resumes. Original ticket backup remains in `raw/linear/backtest-engine-v2-tickets-2026-10-16.json`.
