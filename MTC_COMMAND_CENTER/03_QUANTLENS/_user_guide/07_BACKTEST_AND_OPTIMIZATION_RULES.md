# 07 — Backtest and Optimization Rules / Workflow (QuantLens → MTC_v2)

> **Status:** Official QuantLens backtest & optimization standard.
> **Language:** English (canonical). **Owner discipline:** parity-first, deterministic, no-repaint, no-lookahead, exit-first.
> **Last hard update:** 2026-05-30 (rewritten in English; merged overnight rigor-audit lessons).
> Supersedes the prior short Turkish draft — all of its rules are preserved below in English.

## Quick Use (read this first)

Before calling any producer candidate "good":

1. **Verify data on disk** (real first/last timestamp per symbol/timeframe) — never trust claimed ranges.
2. **Compound returns only** — never sum trade percentages.
3. **Compare against buy-and-hold** — report strategy %, buy&hold %, and excess alpha separately.
4. **Rolling walk-forward + locked OOS** — a single split is NOT walk-forward.
5. **Trade-count guardrail** — below the minimum → `INSUFFICIENT_TRADES`, never `PASS`.
6. **Multiple-testing correction** — bootstrap p-value + Benjamini-Hochberg FDR + Deflated Sharpe before "robust".
7. **Classify + assign a promotion level** with explicit reasons.
8. **Token-efficient output** — summary-first Markdown, raw rows in CSV/JSON, link an Artifact Index.

If any gate is unmet, the candidate cannot advance. When uncertain, label the uncertainty explicitly.

---

## 1. Purpose and Scope

This is the official QuantLens workflow for evaluating YouTube-derived **signal producer** candidates
before any **MTC_v2** integration. Its goal is to prevent weak, overfit, benchmark-losing, inefficient,
or non-parity-compatible ideas from entering MTC_v2.

It must stay compatible with MTC_v2 principles:
- **parity-first** (Pine/Python parity is the integration gate)
- **deterministic backtest** (same inputs → same outputs)
- **no-repaint**, **no-lookahead**
- **exit-first** (exits/risk designed before entries are trusted)
- **producer / filter / exit / risk separation**

This document is a standard, not a strategy. It does not start backtests; it governs how they are run and reported.

---

## 2. Standard Backtest Workflow

1. Read the intake report for the producer candidate.
2. **Isolate the producer logic** (the raw signal), separate from filters, exits, and risk.
3. **Verify actual data coverage from disk** before any test (see §3).
4. Run an initial **sandbox** backtest with a **small, controlled parameter set**.
5. Only after sandbox sanity, expand to **wider grid optimization**.
6. Apply **rolling walk-forward / OOS / lockbox** validation (multiple folds, never one split).
7. Apply **buy-and-hold comparison** and compute **excess alpha**.
8. Apply **bootstrap, BH-FDR, Deflated Sharpe, and multi-window** stability checks where available.
9. **Document skipped datasets, NO_DATA, and INSUFFICIENT_TRADES** explicitly.
10. **Classify** each candidate (§6) and assign a **promotion level** (§9). Do not promote into MTC_v2
    before passing all required gates (§8).

### MTC_v2 development order (preserved, governs promotion path)
parity-first → Python prototype → bounded multi-symbol validation → walk-forward →
robustness/sensitivity check → feature contract → Pine/Python parity → PineTS check →
TradingView export final verification.

---

## 3. Mandatory Data Validation Rules

- Do **not** trust claimed date ranges from a manifest, a prior report, or a previous model's claim.
- Validate the **actual first/last timestamp** per symbol/timeframe directly from the data files.
- Check **bar count**, **missing files**, and **empty train/OOS windows**.
- Report **NO_DATA** and **INSUFFICIENT_DATA** separately.
- **Skip or reject** invalid windows — never silently score them.

**Why this is mandatory (overnight evidence):** A prior run claimed ~5.6 years of BTC 1h training history.
Actual BTC 1h data began ~2024-04 and BTC 15m ~2025-09 — so the claimed train windows were physically
impossible and the scores were meaningless. Data validation is the first gate.

---

## 4. Mandatory Benchmarking Rules

- Net profit alone is **never** sufficient evidence of edge.
- **Every** result is compared against **buy-and-hold over the identical OOS window**.
- Report **strategy return**, **buy-and-hold return**, and **excess alpha** as separate numbers.
- If the asset rose strongly, a long-only strategy can look good with **no edge** (beta, not alpha).
- Strategies that profit while the underlying is **flat or declining** must be highlighted separately as the
  strongest practical candidates.

**Why (overnight evidence):** A TRX producer returned ~+101.98% but TRX buy-and-hold was ~+107.9% over the
same lockbox — i.e. positive yet **worse than holding the asset**. The benchmark gate exposes this.

---

## 5. Required Metrics (every report)

Strategy net return · **compounded-return method stated** · buy-and-hold return · **excess alpha vs buy&hold** ·
max drawdown · profit factor · trade count · average trade · expectancy · win rate · exposure time ·
return per exposure · long-only / short-only breakdown · commission · slippage · spread (if relevant) ·
train period · OOS period · lockbox period · #configurations tested · #configurations skipped ·
#NO_DATA · #INSUFFICIENT_TRADES · worker count · runtime · bootstrap p-value (if available) ·
BH-FDR status (if available) · Deflated Sharpe status (if available) · multi-window stability status (if available).

> Returns are **compound** by definition. Arithmetic sum of trade percentages is forbidden as a return figure.

---

## 6. Candidate Classification

| Label | Definition |
|---|---|
| `TRUE_ALPHA_CANDIDATE` | Profitable while buy&hold is negative/flat, with acceptable risk metrics. |
| `BENCHMARK_BEATER` | Beats a positive buy&hold benchmark by a meaningful margin. |
| `BETA_DISGUISED_AS_ALPHA` | Positive but does not beat buy&hold, or mostly captures the asset trend. |
| `REGIME_SPECIFIC_EDGE` | Works only in a specific market regime (bull/bear/sideways). |
| `OVERFIT_SUSPECT` | Works only in a narrow parameter pocket; fails neighbor-parameter checks. |
| `STATISTICALLY_UNCONFIRMED` | Practically interesting but fails DSR/FDR/bootstrap robustness. |
| `INSUFFICIENT_TRADES` | Too few trades to support a decision. |
| `NO_DATA` | Required symbol/timeframe/window data missing or empty. |
| `REJECTED` | Fails benchmark, drawdown, trade count, robustness, data quality, or parity. |

---

## 7. Antigravity Error-Prevention Checklist

Treat these as **quality-control failures to avoid**, not personal criticism:

- Presenting an **arithmetic sum of trade percentages** as a compounded return.
- Declaring success **without a buy-and-hold comparison**.
- Claiming **data history that does not exist on disk**.
- Presenting a **single split** as walk-forward.
- Using **`OOS return > 0` as the only PASS condition**.
- Ignoring **trade count**, **max drawdown**, or a **weak profit factor**.
- Generalizing from **one symbol** or **one timeframe**.
- Missing **insufficient train data**.
- Ignoring **commission, slippage, spread**.
- Failing to check **lookahead / repaint / future-leak**.
- Not separating **long vs short** performance.
- **Over-optimizing** on the same dataset.
- Ignoring **multiple-testing correction**.
- **Mixing producer, exit, and risk** logic.
- Treating a strategy-wrapper result as **MTC_v2 parity-compatible**.
- Promoting on a **visually attractive equity curve**.
- Ignoring **parameter-neighborhood stability**.
- Ignoring **market regime**.
- Producing **large verbose reports** that waste future LLM context.

---

## 8. Mandatory Quality Gates

A candidate advances only if it clears every applicable gate.

**Data Gate** — physical data present; actual first/last timestamps verified; train/OOS windows valid;
enough history per symbol/timeframe; NO_DATA & INSUFFICIENT_DATA reported.

**Signal Integrity Gate** — producer logic isolated; separated from exits/filters/risk; signals only on confirmed bars.

**No-Lookahead / No-Repaint Gate** — no future leak; confirmed-HTF/shift logic correct; deterministic Pine/Python.

**Benchmark Gate** — buy&hold comparison done; excess alpha positive; performance checked in declining/sideways markets.

**Risk Gate** — max drawdown acceptable; PF, average trade, expectancy, trade count acceptable; commission & slippage included.

**Robustness Gate** — parameter neighborhood stable; tested across multiple symbols/timeframes; not a one-parameter miracle.

**Statistical Gate** — bootstrap p-value computed (if available); BH-FDR status reported; Deflated Sharpe evaluated;
failed candidates are **never** called "proven edge".

**Execution Efficiency Gate** — parallelized when tasks are independent; worker count logged; runtime logged;
start/progress/done/crash markers written; outputs resumable or auditable from disk.

**Token Efficiency Gate** — report is summary-first; large raw tables stored as CSV/JSON, not duplicated in Markdown;
artifact paths listed; no repeated explanations; stable headings; compact handoff block present.

**Regime Gate** — bull/bear/sideways considered; strategy does not win only when the underlying rises.

**Promotion Gate** — explicit promotion reason; compatible with MTC_v2 producer architecture; preserves exit-first & parity-first.

**Documentation Gate** — parameters, date ranges, symbols, timeframes, metrics, runtime, worker count, artifact
paths, and decision rationale all documented.

---

## 9. Promotion Levels

`REJECTED` → `KEEP_AS_RESEARCH_NOTE` → `PROMOTE_TO_SANDBOX` → `PROMOTE_TO_FORWARD_PAPER_TRADE` →
`PROMOTE_TO_PARITY_CANDIDATE` → `APPROVED_FOR_MTC_V2_INTEGRATION`.

`APPROVED_FOR_MTC_V2_INTEGRATION` is reserved for candidates that are **statistically strong,
benchmark-beating, OOS-stable, no-repaint, no-lookahead, token-efficiently documented, and parity-compatible**.

> The overnight "true alpha" candidates are **not proven live edges**. Maximum eligible level today is
> `PROMOTE_TO_FORWARD_PAPER_TRADE` (or `PROMOTE_TO_PARITY_CANDIDATE` for the strongest), never approved-for-integration.

### Production Safety (preserved, enforced at integration)
- `MTC_V2.pine` changes **only** at the final stage.
- New features ship **default OFF** and **feature-gated**.
- A successful backtest does **not** grant direct entry into main code.
- TradingView export remains the **final release audit** surface.
- Optimization output never changes Pine defaults.

---

## 10. Standard Morning Report Format

Future overnight reports must contain, in this order:
Executive Summary · What Changed · Key Decisions · Tested Universe · Data Coverage · Strategy Families ·
Parameter Search Space · Runtime and Worker Count · Walk-Forward / OOS Method · Statistical Corrections ·
Strategy vs Buy-and-Hold Table · True Alpha Candidates · Benchmark Beaters · Beta Disguised as Alpha ·
Rejected / Overfit Candidates · NO_DATA and INSUFFICIENT_TRADES Summary · Antigravity Error Checks ·
Promotion Recommendations · MTC_v2 Next Actions · Reproducibility Notes · **Artifact Index**.

Top of every report: a compact **"What changed / What matters / Next action"** block.

---

## 11. Token-Efficient File and Workflow Standard

- Markdown is **summary-first**; full result sets live in **CSV/JSON artifacts**.
- Markdown shows only **top candidates + rejected counts + artifact paths** — not every row.
- **Do not duplicate** the same table across multiple files.
- Every workflow doc has a **Quick Use** section near the top.
- Every report ends with an **Artifact Index** of exact file paths.
- **Handoff files stay short** and point to canonical reports.
- Future agents **read targeted sections**, not entire long files — keep headings stable and labels concise.
- **No giant pasted logs.** Prefer machine-readable summaries for large result sets.
- Keep generated reports within LLM context limits.

---

## 12. Execution & Reproducibility Standard

- **Parallelize** independent (strategy × symbol × timeframe × config) jobs (multiprocessing pool).
  Reference: a single-worker engine was estimated at 2–6 h; the parallel version scored 935 configs in ~38 s on 8 workers.
- Prefer **NumPy array access / precomputed arrays** over slow per-row Python loops in the trade simulator.
- Long-running scripts must write a **start marker, progress counters, done marker, crash/error marker, and output paths**.
- Report **single-worker vs parallel** execution, **worker count**, **runtime**, **completed/total/skipped jobs**.
- When workers finish quickly and exit, report **final status from disk** — do not infer failure from an empty process list.
- Outputs must be **resumable or auditable from disk** (JSON results + Markdown summary).

---

## Appendix A — Parity Notes (preserved)

- PineTS is usable for L0–L3 feature/indicator/signal checks.
- If PineTS does not emit lifecycle rows, do **not** claim L4–L6 lifecycle parity.
- The Python engine is the local lifecycle/backtest/optimization owner.
- TradingView Strategy Tester XLSX is **not** a chart-data input; the export workbook is the final audit surface.
- Preserve dataset manifest fields: `dataset_id`, `source_type`, and hashes.

## Appendix B — Overnight Evidence Snapshot (2026-05-30)

Engine: 20 strategy families × 5 timeframes (15m/1h/2h/4h/1D) × 17 symbols × wide grids (~93k configs),
8 workers, ~9 min. Gates: rolling WF + locked OOS, bootstrap (up to 50k resamples) + BH-FDR, Deflated Sharpe, multi-window.

- **Inflation example:** "RSI Confluence SOL 1h +402%" → real **+119.74% compound**, **−77.7% max DD**, PF ~1.11.
  The +402% was an arithmetic sum of trade percentages.
- **Statistical humility:** Under strict full-search-space BH-FDR + DSR, **zero** configs were distinguishable from noise.
- **Benchmark filter is decisive:** TRX dominance was beta, not alpha (TRX buy&hold ~+108%).
- **True-alpha shortlist** (made money while the underlying fell; forward-paper-trade candidates, NOT proven edges):

| Producer | Sym | TF | Strategy % | Buy&Hold % | Alpha % | PF | Trades |
|---|---|---|---|---|---|---|---|
| RSI Oversold Reversal | LTC | 1h | +95.8 | −20.8 | +116.7 | 1.23 | 329 |
| Two-Candle SR | ADA | 1h | +79.2 | −30.5 | +109.7 | 1.72 | 53 |
| 8EMA (Elly family) | LINK | 1h | +75.4 | −20.6 | +96.0 | 2.04 | 121 |
| Candlestick Engulf | APT | 1h | +29.8 | −81.1 | +110.9 | 1.61 | 44 |

## Appendix C — Artifact Index (canonical sources)

- `05_BACKTEST_RESULTS/MORNING_REPORT.md` — canonical overnight summary (includes buy&hold alpha layer).
- `05_BACKTEST_RESULTS/CLAUDE_AUDIT_FINDINGS.md` — Antigravity audit + inflation evidence.
- `05_BACKTEST_RESULTS/MEGA_walk_forward_report.md` + `MEGA_walk_forward_results.json` — full WF+stats results.
- `05_BACKTEST_RESULTS/MULTIWINDOW_OOS_REPORT.md` + `multiwindow_summary.json` — regime + parameter stability.
- `05_BACKTEST_RESULTS/RIGOROUS_walk_forward_report.md` — earlier parallel rigorous pass.
- `05_BACKTEST_RESULTS/alpha_summary.json` — strategy vs buy&hold, excess alpha ranking.
- Tools: `tools/{rigorous_walk_forward.py, mega_walk_forward.py, finalize_bootstrap_bh.py, multiwindow_oos.py, alpha_vs_buyhold.py, generate_morning_report.py}`.
- **Note:** No standalone "final comparison report" file exists; the comparison lives inside `MORNING_REPORT.md` and `CLAUDE_AUDIT_FINDINGS.md`.

---

## Quick Checklist (run before any promotion)

- [ ] Physical data coverage verified (real first/last timestamps)?
- [ ] Buy-and-hold comparison performed?
- [ ] Excess alpha calculated?
- [ ] Performance checked while the underlying declined or moved sideways?
- [ ] OOS / lockbox testing performed (rolling, not a single split)?
- [ ] Multi-window testing performed?
- [ ] Long and short results analyzed separately?
- [ ] Commission and slippage included?
- [ ] Lookahead / repaint risk checked?
- [ ] DSR / FDR / bootstrap results reported?
- [ ] Parameter neighborhood stable?
- [ ] Trade count sufficient (else `INSUFFICIENT_TRADES`)?
- [ ] Drawdown acceptable?
- [ ] Runtime and worker count reported?
- [ ] Raw artifacts stored outside Markdown (CSV/JSON)?
- [ ] Report token-efficient (summary-first + Artifact Index)?
- [ ] Compatible with MTC_v2 parity requirements?
- [ ] Promotion level explicit and justified?
