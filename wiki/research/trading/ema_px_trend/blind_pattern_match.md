# EMA/PX Trend — Blind Pattern Match (Track 3)

Running doc for the third research track: Destin shows unlabeled price charts with indicators attached, one window at a time; the agent pattern-matches directly, states falsifiable rules, updates priors each window, and ultimately codifies a strategy.

Deliberately isolated from the other two tracks (agent signal-panel event stats; Destin-labeled chart codification in [[codification]]). Do not import their observations into this doc until a convergence review is explicitly requested.

## Goal

Capture what Destin already trades by hand, codify it, target net positive returns with decent Sharpe. Validation is out-of-sample backtest once rules are codified — no backtest series exists yet for this track; surrounding tools exist to build it.

## Setup

- Indicators: **10 EMA of lows** and **200 EMA of close**, color-coded by price relationship (over/under).
- First asset/timeframe: **HYPE (Hyperliquid) 4H**.
- Process: one chart window at a time, walked forward. Each window produces observations and prior updates recorded here.
- Discipline: every candidate pattern must be verbalized as a precise, falsifiable rule before any strategy code is written. Chart reads are hypothesis generation only; hindsight bias on visible windows is assumed until rules survive unseen data.

## Current Priors

<!-- Format per prior: id, statement (falsifiable rule), confidence (low/med/high), supporting windows, contradicting windows -->

- **P1 — Regime line, structural-precursor confirmation (medium-high):** 200 EMA_close side defines direction, but raw crosses are noisy. Dwell time alone is DEAD as a confirmation (Aug: ~1 week below, deep excursion, still reclaimed). Slope agreement also insufficient. Current discriminator: real flips are preceded by structural change — chop/top formation around a flattening 200 (Feb), aging-regime stress + acceleration away (Sep), or capitulation extension + V-reversal (Apr); fakes are single sharp counter-moves against an otherwise healthy trend that never accelerate away (Jun, Aug, late-Oct). Support: W1–W4 (Sep call graded correct out-of-sample). Contradict: dwell/slope forms killed by W3.
- **P2 — Continuation entry at the 200 (high):** Pullback/rally into the 200 EMA that holds/fails is the continuation entry in both directions. Support: W1 (Mar rejection short), W2 (Jun hold long), W3 (late-Jul tag-and-hold long; Aug reclaim → mid-Aug rally), W4 (early-Oct and late-Oct underside rejections, both followed by large legs down). Contradict: none.
- **P3 — Chop filter (medium):** Flattening 200 slope + repeated fill flips = stand aside. Support: W1 (Feb), W3 (late-Aug chop around flattening 200). Contradict: none.
- **P4 — 10 EMA_low as pullback zone, not hard trail (low-med):** Pierced repeatedly mid-trend without trend end (W2 late May/mid-Jun, W3 multiple). Use as pullback/re-entry zone; 200 carries the regime exit. Support: W1–W3. Contradict: strict-trail form weakened by W2/W3.
- **P5 — Trend persistence with aging signature (medium):** Regime flips run for months (Apr → Sep macro uptrend, 15 → 57). New nuance from W3: regimes age — 200-stress frequency rises late in trend (one stress event in W2 vs three in W3 before the Sep break). Support: W2, W3. Contradict: none.
- **P6 — Break trades need extension-based partial exits (medium):** Aug break short had ~15% open excursion at the low; reclaim-only exit gave it all back. Take partial profit at extension, remainder on reclaim (or % combo). W4's Oct 10–11 flash wick (huge extension, instant recovery) is further support — extensions mean-revert fast. Support: W3, W4 (also W1's ~9.3 capitulation). Contradict: none.
- **P7 — Directional asymmetry, phase-refined (medium):** Downtrends are jagged with violent deep counter-rallies; the tradeable short events are 200-underside rejections. Early/mid uptrend legs stair-step riding the 10 EMA_low — but late legs can go parabolic and crash with downtrend-like violence (W6 May→Jun: ~46→76 parabola, then −27% in ~4 days). Asymmetry is a phase property more than a direction property. Long and short books still need different mechanics. Support: W1–W5. Contradict: W6 partially (smoothness claim weakened for late-phase legs).
- **P8 — Close-based logic, not wick-based (medium):** W4's Oct 10–11 flash wick (print near ~21, instant recovery to mid-30s) would destroy wick-triggered stops/regime logic. Regime state and exits should key off closes; wicks only feed extension measures. Support: W4. Contradict: none.

## Candidate Rules

Rules v1 (finalized after W7, all seven windows reviewed; pre-registered record 2-for-3 clean + 1 contaminated miss + 1 live call open). All parameters to be tuned by backtest, not by eye. Codification-ready.

- **R1 — Regime state:** direction = side of 200 EMA_close, using closes only (P8). Flips require structural-precursor confirmation (P1): top/chop formation at a flattening 200, capitulation extension + V-reversal through both lines, or aging-regime stress followed by acceleration away from the line. Single sharp counter-moves against a healthy trend do not flip regime.
- **R2 — Continuation entry:** enter with-regime on pullback/rally into the 200 zone that holds/rejects (P2, highest confidence). Long side may also use 10 EMA_low tags in strong trends (P4, P7).
- **R3 — Chop filter:** stand aside when 200 slope flattens and fill flips cluster (P3).
- **R4 — Exits:** partial at extension from the 200 (ATR or % distance, defined from data), remainder on close-based reclaim of the regime line, tunable % combination (P6). No wick-triggered exits (P8).
- **R5 — Asymmetry:** long and short books tuned separately — short entries lean on 200-underside rejections; longs ride 10 EMA_low structure (P7, phase-refined: late-phase parabolic legs are exit/partial territory, not stair-step hold territory).

W7 refinements folded in: violence of a break is NOT a flip signal (June −27% break held; no precursor → fake). Young/healthy-trend breaks default to continuation entries at the line; flips require the precursor set (top/chop formation at flattening 200, capitulation extension + V-reversal, or aging stress escalation).

## Window Log

<!-- Per window: window id/date-range, chart file if saved, raw observations, prior updates (new/strengthened/weakened/killed), open questions -->

### W1 — HYPE 4H, ~Jan 28 – Apr 17 (2026-07-20)

Chart: `w1_hype_4h_jan-apr.png`

Observations:

- Late Jan–Feb 22: chop 23–28 around flat 200 EMA, frequent fill flips, no tradeable structure.
- Feb 22–23: decisive loss of 200 EMA; red regime opens, persistent downtrend ~24 → ~12.5 through March.
- Mid/late March: countertrend rally ~12.5 → ~17 into underside of declining 200 EMA (red pocket nearly pinches closed ~Mar 24–26); rejected; final leg down to ~9.3 low ~Apr 7. Exemplar short-continuation sequence.
- Apr 7–10: capitulation low, V-reversal, reclaim of both EMAs, fill flips green; lows ride above rising 10 EMA_low up to ~17 through window end.

Prior updates: P1–P4 opened (all low confidence, single window, full hindsight).

### W2 — HYPE 4H, ~Apr 5 – Jun 28 (2026-07-20)

Chart: `w2_hype_4h_apr-jun.png` (directly right of W1, slight overlap at the Apr low)

Observations:

- Apr 7–12: capitulation low ~9.3; 10 EMA_low reclaimed ~11–12, 200 EMA reclaimed ~14.5 (fill flips green). Flip-timing note: 10-low reclaim entered ~20% cheaper than 200 reclaim here, less confirmed.
- Mid-Apr → mid-Jun: clean stair-step uptrend ~15 → ~43; lows ride the rising 10 EMA_low; pullbacks tag it and resume. Uptrend much smoother than W1's jagged downtrend — directional behavior asymmetry is a theme.
- Late May: pullback ~37 → ~31 pierced 10 EMA_low, held well above 200.
- Mid-Jun (~20–23): pullback ~43 → ~33 briefly undercut the rising 200 EMA (small red fill flicker), reclaimed within a few bars, resumed to new local highs into window end (~39.8).

Prior updates: P1 low→medium with confirmation refinement (Apr-real vs Jun-noise discriminating pair). P2 low→medium (long-side mirror confirmed). P3 untested. P4 recast — strict trail weakened, pullback-zone role strengthened. P5 opened (trend persistence / hold-the-middle economics).

### W3 — HYPE 4H, ~Jun 15 – Sep 26 (2026-07-20)

Chart: `w3_hype_4h_jun-sep.png` (directly right of W2)

Observations:

- Late Jun → mid-Jul: trend resumes ~40 → ~52; late-Jul pullback tags rising 200 (~44) and holds (P2 long continuation).
- Early Aug: real breakdown — ~1 week red pocket, low ~36 (well below the 200), then full reclaim and rally to ~52 by mid-Aug. Kills dwell-time confirmation. Exit-design evidence: break short had ~15% open excursion, reclaim-only exit surrendered it (→ P6).
- Late Aug: chop across flattening 200, repeated fill flips — first live P3 condition since Feb; filter would have avoided whipsaw.
- Sep: final leg ~44 → ~57–58 peak (Sep 17–19), then fast steep break through the 200 (~49) to ~41 at window edge. Unresolved at window end.

Prior updates: P1 revised (dwell and slope forms dead; structural-precursor discriminator adopted). P2 → medium-high. P3 → medium. P4 held. P5 → medium with aging signature. P6 opened.

**Pre-registered W4 prediction (made before seeing W4):** the late-Sep break is REAL (or at least much deeper than the Jun/Aug fakes). Reasoning: rising 200-stress frequency through W3 (aging regime) + price accelerating away from the line within days, unlike the fakes which stalled under it. If W4 shows a quick reclaim, the structural-precursor discriminator takes a serious hit — grade honestly.

### W4 — HYPE 4H, ~Sep 21 – Dec 27 (2026-07-20)

Chart: `w4_hype_4h_sep-dec.png` (directly right of W3)

**Prediction grade: CORRECT.** Sep break was real — ~3-month downtrend, ~56 → ~22 low (≈ −60%). First out-of-sample win for the structural-precursor discriminator.

Observations:

- Early Oct: counter-rally to ~50 into the underside of the falling 200, rejected — textbook P2 short continuation (March-in-W1 shape).
- Oct 10–11: violent flash-crash wick to ~21, instant recovery to mid-30s. Lessons: extensions mean-revert fast (P6); regime/stop logic must be close-based, not wick-based (P8 opened).
- Late Oct: sharp rally to ~47, brief green fill flip near the falling 200, hard rejection — short-side mirror of the Jun/Aug fakes. Fake taxonomy now symmetric: single sharp counter-move against a healthy trend that never accelerates through the line.
- Nov → mid-Dec: grind down ~44 → ~22 (low ~Dec 17–18); counter-bounces reject below the 200 throughout.
- Window edge: price ~26 above reclaimed 10 EMA_low (~25.4), still below falling 200 (~28.8). Unresolved.

Prior updates: P1 → medium-high (discriminator scored). P2 → high (two more 200-underside rejection entries). P6 → medium. P7 opened (directional asymmetry, promoted from running theme). P8 opened (close-based logic).

**Pre-registered W5 prediction (made before seeing W5):** the first approach to the ~28–29 200-zone REJECTS. Analog pair: March grind-up-to-the-line (fake, new lows followed) vs April violent V through both lines (real). Current bounce (22 → 26.5, grinding) matches the March shape, not the April shape. A real long flip in W5 requires either a power move through both lines or a higher-low retest above ~22 first. Moderate confidence; the −60% decline magnitude suggests a bottoming process may be starting even if the first tag rejects.

### W5 — HYPE 4H, ~Jan 1 – Apr 12 2026 (2026-07-20)

Chart: `w5_hype_4h_jan-apr2026.png` (directly right of W4)

**Prediction grade: CORRECT (both parts).** Early-to-mid Jan grind into the 26–29 zone rejected below the falling 200 → new low ~20.5–21 (Jan ~21, undercutting Dec's ~22) → real flip arrived Jan 25–26 as a violent V powering through both lines (the specified April-analog form). Grind-vs-V discriminator confirmed out-of-sample. Pre-registered predictions now 2-for-2.

Observations:

- Early Feb: spike to ~38, then near-full giveback — deep multi-week retest into and briefly below the 200 (late Feb, red flickers ~26–27) before trend resumed. First young-trend fake in sample: flip-confirmation must tolerate a deep post-flip retest; first close back below the 200 does not un-flip regime. Also more P6 extension-partial evidence.
- March: rally ~28 → ~44–45 peak (~Mar 20).
- Early Apr: pullback tagged rising 200 (~37), held, resumed — P2 now six-for-six across both directions.
- Window end: green regime, price ~43, 10 EMA_low ~41, 200 ~37.1.

Prior updates: P1 grind-vs-V confirmation scored; young-trend retest nuance added. P2, P6 further supported. Candidate rule skeleton v0 promoted.

**W6 leakage disclosure:** the chart's live price label (~62.4, visible on W3–W5 screenshots) reveals HYPE trades near ~62 at present — the uptrend broadly continues into July. No clean W6 prediction is possible; W6 review will be observational only. W4/W5 gradings were unaffected (label not decodable into path, and both calls resolved within the shown windows).

### W6 — HYPE 4H, ~Apr 7 – Jun 8 2026 (2026-07-20)

Chart: `w6_hype_4h_apr-jun2026.png` (directly right of W5; price label removed by Destin after leak)

Observations:

- Apr → mid-May: digestion — grind to ~46, then a month of chop 39–45 with repeated small 200-stress flickers (Apr 22, ~May 1, deepest May 13–15 dip below the line to ~38–39, V-reclaimed). Mid-May dip added to the fake ledger (sharp counter-move, no acceleration away, quick close-based reclaim).
- May 16 → Jun 4: character change — parabolic leg ~46 → ~75–76; at peak, ~50% extension above the 200, largest extension in dataset either direction.
- Jun 5–8: violent break, −27% in ~4 days, ~76 → ~55–56, fill flips red at window edge (200 ~57.6). Unresolved.
- Rule-set behavior at edge: R1 does NOT flip short (no structural precursor — no top chop, no aging stress; healthy trend straight into parabola). Long book per R2 waits for close-based reclaim, no knife-catch after a break this violent.

Prior updates: P7 refined (smoothness is early/mid-phase property; late legs can go parabolic — first partial contradiction in sample). P6 strengthened (extension partials at parabolic extremes carry most of the leg's P&L; reclaim-only exits give back 20+ points).

**Pre-registered W7 path call (CONTAMINATED — endpoint ~62 known from label leak; Destin hints path is surprising):** predict a deeper flush first — meaningful time below the 200, plausibly into ~45–52, so the hold-at-the-line long entry fails and only the later close-based reclaim works, recovering to ~62 by mid-July. Wrong if price bounces cleanly off ~56 and grinds back up (in which case the simple 200-hold entry was right). Gradeable on shape despite endpoint contamination.

### W7 — HYPE 4H (Bybit perp), ~May 28 – Jul 20 2026 (2026-07-20) — FINAL WINDOW

Chart: `w7_hype_4h_jun-jul2026.png`

**Path call grade: INCORRECT.** The June break held at/above the rising 200 (~54–55); the predicted 45–52 flush never came. Price V-rallied back to ~77–78 (double top vs early June). The knife-catch at the still-rising 200 was the right trade. Root cause of the miss: over-weighted the break's violence; my own P1 taxonomy (no structural precursor → fake) had it right. Lesson: when gut and rule set disagree, trust the graded rule set. Pre-registered record: 2-for-3 clean, plus this contaminated miss.

Observations:

- Jun 7–10: break held the rising 200, V-rally to ~77–78 by Jun 16 (double top with early Jun).
- Mid-Jun → mid-Jul: regime aging in real time — lower highs (~73 Jul 4–7, then ~70), three 200-stress events in six weeks (Jun 7–10, Jun 20–22, Jul 16–18), 200 flattening. The Feb/Sep-2025 top-formation signature at larger scale (P5 aging validated again).
- Jul 16–18: real break below the 200 (~65) to ~58–59; current bounce sits at the underside (~64.4), rejecting so far. Price ~62, above 10 EMA_low (~60.5), below the 200. Red regime at present.

**LIVE FORWARD CALL (2026-07-20, zero contamination — no future data exists):** per R1 the structural precursor exists this time (six-week top formation, escalating stress frequency, flattening 200) — unlike June. Call: this resolves as a REAL short regime unless price achieves a close-based reclaim of the ~64.5 zone. Current underside bounce is the R2 short continuation entry; invalidation = close-based 200 reclaim. To be graded against live data in coming weeks.

Prior updates: P1 vindicated against my own drift (June violence-without-precursor was a fake). P2 supported again (rising-200 hold in June). P5 aging signature confirmed live. No prior contradicted by W7 except the already-graded path call.

## Free Design Parameters

Destin confirmed (post-W1) these are agent design choices, not hidden constraints of his hand-traded system — he is deliberately withholding his own answers to avoid shaping priors. Resolve empirically at codification/backtest time:

- Initial regime break: tradeable if desired, or pullback-only (P2 variant).
- Exit mechanics: extension-based take-profit, cover on reclaim, or any % combination.
- Regime-flip entry timing: 200 EMA reclaim or 10 EMA_low reclaim.
- Extension bands: available on request as a chart overlay, declined for now to keep the blind read clean; extension measure to be defined from data (e.g. ATR or % distance from 200 EMA) if extension exits survive as a candidate rule.

## Scope Notes

- Both directions in scope (Destin: "definitely long or short").

## Codification (2026-07-20)

Rules v1 implemented as backtest strategy `ema_px_trend` in `mm_v04/backend/app/backtest/strategies/ema_px_trend.py` (registered; params/config schemas exposed via the standard registry, canonical V2 position pipeline).

Rule → parameter mapping:

- R1 regime/flip: `accel_atr_mult` (accelerated close beyond the 200), precursors `stress_window`/`stress_flip_min` (cross-frequency stress) OR `capitulation_pct`/`capitulation_lookback` (old-side extension extreme, pct-based to separate Apr/Jan capitulations ~26–35% from ordinary trend extensions ~15%).
- R2 continuation: full size restored when `|ext_atr| <= reentry_ext_atr` (near-line touch that survives).
- R3 chop gate: `chop_slope_atr` + `chop_stress_min`, auto-released when `|ext_atr| >= accel_atr_mult`.
- R4 exits: `partial_ext_atr`/`partial_frac` profit-side reduction with hysteresis; regime exit only via confirmed opposite flip. Close-based throughout (P8); wicks only affect ATR.
- R5 asymmetry: config `long_size_frac`/`short_size_frac`.

Verification: 14 focused unit tests incl. negative paths (fake counter-cross no-flip, unaccelerated cross never flips, wrong-side capitulation rejected, hysteresis, NaN no-op, param-ordering validation) — all passing; mypy/ruff clean on new files. Dev set: HYPE 4H; real OOS = other assets/timeframes via Research MCP after Destin's backtest run.

## Write Log

- 2026-07-20: Doc created ahead of window 1. Setup, goal, and discipline recorded; no observations yet.
- 2026-07-20: W1 logged (HYPE 4H ~Jan 28–Apr 17). Priors P1–P4 opened at low confidence. Scope confirmed long+short.
- 2026-07-20: W1 open questions reframed as free design parameters per Destin (entry/exit/flip-timing variants are agent choices, resolved by backtest). Extension-band overlay declined to preserve blind read.
- 2026-07-20: W2 logged (HYPE 4H ~Apr 5–Jun 28). P1/P2 → medium, P4 recast, P5 opened.
- 2026-07-20: W3 logged (HYPE 4H ~Jun 15–Sep 26). P1 confirmation revised to structural-precursor form; P6 opened (extension partials); W4 prediction pre-registered (Sep break = real).
- 2026-07-20: W4 logged (HYPE 4H ~Sep 21–Dec 27). W4 prediction graded CORRECT. P1 → med-high, P2 → high, P7 (asymmetry) and P8 (close-based logic) opened. W5 prediction pre-registered (first 200 tag rejects).
- 2026-07-20: W5 logged (HYPE 4H ~Jan 1–Apr 12 2026). W5 prediction graded CORRECT (2-for-2). Young-trend retest nuance added to P1. Candidate rule skeleton v0 promoted. W6 endpoint leakage disclosed (live price label ~62).
- 2026-07-20: W6 logged (HYPE 4H ~Apr 7–Jun 8 2026). P7 phase-refined (first partial contradiction); P6 strengthened at parabolic extremes. Contaminated W7 path call pre-registered (deeper flush below 200 before reclaim to ~62).
- 2026-07-20: W7 logged (final window, ~May 28–Jul 20 2026). Path call graded INCORRECT (over-weighted violence; P1 taxonomy had it right). Rules promoted to v1, codification-ready. Live forward call registered: current setup = real short flip unless close-based reclaim of ~64.5.
- 2026-07-20: Rules v1 codified as `ema_px_trend` backtest strategy with focused unit tests; awaiting Destin's backtest manager run on HYPE 4H dev set.
- 2026-07-21: First backtest ran first try with **positive Sharpe** (metrics live in Destin's backtest UI). Companion strategy doc created: [[strategy_ema_px_trend]]. Destin confirms room for improvement; v2 candidates listed there. Live forward call (short flip unless ~64.5 reclaim) still open/ungraded.
