# Research Board

Status: in progress

Purpose: authoritative portfolio view for Money Machine strategy research. This board answers **what is funded now, why, and what decision comes next**. Per-thread pages hold evidence and run pointers; Linear holds concrete execution.

Related process: [[research/trading/research_process_v2|Research Process V2]]

## Portfolio objective

Select and advance the shortest credible path to positive net realized P&L after costs. Strategy origin does not determine priority. Rank candidates from current evidence, expected net edge, operational fit, fragility, and distance to the next decisive economic test.

## Revenue candidates

Exactly one candidate may be `primary`.

| Rank | Candidate | Lane | Evidence state | Monetization state | Portfolio state | Next decisive step | Linear |
|---:|---|---|---|---|---|---|---|
| 1 | [[research/trading/vwap-mean-reversion/vwap-mean-reversion]] | Capture engineering | Broad 5m/15m Hyperliquid lead; 1m asset-selective | Survives recorded fees at 5m/15m; realistic slippage untested | **primary** | Reproduce frozen 5m/15m baseline under intended achievable slippage and a separate stress regime; promote, narrow, or reject each timeframe | [MON-159](https://linear.app/money-machine/issue/MON-159/run-vwap-5m15m-realistic-slippage-monetization-gate) |
| 2 | [[research/trading/emac-cross-10-200/emac-cross-10-200]] | Capture engineering / signal decomposition | Conditional band-to-band structure supported across assets and timeframes | No complete tradeable P&L series for the traversal mapping | **challenger** | Implement and evaluate the simplest distinct band-target strategy net of realistic costs | [MON-157](https://linear.app/money-machine/issue/MON-157/monetize-the-emac-10200-escalation-ladder-edge-band-to-band-traversal) |
| 3 | [[research/trading/ema_px_trend/strategy_ema_px_trend]] | Discretionary codification / agent vision | Strategy implementation and focused tests exist; intended-behavior parity and economic interpretation remain unresolved | Not decision-ready | **parked** | Resume when the primary and challenger are decided, or when Destin explicitly selects it; first re-establish intended behavior versus implementation | none funded |
| 4 | [[research/trading/multi-speed-ewmac/multi-speed-ewmac]] | External-model reproduction | Book-faithful baseline exists; one reported BTC lead lacks a durable run pointer and local EMA controls reportedly outperform it | Insufficiently tested | **parked** | Resume if a diversified trend benchmark is needed; reproduce the frozen baseline with a saved run before variants | none funded |

## Reusable mechanisms and research assets

These components may improve more than one candidate. They do not become primary work independently; attach them only when a candidate's evidence names the capture problem they solve.

| Component | Current state | Candidate use | Resume / use condition |
|---|---|---|---|
| Static and dynamic threshold logic | Static variants received limited testing; rolling signal-stat thresholds remain an open comparison | EMA 10/200; VWAP | Use only after the unchanged primary baseline reaches its cost gate, or as the bounded fix for a demonstrated turnover/capture problem |
| Band stepping / escalation logic | Conditional traversal structure is the strongest supported EMA signal finding | EMA 10/200; potentially other normalized signals | Funded through the EMA challenger, not as a generic framework project |
| [[trading/positioning/size-distribution]] | V1 exposed logic and continuity errors; confirmed economic intent exists, but path-dependent control semantics remain unresolved | Any continuous-position strategy | Resume when a primary candidate demonstrates that linear inventory allocation is the binding monetization problem |
| Citadel-inspired signal-to-position function | Promising conceptual work from the 2026-08-03 research inventory; not yet evaluated as a Money Machine mapping | Continuous-position candidates | Formalize only when attached to a named candidate and compared with its simpler mapping |
| [[trading/catalog_v1]] | Useful inventory and glossary; not a strategy specification | All lanes | Retrieve individual concepts as needed; do not turn the catalog into an implementation queue |
| [[engineering/backtest-strategies-index]] | Existing simple strategies provide controls and backtester sanity checks | All strategy research | Maintain as comparison controls; do not optimize merely to expand the suite |
| Papers and book extracts, including Carver and Ronnie Chen material | Source inventory exists; only selected ideas have implementations | External-model research | Pull a source into active work only when it supplies a testable candidate or mechanism relevant to the current revenue portfolio |

## Horizon programs

These remain visible so they are not forgotten, but they receive no current execution WIP.

| Program | State | Resume condition |
|---|---|---|
| Karpathy-style autoresearch / Agentic Research Loop | **horizon — parked** | Resume after repeated manual strategy-optimization loops show a measured throughput bottleneck and the objective, holdouts, and promotion gates are trustworthy |
| Vision/FSD-style model trading | **horizon — parked** | Resume with a bounded perception or policy hypothesis and a labeled evaluation set; do not combine perception, policy learning, and live execution in one first experiment |
| Large Financial Models | **horizon — parked** | Resume when a concrete prediction/control objective, proprietary data advantage, compute budget, and baseline comparison are defined |
| [[research/trading/weather-map/overview|Multiframe Forecasting Weather Map]] | **horizon — parked** | Resume when the first forecast target, confidence/calibration contract, graph relationship, deployment target, and baseline comparison are defined |
| Broad literature-to-strategy automation | **horizon — parked** | Resume when manual extraction-to-test repetition is proven limiting or a specific source presents a high-value candidate |

## Board operating rules

- **Portfolio state:** `primary` = sole active revenue candidate; `challenger` = next candidate if the primary closes or fails; `active` = funded supporting research for the primary; `parked` = preserved with an explicit resume condition; `closed` = decided; `horizon` = intentionally outside the current revenue loop.
- **Lane is method, not priority.** Discretionary codification, capture engineering, open discovery, external-model reproduction, and cross-market extension use different procedures but receive no automatic ranking.
- **Validity and monetization stay separate.** A valid signal with a losing first mapping remains capture-open; reject the mapping without erasing the signal.
- **One primary.** Promoting a new primary requires explicitly demoting, parking, or closing the previous one.
- **Board ↔ thread page:** update this row whenever evidence changes validity, monetization, portfolio state, blocker, or next decisive step.
- **Board ↔ Linear:** every `primary` or `active` item needs linked funded execution in Linear. Every `In Progress` research issue must map to a `primary`/`active` row or be bounded enablement for the primary.
- **Linear holds execution, not portfolio truth.** If Linear and this board disagree, reconcile the board from per-thread evidence first, then correct Linear.
- **Metrics remain in saved runs/UI.** The board records evidence state and decisions, not standard result tables.
- All current revenue candidates are crypto-only so far. Cross-market work remains an explicit evidence axis, not an automatic requirement before a crypto-specific candidate can proceed.
