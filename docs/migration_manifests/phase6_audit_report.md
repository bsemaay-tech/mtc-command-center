# Phase 6 Migration Audit Report

- Generated: 2026-05-31T18:32:30+03:00
- Auditor: Claude (Opus 4.7, independent read-only audit)
- HEAD: 39f79c3f1ed48449888ab7f3f07df9f7864d6230
- Audit scope: read-only verification of migration from `C:\LAB\tradingview-lab` (frozen) → `C:\LAB\Tradingview_LAB_CLEAN` (active).

## Verdict

**Overall: PASS_WITH_WARNINGS** (1 FAIL is informational — does not affect clean-tree integrity).

- PASS count: **10 / 12**
- FAIL count: **1 / 12** (CHECK 1 — legacy tampering, *outside* clean tree)
- WARN/PASS_WITH_WARN count: **1 / 12** (CHECK 9 — phase4 manifest hashes truncated)

Pine byte-stability (CHECK 4) — the most critical safety invariant — is **PASS** (24/24 files match). No critical-safety failure detected.

## Check Results

| # | Check                                | Verdict        | Evidence |
|---|--------------------------------------|----------------|----------|
| 1 | Legacy frozen state                  | **FAIL**       | One post-archive modification in legacy (`MTC_COMMAND_CENTER/01_PROMPTS/CLAUDE_CONTINUATION_2026-05-31.md`). Spec-expected 3 files (`MEGA_walk_forward_report.md`, `MEGA_walk_forward_results.json`, `Claude.md`) were committed in `3b484f87` and are no longer in diff. |
| 2 | Target git state                     | PASS           | 6 commits in exact spec order; working tree clean (empty `--porcelain`). |
| 3 | Excluded items absent in clean       | PASS           | All 7 excluded paths absent. `.pytest_cache` absent. `__pycache__` present only as runtime artifact and gitignored (`.gitignore:19`). |
| 4 | Pine byte-stability                  | **PASS**       | 24 / 24 Pine files SHA256 match manifest. 0 mismatches. Saved: `phase6_pine_recheck.csv`. |
| 5 | MTC_COMMAND_CENTER hash stability    | PASS           | 406 / 406 files SHA256 match. 0 unexpected mismatches. Expected tracker mismatch (`MTC_V2_PARITY_CASES.csv`) was already absorbed into manifest. |
| 6 | Hardcoded path absence (18 scripts)  | PASS           | 0 hits for `01_MASTER TEMPLATE_V2`; 0 hits for `C:\LAB\tradingview-lab` across all 18 active scripts. |
| 7 | REPO_ROOT semantics                  | PASS           | 13 / 13 scripts that define `REPO_ROOT` resolve it to `C:\LAB\Tradingview_LAB_CLEAN` exactly. 3 scripts (`pine_trades.py`, `run_pinets.mjs`, `validate_syntax.mjs`) intentionally use `__dirname`/script-local anchors (no `REPO_ROOT` needed). |
| 8 | Smoke reproducibility                | PASS (1 WARN)  | `AUTO_002` smoke exit 0; FINAL VERDICT: PASS; Strict trade PASS: YES; Pine=Python=7 trades; all 5 metrics OK. Log: `phase6_smoke_AUTO_002.log`. WARN: tracker xlsx fallback workbook missing (CSV path used instead). |
| 9 | Manifest cross-reference             | PASS_WITH_WARN | `copy_manifest.csv` 100/100 sampled targets exist. `phase3_archive_summary.json` fields validated. All 6 `phase4_late_root_scripts_restore.csv` files exist. WARN: phase4 manifest stores truncated 16–18 char hashes (not full SHA256) — strict hash cross-verify not possible. |
| 10 | .gitignore correctness              | PASS           | All 3 `git check-ignore -v` probes report hits. `git ls-files` for `(mtc_signals.json|pine_trades.json|pine_trades.csv)` returns empty. |
| 11 | Deferred items documentation        | PASS           | `hardcoded_path_rewrite_TODO.md` line 17 carries "Deferred — QuantLens references (116 hits across 57 files)" + "Fix on demand" policy (line 22). `phase2_quantlens_06_quantlens_lab_hits.csv` has 116 data rows (117 lines incl. header). |
| 12 | Author / agent attribution          | PASS           | All 6 commits authored by `bsemaay-tech <bsemaay@gmail.com>`. No secrets/keys/tokens detected in commit messages. |

## Failures

### CHECK 1 — Legacy frozen state (FAIL, informational)

**Symptom:** `git -C C:\LAB\tradingview-lab status --porcelain` returns:

```
 M MTC_COMMAND_CENTER/01_PROMPTS/CLAUDE_CONTINUATION_2026-05-31.md
?? ARCHIVE_NOTICE.md
```

**Expected per spec:**
- `M 01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/05_BACKTEST_RESULTS/MEGA_walk_forward_report.md`
- `M 01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/05_BACKTEST_RESULTS/MEGA_walk_forward_results.json`
- `M 01_MASTER TEMPLATE_V2/Claude.md`

**Resolution of discrepancy:**
- The 3 spec-expected files were committed in `3b484f87 docs(handoff,quantlens): freeze pre-archive state`. They are no longer in diff. That divergence from spec is benign — the freeze actually completed.
- `ARCHIVE_NOTICE.md` is the new untracked file Phase 3 wrote — expected.
- `CLAUDE_CONTINUATION_2026-05-31.md` shows a **one-line content change** post-archive: `"You are Claude continuing..."` → `"You are Codex continuing..."` (1 insertion / 1 deletion).

**Implication:**
- Legacy `ReadOnly` directory attribute is set (confirmed: `ReadOnly, Directory`), but the Windows `ReadOnly` flag on a directory does *not* prevent file-level writes inside it. A handoff agent (likely Codex per the diff text) edited the file in place.
- This does **not** affect the clean tree, which is what the migration actually delivers. Pine bytes are intact; clean SHA256 manifests match; smoke passes.
- Action item (outside audit scope): re-freeze legacy via NTFS DACL deny-write or by force-checkout (not done by this auditor — read-only constraint).

## Warnings

### CHECK 8 — Smoke run reported missing tracker workbook

```
Tracker workbook missing: ...\MTC_COMMAND_CENTER\01_MTC_PROJECT\05_PARITY\MTC_V2_PARITY_CASE_TRACKER.xlsx
```

The CSV tracker (`MTC_V2_PARITY_CASES.csv`) was used and updated successfully; the optional xlsx fallback workbook is not present in the clean tree. Smoke still produced FINAL VERDICT PASS, so this is non-blocking. Either the xlsx should be intentionally added back to the tree or the warning should be removed from the runner.

### CHECK 9 — phase4 restore manifest hash format

`phase4_late_root_scripts_restore.csv` declares column `src_sha256` / `dst_sha256` but stores values of length 16–18 hex chars (e.g. `89C5C7D398B01CC85A`) — these are **not** full SHA256 digests (which are 64 hex chars). The 6 listed files all exist; their byte counts match (`bytes` column). Full SHA cross-check from this manifest is therefore not possible. Recommend either re-running the phase4 hash collector to emit full SHA256, or renaming the column to `sha256_prefix` to set correct expectations.

## Notes

- Pine recheck duration: 0.00 s (24 files).
- MTC manifest recheck duration: 0.09 s (406 files).
- Smoke run duration: ~8 s (5.3 s Binance fetch + ~3 s PineTS + Python parity).
- Total audit wall-clock duration: ~5 minutes (most spent on script-tree walks and parallel grep).

### Artifacts written by this audit
- `docs\migration_manifests\phase6_audit_report.md` (this file)
- `docs\migration_manifests\phase6_pine_recheck.csv` (24-row Pine SHA cross-check)
- `docs\migration_manifests\phase6_smoke_AUTO_002.log` (full AUTO_002 smoke stdout/stderr)

### No mutating actions taken
- Both trees treated as read-only.
- No git operations beyond `status`, `log`, `show`, `check-ignore`, `ls-files`, `diff` (all read-only).
- No `--no-verify`, no hook bypass, no push.
- Smoke run performed a Binance read-only fetch and wrote local runtime artifacts under `MTC_COMMAND_CENTER\02_MTC_BACKTEST\data\` and `\reports\` — both gitignored, no commits made.
