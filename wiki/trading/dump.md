This is a work in progress brain dump of things I do manually trading and concept ive learned over the years. 

>>>>>
Trends can be defined as higher highs or lower lows.

Therefor it makes sense to measure the highs and the lows of the asset. 

When measured and plotted at the same time it forms a channel, known as the High Low Channel or HL_Channel for short.

HL Channel

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

>>>
*Note: we generally use Exponential moving average for many calculations with exception of vwap. Not a hard rule but when in doubt use EMA.*
>>

200 EMA

Well know and widely used. simple and effective. 
Good starting point on getting positioned on the right side of market.
Often used in combination with others.

>>>
Moving Average Crossing
The main Moving averages preffered are the 10 and 200 periods combined, as together they enable you to answer several important questions. 

Where is the long term and short term trends? Is the trend just starting? How extended is it? Is it expanding or contracting.

We chose the 10 Ema as the short term indicator as it is snappy enough to capture the beginning portion of the trend, while not being overly sensitive to price fluctions around the longer term trend. 

The 10 EMA is also fast enough to detect when the expansion portion of the trend is done and contraction is begining, without giving back too much profit. 

It should be said that in practice I use the 10 EMA LOW(see channel) as the short term indi, with reasoning that close prices often chop near the long term trend(200) and by using the LOWs (or highs) you get cleaner verification that price is trending in the cross overs direction. 

Note: The Ema crossing is often used to frame the opportunity set, but seldom used alone without measuring where the price is in relationship to the moving averages. For that we use PX(Price Extension). More on that later. 
>>>
MA Ribbon
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

>>>>
VWAP

>>>
VFTI
>>>
PX
>>>
SLOPE
>>>
RSI(normalized to 1,-1)
>>>
PRI
PRL
PRB
Combined PR system. Discretionary. Signalized
Measure forward returns of PRI and PRB
>>>>
Volume Anomalies
>>>>>
ATR Anomalies
>>>
Volume Delta Anomaly
>>>
Absorbtion
>>>>
Order Book Imbalance
>>>
Combined signal
VFTI + PX(RVWAP) + SLOPE(RVWAP) + RSI = sig_current
Add orderbook 

>>>
Multi time Frames
>>>>

Scaling in and scaling out

>>>
Scaling part two



>>>
Trading Styles:
Smash n Scale -> enter chunk of position with market order and put up for sale with a spread of limit orders
Buy n Bid -> enter position with between 10-30% of intended target via market, place limits down to target to accumulate. Keep lifting limits as candles progres and replaceing orders down to the updated target. 
Opposite Only -> IF trend is determined THEN buy ONLY on opposite candles of trend AND sell IF in the money AND candle is in trend direction. 
Ride the Wave -> Quote both sides of book with a limit order grid. Inventory is ONLY in direction of the trend. 
Effectively states If asset is trending THEN im willing to absorb favorable inventory and will distribute the inventory away from the mean of the trend. 

>>>
Top K Bottom K
>>> 
Types of Sytematic trading

Conditional IF THEN / Match case

Signal -> Position
Signal -> Condition -> Position

Signal -> Model -> Prediction -> Condition -> Position



>>>
Research Directions
- Model Pipelining
- TradeView Scraping
- Image based model trading
- LFM (Large Financial Models)[as opposed to LLM large language models]


>>>.
MAX_P concept
>>>
Half Life of Mean Reversion
>>>
Optimal Trend Testing(OLS)
>>>
CPO - Conditional Parameter Optimization