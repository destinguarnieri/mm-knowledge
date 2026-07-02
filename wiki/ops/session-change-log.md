# Session Change Log

## 2026-07-02 01:15 EDT

- Investigated MON-98 ROE / max-position-drawdown semantics. Found that `MockTradingService` emits ROE as a margin-based percentage, `_compute_position_metrics()` preserves whatever ROE unit it receives, but `bt_engine._aggregate_backtest_data()` divides emitted ROE by `100.0` before building `BarPositionSnapshot`, making `max_position_dd` fractional while the mock/live ROE contract is percent-based. Existing tests cover emitted mock ROE/margin but not engine-level `max_position_dd` unit propagation. Focused pytest attempt was blocked by sandbox `.env` access during import; no code edits were made.
- 01:24 EDT: Created Linear `MON-103` under Backtesting and Evaluation to align `max_position_dd` with ROE percent-point semantics. Ticket captures the confirmed repo convention (`roe=40.0` means 40%), the `/ 100.0` aggregation mismatch, frontend double-scaling risk, acceptance criteria, regression test shape, and anti-goals.
- 01:52 EDT: Tidied MON-98 in Linear around a proof-first path. Created child issue `MON-104 Backtest golden ledger harness for percent sizing invariants` as the next high-priority proof-gate slice, moved `MON-103` under MON-98 as a narrower follow-up, related MON-103 and MON-104, and added a MON-98 comment clarifying that the harness should come first and drive subsequent poke-hole fixes.
- 15:34 EDT: Pulled Linear `MON-104` with coding-manager launch review. Scope is packageable as a deterministic synthetic golden-ledger backend harness, but launch decision is `Stop` for a cold-start worker until MON-98 ledger items 2/3 are accepted/committed or Destin explicitly launches MON-104 on the current dirty branch. No Linear brief was published because the dependency gate is not clear.
- 15:40 EDT: Destin confirmed MON-98 items 1-3 are committed. Verified `mm_v04` clean at `0801a380 Fix mock backtest leverage accounting`, published Linear doc `Brief: MON-104 Backtest golden ledger harness`, and updated the MON-104 coding-manager launch decision to `Ready`.
- 16:10 EDT: Implemented MON-104 locally with new backend golden ledger harness `backend/tests/backtest/test_backtest_golden_ledger_percent_sizing.py`. The test-local oracle covers fee-free/no-slippage/1x flat -> long -> hold/MTM -> close runs at 10%, 50%, and 100%, asserts public orders/fills/positions/PnL/metrics plus actual-output proportionality, and adds missing-settings/missing-account invariant failures. Verification: focused + adjacent anchor pytest passed (`14 passed, 2 warnings`), py_compile passed, and Cursor lints are clean. No production backtest code was changed.
- 16:52 EDT: Tightened the MON-104 harness after review. Changed the price path to distinct hold and close prices (`100 -> 95 -> 90`), made `total_volume` oracle explicit as open fill notional plus close fill notional, and removed/documented unused ledger-row fields by moving checked account/metric expectations into a summary oracle. Verification remains green: focused + adjacent anchor pytest `14 passed, 2 warnings`, py_compile passed, and Cursor lints are clean.
- 17:25 EDT: Read MCP engineering docs and made a narrow `research_mcp` patch for the real 10/50/100 backtest characterization loop. `run_backtest` now passes through `assets` for per-run settings like `max_position_percent`, and new read-only `get_saved_run_asset(run_id, asset_id)` hydrates artifact-bearing saved single-run asset detail. Updated Research MCP runbook and KB MCP contract/checkpoint docs. Verification: focused Research MCP suite passed outside sandbox (`18 passed`); sandboxed run is blocked by `.env` access.

## 2026-07-01 22:26 EDT

- Ran MON-98 coding-manager orientation/deep dive from Linear: "Backtest sizing invariants: make position % behavior explicit and testable."
- Traced sizing from request asset settings through `BacktestStrategy.current_and_max_position_value()`, strategy signal/vol/limit helpers, mock trading accounting, `bt_engine`, and metrics.
- Identified likely failure modes before narrowing: missing asset-settings fallback to 100% initial capital, implicit compounding from current equity, leverage-as-sizing-only behavior, inconsistent vol/limit ordering across strategies, USD-value vs executable-size helper split, and absolute min/dust thresholds that affect low-exposure runs disproportionately.
- Recommended narrowing MON-98 around a canonical sizing contract plus deterministic 10/50/100 fixtures before broad implementation.
- 22:51 EDT: Created Linear issue-linked document `Brief: MON-98 Backtest sizing invariants` with issue ledger, canonical sizing contract, diagnostic/contract worker slice, coding-manager launch review (`Ready` for the diagnostic slice only), and worker kickoff prompt. Document URL: https://linear.app/money-machine/document/brief-mon-98-backtest-sizing-invariants-363ac35be098
- 23:58 EDT: Implemented MON-98 ledger item 1 as manager-boundary validation: single and batch backtest execution now reject empty/missing/duplicate/mismatched asset settings before settings can reach `BacktestContext`/strategy sizing. Request DTOs remain data shapes. `BacktestContext` now requires `asset_settings`, and `current_and_max_position_value()` raises instead of falling back to 100% initial capital when settings are missing. Focused validation tests passed (`11 passed, 2 warnings`); touched files compile and lints are clean. A broader service test body passed but root DB fixture teardown still has an unrelated portfolio/user FK cleanup issue.
- 00:14 EDT: Ran coding-manager acceptance pass for MON-98 ledger item 1 against Linear ticket/brief and committed diff `b7b46492`. Decision is `Narrow`: behavior matches the missing-settings fallback fix, but the commit includes accidental scratch file `backend/app/services/backtest/Untitled`. Sandboxed pytest re-run was blocked by `.env` permission access during collection; prior focused passing validation remains the current verification baseline.
- 00:42 EDT: Implemented MON-98 ledger item 2 locally. Backtest engine now marks mock portfolio/account state to the current candle close before same-close strategy sizing, preserving post-decision MTM as the emitted no-trade event path. Added deterministic sizing invariant tests for current-close decision-time MTM and marked-current-equity percent scaling; tightened missing `crossMarginSummary` invariant handling. Verification: focused backtest tests passed (`21 passed, 2 warnings`), touched Python files compile, and Cursor lints are clean.
- 00:58 EDT: Implemented MON-98 ledger item 3 locally. `MockTradingService.configure()` now receives required per-asset settings from `BacktestContext`; mock open/MTM accounting emits configured leverage, `margin_used = notional / leverage`, and ROE on margin instead of initial account value. Added focused leverage-accounting tests for open, MTM, and missing-settings failure; updated direct mock-service tests to configure explicit settings. Verification: leverage/accounting focused suite passed (`27 passed, 2 warnings`), touched Python files compile, and Cursor lints are clean. Wider run including EMAC v2 remains affected by pre-existing MON-102 strategy expectation failures.

## 2026-07-01 21:32 EDT

- Reset MON-97 continuity to clean planning/review state after Destin confirmed prior partial work should be discarded.
- Removed tracked leftover test file `backend/tests/backtest/test_backtest_metrics.py`; no MON-97 implementation code was changed.
- Updated `wiki/ops/current-checkpoint.md` to remove stale partial-implementation claims and set next action to fresh coding-manager review and plan.
- 21:50 EDT: Implemented MON-97 narrow fix in `mm_v04`: explicit fill-level `trade_pnls` now drive backtest trade stats, fee-inclusive PnL points/fees remain intact, backtest UI labels now say `Trade Win Rate`, and vectorbt evaluator was only updated for signature compatibility. Verification: edited Python files compile and Cursor lints are clean; targeted pytest could not run because `uv run` cannot spawn `pytest`, and direct smoke execution could not import `pandas` in the current uv environment.
- 21:57 EDT: Corrected MON-97 trade-outcome thresholds to use domain-specific constants: `EXCHANGE_MIN_NOTIONAL_USD` for start-exposure dust and `POSITION_EPS_USD` for gross closed-PnL dollar noise, replacing the initial `DIV_EPS` checks. Recompiled edited backend files and lints remain clean.
- 22:05 EDT: Resolved multi-root workspace uv issue by running backend tests with explicit `--project /Users/destinguarnieri/Desktop/codebase/mm_v04/backend`. Focused MON-97 tests now pass (`8 passed, 2 warnings`). Wider `tests/backtest` run currently has unrelated/out-of-scope failures (`44 passed, 8 failed, 2 warnings`).
- 22:09 EDT: Created Linear `MON-102` under Backtesting and Evaluation to restore the full `backend/tests/backtest` suite to green. Ticket includes the exact reproduction command, focused MON-97 passing baseline, all 8 observed failures, acceptance criteria, and anti-goals.

## 2026-06-29 02:04 EDT

- Normalized copied agent templates into `wiki/agents/templates/` and updated `wiki/index.md` routing for the template directory.
- Updated `mm_v04/.cursor/skills/` pointers away from source-repo `docs/meta/...` paths to Money Machine KB template paths where matching files exist.
- Cleaned stale `docs/meta/...` references inside the agent templates themselves.
- Missing brought-over source docs/templates were identified in `wiki/ops/current-checkpoint.md`; no Money Machine runtime/product code was edited.

## 2026-06-29 01:04 EDT

- Coding-manager orientation resumed MON-97 from dirty files and `wiki/projects/MON-97-backtest-metrics-plan.md`; no `mm_v04` code edits were made.
- Found MON-97 is not acceptance-ready yet: `backend/app/services/backtest/bt_eval_tmp.py` still has a stale positional `compute_perf_metrics` call, and chunk 4's aggregate/engine-level regression is not implemented.
- Verification attempt `PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run pytest --confcutdir=tests/backtest tests/backtest/test_backtest_metrics.py -q` failed before collection because `pytest` was not available to `uv run`.

## 2026-06-29 00:05 EDT

- Resumed backtest issue work with read-only orientation on Linear tickets MON-97 through MON-101.
- Inspected backend backtest engine/metrics/mock-service/manager/helper/signal paths and frontend chart route/component surfaces.
- No `mm_v04` code edits were made in this orientation pass; pre-existing PRI local changes remain in the worktree.
- Recommended implementation order: MON-97 metrics denominator first, then MON-98 sizing invariants, MON-99 signal semantics, MON-100 fetch pagination, and MON-101 UX after screenshot/context.
- Added `wiki/projects/MON-97-backtest-metrics-plan.md` with an executable plan for classifying trade outcomes from raw fills before fee-inclusive PnL points collapse the data.
- 00:30 EDT: Completed MON-97 chunk 1 RED tests in `backend/tests/backtest/test_backtest_metrics.py`. Replaced a stale broken `sma_cross` integration test that imported a non-existent module with focused pure metric tests. Verification produced expected RED result: two failures because `compute_perf_metrics()` does not yet accept `trade_pnls`; legacy fallback test passed.
- 00:41 EDT: Completed MON-97 chunk 2. Added optional `trade_pnls` to `backend/app/services/backtest/metrics.py`; when supplied, trade metrics use explicit trade outcomes and ignore fee-only/no-trade PnL points, while legacy `pnl_points` fallback remains. Targeted test file now passes: `3 passed in 0.84s`.
- 00:49 EDT: Completed MON-97 chunk 3. Added `_fill_trade_outcome()` in `backend/app/services/backtest/bt_engine.py` to classify raw fills before PnL-point collapse, collect `trade_pnls` in `_aggregate_backtest_data()`, and pass them into metric computation. Added fill-classification unit coverage. Targeted test file now passes: `6 passed, 2 warnings in 1.50s`.

## 2026-06-28 23:10 EDT

- Verified `price_reversal_v2` had a return-contract bug: the exception path returned `None` despite the `PriceReversalV2` return annotation and callers indexing the result as a dict.
- Fixed `backend/app/lib/signals/pri_v2.py` to return a neutral `PriceReversalV2` fallback with fresh empty list fields on errors.
- Added `backend/tests/indicator/test_pri_v2.py` regression tests for the exception fallback and mutable-list freshness.
- Verification: direct fallback assertion passed; isolated pytest passed with `PYTHONPATH=/Users/destinguarnieri/Desktop/codebase/mm_v04/backend uv run pytest --confcutdir=tests/indicator tests/indicator/test_pri_v2.py`.
- Note: normal pytest invocation hit root `.env` access through repo-level `tests/conftest.py`, so isolated indicator pytest was used to avoid secret-file access.

## 2026-06-28 22:26 EDT

- Created Linear tickets MON-97 through MON-101 for backtesting correctness/UX issues from Destin's backtester complaint list.
- Fixed QMD local install mismatch by reinstalling `@tobilu/qmd@2.5.3` with Bun; verified `qmd status`, `qmd update`, and keyword search work.
- Decided operating model: Money Machine KB is an Obsidian-compatible linked markdown wiki; QMD is indexed search/retrieval over it; prompts enforce discipline/hygiene.
- Patched `~/.hermes/SOUL.md` with global knowledge/continuity discipline.
- Patched `mm_v04/AGENTS.md` with Money Machine KB usage, checkpoint, and changelog requirements.
- Rewrote `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/AGENTS.md` as the KB operating contract.
- Initialized `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/wiki/` with index/log and core context pages.
- Updated canonical checkpoint path: `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/wiki/ops/current-checkpoint.md`.
- Reorganized `/Users/destinguarnieri/Desktop/codebase/mm-knowledge` so canonical category markdown lives under `wiki/` instead of duplicate top-level category folders.
- Moved historical prompt dumps to `archive/prompts_DUMP/` and pointed QMD collections at `wiki/` paths.
- Added `scripts/check_wikilinks.py`; verified current wiki links with `missing=0` and `ambiguous=0`.
- Created Hermes skill `moneymachine-knowledge-base` for Money Machine wiki/QMD workflow.
- Redirected repo prompt/changelog discipline away from `mm_v04/docs/work/*` and into the KB paths under `mm-knowledge/wiki/ops/`.
