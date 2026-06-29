# Hyperliquid API Weightings

> Vendor reference for exchange/API limits that affect Money Machine market snapshots, monitoring, research, and future exchange integrations.
>
> Last checked: 2026-06-27
>
> Sources:
> - Hyperliquid docs — Rate limits and user limits: https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits.md
> - Hyperliquid docs — Info endpoint / candle snapshot: https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint.md

## Why this matters

Market-wide technical snapshots can get expensive fast. For `Monitoring → Markets`, use this file when sizing refresh cadence, polling behavior, concurrency, and cache TTLs.

Do **not** build all-asset technical refreshes as one blocking request. Use an accepted-job + polling flow and render the latest cached/partial snapshot while refresh work continues.

## REST/IP limits

Hyperliquid documents these IP-level limits:

| Limit | Value |
| --- | ---: |
| Aggregated REST weight budget | `1200 weight / minute` |
| Websocket connections | `10 max` |
| New websocket connections | `30 / minute` |
| Websocket subscriptions | `1000 max` |
| Unique users across user-specific websocket subscriptions | `10 max` |
| Messages sent to Hyperliquid over websockets | `2000 / minute` |
| Simultaneous inflight websocket post messages | `100 max` |
| HyperEVM JSON-RPC requests to `rpc.hyperliquid.xyz/evm` | `100 / minute` |

## REST request weights

| Request class | Weight |
| --- | ---: |
| Documented `exchange` API requests | `1 + floor(batch_length / 40)` |
| Unbatched exchange action | `1` |
| Batched exchange action with length `79` | `2` |
| `info` requests: `l2Book`, `allMids`, `clearinghouseState`, `orderStatus`, `spotClearinghouseState`, `exchangeStatus` | `2` |
| `info` request: `userRole` | `60` |
| All other documented `info` requests | `20` |
| Explorer API requests | `40` |

Some `info` endpoints have additional response-size weight. See the docs before using user-history/fills/funding/TWAP/delegator endpoints at scale.

## `candleSnapshot` weight

`candleSnapshot` is a documented `info` request, so use:

```txt
base documented info weight = 20
additional candleSnapshot weight = per 60 items returned
```

Conservative planning formula:

```txt
candle_snapshot_weight ~= 20 + ceil(returned_candles / 60)
```

Notes:

- The docs say additional weight is "per 60 items returned". Use `ceil` for safety when estimating.
- Only the most recent `5000` candles are available.
- Supported intervals include: `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1M`.

## Planning examples for Markets snapshots

For `MON-90 — Trend breadth vs 200D and 200x4H`, each asset needs two candle snapshots:

1. `1d` interval, about `200` candles
2. `4h` interval, about `200` candles

Estimated per snapshot:

```txt
20 + ceil(200 / 60) = 24 weight
```

If the universe has about `230` perp assets:

```txt
230 assets × 2 snapshots/asset × 24 weight = 11,040 weight
```

At the theoretical max budget:

```txt
11,040 / 1,200 ~= 9.2 minutes minimum
```

At a safer 50% budget:

```txt
11,040 / 600 ~= 18.4 minutes
```

## Recommended Money Machine policy

For all-asset technical references such as 200D / 200x4H:

- Filter out inactive assets before scheduling candle snapshots. In Money Machine, treat assets with both zero/missing open interest and zero/missing 24h notional volume as inactive for market breadth work.
- Use an async refresh job, not a blocking request.
- Accept the request immediately with a `run_id`.
- Poll job status from the frontend.
- Keep and display the latest completed/partial snapshot while refreshing.
- Start with one candle snapshot request at a time.
- Use conservative pacing: about `1 request / 2 seconds` for initial implementation.
- Track and expose progress:
  - requested assets
  - completed assets
  - failed assets
  - current asset
  - estimated remaining time
  - started/finished timestamps
  - stale/partial flags

Pacing estimate:

```txt
1 request / 2 seconds = 30 requests / minute
30 × 24 weight ~= 720 weight / minute
```

This leaves headroom under the documented `1200 weight / minute` REST budget for other app activity.

## Relevant repo surfaces

Existing code to reuse or inspect:

- `backend/app/clients/hyperliquid_client.py`
  - `HyperliquidClient.create_candle_snapshot_fetcher(...)`
  - `HyperliquidClient.fetch_candles_snapshot(...)`
  - `CandleSnapshotFetcher`
- `frontend/src/routes/_layout/backtest.tsx`
  - accepted-run + polling pattern for batch backtests
- `backend/app/api/routes/backtest.py`
  - backend accepted/status route pattern for longer work

## Safety note

This document is for read-only vendor/API behavior. It does not authorize live trading, account mutation, order placement/cancellation, deployment, or strategy lifecycle changes.
