# Backtest Risk Measurement

Status: in progress

Implemented locally on 2026-10-04; migration `a47c9e21d603` is prepared and tested as PostgreSQL DDL but has not been applied. No live or deployment operation. Related: [[engineering/backtest-strategies-index|Backtest Strategies Index]].

## Definitions

- `max_drawdown`: unchanged non-positive close-sampled account-equity decline from a previous sampled peak. The initial-capital seed remains included.
- `max_position_dd`: non-positive worst unrealized active-position ROE, not peak-to-trough position giveback or entry-relative MAE/MFE. Version 2 observes the inventory carried into each candle at its adverse OHLC extreme, then each completed fill inventory and the final inventory valued at the candle close. It retains the mock formula: signed size × (mark − weighted entry) / (absolute size × mark / leverage). Fees are in account equity, not unrealized position ROE.
- `max_drawdown_ohlc_bound`: conservative account drawdown for the unchanged close-execution path. For each carried position, visit opening equity, favorable extreme, adverse extreme, close, then ordered post-fill inventory snapshots valued at the candle close. Favorable/adverse ordering is a conservative assumption; this is not a reconstructed price path. Hypothetical extremes never enter Sharpe, CAGR or volatility calculations.

Only inventory present before the current close receives this candle's extremes. Closing/reopening, reversal and size changes do not erase earlier observations; new size and weighted basis are observed at the current close and receive OHLC extremes starting with the following candle. The observer accepts single-asset accounts; batch aggregates summarize separate asset runs, not a portfolio path.

Exposure and `pct_time_in_money` retain final post-decision bar sampling. They do not estimate intrabar duration. This task does not repair the separate placeholder `avg_hold_bars` or redefine fill-based trade outcomes.

## Execution boundary

Measurement never invokes hypothetical high/low marks on the mock executor. Execution, liquidation, fills, sizing, fees and final equity remain unchanged. OHLC crossings of the mock liquidation boundary or zero equity set `risk_intrabar_boundary_crossed`; the OHLC account bound is then null. Position ROE remains an inventory-path diagnostic and may extend beyond the unmodeled intrabar liquidation point; the UI states this limitation. Invalid OHLC/inventory/margin fails explicitly.

## Persistence and pipeline contract

`risk_measurement_version=1` means legacy final snapshots; version 2 means carried OHLC plus ordered close observations. Existing stored values are preserved by the additive migration, new bound columns default null, and historical methodology defaults to version 1. New executions write version 2.

Batch summaries persist version sets and boundary-crossing counts. Mixed-version position risk is suppressed, as are OHLC-bound aggregates missing any constituent value. Do not silently rank legacy and corrected position-risk measurements together. Saved-read hydration and generated API clients carry the same metadata. Applying the migration is required before using the changed database-backed runtime.

## Implementation and memory footprint

Sources under `mm_v04/backend/app/`: `data_models/dto/backtest_risk.py`, `services/backtest/risk_measurement.py`, `bt_engine.py`, read-only `MockTradingService.risk_inventory`, performance/backtest DTOs, persistence and saved-read helpers.

The engine scopes an optional typed inventory observer to each candle. The mock notifies it after completed fill accounting and again after liquidation cash finalization. A final snapshot also covers no-fill closes. Callback cleanup uses a context manager, including exceptions; nested attachment fails explicitly. Fill-priced account/position events remain unchanged and are not used as market marks by this observer.

Risk-specific state is O(1) per asset run: current peak, worst bound, worst ROE and a boundary flag, plus one immutable inventory snapshot at a time. It adds no per-bar retained arrays and works identically in full and summary modes. Existing engine artifact retention is unchanged.

## Verification

Hand-calculated long/short extremes, close-entry exclusion, weighted basis, reductions/additions/reversal/reopen, leverage, ordered costs, invalid inputs, boundary crossings, full/summary parity, historical/new persistence hydration, mixed aggregates, and additive PostgreSQL migration SQL are covered. Existing ledger regressions remain unchanged. The local MemLabs replay preserves all 346 fill economics, fees, return, Sharpe and close drawdown while reporting corrected position risk.

Focused checks: 93 backend tests, 15 frontend tests including rendered risk states, production frontend build and focused new-module Ruff/mypy pass. The broad backtest suite is not green: stale strategy imports/request fixtures, unrelated strategy/auth expectations, and unavailable database/process fixtures remain outside this bounded change.

Follow-up verified 2026-10-06: 106 focused backend tests pass, including nonzero-slippage final-bar entries, long/short additions, reductions, reversals, close/reopen/flat sequences, current-candle marks, callback and strategy exceptions, liquidation cash finalization, and full/summary parity. Focused Ruff/mypy pass. The MemLabs replay still matches all 346 original fill economics and unchanged legacy account metrics; zero-slippage risk measurements match the preceding version-2 implementation. No additional schema change or methodology bump; version 2 remains unreleased.
