# MON-97 Backtest Metrics Plan

Date: 2026-06-29

## Goal

Fix backtest trade-level metrics so fee-only/no-trade bookkeeping rows do not count as wins or losses. Keep fee spend and net PnL accounting intact.

## Key Judgment

Do **not** try to separate fee-only rows inside `PnlPointPublic` alone. Current `PnlPointPublic` only carries `realized_pnl` and `realized_pnl_cum`, both fee-inclusive. Once fee-only noise is collapsed into one float per bar, the code cannot reliably tell:

- actual losing trade PnL
- breakeven trade plus fee
- pure accounting/fee row
- multiple fills in one candle with mixed outcomes

The separation has to happen while raw fill events are still available in `backend/app/services/backtest/bt_engine.py`.

## Current Relevant Flow

```text
StrategyResult.fills
-> bt_engine._aggregate_backtest_data()
   - sums fill.closed_pnl into PnlPointPublic.realized_pnl
   - sums fill.fee into total_fees
   - sums fill sz*px into total_volume
-> bt_engine._compute_metrics()
-> metrics.compute_perf_metrics()
   - currently treats every non-zero pnl point as one trade
```

Relevant files:

- `backend/app/services/backtest/bt_engine.py`
- `backend/app/services/backtest/metrics.py`
- `backend/tests/backtest/test_backtest_metrics.py`
- Optional later API/DTO surface: `backend/app/data_models/dto/performance.py`

## Definition of Fee-Only / No-Trade Row

For MON-97, use fill-level classification, not candle-level `PnlPointPublic` inference.

A fill should count toward win/loss metrics only when it closes actual exposure with non-fee trade PnL:

```text
is_close_fill = abs(fill.start_position) > EPS
fee = fill.fee
net_closed_pnl = fill.closed_pnl
trade_pnl_gross = net_closed_pnl - fee
counts_for_win_rate = is_close_fill and abs(trade_pnl_gross) > EPS
trade_outcome_for_stats = net_closed_pnl
```

Rationale:

- Opening fills can carry fees but no closed trade outcome; exclude from win/loss denominator.
- Close/reduce/flip fills can include actual trade PnL; include only if gross trade PnL is non-zero.
- Fee spend remains included in equity, `PnlPointPublic`, `total_fees`, and net trade outcome for included trades.
- This avoids counting “paid a fee but did not book trade PnL” as a loss.

Use a small local EPS, probably `DIV_EPS`, for numeric comparisons.

## Executable Chunks

### Chunk 1 — Add RED unit tests for pure metrics behavior

Objective: Prove the current bug without touching production code.

Files:

- Modify: `backend/tests/backtest/test_backtest_metrics.py`

Add tests directly around `compute_perf_metrics` because that is where trade stats currently use non-zero PnL points as the denominator.

Test cases:

1. A fee-only negative PnL point should not count as a trade once explicit trade PnLs are supplied.
2. A real win and real loss should produce `n_trades=2`, `win_rate=0.5`, and expected avg/max values.
3. If no explicit trade PnLs are supplied, preserve legacy fallback from `pnl_points` for compatibility.

Expected first run:

```bash
cd backend
PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run pytest --confcutdir=tests/backtest tests/backtest/test_backtest_metrics.py -q
```

Expected: FAIL because `compute_perf_metrics` has no explicit trade-PnL input yet.

Notes:

- Use `--confcutdir=tests/backtest` to avoid repo-level `tests/conftest.py` reading root `.env`.
- Keep this pure unit-level first; no DB, no manager startup, no Hyperliquid client.

### Chunk 2 — Add explicit trade-PnL input to metrics

Objective: Make `compute_perf_metrics` capable of using already-classified trade outcomes.

Files:

- Modify: `backend/app/services/backtest/metrics.py`

Implementation shape:

```python
def compute_perf_metrics(
    equity: pd.Series,
    *,
    tf_sec: int | None = None,
    pnl_points: list[PnlPointPublic] | None = None,
    trade_pnls: list[float] | None = None,
    position_snapshots: list[BarPositionSnapshot] | None = None,
    total_fees: float = 0.0,
    total_volume: float = 0.0,
    total_slippage: float = 0.0,
) -> PerformanceMetrics:
```

Behavior:

- If `trade_pnls is not None`, derive `n_trades`, `win_rate`, `avg_win`, `avg_loss`, `expectancy`, `profit_factor`, etc. from finite non-zero `trade_pnls`.
- If `trade_pnls is None`, keep existing fallback from non-zero `pnl_points` to avoid breaking other callers immediately.
- Do not change equity returns, Sharpe, drawdown, fee totals, or position metrics in this chunk.

Verification:

```bash
cd backend
PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run pytest --confcutdir=tests/backtest tests/backtest/test_backtest_metrics.py -q
```

Expected: pure metrics tests pass.

### Chunk 3 — Classify trade outcomes in the engine before data is collapsed

Objective: Build the explicit trade-PnL list from raw fills while `fee`, `start_position`, and `closed_pnl` are still visible.

Files:

- Modify: `backend/app/services/backtest/bt_engine.py`

Add a small helper near `_aggregate_backtest_data`:

```python
def _fill_trade_outcome(fill: dict[str, Any]) -> float | None:
    start_position = finite_float(fill.get("start_position", 0.0), default=0.0)
    fee = finite_float(fill.get("fee", 0.0), default=0.0)
    net_closed_pnl = finite_float(fill.get("closed_pnl", 0.0), default=0.0)
    gross_trade_pnl = net_closed_pnl - fee
    if abs(start_position) <= DIV_EPS:
        return None
    if abs(gross_trade_pnl) <= DIV_EPS:
        return None
    return net_closed_pnl
```

Then in `_aggregate_backtest_data`:

- initialize `trade_pnls: list[float] = []`
- for every fill, append helper result when not `None`
- return `trade_pnls` in the aggregate dict
- pass `trade_pnls=aggregated["trade_pnls"]` into `compute_perf_metrics`

Important:

- Keep `realized_inc += fill["closed_pnl"]` unchanged. PnL series and equity must remain fee-inclusive.
- Keep `total_fees` and `total_volume` unchanged.
- This ticket should not alter order generation, fill generation, sizing, or equity accounting.

### Chunk 4 — Add engine-level regression around fill classification

Objective: Prove MON-97 at the integration seam, not just inside metrics.

Files:

- Modify: `backend/tests/backtest/test_backtest_metrics.py`

Preferred minimal route:

- Test the helper or `_aggregate_backtest_data` with hand-built `StrategyResult` objects rather than running a full strategy.
- Include three bars:
  1. opening fill with negative fee-only closed PnL: excluded
  2. close/reduce fill with real positive gross PnL: included win
  3. close/reduce fill with gross zero but fee negative: excluded fee-only row

Assertions:

- `pnl_points` still include fee-inclusive realized PnL and cumulative PnL.
- `total_fees` still includes all fees.
- `trade_pnls` contains only the real trade outcome.
- Final metrics from `_compute_metrics` use `n_trades=1`, `win_rate=1.0`.

If importing private helpers is too brittle, use `run_strategy_backtest` with a tiny test-only `BacktestStrategy` class in the test file that emits known fills/accounts. Do not hit DB or manager startup.

Verification:

```bash
cd backend
PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run pytest --confcutdir=tests/backtest tests/backtest/test_backtest_metrics.py -q
```

Expected: all backtest metric tests pass.

### Chunk 5 — Fix/guard the temporary vectorbt evaluation caller if reached

Objective: Ensure the signature change does not break the optional `bt_eval_tmp.py` path.

Files:

- Inspect/possibly modify: `backend/app/services/backtest/bt_eval_tmp.py`

Current suspicious call observed:

```python
compute_perf_metrics(equity_bt_s, ret_bt_s, tf_sec=tf_sec, pnl_points=None)
```

Current `compute_perf_metrics` is keyword-only after `equity`, so this positional `ret_bt_s` looks stale. If this path is active under `settings.BT_EVAL_TMP_ENABLED`, fix the call to:

```python
compute_perf_metrics(equity_bt_s, tf_sec=tf_sec, pnl_points=None)
```

Do not broaden this ticket into vectorbt correctness unless tests show the path is currently broken.

### Chunk 6 — API/UI label clarity, minimal version

Objective: Satisfy “denominator clear” without a broad frontend redesign.

Files:

- Modify only if necessary: `backend/app/data_models/dto/performance.py`
- Modify only if necessary: `frontend/src/routes/_layout/backtest.backtest.tsx`

Minimal acceptable move:

- Rename visible label from `Win Rate` to `Trade Win Rate` or add tooltip/copy indicating “closed trade PnL denominator; fee-only/no-trade rows excluded.”

Avoid in this first ticket unless backend tests are already green. Frontend generated client updates may be needed if DTO changes are introduced, so prefer label-only if possible.

### Chunk 7 — Verification pass

Run targeted tests first:

```bash
cd backend
PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run pytest --confcutdir=tests/backtest tests/backtest/test_backtest_metrics.py -q
```

Then run the narrow related backend tests if fast/available:

```bash
cd backend
PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run pytest --confcutdir=tests/backtest tests/backtest -q
```

Do not run backend server, Docker Compose, live runtime, account APIs, strategy start/stop APIs, or deployment paths for this ticket.

## Acceptance Mapping

- Fee-only rows excluded from wins/losses: chunks 1–4.
- Win rate based on closed trades / booked trade PnL: chunks 2–4.
- Gross/net/fees distinction: chunk 3 keeps fee-inclusive net PnL and fee totals separate; consider DTO expansion only if needed.
- Regression fixture: chunks 1 and 4.
- UI/API label clarity: chunk 6.

## Stop Conditions

Stop and reassess if:

- A “fee-only row” cannot be represented with existing raw fill fields in tests.
- `closed_pnl` semantics differ between backtest fills and Hyperliquid/live fills.
- Existing persisted saved-run hydration needs trade stats recomputed from DB rows but only has `BtPnlPoint` available.
- A DTO/database migration becomes necessary; that likely deserves a follow-up or explicit scope confirmation.
