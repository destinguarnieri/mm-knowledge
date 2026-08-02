# Multiple Trend Following Rules (Strategy Nine)

Status: in progress

Related process: [[research/trading/research_process_v2|Research Process V2]]

## Purpose

Evaluate a book-faithful, backtest-only implementation of Robert Carver's Strategy Nine, "Multiple Trend Following Rules," before introducing Money Machine scaling or signal-normalization variants.

Deployment target for this research is crypto perpetual futures, initially Hyperliquid. This page does not authorize a live strategy, capital allocation, runtime startup, or account/order mutation.

## Faithful Baseline

Registered strategy: `multi_speed_ewmac`.

- EWMAC fast spans: `2, 4, 8, 16, 32, 64`; each slow span is `4 × fast`.
- Eligible rules must be one of the documented cost-filtered suffix sets; each set uses Carver's supplied forecast diversification multiplier (FDM).
- Each EMA gap is divided by Carver price-unit volatility, multiplied by its fixed source forecast scalar, and capped to `[-20, 20]` before equal-weight averaging.
- The equal-weight forecast is multiplied by the suffix set's FDM and capped again to `[-20, 20]`.
- Position sizing targets annualized risk continuously: forecast `+10/-10` is one normal-risk long/short position and `+20/-20` is twice normal risk before the external per-asset cap.
- The no-trade buffer is symmetric around the optimal target and has width `10%` of the current normal-risk position. When outside the band, the strategy trades only to the nearest boundary.
- Annualization is derived from bar duration by default. An explicit factor of `16` reproduces the book's daily convention.
- The ten-year volatility component uses only causal history available at each bar; fewer than 2,560 bars does not cause failure.

## Fixed Baseline Assumptions

- `risk_target = 0.20`
- `instrument_weight = 1.0`
- `instrument_diversification_multiplier = 1.0`
- `buffer_fraction = 0.10`
- volatility span approximately `35` bars
- trailing annual-volatility window `2,560` bars, using finite causal history when shorter
- compounding sizing uses current marked equity; static sizing uses initial equity
- the existing per-asset maximum is an external safety cap, not part of Carver's forecast construction

## Current Decision

Establish the economic behavior of the faithful baseline first. Do not add min-max, affine(max), dynamic absolute scaling, or removal of price-unit-volatility normalization to the baseline strategy yet. Those are distinct research variants and should be tested one axis at a time only after the baseline is understood.

## Competing Hypotheses

1. **Book mechanism generalizes:** the diversified EWMAC family retains useful trend exposure on crypto after realistic costs.
2. **Mechanism works selectively:** performance depends materially on timeframe, instrument history, or eligible speed suffix.
3. **Apparent performance is sizing-driven:** volatility targeting and compounding dominate the result rather than forecast quality.
4. **Null:** the result does not survive costs, disjoint periods, or broader assets.

## Initial Experiment Direction

1. Freeze the faithful defaults and record the saved `run_id` for every interpreted result.
2. Reproduce the BTC `1d` lead on a disjoint window before changing parameters. Destin reported an initial Sharpe near `0.75`; the run ID and complete assumptions are not yet recorded here, so this is a lead rather than verified durable evidence.
3. Separate data-availability questions from strategy questions. Because Hyperliquid assets have different listing dates, do not force every asset into one nominal calendar window and interpret missing history as strategy failure.
4. Use two complementary cross-asset views:
   - a common-overlap cohort for like-for-like comparison; and
   - each asset's maximum eligible history, grouped by available-bar cohorts, for breadth and listing-age sensitivity.
5. Compare static versus compounding sizing as an attribution check, not as a strategy optimization.
6. Stress realistic fees, slippage, and funding before drawing a monetization conclusion.
7. Only after the faithful baseline is characterized, create separately named variants for Money Machine min-max/affine(max) scaling and signal-volatility-normalization ablations.

## Boundary Conditions and Open Questions

- Carver's forecast scalars and FDMs were calibrated on traditional daily futures; portability to crypto is an empirical question.
- The eligible speed suffix is supplied explicitly. Cost eligibility is not automatically inferred from traditional-futures turnover estimates.
- FDM may be miscalibrated for crypto correlations even if the individual EWMAC rules remain useful.
- Automatic annualization adapts to bar duration, but the `2,560`-bar trailing window remains a bar-count parameter rather than ten calendar years on intraday crypto.
- No economic result is promoted until its saved run ID, venue, timeframe, asset set, window, costs, sizing mode, and eligible speed suffix are recorded.

## Run Registry

Metrics remain in the backtest UI and saved-run tools. No verified run ID is recorded yet.

## Write Log

### 2026-08-01

Created the initial research page. Frozen the book-faithful implementation as the baseline and deferred Money Machine signal-scaling and normalization variants until baseline behavior is characterized. No live or capital action was authorized or performed.
