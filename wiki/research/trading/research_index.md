# Research Home

Status: in progress

Browser view: [Open Research Home](research_index.html). Markdown is the source; regenerate with `python3 scripts/build_research_board.py`.

## Current focus

**Candle inventory execution prototype — selected 2026-10-31.**

Destin requested a strategy-independent Python notebook: add long inventory on negative candles under a positive signal, mirror for shorts, and distribute on aligned candles only when position return exceeds EPS. He explicitly selected immediate flattening on an opposite signal, including losses, then following the new direction.

Local artifact: `mm_v04/notebooks/candle_inventory_execution.ipynb`. All 12 code cells execute with hand-calculated checks; the saved chart was visually inspected. Full notebook HTML preview was blocked by the browser file-URL policy. Constructed candles only; no historical evidence or Research MCP run IDs.

Prototype defaults, not settled product policy: fixed-unit capped additions, full distribution, net return on entry notional after fees/slippage, neutral-signal hold, and idealized same-close fills. Next: work through sizing, distribution fraction, profit-candle eligibility, and realistic execution timing with Destin. No live/backtest-runtime integration.

Destin approved a fresh start on 2026-10-06. No past research program, experiment, review request, or ticket carries forward as an active commitment.

## Starting work

Start with what Destin wants to explore or build now. There is no research backlog to clear before beginning.

Use past work only when it helps answer the current question. An old hypothesis, process, “next action,” or unfinished task is not a requirement to continue it.

When Destin chooses a focus, record that focus and its immediate next step here and in [[sessions/current-checkpoint|Current Checkpoint]]. Do not repopulate this page from old tickets or notes.

## History, when useful

The previous work is preserved and optional to consult.

- [Previous research board](../../../archive/research-reset-2026-10-06/research_index.html)
- [Previous checkpoint and routing map](../../../archive/research-reset-2026-10-06/README.md)

Research/evidence pages remain available for targeted search. Historical results retain their original limitations; the reset neither validates nor rejects them.
