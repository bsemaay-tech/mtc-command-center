# TASK O9FIX - close the Gemini NITs K-01..K-05 on the WP-P0-30 Shape-B exporter candidate daf6a43b -> ONE local commit + DISPOSITION

You are a BUILDER (gpt-5.5 high, Codex Plus). Not a reviewer, not the Lead. Worktree `C:/tmp/P030_INTEGRATION_20260913` (branch `feature/p030-integrated-20260913`, HEAD `daf6a43b0c4eaafd78e84df776d30d3e41d81d7b`). Read first: `C:/tmp/CLAUDE_P0_RUN_20260913/laneO9FIX_build/GEMINI_REPORT.md` (findings K-01..K-05 with file:line), `p030_archive_exporter.py`, `check_p030_archive_exporter.py`, `p030_closed_partition_backup_adapter.py` (the consumer's timestamp/canonical rules). Cite `absolute/path:line` for every claim.

## Fix exactly these (no design change; the collector stays untouched)
- **K-01:** a float overflow / non-finite number inside a source line (e.g. `1e999`) must surface as `ExportRefused("source_line_invalid")`, not a raw `ValueError` — move/extend the guard so `_reject_nonfinite_numbers` failures are wrapped; RED test with a `1e999` row and a `NaN` literal row.
- **K-02:** `dataset_content_hash` / contract refusals during export must surface as `ExportRefused("contract_refused")` (wrap `ContractRefused`); RED test with a row that the contracts module refuses.
- **K-03:** `_utc_z` must refuse sub-second timestamps (`parsed.microsecond != 0` → `ExportRefused("invalid_timestamp")`), matching the adapter's whole-second convention (cite the adapter line); RED test.
- **K-04:** add an explicit negative test for EVERY `ExportRefused` code that has none (the review counted 11 of 16 untested) — one small fixture per code; keep the existing D-13 RED/GREEN pair unchanged.
- **K-05:** correct the REPORT citation in your `DISPOSITION_O9FIX.md` (do not edit the previous lane's REPORT.md).

## Deliverables
1. Code + tests; run all four suites and paste verbatim: `python check_p030_archive_exporter.py`, `python check_market_data_collector.py`, `python check_p030_market_data_contracts.py`, `python check_p030_closed_partition_backup_adapter.py` (state the interpreter; pinned is Python 3.12 — if only 3.14 exists in your sandbox, say so; the Lead re-runs on 3.12). Prove the collector is untouched with `git -c safe.directory=* diff --stat -- market_data_collector.py` (empty).
2. `C:/tmp/CLAUDE_P0_RUN_20260913/laneO9FIX_build/DISPOSITION_O9FIX.md`: table K-01..K-05 -> FIXED with file:line + test names; refusal-code/test coverage table (16/16); `SHA256SUMS.txt` (LF).
3. ONE local commit (`p030: exporter — wrap overflow/contract refusals, whole-second timestamps, negative tests for every refusal code (Gemini K-01..K-05)`, trailer `Co-Authored-By: Codex gpt-5.5 <noreply@openai.com>`), exact two paths; if the sandbox cannot take the index lock, say so — the Lead commits. Print HEAD.

## Boundaries (binding)
- Writable: the worktree and the lane dir `C:/tmp/CLAUDE_P0_RUN_20260913/laneO9FIX_build`. Never touch `C:/LAB/Tradingview_LAB_CLEAN` itself, other worktrees, protected scopes, `market_data_collector.py`, the adapter or the contracts module.
- Git only inside the worktree (`-c safe.directory=*`; `add <paths>`, `commit`, `rev-parse`, `diff`, `status`), never while `agy.exe` runs. Codex Plus only; no delegation. Repository wins over this brief on any disagreement — record and stop on that item.
