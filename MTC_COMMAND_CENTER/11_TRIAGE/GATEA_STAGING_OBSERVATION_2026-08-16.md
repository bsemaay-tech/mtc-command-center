# GATEA-STAGING first authorized observation — 2026-08-16

Status: **OBSERVATION RECORD — READ-ONLY ON THE GUEST — NO GUEST CONFIGURATION CHANGED.**
Authority: `HOST_CHANNEL_AUTHORIZATION_2026-08-16.md` (owner grant, GATEA-STAGING only).

## Headline

**The bridge was already deployed on this machine and already ran, disarmed, on
Hyperliquid TESTNET, for two and a half days.** Several current planning
documents state the opposite. They are wrong, and the evidence is on disk.

| Recorded claim | Observed reality |
|---|---|
| "Python install reproducible on Ubuntu — **never yet installed on a real Ubuntu machine**" | Installed 2026-08-08. `/opt/mtc-bridge/venvs/2ce41e34…` with Python 3.12.3. |
| "Service locked down on Ubuntu — written, **none verified on the target**" | Installed and verified. Fully hardened unit present at `/usr/local/lib/systemd/system/mtc-bridge-first-start.service`. |
| "First disarmed start on the server — **finish line, not started**" | **Started 2026-08-09 00:43:49 UTC**, stopped cleanly 2026-08-11 14:17:05 UTC. |
| "`gatea` has only enumerated command-specific NOPASSWD families; generic `sudo -n -v` requires a password" (`ROOT_CHANNEL_RECORD_GAP_2026-08-15.md:160-170`) | `gatea` has **`(ALL) NOPASSWD: ALL`**. `sudo -n true` returns 0. |
| Address `172.24.55.233` | **Stale.** Actual `172.25.67.77` this boot (Default Switch re-subnetted). |

## What ran, and for how long

```
2026-08-09T00:43:49Z  Started  mtc-bridge-first-start.service
                               MTC Crypto Paper Bridge (Hyperliquid TESTNET)
                               — first DISARMED start
2026-08-11T14:17:05Z  Stopping … Deactivated successfully … Stopped
                      Consumed 3min 42.891s CPU, 46.9M memory peak, 0B swap
```

Continuous run: **2 days 13 h 33 min**, clean shutdown, no crash, no restart
loop. An earlier attempt on 2026-08-01T23:35:27Z exited 1 and was repaired
before the successful start. State database `/var/lib/mtc-bridge/bridge.db`
exists with a 461 472-byte write-ahead log — real recorded activity, not an
empty start.

## The proven deployment recipe (reusable for KVM2)

Release `2ce41e34bceb599d80af24c5c33d835820ec321b`, root-owned and read-only
(`dr-xr-xr-x`), with its own pinned venv. Dedicated service account
`mtc-bridge` (uid 999, gid 988, `/usr/sbin/nologin`). The unit is deliberately
hard to misuse:

- installed **masked**, with **no `[Install]` section** — `systemctl enable` is
  structurally impossible, so it can never be pulled in at boot;
- `Restart=no` — a crash stays crashed for human inspection;
- the release path is the **exact 40-hex commit**, never a mutable `current`
  symlink, so the unit cannot drift;
- `MTC_BRIDGE_START_MODE=credential_free_disarmed` pinned inside the hashed
  unit;
- `NoNewPrivileges`, empty `CapabilityBoundingSet`/`AmbientCapabilities`,
  `ProtectSystem=strict`, `ProtectHome`, `ProtectProc=invisible`,
  `ProcSubset=pid`, `PrivateTmp`, `PrivateDevices`, `RestrictNamespaces`,
  `RestrictRealtime`, `RestrictSUIDSGID`, `LockPersonality`,
  `SystemCallFilter=@system-service` with `EPERM`,
  `RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX`, `UMask=0077`,
  `RemoveIPC`;
- exactly two writable paths: `/var/lib/mtc-bridge` and `/var/log/mtc-bridge`.

This is the hardened Linux service the deployment plans describe as unbuilt. It
is built, installed, and has run.

## Eight channel facts — now observed, not UNKNOWN

| Fact | Observed |
|---|---|
| Host / address | `gatea-staging`, `172.25.67.77` this boot; MAC `00-15-5D-01-BF-03` confirmed against the neighbour table |
| Host key | ED25519 `SHA256:btdfRdMTaVJDvZEO2fFhOES/cCLWyj0massIdwiGiMA`, matching the pre-existing pin; verified by `StrictHostKeyChecking=yes` against the pin remapped to the new address — never blind-accepted |
| SSH principal | `gatea`, uid/gid 1000 |
| Account shell | `/bin/bash` |
| Forced command | `none` (sshd effective config); `authorized_keys` carries no command restriction |
| Escalation | `(ALL : ALL) ALL` and `(ALL) NOPASSWD: ALL` — **full passwordless root** |
| Pre-`env` environment | `DBUS_SESSION_BUS_ADDRESS HOME LANG LOGNAME PATH PWD SHELL SHLVL SSH_CLIENT SSH_CONNECTION USER XDG_*`. **No `BASH_ENV`, no `ENV`, no `LD_*`** |
| Initial cwd | `/home/gatea` |
| Descriptors | exactly 0/1/2, all pipes to the SSH channel; no other inherited descriptor |
| Mutation-denial control | **none exists today** — this is the one genuine gap the design must still close |

Also relevant to the design: `sshd` has `permitrootlogin no`,
`passwordauthentication no`, `pubkeyauthentication yes`, `permituserrc yes`
(the open account-shell boundary the transport records describe). Kernel
6.8.0-137 on Ubuntu 24.04.4 LTS with **Landlock up and running**, plus
AppArmor, lockdown, yama, integrity — so the enforcement primitives the channel
design depends on are present.

## What this does and does not establish

**Does:** the deployment pattern works on Ubuntu 24.04 and ran stably; root is
obtainable, clearing residual 4 of the channel design; the kernel supports the
proposed enforcement; the recorded address and sudo scope in the repository are
both stale.

**Does not:** this is `GATEA-STAGING`, not the Hostinger KVM2 target. The run
was DISARMED and TESTNET. Candidate `2ce41e34` is the Gate-A staging candidate,
accepted for staging only, and its acceptance does not transfer to a current
candidate. Nothing here closes a gate, accepts an artifact, or authorizes a
KVM2 deployment.

## Actions taken and their reversal

1. `CheckpointType` on the GATEA-STAGING VM object changed `Disabled` →
   `Standard`, and checkpoint `GATEA-STAGING-CH1-PRECHANGE-V1`
   (`fac77a2c-8af9-4bba-83c3-b280b9b5893a`, 10:14:32) created **before** the VM
   was started. Protective and reversible; the checkpoint is retained.
2. VM started, observed read-only over SSH, then stopped cleanly. Final state
   `Off`.
3. **No guest file, package, service, account, or configuration was modified.**
   Only reads and `sudo -n` reads. No key content was read, printed, hashed,
   copied, replaced, or rotated; the identity was used only as an `-i` path.
   Public-key bodies in `authorized_keys` were redacted before display.
4. Sibling VM `KVM2-Ubuntu-2404-Staging` was never addressed and remains `Off`.
   No Hostinger, production, broker, exchange, ARM, order, mainnet, trading, or
   merge action occurred.
