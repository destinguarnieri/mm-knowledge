# Current Checkpoint

Date: 2026-03-20

## Current state

research_mcp v1 is shipped. The agentic backtest loop has a working MCP surface.

Completed since last checkpoint:
- MON-78 — MCP server built and operational (Done)
- MON-79 — v1 contract locked (Done)
- MON-80 — MCP skeleton + backend auth path (Done)
- MON-81 — Strategy discovery + single-run backtest tools (Done)
- MON-82 — Saved-run retrieval + evaluation tooling (Done)
- MON-83 — Safety guardrails, audit logging, kill switch (Done)
- MON-72 — v1 contract for agentic backtest loop (Done)
- AGENT.md + doc/runbook.md added to research_mcp
- list_assets, system_status, enriched strategy registry shipped
- get_strategy_registry now returns {name, id} pairs so agents can call run_backtest without raw backend calls
- 30+ passing tests across backend client and MCP tooling

## Current truth

research_mcp v1 is a working loop:
  check system_status → list_assets → get_strategy_registry → run_backtest → get_saved_run

The MCP surface is self-sufficient for an agent to run backtests without touching the backend directly.

Known gaps surfaced from dogfooding:
- Zero artifact count when success=True is ambiguous (no-trades vs error) — not yet resolved
- No mcp-level health check beyond system_status
- Authentication: backend is single-user, signed JWT required; research_mcp uses env config for auth

## Next items to pick up

1. GitHub <> Linear sync (operational polish)
   - GitHub connected in Linear UI — branch names are auto-generated per issue
   - Working pattern: cut branches using Linear's suggested name, include MON-XX in PR title
   - PRs then auto-link to issues; state automation is conservative (manual moves preferred)
   - Need to validate this works on next PR against the repo

2. Stress-test MCP with a fresh agent session
   - Spin up a fresh Claude Code instance with only the runbook
   - Run the full loop: system_status → list_assets → get_strategy_registry → run_backtest → get_saved_run
   - Document any friction or gaps found
   - This is the integration test that validates whether the runbook is actually complete

3. Resolve ambiguous zero-artifact runs
   - Distinguish "no trades generated" from "error/empty result"
   - Either surface a trades_count field or add a no_trades flag to run result

4. Operating cadence (still open)
   - daily control pass
   - twice-weekly backlog grooming
   - weekly planning/review
   - monthly strategy sync

## Recommended restart prompt

When resuming, start from:
- Stress-test MCP with a fresh agent (item 2 above)
- Then GitHub/PR sync validation on next real PR
- Then operating cadence formalization
