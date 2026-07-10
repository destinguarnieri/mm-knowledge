# Binance Market Data Access

> Vendor reference for global Binance public candle / market-data access, geo restrictions, klines schema, rate limits, and MM usage posture.
>
> Last checked: 2026-07-10
>
> Sources:
> - Binance Spot API docs — Market Data Only URLs: https://github.com/binance/binance-spot-api-docs/blob/master/faqs/market_data_only.md
> - Binance Spot REST API — general / market data / LIMITS: https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md
> - Binance Spot ENUM definitions — rate limiters: https://github.com/binance/binance-spot-api-docs/blob/master/enums.md
> - Binance USD-M Futures klines: https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data
> - Binance Terms — Eligibility / Restricted Location: https://www.binance.com/en/terms
> - Live probes from US residential IP (Florida), 2026-07-09 / 2026-07-10

## Scope

This page covers **global Binance** public market data (spot candles and related public endpoints), plus a short futures/perp klines note for research planning.

**Out of scope:** Binance.US. Do not use `api.binance.us` for MM research/backtest candle identity — different venue, books, pairs, and liquidity.

## Two hosts, same spot candle product

| Host | Role | Auth | From US IP (2026-07-09 probe) |
| --- | --- | --- | --- |
| `https://api.binance.com` | Main Spot API (public + private) | Public market data needs none | **451** restricted location |
| `https://data-api.binance.vision` | Official public market-data-only mirror | None | **200** — spot klines returned |

Both serve the **same global Binance spot candles** via:

```http
GET /api/v3/klines?symbol=BTCUSDT&interval=1m&limit=1000
```

You are choosing a front door, not a different market. Candle identity (symbol, open time, OHLCV) is the global Spot book.

Official market-data-only hosts:

- REST: `https://data-api.binance.vision`
- Websocket market streams: `wss://data-stream.binance.vision`

Documented public REST endpoints on `data-api.binance.vision` include: `ping`, `time`, `exchangeInfo`, `depth`, `trades`, `aggTrades`, `klines`, `uiKlines`, `avgPrice`, `ticker/*`.

## Spot candle API schema (`GET /api/v3/klines`)

Security: `NONE` (no API key). Data source: Database. Identity: klines are uniquely identified by **open time**.

### Request

| Param | Type | Required | Notes |
| --- | --- | --- | --- |
| `symbol` | STRING | YES | e.g. `BTCUSDT` |
| `interval` | ENUM | YES | case-sensitive; see intervals below |
| `startTime` | LONG | NO | ms UTC |
| `endTime` | LONG | NO | ms UTC |
| `timeZone` | STRING | NO | Default `0` (UTC). Hours/minutes like `-1:00`, `05:45`, or hours like `8`. Range `[-12:00, +14:00]`. Affects interval alignment only; `startTime`/`endTime` stay UTC. |
| `limit` | INT | NO | Default **500**; Maximum **1000** |

Supported intervals:

| Family | Values |
| --- | --- |
| seconds | `1s` |
| minutes | `1m`, `3m`, `5m`, `15m`, `30m` |
| hours | `1h`, `2h`, `4h`, `6h`, `8h`, `12h` |
| days | `1d`, `3d` |
| weeks | `1w` |
| months | `1M` |

Behavior notes:

- If `startTime` and `endTime` are omitted, the most recent klines are returned.
- One request returns at most **1000** bars. Longer history requires paging with `startTime`/`endTime` (or walk open times).
- Sibling endpoint `GET /api/v3/uiKlines` has the same params/response shape/weight; values are presentation-optimized for charts. Prefer `/klines` for research/backtest identity.

### Response

JSON array of arrays. Each candle has **12 fields**:

| Index | Field | Type | Meaning |
| ---: | --- | --- | --- |
| 0 | open time | LONG | ms |
| 1 | open | STRING | |
| 2 | high | STRING | |
| 3 | low | STRING | |
| 4 | close | STRING | |
| 5 | volume | STRING | base asset volume |
| 6 | close time | LONG | ms |
| 7 | quote asset volume | STRING | |
| 8 | number of trades | INT | |
| 9 | taker buy base asset volume | STRING | |
| 10 | taker buy quote asset volume | STRING | |
| 11 | ignore | STRING | unused; ignore |

Example (live `data-api.binance.vision`, 2026-07-10):

```json
[
  [
    1783657980000,
    "63911.20000000",
    "63970.00000000",
    "63900.55000000",
    "63970.00000000",
    "12.18816000",
    1783658039999,
    "779153.03834470",
    3298,
    "9.36084000",
    "598411.39726290",
    "0"
  ]
]
```

### Caps that matter for ingest

| Cap | Value |
| --- | --- |
| Max candles per request | **1000** |
| Default `limit` | 500 |
| Request weight (spot klines / uiKlines) | **2** (fixed; not scaled by `limit`) |
| Auth | none for public market data |

## Spot rate limits

Limits are **per IP**, not per API key. Live values come from `GET /api/v3/exchangeInfo` → `rateLimits` (also available on `data-api.binance.vision`).

Observed live on 2026-07-10 via vision host:

| `rateLimitType` | Interval | Limit |
| --- | --- | ---: |
| `REQUEST_WEIGHT` | 1 MINUTE | **6000** |
| `RAW_REQUESTS` | 5 MINUTE | **300000** |
| `ORDERS` | 10 SECOND | 100 |
| `ORDERS` | 1 DAY | 200000 |

For public candle pulls, the relevant budgets are **`REQUEST_WEIGHT`** and (secondarily) **`RAW_REQUESTS`**. `ORDERS` does not apply to klines.

### Headers

Successful responses include used-weight headers, e.g.:

- `X-MBX-USED-WEIGHT`
- `X-MBX-USED-WEIGHT-1M` (1-minute window)

Live klines probe returned `x-mbx-used-weight: 2` and `x-mbx-used-weight-1m: 2` after a `limit=2` call (matches documented weight 2).

### Breach / ban semantics

- Exceed limit → HTTP **429**; back off. `Retry-After` is seconds to wait to avoid a ban.
- Keep spamming after 429 → automated IP ban HTTP **418**. Ban duration scales **2 minutes → 3 days**.
- `Retry-After` on 418 is seconds until the ban ends.

### Planning math (spot)

```txt
klines_weight_per_call = 2
max_klines_calls_per_minute ≈ 6000 / 2 = 3000
max_candles_per_minute_at_full_pages ≈ 3000 * 1000 = 3_000_000
```

RAW_REQUESTS (300000 / 5 min) is far looser than weight for klines-only traffic; weight is the binding constraint.

Practical guidance: page at `limit=1000`, watch `X-MBX-USED-WEIGHT-1M`, and back off on 429. Do not treat the theoretical 3000 calls/min as a target.

## Geo / eligibility semantics

- Restriction is enforced primarily by **request IP geo**, not citizenship paperwork.
- Restricted locations (per Terms / observed API behavior) include the **United States** and other designated regions.
- From restricted IPs, main Spot/Futures hosts often return HTTP **451** with:

```json
{
  "code": 0,
  "msg": "Service unavailable from a restricted location according to 'b. Eligibility' in https://www.binance.com/en/terms. ..."
}
```

- A US person on a non-restricted server IP can often reach `api.binance.com`.
- A non-US person on a US cloud/residential IP often cannot.

## Futures / perps

| Host | Role | From US IP (2026-07-09 probe) |
| --- | --- | --- |
| `https://fapi.binance.com` | USD-M futures / perps API (incl. klines) | **451** |

`data-api.binance.vision` is **spot market-data only**. It does **not** replace futures/perp endpoints.

To pull Binance perp candles from a restricted location today, the request must egress from a non-restricted IP (VPN, non-US proxy, or non-US server region).

### Futures candle schema note (`GET /fapi/v1/klines`)

Same 12-field candle array shape as spot. Important differences vs spot:

| Item | Spot `/api/v3/klines` | Futures `/fapi/v1/klines` |
| --- | --- | --- |
| Max `limit` | 1000 | **1500** |
| Default `limit` | 500 | 500 |
| Weight | fixed **2** | **depends on `limit`** |

Futures request weight by `limit`:

| `limit` | Weight |
| --- | ---: |
| `[1, 100)` | 1 |
| `[100, 500)` | 2 |
| `[500, 1000]` | 5 |
| `> 1000` | 10 |

So `limit=1500` costs weight **10**. For bulk history, paging at **499** (weight 2) is often cheaper than max pages at weight 10.

Futures IP limits are also published via `fapi` `exchangeInfo` `rateLimits` (`REQUEST_WEIGHT`, `RAW_REQUEST`, `ORDERS`). Same 429 / 418 / `Retry-After` pattern as spot. Confirm live budgets from a non-restricted IP before sizing a research worker.

## Money Machine posture

### Backtesting and research immediacy (spot)

- Prefer **`https://data-api.binance.vision/api/v3/klines`** for global Binance spot candle snapshots from local/US machines.
- Same product as `api.binance.com` public klines; works without VPN for spot.

### Trading servers

- Live trading servers are in **Japan** → non-restricted egress for main Binance APIs is a non-issue for those hosts.

### Research backend / perps

- If research needs durable Binance **perp** history or live futures market data without VPN gymnastics, put the research backend (or at least the Binance fetch worker) in a non-restricted region such as **Japan**, aligned with trading egress.
- Local laptop: a VPN to a non-restricted region is a valid short-term way to hit `fapi.binance.com` for exploratory perp pulls. Prefer region-correct servers for anything automated or durable.

## Quick decision table

| Need | Use |
| --- | --- |
| Global spot candles from US/local | `data-api.binance.vision` `/api/v3/klines` |
| Global spot candles from Japan/trading servers | `api.binance.com` or `data-api.binance.vision` |
| Global futures/perp candles from US/local | Non-restricted egress (VPN or JP research worker) → `fapi.binance.com` |
| Binance.US candles | Do not use for MM global research identity |

## Verification notes (2026-07-09 / 2026-07-10)

Probed from US residential IP (`country: US`):

- `api.binance.com/api/v3/klines` → 451
- `api1.binance.com/api/v3/klines` → 451
- `fapi.binance.com/fapi/v1/klines` → 451
- `data-api.binance.vision/api/v3/klines` → 200 with BTCUSDT candle payload
- `data-api.binance.vision/api/v3/ping` → 200 `{}`
- `data-api.binance.vision/api/v3/klines?limit=2` → headers `x-mbx-used-weight: 2`, `x-mbx-used-weight-1m: 2`
- `data-api.binance.vision/api/v3/exchangeInfo?symbol=BTCUSDT` → `REQUEST_WEIGHT` 6000/1m, `RAW_REQUESTS` 300000/5m

## Safety

This document is for read-only vendor/API behavior and research/backtest data access planning. It does not authorize live trading, account mutation, order placement/cancellation, deployment, or strategy lifecycle changes. VPN use for personal exploratory market-data pulls is noted as an operational option; do not treat it as a production architecture.

## Related

- [[vendors/hyperliquid-api-weightings|Hyperliquid API Weightings]]
- [[index|Money Machine Knowledge Index]]
