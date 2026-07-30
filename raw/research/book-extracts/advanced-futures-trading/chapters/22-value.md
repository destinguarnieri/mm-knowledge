# Strategy Twenty-Two: Value

## Chapter purpose and central argument

This chapter adapts **value**—normally an equity strategy based on inexpensive versus expensive accounting ratios—to futures and other arbitrary assets. The proposed proxy is **very slow mean reversion in relative performance within an asset class**: go long instruments that have underperformed over the previous five years and short those that have outperformed. 

The chapter's central conclusion is deliberately modest. Value is weak as a standalone futures strategy, but its low correlation with trend and carry can modestly improve a combined portfolio when value receives a small allocation.

## Strategy definition

> **Strategy twenty-two:** Go long instruments that have underperformed in the last five years, and short instruments that have outperformed.

The strategy's stated objective is to go long or short one or more instruments using a variable risk estimate and a forecast based on mean reversion in outperformance over the last five years.

## Background and rationale

### Equity value versus the futures proxy

In equities, value identifies cheap stocks using accounting ratios such as low price-to-earnings (P/E) or high dividend yield, buys those stocks, and may short expensive stocks with high P/E or low yields. The direct approach is difficult to generalize: even an aggregated S&P 500 P/E takes considerable work, and analogous ratios for Corn or Bitcoin are not obvious.

The simplifying premise is that equity earnings are relatively stable, so changes in P/E are mostly driven by price. On that premise, a simplified value strategy buys assets whose prices have fallen and sells those whose prices have risen. For an arbitrary asset, value is therefore treated as very slow mean reversion: recent multi-year outperformance is expected to be followed by underperformance, and vice versa.

### Time horizon and persistence

Value requires patience: whereas trend tends to play out over weeks or months, stocks may remain cheap or expensive for years. The chapter cites a period of equity-value underperformance from January 2017 through October 2020; its footnote reports cumulative US value-factor underperformance of -54.7%, followed by +52.5% from November 2020 to April 2022, effectively reversing almost all of it.

The chosen horizon is **five years**. One year is considered too short because trend remains effective at that frequency (connection to Strategy Nine). Horizons of two to four years yielded fairly similar results, while a 10- or 20-year horizon is impractical to evaluate. The author found no benefit from combining multiple horizons.

## Forecast construction

This calculation reuses the relative-outperformance construction introduced in Strategy Nineteen, with inputs derived in Strategies Seventeen and Eighteen.

### Inputs and notation

| Symbol | Meaning | Source / conditions |
|---|---|---|
| `i` | Instrument identifier. | Any instrument being evaluated. |
| `t` | Trading day. | Daily calculation. |
| `P^N_{i,t}` | Volatility-normalised price for instrument `i` at day `t`. | Derived in Strategy Seventeen. A pure spot price from Strategy Fourteen may instead be used; the chapter says this has little effect, though some traders may prefer it. |
| `A_{i,t}` | Normalised price of the relevant asset class for instrument `i` at day `t`. | Derived in Strategy Eighteen. |
| `R_{i,t}` | Instrument `i`'s relative price versus its asset class at day `t`. | Difference between the two normalised prices. |
| `H` | Lookback horizon, measured in years. | Use `H = 5` for the specified rule. |
| `Outperformance_H` | Average daily outperformance over the `H`-year horizon. | Assumes approximately 256 business days per year. |
| `EWMA_span=30(·)` | Exponentially weighted moving average with a 30-day span. | Smoothing step. |

### Equations

1. **Relative price**

   \[
   R_{i,t} = P^N_{i,t} - A_{i,t}
   \]

2. **Average daily outperformance over `H` years**

   \[
   Outperformance_H = \frac{R_{i,t} - R_{i,t-(256\times H)}}{256\times H}
   \]

   The numerator is the change in relative price from roughly `256 × H` business days earlier; dividing by that count expresses it as average daily outperformance.

3. **Raw value forecast**

   \[
   Forecast = EWMA_{span=30}(-Outperformance_H)
   \]

   The negative sign implements expected mean reversion: past relative outperformance produces a negative forecast, while past relative underperformance produces a positive forecast. A 30-day smoothing span is presented as sufficient to reduce costs without penalising performance because the signal itself is measured over multiple years.

### Scaling, cap, and implementation filter

- Multiply the raw forecast by a **forecast scalar of 7.27** for the five-year rule.
- Cap the absolute scaled forecast at **20**.
- The rule's forecast turnover for `H = 5` is **8.7**.
- Trade a variation only when it passes the chapter's cost rule:

  \[
  Turnover < \frac{0.15 - (Cost\ per\ trade\times Rolls\ per\ year)}{Cost\ per\ trade}
  \]

  The trading-plan graphic supplies this inequality but does not define its units or precise cost convention. Preserve the conventions used elsewhere in the book rather than inferring them here.

## Trading plan

| Stage | Instruction |
|---|---|
| Instruments | Any instruments meeting minimum capital, liquidity, and cost thresholds. |
| Rule selection | Select only rule variations satisfying the turnover/cost inequality above. |
| Outperformance | Compute `R`, then `Outperformance_H`, using `H = 5` years and approximately 256 business days per year. |
| Raw forecast | Apply a 30-day-span EWMA to negative outperformance. |
| Forecast scalar | Use 7.27 for `H = 5` years, then cap the absolute scaled forecast at 20. |
| Other stages | Identical to Strategy Nine. |

## Portfolio classification and allocations

Value is classified as a **convergent** strategy, alongside carry: convergent strategies make money when markets move toward equilibrium. Trend following and the preceding breakout strategy are described as **divergent**.

To add value to Strategy Eleven (which currently combines trend and carry), the chapter uses these forecast weights:

| Level | Allocation |
|---|---:|
| Convergent style | 40% |
| Divergent style | 60% |
| Carry within the combined strategy | 35% |
| Value within the combined strategy | 5% |
| Trend / EWMAC within the combined strategy | 60% |
| Each of up to four carry variations | Equal share of the 35% carry allocation |
| Single value variation | 5% |
| Each of up to six EWMAC variations | Equal share of the 60% allocation |

This intentionally departs from splitting the 40% convergent allocation evenly between carry and value. An equal split would give value 20%; the author uses 5% because standalone value is not very profitable and 20% would worsen performance. The author explicitly acknowledges that fitting these weights is in-sample fitting and says results should be treated as an indication of possible future performance, not a realistic record of what could have been achieved in the past. Forecast diversification multipliers should be taken from Table 52 (page 234).

## Evidence and performance assessment

### Correlations

- Value with trend: **-0.03**.
- Value with carry: **0.16**.
- Trend with carry: **0.31**.

The chapter notes that financial theory permits a money-losing strategy to improve a portfolio Sharpe ratio when it is negatively correlated with existing assets.

### Table 99: performance for value, trend, and carry

| Metric | Strategy 22: Value | Strategy 11: Trend 60% / Carry 40% | Strategy 22 combined: Trend 60% / Carry 35% / Value 5% |
|---|---:|---:|---:|
| Mean annual return (net) | -1.0% | 26.5% | 27.0% |
| Costs | -0.8% | -1.1% | -1.1% |
| Average drawdown | -66.7% | -8.9% | -9.1% |
| Standard deviation | 16.8% | 20.9% | 21.0% |
| Sharpe ratio | -0.06 | 1.27 | 1.29 |
| Turnover | 11.7 | 46.5 | 48.5 |
| Skew | 0.21 | 0.76 | 0.82 |
| Lower tail | 1.32 | 1.86 | 1.89 |
| Upper tail | 1.49 | 1.75 | 1.74 |
| Annualised alpha (net) | 2.9% | 22.3% | 22.6% |
| Beta | -0.25 | 0.30 | 0.31 |

The standalone aggregate Jumbo value portfolio is described as mediocre, with a modest positive alpha attributable to negative beta. Adding 5% value raises the reported mean net annual return from 26.5% to 27.0% and the Sharpe ratio from 1.27 to 1.29, while increasing average drawdown slightly in magnitude and turnover from 46.5 to 48.5. The chapter attributes the improvement entirely to correlations and considers those relatively predictable, hence expresses some confidence that the additional returns can be earned in the future.

## Constraints, warnings, and edge cases

- A five-year lookback leaves almost no statistically significant empirical evidence; the author cautions against putting too much weight on the findings and characterises value as something one must believe in rather than strongly test empirically.
- Value in futures is unlikely to be as effective as value in equities and is not good enough to trade standalone.
- Long stretches of poor performance are possible; the cited equity-value episode is a reminder of the patience required.
- Do not use a one-year value horizon if the objective is to isolate slow mean reversion: the chapter says trend is still effective at that frequency.
- The 5% portfolio weight is an illustrative, in-sample-fitted choice. It is not presented as a universally validated optimum.
- An alternative construction removes the final year, producing four-year mean reversion with a one-year lag. It removes the strong momentum effect up to a one-year holding period, but the author considers it unnecessary when a trend strategy is also traded.
- The displayed eligibility formula is not fully specified in this chapter; its cost units and conventions should not be guessed.

## Practical implications

Use value as a small diversifier alongside trend and carry, not as an isolated futures allocation. The method requires daily volatility-normalised and asset-class-normalised prices, a long-history buffer of roughly five years, cost-aware selection of eligible rule variations, and the existing Strategy Nine implementation stages.

## Connections to other chapters

| Referenced chapter / item | Connection stated in this chapter |
|---|---|
| Strategy Nine | One-year horizon is rejected because trend works at that frequency; all non-specific trading-plan stages are identical to Strategy Nine. |
| Strategy Eleven | Base trend/carry portfolio to which 5% value is added. |
| Strategy Fourteen | Pure spot price is an alternative input; results are said not to change much. |
| Strategy Seventeen | Supplies the volatility-normalised instrument price `P^N_{i,t}`. |
| Strategy Eighteen | Supplies relevant-asset-class normalised price `A_{i,t}`. |
| Strategy Nineteen | Origin of the relative-outperformance measure reused here. |
| Preceding breakout strategy | Example of a divergent strategy. |
| Table 52, p. 234 | Source for forecast diversification multipliers. |

## Glossary

- **Value:** A strategy that buys relatively cheap/underperforming instruments and sells relatively expensive/outperforming ones; here, a very slow relative-performance mean-reversion signal.
- **Convergent strategy:** A strategy expected to profit as markets move toward equilibrium; value and carry are classified this way.
- **Divergent strategy:** A strategy expected to profit from movement away from equilibrium; trend following and breakout are examples in the chapter.
- **Relative price (`R`):** Volatility-normalised instrument price minus relevant asset-class normalised price.
- **Outperformance:** The average daily change in relative price over the selected multi-year horizon.
- **Forecast scalar:** Multiplier used to scale the raw forecast; 7.27 for five-year value.
- **Forecast turnover:** Turnover associated with the forecast rule; 8.7 for five-year value in the trading-plan figure.
- **EWMAC:** The trend rule family mentioned in the allocation scheme; the chapter does not expand the acronym here.
- **Forecast diversification multiplier:** Multiplier used when combining forecasts; consult Table 52, page 234.

## Key takeaways

1. Build futures value from five-year mean reversion in relative, volatility-normalised performance—not from accounting ratios.
2. Use `R = P^N - A`, convert its five-year change to average daily outperformance, negate it, and smooth it with a 30-day EWMA.
3. Scale by 7.27, cap absolute forecast at 20, and apply the cost/turnover filter before selecting a rule variation.
4. Treat it as a small, diversifying component: it is weak standalone but can marginally improve a trend-and-carry portfolio because of low correlations.
5. Evidence is weak statistically because the signal acts over long horizons; avoid overconfidence and avoid treating the 5% allocation as a robust optimum.

## Source notes retained from chapter

- The FX fair-value example is BEER (Behavioural Equilibrium Exchange Rate); the author also mentions informal internal names WINE and CIDER.
- The cited academic source for a five-year horizon is Clifford Asness, Lasse Pedersen, and Tobias Moskowitz, “Value and Momentum Everywhere,” *The Journal of Finance* 68, no. 3 (2013). The chapter notes that this work uses a ratio of log prices, so its results will not be identical to this strategy.
