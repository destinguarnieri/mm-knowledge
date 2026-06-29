# MCP-Relevant API Inventory

## Why this exists

If this codebase is exposed to future agents through MCP or any agent tool layer, the raw OpenAPI spec is not enough.

Reasons:
- important live data comes over websockets
- some websocket payloads are only represented in OpenAPI via schema-helper GET routes
- some REST endpoints are high-risk and should not be exposed as default tools
- some read surfaces are much better agent entry points than the raw CRUD surface

## Recommended MCP exposure model

### Safe default tools
Expose read-only tools first.

Recommended read-only tools:
- system status
- dashboard summary
- active strategy listing/detail/status
- monitoring reads for fills/orders/positions/decisions/performance/status events
- backtest saved-run reads
- research saved-study reads
- candle slice reads

### Restricted tools
Do not expose by default. Gate behind explicit operator approval.

Restricted tools:
- system start/stop/command
- active strategy start/stop
- trading nuke
- account create/update/delete
- hyperliquid asset sync/create/update/delete
- strategy create/update/delete if linked to real trading operations

## Best MCP resource candidates

These are the most useful read surfaces for agents.

### 1. System status
- Route: `GET /api/v1/system/status`
- Why it matters:
  - tells an agent whether live runtime is even active
  - should gate many follow-up actions
- Suggested MCP resource name:
  - `system.status`

### 2. Dashboard summary
- Route: `GET /api/v1/dashboard/summary`
- Why it matters:
  - denormalized high-level operator snapshot
  - good first page for an agent checking current system state
- Suggested MCP resource name:
  - `dashboard.summary`

### 3. Active strategy inventory
- Routes:
  - `GET /api/v1/active-strategies/`
  - `GET /api/v1/active-strategies/{id}`
  - `GET /api/v1/active-strategies/{id}/status`
- Why it matters:
  - likely the central operational object in live trading
- Suggested MCP resource names:
  - `active_strategies.list`
  - `active_strategies.get`
  - `active_strategies.status`

### 4. Monitoring read model
This is the best operator/agent read surface for understanding what happened.

Routes:
- `GET /api/v1/monitoring/strategy/status-events/recent`
- `GET /api/v1/monitoring/strategy/status-event/{event_id}`
- `GET /api/v1/monitoring/strategy/{active_strategy_id}/performance`
- `GET /api/v1/monitoring/strategy/{active_strategy_id}/status-latest`
- `GET /api/v1/monitoring/strategy/{active_strategy_id}/status-events`
- `GET /api/v1/monitoring/strategy/{active_strategy_id}/equity-curve`
- `GET /api/v1/monitoring/strategy/{active_strategy_id}/positions`
- `GET /api/v1/monitoring/strategy/{active_strategy_id}/position-events`
- `GET /api/v1/monitoring/strategy/{active_strategy_id}/fills`
- `GET /api/v1/monitoring/strategy/{active_strategy_id}/order-events`
- `GET /api/v1/monitoring/strategy/{active_strategy_id}/orders`
- `GET /api/v1/monitoring/strategy/{active_strategy_id}/decisions`
- per-asset equivalents under `/asset/{asset_id}/...`

Suggested MCP resource grouping:
- `monitoring.status_events_recent`
- `monitoring.strategy.performance`
- `monitoring.strategy.status_latest`
- `monitoring.strategy.status_events`
- `monitoring.strategy.equity_curve`
- `monitoring.strategy.positions`
- `monitoring.strategy.position_events`
- `monitoring.strategy.fills`
- `monitoring.strategy.order_events`
- `monitoring.strategy.orders`
- `monitoring.strategy.decisions`
- `monitoring.strategy_asset.*`

### 5. Candle history
- Route: `GET /api/v1/ws/candles/slice`
- Why it matters:
  - useful read surface for charts, diagnostics, and strategy analysis
  - despite `/ws` prefix, this one is REST
- Suggested MCP resource name:
  - `candles.slice`

### 6. Backtest saved runs and research artifacts
Routes:
- `GET /api/v1/backtest/manager/status`
- `GET /api/v1/backtest/run/saved`
- `GET /api/v1/backtest/run/saved/{run_id}`
- `GET /api/v1/backtest/run/saved/{run_id}/asset/{asset_id}`
- `GET /api/v1/backtest/run/batch/saved`
- `GET /api/v1/backtest/run/batch/saved/{run_id}`
- `GET /api/v1/backtest/run/batch/{run_id}`
- `GET /api/v1/backtest/run/batch/{run_id}/asset/{asset_id}`
- `GET /api/v1/backtest/research/saved`
- `GET /api/v1/backtest/research/signal-deciles/saved/{research_id}`

Suggested MCP resource names:
- `backtest.manager_status`
- `backtest.saved_runs`
- `backtest.saved_run`
- `backtest.saved_run_asset`
- `backtest.saved_batches`
- `backtest.saved_batch`
- `research.saved_runs`
- `research.saved_signal_deciles`

## Operator-dangerous MCP tools

These should not be enabled in a default agent environment.

### Runtime control
- `POST /api/v1/system/start`
- `POST /api/v1/system/stop`
- `POST /api/v1/system/command`

### Strategy control
- `POST /api/v1/active-strategies/{id}/start`
- `POST /api/v1/active-strategies/{id}/stop`

### Emergency trading action
- `POST /api/v1/trading/strategy/{active_strategy_id}/nuke`

### Secret-bearing or potentially secret-bearing CRUD
- `/api/v1/accounts/*`
- any route returning account-linked objects until public models are confirmed sanitized

### Exchange metadata mutation
- hyperliquid asset create/update/delete/sync endpoints

## Websocket inventory

These are not normal REST tools. They are streaming resources and likely need MCP subscription support or a polling bridge.

### Candle stream
- `ws /api/v1/ws/candles?asset_id=<uuid>&tf_sec=<seconds>`
- Payload schema helper:
  - `GET /api/v1/ws/candles/schema`

### Indicator stream
- `ws /api/v1/ws/indicators?asset_id=<uuid>&tf_sec=<seconds>`
- Payload schema helper:
  - `GET /api/v1/ws/indicators/schema`

### Signal stream
- `ws /api/v1/ws/signals?active_strategy_id=<uuid>&asset_id=<uuid>&tf_sec=<seconds>`
- Payload schema helper:
  - `GET /api/v1/ws/signals/schema`

### Trade stream
- `ws /api/v1/ws/trades?account=<addr>&kind=orders|fills|positions|account`
- repeatable `account` query parameter is supported
- Payload schema helper:
  - `GET /api/v1/ws/trades/schema`

### Performance stream
- `ws /api/v1/ws/performance?account=<addr>&kind=asset|strategy`
- `ws /api/v1/ws/performance?portfolio_id=<uuid>&kind=portfolio`
- Payload schema helper:
  - `GET /api/v1/ws/performance/schema`

### Decision stream
- `ws /api/v1/ws/decisions?active_strategy_id=<uuid>&asset_id=<uuid>&tf_sec=<seconds>`
- Payload schema helper:
  - `GET /api/v1/ws/decisions/schema`

### Strategy-status stream
- `ws /api/v1/ws/strategy-status?active_strategy_id=<uuid>[&active_strategy_id=<uuid2>]`
- Payload schema helper:
  - `GET /api/v1/ws/strategy-status/schema`

## Recommended MCP design notes

### Read-only first
For an initial MCP server, expose read-only tools/resources only.

Good first set:
- `system.status`
- `dashboard.summary`
- `active_strategies.list`
- `active_strategies.get`
- `active_strategies.status`
- `monitoring.*` reads
- `candles.slice`
- `backtest.saved_*`
- `research.saved_*`

### Treat websockets separately
Options:
1. Subscription-capable MCP resources
2. Server-side websocket bridge that maintains subscriptions and offers latest snapshots
3. Polling wrappers over persisted read models where low latency is not required

### Avoid using accounts as a generic resource until fully reviewed
Public response models were scrubbed to remove `secret_key`, but account routes are still operationally sensitive and not owner-scoped.
Do not expose account list/get as normal MCP resources until account scoping and secret-handling policy are fully reviewed.

### Best initial agent workflows
1. health/status workflow
   - system status -> dashboard summary -> recent strategy status events
2. strategy triage workflow
   - active strategy list -> strategy status -> positions/fills/orders/decisions -> equity curve
3. research workflow
   - list saved backtests -> inspect run -> inspect per-asset detail -> inspect saved research study

## Gaps that block clean MCP exposure

1. No explicit API danger classification in the codebase.
2. Websocket auth model is not clearly documented.
3. Account/public model sanitization appears unsafe.
4. OpenAPI does not represent the websocket transport itself, only helper schemas.
5. No canonical resource map exists for operators or agents.

## Practical rule for future agents

If you are building an MCP layer for this repo:
- start with monitoring and backtest reads
- gate all mutations
- exclude account resources until sanitized
- treat websocket support as a second phase, not phase one
