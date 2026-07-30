---
title: "Risk Management"
chapter: 8
source: "Algorithmic Trading: Winning Strategies and Their Rationale"
status: "extracted"
---

# Chapter 8: Risk Management

## Chapter Overview

The chapter defines risk management as maximizing long-term equity growth while avoiding risk only where it impedes that objective. It covers constant leverage, Kelly optimization, non-Gaussian Monte Carlo optimization, historical-growth optimization, maximum-drawdown constraints, constant proportion portfolio insurance (CPPI), stop losses, and leading risk indicators.  
Source: pp. 169–186

## Learning Objectives

Inferred objectives:

- Choose leverage to maximize compounded growth under stated assumptions and constraints.
- Understand why constant leverage requires selling after losses and buying after gains.
- Compare drawdown control with CPPI and stop loss.
- Test strategy-specific leading risk indicators while guarding against data snooping.  
Source: pp. 169–186

## Key Concepts

### Constant leverage and ruin

The central requirement for the chapter’s leverage methods is constant leverage. If equity reaches zero, compounded growth is −100%, so a leverage that permits historical ruin cannot be optimal. After a loss, constant leverage requires liquidating exposure; after a gain it requires increasing exposure. This deleveraging can propagate losses among funds holding similar assets.  
Source: pp. 170–171

### Kelly as an upper bound

Kelly is presented under a Gaussian return assumption as the leverage that maximizes compounded growth with reinvestment. Mean/variance estimation error, nonstationarity, and non-Gaussian returns can cause overleverage and ruin; underleverage merely sacrifices some growth. The author commonly treats Kelly as an upper bound and cites half-Kelly as a routine conservative practice.  
Source: pp. 171–173

### Maximum drawdown

Drawdown is return from a historic high watermark. It is a nonlinear function of leverage: halving leverage need not halve maximum drawdown. Simulated returns provide more statistical significance but can miss serial correlation and include ultra-rare extremes; historical returns preserve realized correlation but are too limited to represent worst case.  
Source: pp. 178–180

### CPPI

CPPI reserves a fraction `$1-D$` of account equity as cash and applies the optimal strategy leverage to a trading subaccount initially equal to `$D$` of equity. At new high-water marks, reset the trading subaccount to `$D$` of total equity; after losses, do not replenish it. It is intended to cap total-account drawdown at `$-D$` while retaining substantial growth.  
Source: pp. 180–182

### Leading risk indicators

A leading indicator predicts next-period risk, unlike a contemporaneous risk indicator. Its usefulness is strategy-specific: VIX above 35 was beneficial in the cited stock buy-on-gap strategy yet destructive for the cited FSTX gap strategy. TED spread, HYG, MXN, ONN/OFF, commodity prices, Baltic Dry Index, and high-frequency order flow are candidates discussed, not universal rules.  
Source: pp. 184–186

## Mathematical Formulas

### Gaussian Kelly leverage

**Formula**

$$
f=\frac{m}{s^2}. \tag{8.1}
$$

**Variables**

- `$f$` — optimal leverage; gross market value per unit equity, dimensionless.
- `$m$` — mean excess return over the risk-free rate per bar; dimensionless return.
- `$s^2$` — variance of excess return per bar; return squared.

**Purpose:** Maximize compounded equity growth under the Gaussian-return approximation and full reinvestment.  
**Conditions and assumptions:** Future return distribution is assumed to match the past; strategy return is Gaussian; the account must avoid ruin.  
**Interpretation:** Higher mean permits more leverage; higher variance reduces it.  
**Source:** p. 172, Equation 8.1

### Multi-portfolio Kelly allocation

**Formula**

$$
F=C^{-1}M. \tag{8.2}
$$

**Variables**

- `$F$` — column vector of portfolio leverages from common equity.
- `$C$` — covariance matrix of portfolio returns.
- `$M$` — column vector of mean excess returns.

**Purpose:** Allocate buying power across strategies while accounting for covariance.  
**Conditions and assumptions:** Same Kelly/Gaussian framework; matrix invertibility is implicit. Broker/risk-manager gross leverage can constrain the solution.  
**Interpretation:** Correlation changes the allocation; gross leverage is `$\sum_i|F_i|$`, not net long-minus-short exposure.  
**Worked example:** Two independent strategies with annualized excess returns/volatilities 30%/26% and 60%/35% yield stated Kelly leverages 4.4 and 4.9. With a maximum leverage of 2, scaling them to 0.95 and 1.05 gives growth 0.82, while allocating all 2 to strategy 2 gives stated growth 0.96.  
**Source:** pp. 173–175, Equation 8.2 and Example 8.2

### Compounded growth rate under simulated returns

**Formula**

$$
g(f)=\left\langle\log(1+fR)\right\rangle. \tag{8.5}
$$

**Variables**

- `$g(f)$` — expected compounded growth rate per bar.
- `$f$` — leverage.
- `$R$` — unlevered strategy return per bar (not market-price return).
- `$langle\cdot\rangle$` — average over random samples of `$R$`.

**Purpose:** Numerically optimize leverage when return distributions may be fat-tailed or otherwise non-Gaussian.  
**Conditions and assumptions:** Risk-free rate is assumed zero for this expression; the chosen fitted distribution must be usable for sampling; `$1+fR$` must remain positive to avoid log/ruin.  
**Interpretation:** Average log wealth, not average arithmetic return, is optimized.  
**Worked example:** A Pearson-system fit to daily returns generates 100,000 simulated returns. The stated optimizer finds `$f\approx19$`, near a Kelly estimate of 18.4; at `$f=31$`, a return of −0.0331 implies ruin because `$1/0.0331=30.2$`.  
**Source:** pp. 175–177, Equation 8.5 and Boxes 8.1–8.3

### Gaussian growth-rate formulas cited in Example 8.2

**Formula**

$$
g=\frac{F^T C F}{2}. \tag{8.3}
$$

**Variables**

- `$g$` — annualized compounded growth rate in the example.
- `$F$`, `$C$` — Kelly leverage vector and covariance matrix as above.
- `$T$` — transpose.

**Purpose:** State the optimal growth rate under the example’s Gaussian/zero-risk-free-rate conditions.  
**Conditions and assumptions:** The book explicitly says Equation 8.3 applies only when the leverages used are optimal.  
**Interpretation:** In the example, the formula gives `$g=2.1$` at unconstrained Kelly leverage.  
**Source:** p. 174, Equation 8.3

**Source transcription note:** OCR makes Equation 8.4 unreadable in the supplied PDF text. The book reports its numerical result (`$g=0.82$`) for the scaled constrained allocation but this extraction does not reconstruct the missing expression.

## Methods and Procedures

### Constant-leverage rebalancing

1. Set target market value equal to target leverage times current equity.
2. Recalculate after each P&L period.
3. Sell exposure after losses and buy/add short exposure after gains to restore the target.
4. Apply maximum-drawdown and broker constraints separately.  
**Example:** `$100K` equity and leverage 5 gives `$500K` market value. After a `$10K` loss, market value is `$490K` but target is `$450K`, requiring `$40K` liquidation. After a subsequent `$20K` gain, target is `$550K`; from `$470K` current market value, add `$80K`.  
Source: pp. 170–171, Example 8.1

### Monte Carlo leverage optimization

1. Calculate mean, standard deviation, skewness, and kurtosis of backtest daily return vector `ret`.
2. Fit/simulate a Pearson-system distribution with `pearsrnd`; the example produces 100,000 `ret_sim` observations.
3. Define `g(f)=sum(log(1+f*R))/length(R)`.
4. Numerically minimize `-g` over a safe bracket using `fminbnd`.
5. Check the largest loss explicitly for ruin at candidate leverage.  
Source: pp. 175–177, Boxes 8.1–8.3

### Historical-growth optimization

Use the same `g` and bounded optimizer, but feed actual backtest returns `ret` rather than simulated returns. The example bounds `$f$` from 0 to 21 and obtains 18.4. The author warns this is ordinary backtest parameter optimization/data snooping and lacks the breadth of many realizations.  
Source: pp. 177–178, Box 8.4

### CPPI workflow

1. Choose a maximum permitted total-account drawdown `$-D$` and determine strategy leverage `$f$`.
2. Trade only a subaccount equal to `$D$` of total equity, at leverage `$f$`; retain `$1-D$` as cash.
3. On a new high-water mark, reset trading subaccount equity to `$D$` of total equity; otherwise do not move cash into it.
4. If the trading subaccount is exhausted, stop the strategy.
5. Apply only to one-strategy accounts; profitable strategies can otherwise subsidize a failing one.  
Source: pp. 180–182

### Stop-loss selection

For a position stop, exit when unrealized P&L breaches the threshold but permit later re-entry. For a strategy-level stop, cease trading after a drawdown threshold; the author considers CPPI preferable for that protection. For a mean-reversion strategy, set a stop wider than the maximum intraday drawdown in backtest, so it is not triggered by the data that caused survivorship bias but can address a future regime-change/black-swan loss. Momentum signals themselves act as continuously updated de facto stops.  
Source: pp. 182–184

## Derivations and Proofs

- The text states that Equation 8.1 follows under a Gaussian approximation and that differentiating the Gaussian form of Equation 8.5 reproduces Kelly; it does not supply the full derivation in this chapter. Source: pp. 171–176.
- CPPI is contrasted with simply applying `$fD$` leverage to total equity: with any drawdown, CPPI reduces order size faster and hence does not have the same pathwise return. The author says they do not know a mathematical proof that long-run growth is the same, but gives a simulation: 0.002484/day CPPI versus 0.002525/day for the alternative at `$D=0.5$`. Source: pp. 180–181.

## Worked Examples

### Constrained two-strategy allocation (Example 8.2)

Strategy 1: annualized mean excess return 30%, volatility 26%. Strategy 2: 60%, 35%. With zero correlation, stated Kelly leverages are 4.4 and 4.9 (gross 9.3). A leverage cap of 2 makes proportional scaling suboptimal in the example: allocating the full cap to strategy 2 raises stated growth from 0.82 to 0.96.  
Source: pp. 173–175

### Pearson-system Monte Carlo (Boxes 8.1–8.3)

The return moments fit a Pearson distribution of reported type 4, then 100,000 simulated returns are optimized. The reported maximum near 19 agrees closely with the 18.4 Kelly calculation.  
Source: pp. 175–177

### Drawdown calibration

For the simulated return sequence, unconstrained `$f=19.2$` yielded drawdown −0.999. Half leverage (9.6) still gave −0.963; approximately 2.7 (one-seventh) was required for drawdown about 0.5. Historical-return calibration instead needed only reduction to 13 to go below −0.49.  
Source: pp. 178–180

## Figures and Tables

- **Figure 8.1, Constrained Growth Rate `$g$` as Function of `$F_2$`:** plots the two-strategy constrained allocation and shows maximum at `$F_2=F_{max}=2$`. Source: p. 174.
- **Figure 8.2, Expected Growth Rate `$g$` as Function of `$f$`:** the Monte Carlo growth curve, with maximum near 19. Source: p. 178.

## Applications

- The text says Direxion triple-leveraged ETFs BGU and TNA tracking Russell indices with stated Kelly leverage about 1.8 present NAV-to-zero danger for buy-and-hold investors. Source: pp. 172–173.
- VIX `$>35$` was a poor-risk warning for FSTX opening gaps (annualized return 2.6%, Sharpe 0.16) but a favorable condition for the Chapter 4 buy-on-gap stock strategy (17.2%, Sharpe 1.4). Source: p. 184.
- TED spread measures bank-default risk; HYG, MXN, ONN/OFF, commodity inputs, Baltic Dry Index, and order flow are discussed as possible indicators needing testing. Source: pp. 184–186.

## Assumptions, Limitations, and Edge Cases

- All leverage methods assume future market returns resemble past returns; many additionally assume strategy returns are stationary, and Kelly assumes Gaussian strategy returns. Source: p. 170.
- Portfolio Kelly scaling to a broker cap is not generally constrained-growth optimal. Source: pp. 173–175.
- Pearson fits retain four moments only and can miss higher/infinite moments; fitting more can add data-snooping bias. Source: pp. 175–176.
- CPPI and stops cannot protect against an overnight gap or suspended market; options may mitigate expected closure risk but are costly. Source: pp. 181–182.
- Stops may execute far past their intended threshold on reopening, and can be ineffective in a liquidity vacuum such as the May 6, 2010 flash crash/stub quotes. Source: pp. 182–183.
- Risk-indicator crises are rare, making indicator backtests especially vulnerable to data snooping; financial indicators do not predict natural/nonfinancial disasters. Source: p. 186.

## Common Mistakes and Warnings

- Treating loss aversion itself as the objective rather than long-term growth. Source: p. 169.
- Using full estimated Kelly as an imperative instead of recognizing estimation error and the consequence of overleverage. Source: pp. 171–172.
- Scaling a multistrategy Kelly vector proportionally without checking constrained optimum. Source: pp. 173–175.
- Assuming drawdown scales linearly with leverage. Source: pp. 178–179.
- Applying CPPI to a multistrategy account where winners conceal a persistently failing strategy. Source: p. 182.
- Concluding that stops never help mean reversion: that result contains survivorship bias when regime changes are excluded from backtests. Source: pp. 182–184.

## Key Takeaways

- Constant leverage is foundational but mechanically forces procyclical rebalancing.
- Half-Kelly is presented as a practical conservative choice; fat tails motivate simulation-based optimization.
- A hard drawdown target requires CPPI or a strategy-level stop, not merely proportionally lower leverage.
- Mean-reversion stops should be outside backtest intraday drawdowns; momentum exits naturally respond to reversal.
- Risk indicators must be tested per strategy and are highly susceptible to data-snooping bias.  
Source: pp. 169–186

## Glossary

| Term | Definition | Source |
|---|---|---|
| Leverage | Gross market value relative to equity. | pp. 170–173 |
| Kelly leverage | Gaussian optimal leverage `$m/s^2$`. | p. 172 |
| Half-Kelly | One-half of Kelly leverage, used to reduce overestimation risk. | p. 172 |
| Gross leverage | `$\sum_i |F_i|$`; absolute sum of long and short market values divided by equity. | p. 173 |
| Maximum drawdown | Return from historic high watermark. | p. 178 |
| CPPI | Constant proportion portfolio insurance: cash reserve plus leveraged trading subaccount. | pp. 180–182 |
| Position stop | Exits one position on unrealized P&L threshold but permits re-entry. | p. 182 |
| Leading risk indicator | Predictor of next-period risk rather than a contemporaneous measure. | p. 184 |
| TED spread | Three-month LIBOR minus three-month T-bill rate. | pp. 184–185 |

## Connections to Other Chapters

- Chapter 4’s buy-on-gap stock strategy is used to show that VIX risk is strategy-specific. Source: p. 184.
- Chapter 7’s FSTX opening-gap strategy is used as the contrasting VIX example; Chapter 7 order flow is presented as a short-term risk signal. Source: pp. 184–185.
- Example 5.1 supplies the mean-reversion return series used for the Monte Carlo leverage illustration. Source: p. 176.

## Open Questions or Extraction Issues

- Equation 8.4 is visibly incomplete/unreliable in the supplied text extraction. Its result and context are retained, but its formula is not invented.
- In the PDF’s OCR text, Equation 8.3 is rendered as shown above; readers needing publication-grade symbol verification should inspect the original p. 174.

## Quality-control checklist

- [x] Entire assigned chapter examined (pp. 169–186).
- [x] All major headings represented.
- [x] Important formulas, symbol definitions, conditions, and examples captured.
- [x] Figures and code boxes described.
- [x] Source locators included where available.
- [x] Only supplied-text content used; OCR ambiguity is flagged.
