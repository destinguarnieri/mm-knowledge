# Research Board

Living roster of active strategy-research threads. One row per thread — this page only points; per-thread state lives in each thread's two-layer doc, and metrics live in the backtest UI / saved runs (do not paste tables here). Update a row whenever that thread's living head changes.

Related process: [[research/trading/research_process_v2|Research Process V2]]

## Active threads

| Thread | Lane | Validity | Monetization | Confidence | Status | Next step |
|---|---|---|---|---|---|---|
| [[research/trading/ema_px_trend/strategy_ema_px_trend\|ema_px_trend]] | discretionary codification | v1 positive (HYPE 4H) | early | low | primary / active | 10 EMA_low integration, hold-confirmation at line, param tune, cross-asset OOS |
| [[research/trading/emac-cross-10-200/emac-cross-10-200\|EMA 10/200]] | capture engineering | leaning strongly yes (~80% time-in-money) | capture-open | med | active | mean-cycle capture variant vs flip-only control; continuous `emac_v5` |
| [[research/trading/vwap-mean-reversion/vwap-mean-reversion\|VWAP mean reversion]] | capture engineering | supported at 5m/15m (broad, 66–69/96 assets +); 1m asset-selective | net of fees: survives 5m/15m; realistic slippage untested (input ≈0) | med | active | realistic-slippage rerun on 5m/15m (config confirmed; MCP caps 32/batch) |

All three are crypto-only so far; cross-market (equities / other venues) extension is untested for each and is a first-class next axis per Research Process V2.

## Conventions

- **Status:** `primary` = next in line for live capital / canary — exactly one at a time, Destin's call; `active` = under research now; `parked` = promising but paused, must carry a "resume when X" note; `closed` = decided.
- **Validity vs Monetization** are the two separately-gated questions from Research Process V2 §2. A thread can be validity-strong while monetization is `capture-open` — that is a fundable state, not a failure.
- **Linear holds execution/backlog; this board is the synthesized state.** Each thread's doc links its Linear project/issue. Do not duplicate tasks or metrics here.
- **Reusable building blocks** (signals, features, capture mechanisms) can cross threads — e.g. signal-statistic overlays span EMA 10/200 and VWAP. Note cross-thread reuse in the relevant docs.

## Parked / closed

(none yet)
