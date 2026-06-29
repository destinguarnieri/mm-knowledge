# Research MCP Runbook

Last updated: 2026-03-19
Written for: agents and future Hermes sessions operating the research backtest loop.

---

## What this is

The research MCP is a thin policy facade over the mm_v04 backend.
It exposes a narrow set of research-safe tools so an agent can run the backtest loop
autonomously without touching live trading infrastructure.

It does NOT expose:
- live trading controls
- batch backtest execution
- websocket or streaming surfaces
- strategy start/stop or system lifecycle controls

All tools go through HTTP to the backend. No backend imports in the MCP codebase.

---

## Prerequisites before calling any tool

**The backtest manager must be running.**

Call `system_status` first, every time. If `backtest_manager_running` is False,
`run_backtest` will return a confusing 404. Do not proceed until it is True.

The backend itself must be up at `http://localhost:8000` (or wherever
`RESEARCH_MCP_BACKEND_BASE_URL` is pointed). Auth is handled automatically
via env — do not worry about tokens.

---

## The canonical call sequence

This is the complete loop an agent should follow:

```
1. system_status()
   -> confirm backtest_manager_running == True before continuing

2. list_assets(limit=50)
   -> returns [{id, name}, ...]
   -> pick the asset you want, note its id (UUID)

3. get_strategy_registry()
   -> returns strategy_names (list of strings) and strategies (list of {name, id})
   -> use strategies[n].id as strategy_id in run_backtest
   -> use strategies[n].name as strategy_name

4. get_strategy_params_and_config(name)
   -> returns {params, config, trade_config} with defaults for that strategy
   -> use these as the starting point, mutate params for your experiment

5. run_backtest(...)
   -> required fields: asset_id, interval, min_candles, strategy_id, strategy_name,
      params, initial_capital, fees, slippage
   -> defaults: detail_mode="compact", auto_save=True
   -> returns: run_id, success, performance_metrics, message, symbol, interval

6. evaluate performance_metrics inline (from run_backtest response)
   -> key fields: sharpe, total_return, cagr, max_drawdown, n_trades, vol_annual

7. get_saved_run(run_id) — optional, for full metadata
   -> call this if you need the full saved record
   -> get_saved_run retries automatically on 404 (async persistence lag is normal,
      the run may not be flushed to DB immediately after run_backtest returns)
   -> check can_hydrate_artifacts — if True, full event data (orders, fills, etc.)
      is in the DB even though it was stripped from the run_backtest response

8. list_saved_runs(limit, offset) — optional
   -> use to inspect prior runs in the session or across sessions
```

---

## detail_mode explained

The MCP defaults to `detail_mode="compact"`. This is intentional.

| detail_mode | What comes back in run_backtest response | DB persistence |
|-------------|------------------------------------------|----------------|
| compact     | performance_metrics only. candles, orders, fills, positions, indicators, signals, pnl_points are ALL stripped (empty arrays). | Full artifact data IS persisted. can_hydrate_artifacts=True. |
| full        | Everything inline. Heavy response. | Full artifact data persisted. |
| lite        | performance_metrics only. | Summary only. can_hydrate_artifacts=False. |

**Use compact for the research loop.** It is fast and gives you the metrics you need
for scoring. If you need to inspect individual orders, signals, or candles for a
specific run, call get_saved_run — the full data is in the DB.

Do not be confused by empty candles/orders/fills in the run_backtest response when
using compact. That is expected behavior, not an error. The agent does not need raw
event data to score a run.

---

## run_backtest field reference

```python
{
    "asset_id": "<UUID from list_assets>",
    "interval": "1h",           # e.g. "1m", "5m", "15m", "1h", "4h", "1d"
    "min_candles": 500,         # bars to fetch. 500 = ~20 days on 1h
    "strategy_id": "<UUID from get_strategy_registry strategies[n].id>",
    "strategy_name": "emac",    # must match registry name exactly
    "params": {},               # get defaults from get_strategy_params_and_config
    "config": {},               # optional, defaults to {}
    "trade_config": {},         # optional, defaults to {}
    "initial_capital": 10000.0,
    "fees": 0.0005,             # 5 bps
    "slippage": 0.0005,         # 5 bps
    "detail_mode": "compact",   # default — keep this for the loop
    "auto_save": True,          # default — always save
}
```

---

## Interpreting run results

A successful run returns `success=True` and a `performance_metrics` dict.

Key metrics to evaluate:

| field | meaning |
|-------|---------|
| sharpe | annualised sharpe ratio |
| total_return | raw total return over the backtest window |
| cagr | compound annual growth rate |
| max_drawdown | worst peak-to-trough drawdown (negative number) |
| n_trades | total number of trades executed |
| vol_annual | annualised volatility |
| win_rate | fraction of trades that were profitable |
| profit_factor | gross profit / gross loss |

**If n_trades is 0:** the strategy produced no signals over the backtest window.
This is not an error — it means the params/config/interval combo never triggered an
entry. Try a shorter window, different params, or a more liquid asset.

**If success=False:** check the `message` field. Common causes:
- insufficient candles (min_candles too high for available history)
- strategy validation error (bad param values)
- backend error (check system_status, manager may have gone down)

---

## Authentication

The MCP handles auth automatically. The agent user is `hermes-agent@moneymachine.dev`.
Credentials come from env vars — do not hardcode them anywhere.

If you see 401 errors, the token may have expired mid-session. This should not happen
in practice since the auth client re-fetches on demand. If it does, restarting the MCP
process will re-authenticate cleanly.

---

## Known gotchas

1. **strategy_id is a UUID, not a name.** Use `get_strategy_registry()` which now
   returns both `strategy_names` (strings) and `strategies` (list of {name, id}).
   Always use the id from `strategies`, not a hand-crafted UUID.

2. **asset_id is a UUID.** Use `list_assets()`. Never guess or hardcode asset UUIDs.

3. **get_saved_run may 404 immediately after run_backtest.** The persistence flush
   is async. The MCP client retries automatically with backoff (100ms → 250ms →
   500ms → 1s). Do not add your own retry on top.

4. **compact mode strips raw event data.** candles/orders/fills/positions/indicators/
   signals/pnl_points will be empty arrays in the run_backtest response. This is
   correct. See detail_mode section above.

5. **system_status before run_backtest.** If the manager is not running, run_backtest
   returns a confusing 404. Always check first.

6. **strategy_name must match the registry exactly.** Case-sensitive. Use the name
   from get_strategy_registry verbatim.

---

## MCP service location

Codebase: `/Users/destinguarnieri/Desktop/codebase/mm_v04/research_mcp/`
Entry point: `python -m research_mcp`
Config: `.env` at repo root (do not commit credentials)
Tests: `cd research_mcp && .venv/bin/python -m pytest tests/ -v`

The MCP runs as a separate process alongside the backend. It does not import any
backend modules — all communication is over HTTP.

---

## Current tool surface (v1)

| tool | purpose |
|------|---------|
| system_status | check backtest_manager_running before run_backtest |
| list_assets | discover asset UUIDs for run_backtest |
| get_strategy_registry | list strategy names + UUIDs |
| get_strategy_params_and_config | get default params/config for a strategy |
| get_strategy_params_and_config_schema | get JSON schema for a strategy's params |
| run_backtest | execute a single backtest |
| list_saved_runs | browse prior saved runs |
| get_saved_run | fetch full metadata for a specific run |

Explicitly not in v1: batch backtest, signal deciles, live trading, monitoring,
websockets, system lifecycle controls.
