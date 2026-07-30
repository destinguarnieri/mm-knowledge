# Strategy thirteen: Trend following and carry in different risk regimes

## Purpose and central argument

Strategy thirteen modifies a system that uses EWMAC trend-following and/or carry rules by changing each rule's **forecast strength** according to the instrument's current volatility relative to its own history. The chapter's core empirical claim is that rule performance differs materially by volatility regime: both trend and carry deteriorate as volatility rises, but the deterioration is especially severe for EWMAC. A continuous down-weighting of forecasts at high relative volatility and up-weighting at low relative volatility improves the combined carry-and-trend benchmark when applied to EWMAC; the same adjustment to carry alone does not improve it.

The chapter distinguishes *a market that moves persistently* from *a market that whipsaws sharply between extremes*: both may have substantial movement/volatility, but the latter is usually harmful to trend trading. Position-risk scaling is already used to manage estimated risk; this strategy adds a forecast-level adjustment to exploit the observed relationship between a rule's profitability and volatility regime.

## Scope and baseline

- Applies to any strategy with one or more **EWMAC** or **carry** trading rules.
- The performance benchmark is **strategy eleven**, the unadjusted "plain vanilla" combination of carry and trend.
- This chapter evaluates changes relative to that common benchmark rather than carrying forward strategy twelve or examining strategy thirteen in later chapters. Part Two strategies may be implemented independently or, where appropriate, in combination.
- The analysis uses the 102-instrument **Jumbo portfolio** for pooled volatility-regime evidence and later shows aggregate Jumbo-portfolio results. The chapter says average-across-instrument results are similar.
- Source-dependent elements not redefined here—such as the strategy-three percentage-volatility estimator, EWMAC construction, carry forecast construction, forecast scaling/capping, and the exact definitions of some performance statistics—are referenced but not specified further in this chapter.

## Concepts and definitions

### Relative volatility

The volatility measure must be:

- **Backward looking**, so it can be used in trading without look-ahead.
- **Instrument specific**, since crisis events may be idiosyncratic as well as global.
- **Scale free** and consistently defined across instruments.

Let \(\sigma_{\%,i,t}\) be the current estimated percentage standard deviation of returns for market \(i\), measured with the method from strategy three. Relative volatility is current estimated percentage volatility divided by its ten-year rolling mean:

\[
V_{i,t}=\frac{\sigma_{\%,i,t}}
{\operatorname{mean}(\sigma_{i,t-2560},\sigma_{i,t-2559},\ldots,\sigma_{i,t})}
\]

| Symbol | Definition / domain |
|---|---|
| \(i\) | Market/instrument index. |
| \(t\) | Current time index (business-day observations implied). |
| \(\sigma_{\%,i,t}\) | Current estimated percentage standard deviation of returns for instrument \(i\). The source denotes it as a percentage-volatility estimate; its estimator is developed in strategy three. |
| \(V_{i,t}\) | Dimensionless relative volatility: the current estimate compared with the ten-year rolling average. |
| 256 | Assumed business days per year. |
| 2,560 | Ten years \(=10\times256\) business days; establishes the intended rolling-history length. |

Because the ratio compares a volatility estimate to its own long-run average, it permits comparison across instruments with different absolute volatility levels.

### Volatility regimes (descriptive analysis)

The author pools relative-volatility observations across the 102 Jumbo-portfolio instruments and uses backward-looking estimates of their distribution to prevent in-sample cheating. The current reference cutoffs—chosen as the 25th and 75th percentiles—are:

| Regime | Relative-volatility interval \(V\) | Definition |
|---|---:|---|
| Low | 0.28–0.77 | Below the 25th percentile. |
| Medium | 0.77–1.12 | Between the 25th and 75th percentiles. |
| High | 1.12–24.4 | Above the 75th percentile. |

Important caveats:

- The pooled distribution has a long high-volatility tail. The plotted distribution is truncated; the maximum \(V\) is 24.4.
- Although quartile cutoffs might suggest equal regime sizes, using a backward-looking distribution together with secular downward volatility trends in many assets produces approximately half the observations in low vol and roughly one quarter each in medium and high vol.
- These discrete regimes explain/analyze the evidence. The implementation deliberately does **not** rely on fixed regime boundaries.

## Evidence: rule performance by regime

Figure 56 plots Sharpe ratios for each rule, averaged across instruments and conditioned on the current volatility environment. The rule set is carry5, carry20, carry60, carry120, and EWMAC2, 4, 8, 16, 32, 64.

The source's conclusions are:

- Performance is badly degraded from low to high volatility for both rule families.
- EWMAC is particularly vulnerable: its high-volatility Sharpe ratios are negative for every plotted EWMAC speed, making those rules "sure fire losers" in the author’s characterization.
- Carry remains positive in low and medium regimes and is approximately break-even in high volatility.
- The same broad result appears for aggregate Jumbo portfolios, not just the average across individual instruments.
- The pattern is also identical on a pre-cost Sharpe-ratio basis, though the faster EWMAC rules look somewhat better relative to the others before costs.
- The author describes the figures as highly statistically significant and as passing every statistical test considered, but does not provide the tests, sample period, or p-values in this chapter.

## Method: continuous forecast adjustment

### Why not simply stop trading at high volatility?

An obvious discrete policy is to stop trading in the high regime. The chapter rejects that as the preferred implementation because crossing a threshold can force selling everything and then repurchasing it when volatility falls just below the cutoff, potentially raising trading costs substantially. It would also depend on calibration of potentially in-sample-fitted regime boundaries.

Instead, scale the forecast continuously according to the current relative-volatility quantile.

### Step 1 — Quantile of relative volatility

For each instrument, calculate the historical quantile of its current relative volatility:

\[
Q_{i,t}=\operatorname{Quantile}\!\left(V_{i,t}\ \text{in}\ \operatorname{distribution}(V_{i,0},\ldots,V_{i,t})\right)
\]

| Symbol | Definition / range |
|---|---|
| \(Q_{i,t}\) | Historical quantile/rank of \(V_{i,t}\) for instrument \(i\), calculated from observations through \(t\). It ranges from 0 (lowest value seen so far) to 1 (highest), with 0.5 denoting the historical median. |
| \(V_{i,0},\ldots,V_{i,t}\) | Instrument \(i\)'s relative-volatility history available up to \(t\). |

### Step 2 — Volatility multiplier

Calculate and smooth a multiplier:

\[
M_{i,t}=\operatorname{EWMA}_{\mathrm{span}=10}\left(2-1.5\,Q_{i,t}\right)
\]

| Symbol | Definition / condition |
|---|---|
| \(M_{i,t}\) | Smoothed, dimensionless volatility multiplier applied to a rule's raw forecast. |
| \(\operatorname{EWMA}_{\mathrm{span}=10}\) | Exponentially weighted moving average using a ten-day span. It is applied to reduce multiplier noise and trading costs; the author says the modest smoothing does not reduce efficacy. |

Before smoothing, the mapping is linear:

- At \(Q=0\), \(M=2\): multiply the forecast by two and take double the normal position.
- At \(Q=1\), \(M=0.5\): halve the forecast.

Thus, the overlay increases conviction in historically low relative-volatility conditions and reduces it in historically extreme high-volatility conditions, without a hard on/off threshold.

### Step 3 — Apply the multiplier to each rule's raw forecast

For trend, the chapter gives:

\[
\text{Raw EWMAC}(N)\text{ forecast}_{i,t}=
\frac{\operatorname{EWMA}_{N,i,t}-\operatorname{EWMA}_{4N,i,t}}
{\sigma_{\rho,i,t}}
\]

\[
\text{Adjusted raw EWMAC}(N)\text{ forecast}_{i,t}
=\text{Raw forecast}_{N,i,t}\times M_{i,t}
\]

| Symbol | Definition |
|---|---|
| \(N\) | The fast EWMAC span / rule variation; the slow EWMA uses span \(4N\). |
| \(\operatorname{EWMA}_{N,i,t}\), \(\operatorname{EWMA}_{4N,i,t}\) | Fast and slow exponential moving averages for the instrument (the chapter displays them but does not redefine their underlying price/series input here). |
| \(\sigma_{\rho,i,t}\) | Risk/volatility normalizer shown in the formula. The source does not define the \(\rho\) subscript in this chapter; it is therefore left uninterpreted here. |

For carry, first smooth the carry forecast for the selected span, then adjust it:

\[
\text{Smoothed carry (span) forecast}_{i,t}
=\operatorname{EWMA}_{\mathrm{span}}(\text{Carry forecast}_{i,t})
\]

\[
\text{Adjusted smoothed carry (span) forecast}_{i,t}
=\text{Smoothed carry (span) forecast}_{i,t}\times M_{i,t}
\]

The `span` specifies the carry-forecast smoothing span. Its exact choices and the underlying carry calculation are not reproduced in this chapter.

### Step 4 — Scale, cap, and combine as usual

After multiplying raw forecasts by \(M\), apply the normal forecast scalar and forecast cap.

- EWMAC uses the same forecast scalars as before.
- Carry’s forecast scalar must be reduced from **30 to 23**. High carry forecasts tend to coincide with low volatility; multiplying them by \(M\) therefore raises the average carry forecast, so the scalar is lowered to correct that effect.
- Forecast capping is unchanged. Even when low volatility raises the raw forecast, the final capped forecast cannot exceed **20** after the normal capping stage.
- Forecast combination is unaffected.

## Performance evaluation

The author tests three versions against unadjusted strategy eleven: adjust carry alone, EWMAC alone, or both. All figures below are aggregate Jumbo-portfolio results (Table 60).

| Metric | Strategy 11: EWMAC & carry, unadjusted | Strategy 13: adjust carry | Strategy 13: adjust EWMAC | Strategy 13: adjust both |
|---|---:|---:|---:|---:|
| Mean annual return | 26.5% | 25.5% | 30.0% | 28.9% |
| Costs | −1.1% | −1.1% | −1.2% | −1.2% |
| Average drawdown | −8.9% | −9.2% | −8.7% | −9.3% |
| Standard deviation | 20.9% | 20.5% | 21.5% | 21.6% |
| Sharpe ratio | 1.27 | 1.25 | 1.39 | 1.34 |
| Turnover | 46.5 | 47.7 | 53.1 | 53.8 |
| Skew | 0.76 | 0.74 | 0.59 | 0.43 |
| Lower tail | 1.86 | 1.82 | 1.76 | 1.73 |
| Upper tail | 1.75 | 1.73 | 1.66 | 1.61 |
| Alpha | 22.3% | 21.1% | 24.8% | 24.4% |
| Beta | 0.30 | 0.31 | 0.36 | 0.34 |

Interpretation stated by the chapter:

- **Carry-only adjustment:** no improvement. This accords with carry still profiting in medium volatility and roughly breaking even in high volatility.
- **EWMAC-only adjustment:** significant improvement—the highest mean annual return, Sharpe ratio, and alpha of the alternatives shown. Skew is somewhat worse; the suggested explanation is that the system may forgo upside on rare high-volatility occasions when it is otherwise on the right side of the trade.
- **Adjusting both:** results sit between carry-only and EWMAC-only adjustments.
- EWMAC adjustment outperformance is described as fairly consistent in cumulative relative returns (Figure 57), except in the 2008 financial crash. That was both a heightened-volatility period and a banner year for trend following, so with hindsight it was a poor time to reduce trend position sizes.

Comparison caveat: cumulative differences in returns are plotted without first equalizing standard deviations across strategies. The author notes that standard deviations are very similar, so expects this to have little effect on the conclusion.

## Figures and what they communicate

| Item | Description / message |
|---|---|
| Figure 54 | Relative volatility through time for the S&P 500 micro future. It visually shows distinct low, normal, and high-volatility periods. |
| Figure 55 | Pooled distribution of relative volatility across all instruments. Used to motivate low/medium/high regimes and demonstrates a long high-volatility tail; the displayed plot truncates the maximum. |
| Figure 56 | Average-across-instruments Sharpe ratios of carry5/20/60/120 and EWMAC2/4/8/16/32/64 by low, medium, and high-volatility regimes. Carry weakens toward high vol but is approximately break-even there; EWMAC becomes negative in high vol. |
| Table 60 | Aggregate performance comparison of the unadjusted benchmark and the three forecast-adjustment variants. EWMAC-only adjustment is best by mean return and Sharpe ratio in this table. |
| Figure 57 | Cumulative relative-return differences of the strategy-thirteen variants versus the strategy-eleven benchmark. EWMAC-adjustment outperformance is mostly consistent, with a notable 2008 exception. |
| Strategy thirteen trading plan | Compact implementation summary: compute relative volatility, rank it historically, form the ten-day-smoothed multiplier, multiply a rule's raw forecast by it, then scale/cap normally; carry scalar is 23 and forecast combination is unchanged. |

## Implementation procedure

1. For each instrument and date, estimate current percentage return volatility using the strategy-three method.
2. Compute \(V_{i,t}\) by dividing the current estimate by the mean of its ten-year (2,560 business-day) volatility history.
3. From only the instrument's history available through \(t\), compute the quantile \(Q_{i,t}\) of the current \(V_{i,t}\).
4. Compute the raw multiplier \(2-1.5Q_{i,t}\); smooth it with a ten-day-span EWMA to obtain \(M_{i,t}\).
5. Multiply each chosen raw EWMAC and/or smoothed carry forecast by \(M_{i,t}\).
6. Apply forecast scaling and capping as normal. Retain EWMAC scalars; use carry scalar 23 rather than 30.
7. Combine forecasts normally. No alteration to forecast-combination logic is specified.
8. If evaluating the method, compare variants against the common unadjusted strategy-eleven benchmark; account for the caveat that relative-return comparisons ideally standardize volatility first.

## Constraints, warnings, and edge cases

- Do not use future volatility or future distribution information: relative volatility and its quantile must be backward looking.
- Do not treat cross-instrument absolute volatility levels as directly comparable; use the scale-free relative measure.
- Avoid assuming quartile cutoffs yield 25% of realized observations in each regime when the cutoffs are estimated backward-looking and asset volatility trends secularly.
- Do not replace the continuous overlay with an abrupt high-volatility stop without considering threshold turnover and costs.
- Do not omit the carry-scalar adjustment: low-volatility conditions coincide with high carry forecasts, so the multiplier would otherwise increase their average level.
- Do not loosen the standard forecast cap because the raw forecast is boosted in low volatility; the cap remains 20.
- High volatility is not synonymous with bad trend performance in every episode. The 2008 crash is the explicit counterexample: volatility was high yet trend following performed exceptionally well, so scaling down was harmful in retrospect.
- The chapter supplies no precise rule for initial dates before a full ten-year history, no tie-handling convention for quantiles, no explicit details of the strategy-three volatility estimator, and no definitions for the displayed tail/alpha/beta metrics. Those implementation details must be obtained elsewhere rather than invented.

## Connections to other chapters

- **Strategy three:** supplies the method for estimating current percentage standard deviation of returns.
- **Strategy eleven:** provides the unadjusted combined carry-and-trend benchmark and the normal forecast-scaling/capping framework used here.
- **Strategy twelve:** explicitly not evaluated in this chapter; the Part Two approach is to compare appropriate changes with strategy eleven rather than create a sequential performance chain.

## Key takeaways

1. Relative volatility, expressed as current percentage volatility divided by its own ten-year mean, makes a cross-market, backward-looking regime signal.
2. Both carry and EWMAC weaken in higher-volatility regimes, but high volatility is particularly damaging on average to EWMAC.
3. A continuous historical-quantile multiplier \(M=\operatorname{EWMA}_{10}(2-1.5Q)\) avoids hard regime thresholds while lowering high-volatility exposure and raising low-volatility exposure.
4. In the reported combined-system test, scaling **EWMAC** forecasts produces the improvement; scaling carry alone does not.
5. The rule is an empirical average, not a guarantee: rare high-volatility trend bonanzas—specifically 2008—can be penalized by the overlay.

## Glossary

- **Carry forecast:** A forecast derived from carry; its exact underlying construction is referenced but not defined in this chapter.
- **EWMAC:** Exponentially weighted moving-average crossover trend rule; here a fast span \(N\) is compared with a slow span \(4N\).
- **Forecast cap:** The unchanged downstream ceiling of 20 on a scaled forecast.
- **Forecast scalar:** Downstream multiplicative calibration applied after raw-forecast adjustment; carry’s is reduced from 30 to 23 for this strategy.
- **Historical quantile (\(Q\)):** Rank of current relative volatility within its available historical distribution, from 0 to 1.
- **Jumbo portfolio:** The source's 102-instrument portfolio used for the pooled analysis and aggregate results.
- **Relative volatility (\(V\)):** Current estimated percentage volatility divided by its ten-year rolling average.
- **Volatility multiplier (\(M\)):** Ten-day-EWMA-smoothed multiplier constructed from the relative-volatility quantile and applied to raw forecasts.
- **Volatility regime:** Low, medium, or high range of relative volatility used for descriptive performance analysis.
