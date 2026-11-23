# Backtest scoring dates and warmup

Status: in progress (fresh-fetch boundary repair committed; existing cache inspection remains separate)

Updated: 2026-11-20

Destin approved selected dates as the scored period, with strategy warmup fetched before it. The explicit-date fix is committed as `4d8b9839`. Destin then requested beginning the Latest N follow-up; its local implementation is described below.

## Contract

- Explicit API timestamps select candle opens in `[start_ms, end_ms)`. The date picker includes both displayed UTC calendar dates by using midnight after the last selected day as the exclusive end.
- Resolve the first aligned candle open at or after the selected start. Load `warmup_bars` preceding candles plus all selected candles. The strategy owns its warmup property; it is not inferred independently in the UI.
- Engine validation requires the complete aligned data grid before any strategy callbacks or account observations. Warmup supplies indicator history but generates no trades, fees, equity/risk observations or scored results. Existing bounded window and strategy initialization behavior is retained; see [[engineering/bounded-ema-history]].
- Explicit dates override the legacy `min_candles` floor. That request field remains schema-compatible, and UI/manual-plan builders use at least ten for it even when the scoring period is shorter. Actual required history is scored bars plus warmup.
- The existing 100,000-candle limit applies to the total load, including warmup. Missing warmup/scoring history fails explicitly; the selected period never shifts. Invalid total windows are rejected before loading. Provider/cache limitations still apply.

## Results and compatibility

`CandleLoadReport` stores `window_contract_version=2` for new explicit-date and Latest N runs, selected scoring dates, warmup count, and the original requested fields as data-load bounds/count. `scored_*` fields describe available scoring candles; `executed_*` fields describe actual engine coverage, including earlier liquidation. Failed loads record zero executed bars. The report persists through the existing per-asset JSON field: no database migration is required.

Saved-run hydration uses version-2 persisted load bounds, retaining warmup candles in charts. Reports with an absent version default to version 1 and retain historical retrieval semantics/results. Rerunning historical inputs creates a new run using the current scoring-date contract; historical metrics are never rewritten.

Binance manual previews now require execution `settings`, resolve warmup through the backtest strategy factory, audit prehistory against stored lifespans, show load start/total bars, and bind settings into plan identity. Policy is `manual-binance-plan-preview-v2-scoring-window`. Execution rebuilds the canonical plan and rejects changed settings/stale reviews. Previously completed idempotent execution retries retain their existing receipts. Research MCP forwards the settings and documents scoring-date semantics.

## Implementation and verification

Main paths in `mm_v04`: `backend/app/helpers/backtest_window.py`, `app/data_models/backtest_window.py`, `app/helpers/backtest.py`, `app/services/backtest/asset_executor.py`, `bt_engine.py`, candle loaders, and manual Binance preview/execution services. Frontend control/report views and generated API types are updated.

At the explicit-date implementation milestone, 171 focused offline backend tests, 25 Research MCP tests, and eight frontend tests pass. Production frontend build and scoped Ruff/core type checks pass. The summary-worker fixture was refreshed from removed `THRESHOLDS` to current volatility settings. Tests cover exact boundaries, zero/long warmup, missing candles, nonaligned inputs, total limits, then-unchanged Latest N, worker/full parity, simulated trading economics, liquidation coverage, saved-run compatibility, and reviewed-plan settings changes.

Frontend lint retains two unchanged semantic-element diagnostics in BacktestControlPanel and RefreshBacktestDefaults. Wider preview/execution module mypy checking also exposes two existing annotations (audit-metrics dictionary and redundant cast); the four core changed modules pass. At that offline milestone, no live/backend startup, provider calls, database operations, migration, commit or push was performed. See [[ops/backend-testing]].


## Running-manager verification — 2026-11-18

At Destin's explicit request after he started the backtest manager, ran and saved `8256221e-4a8b-411a-8518-be91f3305500` through Research MCP. Used BTC / custom_adx / daily Hyperliquid candles, selecting January 1–31, 2026 UTC; reused configuration and asset settings from `fa41ea25-6fd6-4a4d-8009-cdc495e8b04e` and deliberately retained its larger legacy min_candles input. Full retention supports inspection in the backtest UI.

Verified against persisted metadata and reloaded artifacts: every selected day is scored, warmup lies entirely before the scoring period, explicit dates override the legacy minimum, no order/fill/position occurs during warmup, and saved metrics/P&L/candle values match the immediate result. Candle price strings differ only in decimal formatting on hydration. Cache supplied all data; no missing bars or provider fetches. This validates the running single-asset path and saved reload, not profitability or the manual Binance batch path. No code change, live-trading action, commit or push. Latest N was still deferred at that verification milestone.


## Latest N completed candles — 2026-11-18

Implemented locally after committing the explicit-date fix. When dates are omitted, `min_candles=N` now means N completed scoring candles, plus preceding strategy warmup. The exclusive end is the interval boundary at or before the execution anchor, so the currently forming candle is excluded. Every asset in a batch uses the same anchor captured at batch start, before asset queue waits. Existing early liquidation can still shorten actual execution and is reflected in executed coverage.

Both in-process and summary workers receive frozen scoring boundaries for full-grid validation. Missing warmup/scoring history fails rather than reducing N; the total-load cap includes warmup. Original request dates remain null, preserving Latest N when rerunning, while version-2 reports retain the exact load/scoring window for saved hydration. Historical version-1 retrieval/results remain unchanged. The UI labels the field Latest N Candles; generated API descriptions and MCP tool descriptions match.

Verification: 120 focused offline backend tests pass, including boundary rounding, additional warmup, full/summary parity, shared batch anchor, missing first/scoring/final candles, persisted reload completeness and historical compatibility. Scoped Ruff and mypy checks and the frontend production build pass. At the offline implementation milestone, running-manager Latest N verification had not yet been performed. Latest N changes are uncommitted; nothing pushed.


## Latest N running-manager verification — 2026-11-18

After Destin restarted the manager, executed and saved Latest N run `e28447ab-3b23-44f7-92f6-98efba0faf63` through Research MCP. Reused BTC/custom_adx daily configuration and asset settings from the explicit-date verification, set N to 31 and omitted both dates.

Verified the completed-candle cutoff against the call timestamps, exactly N scored observations plus preceding strategy warmup, a contiguous load grid, no warmup order/fill/position events, and unchanged metrics/P&L/candle values after saved artifact hydration. The saved request retains null dates and N, while the report retains the frozen scoring/load boundaries. All candles came from cache. This verifies the running single-asset path; batch and summary-worker behavior remain covered by offline checks. No code changes, commit, push or live-trading operation.


Commit completion: at Destin's request, Latest N was committed as `7269ac88` (`fix(backtest): score latest N completed candles with extra warmup`). Explicit-date fix remains `4d8b9839`. Code working tree clean after commit; nothing pushed. Earlier uncommitted milestone notes are historical.


## Hyperliquid fresh-fetch boundary repair — 2026-11-20

Destin reported BTC/4h Latest N failing engine validation after the loader reported complete history. Offline reproduction with an inclusive-end provider response produced 354 loaded candles for 353 required; completeness counted only in-window candles while the engine compared the whole array. Cache reads already enforce an exclusive end. Earlier real-manager verification was cache-only and did not exercise this failure path.

Approved repair implemented locally: `restrict_candle_window` in `app/helpers/candle.py` filters all candle columns together; Hyperliquid `_fetch_missing` restricts each fetched view to its own `[span.start_ms, span.end_ms)` before merging or persistence. This prevents out-of-span candles from being stored or passed to the engine, including the extra forming candle at a Latest N cutoff. Strict engine validation remains. Raw fetch-page counts/weights remain provider diagnostics; accepted fetched counts and actual bounds describe filtered data. Shared Hyperliquid client and live paths are unchanged.

61 focused offline tests pass, including cold-cache/reload equality for 100 scored + 253 warmup at 4h, extra start/end candles, partial-cache gaps, Latest N/explicit dates, full/summary execution, and genuinely missing warmup/scoring bars. Scoped Ruff/mypy and whitespace checks pass. Uncommitted; no service restart, provider call or database mutation. Existing cached unfinished boundary candles are not retroactively refreshed by this change and remain a separate inspection/repair follow-up.


Boundary repair committed at Destin's request as `316ac7ed` (`fix(backtest): filter fetched candles before caching`). Includes only the candle helper, Hyperliquid backtest loader and regression tests. Unrelated Opposite Bid Trend and position DTO edits remain uncommitted. Nothing pushed.
