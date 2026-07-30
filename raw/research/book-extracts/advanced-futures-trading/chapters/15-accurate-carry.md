# Strategy Fifteen: Accurate Carry

## Purpose and central argument

This strategy is a modification that can be applied to any strategy using one or more carry trading rules. Its purpose is to make the carry estimate better reflect the carry that will actually be experienced. The central problem is that the usual futures-curve comparison only corresponds to realised carry if spot prices remain unchanged **and** the curve has an identical gradient without irregularities from such things as seasonal weather, bond auctions, or dividend-payment timing.

The chapter distinguishes a few cases. For a non-front contract, comparing the held contract with a nearer contract is already accurate. For front-month contracts, the natural futures-to-next-futures comparison can contain predictable seasonal distortion. The chapter gives a seasonal-adjustment procedure, but its test produces slightly worse results. For fixed seasonal contract months, it gives an alternative long-horizon comparison, which likewise does not improve the author's tested performance. The author concludes that the additional work is generally not justified by marginal gains.

## Core terms and relationships

- **Carry**: the expected return arising as a futures contract ages/moves along an unchanged futures curve. The chapter takes unchanged spot prices as an unspoken assumption of carry.
- **Current/held contract**: the futures expiry currently traded.
- **Nearer contract**: a contract expiring before the held contract.
- **Front month / nearest contract**: the earliest-expiring futures contract.
- **Further-out/next contract**: the expiry after the held contract; it is used when the held contract is the front month because no nearer contract exists.
- **Raw carry**: the unadjusted carry quantity derived from contract prices. The exact price-difference orientation used in the trading-plan graphic is given below.
- **Carry forecast**: volatility-normalised annualised raw carry; it is the quantity seasonally adjusted in this chapter.
- **Seasonal carry component**: the calendar-pattern component found by comparing today's carry forecast with its trailing one-year average.
- **Net carry forecast**: carry forecast after removing the unshifted seasonal component.
- **Shifted seasonal component**: the historical seasonal component moved forward by one contract-roll interval, intended to represent the seasonal carry that would actually be experienced between the current futures contract and spot.

## When the usual carry measure is accurate

### Held contract is not the nearest

If a fixed held contract is not the nearest expiry, measure carry by comparing it with a nearer contract. Example: for March 2025 Eurodollar, compare with December 2024. The chapter calls this an accurate estimate of expected carry and requires no additional adjustment.

Examples named: short-term interest rates such as Eurodollar, volatility instruments, Natural Gas, and commodities including Butter, Feeder cattle, Heating Oil, and Rice.

### Held contract is the nearest

With a front-month holding there is no nearer contract. The conventional proxy compares the current contract price with the next expiry. But the carry actually experienced is the difference between the current contract price and the **spot price**. Thus a non-constant futures-curve slope makes the proxy imperfect.

Metals and FX normally have an approximately constant curve slope, but expected near-term interest-rate changes can disrupt it. The chapter says there is no consistent historical pattern to correct this without extra inputs such as interest-rate data. In metals, carry is driven by storage and funding costs; with storage relatively static, interest rates are key. In FX, relative forward interest rates determine futures prices and carry. A more involved alternative is to infer storage cost from the yield curve (metals) or use the forward curve (FX), but both need futures-synchronised interest-rate data and are described as demanding.

## Using spot prices

The best direct correction is to calculate carry from the price difference between current futures and spot. It requires additional data that are synchronised with futures prices.

| Spot-price availability in the chapter | Markets |
|---|---|
| Readily available | Equity indices; volatility (for example VIX); FX rates |
| Usually available | Agricultural commodities; energy markets; metals and crypto |
| Difficult to obtain | Bond markets |

For bonds, the required work is to identify the cheapest-to-deliver bond, obtain its price, and obtain or calculate its conversion factor. Expected bond carry can alternatively be measured from the yield curve, but this also requires knowing or estimating bond duration.

The strategy-plan formula for seasonal front-month instruments when a good-quality spot price is synchronised with futures is:

\[
\text{Raw carry}=\text{spot price}-\text{price of current futures contract}.
\]

## Seasonal adjustment for front-month carry

### Applicability and requirements

This approach applies where the held contract is the nearest and predictable seasonal effects distort the curve. Seasonal effects occur in commodity markets, equity indices (because of dividend timing), and some bond markets. It needs several years of data; the author suggests at least three years of price history so seasonal adjustments can be averaged across years.

Begin with the raw, unsmoothed, volatility-normalised carry forecast. The chapter uses:

\[
\text{Carry forecast}=\frac{\text{annualised raw carry}}{\sigma_p\times16}.
\]

Here \(\sigma_p\) is the volatility term shown in the source formula; the chapter does not further define its calculation or unit in this chapter. The factor 16 is also not re-derived here. This volatility-normalised formulation is chosen because volatility itself may be seasonal, and—more importantly—because forecasts become comparable across time for estimating seasonality.

Let \(C_t\) be the carry forecast at time \(t\). With 256 business days in a year, the current seasonal carry estimate is:

\[
S_t=C_t-\frac{C_t+C_{t-1}+C_{t-2}+\dots+C_{t-256}}{256}.
\]

Where:

- \(S_t\): estimated seasonal component at time \(t\).
- \(C_t\): current volatility-normalised carry forecast.
- \(C_{t-k}\): carry forecast \(k\) business days earlier.
- 256: assumed number of business days in a year.

The textual description calls the average a rolling one-year moving average. The displayed expression includes \(C_t\) through \(C_{t-256}\) while dividing by 256; this apparent count convention is preserved from the source rather than resolved here.

### Step-by-step procedure

1. Calculate the unsmoothed volatility-normalised carry forecast \(C_t\).
2. Calculate \(S_t\) by subtracting the rolling one-year average of the carry forecast from \(C_t\).
3. Assign each \(S_t\) a calendar-year and calendar-day index: index 1 is 1 January, 2 is 2 January, and so on. Ignore 29 February for this indexing.
4. Average each calendar-day seasonal estimate across years. For an illustrative data history from 2000 through 2021:

   \[
   S_{\text{average},1}=\frac{S_{1,2000}+S_{1,2001}+S_{1,2002}+\dots+S_{1,2021}}{22}.
   \]

   In general, \(S_{\text{average},d}\) is the across-year average seasonal component for calendar day \(d\). For 29 February, use the average seasonal component for 28 February.
5. Remove the seasonal component to form net carry. On 3 February 2021 (day 34), subtract \(S_{\text{average},34}\) from the carry forecast. This net forecast can be used for position sizing if the goal is to remove seasonality completely.
6. To estimate the seasonal carry actually experienced, circularly shift the average seasonal series by one roll interval. If rolling four times per year, the approximate interval is \(365/4=91\) days: replace \(S_{\text{average},92}\) with \(S_{\text{average},1}\), \(S_{\text{average},93}\) with \(S_{\text{average},2}\), continuing through the wraparound; \(S_{\text{average},1}\) is replaced with \(S_{\text{average},275}\), and \(S_{\text{average},91}\) with \(S_{\text{average},365}\).
7. Add the shifted seasonal average to net carry. For a net carry forecast on 2 April 1998 (day 92), add the shifted \(S_{\text{average},92}\).

The intuition is: first subtract the incorrectly included seasonal component from the current-to-next-contract proxy, then add the expected seasonal carry between the current contract and spot.

### Worked conceptual example

Suppose a quarterly rolling contract has strong positive carry from mid-December to mid-June and negative carry for the rest of the year. In mid-September, while holding December (the front month), comparing December to the following March gives a highly positive carry forecast even though the actual expected carry is negative. Subtract the expected seasonal carry for December-to-March, then add expected seasonal carry actually earned from September-to-March. The result is intended to match expected realised carry.

## Figures 60–64: Eurostoxx seasonal-adjustment example

The source supplies graphs rather than numerical data; their intended messages are:

- **Figure 60 — Original raw carry for Eurostoxx**: raw carry forecast plus its 12-month rolling average. The difference between the lines is the seasonal carry estimate.
- **Figure 61 — Seasonal carry estimate across years for Eurostoxx, plus average**: yearly seasonal estimates are aligned to an arbitrary common x-axis (2001 was used only as a reference). Thin lines are individual years; the thick line is the day-by-day across-year average. It shows an apparently positive seasonal component while holding March (mid-December to mid-March), but this is known to be incorrect because the calculation compares March with June.
- **Figure 62 — Average seasonal component for Eurostoxx: original and shifted**: compares the original average seasonal component with the version shifted by three months, the approximate quarterly-roll interval, to obtain a more accurate estimate.
- **Figure 63 — Net carry forecast without seasonal component for Eurostoxx**: shows raw carry after subtracting the original, unshifted seasonal average. Some seasonal patterns remain, but they vary year to year and are not easily predictable.
- **Figure 64 — Raw carry forecast before and after seasonal adjustment**: shows the final adjusted forecast after adding the shifted seasonal component back.

## Evaluation of seasonal adjustment

The test used a restricted Jumbo portfolio: only instruments trading the nearest contract; excluding FX and metals because their carry seasonality was not predictable; and requiring at least three years of data. The resulting sample was 57 instruments: 35 equities, 20 bond markets, one agricultural market, and one energy market.

The three tested variants were (1) original raw carry with incorrect seasonality, (2) net raw carry with seasonality removed, and (3) raw carry with shifted seasonal component added back.

| Metric | Original raw / incorrect seasonality | Net raw / no seasonality | Adjusted raw / correct seasonality |
|---|---:|---:|---:|
| Mean annual return | 11.3% | 10.6% | 9.9% |
| Costs | −0.6% | −0.6% | −0.6% |
| Average drawdown | −18.5% | −18.3% | −19.7% |
| Standard deviation | 19.2% | 19.3% | 19.4% |
| Sharpe ratio | 0.59 | 0.55 | 0.51 |
| Turnover | 15.5 | 15.0 | 17.1 |
| Skew | 0.06 | 0.02 | 0.06 |
| Lower tail | 1.83 | 1.80 | 1.80 |
| Upper tail | 1.68 | 1.67 | 1.70 |
| Alpha | 6.8% | 6.5% | 5.8% |
| Beta | 0.18 | 0.17 | 0.17 |

The result was slightly worse performance after the extra adjustment. A more complex seasonal-extraction method might improve it, but the chapter's practical recommendation for someone uncomfortable with incorrect seasonality is to omit the carry rule for affected instruments or use spot if available.

### Backtest warning and refinement

An exponentially weighted moving average can improve the seasonal methodology by weighting recent years more heavily; the author uses a five-year span. In a backtest, seasonal adjustments should be recalculated annually using only backward-looking information.

## Fixed seasonal instruments: long-horizon carry

For some commodities the position holds the same contract month every year, which removes seasonality from the price. This requires sufficient liquidity far enough out on the curve. Named examples are full-sized Corn, WTI Crude Oil, Soybeans, and Wheat.

The usual version compares the held contract with a nearer contract. Example: in late December 2022, holding December 2023 Wheat, compare it with September 2023; before September expires, roll to December 2024 so the carry comparison remains September versus December 2024.

This is accurate only relative to the intended holding horizon. Consider the stated illustrative curve:

| Point on curve | Price | Maturity from mid-December 2022 |
|---|---:|---|
| Spot | $900 | immediate |
| March 2023 | $880 | 3 months |
| May 2023 | $860 | 5 months |
| September 2023 | $820 | 9 months |
| December 2023 | $840 | 12 months |

Although September is below December, producing a negative forecast from that segment of an upward-sloping curve, the spot, March, and May prices are all above December. The source notes this resembles the actual Wheat curve when the chapter was written, though its figures were simplified and the carry magnitude enlarged.

Under the unchanged-curve assumption:

- Mid-December to March: December 2023 ages from 12 to 9 months and moves from $840 to $820: negative carry, correctly signalled as negative.
- March to May: it ages from 9 to 5 months and moves from $820 to $860: positive carry, correctly signalled as positive.
- May to September: it ages from 5 to 3 months and moves from $860 to $880: positive carry, correctly signalled as positive.

Total carry over the year is positive $40. The nearer-contract comparison makes sense for an initial position held fewer than three months and closed by mid-March, because the forecast and earned carry align. For a one-year-or-longer horizon, a positive estimate reflecting the entire year would be more sensible.

The proposed long-horizon modification is to compare the held contract with the **current front contract**, rather than the prior/nearer contract:

\[
\text{Raw carry}=\text{price of nearest futures contract}-\text{price of current futures contract}.
\]

For the example, it produces a positive forecast from December to March (even while realised carry in that segment is negative), and positive forecasts from March to May and May to September, aligning with the whole-year positive result. This modification did not improve performance in a test of five instruments with fixed annual holding months. The sample is too small for firm conclusions, but the author notes that even the slowest carry rules usually hold positions only a few months, which may explain the result.

## Trading plan / decision rules

| Instrument situation | Examples named | Action |
|---|---|---|
| Variable held contract that is not nearest | Volatility, short-term interest rates, many commodities | No adjustment needed. |
| Nearest contract, no predictable carry seasonality | FX and metals | No adjustment possible. |
| Nearest contract; seasonal; synchronised, good-quality spot available | Equity indices and some commodities | Replace `current futures − next contract` raw carry with `spot − current futures`. |
| Nearest contract; seasonal; no spot available | German and Spanish bond futures, equity indices, some commodities | Either remove seasonal component from raw carry, or add shifted seasonal component for a more accurate seasonal raw-carry estimate. |
| Fixed contract month each year (for example December) | Full-sized Corn, WTI Crude Oil, Soybeans, Wheat | Change from `nearer futures − current futures` to `nearest futures − current futures`. |

## Constraints, common errors, and takeaways

- Do not treat current-to-next contract carry as realised front-month carry when curve gradients vary.
- Do not assume every variation can be seasonally corrected: FX and metals are specifically excluded where predictable seasonality is absent.
- Synchronise spot and futures data before using spot-based carry.
- Do not use annual averages based on insufficient data; the stated minimum is three years.
- Treat leap day explicitly: substitute the 28 February seasonal average for 29 February.
- Avoid look-ahead bias: recompute backtest adjustments annually with only historical information.
- Align the carry measure with expected holding horizon. A short-horizon contract-pair comparison can be appropriate even when it disagrees with a full-year result.
- The empirical findings in this chapter do **not** support an improvement from either seasonal adjustment or fixed-month long-horizon carry modification in the author's tests.

## Glossary candidates

Carry; raw carry; annualised raw carry; carry forecast; front month; futures curve; curve gradient; spot price; volatility normalisation; seasonal carry component; net carry; shifted seasonal component; cheapest-to-deliver bond; conversion factor; duration; roll interval; fixed seasonal contract; Jumbo portfolio; turnover; lower tail; upper tail; alpha; beta.

## Explicit connections to other chapters

- **Strategy Ten (Basic Carry):** introduced the two ways of measuring futures carry and the front-month issue addressed here.
- **Part One:** supplied the basic trend-trading rules whose later refinements frame this part of the book.
- **Any strategy with carry trading rules:** Strategy Fifteen's adjustments are designed to be applied as a variation.
