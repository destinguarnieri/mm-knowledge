# Strategy Eleven — Combined Carry and Trend

## Purpose and central argument

Strategy eleven completes Part One by combining two forecast-based styles—trend and carry—into one risk-scaled futures portfolio. Its premise is that individual trend and carry forecasts have already been calibrated to a common scale, so they can be weighted together. The author’s recommended illustration is **60% trend / 40% carry**, chosen because it maximises the reported Jumbo-portfolio Sharpe ratio, minimises its average drawdown, and retains good alpha; the appropriate mix remains preference-dependent.

> **Strategy definition:** Trade one or more instruments with positions scaled to a variable risk estimate. Scale positions by the strength of a combined forecast: a weighted average of carry and trend forecasts.

## Building blocks and terms

- **Trend / divergent style:** the EWMAC rule from strategy nine. Candidate variations: EWMAC2, EWMAC4, EWMAC8, EWMAC16, EWMAC32, EWMAC64. (The worked example identifies the two slowest as EWMAC(32,128) and EWMAC(64,256).)
- **Carry / convergent style:** the smoothed carry rule from strategy ten, with an `N`-day EWMA smoothing window: Carry5, Carry20, Carry60, Carry120. Carry is called convergent because it assumes spot prices remain stable.
- **Forecast:** a risk-adjusted measure of expected future returns. Every raw forecast is scaled to an absolute average of **10**, then capped so its absolute value does not exceed **20**.
- **FDM (forecast diversification multiplier):** adjustment applied after initial forecast weighting to account for diversification among trading rules.
- **Jumbo portfolio:** the author’s aggregate portfolio of more than 100 instruments.
- **SR / Sharpe ratio:** reported in the source as a performance and cost unit. The chapter does not give its mathematical definition.
- **SRR (Sharpe ratio ratio):** aggregate Jumbo-portfolio SR divided by the median instrument SR; interpreted as realised cross-instrument diversification benefit in risk-adjusted returns.

The chapter gives no explicit algebraic formula for the combined forecast or the FDM application. In words: form a weighted average of the eligible, scaled-and-capped carry and trend forecasts, apply the FDM, then use the usual capping, position-sizing, and buffering procedure from earlier strategies. No new variables, units, or derivation are specified here beyond the forecast scale, cap, weights, FDM table, and cost threshold below.

## Eligibility and allocation procedure

1. For each instrument, use the turnover figures from tables 35 (trend) and 40 (carry) and the instrument’s risk-adjusted cost per trade.
2. Keep only rule variations whose costs do not exceed the author’s **speed limit of 0.15 SR units**.
3. Split the eligible rules by style: divergent (trend) and convergent (carry).
4. Allocate weight between styles according to preference.
5. Within each style, allocate equally across trading rules; here there is one rule per style (EWMAC and carry).
6. Allocate a rule’s weight equally across its eligible variations.
7. Apply the FDM corresponding to the number of trading rules; interpolate table values if required.
8. Apply the standard capping, position sizing, and buffering procedure. The chapter directs readers to strategies nine and ten for the other elements.

### Worked allocation: Eurodollar futures

The stated risk-adjusted cost per trade is **0.0088 SR units**. Strategy nine used this to derive maximum annual turnover of **13 trades**. Using tables 35 and 40, the eligible set is the two slowest EWMAC variants and all four carry variants.

- Trend/divergent style: 60%; two EWMAC variants, so 30% each: EWMAC(32,128) 30%, EWMAC(64,256) 30%.
- Carry/convergent style: 40%; four carry variants, so 10% each: Carry5, Carry20, Carry60, Carry120.

## Rule-weight lookup (Table 51)

Each row describes the eligible rule set; values are the weight assigned to **each** listed EWMAC or carry variation.

| Eligible variations | Each EWMAC | Each carry |
|---|---:|---:|
| EWMAC2, 4, 8, 16, 32, 64; Carry5, 20, 60, 120 | 0.10 | 0.10 |
| EWMAC4, 8, 16, 32, 64; Carry5, 20, 60, 120 | 0.12 | 0.10 |
| EWMAC8, 16, 32, 64; Carry5, 20, 60, 120 | 0.15 | 0.10 |
| EWMAC16, 32, 64; Carry5, 20, 60, 120 | 0.20 | 0.10 |
| EWMAC32, 64; Carry5, 20, 60, 120 | 0.30 | 0.10 |
| EWMAC32, 64; Carry20, 60, 120 | 0.30 | 0.13333 |
| EWMA64 [sic in source]; Carry20, 60, 120 | 0.60 | 0.13333 |
| Carry20, 60, 120 | 0 | 0.3333 |
| Carry60, 120 | 0 | 0.5 |
| Carry120 | 0 | 1.0 |

**Source ambiguity:** Table 51 says `EWMA64`, whereas surrounding text calls the trend rule EWMAC and uses `EWMAC64`; it is retained exactly as printed.

## FDM lookup (Table 52)

| Rules | FDM | Rules | FDM |
|---:|---:|---:|---:|
| 1 | 1.00 | 14 | 1.41 |
| 2 | 1.02 | 15 | 1.42 |
| 3 | 1.03 | 16 | 1.44 |
| 4 | 1.23 | 17 | 1.46 |
| 5 | 1.25 | 18 | 1.48 |
| 6 | 1.27 | 19 | 1.50 |
| 7 | 1.29 | 20 | 1.53 |
| 8 | 1.32 | 21 | 1.54 |
| 9 | 1.34 | 22 | 1.55 |
| 10 | 1.35 | 25 | 1.69 |
| 11 | 1.36 | 30 | 1.81 |
| 12 | 1.38 | 35 | 1.93 |
| 13 | 1.39 | 40 or more | 2.00 |

## Choosing the carry–trend mixture (Tables 49–50)

Percentages are the proportion allocated to **trend**; carry receives the remainder. Results are for Jumbo portfolios.

| Trend weight | SR | Avg. drawdown | Weekly skew | Monthly skew | Annual skew | Lower tail | Upper tail | Alpha | Beta |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100% | 1.14 | −11.2% | 0.05 | 0.98 | 1.28 | 1.99 | 1.81 | 18.8% | 0.43 |
| 90% | 1.19 | −10.1% | 0.08 | 0.94 | 1.27 | 1.95 | 1.79 | 19.1% | 0.40 |
| 80% | 1.24 | −9.6% | 0.12 | 0.88 | 1.26 | 1.91 | 1.76 | 20.4% | 0.39 |
| 70% | 1.26 | −9.2% | 0.16 | 0.83 | 1.25 | 1.88 | 1.76 | 21.5% | 0.37 |
| 60% | 1.27 | −8.9% | 0.18 | 0.76 | 1.22 | 1.86 | 1.75 | 22.3% | 0.30 |
| 50% | 1.27 | −9.3% | 0.20 | 0.72 | 1.16 | 1.78 | 1.76 | 22.9% | 0.30 |
| 40% | 1.25 | −9.8% | 0.19 | 0.68 | 1.04 | 1.74 | 1.67 | 22.87% | 0.25 |
| 30% | 1.20 | −11.1% | 0.16 | 0.63 | 0.85 | 1.67 | 1.59 | 22.4% | 0.20 |
| 20% | 1.12 | −13.2% | 0.12 | 0.57 | 0.62 | 1.62 | 1.55 | 21.6% | 0.15 |
| 10% | 1.03 | −16.0% | 0.08 | 0.50 | 0.38 | 1.60 | 1.54 | 20.5% | 0.10 |
| 0% | 0.94 | −18.6% | −0.01 | 0.41 | 0.16 | 1.57 | 1.49 | 19.1% | 0.06 |

**Trade-off:** More trend improves skew and right tails; adding carry produces a better left tail. The author uses 60/40 in their own system; the footnote notes that it echoes the classic 60/40 long-only equity/bond cash-weight split.

## Evaluation by asset class

### Financial assets (Table 53)

| Metric | Equity | Vol | FX | Bond |
|---|---:|---:|---:|---:|
| Mean annual return | 2.4% | 18.5% | 6.8% | 13.3% |
| Costs | −0.3% | −1.3% | −0.4% | −0.4% |
| Average drawdown | −21.9% | −30.7% | −40.2% | −20.2% |
| Standard deviation | 18.6% | 32.2% | 21.6% | 23.3% |
| Sharpe ratio | 0.13 | 0.58 | 0.30 | 0.54 |
| Turnover | 12.1 | 11.4 | 11.8 | 11.5 |
| Skew | 0.51 | −0.50 | 0.53 | 0.64 |
| Left tail | 3.56 | 2.98 | 3.42 | 2.52 |
| Right tail | 2.46 | 1.79 | 2.96 | 2.52 |

### Commodities (Table 54)

| Metric | Metals | Energy | Ags | Median |
|---|---:|---:|---:|---:|
| Mean annual return | 6.8% | 10.2% | 5.4% | 5.7% |
| Costs | −0.3% | −0.5% | −0.4% | −0.4% |
| Average drawdown | −29.7% | −34.8% | −40.0% | −24.9% |
| Standard deviation | 19.6% | 25.6% | 23.8% | 21.7% |
| Sharpe ratio | 0.36 | 0.41 | 0.23 | 0.27 |
| Turnover | 13.4 | 12.4 | 11.4 | 11.8 |
| Skew | 2.20 | 0.66 | 0.70 | 0.63 |
| Left tail | 3.27 | 2.85 | 2.74 | 3.11 |
| Right tail | 4.07 | 2.44 | 2.56 | 2.67 |

Most classes perform similarly across carry and trend. The stated exception is equities: carry does better and trend is especially weak, yet the combined result improves less than expected because equity carry’s annualised standard deviation is only half target (per table 46), so carry contributes about 20%, rather than 40%, of equity return risk.

## Aggregate Jumbo-portfolio comparison (Table 55)

| Metric | Long-only (S4) | Multiple trend (S9) | Carry (S10) | Carry + trend (S11) |
|---|---:|---:|---:|---:|
| Mean annual return | 15.4% | 25.2% | 19.7% | 26.5% |
| Costs | −0.8% | −1.2% | −0.8% | −1.1% |
| Average drawdown | −24.7% | −11.2% | −18.6% | −8.9% |
| Standard deviation | 18.2% | 22.2% | 20.8% | 20.9% |
| Sharpe ratio | 0.85 | 1.14 | 0.94 | 1.27 |
| Turnover | 20.7 | 62.9 | 19.2 | 46.5 |
| Skew | −0.04 | 0.98 | 0.41 | 0.76 |
| Lower tail | 1.44 | 1.99 | 1.57 | 1.86 |
| Upper tail | 1.24 | 1.81 | 1.49 | 1.75 |
| Alpha | 0 | 18.8% | 19.1% | 22.3% |
| Beta | 1.00 | 0.43 | 0.06 | 0.30 |

The author calls 60/40 a good compromise: it improves every reported statistic versus pure trend except skew.

### Figure 45 — cumulative account curves

The chart covers roughly the late 1970s through early 2020s. The combined strategy (black) rises most consistently and finishes highest (about 1,400 index units), slightly above multiple trend (about 1,330). Carry ends around 1,050 and long-only about 810. The source’s stated interpretation is that carry plus trend performed consistently well over time.

## Diversification diagnostics (Table 56)

| Measure | Long-only | Multiple trend | Carry | Carry + trend |
|---|---:|---:|---:|---:|
| A: Median SR across instruments | 0.32 | 0.23 | 0.28 | 0.27 |
| B: Aggregate Jumbo SR | 0.85 | 1.14 | 0.94 | 1.27 |
| SRR = B ÷ A | 2.66 | 4.96 | 4.10 | 4.70 |
| C: Median instrument skew | −0.09 | 0.84 | −0.17 | 0.63 |
| D: Aggregate Jumbo skew | −0.04 | 0.98 | 0.41 | 0.76 |
| Skew improvement = D − C | 0.05 | 0.14 | 0.58 | 0.13 |
| E: Median lower-tail ratio | 1.56 | 3.47 | 2.62 | 3.11 |
| F: Aggregate Jumbo lower-tail ratio | 1.44 | 1.99 | 1.57 | 1.86 |
| Tail improvement = E − F | 0.12 | 1.48 | 1.05 | 1.25 |

The chapter’s interpretations:

- Trend’s aggregate SR is far stronger relative to its median instrument SR than long-only’s (SRR 4.96 vs 2.66).
- Carry has higher instrument-level SR than trend but lower aggregate SR and SRR (4.10); the author speculates that stickier carry positions and trend’s outlier-market benefits may contribute.
- The combined strategy lies between them on median SR, but delivers the best aggregate SR and an SRR of 4.70.
- Carry’s adverse individual-instrument skew diversifies substantially across assets because bad skew events are mostly uncorrelated. The source notes the lower-tail measure improves most for momentum/trend, while carry’s tails are generally better than momentum’s for both median-instrument and aggregate results.
- The preferred mixture can differ with portfolio size: for a single instrument, carry offers better SR and trend nicer skew; for the Jumbo portfolio, trend is better on both. For all trader sizes, the author expects a combination to be preferable if one accepts a small sacrifice in either SR or skew for a larger improvement in the other.

## Trading-plan checklist (Strategy 11 figure)

| Item | Instruction |
|---|---|
| Strategy | Go long or short one or more instruments using a variable risk estimate and a combined forecast from multiple smoothed-carry and EWMAC forecasts. |
| Instruments | Any that meet minimum capital, liquidity, and cost thresholds. |
| Choose rules | Use turnover figures in table 35 (trend) and table 40 (carry). |
| Rule variations | See strategy nine (trend) and strategy ten (carry). |
| Allocate forecast weights | See Table 51. |
| Forecast diversification multiplier | See Table 52. |

## Constraints, warnings, and boundaries

- Exclude rule variations that breach the 0.15-SR-unit cost speed limit.
- Rule availability is instrument-specific; weights must be recalculated for its eligible subset.
- Forecast scale and cap must be applied before combination: absolute average 10; absolute maximum 20.
- FDM is a necessary step and was initially omitted in the narrative deliberately as a catch for attentive readers.
- Tables 49–50 are characteristics of the author’s Jumbo portfolios, not a universal optimisation result. Weight choice depends on preferences, portfolio size, and desired SR/skew/tail trade-off.
- The chapter references procedures and performance tables in prior chapters rather than reproducing their calculations; do not infer undocumented formulas from this chapter.

## Connections and conclusion

This strategy combines the forecast framework developed in strategies nine (multiple trend) and ten (carry), while relying on the risk scaling and portfolio construction introduced earlier in Part One. Tables 53–54 should be compared with trend tables 37–38 and carry tables 46–47. The remaining parts can be read independently: Part Two extends carry and trend; Part Three introduces other trading strategies; Parts Four and Five cover strategies outside this forecasting framework; Part Six addresses tactics for managing strategies. The footnote says strategies seven and eight are components of strategy nine, and strategies one to six do not use forecasting.

## Glossary candidates

Carry; convergent strategy; divergent strategy; EWMAC; EWMA; forecast; forecast diversification multiplier (FDM); forecast weight; Jumbo portfolio; lower/left tail ratio; risk-adjusted cost per trade; Sharpe ratio (SR); Sharpe ratio ratio (SRR); skew; speed limit; turnover; variable risk estimate.
