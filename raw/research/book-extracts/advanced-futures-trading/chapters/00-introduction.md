# Introduction

## Purpose and central argument

This introduction positions *Advanced Futures Trading Strategies* (AFTS) as a practical reference for serious futures traders. Its central argument is that futures trading should be approached deliberately, with clearly specified and historically tested strategies, disciplined risk and position management, and diversification across both strategies and markets.

The book presents 30 futures-specific strategies tested on data from more than 100 instruments, with some histories exceeding 50 years. It argues that testing a strategy across many markets increases confidence that its apparent effectiveness is not confined to a single market or unusually favorable environment. At the same time, a strategy must be assessed for suitability to each specific instrument and adapted when needed.

## Author context and approach

The author contrasts an initial instinctive purchase of one December Bund futures contract in September 2002 with his subsequent systematic approach. His stated professional background includes development and management of systematic futures strategies at AHL, followed by personal automated futures trading.

The book’s stated approach is:

- **Systematic and objective:** Given the same data, the strategies always recommend the same action; their instructions are intended to be followed without discretionary deviation.
- **Rules-based and testable:** Each strategy’s rules and historical performance are described so readers can understand strengths, weaknesses, and expected future behavior.
- **Price-data focused:** The main strategies use price data only.
- **Practical:** Strategy chapters include strategies that can actually be traded, while early chapters introduce concepts used throughout the book.

The author permits discretionary use as an overlay: a reader may use strategy signals to inform a final judgment. This is outside the strictly systematic use case, but explicitly allowed as a possible application.

## What the book covers

### Strategy set and diversification

The book addresses diversification in two dimensions:

1. **Across trading strategies and time scales.**
2. **Across futures markets.** The author calls market diversification an especially potent source of extra profits.

The markets described as available through futures are globally diverse, including interest rates, cryptocurrency, iron ore, stocks, and milk. The introduction emphasizes that markets differ in participants and drivers, yet asks whether common strategies can work across asset classes. Its proposed benefit of common strategies is the ability to test them over a wider cross-section of markets.

### Portfolio and implementation topics

Beyond forecasting market direction, the book says it will cover:

- Selecting markets given available capital.
- Allocating risk across a portfolio.
- Evaluating strategy performance.
- Choosing the appropriate degree of leverage.
- Predicting and managing risk.
- Measuring and reducing trading costs.
- Contract selection, trade execution, and cash management.

### Tools and mathematical level

Most strategies are said to be implementable in a spreadsheet. The book’s website, linked in Appendix A, provides copyable/adaptable spreadsheets and Python code snippets. Most equations are described as high-school-level mathematics, though a few chapters contain more advanced material that may be skipped.

**Formulas in this chapter:** None are provided.

## Intended readership and entry requirements

The stated rule of thumb is that the book is most useful to traders with at least **$100,000** (or equivalent) in a trading account. Some futures can be accessed with a few thousand dollars, but most require substantially more capital.

The book is not presented as a beginner primer. It assumes rudimentary knowledge of futures markets and trading jargon. Its examples use US dollars for simplicity, but the intended audience is not limited to US residents; usefulness is conditioned on the reader being legally able to trade futures in their jurisdiction. Cross-border issues are promised later in the book.

For readers outside the United States who lack the stated capital level, the footnote identifies dated contracts for difference (CFDs) or spread bets as possible alternatives to futures, while warning that they are more expensive to trade even though their funding requirements are lower. The book points to *Leveraged Trading* for treatment of those instruments.

## Scope and exclusions

The exclusions below are substantive boundary conditions for interpreting every strategy and result in the book.

| Excluded or limited area | Stated boundary / implication |
|---|---|
| Subjective decision-making | Strategies are objective, though their signals may be incorporated into a discretionary methodology. |
| Fundamental data | Main strategies use price data only; no CPI, nonfarm-payroll, earnings, commitment-of-traders, or rig-count inputs. Part Three nevertheless explains how to construct a strategy from arbitrary quantifiable data, which could include fundamental data. |
| Volume data | Not used. The stated reason is that futures volume is difficult to analyze systematically because rolling between contract expiries affects it. |
| Candlesticks / OHLC data | Only closing prices for each relevant period are used. Open, high, and low prices—and strategies based on candlestick patterns—are excluded. |
| High-frequency or very fast trading | The smallest collected price interval is hourly. Strategies with holding periods under a few hours cannot be accurately tested on this data. The author advises that most traders should not try to compete with specialized high-frequency firms. |
| Options | Futures options could be used to express a strategy, but this is explicitly not an options-trading book. |
| Individual stocks | Strategies may be applicable to shares, but no suitability analysis or individual-equity testing is claimed. Equity-index futures, including the S&P 500 index, are included in testing. |
| Other asset classes directly | The book is not directly about crypto, FX, or bonds, but futures based on those assets can generally be traded. |
| Tax | No tax treatment, tax optimization, or tax-loss-harvesting strategy is included. Tax treatment is described as complex, jurisdiction-dependent, owner-status-dependent, and changing. |
| Complete universe of futures | The book does not test every future. It uses more than 100 futures that meet liquidity and cost requirements; data for other markets can be unavailable, difficult, or too expensive. |

### Data-universe qualifications

The book reports that it tested the strategies on over 100 futures satisfying its liquidity and cost requirements, which are said to be detailed in Strategy Three. It also reports tests on about 50 additional instruments that were too expensive or illiquid to trade; results were not significantly different. The author nevertheless does not claim coverage of all futures markets.

One specific data limitation is named: due to data-acquisition costs, the author could not trade or test UK Intercontinental Exchange (ICE) futures including short sterling interest-rate futures, UK gilt futures, and FTSE 100 index futures.

## Key distinctions and concepts

### Systematic vs. discretionary trading

- **Systematic trading:** clear rules, no discretionary judgment, and identical action for identical inputs.
- **Discretionary trading:** the trader may combine strategy signals with personal intuition, experience, and final judgment.

The book is written to support systematic implementation; discretionary application is presented as optional rather than the basis of the tests.

### Directional vs. relative-value strategies

- **Directional strategy:** bets on the overall direction of a market, rather than on relative performance between instruments.
- **Relative-value strategy:** tries to predict relative futures-price movements while, ideally, hedging overall market movement.

Relative-value approaches later include:

- **Calendar strategies:** trade different delivery months of the same future against each other.
- **Cross-instrument strategies:** trade the relative value of different futures.

### Trend following and carry

- **Trend following:** identifies trends assumed to continue.
- **Carry:** uses futures prices at different expiry dates to try to predict the future.

Both are directional strategies. They are introduced near the end of Part One and expanded in Part Two.

### Closing prices vs. OHLC/candlestick data

The strategies rely on closing prices for the relevant time period. They do not use the OHLC set—open, high, low, and close—needed to construct candlestick charts. The author’s stated rationale is explanatory and operational simplicity, plus a lack of conviction from testing that patterns uniquely visible in candlesticks create profitable objective strategies.

## Recommended reading order and book architecture

The author strongly instructs readers to read **Part One: Basic Directional Strategies** before any other part. It contains tradable strategies but also progressively introduces concepts needed throughout the book.

| Book component | Focus and relationship to other components |
|---|---|
| Part One: Basic Directional Strategies | Required starting point; defines foundations used throughout. Exclusively directional. |
| Part Two: Advanced Trend Following and Carry Strategies | Extends the trend-following and carry approaches introduced near the end of Part One. |
| Part Three: Advanced Directional Strategies | Other directional sources of return beyond trend following and carry; also includes a method for a strategy based on arbitrary quantifiable input data. |
| Parts One–Three | Can be mixed and matched because they use a consistent position-management methodology and are designed to trade once daily using daily data to determine trades. |
| Part Four: Fast Directional Strategies | A small number of strategies that trade more often than daily; holding periods can be hours or days rather than weeks. Not high-frequency trading. |
| Part Five: Relative Value Strategies | Calendar and cross-instrument relative-value strategies; shifts away from directional prediction. |
| Part Six: Tactics | Contract selection, risk control, execution, and cash management; does not try to predict absolute or relative price movement. |
| Appendix A | Further resources, including useful books, websites, and the site link for code/spreadsheets. |
| Appendix B | Key calculations used throughout the book. |
| Appendix C | Full list of futures contracts used in the book. |

In Parts One to Five, “chapter” can mean a strategy; in Part Six, it can mean a tactic.

## Connections to the author’s other books

- **Leveraged Trading (LT):** introductory material on the mechanics of leveraged instruments such as futures; recommended if the reader needs basic futures knowledge. It is said to help with concepts introduced in AFTS Part One and covers CFDs/spread bets.
- **Systematic Trading (ST):** primarily about general strategy design rather than futures specifically. It overlaps briefly with futures and some strategies covered in AFTS. Readers seeking to develop and test their own futures strategies are advised to read both AFTS and ST.
- **Recommended sequence for a complete beginner who wants to design strategies:** LT → AFTS → ST.
- **Smart Portfolios:** about investment, not trading; no prerequisite relationship is asserted.

## Practical implications and cautions

- Treat the historical tests as cross-market evidence, not as a claim that any strategy fits every instrument unchanged.
- Capital, liquidity, costs, and legal ability to trade are explicit constraints on implementation.
- Do not infer support for intraday approaches with sub-hour holding periods from this book’s test framework.
- Do not infer results for individual stocks, options strategies, tax-adjusted outcomes, volume-based methods, candlestick methods, or fundamental-data strategies from the book’s main analysis.
- A reader who skips Part One risks missing concepts necessary for the later parts, even if experienced.
- The introduction provides an authorial opinion that competing with specialized high-frequency firms is unrealistic for most traders; this is not supplied as a demonstrated result in the chapter.

## Figures, tables, examples, and equations

### Figures and tables

The introduction contains no figures, diagrams, data tables, or mathematical equations. The scope and book-architecture tables above reorganize narrative content for reference; they are not reproductions of source tables.

### Narrative example: first futures trade

The author’s first trade was a single December Bund futures contract. Faced with whether to buy or sell and without a stated analysis, he chose to buy to avoid delay. This is used to frame the contrast between instinctive trading and the book’s deliberate, analysis-backed strategy process. No price, profit/loss, or calculation is supplied.

## Glossary

- **AFTS:** *Advanced Futures Trading Strategies*, the book discussed in this introduction.
- **Bund:** the futures contract for 10-year German government bonds in the author’s narrative; a footnote says the name is apparently short for *Bundesanleihe*.
- **Calendar strategy:** a relative-value strategy trading different delivery months of the same future against each other.
- **Carry:** a directional approach using futures prices at different expiries to try to predict the future.
- **CFD (contract for difference):** named as a possible lower-funding-requirement alternative to futures for some non-US readers; the chapter states it is more expensive to trade.
- **Closing price:** the only price type used for the strategies for each relevant time period.
- **Cross-instrument strategy:** a relative-value strategy trading the relative value of different futures.
- **Directional strategy:** a strategy that bets on overall market direction.
- **Discretionary trading:** trading in which human judgment makes the final decision, potentially informed by strategy signals.
- **Futures contract:** the book’s primary trading instrument; the introduction does not provide a formal contract definition.
- **High-frequency trading:** trading faster than the book’s addressed scope; the smallest source-data interval is hourly.
- **Leverage:** a topic the book says it will address through selecting the correct degree of leverage; no formal definition is supplied here.
- **OHLC:** open, high, low, close prices, excluded from the main strategies.
- **Position-management methodology:** the common methodology that allows Parts One–Three strategies to be combined; its mechanics are not defined in this introduction.
- **Relative-value strategy:** a strategy seeking to predict relative futures-price movement while ideally hedging overall market movement.
- **Spread bet:** an alternative identified with CFDs for certain lower-funding-requirement cases outside the United States; no definition is supplied.
- **Systematic trading:** rule-based, objective trading with no discretionary deviation.
- **Trend following:** a directional approach that identifies trends assumed to continue.

## Key takeaways

1. The book advocates deliberate, rule-defined, historically tested futures trading rather than instinctive decision-making.
2. Its 30 strategies are evaluated over a broad cross-section of futures markets and long data histories, but must still be checked and adapted for individual instruments.
3. Diversification across strategies, time scales, and especially markets is a central portfolio principle.
4. The practical framework includes risk, leverage, costs, contract selection, execution, and cash management—not only price forecasting.
5. Part One is essential prerequisite reading; later parts are organized by directional, fast directional, relative-value, and tactical applications.
6. The strategy evidence is bounded by the data and methods used: primarily closing-price-based, non-fundamental, non-volume, non-candlestick, and not high-frequency, tax, individual-stock, or options analysis.
