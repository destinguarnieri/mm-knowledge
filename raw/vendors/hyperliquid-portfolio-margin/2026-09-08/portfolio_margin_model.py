"""Explain this wallet's Hyperliquid PM balances from their components.

Read-only. Default: replay the included independently captured API snapshots.
Use --live to fetch a new snapshot; REST responses are not atomic, so inspect
reconciliation residuals before relying on the result.

Validated scope: HYPE-only eligible collateral, USDC debt and native USDC perps,
cross positions within their first maintenance tiers, and resting orders which
add to existing positions. No cross-DEX positions, other collateral, or spot
orders. These restrictions are checked instead of silently generalizing.

The 1% order-margin buffer and PMR reconstruction are empirically verified for
the captured account, not a claim to reproduce all unpublished engine branches.
"""
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from urllib.request import Request, urlopen

D = Decimal
ZERO = D('0')
ONE = D('1')
TWO = D('2')
ORDER_MARGIN_BUFFER_RATE = D('0.01')  # Observed: buffer is 1% of order margin.
DOCUMENTED_MIN_BORROW_OFFSET = D('20')
USD_TOLERANCE = D('0.0001')
RATIO_TOLERANCE = D('0.000000001')
TOKEN_TOLERANCE = D('0.0000001')
API_URL = 'https://api.hyperliquid.xyz/info'
WALLET = '0x7c80d61F16A216b62Cce8719A8355543055456B7'


def info(body):
    request = Request(API_URL, data=json.dumps(body).encode(),
                      headers={'Content-Type': 'application/json'})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def roll_forward_net_balance(*, starting_net_balance, starting_unrealized_pnl,
                             ending_unrealized_pnl, net_external_transfers,
                             spot_cash_flow, realized_perp_pnl, trading_fees,
                             funding_received, supply_interest, borrow_interest):
    """Economic ledger equation. All arguments are Decimal amounts in USDC.

    funding_received is signed; trading_fees may be negative for rebates.
    Fees include builder fees already included in each fill's fee field.
    Borrow originations/repayments are deliberately absent: they change the
    asset and liability together. Borrow INTEREST does reduce net equity.
    Isolated/cross internal allocations are not external account cash flows.
    """
    return (starting_net_balance
            + net_external_transfers + spot_cash_flow
            + realized_perp_pnl - trading_fees + funding_received
            + supply_interest - borrow_interest
            + ending_unrealized_pnl - starting_unrealized_pnl)


def fetch_snapshot(wallet):
    jobs = {
        'spot': {'type': 'spotClearinghouseState', 'user': wallet},
        'perps': {'type': 'clearinghouseState', 'user': wallet},
        'orders': {'type': 'frontendOpenOrders', 'user': wallet},
        'reserves': {'type': 'allBorrowLendReserveStates'},
        'dexs': {'type': 'perpDexs'},
        'meta': {'type': 'meta'},
    }
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = dict(zip(jobs, pool.map(info, jobs.values())))
    names = [dex['name'] for dex in results.pop('dexs') if dex]
    jobs = [(dex, kind) for dex in names
            for kind in ('clearinghouseState', 'frontendOpenOrders')]
    with ThreadPoolExecutor(max_workers=4) as pool:
        values = list(pool.map(info, [
            {'type': kind, 'user': wallet, 'dex': dex} for dex, kind in jobs
        ]))
    for (dex, kind), value in zip(jobs, values):
        active = value['assetPositions'] if kind == 'clearinghouseState' else value
        if active:
            raise ValueError(f'Unsupported cross-DEX exposure/orders: {dex}')
    results['received_at'] = datetime.now(timezone.utc).isoformat()
    results['other_dexs_checked'] = names
    results['atomic'] = False
    return results


def calculate(snapshot):
    spot = snapshot['spot']
    perps = snapshot['perps']
    orders = snapshot['orders']
    reserves = dict(snapshot['reserves'])
    balances = {row['coin']: row for row in spot['balances']}
    positions = {row['position']['coin']: row['position']
                 for row in perps['assetPositions']}
    if not spot.get('portfolioMarginEnabled'):
        raise ValueError('Portfolio margin mode is required.')
    if snapshot.get('other_dexs_active'):
        raise ValueError('Unsupported cross-DEX exposure.')
    for row in spot['balances']:
        if row['coin'] != 'USDC' and D(row.get('borrowed', '0')) != ZERO:
            raise ValueError('Model currently supports USDC debt only.')
        if row['coin'] != 'HYPE' and D(row.get('ltv', '0')) > ZERO and D(row['total']) != ZERO:
            raise ValueError('Model currently supports HYPE collateral only.')
        if row['coin'] != 'USDC' and D(row.get('supplied', '0')) > ZERO and D(row.get('ltv', '0')) == ZERO:
            raise ValueError('Other supplied settlement assets need separate accounting.')
    usdc, hype = balances['USDC'], balances['HYPE']
    if D(usdc.get('supplied', '0')) != ZERO:
        raise ValueError('The supplied-USDC branch has not been validated.')

    # NET EQUITY: reconstruct the marked account from its signed quote ledger.
    # rawUsd includes the quote legs of perpetual positions and loan proceeds.
    # It is not a withdrawable cash balance and may be negative.
    raw_quote_balance = D(perps['marginSummary']['totalRawUsd'])
    signed_position_value = ZERO
    unrealized_pnl = ZERO
    cross_initial_margin = ZERO
    cross_maintenance_margin = ZERO
    isolated_equity = ZERO
    position_details = []
    meta_by_coin = {row['name']: row for row in snapshot['meta']['universe']}
    tables = dict(snapshot['meta'].get('marginTables', []))
    for coin, position in positions.items():
        size = D(position['szi'])
        notional = D(position['positionValue'])
        signed_value = notional if size > ZERO else -notional
        leverage = D(position['leverage']['value'])
        pnl = D(position['unrealizedPnl'])
        signed_position_value += signed_value
        unrealized_pnl += pnl
        if position['leverage']['type'] == 'cross':
            maximum_leverage = D(position['maxLeverage'])
            tiers = tables.get(meta_by_coin[coin].get('marginTableId'), {}).get('marginTiers', [])
            if len(tiers) > 1 and notional >= D(tiers[1]['lowerBound']):
                raise ValueError(f'{coin}: tiered maintenance needs a generalized model.')
            if leverage > maximum_leverage:
                raise ValueError(f'{coin}: selected leverage exceeds current tier maximum.')
            margin = notional / leverage
            cross_initial_margin += margin
            cross_maintenance_margin += notional / (TWO * maximum_leverage)
        else:
            # Isolated equity = assigned signed quote balance + marked position.
            margin = D(position['leverage']['rawUsd']) + signed_value
            isolated_equity += margin
        position_details.append({
            'coin': coin, 'mode': position['leverage']['type'],
            'size': size, 'notional': notional, 'unrealized_pnl': pnl,
            'calculated_margin': margin,
            'margin_residual': margin - D(position['marginUsed']),
        })
    borrowed_usdc = D(usdc.get('borrowed', '0'))
    gross_marked_equity = raw_quote_balance + signed_position_value
    net_balance = gross_marked_equity - borrowed_usdc
    settled_net_equity = net_balance - unrealized_pnl

    # OPEN ORDERS: the observed orders are all buys adding to existing longs.
    # Ignore untriggered reduce-only protective orders. Fail on untested shapes.
    open_order_initial_margin = ZERO
    order_details = []
    for order in orders:
        if order['isTrigger']:
            if not order['reduceOnly']:
                raise ValueError('Entry trigger orders require separate validation.')
            continue
        if order['reduceOnly']:
            raise ValueError('Resting reduce-only orders require separate validation.')
        if order['coin'] not in positions:
            raise ValueError('Need leverage/risk rules for an order without a position.')
        position = positions[order['coin']]
        if (D(position['szi']) > ZERO) != (order['side'] == 'B'):
            raise ValueError('Opposing/position-flipping orders require netting rules.')
        margin = D(order['sz']) * D(order['limitPx']) / D(position['leverage']['value'])
        open_order_initial_margin += margin
        order_details.append({'coin': order['coin'], 'oid': order['oid'], 'margin': margin})
    order_buffer = open_order_initial_margin * ORDER_MARGIN_BUFFER_RATE
    order_reservation = open_order_initial_margin + order_buffer

    # BORROWING CAPACITY: gross capacity, not capacity minus existing debt.
    # Debt has already been deducted in net_balance. Subtracting it here again
    # would double-count it.
    hype_quantity = D(hype['total'])
    hype_oracle_price = D(reserves[hype['token']]['oraclePx'])
    hype_ltv = D(reserves[hype['token']]['ltv'])
    if hype_quantity <= ZERO or hype_oracle_price <= ZERO or hype_ltv <= ZERO:
        raise ValueError('This model requires positive eligible HYPE collateral.')
    if hype.get('supplied') is None or D(hype['supplied']) != hype_quantity:
        raise ValueError('Only fully supplied HYPE collateral has been validated.')
    if borrowed_usdc <= ZERO:
        raise ValueError('The debt-free PM branch has not been validated.')
    hype_value = hype_quantity * hype_oracle_price
    borrow_capacity = hype_value * hype_ltv
    if D(reserves[usdc['token']]['balance']) <= borrow_capacity:
        raise ValueError('Global lendable-liquidity constraint requires a capped model.')
    if any(D(value) >= ONE for _, value in spot.get('tokenToPortfolioBorrowRatio', [])):
        raise ValueError('Borrow-cap branch has not been validated.')
    if any(D(value) >= ONE for _, value in spot.get('tokenToPortfolioSupplyRatio', [])):
        raise ValueError('Supply-cap branch has not been validated.')
    borrow_headroom = borrow_capacity - borrowed_usdc
    borrow_health_factor = borrow_capacity / borrowed_usdc

    # THE FULL AVAILABLE-BALANCE EQUATION.
    position_margin = isolated_equity + cross_initial_margin
    total_margin_commitment = position_margin + order_reservation
    hold = total_margin_commitment - borrow_capacity
    available_balance = net_balance + borrow_capacity - total_margin_commitment
    # No max(0, ...) on the displayed USDC available/hold values.

    # Equivalent equation makes the connection with outstanding debt visible.
    free_quote_after_unbuffered_orders = (
        gross_marked_equity - position_margin - open_order_initial_margin
    )
    alternative_available = (
        borrow_headroom + free_quote_after_unbuffered_orders - order_buffer
    )

    # HYPE collateral encumbrance in this one-collateral configuration.
    required_collateral_credit = max(ZERO, total_margin_commitment - net_balance)
    if required_collateral_credit > borrow_capacity:
        raise ValueError('Collateral-deficit branch needs separate validation.')
    hype_held = required_collateral_credit / (hype_oracle_price * hype_ltv)
    hype_available = hype_quantity - hype_held

    # MAINTENANCE: validated for this debt-bearing, cross-equity-deficit regime.
    cross_net_equity = net_balance - isolated_equity
    if cross_net_equity >= ZERO or cross_maintenance_margin <= DOCUMENTED_MIN_BORROW_OFFSET:
        raise ValueError('PMR branch outside the empirically validated regime.')
    liquidation_weight = (ONE + hype_ltv) / TWO
    liquidation_collateral_value = hype_value * liquidation_weight
    available_after_maintenance = (
        cross_net_equity + liquidation_collateral_value - cross_maintenance_margin
    )
    maintenance_borrow = cross_maintenance_margin - cross_net_equity
    portfolio_margin_ratio = (
        (cross_maintenance_margin + maintenance_borrow)
        / (liquidation_collateral_value + cross_maintenance_margin)
    )

    # All reported total/hold fields enter below, for comparison only.
    reported_net = D(usdc['total'])
    reported_available = reported_net - D(usdc['hold'])
    reported_after_maintenance = D(dict(spot['tokenToAvailableAfterMaintenance'])[usdc['token']])
    checks = {
        'net_balance': (net_balance - reported_net, USD_TOLERANCE),
        'available_balance': (available_balance - reported_available, USD_TOLERANCE),
        'hold': (hold - D(usdc['hold']), USD_TOLERANCE),
        'position_margin': (position_margin - D(perps['marginSummary']['totalMarginUsed']), USD_TOLERANCE),
        'cross_maintenance_margin': (cross_maintenance_margin - D(perps['crossMaintenanceMarginUsed']), USD_TOLERANCE),
        'hype_hold': (hype_held - D(hype['hold']), TOKEN_TOLERANCE),
        'available_after_maintenance': (available_after_maintenance - reported_after_maintenance, USD_TOLERANCE),
        'portfolio_margin_ratio': (portfolio_margin_ratio - D(spot['portfolioMarginRatio']), RATIO_TOLERANCE),
        'equivalent_available_equations': (available_balance - alternative_available, USD_TOLERANCE),
    }
    for row in position_details:
        checks['position_' + row['coin']] = (row['margin_residual'], USD_TOLERANCE)
    return {
        'received_at': snapshot['received_at'],
        'raw_quote_balance': raw_quote_balance,
        'signed_position_value': signed_position_value,
        'gross_marked_equity': gross_marked_equity,
        'borrowed_usdc': borrowed_usdc,
        'unrealized_pnl': unrealized_pnl,
        'settled_net_equity': settled_net_equity,
        'net_balance': net_balance,
        'hype_quantity': hype_quantity,
        'hype_oracle_price': hype_oracle_price,
        'hype_ltv': hype_ltv,
        'borrow_capacity': borrow_capacity,
        'borrow_headroom': borrow_headroom,
        'borrow_health_factor': borrow_health_factor,
        'isolated_equity': isolated_equity,
        'cross_initial_margin': cross_initial_margin,
        'position_margin': position_margin,
        'open_order_initial_margin': open_order_initial_margin,
        'order_buffer': order_buffer,
        'order_reservation': order_reservation,
        'total_margin_commitment': total_margin_commitment,
        'hold': hold,
        'available_balance': available_balance,
        'reported_available_balance': reported_available,
        'free_quote_after_unbuffered_orders': free_quote_after_unbuffered_orders,
        'hype_held': hype_held,
        'hype_available': hype_available,
        'cross_net_equity': cross_net_equity,
        'cross_maintenance_margin': cross_maintenance_margin,
        'liquidation_collateral_value': liquidation_collateral_value,
        'maintenance_borrow': maintenance_borrow,
        'available_after_maintenance': available_after_maintenance,
        'portfolio_margin_ratio': portfolio_margin_ratio,
        'positions': position_details,
        'orders': order_details,
        'checks': {name: {'residual': residual, 'tolerance': tolerance,
                          'passed': abs(residual) <= tolerance}
                   for name, (residual, tolerance) in checks.items()},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--wallet', default=WALLET)
    parser.add_argument('--snapshot', type=Path,
                        default=Path(__file__).with_name('portfolio-margin-snapshots.json'))
    args = parser.parse_args()
    if args.live:
        snapshots = [fetch_snapshot(args.wallet)]
        args.snapshot.with_name('portfolio-margin-live.json').write_text(json.dumps(snapshots, indent=2))
    else:
        snapshots = json.loads(args.snapshot.read_text())
    results = [calculate(snapshot) for snapshot in snapshots]
    for result in results:
        failed = [name for name, check in result['checks'].items() if not check['passed']]
        print(result['received_at'], 'MATCH' if not failed else 'MISMATCH',
              'net=', f"{result['net_balance']:.8f}",
              'available=', f"{result['available_balance']:.8f}",
              'residual=', result['checks']['available_balance']['residual'])
        if failed:
            print('Inspect data timing / unsupported branches:', ', '.join(failed))
    print('\nCOMPONENTS — first snapshot')
    for name, value in results[0].items():
        if isinstance(value, D):
            print(f'{name:38} {value:,.8f}')
    results_filename = ('portfolio-margin-live-results.json' if args.live
                        else 'portfolio-margin-results.json')
    Path(__file__).with_name(results_filename).write_text(
        json.dumps(results, indent=2, default=str))


if __name__ == '__main__':
    main()
