# Neutral Classification of Chapters 00–07

## Scope and evidence convention

This batch covers the introduction, futures mechanics, risk scaling, multi-instrument portfolio construction, and the progression from long-only trend filters to strength-scaled long/short trend. Rules and results are textbook proposals or reported textbook results unless explicitly marked as classifier inference.

## Classification map

| Material | Classification |
|---|---|
| Contract multiplier, expiry, rolling, P&L, carry, notional and excess return | Foundational knowledge |
| Volatility targeting, contract rounding, cost normalization and cross-market testing | Transferable research methods |
| Buy-and-hold risk premia, long-only trend, long/short trend, strength-scaled trend | Concrete research directions |
| Point-in-time contract data, lifecycle accounting, portfolio covariance and executable sizing | Strategic capabilities |
| Source-era instrument statistics and reported performance | Requires independent validation |

## Foundational knowledge

- A futures position is defined by dated contract, multiplier, quote, FX conversion, expiry and settlement—not just by a continuous ticker. Continuous exposure requires explicit rolls.
- Back-adjusted prices are analytical total/excess-return series. They are appropriate for many signal calculations but not for current notional exposure, cash P&L, or executable order prices.
- Position risk equals contract risk times contract count. Volatility targeting reverses the naive workflow: start with capital and target risk, then derive the position.
- Volatility clusters more reliably than direction. A recent EWMA blended with a long-run estimate is used to avoid both stale risk and unstable sizing.
- Diversification lowers portfolio risk only to the extent that instruments are imperfectly correlated. Restoring a portfolio risk target with an instrument diversification multiplier also restores leverage and tail exposure.
- Contract indivisibility creates a capital floor and tracking error. A theoretically valid rule can be unusable when the risk-equivalent position rounds to zero or jumps in coarse increments.
- Trend direction and trend strength are separate quantities. A crossover sign determines direction; a volatility-normalized forecast magnitude controls exposure.

## Transferable research methods

1. **Risk-first sizing:** calculate current contract risk from price, multiplier, FX and a point-in-time volatility forecast; size against an explicit portfolio-risk budget; round only at the execution boundary.
2. **Forecast normalization:** divide a raw price signal by price-change volatility, scale its pooled average absolute value to a common target, and cap extremes before position sizing.
3. **Cross-market replication:** test common rules across many instruments and asset classes, while preserving instrument-specific liquidity, contract and cost constraints.
4. **Cost in Sharpe units:** translate spread and commission into risk-adjusted cost per trade, combine with expected turnover, and exclude rules too fast for a given instrument.
5. **Granularity-aware portfolio tests:** report both unrounded theoretical positions and integer executable positions at realistic capital levels.
6. **Dynamic versus static exposure comparison:** distinguish a signal's value from the effect of continuously resizing for volatility, capital, price and FX.
7. **Portfolio-level evidence:** compare median single-instrument results with the aggregate portfolio; a weak average component may still add diversified portfolio value.

## Concrete research directions

### 1. Cross-asset risk-premium baseline

- **Textbook basis:** continuously hold futures expected to have positive premia, or short structurally negative-premium instruments, with explicit rolling and costs.
- **Core hypothesis/question:** Which premia remain positive and diversifying after current roll, financing, spread, margin and tail costs?
- **Applicable markets:** liquid futures across rates, equities, FX, commodities, volatility and crypto.
- **Required data:** dated contracts, multipliers, FX, rolls, executable quotes, margin and lifecycle rules.
- **Meaningful baselines:** cash; unscaled one-contract exposure; equal notional; equal risk.
- **Evaluation design:** point-in-time instrument eligibility, multiple roll conventions, volatility scaling, cost stress and tail analysis.
- **Major failure modes:** hindsight instrument selection, adjusted-price misuse, hidden leverage, stale contract metadata and crisis concentration.
- **Continue only if:** net premia survive across instruments, regimes and plausible roll/cost conventions without depending on a few historical winners.

### 2. Volatility-targeted multi-market portfolio

- **Textbook basis:** Strategies 2–4 progress from fixed risk, to variable risk, to a weighted portfolio with an instrument diversification multiplier.
- **Core hypothesis/question:** Does point-in-time volatility scaling and broad diversification produce more stable realized portfolio risk without destroying net return?
- **Candidate methods/rules:** EWMA volatility blended with a long-run mean; risk parity or bounded hand-set weights; covariance-aware portfolio multiplier.
- **Baselines:** fixed contracts, fixed notional, unscaled buy-and-hold and equal-risk without multiplier.
- **Evaluation design:** forecast-versus-realized risk calibration, volatility jumps, correlation shocks, contract rounding, turnover and capital cohorts.
- **Continue only if:** realized risk is better controlled across regimes and the improvement remains net of resizing costs and integer-position effects.

### 3. Long-only versus long/short slow trend

- **Textbook basis:** EWMAC(64,256) is used as long/flat and long/short, with variable-risk sizing.
- **Core hypothesis/question:** Is crisis/downtrend participation worth the loss of long-premium exposure and added short-side implementation risk?
- **Baselines:** risk-scaled long-only; sign-only long/short; buy-and-hold portfolio.
- **Evaluation design:** identical risk and costs, decomposition by long and short state, regime slices, drawdown and skew, and portfolio diversification contribution.
- **Major failure modes:** implicit long bias, slow reversal response, back-adjustment errors and short-side contract constraints.
- **Continue only if:** long/short improves portfolio-level net outcomes across several downtrends rather than one crisis episode.

### 4. Strength-scaled trend forecast

- **Textbook basis:** risk-normalize the slow EWMAC gap, scale the average absolute forecast to 10, cap at ±20, and size continuously.
- **Core hypothesis/question:** Does forecast magnitude contain incremental information beyond trend sign?
- **Baselines:** sign-only EWMAC; capped versus uncapped; static versus dynamic position size.
- **Evaluation design:** monotonic forecast buckets, later-period tests, parameter-neighborhood stability and cost-aware sizing.
- **Continue only if:** forward risk-adjusted return is reasonably monotonic through the usable forecast range and survives cap/scalar perturbations.

## Strategic capabilities

- Point-in-time futures security master and contract-lifecycle engine.
- Back-adjusted research series kept separate from executable dated-contract prices.
- Risk, covariance, FX, margin, cost and integer-position sizing services.
- Cross-market portfolio simulator with roll, liquidity, turnover and tail diagnostics.
- Forecast registry preserving raw signal, scalar, cap, position and realized outcome.

## Source-specific material

The 32-day volatility span, 30/70 short/long blend, 64/256 EWMAC, forecast scale of 10, cap of 20, illustrative 20% risk target, four-contract capital heuristic and instrument tables are source defaults—not universal constants.

## Claims requiring independent validation

- Reported benefits of volatility scaling, diversification multipliers and each trend variation.
- The stability of the source's volatility forecast and long-run risk estimates.
- Historical premia, asset-class medians, liquidity thresholds, contract specifications and cost estimates.
- Any inference from the author's 102-instrument universe to a current or narrower deployment universe.

## Source files

`chapters/00-introduction.md` through `chapters/07-slow-trend-following-trend-strength.md`.
