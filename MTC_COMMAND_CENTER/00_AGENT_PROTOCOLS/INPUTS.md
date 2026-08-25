# Governance stage inputs

Read only the rows triggered by the scoped task.

| Trigger | Input |
|---|---|
| Any write | Shared GitHub claim: issue, branch, worktree, exact paths, live-dependency status; check `_AI_MEMORY/SESSION_LOCK.md` as mirror/history |
| Gate workflow | `04_SHARED/prompts/05_ai_workflow/00_index.md` and the one current-gate prompt |
| Protected paths | `_AI_MEMORY/DO_NOT_TOUCH.md`; `09_DOCS/PROTECTED_PATHS_POLICY.md` |
| Account/model/quota operation | `_AI_MEMORY/AI_ACCOUNT_AND_MODEL_ROUTING.md`; verify current state, do not trust dated snapshots |
| DeepSeek fallback | `_deepseek_driver/README.md` before dispatch |
| Executable check/block/preregistration | `11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md` before design or audit |
| Impact/blast radius | Build a scoped graph with `03_QUANTLENS/tools/graphify_impact.py`; never graph the drive/repo blindly |
| Binary document | Convert with `03_QUANTLENS/tools/markitdown_ingest.py --apply`, then read Markdown, never raw binary |
| Cost/routing check | `codeburn status`; use `codeburn models` when breakdown matters |
| Historical fact | Grep `11_TRIAGE/INDEX.md` or `_AI_MEMORY/history/`; open only the matching record |
| AI Boardroom | `_deepseek_driver/board_runner.py`; output under `11_TRIAGE/FUSION/runs/`; full policy record in `11_TRIAGE/FUSION/FINAL_FUSION_CONSOLIDATED_RECOMMENDATION.md`; never send `.env`, API keys, broker/exchange/wallet secrets, or whole-repo dumps |

Before a repair lane, assess inherited state read-only per scope item: implemented, evidenced, both,
or neither. Comments and reports are not evidence. Check all refs before declaring work missing.
