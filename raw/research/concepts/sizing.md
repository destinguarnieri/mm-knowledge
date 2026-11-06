# Sizing, capital feedback, and explicit position management

Status: in progress
Updated: 2026-11-06

Working synthesis of Destin’s positioning discussion. This records observations and a framework for further design, not a settled replacement policy or authorization to change the trading runtime. Kept at the explicitly requested concept-note path.

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

The working direction is to define these policies before choosing implementation machinery. “Constant signal means hold” is not yet a selected rule. Neither Carver-style continuous sizing nor its alternatives should be adopted solely by convention.

## 7. Implementation and verification context

The backtest compounding-source setting is implemented and verified. It does not implement the mandate framework described above. Existing strategy sizing and allocation caps follow the selected capital source; broker margin/liquidation checks remain based on marked equity.

Paired Example BTC daily runs, differing only in compounding source:

- Account equity: `0aaac038-6670-4873-b77d-d8cd131776cd`.
- Booked P&L: `5fa8950a-992d-4629-81d2-0429fb2ed901`.

Signals were identical and every order/hold across 2,307 scored bars per run matched reconstructed targets, precision, and minimum-order filtering. Equity mode reproduced the original run’s metrics. These establish implementation correctness for those settings, not the desirability of either policy. Metrics remain in saved-run tools and the backtest UI.

See [[engineering/bounded-ema-history#Backtest compounding source and absolute-sizing note — 2026-11-06]] for implementation continuity.
