# SPRINT_WORKFLOW

Solo-developer loop for working with multiple AI agents
(Codex / Claude / Gemini) on this repo.

A "sprint" here is one focused work unit — anything from a 5-minute
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

| Step                 | Model role  | Notes                                    |
|----------------------|-------------|------------------------------------------|
| Scope (G1)           | Either      | Pick whichever has the freshest context  |
| Plan (G2)            | Implementer | Same model that will write code          |
| Impl (G3)            | Implementer | Stay in scope from G1                    |
| QA (G4)              | Implementer | Self-test before handing off             |
| Review (G5)          | **Other**   | Must be a different model. Adversarial.  |
| Security (G6)        | Either      | Skip if not security-touching            |
| Handoff (G7)         | Implementer | Whoever did the work updates memory      |

If the reviewer model flags something serious: loop back to Plan or Impl.
Do not merge a review-flagged change without resolving it.

## Sprint Size Guidance

- **5-minute typo / doc** → G1 (1 line) + G3 + G7. Skip G2, G4, G5, G6.
- **Single-function fix** → G1 + G3 + G4 + G5 + G7.
- **Feature / refactor**  → Full loop, all gates.
- **Pine / parity / MTC** → Full loop **plus** explicit Barış approval
  before G3 starts.

## When to Stop a Sprint

- Reviewer (G5) finds a blocker → stop, fix or revert.
- Parity regression risk surfaces → stop, surface to Barış.
- Scope creep detected → stop, restart at G1 with new scope.
- Out of context window → stop at the nearest gate boundary, write G7,
  hand off to next session via `GLOBAL_HANDOFF.md` + `NEXT_STEPS.md`.

## Entry Points for a Fresh Agent

- Starting cold: `START_HERE.md` → `AI_RULES.md` → this file.
- Resuming work: `GLOBAL_HANDOFF.md` → `NEXT_STEPS.md` → pick the gate
  prompt that matches the next step.
