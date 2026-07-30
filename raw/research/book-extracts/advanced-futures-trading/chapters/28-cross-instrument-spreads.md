# Strategy Twenty-Eight: Cross Instrument Spreads

## Purpose and central claim

This chapter turns two related futures into a **synthetic relative-value (RV) instrument**: long one leg and short the other. It argues that the synthetic price can be handled much like a futures price—back-adjusted, forecast, risk-scaled, sized, and buffered—but that this convenience conceals important operational and tail risks. The central trade-off is lower exposure to outright market movement and potentially strong diversification versus higher leverage, two-leg costs, correlation-break risk, and generally weaker results than outright trades in the limited tests shown.

> **Strategy:** Trade pairs of instruments as relative-value spreads.

Source scope: Strategy Twenty-Eight only. The book refers to methods in Strategies 3, 4, 9, and 10; those methods are not restated here except where this chapter specifies a modification.

## Core concepts and notation

- **Spread instrument \(R a/b\):** long instrument \(a\) and short instrument \(b\) in a value-weight ratio \(R:1\). If \(R=1\), write \(a/b\).
- **Synthetic instrument:** the spread treated as a new tradable whose unit is defined as one short contract of \(b\), hedged by the required long quantity of \(a\).
- \(R\): desired weight ratio, positive by convention. Example: \(1.5\mathrm{US5}/\mathrm{US10}\) is long US 5-year futures and short US 10-year futures in a 1.5:1 ratio.
- \(p_a,p_b\): prices of instruments \(a,b\), in their quoted price units.
- \(p_\Delta\): synthetic spread price, in the price units normalized to leg \(b\).
- \(N_a,N_b\): positive numbers of contracts in legs \(a,b\). The actual \(b\)-leg position of a long synthetic spread is \(-N_b\).
- \(M_a,M_b\): futures multipliers for legs \(a,b\), in currency per price point per contract.
- \(FX_a,FX_b\): FX conversion rates into base currency.
- \(\sigma_{p,a},\sigma_{p,b},\sigma_{p,\Delta}\): standard deviations of *daily price changes* (not percentage returns) for leg \(a\), leg \(b\), and the spread.
- \(\rho\): correlation between daily price changes of \(a\) and \(b\).
- \(\tau\): annual risk target; the chapter suggests 10% for spreads.
- **weight:** capital allocation proportion for an instrument; **IDM:** instrument-diversification multiplier.
- \(C_b\): current position in leg \(b\). \(B\): buffer width. A bar/rounded position represents an executable whole-contract position.

## Constructing the synthetic price and hedge

### Synthetic price

\[
p_\Delta = R p_a - p_b
\]

The price may be zero or negative. Percentage volatility is therefore inappropriate; use price changes. For the illustrative prices US5 \(\approx112\), US10 \(\approx119\), and \(R=1.5\):

\[
p_\Delta=1.5(112)-119=49.
\]

### Contract ratio

To make the actual contracts implement the desired *value* weights:

\[
\frac{N_a}{N_b}=
\frac{R\,M_b\,FX_b}{M_a\,FX_a}.
\]

For equal multipliers and equal USD FX rates, this reduces to \(N_a/N_b=R\). Thus one short US10 contract needs 1.5 long US5 contracts in the example.

### Value/exposure derivation

For any futures position:

\[
\text{Notional exposure} = N\,M\,p\,FX.
\]

The two-leg net exposure is

\[
E=N_aM_ap_aFX_a-N_bM_bp_bFX_b.
\]

Substituting the contract ratio gives

\[
E=N_b\,p_\Delta\,(M_bFX_b).
\]

Hence one unit of the synthetic instrument (one short \(b\) contract) has notional exposure \(p_\Delta M_bFX_b\). A one-unit change in spread price changes value by \(M_bFX_b\). With US10 multiplier 1,000 and USD FX 1, a move from 49 to 50 raises exposure from $49,000 to $50,000: $1,000 profit.

### Implementation implication

If the synthetic strategy calls for buying/selling \(X\) spread units, buy/sell \(X(N_a/N_b)\) contracts of \(a\) and simultaneously sell/buy \(X\) contracts of \(b\). Back-adjust the underlying futures first, then calculate \(p_\Delta\). Fractional contracts must be resolved operationally (see minimum capital).

## Spread risk: why correlation matters

Daily spread-price-change volatility is measured as

\[
\sigma_{p,\Delta}=\operatorname{sd}\big[(p_{\Delta,t}-p_{\Delta,t-1})\big].
\]

For a two-asset portfolio,

\[
\sigma_{portfolio}=\sqrt{w_a^2\sigma_{p,a}^2+w_b^2\sigma_{p,b}^2+2\rho w_aw_b\sigma_{p,a}\sigma_{p,b}}.
\]

Using spread weights \(w_a=R\), \(w_b=-1\):

\[
\sigma_{p,\Delta}=\sqrt{R^2\sigma_{p,a}^2+\sigma_{p,b}^2-2\rho R\sigma_{p,a}\sigma_{p,b}}.
\]

The formula is presented for intuition and risk management; the author does not use it as the primary realized-volatility estimator. The chapter’s stated estimator for sizing is an exponentially weighted standard deviation with a 32-day span and a blend of past and future volatility (as defined in Strategy 3).

**Example.** For 1.5US5/US10, the reported daily price-change standard deviations are 0.379 (US5), 0.568 (US10), and 0.159 (spread), with \(\rho=0.961\). Reducing correlation to 0.86 would raise estimated spread risk to about 0.30—nearly double. This is **correlation risk**: high initial correlation produces a low estimated volatility and high leverage; a subsequent correlation break can force margin-driven liquidation, including a possible “death spiral.”

Footnote context: the chapter says the component/correlation formula may be used to stress correlation and risk for sizing or portfolio risk. It also notes that high leverage does not automatically mean more margin; margin depends on broker, exchange, and product mix.

## Position sizing

The directional-futures form quoted by the chapter is

\[
N_i=\frac{\text{scaled forecast}_i\times\text{capital}\times\text{weight}_i\times IDM\times\tau}{10\times M_i\times p_i\times FX_i\times\sigma_{\%,i}\times16}.
\]

For a spread, replace percentage volatility with price-change volatility; the price cancels and the synthetic unit is leg \(b\):

\[
N_b=\frac{\text{scaled forecast}\times\text{capital}\times\text{weight}\times IDM\times\tau}{10\times M_b\times FX_b\times\sigma_{p,\Delta}\times16}.
\]

The divisor 10 converts the chapter’s average scaled forecast of 10 to a full-risk forecast; 16 annualizes a daily standard deviation under the book’s convention. \(N_b\) is the number of synthetic units and represents a *short* \(b\) position for a positive spread forecast. Set \(N_a=(N_a/N_b)N_b\) for the long leg.

**Worked sizing example.** Capital $500,000; one spread only (weight = IDM = 1); \(\tau=10\%\); scaled forecast \(+10\); \(\sigma_{p,\Delta}=0.159\); US10 multiplier 1,000; USD FX 1. The result is \(N_b\approx19.7\) short US10 contracts and \(N_a\approx29.5\) long US5 contracts. The reported absolute notional is nearly $5.6m (over 11× capital): about $3.3m long US5 and $2.3m short US10. Comparable outright directional positions with the same assumptions are about 8.2 US5 or 5.5 US10 contracts.

**Constraint:** use a lower spread target. The author calls 10% reasonably conservative but warns that even this may be too aggressive because the position is highly leveraged.

## Choosing \(R\)

Avoid picking \(R\) to maximize backtested profitability: that is likely overfitting. One could use beta-neutral equity weights or duration-neutral fixed-income weights to hedge a defined “market.” This chapter instead minimizes outright spread-price risk.

Differentiating the spread-volatility expression with respect to \(R\) gives

\[
R^*=\frac{\rho\sigma_{p,b}}{\sigma_{p,a}}.
\]

The text then identifies the practical, order-independent ratio for minimum spread-price risk as

\[
R=\frac{\sigma_{p,b}}{\sigma_{p,a}}.
\]

Place the lower-volatility leg in position \(a\) if you prefer \(R>1\); ordering is otherwise a convention. For US5/US10, \(R=0.568/0.379=1.5\). The chapter explains that blindly using the first expression creates an ordering paradox when volatilities are equal and \(\rho<1\): it would prescribe the same \(R<1\) after swapping legs.

Operationally, optimal ratios are usually non-integers and time-varying (US5/US10 reportedly ranged from 1 to 2.75 over 30 years). The author generally averages the volatility-ratio result over the last ten years (all available data if shorter), rounds it to a “nice” number, or uses a market convention. Fixed \(R\) sacrifices the optimal hedge and increases correlation with outright prices.

## Capital, integer constraints, and cost

### Minimum capital

For four contracts, the original formula is

\[
\text{minimum capital}=\frac{4M_ip_iFX_i\sigma_{\%,i}}{IDM\times weight_i\times\tau}.
\]

For a spread:

\[
\text{minimum capital}=\frac{4M_bFX_b\sigma_{p,\Delta}\times16}{IDM\times weight_i\times\tau}.
\]

Use \(\tau=10\%\) as suggested. If \(N_a/N_b\) is not integral, multiply the calculated minimum by the smallest contract-package factor that makes both legs whole. Examples: 0.5 requires 2 units (double capital); 0.4 requires a 2:5 package (fivefold capital); 0.95 would require a 20-fold package, so adjust \(R\) toward a practical contract ratio instead. In the 1.5US5/US10 example, the basic calculation is multiplied by two for a 3-US5/2-US10 package, yielding just over $200,000. At matching 10% risk, the stated standalone minima are $242,000 (US5) and $363,500 (US10); at a normal 20% directional target, $121,000 and $181,000.

### Trading cost

Here “spread cost” means bid–offer execution spread, not an RV spread:

\[
\text{spread cost (price points)}=(\text{bid}-\text{offer})/2
\]
\[
\text{spread cost (currency)}=M\times\text{spread cost (price points)}
\]
\[
\text{cost per contract}=\text{spread cost (currency)}+\text{commission}.
\]

Normalize to leg \(b\)’s currency:

\[
\text{cost}_a=\frac{N_a}{N_b}\times\text{cost per contract}_a\times\frac{FX_a}{FX_b},\qquad
\text{cost}_b=\text{cost per contract}_b
\]
\[
\text{total cost}=\text{cost}_a+\text{cost}_b
\]
\[
\text{risk-adjusted cost per trade}=\frac{\text{total cost}}{\sigma_{p,\Delta}\times16\times M_b}.
\]

The 1.5US5/US10 risk-adjusted execution cost is reported as almost eight times each standalone leg (US5 0.00091; US10 0.001), because the spread trades 2.5 contracts total and has much lower volatility. If roll schedules differ, use the larger number of rolls per year for rolling-cost calculation.

## Selecting plausible spreads

There are nearly 5,000 possible pairs among the author’s 100+ instruments. Restrict candidates to economically justified, high-correlation relationships within an asset class; otherwise selection is data mining/overfitting. The chapter’s cautionary rejected example is NZD/USD versus Live Cattle. Inclusion of one plausible pair rather than another does not imply superiority, and sufficiently capitalized traders could hold both.

- **Fixed income:** natural home of spreads due to very high bond/STIR correlations. A caveat: 2012–early 2022 suppressed yield volatility, especially at the short end, distorting empirically calculated \(R\). The author adjusted displayed fixed-income ratios using both empirical averages and a judgmental “normal” rate environment; e.g., duration weighting for German 2-year Schatz/20-year Buxl would be roughly 7, while raw data would yield much higher.
- **Equities:** correlations lower than bonds; usually stronger within countries. Candidates include sector/index, large/small cap, tech/index.
- **Volatility:** only VIX and VSTOXX were liquid enough in the Jumbo portfolio, leaving the Atlantic volatility spread.
- **FX:** excluded. A cross rate requires a ratio of FX rates, whereas this method uses their difference; therefore an additive synthetic spread is not a theoretically correct cross-rate proxy.
- **Agriculture:** seek related contracts within granular groups (grains, softs, meats, indices), or cautiously across subgroups.
- **Metals:** precious, non-precious, and crypto groups can be compared. Gold/Bitcoin is omitted because the observed correlation is slightly negative.
- **Energy:** logical refinery-product relations can support a spread but can also change for fundamental production-cost reasons that a backward-looking \(R\) misses. Grade/location and last-day variations can be highly related. Natural gas/oil is excluded because the reported correlation is very low.

The chapter displays Tables 136–141 as example fixed-income, equity, Atlantic-volatility, agricultural, metals, and energy spreads. Each has the same fields: legs, daily-price-change correlation \(\rho\), suggested \(R\), \(N_a/N_b\), minimum capital at \(\tau=10\%\), and risk-adjusted cost. The table values are graphical in this EPUB extraction and are not reproduced here rather than guessed.

## Trading and buffering the spread

Use standard forecasting and sizing machinery on the back-adjusted synthetic price, with the modifications above. Do **not** buffer legs independently: doing so can leave a temporary unhedged exposure.

1. Calculate the spread buffer width using daily price-change volatility and leg \(b\)’s multiplier/FX (the same substitutions used in spread sizing).
2. Form the buffer around the optimal \(-N_b\) position for leg \(b\), and compare current \(C_b\) with it.
3. If \(b\) is inside its buffer, make no trade in either leg.
4. If outside, trade \(b\) to the applicable rounded buffer edge; use that resulting rounded \(b\) position to calculate the matching target in \(a\) from \(N_a/N_b\), round \(a\) if needed, compare with current \(a\), and execute both required trades as close to simultaneously as possible.

## Trend test: US bond spreads

The chapter tests EWMAC16,64 on ten spreads constructed from US 2-, 5-, 10-, 20-, and 30-year futures. It omits ultra US10 (very similar, short history) and US3 (limited history). Nearby maturity spreads resemble forward-rate/yield-curve-slope exposures and may be idiosyncratic; wide spreads reflect a larger portion of the rate cycle. Figures 84 and 85 plot 7US2/US20 and 1.5US5/US10 synthetic prices. The former visibly tracks rate cuts/rises through 2004, the 2008 crash, and 2020; the latter also follows rates, less clearly after the post-2008 low-rate regime. Both visually exhibit trends.

In the matrices below, instrument \(a\) is the row and \(b\) the column. Empty cells duplicate the opposite ordering and are not separately reported.

### Inputs and construction

| US Treasury future | Code | Annual vol | Multiplier | Min capital (20%, 4 contracts) | Risk-adjusted cost |
|---|---:|---:|---:|---:|---:|
| 2-year | ZT | 1.8% | 2,000 | $74,000 | 0.0031 |
| 5-year | ZF | 4.7% | 1,000 | $108,000 | 0.00091 |
| 10-year | ZN | 6.8% | 1,000 | $160,000 | 0.0010 |
| 20-year | ZB | 13.1% | 1,000 | $370,000 | 0.0017 |
| 30-year | UB | 19.9% | 1,000 | $610,000 | 0.00091 |

Reported daily-price-change correlations: 2y/5y .92, 2y/10y .82, 2y/20y .62, 2y/30y .50; 5y/10y .96, 5y/20y .81, 5y/30y .70; 10y/20y .92, 10y/30y .83; 20y/30y .96. Suggested \(R\): 2y/5y 2.5; 2y/10y 4; 2y/20y 7; 2y/30y 10; 5y/10y 1.5; 5y/20y 3; 5y/30y 4; 10y/20y 2; 10y/30y 3; 20y/30y 1.5.

### EWMAC16,64 results

| Measure | Spreads, in row/column order 2/5, 2/10, 2/20, 2/30; 5/10, 5/20, 5/30; 10/20, 10/30; 20/30 | Outrights (2y, 5y, 10y, 20y, 30y) |
|---|---|---|
| Sharpe ratio | .17, .18, .40, .20; −.12, .14, .11; .20, .10; .06 | .64, .54, .43, .30, .43 |
| Skew | 1.00, .90, 1.31, 2.52; 1.18, 1.36, 3.47; 1.39, 3.67; 6.40 | 1.32, .95, 1.03, 1.25, 1.74 |
| Lower-tail ratio | 3.42, 3.19, 3.01, 3.02; 3.75, 3.67, 3.02; 3.38, 3.12; 3.31 | 3.38, 2.94, 2.98, 2.93, 2.84 |
| Correlation to EWMAC16 US10 returns | .37, .39, .36, .27; .14, .23, .20; .28, .21; .18 | .71, .94, 1.00, .90, .40 |

Interpretation supplied by the author: no spread beats every outright SR (possible exception US2/US20); adjacent maturities may perform worse. Positive skew is surprisingly good, perhaps because trend-following exits sharp adverse moves. But the more robust lower-tail statistic is significantly worse, especially for highly correlated spreads—possibly because a few positive outliers drive skew under higher leverage. Spreads are generally more diversifying than out-rights; US30 is the exception. Different history lengths, especially only 12 years for US30, may distort the comparisons.

## Carry on spreads

Carry requires more than a back-adjusted price. Substitute synthetic spread prices into the raw-carry formulas from Strategy 10, provided both legs use the same raw-carry convention. The chapter assumes:

1. Both instruments have the same number of rolls per year.
2. Both always roll on the same day.

Use months between contracts for leg \(b\) and divide the annualized raw-carry measure by \(\sigma_{p,\Delta}\) rather than percentage volatility; then cap the forecast and use the usual sizing/buffering procedure. Broken synchronization distorts carry during unsynchronized roll periods (e.g., monthly versus quarterly is wrong roughly two-thirds of the time), though smoothing may reduce the damage.

For carry60 on the same US bond set:

| Measure | Spreads in the same row/column order as above | Outrights (2y, 5y, 10y, 20y, 30y) |
|---|---|---|
| Sharpe ratio | −.07, −.06, .06, −.13; −.07, .00, −.11; .25, −.08; −.05 | .25, .47, .48, .57, .20 |
| Skew | .37, .57, .68, −.53; −.03, .25, −.85; −.09, −.93; 1.04 | −.09, .04, −.07, .25, .11 |
| Lower-tail ratio | 1.41, 1.53, 1.90, 2.67; 1.45, 1.84, 3.20; 1.56, 2.81; 2.14 | 1.85, 2.31, 2.19, 2.03, 2.70 |
| Correlation to carry US10 returns | −.47, −.50, −.41, −.16; −.22, −.30, −.01; .01, −.02; .07 | .72, .93, 1.00, .80, .22 |

Carry spreads are highly diversifying (zero/negative correlations) but the chapter calls this “diworsification”: SRs are near zero and tail measures unimpressive. In this US fixed-income subset, spread carry does not work well.

## Warnings, boundary conditions, and practical takeaways

- RV does not eliminate market risk in practice; it converts much of it into correlation, model/hedge-ratio, leverage, execution, and liquidity risk.
- Spreads require substantially more leverage to hit a given risk target. Lower realized risk can be a dangerous input if correlation is unstable.
- Two-leg costs can overwhelm the apparent diversification benefit; assess cost on a risk-adjusted basis.
- Do not use percentage volatility when \(p_\Delta\) can approach/cross zero.
- Avoid unjustified cross-asset pairs and data-mined relations. FX cross rates are specifically outside this additive-spread framework.
- Market conventions and practical integer packages may justify deliberately imperfect fixed weights.
- Execute both legs nearly simultaneously; independent leg buffers create unwanted directional exposure.
- The favorable trend skew result does not negate poorer lower-tail behavior.

## Conclusion and glossary

The chapter’s limited results suggest spreads are harder, costlier, more capital-intensive, and less rewarding than directional trades, particularly for carry; hedging away risk may also hedge away risk premia. Their case is diversification: a large institution already trading liquid outright futures may gain from relatively low-correlated spread strategies.

**Glossary:** relative value (RV); spread instrument; synthetic instrument; outright instrument; hedge ratio; correlation risk; price-change volatility; risk target; IDM; back-adjusted price; minimum capital; risk-adjusted cost; buffer; beta neutral; duration neutral; EWMAC16,64; carry60; lower-tail ratio; STIR; data mining; overfitting.

## Explicit chapter connections

- **Strategy 3:** exponentially weighted volatility (32-day span) and blended past/future volatility.
- **Strategy 4:** IDM calculation/approximations.
- **Strategies 9 and 10:** trading-plan stages; the final plan says all other stages are identical to these strategies.
- **Strategy 10:** raw-carry formulas and carry smoothing, modified here for synthetic prices.
