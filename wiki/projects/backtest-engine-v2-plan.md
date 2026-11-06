# Backtest Engine V2 delivery draft

Status: in progress

Date: 2026-10-18

## Current status — 2026-10-18: core rewrite removed

Destin stopped the first-principles rewrite process and removed the core code himself. The separate core engine, accounting/ledger implementation and example_core strategy are no longer an active implementation or delivery path. Do not recreate them, resume their integration, or continue the previously listed next-open admission/metrics work without new direction from Destin.

The 2026-10-17/18 first-principles walkthroughs, implementation notes, file layouts and test results below are historical records of the removed attempt. They are superseded as descriptions of current code; their passing tests do not establish the health of the repository after removal. Next-bar-open and liquidation discussions are historical design decisions, not evidence that those behaviors are implemented in the remaining engine.

The broader V2 roadmap is retained for reference. No replacement approach or next implementation task has been selected. This update records the removal only; no code repairs, tests, ticket changes, commits or further implementation were performed.

### Standalone strategy restored

On 2026-10-18, at Destin’s request, restored standalone feature preparation, configuration, and validation inside `backend/app/backtest/strategies/example_vectorized.py`, removing imports of the deleted shared example modules. Preserved the fixed volatility window and existing strategy behavior. Updated the two affected test references. Verification: 35 vectorized-strategy tests pass; scoped Ruff and mypy pass. This verifies the strategy only, not overall repository health or manager integration. The core rewrite remains stopped; no commit or next implementation task selected.

Build V2 in the order Destin selected: **vectorization → multi-timeframe data → limit orders → cross margin**. Each stage should produce a usable capability and expose the requirements for the next. Define interfaces alongside those capabilities; do not require a complete account, allocation, persistence, and remote-compute architecture before improving the engine.

This is a proposed replacement plan for [Backtest Engine V2](https://linear.app/money-machine/project/backtest-engine-v2-8db3cb02c845). Destin authorized creating the replacement tickets on 2026-10-16. Linear now contains MON-228 → MON-229 and MON-234 → MON-230 → MON-231 → MON-232 → MON-233, with four ordered milestones matching this plan. MON-228 and MON-229 are completed locally; later tickets retain their dependencies and await selection. Stages 2–4 remain outlines for refinement with Destin. Historical ticket IDs below identify source material, not inherited prerequisites. MON-212 remains completed reference work and MON-223 remains separate in Triage.

## Delivery sequence

| Stage | Usable result | Question answered |
| --- | --- | --- |
| 1. Vectorize | A faster local backtest for the first migrated strategy, retaining independent accounts | Can we remove repeated computation without changing trading behavior? |
| 2. Multi-timeframe data | One strategy reads completed higher and lower timeframe data on its chosen decision schedule | What information is available at each decision? |
| 3. Limit orders | Resting orders fill partially or fully on a finer simulation clock | How do decisions, orders, fills, and account updates interact? |
| 4. Cross margin | Multiple assets share collateral under an explicit allocation policy | How should positions and outstanding orders share capital? |

Local execution comes first. Portfolio analytics, Modal, and live deployment are later options, not prerequisites for these four stages.

## Stage 1 Vectorize the existing backtest

Use the consolidated `example` strategy; the original emac_cross registration has been removed. Vectorize causal feature preparation and remove unnecessary per-bar object construction. Keep stateful position and execution processing sequential where its behavior requires it. “Vectorized” does not mean replacing order accounting with an array of returns.

### Ticket 1a Small load correctness baseline and profiling

[MON-228](https://linear.app/money-machine/issue/MON-228) remains Ready. Select one representative asset/configuration and a bounded range with sufficient warmup and meaningful transitions. Freeze corrected causal indicators, decisions, fills, fees, positions, cash/equity, and numeric tolerances. Profile concrete CPU/allocation hotspots. This small fixture is for inspectable correctness and diagnosis; large data preparation is not required to close it.

### Ticket 1b Large load performance baseline

[MON-234](https://linear.app/money-machine/issue/MON-234) follows MON-228. Measure independent-account throughput, stage timings, memory, and variance up to the agreed 96 assets × 50,000 bars upper bound using median-of-three warm-cache runs. Preserve the exact reference code/data/config/environment for later optimized comparisons. Smaller measured scales can diagnose scaling; do not extrapolate and claim the upper bound was measured.

MON-229 can proceed after MON-228 without waiting for MON-234. MON-230 requires both the vectorized path and the large reference benchmark. Small-load checks diagnose correctness; large-load checks primarily measure throughput and memory, with result consistency checks at scale.

### Ticket 2 Implement the first vectorized strategy path

**Outcome:** `example` prepares features efficiently and executes through a lean state loop.

**Work:** Introduce only the typed feature/decision interfaces needed for this strategy. Preserve canonical previous/current indicator values, warmup, signal timing, sizing, costs, and execution semantics. Avoid constructing unused events and full artifacts in summary mode. Retain an explicit existing-engine fallback for unsupported strategies.

**Acceptance:** Features agree with a continuous causal reference. Extending the input with future bars cannot change earlier features or decisions. Fills, position transitions, and metrics match the corrected baseline within the declared tolerances. State is bounded and isolated per run. Full retention still supplies the artifacts needed to diagnose differences.

**Depends on:** Ticket 1. **Reuse:** MON-189 and the feature/decision portion of MON-184.

### Ticket 3 Make the faster path usable and measure it

**Outcome:** The first migrated strategy can be selected through the existing research workflow, with reproducible saved results and measured performance.

**Work:** Add the smallest explicit engine selection and result provenance needed in the existing API/research path. Preserve authorization, cancellation, failure reporting, and saved-run readability. Compare the same independent-account workload on both engines using median-of-three warm-cache measurements. Separate engine speed from end-to-end time, and record memory and responsiveness.

**Acceptance:** A user or agent can run and inspect the migrated strategy without invoking an internal-only benchmark. Correctness comparisons pass. Preserve the original ≥10× engine-compute target as a measured goal; if it is missed, identify the remaining cost and bring Destin a concrete optimize-or-proceed decision. Do not silently lower the target or expand the project to meet it. The performance result does not depend on cross-margin support.

**Depends on:** Ticket 2. **Reuse:** MON-191 and the minimum access/provenance requirements from MON-190. Generalized account persistence remains later work.

## Stage 2 Add multi-timeframe data

Expand this into implementation tickets after the first stage reveals the actual feature and decision interfaces.

**Build:** Per-stream history and warmup; explicit native versus derived candles; completed-bar visibility; deterministic ordering when intervals close together; distinct data-update and strategy-decision schedules. Introduce only the scheduling machinery needed for these behaviors. Keep asset identity explicit without building shared allocation.

**Working example:** One asset makes hourly decisions using a completed daily 200-period moving average and a lower-timeframe feature. A new five-minute candle updates available data without automatically triggering another hourly decision. At a daily/hourly boundary, specify which completed inputs the hourly decision sees.

**Done when:** The example runs through the research workflow with inspectable timeframe/source metadata. Warmup, missing data, duplicate/conflicting bars, native/derived differences, and same-time boundaries are tested. Finer data never exposes a later candle to an earlier decision.

**Live compatibility:** Bring forward the read-only scheduling investigation from MON-204 while designing these semantics. Establish what current live code actually does with event timestamps, arrival order, late/missing candles, and decision triggers. Use this evidence to identify choices for Destin; do not assume either a global candle barrier or an arbitrary jitter window is the desired live policy. This investigation need not delay initial vectorization.

**Reuse:** MON-195 and MON-197, the relevant scheduling portion of MON-186, and the relevant live audit scope of MON-204. MON-196 supplies aggressor-volume fields if used by the example; otherwise introduce them with the limit-fill model in stage 3. Basic MTF support must not depend on a particular volume feature.

## Stage 3 Use finer data to simulate resting limit orders

**Build:** Order placement, activation, partial/full fill, cancellation, replacement, rejection, and terminal cleanup. Keep order identity and remaining quantity explicit. Process account updates on every simulated fill independently of the strategy’s decision schedule.

**Working example:** An hourly strategy places a resting order. Later five-minute bars partially fill it before the next hourly decision. The position, cash, fees, remaining order, and committed capacity update as those fills occur. Decide with Destin whether a fill also triggers strategy logic, such as a protective order, or whether that strategy waits for its next scheduled decision.

**Starting fill model to review:** Retain the original conservative proposal: later-bar trade-through, no touch-only fill, no fill from the bar used to place the order, and a configurable participation cap with 1% of opposite-aggressor volume as the proposed default. This is candle-level simulation; exact order-book timing and queue position remain outside its claims. Post-only behavior must have an explicit approximation or unsupported-state diagnostic when the data cannot establish it.

**Done when:** An inspectable ledger reconciles orders, partial fills, fees, positions, cash, and equity on a single-account example. Cancel/fill and replace/fill ordering are explicit. Pending commitments cannot silently spend the same available capacity twice. Saved results identify the fill assumptions, and participation sensitivity and finer-clock performance are measured.

**Reuse:** MON-198–200, MON-196 where needed, and fill/valuation timing from MON-186. Validate accounting under the chosen existing single-asset account mode; do not make this stage wait for the Hyperliquid multi-asset cross-margin model. Add only the persistence needed to save this working capability.

## Stage 4 Decide and implement shared cross margin

Begin with the functioning data, order, fill, and account behavior from the preceding stages. The first shared-account example remains one strategy trading several assets against one collateral pool.

**Decide before implementing allocation:**

- Does the strategy request new trades, absolute position targets, or a complete desired portfolio? An unchanged target must not create duplicate orders.
- Does new demand use spare capacity or resize existing positions? What happens to outstanding orders?
- Which requests compete together, and how are late or missing asset inputs handled?
- How do open orders reserve capacity, and how do partial fills, cancellations, and replacements release or consume it?
- What happens if an account update arrives between allocation and submission? Define revalidation and retry behavior.
- Are requests equal-priority, explicitly ranked, or governed by another strategy policy? Proportional allocation is a candidate, not an already-settled requirement.

**Build after those choices:** The shared account and margin model, the selected allocation policy, necessary multi-asset scheduling, and durable account-level results with per-asset attribution. Preserve the boundary between pure allocation calculations and execution. Batch decisions where the policy calls for batching; account updates continue on their own events.

**Done when:** Scenarios cover competing entries, existing positions, outstanding orders, partial fills, reductions, flips, insufficient margin, fees/funding, and account-level liquidation. Outcomes are independent of accidental processing order where the chosen policy requires simultaneous treatment. Shared-account behavior is checked against independently worked examples; independent V1 accounts are not an oracle for the new shared-capital economics.

**Reuse:** MON-187–188, the remaining multi-asset scope of MON-186, and MON-185/MON-190 for persistence and access. Incorporate the earlier live audit’s findings before fixing allocation interfaces. Live control still requires separate shadow evidence and explicit authorization.

## What happens to the original plan

| Existing material | Treatment in this draft |
| --- | --- |
| MON-183, MON-189, MON-191 | Form the first delivery stage |
| MON-184 universal contracts | Distribute interfaces into the stages that exercise them; no standalone universal-contract prerequisite |
| MON-185, MON-190 persistence and access | Minimal access/provenance in early stages; shared-account schema and results in stage 4 |
| MON-186 scheduler | MTF scheduling in stage 2, fill timing in stage 3, shared allocation scheduling in stage 4 |
| MON-195–197 MTF and volume | Stage 2, with aggressor-volume ingestion timed to its first actual use |
| MON-198–200 limits | Stage 3, starting with a single asset |
| MON-187–188 allocation and margin | Stage 4, after trading-policy decisions |
| MON-192–194 portfolio analytics | Retain for later; compact series may be pulled forward only if a current stage needs them |
| MON-201–203 Modal | Retain for later, after local performance and an actual remote-compute need |
| MON-204 live audit | Bring relevant read-only investigation into stage 2 and carry findings into stages 3–4 |
| MON-205–206 shadow and canary decision | Retain as separately authorized follow-up work |
| MON-212 indicator causality | Preserve completed work; verify it in the stage 1 baseline |
| MON-223 Databento | Separate scope; not a prerequisite for this sequence |

The [original architecture map](https://linear.app/money-machine/document/backtest-engine-v2-architecture-and-delivery-map-1679d5102cfd) and ticket descriptions remain reference material. Later stages should be refined from working examples with Destin before becoming detailed implementation queues. The replacement project overview and Linear delivery document reflect this sequence. Destin approved MON-228 and subsequently approved MON-229 as a separate example_vectorized.py strategy preserving example.py. Live runtime operations, deployment, and capital use remain outside scope.

## Immediate next step

MON-228 and MON-229 are complete locally. Review the new strategy; MON-234 remains the separate scale benchmark blocking MON-230. Neither MON-234 nor MON-230 has started.


## MON 228 small baseline results

Completed locally on 2026-10-16 using the actual current engine and mock trading service. Four new files supply the JSON fixture, typed harness, baseline tests, and profiling command. Application engine/strategy code is unchanged.

The fixture contains 1,024 synthetic hourly candles with oscillations and reversals. Seven cases exercise fixed/raw-zero/no thresholds, full/continuous/banded sizing, direct/inverse maps, transition/every-bar adjustment, and optional volatility. Six cases have 129 warmup bars; the volatility case has 201. All cross the 512-bar rolling-window boundary and trade both directions. This is selected branch coverage, not every configuration combination or market evidence.

### Verification and preserved semantics

- 22 new checks pass: exact fresh-run traces and metrics, exact prefix equivalence at 768 bars, summary/full-retention economic parity, continuous EMA recurrence across the rolling boundary, independently reconstructed fill P&L/fees/cash/size, and reported net P&L/fee reconciliation.
- 50 existing example, registry, and causal-state tests pass. Scoped Ruff and strict mypy pass. New-file whitespace checks are clean; the repository-wide diff check reports an unrelated pre-existing trailing space in indicator_lab.py.
- Numeric reconciliation uses absolute tolerance 1e-8 and relative tolerance 1e-10 where explicitly specified; fresh-run and prefix comparisons are exact. The independent ledger explicitly accounts for the existing simulator rule that snaps a reducing residual of at most $10 to flat and realizes it. This behavior was preserved, not changed.
- Frame traces retain features, processed signals, threshold state, emitted orders/fills, position size/entry/unrealized P&L, cash, and equity. They exclude random event identities and wall-clock timing. They do not invent internal target/omission diagnostics the strategy does not emit.

### Measurement and interpretation

Warm median-of-three local harness time ranges from approximately 205 to 331 ms per case; engine time ranges from 173 to 302 ms. Separate tracemalloc runs peak around 8.9–13.1 MiB of traced Python allocations; this is not whole-process RSS. Profiled times are diagnostic and are not used as throughput timings. Logging output is disabled, while event construction remains active. Network fetch, database saving, API latency, and process startup are outside these measurements.

The fixed/full transition case spends about 37% of profiled cumulative time in feature preparation; the ungated continuous case about 27%. Both construct four feature events per decision bar. The volatility case spends about 35% in instrument_vol_scores, repeatedly evaluating window-based calculations. Decision serialization, Pydantic validation, copied indicator arrays, and per-bar timestamp conversion also appear in the profiles. These are measured candidates for MON-229; percentages are nested and must not be added, and no speedup has yet been demonstrated.

### Artifacts and reproduction

Accepted artifact directory: `/Users/destinguarnieri/Desktop/codebase/mm_v04/.research/mon228-example-baseline-2026-10-16-final/`.

It contains a resolved manifest, seven trace JSON files, summary timing/allocation data, seven cProfile binaries and readable reports, and a verified 357-file source/lockfile snapshot in source.zip. The directory is local and git-ignored; no persisted backtest run_id or UI result is claimed. An earlier exploratory directory without the `-final` suffix is not the accepted baseline.

- Source digest: `b792fd2b7e19ef3635f55c1567fcb7d356ab23fa7ece18640ea00b6ca0b1082a`.
- Fixture digest: `1418cd4db143ea8b8b0bc4e224df54acafeadb46515e5f0ca128d0312ed5335c`.
- Candle digest: `43b092979fe731f9522fae0a033acc0d78c643c30850060cc5f7322ca728a3e5`.

From `mm_v04/backend`:

```bash
.venv/bin/python -m pytest --confcutdir=tests/backtest tests/backtest/test_example_baseline.py -q
.venv/bin/python scripts/profile_example_backtest.py --output ../.research/mon228-example-new-comparison
```

Use a new output directory; the command refuses to overwrite a frozen baseline. The harness imports application settings with dotenv reads disabled and explicit dummy values. The pytest confcutdir excludes the application-starting root conftest. No application startup, local credential read, live mutation, commit, push, or deployment was performed.


### 10,000-bar scaling follow-up — 2026-10-16

At Destin’s request, reran all seven configurations at 1,024 and 10,000 bars in the same session, each with one warmup run and three unprofiled timed trials. Same source digest as the accepted baseline; no engine changes. All 42 measured trials completed with exactly input bars minus strategy warmup decisions. Local total medians at 10,000 bars span 2.63–4.37 seconds, versus 0.201–0.331 seconds at 1,024. Runtime ratios span 12.14–13.20 for 9.77 times the input bars. After accounting for warmup, there are 11.03–11.91 times as many decisions, and time per decision rises about 10–18%. These two sizes show modest overhead growth beyond decision count, not an established asymptotic complexity law. This remains a single-asset synthetic timing experiment, not MON-234’s multiasset workload or a new correctness oracle.

Evidence and reusable runner: `/Users/destinguarnieri/Desktop/codebase/mm_v04/.research/mon228-example-scaling-10000-2026-10-16/` contains run.py, source.zip, per-size resolved provenance, and all trial timings/outcomes in summary.json. Fetch, database/API, startup, explicit between-trial garbage collection, and diagnostic profiling are excluded from timed calls.


## MON 229 first prepared strategy — 2026-10-16

The implementation details below describe the first revision; the standalone revision at the end supersedes inheritance and EMA/index handling. Timing evidence remains tied to this first revision.

Implemented Destin’s approved nondestructive variant as `backend/app/backtest/strategies/example_vectorized.py`, registered as `example_vectorized`. `example.py` is byte-for-byte identical to its frozen MON-228 source. The subclass reuses configuration, threshold/sizing/order logic and the existing mock broker. It owns a small typed feature container and upfront preparation in the same file; no separate feature-interface package was introduced. A default no-op `prepare_backtest` hook on the backtest-only base class is called once inside engine timing. Existing strategies retain their incremental execution path.

The prepared path supports min/max scaling with no active buffering, including all seven baseline configurations. Other scaling/buffering modes and nonfinite inputs take the explicit reference fallback (`fallback_reason`). Supported-path errors are not swallowed. EMA initialization and scalar recurrence arithmetic are preserved exactly; trailing scaling is calculated once over the arrays. Volatility still evaluates original capped windows but computes only the consumed r_score. This is a first prepared path, not an assertion that every calculation is vectorized. Summary mode omits indicator/signal events; full mode retains them. Execution, risk observation, liquidation, and aggregation continue through the existing engine/broker.

Feature storage is five float64 arrays and one int64 timestamp array (48 bytes per input bar, excluding temporary arrays and engine outputs). Arrays are read-only and per instance. Mutable threshold state is bounded for this single-asset execution; reused prepared instances are rejected. Existing engine output retention remains proportional to bars. No cross-run cache or bars-by-window matrix is introduced.

### Verification and measured result

- 128 targeted tests pass, including 21 new prepared-path checks, the baseline suite, original example/registry/causal-state tests, liquidation and risk tests. Seven full traces match exactly at 1,024 bars; all seven economic traces and metrics also match exactly at 10,000 bars. Prefix/future-extension checks, summary/full equality, fallback scaling, flat prices, forced liquidation, read-only arrays, and isolation are covered. Scoped Ruff and strict mypy pass; changed tracked application files pass whitespace checks.
- Same-session median-of-three unprofiled comparisons include preparation. At 10,000 bars: baseline 2.65–4.39 seconds, prepared 1.21–1.71 seconds; individual speedups 1.82–2.72 times. At 1,024 bars individual speedups are approximately 1.82–2.78 times. Fetch, database/API, startup, and explicit between-trial collection are excluded. Timing trials were separate from tests and diagnostic instrumentation.
- Separate 1,024-bar profiling shows traced Python allocation peaks fall from 8.91–13.09 MiB to 5.76–9.73 MiB, depending on configuration. This is not process RSS. Profiles still include broker, observability, per-bar result construction, and aggregation as remaining work.

### Evidence and reproduction

Artifacts: `/Users/destinguarnieri/Desktop/codebase/mm_v04/.research/mon229-vectorized-2026-10-16/` contains comparison runner, per-case/per-size trials, resolved provenance, verified source snapshot, separate CPU/allocation diagnostics, and a copy of the new parity tests. Source digest: `59aa9fd5b0a5bb46e4926ff472c3641d710ff171ff58a967474c3b741ac2714d`. The measured application/profiler/harness snapshot was verified against current files. Original MON-228 artifacts remain unchanged.

The profiling CLI now accepts `--vectorized` and `--bars 10000`, e.g. from backend: `.venv/bin/python scripts/profile_example_backtest.py --vectorized --bars 10000 --output ../.research/new-unique-output`. It refuses to overwrite an existing output directory. Offline tests retain the dummy-settings/dotenv-disabled harness and confcutdir isolation. Changes are local and uncommitted; no app startup, database persistence, live mutation, deployment, or push was performed.


## MON 229 standalone revision — 2026-10-16

Destin requested removal of inheritance from ExampleStrategy, direct bar indexing, and a single-call EMA. Implemented these changes: `ExampleVectorizedStrategy` now derives directly from `BacktestStrategy`, owns its local configuration models and decision/fallback methods, and imports no code from `example.py`. Duplication is intentional while the original is retained as an independent comparison. The engine passes its existing loop index through a default no-op `set_backtest_bar_index` hook. Prepared feature access validates the timestamp at that index and performs no searchsorted. Each fast/slow EMA is now one `EMA_P_CLEAN` call over the supplied source array; the extra scalar recurrence wrapper is removed.

All seven fixtures retain exact orders/fills/accounting/metrics at 1,024 and 10,000 bars. Feature floats are no longer bitwise identical: the observed maximum difference at 1,024 bars is 1.8474111129762605e-13, within the previously declared atol=1e-8, rtol=1e-10. Feature tests now use those tolerances only for feature values; economic frame fields and execution traces remain exact. Prefix checks stay exact within the new path. 163 targeted tests pass (including multi-speed EWMAC tests), scoped Ruff/strict mypy pass, and a fresh standalone-ownership/direct-index check passes. Original example.py and multi_speed_ewmac.py were not changed. New source/provenance/verification snapshot: `.research/mon229-standalone-2026-10-16/`. Performance was not rebenchmarked for this revision; previous timings describe the prior snapshot.

Volatility semantics remain unchanged while Destin considers the intended behavior. The relevant distinction is finite trailing statistics versus restarting recursive filters. Example min/max scaling uses a genuine finite lookback over continuously calculated EMA values. Example volatility recomputes the return-volatility EMA and its r_score EMA from each capped price slice; sliding the slice discards the prior seed/history. Multi-speed EWMAC instead keeps return mean/second moment and previous close across bars, initializes from the first available history, then updates once per new timestamp. Its separate bounded history (default 2,560 samples) supplies a trailing mean of annualized volatility, blended 70% current/30% trailing. It uses simple returns; the example uses log returns. Centered versus RMS volatility is independent of this state/window distinction. A continuous RMS implementation is possible but has not been selected or implemented here.


### Prepared-only cleanup — 2026-10-16

At Destin’s request, removed all `_reference_*` duplicates, the incremental EMA/signal-history state and its helper, and fallback dispatch from example_vectorized.py. This supersedes the earlier fallback description. Unsupported scaling, active buffering, and nonfinite source/close input now raise explicit errors directing callers to the separately registered example strategy. Unprepared execution raises a clear error. Volatility semantics and example.py remain unchanged. The scoped prepared-strategy suite passes all 31 tests, including seven-case exact economics at 1K/10K, feature tolerances, prefix/retention parity, liquidation, and rejection tests; scoped Ruff/mypy pass. No new timing measurement.


### Deferred feature output — 2026-10-16

Destin reorganized example_vectorized.py and requested removing feature-event work from the bar loop now. Preserved his method ordering and section marker. Removed `_retain_features` and the retention argument from preparation. `_features` now only validates the engine index and returns the prepared signal pair. Both full and summary per-bar results contain no indicator/signal messages. A once-per-full-run array handoff exposes the existing arrays; the engine serializes legacy chart/save records after execution through `helpers/backtest_features.py`. Shared params/hash/version metadata are calculated once. Summary does not invoke this serializer. This moves row materialization to the output boundary; existing row-oriented API/persistence schemas still require rows there.

The existing decision UUID is retained on the internal StrategyResult (no new per-bar wrapper object) so final signals retain their order association. Pre-decision liquidation bars have no feature rows, and later precomputed values are never exported. Full public feature values, persistence metadata, and decision links are checked against the baseline, alongside exact economics and existing prefix/risk/retention tests. All 140 targeted tests pass; scoped Ruff and mypy pass for five files. Original example and volatility semantics are unchanged. The profiling trace writer now records deferred full-output features separately from per-bar economic frames.

Evidence snapshot: `.research/mon229-deferred-features-2026-10-16/` (source, provenance, tests, verification). No new performance benchmark, database operation, or live startup was performed.


### Volatility helper extraction and visual comparison — 2026-10-16

Approved scope implemented locally: extracted bounded centered-return EWMA and 70/30 trailing blend into `backend/app/lib/utils/ewmac_volatility.py`; multi_speed_ewmac consumes it. `vol_adj_position` now accepts either the legacy score dictionary or a scalar r_score; example_vectorized uses the shared helper without a per-bar dictionary. Defaults and capped-window semantics remain unchanged. 112 targeted tests and scoped Ruff/mypy pass; all EWMAC snapshot fields exactly match the prior committed implementation across 3,000 deterministic bars.

Executed notebook `backend/notebooks/volatility_comparison.ipynb` contains seven inspected figures on four synthetic hourly paths, separating cap reset, centering, return definition, blend, and relative versus absolute risk sizing. HTML preview is `.research/volatility-comparison/volatility_comparison.html`. Span35/cap512 history differences are negligible on these fixtures; centering and blending are visible. Perfectly constant returns expose tiny positive floating-point centered-variance residuals, yielding spurious relative-score variation and huge unconstrained risk-target notionals. This boundary is documented, not changed. Next action: Destin reviews the plots and selects volatility/sizing semantics; no default decision or performance claim. Latest work remains uncommitted; the earlier cleanup was committed in five groups.


### Fixed-window volatility selected and implemented — 2026-10-17

Destin selected restart/history-independent volatility. Defaults are span35, explicit `volatility_window=512` prices, and EWMAC `long_volatility_window=2560` complete estimates. The long window remains configurable shorthand for a long history, not ten calendar years on intraday bars. EWMAC now resets return moments within each fixed window and excludes incomplete estimates from its 70/30 blend. Required prices are W+L-1 (3071 by default); no trading on a partial blend. Engine warmup index is required prices minus one, also respecting price-EMA warmup. Signal version bumped to 2.

Example_vectorized prepares its log-RMS/r_score within its own explicit window, independently of BT_WINDOW_CAP, and waits for complete price history. Original example.py is unchanged. Existing volatility-enabled baseline comparisons now align the reference start in test code: earlier-start economics are intentionally no longer the contract. Price EMAs remain continuous; full forecast/trade restart equivalence is not claimed.

Validation: 117 targeted tests pass; scoped Ruff and mypy on six source/test files pass. Exact volatility equality verified for 10000 versus trailing3071 price inputs, restart continuation, batch/incremental strategy processing, and engine-cap independence. Readiness boundaries and configurable windows are tested. Expanded mypy on the pre-existing multi-speed test file still reports its existing SimpleNamespace/CandleCtx and sizing-mode fixture typing issues. Notebook was rerun after separating its continuous reference from the newly fixed-window production helper. No performance benchmark or live operation. Work remains local/uncommitted.


### Volatility checkpoint committed — 2026-10-17

Committed implementation, helper tests, and executed comparison notebook in mm_v04 as `4d816761` (`feat/backtestv2`); code working tree clean, not pushed. Existing verification remains 117 targeted tests plus scoped lint/type checks. Linear checked: MON-228 and MON-229 Done; MON-234 and MON-230 Backlog, with MON-234 blocking MON-230. MON-231 → MON-232 → MON-233 remain later stages. Next proposed work is the separate large-load baseline; latest volatility revision has not been performance-benchmarked. No ticket state changes made.


### MON-234 maximum-load reference baseline — 2026-10-17

Completed and marked Done in Linear. Destin requested going directly to the maximum workload, so no scaling sweep was run. Offline synthetic independent-account reference: 96 distinct generated instruments × 50,000 hourly prices, four workers, summary retention, original example fixed/full transition settings with volatility adjustment disabled. One warmup and three full measured passes completed; all 384 runs have the expected decision count and identical per-asset economics across repeats. Input checksums verified. The median is about 5m35s; source of truth for timings, variance, per-worker memory high-waters, overlapping worker-stage totals and exact configuration is `.research/mon234-max-reference-2026-10-17/summary.json` plus manifest/verification/diagnostic artifacts. Source and all inputs are frozen there; original example matches MON-228, with the shared engine frozen at the current version.

Scope excludes real-market fetch, DB persistence, API responsiveness, cross margin and optimized-path speedup. The separate profile is diagnostic and excluded from throughput measurements. Runner `backend/scripts/benchmark_example_scale.py` passes scoped Ruff/mypy and remains uncommitted. Its only postmeasurement change is a local type annotation, documented against the frozen runner. Destin’s comment in example_vectorized.py was preserved. No app startup, live operation, commit or push.

Next selected-ticket boundary is MON-230 (not started): make/verify research-workflow access and compare the optimized path against the same frozen workload. Preserve the original measured speed target and bring an optimize-or-proceed decision if missed; do not silently add work. MON-231/232/233 remain later stages.


## 2026-10-17 — MON-230 workflow checks; large benchmark deferred

Created MON-235 for remaining backtest latency/allocation work. Existing strategy registry, picker and summary worker already support `example_vectorized`; expanded discovery/worker coverage and repaired the saved-read test's missing request/response arguments. 92 workflow tests pass, with vectorized parity passing separately. No production interface changes or actual API/DB run. Extended `backend/scripts/benchmark_example_scale.py` with verified frozen-reference input reuse and exact economic comparison; preserve MON-234 unchanged.

Destin questioned repeating expensive measurements before finishing improvements. Stopped the optimized run during warmup; `.research/mon230-max-vectorized-2026-10-17/interrupted.json` records partial parity and zero completed measured passes. No speedup conclusion. Use small targeted profiles during optimization; defer maximum-load median-of-three until ready. MON-230 remains In Progress and ≥10× remains an unmet measurement goal. Existing cancellation stops the waiter, not already-running process work; recorded for MON-235. No commit, push, startup, live/account mutation, or deployment.


## 2026-10-17 — Independent V2 engine boundary implemented

Destin approved separating engine work after a code/trace/object-lifetime review. `backend/app/services/backtest/bt_engine_v2.py` now owns execution, aggregation and response construction. `bt_engine.py` is byte-identical to the reference at commit `77e07fa4`; snapshot and verification live in `.research/mon230-engine-separation-2026-10-17/`. A small dispatcher routes `example_vectorized` to V2 and other strategies to V1 in both direct asset execution and the summary worker. No separate API engine picker or persistence migration was added. Strategy name alone is not historical engine-version provenance: earlier vectorized runs used V1; offline manifests now explicitly label the engine and freeze sources.

V2 uses a typed aggregation record and smaller functions; its execution does not delegate to V1. It still shares the broker, strategy hooks, metrics/output helpers, and V1 result containers. Further changes to those dependencies need their own isolation/parity review to keep V1 a useful reference. This is a separation, not a speedup result.

Footprint remains O(N): full prepared arrays, per-bar StrategyResults and broker account/position histories survive through aggregation, including summary mode. The small 1,024-bar investigation found 895 decisions and 1,790 retained account snapshots; disabled logging still encodes decision JSON. Those are MON-235 candidates, not optimizations shipped here. Preserve current execution semantics: risk marks at candle close while new-entry account snapshots use fill prices; non-finite account equity falls back to previous equity pending a separate policy decision.

Verification: 75 targeted tests pass (all seven same-strategy configurations, full/summary outputs, causal prefixes/changed future, independent accounting identities, liquidation, error cleanup, input validation and both workflow entry points). Fixed stale equity fixtures missing request assets. Scoped Ruff passes; mypy passes eight files with third-party missing-stub diagnostics disabled because pandas-stubs is absent. Profiling scripts now run V2 for optimized mode; no large benchmark was run. MON-230 remains In Progress; maximum comparison stays deferred. Next: choose a bounded MON-235 hotspot and optimize inside the V2 boundary. Work is uncommitted; no live/API/DB operations, startup, deployment or push.


## 2026-10-17 — V2 output/retention naming cleanup

Approved bounded follow-up: V2 passes `retention_mode` through aggregation instead of derived `include_artifacts` flags. Builders are now `_build_run_summary`, `_build_detailed_api_response`, and `_build_persistence_records`; summary-only output returns explicitly before full-detail/record construction. Legacy BacktestEngineResult fields remain at the caller compatibility boundary. No API/schema or persistence behavior changed. Per-bar construction, broker histories, execution traces and eager full output remain unchanged. 75 targeted tests and scoped Ruff/mypy pass (missing pandas stubs excluded); V1 remains byte-identical. Evidence: `.research/mon230-engine-separation-2026-10-17/output-cleanup-verification.json`. Destin permits a V2 broker when needed for the next state/snapshot separation. No benchmark, commit, push, startup or live operations.


## 2026-10-17 — Optional V2 execution diagnostics

V2 execution diagnostics are now opt-in: extracted transition collection and trace construction to execution_diagnostics.py; ordinary full/summary V2 runs skip both, comparison harnesses explicitly enable capture_execution_trace. Summary worker accepts absent traces unless requested. V1 unchanged. 77 targeted tests pass, including fail-if-called diagnostics checks and unchanged economic/output comparisons; scoped Ruff/mypy pass (missing third-party stubs excluded). Evidence: .research/mon230-engine-separation-2026-10-17/trace-opt-in-verification.json. General per-bar/broker retention remains unchanged. Maximum benchmark remains deferred; no commit or live operations.

## 2026-10-17 — First-principles checkpoint 1: minimum simulation

Status: draft. Destin selected a first-principles rewrite; API and persistence shapes may change or be replaced. This supersedes the immediate plan to refactor snapshots out of the existing broker. V1 is evidence, not the architecture or an unquestionable behavioral specification. Rust is a design thought experiment, not an approved language migration. This checkpoint investigates and proposes behavior; no engine implementation changed.

### Scope and required inputs

First slice: one linear, quote-settled instrument, one account, signed net inventory, market execution and prepared strategy features. This matches the current accounting form; it is not a universal model for spot, inverse contracts, or options. Inputs are timestamped market observations, strategy configuration/features, instrument quantity/price constraints, initial collateral, fees, slippage and an explicit execution/liquidation policy. Funding and cash transfers require explicit events if introduced; neither is silently modeled here. MTF, resting orders and shared cross margin remain later stages.

### State inventory

| Item | Why it survives to the next event |
|---|---|
| Cash/collateral balance | Accumulates realized gross P&L less fees; opening notional is not a cash purchase in this model |
| Signed position quantity | Determines exposure and how much an opposing fill closes |
| Average entry basis | Determines realized and unrealized P&L; reset when flat |
| Current observation/time and run terminal status | Defines valuation and ordering; prevents decisions after terminal liquidation |
| Strategy-owned state | Threshold/hysteresis/sizing logic may depend on previous decisions; not broker accounting state |
| Metric accumulators or necessary numerical series | Only what each selected metric needs; inventory alone cannot reconstruct historical risk |

Equity = cash + quantity × (market mark − entry basis). Notional, unrealized P&L, margin usage and ROE are derived, not independent sources of truth. Caching may later be justified by measured reuse, with an explicit invalidation rule. Instrument rules and execution policy are configuration. Event IDs, account addresses, nested venue response models and position-history objects are not required to apply this accounting. Outstanding-order state becomes necessary with resting orders, not in this immediate-fill slice. Input/prepared arrays and metric storage are separate from bounded execution state.

### One execution sequence (proposed, not yet implemented)

1. Make the current market observation available; retain the distinction between carried inventory and inventory opened at this decision.
2. Observe carried-inventory risk over the completed bar if that metric is requested. OHLC extremes supply a bound, not an observed intrabar event order.
3. Value current inventory at the market mark; apply the explicit liquidation rule before another strategy decision. A terminal event suppresses that decision.
4. Evaluate the strategy using available data and current state; produce an instruction. Separate strategy intent from fill application. The present strategy executes the broker directly.
5. Validate/quantize the instruction under instrument and exposure rules; execute it under the selected price/timing assumption. Invalid instructions need explicit rejection/error behavior.
6. Apply the fill: realize only the opposing quantity; deduct the fee once; update quantity and entry basis. Increasing uses a weighted basis, reducing preserves it, a reversal closes the prior side and opens the remainder at fill price, flat resets it.
7. Value the resulting inventory at the same external market mark, not the fill price. Observe post-fill risk and update selected metrics; append detail only if requested. Multiple fills at one timestamp retain their sequence and intermediate risk observations.

For now, same-close execution is an explicit simulation assumption to review, not a claim of live attainability. The future event scheduler must distinguish data availability, decision, submission and fill times. No global all-assets candle barrier is assumed by this state model.

### Independent worked ledger

Illustrative inputs: starting cash 1000; fee 0.1% of executed notional; adverse slippage 0.1%; no funding. These are test assumptions, not venue facts. Prices and quantities are deliberately simple and valid. Fees below are positive expenses, unlike V1's negative fee field.

| Event | Market mark | Fill | Cash after | Quantity | Entry basis | Equity at market mark |
|---|---:|---|---:|---:|---:|---:|
| Entry | 100 | Buy 2 at 100.10 | 999.79980 | 2 | 100.10 | 999.59980 |
| Hold | 110 | None | 999.79980 | 2 | 100.10 | 1019.59980 |
| Partial exit | 110 | Sell 1 at 109.89 | 1009.47991 | 1 | 100.10 | 1019.37991 |
| Close | 120 | Sell 1 at 119.88 | 1029.14003 | 0 | 0 | 1029.14003 |

Checked with Python Decimal arithmetic and asserted at each fill: equity_after − equity_before = signed_fill_quantity × (market_mark − fill_price) − fee, with the market mark held constant. Partial-exit gross P&L is 9.79; final-exit gross P&L is 19.78. Slippage is embedded in prices; reporting it separately must not deduct it again. This is a numerical oracle, not a test of the existing engine. Add/increase, short-side symmetry, reversals and quantity conservation join the implementation acceptance cases.

### Existing behaviors that must earn approval

- **Fill versus market valuation:** `mock_services.py:968` onward replaces position state using fill price; `bt_engine_v2.py:64` skips post-fill marking when fills exist. Thus the old account series can temporarily disagree with market-marked risk. Proposed: use market-marked post-fill equity consistently; an intentional V1 difference.
- **Liquidation:** `mock_services.py:238` computes a fee/slippage-adjusted zero-equity exit boundary. `:731` checks only the supplied close mark, then `:283` executes at the boundary, and `:270` clamps final cash nonnegative. This is not an implemented venue maintenance-margin model. Example with no costs: cash 100, short 2 at 100 has boundary 150. A close at 160 triggers a simulated fill at 150 and zero balance; exiting at 160 would leave −20. Need an explicit decision on boundary/trigger/fill/gap/deficit treatment before implementing liquidation. Do not silently pick a venue model.
- **Dust conservation:** `mock_services.py:389` snaps an opposing residual worth at most the minimum notional to flat; `:412` can then realize the whole prior quantity although the recorded fill quantity is smaller. Proposed: do not erase inventory; either fill the permitted actual close quantity or retain the remainder. Verify both quantity and cash conservation.
- **Invalid data:** V1 can substitute prior equity (`bt_engine_v2.py:219`) or turn invalid size/price into an empty execution (`mock_services.py:846`). Proposed: malformed market/accounting data fails explicitly; valid but non-executable instructions have an explicit no-fill/rejection outcome.
- **Close timing:** `example_vectorized.py:371` sizes and immediately executes at the same close used by the signal. Keep timing a named assumption; next-observation execution changes economics and is a separate user decision.

Current risk measurement (`risk_measurement.py`) observes carried OHLC bounds and post-fill inventory independently of broker snapshots. Preserve that distinction; do not turn the favorable/adverse bound ordering into an execution path.

### Next checkpoint

Sketch the minimal core and one iteration using this ledger; resolve valuation, dust, invalid-input and liquidation/timing choices before implementing affected behavior. API, saved-run schema and consumers are redesignable; inventory their actual needs at checkpoint 4 instead of carrying their models into the core. Verification combines independent arithmetic, state invariants, causality and explained V1 differences. Full/summary/diagnostic recording must not affect the trading state trajectory. No maximum benchmark yet.

## 2026-10-17 — First-principles checkpoint 2: core sketch

Status: draft. Destin accepted checkpoint 1 and requested proceeding. This is a design sketch, not implemented code or a Rust migration. Liquidation and fill timing are still explicit policy choices, not inferred approvals.

### The smallest useful separation

- **Strategy decides:** reads prepared features by index and current quantity/equity; returns an instruction. It cannot mutate the ledger or call the execution service.
- **Execution determines the fill:** applies instrument rules, the selected timing assumption and execution costs. A desired adjustment is not an executed fill.
- **Accounting applies the fill:** owns cash, signed quantity and entry basis; knows nothing about candles, strategies, API schemas or recording modes.
- **Runner orders these operations:** owns time/index and stop status. Market observations supply the valuation price.
- **Recording observes:** updates metric accumulators and optional numerical histories. It never determines the accounting state.

These are responsibilities, not five classes, services, interfaces or files. Start with ordinary functions and one ledger allocated per run. No event bus, plugin registry, inheritance tree or universal broker interface is justified yet.

### Candidate state and operations

```python
# Illustrative Python, not a committed public interface.
@dataclass(slots=True)
class Ledger:
    cash: float
    quantity: float = 0.0
    entry_price: float = 0.0

def equity(ledger: Ledger, mark: float) -> float: ...
def apply_fill(ledger: Ledger, signed_quantity: float,
               fill_price: float, fee_paid: float) -> float: ...
# Mutates ledger only after validating inputs/calculating the result.
# Returns gross realized P&L for metric collection; fee_paid is a positive expense.
```

No separate equity/UPnL/notional fields to keep synchronized. No history inside Ledger. Integer quantity lots are a candidate for exact quantity conservation when the instrument has a fixed lot step; choose the representation after inspecting current instrument metadata/rounding semantics. Floats above express the mathematics, not a settled precision policy. Decimal remains an independent test oracle, not a proposed hot-loop requirement.

`apply_fill` does not accept a market mark: the fill determines cash and basis; the market mark determines valuation. It must work equally for an ordinary execution or a forced close. Precompute and validate the resulting state before mutation so invalid arithmetic cannot partially update cash and inventory.

The first strategy instruction can be `signed_adjustment: float | None`: positive buys, negative sells, None means no order. The strategy keeps its existing target/threshold/volatility reasoning and produces this adjustment; the executor validates it. The runner passes existing scalars/index, not a newly constructed CandleCtx or DecisionContext. This deliberately covers only the first market-order slice. Resting orders later need price, duration, cancellation and order identity; do not cram those into a scalar or prebuild an order framework today.

### One iteration

```text
read timestamp and market mark from existing arrays at index i
observe the bar's carried-inventory risk, if requested
calculate pre-decision equity directly from ledger and mark
check the selected liquidation rule
    if triggered: resolve forced fill, apply it, observe it, terminate
otherwise:
    adjustment = strategy.decide(i, quantity, pre-decision equity, mark)
    if adjustment exists:
        validate quantity/instrument/exposure constraints
        resolve fill price and fee under the selected execution assumption
        gross_realized = apply_fill(ledger, actual_quantity, fill_price, fee)
        observe fill metrics and post-fill risk using the external mark
        append a fill record only if requested
calculate final equity at the external mark
update selected bar metrics; optionally store a numerical equity sample
```

Liquidation resolution is intentionally named rather than implemented with V1's zero-equity boundary. Same-close execution can make the first slice synchronous; delayed execution requires pending instruction state and event scheduling. Neither option alters the fill-accounting operation. A terminal branch still records final state once and never calls the strategy. Warmup, input validity and feature causality remain runner/input responsibilities, not ledger fields.

### Example: partial exit

Before the fill: cash 999.79980, quantity 2, basis 100.10, market 110. Strategy requests sell 1; execution supplies signed quantity −1, fill 109.89 and fee 0.10989. Accounting realizes 9.79 and changes cash to 1009.47991; quantity becomes 1 and basis remains 100.10. Market valuation gives equity 1019.37991. No account/position response is constructed to obtain any of those values. If detail is requested, the recorder copies the numerical values, not a reference to the mutable ledger.

### Work and memory per iteration

Persistent: one ledger, strategy state, run cursor/status, configuration, metric state and requested output buffers. Input/prepared-feature arrays retain their own lifetime. Most scalar calculations are transient. A no-order bar does not need an order, fill, account, position, StrategyResult or window-dictionary allocation. Python arithmetic still creates scalar objects; this is not a zero-allocation claim.

Fill records exist only for actual fills when selected; bar series can be preallocated numeric columns. Summary may still require numerical series for certain metrics—no O(1) total-memory claim before the metric inventory. Full mode adds detail without a second trading algorithm. Diagnostic capture is independent and default-off. Return construction occurs after execution; API/persistence schemas will be derived from actual consumer needs at checkpoint 4.

### Next implementation boundary

Implement and test fill accounting first, then the small runner/strategy slice after execution-policy decisions. Acceptance: the worked ledger, long/short/add/reduce/close/reversal cases, quantity conservation, fill equity identity, invalid-input atomicity, and identical state with recording enabled/disabled. Compare V1 only on cases with matching assumptions; explain expected differences. File-level implementation plan follows policy/precision inspection. No new production module, consumer migration or benchmark is part of this sketch.

## 2026-10-17 — Minimal fill accounting implemented

Implemented the isolated accounting slice after Destin approved proceeding: `backend/app/data_models/dto/backtest_ledger.py` holds a slotted mutable Ledger (cash, signed quantity, entry basis); `backend/app/services/backtest/accounting.py` provides equity and apply_fill. Fill accounting handles opening/increasing/reducing/closing/reversing; positive fee expenses are deducted once; negative balances and small residuals are preserved. Invalid inputs or non-finite results raise before mutation. No broker, API, history or strategy dependencies. Float quantities are approximate; instrument quantization remains outside accounting and needs resolution before execution integration. No exact decimal-lot conservation or speedup claim.

Verification: 23 offline tests pass, including worked ledger, long/short transitions, deficit/residual preservation, invalid-state/input and overflow atomicity, plus 500 deterministic fills compared with an independent Decimal cash-flow/cost-basis oracle. Scoped Ruff and strict mypy pass all three files. Existing engine is not wired to this module; liquidation/timing, runner and consumer redesign remain next work. No benchmark, live operations or commit.

## 2026-10-17 — Next-bar-open timing selected

Destin selected next-bar-open execution: decide from completed bar i, retain the instruction, execute at bar i+1 open under the selected slippage model. Do not use bar i+1 high/low/close for that fill or fabricate an execution beyond the dataset; opening risk checks precede risk-increasing execution. This requires pending-instruction state in the runner. Next-bar open is a candle-data timing approximation, not measured live latency.

Destin supports a clearly labeled simplified liquidation model that can later be replaced by venue rules and acknowledges maintenance margin. Exact maintenance rate, trigger sampling and deficit settlement are not yet selected. His observation that crypto liquidation leaves zero balance needs a distinction: Hyperliquid ordinary book liquidation can leave collateral; cross backstop liquidation transfers cross positions/margin and leaves zero equity when no isolated positions remain. Its ADL documentation explicitly addresses negative account/isolated equity. Sources checked 2026-10-17: https://hyperliquid.gitbook.io/hyperliquid-docs/trading/liquidations and https://hyperliquid.gitbook.io/hyperliquid-docs/trading/auto-deleveraging . Proposed design separates raw execution accounting from any explicit backstop/settlement adjustment; no blanket zero clamp or venue mechanics implemented.

## 2026-10-17 — Integer-unit next-open runner implemented

Implemented the approved isolated runner in `backend/app/services/backtest/core_runner.py`, with lightweight types in `backend/app/data_models/dto/backtest_core.py`. Ledger now holds exact signed integer instrument units and a configured unit_size; cash, basis and valuation remain floating point. Supported unit counts are bounded at 2**53 for safe integer-to-float conversion, with non-finite monetary results rejected before mutation. No implicit quantization, dust removal or instrument metadata conversion. Decimal-oracle tests now use 0.001-unit increments.

Runner: completed-close callback returns signed unit adjustment or None; it executes at the next row open with explicit fee/slippage rates. Pending quantity is fixed at decision time. Last-row instruction is returned unfilled. Opening liquidation checks precede pending fills, followed by post-fill and close checks. Optional fill callback receives only scalars; optional equity samples are numerical values. No StrategyResult, account/position snapshots or nested broker response. Execution state is O(1); requested equity history is O(N), and callers own input/prepared arrays and any retained fill history.

Liquidation must be supplied explicitly: None disables it; SimplifiedLiquidation requires maintenance_rate and deficit policy (preserve/backstop). This is a configurable approximation, not a selected production default or venue implementation: open/close prices proxy marks, trigger is equity <= maintenance_rate * marked notional, full exit occurs at observed price with costs, then termination. Backstop records a separate positive adjustment if cash is negative; positive remaining collateral is retained. No intrabar crossing reconstruction, margin tiers, initial-margin admission, partial liquidation or ADL. Rates and settlement are caller choices; no venue defaults inferred.

Validation: 43 offline tests pass; scoped Ruff and mypy pass six files. Coverage includes accounting/500-fill Decimal oracle, exact unit closing, next-open timing, pending final instruction, changed-future causality, detail-on/off equality, a 1000-bar no-order run without detail history, gaps cancelling pending orders, maintenance exits with positive collateral, post-fill fee breaches, both deficit policies, invalid inputs/configuration and overflow atomicity. No maximum benchmark or speed claim. Existing application dispatcher, strategies, V1/V2 engine integration and persistence remain untouched. No commit, live operation or deployment.

Next: connect a minimal real strategy to this runner, resolve production instrument quantization/admission and liquidation configuration, then derive metrics and application outputs from consumer needs. Timestamp/data alignment is currently the caller's responsibility; runner consumes ordered open/close sequences. No full-system correctness or production readiness claim.

## 2026-10-17 — Example strategy connected to independent core

Added `backend/app/backtest/strategies/example_core.py`: standalone ExampleCoreDecision and run_example_core connect all seven existing example configurations to the independent next-open runner. No inheritance from either strategy, no broker instance, no CandleCtx/DecisionContext or StrategyResult per bar. Existing configuration models and scalar math helpers remain shared deliberately. Pure feature/configuration/warmup operations were extracted to module-level functions in example_vectorized.py; legacy methods delegate, preserving the reference path and the volatility optimization comment.

Threshold gates depend only on signals, so prepare them once into readonly int8 state and boolean adjustment arrays (2 bytes per input bar in addition to existing prepared arrays). Existing threshold logic is reused during preparation; per-bar state-machine records disappear. Runtime sizing reads prepared arrays and supplied quantity/equity, then returns signed integer adjustments. Quantity conversion uses Decimal rounding toward zero to match the existing instrument decimal-scale rule; subsequent inventory differences use exact integer arithmetic. Static/compounding, full/continuous/banded, direct/inverse, volatility, minimum target and adjustment constraints are retained. Below-minimum adjustments are omitted without deleting inventory.

Verification: 69 core/accounting/strategy tests, 77 existing engine regressions and 35 vectorized-strategy regressions pass (181 total). Seven-config comparisons use identical flat-inventory/equity inputs against the old strategy; separate tests cover nonflat integer differences, deadband, static/compounding sizing, prefix causality, readonly arrays and actual next-open runs with old broker construction forbidden. This is not a claim of whole-run V1 parity: fill timing, valuation and quantity conservation intentionally differ. Scoped Ruff and mypy pass five files; missing third-party pandas stubs remain excluded. No benchmark, commit or live operation.

Boundary: offline function entry point only, existing application dispatch unchanged. All production instrument settings are explicit inputs. Minimum notional is currently checked at decision price; execution-time admission after a gap, initial-margin constraints, funding and venue-specific liquidation are not implemented. Tests explicitly disable liquidation to isolate decision comparison, not to choose a production default. Next bounded work should address next-open admission before application integration, then derive selected metrics and output persistence from actual consumers. Input features retain O(N) memory; the per-bar execution state remains bounded except requested recording.

## 2026-10-17 — Rewrite and shared example files separated

Completed the user-requested organization cleanup. The first-principles engine is now entirely under `backend/app/services/backtest/core/`: `runner.py`, `accounting.py`, `ledger.py`, `types.py`, and package marker. The former root accounting.py/core_runner.py and dto/backtest_ledger.py/backtest_core.py files were moved, not kept as compatibility shims. Explicit user request to colocate the rewrite takes precedence over the default central DTO convention.

Shared example configuration/validation now lives in `backend/app/backtest/strategies/example_config.py`; shared feature preparation/warmup and PreparedFeatures live in `example_features.py`. Both example_core.py and example_vectorized.py import those shared modules; neither imports the other strategy. Original example.py remains untouched. Retained the volatility optimization comment and the existing strategy method ordering. Updated all Python imports and the old ownership test that assumed config models lived inside example_vectorized.py. No trading behavior, application dispatch or persistence changes.

Reading order: strategies/example_core.py (new decisions) -> services/backtest/core/runner.py (timing/execution) -> core/accounting.py (fill math), with core/ledger.py (state) and core/types.py (configuration/results). Old bt_engine.py, bt_engine_v2.py, engine_dispatch.py and execution_diagnostics.py remain outside core; they belong to the existing application path, not this rewrite. Next work remains next-open admission checks, then application output/metrics integration. No commit or live operations.

Layout verification: 69 core/strategy tests and 77 engine regressions passed; 34 vectorized tests passed initially and the sole stale config-module ownership assertion passed after its update (181 distinct tests now passing). Scoped Ruff passes; mypy passes 12 files with missing third-party stubs excluded. No benchmark.

## 2026-10-18 — Engine owns orchestration

Destin explicitly chose the familiar manager -> engine -> strategy ownership and requested use of his empty core/core_engine.py. Moved the simulation loop from core/runner.py into core/core_engine.py and removed runner.py. Moved run_example_core out of the strategy file, renaming the engine entry point run_strategy_backtest; it now appears first, followed by _run_strategy_loop and execution/liquidation/input helpers. example_core.py contains only preparation and decision logic and imports no engine. Existing manager/executor names and application routing are unchanged; no new worker layer or manager was added. User-created empty core_manager.py was left untouched.

Current boundary: existing application plumbing calls engine_dispatch.py from AssetExecutor (direct) or summary_worker (process); that dispatcher still chooses bt_engine_v2 for example_vectorized. The rewrite is exercised through core_engine.run_strategy_backtest in offline tests and is not yet routed from API requests. This is explicit ownership cleanup, not completed application integration. It currently constructs the example decision strategy; generic multi-strategy selection is not claimed. Next-open admission and result/metrics integration remain outstanding.

Validation: 69 affected tests pass (all seven configurations, core arithmetic and timing, causal preparation, etc.); scoped Ruff and mypy pass four changed files, with missing third-party stubs excluded. Renamed test_core_runner.py to test_core_engine.py and updated tests to invoke the engine instead of the strategy convenience function. No accounting/timing policy changes, benchmarks, commits or live operations.
