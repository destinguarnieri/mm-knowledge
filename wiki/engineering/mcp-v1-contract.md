# MCP v1 Contract (Original Baseline)

Status: historical scope baseline. The implemented tool catalog has expanded
since this document was written. The current executable contract and canonical
request examples live in `mm_v04/research_mcp/doc/runbook.md` and
`mm_v04/research_mcp/AGENT.md`; use those instead of old field lists below.

## Purpose

This document is the source of truth for the first implementation of the MM v04 backtest/research MCP server.

Use it to keep `MON-79`, `MON-80`, `MON-81`, `MON-82`, and `MON-83` aligned around one narrow contract.

## One-sentence definition

MCP v1 is a research-only interface for single-strategy autonomous iteration: discover a strategy, inspect its schema/defaults, run one backtest, inspect the saved result, and repeat.

## Permanent boundary

This project is strictly for backtest and research workflows.

It should never include live trading controls in any version.

Anything involving live trading agent interfaces should be treated as a separate project.

## What MCP v1 is not

MCP v1 is not:
- a generic wrapper over the full MM v04 API
- a live-trading control plane
- an operator console
- a websocket bridge
- a batch backtest interface

## V1 product goal

Enable a minimal autonomous research loop with the smallest safe tool surface:
1. discover a backtestable strategy
2. inspect params/config defaults and schemas
3. run a single backtest
4. inspect the saved result and one saved run asset when artifact detail is needed
5. repeat with revised inputs

## Explicitly out of scope for v1

Do not include any of the following in MCP v1:
- batch backtests
- websocket or subscription support
- monitoring/operator read surfaces unless needed later by a separate approved scope
- system lifecycle control
- active strategy lifecycle control
- trading control actions
- account CRUD or account listing
- exchange metadata mutation
- any route that touches live-money paths

Examples of excluded endpoints:
- `POST /api/v1/system/start`
- `POST /api/v1/system/stop`
- `POST /api/v1/system/command`
- `POST /api/v1/active-strategies/{id}/start`
- `POST /api/v1/active-strategies/{id}/stop`
- `POST /api/v1/trading/strategy/{active_strategy_id}/nuke`
- `/api/v1/accounts/*`
- hyperliquid asset mutation endpoints
- all `/api/v1/ws/*` websocket routes
- all `/api/v1/backtest/run/batch*` routes

## Canonical v1 tool catalog

These are the only tools MCP v1 should expose.

### 1. `get_strategy_registry`
Purpose:
- list backtestable strategy names from the in-code registry

Backend route:
- `GET /api/v1/strategies/registry?backtest=true`

Minimal input:
- none

Expected output:
- `strategy_names: string[]`

Notes:
- MCP should hardcode `backtest=true`
- callers should not be allowed to toggle to non-backtest mode

### 2. `get_strategy_params_and_config`
Purpose:
- retrieve default params/config/trade_config for one strategy

Backend route:
- `GET /api/v1/strategies/registry/params_and_config?backtest=true&name=<strategy_name>`

Minimal input:
- `name: string`

Expected output:
- `name: string`
- `params: object`
- `config: object`
- `trade_config: object`

Notes:
- MCP should pass through the backend response but normalize missing objects to `{}`

### 3. `get_strategy_params_and_config_schema`
Purpose:
- retrieve JSON schemas for typed parameter construction and validation

Backend route:
- `GET /api/v1/strategies/registry/params_and_config_schema?backtest=true&name=<strategy_name>`

Minimal input:
- `name: string`

Expected output:
- `name: string`
- `params_schema: object`
- `config_schema: object`
- `trade_config_schema: object`

Notes:
- this is the primary schema-discovery tool for the agent loop

### 4. `run_backtest`
Purpose:
- run one single-asset backtest

Backend route:
- `POST /api/v1/backtest/run`

Backend request model:
- `BacktestRunRequest`
- source: `backend/app/data_models/dto/backtest.py`

Required input fields:
- `asset_id: UUID`
- `interval: Interval`
- `min_candles: int`
- `strategy_id: UUID`
- `strategy_name: string`
- `params: object`
- `initial_capital: float`
- `assets: list` containing exactly one settings entry matching `asset_id`
- `fee_bps: float`
- `slippage_bps: float`

Optional input fields:
- `backtest_strategy_id: UUID | null`
- `backtest_strategy_group_id: UUID | null`
- `backtest_strategy_version: int | null`
- `config: object`
- `trade_config: object`
- `retention_mode: "summary" | "full"`
- `start_ms` and `end_ms` together
- `candle_source`
- `source_symbol`

Expected output:
- `run_id: UUID`
- `success: bool`
- `message: string | null`
- `asset_id: UUID`
- `symbol: string`
- `interval: string`
- `performance_metrics: object`
- optional artifacts depending on `detail_mode`

MCP normalization requirements:
- always return `run_id`
- always surface `success`
- always surface `performance_metrics`
- include `artifact_counts` summary instead of forcing the agent to inspect large arrays first
- preserve raw backend payload under a nested field if needed, but keep the top-level response concise

Recommended MCP-side defaults:
- `retention_mode="summary"`
- if `config` or `trade_config` missing, send `{}`

### 5. `list_saved_runs`
Purpose:
- recover progress and continue the loop from previously saved single runs

Backend route:
- `GET /api/v1/backtest/run/saved`

Minimal input:
- `limit: int = 20`
- `offset: int = 0`

Expected output:
- `data: list[...]`
- `count: int`

Important backend fields from `BacktestSavedRunListItem`:
- `run_id`
- `run_type`
- `status`
- `detail_mode`
- `submitted_at_ms`
- `started_at_ms`
- `finished_at_ms`
- `strategy_id`
- `strategy_name`
- `interval`
- `min_candles`
- `primary_asset_id`
- `primary_symbol`
- `can_hydrate_artifacts`

MCP restriction:
- v1 should only present single-run items to the caller
- if a batch run appears in backend storage, MCP should omit it from v1 results rather than expose it

### 6. `get_saved_run`
Purpose:
- retrieve one saved single run for inspection and loop continuation

Backend route:
- `GET /api/v1/backtest/run/saved/{run_id}`

Expected output for v1:
- only single-run results should be returned to the agent
- if the backend returns a batch run type, MCP should reject it as out of scope for v1

Important backend fields for single-run saved detail:
- `run_type`
- `run_id`
- `asset_id`
- `symbol`
- `success`
- `message`
- `performance_metrics`
- `can_hydrate_artifacts`

MCP normalization requirements:
- preserve the single-run detail shape
- add a concise `result_summary` block extracted from `performance_metrics`
- avoid unnecessary large payload expansion at top level

### 7. `get_saved_run_asset`
Purpose:
- retrieve artifact-bearing detail for one asset in a saved single-run backtest

Backend route:
- `GET /api/v1/backtest/run/saved/{run_id}/asset/{asset_id}`

Minimal input:
- `run_id: UUID`
- `asset_id: UUID`

Expected output:
- `run_id`
- `asset_id`
- `symbol`
- `success`
- `message`
- `interval`
- `performance_metrics`
- `artifact_counts`
- `result_summary`
- `raw`

MCP restriction:
- only use this for saved single-run asset inspection
- do not add batch saved-run tools under this scope

## Recommended MCP-side guardrails

These are stricter than the backend where useful.

### Global rules
- deny by default; only the seven tools above are routable
- if a request can map to a batch or live-trading surface, reject it
- tool handlers should validate input before backend calls
- all tool calls must carry a request ID
- all tool calls must be auditable

### Input limits
Initial recommended limits:
- `list_saved_runs.limit <= 50`
- `run_backtest.min_candles <= 50_000` unless explicitly raised later
- `strategy_name` length must follow backend limits
- reject oversized free-form objects if serialized payload exceeds a modest v1 cap

Current implementation status:
- MCP-layer bounds are enforced for `list_saved_runs.limit` and `run_backtest.min_candles`
- broader compatibility still needs real-backend integration testing before calling hardening complete

### Runtime behavior
- default `run_backtest.retention_mode="summary"`
- timeouts should be bounded and explicit
- retries should be conservative and only for transport or transient upstream failures
- single-run POST timeouts are ambiguous because backend execution may continue;
  they are non-retryable until saved-run state is inspected

## Auth model for v1

Recommended default:
- use one dedicated internal research-only service identity between MCP and backend

Assumptions:
- the MCP server is an internal operator tool, not a public multi-tenant surface
- auth should be narrow and explicit, not a reused superuser shortcut if that can be avoided
- user impersonation is not required for the first version

Implementation boundary note:
- design `research_mcp` as a separate service that talks to the backend over HTTP
- avoid importing backend internals into MCP runtime code
- long-term, avoid backend imports even in MCP startup/build-time code so the service can be split into its own repo cleanly

Open question for implementation:
- whether backend auth should use a dedicated service user or another narrow trusted path

## Error taxonomy

MCP v1 should normalize backend and policy failures into a small fixed set.

Recommended top-level categories:
- `validation_error`
- `authorization_error`
- `out_of_scope`
- `not_found`
- `conflict`
- `upstream_error`
- `timeout`
- `internal_error`

Recommended error shape:
- `error.code: string`
- `error.category: string`
- `error.message: string`
- `error.retryable: bool`
- `error.details?: object`
- `error.request_id: string`

Examples:
- asking for a saved batch run via `get_saved_run` => `out_of_scope`
- unknown strategy name => `not_found` or `validation_error` depending on backend behavior
- backend 409 => `conflict`

## Response-shaping rule

The MCP server should not blindly dump raw backend responses as the primary interface.

For every tool:
- return a concise top-level summary optimized for agent use
- include stable identifiers and the key decision-making metrics first
- keep any large raw payload under a nested field if needed

This matters most for:
- `run_backtest`
- `get_saved_run`

## Minimum audit record per tool call

Every tool call should capture:
- timestamp
- request_id
- tool_name
- caller identity
- normalized input summary
- policy decision
- backend route called
- backend status/result summary
- duration_ms
- success/failure
- error category if failed

## Acceptance criteria for MON-79

MON-79 is done when:
- the permanent project boundary is explicit and unambiguous
- the exact v1 tool catalog is locked
- excluded surfaces are named explicitly
- the auth model assumption is documented
- the MCP error taxonomy is documented
- implementers of MON-80 through MON-83 can work without guessing the v1 scope

## Immediate follow-on mapping

- `MON-80` should implement the shell and auth path described here
- `MON-81` should implement tools 1 through 4
- `MON-82` should implement tools 5 and 6
- `MON-83` should implement the guardrails and audit rules defined here
