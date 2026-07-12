# Brief: MON-137 BT V2 compatibility projections

Parent: `MON-133`.

Proposed child title: **Project BT V2 through existing API, MCP, and frontend contracts**

## Objective
- Switch current single/batch submission, status, saved-list/detail, and hydration behavior to V2 while preserving existing public FastAPI DTOs/routes and therefore existing Research MCP/frontend clients.

## Dependency State
- Hard dependencies:
  - accepted MON-134 foundation;
  - accepted Trial result/attempt-artifact persistence;
  - accepted durable scheduler/lifecycle.
- Saved research/signal-deciles migration is a later child.
- Legacy data is disposable. This ticket does not implement dual-read or fallback: after switch, public BT execution/read surfaces are V2-only while legacy tables remain inert until deletion.

## Exact Scope
- Route current single/batch manager methods through V2 acceptance, scheduler state, results, and artifacts.
- Add V2 projection/resolution helpers and V2 CRUD queries.
- Keep public route paths, request/response DTOs, status codes, and generated frontend client stable.
- Prove Research MCP saved/batch tools and frontend contracts pass unchanged.
- Do not migrate research routes or delete legacy code/tables.

## Deliverable Boundary
- Editable:
  - `backend/app/services/backtest/backtest_manager.py`
  - new `backend/app/services/backtest/v2_projection.py`
  - `backend/app/helpers/backtest.py`
  - `backend/app/crud.py`
  - route implementation only if delegation requires it; route signatures/status codes are locked
  - focused backend compatibility tests
- Verification-only unless a true contract mismatch is found:
  - `research_mcp/`
  - frontend
  - generated OpenAPI client
- Read-only:
  - public request/response DTO field shapes
  - research/signal-deciles services
  - legacy model/table deletion

## Public Identity and Shape
- Public `run_id` is exactly `BtStudy.id`; no translation table.
- Current wrappers support exactly one Variant:
  - zero or multiple Variants → 409 `study is not a single/batch wrapper shape`;
  - one Trial → derived `run_type = "single"`;
  - more than one Trial → derived `run_type = "batch"`;
  - zero Trials → invariant error/409.
- `(run_id, asset_id)` resolves Study → sole Variant → unique Trial.
- Metrics/artifacts resolve through the unique succeeded Attempt guaranteed by the partial unique constraint.
- No V2/legacy UUID resolver and no merging of data sources.

## Submission Contract
- `POST /run`:
  - build one Study, one Variant, and one Trial through V2 acceptance;
  - await terminal Trial through durable scheduler;
  - return the existing `BacktestRunResponse` with `run_id = study.id`.
- `POST /run/batch`:
  - build one Study, one Variant, and N Trials;
  - return existing 202 shape with `run_id = study.id`;
  - poll durable database status.
- `auto_save` remains accepted as a deprecated no-op; every accepted run is durable.
- Retention mapping:
  - `detail_mode = lite` → `retention_mode = metrics`;
  - `detail_mode = compact|full` → `retention_mode = full`.

## Status Projection
- Batch poll:
  - Study `queued` → `queued`
  - `running` → `running`
  - `succeeded|partially_succeeded` → `completed`
  - `failed|canceled` → `failed`; canceled uses error `canceled`
- Counts are derived:
  - requested = all Trials;
  - completed = succeeded + failed + canceled;
  - successful = succeeded;
  - failed = failed + canceled.
- Saved-list/detail eligibility:
  - include only `succeeded` and `partially_succeeded` Studies;
  - exclude queued, running, failed, and canceled Studies.
- Existing saved DTO `status` is `"saved"` for eligible V2 Studies.
- Timestamps convert timezone-aware Study timestamps to epoch milliseconds.

## List Projection
- `run_id` ← Study ID.
- `run_type` ← derived wrapper shape.
- Strategy identifiers/names ← immutable Study snapshots.
- `interval` ← singleton list containing Study interval.
- range/min-candles ← Study fields.
- `requested_assets`, `successful_assets`, `failed_assets` ← derived Trial counts.
- `primary_asset_id`/symbol ← sole Trial for single shape; null for batch.
- `detail_mode`:
  - metrics retention → `lite`;
  - full retention → validated original `request_json.detail_mode`, falling back to `compact`.
- `auto_save = true`.
- `can_hydrate_artifacts = true` only when retention is full and at least one succeeded Trial has persisted attempt artifacts.
- Batch-only list filters derived `run_type = batch`.

## Detail and Aggregate Projection
- Single detail:
  - Trial identity/symbol/status;
  - error from latest terminal Attempt when failed;
  - metrics from `BtTrialResult`;
  - candle-load report from result JSON;
  - artifact hydration flag from retention plus persisted artifact availability.
- Batch detail:
  - compact result per succeeded Trial;
  - error per failed/canceled Trial;
  - candle-load summary from Trial results;
  - no stored aggregate row.
- Derive existing `AggregatedPerformanceMetrics` on read using successful Trial metrics and the existing metric field set:
  - mean/median per metric;
  - sum `n_trades` and `n_bars`;
  - requested/success/failed counts from Trials.
- Fixture-equivalence tests must show V2 derivation matches current batch aggregate DTO output for identical metrics.

## Hydration Contract
- Supported routes remain:
  - `/run/saved/{run_id}/asset/{asset_id}`
  - `/run/batch/{run_id}/asset/{asset_id}`
- Resolve sole Variant and Trial by asset, then the unique succeeded Attempt.
- Read attempt-owned order/fill/position/indicator/signal/PnL rows ordered by their attempt/timestamp indexes.
- Reuse existing public artifact builders and candle retrieval semantics.
- Fail closed:
  - multi-Variant Study → 409;
  - missing Trial or no succeeded Attempt → 404;
  - metrics retention → 404;
  - full retention with no persisted artifact rows → 404;
  - incomplete explicit candle window → 404.
- Explicit range remains half-open; legacy null-range behavior is not needed for V2 because Study records the accepted range contract.

## Type Contract
- Public DTO definitions remain unchanged.
- New projection helpers accept V2 model/query bundles and return existing:
  - saved list items;
  - saved single/batch detail responses;
  - batch status response;
  - hydrated `BacktestRunResponse`.
- Do not use unions of legacy and V2 rows in one helper. V2 helpers are separately typed.

## Acceptance Checks
- Single and batch submissions return Study UUIDs in existing `run_id` fields.
- Batch polling survives manager process restart because it reads the database.
- Wrapper shape rejects multi-Variant Studies.
- Saved eligibility/status/count/detail-mode projections match this brief.
- Aggregate fixture matches legacy DTO semantics.
- Hydration resolves Attempt artifacts and preserves candle completeness/same-timestamp chart behavior.
- Metrics-only retention fails hydration closed.
- Existing Research MCP batch/saved client tests pass unchanged.
- Frontend typecheck/build passes without generated-client changes.
- OpenAPI diff contains no public contract change.
- No research service/model changes and no legacy table deletion.

## Anti-Goal
- No grid projection, research/signal-deciles migration, legacy fallback/dual-read, backfill, new DTOs/routes, or deletion.

## Stop Condition
- Stop if scheduler/output dependencies are not accepted, public DTO changes are required, current clients cannot remain unchanged, or multi-Variant Studies would be silently exposed through single/batch wrappers.
