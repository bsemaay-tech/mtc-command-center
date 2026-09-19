# TASK P31B-CONT - CONTINUE the WP-P0-31 engineering batch that the Codex Plus usage cap cut at 10:55Z (owner GO `OD-20260914-P031-BATCH-GO-1`; answers `OD-20260914-P031-LIFECYCLE-1`)

You are a BUILDER (gpt-5.5 high, Codex Plus). Not a reviewer, not the Lead. Worktree: `C:/tmp/P031_M1_20260913` (branch `feature/p031-m1-20260913-refresh`, reviewed HEAD `c76043b92c70c9f79a6d06630c0896ebe73e68a1`).

## What already happened (read before touching anything)
1. The ORIGINAL brief is in the worktree as `TASK_P31B.md` (untracked). Read it in full first; every rule, boundary and deliverable in it still binds. This file only tells you how to resume.
2. A previous builder ran 96 commands against that brief and was cut by the provider's usage limit. **The worktree already contains UNCOMMITTED partial edits** — at the time of the cut: `MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py` (+247/-23) and `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py` (+185/-25). Its last messages said: REJECTED purpose/hash/failing_checks refusals and tests done; capacity-withholding purpose from the configured version done; `catalog_backed: false` added to manual history injection; OD-10 same-epoch reuse assertions done. Which of OD-2 (DEMOTED), OD-7 (deployment refresh), OD-9 (RETIRED -> RE_ENTRY sixth trigger), OD-11 (catalog), OD-1 (doc), OD-4/OD-8 (recording) are complete is UNKNOWN.
3. **Never discard, revert, stash or checkout over those edits.** Inventory them first:
   - `tasklist | findstr /i agy.exe` must show NOTHING before every git command (a review helper watches the shared repository store); if it shows agy.exe, wait 60 s and re-check.
   - `git -c safe.directory=* status --porcelain` and `git -c safe.directory=* diff --stat`, then `git -c safe.directory=* diff` on each changed file. Write the inventory (per owner answer: DONE / PARTIAL / NOT STARTED, with file:line) into `C:/tmp/CLAUDE_P0_RUN_20260913/laneP31B_cont/INVENTORY.md` BEFORE editing.
4. Run the ledger test file once as found (`pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py -q -p no:cacheprovider` with the package's pinned interpreter per `P031_M1_SCOPE_AND_STATUS.md`) and record the result in INVENTORY.md — it may be RED mid-edit; that is information, not a failure of yours.

## Then finish the batch
- Complete every item of `TASK_P31B.md` that the inventory shows PARTIAL or NOT STARTED, in the order OD-2, OD-7, OD-9, OD-11, OD-1, OD-4/OD-8, then re-verify OD-5/OD-6/OD-10. Each new rule keeps the RED (refusal) + GREEN test pair.
- **Write progress as you go**: after each owner item append a dated line to `C:/tmp/CLAUDE_P0_RUN_20260913/laneP31B_cont/PROGRESS.md` (item, files, test count). The provider cap can cut you again at any moment; the next builder must be able to resume from PROGRESS.md the way you resumed from this file.
- Run EVERY check command the package publishes (`P031_M1_SCOPE_AND_STATUS.md`: pinned python compile, reader, guard, diff-check, Ruff, fixture demo, D026, the full ledger test file) and paste each command with its verbatim output into the REPORT.
- ONE local commit on the branch exactly as `TASK_P31B.md` deliverable 2 specifies (`git -c safe.directory=* add <exact paths>` — list them; `git -c safe.directory=* commit` with the specified message and the `Co-Authored-By: Codex gpt-5.5 <noreply@openai.com>` trailer; no push, PR, merge, branch switch, stash). Do NOT add `TASK_P31B.md`, `TASK_P31B_CONT.md` or any lane file to the commit. Print the new HEAD.
- `C:/tmp/CLAUDE_P0_RUN_20260913/laneP31B_cont/REPORT.md` per `TASK_P31B.md` deliverable 3, plus a section "Resumed from a cut lane" that lists what the inventory found and what this lane changed. Also `SHA256SUMS.txt` (LF) of the committed candidate files.

## Boundaries (binding; same as the original brief)
- Writable: the worktree `C:/tmp/P031_M1_20260913` and the lane dir `C:/tmp/CLAUDE_P0_RUN_20260913/laneP31B_cont`. Never touch `C:/LAB/Tradingview_LAB_CLEAN` itself, any other worktree, or protected scopes (`02_MTC_BACKTEST`, `07_ADAPTERS`, `01_PINE`, `MTC_V2`).
- Git only inside the worktree, only `add <paths>` / `commit` / `rev-parse` / `diff` / `status` / `log`, always with `-c safe.directory=*`, never while `agy.exe` runs.
- No new shared lifecycle semantics beyond the answered options; no legacy import, cutover, deployment, host, credential, network, install, trading.
- Cite `absolute/path:line` for every claim; read the line before citing it. If the repository disagrees with this brief, the repository wins — record the discrepancy in the REPORT and stop on that item.
