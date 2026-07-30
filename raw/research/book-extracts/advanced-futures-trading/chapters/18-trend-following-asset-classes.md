# Strategy eighteen: Trend following asset classes

## Purpose and central argument

This strategy treats movements within an asset class as largely synchronised. Rather than trend-follow each future from its own price history, it constructs a volatility-normalised price index for an asset class, applies EWMAC trend filters to that index, and assigns the resulting asset-class forecast to its constituent instruments.

The proposed rationale is a **latent** (hidden) trend shared by instruments in an asset class, with each observable instrument price comprising that latent trend plus idiosyncratic noise. Averaging normalised price changes across the class is intended to measure that common trend and therefore give a cleaner signal.

The chapter finds that this improves median single-instrument performance versus the original multiple-trend portfolio, especially in equities, but weakens the aggregate Jumbo portfolio because forecasts become much less diversified within each asset class. It can nevertheless be useful for capital-constrained traders who can hold only one or two instruments per asset class, and can be a modestly useful addition alongside carry and the other trend variants.

## Core concepts and distinctions

- **Asset-class trend:** a trend forecast produced from a common, normalised asset-class price, then used for instruments in that class.
- **Latent trend:** the hypothesised unobserved common trend driving instruments in an asset class. An individual observable index is described as the latent trend plus idiosyncratic noise.
- **Volatility-normalised price:** a cumulative price-like series built from daily price changes scaled by a price-change standard deviation. The unitless construction makes series comparable in risk terms across instruments and gives consistent volatility over time.
- **Normalised asset-class price (`A`):** the cumulative average of constituent instruments’ normalised daily price changes.
- **EWMAC(`N`, `4N`):** an exponentially weighted moving-average crossover using a fast EWMA with span `N` business days and a slow EWMA with span `4N`.
- **Original trend / normalised trend / asset-class trend:** respectively, strategy nine’s back-adjusted-price trend; strategy seventeen’s instrument-level normalised-price trend; and this chapter’s asset-class-level normalised-price trend.
- **Divergent and convergent rules:** trend is classified as divergent and carry as convergent for the top-down forecast-allocation method.
- **Forecast diversification multiplier (FDM):** a multiplier applied when combining forecasts. The chapter directs the reader to prior tables for its values; it does not reproduce the values.

## Constructing the asset-class price

The construction uses only futures prices, unlike conventional investable asset-class indices that are typically based on percentage returns of individual instruments and weighted by market capitalisation or similar metrics.

The chapter cites four drawbacks of using conventional published indices here:

1. They are outside the book’s futures-price-only scope.
2. They implicitly give more weight to higher-volatility instruments.
3. Their instrument universe may not be the actual traded universe.
4. Their market-capitalisation weights may be heavily biased. As an example, the cited footnote says 69% of the MSCI World Developed Equity Index was currently in US stocks.

The alternative requires no additional data, controls for different instrument risks, permits a custom basket, and permits a chosen weighting scheme. The reported results use asset-price indices from more than 140 instruments, compared with 102 tradeable instruments in the Jumbo portfolio. The index may include instruments not actually traded—because they are too expensive, illiquid, or beyond available capital—to improve the robustness of the asset-price-trend measure.

### 1. Normalise each constituent future

For each instrument `i` in the asset class:

\[
P^N_{i,t}=100\times\frac{p_{i,t}-p_{i,t-1}}{\sigma_{p,i,t}}+P^N_{i,t-1}
\]

Where:

| Symbol | Meaning | Units/domain |
|---|---|---|
| `P^N_{i,t}` | Normalised price of instrument `i` at time `t` | Normalised-price units; cumulative series |
| `p_{i,t}` | Price of instrument `i` at time `t` | Instrument-price units |
| `p_{i,t-1}` | Prior-period price of instrument `i` | Same units as `p_{i,t}` |
| `σ_{p,i,t}` | Standard deviation of price changes for instrument `i` at time `t` | Same units as the price change; must be nonzero to divide |
| `100` | Fixed scaling constant | Normalised-price units per standard-deviation-scaled price change |
| `t` | Time index | The text subsequently refers to daily returns and business-day EWMA spans |

This is the normalised-price calculation introduced in strategy seventeen. The chapter does not state an initialization rule for `P^N_{i,0}`.

### 2. Average normalised daily changes across the class

For the asset class’s average daily return `R`:

\[
R_t=\frac{[P^N_{0,t}-P^N_{0,t-1}]+[P^N_{1,t}-P^N_{1,t-1}]+\ldots+[P^N_{j,t}-P^N_{j,t-1}]}{j}
\]

Where `i = 0` through `i = j`, and the text identifies `j` as the number of instruments in the asset class. The method uses equal weights and a simple average, although other weights may be used.

**Source notation caution:** as printed, the numerator includes indices `0` through `j` while the denominator is `j`. That would be `j + 1` terms divided by `j` if `j` is an inclusive final index. The prose also says `j` is the number of instruments. The chapter does not resolve this indexing/denominator ambiguity; do not silently alter it in an implementation.

| Symbol | Meaning | Units/domain |
|---|---|---|
| `R_t` | Average daily normalised-price change for the asset class at `t` | Normalised-price units per day |
| `j` | Stated to be the number of instruments in the asset class | Positive integer; see source-notation caution |
| `P^N_{i,t}-P^N_{i,t-1}` | Daily normalised-price change for constituent `i` | Normalised-price units per day |

### 3. Cumulate the average changes

\[
A_t=R_1+R_2+\ldots+R_t
\]

Where:

| Symbol | Meaning | Units/domain |
|---|---|---|
| `A_t` | Normalised price for asset class `A` at time `t` | Cumulative normalised-price units |
| `R_k` | Asset-class average daily return/change at period `k` | Normalised-price units per day |

The chapter explicitly notes that `A_0` is zero.

### Figures 70–71

- **Figure 70, “Normalised asset class trend for financials”:** plots normalised asset-class prices for financial asset classes. The chapter says the normalised prices have consistent volatility over time and identifies the equity bear markets of the early 2000s and 2008 as clearly visible significant trends.
- **Figure 71, “Normalised asset class momentum for commodities”:** plots normalised asset-class price/momentum series for commodity asset classes. The chapter uses it, together with Figure 70, to illustrate the trend content of the constructed normalised series. The image has no embedded legend/text extract sufficient to name every plotted series; this is flagged rather than inferred.

## Applying trend following

The strategy is otherwise like strategy nine, except that:

1. It uses the normalised price for the relevant **asset class**, not an individual instrument’s back-adjusted price.
2. Each instrument in the same asset class has the same forecast for a given trend speed.

A qualification in footnote 195 is important: the final *combined* forecasts can differ because not every instrument in the class may be cheap enough to trade every speed of asset-class trend.

Use up to six EWMAC speeds. Forecast scalars are the same as strategy nine, and turnover at each trend speed is roughly the same as strategy seventeen. The chapter says the forecast-diversification multipliers estimated in strategy nine may also be used.

### EWMAC procedure

Choose one or more EWMAC(`N`, `4N`) filters, with `N` one of `2, 4, 8, 16, 32, 64` business days.

For the `N`-business-day EWMA of normalised asset price `A`:

\[
\lambda=\frac{2}{N+1}
\]

\[
\operatorname{EWMA}_{i}(N)_t=λ A_t+λ(1-λ)A_{t-1}+λ(1-λ)^2A_{t-2}+…
\]

The figure prints an `i` subscript on EWMA even though `A` is an asset-class series and the immediately following text says every `i` in the class receives the same forecast. Treat that subscript as source notation, not evidence of an instrument-specific asset-class EWMA.

| Symbol | Meaning | Units/domain |
|---|---|---|
| `N` | Fast EWMA span | One of 2, 4, 8, 16, 32, 64 business days |
| `4N` | Slow EWMA span | Four times the fast span |
| `λ` | EWMA smoothing constant | `2/(N+1)` |
| `A_t` | Normalised asset-class price | Cumulative normalised-price units |
| `EWMA_i(N)_t` | Printed EWMA notation for `A` | Same units as `A`; see notation caution |

For each instrument `i` in the class, calculate the raw forecast:

\[
\operatorname{RawForecast}_{N,i,t}=\frac{\operatorname{EWMA}(N)_{i,t}-\operatorname{EWMA}(4N)_{i,t}}{\sigma^A_{p,t}}
\]

where `σ^A_{p,t}` is the daily standard deviation of price changes for the normalised asset price. Thus the raw forecast is identical for all instruments in the asset class at a given speed.

Scale and cap it:

\[
\operatorname{ScaledForecast}_{N,i,t}=\operatorname{RawForecast}_{N,i,t}\times\operatorname{ForecastScalar}_{N}
\]

\[
\operatorname{CappedForecast}_{N,i,t}=\max\bigl(\min(\operatorname{ScaledForecast}_{N,i,t},+20),-20\bigr)
\]

| Symbol | Meaning | Units/domain |
|---|---|---|
| `σ^A_{p,t}` | Daily standard deviation of changes in normalised asset price | Normalised-price units per day; must be nonzero |
| `RawForecast` | Fast-minus-slow EWMAC spread, risk-normalised | Forecast units |
| `ForecastScalar_N` | Speed-specific scaling factor | Directed to Table 29, p.177; not reproduced here |
| `ScaledForecast` | Scalar-adjusted forecast | Forecast units |
| `CappedForecast` | Final per-speed forecast | Constrained to `[-20, +20]` |

## Standalone performance evidence

Tables 76 and 77 report median instrument performance by asset class. The chapter compares them with Tables 37–38 (p.195) for strategy nine and notes that some uninteresting figures were omitted.

### Table 76 — financial asset classes

| Metric | Equity | Vol | FX | Bond |
|---|---:|---:|---:|---:|
| Mean annual return | 3.1% | 12.5% | 4.9% | 13.2% |
| Costs | −0.5% | −1.1% | −0.6% | −0.6% |
| Standard deviation | 25.8% | 25.6% | 24.0% | 26.0% |
| Sharpe ratio | 0.12 | 0.49 | 0.19 | 0.52 |
| Skew | 0.28 | 0.37 | 0.73 | 0.77 |
| Lower tail | 3.13 | 3.15 | 3.07 | 2.56 |

### Table 77 — commodity asset classes

| Metric | Metals | Energy | Ags | Median |
|---|---:|---:|---:|---:|
| Mean annual return | 11.8% | 8.9% | 7.7% | 7.1% |
| Costs | −0.5% | −0.5% | −0.4% | −0.5% |
| Standard deviation | 25.4% | 25.9% | 25.5% | 25.5% |
| Sharpe ratio | 0.45 | 0.36 | 0.30 | 0.30 |
| Skew | 1.65 | 0.88 | 0.90 | 0.57 |
| Lower tail | 3.00 | 3.24 | 2.48 | 2.93 |

The chapter interprets the median Sharpe ratio of 0.30 as better than the 0.23 for strategy nine’s original multiple-trend portfolio, suggesting cleaner signals. Equities show the largest improvement: SR 0.12, versus 0.03 for back-adjusted-price trend in strategy nine and a negative SR for normalised trend in strategy seventeen. Footnote 196 notes that this makes strategy sixteen’s approach of reducing trend-versus-carry allocation only for equities less sensible here.

### Table 78 — aggregate Jumbo portfolio comparison

| Metric | Strategy 9: multiple trend (back-adjusted price) | Strategy 17: multiple trend (instrument normalised price) | Strategy 18: multiple trend (asset-class normalised price) |
|---|---:|---:|---:|
| Mean annual return | 25.2% | 28.2% | 24.0% |
| Costs | −1.2% | −1.4% | −1.3% |
| Average drawdown | −11.2% | −12.9% | −14.6% |
| Standard deviation | 22.2% | 24.4% | 23.5% |
| Sharpe ratio | 1.14 | 1.15 | 0.97 |
| Turnover | 62.9 | 72.1 | 65.5 |
| Skew | 0.98 | 0.93 | 0.94 |
| Lower tail | 1.99 | 1.87 | 1.94 |
| Upper tail | 1.81 | 1.80 | 1.82 |
| Alpha | 18.8% | 20.1% | 15.9% |
| Beta | 0.43 | 0.55 | 0.46 |

The individual-instrument outperformance disappears after aggregation. The chapter’s explanation is forecast concentration: within an asset class, instruments almost always have the same sign (all long or all short), so diversification is primarily across asset classes. The performance improvement from median instrument to aggregate portfolio falls from a factor of five to a little above three, enough to offset the instrument-level improvement.

## Combining asset-class trend with carry and other trend rules

The chapter does not recommend simply replacing the original trend rules with asset-class trend, except potentially for smaller accounts or for equities. It instead tests adding it to carry plus original and normalised trend.

### Top-down allocation procedure

1. Allocate 60% to divergent (trend) rules and 40% to convergent (carry) rules.
2. Divide trend equally among original trend, normalised trend, and asset-class trend: 20% to each.
3. Allocate the full 40% carry allocation to the single carry rule family.
4. Within a rule family, allocate equally across the available variations.

**Worked allocation example — WTI Crude Oil future:** It can trade four carry rules and the four slowest trend rules of each of the three trend types, for 16 rules total.

| Rule group | Group allocation | Variations | Allocation per variation |
|---|---:|---|---:|
| Original trend | 20% | EWMAC8, EWMAC16, EWMAC32, EWMAC64 | 5% |
| Normalised trend | 20% | Four slowest variations | 5% |
| Asset-class trend | 20% | Four slowest variations | 5% |
| Carry | 40% | carry5, carry20, carry60, carry120 | 10% |

Use FDMs appropriate to the number of variations, from Table 52 (p.234).

### Table 79 — adding trend variants to carry plus trend

| Metric | Strategy 11: carry + adjusted-price trend | Strategy 17: carry + normalised and adjusted-price trend | Strategy 18: carry + asset-class, normalised, and adjusted-price trend |
|---|---:|---:|---:|
| Mean annual return | 26.5% | 27.5% | 28.3% |
| Costs | −1.1% | −1.1% | −1.1% |
| Average drawdown | −8.9% | −8.7% | −9.1% |
| Standard deviation | 20.9% | 20.9% | 21.7% |
| Sharpe ratio | 1.27 | 1.32 | 1.31 |
| Turnover | 46.5 | 47.6 | 46.1 |
| Skew | 0.76 | 0.75 | 0.71 |
| Lower tail | 1.86 | 1.85 | 1.85 |
| Upper tail | 1.75 | 1.70 | 1.81 |
| Alpha | 22.3% | 22.9% | 24.0% |
| Beta | 0.30 | 0.32 | 0.31 |

Adding asset-class prices lowers SR slightly (1.32 to 1.31 relative to strategy seventeen), but raises alpha (22.9% to 24.0%) due to slightly lower beta (0.32 to 0.31). The chapter says this modest alpha increase is statistically significant. Footnote 197 explains why small differences can be significant when returns are highly correlated: correlations among the three trend types are about 0.96, and correlations among the table’s strategies are about 0.98.

## Trading plan

| Stage | Instruction |
|---|---|
| Strategy | Go long or short one or more instruments using variable risk estimates and a combined forecast from multiple trend filters; modify filters to use the relevant asset class’s normalised price as input. |
| Eligible instruments | Any meeting minimum capital, liquidity, and cost thresholds. |
| Choosing rules | Turnover figures are directed to Table 73, p.304. |
| Rule variations | Construct one or more EWMAC(`N`, `4N`) filters for `N ∈ {2,4,8,16,32,64}`. |
| Forecast scalars | Table 29, p.177. |
| Forecast cap | Cap each scaled forecast at +20 / −20. |
| Forecast weights | Table 36, p.193 for standalone trend; Table 51, p.233 when combined with carry; p.316 when combined with carry and other trend types. |
| FDM | Table 36, p.193 for standalone asset-class trend; Table 52, p.234 when combined with carry and/or standard trend. |
| Other stages | Identical to strategy nine for standalone trend or strategy eleven when combined with carry. |

## Practical implications, constraints, and warnings

- The asset-class basket can and, for robustness, may include markets that are not tradeable by the user. Positions are still taken only in eligible instruments.
- The strategy presumes that the shared asset-class signal is useful. It deliberately sacrifices instrument-specific signal differences.
- Limited-capital traders who can hold only one or two instruments per asset class may benefit most, because the broader index can incorporate instruments they cannot hold.
- Asset-class trend is relatively strong in equities in the reported analysis, but increasing its equity allocation could be overfitting.
- The author views the performance increment from adding asset-class trend as modest and potentially not worth added operational complexity for a non-automated strategy, though personally favours using as many trend types as available.
- Standard-deviation denominators in the formulas must be estimable and nonzero; the chapter gives no fallback treatment for unavailable or zero volatility estimates.
- Source notation has two ambiguities: the `0..j` average denominator described above, and an instrument subscript on the asset-class EWMA. Both should be resolved explicitly before coding, rather than guessed.

## Connections to other chapters/strategies

- **Strategy nine:** baseline EWMAC trend using each instrument’s back-adjusted price; provides identical forecast scalars and prior FDM estimates. Tables 37–38 (p.195) are the relevant baseline performance comparison; Table 36 (p.193) supplies standalone weights/FDM.
- **Strategy eleven:** carry plus original trend; all non-asset-class stages follow it when this strategy is combined with carry. Table 51 (p.233) supplies weights for carry combinations.
- **Strategy sixteen:** its equity-specific reduction in trend-versus-carry allocation is less appropriate here, per footnote 196.
- **Strategy seventeen:** provides the constituent-instrument normalised-price construction; comparable turnover; normalised trend is one of the trend types combined in Table 79.
- **Table 52 (p.234):** FDM values for the relevant number of rule variations when combining carry and/or standard trend.

## Key takeaways

1. Construct a futures-only asset-class index by averaging volatility-normalised constituent price changes and cumulating them.
2. Feed the common series into EWMAC(`N`, `4N`) filters; every class member gets the same per-speed forecast.
3. The signal appears cleaner at a median-instrument level (SR 0.30 vs 0.23 baseline), with the clearest relative improvement in equities.
4. Aggregate performance is poorer than the other two standalone trend variants because common forecasts eliminate within-class forecast diversification.
5. In a carry-plus-trend portfolio, adding asset-class trend slightly reduces SR but increases alpha in the reported results; the author calls the alpha gain statistically significant but modest.

## Glossary

- **Asset-class index price:** cumulative average of normalised changes of the asset class’s constituents.
- **Asset-class trend:** trend following driven by a shared asset-class index rather than individual prices.
- **Back-adjusted price:** the price input used by strategy nine (definition not reproduced in this chapter).
- **Carry:** convergent trading rule family used alongside trend.
- **EWMAC:** exponentially weighted moving-average crossover.
- **FDM:** forecast diversification multiplier.
- **Forecast scalar:** EWMAC-speed-specific multiplier that scales the raw forecast.
- **Latent trend:** hidden common trend hypothesised to underlie related instruments.
- **Normalised price:** volatility-scaled cumulative price series.
- **Raw / scaled / capped forecast:** successive EWMAC forecast stages, the last constrained to ±20.
- **Turnover:** reported trading-activity measure; no definition is supplied in this chapter.
