# Money Machine Knowledge Index

Purpose: routing map for Money Machine's agent-readable knowledge graph. Agents should start here, then follow Obsidian-style wikilinks and use QMD search when exact routing is unclear.

## Core Pages

- [[company/money-machine-360|Money Machine Operating Context]] — canonical company frame, revenue proof, work lanes, and decision standard.
- [[sessions/current-checkpoint|Current Checkpoint]] — active strategy, proof period, blocker, evidence, and next action.
- [[ops/linear-operating-system|Linear Operating System]] — issue intake, execution state, and WIP rules.
- [[research/trading/research_process_v1|Research Process V1]] — repeatable quant strategy research protocol from idea card through candidate handoff.
- [[research/trading/example_research_directory/example_research_doc|Example Research Doc]] — style reference for structured research files with timestamped write logs.
- [[research/trading/emac-cross-10-200/emac-cross-10-200|EMA Cross 10/200 Research]] — active BTC timeframe scan, followed by multi-asset screening if the baseline remains coherent.
- [[projects/ema_px_trend/codification|EMA/PX Trend Continuation Codification]] — running chart-led specification for Destin's short-side EMA/PX discretionary mapping, with long-side semantics still pending.
- [[trading/entry/123|123 Entry]] — reusable breakover, pullback, go entry lifecycle and sizing primitive.

## Active Projects

- [[projects/ema_px_trend/codification|EMA/PX Trend Continuation Codification]] — provisional discretionary-alpha transfer spec for short-side trend continuation, countertrend absorption, PX scale-out, and close-only implementation handoff.
- [[projects/MON-144-hl-1d-candle-overflow.plan|MON-144 HL 1d Candle Overflow]] — widen live `candle`/`indicatorvalue` `tf_sec` for daily bars and route Hyperliquid research cache through `backtest_candle`.
- [[projects/MON-142-backtest-risk-metric-contract.plan|MON-142 Backtest Risk Metric Contract]] — explicit risk labels plus decimal-unit normalization for worst active position ROE across compute, persistence, API, MCP, and frontend consumers.

## Wiki Areas

Canonical markdown lives under `wiki/`:

- `wiki/company/` — canonical company operating context.
- `wiki/agents/templates/` — the optional managed-worker brief and coding-execution reference.
- `wiki/ops/` — operating runbooks, process notes, Linear operating system.
- `wiki/engineering/` — stable engineering architecture, contracts, inventories, implementation context, and invariants; not ticket or implementation plans.
- `wiki/quant/` — quantitative research notes.
- `wiki/research/trading/` — strategy research protocol and per-project research docs (`research_process_v1`, example research directory).
- `wiki/trading/` — trading language and discretionary/strategy context.
  - `wiki/trading/entry/` — reusable discretionary entry and sizing primitives.
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
