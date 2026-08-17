# Phase-watch — dedicated read-only forced-command SSH design **V2** (T0 finding #3)

**STATUS: DESIGN + T0 PACKAGE ONLY. NOTHING APPLIED. No KVM2 contact made.**
V2 written 2026-08-17 per owner revision instructions; V1 (which reused the
interactive `baris` account and floated broad journal-group membership) is
SUPERSEDED by this file. Every server-side change requires the owner's separate
exact approval after review, then post-application verification.

## 1. Dedicated unprivileged account (owner req. 1)

A new Linux system account **`mtc-watch`**, used by nothing else:

```
useradd --system --create-home --home-dir /home/mtc-watch --shell /bin/sh mtc-watch
passwd -l mtc-watch
```

- No password login (locked), no sudo, no admin/adm/systemd-journal groups.
- `/bin/sh` is required only so sshd can execute the forced command; `restrict`
  in the key entry means every login runs only that command — the account has no
  interactive use.
- Its authorized_keys live OUTSIDE its own control so the account cannot alter
  its key restrictions:

```
# sshd_config (drop-in): AuthorizedKeysFile for mtc-watch only
Match User mtc-watch
    AuthorizedKeysFile /etc/ssh/authorized_keys.d/mtc-watch
```

`/etc/ssh/authorized_keys.d/mtc-watch` owned `root:root` 0644.

## 2. Key + forced command (owner req. 2)

Owner generates the keypair HIMSELF on Windows (AI never displays, copies,
serializes, or reads the private key at any point):

```bash
ssh-keygen -t ed25519 -C mtc-watch-ro -f "%USERPROFILE%\.ssh\mtc_watch_ro"
```

Single-line entry in `/etc/ssh/authorized_keys.d/mtc-watch`:

```
command="/usr/local/bin/mtc-watch-collect",restrict ssh-ed25519 <OWNER-SUPPLIED-PUBKEY> mtc-watch-ro
```

`/usr/local/bin/mtc-watch-collect` (root:root 0755; frozen text §6; hash-pinned at
freeze): reads `$SSH_ORIGINAL_COMMAND`, accepts ONLY a check ID from the fixed
menu, executes the corresponding hardcoded read-only command, refuses everything
else. Check IDs — never command strings — cross the wire; a fully compromised
client can only pick from the menu.

## 3. Windows authentication across reboots (owner req. 3)

**Mechanism: the Windows OpenSSH `ssh-agent` SERVICE, set to `Automatic`.** Keys
added to it persist across reboots, encrypted at rest by DPAPI under the owner's
Windows account. Owner does ONCE, himself:

```
Set-Service ssh-agent -StartupType Automatic; Start-Service ssh-agent
ssh-add "$env:USERPROFILE\.ssh\mtc_watch_ro"
```

After that the on-disk private key file may be moved to offline storage — the
agent's DPAPI-protected copy suffices. The collector authenticates via the agent
(`IdentitiesOnly=yes` with the public key present as `mtc_watch_ro.pub` so ssh
selects exactly this identity from the agent).

Reboot behavior, stated honestly: the scheduled task runs **only when the owner
is logged on** (its current, password-less configuration). After a reboot the
watch pauses until logon; the missing daily-OK summary is itself the signal.
The alternative — "run whether user is logged on" — requires storing the Windows
password with the task and runs outside the user's DPAPI session, which breaks
agent access and would push toward an unprotected key file. **Rejected: key
isolation wins over reboot coverage.**

## 4. Log access — exact ACLs only (owner req. 4)

No group memberships. File-level ACLs granting `mtc-watch` read on exactly the
two bridge log files plus traverse on the directory, with a default ACL so
rotated files inherit:

```
setfacl -m u:mtc-watch:rx /var/log/mtc-bridge
setfacl -m u:mtc-watch:r  /var/log/mtc-bridge/bridge.log /var/log/mtc-bridge/bridge.err.log
setfacl -d -m u:mtc-watch:r /var/log/mtc-bridge
```

**Journal access: dropped from the default design.** check6 becomes
`tail -50 /var/log/mtc-bridge/bridge.err.log` only — the stderr log plus
`systemctl status` output (check1) covers error visibility. If the owner later
decides journal access is essential, the narrow option is ONE exact sudoers line
(`mtc-watch ALL=(root) NOPASSWD: /usr/bin/journalctl -u mtc-bridge-first-start --since -24h -p warning --no-pager`)
invoked only from inside `mtc-watch-collect` — default OFF, separate approval.

## 5. Backup contract — separate from monitoring (owner req. 5)

Naming `/var/backups/mtc-bridge` does not make it real. The backup SYSTEM is its
own reviewed unit, independent of the watcher; monitoring only ever LOOKS at it.

| Aspect | Contract |
|---|---|
| Creator | root-installed systemd `mtc-bridge-backup.service` (oneshot) + `mtc-bridge-backup.timer`, running as the existing `mtc-bridge` service user |
| What | `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py create` against `/var/lib/mtc-bridge/bridge.db` (WAL-safe by construction; a plain file copy is never a backup) |
| Schedule | daily 03:00 UTC (timer `OnCalendar=*-*-* 03:00:00 UTC`, `Persistent=true`) |
| Destination + permissions | `/var/backups/mtc-bridge` — `root:mtc-bridge` 0750; bundles 0640 `mtc-bridge:mtc-bridge`; ACL `u:mtc-watch:rx` on the DIRECTORY only (monitoring can list names/sizes/dates but cannot read bundle contents) |
| Retention | 14 daily bundles; the service prunes older ones itself after a successful verify |
| Verification | every run immediately `wal_state_bundle.py verify`-s its own fresh bundle; verify failure fails the unit (visible in check1-style status and in check4's listing gap) |
| Restore drill | monthly, a HUMAN action (owner or Lead under owner authorization): restore the newest bundle to a scratch path, run verify against it, record the transcript as evidence in `11_TRIAGE/` — never automated, never done by the watcher |
| Monitoring's role | check4 = `ls -lh /var/backups/mtc-bridge` via the forced-command menu; healthy = newest bundle ≤ 26 h old. Monitoring creates, rotates, verifies NOTHING. |

The backup unit files are part of the frozen package (§6) and their installation
is a KVM2 change under the owner's separate approval.

## 6. Frozen artifacts for pre-application T0 review (owner req. 6)

To be frozen byte-exact (with SHA-256 of each) the moment the owner approves this
V2 direction — then reviewed BEFORE any application:

1. `/usr/local/bin/mtc-watch-collect` final text — menu: `check1` service state
   (is-active + status -n 0 + NRestarts), `check2` loopback `/api/status` via
   `curl -q -sS --max-time 15`, `check3` `ls -lh /var/log/mtc-bridge/` +
   `tail -3 bridge.log`, `check4` `ls -lh /var/backups/mtc-bridge`, `check5`
   MemoryCurrent + `df -h` (two fixed paths), `check6` `tail -50 bridge.err.log`.
2. The exact `authorized_keys.d/mtc-watch` line (pubkey placeholder until the
   owner supplies his generated public key).
3. The exact provisioning command list: useradd/passwd -l, sshd Match drop-in,
   script install + chmod, the three setfacl lines, backup unit + timer texts.
4. The client diff: `collect_kvm2_evidence.ps1` sends `checkN` IDs as
   `mtc-watch@152.239.123.231`, `IdentitiesOnly=yes`, agent-based auth, frozen
   client table retained as the redundant second allowlist.

## Gate chain (recorded; nothing here is automatic)

(a) owner reviews this V2 → (b) artifacts frozen + pre-application T0 review →
(c) owner's separate EXACT approval to apply to KVM2 → (d) application via the
deployment-owner route → (e) post-application verification → (f) only then the
acceptance re-audit of the whole watcher (exact `claude-opus-5` xhigh +
`gpt-5.6-sol` xhigh; capacity reopens 2026-08-19 but the audit is GATED on
(a)–(e) and the backup contract, not on the date) → (g) activation preconditions
(`WATCH_ACTIVE` flip needs the accepting pair + real backups + working log ACLs).

**No acceptance audit will be dispatched while finding #3 or the backup contract
is incomplete — per owner instruction 2026-08-17.** `WATCH_ACTIVE: NO` throughout.
