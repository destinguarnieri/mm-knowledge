# Tactic Three: Cash and Compounding

## Purpose and central argument

A futures account is a pool of cash supporting derivative contracts. Futures positions may be the main source of trading return, but cash management matters because free cash must absorb variation margin and because a poor cash or compounding policy can create avoidable risk or eventual bankruptcy. The chapter recommends:

- Keep the account **fully capitalised**: deposit all, and only, the notional capital allocated to trading.
- Keep net free cash in cash rather than seeking yield through riskier investments.
- For foreign-currency margin, generally use an explicit **FX trade** rather than borrowing the foreign currency; accept the resulting unhedged-FX noise and periodically convert excess currency back to the domestic currency.
- Never run fixed capital live. Use full compounding unless profits are to be extracted; for that case, use the author's “half compounding” (a high-watermark cap on notional capital) and withdraw excess cash regularly.

## Futures, cash, and margin

### Definitions

- **Free cash:** cash not segregated as initial margin. It is not truly spare: it covers likely trading losses and variation-margin calls.
- **Initial margin:** cash segregated for an open futures position; the clearing house has a legal claim on it while the trade remains open.
- **Variation margin:** cash paid from free cash to settle losses on an open futures position. It cannot come from initial margin, which must remain posted.
- **Margin call:** broker demand for additional money when free cash cannot cover variation margin.
- **Liquidation:** broker closes all or part of a position, releasing initial margin to cover a free-cash shortfall.
- **Notional capital:** the capital figure used to size positions and set risk; it need not equal the cash currently in the brokerage account unless the account is fully capitalised.

### Worked margin example

Start with $500,000 free cash. Buy one S&P 500 micro futures contract requiring $1,150 initial margin.

| Account item | Before trade | After opening one contract |
|---|---:|---:|
| Free cash | $500,000 | $498,850 |
| Initial margin | $0 | $1,150 |
| Total | $500,000 | $500,000 |

The margin limits a trader with this cash to 434 contracts, but this mechanical maximum is not a sensible position size. The chapter estimates its notional exposure at about $8.7 million and annualised standard deviation above 250% of account value—more than 12 times the suggested risk target, \(\tau = 20\%\).

If the S&P 500 falls 40 points and the futures multiplier is $5 per point:

\[
\text{loss} = 40\ \text{points} \times \$5/\text{point} = \$200.
\]

| Account item | After 40-point loss |
|---|---:|
| Free cash | $498,850 − $200 = $498,650 |
| Initial margin | $1,150 |
| Total | $499,800 |

If the trader then opens 433 more contracts, total initial margin becomes \(434 \times \$1{,}150 = \$499{,}100\), leaving only $700 free cash. A further 1-point fall costs \(434 \times \$5 = \$2{,}170\), more than free cash. The broker may issue a margin call or liquidate positions.

At the suggested \(\tau=20\%\) target, frequent margin problems should be unlikely. The author reports using \(\tau=25\%\) personally, with average margin usage around 30% and about 70% of account value normally remaining free cash.

## Account capitalisation

### Under-capitalisation

Example: from $500,000 designated trading capital, keep $250,000 elsewhere and place only $250,000 with the broker. After posting $1,150 initial margin, the account has $248,850 free cash.

Potential benefits claimed:

1. External spare cash could earn more than broker-paid cash interest.
2. Less money sits with a broker that could fail.

The author advises against it. A severe trading loss requires an immediate top-up, but the external investment may have fallen or be illiquid. Repeatedly adding capital after losses may also condition a retail trader to keep feeding a losing account. If broker failure is the concern, the chapter recommends changing broker or using multiple brokers; this is particularly relevant where government-backed protection has a maximum covered loss. Under-capitalisation also complicates position sizing because account cash and external spare cash must be added to compute notional capital.

### Over-capitalisation and recommendation

**Over-capitalisation** is safer for margin availability but increases exposure to the broker and lowers return on total capital because excess cash could be invested elsewhere.

**Full capitalisation** means putting all notional trading capital into the account—“no more and no less.” This is the chapter's general recommendation.

## What to do with free cash

The book's backtests use excess returns, excluding interest on margin. The author notes broker rates at the time of writing of 0.33% on qualifying USD balances, 0.41% on GBP, and negative interest on EUR deposits.

With 70% free cash on average, a 3% incremental return would add \(0.70 \times 3\%=2.1\%\) annual return, stated as just over 0.10 Sharpe-ratio units for a \(\tau=20\%\) strategy. But higher yield entails higher risk: the cited globally diversified government-bond ETF yielded about 2.5% yet had fallen over 12% while the author was writing. Yields above 3% would require riskier assets such as emerging-market debt, junk corporate bonds, or equities. Unless the investment is negatively correlated with the trading strategy, this effectively raises the overall risk target.

Hedging a bond fund with bond futures offers no free lunch: a perfect hedge gives approximately zero net return before transaction costs; an imperfect hedge creates leveraged exposures the trader may not understand. The hedge also consumes free cash unless it happens to offset an existing futures position.

**Recommendation:** leave net account balance in cash. If investing it anyway, use only an extremely liquid investment because it may need to be sold quickly to satisfy margin demands.

## Margin and foreign exchange

### Two ways to fund foreign-currency margin

Starting with $500,000 USD free cash, buying 50 German Bund 10-year futures requires €235,000 initial margin (about $250,000).

| Method | Mechanics after opening trade | Initial net FX exposure |
|---|---|---|
| **FX trade option** | Sell USD and buy EUR for margin: $250,000 USD free cash plus €235,000 initial margin. | Net long €235,000. |
| **FX borrow option** | Keep $500,000 USD cash; borrow €235,000 and post it as €235,000 margin. | Zero. |

“Option” here means a choice, not a financial derivative. Many brokers automatically create the borrowing position unless the trader makes an explicit FX trade.

If the Bund trade loses €20,000 (about $21,270):

- **FX trade option:** sell more dollars and buy euros. Free USD cash falls to $228,730; initial margin remains €235,000 (shown as worth $250,000); total is $478,730.
- **FX borrow option:** borrow more euros. USD cash remains $500,000; euro loan becomes −€255,000 (shown as worth $271,270); initial margin remains €235,000 (shown as worth $250,000); total is $478,730.

If the Bund position later closes at no further gain or loss, the borrower repays the euro loan with released initial margin. Under FX trading, the account retains €255,000 surplus free cash (shown as worth $271,270) alongside $228,730 USD, totaling $500,000. It can be retained for a future trade or converted back to dollars.

### Choice, costs, and risk

Relevant factors:

- FX conversion has a transaction cost, though the author expects it to be relatively small.
- Deposited cash earns interest while borrowed cash incurs interest. The cited rates are 0.33% earned on USD versus about 1% to borrow EUR; the broker earns the borrow/lend spread.
- FX trading creates more currency exposure. With €235,000 net balance, a 2% EUR depreciation costs €4,700, said to be about $5,000 or 1% of the account. With FX borrowing, exposure is zero initially and −€20,000 only after the loss; the relevant concern is EUR appreciation. The text says “a 2% depreciation would cost only €400,” which conflicts with that preceding directional statement; preserve this as a source inconsistency rather than resolving it.

FX exposure may be hedged with currency futures. The example says a USD/EUR contract is exactly €125,000, so €250,000 can be hedged, but fractional contracts are unavailable and a precise match is usually impossible. Hedging costs money and makes operational separation from core strategy positions harder.

For most retail traders, the author does not recommend routine hedging: if exchange rates follow a random walk, gains and losses should net to zero over time but add return noise. Selective hedging based on favorable carry and/or trend forecasts is possible, but increases the implicit FX asset-class weight and may require reducing it in the core strategy. Institutions may prefer hedging because FX noise weakens benchmark correlation and can irritate investors; they also have large balances that can be hedged more accurately.

**Recommendation:** use explicit FX trading to avoid borrowing interest, tolerate unhedged-FX noise, and regularly exchange foreign-currency balances not needed for initial margin or likely variation margin back into the domestic currency.

For scale, the author describes a UK trader whose foreign-currency margins average 30% of account size. A 10% GBP appreciation against all used currencies would cause a 10% loss on margin, or roughly a 3% loss on notional capital; an equal gain is assumed equally likely. Since 2014 the author found annual FX gains/losses of this scale typical. If this noise is unacceptable, partial hedging should be considered where possible.

## Margin problems

With sensible risk management, shortages should be rare. The chapter explicitly defers procedures for them to the next chapter because they are failures of risk management.

## Compounding tactics

Backtests in the book show **non-compounded percentage returns**, but live trading with fixed capital is called extremely dangerous. Kelly-style risk targeting requires reducing position size after losses. A simple implementation sets notional capital equal to current account value.

The three alternatives are fixed capital (do not use), full compounding, and half compounding.

### Common simplified example and formula

Assumptions:

- Beginning capital: $500,000.
- A long-only version of strategy three, holding one imaginary instrument.
- At $500,000 capital, position is 500,000 contracts; the multiplier is deliberately tiny.
- Estimated instrument standard deviation is constant and there are no FX effects; only trading capital affects the optimal position.
- Initial price: $1; daily returns: +10%, +10%, −10%, +10%.
- Capital, prices, and target positions are recalculated daily.

\[
\text{Optimal position (contracts)} = \frac{\text{notional capital (currency)}}{\text{price (currency per contract)}}.
\]

This is a deliberately simplified formula applicable only under the listed assumptions.

### Fixed capital — do not use live

Notional capital stays $500,000, so target position value remains $500,000. After successive prices of $1.10, $1.21, and $1.089, target contracts are 454,545 (the source image prints 454,454), 413,223, and 459,137 respectively. Each daily 10% move is applied to the fixed $500,000 position value: account value progresses $500,000 → $550,000 → $600,000 → $550,000 → $600,000.

- Arithmetic daily returns sum to +20%, and with fixed capital final account gain is exactly 20%; this makes fixed-capital account curves easy to interpret.
- After gains, position becomes too small relative to account size; after losses it would be too large.
- The account becomes over-capitalised after gains and under-capitalised after losses.
- It violates risk targeting because bet size is not adjusted to stake size.

Stress case: a 5% loss each day for 20 days is $25,000 per day under fixed capital and wipes out $500,000. The chapter says never use fixed capital in a live account.

### Full compounding

Set notional capital equal to current account value. Under the example, the position remains 500,000 contracts each day because price and account value scale together.

| Day | Return | Profit/loss | Account/notional capital |
|---|---:|---:|---:|
| Start | — | — | $500,000 |
| 1 | +10% | +$50,000 | $550,000 |
| 2 | +10% | +$55,000 | $605,000 |
| 3 | −10% | −$60,500 | $544,500 |
| 4 | +10% | +$54,450 | $598,950 |

The sum of daily returns is +20%, but compounded return is a little below 20%: geometric mean return is

\[
\left[(1+10\%)\,(1+10\%)\,(1-10\%)\,(1+10\%)\right]-1 = 4.6\%
\]

per day, as stated in the footnote. Positions remain correctly scaled to account size. One source figure prints “500000 × $1.089 = $561,000” during day three; that multiplication does not equal the displayed account/notional capital of $544,500, so the figure contains an apparent numerical error.

In the 20-day, −5% stress case, both account and position shrink 5% daily: losses begin $25,000, $23,750, and $22,562.50. The account retains just over $179,000 after day 20. With a Kelly-criterion risk target, full compounding is stated to maximize expected geometric mean return and expected final account value.

Use it for institutions whose clients expect compounded returns and for retail traders not relying on the account for income. Additions or withdrawals should adjust notional capital by the same amount; this is automatic when fully capitalised and using account value as notional capital.

### Half compounding

The author's method resembles a hedge fund with 0% management fee and 100% performance fee above a **high watermark**. Cap notional capital at the starting maximum; treat profit above that maximum as withdrawable performance fee. If losses occur, subtract them from notional capital so position sizing remains risk-correct.

In the example:

| Day | Account value | Notional capital | Key behavior |
|---|---:|---:|---|
| Start | $500,000 | $500,000 | Fully capitalised. |
| 1, +10% | $550,000 | $500,000 maximum | Gain not compounded; target 454,545 contracts at $1.10. |
| 2, +10% | $600,000 | $500,000 maximum | Gain not compounded; target 413,223 contracts at $1.21. |
| 3, −10% | $550,000 | $450,000 | Reduce capital and target to 413,223 contracts at $1.089. |
| 4, +10% | $595,000 | $495,000 | Increase from $450,000 by $45,000, still below high watermark. |

- Above or at the high watermark, behavior resembles fixed capital; after losses it resembles full compounding.
- Gains are not compounded once notional capital is at its maximum.
- The account is always fully capitalised if losses begin immediately, otherwise over-capitalised.
- In the 20-day, −5% stress case it behaves like full compounding because it is below the maximum, retaining just over $179,000.
- When profitable, excess cash accumulates above notional capital. In the example this is $100,000 after day two; withdraw it regularly to avoid becoming substantially over-capitalised.

The chapter says half compounding is not ideal for steady monthly income unless the strategy is consistently profitable, and warns that relying on brokerage income for monthly pay is risky. Any performance-fee fraction may be used: 50% is given as an alternative.

## Practical checklist

1. Size positions from appropriate notional capital, not from margin capacity.
2. Keep enough immediately available free cash for plausible variation margin.
3. Fully capitalise the account unless there is a deliberate, understood exception.
4. Do not reach for yield with free cash unless the added risk, liquidity requirement, and total portfolio risk are explicitly accepted.
5. For foreign margin, decide between explicit conversion and borrowing; account for interest, FX exposure, and operational complexity.
6. Do not use fixed capital live. Match compounding method to whether account growth or profit extraction is the objective.
7. Under half compounding, withdraw accumulated excess cash on a regular basis.

## Glossary

Free cash; initial margin; variation margin; margin call; liquidation; notional capital; under-capitalisation; over-capitalisation; full capitalisation; FX trade option; FX borrow option; FX exposure; FX hedge; excess return; compounding; arithmetic mean return; geometric mean return; Kelly criterion; high watermark; performance fee; full compounding; half compounding.

## Explicit connections to other chapters

- **Part One:** prior discussion of risk targets, \(\tau\), Kelly risk targeting, non-compounded backtest reporting, and risk targeting.
- **Strategy three:** the compounding example uses a long-only variation with fixed target risk.
- **Next chapter:** procedures for margin shortages are deferred there.

## Source limitations and extraction notes

- The six worked-example figures contain no descriptive alt text; their numerical content was transcribed from the images.
- The source has apparent numerical or directional inconsistencies noted above: fixed-capital day-one target contracts, full-compounding day-three position value, and the FX-borrower depreciation/appreciation sentence. They are flagged rather than corrected in the source record.
