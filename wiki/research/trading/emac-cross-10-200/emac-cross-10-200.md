# EMA Cross 10/200 Research

Related process: [[research/trading/research_process_v1|Research Process V1]]

## Status

- Research state: BTC timeframe scan and tiered-history liquid-universe `4h` screen complete for assets in the first 200 Research MCP records.
- Current decision: retain separate 5,000-, 2,500-, and 1,000-candle cohorts. ETH remains the cleanest long-history leader; POL and PAXG merit follow-up from the 2,500-candle cohort, while HYPE, MET, and MON remain provisional due to only 4–8 realized trades.
- Started: 2026-07-11 00:18 EDT.
- Strategy: `emac_cross`, fast EMA `10`, slow EMA `200`.
- Initial asset: BTC; liquid-universe screen used a point-in-time `$250,000` rolling 24-hour Hyperliquid notional-volume floor.

## Research Question

Does a passive 10/200 EMA cross, continuously targeting maximum long or maximum short exposure after the first cross, produce useful net risk-adjusted performance on BTC across `1d`, `4h`, `1h`, `30m`, `5m`, and `1m`?

Primary KPI: net annualized Sharpe after fees and slippage. Supporting evidence: total return, CAGR, maximum drawdown, trade count, win rate, profit factor, annualized volatility, and cost drag when available.

## Fixed Baseline Assumptions

- Candle source: Binance USD-M perpetual `BTCUSDT`.
- Initial capital: `$10,000`.
- Position sizing: compounding.
- Maximum position: `100%` of equity at `1x` leverage.
- Fee rate: `0.0005` (`5 bps`).
- Slippage input: `5.0` (`5 bps`; this field is expressed directly in basis points).
- Initial state: flat until the first observed cross; subsequent crosses flip between maximum long and maximum short.
- Funding is absent from OHLCV results and remains an explicit limitation.
- Timeframes may require different calendar windows because the explicit-request cap is 100,000 candles. Cross-timeframe results are therefore intuition-building, not a controlled ranking unless their windows overlap.

## Run Registry

Cumulative reviewable asset-window evaluations: `86` successful. The liquid `4h` universe now contains 52 comparable 5,000-candle results, 20 shorter-history 2,500-candle results, and seven 1,000-candle results. APEX is unsupported on Binance USD-M and MEGA remains 31 candles short of the 1,000-candle window. One additional 57,192-bar BTC `1h` attempt completed computation but failed autosave.

### `ce0bc93e-01c6-41cb-8a2b-3b08a5ef26a1` — BTC `1d`

- Requested range: 2020-01-01 through 2026-07-10 UTC.
- Scored bars: `2,183` after the 200-bar warmup; complete candle load with no gaps.
- Net return: `93.67%`; CAGR: `11.70%`.
- Sharpe: `0.471`; HAC Sharpe: `0.480`.
- Maximum drawdown: `-45.77%`; worst position ROE: `-17.93` percentage points; annualized volatility: `43.92%`.
- Time in money: `88.21%` of active bars.
- Trades: `22`; win rate: `27.27%`; profit factor: `1.266`.
- Net P&L: `$9,366.66`; total fees: `$288.85`.
- Fee drag / initial capital: `2.89%`; total cost drag / initial capital: `5.78%`.
- Turnover / average equity: `42.31x`.
- Interpretation: positive absolute performance driven by infrequent large winners, but Sharpe is weak and drawdown is severe. This is useful enough to continue the timeframe scan, not strong enough to treat as a candidate.

### `78ee3fe1-ee12-40d7-b68c-e962344d8652` — BTC `4h`

- Requested range: 2020-01-01 through 2026-07-10 UTC; `14,098` scored bars.
- Net return: `918.01%`; CAGR: `43.44%`; Sharpe: `0.935`.
- Maximum drawdown: `-68.25%`; worst position ROE: `-32.85` percentage points.
- Time in money: `84.62%` of active bars; trades: `122`; win rate: `27.87%`; profit factor: `1.424`.
- Fee drag / initial capital: `59.20%`; total cost drag / initial capital: `118.40%`; turnover / average equity: `222.37x`.
- Interpretation: strongest BTC interval by Sharpe and profit factor, but its extreme drawdown prevents promotion. It is the only reasonable interval for an initial cross-asset screen.

### `2c8223d5-4c4a-445e-82ac-cbd957379c14` — BTC `1h`

- Requested range: 2025-05-20 08:00 through 2026-07-10 UTC; `9,800` scored bars.
- Net return: `-8.83%`; CAGR: `-7.94%`; Sharpe: `-0.020`.
- Maximum drawdown: `-34.64%`; worst position ROE: `-4.18` percentage points.
- Time in money: `84.58%` of active bars; trades: `114`; win rate: `28.07%`; profit factor: `0.915`.
- Gross return before fees: `1.67%`; fee drag / initial capital: `10.51%`; total cost drag / initial capital: `21.01%`.
- Interpretation: approximately flat gross edge becomes negative after costs. Reject the current flip-only monetization on this interval, not necessarily the directional signal.

### `756fade0-fc72-4397-96be-8790607f9080` — BTC `30m`

- Requested range: 2025-12-14 16:00 through 2026-07-10 UTC; `9,800` scored bars.
- Net return: `-16.72%`; CAGR: `-27.91%`; Sharpe: `-0.555`.
- Maximum drawdown: `-36.27%`; worst position ROE: `-3.12` percentage points.
- Time in money: `83.87%` of active bars; trades: `114`; win rate: `22.81%`; profit factor: `0.813`.
- Gross return before fees: `-6.59%`; total cost drag / initial capital: `20.25%`.
- Interpretation: negative before and after fees despite spending most active bars in profit. Reject the current monetization on this interval.

### `e40c891e-8302-4317-b588-5a00a9a5a169` — BTC `5m`

- Requested range: 2026-06-06 06:40 through 2026-07-10 UTC; `9,800` scored bars.
- Net return: `-33.43%`; Sharpe: `-9.389`; maximum drawdown: `-36.94%`; worst position ROE: `-1.94` percentage points.
- Time in money: `79.66%` of active bars.
- Trades: `128`; win rate: `13.28%`; profit factor: `0.371`.
- Gross return before fees: `-23.09%`; total cost drag / initial capital: `20.68%`.
- Interpretation: structurally poor over this short recent sample; costs compound an already negative gross signal. Reject.

### `987817d2-0c0f-406d-aa92-09b0da5fae38` — BTC `1m`

- Requested range: 2026-07-04 01:20 through 2026-07-10 UTC; `9,800` scored bars.
- Net return: `-25.37%`; Sharpe: `-36.260`; maximum drawdown: `-25.85%`; worst position ROE: `-0.94` percentage points.
- Time in money: `77.84%` of active bars.
- Trades: `137`; win rate: `10.22%`; profit factor: `0.251`.
- Gross return before fees: `-13.34%`; total cost drag / initial capital: `24.07%`.
- Interpretation: rapid churn overwhelms the strategy over the one-week sample. Reject.

### `3c0f2043-aeac-44da-945f-523965b33c97` — 20-asset `4h` batch

- Requested range: 2024-03-29 16:00 through 2026-07-10 UTC; 5,000 requested and 4,800 scored bars per successful asset.
- Outcome: `19/20` assets succeeded; MATIC failed because only 995 candles existed before its Binance USD-M symbol stopped producing data.
- Aggregate: median Sharpe `0.438`, median net return `12.42%`, median maximum drawdown `-64.38%`, median profit factor `0.951`, and median expectancy `-$22.95`.
- Position path: median time in money `87.84%`, median realized win rate `23.73%`, and median worst position ROE `-11.76` percentage points. The monetization gap generalized across assets.
- Breadth: 14 assets had positive Sharpe, 11 had positive net return, nine had profit factor above one, and four cleared Sharpe `1.0`.
- Leading assets:
  - ETH — Sharpe `1.169`, net return `193.50%`, maximum drawdown `-31.61%`, worst position ROE `-8.08` points, profit factor `1.822`.
  - SUI — Sharpe `1.350`, net return `479.59%`, maximum drawdown `-51.38%`, worst position ROE `-10.13` points, profit factor `1.642`.
  - ARB — Sharpe `1.044`, net return `199.33%`, maximum drawdown `-56.64%`, worst position ROE `-21.94` points, profit factor `1.792`.
  - DOGE — Sharpe `1.023`, net return `190.88%`, maximum drawdown `-63.19%`, worst position ROE `-11.76` points, profit factor `1.366`.
- BTC same-window control: Sharpe `0.770`, net return `66.11%`, maximum drawdown `-38.72%`, worst position ROE `-7.11` points, and profit factor `1.414`.
- Interpretation: the strategy is not a universal `4h` edge; the median asset remains weak after costs and suffers severe drawdown. A coherent leader cluster exists, with ETH offering the strongest balance rather than the highest headline return.

### `8c3d5e49-5026-4146-a7be-d7fe1a6a1f7f` — 30-asset liquid `4h` batch

- Liquidity snapshot: Hyperliquid `dayNtlVlm >= $250,000` at 2026-07-11 02:21 EDT.
- Outcome: `23/30` completed the common 5,000-candle range; ZRO, HYPE, EIGEN, SAGA, SYRUP, WLFI, and TRUMP lacked full history.
- Aggregate: median Sharpe `0.276`, median net return `-18.80%`, median maximum drawdown `-75.68%`, median profit factor `0.842`, median time in money `85.34%`, and median trade win rate `20.00%`.
- Leaders:
  - ZEC — Sharpe `1.323`, net return `585.99%`, but maximum drawdown `-79.12%`, worst position ROE `-24.63` points, and cost drag `31.77%`.
  - kBONK — Sharpe `0.894`, net return `136.93%`, maximum drawdown `-68.88%`, worst position ROE `-17.53` points.
  - XLM — Sharpe `0.887`, net return `140.27%`, maximum drawdown `-59.57%`, worst position ROE `-11.58` points, but cost drag `31.65%`.
  - WLD — Sharpe `0.829`, net return `105.78%`, maximum drawdown `-59.66%`, worst position ROE `-21.60` points.
- Interpretation: broader breadth weakened the median result. ZEC's headline Sharpe is not sufficient to outrank ETH after risk and costs.

### `c98d9c89-971c-440a-9647-44929937e3bf` — 32-asset liquid `4h` batch

- Outcome: `11/32` completed the common range; 21 mostly newer listings lacked 5,000 candles.
- Aggregate: median Sharpe `0.291`, median net return `-23.85%`, median maximum drawdown `-81.39%`, median profit factor `0.809`, median time in money `86.92%`, and median trade win rate `25.00%`.
- HBAR was the only Sharpe-above-one result (`1.308`) but is excluded from a risk-filtered Top K: maximum drawdown `-70.49%`, worst position ROE `-61.47` points, and cost drag `70.75%`.
- IOTA returned Sharpe `0.799` and `102.75%` net return, but its `-81.39%` drawdown also fails a risk-aware ranking.
- Interpretation: no new clean leader emerged.

### `28a4f773-c94c-48c1-892f-de1ff8ce6ab0` — MEGA `4h` history check

- MEGA cleared the liquidity floor but had only 969 of 5,000 requested candles, so it joins the separate new-listing cohort.

### `a32d01a7-096b-4ba8-b17f-b3c35baad2c3` — 29-asset `2,500`-candle `4h` cohort

- Outcome: `20/29` completed; HYPE, PUMP, WLFI, APEX, MON, SKY, MET, ASTER, and MEGA still lacked the requested range or Binance support.
- Aggregate: median Sharpe `-0.123`, median net return `-49.22%`, median maximum drawdown `-70.91%`, median profit factor `0.535`, median time in money `84.96%`, and median trade win rate `20.42%`.
- Credible leaders:
  - POL — Sharpe `1.231`, net return `81.82%`, maximum drawdown `-40.08%`, profit factor `2.130`, and 18 trades.
  - PAXG — Sharpe `0.888`, net return `22.03%`, maximum drawdown `-26.04%`, profit factor `1.324`, and 24 trades.
  - TRUMP — Sharpe `0.741`, net return `32.69%`, maximum drawdown `-43.24%`, profit factor `1.194`, and 13 trades.
- ENA and POPCAT were marginally positive, while the other 15 assets were net-negative.
- Interpretation: the shorter-history cohort is weak in aggregate, but POL and PAXG are materially better than the cohort median and deserve validation without merging their scores into the 5,000-candle ranking.

### `687ef1b4-2043-4fc3-8742-5330d2ec415a` — nine-asset `1,000`-candle `4h` cohort

- Outcome: `7/9` completed. APEX is unsupported on Binance USD-M; MEGA had 969 candles and missed the requested window by 31.
- Aggregate: median Sharpe `-0.913`, median net return `-12.90%`, median maximum drawdown `-38.61%`, median profit factor `0.505`, median time in money `86.56%`, and median trade win rate `17.65%`.
- Positive but low-count observations:
  - HYPE — Sharpe `1.040`, net return `21.14%`, maximum drawdown `-38.61%`, profit factor `1.164`, but only eight trades.
  - MET — Sharpe `0.956`, net return `18.02%`, maximum drawdown `-25.67%`, profit factor `1.598`, but only four trades.
  - MON — Sharpe `0.706`, net return `9.16%`, maximum drawdown `-43.98%`, profit factor `1.250`, but only seven trades.
- ASTER, PUMP, SKY, and WLFI were negative.
- Interpretation: HYPE, MET, and MON are watchlist observations, not ranking-quality evidence. The very low trade counts make their Sharpe estimates fragile.

## Preliminary Risk-Filtered Top 10

Selection requires positive net return, profit factor above one, maximum drawdown better than `-70%`, and worst position ROE better than `-25` percentage points, then ranks by Sharpe:

1. SUI
2. ETH
3. ARB
4. DOGE
5. kBONK
6. kPEPE
7. XLM
8. WLD
9. BTC
10. SEI

This is a screening rule, not a promotion gate. ZEC, HBAR, and IOTA rank highly on headline Sharpe but fail the stated risk filter.

## Cross-Timeframe Diagnosis

`pct_time_in_money` is the fraction of active bar snapshots whose position ROE is positive; it is not a direct signal-classification accuracy measure. Even so, the consistent `77.84%`–`88.21%` range alongside only `10.22%`–`28.07%` realized win rates is important: positions are profitable during most active bars, but the flip-only exit often gives the favorable excursion back before realization.

Worst position ROE and portfolio drawdown separate two failure modes:

- `1d` and `4h` allow large adverse excursions within a position (`-17.93` and `-32.85` percentage points), alongside severe portfolio drawdowns.
- `1h` through `1m` keep the worst individual adverse ROE much smaller (`-4.18` to `-0.94` points), yet still accumulate `-25.85%` to `-36.94%` portfolio drawdowns through repeated losses and costs.

The evidence therefore does not simply say that the EMA direction is useless at shorter intervals. It says the current rule—hold until the opposite cross and then flip fully—is poorly monetizing favorable position paths. A later mechanism test should target profit retention and churn reduction rather than immediately widening the EMA parameter search.

## Write Log

### 2026-07-11 00:18 EDT

Opened the BTC 10/200 baseline timeframe scan. The first run is BTC `1d`; each result will be interpreted before advancing to the next interval.

### 2026-07-11 00:20 EDT

Completed BTC `1d` run `ce0bc93e-01c6-41cb-8a2b-3b08a5ef26a1`. The run loaded all 2,383 requested Binance candles and scored 2,183 after warmup. Net return was positive, but `0.471` Sharpe and `-45.77%` maximum drawdown indicate poor risk-adjusted quality. Continue to `4h` to learn whether the faster interval improves responsiveness without allowing turnover and costs to dominate.

### 2026-07-11 00:40 EDT

Completed the remaining BTC timeframe scan. The six-year `4h` run materially outperformed `1d` on Sharpe (`0.935` versus `0.471`) but suffered `-68.25%` maximum drawdown. A 57,192-bar `1h` attempt exposed an autosave timeout after generating roughly 250,000 artifacts, so the reviewable `1h`, `30m`, `5m`, and `1m` runs were limited to 10,000 requested bars each. All four were net-negative; deterioration accelerated as interval length shortened. Next question: does the fixed 10/200 configuration show a coherent `4h` edge across other assets, or was BTC performance asset-specific?

### 2026-07-11 01:08 EDT

Revised the interpretation to include time in money and worst position ROE. Every interval spent at least `77.84%` of active bars with positive position ROE, despite low realized win rates. The combination points to profit giveback and poor exit monetization rather than a clean rejection of directional information. Worst position ROE is now tracked alongside portfolio maximum drawdown for every run.

### 2026-07-11 01:48 EDT

The existing shared-config Research MCP batch path now supports Binance USD-M with per-asset symbol derivation and partial failure isolation. The request bound is 32 assets while execution concurrency remains eight. This removes the tooling blocker for the planned `4h` cross-asset screen; no new strategy result was produced in this implementation step.

### 2026-07-11 02:04 EDT

Completed 20-asset Binance USD-M `4h` batch `3c0f2043-aeac-44da-945f-523965b33c97`. Nineteen assets completed across a common 5,000-candle window; MATIC failed cleanly on missing post-delisting history. ETH, SUI, ARB, and DOGE cleared Sharpe `1.0`, but median profit factor remained below one and median maximum drawdown was `-64.38%`. The high-time-in-money/low-realized-win pattern persisted across the batch, strengthening the profit-retention diagnosis. Pause before wider screening to choose whether the next test should validate the leader cluster or modify exit monetization.

### 2026-07-11 02:28 EDT

Applied a point-in-time `$250,000` rolling 24-hour Hyperliquid notional-volume floor and expanded the common-window screen through three additional batch calls. The two substantive runs requested 30 and 32 assets; a final one-asset MEGA check completed the known liquid set available within the first 200 Research MCP assets. Thirty-four additional assets produced reviewable results and 29 liquid assets lacked the full 5,000-candle Binance window. Broader breadth weakened the median outcome and produced no cleaner leader than ETH. Formed a preliminary risk-filtered Top 10 for lower-timeframe testing while keeping the 29 newer assets in a separate cohort.

### 2026-07-11 02:38 EDT

Worked backward through the 29 incomplete-history assets. A common trailing 2,500-candle run recovered 20 assets; a trailing 1,000-candle run recovered seven of the remaining nine. POL and PAXG were the strongest shorter-history results. HYPE, MET, and MON were positive in the 1,000-candle cohort but produced only 4–8 trades, so they remain provisional. APEX has no Binance USD-M symbol and MEGA is 31 candles short of the 1,000-candle requirement. Kept all three calendar-window cohorts separate to avoid biased ranking.
