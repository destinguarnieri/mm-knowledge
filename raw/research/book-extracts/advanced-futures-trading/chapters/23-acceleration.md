# Strategy Twenty-Three: Acceleration

## Purpose and central argument

Trend-following rules respond late at both the beginning and end of a trend. Making ordinary trend rules faster may be prohibitively costly and may enter horizons at which trend following works less effectively. This strategy instead uses the *rate of change of a scaled trend forecast*—called **acceleration**—as an additional forecast. It is intended to identify whether an established trend is strengthening or weakening, and can diversify ordinary EWMAC trend following because its return correlations with EWMAC are relatively low.

The chapter uses EWMAC forecasts and their four tradable acceleration variants: `Acceleration8`, `Acceleration16`, `Acceleration32`, and `Acceleration64`.

## Construction

### Base EWMAC forecast

For a fast EWMA span \(N\), the slow EWMA span is \(4N\). The source uses the standard pairings EWMAC(2,8), EWMAC(4,16), and so on. A positive EWMAC forecast denotes an established bullish trend; a negative forecast denotes a bearish environment.

\[
\operatorname{Raw\ EWMAC\ forecast}_{N,t}=
\frac{\operatorname{EWMA}_{N,t}-\operatorname{EWMA}_{4N,t}}{\sigma_{p,t}}
\]

\[
\operatorname{Forecast}_{N,t}=\operatorname{Raw\ forecast}_{N,t}\times\operatorname{EWMAC\ forecast\ scalar}_{N}
\]

- \(N\): fast moving-average span, in business days.
- \(t\): current time/business day.
- \(\operatorname{EWMA}_{N,t}\), \(\operatorname{EWMA}_{4N,t}\): fast and slow exponentially weighted moving averages at \(t\).
- \(\sigma_{p,t}\): annual standard deviation of returns for the price/instrument, at \(t\).
- `EWMAC forecast scalar`: scaling factor used so the ordinary forecast has average absolute value 10.

### Acceleration forecast

Acceleration is measured over the same number of business days as the fast EWMAC span. This choice avoids fitting an additional parameter; the author reports sensitivity analysis for that arbitrary choice, but no results are given in this chapter.

\[
\operatorname{Raw\ acceleration}_{N,t}=\operatorname{Forecast}_{N,t}-\operatorname{Forecast}_{N,t-N}
\]

\[
\operatorname{Acceleration}_{N,t}=\operatorname{Raw\ acceleration}_{N,t}\times\operatorname{Acceleration\ forecast\ scalar}_{N}
\]

- \(\operatorname{Forecast}_{N,t-N}\): scaled EWMAC forecast \(N\) business days earlier.
- \(\operatorname{Raw\ acceleration}_{N,t}\): change in the scaled EWMAC forecast over \(N\) business days. The source does not explicitly state the units; it is not divided again by elapsed time in the displayed formula.
- `Acceleration forecast scalar`: a separate calibration factor. No new risk adjustment is applied because the underlying EWMAC forecast is already divided by annual return volatility; the separate scalar is still needed for technical scaling reasons.

### Forecast scalars (Table 100)

| Rule | Acceleration forecast scalar |
|---|---:|
| Acceleration8 | 1.87 |
| Acceleration16 | 1.90 |
| Acceleration32 | 1.98 |
| Acceleration64 | 2.05 |

The scalars follow the previously observed approximate square-root-of-two pattern as rule speed is doubled or halved. Acceleration2 and Acceleration4 are excluded: their turnovers are prohibitively high, substantially above EWMAC2.

## Interpretation: trend direction × acceleration

| Trend forecast | Acceleration forecast | Meaning | Position implication |
|---|---|---|---|
| Negative | Negative | Bearish trend becoming more bearish | The forecasts agree; larger position suggested. |
| Negative | Positive | Bearish trend becoming less bearish; it may be near an end | Mixed messages; smaller position suggested. |
| Positive | Positive | Established bullish trend becoming more bullish | The forecasts agree; larger position suggested. |
| Positive | Negative | Bullish trend becoming less bullish; it may be near an end | Mixed messages; smaller position suggested. |

## Figures and worked interpretation

- **Figure 76 — Back-adjusted Bitcoin futures price:** price rises from roughly August 2020 through an April 2021 peak, then reverses sharply. It supplies the market example for the forecasts below.
- **Figure 77 — Raw EWMAC64 and Acceleration64 forecasts for Bitcoin futures:** EWMAC64 stays long/bullish throughout the displayed period even after the market turns, though it declines as the trend becomes unclear. Acceleration64 is initially positive (scenario 3) and remains long until June 2021. After the trend forecast has slowed for several weeks, acceleration turns negative, indicating scenario 4—a weakening bullish trend—before the slower EWMAC64 signal becomes bearish. The chapter's point is reduced exposure/loss relative to a constant or solely lagging trend position, not a claim that acceleration alone immediately predicts the reversal.

## Relationship with EWMAC (Table 101)

These are correlations of **returns**, calculated from aggregate Jumbo-portfolio returns. The author says an individual instrument selected at random shows a similar pattern.

| EWMAC rule | Accel8 | Accel16 | Accel32 | Accel64 |
|---|---:|---:|---:|---:|
| EWMAC2,8 | 0.72 | 0.56 | 0.38 | 0.18 |
| EWMAC4,16 | 0.69 | 0.75 | 0.58 | 0.31 |
| EWMAC8,32 | 0.40 | 0.71 | 0.76 | 0.50 |
| EWMAC16,64 | 0.08 | 0.38 | 0.68 | 0.66 |
| EWMAC32,128 | −0.07 | 0.09 | 0.39 | 0.63 |
| EWMAC64,256 | −0.07 | −0.02 | 0.09 | 0.33 |

No displayed correlation exceeds 0.76, supporting the claim that acceleration does materially different things from EWMAC. A given Acceleration\(N\) is usually most correlated with the EWMAC whose **slow** EWMA span is \(N\): e.g., Acceleration8 with EWMAC(2,8), and Acceleration16 with EWMAC(4,16). For contrast, the chapter cites a 0.97 correlation between normalized trend (strategy 17) and mixed trend (strategy 9).

## Stand-alone performance (Table 102)

Aggregate Jumbo-portfolio results, with all instruments included—even those too expensive for a particular variation—so the figures can be compared directly with the EWMAC tables cited in the source (Tables 30 and 31). The appropriate comparison for Acceleration\(N\) is EWMAC with slow span \(N\), such as Acceleration8 versus EWMAC(2,8).

| Metric | Accel8 | Accel16 | Accel32 | Accel64 |
|---|---:|---:|---:|---:|
| Mean annual return (gross) | 11.1% | 17.5% | 12.8% | 13.1% |
| Mean annual return (net) | 4.8% | 14.1% | 10.6% | 11.2% |
| Costs | −6.2% | −3.3% | −2.2% | −1.9% |
| Average drawdown | >100% | −19.9% | −25.9% | −28.7% |
| Standard deviation | 24.7% | 24.1% | 24.5% | 24.4% |
| Sharpe ratio | 0.20 | 0.59 | 0.43 | 0.46 |
| Turnover | 258.8 | 136.2 | 81.6 | 57.9 |
| Skew | 0.97 | 1.55 | 1.11 | 0.34 |
| Lower tail | 1.75 | 1.72 | 1.71 | 1.86 |
| Upper tail | 1.99 | 1.94 | 1.87 | 1.72 |
| Annualised alpha (gross) | 10.0% | 15.6% | 11.9% | 11.8% |
| Annualised alpha (net) | 3.8% | 12.3% | 9.7% | 9.9% |
| Beta | 0.07 | 0.13 | 0.07 | 0.09 |

All variants are profitable, but none is as good as its closest EWMAC match. Their much lower beta is the reason offered for using them as diversifiers. Acceleration8's high turnover and 6.2% annualized costs leave it with the weakest net performance.

## Combining acceleration variants

### Eligibility turnover inputs (Table 103)

| Rule | Forecast turnover |
|---|---:|
| Acceleration8 | 64.0 |
| Acceleration16 | 34.4 |
| Acceleration32 | 20.9 |
| Acceleration64 | 14.9 |

Use only rule variations that satisfy the strategy-plan cost constraint:

\[
\operatorname{Turnover}<\frac{0.15-[(\operatorname{Cost\ per\ trade})\times(\operatorname{Rolls\ per\ year})]}{\operatorname{Cost\ per\ trade}}
\]

`Cost per trade` and `rolls per year` are instrument-specific inputs; the source does not restate their units or estimation method in this chapter. The 0.15 threshold is presented exactly as shown.

### Correlations across acceleration horizons (Table 104)

| Rule | Accel8 | Accel16 | Accel32 | Accel64 | Average vs. other horizons |
|---|---:|---:|---:|---:|---:|
| Acceleration8 | 1.00 | 0.53 | 0.07 | −0.07 | 0.18 |
| Acceleration16 |  | 1.00 | 0.51 | 0.04 | 0.36 |
| Acceleration32 |  |  | 1.00 | 0.50 | 0.36 |
| Acceleration64 |  |  |  | 1.00 | 0.15 |

Adjacent acceleration variants are near 0.50–0.53, much lower than the greater-than-0.8 adjacent-variation correlations reported for EWMAC and other trading rules. This low dependence is the stated basis for meaningful diversification from combining speeds.

### Equal-weight/FDM sets (Table 105)

| Available acceleration rules | Weight of each included rule | FDM |
|---|---:|---:|
| 8, 16, 32, 64 | 0.25 | 1.55 |
| 16, 32, 64 | 0.333 | 1.37 |
| 32, 64 | 0.50 | 1.17 |
| 64 | 1.00 | 1.00 |

The highest FDM, 1.55 for all four variants, exceeds the chapter's cited highest FDM of 1.26 for strategy 9's six EWMAC variants. The source attributes this to lower inter-variant correlations.

### Combined-rule results (Table 106)

| Metric | Median across instruments | Aggregate Jumbo portfolio |
|---|---:|---:|
| Mean annual return | 1.4% | 16.7% |
| Costs | −0.7% | −1.9% |
| Average drawdown | −32.7% | −17.2% |
| Standard deviation | 24.8% | 23.2% |
| Sharpe ratio | 0.08 | 0.72 |
| Turnover | 24.9 | 99 |
| Skew | 0.94 | 0.98 |
| Lower tail | 3.05 | 1.77 |
| Upper tail | 3.09 | 1.91 |

The combined acceleration strategy is not quite as good as strategy 9's combined EWMAC benchmark, although monthly skew is identical. Its most notable result is the diversification gain from a barely profitable median instrument to the aggregate portfolio: Sharpe ratio rises ninefold (0.08 to 0.72), versus just under fivefold for strategy 9. Skew does not improve similarly because individual instruments already have relatively high skew.

## Adding acceleration to carry and trend

The allocation is top-down:

1. Allocate 40% to convergent style and 60% to divergent style, as in strategy 11.
2. Allocate the full convergent 40% to carry.
3. Split the divergent 60%: 30% EWMAC and 30% acceleration.
4. Split carry's 40% equally across up to four carry variations.
5. Split acceleration's 30% equally across up to four acceleration variations.
6. Split EWMAC's allocation equally across up to six EWMAC variations. **Source ambiguity:** the text says these variations “share 60% equally,” which is consistent with the divergent-style total but conflicts with the immediately preceding 30% EWMAC allocation. The chapter does not resolve this.

### Aggregate Jumbo-portfolio comparison (Table 107)

| Metric | Strategy 9: multiple trend | Acceleration-only column* | Strategy 11: carry & trend | Strategy 23: carry, acceleration & trend |
|---|---:|---:|---:|---:|
| Mean annual return | 25.2% | 16.7% | 26.5% | 26.9% |
| Costs | −1.2% | −1.9% | −1.1% | −1.3% |
| Average drawdown | −11.2% | −17.2% | −8.9% | −8.5% |
| Standard deviation | 22.2% | 23.2% | 20.9% | 20.9% |
| Sharpe ratio | 1.14 | 0.72 | 1.27 | 1.29 |
| Turnover | 62.9 | 99.0 | 46.5 | 59.1 |
| Skew | 0.98 | 0.98 | 0.76 | 0.91 |
| Lower tail | 1.99 | 1.77 | 1.86 | 1.79 |
| Upper tail | 1.81 | 1.91 | 1.75 | 1.80 |
| Alpha | 18.8% | 15.2% | 22.3% | 24.0% |
| Beta | 0.43 | 0.11 | 0.30 | 0.22 |

\*The EPUB table labels this column “Strategy twenty-one / Acceleration,” despite this chapter identifying acceleration as strategy twenty-three. This study file preserves the data but flags the source-label inconsistency rather than correcting it.

Adding acceleration raises costs because of turnover, but the chapter concludes it improves all other reported measures relative to the basic carry-and-trend strategy and appears to add an edge.

## Trading plan

- **Strategy:** go long or short one or more instruments using a variable risk estimate and a forecast based on the difference between two trend forecasts.
- **Eligible instruments:** any that meet minimum capital, liquidity, and cost thresholds.
- **Permitted rule variants:** Acceleration built from EWMAC(\(N,4N\)), with \(N\in\{8,16,32,64\}\), subject to the turnover cost constraint above.
- **Raw/derived forecast:** calculate the volatility-adjusted EWMAC forecast, scale it with the EWMAC scalar, then calculate its \(N\)-business-day change. The plan image calls this row “Raw forecast,” but its formula is the acceleration difference; the equation is preserved under *Acceleration forecast* above.
- **Acceleration scalars:** Table 100.
- **Weights and FDM:** Table 105.
- **Other implementation stages:** identical to strategy 9; this chapter does not reproduce them.

## Constraints, warnings, and takeaways

- Faster EWMAC alternatives can be too costly, and pre-cost trend performance degrades for the two fastest variations (EWMAC4 and EWMAC2); after-cost results are worse still.
- Acceleration2 and Acceleration4 are not used due to prohibitive turnover.
- Stand-alone acceleration is profitable but inferior to matched EWMAC; its value in the chapter is diversification, including low beta and low correlations across speeds.
- Signals agreeing on direction imply a larger position; disagreement implies reduced position—not necessarily an immediate reversal trade.
- Reported aggregate results may differ greatly from the median instrument; do not infer individual-instrument quality from portfolio performance.
- Tables 102 and 106 use the “Jumbo” portfolio; the chapter does not define it here.

## Connections to other chapters

- **Strategy 7:** introduced strength-adjusted forecasts rather than constant positions.
- **Strategy 9:** provides the general multiple-rule combination method; its Tables 36 and 39 are cited for FDM and combined EWMAC benchmarking. All unshown trading-plan stages are said to be identical to strategy 9.
- **Strategy 11:** supplies the original carry-and-trend mix and 40% convergent / 60% divergent style allocation.
- **Strategy 17:** normalized trend is cited as a contrast: it correlated 0.97 with mixed trend from strategy 9.
- **Breakout and value:** the carry/trend/acceleration combination is said to follow the same testing approach used when adding breakout and value.

## Glossary

- **Acceleration forecast:** scaled change in a scaled EWMAC forecast over \(N\) business days.
- **EWMAC:** exponentially weighted moving-average crossover; here uses a fast span \(N\) and slow span \(4N\).
- **Forecast scalar:** calibration multiplier; the base EWMAC scalar makes average absolute forecast equal 10, while acceleration requires a distinct scalar.
- **FDM (forecast diversification multiplier):** multiplier reported for a set of forecast variations to reflect diversification.
- **Convergent / divergent styles:** the two style buckets used for the carry/trend/acceleration allocation.
- **Turnover:** forecast turnover, used here to decide whether an instrument can trade a rule variation under its cost constraint.
- **Jumbo portfolio:** aggregate portfolio used for reported results; not defined in this chapter.
