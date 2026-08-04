# Multiple Trend Following Rules (Strategy Nine)

Status: in progress

Related process: [[research/trading/research_process_v2|Research Process V2]]

Tags: #research/strategy #trend-following #ewmac #carver/strategy-nine #source/book-extract

## Purpose

Evaluate a book-faithful, backtest-only implementation of Robert Carver's Strategy Nine, "Multiple Trend Following Rules," before introducing Money Machine scaling or signal-normalization variants.

Deployment target for this research is crypto perpetual futures, initially Hyperliquid. This page does not authorize a live strategy, capital allocation, runtime startup, or account/order mutation.

## Book Extract Source Map

Extraction provenance and scope: [Advanced Futures Trading book-extract README](../../../../raw/research/book-extracts/advanced-futures-trading/README.md).

### Primary specification — Strategy Nine

Source: [Chapter 9 — Multiple Trend Following Rules](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/09-multiple-trend-following-rules.md).

| Research claim | Tagged source section |
|---|---|
| Strategy identity and inherited mechanics | [Purpose and central argument](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/09-multiple-trend-following-rules.md#purpose-and-central-argument) and [Scope, dependencies, and assumptions](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/09-multiple-trend-following-rules.md#scope-dependencies-and-assumptions) |
| EWMAC family and `slow = 4 × fast` | [Filter universe and design boundaries](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/09-multiple-trend-following-rules.md#filter-universe-and-design-boundaries) |
| Fixed forecast scalars | [Forecast scalars (Table 29)](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/09-multiple-trend-following-rules.md#forecast-scalars-table-29) |
| Gap divided by price risk, scalar, and individual cap | [Compute each EWMAC forecast](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/09-multiple-trend-following-rules.md#1-compute-each-ewmac-forecast) |
| Cost-filtered eligible suffix sets | [Choose tradable filters by cost](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/09-multiple-trend-following-rules.md#2-choose-tradable-filters-by-cost) |
| Cap each forecast before equal-weight averaging | [Allocate forecast weights](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/09-multiple-trend-following-rules.md#3-allocate-forecast-weights) |
| FDM suffix table and final combined cap | [Restore forecast scale and cap again](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/09-multiple-trend-following-rules.md#4-restore-forecast-scale-and-cap-again) |
| Forecast-to-position mapping and inherited buffer | [Size, buffer, and trade the position](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/09-multiple-trend-following-rules.md#5-size-buffer-and-trade-the-position) |
| Reported diversification claim | [Diversification and weight-selection evidence](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/09-multiple-trend-following-rules.md#diversification-and-weight-selection-evidence) and [Aggregate results and practical implications](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/09-multiple-trend-following-rules.md#aggregate-results-and-practical-implications) |
| Historical failure periods and anti-overfitting caution | [Historical behavior, cautions, and figures](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/09-multiple-trend-following-rules.md#historical-behavior-cautions-and-figures) |

### Inherited supporting mechanics

| Mechanic | Tagged source section | Use here |
|---|---|---|
| Centered EWMA volatility | [Chapter 3 — EWMA estimator](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/03-buy-and-hold-variable-risk-scaling.md#ewma-estimator) | Current percentage-volatility estimate rather than the repository's relative-volatility overlay. |
| `70%` current plus `30%` long-run volatility | [Chapter 3 — Blend short-run clustering with long-run mean reversion](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/03-buy-and-hold-variable-risk-scaling.md#blend-short-run-clustering-with-long-run-mean-reversion) | Causal blended annual volatility used by signal normalization and sizing. |
| Risk-targeted normal position | [Chapter 3 — Position sizing](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/03-buy-and-hold-variable-risk-scaling.md#position-sizing) | Capital × IDM × weight × risk target divided by annual percentage volatility. |
| Risk-normalized raw forecast | [Chapter 7 — Calculate a raw forecast](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/07-slow-trend-following-trend-strength.md#1-calculate-a-raw-forecast) | Establishes the EWMAC gap divided by price-unit volatility. |
| Common forecast scale of `10` | [Chapter 7 — Scale to a common forecast scale](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/07-slow-trend-following-trend-strength.md#3-scale-to-a-common-forecast-scale) | Gives forecast `±10` its normal-risk interpretation. |
| Forecast position equation and `±20` cap | [Chapter 7 — Position sizing](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/07-slow-trend-following-trend-strength.md#position-sizing) and [Cap forecasts before sizing](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/07-slow-trend-following-trend-strength.md#cap-forecasts-before-sizing) | Provides the linear forecast-to-position mapping and twice-normal limit. |
| Fast EWMAC worked formula | [Chapter 8 — Forecast, cap, and position size](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/08-fast-trend-following-long-short-trend-strength.md#forecast-cap-and-position-size) | Confirms EWMAC(16,64), scalar `4.1`, and the shared sizing equation. |
| Symmetric 10% normal-position buffer | [Chapter 8 — Buffering to reduce costs](../../../../raw/research/book-extracts/advanced-futures-trading/chapters/08-fast-trend-following-long-short-trend-strength.md#buffering-to-reduce-costs) | Defines buffer width independently of current forecast magnitude. |

### Classification tags and validation boundary

Source: [Advanced Futures Trading classification synthesis](../../../../raw/research/book-extracts/advanced-futures-trading/classification-synthesis.md).

- [Forecast architecture](../../../../raw/research/book-extracts/advanced-futures-trading/classification-synthesis.md#forecast-architecture): preserve the distinct raw signal → risk normalization → scalar → cap → combination → sizing → buffer → execution stages.
- [Transferable research methods](../../../../raw/research/book-extracts/advanced-futures-trading/classification-synthesis.md#transferable-research-methods): test point-in-time normalization, cost-speed eligibility, mechanism-first ensembles, realistic execution, stress, and negative results.
- [Trend family](../../../../raw/research/book-extracts/advanced-futures-trading/classification-synthesis.md#trend-family): classifies cost-filtered multi-speed EWMAC as a concrete research direction and trend-strength-versus-sign as a distinct question.
- [Source-specific material](../../../../raw/research/book-extracts/advanced-futures-trading/classification-synthesis.md#source-specific-material): the `20%` risk target, `32/35`-day volatility spans, `70/30` blend, EWMAC horizons, forecast scale/cap, cost speed limit, FDM/IDM tables, and compounding practices are historical source inputs—not validated crypto constants.
- [Claims requiring independent validation](../../../../raw/research/book-extracts/advanced-futures-trading/classification-synthesis.md#claims-requiring-independent-validation): independently test performance, forecast-scalar/FDM stability, eligibility/cost assumptions, and generalization from broad daily futures to Hyperliquid crypto and other bar frequencies.
- [Evidence ladder](../../../../raw/research/book-extracts/advanced-futures-trading/classification-synthesis.md#one-sheet-architecture): textbook proposal → reproduced gross baseline → point-in-time net backtest → alternate universe/regime → realistic execution → forward shadow → explicitly authorized live evidence.

### Source ambiguities retained

- Chapter 8 prints the lower/upper no-trade inequality in reverse and describes trade-to-boundary behavior inconsistently. This implementation uses the coherent nearest-boundary no-trade rule; it minimizes turnover and is explicitly treated as an interpretation of the source ambiguity.
- Chapter 7 contains an EWMAC span/scalar inconsistency in one displayed formula. Strategy Nine's explicit Table 29 scalar family and Chapter 9 calculation procedure govern this baseline.
- Chapter 9's cost eligibility and turnover inputs come from traditional daily futures. The baseline therefore accepts only documented suffix sets but does not infer Hyperliquid eligibility automatically.

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

Tagged the exact primary and inherited book-extract sections for forecast construction, volatility, sizing, FDM, buffering, and cost eligibility. Added classification tags distinguishing portable research methods from source-specific constants and independently testable claims.
