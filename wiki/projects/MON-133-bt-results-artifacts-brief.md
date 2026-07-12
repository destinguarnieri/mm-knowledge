# Brief: MON-135 BT trial results and attempt artifacts

Parent: `MON-133`. Depends on accepted/merged `MON-134`.

Proposed child title: **Add BT trial results and attempt-owned artifact persistence**

## Objective
- Add the V2 output-plane schema and one atomic, insert-only writer for a single Trial Attempt. Do not schedule attempts, transition lifecycle state, or change public readers.

## Dependency State
- Hard dependency: accepted MON-134 models/migration for `BtStudy`, `BtVariant`, `BtTrial`, and `BtTrialAttempt`.
- The worker must use the accepted MON-134 Alembic head as `down_revision`; the brief intentionally does not guess that revision while MON-134 is in flight.
- Legacy execution and persistence remain authoritative throughout this slice.

## Exact Scope
- Add:
  - `BtTrialResult` / `bt_trial_result`
  - `BtAttemptOrderEvent` / `bt_attempt_order_event`
  - `BtAttemptFill` / `bt_attempt_fill`
  - `BtAttemptPositionEvent` / `bt_attempt_position_event`
  - `BtAttemptIndicatorValue` / `bt_attempt_indicator_value`
  - `BtAttemptSignalValue` / `bt_attempt_signal_value`
  - `BtAttemptPnlPoint` / `bt_attempt_pnl_point`
- Add one additive Alembic migration.
- Add `BtAttemptOutputWriteInput` and `persist_bt_attempt_output()`.
- Add PostgreSQL-backed atomicity, identity, retention, constraint, and cascade tests.
- Do not wire the helper into runtime code.

## Deliverable Boundary
- Editable:
  - `backend/app/models.py`
  - one new Alembic revision
  - `backend/app/services/backtest/persistence_types.py`
  - new `backend/app/services/backtest/attempt_output_persistence.py`
  - new `backend/tests/backtest/test_bt_attempt_output_persistence.py`
- Read-only:
  - `backtest_manager.py`
  - `backtest_persistence_service.py`
  - `async_backtest_backend.py`
  - routes, CRUD, public DTOs, helpers, research, MCP, and frontend

## Exact Result Contract
- `attempt_id UUID PK FK bt_trial_attempt.id ON DELETE CASCADE`.
- `metrics_schema_version SMALLINT NOT NULL DEFAULT 1 CHECK >= 1`.
- Counts:
  - `n_bars INT NOT NULL CHECK >= 0`
  - `n_trades INT NOT NULL CHECK >= 0`
- Nullable `DOUBLE PRECISION` metric columns:
  - `total_return`, `cagr`, `vol_annual`, `sharpe`, `max_drawdown`, `bars_per_year`
  - `win_rate`, `profit_factor`, `avg_win`, `avg_loss`, `max_win`, `max_loss`, `expectancy`, `avg_hold_bars`
  - `sharpe_hac`, `sharpe_5x`, `sharpe_5x_hac`, `sharpe_15x`, `sharpe_15x_hac`, `sharpe_60x`, `sharpe_60x_hac`
  - `pct_time_active`, `pct_time_in_money`, `avg_position_size`, `max_position_dd`
  - `total_fees`, `total_volume`, `fees_pct_volume`, `total_slippage`
  - `avg_notional_exposure`, `max_notional_exposure`, `avg_equity`, `net_pnl`, `net_return`
  - `gross_pnl_before_fees`, `gross_return_before_fees`, `turnover_avg_equity`
  - `fee_drag_initial_capital`, `cost_drag_initial_capital`, `cost_drag_gross_pnl`
- Every nullable metric has a named check permitting null but rejecting PostgreSQL `NaN`, `Infinity`, and `-Infinity`.
- The writer converts non-finite `PerformanceMetrics` floats to SQL null; it never persists special float values.
- `candle_load_json JSONB NULL`, with a named check requiring an object when non-null.
- `created_at TIMESTAMPTZ NOT NULL`.
- Identity: exactly one result per Attempt; no upsert.

## Exact Artifact Contract
- All artifacts:
  - use application-generated UUID primary keys;
  - have `attempt_id UUID NOT NULL FK bt_trial_attempt.id ON DELETE CASCADE`;
  - do not contain ownership `run_id` or `asset_id`;
  - preserve current event payload columns except where explicitly changed below;
  - use `TIMESTAMPTZ` for `created_at` and `BIGINT` for market timestamps.
- `BtAttemptOrderEvent`:
  - preserve `order_id`, `oid`, account, symbol, side, status, `status_ts_ms`, nullable price/size/original size, cloid, decision ID, and raw JSON.
  - index `(attempt_id, status_ts_ms)`.
  - nullable floating price/size fields reject non-finite values.
  - no additional uniqueness; repeated order-state events remain distinct.
- `BtAttemptFill`:
  - preserve account, symbol, `tid`, `oid`, cloid, decision ID, price, size, timestamp, side, crossed, start position, closed PnL, fee, fee token, builder fee, hash, twap ID, and liquidation JSON.
  - all NUMERIC fields are `NUMERIC(38,18)` and explicitly reject `NaN` and ±Infinity.
  - unique `(attempt_id, account_address, tid)`.
  - index `(attempt_id, ts_ms)`.
- `BtAttemptPositionEvent`:
  - preserve pid, account, symbol, event type, timestamp, size, entry price, position value, unrealized PnL, ROE, margin used, leverage type/value, and liquidation price.
  - all NUMERIC fields explicitly reject special values.
  - index `(attempt_id, ts_ms)`; no additional uniqueness.
- `BtAttemptIndicatorValue`:
  - preserve timeframe, timestamp, indicator name/component, value, params, params hash, set, and version.
  - `value` rejects non-finite floats; `params` must be a JSON object.
  - index `(attempt_id, t_ms)`; no additional uniqueness.
- `BtAttemptSignalValue`:
  - preserve active-strategy ID, decision ID, timeframe, timestamp, signal name/variant, score, params, params hash, signal/indicator sets and versions.
  - `score` rejects non-finite floats; `params` must be a JSON object.
  - index `(attempt_id, t_ms)`; no additional uniqueness.
- `BtAttemptPnlPoint`:
  - preserve nullable symbol, timestamp, realized PnL, and cumulative realized PnL.
  - PnL fields reject non-finite floats.
  - index `(attempt_id, ts_ms)`; no additional uniqueness.
- Artifact payload JSON fields that represent objects must have named object-shape checks when non-null.

## Writer Type Contract
```python
@dataclass(slots=True, frozen=True)
class BtAttemptOutputWriteInput:
    attempt_id: UUID
    retention_mode: Literal["metrics", "full"]
    symbol: str
    metrics: PerformanceMetrics
    metrics_schema_version: int = 1
    candle_load: CandleLoadReport | None = None
    artifacts: BacktestPersistArtifacts | None = None

async def persist_bt_attempt_output(
    session: AsyncSession,
    *,
    input: BtAttemptOutputWriteInput,
) -> None:
    ...
```
- Use existing strongly typed `PerformanceMetrics`, `CandleLoadReport`, and `BacktestPersistArtifacts`; do not introduce `Any`.
- The helper uses the caller-provided session, never commits, never upserts, and never mutates Study/Trial/Attempt status.
- `metrics` retention inserts only `BtTrialResult`, ignoring supplied artifacts.
- `full` retention inserts the result and every supplied artifact family; empty families are legal.
- Port legacy row coercion/mapping into the new module without editing or calling `AsyncBacktestBackend`.
- Any mapping/constraint/insert failure raises and leaves rollback to the caller.

## Semantic Invariants
- Result identity is `attempt_id`.
- Fill identity is Attempt × account × trade ID.
- All other artifacts preserve individual event rows; no content dedupe.
- Retry output is distinct because a retry has a new Attempt ID.
- Result and retained artifacts are one transaction; partial committed output is forbidden.
- `BtStudy.retention_mode` is the only V2 artifact gate.

## Acceptance Checks
- Upgrade creates exactly seven additive tables; downgrade removes only those tables.
- SQLModel and Alembic agree on names, types, nullability, checks, indexes, and cascades.
- Duplicate result and fill identities fail without silent merge.
- Same fill trade identity on different Attempts succeeds.
- Metrics retention writes no artifacts even when provided.
- Full retention with empty artifact lists succeeds.
- A forced mid-artifact failure rolls back result and every artifact row.
- Bogus Attempt FK fails without orphans.
- Study deletion cascades through Attempt to all output rows.
- PostgreSQL negative tests reject non-finite metrics/artifact numerics and invalid JSON shapes.
- No runtime file imports or invokes `persist_bt_attempt_output`.

## Anti-Goal
- No scheduling, lifecycle transition, public read projection, aggregate persistence, research migration, legacy dual-write, or deletion.

## Stop Condition
- Stop if MON-134 is not accepted/merged, its actual migration head differs from the ticket dependency, atomic writes require a separate session/commit, or implementation requires touching a read-only runtime/API surface.
