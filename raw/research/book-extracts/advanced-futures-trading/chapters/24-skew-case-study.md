# Strategy 24 — Skew: a case study

## Purpose and central argument

This chapter uses **skew** to show how to fit a prospective trading idea into the book's forecasting framework. A usable strategy must begin with quantifiable information that can be turned into a forecast; it should also make economic sense, be robust, be risk-normalised (where necessary), be smoothed, scaled, capped, and then assessed alone and in a diversified portfolio.

The case-study rule is simple: **buy instruments with more negative skew and short instruments with more positive skew.** The economic intuition is a risk premium: investors value positively skewed payoffs (lottery-like upside) and may overpay for them; holding negatively skewed assets may therefore earn compensation. The chapter presents this as a plausible rationale, not as an explanation of *why* investors prefer positive skew.

## Core concepts and constraints

### Economic rationale: risk premia

- A risk premium is payment for bearing a risk the average investor or trader does not want.
- Examples used to illustrate demand for positive skew are lottery tickets, long-shot horse-race bets, far-out-of-the-money options, and high-multiple “moon-shot” meme stocks.
- The intended trade is therefore long negative-skew assets and short positive-skew assets. This deliberately exposes the strategy to the adverse behaviour of negative-skew assets in crises.

### Requirements for a candidate strategy

1. **Quantifiable statistic:** subjective chart patterns, merger-approval judgments, and the mood of an earnings call are not directly usable unless converted into a number (for example, by pattern recognition or voice analysis). The number need only be correlated with expected future price moves at this stage; it need not yet be proportional to expected risk-adjusted return.
2. **Robustness:** a forecast should not change materially after small market-data perturbations. A diagnostic is to add a small amount of noise to back-adjusted prices before running the backtest; a robust forecast should leave positions and performance mostly unchanged.
3. **Avoid stale or too-small samples:** for daily skew estimates, a few weeks is an absolute minimum for accuracy, while more than a year may include out-of-date information. The chapter chooses windows between one month and one year.
4. **Avoid overfitting:** do not optimise the skew window merely to find the highest historical result. Choose variations with sound logic and evaluate broad option sets with an appropriately robust process.

## The skew statistic and raw forecast

Skew is updated daily from daily percentage returns. It is sensitive to outliers: Figure 78 shows VIX-futures skew, estimated in rolling three-month windows, falling sharply in late March 2020 after one very large negative return and rising sharply in mid-June when that return leaves the window. Possible alternatives are exponentially weighted estimation or more robust tail measures (linked to Strategy 1); the chapter instead retains the standard skew formula and uses windows no shorter than three months.

Three pre-specified business-day windows are used, following the author's doubling convention:

| Rule | Estimation window | Approximate horizon |
|---|---:|---|
| `skew60` | 60 days | 3 months |
| `skew120` | 120 days | 6 months |
| `skew240` | 240 days | 12 months |

For daily percentage returns in the back-adjusted price, the raw forecast is:

\[
\operatorname{RawSkewForecast}_{w,t}=-\operatorname{Skew}(r_t,r_{t-1},r_{t-2},\ldots,r_{t-w+1})
\]

Where:

- \(r_t\) = daily percentage return at time \(t\).
- \(w\) = rolling estimation-window length in business days (60, 120, or 240).
- \(t\) = current day.
- \(\operatorname{Skew}(\cdot)\) = the standard skew statistic over the returns in the specified window.
- The negative sign encodes the premise that high positive skew implies poor expected return.

For backtesting, the chapter specifies that each daily percentage return is the difference between two daily **back-adjusted** prices divided by the price of the futures contract actively traded at that time—not divided by the back-adjusted price.

### Risk normalisation

A forecast is a prediction for risk-adjusted prices; dividing an expected price change by return standard deviation makes it proportional to a Sharpe-ratio prediction and dimensionless. Skew needs no separate risk normalisation because its standard formula already divides by standard deviation. Thus it is directly comparable across instruments and time periods.

## Strategy construction choices

For an already risk-adjusted forecast \(f\), the chapter distinguishes:

| Type | Long when | Main implication for skew |
|---|---|---|
| Absolute | \(f>0\) | Used here. Long when estimated skew is below zero; preserves asset-class biases and global timing. |
| Demeaned | \(f\) exceeds its global historical mean | Removes long bias; may lower outright performance and beta, perhaps improve alpha; retains asset-class biases. |
| Relative | \(f\) exceeds that instrument's historical mean | Expected average position is zero per instrument; removes asset-class bias but also loses a potential return source. |
| Cross-sectional | \(f\) exceeds today's cross-asset average | Net forecast is zero; retains asset-class bias but loses global timing. |
| Asset-class cross-sectional | \(f\) exceeds its asset-class average today | Removes asset-class bias but retains within-class bias; may need finer splits such as emerging vs developed FX. |
| Aggregated asset class | the asset-class average exceeds the global cross-asset average | Retains asset-class bias and global timing; loses within-class cross-sectional return. |
| Static | instrument's historical mean exceeds global historical mean | Bakes in asset-class biases and has no timing effect; potentially suits a risk-parity-style investor seeking the premium with little trading. |

Most asset classes have negative skew. The exceptions named are volatility instruments such as VIX, plus bonds and agricultural markets (modestly positive skew on average). With absolute skew, the portfolio is generally long; it is especially long equities (median skew −0.78) and heavily short volatility (skew 0.73). More-negative-than-usual aggregate skew makes the average position longer; this risky but historically profitable post-systemic-crash effect is called **global timing**. Strategy choice should reflect risks the investor is willing to bear, not solely the highest backtested Sharpe ratio.

## Smoothing, scaling, and capping

### Smoothing

The raw forecast is smoothed with an exponentially weighted moving average (EWMA). The span is set arbitrarily, without calibration, to one quarter of the estimation window:

\[
\operatorname{SmoothedSkewForecast}_{w,t}=\operatorname{EWMA}_{\text{span}=w/4}(\operatorname{RawSkewForecast}_{w,t})
\]

For \(w=60,120,240\), spans are therefore 15, 30, and 60 business days. Smoothing `skew60` reduces turnover by about two-thirds without damaging performance; the other variations see similarly large reductions. The stated optimum trading frequency is the slowest frequency before after-cost performance degrades.

### Distribution check and scalar

Pool/stack the forecast histories of all available instruments before estimating the scalar. A Gaussian distribution is ideal; absent that, avoid serious kurtosis, skew, or biases. Figure 79 (pooled `skew60`, before scaling) is non-Gaussian, slightly positively biased, fat-tailed, and mildly positively skewed, but has no suspicious lumps such as a bimodal shape. The tail risk is addressed by capping.

The required target is an average absolute forecast of 10. For `skew60`, average absolute raw-smoothed forecast is 0.30:

\[
\text{scalar}=10/0.30=33.3
\]

Forecasts are then capped at absolute 20. For `skew60`, this caps any pre-scaled forecast with absolute value above \(20/33.3=0.6\).

| Variation | Forecast scalar | Estimated forecast turnover (before the later portfolio results) |
|---|---:|---:|
| `skew60` | 33.3 | 8.5 |
| `skew120` | 37.2 | 4.0 |
| `skew240` | 39.2 | 1.9 |

Longer windows yield somewhat nicer distributions and smaller average absolute values, hence higher scalars. A seriously biased backtest forecast mean can make a scalar wrong when that bias does not recur. The chapter's illustrative warning: a Gaussian forecast with mean +5 and standard deviation 5 has average absolute value about 5.8; an inferred scalar about 1.7 would produce a future average absolute forecast about 8.5 if the bias vanished, below the target 10.

## Evaluation of individual variations

No return backtest is used to design the rule, smoothing span, or scalar—only the forecast series is used to study distribution, scale, and turnover. The final backtest is a behaviour/performance check.

### Table 108 — aggregate Jumbo portfolio, all instruments included

| Metric | Skew60 | Skew120 | Skew240 |
|---|---:|---:|---:|
| Mean annual return, gross | 14.4% | 17.9% | 17.0% |
| Mean annual return, net | 13.0% | 16.9% | 16.1% |
| Costs | −1.4% | −1.1% | −0.9% |
| Average drawdown | −26.6% | −23.4% | −36.7% |
| Standard deviation | 21.8% | 22.6% | 22.8% |
| Sharpe ratio | 0.60 | 0.75 | 0.71 |
| Turnover | 43.6 | 25.6 | 18.1 |
| Skew | −0.40 | 0.01 | −0.10 |
| Lower tail | 1.71 | 1.73 | 1.74 |
| Upper tail | 1.61 | 1.50 | 1.51 |
| Annualised alpha, gross | 8.8% | 9.5% | 7.0% |
| Annualised alpha, net | 7.4% | 8.4% | 6.1% |
| Beta | 0.38 | 0.56 | 0.66 |

Conclusions: the strategy is profitable with reasonable Sharpe ratios; costs/turnover are reasonable; volatility is on target. The strategy's deliberate purchase of negative-skew assets produces a serious negative return skew only for the short `skew60` horizon. Skew mean-reverts after a few months, leaving the slower variants near zero return skew. Aggregate-portfolio turnover is higher than individual-instrument turnover because leverage reflects cross-market diversification via the instrument diversification multiplier.

### Table 109 — correlation matrix of variation returns

|  | Skew60 | Skew120 | Skew240 |
|---|---:|---:|---:|
| Skew60 | 1.00 | 0.68 | 0.48 |
| Skew120 | 0.68 | 1.00 | 0.76 |
| Skew240 | 0.48 | 0.76 | 1.00 |

These correlations are lower than for the trend variations in Strategy 9, so the text says additional speeds such as `skew80`, `skew100`, or `skew200` might have room—but does not adopt them.

## Combined skew variations and asset-class results

The forecast diversification multiplier (FDM) is 1.18 with three skew variations, 1.10 with two, and 1.00 with one.

### Tables 110–111 — combined skew, median statistic across instruments within each asset class

| Metric | Equity | Vol | FX | Bond |
|---|---:|---:|---:|---:|
| Mean annual return | 8.9% | 3.3% | 4.2% | 7.3% |
| Costs | −0.3% | −1.9% | −0.3% | −0.4% |
| Average drawdown | −21.7% | −46.6% | −36.1% | −24.3% |
| Standard deviation | 28.7% | 32.2% | 26.9% | 24.6% |
| Sharpe ratio | 0.32 | 0.09 | 0.16 | 0.32 |
| Turnover | 7.9 | 8.3 | 8.0 | 7.7 |
| Skew | −0.44 | −2.21 | −0.25 | −0.20 |
| Lower tail | 2.81 | 2.89 | 2.72 | 2.56 |
| Upper tail | 1.98 | 1.58 | 2.26 | 2.30 |

| Metric | Metals | Energy | Ags | Global median |
|---|---:|---:|---:|---:|
| Mean annual return | 8.4% | 11.5% | 1.6% | 7.1% |
| Costs | −0.3% | −0.3% | −0.2% | −0.3% |
| Average drawdown | −70.5% | −33.7% | −58.8% | −28.4% |
| Standard deviation | 29.7% | 26.6% | 20.0% | 27.1% |
| Sharpe ratio | 0.27 | 0.43 | 0.08 | 0.26 |
| Turnover | 8.2 | 6.9 | 6.6 | 7.7 |
| Skew | 0.37 | −0.43 | −0.06 | −0.20 |
| Lower tail | 2.46 | 2.91 | 2.82 | 2.74 |
| Upper tail | 2.57 | 2.81 | 2.74 | 2.23 |

Performance is mixed but all asset classes are profitable. Volatility has the highest standard deviation and extremely negative strategy return skew, consistent with VIX and VSTOXX being almost permanently positive-skew and therefore usually shorted. This does not produce a high median SR (0.09); the chapter cautions that there are only two volatility instruments. Apart from volatility, it finds no clear cross-asset-class relation among standard deviation, skew, and SR.

## Aggregate comparison and diversification

### Table 112 — Jumbo portfolio comparison

| Metric | Long only (Strategy 4) | Multiple trend (Strategy 9) | Carry (Strategy 10) | Skew long/short (Strategy 24) |
|---|---:|---:|---:|---:|
| Mean annual return | 15.4% | 25.2% | 19.7% | 17.9% |
| Costs | −0.8% | −1.2% | −0.8% | −0.9% |
| Average drawdown | −24.7% | −11.2% | −18.6% | −28.4% |
| Standard deviation | 18.2% | 22.2% | 20.8% | 22.4% |
| Sharpe ratio | 0.85 | 1.14 | 0.94 | 0.80 |
| Turnover | 20.7 | 62.9 | 19.2 | 23.9 |
| Skew | −0.04 | 0.98 | 0.41 | 0.14 |
| Lower tail | 1.44 | 1.99 | 1.57 | 1.72 |
| Upper tail | 1.24 | 1.81 | 1.49 | 1.52 |
| Alpha | 0 | 18.8% | 19.1% | 8.5% |
| Beta | 1.0 | 0.43 | 0.06 | 0.62 |

Skew is inferior to trend and carry and even to long only in this aggregate comparison, despite similar individual-instrument performance to trend. Diversification improves the median individual skew SR from 0.26 to 0.80—a roughly threefold improvement—but the text says trend's improvement is almost fivefold. Figure 80 shows skew sharing long only's early-1980s drawdown, outperforming all peers in the early-2000s “great moderation,” then suffering a small setback and continuing to profit until the COVID-19 market shock in early 2020.

## Combination with carry and trend

The combined skew strategy has correlation around 0.14 with both Strategy 9 trend and Strategy 10 carry, offering substantial diversification. The chapter assigns skew to the **convergent** group (like carry/value), despite no clear correlation-based answer, because negative-skew assets tend to do badly in market crises. It gives skew a 20% forecast weight: half of the customary 40% allocation to convergent strategies, with carry taking the remainder.

### Table 113 — aggregate Jumbo portfolio results

*The source caption says “carry, trend and acceleration,” while the table columns and surrounding text compare skew, carry-and-trend, and carry-trend-skew; this reference preserves the data and flags the caption as an apparent source inconsistency.*

| Metric | Skew | Carry and trend (Strategy 11) | Carry, trend and skew |
|---|---:|---:|---:|
| Mean annual return | 17.9% | 26.5% | 28.9% |
| Costs | −0.9% | −1.1% | −1.2% |
| Average drawdown | −28.4% | −8.9% | −8.4% |
| Standard deviation | 22.4% | 20.9% | 21.0% |
| Sharpe ratio | 0.80 | 1.27 | 1.38 |
| Turnover | 23.9 | 46.5 | 56.1 |
| Skew | 0.14 | 0.76 | 0.62 |
| Lower tail | 1.72 | 1.86 | 1.85 |
| Upper tail | 1.52 | 1.75 | 1.67 |
| Alpha | 8.5% | 22.3% | 22.5% |
| Beta | 0.62 | 0.30 | 0.44 |

Adding skew materially improves return and Sharpe ratio (1.27 to 1.38) and slightly improves average drawdown (−8.9% to −8.4%). The alpha improvement is modest because of extra long bias; the positive skew of monthly returns associated with a trend-dominated portfolio is reduced somewhat.

## Trading plan

- **Strategy:** take variable-risk long or short positions in one or more instruments, using a skew forecast; go long negative-skew assets and short positive-skew assets.
- **Eligible instruments:** any that pass minimum capital, liquidity, and cost thresholds.
- **Rule selection by expected turnover:** 8.5 for `skew60`, 4.0 for `skew120`, and 1.9 for `skew240`.
- **Forecast calculation:** use the raw and EWMA-smoothed equations above.
- **Scalars:** `skew60` 33.3; `skew120` 37.2; `skew240` 39.2.
- **Forecast diversification multipliers:** three skew variations 1.18; two 1.10; one 1.00.
- **All remaining stages:** identical to Strategy 9, according to the source.

## Warnings and edge cases

- Standard rolling skew is outlier-sensitive; a single extreme return entering or leaving the window can move it sharply.
- Windows shorter than three months were deliberately avoided; longer than a year risks staleness.
- Optimising horizons/spans by backtest invites overfitting.
- Scaling on a biased historical forecast distribution can miss the intended out-of-sample average absolute forecast.
- A relative strategy's expected zero mean position need not occur exactly, particularly with a short, trending history.
- Volatility conclusions are weak because the Jumbo portfolio has only VIX and VSTOXX.
- Negative-skew holdings can perform badly in crises, which is central to the choice to treat skew as convergent.

## Connections to other chapters

- **Part One, Tables 3–4 (pp. 49–50):** cross-asset-class skew patterns and their relationship with performance.
- **Strategy 1:** tail measures as a more robust alternative to standard skew.
- **Strategy 7:** definition of forecast as a prediction for risk-adjusted prices.
- **Strategy 9:** EWMAC/multiple trend, smoothing comparison, standard post-forecast stages, and benchmark portfolio.
- **Strategy 10:** carry; together with trend it provides the benchmark for diversification.
- **Strategy 11:** carry-and-trend benchmark used for the combined allocation.
- **Strategy 18:** aggregated asset-class example.
- **Strategies 19–20:** asset-class cross-sectional trend and carry.
- **Strategy 22:** value, an example of a weak standalone strategy that can improve a portfolio through diversification.
- **Part Five:** distinguishes cross-market forecasting from relative-value trading.

## Glossary

- **Absolute forecast** — trades the sign of the forecast directly.
- **Asset-class cross-sectional forecast** — compares an instrument's forecast with the current average for its asset class.
- **Back-adjusted price** — price series used here to calculate return differences; return denominator remains the actively traded futures price.
- **Beta** — reported portfolio sensitivity metric; the chapter uses it in comparing strategy variants.
- **Convergent strategy** — category including carry/value; skew is assigned here because negative-skew assets tend to fare badly in crises.
- **Cross-sectional forecast** — compares an instrument with all instruments' current average forecast.
- **EWMA** — exponentially weighted moving average used to slow the raw forecast.
- **FDM** — forecast diversification multiplier applied when combining forecast variations.
- **Global timing** — return source from changing aggregate skew levels, retained by absolute skew.
- **Risk premium** — compensation for bearing an undesired risk.
- **Sharpe ratio (SR)** — risk-adjusted performance measure used throughout the results.
- **Skew** — standardized third-moment statistic; here the signal is its negative.
- **Turnover** — trading-rate measure used to determine which rule speeds are economical.
