# SPRINT_WORKFLOW

Solo-developer loop for working with multiple AI agents
(Codex / Claude) on this repo.

A "sprint" here is one focused work unit - anything from a 5-minute
typo fix to a multi-hour feature. Same loop, different depth.

## The Loop

```
        +-------------------+
        |  0. ORIENT        |  read GLOBAL_HANDOFF + NEXT_STEPS
        +---------+---------+
                  |
                  v
        +-------------------+
        |  1. SCOPE  (G1)   |  prompt 01_office_hours_scope_review
        +---------+---------+
                  |
                  v
        +-------------------+
        |  2. PLAN   (G2)   |  prompt 02_engineering_plan_review
        |  (skip if trivial)|
        +---------+---------+
                  |
                  v
        +-------------------+
        |  3. IMPL   (G3)   |  prompt 03_implementation_task
        +---------+---------+
                  |
                  v
        +-------------------+
        |  4. QA     (G4)   |  prompt 05_qa_test_review
        +---------+---------+
                  |
                  v
        +-------------------+
        |  5. REVIEW (G5)   |  prompt 04_adversarial_code_review
        |  DIFFERENT MODEL  |  (Codex impl -> Claude review, etc.)
        +---------+---------+
                  |
                  v
        +-------------------+
        |  6. SEC    (G6)   |  prompt 06_security_review
        |  (only if hits    |
        |   security surf.) |
        +---------+---------+
                  |
                  v
        +-------------------+
        |  7. HANDOFF (G7)  |  prompt 07_handoff_update
        |  MANDATORY        |
        +-------------------+
```

## Cross-Model Pairing

Two-tier model (see `AGENTS.md`): the **Lead** orchestrates + owns acceptance; the **Implementer** (counterpart flagship CLI) does the work. Cline/DeepSeek are the implementer's sub-delegation tools, not the lead's.

| Step                 | Model role      | Notes                                    |
|----------------------|-----------------|------------------------------------------|
| Scope (G1)           | **Lead**        | Lead owns scope definition and acceptance authority; surfaces counterpart-unavailable blocker here |
| Plan (G2)            | Implementer     | Same model that will write code; Lead accepts plan before G3 starts |
| Impl (G3)            | Implementer     | Stay in scope from G1                    |
| QA (G4)              | Implementer     | Self-QA; produces evidence for Lead review at G5 |
| Review (G5)          | **Lead**        | Lead's independent inspection. Exact roster: see `AGENTS.md` CANONICAL AUDIT ROSTER (Claude: `claude-opus-4-8`+`xhigh`; Codex: `gpt-5.6-sol`+`high`/`xhigh`). Fresh session. Verdicts: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK. <=3 repair rounds. |
| Security (G6)        | Lead / independent | Must not be the implementer of the same change; Lead retains acceptance. Roster: same as G5 but always `xhigh`. |
| Handoff (G7)         | **Lead**        | Lead's final repository write-back; executed only after an accepting G5 verdict (PASS or PASS-WITH-NITS) and G6 if applicable. Implementer may supply factual inputs but the write-back is Lead-owned |

If the reviewer model flags something serious: loop back to Plan or Impl.
Do not merge a review-flagged change without resolving it.

## Sprint Size Guidance

- **5-minute typo / doc** -> G1 + G3 + G5 + G7. Skip G2, G4, G6.
- **Single-function fix** -> G1 + G3 + G4 + G5 + G7.
- **Feature / refactor**  -> Full loop, all gates.
- **Pine / parity / MTC** -> Full loop **plus** explicit Barış approval
  before G3 starts.

## When to Stop a Sprint

- Reviewer (G5) finds a blocker -> stop, fix or revert.
- Parity regression risk surfaces -> stop, surface to Barış.
- Scope creep detected -> stop, restart at G1 with new scope.
- Out of context window -> stop at the nearest gate boundary. BEFORE an
  accepting G5 verdict: do NOT write G7 or any repository handoff file;
  provide only a transient non-repository chat/session handoff for a
  fresh session. Only after an accepting G5 (and G6 if applicable) may
  the Lead perform the G7 repository write-back.

## Entry Points for a Fresh Agent

- Starting cold: `START_HERE.md` -> `AI_RULES.md` -> this file.
- Resuming work: `GLOBAL_HANDOFF.md` -> `NEXT_STEPS.md` -> pick the gate
  prompt that matches the next step.
