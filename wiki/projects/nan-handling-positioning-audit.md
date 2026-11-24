# NaN handling and positioning audit

Status: in progress

Started: 2026-11-14. Owner: Destin. Scope: narrow RSI/slope padding fix delivered 2026-11-16; broader missing-data policy remains deferred.

## Purpose and current stopping point

Establish consistent meaning for missing and invalid values from indicator calculation through signal processing, target sizing, rebalance, and execution. Positioning must not silently interpret an unavailable signal as a valid neutral forecast or a valid instruction to trade.

Destin requested this running document after an affine-plus-tanh backtest raised `ValueError: signal must contain only finite values`. Inspection and offline reproductions identified conflicting policies. These are observed implementation facts, not approval of their behavior. Destin subsequently rejected the broad redesign and authorized only correcting RSI and slope padding, using the existing EMA padding pattern. Do not resume the wider policy work without a new request.

Related context: [[engineering/bounded-ema-history]], [[ops/backend-testing]], and [[sessions/current-checkpoint]]. This audit covers the inspected signal and sizing paths, not every NaN treatment in the repository.

## Narrow padding fix — 2026-11-16

Committed in mm_v04 as `3da05787` at Destin's request. RSI now pads `lookback` seed prices and slices `lookback` outputs, because RSI requires that many price changes. Both log-price and raw signed slope pad `lookback - 1` seed values via existing `pad_ta`, then slice both slope and r² back to the input length. No scaler, transform, sizing, or general missing-data policy changes.

Finite synthetic inputs now have finite output from the first observation, including short histories. RSI retains TA-Lib's flat-seed result 0 (centered RSI -1), and its previously valid tail is unchanged in the regression fixtures. Slope outputs match independent seeded OLS windows. Padding does not repair genuine gaps or invalid source data.

Verification: 36 indicator cases and two Combo affine+tanh/exponential regressions pass; Combo executes simulated orders with positions matching the transformed blend. The old indicator implementations reproduce the finite-input exception in both new Combo cases. The four-file test selection has 123 passes and 10 pre-existing failures, reproduced against old indicator code: eight stale `vfti_raw` name expectations and two missing `MIN_ADJUSTMENT_VALUE_PCT` references. Excluding those cases gives 123 passes. New/modified test files pass Ruff checks and format checks; staged whitespace check passes. No live runtime, database, external backtest, or push.

## Uniform scaler input cleanup — 2026-11-16

Destin explicitly selected replacing NaN and ±infinity with zero before scaling, rather than rejecting invalid input. Implemented in `signal_scale.py` through one `_zero_nonfinite` helper called by all five scalers and the optimized min/max last-value path. Percent denominators receive the same cleanup and retain the existing zero-denominator output of zero. Input arrays are copied, not mutated. These zeros participate in estimates; min/max no longer omits invalid samples and stddev no longer forward-fills them through its internal volatility helper. Finite-input formulas are unchanged. Transforms, buffers, sizing and indicator padding are unchanged.

Verification: 125 tests pass across scaler policy, min/max, transform pipeline and Combo tests; eight previously verified stale signal-name cases are deselected. Tests cover leading/interior/current NaN and infinities, all-NaN inputs, invalid percent denominators, scalar/full-array agreement, transforms and input non-mutation. A deterministic finite-input comparison against HEAD gives identical results for all five scalers, their last-value paths and smoothed affine. Scoped Ruff and whitespace checks pass. Committed at Destin’s request as `15cb8800`; all ATR work (including registration and tests) and unrelated `test_transform_position_units.py` were excluded. No live operations or push.

## Original affine and transform failure (before the padding fix)

Using valid synthetic candles and the existing Combo test harness with `SIG_SCALE=affine`, `SIG_TRANSFORM=tanh`, and default component lengths:

- VFTI and PX histories were finite.
- Slope had NaNs at indices 0 and 1. Its lookback-3 TA-Lib standard deviation is undefined there. The code replaces invalid correlation values, but multiplication by the still-NaN standard deviation leaves NaN.
- Centered RSI had a NaN at index 0. Its padding and slicing leave one leading unavailable observation.
- Affine scaling retained exactly those NaNs. All four latest scaled values were finite.
- `process_signal` raised for slope and RSI; `process_signal_last` succeeded on the same arrays with buffering disabled.
- Combo's `on_candle_closed` reproduced the exception because it transforms each full history before selecting its last value.

The indicators are recalculated over the supplied candle window, so unavailable values at the beginning of that window can recur after strategy warmup. This reproduction does not require corrupt source candles. It establishes a concrete cause for this configuration; the user's separate failing run was not retrieved with a run ID.

Sources in `mm_v04`:

- [Slope warmup arithmetic](../../../mm_v04/backend/app/lib/indicators/momentum/slope.py), `lr_slope`.
- [RSI padding and slicing](../../../mm_v04/backend/app/lib/indicators/momentum/rsi.py), `RSI_P`; [padding helper](../../../mm_v04/backend/app/lib/utils/pad_ta.py).
- [Affine scaling](../../../mm_v04/backend/app/lib/utils/signal_scale.py), `affine_scale`.
- [Array and scalar processing](../../../mm_v04/backend/app/lib/utils/signal_processing.py).
- [Strict transforms](../../../mm_v04/backend/app/lib/utils/signal_clamp.py).
- [Combo processing](../../../mm_v04/backend/app/backtest/strategies/combo/combo_v1.py), `_features`.

## Observed handling by stage

| Stage | Current behavior | Positioning implication or audit question |
|---|---|---|
| Absolute scaling | Cleans non-finite input to zero before the magnitude EMA; guards unavailable/zero estimates. | Invalid samples count as zero observations under the selected policy. |
| Affine scaling | Cleans non-finite input to zero before rolling max and optional EMA. | Invalid current samples output zero; history participates as zero. |
| Signed magnitude min/max | Cleans non-finite input to zero before trailing extrema; degenerate spans output zero. | Zeros now enter window minima instead of being skipped; scalar and array agree. |
| Percent scaling | Cleans numerator and denominator to zero; divides where abs(denominator) exceeds DIV_EPS. | Invalid denominator follows existing zero-denominator behavior and outputs zero. |
| Standard deviation scaling | Cleans non-finite input to zero before signal dispersion estimation; retains division guard. | Gaps affect estimates as zeros rather than being forward-filled. |
| `EMA_P` | Intended for dense input; internal NaNs can propagate into later EMA output. | Padding alone does not sanitize a sparse series. |
| `dense_fill` / `EMA_P_CLEAN` | Fills leading gaps from the first finite observation and later gaps from prior finite observations; optional output mask restores NaNs. All-invalid series remains NaN. | Filling changes estimator state. Leading backfill requires careful separation from historical tradable outputs. |
| Hard signal buffer | Array version turns NaN into zero because its comparison fails; scalar version preserves NaN. | Confirmed array/scalar discrepancy. |
| Smooth signal buffer | NaNs fall through comparison masks into initialized zeros. | Missing data becomes neutral without explicit validation. |
| Sticky signal buffers | Preserve invalid current observations as NaN; previous-sign variant uses zero when the prior sign is unavailable. | Current missingness and missing sign history receive different treatments. |
| Tanh and exponential transforms | Reject the entire scalar/array if any value is non-finite. | Strict whole-array validation rejects valid latest decisions because of historical warmup gaps. |
| Continuous `signal_to_position` | Arithmetic mapping does not itself validate the input signal. | Non-finite forecasts can reach later validation; no universal decision-boundary contract established. |
| Rebalance, exposure cap, order checks | `positions_v2` validates finite targets/deltas and rejects invalid values. | Rejection occurs downstream, unless an earlier stage has silently replaced the invalid value. |
| Volatility sizing | `normal_risk_quantity` returns zero for unavailable/nonpositive volatility or a non-finite computed quantity; other inputs have explicit validation. | An unavailable sizing input can become zero sizing. Inventory consequences need evaluation. |

Additional sources: [buffers](../../../mm_v04/backend/app/lib/utils/signal_buffer.py), [EMA helpers](../../../mm_v04/backend/app/lib/indicators/moving_averages/ema_padded.py), [position mapping](../../../mm_v04/backend/app/helpers/signal_position.py), and [position and execution checks](../../../mm_v04/backend/app/helpers/positions_v2.py).

## Original offline reproduction (before uniform scaler cleanup)

Input `[NaN, 1, NaN, 2]` produced the following, without running a backend or database:

- Absolute, target 1/span 3: `[0, 2, 0, 1.777778]`.
- Affine, window 3: `[NaN, 1, NaN, 1]`.
- Magnitude min/max, window 3: `[0, 0, 0, 1]`.
- Percent, denominator all ones: `[NaN, 1, NaN, 2]`.
- Standard deviation, span 3: `[0, 0, 0, 2.828427]`.
- Hard buffer, threshold 0.1: array `[0, 1, 0, 2]`; scalar element-by-element `[NaN, 1, NaN, 2]`.

These are diagnostic examples, not desired outputs. In particular, the absolute example demonstrates that substituting zeros affects subsequent valid estimates.

## Deferred policy questions (not an active implementation plan)

1. Define expected leading warmup, a later missing observation, invalid arithmetic, positive/negative infinity, and genuine zero separately. A single NaN value does not encode its cause.
2. Decide whether estimators skip an observation, advance time without updating, carry prior state, or become unavailable. Determine how gaps affect lookbacks and minimum valid sample counts.
3. Scaler input policy selected 2026-11-16: replace NaN and ±infinity with zero before estimates and division. See implementation above; other pipeline policies remain deferred.
4. Decide whether pointwise transforms preserve NaN markers while processing finite values, and how infinities are treated. This was proposed, not approved.
5. Define behavior when the current signal or sizing input is unavailable: no signal-driven order, explicit failure, or another deliberate policy. Holding inventory, closing it, and skipping a decision are different actions. Independent risk-reduction requirements must remain explicit.
6. Define Combo behavior when one component is unavailable: block the blend, omit/reweight, or another policy. No choice is approved; implicit zero substitution changes the blend.
7. Require array and scalar behavior to agree for the same current observation and history.
8. Decide what evidence should be exposed: validity/reason, pre-transform forecast, transformed forecast, desired target, selected target, cap, and order omission reason. Keep storage bounded and avoid an unrequested observability expansion.

Do not fix this by blanket `nan_to_num`, forward filling, or removing all validation without resolving these meanings. Those are behavior changes, not merely numerical cleanup.

## Earlier broad validation proposal (deferred)

Use offline fixtures spanning finite signals, all-zero signals, leading warmup, interior gaps, invalid latest values, all-invalid histories, infinities, zero denominators, and extreme finite values. Exercise every scaler, transform, and buffer in both array and scalar paths.

Then trace representative strategies through direct/inverse and banded mapping where applicable, volatility sizing/adjustment, rebalance, exposure caps, quantity rounding, minimum notional, and mock fills. Test flat, existing long/short, flip, and over-cap inventory cases. Verify both selected targets and emitted/omitted orders, including recovery after missing data. Expected outcomes must follow the agreed policy rather than mirror current code.

## Separate unresolved transform units issue

Saved run `767e771a-ebbd-4d56-b2d9-84e36170a82f` is a completed Combo BTC daily run with no trades, not a NaN exception. Its absolute scaler uses `SIG_SCALAR=10`, exponential transformation, direct sizing, and a rebalance buffer fraction of 0.1. The original unit-scale transform compresses component forecasts before blending; subsequent division by 10 leaves targets inside the position buffer. All saved processed observations were checked against the buffer selection from flat and selected no position. Retrieve metrics and series through saved-run tools rather than copying standard result tables here.

Normalize-transform-restore units was proposed, but no curve reference magnitude or remedy was approved. Transform placement, component-versus-blend application, and a separate no-add policy at signal extremes are also unresolved. Keep these design questions distinct from NaN handling.

## Repository state and handoff

- Narrow indicator fix and focused tests committed as `3da05787`. Existing transforms retain original unit-scale formulas and strict finite-input checks; the separate no-trade units issue is unresolved.
- The earlier experimental `backend/tests/backtest/test_transform_position_units.py` remains untracked and excluded from this commit. Its last run had two passing `none` cases and four failing transformed cases; no unit-scale remedy has been approved.
- Uniform scaler zero-input cleanup is committed as `15cb8800`. Requested padding work is complete. Broader policy questions and unrelated stale tests remain deferred, not automatic follow-up work.


## No signal scaling — 2026-11-17

Added `SignalScale.NONE` (`SIG_SCALE="none"`) to the shared strategy config and scaler. Finite values retain their magnitude; non-finite values still become zero under the existing policy. Both processing APIs retain polarity, buffers, transforms and optional clipping (default ±1). Registry JSON schema supplies the frontend option; no generated client change needed. 161 focused offline tests and scoped Ruff/whitespace checks pass. Local/uncommitted; no live operations.
