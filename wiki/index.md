# Start Here

Status: confirmed

Destin approved a fresh start on 2026-10-06. **No active research commitments carry forward by default.**

- [Open Research Home](research/trading/research_index.html) — the human-facing starting point.
- [[research/trading/research_index|Research Home source]] — current focus, once selected.
- [[sessions/current-checkpoint|Current Checkpoint]] — compact agent pickup state.
- [[ops/research-mcp-runbook|Research MCP Reference]] — links to the maintained implementation-side instructions.

## For agents

Start from Destin’s current request. Destin selected the candle inventory execution notebook on 2026-10-31; see [[research/trading/research_index|Research Home]]. Do not derive an agenda from old programs, tickets, hypotheses, review gates, or “next action” sections. Do not make historical reading or reconciliation a prerequisite for new work.

Search QMD and follow relevant source links only when useful to the current task. Older pages remain reference material; their active/ready/in-progress labels do not activate work after the reset. Current implementation facts and safety constraints still need verification when relevant.

## Current engineering draft

- [[projects/backtest-engine-v2-plan|Backtest Engine V2 delivery draft]] — vectorization, multi-timeframe data, limit orders, then cross margin; proposed ticket scopes for review.

## Frontend UI in progress

- [[projects/trading-terminal-ui|Trading terminal UI]] — separate route, perpetuals, dockable panels, frontend-only order previews.

## Implementation references

- [[ops/backend-testing|Backend testing]] — offline defaults, disposable PostgreSQL, explicit public candles, coverage and CI commands.
- [[engineering/bounded-ema-history|Bounded EMA history]] — retention API, backtest capacity alignment, footprint, and migration verification.

## Optional history

[Pre-reset board, checkpoint, and routing map](../archive/research-reset-2026-10-06/README.md). Original research and evidence remain available in the wiki; source dumps remain in `raw/`. There is no requirement to reconcile or resume them.
