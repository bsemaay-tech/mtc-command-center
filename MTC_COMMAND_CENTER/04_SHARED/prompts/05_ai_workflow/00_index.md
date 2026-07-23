# 05_ai_workflow - index

GStack-inspired, repo-local workflow prompts. Generic across AI agents
(Codex / Claude). Tied to the memory layer at
`MTC_COMMAND_CENTER/_AI_MEMORY/`.

## Read first

1. `AGENTS.md` (repo root)
2. `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`
3. `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md`
4. `MTC_COMMAND_CENTER/_AI_MEMORY/SPRINT_WORKFLOW.md`

## Prompts

| #  | File                                  | Gate  | Actor                        | Use when                              |
|----|---------------------------------------|-------|------------------------------|---------------------------------------|
| 01 | `01_office_hours_scope_review.md`     | G1    | **Lead**                     | Before coding anything new            |
| 02 | `02_engineering_plan_review.md`       | G2    | Implementer -> Lead accepts   | Before architecture / multi-file change |
| 03 | `03_implementation_task.md`           | G3    | Implementer                  | When actually writing the code        |
| 04 | `04_adversarial_code_review.md`       | G5    | **Lead** (independent)       | Lead's adversarial inspection of the diff |
| 05 | `05_qa_test_review.md`                | G4    | Implementer (self-QA)        | Self-QA before handing evidence to lead |
| 06 | `06_security_review.md`               | G6    | Lead / independent           | Only if security surface touched      |
| 07 | `07_handoff_update.md`                | G7    | **Lead** (after sequence: accepting G5, G6 if applicable, G7) | Mandatory final write-back     |
| 08 | `08_backtest_launch.md`               | Stage 0-7 | two-tier by stage            | Any backtest (in-day single / sprint / overnight) |

## Conventions

- Every prompt ends with a **WRITE-BACK** block listing which
  `_AI_MEMORY/` files to update afterward.
- Prompts do **not** create new memory files at repo root. They update
  the canonical ones inside `_AI_MEMORY/`.
- Two-tier model (see `AGENTS.md`): **Lead** owns G1 (scope), G5 (independent review), G6 (or delegates to independent reviewer with lead acceptance), and G7 (final write-back after an accepting G5 verdict (PASS or PASS-WITH-NITS)). **Implementer** owns G2 (plan, passed to lead for acceptance), G3 (impl), and G4 (self-QA producing evidence for lead). Cheap models (DeepSeek, Cline) are implementer sub-delegation only. Fable and Gemini are advisory/non-gate reviewers - they may supplement but never replace a canonical Claude/Codex gate audit.
- Cross-model review (Gate 5) is mandatory for every repository change/write task, including trivial typo/doc work - it is the **Lead's** independent inspection gate, not the implementer's. See `AGENTS.md` two-tier model and CANONICAL AUDIT ROSTER.
