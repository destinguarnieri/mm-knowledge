# EMAC 10/200 Signal-Stats Event Labels V1

Causal event and state label definitions for the signal-statistics event study. Consolidates the observation sets from the three-agent review and Destin's 2026-07-20 hypotheses (see `ema_stats_condensed_synthesis_5c512469.plan.md`). Labels only — no strategy or runtime behavior change is implied.

Parent research: [[emac-cross-10-200|EMA Cross 10/200 Research]]

## Decision supported

Determine which signal-statistic events carry incremental, causal information beyond the raw-signal baseline (zero-cross + slope), ranked by the cheapest-discriminator test order in the synthesis doc, before any strategy mapping is built.

## Fixture and fixed assumptions

- Asset/venue/timeframe: BTC, Hyperliquid, **5m** (Destin's priority interval; matches the reviewed screenshots).
- Signal: EMAC 10/200 processed through the strategy's `process_signal` pipeline (rolling min-max scaling per the run's `StrategySignalConfig`, clipped to [−1, 1] when `SIG_CLIP_MAX`). The event study must consume the exact config of the anchor run.
- **Anchor run:** `8077b0dd-e440-48d7-8e64-a4ef81d1074e` (2026-07-20) — BTC **Binance USD-M** 5m (`BTCUSDT`), 49,800 scored bars, ~2026-01-28 → 2026-07-19 UTC, complete candle load, summary retention. `emac_v4` defaults, ±0.01 hysteresis, $10k, 1x, 5 bps fees + 5 bps slippage. This is both the label fixture and the flip-only control economics for the same window.
- Companion visual run: `d82eda65-aaf0-4a76-b536-12921c6682bb` — BTC Hyperliquid 5m, 5,600 scored bars (~June 30 → July 20), full retention. Kept for UI panel parity with the reviewed screenshots (which are Hyperliquid data); not the primary fixture.
- Venue constraint (Destin, 2026-07-20): Hyperliquid serves only ~5,000 bars per timeframe. Binance USD-M has history to first listing via `candle_source: binance_usdm` (explicit `start_ms`/`end_ms` required; single-run request cap 50,000 candles; egress needs a non-US IP). Holdout can therefore be a disjoint earlier Binance 5m window.
- Cross-venue caveat: labels defined on Binance candles will not match the Hyperliquid screenshots bar-for-bar; screenshot-derived intuitions transfer as patterns, not exact events.
- Stats lookback: 200 bars (strategy default `signal_stats_lookback`).
- Computation mode: single full-series causal computation over the fixture (`sig_stats(sig, 200)`, `sig_extension(sig, 200, symetric=True)`, `sig_extension(sig, 200, symetric=False)`). Note the documented emitted-value identity caveat (2026-07-20 write log): live emissions under a sliding 512-bar window can differ from full-series recomputation. Research labels use the full-series causal identity; live parity is a separate later check.
- Holdout: one untouched fixture (different window and/or asset), selected only after label definitions are frozen, never from the reviewed screenshots.

## Input arrays

| Series | Source | Fields used |
|---|---|---|
| `sig` | `process_signal(emac(...))` | processed signal |
| Rolling | `sig_stats(sig, 200)` | `mean`, `std_dev`, `upper/lower_band_1/2` |
| Sym magnitude | `sig_extension(sig, 200, symetric=True)` | `pos_mean`, `std_dev`, `upper/lower_band_1/2`, `extension_value` |
| Asym magnitude | `sig_extension(sig, 200, symetric=False)` | `pos_mean`, `neg_mean`, `pos/neg_std_dev`, `upper/lower_band_1/2` |
| Slope | `Slope(sig, 10)` (strategy uses `fast_window`) | `slope`, `r2` |
| EMA regime | `EMA_P(close, 10)`, `EMA_P(close, 200)` | fast vs slow |

## Event grammar

- **Causality:** every label at bar `t` uses only values available at the close of bar `t`. Crossing events compare `t−1` and `t`.
- **Crossing convention (matches Threshold Engine V3):** cross-over of series `x` above level `L` at `t` ⇔ `x[t−1] < L` and `x[t] ≥ L`; cross-under ⇔ `x[t−1] > L` and `x[t] ≤ L`. Landing exactly on the level counts as crossing; starting exactly on it does not re-trigger.
- **Identity:** an event instance is `(fixture_id, label_id, bar_ts)`. At most one instance per label per bar. Repeated identical content on different bars remains distinct.
- **NaN/warmup:** any label whose required stat is non-finite at `t` or `t−1` does not fire and the bar is excluded from that label's denominator (first ~200 warmup + 200 stats bars).
- **Same-bar coincidence:** labels never suppress each other at labeling time. Within one band family, if multiple levels are crossed in one bar, all level events fire and the most extreme level is additionally marked `max_level=true` for exclusive analyses. Cross-lens coincidence is handled by the incrementality tests, not by precedence.

## State labels (mutually exclusive within each family)

| Family | States | Definition |
|---|---|---|
| `ema_regime` | `up` / `down` | `EMA10 > EMA200` on close, else `down` |
| `sign_state` | `pos` / `neg` / `zero` | sign of `sig[t]` |
| `slope_state` | `up` / `down` | sign of `Slope(sig,10).slope[t]` |
| `sym_mean_filter` | `beyond` / `inside` | `|sig[t]| > pos_mean_sym[t]` (Destin sym #1: beyond = something interesting) |
| `sym_compression` | `compressing` / `expanding` | `pos_mean_sym[t]` vs `SMA(pos_mean_sym, 200)[t]`: below ⇒ compressing (Destin sym #4, mean-band compression vs its own average) |
| `rolling_width` | `pinched` / `normal` | `std_dev_roll[t]` below its trailing 200-bar 25th percentile ⇒ pinched (chop flag) |
| `asym_dominance` | `pos_dom` / `neg_dom` / `balanced` | skew `k = (upper_band_2 − |lower_band_2|) / (upper_band_2 + |lower_band_2|)`; `k > +0.2` ⇒ pos_dom, `k < −0.2` ⇒ neg_dom |
| `asym_dormancy` | `pos_dormant` / `neg_dormant` / `none` / `both` | side occupancy (fraction of trailing 200 bars with that sign) `< 25%` ⇒ that side dormant |

## Point events

### Baseline (control family)

- `B1_zero_cross_up` / `B1_zero_cross_down`: `sig` crosses 0 (raw sign transition).
- `B2_v4_transition`: Threshold Engine V3 transition under the static ±0.01 hysteresis config (the flip-only control rule's own events; long entry `+0.01 CROSS_OVER`, etc.).
- `B3_slope_flip`: `slope_state` changes.

### Rolling lens

- `R1_surprise_1s_up/down`: `sig` crosses over `upper_band_1_roll` / under `lower_band_1_roll`. Tagged `prevailing` when the breach direction matches `ema_regime`, else `opposing`.
- `R2_surprise_2s_up/down`: same at band 2.
- `R3_mean_cross_up/down`: `sig` crosses the rolling `mean` (the known earlier-than-zero-cross trigger).
- `R4_width_pinch_enter/exit`: `rolling_width` state transition (chop gate candidate).
- `R5_mean_slope_flip`: sign change of the rolling-mean slope, defined as `lr_slope(mean_roll, 10).slope`. Disagreement covariate: `sign(mean_slope) ≠ sign(sig)` (Destin rolling hypothesis: filter/sizing input).

### Symmetric magnitude lens

Defined on `m = |sig|` against the positive band stack (`pos_mean`, `upper_band_1`, `upper_band_2`), with `direction = sign(sig)` recorded on every event.

- `S1_mean_break`: `m` crosses over `pos_mean_sym` (mean-filter activation).
- `S2_b1_break`: `m` crosses over `upper_band_1_sym`.
- `S3_b2_break`: `m` crosses over `upper_band_2_sym`.
- `S4_mean_retreat` / `S5_b1_retreat` / `S6_b2_retreat`: `m` crosses back under the respective level having been at-or-above it on `t−1`. `S6` is Destin's de-risk/exit candidate; `S5` is the agent-observed giveback-start marker; the study scores all three retreat levels side by side.
- Escalation conditionals (measured, not separate labels): `P(S2 | S1)`, `P(S3 | S2)`, and time-to-touch distributions (Destin sym #2, band-to-band).
- Continuous covariate: `extension_value` (`sig / upper_band_2_sym`).

### Asymmetric magnitude lens

Side = current `sign_state`; positive side uses `upper_band_1/2_asym`, negative side uses `lower_band_1/2_asym` mirrored.

- `A1_same_side_b1_break` / `A2_same_side_b2_break`: `sig` crosses outside the same-side band 1 / band 2.
- `A3_first_after_dormancy`: an `A1` or `A2` whose side was `dormant` (occupancy < 25%) at `t−1`. Separates occupancy-starvation breaks from genuine-size breaks (the known mechanical-compression confound).
- `A4_breakout_exit`: `sig` crosses back inside the same-side 2σ band having been outside on `t−1`. `A2` + `A4` pairs form **breakout episodes** (Destin's asym proposal; entry outside 2σ, exit back inside, flat otherwise). Episodes are labeled with entry dormancy state, entry skew, and episode duration.
- `A5_skew_flip`: `asym_dominance` state change (slow directional-bias handoff candidate).

## Conditioning covariates (recorded on every event)

`ema_regime`, regime age (bars since last `ema_regime` change), `sign_state` age, side occupancy, `rolling_width` state, `sym_compression` state, `asym_dominance` value `k`, `extension_value`, rolling `z` (`(sig − mean)/std_dev`), slope `r2`.

## Outcome measures

- Forward log return of the close at horizons **{1, 3, 6, 12, 36, 72, 144} bars** (5m–12h; long horizons added because 5m giveback windows span hours), signed by event direction where the event has one.
- MFE / MAE within each horizon (high/low path, signed by event direction).
- **Return-to-flip:** signed cumulative close-to-close return from the event bar to the next `B1` zero-cross, in the direction of the pre-flip sign. For retreat/exit candidates this is the direct "what the flip-only control subsequently gave back or gained" score — computable from candles + signal alone, no run artifacts required.
- For chop tests: outcome of the *next* `B1` following each sign cross, split by the magnitude/width states at the cross (low- vs high-magnitude sign crosses).
- For breakout episodes: episode gross return, MAE, duration, and fraction-of-trend captured vs the enclosing regime leg.

## Parameters

| Parameter | Value | Status |
|---|---|---|
| Stats lookback | 200 | structural (strategy default) |
| Slope lookback | 10 | structural (strategy uses `fast_window`) |
| Hysteresis for `B2` | ±0.01 | structural (canonical control config) |
| Dormancy occupancy threshold | 25% | analysis choice — sensitivity-check, do not optimize |
| Skew threshold θ | 0.2 | analysis choice — sensitivity-check, do not optimize |
| Width-pinch percentile | 25th over trailing 200 | analysis choice — sensitivity-check, do not optimize |
| Compression baseline | `SMA(pos_mean, 200)` | analysis choice — sensitivity-check, do not optimize |
| Horizons | 1/3/6/12/36/72/144 bars | analysis choice |

## Hypothesis → label mapping (falsifiers)

- Asymmetric handoff (H1/H2): `A3` and `A5` vs `B1` — dies if first-after-dormancy and skew flips do not beat ordinary sign crosses on forward return, MFE/MAE, or false-transition rate.
- Rolling incrementality (H3): `R1`–`R3` conditioned on `B1` + `slope_state` + `asym_dormancy` — dies if the simpler state explains outcomes.
- Chop suppression (H4): `B1` split by `sym_mean_filter`, `rolling_width`, `sym_compression` — dies if low-magnitude sign crosses are not materially worse.
- De-risk levels (Destin sym #3 vs agent 1σ): `S4`/`S5`/`S6` ranked by return-to-flip — the level whose events precede the largest subsequent giveback wins.
- Band-to-band continuation (Destin sym #2): escalation conditionals materially above unconditional touch rates, with usable time-to-touch.
- Breakout mode (Destin asym): episode economics (`A2`→`A4`) vs the flip-only control over the same window, judged net of costs at 5m.
- Null: nothing separates from `B1` + `slope_state` after conditioning — stop per the synthesis stop condition.

## Non-goals

No strategy implementation, no parameter optimization of analysis choices, no cross-asset expansion, no live/capital action. Output of the next step is an event table + conditioned outcome statistics on the anchor fixture, then the same on one holdout.

## Implementation (2026-07-20)

Script: `mm_v04/backend/app/lib/analysis/event_study/` (CLI `python -m app.lib.analysis.event_study.run_event_study --run-id <uuid> [--start-ms --end-ms]`). Read-only: run config from `bt_backtest_run`, candles from `backtest_candle`, no network fetch. Holdout mode reuses the anchor run's config over an explicit disjoint window (candles must be cached first via the normal backtest path). Outputs per fixture: `events.csv` (label table with covariates and outcomes), `label_summary.csv`, `label_horizon_summary.csv`, `b1_chop_splits.csv`, `sign_legs.csv` + `escalation.csv`, `episodes.csv` + `episode_summary.csv`, `meta.json`.

Resolved analysis choices made during implementation (frozen; not in V1 text):

- **Moving-level crossings:** cross-over at `t` compares `x[t−1]` vs `L[t−1]` and `x[t]` vs `L[t]` (band-overtake counts as a cross). This also closes every breakout episode cleanly.
- **`max_level`:** marks the terminal level of the move — outermost crossed level for breaks, innermost (deepest) for retreats/exits.
- **Warmup:** events before bar 200 (EMA warmup) are excluded entirely; the processed signal is a placeholder `0.0` there, not NaN, so sign/slope events in that region are artifacts. Matches the run's scored region (49,800 of 50,000 bars).
- **Slope ln-clamp caveat:** `lr_slope` applies `ln(max(x, eps))`, so negative signal stretches flatten and slope reads `0` there. Preserved because it is the live code path; affects `B3`/`slope_state` and `R5`/mean-slope during negative regimes.
- **Escalation conditionals:** measured per sign leg (B1-to-B1): `P(S2 after S1 | S1, same leg)` etc., with unconditional per-leg touch rates as baseline and bars-between as time-to-touch.
- **`sym_mean_filter` at B1 is near-degenerate** (|sig| ≈ 0 at a zero cross, so essentially all B1 events are `inside`); H4 chop splits should lean on `rolling_width` and `sym_compression`.
- **Semantics correction (Destin, 2026-07-20):** sym #1 was mis-scoped as a B1-bar filter state. The intent was **the mean break as the entry trigger itself** — i.e. the `S1_mean_break` event, evaluated as an entry, not `sym_mean_filter` sampled at the zero cross. Tested in interpretation as the leg-level B1-entry vs S1-entry comparison.
- **Chop-flag lookback caveat (Destin, 2026-07-20):** the 200-bar trailing window behind `rolling_width` pinch and `sym_compression` is an unvalidated free parameter — the H4 failure may be a lookback artifact rather than a hypothesis failure. Deferred check (explicitly not blocking the holdout): visually confirm the flagged compression areas match the chart-identified braid/chop regions before trusting or tuning the flag.

Anchor fixture ran: 11,953 events, 410 sign legs, 507 breakout episodes over 49,800 scored bars. Artifacts in `mm_v04/backend/app/lib/analysis/event_study/output/8077b0dd-e440-48d7-8e64-a4ef81d1074e/` (local, uncommitted).
