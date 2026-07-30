# Neutral Classification of Chapters 16–23

## Scope and evidence convention

This batch explores adaptive trend/carry allocation, alternative trend representations, cross-sectional signals, breakout, value and acceleration. It contains many diversification arguments where a weak standalone rule may still have portfolio value; those arguments remain hypotheses until replicated.

## Classification map

- **Foundations:** style timing, latent/common versus idiosyncratic movement, time-series versus cross-sectional signals, weak-signal diversification.
- **Methods:** volatility-normalized representations, common-factor removal, cost-filtered multi-horizon ensembles, incremental portfolio tests.
- **Directions:** adaptive style allocation; normalized and asset-class trend; cross-sectional momentum/carry; breakout; long-horizon value; acceleration.
- **Mixed evidence:** most alternative rules are close substitutes for, or weaker than, ordinary trend and carry.

## Foundational knowledge

- A dynamic allocator is itself a forecasting strategy and must be evaluated separately from the components it weights.
- Normalizing daily price changes before cumulation creates a scale-free price-like path. Applying trend to this representation is not identical to normalizing the final moving-average gap.
- Asset-class aggregation can denoise an individual signal while simultaneously destroying cross-instrument forecast diversification.
- Time-series momentum asks whether an instrument is rising; cross-sectional momentum asks whether it is outperforming peers. A directional implementation is not automatically market neutral.
- A rule with weak standalone Sharpe can add value only if its lower correlation survives realistic costs and stress periods.
- Closely related variations do not create the same diversification as adding instruments or distinct economic mechanisms.

## Transferable research methods

1. **Representation ablation:** hold the forecast family constant while changing only its input—adjusted price, normalized price, common asset-class price or relative price.
2. **Common/idiosyncratic decomposition:** build an asset-class reference series from point-in-time constituents, subtract it where appropriate, and separately test common and relative components.
3. **Standalone-plus-portfolio gate:** require a new rule to show either credible standalone value or stable incremental portfolio value under conservative allocation and costs.
4. **Allocation sensitivity:** evaluate broad weight regions rather than choosing the historical maximum; weak components should receive explicitly bounded weights.
5. **Horizon-family discipline:** predeclare related lookbacks, apply the same cost eligibility rule, and avoid adding multiple horizons when correlations leave little marginal information.
6. **Economic sign audit:** verify whether the proposed mechanism implies continuation, mean reversion, convexity or crash exposure before interpreting a backtest.

## Concrete research directions

### 1. Adaptive trend-versus-carry allocation

- **Textbook basis:** vary top-level trend weight from recent relative style performance, or use asset-class-specific fixed mixes.
- **Core hypothesis/question:** Is style performance persistent enough to time without chasing noise?
- **Required data:** point-in-time component returns, exposures, costs and asset-class membership.
- **Baselines:** fixed 60/40, equal style weights, static asset-class mixes and no timing.
- **Evaluation design:** freeze the timing function, account for allocator turnover, use rolling-origin tests and examine whipsaw after style reversals.
- **Major failure modes:** fitted equity exception, short history, double use of component backtests and performance chasing.
- **Continue only if:** gains persist across later periods and broad parameter ranges and exceed switching costs.

### 2. Alternative trend representations

- **Textbook basis:** ordinary EWMAC, normalized-price EWMAC and common asset-class EWMAC.
- **Core hypothesis/question:** Can alternative representations isolate cleaner trend components or diversify ordinary trend?
- **Baselines:** identical EWMAC horizons on ordinary adjusted prices; carry plus ordinary trend.
- **Evaluation design:** common universe and costs, pairwise forecast/return correlation, single-instrument versus aggregate portfolio results, and constituent/membership sensitivity.
- **Reported textbook result:** normalized trend was very similar to ordinary trend; asset-class trend helped median instruments but hurt aggregate diversification.
- **Continue only if:** incremental portfolio value survives outside the source universe and is not just exposure concentration.

### 3. Cross-sectional momentum and carry

- **Textbook basis:** subtract a normalized asset-class reference from each instrument; follow relative performance for momentum or demean smoothed carry within the class.
- **Core hypothesis/question:** Do relative rankings contain net information distinct from directional trend/carry?
- **Baselines:** market-neutral ranked books, directional trend/carry, within-class equal weight and random ranks.
- **Evaluation design:** point-in-time class membership, rank monotonicity, neutrality diagnostics, capacity, turnover and crisis correlation.
- **Reported textbook result:** both are weaker standalone; diversification supports at most modest allocations.
- **Continue only if:** low correlation produces stable net portfolio improvement without hidden class beta or a hindsight allocation.

### 4. Continuous breakout

- **Textbook basis:** map current position within the rolling high–low range to a continuous bounded forecast, smooth, scale and combine several horizons.
- **Core hypothesis/question:** Does range position add information beyond moving-average trend?
- **Baselines:** binary breakout; EWMAC trend; Donchian-style entry/exit; randomized range with matched turnover.
- **Evaluation design:** identical risk/cost pipeline, high correlation acknowledged, horizon stability and incremental forecast tests conditional on EWMAC.
- **Continue only if:** breakout adds net information or distinct tail behavior after controlling for trend exposure.

### 5. Long-horizon relative value

- **Textbook basis:** treat five-year relative underperformance within an asset class as value and mean reversion.
- **Core hypothesis/question:** Is very slow relative reversal strong and stable enough to diversify trend/carry?
- **Major failure modes:** few independent observations, changing constituents, structural repricing, weak statistical power and fitted 5% allocation.
- **Continue only if:** results survive several long historical windows, alternate two-to-ten-year horizons and conservative membership handling.

### 6. Trend acceleration

- **Textbook basis:** use the rate of change of an EWMAC forecast over its fast span as a separate signal.
- **Core hypothesis/question:** Does trend strengthening/weakening predict returns beyond trend level?
- **Baselines:** EWMAC alone; faster EWMAC; acceleration conditional on trend sign.
- **Evaluation design:** incremental regressions/buckets, matched turnover and cost, multiple horizons and reversal episodes.
- **Continue only if:** acceleration remains informative after conditioning on the level and speed of the base trend.

## Strategic capabilities

- Point-in-time asset-class membership and custom normalized class-index construction.
- Rule-level exposure, correlation and incremental-contribution attribution.
- Multi-horizon eligibility and forecast-combination engine.
- Long-history validation capable of handling sparse independent observations.

## Claims requiring independent validation

The source's style autocorrelation, asset-class exceptions, forecast scalars, FDMs, horizons, allocation percentages, correlation estimates and claimed statistical significance all require replication. The academic/economic narratives attached to momentum, value and skew-like preferences are hypotheses in this batch, not established causes.

## Source files

`chapters/16-trend-and-carry-allocation.md` through `chapters/23-acceleration.md`.
