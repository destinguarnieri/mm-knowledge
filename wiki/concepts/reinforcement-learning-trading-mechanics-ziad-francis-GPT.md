# Reinforcement-Learning Trading Mechanics — Ziad Francis

Status: draft

Purpose: record the mechanical layer of the reinforcement-learning trading implementation published by Ziad Francis, separate the reusable ideas from the repository's specific choices, and identify what Money Machine should not carry forward unchanged.

This is a GPT-authored external implementation analysis. It is not a Money Machine architecture decision, evidence that reinforcement learning is profitable, or approval of the repository's reported results.

Related: [[concepts/supervised-trading-labels|Supervised Trading Labels]], [[research/trading/research_process_v2|Research Process V2]], [[trading/pmax|P_Max]]

Source snapshot: [`ZiadFrancis/Reinforcement_Trading_Part_2`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/tree/7615a58c33802c298ae147b14137ff36ca130590) at commit `7615a58c33802c298ae147b14137ff36ca130590`, reviewed 2026-08-30. The repository does not include its XAUUSD dataset or trained model artifacts, so the code and stored notebook outputs can be inspected but the training run cannot be independently reproduced from the repository alone.

## Executive read

This implementation does not create future-outcome labels or fit a classifier to labeled rows. It trains an actor-critic MLP with PPO through interaction with a historical market simulator:

```text
31-value observation
        ↓
actor-critic MLP [128, 64 per branch], trained with PPO
        ↓
(direction, stop-loss bucket, take-profit bucket)
        ↓
environment resolves the next H1 transition using M1 candles
        ↓
realized equity change + unrealized-P&L shaping − holding penalty
        ↓
reward used for PPO updates
```

The environment supplies most of the trading structure. It fixes the decision clock, single-position constraint, position-sizing rule, bracket menu, transaction-cost assumptions, fill rules, and reward definition. The deployed learned object is the actor policy inside that shell: a mapping from market-plus-position state to direction and bracket geometry. During training, PPO also fits a critic/value function used to estimate advantages; the critic is not part of the live action decision.

This distinction is load-bearing. The implementation is not an unconstrained agent discovering every aspect of trading. Its learned object is approximately:

```text
policy(action | current market features, current position state,
       fixed simulator, fixed reward, fixed risk shell)
```

## Part I — What exactly the implementation does

### 1. Decision and execution clocks

The agent makes one decision per H1 bar. Position entries, exits, stops, and targets are resolved against M1 candles between the current H1 close and the next H1 close.

This separates policy frequency from execution resolution:

- H1 determines when the model may reconsider the position;
- M1 approximates the intrahour price path used to determine bracket outcomes;
- if a single M1 candle touches both stop and target, the environment assumes the stop occurred first.

The last rule is deliberately conservative, but it remains a bar-path assumption rather than observed trade ordering.

Source: [`env_bracket.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/env_bracket.py), [`data_loader.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/data_loader.py).

### 2. Observation contract

Each observation contains 31 values: 25 market features and six position-state features.

The market features cover:

- price distance from EMA 20, 50, and 200, normalized by ATR;
- EMA 20 versus EMA 50 distance;
- MACD histogram and 20-bar rate of change, normalized by ATR;
- ATR relative to price and fast ATR relative to slow ATR;
- Bollinger width;
- candle range and wick ratios;
- one- through five-bar price changes normalized by ATR;
- cyclical time-of-day and day-of-week encodings;
- Asia, London, New York, and London/New York overlap flags.

The position-state features are:

- current direction;
- current unrealized return in initial-risk units;
- bars held;
- ATR distance to the target;
- ATR distance to the stop;
- selected target multiple.

The current repository calculates RSI but removes it from the final feature matrix as redundant. RSI therefore is not one of the agent's inputs despite its mention in surrounding creator material.

Source: [`features.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/features.py), [`env_bracket.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/env_bracket.py).

### 3. Action contract

The Gym action space is `MultiDiscrete([3, 3, 4])`. PPO emits three categorical decisions:

| Component | Choices |
| --- | --- |
| Direction | flat/close, long, short |
| Stop distance | 1, 1.5, 2 ATR |
| Profit target | 1, 1.5, 2, 3 times initial risk |

The meaning of direction action `0` depends on position state:

- when flat, it remains flat;
- when holding a position, it closes that position;
- emitting the existing direction retains the position and its original bracket;
- emitting the opposite direction closes the current position and opens the reverse direction with a newly selected bracket.

There is no separate `hold` action. When the existing direction is emitted, newly emitted stop and target components are ignored rather than modifying the live bracket.

Position size is not learned. At entry, the environment risks 0.5% of current realized equity against the selected stop distance:

```text
risk_cash = current_equity × 0.005
units = risk_cash / stop_distance
```

Because entry and exit costs sit outside the raw stop distance, the actual loss at a stopped exit can exceed the nominal `risk_cash`.

Source: [`env_bracket.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/env_bracket.py), [`config.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/config.py).

### 4. Transition and cost model

The environment supports one open position. It applies a fixed spread, per-side slippage, and commission. An entry is shifted against the agent by half the spread plus slippage; exits are shifted against the position by the same amount.

A position can close by:

- stop loss;
- take profit;
- the direction action requesting flat;
- reversal into the opposite direction.

There is no hard maximum holding period. Holding duration influences the observation and a small reward penalty, but the environment does not automatically close an old trade.

### 5. Reward contract

For each H1 step, the environment approximately computes:

```text
risk_unit = equity_at_start_of_step × risk_fraction

reward = realized_equity_change / risk_unit

if a position remains open:
    reward += 0.01 × current_unrealized_R
    reward -= 0.00002
```

The realized term places gains and losses into a risk-relative unit. The unrealized term supplies denser feedback before a trade closes. `VecNormalize` then normalizes training observations and rewards before PPO consumes them; evaluation freezes the saved normalization state.

The unrealized term is the full current unrealized return on every open bar, not the change in unrealized return since the previous bar. A persistent open gain or loss is therefore credited or debited repeatedly across time. This makes the reward an integral of marked position state rather than a clean sequence of incremental economic returns.

Source: [`env_bracket.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/env_bracket.py), [`train_ppo.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/train_ppo.py).

### 6. PPO training loop

The repository-level call `PPO("MlpPolicy", ...)` is a high-level Stable-Baselines3 constructor, not a statement that PPO is the neural-network architecture. The layers are MLPs; PPO defines the rollout, advantage, loss, and constrained policy-update procedure; PyTorch automatic differentiation performs backpropagation; and Adam applies the resulting gradients to the weights.

#### Network and action distribution

Under the Stable-Baselines3 `ActorCriticPolicy` contract, `net_arch=[128, 64]` creates two separate feed-forward branches with the same shape:

```text
31 normalized observation values
        ├─ actor:  128 tanh → 64 tanh → 10 logits split [3, 3, 4]
        └─ critic: 128 tanh → 64 tanh → 1 scalar state-value estimate
```

The actor and critic do not share learned hidden layers. They share only the default flattening feature extractor, which has no learned parameters for this vector observation. The approximately 25,000 trainable parameters are initialized with Stable-Baselines3's default orthogonal initialization: gain `sqrt(2)` for the MLPs, `0.01` for the action head, and `1` for the value head.

The `MultiDiscrete([3, 3, 4])` action space becomes one `MultiCategoricalDistribution`: ten actor logits split into independent three-, three-, and four-way categorical distributions. Training rollouts sample each component stochastically and sum their log probabilities and entropies. Deterministic evaluation takes the highest-probability choice independently for each component. This factorization means the actor can condition all three output distributions on the same observation, but it does not model direction, stop, and target as an autoregressive action sequence.

#### Rollouts, advantages, and loss

The default sliding-fold entry point uses four parallel environments, 2,048 steps per environment per rollout, and therefore 8,192 transitions before each update. Generalized Advantage Estimation uses explicit `gamma=0.99` and `gae_lambda=0.95`; Stable-Baselines3 also normalizes advantages within each minibatch by default.

For each minibatch, Stable-Baselines3 recomputes action log probabilities, entropy, and critic values and combines:

```text
clipped PPO policy loss
+ 0.5 × critic mean-squared-error loss
+ 0.03 × entropy loss
```

The policy ratio is clipped to `[0.9, 1.1]`. The critic target is the GAE-derived return; value-function clipping is not enabled. Each rollout is reused for five epochs. Approximate reverse KL is monitored and the remaining epoch passes stop early when it exceeds `1.5 × 0.025`. The environment and its reward calculation are not differentiable and are not backpropagated through: rewards and critic estimates produce advantages, which weight the differentiable log-probability loss inside the actor.

#### Backpropagation and optimizer

Stable-Baselines3 owns the lower-level update that is absent from `train_ppo.py`:

```text
zero Adam gradients
→ backpropagate the combined PPO loss through actor and critic
→ clip the joint gradient norm to 0.5
→ take one Adam step over all actor-critic parameters
```

The repository does not select `optimizer_class`, so Stable-Baselines3 supplies PyTorch `Adam`, not `AdamW`. It passes `weight_decay=1e-5` to Adam; under the reviewed dependency floor this is Adam's coupled L2-style decay, not AdamW's decoupled decay. The learning rate starts at `6e-5` and decays linearly to zero over the fold's training budget.

The code makes minibatch size hardware-dependent: `256` on CPU and `1,024` on CUDA. An 8,192-transition rollout therefore produces 32 CPU minibatches or eight CUDA minibatches per epoch, so the same nominal five-epoch configuration performs a different number of optimizer steps depending on hardware. `device="auto"` resolves only to CUDA when available and otherwise CPU.

#### Observation and reward normalization

`VecNormalize` maintains running per-coordinate observation statistics, standardizes observations, and clips normalized values to `[-10, 10]`. Reward normalization is not a simple reward z-score: it tracks the variance of discounted returns with `gamma=0.99`, divides each training reward by that running standard deviation, and applies the default reward clip `[-10, 10]`. Evaluation freezes the selected checkpoint's saved running statistics and disables reward normalization.

#### Dependency boundary

The repository's `requirements.txt` specifies `stable-baselines3>=2.3` rather than an exact version and does not pin PyTorch directly or provide a lockfile. The architecture, action-distribution, loss, backpropagation, and default values above are verified against the repository code and Stable-Baselines3 2.3.0, the declared minimum. The absent training artifact and runtime manifest mean the exact installed Stable-Baselines3/PyTorch versions—and therefore every transitive numerical default—cannot be reconstructed. For example, because the repository passes a nonempty `optimizer_kwargs` dictionary containing only `weight_decay`, Stable-Baselines3 2.3.0 does not inject its usual Adam `eps=1e-5`; the installed PyTorch Adam default applies instead. A reproducible rerun must pin both packages and serialize the resolved optimizer configuration.

Source: [`train_ppo.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/train_ppo.py), [`config.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/config.py), [`requirements.txt`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/requirements.txt), [Stable-Baselines3 2.3.0 PPO](https://github.com/DLR-RM/stable-baselines3/blob/v2.3.0/stable_baselines3/ppo/ppo.py), [actor-critic policy](https://github.com/DLR-RM/stable-baselines3/blob/v2.3.0/stable_baselines3/common/policies.py), [MLP extractor](https://github.com/DLR-RM/stable-baselines3/blob/v2.3.0/stable_baselines3/common/torch_layers.py), [multi-categorical distribution](https://github.com/DLR-RM/stable-baselines3/blob/v2.3.0/stable_baselines3/common/distributions.py), and [`VecNormalize`](https://github.com/DLR-RM/stable-baselines3/blob/v2.3.0/stable_baselines3/common/vec_env/vec_normalize.py).

Each walk-forward fold trains a new policy from scratch. Four parallel environments independently sample random contiguous 2,048-H1-bar episodes from the fold's training period. Equity resets to $10,000 at every episode reset.

The policy therefore experiences many bounded, randomized trajectories rather than one uninterrupted pass through the five-year training history. Contiguous episodes preserve path-dependent position and reward state; random starting points broaden coverage of the training window.

The configured sliding-fold run uses three million environment steps per fold and the same seed, `42`, for each fold. The repository does not perform multi-seed training to distinguish a repeatable policy result from PPO initialization or sampling luck.

Source: [`train_ppo.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/train_ppo.py), [`config.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/config.py).

### 7. Checkpoint selection

During fold training, checkpoints are evaluated deterministically on:

1. a tail of the training period equal in length to the validation window;
2. the chronological validation window.

For each leg, the code combines cumulative raw environment reward with maximum drawdown:

```text
leg_quality = cumulative_reward − 0.8 × abs(max_drawdown_pct)
checkpoint_score = min(train_tail_quality, validation_quality)
```

A checkpoint is eligible only when both legs have positive cumulative reward and at least five trades. Using the weaker leg prevents an exceptional training-tail result from numerically compensating for weak validation. Training continues for the full step budget; checkpoint selection saves the best eligible policy and its matching `VecNormalize` snapshot.

The scoring units are not cleanly unified: cumulative shaped reward is combined with drawdown percentage. The structure is useful, but its exact objective should not be copied without redefining a coherent economic utility.

Source: [`train_ppo.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/train_ppo.py), [`training_diagnostics.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/training_diagnostics.py).

### 8. Sliding walk-forward evaluation

The default pipeline uses approximately 35 sliding folds:

```text
5 years train
        ↓
6 months validation and checkpoint selection
        ↓
6 months fold test
        ↓
advance 6 months and train a fresh policy
```

The selected checkpoint from each fold is tested on that fold's immediately following six-month window. Fold-test equity curves are then stitched and compounded. This evaluates a historical operating procedure—periodically train a policy on the latest five years, select it on the next six months, and operate it for the following six months—rather than pretending one fixed policy remains valid for the entire history.

After all tests, a consistency gate checks fold-level profitability, profit factor, worst-fold profit factor, and mean Sharpe. The final fold's checkpoint is the proposed current policy.

Source: [`run_pipeline.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/run_pipeline.py), [`train_ppo.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/train_ppo.py).

## Part II — Mechanics worth carrying forward

These ideas are useful independently of PPO, Stable-Baselines3, gold, or the repository's performance:

### Explicit environment contract

Treat state, actions, transition rules, costs, termination, and reward as a versioned research object. An RL result is conditional on this complete contract, not merely on the neural-network architecture.

### Decomposed actions inside a constrained risk shell

Separating direction from stop and target geometry creates an auditable action space and prevents the policy from expressing nonsensical orders. A fixed safety shell can retain authority over sizing, exposure, leverage, and permitted execution while the policy learns a narrower control problem.

The particular menu need not be retained. The reusable concept is constrained, typed action decomposition.

### Separate decision and execution clocks

Coarse model decisions can be simulated against a finer-grained path when stop/target ordering matters. This is preferable to pretending an H1 OHLC bar reveals the intrabar order of events. The lower-timeframe data must still be causal, aligned correctly, and governed by explicit ambiguous-bar rules.

### Risk-relative outcomes

Representing outcomes in initial-risk or another stable economic unit can reduce scale drift as price, volatility, and equity change. Reward normalization must preserve net economic meaning after costs.

### Random contiguous trajectories

Randomized episode starting points broaden regime exposure while contiguous sequences preserve path dependence. Episode length, reset state, boundary treatment, and sampling weights are part of the experimental design and must be recorded.

### Weak-leg checkpoint selection

Scoring a checkpoint by the weaker of training-tail and validation performance is a useful robustness pattern. Money Machine should retain the maximin idea while replacing the repository's mixed-unit formula with a preregistered economic utility and adequate evidence constraints.

### Model and preprocessing are one artifact

The policy, observation ordering, feature specification, normalization statistics, environment version, cost model, and action mapping must be saved and loaded together. A policy evaluated with a different normalizer is not the same trained system.

### Evaluate the rolling replacement procedure

When the intended live process retrains periodically, walk-forward testing should evaluate that repeated procedure. The fold tests estimate the behavior of train → select → deploy → replace, not the timeless merit of one model.

### Ensemble policies at the allocation layer

The repository's post-hoc analysis distinguishes averaging capital allocated to independently operating policies from majority-voting their discrete actions. That is conceptually useful: policies can disagree in timing and state, so aggregating their economic exposures is generally more coherent than voting across context-dependent action codes. This remains an unvalidated extension in this repository, not an adopted Money Machine rule.

## Part III — What should not be carried over unchanged

### Do not carry over the performance claims

The dataset and trained model artifacts are absent, so the reported notebook results cannot be reproduced from the repository. Performance is not needed to retain the mechanical ideas.

### Do not repeatedly reward the same unrealized P&L

Adding the full unrealized return every open bar double-counts persistent marked P&L through time. Prefer an incremental net-liquidation-value change, incremental unrealized-P&L change, or another reward whose cumulative sum has a defined economic interpretation.

### Do not drop terminal inventory

Training and evaluation can end with an open position that is not forcibly closed or included in final realized equity. A Money Machine environment must specify one of:

- forced terminal liquidation with costs;
- terminal mark-to-market net of estimated liquidation costs;
- continuation state across boundaries when the boundary is operational rather than analytical.

Reported return, reward, and drawdown must use the same terminal accounting convention.

### Do not treat the global last 10% as sealed after default sliding training

The default sliding folds traverse the full dataset. Later folds train and validate on portions of the repository's global final 10% period, so `final_holdout_eval.py` does not provide an untouched final holdout for the final sliding-fold policy.

The individual fold-test windows are out of sample for their own fold policies. The collection of those tests estimates the rolling training procedure. A separate terminal holdout must sit beyond all development folds and remain unseen by checkpoint selection, gating, ensemble design, and method iteration.

Source: [`final_holdout_eval.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/final_holdout_eval.py), [`data_loader.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/data_loader.py), [`train_ppo.py`](https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2/blob/7615a58c33802c298ae147b14137ff36ca130590/train_ppo.py).

### Do not use one seed as robustness evidence

PPO training is stochastic. Required seeds should be preregistered, run independently, and summarized as a distribution. Seed selection must not become another hidden optimization surface.

### Do not inherit the exact feature set or action buckets by default

The 25 inputs and bracket choices are design hypotheses, not universal RL primitives. Each feature must have a causal availability contract, and the action grid must match the instrument, execution venue, horizon, cost structure, and risk objective being tested.

### Do not conflate a holding penalty with a holding constraint

The small negative reward only changes incentives; it does not enforce an exit. If maximum exposure duration is a risk or operational constraint, enforce it explicitly in the environment. If it is a learnable choice, preserve the policy's authority and measure the resulting duration distribution.

### Do not promote on a permissive or contradictory gate

The repository can copy the latest checkpoint into the production artifact location even when the recorded consistency gate fails, while also creating a `NO_DEPLOY` marker. A production contract should fail closed: an ineligible model must not occupy the deployable artifact identity.

The repository's gate also counts a small minimum number of positive folds rather than requiring a strong prespecified distribution across all folds. Money Machine should define promotion from the intended operating objective, fold evidence, costs, drawdown, tail behavior, seed stability, baseline comparison, and capacity—not copy these thresholds.

### Do not select on test-visible iteration

Fold tests are useful for estimating the rolling procedure, but repeated architecture, reward, feature, action, or ensemble changes made after inspecting them turn the test sequence into development evidence. Any such iteration requires fresh protected evaluation data.

### Do not make the final fold automatically authoritative

Recency is relevant under nonstationarity, but the latest fold policy should not become live merely because it is latest. It must pass the complete promotion contract and retain a fallback, abstention, or no-deploy outcome.

## Part IV — Money Machine adaptation boundary

A Money Machine RL experiment should preserve the mechanical discipline while replacing repository-specific choices with an explicit contract:

1. **Objective:** specify which decision RL is expected to improve over a deterministic or supervised baseline.
2. **State:** version causal market, portfolio, execution, and risk features with point-in-time availability.
3. **Action:** use typed, bounded controls; state which controls remain outside the agent's authority.
4. **Transition:** specify fills, intrabar ambiguity, costs, latency, rejections, terminal inventory, and resets.
5. **Reward:** use an incrementally additive net economic quantity, with any shaping term separately reported and justified.
6. **Episodes:** specify trajectory length, start sampling, warm-up, reset equity, boundary liquidation, and regime weighting.
7. **Training:** save seeds, checkpoints, observation/reward normalization, environment version, and complete configuration.
8. **Selection:** choose checkpoints on chronological development folds using a frozen robust utility and minimum evidence requirements.
9. **Evaluation:** test the full retraining/replacement process across folds, multiple seeds, realistic costs, stress costs, and relevant baselines.
10. **Protection:** keep a terminal holdout outside all model, reward, action, ensemble, and gate iteration.
11. **Promotion:** fail closed unless the locked artifact passes the preregistered economic and operational gate.

The first implementation question is therefore not “Should Money Machine use PPO?” It is:

> Which bounded sequential decision currently loses important information when reduced to a supervised label or fixed backtest rule, and what environment contract would let an agent learn that decision without manufacturing reward through simulator artifacts?

## Relationship to existing raw material

The raw *Hands-On AI Trading* extracts already cover the conceptual RL vocabulary—state, action, policy, reward, simulation, and chronological validation:

- [RL hedging and the state/action/reward contract](../../raw/research/book-extracts/hands-on-ai-trading/07-better-hedging-with-reinforcement-learning.md)
- [Problem definition across objective, target, features, scope, and constraints](../../raw/research/book-extracts/hands-on-ai-trading/03-step-1-problem-definition.md)

Ziad Francis's repository adds the implementation-level bridge those extracts do not fully specify: a concrete trading environment, decomposed action space, risk-relative reward, randomized trajectory training, normalization artifact, checkpoint selection, and rolling policy replacement. This page records that bridge while keeping its source-specific weaknesses out of Money Machine's default design.
