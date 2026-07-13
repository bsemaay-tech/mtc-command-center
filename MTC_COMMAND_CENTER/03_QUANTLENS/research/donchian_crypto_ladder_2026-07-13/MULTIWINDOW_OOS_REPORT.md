# Multi-Window OOS + Parameter-Stability Report

- Candidates analysed: 0 (top PASS by bootstrap-FDR / boot_p)
- Windows: Q1(0-25%) Q2(25-50%) Q3(50-75%) Q4(75-100%=lockbox) H2(50-100%)
- A config is **REGIME-ROBUST** if positive return in >=3 of 5 windows with >=15 trades each.
- A config is **PARAM-STABLE** if >=70% of +/-step neighbors keep positive lockbox return.

## Per-Candidate Robustness

| Strategy | Sym | TF | Params | Q1 | Q2 | Q3 | Q4 | H2 | Win+/5 | Regime? | Param-Stable? |
|---|---|---|---|---|---|---|---|---|---|---|---|

## REGIME-ROBUST + PARAM-STABLE (cross-window survivors)

_(No candidate is both regime-robust across windows AND parameter-stable.)_

