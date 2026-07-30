---
title: "Intraday Momentum Strategies"
chapter: 7
source: "Algorithmic Trading: Winning Strategies and Their Rationale"
status: "extracted"
---

# Chapter 7: Intraday Momentum Strategies

## Chapter Overview

The chapter develops short-horizon momentum models. In contrast with the month-or-longer horizons typical of interday momentum, intraday models can yield more frequent independent signals and may avoid the post-crisis weakness described for longer-horizon momentum. The book attributes intraday momentum to news diffusion, fund rebalancing, order-book imbalance, and triggered stops; persistence of futures roll return is the stated exception because it is too small and slow intraday.  
Source: pp. 155–156

## Learning Objectives

Inferred objectives:

- Construct and test opening-gap, event-driven, leveraged-ETF, and order-book momentum strategies.
- Identify the mechanics, data requirements, and failure modes of short-horizon breakouts.
- Distinguish legitimate predictive signals from execution-sensitive high-frequency tactics.  
Source: pp. 155–168

## Key Concepts

### Breakout and stop cascades

A breakout is a price exceeding a trading range. Overnight/weekend gaps may trigger many differently placed stop orders simultaneously; their execution can cascade into more stops farther from the opening price. This is one explanation for opening-gap momentum.  
Source: pp. 155–157

### News-driven drift

The text treats a material corporate announcement as prompting a reassessment toward a new equilibrium price. The resulting post-announcement move may persist intraday. Earnings announcements, guidance, analyst changes, same-store sales, airline load factors, M&A, index-composition changes, and some macro announcements are discussed. Recent tests in the text suggest that some formerly multiday effects have shortened to intraday.  
Source: pp. 157–163

### Leveraged-ETF rebalancing

A constant-leverage ETF must buy underlying exposure after an up move and sell after a down move near the close. The book says this creates same-direction momentum in the underlying; it applies for both leveraged long and inverse funds because an inverse fund losing equity after an index rise must reduce its short position (buy). Investor flows can offset this effect.  
Source: pp. 163–164

### Bid/ask imbalance and order flow

Bid size materially larger than ask size implies an expected uptick, and conversely. Order flow is signed transaction volume: purchases at the ask are positive and sales at the bid are negative. A large, one-directional flow may reveal informed urgency, prompting market makers to adjust quotes.  
Source: pp. 164–168

## Mathematical Formulas

### Opening-gap entry thresholds (Example 7.1)

**Formula**

$$
\text{long}_t = \left(O_t > H_{t-1}\left[1+z\sigma^{(90)}_{C2C,t-1}\right]\right), \qquad
\text{short}_t = \left(O_t < L_{t-1}\left[1-z\sigma^{(90)}_{C2C,t-1}\right]\right)
$$

$$
r_t=p_t\frac{O_t-C_t}{O_t}, \qquad p_t\in\{-1,0,1\}.
$$

**Variables**

- `$O_t$, $H_t$, $L_t$, $C_t$` — open, high, low, and close on day `$t$`; price units.
- `$z$` — `entryZscore`, set to `0.1` in the example; dimensionless.
- `$sigma^{(90)}_{C2C,t-1}$` — prior 90-day moving standard deviation of close-to-close returns; dimensionless return.
- `$p_t$` — long/flat/short position selected at the open.
- `$r_t$` — intraday strategy return from open to close.

**Purpose:** Trade a gap beyond the prior high or low by a volatility-scaled threshold, then exit at the same close.  
**Conditions and assumptions:** Daily OHLC data; the moving standard deviation is lagged one day; execution is assumed at the stated open/close.  
**Interpretation:** A positive gap above the prior high triggers long; a negative gap below the prior low triggers short.  
**Worked example:** For FSTX, the cited backtest reports APR 13% and Sharpe ratio 1.4 from July 16, 2004 to May 17, 2012.  
**Source:** p. 156, Example 7.1

### Post-earnings announcement drift (PEAD) thresholds (Example 7.2)

**Formula**

$$
r^{C2O}_{t,i}=\frac{O_{t,i}-C_{t-1,i}}{C_{t-1,i}},
$$

$$
\text{long}_{t,i}=\left(r^{C2O}_{t,i}\ge0.5\sigma^{(90)}_{C2O,t,i}\right)\land E_{t,i},
\qquad
\text{short}_{t,i}=\left(r^{C2O}_{t,i}\le-0.5\sigma^{(90)}_{C2O,t,i}\right)\land E_{t,i},
$$

$$
r_t=\frac{1}{30}\sum_i p_{t,i}\frac{C_{t,i}-O_{t,i}}{O_{t,i}}.
$$

**Variables**

- `$O_{t,i}$`, `$C_{t,i}$` — opening and closing price of stock `$i$` on day `$t$`.
- `$r^{C2O}_{t,i}$` — previous-close-to-current-open return.
- `$sigma^{(90)}_{C2O,t,i}$` — 90-day moving standard deviation of that return.
- `$E_{t,i}$` — true when the earnings announcement was after the previous close and before today’s open.
- `$p_{t,i}$` — selected position (`$1$`, `$-1$`, or `$0$`).
- `$30$` — maximum number of positions in the cited test; the author notes this is a degree of look-ahead bias.

**Purpose:** Trade the open-to-close continuation following an overnight earnings announcement with an unusually large gap.  
**Conditions and assumptions:** Requires reliable historical announcement timestamps, not merely dates; positions are liquidated at the same close.  
**Interpretation:** The market’s opening reaction, rather than an independent judgment of earnings quality, determines direction.  
**Worked example:** S&P 500 universe, January 3, 2011–April 24, 2012: APR 6.7%, Sharpe 1.5; the author says fourfold leverage could make the annualized average return near 27%.  
**Source:** pp. 158–162, Example 7.2

## Methods and Procedures

### Opening-gap strategy

1. Estimate a lagged 90-day close-to-close volatility.
2. At the open, go long only above prior high times the upper threshold; go short only below prior low times the lower threshold.
3. Hold to that day’s close and compute return using opening price as denominator.
4. For currencies, define open/close deliberately; the GBPUSD example uses 5:00 p.m. ET close and 5:00 a.m. ET London open.  
Source: pp. 156–157

### Earnings-calendar selection and PEAD backtest

1. For each date and stock universe, retrieve announcements from the prior date and current date.
2. Keep prior-date announcements marked AMC or explicit PM time, and current-date announcements marked BMO or explicit AM time.
3. Create the `$T\times N$` logical announcement array; exclude announcements that occur after today’s open.
4. Compute the gap and its 90-day moving standard deviation; trade only earnings names whose gap exceeds ±0.5 standard deviations.
5. Equal-weight via the stated 30-position divisor and close positions the same day.  
Source: pp. 158–161, Box 7.1 and Example 7.2

### Leveraged-ETF close strategy

1. Measure return from prior close to 15 minutes before market close.
2. Buy DRN above +2%; sell below −2%; otherwise remain flat.
3. Exit at the close. The stated DRN test, October 12, 2011–October 25, 2012, produced APR 15% and Sharpe 1.8.  
Source: pp. 163–164

### High-frequency implementations described

- **Ratio trade (pro-rata markets):** join a disproportionately large bid; after fill, sell after an uptick or at best ask if spread exceeds round-trip commission. A non-moving bid can allow exit at original best bid with commission loss only.
- **Ticking / quote matching:** when spread exceeds two ticks, buy at best bid plus one tick, then offer at best ask minus one tick. It requires round-trip commission below spread minus two ticks.
- **Flipping / momentum ignition:** place a large bid and small ask to induce others to buy, fill the small ask, then cancel the large bid. The author identifies fill risk and deliberately deceptive mechanics.
- **Stop hunting:** sell near a support level to try to trigger clustered sell stops, then cover after the continuation. Resistance is symmetric.
- **Order-flow signal:** classify transaction at bid/ask, sum or average signed flow over a look-back window, and predict direction.  
Source: pp. 164–168

## Derivations and Proofs

The chapter gives mechanism-based reasoning rather than formal derivations: stop execution creates additional price pressure; slow information diffusion generates drift; constant leverage mechanically forces procyclical ETF rebalancing; and order-book/order-flow imbalance transmits information into quotes.  
Source: pp. 155–168

## Worked Examples

### FSTX opening gap

Use `entryZscore=0.1`, lagged 90-day close-to-close standard deviation, and long/short breakout conditions in Example 7.1. The position is `$1$`, `$-1$`, or `$0$` and is held open-to-close. Reported FSTX result: APR 13%, Sharpe 1.4.  
Source: p. 156, Example 7.1

### GBPUSD opening gap

With close at 5:00 p.m. ET and open at 5:00 a.m. ET, the same framework reported APR 7.2% and Sharpe 1.3% from July 23, 2007 to February 20, 2012.  
Source: p. 157

### PEAD

The procedure and equations above constitute Example 7.2; its 30-position normalizer is chosen from the backtest maximum and explicitly noted as mild look-ahead bias. Overnight returns were negative on average in the cited test, so holding overnight did not add profits.  
Source: pp. 160–162

## Figures and Tables

- **Figure 7.1, Equity Curve of FSTX Opening Gap Strategy:** cumulative equity curve for Example 7.1. Source: p. 157.
- **Figure 7.2, Cumulative Returns Curve of PEAD Strategy:** cumulative return curve for the S&P 500 PEAD backtest. Source: p. 161.
- **Figure 7.3, Ticking Strategy:** Best ask and bid are separated by more than two ticks. Buy at `$B$` (bid + one tick), seek sale at `$S$` (ask − one tick), and if necessary sell at `$S'$` for a one-tick loss. Source: p. 165.

## Applications

The chapter applies intraday momentum to FSTX futures, GBPUSD, S&P 500 stocks after earnings, DRN (as a leveraged instrument), and order-book-driven trading. It also says index additions/deletions create immediate momentum and reports no significant EURUSD momentum from the macro events tested, while citing older GBPUSD evidence lasting at least 10 minutes.  
Source: pp. 156–168

## Assumptions, Limitations, and Edge Cases

- Long-horizon momentum has fewer independent signals and may underperform after crises; intraday strategies are presented as avoiding those particular drawbacks. Source: p. 155.
- PEAD requires announcement times; date-only event data creates wrong triggers. Source: pp. 158–160.
- The 30-position PEAD denominator is a look-ahead bias. Source: p. 161.
- ETF cash flows can neutralize mechanical rebalance momentum. Source: p. 164.
- Quote matching can fail if the original bid is canceled or is a trap. Flipping can result in a large unwanted fill. Source: pp. 165–166.
- High-frequency profit is framed as coming from slower participants; if only equally fast traders remain, average net profit is zero. Source: p. 166.
- Currency order flow is difficult to observe because many dealers do not report transaction prices; currency futures may be necessary. Source: pp. 167–168.

## Common Mistakes and Warnings

- Do not assume an event effect remains multiday; the author’s newer tests often found intraday horizons. Source: pp. 161–163.
- Do not use news that arrives after the current open as an opening trade trigger. Source: pp. 158–160.
- Include transaction costs and execution risk in ticking; spread alone is insufficient. Source: p. 165.
- Treat apparent book pressure cautiously: displayed orders can be canceled and may be strategic. Source: pp. 165–166.

## Key Takeaways

- Intraday momentum can arise from stop cascades, event diffusion, leveraged-ETF rebalancing, and microstructure signals.
- Breakout gaps can work on selected futures/currencies; PEAD uses overnight timing plus abnormal opening gap.
- Bid/ask imbalance and signed order flow are short-term predictors but demand detailed, timely data and realistic execution modeling.
- Stop hunting, flipping, and quote tactics carry explicit adverse-selection, cancellation, and fill risks.  
Source: pp. 155–168

## Glossary

| Term | Definition | Source |
|---|---|---|
| Opening gap | Difference between the open and prior trading range used as a breakout trigger. | pp. 156–157 |
| PEAD | Post-earnings announcement drift: continuation after an earnings reaction. | pp. 157–162 |
| AMC / BMO | After-market-close / before-market-open earnings timing labels. | pp. 158–160 |
| Ratio trade | Pro-rata-market bid-joining trade based on bid/ask size imbalance. | p. 165 |
| Ticking / quote matching | Buy at bid + one tick and attempt sale at ask − one tick. | pp. 165–166 |
| Flipping | A momentum-ignition tactic using a large displayed bid and small ask. | p. 166 |
| Stop hunting | Attempt to exploit clustered stop orders near support/resistance. | p. 167 |
| Order flow | Signed transaction volume; ask-side buys positive, bid-side sells negative. | pp. 167–168 |

## Connections to Other Chapters

- Chapter 4’s stock buy-on-gap model is explicitly contrasted as mean reverting; this chapter examines the opposite gap-momentum case. Source: p. 156.
- Chapter 6’s causes of momentum and forced mutual-fund trades are invoked for intraday effects. Source: pp. 155, 162.
- Chapter 7’s order-flow discussion is explicitly used as a risk-indicator connection in Chapter 8. Source: p. 185.

## Open Questions or Extraction Issues

- The supplied PDF’s MATLAB code is OCR-extracted with typography artifacts; equations above normalize only the code’s unambiguous arithmetic and preserve its stated logic.
- The book describes potentially manipulative high-frequency tactics; this file records the textbook’s description and risks, not an endorsement or implementation recommendation.

## Quality-control checklist

- [x] Entire assigned chapter examined (pp. 155–168).
- [x] Major headings and subsections represented.
- [x] Important formula/code logic and symbols captured.
- [x] Examples, figures, and constraints included.
- [x] Source locators included.
- [x] No external information added.
