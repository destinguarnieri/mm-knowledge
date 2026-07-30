# Strategy Twenty-One — Breakout

## Purpose and central argument

This strategy converts a breakout-style view of prices into a *continuous forecast* of risk-adjusted returns, rather than using a binary “in/out of the range” signal. It uses only the recent rolling minimum and maximum of a back-adjusted daily closing-price series—no Fibonacci levels or other discretionary range definitions. The forecast is strongest at the range extremes, is smoothed to reduce trading costs, then scaled and combined across several look-back horizons.

The author’s central practical conclusion is that a diversified combination of 10-, 20-, 40-, 80-, 160-, and 320-business-day breakout forecasts is tradeable subject to a cost “speed limit.” It has performance comparable to the multiple-trend system, and it can be added to trend and carry even though breakout and trend are highly correlated.

## Core idea and terminology

- **Breakout (intuitive account):** prices move inside a natural range until reaching an extreme; a break beyond the range is traditionally treated as potentially releasing pent-up buying or selling. The author does not claim to have scientifically validated this narrative.
- **Back-adjusted price:** the daily closing-price series used as the input. Denote it by \(p_t\).
- **Horizon / look-back \(h\):** number of business days over which the current range is calculated.
- **Rolling maximum / minimum:** the highest and lowest prices in the inclusive \(h\)-day look-back window.
- **Forecast:** a continuous prediction of risk-adjusted returns. Its permitted absolute maximum is 20.
- **Breakout variation:** one specified horizon, named Breakout10, Breakout20, etc.
- **EWMAC:** exponentially weighted moving-average crossover trend rule, used for comparison and combination with breakout.
- **FDM:** forecast diversification multiplier, applied after averaging diversified forecasts.
- **Jumbo portfolio:** the book’s aggregate portfolio of more than 100 instruments.

## Construction of one breakout forecast

### 1. Calculate the rolling range

For horizon \(h\) and date \(t\):

\[
\operatorname{max}_{h,t}=\max(p_t,p_{t-1},p_{t-2},\ldots,p_{t-h+1})
\]

\[
\operatorname{min}_{h,t}=\min(p_t,p_{t-1},p_{t-2},\ldots,p_{t-h+1})
\]

\[
\operatorname{mean}_{h,t}=\frac{\operatorname{max}_{h,t}+\operatorname{min}_{h,t}}{2}
\]

| Symbol | Meaning | Units / domain |
|---|---|---|
| \(p_t\) | Back-adjusted daily closing price at date \(t\) | Price |
| \(h\) | Look-back horizon | Positive integer, business days |
| \(\operatorname{max}_{h,t}\), \(\operatorname{min}_{h,t}\) | Range extrema over the last \(h\) observations, including \(t\) | Price |
| \(\operatorname{mean}_{h,t}\) | Midpoint of that rolling range | Price |

Short horizons react faster when prices move but have higher trading costs. A long horizon captures long-established ranges but trades infrequently; excessively long horizons become difficult to evaluate.

### 2. Form and smooth the raw forecast

\[
\text{Raw forecast}_{h,t}=40\,\frac{p_t-\operatorname{mean}_{h,t}}{\operatorname{max}_{h,t}-\operatorname{min}_{h,t}}
\]

\[
\text{Smoothed forecast}_{h,t}=\operatorname{EWMA}_{\text{span}=h/4}\left[\text{Raw forecast}_{h,t}\right]
\]

The raw formula locates price within its recent range. At the rolling minimum it is \(-20\); at the rolling maximum it is \(+20\). The factor 40 therefore makes the extrema coincide with the author’s permitted forecast bounds.

| Additional symbol / operation | Meaning and condition |
|---|---|
| \(\operatorname{max}_{h,t}-\operatorname{min}_{h,t}\) | Range width; the formula presupposes a non-zero range. The chapter does not specify a fallback for a zero-width range. |
| \(\operatorname{EWMA}_{\text{span}=h/4}\) | Exponentially weighted moving average applied to the *forecast*, with span one quarter of the horizon. This span choice was arbitrary to avoid overfitting, and the author subsequently checked that results were not overly sensitive to it. |

Smoothing materially reduces the raw forecast’s noise and trading costs, but causes lag. The chapter notes that applying an EWMA instead to rolling extrema would add complexity without a significant cost reduction or clear performance benefit.

### 3. Scale the variation forecast

\[
\text{Scaled forecast}_{h,i,t}=\text{Smoothed forecast}_{h,i,t}\times\text{forecast scalar}_{h}
\]

| Symbol | Meaning |
|---|---|
| \(i\) | Instrument |
| \(\text{forecast scalar}_{h}\) | Horizon-specific scalar, pooled across all instruments in the data set, chosen to give an average absolute forecast of 10 |

In theory the scaled forecast is capped at absolute value 20. Here the chapter says that cap is redundant: the pre-scaled forecast cannot exceed 20 and every listed scalar is below 1. The multiplier 40 alone would give the desired distribution only if price locations inside their ranges were uniformly distributed.

### No volatility normalization

The strategy deliberately does **not** divide by standard deviation. A tight historical range usually corresponds to lower volatility, so it naturally makes the forecast more sensitive to a small price movement. The relationship does not necessarily hold after a consistent trend: then the range can be wide relative to standard deviation, yielding a lower breakout forecast. The author considers this appropriate because the rule is intended to catch the *start* of a trend, not enlarge an already-established one. Omitting volatility normalization also reduces correlation with EWMAC trend rules, with little stated effect on outright performance.

### Important distinction from a pure binary breakout

The raw forecast is zero only when current price equals the range midpoint. Thus the strategy normally has a non-zero position before a literal range exit and gradually builds exposure into the extreme. It is therefore closer to a gradual-position trend rule than to a pure breakout rule that holds nothing until a breakout occurs. A no-position threshold around the midpoint could change this, but would increase transaction costs and introduce an overfittable parameter.

## Figures and what they show

- **Figure 74 — Back-adjusted price, rolling minimum and rolling maximum for WTI Crude Oil:** uses a 320-business-day (about 15-month) range. WTI spends the first years mostly inside the range and tests the ceiling; in October 2014 it breaks the lower range edge and an 18-month bear market follows. It illustrates why the rule reaches maximum bearishness when price hits the rolling minimum.
- **Figure 75 — Raw and smoothed breakout forecast, 320-day horizon, WTI Crude Oil:** the raw forecast is visibly noisy; the EWMA-smoothed forecast is much less noisy but lags it.
- **Strategy twenty-one trading-plan figure:** specifies long or short positions, variable risk estimate, combined forecasts from multiple breakout variations, instrument eligibility, range/forecast equations, scalar lookup, weights, and FDM. It says all other stages are identical to strategy nine.

## Chosen speeds and scalar estimates

The selected horizons double successively: 10, 20, 40, 80, 160, and 320 business days. The 10-day rule is the fastest traded (about two weeks). Doubling produced adjacent variants with similar correlations, a pattern intended to create consistently diversified rule variations.

| Variation | Horizon (business days) | Forecast scalar |
|---|---:|---:|
| Breakout10 | 10 | 0.60 |
| Breakout20 | 20 | 0.67 |
| Breakout40 | 40 | 0.70 |
| Breakout80 | 80 | 0.73 |
| Breakout160 | 160 | 0.74 |
| Breakout320 | 320 | 0.74 |

## Diversification among breakout speeds

**Table 92 — return correlations.** Adjacent horizons are more correlated than distant horizons; adjacent breakout correlations are approximately 0.83, versus about 0.87 for adjacent EWMAC trend variations in strategy nine.

|  | 10 | 20 | 40 | 80 | 160 | 320 | Average versus other horizons |
|---|---:|---:|---:|---:|---:|---:|---:|
| Breakout10 | 1.00 | 0.80 | 0.55 | 0.40 | 0.28 | 0.26 | 0.55 |
| Breakout20 |  | 1.00 | 0.83 | 0.62 | 0.42 | 0.33 | 0.67 |
| Breakout40 |  |  | 1.00 | 0.83 | 0.60 | 0.45 | 0.72 |
| Breakout80 |  |  |  | 1.00 | 0.84 | 0.64 | 0.72 |
| Breakout160 |  |  |  |  | 1.00 | 0.86 | 0.67 |
| Breakout320 |  |  |  |  |  | 1.00 | 0.59 |

## Performance by horizon

Tables 93–94 report **aggregated Jumbo portfolio** results with all instruments included regardless of cost. Accordingly, the chapter cautions that the costs of faster variants are exaggerated because the calculation includes instruments that are too costly to trade at their likely turnover.

| Metric | B10 | B20 | B40 | B80 | B160 | B320 |
|---|---:|---:|---:|---:|---:|---:|
| Mean annual return (gross) | 15.1% | 21.6% | 21.8% | 24.4% | 19.9% | 20.5% |
| Mean annual return (net) | 6.3% | 17.5% | 19.6% | 23.1% | 18.9% | 19.7% |
| Costs | −8.6% | −4.0% | −2.2% | −1.4% | −1.0% | −0.8% |
| Average drawdown | −120.0% | −14.1% | −11.6% | −10.0% | −13.3% | −14.3% |
| Standard deviation | 21.0% | 21.0% | 21.1% | 20.9% | 20.6% | 20.6% |
| Sharpe ratio | 0.30 | 0.83 | 0.93 | 1.10 | 0.92 | 0.96 |
| Turnover | 365.3 | 170.3 | 81.4 | 42.4 | 23.8 | 15.2 |
| Skew | 0.91 | 1.29 | 0.94 | 0.69 | 0.34 | 0.39 |
| Lower tail | 1.64 | 1.71 | 1.68 | 1.83 | 1.80 | 1.76 |
| Upper tail | 1.83 | 1.76 | 1.73 | 1.59 | 1.52 | 1.40 |
| Annualised alpha (gross) | 12.3% | 18.2% | 18.0% | 19.9% | 13.9% | 14.2% |
| Annualised alpha (net) | 3.7% | 14.2% | 15.8% | 18.6% | 12.9% | 13.4% |
| Beta | 0.17 | 0.23 | 0.27 | 0.31 | 0.40 | 0.43 |

The stated pattern: pre-cost performance is similar except for the fastest rule (Breakout10); costs and turnover fall as the rule slows. Monthly-return skew generally improves as horizons shorten, but this depends on the return frequency used for skew. Longer horizons have more long-only-benchmark exposure, so beta increases. If restricted to one variation, the author would choose Breakout80.

## Combined breakout strategy

### Instrument-specific eligibility (“speed limit”)

For an instrument, include a breakout variation only when its forecast turnover is less than the maximum turnover:

\[
\text{Maximum turnover}=\frac{0.15-(\text{cost per trade}\times\text{rolls per year})}{\text{cost per trade}}
\]

| Quantity | Meaning / condition |
|---|---|
| 0.15 | Fixed threshold in the displayed formula; the chapter does not restate its units or derivation here. |
| Cost per trade | Per-trade cost used in the eligibility calculation. |
| Rolls per year | Number of futures rolls per year. |
| Forecast turnover | Variation-specific annual turnover estimate, below. |

| Variation | Forecast turnover |
|---|---:|
| Breakout10 | 74.7 |
| Breakout20 | 35.1 |
| Breakout40 | 17.4 |
| Breakout80 | 8.7 |
| Breakout160 | 4.2 |
| Breakout320 | 2.0 |

### Averaging and FDM

For the eligible subset, give each included breakout variation equal forecast weight, multiply the resulting average by the stated FDM, and cap the final combined forecast at absolute 20.

| Eligible set | Weight for each variation | FDM |
|---|---:|---:|
| 10, 20, 40, 80, 160, 320 | 0.167 | 1.33 |
| 20, 40, 80, 160, 320 | 0.200 | 1.24 |
| 40, 80, 160, 320 | 0.250 | 1.17 |
| 80, 160, 320 | 0.333 | 1.10 |
| 160, 320 | 0.500 | 1.07 |
| 320 | 1.000 | 1.00 |

## Combined-breakout results

| Metric | Median average per instrument | Aggregate Jumbo portfolio |
|---|---:|---:|
| Mean annual return | 5.6% | 20.3% |
| Costs | −0.5% | −1.1% |
| Average drawdown | −22.9% | −8.6% |
| Standard deviation | 18.7% | 17.3% |
| Sharpe ratio | 0.30 | 1.17 |
| Turnover | 16.1 | 55.4 |
| Skew | 0.85 | 0.64 |
| Lower tail | 2.88 | 1.86 |
| Upper tail | 2.48 | 1.68 |

Compared with strategy nine’s multiple-trend rule, the median-instrument Sharpe ratio is 0.30 for breakout versus 0.23 for trend. Aggregate Jumbo Sharpe is only slightly higher: 1.17 versus 1.14. Breakout’s diversification bonus is more modest; aggregate skew is lower (0.64 versus 0.98). Equities are an outlier: their median instrument Sharpe is 0.10, although that exceeds the 0.03 cited for strategy nine.

## Combining breakout with trend and carry

### Required process

1. Start with six EWMAC variations (strategy nine), four carry variations (strategy ten), and six breakout variations.
2. For each instrument, use relevant turnover figures to retain only variations meeting the speed limit.
3. Allocate weights top-down: first across styles, then rules within a style, then variations within a rule.
4. Apply an FDM based on the selected count of rule variations.
5. Cap the combined forecast at absolute 20.

### Specific allocation used

- Treat carry as **convergent** and trend plus breakout as **divergent**.
- Allocate 40% to convergent/carry and 60% to divergent, consistent with strategy eleven.
- Within divergent, allocate 30% each to EWMAC and breakout.
- Within carry, equally divide its 40% over its available four variations.
- Within EWMAC, equally divide its 30% over its available six variations.
- Within breakout, equally divide its 30% over its available six variations.
- Use the generic FDM table 52 (page 234) for a selected set of well-diversified rules.

| Aggregate Jumbo metric | Multiple trend (S9) | Breakout (S21) | Carry + trend (S11) | Carry + breakout + trend |
|---|---:|---:|---:|---:|
| Mean annual return | 25.2% | 20.3% | 26.5% | 25.7% |
| Costs | −1.2% | −1.1% | −1.1% | −1.0% |
| Average drawdown | −11.2% | −8.6% | −8.9% | −8.4% |
| Standard deviation | 22.2% | 17.3% | 20.9% | 19.9% |
| Sharpe ratio | 1.14 | 1.17 | 1.27 | 1.29 |
| Turnover | 62.9 | 55.4 | 46.5 | 42.3 |
| Skew | 0.98 | 0.64 | 0.76 | 0.68 |
| Lower tail | 1.99 | 1.86 | 1.86 | 1.83 |
| Upper tail | 1.81 | 1.68 | 1.75 | 1.73 |
| Alpha | 18.8% | 16.1% | 22.3% | 22.1% |
| Beta | 0.43 | 0.29 | 0.30 | 0.26 |

Adding breakout to strategy eleven gives a modest, mixed improvement. The author attributes this to high similarity between breakout and trend (correlation 0.97). Breakout/carry correlation is 0.31, essentially identical to trend/carry. The stated recommendation is nevertheless to add an additional trading-rule type if it creates no extra workload, even if it is similar to an existing rule.

## Constraints, warnings, and edge cases

- Do not infer a scientific foundation for conventional resistance/range narratives from this chapter; the author explicitly has not performed serious scientific corroboration of breakout popularity or its intuitive story.
- Avoid non-scientific/discretionary range definitions such as Fibonacci levels; use rolling extrema.
- Do not run variants too fast when trading cost is prohibitive; enforce the eligibility formula per instrument.
- Do not assume range width always tracks standard deviation; persistent trends break that intuition.
- The raw formula requires a non-zero rolling range; no handling of equal rolling minimum and maximum is specified.
- An added midpoint threshold may make the rule more binary but raises transaction costs and overfitting risk.
- The performance tables by horizon include all instruments regardless of cost and therefore overstate fast-rule costs for an actually cost-filtered implementation.
- Performance conclusions are tied to the reported return frequency: skew conclusions can differ for daily, weekly, monthly, or annual returns.

## Connections to other chapters

- **Strategy one:** rejects Fibonacci “magic numbers.”
- **Strategy eight:** supports EWMA smoothing as a means to cut trading costs without penalising performance.
- **Strategy nine:** analogous EWMAC trend variations; its combination procedure and trading-plan stages are reused; correlation/performance comparisons appear throughout.
- **Strategy ten:** contributes four carry variations when carrying out the three-rule combination.
- **Strategy eleven:** supplies the top-down forecast-weight methodology and the earlier carry-plus-trend comparison.
- **Part Two:** establishes the general use of trading-rule forecasts, repeated combination procedures, and the generic FDM approach (table 52, p. 234).

## Glossary

- Back-adjusted price
- Breakout forecast / breakout variation
- Cost per trade
- Divergent trading style
- EWMA and EWMA span
- EWMAC
- Forecast scalar
- Forecast turnover
- Forecast diversification multiplier (FDM)
- Horizon / look-back
- Jumbo portfolio
- Rolling maximum / rolling minimum / range midpoint
- Speed limit
- Turnover

## Key takeaways

1. A rolling-range position formula converts breakout intuition into a bounded, continuous forecast from −20 to +20 before smoothing/scaling.
2. Use EWMA smoothing with span \(h/4\), then apply horizon scalars; omit volatility normalization by design.
3. Trade six doubled horizons where costs allow, equally weight the eligible set, apply its FDM, and cap the combined forecast at 20.
4. Breakout80 is the author’s single-variation preference; the combined breakout rule has reported aggregate Jumbo Sharpe 1.17.
5. Breakout is a divergent style closely related to trend (0.97 correlation), so adding it to carry+trend improves results only modestly and not uniformly, but the author still favors it if no additional workload is incurred.

