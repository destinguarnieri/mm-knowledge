# Current Checkpoint

Date: 2026-03-20

## Current state

research_mcp v1 is shipped and stress-tested. Runbook is updated and accurate.
Backend has a new `/authorize` pre-flight endpoint.

Completed since last checkpoint:
- MON-78 through MON-83 — all Done (MCP server, tools, guardrails, docs)
- MON-72, 79, 80 — Done
- Stress test of research_mcp by cold agent simulation — loop works end to end
- Runbook updated: stdio model explained, correct health-check route, /authorize prereq, type corrections, interval type mismatch documented
- MON-84 — POST /api/v1/authorize endpoint added to backend (Done)
- MON-85 — type annotations for research_mcp tools (open, Ready)

## Current truth

research_mcp v1 is a working loop:
  GET /api/v1/utils/health-check/ (no auth)
  POST /api/v1/authorize (confirms token valid)
  system_status → list_assets → get_strategy_registry → get_strategy_params_and_config → run_backtest → get_saved_run

Runbook is in research_mcp/doc/runbook.md and is accurate as of 2026-03-20.

Known open items:
- MON-85: MCP tool layer has zero type annotations; interval is list[str] in saved run responses but str in run_backtest input — document and fix
- Docker: backend runs with --reload inside container; docker cp triggers watchfiles loop on macOS Docker Desktop. Workaround: docker compose build + up to deploy backend changes cleanly.

## Next items to pick up

1. MON-85 — Add type annotations to research_mcp tools
   - Audit all tool return shapes vs actual backend responses
   - Add TypedDicts or type annotations to tools/
   - Update runbook field types where needed

2. GitHub <> Linear sync (operational polish)
   - Connected in Linear UI
   - Working pattern: use Linear's suggested branch name, include MON-XX in PR title
   - Need to validate on next real PR

3. Operating cadence (still open)
   - daily control pass
   - twice-weekly backlog grooming
   - weekly planning/review
   - monthly strategy sync

## Recommended restart prompt

When resuming, start from:
- MON-85 (type annotations + interval type fix)
- Then GitHub/PR sync validation on next real PR
- Then operating cadence formalization
