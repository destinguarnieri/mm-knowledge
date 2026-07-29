# Quantile Regression Trading Reference

Status: draft

Extracted text from external QR trading screenshots (source images co-located under `images/`). This is a faithful transcription of the tables, not MM-validated evidence. Claims about IR lift, win rate, and BTC session behavior are from the source material — treat as hypotheses until tested in-repo.

Sources:

- `images/QR_trading_1.png` — ranked knobs / IR impact
- `images/QR_trading_2.png` — decision mapping vs raw signal failure modes
- Original copies also under `mm_v04/backend/app/lib/analysis/QR_trading_{1,2}.png`

Related: [[research/trading/research_process_v2|Research Process V2]], [[research/trading/research_index|Research Board]]

---

## Knobs ranked by IR impact

From `QR_trading_1.png`.

| Rank | Knob | Range that matters | IR impact | How to tune it properly |
| ---: | --- | --- | --- | --- |
| 1 | Lookback length (`lb`) | 21 → 89 | **+0.9 IR** (34 → 55 is sweet spot) | Longer = smoother slope, higher IC but laggy entries |
| 2 | R² threshold (`min_r2`) | 0.88 → 0.96 | **+0.7 IR** (0.92 → 0.94 peak) | Higher = fewer signals, but 90%+ win rate |
| 3 | Signal weighting function | `slope * r2**p` | **+0.6 IR** (p=2.0 → 2.7 best) | `strength = slope * r2**2.5` kills weak trends |
| 4 | Forward horizon | 3 → 8 min | **+0.5 IR** (5 min absolute peak) | 5 min = max IC, 8 min = max profit factor |
| 5 | Input price transformation | log(close) → log(HLC3) → log(EMA(high/low)) | **+0.4 IR** | `log(ta.ema(high,3) * ta.ema(low,3))**0.5` = cleanest line |
| 6 | R² acceleration filter | `r2 - r2[10] > δ` | **+0.35 IR** (δ = 0.12 → 0.18) | Only enter when trend confidence is rising fast |
| 7 | Volatility normalization | divide slope by ATR(14) or close stdev | **+0.3 IR** | Makes signal comparable across 2024 chop vs 2025 pumps |
| 8 | Dynamic min_r2 via rolling IC | `min_r2 = 0.90 + 0.05 * (1 - IC_rolling)` | **+0.25 IR** | Auto-tightens filter when edge weakens |
| 9 | Session filter | Trade only 9:30–16:00 EST or 20:00–02:00 UTC | **+0.2 IR** | US + Asia sessions = where BTC actually trends |
| 10 | Volume confirmation | `volume > 2.5 × EMA(volume,50)` | **+0.15 IR** | Removes fake 3 AM pumps |

### Knob formulas (quick copy)

```text
strength = slope * r2**2.5
price_line = log(ta.ema(high,3) * ta.ema(low,3))**0.5
r2_accel_ok = r2 - r2[10] > δ          # δ ≈ 0.12–0.18
min_r2 = 0.90 + 0.05 * (1 - IC_rolling)
vol_confirm = volume > 2.5 * EMA(volume, 50)
```

---

## Decision layer: what replaces the raw signal

From `QR_trading_2.png`. Maps each trading decision to a quantile-forecast quantity and why a raw (binary / lagging) signal fails at that step.

| Decision | What to use | Why raw signal dies here |
| --- | --- | --- |
| Direction | `sign(forecast_50 - current_price)` | Signal can lag 1–2 bars; forecast already baked in momentum |
| Entry trigger | `forecast_10th > current_price + 15 bps` (for longs) | Only enter when downside is statistically impossible |
| Position sizing | `edge_probability × volatility_target` | Raw signal is binary (on/off). Forecast gives you 64% → 89% gradient |
| Take-profit | `forecast_90th` | Locks in the exact 90th percentile edge |
| Stop-loss | `forecast_10th - 0.1%` | Dynamic, never fixed % |
| Exit on decay | `edge_probability < 70%` OR `r2_accel < 0` | Signal can stay high while edge vanishes |

### Decision formulas (quick copy)

```text
direction     = sign(forecast_50 - current_price)
long_entry    = forecast_10th > current_price + 15_bps
size          = edge_probability * volatility_target
take_profit   = forecast_90th
stop_loss     = forecast_10th - 0.1%
exit_decay    = (edge_probability < 0.70) or (r2_accel < 0)
```

---

## Notes / open questions for MM use

- Source is external / unverified — IR deltas and “90%+ win rate” are claims to test, not accepted MM evidence.
- Horizon is framed in minutes (3–8 min; 5 min peak IC) — map carefully onto MM candle TFs before any backtest.
- Forecast objects assumed: `forecast_10th`, `forecast_50`, `forecast_90th`, plus `edge_probability` and `r2_accel`. Confirm which of these we can actually produce from our QR / signal stack.
- Next move: none until Destin decides whether this becomes an active research thread on the [[research/trading/research_index|Research Board]].
