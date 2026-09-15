# CODEX PICKUP — 2026-06-08 (Claude Opus 4.8 → Codex)

> **Read this first when picking up.** Barış's weekly Claude credit ran out; Codex continues. This is the single authoritative handoff for the open work. Source files cited are real and current. Constraints below are binding.

## Hard constraints (unchanged, binding)
- **Read-only dashboard.** Display-only fixes + read-only Python API. The owner ruled out ALL write-back UI permanently (no decision dropdowns, no persisted state from the page).
- **No Pine / MTC_V2 / parity / trading-logic edits without explicit Barış approval.** Denylist enforced in the dispatch harness (`*.pine`, `parity`, `MTC_V2`, `.git` never writable).
- **Token discipline:** dispatch bounded mechanical work to cheap models (`_deepseek_driver/ds_agent.py`); orchestrator does decisions/specs/audits and audits results on REAL data. NOTE: the DeepSeek auto-driver has been throwing `OSError [Errno 22]` on Windows stdout — if it fails, do the edit directly.
- **Commit after every agent** on shared files (app.js) — uncommitted work gets clobbered by the next agent's git checkout.

## Current state snapshot (2026-06-08)
- Frontend single file: `08_DASHBOARD_APP/apps/web/app.js` (vanilla JS, template strings). Readers: `08_DASHBOARD_APP/apps/api/mcc_readonly/{scorecard_reader,read_model,quantlens_reader}.py`.
- Run dashboard: `cd 08_DASHBOARD_APP/apps/api && python -m mcc_readonly serve --port 8765` → `/dashboard`; force refresh `/api/snapshot?refresh=1`.
- Live snapshot: **38 distinct strategies · 360 backtest-run scorecards · 1 promotable.**
- UI Review Round 1 (UI-1..39): 38 shipped, UI-5 parked. Round 2 (R2-*): **8 commits shipped today** (`16c3c58 aaa089a 0f684b8 5a92065 e2bf40b cec2cf6 5f5f1a4` + this handoff), ~26 findings. Full record: `_AI_MEMORY/UI Reviev/ROUND2_PLAN.md` (§7 = 4/4 audit reconciliation, §7.9 = implementation progress).

---

## THE 5 OPEN WORK ITEMS (Barış's priority order)

### 1. Reflect ALL repo night-run results in MCC  ⬅ data/pipeline
**Problem:** MCC's `scorecard_reader.py` only ingests `<run>/scorecard_v2/*.scorecard.json` files whose JSON has `scorecard_version == "v2"`. Several recent night runs wrote their scorecards to `<run>/iter_*/gate2_scorecards/` instead (no `scorecard_v2/` dir, empty `scorecard_version`) → **MCC does not see them.**

**Gap (verified on disk 2026-06-08), runs NOT in MCC:**
| Run dir (under `03_QUANTLENS/05_BACKTEST_RESULTS/`) | scorecards stuck in gate2_scorecards/ |
|---|---|
| `night_1m_2026-06-07` (finished clean 03:53, 5 iters, 0 crash, ~1.08M evals) | 122 |
| `full_sweep_2026-06-07` | 122 |
| `batch023_034_2026-06-07` | 111 |

**Already in MCC (scorecard_v2 present):** `final_gate2_2026-06-05` (38), `heavy_tier_2026-06-05` (72), the 5 analysis runs `enriched_metrics/bh_benchmark/worst_window/annualized_risk/slippage_2026-06-05` (38 each), `fam_templates_2026-06-06` (9), `new_strategies_2026-06-06` (2), `lbr_coil_2026-06-06` (1), `remaining_2026-06-07-recovery` (11, partial). These make up the current 38 strategies / 360 cards.
**Empty/smoke/legacy (ignore):** all `smoke_*`, every `QL_2026-05-01_*` dir, `overnight_research_20260501`, `FOCUSED_VALIDATION`, `confirm_2026-06-04`.

**Fix:** run the enrichment that produces `scorecard_v2/` + Gate2/Gate3 enrich (bridge = `mcc_night_tail.sh`). Pre-read `MTC_COMMAND_CENTER/_AI_MEMORY/NIGHT_BATCHES.md` (esp. **D009 scipy/OpenBLAS hang** rule → must launch via `run_python_clean.py` + `_scipy_shim.py`, NOT bare `python`). Then verify scorecards land in MCC (`/api/snapshot?refresh=1`, distinct count rises above 38).
```bash
cd MTC_COMMAND_CENTER/03_QUANTLENS/tools
for r in night_1m_2026-06-07 full_sweep_2026-06-07 batch023_034_2026-06-07; do
  bash mcc_night_tail.sh "../05_BACKTEST_RESULTS/$r" "$r"
done
```
⚠ Confirm the enrich actually writes `scorecard_v2/*.scorecard.json` with `scorecard_version:"v2"` for these (the launcher format differs). If `mcc_night_tail` doesn't, find/adjust the promotion step. Audit on real data — don't trust the script's report.

### 2. Finish UI Round-2 remaining (minor/backlog), then Barış re-checks  ⬅ display-only
Shipped already (do NOT redo): R2-01/02/06/07/08a/08b/09/10/11/12/14/15/16/17/18/19/20/22/23/24/25/26/27/29/30/32/34/35 + R2-D1 rename. **Remaining:**
- **R2-31** — data-freshness shows the *snapshot* timestamp, not the *scorecard* timestamp (a score could be days old while snapshot is fresh). `snapshotFreshness()` in app.js; needs the displayed scorecard's own timestamp surfaced in the detail header.
- **R2-13-deep** — short "why points deducted" per sub-score. Needs a reason field per `sub_score` from the backend; backlog.
- **R2-36** — a Gate 2 tooltip allegedly references a field that isn't emitted ("ghost requirement"); locate + drop. Unverified, low.
- **R2-04 / R2-05** — verdict ladder (6-level) + badge ladder (3-state) surfaced as graded UI. Audit said BACKLOG (nice-to-have, competes for the single-file app.js owner). If done, do it as a tooltip listing the ladder, NOT a stacked widget.
- Then: **Barış reloads the dashboard + screenshot-verifies** (his review style). Screenshots live in `_AI_MEMORY/UI Reviev/`.

### 3. R2-E — QuantLens = Claude/Codex-authored expert verdict  ⬅ ACTIVE AI WORK (separate project)
The dashboard's old "QuantLens" was the **Gemini GEM intake pre-screen**; it has been **renamed to "Gemini Pre-Screen"** everywhere visible (commit `e2bf40b`). The name **"QuantLens" is now reserved** for the AI's OWN expert verdict that Barış wants.
- **Rubric already written:** `03_QUANTLENS/_user_guide/11_STRATEGY_DETAIL_PAGE_REDESIGN_PLAN.md` §4.2–4.4 (strict skeptical chief auditor; decision states PASS/NEEDS_CLARIFICATION/RESEARCH_ONLY/SALVAGE/REJECT/GARBAGE/CLOSED_SOURCE_STOP/COMPLEXITY_OVERLOAD).
- **Rule:** QuantLens writes **opinion/labels only, NEVER a score** — the only scoring authority is the Scorecard (Gate 2).
- **Work:** manually review each strategy → produce a QuantLens verdict → write to a new data file → dashboard reads it (a new render section, or repurpose). This is serious per-strategy AI work (like item 4), needs its own run + Barış sign-off on the storage format.

### 4. AI-assigned project/strategy names  ⬅ ACTIVE AI WORK
Strategy display names are still raw (UI-5 PARKED earlier by Barış). Many strategies show humanized-id or raw video titles ("8 EMA purple line Amazon trade"). Barış wants AI to assign clean human-readable names per strategy. This is a deliberate per-strategy AI pass (writes a name field the dashboard already prefers via `strategyDisplayName` candidate chain). Decide storage location + run the naming pass.

### 5. Other backlog Barış may not remember (from Claude memory)
- **UI-30 producer_spec field-fill** — many producer_specs missing SL/TP/risk; 3 empty (STG040/055/059). Requires trading-logic + parity → **needs Barış approval**, out of display scope. (RESULT_D7_fieldaudit.md has the field-level audit.)
- **Gate 3 builder MISSING (system-wide)** — no production-readiness scorer exists; every strategy is INCOMPLETE on Gate 3. Building it is a real project. Binding owner decisions in memory `mcc-gate3-promotion-decisions`: Gate3 must be honest (real evidence only), production phased (Pine-parity + dry-run first), DSR-fail + CPCV-robust → FORWARD_PAPER.
- **W1** — wire MTC_V2 parity into the approved night flow (currently parity is in the "autonomous-NOT-allowed" list, runs only on Barış approval; backtest engine = Python producers, MTC_V2 = downstream parity check only).
- **W2** — automatic "needs-backtest" selector (registry: `eligible_for_backtest=true` AND no gate2 scorecard). = NIGHT_BATCHES N5, currently TODO; selection is manual/recipe-based today.
- **Dead code** — `renderDecisionPanel()` in app.js (~line 1299) is defined but never called and harbors a stale "score below 65" blocker source; safe to delete. (A background task chip was spawned for this.)
- **Stray hung processes** — python PIDs 18480 (scipy multiprocessing test, running since 06-07 10:00, likely D009 hang), 57724/21200 (empty-cmd, since 06-06). Kill them or reboot; they're not the night run.
- **STG042 code collision** — resolved in Round 1 (UI-39, commit 1b3812e renamed the rejected triage entry to `Stg042_REJECTED`). Note the new `GEN_*` strategies from the unenriched night runs are a different family from the `QL_*` ones.

---

## Handoff file map (what points where)
- `AGENTS.md` (root) → entry; read order, token discipline, dispatch harness, backtest gates. **Unchanged, current.**
- `CLAUDE.md` (root) → "read AGENTS.md then START_HERE.md". **Unchanged, current.**
- `_AI_MEMORY/START_HERE.md` → hub read-order. Pointer to THIS file added.
- `MTC_COMMAND_CENTER/CURRENT_STATUS.md` + `PROJECT_HANDOFF.md` → older (2026-05-31) baseline narrative; pointer to THIS file added at top. (Their MVP-8 detail is still valid background; the live counts here supersede theirs.)
- `_AI_MEMORY/GLOBAL_HANDOFF.md` → single cross-model log; new dated entry added.
- `_AI_MEMORY/NEXT_STEPS.md` → tagged task list; the 5 items added as `[AI: Codex]`.
- `_AI_MEMORY/UI Reviev/ROUND2_PLAN.md` → the full Round-2 plan + 4-way audit + progress (authoritative for item 2).
- Claude memory (persists for Claude only, Codex can't read): `mcc-ui-review-state`, `mcc-gate3-promotion-decisions` — key facts copied into this file.
