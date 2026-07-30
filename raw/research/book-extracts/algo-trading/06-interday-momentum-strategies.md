---
title: "Interday Momentum Strategies"
chapter: 6
source: "Algorithmic Trading: Winning Strategies and Their Rationale"
status: "extracted"
---

# Chapter 6: Interday Momentum Strategies

## Chapter Overview

The chapter studies multi-day momentum arising from persistent futures roll returns, slow information diffusion, forced fund trading, and high-frequency-trader manipulation. It distinguishes time-series momentum (a series’ past return predicts its own future return) from cross-sectional momentum (relative winners continue to outperform). It also emphasizes a recently discovered momentum weakness and the strategy family’s different risk profile from mean reversion. **Source: pp. 133–134, 152–154**

## Learning Objectives

* Test time-series momentum without overlapping observations. **Source: pp. 134–137**
* Construct time-series, roll-return extraction, and cross-sectional momentum strategies. **Source: pp. 137–149**
* Recognize data-snooping, financing, execution-timing, crowding, and crash-risk limitations. **Source: pp. 139–154**

## Key Concepts

### Causes of momentum

The author lists four causes: persistent sign of futures roll returns; slow diffusion/analysis/acceptance of information; forced asset sales/purchases by funds; and market manipulation by high-frequency traders. **Source: p. 133**

### Measuring time-series momentum

Measure correlation and p-value between a chosen past-return (look-back) period and future-return (holding) period; positive correlation supports momentum. Correlation between signs can be used when only directional continuation matters. Hurst exponent and Variance Ratio tests can test longer-run trending versus random walk. **Source: pp. 134–135**

### Independent return pairs

When comparing look-back and holding returns, observations must not overlap. Advance by the look-back if it is larger than holding period; otherwise advance by holding period. **Source: pp. 135–136; Figure 6.1**

### Roll return as an economic momentum signal

Futures may trend because contango/backwardation, and therefore roll-return sign, persists much longer than noisy spot returns. A lagged roll-return threshold can be a cleaner signal than lagged total return. **Source: pp. 139–140**

### Cross-sectional momentum

Rank a futures or stock universe by trailing performance; buy top-ranked and short bottom-ranked members, with staggered holdings. For futures, the intended effect is long backwardation and short contango so that correlated spot movements cancel and favorable roll returns remain. **Source: pp. 144–148**

## Mathematical Formulas

### Look-back and future returns

**Formula**

$$
r_{\mathrm{lag}}(t)=\frac{C_t-C_{t-L}}{C_{t-L}},\qquad
r_{\mathrm{fut}}(t)=\frac{C_{t+H}-C_t}{C_t}
$$

**Variables:** `$C_t$` close at time `$t$`; `$L$` look-back days; `$H$` holding days. **Purpose:** inputs to correlation test and direction signal. **Conditions:** omit missing values and select a nonoverlapping independent set. **Interpretation:** momentum expects positive correlation between the two returns. **Source: pp. 135–136, Box 6.1**

### Staggered time-series position and return

**Formula (equivalent to Example 6.1 code)**

$$
s_t=\begin{cases}1&C_t>C_{t-L}\\-1&C_t<C_{t-L}\end{cases},\qquad
\mathrm{pos}_t=\sum_{h=0}^{H-1}s_{t-h}
$$
$$
r_t=\frac{\mathrm{pos}_{t-1}}{H}\frac{C_t-C_{t-1}}{C_{t-1}}
$$

`$s_t$` is the daily direction decision; `$\mathrm{pos}_t$` aggregates `$H$` overlapping daily vintages; `$H$` normalizes capital. **Purpose:** make a decision every day while each tranche is held `$H$` days. **Conditions:** missing signals are zeroed. **Source: pp. 137–138**

### Cross-sectional ranking return

$$
R_{t,i}=\frac{C_{t,i}-C_{t-L,i}}{C_{t-L,i}}
$$

Rank `$R_{t,i}$` across instruments `$i$`; Example 6.2 buys the top `$N$` and shorts bottom `$N$`, rolls the same staggered `$H$`-day construction, and sums lagged-position dollar returns normalized by gross position. **Purpose:** capture persistence of relative performance. **Source: pp. 145–147**

## Methods and Procedures

### Test and trade a single future

1. Evaluate candidate look-back/holding pairs using nonoverlapping return pairs, correlation coefficient, and p-value.
2. Choose a statistically favorable pair, subject to out-of-sample validation.
3. Go long if price exceeds its `$L$`-day-old price, short if below.
4. Allocate one `$H$`th of capital daily and hold each tranche `$H$` days. **Source: pp. 134–139**

Example 6.1 applies `$L=250$`, `$H=25$` to TU. The chapter reports June 1, 2004–May 11, 2012 APR 1.7%, Sharpe about 1, and 2.5% maximum drawdown, calculated on approximately $200,000 notional while stated margin is about $400. **Source: pp. 137–139**

### Use roll-return signals / future-versus-ETF arbitrage

Long a future when lagged annualized roll return is above a positive threshold, short below negative threshold, and otherwise exit. For negative roll return/contango, buy the underlying (or proxy) and short the future/commodity fund; reverse in backwardation. The GLD–GC illustration’s apparent return is largely offset by financing GLD. XLE/USO is a proxy implementation: short USO/long XLE in CL contango, reverse in backwardation. **Source: pp. 140–143**

### VX–ES roll-return strategy

If front VX is above VIX by more than 0.1 point times days to settlement, short 0.3906 VX and short one ES; if below by the corresponding amount, buy both; hold one day. The author’s hedge ratio comes from the Chapter 5 price fit, not the original paper’s return regression. Reported out-of-sample July 29, 2010–May 7, 2012 APR is 6.9%, Sharpe 1. **Source: pp. 143–144**

### Cross-sectional futures and stocks

For 52 physical commodities, Example 6.2 ranks 252-day returns, buys 50 highest and shorts 50 lowest, and holds daily tranches 25 days. The stock version replaces total return with residual/factor return concepts; candidate factors include news sentiment and institutional purchase pressure. **Source: pp. 144–151**

## Derivations and Proofs

The chapter gives an economic decomposition rather than a formal proof: futures total return equals spot plus roll return (from Chapter 5). If spot returns are noisy but roll-sign persists, long-horizon total returns become serially correlated. In cross-sectional futures momentum, offsetting long/short spot exposure is intended to isolate roll return. **Source: pp. 139–145**

## Worked Examples

### Box 6.1 and Table 6.1: TU correlation search

The code loops `$L,H\in\{1,5,10,25,60,120,250\}$`, removes missing data, subsamples independently, and prints correlation/p-value. The author chooses TU 250-day look-back and 25-day hold because reported correlation is 0.2719 with p-value 0.0238. **Source: pp. 135–137; Table 6.1**

### Example 6.1: TU Momentum

Uses trailing 250-day sign, 25 overlapping holding tranches, and normalized prior-day position. **Source: pp. 137–139**

### Example 6.2: Cross-Sectional Momentum for Stocks

Uses 252-day return ranking, `topN=50`, separate top/bottom baskets, and 25-day staggered positions; the text reports 37% APR and 4.1 Sharpe for May 15–Dec. 31, 2007, while noting the short span. **Source: pp. 145–148**

## Figures and Tables

* **Figure 6.1:** nonoverlapping windows for correlation calculations. **Source: p. 135**
* **Table 6.1:** TU look-back/holding correlations and p-values; supports 250/25 selection. **Source: pp. 136–137**
* **Figure 6.2; Table 6.2:** TU equity curve and results for BR, HG, TU. Table 6.2 reports BR 100/10, APR 17.7%, Sharpe 1.09, max drawdown −14.8%; HG 40/40, 18.0%, 1.05, −24.0%; TU 250/25, 1.7%, 1.04, −2.5%. **Source: pp. 138–140**
* **Figures 6.3–6.4:** XLE–USO and VX–ES roll-return strategy cumulative returns. **Source: pp. 142–144**
* **Figures 6.5–6.6:** cross-sectional futures and stocks momentum equity curves. **Source: pp. 145–148**
* **Figure 6.7:** S&P DTI index, used in the discussion of momentum deterioration and tail behavior. **Source: pp. 153–154**

## Applications

The chapter applies interday momentum to futures with persistent term structures, ETF/future proxy spreads, volatility/equity futures, commodity ranking, equity ranking, news sentiment, and fund-flow pressure. **Source: pp. 137–152**

## Assumptions, Limitations, and Edge Cases

Results with few long-horizon trades risk data snooping; true out-of-sample testing is required. Margin permits leverage but also magnifies risk. ETF financing can eliminate a gross roll-arbitrage return. GC and GLD closing times differ, although the cited signal uses GC closes. Equation 5.7 cannot be used for VX. **Source: pp. 139–144**

Momentum’s stated weakness is “momentum crash”: it can lose sharply when a market reverses after a prolonged decline, as forced deleveraging/short-covering and crowded strategies interact. It has positive skew only in some settings and unlike mean reversion can have long losing stretches; diversification and a momentum/mean-reversion mix are discussed as mitigants, not guarantees. **Source: pp. 152–154**

## Common Mistakes and Warnings

* Computing correlations from overlapping return observations. **Source: pp. 135–136**
* Treating an in-sample parameter search as confirmation rather than data snooping risk. **Source: pp. 139–140**
* Ignoring financing costs, closing-time mismatch, or contract settlement timing. **Source: pp. 141–144**
* Assuming strong historical momentum is stable after a regime change/crowding. **Source: pp. 152–154**

## Key Takeaways

Interday momentum is most intelligible when tied to a persistence mechanism—especially roll return—not merely price-chart continuation. It demands nonoverlapping testing, careful exposure construction, out-of-sample validation, and explicit crash-risk management. **Source: pp. 133–154**

## Glossary

| Term | Definition | Source |
|---|---|---|
| Time-series momentum | A series’ past return positively predicts its future return. | p. 134 |
| Cross-sectional momentum | Relative winners continue outperforming relative losers. | pp. 133–134 |
| Look-back / holding period | Past-return / future-holding horizon used in the test and strategy. | pp. 134–136 |
| Roll return | Term-structure component of futures return. | pp. 139–145 |
| Momentum crash | Sharp adverse momentum reversal discussed as a strategy weakness. | pp. 152–154 |

## Connections to Other Chapters

Uses Chapter 2’s Hurst/Variance Ratio testing and Chapter 5’s spot-plus-roll framework. It contrasts with the Chapter 4/previous mean-reversion models and hands intraday momentum to Chapter 7. **Source: pp. 134, 139–145, 133–134**

## Open Questions or Extraction Issues

The end-page source presentation is partly graphical; Figure 6.7’s detailed axes/values are not fully recoverable from text extraction, so this file describes rather than reproduces it. Code is represented as mathematical/pseudocode logic, not copied verbatim.

## Quality-control checklist

- [x] Entire assigned chapter (pp. 133–154) examined; Chapter 7 material excluded.
- [x] Concepts, methods, examples, figures/tables, formulas, limitations, and locators represented.
- [x] No unsupported external information introduced; unresolved figure detail is flagged.
