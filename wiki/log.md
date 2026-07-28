# Money Machine Knowledge Log

Chronological log of meaningful KB changes. Keep entries concise and link changed pages.

## 2026-07-26

- Added [[trading/positioning/size-distribution|Size Distribution]] under `wiki/trading/positioning/` (elicited signal→position skew concept; curves image co-located). Linked from [[index|wiki index]] and [[trading/catalog|Trading Catalog]] Scaling In/Out.
- Expanded [[trading/positioning/size-distribution|Size Distribution]] with exchange knobs (curve / Lower|Higher / 0–100%), polarity vs size-shape split, inverse signal-axis sketch, underwater linear-inverse example, and prefer-separate-direct/inverse implementation note.
- Corrected continuous rule on [[trading/positioning/size-distribution|Size Distribution]]: scale-in/out from toward/away zero via `d_abs = abs(sig[-1]) - abs(sig[-2])`; mid-cut absolute bands superseded.
- Added caller-owned active signal space on [[trading/positioning/size-distribution|Size Distribution]]: strategy thresholds shrink the skew band (e.g. `[0.1,1] || [-1,-0.1]`).
- Reverted in-place `signal_inner` change on linear `signal_to_position`; threshold-aware mapping will be a separate opt-in helper (existing callers stay on the legacy function).
- Added opt-in `signal_to_position_banded` (caller `band_inner`/`band_outer`, no `signal_scale`); legacy `signal_to_position` unchanged. Documented on [[trading/positioning/size-distribution|Size Distribution]].

## 2026-07-12

- Added [[projects/MON-144-hl-1d-candle-overflow.plan|MON-144 HL 1d Candle Overflow]] and linked it from [[index|wiki index]] Active Projects.

## 2026-07-10

- Consolidated company routing around [[company/money-machine-360|Money Machine Operating Context]], removed the conflicting company overview, repaired the core index links, and reduced the agent template inventory to the managed [[agents/templates/worker-brief-template|Worker Brief]] and [[agents/templates/managed-coding-execution|Coding Execution]] references.

## 2026-07-09

- Added [[vendors/binance-market-data-access|Binance Market Data Access]]: global Binance spot/futures host semantics, US 451 geo block, official `data-api.binance.vision` for public spot candles, MM posture (vision for backtest/research immediacy; JP trading servers; research/perps may need JP egress or VPN). Renamed wiki folder `vendor/` → `vendors/` so QMD indexes it (QMD hard-excludes dirs named `vendor`). Updated [[index|Money Machine Knowledge Index]] vendor routing. Follow-up same day: documented spot klines schema, caps (`limit` max 1000, weight 2), live rateLimits, and futures klines weight-by-limit table.

## 2026-07-08

- Corrected [[index|Money Machine Knowledge Index]] research routing from stale `wiki/quant/research*` paths to [[research/trading/research_process_v1|Research Process V1]] and [[research/trading/example_research_directory/example_research_doc|Example Research Doc]] under `wiki/research/trading/`. Also pointed session continuity routing at `wiki/sessions/` (not `wiki/ops/`). Earlier same-day index entries that pointed at `wiki/quant/research*` are superseded by this routing.

## 2026-07-02

- Added the historical `MON-98` backtest sizing smoking-gun note with the canonical BTC `emac` 30m/1000-candle 10/50/100 Research MCP repro settings, run IDs, UI headline metrics, and next investigation hypothesis. The note is no longer present in the canonical wiki.
- Updated [[index|Money Machine Knowledge Index]] routing for the MON-98 sizing evidence page.

## 2026-06-29

- Moved agent/worker/coding-manager prompt templates under `wiki/agents/templates/`, updated [[index|Money Machine Knowledge Index]], and cleaned copied project skill pointers in `mm_v04/.cursor/skills/` to target the Money Machine KB.

## 2026-06-28

- Redirected session continuity from `mm_v04/docs/work/*` to `wiki/ops/current-checkpoint.md` and `wiki/ops/session-change-log.md` so the repo `docs/` tree can be removed without losing agent continuity.
- Restored the trading language dictionary into `wiki/trading/money-machine-language.md` and updated `mm_v04/AGENTS.md` to point there.
- Moved category docs into canonical `wiki/` subfolders: `wiki/company/` and `wiki/ops/`.
- Removed duplicate top-level category trees and moved historical prompt dumps to `archive/prompts_DUMP/`.
- Added `scripts/check_wikilinks.py` and verified current wiki links resolve.
- Initialized `wiki/` graph spine and clarified operating model: wiki graph is durable context, QMD is retrieval/index over it, Linear is execution truth.
- Added/updated the initial knowledge index and operating-context routing; the 2026-07-10 consolidation supersedes the original phantom page names.
- Follow-up: add QMD collection contexts and continue promoting active docs into linked wiki pages as they are used.
