# MEGA Rolling Walk-Forward + Deflated Sharpe + Bootstrap-FDR — Overnight Audit

- Generated: `2026-06-03T16:29:57.425754+00:00`
- Runtime: `2.1s` (0.0 min) with `2` worker processes
- Symbols: 17 | Timeframes: ['15m', '1h', '2h', '4h', '1D']
- Strategies: 43 (11 prototyped + 6 generic patterns)
- Param sets total across grids: **64**
- Total (strategy, symbol, tf) jobs: **1**
- Cost: `8.0 bps` round-trip | Lockbox: last 25% | Rolling folds: 3
- Classification counts: `{'FAIL': 1}`
- PASS configurations: **0**
- Bootstrap-FDR family size (testable lockboxes): **1** | BH q=0.10 | threshold p≤0.00000
- BH-FDR survivors: **0** | DSR-robust (p≥0.95): **0**
- **FINAL ROBUST (PASS ∧ BH-FDR ∧ DSR): 0**

## Methodology note

Three independent gates must ALL pass for `robust_final`:
1. **Rolling walk-forward** — best param chosen on train folds; profitable on a 25% locked-box OOS slice never seen in selection; positive in ≥ half of forward folds.
2. **Bootstrap significance** — 2000-resample one-sided bootstrap that lockbox mean-R > 0, then **Benjamini-Hochberg FDR (q=0.10)** across ALL testable cells to control multiple-testing.
3. **Deflated Sharpe Ratio** — Bailey & López de Prado, per-trade Sharpe deflated by the expected max across the grid's parameter trials; p ≥ 0.95.

## FINAL ROBUST Survivors (all three gates)

| Strategy | Symbol | TF | Best Params | Lockbox Ret % | Sharpe | Boot p | DSR p | Trades | PF | Max DD % | Folds+ | Class |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| _(none survived all three gates)_ | | | | | | | | | | | | |

## Bootstrap-FDR Survivors (gate 1+2, DSR aside)

| Strategy | Sym | TF | Lockbox Ret % | Sharpe | Boot p | DSR p | Trades | PF | Folds+ | Class |
|---|---|---|---|---|---|---|---|---|---|---|

## All PASS / STRONG_PASS (no multiplicity filter)

| Strategy | Sym | TF | Lockbox Ret % | Sharpe | Boot p | DSR p | Trades | PF | MaxDD % | Folds+ | Class |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Per-Strategy Top 3 PASS configurations

