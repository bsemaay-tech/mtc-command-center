# KVM2 / Hostinger — first authorized read-only inventory — 2026-08-16

Status: OBSERVATION RECORD — READ-ONLY — NO CONFIGURATION CHANGED, NO SECRET
READ OR DISPLAYED. Authority: accelerated-contract clause 5
(`OWNER_DECISION_ACCELERATED_COMPLETION_2026-08-16.md`); key loaded into the
Windows ssh-agent by the owner personally; passphrase never touched an AI.

## Access route (verified live)

| Item | Value |
|---|---|
| Host | `srv1856225` (Hostinger VPS), `152.239.123.231` |
| Host key | pre-pinned in local `known_hosts` (all three types); `StrictHostKeyChecking=yes` used throughout — never blind-accepted |
| Principal | `baris`, uid 1000, groups `baris, sudo, users`, shell `/bin/bash` |
| Escalation | `sudo -n true` → rc 0 (**passwordless sudo for `baris`**) |
| Identity | `~/.ssh/hostinger_kvm2` via Windows ssh-agent |
| Operator-side note | ssh needs explicit `-o UserKnownHostsFile` (Turkish char in `%USERPROFILE%` breaks default resolution in some shells) |

## Observed state (2026-08-16 ~09:35Z)

- **OS:** Ubuntu 24.04.4 LTS, kernel `6.8.0-136-generic`, up 3 weeks (booted
  2026-07-25 17:45), NTP synchronized.
- **Resources:** 96 G disk (1.4 G used, 2%), 7.8 Gi RAM (443 Mi used), 2 vCPU.
- **Bridge: NOTHING INSTALLED — now a live observed fact, not just absence of
  records.** `/opt` is empty; no `/opt/mtc-bridge`, no `/etc/mtc-bridge`, no
  `/var/lib/mtc-bridge`, no `/var/log/mtc-bridge`, no `mtc-bridge` user, no
  custom unit files (`/usr/local/lib/systemd/system` absent; `/etc/systemd/
  system` carries only distro symlink units).
- **Firewall:** UFW active, default deny incoming / allow outgoing; the ONLY
  allow rule is 22/tcp (v4+v6), logging on.
- **Listeners:** sshd on 22 (v4+v6); systemd-resolved on loopback 53;
  `monarx-agent` (Hostinger security scanner) on `127.0.0.1:65529`. Nothing
  else. No public listener except SSH.
- **sshd:** `permitrootlogin no`, `passwordauthentication no`,
  `pubkeyauthentication yes`, port 22.
- **Hardening services:** fail2ban active; unattended-upgrades active;
  sysstat, logrotate, fstrim, apt-daily timers normal; `monarx-update` cron.
- **Running services:** distro-standard set only (cron, dbus, fail2ban, getty,
  monarx-agent, polkit, qemu-guest-agent, rsyslog, ssh, journald, logind,
  networkd, resolved, timedated, timesyncd, udevd, unattended-upgrades,
  user@1000). No app processes.
- **Tooling:** Python 3.12.3, git 2.43.0; **no docker, no pip3**.
- **Users:** only `baris` (uid 1000). Home dirs: only `/home/baris`.
- **Backups/monitoring: none.** No backup or monitoring agent beyond the
  Hostinger Monarx scanner and sysstat. No prometheus/node_exporter/restic/
  borg processes.
- **Last logins:** `baris` and one `root` console session on 2026-07-25 from
  the owner's IP; nothing since. wtmp begins 2026-07-25 (fresh provision).

Matches the 2026-07-25 owner-supplied snapshot in every checked respect;
kernel one patch newer (`-136` vs boot-era `-134`).

## Consequences for the deployment plan

1. **Clean target.** Nothing to archive or protect on-host before install
   (the pre-cutover archive decision concerns the retiring Windows machine,
   not KVM2). No existing state can be destroyed by an install.
2. **The proven GATEA recipe transfers structurally** (same Ubuntu 24.04,
   same Python 3.12): root-owned read-only release at
   `/opt/mtc-bridge/releases/<40-hex>`, pinned venv beside it, dedicated
   nologin `mtc-bridge` user, masked no-[Install] unit, `Restart=no`,
   `credential_free_disarmed` pinned, two writable paths only. Caveat stands:
   Gate-A acceptance belongs to `2ce41e34` on GATEA-STAGING; the candidate
   for KVM2 is **`62bf661b`** (dual-T0 accepted 2026-08-16) and must produce
   its own on-host evidence.
3. **UFW already default-deny with SSH-only** — the bridge's loopback-only
   listener (127.0.0.1:8790) adds no public surface; verify.sh's UFW and
   listener assertions can run unmodified.
4. **No pip3 on host** is fine: the installer builds a venv from the locked
   requirements (`requirements.lock`, 56 hashed packages); confirm the
   installer's bootstrap path (`python3 -m venv` + in-venv pip) — it does not
   need system pip.
5. **Monarx agent** is Hostinger's scanner on loopback; leave untouched;
   note it in the deployment record as pre-existing.
6. **Backups/monitoring do not exist** — the contract's operational
   verification (backup, restore, monitoring, rollback) must bring its own
   minimal mechanism; owner choices (provider/retention) remain the open
   owner inputs from the VPS-readiness refresh item 8.

## Host-bound plan skeleton (execution needs the separate clause-6 authorization)

1. Build release payload from `62bf661b` locally (`package.sh` path), record
   payload hashes.
2. Transfer payload; install via `install.sh` → root-owned release +
   pinned venv + `mtc-bridge` user + masked unit; NO enable, NO start.
3. Run `verify.sh` read-only assertions: identity, permissions, writable
   paths, UFW, closed 8790, masked/inactive unit.
4. Operational evidence: logrotate config, rollback rehearsal
   (`rollback.sh` stop/mask/preserve semantics), minimal backup+restore of
   the (empty) state dir, log/monitoring check.
5. Owner gates thereafter, each separate: TESTNET secret provisioning
   (never through AI), single first DISARMED start, clean-stop verification.
   ARM/mainnet/orders remain forbidden.

Rollback at any step: stop/mask (unit is masked and never enabled anyway),
remove release dir + venv + user — the host returns to today's observed clean
baseline, which this record documents.

## First published estimate under the accelerated contract (forecast, host-labelled)

Old mixed-host figures stay retired. Forecast, not measurement:

- **KVM2 host path** (steps 1–4 above + first-start window): **7–12 h**.
- **Local freeze/acceptance chain remaining** (V3 review close → Stage-1
  freeze → WP-I execution → Audit 2 (≤6 h cap, metered) → WP-A → final
  freeze): **8–15 h**, dominated by the metered Audit 2 cap and WP-I run.
- Owner-side actions (decisions, secret provisioning, authorizations):
  **~1 h** spread across gates.

Ranges assume no new REQUIRED findings force repairs; any repair adds its
tier-capped rounds.
