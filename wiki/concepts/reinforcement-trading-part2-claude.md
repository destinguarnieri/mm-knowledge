# RL Bracket Trading Agent (Ziad Francis, Part 2) — Claude Review

Status: draft

Purpose: extract the reusable mechanisms from a third-party reinforcement-learning trading repo, separated from its framework choices, and record which of them Money Machine has no equivalent for. This is a review of external material, not confirmed Money Machine practice.

Reviewer tag: `claude` (one of several parallel agent write-ups of the same source).

Related: [[concepts/supervised-trading-labels|Supervised Trading Labels]] · [[research/trading/study-menu|Study Menu]] · [[research/trading/research_process_v2|Research Process V2]]

## Source

- Repo: https://github.com/ZiadFrancis/Reinforcement_Trading_Part_2 (~4,200 lines Python)
- Video transcript reviewed alongside the code; several of the strongest mechanisms appear only in the repo.
- Instrument: XAUUSD, 1-minute bid data May 2003 – May 2026 (~23 years), decisions on H1.
- Stack: Gymnasium environment + Stable-Baselines3 PPO. Framework-specific; the mechanisms below are not.

## What the system is

A PPO agent trades gold through bracket orders. Unlike a supervised setup there is no label: the agent acts, the environment returns a scalar reward, and the policy updates toward more reward. The training data does not exist until the policy generates it by acting, which is why the reward function — not a label resolver — is the artifact that specifies what gets learned.

Relation to [[concepts/supervised-trading-labels|Supervised Trading Labels]]: the reward function occupies the role the label resolver occupies there, and the leakage boundary relocates from the feature vector into the environment. The observation at bar `t` may expose only bar-`t` information; the reward paid at `t` may depend only on what has resolved by `t`. There is no `resolved_at` — episodes overlap continuously and credit assignment belongs to the algorithm, not the data schema.

## Reward function

`env_bracket.py`, in `step()`:

```python
reward_risk_unit = max(prev_equity * risk_fraction, 1e-12)   # 0.5% of equity
reward = (equity - prev_equity) / reward_risk_unit           # realized, in R
if position.direction != 0:
    reward += (unrealized / position.risk_cash) * 0.01       # mark-to-market shaping
    reward -= 0.00002                                        # holding penalty
```

Three terms, three jobs:

- **Realized outcome, in R-multiples.** Dividing equity change by cash at risk makes a 1R win score `+1` and a stop score `-1` regardless of price level or volatility regime. The objective is normalized the same way the features are.
- **Mark-to-market shaping**, weight `0.01`. Fixes sparse-reward credit assignment: without it the agent receives a flat zero for potentially hundreds of bars. Deliberately too small to outweigh the realized term. Uses the *current* bar's close, with an explicit code comment that this is to avoid lookahead.
- **Holding penalty**, `2e-5` per bar in position. Negligible per bar, meaningful over hundreds. Produces the observed `manual_close` exits without any hard time-stop rule.

## Observation and action space

Observation is 31 dimensions: 25 market features plus 6 position-state features.

```python
[direction, unrealized_r, min(bars_in_trade/100, 10), dist_tp_atr, dist_sl_atr, tp_r]
```

The position block is load-bearing and absent from the video's account. Without it the agent chooses hold-vs-close about a position it cannot perceive. `dist_tp_atr` / `dist_sl_atr` express proximity to each barrier in volatility units, which is what makes an early manual close learnable rather than noise.

Market features are all dimensionless — EMA distances over ATR, ATR/close, ATR fast/slow ratio, BB width/close, candle range and wick ratios over ATR, 1–5 bar returns over ATR, cyclical time encodings, session flags. No absolute prices.

Action is `MultiDiscrete([3, 3, 4])`: direction × SL bucket (1.0/1.5/2.0 × ATR) × TP bucket (1.0/1.5/2.0/3.0 R). Bracket indices are consumed only on open.

## Execution model

- M1 replay inside each decision interval uses a **half-open interval `(start, end]`** via `searchsorted` — excludes the decision bar itself, so no same-bar fill.
- **Pessimistic intrabar tie-break:** `# if both touched, assume SL first`. This resolves the ambiguity [[research/trading/study-menu|Study Menu]] Shape 1 leaves open when both barriers are touched inside one bar, and resolves it against the strategy.
- Costs applied adversely on both sides: `spread/2 + slippage` added on entry, subtracted on exit, plus commission at close.
- Ingest detail: MT4 exports timestamp each row at candle **open**; the loader reindexes to **close** time so a decision timestamp means the candle is complete and known. Handles a whole class of silent lookahead at the source.

## Data protocol

Sliding-window walk-forward, configured as 5 years train / 6 months validation / 6 months test, stepping 6 months — roughly 34 folds across the 23-year dataset. Train, validation, and test move forward together and the oldest data falls off the back, so the model always learns from a recent slice.

The config states the deliverable plainly: *stitching every fold's test window gives one continuous out-of-sample equity track record.* That is a substantially stronger claim than the single test-window number the video led with.

`test_frac` is held equal to `1 - train_frac - val_frac` so the sealed final holdout is byte-for-byte identical whether the model came from a single split or from walk-forward.

## Leakage controls

Two, both worth taking.

**Embargo.** `split_embargo_bars = 200`, applied on each side of every split boundary, with the reasoning recorded: EMA-200 retains ~37% of a bar's weight after 200 steps, so 200 bars makes cross-boundary contamination negligible.

**Mechanical causality assertion.** `leakage_checks.py`, ~30 lines:

```python
def assert_feature_stability_when_future_appended(df, feature_cols, cut_index, atol=1e-10):
    feat_past, _ = add_stationary_features(df.iloc[:cut_index])
    feat_full, _ = add_stationary_features(df)
    common = feat_past.index.intersection(feat_full.index)
    diff = (feat_past.loc[common, feature_cols] - feat_full.loc[common, feature_cols]).abs().max().max()
    if diff > atol:
        raise AssertionError(f"Potential leakage: max feature change = {diff}")
```

Compute features on truncated history, compute them again on full history, assert overlapping rows are identical. Any centered window, backward fill, full-sample normalization, or non-causal transform fails immediately. Framework-agnostic and cheap.

## Model selection

Checkpoints are scored on two legs and selected on the weaker one:

```python
q_train = train_r - dd_penalty * train_dd_pct      # dd_penalty = 1.0 reward-units per 1% DD
q_val   = val_r   - dd_penalty * val_dd_pct
score   = min(q_train, q_val)
```

Two details absent from the video:

- The "train" leg is **the last ~`len(val)` bars of training data**, not the whole training set, so both legs are comparable in length and sit near the split boundary.
- A **do-nothing guard** is required for the drawdown penalty to be safe:

```python
eligible = (train_r > 0 and val_r > 0
            and train_n >= min_trades and val_n >= min_trades)
```

An idle policy makes no trades, has ~0 drawdown, and would otherwise win on the penalty term. Both legs must be genuinely profitable and genuinely active before a checkpoint is eligible.

`VecNormalize` statistics are snapshotted with every saved checkpoint — the RL equivalent of shipping the fitted scaler with the model rather than refitting at inference.

## Deployment gate

Three ANDed conditions over the completed folds:

```python
good        = count(fold return > 0 AND PF > 1.0)   # need >= 4
worst_pf    = min(PF across folds)                  # need >= 0.9
mean_sharpe = mean(sharpe across folds)             # need > 0
passed      = c_count and c_worst and c_sharpe
```

Breadth, a floor, and a positive mean. A strategy carried by one spectacular fold fails the floor; a strategy of many mediocre folds fails breadth. On failure the artifacts are quarantined under `models/walk_forward/` and any stale `run_info.json` is renamed `run_info.NO_DEPLOY.json`. The stated design principle: *the gate only ever PREVENTS a bad deploy — it never fabricates one.*

The folds are evidence that the **procedure** generalizes; they do not select the model. If the gate passes, the model promoted is the one from the **last** fold, because it trained on the most recent data.

**Default caveat:** `_passes_consistency_gate` reads the `val_*` columns by default, so out of the box the promotion decision uses the same windows that drove checkpoint selection. The docstring flags this and supplies the fix — pass `test_*` to gate on the sliding walk-forward's true out-of-sample windows. Anyone adopting the gate should pass `test_*`.

## Candidates for Money Machine

Ranked by what MM currently lacks.

1. **Mechanical causality assertion.** MM states the point-in-time invariant in [[concepts/supervised-trading-labels|Supervised Trading Labels]] but has no executable test of it. `assert_feature_stability_when_future_appended` is the invariant in runnable form, applies to any feature pipeline, and is ~30 lines.
2. **Maximin checkpoint selection with a do-nothing guard.** MM has no documented model-selection rule anywhere. The pattern generalizes past RL: score on two slices, select on the weaker leg, and guard against the degenerate solution the scoring function invites.
3. **Pre-registered deployment gate with quarantine on failure.** Breadth + floor + mean, thresholds fixed in config before the run, with artifact handling automated so a failed gate cannot quietly ship. This is the concrete form of the symmetric kill/upside framing in [[research/trading/research_process_v2|Research Process V2]].
4. **Pessimistic intrabar tie-break.** Direct answer to the both-barriers-touched case in [[research/trading/study-menu|Study Menu]] Shape 1.
5. **Stitched walk-forward test windows as the reported result.** One continuous OOS equity track rather than a single held-out number.
6. **Reward/objective normalization in R-multiples.** Makes the objective scale-free across volatility regimes, the same way the features are.

## Provenance notes

Several repo behaviours contradict or exceed the video:

- The video names RSI as an input feature. The repo **dropped** `rsi_centered` in a dated collinearity audit (2026-06-02, `|r| = 0.98` against `close_ema20_atr`). Three other features were dropped the same way with correlations recorded in comments; 25 remain.
- The video presents a single test-window result. The repo is built to produce a ~34-fold stitched OOS track.
- The video does not mention the embargo, the leakage assertion, the position-state observation block, the do-nothing guard, or the pessimistic tie-break.
- PPO hyperparameters are an explicitly "generalisation-first" preset (lr 6e-5 linear decay, entropy 0.03, 5 epochs, clip 0.1, target_kl 0.025, weight decay 1e-5, 128×64 net) with the recorded rationale that thin XAUUSD signal lets PPO memorize the training period.

None of the reported performance figures were reproduced or verified during this review; only the code paths were read.

## Open items

- Nothing here is validated against MM data or promoted to MM practice.
- Items 1–3 are the ones worth extracting first; each is independent of RL and of this repo's framework.
- Parallel agent write-ups of the same source exist; this page is not the merged view. `wiki/index.md` deliberately not updated pending selection among them.
