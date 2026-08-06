# Crypto CTA Seven-Component Trend System

Source extraction and comparison, retrieved 2026-08-05.

- Repository: [OctopusTakopi/crypto-trend-following](https://github.com/OctopusTakopi/crypto-trend-following)
- Upstream construction thread: [macrocephalopod, November 2022](https://x.com/i/web/status/1587591552691765251)
- Repository commit inspected: `804eb428705c913988371c28a57ca051bb3a7f9c`
- Comparison baseline: Robert Carver, *Advanced Futures Trading Strategies*, Strategy 9, extracted in `raw/research/book-extracts/advanced-futures-trading/chapters/09-multiple-trend-following-rules.md`

## Bottom line

This is not a new trend signal. It is a careful crypto-perpetual implementation of the same broad CTA architecture as Carver Strategy 9: multi-horizon moving-average trend, volatility-normalized exposure, diversification-aware sizing, portfolio risk control, buffering, and explicit costs.

Its useful contribution is not a replacement for Carver. It supplies several crypto-specific controls and one credible signal-normalization variant worth testing separately:

1. point-in-time liquidity and listing eligibility, including delisted markets;
2. effective breadth measured from return correlations rather than nominal coin count;
3. rolling, causal standardization of each trend speed instead of importing fixed traditional-futures forecast scalars;
4. measured perpetual funding alongside trading costs;
5. an asymmetric per-market short cap framed as survival insurance against pump/liquidation risk;
6. paired ablations with block-bootstrap uncertainty rather than relying only on headline backtest metrics.

The repository does **not** provide evidence to replace Carver's linear capped forecast with `tanh`, to adopt the overextension response, or to use dynamic crypto clusters as a return-enhancing allocation rule.

## Strategy construction

### Data and timing

- Binance USDT perpetuals, including delisted contracts and excluding stablecoin bases.
- Hourly archives are resampled to daily UTC bars.
- Signals use information through the prior close; rebalancing fills at the next daily open.
- Eligibility is recomputed point in time from minimum history, trailing median quote volume, and bar completeness.
- Missing execution prices freeze rather than fictitiously liquidate a position.

These are repository choices, not claims supplied by the original thread.

### Volatility estimate

The baseline blends 60-day realized volatility with an expanding long-run estimate:

\[
\hat\sigma_{i,t}=0.70\sigma^{ST}_{i,t}+0.30\sigma^{LT}_{i,t}
\]

with a 20% annualized floor and crypto annualization by \(\sqrt{365}\). The source thread recommends a simple short/long blend but does not supply the weights or floor.

### Trend ensemble

The baseline uses log-price EWMA crossovers:

\[
(S,L)\in\{(16,48),(32,96),(64,192)\}
\]

For each speed:

\[
y_{k,i,t}=\frac{EWMA_{S_k}(\log p)-EWMA_{L_k}(\log p)}{\sigma^d_{i,t}\sqrt{L_k}}
\]

and then:

\[
z_{k,i,t}=\frac{y_{k,i,t}}{sd_{365}(y_{k,i,\cdot})}
\]

Available speed forecasts are equally averaged. Young contracts can begin with the faster available rules while slower rules remain unready.

The important distinction from Carver is the **rolling causal standardization**. Carver uses fixed filter scalars calibrated across traditional futures so every speed has mean absolute forecast 10. This repository re-estimates each market/speed's scale from its own trailing year. The constant \(\sqrt{L_k}\) factor cancels algebraically inside the later rolling standardization; the rolling standard deviation is the operative cross-speed calibration.

### Signal-to-position response

The baseline applies:

\[
f(z)=\tanh(z)
\]

Alternatives are clipped linear, binary sign, and an overextension response that reduces exposure after trend strength becomes extreme:

\[
f(z)\propto z e^{-z^2/4}
\]

This response layer is conceptually distinct from Carver's fixed scalar, linear forecast-to-position mapping, and \(\pm20\) cap.

#### Interpretation of the response choices

The two nonlinear functions encode different hypotheses:

- `tanh` is monotonic saturation. A stronger signal never produces a smaller target; additional magnitude simply matters less near full exposure.
- The overextension response is hump-shaped. Exposure peaks at \(|z|=\sqrt{2}\), then falls back toward zero as the signal becomes more extreme. It keeps the trend direction but treats unusually large normalized trends as exhaustion or reversal risk.

The overextension curve is therefore a smooth relative of Carver Strategy 12's adjusted-trend mapping, especially the fast-EWMAC double-V rule that enlarges moderate forecasts and tapers extreme forecasts to zero. Carver found that construction costly and mixed, and did not recommend Strategy 12.

The repository's own ordering is also cautionary: binary sign reported the highest Sharpe estimate, `tanh` and clipped linear were nearly identical, and overextension reported the lowest estimate. The pairwise uncertainty does not establish binary as superior, but it creates a useful hypothesis: **trend direction may contain most of the usable information, while this particular standardized magnitude adds little or is miscalibrated.**

This source-side nonlinearity must remain separate from Money Machine's other positioning questions:

- response mapping is a stateless `current signal -> absolute target` function;
- size distribution controls where incremental inventory is accumulated or released along a price leg and is path/state dependent;
- Citadel-inspired inventory geometry changes marginal desirability as current inventory approaches risky states.

Do not use a hump-shaped signal response as a substitute for price-leg allocation or inventory-conditioned risk.

The discriminating test should precede the mapping choice: estimate forward risk-adjusted return conditional on signal magnitude, using forecast bins and a horizon matched to the rule's holding period. A monotonic relationship supports linear or saturating control; a credible hump supports overextension; a sign-only relationship supports binary as the simple control. Any mapping comparison should hold signal, horizons, costs, buffer, and risk budget fixed and should attribute turnover separately.

### Portfolio construction

Before portfolio targeting, each market receives inverse-volatility exposure. The repository then:

1. estimates a 180-day, pairwise-complete crypto return correlation matrix;
2. shrinks it toward constant correlation and projects it to a positive-semidefinite matrix;
3. reclusters the eligible universe weekly into eight correlation groups;
4. scales groups toward equal standalone full-signal risk;
5. scales the total book to a 20% annualized covariance forecast;
6. caps gross exposure at 2x equity.

This is a data-driven crypto substitute for the source thread's stable, exogenous asset-class sectors. It is more adaptive than Carver's fixed instrument weights and IDM, but also much less stable and more estimation-heavy.

### Buffer, costs, and accounting

- A 10% no-trade buffer trades to the nearest edge rather than all the way to the target.
- Trading costs are modeled as a flat 10 bps baseline with 2/5/10/20 bps sensitivity.
- Published contract funding is charged when available; missing archives are optimistically charged zero and coverage is disclosed.
- Equity compounds, positions are marked through data gaps, and a zero-equity account is treated as ruined rather than artificially kept alive.

## Comparison with Carver Strategy 9

| Layer | Carver Strategy 9 | Repository implementation | Assessment |
|---|---|---|---|
| Price input | Back-adjusted price | Log close | Similar trend information; different futures/perpetual data problem |
| Speeds | Six `(N,4N)` rules from `(2,8)` to `(64,256)` | Three `(N,3N)` rules from `(16,48)` to `(64,192)` | Repository choices are not evidence against Carver's family |
| Per-speed normalization | Price-unit volatility plus fixed forecast scalar | Volatility normalization plus trailing per-market/speed z-score | Worth a separate portability test |
| Combination | Individual cap, equal weight, FDM, final cap | Equal average, then nonlinear bounded response | Same ensemble idea; different scale and mapping |
| Position mapping | Linear forecast strength; normal position at forecast 10 | `tanh` baseline with binary/linear/overextension ablations | No evidence that nonlinear is superior |
| Instrument selection | Cost-based rule eligibility per instrument | Point-in-time history and liquidity gate; all selected speeds used | Crypto gate is useful, but does not replace speed-specific cost eligibility |
| Diversification | Fixed instrument weights and IDM | Dynamic clusters plus full covariance risk target | Useful risk diagnostic; unstable as an allocation edge |
| Trading control | 10% normal-position buffer | 10% market-risk-allocation buffer | Closely aligned |
| Costs | Trading and holding/roll costs in Sharpe units | Flat trading bps plus measured funding | Funding treatment is directly useful for perpetuals |
| Tail constraint | Forecast cap and portfolio/instrument sizing | Gross cap plus optional asymmetric short cap | Crypto-specific survival control worth isolating |

## Reported evidence

The checked-in report states that the frozen baseline achieved net Sharpe 1.04 over 2020–2026 after 10 bps trading costs and measured funding, with Sharpe 0.68 in the design period and 1.54 in the held-out period. Maximum drawdown was 30%. These are repository-reported results, not independently reproduced Money Machine runs.

The more informative findings are structural:

- 268 established single-market trend streams had median gross Sharpe 0.17 and median net Sharpe 0.10.
- Their variance-equivalent effective breadth was only 3.81 despite hundreds of listed contracts.
- Expanding the nominal universe from roughly 64 to the maximum available set barely changed gross portfolio Sharpe.
- Inverse-volatility sizing was the only baseline component ablation whose paired Sharpe-difference interval excluded zero.
- Portfolio risk targeting improved realized risk control and had a positive estimated Sharpe effect, but its paired interval crossed zero.
- Dynamic cluster weighting equalized constructed cluster risk, but its return benefit was statistically unresolved and cluster separation weakened out of sample.
- `tanh` and clipped-linear responses were similar. Binary sign reported the highest Sharpe, but not with a resolved advantage. The overextension response was worse than the baseline estimate.
- Faster crypto trend horizons looked better in the diagnostic, but those cells were inspected after the baseline was frozen and were not promoted as a replacement.
- Wider buffers reduced turnover, but net-performance differences were unresolved.

## What appears valuable for Money Machine

### 1. Effective breadth as a required portfolio diagnostic

The strongest finding is that crypto listing count is not strategy breadth. Correlated altcoin trend streams saturate diversification quickly. Any multi-asset EMAC/EWMAC result should report effective breadth from strategy returns and price-risk correlations alongside asset count.

This can prevent false confidence from a 50- or 100-asset panel that is economically only a few common crypto factors.

### 2. Rolling forecast calibration as a clean Carver variant

Carver's fixed scalars and FDMs were calibrated on traditional daily futures. A causal rolling scale per asset and speed is a defensible crypto/timeframe portability alternative.

It should be tested as one isolated axis:

- keep the same EWMAC spans, cost assumptions, position mapping, and buffer;
- compare fixed Carver scalar/FDM against causal rolling per-speed calibration;
- inspect forecast distribution stability, saturation frequency, turnover, directional validity, and net capture;
- do not simultaneously change horizons or nonlinear mapping.

### 3. Point-in-time universe and delisting discipline

Rolling liquidity/history gates, delisted-contract retention, missing-bar handling, and explicit liquidation assumptions are reusable backtest correctness requirements for broad crypto studies. They are more valuable than the repository's particular $5 million volume threshold.

### 4. Funding as a first-class cost

Directional perpetual trend can hold for weeks. Contract funding should be measured when possible and reported with coverage rather than silently assumed away. Missing funding charged as zero is optimistic and must remain visible.

### 5. Asymmetric short survival constraint

The repository's supplementary rule caps one short near:

\[
\frac{p}{2m}
\]

of gross exposure, where \(p\) is the capital fraction treated as margin and \(m\) is the pump multiple the book should survive. This is a useful risk hypothesis for small-cap perpetuals because long loss is bounded by notional while short loss before liquidation is not.

The daily study cannot test its intended benefit: an intraday pump and retrace is invisible without intraday marks and liquidation mechanics. Treat it as a separate tail-risk/survival experiment, not as an alpha improvement.

### 6. Paired uncertainty for component ablations

Variants share the same market path, so paired block-bootstrap comparisons are better than comparing standalone Sharpe values. This is a useful evaluation pattern for position mapping, risk targeting, clustering, and buffering changes.

## What should not be imported yet

- Do not replace Carver's faithful baseline with the repository's three hand-chosen speeds.
- Do not promote `tanh`, binary, or overextension mappings from the reported ranking; their differences are largely unresolved and the strongest cell may be selection noise.
- Do not treat eight rolling correlation clusters as stable crypto sectors. The cluster count is arbitrary and the out-of-sample separation weakened materially.
- Do not infer institutional capacity from a broad backtest. The repository itself notes that hundreds of alt-perpetual positions are not executable at meaningful institutional scale.
- Do not interpret the 2024–2026 Sharpe as stationary evidence; it differs sharply from the design period and spans only one crypto regime slice.

## Evidence cautions

- The repository has one public commit containing code, choices, results, and narrative together. The claimed freeze-before-results discipline is documented but cannot be verified from public commit history.
- The raw Binance archive mirror is not included, so the checked-in result files are not independently reproducible from the repository alone.
- The commit message reports an earlier/different baseline and breadth result than the checked-in README and report. This provenance inconsistency does not invalidate the code, but it lowers confidence in treating the published metrics as independently verified.
- The daily accounting cannot model intraday liquidation, squeeze paths, order-book impact, queue position, or capacity.
- Funding alignment uses a disclosed daily boundary approximation, and uncovered funding is optimistically zero.
- Most parameters are author choices rather than values supplied by the original thread.

## Decision

**Merge selected mechanisms, not the strategy.** Preserve this source as a useful crypto CTA implementation reference. The highest-value follow-up is a single-axis comparison of Carver's fixed forecast calibration against rolling causal per-asset/per-speed calibration. Effective-breadth reporting, point-in-time universe handling, and measured funding should be treated as general research controls. The asymmetric short cap belongs in a separate intraday survival/liquidation study.

No live strategy, capital allocation, implementation change, Research Board promotion, or Linear work item is implied by this extraction.
