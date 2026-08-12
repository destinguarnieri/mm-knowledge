# Research Board

Status: in progress

Purpose: authoritative portfolio and routing view for Money Machine strategy research. This board answers **what programs exist, what independent work can run now, what needs Destin, and what decision each branch is trying to close**. Per-thread pages hold evidence and run pointers; Linear holds executable agent work.

Related process: [[research/trading/research_process_v2|Research Process V2]]

## Operating objective

Use parallel agents to reduce elapsed time from an idea to trustworthy economic evidence and ultimately positive net realized live P&L after costs. Human attention is scarce; agent execution is not. Focus means each workstream has a bounded question and clean evidence boundary, not that every other program must sit idle.

## Research system model

A one-signal → one-position backtest is a useful control, not Money Machine's assumed final strategy architecture. Research may advance any independent layer:

1. signal and feature primitives;
2. multi-signal market-state representation;
3. conditional or forward-price forecasts;
4. signal/forecast-to-position and path-dependent control;
5. execution and cost realization;
6. portfolio combination and live risk.

Do not interpret a weak primitive control as proof that the richer system is invalid. Do not interpret a good primitive as a complete deployable strategy either.

## Active research programs

`Ready` means a separate agent can pull the linked issue now. `In progress` means an agent is actually working it. `Human blocked` stops only the dependent branch, not the entire program.

| Program | Current evidence / state | Parallel agent work available now | Human dependency | Linear |
|---|---|---|---|---|
| [[research/trading/vwap-mean-reversion/vwap-mean-reversion|VWAP mean reversion]] | Gross signal retained; no immediate-execution mapping promoted. The frozen fractional-depth event study replicated minority outward continuation at every half-band step and meaningful partial reversals without a full next-band touch; depth is useful location context but does not yet select a position curve | After MON-168 verifies the pure schedule allocator, compare the binary control with linear distributed sizing and one preregistered favorable backloaded schedule. Keep readiness features, curve tuning, and live wiring out of that comparison | None for the bounded offline comparison after MON-168 | [Project](https://linear.app/money-machine/project/vwap-mean-reversion-research-ec37e0025905) · [MON-162](https://linear.app/money-machine/issue/MON-162/specify-and-evaluate-pnl-aware-vwap-resizing) · [MON-168](https://linear.app/money-machine/issue/MON-168/implement-and-verify-bounded-accumulationdistribution-schedules) |
| [[research/trading/emac-cross-10-200/emac-cross-10-200|EMA 10/200]] | **1D four-version runs reclassified as window-confounded diagnostics.** All mappings executed the same 96 fixed-floor cells, but the planner synthetically starts each batch at `common end − floor`, discarding up to the inter-floor gap of available history and potentially entire crypto regimes. Pairing remains useful for conditional implementation comparisons; breadth, winners, correlation, medians, and generalization are quarantined. Band traversal remains a separate supported branch | Resolve MON-214: define a maximum permitted loss of available calendar history, expose available/executed starts and loss per asset, inspect a plan-only audit, then rerun affected 1D cells. Only afterward resume winner overlap/correlation, `±0.05`/`±0.10`, and remaining MON-211 timeframes | MON-214's planner/history-retention contract requires Destin review; MON-165's full verdict still depends on MON-211 | [Project](https://linear.app/money-machine/project/ema-10200-research-b4f25ac9aabd) · [MON-214 planner redesign](https://linear.app/money-machine/issue/MON-214/redesign-binance-batch-planning-to-preserve-auditable-crypto-history) · [MON-210](https://linear.app/money-machine/issue/MON-210/complete-the-multi-asset-1d-emac-cross-control) · [MON-211](https://linear.app/money-machine/issue/MON-211/establish-the-unthresholded-continuous-emac-v1-baseline) · [MON-165 blocked](https://linear.app/money-machine/issue/MON-165/compare-thresholded-continuous-emac-v5-with-continuous-v1-and-v4) · [MON-157](https://linear.app/money-machine/issue/MON-157/monetize-the-emac-10200-escalation-ladder-edge-band-to-band-traversal) · [MON-167](https://linear.app/money-machine/issue/MON-167/compare-static-and-causal-dynamic-thresholds-in-the-ema-10200-program) |
| [[research/trading/ema_px_trend/strategy_ema_px_trend|EMA/PX agent-vision strategy]] | Implementation and focused tests exist; first development result was positive-Sharpe, but behavioral/economic interpretation is unresolved | Re-audit the implemented v1 against discriminating events and evaluate one bounded v2 candidate | Human-labeled codification remains separately blocked on unresolved Destin semantics | [MON-171](https://linear.app/money-machine/issue/MON-171/re-audit-ema-px-trend-v1-and-test-one-bounded-v2-candidate) · [MON-172](https://linear.app/money-machine/issue/MON-172/resolve-human-labeled-emapx-execution-semantics) |
| [[research/trading/multi-speed-ewmac/multi-speed-ewmac|Multi-speed EWMAC]] | Book-faithful code exists; the reported BTC lead lacks a durable saved-run reproduction and simple EMA controls reportedly outperform it | Reproduce the frozen baseline and controls without tuning | None | [MON-166](https://linear.app/money-machine/issue/MON-166/reproduce-the-frozen-multi-speed-ewmac-baseline-and-controls) |
| [[trading/positioning/size-distribution|Position/control research]] | Accumulation and distribution are confirmed as concurrent bounded transaction schedules; legacy absolute-target mappings may contain reusable curve math but have the wrong contract | Implement and deterministically verify the pure schedule allocator, inventory controller, and simultaneous-schedule lab before strategy wiring | Price- and signal-space fixtures pass all quantity, inventory, side, endpoint, and rounding invariants | [MON-168](https://linear.app/money-machine/issue/MON-168/implement-and-verify-bounded-accumulationdistribution-schedules) |
| [[trading/catalog_v1|Trading Catalog implementation queue]] | Catalog captures years of indicators, signals, anomalies, market-state concepts, controls, and trading styles; implementation/evaluation state is incomplete | Convert every catalog entry into a typed, status-bearing agent-pull queue; then implement/evaluate independent primitives in parallel | Destin only for genuinely missing definitions or priority decisions | [MON-169](https://linear.app/money-machine/issue/MON-169/convert-the-trading-catalog-into-an-implementation-and-evaluation) |
| Multi-signal market state and forecasting | Existing signals, QR references, and model ideas are not connected to the active strategy loop; current tests overuse one-signal → one-position controls | Define the first frozen multi-signal state plus forward-price baseline, keeping forecast evaluation separate from position policy | Target/horizon forks return to Destin only if existing context cannot resolve them | [MON-170](https://linear.app/money-machine/issue/MON-170/define-the-first-multi-signal-market-state-and-forward-price-baseline) |

## Shared research assets

| Asset | Role |
|---|---|
| Static/dynamic thresholds and band stepping | Reusable state representations and capture mechanisms; evaluate both independently and inside named programs. |
| [[engineering/backtest-strategies-index|Baseline strategy suite]] | Backtester sanity checks and control conditions. Simple strategies are controls, not the ceiling on strategy intelligence. |
| Papers and book extracts, including Carver and Ronnie Chen material | Sources for queueable features, models, controls, and complete strategy hypotheses. Extracted knowledge should flow into the catalog/implementation queue. |
| [[research/trading/alpha-inbox/overview|Alpha Inbox]] | High-throughput capture. Triage ideas into a program, catalog primitive, horizon program, or rejection without interrupting the current human task. |
| [[projects/agentic-research-loop-product-brief|Agentic Research Loop]] | Active agent-as-customer enablement. [MON-177](https://linear.app/money-machine/issue/MON-177/establish-research-run-artifact-workspace-and-contain-event-study) is the sole Ready foundation issue; MON-178–181 form the dependency-gated event-study evidence/inspection/acceptance path. [MON-182](https://linear.app/money-machine/issue/MON-182/decide-preservation-and-cleanup-of-legacy-tracked-event-study-outputs) is human-blocked on preservation of existing outputs. |

## Horizon programs

These remain visible so they are not forgotten. They may receive bounded definition or baseline work in parallel when an issue is independently executable; “horizon” means the full program is not yet a production commitment.

| Program | State | Resume condition |
|---|---|---|
| Karpathy-style continuous autoresearch | **horizon — parked** | Resume after the active agentic evidence/perception slice proves the manual alpha loop and exposes a repeated optimization or orchestration bottleneck worth automating |
| Vision/FSD-style model trading | **horizon — parked** | Resume with a bounded perception or policy hypothesis and a labeled evaluation set; do not combine perception, policy learning, and live execution in one first experiment |
| Large Financial Models | **horizon — parked** | Resume when a concrete prediction/control objective, proprietary data advantage, compute budget, and baseline comparison are defined |
| [[research/trading/weather-map/overview|Multiframe Forecasting Weather Map]] | **horizon — parked** | Resume when the first forecast target, confidence/calibration contract, graph relationship, deployment target, and baseline comparison are defined |
| Broad literature-to-strategy automation | **horizon — parked** | Resume when manual extraction-to-test repetition is proven limiting or a specific source presents a high-value candidate |

## Board operating rules

- **Parallelism is the default for independent agent work.** Each agent owns one bounded issue at a time; many agents may work different issues and programs simultaneously.
- **Human focus is not portfolio WIP.** Destin may concentrate on one review or ambiguity while autonomous work continues elsewhere.
- **Avoid collisions.** A Ready issue must name its question, fixed evidence surface, decision boundary, dependencies, and likely shared files. Work that would edit the same mechanism or consume the same holdout is sequenced or isolated first.
- **Lane is method, not priority.** Discretionary codification, capture engineering, open discovery, external-model reproduction, and cross-market extension receive no automatic ranking.
- **Validity, forecasting, control, and monetization stay separate.** Reject a failed mapping without erasing a supported signal or market-state finding.
- **Controls are intentionally simple.** One-signal → one-position tests isolate primitives; they do not define the maximum allowed strategy sophistication.
- **Catalog → queue.** Every catalog item should eventually carry implementation and evaluation state. Queueing a primitive does not claim it is alpha or authorize arbitrary combination with other primitives.
- **Board ↔ thread page:** update the affected program/workstream whenever evidence changes its state, blocker, dependency, or next decision.
- **Board ↔ Linear:** every executable active/Ready workstream needs a linked Linear issue. Every In Progress research issue must map to a board program or shared asset.
- **Linear holds execution, not scientific truth.** Reconcile per-thread evidence first, this board second, and Linear execution third.
- **Metrics remain in saved runs/UI.** The board records evidence state and decisions, not standard result tables.
- All current tested candidates are crypto-only so far. Cross-market work remains an explicit evidence axis, not an automatic gate before a crypto-specific candidate can proceed.
