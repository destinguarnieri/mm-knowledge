# Trading Catalog

Status: draft

This is a catalog of indicators, signals, and concepts used in manually trading strategies Ive learned over the years.

## Implementation and evaluation queue

This glossary is the wording and maturity source for the canonical [[research/trading/catalog_queue|Trading Catalog Implementation and Evaluation Queue]]. The queue records type, implementation evidence, smallest first-pass measurement/evaluation, dependencies, Destin review questions, candidate uses, and execution state without rewriting the source entries below.

Independent primitives may be measured and evaluated by separate agents. Recommended measurements for underspecified entries are provisional until Destin reviews whether they capture his intent. PRI, PRL, PRZ, and PRB are independently testable parts and one combined Price Reversal System. Queueing any primitive does not assert alpha, and combining primitives into a strategy still requires an explicit hypothesis and protected evaluation.

## High Low Channel (HL_Channel)

Trends can be defined as higher highs or lower lows.

Therefor it makes sense to measure the highs and the lows of the asset.

When measured and plotted at the same time it forms a channel, known as the High Low Channel or HL_Channel for short.

Price is effectively only in two states regarding the channel. It is either outside the channel or inside the channel.
This could be split further into three states to more accurately descibe it.
Above Channel, Inside Channel, Below Channel.

Price breaking out of a channel, or price falling back inside the channel are core to utilizing it as a breakout or trend strategy.

Price can also be traded inside the channel using the channel as the range bounds.

Observation: Sustained vertical price action only occurs outside the channel.

Logical explanation. If an asset is making sustained verticle progress it can be said to be trending.
If it is trending it is either making higher highs or lower lows.
If its making higher highs or lower lows that will be reflected in the HL channel.
More specifically it will be refleted in the prices relationship to the HL channel.

There is second derivite studys on the channel that can be usefull namely the Slope of the channel and the spread distance.

A unique propety of measuring high and low channel slope seperately is identifyiing when the High and Low Channel Slopes Disagree.

## Moving Average Convention

*Note: we generally use Exponential moving average for many calculations with exception of vwap. Not a hard rule but when in doubt use EMA.*

## 200 EMA

Well know and widely used. simple and effective.
Good starting point on getting positioned on the right side of market.
Often used in combination with others.

## Moving Average Crossing

The main Moving averages preffered are the 10 and 200 periods combined, as together they enable you to answer several important questions.

Where is the long term and short term trends? Is the trend just starting? How extended is it? Is it expanding or contracting.

We chose the 10 Ema as the short term indicator as it is snappy enough to capture the beginning portion of the trend, while not being overly sensitive to price fluctions around the longer term trend.

The 10 EMA is also fast enough to detect when the expansion portion of the trend is done and contraction is begining, without giving back too much profit.

It should be said that in practice I use the 10 EMA LOW(see channel) as the short term indi, with reasoning that close prices often chop near the long term trend(200) and by using the LOWs (or highs) you get cleaner verification that price is trending in the cross overs direction.

Note: The Ema crossing is often used to frame the opportunity set, but seldom used alone without measuring where the price is in relationship to the moving averages. For that we use PX(Price Extension). More on that later.

## MA Ribbon

The natural extension of using two moving averages is adding more.
For this I propose 5 moving averages with the spans of: [10,20,50,100,200]

This creates what I call a ribbon of moving averages.

This should be considered a tool that can be utilized multiple ways.

For one you might want to know how the moving averages are stacked.
Are they all in same direction? Are they entangled?
Are they expanding or contracting?which ones are expanding which ones are contracting?
Did 2 of them just cross?

Secondly you might want to know where price is in relation to the stack.
an example might be price is under the 10 and 20 but over the 50 , 100, 200.

Observation: Price only makes vertical progress when it has "cleared" all of the averages.
That is to say moving averages act as support and resistance .
Once the resistence is lifted it can trend.

Observation #2: Price stair steps up and down from one moving average to the next.
Example: if price breaks 10 it will likely test 20, if break 20 likely test 50, and so on.
There for you can trade "from band to band"

One possible way to trade with it:
Best entrys are when the ma's are first crossing over the 200 and expanding or after a period of the averages compressing(and beginning to expand.) You might want to hold the position outright until a pair of the MAs cross(i like 10/20) or you can scale out position as trend extends.

This is just one example.

Another is continuation style trend strategy where you confirm the MAs are stacked in order but price is under the some of the stack, to which price "clears" the moving averages and is ready to continue trend.

You can also convert this to a signal or set of signals.
For example you might measure the spread of several MA pairs.
Pairs: 10/20 , 20/50, 50/100, 100/200

This produces a full scope of how the asset is trending over different time horizons.
*Note the longer span of each pair is used as the shorter span in next pair.
You could combine them into one signal or keep separate.

## VWAP

Can be used for mean reverting or trending as determined by the VWAPs slope.

Trying to mean revert a strongly trending asset is how you get blown out.

Conversly if VWAP slope is low trend trading gets chopped.


Often paired with PX for proximity of price to vwap but not strictly required.

Can be used as input to Moving Average cross
example ema spread [vwap,ema(200)]

## VFTI (Volume Flow Trend Indicator)

Combines volume and price into one signal.

Used to detect the trend of volume flow.

Volume Flow can be confirming or rebuking price direction.

Example , price is grinding around the highs but VFTI starts turning negative. dispite price not going down, the volume is signaling the underlying directional flow of the participants.

Hard to hide volume. The intentions show themselves.

VFTI is very much a leading indicator of price movement. *should be verified*

## PX (Price Extension)

PX measures the distance of price from another indicator, usually moving average but could be level based.

Returns raw $ amount for trade specifics and percent based for normalizing/modeling, and stat(std, mean, ect)

We call it PX but this is not really a novel concept, it is very useful and versatile though.

Can be used with trend or mean reverting strategies.

For trend, you might use the std dev of the px for levels to book profits.
Mean reversion might use the same band for entry.

Equally important, so to make it explicit, PX is often used for sizing.

If trend trading you want to be increasing position closer to the Moving average, and distributing it away from MA.
Logically it stands to say you would do the opposite for mean reverting, and reducing as it approches the MA.

Can be used in conjunction with multiple moving averages to get a better picture of landscape.

For example measure PX_EMA(10) & PX_EMA(200) will tell you prices relationship to both indicators.
Price might be Over the 200 but under the 10 , or obviously any combination of that.

## SLOPE

Linear Regression Slope. Another classic.

Indicator itself doesnt need much explanation, and fairly easy to interpret.

Can measure slope of price directly, slope of indicator, or slope of signal. (possibly more?)

I'd add its important for getting you on the right side of the trade.

Often used as as filter for trend/mean_revert.

Can use r2 as filter for periods of low correlation of sig<>price. Inverely said take trades with high r2.

## RSI (normalized to 1,-1)

Classic. Transformed to [1,-1] signal space instead of traditional [0,100]

The underlying math of RSI is fundamentally sound measurment of price action, very high correlations.

Simple interpretation is under over zero bullish and under zero bearish.

Can trend trade it from 0 outwards.

You can also fade the extremes, if staticly measured, [0.9,-0.9] is recommended extremes. Otherwise use dynamic stats from signal such as std dev.

If fading extremes, usually best to wait until its leaving the extreme.

Things can stay "overbought/oversold" in trend environment for a while.

## ROC

Universal measurement of speed in physics. 

## PRI / PRL / PRZ/ PRB

Price Reversal Indicator. Price Reversal Levels. Price Reversal Zone. Price Reversal Breaker.

Combined they form a Price Reversal System that can be used as a discretionary or signalized.

The core concept attempts to capture whether buyers or sellers are control of price action. 

It determines this by looking at the current candles close compared to the previous candles range. 

Bullish PRI:

previous candle was bearish (sellers had the bar)
current candle is bullish (buyers took it back)
current close is above the previous high
Bearish PRI:

previous candle was bullish
current candle is bearish
current close is below the previous low
That third condition is the important one. Color flip alone is noise. Closing through the previous high/low is the reclaim — buyers (or sellers) didnt just paint a green/red candle, they took out the prior bars range.


PRL (Price Reversal Levels)

When PRI fires, the signal candle leaves levels that matter: typically the open and the extreme (low on bullish PRI, high on bearish PRI). Those become the Price Reversal Levels — places price often retests.

PRZ (Price Reversal Zone)
The OLHC levels form the Price Reversal Zone.
Generally considered a safe place to absorb inventory in the direction of whos in control. 
Conversly, if you think the party in control is going to be tested, you might target this zone as weakness or place to take profit.

PRB (Price Reversal Breaker)
If price later breaks the PRL the signal direction is invalidated and the reverse implication is true. 

System Notes:
Can be used as entry trigger, reversal, or continuation signal.
Can be used as sole input to a strategy or in combination with other signals.

There are typically two reaction types from an event firing, immediate follow through in the direction of the print, or a delayed reaction in which the control party is tested. 



## Volume Ratio

Volume Ratio measures current bar volume relative to its recent baseline:

`current volume / EMA(volume, window)`

It is expressed as a multiple. A reading of 1 means current volume is equal to its EMA baseline, 2 means twice the baseline, and 0.5 means half the baseline.

The full range is useful. Low ratios identify periods of low participation or quiet trade, while rising and elevated ratios show increasing participation and can confirm that price is accelerating. The ratio is not inherently directional and should be interpreted alongside price direction, candle structure, and location within the recent range.

The rolling standard deviation of the ratio adds regime information. Compression indicates that relative volume is behaving consistently; expansion indicates a widening distribution of participation and can identify a changing or unstable regime.

### Volume anomalies

Extreme high ratios are a special case of the broader feature. Readings around 2–3 have often accompanied price acceleration, while readings around 4 or higher have often appeared near tops and bottoms. These thresholds are heuristics and should be evaluated by asset and timeframe.

A high-ratio candle near a rolling-window high or low is more likely to mark exhaustion or reversal; one in the middle of the range may instead act as an accelerant. The intuition behind an extreme print is that participants may have committed and exhausted much of the capital available for that period.

At extreme readings, the usual guidance is to shrink or close the position regardless of direction. The anomaly candle's OHLC should be retained as important levels that price may later retest.

## ATR Ratio

ATR Ratio measures current ATR relative to its recent baseline:

`current ATR / EMA(ATR, window)`

It is expressed as a multiple. A reading of 1 means current ATR is equal to its EMA baseline, 2 means twice the baseline, and 0.5 means half the baseline.

The full range is useful. Low ratios identify range and volatility compression; high ratios identify range expansion. Neither state is inherently directional, but each changes the expected movement, risk, sizing, and execution environment.

The rolling standard deviation of the ratio adds regime information. Compression indicates a stable volatility regime, while expansion indicates that realized range is becoming less consistent and may signal a regime transition.

### ATR anomalies

Extreme high ratios are a special case of the broader feature: something unusually large just happened. Readings around 4 or higher are useful candidate triggers, but the threshold should be evaluated by asset and timeframe.

These events often occur near reversal points, and price frequently retraces part or all of the move. The usual guidance is to reduce position size or close, then re-enter at a better price if the trend remains intact.

The anomaly candle's OHLC should be retained as important levels that price may later retest.

## Volume Delta Anomaly

Observed when the CVD of a candle is opposite the direction.

Example the candle is an up green candle but the cumulative volume delta had more selling flow then buying.
This can be used as a reversal signal to take profit or flip direction, or an accelerant signal if in your positions favor.

## Trade Speed

Speed kills. Measure it.

Measurement is number of trades per bar. Is provided naturally from Hyperliquid via candle websocket. Otherwise would need to sub 'trades' ws on other exchanges and cummulate them.

Often find volume tracks with trade speed but not always.

For example, a counter party may place a single 100K order.

If you measure candles total volume it will show up, if you watch for trades over X USD amount it will show, but trade speed counts as one.
Conversely, the counter party may break the 100K order into smaller chunks as to avoid detection. This will show up in trade speed.

Not the end all be all but useful for seeing under the hood of whats going on.

Can use as signal direct or as anamoly detection.

Speed is an important part of physics for determing an objects energy and motion. (e = mc2)
You need a way to measure speed, this is one of them.

Additional use: may want to use as a knob for determining trade urgency for entry/exits, and avoiding adverse selection if you know price is likely to move away from you.

## Absorption (WIP)

Measured by amount of candle body that is a wick.
Used to detect reversals
At minimum should reduce position if on correct side.

## Candle Strength Indicator (WIP)

Attempts to measure stregtch of a candle by a composite of factors.
Core input is proximity of close to high/low respective of candle direction.

## Order Book Imbalance

Name says what it is.

Retail generally is not the ones setting limit orders and quoting the book, market makers are.
OB imbalance displays intentions of accumulating or distributing inventory.

## Combined Signal

VFTI + PX(RVWAP) + SLOPE(RVWAP) + RSI + roc  = sig_current
Add orderbook inbalance to combo = sig_v2

## Multi Time Frames (MTF)

Indicators and signals of one timeframe have effects and can explain activity on other timeframes. 

Example: The 200 day moving average projected down to 1 hour timeframe, you can observe price reacting to the 200 day MA as support resistence directly. 

Example2: Compositing. Consider the same example again. IF price is under the 200 Day Ma && over the 1H 200 ma, you can start to compose a multitime frame view of the market. 


## EMA MAXI

Combines moving averages of different timeframes to form a composite view of the market on a specific timeframe.

Current daytrading setup on 5m timeframe:
- 200 ema 1D
- 200 ema 4H
- 10 ema_low 4H
- 10 ema_high 4H
- 200 ema 5M

## MTF Ribbon

Building on the Ma ribbon and MTF concept, I propose using the 200 ema of various timeframes to form a lower timeframe ribbon, and then trading band to band as support and resistence.

## Volatility Scores

Many ways to slice and dice vol.

Would recommend starting with an industry standard of volatility measuring std dev and add your own flavors in addition.
The standard sanity checks you, but there is genuine alpha in measuring it in unique ways.

Some ways include blended vol, ratio-vol,

examples:
Blended vol = (vol(365) * 0.3) + (vol(30)* 0.3) + (vol(3) * 0.4)
Ratio vol = vol(3) / vol(30)

Normal std and blended std are useful for measuring how volatile the asset is in general when comparing to other assets and ratio is good for "how volatile is it right now compared to normal". Two different things.

## Funding Rates

The Market is sometimes wrong, but not for long.

Example: If the funding rate is negative and you are long, you should consider what other participants know that you dont.
Funding is a mechanism for exchange positions, it directly reflects how people are positioned.

Being on the opposite side of funding rate is not inherently a bad thing, but you should ask why.

Often I find being on the side of funding rate (and paying it) is more accurate for estimating a positions direction.

Can be used as a reversal signal when it changes signs.

Example people selling the top or buying the bottom, the rate will change before the price does.

I seen a nice formula (that i forget) but it effectively stated:
Price needs to move in the direction of the funding, per time schedule of the funding rate, or it is -EV to hold.

Sounds obvious but what does it really mean.

Market participants are generally rational. If they are willing to pay n% per hour to hold a position, they expect over a window of time, the position will move more then that. It has to or they will close it eventually. (and that closing is reflected in the funding rate).

Said another way: The funding rate reflects the positioning of participants directly, and price must move according to the rate, or else participants will reposition until the rate reflects the opportunity.

## Future Indi/Sig

- POC_MA (Point Of control MA)
- POC_BREAKER
- ATR Breaker

## Scaling In and Scaling Out(WIP)


Scaling in and out of positions reduces price path dependence for profitablity and risk. 
It transforms timing risk into directional risk. 

*(section body not yet written)*

See [[research/trading/positioning/size-distribution|Size Distribution]] for the elicited signal→position skew concept (size mass along the signal path; not quote spacing).

## Trading Styles

- Pop it , dunk it. -> Entry triggers full position, exit position trigger closes fully.
- 123 -> market enter a position in thirds. Second and third buys are used to cost average the positon , with the requirement that the position is in the money before fully allocating. if your wrong, youre only 2/3ds wrong.
- Smash n Scale -> enter chunk of position with market order and put up for sale with a spread of limit orders
- Buy n Bid -> enter position with between 10-30% of intended target via market, place limits down to price target to accumulate. Keep lifting limits as candles progress and replaceing orders down to the updated target.
- Ride the Wave -> Quote both sides of book with a limit order grid. Inventory is ONLY in direction of the trend.
Effectively states If asset is trending THEN im willing to absorb favorable inventory and will distribute the inventory away from the mean of the trend.
- Opposite Only -> IF trend is determined THEN buy ONLY on opposite candles of trend AND sell IF in the money AND candle is in trend direction.
