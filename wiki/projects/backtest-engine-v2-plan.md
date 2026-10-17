# Backtest Engine V2 delivery draft

Status: in progress

Date: 2026-10-16

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
