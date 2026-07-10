# Current Checkpoint

Date: 2026-07-09 22:46 EDT

## Current State

Deleted the accidental `MON-122` Research MCP suite implementation from the working tree.

- Removed new files: `research_mcp/models/suite.py`, `tests/test_batch_client.py`, `tests/test_suite_tools.py`, `tests/test_suite_validation.py`.
- Restored pre-ticket contents for tools/client/allowlist/validation/errors/models/docs/smoke tests.
- Not a git revert of `0f44d698` (still on `origin/master`); deletion is uncommitted working-tree state.
- Verification: research_mcp smoke/bounds/client tests **13 passed**.
- Destin decision: MCP-owned cartesian grid/suite orchestration is the wrong ownership boundary; do not keep or Accept that design. Re-read/re-spec `MON-122` backend-first before re-implementation.

## Prior Current State

Completed a timeboxed N-bar breakout strategy/research-loop dogfood session (`n_bar_breakout`, BTC + 49-asset UI smokes). Created Linear `MON-131` Trades & Fills Inspector (Triage; launch gate required).

## Objective

Re-open `MON-122` as a ticket-quality problem: batch/grid/suite ownership must be redesigned so backend defines durable contracts and MCP stays a thin wrapper. Parallel: BackTest v2 trades/fills inspector (`MON-131`).

## Locked Shared Contracts

- **Research root:** `wiki/research/trading/` (not `wiki/quant/research/`).
- **`project_id`:** equals the research project slug.
- **KB writeback:** lives in Research MCP for V1.
- **Batch ≠ grid:** still distinct concepts — but grid must not be MCP-only cartesian glue over single/batch leaves.
- **Registry:** KB-first run registry; backend saved-run IDs as references.
- **`MON-130`:** Done (explicit date ranges).
- **`MON-122`:** Implementation deleted from working tree; ticket not Done; prior Accept/commit treated as accidental and withdrawn for product purposes.
- **`MON-131`:** backend owns trade/fill grouping + semantic labels; frontend renders; orange = avg position price.

## Sequencing

**V1 critical path (pending MON-122 re-spec)**

1. `MON-130` — explicit backtest date ranges (**Done**)
2. Re-spec `MON-122` ownership (backend grid/suite vs thin MCP) before coding
3. Then resume `MON-128` / `MON-126` / consumers as appropriate after the new contract

**BackTest v2 (parallel UX)**

- `MON-131` — Trades & Fills Inspector (Triage; launch gate before worker)

## Next Action

1. Coding-manager / lead pass: re-read `MON-122` ticket + brief and mark what is wrong (MCP-owned grid) vs keepable (batch≠grid identity, bounds, no fake parent UUID).
2. Decide whether to commit the working-tree deletion (and later push) so master matches intent.
3. Re-spec ticket before any worker launch.
