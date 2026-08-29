# P_Max

Status: working draft — basis for a formal write-up

Purpose: Money Machine's foundational model of market opportunity. P_Max asserts that extractable value in a price series is a computable positive quantity, and that the research problem is not *whether* value exists but *which constraints prevent its capture*. This page holds the original statement, the formal definitions that follow from it, and the open problems.

This is an asset-class-agnostic theory. Nothing below depends on a particular venue, instrument, or market structure.

Related: [[trading/concepts|Trading Concepts]] · [[trading/catalog_v1|Trading Catalog]]

---

## 1. Original statement

Destin's original formulation, preserved:

> P_Max is an optimization function used to calculate the maximum extractable value of any asset's price time series.
>
> One proposed way of measuring the value is by analyzing the series at a granular level, for example 1 min time frames or less, and adding the sum of all cumulative price movements.
>
> Under perfect conditions and prediction it's theoretically possible to capture it all.
>
> **The hypothesis then, is to work backwards from the maximum to prove why you can't capture it all.**
>
> P_MAX has extended to an overarching concept of optimization: when given a set of decisions and trade offs you should optimize for profit.

The fourth sentence is the operative one. It defines a methodology, not just a quantity.

## 2. The consequence for research epistemics

Under P_Max there is **no null hypothesis.**

The extractable value of a non-constant price series is positive by construction. "There is no edge here" is therefore not a finding — it is a failure to complete the analysis. The valid output of any research task is a **gap decomposition**: how much of the available value was lost, and to which constraint.

This is the standard Money Machine research protocol. An agent that returns a verdict on whether an edge exists has answered a question the framework does not ask.

## 3. Notation

| symbol | meaning |
|---|---|
| `T` | length of the evaluation window |
| `Δt` | action resolution — the shortest interval at which a decision can be made *and executed* |
| `σ` | volatility per unit time |
| `c` | round-trip transaction cost, as a fraction of price (fees + spread) |
| `φ` | policy efficiency — fraction of each available move the strategy actually captures |
| `Q` | position size |
| `v` | market volume rate (volume per unit time) |
| `k` | market impact coefficient |

## 4. Naive P_Max

**Naive P_Max** is P_Max computed on price alone, ignoring the actor's effect on the market. It is the correct model whenever participation is small enough that impact is negligible.

### 4.1 It requires a stated resolution

The original phrasing — *"the maximum extractable value"* — is unbounded as written. Summing absolute price movements is the **total variation** of the path, and for any diffusion-like process total variation diverges as sampling resolution goes to zero:

```
TV(Δt)  =  (T/Δt) · E|ΔP|  =  (T/Δt) · σ√Δt · √(2/π)  =  σT√(2/π) · Δt^(−1/2)   →   ∞   as Δt → 0
```

(First-order variation diverges; quadratic variation converges, which is realized volatility. They are different objects.)

So the unconstrained quantity is a **supremum that is never attained**, not a maximum. Every finer resolution beats the last.

The fix is to make resolution explicit:

> **P_Max(Δt)** — the maximum extractable value at action resolution `Δt`.

Now the quantity is finite, computable, and honestly named. This is the general pattern in the theory: *an unbounded optimum means a constraint has not yet been written down.* The constraints are the content.

Consequence worth stating plainly: **P_Max is not a property of the price series.** It is a property of the series *and* the actor's capabilities. Faster execution does not make you more efficient against a fixed ceiling — it raises the ceiling.

### 4.2 Costs create an interior optimum

Gross opportunity grows as resolution gets finer, but so does the number of round trips:

```
gross(Δt)  =  φ · σT√(2/π) · Δt^(−1/2)        grows as Δt^(−1/2)
cost(Δt)   =  c · T · Δt^(−1)                 grows as Δt^(−1)
```

Cost diverges faster. Net value therefore rises, peaks, and collapses. Setting `d/dΔt [gross − cost] = 0`:

```
                    2π c²
        Δt*  =  ───────────
                   φ² σ²
```

**The theory yields a computable optimal trading frequency**, per asset, from volatility and cost structure alone.

Worked example — 50% annualized volatility, 5bp round-trip cost, `φ = 1`:

```
σ_daily = 0.50/√365 = 0.0262
Δt*     = 2π(0.0005)² / (0.0262)²  =  0.0023 days  ≈  3.3 minutes
```

At 1bp round-trip cost the same asset optimizes near 8 seconds. At 100% annualized volatility and 5bp, near 50 seconds. The formula behaves correctly in both directions: **more volatile → trade faster; more expensive → trade slower.**

### 4.3 Policy efficiency compounds into speed

Because `Δt* ∝ 1/φ²`, doubling capture efficiency reduces the optimal timeframe by a factor of four. Timeframes that were cost-dominated become viable once the exit policy improves.

This has a practical ordering consequence: **improve φ before buying speed.** Infrastructure purchased ahead of policy efficiency operates below its own cost floor.

## 5. The constraint ladder

The methodology — *work backwards from the maximum* — is a ladder of successively constrained maxima. Each rung's drop is a named loss with a magnitude.

| rung | constraints applied | interpretation |
|---|---|---|
| `P_Max(∞)` | none | diverges; discard |
| `P_Max(Δt)` | action resolution | theoretical ceiling at your speed |
| `P_Max(Δt, c)` | + transaction costs | **what is actually on the table** |
| `P_Max(Δt, c, causal)` | + only information available at decision time | ceiling for any automated system |
| `P_Max(Δt, c, causal, φ)` | + your actual policy | realized |

Losses sort into three categories:

- **information** — the move required knowledge unavailable at the decision bar. Irreducible.
- **cost** — fees, spread, funding, slippage. Reducible by venue, execution, or frequency choice.
- **policy** — the move was visible and affordable, and entry/exit/sizing left it on the table. Fully reducible, and where most current gap lives.

### 5.1 Capture ratio

```
capture  =  realized_pnl / P_Max(Δt, c)
```

The denominator must be pinned at the actor's own action resolution; measured against the unconstrained supremum, capture is identically zero. Two useful readings follow:

- capture at your own resolution → a fair scorecard for policy
- capture at a finer resolution → the value of faster infrastructure, denominated in currency

### 5.2 Rung 3 is exactly computable

`P_Max(Δt, c)` is not an estimate. Perfect-foresight optimal trading with costs, holding one position at a time, is a dynamic program over `(bar, position ∈ {flat, long, short})`, solvable in `O(3N)` for an `N`-bar window.

This makes capture ratio a hard number rather than a philosophical quantity, and running the DP across several `Δt` produces the empirical version of the `Δt*` result in §4.2 — the curve can be observed rather than assumed.

## 6. P_Max proper — the volume ceiling

Naive P_Max assumes the actor can trade any size at the observed price. A real participant cannot: they are bounded by market volume, and their own trading moves price against them.

Two distinct constraints, often conflated:

- **participation cap** — an actor can be at most some fraction of volume in a time slice. A hard wall on throughput.
- **market impact** — trading moves price adversely, degrading realized fills. A slope, not a wall.

### 6.1 P_Max stops being scale-free

Naive P_Max is expressed as a return and is therefore independent of capital. Once volume enters, **P_Max becomes a concave function of deployed capital.** This is the quantity that determines whether a strategy is worth building — not whether it has edge, but how large it can become before it stops working.

### 6.2 Impact is resolution-independent, size-dependent

Under the square-root impact law, with volume proportional to time (`V ≈ v·Δt`) and interval volatility `σ√Δt`:

```
impact  ≈  k · σ√Δt · √(Q / (v·Δt))  =  k · σ · √(Q/v)
```

The `Δt` cancels. **Impact per round trip is independent of timeframe** — it depends only on size relative to the volume rate. Total impact over the window still scales as `Δt^(−1)`, the same exponent as fixed costs, so impact folds cleanly into an effective cost:

```
c_eff  =  c  +  k · σ · √(Q/v)
```

### 6.3 Size and speed are one decision

Substituting `c_eff` into §4.2, in the regime where impact dominates fees:

```
Δt*  ∝  Q / v
```

**Optimal timeframe scales linearly with size relative to market volume.** Double the position, halve the speed. The theory reproduces a known structural fact — large funds trade slower than small ones — from first principles, and establishes that position size and trading frequency cannot be chosen independently.

### 6.4 Capacity

Gross scales linearly in `Q`. Impact cost scales as `Q^(3/2)` — more size per trip, and each trip more expensive:

```
net(Q)  =  a·Q  −  b·Q^(3/2)         →         Q*  =  4a² / 9b²
```

An interior optimum in size. Past `Q*`, the actor pays the market more than it extracts. This is the strategy's **capacity**.

## 7. Status of each result

| result | status |
|---|---|
| total variation diverges as `Δt → 0` | proven for diffusions; holds broadly |
| `P_Max(Δt, c)` computable by DP | exact, constructive |
| `Δt* = 2πc²/(φ²σ²)` | derived under diffusive scaling and fixed `φ`; idealized |
| `Δt* ∝ 1/φ²` | follows from the above |
| impact resolution-independence | derived from square-root law; law is empirical, not theoretical |
| `Δt* ∝ Q/v` | derived; inherits the square-root assumption |
| `Q* = 4a²/9b²` | derived; inherits the square-root assumption |

## 8. Open problems

1. **The `φ` idealization.** §4.2 assumes a fixed fraction of *every* increment is captured, which no real policy achieves. The closed form is an intuition-builder; the DP at rung 3 is the rigorous statement. A policy-aware derivation of `Δt*` is open.

2. **Microstructure noise.** At very fine resolution, total variation is dominated by bid-ask bounce rather than tradeable movement. Naive P_Max at ultra-fine `Δt` measures noise. Where the crossover sits — the resolution below which additional variation is untradeable in principle — is unresolved and probably asset-specific.

3. **Non-diffusive dynamics.** Real series have fat tails, trends, and volatility clustering. The `√Δt` scaling in §4.2 is an approximation whose error has not been characterized.

4. **Estimating `k`.** The impact coefficient is venue- and size-specific and unstable across regimes. Where full order-book data exists, impact can be measured directly by walking the book rather than assuming a functional form; where only trade prints exist, it must be estimated. Both paths should be specified.

5. **Multi-position generalization.** The rung-3 DP assumes one position at a time. Extending to concurrent positions, portfolio constraints, and shared capital is unsolved and interacts with §6.

6. **Where the volume ceiling begins to bind.** For small participation, naive P_Max is correct and the §6 machinery is unnecessary. Computing the capital threshold at which impact becomes material is a prerequisite to knowing when this layer matters.
