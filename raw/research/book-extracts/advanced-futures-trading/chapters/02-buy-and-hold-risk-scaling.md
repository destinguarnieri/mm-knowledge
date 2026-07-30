# Strategy Two — Buy and Hold with Risk Scaling

## Purpose and central argument

Strategy one chose a fixed one-contract position and then calculated the capital needed to fully fund it. This chapter reverses that order: start with available capital, select an annualised risk target, and size the futures position so that its estimated risk equals that target. The central claim is that risk targeting produces a more logical position size and materially improves the reported risk-adjusted results versus a fixed contract position, while still leaving time-varying risk, skew, and fat-tail problems for Strategy Three.

The strategy is: **remain buy-and-hold long, but continuously scale the number of contracts for risk.** Higher-risk instruments receive smaller positions for a given capital base.

### Trading-plan card (chapter visual)

The chapter ends with a one-page trading-plan visual. It specifies: use instruments expected to have a positive risk premium, while considering short exposure to instruments such as VIX that have a negative risk premium; use the rounded current value of the position formula; estimate instrument `σ%` from the average of the backtested series or the risk level at strategy start (and refer to Appendix B for calculation detail); set `τ` to the minimum of the four stated constraints or use 20%; use current account value as capital; and require enough capital for four contracts. Calculate daily, trade only when rounded desired and actual positions differ, and include rollover trades. Trades need not occur every day; they depend on changes in capital, price, and FX.

## Core inputs and conventions

| Item | Meaning / convention in this chapter |
|---|---|
| `Capital` | Trading capital in the account/base currency. Fixed for the chapter's backtest reporting, but the current account value should be used in live trading. |
| `N` | Required number of futures contracts; it must be rounded because futures are indivisible. |
| `Multiplier` | Currency value per futures price point, in the instrument currency. |
| `Price` | Current price of the futures expiry actually held—not a back-adjusted price. |
| `FX` | Exchange rate translating the instrument currency into the account/base currency. |
| `σ%` | Annualised standard deviation of the instrument's percentage returns, expressed as a decimal (e.g. 16% = 0.16). |
| `σP` | Daily risk in futures price points. |
| `σ(Contract, base)` | Annualised standard deviation of one contract's P&L, in base-currency units per year. |
| `σ(Position, base)` | Annualised standard deviation of the whole position's P&L, in base-currency units per year. |
| `τ` | Target risk: annualised percentage standard deviation of the capital base, expressed as a decimal. |

For the illustrative S&P 500 micro future: multiplier = **$5**, price = **4,500**, so notional exposure per contract = **$22,500**. Assuming daily percentage standard deviation of 1%, the chapter annualises it using the Strategy One convention `0.01 × 16 = 16%`.

## Measuring single-contract risk

Annualised currency risk is notional exposure times annual percentage risk:

`σ(Contract, base) = Notional exposure(base) × σ%`

For the S&P micro example:

`$22,500 × 16% = $3,600` annualised standard-deviation risk per contract.

### Interpreting standard deviation (illustrative only)

The chapter assumes a symmetric Gaussian return distribution only to illustrate the number. It explicitly says this is not true in practice and that realised downside should be expected to be materially larger.

With a Sharpe ratio (SR) of 0.3055:

`mean annual excess return = SR × standard deviation = 0.3055 × $3,600 = $1,100`

Under the normal-distribution assumption, 68% of annual outcomes fall within one standard deviation of the mean: here, from `1100 − 3600 = −$2,500` to `1100 + 3600 = $4,700`. Thus a loss worse than $2,500 occurs at least 16% of years (about one in six) under that assumption. The same caveats are even more important when converting to daily loss expectations.

## Position-sizing model

### Equations

1. **Notional exposure per contract (base currency)**

   `Notional exposure(base) = Multiplier × Price × FX`

2. **Risk of one contract**

   `σ(Contract, base) = Notional exposure(base) × σ%`

3. **Risk of `N` contracts**

   `σ(Position, base) = σ(Contract, base) × N`

4. **Currency risk target**

   `σ(Target, base) = Capital(base) × τ`

5. **Risk-targeting condition**

   `σ(Target, base) = σ(Position, base)`

6. **Required position**

   `N = (Capital × τ) / (Multiplier × Price × FX × σ%)`

All dollar/currency terms in a formula must be in the account/base currency after applying `FX`. The formula applies to a single futures instrument and assumes an annualised percentage standard-deviation estimate. It gives a continuous contract number; implementation requires rounding to a tradable integer.

### Directional implications

`N` is larger with lower `σ%`, higher `τ`, more capital, a lower multiplier, a lower price, or a depreciation of the instrument currency relative to the account currency (as represented by the chapter's FX convention).

### Worked sizing examples

- `$22,500` capital at `τ = 16%` requires `$3,600` annualised risk; one S&P micro contract has that risk, so `N = 1`.
- With `$45,000` at `τ = 16%`, target risk is `$7,200`; two contracts provide it.
- If annual instrument risk doubles to 32%, a single S&P micro contract carries `$7,200` risk. With `$45,000` capital and a 16% target, `N = 1` again.
- The full substitution for the first example is:

  `N = (22,500 × 0.16) / (5 × 4,500 × 1.0 × 0.16) = 1.0`

### Daily-price-point formulation

The alternative formulation measures risk in daily price points:

`σP = (Price × σ%) / 16`

`σP` may also be calculated directly as the standard deviation of successive daily differences in back-adjusted prices:

`σP = stdev(Pt − Pt−1, Pt−1 − Pt−2, …)`

This latter approach works even when the current futures price is negative. The position formula becomes:

`N = (Capital × τ) / (Multiplier × FX × σP × 16)`

### Useful ratios

- **Contract leverage ratio**: `Notional exposure per contract / Capital`.
- **Volatility ratio**: `τ / σ%`.
- The sizing equation can be restated as: `N = Volatility ratio / Contract leverage ratio`.
- **Leverage ratio**: `Total notional exposure / Capital = (N × Notional exposure per contract) / Capital`.

Substitution yields the single-instrument identity:

`Leverage ratio = Volatility ratio = τ / σ%`

This identity is explicitly limited to trading one instrument; the chapter says it holds for the book's first three strategies.

## Selecting the target risk

Choose the **lowest** (most conservative) of four constraints:

1. Risk available under exchange/broker initial-margin limits.
2. Risk consistent with prudent leverage and the ability to survive extreme losses.
3. Personal/client risk appetite.
4. Risk optimal for expected strategy performance.

### Margin constraint

If all capital were used as initial margin (called insane in the chapter):

`Maximum N = Capital / (Margin per contract × FX)`

Substituting into the risk-target formula gives:

`Maximum τ = (Multiplier × Price × σ%) / Margin per contract`

For the S&P micro with multiplier `$5`, price `4,500`, risk `16%`, and margin `$1,150`:

`Maximum τ = (5 × 4,500 × 0.16) / 1,150 = 313%`

The lesson is that margin is generally not the binding leverage constraint for a sensible futures trader.

### Extreme-loss / prudent-leverage constraint

To retain a specified fraction of capital through an assumed worst daily return:

`Maximum leverage ratio = Maximum capital loss / Worst return`

Since leverage ratio equals `τ / σ%` for this single-instrument setup:

`Maximum τ = σ% × (Maximum capital loss / Worst return)`

Illustration: assume a 30% one-day crash and a willingness to lose half the capital. Maximum leverage is `0.50 / 0.30 = 1.667`; with `σ% = 16%`, maximum target risk is:

`0.16 × (0.50 / 0.30) = 26.7%` (summarised later as about 27%).

Historical worst daily returns are a starting point, not a sufficient bound. The chapter's CHF/EUR example shows why: before January 2015 the rate was unusually stable near a 1.20 peg; after the peg was removed it fell more than 0.20 price units in seconds, about 16% of the preceding day's close. The chapter argues a prudent assessment would look beyond the market's own recent history—e.g. the roughly 14% GBP decline over Black Wednesday and the following day in 1992.

### Personal risk appetite

Excess risk can induce harmful behaviour such as closing positions early; for external capital, it can also cause client withdrawals. The chapter says it is difficult to measure risk appetite precisely in annualised-standard-deviation terms. It offers rough reference points:

| Reference portfolio / asset | Typical annualised standard deviation stated |
|---|---:|
| Diversified bonds | 2%–8% |
| Mixed stocks-and-bonds portfolio | ~12% |
| Diversified global stocks | ~15% |
| Blue-chip developed-market individual stock | 20%–40% |
| Especially volatile stock or cryptocurrency | >100% |

### Kelly / expected-performance constraint

The **Kelly optimal risk** maximises final compounded account value in the chapter's S&P 500 experiment. With Gaussian normal returns, the optimal target risk equals the underlying strategy SR. The footnote derives this from `f = μ / σ²`, so `fσ = μ / σ = SR`, where `μ` is average excess return and `σ` is the unleveraged portfolio standard deviation.

For the 40-year S&P 500 buy-and-hold backtest, Figure 11 peaks around 38% risk target, although SR ≈ 0.47 would imply 47% under Gaussian assumptions. The divergence is attributed to non-normal S&P returns, negative skew, and fat tails. The chapter recommends **half Kelly** because returns are rarely Gaussian and SR forecasts are difficult:

`target risk from expected performance = expected SR / 2`

Using SR = 0.47 gives 23.5%. A footnote notes the circularity—backtesting needs a risk target, but SR is risk-adjusted; run an initial nominal-risk backtest, calculate SR, choose the target, then rerun—or use the book's 20% recommendation.

### Chapter's S&P target-risk summary

| Constraint | S&P micro illustration |
|---|---:|
| Initial-margin maximum | ~313% |
| Survive a 1987-size crash with half capital intact | ~27% |
| Personal risk appetite | typically 10%–100%; generally lower institutional values |
| Half-Kelly expected-performance estimate | ~23% |

The lowest is about 23%; the chapter uses **20% annualised target risk** for the rest of the book.

## Implementation: S&P 500 micro risk scaling

With capital `$100,000`, `τ = 20%`, `σ% = 16%`, multiplier `$5`, and FX `1`:

`N = (100,000 × 0.20) / (5 × Price × 1 × 0.16) = 25,000 / Price`

Recalculate the desired position daily using current futures price and FX, round `N`, and buy/sell whenever actual and desired positions differ. The chapter does **not** yet update `σ%` daily; it says Strategy Three will do so. The backtest instead uses the whole-sample average standard deviation (16.1%), which is explicitly flagged as forward-looking in-sample information that would not have been known at the start.

This rebalancing incurs more trading cost than Strategy One (which only rolls contracts); the chapter estimates the additional S&P cost at **0.17% per year**.

### Continuous versus discrete trading

The chapter contrasts discrete trade narratives (open a position, then close it) with continuous trading: calculate the optimal position—normally once daily here—round it, compare it with the actual position, and trade the difference. A long position can be reduced, rebuilt, closed, or ultimately reversed without defining separate opened-and-closed trades. The author says this approach is common in quantitative hedge funds and supports combining strategies more easily later in the book.

## Backtest reporting, compounding, and S&P results

For the chapter's risk-targeted S&P backtest, dollar P&L uses a varying contract count, while percentage returns use a fixed `$100,000` notional capital. Consequently cumulative currency and percentage curves differ only in their y-axis.

The chapter uses **non-compounded percentage returns** in its backtests and sums percentage returns for cumulative plots (100 = 100%). It does this to avoid visually dominant exponential compounded curves and to allow easy comparison independent of capital. With compounded returns, the appropriate average is CAGR—the annualised geometric mean of daily returns—not an arithmetic average.

**Live-trading warning:** fixed capital is described as extremely dangerous for real money. Kelly/half-Kelly risk targeting requires reducing position size after losses. Use the current account value as `Capital` in the sizing calculation, so losses decrease positions and profits increase them. The author updates daily in an automated system; at a 20% risk target, weekly may be safe except in market stress, while institutional notional AUM may update weekly or monthly subject to fund liquidity/rules.

### Figures

- **Figure 11 — Final account value vs. risk target:** 40-year compounded S&P backtest beginning with one capital unit. Final value rises until roughly a 40% target, then falls sharply and approaches zero near 60%. The explanation is that leveraged worst days become too damaging; a 27% October-1987 loss times 3.75 leverage (60%/16%) exceeds 100%.
- **Figure 12 — Contracts through time:** S&P micro holdings fall from nearly 250 contracts when price is just above $100 to just under six when price exceeds $4,000, illustrating inverse scaling with price.
- **Figure 13 — Daily percentage returns:** shows daily returns under the fixed-risk target; subsequent text notes realised risk can still be above or below target.
- **Figure 14 — Account curve:** cumulative sum of the non-compounded percentage returns for the same fixed-risk S&P strategy.

### S&P backtest performance characteristics

| Metric | Value |
|---|---:|
| Strategy label in table | Buy and hold, single contract |
| Instrument | S&P 500 micro future |
| Years of data | 41 |
| Mean annual return | 12.1% |
| Average drawdown | −16.9% |
| Annualised standard deviation | 25.0% |
| Annualised Sharpe ratio | 0.48 |
| Skew | −0.47 |
| Left tail | 2.21 |
| Right tail | 1.79 |

**Source ambiguity flagged:** the table labels the strategy “Buy and hold, single contract,” although it appears in the Strategy Two risk-scaling discussion and the surrounding text describes a varying-contract risk-targeted backtest. This study file preserves the label rather than silently correcting it.

The 25.0% annualised standard deviation overshoots the 20% target because of several extreme days; using monthly rather than daily returns yields 19.8%. The chapter says this demonstrates that realised risk can still vary substantially and will be addressed in Strategy Three.

## Minimum capital and contract granularity

At `$5,000` capital, the S&P example gives:

`N = (5,000 × 0.20) / (5 × 4,500 × 1 × 0.16) = 0.278`

Fractional futures contracts cannot be traded. Rearranging the sizing formula:

`Capital = (N × Multiplier × Price × FX × σ%) / τ`

For one contract:

`Minimum capital(1 contract) = (Multiplier × Price × FX × σ%) / τ`

For the S&P micro, this is:

`($5 × 4,500 × 1.0 × 0.16) / 0.20 = $18,000`

But one contract leaves no adjustment room. If the price doubles, desired `N` becomes 0.5: either go flat with 0% expected risk or retain one contract at 40% expected risk. The chapter recommends beginning with **at least four contracts**:

`Minimum capital(4 contracts) = (4 × Multiplier × Price × FX × σ%) / τ`

Equivalently:

`Minimum capital(4 contracts) = 4 × Notional exposure per contract × (σ% / τ)`

For the S&P micro this is `$72,000`.

Minimum capital rises with a higher multiplier; higher price and/or exchange rate; larger notional exposure per contract; higher instrument standard deviation; and a lower risk target. The chapter warns against solving limited capital by simply raising the risk target.

### Table 5 — selected minimum-capital requirements

The source caption defines these as current capital required to hold **one contract** using a 20% annualised risk target.

| Lower-capital examples | Minimum capital | Higher-capital examples | Minimum capital |
|---|---:|---|---:|
| Schatz (Bond) | $7,600 | Palladium (Metal) | $1,880,000 |
| US 2-year (Bond) | $15,600 | S&P 400 (Equity) | $860,000 |
| BTP 3-year (Bond) | $19,600 | Gas – Last (Energy) | $844,000 |
| Korean 3-year (Bond) | $24,400 | US 30-year (Bond) | $552,000 |
| VSTOXX (Volatility) | $26,400 | Copper (Metal) | $548,000 |
| Eurodollar (Interest rate) | $29,200 | AEX (Equity) | $533,000 |
| MXPUSD (FX rate) | $34,000 | NOKUSD (FX rate) | $520,000 |
| US 3-year (Bond) | $40,000 | Gasoline (Energy) | $468,000 |

Short-duration bonds dominate the low-capital side because the chapter characterises them as low volatility. VSTOXX is also low-capital because its stated price was about 22.9 and multiplier 100; the US VIX's multiplier of 1,000 gives a stated minimum capital near $250,000. MXPUSD has $24,000 notional exposure and 8.3% annualised standard deviation. Palladium combines roughly $189,500 notional exposure (price nearly $1,900 × multiplier 100) and nearly 50% annualised standard deviation, leading to about $1.88m for four contracts.

## Cross-asset results

Tables 6 and 7 report average performance under fixed risk targeting and are explicitly comparable with Strategy One's Tables 3 and 4.

| Metric | Equity | Vol | FX | Bond |
|---|---:|---:|---:|---:|
| Mean annual return | 11.5% | −8.3% | 1.5% | 12.3% |
| Average drawdown | −8.7% | −76.9% | −29.2% | −12.5% |
| Annualised standard deviation | 22.2% | 21.8% | 21.2% | 21.4% |
| Sharpe ratio | 0.48 | −0.39 | 0.07 | 0.60 |
| Skew | −0.40 | 2.27 | −0.24 | 0.15 |
| Lower tail | 1.98 | 1.30 | 1.74 | 1.81 |
| Upper tail | 1.54 | 2.68 | 1.65 | 1.53 |

| Metric | Metals | Energy | Ags | Median |
|---|---:|---:|---:|---:|
| Mean annual return | 6.7% | 6.5% | 4.5% | 6.3% |
| Average drawdown | −38.3% | −33.4% | −45.5% | −15.0% |
| Annualised standard deviation | 21.9% | 22.5% | 21.4% | 21.5% |
| Sharpe ratio | 0.31 | 0.29 | 0.20 | 0.34 |
| Skew | −0.13 | −0.20 | 0.45 | −0.17 |
| Lower tail | 1.80 | 1.65 | 1.64 | 1.82 |
| Upper tail | 1.64 | 1.58 | 1.71 | 1.62 |

The stated interpretation: equities retain unpleasant skew and tails but have decent SR; bonds have the highest SR and better behaviour; volatility has negative SR but positive skew and a fat right tail; the others lie between. Average asset-class standard deviations land near the 20% target. Relative to Strategy One, SR is higher in every asset class; median SR rises from 0.13 to 0.34, and negative skew improves from −0.38 to more than half that magnitude.

## Assumptions, limitations, and warnings

- Standard-deviation loss interpretation assumes symmetric, normally distributed returns; the chapter says real downside is likely larger.
- FX-rate volatility does not affect the stated `σ%` standard deviation in the formula (footnote 44), although the current FX level does affect base-currency exposure and position size.
- A fully funded futures position can still lose all capital if the futures price reaches zero or below; the chapter notes crude oil in early 2020 as an example.
- Initial margin permits extreme risk and should not be treated as the prudent sizing rule.
- Worst historical return is only a starting point; regime breaks and policy changes can create losses far beyond recent history.
- Risk-appetite questionnaires are not precise scientific measures.
- Full-Kelly inference assumes Gaussian returns and a reliable expected SR; negative skew/fat tails can make the actual optimum lower.
- Daily rebalancing for price/FX creates transaction costs; the chapter postpones detailed cost methodology to Strategy Three.
- Whole-period 16.1% backtest volatility is in-sample, forward-looking information; it is labelled “cheating” for a live historical simulation.
- Contract rounding causes material target-risk error at small capital. Four starting contracts is a rule of thumb, not a guarantee.
- Rebalancing solely for price changes may interact with the equity-futures leverage effect: falling prices may make indebted firms riskier while the strategy buys more stock. The chapter says it did not find materially different results across asset classes in practice.

## Explicit connections to other chapters

- **Strategy One:** supplies the annualisation convention, notional-exposure framework, P&L formula, Tables 3–4, and the contrast with fully funded one-contract positions. It implicitly compounds because its capital varies with price.
- **Strategy Three:** will update `σ%`, address time-varying realised risk, and explain trading-cost calculation in more detail.
- **Later in the book:** uses the daily-price-point formulation; discusses discrete implementation of strategies; explains account-compounding management; and combines multiple strategies.
- **Appendix A:** bibliography mentioned for Kelly/Kelly criterion history.

## Glossary

- **Annualised standard deviation:** the chapter's risk measure, expressed either as a return percentage or base-currency P&L.
- **Back-adjusted price:** historical price series used for certain calculations; not the price to use for the contract currently held in the notional-exposure formula.
- **Base/account currency:** currency in which capital and P&L risk are measured.
- **Contract leverage ratio:** one contract’s notional exposure divided by capital.
- **Continuous trading:** repeated calculation and adjustment to the current optimal position, normally daily here.
- **Discrete trading:** opening and later closing separately identifiable trades.
- **FX rate:** conversion rate from instrument currency to base currency in the model.
- **Half Kelly:** target risk equal to half the expected Sharpe ratio, recommended here as a conservative alternative to full Kelly.
- **Initial margin / variation margin:** cash required to initiate or maintain futures positions; higher-risk instruments generally require more.
- **Kelly optimal risk:** target risk that maximises final compounded account value under its assumptions.
- **Leverage ratio:** total notional exposure divided by capital.
- **Notional exposure:** multiplier × current futures price × FX; the base-currency exposure of a contract.
- **Risk target (`τ`):** desired annualised standard deviation as a percentage of capital.
- **Sharpe ratio (SR):** mean excess return divided by standard deviation in the chapter's usage.
- **Volatility ratio:** target risk divided by instrument percentage risk.

## Key takeaways

1. Size the position from capital and estimated risk, rather than deciding a fixed contract count first.
2. For one instrument, required leverage equals `τ / σ%`; riskier instruments get smaller positions.
3. Set `τ` as the lowest of margin, crash-survival, risk-appetite, and expected-performance constraints; the chapter adopts 20% annually.
4. Continuous daily resizing meets a target only approximately: rounding, extreme days, stale volatility estimates, price/FX changes, and trading costs matter.
5. Backtest reporting may use fixed capital for clarity, but live risk sizing should use current account value to reduce exposure after losses.
6. Risk targeting is presented as a major improvement over Strategy One, not as a complete solution to tails, skew, or changing risk.
