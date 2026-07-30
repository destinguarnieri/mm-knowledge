# Strategy Fourteen: Spot Trend

## Purpose and central argument

Back-adjusted futures prices include returns from both **spot-price changes** and **carry**. Consequently, an EWMAC trend rule run on an adjusted price can be responding to either source. This chapter tests whether extracting carry first—then trend-following only the resulting **synthetic spot** price—produces a cleaner, less carry-correlated trend signal.

The chapter's practical strategy is a variation of any EWMAC-based strategy: replace the back-adjusted price input with synthetic spot. On its own, synthetic-spot trend performs worse than adjusted-price trend, especially at slow speeds and in high-carry asset classes. But when it is blended with a carry strategy, a 40% synthetic-spot-trend / 60% carry mix offers a different trade-off: modestly lower Sharpe ratio than the adjusted-price carry/trend blend, but improved alpha, beta, costs, skew, and tails in the reported aggregate results.

## Key ideas

- **Adjusted price / back-adjusted price:** a total-return price series. Its changes contain both spot and carry returns.
- **Carry:** the return attributable to carry; the required input is the *annualised raw carry* from strategy ten, expressed as expected price points of carry per year.
- **Synthetic spot price:** a futures-price-derived series whose carry return has been deducted, intended to reflect only spot-price changes. It requires no separate actual-spot data feed.
- **EWMAC:** the chapter assumes the existing EWMAC trend rules; synthetic spot replaces their price input, not the trend-rule construction itself.
- **Double counting concern:** in a combined carry-and-trend strategy, adjusted-price trend can also be following trends created by carry. A long carry forecast and a long adjusted-price trend forecast after a carry-driven rally may therefore overlap economically.
- **Pure versus impure trend:** the author calls synthetic-spot trend “purer,” since adjusted-price trend is contaminated by carry. The chapter finds that purity is not automatically superior statistically.

## Constructing synthetic spot

The source states the return decomposition:

\[
\text{Adjusted price change}_{t,t-1}
= \text{Spot price change}_{t,t-1} + \text{Carry accrued}_{t,t-1}
\]

\[
\text{Carry accrued}_{t,t-1}
= \text{Annualised raw carry} \times \text{Year fraction}(t,t-1)
\]

For adjusted price \(P_t\) and synthetic spot \(S_t\):

\[
P_t-P_{t-1}=S_t-S_{t-1}+\text{Carry accrued}_{t,t-1}
\]

\[
\boxed{S_t=S_{t-1}+P_t-P_{t-1}-\left[\text{Annualised raw carry}\times\text{Year fraction}(t,t-1)\right]}
\]

### Symbols, units, and conditions

| Item | Meaning / unit |
|---|---|
| \(t, t-1\) | Current and immediately prior observation times. |
| \(P_t\), \(P_{t-1}\) | Adjusted price at the two times; price points. The prose initially refers to adjusted price as \(P_t\), although elsewhere it calls it back-adjusted price. |
| \(S_t\), \(S_{t-1}\) | Synthetic spot price at the two times; price points. |
| Annualised raw carry | Expected carry in one year; number of price points per year. It is calculated in strategy ten. |
| Year fraction \((t,t-1)\) | Fraction of a year elapsed between observations; dimensionless. For daily data indexed to business days, approximately 0.00391. |
| Carry accrued \(_{t,t-1}\) | Carry allocated to the interval; price points. |

### Implementation procedure

1. Obtain the instrument's adjusted-price series and its annualised raw carry.
2. For each observation interval, calculate the year fraction.
3. Calculate carry accrued for the interval as annualised raw carry × year fraction.
4. Update synthetic spot recursively using the boxed equation above.
5. Feed the synthetic-spot series, rather than the back-adjusted-price series, into every EWMAC rule being modified.

The initial level is arbitrary. The author uses \(S_0=A_0\), where \(A_0\) is the initial back-adjusted price. This choice does not affect forecasts or the performance of a trading rule using synthetic spot; equivalently, one could anchor the final value to the final adjusted price or use any arbitrary initial/final level. Only the path of changes matters to the stated use.

## Figures

### Figure 58 — US 10-year bond future

**Caption:** “Cumulative returns from carry, adjusted price and synthetic spot for US 10-year bond future.”

The plot shows cumulative carry, adjusted price, and synthetic spot from roughly the early 1980s through 2022. The adjusted-price rise is much clearer than the synthetic-spot path; the source says about half the bond-future return was due to carry. Thus, removing carry yields a murkier spot series, likely smaller trend positions, and fewer clear trends for EWMAC to capture. The unusual upward carry tick in late 1999 is attributed to a change in the reference bond's coupon rate (footnote 178).

### Figure 59 — Trend speed comparison

**Caption:** “Sharpe ratio (y-axis) for combined trend strategy using adjusted versus synthetic prices, over different speed trend filters (x-axis).”

The chart compares adjusted and synthetic inputs across EWMAC2 through EWMAC64, moving left-to-right from faster to slower filters. Synthetic spot is worse at every speed, and the performance gap expands for slower filters. For EWMAC64, the source says about one-third of the Sharpe ratio is lost on switching to synthetic spot. The corresponding beta versus the long-only benchmark (strategy four) is also lower for synthetic spot; at EWMAC64 it is 0.46 versus 0.53 for adjusted prices.

## Asset-class evidence

Tables 61 and 62 report median-instrument carry characteristics and multiple-trend results. Trend results average across instruments within each asset class; the selected rules are a cost-dependent subset of EWMAC2–EWMAC64. “Back-adjusted trend” corresponds to the prior multiple-trend strategy (strategy nine); the final three rows replace its input with synthetic spot.

### Table 61 — Financial asset classes

| Measure | Equity | Vol | FX | Bond |
|---|---:|---:|---:|---:|
| Median absolute carry | 0.12 | 0.67 | 0.21 | 0.41 |
| Sharpe ratio of carry | 0.40 | 0.59 | 0.30 | 0.48 |
| **Back-adjusted trend: mean annual return** | 0.7% | 13.3% | 5.2% | 9.5% |
| Back-adjusted trend: standard deviation | 22.1% | 25.9% | 22.8% | 23.1% |
| Back-adjusted trend: Sharpe ratio | 0.03 | 0.51 | 0.19 | 0.43 |
| **Synthetic spot trend: mean annual return** | 1.1% | 2.4% | 0.0% | 5.4% |
| Synthetic spot trend: standard deviation | 15.8% | 15.7% | 17.6% | 19.5% |
| Synthetic spot trend: Sharpe ratio | 0.07 | 0.15 | 0.0 | 0.28 |

### Table 62 — Commodity asset classes

| Measure | Metals | Energy | Ags | Median |
|---|---:|---:|---:|---:|
| Median absolute carry | 0.15 | 0.42 | 0.45 | 0.24 |
| Sharpe ratio of carry | 0.25 | 0.20 | 0.14 | 0.28 |
| **Back-adjusted trend: mean annual return** | 8.9% | 8.9% | 5.4% | 5.2% |
| Back-adjusted trend: standard deviation | 24.3% | 25.5% | 22.8% | 23.0% |
| Back-adjusted trend: Sharpe ratio | 0.37 | 0.39 | 0.24 | 0.23 |
| **Synthetic spot trend: mean annual return** | 9.8% | 6.3% | 3.9% | 3.0% |
| Synthetic spot trend: standard deviation | 24.7% | 23.1% | 22.4% | 18.9% |
| Synthetic spot trend: Sharpe ratio | 0.42 | 0.25 | 0.17 | 0.15 |

**Interpretation:** performance worsens in almost every class when adjusted price is replaced with spot. High-carry bonds and volatility are particularly weak; low-carry equities and metals improve slightly. Standard deviation also falls except for metals, consistent with carry removal making trends murkier, forecasts smaller, and return volatility lower. Footnote 179 notes that changing EWMA forecast scalars could compensate for this, but does not recommend it.

## Combining spot trend with carry

Synthetic-spot trend alone is inferior, so the relevant comparison includes carry. Strategy eleven originally uses 60% adjusted-price trend and 40% carry. Because synthetic-spot trend has lower Sharpe ratio and is less correlated with carry rules, the chapter argues for a higher carry allocation.

### Table 63 — 50–100% allocation to trend

Percentages are the allocation to trend; the residual is carry.

| Input / metric | 100% | 90% | 80% | 70% | 60% | 50% |
|---|---:|---:|---:|---:|---:|---:|
| **Carry + synthetic spot trend: Sharpe ratio** | 0.76 | 0.86 | 0.96 | 1.04 | 1.12 | 1.16 |
| Alpha | 10.8 | 12.8 | 14.9 | 17.1 | 19.0 | 20.4 |
| Beta | 0.36 | 0.36 | 0.35 | 0.34 | 0.31 | 0.28 |
| Monthly skew | 1.22 | 1.21 | 1.19 | 1.14 | 1.07 | 0.99 |
| **Carry + back-adjusted trend: Sharpe ratio** | 1.14 | 1.19 | 1.24 | 1.26 | 1.27 | 1.27 |
| Alpha | 18.8% | 19.1% | 20.4% | 21.5% | 22.3% | 22.9% |
| Beta | 0.43 | 0.40 | 0.39 | 0.37 | 0.30 | 0.30 |
| Monthly skew | 0.98 | 0.94 | 0.88 | 0.83 | 0.76 | 0.72 |

### Table 64 — 0–50% allocation to trend

| Input / metric | 50% | 40% | 30% | 20% | 10% | 0% |
|---|---:|---:|---:|---:|---:|---:|
| **Carry + synthetic spot trend: Sharpe ratio** | 1.16 | 1.16 | 1.12 | 1.07 | 1.00 | 0.94 |
| Alpha | 20.4 | 21.1% | 22.2% | 20.8% | 20.1% | 19.1% |
| Beta | 0.28 | 0.23 | 0.18 | 0.14 | 0.10 | 0.06 |
| Monthly skew | 0.99 | 0.88 | 0.77 | 0.65 | 0.53 | 0.41 |
| **Carry + back-adjusted trend: Sharpe ratio** | 1.26 | 1.25 | 1.20 | 1.12 | 1.03 | 0.94 |
| Alpha | 22.9% | 22.87% | 22.4% | 21.6% | 20.5% | 19.1% |
| Beta | 0.30 | 0.25 | 0.20 | 0.15 | 0.10 | 0.06 |
| Monthly skew | 0.72 | 0.68 | 0.63 | 0.57 | 0.50 | 0.41 |

**Source-format note:** Table 63 shows synthetic-spot alpha values without percent signs; Table 64 similarly shows `20.4` without a percent sign at 50% trend while adjacent alpha cells do display `%`. The source does not explain this inconsistency, so the values above are transcribed as displayed rather than normalized.

The stated choice is a **mirror-image 40% synthetic-spot trend / 60% carry** allocation: it produces the highest reported synthetic-spot-combination SR (tied at 1.16 with 50% trend) and one of the highest alphas.

## Aggregate portfolio comparison

Table 65 compares the aggregate “Jumbo” portfolio across trend-only and carry-plus-trend variants.

| Metric | Strategy 9: trend, adjusted | Strategy 14: trend, spot | Strategy 11: carry + trend (adjusted), 60:40 | Strategy 14: carry + trend (spot), 40:60 |
|---|---:|---:|---:|---:|
| Mean annual return | 25.2% | 15.3% | 26.5% | 24.1% |
| Costs | −1.2% | −1.3% | −1.1% | −1.0% |
| Average drawdown | −11.2% | −14.4% | −8.9% | −9.5% |
| Standard deviation | 22.2% | 20.0% | 20.9% | 20.0% |
| Sharpe ratio | 1.14 | 0.77 | 1.27 | 1.20 |
| Turnover | 62.9 | 65.4 | 46.5 | 33.7 |
| Skew | 0.98 | 1.21 | 0.76 | 0.94 |
| Lower tail | 1.99 | 2.10 | 1.86 | 1.78 |
| Upper tail | 1.81 | 2.06 | 1.75 | 1.78 |
| Alpha | 18.8% | 11.5% | 22.3% | 22.6% |
| Beta | 0.43 | 0.34 | 0.30 | 0.18 |

For trend alone, synthetic spot has worse performance and lower beta, but higher positive skew: removing carry makes returns more like “pure” trend following. With carry included, the spot version has a modest SR reduction (1.20 vs. 1.27), while alpha, beta, costs, skew, and tails are described as improved. The source uses these results as an argument that the modification may be worthwhile, rather than as a definitive statistical win.

## Trading plan

| Component | Instruction |
|---|---|
| Strategy | Modify any strategy using EWMAC trading rules to use synthetic spot instead of adjusted prices. |
| Input price | Replace the back-adjusted price input to EWMAC with synthetic spot calculated by the recursive equation above. |
| Forecast weights | If allocating to both carry and trend, reduce trend from 60% to 40%; increase carry from 40% to 60%. |

The text immediately preceding the plan says “the adjustments in strategy thirteen” can be applied to any strategy with EWMAC rules. In the context of this chapter and the plan image, this appears inconsistent; the source does not clarify it.

## Assumptions, limitations, and warnings

- Synthetic spot is an accounting construction from futures prices, not observed cash/actual spot; it depends on the annualised raw carry input from strategy ten.
- The method assumes an appropriate year fraction for each observation interval. The daily-business-day approximation is 0.00391.
- Faster trend filters should be less affected; slow filters can piggyback on slow price components largely caused by carry, particularly in bonds and volatility.
- Applying asset-class-specific carry/trend weights might improve results, but the author opposes it as usually overfitted.
- Changing EWMA forecast scalars to counter smaller spot-trend forecasts is possible but explicitly not recommended (footnote 179).
- Adjusted-price trend has a “natural stop loss” because adjusted price reflects recent profitability. Spot-price trend instead gives a more explicit accounting of whether returns are from spot or carry. The chapter frames this as a philosophical as well as statistical trade-off.

## Connections to other chapters

- **Strategy 1:** establishes that back-adjusted prices contain carry and spot returns.
- **Strategy 4:** provides the long-only benchmark used for beta comparisons.
- **Strategy 9 (multiple trend):** its back-adjusted trend results form the baseline; its rules are EWMAC2–EWMAC64, selected by instrument cost.
- **Strategy 10:** defines/calculates annualised raw carry and discusses data availability for actual spot.
- **Strategy 11:** the baseline carry-and-trend blend is 60% trend / 40% carry; this chapter proposes the 40% spot-trend / 60% carry alternative.
- **Strategy 13:** the final prose references “adjustments in strategy thirteen,” but the intended connection is unclear from this chapter alone.

## Glossary

- **Adjusted price / back-adjusted price** — total-return futures price series incorporating spot and carry.
- **Annualised raw carry** — expected number of price points of carry over one year.
- **Carry accrued** — interval carry: annualised raw carry multiplied by year fraction.
- **Carry strategy** — trading rules intended to capture carry.
- **EWMAC** — the chapter's existing trend-following rule family; examples span EWMAC2 to EWMAC64.
- **Forecast** — trading-rule output; synthetic spot is used as its price input in this strategy.
- **Synthetic spot** — futures-only, carry-extracted price series designed to represent spot-price changes.
- **Year fraction** — elapsed interval expressed as a fraction of a year.

## Conclusions

1. Synthetic spot separates carry from adjusted-price changes with a simple recursive calculation and no extra data feed.
2. It produces a more isolated trend signal but weaker standalone trend performance, especially for slow filters and high-carry asset classes.
3. It reduces beta and can improve positive skew by reducing carry's influence on trend returns.
4. In a carry-plus-trend system, the chapter's selected allocation is 40% synthetic spot trend and 60% carry.
5. The chief decision is not only performance-based: adjusted-price trend embeds realised profitability in the price path, while synthetic spot makes return attribution between spot and carry more transparent.
