# WP-L Phase 1 — Verification Record (2026-08-01)

**Author:** Grok via _deepseek_driver under Codex Lead oversight
**Scope:** WP-L Phase 1 — verification only. **No Ubuntu execution.**
**Status:** PASS / Lead-verified / independently audited

---

## 1. Scope and Identities

| Item | Value |
|---|---|
| Source origin/master | `637307e83951ffe23e768ed8e50ddaf8712b0660` |
| Old-base | `6fe0130f45f3c821e230ee30d1e61f548741a6a1` |
| Plan blob SHA-256 | `a07c90cc49a4f34910f82bd9c94ba4fb71d76b511bc2cabe0bd727faf57fe3ee` |

WP-L Phase 1 is **verification only**; no Ubuntu execution was performed. All Ubuntu evidence below is **owed later** (WP-L Phase 2 — Ubuntu revalidation / WP-A).

---

## 2. Semantic-Port Manifest — Five Plan Section-17 Areas

| # | Area | Exact artifacts (repo paths) | Named static tests (WP0) | Rationale | Current static result | Ubuntu evidence owed later |
|---|---|---|---|---|---|---|
| 1 | systemd startup/restart/shutdown | `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template`, `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-steady.service.template`, `IBKR_PAPER_BRIDGE/deploy/linux/install.sh` | `test_first_start_unit_is_separate_masked_design_and_restart_no`, `test_steady_unit_is_separate_restart_enabled_and_not_enableable`, `test_installer_never_installs_the_steady_profile` | Port must preserve service lifecycle semantics | Static inspection: units present, directives consistent; steady profile stays inert | Executed start/restart/stop on Ubuntu |
| 2 | SIGTERM shutdown chain | `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template`, `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-steady.service.template`, `IBKR_PAPER_BRIDGE/bridge/app.py:72-83`, `IBKR_PAPER_BRIDGE/bridge/engine/engine.py:229-236` | none — see §6 gap I-R4 | Clean shutdown must propagate SIGTERM through the engine | Static: `KillSignal=SIGTERM`, `TimeoutStopSec=45`, `FinalKillSignal=SIGKILL`; lifespan `finally` awaits `engine.stop` | Executed SIGTERM shutdown, verify clean exit |
| 3 | paths/permissions | `IBKR_PAPER_BRIDGE/deploy/linux/install.sh`, `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh`, `IBKR_PAPER_BRIDGE/deploy/linux/logrotate/mtc-bridge` | `test_canonical_paths_ownership_modes_and_no_symlink_contract_are_structural`, `test_payload_tree_rejects_symlinks_and_special_entries` | Port must preserve filesystem layout and ownership | Static: paths/permissions unchanged vs old-base | Executed permission/ownership checks on Ubuntu |
| 4 | environment isolation | `IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template`, `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template`, `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-steady.service.template`, `IBKR_PAPER_BRIDGE/bridge/app.py` (state-db resolution) | `test_state_path_default_is_preserved_and_posix_env_override_resolves`, `test_state_path_cli_wins_and_bad_values_fail_closed`, `test_env_template_contains_names_and_comments_but_no_definitions` | Port must preserve isolation boundaries | Static: isolation config present, unchanged; template carries names only, no values | Executed env isolation verification on Ubuntu |
| 5 | dependency installation | `IBKR_PAPER_BRIDGE/requirements.in`, `IBKR_PAPER_BRIDGE/requirements.lock`, `IBKR_PAPER_BRIDGE/requirements.txt`, `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py`, `IBKR_PAPER_BRIDGE/deploy/linux/install.sh` | `test_lock_is_exact_fully_hashed_and_contains_every_direct_dependency`, `test_lock_generation_contract_targets_python_312_linux_with_hashes`, `test_installer_uses_per_sha_venv_hashes_and_binary_wheels_only` | Port must preserve pinned dependency set | Static: zero diff vs old-base (see §3); lock covers every direct dependency | Executed dependency install on Ubuntu |

---

## 3. Identity Proof (exact PowerShell, C:/WPL)

```powershell
Set-Location -LiteralPath 'C:\WPL'
$old = '6fe0130f45f3c821e230ee30d1e61f548741a6a1'
$master = 'origin/master'
git merge-base --is-ancestor $old $master
git diff --exit-code $old $master -- IBKR_PAPER_BRIDGE/deploy/linux IBKR_PAPER_BRIDGE/requirements.in IBKR_PAPER_BRIDGE/requirements.lock IBKR_PAPER_BRIDGE/requirements.txt IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py IBKR_PAPER_BRIDGE/tests/test_deployment_wrapper.py
```
Both exit 0; diff has no output.

Plan blob commands:
```powershell
Set-Location -LiteralPath 'C:\WPL'
$master = 'origin/master'
$planPath = 'MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md'
$planBlob = git rev-parse "${master}:$planPath"
$planBlob
python -c "import hashlib,subprocess,sys; b=subprocess.check_output(['git','cat-file','blob',sys.argv[1]]); print(hashlib.sha256(b).hexdigest())" $planBlob
```
Results: 9ecae648701fea832b1ad2fa5be2833b9936edf5 and a07c90cc49a4f34910f82bd9c94ba4fb71d76b511bc2cabe0bd727faf57fe3ee.

Ledger commands:
```powershell
Set-Location -LiteralPath 'C:\WPL'
$old = '6fe0130f45f3c821e230ee30d1e61f548741a6a1'
$master = 'origin/master'
$ledgerPath = 'MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json'
$ledgerBlob = git rev-parse "${master}:$ledgerPath"
$ledgerBlob
python -c "import hashlib,subprocess,sys; b=subprocess.check_output(['git','cat-file','blob',sys.argv[1]]); print(hashlib.sha256(b).hexdigest())" $ledgerBlob
(Get-FileHash -Algorithm SHA256 -LiteralPath $ledgerPath).Hash.ToLowerInvariant()
git check-attr text eol -- $ledgerPath
git diff --exit-code $old $master -- MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/EVIDENCE_LEDGER.jsonl
git diff --exit-code origin/master -- $ledgerPath
```
Results: blob 9433294c050b788dfd47064528ca252bc95bc01e; blob SHA-256 f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e; working SHA-256 b6580e31c0a794a83455ce1cfc4efb17a061a34bbe0e9c5b7df1feeb3064114a; text auto; eol unspecified; both diffs exit 0/no output. Byte proof: working 903 bytes, 36 CRLF/36 LF; blob 867 bytes, 0 CRLF/36 LF. Classification: Windows CRLF checkout conversion under text=auto; committed artifact matches canonical ledger hash and is not stale.

---

## 4. Exact Lead-Run Tests (from C:/WPL/IBKR_PAPER_BRIDGE)

```powershell
Set-Location -LiteralPath 'C:\WPL\IBKR_PAPER_BRIDGE'
python -m pytest -q tests/test_linux_deployment.py tests/test_deployment_wrapper.py -p no:randomly
```
Exit 1; 1 failed, 34 passed in 0.86s; only `tests/test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate` failed.

```powershell
Set-Location -LiteralPath 'C:\WPL\IBKR_PAPER_BRIDGE'
python -m pytest -q --ignore=TSP1009B.pytest_tmp_s1r1 -p no:randomly
```
Exit 1; 2 failed, 1304 passed, 1 warning in 151.34s; failures were `tests/test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate` and `tests/test_wal_state_bundle.py::test_invariants_preserve_risk_and_history`; the second failure expected schema_version `"2"` versus actual `"4"`. Both are pre-existing/out of scope; no fix.

---

## 5. Ledger Classification

| Item | Value |
|---|---|
| Expected ledger hash | `f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e` |
| Committed Git blob SHA-256 | equals expected hash, for blob `9433294c050b788dfd47064528ca252bc95bc01e` |
| Windows working file | `b6580e31c0a794a83455ce1cfc4efb17a061a34bbe0e9c5b7df1feeb3064114a` |
| Git attribute | `text=auto` |
| Ledger/source unchanged since | `6fe0130f` (old-base) |

**Classification:** Windows CRLF / raw-working-copy hash-fixture mismatch.
- **Not** Linux-package drift.
- **Not** a stale committed ledger hash.

**Fix:** out of scope for WP-L Phase 1; no fix proposed here.

---

## 6. Static Signal Chain

- Units use `KillSignal=SIGTERM`, `TimeoutStopSec=45`, `FinalKillSignal=SIGKILL`.
- FastAPI lifespan `finally` awaits `engine.stop`.
- **Static Windows evidence cannot prove executed-Ubuntu clean shutdown.**
- **I-R4 stays COVERED-STATIC / open** for WP-L Phase 2 — Ubuntu revalidation / WP-A.

---

## 7. Lightweight Invariant Review

- Single-writer protected-core ownership is preserved because WP-L Phase 1 made zero source/runtime changes; this is preservation by unchanged artifact identity, not new behavioral proof.
- No protected behavior changed (see §8).

---

## 8. Safety

- Nothing ported / cherry-picked.
- No cross-branch source operation.
- No Ubuntu / broker / network / ARM / TESTNET / VPS / runtime action.
- No protected behavior changed.

---

## 9. Hour Note

Last reproducible pre-WP-L ledger = WP-0 2.0 + WP-S 12.0 + contingency 3.0 + WP-R 3.5 = 20.5 h used, 29.5 h remaining. S3-STRUCT is outside the 50-hour ledger. Rejected WP-L documentation work has no reproducible actual-hours itemization. Exact post-WP-L booking remains for Lead Gate-7 closeout.

---

## 10. Verdict

**PASS** — evidence Lead-verified for WP-L Phase 1 (verification only).

Fresh independent audit: external Codex `gpt-5.6-sol` at `xhigh` effort, session
`019fbeb2-c64a-7310-b1a1-c2ff0116693b`, returned **PASS** with no required
findings and no optional nits. The auditor reproduced every identity/hash/diff
check and executed both mandated pytest commands. Its focused result was
`1 failed, 34 passed`; its full result was `2 failed, 1304 passed, 1 warning`.
The failures and classifications matched §4 exactly, and no third failure
occurred. Audit-target SHA-256:
`b7fdb456420fc36b186545c2312ba9c1265908932897cacc98e5276772e904eb`.

Lead closeout changed only this status/audit metadata after that PASS; no
command, evidence value, classification, scope statement, or source/runtime
artifact changed.

**Gate A is NOT ready** — WP-I readiness remains next. No Ubuntu before Gate A.

---

Self-check: zero command placeholders/ellipses; only this record edited.
