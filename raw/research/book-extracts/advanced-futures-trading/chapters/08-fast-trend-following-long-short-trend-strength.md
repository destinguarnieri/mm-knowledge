# Strategy 8 — Fast trend following, long and short with trend strength

## Purpose and central argument

Strategy 8 is a faster long/short EWMAC trend-following variation. It risk-scales each instrument, holds long in a recent uptrend and short in a recent downtrend, and varies position size with trend strength. It uses EWMAC(16,64), rather than Strategy 7’s EWMAC(64,256), plus a position buffer to reduce unnecessary turnover.

The chapter argues that a faster filter can capture reversals that slow trend following misses. In the reported tests it outperforms the slow filter and long-only benchmark on most measures, but with higher costs and turnover. It should not replace the slow rule entirely: the next chapter combines forecasts from multiple EWMAC variations.

## Scope and relationships

* Large secular bull/bear markets can last years; the slow filters from Strategies 5–7 target them, but can miss shorter reversals.
* The generic rule is **EWMAC**. This chapter adds **EWMAC(16,64)** as a trading-rule variation alongside EWMAC(64,256).
* All other trading-plan elements are identical to Strategy 7. A buffered Strategy 7 uses this plan with EWMAC(64,256).

## Method

### Fast and slow EWMAs

Use back-adjusted price \(p\):

\[
\operatorname{EWMA}(N=16,\lambda=0.118)_t=0.118p_t+0.118(1-0.118)p_{t-1}+0.118(1-0.118)^2p_{t-2}+\ldots
\]

\[
\operatorname{EWMA}(N=64,\lambda=0.031)_t=0.031p_t+0.031(1-0.031)p_{t-1}+0.031(1-0.031)^2p_{t-2}+\ldots
\]

\(N\) is span in business days; \(\lambda\) is the stated EWMA coefficient; \(p_t\), \(p_{t-1}\), \(p_{t-2}\) are current and lagged back-adjusted prices. The original slow filter is \(\operatorname{EWMA}(64)-\operatorname{EWMA}(256)\); 256 is approximately a business year. The author reports that length ratios from 2 to 6 gave statistically indistinguishable results in both real and artificial data (the latter used to avoid potential in-sample fitting). A one-quarter ratio yields 64/256, 32/128, 16/64, 8/32, etc.

### Forecast, cap, and position size

\[
\text{Raw forecast}_{i,t}=\frac{\operatorname{EWMA}(16)_{i,t}-\operatorname{EWMA}(64)_{i,t}}{\sigma_{p,i,t}}
\]

\[
\text{Scaled forecast}_{i,t}=\text{Raw forecast}_{i,t}\times4.1
\]

\[
\text{Capped forecast}_{i,t}=\max(\min(\text{Scaled forecast}_{i,t},+20),-20)
\]

\[
N_{i,t}=\frac{\text{Capped forecast}_{i,t}\times\text{Capital}\times\text{IDM}\times\text{Weight}_i\times\tau}{10\times\text{Multiplier}_i\times\text{Price}_{i,t}\times\text{FX}_{i,t}\times\sigma_{\%,i,t}}
\]

\(i\) identifies instrument and \(t\) time. \(\sigma_{p,i,t}\) is the price-standard-deviation normalization term; \(\sigma_{\%,i,t}\) is the percentage standard-deviation estimate. \(N\) is the current **unrounded** contract position and may be positive or negative. The chapter names, but refers to earlier strategies for detailed definitions of, Capital, IDM, Weight, risk target \(\tau\), Multiplier, Price, and FX. Forecast scalar is 4.1; capping bounds forecast to [−20, +20]. Capping is said to matter more for fast filters because extreme values are more likely.

## Buffering to reduce costs

Faster filters trade more. The chapter contrasts forecast smoothing (not used, since extra smoothing would reduce the moving-average filter’s uptrend detection) with **buffering**: ignore small forecast-driven changes and trade only when actual position materially differs from optimal. Buffering is said to be optimal for costs that are a fixed percentage regardless of trade size—approximately fixed per-contract retail futures commissions without market impact—not the non-linear costs of large funds. It usually lowers turnover, except when the position moves in a straight line.

Set buffer fraction \(F=0.10\), described as a conservative convenience value. The theoretically correct value depends on rule speed/profitability and costs. The buffer is a fraction of average long position: Strategy 4’s position, equivalently Strategy 8’s position at forecast +10.

\[
B_{i,t}=\frac{F\times\text{Capital}\times\text{IDM}\times\text{Weight}_i\times\tau}{\text{Multiplier}_i\times\text{Price}_{i,t}\times\text{FX}_{i,t}\times\sigma_{\%,i,t}}
\]

\[
B^L_{i,t}=\operatorname{round}(N_{i,t}-B_{i,t}),\qquad B^U_{i,t}=\operatorname{round}(N_{i,t}+B_{i,t})
\]

Here \(B\) is buffer width in contracts, and \(B^L\)/\(B^U\) are lower/upper whole-contract bounds. Recalculate as forecasts, capital, price, FX, and standard-deviation estimate update. With current whole-contract position \(C_{i,t}\):

* Within the buffer zone: no trade.
* If \(C_{i,t}<B^L_{i,t}\): buy \(B^U_{i,t}-C_{i,t}\) contracts.
* If \(C_{i,t}>B^U_{i,t}\): sell \(C_{i,t}-B^U_{i,t}\) contracts.

**Source inconsistency.** The printed no-trade inequality is \(B^U_{i,t}\le C_{i,t}\le B^L_{i,t}\), reversing the lower and upper labels. Given the definitions, this cannot be a nonempty interval. The prose and worked example establish the intended meaning: no trade while the current position lies between lower and upper bounds. Retain this caveat in implementation review.

### Worked example: 22 July 2021

With $100,000 capital and only S&P 500 micro futures, the unrounded optimum was long 13.2 contracts. The average long position was 8.8; with \(F=0.1\), \(B=0.88\). Thus \(B^L=\operatorname{round}(13.2-0.88)=\operatorname{round}(12.3)=12\), and \(B^U=\operatorname{round}(13.2+0.88)=\operatorname{round}(14.1)=14\). Current \(C=12\), unchanged since 20 July, so no trade was required.

**Figure 33 (S&P 500, early 2021):** compares fractional unrounded optimal position (light-grey dashed), conventional rounded position (darker dashed), and buffered position (solid). From 7–30 April, simple rounding traded seven contracts in total; buffering made one two-contract trade on 16 April. The figure communicates substantially reduced turnover without performance damage.

## Results

Comparisons: Strategy 4 (long-only/no trend filter/risk-dynamic sizing); Strategy 7 (buffered slow EWMAC(64,256)); Strategy 8 (buffered fast EWMAC(16,64)).

### Table 27 — Median performance across instruments

| Metric | 4: Long only | 7: Slow L/S | 8: Fast L/S |
|---|---:|---:|---:|
| Mean annual return | 6.9% | 4.0% | 6.5% |
| Costs | −0.3% | −0.3% | −0.5% |
| Average drawdown | −18.7% | −30.1% | −28.8% |
| Standard deviation | 20.9% | 22.6% | 23.6% |
| Sharpe ratio | 0.32 | 0.19 | 0.27 |
| Turnover | 2.7 | 8.9 | 16.7 |
| Skew | −0.09 | 0.14 | 1.00 |
| Lower tail | 1.56 | 3.29 | 3.35 |
| Upper tail | 1.29 | 2.63 | 2.99 |

The author says fast trend is more profitable than slow trend on every shown measure except turnover/costs. It has much better skew, though slightly fatter tails. Positive skew is presented as desirable for trend following, and faster filters tend to provide better skew.

### Table 28 — Aggregate Jumbo portfolio

| Metric | 4: Long only | 7: Slow L/S | 8: Fast L/S |
|---|---:|---:|---:|
| Mean annual return | 15.4% | 21.5% | 24.1% |
| Costs | −0.8% | −1.0% | −1.7% |
| Average drawdown | −24.7% | −16.0% | −11.4% |
| Standard deviation | 18.2% | 22.3% | 22.7% |
| Sharpe ratio | 0.85 | 0.96 | 1.06 |
| Turnover | 20.7 | 27.5 | 60.5 |
| Skew | −0.04 | 0.61 | 0.81 |
| Lower tail | 1.44 | 1.90 | 1.97 |
| Upper tail | 1.24 | 1.63 | 1.81 |

For the aggregate portfolio, fast trend matches or outperforms slow trend on almost every measure, while bearing higher cost/turnover and having noticeably better skew.

**Figure 34 — Account curves:** Fast Strategy 8 finishes highest, buffered slow Strategy 7 second, and long-only Strategy 4 lowest (mid-1970s to about 2022). In late 2008, slow trend remained long most equity markets and performed similarly poorly to long-only; fast trend picked up the downtrend and had its best year.

## Regression against long-only returns

Using monthly returns and buffering for Strategies 7 and 8:

\[
\text{Fast 8: }y_t=\alpha+\beta x_t+\epsilon_t=1.55\%+0.38x_t+\epsilon_t
\]

\[
\text{Slow 7: }y_t=\alpha+\beta x_t+\epsilon_t=1.13\%+0.53x_t+\epsilon_t
\]

In context, \(y_t\) is the trend strategy monthly return, \(x_t\) Strategy 4 long-only return, \(\alpha\) uncorrelated additional return, \(\beta\) long-only exposure, and \(\epsilon_t\) residual. Fast beta is lower because the backtest mostly rose and the slow rule spent more time long; the faster rule is more likely to balance longs and shorts. Fast alpha is 0.17% per month (about 2% annually) higher. A footnote defines beta as covariance: relative standard deviation times return correlation; because all three standard deviations are roughly similar, beta estimates are almost identical to correlations.

## Implementation checklist and warnings

1. Calculate 64- and 16-day EWMAs from back-adjusted prices.
2. Normalize the crossover by price standard deviation; multiply by 4.1; cap at ±20.
3. Compute unrounded \(N\), then the 10%-average-long buffer and rounded limits.
4. Trade only outside the intended lower-to-upper no-trade zone, using the stated target-bound trade sizes.

Higher turnover/costs are the principal tradeoff. Forecast smoothing is deliberately excluded here. Buffering targets linear/fixed-per-contract-like costs, not market-impact costs. The printed no-trade inequality is internally inconsistent and must be treated as a likely typographical error.

## Conclusion, connections, and glossary

Strategy 8 is called the book’s “star” so far, exceeding Strategies 4 and 7 on nearly every benchmark. Strategy 9 explores skew and combining forecasts from 7, 8, and other EWMAC variations. Because forecasts have a consistent scale, their average can replace a single-rule forecast in the same position-sizing equation. Strategy 9 also discusses avoiding expensive instruments for faster variations; Part Two returns to capping; Part Six covers per-trade and non-linear cost reduction; Appendix A contains full citations.

**Glossary:** EWMAC (exponentially weighted moving-average crossover); EWMAC(16,64) (fast variation); forecast scalar (4.1 multiplier); capped forecast (restricted to −20/+20); buffering (no-trade band); turnover (trading activity); alpha (uncorrelated additional return); beta (covariance/exposure); skew (return-distribution asymmetry).
