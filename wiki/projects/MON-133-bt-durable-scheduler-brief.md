# Brief: MON-136 durable BT attempt scheduling

Parent: `MON-133`.

Proposed child title: **Add durable BT attempt scheduling and recovery**

## Objective
- Add database-backed Study acceptance, Attempt claiming, leases, guarded lifecycle transitions, bounded infrastructure retries, and restart recovery using the accepted foundation and output writer. Keep public route/DTO projections and research unchanged.

## Dependency State
- Hard dependencies:
  - accepted/merged MON-134 foundation;
  - accepted/merged BT Trial results and attempt-artifact child.
- This ticket blocks compatibility projection, research migration, legacy deletion, and MON-132.
- Legacy route execution remains available until the compatibility child switches submissions to V2.

## Exact Scope
- Add:
  - `bt_acceptance.py`: validate/expand and atomically create Study, Variants, Trials, and Attempt 1.
  - `bt_control_plane.py`: transactional admission, claim, heartbeat, recovery, and rollup queries.
  - `bt_lifecycle.py`: legal transitions and terminal immutability.
  - `bt_failure_mapping.py`: execution-stage-aware failure classification.
  - `bt_attempt_executor.py`: execute one claimed Attempt and atomically commit output/lifecycle.
  - `bt_attempt_scheduler.py`: worker, heartbeat, and recovery loops.
- Extend manager start/stop to own the V2 scheduler lifecycle, but do not switch existing POST/GET route behavior in this ticket.
- Add scheduler settings and focused PostgreSQL concurrency/recovery tests.

## Deliverable Boundary
- Editable:
  - new modules above under `backend/app/services/backtest/`
  - `backend/app/services/backtest/backtest_manager.py` only for scheduler start/stop ownership
  - `backend/app/core/config.py`
  - new focused scheduler/lifecycle tests under `backend/tests/backtest/`
- Read-only:
  - FastAPI routes and public DTOs
  - saved-read CRUD/builders
  - frontend and Research MCP
  - research services/models
  - legacy table models and legacy readers/writers

## Admission Contract
- Validate strategy, assets/settings, range, bounds, and all canonical Variant identities before any write.
- Resolve every source Strategy/BacktestStrategy/asset before acceptance; a missing source is a pre-acceptance failure and creates no rows.
- Acquire a PostgreSQL transaction-level advisory lock dedicated to BT admission.
- Count queued + running Attempts and reject with 503 when existing count + incoming Trials exceeds `BT_PENDING_ATTEMPT_CAP`.
- In one transaction insert one Study, all Variants, all Trials, and Attempt 1 for every Trial.
- Return the preallocated Study UUID only after commit.
- No upsert and no silent dedupe; foundation uniqueness violations roll back the entire submission.

## Claim and Lease Contract
- Workers claim one queued Attempt in `(queued_at, id)` order with `FOR UPDATE SKIP LOCKED`.
- Claim is a conditional `queued → running` update and atomically:
  - records `worker_id`;
  - sets `started_at`, `heartbeat_at`, and `lease_expires_at`;
  - changes its Trial to `running`;
  - changes a queued Study to `running` and sets first `started_at`.
- A heartbeat extends the lease only when Attempt is still `running` and `worker_id` matches. Row count zero means lease loss; the worker must stop and must not commit output.
- Process memory may cache worker tasks but is never authoritative for queue membership or status.

## Exact Transition Matrix
- Attempt:
  - `queued → running`: successful claim only.
  - `queued → canceled`: cancellation request before claim.
  - `running → succeeded`: matching worker owns lease and output/lifecycle transaction commits.
  - `running → failed`: data/strategy failure or retry-exhausted infrastructure failure.
  - `running → interrupted`: expired lease or shutdown interruption.
  - `running → canceled`: cooperative cancellation acknowledgement.
  - Terminal Attempt states never transition.
- Trial:
  - `queued → running` on claim.
  - `running → succeeded` with successful Attempt.
  - `running → queued` only when a new retry Attempt is inserted.
  - `running → failed` when failure is non-retryable or retries are exhausted.
  - `queued|running → canceled` through cancellation policy.
  - Terminal Trial states never transition.
- Study rollup:
  - `queued`: every Trial queued and none has started.
  - `running`: at least one Trial is running, or queued work remains after any Trial started.
  - `succeeded`: every Trial succeeded.
  - `partially_succeeded`: at least one succeeded and at least one failed/canceled.
  - `failed`: none succeeded and every non-canceled Trial failed.
  - `canceled`: none succeeded and every Trial canceled.
- Study counts are query-derived and never stored as authoritative counters.

## Completion and Idempotency
- Success transaction:
  1. lock Attempt and verify `running`, matching worker, and unexpired lease;
  2. call `persist_bt_attempt_output()` with the same session;
  3. mark Attempt and Trial succeeded;
  4. recompute Study rollup;
  5. commit once.
- Any failure rolls back output and statuses. The still-running Attempt is later recovered by lease expiry.
- Attempt identity is insert-only `(trial_id, attempt_number)`.
- Claim uses conditional state and worker ownership; losing races return no work.
- A partial unique success constraint prevents two successful Attempts for one Trial.
- Recovery handles each stale Attempt under row lock; concurrent recovery workers cannot create the same next attempt.

## Retry and Recovery Contract
- `BT_ATTEMPT_MAX_PER_TRIAL = 2` total Attempts.
- Infrastructure failure:
  - terminalize current Attempt as failed;
  - if below cap, insert Attempt N+1 queued and return Trial to queued;
  - otherwise fail Trial.
- Expired lease:
  - mark current Attempt interrupted with `bt.lease_expired`;
  - apply the same capped new-Attempt rule.
- Data, strategy, and cancellation outcomes never retry.
- Graceful manager stop stops claims, allows configured drain time, then leaves uncompleted running Attempts to expire and recover; it does not rewrite them to failed.

## Failure Taxonomy
- Pre-acceptance: request/identity/range/asset validation—no Study.
- `data`, non-retryable:
  - incomplete or insufficient candle window → `bt.candle_incomplete`;
  - deterministic missing required data after acceptance → `bt.data_missing`.
- `strategy`, non-retryable:
  - invalid engine input → `bt.engine_input_invalid`;
  - no engine result → `bt.engine_no_results`;
  - missing asset settings → `bt.asset_settings_missing`;
  - strategy/engine exception during execution stage → `bt.strategy_runtime_error`.
- `infrastructure`, retryable:
  - reference-data transport/service failure → `bt.refdata_unavailable`;
  - exchange/candle transport failure → `bt.candle_fetch_failed`;
  - output transaction failure → `bt.result_commit_failed`;
  - unexpected exception outside strategy execution → `bt.execution_infrastructure_error`.
- `interrupted`, retryable:
  - expired lease → `bt.lease_expired`;
  - scheduler shutdown/cancellation → `bt.scheduler_interrupted`.
- `canceled`, non-retryable: `bt.canceled`.
- Classification is based on the executor stage plus typed exceptions; a generic exception is not automatically considered infrastructure when thrown inside strategy execution.
- `error_details_json` may contain safe structured diagnostics and exception type, never secrets.

## Configuration Contract
- Add:
  - `BT_PENDING_ATTEMPT_CAP = 1024`
  - `BT_ATTEMPT_WORKER_CONCURRENCY = 8`
  - `BT_ATTEMPT_MAX_PER_TRIAL = 2`
  - `BT_LEASE_TTL_SECONDS = 120`
  - `BT_HEARTBEAT_INTERVAL_SECONDS = 30`
  - `BT_RECOVERY_INTERVAL_SECONDS = 15`
  - `BT_SCHEDULER_STOP_DRAIN_SECONDS = 15`
- Validate heartbeat interval < lease TTL.
- Pending cap is global queued + running Attempts and is enforced transactionally under the admission advisory lock.
- Existing batch/persistence settings remain until the final deletion child; do not silently repurpose their meanings.

## Acceptance Checks
- Concurrent workers never double-claim an Attempt.
- Heartbeat from the wrong worker cannot extend a lease.
- Lost/expired lease creates one immutable interrupted Attempt and at most one next Attempt.
- Infrastructure failure retries once; second failure exhausts and fails Trial.
- Data/strategy failures create no retry.
- Completion failure leaves no result/artifacts and no succeeded lifecycle row.
- Mixed Trial outcomes produce `partially_succeeded`.
- Pending-cap rejection writes no hierarchy rows.
- Restart preserves queued work and recovers stale running work.
- Terminal-state mutation is rejected.
- Existing public API contract tests remain unchanged because routes are not switched here.

## Anti-Goal
- No public route/DTO projection changes, research migration, legacy deletion, grid expansion, cancellation API/UI, or legacy dual-write.

## Stop Condition
- Stop if dependencies are not accepted, output persistence cannot share the completion transaction/session, claim/recovery cannot use PostgreSQL row locks safely, or implementation requires changing public API contracts.
