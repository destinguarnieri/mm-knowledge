# Strategy Sixteen: Trend and Carry Allocation

## Purpose and central argument

Strategy Sixteen modifies a strategy that trades both trend and carry by changing their **top-level forecast weights** instead of always using the fixed 60% trend / 40% carry allocation adopted in Strategy Eleven. The chapter investigates two variants:

1. **Dynamic allocation through relative performance.** Increase the trend weight after trend has outperformed carry over the prior year; increase carry after trend has underperformed.
2. **Allocation by asset class.** Give equities a much lower trend weight (10%) and higher carry weight (90%), while retaining 60% trend / 40% carry for every other asset class.

The author finds modest backtested improvements in both cases but stresses the weak evidence for aggressive factor timing, the risk of overfitting, and insufficient data for instrument-specific allocations.

## Scope and prerequisites

- Applies to **any strategy with both trend and carry trading rules**.
- The baseline is Strategy Eleven: divergent trend forecasts at 60% and convergent carry forecasts at 40%.
- Performance discussion uses the **Jumbo portfolio** and the historical backtest presented in the book.
- This chapter does not replace the underlying trend or carry rules. It changes only their relative, top-level forecast weights.

## Key concepts

### Forecast weights

Forecast weights allocate risk/significance between trading-rule forecasts. Here they allocate between the trend and carry sources of return:

- `W_t`: top-level weight on divergent trend forecasts at time `t`.
- `1 - W_t`: top-level weight on convergent carry forecasts at time `t`.
- A fixed baseline is `W_t = 0.60`; the dynamic version varies daily.

### Return auto-correlation

Auto-correlation is the correlation between a strategy's return and its prior-period return—effectively account-curve momentum. It can be measured at daily, weekly, monthly, and longer frequencies.

- **Positive auto-correlation:** recent good performance implies increasing allocation; recent poor performance implies reducing it.
- **Negative auto-correlation:** implies taking profits after good performance, but increasing allocation after losses (“catching a falling knife”).
- For switching between two strategies, their **relative performance** is the relevant return series.

The chapter notes research finding weak negative auto-correlation for returns of trend-following funds, but says this may reflect performance-fee mechanics rather than the underlying trend strategy. Fees subtract from positive months when a fund makes a new high-water mark, while drawdown months are not charged; this can make positive months look worse and negative months relatively better.

## Evidence motivating the dynamic allocation

### Figure 65 — annual carry and trend performance

Figure 65 plots annual Jumbo-portfolio performance for multiple trend (labelled “Momentum” in the graphic) and carry from 1990–2022. Both have highly variable, sometimes opposing yearly results. The chapter highlights:

- 2017: trend was bad while carry was profitable.
- 2018: carry was the laggard, so a 100% trend allocation would have been attractive in hindsight.

The figure motivates the question, not a claim that these switches were knowable in advance.

### Figure 66 — auto-correlation by return horizon

Figure 66 compares auto-correlations for momentum/trend, carry, and their relative return using **non-overlapping** periods. Non-overlapping periods make each estimate more reliable, but reduce observations and hence statistical significance.

- Short-horizon values are mostly not especially significant and would be expensive to trade because frequent switches add turnover.
- Six-month results become more interesting.
- Annual auto-correlations are significantly positive and have the largest useful magnitude.
- Five-year results are mixed and unreliable: only eight non-overlapping five-year observations exist.

The author therefore chooses a one-year lookback: a practical balance between trading cost at shorter horizons and weak/mixed evidence at longer horizons.

## Dynamic relative-performance allocation

### Formulas

**1. Daily relative performance**

\[
R_t = T_t - C_t
\]

| Symbol | Definition | Units / domain |
|---|---|---|
| `R_t` | Relative daily performance of trend versus carry at day `t` | Percentage of capital per day |
| `T_t` | Daily performance of the spot trend strategy | Percentage of capital per day |
| `C_t` | Daily performance of the carry strategy | Percentage of capital per day |
| `t` | Trading-day index | Daily |

Positive `R_t` means trend beat carry that day; negative `R_t` means carry beat trend.

**2. Rolling one-year relative performance, scaled by risk target**

\[
RP_t = \frac{R_t + R_{t-1} + R_{t-2} + \dots + R_{t-255}}{\tau}
\]

| Symbol | Definition | Units / conditions |
|---|---|---|
| `RP_t` | Rolling 12-month trend-minus-carry performance, normalized by the volatility target | Dimensionless; uses 256 business days |
| `R_{t-k}` | Relative daily performance `k` business days before `t` | Percentage of capital per day |
| `\tau` | Volatility target | 20% in this book |

Thus `RP_t = 1` corresponds to trend outperforming carry by one volatility-target unit (20% under the book’s target) over the last 12 months; `RP_t = -1` corresponds to a 20% underperformance.

**3. Trend-weighting function**

\[
W_t = \operatorname{EWMA}_{\text{span}=30}\!\left(\min\left(1,\max\left(0,\,0.5 + \frac{RP_t}{2}\right)\right)\right)
\]

| Symbol / operator | Definition | Conditions |
|---|---|---|
| `W_t` | Smoothed top-level forecast weight allocated to trend | Bounded from 0 to 1 |
| `0.5 + RP_t / 2` | Raw linear mapping from normalized relative performance to trend weight | 0.5 when `RP_t = 0` |
| `max(0, ·)` / `min(1, ·)` | Floor and cap the raw weight | Prevent weights below 0 or above 1 |
| `EWMA_span=30(·)` | Exponentially weighted moving average with 30-day span | Smooths noise and reduces trading costs |

The remaining carry weight is `1 - W_t`.

### Boundary cases and interpretation

| Condition | Raw allocation before smoothing |
|---|---|
| `RP_t = 0` | 50% trend / 50% carry |
| `RP_t > 0` | Trend weight moves toward 1 |
| `RP_t < 0` | Trend weight moves toward 0; carry weight rises |
| `RP_t >= 1` | 100% trend / 0% carry |
| `RP_t <= -1` | 0% trend / 100% carry |

The 30-day EWMA means the traded weight changes daily but is moderated by both smoothing and the full-year performance lookback. Figure 67 plots the normalized rolling relative performance, showing long swings above and below zero. Figure 68 plots the resulting trend weight, which often approaches the 0 or 1 bounds when relative performance is extreme.

### Procedure

1. Obtain daily percentage-of-capital returns for the spot trend and carry strategies, `T_t` and `C_t`.
2. Calculate daily relative return `R_t = T_t - C_t`.
3. Sum the most recent 256 business-day values of `R` and divide by the volatility target `τ` to obtain `RP_t`.
4. Map `RP_t` to the raw trend weight `0.5 + RP_t/2`.
5. Cap/floor it to `[0, 1]`.
6. Apply a 30-day-span EWMA to form `W_t`.
7. Allocate `W_t` to divergent trend forecasts and `1 - W_t` to convergent carry forecasts.

## Backtest: fixed versus variable allocation (Table 67)

| Metric | Strategy Eleven: 40% carry / 60% trend | Strategy Sixteen: variable allocation |
|---|---:|---:|
| Mean annual return | 26.5% | 28.1% |
| Average drawdown | −8.9% | −10.1% |
| Standard deviation | 20.9% | 21.0% |
| Sharpe ratio | 1.27 | 1.33 |
| Skew | 0.76 | 0.89 |
| Lower tail | 1.86 | 1.84 |
| Upper tail | 1.75 | 1.74 |
| Alpha | 22.3% | 20.7% |
| Beta | 0.30 | 0.46 |

The author calls the results “okay”: most metrics improve by small but statistically significant amounts, except drawdown and alpha. The dynamic strategy’s average trend allocation is just under 50%, versus 60% in Strategy Eleven. This is surprising because the standalone trend strategy has better Sharpe ratio and skew than carry; greater average carry exposure would normally be expected to make the combination worse.

Altering the function to restore an average 60% trend exposure might improve the reported results, but the author considers that arguably overfitting.

## Cautions on factor timing

- Full de-allocation from one factor to the other can feel risky. A modified scheme could constrain trend to 20%–80%, but that would move the strategy closer to Strategy Eleven and reduce potential benefit.
- The chapter is sceptical of other factor-timing approaches. It cites Cliff Asness’s warning that aggressive factor timing is hazardous and that investors are generally better served by diversification across factors they believe in.
- Forecast-driven trading already has an **implicit timing effect**: weak forecasts reduce a strategy’s effective allocation, strong forecasts increase it. Additional factor timing is difficult to improve.
- Account-curve trend following is another name for expecting positive strategy performance to persist. The author explicitly does not favor complex technical indicators for setting strategy leverage in this context.

## Allocation by asset class

The second question is whether different asset classes warrant distinct carry/trend mixes. Tables 68 and 69 compare median instrument performance for the carry strategy (Strategy Ten) and multiple trend strategy (Strategy Nine). The comparison statistic is `SR_trend - SR_carry`; relative rather than standalone performance is what matters for allocating between them.

### Table 68 — financial asset classes

| Strategy / metric | Equity | Vol | FX | Bond |
|---|---:|---:|---:|---:|
| Carry: mean annual return | 3.1% | 21.4% | 5.1% | 13.3% |
| Carry: standard deviation | 9.9% | 36.0% | 18.3% | 27.5% |
| Carry: Sharpe ratio | 0.40 | 0.59 | 0.30 | 0.48 |
| Trend: mean annual return | 0.7% | 13.3% | 5.2% | 9.5% |
| Trend: standard deviation | 22.1% | 25.9% | 22.8% | 23.1% |
| Trend: Sharpe ratio | 0.03 | 0.51 | 0.19 | 0.43 |
| `SR_trend - SR_carry` | −0.47 | −0.08 | −0.11 | −0.05 |

### Table 69 — commodity asset classes and median

| Strategy / metric | Metals | Energy | Ags | Median |
|---|---:|---:|---:|---:|
| Carry: mean annual return | 3.5% | 5.0% | 3.5% | 4.4% |
| Carry: standard deviation | 16.7% | 28.2% | 29.3% | 19.8% |
| Carry: Sharpe ratio | 0.25 | 0.20 | 0.14 | 0.28 |
| Trend: mean annual return | 8.9% | 8.9% | 5.4% | 5.2% |
| Trend: standard deviation | 24.3% | 25.5% | 22.8% | 23.0% |
| Trend: Sharpe ratio | 0.37 | 0.39 | 0.24 | 0.23 |
| `SR_trend - SR_carry` | 0.12 | 0.19 | 0.10 | −0.05 |

### Interpretation and confounds

Ordered from best for trend to worst by relative Sharpe ratio: **energy, metals, agricultural markets, bonds, volatility, FX, equities**. The apparent pattern—commodities favor trend while financial markets favor carry—could be attributed to market efficiency or fewer commercial hedgers in financial markets, but the author rejects this inference as a mirage.

The confound is **unequal history length**:

- Commodity instruments have longer histories, including pre-1990 data when trend was especially strong and carry less compelling.
- Financial instruments tend to have shorter histories concentrated in the later period when trend was relatively weaker.
- Rerunning the backtest only from the mid-1990s removes this asset-class pattern. This shorter sample is almost exactly half the full backtest.

The persistent outlier is equity trend: its relative Sharpe is the only value significantly different from zero. Equity carry is decent, while equity trend has approximately zero Sharpe. A possible explanation is that cheap equity instruments permit more fast trend rules, and the fastest moving averages perform relatively poorly; however, the author finds equity trend poor at every speed and worse than every other asset class regardless of speed. After costs, equity-trend Sharpe ranges from −0.08 for EWMAC2 to +0.08 for EWMAC64.

## Equity-specific allocation rule

The resulting asset-class rule is deliberately narrow:

- **Equities:** 10% trend, 90% carry.
- **Other asset classes:** retain 60% trend, 40% carry.

The author does not reduce the equity trend weight to zero because concentrating all risk in a single basket is usually unwise even when its backtested Sharpe is superior.

## Backtest: lower trend weight in equities (Table 70)

| Metric | Strategy Eleven: 40% carry / 60% trend | Strategy Sixteen: equities 90% carry / 10% trend; other classes unchanged |
|---|---:|---:|
| Mean annual return | 26.5% | 26.5% |
| Costs | −1.1% | −1.0% |
| Average drawdown | −8.9% | −8.0% |
| Standard deviation | 20.9% | 19.9% |
| Sharpe ratio | 1.27 | 1.33 |
| Turnover | 46.5 | 36.8 |
| Skew | 0.76 | 0.86 |
| Lower tail | 1.86 | 1.83 |
| Upper tail | 1.75 | 1.87 |
| Alpha | 22.3% | 22.5% |
| Beta | 0.30 | 0.28 |

Only one of seven asset classes changes, so the chapter expects and observes a modest whole-portfolio effect. Turnover improves substantially because the portfolio has less exposure to fast trend rules, which were mostly tradable in cheap equity instruments. The chapter explicitly says there is insufficient data to reach meaningful conclusions about allocations for individual instruments within an asset class.

## Trading plan

### Strategy

Modify any strategy that trades trend and carry so its top-level forecast weights are not permanently 60% trend and 40% carry.

### Option A — recent relative performance

Use the dynamic procedure above to modify the trend/carry weight according to recent relative performance. Trend receives `W_t`; carry receives `1-W_t`.

### Option B — asset class

For equities, reduce the trend top-level forecast weight to 10% and increase carry to 90%. Maintain 60% trend / 40% carry in other asset classes.

## Practical constraints, warnings, and edge cases

- Do not infer real-time predictability from ex post annual winners/losers in Figure 65.
- A weekly or similarly short switching horizon can have high turnover and transaction costs.
- Non-overlapping long-horizon auto-correlation estimates have few observations; five-year estimates here are not likely statistically significant.
- The dynamic weighting function saturates at 0% or 100%; if that concentration is unacceptable, bounds such as 20%–80% are possible, at the cost of smaller differentiation from the fixed baseline.
- Matching the dynamic rule’s average allocation to a desired 60% trend after observing results is a potential overfitting step.
- Do not treat raw cross-asset-class Sharpe comparisons as structural evidence without controlling for sample period/history length.
- There is not enough data in the chapter to support individualized allocation rules within asset classes.
- All results are presented as backtests; no forward-performance claim is made.

## Connections to other chapters

- **Strategy Nine:** multiple trend; supplies the trend performance comparisons.
- **Strategy Ten:** carry; supplies the carry performance comparisons.
- **Strategy Eleven:** fixed 60% trend / 40% carry baseline used for every comparison.
- **Tables 30 and 31 (pages 178–179):** fastest moving averages do relatively poorly; considered, then rejected as the complete explanation for weak equity trend.
- **Figure 45 (page 236):** supports the claim that earlier history favored trend more and carry less, explaining the unequal-history confound.
- The chapter follows several prior chapters that attempted to improve the basic trend and carry strategies introduced in Part One.

## Glossary

- **Alpha:** reported portfolio performance measure relative to the chapter’s benchmark/model; definition not restated here.
- **Auto-correlation:** correlation of a return with its prior-period return.
- **Beta:** reported portfolio market-exposure/sensitivity measure; definition not restated here.
- **Carry:** a convergent trading forecast/strategy used with trend in this book.
- **Divergent trend forecast:** the trend forecast category receiving `W_t`.
- **EWMA:** exponentially weighted moving average; here a 30-day-span smoother.
- **Forecast weight:** top-level allocation assigned to a forecast type.
- **Jumbo portfolio:** the book’s aggregate portfolio used for the reported results.
- **Lower tail / upper tail:** reported tail measures; definitions are not restated in this chapter.
- **Relative performance:** trend return minus carry return.
- **Sharpe ratio (SR):** risk-adjusted performance statistic used for cross-strategy and asset-class comparisons.
- **Spot trend strategy:** the trend strategy whose daily percentage-of-capital performance is `T_t`.
- **Trend following the account curve:** allocating more after strong strategy performance because it is expected to persist.
- **Turnover:** reported trading-activity metric; its precise unit/definition is not restated in this chapter.
- **Volatility target (`τ`):** target annual risk used to normalize performance; 20% in this book.

## Chapter takeaway

The chapter provides a concrete, bounded and smoothed one-year relative-performance rule for switching forecast weight between trend and carry, plus a simpler equity-specific allocation adjustment. Both improve selected backtest metrics modestly, but the author’s main practical message is cautious: factor timing is hard, underlying forecasts already time exposure implicitly, historical differences can be sample artifacts, and diversification should not be abandoned on limited evidence.
