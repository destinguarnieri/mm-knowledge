# Brief: MON-138 migrate saved BT research to V2

Parent: `MON-133`.

Proposed child title: **Migrate BT research ownership and signal-deciles reads to V2**

## Objective
- Rebind new saved research and signal-deciles analysis to Study/Trial/successful-Attempt ownership while preserving current public research routes and DTOs.

## Dependency State
- Hard dependency: accepted BT V2 compatibility projection child.
- Attempt-owned signal and PnL artifacts must be available and public BT wrappers must already use `run_id = study_id`.
- Legacy saved research data is disposable and need not be backfilled or exposed after this switch.
- Legacy columns/tables are removed only by the final deletion child.

## Exact Scope
- Add nullable indexed `study_id` FK to `BtResearchRun`.
- Make every new research snapshot/job use `study_id`; stop new writes to `backtest_run_id`.
- Resolve V2 wrapper shape, Trial, successful Attempt, signal rows, and PnL rows for signal-deciles analysis.
- Project `study_id` through existing public `run_id` fields.
- Keep signal-deciles algorithms and public request/response DTOs unchanged.

## Deliverable Boundary
- Editable:
  - `backend/app/models.py`
  - one additive Alembic revision
  - `backend/app/crud.py`
  - `backend/app/services/research/backtest_signal_deciles_service.py`
  - `research_manager.py`
  - `async_research_backend.py`
  - research `persistence_types.py`
  - new `backend/app/services/research/v2_artifact_resolver.py`
  - focused research migration tests
- Read-only:
  - public research DTOs and route signatures
  - signal-deciles math/aggregation helpers
  - frontend and Research MCP public contracts
  - legacy deletion

## Schema Contract
- Add `study_id UUID NULL FK bt_study.id ON DELETE CASCADE` and index it.
- Make existing `backtest_run_id` nullable for old rows.
- Add named exactly-one-owner check:
  - `(study_id IS NOT NULL AND backtest_run_id IS NULL) OR (study_id IS NULL AND backtest_run_id IS NOT NULL)`.
- New application writes require `study_id` and null `backtest_run_id`.
- Existing signal-deciles child tables remain keyed by `research_id`; no duplicate Study/Trial ownership is added to children.
- No backfill.

## Public Identity Contract
- `SignalDecilesRequest.run_id` is a Study UUID for new analysis.
- `SignalDecilesResponse.run_id` and `ResearchSavedListItem.run_id` project `BtResearchRun.study_id`.
- Existing `research_id` remains the immutable identity of the analysis snapshot.
- `run_type` is derived from one-Variant wrapper shape:
  - one Trial → single;
  - more than one Trial → batch;
  - zero/multiple Variants → input error.
- Request `run_type` mismatch preserves current typed input-error behavior.

## Artifact Resolution
- New typed resolver:
```python
async def resolve_bt_research_attempts(
    session: AsyncSession,
    *,
    study_id: UUID,
    run_type: Literal["single", "batch"],
    scope: Literal["single_asset", "batch_asset", "batch_aggregate"],
    asset_id: UUID | None,
) -> list[BtResearchAttemptScope]:
    ...
```
- `BtResearchAttemptScope` contains Study, Trial, succeeded Attempt ID, asset/symbol, and typed signal/PnL rows.
- Resolution:
  - `single_asset`: sole Trial and its succeeded Attempt.
  - `batch_asset`: unique Trial for required asset ID.
  - `batch_aggregate`: every succeeded Trial and its succeeded Attempt; failed/canceled Trials become exclusions.
- Query:
  - `BtAttemptSignalValue` by Attempt ordered by `t_ms`;
  - `BtAttemptPnlPoint` by Attempt ordered by `ts_ms`.
- Eligibility:
  - Study is succeeded or partially succeeded;
  - Study retention is full;
  - requested Trial succeeded;
  - signal and PnL artifact sets required by the current join semantics exist.
- Metrics-only retention fails with the current artifact-unavailable input error.

## Analysis Semantics
- Preserve current signal-name selection, timestamp matching, horizons, decile computation, and aggregate math.
- Batch aggregate remains per-asset analysis followed by current aggregation.
- Preserve exclusion reasons for failed Trials, unavailable artifacts, missing signal, and zero matched bars.
- Available signal names are the union across successfully loaded Trial artifacts.
- Do not infer or aggregate across multiple Variants; wrapper gate rejects them.

## Persistence Contract
- Root snapshot creation writes `study_id`, derived run type, scope, asset ID, request JSON, and current research status.
- Research lifecycle remains `queued → writing → saved|failed`; it is independent of Study execution status after eligibility validation.
- Save-job types use `study_id`; no new job may carry `backtest_run_id`.
- Child insertion and failure handling remain atomic under the existing research persistence transaction.
- Saved research list/detail queries return only V2-owned rows after this switch; old legacy-owned rows remain inert until deletion.

## Acceptance Checks
- Exactly-one-owner database check rejects both-owner and no-owner rows.
- New research writes `study_id` and null legacy owner.
- Single, batch-asset, and batch-aggregate analyses read Attempt-owned signal/PnL artifacts.
- Failed Trials are excluded from batch aggregate without hiding successful siblings.
- Metrics-only Study is rejected.
- Run-type and scope/asset mismatches preserve current typed errors.
- Saved list/detail project Study UUID as `run_id`.
- Current signal-deciles algorithm fixtures produce unchanged results for equivalent artifacts.
- Public OpenAPI shape and frontend/MCP contracts do not change.
- No legacy backtest/research table or column deletion.

## Anti-Goal
- No algorithm changes, grid/multi-Variant research, public API expansion, backfill, dual-read of old research rows, or legacy deletion.

## Stop Condition
- Stop if compatibility child is not accepted, successful Attempt signal/PnL artifacts cannot reproduce current timestamp joins, a public DTO change is required, or implementation would need to infer a Variant.
