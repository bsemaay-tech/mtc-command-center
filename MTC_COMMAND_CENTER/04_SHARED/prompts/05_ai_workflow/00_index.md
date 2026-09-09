# Workflow prompts

Follow root `AGENTS.md` and `CONTEXT_MAP.md`: one stage AGENTS at startup; selected INPUTS/TESTS
before writes/execution, relevant HANDOFF on resume, OUTPUTS before delivery. Search matching
DECISIONS rows. Load only the current prompt and its triggered sources.

The seven gates are logical checks, not seven meetings. One small task can combine scope,
plan and QA in its existing brief. Use consequence-based `../../../00_AGENT_PROTOCOLS/REVIEW_POLICY.md`
for classification and review; templates do not create a second review policy.

| Prompt | Use |
|---|---|
| `01_office_hours_scope_review.md` | Lead's scope and completion/QA brief, G1/G2/G4 outline |
| `02_engineering_plan_review.md` | Additional design detail only when the task needs it |
| `03_implementation_task.md` | Builder's scoped implementation and self-QA |
| `04_adversarial_code_review.md` | Required fresh review and Lead independent reproduction |
| `05_qa_test_review.md` | Meaningful working path and repeatable evidence |
| `06_security_review.md` | Applicable independent security check using the same packet |
| `07_handoff_update.md` | Factual progress/blocked/accepted write-back with honest boundaries |
| `08_backtest_launch.md` | Existing specifically authorized backtest contract; unchanged |

Low-risk work needs no automatic two-flagship builder pair. Preserve explicit protected contracts,
actual review obligations, ordinary local-commit authority and separate push/merge gates.
