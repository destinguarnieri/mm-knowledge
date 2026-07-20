---
name: Rolling vs Magnitude Stats
overview: Snapshot of first-pass pattern-match findings comparing rolling vs magnitude signal statistics on the same EMAC 10/200 signal, plus the candidate trade-mapping implications to review before deciding any next experiment.
todos: []
isProject: false
Model: Fable 5 High
Skill: Discretionary Strategy Codifier
---

# Rolling vs Magnitude Signal Stats — First-Pass Snapshot

Status: observation only, no code changes, no KB writes. Awaiting Destin's comments before anything becomes an experiment or implementation.

## Source material

- Charts in `mm-knowledge/wiki/research/trading/emac-cross-10-200/`: `rolling_stats.png`, `magnitude_stats.png` (symmetric config, confirmed by Destin), and `mag_asym_stats.png` (asymmetric config) — same asset (BTC), same window (12th–20th), same EMAC 10/200 processed signal; only the signal-panel statistics differ. The rolling and asymmetric screenshots share the exact same last bar (signal `0.4463`); the symmetric screenshot is one bar earlier (`0.4349`).
- Code behind each mode in [backend/app/backtest/strategies/emac_v4.py](backend/app/backtest/strategies/emac_v4.py) `_signal_stat_messages`:
  - `rolling` → [backend/app/lib/indicators/sig_stats.py](backend/app/lib/indicators/sig_stats.py): signed rolling mean, bands = mean ± 1σ/2σ (envelope drifts with the signal).
  - `magnitude` → [backend/app/lib/indicators/sig_extension.py](backend/app/lib/indicators/sig_extension.py): zero-anchored excursion-magnitude bands. Symmetric mode uses shared |signal| stats mirrored to both sides; asymmetric mode computes per-side mean/σ via `SMA_PINE` (occupancy-diluted; see asym observation 4). `emac_v4` `"magnitude"` mode uses `symetric=False`.

## Core finding

Rolling stats is a **change detector**; symmetric magnitude stats is an **extension detector**; asymmetric magnitude sits between them — zero-anchored like magnitude but per-side regime-adaptive, so it is transition-sensitive at regime birth and extension-sensitive at maturity.

The same final bar read through all three lenses (right-edge labels): rolling z ≈ +2.3 (beyond 2σ), asymmetric z_pos ≈ +1.7 (between bands 1 and 2), symmetric z ≈ +0.8 (inside band 1). The ordering — rolling most transition-sensitive, symmetric most stable, asymmetric in between — is structural, not coincidental.

## Observations (with chart anchors)

1. **Same bar, opposite reading.** Right-edge labels: rolling mean `-0.0355`, σ ≈ 0.207 → current signal `0.4463` is a >2σ event. Magnitude pos_mean `0.1671`, σ_pos ≈ 0.336 → same burst is only ~+0.8σ. Rolling flags freshness of the flip, not size of the excursion.
2. **Rolling fires at trend birth, then goes silent.** At each turn (13th, 14th, 16th–17th, 18th) the signal slices the displaced rolling envelope (big z), then the mean catches up and z decays toward zero through the mature trend (15th plateau). Rolling z structurally cannot mean "trend is stretched."
3. **Magnitude tags trend peaks.** Green humps on the 14th and 18th–19th touch magnitude +1σ/+2σ near max EMA separation; retreat inside bands precedes the fade. Correct input for exhaustion / don't-chase / de-risk semantics.
4. **Rolling band-width pinch is a chop flag.** Around the 16th the whole rolling envelope collapses toward zero during the EMA braid; magnitude bands barely narrow there. Rolling width is the better dead-zone detector.
5. **Signal-crosses-rolling-mean is an earlier trigger than zero-cross** at every turn (mean is displaced in the old trend's direction). Earlier entry, more whipsaw. Magnitude stats has no analogous trigger.
6. **Confirmed:** the `magnitude_stats.png` bands are exactly mirrored (`±0.8397`, `±0.5034`, `±0.1671`) → symmetric `sig_extension` config, per Destin.

## Observations — asymmetric magnitude (second pass)

1. **Per-side regime memory.** Lower envelope balloons during the long red leg (13th) while the upper envelope collapses flat against zero; roles swap after the 14th flip. Each side's bands reflect only that side's recent activity.
2. **Transition sensitivity returns, per side.** After a long red regime the positive-side stats have decayed toward zero, so the first green burst towers above the collapsed upper bands (start of the 14th up-leg). Bands inflate and catch up; by trend maturity the signal rides inside. Rolling-like at regime birth, extension-like at maturity.
3. **Partial chop pinch.** Both envelopes compress toward zero in the 16th–17th braid — weaker than the rolling pinch, absent in symmetric mode.
4. **Occupancy-dilution semantics (confirmed intended, 2026-07-19).** `SMA_PINE` sums a side's values over the window but divides by the full `span`; bars spent on the other side contribute zero yet stay in the denominator ([backend/app/lib/indicators/sma_padded.py](backend/app/lib/indicators/sma_padded.py)). So `pos_mean` conflates typical green-excursion magnitude with fraction of time spent green. Destin confirmed this is deliberate — it captures the occupancy factor and natural decay when a side is inactive — while flagging it "may be a naive implementation." Non-blocking refinement candidate only: a count-normalized per-side mean is a *different* strategy variant, not a fix. Behavioral consequence stands: "signal > pos band 1" fires for a different reason early in a regime (occupancy starvation) than late (genuine size).
5. **Unique information: band skew.** Upper-vs-lower envelope size directly encodes which side has dominated recently (huge lower/flat upper on the 13th; reversed through the 15th). Symmetric mode destroys this by construction.

## Candidate trade mappings (kept separate, not merged)

- **Entry/flip:** rolling z spike at transition, or signal-crosses-rolling-mean (aggressive variant), vs plain zero-cross baseline.
- **Extension / de-risk / continuous sizing:** symmetric magnitude bands; `extension_value` (signal ÷ 2σ band) is a quasi-bounded input for the planned `sig_to_position` work. Most stable "stretched" reference of the three.
- **Adaptive extension (this trend's own scale):** asymmetric bands — after inflating, only excursions bigger than the current regime's typical push tag 2σ. Caveat: as a don't-chase filter it would suppress entries exactly at trend birth (first excursion always reads extended); as a fade-the-first-counter-bounce rule that same property is the mechanism.
- **Chop suppression:** rolling band-width floor as an entry permission gate (asymmetric width pinch as a weaker alternative).
- **Regime skew:** asymmetric band asymmetry as a slow directional-bias input (unique to asym mode).
- **Anti-pattern to avoid:** rolling z as exit-on-extension — fires at trend birth, never at maturity. Same trap applies to asymmetric z immediately after a regime flip.

## Destin rulings (2026-07-19)

- Asymmetric occupancy dilution is intended as-is (see asym observation 4).
- No fixed discretionary interpretation of the three stat modes: they may be used flexibly, in combination or separately, each producing different strategy variations around the same stats.
- Experiment design is delegated: run experiments as I see fit, uninfluenced by his inputs. The discriminating experiment below stands unmodified.
- Note on "z" in this document: z-score is not plotted or emitted anywhere; all z values here are derived from panel geometry (bands are mean ±1σ/±2σ, so z = distance from the mean label in units of band spacing). `sig_stats`/`sig_extension` compute `z_score` arrays but `emac_v4` does not emit them.

## Next observation pass (before/alongside experiments)

Pattern match the panels hidden in the current screenshots, on the same fixture and window: cumulative PnL, PnL per bar, position ROE, position size, and the signal itself. Goal: connect the three stat-lens readings to realized monetization behavior (especially the known high-time-in-money / low-realized-win-rate giveback diagnosis). Destin will share his own panel observations after this snapshot is settled.

## Open questions for Destin

1. What timeframe are these screenshots (to pin the fixture for any parity/threshold run)?

## Proposed next step (pending your comments)

Smallest discriminating experiment: on the canonical BTC fixture, a bounded threshold comparison using rolling-derived triggers for entry vs magnitude-derived bands for exit/sizing, each evaluated as its own mapping against the static ±0.01 V4 baseline (`bad11f56-…`). Not started.