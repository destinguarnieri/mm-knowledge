# Trading Catalog Implementation and Evaluation Queue

Status: in progress

Source glossary: [[trading/catalog_v1|Trading Catalog]]. Execution owner: [Linear MON-169](https://linear.app/money-machine/issue/MON-169/convert-the-trading-catalog-into-an-implementation-and-evaluation).

## Contract

This page converts Destin's catalog into agent-pull units without changing the source wording or claiming that a listed item is alpha. Source maturity is copied or conservatively inferred from explicit phrases such as `WIP`, `propose`, `observation`, `heuristic`, or `formula forgotten`; it is not upgraded here.

For an underspecified item, an agent may recommend and implement the smallest conventional measurement as a **provisional first pass**. That measurement must receive Destin's semantic review before it is treated as faithful, economically evaluated, or usable in a composed strategy. Candidate uses below are routing context only. Combining primitives, including the Price Reversal System, requires an explicit system hypothesis and protected evaluation.

Implementation evidence vocabulary:

- `implemented`: code matches the stated primitive closely enough for correctness/evaluation work;
- `partial`: only part of the stated behavior exists;
- `related only`: nearby code must not be treated as semantic equivalence;
- `data only`: raw data exists but the catalog feature does not;
- `none found`: no matching code was found in the August 2026 audit.

Queue states are `captured`, `needs specification`, `ready`, `in progress`, `blocked`, `evaluated`, and `rejected`. `Evaluated` means a bounded test occurred; it does not mean promoted alpha.

## Pull index

| ID | Item | Primary type | Queue state | Gate / smallest pull |
|---|---|---|---|---|
| CAT-001 | High Low Channel | market-state feature | needs specification | Provisional channel definition, then Destin review |
| CAT-002 | High/Low Channel slope disagreement | market-state feature | ready | Lock deterministic slope/disagreement fixtures |
| CAT-003 | 200 EMA | indicator | ready | Fixed-series parity test |
| CAT-004 | Moving Average Crossing | signal | evaluated | Continue within EMA 10/200 program |
| CAT-005 | MA Ribbon | market-state feature | ready | Emit stack and adjacent spreads |
| CAT-006 | VWAP | indicator | evaluated | Standalone RVWAP fixture parity |
| CAT-007 | VFTI | forecast input | ready | Return-blind series audit |
| CAT-008 | PX measurement | indicator | evaluated | Preserve existing evidence |
| CAT-009 | PX sizing | position/control mechanism | ready | One explicit mapping per hypothesis |
| CAT-010 | Slope and R² | market-state feature | ready | Deterministic OLS fixtures |
| CAT-011 | RSI | signal | needs specification | Provisional source choice, then Destin review |
| CAT-012 | ROC | forecast input | ready | Formula/warmup fixtures |
| CAT-013 | Price Reversal System | strategy concept | needs specification | Review system lifecycle after component measures |
| CAT-014 | PRI | signal | ready | Direct three-condition truth table |
| CAT-015 | PRL | market-state feature | needs specification | Provisional level lifecycle, then Destin review |
| CAT-016 | PRZ | market-state feature | needs specification | Provisional zone bounds, then Destin review |
| CAT-017 | PRB | signal | blocked | Depends on reviewed PRL/PRZ break semantics |
| CAT-018 | Volume Ratio | market-state feature | ready | Formula, dispersion, and causality tests |
| CAT-019 | Volume Anomaly | signal | ready | Location-conditioned event measurement |
| CAT-020 | ATR Ratio | market-state feature | needs specification | Provisional ATR/baseline windows, then review |
| CAT-021 | ATR Anomaly | signal | needs specification | Depends on reviewed ATR Ratio |
| CAT-022 | Volume Delta Anomaly | signal | blocked | Needs signed trade-flow history and definition |
| CAT-023 | Trade Speed | execution feature | ready | Ratio/anomaly over candle trade count |
| CAT-024 | Absorption | signal | needs specification | Compare wick measures, then Destin review |
| CAT-025 | Candle Strength | indicator | needs specification | Provisional close-location measure, then review |
| CAT-026 | Order Book Imbalance | execution feature | blocked | Needs causal L2 capture/replay |
| CAT-027 | Combined Signal | signal | needs specification | Freeze transforms, weights, polarity, alignment |
| CAT-028 | Multi Time Frames | market-state feature | needs specification | Causal closed-bar alignment contract |
| CAT-029 | EMA MAXI | market-state feature | blocked | Depends on reviewed MTF alignment |
| CAT-030 | MTF Ribbon | market-state feature | blocked | Depends on reviewed MTF alignment |
| CAT-031 | Volatility Scores | market-state feature | needs specification | Provisional standard/blend/ratio measures |
| CAT-032 | Funding Rates | forecast input | blocked | Needs timestamped funding history |
| CAT-033 | POC_MA | indicator | needs specification | Recommend provisional measurement, then review |
| CAT-034 | POC_BREAKER | signal | blocked | Depends on POC_MA and break semantics |
| CAT-035 | ATR Breaker | signal | needs specification | Recommend provisional measurement, then review |
| CAT-036 | Scaling In and Out | position/control mechanism | in progress | Owned by MON-168 schedule semantics |
| CAT-037 | Pop it, dunk it | strategy concept | captured | State-transition fixture before code |
| CAT-038 | 123 | position/control mechanism | needs specification | Specify tranche/profit sequencing |
| CAT-039 | Smash n Scale | execution feature | needs specification | Specify market/limit lifecycle |
| CAT-040 | Buy n Bid | execution feature | needs specification | Specify repricing/cancel lifecycle |
| CAT-041 | Ride the Wave | execution feature | needs specification | Specify grid and risk bounds |
| CAT-042 | Opposite Only | strategy concept | needs specification | Specify trend and in-money exit semantics |

## Queue records

### CAT-001 — High Low Channel

- **Source maturity:** Core concept plus observations; exact construction is not stated.
- **Type:** market-state feature.
- **Implementation:** `related only` — `mm_v04/backend/app/lib/indicators/slope.py` has `HL_Slope`; `backend/app/backtest/strategies/n_bar_breakout.py` is a related breakout, not proof of the catalog channel.
- **First pass:** Recommend rolling high and rolling low over one caller-supplied lookback, with close classified `above`, `inside`, or `below`; test boundary equality, transitions, warmup, and prefix causality.
- **Gate/dependencies:** Destin reviews rolling extrema versus EMA(high)/EMA(low), period, close versus intrabar classification, and break semantics before faithfulness/economic evaluation.
- **Candidate uses:** breakout, fall-back-inside, range state, MA/PX landscape. **State:** needs specification.

### CAT-002 — High/Low Channel slope disagreement

- **Source maturity:** Described as a useful second-derivative study.
- **Type:** market-state feature.
- **Implementation:** `partial` — `mm_v04/backend/app/lib/indicators/slope.py::HL_Slope` and indicator-engine emission exist; focused correctness tests do not.
- **First pass:** Lock high-slope, low-slope, spread, and sign-disagreement outputs on deterministic rising/falling/diverging fixtures with R² and causality checks.
- **Gate/dependencies:** Uses the reviewed channel/source definition from CAT-001 for a faithful catalog claim.
- **Candidate uses:** trend quality, compression/expansion, breakout regime. **State:** ready.

### CAT-003 — 200 EMA

- **Source maturity:** Established, widely used starting input; not claimed sufficient alone.
- **Type:** indicator.
- **Implementation:** `implemented` — `mm_v04/backend/app/lib/indicators/ema_padded.py`; explicit consumers include `backend/app/services/markets/market_technical_snapshot_service.py` and EMA strategies.
- **First pass:** Add or identify fixed-series EMA-200 parity, warmup, source-selection, and prefix-causality evidence.
- **Gate/dependencies:** EMA is the catalog default convention except VWAP; the convention itself is queue metadata, not a primitive.
- **Candidate uses:** long-term trend side, crossings, ribbons, PX. **State:** ready.

### CAT-004 — Moving Average Crossing

- **Source maturity:** Preferred 10/200 framing; 10 EMA low is preferred in practice and symmetry remains context-dependent.
- **Type:** signal.
- **Implementation:** `implemented` — `mm_v04/backend/app/lib/indicators/emac.py`, `backend/app/lib/signals/emac.py`, and registered EMAC strategies; tests include `backend/tests/backtest/test_emac_cross.py` and related EMA suites.
- **First pass:** No new primitive build. Continue exact mechanism/economic work inside the existing EMA 10/200 program using auditable windows.
- **Gate/dependencies:** Any canonical high/low source symmetry belongs to the named strategy hypothesis, not generic cross math.
- **Candidate uses:** opportunity framing, trend state, expansion/contraction. **State:** evaluated.

### CAT-005 — MA Ribbon

- **Source maturity:** Proposed five-EMA tool with observations and several possible uses.
- **Type:** market-state feature.
- **Implementation:** `none found` for the catalog `[10,20,50,100,200]` ribbon; generic EMA exists.
- **First pass:** Emit the five causal series, ordinal stack state, entanglement/ties, and normalized adjacent spreads for `10/20`, `20/50`, `50/100`, `100/200`; test ordered, entangled, crossing, expanding, and contracting fixtures.
- **Gate/dependencies:** Destin reviews whether these measurements capture “stacked,” “entangled,” and “cleared” before any trade mapping.
- **Candidate uses:** multi-horizon trend state and later band-to-band hypotheses. **State:** ready.

### CAT-006 — VWAP

- **Source maturity:** General indicator with trend/mean-reversion observations; current mapping evidence is maintained separately.
- **Type:** indicator.
- **Implementation:** `implemented` — `mm_v04/backend/app/lib/indicators/rvwap.py` with many PX/VWAP strategies and event studies under `backend/app/lib/analysis/event_study/vwap_band/`.
- **First pass:** Add standalone fixed/adaptive-window RVWAP fixture parity if absent; do not create another strategy here.
- **Gate/dependencies:** Trend versus mean-reversion use of slope remains a hypothesis, not primitive correctness.
- **Candidate uses:** location, PX, mean-reversion/trend programs. **State:** evaluated.

### CAT-007 — VFTI

- **Source maturity:** Leading-price claim explicitly marked “should be verified.”
- **Type:** forecast input.
- **Implementation:** `implemented` — `mm_v04/backend/app/lib/indicators/vfti.py`, registered `backend/app/backtest/strategies/vfti.py`; direct tests in `backend/tests/indicator/test_vfti.py`.
- **First pass:** Return-blind series/chart audit of sign and turns, followed by a preregistered forward-response event study rather than immediate strategy mapping.
- **Gate/dependencies:** Destin reviews whether the emitted measure matches intended participant flow before economic use.
- **Candidate uses:** price confirmation/rebuke and VWAP readiness. **State:** ready.

### CAT-008 — PX measurement

- **Source maturity:** General-purpose distance/statistics primitive with explicit trend and mean-reversion uses.
- **Type:** indicator.
- **Implementation:** `implemented` — `mm_v04/backend/app/lib/indicators/price_extension.py`; direct tests under `backend/tests/indicator/test_price_extension_*` and extensive strategy/event-study evidence.
- **First pass:** Preserve existing correctness/evaluation evidence; any new band must state raw-price versus processed-signal domain and lookback.
- **Gate/dependencies:** None for the measurement primitive.
- **Candidate uses:** location, extension, levels, forecast inputs. **State:** evaluated.

### CAT-009 — PX sizing

- **Source maturity:** Explicit sizing concept; direction differs for trend versus mean reversion.
- **Type:** position/control mechanism.
- **Implementation:** `partial` — threshold and continuous mappings exist in `mm_v04/backend/app/backtest/strategies/px_threshold*.py`, but no mapping represents all catalog uses.
- **First pass:** Evaluate one frozen direction/domain/curve at a time against a named binary control; retain average-entry and path evidence.
- **Gate/dependencies:** Requires a separate strategy hypothesis; never infer the curve from CAT-008 correctness.
- **Candidate uses:** trend accumulation/distribution and mean-reversion exposure control. **State:** ready.

### CAT-010 — Slope and R²

- **Source maturity:** Classic indicator and proposed filter; inputs and lookbacks are contextual.
- **Type:** market-state feature.
- **Implementation:** `implemented` — `mm_v04/backend/app/lib/indicators/slope.py` plus slope strategies; focused primitive tests are incomplete.
- **First pass:** Deterministic OLS slope/R² tests for price, indicator, and signed signal, including constant, zero-crossing, and prefix-causal cases.
- **Gate/dependencies:** Destin reviews output meaning on representative charts before a gate is called faithful.
- **Candidate uses:** trade side, trend/mean-reversion regime, confidence filter. **State:** ready.

### CAT-011 — RSI

- **Source maturity:** Classic measure with several proposed uses and heuristic `±0.9` extremes.
- **Type:** signal.
- **Implementation:** `implemented` — `mm_v04/backend/app/lib/indicators/rsi.py::RSI_CENTER` maps to `[-1,1]`; current source is HL2, not conventional close; registered RSI strategy exists.
- **First pass:** Compare HL2 and close on fixed/reference fixtures and representative charts; test centering, warmup, and extremes.
- **Gate/dependencies:** Destin selects or accepts the source before faithfulness. Trend-from-zero and fade-on-leaving-extreme are separate hypotheses.
- **Candidate uses:** direction, exhaustion, VWAP readiness control. **State:** needs specification.

### CAT-012 — ROC

- **Source maturity:** Captured as a universal speed measurement; no fixed trading semantics.
- **Type:** forecast input.
- **Implementation:** `implemented` — `mm_v04/backend/app/lib/indicators/roc.py`; direct unit evidence is incomplete.
- **First pass:** Exact lag-percent, warmup, zero-denominator, sign, and causality tests, then horizon-separated forward-response measurement.
- **Gate/dependencies:** Destin reviews whether period/output scaling capture intended speed.
- **Candidate uses:** acceleration, composite inputs, regime state. **State:** ready.

### CAT-013 — Price Reversal System

- **Source maturity:** PRI, PRL, PRZ, and PRB are explicitly one discretionary or signalized system with immediate and delayed reaction types.
- **Type:** strategy concept.
- **Implementation:** `partial` — PRI and some level calculations exist across `mm_v04/backend/app/lib/signals/pri_v1.py` through `pri_v3.py`; no faithful persistent combined lifecycle exists.
- **First pass:** Evaluate CAT-014–017 individually for measurement correctness, then assemble one typed event lifecycle fixture: PRI print → PRL/PRZ creation → immediate follow-through or delayed retest → PRB invalidation/reversal.
- **Gate/dependencies:** Destin reviews every provisional component measurement and the combined state machine before economic evaluation. Component independence must not erase the intended system use.
- **Candidate uses:** standalone reversal/continuation system and entry trigger. **State:** needs specification.

### CAT-014 — PRI

- **Source maturity:** Exact three-condition bullish/bearish rule; color flip alone is explicitly noise.
- **Type:** signal.
- **Implementation:** `implemented` — `mm_v04/backend/app/lib/signals/pri_v3.py`; service integration exists, but direct truth-table coverage is incomplete.
- **First pass:** Test bullish/bearish reclaim, rejected color-only flip, equality, doji, missing data, and prefix causality.
- **Gate/dependencies:** Destin reviews event marks on representative candles before system use.
- **Candidate uses:** CAT-013 trigger, reversal, continuation. **State:** ready.

### CAT-015 — PRL

- **Source maturity:** Signal candle open and extreme are described as levels that often retest; lifecycle is unstated.
- **Type:** market-state feature.
- **Implementation:** `partial` — level calculations appear in `mm_v04/backend/app/lib/signals/pri_v1.py` and `pri_v2.py`; no persistent lifecycle.
- **First pass:** Recommend typed bullish `{open, low}` and bearish `{open, high}` levels tied to the PRI event, retained until superseded, broken, or a configurable expiry; test price identity and state transitions.
- **Gate/dependencies:** Destin reviews retention, supersession, expiry, and what constitutes a retest before faithfulness.
- **Candidate uses:** CAT-013 retest location and targets. **State:** needs specification.

### CAT-016 — PRZ

- **Source maturity:** “OLHC levels form the Price Reversal Zone”; exact bounds are not executable.
- **Type:** market-state feature.
- **Implementation:** `none found`.
- **First pass:** Recommend a provisional interval spanning the reviewed PRL open and extreme, while retaining all signal-candle OHLC as named levels; test membership, direction, and boundary equality.
- **Gate/dependencies:** Destin confirms which OHLC bounds form one or more zones before faithfulness.
- **Candidate uses:** CAT-013 absorption, weakness target, profit-taking area. **State:** needs specification.

### CAT-017 — PRB

- **Source maturity:** A PRL break invalidates the signal and implies reversal; exact break/confirmation is unstated.
- **Type:** signal.
- **Implementation:** `none found`.
- **First pass:** After CAT-015/016 review, recommend close-through invalidation as the conservative provisional event; test wick-only non-break, equality, confirmed close break, and one-shot transition.
- **Gate/dependencies:** Destin confirms wick versus close, invalidating boundary, and immediate versus confirmed reverse implication.
- **Candidate uses:** CAT-013 invalidation and reversal transition. **State:** blocked.

### CAT-018 — Volume Ratio

- **Source maturity:** Formula is explicit; dispersion interpretation is proposed.
- **Type:** market-state feature.
- **Implementation:** `partial` — `mm_v04/backend/app/lib/indicators/volume_anomalies.py` computes volume/EMA(volume), but catalog ratio dispersion is absent.
- **First pass:** Test exact EMA ratio, zero/NaN behavior, warmup, rolling standard deviation of the ratio, and prefix causality.
- **Gate/dependencies:** Destin reviews baseline window and dispersion chart before semantic acceptance.
- **Candidate uses:** participation state and CAT-019 context. **State:** ready.

### CAT-019 — Volume Anomaly

- **Source maturity:** `2–3` acceleration and `4+` reversal heuristics are explicitly asset/timeframe dependent.
- **Type:** signal.
- **Implementation:** `partial` — `volume_anomalies.py` emits ratio/z-score; location conditioning and event OHLC lifecycle are absent.
- **First pass:** Measure ratio quantile plus rolling-range location, candle direction, forward return, and retained OHLC without hard-coding heuristic thresholds as truth.
- **Gate/dependencies:** Destin reviews whether the measurement separates accelerant versus exhaustion intent.
- **Candidate uses:** risk reduction, exhaustion, acceleration qualifier. **State:** ready.

### CAT-020 — ATR Ratio

- **Source maturity:** Formula is explicit at a high level; exact current ATR and baseline windows are not.
- **Type:** market-state feature.
- **Implementation:** `partial` — `mm_v04/backend/app/lib/indicators/atr_anomaly.py` computes ATR(1)/ATR(length), not clearly ATR/EMA(ATR).
- **First pass:** Recommend ATR(14)/EMA(ATR(14),100) plus rolling ratio dispersion as a provisional measurement; compare with current implementation on fixtures and charts.
- **Gate/dependencies:** Destin reviews ATR period and EMA baseline before faithfulness.
- **Candidate uses:** compression/expansion, sizing, execution regime. **State:** needs specification.

### CAT-021 — ATR Anomaly

- **Source maturity:** `4+` is a candidate trigger; reversal/re-entry language is heuristic.
- **Type:** signal.
- **Implementation:** `partial` through `atr_anomaly.py`; event OHLC lifecycle is absent.
- **First pass:** After CAT-020 review, measure ratio quantile, forward retracement/continuation, and retained OHLC by asset/timeframe.
- **Gate/dependencies:** Reviewed CAT-020 identity; do not encode mandatory close/re-entry policy from the heuristic.
- **Candidate uses:** risk reduction, reversal context, volatility shock. **State:** needs specification.

### CAT-022 — Volume Delta Anomaly

- **Source maturity:** Directional-disagreement examples are given; per-bar delta versus cumulative CVD is ambiguous.
- **Type:** signal.
- **Implementation:** `none found`; candle series lack signed flow history despite trade DTOs.
- **First pass:** Once data exists, compare candle direction with signed aggressive per-bar delta and separately with CVD change; test alignment and no-lookahead.
- **Gate/dependencies:** Trustworthy historical signed trades; Destin selects delta/CVD identity after visual review.
- **Candidate uses:** reversal, profit-taking, acceleration confirmation. **State:** blocked.

### CAT-023 — Trade Speed

- **Source maturity:** Measurement is explicit as number of trades per bar; signal/anomaly/urgency uses are proposed.
- **Type:** execution feature.
- **Implementation:** `data only` — candle trade count `n` exists in `mm_v04/backend/app/data_models/dto/timeseries.py`; no feature consumes it.
- **First pass:** Emit raw trades/bar, trades-per-second, and current/EMA ratio with zero/warmup/causality fixtures; compare against volume on representative charts.
- **Gate/dependencies:** Destin reviews which measure captures intended speed before anomaly or urgency policy.
- **Candidate uses:** participation, hidden slicing clues, entry/exit urgency, adverse-selection avoidance. **State:** ready.

### CAT-024 — Absorption

- **Source maturity:** Explicitly WIP; described as candle-body amount that is wick.
- **Type:** signal.
- **Implementation:** `partial` — `mm_v04/backend/app/lib/indicators/absorption.py` emits several wick/body/range measures; Indicator Lab consumes a subset.
- **First pass:** Present wick/range, wick/body, directional wick imbalance, and doji-safe behavior side-by-side on fixtures and charts.
- **Gate/dependencies:** Destin selects the intended measure and event threshold before correctness/economic evaluation.
- **Candidate uses:** reversal, exhaustion, minimum position reduction. **State:** needs specification.

### CAT-025 — Candle Strength

- **Source maturity:** Explicitly WIP; close proximity is the only confirmed core input.
- **Type:** indicator.
- **Implementation:** `related only` — a `CSI` DTO exists in `mm_v04/backend/app/data_models/dto/indicators.py`; no matching calculator/consumer was found.
- **First pass:** Recommend signed close-location value `2*(close-low)/(high-low)-1`, with zero-range behavior, before adding volume/range/composite factors.
- **Gate/dependencies:** Destin reviews the first-pass chart output and specifies any additional factors, weights, normalization, or lookback.
- **Candidate uses:** bar quality and directional confirmation. **State:** needs specification.

### CAT-026 — Order Book Imbalance

- **Source maturity:** Conceptual participant-intention claim; no depth/normalization contract.
- **Type:** execution feature.
- **Implementation:** `data only` — websocket book DTOs exist in `mm_v04/backend/app/data_models/dto/hyperliquid.py`; no causal capture/replay feature exists.
- **First pass:** After L2 replay exists, compare top-of-book and fixed-bps depth imbalance with timestamp/staleness metadata.
- **Gate/dependencies:** Causal L2 capture/replay; Destin reviews depth horizon and intended interpretation.
- **Candidate uses:** inventory intention, readiness, execution context. **State:** blocked.

### CAT-027 — Combined Signal

- **Source maturity:** `sig_current` and order-book `sig_v2` formulas are captured as additions, without weights/transforms.
- **Type:** signal.
- **Implementation:** `partial` — generic combination exists in `mm_v04/backend/app/lib/signals/combo_v1.py`; Indicator Lab uses a related equal-weight combination, not an accepted catalog implementation.
- **First pass:** Freeze component versions, transforms, lookbacks, polarity, missing-data behavior, alignment, and provisional equal weights; prove deterministic component parity.
- **Gate/dependencies:** Destin reviews the combined series before any claim of intended capture; CAT-026 blocks `sig_v2`.
- **Candidate uses:** multi-signal state/forecast baseline under a separate hypothesis. **State:** needs specification.

### CAT-028 — Multi Time Frames

- **Source maturity:** General compositing concept with examples; exact synchronization is unstated.
- **Type:** market-state feature.
- **Implementation:** `related only` — live higher-timeframe rollups exist in `mm_v04/backend/app/services/data/data_servicev2.py`, but backtests lack a canonical causal cross-timeframe join.
- **First pass:** Specify last-fully-closed higher-timeframe projection onto lower bars with timezone/session, gap, warmup, and no-lookahead fixtures.
- **Gate/dependencies:** Destin reviews projected levels on charts before feature use.
- **Candidate uses:** cross-horizon support/resistance and composite state. **State:** needs specification.

### CAT-029 — EMA MAXI

- **Source maturity:** Current 5m day-trading setup with five explicit higher/lower-timeframe EMAs.
- **Type:** market-state feature.
- **Implementation:** `none found` for the stated stack.
- **First pass:** After CAT-028, emit the exact `200 EMA 1D`, `200 EMA 4H`, `10 EMA low 4H`, `10 EMA high 4H`, and `200 EMA 5m` projections without trading logic.
- **Gate/dependencies:** Reviewed MTF alignment; Destin reviews the five plotted series and state representation.
- **Candidate uses:** multi-horizon landscape and later discretionary codification. **State:** blocked.

### CAT-030 — MTF Ribbon

- **Source maturity:** Proposed extension of MA Ribbon and MTF with band-to-band use.
- **Type:** market-state feature.
- **Implementation:** `none found`.
- **First pass:** After CAT-028, emit a configurable set of higher-timeframe 200 EMAs projected onto one lower timeframe, plus ordering and band distances.
- **Gate/dependencies:** Reviewed timeframe set/alignment; band-to-band trading remains a separate strategy hypothesis.
- **Candidate uses:** cross-timeframe support/resistance landscape. **State:** blocked.

### CAT-031 — Volatility Scores

- **Source maturity:** Standard deviation is recommended; blend/ratio formulas are examples and possible alpha, not settled identities.
- **Type:** market-state feature.
- **Implementation:** `partial` — `mm_v04/backend/app/lib/utils/vol_score.py`, `volatility_ewma.py`, multi-speed EWMAC, and asset-weight analysis contain related but different measures.
- **First pass:** Present standard annualized return volatility, the example `0.3*vol365 + 0.3*vol30 + 0.4*vol3`, and `vol3/vol30` on causal fixtures/charts.
- **Gate/dependencies:** Destin reviews spans, weights, return convention, and annualization before faithfulness or risk sizing.
- **Candidate uses:** cross-asset risk, current-versus-normal regime, position sizing. **State:** needs specification.

### CAT-032 — Funding Rates

- **Source maturity:** Participant-positioning intuition and sign-change idea; EV formula explicitly forgotten.
- **Type:** forecast input.
- **Implementation:** `data only` — current funding snapshot and user cumulative funding exist; no causal historical feature/backtest series.
- **First pass:** Once history exists, emit rate, sign, change, cumulative cost to next horizons, and price movement versus scheduled funding without reconstructing the forgotten formula.
- **Gate/dependencies:** Timestamped venue-specific funding history; Destin reviews horizon/settlement meaning.
- **Candidate uses:** participant positioning, directional/reversal context, carry-aware forecast. **State:** blocked.

### CAT-033 — POC_MA

- **Source maturity:** Name captured under Future Indi/Sig; no definition.
- **Type:** indicator.
- **Implementation:** `none found`.
- **First pass:** Recommend a provisional volume-profile point of control per completed window followed by an EMA of that POC series; expose both series and causal window boundaries.
- **Gate/dependencies:** Destin confirms whether POC means volume-profile POC, window/session, price bins, and EMA span after reviewing output.
- **Candidate uses:** participant value/level context. **State:** needs specification.

### CAT-034 — POC_BREAKER

- **Source maturity:** Name only under Future Indi/Sig.
- **Type:** signal.
- **Implementation:** `none found`.
- **First pass:** After CAT-033 review, recommend one-shot close-through/retest events around the accepted POC level and display them without trading.
- **Gate/dependencies:** Reviewed POC identity and Destin-defined break/retest/confirmation semantics.
- **Candidate uses:** level transition and continuation/reversal hypotheses. **State:** blocked.

### CAT-035 — ATR Breaker

- **Source maturity:** Name only under Future Indi/Sig.
- **Type:** signal.
- **Implementation:** `none found`.
- **First pass:** Recommend a provisional event when close displacement from a reviewed reference level exceeds `k * ATR`, emitting direction, distance, ATR multiple, and one-shot transition.
- **Gate/dependencies:** Destin confirms reference level, ATR identity, multiplier, wick/close, and reset semantics after visual review.
- **Candidate uses:** volatility-adjusted breakout/event detection. **State:** needs specification.

### CAT-036 — Scaling In and Scaling Out

- **Source maturity:** WIP in catalog; confirmed architecture lives in [[research/trading/positioning/size-distribution|Size Distribution]].
- **Type:** position/control mechanism.
- **Implementation:** `related only` — `mm_v04/backend/app/helpers/signal_position.py` and `backend/app/backtest/strategies/positions_lab.py` use rejected absolute-target semantics.
- **First pass:** Follow MON-168's pure concurrent bounded accumulation/distribution schedule, inventory, side, endpoint, and rounding fixtures before strategy wiring.
- **Gate/dependencies:** MON-168 and accepted size-distribution invariants.
- **Candidate uses:** path-aware inventory acquisition/release. **State:** in progress.

### CAT-037 — Pop it, dunk it

- **Source maturity:** Named trading style: full entry on trigger and full close on exit trigger.
- **Type:** strategy concept.
- **Implementation:** `related only` — binary strategies resemble it but are not a faithful named contract.
- **First pass:** Write a signal/position transition fixture covering flat→full, hold, full→flat/reverse, duplicate timestamps, and costs before code.
- **Gate/dependencies:** Requires a named entry/exit hypothesis; Destin reviews fixture behavior.
- **Candidate uses:** binary control for richer position policies. **State:** captured.

### CAT-038 — 123

- **Source maturity:** Market entry in thirds; later buys cost-average, with profitability required before full allocation.
- **Type:** position/control mechanism.
- **Implementation:** `none found` faithfully; related context at [[trading/entry/123|123]].
- **First pass:** Specify three tranche states, adverse/favorable path examples, maximum `2/3` wrong exposure, and the exact profitability gate for the final tranche.
- **Gate/dependencies:** Destin confirms sequencing, price anchors, reset, exit, and whether the second or third tranche carries the in-money requirement.
- **Candidate uses:** bounded staged entry. **State:** needs specification.

### CAT-039 — Smash n Scale

- **Source maturity:** Market chunk entry followed by a spread of limit sells.
- **Type:** execution feature.
- **Implementation:** `related only` — legacy/live scale-order code must not count as this style.
- **First pass:** Specify initial fraction, limit quantity/price schedule, partial fills, expiry/cancel-replace, and inventory cap in deterministic fixtures.
- **Gate/dependencies:** Destin reviews order lifecycle; any live wiring requires separate capital authorization.
- **Candidate uses:** immediate inventory plus passive distribution. **State:** needs specification.

### CAT-040 — Buy n Bid

- **Source maturity:** Market-enter `10–30%`, bid down to target, lift/replace limits as candles progress.
- **Type:** execution feature.
- **Implementation:** `related only`; no faithful tested contract found.
- **First pass:** Specify anchor/target updates, ladder quantities, lift conditions, cancel-replace atomicity, partial fills, and maximum inventory with an offline order-state fixture.
- **Gate/dependencies:** Destin reviews exact lifecycle; live wiring needs separate capital authorization.
- **Candidate uses:** favorable passive accumulation after initial entry. **State:** needs specification.

### CAT-041 — Ride the Wave

- **Source maturity:** Quote both sides with a grid while inventory remains only in trend direction.
- **Type:** execution feature.
- **Implementation:** `none found` faithfully.
- **First pass:** Specify trend input, two-sided quotes, one-sided inventory invariant, grid bounds, skew, fill handling, stop/flatten, and stale-order recovery in a simulator.
- **Gate/dependencies:** Destin reviews inventory/risk behavior; live wiring needs separate capital authorization.
- **Candidate uses:** trend-aligned market making. **State:** needs specification.

### CAT-042 — Opposite Only

- **Source maturity:** Buy only on candles opposite the trend; sell when in money and candle agrees with trend.
- **Type:** strategy concept.
- **Implementation:** `none found` faithfully.
- **First pass:** Freeze an external trend label and test candle-color entry eligibility plus average-entry profitability and trend-candle exit on deterministic paths.
- **Gate/dependencies:** Destin confirms trend definition, candle timing, in-money costs, scaling, and exit scope.
- **Candidate uses:** trend pullback entry and profit-aware release. **State:** needs specification.

## Agent pull rules

1. Pull only a `ready` record whose files, fixtures, and evidence window do not collide with another active agent.
2. Treat the listed first pass as a recommendation, not accepted semantics, whenever the record requires Destin review.
3. Separate measurement correctness, semantic acceptance, forecasting evidence, position policy, execution, and economics.
4. Create a Linear issue only when the bounded work passes the existing intake gate; this page is the inventory and does not require one issue per row.
5. Update the source record, [[research/trading/research_index|Research Board]], and Linear only when evidence materially changes state or dependency.
6. Never infer a combined strategy from candidate uses. The Price Reversal System is explicitly combined, but its component and full-system evaluations remain distinct.
