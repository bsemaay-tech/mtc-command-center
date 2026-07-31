# FAZ 3B — Stage-2 Deferred Forward Confirmation Pre-Registration

> **Status: D016 APPROVED FOR SCOPE FREEZE AND PASSIVE DATA ACCRUAL ONLY.**
> Barış approved Path A on 2026-07-13: “yol a onaylıyorum sen işlemi yap.”
> This approval freezes the future-data design below. It does **not** authorize
> exit-aware tool changes, data download/ingestion, a runner, smoke test,
> backtest, CPCV, PBO, multi-window evaluation, paper trading, or live trading.
> Each of those remains separately approval-gated. Earliest possible evaluation:
> **2028-07-14**, after the complete fixed window closes and a new Gate-5 review.

## 1. Why this is a new pre-registration

The superseded 2026-07-13 Stage-2 draft is permanently blocked. Its six proposed
“held-out” symbols had already been evaluated by `GEN_KELTNER_BREAKOUT` at 1h
on the same 2020-07-27 through 2026-06-26 observations, its 12-set grid was
effective re-optimization, and the existing CPCV/multi-window/PBO path could not
score the requested exit correctly. The immutable record is:

- blocked draft: `FAZ3B_STAGE2_CONFIRM_PREREG_2026-07-13.md`;
- Codex findings: `11_TRIAGE/CODEX_GATE5_FINDINGS_FAZ3B_STAGE2_2026-07-13.md`;
- blocked banner commit: `f32a354c`.

This document does not repair or revive that draft. It defines a new temporal
holdout whose decision bars do not yet exist.

## 2. Frozen research question

Does the already-selected `GEN_KELTNER_BREAKOUT` 1h strategy at the already-
selected primary parameters `{ema_len: 50, atr_len: 10, mult: 2.0}` show an
incremental benefit from `trail_ema8` over `fixed_2R` on genuinely future US ETF
bars, across at least two predefined market-diversity groups?

- **H1 — exit incremental:** the trail passes the full forward bar while the
  fixed-2R twin does not, in at least one symbol from each of at least two groups.
- **H-pocket — strategy/timeframe pocket:** both modes pass; this supports the
  Keltner-1h family but not an incremental trail claim.
- **H0 — no forward confirmation:** the H1 condition is not met. The Stage-1 AAPL
  result remains research-only and this fixed forward window gets no second bite.

## 3. Frozen future window and data contract

| Field | Frozen value |
|---|---|
| Provider | Alpaca IEX, matching the canonical bundle's `alpaca_iex` convention |
| Adjustment | `alpaca_all` |
| Session | US regular trading hours only |
| Timeframe | 1h only |
| First scored session date | 2026-07-14 |
| Last scored session date | 2028-07-13 |
| Earliest ingestion/evaluation date | 2028-07-14 |
| Pre-window history | Exactly the last 250 complete 1h bars before 2026-07-14, indicator warm-up only; never scored, optimized, or counted as confirmation evidence |
| Costs | Engine convention: 8 bps round trip plus 2 bps per side slippage stress |
| Holding cap | 96 bars, unchanged |

The scored interval is fixed by session date, not by bar count, trade count,
market regime, profitability, or tool readiness. It will not be extended if it
is unfavorable or insufficient. Holidays and genuine provider outages remain
missing; no synthetic bars may be inserted. A provider/adjustment/session change
is a STOP event requiring a replacement pre-registration and fresh approval.

The audit suggested bars after 2026-06-26. This design begins on 2026-07-14 so
every scored bar is also later than the 2026-07-13 approval itself. The two-year
end date is fixed now to avoid optional stopping and to provide materially more
trade-density opportunity than a six-month window. Insufficient trades at the
fixed end date are a valid negative/inconclusive outcome, never a reason to wait
for more bars under this registration.

## 4. Frozen symbols and diversity groups

All six were present with PASS data validation at 1h in the historical canonical
manifest as of D016. Their historical rows are not held out; **only the future
2026-07-14 through 2028-07-13 interval is held out**.

| Group | Purpose | Frozen decision symbols |
|---|---|---|
| G1 — broad market | large-cap and small-cap market breadth | SPY, IWM |
| G2 — cyclical sectors | financial and energy cycle exposure | XLF, XLE |
| G3 — defensive sectors | health care and consumer staples exposure | XLV, XLP |

There are six decision symbols and three groups. No AAPL reference row is run.
There is no symbol reserve list. A missing, delisted, invalid, or contaminated
symbol is not replaced or dropped; it triggers STOP and a newly approved scope.
H1 requires qualifying EXIT-INCREMENTAL cells in at least two distinct groups;
two successes inside one group count as one group.

## 5. Frozen strategy, exits, and configurations

Strategy logic and entry math stay unchanged. The only compared exit modes are:

1. candidate: `trail_ema8`;
2. control: `fixed_2R`.

The primary decision configuration is fixed and is the only configuration that
can confirm or reject H1:

| Role | `ema_len` | `atr_len` | `mult` |
|---|---:|---:|---:|
| Primary decision | 50 | 10 | 2.0 |
| Diagnostic star only | 20 | 10 | 2.0 |
| Diagnostic star only | 50 | 20 | 2.0 |
| Diagnostic star only | 50 | 10 | 1.5 |
| Diagnostic star only | 50 | 10 | 2.5 |

The four star points are fixed sensitivity/PBO inputs. They cannot replace the
primary, select a new winner, rescue a failed primary, or become production
parameters. No Cartesian cross terms and no additional parameter values are
allowed. Future computation, if separately approved, therefore contains
`6 symbols × 2 exits × 5 configurations = 60` configuration evaluations, of
which only the 12 primary symbol/exit rows enter the decision-level BH family.
Every literal configuration must be persisted separately. An engine summary that
selects the best of five is not decision evidence; the primary row must be read
by exact parameter equality, while the other four rows remain diagnostic only.

## 6. Data firewall during accrual

Before the fixed window closes, nobody may run this strategy/exits/configuration
set on any portion of the scored interval or inspect derived signals, trades,
returns, Sharpe, drawdown, PBO, CPCV, or multi-window metrics from it. General
market observation is unavoidable and is not evidence; systematic strategy
evaluation is prohibited.

Passive passage of time is the only activity approved now. Data ingestion,
normalization, hashing, scoring, or a completeness probe against the future
window requires a later written approval. When eventually authorized, the first
allowed data action is a non-performance inventory that records provider,
adjustment/session policy, first/last timestamp, row count, missing intervals,
and file hashes without computing signals or returns.

## 7. Historical trial-family rule fixed now

`RESEARCH_RUN_REGISTRY.json` is not an evidence inventory. Before any future
metric is unblinded, an artifact ledger must recursively scan result JSONs under
both `03_QUANTLENS/05_BACKTEST_RESULTS/` and `03_QUANTLENS/research/`.

The DSR trial family includes every unique `GEN_KELTNER_BREAKOUT` configuration
evaluation whose metrics existed before D016 and could have influenced selection,
plus all 60 future configuration evaluations. Exact deterministic duplicates may
be deduplicated only by the tuple `{data file hash, scored observation window,
strategy, symbol, timeframe, exit_mode, literal params, cost model}`. Every
include/exclude decision must appear in a row-level ledger with artifact path.
Registry absence is never an exclusion reason.

The final historical count is deliberately not invented here. Completion and
independent review of that ledger are hard prerequisites to an execution
approval. The DSR calculation must then copy the engine equations literally:

- `SR = lockbox_oos.sharpe_pt` and `T = num_trades`;
- `sigma = sample_std(best_train_sharpe_pt, ddof=1)` over the attached comparable
  1h Keltner pool, with no silent 10m/1h mixing;
- Euler-Mascheroni constant `gamma = 0.5772156649`, skew 0, kurtosis 3;
- expected maximum and normal-CDF equations exactly as
  `mega_walk_forward.py:deflated_sharpe_pvalue`;
- no intermediate rounding; final confidence rounded to four decimals only.

Literal equations, with `Phi` the standard normal CDF and `Phi^-1` its inverse:

`z_max = (1-gamma) × Phi^-1(1-1/N) + gamma × Phi^-1(1-1/(N×e))`

`expected_max_SR = sigma × z_max`

`denom = sqrt(max(1e-9, (1 + ((3-1)/4)×SR^2) / (T-1)))`

`du_cell = Phi((SR-expected_max_SR) / denom)`

Six-cell selection is corrected separately from trial-family N:
`du_family = 1 - min(1, 6 × (1 - du_cell))`. Requiring
`du_family >= 0.95` means each deciding cell must have unadjusted
`du_cell >= 0.9916667`.

## 8. Exit-aware tooling prerequisite — not approved by D016

No existing gauntlet output is eligible for this confirmation until a separate
tooling task is approved, implemented, tested, and adversarially reviewed. That
task must, at minimum:

- pass each row's literal `exit_mode` into every CPCV and multi-window
  `simulate_slice` call and stamp it in every output/candidate ID;
- use the five literal configurations above, never generated percentage
  perturbations;
- count insufficient-trade diagnostic neighbors as stability failures rather
  than removing them from the denominator;
- persist, per symbol and exit, a 5-configuration × 6-common-period return matrix
  for PBO; never treat symbols or exits as configuration competitors;
- preserve byte-identical default `fixed_2R` behavior and pass the existing
  self-parity gate without recapturing goldens.

Tool approval is not run approval. Passing tool tests is not strategy evidence.

## 9. Forward decision bar fixed now

For each primary symbol/exit row, `forward_bar(mode)` is true only when all are
true on the fixed future interval:

- at least 30 trades;
- net return after the fixed slippage stress is positive;
- profit factor at least 1.30 and expectancy_R at least 0.10;
- max drawdown greater than -50%;
- positive excess return versus buy-and-hold on the identical scored interval;
- bootstrap p-value survives BH-FDR at Q=0.10 across all 12 primary rows;
- union DSR meets the section 7 six-cell-adjusted requirement;
- exit-aware CPCV, PBO, multi-window, and literal-neighbor gates below all pass.

Gauntlet contract:

- **CPCV:** six contiguous groups, two test groups, 15 combinations, 1% embargo,
  at least 30 trades and positive return per passing combination, PF at least
  1.0, maxDD greater than -50%, median return positive, and at least 11/15
  combinations passing.
- **PBO:** the per-cell 5×6 matrix; ten complement-unique 3/3 CSCV partitions;
  PBO below 0.50.
- **Multi-window:** the fixed Q1/Q2/Q3/Q4/H2 placements; positive return in at
  least 3/5 with at least 15 trades in every positive window.
- **Literal-neighbor stability:** at least 70% of the four star diagnostics have
  positive future return; a neighbor with insufficient trades counts as fail.

Any `N_A`, `INSUFFICIENT_DATA`, `TOOL_FAILED`, missing exit stamp, missing matrix,
or incomplete split set is a gauntlet failure. No gate is waived as “not
applicable” after results are visible.

## 10. Per-cell truth table and aggregate outcome

There is no DSR-difference margin and no judgment override.

| `forward_bar(trail)` | `forward_bar(fixed)` | Cell category |
|---:|---:|---|
| 1 | 0 | EXIT-INCREMENTAL |
| 1 | 1 | POCKET-ONLY |
| 0 | 1 | BASE-ONLY |
| 0 | 0 | NEITHER |

| Outcome | Mechanical condition | Action |
|---|---|---|
| A — CONFIRMED | EXIT-INCREMENTAL appears in at least two distinct diversity groups | Record forward confirmation and propose, but do not authorize, a separate FORWARD_PAPER decision package |
| B — POCKET | No A; at least one POCKET-ONLY cell | Exit hypothesis negative-incremental; base pocket may only continue under a new separately approved plan |
| C — BASE ONLY | No A/B; at least one BASE-ONLY cell | Exit hypothesis negative; no trail continuation |
| D — NOT CONFIRMED | All cells NEITHER, or only one diversity group has EXIT-INCREMENTAL | Stage-1 result remains research-only; no rerun or window extension under this preregistration |
| E — VOID | Any STOP rule fires | Zero evidentiary weight; amendment and fresh approval required |

E overrides all other rows. Outcome A is not paper/live authorization and does
not auto-promote anything.

## 11. Immutable STOP rules

Any of the following makes the attempted evaluation E/VOID:

- evaluation before 2028-07-14;
- window, provider, adjustment, session, symbol, group, exit, parameter, cost,
  or threshold differs from this document;
- any symbol is replaced/dropped or any new symbol is added;
- historical or future artifact ledger incomplete;
- exit-aware tooling lacks its own approval and completed Gate-5 review;
- any scored-window strategy metric was computed before the approved unblinding;
- row/job-key mismatch, missing stamping, `NO_DATA`, `SKIPPED_*`, `ERROR`, crash,
  partial output, or reused smoke/full checkpoint;
- any engine/trading-logic change not separately approved and parity-verified;
- any attempt to extend the window because trades or performance are weak.

There is no automatic retry. A first crash or mismatch stops the attempt. A
future execution document must assert the exact symbol order, groups, timeframe,
exits, five configurations and their roles, manifest realpath/hash, engine commit,
output directory, job-key set, and absence of extra values before launch.
Any future plumbing smoke must use only pre-window historical AAPL data in an
isolated disposable directory, keep performance fields blinded, and inspect only
stamping/runtime. It cannot touch a decision symbol's future window or share a
checkpoint/output directory with the full evaluation.

## 12. Authorization ledger and next gates

- [x] D016: Path A selected; this scope/data-window freeze is approved.
- [ ] Separate approval for exit-aware CPCV/multi-window/PBO tooling.
- [ ] Tool implementation tests and independent Gate-5 review.
- [ ] Historical trial ledger completed and independently reviewed.
- [ ] Future window closed and non-performance data inventory approved/completed.
- [ ] New execution-specific Gate-5 review of code, ledger, and frozen contract.
- [ ] Separate written approval for exactly one smoke and one full evaluation.
- [ ] Separate human decision for any proposed FORWARD_PAPER package.

Until every unchecked item is closed in order, the only approved action is to
retain this document while the calendar window accrues.
