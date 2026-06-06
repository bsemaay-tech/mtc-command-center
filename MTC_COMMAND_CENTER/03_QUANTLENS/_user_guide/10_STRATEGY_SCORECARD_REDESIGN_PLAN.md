# Strategy Scorecard Redesign — Implementation Plan

Status: PLANNED (not started). Proposed 2026-06-02 by Claude (Opus 4.8).
Revised 2026-06-02 after two independent LLM audits (see §9 Audit log).
Owner decision pending: Barış.
Source rubric: `11_TRIAGE/_eval_pipeline_source_TEMP/` (draft, **delete only in Phase 5** — needed as reference until canonical rubric + schema + tests + UI merged).

---

## 1. Problem (why redo the score)

Current strategy-detail score = `build_scorecard()` in
`08_DASHBOARD_APP/apps/api/mcc_readonly/presentation_reader.py:65`.

One flat 100-point blend:

| bucket | max | what it actually measures |
|---|--:|---|
| Source coverage | 20 | has URL / transcript (documentation, not edge) |
| Rule quality | 25 | rules written down (documentation, not edge) |
| Backtest evidence | 35 | **25 = pipeline stage maturity, only 10 = real PF+return+trades** |
| Execution readiness | 10 | stage-gated |
| Risk / cleanliness | 10 | source hygiene, not trade risk |

Core defects:

1. **Measures pipeline progress, not strategy quality.** A strategy reaching the
   `integrated` stage collects ~25 free points whether or not it makes money.
   Circular: advancing through the funnel raises the score that is supposed to
   decide whether it should advance.
2. **Risk-blind.** Return scored as `return/20`; PF as `(PF-1)*5`. No max
   drawdown, no Sharpe/Sortino, no recovery factor, no exposure adjustment.
   100% return @ 90% DD scores same as 100% @ 10% DD.
3. **No benchmark.** Nothing compares against Buy&Hold on the same period/fees.
4. **No robustness layer.** OOS, walk-forward, CPCV, PBO/overfitting absent from
   the score, even though the overnight tooling already computes them.
5. **No hard-fail gate.** Repaint / lookahead / uncodable do not stop or zero a
   score. They should be kill switches.
6. **One misleading number.** A well-documented but unproven (or curve-fit)
   strategy reads ~55+. User cannot tell "documented" from "has edge."

The draft rubric in `_eval_pipeline_source_TEMP/` fixes all six by replacing one
blend with **separate gates per phase** + hard-fail gates. This plan adapts that
rubric into the dashboard and backtest pipeline.

---

## 2. Target design

Replace single composite with **4 gate scores + hard-fail flags**, shown as
separate bars on the strategy-detail page. Never recollapse to one number.

```
Gate 1  Candidate Intake        /100   (codable? worth testing?)
Gate 1B MTC Feasibility         /50    (representable in MTC_v2?)
HARD    Repaint / Lookahead     pass/fail   (REJECT_REPAINT zeroes everything)
Gate 2  Backtest Evidence       /100   (risk-adjusted, benchmark, robustness)
Gate 3  Production Readiness     /100   (signal contract, alert, fail-safe)
```

Each gate min-pass 75 (Gate1B 40/50 or PASS). A gate stays `N/A` until its phase
data exists — the page shows "not evaluated", not a fake number. This is the
whole point: no Gate2 score before a backtest, no Gate3 score before integration.

Key data-coupling principle: **every Gate2/Gate3 sub-criterion must map to a
field the pipeline already emits or can emit.** Criteria with no data source get
a numeric threshold definition first (see §3), then a producer.

---

## 3. Make the rubric machine-computable (prerequisite)

The draft rubric is judgement-based ("Max drawdown kabul edilebilir / 5"). Convert
**every** subjective sub-criterion — not just Gate2 — to a field + scorer rule.
Audit finding: Gate1 ("human interpretation", "state machine") and Gate1B ("risk
engine conflict", "alert format") are also subjective and need explicit source
fields before implementation. The full subjective→field mapping is a Phase 0A
deliverable.

**Provisional** numeric bands below are anchors only. Per both audits, the real
ranges are set in **Phase 1.5 from observed distributions** of 5–10 real
strategies — not guessed up front. Final bands need Barış sign-off.

| metric | 5 pts | 3 pts | 1 pt | 0 |
|---|---|---|---|---|
| Max drawdown | <15% | <25% | <40% | ≥40% |
| Sharpe | >1.5 | >1.0 | >0.5 | ≤0.5 |
| Profit factor | >1.8 | >1.4 | >1.1 | ≤1.1 |
| Recovery factor | >3 | >2 | >1 | ≤1 |
| PBO (overfit prob) | <0.2 | <0.35 | <0.5 | ≥0.5 → **Gate2 FAIL / OVERFIT_SUSPECT** |
| Return / MaxDD | >3 | >2 | >1 | ≤1 |

PBO policy (audit-recommended): PBO≥0.5 **blocks promotion** and marks Gate2
`OVERFIT_SUSPECT` — it does **not** archive/reject the idea. Only valid once the
PBO tool split bug (AUDIT-005) is fixed (Phase 1A).

These metrics (Sharpe, Sortino, recovery factor, PBO, CPCV verdict) are **absent
from the source Gate2 rubric** (`05_gate_2_backtest_evidence.md` is fully
subjective). Phase 0A must add them as explicit Gate2 sub-criteria so the bands
have a rubric to operationalize.

Benchmark (Gate2 §5.6): per-run, **same symbol / timeframe / OOS window / fee**,
not just "already produced". Artifact must carry `bh_return`, `bh_maxdd`,
`bh_sharpe`, `excess_alpha`. Strategy must beat B&H on risk-adjusted (Return/DD,
Sharpe), not raw return. AGENTS.md also requires **multi-window** + DSR + BH-FDR
for promotability → add multi-window fields to the artifact.

### 3.1 Per-metric status envelope (audit-required)

"Populated or null" loses meaning. Every metric in every artifact carries:

```json
{ "value": 1.42, "status": "OK", "reason": "", "source_path": "sprint_runs/.../result.json" }
```

`status` ∈ `OK | N_A | NOT_COMPUTED | INSUFFICIENT_DATA | INSUFFICIENT_TRADES | TOOL_FAILED`.

Scorer rule: only `OK` scores. `N_A`/`NOT_COMPUTED`/`TOOL_FAILED` → sub-criterion
greyed, gate cannot reach pass until resolved. A failed CPCV/PBO tool → `N_A`,
**never auto-zero / auto-fail**.

---

## 4. What already exists (leverage, don't rebuild)

| need | already in repo | file |
|---|---|---|
| Walk-forward / OOS | yes | `03_QUANTLENS/tools/mega_walk_forward.py` |
| CPCV | yes | `03_QUANTLENS/tools/cpcv_validator.py` |
| PBO / overfitting | yes | `03_QUANTLENS/tools/probabilistic_pbo.py` |
| Buy&Hold baseline | yes | `buy_hold_baseline.py` (sprint_runs) |
| Single-strategy flow | yes | `03_QUANTLENS/tools/single_strategy_backtest.py` |
| Scorecard render (UI) | yes | `08_DASHBOARD_APP/apps/web/app.js` `renderScorecard()` |
| Scorecard compute | yes (to replace) | `presentation_reader.py:build_scorecard()` |

So Gate2 robustness inputs (WFO, CPCV, PBO, B&H) are **already computed** — they
are just not surfaced into the score. Half of Phase 2 is plumbing, not new math.

---

## 5. Phased plan + AI assignment

Tag format per AGENTS.md: `[AI: Claude|DeepSeek|Any|Barış]`.

Order revised per both audits: schema + rubric mapping first, tool fixes next,
**emit metrics before finalizing bands** (bands set from real data), then engine,
UI, backfill, cleanup.

### Phase 0A — Rubric mapping + schemas + template (spec only, no bands yet)
- Migrate source rubric into canonical `_user_guide/` doc. While migrating, fix
  the source gaps both audits flagged:
  - Add Sharpe/Sortino/recovery/PBO/CPCV as explicit Gate2 sub-criteria.
  - **Gate1B mode decision**: pick /50 **or** PASS/FAIL (recommend /50 bar +
    derived PASS at ≥40), and sync `07_final_decision_matrix` column wording.
  - De-dup Gate1B vs Gate3 signal-contract overlap (Gate1B = "representable at
    all?" coarse; Gate3 = "production-grade?" precise) to kill double-score bias.
  - Score SAFE_WITH_DELAY (delay penalty in Gate2 execution-realism) and define
    NEEDS_MODIFICATION behavior (block Gate2 → back to prototype).
  - Promote parity ("Pine=Python signals match") to a scored Gate2 sub-criterion
    or hard pass/fail.
  - Raise Gate2 §5.7 Rejim Analizi 5→10 pts (regime awareness = production-gating
    basis); borrow from §5.1/§5.3.
- Define **two** JSON schemas with the §3.1 status envelope:
  `evaluation_artifact_v1` (Gate2 metrics) and `production_readiness_artifact_v1`
  (Gate3: alert adapter, state sync, risk-engine compat, monitoring, fail-safe,
  reproducibility — these are **not** in backtest output, audit-flagged). Include
  `backtest_run_id`, `evaluation_artifact_version`, multi-window fields.
- Add to strategy record template: `strategy_thesis_en`, `strategy_thesis_tr`,
  `gate_{1,2,3}_hard_fail` + reasons, `backtest_run_id`,
  `evaluation_artifact_version`, `phase_current` (the N/A discriminator → drives
  which gate bars show vs grey).
- Effort: ~1 day. **[AI: Claude drafts → Barış approves Gate1B mode + structure]**

### Phase 1A — Robustness tool reliability fixes (prereq for hard-gating)
- Both audits: do **not** hard-gate on CPCV/PBO until known bugs fixed.
  - AUDIT-002 CPCV 3-tuple short support (`cpcv_validator.py:86`).
  - AUDIT-005 PBO asymmetric CSCV split (`probabilistic_pbo.py:54`).
  - Add CPCV/PBO `TOOL_FAILED`/`N_A` fallback path (never NaN→auto-fail).
- Effort: ~1 day. **[AI: DeepSeek / Claude Sonnet — narrow tool fixes]**

### Phase 1 — Emit artifacts on 5–10 existing strategies (real data)
- Wire `mega_walk_forward.py` / `single_strategy_backtest.py` to write
  `evaluation_artifact_v1` (collects already-computed max_dd/sharpe/oos/cpcv/pbo/
  B&H into one schema with status envelopes).
- Add a **completeness check**: flag strategies missing B&H, multi-window, or
  CPCV/WFO so backfill (Phase 4) doesn't silently score partial runs.
- Acceptance: run → one valid artifact, every field has status+reason+source.
  Idempotent.
- Effort: ~1–2 days. **[AI: Claude — output schema; DeepSeek per-metric extract]**
- Constraint: read-only on trading logic. Output writer only — no signal/Pine/
  parity change (AGENTS.md).

### Phase 1.5 — Finalize numeric bands from observed distributions
- Take the Phase-1 artifacts, look at real metric ranges, set §3 band cutoffs
  from data (not guessed). Add per-strategy-type trade/duration minimums.
- Effort: ~0.5 day. **[AI: Claude proposes from data → Barış approves bands]**

### Phase 2 — Gate scoring engine (replace build_scorecard)
- New `presentation_reader` functions: `gate1_intake()`, `gate1b_feasibility()`,
  `gate2_backtest()`, `gate3_production()`, plus `repaint_gate()` hard-fail.
- Gate1/1B read existing row/audit/source fields (same inputs current code uses).
- Gate2 reads `evaluation_artifact_v1`; **Gate3 reads
  `production_readiness_artifact_v1`** (audit: Gate3 needs alert/state/risk/
  monitoring evidence that backtest output does not contain). Gate3 stays `N/A`
  until integration/parity/alert evidence exists. Apply §3 bands.
- Hard-fail: REJECT_REPAINT → all downstream `N/A`; PBO≥0.5 → Gate2
  `OVERFIT_SUSPECT` (blocks promotion, not archive).
- Emit as **`scorecard_v2`** alongside legacy `scorecard` — do not overwrite. Keep
  old `build_scorecard()` for one release (rollback + UI migration safety).
- Acceptance: golden-file tests — known strategy → expected per-gate scores.
  Byte-stable on unchanged input.
- Effort: ~2 days. **[AI: Claude — core logic + tests. Cross-model review by
  DeepSeek/Gemini per Gate 5 rule before merge]**

### Phase 3 — Dashboard detail-page redesign (UI)
- Replace single scorecard block with: English thesis title at top, then 4 gate
  bars (+ repaint flag), each expandable to its sub-criteria table with note +
  data source. Color by band (high/med/low) reusing existing `scoreBand()`.
- `phase_current`-driven `N/A` gates render greyed with "needs <phase> data".
- Migrate filters (`pipelineScoreFilter` etc.) + decision panel from numeric
  `score`/`score_band` to **gate status** (audit: filters wired to old composite).
  Read `scorecard_v2`; keep legacy badge one release behind a flag.
- Files: `08_DASHBOARD_APP/apps/web/app.js`, `index.html`, CSS.
- Acceptance: detail page renders all gates from `scorecard_v2`; thin render only
  (no business logic in JS); old composite hidden behind flag.
- Effort: ~1–2 days. **[AI: Claude — frontend-design; Any model for static
  HTML/CSS tweaks]**

### Phase 4 — Backfill + validation
- Backfill artifacts across existing backtested strategies. Use Phase-1
  completeness check to skip/flag partial runs (no B&H, single-window, no CPCV) —
  do not silently score them.
- Spot-check 5–10 strategies: gate scores match manual judgement? Does a known
  curve-fit strategy now correctly hit Gate2 `OVERFIT_SUSPECT`?
- Feed mis-rankings back to Phase 1.5 bands.
- Effort: ~1 day compute + review. **[AI: DeepSeek runs backfill batch; Barış
  validates ranking sanity]**

### Phase 5 — Cleanup (only after stable release)
- Remove `build_scorecard()` legacy flag + legacy badge.
- Update `07_BACKTEST_AND_OPTIMIZATION_RULES.md` to point gates at new engine.
- **Delete `_eval_pipeline_source_TEMP/`** — only now, once canonical rubric +
  schemas + tests + UI all merged and stable.
- Effort: ~0.5 day. **[AI: Claude]**

---

## 6. Effort / benefit summary

| | effort | who | benefit |
|---|---|---|---|
| Phase 0A | 1d | Claude + Barış | rubric mapped, schemas + template defined |
| Phase 1A | 1d | DeepSeek / Sonnet | CPCV/PBO reliable → safe to hard-gate |
| Phase 1 | 1–2d | Claude / DeepSeek | metrics emitted w/ status envelope |
| Phase 1.5 | 0.5d | Claude + Barış | bands set from real data, not guessed |
| Phase 2 | 2d | Claude | edge-weighted scoring (`scorecard_v2`) |
| Phase 3 | 1–2d | Claude | honest multi-gate UI + gate-status filters |
| Phase 4 | 1d | DeepSeek + Barış | validated ranking |
| Phase 5 | 0.5d | Claude | clean repo, TEMP deleted |
| **Total** | **~8–10 days** | | score reflects edge + risk + robustness, not funnel position |

Benefit: high. Moves the score from maturity-weighted → edge-weighted,
risk-adjusted, benchmark-relative, hard-fail-gated. Directly fixes "score is
insufficient and wrong." ~Half of Phase 1 inputs already exist (WFO/CPCV/PBO/B&H),
lowering real cost.

---

## 7. Constraints (carry into every phase)

- No change to trading/Pine/MTC strategy behavior or parity without explicit
  Barış approval (AGENTS.md). This work only **reads** results and **adds output
  writers + scoring + UI**.
- Follow the 7-gate workflow in `AI_RULES.md`. Declare whitelist per phase.
- Gate 5 cross-model review: Phase 2 scoring engine reviewed by a non-author model
  (DeepSeek or Gemini) before merge.
- Keep gates separate. Do not regress to a single composite number.
- Phase 1/2 must be idempotent + golden-file tested.

---

## 8. Open questions for Barış

1. Final numeric bands in §3 — but set in Phase 1.5 from real data, not now.
2. Min trade-count / duration per strategy type (accept source draft, or adjust?).
3. PBO≥0.5 policy — recommend Gate2 `OVERFIT_SUSPECT` (blocks promotion, keeps
   idea), not full reject. Confirm?
4. English thesis title: AI-generated draft per strategy, or Barış-authored?
5. **Gate1B scoring mode**: /50 bar or PASS/FAIL? (recommend /50 + derived PASS
   ≥40, sync decision matrix.)
6. **Gate3 separate `production_readiness_artifact`** — confirm Gate3 stays N/A
   until integration/alert/parity evidence exists (recommended).

---

## 9. Audit log

2026-06-02 — two independent LLM audits reviewed this plan + source rubric.
Both converged; the following were **applied** above:

- Swap order: emit metrics (Phase 1) before finalizing bands (Phase 1.5) — bands
  from observed distributions, not guessed.
- New **Phase 1A**: fix CPCV 3-tuple (AUDIT-002) + PBO split (AUDIT-005) + add
  TOOL_FAILED/N_A fallback before any CPCV/PBO hard-gate.
- **Separate `production_readiness_artifact_v1`** for Gate3 (backtest output can't
  feed alert/state/risk/monitoring criteria).
- **Per-metric status envelope** `{value,status,reason,source_path}` replaces
  "populated or null"; only `OK` scores; tool failure → N_A not auto-fail.
- B&H must be **per-run same-window same-fee** with `excess_alpha`; add
  **multi-window** fields (AGENTS.md promotability rule).
- PBO≥0.5 → Gate2 `OVERFIT_SUSPECT` (block promotion, not archive).
- Rubric gap fixes folded into Phase 0A: add Sharpe/Sortino/recovery/PBO/CPCV as
  Gate2 sub-criteria; resolve Gate1B /50-vs-PASS ambiguity + sync decision matrix;
  de-dup Gate1B/Gate3 signal-contract overlap; score SAFE_WITH_DELAY + define
  NEEDS_MODIFICATION; score parity; raise Rejim Analizi 5→10.
- Template fields added: `strategy_thesis_en/tr`, hard-fail reasons,
  `backtest_run_id`, `evaluation_artifact_version`, `phase_current` (N/A driver).
- UI: emit `scorecard_v2` parallel to legacy; migrate filters/decision panel to
  gate status; keep legacy one release.
- TEMP source folder deleted **only in Phase 5**, not Phase 0.

Not applied / deferred: none material. Remaining judgement calls surfaced as §8
owner decisions.
