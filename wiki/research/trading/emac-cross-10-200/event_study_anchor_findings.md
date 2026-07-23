# EMAC 10/200 Event Study — Anchor + Holdout Findings (2026-07-20/21)

Interpretation of the conditioned statistics from the [[event_labels_v1|frozen label grammar]] on the anchor fixture, read in the synthesis test order. Provisional until the disjoint Binance 5m holdout reproduces the signs and rankings.

- Fixture: run `8077b0dd-e440-48d7-8e64-a4ef81d1074e` (BTC Binance USD-M 5m, 49,800 scored bars, ~Jan 28 → Jul 19 2026). 11,953 events, 410 sign legs, 507 breakout episodes.
- Tooling: `mm_v04/backend/app/lib/analysis/event_study/interpret_events.py` (CLI, reads the fixture output dir, writes `interpretation.json`). Rerunnable on the holdout for direct comparison.
- Units: log returns in bps. Cost floor ≈ 20 bps per flip round trip (5 bps fee + 5 bps slippage per side; flip = close + open).
- Corrections recorded this session (Destin): sym #1 = mean break **as entry trigger** (the `S1` event), not a B1-bar filter state; and the observation window was **not** a favorable/cherry-picked one — flip-only was decisively negative here.

## Legend (label + metric glossary)

- **Leg** — one B1→B1 span (zero cross to next zero cross); the flip-only control holds exactly one leg at a time.
- **rtf (return-to-flip)** — signed close-to-close log return from an event bar to the leg's next zero cross; "what holding to the flip earns from here."
- **MFE / MAE** — max favorable / adverse excursion within a fixed forward horizon.
- **B1** zero cross of the processed signal · **B2** V4 threshold-engine transition (±0.01 hysteresis) · **B3** signal-slope sign flip.
- **R1 / R2** signal breach of the rolling mean ±1σ / ±2σ envelope (tag: prevailing = breach with the EMA regime, opposing = against it) · **R3** signal crossing the rolling mean · **R4** rolling-width pinch enter/exit · **R5** rolling-mean slope flip.
- **S1** |sig| breaks over the symmetric magnitude mean · **S2 / S3** breaks over the 1σ / 2σ bands · **S4 / S5 / S6** retreats back under the mean / 1σ / 2σ.
- **A1 / A2** |sig| breaks over the asymmetric *same-side* 1σ / 2σ band (per-side envelope) · **A3** first same-side break after that side was dormant · **A4** close back inside the same-side 2σ band (breakout exit) · **A5** dominance-skew sign flip.
- **Episode** — one A2-entry → A4-exit span (breakout mode; can be flat between episodes).
- **Mean cycle** — S1 entry → first S4 exit (enter on mean break, exit on mean retreat).
- **Escalation conditionals** — P(next band touch | previous band touched), per leg.
- **Cost floor** — ~20 bps round trip at the control's max-taker assumption (5 bps fee + 5 bps slippage per side); maker reality ≈ 2 bps round trip.

## Verdicts (anchor only)

1. **Leg selection via magnitude mean break — strongest structure.** Legs in which |sig| eventually breaks its magnitude mean (218/410, 53%) average **+53 bps** gross; legs that never break average **−43 bps** (−8,311 bps total across 192 legs). But the causal entry *at* the break captures only **+8.8 bps** mean (hit 33%) — by the time S1 fires most of the move is gone. The break works as leg-quality selection, not entry timing; the causal open question is finding an at-entry predictor of "this leg will break its mean," since gating on the future break is not causal.
2. **Escalation conditionals (sym #2) — supported.** P(1σ | mean break) = 0.71 vs 0.38 unconditional; P(2σ | 1σ) = 0.62 vs 0.24. Median time-to-touch 6–7 bars. Symmetric both sides. Part of the lift is mechanical (legs that break are stronger legs), but the conditional structure is real on this window.
3. **Rolling opposing-2σ = exhaustion / flip precursor — suggestive, n=76.** Signed by breach direction: −10/−20/−43 bps at 12/36/144 bars, and the sign flip arrives ~11 bars later (median). Opposing 2σ breaches mark late-leg blowoff, not entries. Prevailing R2 mildly positive (+11 bps at 144, n=316). The fresh-vs-stale (sign_age ≤ 12) split shows only mild differences — rolling breaches are not purely post-flip lag artifacts, but nothing else in the rolling family clears noise.
4. **Retreat de-risk levels (sym #3 vs agent S5) — mixed, level choice secondary.** Remaining-leg return after retreat: medians −24 (S4 mean-retreat), −32 (S5 1σ), −30 (S6 2σ) bps — every level marks a giveback-dominated remainder. But the whole-leg median from B1 itself is −27 bps, so the incremental value of the level is small; S5's positive **mean** (+7.3) is the fat tail of continuations an early exit forfeits. No decisive winner between Destin's 2σ and the agent's 1σ.
5. **Asym handoff (H1/H2) — failing.** A3 first-after-dormancy (n=600) is *worse* than B1 at 12/36 bars (−4.6/−6.9 vs −1.0/−2.5) with only a mild +8.7 at 144. A5 skew flips (n=130 directional) mildly positive long-horizon but late in legs (rtf mean −14). First-after-dormancy does not beat ordinary sign crosses on this window.
6. **Chop suppression via width/compression (H4) — failing.** Flagged vs normal B1 leg medians are indistinguishable (width pinched −25.0 vs normal −27.3; compressing −26.9 vs not −25.6). Neither state flag isolates the bad flips. (`sym_mean_filter` was already degenerate at B1.)
7. **Asym 2σ breakout mode — dead on anchor.** 507 episodes: −3.9 bps mean gross *before* costs, 30.6% win rate, both sides negative.
8. **Null check:** nothing clears the ~20 bps cost floor as a standalone fixed-horizon entry. Survivors are decision-changing structures: leg selection (1), escalation conditionals (2), retreat-marked giveback (4), opposing-2σ exhaustion (3).

## Review addendum (Destin pushback, 2026-07-20 evening)

Destin challenged the "move is gone" framing on (1): the S1-entry number was dragged down by the exit at zero, which sits below the mean. Computed follow-ups (new `band_cycles` cut in `interpret_events.py`):

- **Mean-in / mean-out cycle** (enter first S1 break per leg, exit first S4 mean retreat — which mechanically always precedes the flip): **+10.7 bps mean / −22.2 median / 29% hit** vs **+8.8 / −34.2 / 33%** for hold-to-flip on the same 218 legs. The mean exit recovers ~12 bps of median giveback; verdict (1) reworded — the entry forfeits the zero→mean appreciation, and chop cycles that never escalate keep gross under the ~20 bps floor.
- **Bps between band touches, given escalation:** mean→1σ **+33.4 mean / +24.2 median** (n=155, 82% positive); 1σ→2σ **+47.2 / +35.4** (n=95, 85%); mean→2σ **+79.8 / +56.3** (94%). Payoff per rung and hit rate both rise while climbing, on top of the 0.71/0.62 conditional touch rates. Most monetizable structure so far; its economics hinge on cutting the non-escalating branch cheaply. Top holdout question.
- **Retreat verdict (4) upgraded to supported (level ranking still undecided):** the retreat exit replaces the close paid at the flip anyway, so the 24–32 bps median saving is costless timing gain; S4 and S6 dominate hold-to-flip on both mean and median, only S5 forfeits the continuation tail.
- **Chop clarification for (6):** the test asks "should the strategy have refused this flip?", scored by whole flip-to-flip leg return, splitting B1 events by `rolling_width` pinch and `sym_compression` sampled at the flip bar. Per-flip medians are indistinguishable, but compression-flagged legs are shorter (median 33 vs 49 bars), so a per-unit-time reading could still favor suppression — check on holdout.

## Holdout replication (2026-07-21)

Disjoint immediately-preceding window: run `9c96c57f-733d-4b0b-a063-9a8824349d80` (same config/fees, Binance USD-M BTCUSDT 5m, `start_ms 1754505600000` → `end_ms 1769505600000`, ≈ Aug 7 2025 → Jan 27 2026, 50,000 bars, 457 legs, 12,208 events). Event study rerun with the anchor's config via `--start-ms/--end-ms`; artifacts in `output/8077b0dd-…_1754505600000_1769505600000/`.

**Replicated (symmetric magnitude family):**

- **Escalation ladder:** conditionals essentially identical (P(1σ|mean) 0.69 vs 0.71; P(2σ|1σ) 0.63 vs 0.62). Per-rung traversal stays positive with *higher* hit rates (88%/90%/96% vs 82%/85%/94%) at ~50–70% of anchor magnitude: mean→1σ +27.2 mean/+19.9 median; 1σ→2σ +24.3/+18.2; mean→2σ +48.6/+37.2 bps.
- **Mean-break leg selection:** skip rate 0.48 (vs 0.47); legs that never break total −6,825 bps (mean ≈ −31) vs +31 bps mean for legs that do. Separation holds.
- **Mean-in/mean-out cycle — strengthened relative to hold:** +12.9 bps mean / −12.2 median per cycle vs hold-to-flip collapsing to +0.9 / −25.3 on the holdout (anchor: +10.7 vs +8.8). The mean-exit return is roughly regime-stable across the two windows while hold-to-flip is not. Still under the ~20 bps cost floor gross.
- **Retreat giveback medians:** negative at every level again (−16 to −23 bps), but the level *means* flipped signs (S5 +7.3→−6.2; S6 −5.7→+11.0) — level ranking is noise; S4 (mean retreat) is the stable one (−3.2/−3.3 mean both windows).

**Weakened or dead:**

- **Rolling opposing-2σ exhaustion:** directionally consistent (−10/−17.6 at 36/144, flip ~7 bars later) but roughly half the anchor magnitude, and the anchor's +49 bps pre-flip blowoff signature vanished (−3.4). Contextual at best.
- **Asym handoff:** dead — A3's lone positive (144-bar +8.7) reversed to −25.8 on the holdout.
- **Chop flags (200-bar lookback as specified):** dead — pinched-width legs are again no worse (slightly better) than normal; compression split flipped. Destin's lookback caveat stands; visual validation of the compression areas remains the deferred check before tuning.
- **Asym breakout mode:** dead net of costs both windows (−3.9 and +1.8 bps mean gross vs ~20 bps cost).

**Bottom line:** all surviving structure lives in the symmetric magnitude family — mean-break selection, escalation conditionals, and the mean-cycle entry/exit — with the ladder's conditionals stable across regimes and its per-rung payoff regressing but staying decisively positive. No standalone structure clears costs yet; the smallest promotable experiment would be a bounded strategy variant of the mean cycle (S1 entry, retreat exit, optionally escalation-aware) evaluated against the flip-only control — pending Destin's call.

## Compression-flag visual diagnosis (2026-07-21)

Destin asked to examine the compression zones before going further. New reusable CLI: `plot_compression.py` in the event-study module (price + `pos_mean` vs its baseline + rolling std vs its quantile, flagged spans shaded, any date window). Rendered the Jul 12–19 screenshot week and the Jun 15 – Jul 19 month on the anchor. Diagnosis — the chop-flag failure is explained, not just observed:

- `sym_compression` has ~50% duty cycle and blankets trend segments (the Jul 13→14 rally runs inside a flagged span). Its comparator is a 200-bar SMA of a 200-bar mean — double smoothing that puts the baseline in near-quadrature with `pos_mean`, so the flag reads "post-impulse magnitude decay," not "market is quiet now."
- `rolling_width` pinch (~25% duty cycle by construction) is two-sided: it marks squeezes right before expansions as well as braids, consistent with its null at the flip bar.
- The genuine braid zones (e.g. Jul 17–18) *are* flagged — but buried among mid-trend false positives, which is why flagged and unflagged B1 legs average out the same.
- Label redesign is deliberately left open: Destin has further compression/expansion semantics to give; the 200-bar lookback critique stands but the deeper issue is the baseline construction.
- **Annotation review (Destin's pink-box chart, 2026-07-22):** the boxed compression zones share (a) the zero-anchored sym envelope at roughly half its weekly level (2σ band below the week's q25 in the clear cases), (b) actively contracting envelope (2σ level falling ~−0.5/day), (c) |sig| idling small. Trend windows show the opposite on all three. One box straddles the squeeze→launch boundary (levels low but envelope already expanding) — the exit condition (slope turn / signal breakout) matters as much as the entry. Pending candidate semantics: envelope *level* below a short reference (or absolute level on the bounded scale) with non-positive envelope slope — a market-state label independent of the zero-flip method (Destin: compression stands better outside the zero method). Not re-tested until Destin confirms phrasing.

## Cost-floor context (Destin, 2026-07-21)

The ~20 bps round trip used throughout is the control's max-taker assumption (5 bps fee + 5 bps slippage per side) — a ceiling, not a floor. Fees fall with volume, and maker executions run ~1 bps/side. At maker economics the surviving structures (band-to-band traversals, mean cycle) are already net positive as measured. If the core alpha holds at other timeframes, band-to-band bps grow relative to fees. All-in/all-out flip positioning remains the control condition only, not the endstate; learnings are expected to transfer to other positioning mechanisms.

## Caveats

Single window, single asset; overlapping forward windows at long horizons (treat means as effect sizes, not significance); flip-only baseline itself deeply negative here. Visual canvas of these results lives in the session workspace (`emac-event-study-anchor.canvas.tsx`), not the KB.

**Slope code divergence (2026-07-22) — affects B3/`slope_state` and R5/mean-slope labels.** The live/backtest strategy slope was changed: `emac_v4.py` now calls a new `sig_slope` (raw linear regression, no `ln`) instead of the log `Slope`/`lr_slope`. `slope.py` adds `sig_slope` + `raw_lr_slope`; `Slope`/`lr_slope`/`ln` are unchanged. The event-study path (`backend/app/lib/analysis/event_study/series.py`) still calls the **log** `Slope` on the signed signal, so every slope-based label in these findings reflects the OLD `ln(max(x,eps))`-clamped behavior (negative signal stretches flatten to slope 0) and **no longer matches the live strategy's slope**. Before relying on B3/`slope_state` or R5/mean-slope going forward, either rerun the event study after switching `series.py` to `sig_slope`, or read those two label families as legacy-log-slope only. All non-slope labels (magnitude family, escalation, rolling, asym, chop) are unaffected. Not yet changed in the research path — scoped to the live signal this session.

## Next

Cache one disjoint earlier Binance 5m window via the normal backtest path, rerun `run_event_study` + `interpret_events` with `--run-id <anchor> --start-ms/--end-ms`, and check which verdict signs/rankings survive — in particular (1), (2), and (3) above.
