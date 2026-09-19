# LEAD_VERIFICATION_P1FIX — P012 Path 1 capture tool correction `af921d75226932b11c5f0279b2cbf0b0de5be9e0` — 2026-09-15 06:42Z

**Result: correction candidate built BY THE LEAD (owner `OD-20260915-P012-P1FIX-LEAD-1`, "A"), verified on Python 3.12, committed as `af921d75` on `feature/p012-path1-capture-20260914` (parent `e77af1c8`), backup-pushed. NONACCEPTING: Gemini delta review launched 06:44Z; exact Opus after the 2026-09-16 20:00Z reset; exact Sol after the Codex reset (Sep 19). The Lead does not accept its own code.**

## What changed (2 files; `DISPOSITION_P1FIX.md` has the finding-by-finding table)
| Path | sha256 | Change |
|---|---|---|
| `IBKR_PAPER_BRIDGE/tools/capture_own_account_evidence.py` | `00b3b8f6…` | F-1 run-id gate + signature verified before `make_info`/`mkdir`; F-2 half-open window filter + range refusals + manifest `window.{start_ms,end_ms,semantics}`; F-4 coin in funding identity; F-5 exclusive create; F-6 error bytes kept (`recorded_call`); F-7 `raw_bytes_source`; F-11 content re-query (`requery_check`); docstring; `ruff format` |
| `IBKR_PAPER_BRIDGE/tests/test_capture_own_account_evidence.py` | `5d141fb1…` | 10 → 21 tests; fixtures moved inside the window; F-8 `CapturingInfo.post` unit test with a fake session; F-9 multi-page + wrong-signature + run-id arms; window arms; coin, exclusive write, error-bytes arms; `ruff format` |

## Evidence (interpreter `C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe` = 3.12.12; `-p no:cacheprovider`; `--basetemp` under the user temp dir)
| Check | Observed |
|---|---|
| focused module | `21 passed in 0.94s` (`LEAD_FOCUSED_PY312.txt`) |
| **RED on the pre-fix tool** `e77af1c8` (scratch tree: old tool `a1ef5ee1…` + new tests + minimal conftest) | **`12 failed, 9 passed`** — failures = manifest window/provenance fields, half-open end exclusion, before-start refusal, after-end refusal, re-query detail, re-query content, funding coin, exclusive write, error bytes kept, `CapturingInfo` error capture, run-id gate, wrong signature before network (`LEAD_RED_ARMS_PREFIX_TOOL.txt`) |
| full Bridge suite, clean basetemp | `tests/`: `1619 passed, 1 skipped, 1 warning in 214.46s`; tools_v2 modules: `30 passed` → **1649 passed, 0 failed** (`LEAD_FULL_SUITE_PY312.txt`); the stray `C:/tmp/.git` no longer exists (deleted 05:30Z), so no phantom `export_mtc_funding` failures |
| Ruff 0.16.4 `--select E9,F821,F811,F401,F841,RUF100` | `All checks passed!`; `ruff format --check`: both files formatted |
| `py_compile` | OK |
| repo guard (worktree) | `RESULT: PASS` (`LEAD_GUARD.txt`) |
| staged set | exactly the two paths |
| read-only invariants | `test_tool_imports_no_write_capable_exchange_client` still passes; imports unchanged (`Info`, `constants`, `eth_account`); key refusal first |

## Prepared for the owner's real capture (after the Gemini delta review; NOT run)
- run_id fixed FIRST: **`p012-path1-20260914T1500Z-1900Z-r1`**; ownership message printed with `--print-ownership-message` → `OWNERSHIP_MESSAGE_r1.txt`:
  `P012 Path 1 own-account evidence capture` / `address: 0x1e265f5e39957e08ed02a120cefa33a9bd46ac49` / `run_id: p012-path1-20260914T1500Z-1900Z-r1`.
- The owner signs in his wallet via `file:///C:/tmp/P1CAP_20260914/IBKR_PAPER_BRIDGE/tools/path1_sign_ownership.html?address=0x1E265F5E39957E08ed02A120ceFA33A9bd46AC49&run_id=p012-path1-20260914T1500Z-1900Z-r1` (offline page: `eth_requestAccounts` + `personal_sign` only) and hands the signature string to the Lead (a signature is public data; no key ever leaves the wallet).
- Capture command (read-only mainnet Info API; window 2026-09-14T15:00:00Z → 2026-09-14T19:00:00Z, half-open): `python tools/capture_own_account_evidence.py --network mainnet --address 0x1E26…AC49 --coin BTC --start 2026-09-14T15:00:00Z --end 2026-09-14T19:00:00Z --run-id p012-path1-20260914T1500Z-1900Z-r1 --ownership-signature <sig file> --out C:/tmp/CLAUDE_P0_RUN_20260913/P012_PATH1_REAL_CAPTURE_20260915/r1` then `--verify-existing`. Expected content: fills T2/T3/duplicate/T1-maker 16:03-16:14Z, funding 17:00Z + 18:00Z, close 18:08Z; account state.

Recorded by Claude Opus 5 Lead (743291).
