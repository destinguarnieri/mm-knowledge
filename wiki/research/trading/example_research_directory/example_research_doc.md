# Example Research Doc

Purpose: show the expected shape of a Money Machine strategy research file. This is an example, not real research evidence.

Use this style for files under `/mm-knowledge/wiki/research/`. Keep structured sections stable, and append timestamped write-log entries as the work evolves. Do not silently rewrite the objective, kill criteria, or conclusion after seeing results.

This doc has a matching artifact folder at `/mm-knowledge/wiki/quant/research/trend-continuation-slope-filter/`, holding `configs/`, `artifacts/[run-id]/`, and `review/` as described in the process doc. Paths below are relative to that folder unless already prefixed with `research/`.

Related process: [[research/trading/research_process_v1|Research Process V1]]

## Status

- Research state: mid-research example.
- Current decision: modify and rerun small grid.
- Last updated: 2026-07-08 15:20 EDT.
- Owner: agent / researcher.
- Strategy: example trend continuation with slope filter.
- Assets/timeframes: BTC and ETH, 1h.

## Write Log

Use the write log as the audit trail. Add entries when the research question, objective, data, strategy logic, grid, interpretation, or decision changes.

### 2026-07-08 09:10 EDT

Created research card for a trend-continuation strategy. Objective, kill criteria, data split, and period segmentation were written before any grid search. Initial plan is BTC 1h only, then ETH 1h as a quarantined validation asset if the small grid shows a stable response surface.

### 2026-07-08 10:35 EDT

Ran baseline configs: `9f3b2a10-6e5c-4b8a-9d21-9c4a7e0f2b31`, `2b6f9e33-1c7a-4f6e-8b52-3a8d5c9e0f14`, `7a1d4c88-5f2b-4e9a-8c07-6b3f2d9a1e55`, and `c4e8b219-3a7f-4d6c-9e10-8f2b5a6d3c07`. Default trend config is profitable before costs but weak after fee/slippage stress. No-filter baseline has higher gross return but materially worse drawdown and churn. Random-entry null baseline is clearly negative, so the entry signal beats noise. This suggests the core issue is not entry signal strength alone; regime/chop filtering matters.

### 2026-07-08 12:05 EDT

Ran small structured BTC grid: `5d2a7f14-9b3e-4c8a-a1f6-3e7c9b2d5a80`. Best configs cluster around medium signal windows and moderate entry thresholds. Sharpest winner has highest turnover and fails fee stress, so it is not a candidate. Broad plateau appears around `fast=24`, `slow=96`, `entry_threshold=0.35-0.45`.

### 2026-07-08 13:20 EDT

Trade artifact review found repeated losses during flat/choppy segments. Decision changed from `continue` to `modify`: add a slope filter and rerun the small grid before expanding. Objective did not change.

## 1. Research Card

- Strategy idea: enter trend continuation when signal strength confirms direction, then exit on trend deterioration or reversal.
- Edge hypothesis: persistent directional moves should continue long enough to overcome fees when entries avoid low-slope chop.
- Asset universe and timeframes:
  - initial: BTC 1h;
  - validation: ETH 1h;
  - possible later scan: SOL, HYPE, XRP on 1h.
- Entry logic:
  - long when trend signal crosses above an entry threshold and slow slope is positive;
  - short when trend signal crosses below a negative entry threshold and slow slope is negative.
- Exit logic:
  - exit when trend signal crosses back toward neutral or when reversal threshold triggers.
- Risk, sizing, leverage, fee, and slippage assumptions:
  - initial capital: `$100,000`;
  - max position: `50%`;
  - leverage: `3x`;
  - fees: `0.00015`;
  - slippage: `0.05`;
  - sizing mode: static for research comparability.
- Data split:
  - discovery: BTC 1h, 2025-01-01 through 2026-06-30;
  - validation: ETH 1h over the same range, quarantined until the BTC candidate region is frozen;
  - holdout: forward data from 2026-07-01, consumed exactly once at the promotion gates.
- Market period / regime definition:
  - calendar quarters, fixed before the first grid, used for single-segment dependence and regime-sanity checks.
- Core knobs:
  - fast signal window;
  - slow signal window;
  - entry threshold;
  - exit threshold;
  - slow slope lookback / minimum slope.
- Incidental knobs:
  - chart display settings;
  - artifact verbosity;
  - run naming.
- Expected risks and tripwires:
  - churn in chop;
  - fee drag from repeated threshold recrossing;
  - low trade count after adding slope filter;
  - overfit to BTC 1h trend windows;
  - one strong trend segment explaining most return.
- Initial kill criteria:
  - fewer than `30` validation trades;
  - fee-stressed net return below `0`;
  - max drawdown worse than `-18%`;
  - top config isolated with nearby configs failing (median nearby-config Sharpe below `70%` of top-config Sharpe);
  - turnover rising faster than net return without a clear reason;
  - more than `60%` of net return from one contiguous market period.

## 2. Optimization Objective

Primary objective:

- Maximize net Sharpe after fees and slippage.

Metric definitions:

- Net return and Sharpe are computed on the fee- and slippage-adjusted equity curve.
- Trade count counts completed round trips.
- Fee drag is total fees paid as a percent of initial capital.

Hard reject conditions live in the research card kill criteria (section 1); final acceptance checks live in the promotion gates (section 12). No separate guardrail list is kept here.

Objective-change log:

- 2026-07-08 09:10 EDT: initial objective written before baselines.
- 2026-07-08 13:20 EDT: no objective change. Strategy logic changed to test slope filtering because artifact review showed chop losses.

## Run Registry

Every result cited in this research note should have a registry entry. Use this section to make claims reviewable.

| Run ID | Type | Asset/TF | Purpose | Review Link | Config Link | Artifact Links | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `9f3b2a10-6e5c-4b8a-9d21-9c4a7e0f2b31` | saved single run | BTC 1h | default baseline | `saved-run://9f3b2a10-6e5c-4b8a-9d21-9c4a7e0f2b31` | `research/trend-continuation-slope-filter/configs/example-default.json` | `research/trend-continuation-slope-filter/artifacts/9f3b2a10-6e5c-4b8a-9d21-9c4a7e0f2b31/` | baseline used in section 3 |
| `2b6f9e33-1c7a-4f6e-8b52-3a8d5c9e0f14` | saved single run | BTC 1h | no-filter baseline | `saved-run://2b6f9e33-1c7a-4f6e-8b52-3a8d5c9e0f14` | `research/trend-continuation-slope-filter/configs/example-no-filter.json` | `research/trend-continuation-slope-filter/artifacts/2b6f9e33-1c7a-4f6e-8b52-3a8d5c9e0f14/` | churn comparison |
| `7a1d4c88-5f2b-4e9a-8c07-6b3f2d9a1e55` | saved single run | BTC 1h | 2x-fee stress baseline | `saved-run://7a1d4c88-5f2b-4e9a-8c07-6b3f2d9a1e55` | `research/trend-continuation-slope-filter/configs/example-default-2x-fees.json` | `research/trend-continuation-slope-filter/artifacts/7a1d4c88-5f2b-4e9a-8c07-6b3f2d9a1e55/` | cost robustness check |
| `c4e8b219-3a7f-4d6c-9e10-8f2b5a6d3c07` | saved single run | BTC 1h | random-entry null baseline | `saved-run://c4e8b219-3a7f-4d6c-9e10-8f2b5a6d3c07` | `research/trend-continuation-slope-filter/configs/example-random-entry.json` | `research/trend-continuation-slope-filter/artifacts/c4e8b219-3a7f-4d6c-9e10-8f2b5a6d3c07/` | signal-vs-noise check; seed recorded in config |
| `5d2a7f14-9b3e-4c8a-a1f6-3e7c9b2d5a80` | saved batch/grid | BTC 1h | small structured grid | `saved-batch://5d2a7f14-9b3e-4c8a-a1f6-3e7c9b2d5a80` | `research/trend-continuation-slope-filter/configs/example-small-grid.json` | `research/trend-continuation-slope-filter/artifacts/5d2a7f14-9b3e-4c8a-a1f6-3e7c9b2d5a80/` | source for section 4 top configs |

Search budget:

- Cumulative configs evaluated so far: `4` baselines + `54` small-grid configs = `58`.

Review checklist:

- Review link opens the saved run or saved batch.
- Config link captures exact strategy params, trade config, data range, fees, slippage, leverage, and asset settings.
- Artifact links include orders, fills, positions, signals, PnL points, charts, and any exported grid tables used in the interpretation.
- If a run is discarded, keep it in the registry and mark why it was excluded.

## 3. Baselines

Data:

- BTC 1h.
- Range: 2025-01-01 through 2026-06-30 (discovery range from the research card).
- Candle count: `13,104`.
- Backend commit: `example-commit`.

Baseline runs:

| Run | Config | Net Return | Sharpe | Max DD | Trades | Fee Drag | Decision |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `9f3b2a10-6e5c-4b8a-9d21-9c4a7e0f2b31` | default trend config | `8.4%` | `0.72` | `-14.9%` | `118` | `3.2%` | usable baseline |
| `2b6f9e33-1c7a-4f6e-8b52-3a8d5c9e0f14` | no-filter version | `11.9%` | `0.65` | `-22.4%` | `241` | `7.8%` | reject as churny |
| `7a1d4c88-5f2b-4e9a-8c07-6b3f2d9a1e55` | default with 2x fees | `2.1%` | `0.21` | `-15.7%` | `118` | `6.4%` | weak cost robustness |
| `c4e8b219-3a7f-4d6c-9e10-8f2b5a6d3c07` | random-entry null | `-6.8%` | `-0.41` | `-19.3%` | `121` | `3.4%` | entry signal beats noise |

Baseline interpretation:

The idea may have gross edge, but the no-filter version confirms that raw trend signal alone creates too much churn. The random-entry null baseline is clearly negative with matched exit/sizing/cost logic, so the entry signal itself adds value. Cost robustness is weak enough that later candidates must reduce turnover or improve trade quality.

## 4. Small Structured Grid

Grid question:

Which signal windows and thresholds create a stable response surface before adding extra filters?

Grid:

- fast windows: `12`, `24`, `36`;
- slow windows: `72`, `96`, `144`;
- entry thresholds: `0.25`, `0.35`, `0.45`;
- exit thresholds: `0.05`, `0.15`;
- fixed fees, slippage, leverage, data range, and sizing.

Top configs:

| Rank | Config Family | Net Return | Sharpe | Max DD | Trades | 2x Fee Return | Note |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | `fast=12 slow=72 entry=0.25 exit=0.05` | `18.6%` | `1.08` | `-17.2%` | `312` | `-1.4%` | reject: turnover winner |
| 2 | `fast=24 slow=96 entry=0.35 exit=0.15` | `14.2%` | `1.01` | `-12.8%` | `94` | `6.8%` | candidate region |
| 3 | `fast=24 slow=96 entry=0.45 exit=0.15` | `12.9%` | `0.96` | `-11.7%` | `71` | `7.2%` | candidate region |
| 4 | `fast=36 slow=144 entry=0.35 exit=0.15` | `10.7%` | `0.82` | `-10.5%` | `54` | `6.1%` | lower return, stable |

Response-shape notes:

- Profitable configs cluster around medium and slow windows.
- Low entry threshold produces high turnover and fails fee stress.
- Candidate region survives nearby parameter values.
- Fastest windows appear too reactive for 1h trend continuation.

Initial recommendation:

- Modify before expanding. Add a slope/chop filter because artifact review shows losses concentrate in flat slow-slope periods.

## 5. Reflection Checkpoint

Decision: modify.

Modify budget: this is mechanism change `1` of a `2`-change budget for this research card.

Reason:

The strategy shows a real response shape, but the best raw signal config wins through turnover and fails fee stress. The more stable configs cluster in a medium-window region, but artifact review shows avoidable losses during flat slow-slope segments.

Strategy change:

- Add slow slope filter:
  - require positive slow slope for longs;
  - require negative slow slope for shorts;
  - test minimum slope values `0`, `0.05`, `0.10`.

What did not change:

- Primary objective.
- Fees/slippage/leverage assumptions.
- Data range.
- Baseline interpretation.

## 6. Expanded Grid Plan

Do not run a broad expansion yet.

Next small-grid rerun:

- hold candidate signal region near `fast=24`, `slow=96`;
- test entry thresholds `0.35`, `0.45`;
- test exit thresholds `0.10`, `0.15`;
- test slope minimum `0`, `0.05`, `0.10`;
- compare against previous no-slope candidate configs.

Named question:

Can a slow-slope filter reduce chop losses without destroying trade count or making the result dependent on one trend segment?

## 7. Asset Generalization Path

Chosen path: Option B first, then Option C if ETH diverges.

Rationale:

BTC 1h is the representative discovery asset. If the slope-filtered candidate region survives, run ETH 1h using the same candidate region. If BTC and ETH prefer meaningfully different slope/threshold families, cluster by behavior instead of forcing one global config.

Quarantine: ETH results will not be used to tune parameters. If they are, ETH becomes a discovery asset and a fresh validation asset is required.

## 8. Mid-Research Sweep

Not yet run.

Planned outputs:

- BTC slope-filter small grid;
- ETH validation grid using BTC candidate region;
- per-asset metrics;
- rejected config families;
- whether the edge appears global, asset-specific, or clustered.

## 9. Robustness Scoring

Current scoring draft:

- reward net Sharpe and net return;
- reward 2x-fee survival;
- penalize max drawdown;
- penalize turnover;
- penalize low trade count;
- penalize nearby-config decay;
- penalize BTC-only success if ETH fails the same candidate region.

Current robustness status:

- Parameter sanity: partial pass; medium-window region is stable.
- Cost sanity: partial fail; turnover winner fails 2x fees.
- Artifact sanity: partial fail; chop losses require strategy review.
- Asset sanity: not tested.
- Forward sanity: not tested.

## 10. Objective Review

Current decision:

- Keep the original objective.

Reason:

The first grid did not prove the objective was wrong. It showed the current strategy needs a mechanism to avoid flat/choppy environments. Changing the objective now would hide the weakness rather than test whether the strategy can solve it.

## 11. Final Optimization Loop

Not ready.

Entry condition:

- Slope-filtered small grid must pass cost and artifact sanity.
- ETH validation must not invert the BTC conclusion.
- Candidate region must remain a plateau, not a single winning config.

## 12. Promotion Gates

Current gate status:

- Artifact sanity: not passed. Need slope-filter rerun and trade review.
- Statistical sanity: not passed. Need ETH validation and independent-period check.
- Cost sanity: not passed. Need candidate to survive 2x fees.
- Parameter sanity: partial pass.
- Asset sanity: not tested.
- Regime sanity: not passed. Current result still depends too much on trending periods.
- Forward sanity: not tested.
- Operational sanity: partial pass; leverage and sizing assumptions are plausible, but turnover remains a risk.

## 13. Research Handoff

Current handoff decision:

- Continue research after modifying the strategy.

Summary:

The trend-continuation idea shows a plausible medium-window response surface on BTC 1h, but the raw signal version is too exposed to chop and fee drag. Do not promote any current config. Add the slow-slope filter and rerun a constrained small grid around the candidate region before expanding to ETH.

Evidence supporting this handoff:

- Baseline runs: `9f3b2a10-6e5c-4b8a-9d21-9c4a7e0f2b31`, `2b6f9e33-1c7a-4f6e-8b52-3a8d5c9e0f14`, `7a1d4c88-5f2b-4e9a-8c07-6b3f2d9a1e55`.
- Small grid batch: `5d2a7f14-9b3e-4c8a-a1f6-3e7c9b2d5a80`.
- Artifact review note: `research/trend-continuation-slope-filter/review/chop-loss-review.md`.
- Grid summary export: `research/trend-continuation-slope-filter/artifacts/5d2a7f14-9b3e-4c8a-a1f6-3e7c9b2d5a80/grid-summary.csv`.
- Candidate-region chart pack: `research/trend-continuation-slope-filter/artifacts/5d2a7f14-9b3e-4c8a-a1f6-3e7c9b2d5a80/charts/candidate-region/`.

Next action:

- Implement or configure the slope filter.
- Rerun the small grid described in section 6.
- Append a new write-log entry with run IDs and decision.

## Appendix: Run And Artifact Links

- Saved run detail:
  - `saved-run://9f3b2a10-6e5c-4b8a-9d21-9c4a7e0f2b31`;
  - `saved-run://2b6f9e33-1c7a-4f6e-8b52-3a8d5c9e0f14`;
  - `saved-run://7a1d4c88-5f2b-4e9a-8c07-6b3f2d9a1e55`;
  - `saved-run://c4e8b219-3a7f-4d6c-9e10-8f2b5a6d3c07`.
- Saved batch detail:
  - `saved-batch://5d2a7f14-9b3e-4c8a-a1f6-3e7c9b2d5a80`.
- Exact config snapshots:
  - `research/trend-continuation-slope-filter/configs/example-default.json`;
  - `research/trend-continuation-slope-filter/configs/example-no-filter.json`;
  - `research/trend-continuation-slope-filter/configs/example-default-2x-fees.json`;
  - `research/trend-continuation-slope-filter/configs/example-random-entry.json`;
  - `research/trend-continuation-slope-filter/configs/example-small-grid.json`.
- Artifact review notes:
  - `research/trend-continuation-slope-filter/review/chop-loss-review.md`;
  - `research/trend-continuation-slope-filter/review/turnover-winner-rejection.md`.
- Exported tables:
  - `research/trend-continuation-slope-filter/artifacts/5d2a7f14-9b3e-4c8a-a1f6-3e7c9b2d5a80/grid-summary.csv`;
  - `research/trend-continuation-slope-filter/artifacts/5d2a7f14-9b3e-4c8a-a1f6-3e7c9b2d5a80/neighbor-performance.csv`;
  - `research/trend-continuation-slope-filter/artifacts/5d2a7f14-9b3e-4c8a-a1f6-3e7c9b2d5a80/fee-stress.csv`.
- Chart packs:
  - `research/trend-continuation-slope-filter/artifacts/5d2a7f14-9b3e-4c8a-a1f6-3e7c9b2d5a80/charts/top-configs/`;
  - `research/trend-continuation-slope-filter/artifacts/5d2a7f14-9b3e-4c8a-a1f6-3e7c9b2d5a80/charts/candidate-region/`.

