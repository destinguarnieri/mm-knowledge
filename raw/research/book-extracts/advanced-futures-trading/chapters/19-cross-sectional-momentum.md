# Strategy nineteen: Cross-sectional momentum

## Purpose and central argument

This strategy converts an instrument's performance **relative to its own asset class** into a directional forecast. It is therefore cross-sectional momentum: an instrument that has outperformed its asset class is more likely to receive a long forecast, and one that has underperformed is more likely to receive a short forecast. The strategy is not a market-neutral relative-value book: its forecast is fed into the book's usual position-sizing framework, so the resulting equity (or other asset-class) positions need not balance to zero market exposure.

The chapter finds that standalone cross-sectional momentum is much weaker than the book's trend rules, but is less correlated with carry and trend following. A small allocation can therefore be useful for diversification; the chapter's 15% allocation did not clearly improve its backtest, while a 5% allocation would have produced a small improvement. The author uses 12% in his own system, preferring diversification to maximum backtested Sharpe ratio.

## Context and key distinctions

- **Time-series momentum / trend following:** Buy an instrument that has risen and sell one that has fallen, based on its absolute performance. This is the convention used by traditional futures traders and by earlier strategies in the book.
- **Cross-sectional momentum:** Buy an instrument that has risen *more than its relevant index/asset class* and sell one that has fallen relative to it. The academic finance convention treats momentum as a long–short, market-neutral basket of stocks.
- **This strategy versus relative value:** It uses a relative price, but is classified with trend/carry strategies because it creates a trading-rule forecast and then applies the book's standard position-sizing method. Part Five relative-value strategies instead use different sizing/trading methods designed around market neutrality.
- The chapter explicitly connects the idea to Fama and French's cross-section-of-expected-returns work (1992) and Carhart's addition of a momentum factor (1997).

## Inputs, definitions, and units

| Symbol / term | Meaning | Units / domain |
|---|---|---|
| \(i\) | Instrument | An eligible futures instrument |
| \(t\) | Day/time index | Trading-day index |
| \(P^N_{i,t}\) | Normalised price of instrument \(i\), constructed in Strategy 17 | Scale-free, volatility-normalised units |
| \(A_{i,t}\) | Normalised price of the relevant asset class for instrument \(i\), from Strategy 18 | Same scale-free, volatility-normalised units as \(P^N\) |
| \(R_{i,t}\) | Relative price | Scale-free normalised units |
| \(H\) | Look-back horizon | Positive number of business days |
| \(n\) | Horizon/rule identifier | One of 5, 10, 20, 40, 80, 160 days |
| \(\operatorname{EWMA}_{s}(x)\) | Exponentially weighted moving average of \(x\) with span \(s\) | Span in days; output retains \(x\)'s units |
| Forecast scalar | Per-horizon multiplicative calibration constant | Table 80 |
| FDM | Forecast diversification multiplier applied to a combined forecast | Dimensionless |

## Core method

### 1. Construct relative price

\[
R_{i,t}=P^N_{i,t}-A_{i,t}
\]

Subtraction is valid because both inputs have the same scale-free volatility-normalised units. Rising \(R\) means instrument \(i\) is outperforming its asset class; falling \(R\) means underperformance.

**Data edge case.** In the S&P 500 micro-futures example, the asset-class and instrument prices are identical before 2000 because the S&P 500 is the only equity instrument in the data. \(R\) is then zero. Those zeros are removed before continuing, to avoid zero forecasts that would disrupt the position-scaling equations. The source does not specify a general missing-data policy beyond this removal.

### 2. Measure average relative outperformance

\[
\operatorname{Outperformance}_{i,t}^{(H)}=\frac{R_{i,t}-R_{i,t-H}}{H}
\]

This is average relative-price change over \(H\) days. Longer \(H\) targets a slower trend, analogous to using a longer moving-average-crossover span. Its unit is normalised-price units per day.

### 3. Smooth into the raw forecast

\[
\operatorname{RawForecast}_{i,t}^{(H)}=
\operatorname{EWMA}_{H/4}\!\left(\operatorname{Outperformance}_{i,t}^{(H)}\right)
\]

The chapter uses an EWMA smoothing span equal to one quarter of the horizon. No division by the volatility of \(R\) is needed because both source prices are already normalised. The \(H/4\) ratio was selected arbitrarily to avoid fitting; sensitivity checks found performance not overly sensitive to its exact value.

**Integer-span implementation condition.** The software requires integer spans, so use the rounded value of \(H/4\), subject to a minimum span of two days. Thus the 5-day horizon uses a 2-day smoother.

### 4. Scale and cap each horizon forecast

\[
\operatorname{ScaledForecast}_{n,i,t}=
\operatorname{RawForecast}_{n,i,t}\times\operatorname{ForecastScalar}_{n}
\]

\[
\operatorname{CappedForecast}_{n,i,t}=
\max\bigl(\min(\operatorname{ScaledForecast}_{n,i,t},20),-20\bigr)
\]

The absolute forecast cap is 20. Apply it after scaling every individual horizon; apply it again after combining/scaling forecasts.

## Horizon set and per-horizon scalars

The horizon sequence starts at five business days (roughly one week) and doubles each successive horizon, following the same rationale used for EWMAC filter speeds.

| Rule | Horizon | Smoothing span | Forecast scalar |
|---|---:|---:|---:|
| Horizon5 | 5 days | 2 days | 56.1 |
| Horizon10 | 10 days (~2 weeks) | 3 days | 79.0 |
| Horizon20 | 20 days (~1 month) | 5 days | 108.5 |
| Horizon40 | 40 days (~2 months) | 10 days | 153.5 |
| Horizon80 | 80 days (~4 months) | 20 days | 217.1 |
| Horizon160 | 160 days (~8 months) | 40 days | 296.8 |

## Combining multiple horizons

1. For each instrument, discard rule variations that are too expensive to trade, using the turnover information below (and the book's existing cost-threshold process).
2. Equally weight the selected horizons.
3. Apply the FDM corresponding to the available set of horizons.
4. Cap the combined, scaled forecast at \(\pm20\).
5. Use the standard downstream stages of Strategy 9 for standalone use, or Strategy 11 when combined with carry: variable risk estimate and the book's usual position-sizing methodology.

The author refers to this selection/weighting process as the **handcrafting method** introduced in Strategy 9. The present chapter does not restate its full mechanics.

### Turnover by horizon (Table 83)

Annual turnover, averaged across instruments:

| Rule | Turnover |
|---|---:|
| Horizon5 | 120.1 |
| Horizon10 | 80.6 |
| Horizon20 | 35.5 |
| Horizon40 | 17.4 |
| Horizon80 | 8.5 |
| Horizon160 | 4.1 |

### Forecast weights and FDM for a standalone strategy (Table 84)

| Available horizons | Equal weight per included horizon | FDM |
|---|---:|---:|
| 5, 10, 20, 40, 80, 160 | 0.1667 | 1.49 |
| 10, 20, 40, 80, 160 | 0.20 | 1.40 |
| 20, 40, 80, 160 | 0.25 | 1.30 |
| 40, 80, 160 | 0.333 | 1.21 |
| 80, 160 | 0.5 | 1.11 |
| 160 | 1.0 | 1.0 |

For a strategy combined with carry and/or trend following, use the FDM values in Table 52 (page 234), rather than Table 84. The chapter says to choose weights by the same top-down method used previously but does not reproduce all weights in this chapter.

## Figure and diagram interpretation

- **Figure 72 — Construction of relative price for S&P 500:** Shows normalised S&P 500 price, its normalised asset-class price, and their difference. Before 2000, the two are identical and relative price is zero due to the single-equity-instrument data limitation. After 2000, the relative line departs from zero: the S&P underperforms from the technology crash through the 2008 financial crisis, then has a long period of outperformance.
- **Trading-plan diagram:** Restates the operational sequence: choose eligible instruments; use Table 83 to select affordable rules; calculate \(R\), outperformance, and smoothed forecast; scale using Table 80; cap each forecast; allocate weights via Strategy 9's handcrafting method; use Table 84 FDM standalone or Table 52 with carry/trend; then apply the standard downstream risk/position process.

## Results: individual horizons

All following individual-rule results are for the aggregated **Jumbo portfolio**, including all instruments even when a rule would be too expensive for an individual instrument to trade.

### Shorter horizons (Table 81)

| Metric | H5 | H10 | H20 |
|---|---:|---:|---:|
| Mean annual return (gross) | −0.9% | 5.2% | 9.8% |
| Mean annual return (net) | −13.8% | −4.3% | 5.6% |
| Costs | −12.7% | −9.4% | −4.1% |
| Standard deviation | 21.1% | 21.3% | 20.3% |
| Sharpe ratio | −0.65 | −0.20 | 0.28 |
| Turnover | 598 | 407 | 172 |
| Skew | 0.59 | 0.55 | 0.35 |
| Lower tail | 1.50 | 1.44 | 1.54 |
| Annualised alpha (gross) | −3.9% | 3.4% | 7.1% |
| Annualised alpha (net) | −16.6% | −6.0% | 3.0% |
| Beta | 0.16 | 0.10 | 0.18 |

### Longer horizons (Table 82)

| Metric | H40 | H80 | H160 |
|---|---:|---:|---:|
| Mean annual return (gross) | 9.6% | 5.3% | 6.8% |
| Mean annual return (net) | 7.2% | 3.7% | 5.6% |
| Costs | −2.3% | −1.5% | −1.2% |
| Standard deviation | 19.8% | 18.6% | 18.8% |
| Sharpe ratio | 0.36 | 0.20 | 0.30 |
| Turnover | 85.9 | 46.2 | 26.4 |
| Skew | 0.20 | 0.22 | 0.14 |
| Lower tail | 1.44 | 1.49 | 1.58 |
| Annualised alpha (gross) | 6.5% | 2.4% | 4.1% |
| Annualised alpha (net) | 4.2% | 0.8% | 2.9% |
| Beta | 0.20 | 0.19 | 0.18 |

The author considers the lower Sharpe ratios unsurprising: Strategy 18 showed that a large share of an instrument's trend profit comes from its asset-class direction; stripping out that trend leaves less residual cross-sectional effect.

## Results: combined cross-sectional momentum (Table 85)

Aggregate Jumbo-portfolio comparison with earlier trend approaches:

| Metric | Strategy 9: multiple trend (back-adjusted) | Strategy 17: multiple trend (instrument normalised) | Strategy 18: multiple trend (asset-class normalised) | Strategy 19: multiple cross-sectional momentum |
|---|---:|---:|---:|---:|
| Mean annual return | 25.2% | 28.2% | 24.0% | 6.1% |
| Costs | −1.2% | −1.4% | −1.3% | −1.4% |
| Average drawdown | −11.2% | −12.9% | −14.6% | −40.0% |
| Standard deviation | 22.2% | 24.4% | 23.5% | 18.1% |
| Sharpe ratio | 1.14 | 1.15 | 0.97 | 0.34 |
| Turnover | 62.9 | 72.1 | 65.5 | 81.4 |
| Skew | 0.98 | 0.93 | 0.94 | 0.51 |
| Lower tail | 1.99 | 1.87 | 1.94 | 1.49 |
| Upper tail | 1.81 | 1.80 | 1.82 | 1.47 |
| Alpha | 18.8% | 20.1% | 15.9% | 2.4% |
| Beta | 0.43 | 0.55 | 0.46 | 0.24 |

Conclusion from the table: the strategy is relatively poor on its own, with no redeeming feature other than a slightly better lower tail according to the author. Footnote detail: equity SR is −0.05 (versus a median of 0); bonds and metals are worse. The method from Strategy 13 improves this strategy but not enough to make it interesting.

## Diversification with carry and other trend rules

Despite poor standalone results, the rule is distinct:

- Correlation with carry: **0**, versus about **0.30** for prior trend-following strategies.
- Average correlation with trend strategies: **0.31**, versus **over 0.90** among the other trend strategies.
- Adjacent-horizon correlation: about **0.70**, versus **0.87** for adjacent EWMAC filters.
- Correlation for horizons two positions apart: **0.47**, versus **0.60** for corresponding EWMAC filters.

The chapter tests adding this rule to carry plus three prior types of momentum/trend. It states that 60% of total forecast weight is allocated to divergent strategies; split across four momentum/trend types, that gives cross-sectional momentum a 15% weight in the reported test.

### Carry + momentum/trend comparison (Table 86)

| Metric | S11: carry + adjusted-price trend | S17: carry + normalised & adjusted trend | S18: carry + asset-class, normalised & adjusted trend | S19: carry + cross-sectional, asset-class, normalised & adjusted trend |
|---|---:|---:|---:|---:|
| Mean annual return | 26.5% | 27.5% | 28.3% | 27.0% |
| Costs | −1.1% | −1.1% | −1.1% | −1.1% |
| Average drawdown | −8.9% | −8.7% | −9.1% | −8.8% |
| Standard deviation | 20.9% | 20.9% | 21.7% | 20.8% |
| Sharpe ratio | 1.27 | 1.32 | 1.31 | 1.30 |
| Turnover | 46.5 | 47.6 | 46.1 | 43.9 |
| Skew | 0.76 | 0.75 | 0.71 | 0.70 |
| Lower tail | 1.86 | 1.85 | 1.85 | 1.82 |
| Upper tail | 1.75 | 1.70 | 1.81 | 1.73 |
| Alpha | 22.3% | 22.9% | 24.0% | 23.8% |
| Beta | 0.30 | 0.32 | 0.31 | 0.31 |

There is no clear improvement at the 15% allocation: it is larger than the point at which diversification benefit is overcome by the strategy's weaker standalone Sharpe ratio. A 5% allocation would show a small backtested improvement. The author's live-system choice is 12%, based on the view that correlations are more predictable than Sharpe ratios: relative momentum could outperform in future, but is very likely to remain lowly correlated.

## Assumptions, constraints, warnings, and implementation notes

- Use only instruments meeting the book's minimum capital, liquidity, and cost thresholds.
- Construct comparison only against the **relevant asset class** and use normalised series on the same scale.
- Remove the identified artificial zero-relative-price period before creating forecasts; otherwise zero forecasts interfere with position scaling.
- Fast horizons have very high turnover and strongly negative net results in the Jumbo test; cost filtering is required before combining rules for a particular instrument.
- The reported standalone results are not market-neutral and should not be interpreted as the return of an equity-neutral long–short factor portfolio.
- The reported performance is backtest evidence, not a claim of statistically strong standalone profitability: SR 0.34 is described as only barely statistically significant, and annual alpha 2.4% as not statistically significant.
- Do not infer omitted mechanics from this chapter: downstream risk sizing is referred to Strategies 9/11, the complete handcrafting method to Strategy 9, and combined-strategy FDM to Table 52 in Strategy 11's material.

## Glossary

- **Asset-class normalised price:** Scale-free volatility-normalised price series for an instrument's relevant asset class (Strategy 18).
- **Cross-sectional momentum:** Momentum measured as an instrument's performance relative to peers or an asset-class benchmark.
- **EWMAC:** Exponentially weighted moving-average crossover rule used elsewhere in the book; used here as a comparison for filter/horizon correlations.
- **EWMA:** Exponentially weighted moving average; smooths the noisy average-outperformance measure.
- **Forecast cap:** Bound of \(\pm20\) imposed on scaled individual and combined forecasts.
- **Forecast diversification multiplier (FDM):** Multiplier that compensates for diversification when combining correlated forecast rules.
- **Normalised price:** Volatility-normalised, scale-free price series.
- **Relative price:** \(P^N-A\), the normalised instrument price less the normalised asset-class price.
- **Time-series momentum / trend following:** A directional rule based on an instrument's own absolute price movement.
- **Turnover:** Annual trading activity measure used here to screen rules for cost feasibility.

## Chapter conclusions

1. Cross-sectional momentum can be built simply from normalised instrument and asset-class prices, using a horizon return in their difference followed by EWMA smoothing.
2. Its forecast should be scaled with horizon-specific constants, capped at \(\pm20\), and combined only after instrument-specific cost/turnover filtering.
3. It is materially weaker than the book's time-series trend variants as a standalone strategy, especially after transaction costs.
4. Its low correlation with carry and trend means that a modest allocation may still be rational; allocation size is the critical trade-off between diversification and weak standalone performance.
5. This is a directional forecast component, not a market-neutral relative-value implementation.

## Explicit cross-chapter connections

- **Strategy 9:** Supplies the general standalone position/risk process and the handcrafting method for forecast weights; Table 85 compares the original multiple-trend rule.
- **Strategy 11:** Supplies the process when combining with carry; Table 86 compares carry-and-trend variants.
- **Strategy 13:** Its method modestly improves this strategy, but not enough to make it interesting.
- **Strategy 17:** Defines the instrument normalised price \(P^N\); Table 85 compares its normalised-price trend implementation.
- **Strategy 18:** Defines the asset-class normalised price \(A\); shows why residual cross-sectional trend is weaker; is extended here with carry plus three trend types.
- **Table 52, page 234:** Gives FDM values for the combined carry/trend/cross-sectional set.
- **Part Five:** Covers true relative-value methods, which differ because they explicitly target market neutrality.
