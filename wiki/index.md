# Money Machine Knowledge Index

Purpose: routing map for Money Machine's agent-readable knowledge graph. Agents should start here, then follow Obsidian-style wikilinks and use QMD search when exact routing is unclear.

## Core Pages

- [[company/money-machine-360|Money Machine Operating Context]] — canonical company frame, revenue proof, work lanes, and decision standard.
- [[sessions/current-checkpoint|Current Checkpoint]] — active strategy, proof period, blocker, evidence, and next action.
- [[ops/linear-operating-system|Linear Operating System]] — issue intake, execution state, and WIP rules.
- [[trading/pmax|P_Max]] — foundational model of market opportunity: extractable value is positive and computable, so "no edge" is not a finding. Defines the constraint ladder, capture ratio, and the gap decomposition (information / cost / policy) that every research result must supply. Mandatory reading.
- [[trading/catalog_v1|Trading Catalog]] — Destin's inventory of indicators, anomalies, market-state inputs, controls, execution styles, and concepts. It is both the glossary of record and the source for a typed implementation/evaluation queue. A queued primitive is not automatically alpha and must not be combined into a strategy without a separate hypothesis.
- [[research/trading/catalog_queue|Trading Catalog Implementation and Evaluation Queue]] — stable agent-pull records for every catalog primitive, including implementation evidence, provisional first-pass measurements, semantic-review gates, dependencies, and queue state.
- [[research/trading/research_process_v2|Research Process V2]] — current quant research protocol: lane router + evidence ladder, signal-validity/monetization split, symmetric kill/upside framing, dual costs, cross-market generalization. (Supersedes V1, removed 2026-08-28; history in the session changelog.)
- [[research/trading/study-menu|Study Menu]] — the named set of event-study shapes, when each applies, and what each is structurally unable to see. Choose from it rather than copying a neighbouring study.
- [[research/trading/agentic_research_playbook|Agentic Research Playbook]] — **first draft, not current process.** Design sketch for a future autonomous solo research loop; rework deferred. Use the `capture-engineer` skill for per-cycle execution and [[research/trading/research_process_v2|V2]] for process.
- [[projects/agentic-research-loop-product-brief|Agentic Research Loop Product Brief]] — agent-as-customer product contract for typed research-run evidence, bounded extraction, deterministic chart rendering, annotations, and the event-study vertical slice.
- [[research/trading/example_research_directory/example_research_doc|Example Research Doc]] — style reference for the two-layer research file (living head + append-only tail) per Research Process V2.
- [[research/trading/research_index|Research Board]] — living roster of active research threads (lane, validity/monetization state, status, next step); read this first to see what research is live.
- [[research/trading/alpha-inbox/overview|Alpha Inbox]] — low-friction capture funnel for new alpha ideas; inbox entries are not research commitments or Linear tasks.
- [[research/trading/weather-map/overview|Multiframe Forecasting Weather Map]] — parked long-horizon concept for probabilistic timeframe × horizon price paths, graph topology, and traversal-aware trading.
- [[research/trading/emac-cross-10-200/emac-cross-10-200|EMA Cross 10/200 Research]] — active BTC timeframe scan, followed by multi-asset screening if the baseline remains coherent.
- [[research/trading/vwap-mean-reversion/vwap-mean-reversion|VWAP Mean Reversion Research]] — active multi-branch program; no current immediate-execution mapping is promoted.
- [[research/trading/vwap-mean-reversion/event-study-findings-audit|VWAP Event-Study Findings Audit]] — interpreted audit of the dual-domain, fractional-depth, and signed depth-response studies; new event-study design is paused pending review.
- [[research/trading/multi-speed-ewmac/multi-speed-ewmac|Multiple Trend Following Rules (Strategy Nine)]] — book-faithful multi-speed EWMAC baseline, crypto evaluation assumptions, and staged research direction.
- [[research/trading/emac-cross-10-200/event_study_anchor_findings|EMAC Event Study — Anchor Findings]] — interpreted verdicts from the signal-stats event study anchor run; holdout pending.
- [[research/trading/ema_px_trend/codification|EMA/PX Trend Continuation Codification]] — running chart-led specification for Destin's short-side EMA/PX discretionary mapping, with long-side semantics still pending.
- [[projects/ema_hilo_200_reentry/hype-ema-hilo-200-reentry-codification|HYPE EMA High/Low 200 Re-entry Codification]] — accepted simple HYPE 4H close-driven direction, stop, and re-entry mapping; implemented locally with baseline viability pending.
- [[research/trading/ema_px_trend/blind_pattern_match|EMA/PX Blind Pattern Match (Track 3)]] — agent pattern-matches unlabeled HYPE 4H charts (10 EMA_low / 200 EMA_close) window by window, updating priors toward a codified strategy.
- [[research/trading/ema_px_trend/strategy_ema_px_trend|ema_px_trend Strategy Doc]] — code walkthrough, rule semantics, dev-set discriminating events, and v2 candidates for the codified Track 3 strategy (first run: positive Sharpe).
- [[research/trading/quantile_regression/qr-trading-reference|Quantile Regression Trading Reference]] — extracted external QR trading tables (ranked knobs / IR impact + decision layer vs raw-signal failure modes); draft, not MM-validated.


## Active Projects

- [[projects/agentic-research-loop-product-brief|Agentic Research Loop]] — active bounded enablement project; first prove one event-study loop through MCP without Browser Use or generated artifacts in source.
- [[research/trading/vwap-mean-reversion/vwap-mean-reversion|VWAP Mean Reversion Research]] — active branches for slope/regime filtering, PnL-aware resizing, wide-stop risk, longer history, and later passive-fill modeling.
- [[research/trading/emac-cross-10-200/emac-cross-10-200|EMA Cross 10/200 Research]] — active parent program spanning controls, signal statistics, thresholds, traversal, continuous/nonlinear position control, and selection.
- [[research/trading/research_index|Research Board]] — the complete set of parallel Ready/In Progress programs, shared assets, dependencies, and horizon work.

## Wiki Areas

Canonical markdown lives under `wiki/`:

- `wiki/company/` — canonical company operating context.
- `wiki/agents/templates/` — the optional managed-worker brief and coding-execution reference.
- `wiki/ops/` — operating runbooks, process notes, Linear operating system.
- `wiki/engineering/` — stable engineering architecture, contracts, inventories, implementation context, and invariants; not ticket or implementation plans.
  - [[engineering/backtest-strategies-index|Backtest Strategies Index]] — light inventory of registered backtest strategy implementations (registered name, class, file, key params).
- `wiki/quant/` — quantitative research notes.
- `wiki/research/trading/` — strategy research protocol and per-project research docs (`research_process_v2` current; per-program research directories).
- `wiki/trading/` — trading language and discretionary/strategy context.
  - [[trading/catalog_v1|Trading Catalog]] — Destin's draft catalog of his hand-trading tools and vocabulary; the glossary of record for his terms.
  - [[research/trading/catalog_queue|Trading Catalog Implementation and Evaluation Queue]] — operational queue derived from the catalog without changing its wording or maturity.
  - `wiki/trading/entry/` — reusable discretionary entry and sizing primitives.
  - [[research/trading/positioning/size-distribution|Size Distribution]] — confirmed price-leg inventory-allocation intent (Higher/Lower + curve + amount), underwater linear-average problem, and unaccepted experimental signal-target implementation.
- `wiki/concepts/` — cross-cutting domain concepts and agent procedures.
- `wiki/projects/` — active initiative context, project-level synthesis, and bounded execution plans.
- `wiki/decisions/` — durable decision records.
- `wiki/sessions/` — promoted session summaries and current checkpoint / change log.
- `wiki/vendors/` — vendor/API specs and access notes (exchange limits, geo, market-data hosts). Named `vendors/` because QMD hard-excludes directories named `vendor`.

## Vendors

- [[vendors/hyperliquid-api-weightings|Hyperliquid API Weightings]] — HL rate limits and candleSnapshot weight planning.
- [[vendors/binance-market-data-access|Binance Market Data Access]] — global Binance spot vs futures hosts, US geo block, `data-api.binance.vision` for research/backtest spot candles; JP trading egress; perps need non-restricted IP.

## Routing Rules

- For current execution state, check `wiki/sessions/current-checkpoint.md` and `wiki/sessions/session-change-log.md`.
- For execution/backlog truth, check Linear.
- For durable project synthesis, update this wiki.
- Put active project or ticket plans in `wiki/projects/`; promote stable conclusions to the relevant engineering, decision, or operating page after delivery.
- For broad retrieval, use QMD over the wiki, then retrieve the matching markdown pages before answering.

## Open Maintenance

- Add backlinks and related links as pages stabilize.
- Add QMD collection context descriptions after the core wiki skeleton settles.
- Use `scripts/check_wikilinks.py` to verify links after wiki edits.
