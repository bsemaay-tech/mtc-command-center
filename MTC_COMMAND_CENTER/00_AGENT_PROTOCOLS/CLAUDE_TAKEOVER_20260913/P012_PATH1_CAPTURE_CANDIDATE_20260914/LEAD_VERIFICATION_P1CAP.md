# LEAD_VERIFICATION_P1CAP — P012 Path 1 own-account capture tool candidate — 2026-09-14 21:05Z (records written 2026-09-15 05:10Z)

**Result: candidate VERIFIED by the Lead and committed as `e77af1c8` on `feature/p012-path1-capture-20260914` (base `fcac0ac6` = master after PR #191), backup-pushed to origin. NONACCEPTING: no review yet, no network call made, no real capture produced.** Lane P1CAP: Codex Plus gpt-5.5 high, 20:11Z-20:34Z (capped once at 20:34Z, resumed), exit 0.

## Deliverables (blob OIDs pinned per the owner's 2026-08-29 ruling; sha256 = lane `SHA256SUMS.txt`, verified byte-for-byte)
| Path | blob OID | sha256 |
|---|---|---|
| `IBKR_PAPER_BRIDGE/tools/capture_own_account_evidence.py` (548 lines) | `58ddd75f…` | `a1ef5ee1c1241577e0c3c4edf52a07acb71f67dc36af050d9629fcd8c2ad475d` |
| `IBKR_PAPER_BRIDGE/tools/path1_sign_ownership.html` (58 lines) | `6e786231…` | `b43dbe39aaa9536fbc8f3e05d29ddc851ad3d2e3e271e1bee38b53fddc54e01f` |
| `IBKR_PAPER_BRIDGE/tests/test_capture_own_account_evidence.py` (224 lines, 10 tests) | `fad1e297…` | `d1d2ad20b46d0ec20fac1b15e63f9837d961609d88d234d1a55a6b75f37953b3` |
Lane files `REPORT.md` (`1617d247…`), `SHA256SUMS.txt`, `TASK_P1CAP.md` stay untracked in the worktree and are copied to CT13 `P012_PATH1_CAPTURE_CANDIDATE_20260914/`.

## What the Lead ran (Python 3.12 `C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe`, `-p no:cacheprovider`)
| Check | Observed |
|---|---|
| focused tests | `10 passed` (twice: original worktree, then the re-created clean worktree) |
| full Bridge suite, `--basetemp` under `C:/tmp` | `33 failed, 1605 passed, 1 skipped` — all 33 in `tests/test_mtc_funding_export.py`, refusal `export_mtc_funding: CANDIDATE_STAGING_UNSAFE: the staging directory must not be inside another Git checkout or worktree` |
| **same file on an untouched detached worktree at `fcac0ac6`** (`git worktree add --detach C:/tmp/P1CAP_BASE_fcac0ac6_20260914 fcac0ac6`) | `33 failed, 128 passed, 1 skipped` — **identical FAILED id set** (`diff` empty; lists in `base_fcac0ac6_funding_export_failures.txt` / `cand_P1CAP_funding_export_failures.txt`) |
| root cause | a stray, repository-less directory **`C:/tmp/.git`** (only `info/`, created 2026-09-09 11:34) — `export_mtc_funding.py:_git_ancestor` treats any `.git` directory ancestor as a Git checkout, so every staging path under `C:/tmp` refuses. Environmental; not caused by the candidate. (The P012_PATHD worktree at `dac9dba6` shows the same 33 — but it is not an ancestor of `fcac0ac6`, so it was not used as the base.) |
| same file, `--basetemp` under the user temp dir (no `.git` ancestor) | candidate `161 passed, 1 skipped`; base `161 passed, 1 skipped` |
| **full suite, clean basetemp** | `tests/`: `1608 passed, 1 skipped, 1 warning in 178 s`; `tools_v2/observability/tests/test_export_audit_pack.py` + `tools_v2/analysis_package/tests/test_generator.py`: `30 passed` → 1638 passed total, 0 failed (`LEAD_FULL_SUITE_PY312_CLEAN_BASETEMP.txt`) |
| imports / write-capability | only `hyperliquid.info.Info` + `hyperliquid.utils.constants` + `eth_account`; no `Exchange`, no `requests`/`urllib`/`subprocess` import in the tool; `HL_API_WALLET_KEY` refusal at `:414` |
| Ruff 0.16.4 | `F401` tests:5 unused `os`; `RUF100` tool:157 unused `noqa: BLE001`; `F841` tool:160 unused `raw`; `ruff format --check`: both files would be reformatted (no CI lint gate exists for the Bridge; carried to the correction brief, bytes left as built so the review sees the lane's artefact) |
| citations in the lane REPORT (R6 grep, 22 checked) | 20 exact; 2 off: tool `:23` (Info import is `:24`), tool `:125` (`info_base_url` is `:121-122`; `:125` is `sdk_version`) |
| repo guard | first run **BLOCKED** (`PINE_ALERT_GUARD UNEVALUATED path=.pytest_cache … Erişim engellendi`): the Codex sandbox left ACL-locked `.pytest_cache/` and `IBKR_PAPER_BRIDGE/pytest-of-BarışSemaay/` (takeown/icacls/rm all denied without elevation). Fix: moved the directory to `C:/tmp/P1CAP_20260914_LOCKED_SANDBOX_DIRS` (owner may delete it elevated), `git worktree prune`, re-created `C:/tmp/P1CAP_20260914` on the same branch, copied the six files back (digests re-verified) → guard **PASS** (`PINE_ALERT_GUARD PASS files=21 matches=0`) |
| staged set | exactly the three paths (`git diff --cached --name-only`) |

## Lead findings for the reviewers / correction brief (P1FIX, not yet written)
- L-1 Ruff findings above + format drift.
- L-2 no RED test for a WRONG ownership signature (only the GREEN recovery test at tests:204); no multi-page success test (only the stall refusal at tests:129).
- L-3 `funding_identity` = `hash:time` only (`:197-203`); two coins funded in the same block would collide and refuse `funding identity conflict` — latent, single-coin owner account not affected; identity should include `coin`.
- L-4 ownership signature is verified AFTER the five network passes (`run_capture` end); a bad signature leaves page files with no manifest → verify before the first call.
- L-5 `write_once` uses `exists()` then `write_bytes` (TOCTOU; `open(path, "xb")` is the exclusive form); `call_info` drops the raw error body on the failure path (`raw` unused).
- L-6 manifest does not state that `raw` bytes are `response.content` (the test double path re-serializes parsed JSON via `consume_capture`) — add `raw_bytes_source`.
None of these blocks the detection review; they are what the review should confirm or extend.

## Next (in order)
1. Gemini 3.8 detection review of `e77af1c8` (stage packet ≥ 75 s before the chain; no git during the call).
2. Exact Sol review (Codex Plus bucket); exact Opus after the 2026-09-16 20:00Z reset.
3. P1FIX correction lane (Codex) with L-1..L-6 + reviewer items.
4. Only after the tool is accepted: the real read-only capture of the owner's mainnet address (window 2026-09-14T15:00Z → 2026-09-14T19:00Z covers T1/T2/T3, the duplicate, both funding rows and the close) with `--run-id` fixed FIRST and the owner signing the printed message in `path1_sign_ownership.html` (his wallet, his click; the Lead never handles keys).

Recorded by Claude Opus 5 Lead (b9df29).
