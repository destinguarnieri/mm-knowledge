---
title: "Step 1: Problem Definition"
chapter: 3
source: "Hands-On AI Trading with Python, QuantConnect, and AWS"
source_file: "OPS/c003.xhtml"
status: "extracted"
---

# Chapter 3: Step 1: Problem Definition

## Overview

Problem definition converts a broad financial goal into a precise algorithmic-trading task. The process begins with a financial objective, translates that objective into a target variable, fixes the scope and constraints, identifies possible predictor variables, and states a hypothesis linking those predictors to the target. The chapter demonstrates this framework with three cases: next-day price forecasting, adaptive portfolio rebalancing, and reinforcement-learning-based trade execution. (Source: pp. 49–51)

## Learning Objectives (Inferred)

After studying this chapter, a reader should be able to:

- Translate a financial objective into a measurable prediction or optimization target. (Source: p. 49)
- Define a trading problem's time horizon, market and asset universe, constraints, risk tolerance, and performance benchmarks. (Source: p. 49)
- Distinguish a target variable (label/dependent variable) from predictor variables (features/factors/independent variables). (Source: p. 49)
- Form a hypothesis about how available features could explain or predict the target. (Source: p. 49)
- Apply the problem-definition framework to forecasting, portfolio management, and trade execution. (Source: pp. 50–51)

## Key Concepts

### Financial Objective

The financial objective states the specific outcome an algorithm should achieve. Examples include forecasting stock prices, improving trade execution, and managing risk through dynamic portfolio changes. It is the business or investment purpose from which the technical task is derived. (Source: p. 49)

### Target Variable

The target variable is the measurable quantity the algorithm will predict or optimize. It is also called the **label** or **dependent variable**. Examples given in the chapter include a future stock price, next-period market volatility, and expected portfolio return. The target must directly operationalize the financial objective. (Source: p. 49)

### Scope and Constraints

Once the target is selected, the problem must be bounded along several dimensions: (Source: p. 49)

- **Prediction or decision horizon:** intraday, daily, weekly, or another explicit time frame.
- **Markets and assets:** for example, equities, commodities, or foreign exchange.
- **Regulatory constraints:** applicable financial regulations and trading rules.
- **Operational constraints:** practical restrictions such as transaction costs, liquidity, order size, or rebalancing frequency.
- **Risk tolerance:** the amount and type of risk the strategy may assume.
- **Performance benchmarks:** reference measures against which success is judged.

These boundaries determine what data is relevant, what actions are feasible, and how performance should be evaluated.

### Predictor Variables

Predictor variables are the inputs believed to contain information about the target. They are also called **features**, **factors**, or **independent variables**. Candidate inputs may include price histories, volume, macroeconomic indicators, and sentiment extracted from news or social media. (Source: p. 49)

### Hypothesis Linking Features to the Target

A well-defined problem includes an explicit hypothesis about how candidate features interact with, explain, or predict the target variable. This hypothesis guides subsequent data collection and feature engineering rather than allowing those activities to proceed without a defined purpose. (Source: p. 49)

### Case Study 1: Forecasting Short-Term Stock Market Trends

#### Objective and Target

The objective is to find profitable opportunities on a daily horizon. The target is an equity's closing price on the next trading day. (Source: p. 50)

#### Scope and Constraints

- **Time frame:** daily prediction.
- **Universe:** equities listed on major exchanges, including the NYSE and NASDAQ.
- **Regulatory constraint:** compliance with relevant financial regulations.
- **Operational constraints:** transaction costs and possible liquidity limitations. (Source: p. 50)

#### Candidate Features

- Historical close, high, low, and open prices.
- Daily trading volume.
- Technical indicators: moving averages (MA), Relative Strength Index (RSI), and Bollinger Bands.
- Economic variables such as interest rates and inflation rates.
- Sentiment scores derived from financial news and social media. (Source: p. 50)

#### Hypothesis

Patterns across historical prices, volume, technical signals, economic conditions, and sentiment may each provide different amounts of predictive information about the next closing price. The chapter does not assert equal usefulness or guaranteed predictability; feature value remains an empirical question. (Source: p. 50)

### Case Study 2: Mitigating Risk with Adaptive Portfolio Rebalancing

#### Objective and Target

The objective is to maximize risk-adjusted return while maintaining a desired risk profile. The target is a portfolio risk-adjusted-return measure, with the Sharpe ratio offered as an example. (Source: p. 50)

#### Scope and Constraints

- **Time frame:** weekly portfolio adjustments.
- **Universe:** US equities, bonds, and commodities.
- **Portfolio constraints:** allocation limits and diversification rules.
- **Regulatory constraint:** compliance with portfolio-management regulations.
- **Operational constraints:** transaction costs and rebalancing frequency. (Source: p. 50)

#### Candidate Features

- Historical prices and returns for assets held or considered for the portfolio.
- Risk measures including volatility, value at risk (VaR), and cross-asset correlations.
- Macroeconomic information that affects the included asset classes.
- News- and social-media-derived market sentiment. (Source: pp. 50–51)

#### Hypothesis

Actively changing portfolio composition in response to market conditions and updated risk assessments may improve return after accounting for risk, while still respecting a specified risk exposure. (Source: p. 51)

### Case Study 3: Enhancing Trade Execution with Reinforcement Learning Techniques

#### Objective and Target

The objective is to execute trades with lower transaction costs and less market impact. The target is execution-price improvement relative to a benchmark, such as volume-weighted average price (VWAP). (Source: p. 51)

#### Scope and Constraints

- **Time frame:** intraday.
- **Universe:** highly liquid US equities and exchange-traded funds (ETFs).
- **Regulatory constraint:** compliance with market regulations and trading rules.
- **Operational constraints:** order size, market impact, and available liquidity. (Source: p. 51)

#### Candidate Features

- Real-time order-book observations, trade prices, and volumes.
- Execution benchmarks, particularly VWAP and time-weighted average price (TWAP).
- Order attributes: size, order type (including market or limit), and execution time.
- Economic events and news that could alter liquidity.
- Historical execution quality and slippage. (Source: p. 51)

#### Hypothesis

A reinforcement-learning algorithm may reduce costs and improve execution prices by learning better order-placement and timing decisions. This is a testable proposition, not a guaranteed result. (Source: p. 51)

## Formulas and Quantitative Relationships

The chapter does not present explicit equations or mathematical derivations. It does, however, define several quantitative relationships that later work would need to formalize:

- **Forecasting target:** the next trading day's closing price is modeled as a function of historical market data, technical indicators, economic variables, and sentiment. No functional form is specified. (Source: p. 50)
- **Portfolio target:** performance is evaluated on a risk-adjusted basis, with the Sharpe ratio named as an example target. No Sharpe-ratio equation, return interval, or risk-free-rate convention is supplied. (Source: p. 50)
- **Execution target:** execution-price improvement is measured relative to a benchmark price such as VWAP. The sign convention and exact calculation are not defined. (Source: p. 51)
- **Execution costs:** transaction costs and market impact are quantities to minimize, while liquidity and order size constrain the optimization. No objective function is provided. (Source: p. 51)

## Methods and Procedures

### Problem-Definition Workflow

1. **State the financial objective.** Specify the economic outcome the algorithm should achieve. (Source: p. 49)
2. **Translate the objective into a target.** Choose a measurable label or dependent variable to predict or optimize. (Source: p. 49)
3. **Set the time frame.** Define how frequently predictions or decisions occur, such as intraday, daily, or weekly. (Source: p. 49)
4. **Choose the asset and market universe.** Identify which instruments and venues fall within the problem. (Source: p. 49)
5. **Record constraints and evaluation criteria.** Include regulatory and operational constraints, risk tolerance, and performance benchmarks. (Source: p. 49)
6. **Identify candidate features.** Select plausible market, technical, economic, risk, sentiment, order, or execution inputs relevant to the target. (Source: p. 49)
7. **State a testable hypothesis.** Explain why and how those features might predict or improve the target. Use that hypothesis to direct data collection and feature engineering. (Source: p. 49)

## Examples

### Daily Equity Forecasting Example

A next-day equity forecasting problem combines a daily target (tomorrow's close), a large-exchange equity universe, transaction-cost and liquidity restrictions, and predictors spanning prices, volume, technical indicators, macroeconomic data, and sentiment. The output is intended to help identify profitable daily opportunities. (Source: p. 50)

### Weekly Adaptive Allocation Example

A portfolio algorithm reconsiders allocations weekly across US stocks, bonds, and commodities. It uses market, risk, macroeconomic, and sentiment inputs to pursue improved risk-adjusted return while honoring diversification, allocation, and risk-exposure requirements. (Source: pp. 50–51)

### Intraday Execution Example

An execution algorithm for liquid US equities and ETFs observes real-time market and order information and chooses order placement and timing. Its success is judged by costs, market impact, and execution-price performance relative to VWAP or a similar benchmark. (Source: p. 51)

## Figures and Tables

The chapter contains no figures or tables. Its three case studies are presented as boxed text sections rather than tabular or graphical material. (Source: pp. 50–51)

## Applications

- **Alpha-oriented forecasting:** define supervised-learning tasks that predict a future price or other market outcome. (Source: pp. 49–50)
- **Risk-aware portfolio management:** adapt allocations as market conditions and risk measures change. (Source: pp. 50–51)
- **Execution optimization:** apply reinforcement learning to order placement and timing under liquidity and impact constraints. (Source: p. 51)
- **Data and feature planning:** use the hypothesis and target definition to decide which historical, real-time, economic, technical, or sentiment data should be collected. (Source: p. 49)

## Assumptions, Limitations, and Edge Cases

- The chapter assumes that the financial objective can be represented by a measurable target variable. It does not address objectives that require multiple competing targets. (Source: p. 49; limitation inferred)
- Candidate features are hypotheses about useful information, not proof of predictive value. Validation procedures are outside this chapter's scope. (Source: pp. 49–51)
- Time horizon and universe choices materially change the data, constraints, and decision process; they cannot be left implicit. (Source: pp. 49–51)
- Regulatory and operational feasibility are part of the problem definition, not post-model deployment details. (Source: pp. 49–51)
- The forecasting example acknowledges transaction costs and liquidity but does not specify thresholds or how profitability should be calculated after costs. (Source: p. 50)
- The portfolio example does not define the desired risk profile, allocation bounds, diversification rules, or precise Sharpe-ratio methodology. (Source: pp. 50–51)
- The execution example does not define benchmark-calculation windows, the direction/sign of price improvement, reinforcement-learning states/actions/rewards, or treatment of partial fills. (Source: p. 51)

## Common Mistakes and Warnings

- Starting with a model or data source before specifying the financial objective and target can disconnect the technical work from the intended outcome. (Source: p. 49; warning inferred from the prescribed sequence)
- Treating features and labels as interchangeable obscures what is being predicted versus what information is used to predict it. (Source: p. 49)
- Leaving the time horizon, asset universe, benchmark, risk tolerance, or constraints vague produces an underspecified problem. (Source: p. 49)
- Ignoring trading frictions such as transaction costs, liquidity, slippage, rebalancing frequency, and market impact can make an otherwise plausible objective operationally unrealistic. (Source: pp. 50–51)
- Treating the case-study hypotheses as established facts would overstate the chapter; each relationship must still be tested. (Source: pp. 50–51)

## Key Takeaways

- Algorithmic-trading work should begin with a specific financial objective and a measurable target. (Source: p. 49)
- A complete problem definition specifies horizon, asset/market universe, regulatory and operational constraints, risk tolerance, and evaluation benchmarks. (Source: p. 49)
- Labels are outcomes to predict or optimize; features are candidate explanatory or predictive inputs. (Source: p. 49)
- An explicit hypothesis connects features to the target and focuses later data collection and feature engineering. (Source: p. 49)
- The same definition framework applies across distinct trading tasks, but each task requires different targets, features, horizons, constraints, and benchmarks. (Source: pp. 50–51)

## Glossary

| Term | Definition | Source |
|---|---|---|
| Financial objective | The specific financial result an algorithm is intended to achieve. | p. 49 |
| Target variable | The measurable quantity to predict or optimize; also called a label or dependent variable. | p. 49 |
| Label | Another term for the target or dependent variable. | p. 49 |
| Feature | A potential predictor used to explain or predict the target; also called a factor or independent variable. | p. 49 |
| Factor | Another term used for a feature or independent variable. | p. 49 |
| Independent variable | A predictor supplied to a model, contrasted with the dependent target variable. | p. 49 |
| Dependent variable | The outcome or target whose behavior is to be predicted or optimized. | p. 49 |
| Moving average (MA) | A technical indicator proposed as a feature in the equity-forecasting case. | p. 50 |
| Relative Strength Index (RSI) | A technical indicator proposed as a forecasting feature. | p. 50 |
| Bollinger Bands | A technical indicator proposed as a forecasting feature. | p. 50 |
| Sharpe ratio | An example of a portfolio risk-adjusted-return target. | p. 50 |
| Value at risk (VaR) | A portfolio risk metric proposed as a feature in adaptive rebalancing. | p. 51 |
| Volume-weighted average price (VWAP) | A price benchmark weighted by trading volume, used here to assess execution-price improvement. | p. 51 |
| Time-weighted average price (TWAP) | A time-based execution benchmark proposed as an input/reference in the execution case. | p. 51 |
| Slippage | Historical execution-performance information proposed as a feature for the execution problem. | p. 51 |
| Market impact | The effect of order execution on market prices; a cost the execution problem seeks to minimize. | p. 51 |
| Reinforcement learning | The algorithmic approach proposed for learning order placement and timing decisions in the execution case. | p. 51 |

## Connections to Other Chapters

- The chapter explicitly positions problem definition as guidance for later **data collection** and **feature engineering**. (Source: p. 49)
- Its repeated sequence of objective, target, scope, features, and hypothesis establishes inputs likely needed by later modeling and evaluation steps, although no chapter numbers are named. (Source: pp. 49–51; connection inferred)

## Extraction Issues

- The XHTML was complete and readable, with print-page anchors for pages 49, 50, and 51.
- No equations, derivations, figures, or tables appear in the source chapter.
- The source calls the portfolio objective “maximizing risk-adjustment returns”; this extraction interprets the surrounding context as **risk-adjusted returns** without attributing an explicit correction to the source. (Source: p. 50)
- Several quantitative concepts—Sharpe ratio, VWAP, TWAP, VaR, and price improvement—are named but not mathematically defined in this chapter; no external formulas were added.
