# Strategy One: Buy and Hold, Single Contract

## Scope and central argument

This chapter establishes the simplest futures strategy: hold one futures contract continuously, rolling it before expiry. It uses the S&P 500 micro future as the main worked case, then applies the same framework to US 10-year bonds, WTI crude oil, and VIX futures. Its central claim is that positive long-run returns should come from accepting risks other traders are unwilling or unable to bear—not from a secret predictive pattern—and that this only makes sense when the risk, implementation costs, capital, and backtest limitations are explicitly measured.

The strategy can be lucrative in the right instrument, but choosing that instrument ex ante is difficult. A single-contract position also leaves substantial concentration, volatility, negative-skew, and fat-tail risk. The chapter treats the resulting return series as the raw material that later strategies aim to improve.

## Strategy specification

| Item | Chapter specification |
|---|---|
| Instrument | Any future expected to deliver a positive risk premium. The strategy-plan graphic says to go short instruments such as volatility when their risk premium is negative. |
| Position | One contract, held continuously. |
| Trading | Opening trade plus rollovers; contracts cannot simply be held through expiry. |
| Capital | Current notional exposure per contract: `multiplier × price × FX rate`. |
| Return basis | Excess return only: price and carry effects, excluding interest earned on cash in the trading account. |

The chapter's guiding distinction is between *blind* risk taking and quantified, adequately compensated risk taking. It identifies avoidable errors as excessive trading costs, excessive leverage, and rules that assume the future will closely replicate the past (over-/curve-fitting).

## Futures mechanics and implementation

### Multiplier, notional exposure, and ticks

For the S&P 500, the chapter lists two CME contracts:

| Contract | Symbol | Multiplier / “contract unit” | Minimum price fluctuation | Tick value |
|---|---:|---:|---:|---:|
| E-mini | ES | $50 per index point | 0.25 points | $12.50 |
| Micro e-mini | MES | $5 per index point | 0.25 points | $1.25 |

The worked strategy uses the micro. A move from 4,500 to 4,545 produces `45 × $5 = $225` for one micro, or `45 × $50 = $2,250` for one e-mini.

\[
\text{Notional exposure per contract (instrument currency)} = M P
\]

\[
\text{Notional exposure per contract (base currency)} = M P X
\]

\[
\text{Tick value} = M \times \tau
\]

Where `M` is the futures multiplier (currency per price point), `P` is futures price (price points), `X` is the relevant exchange rate in base-currency units per instrument-currency unit, and `τ` is tick size (price points). The formula assumes a fixed multiplier; the chapter flags that a small number of futures have variable multipliers.

Example: at 4,500, one e-mini has `$50 × 4,500 = $225,000` notional exposure. For a UK account at `$1 = £0.75`, this is `$50 × 4,500 × 0.75 = £168,750`.

### Expiry, contract choice, and rolling

S&P 500 micro futures expire quarterly (March, June, September, December). At the 9 September 2021 example, September is the front month and most liquid (119,744 volume; 123,856 open interest), but expires in eight days. The chapter therefore opens the reasonably liquid December contract at its offer, 4,494.25.

The rule of thumb used here is: **roll five days before expiry of the front month**, when both the front and second contract months are reasonably liquid. For the December 2021 contract (expiry 17 December), five days before falls on Sunday 12 December, so the example rolls on Monday 13 December. A roll sells the held contract and simultaneously buys the next one, preserving exposure.

| 13 Dec 2021 order book | Bid | Offer | Mid | Volume | Open interest |
|---|---:|---:|---:|---:|---:|
| Dec 2021 | 4,706.25 | 4,706.50 | 4,706.375 | 119,744 | 123,856 |
| Mar 2022 | 4,698.00 | 4,698.25 | 4,698.125 | 64,432 | 35,212 |
| Jun 2022 | 4,690.50 | 4,691.00 | 4,690.750 | 12 | 227 |

The example closes December by hitting 4,706.25 and opens March by lifting 4,698.25. A *calendar spread* can instead execute the two legs together between expiries, potentially at lower spread cost and without exposure to an underlying-price move during the roll. The chapter conservatively models separate orders. Its footnote says a one-tick micro S&P calendar spread could cost 0.0025 index points, or $0.0125 per contract, but the detailed rolling methodology is deferred to Part Six.

### Trading costs and the worked roll calculation

Trading costs comprise:

- **Commission**: fixed per contract; $0.25 for the micro S&P in the example.
- **Spread cost**: the difference between execution price and the mid price—the price that would apply absent a bid-offer spread.

For December at 4,494.00 bid / 4,494.25 offer / 4,494.125 mid, buying at the offer costs `4,494.25 − 4,494.125 = 0.125` points. At `$5` per point, this equals `$0.625`. Thus an initial trade costs `$0.25 + $0.625 = $0.875`.

If the bid-offer is one tick wide, spread cost is half a tick value; a two-tick bid-offer costs one tick value. This simple assumption only applies to an order small enough to fill at the top of a liquid order book under normal spreads. Larger institutional orders face potentially higher spread costs and market impact.

Worked December leg: bought at 4,494.25, sold at 4,706.25. Gross gain is `(4,706.25 − 4,494.25) × $5 = $1,060`. Less the $0.25 initial commission and $0.25 closing commission gives `$1,059.50` net (the original exposition’s first decomposition).

Equivalent decomposition: `$0.875` initial spread-plus-commission cost, holding profit from mids of `(4,706.375 − 4,494.125) × $5 = $1,061.25`, and `$0.875` close/roll cost. This yields the same net. Generalized, total P&L is (1) costs of initial/non-roll trades, (2) costs of all roll trades, and (3) mid-price P&L while each contract is held. The separation is essential because expiring contracts otherwise create artificial price jumps.

## Back-adjusted prices, spot, carry, and excess return

Daily closes for each expiry are used for the initial tests. *Back-adjustment* constructs a continuous series for constantly holding and rolling one contract while deliberately excluding trading costs.

At the December-to-March roll, the mid prices are 4,706.375 and 4,698.125: a raw stitched series would fall 8.25 points and falsely show a long loss. At mid-market, selling December and buying March generate no immediate P&L; only the notional value changes. Therefore, a back-adjusted price must be unchanged across a roll with no actual market movement. The procedure subtracts the roll differential ($8.25 in the example) from all prior December prices, joins adjusted December through the roll date to actual March after it, and repeats backwards through history.

The chapter names this the simple **Panama** back-adjustment method. Its final adjusted price equals the final raw futures price by construction. Forward adjustment instead holds the earliest adjusted price equal to the earliest contract and requires less historical rewriting; the chapter says either method gives the same strategy results, though forward-adjusted final values may differ materially from the current futures price. Avoid unadjusted stitched third-party series, and understand any vendor methodology; bought adjusted data also removes flexibility to test different roll choices.

### Figures 1–2: what the S&P price plots show

- **Figure 1** overlays raw expiry-price segments with the grey back-adjusted S&P micro series. They overlap at the end; the adjusted series is below raw prices early on, then outpaces them after roughly 2008.
- **Figure 2** plots their difference. Apart from noise attributed to roll timing and data frequency, it indicates rolling losses before 2008 and rolling gains afterward.

The chapter frames this through the following return identities:

\[
\text{Total return}=\text{spot return}+\text{dividends}
\]
\[
\text{Excess return}=\text{total return}-\text{interest}=\text{spot return}+\text{dividends}-\text{interest}
\]
\[
\text{Excess return}=\text{spot return}+\text{carry}
\]

Here *carry* is the component `dividends − interest` in this equity-futures example. The no-arbitrage explanation supplied is that futures price reflects spot plus expected dividends before expiry less borrowing interest. Before 2008, dividends were below interest rates, making carry negative; after rates fell more than dividends, carry became positive (briefly interrupted by rate rises in 2016–19). Thus an adjusted futures series contains both spot and carry returns.

An adjusted futures series is **not** a total-return series: it is cumulated *excess* return, with interest cost deducted. Interest on trading-account cash is excluded because it varies with chosen leverage and is not part of the strategy.

## P&L and return calculation

For position `N_t` (positive long, negative short) and back-adjusted price `P_t`, the chapter gives:

\[
R^{\mathrm{points}}_t=N_{t-1}(P_t-P_{t-1})
\]
\[
R^{\mathrm{inst}}_t=R^{\mathrm{points}}_t M
\]
\[
R^{\mathrm{base}}_t=R^{\mathrm{inst}}_t X_t
\]

`R^points_t` is period return in price points; `R^inst_t` is return in the futures instrument currency; `R^base_t` is return in account base currency; `M` is multiplier; and `X_t` is the instrument-to-base exchange rate. The price and position series must be aligned so the prior period’s position earns the price movement. For this simple strategy, `N_t = 1` throughout, so cumulated price-point return from time 0 through `T` is `P_T − P_0`.

UK-account example: with `N=1`, price moving 4,500 to 4,545, `M=$5`, and `$1=£0.75`, the return is 45 points, then `$225`, then `£168.75`.

The cumulative sum of `R^base_t` is the strategy’s cumulative profit, also called an **account curve**. Figure 3 shows this for a US-dollar trader long one S&P micro: it is the adjusted-price series scaled by the multiplier and rebased to zero, producing total profit above $200,000. The text later inconsistently refers to “$24,000 in just over 40 years” when discussing Figure 3; this apparent contradiction is retained as an unresolved source inconsistency.

For a 40-year S&P test with four rolls annually and modeled $1.75 per roll (two $0.875 trade legs), estimated roll costs are `4 × 40 × $1.75 = $280`, plus optional $0.875 initial and final costs. The chapter cautions that assuming the same cost in 1982 as now may be unrealistic and defers treatment of historical costs.

## Backtesting: use and limitations

A **backtest** is a test of a strategy on historical data. It serves two purposes: choose what to trade (strategies, instruments, risk allocations) and understand how a strategy behaves (trading frequency, costs, leverage), not merely rank profitability.

There is a tension between reproducing what was knowable in the past and measuring the behavior of the strategy one will actually trade. In the chapter’s A-versus-B illustration, a historically realistic test begins with both strategies and shifts toward B only as backward-looking evidence accumulates. Testing only the ultimately selected B is **in sample** and involves **fitting**, so its return is necessarily higher than the no-foresight version.

Selecting B can be necessary to understand B, but risks **overfitting**: noisy financial data rarely justify replacing A entirely because it performed only somewhat better. Choosing the single best day (26 January) or instrument (EUR/USD) based only on backtest performance illustrates this error. A more robust process maintains allocations to both strategies, tilts toward the better one as evidence accrues, then can run a fixed-weight behavior test; even that fixed-weight test is somewhat overstated.

Use results only when significant and logically explicable; unexplained findings may be **data-mining**. Automated historical fitting that sees only prior data reduces hindsight, but every backtest should still be presumed to overstate future achievement. Known non-repeatable trends are another issue: the chapter flags falling US policy rates from above 10% in 1980 to 0.25% at writing as a major boost to historical bond results that should not drive an all-long-bond allocation.

## Capital and percentage returns

Dollar P&L requires capital context. With no leverage, a micro-like $5 exposure at an S&P index of ~109 originally needs `$545`; at ~4,500 it needs `$22,500`. The stated micro initial margin is $1,150, which implies almost 20:1 leverage on ~$22,500 notional. That is insufficiently cautious because adverse moves require **variation margin**: at `$5` multiplier, each point against the position requires an additional $5. If cash is not available, the broker may liquidate the position.

For this chapter’s performance comparisons, required capital equals the full current notional exposure: effectively no leverage. It is an intentionally conservative rule for a long position—enough to survive a move to zero—and is not asserted to be generally necessary. A short position technically needs unlimited cash for all eventualities. Strategy two will alter capital for asset risk.

\[
r_t=100\times\frac{R^{\mathrm{base}}_t}{C_{t-1}}
\]

`r_t` is the percentage return in percent, `R^base_t` is period base-currency P&L, and `C_{t-1}` is prior-day required capital in base currency. Using prior-day capital avoids dividing the day’s profit by capital after the price move. Figure 4 overlays S&P cumulative dollar P&L and required capital (current futures price × multiplier); their close tracking follows from their construction. Figure 5 shows daily percentage returns, visibly including the 1987, 2008, and lesser 2020 shocks. Figure 6 cumulatively **sums** daily percentage returns, reaching nearly 250% over more than 40 years; this makes early history more visible than dollar P&L.

The conventional compounded plot would use `∏(1+r_t)` with decimal returns, but the chapter uses summed returns because compounding again obscures early moves. A logarithmic dollar-P&L plot would look similar to Figure 6 on another scale. It does not use CAGR here because returns are not compounded; the reason is deferred to Strategy Two.

## Performance assessment

### Annual return and risk

Mean daily S&P return is 0.0235%. Assuming 256 business days gives `0.0235% × 256 = 6.02%` annualized. The 256 convention approximates 365 minus 104 weekend days and holidays; it is chosen partly because `√256 = 16`.

Risk-adjusted rather than outright returns are required because leverage scales both return and risk. The preferred primary risk measure is the **standard deviation of returns**, a symmetric metric. The chapter’s reasons: it uses all data and is more robust to occasional outliers; daily upside can become downside on the next coin-flip-like move; and a symmetric measure does not change simply because the futures position is long versus short.

For returns `r_1 … r_T`:

\[
r^*=\frac{1}{T}\sum_{t=1}^{T}r_t
\]
\[
\sigma=\sqrt{\frac{1}{T}\sum_{t=1}^{T}(r_t-r^*)^2}
\]

`r*` is mean return, `T` number of observations, and `σ` standard deviation at the same frequency as the returns. The text presents the population-style divisor `T`. Under zero autocorrelation and a symmetric, well-behaved distribution, `σ_annual = σ_daily √256 = 16σ_daily`. S&P daily `σ=1.2%` becomes 19.2% annualized, whereas directly measured annual standard deviation is 17.2%.

Annualization can mislead. Negative autocorrelation (alternating +$1/-$1) makes annualized daily volatility too high; clustered/uneven outcomes (daily +$1 then final-day ±$364) make it too low (`$304` annualized daily versus `$364` direct annual). Daily annualization is nevertheless preferred because it uses many more points, subject to this warning.

**Drawdown.** Maximum drawdown is the greatest cumulative loss at any point; mean return divided by maximum drawdown is the Calmar ratio. The chapter does not favor it as primary risk because it relies on one observation, changes with sample length, and can falsely suggest the historical worst loss is a ceiling. It reports **average drawdown** instead: calculate current drawdown on every day and take their mean.

### Sharpe ratio, skew, and tails

\[
SR=\frac{\text{mean return}-\text{risk-free rate}}{\sigma}
\]

Because the chapter uses excess returns, it uses `SR = mean excess return / σ`. Mean and standard deviation must have the same frequency. For S&P: daily `0.0235% / 1.2% ≈ 0.0196`; annualized `SR = 0.0196 × √256 = 0.31`. Unless specified otherwise, quoted Sharpe ratios are annualized. Autocorrelation and distribution issues affecting volatility can also affect annualized SR.

The chapter uses **skew** separately from SR rather than relying on the Sortino ratio (which uses only negative-return deviation). Positive skew has more losing days but smaller losses and occasional large gains; negative skew has fewer losing days but larger losses. Insurance buyer versus insurer is the analogy. Negative skew may earn higher returns because it is disliked, but strongly negative skew makes symmetric-return assumptions poor and prices unstable. Monthly skew is preferred: daily/weekly estimates can be dominated by a few extreme days, and annual data offer too few observations. S&P monthly skew is −1.37.

For tails, a Gaussian six-standard-deviation daily S&P move (~7.2% at 1.2% daily σ) should occur about once per 2.7 million years, yet the chapter reports ~40 such days over the last century. It rejects kurtosis as hard to interpret (S&P monthly kurtosis 6.65), unable to distinguish good right from harmful left tails, and non-robust.

Instead, demean returns and calculate 1st, 30th, 70th, and 99th percentiles. For S&P: −3.25%, −0.28%, +0.42%, +3.04%. The 30th/70th points approximate −/+ one standard deviation; 1st/99th represent extremes. More extreme percentiles (0.1%, 99.9%) have fewer contributing observations and are less reliable.

\[
\text{Lower percentile ratio}=\frac{q_{1\%}}{q_{30\%}}=\frac{-3.25\%}{-0.28\%}=11.6
\]
\[
\text{Upper percentile ratio}=\frac{q_{99\%}}{q_{70\%}}=\frac{3.04\%}{0.42\%}=7.2
\]
\[
\text{Relative lower/upper tail}=\frac{\text{corresponding percentile ratio}}{4.43}
\]

For a Gaussian distribution, both raw ratios equal 4.43. S&P relative lower tail is `11.6/4.43=2.16`; upper tail `7.2/4.43=1.60`. Values above 1 are fatter-tailed than Gaussian in that direction. Demeaning is necessary because otherwise the 1st and 30th percentiles could have different signs and make the lower ratio negative.

## Instrument results and visuals

| Single-contract buy-and-hold result | S&P micro | US 10-year bond | WTI crude | VIX |
|---|---:|---:|---:|---:|
| Years of data | 41 | 41 | 33 | 17 |
| Mean annual return | 6.0% | 3.75% | 4.03% | −40.6% |
| Average drawdown | −23.2% | −3.90% | −66.9% | More than 100% |
| Annualized standard deviation | 19.2% | 6.39% | 27.7% | 45.9% |
| Sharpe ratio | 0.31 | 0.59 | 0.15 | −0.88 |
| Monthly skew | −1.37 | 0.15 | −0.49 | 0.96 |
| Lower tail | 2.16 | 1.49 | 1.81 | 1.34 |
| Upper tail | 1.60 | 1.36 | 1.33 | 1.96 |

**US 10-year bond future.** TN at CBOT; multiplier $1,000; tick 0.015625 (1/64); commission $0.85; stated current one-contract trading cost $8.6625; physical delivery; quarterly expiries; hold first contract until ~25 days before expiry. Figure 7 shows the back-adjusted series substantially and persistently above raw prices, attributed almost entirely to high carry; its early adjusted values are negative, which is acceptable only for strategies robust to negative numbers. Figures 8–9 show better-behaved percentage returns and cumulative results than S&P. The chapter attributes much historical profit to a secular fall in US interest rates, while saying carry persisted through flat/rising-rate periods; low tail ratios and small positive skew make returns comparatively near-normal.

**WTI crude oil.** CL at NYMEX; multiplier $1,000; tick 0.01; commission $0.85; cost $10.425; physical delivery; monthly expiry. Hold the next December contract and roll 40 days before expiry. A consistent December month aims to reduce seasonal effects and is chosen for liquidity, but this needs liquid contracts at least a year ahead and is not viable for every contract. Long roll timing supports a later carry strategy (Chapter Ten). Oil has high risk, negative skew, and a fat lower tail, but may perform under hot macro/inflation conditions, so it is presented as an inflation hedge and source of risk premium; the text also notes conflict sensitivity.

**VIX.** VX at CBOE; multiplier $1,000; tick 0.05; commission $0.85; cost $25.85; cash settlement; weekly then monthly expiries. Hold the second monthly contract (e.g., April on 1 March 2022), rolling into May in mid-March before March expiry changes the front/second-month designations. Figure 10 is the cumulative percentage-return curve: crisis gains in 2008 and 2020 but persistent decline otherwise, ultimately exceeding six times starting capital if continually funded. Long VIX buys insurance: frequent premium-like losses, occasional large gains, positive skew, and a fat upper tail, but negative long-run return. It may hedge long equities, not serve as an outright investment; later strategies generally favor short VIX.

### Asset-class medians (Tables 3–4)

| Statistic | Equity | Vol | FX | Bond | Metals | Energy | Ags | All-instrument median |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Mean annual return | 7.6% | −51.6% | −0.39% | 3.2% | −0.94% | 0.17% | −1.5% | 1.35% |
| Standard deviation | 28.9% | 64.6% | 15.0% | 6.3% | 38.3% | 43.1% | 28.8% | 23.2% |
| Sharpe ratio | 0.30 | −0.80 | −0.03 | 0.57 | −0.03 | 0.00 | −0.04 | 0.13 |
| Skew | −0.78 | 0.73 | −0.18 | 0.11 | −0.50 | −0.38 | 0.21 | −0.38 |
| Lower tail | 1.98 | 1.29 | 1.65 | 1.62 | 1.86 | 1.72 | 1.54 | 1.74 |
| Upper tail | 1.39 | 1.92 | 1.42 | 1.47 | 1.41 | 1.32 | 1.45 | 1.40 |

Each asset-class statistic is the median across eligible instruments, and the final column is the median across all instruments; median is chosen as more robust to extreme outliers than mean. Eligible instruments have at least one year of data and meet later-discussed liquidity/cost requirements. Positive adjusted returns appear only in bonds and equities; volatility is very poor. Bonds are safest (~6% annualized risk); FX is also relatively low-risk; equities and commodities are risky; most classes have negative skew, while equity lower tails are especially fat. These medians hide substantial within-class variation.

## Warnings, boundaries, and explicit connections

- This is not passive cash-equity buy-and-hold: futures expire and must be rolled.
- Back-adjustment omits actual trade costs; costs must be added separately, and past costs may differ from current ones.
- Adjusted price series should not be used for magic-number/Fibonacci or round-number rules, because market participants use actual prices and a roll changes the raw price absent a meaningful market move. The chapter prefers adjusted prices because positions remain consistent through rolls.
- Full-notional capital is a deliberately conservative chapter assumption, not a universal margin rule. Initial margin alone can lead to liquidation after adverse movement.
- Standard-deviation and annualized-Sharpe estimates rely on assumptions that can fail through autocorrelation and non-normal/uneven return patterns.
- Maximum drawdown is not a reliable loss ceiling. Historical data may omit catastrophic events; the chapter cites the 1987 one-day equity loss as an example of an “impossible” event exceeding prior-history expectations.
- Tail measures need adequate data; very extreme percentiles reduce reliability.
- Do not extrapolate historical bond success driven by falling rates. Do not treat selection made with future knowledge as achievable historical performance.

Explicit forward connections: Strategy Two will risk-adjust the capital requirement and explain non-compounding; Part Six covers roll/contract selection and calendar spreads; Chapter Ten returns to carry-based oil rolling; later strategies use estimated skew, improve return/risk/skew/drawdown, and generally bias short VIX. Appendix B explains back-adjustment, Appendix A names data providers, Appendix C lists instruments.

## Glossary

**Backtest:** historical test of a trading strategy.  
**Back-adjustment / Panama method:** adjusts prior futures prices by roll differentials so rolling creates no artificial P&L jump.  
**Base currency / instrument currency:** account denomination / currency in which the future’s P&L is expressed.  
**Carry:** excess-return component beyond spot return; in the S&P discussion, dividends minus interest.  
**Calendar spread:** a combined buy/sell trade between expiries of the same future.  
**Drawdown:** cumulative loss from a prior peak; average drawdown is the mean current drawdown across days.  
**Excess return:** total return less interest; the return basis used throughout this chapter.  
**Front month:** nearest-expiring futures contract.  
**Futures multiplier:** currency value per one price-point movement.  
**In-sample fitting / overfitting:** selecting or tuning with future-aware historical results; overfitting gives noise undue weight.  
**Initial and variation margin:** cash required to open a futures trade / additional cash required after losses.  
**Notional exposure:** price × multiplier (and FX conversion where relevant), the effective underlying-value exposure.  
**Open interest / volume:** outstanding positions / contracts traded in the stated period.  
**Risk premium:** expected compensation for bearing an undesired or constrained risk.  
**Sharpe ratio:** mean excess return divided by standard deviation of returns.  
**Skew:** asymmetry of returns; negative skew means relatively infrequent but larger losses.  
**Spread cost:** execution price minus mid-market value, expressed in price or currency.  
**Tick size / tick value:** smallest permissible price increment / its currency value per contract.  
**Upper and lower tail ratios:** relative extremity of high and low returns versus a Gaussian benchmark.

## Chapter conclusion

Single-contract buy-and-hold futures can produce attractive returns if the right future is selected, but hindsight does not make that selection reliable. Instruments can carry high volatility, negative skew, and fat tails even when historical risk-adjusted returns look good. The chapter’s practical contribution is a consistent way to roll contracts, create a cost-free continuous excess-return series, apply costs and capital, and judge returns with more than one statistic before attempting more sophisticated, diversified, and risk-controlled strategies.
