# Sizing, capital feedback, and explicit position management

Status: in progress
Updated: 2026-11-12

Working synthesis of Destin’s positioning discussion. This records observations and a framework for further design, with a V1 baseline pinned on 2026-11-12 and V2 still under discussion. It is not authorization to change the trading runtime. Kept at the explicitly requested concept-note path.

## 1. Observation: an unchanged forecast can still generate orders

The Example backtest pipeline recalculates a desired quantity from the current signal, sizing capital, price, and optional volatility inputs. It then applies rebalance selection, exposure limits, quantity precision, and the minimum-order threshold.

In the simple direct capital-sizing case:

```text
target quantity = normalized forecast × allocated sizing capital ÷ price
order quantity  = target quantity − current inventory
```

This is a continuously maintained exposure policy. An unchanged forecast does not imply unchanged quantity: capital or price movements can generate orders independently of a change in the investment view.

The original investigation did not identify a major arithmetic error. The concern is the policy embedded in the calculation: account movements can become trade instructions without a separately expressed decision to compound, rebalance, add, or trim.

### Equity feedback can reverse the direction of trading

For one long position initially at its target exposure, assume a constant target multiple L of marked equity, no other holdings or cash flows, and no fees, slippage, or changing volatility. After price return r:

```text
new equity          = old equity × (1 + L × r)
new target quantity = old quantity × (1 + L × r) ÷ (1 + r)
```

This holds while prices and equity remain positive and no risk intervention occurs.

| Target exposure | Rising price | Falling price |
|---|---|---|
| Below 1× | Reduce quantity | Increase quantity |
| Exactly 1× | Hold quantity | Hold quantity |
| Above 1× | Increase quantity | Reduce quantity |

The same formula therefore produces contrarian adjustments below 1× and trend-following adjustments above 1×. The rule is deterministic, but its resulting trade path depends on the evolving relationship between price, equity, and exposure.

For example, starting with $500,000 at price $1 and targeting 2× exposure gives 1,000,000 units. After a 10% rise, equity becomes $600,000 and the target becomes 1,090,909 units. After rebalancing and another 10% rise, equity becomes $720,000 and the target becomes approximately 1,190,083 units. The unchanged forecast produces additions funded by open gains.

At 1×, capital and price rise proportionally, so quantity remains constant. That special cancellation should not be generalized to other exposure levels.

## 2. Potential pitfalls and side effects

### Open profits become an immediate sizing input

The feedback is price → unrealized P&L → sizing capital → inventory adjustment → sensitivity to the next price move. Gains can authorize additions before any profit is booked; reversals can shrink the same capital base and prompt reductions. This may be intentional, but should be an explicit policy choice.

### Portfolio movements can trigger unrelated asset trades

When capital is shared across positions, another asset’s P&L can change this asset’s target even when its own price and forecast are unchanged. Portfolio-level coupling can be useful, but its purpose should be clear.

### Attribution becomes harder

Orders and performance reflect more than forecast changes. They also reflect compounding, price-driven rebalancing, volatility updates, constraints, and execution rules. A signal-versus-position chart alone does not explain those contributions.

### Turnover and path dependence

Frequent recalculation can generate repeated adjustments and costs. The outcome depends on the route prices take, the decision cadence, rounding, thresholds, and whether partial closes book gains or losses. More frequent recalculation need not justify more frequent execution.

### Excluding uPnL does not eliminate rebalancing

Booked-P&L capital removes immediate open-P&L feedback, but dividing a fixed dollar budget by a changing price still changes desired quantity. Partial closes then update booked capital and can influence subsequent orders. Even booked profits need not automatically enlarge the current session’s mandate.

In the verified Example configuration, booked-P&L mode traded more often than equity mode. At a saturated 1× target, equity compounding can cancel price-driven quantity adjustments; booked capital does not provide that cancellation. This is a configuration-specific observation, not a general ranking of the two policies.

### Gating a moving target can defer rather than remove the effect

If a forecast-change trigger unlocks the entire recalculated target, the resulting trade can include accumulated capital and price adjustments. Likewise, rewriting the same moving target as an inventory-error or marginal-signal formula does not change the underlying policy.

### Stable quantities also have consequences

Holding quantity allows dollar exposure, portfolio weight, and measured risk to drift. A stable mandate cannot replace ongoing risk measurement or mandatory intervention. Continuous exposure maintenance remains a coherent option when that behavior is actually desired.

## 3. Working framework: the portfolio manager and the trading desk

The central distinction is between capacity and intent:

> Having more capacity permits a trade; it does not request one.

### Trader managing an assigned asset

Consider a trader assigned Nasdaq index futures for a session. They begin with a risk budget and familiar trade increments—perhaps hotkeys for 1, 5, and 25 lots. They put inventory on and take it off through the day. Trades change holdings and remaining capacity; market moves change P&L and measured risk. Neither automatically changes the lot increments or assigned budget.

A separate review might update the budget the next day, or an exceptional risk event might revise it during the session. Daily review is an illustrative choice, not a settled requirement or a claim about every desk.

### Portfolio manager allocating across assets

A manager can decide to establish a 10% allocation at a particular time and then allow the weight to drift as prices move. “Establish 10% now” and “maintain 10% continuously” are different mandates. Buying and selling shares are explicit subsequent decisions.

An appreciated position may be allowed to run, trimmed, deliberately increased, or rebalanced. Each expresses a position-management policy rather than an inevitable consequence of changed account value.

### Keep three objects separate

| Object | Meaning | Update authority |
|---|---|---|
| Mandate | Assigned capital, normal trade scale, risk limits, and permitted behavior | Allocation review or explicit exception |
| Current state | Inventory, marked exposure, booked/open P&L, risk, and remaining capacity | Market and accounting events |
| Action | Add, hold, trim, exit, reverse, or rebalance | Position-management decision or required risk intervention |

Current state updates continuously. The mandate updates deliberately. Actions need their own justification.

A stable mandate need not mean every limit is a fixed dollar number. It means the rule governing its measurement and revision is explicit. Marked equity can continue to inform margin, liquidation, and risk capacity even when it does not continuously expand desired holdings.

### Separate the decisions within that framework

1. **Investment view:** What opportunity exists, with what conviction and horizon?
2. **Allocation:** How much capital or risk should be committed, and for how long?
3. **Position management:** Given existing inventory, should we add, hold, trim, exit, or reverse?
4. **Execution:** Is this price, timing, size, and order type worthwhile?
5. **Risk oversight:** What actions are prohibited or required regardless of conviction?

These are conceptual responsibilities, not a requirement for five new software services.

## 4. Capital policy has both a source and a clock

The implemented compounding selector answers which capital figure is available:

- `account_equity`: includes unrealized P&L.
- `booked_pnl`: initial capital plus net realized P&L, including fees.
- Static sizing continues to use initial capital.

A separate question remains: when should that figure revise an asset’s allocation or normal trade scale?

Potential review events include a session boundary, a scheduled allocation review, a new investment decision, or an exceptional risk event. None is selected yet. Updating a mandate also need not immediately require trading existing inventory to its new capacity.

This permits compounding at allocation reviews without requiring compounding-driven orders every candle. It also permits continuous compounding where a strategy deliberately chooses it.

### Candidate: snapshot the sizing base in units at the compounding boundary

Historical proposal from 2026-11-07. The V1 decision below supersedes the assumption that a separate normal base and maximum are always required. V2 also need not have two independent quantities: its forecast clip can imply a maximum from the reference quantity, as clarified below.

On 2026-11-07, Destin proposed a simple way to stabilize the mandate: calculate a sizing snapshot **in asset units** when the compounding period starts, then retain that base quantity throughout the period. Destin identified stabilizing units as the likely missing piece. This is a design candidate to develop, not an implemented or fully specified policy.

For direct continuous signal mapping:

```text
At period start:
    base_units = sizing calculation using the selected capital source,
                 reference price, and applicable sizing inputs at that boundary

Within the period:
    proposed_target_units = (signal / signal_scale) × base_units
```

The snapshot is the normal sizing base, not the actual held position or the maximum permitted exposure. For example, a base of 100 units and signal scale 10 maps signals 5, 10, and 15 to proposed targets of 50, 100, and 150 units before separate adjustments and limits.

**Freezing units is different from freezing capital.** A fixed dollar budget divided by each new price still changes the target quantity. Retaining the already-converted base quantity removes that price denominator, as well as changing account value, from the within-period base calculation. If volatility targeting contributes to the base, its boundary-time effect would be captured in the snapshot; any subsequent volatility adjustment must be treated as a separate policy.

With an unchanged signal and no other active adjustment, the proposed unit target stays constant through both gains and losses. Dollar exposure, P&L, leverage, and portfolio weight can still move. Marked risk must continue to be measured, and independent constraints may still block additions or require reductions. The snapshot therefore does not promise that every unchanged signal produces zero orders.

This is a concrete expression of the desk example: establish the normal trade scale for a period, manage inventory using that scale, and revise it deliberately. It does not require resolving every broader architecture question first.

#### Positive and negative return scenarios still to work through

- Test rising and falling prices for both long and short holdings, including below-1× and above-1× exposure, under unchanged and changing forecasts.
- Compare account-equity and booked-P&L snapshots after open gains/losses, partial closes, and fees. Booked profits during the period would not change the retained base unless an explicit refresh rule permits it.
- Follow marked exposure and remaining risk capacity during the period, especially when losses reduce equity while units remain fixed.
- At the next boundary, inspect how capital, price, and any volatility inputs jointly change the new base. Positive returns do not automatically imply more units, nor negative returns fewer units.
- Decide whether a changed base immediately rebalances existing holdings or applies only to subsequent position-management decisions. A periodic snapshot can concentrate an adjustment at rollover rather than eliminate it.

Still open: period duration and alignment; initial snapshot timing; which inputs and limits are frozen versus dynamic; exceptional refresh conditions; and restart/replay handling that preserves the intended period snapshot. No cadence, gain/loss response, or rollover trading rule has been selected. These were the open questions on 2026-11-07; use the 2026-11-12 decision below for the current V1 direction.


### V1: one snapshotted maximum quantity — pinned 2026-11-12

Status: confirmed as the conceptual baseline. The V1 calculation is implemented in the 2026-11-12 patch below; retaining its maximum as a period snapshot is still pending. Destin first pinned this baseline, then authorized the scoped calculation cleanup after discussing V2.

V1 has no separate normal/base position size. Each instrument has a leverage setting and maximum position percentage. At a strategy-defined sizing/compounding boundary:

```text
allocated_margin_budget = selected_capital × max_position_percent / 100
maximum_notional = allocated_margin_budget × configured_leverage
snapshot_maximum_units = maximum_notional / boundary_price
```

For $10,000 capital, BTC at 40×/50%, ETH at 25×/30%, and SOL at 20×/20% yield assigned margin budgets of $5,000/$3,000/$2,000 and maximum notionals of $200,000/$75,000/$40,000. Multiplying the assigned margin budget by leverage converts it to notional capacity; it does not multiply account capital. This is an allocation policy, not a complete available-margin or maintenance-margin model.

Within the period:

```text
signal_to_position(signal, snapshot_maximum_units)
    → dynamic volatility adjustment
    → strategy rebalance/transition policy
    → clamp to ±snapshot_maximum_units
    → executable order delta against actual inventory
```

The SAME retained maximum quantity is both the signal-sizing reference and the enforced position ceiling. Checks continue on every decision; the threshold is fixed until refresh. Do not reintroduce a moving account-value/price cap under the label of live enforcement. Price/account-value changes alone do not move either reference. Exchange margin requirements and any separately explicit risk rules remain independently applicable.

Strategy configuration selects refresh timing and the existing capital source; no universal two-week default was chosen. Strategy owns movement toward its target. Dynamic volatility adjustment remains allowed. At rollover, enforcing a lower maximum can require a reduction; the current Example over-limit branch bypasses its deadband/buffer, so its interaction with strategy transition speed needs explicit treatment in implementation. Initialization, alignment, exceptional refresh and replay details are not yet specified.

Signal mapping and final capping must have explicit semantics when forecasts can exceed their reference scale. V1 does not require a separate Carver-style normal quantity. Static margin allocations are a starting policy, not a claim of optimal portfolio risk allocation: leverage, volatility and correlation produce unequal risk; full utilization leaves no initial-margin reserve for costs/other commitments. Snapshotting stabilizes units but permits marked exposure and risk to drift.

### V2: volatility targeting — clarified 2026-11-12

Status: in progress. V1 remains pinned separately. Destin leaned toward full-signal terminology during design, then explicitly selected keeping the existing reference convention for this patch to reduce simultaneous changes. Full-signal terminology remains a possible future option; it is not implemented.

**Do not import V1's `max_position_percent` maximum into V2 by default.** The earlier proposal to combine a volatility-sized reference with a separate allocation/margin-derived “capacity cap” mixed the two models. “Capacity cap” was an assistant label for V1's existing maximum, not a requested new setting. That hybrid is not the agreed V2 design.

#### Reference-signal and full-signal formulations

In the reference-signal construction under discussion, scale forecasts toward average absolute magnitude 10 and clip at ±20. Let B be the snapshotted volatility-sized quantity at reference signal 10:

```text
f = signal clipped to [-20, 20]
target_units = (f / 10) × B
implied position range = [-2B, +2B]
```

The signal clip supplies the implied maximum. There is no independently selected position maximum in this construction. This describes the forecast-sizing map, not a claim that a complete trading system has no other controls. Carver describes the average-absolute-10 / clip-at-20 convention in [Do non binary forecasts work?](https://qoppac.blogspot.com/2020/07/do-non-binary-forecasts-work.html).

The equivalent full-signal formulation is:

```text
M = 2 × B
target_units = (f / 20) × M
implied position range = [-M, +M]
```

For B = 25 units and M = 50 units, signals 5, 10 and 20 produce 12.5, 25 and 50 units in BOTH formulations. With the same capital, price and volatility inputs, a 20% risk target at reference signal 10 corresponds to a 40% risk target at full signal 20. The equivalence requires matching snapshot timing, adjustments and constraint placement. A 20% target at full signal is not equivalent to 20% at reference signal: it produces half the units in this example.

The 10 and 20 are illustrative configured signal scales, not hardcoded requirements. Generally, M = B × (signal_clip / reference_signal). One snapshot quantity is sufficient because the other is derived; V2 does not inherently need two independent sizing quantities or a moving account-value cap.

#### Volatility-sizing semantics

For one linear instrument, the underlying calculation is:

```text
annual_dollar_volatility_target = capital_basis × annual_volatility_target
volatility_sized_units = annual_dollar_volatility_target /
                         (estimated_annual_instrument_volatility × snapshot_price)
```

This yields B or M depending on whether the configured volatility target applies at reference or full signal. The capital basis and any portfolio allocation weights must be explicitly defined; do not silently reuse V1's margin-allocation percentage for that purpose. The dollar volatility target expresses estimated PnL standard deviation, not maximum loss or margin deposited.

Exchange leverage does not multiply capital in this risk-sizing formula. Exchange margin requirements remain independently applicable; they do not imply importing V1's maximum into the forecast map. The 2026-11-12 patch removes the leveraged-risk-capital branch and inherited V1 allocation cap from calculate_sizing; see implementation scope below.

Average absolute forecast 10 calibrates forecast magnitude, not exact realized strategy volatility. Signal variation, squared exposures, estimation errors, constraints and portfolio correlations affect realized risk. A full-signal risk target will generally exceed the typical signal-scaled risk level when signals spend most of their time below maximum; changing the configured target can account for the reference/full-signal scale difference, without guaranteeing a particular realized volatility.

#### Snapshot and post-mapping adjustment

Snapshot the chosen unit reference at strategy-defined refresh boundaries using the selected capital source and boundary sizing inputs. Hold that unit reference within the period. Dynamic volatility adjustment remains a distinct downstream policy; snapshot-based targeting establishes risk at the boundary and does not continuously maintain it.

The ±2B / ±M bound above applies BEFORE subsequent volatility adjustment. If that adjustment can amplify positions, the final target may exceed the signal-implied range. The current patch enforces the mapping-derived bound after adjustment, as in the proposed max_size return and existing callers. Amplification can use remaining headroom but cannot exceed that bound when one exists. This is a separate choice from adding V1's allocation cap. Avoid accidentally applying the same volatility-targeting rule twice.

The current patch retains portfolio sizing capital × instrument_weight × instrument_diversification_multiplier as the risk-capital basis, with no leverage multiplier. Further allocation/terminology changes are separate work. Elapsed unit snapshots are now implemented for the four migrated backtest strategies; see the implementation section below. Broker-margin redesign is not included.

## 5. Broader concepts that inform the discussion

The related notes broaden the possible decision interface:

- [[inventory-conditioned-signals-and-marginal-edge]]: ask whether another unit is worthwhile given existing inventory; preserve forecast edge, inventory penalty, and execution cost separately.
- [Inventory-risk condensation](inventory_risk%5B1105.3115%5D_CONDENSE.md): distinguish desired inventory from the price, probability, and speed of acquiring or reducing it; recomputation and order modification can have different clocks.
- [[from-position-targets-to-transition-kernels]]: evaluate actions through their possible future inventory paths, persistence, and exit difficulty.

These are research inputs, not adopted production models. A normalized EMAC score is not automatically a monetary edge that can be compared directly with transaction costs; units and horizon must be defined before doing that.

No full market-making model, stochastic-control solution, or rejection of target positions is required to adopt the more modest principle: make the reason and authority for changing inventory explicit.

## 6. Open design questions

- What exactly is assigned: capital, normal quantity, risk budget, maximum exposure, or a combination?
- What remains stable between reviews, and which measurements remain dynamic?
- When and by whom is the mandate revised? Which P&L source enters that review?
- What justifies initial entry, additions, reductions, exits, and reversals?
- When is weight or exposure drift acceptable, and when is rebalancing intentional?
- Does a mandate revision affect only future trade capacity or also existing holdings?
- Which risk events block additions, and which require reductions?
- How should decisions record their causes so forecast, allocation, rebalancing, and risk effects are distinguishable?

V1 now has the pinned unit reference and ceiling described above. It does not promise zero orders from an unchanged signal: volatility adjustments, unfinished transitions and explicit risk actions can still trade. Remaining broad questions apply to V2 and implementation details; do not reopen the settled V1 distinction by assuming a separate normal base is mandatory.

## 7. Implementation and verification context


### V1/V2 calculation separation — 2026-11-12

Implemented after Destin approved the single-helper approach, building on his existing edit to `positions_v2.py`. Committed at his request as `810e7dbc` (Separate allocation and volatility reference sizing). No runtime starts, live operations or Research MCP runs.

- `calculate_sizing` remains one function. V1 converts its allocation maximum notional into units and returns that quantity in both `base_size` and `max_size`; the shared base field is the signal-mapping input, not an independent V1 budget. V2 calls `normal_risk_quantity` with selected capital unchanged, and derives its final limit from the signal mapping. V2 callers do not compute or pass V1 maximum notional.
- Removed `sizing_base`/`leverage` arguments and `SIZING_BASE` configuration from Example, Kitchen Sink, MACD and Combo. Leverage remains upstream in V1's maximum-notional calculation. V1 therefore uses the full allocation maximum, unlike the previous unlevered base. Existing saved configurations containing `SIZING_BASE` are rejected and must be explicitly reviewed/updated; the UI explains this for all four callers. No silent config migration.
- V2 retains reference-signal semantics. With direct absolute mapping, the actual configured clip/reference ratio determines the limit (10/20 implies 2×). Non-absolute clipping uses the shared signal clip definition. Continuous inverse mapping uses the bound of its existing sign(f) × (1 − abs(f/scale)) map, preserving its sign-reversal behavior. Kitchen Sink full/banded paths use a 1× reference bound.
- With clipping disabled, continuous V2 has no configured finite sizing cap (`max_size=None`); cap/over-limit helpers explicitly support that absence. This does not implement exchange admission checks or change broker liquidation. Full/banded V2 remain bounded by their mapping. The normal post-adjustment cap and over-limit buffer bypass are retained wherever a limit exists.
- `get_sizing_capital`, forecast normalization/divisor, volatility adjustment and rebalance algorithms are unchanged. `calculate_position_sizing` and multi-speed EWMAC retain their legacy sizing policy. Runtime registry schemas expose the removed field automatically; no API DTO generation or database migration is needed.
- This calculation-only commit did not include snapshots. The subsequent scheduler below stabilizes its outputs; continuous sizing remains the default.

Verification: 638 backend checks passed, including cross-caller V2 sizing, long/short post-adjustment capping, over-limit buffer bypass, absent clipping, V1 leverage dependence, V2 independence from V1 allocation/leverage, and schema rejection. Sixteen unrelated Combo/MACD feature-output failures reproduced on an isolated committed-HEAD baseline and were deselected in the final passing suite. Eleven frontend config tests, frontend TypeScript, scoped backend mypy/Ruff and frontend lint passed. Comparison JSON fixtures were refreshed for removal of `SIZING_BASE` and the existing default compounding source. Whitespace checks passed. Tests are offline; no saved-run performance comparison was performed.


### Elapsed unit snapshots — 2026-11-12

Status: in progress; committed at Destin’s request as `68b667c6`. Destin selected elapsed intervals anchored to the first eligible sizing decision.

- Example, Kitchen Sink, MACD and Combo expose `SIZING_REFRESH_INTERVAL_SECONDS`: `null` preserves calculation on every decision; a positive integer enables snapshots (1,209,600 seconds = two weeks). The UI exposes both choices through the runtime trade schema. Existing saved configs default to continuous behavior. Other strategies retain their existing policies.
- The first eligible post-warmup sizing calculation captures both `PositionSizing.base_size` and `max_size` in units. V1 retains its allocation maximum in both fields. V2 retains its volatility-sized reference and mapping-derived limit, including `None` when no finite limit is configured. Capital source remains independently selected by existing static/equity/booked settings.
- Each asset anchors its own elapsed schedule using candle milliseconds. A refresh uses current selected capital, price and targeting volatility on the first eligible observation at or after a boundary. Missing periods are skipped without shifting the original anchor. Repeated reads within a period, including after fills change booked capital, reuse the same snapshot.
- Signal mapping, live post-mapping volatility adjustment, rebalance policy, minimum-order filtering and execution gates remain active. A new snapshot can change the desired position at rollover, but the scheduler does not itself place an order. Existing post-adjustment limits and over-limit buffer bypass use the retained limit. Kitchen Sink refreshes before its execution gate, so a closed gate does not postpone the sizing schedule; that gate still controls actual orders.
- State is bounded to one latest snapshot per configured asset per strategy instance: anchor/capture timestamps, interval, period index and the unit pair. Calculation failure leaves the prior snapshot untouched. A new run initializes fresh state; no serialization for resuming mid-run was added. Refreshes emit DEBUG logs with asset, anchor, capture time, period and unit values. No wall-clock timers, calendar alignment, database migration or live-runtime changes.

Verification: the expanded offline suite passed 675 checks with the same 16 baseline Combo/MACD feature failures deselected. All 37 snapshot tests passed again after the final assertion update. The 30-day synthetic gain/loss path covers long/short positions, equity/booked capital and V1/V2 sizing: unchanged signals trade only on days 0, 14 and 28. Tests also cover all four callers, exact/delayed boundaries, duplicate reads, failed refresh, strict configuration, live signal/volatility adjustment and Kitchen Sink execution gates. Fourteen frontend tests, production TypeScript and scoped lint/type checks pass. The legacy backtest base class retains exactly its 26 baseline mypy errors, with no new errors. These are offline regressions, not saved Research MCP performance runs.

The backtest compounding-source setting is implemented and verified. It does not implement the mandate framework described above. The earlier verified runs below used the prior mixed sizing/cap policy. The 2026-11-12 formula changes above supersede that policy for the four migrated strategies; the capital-source getter and broker accounting are unchanged.

Paired Example BTC daily runs, differing only in compounding source:

- Account equity: `0aaac038-6670-4873-b77d-d8cd131776cd`.
- Booked P&L: `5fa8950a-992d-4629-81d2-0429fb2ed901`.

Signals were identical and every order/hold across 2,307 scored bars per run matched reconstructed targets, precision, and minimum-order filtering. Equity mode reproduced the original run’s metrics. These establish implementation correctness for those settings, not the desirability of either policy. Metrics remain in saved-run tools and the backtest UI.

See [[engineering/bounded-ema-history#Backtest compounding source and absolute-sizing note — 2026-11-06]] for implementation continuity.


### Snapshot scheduling verified through Research MCP — 2026-11-12

After Destin started the manager, ran six Example BTC daily backtests against stored Binance USD-M candles from 2021-01-01 through exclusive 2024-01-01. Shared assumptions: initial capital 10,000; leverage 2; allocation 100%; instrument weight/IDM 1; absolute forecast reference 10 / clip 20; direct mapping; zero rebalance deadband; 5 bps fee and 5 bps slippage; post-mapping volatility adjustment disabled. V2 uses the default RMS targeting settings and 20% risk target. Compare continuous sizing (null interval) with 14-day unit snapshots (1,209,600 seconds). These are behavior checks, not parameter optimization or performance recommendations.

Saved run IDs:

- V1 / equity / continuous: `c5ce09d1-e49e-44ba-8147-e46ee7fa14a5`.
- V1 / equity / 14-day snapshot: `aa153864-28a4-4c97-a9d1-5601fde82f36`.
- V1 / booked / continuous: `a04bd1c9-7144-4396-9b59-e9e9604276a6`.
- V1 / booked / 14-day snapshot: `ca6e89cf-01d9-4af4-9d50-5368a286e643`.
- V2 / equity / continuous: `c04fec45-ed5b-4076-9e4b-9732f74e49e4`.
- V2 / equity / 14-day snapshot: `5eca2f52-e99e-479e-9bb3-0fa2206bf974`.

All six completed, with full artifacts available, identical processed signals, no missing candles and no provider fetch. Independent reconstruction from persisted candles, fills and position state matched every order/hold across 842 scored bars per run. Reconstruction used pre-decision marked equity or booked cash, the elapsed unit snapshot, signal mapping/cap, five-decimal quantity truncation and the $10 minimum-order filter; V2 RMS/blended volatility was independently reconstructed from the 512-bar price window. The first scored decision is 2021-09-11 UTC; 61 retained periods follow the original 14-day anchor. Refreshes include both quantity increases and reductions.

There were 81 unchanged-signal comparisons away from refresh boundaries (68 long, 13 short). All three snapshot runs placed no orders on these bars, while the paired continuous runs continued resizing. On the constant -20 signal from 2022-06-18 through 2022-07-01, the equity V1 snapshot entered the period at -1.65765 BTC and held it throughout despite price/equity movement; continuous V1 equity sizing traded every day. Changing signals still generated within-period trades as intended. No evidence of the original account/price-driven resizing remained within these snapshot periods.

Scope: runtime verification covers Example, V1 equity/booked and V2 equity, with post-mapping adjustment disabled. Other callers, V2 booked, live adjustment and execution-gate behavior retain the earlier offline regression coverage. No live-system operations or code changes were needed. Standard metrics remain in saved-run tools/UI.
