

There is a reasonably short version that does the paper justice.

# The paper in three equations

The market maker chooses how far to quote from a reference price \(S\). If \(\delta\) is the quote’s distance from \(S\), the assumed execution intensity is:

\[
\lambda(\delta)=Ae^{-k\delta}
\]

Quoting closer produces more fills but earns less per fill. Quoting farther earns more conditional on execution but fills less frequently.

The market maker maximizes expected utility of terminal marked-to-market wealth:

\[
\sup_{\delta^a,\delta^b}
\mathbb E\left[
-\exp\left(-\gamma(X_T+q_TS_T)\right)
\right]
\]

subject to bounded inventory:

\[
-Q\leq q_t\leq Q
\]

The resulting policy can be understood approximately as:

\[
\boxed{
\text{quote center}
=
S+D\left(q^*-q\right)
}
\]

where:

\[
\boxed{
q^*=\frac{\mu}{\gamma\sigma^2}
}
\]

and \(D>0\) controls how strongly quote prices react to the difference between preferred and current inventory. 

That final relationship is the most important thing in the paper for your current line of thought.

---

# 1. The deepest lesson: alpha defines a preferred inventory, not an order

In the base model, the price has no drift:

\[
dS_t=\sigma\,dW_t
\]

There is no directional expectation, so the preferred inventory is zero:

\[
q^*=0
\]

The market maker changes its quotes to push inventory back toward zero.

The paper then introduces drift:

\[
dS_t=\mu\,dt+\sigma\,dW_t
\]

Now the preferred inventory becomes approximately:

\[
\boxed{
q^*=\frac{\mu}{\gamma\sigma^2}
}
\]

A positive expected drift makes some long inventory desirable. A negative drift makes some short inventory desirable. But the system does not ask merely whether \(\mu\) is positive or negative. It asks:

\[
\boxed{
q^*-q
}
\]

That is:

> How does the inventory I currently own compare with the inventory justified by my forecast, risk aversion, and volatility?

This is almost exactly the topology we uncovered in the Citadel example:

\[
out=e-\lambda q
\]

which can be rewritten as:

\[
out=\lambda(q^*-q)
\]

The difference is the controlled output:

- Citadel’s toy function emits a marginal signal.
- This paper uses the inventory residual to shift bid and ask prices.
- Both center the decision on **preferred inventory minus current inventory**.

That is more than a superficial resemblance. It is the same control-system architecture. 

---

# 2. Separate the center of the action from the width of the action

This is probably the second most valuable lesson.

Let:

\[
\delta^b=S-b
\]

be the distance from reference price to bid, and:

\[
\delta^a=a-S
\]

be the distance from reference price to ask.

The paper’s asymptotic approximation can be written compactly as:

\[
\delta^b
\approx
B+D\left(q-q^*+\frac12\right)
\]

\[
\delta^a
\approx
B+D\left(q^*-q+\frac12\right)
\]

where:

\[
B=\frac{1}{\gamma}\ln\left(1+\frac{\gamma}{k}\right)
\]

and \(D\) is a positive inventory-sensitivity coefficient determined by volatility, risk aversion, and fill dynamics.

From those two quotes, calculate their center:

\[
r=\frac{a+b}{2}
\]

This produces:

\[
\boxed{
r=S+D(q^*-q)
}
\]

The approximate total spread is:

\[
\boxed{
a-b\approx 2B+D
}
\]

This gives a clean decomposition:

\[
\boxed{
\text{quote center}
\longleftarrow
\text{forecast and inventory}
}
\]

\[
\boxed{
\text{quote width}
\longleftarrow
\text{risk, liquidity, and execution economics}
}
\]

Inventory primarily **skews the center** of the quotes. It does not merely tell the strategy to trade a smaller quantity.

When long beyond the preferred inventory:

\[
q>q^*
\]

the center moves downward. The strategy lowers both its bid and ask:

- the lower bid makes further purchases less likely;
- the lower ask makes inventory-reducing sales more likely.

When under-positioned:

\[
q<q^*
\]

the entire quote structure moves upward:

- the higher bid makes purchases more likely;
- the higher ask makes sales less likely.

This is a richer control mechanism than converting one signal into one target size. 

---

# 3. Inventory is controlled through the probability of the next state transition

The strategy does not directly command:

> Reduce inventory by five units.

It modifies the probabilities of future events.

Current inventory is \(q\). A bid fill moves it to:

\[
q+1
\]

An ask fill moves it to:

\[
q-1
\]

The strategy changes the bid and ask distances to alter the transition intensities:

\[
q\rightarrow q+1
\]

and:

\[
q\rightarrow q-1
\]

So the market maker is controlling a stochastic state machine:

```text
             bid fill
       q --------------> q + 1

             ask fill
       q --------------> q - 1
```

Quote placement controls the rates of those transitions.

That is a broader lesson for Money Machine:

> A position controller does not necessarily need to output a final desired quantity. It can alter the probability, price, speed, or desirability of incremental movements through position space.

The relevant object may be a policy:

\[
\pi(a\mid q,x)
\]

rather than only a target:

\[
q^*=g(x)
\]

Here, \(x\) is the rest of the market state and \(a\) is an available trading action.

---

# 4. Liquidity is part of position risk

The paper produces an important relationship:

- higher volatility \(\sigma\) increases inventory risk;
- higher order-arrival intensity \(A\) reduces inventory risk.

The authors explicitly observe that increasing \(A\) has broadly the opposite effect of increasing \(\sigma^2\). Faster incoming flow gives the market maker more opportunities to recycle unwanted inventory. 

This means position risk is not just:

\[
\text{position}\times\text{volatility}
\]

It is closer to:

\[
\text{inventory risk}
=
f(
\text{position},
\text{volatility},
\text{time to exit},
\text{probability of exit}
)
\]

Two equal positions in the same instrument can carry different effective risk depending on:

- current depth;
- trade-arrival rate;
- spread;
- queue position;
- available opposing flow;
- expected time to liquidation;
- whether the market is currently one-sided.

A position that can be recycled in two seconds is not economically equivalent to one likely to remain trapped for two minutes.

This suggests that Money Machine’s position penalty should eventually depend on **liquidation opportunity**, not merely volatility and notional exposure.

---

# 5. Fill probability is part of the strategy’s economic model

The paper does not optimize quote price independently of execution probability.

Under:

\[
\lambda(\delta)=Ae^{-k\delta}
\]

a deeper quote has:

- greater profit if filled;
- lower probability of being filled;
- slower inventory correction;
- greater risk of being stuck.

This creates two competing marginal effects:

\[
\text{value per fill}
\]

versus:

\[
\text{frequency and timing of fills}
\]

That principle transfers beyond market making.

For any potential order, Money Machine should eventually distinguish:

\[
\text{economic value conditional on execution}
\]

from:

\[
\text{probability and timing of execution}
\]

A passive order with a theoretical 10-basis-point edge is not necessarily superior to an aggressive order with a 6-basis-point edge if the passive order:

- rarely fills;
- fills only when adverse information arrives;
- leaves the strategy under-positioned during the forecast horizon;
- loses queue priority through repeated modification.

Execution probability is not plumbing beneath the signal. It is part of the economic value of the action.

---

# 6. Adverse selection is not just another fee

The paper’s market-impact extension models a bid fill as being followed by a downward movement in reference price, and an ask fill by an upward movement:

\[
dS_t
=
\sigma\,dW_t
+
\xi\,dN_t^a
-
\xi\,dN_t^b
\]

This captures the basic adverse-selection pattern:

- you buy, then price falls;
- you sell, then price rises.

The direct response is to quote farther away and demand more compensation.

But the paper identifies a second-order effect: quoting farther away lowers execution frequency, which makes existing inventory harder to unwind. Adverse selection therefore increases inventory risk indirectly as well as reducing per-trade profitability directly. 

That creates a feedback loop:

\[
\text{more adverse selection}
\]

\[
\Downarrow
\]

\[
\text{quote farther away}
\]

\[
\Downarrow
\]

\[
\text{fewer inventory-reducing fills}
\]

\[
\Downarrow
\]

\[
\text{greater risk of remaining stuck}
\]

So adverse selection should not merely be subtracted as a fixed transaction cost after sizing. It may alter:

- permissible inventory;
- required edge;
- quote placement;
- urgency;
- passive/aggressive choice;
- the slope of the inventory penalty itself.

---

# 7. Hard constraints should alter the policy, not clip its result

The model imposes:

\[
-Q\leq q\leq Q
\]

At:

\[
q=Q
\]

the market maker stops posting a bid because another bid fill would violate the limit.

At:

\[
q=-Q
\]

it stops posting an ask.

This is different from calculating an unconstrained action and clipping the resulting position afterward. The constraint changes the available action set inside the optimization problem. 

That distinction matters:

```text
Weak architecture:
unconstrained decision → trade → position clipping

Stronger architecture:
current constraints → permitted action set → decision
```

At or near a limit, the system should behave differently before a violation occurs:

- disable exposure-increasing actions;
- increase the value placed on exposure-reducing actions;
- change execution aggressiveness;
- alter the no-trade region;
- potentially accept worse prices to restore flexibility.

A limit is therefore not just a maximum output. It changes the topology of the decision surface near the boundary.

---

# 8. Time horizon matters mainly near the terminal boundary

The exact model is finite-horizon, but the authors find that optimal quotes become almost time-independent when sufficiently far from terminal time. They therefore derive long-horizon or asymptotic quote approximations using the smallest eigenvalue and eigenvector of the transformed linear system. 

Architecturally, this suggests two policy regimes:

## Normal regime

Use a mostly stationary policy:

\[
\pi(q,\text{market state})
\]

This could potentially be precomputed or represented as a lookup surface.

## Terminal regime

As shutdown, expiry, signal-horizon end, funding deadline, or forced flattening approaches, use a time-dependent policy:

\[
\pi(t,q,\text{market state})
\]

This matters for Money Machine because “time remaining for the forecast to pay” should affect position decisions.

The same forecast and inventory can rationally produce different actions when:

- the forecast has 30 seconds left;
- the forecast has 30 minutes left;
- the position must be flat before settlement;
- the system can carry inventory indefinitely.

Time-to-horizon belongs in the state.

---

# 9. Constant repricing can make a theoretically optimal strategy worse

The paper acknowledges that the mathematical model is continuous, while real markets have:

- discrete ticks;
- queue priority;
- discrete order updates;
- finite order sizes.

For the backtest, the authors round quotes to ticks and leave orders unchanged for a period \(\Delta t\), unless a fill changes inventory. They explicitly note that changing orders too often reduces the probability of execution because it sacrifices priority. 

This is a subtle but valuable lesson:

> The frequency with which a strategy recomputes an optimal action is not necessarily the frequency with which it should modify its live order.

There are two clocks:

\[
\text{decision recomputation clock}
\]

and:

\[
\text{market-action update clock}
\]

They should not automatically be identical.

A theoretically more current quote may be economically worse after accounting for:

- lost queue position;
- cancel latency;
- replacement latency;
- message-rate limits;
- fill probability during the transition;
- information leakage.

The persistence of an existing action has option value.

---

# 10. The backtest should not be treated as persuasive evidence

The empirical section is illustrative, not a convincing validation of the model.

It uses:

- one stock;
- one trading day;
- a risk-aversion parameter selected to keep inventory roughly within a desired range;
- full fills under simplified trade-through conditions;
- no realistic queue-position model;
- \(A\) and \(k\) held independent of the prevailing spread;
- algorithm details deliberately withheld.

The authors themselves say their goal is to exemplify use of the model, not present a comprehensive empirical demonstration. 

So the paper’s value is primarily:

- conceptual;
- mathematical;
- architectural.

Its one-day P&L chart is not the reason to believe the framework.

---

# What not to import literally

The model makes aggressive simplifying assumptions:

\[
dS_t=\mu\,dt+\sigma\,dW_t
\]

\[
\lambda(\delta)=Ae^{-k\delta}
\]

along with:

- one instrument;
- constant trade size;
- symmetric bid/ask arrival functions;
- exogenous reference price in the base model;
- CARA utility;
- simple inventory limits;
- no explicit queue model;
- no stochastic spread;
- no rich order-book state;
- no changing volatility;
- no cross-asset risk;
- no passive market impact in the final implementation.

The authors explicitly note that the exponential intensity assumption is mainly suitable for liquid, small-spread stocks and identify more general intensity functions and passive impact as unresolved extensions. 

The literal formulas are therefore less important than the decomposition that produced them.

---

# The transferable architecture for Money Machine

I would extract the paper into five first-class objects.

## 1. Preferred inventory

\[
q_t^*
=
f(
\text{forecast},
\text{risk},
\text{volatility}
)
\]

In the paper’s drift approximation:

\[
q_t^*=\frac{\mu_t}{\gamma\sigma_t^2}
\]

## 2. Inventory error

\[
\boxed{
\varepsilon_t=q_t^*-q_t
}
\]

This is the central state variable connecting prediction to positioning.

## 3. Inventory-control intensity

\[
D_t
=
g(
\sigma_t,
\text{liquidity},
\text{fill rates},
\text{risk tolerance},
\text{horizon}
)
\]

This says how strongly the strategy should react to inventory error.

## 4. Action center

\[
\boxed{
r_t=S_t+D_t\varepsilon_t
}
\]

In a market maker this is the quote center. In a directional system it might instead control:

- marginal buy/sell value;
- acceptable execution price;
- aggressiveness;
- order asymmetry;
- desired rate of position change.

## 5. Action width

\[
w_t
=
h(
\text{uncertainty},
\text{costs},
\text{adverse selection},
\text{fill dynamics}
)
\]

This determines how much compensation is needed before acting.

That separation gives you:

\[
\boxed{
\text{where the strategy wants to lean}
}
\]

independently from:

\[
\boxed{
\text{how cautious it should be while leaning there}
}
\]

Your current signal-to-position mapper may be compressing both into one scalar target.

---

# The connection to the Citadel slide

The Citadel toy was:

\[
out=e-\lambda q
\]

or:

\[
out=\lambda(q^*-q)
\]

The paper’s approximate quote-center policy is:

\[
r-S=D(q^*-q)
\]

They share the same primitive:

\[
\boxed{
\text{desired inventory}-\text{current inventory}
}
\]

But they expose it through different controls:

| Framework | Controlled output |
|---|---|
| Citadel toy | Marginal signal |
| Guéant–Lehalle–Fernandez-Tapia | Bid/ask quote center |
| Money Machine today | Target position |
| Possible Money Machine redesign | Marginal action values, execution prices, speed and size |

That is the single most useful extraction from the paper.


\text{forecast and current inventory meet through an inventory-error state before execution is chosen}
}
\]

That is the conceptual bridge between the paper, the Citadel function, and the gap you have been feeling in Money Machine’s positioning architecture.