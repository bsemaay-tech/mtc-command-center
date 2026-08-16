# RIC1 implementation report — replacement initial-release candidate + launcher v2

Date: 2026-08-16  
Workspace: `C:\BRIDGE_RELEASE_INTEGRATION_20260815`  
Branch observed: `integration/bridge-release-20260815`  
Audit tier: **T0** (host/deploy/systemd/verification surfaces)  
Implementation status: **READY FOR LEAD REVIEW — no Gate-5/T0 acceptance claimed here**

No commit, checkout, reset, stash, push, branch, host contact, service action, firewall mutation, credential read, broker/exchange contact, ARM, order, or economic action occurred. The launcher was parsed and its OpenSSH configuration was evaluated with the non-connecting `ssh -G` mode; the launcher itself was not executed.

## Pre-repair state assessment

| Scope | Implemented before this lane? | Closure evidence before this lane? |
|---|---:|---:|
| C1 status/deployment facts | No | No |
| C2 multi-tenant UFW invariant | No; old predicate rejected all non-SSH allows | No |
| C3 complete dry-run manifest | No; dry run exited before the mutation list | No |
| C4 resource/log policy | No; no memory ceiling and misleading 64 MiB claim | No |
| C5 genuinely read-only verifier | No; unit and payload comparisons used temp files | No |
| C6 venv capability preflight | No | No |
| C7 regression/D026 evidence | No | No |
| Launcher v2 | No; v1 carried the reproduced failures | No |

## Candidate changes

- `IBKR_PAPER_BRIDGE/bridge/api/routes.py:35-37,262-274` adds `host_identity`, `release_sha`, `service_start_ts`, per-response `status_ts`, and derived `service_health`. Health is `healthy` for normal DISARMED/ARMED service state, `degraded` for an invalid/interrupted state, and `halted` for KILLED. `MTC_BRIDGE_RELEASE_SHA` defaults to `unknown` when unset.
- `IBKR_PAPER_BRIDGE/bridge/static/index.html:101-105` and `bridge/static/app.js:129-133` render all five facts in the existing System panel without redesigning the dashboard.
- `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:157-185` replaces the SSH-only firewall assertion with `assert_ufw_bridge_safe`: UFW active, default deny incoming, port 22 allowed, and no inbound ALLOW for port 8790. Other ALLOW rules such as 80/443 are accepted.
- `IBKR_PAPER_BRIDGE/deploy/linux/install.sh:219-277` prints a complete, ID-keyed dry-run mutation manifest with exact expanded paths and exits before identity/filesystem/systemd mutation. It also read-only-verifies an existing service identity before printing.
- `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:61-68` and `install.sh:135` add the no-write `import venv, ensurepip` preflight before installation mutation, with a fail-closed `python3.12-venv` message.
- `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:43,60-61` adds the exact release-SHA environment value plus `MemoryHigh=768M` and `MemoryMax=1G`; `verify.sh:169-174` asserts the rendered values.
- `IBKR_PAPER_BRIDGE/deploy/linux/logrotate/mtc-bridge:7-18` changes retention to seven generations and `maxsize 64M`, names the two logs explicitly, computes the threshold budget as 1 GiB, and truthfully states that scheduled logrotate is not a hard quota and the between-run policy-only worst case is unbounded.
- `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:132-153` and `verify.sh:191-201` replace temp-file comparisons with in-memory/process-substitution comparisons. `verify.sh` contains no `mktemp`, expected-unit temp path, or mutating systemctl action.
- Tests are in `tests/test_api.py:47-79`, `tests/test_dashboard_static.py:9-53`, and `tests/test_linux_deployment.py:199-336,339-352,565-573,846-866`.

## Finding-by-finding disposition

### Codex REQUIRED-1 through REQUIRED-10

| Finding | Disposition | Change and verification |
|---|---|---|
| R1 dashboard cannot pass D3-4 | **IMPLEMENTED** | Status facts and System-panel renderers at `routes.py:35-37,262-274`, `index.html:101-105`, `app.js:129-133`. RED/GREEN status/UI tests below. |
| R2 launcher lacks agent-only isolated route/pin store | **IMPLEMENTED** | `Open-BridgeDashboard_v2.ps1:99-146` checks the intended public-key fingerprint against `ssh-add -l`; `:151-174` uses `-F NUL`, `IdentityFile=NUL`, no proxy/jump, isolated global/user known-host stores, and disabled password/keyboard auth. `ssh -G` rc 0 evidence below. |
| R3 launcher failure/cleanup paths unreliable | **IMPLEMENTED** | `Open-BridgeDashboard_v2.ps1:76-95` performs proxy-free loopback HTTP 200 + page-marker checks; `:175-225` polls `HasExited` throughout readiness, reports the real child `ExitCode` with failure-class guidance, catches tunnel/browser failures, and owns the child in `try/finally`. |
| R4 incomplete dry run | **IMPLEMENTED** | Complete 31-ID action manifest at `install.sh:219-258`, emitted at `:274` before mutation; parity test compares IDs against every real mutation at `test_linux_deployment.py:212-264`. |
| R5 SSH-only firewall predicate | **IMPLEMENTED** | New invariant at `common.sh:157-185`; install call sites `install.sh:267,435`; verify call site `verify.sh:251`; fixture tests include 80/443 GREEN, 8790 RED, and missing-22 RED. |
| R6 unenforced resource/log claim | **IMPLEMENTED IN CANDIDATE; PLAN WORDING DEFERRED** | Memory ceilings at unit `:60-61`; verify assertions `:169-170`; honest rotation at logrotate `:7-18`. V2/V3 prose must be updated separately as listed below. |
| R7 application-controlled log absence as no-side-effect proof | **DEFERRED-TO-PLAN** | Plan must require an independent egress/socket/order-side-effect observation and retain exact before/after DISARMED evidence; no trading/runtime behavior was changed in this lane. |
| R8 rollback rehearsal inputs/disposition | **DEFERRED-TO-PLAN** | Plan must supply the exact state-manifest input/command, describe the rollback-manifest write honestly, and define partial-install disposition. `rollback.sh` was outside this repair allowlist. |
| R9 verifier not read-only | **IMPLEMENTED** | In-memory inventory comparison `common.sh:132-153`; in-memory unit comparison `verify.sh:191-201`; focused structural regression and Bash parse GREEN. |
| R10 venv prerequisite unproved | **IMPLEMENTED** | `preflight_venv_capability` at `common.sh:61-68`, called at `install.sh:135` before any target mutation and on the dry-run path. Mocked missing capability refuses with `python3.12-venv`. |

### Claude REQUIRED-1 through REQUIRED-7

| Finding | Disposition | Change and verification |
|---|---|---|
| R1 fatal warmup/native stderr under EAP Stop | **IMPLEMENTED** | Fatal warmup deleted. All direct native calls use `Invoke-NativeCapture` at launcher `:28-56`, which temporarily sets EAP to Continue, captures `$LASTEXITCODE`, then restores EAP. AST errors = 0. |
| R2 agent failure branch unreachable / ssh-add absent | **IMPLEMENTED** | Binary preflight at `:99-107`; local agent rc 2 and rc 1 have distinct messages at `:116-125`; intended public fingerprint is mandatory at `:132-146`. |
| R3 known_hosts file-only check | **IMPLEMENTED** | Real `ssh-keygen -F $HostAddr -f $KnownHosts` check at `:127-130`; any nonzero rc says STOP/report and never accept a new key. |
| R4 D3-4 capability absent | **IMPLEMENTED** | Same C1 status/API/System-panel patch and RED/GREEN tests as Codex R1. |
| R5 dashboard requirement citation mismatch | **DEFERRED-TO-PLAN** | Repair the audit/plan citation set so it references the eight actual dashboard owner items and separately identifies the multi-tenant item-12 source. |
| R6 D3-6 evidence can pass on stale-confirm refusal | **DEFERRED-TO-PLAN** | Require the dashboard ARM action with current `X-Confirm`, exact credential-free HTTP 409 detail, and before/after `state=DISARMED` with unchanged `state_version`; independently observe no egress/order effect. |
| R7 §9 delegates scope to superseded V2 | **DEFERRED-TO-PLAN** | State that V3 incorporates V2 §0-§8 with no independent V2 authority, and enumerate transfer/dry-run/install/read-only verify/Bridge-scoped evidence inside §9. |

## Launcher v2 validation

Artifact: `C:\tmp\lane_out\Open-BridgeDashboard_v2.ps1`  
Bytes: `9008`  
SHA-256: `e6e8bfa4217b05b0b134018175c082186b6fcbcb5c66d0cfbfa7ed84c2e1675c`

PowerShell parser output:

```text
AST_ERRORS=0
```

Non-connecting Windows OpenSSH option validation:

```text
SSH_G_RC=0
user baris
hostname 152.239.123.231
batchmode yes
exitonforwardfailure yes
kbdinteractiveauthentication no
passwordauthentication no
stricthostkeychecking true
identityfile NUL
globalknownhostsfile NUL
userknownhostsfile C:\Users\BarışSemaay\.ssh\known_hosts
connecttimeout 10
```

The exact `-F NUL`, `ProxyCommand=none`, and `ProxyJump=none` arguments were part of that rc-0 parse. `ssh -G` evaluates configuration only and made no network connection.

## D026 RED/GREEN evidence

### RED — status fields against exact pre-fix behavior

Command:

```powershell
$env:PYTHONUTF8='1'; python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests/test_api.py::test_status_exposes_deployment_identity_health_and_fresh_timestamp IBKR_PAPER_BRIDGE/tests/test_api.py::test_status_release_sha_defaults_to_unknown
```

Real output:

```text
FF                                                                       [100%]
FAILED ...::test_status_exposes_deployment_identity_health_and_fresh_timestamp - KeyError: 'host_identity'
FAILED ...::test_status_release_sha_defaults_to_unknown - KeyError: 'release_sha'
2 failed, 1 warning in 0.79s
```

### RED — UI, deploy, firewall, resource/log, and read-only tests against pre-fix behavior

Command:

```powershell
$env:PYTHONUTF8='1'; python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests/test_api.py::test_status_exposes_deployment_identity_health_and_fresh_timestamp IBKR_PAPER_BRIDGE/tests/test_api.py::test_status_release_sha_defaults_to_unknown IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py::test_dashboard_core_static_contract IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_installer_preflights_venv_capability_before_any_mutation IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_dry_run_manifest_matches_every_real_install_mutation IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_ufw_bridge_safe_invariant_is_multi_tenant_and_fail_closed IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_first_start_unit_is_separate_masked_design_and_restart_no IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_logrotate_contract_is_persistent_bounded_and_nonrestarting IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_verifier_is_read_only_and_binds_release_unit_venv_and_manifest
```

Real output (failure summary; all 11 arms went red):

```text
FFFFFFFFFFF                                                              [100%]
FAILED ...::test_dashboard_core_static_contract - AssertionError: assert 'Host' in html
FAILED ...::test_installer_preflights_venv_capability_before_any_mutation - assert 'python3.12-venv' in stderr
FAILED ...::test_dry_run_manifest_matches_every_real_install_mutation - AssertionError: set() != expected action IDs
FAILED ...::test_ufw_bridge_safe_invariant_is_multi_tenant_and_fail_closed[future_web_tenant-...-True]
FAILED ...::test_ufw_bridge_safe_invariant_is_multi_tenant_and_fail_closed[bridge_port_exposed-...-False]
FAILED ...::test_ufw_bridge_safe_invariant_is_multi_tenant_and_fail_closed[ssh_missing-...-False]
FAILED ...::test_first_start_unit_is_separate_masked_design_and_restart_no - missing MTC_BRIDGE_RELEASE_SHA
FAILED ...::test_logrotate_contract_is_persistent_bounded_and_nonrestarting - missing rotate 7
FAILED ...::test_verifier_is_read_only_and_binds_release_unit_venv_and_manifest - mktemp present
11 failed, 1 warning in 1.35s
```

The initial combined RED run's first status arm failed while resolving the not-yet-imported `socket` symbol. The status-only RED rerun above corrected the harness to patch Python's `socket.gethostname` and proved the intended missing-field behavior directly. No candidate implementation byte changed between those two RED runs.

### GREEN — focused regression set on final LF-normalized bytes

Same 11-node focused command as above.

```text
AST_ERRORS=0
...........                                                              [100%]
11 passed, 1 warning in 1.39s
```

Each new/extended regression arm therefore has a recorded pre-fix RED and final-byte GREEN. The warning is the pre-existing Starlette `httpx` deprecation warning.

## Final validation

Bash syntax:

```text
bash -n deploy/linux/install.sh  -> rc 0
bash -n deploy/linux/verify.sh   -> rc 0
bash -n deploy/linux/lib/common.sh -> rc 0
```

Line endings: all 11 changed repository files and the launcher were measured at `CR=0` after normalization. `git diff --check` returned rc 0 with no whitespace errors.

Mandated full suite, executed from repo root on the final normalized bytes:

```powershell
$env:PYTHONUTF8='1'; python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests
```

Exact final summary line:

```text
1367 passed, 1 warning in 183.59s (0:03:03)
```

Zero failures.

## DEFERRED-TO-PLAN list

1. Codex R7 — replace application-log absence with independent outbound/socket/order observation; preserve exact refusal/state evidence.
2. Codex R8 — provide exact rollback rehearsal manifest/command, admit its manifest write, and define partial-install failure disposition.
3. Claude R5 — correct the dashboard-owner-requirement citation/count discrepancy.
4. Claude R6 — require current-confirm exact credential-free refusal plus unchanged before/after state and independent side-effect observation.
5. Claude R7 — make V3's incorporation of V2 formal and enumerate the §9 action scope in the owner sentence.
6. Resource-claim wording — replace V2's 64 MiB total-cap/monitoring-as-enforcement language with the actual `MemoryHigh=768M`, `MemoryMax=1G`, seven-generation `maxsize 64M` threshold policy, 1 GiB threshold budget, and explicit non-hard-quota caveat.

These are plan-text/evidence-procedure changes outside the candidate-code and launcher outputs authorized to this lane.

## Changed-file stat

Exact read-only command:

```powershell
git -C C:\BRIDGE_RELEASE_INTEGRATION_20260815 diff --stat
```

Output:

```text
 IBKR_PAPER_BRIDGE/bridge/api/routes.py             |  27 ++++-
 IBKR_PAPER_BRIDGE/bridge/static/app.js             |   5 +
 IBKR_PAPER_BRIDGE/bridge/static/index.html         |   7 +-
 IBKR_PAPER_BRIDGE/deploy/linux/install.sh          | 101 +++++++++++-----
 IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh       |  59 ++++-----
 .../deploy/linux/logrotate/mtc-bridge              |  18 +--
 .../mtc-bridge-first-start.service.template        |   5 +
 IBKR_PAPER_BRIDGE/deploy/linux/verify.sh           |  19 +--
 IBKR_PAPER_BRIDGE/tests/test_api.py                |  35 ++++++
 IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py   |  17 +++
 IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py   | 134 ++++++++++++++++++++-
 11 files changed, 350 insertions(+), 77 deletions(-)
```

External outputs (not in Git stat):

- `C:\tmp\lane_out\Open-BridgeDashboard_v2.ps1`
- `C:\tmp\lane_out\RIC1_IMPLEMENT_REPORT.md`

No unlisted repository file was changed.
