# Current Checkpoint

Date: 2026-08-03

Company frame: [[company/money-machine-360|Money Machine Operating Context]].

## Active Revenue Proof

- **Objective:** positive net realized live P&L after costs over a founder-set proof period.
- **Proof period:** not yet set; Destin sets it before live evaluation begins.
- **Company phase:** revenue-candidate selection and monetization. Strategy origin does not determine priority.
- **Strategy / experiment:** VWAP mean reversion on Hyperliquid, with `5m` and `15m` treated as separate primary configurations.
- **Observed blocker:** the broad baseline results include fees but used effectively zero slippage. Realistic-slippage survival is the decisive monetization uncertainty.
- **Next action:** reproduce the frozen `5m`/`15m` baseline under the intended achievable execution-cost regime and a separate stress regime, then promote, narrow, or reject each timeframe.
- **WIP:** one primary revenue outcome unless Destin explicitly expands it.

## Current Engineering State




## Current Decision

VWAP mean reversion is the primary revenue candidate because it is presently closest to a decisive economic test. EMA 10/200 band traversal is the challenger because its conditional signal structure is supported but lacks a tradeable P&L series. Discretionary codification, multi-speed EWMAC, and other candidates remain available but are not privileged by origin. The Agentic Research Loop, vision/FSD trading, and Large Financial Models remain horizon programs until the active revenue loop shows they are the highest-value next investment.

## Verification

- Linear MON-155 (fee/slippage cost semantics) is Done.
- Linear MON-156 (cold batch acceleration) is Done.
- Linear MON-145 (agent access to UI-owned saved runs) is Done.
- The Research Board is rebuilt around revenue candidates, reusable mechanisms, and horizon programs.
- Linear is reconciled: VWAP is In Progress through MON-159; EMA traversal remains the High/Backlog challenger through MON-157; stale category/platform projects were retired.

## Next Action

Execute [MON-159](https://linear.app/money-machine/issue/MON-159/run-vwap-5m15m-realistic-slippage-monetization-gate), preserving the frozen baseline before testing thresholds, signal statistics, or nonlinear position controls.
