# FastAPI 0.140.0 rollback walk — real command evidence

**Date:** 2026-08-24  
**Component:** FastAPI 0.140.0, entry 0008 in `DEPENDENCY_LEDGER.md`  
**Environment:** throwaway venv under this output directory; Python 3.14.2; pip 25.3; no repository interpreter/environment changed.  
**Scope:** component distribution only, installed with `--no-deps`. This proves that the exact hash-verified FastAPI artifact can be installed, removed and restored. It does **not** claim the Bridge application or its full 56-package environment was run under Python 3.14, and it does not replace Bridge compatibility tests for a future version change.

## Why this is a rollback

The repository has one historical Bridge lock creation and no earlier FastAPI lock revision. There is therefore no honest older repository-approved FastAPI version to invent. The walked prior state is the exact pinned component state established at the first install: `fastapi==0.140.0`. The walk snapshots that state, removes the component, proves absence, and reinstalls the same prior state from an immutable hash input. A future version bump must perform the stronger A→B→A walk between two accepted full locks.

## Hash input

Temporary input (deleted after the walk):

```text
fastapi==0.140.0 \
    --hash=sha256:e951c0a0d9540bf5d9a2a9e078fd415da2ab7e312d435139e7d9e2e7fe9f0b23 \
    --hash=sha256:f338951b82fd74ca8f843163aec43ea1a1ce84d515415a50fa98fa25572a5544
```

Temporary input SHA-256: `57389a87772dc467fa9af30745acb6548dec5029fd42c43eac96654568b1d227`.

These two hashes are copied from `IBKR_PAPER_BRIDGE/requirements.lock` lines 523–525. pip selected the wheel whose SHA-256 is `e951c0a0d9540bf5d9a2a9e078fd415da2ab7e312d435139e7d9e2e7fe9f0b23`.

## Commands executed

PowerShell variables resolved to:

```text
OUT_DIR=C:\WPP024_20260824\MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_24_OSS_LEDGER_2026-08-24
VENV=C:\WPP024_20260824\MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_24_OSS_LEDGER_2026-08-24\_tmp_rollback_venv
```

The material commands were:

```powershell
python -m venv $venv
& $py -m pip freeze
& $py -m pip install --disable-pip-version-check --no-deps --require-hashes -r $pin
& $py -c "import importlib.metadata as m; print('FASTAPI_VERSION=' + m.version('fastapi'))"
& $py -m pip show fastapi
& $py -m pip uninstall -y fastapi
& $py -c "import importlib.util; print('FASTAPI_PRESENT_AFTER_REMOVE=' + str(importlib.util.find_spec('fastapi') is not None))"
& $py -m pip install --disable-pip-version-check --no-deps --require-hashes -r $pin
& $py -c "import importlib.metadata as m; print('RESTORED_FASTAPI_VERSION=' + m.version('fastapi'))"
& $py -m pip freeze
```

## Real output

Exit code: **0**. Start `2026-08-24T17:11:17.6159788Z`; end `2026-08-24T17:11:31.3580011Z`.

```text
Python 3.14.2
pip 25.3 from ...\_tmp_rollback_venv\Lib\site-packages\pip (python 3.14)

BASELINE_FREEZE_BEGIN
BASELINE_FREEZE_END

INSTALL_1_BEGIN
Collecting fastapi==0.140.0 (from ...\_rollback_fastapi_pin.txt (line 1))
  Downloading fastapi-0.140.0-py3-none-any.whl (130 kB)
Installing collected packages: fastapi
Successfully installed fastapi-0.140.0
INSTALL_1_END
FASTAPI_VERSION=0.140.0
Name: fastapi
Version: 0.140.0
Summary: FastAPI framework, high performance, easy to learn, fast to code, ready for production
Home-page: https://github.com/fastapi/fastapi
License-Expression: MIT
Location: ...\_tmp_rollback_venv\Lib\site-packages
Requires: annotated-doc, pydantic, starlette, typing-extensions, typing-inspection
Required-by:
PINNED_STATE_SHA256=57389a87772dc467fa9af30745acb6548dec5029fd42c43eac96654568b1d227

UNINSTALL_BEGIN
Found existing installation: fastapi 0.140.0
Uninstalling fastapi-0.140.0:
  Successfully uninstalled fastapi-0.140.0
UNINSTALL_END
FASTAPI_PRESENT_AFTER_REMOVE=False

RESTORE_BEGIN
Collecting fastapi==0.140.0 (from ...\_rollback_fastapi_pin.txt (line 1))
  Using cached fastapi-0.140.0-py3-none-any.whl (130 kB)
Installing collected packages: fastapi
Successfully installed fastapi-0.140.0
RESTORE_END
RESTORED_FASTAPI_VERSION=0.140.0

FINAL_FREEZE_BEGIN
fastapi==0.140.0
FINAL_FREEZE_END
```

## Result and limits

- **Walk result: PASS.** Baseline had no FastAPI; the exact pin installed; removal was observed (`FASTAPI_PRESENT_AFTER_REMOVE=False`); the prior exact pin was restored; final freeze matched `fastapi==0.140.0`.
- pip enforced the two repository hashes with `--require-hashes`; no unhashed or alternate version was accepted.
- Dependencies were deliberately not installed. Importing/running FastAPI would require the full locked closure and is outside this component-distribution rollback.
- No regression test is claimed, so D026 RED/GREEN does not apply to this evidence. The observed absent state is rollback-state proof, not defect-closure proof.
- The venv and temporary pin file were deleted after capturing this output; cleanup verification is recorded below.

## Cleanup verification

The exact generated venv path was resolved and verified to be a child of this output directory before `Remove-Item -LiteralPath ... -Recurse -Force`. The temporary pin file was removed separately. Final `Test-Path` results and git status are part of Lane QA in `LANE_REPORT.md`.
