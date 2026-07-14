---
name: MON-144 HL 1d Candle Overflow
overview: Widen live candle tf_sec for daily bars and route Hyperliquid research candle cache through provider-qualified backtest_candle.
todos:
  - id: schema-widen
    content: Alembic + models widen candle.tf_sec and indicatorvalue.tf_sec SmallInteger → Integer
    status: completed
  - id: hl-research-cache
    content: Route HL db-first and db-only candle cache through backtest_candle source=hyperliquid
    status: completed
  - id: verification
    content: Focused tests for 1d upsert and HL write target; regression on shorter TF and Binance
    status: completed
isProject: false
---

# MON-144 HL 1d Candle Overflow + Research Cache Separation

Date: 2026-07-12  
Status: done (local migrate applied)  
Linear: [MON-144](https://linear.app/money-machine/issue/MON-144/fix-hl-1d-candle-smallint-overflow-and-stop-writing-research-candles)

Related: [[sessions/current-checkpoint|Current Checkpoint]], MON-113 `backtest_candle` / `f8a9b0c1d2e3` widen pattern.

## Outcome

1. Daily `tf_sec=86400` persists without PostgreSQL `smallint out of range`.
2. Hyperliquid research/backtest candle cache reads and writes `backtest_candle` with `source=hyperliquid`, not live `candle`.
3. Live runtime continues to own the live `candle` table.

## Why This Work Exists

Observed Hyperliquid 1d backtests fail on `INSERT INTO candle (... tf_sec ...)` because live `Candle.tf_sec` is `SmallInteger` (max 32767) while 1d is 86400. Separately, HL research still caches into live `candle` while Binance research already uses provider-qualified `backtest_candle` (`Integer` `tf_sec`). Widening alone would leave research polluting live candle storage; routing alone would still leave live schema unable to store daily bars if live ingestion ever needs them. Both fixes ship together.

## Locked Semantic Contract

### Schema

- Alter live `candle.tf_sec`: `SmallInteger` → `Integer` (mirror `f8a9b0c1d2e3` on `backtest_candle`).
- Alter `indicatorvalue.tf_sec` in the **same** migration: `SmallInteger` → `Integer`. Same overflow class; cheap and safe; lock it in rather than leaving soft “consider”.
- Update `Candle.tf_sec` and `IndicatorValue.tf_sec` SQLAlchemy columns in `backend/app/models.py` to `Integer`.
- Alembic `down_revision` = current head `e0f1a2b3c4d5`. Do not invent a parallel head.
- No OHLC/scale redesign. No data backfill/migration of historical rows from `candle` → `backtest_candle`.

### Hyperliquid research identity

- Table: `backtest_candle`.
- `source`: `DataProvider.HYPERLIQUID.value` → `"hyperliquid"`.
- `source_symbol`: the HL coin symbol already passed into `_load_candles_db_first_async` as `symbol` (e.g. `"BTC"`).
- Series identity / conflict key remains existing unique constraint: `(source, source_symbol, asset_id, tf_sec, t_ms)`.
- `price_scale`: the same HL scale already used by the loader (`derive_price_scale` / call-site `price_scale`), persisted via `build_backtest_candle_upsert_rows`.
- Retry/failure: keep current HL semantics — gap fetch then `async_upsert_backtest_candles_ignore_conflicts` (ignore duplicates). Do **not** invent Binance-style page conflict HTTP (`provider_candle_conflict`) for HL in this ticket.
- Cache cold-start after cutover is intentional: existing HL research rows in live `candle` are not reused; the next HL backtest re-fetches missing spans into `backtest_candle`.

### Live `candle` contract after this ticket

- Live runtime ingestion/persistence remains on `candle` (`persistence_service` / storage backend / `upsert_candles*`).
- Research/backtest HL path must not call `async_read_candles_window` / `async_upsert_candles_ignore_conflicts`.
- Binance path stays on `backtest_candle` / `source=binance_usdm`; touch only shared helpers if required for HL parity.

## Repo Anchors

Inspect first:

| Path | Why |
| --- | --- |
| `backend/app/models.py` (`Candle`, `IndicatorValue`, `BacktestCandle`) | Column types |
| `backend/app/alembic/versions/f8a9b0c1d2e3_widen_backtest_candle_tf_sec.py` | Migration pattern to mirror |
| `backend/app/alembic/versions/e0f1a2b3c4d5_add_candle_availability_preflight.py` | Current head for `down_revision` |
| `backend/app/services/backtest/backtest_manager.py` (`_load_candles_db_first_async`, `_load_candles_db_only_async`, `_cache_binance_page`, `_load_binance_candles_db_first_async`) | HL vs Binance seams |
| `backend/app/crud.py` (`async_read_*`, `async_upsert_*` candle helpers) | Persistence helpers |
| `backend/app/helpers/backtest.py` (`build_candle_upsert_rows`, `build_backtest_candle_upsert_rows`) | Row builders already exist |
| `backend/app/data_models/dto/enums.py` (`DataProvider`) | Source string lock |
| `backend/tests/backtest/test_backtest_candle_loading.py` | HL loader tests currently monkeypatch live candle CRUD |
| `backend/tests/backtest/test_backtest_explicit_date_range.py` | Same live-candle monkeypatches for HL path |

## Implementation Plan

### 1. Schema widen

1. New Alembic revision after `e0f1a2b3c4d5` that `alter_column`s `candle.tf_sec` and `indicatorvalue.tf_sec` to `sa.Integer()`, with matching downgrade to `SmallInteger`.
2. Change model `sa_column` types from `SmallInteger` to `Integer` for both fields.
3. Do not change `BacktestCandle.tf_sec` (already `Integer`).

### 2. Route HL research cache

In `BacktestManager._load_candles_db_first_async`:

1. Read via `async_read_backtest_candles_window` with `source=DataProvider.HYPERLIQUID.value`, `source_symbol=symbol`, same `asset_id` / `tf_sec` / window.
2. Convert with `backtest_candles_to_candleview(..., price_scale=price_scale)` instead of `candles_to_candleview` on live `Candle` rows.
3. On gap fill, upsert with `build_backtest_candle_upsert_rows(...)` + `async_upsert_backtest_candles_ignore_conflicts` instead of live candle builders/helpers.
4. Keep fetch (`_fetch_gap_candles_async`), completeness validation, and report fields otherwise unchanged.

In `BacktestManager._load_candles_db_only_async`:

1. For non-Binance (HL) paths, read `backtest_candle` with `source=hyperliquid` and `source_symbol` from the persisted run (or equivalent symbol already available at the call site). Do not fall back to live `candle`.
2. If `source_symbol` is missing for an HL persisted run, fail explicitly (same class of error as Binance missing `source_symbol`) rather than silently reading live `candle`.

Imports/cleanup: drop unused live-candle imports from the HL research path once call sites are gone; leave live CRUD helpers intact for runtime.

### 3. Verification (acceptance)

Focused tests (prefer extending existing backtest candle tests):

- **1d upsert / type path:** building or upserting rows with `tf_sec=86400` no longer targets a SmallInteger live candle column; model/migration assert Integer. Prefer a unit/integration assertion that HL loader upsert rows use `backtest_candle` helpers with `tf_sec=86400` and `source="hyperliquid"`.
- **Write target:** monkeypatched HL `_load_candles_db_first_async` asserts calls go to `async_read_backtest_candles_window` / `async_upsert_backtest_candles_ignore_conflicts` (not live candle helpers), with `source="hyperliquid"` and `source_symbol` equal to the HL symbol.
- **Regression:** existing shorter-TF HL loader tests updated for the new monkeypatch targets still pass; Binance tests untouched unless shared helpers force a trivial update.
- **Negative path:** empty/missing cache still fetches gaps; ignore-conflicts duplicate upsert still succeeds (no conflict-raising HL path).
- Run focused pytest for the touched backtest/candle tests; confirm Alembic head resolves to the new revision.

Do not start live trading runtime, deploy, or mutate live accounts as part of this ticket.

## Out of Scope

- Candle OHLC bigint / scaling redesign.
- Migrating historical live `candle` rows into `backtest_candle`.
- Binance loader redesign or HL Binance-parity conflict HTTP.
- Live runtime candle ingestion changes beyond the schema widen.
- Frontend / Research MCP contract changes (none required if providers already pass through).

## Anti-Goal

Do not turn this into a multi-venue candle platform rewrite, shared “universal loader” abstraction, or live/research table merge. Smallest fix: widen + point HL research at the existing `backtest_candle` helpers.

## Stop Condition

Hand back if:

- Alembic head is no longer `e0f1a2b3c4d5` and the correct parent is ambiguous.
- Saved-run HL retrieval cannot obtain a stable `source_symbol` without inventing a new persistence field.
- Implementation appears to require changing live candle writers or Binance conflict semantics to make HL work.
- Scope expands into historical cache migration or indicator persistence redesign beyond the `tf_sec` column widen.

## Acceptance Checklist

- [x] `candle.tf_sec` and `indicatorvalue.tf_sec` are `Integer` in models + migrated DB
- [x] HL 1d backtest candle insert path no longer raises smallint out of range
- [x] HL backtest cache uses `backtest_candle` with `source=hyperliquid`
- [x] Focused tests cover 1d upsert targeting and HL→`backtest_candle` write target
- [x] Live `candle` remains the live-runtime store; Binance path unchanged in behavior

## Implementation Notes (2026-07-12)

- Migration revision: `a2b3c4d5e6f7` (parent `e0f1a2b3c4d5`).
- Verification: 56 focused backtest candle tests passed (`test_backtest_candle_loading`, `test_backtest_explicit_date_range`, `test_binance_backtest_candles`).
- Local DB migrate applied: `a2b3c4d5e6f7`; Postgres `candle.tf_sec` / `indicatorvalue.tf_sec` verified INTEGER. Linear marked Done.
