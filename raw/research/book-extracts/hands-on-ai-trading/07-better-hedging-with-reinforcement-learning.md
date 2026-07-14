---
title: "Better Hedging with Reinforcement Learning"
chapter: 7
source: "Hands-On AI Trading with Python, QuantConnect, and AWS"
source_file: "OPS/c007.xhtml"
status: "extracted"
---

# Chapter 7: Better Hedging with Reinforcement Learning

## Overview

The chapter presents a practical, deliberately small reinforcement-learning (RL) system for hedging call options. Rather than learn an unbounded PnL objective from scratch, the policy network is first primed on simulated Black–Scholes–Merton (BSM) delta targets and then refined on recent option and stock prices using a downside-only PnL penalty. The implementation uses PyTorch and QuantConnect, daily AAPL data, and a three-variable state. It is compared with static, theoretical delta, and numerical-delta hedging. (Source: pp. 281–304)

## Learning Objectives (Inferred)

- Explain why continuous frictionless BSM hedging is an imperfect practical benchmark. (Source: pp. 281–283)
- Formulate option hedging as a state–action policy-learning problem. (Source: pp. 284–292)
- Identify an underlying price process and use simulation to prime an RL policy. (Source: pp. 285–296)
- Define the policy state, action distribution, training targets, and refinement penalty. (Source: pp. 290–300)
- Implement and evaluate the two-stage QuantConnect/PyTorch workflow. (Source: pp. 288–303)
- Recognize data, non-stationarity, convergence, overfitting, and deployment limitations. (Source: pp. 283–304)

## Key Concepts

### Introduction

#### A New AI Trading Assistant

BSM transformed option trading by turning a few inputs—spot, expiry, risk-free rate, and estimated volatility—into a rapid theoretical price. Early market prices often differed from BSM values, but harvesting convergence required managing the option inventory's risk. The ideal BSM replication assumes continuous rebalancing, zero frictions, and fractional shares, conditions that remain unattainable even with modern low commissions, narrow spreads, fractional trading, and high-frequency infrastructure. BSM nevertheless became the dominant reference across option markets and other financial applications. (Source: pp. 281–282)

#### Continuous Hedging Is Not Required

Under shared beliefs about terminal outcomes, constant implied volatility, reasonable efficiency, and equilibrium expectations, prices may converge toward BSM without literal continuous hedging, but that convergence is risky rather than arbitrage-free. Empirical option surfaces violate the constant-volatility premise: implied volatility varies across strikes, forming smiles and usually negative skews. For comparable moneyness, out-of-the-money puts tend to carry higher implied volatility than out-of-the-money calls. (Source: pp. 282–283)

Heston-style stochastic volatility fits observed prices better but adds parameters, calibration cost, numerical pricing, and overfitting risk because fitted parameters vary by stock. Real hedging also bears commissions, fees, bid–ask spreads, market impact, and rounding-related over/under-hedging; costs differ by trader and require realistic distributional modeling. (Source: p. 283)

#### Machine Learning Comes to the Rescue

A deep network can incorporate transaction costs, liquidity, sentiment, and other empirical inputs excluded from simple structural models. RL extends this idea from pricing to an ex-ante hedging policy that can account for market frictions and inventory risk. The approach can apply to option combinations and structured notes, whose contingent coupons or principals embed options and therefore create issuer hedging needs. (Source: pp. 283–284)

#### A Simplified but Effective RL Approach

Industrial AI hedging can require large networks, large datasets, and extensive compute. The chapter instead uses a reduced network and smaller dataset suitable for an individual practitioner. It is available through QuantConnect; a local alternative is described as requiring a GPU, at least 16 GB RAM, and daily option/equity data. The treatment assumes familiarity with BSM, neural networks, and RL. (Source: pp. 284–285)

### Overview of the Reinforcement Learning

The four conceptual phases are: (1) identify the underlying price process, (2) train on simulation, (3) refine on real market data, and (4) test and implement. (Source: p. 285)

#### Identification

The “stock” denotes any risky reference asset or index. Its stochastic dynamics must be chosen and parameters estimated or calibrated accurately enough for the asset class. The example chooses geometric Brownian motion (GBM), whose simple statistics, closed-form BSM prices, and Greeks make it computationally attractive. Heston adds stochastic volatility and greater empirical flexibility but incurs substantial calibration and numerical cost. (Source: pp. 285–286)

#### Simulation

BSM/GBM simulation supplies abundant examples of the core no-arbitrage relationship. Daily simulated prices and daily hedges make replication discrete, unlike the continuous BSM ideal. Exact optimal discrete hedging can require costly stochastic PDE solutions; after training, a policy network maps current state to action with low latency. Simulators can incorporate known transaction-cost, liquidity, trend, and predictive processes, but cannot teach processes that were never represented—“unknown unknowns.” (Source: pp. 286–287)

#### Refinement Training on Actual Market Data

Real data can reveal persistent processes omitted from simulation. This is most promising where markets are less competitive and data are abundant, such as high-frequency settings with high infrastructure barriers. The chapter uses simulation as a theoretical prior, then fine-tunes on a short recent window because liquidity, costs, trends, and option-market structure evolve and are not stationary. (Source: p. 287)

#### Testing and Implementation

Data should be separated into training, validation, and out-of-sample evaluation. Financial markets continually provide new observations, enabling paper portfolios and forward tests. Live deployment does not end validation: expected state-conditional performance must be compared with realized results to find blind spots and errors. No AI hedge should be deployed without continuous testing, attribution, and refinement. (Source: pp. 287–288)

### Implementation on QuantConnect

The objective is to minimize variability in the PnL of a portfolio containing a short/hedged call and underlying shares. The **policy network** is the learned neural mapping from current state to next-period decision; the **agent** is the complete trading algorithm that uses this network in real time. The demonstration uses AAPL calls and stock with PyTorch. (Source: p. 288)

Project layout: `research.ipynb` runs training and tests; `main.py` defines `AIDeltaHedgingAlgorithm`; the `aihedging` project contains `model.py` (`AIDeltaHedgeModel`) and `policy.py` (network architecture). (Source: pp. 288–289)

#### Primary Research Notebook

The notebook constructs the model with contract durations 30–120 days and a 14-day minimum holding period; trains the base policy for 1,000 epochs; refines on AAPL daily data from December 19, 2023 through February 17, 2024 for 40 epochs; and tests a chosen strike level. Random seeds and CPU/GPU choice support reproducibility and available acceleration. (Source: pp. 289–290)

#### The Policy Network

**State:** three dimensions—moneyness, time to maturity, and the previous underlying-stock position. The code actually represents moneyness as $S/K-1$ in refinement and samples it on $[-1,1]$ in simulation; time-to-maturity is supplied as its square root in base training. The prose's verbal max-zero definition is inconsistent for calls (see Extraction Issues). (Source: pp. 290–291, 295, 299–300)

**Action:** a normal distribution over next-period hedge quantity, parameterized by network outputs `mu` and `sigma`. These names describe hedge-action mean and uncertainty, not asset-return drift and volatility. A reparameterized sample supplies the action and log probability. Sigmoid bounds both outputs; $10^{-12}$ is added to `sigma` to keep it positive. (Source: pp. 290–291)

**Architecture:** 3 inputs → 256 ReLU units → 256 ReLU units → 2 outputs. Adam uses learning rate $3\times10^{-4}$. The chosen action is passed forward as the next state's previous position; time to maturity falls by one day while moneyness changes with stock price. The author explicitly does not claim this small network is sufficient for the full hedging problem. (Source: pp. 290–292)

Option price is omitted from the base state because, under simulated BSM, it is determined by the other variables. Volume, spread, macro conditions, and other market features are also omitted; adding them requires both state expansion and plausible simulation processes. (Source: p. 290)

#### Model Functions

`AIDeltaHedgeModel` exposes initialization, `train_base_model`, `train_asset_model`, and `research_test`. Defaults include 10,000×1 simulated observations, commission 0.01, 30/120-day contract bounds, and 14-day minimum holding. Seeds are fixed to 1; tensors use float32; CUDA is used if available. (Source: pp. 292–293)

Base training initializes the policy, gets volatility and risk-free-rate inputs, generates fresh simulations each epoch, forges 75% training/25% test tensors, samples actions, minimizes MSE to the target, backpropagates with Adam, tracks in/out-of-sample loss, plots convergence, and saves the policy. (Source: pp. 293–295)

#### Generating Training Data Using Black–Scholes

The code implements call price and call delta using $d_1$, $d_2$, and the normal CDF. Volatility is estimated from historical equity data and the risk-free input from the FOMC primary credit rate. A single fixed AAPL volatility is used, though the author recommends training across multiple volatility assumptions. (Source: pp. 294–295)

Simulation draws time-to-maturity uniformly up to $31/252$ years, moneyness uniformly over $[-1,1]$, and prior position uniformly over $[0,1]$. The target is intentionally underhedged: `0.9 * delta + 0.1 * position`. State tensors concatenate moneyness, square-root time, and position. (Source: p. 295)

#### Target and Loss Function with Simulated Data

The first-stage target is a discrete, underhedged approximation to call delta. Delta is bounded from 0 to 1 for the call case and therefore easier and more stable to learn than unbounded, skewed option PnL. For derivatives without closed-form delta, a finite-difference estimate can replace the analytic target. The current state determines a next-period hedge before the next random price is known, so finite error versus either current or future delta is unavoidable. This phase primes rather than finishes the policy. (Source: pp. 295–296)

### Fine-Tuning with Market Data

Recent option and equity prices inject transaction costs, liquidity, trends, and other real conditions into the delta-primed policy. The refinement objective penalizes adverse changes in hedged-portfolio wealth. (Source: p. 296)

The code uses `penalty = ReLU(-change / wealth)`: negative percentage wealth changes are penalized; nonnegative changes are not. This asymmetric downside objective may preserve alpha-like gains, though hedging itself is not intended to create alpha. (Source: pp. 296–297)

#### Pick Your Poison: Price or Delta?

Stock and option prices are unbounded; option payoffs are nonlinear, skewed, and fat-tailed even under GBM returns. A pure PnL loss may require enormous high-quality datasets, networks, and epochs and may fail to converge. One alternative is clipped/regularized Q-learning, feasible with substantial data and compute. The book's alternative is two-stage regularization: delta simulation supplies a stable prior; recent market data makes small dynamic adjustments. This can chase recent history, but more simulation strengthens the prior. (Source: p. 297)

A rejected alternative combines delta-deviation and PnL-variance terms with a regularization weight. It requires hyperparameter tuning and risks in-sample overfitting if only historical data are used. (Source: p. 297)

#### Refinement with Real Data

`train_asset_model` ensures a base model exists, sets the research date to the end date to avoid look-ahead bias, seeds tradable prices, subscribes to raw equity data, calls `refit`, plots penalties, and optionally returns the equity symbol. (Source: pp. 298–299)

`refit` loads the base model, retrieves two years of data by default, switches to AdamW with learning rate $10^{-5}$, loops through selected strikes and nearest expiries, builds an option path, initializes position at zero and wealth at initial option invoice price, samples a daily action, computes hedge PnL less commission and option-price change, accumulates downside penalties, backpropagates, updates once per strike path, optionally saves the asset-specific policy, and returns epoch penalties. (Source: pp. 299–300)

### Results

Refinement uses AAPL and front 180-strike call observations from December 2023 to February 2024. Rolling from an expiring front contract to the next produces visible option-price discontinuities; the chapter argues this is acceptable because expiry state is updated and roll behavior becomes part of training. (Source: p. 300)

Base MSE converges rapidly both in and out of sample; similarity is unsurprising because both simulated subsets are identically distributed. The market-data penalty also converges quickly. (Source: pp. 300–301)

For the AAPL 180-strike May 17, 2024 call, AI actions track BSM delta but remain lower (roughly 0.33–0.36 versus delta around 0.50–0.54 in the figure). The explanation is asymmetric cost under uncertain forward delta and the earlier AAPL decline: catching up from a smaller hedge may be cheaper than overshooting. (Source: pp. 301–302)

In the displayed path, AI hedging has the highest cumulative hedging and net hedged-portfolio wealth. It has less variance than numerical hedging and variance similar to hold and discrete delta strategies. Numerical hedging is extremely unstable and ends deeply negative in both plots. These are demonstration-path results, not universal performance guarantees. (Source: pp. 302–303)

### Conclusion

The chapter concludes that a small two-stage model can work practically: first acquire a theoretical delta prior, then adjust it with a PnL penalty on real data. The method can substitute other underlying stochastic models and, because the policy is not tied to a structural option-pricing model during refinement, can learn persistent non-fundamental dynamics. Policies must be rolled forward as conditions evolve. Advanced policies may also imply a pricing kernel useful for option-price prediction. AI hedging remains early-stage. (Source: pp. 303–304)

## Mathematical Formulas and Quantitative Relationships

### MathML 1 (EQ 0032): Structured-Note Terminal Value

$$
V=
\begin{cases}
V_0+1.105(x-V_0), & x>V_0,\\
\min\!\left(0,\,x-0.8V_0\right), & x\le V_0.
\end{cases}
$$

- $V$: terminal principal value specified by the source payoff.
- $V_0$: initial value of the reference index.
- $x$: final reference-index value.
- $1.105$: upside participation/leverage factor.
- $0.8V_0$: 80% protection threshold/short-put strike.

**Purpose:** Illustrate an option-embedded structured note requiring hedging. **Conditions:** Apply the branch determined by whether $x$ exceeds $V_0$. **Interpretation:** Upside receives 110.5% participation; downside embeds a 20% buffer and put-spread-like exposure. The second branch as printed can produce nonpositive “principal,” so its economic labeling is questionable and is preserved rather than corrected. (Source: p. 284)

### MathML 2–4 (EQ 0033–0035): Structured-Note Symbols

The source separately encodes $V_0$, $x$, and $V_0$ as inline nodes defining the initial index, final index, and the 80%-strike reference. They are not additional equations. (Source: p. 284)

### MathML 5 (EQ 0036): Geometric Brownian Motion

$$
dS_t=\mu S_t\,dt+\sigma S_t\,dW_t.
$$

- $S_t$: stock/reference-asset price at time $t$.
- $t$: continuous time; $dt$ is an infinitesimal time increment.
- $\mu$: mean drift rate.
- $\sigma$: constant return volatility.
- $W_t$: standard Wiener process; $dW_t$ is its increment.

**Purpose:** Generate underlying paths for base-stage simulation. **Assumptions:** Constant drift and volatility, continuous diffusion, and GBM/lognormal dynamics. **Interpretation:** proportional price change combines deterministic drift and Brownian shock. (Source: p. 285)

### MathML 6–12 (EQ 0037–0043): GBM Symbols

The seven inline nodes define $S_t$, $t$, $\mu$, $\sigma$, $W_t$, and repeat $\mu$ and $\sigma$ in the statement about the return distribution. They support EQ 0036 and add no new formulas. (Source: p. 285)

### MathML 13 (EQ 0044): Heston Stock Process

$$
dS_t=\mu S_t\,dt+\sqrt{v_t}\,S_t\,dW_t^{S}.
$$

- $S_t$, $t$, $\mu$, and $dt$: as above.
- $v_t$: stochastic instantaneous variance.
- $\sqrt{v_t}$: instantaneous volatility.
- $W_t^S$: Wiener process driving stock returns.

**Purpose:** Show a stochastic-volatility alternative to GBM. **Conditions:** $v_t\ge0$; the chapter specifies independent stock and volatility Wiener processes. **Interpretation:** return volatility changes through time rather than remaining fixed. (Source: pp. 285–286)

### MathML 14 (EQ 0045): Instantaneous Volatility

$$
\sigma_t=\sqrt{v_t}.
$$

- $\sigma_t$: volatility at time $t$.
- $v_t$: variance state at time $t$.

**Purpose:** Connect Heston variance to volatility. **Condition:** $v_t\ge0$. **Interpretation:** volatility is the positive square root of variance. (Source: p. 286)

### MathML 15 (EQ 0046): Printed Volatility Process

$$
d\sqrt{v_t}=-\theta\sqrt{v_t}\,dt+\delta\,dW_t^v.
$$

- $\sqrt{v_t}$: stochastic volatility state.
- $\theta$: mean-reversion/decay coefficient.
- $\delta$: volatility-of-volatility coefficient (the prose calls it the variance of the Wiener process).
- $W_t^v$: Wiener process driving volatility.

**Purpose:** Model time-varying volatility as an Ornstein–Uhlenbeck-type process. **Conditions:** The source assumes $W_t^S$ and $W_t^v$ independent. **Interpretation:** the negative drift pulls volatility toward zero in the printed specification while shocks perturb it. This is not the canonical Heston CIR variance equation; it is preserved exactly. (Source: p. 286)

### MathML 16–20 (EQ 0047–0051): Heston Symbols

The five inline nodes are $\theta$, $\delta$, repeated $\theta$, $W_t^S$, and $W_t^v$. They define parameters and the two independent drivers used above. (Source: p. 286)

### Code-Level BSM Relationships

Although not MathML, the implementation uses:

$$
d_1=\ln(S/K)+(r+\sigma^2/2)t,\qquad d_2=d_1-\sigma\sqrt{t},
$$

$$
C=S\Phi(d_1)-Ke^{-rt}\Phi(d_2),\qquad \Delta_{call}=\Phi(d_1).
$$

Here $S$ is spot, $K$ strike, $r$ risk-free rate, $\sigma$ volatility, $t$ time to maturity, $\Phi$ the standard-normal CDF, $C$ call price, and $\Delta_{call}$ call delta. **Purpose:** Create simulated price/delta targets. **Conditions:** BSM/GBM assumptions and $S,K,t>0$. **Interpretation:** discounted risk-neutral call value and its stock sensitivity. The code's displayed `d1` omits an explicit division by $\sigma\sqrt t$ found in the standard formula; this extraction reports the code as written and flags it below. (Source: pp. 294–295)

### MathML 21 (EQ 0052): Hedged-Portfolio Change

$$
\Delta_{t+1}=a_{t+1}(S_{t+1}-S_t)-c(a_{t+1}-a_t)-(C_{t+1}-C_t).
$$

- $\Delta_{t+1}$: change in hedged-portfolio value from $t$ to $t+1$ (not option delta).
- $a_{t+1}$: stock quantity selected at $t$ and held to $t+1$.
- $a_t$: previous stock quantity.
- $S_t,S_{t+1}$: underlying prices.
- $c$: commission rate/cost coefficient.
- $C_t,C_{t+1}$: call invoice prices; quoted option prices are multiplied by 100.

**Purpose:** Compute the refinement-stage reward/penalty input. **Conditions:** One-step discrete hedge, source's linear transaction-cost expression, and consistent contract/share units. **Interpretation:** stock-hedge gain minus rebalancing cost minus the call's value change. The source omits an absolute value around turnover, so reducing a position can create a negative “cost”; preserved as written. (Source: p. 296)

### MathML 22–32 (EQ 0053–0063): PnL Symbols

These 11 inline nodes define $\Delta_{t+1}$, $t$, $t+1$, $a_{t+1}$, repeated $t$ and $t+1$, $S_t$, repeated $t$, $c$, $C_t$, and repeated $\Delta_{t+1}$. They support EQ 0052 and the loss definition; they are not separate equations. (Source: p. 296)

### Downside Penalty / Reward Definition

$$
L_{t+1}=\operatorname{ReLU}\!\left(-\frac{\Delta_{t+1}}{W_t}\right)
=\max\!\left(0,-\frac{\Delta_{t+1}}{W_t}\right),
$$

where $W_t$ is current hedged-portfolio wealth and the other symbols are above. **Purpose:** Penalize only negative percentage wealth changes. **Conditions:** $W_t\ne0$ and preferably positive. **Interpretation:** losses produce positive training penalty; gains produce zero penalty. (Source: pp. 296–297)

### MathML 33–35 (EQ 0064–0066): Rolling Training Windows

The nodes encode update time $\tau$, the short refinement window

$$
\tau-\Delta t<t<\tau,
$$

and a longer simulation-history cutoff $\tau-\Delta$. Here $\tau$ is model-update time, $t$ a market-data timestamp, $\Delta t$ the recent refinement-window length, and $\Delta$ the longer return-estimation lookback. **Purpose:** Separate recent market refinement from longer simulation calibration. **Condition:** Only information preceding $\tau$ is used. **Interpretation:** roll both stages forward, emphasizing recent option prices while estimating stock dynamics over more history. (Source: p. 297)

## Methods and Procedures

### Two-Stage RL Training

1. Specify and estimate the underlying process (GBM in the example).
2. Generate synthetic moneyness, maturity, prior positions, and BSM deltas.
3. Split each simulated batch 75%/25% into training/test data.
4. Train the policy for 1,000 epochs to minimize action-versus-underhedged-delta MSE.
5. Save the base policy.
6. Load recent raw equity and front-option data without looking ahead.
7. Build daily state paths for selected strikes and nearest expiries.
8. Sample hedge actions and compute hedged-portfolio changes including commission.
9. Backpropagate downside percentage-wealth penalty with lower-rate AdamW.
10. Evaluate forward/paper results and continuously attribute, update, and refine. (Source: pp. 285–300)

### State–Action–Penalty Specification

- **State $s_t$:** moneyness, remaining maturity, previous position.
- **Action $a_{t+1}$:** sampled next-period underlying quantity from a normal policy distribution.
- **Base target $y$:** $0.9\Delta_{BS}+0.1a_t$.
- **Base loss:** MSE between sampled action and $y$.
- **Refinement outcome:** one-step hedged-portfolio change.
- **Refinement loss:** downside-only ReLU of negative change divided by wealth.
- **Policy update:** gradient backpropagation with Adam/AdamW. (Source: pp. 290–300)

## Examples

- Barclays S&P 500-linked structured note: 110.5% upside participation and a 20% buffered put-spread-like payoff illustrates non-vanilla hedging. (Source: p. 284)
- AAPL call experiment: 30–120-day contracts, 14-day holding minimum, simulated delta priming, and refinement from December 19, 2023 to February 17, 2024. (Source: pp. 289–303)
- Alternative model: Heston stochastic volatility is discussed but rejected for this small implementation because of calibration and computational burden. (Source: pp. 283, 285–286)

## Figures and Tables

The chapter contains no formal tables and eight figures:

1. **Figure 7.1:** MSFT January 24, 2024 call implied volatilities as of noon January 2 show a downward strike skew around $375 spot, contradicting constant volatility. (Source: p. 283)
2. **Figure 7.2:** Rolling two-stage timeline; longer simulated-data blocks precede shorter recent-market refinement blocks at successive update times. (Source: p. 297)
3. **Figure 7.3:** AAPL shares and 180-strike front calls from December 2023–February 2024; call series jump at expiry rolls. The caption contains the typo “APPL.” (Source: p. 300)
4. **Figure 7.4:** Base in-sample and test MSE fall rapidly and nearly overlap because both samples come from the same simulator. (Source: p. 301)
5. **Figure 7.5:** Total real-data refinement penalty decreases rapidly across epochs. (Source: p. 301)
6. **Figure 7.6:** AI hedge remains around 0.33–0.36 while delta is around 0.50–0.54 for the displayed AAPL contract. (Source: pp. 301–302)
7. **Figure 7.7:** AI hedging wealth finishes above delta and hold; numerical hedging is volatile and deeply negative. (Source: p. 303)
8. **Figure 7.8:** Net hedged wealth similarly favors AI in this path; numerical hedging again performs worst. (Source: p. 303)

## Applications

- Inventory-risk management for option market makers and dealers.
- Dynamic hedging of option combinations and structured-note embedded options.
- Low-latency approximation of expensive optimal discrete-hedging calculations.
- Continuous policy adaptation to transaction costs, liquidity, trends, and calendar rolls.
- Potential inference of pricing kernels and improved derivative-price models from learned hedge behavior. (Source: pp. 283–304)

## Assumptions, Limitations, and Edge Cases

- BSM/GBM simulation inherits constant-volatility, diffusion, and structural assumptions. (Source: pp. 282–286)
- Simulation learns only represented “known unknowns”; unmodeled processes require real data and may still not persist. (Source: p. 287)
- The three-feature state excludes price, spread, volume, macro data, and market structure. (Source: p. 290)
- The architecture is intentionally small and not claimed industrially adequate. (Source: pp. 284–285, 291)
- Fixed-volatility base training may not transfer across volatility regimes or stocks. (Source: p. 295)
- Discrete actions cannot exactly match continuously changing or next-period delta. (Source: pp. 295–296)
- PnL is unbounded, nonlinear, skewed, and high-kurtosis; convergence can be data- and compute-intensive. (Source: p. 297)
- Recent-window refinement can mistake transitory history for future structure. (Source: p. 297)
- Downside-only ReLU ignores positive PnL dispersion, so it does not literally minimize total PnL variance. (Source: pp. 296–297; limitation inferred)
- `wealth` can approach zero or become negative, making normalized penalty unstable or semantically awkward; no guard is shown. (Source: pp. 299–300; edge case inferred)
- The commission term lacks absolute turnover and can reward position reductions; this may be a source/code defect. (Source: pp. 296, 300; edge case inferred)
- Contract rolls create discontinuities but are implicitly learned rather than normalized. (Source: p. 300)
- The performance comparison is a short, single-asset demonstration and cannot establish broad superiority. (Source: pp. 300–304)

## Common Mistakes and Warnings

- Treating BSM prices, deltas, or continuous hedging assumptions as frictionless truths in live markets. (Source: pp. 281–283)
- Expanding the state without defining how added features will be simulated in base training. (Source: p. 290)
- Starting with unregularized price/PnL learning when data and compute are insufficient. (Source: p. 297)
- Combining delta and PnL losses without careful weighting and out-of-sample hyperparameter control. (Source: p. 297)
- Introducing look-ahead bias when requesting research data; the implementation explicitly moves the QuantBook date to the refinement endpoint. (Source: p. 298)
- Confusing policy-output `mu`/`sigma` with GBM drift/volatility, or portfolio-change $\Delta$ with option delta. (Source: pp. 285–286, 290–291, 296)
- Reading fast loss convergence as proof of live profitability; simulated train/test distributions are identical. (Source: p. 301)
- Deploying without paper testing, performance attribution, model monitoring, and rolling refinement. (Source: pp. 287–288, 304)

## Key Takeaways

- A stable theoretical prior plus limited real-data refinement is a pragmatic alternative to end-to-end PnL learning. (Source: pp. 285–300)
- State, action, timing, cost, and reward definitions determine what the agent can learn. (Source: pp. 290–300)
- Delta is a bounded and learnable priming target; PnL supplies realism but is harder to optimize. (Source: pp. 294–297)
- The example policy learns a lower hedge than spot delta and outperforms comparators on the shown path, but this is illustrative evidence. (Source: pp. 300–303)
- Financial policies need continual out-of-sample testing and forward updates because market conditions evolve. (Source: pp. 287–288, 303–304)

## Glossary

| Term | Definition | Source |
|---|---|---|
| BSM | Black–Scholes–Merton option-pricing/hedging framework. | pp. 281–283 |
| Delta hedging | Holding underlying quantity based on option price sensitivity to spot. | pp. 284, 294–296 |
| Volatility smile/skew | Strike-dependent implied-volatility pattern inconsistent with constant volatility. | pp. 282–283 |
| GBM | Constant-drift, constant-volatility geometric Brownian price process. | p. 285 |
| Heston model | Stochastic-volatility alternative with extra state and calibration burden. | pp. 283, 285–286 |
| Policy network | Neural mapping from current market state to next hedge distribution. | pp. 288, 290–291 |
| Agent | Trading algorithm using the policy network to decide and trade. | p. 288 |
| State | Moneyness, maturity, and prior hedge position in this implementation. | p. 290 |
| Action | Next-period quantity of underlying stock to hold. | pp. 290, 296 |
| Moneyness | Relative strike/spot measure used as a state input. | pp. 290, 299 |
| MSE | Mean squared error between base action and target hedge. | pp. 293–296 |
| ReLU | $\max(0,x)$ activation used for network layers and downside penalty. | pp. 291, 296–297 |
| Refinement | Second-stage tuning of the simulated-data prior on recent market data. | pp. 287, 296–300 |
| Underhedging | Holding less underlying than a full theoretical delta hedge. | pp. 293, 295–296 |
| Policy prior | Delta-like behavior acquired from simulation before market-data tuning. | pp. 296–297 |
| Invoice price | Listed option quote multiplied by 100 to reflect contract convention. | p. 296 |
| Paper portfolio | Forward, non-capital test on newly arriving market observations. | pp. 287–288 |

## Connections to Other Chapters

- The chapter assumes prior option-pricing theory, BSM, neural-network, and RL knowledge. (Source: p. 284)
- It applies the general problem-definition, dataset, training, and out-of-sample workflow developed earlier in the book to a concrete hedging task. (Source: pp. 285–300; connection inferred)
- The full files are linked to the book repository and the Part III setup instructions. (Source: p. 285)

## Extraction Issues

- The XHTML was complete and readable, with print anchors spanning pages 281–304.
- All 35 MathML nodes (EQ 0032–0066) are accounted for: six principal equations/relationships plus 29 inline or supporting symbol/window nodes. Code-level BSM and penalty equations were also captured because they are mathematically substantive despite not being MathML.
- All eight figure assets were accounted for; Figures 7.2 and 7.6–7.8 were visually inspected for details not fully expressed by alt text.
- The prose defines call moneyness as `max(0, strike - stock)`, then says calls are in the money when stock exceeds strike. The implementation instead uses `S/K - 1`, which matches the latter direction. This extraction reports the executable definition and flags the prose inconsistency. (Source: pp. 290, 299)
- The displayed `black_scholes_call` and `black_scholes_delta` code computes `d1` without dividing by $\sigma\sqrt t$, unlike the standard BSM equation it claims to implement. The code was not silently corrected. (Source: pp. 294–295)
- The printed structured-note second branch and the hedging commission term have potentially problematic economics/sign conventions; both are preserved and flagged rather than repaired. (Source: pp. 284, 296, 300)
- The source calls $\delta$ “the variance of the Wiener process” in the volatility equation; mathematically it acts as the diffusion coefficient/volatility of volatility. (Source: p. 286)
- The chapter describes the objective as minimizing PnL variance, but the implemented ReLU loss penalizes downside percentage changes only. These objectives are related but not identical. (Source: pp. 288, 296–297)
- Figure 7.3's caption says “APPL” while the underlying ticker throughout the example is AAPL. (Source: p. 300)
