# research_mcp checkpoint

Date: 2026-03-18

## Current status

`research_mcp/` now exists as a separate root-level service inside `mm_v04`.

Implemented locally:
- real FastMCP runtime
- backend HTTP client boundary
- deny-by-default tool surface
- kill switch
- in-memory audit recording
- backend/http error normalization
- MCP-layer input bounds

Current v1 tool surface:
- `get_strategy_registry`
- `get_strategy_params_and_config`
- `get_strategy_params_and_config_schema`
- `run_backtest`
- `list_saved_runs`
- `get_saved_run`
- `get_saved_run_asset`

Current local validation status:
- `research_mcp` focused changed-tool suite is green as of 2026-07-02: 18 passing tests for run-backtest, saved-run, and allowlist surfaces.
- earlier baseline count at checkpoint time: 35 passing tests

## Key implementation decisions already made

- `research_mcp` is research-only and should never expose live trading
- v1 excludes batch operations
- v1 excludes signal deciles
- service is designed around backend-over-HTTP, not backend imports
- long-term preferred boundary is to avoid backend imports even during startup/build-time code

## Current blocker / open design question

Auth path needs a holistic decision before real backend integration testing.

Reason:
- backend routes currently expect `CurrentUser` or `CurrentAsyncUser`
- those dependencies expect a signed JWT path via `backend/app/api/deps`
- backend behavior is still shaped around Destin effectively being the primary user
- saved-run persistence and listing are user-scoped in the backend

Example complication:
- saved backtest run queries filter on `BtBacktestRun.user_id` when `user_id` is present
- this means the MCP service auth choice affects visibility, ownership, and retrieval semantics

## Practical interpretation

Local hardening is no longer the main bottleneck.
The next real step is not more speculative polishing.
The next real step is:
1. decide the backend auth model for `research_mcp`
2. connect `research_mcp` to a real backend instance
3. test the 7 v1 tools against live backend responses
4. fix any contract or auth mismatches

2026-07-02 implementation note:
- `run_backtest` now passes the backend `assets` field through for per-run asset settings such as `max_position_percent`.
- `get_saved_run_asset` now reads persisted artifact-bearing detail for one saved single-run asset.

## Recommended next discussion

Resolve:
- should `research_mcp` authenticate as one dedicated service principal or through another model?
- how should that service principal map into backend user expectations for saved runs and backtests?
- do we want a service user, signed internal JWT, or another narrow auth path?

Until that is decided, further local work should stay light and avoid deep auth assumptions.
