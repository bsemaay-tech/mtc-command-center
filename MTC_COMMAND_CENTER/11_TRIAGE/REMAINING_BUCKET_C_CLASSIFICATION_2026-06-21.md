# Remaining Bucket C Classification - 2026-06-21

## 1. Branch / Preflight Result

- Branch: `feature/ui-impeccable-pilot`
- Preflight result: PASS
- Working tree state before this report: untracked Bucket C candidates only
- C1 status: closed; `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md` was not dirty
- Index state before this report: empty (`git diff --cached --stat` produced no output)
- Unpushed commits: none (`git rev-list --count '@{u}..HEAD'` = `0`)
- Notes: no staging, commit, push, delete, backtest, optimization, artifact generation, Pine, or MTC_V2 action was performed during this classification pass.

## 2. Current Pushed HEAD

- `b565f96f376803418a9daca5d3ff0fb05c5047de`
- Short log head: `b565f96 Clarify archived overnight next steps`

## 3. Index State

- Index is empty.
- This report is intentionally left untracked and unstaged.

## 4. Remaining Dirty Count

- Pre-report dirty count: 33 untracked items
- Classification counts, excluding this report:
  - C2: 12
  - C3: 9
  - C4: 4
  - C5: 8

## 5. Remaining Item Classification

| path | status | rough size | bucket | recommended action | risk | reason |
|---|---:|---:|---|---|---|---|
| `.codex/` | untracked dir | 1 top-level file, 0.5 KB | C5 | ignore or delete after user approval | high | Local Codex/session metadata; should not be committed without explicit review. |
| `AUDIT_REPORT_CODEX.md` | untracked file | 6.8 KB | C5 | move into `MTC_COMMAND_CENTER/11_TRIAGE/` if still useful, otherwise delete after approval | medium | Root scratch audit about dashboard UI deployment; likely belongs in triage history, not repo root. |
| `CHATGPT_MEMORY_PROMPT.md` | untracked file | 3.0 KB | C5 | move into `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/` only if approved, otherwise ignore/delete | high | Memory bootstrap text may contain durable personal/project context; root scratch location is wrong. |
| `Claude rapor.md` | untracked file | 2.0 KB | C5 | move into `MTC_COMMAND_CENTER/11_TRIAGE/` only if useful, otherwise delete after approval | medium | Scratch implementation report/prototype note; not canonical in root. |
| `DESIGN.md` | untracked file | 12.3 KB | C5 | user decision needed; possible move into `MTC_COMMAND_CENTER/11_TRIAGE/` or design reference area | medium | Design spec for Strategy Intelligence Command Center; could be useful but needs ownership decision. |
| `HERMES/` | untracked dir | 1 top-level dir | C4 | separate repo candidate or user decision needed | high | Auxiliary Hermes skills package; outside current MTC cleanup scope and should not be mixed into MCC commit. |
| `HERMES_MTC_MEMORY_IMPORT/` | untracked dir | 3 dirs, 1 file, 0.7 KB top files | C4 | separate handoff/import bundle; user decision needed | high | Memory import package with proposed Hermes memory/context/prompt material; likely sensitive and side-project scoped. |
| `MCC_COMMAND_CENTER/` | untracked dir | 1 top-level dir | C5 | user decision needed; likely duplicate/misplaced root folder | high | Looks like a duplicate command-center tree at repo root; must not be staged until compared and approved. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/13_GATE_SCORECARD_V2_TR.md` | untracked file | 17.1 KB | C2 | focused C2 audit candidate | medium | QuantLens guide doc, Turkish scoring/gate material; likely repo docs but needs content/placement review. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/14_OPTIMIZASYON_SKORLAMA_TR.md` | untracked file | 13.3 KB | C2 | focused C2 audit candidate | medium | QuantLens optimization scoring guide; likely useful but should be reviewed before commit. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_profile_result_artifact.py` | untracked file | 12.5 KB | C2 | focused C2 audit candidate | high | Tool can generate/read artifact contracts; must be audited for read-only behavior and no fake result generation. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_run_plan.py` | untracked file | 17.0 KB | C2 | focused C2 audit candidate | high | QuantLens run-plan builder; likely useful but touches planning/execution boundary. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/night_1m_2026-06-07.sh` | untracked file | 7.4 KB | C2 | focused C2 audit candidate, but do not stage without explicit approval | high | Overnight launcher script; execution-related and date-specific. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/overnight_loop_2026-06-08.sh` | untracked file | 7.0 KB | C2 | focused C2 audit candidate, but do not stage without explicit approval | high | Overnight loop script; execution-related and date-specific. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_1m_2026-06-07_keepawake.ps1` | untracked file | 1.6 KB | C2 | focused C2 audit candidate, but do not stage without explicit approval | high | Keep-awake runner for overnight work; operational script with local machine impact. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_3M_2026-06-08_keepawake.ps1` | untracked file | 1.8 KB | C2 | focused C2 audit candidate, but do not stage without explicit approval | high | Keep-awake runner for overnight work; operational script with local machine impact. |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_profile_result_artifact.py` | untracked file | 7.9 KB | C2 | focused C2 audit candidate | medium | Matching test for profile-result artifact tool; should be paired with tool audit. |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py` | untracked file | 5.6 KB | C2 | focused C2 audit candidate | medium | Matching test for run-plan builder; should be paired with tool audit. |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py` | untracked file | 5.9 KB | C2 | focused C2 audit candidate | medium | Dashboard invariant test; likely useful, but include only with focused dashboard/test audit. |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/run_dashboard_server.ps1` | untracked file | 7.2 KB | C2 | focused C2 audit candidate, but do not stage without explicit approval | high | Launcher script can affect local server/process behavior; needs operational review. |
| `MTC_COMMAND_CENTER/11_TRIAGE/UI_AUDITS/` | untracked dir | 6 files, 147.9 KB top files | C3 | keep in handoff bundle or curate selected summary into triage | low | Multi-model UI audit reports; useful evidence but may not belong in all-at-once commit. |
| `MTC_COMMAND_CENTER/11_TRIAGE/ui_references/google_strategy_intelligence_v2_final/` | untracked dir | 1 dir, 30 files, 4.5 MB top files | C3 | user decision needed; curate only selected assets into `ui_snapshots/latest/` | medium | Large UI reference bundle; needs pruning to avoid committing raw prompt/reference bloat. |
| `MTC_COMMAND_CENTER/11_TRIAGE/ui_references/strategy_intelligence_lovable/` | untracked dir | 1 dir, 18 files, 3.9 MB top files | C3 | user decision needed; keep only if needed as source reference | medium | Lovable reference bundle; likely useful for design provenance but should be curated. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/ARCHİVE 1/` | untracked dir | 21 files, 1.1 MB top files | C3 | ignored/local archive or move curated subset to `11_TRIAGE/ui_snapshots/latest/` | medium | Screenshot/archive folder under misspelled memory path; should not remain there if committed. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/Ekran görüntüsü 2026-06-07 211721.png` | untracked file | 229.5 KB | C3 | curate only if needed, otherwise local archive/delete after approval | low | UI screenshot; evidence asset but not independently useful without naming/context. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/Ekran görüntüsü 2026-06-07 211746.png` | untracked file | 199.3 KB | C3 | curate only if needed, otherwise local archive/delete after approval | low | UI screenshot; evidence asset but not independently useful without naming/context. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/Ekran görüntüsü 2026-06-07 211806.png` | untracked file | 156.8 KB | C3 | curate only if needed, otherwise local archive/delete after approval | low | UI screenshot; evidence asset but not independently useful without naming/context. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/Ekran görüntüsü 2026-06-07 211857.png` | untracked file | 212.1 KB | C3 | curate only if needed, otherwise local archive/delete after approval | low | UI screenshot; evidence asset but not independently useful without naming/context. |
| `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/Ekran görüntüsü 2026-06-07 211911.png` | untracked file | 187.5 KB | C3 | curate only if needed, otherwise local archive/delete after approval | low | UI screenshot; evidence asset but not independently useful without naming/context. |
| `PRODUCT.md` | untracked file | 3.5 KB | C5 | user decision needed; possible move into protocol/design docs, otherwise delete after approval | medium | Generic product prompt/spec in root; location and ownership unclear. |
| `Quantlens.md` | untracked file | 9.4 KB | C5 | user decision needed; possible move into `00_AGENT_PROTOCOLS` or `03_QUANTLENS/_user_guide/` after review | high | Turkish QuantLens assistant prompt/spec may affect strategy intake behavior; should not be casual root commit. |
| `YT_TRANSCRIPT_COLLECTOR/` | untracked dir | 4 dirs, 9 files, 11.6 KB top files | C4 | separate repo candidate; do not commit under MTC without approval | high | Auxiliary transcript collector includes `.venv`, reports, transcripts, tests, and URL run files. |
| `_HERMES_MEMORY_IMPORT/` | untracked dir | 2 dirs, 1 file, 0.7 KB top files | C4 | side handoff/import bundle; user decision needed | high | Memory import material outside main tree; likely sensitive context and not a normal repo artifact. |

## 6. Recommended Next Cleanup Unit

Recommended next cleanup unit: `C5_ROOT_SCRATCH_AND_DUPLICATES`

Reason: it is the smallest safe unit and mostly classification/move-or-delete decisions. It can reduce root noise without touching execution code, dashboard source, QuantLens tools, screenshots, HERMES, YT transcript tooling, Pine, or MTC_V2. It also isolates high-risk local metadata and duplicate root folders before any C2 implementation audit.

## 7. Files That Must Not Be Staged Without Explicit Approval

- `.codex/`
- `HERMES/`
- `HERMES_MTC_MEMORY_IMPORT/`
- `_HERMES_MEMORY_IMPORT/`
- `YT_TRANSCRIPT_COLLECTOR/`
- `MCC_COMMAND_CENTER/`
- `CHATGPT_MEMORY_PROMPT.md`
- `Quantlens.md`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/night_1m_2026-06-07.sh`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/overnight_loop_2026-06-08.sh`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_1m_2026-06-07_keepawake.ps1`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_3M_2026-06-08_keepawake.ps1`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/run_dashboard_server.ps1`
- Any file under `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/`
- Any full UI reference bundle under `MTC_COMMAND_CENTER/11_TRIAGE/ui_references/` until curated.

## 8. Suggested Exact Next Prompt

```text
You are doing Bucket C cleanup unit C5_ROOT_SCRATCH_AND_DUPLICATES only.

Do not edit, stage, commit, push, or delete anything until after a read-only decision table.
Do not touch C2 QuantLens/dashboard files, C3 UI snapshots/references, C4 HERMES/YT side projects, Pine, MTC_V2, backtests, optimizations, or generated artifacts.

Repo: C:\LAB\Tradingview_LAB_CLEAN
Branch must be: feature/ui-impeccable-pilot

Read:
MTC_COMMAND_CENTER/11_TRIAGE/REMAINING_BUCKET_C_CLASSIFICATION_2026-06-21.md

Scope only these C5 items:
.codex/
AUDIT_REPORT_CODEX.md
CHATGPT_MEMORY_PROMPT.md
Claude rapor.md
DESIGN.md
PRODUCT.md
Quantlens.md
MCC_COMMAND_CENTER/

For each item, inspect only enough to decide: move into MTC_COMMAND_CENTER/11_TRIAGE/, move into MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/, ignore, delete after user approval, or user decision needed.

Output a read-only action plan first. Do not perform moves/deletes/staging until Baris approves.
```
