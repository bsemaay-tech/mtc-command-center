# Phase-watch — dedicated read-only forced-command SSH design **V3** (T0 finding #3)

**STATUS: V3 FREEZE APPROVED BY OWNER 2026-08-18 — artifact set FROZEN at
`PHASE_WATCH_FC_FROZEN_V3/` (byte-exact, git-blob-OID + SHA-256 pinned, see its
`FREEZE_MANIFEST.md`). HELD for the exact pre-application T0 pair; NO KVM2 contact
or mutation. Owner-added hardening baked into the frozen artifacts: absolute
executable paths, sanitized `env -i`, restrictive `umask`, flock overlap
prevention, ACL-preserving atomic manifest replacement, full T/B/W falsification
scripts.**
V2 was accepted conceptually 2026-08-17; freeze was withheld pending the six V3
repairs below, all incorporated here. V1/V2 are superseded in place. No T0
dispatch and no KVM2 mutation before the owner's freeze approval and separate
exact application approval. `WATCH_ACTIVE: NO` throughout.

## 1. Account + TWO-LAYER server enforcement (V3 req. 1)

Dedicated unprivileged **`mtc-watch`** account (locked password, no groups,
`/bin/sh` only so sshd can exec the forced command):

```
useradd --system --create-home --home-dir /home/mtc-watch --shell /bin/sh mtc-watch
passwd -l mtc-watch
```

**Layer 1 — sshd server config** (`/etc/ssh/sshd_config.d/70-mtc-watch.conf`):

```
Match User mtc-watch
    ForceCommand /usr/local/bin/mtc-watch-collect
    DisableForwarding yes
    PermitTTY no
    PasswordAuthentication no
    KbdInteractiveAuthentication no
    AuthorizedKeysFile /etc/ssh/authorized_keys.d/mtc-watch
    AllowAgentForwarding no
    X11Forwarding no
```

`ForceCommand` is an absolute path and applies regardless of any key options, so
even a rogue/edited key line cannot escape it.

**Layer 2 — root-owned authorized_keys entry** (`/etc/ssh/authorized_keys.d/mtc-watch`,
`root:root` 0644 — the account cannot edit its own restrictions):

```
command="/usr/local/bin/mtc-watch-collect",restrict ssh-ed25519 <OWNER-SUPPLIED-PUBKEY> mtc-watch-ro
```

Both layers force the same absolute command; either alone suffices, both must be
present. The owner generates the keypair himself; **the AI never displays, copies,
serializes, or reads the private key** — all verification uses fingerprints only.

## 2. Pre-application test matrix + safe change procedure (V3 req. 2)

Run from Windows with the dedicated key after provisioning, BEFORE the watcher
uses the account. Every test's expected result is stated; any deviation aborts.

| # | Test (client command) | Expected |
|---|---|---|
| T1 | `ssh -i key mtc-watch@host check1` | service-state output, exit 0 |
| T2 | `ssh -i key mtc-watch@host` (no command, interactive) | `mtc-watch-collect` runs with empty `SSH_ORIGINAL_COMMAND` → "refused", exit 1; NO shell |
| T3 | `ssh -i key mtc-watch@host 'id; uname -a'` | forced command runs instead; unknown ID → "refused", exit 1 |
| T4 | `ssh -tt -i key mtc-watch@host check1` | PTY refused (`PermitTTY no`) |
| T5 | `ssh -L 9999:127.0.0.1:8790 -i key mtc-watch@host check1` | forwarding refused (`DisableForwarding`) |
| T6 | `ssh -R`/`-D` variants | refused |
| T7 | `scp -i key mtc-watch@host:/etc/passwd .` and `sftp -i key mtc-watch@host` | both fail (ForceCommand replaces the scp/sftp server; no sftp subsystem for this user) |
| T8 | `ssh -i key mtc-watch@host check99` | "refused: unknown check id", exit 1 |
| T9 | `ssh mtc-watch@host` with a DIFFERENT key | authentication refused (only the one key is authorized) |
| T10 | password/keyboard-interactive attempt | refused by Match block |

**Safe change procedure (root, one held session):**
1. Keep an existing root SSH session OPEN for the whole window (rollback lifeline).
2. Write the new drop-in + key file; `sshd -t` MUST pass before anything reloads;
   on any error, delete the drop-in and stop.
3. `systemctl reload sshd` (reload, not restart — existing sessions survive).
4. Run T1–T10. Any deviation → rollback: remove
   `/etc/ssh/sshd_config.d/70-mtc-watch.conf` and the key file, `sshd -t`,
   `systemctl reload sshd`, confirm normal login from a second session, record.
5. Only after T1–T10 pass is the watcher client allowed to use the account.

## 3. Backup contract V3 — root orchestrator, staging, atomic promote (V3 req. 3)

V2's flaw (owner-caught): `mtc-bridge` cannot write into `root:mtc-bridge 0750`.
V3 uses a **root-run orchestrator** with a bounded staging area:

`mtc-bridge-backup.service` (oneshot, `User=root`) runs
`/usr/local/sbin/mtc-bridge-backup` (root:root 0755, frozen text in the package):

1. **Stage:** create `/var/backups/mtc-bridge/.staging/<runid>/` fresh,
   `mtc-bridge:mtc-bridge` 0700 (`.staging` itself root-owned 0711; refuse if the
   runid path already exists; `lstat` every path — regular dirs only, never
   follow symlinks).
2. **Create:** `runuser -u mtc-bridge -- python3 .../wal_state_bundle.py create`
   writing ONLY into that staging dir — the Bridge user touches nothing else.
3. **Verify:** `runuser -u mtc-bridge -- ... wal_state_bundle.py verify` on the
   staged bundle. Nonzero → abort: staging kept for diagnosis, manifest records
   failure, promotion and prune DO NOT run.
4. **Promote (atomic):** root `lstat`s the staged bundle (regular file, expected
   owner, nonzero size), computes SHA-256, then `mv` (same filesystem → atomic
   rename) into `/var/backups/mtc-bridge/`, `chown root:root`, `chmod 0444`,
   then `chattr +i` (immutable; removed only by the prune step of a LATER
   successful run).
5. **Manifest (V3 req. 4):** root writes `status.json.tmp` then atomically
   renames to `/var/backups/mtc-bridge/status.json` (root:root 0644):

```json
{ "bundle": "<name>", "size_bytes": N, "created_utc": "<ISO>",
  "verify_result": "PASS|FAIL", "sha256": "<hex>",
  "last_success_utc": "<ISO>", "consecutive_failures": N }
```

6. **Prune:** ONLY after a fully successful create+verify+promote; `chattr -i`
   then delete bundles beyond retention 14, oldest first, and **never the last
   known-good bundle** (the one named in `status.json`) even if it exceeds
   retention alone.

Directory: `/var/backups/mtc-bridge` root:root 0755; bundles root:root 0444+i;
ACL `u:mtc-watch:r--` on **`status.json` only** plus `u:mtc-watch:--x` traverse
on the directory — the watcher can read the manifest and nothing else.

**Watcher check4 (V3 req. 4):** the forced-command menu's `check4` becomes
`cat /var/backups/mtc-bridge/status.json`. The summarizer judges health from
`verify_result`, `created_utc` age (≤26 h) and `consecutive_failures` — never
from filenames or mtimes.

## 4. Backup failure tests (V3 req. 5) — part of pre-application acceptance

| # | Induced failure | Expected |
|---|---|---|
| B1 | create fails (tool exits nonzero — simulated via env/flag) | no promotion; staging preserved; `verify_result:FAIL`, `consecutive_failures`+1; last known-good untouched |
| B2 | verification fails (corrupt staged bundle deliberately) | same as B1 |
| B3 | partial output (truncate staged file mid-size) | verify catches → B1 path |
| B4 | symlink/path substitution (replace staging path or staged file with symlink before promote) | orchestrator `lstat` checks refuse; run aborts with failure manifest; nothing followed |
| B5 | failed promotion (pre-place a colliding immutable target) | `mv` fails → staging kept, failure manifest, last known-good untouched |
| B6 | retention ordering (state with exactly one good bundle + failing runs) | prune never runs on failure; the single known-good bundle is never deleted regardless of age |

Each test's commands + real output are recorded as evidence before application is
called accepted (D026 discipline).

## 5. Windows agent path — behavioral verification (V3 req. 6)

Local tests, fingerprints only, never key material:

| # | Test | Expected |
|---|---|---|
| W1 | `Restart-Service ssh-agent`, then `ssh-add -l` | pinned fingerprint still listed (DPAPI-persisted) |
| W2 | full logoff → logon, `ssh-add -l` | still listed |
| W3 | reboot, logon, `ssh-add -l` | still listed |
| W4 | scheduled-task context: run the collector preflight from the task account after W1–W3 | fingerprint check passes |

Honest reboot behavior (unchanged from V2): the task runs only while the owner is
logged on; after reboot the watch pauses until logon and the missing daily-OK
summary is the signal. "Run whether logged on" stays REJECTED (stores the Windows
password, escapes the DPAPI session, would push toward an unprotected key file).

## 6. Frozen artifact set for pre-application T0 review

Frozen byte-exact with SHA-256 at freeze approval: (1) `mtc-watch-collect` final
text (menu: check1 service state, check2 loopback status, check3 log listing +
tail, check4 `cat status.json`, check5 memory+disk, check6 err-log tail);
(2) sshd drop-in `70-mtc-watch.conf` exactly as §1; (3) the authorized_keys line
(pubkey placeholder until owner supplies it); (4) `/usr/local/sbin/mtc-bridge-backup`
final text + unit/timer files; (5) provisioning command list (useradd, files,
ACLs, `sshd -t`+reload); (6) the client diff (check IDs, `mtc-watch@host`,
`IdentitiesOnly=yes`, agent auth); (7) the T1–T10, B1–B6, W1–W4 test scripts.

## Gate chain (nothing automatic)

(a) owner FREEZE approval of this V3 → (b) artifacts frozen + pre-application T0
review → (c) owner's separate EXACT approval to apply to KVM2 → (d) application
via the deployment-owner route, with §2's held-session/rollback procedure →
(e) post-application verification (T/B/W matrices, evidence recorded) → (f) only
then the watcher acceptance re-audit (exact `claude-opus-5` xhigh +
`gpt-5.6-sol` xhigh) → (g) activation preconditions. **No T0 dispatch and no
KVM2 mutation before freeze approval — owner instruction 2026-08-17.**
