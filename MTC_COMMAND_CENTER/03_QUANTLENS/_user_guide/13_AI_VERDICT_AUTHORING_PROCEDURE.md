# 13 — AI / QuantLens Verdict Authoring Procedure (canonical)

**Why:** cold-onboarding audits (6 models, 2026-06-29) unanimously flagged **W4** as the worst
remaining gap — the QuantLens expert-verdict layer is shipped (registry + reader + dashboard) but
had **no documented procedure for how a verdict is produced**, so two agents would label the same
strategy differently. This file is that procedure. Following it, two authors with the same evidence
must reach the **same** decision token.

## What a verdict is (and is not)
- A QuantLens verdict is an **opinion/label layer** on a strategy: a decision token + qualitative
  reasons. It is rendered in the Strategy-Detail "Verdict & Decision" block.
- It is **NEVER a number.** The **Scorecard is the only scoring authority.** A verdict *cites*
  scorecard evidence via `score_reference`; it never restates or invents metrics.
- Registry: `05_REGISTRY/AI_QUANTLENS_VERDICT_REGISTRY.json`. Reader (read-only, auto):
  `08_DASHBOARD_APP/apps/api/mcc_readonly/expert_quantlens_reader.py`. No UI work to publish — the
  dashboard reads the registry.

## Who may author (authority)
- **Only Claude or Codex may author and commit a verdict.** Other models (DeepSeek, etc.) may
  produce a **proposal/draft**, but a verdict only lands after **Claude or Codex reviews, confirms
  the decision token against the tree below, and commits it.** The reviewing model owns correctness.

## Mandatory inputs (gather before deciding)
1. The source/spec state: is there a readable, deterministic rule set? Is the source open or a
   closed/paid black box?
2. Implementation complexity (`complexity_score`, 0–10).
3. Linked Scorecard evidence (`scorecard_v2/*.scorecard.json`): Gate 1/1B/2/3 state, `robust_final`,
   DSR confidence, cross-symbol cell count, buy&hold/alpha — via the strategy's scorecard.
4. Universe-mismatch / data-provenance flags.

If you cannot obtain (1) or (3), the decision is a stop/clarification token — do not guess a
PASS/REJECT.

## Deterministic decision tree (evaluate top to bottom; first match wins)

**Stop / pre-evidence states:**
1. Source is a **closed / paid / black-box** indicator (rules not inspectable) → `CLOSED_SOURCE_STOP`.
2. Source readable but **fundamentally unsound** (lookahead/repaint, no real rule, nonsense) → `GARBAGE`.
3. Rules implementable but **`complexity_score ≥ 8/10`** → `COMPLEXITY_OVERLOAD`.
4. Source/rules **ambiguous** — no deterministic spec can be written, OR **no linked scorecard
   evidence** exists yet → `NEEDS_CLARIFICATION`.

**Evidence-based states** (deterministic spec exists AND scorecard_v2 evidence is linked):
5. Scorecard is **robust** — Gate 2 PASS **and** `robust_final = true` (i.e. PASS ∧ bh_fdr_survivor ∧
   dsr_robust, DSR confidence ≥ 0.95) → `PASS` (advance to technical scoring / promotion track).
   *(Strict, per owner decision: a non-robust positive is NOT a PASS.)*
6. Tested; only a **partial edge in a subset/regime**, not robust overall, **but a reusable
   component/idea is worth keeping** → `SALVAGE`.
7. Tested; no robust edge and **no reusable component to extract**, but worth keeping as a documented
   research note → `RESEARCH_ONLY`.
8. Tested; **clearly no edge** (net-negative / dominated by buy&hold) and nothing salvageable →
   `REJECT`.

(Decision labels for the UI come from §4.4 of `11_STRATEGY_DETAIL_PAGE_REDESIGN_PLAN.md`.)

## Authoring rules
- **Labels only.** `commercial_value`, `literature_relevance`, `testability`, `complexity` are
  qualitative strings — never numeric scores. Put the scorecard pointer in `score_reference`.
- **One entry per `strategy_id`.** A verdict is **revisable**: when new scorecard evidence lands,
  update the entry and bump `generated_at` + set `source`.
- Two authors, same evidence → same decision token. If your token isn't forced by the tree, you are
  missing an input — go back to "Mandatory inputs".

## Registry entry schema (write/update one object in `entries[]`)
`strategy_id`, `strategy_display_name`, `decision` (one of the 8 tokens), `decision_label`,
`reason`, `can_test`, `blocking`, `next_action`, `commercial_value`, `literature_relevance`,
`testability`, `complexity`, `risk_flags` (list), `score_reference`, `source`.
Top-level: bump `generated_at`, set `model`.

## Approval-gating
- A **single / few** verdicts that follow this tree and write **labels only** → no per-verdict Barış
  approval needed (low risk; Claude/Codex review is the gate).
- A **batch re-verdict** (re-labeling many/all strategies at once) → **requires explicit Barış
  approval** before writing (mass artifact regeneration).
- The registry is data, not protected scope, but it feeds the dashboard — never fabricate, never
  write a number.

## Verify (read-only)
```
cd MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api
python -c "from mcc_readonly.expert_quantlens_reader import build_expert_quantlens; from pathlib import Path; r=build_expert_quantlens(Path('<MCC_ROOT>')); print(r['count'], list(r['by_strategy_id'])[:1])"
```
