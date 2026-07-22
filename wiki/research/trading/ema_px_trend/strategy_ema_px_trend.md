# `ema_px_trend` Strategy — Code and Trade Logic

Companion doc for `mm_v04/backend/app/backtest/strategies/ema_px_trend.py` (registered name `ema_px_trend`). The trade logic was derived in the blind chart walk-forward recorded in [[blind_pattern_match]] (Rules v1, seven HYPE 4H windows, pre-registered predictions 2-for-3 clean + 1 disclosed contaminated miss). Read that doc for the evidence; read this one for what the code does.

## Intent

Capture Destin's hand-traded EMA/PX trend style: hold with the regime defined by the 200 EMA of closes, treat unconfirmed counter-crosses as noise, add at the line, take partials at extreme extension, and stand aside in chop. Target: net positive returns with decent Sharpe. Dev set: HYPE 4H. Real out-of-sample: other assets/timeframes.

## Architecture (three layers)

1. **`compute_trend_features`** — pure vectorized math over the candle view. No state.
2. **`transition_regime`** — pure per-bar state machine `(regime, size_frac) + features → RegimeDecision`. All rule semantics live here; unit-testable without engine context.
3. **`EmaPxTrendStrategy`** — engine shell: per-`(asset, tf)` state bookkeeping, feature/signal emission, canonical V2 position pipeline (`convert_target_notional_to_sizes → build_position_adjustment_plan → build_market_order_plan`), market order placement.

## Core quantities

- `ext_atr` = (close − EMA200) / ATR(14): volatility-normalized extension. Used for acceleration, partials, re-add band, chop release.
- `ext_pct` = (close − EMA200) / EMA200: percent extension. Sign = raw regime side; magnitude history feeds the capitulation precursor.
- `slope_atr`: EMA200 slope over `slope_window` bars in ATR/bar. Chop-gate input.
- `cross_count`: close/EMA200 crossings in trailing `stress_window` bars. Codified "regime aging / top formation" stress signature.
- `ext_pct_high/low`: extension extremes over `capitulation_lookback` bars.

Everything is close-based (prior P8): wicks affect only ATR, never regime or exits.

## Rule semantics

**R1 — regime flip.** A flip requires ALL of: (1) close on the opposite side of the 200; (2) acceleration `|ext_atr| ≥ accel_atr_mult`; (3) a structural precursor — either stress (`cross_count ≥ stress_flip_min`) or capitulation (old-regime-side extension extreme ≥ `capitulation_pct` within `capitulation_lookback`). Failing any leg → regime holds (the fake taxonomy: single sharp counter-moves against a healthy trend are noise). `capitulation_pct` is percent-based deliberately: real capitulations in the dev set ran 26–35% versus ~15% for ordinary trend extensions, which ATR units blurred. On flip, size resets to full.

**R2 — continuation add.** Full size restored when `|ext_atr| ≤ reentry_ext_atr` (price back near the line and the regime survived). This is the highest-confidence pattern from the windows (7-for-7 both directions).

**R3 — chop gate.** Target notional forced to zero while flat slope (`|slope_atr| < chop_slope_atr`) AND clustered crosses (`cross_count ≥ chop_stress_min`) AND not accelerated (`|ext_atr| < accel_atr_mult`). The third clause self-releases the gate on a decisive break with no extra state — chop signature and flip precursor are the same market condition, so gate release and regime flip resolve on the same bar.

**R4 — extension partials.** In regime-profit direction, extension ≥ `partial_ext_atr` reduces to `partial_frac`; between the partial and re-add bands the current fraction is held (hysteresis, no flapping). Remainder rides until a confirmed opposite flip.

**R5 — asymmetry.** Config `long_size_frac` / `short_size_frac` scale the two books independently.

## Dev-set discriminating events (what the params were eyeballed against)

| Event | Correct behavior | Deciding mechanism |
|---|---|---|
| Feb 2025 break down | flip short | stress precursor (flat-200 chop crosses) |
| Apr 2025 V-bottom | flip long | capitulation (~35% below) + accelerated reclaim |
| Jun + Aug 2025 dips | no flip | no precursor (Aug: ~15% July extension < 20% gate) |
| Sep 2025 break down | flip short | stress precursor (aging regime) |
| Jan 2026 V-bottom | flip long | capitulation (~26% below) |
| Jun 2026 −27% crash | no flip | never closed ≥ 1.5 ATR beyond the line |

If a backtest shows one of these resolving wrong, suspect parameters before design.

## Observability

Every bar emits indicators `ema_fast_low_{n}`, `ema_slow_close_{n}` and signal family `ema_px_trend` with components `regime`, `size_frac`, `chop_active`, `flipped`, `ext_atr`, `ext_pct`, `slope_atr`, `cross_count` — enough to audit any flip/partial/gate decision against the chart in the backtest UI.

## Known v1 simplifications (v2 candidates)

- The 10 EMA_low is computed and emitted but not load-bearing; all decisions route through the 200. Candidate: tighter long-side re-add trigger off the 10-low (priors P4/P7).
- No hold-confirmation at the line: the re-add band knife-catches deep in-regime excursions (Aug-2025 shape). Candidate: require the touch to hold N closes before restoring full size.
- Partials are a single level/fraction; the windows suggested extension-scaled laddering.
- Defaults were eyeballed from charts, not tuned; all are exposed params.

## Verification

- 14 focused unit tests in `mm_v04/backend/tests/backtest/test_ema_px_trend.py`, including negative paths (unconfirmed/unaccelerated crosses never flip, wrong-side capitulation rejected, hysteresis, NaN no-op, param-ordering validation). mypy/ruff clean.
- 2026-07-21: first backtest run by Destin completed first try with positive Sharpe (run details in the backtest UI; per research-continuity policy metrics stay there).
