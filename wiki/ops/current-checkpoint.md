# Current Checkpoint

Date: 2026-06-29 01:04 EDT

## Current State

Coding-manager orientation resumed MON-97 from prior agent changes. Dirty MON-97 files currently implement chunks 1-3 of `wiki/projects/MON-97-backtest-metrics-plan.md`: explicit `trade_pnls`, fill-level trade outcome classification, and unit/helper coverage. No code edits were made during this orientation pass.

Acceptance is not ready yet. Remaining ticket-local gaps:

- `backend/app/services/backtest/bt_eval_tmp.py` still calls `compute_perf_metrics(equity_bt_s, ret_bt_s, ...)` even though `compute_perf_metrics` is keyword-only after `equity`; the optional temp evaluator will fail if `BT_EVAL_TMP_ENABLED` is on.
- Chunk 4 asks for an engine/aggregate-level regression proving `pnl_points`, `total_fees`, `trade_pnls`, and final metrics stay aligned. Current dirty tests cover `compute_perf_metrics` and `_fill_trade_outcome`, but not `_aggregate_backtest_data` / `_compute_metrics` together.
- Targeted verification attempted with `PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run pytest --confcutdir=tests/backtest tests/backtest/test_backtest_metrics.py -q`; it failed before collecting tests because `uv run` could not spawn `pytest` (`No such file or directory`). Dev dependencies likely need sync/install before rerun.

Earlier state:

Current session resumed backtest issue work with read-only orientation. Linear tickets MON-97 through MON-101 are still in Triage under Backtesting and Evaluation. The most actionable engineering sequence appears to be backend correctness first, then UI clarity:

1. MON-97 metrics denominator / fee-only rows.
2. MON-98 sizing invariants and proportionality fixtures.
3. MON-99 signal semantics and raw/transformed/flat/EPS separation.
4. MON-100 candle fetch pagination/completeness.
5. MON-101 chart UX after semantics are available and Destin provides screenshot/context.

No repo code was edited during this orientation pass.

## Completed This Session

- Oriented on backtesting tickets MON-97 through MON-101 from Linear.
- Read KB routing/checkpoint/changelog and `wiki/projects/Backtesting and Evaluation.md`.
- Inspected relevant repo surfaces:
  - `backend/app/services/backtest/bt_engine.py`
  - `backend/app/services/backtest/metrics.py`
  - `backend/app/services/backtest/mock_services.py`
  - `backend/app/services/backtest/backtest_manager.py`
  - `backend/app/helpers/backtest.py`
  - `backend/app/helpers/signal_position.py`
  - `backend/app/helpers/position_limits.py`
  - `backend/app/lib/utils/signal_processing.py`
  - `backend/app/backtest/strategies/strategy_base_backtest.py`
  - `backend/app/backtest/strategies/emac_v3.py`
  - `backend/tests/backtest/test_backtest_metrics.py`
  - `frontend/src/components/Backtest/TradingViewChart.tsx`
  - `frontend/src/routes/_layout/backtest.backtest.tsx`
- Current working tree still has pre-existing local changes from the prior PRI fix: `.DS_Store`, `backend/app/lib/signals/pri_v2.py`, and untracked `backend/tests/indicator/test_pri_v2.py`.

## Prior Completed Context

- Created Linear tickets for backtesting complaints/bugs:
  - MON-97 — fee-only/no-trade rows excluded from win-rate accounting.
  - MON-98 — position sizing behavior explicit/testable.
  - MON-99 — raw/transformed/flat/EPS signal semantics.
  - MON-100 — >2,000 bar fetch pagination and completeness checks.
  - MON-101 — signal/warmup UX clarity.
- Fixed local QMD native module mismatch by reinstalling `@tobilu/qmd@2.5.3` with Bun.
- Verified QMD runs and `qmd update` indexes the KB.
- Patched `~/.hermes/SOUL.md` with global knowledge/continuity discipline.
- Patched `mm_v04/AGENTS.md` with Money Machine KB and session hygiene requirements.
- Rewrote `mm-knowledge/AGENTS.md` into an operating contract for wiki + QMD.
- Initialized and reorganized `mm-knowledge/wiki/` as the canonical KB home. Top-level category docs were moved under `wiki/` to avoid duplicate markdown trees.
- Created `moneymachine-knowledge-base` Hermes skill for this exact wiki/QMD workflow.
- Added `mm-knowledge/scripts/check_wikilinks.py` and verified wiki links resolve.
- Fixed `price_reversal_v2` return-contract violation and verified with isolated pytest:
  - `PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run pytest --confcutdir=tests/indicator tests/indicator/test_pri_v2.py`
- Current `mm-knowledge/wiki/` spine includes:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/company/overview.md`
  - `wiki/company/money-machine-360.md`
  - `wiki/ops/current-checkpoint.md`
  - `wiki/ops/session-change-log.md`
  - `wiki/ops/linear-operating-system.md`
  - `wiki/ops/research-mcp-runbook.md`
  - `wiki/concepts/Agent Knowledge Discipline.md`
  - `wiki/projects/Backtesting and Evaluation.md`
  - `wiki/projects/Money Machine Operating Context.md`

## Current Truth

Canonical continuity stack:

1. Explicit user direction.
2. `mm_v04/AGENTS.md` for repo-local safety and entrypoint instructions.
3. `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/AGENTS.md` and `wiki/index.md` for KB operating discipline.
4. `mm-knowledge/wiki/ops/current-checkpoint.md` and `mm-knowledge/wiki/ops/session-change-log.md` for continuity.
5. Linear for execution/backlog truth.
6. QMD for indexed retrieval over the KB.
7. Built-in Hermes memory only for compact global facts/preferences.

## Known Open Items

- `mm-knowledge` has untracked/moved files and should be cleaned/committed intentionally.
- QMD reports pending embeddings; run `qmd embed` when semantic retrieval should be fully online.
- Add QMD collection contexts for better retrieval.
- Consider a Hermes cron job for ambient KB/checkpoint hygiene after the prompt/file discipline settles.
- External memory provider decision deferred; likely bakeoff Honcho vs Holographic only if Wiki+QMD+cron leaves a gap.
- A normal `uv run pytest tests/indicator/test_pri_v2.py` run imports repo-level `tests/conftest.py`, which attempts to read root `.env`; isolated indicator pytest with `--confcutdir=tests/indicator` avoids secret-file access.

## Backtest Orientation Notes

- MON-97 executable plan now lives at `wiki/projects/MON-97-backtest-metrics-plan.md`.
- MON-97 chunks 1-3 are complete: `backend/tests/backtest/test_backtest_metrics.py` has pure metric and fill-classification tests, `backend/app/services/backtest/metrics.py` accepts optional `trade_pnls` while preserving legacy `pnl_points` fallback, and `backend/app/services/backtest/bt_engine.py` now classifies raw fills into `trade_pnls` before fee-inclusive PnL-point collapse. Targeted verification passed: `PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run pytest --confcutdir=tests/backtest tests/backtest/test_backtest_metrics.py -q` -> `6 passed, 2 warnings in 1.50s`.
- MON-97 likely centers on `backend/app/services/backtest/metrics.py:253`, where trade stats currently count every non-zero `PnlPointPublic.realized_pnl` as a trade. Since `bt_engine.py` builds one PnL point per processed bar from fill `closed_pnl`, fee-only close/open accounting can become denominator noise if represented as non-zero realized PnL.
- MON-98 likely centers on asset settings and target sizing: `strategy_base_backtest.py:249` computes max position as current account value × `max_position_percent` × leverage; strategies convert signal to target value through `signal_position.py`, clamp through `position_limits.py`, then size/order through helpers and `MockTradingService`.
- MON-99 likely centers on `signal_processing.py`, `signal_position.py`, and per-strategy signal events. Current signal payloads expose only `score` plus generic `variant/meta`; `emac_v3.py` already emits separate raw-ish and trade signal rows, but the DTO/API/chart model does not yet encode raw vs transformed vs flat/EPS position state as first-class semantics.
- MON-100 centers on `backtest_manager.py:923` / `_fetch_gap_candles_async`: DB rows are read for the requested window and a single exchange snapshot fills the gap. If Hyperliquid/provider snapshot caps around 2,000 bars, there is not yet visible chunking or completeness validation at this callsite.
- MON-101 centers on `frontend/src/components/Backtest/TradingViewChart.tsx` and `frontend/src/routes/_layout/backtest.backtest.tsx`; defer until backend/API semantics exist and screenshot/context is attached.

## Next Recommended Actions

1. Start with MON-97 if the goal is quickest trust restoration: add pure unit tests around `compute_perf_metrics` before touching engine/accounting.
2. Then tackle MON-98 with deterministic engine/mock-service fixtures for 10/50/100% sizing, no compounding, and no fee/slippage first.
3. Keep MON-101 parked until Destin provides screenshot/context and MON-99 semantics are clearer.
