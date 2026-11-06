# Current Checkpoint

Status: in progress

Date: 2026-10-30

## Account equity chart — 2026-11-03

Implemented Destin's approved backend-derived equity series, nullable per-bar persistence, regenerated API types, Account Equity panel, and clearer realized-PnL/position-ROE labels. Migration `e24b6c91a703` is applied to `localhost:5432/app` at Destin’s explicit request; revision and nullable double-precision column verified. Changes remain uncommitted. Old runs show unavailable equity. 71 backend tests and six frontend tests pass; production build and scoped checks pass. Backend checks used the committed inventory module in memory because the user's unrelated unfinished `def match_` blocks imports; their file is untouched. See [[engineering/backtest-risk-measurement#Backend account equity chart — 2026-11-03]]. Migration prerequisite is complete. The previously observed unfinished user edit remains a separate runtime-import concern; no runtime was started.

## Independent volatility stages — 2026-11-03

Latest request: reverted only the last centered-estimator edits (history_size/per_bar_values). Example and new tests still reference those removed APIs; integration is temporarily incomplete pending the user's design. Earlier log-return support remains.

Latest: completed Destin's version-3 scorer for precomputed per-bar volatility. Example now streams centered adjustment separately from centered targeting; RMS estimation stays in features. Fixed RMS targeting timeframe and prevents double annualization through per_bar_values(). One bounded history deque per centered role; no estimator scoring methods. 402 targeted tests and scoped lint/types pass. See [[trading/backtest-strategies-index#Precomputed-volatility scorer and centered adjustment — 2026-11-03]].

Latest correction: Destin requested restoring BlendedCenteredEwmaVolatility in Example. Centered targeting now streams per asset/timeframe and reuses its snapshot blend; RMS targeting/adjustment remain the array sketch pending design. The concern is estimator state consistency, not adding score state. No estimator scoring methods restored. 396 targeted tests plus the added simple/log reference cases pass; scoped lint/types pass.

Latest review: implemented Destin's instrument_vol_scores2 array/scoring sketch, with requested optional score keys and RMS/Centered selection. Example now uses supplied-window b_score/r_score calculations, retaining no volatility state (explicit working assumption pending review). EWMAC keeps its original stateful centered estimator. 554 targeted tests and scoped lint/types pass. See [[trading/backtest-strategies-index#Requested volatility scores from price windows — 2026-11-03]].

Review follow-up: removed the Example legacy rebalance fallback; REBALANCE is now explicit/default-only. Stage-specific target names, direct capital/risk formulas, explicit volatility feature branches, and clearly grouped compatibility DTOs are implemented. 541 targeted tests and scoped lint/types pass. No commit or migration execution.

Destin authorized the per-asset weight migration alongside Example-only volatility configuration/order changes. Implemented locally: independent targeting/adjustment settings, annual b_score and relative r_score, adjustment after signal mapping, unchanged allocated-capital × leverage cap, and per-asset instrument_weight persistence/API/editor plumbing. 581 offline backend tests, three frontend tests, production TypeScript, focused lint/types pass. Migration d92e7a41c608 is prepared, not applied. No commit or push by this task. Registered strategies retain prior sizing behavior until explicitly propagated; template old POSITION_SIZING config is removed. Review the template/config layout next. Details: [[trading/backtest-strategies-index#Independent volatility stages and per-asset risk weights — 2026-11-03]].

## Playwright removal — 2026-11-03

Destin approved removing Playwright from the main checkout and machine user caches while preserving tests. Completed locally: Vitest replaces the non-browser runner (82 tests across 10 files pass); 4 browser suites/setup/helpers are retained in `frontend/tests/browser-archive/` and inactive. Playwright CI/Compose/config/packages, browser downloads, two npx caches, and the stopped repo-specific test container/image were removed. Codex bundled dependencies and other worktrees were left intact. Production TypeScript and new config lint pass; wider test typechecking retains existing Position Lab fixture/library errors. No live runtime operation, commit or push. See [[projects/position-lab-stages-1-3-plan#Test tooling update — 2026-11-03]].

## Current focus

Live startup/recovery separation planning continues. Destin has separately resumed frontend-only Terminal UI work; live terminal integration remains deferred. On 2026-10-30 Destin selected dedicated accounts per strategy and retaining strategy stop-and-flatten for the first stage, with explicit UI labeling. He agrees with separating service startup, account synchronization, and explicit flattening; detailed implementation remains proposed, not approved or implemented.

Read-only code inspection found system boot nukes all strategy-linked accounts regardless of running status; BaseStrategy start and stop also nuke. Account WS callbacks belong to strategies; clearinghouse enrichment ignores unknown positions and fill snapshots are discarded. Risk-policy strategy/portfolio halts call strategy stop, so preserve their exposure-reduction intent. Proposed first-release strategy policy: block start on existing positions/orders or uncertain account state; do not auto-resume/adopt exposure. Linear execution plan now lives in [MON-8](https://linear.app/money-machine/issue/MON-8/separate-live-startup-account-recovery-and-explicit-flattening), in Trading System Reliability, milestone Live startup and account recovery. Eight sequential children MON-237 through MON-244 cover lifecycle behavior/account scope, snapshots, local recovery, streams, flattening, lifecycle integration, UI, and release verification. All are Backlog. Destin requested reading all code changes after each chunk: provide full diff and reading order, verification and failure-path notes; wait for explicit acceptance before Done or the next chunk. Use Blocked with reason Awaiting Destin code review at handoff. Next action: discuss MON-237 lifecycle behavior and account-scope decisions. Destin explicitly deleted the proposed test harness and lifecycle test program; MON-237 is contract only. Do not reintroduce a drawn-out testing process as prerequisite work. Implementation has not begun. No runtime operation, secrets, database access, source edits, tests, commit, or push. Code working tree was clean during this inspection; older dirty-tree notes below are historical.

## Parallel frontend Terminal track

Destin approved removing linking and hover activation from the multi-chart Terminal. Local uncommitted work in `/Users/destinguarnieri/.codex/worktrees/a137/mm_v04` now uses click-selected charts to drive the ticket. Each chart owns market/timeframe/EMA visibility; ticket/watchlist changes affect only the active chart. First inactive plot gestures only select; same-market drafts survive, different-market drafts reset. Older linked layouts migrate without losing stored settings. Named layouts and Single/Two stacked/Four-chart presets remain. Chart controls now share one compact Dockview header with a drag grip, timeframe dropdown, indicator menu and palette icon. EMA 20/100 visibility is independently persisted, with older single-flag layouts migrated. The new indicator-persistence test and three affected layout checks also pass. Drawing hints/counter/trash are now removed; chart right-click offers market-scoped Clear drawings without switching the ticket. Seven affected interaction tests and static/build checks pass. All 27 isolated terminal tests, TypeScript, scoped lint, build and visual inspection pass. Execution remains unwired; checkpoint remains `db455737`, `feat/terminal`. See [[projects/trading-terminal-ui]]. No new commit or push.

## Backend test isolation track

Destin accepted the final stage on 2026-11-03 after reviewing the external candle guard explanation. MON-245/246/247 and parent MON-149 are Done. At his subsequent explicit request, committed the harness as 7e891a59 on fix/test_harness and merged it into his selected feat/work branch as 38fc3c93 in /Users/destinguarnieri/Desktop/codebase/mm_v04. Both code checkouts are clean. No push, deployment, remote CI dispatch, or live external requests. Supported commands and durable guidance: [[ops/backend-testing]]. Incremental diff /tmp/mm247-review.patch; complete change /tmp/mm149-full-review.patch.

Legacy shell entrypoints now delegate offline and no longer start/down the application stack or delete volumes. Offline/database modes run in separate CI matrix jobs with per-suite reports and combined coverage for the existing Smokeshow check. External mode uses a public-candle-only transport and a manual-only workflow; no SDK websocket/account client. Assertions retained. Changes are committed and merged locally; no push, remote CI dispatch or live external checks.

Local CI equivalents: offline 1,118 passed with the identical 41 failures/2 collection errors; DB 108 passed with the identical 2 email-related failures. The 25 new offline cases pass. Six shell entrypoints verified for exact argument forwarding, unrelated cwd, and exit-code preservation. External collection eight cases; guards verified with mocks and isolated child checks, no real requests. Coverage union checked across 355 files; reports warn about preexisting invalid forecast.py annotations, not hidden test failures. Scoped Ruff/strict mypy and diff checks pass. No disposable Docker resources remain. Full details/limitations on MON-247 and the testing guide. This track remains separate from live runtime/research work. Merge verification on feat/work: 84 focused tests and scoped Ruff pass; full offline 1,581 passed/73 failed/2 collection errors; DB 108 passed/same 2 email failures. The 47 added failure nodes versus the older worktree baseline come from existing feat/work fixtures (41 missing MultiSpeedEwmacSnapshot.trailing_annual_volatility; 6 old Example THRESHOLDS payloads); 15 old Example failures are gone. Relevant strategy/fixture files are unchanged by the merge. Fresh disposable migrations include d92e7a41c608; owned container/network cleanup verified.

## Current implementation

EWMAC retains the inline target → buffer → cap → delta → order flow, with a comment above each step. Only the order delta is rounded; intermediate inventory/target/buffer rounding is removed. Existing order-size validation is reused. Other strategy behavior remains unchanged; positions_v2 now also provides the extracted normal-risk sizing helper. User edits were preserved.

All agent changes to strategy_base_backtest.py and data_models/dto/strategy.py are reverted. EWMAC again inherits StrategyTradeConfig with its original fields and zero-constrained minimum-percentage overrides. No StrategySizingConfig, TradeConfigT, or generic base subscription remains. The prior three config/base type errors are resolved.

## Verification and boundaries

After restoring configs: existing 43 EWMAC cases pass; scoped Ruff and mypy pass on the strategy and its test file. No tests added during rollback. Earlier neighboring example-test failures remain pre-existing and untouched. No app startup, database run, live operation, commit or push. Work remains uncommitted. Await user direction; no v3 or additional migration selected. Previous Engine V2 context is historical: [[projects/backtest-engine-v2-plan]].


### Shared sizing-capital follow-up — 2026-10-27

Destin added get_sizing_capital to BacktestStrategy himself and is handling the current_and_max_position_value integration. At his request, EWMAC's duplicate _sizing_capital was removed and its two callers now use the shared method. Agent did not edit the base file. Existing static/compounding capital test and scoped Ruff pass; no new tests. Destin is also editing signed order sizing: current EWMAC uses normalize_position_size, which returns a signed float rather than None and does not enforce minimum notional. Its order submission still needs positive magnitude and zero/minimum handling; not changed in this sizing-capital edit. Earlier all-strategy-test claims predate these user edits.


### Explicit volatility naming and reusable centered estimator — 2026-10-27

Extracted the current checkout's recursive centered simple-return EWMA, annualization, bounded trailing mean, 70/30 blend, and price-unit conversion into `app/lib/utils/volatility_ewma_centered.py::BlendedCenteredEwmaVolatility`. Its immutable output type is `app/data_models/dto/volatility.py::BlendedVolatilitySnapshot`. Per review, constructor arguments `current_weight=0.70` and `trailing_weight=0.30` now configure the blend; finite nonnegative fractions must sum to one. EWMAC passes both explicitly. Annualization resolution now lives in the volatility constructor: `tf_sec` defaults to daily and the optional `annualization_factor` overrides the calendar-derived factor. `_RecursiveCarverState` accepts timeframe, not a computed factor. Shared conversion functions live in `app/lib/utils/annualization.py`; backtest metrics re-export the prior import paths. EWMAC delegates volatility while retaining candle timestamp handling, EMAs, forecasts, and sizing. State remains O(long_window): one bounded deque plus scalar moments/last close. Continuous history and partial-history startup are preserved; the October 17 fixed-window notes do not describe this checkout.

Renamed the uncentered function `ewma_vol_price` to `ewma_rms_returns` in `volatility_ewma.py` and updated all four source callers. Its simple/log return calculations are unchanged. No compatibility alias remains. User positioning edits were preserved; shared strategy base/configs were not edited.

Verification: 90 focused offline tests pass (43 EWMAC, 27 estimator, 20 backtest-metrics cases), including custom/endpoint blends, invalid weights, timeframe derivation and overrides. Scoped Ruff/mypy pass after the annualization follow-up; exact parity was rechecked over all 6 speed sets × 3000 bars. Exact equality against pre-edit source holds for every snapshot field over 6 speed sets × 3000 bars, and for both RMS return definitions. Scoped Ruff/mypy pass on five estimator/strategy/test files; the four caller files retain exactly their prior Ruff diagnostics and differ only in the symbol rename. Tests disabled parent conftest loading and dotenv reads and used synthetic settings. No app startup, database access, live operation, commit, or push. Work remains local for review.


### Reusable normal-risk sizing — 2026-10-27

Moved EWMAC's `normal_risk_quantity` method to `app/helpers/positions_v2.py` as a standalone keyword-only helper taking capital, blended annual volatility, price, instrument weight, diversification multiplier, and risk target. The strategy passes these explicitly; no strategy/config dependency was added to the helper. Formula, price validation, zero/nonfinite-volatility behavior, and nonfinite-result fallback are unchanged. Updated the existing capital-base test; no new tests. All 74 EWMAC/positions-v2 tests and scoped Ruff/mypy pass. User edits preserved; no runtime operation, commit, or push.


### Bounded EMA migration complete locally — 2026-10-27

161 focused tests pass, including six PX Threshold replay scenarios. Independent batch EMA and frozen pre-change comparisons match PX signals within tolerance and every threshold transition, order, fill, and position. EWMAC snapshots match exactly across six speed sets × 3000 bars; 22 constructor smoke checks pass. Continuous PX replay matches; Slope variant entry gates/trades match despite small normalized-slope rounding differences and its pre-existing double advance, which remains unchanged. Broader checks reproduce 22 baseline failures (15 example, one PX signal-bands mock, six outdated engine fixtures); these are not introduced by this migration. Scoped Ruff/mypy pass. See [[engineering/bounded-ema-history]]. No live runtime, deployment, new commit, or push.


### Initialization timing requested before sign-off — 2026-10-29

Reverified current working tree: 161 focused tests and 36 frozen-source/caller checks pass; scoped Ruff/mypy pass. Destin then requested a scalar-versus-EMA_P_CLEAN initialization benchmark before sign-off. With span 200 and both retaining 512 outputs, median 100k-input initialization is 23.438 ms scalar versus 6.026 ms batch (3.89x faster); 512 inputs are 0.1334 versus 0.0558 ms. Outputs agree within 4.55e-13. Details in [[engineering/bounded-ema-history]]. No source changes or new commit; awaiting user decision.


### Candle inventory execution notebook — 2026-10-31

Destin selected a signal-agnostic candle accumulation/distribution walkthrough. Created local `mm_v04/notebooks/candle_inventory_execution.ipynb`; all 12 code cells pass, including long/short accounting, strict EPS, costs, caps, reversals, invalid inputs, and causal prefix checks. Saved chart visually inspected; full notebook preview remains unverified because browser file URLs are blocked. Synthetic examples only, no Research MCP run IDs. Destin explicitly chose immediate flatten-on-opposite-signal even at a loss, then following the new signal. Fixed-unit sizing, full exits, neutral hold, and idealized same-close fills remain prototype assumptions. Next: review notebook mechanics and refine sizing/distribution and fill timing. No production code, runtime operation, commit, or push. See [[research/trading/research_index|Research Home]].


### Candle inventory backtest strategy — 2026-10-31

Destin requested a new reusable backtest strategy and explicitly selected a constant long/short signal to isolate execution. Added registered `candle_inventory`, typed config, pure `execution_actions` helper, and focused tests. Provisional defaults: add 10% of configured max notional per qualifying candle (capped), full distribution only on aligned candles with strict gross unlevered weighted-entry return > `eps=0.001`, neutral/doji hold, immediate flatten-on-opposite-signal before any new accumulation, same-close simulated fills, no terminal liquidation. Costs are accounted by the broker but excluded from the EPS test except entry slippage embedded in entry price. Override `signal_for_candle` or call the helper for other signals. State O(1); no shared base/API/live changes. Existing untracked notebook in `backend/notebooks/` preserved.

Verification: 27 focused offline cases pass, including broker accounting and full/summary engine replay; scoped Ruff and strict mypy pass. Temporary `/tmp/mm-candle-inventory-tests.py` disables dotenv reads and network, supplies synthetic settings, and excludes parent conftest loading. A four-minute large-move fixture exposed an existing CAGR exponent overflow at `services/backtest/metrics.py:251`; unchanged, execution integration verified with daily candles. No real-data run, database/catalog mutation, live startup, commit, or push. Ready for code walkthrough and sizing/return-definition refinement. See [[trading/backtest-strategies-index]].


### Candle inventory reads stored position return — 2026-10-31

At Destin's request, removed the strategy's risk_inventory access and entry-price return calculation. Execution needs signed size and stored roe only. Added MockTradingService.get_position_roe, which reads existing state without recalculation and returns zero when flat. The strategy divides percentage-point ROE by 100 to retain fractional EPS units. This supersedes the initial unlevered entry-return gate: the engine marks state before strategy evaluation, and stored ROE includes leverage and current marked margin. No change to broker return calculation or live code. Thirty-three focused strategy/mark-to-market tests pass, including long/short leverage gates and direct stored-value consumption; scoped Ruff/mypy and diff checks pass. Local and uncommitted.


### Candle inventory target/delta execution — 2026-10-31

Destin rejected sequential close/reopen orders and selected current-size versus target-size execution. Candle inventory now chooses one hold/accumulate/distribute action. Separate _accumulate and _distribute methods calculate the signed target; distribution currently targets zero. One rounded target-minus-current delta is submitted through the mock market executor, including cross-zero reversals. Current size is read once; no post-close re-read or intermediate flatten order. Reversal on a qualifying accumulation candle targets one increment on the new side; otherwise it targets zero. This supersedes the earlier ordered flatten/accumulate helper; the reusable helper is now execution_action. Existing stored-state ROE and fractional EPS remain. Thirty-six focused strategy/mark-to-market checks pass, including both one-order reversal directions; scoped Ruff/mypy and diff checks pass. No live changes, database mutation, commit, or push.


### Candle inventory uses standard sizing flow — 2026-11-01

At Destin's request, removed aligned_size, notional-room arithmetic, and the minimum-target-to-zero rule from accumulation. _accumulate now returns current size plus a signed increment, or one new-side increment for a reversal. The caller explicitly caps the desired target, computes target minus current, and uses existing executable_order_size for precision/minimum validation on all orders including exits. Hold remains unchanged. Accumulation now corrects already-over-cap inventory subject to executable delta; undersized additions no longer turn into exits. Thirty-six focused strategy tests pass, including long/short over-cap and small-inventory regressions; scoped Ruff/mypy and diff checks pass. No real-data backtest, live operation, commit, or push. Other concurrent working-tree edits preserved.


### Opposing inventory handled by execution decision — 2026-11-01

Destin selected distribution-first behavior for opposing inventory. execution_action now checks opposing position/signal signs before candle accumulation and returns distribute regardless of candle color or loss. The strategy targets zero for that candle; accumulation on the new side waits for a later qualifying candle. Removed the reversal branch from _accumulate, which now only returns current size plus a signed increment. This supersedes same-candle cross-zero targets in earlier notes. Thirty-six focused strategy tests and scoped Ruff/mypy pass, including both directions closing at a loss and entering only on a later candle. One current-size read and one target-minus-current order per decision remain. No real-data run, live operation, commit, or push.


### Backtest execution visibility — 2026-11-01

Added toggleable fill-price dots (green buy/red sell) and hover detail using existing artifacts. Preserved the original USD panel and visibility under Position USD; added independent signed Position Quantity (units). No decision/API plumbing changes. Seven focused frontend tests, scoped lint and production build pass; isolated headless Chrome checks confirm actual markers, separate values, persisted toggles and panel rebuilds without browser errors. Synthetic visual inspection complete; no backend startup or research run. Local uncommitted changes; see [[trading/backtest-strategies-index]].


### Candle inventory cap-induced reduction identified — 2026-11-01

Retrieved full saved run `ee9ea3ce-fda8-495b-b34f-fad0812d32cd` through Research MCP at Destin's request. Traced LINK 4h short-signal buy of 14.2 units at 2026-10-12 04:00 UTC: green candle selects accumulate, but compounding equity cap is below existing short exposure, so unconditional target clamping produces a buy reduction despite negative position return. Saved fill/position evidence and reconstructed target delta agree. Destin subsequently confirmed this is intended risk management: accumulation requests remain subject to the cap, including forced reduction of existing over-cap exposure. No fix requested; preserve current behavior. No new backtest or live operation. See [[trading/backtest-strategies-index]].


### Candle inventory execution mechanics accepted — 2026-11-01

Destin considers this execution style a working implementation after visual inspection of both fixed signal directions and explanation of cap-driven reduction. Fraction semantics and sizing optimality remain TBD. Reuse the pure action helper with strategy-specific accumulation/distribution targets and standard downstream cap/delta/order flow. No code change or new run. See [[trading/backtest-strategies-index]].


### Position helpers simplified; target floor removed — 2026-11-01

Destin approved the helper refactor and removing MIN_POSITION_VALUE_PCT. Migrated all Python callers to explicit cap → quantity → delta/deadband → executable-order flow; removed plan builders/types, unused helpers, and target-floor config/forwarding. Shared production-strategy callers use cap-only sizing too; no runtime operations. Old saved configs containing the retired key now fail with a removal message. Actual quantity is read without normalization; order rounding/minimum checks remain. Legacy market fractions preserved. Example template scalar/optional-volatility bugs fixed; registry continues using example_kitchen_sink. Destin explicitly chose to KEEP the broker's separate <=$10 residual dust-to-flat rule. 292 focused offline checks pass; unrelated absorption display-test failure reproduced on HEAD. Scoped Ruff/mypy pass; five pre-existing indicator input typing mismatches remain outside that passing scope. Destin accepted the result and requested packaging; committed as `9c8496ed` on `feat/work`, with a clean source working tree. No DB/catalog mutation or push. See [[trading/backtest-strategies-index#Position helper migration — 2026-11-01]].

### Signed executable-order sizing — 2026-11-01

At Destin's request, moved `abs()` into `executable_order_size` and removed wrappers from all 18 strategy callers. Signed finite deltas now produce a positive executable magnitude or `None`; direction remains with callers. Added negative-input rounding/minimum coverage and retained nonfinite rejection. 115 focused offline tests and scoped Ruff pass. Local/uncommitted follow-up to `9c8496ed`. See [[trading/backtest-strategies-index#Position helper migration — 2026-11-01]].


### Backtest cap priority after rebalance selection — 2026-11-01

Destin approved target-selecting deadbands followed by final capping. Migrated all 16 callers; entry/reduction fractions also precede the cap. EWMAC/candle inventory reuse the quantity-cap helper; sizing formulas and explicit signal/transition gates remain. Over-cap deadband holds now request correction to the cap, subject to venue constraints. 406 focused offline checks pass; unrelated PX absorption test and five existing typing mismatches reproduced on HEAD. Scoped Ruff and 16-file strict mypy pass. Local/uncommitted, no live or DB operations. See [[trading/backtest-strategies-index#Rebalance selection before the cap — 2026-11-01]].


### Example-only over-cap bypass preview — 2026-11-01

Destin changed the desired policy: once over-cap, ignore the deadband and pursue the desired capped target. At his explicit scope request, implemented only in `example.py` for review; other callers/shared helpers retain the prior behavior. Exact-cap inventory still uses the deadband. Updated targeted expectations; 113 focused checks and Ruff pass. No broader migration, live operation, commit, or push. See [[trading/backtest-strategies-index#Example-only over-cap bypass preview — 2026-11-01]].


### Over-cap bypass rolled out — 2026-11-01

Destin accepted the Example preview, added `is_over_limit`, and authorized rollout. All 16 deadband callers now bypass to desired target when over-cap; EWMAC bypasses its buffer too. Four legacy callers also bypass partial-trade fractions. Final cap/delta/order checks and existing signal gates remain. 493 focused offline checks and Ruff pass; only the previously established display-test and five typing issues remain. Local/uncommitted, no live or DB operations. See [[trading/backtest-strategies-index#Over-cap bypass rolled out — 2026-11-01]].


### Backtest over-cap bypass committed — 2026-11-01

At Destin's request, committed the reviewed rollout as `3b6b4321` (`fix: bypass rebalance suppression for over-cap inventory`) on `feat/work`: 23 files, source working tree clean. Retained evidence: 493 focused passing checks, Ruff pass, known unrelated display-test and five existing typing issues. No push or live operation. Mixed KB edits remain uncommitted. See [[trading/backtest-strategies-index#Over-cap bypass rolled out — 2026-11-01]].

### Shared sizing stage and volatility-dependent cap — 2026-11-01

Destin chose visible stages with shared helpers and explicitly wants volatility dampening to reduce both the capital sizing base and hard cap. Added a typed shared sizing stage to both Example files and EWMAC; Carver sizing keeps its independent capital cap and rejects stacked dampening. Existing public settings remain; signal/transition gates and downstream execution rules remain. 433 focused offline checks, scoped Ruff/mypy, and diff checks pass. Local/uncommitted; no live or DB operations. Signal/rebalance helper convergence remains future work. See [[trading/backtest-strategies-index#Shared sizing stage and volatility-dependent cap — 2026-11-01]].

### Sizing policies paired with runtime inputs — 2026-11-01

Reworked the shared sizing stage from Destin's draft: a union ties each immutable policy to its required validated input model, with no optional sizing arguments. Both Example variants and EWMAC construct policies once at initialization. No dampening is 1.0; Carver inputs exclude dampening and preserve the existing unavailable-volatility fallback. Sizing/cap/rebalance behavior remains as in the preceding implementation. 442 focused offline checks, scoped Ruff and six-file mypy pass. Local/uncommitted; no live or DB operations. See [[trading/backtest-strategies-index#Shared sizing stage and volatility-dependent cap — 2026-11-01]].

### Runtime sizing inputs restored to TypedDict — 2026-11-01

At Destin's request, replaced per-candle Pydantic input models with required-field TypedDicts and replaced isinstance dispatch with policy.method literal branches. Immutable policies remain constructed once. Pairing/shape enforcement is static; runtime numeric checks remain. No dampening requires explicit 1.0. Existing sizing behavior passes 438 focused offline checks plus scoped Ruff/mypy. No performance benchmarks, live operations, commit, or push. Supersedes the prior runtime input-model validation choice. See [[trading/backtest-strategies-index#Shared sizing stage and volatility-dependent cap — 2026-11-01]].

### Literal-tagged sizing union — 2026-11-02

At Destin's request, added a top-level literal tag to the policy/input tuple union so branching narrows the entire request. Removed sizing casts; TypedDict inputs and once-initialized policies remain. All three callers updated. 438 focused offline checks and scoped Ruff/mypy pass; no behavior change or commit. See [[trading/backtest-strategies-index#Shared sizing stage and volatility-dependent cap — 2026-11-01]].

### Named sizing request fields — 2026-11-02

Replaced positional request tuples with literal-tagged named-tuple variants at Destin's request. Helper uses request.method, request.policy, and request.inputs; no numeric indexing or casts. TypedDict inputs and cached policies remain. 438 focused checks and scoped Ruff/mypy pass. Local/uncommitted. See [[trading/backtest-strategies-index#Shared sizing stage and volatility-dependent cap — 2026-11-01]].

### Shared signal mapping — 2026-11-02

EWMAC now uses signal_to_position with forecast scale 10. Renamed mapper base argument to base_size across standard/banded/skewed variants and all keyword callers; positional callers remain compatible. 469 focused offline checks, scoped Ruff and ten-file mypy pass. Local/uncommitted. Next convergence stage is rebalance selection. See [[trading/backtest-strategies-index#Shared signal mapping — 2026-11-02]].

### Shared rebalance buffer — 2026-11-02

Extracted EWMAC nearest-edge buffer into apply_rebalance_buffer; Example deadband and visible over-cap bypass remain. Preserved policy-method removal from user DTO cleanup; request variants retain specific Literal tags for narrowing. 407 focused checks and scoped Ruff/mypy pass. No new config selector, commit, or live operation. See [[trading/backtest-strategies-index#Shared rebalance buffer — 2026-11-02]].

### Configurable position-mapping divisor — 2026-11-02

Added positive/finite SIG_SCALAR to signal config (base 1, EWMAC 10) and wired all ten backtest continuous mapper callers. Destin explicitly chose to preserve EWMAC calibrated forecasts; adaptive ABSOLUTE processing and fixed forecast caps remain unchanged. 523 focused checks and scoped Ruff/mypy pass; legacy configs load with defaults. Local/uncommitted. Sizing/rebalance configuration wiring remains. See [[trading/backtest-strategies-index#Configurable position-mapping divisor — 2026-11-02]].

### Example-only configuration wiring preview — 2026-11-02

Destin narrowed selector wiring to unregistered example.py. Added configurable capital/volatility-target sizing and deadband/buffer selection, preserving old settings when selectors are omitted. Bounded per-stream annual-volatility state supports Carver sizing. Registered Example/EWMAC remain outside this rollout. 506 focused checks and scoped Ruff/mypy pass; local/uncommitted. Review template before wider migration. See [[trading/backtest-strategies-index#Example-only configuration wiring preview — 2026-11-02]].

### Single sizing-volatility call — 2026-11-02

Removed Example's redundant feature-stage volatility call; sizing owns the update and the template has no gate before sizing. Prior calls were timestamp-deduplicated but unnecessary. 261 focused pipeline tests and scoped Ruff/mypy pass, including one helper call per candle and rolling-history checks. Local/uncommitted.

### Caller-owned sizing-volatility update — 2026-11-02

Supersedes the preceding sizing-owned update decision: Destin requested the general strategy pattern with no timestamp checks. Example now updates annual volatility once at candle-callback entry, before features/trading gates; sizing only reads it. Initial window seeds once, later callbacks consume the latest close. Removed the timestamp map. 262 pipeline tests and scoped Ruff/mypy pass, including warmup/rolling parity and updates while the order stage holds. Local/uncommitted; selector rollout remains Example-template-only.

### Example helper extraction, first function — 2026-11-02

Destin is reducing strategy boilerplate with explicit helper inputs and requested incremental extraction. Moved select_rebalance_target into app/helpers/positions_v2.py; Example calls it with trade_config.REBALANCE and keeps the over-cap bypass visible. 129 existing position/sizing helper tests and scoped helper Ruff/mypy pass. Example remains mid-refactor: user moved annual-volatility updating into _features (still once before trading), passed the stream key, and returns its snapshot; the missing snapshot argument to _order_size, optional-snapshot typing, volatility-policy narrowing, and feature display emission remain to complete. No end-to-end passing claim for this intermediate state. Follow-up: extracted volatility_multiplier to app/lib/utils/vol_adj_position.py with explicit closes and CapitalSizingConfig inputs; Example calls it only in the capital branch. Updated affected test patch locations/calls; 14 targeted sizing/rebalance integration cases and helper Ruff/mypy pass. Annual-volatility state updating and sizing-request preparation remain in Example. Local/uncommitted.

### Feature-owned volatility observations — 2026-11-02

Destin rejected the extracted volatility_multiplier wrapper because volatility calculation belongs in strategy features. Removed that wrapper. Example _features now calculates VolScore from the capital policy spans (including when dampening is disabled, for display) or updates the annual-volatility estimator for volatility targeting. Capital warmup includes both score spans. It emits volatility_r_score or blended_annual_volatility alongside EMAs. Sizing consumes the already computed observation and applies vol_adj_position only when capital dampening is enabled; neither sizing nor order preparation accepts candle history. Lightweight literal-tagged CapitalSizingObservation/VolTargetSizingObservation tuples in dto/position.py pair configuration with its matching result without None, new casts, or runtime instance checks. Fixed the missing snapshot argument and policy narrowing; annual-volatility update receives the specific policy explicitly. Shared rebalance extraction remains. 510 focused pipeline/helper/Example/EWMAC tests and four-file Ruff/mypy pass; prior intermediate wiring errors are resolved. Local/uncommitted, selector rollout still limited to the Example template.

### Volatility estimator owns window initialization — 2026-11-02

Added advance(closes) and _initialize to BlendedCenteredEwmaVolatility, mirroring the stateful EMA window interface. Initialization checks _last_close is None, since one received close leaves return history empty. First call streams the seed window; later calls consume only the latest close and return a snapshot. Existing update(close) callers, including EWMAC, remain compatible. Example creates per-stream estimators in features and calls advance directly; removed _update_sizing_volatility. Preserved Destin's removal of volatility indicator emission and removed its unused display variables. No timestamp checks or added retained history. 363 estimator/pipeline/EWMAC tests and scoped Ruff/mypy pass, including single-close initialization, rolling-window parity, bounded history, and stream isolation. Local/uncommitted.

### Shared sizing preparation — 2026-11-02

Moved Example _calculate_sizing to app/helpers/positions_v2.py as calculate_sizing, taking sizing_capital, max_notional_usd, price, and the literal-tagged SizingObservation. It applies configured capital dampening or builds the volatility-target request, then delegates to existing calculate_position_sizing. Example retains account/capital lookups in its visible order pipeline; removed the private sizing method and unused request imports. Feature calculations and state remain strategy-owned. Existing pipeline/helper/Example/EWMAC checks: 510 pass; scoped Ruff/mypy and diff whitespace checks pass. Local/uncommitted.

### Position pipeline checkpoint committed — 2026-11-02

At Destin's explicit request, committed all 25 dirty mm_v04 pipeline files as b94f5080 (refactor: share configurable position sizing pipeline) on feat/work. Pre-commit verification: 565 focused tests pass, Ruff passes all changed Python files, and scoped mypy passes 12 files. No propagation beyond existing work and no push. Shared helper extraction and Example-template policy wiring are checkpointed for the next rollout. Earlier local/uncommitted labels above describe pre-checkpoint history.


### Cohesive volatility pipeline — 2026-11-03

Completed explicit Example targeting/adjustment sections and shared annualized-series scoring. CenteredEwmaVolatility now only estimates/retains volatility; blending lives in b_score, used by Example and EWMAC. Removed the old blended snapshot DTO/API. 401 focused tests pass; scoped mypy/Ruff pass; EWMAC snapshots exactly match the pre-refactor implementation across six speed sets × 3000 candles. See [[engineering/bounded-ema-history]]. Work remains uncommitted; no runtime operations.

RMS follow-up: optional annualization now lives in ewma_rms_returns; Example passes timeframe/override directly. Completed removal of EWMAC trailing-volatility snapshot field and corrected centered advance indentation. 411 focused tests and scoped checks pass.


### Volatility and sizing package committed — 2026-11-03

At Destin's request, committed the 25-file package as efd97d06 (refactor: unify volatility scoring and configurable backtest sizing) on feat/work. Includes Example volatility/scoring/sizing refactor, EWMAC shared blending, optional RMS annualization, and per-asset backtest risk-weight migration/API/UI. Verification: 512 focused backend tests and three frontend tests pass; TypeScript and production build pass; scoped source typing/lint and whitespace checks pass. Database migration remains unapplied. No push or live operations. This supersedes prior uncommitted status for these changes.


### Local risk-weight migration applied — 2026-11-03

At Destin's explicit request, applied d92e7a41c608 to the configured local PostgreSQL app database at localhost:5432, advancing from a47c9e21d603. Verified instrument_weight is double precision, NOT NULL, default 1, and Alembic is at the repository head. backteststrategyasset contained zero rows, so no existing rows needed backfilling. No application startup, trading operations, or remote database changes. This supersedes the earlier unapplied migration status.


### Separate Example registration — 2026-11-03

At Destin's request, the strategy package now imports/exports Example from example.py under Example* and registers it as example. Kitchen Sink remains implemented in example_kitchen_sink.py, registered/named/tagged example_kitchen_sink and exported as ExampleKitchenSink*. Its frontend-specific validation and trade controls now target that distinct name. Old saved JSON was not rewritten; comparison fixtures were updated to the Kitchen Sink identity. Removed the test-only registry override. Corrected latest user-edit fast_emac/slow_emac calls to the actual EMACState fast_ema/slow_ema accessors while preserving the _emac field rename. 349 targeted backend tests, three frontend tests, TypeScript, scoped Ruff/mypy, and diff checks pass. Changes uncommitted; no runtime/database changes. This supersedes earlier descriptions of Example as an unregistered template.

### Kitchen Sink sizing and volatility propagation — 2026-11-03

Implemented Destin's approved propagation of Example's independent volatility/sizing pipeline into Kitchen Sink, preserving its threshold/sizing branches and transition execution gate. New unlevered default, fixed cap, nested volatility roles and explicit rebalance configuration are intentional behavior/config changes; UI controls and test fixtures updated. 435 focused offline backend tests, eight frontend tests, production build and scoped typing/lint pass. Final tests use the normal working tree after Destin fixed the unrelated inventory syntax error. Local and uncommitted; no runtime/database operations. See [[engineering/bounded-ema-history#Kitchen Sink sizing and volatility propagation — 2026-11-03]].


### Backtest asset fetch recovery — 2026-11-04

Added frontend React Query loading for assets and volume metadata after Destin confirmed a reload restored missing data. Transient failures retry three times at 1/2/4 seconds; non-transient 4xx responses do not retry (408/429 do). Existing global auth handling now applies. The panel shows failure messages and a manual Retry button, preserves cached data, and can refetch on focus/reconnect. Nine focused tests and production build pass; new helper/test lint passes. Local/uncommitted. Backend metadata client timeout/websocket lifecycle issues identified during inspection remain unchanged; no runtime or database operations.


### EMAC signal EMA — 2026-11-04

Added configurable signal_period=9, signal_ema(), and latest_signal to EMACState; existing EMAC outputs stay unchanged. All three histories remain bounded and initial seeding consumes the full input. 94 focused offline tests plus scoped lint/type/whitespace checks pass. One separate stale emac_v2 test cannot collect due to its missing strategy module. Local/uncommitted; no runtime operations. See [[engineering/bounded-ema-history#EMAC signal EMA — 2026-11-04]].


### MACD histogram backtest strategy — 2026-11-04

Renamed the user's Example clone to MACDHist* and registered/exported macd_hist. Features process EMAC-minus-signal and emit histogram raw/processed signals plus MACD/signal indicators. Defaults are 10/200/9; signal_window is configurable and included in warmup. Cloned sizing remains unchanged. 95 focused offline tests and scoped typing/lint/whitespace checks pass. Local/uncommitted; no runtime operations. See [[engineering/bounded-ema-history#MACD histogram backtest strategy — 2026-11-04]].


### Live ExampleV1 EMAC migration — 2026-11-04

Replaced ExampleV1's deleted emac_signal dependency with per-asset/timeframe EMACState (capacity one plus last timestamp), preserving legacy RMS scaling and feature publication. 76 offline tests pass; lint/whitespace pass. Two pre-existing optional-client typing errors remain in unchanged order paths. Separate research/scratch deleted-helper imports remain. Local/uncommitted; no runtime operations. See [[engineering/bounded-ema-history#Live ExampleV1 EMAC migration — 2026-11-04]].


### Combo v1 backtest blend — 2026-11-04

Implemented Destin's VFTI(10), RVWAP slope(min bars 1/lookback 3), RSI(10), PX RVWAP(min bars 1), independently normalized with lookback 200 and blended at 25% each by default. Weights configurable; registered combo_v1 separately. 44 targeted offline tests plus scoped mypy/Ruff pass. Four unrelated MACD histogram tests expect removed indicator outputs. Local/uncommitted; no runtime operations. Exact TradingView parity remains unverified without the script. See [[engineering/bounded-ema-history#Combo v1 backtest feature blend — 2026-11-04]].


### Affine signal lookback fix — 2026-11-04

Fixed shared affine scaling to honor SIG_SCALE_LOOKBACK instead of hardcoded 252, discovered while inspecting saved run 828dc3d4-dda8-4b89-9192-3d5b90dc8f28. Array/scalar paths covered; 28 focused offline tests and lint/type/whitespace checks pass. Existing saved results unchanged; local/uncommitted. See [[engineering/bounded-ema-history#Affine signal lookback fix — 2026-11-04]].


### MACD log-price toggle — 2026-11-04

Added use_log_price=false to MACD strategy params; true logs the selected source before EMAs and masks nonpositive values. Existing histogram processing preserved; TradingView's separate double-normalization block is not part of this toggle. 80 focused offline tests and lint/type/whitespace checks pass. Local/uncommitted. See [[engineering/bounded-ema-history#MACD log-price toggle — 2026-11-04]].


### Optional MACD double normalization — 2026-11-04

Added normalize_macd_first=false in the strategy only. Enabled mode affine-normalizes MACD before a bounded stateful signal EMA, then processes its residual with existing config. Use AFFINE/100 plus use_log_price=true for the supplied pipeline order. Full chronological seeding, expanded warmup, intermediate indicators and flat-price roundoff guard included; 90 focused tests plus scoped lint/type/whitespace checks pass. Local/uncommitted. See [[engineering/bounded-ema-history#Optional MACD double normalization — 2026-11-04]].


### Combo warmup convention restored — 2026-11-04

At Destin’s request, replaced additive startup-plus-normalization warmup with the base Example max(requirements) + 1 convention. Default combo warmup is now 201 bars rather than 300; volatility requirements remain included. Updated the existing warmup regression assertions. See [[engineering/bounded-ema-history#Combo v1 backtest feature blend — 2026-11-04]].


### Backtest unrealized PnL panel — 2026-11-04

Added Unrealized PnL ($) as a toggleable, reorderable histogram in TradingViewChart using existing position_chart.upnl. Uses signed USD colors and existing panel preference migration; no backend changes. Production build, scoped lint, and seven existing chart/order tests pass. Browser verification outstanding. Local/uncommitted; no runtime operations.


## Signal transform helpers — 2026-11-04

Implemented standalone `tanh_clamp` and `exponential_damp` in `backend/app/lib/utils/signal_clamp.py`: exact tanh(x) and x*exp(-x²), scalar/float64-array support, finite-input validation and stable extreme finite inputs. No pipeline integration or runtime change. Supersedes the exploratory rational tail-damping formula in this chat. Ten focused offline tests and scoped Ruff/mypy pass. Local/uncommitted.


### MACD warmup and absolute forecast wiring — 2026-11-04

Implemented partial-history centered-targeting warmup for MACD and shared absolute scaling's configured target/span wiring. Absolute clipping follows twice SIG_SCALAR; existing absolute configurations change behavior. 158 tests pass, eight existing MACD indicator-expectation failures remain; scoped lint/types pass. Local/uncommitted, no runtime operations. See [[engineering/bounded-ema-history#MACD warmup and absolute forecast wiring — 2026-11-04]].


## Final signal transform integration — 2026-11-05

Integrated `SIG_TRANSFORM` (`none` default, `tanh`, `exponential`) into shared `StrategySignalConfig`, `process_signal`, and both `process_signal_last` paths. Destin selected the final order: scaling → polarity → buffering → transform → optional clipping. Exact formulas operate in existing signal units without rescaling; transforms see the full buffered magnitude before the output cap (absolute cap 2*SIG_SCALAR, otherwise 1). Existing configurations default to none. Dynamic registry schema exposes choices without generated-client changes. 121 targeted offline tests plus scoped Ruff/mypy and whitespace checks pass, including tight absolute caps and both scalar branches. No runtime operations or commits. Supersedes the standalone-only state above and the initial clip-before-transform implementation.


### Backtest compounding source — 2026-11-06

Implemented requested account-equity/booked-P&L compounding choice and absolute-scaling info popover. Existing equity default preserved; booked source includes realized fees, excludes open P&L. Strategy caps follow sizing capital; broker risk remains marked-equity based. 356 offline tests, 10 frontend config tests and build pass; unrelated EWMAC fixture/type/lint issues remain. Browser verification outstanding. See [[engineering/bounded-ema-history#Backtest compounding source and absolute-sizing note — 2026-11-06]]. Local/uncommitted.


### Compounding MCP verification — 2026-11-06

Verified paired Example runs through Research MCP after Destin started the manager. Equity `0aaac038-6670-4873-b77d-d8cd131776cd`; booked `5fa8950a-992d-4629-81d2-0429fb2ed901`. Same signals, sole config difference is source, all 2307 per-run order deltas match independently reconstructed targets/rounding/minimum. Equity reproduces original metrics; booked excludes open P&L as intended. See [[engineering/bounded-ema-history#Compounding source verified through Research MCP — 2026-11-06]].


### Sizing mandate working framework — 2026-11-06

Destin requested a synthesis in [sizing.md](../../raw/research/concepts/sizing.md): continuous equity-driven rebalancing, exposure-dependent feedback, booked-P&L limitations, and a PM/desk framework separating mandate, state, and action. Status remains in progress. Capital source and allocation-review timing are separate decisions; no replacement controller or review cadence selected. Existing compounding implementation is unchanged.
