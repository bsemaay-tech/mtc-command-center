# WAYFINDER KERNEL FOLD — 2026-08-23 (map #67)

**Status:** owner-decision record and plan-amendment pass. Planning only — **implementation authorized: NO.** Per D-12, nothing here is an authorization: no migration starts, no collector deploys, no registry is built, no package begins because of this document.

**What this is.** GitHub map issue [#67](https://github.com/bsemaay-tech/mtc-command-center/issues/67) ("Strategy Kernel & Economic Honesty decision map — one brain, one honest simulation, queue 2/8") ran 2026-08-23 in the owner's rapid-fire mode: 4 AFK research tickets and 5 owner-grilled decision tickets, all resolved and closed the same day, the owner answering every question personally. This fold carries the decisions into the planning set under its change control. **Detail lives in each ticket's resolution comment; this document indexes and applies.**

**Change-control position.** Amends the planning set at master `3d6a621c` (which already carries the map #37 and map #54 folds). **Owner outcome documents untouched. Requirement count stays 60 = 44 + 16. Package count stays 75.** Amendments land inside existing sections and existing packages' text (WP-P0-20, WP-P0-30). **Materiality: MATERIAL** (acceptance additions on WP-P0-20; new governed definition artifacts; §6.5 additions). A fresh G1 acceptance round over the amended set is recommended before G1-IA on affected packages — the owner's call, outside this fold.

---

## 1. The five owner decisions (index — detail lives in each ticket)

| Ticket | Decision gist |
|---|---|
| [Decide: the economic-honesty bar — control parity and cost governance (#73)](https://github.com/bsemaay-tech/mtc-command-center/issues/73) | Control-parity checklist tiered by economic impact: REQUIRED in simulation = allocator, fees, funding, slippage, protective-order semantics (missing one ⇒ BLOCKED evidence); declared-and-tolerated = Guardian veto, partial fills, snapshot staleness — each with a named ladder-measured divergence metric, a D026 fixture, and membership in `evaluation_run_hash` config. Checklist = owner-gated versioned definition (v1: §4 below). Costs MEASURED + event-driven (fees from schedule, funding from history, slippage from own fills; research-side registry, bridge feeds fills upward). Backtest-vs-forward divergence = standing §6.5 check row: breach BLOCKS promotion + notifies, never auto-demotes. |
| [Decide: the reference-implementation doctrine — one brain, fate of the other four, Pine's role (#72)](https://github.com/bsemaay-tech/mtc-command-center/issues/72) | `mtc_v2/core` seeds the canonical kernel; its behaviour = the `LEGACY_COMPATIBLE` baseline. Harvest-then-freeze, nothing deleted: research simulator first, then the `02_MTC_BACKTEST` port (validation pipeline harvested). Bridge executor NOT collapsed — consumes kernel intents via the settled §5.4/§5.5 seams. Pine = frozen reference corpus (parity suite pinned once) + everyday charting; NO standing parity obligation; never evidence (D-13). Known-divergence register: §5 below. Doctrine: only canonical-kernel outputs are ever acceptance-bearing. |
| [Decide: the optimization regime — search-space, budgets, family accounting (#74)](https://github.com/bsemaay-tech/mtc-command-center/issues/74) | Versioned owner-gated search-space definition per family. Trial family = CUMULATIVE per candidate-family forever (TrialRecord makes it countable). Budgets = measured throughput + DSR's self-punishing bar; single owner-gated per-sweep sanity ceiling [OPEN]. Deterministic grid for acceptance-bearing sweeps; adaptive search (dormant Optuna) ONLY in `SIGNAL_SCREEN_ONLY` until an adaptive accounting method is separately ratified. Refresh sweeps = ordinary sweeps under the same family ledger. |
| [Decide: the validation battery and lockbox governance (#75)](https://github.com/bsemaay-tech/mtc-command-center/issues/75) | Battery = versioned owner-gated definition (v1: §6 below; DSR ≥ 0.95 stays). All seven elements kept; CPCV/PBO move INLINE at the port harvest — no skippable offline stage; skipped element ⇒ BLOCKED. Lockbox eras per dataset version; opening AUTOMATIC on earned mechanical criteria + ledger-recorded; an opened era is SPENT for that family. |
| [Decide: historical evidence and the data doctrine (#76)](https://github.com/bsemaay-tech/mtc-command-center/issues/76) | Rerun policy = the canonical kernel's arrival fires the settled new-kernel-version re-entry trigger (auto re-screen; screens never evidence; zero new machinery). Continuous venue-candle archiving = standing owned service, the venue market-data package's EARLIEST deliverable, flagged MOST TIME-CRITICAL wave-1 candidate (daily permanent loss; G1-IA still required). Dataset registry = registered-or-BLOCKED (bundle id + content hash + era boundaries; quality checks as the registrar's gate). Minimum-data bar shape fixed, numbers [OPEN]. |

Research inputs (all closed same day, gists on the map): implementation inventory (#68), parity ground truth (#69), data foundation (#70), optimization/validation state (#71) — findings on `research/kernel-*`, `research/parity-*`, `research/data-*`, `research/optimization-*` branches under `MTC_COMMAND_CENTER/11_TRIAGE/wayfinder_research/`.

---

## 2. Amendments applied

| # | File · where | What |
|---|---|---|
| A1 | brief · new **§9.7** before section 10 | "Kernel & economic-honesty governance — map #67 fold": the normative summary of all five decisions (doctrine, honesty tiers married to §9.1's `UNSIMULATED_CONTROLS` manifest, cost governance, optimization regime, battery/lockbox, data doctrine), with ticket links and [OPEN] marks. |
| A2 | brief · §6.5 map-#54 admission-mechanics block | Two rows appended: the backtest-vs-forward divergence check (blocks promotion, notifies) and the lockbox-opening record + spent rule. |
| A3 | plan · WP-P0-20 section head | Amendment paragraph: seed named (`mtc_v2/core`, LEGACY_COMPATIBLE baseline = its behaviour); acceptance additions — control-parity checklist v1 exists and the simulator implements its REQUIRED tier; statistical-battery definition v1 exists; CPCV/PBO inline unification at the port harvest. |
| A4 | plan · WP-P0-30 section head | Amendment paragraph: the continuous collector is this package's EARLIEST deliverable and the platform's most time-critical wave-1 candidate (#76); label correction noted (§7). |

Discipline: anchored script, every replacement asserts its anchor occurs exactly once; repo-wide grep for changed values after the pass.

---

## 3. New owner-gated definition artifacts (registered by this fold; each versioned, changes owner-gated, application automatic)

1. **Control-parity checklist** (v1 in §4).
2. **Statistical-battery definition** (v1 in §6).
3. **Search-space definition** (per-family; class registered here, instances created per family — no v1 exists until a family forms under the new machine).
Existing members of the class, for the record: eligibility check sets (map #54), slot-ranking rule (map #54), triage worthiness checklist (map #54 fold).

---

## 4. Control-parity checklist — v1 (owner-ratified via #73)

| Control | Tier | If tolerated: divergence metric (measured at) |
|---|---|---|
| Risk Allocator | REQUIRED (settled, WP-P0-20) | — |
| Fees | REQUIRED | — |
| Funding | REQUIRED | — |
| Slippage | REQUIRED | — |
| Protective-order semantics | REQUIRED | — |
| Guardian authorize/reject | tolerated | veto rate (SHADOW) |
| Partial fills | tolerated | fill-shape divergence (TESTNET) |
| Snapshot staleness | tolerated | staleness distribution (SHADOW) |

Rules: a REQUIRED control absent from a sim run ⇒ **BLOCKED evidence**. Every tolerated control: named metric + D026 fixture + `evaluation_run_hash` config membership. Tolerated controls are exactly the checklist's projection of §9.1's `UNSIMULATED_CONTROLS` manifest — the manifest names them, the checklist governs them.

---

## 5. Known-divergence register — seeded (owner-ratified via #72)

Disposition vocabulary: **REPRODUCE-THEN-CORRECT** (reproduced in `LEGACY_COMPATIBLE`, fixed as a versioned `CORRECTED_VNEXT` change) or **LEGACY-DEFECT** (dies with its frozen implementation). Dispositions per entry are set when WP-P0-20 reaches each item; nothing is silently absorbed.

| # | Divergence (source) | Initial classification |
|---|---|---|
| 1–4 | Four multi-timeframe/regime-filter parity divergences (parity ground truth #69, "mixed character, needs live investigation") | undetermined — investigate at WP-P0-20 |
| 5–6 | Two additional real behavioural divergences from the 6/58 set (#69) | undetermined — investigate at WP-P0-20 |
| 7 | Parity confirm/refresh gating bug (#69, "bounded, scoped") | LEGACY-DEFECT candidate |
| 8 | CPCV `exit_mode` not passed to simulator (#71, live on master) | LEGACY-DEFECT of the offline stage; the inline unification (#75) supersedes the stage — a separate fix task chip exists for the interim |

Also recorded, not divergences: Pine's contract-multiplier sizing difference vs the Python kernel (`position_sizer.py:47`, inventory #68) — a known cross-implementation difference the LEGACY_COMPATIBLE baseline must take a position on at migration.

---

## 6. Statistical-battery definition — v1 (owner-ratified via #75)

Elements (all seven, none skippable; skipped ⇒ BLOCKED): walk-forward · lockbox · CPCV · PBO · DSR ≥ 0.95 · BH-FDR · sensitivity. Verdicts bind to `evaluation_run_hash` + battery version. CPCV/PBO run inline in the canonical pipeline from the port harvest onward. Lockbox: eras per registered dataset version; opening automatic on earned mechanical criteria, always a lifecycle-ledger record; an opened era is SPENT for that family (later results navigational).

---

## 7. Corrections recorded by this fold

1. **Label correction:** the #76 resolution prose says "VEN-C" for the archiver's carrier; the venue market-data package is **VEN-E = WP-P0-30** (VEN-C = WP-P0-29, custody). The owner's ratified option text named "the existing venue-data package" — referent unambiguous; the fold applies it to WP-P0-30.
2. **Corpus identity:** the 437/439 figure (`PARITY_STATUS_FINAL_20260304.md`, brief §2 Corpus B) tests the `02_MTC_BACKTEST` port, NOT the `mtc_v2` kernel — the two parity figures measure different codebases (parity ground truth #69).
3. **Catalog honesty:** the documented "PRIMARY" Alpaca bundle's data is absent (git-ignored, never present); the deepest dataset (Binance BTC/ETH 2018–2026) is reachable only via a broken catalog path into an ungoverned legacy folder (`C:\LAB\tradingview-lab\110_...`, untouched since 2026-03). Both feed the registered-or-BLOCKED rule (#76); the deep dataset becomes registrable only after quality-pass + copy into governed storage.
4. One wrong commit-hash citation in the brief flagged by the implementation inventory (#68) — recorded in that research file; corrected opportunistically at the next brief-touching round rather than by this fold.

---

## 8. What this fold does not do

No migration, collector, registry, or import is built or started; no thresholds set (every number stays [OPEN]); no package added or removed; no owner document edited; the CPCV interim fix stays a separately-authorized chip task. G1-IA remains ungiven for every package. D-12 throughout.
