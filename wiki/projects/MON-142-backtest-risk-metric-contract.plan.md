---
name: MON-142 Backtest Risk Metric Contract
overview: Clarify the two backtest risk labels and normalize both summary values to negative decimal fractions without changing their underlying risk semantics.
todos:
  - id: metric-contract
    content: Normalize max_position_dd to a decimal fraction and document both risk metrics
    status: pending
  - id: persisted-values
    content: Atomically migrate saved single-run and batch aggregate values
    status: pending
  - id: consumers
    content: Update UI, generated schema, and Research MCP labels and formatting
    status: pending
  - id: verification
    content: Prove computation, migration, hydration, and consumer compatibility
    status: pending
isProject: false
---

# MON-142 Backtest Risk Metric Contract

Date: 2026-07-11  
Status: ready for bounded implementation  
Linear: `MON-142`

Related: [[research/trading/emac-cross-10-200/emac-cross-10-200|EMA Cross 10/200 Research]], [[sessions/current-checkpoint|Current Checkpoint]].

## Outcome

Make the backtest contract unambiguous:

- `max_drawdown` remains peak-to-trough mark-to-market account-equity drawdown.
- `max_position_dd` remains the worst adverse ROE observed on an active position bar.
- Both values use the same wire and persistence unit: a non-positive decimal fraction.
- User-facing and schema labels explicitly name the distinct scopes.

Examples after this change:

- `max_drawdown = -0.1667` displays as `-16.67%`.
- `max_position_dd = -0.0909` displays as `-9.09%`.

The existing API keys remain unchanged for compatibility. `max_position_dd` is a legacy key; its OpenAPI title and description become **Worst Active Position ROE**.

## Why This Work Exists

The EMA 10/200 review exposed a real interpretation failure: the abbreviated `Max Drawdown` label was read as the worst individual strategy loss, while `max_position_dd` sounds like a peak-to-trough position drawdown even though it is worst active-bar margin ROE. The generated schema currently supplies titles but no scope or unit descriptions.

The current no-build alternative is to restate both definitions manually in every research note. That does not remove the ambiguity from UI, saved-run responses, generated clients, or Research MCP. The smallest durable fix is one coordinated contract correction; it does not justify a new risk framework or metric family.

## Locked Semantic Contract

### Peak-to-Trough Equity Drawdown

- API key: `max_drawdown`.
- Label: **Peak-to-Trough Equity Drawdown**.
- Formula: minimum of `equity / cumulative_equity_peak - 1`.
- Equity source: per-bar mark-to-market `crossMarginSummary.accountValue`, including unrealized PnL.
- Unit: decimal fraction.
- Sign: non-positive; `0.0` means no decline from an observed peak.

### Worst Active Position ROE

- API key: `max_position_dd` for compatibility.
- Label: **Worst Active Position ROE**.
- Formula: minimum finite active-bar position ROE, clipped at `0.0`.
- Active identity: the existing `abs(position value) > EXCHANGE_MIN_NOTIONAL_USD` rule.
- Source position-event ROE remains in percentage points; only the summary metric divides the selected minimum by `100`.
- Unit at the `PerformanceMetrics`, persistence, batch aggregate, API, MCP, and frontend boundaries: decimal fraction.
- Sign: non-positive; `0.0` means no sampled active position was underwater.

This metric is not peak-to-trough position giveback, continuous intra-bar MAE, or realized trade loss.

## Identity, Type, and Compatibility

- Saved-run identity remains `(run_id, asset_id)`; batch aggregate identity remains `run_id`. Unit conversion does not create a new run or alter strategy/result identity.
- `PerformanceMetrics.max_drawdown` and `PerformanceMetrics.max_position_dd` are both `float` decimal fractions.
- `AggregatedPerformanceMetrics.max_drawdown` and `.max_position_dd` contain mean/median statistics over decimal fractions.
- Position events and `BacktestPositionChartPoint.roe` remain percentage points. They are a separate event/chart contract and must not be divided by `100`.
- `fees_pct_volume` and live `PerformancePolicyRules.max_drawdown_pct` retain their existing percentage-point contracts; MON-142 is limited to the two backtest summary metrics.
- API field names remain stable. This is still a breaking semantic correction for `max_position_dd`, so backend, migration, generated client, frontend, and Research MCP documentation ship together.

## Backend Computation

In `backend/app/services/backtest/metrics.py`:

- Keep `BarPositionSnapshot.roe` in percentage points.
- In `_compute_position_metrics()`, select the worst finite active ROE exactly as today, then divide that selected value by `100.0` before returning `max_position_dd`.
- Rename local variables and docstrings to `worst_active_position_roe` where practical; do not rename the public API key.
- Preserve flat, dust, non-finite, and never-adverse behavior.
- Leave `max_drawdown_from_equity()` unchanged.

In `backend/app/data_models/dto/performance.py`:

- Add explicit `Field` titles and descriptions for both metrics, including scope, sign, and decimal units.
- Do not add aliases that create two wire keys.

## Persisted-Value Migration

Create one Alembic revision after `f8a9b0c1d2e3`.

Upgrade, in one database transaction:

1. Validate every non-null `bt_backtest_batch_aggregate.max_position_dd` payload has the expected object shape and numeric-or-null `mean` / `median` members. Abort on malformed rows.
2. Divide non-null `bt_backtest_run_asset.max_position_dd` values by `100.0`.
3. Divide numeric batch aggregate `mean` and `median` values by `100.0`, preserving null members and null columns.
4. Set `bt_backtest_batch_aggregate.aggregate_metrics_schema_version = 2`.

Downgrade reverses the transform:

1. Validate the same payload shape.
2. Multiply single-run and numeric aggregate values by `100.0`.
3. Restore `aggregate_metrics_schema_version = 1`.

Failure semantics:

- The migration is atomic: malformed aggregate JSON or any conversion failure leaves all rows and schema versions unchanged.
- Backtest writers must be quiesced while the migration runs so no percent-point row can be inserted after the conversion scan.
- Alembic revision state provides exactly-once application. Do not add runtime heuristics such as “divide values whose magnitude exceeds one”; leveraged ROE can legitimately exceed `100%`.
- New writes use aggregate schema version `2` in `backend/app/services/backtest/async_backtest_backend.py` and `backend/app/models.py`.
- Hydration reads canonical decimal values directly after migration; it must not apply a second conversion.

## Consumer Updates

Frontend:

- Replace backtest labels `Max Drawdown` with **Peak-to-Trough Equity Drawdown**.
- Replace displayed `Worst Position ROE` / `Worst Pos ROE` with **Worst Active Position ROE**.
- Format `max_position_dd` with the same decimal-percent formatter as `max_drawdown`.
- Remove `max_position_dd` from percentage-point formatter sets and delete now-unused formatter helpers.
- Do not alter live performance-policy labels or units.

Known consumers:

- `frontend/src/components/Backtest/SingleRunDataView.tsx`
- `frontend/src/components/Backtest/BatchResultsSummary.tsx`
- `frontend/src/components/Backtest/BatchResultsTable.tsx`
- `frontend/src/routes/_layout/backtest.backtest.tsx`

Schema and agents:

- Regenerate the frontend OpenAPI client after the DTO descriptions change.
- Update `research_mcp/doc/runbook.md` to define both keys, decimal units, and distinct semantics.
- Research MCP remains a pass-through and performs no conversion.
- Existing historical research prose may continue displaying percentages; do not mechanically rewrite prior reported results.

## Focused Negative-Path Tests

Backend metric tests:

- ROE path `0`, `+45.45`, `-9.09` produces `max_position_dd == -0.0909`, not `-9.09` and not peak-to-trough `-0.5454`.
- Positive-only active ROE returns `0.0`.
- Flat/dust rows and non-finite ROE do not create adverse values.
- Position event and position-chart ROE remain percentage points while the summary value is decimal.
- Leveraged ROE below `-100%` converts arithmetically without magnitude heuristics or clipping.
- `max_drawdown` remains unchanged for a fixed equity path, including `$100,000 → $150,000 → $125,000 == -1/6`.

Persistence and migration tests:

- Upgrade converts populated single-run and batch mean/median values exactly once and sets schema version `2`.
- Null columns and null aggregate members remain null.
- Malformed aggregate JSON fails without partially converting single-run rows or bumping versions.
- Downgrade restores the original percent-point values and schema version `1`.
- Upgrade → hydrate returns the same decimal value as a newly computed run.
- Repeated saved-run and saved-batch retrieval does not reconvert values.

Consumer tests:

- OpenAPI exposes the explicit titles/descriptions and stable field names.
- Single, batch-summary, batch-table, and route-level UI labels use the accepted wording.
- All displayed backtest risk values multiply decimal fractions by `100` exactly once.
- Research MCP single, batch, and saved-run responses preserve the backend decimal value unchanged.

## Verification

Run:

- focused backend metric, persistence, saved-run, and migration tests;
- all non-destructive backend backtest tests;
- focused Ruff, mypy, and compile checks;
- Research MCP deterministic tests;
- frontend client generation, lint, and build;
- Alembic upgrade/downgrade/upgrade on populated representative rows, ending at head;
- static search proving no backtest `fmtPctPoints(max_position_dd)` or abbreviated labels remain.

Do not start backend/compose, run network-backed backtests, or perform any live runtime, trading, account, strategy-lifecycle, deployment, or capital mutation without separate authorization.

## Non-Goals

- No change to the two formulas beyond `max_position_dd` unit conversion.
- No API key rename, duplicate compatibility field, or database column rename.
- No new MFE, MAE, exit-efficiency, position-giveback, or realized-loss metric.
- No change to ranking rules, risk thresholds, live performance policies, position-event ROE, or charts.
- No backfill of prose values in historical research documents.

## Terminal Condition

MON-142 is complete when new and migrated saved results expose both backtest risk summaries as documented decimal fractions, every backtest consumer uses the explicit labels and one decimal-percent formatter, migration round-trip and negative paths pass, and no unrelated runtime or research behavior changes.
