# FAZ 3B — STAGE-2 NEW-SYMBOL CONFIRMATION PRE-REGISTRATION (DRAFT — awaiting Gate-5 + Barış approval)

> Status: **DRAFT. NOT APPROVED. NO RUN, NO DOWNLOAD, NO RUNNER EXECUTION IS AUTHORISED.**
> Written 2026-07-15/16 by Claude Fable 5, BEFORE any Stage-2 result of any kind exists and
> before any new data was acquired. Requires (1) adversarial Gate-5 review, (2) Barış's explicit
> written approval → recorded as a new decision in `_AI_MEMORY/DECISIONS.md`.
>
> **Supersedes the 2028 forward-window plan (D016 Path A) as the primary route.** Barış rejected
> the two-year wait 2026-07-15 ("2028 diye bir şey yok"). This document is the executable-now
> alternative. The older drafts remain historical records:
> `FAZ3B_STAGE2_CONFIRM_PREREG_2026-07-13.md` (BLOCKED, Gate-5 FATAL) and
> `FAZ3B_STAGE2_FORWARD_CONFIRM_PREREG_2026-07-13.md` (D016 Path A, now the fallback if this
> design is rejected).
> Binding parents: D013 (two-stage DSR discipline), D015, `FAZ3B_EXIT_SWEEP_SCOPE.md`,
> Stage-1 report `03_QUANTLENS/research/faz3b_stage1_20260705/STAGE1_REPORT.md`,
> `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md`,
> Gate-5 findings `11_TRIAGE/CODEX_GATE5_FINDINGS_FAZ3B_STAGE2_2026-07-13.md` (every REQUIRED
> EDIT is applied here — see §11).

## 1. The problem this solves

Stage-1 (D015) found ONE clean cell: GEN_KELTNER_BREAKOUT × AAPL × 1h × `trail_ema8`,
STRONG_PASS, union-DSR 0.581, 49 trades, +19.0% OOS, winner `{ema_len:50, atr_len:10, mult:2.0}`
(re-verified from `pass2_1h/MEGA_walk_forward_results.json`). Its fixed_2R twin was
INSUFFICIENT_TRADES (25 trades). Known confound: the first-ever 1h fixed_2R baseline itself
produced robust KELTNER cells on SPY/QQQ — so part of the Stage-1 signal may be the 1h pocket,
not the exit.

Confirming that requires data the candidate family has never touched. **A verified scan
(2026-07-15, 145 result files) proves no such data exists in-repo:** the canonical bundle
`native_multiasset_alpaca_2026-06-28` has 51 symbols × 7 timeframes = 357 cells and the
June-29 overnight swept GEN_KELTNER_BREAKOUT across **all 357** — zero untouched (symbol,TF)
pairs. The registry did not reveal this (it lists 5 runs); only a result-JSON scan did.
Two genuine out-of-sample sources remain: future bars (the rejected 2028 wait) or **symbols the
family has never seen**. This design takes the second.

## 2. Pre-registered hypotheses

The Stage-1 winner is **FROZEN**. This is a confirmation of ONE pre-specified configuration on
data it was never selected on — not a search.

- **H1 (exit is incremental):** on the frozen config, `trail_ema8` clears the §6 decision bar on
  decision cells in **≥2 pre-defined diversity groups**, where `fixed_2R` at the SAME cell does
  not.
- **H0 (family closes):** no cell clears at `trail_ema8` → the Stage-1 AAPL result does not
  generalise; the family is recorded as non-generalising and gets no further run on this data.
- **H_confound (pocket, not exit):** cells clear at BOTH exits → the KELTNER-1h pocket is real
  but the exit knob is not incremental → Faz 3b concludes negative-incremental.

## 3. Scope — every axis frozen BEFORE acquisition

| Axis | Value | Justification |
|---|---|---|
| Strategy (1) | `GEN_KELTNER_BREAKOUT` | the sole clean Stage-1 H1 family; adding others = discovery |
| Timeframe (1) | `1h` | H1 confirmed at 1h; H0 held at 10m. Other TFs = new discovery, and all are swept anyway |
| Exit modes (2) | `trail_ema8` (candidate, FROZEN) + `fixed_2R` (confound twin, not a candidate) | the paired twin is the only way to measure the exit's incremental value |
| **Decision config (1, FROZEN)** | **`{ema_len: 50, atr_len: 10, mult: 2.0}`** | the Stage-1 winner, unchanged. **Only this config decides.** No best-of-N selection on the new data (Gate-5 edit 4) |
| Diagnostic stars (4, NON-DECIDING) | `{20,10,2.0}`, `{50,20,2.0}`, `{50,10,1.5}`, `{50,10,2.5}` | one-axis neighbours, used ONLY for neighbourhood-stability + the PBO config matrix. They can never replace or rescue the primary |
| Symbols (16, held-out) | §4 — 4 diversity groups × 4 | verified 2026-07-15 absent from every GEN_KELTNER_BREAKOUT row in `05_BACKTEST_RESULTS/` + `research/` (68 Keltner-touched symbols enumerated; none of the 16 appear) |
| Data window | `2020-07-27 → 2026-06-26`, provider `alpaca_iex`, 1h | identical convention to the canonical bundle so the comparison is like-for-like |
| Grid | none — the frozen config is scored directly | this is confirmation, not a sweep |

**Decision cells (frozen now):** 16 symbols × 1h × `trail_ema8` = **16 decision cells**. Their 16
`fixed_2R` twins exist only for the §7 confound rule. No AAPL/bundle symbol appears anywhere.

## 4. Symbol universe — frozen, diversity-grouped (Gate-5 edit 3)

Groups are defined NOW and may never be redefined after results are visible. Confirmation
requires success in **≥2 groups**; a single-group success is research evidence only.

| Group | Symbols | Why this group |
|---|---|---|
| **G1 — US single-name, non-tech** | JPM, XOM, JNJ, PG | financials/energy/healthcare/staples — deliberately NOT the tech cluster the Stage-1 symbols came from |
| **G2 — International equity ETF** | EWJ, EWG, INDA, EWZ | Japan/Germany/India/Brazil — **different market regimes**, the strongest available answer to the "same 2020-2026 US regime" correlation objection |
| **G3 — Broad / factor ETF** | RSP, QUAL, MTUM, USMV | equal-weight + factor tilts — structurally different from the cap-weighted SPY/QQQ pocket |
| **G4 — Sector / theme (non-bundle)** | SMH, XBI, KRE, XOP | semis/biotech/regional-banks/oil-services — sector dispersion |

**Honest limitation (disclosed, not hidden):** these are new SYMBOLS, not new TIME. They share
the 2020-2026 macro era with the swept universe, so they are less regime-independent than a true
forward window. G2 (international) and G4 (dispersed sectors) partly mitigate this; the ≥2-group
rule prevents one correlated regime from carrying the claim. This design trades some
regime-independence for a result in days instead of two years — an explicit, approved trade-off.

## 5. Step 0 — data acquisition (approval-gated, run BEFORE anything else)

```powershell
# NOT AUTHORISED until Barış approves this pre-registration.
python MTC_COMMAND_CENTER\03_QUANTLENS\tools\alpaca_download_dataset.py `
  --bundle-name native_newsymbol_confirm_2026-07 `
  --symbols JPM XOM JNJ PG EWJ EWG INDA EWZ RSP QUAL MTUM USMV SMH XBI KRE XOP `
  --asset-class confirm_newsymbol `
  --timeframes 1h --start 2020-07-27 --end 2026-06-26 --feed iex --adjustment all
```
> The `--symbols` / `--asset-class` override did NOT exist when this pre-reg was first drafted —
> the self-review caught that the original command was fabricated. The flags were added
> 2026-07-15 as an **additive** change (omitting `--symbols` reproduces the historical universe
> byte-for-byte; `EQUITY_UNIVERSE` is never mutated, so existing bundles keep their exact
> composition). Unit-tested in `tools/tests/test_exit_aware_gauntlet.py`. Requires Alpaca API
> credentials in the environment.
Acceptance before any scoring: all 16 symbols present at 1h with
`ohlcv_validation_status: PASS`, bar counts within ±10% of the bundle's 1h norm (~8,850), and
first/last timestamps matching the window. **Any symbol failing acceptance is DROPPED and
recorded — never silently substituted** (Gate-5 edit 12). If fewer than 8 symbols or fewer than
2 groups survive acceptance, the run is VOID and needs an amended pre-registration.

Re-verify virginity at launch (Gate 1.1): re-run the result-JSON scan and assert every acquired
symbol is still absent from every GEN_KELTNER_BREAKOUT row. A hit VOIDS that symbol.

## 6. Decision bar (per decision cell)

All thresholds are the engine's existing gates; none is invented here.

- **MIN_TRADES:** ≥30 lockbox trades, else `INSUFFICIENT_TRADES` (never PASS).
- **Classification:** engine fold logic unchanged; decision requires PASS/STRONG_PASS.
- **Benchmark Gate:** positive excess alpha vs buy & hold over the identical window. A cell that
  beats the gate but loses to buy & hold is `BETA_DISGUISED_AS_ALPHA` and does not confirm.
- **BH-FDR:** engine within-run Benjamini-Hochberg at **Q = 0.10** over the run's 32 rows.
  Decision requires `bh_fdr_survivor = true`.
- **Multiplicity across cells (Gate-5 edit 6):** because we claim "≥1 cell in ≥2 groups", each
  confirming cell must also satisfy `du_family = 1 − min(1, m × (1 − du_cell)) ≥ 0.95` where
  `m` = number of decision cells actually scored (16 if all survive acceptance) — i.e.
  `du_cell ≥ 1 − 0.05/m`. `du_cell` is the union-adjusted DSR computed by the §8 literal algorithm.
- **Gauntlet (exit-aware, all three required):** CPCV pass-rate ≥ 70% with median OOS > 0;
  PBO < 0.50 from the per-cell **configuration × period** matrix; multiwindow ≥3/5 positive
  windows AND ≥70% literal-star neighbour stability with insufficient-trade neighbours counted as
  failures. **Any N_A / INSUFFICIENT_DATA / TOOL_FAILED / missing exit stamp = GAUNTLET_FAIL**,
  never a waiver (Gate-5 edit 10). Tooling: `03_QUANTLENS/tools/exit_aware_gauntlet.py`
  (built + unit-tested 2026-07-15 on branch `feature/exit-aware-gauntlet`; the legacy tools
  silently scored fixed_2R and must never be used for this).

**A cell CONFIRMS iff:** PASS/STRONG_PASS ∧ trades ≥30 ∧ excess alpha > 0 ∧ `bh_fdr_survivor`
∧ `du_family ≥ 0.95` ∧ gauntlet PASS.

## 7. Confound rule — exact, no tunable margin (Gate-5 edit 8)

Per cell, `bar(mode)` = the full §6 decision bar:

| bar(trail) | bar(fixed) | Category |
|---|---|---|
| 1 | 0 | **EXIT-INCREMENTAL** |
| 1 | 1 | **POCKET-ONLY** |
| 0 | 1 | **BASE-ONLY** |
| 0 | 0 | **NEITHER** |

The old draft's `du(trail) ≥ du(fixed) + 0.10` escape hatch is REMOVED — a difference between two
nonlinear confidence transforms is not evidence that the exit added return.

## 8. Union-adjusted DSR — literal algorithm (Gate-5 edit 7)

Copy of the engine convention (`mega_walk_forward.py:1507-1525`), stated so two implementers get
the same number: Euler–Mascheroni expected-maximum Sharpe; skew = 0, kurtosis = 3; denominator on
`n_trades − 1`; normal CDF; `np.std(..., ddof=1)`; `NO_DATA/ERROR/SKIPPED_RULE` rows excluded;
rounding only after the final CDF.

**Which multiplicity actually applies — the design's central statistical claim.**

The old draft deflated by a "union family" because it selected the best of 12 configs *on the
same data it judged*. **This design does not select on the new data at all**: `{50,10,2.0}` was
chosen on Stage-1 data and is frozen. Testing a pre-specified hypothesis on data it was never
fit or selected on is exactly what out-of-sample validation buys — the prior search is *paid
for* by the fresh data, so deflating the per-cell test by the historical search count would be
double-counting and over-conservative.

**Therefore the PRIMARY decision uses only the multiplicity created INSIDE this run:**
1. `m` = number of decision cells scored (16 if all survive acceptance) → the §6 rule
   `du_family = 1 − min(1, m × (1 − du_cell)) ≥ 0.95`;
2. the engine's within-run BH-FDR at Q = 0.10 over the run's 32 rows;
3. the ≥2-diversity-group requirement.
`du_cell` is computed with the literal algorithm above using **this run's own rows** as the
Sharpe pool (all 32; `NO_DATA/ERROR/SKIPPED_RULE` excluded).

**SECONDARY (reported, never decisive) — historical-search conservatism check.** The frozen
config did come from a large search, and the new symbols share the 2020-2026 era with the swept
universe, so the fresh data is not perfectly independent. As an honesty diagnostic the report
must ALSO publish the union-adjusted DSR using the full historical ledger:

| Component | Artifact | Trials |
|---|---|---:|
| Historical 10m fixed_2R full grid | 6yr US-equities sweep | 16 |
| Stage-1 10m, 3 new modes × floor(16/3) | `faz3b_stage1_20260705` | 15 |
| Stage-1 1h, 4 modes × floor(16/3) | `faz3b_stage1_20260705` | 20 |
| **June-29 overnight Keltner (51 sym × 7 TF × 16 cfg)** — omitted by the old draft, proven by the 2026-07-15 result-JSON scan | `overnight_multiasset_2026-06-29` | **5,712** |
| This run (16 sym × 2 exits × 1 frozen config) | new | 32 |
| **N_historical_union** | | **5,795** |

Both numbers are pre-registered so neither can be renegotiated after seeing results. **If the
primary bar passes but the N=5,795 secondary does not, the report must say so plainly and the
outcome is capped at §10 row A′ (research evidence, no promotion)** — the confirmation is then
"survives fresh-symbol testing but not full historical deflation", which is an honest and
materially weaker claim than an unqualified CONFIRMED.

## 9. Execution plan (ONLY after approval) + STOP rules

Order: **0. acquire + verify → 1. virginity re-scan → 2. 1-cell smoke → 3. full run → 4. gauntlet
→ 5. report.**

1. Runner `03_QUANTLENS/tools/faz3b_newsymbol_runner.py` (zero engine edit; injects the frozen
   config, asserts the exact symbol list, `1h` only, both ordered exit modes, stride unset,
   resolved manifest + hash, clean engine commit, empty output dir, expected 32 job keys).
2. **Smoke:** one NON-DECIDING reference cell in both modes, disposable output dir, inspect
   stamping/runtime ONLY — never performance (Gate-5 edit 13). Record
   `full_cap_seconds = ceil(1.5 × 16 × smoke_seconds)` before launch.
3. Full run → `03_QUANTLENS/research/faz3b_newsymbol_<ts>/`; register in
   `RESEARCH_RUN_REGISTRY.json`; morning report per rules-doc §10.

**Power floor (added by self-review 2026-07-16, §E):** the bar needs ≥30 lockbox trades/cell and
CPCV needs enough trades per 2-group window. Low-volatility cells (e.g. USMV, QUAL) may fall
short, which would make the run underpowered rather than informative. **Pre-registered VOID
rule: if fewer than 8 decision cells reach ≥30 lockbox trades at `trail_ema8`, or if the
surviving cells span fewer than 2 diversity groups, the run is VOID** — not "H0 confirmed".
An underpowered run must never be read as evidence against H1.

**STOP rules (any hit = VOID, partial results are NEVER evidence in any direction):** row count
≠ 32 (after documented acceptance drops); missing/incorrect stamping; any `exit_mode` stamp
absent from a gauntlet output; `SKIPPED_NA_EXIT_MODE` > 0; any engine edit needed; a virginity
hit on any acquired symbol; the power floor above; first crash; wall-clock > cap; disk < 10 GB;
any unexplained ERROR row. **No substitution, no cell drop after acceptance, no automatic retry**
— amendment + fresh approval only (Gate-5 edit 12).

## 10. Decision table — every outcome pre-mapped

| # | Outcome | Action |
|---|---|---|
| A | EXIT-INCREMENTAL cells in **≥2 groups**, each passing the gauntlet | Faz 3b exit hypothesis **CONFIRMED**. Propose FORWARD_PAPER queue entry to Barış (separate human gate; production phased: Pine-parity + dry-run first — NOT live, NOT auto-promoted). |
| A′ | EXIT-INCREMENTAL cells but in only 1 group, **or** the §8 secondary N=5,795 check fails, **or** the gauntlet fails on every such cell | research evidence only ("survives fresh-symbol testing, not full historical deflation"); no promotion; no re-run with tweaked settings. |
| B | POCKET-ONLY in ≥1 cell, no EXIT-INCREMENTAL | KELTNER-1h pocket generalises but the **exit is not incremental** → Faz 3b concludes NEGATIVE-incremental. The base result may go to Barış for a SEPARATE decision with its own pre-reg. |
| B′ | BASE-ONLY in ≥1 cell | exit hypothesis DEAD; same handling as B. |
| C | no cell confirms, but ≥1 trail cell is research_robust (`du_cell ≥ 0.50` ∧ trades ≥30) | family stays RESEARCH; no further run without genuinely new data + a new pre-reg. |
| D | zero trail cells research_robust | family **DEAD**. Stage-1 AAPL recorded as non-generalising (selection artifact / pocket). Write the negative result in the registry + handoff. |
| E | any STOP rule fired | run VOID, zero evidentiary weight either way; triage; relaunch only via new approval. |

Precedence A > A′ > B > B′; C/D only when no cell reached any §7 positive category.

## 11. Gate-5 REQUIRED EDITS — application record

| Edit | Applied here |
|---|---|
| 1 status sentence | §header — draft, unapproved, review-gated |
| 2 disqualify contaminated symbols | old 6 symbols gone; 16 scan-verified untouched symbols (§3/§4) |
| 3 diversity rule | §4 — 4 groups, ≥2 required, frozen before results |
| 4 no best-of-N grid | §3 — ONE frozen decision config; 4 stars are diagnostic-only |
| 5 artifact-level family ledger | §8 — incl. the omitted June-29 5,712 trials → N=5,795 |
| 6 cross-cell multiplicity formula | §6 — `du_family = 1 − min(1, m(1−du_cell)) ≥ 0.95` |
| 7 literal DSR algorithm | §8 |
| 8 remove 0.10 margin | §7 — plain truth table |
| 9 exit-aware gauntlet prerequisite | §6 — `exit_aware_gauntlet.py` built + tested; legacy tools forbidden |
| 10 CPCV scoring + N_A = fail | §6 |
| 11 PBO config×period matrix | §6 — per-cell matrix, mixed symbol/exit refused |
| 12 no substitution / STOP | §5, §9 |
| 13 non-evidentiary smoke + cap formula | §9 |
| 14 runner hard assertions | §9.1 |
| 15 sign-off + re-review | §12 |

## 12. What this will NOT claim, and sign-off

Stage-2 will not claim: a tradable edge; that the exit works on any other strategy/timeframe/asset
class; that a confirmed cell is promotable without the separate FORWARD_PAPER human gate; or that
absence of confirmation proves the exit is worthless (only that it does not generalise on THIS
evidence).

- [x] **Self-adversarial review** 2026-07-16: `11_TRIAGE/FAZ3B_NEWSYMBOL_SELF_GATE5_2026-07-16.md`
      — found 2 blocking gaps (fabricated acquisition command → FIXED; gauntlet orchestrator
      `main()` is a stub → OPEN) + corrected the deflation framing (§8) + added the §9 power
      floor. A self-review is NOT independent review.
- [ ] **Wire `exit_aware_gauntlet.main()` end-to-end** (self-review §C) — the gauntlet cannot run
      today; the approved artifact must be the thing that actually runs.
- [ ] Independent adversarial **Gate-5 review** (Codex; own prompt) of this document AND the
      tooling diff — attack symbol virginity, the primary-vs-secondary deflation choice, the
      multiplicity formula, gauntlet feasibility/trade counts, and the §4 correlation limitation.
- [ ] Required edits applied.
- [ ] **Barış approval sentence** → recorded in `_AI_MEMORY/DECISIONS.md`.
- [ ] Only then: §5 acquisition → §9 execution.

**D016 remains unspent on this design.** Nothing above authorises a download, a run, or a promotion.
