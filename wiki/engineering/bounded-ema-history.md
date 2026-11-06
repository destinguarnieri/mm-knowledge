# Bounded EMA history

Status: confirmed

Destin approved keeping the current implementation after reviewing initialization and its speed comparison on 2026-10-29. Committed in mm_v04 as `3f8f36f8` on `feat/work`: `refactor: bound EMA history and share scalar updates`. All 20 migration files were committed; not pushed. The subsequent local PX Threshold Slope fix is described below. Earlier extraction commit: `f7a4243e`. See [[sessions/current-checkpoint]].

## Retention contract and footprint

`app/lib/indicators/ema_state.py::CausalEMAState` requires positive keyword-only `history_size`. It stores two scalar calculation values and a `deque(maxlen=history_size)` of visible outputs. Initialization streams the input, retaining at most that many outputs throughout; it does not build an input-sized EMA output array. Returned copies use O(history_size) memory. `EMACState` owns three such states (fast, slow, and signal), each with the supplied capacity, plus an initialization flag.

- `update(value)` consumes one observation and returns its EMA; `latest` reads the latest visible output (NaN before observations).
- `advance(window)` seeds from the whole first input, then consumes only the last observation per call. It returns the retained suffix up to the input length. A shorter input does not reduce stored retention. A requested output longer than retained history cannot be supplied.
- `values()` returns a copy of the retained outputs. Scalar and array methods share one retention policy.
- Dropping old outputs does not reset the recursive EMA or remove older observations' influence. Timestamp ordering and deduplication remain caller responsibilities.
- Span-one identity, dense-fill leading-gap initialization, internal gap forward-fill, and optional visible missing values remain supported. Streaming initialization can produce small floating-point differences from TA-Lib initialization.

## Backtest consumers

`BT_WINDOW_CAP` is positive, defaults to 512, and no longer accepts the old <=0 unbounded mode. `app/helpers/backtest.py::effective_window_cap` returns `max(BT_WINDOW_CAP, warmup_bars + 1)`. All array EMA/EMAC callers use that same resolution as the engine candle window, including inherited warmup overrides. Do not substitute a hard-coded 512 or only the configured value when warmup is larger. Treat configuration/warmup as fixed for a strategy instance/run.

Multi-speed EWMAC uses the shared scalar update with capacity one per unique EMA span; it retains its existing candle ordering/deduplication and volatility state. Its centered volatility estimator has a separate O(long_window) bounded deque.

## Verification and remaining findings

161 focused tests pass, including bounded seeding, mixed scalar/array updates, nonfinite recovery, cap validation, and PX Threshold replay. Six 1800-bar synthetic PX scenarios cover RVWAP, close/HLC3 EMAs, caps 64/512/768, warmup 700, four scaling modes, and buffering. Independent full-series EMA and pre-change EMA comparisons preserve PX indicators/signals within tolerance and match every threshold transition, order, fill, and position. All six EWMAC speed sets match pre-change snapshots exactly over 3000 bars. All 11 array strategy constructors use the resolved capacity at configured caps 64 and 512 (22 smoke cases).

PX Threshold Continuous also matches the old-state replay. At the EMA migration commit, PX Threshold Slope advanced its EMA twice per candle via `_features` and `_normalized_slope`; that migration preserved the behavior. The subsequent fix below removes it. Its normalized slope differs by up to about 2.08e-5 from old initialization arithmetic in this replay, while every slope gate and trade matches. This is a separate existing caller issue, not a guarantee of equivalence for all data or threshold settings.

Broader selected tests reproduce 22 unrelated baseline failures: 15 example feature-mock arity failures, one PX signal-bands stale absorption mock, and six engine request fixtures missing required assets. The stale PX Threshold default assertion was corrected from 200 to its existing signal_stats_lookback default of 100; production defaults are unchanged. Verification used synthetic settings with dotenv and parent conftest disabled; no database/live runtime was started.

## Initialization benchmark — 2026-10-29

At Destin's request, compared the current scalar initializer with the pre-migration `_initialize` routine from `f7a4243e`, installed on the same current class so both retain a bounded 512-output deque. Timings include construction, initialization, output retention, and returning the retained array; these are not timings of EMA_P_CLEAN alone. EMA span 200, finite synthetic float64 prices (seed 42), local arm64 Python 3.11.6 / NumPy 2.3.3 / TA-Lib 0.6.8. Five warmups and 31 alternating-order rounds; 512-input cases batch 20 initializations per round. Imports and input generation excluded; cyclic GC disabled during timing.

Median at 100,000 inputs: scalar 23.438 ms, EMA_P_CLEAN-based initializer 6.026 ms (batch initializer 3.89x faster). At 512 inputs: scalar 0.1334 ms, batch initializer 0.0558 ms (2.39x faster). Retained outputs differ by at most 4.55e-13; continuation after another observation also matches within 1e-12 tolerance. The streaming initializer trades initial-load speed for bounded additional EMA output storage; the batch initializer still extends the bounded deque across every computed output, matching the original initializer logic. No implementation decision or source edit followed this benchmark. Reproduction script and JSON were saved temporarily under `/tmp/mm-bounded-ema/benchmark_initialization.py` and `benchmark_initialization_results.json`.

## PX Threshold Slope single-update fix — 2026-10-29

Status: in progress

At Destin's request, `on_candle_closed` now computes the moving-average array once and passes that same array to both `_features` and `_normalized_slope`. The parent PX Threshold `_features` accepts an optional keyword-only precomputed moving_average, computing one only when omitted; other callers retain their existing call contract. `_normalized_slope` now consumes only the supplied numeric array and cannot advance EMA state. No EMA implementation changes, cache, or extra persistent state.

This corrects repeated EMA observations and the resulting distorted history for EMA sources. With span 3 and closes [100, 102, 104, 110, 112], the retained current EMA is now 106.25 then 109.125, instead of an extra update producing 108.125 then 111.03125. Default RVWAP also computes once rather than twice. EMA-source slope-strategy signals/decisions may intentionally differ from the buggy version; prior old-version parity is not a target for this fix.

Two regression cases failed before the fix on the observed duplicate call, then pass for CLOSE and RVWAP. They exercise actual strategy callbacks, retained EMA versus an independent EMA_P_CLEAN reference, emitted MA and normalized slope, and rollover with capacity 8. Existing threshold entry/exit gating tests and parent/continuous/PX replay tests pass: 23 tests total. Scoped Ruff and mypy pass. Changes are local and uncommitted; no live runtime, database access, or push.


## Example sizing-volatility footprint — 2026-11-02

Status: in progress (local template-only configuration preview).

When example.py selects volatility-target sizing, it owns one map keyed by the run's asset/timeframe streams, containing one BlendedCenteredEwmaVolatility per stream. Each estimator retains scalar moments/last close plus a deque bounded by configured long_volatility_window (default 2560); storage is O(stream count × long_volatility_window), with no candle-history copies retained. Capital sizing leaves the map empty. The feature stage calls estimator.advance(closes): the estimator seeds the first available window once, then updates with the latest close before trading gates. Initialization uses the existing last-close sentinel, adding no retained state; the former Example seeding helper is removed. Features passes the snapshot to sizing without further state advancement. Capital mode computes score features from the current candle window, including when dampening is disabled, and retains no additional score history. No timestamp tracking or replay deduplication is retained; callbacks are ordered once per candle. Focused tests cover bounded retention, warmup/prefix parity through rolling windows, read-only sizing, hold-path updates, and isolation between streams. See [[trading/backtest-strategies-index#Example-only configuration wiring preview — 2026-11-02]].


## Independent volatility roles — 2026-11-03

Status: in progress, superseding the template footprint description above.

Example now keys BlendedEwmaVolatility by (asset, timeframe, targeting/adjustment), retaining at most two estimators per configured stream. Each estimator keeps scalar moments/last close, an annual volatility deque capped at slow_span, and a scoring deque capped at max(fast_span, slow_span). Scores use the retained annual-volatility window; recursive return moments continue across rolling windows. No price history or timestamps are retained. Both roles disabled means no volatility state. Each active role advances once in features even when orders hold; downstream sizing and adjustment only read observations. The old BlendedCenteredEwmaVolatility import remains an alias with centered/simple-return defaults, preserving EWMAC outputs; that estimator also now maintains the bounded scoring deque. Space is O(streams × enabled roles × (slow_span + max(fast_span, slow_span))). See [[trading/backtest-strategies-index#Independent volatility stages and per-asset risk weights — 2026-11-03]].


## Window-based Example volatility — 2026-11-03

Status: in progress, implementation assumption following Destin's array-scoring sketch. Supersedes Example's retained-role footprint above.

Example now retains no volatility estimator/history. Each enabled role computes volatility arrays and only its requested scores from the supplied candle window, using O(window capacity) temporary arrays. No pre-window recursive influence is retained. EWMAC still uses the original BlendedCenteredEwmaVolatility scalar moments plus one long_window-bounded deque; its added score-history deque and scores() wrapper are removed. See [[trading/backtest-strategies-index#Requested volatility scores from price windows — 2026-11-03]].


## Centered targeting restored — 2026-11-03

At Destin's request, Example again retains one BlendedCenteredEwmaVolatility per asset/timeframe when targeting.method is Centered. Space is O(stream count × slow_span) for one bounded annual-volatility deque plus scalar EWMA moments/last close per stream. There is no score-history deque or timestamp state. Features advance once; sizing reads its snapshot. RMS targeting and adjustment remain window-based while their common state/interface design is unsettled. This supersedes the preceding statement that Example retains no volatility state. Simple/log returns are supported; EWMAC's simple-return default is preserved.


## Volatility estimation and scoring separation — 2026-11-03

At Destin's direction, renamed BlendedCenteredEwmaVolatility to CenteredEwmaVolatility and removed its blend weights, snapshot calculation, and unused BlendedVolatilitySnapshot DTO. The estimator owns one annual-volatility deque bounded by long_window plus scalar recursive moments/last close. advance returns a detached annualized array; annual_volatility_values remains the read-only-copy accessor. No separate strategy score history or timestamp state was added.

Example has explicit targeting and adjustment sections. Its _annual_volatility helper selects the estimator and returns annualized values; both roles then use instrument_vol_scores3, requesting b_score or r_score respectively. RMS remains a window estimator; centered remains streaming, with independent state per role/asset/timeframe. Blend math lives only in b_score. The scorer accepts precomputed annualized values and no longer takes the unused tf_sec argument. A centered first close has no return, producing empty history/NaN scores; targeting safely sizes zero. If slow_span is shorter than fast_span, centered r_score remains NaN and adjustment is neutral.

EWMAC now computes its blend through b_score and keeps its strategy snapshot/output schema, price-unit conversion, calibrated forecasts, and zero-volatility startup behavior. Exact equality against the pre-refactor implementation holds for all snapshot fields over six speed sets × 3000 candles. 401 focused pipeline/EWMAC/estimator/scorer tests pass; scoped source mypy and source/test Ruff pass. Stale removed-API tests were migrated. No live operations or commit.


### RMS annualization follow-up — 2026-11-03

ewma_rms_returns now optionally annualizes using tf_sec or an explicit annualization_factor override. Omitting both preserves per-bar output for existing callers. Example delegates annualization to the estimator and advances centered state on every candle. Completed removal of the unused EWMAC trailing_annual_volatility snapshot field after Destin removed its calculation; the blend still uses the trailing mean internally through b_score. 411 focused tests and scoped mypy/Ruff pass. No commit or runtime operations.


### Volatility and sizing package committed — 2026-11-03

At Destin's request, committed the 25-file package as efd97d06 (refactor: unify volatility scoring and configurable backtest sizing) on feat/work. Includes Example volatility/scoring/sizing refactor, EWMAC shared blending, optional RMS annualization, and per-asset backtest risk-weight migration/API/UI. Verification: 512 focused backend tests and three frontend tests pass; TypeScript and production build pass; scoped source typing/lint and whitespace checks pass. Database migration remains unapplied. No push or live operations. This supersedes prior uncommitted status for these changes.

### Kitchen Sink sizing and volatility propagation — 2026-11-03

Status: in progress; Destin approved the proposed scope and requested implementation, now implemented locally for review.

example_kitchen_sink.py now uses Example's SIZING_BASE (default unlevered), per-asset instrument_weight, global diversification multiplier, independent VOLATILITY.vol_targeting / vol_adjustment, and explicit REBALANCE deadband/buffer settings. Its full/continuous/banded mapping, fixed/zero-cross/disabled thresholds, remembered threshold state and transitions/every_bar gate remain. Full sizing means the calculated capital/risk base. Pipeline: capital/risk base → sizing branch/threshold direction → volatility adjustment → rebalance/over-cap bypass → fixed allocation/leverage cap → executable delta. The execution gate still controls whether over-cap correction runs. Volatility no longer dampens the cap or rebalance buffer base.

Centered state is separate per role and asset/timeframe, with one annual-volatility deque bounded by that role's slow_span plus scalar estimator state. Space is O(streams × sum of enabled Centered slow_spans); RMS uses temporary window arrays and retains no volatility state. Features advance every enabled estimator once per candle before the transition gate; sizing reads observations only. Warmup includes fast_span × 3 and slow_span for both roles. Existing bounded EMAC history and two-emitted-signal history remain.

Old flat VOLATILITY and null VOLATILITY configs are rejected. Disabled roles use VOLATILITY={} or null nested role values. MIN_ADJUSTMENT_VALUE_PCT and VOL_ADJ_POS_SIZE remain inherited compatibility fields but do not drive this strategy's sizing; use REBALANCE and nested volatility_scale instead. No legacy fallback was added. Frontend controls support nested roles, RMS/Centered, boolean/nullable fields, and rebalance selection; obsolete controls are hidden and old volatility layouts are flagged. Saved user configurations are not rewritten. Comparison fixtures now use the new format and are not historical parity guarantees. No database/generated-client contract change is needed: registry schemas are dynamic JSON.

Verification: 435 focused offline backend tests and eight frontend tests pass; production build, TypeScript, scoped source mypy/Ruff, frontend lint and changed-file whitespace checks pass. The existing forecast.py coverage parse warning remains. An initial collection block from an unrelated unfinished candle-inventory edit was removed by Destin; final tests ran against the normal working tree with the standard offline runner. No commit, push, migration, application startup, or live operation.


### EMAC signal EMA — 2026-11-04

Status: in progress (local, uncommitted).

EMACState now computes a MACD-style signal EMA over fast-minus-slow, configured by keyword-only signal_period (default 9, positive). signal_ema() returns a detached retained array; latest_signal reads its latest value. histogram() and latest_histogram derive EMAC minus signal without extra retained state. Existing advance/update/latest outputs remain the EMAC line. Initial seeding streams the whole input into all three EMAs even when history_size is shorter; leading-gap backfill and preserve_nans behavior remain supported. Retained storage is three bounded EMA histories plus scalar state; no input-sized intermediate EMA output is retained.

94 focused offline indicator/EMAC strategy tests pass; scoped Ruff, source mypy, and whitespace checks pass. The separate stale test_emac_v2_entry_from_flat.py cannot collect because app.backtest.strategies.emac_v2 does not exist. No strategy decision wiring, runtime operation, commit, or push.


### MACD histogram backtest strategy — 2026-11-04

Status: in progress (local, uncommitted).

The user-cloned ema/macd_hist.py now defines MACDHistParams/Config/TradeConfig/Strategy, exported and registered separately as macd_hist. Defaults retain fast_window=10 and slow_window=200 and add positive signal_window=9. The feature stage advances EMAC once per candle, processes its retained histogram, and passes that processed histogram into the cloned sizing/execution pipeline. Indicators expose fast/slow EMAs, macd, and macd_signal_<window>; raw/processed signals are macd_hist_raw and macd_hist_processed, tagged with macd_hist feature sets.

Warmup includes slow_window + signal_window - 1 alongside scaling/volatility requirements; EMAC uses the engine's effective capacity. Retention is the same three bounded EMA histories; no separate histogram history. Volatility and sizing settings remain as cloned from Example. Registry JSON schemas expose the signal window without a generated-client or database migration.

95 focused offline indicator, registry, and strategy tests pass; source mypy, scoped Ruff, and whitespace checks pass. Tests cover independent full-series histogram references through rolling windows, source selection, signal-window validation/capacity, registry isolation, and a simulated short position while MACD is positive but its histogram is negative. No application startup, live operations, commit, or push.


### Live ExampleV1 EMAC migration — 2026-11-04

Status: in progress (local, uncommitted).

After Destin deleted app/lib/signals/emac.py, live example/example_strategy.py now uses EMACState for its feature math. Each subscribed (asset_id, tf_sec) has a separate capacity-one state plus one last-consumed timestamp; persistent storage is O(subscribed streams), with no retained price window or extra signal history. The first callback seeds the full available close-price window. Later calls consume every newer close present in the supplied window; duplicate windows do not advance EMA state, and older/non-monotonic windows are rejected. State belongs to the strategy instance; normal manager teardown removes the instance. Missing candles absent from the supplied window cannot be reconstructed.

Published fast/slow EMA values and EMAC share the same state. The prior signal scaling is preserved: raw EMAC divided by unannualized 35-period simple-return RMS from the current candle window, with zero for invalid/zero volatility or nonfinite results. SOURCE remains legacy close-price behavior. Rolling EMA values intentionally retain pre-window influence rather than reseeding every callback. Bracket-order behavior, live lifecycle methods, and feature message names/contracts are unchanged.

76 focused offline tests pass, including actual callback publication with mocked order boundaries, recursive history, duplicate/catch-up behavior, asset/timeframe isolation, and flat/single-candle guards. Scoped Ruff and whitespace checks pass. Source mypy retains two pre-existing optional HyperliquidClient argument errors in unchanged placement/cancel paths; both reproduced against the original file. No live system, database, exchange operation, commit, or push. Research forward_return_metrics.py and scratch emac_cycle.py still import the deleted helper; those separate callers were not part of the requested live Example patch.


### Combo v1 backtest feature blend — 2026-11-04

Status: in progress (local, uncommitted).

Destin selected VFTI length 10, RVWAP slope length/minimum bars 1 and regression lookback 3, RSI length 10, PX RVWAP length/minimum bars 1, and signal lookback 200. Registered the Example clone separately as combo_v1 with ComboV1Params/Config/TradeConfig/Strategy. Each raw component runs through the shared process_signal pipeline, then combo_v1_stream blends the processed scalars; there is no second normalization. Four flat configurable weights default to 0.25 each and must be finite, nonnegative, and sum to one. The default therefore matches the requested arithmetic average.

Reuses existing helpers: VFTI up-minus-down volume EMAs, log-regression Slope, HL2-centered RSI, HLC3 adaptive RVWAP, and close-percent-distance PX_core. Shared RVWAP is computed once when both minimum-bar settings match. Default normalization remains min_max with SIG_SCALE_LOOKBACK=200. Percent scaling is rejected because this combo has no specified denominators. No exact TradingView script parity claim: the script has not been supplied.

No retained component state/history: feature arrays are computed from the engine's bounded candle window, including window-seeded VFTI/RSI. Temporary space is O(window capacity); existing separate centered-volatility state remains bounded per stream/role as in Example. At Destin’s request, warmup now follows the base Example max(requirements) + 1 convention: VFTI/RSI length × 2, slope minimum bars/lookback, PX minimum bars, signal-scale lookback, and enabled volatility requirements. Default warmup is 201 bars. The earlier additive 300-bar allowance and hardcoded 96-bar RVWAP allowance were removed; early normalization history may include RVWAP startup values. Example sizing/rebalance/execution is preserved. Signals expose raw/processed values for all four legs and combo_v1_processed; indicators expose slope_rvwap and px_rvwap. Dynamic registry schemas need no generated-client or database migration.

44 combo/Example-registry offline tests pass; scoped source mypy, Ruff, and whitespace checks pass. Broader run also found four existing MACD histogram test failures: tests expect macd/macd_signal indicators absent in the current independently edited MACD file. No changes to that file/tests, live runtime, database, commits, or pushes. Next: compare supplied TradingView script/outputs if exact parity is requested.


### Affine signal lookback fix — 2026-11-04

Status: in progress (local, uncommitted).

Investigating saved macd_hist run 828dc3d4-dda8-4b89-9192-3d5b90dc8f28 exposed a hardcoded 252-bar affine normalization window despite SIG_SCALE_LOOKBACK=100. signal_scale now passes its lookback argument into affine_scale; both process_signal and process_signal_last already forward SIG_SCALE_LOOKBACK. The default remains 252. Raw indicators/histograms and existing saved results are unchanged; new calculations use the configured window.

The 100-bar regression failed before the change and passes afterward; the 252-bar case preserves default behavior. 28 focused signal-processing/scaling tests, scoped Ruff, source mypy, and whitespace checks pass. No saved-run rewrite, backtest execution, live operation, commit, or push.


### MACD log-price toggle — 2026-11-04

Status: in progress (local, uncommitted).

MACDHistParams now exposes use_log_price=false. When true, the selected SOURCE is transformed with natural log before the bounded fast/slow EMAs; nonpositive inputs map to NaN without log warnings and follow existing EMAC missing-input semantics. Raw output remains MACD minus its signal EMA; shared histogram processing remains unchanged. The supplied TradingView normal_* block normalizes MACD before the signal EMA and normalizes the residual again; that separate processing order is not implemented by this toggle. No persistent state or capacity change. Dynamic parameter schemas already support booleans.

80 focused offline MACD/causal-state tests pass, plus scoped Ruff, source mypy and whitespace checks. Coverage includes log/raw source selection through rolling windows, price-unit invariance, and nonpositive inputs. Updated stale indicator assertions to match the user's existing fast/slow-only publication. No runtime operations, commits or pushes.


### Optional MACD double normalization — 2026-11-04

Status: in progress (local, uncommitted).

MACDHistParams.normalize_macd_first defaults false. Enabled mode streams every seed observation through EMAC, affine-normalizes the retained MACD using SIG_SCALE_LOOKBACK, updates a strategy-owned signal EMA, retains the normalized-MACD-minus-signal residual, and passes that history to the existing process_signal pipeline. Later calls consume one latest observation as in the original strategy. Both normalization windows use SIG_SCALE_LOOKBACK; select AFFINE and 100 for the supplied TradingView normalization order, and use_log_price=true for log source. No exact custom Utils implementation parity claim. Defaults remain the user's latest 13/26/9 and min_max/252; normalization mode is optional.

The mode adds one capacity-one signal EMA, a residual deque bounded by effective_window_cap, and one latest normalized-MACD scalar; EMAC still has three bounded histories. Initial seeding streams the entire input before truncation. Warmup adds both scaling windows to slow-plus-signal requirements. A machine-precision-relative subtraction guard prevents flat-price roundoff becoming a normalized signal. Indicators macd_normalized and macd_normalized_signal are emitted only in enabled mode; macd_hist_raw then means the residual before final processing. Disabled mode preserves the user's current empty indicator list.

90 focused MACD/causal-state offline tests pass; scoped Ruff, mypy and whitespace checks pass. Tests cover full-history reference agreement with seed sizes 1/80, rolling windows, log/raw prices, signal span 1/5, retention bounds, flat prices, and warmup. Registry schema exposes the boolean; existing catalog records need defaults refresh. No shared indicator modifications, runtime operations, commits or pushes.


### MACD warmup and absolute forecast wiring — 2026-11-04

Status: in progress (implemented locally; uncommitted).

Investigated saved runs fb9d9729-5f4e-4f82-9d9e-7315fc254b9a (EWMAC) and 5b09da8a-a4c2-49e6-b0a6-cf8c4e4c4e2f (MACD). Their forecast normalization conventions explain the main exposure gap; volatility blend horizons also differed. Refer to saved runs for metrics.

At Destin's request, MACD centered targeting now permits partial-history long-term volatility blending like EWMAC: slow_span no longer gates its warmup; fast_span × 3 and signal requirements still apply. RMS targeting and adjustment retain full-window requirements. With standard signal settings and centered slow_span=2560, MACD warmup is 253 and the shared minimum with min_candles=500 is 500. Estimator retention is unchanged; EMAC capacity still follows effective_window_cap.

Shared signal processing now passes SIG_SCALAR as absolute scaling's target_abs and SIG_SCALE_LOOKBACK as its EMA span in both array and scalar paths. Absolute-mode clipping uses ±2 × SIG_SCALAR, selected as the Carver convention after an optional clarification; other modes retain ±1. Existing absolute-mode configurations change behavior. Buffer thresholds retain forecast units; arbitrary nonzero buffers do not automatically rescale. Direct helper defaults remain 0.5/252. EWMAC's separate calibrated forecast path is unchanged.

158 focused offline tests pass; eight pre-existing MACD double-normalization tests expect indicators the current implementation does not emit. Scoped Ruff/mypy and whitespace checks pass. No runtime, database, new research execution, commit or push.


## Backtest compounding source and absolute-sizing note — 2026-11-06

Status: in progress; implemented locally at Destin's request.

StrategyTradeConfig now exposes COMPOUNDING_SOURCE=account_equity (default) or booked_pnl. BacktestStrategy.get_sizing_capital selects marked equity or MockTradingService.get_booked_account_value (existing cash ledger: initial capital plus net realized P&L including fees); static ignores the source. No extra accounting state is retained. Open P&L never changes the booked ledger; closes and fees do. Existing strategy allocation/leverage caps follow selected sizing capital; broker margin/liquidation still use marked equity. This is backtest wiring, not a live-runtime implementation. Candle inventory and AR3 allowlists accept the source.

Backtest UI labels the choice Compounding capital, hides it for static, and supplies account_equity for older saved configs. Config persistence uses existing JSON and dynamic registry schemas; no database migration or generated API client change. Selecting absolute scaling shows a small clickable info popover explaining SIG_SCALAR, twice-scalar clipping, direct mapping, base/cap saturation with leveraged capital sizing, volatility-targeting differences, and transform/mapping caveats.

356 targeted offline backend tests and 10 existing frontend config tests pass; production build and scoped Ruff/whitespace checks pass. Broader EWMAC tests have 41 existing fixture failures (missing trailing_annual_volatility); broader mypy reports legacy errors in base/mock files, and panel lint reports an existing role=status issue. Browser interaction verification remains outstanding. No runtime operations, commit, or push.


### Compounding source verified through Research MCP — 2026-11-06

Ran paired Example BTC daily backtests with original request settings (2019-11-01 through exclusive 2026-11-04, initial capital 10000, absolute scalar 10, leverage 1, unlevered capital sizing, volatility roles off, deadband 0, fees/slippage 5 bps, full retention). Only COMPOUNDING_SOURCE differs. Saved equity run: `0aaac038-6670-4873-b77d-d8cd131776cd`; booked run: `5fa8950a-992d-4629-81d2-0429fb2ed901`. Both completed with artifacts available.

Reconciled every one of 2307 scored bars per run from saved candles, forecasts, positions and fills. Pre-trade booked capital is initial capital plus prior fee-inclusive closed_pnl; equity adds previous inventory marked at current candle close. Independently computed capped signal/10 targets, floored signed deltas to BTC quantity precision, and applied the >10 USD order threshold: every saved fill delta matches, including hold bars. Cash plus saved open P&L reconciles with saved account equity to floating-point tolerance. Signals are identical; account-equity performance metrics exactly reproduce original run `481bce23-80b5-4a80-a954-438521bbcaea`. Booked mode demonstrably excludes open P&L, but generates more adjustment trades in this configuration; this is a behavioral verification, not evidence of superior performance or lower turnover. No code changes or live operations during verification.
