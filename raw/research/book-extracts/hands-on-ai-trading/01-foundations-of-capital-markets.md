---
title: "Foundations of Capital Markets"
chapter: 1
source: "Hands-On AI Trading with Python, QuantConnect, and AWS"
source_file: "/Users/destinguarnieri/Desktop/Hands-On AI Trading with Python QuantConnect and AWS.epub/OPS/c001.xhtml"
status: "extracted"
---

# Chapter 1: Foundations of Capital Markets

## Overview

This chapter supplies the market-structure vocabulary and QuantConnect representations used by the rest of the book. It explains how US orders and prices flow through public exchanges, market makers, and private venues; how limit-order books match liquidity; how market data becomes ticks and bars; how brokers and transaction costs alter realized performance; how durable security identifiers prevent corporate-action errors; and how QuantConnect represents equities, options, index options, futures, and cryptocurrencies. The recurring practical lesson is that an algorithm must model the market as it actually trades—not as an idealized sequence of last-sale prices. Source: pp. 3–24.

## Learning Objectives (Inferred)

- Explain NBBO formation and the relationship among exchanges, the SIP, market makers, TRF, DMA, and private alternative trading systems. Source: pp. 3–4.
- Distinguish limit and market orders, describe book walking, and identify liquidity, market-making, and informed-trading roles. Source: pp. 4–7.
- Work with trade ticks, quote ticks, trade bars, quote bars, and alternative/custom data in QuantConnect. Source: pp. 7–10.
- Model brokerage constraints, fees, spread crossing, slippage, and market impact. Source: pp. 10–13.
- Track an economic asset across ticker and corporate changes with persistent identifiers. Source: pp. 13–15.
- Represent and trade the principal asset classes used later in the book while respecting their settlement, normalization, expiry, and venue-specific behavior. Source: pp. 15–24.

## Key Concepts

### Market Mechanics

The United States has 11 major stock exchanges; NYSE and NASDAQ are the largest. Public exchange trades and quotes are consolidated by the Securities Information Processor (SIP). The SEC uses this feed to determine the National Best Bid or Offer (NBBO), the best publicly posted national prices. In the chapter's description, a quote must cover more than 100 shares to establish a better NBBO; sub-100-share **odd lots** are excluded. Source: p. 3.

Retail brokers often route orders to market makers for off-exchange execution. Such fills must remain within the NBBO range, are reported to the Trade Reporting Facility (TRF), and later enter SIP data. Direct Market Access (DMA) instead lets an order target a particular exchange, but a chosen venue need not have the best national price. Institutional flow may transact through private alternative trading systems (ATSs), while public venues establish the NBBO. Source: pp. 3–4.

### Market Participants

#### Trading Is the “Play”

The chapter frames algorithmic trading as coordinated and scripted: the market venue and order book are the stage, trading rules govern interactions, and participants occupy roles that may change over time. Source: p. 4.

#### The Limit Order Book

A **limit order book** is a price-and-size ledger. Bids state willingness to buy; asks state willingness to sell. Equity size is commonly expressed in round lots of 100 shares, while options and futures use contracts. Prices are ordered so the best bid and best ask meet at the inside market. A persistent crossed book cannot remain: compatible orders execute. Source: pp. 4–5.

A buy limit priced at or above the best ask behaves like a marketable order. It consumes the best ask and, if necessary, successively higher asks until filled or until the remaining price limit prevents further execution. This is **walking the book**. A sell order works symmetrically through progressively lower bids. Passive limit orders usually rest below the best ask (buys) or above the best bid (sells), trading immediacy for price control and accepting possible non-fill. Market orders prioritize immediate execution in a sufficiently liquid market but accept the available book prices. Large orders relative to displayed depth walk farther and create adverse price impact. Source: pp. 4–5.

#### Roles: Liquidity Trader, Market Maker, and Informed Trader

A trader can play several roles, even simultaneously. A **liquidity trader** seeks to enter or exit for reasons other than privileged information. This includes benchmark rebalancers, public-information fundamental investors, and undisciplined “noise” traders. Their common feature is the absence of an informational advantage. Source: p. 5.

A broker may internally cross or net opposite client orders, often around the midpoint of the best bid and ask. Otherwise, a liquidity-seeking market order hits the bid (sell) or lifts the offer (buy); resting limit orders supply the liquidity, and exchanges may rebate filled limit orders. Source: pp. 5–6.

A **market maker** improves price or immediacy by standing ready to transact, often placing quotes inside an overly wide spread. Its prospective gross compensation is the spread between buying at a bid and selling at a higher ask. Floor specialists historically performed this function; modern market making is predominantly algorithmic and high-frequency. Any strategy can effectively make a market if it supplies liquidity and improves outcomes, intentionally or not. Source: p. 6.

An **informed trader** possesses nonpublic information known to few agents, not merely superior skill or a distinctive public-information forecast. Information about a pending market-moving block trade also qualifies; trading ahead of it is illegal **front-running**. Informed traders impose adverse-selection risk because counterparties cannot reliably identify them. Speed alone does not defeat a genuine information advantage, so market makers must price and manage this risk. Source: pp. 6–7.

#### AI Actors Wanted

Market activity generates terabytes of data that humans cannot inspect or react to quickly enough. The proposed AI role is to identify activity patterns that may reveal informed flow or other tradable signals, then react at machine speed. Source: p. 7.

### Data and Data Feeds

Every bid, ask, or trade is a market event. Event volume commonly falls around lunch and rises near 3 p.m.; opening and closing volume can be two to three times midday volume. Historical “ticker tape” language comes from recording these events on paper. QuantConnect's `self.time` is the algorithm time in both backtesting and live trading. Source: p. 7.

A **point-in-time dataset** preserves what the feed showed at the moment of capture, including connectivity and exchange errors. Trades are supposed to be reported within 90 seconds, but late reports can appear at stale prices and resemble discontinuities. Researchers must identify/filter them without silently importing future knowledge. Source: pp. 7–8.

The May 6, 2010 Flash Crash began around 2:30 p.m. and lasted about 35 minutes; algorithmic trading exacerbated the decline. Exchanges later introduced curbs/circuit breakers and sometimes retroactively canceled extremely low-priced trades. Because cancellation occurs minutes or hours later, a point-in-time strategy cannot know it at execution time. Source: p. 8.

Primary market-data forms are:

- **Trade tick:** a filled-order sales report, with flags such as venue or reporting delay.
- **Quote tick:** an offer to buy or sell a stated quantity at a stated price. The highest bid and lowest ask form the spread; US national best quotes form NBBO and are specially flagged.
- **Consolidated data:** tick streams aggregated into fixed-interval bars to reduce billions of events and make research tractable. A trade bar summarizes sale-price OHLC and volume. A quote bar contains separate bid and ask OHLC child bars and a midpoint representation. QuantConnect prefers quote data for fill modeling because it represents executable prices better than a previous trade. Source: pp. 8–9.

In an `on_data(self, slice)` event, tick lists are available from `slice.ticks`; `tick.tick_type` distinguishes trade from quote. Trade and quote bars are available from `slice.bars` and `slice.quote_bars`; the latter exposes values such as `quote_bar.bid.close` and `quote_bar.ask.close`. Source: pp. 8–9.

#### Custom and Alternative Data

**Alternative data** includes imagery, real estate, weather, shipping, regulatory data, geolocation, reviews, sentiment, and transaction/customer tracking. QuantConnect-hosted sources can be attached with `add_data`; the chapter pairs Apple equity data with `TiingoNews`. If a hosted source is unavailable, a user-defined data class can describe fields and parse a source such as CSV, then be registered with `add_data(MyFactorDataset, "Factors")`. Converting alternative data into a tradable signal remains a substantive analytical task. Source: pp. 9–10.

### Brokerages and Transaction Costs

Brokers custody assets, intermediate access, clear exchange trades (often through clearing firms), and enforce SEC/FINRA margin limits. Brokerages differ in supported assets, fees, order types, routing, and update/cancel capabilities. They may sell/direct order flow to market makers for rebates or internally net client orders, but internal fills must be within public NBBO. Source: pp. 10–11.

QuantConnect implements 12 order types. Examples are `market_on_open_order`, intended for the opening auction, and `stop_market_order`, which submits a market order once a stop price is reached. Brokerage support is not universal. Every QuantConnect order returns an **order ticket**, the handle for updating or canceling an unfilled order and receiving order feedback. Source: p. 11.

#### Transaction Costs

Transaction costs include explicit brokerage fees and taxes plus implicit costs generated by trading itself. Research should model both so an apparently profitable strategy does not fail live. Source: p. 11.

**Trading fees.** Brokers may charge per order or share. QuantConnect can attach a security-level fee model (for example, a constant $1 fee) or a brokerage model that jointly enforces a broker's costs and limitations. Source: pp. 11–12.

**Bid-ask spread.** A market buy fills at the ask and a market sell at the bid. The last sale may be at either side or between them, so assuming the last price is an executable fill is optimistic. QuantConnect uses quote data to incorporate the spread, while a fill-model plugin can customize behavior. Source: p. 12.

**Slippage.** Slippage is the difference between expected and final execution prices. For small orders in liquid assets, price movement during execution is the common cause. For large orders or illiquid assets, consuming multiple depth levels causes temporary or permanent impact. Liquid-market makers may replenish near the pre-trade price (temporary impact); suspected informed flow may cause them to replenish near the new, worse price (permanent impact). Splitting orders may mitigate temporary impact, while anticipated permanent impact calls for execution logic that obscures total size. QuantConnect defaults toward liquidity assumptions but offers `NullSlippageModel` (instant top-of-book fill) and `MarketImpactSlippageModel`. Source: pp. 12–13.

### Security Identifiers

Stable identity is essential because ticker renames, mergers, and delistings can otherwise corrupt historical portfolios. Common systems include CUSIP (US/Canada, eight alphanumeric characters plus optional check digit), FIGI (Bloomberg's free proprietary lookup), and ISIN (for many US/Canadian assets, a country code combined with the CUSIP). Their limitations include licensing cost/restrictions, dependence on separate lookup databases, and incomplete asset/country coverage. Source: pp. 13–14.

QuantConnect's open-source **Symbol** encodes the data needed to fingerprint an asset, eliminating a lookup database and licensing fee. It supports up to 99 asset classes in 255 countries and derivatives. The durable object remains constant through ticker changes and mergers. Its `id` can be serialized for JSON or storage; an example is `SPY R735QTJ8XC9X`. The encoding contains the IPO ticker, security type, a date, option strike/right, and listing market. The `market` field distinguishes identically spelled tickers on different venues, such as BTCUSD on Coinbase versus Kraken. Source: pp. 14–15.

Google's 2014 share restructuring illustrates why ticker text is not identity: temporary GOOCV/GOOAV tickers facilitated the Class C issue; the original Class A ticker changed to GOOGL while GOOCV became GOOG. A persistent Symbol follows the economic asset across the rename. Source: p. 14.

### Assets and Derivatives

QuantConnect calls assets **securities** and stores them in a central collection. Shared attributes include hours, margin, P&L accounting, and contract multipliers. A security exposes current price, Symbol, and holdings quantity. Liquid markets with maintained point-in-time data are easiest to model; much of QuantConnect's price data is supplied by Algoseek. Source: p. 15.

#### US Equities

The chapter characterizes the US equity market as the world's largest and most liquid, roughly half of global capitalization with about 9,000 listed companies. **Corporate actions** include IPOs, dividends, splits/reverse splits, mergers, and acquisitions and can materially affect value and data. **Fundamental data** comes from financial statements and forecasts; providers may harmonize fields across accounting conventions. Ratios enable cross-company comparisons and later become machine-learning features. Source: pp. 15–16.

QuantConnect can screen a fundamental universe, for example selecting companies with `valuation_ratios.pe_ratio < 10`. Ratios introduced are PE (close price / earnings per share), revenue growth (percentage revenue change), free-cash-flow percent (free cash flow / operating cash flow), and dividend payout ratio (dividends / net earnings). Source: p. 16.

##### US Equity Corporate Events

- **Splits/reverse splits:** a split increases share count and proportionally reduces unit price without changing total investment value at the event. It can improve accessibility/liquidity. A reverse split consolidates shares and increases unit price, potentially helping remain above an exchange's listing threshold (the chapter gives $1). QuantConnect exposes split events through `on_splits` and `slice.splits`. Discontinuous raw prices require resetting price-continuity-dependent indicators. Source: pp. 16–17.
- **Dividends:** usually quarterly but governed by company decisions, quoted per share, and credited as cash. They appear in `slice.dividends` or `on_dividends`; split/dividend histories support yield calculation and trend forecasting. Source: pp. 17–18.
- **Data normalization:** adjusted histories alter past prices to incorporate splits/dividends smoothly. This simplifies research but has unresolved methodological issues. `RAW` leaves prices unadjusted and credits dividends in cash; `ADJUSTED` adjusts for both splits and dividends; `SPLIT_ADJUSTED` adjusts splits only and pays dividends as cash. Raw mode supports more realistic portfolio accounting and user-controlled reinvestment. Source: p. 18.
- **Security changes:** IPOs add securities; renames emit old/new ticker events but do not require replacing the persistent Symbol; acquisitions can delist the target; mergers may combine delisting and rename; delistings appear both in a dedicated handler and as removed securities. These events preserve portfolio continuity even if they do not themselves represent an economic price move. Source: pp. 18–19.

#### US Equity Options

An **option** grants a right, not an obligation, to transact in an underlying asset at a strike by/on expiry. Calls grant a right to buy; puts a right to sell. US equity options are generally American style, exercisable before expiry, and physically settled. Each listed contract represents 100 underlying shares, so listed option prices and payouts must be multiplied by 100 for contract cash amounts. Source: pp. 19–20.

OPRA consolidates US option-exchange prices. Roughly 1.5 million contracts across about 4,000 liquid companies may exist on a day, producing hundreds of terabytes because strikes and expiries multiply the data set. QuantConnect supports an underlying option universe with filtering, subscription to individual contracts, and option-chain access through data slices. Source: p. 20.

A call is ITM when underlying price exceeds strike; a put is ITM when underlying price is below strike. The opposite relationships are OTM. Exercise of an ITM option creates positive cash flow for its buyer; OTM options can serve as catastrophe insurance. Source: p. 20.

Early exercise of an American call is described as unlikely because its pre-expiry theoretical value should exceed intrinsic value; selling to close generally captures the gain without discarding time value. At expiry, a broker automatically exercises an ITM call, delivering shares for strike-price cash. American puts can be exercised early; a short-put seller may be assigned shares above market and incur a loss. ITM puts held to expiry are automatically exercised, with assignment managed by the exchange/broker on FIFO. Source: pp. 20–21.

#### Index Options

Equity-index options differ chiefly by being European style (exercise only at expiry) and cash settled. Payout is based on the difference between index and strike levels times the multiplier. QuantConnect supports monthly and weekly variants for VIX/VIXW, NDX/NQX, and SPX/SPXW. NDX references Nasdaq-100; SPX references S&P 500; VIX reflects a 30-day expected S&P 500 volatility measure derived from SPX option quotes. Each listed example has a multiplier of 100. Source: p. 21.

Cash settlement creates tax treatment different from equity options. Broker permission may be required and some brokers disallow index-option trading; eligibility and tax advice must be obtained externally. Source: p. 21.

#### US Futures

Futures originally let producers lock in future commodity prices and reduce revenue uncertainty; markets expanded from agriculture into metals, energy, bonds, indices, and currencies. Contracts settle at discrete monthly/quarterly expiries, and a product's active expiries form a universe. Source: pp. 21–22.

The **front month** is the contract most closely tracking spot. **Rolling** selects the next front month, introducing a jump because the two contracts have different prices and expiries. A **continuous contract** stitches and normalizes successive contracts for analysis; it is a representation, not an actual tradable price, and has no uniquely correct normalization. QuantConnect calls it the **canonical** contract and calls the current tradable underlying contract the **mapped** asset. Signals may use the canonical series, but orders must target `future.mapped`. Source: p. 22.

At a roll, mapped prices jump, so indicators must be reviewed/reset. After settlement, delisting emits an event. Although P&L is commonly marked/settled daily in cash, many commodity and financial contracts still require physical delivery at expiry. Speculators should close or roll before broker liquidation deadlines; forced liquidation can damage a portfolio. Source: pp. 22–23.

#### Cryptocurrency

Crypto trading is fragmented across centralized and decentralized exchanges. Unlike SIP-linked US equities, venues are independent, have different prices, and rely on private market makers plus cross-exchange arbitrage. The ecosystem has grown from spot cash trading into margin and derivatives. Source: p. 23.

The same text ticker is venue-specific: `BTCUSD` on Coinbase and Kraken represents distinct markets and prices, so QuantConnect subscriptions specify `market`. A matching brokerage model must also encode the venue's assets, order types, margin rules, and cash/margin account type. Source: pp. 23–24.

## Formulas and Quantitative Relationships

The chapter contains no typeset equations, but states these operational relationships:

- **Mid-price:** $M=(B+A)/2$, where $B$ is best bid and $A$ best ask. Internal crosses are often near $M$. Source: p. 5.
- **Bid-ask spread:** $S=A-B$. A market buy crosses to $A$; a market sell crosses to $B$. Source: pp. 8, 12.
- **Slippage:** execution slippage is the final fill price minus the expected execution price, interpreted directionally as an adverse cost. Source: p. 12.
- **PE ratio:** $PE=P/EPS$, where $P$ is close price and $EPS$ earnings per share. Source: p. 16.
- **Free-cash-flow percent:** $FCF\%=FCF/OCF$ (expressed as a percentage), where $OCF$ is operating cash flow. Source: p. 16.
- **Dividend payout ratio:** $DPR=D/NI$, dividend payments divided by net earnings. Source: p. 16.
- **Split invariance:** immediately at an ideal split, old shares × old price = new shares × new price; Figure 1.10 shows $1\times\$100=2\times\$50$. Source: p. 17.
- **Equity-option contract amount:** listed option price or per-share payout × 100 shares per contract. Source: p. 20.
- **Moneyness:** call ITM if $S>K$ and put ITM if $S<K$, where $S$ is underlying price and $K$ strike. Source: p. 20.
- **Index-option settlement:** payout depends on the favorable difference between index level and strike, multiplied by the contract multiplier (100 for NDX, SPX, and VIX examples). Source: p. 21.
- **Reverse-split example:** consolidating two shares into one approximately doubles unit price, absent other market movement. Source: p. 17.

## Methods and Procedures

### Build Research Data from Market Events

1. Preserve event time and distinguish trade from quote ticks.
2. Filter/flag late or erroneous prints without using knowledge unavailable at that time.
3. Consolidate ticks to an interval suitable for research: trade OHLCV or bid/ask quote OHLC.
4. Use quote bars, when present, to model executable fills rather than assuming the last trade.
5. Add alternative/custom data only after defining its timing and parsing semantics.

Source: pp. 7–10.

### Model an Executable Strategy

1. Select a brokerage model matching supported assets, orders, fees, margin, and venue.
2. Use an order type actually supported by that brokerage.
3. Retain the order ticket for permitted update/cancel operations.
4. Include explicit fees/taxes, spread crossing, slippage, and market impact.
5. Scale execution or use more sophisticated scheduling when order size is large relative to depth.

Source: pp. 10–13.

### Handle Equity Corporate Actions

1. Track assets with persistent Symbol objects, not ticker strings alone.
2. Consume split, dividend, symbol-change, securities-change, and delisting events.
3. Reset indicators after discontinuous raw-price events such as splits.
4. Choose `RAW`, `ADJUSTED`, or `SPLIT_ADJUSTED` normalization according to the accounting question.
5. Preserve portfolio identity through rename, merger, spin-off, and delisting transitions.

Source: pp. 14–19.

### Trade Futures Without Delivery Surprises

1. Use the canonical continuous series only for analysis/signals.
2. Resolve and trade the current mapped contract.
3. Detect roll changes and review/reset affected indicators.
4. Learn the broker's early-liquidation date.
5. Close or roll physical-delivery exposure before forced liquidation or delivery.

Source: pp. 22–23.

## Examples

- A benchmark mutual fund rebalance is liquidity trading because execution seeks portfolio alignment, not profit from privileged information. Source: p. 5.
- A broker who trades ahead of a known, market-moving client block order commits front-running. Source: pp. 6–7.
- A stale late-reported trade can look like a discontinuous price move even though it occurred earlier. Source: pp. 7–8.
- Google’s 2014 Class A/Class C restructuring shows ticker strings changing while the underlying Symbol identity persists. Source: p. 14.
- A fundamental screen selects equities with PE below 10. Source: p. 16.
- Berkshire Hathaway Class A is used as an example of a never-split, extremely high-price share with reduced accessibility; the book states a price above $200,000 at publication. Source: pp. 16–17.
- A two-for-one split turns one $100 share into two $50 shares while preserving $100 total value. Source: p. 17.
- An ITM call is generally sold to close before expiry rather than exercised early; an ITM short put can be assigned early, forcing purchase above market. Source: pp. 20–21.
- Coinbase BTCUSD and Kraken BTCUSD are separate venue-specific securities despite identical ticker text. Source: pp. 15, 23–24.

## Figures and Tables

| Figure | Meaning | Source |
|---|---|---|
| 1.1 | Retail orders are concentrated among market makers, public exchanges collectively generate NBBO, and institutional orders also use fragmented private ATS venues. | p. 3 |
| 1.2 | During the May 6, 2010 crash, P&G fell far more abruptly than broad indices/other assets before rebounding; the dollar index stayed comparatively stable, showing uneven cross-asset impact. | p. 8 |
| 1.3 | A trade bar compresses individual trades into interval open, high, low, close, and volume. | p. 9 |
| 1.4 | A quote bar separately aggregates bid and ask OHLC and derives their midpoint, preserving executable-side information. | p. 9 |
| 1.5 | An algorithm sends an order to a brokerage and receives confirmation/status feedback through an order ticket. | p. 11 |
| 1.6 | Sell market orders execute at bid; buys at ask; last sale can lie anywhere between/at those prices and is not necessarily executable. | p. 12 |
| 1.7 | Liquid assets show limited taken depth and a small midpoint shift; illiquid assets consume more levels and move the new midpoint farther, illustrating larger impact/slippage. | p. 12 |
| 1.8 | Google's Class A, Class C, and temporary “when issued” listings overlap through a restructuring, demonstrating complex ticker history. | p. 14 |
| 1.9 | GOOCV changes to GOOG at an event date while the encoded Symbol and Google Class-C asset identity remain continuous. | p. 14 |
| 1.10 | A two-for-one split doubles shares and halves per-share price while preserving owner value. | p. 17 |

No tables appear in the chapter.

## Applications

- Detect informed-flow or other high-volume market patterns with machine learning. Source: p. 7.
- Build backtests from point-in-time ticks/bars without assuming corrected future data. Source: pp. 7–9.
- Use news, sentiment, weather, geolocation, or custom factor data as candidate predictive features. Source: pp. 9–10.
- Screen equities with standardized fundamentals and train models on ratios/corporate actions. Source: p. 16.
- Simulate broker-specific fills and costs before live deployment. Source: pp. 10–13.
- Maintain survivorship and identity continuity across corporate changes. Source: pp. 13–19.
- Analyze futures on normalized series while routing execution to real mapped contracts. Source: p. 22.

## Assumptions, Limitations, and Edge Cases

- NBBO excludes odd lots under the rule described, so small-lot price improvement may be invisible to national best pricing. Source: p. 3.
- DMA provides venue control, not guaranteed national-best execution. Source: p. 4.
- Limit orders may never fill; market orders assume enough liquidity for reasonable immediacy. Source: p. 5.
- Point-in-time truth can contain bad or late data; retroactive cancellation cannot be known in advance. Source: pp. 7–8.
- Bar consolidation reduces size but discards tick-level sequence and detail. Source: p. 9.
- Brokerage order capabilities and update rules vary; platform availability does not guarantee broker support. Source: p. 11.
- Default liquid-fill assumptions are unsuitable for illiquid assets or large orders. Source: pp. 12–13.
- Adjusted prices simplify analysis but do not uniquely solve normalization and may abstract away cash/reinvestment timing. Source: p. 18.
- Options create exceptionally large data universes; filters are operationally important. Source: p. 20.
- Early-call-exercise reasoning is stated as a general theory result; taxes and special situations can affect actual decisions. Source: pp. 20–21.
- Continuous futures normalization has no single correct method and the resulting price is not tradable. Source: p. 22.
- Crypto has no consolidated national feed, so venue identity and broker model are integral to the security definition. Source: pp. 23–24.

## Common Mistakes and Warnings

- Treating last sale as the fill price and ignoring spread. Source: p. 12.
- Ignoring fees, slippage, and impact when evaluating profitability. Source: pp. 11–13.
- Interpreting late prints as genuine contemporaneous jumps. Source: pp. 7–8.
- Assuming DMA necessarily obtains the best price. Source: p. 4.
- Keying histories by ticker rather than persistent security identity. Source: pp. 13–15.
- Failing to reset continuity-dependent indicators after splits or futures rolls. Source: pp. 17, 22–23.
- Multiplying option positions by listed price but forgetting the 100-share contract multiplier. Source: p. 20.
- Exercising an ITM call early instead of considering sale-to-close and remaining time value. Source: p. 20.
- Selling American puts without accounting for early assignment. Source: pp. 20–21.
- Sending an order to a canonical futures Symbol rather than the mapped contract. Source: p. 22.
- Holding physical-delivery futures into broker-forced liquidation or delivery windows. Source: pp. 22–23.
- Treating same-text crypto pairs on different exchanges as interchangeable. Source: pp. 15, 23–24.

## Key Takeaways

1. Executable price is determined by venue, side, spread, depth, and timing—not merely the last trade.
2. Participants face a trade-off among immediacy, price control, liquidity provision, and adverse selection.
3. Point-in-time data integrity includes preserving errors and later corrections with their actual availability times.
4. Realistic brokerage, fee, fill, slippage, and market-impact models are prerequisites for credible research.
5. Stable asset identity and explicit corporate-event handling prevent subtle longitudinal errors.
6. Each asset class has distinct multipliers, exercise/settlement, expiry, normalization, delivery, and venue rules that an algorithm must encode.

## Glossary

| Term | Definition | Source |
|---|---|---|
| Ask | Price at which a seller offers an asset. | pp. 3–5 |
| ATS | Private alternative trading system used especially for institutional flow. | p. 3 |
| Bid | Price at which a buyer offers to purchase an asset. | pp. 3–5 |
| Canonical contract | QuantConnect continuous normalized futures representation used for analysis, not trading. | p. 22 |
| Corporate action | Company lifecycle event such as dividend, split, merger, or acquisition. | p. 16 |
| DMA | Direct routing to a selected exchange. | p. 4 |
| FIGI | Bloomberg proprietary identifier lookup service described as free. | p. 13 |
| Front month | Futures contract most closely tracking spot among active expiries. | p. 22 |
| Front-running | Illegal trading ahead of a known market-moving client order. | pp. 6–7 |
| Informed trader | Trader possessing advantaged nonpublic information. | pp. 6–7 |
| ISIN | International identifier formed for many US/Canadian assets from country code and CUSIP. | p. 13 |
| Limit order | Order constrained to a stated price or better; execution is not assured. | pp. 4–5 |
| Liquidity trader | Trader seeking execution without privileged information. | p. 5 |
| Mapped asset | Current underlying tradable futures contract associated with a canonical series. | p. 22 |
| Market maker | Participant/strategy that supplies liquidity and improves price or immediacy. | pp. 5–6 |
| NBBO | National best publicly posted bid and offer in US markets. | p. 3 |
| Odd lot | Equity order/quote smaller than 100 shares. | p. 3 |
| OPRA | Consolidator of US options exchange price data. | p. 20 |
| Order ticket | QuantConnect handle for order feedback and allowed update/cancel actions. | p. 11 |
| Point-in-time data | Data preserved as available at its capture time, including imperfections. | p. 7 |
| Quote bar | Fixed-interval OHLC aggregation with bid and ask child bars. | p. 9 |
| SIP | Processor consolidating public US exchange trades and quotes. | p. 3 |
| Slippage | Difference between expected execution price and final fill. | p. 12 |
| Symbol | QuantConnect's persistent, self-contained encoded security identity. | pp. 14–15 |
| TRF | Facility to which off-market trades are reported before inclusion in consolidated data. | pp. 3–4 |
| Walk-the-book | Sequential execution through progressively worse price levels when top-level size is insufficient. | pp. 4–5, 12–13 |

## Connections to Other Chapters

- The chapter explicitly states that later chapters use AI trained on corporate actions and machine learning on fundamental ratios to predict prices or formulate strategies. Source: p. 16.
- Later chapters will address the scientific process of converting alternative data into tradable signals. Source: p. 10.
- The five asset classes and their QuantConnect representations establish the data and execution primitives used in later examples. Source: p. 15.

## Extraction Issues

- The chapter introduction says “five asset classes,” but the named subsections are US equities, US equity options, index options, US futures, and cryptocurrency; index options are treated separately although they are also options. Source: pp. 15–24.
- The source says market feeds generate “three primary data types of tick data” but lists trade ticks and quote ticks, then discusses consolidated data separately; consolidated bars are derived from ticks rather than a third tick type. Source: pp. 8–9.
- The source states an ISIN is country code plus the “eight-digit CUSIP,” but standard identifier composition can be more nuanced; this extraction preserves the chapter's statement without external correction. Source: p. 13.
- A code sample for `on_data(self, slice:` appears syntactically incomplete in the source. It is treated as illustrative, not silently corrected. Source: p. 17.
- Time-sensitive counts, market shares, asset prices, platform coverage, and supported datasets/order types are preserved as claims made by the book at publication, not verified as current facts.
