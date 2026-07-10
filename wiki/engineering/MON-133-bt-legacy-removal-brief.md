# Brief: MON-139 remove legacy BT persistence

Parent: `MON-133`.

Proposed child title: **Remove legacy BT persistence, services, and data**

## Objective
- Perform the one-way cleanup after every V2 writer/reader is accepted: remove legacy BT run/batch/artifact ownership, legacy research ownership, dead persistence services/config, and all fallback code.

## Dependency State
- Hard gates—all must be accepted and merged:
  - MON-134 foundation;
  - Trial result/attempt artifacts;
  - durable scheduler/lifecycle;
  - API/MCP/frontend compatibility projections;
  - saved research migration.
- This is the only final destructive slice.
- MON-132 remains blocked until this slice is accepted.

## Pre-Launch Proof
- Single/batch submission and polling use V2 only.
- Saved list/detail/hydration use V2 only.
- Research signal-deciles uses Study/Trial/successful Attempt only.
- Existing backend, Research MCP, and frontend contract suites pass without legacy readers.
- No production write path imports `BacktestPersistenceService` or `AsyncBacktestBackend`.
- If any proof fails, launch decision is Stop.

## Exact Data Migration
- Migration docstring must state that legacy saved backtests, artifacts, and legacy-owned saved research are intentionally destroyed.
- Delete legacy-owned research children in FK order:
  1. decile buckets whose study belongs to a `BtResearchRun` with `study_id IS NULL`;
  2. legacy-owned signal-deciles study rows;
  3. legacy-owned excluded-asset rows;
  4. `BtResearchRun` rows with `study_id IS NULL`.
- Alter V2 research root:
  - remove exactly-one legacy/V2 owner check;
  - drop FK and column `backtest_run_id`;
  - make `study_id NOT NULL`;
  - retain Study `ON DELETE CASCADE`.
- Drop legacy run-owned artifact tables:
  - `bt_pnl_point`
  - `bt_signal_value`
  - `bt_indicator_value`
  - `bt_position_event`
  - `bt_fill`
  - `bt_order_event`
- Drop legacy run children:
  - `bt_backtest_run_asset`
  - `bt_backtest_batch_aggregate`
- Drop `bt_backtest_run`.
- Do not drop V2 `bt_study`, `bt_variant`, `bt_trial`, `bt_trial_attempt`, `bt_trial_result`, `bt_attempt_*`, V2-owned `bt_research_run`, or signal-deciles child tables.
- Historical Alembic revisions remain in version control.

## Rollback Boundary
- Forward data deletion is irreversible by Alembic.
- Downgrade may recreate empty legacy table shells only; it cannot restore rows.
- Operational rollback requires restoring a pre-migration database backup and the matching application release.
- Application rollback without database restore is unsupported.
- Migration must not run until the pre-launch proof is green.

## Code Removal
- Delete:
  - `backend/app/services/backtest/backtest_persistence_service.py`
  - `backend/app/services/backtest/async_backtest_backend.py`
- Remove legacy models:
  - `BtBacktestRun`
  - `BtBacktestRunAsset`
  - `BtBacktestBatchAggregate`
  - legacy `BtOrderEvent`, `BtFill`, `BtPositionEvent`, `BtIndicatorValue`, `BtSignalValue`, `BtPnlPoint`
- Remove legacy save types `BtSingleRunSaveJob` and `BtBatchRunSaveJob`; retain shared engine artifact types only if used by V2.
- Remove from manager:
  - `_BatchJobState`, `_jobs`, `_job_queue`, `_active_batch_tasks`;
  - legacy persistence-service lifecycle and enqueue helpers;
  - memory status as authority;
  - legacy saved/status/hydration branches.
- Remove legacy CRUD and helper families keyed by `(run_id, asset_id)` or `BtBacktestRun`.
- Remove research `backtest_run_id` branches and types.
- Remove any compatibility fallback that reads legacy rows.

## Configuration Cleanup
- Remove:
  - `BT_BATCH_QUEUE_MAXSIZE`
  - `BT_BATCH_JOB_TTL_SECONDS`
  - `BT_PERSIST_QUEUE_MAXSIZE`
  - `BT_PERSIST_WORKERS`
  - `BT_PERSIST_FLUSH_TIMEOUT_SECONDS`
  - `BT_PERSIST_STOP_TIMEOUT_SECONDS`
- Keep only V2 scheduler/retention settings that still have live consumers.
- Do not rename V2 settings in this cleanup ticket.

## Test and Documentation Cleanup
- Rewrite or remove fixtures importing legacy models/writers.
- Preserve behavior coverage by moving saved-list, range, candle-load, position-chart, hydration, and research assertions onto V2 fixtures.
- Update:
  - `backend/app/services/backtest/BACKTEST.md`
  - `backend/app/services/research/RESEARCH.md`
  - scratch inspection utilities that query legacy tables
- Add a permanent repository guard test rejecting production references to:
  - legacy models/table names;
  - `BacktestPersistenceService` / `AsyncBacktestBackend`;
  - legacy save jobs;
  - `_jobs`, `_job_queue`, or memory job status authority;
  - research `backtest_run_id`;
  - legacy `"writing"` / `"saved"` persistence lifecycle logic.

## Deliverable Boundary
- Editable:
  - migration, models, manager, persistence types, legacy CRUD/helper/research branches, config, affected tests/docs
- Deletable:
  - the two legacy persistence service files
- Read-only:
  - public FastAPI DTO/route shapes
  - frontend/MCP contracts
  - V2 identity/lifecycle semantics
  - MON-132 grid work

## Acceptance Checks
- Migration drops exactly the legacy tables/column listed and preserves every V2 table.
- Legacy-owned research rows are removed without deleting V2-owned research.
- Backend backtest and research suites pass on V2 fixtures.
- Research MCP tests pass.
- Frontend lint/build and OpenAPI compatibility pass.
- Repository guard finds zero production legacy references.
- V2 single/batch execution, restart polling, saved retrieval, hydration, and signal-deciles smoke paths pass.
- No fallback, translation table, backfill, or dual-write remains.

## Anti-Goal
- No new feature behavior, grid work, DTO redesign, optimization, backfill, or partial retention of legacy internals.

## Stop Condition
- Stop if any pre-launch proof is not green, any accepted V2 path still imports legacy code, migration would remove V2-owned research, or rollback backup/release procedure is not available.
