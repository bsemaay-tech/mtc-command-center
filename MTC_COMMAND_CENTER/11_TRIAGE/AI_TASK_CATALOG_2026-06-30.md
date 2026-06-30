# AI Task Catalog — every job the AI runs on Barış's command

Source for the planned **AI Task** dashboard tab. Synthesized from `04_SHARED/prompts/05_ai_workflow/`,
`03_QUANTLENS/_user_guide/`, the backtest runbook + lessons, and the 2026-06 onboarding work.
Each job names: what it does · read-first · key tools · safety/gates · modular knobs.

Barış's original 4 are marked **[B1]–[B4]**; everything else is added (the gaps).

---

## A. Strategy research lifecycle (transcript → live candidate)

**A1. Transcript / video / screenshot → strategy intake** **[B2 part]**
Extract a strategy from a user-supplied transcript/screenshot, route it, create the `STGxxx`
candidate + deterministic spec.
- Read: `_user_guide/09_TRANSCRIPT_INTAKE_WORKFLOW.md`, `02_WHAT_TO_DO_WITH_A_NEW_YOUTUBE_VIDEO.md`.
- Tools: `tools/route_user_intake.py`, `tools/markitdown_ingest.py` (binary docs first), `tools/build_strategy_research_registry.py`.
- Input: files in `00_INBOX/USER_INTAKE/`.

**A2. Strategy scoring (Scorecard v2 / gates)** **[B2 part]**
Run Gate 1/1B/2/3 scorecard on a candidate → `scorecard_v2/*.scorecard.json`.
- Read: `_user_guide/12_STRATEGY_EVALUATION_RUBRIC.md`, `13_GATE_SCORECARD_V2_TR.md`, `07_BACKTEST_AND_OPTIMIZATION_RULES.md`.
- Rule: Scorecard is the ONLY scoring authority.

**A3. QuantLens / AI verdict** **[B2 part]**
Author a labels-only verdict (8-token decision tree).
- Read: `03_QUANTLENS/_user_guide/13_AI_VERDICT_AUTHORING_PROCEDURE.md`.
- Authority: only Claude/Codex author+commit; others propose. Labels only, never a number.

**A4. Pipeline triage / promotion decision** **[B3]**
Review all strategies, decide advance / hold / reject; rank.
- Read: `12_STRATEGY_EVALUATION_RUBRIC.md` (Final Decision Matrix), `00_AGENT_PROTOCOLS/NO_PROMOTION_SAFETY_RULES.md`.
- Hard rule: never promote without `robust_final` true.

**A5. Per-strategy backtest-space design** **[B4]**
For each strategy, pre-define its backtest+optimization space (symbols, TFs, param grid, gates) so
the night run is planned in advance (avoids the A22 "what do I even run" waste).
- Output: a run-plan menu Barış picks from before launching A6.
- Read: `07_BACKTEST_AND_OPTIMIZATION_RULES.md` §8, `tools/build_run_plan.py`.

## B. Backtest / optimization

**B6. Overnight / timed backtest + optimization sweep** **[B1]**
Run a sweep per the 4-gate rules, resumable, keep-awake, A22-disciplined.
- Read (Gate-0, mandatory): `AGENTS.md` DATA & LAUNCH → `START_HERE` → `07_BACKTEST_AND_OPTIMIZATION_RULES.md` → `11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md` → **newest `lessons_archive/*`**.
- Engine: `tools/mega_walk_forward.py` + `MEGA_BUNDLE_MANIFEST`. Resume: `--resume`/`--checkpoint-every`.
- Safety: keep-awake + checkpoint-resume + reboot hook; **A22** runtime↔budget (fill with heavy-validation or release machine; never idle-awake; never re-run a deterministic sweep).

**B7. Heavy-validation tier** *(the gap that wasted 2026-06-29)*
On survivors/most-traded cells: ±2-step pre-registered grid, 50k bootstrap, multi-seed DSR
stability, full CPCV, PBO, more symbols/TFs. This is the NON-identical work that fills a long budget.

**B8. Morning close** *(missing from B's list)*
Aggregate → alpha vs buy&hold → morning report → dashboard ingest verify → lessons write-back.
- Read: runbook §6.4. Tools: `aggregate_overnight_iters.py`, `alpha_vs_buyhold.py`.

**B9. Results → MTC Command Center ingest** *(missing)*
Produce/validate the right artifact so the dashboard shows the result.
- Read: `11_TRIAGE/RESULTS_TO_DASHBOARD_MAP_2026-06-29.md`. Never fabricate `backtest_profile_result.json`/`top_results.json`.

## C. Data

**C10. Data acquisition** *(missing)* — download/validate/normalize a new dataset → bundle+manifest → register in `03_QUANTLENS/data/README.md`. Tool: `tools/alpaca_download_dataset.py`.
**C11. Data validation/consolidation** *(missing)* — validate raw CSV exports (timestamps, OHLC sanity, gaps, session), consolidate.

## D. Engineering / repo

**D12. Implementation task** *(missing)* — bounded code change, TDD, repo-guard, PR. Read: `prompts/05_ai_workflow/03_implementation_task.md`.
**D13. Code review / adversarial review / QA / security review** *(missing)* — prompts `04`, `05`, `06`.
**D14. Cross-model board review** *(missing, approval-gated)* — `_deepseek_driver/board_runner.py`.
**D15. Repo audit / cold-onboarding self-test** *(missing)* — `11_TRIAGE/COLD_ONBOARDING_AUDIT_PROMPT_v2_2026-06-29.md`.
**D16. Dispatch mechanical work to DeepSeek** *(missing)* — token discipline, `_deepseek_driver/ds_agent.py`.

## E. Ops / housekeeping

**E17. Handoff / memory write-back (Gate 7)** *(missing)* — `prompts/05_ai_workflow/07_handoff_update.md`.
**E18. Dashboard serve + verify** *(missing)* — read-only `mcc_readonly serve`; verify `backtest_reader`.
**E19. Long-run monitoring** *(missing)* — `run_emitter_supervisor.py` + `run_watchdog.py`.
**E20. UI / Impeccable design pass** *(missing)* — frontend polish on the dashboard.

---

## Gaps in Barış's original list (what was missing)
B's 4 covered the **research lifecycle core** (intake/score/verdict = A1–A3, triage = A4, per-strategy space = A5) + overnight run (B6). **Missing:** heavy-validation tier (B7), morning close (B8), dashboard ingest (B9), data acquisition/validation (C10–C11), all engineering/review jobs (D12–D16), and ops (E17–E20). The most consequential addition is **B7 heavy-validation** — it's the work that makes a long night productive instead of idle (A22).

---

## Modular prompt templates (AI Task tab content)

Short, knob-driven. `{...}` = a knob Barış edits before sending.

### T1 — Overnight backtest + optimization
```
Run an overnight backtest + optimization. First do the Gate-0 pre-read (AGENTS.md DATA & LAUNCH,
07_BACKTEST_AND_OPTIMIZATION_RULES.md, 11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md, and the NEWEST
11_TRIAGE/lessons_archive/ file). Budget: {HOURS=14}h, target ~{CASES=1,000,000}.
Strategies: {ALL | LIST: <ids> | RECOMMEND_TOP: pick the highest-potential and tell me which}.
Take keep-awake + checkpoint-resume + power-loss reboot-resume measures. Apply A22: estimate
runtime vs budget; if the sweep finishes short, fill the rest with the heavy-validation tier
(±2 grid, 50k bootstrap, multi-seed DSR, CPCV-all, PBO) instead of idling — never re-run a
deterministic sweep, never keep an idle machine awake. Don't ask me anything. In the morning do the
full close (aggregate, alpha, MORNING_REPORT, dashboard verify, lessons write-back). Promote nothing
without robust_final.
```

### T2 — Transcript → strategy intake + score + verdict
```
A strategy transcript/screenshot is in 00_INBOX/USER_INTAKE ({FILE=auto-detect}). Read
03_QUANTLENS/_user_guide/09_TRANSCRIPT_INTAKE_WORKFLOW.md. Extract the strategy, route it, create
the STG candidate + deterministic spec, run the Scorecard, then author a QuantLens verdict per
03_QUANTLENS/_user_guide/13_AI_VERDICT_AUTHORING_PROCEDURE.md. Confirm it shows in the dashboard.
Score numbers come only from the Scorecard; the verdict is labels only.
```

### T3 — Pipeline triage (which strategies advance)
```
Review all strategies in the Command Center. Using 12_STRATEGY_EVALUATION_RUBRIC.md + the gates,
decide advance / hold / reject for each and give me a ranked list with reasons. Do not promote
anything without robust_final. Scope: {ALL | only NEEDS_CLARIFICATION | only scored}.
```

### T4 — Design the per-strategy backtest space (pre-plan the night)
```
For {ALL strategies | <ids>}, design each one's backtest+optimization space (symbols, timeframes,
param grid, gates) on the multi-asset bundle, and output a run-plan MENU I can pick from before
tonight's run. Recommend the {N=5} highest-potential cells to prioritize. No execution yet.
```

### T5 — Data acquisition (new dataset)
```
Acquire {SYMBOLS} at {TIMEFRAMES} via {alpaca}. Validate (timestamps/OHLC/gaps/session), normalize,
build the bundle + manifest, and register it in 03_QUANTLENS/data/README.md. Don't run a backtest.
```

Knobs summary: **T1** HOURS, CASES, strategies(ALL/LIST/RECOMMEND_TOP) · **T2** FILE · **T3** scope ·
**T4** strategies, N · **T5** symbols, timeframes, provider.

---

## Phase 1 — AI Task dashboard tab (proposal)
A read-only **AI Tasks** tab that renders these templates as **copy-able prompt cards** (title +
short prompt + "copy" button + the editable knobs shown inline). Barış copies, tweaks a knob,
pastes to the AI. Open design choice: serve the templates as a small JSON via the read-only API
(easy to edit/extend without touching app.js) vs. inline in app.js. Recommend JSON-driven.
