# Lane F Report — WP-P0-07

## Status

**IMPLEMENTER SELF-QA COMPLETE — ready for Lead-owned T2 acceptance.**

The inventory closes the O-14 investigation at its evidence boundary. No strict survivor was found, but F-22 cannot defensibly be upgraded to an all-time claim from this checkout. It remains bounded, with the missing-result and identity gaps named in `F22_VERDICT.md`.

No backtest or optimization was run. No result was promoted. All writes are new files inside this lane package.

## Delivered evidence

- `RUN_RESULT_INVENTORY.md`: 67 directly parseable completed result JSONs, derived records, absent recorded run families, and tracked pre-strict packages.
- `F22_VERDICT.md`: acceptance-gate answer — keep F-22 bounded.
- `SEARCH_LOG.md`: discovery commands, complete-corpus parsing method, and the RED/GREEN enumeration self-test.
- `LANE_REPORT.md`: this closeout record.

## Self-QA

| Check | Result |
|---|---|
| Direct-file/table comparator | PASS — 67 actual files, 67 numbered rows, 67 unique paths, zero extra paths, zero mismatches. |
| Source rows checked | PASS — 220,761 result rows; every `robust_final` value in the 67-file final corpus is explicitly false. |
| Dates, trial totals, row coverage, engine versions | PASS — recomputed from each cited JSON and matched to the inventory. |
| Markdown table widths | PASS — 110 table lines, zero inconsistent-width lines within a table. |
| Unrecoverable-field wording | PASS — every unrecoverable field uses the required uppercase placeholder, em dash, and searched/absent explanation. |
| Enumeration falsification | PASS — default ignored-file discovery missed the unannounced nested artefact (RED); `--hidden --no-ignore` found it exactly once (GREEN). |
| Temporary self-test cleanup | PASS — planted file deleted; temporary directory absent. |
| Scope check | PASS — only the four required new files exist under the authorized package directory; no tracked file outside it changed. |
| Runtime boundary | PASS — no backtest, optimization, engine import, network, Docker/WSL, or external AI CLI was used. |
| Patch hygiene | PASS — `git diff --cached --check` reported no error before the evidence commit. |

Two earlier ad hoc checker attempts were discarded before acceptance: one assumed one fixed pipe width across different Markdown tables, and one inline Unicode literal was transformed by the shell. The corrected table-aware and code-point-safe checks produced the passing results above; neither failed attempt changed repository state.

## Git record

Primary evidence commit:

`4ca16cbfaa3836e688869d18412ac036da309d77`

Commit subject:

`docs(wp-p0-07): run/result inventory closing O-14 (T2, lane F 2026-08-25)`

Exact files staged for that commit:

- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_07_RUN_INVENTORY_2026-08-25/F22_VERDICT.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_07_RUN_INVENTORY_2026-08-25/RUN_RESULT_INVENTORY.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_07_RUN_INVENTORY_2026-08-25/SEARCH_LOG.md`

This report necessarily follows the immutable evidence commit so it can record that SHA. Its closeout commit SHA is reported in the terminal/final lane output; a commit cannot contain its own SHA.

## Open issues / acceptance boundary

- Primary bytes for part of the historical git-ignored result estate are absent from this worktree.
- Four of six registered research-run directories are absent; the canonical backtest registry is empty.
- Pre-strict/custom May packages do not expose the current `robust_final` field or, in several cases, an authoritative total configuration count.
- `overnight_full_2026-07-02` has a recorded run-id/path identity conflict; `overnight_resilient_2026-07-02/variants` is unregistered.
- These gaps prevent an evidence-backed “zero strict survivors ever” statement. They do not refute the directly verified zero across the present 67-file corpus.
- Lead-owned single-reviewer T2 acceptance remains outside implementer self-QA.

No memory/handoff file was updated because the lane's hard write boundary permits only new files in this package.
