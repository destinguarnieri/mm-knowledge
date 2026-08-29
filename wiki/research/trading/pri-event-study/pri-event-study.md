# PRI Event Study Research

Status: in progress — measurement reset

Related process: [[research/trading/research_process_v2|Research Process V2]]  
Source glossary: [[trading/catalog_v1|Trading Catalog]]  
Catalog work inventory: [[research/trading/catalog_queue|Trading Catalog Implementation and Evaluation Queue]]  
Linear: [Price Reversal System Research](https://linear.app/money-machine/project/price-reversal-system-research-1b1579ea6126) · [MON-226](https://linear.app/money-machine/issue/MON-226/validate-pri-and-run-the-initial-prb-censored-event-study)

## Active scope

PRI is a closed-bar reversal signal. The PRI candle open is the primary Price Reversal Level (PRL); its directional extreme is a secondary level. A strict adverse close through the primary PRL is a Price Reversal Breaker (PRB). PRL targeting, PRZ behavior, position management, execution, costs, and combined-system trading rules are separate work.

The active diagnostic is deliberately minimal:

- Binance USD-M perpetuals from reviewed 60-contract plan `6ae6ecf0-9f9a-41dc-9a50-aecc56891454`.
- One timeframe per run; `5m` is first.
- PRI event direction adapted into the existing forward-return package.
- Exact signal-close to future-close horizons `H1–H6`, `H12`, and `H24`.
- No episode, PRB, or later-PRI censoring in this diagnostic.
- Only the existing package outputs: `horizon`, `spearman_ic`, `abs_spearman_ic`, `pearson`, `hit_rate`, `expectancy`, and `n_samples`, plus its ordinary run metadata.
- Development evidence only. Replication and holdout remain sealed.

This diagnostic answers only whether signed PRI events contain forward close-return information. It is not expected trade return and does not define a trading strategy. Any backtest will begin from newly confirmed trade rules rather than reconstructing them from earlier event-study measurements.

## Quarantine boundary

The earlier PRI fixed-return probability surface, episode MFE/MAE suite, and ordered first-passage studies are superseded measurement designs. Destin determined that their primary outputs do not measure the decisions he cares about. They must not be treated as active PRI evidence, optimization targets, or priors for a new backtest.

Their historical page is retained outside the indexed wiki at `archive/research/trading/pri-event-study/pri-event-study-2026-08-19.md`, and raw artifacts remain in the ignored `.research/runs/` store for audit only.

## Next action

Canonical `5m` development run `808a5d98-e522-45d0-b7c6-dc2572019c0f` is complete. It contains 60 reviewed assets × 8 horizons = 480 package-native result rows, only the `5m` interval, no nonfinite CSV values, and three checksum-verified artifacts. Inspect this diagnostic and decide whether it supplies a useful signal sanity check. If strategy testing proceeds, elicit the entry, target, scale-out, invalidation, and exit rules from a blank page before implementing a backtest.
