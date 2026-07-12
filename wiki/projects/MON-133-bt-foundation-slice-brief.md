# Brief: MON-134 BT persistence foundation

Parent: `MON-133` — BT persistence V2 architecture.

Proposed child ticket title: **Add BT Study/Variant/Trial/Attempt foundation**

## Objective
- Add the inert, additive V2 control-plane schema and deterministic Variant identity helper without routing any execution, persistence, API, MCP, frontend, or research path to it.

## Why Now
- `MON-132` cannot safely add grids on the legacy run/batch persistence model.
- This slice establishes durable identities and database constraints that downstream execution and cutover tickets can rely on without mixing schema design with orchestration.

## Dependency State
- Parent architecture: `MON-133`, approved direction but intentionally not a worker ticket.
- Existing single/batch implementation remains authoritative throughout this slice.
- No legacy backtest tables or data are changed, copied, dual-written, or dropped.
- Downstream execution work must wait until this slice is accepted and merged.

## Exact Scope
- Add SQLModel models and one additive Alembic migration for:
  - `BtStudy` / `bt_study`
  - `BtVariant` / `bt_variant`
  - `BtTrial` / `bt_trial`
  - `BtTrialAttempt` / `bt_trial_attempt`
- Add a pure canonical identity module for `BtVariant.variant_key`.
- Add focused model, migration-constraint, and canonicalization tests.
- Do not add `BtTrialResult`, attempt artifact tables, repositories, CRUD, scheduler/lease logic, runtime creation helpers, API projections, or research migration.

## Deliverable Boundary
- Editable:
  - `backend/app/models.py`
  - one new Alembic revision under `backend/app/alembic/versions/`
  - new `backend/app/services/backtest/identity.py`
  - new `backend/tests/backtest/test_bt_persistence_foundation.py`
- Read-only:
  - `backend/app/services/backtest/backtest_manager.py`
  - `backend/app/services/backtest/backtest_persistence_service.py`
  - `backend/app/services/backtest/async_backtest_backend.py`
  - `backend/app/api/routes/backtest.py`
  - `backend/app/data_models/dto/backtest.py`
  - `backend/app/helpers/backtest.py`
  - `backend/app/crud.py`
  - `research_mcp/`
  - `frontend/`

## Exact Model Contract

### `BtStudy` / `bt_study`
- `id UUID` primary key, application-generated.
- `user_id UUID NULL` FK → `user.id`, `ON DELETE SET NULL`.
- Navigational `strategy_id UUID NULL` FK → `strategy.id`, `ON DELETE SET NULL`.
- Immutable `strategy_id_snapshot UUID NOT NULL`; no FK and never updated after insertion.
- Named consistency check: `strategy_id IS NULL OR strategy_id = strategy_id_snapshot`.
- `strategy_name_snapshot VARCHAR(255) NOT NULL`.
- Navigational `backtest_strategy_id UUID NULL` FK → `backteststrategy.id`, `ON DELETE SET NULL`.
- Immutable `backtest_strategy_id_snapshot UUID NULL`; no FK and never updated after insertion.
- Named consistency check: `backtest_strategy_id IS NULL OR (backtest_strategy_id_snapshot IS NOT NULL AND backtest_strategy_id = backtest_strategy_id_snapshot)`.
- `backtest_strategy_group_id_snapshot UUID NULL`.
- `backtest_strategy_version_snapshot INT NULL`.
- `interval VARCHAR(16) NOT NULL`.
- `min_candles INT NOT NULL CHECK min_candles >= 10`.
- `start_ms BIGINT NULL`, `end_ms BIGINT NULL`.
- Named range check: both range fields are null, or both are non-null with `0 <= start_ms < end_ms`.
- `request_json JSONB NOT NULL`.
- `retention_mode VARCHAR(16) NOT NULL CHECK IN ('metrics', 'full')`.
- `status VARCHAR(24) NOT NULL DEFAULT 'queued' CHECK IN ('queued', 'running', 'succeeded', 'partially_succeeded', 'failed', 'canceled')`.
- `submitted_at TIMESTAMPTZ NOT NULL`, nullable `started_at` and `finished_at`.
- `created_at TIMESTAMPTZ NOT NULL`, `updated_at TIMESTAMPTZ NOT NULL`.
- Indexes:
  - `(user_id, submitted_at)`
  - `(status, submitted_at)`
  - `(strategy_name_snapshot, submitted_at)`

### `BtVariant` / `bt_variant`
- `id UUID` primary key, application-generated.
- `study_id UUID NOT NULL` FK → `bt_study.id`, `ON DELETE CASCADE`.
- `variant_index INT NOT NULL CHECK variant_index >= 0`.
- `variant_key VARCHAR(64) NOT NULL`.
- Named digest-format check: `variant_key ~ '^[0-9a-f]{64}$'`; uppercase, non-hex, short, and long values are rejected by PostgreSQL.
- `variant_key_version SMALLINT NOT NULL DEFAULT 1 CHECK variant_key_version >= 1`.
- `params_json JSONB NOT NULL`, `config_json JSONB NOT NULL`, `trade_config_json JSONB NOT NULL`.
- Named JSON-shape checks require `jsonb_typeof(column) = 'object'` for each Variant JSON column; arrays, scalars, and JSON null are rejected by PostgreSQL.
- `initial_capital NUMERIC(38,18) NOT NULL`; named checks require a finite value and `initial_capital > 0`.
- `fees NUMERIC(38,18) NOT NULL`; named checks require a finite value and `fees >= 0`.
- `slippage NUMERIC(38,18) NOT NULL`; named checks require a finite value and `slippage >= 0`.
- For each NUMERIC column, finite means `column NOT IN ('NaN'::numeric, 'Infinity'::numeric, '-Infinity'::numeric)`.
- `created_at TIMESTAMPTZ NOT NULL`.
- Unique `(study_id, variant_index)`.
- Unique `(study_id, variant_key)`.
- Index `study_id`.

### `BtTrial` / `bt_trial`
- `id UUID` primary key, application-generated.
- `variant_id UUID NOT NULL` FK → `bt_variant.id`, `ON DELETE CASCADE`.
- `asset_id UUID NOT NULL` FK → `hyperliquidasset.id`, `ON DELETE RESTRICT`.
- `symbol_snapshot VARCHAR(50) NOT NULL`.
- `leverage SMALLINT NOT NULL CHECK 1 <= leverage <= 100`.
- `max_position_percent NUMERIC(38,18) NOT NULL`; named checks require a finite value and `0 <= max_position_percent <= 100`, using the same explicit special-value exclusion as Variant NUMERIC fields.
- `is_cross_margin BOOLEAN NOT NULL`.
- `status VARCHAR(16) NOT NULL DEFAULT 'queued' CHECK IN ('queued', 'running', 'succeeded', 'failed', 'canceled')`.
- `created_at TIMESTAMPTZ NOT NULL`, `updated_at TIMESTAMPTZ NOT NULL`.
- Unique `(variant_id, asset_id)`.
- Index `(variant_id, status)`.
- Index `(status, updated_at)`.

### `BtTrialAttempt` / `bt_trial_attempt`
- `id UUID` primary key, application-generated.
- `trial_id UUID NOT NULL` FK → `bt_trial.id`, `ON DELETE CASCADE`.
- `attempt_number SMALLINT NOT NULL CHECK attempt_number >= 1`.
- `status VARCHAR(16) NOT NULL DEFAULT 'queued' CHECK IN ('queued', 'running', 'succeeded', 'failed', 'interrupted', 'canceled')`.
- `failure_kind VARCHAR(16) NULL CHECK IN ('data', 'strategy', 'infrastructure', 'interrupted', 'canceled')`.
- `error_code VARCHAR(64) NULL`, `error_message TEXT NULL`, `error_details_json JSONB NULL`.
- `worker_id VARCHAR(128) NULL`, `lease_expires_at TIMESTAMPTZ NULL`, `heartbeat_at TIMESTAMPTZ NULL`.
- `queued_at TIMESTAMPTZ NOT NULL`, nullable `started_at` and `finished_at`.
- `created_at TIMESTAMPTZ NOT NULL`.
- Unique `(trial_id, attempt_number)`.
- Index `(status, queued_at)`.
- Index `(status, lease_expires_at)`.
- Partial unique index on `trial_id` where `status = 'succeeded'`.

## Immutable Strategy Snapshot Identity
- The immutable Study strategy snapshot is exactly:
  - `strategy_id_snapshot`, copied from the required resolved source Strategy UUID;
  - `strategy_name_snapshot`;
  - `backtest_strategy_id_snapshot`, when supplied;
  - `backtest_strategy_group_id_snapshot` and `backtest_strategy_version_snapshot`, when supplied.
- Navigational `strategy_id` and `backtest_strategy_id` may become null through `ON DELETE SET NULL`; they are never canonical hash inputs.
- Snapshot UUID/group/version/name fields are not FKs and are immutable after insertion.
- The Variant identity payload includes those immutable snapshot values plus:
  - `params_json`
  - `config_json`
  - `trade_config_json`
  - `initial_capital`
  - `fees`
  - `slippage`
- This identifies configuration, not deployed Python source code. Code-build fingerprinting is explicitly deferred rather than implied.

## Canonical Identity Type Contract
- Add `backend/app/services/backtest/identity.py`.
- Define a strongly typed immutable `BtVariantIdentityInput`; use `pydantic.JsonValue` for JSON values and `Decimal` for capital/cost fields. Do not use `Any` or `unknown`.
- Public helper:

```python
def compute_bt_variant_key(identity: BtVariantIdentityInput) -> str:
    """Return a lowercase 64-character SHA-256 hex digest."""
```

- Canonicalization version is fixed at `1`.
- Rules:
  - recursively sort object keys;
  - preserve list order;
  - serialize UUIDs as lowercase canonical strings;
  - serialize absent optional snapshot fields as JSON null;
  - serialize top-level `Decimal` capital/cost fields as normalized non-exponent decimal strings;
  - preserve validated JSON scalar types inside params/config/trade config;
  - reject NaN, infinity, non-string object keys, and unsupported values;
  - emit compact UTF-8 JSON and hash with SHA-256.
- Consequences:
  - reordered object keys dedupe;
  - reordered lists remain distinct;
  - changing any immutable strategy snapshot or executable config field changes the key;
  - deleting a source Strategy or BacktestStrategy cannot change the key because navigational FKs are excluded;
  - repeated content within one Study is rejected by the database unique constraint;
  - this slice does not silently dedupe or create rows.

## Concurrency Schema
- `lane`: backend persistence foundation.
- `parallel_after`: `MON-133` architecture decision only; no code dependency.
- `primary_files`: the four editable surfaces listed above.
- `lock_level`: hard on `backend/app/models.py` and the Alembic head; soft on the new identity/test files.
- `merge_blocker`: yes for every V2 execution, result/artifact, compatibility, and grid ticket.
- Database uniqueness is the concurrency guard. This slice adds no resolve/ensure/upsert helper and therefore no application-level race policy.

## Semantic Invariants
- Identity:
  - Study is distinct by UUID.
  - Variant is distinct by both deterministic index and canonical key within one Study.
  - Trial is distinct by Variant × asset.
  - Attempt is distinct by Trial × positive attempt number.
- Dedupe:
  - duplicate Variant indexes, Variant keys, Trial assets, or Attempt numbers are rejected; never silently merged.
- Failure:
  - the migration is additive and transactional.
  - canonicalization failure occurs before hashing and has no side effect.
  - lifecycle transition enforcement and failure-to-taxonomy mapping are downstream scheduler responsibilities, not invented here.
- Recovery:
  - Alembic downgrade removes only the four new empty V2 tables in child-first order.
  - Existing backtest tables and execution remain untouched and authoritative.
- Type contract:
  - canonical identity takes `BtVariantIdentityInput` and returns exactly one lowercase SHA-256 string.
  - no runtime helper may import or call this module in this slice.

## Acceptance Checks
- Alembic upgrade creates exactly the four additive tables, named checks, FKs, unique constraints, partial unique success index, and query indexes.
- Alembic downgrade drops only those four tables and leaves all legacy tables intact.
- Model metadata matches the migration for names, nullability, types, FKs, and deletion behavior.
- Canonicalization tests prove:
  - object-key ordering stability;
  - list-order sensitivity;
  - strategy snapshot/config/capital/cost changes alter the key;
  - unsupported and non-finite values fail;
  - output is deterministic lowercase SHA-256.
- PostgreSQL-backed negative tests prove duplicate Variant index/key, Trial asset, and Attempt number constraints fail.
- PostgreSQL-backed negative tests prove a non-null `strategy_id` or `backtest_strategy_id` cannot disagree with its immutable snapshot, while source deletion may null the navigational FK without clearing the snapshot.
- PostgreSQL-backed negative tests prove `variant_key` rejects uppercase, non-hex, short, and long values.
- PostgreSQL-backed negative tests prove `params_json`, `config_json`, and `trade_config_json` reject arrays, strings, numbers, booleans, and JSON null.
- PostgreSQL-backed negative tests prove every NUMERIC field rejects `NaN`, `Infinity`, and `-Infinity` in addition to its domain bounds.
- A source Strategy/BacktestStrategy deletion test proves navigational FKs may null while immutable snapshot fields and the previously computed Variant key remain unchanged.
- Cascade tests prove deleting a Study removes its Variants, Trials, and Attempts.
- Existing focused backtest tests remain green.
- No route, manager, persistence service, CRUD, DTO, MCP, frontend, result, artifact, or research code changes.

## Anti-Goal
- Do not make V2 executable. This ticket does not enqueue, claim, retry, persist metrics/artifacts, project compatibility DTOs, migrate research, or remove legacy code/data.

## Stop Condition
- Stop and hand back if the model contract requires changing a current API/runtime path, if the current Alembic head is not the expected parent, or if a required database constraint cannot be represented consistently in both SQLModel metadata and Alembic.

## Open Questions
- None. Result/artifact DDL, lifecycle transitions, failure mapping, queue bounds, compatibility projections, research migration, and destructive cutover belong to explicit downstream tickets.
