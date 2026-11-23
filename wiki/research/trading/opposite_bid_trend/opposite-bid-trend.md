# Opposite Bid Trend

Status: in progress

Working name: Opposite Bid Trend (formerly Candle Inventory)

Updated: 2026-11-23

## Core idea

> Get me on the right side of the trend and let execution handle the rest.

The trend signal chooses direction. Execution manages when and how much inventory to accumulate or distribute. “Opposite bid” means accumulating against the immediate candle move while staying aligned with the broader trend: buy red candles in a positive trend, and mirror this for shorts. It does not currently imply passive limit orders; the prototype uses simulated market fills.

## Main dials

- **Trend signal:** still TBD. Custom ADX (`signed_strength × agreement`, then shared processing) is the working strategy input. The example instead uses `params.signal` directly, default +1, to isolate execution. The likely direction is a Combo of complementary trend signals; components, weights, and combination rules remain open.
- **Execution:** entry timing, accumulation size, distribution size, and exposure control. A constant accumulation fraction (default 10% of the cap) and distribution fraction (default 100% of current inventory in the ADX variant) are starting points. The static example retains full profit exits. The aim is to make accumulation and distribution adaptive.
- **Required profit after costs:** the reward demanded before distributing inventory. The additional buffer currently defaults to 10 BPS. It will likely become adaptive to asset volatility and risk: how much reward is needed to compensate for the risk taken? The risk measure, horizon, and mapping to required BPS remain undecided.

## Starting policy and assumptions

The intended policy accumulates on candles opposite the signal, distributes on aligned candles when the profit floor is exceeded, and flattens on a zero or opposing signal even at a loss. A zero signal means zero target exposure, regardless of candle direction or profit threshold; already-flat inventory stays flat. Dojis with an aligned directional signal can take available profit; otherwise they hold. New-side accumulation follows on a later qualifying candle.

### Sizing
Options:
1) Let fractions use % of Capital.
2) Use Sig-to-Position Sizing for target, then Fraction of Target.

Fractions:
1) Pyramidding fractions
2) Dynamic Fractions

*Idea*
Measure frequency of consective candle duration to estimate how number of fractions needed for adverse price.



## Static short example observation — 2026-11-19

Saved run `308fe3bf-a28d-4f57-9dda-d7eae1324819` ran `opposite_bid_trend_example` on 50 BTC daily candles with a constant `params.signal = -1`. Destin deliberately selected the recent 50-day window knowing the market had been down and described the performance as outstanding. The saved run confirms a successful, profitable result after simulated costs. It used 1× leverage, equity-compounding sizing, 10% fixed-fraction additions, full profit exits, a 10 BPS additional profit buffer, and 5 BPS each for fees and slippage; volatility targeting/adjustment were disabled. Detailed metrics remain in the saved run/backtest UI.

This supports the strategy's central premise in the selected regime: **get the direction right and let execution handle the rest.** A constant correct-side signal allowed the execution rules to manage accumulation and profit-taking without further signal timing. Because the direction and window were chosen with hindsight, this is an encouraging demonstration of execution conditional on correct direction; identifying that direction prospectively remains the open signal-design problem.

## Implementation status

Packaging checkpoint — 2026-11-23: Fractional distribution is committed in mm_v04
as `da3b5e28`. Updated the stale feature assertions to validate both ADX and historical
volatility outputs; all 156 tests across the two Opposite Bid Trend test modules now
pass, with scoped Ruff passing. Strategy behavior was preserved during packaging.
The snapshot MCP is committed separately as `6943c2ce` and verified through the
refreshed connection. Earlier uncommitted/excluded-test notes below describe their
original verification dates. Nothing pushed.

On 2026-11-20, added ADX Params.distribution_fraction beside accumulation_fraction, finite and in (0, 1], default 1.0. Profit-taking targets current_size × (1 − distribution_fraction), so each qualifying candle closes that fraction of remaining inventory; 0.25 closes 25%. Zero/opposing signals still flatten fully. Final caps, precision, and minimum-notional validation remain in force, so actual fills can differ from the requested fraction. The static example is unchanged. Verification: 167 focused offline checks pass, including repeated long/short partial distributions, the profit gate, full signal exits, and invalid fraction rejection; scoped Ruff/mypy pass. Eight existing ADX feature-count cases were excluded, as they expect one output while the strategy now emits two. Uncommitted.


On 2026-11-20, Destin approved zero signal → zero target exposure. The shared execution helper now returns a signal-exit event for existing inventory on zero, applying to both variants. This supersedes the previous neutral hold/profit rule; directional dojis retain the strict profit gate. Validation: 136 execution-focused offline checks plus scoped Ruff/mypy, including losing long/short exits in both variants, remaining flat on subsequent zero signals, and synthetic engine replay. A broader test attempt had eight ADX feature-count failures during concurrent feature edits; that work was left untouched. Existing order precision/minimum-notional constraints still apply.

Both the static example and ADX execution paths were repaired on 2026-11-19. Their helper decision now always supplies the inventory target, followed by the exposure cap and target-minus-current order. Fixed-fraction additions, profit-gated full exits, zero/opposing-signal flattening, directional-doji holds/profit-taking, and cap reductions on holds are covered through actual broker fills. Signal magnitude does not scale the fixed fraction; sign selects direction. Capital/risk sizing and sizing snapshots remain available. A missing finite cap is rejected explicitly for accumulation because a fraction of an unbounded maximum is undefined.

The diagnosis compared commits cca6f11a (trade events), e10f789c (fixed BPS floor), and 44f2b666 (hold caps/neutral profit-taking). Helper logic still matches 44f2b666; only its type import moved. The broken uncommitted wiring used the full signal target except when already over cap. Removed that competing path and its unused adjustment calculation from both variants. Volatility-adjustment and rebalance settings are not applied to either variant's execution policy; defining their role remains separate work. Volatility targeting still supplies the sizing cap.

The ADX working clone now uses the same decision target → cap → delta path, with ADX calculation/processing and volatility sizing preserved. Rebalancing remains deliberately excluded. Validation: 168 focused offline checks pass, including actual ADX full/summary synthetic replay, long/short execution, caps, costs and registry discovery; scoped Ruff and mypy pass. A broader run also hit 12 pre-existing Example comparison-fixture failures using the removed MIN_ADJUSTMENT_VALUE_PCT field; those fixtures were not changed. No historical backtest or runtime restart was performed. The ADX repair is uncommitted.

Code variants (registered separately):

- Working strategy: [bid_algo/opposite_bid_trend.py](../../../../../mm_v04/backend/app/backtest/strategies/bid_algo/opposite_bid_trend.py), key `opposite_bid_trend`, class `OppositeBidTrendStrategy`.
- Example: [opposite_bid_trend_example.py](../../../../../mm_v04/backend/app/backtest/strategies/opposite_bid_trend_example.py), key `opposite_bid_trend_example`, class `OppositeBidTrendExampleStrategy`. Static `params.signal` defaults to +1 (long); negative is short and zero is neutral. It bypasses signal processing and emits `static_signal` (version 3). ADX parameters are removed from the example; warmup depends only on enabled volatility features, otherwise zero.

Destin cloned the example into the bid-algo folder; the package is named `bid_algo` for normal Python imports. Each strategy file defines its own Params, Config, and TradeConfig classes so the variants can evolve independently. InventorySide lives in dto/trade.py; the separate opposite_bid_trend DTO file was removed. Both strategies use the candle decision helper. Registration changes preserve both implementations. Historical saved configurations and runs were not rewritten; reruns using the old `candle_inventory` key need a current strategy selection.

Related: [[research/trading/research_index|Research Home]], [[engineering/bounded-ema-history|Feature and sizing implementation notes]], [[sessions/current-checkpoint|Current checkpoint]].

Code checkpoint: `f82dfe45` (2026-11-19), committed at Destin's request; not pushed.
