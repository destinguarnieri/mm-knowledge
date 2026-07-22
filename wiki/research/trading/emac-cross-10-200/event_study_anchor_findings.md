# EMAC 10/200 Event Study — Anchor Findings (2026-07-20)

Interpretation of the conditioned statistics from the [[event_labels_v1|frozen label grammar]] on the anchor fixture, read in the synthesis test order. Provisional until the disjoint Binance 5m holdout reproduces the signs and rankings.

- Fixture: run `8077b0dd-e440-48d7-8e64-a4ef81d1074e` (BTC Binance USD-M 5m, 49,800 scored bars, ~Jan 28 → Jul 19 2026). 11,953 events, 410 sign legs, 507 breakout episodes.
- Tooling: `mm_v04/backend/app/lib/analysis/event_study/interpret_events.py` (CLI, reads the fixture output dir, writes `interpretation.json`). Rerunnable on the holdout for direct comparison.
- Units: log returns in bps. Cost floor ≈ 20 bps per flip round trip (5 bps fee + 5 bps slippage per side; flip = close + open).
- Corrections recorded this session (Destin): sym #1 = mean break **as entry trigger** (the `S1` event), not a B1-bar filter state; and the observation window was **not** a favorable/cherry-picked one — flip-only was decisively negative here.

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

## Caveats

Single window, single asset; overlapping forward windows at long horizons (treat means as effect sizes, not significance); flip-only baseline itself deeply negative here. Visual canvas of these results lives in the session workspace (`emac-event-study-anchor.canvas.tsx`), not the KB.

## Next

Cache one disjoint earlier Binance 5m window via the normal backtest path, rerun `run_event_study` + `interpret_events` with `--run-id <anchor> --start-ms/--end-ms`, and check which verdict signs/rankings survive — in particular (1), (2), and (3) above.
