# Hyperliquid portfolio margin — reconstructed account model

Status: in progress

Recorded: 2026-09-08. Account-specific reconstruction; empirical rules retain the scope and limitations below. Saved snapshots are historical, not current balances.

## Quick mental model

**Net Balance = settled net USDC equity + unrealized perp PnL.** For an independent API reconstruction, use the signed quote ledger plus signed marked position values, then subtract the outstanding USDC loan.

**Available Balance = Net Balance + collateral borrowing capacity − isolated allocated equity − cross initial margin − entry-order reservation.** Net Balance already includes the debt deduction; do not subtract the loan again from collateral capacity in this equation.

HYPE borrowing capacity uses quantity × borrowing oracle × LTV. Isolated profit raises both net balance and isolated allocated equity, so those two changes cancel in available balance. The observed order reservation includes a 1% buffer on order margin. Available Balance is neither portfolio market value nor an unconditional withdrawal amount.

Related: [[vendors/hyperliquid-api-weightings|Hyperliquid API Weightings]].

## Saved model and evidence

The complete Python model and its adjacent input files are archived under `raw/vendors/hyperliquid-portfolio-margin/2026-09-08/`. Run `python3 portfolio_margin_model.py` there to replay saved inputs, or add `--live` for a fresh read-only API capture. The model checks its supported account configuration and reports reconciliation residuals.

This model reconstructs the supplied wallet's net balance, available balance, HYPE encumbrance, maintenance cushion and PMR from separate API inputs. It does not use `spot.total` or `spot.hold` to calculate the predicted balances: those fields are used afterward as checks.

Nine independently priced snapshots were checked, covering September 7 at 11:42:59 p.m. through September 8 at 12:19:59 a.m. Eastern. The maximum available-balance error was 0.000001879 USDC. All 243 component and aggregate checks passed their stated tolerances. A tenth, fresh end-to-end REST run at September 8, 12:25:36 a.m. Eastern also passed all checks; its available-balance residual was −0.0000018544 USDC. See [live snapshot](../../raw/vendors/hyperliquid-portfolio-margin/2026-09-08/portfolio-margin-live.json) and [live results](../../raw/vendors/hyperliquid-portfolio-margin/2026-09-08/portfolio-margin-live-results.json) for that separate run. The 1% order-margin buffer and maintenance reconstruction are empirical results for the observed configuration, not a claim that unpublished branches have been reproduced.

The account has HYPE collateral, USDC debt, native USDC perps, 14 isolated positions and four cross positions. In the main example there are 77 resting entry orders, all adding to existing positions, and 19 untriggered reduce-only protective orders. Other enumerated DEXs had no positions. Spot holdings with zero LTV do not contribute borrowing capacity.

## The complete balance equation

Let:

- `E` = net USDC equity, including perp PnL and after borrowing liabilities.
- `C` = eligible collateral's gross borrowing capacity.
- `I` = equity tied to isolated positions, including their PnL.
- `M` = cross initial-margin requirement.
- `O` = initial margin for the observed resting entry orders.
- `buffer_rate` = 0.01, empirically verified on these orders.

```python
order_reservation = O * (1 + buffer_rate)
available_balance = E + C - I - M - order_reservation
hold = I + M + order_reservation - C
```

This explains the UI shortcut `available = total - hold`: the API `hold` is itself a net requirement after collateral credit. It is not necessarily the sum of the position margins and need not always be a positive amount. Do not clamp displayed USDC hold/available to zero when reproducing the balance table.

### The actual example at September 8, 12:19:30 a.m. Eastern

| Component | USDC |
|---|---:|
| Net USDC equity, E | 3,440.00649873 |
| HYPE gross borrowing capacity, C | 5,464.71482017 |
| Isolated equity, I | −5,062.72650600 |
| Cross initial margin, M | −1,072.67120400 |
| Entry-order initial margin, O | −977.94340997 |
| Additional 1% of order margin | −9.77943410 |
| Calculated available balance | **1,781.60076484** |
| API available balance | **1,781.60076499** |

The corresponding reconstructed hold is 1,658.40573389 USDC; the API returns 1,658.40573375. These are independently computed values, with sub-micro-USDC differences from precision/near-snapshot timing.

## Net balance from position accounting

The native perp API returns a signed quote-ledger balance, `marginSummary.totalRawUsd`. It includes the quote legs of positions and loan-funded balances. It can be negative and is not cash available to withdraw.

```python
signed_marked_position_value = sum(
    position.position_value if position.size > 0
    else -position.position_value
    for position in positions
)

gross_marked_usdc_equity = raw_quote_balance + signed_marked_position_value
net_balance = gross_marked_usdc_equity - borrowed_usdc
```

The main example gives:

| Component | USDC |
|---|---:|
| Signed quote ledger | −19,045.26005200 |
| Signed marked position value | +26,170.21582900 |
| Gross marked equity | 7,124.95577700 |
| Borrow liability | −3,684.94927827 |
| Net USDC equity | **3,440.00649873** |

The API spot `total` is 3,440.00649874. This is why debt is subtracted in this reconstruction but must not be subtracted again when starting from the spot `total` field.

The equally useful economic form is:

```python
net_balance = settled_net_equity + unrealized_perp_pnl
```

Here those components are 1,660.01058773 + 1,779.99591100. The settled figure is accumulated account equity after realized transactions and costs; it is not the original deposit or free cash. Deriving it as net minus PnL is a decomposition, not an independent lifetime-ledger audit.

### How net balance evolves

```python
ending_net_balance = (
    starting_net_balance
    + deposits_minus_withdrawals_and_external_transfers
    + net_spot_usdc_cash_flow
    + realized_perp_pnl
    - trading_fees
    + signed_funding_payments
    + supply_interest
    - borrow_interest
    + ending_unrealized_pnl
    - starting_unrealized_pnl
)
```

Borrow origination increases assets and liabilities together; repayment decreases both. Neither is an independent increase/decrease in net wealth. Borrow interest is an expense. Internal isolated/cross margin transfers do not create account wealth. Fill `fee` already includes `builderFee`; subtracting both would double-count the builder fee.

A separate historical replay from 11:42:59 p.m. to 12:15:57 a.m. used five fills, funding records, interest records, and a checked empty external-transfer interval:

| Change | USDC |
|---|---:|
| Starting net equity | 3,548.06735339 |
| Realized perp PnL | −3.09000000 |
| Trading fees | −0.53484500 |
| Signed funding | −0.12503000 |
| Posted borrow interest | −0.02048944 |
| Change in unrealized PnL | −152.31196200 |
| Predicted ending equity | **3,391.98502695** |
| API ending equity | **3,391.98493423** |

The remaining −0.00009272 USDC is left explicitly unattributed. This replay uses posted hourly interest and separate endpoint snapshots; it is not a reconstruction of every intra-hour accrual or a lifetime ledger. It establishes the economic equation to well below one cent without assigning a residual to an invented cause.

## Position and order requirements

For each cross position in the tested first-tier regime:

```python
notional = abs(size) * mark_price
cross_initial_margin = notional / selected_leverage
cross_maintenance_margin = notional / (2 * maximum_leverage)
```

Selected leverage controls initial margin. Maximum permitted leverage determines the maintenance fraction; these are distinct inputs. Higher tiers require maintenance deductions to preserve continuity and are rejected by the included personal model rather than guessed.

For an isolated position:

```python
isolated_equity = isolated_raw_quote_balance + signed_marked_position_value
```

That reproduces the API position `marginUsed`, including isolated PnL, transfers, fees and funding already incorporated in its raw balance. Using `notional / selected_leverage` for an existing isolated position does not reproduce its actual allocated equity.

For each of the observed entry orders:

```python
order_initial_margin = remaining_order_size * limit_price / selected_leverage
order_reservation = order_initial_margin * (1 + order_margin_buffer_rate)
```

The 1% is applied to the margin requirement, not to trade notional and not as a claim about the trading fee. The 19 untriggered reduce-only protective orders contributed no reservation in this reconstruction. The script rejects untested opposing/flip orders, spot orders, orders without an existing position, and entry triggers; simple summation cannot be assumed for every possible order configuration.

## Borrow capacity is gross; the loan is a separate state variable

```python
borrow_capacity = hype_quantity * hype_borrow_oracle * hype_ltv
borrow_headroom = borrow_capacity - borrowed_usdc
borrow_health_factor = borrow_capacity / borrowed_usdc
```

The example uses 100.04466674 HYPE × 84.035 USDC/HYPE × 0.65. These are independent API inputs. The borrowing oracle differs from the perp mark in the same capture; substituting the latter caused measurable reconciliation errors.

Net equity is already after debt. Therefore the full available equation adds gross borrowing capacity, not gross capacity minus debt again.

An equivalent form shows why available balance differs from simple borrow headroom:

```python
free_quote_after_unbuffered_orders = (
    gross_marked_usdc_equity - isolated_equity
    - cross_initial_margin - open_order_initial_margin
)

available_balance = (
    borrow_headroom + free_quote_after_unbuffered_orders - order_buffer
)
```

For the example: 1,779.76554190 + 11.61465703 − 9.77943410 = 1,781.60076484 USDC. Actual outstanding borrowing is a path-dependent liability with interest and automatic borrow/repayment events. It should not be replaced by a current minimal-funding estimate. During the short stream, debt mostly accrued interest while the free quote remainder moved with market prices.

Borrow caps, supply caps and global lendable liquidity can limit the usable credit. The observed account is in the unconstrained branch. The code rejects exhausted caps, depleted liquidity, other supplied settlement assets, other debt tokens, and partially supplied collateral. It does not claim a universal formula for those branches.

## HYPE held and available

For this one-collateral configuration:

```python
required_collateral_credit = max(
    0,
    isolated_equity + cross_initial_margin + order_reservation - net_balance,
)
hype_held = required_collateral_credit / (hype_borrow_oracle * hype_ltv)
hype_available = hype_quantity - hype_held
```

The example reconstructs **67.42820629 HYPE held** and **32.61646045 HYPE available**, matching the API within token precision. Borrowed USDC alone is not enough to reconstruct HYPE held; other quote equity and order reservations matter.

## Maintenance and portfolio margin ratio

This account's maintenance calculation excludes open orders and uses cross maintenance margin instead of cross initial margin. Isolated equity remains allocated to isolated positions. Define:

```python
cross_net_equity = net_balance - isolated_equity
liquidation_weight = (1 + hype_ltv) / 2
liquidation_collateral_value = hype_quantity * hype_borrow_oracle * liquidation_weight

available_after_maintenance = (
    cross_net_equity + liquidation_collateral_value - cross_maintenance_margin
)
```

The HYPE liquidation weight is 82.5%, versus borrowing LTV of 65%. The example produces **4,776.92858556 USDC available after maintenance**, which is a different constraint from 1,781.60076484 USDC available balance.

In all captured snapshots, cross net equity was negative and cross maintenance margin exceeded the documented small-borrow offset. In this tested regime the following reconstructs PMR:

```python
maintenance_borrow = cross_maintenance_margin - cross_net_equity

portfolio_margin_ratio = (
    cross_maintenance_margin + maintenance_borrow
) / (
    liquidation_collateral_value + cross_maintenance_margin
)
```

The example gives **36.071679%**, reproducing the returned PMR. `maintenance_borrow` is a risk-accounting quantity, not the current outstanding loan: in the example it is 2,159.05560927 USDC versus 3,684.94927827 actually borrowed. This distinction is why simply inserting the current loan into a guessed PMR formula failed.

This particular simplification is empirically supported, not a universal replacement for the documented max-over-borrowable-tokens calculation. The official formula mentions a 20-USDC minimum borrow offset and uses incompletely defined portfolio-balance terms. The script rejects small-maintenance and nonnegative-cross-equity regimes instead of silently deciding how that offset works there. Isolated positions retain their own liquidation constraints even when aggregate PMR is low.

## The different available fields

| Field | Meaning in the reconstructed account |
|---|---|
| Net Balance | Net USDC equity, including perp PnL |
| Available Balance | Collateral-supported margin headroom after positions and buffered orders |
| Borrow headroom | Collateral credit capacity less outstanding debt |
| Available after maintenance | Cross equity plus liquidation-weighted collateral less cross maintenance |
| `total - spotHold` | Separate spot-balance calculation used by the frontend; zero USDC in the main example |
| Available to Trade | Market- and side-specific output from `activeAssetData`, affected by closing/flipping existing exposure and size precision |

`activeAssetData` returns separate buy and sell limits. In the main capture HYPE's reported values were 3,273.416464 USDC for buy and 1,791.358821 for sell, while the balance-table value was 1,781.60076499. The returned trading amounts match maximum trade size × mark / selected leverage at displayed precision. Their maximum-size engine is a separate calculation; the frontend reads it from the API. The included model deliberately does not turn the table balance into an invented universal maximum trade size or withdrawal amount.

## Consequences for a personal interface

- An isolated position's unrealized profit increases net equity and isolated allocated equity by the same amount, so those contributions cancel in available balance. It is not automatically fresh cross-margin buying power.
- Cross PnL affects available balance, alongside changes in the position's initial-margin requirement.
- New resting entry orders reduce availability before any fill; canceling them releases the applicable reservation without creating profit.
- Moving margin into an isolated position lowers available balance without changing account net equity.
- The HYPE short partially offsets spot exposure, but collateral credit, directional equity and maintenance use different coefficients. A hedge does not mean their displayed numbers stay constant together.
- HYPE and other spot value belong in portfolio valuation, but only eligible weighted collateral belongs in borrowing capacity. The same asset should not be counted twice as spot value and loan-funded equity.
- Use Decimal and stable token/market IDs; spot contexts must be joined by market name, not array position. Keep source timestamps and show reconciliation residuals if data arrive from different blocks.

## Sources and reproduction

- [Python model](../../raw/vendors/hyperliquid-portfolio-margin/2026-09-08/portfolio_margin_model.py): default replay of the nine included snapshots; `--live` reads fresh public API data. No signing or trading.
- [Snapshot inputs](../../raw/vendors/hyperliquid-portfolio-margin/2026-09-08/portfolio-margin-snapshots.json), [calculated results](../../raw/vendors/hyperliquid-portfolio-margin/2026-09-08/portfolio-margin-results.json), and [historical net-equity replay](../../raw/vendors/hyperliquid-portfolio-margin/2026-09-08/net-balance-replay.json).
- [Official margin rules](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/margining).
- [Official portfolio margin rules](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/portfolio-margin).
- [Official PM terminology](https://hyperliquid.gitbook.io/hyperliquid-docs/support/faq/portfolio-margin).
- [Official websocket subscriptions](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket/subscriptions).
- [Frontend module inspected](https://app.hyperliquid.xyz/assets/config-72WzckHq.js): balance-field mappings, `spotHold` distinction, borrowing-capacity calculation and market-specific trading-data consumption. The reconstructed server-side buffer/maintenance rules are supported by saved API comparisons, not attributed to nonexistent frontend source.
