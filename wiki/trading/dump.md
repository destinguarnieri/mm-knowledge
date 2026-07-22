This is a work in progress brain dump of things I do manually trading and concepts Ive learned over the years. 

>>>>>
Trends can be defined as higher highs or lower lows.

Therefor it makes sense to measure the highs and the lows of the asset. 

When measured and plotted at the same time it forms a channel, known as the High Low Channel or HL_Channel for short.

*HL Channel*

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

*200 EMA*

Well know and widely used. simple and effective. 
Good starting point on getting positioned on the right side of market.
Often used in combination with others.

>>>
*Moving Average Crossing*
The main Moving averages preffered are the 10 and 200 periods combined, as together they enable you to answer several important questions. 

Where is the long term and short term trends? Is the trend just starting? How extended is it? Is it expanding or contracting.

We chose the 10 Ema as the short term indicator as it is snappy enough to capture the beginning portion of the trend, while not being overly sensitive to price fluctions around the longer term trend. 

The 10 EMA is also fast enough to detect when the expansion portion of the trend is done and contraction is begining, without giving back too much profit. 

It should be said that in practice I use the 10 EMA LOW(see channel) as the short term indi, with reasoning that close prices often chop near the long term trend(200) and by using the LOWs (or highs) you get cleaner verification that price is trending in the cross overs direction. 

Note: The Ema crossing is often used to frame the opportunity set, but seldom used alone without measuring where the price is in relationship to the moving averages. For that we use PX(Price Extension). More on that later. 
>>>
*MA Ribbon*
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

>>>>
*VWAP*

Can be used for mean reverting or trending as determined by the VWAPs slope.

Trying to mean revert a strongly trending asset is how you get blown out. 

Conversly if VWAP slope is low trend trading gets chopped.

Therfor if slope is under threshold_1 you want to be mean reverting it. 
If slope over threshold_2 you can trend trade it. 

Often paired with PX for proximity of price to vwap but not strictly required. 

Can be used as input to Moving Average cross
example ema spread [vwap,ema(200)]

>>>
*VFTI(Volume Flow Trend Indicator)*

Combines volume and price into one signal.

Used to detect the trend of volume flow. 

Volume Flow can be confirming or rebuking price direction.

Example , price is grinding around the highs but VFTI starts turning negative. dispite price not going down, the volume is signaling the underlying directional flow of the participants. 

Hard to hide volume. The intentions show themselves.

VFTI is very much a leading indicator of price movement. 


>>>
*PX(Price Extension)*
PX measures the distance of price from another indicator, usually moving average but could be level based. 

Returns raw $ amount for trade specifics and percent based for normalizing/modeling, and stat(std, mean, ect)

We call it PX but this is not really a novel concept, it is very useful and versatile though.

Can be used with trend or mean reverting strategies.

For trend, you might use the std dev of the px for levels to book profits. 
Mean reversion might use the same band for entry. 

Equally important, so to make it explicit, PX is often used for sizing.**

If trend trading you want to be increasing position closer to the Moving average, and distributing it away from MA. 
Logically it stands to say you would do the opposite for mean reverting, and reducing as it approches the MA. 

Can be used in conjunction with multiple moving averages to get a better picture of landscape.

For example measure PX_EMA(10) & PX_EMA(200) will tell you prices relationship to both indicators. 
Price might be Over the 200 but under the 10 , or obviously any combination of that.

>>>
*SLOPE*

Linear Regression Slope. Another classic , nothing too fancy.

Indicator itself doesnt need much explanation, and fairly easy to interpret.

Can measure slope of price directly, slope of indicator, or slope of signal. (possibly more?)

I'd add its important for getting you on the right side of the trade. 

Often used as as filter for trend/mean_revert.

Can use r2 as filter for periods of low correlation of sig<>price. Inverely said take trades with high r2.


>>>
*RSI(normalized to 1,-1)*
Classic. Transformed to [1,-1] signal space instead of traditional [0,100]

The underlying math of RSI is fundamentally sound measurment of price action, very high correlations. 

Simple interpretation is under over zero bullish and under zero bearish. 

Can trend trade it from 0 outwards. 

You can also fade the extremes, if staticly measured, [0.9,-0.9] is recommended extremes. Otherwise use dynamic stats from signal such as std dev.

If fading extremes, usually best to wait until its leaving the extreme. 

Things can stay "overbought/oversold" in trend environment for a while. 


>>>
*ROC*
>>>
PRI
PRL
PRB
Combined PR system. Discretionary vs Signalized.
Measure forward returns of PRI and PRB
>>>>
*Volume Anomalies*

Meassured by taking the ema Volume of a window and calculating the multiple of current volume(1) / avg. 
Expressed in multiples (1,2.5,3,4.24,5, ect)
2-3 often indicate price is accelerating in direction of volume
+4 is often negative signal. 
+4 generally occurs at tops and bottoms.

From a logical perspective , when a 4+ occurs the participants capital is used up for that current time period.
They are exhuberant and exhausted. 

Can be interpretted as reversal or accellerant , often using where in the range it occurred.

for example if it happenned near the rolling window low or rolling high it is likely a reversal. 
In the middle of the range likely an accelerant. 

Advice on +4 is usually shrink position regardless or close. 

The candles OHLC should be noted as important levels that are often retested.

>>>>>
*ATR Anomalies*

Meassured by taking the ema ATR of a window and calculating the multiple of current atr(1) / avg. 
Expressed in multiples (1,2.5,3,4.24,5, ect)
All are useful but readings of +4 are the triggers

Interpretation is quite simple: Something big just happened.

Should reduce position size or close position.
Price often retraces part of or all of the move. 
Can generally just rebuy your position at a better price if determined the trend is still intact.

The candles OHLC should be noted as important levels that are often retested.

Often these Triggers are at reversal points hence the guidance that its generally EV to shrink or close.

>>>
*Volume Delta Anomaly*

Observed when the CVD of a candle is opposite the direction.

Example the candle is an up green candle but the cumulative volume delta had more selling flow then buying.
This can be used as a reversal signal to take profit or flip direction, or an accelerant signal if in your positions favor. 



>>>
*Trade Speed*
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



>>>
*Absorbtion*

Measured by percent of candle body that is a wick.
Used to detect reversals
At minimum should reduce position if on correct side. 

>>>>
*Candle Stregnth Indicator (WIP)*
>>>>>
*Order Book Imbalance*
Name says what it is. 

Retail generally is not the ones setting limit orders and quoting the book, market makers are. 
OB imbalance displays intentions of accumulating or distributing inventory. 

>>>
*Combined signal*

VFTI + PX(RVWAP) + SLOPE(RVWAP) + RSI = sig_current
Add orderbook and roc to combo = sig_v2

>>>
*Multi Time Frames(MTF)*
>>>>
*EMA MAXI*
>>>>
*Volatility Scores*
Many ways to slice and dice vol. 

Would recommend starting with an industry standard of volatility measuring std dev and add your own flavors in addition. 
The standard sanity checks you, but there is genuine alpha in measuring it in unique ways. 

Some ways include blended vol, ratio-vol, 

examples:
Blended vol = (vol(365) * 0.3) + (vol(30)* 0.3) + (vol(3) * 0.4)
Ratio vol = vol(3) / vol(30)

Normal std and blended std are useful for measuring how volatile the asset is in general when comparing to other assets and ratio is good for "how volatile is it right now compared to normal". Two different things.

>>>
*Funding Rates*
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

>>>
*Future Indi/Sig:*
- POC_MA (Point Of control MA)
- POC_BREAKER 
- ATR Breaker

>>>
*Scaling in and scaling out*

>>>
*Scaling part two*

>>>
*Trading Styles:*
- Pop it , dunk it. -> Entry triggers full position, exit position trigger closes fully.
-123 -> market enter a position in thirds. Second and third buys are used to cost average the positon , with the requirement that the position is in the money before fully allocating. if your wrong, youre only 2/3ds wrong. 
-Smash n Scale -> enter chunk of position with market order and put up for sale with a spread of limit orders
-Buy n Bid -> enter position with between 10-30% of intended target via market, place limits down to price target to accumulate. Keep lifting limits as candles progress and replaceing orders down to the updated target. 
-Ride the Wave -> Quote both sides of book with a limit order grid. Inventory is ONLY in direction of the trend. 
Effectively states If asset is trending THEN im willing to absorb favorable inventory and will distribute the inventory away from the mean of the trend. 
-Opposite Only -> IF trend is determined THEN buy ONLY on opposite candles of trend AND sell IF in the money AND candle is in trend direction. 

>>>
*Top K Bottom K*
>>> 
*Types of Sytematic trading*

- Conditional Only (IF THEN / Match case)
- Signal -> Position
- Signal -> Condition -> Position
- Signal -> Model -> Prediction -> Condition -> Position



>>>
*Research Directions*
- Explore intial Model set
- Model Pipelining
- TradeView Scraping
- Image based model trading
- LFM (Large Financial Models)[as opposed to LLM large language models]


>>>>
*A Portfolio of strategies*
Key Principle: Strategies can disagree and both make money.
Stay flexible
>>>
*SubAccounts*

In crypto there is concept of subaccounts on exchanges that are NOT cross collateralized and ABSOLUTELY can hold the same universe of assets in arbitrary combinations or directions. 

This is the mechanism which enpowers the portfolio of strategies. 


>>>
*Margin: Cross and Isolated Semantics*
Each position in a sub account can be either Cross Margined or Isolated.

Across the portfolio this enables maximum isolation , maximal capital efficiency, or likely a balance between the extremes.

>>>
*Crypto Forever?*
No. We have goals to accomplish here then stand up tradfi operations. 

Speaking of goals

>>
*BUSINESS GOALS:*
1: Become 1% of volume across all Hyperliquid assets
2: Scale exchange infra to top 10 crypto exchanges
3: Become 1% of volume of top 10 Exchanges
4: Stand Up tradfi infra
4: TRAD KPI_1:: Have a presence on all quoted stocks over 1B MCAP and Futures
5: TRAD KPI_2:: Become 1% of daily US volume
6: TRAD_KPI_3:: Scale international infra
...you guessed it
7: TRAD_KPI_4:: Become 1% of globel daily volume.

**IT SHOULD BE STRONGLY NOTED THAT VOLUME IS IMPLICITLY PROFITABLE. VOLUME ALONE IS OBVIOUSLY NOT THE METRIC**

>>>
*MAX_P Concept*

>>
*Half Life of Mean Reversion*

>>
*Optimal Trend Testing(OLS)*

*CPO - Conditional Parameter Optimization*

*The Physics of Markets*

It helps to think of markets from first princlples of physics.
Unless the market somehow operates outside the law of physics(it doesnt) then the law of physics applies to it. 

Mass, velocity, trajectory, gravity, electical charges, not limited to, are all directly relatble to markets and the core math concepts can be applied. 

I propose there is a gravitational force of an object to the mean. 
The object and the mean are charged entities.

