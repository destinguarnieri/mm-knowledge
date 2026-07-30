# Strategy 17 — Normalised trend

## Purpose and central argument

Normalised trend is an alternative implementation of the existing exponentially weighted moving-average crossover (EWMAC) trend rule. Rather than supplying the back-adjusted futures price directly to EWMAC, it first turns daily price changes into units of their recently estimated volatility and cumulatively sums them into a **normalised price**. The stated aim is to add a trend signal that should perform similarly to ordinary EWMAC but not be perfectly correlated with it; it also supplies the normalisation required by Strategies 18 and 19.

The book’s evidence finds that a standalone multiple-speed normalised-trend strategy is very close to Strategy 9 (ordinary trend): return correlations are 0.97. The author therefore regards the incremental diversification benefit as limited but positive, and personally prefers to trade ordinary trend, normalised trend, and carry together when automation makes the added operational effort manageable.

## Core concepts

### Volatility normalisation

Ordinary EWMAC normalises the *difference between moving averages* by volatility. This makes forecasts comparable across instruments and time periods, producing a forecast proportional to expected risk-adjusted return regardless of market environment.

This strategy instead normalises the **price itself** before applying the EWMAC calculations. Its normalised price broadly follows the back-adjusted price path but has a more consistent volatility. Expected volatility is identical each day; realised volatility is not exactly identical because future standard deviation cannot be forecast perfectly.

### Normalised price

Let:

| Symbol | Definition | Units / domain |
|---|---|---|
| \(p_t\) | Back-adjusted futures price at day \(t\) | Price units |
| \(p_{t-1}\) | Back-adjusted futures price on the prior day | Price units |
| \(\sigma_{p,t}\) | Recent estimate of daily standard deviation of price differences at \(t\) | Price units per day; must be available and non-zero for the computation |
| \(P^N_t\) | Recursively constructed normalised price | Arbitrary normalised-price units |
| \(P^N_{t-1}\) | Prior day’s normalised price | Arbitrary normalised-price units |

\[
P^N_t = \left(100 \times \frac{p_t-p_{t-1}}{\sigma_{p,t}}\right)+P^N_{t-1}
\]

The recursion begins at the first point for which a standard-deviation estimate can be made. The book sets \(P^N_0=0\). This starting value only shifts every value of \(P^N\) by a constant, so it does not affect the result. The multiplier 100 is likewise arbitrary: it merely makes values more familiar in magnitude.

**Figure 69 — Price and normalised price for S&P 500 micro futures.** The plotted normalised price (multiplied by 10 for display) tracks the familiar back-adjusted price path but makes early-period changes easier to see and later-period changes less dramatic. For this instrument, the display multiplier conveniently puts it on approximately the same scale as price.

## Trading-rule construction

All stages apart from the price transformation follow the prior EWMAC trend framework.

For instrument \(i\), the EWMAC calculation shown in the strategy trading plan is:

\[
\lambda=\frac{2}{N+1}
\]

\[
\operatorname{EWMA}_i(N)_t=\lambda P^N_{i,t}+\lambda(1-\lambda)P^N_{i,t-1}+\lambda(1-\lambda)^2P^N_{i,t-2}+\ldots
\]

\[
\operatorname{Raw\ forecast}_{N,i,t}=
\frac{\operatorname{EWMA}_i(N)_t-\operatorname{EWMA}_i(4N)_t}{\sigma_{N,t}}
\]

\[
\operatorname{Scaled\ forecast}_{N,i,t}=
\operatorname{Raw\ forecast}_{N,i,t}\times\operatorname{forecast\ scalar}_{N}
\]

\[
\operatorname{Capped\ forecast}_{N,i,t}=
\max\bigl(\min(\operatorname{Scaled\ forecast}_{N,i,t},+20),-20\bigr)
\]

| Symbol | Definition | Units / domain |
|---|---|---|
| \(i\) | Instrument index | Any eligible futures instrument |
| \(N\) | Fast EWMA span in business days | \(2,4,8,16,32,64\); slow span is \(4N\) |
| \(\lambda\) | Exponential-decay weight | Dimensionless; \(2/(N+1)\) |
| \(P^N_{i,t}\) | Normalised price of instrument \(i\) at \(t\) | Normalised-price units |
| \(\operatorname{EWMA}_i(N)_t\) | \(N\)-business-day-span exponentially weighted moving average of normalised price | Normalised-price units |
| \(\sigma_{N,t}\) | Daily standard deviation of normalised-price changes | Normalised-price units per day; must be non-zero |
| \(\operatorname{forecast\ scalar}_N\) | EWMAC rule scalar | Dimensionless; values in Table 29, p. 177 |
| \(\operatorname{Raw/Scaled/Capped\ forecast}_{N,i,t}\) | Successive forecast stages for EWMAC(\(N,4N\)) | Forecast units; cap applies at \(\pm20\) |

1. Construct \(P^N_t\) from back-adjusted prices and the daily price-difference volatility estimate using the equation above.
2. Create one or more EWMAC filters using \(P^N\) as the input, with pairs EWMAC(2, 8), EWMAC(4, 16), …, EWMAC(64, 256); equivalently, EWMAC(\(N,4N\)) for \(N\in\{2,4,8,16,32,64\}\).
3. Calculate the usual raw EWMAC difference. Divide it by an estimate of the daily standard deviation of **normalised-price** differences. Although less crucial after the price input is already normalised, the book says this step remains worthwhile.
4. Multiply by the same EWMAC forecast scalar used in Part One (Table 29, p. 177). Scalars are properties of the rule, not of the price series, so ordinary EWMAC scalars apply.
5. Cap each individual forecast to the interval \([-20,+20]\).
6. Select variations that meet the instrument’s cost/speed-limit test, assign their forecast weights, apply a forecast diversification multiplier (FDM), and cap the combined forecast at an absolute value of 20.

### Cost-based eligibility and forecast combination

For each instrument, retain only variations cheap enough given its cost per trade, rule turnover, and the **speed limit** (the cap on trading costs). The chapter repeats the maximum-turnover condition:

\[
\text{Maximum turnover}=\frac{0.15-(\text{Cost per trade}\times\text{Rolls per year})}{\text{Cost per trade}}
\]

The quantities “Cost per trade” and “Rolls per year” are referenced without further definition in this chapter; their units/precise construction are supplied by the earlier strategy. If a rule’s turnover is not within this maximum, exclude it. If no variation qualifies, do not trade that instrument; this occurs for four instruments in the author’s dataset. Equally weight the remaining selected variations.

Apply the FDM to the combined forecast because combining forecasts diversifies them. Because the normalised-trend rules are highly similar, use the same FDM values as Strategy 9 (Table 36, p. 193) for standalone normalised trend. Cap the resulting combined forecast at \(\pm20\).

### Table 73 — Average annual turnover by normalised-trend filter

| Filter | Turnover per year |
|---|---:|
| EWMAC2 | 109.9 |
| EWMAC4 | 56.2 |
| EWMAC8 | 28.7 |
| EWMAC16 | 15.2 |
| EWMAC32 | 9.0 |
| EWMAC64 | 6.5 |

## Individual-filter performance

These results are gross/no-cost *Jumbo portfolio* results across all instruments for consistency with Part One. They are not individual-instrument results. An individual instrument’s performance will be substantially lower, and some instruments cannot trade a given speed because it is too expensive. The author deliberately includes instruments too expensive for faster filters to obtain more evidence on potential pre-cost returns.

### Table 71 — Faster normalised EWMAC filters, aggregated Jumbo portfolio

| Metric | EWMAC2 | EWMAC4 | EWMAC8 |
|---|---:|---:|---:|
| Mean annual return (gross) | 18.9% | 24.6% | 26.3% |
| Mean annual return (net) | 8.5% | 19.1% | 23.4% |
| Costs | −10.2% | −5.4% | −2.9% |
| Sharpe ratio | 0.33 | 0.75 | 0.93 |
| Turnover | 435 | 230 | 119 |
| Skew | 1.25 | 1.58 | 1.31 |
| Lower tail | 1.77 | 1.81 | 1.79 |
| Upper tail | 2.09 | 2.03 | 1.99 |
| Annualised alpha (gross) | 15.7% | 20.4% | 21.0% |
| Annualised alpha (net) | 5.5% | 15.0% | 18.1% |
| Beta | 0.20 | 0.29 | 0.36 |

### Table 72 — Slower normalised EWMAC filters, aggregated Jumbo portfolio

| Metric | EWMAC16 | EWMAC32 | EWMAC64 |
|---|---:|---:|---:|
| Mean annual return (gross) | 27.4% | 27.1% | 25.2% |
| Mean annual return (net) | 25.5% | 25.7% | 23.9% |
| Costs | −1.9% | −1.4% | −1.2% |
| Sharpe ratio | 1.03 | 1.04 | 0.95 |
| Turnover | 65.3 | 42.1 | 34.2 |
| Skew | 0.98 | 0.88 | 0.60 |
| Lower tail | 1.96 | 1.87 | 1.77 |
| Upper tail | 1.86 | 1.68 | 1.59 |
| Annualised alpha (gross) | 20.4% | 18.7% | 15.0% |
| Annualised alpha (net) | 18.6% | 17.4% | 13.7% |
| Beta | 0.47 | 0.56 | 0.68 |

The broad pattern resembles ordinary EWMAC: profitability before costs is similar for most rules except the fastest; costs and turnover decline while beta rises as filters slow; and monthly skew declines as filters slow. Against Tables 30–31 (ordinary trend), the author notes: normalisation is a little better for the two fastest speeds; costs and turnover are roughly 25% higher throughout; skew and lower-tail measures are slightly better; and both beta and alpha are a little higher.

## Standalone multiple-trend comparison

### Table 74 — Jumbo portfolio: ordinary versus normalised multiple trend

| Metric | Strategy 9: multiple trend (adjusted prices) | Strategy 17: multiple trend (normalised prices) |
|---|---:|---:|
| Mean annual return | 25.2% | 28.2% |
| Costs | −1.2% | −1.4% |
| Average drawdown | −11.2% | −12.9% |
| Standard deviation | 22.2% | 24.4% |
| Sharpe ratio | 1.14 | 1.15 |
| Turnover | 62.9 | 72.1 |
| Skew | 0.98 | 0.93 |
| Lower tail | 1.99 | 1.87 |
| Upper tail | 1.81 | 1.80 |
| Alpha | 18.8% | 20.1% |
| Beta | 0.43 | 0.55 |

Normalisation has somewhat higher turnover, beta, standard deviation, and costs; its Sharpe ratio is fractionally higher, alpha somewhat higher, skew slightly worse, and lower tail somewhat more amiable. The author’s practical conclusion is that there is little to choose between the two standalone strategies because the return correlation is 0.97.

## Combining normalised trend, ordinary trend, and carry

Replacing Strategy 11’s ordinary trend with normalised trend may use exactly the same forecast weights and FDM as Strategy 11 (Table 51, p. 233), because the trend types are very similar.

To trade both trend types with carry, use the stated top-down allocation principles:

1. Split rules by **style** and allocate among styles according to preference.
2. Within each style, allocate equally across **trading rules**.
3. Within a rule, allocate equally across the available **variations**.

With a 60% allocation to divergent trend and 40% to convergent carry:

- Give 60% to trend and 40% to carry.
- Split trend equally: 30% ordinary trend and 30% normalised trend.
- Give the single carry rule 40%.
- Split each rule’s allocation equally among the variations actually selected for the instrument.

**Worked allocation — WTI Crude Oil.** The chapter says it can trade all four carry rules and the four slowest variations of each trend flavour.

| Component | Allocation |
|---|---:|
| Ordinary EWMAC8, 16, 32, 64 | 7.5% each (= 30% ÷ 4) |
| Normalised EWMAC8, 16, 32, 64 | 7.5% each (= 30% ÷ 4) |
| Carry5, Carry20, Carry60, Carry120 | 10% each (= 40% ÷ 4) |

Use FDMs from Table 52 (p. 234) for the appropriate number of rule variations when normalised trend is combined with carry, or with carry plus standard trend.

### Table 75 — Jumbo portfolio: carry with alternative trend constructions

| Metric | Strategy 11: carry + adjusted-price trend | Strategy 17: carry + normalised-price trend | Strategy 17: carry + normalised and adjusted-price trend |
|---|---:|---:|---:|
| Mean annual return | 26.5% | 28.8% | 27.5% |
| Costs | −1.1% | −1.1% | −1.1% |
| Average drawdown | −8.9% | −8.6% | −8.7% |
| Standard deviation | 20.9% | 21.0% | 20.9% |
| Sharpe ratio | 1.27 | 1.32 | 1.32 |
| Turnover | 46.5 | 48.3 | 47.6 |
| Skew | 0.76 | 0.76 | 0.75 |
| Lower tail | 1.86 | 1.90 | 1.85 |
| Upper tail | 1.75 | 1.79 | 1.70 |
| Alpha | 22.3% | 22.8% | 22.9% |
| Beta | 0.30 | 0.34 | 0.32 |

There is no “slam dunk” winner; results are described as virtually identical and choice depends on preference. Reasons to remain with Strategy 11 include the intuitive difficulty of normalisation and added process work. For automated trading, the author considers those costs manageable, and argues that diversification gains could exceed the 0.97 linear-correlation estimate because correlation is only a linear measure.

## Interactions with Strategies 12–16

| Earlier modification | Finding for normalised trend | Policy / caveat |
|---|---|---|
| Strategy 12: non-linear forecast-strength mapping | No significant improvement | Not recommended |
| Strategy 13: reduce forecast when volatility is particularly high | Modest but significant Sharpe-ratio improvement using normalised synthetic spot price | Same result direction as basic trend |
| Strategy 14: synthetic spot rather than back-adjusted price for trend | Not applicable | — |
| Strategy 15: accurate carry | Not applicable | — |
| Strategy 16: alter trend/carry allocation from historic performance | Small Sharpe-ratio improvement using normalised synthetic spot price | Same result direction as basic trend |
| Strategy 16: reduce trend allocation only for equities | Stronger result than basic trend: equities with normalised trend have slightly negative Sharpe ratio, unlike all other asset classes | Would improve performance, but may be overfit |

The author advises applying the same policies to normalised trend as to basic EWMAC. The similarity of results across a changed trend rule is presented as evidence that Strategies 12–16 may be robust rather than merely statistical/data-mined. These observations also apply to the other Part Two trend strategies (Strategies 18 and 19) unless otherwise noted.

## Practical warnings and boundary conditions

- This is not a replacement mandated by clearly superior evidence: the two trend implementations are extremely correlated, and the performance differences are small.
- Fast filters carry substantially more turnover and cost. Eligibility must be assessed per instrument using costs, annual rolls, and the speed limit.
- Some instruments have no eligible normalised-trend filters and should not be traded under this rule.
- Values shown for individual speeds are aggregated Jumbo portfolio findings, including uneconomic instruments for faster filters to expose pre-cost evidence; do not treat them as achievable individual-instrument net results.
- Normalisation requires an available daily standard-deviation estimate and is operationally more involved; the formula’s initial level and ×100 scale are arbitrary but must be used consistently.
- The book calls the normalisation unintuitive for manual diagnosis; the author’s proposed mitigation for an automated trader is better diagnostic reporting.
- The chapter supplies the EWMAC equations but refers out for the numeric forecast scalar values (Table 29), FDM values, the construction of the normalised-price standard-deviation estimate, and the definitions of the reported performance statistics. They should be sourced from the cited material; this file does not infer missing definitions.

## Trading plan

Go long or short one or more instruments with variable risk estimates and a combined forecast from multiple trend filters, modified to accept the normalised price. Eligible instruments are those meeting minimum capital, liquidity, and cost thresholds. Choose rules using the Table 73 turnover figures and cost test; construct EWMAC(\(N,4N\)) variations for \(N=2,4,8,16,32,64\); calculate and cap their forecasts; combine with appropriate weights and FDM; and use the normalised price in place of the conventional price input. All other stages are identical to Strategy 9 for standalone trend or Strategy 11 when combined with carry.

## Key takeaways

- Normalised trend is EWMAC applied to the cumulative, volatility-standardised price-change series \(P^N\).
- The method creates a more consistently volatile input while retaining a price-like path; the starting level and scale factor are arbitrary.
- It has performance similar to ordinary multiple EWMAC trend, but with modestly higher turnover/costs and a 0.97 return correlation.
- Both ordinary and normalised trend can be combined with carry through transparent top-down style/rule/variation weighting.
- The author sees no decisive winner; the main rationale for adding normalised trend is a potentially positive, nonlinear diversification benefit and its necessity for subsequent strategies.

## Glossary

- **Back-adjusted price** — Futures price series \(p_t\) used as the source for the normalised-price recursion.
- **Normalised price (\(P^N\))** — Recursive cumulative sum of daily price changes divided by their estimated volatility, scaled by 100.
- **EWMAC** — Exponentially weighted moving-average crossover; here constructed as EWMAC(\(N,4N\)).
- **Forecast scalar** — Rule-specific multiplier applied after raw-forecast normalisation; referenced in Table 29.
- **Forecast weight** — Weight of a selected trading-rule variation in the combined forecast.
- **Forecast diversification multiplier (FDM)** — Multiplier applied to a combined forecast to account for diversification among forecasts.
- **Speed limit** — Cap on trading costs used to screen rule variations.
- **Turnover** — Annual trading turnover used in cost eligibility and reported performance statistics.
- **Divergent trend / convergent carry** — The styles used for top-down allocation in the combined strategy.
- **Jumbo portfolio** — The broad multi-instrument portfolio used for the chapter’s aggregate performance analysis.

## Explicit chapter connections

- **Strategy 9:** provides the ordinary multiple-EWMAC trend template, cost-selection method, FDM (Table 36), and baseline comparison.
- **Strategy 11:** provides trend-plus-carry weights/FDM (Table 51) and the benchmark combined strategy.
- **Strategies 12–16:** their modifications are evaluated for normalised trend in the chapter’s “What about…” summary.
- **Strategies 18–19:** will build on the normalisation methodology; prior-modification findings apply unless stated otherwise.
- **Part One / Table 29:** source of EWMAC forecast scalars.
