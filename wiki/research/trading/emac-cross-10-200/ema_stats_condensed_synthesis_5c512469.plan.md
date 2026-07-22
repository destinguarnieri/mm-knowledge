---
name: EMA Stats Condensed Synthesis
overview: Single condensed synthesis of three independent agent reviews (rolling vs symmetric magnitude vs asymmetric magnitude signal statistics on the EMAC 10/200 signal), merging shared findings, preserving unique observations, and unifying the proposed discriminating experiment.
todos:
  - id: pin-metadata
    content: Confirm timeframe and which symmetric/asymmetric config produced each screenshot (resolve emac_v4 symetric=True/False drift).
    status: completed
  - id: define-events
    content: Define causal, non-overlapping event labels across all three stat lenses plus sign/slope baseline.
    status: completed
  - id: run-event-study
    content: Run forward return / MFE / MAE event study on the canonical BTC fixture, conditioned on regime, regime age, and same-side activity.
    status: pending
  - id: test-incremental-info
    content: Test asymmetric dominance first, then rolling-surprise incrementality, then chop suppression; reject anything explained by simpler states.
    status: pending
  - id: bound-combined-control
    content: "Only if info survives: specify smallest combined control and evaluate vs static ±0.01 V4 baseline plus one holdout fixture."
    status: pending
isProject: false
Model: Fable 5 High
Skill: None
---

# EMA Signal Stats — Condensed Synthesis (3-Agent Merge)

Sources merged: `ema_stats_pattern_trail_ff74e053` (GPT 5.6 Sol, no skill), `ema_stats_comparison_7ae09594` (no model tag), `rolling_vs_magnitude_stats_63361ce6` (Fable 5, Discretionary Strategy Codifier). Observation-only; no strategy or runtime changes implied.

## Settled facts (confirmed, supersede open questions in the other two docs)

- **Chart metadata (Destin, 2026-07-20): 5-minute timeframe, July 12–19 2026, Hyperliquid data.** Asset BTC, EMAC 10/200 processed signal throughout.
- Charts, two generations in `mm-knowledge/wiki/research/trading/emac-cross-10-200/`:
  - First pass: `rolling_stats.png`, `magnitude_stats.png` (symmetric, bands exactly mirrored ±0.8397/±0.5034/±0.1671), `mag_asym_stats.png` (asymmetric). Rolling and asym shared last bar (signal 0.4463); symmetric was one bar earlier (0.4349).
  - 4-panel set: `rolling_4panel.png`, `mag_sym_4panel.png`, `mag_asym_4panel.png` — all three share the same last bar (signal 0.4463; rolling mean −0.0355 bands 0.1717/0.3789; sym mean 0.1647 bands 0.5034/0.8421; asym pos mean 0.0646 bands 0.2914/0.5182). Trade panels are identical across the three images (one run, three stat lenses). Panels top→bottom: price + EMA cloud, PnL per bar ($), position ROE (%), position size (signed $), signal stats. Cumulative PnL is not rendered in this set.
- Code: `rolling` → `sig_stats.py` (signed rolling mean ± 1σ/2σ, envelope drifts with the signal); `magnitude` → `sig_extension.py` (zero-anchored excursion bands; symmetric mirrors shared |signal| stats, asymmetric computes per-side stats via `SMA_PINE`).
- Code drift resolved (Destin, 2026-07-20): not drift — `symetric` is not yet exposed in config, so Destin flips it by hand in [backend/app/backtest/strategies/emac_v4.py](backend/app/backtest/strategies/emac_v4.py) per render. The screenshot filenames label which config produced each image (`mag_sym_*` = `symetric=True`, `mag_asym_*` = `symetric=False`).
- Destin rulings (2026-07-19): asymmetric occupancy dilution is intended as-is; no fixed interpretation of the three modes (flexible, combinable, each a strategy-variant axis); experiment design delegated.
- All "z" values below are derived from panel geometry (band spacing), not emitted; `z_score` arrays exist in the helpers but `emac_v4` does not emit them.

## Core finding (unanimous across all three)

- **Rolling** = change/transition detector: measures surprise relative to the recent signed regime. Fires at trend birth (signal slices the displaced envelope), then mean catches up and z decays through the mature trend. Structurally cannot mean "trend is stretched."
- **Symmetric magnitude** = extension detector: absolute directional force on a zero-anchored, sign-neutral scale. Tags trend peaks near max EMA separation; retreat inside bands precedes fades. The most stable "stretched" reference.
- **Asymmetric magnitude** sits between: zero-anchored but per-side regime-adaptive — rolling-like at regime birth (first impulse towers over the decayed same-side envelope), extension-like at maturity (bands inflate, signal rides inside).
- Same-bar proof (right edge): rolling z ≈ +2.3, asym z_pos ≈ +1.7, symmetric z ≈ +0.8. The ordering is structural, not coincidental. Interpretation: an early re-acceleration state — novel vs the prior regime, moderate in absolute force.

## Merged observations

- **Signal amplitude tracks acceleration, not price extrema.** Price often continues after amplitude decays, so amplitude is not a standalone exit/direction rule, and fading outer-band events is unsupported by this sample.
- **Adaptive self-normalization:** all rolling/adaptive bands expand after strong impulses; event meaning changes with regime age.
- **Asymmetric band skew is the unique information.** Upper-vs-lower envelope size directly encodes recent directional dominance (huge lower/flat upper during the long red leg on the 13th, roles swap after the 14th flip). Symmetric mode destroys this by construction. Candidate bounded form: `(upper − |lower|) / (upper + |lower|)`.
- **Occupancy-dilution semantics (intended):** `SMA_PINE` divides a side's sum by the full span, so each side's envelope conflates typical excursion magnitude, sign occupancy, and recency — "side-specific force occupancy," not a conditional distribution. Consequence: "signal > pos band 1" fires for different reasons early in a regime (occupancy starvation) vs late (genuine size). Any predictive claim must separate this mechanical compression effect from real information.
- **First-moment decomposition:** `pos_mean + neg_mean` ≈ signed rolling mean; `pos_mean − neg_mean` ≈ mean absolute magnitude. So asymmetric first moments largely re-express existing information; per-side dispersion (and skew) is the distinct content.
- **Chop detection:** the rolling envelope pinches toward zero in the 16th–17th EMA braid (strongest dead-zone flag); asymmetric shows a weaker pinch; symmetric barely narrows. Separately, sign changes occurring at subdued magnitude relative to bands are candidate no-flip events (chop suppression).
- **Earlier trigger:** signal-crosses-rolling-mean leads zero-cross at every turn (mean displaced in the old trend's direction) — earlier entry, more whipsaw. No magnitude analogue.
- **Phase model (candidate labels, not rules):** dormant side → directional shock → envelope expansion / regime acceptance → mature trend with signal decay → same-side contraction → opposite-side shock.
- **Profit-retention link:** the multi-panel view reinforces the known giveback diagnosis — favorable paths build in established trends, then surrender open profit near flips. Magnitude peaks occur before/during accumulation, not at a dependable exit point.
- **Anti-pattern:** rolling z (or asym z immediately after a flip) as exit-on-extension — fires at trend birth, never at maturity.

## Competing hypotheses (deduped)

1. **Role split (leading):** sign = direction; symmetric magnitude = exposure/continuation; asymmetric = early regime-handoff + slow directional bias; rolling = transition timing/confirmation.
2. **Asymmetric-only:** envelope skew alone captures both permission and transition; rolling adds nothing.
3. **Rolling-artifact:** rolling breaches are lag artifacts after sign changes; no info beyond zero-cross + slope.
4. **Chop suppression:** low relative magnitude identifies sign changes that should not trigger full flips.
5. **Null:** all three overlays are descriptive transforms of one signal; no out-of-sample net improvement after costs.

## Unified discriminating experiment (bounded, no trading-behavior change)

1. Pin remaining chart metadata (timeframe; which symmetric/asymmetric config produced each screenshot given the code drift above).
2. Define causal, non-overlapping event labels: zero/sign cross (baseline), slope direction, rolling ±1σ/2σ surprise (prevailing vs opposing), signal-crosses-rolling-mean, symmetric mean/1σ/2σ crossings, asymmetric same-side crossings including first-after-inactivity, dominance/skew state, dormancy/compression, envelope expansion. From the 2026-07-20 observation sets, add: symmetric mean-filter state (inside vs beyond mean), band-to-band escalation conditionals (mean→1σ→2σ touch chains), symmetric 1σ/2σ retreat-after-outside (de-risk candidates), symmetric mean-band compression vs its own average (chop label), asymmetric 2σ breakout / close-back-inside (breakout mode, allows flat), rolling-mean slope and slope-vs-sign disagreement (filter/sizing input).
3. Event study on the canonical BTC fixture: forward return, MFE, MAE at 1/3/6/12 bars, conditioned on EMA regime, regime age, and recent same-side activity.
4. Test order (cheapest discriminators first): (a) does asymmetric dominance separate continuation/pullback from true reversal better than sign + slope alone; (b) does rolling surprise add anything beyond zero-cross + slope + asymmetric compression — reject if the simpler state explains the outcomes; (c) low- vs high-magnitude sign crosses for chop suppression; (d) control asymmetric effects separately for sign frequency and same-side average magnitude to locate the source of any effect.
5. Only if complementary information survives: specify the smallest combined control — asymmetric state for directional permission, rolling surprise for timing (only if incremental), symmetric/same-side magnitude for target exposure — and evaluate as its own mapping against the static ±0.01 V4 baseline (`bad11f56-…`), then one untouched holdout fixture. Judge net economics, drawdown/MAE, profit retention, turnover, costs — not visual fit.

## Falsifiers and stop condition

- Asymmetric-handoff dies if first opposing-band crossings do not beat ordinary sign crosses on forward return, MFE/MAE, or false-transition rate.
- Chop suppression dies if low-magnitude sign crosses are not materially worse than high-magnitude ones.
- Rolling dies if breaches are explained by zero-cross + slope.
- Visual-selection risk: all patterns were identified on one observation window (Destin, 2026-07-20: it was **not** a favorable one — flip-only was decisively negative there, so the risk is pattern selection by inspection, not window cherry-picking); nothing is promoted until event rules are causal and tested on fixtures not chosen from these screenshots.
- Stop when an overlay adds no stable causal information beyond the raw-signal baseline; continue only if it changes a bounded entry/exit/sizing decision and improves holdout outcomes.

## 4-panel trade-panel pass (2026-07-20, observation only)

Pattern-match of the PnL/ROE/position panels against the three stat lenses on the 4-panel set. Every trend leg shows the same four-act sequence:

1. **Entry act — flip + whipsaw tax.** Realized PnL lands only at zero-cross flips (the +$200-class green spikes: early 14th, mid 15th, 17th ~13:00, early 19th). Most flips are immediately followed by a cluster of small red PnL ticks with the position bar flickering green/red (clearest early 14th and through the 19th). Rolling z-spike and asymmetric first-impulse both fire exactly where this tax is paid — so "earlier entry" variants amplify the tax unless gated by the chop state.
2. **Accumulation act.** ROE builds while the signal rides at/above the symmetric +1σ band: 14th–15th long peaks ~4.5% mid-15th near max band extension; 13th and 16th–17th shorts peak ~3% at their capitulation lows; 17th–19th grind builds ~2.5% slowly. ROE peaks coincide with magnitude peaks (amplitude ≈ acceleration ≈ open-profit accumulation).
3. **Giveback act — now a bounded interval.** ROE decay begins when the signal retreats back inside the symmetric 1σ band; the flip only comes at zero-cross, often many hours later. Two candidate early markers sit inside this window on every leg: signal-crosses-rolling-mean, and asymmetric same-side envelope contraction.
4. **Realization act.** Slow rollovers realize well below peak ROE (15th long: ~4.5% peak, decayed hard before the flip). The 17th V-bottom compressed the window so realization landed near peak. Giveback severity looks proportional to rollover speed — magnitude-retreat timing captures this, zero-cross timing cannot.

Chop economics: the red-tick loss clusters (15th 18:00–16th, 16th–17th braid, 19th afternoon) coincide bar-for-bar with position flickering, rolling envelope pinch (strongest), asymmetric both-side compression (weaker), and sign crosses at subdued magnitude. These clusters are the cost chop suppression would delete.

Right edge in trade terms: long +$9.89K at ROE −0.18% — a fresh re-acceleration entry not yet paid off, consistent with the early-state reading.

**Addition to the event study (step 3 above):** for each candidate early-exit event (sym 1σ retreat, signal-crosses-rolling-mean, asym same-side contraction), also measure ROE surrendered between event and actual flip per leg — a direct score of which lens best marks the start of the giveback act.

## Destin's observations and hypotheses (2026-07-20)

Framing primer: all-in/all-out flip positioning was the intentional simplest starting point and remains a good control condition, but it is not the destination. There are many ways to reach good outcomes; the build philosophy is start as simple as possible, then progressively add complexity. New mechanisms below may leave the always-in-market family entirely.

**Symmetric magnitude:**

1. **Mean lines (white) as trade filter.** Signal beyond the mean = something interesting is happening; inside the mean = no strong trend or breakout. Candidate binary permission state. *(Semantics corrected 2026-07-20: the intent is the mean break as the entry trigger itself — the `S1_mean_break` event — not a filter state sampled at the zero cross.)*
2. **Band-to-band continuation in the sign direction.** Mean break tends to reach 1σ; 1σ break tends to reach 2σ. Escalation-conditional structure — testable as conditional touch probabilities.
3. **2σ re-entry as de-risk/exit.** Signal rolling back under the 2σ band after being outside it is probably a good de-risking or exit point. (Sits in the same band-retreat family as the agent-observed 1σ-retreat giveback start; the event study should test both retreat levels.)
4. **Mean-band compression as the chop/regime label.** All bands compress/expand, but the mean bands (white) look most useful — arguably a better compression read than rolling. Candidate regime label: current mean-band compression vs its own average compression.

**Asymmetric magnitude:**

1. **Breakout mode.** Enter on breaks outside the 2σ band, close on the break back inside. This behaves like a breakout trader rather than trend following: it won't capture the whole trend, but it also won't get chopped around zero. Note this is a structurally different position shape — it can be flat, unlike the flip-only control.

**Rolling stats:**

- Little directly transferable visual value beyond what's already captured.
- 2σ band break as regime change stands.
- 2σ band compression/expansion looks obviously plausible as a value input.
- **Mean-slope hypothesis:** the slope of the rolling mean appears to track the price trend — candidate for aligning position to it, or at minimum as a filter/sizing input when mean slope disagrees with signal sign.

**Timeframe priority:** 1m and 5m preferred; priority weight decreases as timeframe increases. The 1D starting point of the original scan is low-interest.

**Positioning-mechanism space (2026-07-20):** all-in/all-out is only the simplest control. Known family: flip-only; `sig_to_position` (signal amplitude → target position); inverse `sig_to_position` variant; proposed quantile-regression mapping (QR fed by the signal and its stats; Q90/Q50/Q10 outputs, position from current value's proximity to the quantiles, weighted by regression r²; stated mainly to open the positioning scope beyond oversimplistic methods); plus further mappings not yet recorded in this repo. Agent-added candidates (hypotheses only): band-ladder sizing (discrete steps at sym mean/1σ/2σ), bounded z→position map (tanh/clipped of sym or asym z), volatility-targeted overlay (scale any direction signal by inverse realized vol), regime-age decay (shrink target as same-side envelope contracts), asym-skew directional bias (position tilt from `(upper−|lower|)/(upper+|lower|)`), breakout mode with flat state (asym 2σ in/out), and edge-proportional sizing (fraction from the event study's measured conditional edge). Each is a separate strategy variant to be tested against the flip-only control, not merged features.

## Pending

Event labels are defined in [[event_labels_v1|EMAC Signal-Stats Event Labels V1]] (2026-07-20): full causal grammar, state labels, point events, covariates, outcome measures (including return-to-flip and 5m-appropriate horizons out to 144 bars), and hypothesis→falsifier mapping. Fixture anchored on BTC Binance USD-M 5m run `8077b0dd-e440-48d7-8e64-a4ef81d1074e` (49,800 scored bars, ~Jan 28 → Jul 19 2026, summary retention — Hyperliquid only serves ~5,000 bars/timeframe, so Binance is the depth source per Destin). Hyperliquid full run `d82eda65-…` kept as the screenshot-parity companion; 1D `bad11f56-…` secondary. Note: `e58f3c5d-…` exists in the persistence layer per MCP but was not visible in Destin's UI table — possible recurrence of the saved-run UI scoping issue. `run-event-study` (2026-07-20): the offline script is built at `mm_v04/backend/app/lib/analysis/event_study/` and has run on the anchor (11,953 events, 410 sign legs, 507 breakout episodes; local CSV artifacts). Implementation-time analysis choices are recorded in the event_labels_v1 implementation section. **Anchor interpretation is done (2026-07-20)** via `interpret_events.py` (reusable cuts + `interpretation.json`); verdicts and key numbers live in [[event_study_anchor_findings|Anchor Findings]] — headline: magnitude mean-break separates good legs (+53 bps avg) from bad ones (−43 bps) but fires too late to serve as the entry; escalation conditionals real (0.71/0.62 vs 0.38/0.24); asym handoff, chop flags, and asym breakout all failing/dead on the anchor. Remaining before the todo closes: cache one disjoint earlier Binance 5m holdout window and rerun both scripts with `--run-id <anchor> --start-ms <ms> --end-ms <ms>`.