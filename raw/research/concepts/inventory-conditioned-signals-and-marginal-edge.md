# Inventory-Conditioned Signals and Marginal Edge

## Status

Research note for potential integration into Money Machine.

## Origin

This note was prompted by a simplified C++ example shown in a Citadel Securities presentation on vectorization:

```cpp
void update_signals(
    const double* fair,
    const double* mid,
    const double* position,
    double* out,
    size_t n
) {
    for (size_t i = 0; i < n; ++i) {
        out[i] = fair[i] - mid[i] - 0.01 * position[i];
    }
}
```

The example is deliberately simple, but it exposes a useful way of representing a trading signal:


\boxed{
S(q)=fair-mid-\lambda q
}


This differs meaningfully from a conventional architecture in which a scalar signal magnitude is mapped directly into a target position.

The important lesson is not the literal coefficient or formula. It is the underlying representation:

> A signal can represent the marginal desirability of changing inventory from the position currently held.

Position is therefore not merely the output of the signal system. It is part of the state used to compute the signal.

---



# 1. Core Variables

Define:


e=fair-mid


where:

- fair is the model's estimated fair value;
- mid is the current market midpoint;
- e is the raw estimated price edge;
- q is the current position;
- \lambda is the marginal inventory-penalty coefficient;
- S(q) is the resulting inventory-conditioned signal.

The signal is:


\boxed{
S(q)=e-\lambda q
}


The two terms have distinct meanings:


\text{raw edge}=e



\text{inventory pressure}=\lambda q



\text{net marginal signal}=e-\lambda q


This decomposition should remain explicit rather than being collapsed prematurely into one target-position number.

---



# 2. Interpretation One: Inventory-Adjusted Edge

The raw edge is:


e=fair-mid


If fair value is above the market midpoint, the raw edge is positive:


fair>mid
\Rightarrow
e>0


This says the asset appears cheap relative to the model's estimate.

The inventory term modifies that opportunity according to the exposure already held:


S(q)=e-\lambda q


For a long position:


q>0
\Rightarrow
-\lambda q<0


The signal becomes less positive as long inventory accumulates.

For a short position:


q<0
\Rightarrow
-\lambda q>0


The signal becomes more positive because buying would both capture the forecast edge and reduce the short.

The same forecast therefore produces different actions depending on current inventory:


S(e,0)\neq S(e,q_{\text{long}})\neq S(e,q_{\text{short}})


This makes the signal explicitly state-dependent.

## Example

Suppose:


fair=100.20



mid=100.00



e=0.20


and:


\lambda=0.01


Then:


| Current position q | Signal S(q) | Interpretation                                  |
| ------------------ | ----------- | ----------------------------------------------- |
| -10                | 0.30        | Strong incentive to buy                         |
| 0                  | 0.20        | Positive raw opportunity                        |
| 10                 | 0.10        | Still attractive, but less so                   |
| 20                 | 0.00        | Inventory is at equilibrium                     |
| 30                 | -0.10       | Position is too large despite positive raw edge |


The model can therefore prefer selling even while its fair-value estimate remains above the market.

That is not a contradiction. It means:

> The asset may still be attractive in isolation, while another unit is unattractive given current exposure.

---



# 3. Interpretation Two: An Implicit Position Target

The equilibrium position is the position at which the marginal signal reaches zero:


S(q^*)=0


Therefore:


e-\lambda q^*=0


and:


\boxed{
q^*=\frac{e}{\lambda}
}


The function can then be rewritten as:

# 
S(q)

e-\lambda q


# 
S(q)

\lambda q^*-\lambda q



\boxed{
S(q)=\lambda(q^*-q)
}


This shows that the Citadel example contains an implicit target-position mapping:


q^*=\frac{fair-mid}{\lambda}


However, the target is not the complete output. The function retains the residual between the target and the current position:


q^*-q


It also retains the strength with which deviations from the target matter:


\lambda


This is richer than outputting q^* alone.

---



# 4. Why a Target Alone Loses Information

A traditional signal-to-position architecture can be written as:


x
\rightarrow
s
\rightarrow
q^*=g(s)


where:

- x is market state;
- s is a scalar model signal;
- g maps the signal into a target position.

Once the output becomes only:


q^*


the downstream system may no longer know:

- why the target has that value;
- how much raw edge produced it;
- how inventory risk affected it;
- how rapidly desirability decays as inventory grows;
- whether the target resulted from clipping or saturation;
- whether it resulted from a hard position limit;
- whether the mapping was linear or nonlinear;
- how valuable the next incremental unit is;
- how urgently the system should move toward the target.



## Same target, different geometry

Consider two signal fields:


S_1(q)=0.01(20-q)


and:


S_2(q)=0.50(20-q)


Both have the same equilibrium:


q^*=20


A target-only interface represents both as:


q^*=20


But the systems are not economically equivalent.

At:


q=10


the first produces:


S_1(10)=0.10


while the second produces:


S_2(10)=5.00


Both point toward the same destination, but they express radically different marginal conviction, urgency and sensitivity.

The target preserves the zero crossing.

It does not preserve the surrounding topology.

---



# 5. Interpretation Three: The Gradient of an Objective

Consider the objective:


J(q)=eq-\frac{1}{2}\lambda q^2


The first term represents expected value from holding the position:


eq


The second term represents a quadratic penalty on inventory:


\frac{1}{2}\lambda q^2


Differentiating with respect to position gives:

# 
\frac{\partial J}{\partial q}

e-\lambda q


Therefore:


\boxed{
S(q)=\frac{\partial J}{\partial q}
}


The signal is the local gradient of the strategy objective over position space.

It answers:

- Would adding one unit improve the objective?
- Would removing one unit improve it?
- How much does the objective improve locally?
- At what position does the incentive to change inventory disappear?
- How quickly does marginal desirability decay as inventory accumulates?

The sign determines direction:


S(q)>0
\Rightarrow
\text{increasing position improves the objective}



S(q)<0
\Rightarrow
\text{decreasing position improves the objective}



S(q)=0
\Rightarrow
\text{current position is locally optimal}


The second derivative is:

# 
\frac{\partial^2 J}{\partial q^2}

-\lambda


For:


\lambda>0


the objective is concave and has a unique optimum:


q^*=\frac{e}{\lambda}


This interpretation is more general than the literal linear formula.

Instead of thinking only in terms of:


\text{signal}\rightarrow\text{target}


the strategy can be represented as:


\text{market state}
\rightarrow
\text{objective over position space}
\rightarrow
\text{local marginal value}
\rightarrow
\text{execution}


---



# 6. Interpretation Four: Inventory-Adjusted Reservation Value

The original function can also be rearranged:

# 
S(q)

fair-mid-\lambda q


# 
S(q)

(fair-\lambda q)-mid


Define the inventory-conditioned reservation value:


\boxed{
r(q)=fair-\lambda q
}


Then:


\boxed{
S(q)=r(q)-mid
}


The model fair value and the reservation value are different objects.

## Model fair value


fair


This is the strategy's estimate of the asset's value independent of its own current inventory.

## Reservation value


r(q)


This is the value at which the strategy is personally indifferent to acquiring or disposing of additional inventory, given its existing exposure.

For a long position:


q>0
\Rightarrow
r(q)<fair


The strategy becomes:

- less willing to buy;
- more willing to add further long exposure;
- more willing to sell;
- more willing to quote below its unadjusted fair estimate.

For a short position:


q<0
\Rightarrow
r(q)>fair


The strategy becomes:

- more willing to buy;
- less willing to sell;
- more motivated to reduce the short.

This creates a useful conceptual separation:


\boxed{
\text{market-value estimate}
\neq
\text{inventory-conditioned trading value}
}


A strategy can maintain the same forecast while changing its behavior because its internal balance-sheet state has changed.

---



# 7. Signals as Fields Over Position Space

A scalar position target is a point:


q^*


An inventory-conditioned signal is a function:


S(q)


It assigns a marginal value to every possible position.

This can be viewed as a field over position space.

For the linear case:


S(q)=e-\lambda q


the field is a downward-sloping line.

The important properties are:

## Intercept


S(0)=e


This is the raw opportunity while flat.

## Slope

# 
\frac{\partial S}{\partial q}

-\lambda


This determines how quickly desirability decays as inventory accumulates.

## Zero crossing


S(q^*)=0


This determines the equilibrium position.

A target-only representation retains the zero crossing but may discard the intercept, slope and functional shape.

More generally:


\boxed{
S(q)=e-R'(q)
}


where:

- R(q) is a position-risk or inventory-cost function;
- R'(q) is its marginal penalty.

The corresponding objective is:


J(q)=eq-R(q)


and:


S(q)=\frac{\partial J}{\partial q}


This allows nonlinear position geometry without changing the conceptual architecture.

---



# 8. Nonlinear Inventory Geometry

The Citadel slide uses a linear marginal inventory penalty:


R'(q)=\lambda q


This comes from a quadratic total penalty:


R(q)=\frac{1}{2}\lambda q^2


Production systems may require richer shapes.

## Increasingly aggressive penalty near limits

For example:

# 
R(q)

\frac{1}{2}\lambda q^2
+
\frac{1}{4}\eta q^4


Then:

# 
S(q)

e-\lambda q-\eta q^3


The cubic term is small near zero but grows rapidly at large positions.

This provides:

- relatively permissive behavior at low inventory;
- increasingly strong resistance as exposure grows;
- smooth behavior before reaching a hard position limit.



## Soft barrier near a maximum position

If the maximum allowed absolute position is q_{\max}, one possible penalty is:

# 
R(q)

-\kappa
\log\left(
1-\frac{q^2}{q_{\max}^2}
\right)


Its marginal penalty grows sharply as:


|q|\rightarrow q_{\max}


This creates a smooth barrier rather than relying only on final-stage clipping.

## Asymmetric long and short penalties

The strategy may use different marginal penalties depending on direction:


S(q)=
\begin{cases}
e-\lambda_{\text{long}}q, & q\geq 0 [4pt]
e-\lambda_{\text{short}}q, & q<0
\end{cases}


This may be appropriate when:

- upside and downside risks differ;
- borrow or funding costs are asymmetric;
- shorting constraints exist;
- liquidity differs by trading direction;
- the underlying distribution is skewed;
- portfolio exposure is asymmetric.

The broader lesson is that target sizing is determined by the shape of an objective, not necessarily by a standalone mapping table.

---



# 9. Dimensional Consistency

The variables must use compatible units.

Suppose:

- fair-mid is measured in dollars per asset unit;
- q is measured in asset units.

Then:


S(q)


is also measured in dollars per additional asset unit.

For:


\lambda q


to have the same units as e, \lambda must have units:


\frac{\text{dollars}}
{\text{asset unit}^2}


In the objective:


J(q)=eq-\frac{1}{2}\lambda q^2


the units are:

# 
\left(
\frac{\text{dollars}}{\text{unit}}
\right)
(\text{units})

\text{dollars}


and:

# 
\left(
\frac{\text{dollars}}{\text{unit}^2}
\right)
(\text{units}^2)

\text{dollars}


Therefore J(q) can be interpreted as expected economic value over the selected forecast horizon.

A coefficient such as `0.01` is meaningless without knowing:

- the units of position;
- whether position is contracts, shares, dollars or normalized risk;
- the price units;
- the forecast horizon;
- whether the edge is a price difference, return or standardized score;
- whether the signal has already been volatility-scaled.

Money Machine should make these units explicit.

---



# 10. Separating Forecast, Risk and Execution

A useful architecture separates three conceptually distinct layers.

## Layer 1: Forecast or raw opportunity


e_t=fair_t-mid_t


This describes the market opportunity independent of current inventory.

Possible outputs include:

- expected price change;
- expected return;
- estimated terminal fair price;
- expected markout;
- expected spread capture;
- relative-value residual.



## Layer 2: Inventory-conditioned marginal value

# 
S_t(q_t)

e_t-R'_t(q_t)


This combines the opportunity with the current state of the portfolio.

The output answers:

> What is one additional unit worth from the position currently held?



## Layer 3: Execution

# 
a_t

E(
S_t,
cost_t,
liquidity_t,
constraints_t
)


The execution layer determines how to act on the marginal value.

It may control:

- whether to trade;
- order size;
- order aggressiveness;
- limit price;
- quote skew;
- participation rate;
- venue selection;
- passive versus aggressive execution;
- urgency;
- cancellation and replacement behavior.

The execution system should not need to reconstruct the economic meaning of a compressed target-position mapping.

---



# 11. Transaction Costs and the No-Trade Region

The simple formula excludes:

- spread;
- fees;
- rebates;
- slippage;
- market impact;
- adverse selection;
- latency risk;
- opportunity cost.

Let:


c_{\text{buy}}


be the marginal cost of buying, and:


c_{\text{sell}}


be the marginal cost of selling.

Then:


S(q)>c_{\text{buy}}


indicates that buying has positive net marginal value.

Likewise:


S(q)<-c_{\text{sell}}


indicates that selling has positive net marginal value.

Otherwise, the strategy remains inside a no-trade region:


-c_{\text{sell}}
\leq
S(q)
\leq
c_{\text{buy}}


A simplified action rule is:


action=
\begin{cases}
buy, & S(q)>c_{\text{buy}} [4pt]
sell, & S(q)<-c_{\text{sell}} [4pt]
hold, & \text{otherwise}
\end{cases}


This avoids unnecessary turnover when the improvement in the objective is smaller than the cost of changing position.

The target may therefore remain unchanged while execution rationally does nothing.

---



# 12. Dynamic Behavior

The signal naturally creates a feedback controller.

Suppose the execution rule is approximately:

# 
\Delta q_t

kS_t(q_t)


where k converts marginal signal into a position adjustment.

Using:

# 
S_t(q_t)

\lambda(q_t^*-q_t)


gives:

# 
\Delta q_t

k\lambda(q_t^*-q_t)


The strategy moves toward the equilibrium position rather than jumping to it instantaneously.

This creates a closed feedback loop:


\text{forecast}
\rightarrow
\text{marginal signal}
\rightarrow
\text{trade}
\rightarrow
\text{new position}
\rightarrow
\text{new marginal signal}


As the position approaches the equilibrium:


q_t\rightarrow q_t^*


the signal decreases:


S_t(q_t)\rightarrow 0


This produces self-limiting behavior.

A target-position architecture can also implement gradual convergence, but the marginal-signal representation makes the feedback structure explicit.

---



# 13. Multi-Asset Generalization

The scalar model assumes that every instrument can be treated independently.

Let:

- \mathbf e be the vector of raw expected edges;
- \mathbf q be the vector of positions;
- \mathbf\Lambda be a matrix describing marginal portfolio risk.

Define the objective:

# 
J(\mathbf q)

## \mathbf e^\top\mathbf q

\frac{1}{2}
\mathbf q^\top
\mathbf\Lambda
\mathbf q


The gradient is:

# 
\boxed{
\nabla J(\mathbf q)

\mathbf e-\mathbf\Lambda\mathbf q
}


The unconstrained optimum is:

# 
\boxed{
\mathbf q^*

\mathbf\Lambda^{-1}\mathbf e
}


The off-diagonal elements of \mathbf\Lambda represent interactions between positions.

This allows the marginal signal for one instrument to depend on exposure elsewhere in the portfolio.

Possible components include:

- return covariance;
- common-factor exposure;
- beta exposure;
- sector concentration;
- duration;
- delta, gamma or vega;
- exchange exposure;
- venue exposure;
- funding exposure;
- counterparty exposure;
- liquidity concentration;
- strategy correlation.

The scalar Citadel example is equivalent to:

# 
\mathbf\Lambda

\lambda\mathbf I


This assumes:

- identical inventory penalty across instruments;
- no cross-asset interactions;
- no covariance;
- no differences in volatility or liquidity.

The matrix form is the natural portfolio-level generalization.

---



# 14. Comparison With Money Machine's Current Representation



## Current conceptual form

Money Machine currently behaves approximately as:


signal
\rightarrow
position\ target


or:


q^*=g(s)


This answers:

> Given the current signal magnitude, what position should be held?



## Inventory-conditioned form

The alternative representation is:


S(q)=e-R'(q)


This answers:

> Given the current opportunity and current inventory, what is the marginal value of changing the position?



## Main distinction

The current method treats position mainly as a destination.

The alternative method treats position as a coordinate in the strategy's state space.

The same raw market forecast can therefore produce different signals depending on where the system currently sits.

## Information potentially lost by early target compression

When all information is compressed into q^*, the system may lose or obscure:

- raw model edge;
- current inventory pressure;
- marginal value of an incremental trade;
- local slope around the current position;
- shape of the objective;
- distance from equilibrium;
- strength of convergence;
- reason for the target;
- execution urgency;
- sensitivity to position changes;
- distinctions between clipping and genuine economic equilibrium.

The issue is not that target positions are inherently wrong.

The issue is that the target should be treated as one derived property of a richer signal surface, rather than necessarily being the only interface between forecasting and execution.

---



# 15. Proposed Money Machine Representation

A clean internal representation could preserve the following objects separately:

```cpp
struct MarginalSignal {
    double raw_edge;
    double inventory_penalty;
    double marginal_execution_cost;
    double net_marginal_value;

    double current_position;
    double equilibrium_position;

    double local_inventory_slope;
};
```

With a linear model:

```cpp
MarginalSignal update_signal(
    double fair,
    double mid,
    double position,
    double lambda,
    double marginal_execution_cost
) {
    const double raw_edge = fair - mid;
    const double inventory_penalty = lambda * position;
    const double net_before_cost = raw_edge - inventory_penalty;

    const double equilibrium_position =
        lambda > 0.0
            ? raw_edge / lambda
            : 0.0;

    return {
        .raw_edge = raw_edge,
        .inventory_penalty = inventory_penalty,
        .marginal_execution_cost = marginal_execution_cost,
        .net_marginal_value =
            net_before_cost - marginal_execution_cost,
        .current_position = position,
        .equilibrium_position = equilibrium_position,
        .local_inventory_slope = -lambda,
    };
}
```

The exact execution-cost treatment will need to distinguish buy and sell directions. The purpose of the structure is to preserve decomposition rather than immediately collapsing everything into one position number.

---



# 16. A More General Interface

A more general design would treat the inventory penalty as a function:

```cpp
struct SignalState {
    double raw_edge;
    double current_position;
    double marginal_inventory_penalty;
    double marginal_value;
};

template <typename InventoryPenalty>
SignalState evaluate_signal(
    double raw_edge,
    double position,
    InventoryPenalty&& penalty
) {
    const double marginal_penalty = penalty(position);

    return {
        .raw_edge = raw_edge,
        .current_position = position,
        .marginal_inventory_penalty = marginal_penalty,
        .marginal_value = raw_edge - marginal_penalty,
    };
}
```

Examples of penalty functions:

```cpp
auto linear_penalty = [lambda](double q) {
    return lambda * q;
};
```

```cpp
auto nonlinear_penalty = [lambda, eta](double q) {
    return lambda * q + eta * q * q * q;
};
```

This allows Money Machine to experiment with different position geometries without rewriting the forecast model or execution engine.

---



# 17. Recommended Diagnostics

To understand the new representation, Money Machine should log more than the final target or trade.

At each decision point, record:

- raw model edge;
- current mid;
- estimated fair value;
- current position;
- inventory penalty;
- execution-cost estimate;
- net marginal signal;
- implied equilibrium position;
- local slope with respect to position;
- actual position change;
- realized execution price;
- subsequent markout;
- realized P&L;
- active constraints;
- whether the strategy was inside the no-trade region.

Useful diagnostic identities include:


q^*=\frac{e}{\lambda}



S(q)=\lambda(q^*-q)



\frac{\partial S}{\partial q}=-\lambda


Logging these separately makes it possible to determine whether performance came from:

- the forecast;
- the inventory model;
- cost estimation;
- execution;
- risk constraints;
- parameter scaling.

---



# 18. Experimental Questions

The following questions should be tested rather than assumed.

## Representation

1. Does preserving raw edge and marginal inventory pressure improve execution decisions?
2. Does the current signal-to-position mapping hide useful information?
3. Can the existing mapping be represented as the zero crossing of a signal field?
4. What signal fields produce the same current target curve?



## Geometry

1. Is a linear inventory penalty sufficient?
2. Should the slope depend on volatility, liquidity or market regime?
3. Should inventory penalties become nonlinear near limits?
4. Should long and short penalties differ?
5. Should the field contain discontinuities or remain smooth?



## Execution

1. Does marginal value predict optimal aggressiveness better than target distance?
2. Should order size depend on S(q), q^*-q, or both?
3. How should spread and impact define the no-trade region?
4. How quickly should the controller converge toward equilibrium?
5. Does a marginal representation reduce turnover?



## Portfolio behavior

1. Should the penalty depend on individual position or portfolio factor exposure?
2. Can a matrix risk model replace independent per-asset penalties?
3. How should correlated positions alter the marginal value of a new trade?
4. How should capital, leverage and concentration constraints enter the field?



## Attribution

1. Can P&L be decomposed into forecast quality, sizing quality and execution quality?
2. Does the new representation make failure analysis easier?

---



# 19. Suggested Migration Path

A full architectural replacement is not required initially.

## Phase 1: Reconstruct the current mapping

For the existing function:


q^*=g(s)


calculate and log:

- current target q^*;
- current position q;
- target residual q^*-q;
- raw signal s;
- local slope of the mapping, where available.

This establishes the geometry of the current system.

## Phase 2: Add an equivalent marginal signal

Choose an initial slope \lambda and construct:


S(q)=\lambda(q^*-q)


This does not change the target behavior. It creates a marginal representation of the existing target mapper.

The execution layer can compare:

- decisions based on target distance;
- decisions based on marginal value;
- decisions based on both.



## Phase 3: Separate raw edge from inventory penalty

Replace:


S(q)=\lambda(q^*-q)


with:


S(q)=e-R'(q)


This makes the economic decomposition explicit.

## Phase 4: Add cost-aware execution

Introduce directional cost thresholds:


c_{\text{buy}}


and:


c_{\text{sell}}


and trade only when marginal value exceeds estimated marginal cost.

## Phase 5: Test nonlinear and portfolio-aware geometry

Evaluate:

- nonlinear inventory penalties;
- asymmetric penalties;
- dynamic coefficients;
- cross-asset risk matrices;
- soft barriers near limits.

The existing target-position implementation can remain as a benchmark throughout the migration.

---



# 20. Quantile Regression Extension



## Important separation

The quantile-regression methodology is not part of the lesson directly contained in the Citadel slide.

The slide's core lesson stands on its own:


\boxed{
\text{Represent the signal as inventory-conditioned marginal edge}
}


Money Machine's quantile-regression model is a separate extension that may provide a richer forecast distribution for constructing this signal field.

It should therefore be documented and evaluated separately.

## Quantile outputs

Suppose the model produces:


Q_{10},Q_{50},Q_{90}


These may represent quantiles of:

- future return;
- future price change;
- terminal price;
- future markout.

The exact interpretation must remain explicit.

## Possible uses

The median may provide a location estimate:


\mu=Q_{50}


The quantile widths provide distribution information:


d=Q_{50}-Q_{10}



u=Q_{90}-Q_{50}


This information could be used to construct:

- the fair-value estimate;
- the raw edge;
- uncertainty-sensitive inventory penalties;
- asymmetric long and short penalties;
- dynamic position limits;
- cost-aware execution thresholds.

One possible extension is:

# 
S(q)

\mu-\lambda_t q


where:


\lambda_t


depends on predicted uncertainty.

Another possible extension is:


S(q)=
\begin{cases}
\mu-\lambda_{\text{long},t}q,
& q\geq 0 [4pt]
\mu-\lambda_{\text{short},t}q,
& q<0
\end{cases}


where long-side risk is informed by the lower forecast tail and short-side risk by the upper tail.

These are Money Machine design possibilities. They should not be attributed to the Citadel example.

---



# 21. Conceptual Summary

The conventional representation is:


\boxed{
\text{signal magnitude}
\rightarrow
\text{target position}
}


The alternative representation is:

## 
\boxed{
\text{raw opportunity}

# \text{marginal inventory penalty}

\text{marginal value of changing position}
}


The linear example is:


S(q)=fair-mid-\lambda q


This single equation can be interpreted as:

1. an inventory-adjusted edge;
2. a residual relative to an implicit target position;
3. the gradient of a position objective;
4. the difference between an inventory-adjusted reservation value and market mid.

The equilibrium target is:


q^*=\frac{fair-mid}{\lambda}


but the target is only one feature of the signal field.

The richer object is:


S(q)


because it preserves:

- direction;
- marginal value;
- distance from equilibrium;
- inventory sensitivity;
- local objective geometry;
- the decomposition between forecast and risk.

The deepest architectural lesson is:

> Position should not necessarily appear only at the end of the strategy pipeline. It can feed back into the signal itself.

Or, more formally:


\boxed{
\text{A trading signal can be a field over position space, not merely a scalar instruction or target.}
}


---



# 22. Working Design Principle for Money Machine

Money Machine should explore preserving the following objects as distinct first-class values:


\text{forecast edge}



\text{inventory-conditioned marginal penalty}



\text{net marginal trading value}



\text{equilibrium position}



\text{execution cost}



\text{actual execution action}


A target position may still be calculated and used.

It should not necessarily be the only representation passed downstream.

The working hypothesis is:

> Preserving the topology of the signal over position space will improve interpretability, execution control, risk integration and the ability to use richer predictive distributions without prematurely compressing their information.

