# Strategy Thirty: Calendar Trading Strategies

## Purpose and central argument

This chapter moves relative-value (RV) trading **within one futures market**, using different expiries of the same instrument rather than different instruments. A calendar spread or triplet is usually easier to construct and execute than a cross-instrument RV trade: expiry relationships are relatively stable, a combination can often be traded as one order, and all legs share the same futures multiplier and FX rate. The trade-off is that nearby expiries tend to be very highly correlated. That lowers the synthetic instrument's measured volatility but demands high gross leverage and creates fat-tailed, non-Gaussian returns.

The tested implementations—EWMAC16 trend and carry60—are not especially profitable in the presented examples. Calendar prices tend to mean-revert steadily around an equilibrium, interrupted by sharp crisis-driven shifts to a new equilibrium. Trend therefore resembles option buying: long, gradual losses punctuated by large profits. The author suggests testing the combined mean-reversion/trend method from strategy twenty-seven, but does not test it here.

## What is traded

### Synthetic calendar instruments

Use back-adjusted prices from different expiries of the **same underlying futures instrument**.

- **Long calendar spread:** long expiry `a`, short expiry `b`.
- **Long calendar triplet (or triple):** long expiries `a` and `c`, short expiry `b`.
- Maturity order is `a` before `b` before `c`. `a` may be the front contract or a later contract. Expiries may be adjacent or farther apart.
- A spread is a bet on the **steepness** of the futures curve; a triplet is a bet on its **convexity**.

All individual legs must be rolled **simultaneously** to retain the intended distance from expiry. Rolling the first leg of an adjacent spread into the second leg's month without rolling the second leg means the position is no longer a spread. The roll itself is a spread trade.

### Liquidity constraint and examples

The market must support positions in at least two (spread) or three (triplet) liquid expiries at once. In the chapter's contemporaneous US 10-year example, the September 2022 expiry had only 3% of June's volume/open interest, and December had open interest of 34, making a triplet impractical. The author says this rules out bond futures, equity indices, metals, and FX, leaving STIR, volatility, and much of energy/agriculture.

The examples are VIX volatility futures, Eurodollar STIR futures, and WTI Crude. They are examples rather than claimed uniquely attractive markets. All have a volatility term structure; WTI also has seasonal effects.

| Instrument / structure | `a` | `b` | `c` | Roll cycle |
|---|---|---|---|---|
| Eurodollar spread | 8th quarterly (Jun 2024) | 10th quarterly (Dec 2024) | — | Quarterly |
| Eurodollar triplet | 8th quarterly (Jun 2024) | 10th quarterly (Dec 2024) | 12th quarterly (Jun 2025) | Quarterly |
| WTI spread | 2nd monthly (Jun 2022) | 8th monthly (Dec 2022) | — | Monthly |
| WTI triplet | 2nd monthly (Jun 2022) | 8th monthly (Dec 2022) | 14th monthly (Jun 2023) | Monthly |
| VIX spread | 3rd monthly (Jul 2022) | 4th monthly (Aug 2022) | — | Monthly |
| VIX triplet | 2nd monthly (Jun 2022) | 3rd monthly (Jul 2022) | 4th monthly (Aug 2022) | Monthly |

Dates were stated as correct on 1 May 2022. WTI uses the second contract so carry can compare the traded contract with a nearer one; positions are rolled before that first traded contract expires. The VIX spread uses third/fourth contracts. Specifying WTI by fixed calendar month (as in the standalone December contract example) would remove seasonal effects, but the author deliberately retains them here.

## Price construction and hedge conventions

Let `p_a`, `p_b`, and `p_c` be the back-adjusted prices of expiries `a`, `b`, and `c` in price points.

| Structure | General synthetic price | Calendar convention |
|---|---|---|
| Spread | `p^Δ = R p_a − p_b` | `p^Δ = p_a − p_b` (`R = 1`) |
| Triplet | `p^Ω = X p_a + Y p_c − p_b` | `p^Ω = 0.5 p_a + 0.5 p_c − p_b` (`X = Y = 0.5`) |

For a cross-instrument spread, the estimated hedge ratio is `R* = σ_b / σ_a`, where `σ_a` and `σ_b` are standard deviations of daily price changes. If they are identical, `R* = 1`. Calendar spread markets conventionally set `R = 1`, enabling quoted combination trades and lower execution risk/cost versus legging. This is not necessarily optimal: unequal volatility across maturities produces an imperfect hedge and more outright-market correlation.

For the general triplet, `X = ρ_{a,b} σ_b / (2σ_a)` and `Y = ρ_{b,c} σ_b / (2σ_c)`. Equal pairwise correlations plus equal standard deviations imply `X = Y = 0.5`, the calendar-market convention.

`ρ_{a,b}` and `ρ_{b,c}` are the corresponding correlations of price changes/returns. The chapter notes the Samuelson effect: futures volatility is theoretically expected to rise as maturity approaches, which occurs in many markets (clearly in VIX) but is not universal—front STIR expiries were extremely low volatility during much of the effectively fixed-rate 2010s.

## Risk, sizing, and minimum capital

### Daily volatility and annualisation

For either synthetic price `p` above, estimate daily price-change standard deviation as:

`σ_p = standard deviation(p_t − p_{t-1}, p_{t-1} − p_{t-2}, …)`

The chapter directs the reader to Part One's exponential weighting and long-run-average method. Annualised price volatility is `σ_p × 16` (the book's annualisation convention).

### Base-leg position

The base expiry `b` position is:

`−N_{b,t} = −(Scaled forecast_t × Capital × Weight × IDM × τ) / (10 × Multiplier × FX × σ_p × 16)`

Thus a positive forecast creates a short base-leg position for a long synthetic spread/triplet. `N_{b,t}` is contracts of expiry `b` at time `t`; `Scaled forecast_t` is the scaled trading forecast; `Capital` is account capital in base currency; `Weight` is the instrument weight; `IDM` is the instrument-diversification multiplier; `τ` is annualised risk target; `Multiplier` is futures currency value per price point; `FX` converts the contract currency to base currency; and `σ_p` is daily standard deviation of the synthetic price in price points. The recommended RV `τ` is **10%**.

For a calendar spread, equal multiplier/FX and `R=1` simplify the other leg to:

`N_{a,t} = N_{b,t}`

So one long synthetic unit is short one `b` and long one `a`.

For a calendar triplet:

`N_{a,t} = 0.5 N_{b,t}`  
`N_{c,t} = 0.5 N_{b,t}`

Because half contracts cannot be held, the smallest effective triplet position is two synthetic units: short 2 `b`, long 1 `a`, long 1 `c`.

### Worked VIX sizing example

Assumptions: capital `$500,000`, `τ=10%`, one traded instrument (`Weight=IDM=1`), scaled forecast `+10`, and VIX multiplier `$1,000` per point.

- Spread: `σ_p=0.277`; the formula gives `−N_b = −11.2`. Hold short 11.2 contracts of `b`, long 11.2 of `a`.
- Triplet: `σ_p=0.0829`; the formula gives `−N_b = −37.7`. Hold short 37.7 `b`, long 18.9 `a`, and long 18.9 `c`.
- Directional outright VIX expiry `b`: daily price-return standard deviation `0.86`; optimal position `3.63` contracts.

| Position at the stated assumptions | `a` | `b` | `c` | Total absolute notional exposure |
|---|---:|---:|---:|---:|
| Eurodollar outright | — | 13 | — | $3.2m |
| Eurodollar spread | +70 | −70 | — | $17.3m |
| Eurodollar triplet | +120 | −240 | +120 | $118m |
| VIX outright | — | 3.63 | — | $104,000 |
| VIX spread | +11.2 | −11.2 | — | $640,000 |
| VIX triplet | +18.9 | −37.7 | +18.9 | $2.15m |
| WTI Crude outright | — | 1 | — | $100,000 |
| WTI Crude spread | +2.23 | −2.23 | — | $446,000 |
| WTI Crude triplet | +2.16 | −4.33 | +2.16 | $866,000 |

Moving from outright to spread raises leverage about fivefold in each example. From spread to triplet, leverage multiplies roughly sevenfold for Eurodollar, threefold for VIX, and less than twice for Crude. Correlations `a`/`b` are 0.94 Crude, 0.98 Eurodollar, 0.99 VIX. `b`/`c` is similar for VIX/Eurodollar but only 0.88 for Crude; hence the Crude triplet is riskier and needs less leverage. Adjacent Eurodollar quarterlies or adjacent Crude monthlies would make correlations still closer to 1 and substantially raise required leverage.

### Minimum capital

For a four-contract minimum spread position:

`Minimum capital = (4 × Multiplier × FX × σ_p × 16) / (IDM × Weight × τ)`

For a triplet, double this result because the required `a` and `c` positions are half of `b` and contracts are indivisible. Eurodollar examples:

- Spread: `σ_p=0.018`, multiplier `2,500` → `$28,800`.
- Triplet: `σ_p=0.0052` → formula result `$8,320`, then doubled → **$16,640**.

## Execution costs

Calendar combinations can normally be traded directly, rather than by separately trading legs. For a quoted bid–offer width in price points:

| Quantity | Spread (2 legs) | Triplet (3 legs) |
|---|---|---|
| Combination cost, price points | `(Bid − Offer) / 2` | `(Bid − Offer) / 2` |
| Combination cost, currency | `2 × Multiplier × cost_price_points` | `3 × Multiplier × cost_price_points` |
| Cost per synthetic contract | combination cost + `2 × commission per contract` | combination cost + `3 × commission per contract` |

Risk-adjusted cost per trade for either structure:

`Risk-adjusted cost = Cost per contract / (σ_p × 16 × Multiplier)`

VIX example: outright minimum tick is 0.05; VIX spread tick is 0.01. With bid and offer 0.01 apart, half-spread cost is 0.005 points; currency cost is `2×1000×0.005=$10`; adding two `$2.20` commissions gives `$14.40`; dividing by `0.277×16×1000` gives risk-adjusted cost `0.0032`.

## Carry calculation

Use the book's cross-instrument RV carry approach with fixed weights: `R=1` for spreads and `X=Y=0.5` for triplets. Superscripts indicate contracts used to calculate carry, not powers.

### Spreads

If current and further contracts are available:

`Raw carry = (p_a^current − p_b^current) − (p_a^further − p_b^further)`

If the traded expiries are not front contracts (the relevant case for all three examples):

`Raw carry = (p_a^nearer − p_b^nearer) − (p_a^current − p_b^current)`

For adjacent VIX monthly expiries, `b`'s nearer contract is `a`'s current contract, so:

`Raw carry_adjacent = p_a^nearer − p_b^nearer − p_a^current + p_b^current = p_a^nearer + p_b^current − 2p_a^current`

### Triplets

Using current/further contracts:

`Raw carry = (0.5p_a^current + 0.5p_c^current − p_b^current) − (0.5p_a^further + 0.5p_c^further − p_b^further)`

Using nearer/current contracts (used for VIX, WTI, and Eurodollars):

`Raw carry = (0.5p_a^nearer + 0.5p_c^nearer − p_b^nearer) − (0.5p_a^current + 0.5p_c^current − p_b^current)`

The chapter says the formula further simplifies for adjacent expiries such as VIX, but does not print that expanded form.

## Selecting market and expiries

Consider minimum capital and trading costs, and put little or no weight on an outright strategy's performance. Make two distinct decisions:

1. How far along the curve expiry `a` should be.
2. How much distance should separate `a`, `b`, and (if used) `c`.

The first is the same contract-selection problem as an outright directional strategy: ensure liquidity and consider the Part Six contract-selection factors. The second is primarily a correlation choice. Closer expiries mean higher correlation and lower synthetic-price standard deviation/minimum capital, but **much higher leverage and risk-adjusted costs**, plus somewhat “hideous” tail ratios.

VIX uses second/third/fourth contracts because liquidity deteriorates farther out; the first is avoided because carry cannot be computed and its tails are unattractive. Eurodollar and Crude allow years of liquid maturities, so the author spaces expiries to reduce correlation. An adjacent-quarters Eurodollar triplet at `$500,000` capital would have required notional exposure in the billions.

## Price behaviour and figures

- **Figures 89–91:** VIX, WTI Crude, and Eurodollar calendar spread prices. Each spends long periods near an equilibrium, then a crisis shocks it to a new level. WTI stayed near `$6` for years, went sharply negative during the 2020 COVID-19 Crude bear market, slowly returned near `$6`, then became more volatile around Russia's early-2022 invasion of Ukraine.
- **Figure 92:** VIX calendar triplet price. It becomes visibly spikier when hourly data begins after 2013. It mean-reverts around about `$4` in a stable interval, with adjustment periods before and after.
- **Figure 93:** cumulative percentage return of the WTI calendar-spread EWMAC strategy. Trend loses during extended mean-reversion but makes sharp profits during crises. Returns are less Gaussian than directional WTI: high positive skew and tails, and apparent risk-target undershooting when assessed using an inappropriate standard deviation measure.
- **Figure 94:** cumulative percentage return of the VIX calendar-triplet EWMAC strategy. Returns are decent until 2013; subsequent stable mean reversion leads to gradual trend losses.

## Tested results

All statistics below are the source's reported results. The final correlation row compares the strategy on the synthetic calendar instrument with the same rule traded directionally on expiry `b`.

### Calendar spreads: EWMAC16

| Metric | VIX | WTI Crude | Eurodollar |
|---|---:|---:|---:|
| Mean annual return | −1.0% | 1.1% | 1.2% |
| Costs | −1.6% | −0.1% | −2.2% |
| Average drawdown | −12.9% | −4.6% | −14.7% |
| Standard deviation | 7.2% | 7.1% | 9.1% |
| Sharpe ratio | −0.14 | 0.15 | 0.13 |
| Turnover | 9.9 | 9.6 | 11.7 |
| Skew | 4.29 | 2.32 | 2.59 |
| Lower tail | 5.8 | 6.7 | 3.60 |
| Upper tail | 5.1 | 9.5 | 4.79 |
| Correlation with expiry `b` | 0.24 | 0.26 | 0.27 |

### Calendar spreads: carry60

| Metric | VIX | WTI Crude | Eurodollar |
|---|---:|---:|---:|
| Mean annual return | −2.4% | 4.0% | −1.2% |
| Costs | −4.3% | −0.1% | −2.4% |
| Average drawdown | −34.3% | −7.4% | −38.4% |
| Standard deviation | 20.8% | 14.9% | 18.6% |
| Sharpe ratio | −0.12 | 0.27 | −0.06 |
| Turnover | 12.4 | 7.82 | 9.3 |
| Skew | 0 | 0.84 | 0.73 |
| Lower tail | 1.93 | 3.68 | 1.28 |
| Upper tail | 1.81 | 5.52 | 1.43 |
| Correlation with expiry `b` | 0.21 | 0.13 | −0.39 |

### Calendar triplets: EWMAC16

| Metric | VIX | WTI Crude | Eurodollar |
|---|---:|---:|---:|
| Mean annual return | 1.0% | −1.6% | −4.2% |
| Costs | −2.9% | −0.1% | −3.9% |
| Average drawdown | −9.3% | −5.5% | −37.0% |
| Standard deviation | 8.4% | 4.3% | 4.8% |
| Sharpe ratio | 0.12 | −0.37 | −0.87 |
| Turnover | 8.6 | 7.9 | 8.1 |
| Skew | 1.49 | −2.53 | 0.47 |
| Lower tail | 5.89 | 7.80 | 5.67 |
| Upper tail | 6.94 | 4.79 | 4.67 |
| Correlation with expiry `b` | 0.06 | 0.12 | 0.18 |

### Calendar triplets: carry60

| Metric | VIX | WTI Crude | Eurodollar |
|---|---:|---:|---:|
| Mean annual return | −2.4% | −0.2% | −0.7% |
| Costs | −7.0% | 0.1% | −4.6% |
| Average drawdown | −23.4% | −3.4% | −22.3% |
| Standard deviation | 14.8% | 8.3% | 14.5% |
| Sharpe ratio | −0.16 | −0.02 | −0.04 |
| Turnover | 15.1 | 8.1 | 7.4 |
| Skew | −0.54 | −0.15 | 5.28 |
| Lower tail | 2.95 | 3.76 | 3.66 |
| Upper tail | 3.08 | 3.40 | 4.63 |
| Correlation with expiry `b` | 0.01 | 0.19 | 0.12 |

## Implementation plan

1. Choose liquid same-underlying expiries `a`, `b`, and optionally `c`; define them relative to the front contract and a synchronized roll cycle.
2. Build and back-adjust the synthetic price: `p_a−p_b` for a spread or `0.5p_a+0.5p_c−p_b` for a triplet.
3. Estimate `σ_p` from daily synthetic-price changes using the Part One volatility procedure.
4. Calculate minimum capital, costs, and position sizes with the formulas above; use a 10% annual RV risk target. Double triplet minimum capital for indivisible contracts.
5. Derive carry with the applicable nearer/current or current/further formula; use the synthetic back-adjusted price as input to EWMAC or similar rules.
6. Execute as a combination where available; roll every leg at the same time.
7. Expect structural shifts and non-normal tail behaviour; do not rely on Sharpe ratio or a Gaussian standard deviation alone to characterize the trade.

## Warnings and boundary conditions

- Do not use illiquid deferred contracts, even if the front month is liquid.
- `R=1` and `X=Y=0.5` are market conventions, not guaranteed optimal hedges; maturity-dependent volatility can leave substantial outright exposure.
- High expiry correlation suppresses calculated standard deviation but may make gross notional, leverage, and risk-adjusted cost extreme.
- A triplet cannot be implemented in one-unit increments because it requires half-contract side legs.
- Do not roll legs separately; the synthetic definition collapses.
- Trend results can have strong positive skew, fat tails, and long losing periods; symmetric risk statistics can understate or misdescribe their character.
- VIX front-contract use is excluded in the example both for carry-calculation and tail-property reasons.

## Beyond triplets

The chapter notes further RV structures: STIR **packs** (four consecutive expiries), pack spreads/triplets, **bundles** (series of packs), cross-country bond packs, and the four-legged **condor**—the analogue of a butterfly triplet with short exposure in the two middle expiries and long exposure in the two outer expiries. Generalising to many legs becomes statistical arbitrage: regression or vector autoregression can identify co-integrated pairs, triplets, and larger asset sets.

## Explicit connections

- Strategies **twenty-eight** and **twenty-nine**: formulas and cross-instrument RV spread/triplet context; strategy twenty-eight supplies the minimum-capital approach and cautions on fixed weights.
- Strategy **twenty-seven**: proposed as a potentially suitable mean-reversion-plus-trend method for calendars.
- **Part One**: EWMAC, carry rules, and volatility estimation.
- **Part Six**, “Rolling and contract selection”: contract placement, liquidity, and non-stationary volatility implications.
- The directional strategies: rationale for using WTI's second contract and the usual standalone December choice.

## Glossary

- **Calendar spread:** same-underlying futures position long one expiry and short another.
- **Calendar triplet / triple / butterfly:** same-underlying three-expiry position long outer expiries and short middle expiry.
- **Base expiry (`b`):** the short leg of a long synthetic calendar structure.
- **Synthetic price:** constructed back-adjusted price series of a multi-leg position.
- **Term structure of volatility:** different expiries of the same instrument have different return standard deviations.
- **Samuelson effect:** theoretical tendency for futures volatility to increase toward maturity.
- **EWMAC16:** the chapter's exponential-weighted moving-average crossover trend rule.
- **carry60:** the chapter's carry trading rule.
- **Risk-adjusted cost:** per-contract cost divided by annualised currency volatility.
- **Pack / bundle:** STIR groups of four consecutive expiries / a series of packs.
- **Condor:** four-leg extension of the butterfly calendar triplet.
- **Statistical arbitrage (stat arb):** multi-leg RV trading using statistical methods to find co-integrated assets.

## Key takeaways

Calendar RV trades simplify mechanics and often allow combination execution, but liquidity and synchronized rolling are non-negotiable. They are curve-shape trades rather than ordinary direction bets. Very high correlation among expiries causes leverage, costs, and tail risk to matter far more than their low synthetic volatility initially suggests. In the presented tests, neither EWMAC16 nor carry60 produces compelling broad performance; the most distinctive feature is episodic trend opportunity during equilibrium shifts.
