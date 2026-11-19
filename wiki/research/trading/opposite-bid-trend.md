# Opposite Bid Trend

Status: in progress  
Working name: Opposite Bid Trend (formerly Candle Inventory)  
Updated: 2026-11-19

## Core idea

> Get me on the right side of the trend and let execution handle the rest.

The trend signal chooses direction. Execution manages when and how much inventory to accumulate or distribute. “Opposite bid” means accumulating against the immediate candle move while staying aligned with the broader trend: buy red candles in a positive trend, and mirror this for shorts. It does not currently imply passive limit orders; the prototype uses simulated market fills.

## Main dials

- **Trend signal:** still TBD. Custom ADX (`signed_strength × agreement`, then shared processing) is the working strategy input. The example instead uses `params.signal` directly, default +1, to isolate execution. The likely direction is a Combo of complementary trend signals; components, weights, and combination rules remain open.
- **Execution:** entry timing, accumulation size, distribution size, and exposure control. A constant accumulation fraction (default 10%) and full profit exits are starting points. The aim is to make accumulation and distribution adaptive.
- **Required profit after costs:** the reward demanded before distributing inventory. The additional buffer currently defaults to 10 BPS. It will likely become adaptive to asset volatility and risk: how much reward is needed to compensate for the risk taken? The risk measure, horizon, and mapping to required BPS remain undecided.

## Starting policy and assumptions

The intended policy accumulates on candles opposite the signal, distributes on aligned candles when the profit floor is exceeded, and flattens on an opposing signal even at a loss. Neutral signals and dojis can take available profit; otherwise they hold. New-side accumulation follows on a later qualifying candle.

The current profit test compares stored ROE converted to BPS against `2 × fee_rate × 10,000 + exit_slippage_bps + bps`, using a strict greater-than comparison. Entry slippage is already reflected in the stored return. This is a fixed cost allowance, independent of leverage, rather than an exact net realized-profit calculation. Adaptive risk-based BPS is a research direction, not implemented behavior.

Example-derived volatility and sizing tools are available. Same-close market fills, minimum-order constraints, and no forced final exit remain simulation assumptions. The caller owns ordered, once-per-candle delivery.

## Implementation status

The static example's execution path was repaired on 2026-11-19. Its helper decision now always supplies the inventory target, followed by the exposure cap and target-minus-current order. Fixed-fraction additions, profit-gated full exits, opposing-signal flattening, neutral/doji holds/profit-taking, and cap reductions on holds are covered through actual broker fills. Signal magnitude does not scale the fixed fraction; sign selects direction. Capital/risk sizing and sizing snapshots remain available. A missing finite cap is rejected explicitly for accumulation because a fraction of an unbounded maximum is undefined.

The diagnosis compared commits cca6f11a (trade events), e10f789c (fixed BPS floor), and 44f2b666 (hold caps/neutral profit-taking). Helper logic still matches 44f2b666; only its type import moved. The broken uncommitted wiring used the full signal target except when already over cap. Removed that competing path and its unused adjustment calculation from the example. Volatility-adjustment and rebalance settings are not applied to the example's execution policy; defining their role remains separate work. Volatility targeting still supplies the sizing cap.

The ADX working clone retains the old competing target path and needs the equivalent execution correction before relying on its results. This repair was scoped to the example. Validation: 98 focused offline checks including long/short broker sequences, strict BPS gates, small orders, cap reductions and full/summary synthetic replay; scoped Ruff and strict mypy pass. No historical backtest or runtime restart was performed.

Code variants (registered separately):

- Working strategy: [bid_algo/opposite_bid_trend.py](../../../../mm_v04/backend/app/backtest/strategies/bid_algo/opposite_bid_trend.py), key `opposite_bid_trend`, class `OppositeBidTrendStrategy`.
- Example: [opposite_bid_trend_example.py](../../../../mm_v04/backend/app/backtest/strategies/opposite_bid_trend_example.py), key `opposite_bid_trend_example`, class `OppositeBidTrendExampleStrategy`. Static `params.signal` defaults to +1 (long); negative is short and zero is neutral. It bypasses signal processing and emits `static_signal` (version 3). ADX parameters are removed from the example; warmup depends only on enabled volatility features, otherwise zero.

Destin cloned the example into the bid-algo folder; the package is named `bid_algo` for normal Python imports. Each strategy file defines its own Params, Config, and TradeConfig classes so the variants can evolve independently. InventorySide lives in dto/trade.py; the separate opposite_bid_trend DTO file was removed. Both strategies use the candle decision helper. Registration changes preserve both implementations. Historical saved configurations and runs were not rewritten; reruns using the old `candle_inventory` key need a current strategy selection.

Related: [[research/trading/research_index|Research Home]], [[engineering/bounded-ema-history|Feature and sizing implementation notes]], [[sessions/current-checkpoint|Current checkpoint]].

Code checkpoint: `f82dfe45` (2026-11-19), committed at Destin's request; not pushed.
