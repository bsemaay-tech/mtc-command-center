# GATE A RESULT — rerun on the accepted candidate `ebada020` (2026-08-08)

## VERDICT: **GATE A FAILS AT A-4.** A-0, A-1, A-2 and A-3 pass. Stopped per the first-FAIL rule.

The candidate is **not** at fault for A-4. The four repairs did what they were accepted to do — A-2, the
step that failed on 2026-08-02, now passes cleanly. A-4 fails because **the shipped deploy artifact
never selects the credential-free DISARMED start mode**, so the service tries to build a Hyperliquid
broker on startup, cannot resolve credentials from an intentionally-unset env file, and exits 1 before
it ever listens. That is flagship **NIT 1**, reproduced in production form. Full detail in §6.

**Safety posture is good:** it fails *closed*. `app_state` persisted as `DISARMED`, zero broker
connection attempts, no listener ever opened. The failure is that the service does not run at all,
which makes A-4's required "the ARM path refuses" confirmation impossible to obtain.

**Required deliverable of**
`GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md` §5, as amended by
`GATE_A_PREREGISTRATION_ADDENDUM_A_2026-08-02.md` and
`GATE_A_PREREGISTRATION_ADDENDUM_B_2026-08-08.md`.

| Item | Value |
|---|---|
| Candidate | `ebada020a59edf539f60acfbb3a6bf870c8679e9`, accepted 2026-08-08 (both flagships) |
| Artifact | `C:\WPI_ARTIFACTS\ebada020a59edf539f60acfbb3a6bf870c8679e9`, manifest `8fc30864…4700c9` |
| Transfer tar | `payload_ebada020.tar`, 1 039 774 720 B, SHA-256 `351923f3d72cef1c928d1c54405cfbade9bf6b67b839c69d1260026bc692cbc9` |
| Host | `gatea-staging` (`172.24.55.233`), Ubuntu 24.04.4 LTS, kernel 6.8.0-136-generic, x86_64 |
| Runbook rule | run in order, **stop at the first FAIL** |
| Prior attempt | 2026-08-02 FAILED at A-2 (CRLF in `deploy/linux/*.sh`) |

## Scoreboard

| Check | Result | Evidence |
|---|---|---|
| A-0 identity after transfer | **PASS** | `~/gatea-A0A1-20260808.log` |
| A-1 clean-host preconditions | **PASS** (after documented teardown, §1) | `~/gatea-A0A1-20260808.log` |
| A-2 install from artifact only | **PASS** | `~/gatea-A2-dryrun-20260808.log`, `~/gatea-A2-install-20260808.log` |
| A-3 Linux test suite | **PASS** | `~/gatea-A3-suite-20260808.log`, `~/gatea-A3-20260808.log` |
| A-4 starts DISARMED and stays that way | **FAIL** | `~/gatea-A4-20260808.log`, `~/gatea-A4-diag-20260808.log`, `/var/log/mtc-bridge/bridge.err.log` |
| A-5 restart safety | **NOT RUN** — first-FAIL rule | |
| A-6 reconcile completes | **NOT RUN** — first-FAIL rule | |
| A-7 observability | **NOT RUN** — first-FAIL rule | |
| A-8 loopback-only exposure | **NOT RUN** — first-FAIL rule | |
| A-9 no secrets on disk | **NOT RUN** — first-FAIL rule | |

A-5 through A-9 were **not** attempted. The runbook requires stopping at the first FAIL, and every one
of them presupposes a running service.

---

## 1. Pre-run host state — two documented cleanups, both owner-authorised

**Debris wipe.** `/` was 64% full with 14 G free of 39 G, and `~gatea` carried ≈14 G of accumulated
audit trees and tars from many earlier rounds. Barış authorised wiping all prior audit debris. Removed
≈12 G across `lead-ga3br2-*`, `payload*`, `fixpay*`, `recon`, `tmp-leadint`, `lead-build-round2-*`,
`integration-ebada020-lf2-*`, `opus5-audit-20260808` and the `v2_*`/`sub_*` tars. Result **64% → 30%
used, 26 G free.** Dotfiles, `.ssh`, and the Lead's `lead-int-*full.log` evidence were left intact.

**Stale install teardown.** A-1's clean-host assertions failed 7 of 8 against a *previous bridge
install left by the failed 2026-08-02 Gate A attempt*:

```
release_sha        a1dd5b467b12421f632bf3d8462a7244b39b2287
installed_at_utc   2026-08-02T02:20:50Z
unit state         masked, is-active=failed
service_started    false      secrets_provisioned false      firewall_modified false
```

`rollback.sh` takes `--to-release-sha` — it rolls back *to* a release and is not an uninstaller, and
no earlier release existed to roll back to. So the install was removed explicitly: unit stopped,
unmasked, `reset-failed`, unit files deleted from both `/usr/local/lib/systemd/system` and
`/etc/systemd/system`, `daemon-reload`, then `/opt/mtc-bridge`, `/etc/mtc-bridge`,
`/var/lib/mtc-bridge`, `/var/log/mtc-bridge`, `/etc/logrotate.d/mtc-bridge` removed and the
`mtc-bridge` user/group (uid 999) deleted. **Teardown leftovers: 0.** Evidence preserved first to
`~/teardown-a1dd5b46-20260808/` (install manifest, unit file, unit SHA-256, state-dir listing).

**Consequence that supersedes Addendum B §B.2's venv pin.** The venv every prior Linux run used,
`/opt/mtc-bridge/venvs/a1dd5b46…`, *was* that stale install's venv. It is gone. A-3 therefore ran on
the venv **A-2 itself installed**, `/opt/mtc-bridge/venvs/ebada020…/bin/python` — same CPython 3.12.3
and same pytest 9.1.1, so the pre-registered expectation is unaffected. This is strictly better
evidence: the suite now runs on the interpreter the deployment actually produces.

## 2. A-0 — identity after transfer: **PASS**

Transferred as **one tar**, never as loose files.

```
PASS  tar sha256              351923f3d72cef1c928d1c54405cfbade9bf6b67b839c69d1260026bc692cbc9
PASS  RELEASE_SHA marker      ebada020a59edf539f60acfbb3a6bf870c8679e9
PASS  manifest sha256         8fc30864ba342e53dcfc6b2938124f91d005f02671a332580a723f38fd4700c9
PASS  manifest entries        7059
PASS  regular file count      7060
PASS  total bytes             1033359158
      full manifest verification (all 7059 hashes)   sha256sum -c rc=0
      non-regular entries inside payload             none
```

**The 2026-08-02 A-2 defect is disproved on the target platform, not inferred from Windows.** Measured
after a real tar transfer onto the Linux host:

```
install.sh cr=0   common.sh cr=0   package.sh cr=0   rollback.sh cr=0   verify.sh cr=0
PASS  deploy/linux CR bytes total = 0
```

## 3. A-1 — clean-host preconditions: **PASS**, 0 failures

```
PASS  os id ubuntu · os version 24.04 · Ubuntu 24.04.4 LTS · kernel 6.8.0-136-generic · x86_64
PASS  python3.12 present · minor is 3.12 · ensurepip available
PASS  required commands present (none missing)
PASS  ufw active, default deny incoming, allow outgoing, 22/tcp OpenSSH only
PASS  HL_LIVE_ACK unset
PASS  absent: /opt/mtc-bridge /etc/mtc-bridge /var/lib/mtc-bridge /var/log/mtc-bridge
PASS  absent: both systemd units · /etc/logrotate.d/mtc-bridge · user mtc-bridge
PASS  no bridge process
```

Note on Addendum A's prediction **P1** (dry run must die with "ufw is not active" on a host whose ufw
is inactive): **not applicable this run** — ufw is active with default-deny inbound and SSH-only, so
the fail-closed branch was not the one under test. The installer's positive assertion passed instead.

## 4. A-2 — install from the immutable artifact only: **PASS** (install=0, verify=0)

The check that failed on 2026-08-02. It now passes.

**Pass 1, dry run — exit 0, side effects 0.** Verified payload checksums, `release file inventory
exactly matches RELEASE_SHA256SUMS`, `verify_lock: PASS: lock; packages=56`, `ufw active,
default-deny inbound, SSH-only`, `control port 8790 is closed`, `entrypoint binds 127.0.0.1:8790
only`. All six install paths and the service account confirmed still absent afterwards.

**Pass 2, real install — exit 0.** **No file on the host had to be edited to make it work**, so A-2's
FAIL condition was not triggered and the artifact is self-contained.

**Pass 3, `verify.sh` — exit 0.** Every assertion PASS, including: venv distributions exactly match
the hash-locked requirements; `/var/lib` and `/var/log` 750 `mtc-bridge:mtc-bridge`; `/etc/mtc-bridge`
750 `root:root`; env file 600 `root:root`; install manifest binds release and payload manifest hashes;
`HL_LIVE_ACK` absent from env file; unit carries no credential material; unit declares `Restart=no`,
`User=mtc-bridge`, `PrivateTmp=yes`, `ProtectSystem=strict`, `NoNewPrivileges=yes`,
`KillSignal=SIGTERM`, `TimeoutStopSec=45`, `StartLimitBurst=3`; unit bound to the exact release SHA
and per-SHA venv; **installed unit exactly matches the accepted release template**; no `[Install]`
section so it cannot be enabled; unit masked, not active, not enabled; restart-enabled steady unit
absent; logrotate installed; entrypoint binds loopback only; no listener on 8790; ufw unchanged.

```
[mtc-bridge] VERIFY PASS — release ebada020a59edf539f60acfbb3a6bf870c8679e9 installed, masked, unstarted, unarmed
is-active: inactive     is-enabled: masked
env file: 600 root:root, populated assignments = 0   (contract-only, as designed)
install_manifest.json: release_sha ebada020…, release_manifest_sha256 8fc30864…,
  first_start_unit_sha256 ed043ebe2eafcac74cda71e7d48c356e065009a3637f08be9d9d5b1a68ea013a,
  env_file_populated false, service_started false, service_enabled false,
  secrets_provisioned false, firewall_modified false
```

## 5. A-3 — Linux test suite: **PASS**, 0 unexpected failures

Interpreter: `/opt/mtc-bridge/venvs/ebada020…/bin/python`, CPython 3.12.3, pytest 9.1.1 — the venv
A-2 installed. Invocation matched the flagship's for comparability:
`-m pytest IBKR_PAPER_BRIDGE/tests -q -p no:randomly -p no:cacheprovider --basetemp=…`

```
2 failed, 1357 passed, 1 warning in 210.32s (0:03:30)
```

Exactly the pre-registered line. Node-ID set comparison, not just the count:

```
observed but NOT permitted   (any line here is a Gate A FAIL)   -> empty
permitted but NOT observed   (informational)                    -> empty

FAILED …/test_order_state.py::test_gc_referents_of_raw_aliases_contain_no_mutable_container
FAILED …/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container
```

Both are the known CPython-3.12-dependent gc-referents assertions, present identically on parent
`637307e8`, and both pass on Windows CPython 3.14. Carried as NIT 3: the production venv is 3.12, so
these two will be present on the deployed host and the production floor stays amber until scoped
separately. **Out of Gate A scope — they are not regressions of this candidate.**

The runbook's older A-3 expectation (the KVM2 ledger-hash test and the `schema_version == "2"` test)
is obsolete: both were fixed by the repairs, and the ledger test passing here confirms the CRLF
diagnosis rather than a real defect — recorded as Addendum B §B.2 requires.

## 6. A-4 — starts DISARMED and stays that way: **FAIL**

Method as pre-registered (Addendum A §A.4): `systemctl unmask` then `systemctl start`.

### 6.1 What happened

```
systemctl unmask  -> Removed "/etc/systemd/system/mtc-bridge-first-start.service"
systemctl start   -> exit 0 (systemd accepted the job)
unit result       -> Active: failed (Result: exit-code), status=1/FAILURE, Duration: 482ms
Main PID 177417   -> ExecStart=…/bin/python -m bridge.app  (code=exited, status=1/FAILURE)
listener on 8790  -> none, ever
```

### 6.2 Root cause — exact, from `/var/log/mtc-bridge/bridge.err.log`

The unit routes stderr to a file (`StandardError=append:/var/log/mtc-bridge/bridge.err.log`), which is
why the journal showed only systemd's own lines and no traceback:

```
Traceback (most recent call last):
  File ".../bridge/app.py", line 282, in <module>
    runtime_app = create_app(
  File ".../bridge/app.py", line 150, in create_app
    runtime_broker = broker or _build_broker(root, dry_run)
  File ".../bridge/app.py", line 244, in _build_broker
    account_address, api_wallet_key, _source = resolve_hyperliquid_credentials()
  File ".../bridge/settings.py", line 113, in resolve_hyperliquid_credentials
    raise RuntimeError(
RuntimeError: Hyperliquid credentials not found: set both HL_ACCOUNT_ADDRESS and
HL_API_WALLET_KEY in the process environment or in HKEY_CURRENT_USER\Environment
```

Module-level `create_app(...)` at `app.py:282` builds a broker unconditionally, and the broker
constructor resolves credentials. The env file is contract-only and `install.sh` deliberately leaves
every variable unset, so the resolver raises and the process dies before binding a port.

### 6.3 Confirmed on the host: the start mode really is `credentialed`

Executed as the service account against the installed release:

```
START_MODE_ENV_VAR    : MTC_BRIDGE_START_MODE
resolved start mode   : credentialed          <-- NIT 1, in production
CREDENTIAL_FREE const : credential_free_disarmed
```

The installed unit's `ExecStart` is bare `python -m bridge.app` with no `--start-mode`, and the env
file names no `MTC_BRIDGE_START_MODE`. So the credential-free DISARMED path that `17402a58` added and
that both flagships verified in-process **is unreachable from the deployment**. Exactly what flagship
NIT 1 predicted and what Addendum B §B.3 declared in advance.

### 6.4 Why this is a FAIL and not a pass with a nit

A-4 requires three confirmations: `app_state` durably not `ARMED`, **the ARM path refuses**, and no
broker connection attempted. Two hold. The third **cannot be obtained** — there is no listener, so
`POST /api/arm` returns `Errno 111 Connection refused` rather than a refusal from the application.

A required confirmation that cannot be performed is not a pass. The same principle D025 rule 1 applies
to auditors applies here: non-execution is never acceptance. And the runbook's own framing — *"a pass
here is the whole point of the 50 hours"* — means the service running DISARMED, which did not happen.

Recorded precisely, without overclaiming: **the service did not arm, and made no broker connection
attempt.** The exception is raised while *constructing* the broker, before any network I/O; the journal
shows zero connection lines and `ss -tnp` shows zero sockets owned by the service. It fails closed.

### 6.5 Evidence that the persisted state is unambiguous

The store was created and initialised before the failure, and it recorded the safe state:

```
/var/lib/mtc-bridge/bridge.db   188416 B, mode 600, owner mtc-bridge:mtc-bridge
meta = [('schema_version', '4'), ('app_state', 'DISARMED')]
tables = bars, decisions, directives, equity, events, fills, llm_calls, meta,
         order_identity, orders, risk_days, runs, signal_fingerprints,
         submission_attempts, submission_recovery_evidence, trades
```

So the *persisted* state is not ambiguous. What is unobservable is the *running* state, because there
is no running service.

### 6.6 This failure is pre-existing, not introduced by `ebada020`

The journal for this unit carries an identical failure from the earlier attempt:

```
Aug 01 23:35:27  mtc-bridge-first-start.service: Main process exited, code=exited, status=1/FAILURE
Aug 08 12:23:44  mtc-bridge-first-start.service: Main process exited, code=exited, status=1/FAILURE
```

It was invisible on 2026-08-02 because that run FAILED at A-2 and never reached A-4. Fixing the CRLF
defect is what allowed the gate to advance far enough to expose this one. **No repair regressed
anything; the gate simply got further than it ever had.**

### 6.7 Secondary defect noticed while diagnosing — not the A-4 cause

`resolve_hyperliquid_credentials()` (`bridge/settings.py:113`) tells a Linux operator to set variables
"in `HKEY_CURRENT_USER\Environment`" — a Windows registry path, in the failure message of a
Linux-only systemd service. Cosmetic, but actively misleading on the deployment target. Worth folding
into the NIT 1 repair rather than tracking separately.

**One diagnostic artefact, flagged so nobody mistakes it for a finding:** a by-hand
`sudo -u mtc-bridge … python -m bridge.app` reproduction returned
`ModuleNotFoundError: No module named 'bridge'`. That is the Lead's invocation missing the unit's
working directory, not a product defect. The authoritative error is the traceback in §6.2.

### 6.8 Host left in the documented safe posture

After collecting evidence the unit was returned to its installed contract — `systemctl reset-failed`
then `systemctl mask`:

```
is-active : inactive     is-enabled: masked     listener on 8790: none
```

The install itself is left in place at `ebada020…` so the A-4 repair can be retested without a
reinstall. Nothing was armed, no credential was provisioned, no firewall rule changed.

## 7. What is required before Gate A can be rerun

**The fix is a product change and needs its own authorization — none was taken here.** No product code
was modified during this run.

1. **Wire the start mode into the deploy artifact** (NIT 1). Either `ExecStart=… -m bridge.app
   --start-mode credential_free_disarmed` in both unit templates, or `MTC_BRIDGE_START_MODE` named in
   the env template and set by `install.sh`. Fold in §6.7's Windows-registry message while there.
2. Consider whether module-level `create_app()` at `app.py:282` should build a broker at import time
   at all — a first DISARMED start arguably should not construct a broker under any mode.
3. That changes product code, so it needs a new frozen SHA, a rebuilt artifact, and a fresh flagship
   round under D025. `ebada020` stays the accepted candidate for what it was accepted for; it is not
   retroactively rejected by an A-4 failure caused by an out-of-scope `deploy/` gap.
4. Rerun Gate A from **A-0** on the new SHA. A-0→A-3 passing here is strong evidence the rerun will
   reach A-4 again quickly.
5. NIT 3 remains separately owed: the two CPython-3.12 gc-referents failures will be on the deployed
   host until scoped and fixed.
