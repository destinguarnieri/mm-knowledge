# Current Checkpoint

Date: 2026-03-17

## Current state

Strategic, Linear, and codebase-context groundwork is in good shape.

Completed foundation:
- Money Machine 360 context captured in `company/money-machine-360.md`
- Linear operating rules captured in `ops/linear-operating-system.md`
- Linear board cleaned up and aligned to current priorities
- Agent docs for `mm_v04` added under `mm_v04/docs/agents/`
- MON-72 (`Define v1 Contract for the Agentic Backtest Loop`) is in progress and its v1 decisions have been solidified

## Current truth

Primary near-term company priority:
- get a primitive agentic backtest/research loop running as fast as possible

Key judgment from Destin:
- strategy deployment is not structurally blocked by infra cleanup
- the real blocker is getting profitable backtests faster
- therefore the agentic research loop is upstream of strategy-in-prod work

## Next three items to pick back up on

1. `MON-78` — Build MCP Server Around Internal Research and Trading APIs
   - treat as the next major implementation-enabler for the agentic research loop
   - scope to research-safe APIs first
   - do not expose live-money controls in v1

2. GitHub <> Linear sync
   - connect GitHub PRs/branches to Linear issues
   - use issue IDs in branch names / PR titles
   - keep state automation conservative at first

3. Schedule work tempo
   - establish and run the operating cadence:
     - daily control pass
     - twice-weekly backlog grooming
     - weekly planning/review
     - monthly strategy sync

## Recommended restart prompt

When resuming, start from:
- `MON-78`
- then GitHub/PR sync with Linear
- then formalize daily / weekly / monthly tempo
