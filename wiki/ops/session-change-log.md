# Session Change Log

## 2026-06-29 02:04 EDT

- Normalized copied agent templates into `wiki/agents/templates/` and updated `wiki/index.md` routing for the template directory.
- Updated `mm_v04/.cursor/skills/` pointers away from source-repo `docs/meta/...` paths to Money Machine KB template paths where matching files exist.
- Cleaned stale `docs/meta/...` references inside the agent templates themselves.
- Missing brought-over source docs/templates were identified in `wiki/ops/current-checkpoint.md`; no Money Machine runtime/product code was edited.

## 2026-06-29 01:04 EDT

- Coding-manager orientation resumed MON-97 from dirty files and `wiki/projects/MON-97-backtest-metrics-plan.md`; no `mm_v04` code edits were made.
- Found MON-97 is not acceptance-ready yet: `backend/app/services/backtest/bt_eval_tmp.py` still has a stale positional `compute_perf_metrics` call, and chunk 4's aggregate/engine-level regression is not implemented.
- Verification attempt `PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run pytest --confcutdir=tests/backtest tests/backtest/test_backtest_metrics.py -q` failed before collection because `pytest` was not available to `uv run`.

## 2026-06-29 00:05 EDT

- Resumed backtest issue work with read-only orientation on Linear tickets MON-97 through MON-101.
- Inspected backend backtest engine/metrics/mock-service/manager/helper/signal paths and frontend chart route/component surfaces.
- No `mm_v04` code edits were made in this orientation pass; pre-existing PRI local changes remain in the worktree.
- Recommended implementation order: MON-97 metrics denominator first, then MON-98 sizing invariants, MON-99 signal semantics, MON-100 fetch pagination, and MON-101 UX after screenshot/context.
- Added `wiki/projects/MON-97-backtest-metrics-plan.md` with an executable plan for classifying trade outcomes from raw fills before fee-inclusive PnL points collapse the data.
- 00:30 EDT: Completed MON-97 chunk 1 RED tests in `backend/tests/backtest/test_backtest_metrics.py`. Replaced a stale broken `sma_cross` integration test that imported a non-existent module with focused pure metric tests. Verification produced expected RED result: two failures because `compute_perf_metrics()` does not yet accept `trade_pnls`; legacy fallback test passed.
- 00:41 EDT: Completed MON-97 chunk 2. Added optional `trade_pnls` to `backend/app/services/backtest/metrics.py`; when supplied, trade metrics use explicit trade outcomes and ignore fee-only/no-trade PnL points, while legacy `pnl_points` fallback remains. Targeted test file now passes: `3 passed in 0.84s`.
- 00:49 EDT: Completed MON-97 chunk 3. Added `_fill_trade_outcome()` in `backend/app/services/backtest/bt_engine.py` to classify raw fills before PnL-point collapse, collect `trade_pnls` in `_aggregate_backtest_data()`, and pass them into metric computation. Added fill-classification unit coverage. Targeted test file now passes: `6 passed, 2 warnings in 1.50s`.

## 2026-06-28 23:10 EDT

- Verified `price_reversal_v2` had a return-contract bug: the exception path returned `None` despite the `PriceReversalV2` return annotation and callers indexing the result as a dict.
- Fixed `backend/app/lib/signals/pri_v2.py` to return a neutral `PriceReversalV2` fallback with fresh empty list fields on errors.
- Added `backend/tests/indicator/test_pri_v2.py` regression tests for the exception fallback and mutable-list freshness.
- Verification: direct fallback assertion passed; isolated pytest passed with `PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run pytest --confcutdir=tests/indicator tests/indicator/test_pri_v2.py`.
- Note: normal pytest invocation hit root `.env` access through repo-level `tests/conftest.py`, so isolated indicator pytest was used to avoid secret-file access.

## 2026-06-28 22:26 EDT

- Created Linear tickets MON-97 through MON-101 for backtesting correctness/UX issues from Destin's backtester complaint list.
- Fixed QMD local install mismatch by reinstalling `@tobilu/qmd@2.5.3` with Bun; verified `qmd status`, `qmd update`, and keyword search work.
- Decided operating model: Money Machine KB is an Obsidian-compatible linked markdown wiki; QMD is indexed search/retrieval over it; prompts enforce discipline/hygiene.
- Patched `~/.hermes/SOUL.md` with global knowledge/continuity discipline.
- Patched `mm_v04/AGENTS.md` with Money Machine KB usage, checkpoint, and changelog requirements.
- Rewrote `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/AGENTS.md` as the KB operating contract.
- Initialized `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/wiki/` with index/log and core context pages.
- Updated canonical checkpoint path: `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/wiki/ops/current-checkpoint.md`.
- Reorganized `/Users/destinguarnieri/Desktop/codebase/mm-knowledge` so canonical category markdown lives under `wiki/` instead of duplicate top-level category folders.
- Moved historical prompt dumps to `archive/prompts_DUMP/` and pointed QMD collections at `wiki/` paths.
- Added `scripts/check_wikilinks.py`; verified current wiki links with `missing=0` and `ambiguous=0`.
- Created Hermes skill `moneymachine-knowledge-base` for Money Machine wiki/QMD workflow.
- Redirected repo prompt/changelog discipline away from `mm_v04/docs/work/*` and into the KB paths under `mm-knowledge/wiki/ops/`.
