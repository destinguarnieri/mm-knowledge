# Strategy Twenty: Cross-sectional Carry

## Purpose and central argument

This strategy turns *directional* carry into a within-asset-class relative-value forecast. For each instrument, it measures smoothed carry relative to the median smoothed carry of the other instruments in that asset class. The intended benefit is to hedge carry bets against other instruments in the same class, potentially improving the unattractive skew and other risk properties of carry for an undiversified portfolio.

The chapter finds that standalone cross-sectional carry is materially weaker than directional carry. It is somewhat diversified from directional carry (correlation about 0.31), so a modest allocation can be defensible for an investor who values many diversified rules and distrusts backtest statistics. It does not, however, materially improve the standalone carry strategy except for slightly lower turnover. More broadly, adding instruments provides more diversification benefit than adding further, correlated rule variations.

## Definition

**Strategy twenty:** a strategy that uses cross-sectional carry within asset classes.

It is a carry strategy, not a trend strategy. An attempted counterpart to asset-class trend—blending carry forecasts from instruments in an asset class—is stated not to produce a worthwhile strategy. The chapter instead ranks carry *relative to peers in the same asset class*.

## Forecast construction

### 1. Start with the raw directional-carry forecast

For each instrument, begin with the raw carry forecast from Strategy Ten:

\[
\text{Carry forecast} = \frac{\text{Annualised raw carry}}{\sigma_p \times 16}
\]

| Symbol / term | Meaning provided in this chapter | Units / domain |
|---|---|---|
| Annualised raw carry | Input numerator; obtained from Strategy Ten. | Annualised; exact construction is not repeated here. |
| \(\sigma_p\) | Appears in the formula but is not defined in this chapter. | Not specified here. |
| 16 | Formula scaling constant. Its derivation and units are not stated here. | Not specified here. |
| Carry forecast | Raw forecast used as the input to smoothing. | Not explicitly stated. |

**Source limitation:** the chapter refers the underlying raw-carry calculation and any definitions of \(\sigma_p\) to Strategy Ten; they are not reproduced here.

### 2. Smooth carry

Use one 90-day exponentially weighted moving average:

\[
\text{Smoothed carry forecast} = \operatorname{EWMA}_{\text{span}=90}(\text{Carry forecast})
\]

Although several smoothing spans could in principle be used, Strategy Ten found carry forecasts with different smooths to be highly correlated. For simplicity, this strategy uses only the 90-day smooth.

### 3. Remove the asset-class median

At each time period, calculate the median of the current smoothed forecasts for all instruments in the same asset class, then subtract it from the forecast of the instrument being traded:

\[
\text{Cross-sectional carry forecast}_{i,t}
= F_{i,t}-\operatorname{Median}(F_{1,t},\ldots,F_{j,t})
\]

| Symbol | Definition |
|---|---|
| \(F\) | Smoothed carry forecast. |
| \(i\) | Particular instrument. |
| \(t\) | Time period. |
| \(j\) | Number of instruments in the relevant asset class; the formula’s median runs over those instruments. |
| \(F_{i,t}\) | Smoothed carry forecast for instrument \(i\) at time \(t\). |

The median, rather than the mean, is used because it is more robust to outliers. It guarantees equal numbers of long and short positions, but it does **not** guarantee that the strategy’s average mean forecast is zero.

### 4. Scale and cap the forecast

Use a forecast scalar of **50** for the 90-day cross-sectional-carry forecast. This is higher than the scalar of 30 used for normal carry because subtracting the relative value reduces the magnitude of raw forecasts. Apply the normal absolute forecast cap of **20**.

The chapter’s trading-plan wording is:

\[
\text{Scaled forecast}_i = \text{Raw forecast}_i \times \text{forecast scalar}
\]

In this strategy, the raw forecast is the relative/cross-sectional carry forecast and the scalar is 50. The precise cap implementation is not further specified here beyond capping the absolute scaled forecast at 20.

## Illustration: US 2-year bond future (Figure 73)

Figure 73 plots the relative carry calculation for US 2-year bond futures:

| Line | Meaning |
|---|---|
| Solid black | Median carry for all bond futures in the data set. |
| Grey | Smoothed carry for the US 2-year bond future. |
| Dotted black | Difference between the grey and solid-black lines: cross-sectional/relative carry. |

Carry in bonds depends on the yield-curve slope. The chart shows bond carry falling when yield curves flattened across most countries in 2007 and 2019. The US 2-year series follows the same cycle as the bond-class median but with more exaggerated moves, which creates a relative-carry signal.

## Standalone performance

The chapter reports the median performance of each tradable instrument in each asset class, after dropping instruments too expensive to trade. Cross-sectional carry’s reported turnover is **2.9**. The author notes that the following can be compared directly with Tables 46–47 (p. 222) for directional carry in Strategy Ten.

### Financial asset classes (Table 87)

| Metric | Equity | Vol | FX | Bond |
|---|---:|---:|---:|---:|
| Mean annual return | 0.2% | 3.1% | 1.8% | 1.8% |
| Standard deviation | 10.4% | 16.8% | 21.8% | 25.2% |
| Sharpe ratio | 0.03 | 0.19 | 0.10 | 0.09 |
| Skew | 0.00 | −2.22 | −0.72 | −0.16 |

### Commodity asset classes (Table 88)

| Metric | Metals | Energy | Ags | Median |
|---|---:|---:|---:|---:|
| Mean annual return | 5.4% | 5.4% | 0.5% | 1.3% |
| Standard deviation | 17.3% | 27.1% | 32.1% | 17.6% |
| Sharpe ratio | 0.26 | 0.22 | 0.01 | 0.11 |
| Skew | 0.72 | 0.29 | −0.10 | −0.12 |

### Interpretation

- Results are “not especially good,” as with cross-sectional momentum.
- Sharpe ratio is about half that of directional carry, with only a modest skew improvement.
- Standard deviations vary across asset classes because forecast strength is not the same everywhere; they are higher where carry dispersion is greater.
- Unlike directional carry, whose performance was significantly stronger in financial markets (equities, bonds, FX, and volatility), cross-sectional carry has no equally clear financial-versus-commodity distinction.

## Jumbo-portfolio comparison (Table 89)

All figures below are for the aggregated Jumbo portfolio.

| Metric | Strategy Ten: carry | Strategy Twenty: cross-sectional carry | Combined: carry 70% + cross-sectional carry 30% |
|---|---:|---:|---:|
| Mean annual return | 19.7% | 5.7% | 16.1% |
| Costs | −0.8% | −0.7% | −0.7% |
| Average drawdown | −18.6% | −37.7% | −15.0% |
| Standard deviation | 20.8% | 16.1% | 18.0% |
| Sharpe ratio | 0.94 | 0.31 | 0.89 |
| Turnover | 19.2 | 17.6 | 17.3 |
| Skew | 0.41 | 0.21 | 0.09 |
| Lower tail | 1.57 | 1.58 | 1.60 |
| Upper tail | 1.49 | 1.45 | 1.42 |
| Alpha | 19.1% | 2.5% | 14.3% |
| Beta | 0.06 | 0.17 | 0.13 |

The aggregate Strategy Twenty Sharpe ratio is about three times the median individual-instrument result, but this is disappointing relative to directional carry’s approximately fourfold gain in moving from the average instrument to the Jumbo portfolio. Apart from modestly lower turnover, cross-sectional carry improves on none of directional carry’s reported attributes.

### Diversification case and warning

- Directional and cross-sectional carry have correlation of approximately **0.31**, similar to the correlation between directional and cross-sectional momentum.
- The 70%/30% mix is an illustrative allocation offering potential diversification benefit.
- Reducing the cross-sectional weight would improve the *backtested* Sharpe ratio, but the chapter warns against relying too heavily on backtested Sharpe ratios to select forecast weights.

## Add relative carry to trend and directional carry (Table 90)

Strategy Nineteen contains all previously developed momentum types plus directional carry. To add cross-sectional carry using the stated top-down allocation method, split the 30% carry allocation equally: 15% directional carry and 15% relative carry. All other strategy components remain unchanged.

This represents all the standalone trend and carry strategies developed so far, but **excludes** the optional adjustments in Strategies Twelve through Sixteen.

| Metric | Strategy 9: trend | Strategy 11: carry + trend | Strategy 19: four trend/momentum types + original carry | Strategy 20: four trend/momentum types + both carry types |
|---|---:|---:|---:|---:|
| Mean annual return | 25.2% | 26.5% | 27.0% | 26.8% |
| Costs | −1.2% | −1.1% | −1.1% | −1.1% |
| Average drawdown | −11.2% | −8.9% | −8.8% | −8.6% |
| Standard deviation | 22.2% | 20.9% | 20.8% | 20.4% |
| Sharpe ratio | 1.14 | 1.27 | 1.30 | 1.31 |
| Turnover | 62.9 | 46.5 | 43.9 | 46.2 |
| Skew | 0.98 | 0.76 | 0.70 | 0.60 |
| Lower tail | 1.99 | 1.86 | 1.82 | 1.81 |
| Upper tail | 1.81 | 1.75 | 1.73 | 1.69 |
| Alpha | 18.8% | 22.3% | 23.8% | 23.1% |
| Beta | 0.43 | 0.30 | 0.31 | 0.33 |

**Decision boundary:** someone preferring fewer rules, or treating backtested statistics as completely reliable, would probably exclude cross-sectional carry. The author instead prefers many diversified trading rules and remains sceptical of backtest results.

## More trading rules or more instruments?

The chapter’s wider conclusion is that increasing the number of instruments is normally more valuable than increasing the number of trading-rule variations.

| Comparison | Evidence cited |
|---|---|
| Instrument diversification multiplier (IDM) | Table 16: with 10 instruments, IDM = 2.2; with 30 or more instruments, IDM = 2.5. |
| Forecast diversification multiplier (FDM) | Table 52: with 10 rule variations, FDM = 1.35; with 30 variations, FDM = 1.81; it never exceeds 2.0. |
| Realised risk-adjusted return | Strategy Nine’s SR rose almost fivefold from one instrument to the Jumbo portfolio (over 100 instruments). Carry’s SR rose fourfold. From Strategy Nine (one rule type) to Strategy Twenty (six rule types, 30 rule variations), SR rises only from 1.14 to 1.31. Most of that rise occurs when carry is added to trend in Strategy Eleven. |

IDM and FDM measure *expected* diversification through reduced expected risk. Sharpe-ratio improvements measure *realised* diversification through risk-adjusted returns. On both measures, the potential gain from more instruments is stated to be significantly larger than the gain from more trading-rule variations.

Many strategy variants to this point are relatively highly correlated because they are variations on two styles, trend and carry. Cross-sectional trend and carry are relatively uncorrelated with their directional counterparts, but have weak outright performance and therefore add little in combination. The chapter says Part Three strategies are less correlated with trend and carry and should add significant value.

### Exceptions

Adding strategies can be preferable for two groups:

1. **Limited-capital traders:** they may be unable to trade the Jumbo portfolio due to minimum-capital constraints. They should first trade as many instruments as possible, then add rules to eke out performance.
2. **Traders who have exhausted the instrument opportunity set:** a Jumbo portfolio of 100+ instruments already has excellent diversification, so adding another 100 may add little; adding strategies may be preferable.

## Trading plan

| Component | Rule |
|---|---|
| Strategy | Go long or short one or more instruments using a variable risk estimate and a forecast based on cross-sectional carry. |
| Eligible instruments | Any instruments meeting minimum-capital, liquidity, and cost thresholds. |
| Trading-rule speed | Use the usual speed limit. Reported turnover for this rule is 2.9. |
| Forecast | Raw Strategy-Ten carry forecast → 90-day EWMA → subtract asset-class median → scale by 50 → cap absolute scaled forecast at 20. |
| Other stages | Identical to Strategy Ten (standalone carry). Details are not repeated in this chapter. |

## Practical cautions and edge cases

- Only compare instruments within the same asset class; the relative forecast is defined against that class’s median.
- Use a **median**, not a mean, to resist outliers. This produces equal counts of long and short positions but does not ensure a zero mean forecast.
- Drop instruments that are too expensive to trade; the detailed cost threshold is not restated here.
- Do not infer that a slightly better in-sample Sharpe ratio warrants a larger cross-sectional allocation.
- The chapter does not specify behavior when an asset class has insufficient eligible instruments, missing forecasts, or tied median observations; these are implementation details not supplied by the source.

## Connections to other chapters

- **Strategy Ten:** supplies the raw carry forecast, the normal-carry scalar of 30, and all non-forecast stages of the trading plan.
- **Strategy Eighteen:** its asset-class-trend idea motivates a rejected analogue for carry.
- **Strategy Nineteen:** provides the four-momentum-types-plus-directional-carry portfolio to which relative carry is added.
- **Strategies Twelve–Sixteen:** optional adjustments deliberately excluded from the Table 90 composite.
- **Strategy Nine / Strategy Eleven:** used in the instrument-versus-rule diversification comparison.
- **Part Three:** follows this chapter with additional trading styles that still generate combinable trading-rule forecasts.

## Glossary

- **Annualised raw carry:** input to the carry forecast; exact calculation is referenced to Strategy Ten.
- **Carry forecast:** risk-normalised forecast derived from annualised raw carry.
- **Cross-sectional / relative carry:** an instrument’s smoothed carry minus the median smoothed carry of its asset-class peers.
- **Directional carry:** ordinary/standalone carry without the cross-sectional median subtraction.
- **EWMA:** exponentially weighted moving average; here, span 90 days.
- **Forecast scalar:** multiplicative forecast calibration constant; 50 for this cross-sectional-carry rule.
- **Forecast cap:** maximum absolute scaled forecast; 20 here.
- **IDM:** instrument diversification multiplier, a measure of expected diversification through expected-risk reduction.
- **FDM:** forecast diversification multiplier, the analogous expected-diversification measure for rule variations.
- **Jumbo portfolio:** the book’s aggregated portfolio of over 100 instruments.

## Key takeaways

1. Cross-sectional carry expresses carry as a within-asset-class deviation from the median, using a 90-day EWMA and a 50 scalar capped at 20.
2. It is low correlation (about 0.31) with directional carry but has a substantially lower standalone Sharpe ratio and offers little direct improvement other than lower turnover.
3. An illustrative 70% directional / 30% cross-sectional carry mix may diversify exposure, but allocation should not be overfit to backtested Sharpe ratios.
4. In general, expand the instrument universe before piling on closely related rule variations; limited capital and already-exhausted instrument sets are the stated exceptions.

## Source notes

- Footnote 205 notes academic attention to relative carry, citing “Carry,” by Ralph S.J. Koijen, Tobias J. Moskowitz, Lasse Heje Pedersen, and Evert B. Vrugt, *Journal of Financial Economics* 127(2), 2018.
- No outside material was used to expand that citation or fill in definitions absent from this chapter.
