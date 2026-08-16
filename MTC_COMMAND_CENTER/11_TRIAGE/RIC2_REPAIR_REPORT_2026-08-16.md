# RIC2 final round-3 repair report

Date: 2026-08-16  
Workspace: `C:\BRIDGE_RELEASE_INTEGRATION_20260815`  
Candidate base: `be68953787c299bdaf30f83f301aa66a8ec0ea1f`  
Audit tier: **T0** (deployment, host-safety, authentication, and verifier surfaces)  
Role: Codex flagship implementer under `RIC2_FINAL_REPAIR.md`; no sub-delegation.

## Result

All candidate-code, launcher, and test repairs in the kickoff are implemented. The
mandatory local suite is green, every required D026 mutation was shown RED outside
the repository, and the final bytes are GREEN. No host or network was contacted; no
launcher, installer, verifier, service, firewall, credential, broker, exchange, ARM,
order, or trading action was executed. No Git commit, checkout, reset, stash, or push
was run against the candidate repository. The mandated suite's existing packaging tests
create and commit disposable fixture repositories under pytest temp; they do not touch
candidate Git state.

This is an implementer report, not a T0 acceptance verdict. The plan-text-only items
listed under **DEFERRED-TO-PLAN** remain for the Lead's Plan V5.

## Per-finding repair map

| Finding | Change | File:line | Verification |
|---|---|---|---|
| **Codex R1 — UFW false passes** | Replaced the first-field predicate with a complete ALLOW-row parser. It models explicit numeric ports/ranges in either the ordinary destination field or after a destination address, validates source/interface grammar, detects inclusive range membership for 8790, permits safe numeric 80/443 rules, recognizes the existing OpenSSH rule, and fails closed with an operator instruction for every unmodelled/application-profile rule. Added fixtures for destination-address 8790, `8000:9000/tcp`, `8790:8800/tcp`, `Nginx Full`, a safe numeric range, and OpenSSH. | `deploy/linux/lib/common.sh:158-270`; `tests/test_linux_deployment.py:272-353` | Final parametrized arm: 9 pass. D026 old first-field mutation: the destination-address and both range fixtures produced **3 failed**, rc 1, instead of silently passing. |
| **Codex R2 — stale exact Plan V4 commands** | Code cannot repair Plan V4 command authority. Recorded below for Plan V5 with the exact replacement candidate/payload/manifest identities. | **DEFERRED-TO-PLAN** | No stale command was executed. |
| **Codex R3 — independent side-effect evidence** | Code cannot define the host execution evidence contract without changing the plan. Recorded a stronger honest observation below. | **DEFERRED-TO-PLAN** | No host observation was fabricated or claimed. |
| **Codex R4 — rollback input/order contract** | Code cannot reorder V2/V4 plan stages or supply the reviewed host manifest-generation command. Recorded below for Plan V5. | **DEFERRED-TO-PLAN** | Existing rollback bytes were not changed. |
| **Codex R5 — log/disk honesty** | Implemented a real Bridge-only `/etc/cron.hourly` invocation (no systemd timer), changed the policy to `hourly` + `maxsize 64M`, used a timestamp precise to seconds, and installed/verified both assets from the accepted payload. The policy now calls 1 GiB only a nominal calculation and states that active growth and retained oversized generations leave worst-case use unbounded even after rotation. The explicit compensating-control row monitors `/var/log/mtc-bridge` against the 10 GiB tenant budget. | `deploy/linux/logrotate/mtc-bridge:7-30`; `deploy/linux/cron/mtc-bridge-logrotate:1-9`; `deploy/linux/install.sh:177-199,268-271,442-448`; `deploy/linux/verify.sh:232-248`; `tests/test_linux_deployment.py:591-605` | `bash -n` cron runner = 0; logrotate contract test passes; full suite passes. The test asserts the hourly runner, nominal-only wording, post-rotation unbounded caveat, monitoring control, and absence of `daily` in effective policy. `cron.hourly` is used because `cron.daily` cannot honestly deliver an hourly cadence. |
| **Codex R6 — three non-falsifying regressions** | Installer mutations now call `run_action "<id>"`; the test parses planned IDs and real guarded IDs directly from `install.sh`, rejects duplicates/mismatches, and rejects any raw `run` beyond the wrapper. The verifier test parses output redirection targets and positively allows only `/dev/null`, rejects write commands/`tee`/`sed -i`, and allows only `systemctl is-active/is-enabled`. The unit test parses effective non-comment settings and requires one exact `MemoryHigh` and `MemoryMax`. | `deploy/linux/install.sh:226-274,299-492`; `tests/test_linux_deployment.py:217-250,358-372,878-915` | Exact `/opt/hermes`, `/tmp` write, and commented-ceiling mutations each produced **1 failed**, rc 1. Final D026 group: **13 passed**, rc 0. |
| **Codex R7 — launcher identity-key file read** | Removed `$PublicKey`, its existence check, `ssh-keygen -lf`, and all public-file fingerprint parsing. Pinned the Lead-provided literal expected fingerprint and require `-contains` in `ssh-add -l -E sha256` output. No identity key file is opened. Preserved the real known-host pin check. | `C:\tmp\lane_out\Open-BridgeDashboard_v3.ps1:9-16,99-131` | Static fence: no `PublicKey` and no `-lf`. PowerShell AST errors = 0. Launcher SHA-256 `533F29DB75EBFA12D1BB1ECBE7F40D241D94364C4F41D74D293268B0F053ADCA`, 8651 bytes. |
| **Claude R1 — UFW destination-address/range false passes** | Same complete UFW grammar repair and fixtures as Codex R1. | `deploy/linux/lib/common.sh:158-270`; `tests/test_linux_deployment.py:272-353` | D026 destination-address, enclosing-range, and range-start mutation run: **3 failed**, rc 1; final fixtures GREEN. |
| **Claude R2 — frozen timestamp accepted** | Changed the arm from `>=` to strict `second > first`; also require `0 <= now(UTC)-status_ts < 5 seconds`. | `tests/test_api.py:63-66` | Exact verdict mutation `status.setdefault("status_ts", "2020-01-01T00:00:00+00:00")` produced **1 failed**, rc 1 at the strict-order assertion. Final arm GREEN. |
| **Claude R3 — rollback prerequisite/order missing** | Same plan-only deferral as Codex R4. | **DEFERRED-TO-PLAN** | No unreviewed host command or placeholder was invented in code. |

## Launcher v3 preservation checks

The launcher retains the v2 EAP-safe native wrapper, distinct ssh-agent rc 2 / rc
1 messages, real `ssh-keygen -F` known-host pin check, isolated `-F NUL` config,
`IdentityFile=NUL`, disabled proxy routes, strict host-key checking, readiness checks
before and after each probe, real exit-class reporting, and process ownership through
`try/finally`.

The requested optional hardening is documented at launcher lines 140-147:
`IdentitiesOnly no` is deliberate because authentication is agent-based, SSH may offer
other loaded agent keys, and the server accepts only authorized keys. This is a comment
only; behavior is unchanged.

Non-connecting local option validation used a `.invalid` placeholder:

```text
ssh-G-rc=0
user baris
hostname t0-repair-placeholder.invalid
batchmode yes
exitonforwardfailure yes
identitiesonly no
kbdinteractiveauthentication no
passwordauthentication no
stricthostkeychecking true
identityfile NUL
globalknownhostsfile NUL
userknownhostsfile C:\Users\BarışSemaay\.ssh\known_hosts
connecttimeout 10
powershell-ast-errors=0
```

## D026 RED/GREEN transcripts

Scratch root: `C:\tmp\ric2_d026_20260816` (outside the repository). Every mutation
was confirmed present with `rg` before the test ran. `PYTHONUTF8=1` and
`PYTHONDONTWRITEBYTECODE=1` were set for every command.

### Firewall destination-address and range defects — RED

Mutation: replace range membership with the audited first-field-only check:

```text
if (fields[1] == bridge_port || index(fields[1], bridge_port "/") == 1)
```

Command:

```text
python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py -k 'bridge_port_after_destination_address or bridge_port_inside_wide_range or bridge_port_at_range_start'
```

Real terminal result:

```text
FFF                                                                      [100%]
E           assert 0 != 0
E            +  where 0 = CompletedProcess(... stdout='PASS  ufw active, default-deny incoming; SSH port 22 allowed; Bridge port 8790 not exposed\n' ...).returncode
3 failed, 56 deselected in 1.69s
RED_RC=1
```

### Frozen 2020 timestamp — RED

Mutation and command:

```text
status.setdefault("status_ts", "2020-01-01T00:00:00+00:00")
python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests/test_api.py::test_status_exposes_deployment_identity_health_and_fresh_timestamp
```

Real terminal result:

```text
E       assert datetime.datetime(2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc) > datetime.datetime(2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
1 failed, 1 warning in 0.75s
RED_RC=1
```

### Unlisted `/opt/hermes` mutation — RED

Mutation and command:

```text
run install -d -o root -g root -m 0755 /opt/hermes
python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_dry_run_manifest_matches_every_real_install_mutation
```

Real terminal result:

```text
E       assert ['"$@"', 'install -d -o root -g root -m 0755 /opt/hermes'] == ['"$@"']
1 failed in 0.76s
RED_RC=1
```

### Verifier `/tmp` write — RED

Mutation and command:

```text
printf 'codex verifier mutation\n' > /tmp/codex-verifier-mutation
python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_verifier_is_read_only_and_binds_release_unit_venv_and_manifest
```

Real terminal result:

```text
E       AssertionError: assert {'/dev/null', '/tmp/codex-verifier-mutation'} == {'/dev/null'}
1 failed in 0.75s
RED_RC=1
```

### Commented-out ceilings — RED

Mutation and command:

```text
# MemoryHigh=768M
# MemoryMax=1G
python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_first_start_unit_is_separate_masked_design_and_restart_no
```

Real terminal result:

```text
E       AssertionError: assert None == ['768M']
1 failed in 0.78s
RED_RC=1
```

### Final repository bytes — GREEN

Command:

```text
python -m pytest -q -p no:cacheprovider \
  IBKR_PAPER_BRIDGE/tests/test_api.py::test_status_exposes_deployment_identity_health_and_fresh_timestamp \
  IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_dry_run_manifest_matches_every_real_install_mutation \
  IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_ufw_bridge_safe_invariant_is_multi_tenant_and_fail_closed \
  IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_first_start_unit_is_separate_masked_design_and_restart_no \
  IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_verifier_is_read_only_and_binds_release_unit_venv_and_manifest
```

Real terminal result:

```text
.............                                                            [100%]
13 passed, 1 warning in 3.39s
GREEN_RC=0
```

## Mandatory validation

### Shell and PowerShell syntax

```text
bash-n rc=0 IBKR_PAPER_BRIDGE/deploy/linux/install.sh
bash-n rc=0 IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh
bash-n rc=0 IBKR_PAPER_BRIDGE/deploy/linux/verify.sh
bash-n rc=0 IBKR_PAPER_BRIDGE/deploy/linux/cron/mtc-bridge-logrotate
powershell-ast-errors=0
```

### Full suite from repository root — final bytes

Command:

```text
PYTHONUTF8=1 python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests
```

Exact summary:

```text
1373 passed, 1 warning in 176.91s (0:02:56)
```

The warning is the existing Starlette/httpx deprecation warning. Exit code 0.

### Diff and scope checks

`git diff --check` returned 0. No protected Pine, parity, `MTC_V2`, trading,
broker, order, risk, store, schema, backtest, or strategy file is changed.

Exact `git diff --stat` (Git excludes the new untracked cron asset until the Lead
stages it):

```text
 IBKR_PAPER_BRIDGE/deploy/linux/README.md           |  15 ++-
 IBKR_PAPER_BRIDGE/deploy/linux/install.sh          |  88 +++++++-----
 IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh       | 103 +++++++++++++-
 .../deploy/linux/logrotate/mtc-bridge              |  22 +--
 IBKR_PAPER_BRIDGE/deploy/linux/verify.sh           |  17 ++-
 IBKR_PAPER_BRIDGE/tests/test_api.py                |   6 +-
 IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py   | 148 ++++++++++++++-------
 7 files changed, 292 insertions(+), 107 deletions(-)
```

New untracked candidate asset, separately included because `git diff --stat` omits it:

```text
IBKR_PAPER_BRIDGE/deploy/linux/cron/mtc-bridge-logrotate — 263 bytes
sha256 2942986AAB9E5862BF48BF9A117BD13208DF07223C5ABFD9E2D4DCAF88FAFA47
```

## Changed-file inventory

Candidate worktree:

1. `IBKR_PAPER_BRIDGE/deploy/linux/README.md`
2. `IBKR_PAPER_BRIDGE/deploy/linux/install.sh`
3. `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh`
4. `IBKR_PAPER_BRIDGE/deploy/linux/logrotate/mtc-bridge`
5. `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh`
6. `IBKR_PAPER_BRIDGE/deploy/linux/cron/mtc-bridge-logrotate` (new/untracked)
7. `IBKR_PAPER_BRIDGE/tests/test_api.py`
8. `IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py`

Required external outputs:

9. `C:\tmp\lane_out\Open-BridgeDashboard_v3.ps1`
10. `C:\tmp\lane_out\RIC2_REPAIR_REPORT.md`

Nothing else in the repository was changed.

## DEFERRED-TO-PLAN

1. **Codex R2 — exact-command restatement.** Plan V5 must explicitly override the
   incorporated V2 command block and restate the complete transfer, dry-run, one bounded
   install, and verify commands using payload `C:\tmp\payload-be689537` / remote
   `~/payload-be689537`, release
   `be68953787c299bdaf30f83f301aa66a8ec0ea1f`, and manifest SHA-256
   `58705d925c0a2488347f0b6206bb0e75cc130ae704c5cb52ffc4f945891a8a24`.
2. **Codex R3 — evidence-spec mechanism.** Plan V5 must replace point-in-time,
   unattributed socket samples and application logs as proof of no side effects.
3. **Codex R4 / Claude R3 — rehearsal ordering and commands.** Plan V5 must run the
   state capture before the rollback rehearsal, define the exact host-resident manifest
   path/format and SHA-producing command, pass the resulting file and 64-hex SHA to the
   literal `rollback.sh --state-manifest-file ... --state-manifest-sha256 ...` command,
   and state that the initial rehearsal has no `--to-*` arguments.

### Strongest honest host-side observation proposed for Codex R3

Use an operator-owned, root-side event capture that starts before the dashboard attempt
and stops only after the response and persistence snapshots are complete: preferably an
eBPF/BCC `tcpconnect`-class trace filtered to the Bridge service cgroup/UID, recording
monotonic timestamp, PID, UID, executable/cgroup, destination address, and destination
port for every connect event. Bind the observed PID/UID/cgroup to the systemd unit before
and after the window. A rapid `ss -ntupH` loop with PID/UID attribution may be retained as
supplemental evidence, but must be labelled sampled and not exhaustive. Independently,
capture a read-only SQLite orders-table census/IDs and database/WAL identity before and
after the attempt and require exact equality together with the exact credential-free 409
response and unchanged `state_version`. If the attributed event tracer or SQLite read
cannot run, the evidence row must STOP; point samples or service logs must not substitute.
