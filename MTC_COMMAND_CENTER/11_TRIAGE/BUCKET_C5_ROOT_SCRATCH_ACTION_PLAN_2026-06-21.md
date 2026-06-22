# Bucket C5 Root Scratch Action Plan - 2026-06-21

## 1. Executive Verdict

Scope inspected: only the requested C5 items:

- `.codex/`
- `AUDIT_REPORT_CODEX.md`
- `CHATGPT_MEMORY_PROMPT.md`
- `Claude rapor.md`
- `DESIGN.md`
- `PRODUCT.md`
- `Quantlens.md`
- `MCC_COMMAND_CENTER/`

Recommended cleanup order:

1. Keep `.codex/` local-only; do not commit.
2. Move clearly durable context docs only after approval: `DESIGN.md` to triage/design context, `PRODUCT.md` to agent protocols, `Quantlens.md` to the QuantLens guide area after human review.
3. Treat possible-sensitive or duplicate items as decision-gated: `AUDIT_REPORT_CODEX.md`, `CHATGPT_MEMORY_PROMPT.md`, and `MCC_COMMAND_CENTER/`.
4. Delete `Claude rapor.md` only after approval if Baris agrees it is superseded by existing reports/handoffs.

Conservative rule for this unit: no C5 item should be staged directly from repo root. Any keeper should first be moved to a canonical MTC path, reviewed, then staged in its own focused commit.

## 2. Preflight Result

- Branch: `feature/ui-impeccable-pilot`
- Upstream state: no unpushed commits (`git rev-list --count '@{u}..HEAD'` = `0`)
- Index: empty (`git diff --cached --stat` produced no output)
- Prior classification report read: `MTC_COMMAND_CENTER/11_TRIAGE/REMAINING_BUCKET_C_CLASSIFICATION_2026-06-21.md`
- Note: `.impeccable/` appeared as a new untracked item during preflight, but it is outside this C5 scope and was not inspected or classified.

## 3. C5 Item Table

| path | type | approximate size | short content summary | sensitivity risk | duplicate risk | recommended action | proposed destination if moved | delete allowed? | commit allowed? |
|---|---|---:|---|---|---|---|---|---|---|
| `.codex/` | directory | 1 file, 0.5 KB top-level | Local `hooks.json`; configures an Impeccable post-tool hook for UI-file edits. | Medium: local automation config, no key hit in bounded scan | Low | `IGNORE_LOCAL_ONLY` | none | no | no |
| `AUDIT_REPORT_CODEX.md` | file | 6.8 KB | Root scratch Codex dashboard/UI audit report. Bounded scan hit sensitive-risk terms, so content was not printed. | High: `POSSIBLE_SENSITIVE_CONTENT_PRESENT - DO NOT COMMIT` | Medium: may duplicate triage reports or handoff notes | `NEEDS_USER_DECISION` | if sanitized and kept: `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT_REPORT_CODEX_2026-06-14.md` | no | no |
| `CHATGPT_MEMORY_PROMPT.md` | file | 3.0 KB | ChatGPT memory bootstrap prompt. Bounded scan hit sensitive-risk terms, so content was not printed. | High: `POSSIBLE_SENSITIVE_CONTENT_PRESENT - DO NOT COMMIT` | Medium: overlaps agent protocol / memory migration material | `NEEDS_USER_DECISION` | if sanitized and kept: `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CHATGPT_MEMORY_BOOTSTRAP_PROMPT.md` | no | no |
| `Claude rapor.md` | file | 2.0 KB | Short report saying a redesign plan/prototypes were created; mentions no live app implementation. | Low | High: likely superseded by canonical triage/handoff docs | `DELETE_AFTER_APPROVAL` | none unless Baris wants archive; possible `MTC_COMMAND_CENTER/11_TRIAGE/CLAUDE_REDESIGN_PLAN_NOTE.md` | yes, after approval | no |
| `DESIGN.md` | file | 12.3 KB | Strategy Intelligence Command Center design spec with colors, typography, layout/style tokens. | Low | Medium: may overlap UI reference/design prompt files | `MOVE_TO_TRIAGE` | `MTC_COMMAND_CENTER/11_TRIAGE/STRATEGY_INTELLIGENCE_DESIGN_CONTEXT.md` | no | yes, after move and review |
| `PRODUCT.md` | file | 3.5 KB | Product/user-purpose context for the internal read-only MCC dashboard. | Medium: includes user/context language, no key hit in bounded scan | Medium: overlaps memory/agent instructions | `MOVE_TO_AGENT_PROTOCOLS` | `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MCC_PRODUCT_CONTEXT.md` | no | yes, after move and review |
| `Quantlens.md` | file | 9.4 KB | Turkish QuantLens assistant/persona prompt for YouTube trading-video strategy extraction and audit. | Medium: behavior/prompt content, no key hit in bounded scan | Medium: may overlap QuantLens intake/user-guide docs | `MOVE_TO_QUANTLENS_GUIDE` | `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/QUANTLENS_ASSISTANT_PROMPT_TR.md` | no | no until Baris approves behavior ownership |
| `MCC_COMMAND_CENTER/` | directory | 1 top-level dir; contains `_AI_MEMORY/UI Reviev/RESULT_D7_fieldaudit.md` | Duplicate/misplaced command-center-like tree at repo root. Bounded scan hit sensitive-risk terms, so content was not printed. | High: `POSSIBLE_SENSITIVE_CONTENT_PRESENT - DO NOT COMMIT` | High: duplicate/misplaced tree outside canonical `MTC_COMMAND_CENTER/` | `NEEDS_USER_DECISION` | if kept after compare: move selected report to `MTC_COMMAND_CENTER/11_TRIAGE/` | no | no |

## 4. Items Safe To Move / Commit Later

These are the only C5 items that look safe to consider for a later focused move-and-commit after approval:

- `DESIGN.md` -> `MTC_COMMAND_CENTER/11_TRIAGE/STRATEGY_INTELLIGENCE_DESIGN_CONTEXT.md`
- `PRODUCT.md` -> `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MCC_PRODUCT_CONTEXT.md`

`Quantlens.md` is likely durable, but it is prompt/behavior content. It should be reviewed by Baris before moving or committing.

## 5. Items That Should Stay Ignored / Local-Only

- `.codex/`

Reason: local automation hook config, not portable repo content. If a hook policy is desired, it should be documented separately, not committed as local `.codex` state.

## 6. Items That Require Baris Decision

- `AUDIT_REPORT_CODEX.md` - possible sensitive scan hit; decide sanitize+archive or delete.
- `CHATGPT_MEMORY_PROMPT.md` - possible sensitive scan hit; decide whether this belongs in agent protocols after sanitization.
- `Quantlens.md` - useful but behavior-affecting QuantLens prompt; decide canonical ownership and filename.
- `MCC_COMMAND_CENTER/` - duplicate/misplaced tree with possible sensitive scan hit; compare selected report only if Baris wants to preserve it.
- `Claude rapor.md` - likely delete after approval, but Baris may want to archive the note.

## 7. Items That Should Not Be Staged

Do not stage these directly:

- `.codex/`
- `AUDIT_REPORT_CODEX.md`
- `CHATGPT_MEMORY_PROMPT.md`
- `Claude rapor.md`
- `DESIGN.md`
- `PRODUCT.md`
- `Quantlens.md`
- `MCC_COMMAND_CENTER/`

If approved, stage only the moved canonical destination files, not the root scratch originals.

## 8. Recommended Next Execution Prompt

```text
You are executing Bucket C5_ROOT_SCRATCH_AND_DUPLICATES cleanup after approval.

Do not touch C2 QuantLens/dashboard files, C3 UI screenshots/references, C4 HERMES/YT side projects, Pine, MTC_V2, backtests, optimizations, generated artifacts, or top_results.json.

Repo: C:\LAB\Tradingview_LAB_CLEAN
Branch must be: feature/ui-impeccable-pilot

Read:
MTC_COMMAND_CENTER/11_TRIAGE/BUCKET_C5_ROOT_SCRATCH_ACTION_PLAN_2026-06-21.md

Approved actions:
1. Move DESIGN.md to MTC_COMMAND_CENTER/11_TRIAGE/STRATEGY_INTELLIGENCE_DESIGN_CONTEXT.md
2. Move PRODUCT.md to MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MCC_PRODUCT_CONTEXT.md

Do not move, delete, stage, or commit .codex/, AUDIT_REPORT_CODEX.md, CHATGPT_MEMORY_PROMPT.md, Claude rapor.md, Quantlens.md, or MCC_COMMAND_CENTER/ unless Baris explicitly adds them to the approved action list.

After moving only approved files, run git status --short and git diff --cached --stat. Stage only the approved destination files, then stop for review unless Baris explicitly authorizes commit.
```
