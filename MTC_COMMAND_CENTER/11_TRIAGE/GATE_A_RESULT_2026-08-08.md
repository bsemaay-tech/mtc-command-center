# GATE A RESULT — rerun on the accepted candidate `ebada020` (2026-08-08)

**Live record, updated as each check completes.** Required deliverable of
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
| A-4 starts DISARMED and stays that way | pending | |
| A-5 restart safety | pending | |
| A-6 reconcile completes | pending | |
| A-7 observability | pending | |
| A-8 loopback-only exposure | pending | |
| A-9 no secrets on disk | pending | |

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
