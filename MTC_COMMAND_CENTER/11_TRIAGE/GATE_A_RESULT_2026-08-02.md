# GATE A — RESULT (2026-08-02)

Executes `GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md` (`af071882`) as amended by
`GATE_A_PREREGISTRATION_ADDENDUM_A_2026-08-02.md` (`27a3a9d7`), on the host recorded in
`GATE_A_STAGING_HOST_PROVENANCE_2026-08-02.md` (`027f6b33`).

**Verdict: Gate A FAILS at A-2.** The WP-I candidate artifact cannot install on Linux. The runbook
requires stopping at the first FAIL, and the official gate stops here.

---

## 1. Report — runbook §5 format

```
host             : Ubuntu 24.04.4 LTS (GATEA-STAGING, Hyper-V Gen 2, expendable: yes)
artifact hash    : bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02
                   / bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02   (both equal)
A-1 preconditions: PASS
A-2 install      : FAIL  install.sh has CRLF line endings and cannot execute on Linux
A-3 suite        : NOT RUN  (gate stopped at A-2)
A-4 disarmed     : NOT RUN
A-5 restart      : NOT RUN
A-6 reconcile    : NOT RUN
A-7 observability: NOT RUN
A-8 loopback     : NOT RUN
A-9 secrets      : NOT RUN
```

## 2. A-0 — identity across the transfer: PASS

Transferred as a single tar (`b16ff1b1b095568b72616c9c3ba039fb26f03262d04bb5f4349ba977f2a9e3db`,
1,058,274,816 bytes, 8,223 entries) rather than 7,061 individual file copies, specifically to avoid
any line-ending translation in transit.

| Check | Result |
|---|---|
| `RELEASE_SHA` marker | `1adf9ae51b0ddfe81057860aec5c23bb842f5a84` |
| Manifest SHA-256 after transfer | `bfefea2f…ced02` — equals the source value |
| Manifest entries | 7,060 |
| Regular files | 7,061 |
| Total bytes | 1,051,904,669 |
| Full manifest verification | `sha256sum -c` over all 7,060 entries, **rc=0** |
| Non-regular entries in payload | none |

## 3. A-1 — clean-host preconditions: PASS

```
Ubuntu 24.04.4 LTS · kernel 6.8.0-136-generic · x86_64
Python 3.12.3  (lockfile targets 3.12)          ensurepip available
ufw active, Default: deny (incoming), only 22/tcp OpenSSH ALLOW IN
all installer-required commands present
HL_LIVE_ACK unset
/opt/mtc-bridge, /etc/mtc-bridge, /var/lib/mtc-bridge, the unit file — all absent
```

Both Addendum A §A.2 preconditions were satisfied by the **host build**, not by editing the payload.

## 4. A-2 — FAIL: the artifact ships CRLF and cannot execute on Linux

```
install.sh: line 37: $'\r': command not found
install.sh: line 38: set: pipefail: invalid option name
### dry-run exit=2 ###
```

The dry run died before performing any action; the host was left untouched (`/opt/mtc-bridge`,
`/etc/mtc-bridge`, `/var/lib/mtc-bridge`, the unit and the service user were all still absent
afterwards, verified explicitly).

### 4.1 The transfer is exonerated by the manifest itself

This is the important part, because CRLF has already produced one **false** failure in this programme
(the WP-L Phase 1 ledger-hash mismatch), and the obvious first suspicion is that the copy corrupted
the file.

| Evidence | Value |
|---|---|
| `install.sh` CR bytes on host | 434 |
| `install.sh` SHA-256 on host | `9ec660fbef7dfce874ed9b11f63f072cf26aa738167b7bab0baffa26610f6e56` |
| Same path in `RELEASE_SHA256SUMS` | `9ec660fbef7dfce874ed9b11f63f072cf26aa738167b7bab0baffa26610f6e56` |
| `sha256sum -c` on that single entry | `OK` |

The file on the host is **byte-identical to what the manifest describes**. The CRLF is therefore in
the artifact as built and as hash-verified — not introduced in transit.

### 4.2 Scope — it is not one file

Inside the candidate artifact:

| Asset | CR lines |
|---|---:|
| `install.sh` | 434 |
| `verify.sh` | 252 |
| `lib/common.sh` | 220 |
| `rollback.sh` | 185 |
| `package.sh` | 92 |
| `systemd/mtc-bridge-first-start.service.template` | 91 |
| `systemd/mtc-bridge-steady.service.template` | 86 |
| `env/mtc-bridge.env.template` | 38 |
| `logrotate/mtc-bridge` | 26 |
| **shell scripts with CRLF** | **19 of 19** |

`dos2unix install.sh` alone would not have been enough: the systemd unit template, the logrotate
policy and the env contract are all affected, so a "fixed" install would still have written a unit
file carrying `\r` into `ExecStart`, and a logrotate policy systemd-parsed with trailing carriage
returns.

### 4.3 Root cause — the BUILD step, not the committed blobs

> **CORRECTED 2026-08-02.** This section originally asserted the opposite — that the CRLF was in
> Git's object database and present on `origin/master`. **That was wrong.** It was measured with
> `git cat-file blob … | grep -c $'\r'` through a Git Bash pipe that translated git's stdout, i.e.
> the exact trap this programme already documents ("verify artifact identity from the committed
> blob, never the working copy"). An independent `gpt-5.6-sol` audit caught it. The corrected
> finding is below, established by a method that involves no pipe.

Object size needs no pipe and cannot be translated:

| Path | blob (`git cat-file -s`) | artifact on disk | diff |
|---|---:|---:|---:|
| `install.sh` | 19,908 | 20,342 | **434** |
| `lib/common.sh` | 8,153 | 8,373 | **220** |
| `systemd/mtc-bridge-first-start.service.template` | 3,489 | 3,580 | **91** |
| `evidence/ledger_schema.json` | 867 | 903 | **36** |

Each diff equals that file's CR count exactly. Counting `0x0d` bytes in the blob via `od` (no text
pipe) returns **0**.

**The committed blobs are LF-only. The repository is clean.** The CRLF is introduced at payload
build time: `package.sh:73` runs bare `git archive`, and the repo has `core.autocrlf=true`, so the
export applies CRLF conversion on Windows.

Proven directly:

```
git archive 1adf9ae5 …/install.sh                          →  20,342 bytes   (CRLF — the corrupt artifact)
git -c core.autocrlf=false -c core.eol=lf archive …        →  19,908 bytes   = exactly the blob size
```

So `origin/master` is **not** defective, and no renormalisation of committed content is required.
The earlier claim that "19 of 19 committed `*.sh` files carry CRLF" is withdrawn — those files are
LF in Git and appear as CRLF only in a Windows working copy, which `core.autocrlf=true` produces by
design.

The A-2 **FAIL stands unchanged**: the artifact that was hash-verified and transferred does carry
CRLF and cannot execute. Only the attribution moved — from the repository to the build step.

### 4.4 Why every prior check passed

Not one of them could have caught this:

- **WP-I static verification** hashed files. A CRLF file hashes perfectly.
- **The DeepSeek candidate audit** ran `4 passed` / `2 passed` — on Windows, where CRLF is correct.
- **`test_linux_deployment.py`** is, in the deploy README's own words, *"structural only"*.
- The same README states plainly: *"These assets have **never been executed**, on KVM2 or anywhere
  else. No Ubuntu run, no `install.sh` invocation, no `systemctl` call has happened."*

Gate A found it on the first real execution. This is the gate performing precisely the function it
was created for, and it is the strongest argument yet for the rule that a rehearsal must happen on a
disposable host before KVM2 — had this been attempted directly on KVM2, the one bounded
`KVM2-P4-02` install attempt would have been spent on a payload that could never have worked.

## 5. Required repair (implementer work — not performed here)

Much smaller than first thought, because the repository is clean:

1. **Fix the build.** `package.sh:73` must export without line-ending conversion —
   `git -c core.autocrlf=false -c core.eol=lf archive …`, or build the payload on Linux. Verified to
   produce byte-exact LF output equal to the blob sizes.
2. **Belt and braces:** add explicit `eol=lf` attributes for the Linux-parsed paths
   (`IBKR_PAPER_BRIDGE/deploy/linux/**`, `*.sh`, `*.service`, `*.template`, `logrotate/*`, the env
   template) so the export is deterministic regardless of a builder's local `core.autocrlf`. This
   changes attributes, **not** committed content.
3. **No `git add --renormalize`.** The committed bytes are already correct; rewriting them would
   produce a large diff for no benefit and move hashes unnecessarily.
4. Fix `lib/common.sh:98` (defect 2 in the recon list) —
   `find "$root" \( -type f -o -type d \) -perm /222 -print -quit`.
5. Rebuild the WP-I payload. This still yields a **new `RELEASE_SHA256SUMS` SHA-256** (the payload
   bytes change), so records quoting `bfefea2f…` become historical. `RELEASE_SHA` may stay
   `1adf9ae5…` if no commit is needed for step 1 — but step 1 *does* need a commit to `package.sh`,
   so expect both anchors to move.
6. Re-run Gate A from A-0. Nothing below A-2 has been established for the corrected artifact.

The Lead did **not** patch the artifact, the repo, or the host to make the install proceed. Doing so
would have converted the gate's finding into a hidden hand-fix, which is the failure mode the
clean-host rule exists to prevent.

## 6. Safety statement

No ARM, no order, no broker connection, no TESTNET, no mainnet, no wallet action, and no credential
value occurred at any point. The env file was never populated; `HL_LIVE_ACK` was never set. KVM2 was
not touched. `KVM2-Ubuntu-2404-Staging` (the 2026-07-27 VM) was not started, modified or deleted.
