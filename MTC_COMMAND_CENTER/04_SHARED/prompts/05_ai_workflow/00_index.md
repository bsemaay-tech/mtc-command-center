# 05_ai_workflow — index

GStack-inspired, repo-local workflow prompts. Generic across AI agents
(Codex / Claude / Gemini). Tied to the memory layer at
`MTC_COMMAND_CENTER/_AI_MEMORY/`.

## Read first

1. Read root `AGENTS.md` and root `DECISIONS.md`.
2. Use root `CONTEXT_MAP.md` to select exactly one stage.
3. Read that stage's `AGENTS.md`, `INPUTS.md`, `OUTPUTS.md`, `TESTS.md`, and `HANDOFF.md`.
4. Read this index and only the prompt for the current gate.

## Prompts

| #  | File                                  | Gate  | Actor                        | Use when                              |
|----|---------------------------------------|-------|------------------------------|---------------------------------------|
| 01 | `01_office_hours_scope_review.md`     | G1    | **Lead**                     | Before coding anything new            |
| 02 | `02_engineering_plan_review.md`       | G2    | Implementer → Lead accepts   | Before architecture / multi-file change |
| 03 | `03_implementation_task.md`           | G3    | Implementer                  | When actually writing the code        |
| 04 | `04_adversarial_code_review.md`       | G5    | **Lead** (independent)       | Lead's adversarial inspection of the diff |
| 05 | `05_qa_test_review.md`                | G4    | Implementer (self-QA)        | Self-QA before handing evidence to lead |
| 06 | `06_security_review.md`               | G6    | Lead / independent           | Only if security surface touched      |
| 07 | `07_handoff_update.md`                | G7    | **Lead** (after tier-required acceptance/self-verification) | Mandatory final write-back |
| 08 | `08_backtest_launch.md`               | Stage 0–7 | two-tier by stage            | Any backtest (in-day single / sprint / overnight) |

## Conventions

- Every prompt ends with a **WRITE-BACK** block listing which
  `_AI_MEMORY/` files to update afterward.
- Prompts do **not** create new memory files at repo root. They update
  the canonical ones inside `_AI_MEMORY/`.
- Two-tier model (see `AGENTS.md`): **Lead** owns G1 (scope + mandatory audit-tier classification), tier-required G5/G6 review, and G7 final write-back. **Implementer** owns G2 (plan, passed to lead for acceptance), G3 (impl), and G4 (self-QA producing evidence for lead). Cheap models (DeepSeek, Cline) are implementer sub-delegation only.
- GLM supplemental routing (Z.AI Coding Plan model selection for sub-delegation): canonical policy in `AGENTS.md` §GLM SUPPLEMENTAL ROUTING (cheapest-capable tier first; routing record required per task). GLM never replaces a flagship slot required by the audit tier; it may fill the T1 conditional second-opinion or T2 reviewer slot. Gate 1 records planned GLM routing when sub-delegation is anticipated; Gate 3 includes routing record at dispatch.
- Gate 5 follows the permanent audit tier: T0/T1/T2 receive the recorded independent review contract; T3 uses recorded implementer self-verification and invokes no model auditor. See `AGENTS.md` §AUDIT TIER POLICY — PERMANENT DEFAULT.
