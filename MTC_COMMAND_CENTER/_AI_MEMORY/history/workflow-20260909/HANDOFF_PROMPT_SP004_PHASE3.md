# Handoff Prompt — paste into a new chat to continue

You are resuming work on the **Tradingview_LAB_CLEAN** repo (`C:\LAB\Tradingview_LAB_CLEAN`).
Read `AGENTS.md`, then `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`, then `NEXT_STEPS.md`.
Use the token-efficient dispatch workflow. Update handoff files before stopping.

---

## OVERRIDING DIRECTIVE (Barış, standing)

Do NOT stop. Keep doing every reader-side task you can by **dispatching mechanical read/edit work to DeepSeek and Grok**, never stopping, never asking for confirmation on things you can decide. Token efficiency is the #1 rule — Claude weekly credit is scarce. Claude only keeps the **decisions, specs, and audits**; cheap models do the file labor.

**Workflow contract (mandatory):**
1. Claude writes a tight task spec → JSON to `C:/tmp/<name>_task.json`.
2. Dispatch via `python _deepseek_driver/ds_agent.py C:/tmp/<name>_task.json` (DeepSeek primary, Grok `grok-4` backup, OpenRouter fallback).
3. Model returns a report (`C:/tmp/ds_*_report.md`) + transcript.
4. **Claude audits the report AGAINST REALITY** — do not trust the model's self-report. Re-read the actual file it wrote, run `py_compile`, run the script on the real 149-artifact dataset, confirm schema validity, check for fabricated numbers. Only then accept.
5. Never let cheap models touch the HARD denylist (`*.pine`, `parity`, `MTC_V2`, `.git`). Harness enforces this; do not override.

The harness, providers table, task JSON schema, and safety rails are documented in `_deepseek_driver/README.md`. Read it first if unsure.

---

## HARD CONSTRAINTS (do not violate)

- **Do NOT change trading logic, Pine logic, MTC strategy behavior, or TradingView parity without explicit Barış approval** (AGENTS.md).
- Commit / push ONLY when Barış explicitly says so. (Many Batch A–J edits + untracked files are uncommitted — leave them for Barış.)
- Be skeptical. No auto-praise. Report honest INCOMPLETE/FAIL outcomes; never fabricate or auto-zero a metric to make a gate look scorable.
- Caveman mode may be active (terse Turkish/English). Code, commits, security: write normal prose.
- Serialize same-file DeepSeek tasks (no parallel writes to one file).

---

## WHERE THINGS STAND (SP-004 — strategy-evaluation scorecard redesign)

**DONE (audited on real 5.1MB MEGA data, 149 strategies):**
- `06_SCHEMAS/evaluation_artifact_v1.schema.json` — parity moved to advisory `flags.parity_status ∈ {PASS,WARN,N_A,null}`; metrics use status-envelope vocabulary.
- `03_QUANTLENS/tools/build_evaluation_artifact.py` (Phase 1) — `build_artifact(mega_row,cpcv_row,pbo,run_id)`; CLI `--mega --cpcv --pbo --out-dir`. Emits status-enveloped metrics (OK only when computed, else `NOT_COMPUTED`/`N_A`, never auto-zero). 149 artifacts, 0 schema errors, 0 fabricated.
- `03_QUANTLENS/tools/score_gate2.py` (Phase 2) — `score_gate2(artifact)->dict`; CLI `--in-dir --out-dir`. 25 criteria /100 per rubric §5.1–5.7; non-OK metric → unscored → gate `INCOMPLETE`; `REJECT_REPAINT`→`FAIL`; `PBO≥0.5`→`OVERFIT_SUSPECT` advisory; parity advisory; `pass=(status=='OK' and score>=75)`. Result: 149 scorecards all `INCOMPLETE` (22–43, 0 pass, 0 fabricated). **This is the CORRECT status-envelope outcome**, not a bug — MEGA simply doesn't emit ~17 of the Gate-2 metrics yet.

**Rubric / decisions (signed):** `03_QUANTLENS/_user_guide/12_STRATEGY_EVALUATION_RUBRIC.md` (D1–D6 applied); `_AI_MEMORY/DECISIONS.md` D004–D007.

---

## IMMEDIATE NEXT TASK — SP-004 Phase 3 (reader-side, NO approval needed)

Build the remaining gate scorers, mirroring `score_gate2.py` exactly:

1. **`score_gate1.py`** — Gate 1 intake /100 (rubric §"Gate 1").
2. **`score_gate1b.py`** — Gate 1B feasibility /100, PASS≥75 (D1: rescaled ×2 to /100). Reads `flags.parity_status` as **advisory** (WARN never blocks).
3. **`score_gate3.py`** — Gate 3 production-readiness /100. (D4: Gate3 is a separate artifact — check whether it reads `evaluation_artifact_v1` or `production_readiness_artifact_v1`; consult the rubric + `06_SCHEMAS/production_readiness_artifact_v1.schema.json` before specifying the task.)

All three MUST follow the same rules as Gate 2:
- Pure function `score_gateX(artifact)->dict`, plus CLI `--in-dir --out-dir`.
- Layer output into the SAME `scorecard_v2` structure (`{strategy_id, gateX:{score,max,sub_scores[],status,pass,...}, flags:{parity_status}, notes}`).
- Status-envelope rule: only `OK` metrics score; any non-OK → `points_awarded=None`, gate `INCOMPLETE`; never auto-zero/fabricate. Only `REJECT_REPAINT` or an explicit numeric failure may zero/fail.
- Add `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` in `main()` (cp1254 crashes on `→`/Unicode otherwise — known bug, already bit us twice).

**Per scorer, the dispatch loop:**
1. Claude extracts the exact rubric section for that gate into a small `C:/tmp/rubric_gateX.md` (keep the read-cap small — harness caps read_file at 60KB; pre-trim a sample artifact too, like the existing `C:/tmp/sp004_sample_inputs.json`).
2. Claude writes `C:/tmp/gateX_task.json` (`{title, provider, model, max_iters, report_out, allow[], read_extra[], prompt}`), `allow` scoped to the one new file under `03_QUANTLENS/tools/`.
3. Dispatch to DeepSeek (Grok backup). Wait for it to finish before the next same-area task.
4. **Claude audit:** re-read the written file; `py_compile`; run on the real 149 artifacts; confirm `scorecard_v2` shape, INCOMPLETE/FAIL logic, no fabricated numbers, no auto-zero. Fix inline only if a 1-liner is cheaper than a round-trip.
5. Log the batch in `SESSION_LOG.md`, mark progress in `NEXT_STEPS.md`.

Optionally finish with a **unified `score_all_gates.py`** that composes Gate1+1B+2+3+repaint into one `scorecard_v2` per strategy (still never recollapsing to a single number).

---

## DO **NOT** START WITHOUT BARIŞ APPROVAL

- **SP-004-METRIC-ENRICHMENT** (OPEN) — enriching `mega_walk_forward.py` to emit the ~17 missing Gate-2 metrics (sharpe, sortino, recovery_factor, worst_window_drawdown_pct, max_consecutive_losses, calendar_days, regime_coverage_count, top_trade_concentration, long_short_ratio, param_stability_score, multi_window_pass, net_after_fees_pct, net_after_slippage_pct, avg_trade_vs_cost, equity_curve_health, return_pct_compound, benchmark/regime fields) + running CPCV across all PASS cells. **Backtest-side = touches MTC strategy output → approval-gated.** Until done, INCOMPLETE is the correct honest status. Do NOT auto-start.
- Re-running the sweep under D006 disjoint-fold geometry (Barış OPS).
- Adding US-equity data for the 4 OR strategies (Barış OPS).
- Any commit/push.

---

## DOWNSTREAM (after Phase 3)

- **Phase 1.5** — finalize numeric bands from REAL distributions (needs Barış sign-off).
- **Phase 3 dashboard / SP-005 Wave C** — render `scorecard_v2` gate bars in the strategy-detail page from real artifacts only (no faked gates). Depends on this Phase 3 output existing.
- **SP-005 Wave B** — read-only `quantlens_reader.py` over existing salvage YAML/markdown (reader-side, dispatchable).

---

## KEY FILES

- Harness: `_deepseek_driver/ds_agent.py` + `_deepseek_driver/README.md`
- Phase 1/2: `03_QUANTLENS/tools/{build_evaluation_artifact.py, score_gate2.py}`
- Schemas: `06_SCHEMAS/{status_envelope, evaluation_artifact_v1, production_readiness_artifact_v1}.schema.json`
- Rubric: `03_QUANTLENS/_user_guide/12_STRATEGY_EVALUATION_RUBRIC.md`
- Decisions: `_AI_MEMORY/DECISIONS.md` (D004–D007)
- Handoff: `_AI_MEMORY/{SESSION_LOG.md, NEXT_STEPS.md, GLOBAL_HANDOFF.md, ACTIVE_FILES.md}`
- Sample inputs for dispatch: `C:/tmp/sp004_sample_inputs.json`, `C:/tmp/rubric_gate2.md`

Start by reading `AGENTS.md` + the three handoff files, then dispatch `score_gate1.py` to DeepSeek. Audit against reality. Keep going.
