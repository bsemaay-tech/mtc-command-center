# 05_ai_workflow — index

GStack-inspired, repo-local workflow prompts. Generic across AI agents
(Codex / Claude / Gemini). Tied to the memory layer at
`MTC_COMMAND_CENTER/_AI_MEMORY/`.

## Read first

1. `AGENTS.md` (repo root)
2. `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`
3. `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md`
4. `MTC_COMMAND_CENTER/_AI_MEMORY/SPRINT_WORKFLOW.md`

## Prompts

| #  | File                                  | Gate | Use when                              |
|----|---------------------------------------|------|---------------------------------------|
| 01 | `01_office_hours_scope_review.md`     | G1   | Before coding anything new            |
| 02 | `02_engineering_plan_review.md`       | G2   | Before architecture / multi-file change |
| 03 | `03_implementation_task.md`           | G3   | When actually writing the code        |
| 04 | `04_adversarial_code_review.md`       | G5   | Different model reviews the diff      |
| 05 | `05_qa_test_review.md`                | G4   | Run tests / lint / verify             |
| 06 | `06_security_review.md`               | G6   | Only if security surface touched      |
| 07 | `07_handoff_update.md`                | G7   | Mandatory before stopping             |
| 08 | `08_backtest_launch.md`               | G0-G7 | Any backtest (in-day single / sprint / overnight) |

## Conventions

- Every prompt ends with a **WRITE-BACK** block listing which
  `_AI_MEMORY/` files to update afterward.
- Prompts do **not** create new memory files at repo root. They update
  the canonical ones inside `_AI_MEMORY/`.
- Cross-model review (Gate 5) is mandatory for any non-trivial change.
