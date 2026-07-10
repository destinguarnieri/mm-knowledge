# Money Machine Knowledge Index

Purpose: routing map for Money Machine's agent-readable knowledge graph. Agents should start here, then follow Obsidian-style wikilinks and use QMD search when exact routing is unclear.

## Core Pages

- [[company/money-machine-360|Money Machine Operating Context]] — canonical company frame, revenue proof, work lanes, and decision standard.
- [[sessions/current-checkpoint|Current Checkpoint]] — active strategy, proof period, blocker, evidence, and next action.
- [[ops/linear-operating-system|Linear Operating System]] — issue intake, execution state, and WIP rules.
- [[research/trading/research_process_v1|Research Process V1]] — repeatable quant strategy research protocol from idea card through candidate handoff.
- [[research/trading/example_research_directory/example_research_doc|Example Research Doc]] — style reference for structured research files with timestamped write logs.

## Active Engineering

- [[engineering/backtest_persistence_v2_7d0969f3.plan|MON-133 BT Persistence V2]] — parent architecture and ordered implementation slices.
- [[engineering/MON-133-bt-foundation-slice-brief|MON-134 BT Foundation Brief]] — additive Study/Variant/Trial/Attempt foundation.
- [[engineering/MON-133-bt-results-artifacts-brief|MON-135 BT Results and Artifacts Brief]] — typed Trial results and attempt-owned artifacts.
- [[engineering/MON-133-bt-durable-scheduler-brief|MON-136 BT Durable Scheduler Brief]] — database claims, leases, retries, and recovery.
- [[engineering/MON-133-bt-compatibility-brief|MON-137 BT Compatibility Brief]] — existing API/MCP/frontend projections over V2.
- [[engineering/MON-133-bt-research-migration-brief|MON-138 BT Research Migration Brief]] — Study/Trial/Attempt ownership for saved research.
- [[engineering/MON-133-bt-legacy-removal-brief|MON-139 BT Legacy Removal Brief]] — final destructive cleanup.

## Wiki Areas

Canonical markdown lives under `wiki/`:

- `wiki/company/` — canonical company operating context.
- `wiki/agents/templates/` — the optional managed-worker brief and coding-execution reference.
- `wiki/ops/` — operating runbooks, process notes, Linear operating system.
- `wiki/engineering/` — engineering plans, architecture, implementation context.
- `wiki/quant/` — quantitative research notes.
- `wiki/research/trading/` — strategy research protocol and per-project research docs (`research_process_v1`, example research directory).
- `wiki/trading/` — trading language and discretionary/strategy context.
- `wiki/concepts/` — cross-cutting domain concepts and agent procedures.
- `wiki/projects/` — active initiative context and project-level synthesis.
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
- For broad retrieval, use QMD over the wiki, then retrieve the matching markdown pages before answering.

## Open Maintenance

- Add backlinks and related links as pages stabilize.
- Add QMD collection context descriptions after the core wiki skeleton settles.
- Use `scripts/check_wikilinks.py` to verify links after wiki edits.
