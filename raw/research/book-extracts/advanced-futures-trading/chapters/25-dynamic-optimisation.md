# Strategy 25 — Dynamic optimisation (for when you can’t trade the Jumbo portfolio)

## Purpose and central argument

Dynamic optimisation makes a limited-capital futures account behave as much as possible like the *unrounded* positions of a broadly diversified “Jumbo” portfolio (about 100 futures markets). Each day, it chooses integer contract positions whose portfolio-return tracking error against the ideal unrounded portfolio is lowest. The intended benefit is to retain most diversification benefit without needing the author’s estimated $50m minimum capital for directly trading the full Jumbo portfolio.

The chapter’s headline prescription is: dynamically optimise positions produced by an underlying strategy to use limited capital best. It is a coding-intensive method; the author says it is practically impossible to run without a programming language and provides sample Python on the book website. It requires covariance matrices, vectors, and matrix dot products.

## Why it is needed

At $50m, an ideal S&P 500 position of 14.2 contracts can be rounded to 14. At $100k, the comparable ideal position might be 0.0284 contracts, which rounds to zero; across 100+ markets, most or all positions can vanish. A static selection of a small instrument subset (Strategy 4) avoids untradeable positions but gives up diversification and can miss the market that produces that year’s gains.

Dynamic optimisation assumes continuous recalculation of optimal positions and trading toward them. It is not applicable to the usual discretionary style of making discrete trades.

## Inputs, notation, and units

All weights are **notional exposure / trading capital** and are dimensionless. Positive is long; negative is short.

| Symbol | Meaning | Units / constraints |
|---|---|---|
| `i` | Instrument index | Each tradable futures market |
| `N_i` | Optimal, unrounded position from the underlying strategy | Contracts; calculated *before* buffering |
| `P_i` | Previous/current contracts held | Integer contracts |
| `N_i*` | Optimised final position | Integer contracts |
| `w_i` | Ideal/unrounded portfolio weight | `N_i × weight_per_contract_i` |
| `w_i*` | Optimised portfolio weight | Must be an integer multiple of the weight per contract |
| `w_i^P` | Previous/current portfolio weight | `P_i × weight_per_contract_i` |
| `e_i` | Tracking-error weight | `w_i − w_i*` |
| `e_i^P` | Error of current versus optimised portfolio | `w_i* − w_i^P` |
| `e`, `e_P` | Corresponding error vectors | One element per instrument |
| `Σ` | Covariance matrix of **underlying asset percentage returns** | Annualised return covariance; not sub-strategy covariance |
| `ρ` | Correlation matrix of underlying percentage returns | Six months of weekly returns in this chapter |
| `σ` | Vector/diagonal matrix of annualised underlying return standard deviations | EWMA of daily returns, 32-day span; annualised |
| `C_i` | Cash cost of trading one contract | Account base currency after conversion |
| `w_i^c` | Cost per unit of portfolio weight traded | Dimensionless |
| `Δ_i` | Absolute trade in weight terms | `abs(w_i* − w_i^P)` |
| `δ` | Cost of all trades in weight terms | Dimensionless |
| `τ` | Risk target | Annualised return standard deviation; 20% used here |
| `B_σ` | Portfolio-level tracking-error buffer | Annualised standard-deviation units; 1% here |
| `T` | Tracking error of current vs optimised portfolio | Annualised standard deviation |
| `α` | Fraction of the full trade to execute when buffering | In `[0,1]` under the stated condition |

The underlying `N_i` are produced using combined forecasts, instrument weights, IDM, trading capital, price, multiplier, FX rate, and volatility. The supplied trading-plan figure gives:

`N_i = capped_combined_forecast_i × capital × IDM × weight_i × τ / (10 × multiplier_i × price_i,t × FX_i,t × σ_i,t)`.

## Core equations

### Weight and return calculations

```text
notional_exposure_per_contract_i = multiplier_i × price_i × FX_rate_i
weight_per_contract_i = notional_exposure_per_contract_i / capital
w_i = N_i × weight_per_contract_i

percentage_return_i,t = (p_i,t − p_i,t−1) / F_i,t
Σ = σᵀ · ρ · σ
```

`p` is the back-adjusted price and `F` is the traded futures-contract price on the appropriate day. In the source equations, `T` means transpose and `·` means matrix dot multiplication. Covariance uses instrument asset returns rather than returns of trading sub-strategies.

### Tracking-error objective

```text
e_i = w_i − w_i*
e = [e_0, e_1, e_2, ...]
tracking_error_standard_deviation = sqrt(eᵀ · Σ · e)
```

Choose the feasible `w*` that minimizes the final expression. Feasibility is discrete: if a contract carries weight 0.32, permitted weights are `..., −0.96, −0.64, −0.32, 0, 0.32, 0.64, 0.96, ...`.

### Greedy optimisation algorithm

This is a local, irreversible greedy search—not a guaranteed global optimum.

1. Start with zero weight in every instrument; call this `current_best`.
2. Initialize `proposed = current_best`.
3. For each eligible instrument, create an incremental candidate from `current_best` (not from the latest proposed candidate):
   - if ideal `w_i` is positive, add one `weight_per_contract_i` (buy one contract);
   - if ideal `w_i` is negative, subtract it (sell one contract);
   - calculate its tracking error; if lower than `proposed`, replace `proposed`.
4. After the loop, `proposed` is the best portfolio one contract away from `current_best`.
5. If it improves tracking error, make it the next `current_best` and repeat step 2; otherwise stop. Convert final weights to integer positions:

```text
N_i* = w_i* / weight_per_contract_i
```

The procedure only opens positions in the direction of the underlying forecast. It is fast even with 100+ instruments, robust, and usually avoids sparse one- or two-position portfolios; the stated exception is an extremely small account whose genuine optimum is that sparse. It avoids potentially dangerous proxy hedges with the opposite forecast sign. Its trade-off is that it can miss a slightly better global solution, although the author considers such solutions less robust.

## Worked three-market example

Capital is $500,000; the ideal positions are deliberately arbitrary. Correlations: US 5-year vs US 10-year bond = `0.9`; each bond vs S&P 500 = `−0.1`.

| Input | US 5-year bond | US 10-year bond | S&P 500 micro |
|---|---:|---:|---:|
| Ideal contracts `N_i` | 0.4 | 0.9 | 3.1 |
| Notional/contract | $110,000 | $120,000 | $20,000 |
| Weight/contract | 0.22 | 0.24 | 0.04 |
| Ideal weight `w_i` | 0.088 | 0.216 | 0.124 |
| Annualised return s.d. | 5.2% | 8.2% | 17.1% |

The annual covariance matrix is:

| `Σ` | US 5-year | US 10-year | S&P 500 |
|---|---:|---:|---:|
| US 5-year | 0.002704 | 0.003838 | −0.000889 |
| US 10-year | 0.003838 | 0.006724 | −0.001402 |
| S&P 500 | −0.000889 | −0.001402 | 0.029241 |

Starting `current_best = [0, 0, 0]`, so `e = [−0.088, −0.216, −0.124]` and tracking-error s.d. is 2.67% p.a. In the first pass, one 5-year bond produces 3.43% (reject), one 10-year produces 1.53% (accept as proposed), and one S&P micro produces 2.51% (reject). Thus `current_best` becomes `[0, 0.24, 0]`.

| Pass / best outcome | Weights `[5y, 10y, S&P]` | Tracking error |
|---|---|---:|
| Start | `[0, 0, 0]` | 2.67% |
| First accepted addition | `[0, 0.24, 0]` | 1.53% |
| Second pass: add first S&P | `[0, 0.24, 0.04]` | 1.506% |
| Third pass: add second S&P | `[0, 0.24, 0.08]` | 1.504% |
| Fourth pass: no candidate improves | `[0, 0.24, 0.08]` | 1.504% |

The final positions are `[0, 1, 2]`. Simple rounding would yield three S&P micros; the optimiser selects two because, in the author’s intuition, the omitted 5-year interest-rate exposure and slightly negative bond/equity correlation make a further equity contract inferior.

## Cost penalty

Without a cost term, the optimizer is expensive because it can change the instrument set daily. Extend the objective:

```text
w_i^P = P_i × weight_per_contract_i
w_i^c = (C_i / capital) / weight_per_contract_i
Δ_i = abs(w_i* − w_i^P)
δ = Σ_i (Δ_i × w_i^c)
objective = sqrt(eᵀ · Σ · e) + 50δ
```

The cash cost per contract is:

```text
spread_cost_price_points = (bid − offer) / 2
spread_cost_currency = multiplier × spread_cost_price_points
C_i = spread_cost_currency + commission_per_contract
```

Convert `C_i` into the account’s base currency. In a backtest, historical cash costs must be adjusted with the method in Strategy 5 rather than applying today’s currency cost to prior periods.

The multiplier 50 was calibrated to keep costs roughly comparable with Strategy 11. The author says values from 10 to 100 yield very similar results. In the example, cash costs are $5.50 (US 5-year), $11.50 (US 10-year), and $0.875 (S&P micro), producing cost-per-weight values 0.0050%, 0.010%, and 0.0044% respectively. From zero positions to `[0, 0.24, 0.08]`, `δ = 0.00275%`; the objective rises from 1.504% to `1.504% + 50 × 0.00275% = 2.208%`.

**Limitation:** this penalty cannot prevent the full close (and possibly reversal) when an underlying forecast changes sign. Raising it too far concentrates trading in the cheapest instruments and harms after-cost performance.

## Portfolio-level buffering

Buffering is applied *after* optimisation, not to individual ideal positions. First produce unbuffered `N_i`; then use a tracking-error buffer for the portfolio.

```text
B_σ = 0.05τ
e_i^P = w_i* − w_i^P
T = sqrt(e_Pᵀ · Σ · e_P)
α = max((T − B_σ) / T, 0)
required_trade_i = round(α × (N_i* − P_i))
```

The original 10% symmetric position buffer is interpreted as a 5% asymmetric tracking-error buffer. With `τ = 20%`, `B_σ = 1%`.

Operationally:

1. Optimise rounded positions with the cost-penalised dynamic method.
2. Compute `T` between the current and the new optimised portfolio (not the error versus the unrounded ideal).
3. If `T < B_σ`, do not trade.
4. If `T > B_σ`, trade only far enough to target the buffer edge, then round contract trades.

Example: current weights `[0,0,0]` versus optimised `[0,0.24,0.08]` give `T = 2.35%`, so `α = (2.35% − 1%)/2.35% = 0.57`. Full S&P and 10-year changes (`+0.08`, `+0.24`) become `+0.0456` and `+0.138`; in contracts these are `+1.14` and `+0.57`, rounded to buy one S&P and one 10-year. Final weights are `[0,0.24,0.04]`. Due to contract rounding, actual post-trade tracking error need not equal exactly 1%; here it is about 0.2%.

## Backtest evidence and interpretation

All three test variants use Strategy 11 (cost-weighted carry + trend forecasts). Dynamic optimisation is said to work with any strategy in Parts 1–3, but not Parts 4–5.

| Metric | Jumbo, no optimisation: 100 / $50m | Static: 27 / $500k | Dynamic: 100 / $500k |
|---|---:|---:|---:|
| Mean annual return | 26.5% | 25.8% | 25.7% |
| Costs | −1.1% | −1.0% | −1.0% |
| Average drawdown | −8.9% | −9.5% | −9.4% |
| Standard deviation | 20.9% | 21.8% | 21.1% |
| Sharpe ratio | 1.27 | 1.18 | 1.22 |
| Turnover | 46.5 | 32.1 | 48.8 |
| Skew | 0.76 | 0.19 | 0.79 |
| Lower / upper tail | 1.86 / 1.75 | 1.69 / 1.54 | 1.86 / 1.73 |
| Alpha / beta | 22.3% / 0.30 | 21.6% / 0.25 | 22.9% / 0.29 |

The static 27-instrument result is flattered by selection luck: its median-instrument SR is 0.34 versus 0.27 for the 100-instrument Jumbo group, a 26% advantage. After crude adjustment by `1.26`, static results are mean return 20.5%, drawdown −14.8%, SR 0.94, alpha 16.2%; dynamic remains return 25.7%, drawdown −9.4%, SR 1.22, alpha 22.9%. Correlation with the $50m Jumbo strategy is 0.99 dynamic versus 0.78 static.

At $100k, static selection picks 16 instruments; its median SR 0.41 implies a 1.52 adjustment factor. Adjusted static/dynamic results are: mean return 15.5%/20.0%, costs −0.9%/−0.5%, drawdown −12.0%/−9.6%, s.d. 21.3%/18.8%, SR 0.73/1.06, alpha 13.3%/17.8%. Dynamic holds about seven instruments on average, never more than 15; its monthly-return correlation to the full Jumbo portfolio is 0.91, versus static 0.50.

| Capital | Static adjusted SR | Dynamic SR | Static correlation with $50m strategy | Dynamic correlation |
|---|---:|---:|---:|---:|
| $100k | 0.73 | 1.06 | 0.50 | 0.91 |
| $500k | 0.94 | 1.22 | 0.78 | 0.99 |
| $50m | 1.27 | Not required | 1.00 | Not required |

These results are reported backtest findings, not a general guarantee. The author recommends checking the distribution of tracking errors, risk tracking, calibration (`50`, `1%`), and sensitivity to nearby parameter values.

## Constraints, applications, and warnings

- You may generate ideal positions for instruments you never permit the optimiser to hold (too costly, illiquid, or restricted). The optimiser can transfer correlated risk into eligible markets; the author generates roughly 150 candidate futures but allows about 100 to trade.
- Position limits can be imposed (example: at most 10 VIX contracts).
- If a market is temporarily shut but risk must be reduced, set that instrument’s lower and upper limits equal to its current position. The optimiser can proxy-trade open positively/negatively correlated markets if forecasts have the needed sign.
- Before a costly roll, force the expiring instrument to close; the optimiser may reopen it or choose another representation. Constraint handling is more complex; the chapter directs readers to the book website for modifications.
- Correlations can change when exposure is highest; this is why the author favors same-direction proxy positions over a globally optimal opposite-sign hedge.
- The chapter contains no performance proof or full sensitivity analysis; it explicitly says those analyses are outside its space.

## Key takeaways and glossary

Dynamic optimisation is a daily integer-position approximation to an ideal diversified portfolio, minimizing covariance-aware tracking error, then adding a cost penalty and portfolio-level buffering. Its potential advantage is that it can preserve much of broad-market diversification at modest capital, while its costs are complexity, coding dependence, turnover pressure, parameter calibration, and non-global greedy search.

Glossary: **Jumbo portfolio**, **static optimisation**, **dynamic optimisation**, **unrounded position**, **portfolio weight**, **tracking error**, **covariance matrix**, **greedy algorithm**, **weight per contract**, **cost penalty**, **buffering**, **IDM**, **Sharpe ratio**, **proxy trade**.

## Explicit chapter connections

- Strategy 2: portfolio-weight formulae.
- Strategy 3: 32-day-span EWMA volatility.
- Strategy 4: static instrument-selection optimisation.
- Strategy 5: historical currency-cost adjustment for backtests.
- Strategy 8: original position buffering (10% symmetric buffer).
- Strategy 9: reported near-fivefold diversification improvement.
- Strategy 11: carry + trend benchmark and cost-weighted forecasts.
- Strategy 16: possible evidence-based equity down-weighting in trend.
- Strategy 18: trends often occur across an asset class.
- Appendix B: return-correlation methodology.
- Part Six: position limits, risk management, and rolling tactics.
