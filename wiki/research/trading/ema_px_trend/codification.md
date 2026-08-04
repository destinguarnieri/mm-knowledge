# EMA/PX Trend Continuation Codification

Status: in progress

Date opened: 2026-07-18

Maturity note (added 2026-07-25): the "Confirmed" headings below mean Destin described that behavior during the 2026-07-18 session. They do not mean the behavior is settled, audited, or ready to implement. Nothing on this page has behavioral parity. Treat the labeled fixtures as the durable asset here and the rule prose as a live working draft.

Purpose: running specification for transferring Destin's discretionary EMA/PX trend-continuation behavior into executable strategy logic. This page is provisional until both short and long mappings have chart-backed behavioral parity.

Related context: [[company/money-machine-360|Money Machine Operating Context]], [[trading/catalog_v1|Trading Catalog]], [[research/trading/emac-cross-10-200/emac-cross-10-200|EMA Cross 10/200 Research]].

## Source Strategy

This page currently covers the **short-side trend continuation / countertrend absorption** mapping and the first **long-side trend continuation** fixture shown on DOGE/BTC spread `4H` charts. The long-side fixture exposed possible inconsistency in rule application that must be audited before promotion to confirmed semantics.

Source screenshots:

- ![[Screenshot 2026-07-18 at 12.58.48 AM.png]]
- ![[Screenshot 2026-07-18 at 12.59.07 AM.png]]
- ![[Screenshot 2026-07-18 at 2.08.19 AM.png]]
- ![[Screenshot 2026-07-18 at 2.33.23 AM.png]]

The chart used:

- Instrument fixture: DOGE/BTC spread.
- Timeframe example: `4H`.
- Intended eventual scope: cross-asset and cross-timeframe behavior.
- Current fixture constraint: continue using DOGE/BTC until long, short, and failure cases are flushed out. Do not switch assets just to avoid the volatility and ugliness of being wrong on this pair.
- Execution approximation: candle close only. Limit orders are part of the discretionary behavior but are not available in the current backtest engine.
- Visible indicators for this mapping:
  - `10 EMA LOW_4H`.
  - `200 EMA close_4H`.
  - Asymmetric PX bands using `PX 10 Low 4H`, `STDDEV lookback=100`.
- Removed from this mapping for now: `200 EMA close_1D`; it was visible earlier but has not yet been used in the described rules.

## Side Asymmetry And Consistency Audit

Do not assume the long side is a mirror image of the short side. Also do not assume every difference in Destin's first-pass labels is intentional strategy asymmetry.

Discretionary "knowing when to break the rules" is not standard executable behavior. Treat it as one of:

- a human inconsistency to exclude from the deterministic mapping;
- two separate strategies being merged in one chart explanation;
- a valid second entry condition that needs its own explicit predicate and tests.

Do not implement flexible template-breaking as an implicit fallback.

Candidate inconsistency from the first long-side fixture:

- The long fixture labeled an entry before the `10 EMA low` crossed over the `200 EMA close`, while the short-side writeup used same-timeframe `10 EMA low < 200 EMA close` as short permission.
- This is not yet a confirmed long-side asymmetry. It may be:
  - an intentional early `123` exception around a determinate `200 EMA` level;
  - a labeling inconsistency;
  - a missing higher-level permission rule;
  - two separate entry strategies being merged;
  - or evidence that the short-side permission rule was stated too narrowly.
- The actual `10/200` bullish cross occurred after price was already extended; this may become a rule that late crosses are not entries when PX says price is outside the second standard-deviation band, but it still needs consistency review against other charts.
- Late-trend tolerance decay is plausible but still needs failure-case fixtures before being treated as executable.

## Confirmed Short-Side State Model

### Trend Permission

Short-side permission begins when the same-timeframe `10 EMA low` is below the same-timeframe `200 EMA close`.

Additional discretionary confidence comes from:

- price below / failing the `10 EMA low`;
- negative `10 EMA low` slope;
- failed retests of the `200 EMA close`;
- price compressing countertrend toward the `200 EMA` without invalidating the short attempt.

The `1D 200 EMA` is not part of the confirmed permission model yet.

### Entry Trigger

Primary close-only trigger:

- prior close is above the `10 EMA low`;
- current candle closes below the `10 EMA low`;
- same-timeframe `10 EMA low < 200 EMA close`;
- no active ATR cooldown.

This applies to initial shorts and some re-entry / add events when the broader short regime remains valid.

### Countertrend Absorption

Countertrend candles can be absorbed when price moves inverse to the short trend and compresses by PX distance toward the `200 EMA`, while the `10 EMA low` slope remains negative.

This is not treated as bullish by default. It can be a reload zone if the bearish structure remains valid.

### Invalidation

A close over the `200 EMA close` invalidates the specific short attempt being taken from that compression/retest area.

It does not permanently invalidate the whole short regime. If price later returns below the relevant structure and produces a fresh valid trigger after any cooldown, the short regime can resume.

### Close / Reduce Conditions

General close/reduce warning:

- two consecutive closes over the `10 EMA low`;
- `10 EMA low` slope turns upward.

Immediate reduce/close overrides:

- ATR anomaly around `4x`;
- PRI trigger against the position;
- CSI `10` candle strength against the position, described here as a candle closing fully at highs in the short case, with essentially zero upper wick;
- local support / lower extension targets after trend has continued for a while.

For ATR anomaly, a fresh entry trigger does **not** override cooldown. New entries should be avoided during the cooldown window. Risk reduction and closing remain allowed.

## Confirmed Long-Side State Model

### Candidate Early Long Permission

The first long fixture suggests, but does not yet confirm, that long-side permission can begin before `10 EMA low > 200 EMA close` when a [[trading/entry/123|123 Entry]] forms around the `200 EMA`.

Textbook long `123` from the fixture:

- `1`: strong close over the `200 EMA`, with CSI around `9`;
- `2`: pullback to the `200 EMA`, which is the determinate entry level;
- `3`: another CSI around `9`, making progress and closing beyond candle `1` and the pullback candles.

This must be audited before implementation. The `10 EMA low` crossing above the `200 EMA` may be unnecessary for a `123` entry, or the label may reflect inconsistent rule application.

### Long Entry And Add Logic

Candidate long-side entry/add patterns:

- strong close over the `200 EMA` with a `123` pattern;
- pullback to the short-term trend after the impulse over the `200`;
- reclaim of the `10 EMA low` after a break below it;
- reload near the `200 EMA`, where PX allows larger sizing;
- wick through the `200 EMA` does not invalidate by itself;
- absorption wick in the long's favor near the `200 EMA` can justify adding.

Size is smaller when price is not close to the `200 EMA`, especially after the trend has already advanced.

### Long Distribution And Close Logic

Longs distribute into upper PX bands. If an early long entered before the `10/200` cross, the later cross can be a sell event when price is already far through the PX bands.

Candidate reduce/close patterns:

- price breaks the `10 EMA low`;
- `10 EMA low` slope turns negative;
- CSI around `-10` against the long;
- absorption candle plus low CSI;
- PRI lower trigger;
- weak consecutive absorption candles after a mature trend;
- ATR anomaly;
- candle breaks the `200 EMA`;
- weak candle zone with consecutive low CSI and likely VFTI/RSI negative rollover.

Late in the trend, tolerance for weak or absorptive price action decreases. Trend maturity can be measured by half-life of mean reversion, but the exact implementation is still open.

### Candidate Long Invalidation

The fixture suggests wicks through the `200 EMA` do not invalidate, while a candle breaking the `200 EMA` is a hard invalidation if still long. This needs confirmation across additional charts.

If price fails to reclaim the `10 EMA low`, rolls under the `200 EMA`, and VFTI/RSI are likely negative, longs are done for this mapping.

## PX Scale-Out Semantics

PX in the current screenshots is measured against `10 EMA low` with `STDDEV lookback=100`.

Important: PX does not have to be anchored to the `10 EMA low`. Some mappings may use PX bands from the `200 EMA` instead. The anchor is part of strategy identity and must be specified per mapping.

Important source note: the chart screenshots currently use **asymmetric** PX bands.

The current `price_extension.py` asymmetric path:

- `signal_value = (close - MA) / MA * 100`;
- positive and negative percent distances are separated;
- positive and negative means are computed separately;
- positive and negative standard deviations are computed separately;
- `upper_band_1 = positive_mean + 1 * positive_std_dev`;
- `upper_band_2 = positive_mean + 2 * positive_std_dev`;
- `lower_band_1 = negative_mean - 1 * negative_std_dev`;
- `lower_band_2 = negative_mean - 2 * negative_std_dev`;
- band prices are converted back around the `10 EMA low`.

Key principle:

> MA crosses are not automatically entries. A cross can arrive too late and too extended; when PX shows price already outside the second standard-deviation band, the correct action may be skip, reduce, or distribute rather than enter.

For this strategy family, PX bands are not the primary entry signal. They are an exposure and distribution map once the position is already active and in the money, and they can invalidate late entries when price is already too extended.

Confirmed interpretation:

- short side: lower negative mean / lower band area means begin or continue taking profit;
- short side: lower band 1 distributes more, lower band 2 targets far-side distribution and often being heavily reduced or flat;
- long side: upper positive mean / upper band area means begin or continue taking profit;
- long side: upper band 1 distributes more, upper band 2 targets far-side distribution and often being heavily reduced or flat;
- adverse-side PX bands are secondary because entry/reload logic already governs absorption around the `10` and `200`.

Destin's sizing intuition is continuous, not bucketed. The implementation should therefore prefer a continuous target-exposure curve over hard bands like `2/3`, `1/3`, `flat`, while still allowing tests to inspect equivalent points on the curve.

Known limitation:

- Band-based scale-out can undercapitalize long-duration trends if it reduces exposure without a corresponding scale-in / re-add mechanism.
- This may be acceptable for a singular profit-retention strategy, but Money Machine still wants to capture long-duration trends in one strategy or another.
- Do not force the entire long-duration trend-capture problem into this one mapping if doing so muddies the semantics.

## Position Sizing Semantics

The strategy is not full-size-on-signal.

Confirmed allocation model:

- first third: initial entry on the trigger;
- second third: adverse absorption fill between entry and the `200 EMA`, only while the setup remains valid;
- final third: only after the trade is already in the money or has reconfirmed in-trend.

This follows the reusable [[trading/entry/123|123 Entry]] primitive.

Hard invariant for the automated approximation:

> Do not reach full target exposure while the position is still adverse. Full allocation requires positive unrealized position ROE or a distinct in-trend confirmation.

This is the practical meaning of the Trading Catalog's `123` / `Buy n Bid` behavior for this mapping.

Because current backtests are close-only and do not support limit grids, the first codification must be explicitly labeled as a close-price approximation of a discretionary limit-grid strategy.

## Discretionary Scale-Out Semantics

Destin prefers continuous scale-out of winners:

- "If in the money, get this sack of shit off my books."
- Nicer statement: it is often positive EV to reduce path dependency, realize profit, and refill later at more favorable prices.
- Compounding favors realized profit and reduced future exposure risk.

Manual behavior often uses a grid of many limit orders, roughly 30 orders, with skew:

- `20%` default skew;
- `0%` skew when using both absorption-side and distribution-side limits;
- `50%` skew when urgency is higher.

The close-only first implementation should approximate this with continuous exposure reduction as price moves from current in-money price toward lower PX targets, especially lower mean, lower band 1, and lower band 2.

## Example Label Interpretations

### Short-Side Fixture

The initial annotated short-side chart used these labels:

- `1 Short Entry`: `10 EMA low < 200 EMA close`; price was above the `10 EMA low` and closed below it.
- `3 Reload partial short`: countertrend candle compressed by PX toward the `200`; `10 EMA low` slope stayed negative, making absorption acceptable.
- `4 Add to short`: same close-below-`10 EMA low` trigger under bearish permission.
- `5 Close short`: consecutive closes over `10 EMA low` and upward `10 EMA low` slope.
- `6 Short on break`: same bearish trigger after structure broke.
- `7 Scale out`: take profit into rolling lows / lower extension.
- `8 ATR anomaly`: get out of the way; avoid new triggers during cooldown.
- `9 Hard close short`: consecutive candles over `10 EMA low`, upward `10 EMA low` slope, CSI `10`.
- `10 Short`: price compressed to the `200`; absorbed. Close over the `200` invalidates this specific short.
- `11 Add to short`: price accelerated away from the `200` and there was not yet a full pull position.
- `12 Slam short`: first real retest of the `200` failed, then price broke down under the `10 EMA low`.
- `13 Scale out`: take profit into rolling lows / lower PX extension.
- `14 Close`: ATR anomaly plus PRI, local low support, and mature trend; do not be greedy.
- `15 Do not short`: consecutive closes over the `10 EMA low`, upward `10 EMA low` slope, and likely VFTI/RSI turning green. Destin might long preemptively here, but long-side behavior is out of scope for this page until separately elicited.

### Long-Side Fixture

The first annotated long-side chart used these labels:

- `1 Entry`: strong close over the `200 EMA` with a `123` pattern. Did not wait for the `10 EMA low` to cross over the `200 EMA`; this is currently a candidate inconsistency / possible exception, not confirmed permission.
- `2 Actual 10/200 cross`: the `10 EMA low` crossed over the `200 EMA`, but price was already too extended for entry. PX distance / bands may invalidate entry because price is outside the second standard-deviation band; needs consistency audit.
- `2.5 Distribution`: if entered early before the cross, sell/scale out because price has moved far through the PX bands.
- `3 Pullback`: first pullback to the short-term trend after the impulse over the `200`.
- `4 Close`: price broke the `10 EMA low`, `10 EMA low` slope turned negative.
- `5 Add`: price reclaimed the `10 EMA low`, but size should be moderated because price is not close to the `200 EMA`.
- `6 Scale out`: price entered PX bands.
- `7 Close`: price broke the `10 EMA low` with CSI around `-10`.
- `8 Reclaim`: reclaimed `10 EMA low`; small size because not close to the `200 EMA`.
- `9 Scale out`: scale out into PX bands.
- `10 Finish scale-out / close`: absorption candle and low CSI.
- `11 Close`: broke `10 EMA low` again.
- `12 Reload`: reload by the `200 EMA`; PX would allow sizing up.
- `13 Distribution`: band-based distribution plus absorption and low CSI.
- `14 Clear`: PRI lower; finish distribution and clear the position.
- `15 Reload`: reload by the `200 EMA`.
- `16 Hold valid`: wicks through the `200 EMA` do not invalidate.
- `17 Add`: absorption wick in the long's favor near the `200 EMA`.
- `18 Distribution`: band-based distribution.
- `19 Shrink / close`: consecutive absorption candles and weak price action; if not advancing higher, shrink or close.
- `20 Close`: broke EMA lows.
- `21 Small reclaim`: reclaimed lows, but trend is long in the tooth by half-life of mean reversion and not close to the `200 EMA`, so size stays small.
- `22 Trim / close`: absorption late in the trend; lower tolerance for weak action, trim or close.
- `23 Exit`: ATR anomaly.
- `24 Flat / no new long`: broke `10 EMA low`; fortunately already flat.
- `25 Hard exit`: candle broke the `200 EMA`; if still long, close.
- `26 Longs done`: weak candle zone with consecutive low CSI; VFTI and RSI likely negative. Longs are done unless price reclaims the `10 EMA low`, which it did not, and it rolled under the `200 EMA`.

## Open Ambiguities

Only unresolved points that can change orders, position size, or risk:

- Exact continuous scale-out curve from entry/current price through PX negative mean, lower band 1, and lower band 2.
- Exact long-side continuous scale-out curve through PX positive mean, upper band 1, and upper band 2.
- Which PX anchor each mapping uses: `10 EMA low`, `200 EMA`, or another determinate level.
- Default ATR cooldown length. Current provisional approximation: avoid the next few candles; fresh entry triggers do not override cooldown.
- Whether rolling lows should be represented only by PX bands in the first implementation, or combined with an explicit local-low/channel-low detector.
- How to calculate "trend has continued for a while" for discretionary de-greeding. Candidate mentioned by Destin: half-life of mean reversion.
- Exact PRI definition and event source in code. Confirmed semantic shape: `[-1, 0, 1]` directional trigger space.
- Exact CSI `10` implementation source and whether zero-wick/high-close must be literal or score-threshold based.
- Side asymmetry and consistency audit: which short/long differences are intentional versus labeling inconsistency or memory drift.
- Whether early long `123` before the `10/200` cross is a separate entry strategy, a valid explicit exception, a missing shared permission rule, or an inconsistent label.
- Failure-case fixtures where the setup looks valid but should fail, be skipped, or be closed faster.
- DOGE/BTC-specific ugly regimes before changing assets; failure cases are expected to add as much value as success cases because avoiding drawdown is at least half the problem.
- Long-duration trend capture: whether handled by re-add semantics inside this mapping or by a separate strategy.

## Behavioral Parity Fixtures Needed

Before economics:

- Clean short entry under `10 EMA low < 200 EMA close`.
- Countertrend compression reload with negative `10 EMA low` slope.
- Failed `200 EMA` retest followed by slam short.
- Scale-out through PX lower mean / band 1 / band 2.
- ATR anomaly cooldown where a fresh short trigger appears but must be ignored.
- Hard close on consecutive closes over `10 EMA low`.
- Immediate close/reduce on PRI or CSI strength without waiting for two closes.
- Skip short where `10 EMA low` slope is up and price is closing consecutively above it.
- Final-third allocation only after positive unrealized ROE or reconfirmed in-trend behavior.
- Long `123` entry before the `10/200` bullish cross as a disputed fixture, not yet an accepted rule.
- Long late-cross non-entry where price is already outside the second PX band, to determine whether PX extension overrides cross-based entry.
- Long reload near `200 EMA` where wicks through the `200` do not invalidate.
- Long hard exit when candle breaks the `200 EMA`.
- Long late-trend weak-action trim / close.
- After semantics are clearer, run an unlabeled-chart exercise: agent labels candidate actions first, then Destin reviews differences. Treat this as a parity probe, not proof of implementation correctness.
- After DOGE/BTC failure labels are flushed out, run a blind rule-derivation exercise on a fresh asset with the same colored EMA indicators. The agent should not be bounded by the current EMA/PX rule set; a fresh agent with no prior rule context may be preferable to derive a cleaner EMA-only baseline.

## Implementation Handoff

Smallest accepted implementation scope, once remaining semantics are confirmed:

- Create a distinct strategy identity for this mapping rather than overloading `emac_v4`.
- Use same-timeframe `10 EMA low`, same-timeframe `200 EMA close`, asymmetric PX-on-`10 EMA low`, ATR anomaly, PRI, and CSI inputs.
- Implement a close-only state machine:
  - flat;
  - short probe / first third;
  - short absorption up to two thirds;
  - full short only after in-money confirmation;
  - distribution / scale-out;
  - cooldown;
  - invalidated attempt.
- Implement continuous target exposure as a function of:
  - current position ROE;
  - distance to `200 EMA`;
  - side-appropriate PX mean / band 1 / band 2;
  - cooldown and immediate reduce events.
- Add negative-path tests for:
  - no full allocation while adverse;
  - no new entry during ATR cooldown even if a fresh close-below trigger appears;
  - close over `200` invalidates the current attempt but not the whole future short regime;
  - two closes over `10 EMA low` closes/reduces even if `10 EMA low < 200 EMA close` remains true.

## Current Viability

Not tested. Behavioral parity is incomplete and long-side behavior has not yet been elicited.

## Next Action

Collect more chart fixtures focused on:

- continuous scale-out curve;
- ATR cooldown examples;
- failed `200 EMA` retest / slam short examples;
- side-asymmetry and consistency audit;
- failure cases.
- DOGE/BTC continuity before changing assets.
- later: unlabeled-chart agent labeling exercise after the rules are less ambiguous.
- later: fresh-asset blind rule derivation from colored EMAs only, ideally with an unprimed/fresh agent.
