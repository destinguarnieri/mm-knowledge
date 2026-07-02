# Current Checkpoint

Date: 2026-07-02 17:25 EDT

## Current State

Research MCP has a narrow local patch to unblock 10/50/100 backtest characterization:

- Read MCP docs first: `wiki/engineering/mcp-api-inventory.md`, `wiki/engineering/mcp-v1-contract.md`, and `wiki/engineering/research-mcp-checkpoint.md`.
- Scope stayed small and research-only: no live trading, batch backtest, account, websocket, or backend-internal import surface was added.
- `run_backtest` now accepts/passes the backend `assets` list so callers can set per-run asset settings such as `max_position_percent`.
- Added `get_saved_run_asset(run_id, asset_id)` to hydrate saved single-run asset detail via `/api/v1/backtest/run/saved/{run_id}/asset/{asset_id}` with concise `artifact_counts` plus raw backend detail for diagnostics.
- Updated `research_mcp/doc/runbook.md` and KB MCP contract/checkpoint docs to match the new tool surface.

Verification:

- Focused Research MCP suite passed outside the sandbox: `uv run --project /Users/destinguarnieri/Desktop/codebase/mm_v04/research_mcp pytest /Users/destinguarnieri/Desktop/codebase/mm_v04/research_mcp/tests/test_run_backtest_client.py /Users/destinguarnieri/Desktop/codebase/mm_v04/research_mcp/tests/test_run_backtest_tool.py /Users/destinguarnieri/Desktop/codebase/mm_v04/research_mcp/tests/test_saved_runs_client.py /Users/destinguarnieri/Desktop/codebase/mm_v04/research_mcp/tests/test_saved_runs_tools.py /Users/destinguarnieri/Desktop/codebase/mm_v04/research_mcp/tests/test_smoke.py -q` -> `18 passed`.
- Cursor lints found no issues in touched Research MCP source/tests.
- The same test run failed inside the sandbox only because app settings tried to read `.env` and hit `PermissionError`.
- QMD index update succeeded outside the sandbox after KB edits.

Next action: restart/reload the Research MCP server/tool descriptors if needed, then use `list_saved_runs`, `get_saved_run`, `get_saved_run_asset`, and `run_backtest` with explicit `assets` to characterize the real 10/50/100 strategy runs.

MON-104 implementation is complete locally:

- Added `backend/tests/backtest/test_backtest_golden_ledger_percent_sizing.py` in `mm_v04`.
- The harness uses one synthetic asset, fee-free/no-slippage/1x settings, and a mechanical test-local strategy over a deterministic flat -> long -> hold/MTM -> close path with distinct hold and close prices (`100 -> 95 -> 90`) so fill volume cannot be confused with hold notional.
- Expected ledger rows are handwritten in the test and now only retain fields asserted against public outputs; expected fill volume, final PnL, return, drawdown, and average active position size live in a checked summary oracle.
- Assertions cover public `orders`, `fills`, `positions`, `pnl_points`, and `performance_metrics`, including actual-output proportionality across 10%, 50%, and 100% runs.
- Negative-path coverage asserts missing asset settings and missing account snapshots fail as invariants instead of defaulting to full size or reusing prior equity.
- No production implementation files were changed. The known `max_position_dd` ROE unit mismatch remains under MON-103; this harness asserts account/equity drawdown and public position ROE, not a MON-103 fix.

Verification:

- `PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run --project /Users/destinguarnieri/Desktop/codebase/mm_v04/backend pytest --confcutdir=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_backtest_golden_ledger_percent_sizing.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_backtest_sizing_invariants.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_bt_engine_mtm_on_no_position_events.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_mock_trading_service_leverage_accounting.py -q` -> `14 passed, 2 warnings`.
- `py_compile` passed for the new test file.
- Cursor lints clean for the new test file.
- First sandboxed pytest attempt was blocked by `.env` access during import; the passing pytest run was rerun outside the sandbox.

Next action: run coding-manager acceptance review for MON-104, then commit the new harness if accepted.

MON-104 coding-manager launch gate is now clear:

- Linear `MON-104 Backtest golden ledger harness for percent sizing invariants` is the next high-priority child proof gate under MON-98.
- Ticket scope is clear enough to package: build a deterministic synthetic golden-ledger backend harness that compares 10%, 50%, and 100% fee-free/no-slippage/1x runs against independently computed expected ledger values.
- MON-98 ledger items 1-3 are committed; item 1 is `b7b46492 Harden backtest asset settings contract`, and items 2/3 are `0801a380 Fix mock backtest leverage accounting`.
- Created Linear issue-linked document `Brief: MON-104 Backtest golden ledger harness` with coding-manager launch review decision `Ready` and a worker kickoff prompt: https://linear.app/money-machine/document/brief-mon-104-backtest-golden-ledger-harness-f977d3b900a4
- Next action: launch the MON-104 worker with the kickoff prompt from the brief, then review the worker's 2-4 bullet plan before coding.

MON-98 ROE / max-position-drawdown semantics investigation found a narrow unit mismatch:

- `MockTradingService` now emits `PositionEvt.roe` as a percentage on margin (`upnl / margin_used * 100`) and uses configured leverage for `margin_used`.
- `_compute_position_metrics()` treats `BarPositionSnapshot.roe` as an opaque numeric series and returns peak-to-trough drawdown in the same units it receives.
- `_aggregate_backtest_data()` currently divides emitted position-event ROE by `100.0` before storing the bar snapshot, so `max_position_dd` becomes a fraction of ROE while the mock accounting and live performance semantics are percent-based.
- The frontend formats `max_position_dd` with `fmtPct()` / `value * 100`, which masks the unit mismatch in some views but leaves the backend metric contract ambiguous and untested.
- Current coverage asserts mock emitted `roe`/`margin_used`, but does not assert engine-level `max_position_dd` unit propagation from leveraged position events.

Recommended narrow next action: add an engine/metric regression that opens a leveraged position, marks ROE up then down, and asserts `performance_metrics.max_position_dd` uses the intended unit; then remove the `/ 100.0` conversion or explicitly redefine/rename the metric contract if the fractional display contract is preferred.

Created Linear follow-up:

- `MON-103 Align max position drawdown with ROE percent-point semantics` — https://linear.app/money-machine/issue/MON-103/align-max-position-drawdown-with-roe-percent-point-semantics

Linear board tidy-up:

- `MON-98 Backtest sizing invariants` remains the umbrella issue for percent-sizing/backtest accounting trust.
- Created `MON-104 Backtest golden ledger harness for percent sizing invariants` as a high-priority child of MON-98 and the next proof-gate execution slice: https://linear.app/money-machine/issue/MON-104/backtest-golden-ledger-harness-for-percent-sizing-invariants
- Moved `MON-103 Align max position drawdown with ROE percent-point semantics` under MON-98 as a child/follow-up and related it to MON-104.
- Added a MON-98 comment clarifying the intended ordering: build the deterministic golden ledger harness first, then use it to poke holes and drive narrow follow-up fixes such as ROE/DD semantics.

MON-98 is in semantic triage / paired implementation. Ledger item 1 (missing asset settings fallback) is committed in `mm_v04` as `b7b46492 Harden backtest asset settings contract`. Ledger items 2 and 3 are committed in `mm_v04` as `0801a380 Fix mock backtest leverage accounting`.

Created Linear issue-linked document:

- `Brief: MON-98 Backtest sizing invariants` — https://linear.app/money-machine/document/brief-mon-98-backtest-sizing-invariants-363ac35be098

The document includes:

- an issue ledger for each suspected sizing failure;
- a canonical sizing contract;
- a smallest executable diagnostic/contract slice;
- coding-manager launch review decision (`Ready` for diagnostic/contract slice only);
- worker kickoff prompt.

Findings:

- MON-98 asks for explicit/testable backtest sizing semantics because 10%, 50%, and 100% position settings do not appear to scale proportionally.
- The sizing path is `BacktestRunRequest.assets` -> `BacktestContext.asset_settings_by_asset_id` -> `BacktestStrategy.current_and_max_position_value()` -> strategy signal/vol/limit helpers -> mock execution/accounting -> `bt_engine` aggregation -> `metrics`.
- Primary risk cluster is upstream of `metrics.py`: metrics consume the equity curve; non-proportional Sharpe/PnL likely enters through target sizing, rounding/min thresholds, compounding, leverage semantics, or mock accounting.
- Multiple plausible failure modes were identified before narrowing:
  - missing per-asset settings fall back to full `initial_account_value`, ignoring configured/default `max_position_percent` and leverage;
  - configured settings use current account equity, so compounding is implicit and there is no fixed-notional toggle for the ticket's linear-gross-PnL requirement;
  - `max_position_percent` is multiplied by leverage, while mock execution emits `lev_value=1` and `margin_used=value`, making leverage a sizing multiplier rather than simulated margin;
  - strategy sizing order is inconsistent: `emac_v2` applies vol adjustment before position limits, while `emac_v3` and older strategies generally clamp before vol adjustment;
  - older strategies use USD-value sizing helpers while `emac_v2`/`emac_v3` use executable-size helpers, causing rounding/min-delta behavior to differ;
  - absolute `MIN_ADJUSTMENT_VALUE`, `EXCHANGE_MIN_NOTIONAL_USD`, and venue precision can disproportionately affect 10% runs.

MON-98 launch boundary:

- Launch only the diagnostic/contract slice first.
- Worker should add deterministic sizing fixtures and minimal helper/docstring changes only if needed.
- Worker must stop if the path expands into multi-strategy rewrites, API/DB schema, or live margin modeling.

MON-98 item 1 implementation state:

- Added manager-boundary validation helpers in `backend/app/services/backtest/backtest_manager.py`.
- Single backtest execution now rejects empty, duplicate, mismatched, or extra asset settings before strategy lookup/execution.
- Batch enqueue now rejects empty, duplicate, missing, or extra asset settings before queueing.
- `_run_single_asset()` has a defensive guard before `BacktestContext` to prevent missing matching settings from reaching strategy sizing.
- Kept request DTOs as data shapes; no validation policy was moved into `backend/app/data_models/dto/backtest.py`.
- Tightened `BacktestContext` in `backend/app/data_models/dto/backtest_result.py` so `asset_settings` is required.
- Removed the `current_and_max_position_value()` fallback to `initial_account_value`; missing settings now raise before silent 100% sizing can occur.
- Added focused regression coverage in `backend/tests/backtest/test_backtest_request_validation.py`.

Verification:

- `PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run --project /Users/destinguarnieri/Desktop/codebase/mm_v04/backend pytest --confcutdir=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_backtest_request_validation.py -q` -> `11 passed, 2 warnings`.
- `py_compile` passed for touched context/manager/strategy/test files.
- Cursor lints clean for touched files.
- `backend/tests/services/test_backtest_manager_strategy_soft_delete.py` test body passed, but the broader root DB fixture teardown hit an unrelated `portfolio_owner_id_fkey` cleanup error.
- 00:14 EDT coding-manager re-run found the working tree clean and reviewed commit `b7b46492`; local sandboxed pytest re-run was blocked by `.env` permission access during collection, so the last successful focused run above remains the verification baseline.
- 00:28 EDT preflight check found `backend/app/services/backtest/Untitled` is no longer present or tracked in the current working tree.

MON-98 item 2 implementation state:

- Added pre-decision MTM in `backend/app/services/backtest/bt_engine.py`: each candle close now marks mock portfolio/account state to the current close before `strategy.consume_candle_close()` runs.
- Preserved public event shape by ignoring pre-decision MTM return events and leaving the post-decision MTM path responsible for no-trade bar emitted events.
- Tightened `_aggregate_backtest_data()` so missing `crossMarginSummary` raises a `ValueError` invariant error instead of leaking `KeyError`.
- Added `backend/tests/backtest/test_backtest_sizing_invariants.py` covering current-close decision-time MTM and current-equity percent scaling after marked unrealized PnL.
- Updated adjacent engine tests to unwrap `BacktestEngineResult.response` and assert the public `PositionEventPublic.event_type` shape.

Verification:

- `PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run --project /Users/destinguarnieri/Desktop/codebase/mm_v04/backend pytest --confcutdir=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_backtest_sizing_invariants.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_bt_engine_mtm_on_no_position_events.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_backtest_request_validation.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_bt_engine_pnl_points.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_bt_engine_equity_invariants.py -q` -> `21 passed, 2 warnings`.
- `py_compile` passed for touched engine/test files.
- Cursor lints clean for touched files.

MON-98 item 3 implementation state:

- Threaded required `asset_settings` from `BacktestContext` into `MockTradingService.configure()`.
- `MockTradingService` now stores per-asset settings by asset id and raises `ValueError` when an accounting entrypoint receives an asset without settings.
- Open/update position events now emit configured leverage and margin semantics: `margin_used = abs(position notional) / leverage`; `roe = upnl / margin_used * 100`.
- Account snapshots continue to report equity from cash plus unrealized PnL, but `totalMarginUsed` now aggregates leveraged margin instead of full notional.
- Added deterministic leverage-accounting regression coverage for open, MTM, and missing-settings paths. Existing direct mock-service tests now configure explicit 1x settings instead of relying on an implicit service default.

Verification:

- `PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run --project /Users/destinguarnieri/Desktop/codebase/mm_v04/backend pytest --confcutdir=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_mock_trading_service_leverage_accounting.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_mock_trading_service_mark_to_market.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_mock_trading_service_pnl.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_min_adjustment_clip_no_order.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_backtest_sizing_invariants.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_bt_engine_mtm_on_no_position_events.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_bt_engine_pnl_points.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_bt_engine_equity_invariants.py -q` -> `27 passed, 2 warnings`.
- `py_compile` passed for touched mock/context/test files.
- Cursor lints clean for touched files.
- A wider affected run including `backend/tests/backtest/test_emac_v2_entry_from_flat.py` still has the previously tracked MON-102 EMAC v2 strategy expectation failures; the leverage-focused paths pass.

## Prior Current State

MON-97 implementation is in progress in `mm_v04` and currently matches the approved narrow plan: correct new backtest win-rate semantics without API/DB schema changes or historical saved-run backfill.

Implemented:

- `backend/app/services/backtest/metrics.py` now computes trade stats from explicit `trade_pnls` instead of falling back to non-zero bar-level `PnlPointPublic.realized_pnl`.
- `backend/app/services/backtest/bt_engine.py` classifies raw fills before PnL-point collapse. Counted trade outcomes require start exposure above `EXCHANGE_MIN_NOTIONAL_USD` and non-fee gross closed PnL above `POSITION_EPS_USD`; fee-only opening/adding/breakeven-accounting rows are excluded.
- `backend/app/services/backtest/bt_eval_tmp.py` was changed only enough to remain compatible with the explicit metrics signature; vectorbt trade-stat parity remains separate.
- `backend/tests/backtest/test_backtest_metrics.py` was recreated with focused pure metric tests.
- `backend/tests/backtest/test_bt_engine_pnl_points.py` now asserts fee-inclusive PnL points/fees stay intact while trade win-rate counts only the real close.
- Backtest UI labels now say `Trade Win Rate` in backtest result views; live monitoring and research decile win-rate labels were intentionally left untouched.

Working tree notes:

- `mm_v04` has MON-97 edits in backtest metrics/engine/tests, the narrow vectorbt compatibility call, and backtest UI label files.
- `mm-knowledge` has checkpoint/changelog edits from this implementation pass.

Verification:

- Because the multi-root workspace made plain `uv run` pick `/Users/destinguarnieri/.venv`, backend tests must be run with explicit project selection: `uv run --project /Users/destinguarnieri/Desktop/codebase/mm_v04/backend ...`.
- Focused MON-97 tests passed: `PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run --project /Users/destinguarnieri/Desktop/codebase/mm_v04/backend pytest --confcutdir=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_backtest_metrics.py /Users/destinguarnieri/Desktop/codebase/mm_v04/backend/tests/backtest/test_bt_engine_pnl_points.py -q` -> `8 passed, 2 warnings in 0.93s`.
- Wider isolated backtest suite ran but is not clean: `44 passed, 8 failed, 2 warnings`. Failures are outside the MON-97 focused tests and include existing fixture/API drift around string `run_id`s, equity invariant expectations, EMAC v2 fill expectations, and strategy signal config hydration.
- Created Linear follow-up `MON-102` in Backtesting and Evaluation to restore the full `backend/tests/backtest` suite to green with the reproduction command and all 8 failures captured.
- `uv run python -m py_compile` passed for edited backend Python files and tests before focused pytest was working.
- Re-ran `py_compile` and Cursor lints after replacing the initial `DIV_EPS` trade-outcome checks with domain-specific exchange/position thresholds; both remain clean.
- Cursor lints reported no diagnostics for edited backend/frontend files.
- Frontend label search confirmed only intentionally untouched live monitoring and research decile labels still say `Win Rate`.

Next action: run coding-manager acceptance review for MON-97 using the focused passing tests. Treat full-suite cleanup as `MON-102` unless review finds a MON-97 causal link.

## Current Truth

Canonical continuity stack:

1. Explicit user direction.
2. `mm_v04/AGENTS.md` for repo-local safety and entrypoint instructions.
3. `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/AGENTS.md` and `wiki/index.md` for KB operating discipline.
4. `mm-knowledge/wiki/ops/current-checkpoint.md` and `mm-knowledge/wiki/ops/session-change-log.md` for continuity.
5. Linear for execution/backlog truth.
6. QMD for indexed retrieval over the KB.
7. Built-in Hermes memory only for compact global facts/preferences.

## Known Open Items

- `mm-knowledge` has untracked/moved files and should be cleaned/committed intentionally.
- QMD reports pending embeddings; run `qmd embed` when semantic retrieval should be fully online.
- Add QMD collection contexts for better retrieval.

## Prior Context

- Money Machine project skills and agent templates were normalized after being copied from another repo. The durable agent templates live under `wiki/agents/templates/`, and project skill pointers in `mm_v04/.cursor/skills/` were updated away from source-repo `docs/meta/...` paths.
- Linear tickets MON-97 through MON-101 were created for backtesting correctness/UX issues. Recommended order remains MON-97, MON-98, MON-99, MON-100, then MON-101 after backend/API semantics and screenshot context.
- `wiki/projects/MON-97-backtest-metrics-plan.md` exists as prior synthesis, but the current implementation uses the stricter post-review decision: no legacy `pnl_points` fallback for trade stats.
