# Bounded EMA history

Status: confirmed

Destin approved keeping the current implementation after reviewing initialization and its speed comparison on 2026-10-29. Committed in mm_v04 as `3f8f36f8` on `feat/work`: `refactor: bound EMA history and share scalar updates`. All 20 migration files were committed; not pushed. The subsequent local PX Threshold Slope fix is described below. Earlier extraction commit: `f7a4243e`. See [[sessions/current-checkpoint]].

## Retention contract and footprint

`app/lib/indicators/moving_averages/ema_state.py::CausalEMAState` requires positive keyword-only `history_size`. It stores two scalar calculation values and a `deque(maxlen=history_size)` of visible outputs. Initialization streams the input, retaining at most that many outputs throughout; it does not build an input-sized EMA output array. Returned copies use O(history_size) memory. `EMACState` owns three such states (fast, slow, and signal), each with the supplied capacity, plus an initialization flag.

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

When example.py selects volatility-target sizing, it owns one map keyed by the run's asset/timeframe streams, containing one BlendedCenteredEwmaVolatility per stream. Each estimator retains scalar moments/last close plus a deque bounded by configured long_volatility_window (default 2560); storage is O(stream count × long_volatility_window), with no candle-history copies retained. Capital sizing leaves the map empty. The feature stage calls estimator.advance(closes): the estimator seeds the first available window once, then updates with the latest close before trading gates. Initialization uses the existing last-close sentinel, adding no retained state; the former Example seeding helper is removed. Features passes the snapshot to sizing without further state advancement. Capital mode computes score features from the current candle window, including when dampening is disabled, and retains no additional score history. No timestamp tracking or replay deduplication is retained; callbacks are ordered once per candle. Focused tests cover bounded retention, warmup/prefix parity through rolling windows, read-only sizing, hold-path updates, and isolation between streams. See [Example-only configuration wiring preview — 2026-11-02 — archived](../../archive/history-compaction-2026-11-23/current-checkpoint.md#example-only-configuration-wiring-preview--2026-11-02).


## Independent volatility roles — 2026-11-03

Status: in progress, superseding the template footprint description above.

Example now keys BlendedEwmaVolatility by (asset, timeframe, targeting/adjustment), retaining at most two estimators per configured stream. Each estimator keeps scalar moments/last close, an annual volatility deque capped at slow_span, and a scoring deque capped at max(fast_span, slow_span). Scores use the retained annual-volatility window; recursive return moments continue across rolling windows. No price history or timestamps are retained. Both roles disabled means no volatility state. Each active role advances once in features even when orders hold; downstream sizing and adjustment only read observations. The old BlendedCenteredEwmaVolatility import remains an alias with centered/simple-return defaults, preserving EWMAC outputs; that estimator also now maintains the bounded scoring deque. Space is O(streams × enabled roles × (slow_span + max(fast_span, slow_span))). See [Independent volatility stages and per-asset risk weights — 2026-11-03 — archived](../../archive/history-compaction-2026-11-23/current-checkpoint.md#independent-volatility-stages--2026-11-03).


## Window-based Example volatility — 2026-11-03

Status: in progress, implementation assumption following Destin's array-scoring sketch. Supersedes Example's retained-role footprint above.

Example now retains no volatility estimator/history. Each enabled role computes volatility arrays and only its requested scores from the supplied candle window, using O(window capacity) temporary arrays. No pre-window recursive influence is retained. EWMAC still uses the original BlendedCenteredEwmaVolatility scalar moments plus one long_window-bounded deque; its added score-history deque and scores() wrapper are removed. See [Requested volatility scores from price windows — 2026-11-03 — archived](../../archive/history-compaction-2026-11-23/current-checkpoint.md#independent-volatility-stages--2026-11-03).


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


## Elapsed sizing snapshot footprint — 2026-11-12

Status: in progress; committed at Destin’s request as `68b667c6`.

BacktestStrategy now owns a sizing snapshot dictionary, populated only by callers opting into periodic sizing. At most one immutable SizingSnapshot is retained per configured asset: anchor/capture timestamps, elapsed period index, interval seconds and PositionSizing (reference units plus optional maximum units). Rollover replaces the prior entry; no per-candle sizing history is retained. Space is O(configured assets) per strategy instance, independent of run length. Continuous mode removes any entry and uses fresh sizing; fresh runs start empty. No mid-run persistence/recovery was added.

Example, Kitchen Sink, MACD and Combo opt in through SIZING_REFRESH_INTERVAL_SECONDS (positive seconds; null continuous default). Kitchen Sink refreshes before its execution gate; all four retain current signal, post-mapping volatility adjustment and execution behavior. Capital and broker accounting remain live. Calculation failures do not replace retained state. Details and verification: [sizing.md](../../raw/research/concepts/sizing.md#elapsed-unit-snapshots--2026-11-12).

## ATR v1 feature state — 2026-11-16

Status: in progress (local, uncommitted; simplified by Destin).

Destin replaced the custom streaming ATR implementation with existing ATR_P over candle_view. All strategy-specific code remains in backend/app/backtest/strategies/atr/atr_v1.py. feature_state[(asset_id, tf_sec)] directly stores AtrFeatures: ATR, current upper/lower levels, signed breakout and mode. There is no AtrState, private ATR memory map, seed bookkeeping or timestamp deduplication. Retention is one immutable feature snapshot per run asset/timeframe; caller candle arrays are not retained.

ATR_P supplies the current ATR; prior snapshot levels determine strict close-based breakout (-1/0/+1). At Destin's request, mode also accepts -1/0/+1 and now starts neutral (0), changes on nonzero breakout, and holds between breakouts. Only already-processed callbacks contribute prior mode/levels; the first callback starts neutral even when its candle window contains warmup history. Drawing visibility does not gate feature calculation. No trading rules or orders.

A focused offline check through actual strategy callbacks verifies mode sequence [0, -1, -1, 1, 1, 1] and empty orders. The old 19-test suite targets the removed streaming methods and needs adaptation; its earlier passing result does not validate the current simplified implementation. No exported TradingView parity fixture or saved run. Next: continue feature review and choose trading semantics with Destin.


### Indicator package layout — 2026-11-17

Reorganized all 20 indicator modules under `backend/app/lib/indicators/` into `moving_averages` (EMA/SMA, EMA state, EMAC, MA cross stats), `momentum` (RSI, ROC, slope), `volatility` (ATR padded/anomaly/targeting), `volume` (absorption, RVWAP, VFTI, volume anomalies), `price_extension` (price_extension, px_v2), and `signal_statistics` (sig_extension, sig_extension_decomposed, sig_stats). Import directly from the grouped module; old flat module paths are removed. Updated all repository consumers, internal imports, scratch/test code, and logger paths. Calculation bodies are unchanged. 247 selected offline tests pass; nine VFTI/Combo failures reproduce on HEAD. Existing example_v3 import of absent linregslope remains unrelated. Local/uncommitted; no live operations.


### Custom ADX and padded RMA — 2026-11-17

Status: in progress (local, uncommitted).

Imported custom_adx under indicators/momentum with seven aligned fractional series: dx_signed, signed_strength, strength, agreement, cancellation_gap, positive and negative. Types live in data_models/dto/custom_adx.py. Zero first-bar DM and strict directional comparisons match the supplied Pine formulas. DM ratios use RMA_P on both sides; the common scale cancels. Agreement remains NaN for zero strength. No retained state or strategy/UI wiring.

Destin requires no Python loops in imported indicator implementations and reuse of existing padded helpers. New moving_averages/rma_padded.py RMA_P delegates to EMA_P with period 2*span-1 (alpha=1/span), inheriting pad_ta. Custom ADX reuses SMA_P or RMA_P. Both emit immediately; early results intentionally differ from Pine full-window SMA / SMA-seeded RMA. SMA_P now calls pad_ta instead of duplicating padding. RMA_P is dense-series only; internal NaNs propagate. ADX converts missing price differences to zero, as in the supplied nz expressions, and rejects infinity.

83 focused offline tests pass, including independent recurrence/formula references, prefix causality, missing/flat/trending/tied movement, invalid inputs, RMA long-series stability and existing SMA tests. Scoped new-file lint and whitespace checks pass. No TradingView export parity fixture or runtime operations.


### DPO import and CSV parity — 2026-11-17

Status: in progress (local, uncommitted). Added momentum/dpo.py DPO(source, length=21): current source minus SMA_P lagged by floor(length/2)+1, with no centered option, future access or Python loop. Initial lag slots remain NaN; padded SMA differs from full-window Pine until index length-1+lag (31 at length 21). Dense-series missing-data behavior follows SMA_P. 27 targeted tests pass.

Validated on Destin’s BINANCE_BTCUSDT.P, 60_99489.csv: 817 hourly candles, all DPO outputs from index 31 match within 7.28e-11 price units. Earlier ADX comparison on the same export identifies DM14/SMA14: all seven series match within 7.22e-15 over final 300 bars; initial exported state predates CSV history. Scratch plot_imports.py retains the original 720 Hyperliquid BTC hourly candles, adds DPO, and renders signed ADX as columns. Comparison artifacts are local scratch cache, not durable metric records. No upgrade or live operations.


### Range ratio import — 2026-11-17

Status: in progress (local/uncommitted). volatility/range_ratio.py exposes current_range, range_baseline, range_ratio and independent int8 bar_direction; types/modes in dto/range_ratio.py. Defaults: True Range, lookback20, Candle Body. High-Low and Unsigned/Close-to-Close supported. Vectorized TR falls back to high-low for missing previous close. Baseline is RMA_P(range)[1], excluding current bar. First ratio and nonpositive baseline ratios remain NaN; padded seed differs from Pine early values. No Python loops, retained state or trading integration. 32 focused offline tests and scoped lint pass. CSV default-mode comparison on the prior Binance export matches within 2.74e-12 over final300 bars. Scratch chart reuses fixed BTC candles, with range ratio colored columns.


### Prior-window range Z — 2026-11-17

Status: in progress (local/uncommitted). Existing range_ratio now also returns range_mean, range_stdev and range_z. Mean reuses SMA_P; population standard deviation uses NumPy sliding windows on pad_ta input, with exact flat windows set to zero. Both statistics are lagged one bar. Z is NaN for zero std and retains above/below-range sign independent of direction. abc_score z_score_array was not reused because it uses current-inclusive EMA/EWMA estimators. No Python indicator loops. Full-window CSV Z parity from index20 is within 1.43e-14; 37 focused tests pass. Padding differs from Pine during initial history.


### Range std wrapper revision — 2026-11-17

Status: in progress (local/uncommitted). Supersedes NumPy sliding-window implementation above: volatility/stddev_padded.py STDDEV_P wraps TA-Lib STDDEV with pad_ta, output alignment, empty/all-nonfinite guards and span1 handling. range_ratio now reuses it for prior-window std. Dense missing-data behavior follows TA-Lib; no cleaning or changes to abc_score/ewma_vol_sig. 46 focused wrapper/range tests pass; CSV Z maximum error from index20 is 1.03e-12. Direction options are only Candle Body and Close-to-Close; both direction and range-mode helpers use explicit branches ending in assert_never.


### Padded ROC and MOM — 2026-11-17

Status: in progress (local/uncommitted). Added ROC_P alongside legacy ROC in momentum/roc.py and MOM_P in momentum/mom.py. Both default to length10, call TA-Lib with pad_ta(source, length+1), and remove length padding bars. No Python indicator loops or gap cleaning. Empty/all-nonfinite inputs preserve shape. ROC uses percent units and TA-Lib zero-denominator result0; MOM uses source units. Existing ROC/ROC_SIGNAL behavior remains unchanged. 23 targeted tests pass (formulas, prefix causality, raw TA-Lib tail, zero denominators, missing recovery, invalid inputs); scoped lint/whitespace pass. No live operations.


### Reusable log returns and blend — 2026-11-17

Status: in progress (local/uncommitted). Added utils/log_returns.py: log_return(source,length=1,offset=0) computes aligned log endpoints, rolling_sum requires a complete finite contiguous window and recovers after gaps, rolling_log_return sums lag-length returns (overlapping when length>1). Missing/nonpositive/nonfinite endpoints give NaN; logs are subtracted to avoid ratio overflow. No price filling or Python indicator loops.

momentum/log_blend.py log_blend(source,length_1,length_2,fast_weight=.7,slow_weight=.3,trend_length=9) returns blend/trend/diff with types in dto/log_blend.py. Requires 1<=length_1<length_2; recent leg is log(x/x[length_1]), older leg log(x[length_1]/x[length_2]). Finite weights used literally, no normalization. EMA_P_CLEAN(preserve_nans=True) handles derived gaps; internal gaps forward-fill EMA state but remain NaN outputs. Leading outputs remain NaN. 11 targeted tests verify formulas, seeded EMA, prefix causality, history/missing recovery and validation; scoped lint/whitespace pass. No TradingView parity claim without specified leg/window settings.


### Candle-body measurements — 2026-11-17

Status: in progress (local/uncommitted). Added volatility/candle_body.py with shared local OHLC conversion/validation and two loop-free functions. directional_body_fill replaces the requested CSI name: unsigned0–10 body divided by open-to-directional-extreme; doji/zero denominator yields0. candle_body_stats(candles,length,smooth_length) returns body_size,candle_range,body_to_range,avg_body_size,relative_body_size,body_to_range_ema,relative_body_ema; typed output in dto/candle_body.py. Prior body baseline is shifted SMA_P, excluding current candle; zero range/nonpositive baseline yields NaN. EMA_P_CLEAN(preserve_nans=True) masks undefined values while forward-filling gaps for state. 11 focused formula/edge/prefix tests and scoped lint pass. No exported parity fixture, live operations or changes to legacy CSI DTO.

Related addition: momentum/log_ret_ema.py composes log_return(source,length_1) and EMA_P_CLEAN with explicit ema_length, no Python loops. 22 combined log-family tests passed.


### Candle-body API consolidated — 2026-11-17

Status: in progress (local/uncommitted). Supersedes initial candle-body API: directional_body_fill is now a 0–1 field returned by candle_body_stats, with no separate public function. Private array helper avoids repeated OHLC conversion. Shared helpers/ohlc.py ohlc_values supplies matching-shape float arrays and infinity validation for both candle_body_stats and range_ratio. Existing neutral/zero-denominator behavior retained. 40 combined candle-body/range tests and scoped lint pass.


### Indicator helper cleanup — 2026-11-17

Status: in progress (local/uncommitted). Extracted helpers/candle_direction.py candle_direction(open,close,mode) with exhaustive explicit branches, neutral doji/missing comparisons and integer-preserving comparisons. Shared by range_ratio, candle_body fill and PRI v1/v2/v3; scalar PRI variants pass only final2 bars. DirectionMode/PriceArray live in dto/candle_direction.py; range_ratio DTO re-exports DirectionMode for existing callers. Reversal conditions and ATR targets/stops retained.

Extracted utils/rolling_stats.py prior_window_stats(source,lookback), returning typed mean/stdev/z from dto/rolling_stats.py. Uses prior padded SMA/STDDEV, excludes current observation, NaN zero-std Z; replaces range_ratio private prior-statistics code. Shared OHLC conversion stays in helpers/ohlc.py. Range-mode selection and directional-body-fill formulas remain local because their current use is indicator-specific. No broad rewrite of older estimator families or repository changes made concurrently by Destin.

219 targeted tests pass across imported indicators, padded helpers, shared utilities and PRI. Includes precise int64 comparison above2^53, causality, and unchanged PRI bullish/bearish levels, targets and stops. Scoped lint/whitespace pass. No commit/push/runtime operations.


### ATR anomaly retired — 2026-11-17

Status: in progress (local/uncommitted). Destin approved replacing atr_anomaly with range_ratio after reviewing current-inclusive vs preceding ATR and distinct Z estimators. Removed volatility/atr_anomaly.py; Indicator Lab and PX Signal Bands consume range_ratio[range_ratio] and emit range_ratio signal labels. Defaults remain14 in these callers, using True Range. Params renamed range_ratio_lookback, ge2; validation alias accepts old atr_anomaly_lookback saved settings and serialization uses new name. No migration/database changes or runtime operations.

36 focused tests pass with three unrelated PX tests deselected: stale absorption mock and two MIN_ADJUSTMENT_VALUE_PCT references. Initial wider run exposed those failures; these paths were not changed. Coverage includes both parameter classes preserving legacy lookback37 and PX actual prior-baseline spike ratio10. Scoped lint/whitespace pass. Old saved runs retain historical outputs; reruns use the new formula.

### Custom ADX backtest strategy — 2026-11-17

Cloned the lightweight example into `backend/app/backtest/strategies/custom_adx.py`, registered as `custom_adx`. Uses signed_strength (S) as raw signal through the existing processor; returns only the processed custom_adx_processed signal (no indicators or raw signal), per Destin’s follow-up. Six targeted offline checks and scoped lint pass for this output contract. Parameters: length=14, smooth_length=14, smooth_method=SMA (or RMA). Example sizing/execution retained. Stateless indicator recomputes on the bounded engine window; seeds follow the first supplied bar, not full-history parity. No live runtime wiring. Six new feature/execution checks pass across SMA/RMA and rising/falling/flat inputs; discovery/default-schema checks pass.

Custom ADX follow-up — 2026-11-17: strategy now computes S_A = signed_strength * agreement as processor input, superseding signed_strength alone. Output remains custom_adx_processed only, signal_version=2; no indicators/raw emission. Undefined zero-strength agreement is retained until shared signal processing. Eight offline strategy checks (including mixed-direction SMA/RMA) and scoped lint pass.


### Candle inventory ADX features and sizing — 2026-11-19

Status: in progress

Destin requested Example's features with ADX replacing EMAC, then explicitly included volatility features and sizing. The existing registered candle_inventory strategy now computes custom ADX S_A (signed_strength * agreement), applies the shared signal processor, and emits custom_adx_processed only (signal_version=2). Parameters are length=14, smooth_length=14 and smooth_method=SMA/RMA; legacy constant signal params are rejected rather than silently ignored. Config and trade-config types remain in dto/candle_inventory.py; no shared base or separate ADX strategy was introduced.

Example's capital/risk sizing, separate targeting/adjustment volatility roles, instrument weight/diversification, sizing snapshots and rebalance configuration are available. On qualifying candles, additions use accumulation_fraction (default .1) times the absolute signal-mapped, volatility-adjusted quantity, signed by the inventory decision. Inverse mapping affects magnitude, never the decision's direction. Rebalance applies only to additions; full profit/signal exits bypass it and holds retain inventory before final capping. Risk targeting uses Example's derived limit (None when unclipped), not an additional capital cap. BPS cost floor and neutral/doji/opposite-signal policy are unchanged. These sizing choices are implementation for review, not research evidence.

Footprint: ADX and RMS compute over the bounded engine window; ADX retains no history. Centered volatility retains separate bounded estimators for targeting and adjustment, keyed by asset/timeframe as in Example. Engine usage supplies a fixed stream per instance; map cardinality follows consumed streams. Existing sizing snapshots retain one latest entry for the asset. Warmup is max(ADX length + smoothing, scale lookback, enabled volatility spans) + 1; default 253. At Destin's explicit direction, the stream/duplicate guards and unused tracking state were removed. The caller owns ordered, once-per-candle delivery; repeated delivery can add inventory again and advance centered volatility again. Dynamic registry schemas and existing frontend structured controls expose settings without a generated-client/database migration.

Validation: 192 focused offline tests pass, including original execution regressions, real ADX full/summary synthetic replay, SMA/RMA, volatility parity with Example, bounded state, risk sizing, snapshots and exit/rebalance behavior. Scoped Ruff and strict mypy (four files) pass. Broader position suite: 45 failures exactly reproduced against untouched HEAD; removed legacy MIN_ADJUSTMENT_VALUE_PCT usage is unrelated. Local/uncommitted. No historical research run or live operation.

## Example streaming RMS and Centered volatility — 2026-11-23

Example now uses EwmaReturnVolatility for both methods. Each enabled role owns one estimator per asset and timeframe. The first callback seeds the supplied closes and subsequent callbacks advance once with the newest close. Return moments survive candle-window rollover. Targeting retains slow_span annual estimates. Adjustment retains slow_span for Centered and max(fast_span, slow_span) for RMS so its relative score can warm up. Existing centered callers retain their original defaults. Verification used offline rolling-window comparisons with the batch RMS reference for both return definitions.

## Multi EWMAC normalized spread history — 2026-11-23

Status: in progress

Destin selected Example signal processing independently for each speed. Signal version 4 divides each fast-minus-slow EMA spread by close * blended annual return volatility / annualization factor, applies process_signal to each normalized history, then averages the processed forecasts equally. Carver's fixed scalars and FDM remain exclusive to the multi_speed_ewmac reference. Default signal scaling remains Example's min_max; SIGNAL_VOL defaults to RMS and supports Centered. Signal normalization, sizing, and adjustment retain separate volatility settings/states.

Each multi_ewmac stream retains one EMA output per unique span, SIGNAL_VOL.slow_span annual volatility estimates, and SIG_SCALE_LOOKBACK normalized values per speed pair. The first callback processes supplied candles in order using each bar's contemporaneous volatility; subsequent callbacks append only the newest bar. Zero/unavailable volatility produces zero raw forecasts. The caller owns ordered, once-per-candle delivery. Raw/processed forecasts are emitted for each pair and the combined signal. Warmup includes signal-volatility spans and no longer references the removed volatility_normalization_span field. Registry uses MultiEwmacTradeConfig with Example-equivalent sizing/execution.

Verification: 114 focused offline tests pass, including generic registry construction/warmup coverage and shared indicator checks. Independent pandas/numpy reference calculations match every scored raw and combined processed forecast in 12 synthetic scenarios across RMS/Centered, min_max/absolute and lookbacks 32/252/500 with candle-window rollover. Full/summary engine metrics match. Scoped strict mypy and Ruff pass. No historical backtest, live operation, commit, or push.

### Forecast and stream ownership refactor — 2026-11-23

Destin approved extracting forecast calculation, grouping stream state, and separating output formatting/execution. `lib/signals/ewmac.py:EwmacForecast` owns EMA state, signal volatility, per-speed normalized histories, forecast warmup, and detached `EwmacForecastSnapshot` outputs. `backtest/strategies/ema/multi_ewmac.py:AssetState` owns that component plus independent targeting/adjustment estimators. At Destin's follow-up request, the stream class lives alongside MultiEwmacStrategy in the strategy file; the separate state module was removed without changing either class body. The strategy holds one asset/timeframe map; stream count still follows consumed streams. Retention limits and once-per-new-candle delivery are unchanged. Snapshots contain current values only and are not accumulated internally.

`multi_ewmac.py` now orchestrates components and formats snapshot values into the existing feature messages. `helpers/backtest_execution.py:execute_market_delta` handles mock-broker order submission after sizing/rounding; it does not choose target positions. `_calculate_sizing` and `_order_size` remain structurally identical. Config types and the snapshot live in `data_models/dto/multi_ewmac.py`; old strategy-module config imports remain supported. Destin's direct StrategySignalConfig inheritance is preserved. JSON schemas, feature names and signal version 4 are unchanged.

Verification: 122 focused offline checks pass (including eight new reusable-component/execution-adapter checks), scoped strict mypy and Ruff pass. Captured pre-refactor baselines match exactly in 24 synthetic full/summary engine runs for forecasts, indicators, economic order fields, fills, position transitions, metrics, warmup, and config schemas; generated UUID/account identities are excluded. Scenarios cover both volatility methods, independent targeting/adjustment, sizing refresh, static/compounding capital, both rebalance methods, CLOSE/HLC3, flat prices, and history rollover. No historical research run, live operation, commit or push.


### Optional signal-volatility normalization — 2026-11-23

Destin selected a separate boolean that preserves the volatility settings. Shared `VolatilitySignalConfig` in dto/strategy.py extends StrategySignalConfig with `SIG_VOL_NORMALIZE` (default true) and `SIGNAL_VOL`; MultiEwmacConfig adopts it. Strategies without a wired normalization path continue using their existing config bases, so their schemas do not advertise an inactive control. This shared opt-in config supersedes MultiEwmacConfig's direct base-class inheritance described above.

EwmacForecast checks the switch before normalizing each spread. False retains raw price-unit EMA spreads, allocates no signal-volatility estimator, and excludes its spans from forecast warmup. True preserves the existing price-unit normalization and zero/unavailable-volatility behavior. Both paths retain one SIG_SCALE_LOOKBACK-bounded history per pair and apply the same subsequent signal processing. Position targeting and adjustment remain independent. Configuration is fixed during each forecast instance's lifetime.

Dynamic registry schemas expose the boolean to the existing frontend selector; the control is labeled Normalize signal by volatility. Existing saved EWMAC configs that omit the field remain enabled. No generated client or database migration is required. 127 focused backend checks, scoped typing/lint and exact enabled-mode parity across 24 synthetic full/summary engine runs pass. No historical run or live operation.

## Maximum-based position sizing — 2026-11-24

Status: confirmed (approved sizing contract; implementation committed as 06a380bf).

Supersedes the earlier Example-style mapping-derived volatility cap and unclipped/unbounded sizing descriptions on this page. calculate_sizing now returns the unlevered normal_risk_quantity as base_size and twice that quantity as max_size when volatility targeting is enabled. Allocation sizing still returns max_notional_usd / price for both fields. Signal scaling, mapping direction, and SIG_CLIP_MAX do not determine the position maximum. The volatility calculation still ignores the allocation maximum.

Continuous mapping supplies max_size as the generic signal_to_position reference and divides by full signal strength: 2 * SIG_SCALAR for absolute mode, 1 for every other mode. Absolute forecasts retain their existing units, average-magnitude target, lookback and clipping behavior. Typical absolute strength maps to half the maximum; full strength maps to the maximum. SIG_SCALAR no longer acts as an extra position divisor for non-absolute modes in the migrated pipeline. Zero remains flat. Inverse retains sign(fraction) * (1 - abs(fraction)); with clipping disabled, values beyond full strength can still reverse direction. There is no new inverse clamp.

All eight calculate_sizing callers were migrated: Example, Kitchen Sink, Custom ADX, Combo v1, MACD Hist, Multi EWMAC, Opposite Bid Trend and Opposite Bid Trend Example. Kitchen Sink full and banded mappings now use max_size. Opposite Bid accumulation already uses max_size and no longer requires signal clipping to obtain a finite cap. Rebalance buffers retain base_size. Volatility adjustment and rebalance selection precede final capping. PositionSizing.max_size is now typed float; snapshots still retain the same two quantities and timing. No additional retained state. The initial eight-caller change preserved the separate multi_speed_ewmac reference; the follow-up below supersedes that exception. Legacy mapping callers retain their existing signal mapping.

Saved configs load without schema-shape or database migration, but reruns can change: default non-absolute volatility-sized maximum doubles; non-absolute SIG_SCALAR no longer changes sizing; absolute allocation sizing maps typical strength to half the maximum; inverse/full/banded volatility sizing follows the new maximum; disabling clipping retains the cap. Existing persisted run artifacts and configs were not rewritten. Signal processing outputs and feature versions are unchanged. Backend field descriptions and frontend sizing help describe these semantics; PositionSizing is internal and absent from the generated API client.

Validation: 369 focused offline tests passed (shared sizing/mapping, signal pipeline, snapshots, registry and existing engine integration). Scoped Ruff and mypy passed for all 13 changed application modules; frontend build and scoped Biome lint passed. Coverage emitted an existing unparsable forecast.py warning; frontend emitted dependency annotation and bundle-size warnings. No historical backtest, runtime operation, commit or push.

### Single sizing function, including Carver — 2026-11-24

Destin explicitly removed the Carver exception: the independent allocation cap was his crypto-leverage adaptation, not a requirement to preserve. multi_speed_ewmac now calls calculate_sizing with its existing blended annual volatility, risk target, weight and IDM. Its maximum is twice the normal-risk base; it passes max_notional_usd=None and no longer reads the allocation maximum for sizing. Venue leverage still serves margin/accounting behavior; this change removes the separate sizing cap.

Mapping is forecast / (2 * SIG_SCALAR) * max_size, retaining the default 10-to-base and 20-to-maximum relationship. The fixed forecast scalars, FDM, ±20 forecast caps, volatility estimator, base-sized buffer, and forecast feature version are unchanged. Non-default SIG_SCALAR retains its pre-cap target arithmetic, but final exposure now uses the risk-based maximum. Invalid volatility yields zero base and maximum. Existing saved runs are not rewritten.

Removed calculate_position_sizing, its dead capital-dampening branch, and all seven obsolete sizing policy/input/request types including SizingRequest. Shared validation tests now cover calculate_sizing. The generic continuous and banded mapping argument is reference_size; Kitchen Sink's local mapping arguments are max_size. No additional history/state is retained; Carver's old immutable sizing policy was replaced by immutable VolatilitySettings used to enable targeting and carry risk_target. The recursive Carver estimator still owns volatility computation.

Verification: 360 focused offline tests passed, scoped Ruff/mypy and frontend help lint passed. Two synthetic full-engine replays produced identical 317 fills and 344 position events with allocation percentages 0.1 and 100, and exposures exceeded the former smaller cap. This is synthetic wiring verification, not a historical backtest. Local/uncommitted; no database, live runtime or deployment operation.

### MCP sizing verification and commit — 2026-11-24

Committed mm_v04 as `06a380bf` (Unify backtest sizing around a maximum position reference), 28 task files. No push. Backend MCP schemas showed the new descriptions before execution. Six single-asset Research MCP runs completed and were re-read as saved with full artifacts available. All used BTCUSDT Binance USD-M daily candles, scored [2023-01-01, 2025-01-01) UTC (731 candles each), preceding strategy warmup, initial capital 10,000, static sizing, leverage 1, fee 5 bps and slippage 5 bps. Candle loads were complete from cache with no missing bars or provider fetches.

- Example allocation sizing, min/max defaults, 10% allocation: `2a2859ec-758e-4147-b80e-fc289501b950`.
- Example volatility targeting, min/max, SIG_SCALAR=0.25, clipping off, 1% allocation: `8b1c0d9e-fdac-4e4c-bd41-650468c475aa`.
- Example volatility targeting, absolute scalar 10, direct, clipping on, 1% allocation: `49562b4e-c80b-4281-a0f3-d2ad0bf4e2f1`.
- Same Example absolute setup with inverse mapping: `e72358bf-a39d-4366-87df-3e4e63d0c572`.
- Carver defaults, 1% allocation: `af9b420b-1cea-4781-8e44-728972e84fdf`.
- Carver defaults, 100% allocation: `0422d6e7-bba0-4ae7-8340-ca17611eea7e`.

Example targeting cases used RMS with default 35/200 spans, risk target 0.2, no volatility adjustment and zero deadband. Carver retained its default Centered 35/2560 estimator and base-sized 0.1 buffer. All six runs completed without liquidation.

Reconciled recorded signals and position sizes on all 4,386 scored candles against independently calculated EWMA return moments, the normal-risk formula, direct/inverse fractions, and Carver buffer selection. Differences fit the existing 10 USD minimum-order plus one size-step tolerance; small residual inventory above a newly reduced target/cap is expected when the required order is below the execution minimum. The two Carver runs had exactly identical 438 fills and 731 position events despite different allocation settings. These checks support sizing correctness for the exercised cases, not prospective strategy profitability. Standard performance metrics remain in the saved-run tools/UI.

Earlier offline verification remains 360 passed, plus the two synthetic allocation-independence replays. No new production code changes were needed after the MCP runs. Legacy strategy config-field typing errors and three import-order warnings were previously reproduced against baseline; unrelated fixes were excluded. KB records remain local alongside pre-existing unrelated KB edits.
