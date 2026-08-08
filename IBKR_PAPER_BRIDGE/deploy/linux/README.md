# Linux deployment assets — MTC Crypto Paper Bridge (Hyperliquid TESTNET)

- Date added: 2026-07-26
- Status: **PREPARATION ONLY — nothing here has been executed on any host.**
- Authority: none. These files are inert artifacts. Running any of them
  requires the separate owner authorizations named below.

This directory replaces the obsolete global-pip / root-systemd VPS recipe that
used to live in `../../docs/17_DEPLOYMENT.md` §3. That recipe is exactly what
blocking findings 2 and 3 of
`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`
rejected: unpinned global `pip install`, a root-run service with no privilege
separation, no restart throttling, no explicit state/log ownership.

## Contents

| Path | Purpose |
|---|---|
| `package.sh` | Build the immutable payload for one exact SHA on a trusted build host (`git archive` + `RELEASE_SHA` + `RELEASE_SHA256SUMS`). Never runs on the VPS. |
| `install.sh` | One bounded, non-interactive, fail-closed install. Never starts, enables, arms, provisions a secret, or touches the firewall. |
| `verify.sh` | Read-only assertion pass over an installed release. Changes nothing. |
| `rollback.sh` | Stop + mask + optionally re-bind to a prior installed SHA. Never starts, never deletes state. |
| `verify_lock.py` | Offline parser for exact+hashed lock entries and exact installed distribution versions. |
| `lib/common.sh` | Shared layout constants and fail-closed assertions (including the read-only UFW SSH-only check). |
| `systemd/mtc-bridge-first-start.service.template` | The only unit `install.sh` installs. `Restart=no`, no `[Install]` section, installed masked. |
| `systemd/mtc-bridge-steady.service.template` | Restart-enabled profile. **Gated artifact — never installed or enabled by any script here.** |
| `env/mtc-bridge.env.template` | Secret-name-only contract for the root-owned `0600` env file. Contains no values and never will. |
| `logrotate/mtc-bridge` | Frozen persistent-log rotation policy. |
| `COMMANDS.md` | The exact command sequence for a later, separately authorized one-attempt install. |

## Target layout

```
/opt/mtc-bridge/releases/<exact-40-hex-sha>/   root:root, dirs 0555, files 0444/0555
                                   ├── IBKR_PAPER_BRIDGE/...   exact exported tree
                                   ├── RELEASE_SHA
                                   └── RELEASE_SHA256SUMS
/opt/mtc-bridge/venvs/<exact-40-hex-sha>/      root:root, read-only
                                   └── Python 3.12, exact hash-locked distributions
/var/lib/mtc-bridge/                mtc-bridge:mtc-bridge 0750   bridge.db (WAL)
/var/log/mtc-bridge/                mtc-bridge:mtc-bridge 0750   bridge.log, bridge.err.log
/etc/mtc-bridge/                    root:root 0750
        ├── mtc-bridge.env          root:root 0600   names only until KVM2-P4-03
        ├── install_manifest.json   root:root 0640
        └── rollback_manifest.json  root:root 0640
/usr/local/lib/systemd/system/mtc-bridge-first-start.service   the real unit
/etc/systemd/system/mtc-bridge-first-start.service -> /dev/null  the mask
/etc/logrotate.d/mtc-bridge
```

The release path contains the exact commit SHA and the unit hard-codes that
path, so the running service can never silently follow a mutable `current`
symlink to a different build.

## Design decisions worth knowing before reviewing

**Reproducible Python.** `requirements.txt` is untouched (it is still the file
the TS-P0-001 runtime-baseline source scope hashes). `requirements.in` mirrors
its direct entries; `requirements.lock` is the fully pinned, fully hashed
transitive closure resolved for CPython 3.12 on Linux. `install.sh` installs
only the lock, with `--require-hashes --no-deps --only-binary=:all:`, into a
per-SHA venv outside the exact payload tree. A local verifier proves every lock
entry is exact+hashed and the installed distribution set equals the lock.
There is no global `pip install`, source build/build-isolation dependency,
floating specifier, mutable branch or
`pip install --upgrade pip` (that would itself be an unpinned network install).
`--wheelhouse <dir>` makes the install fully offline; binary-wheel-only is
mandatory in both online and offline modes.

**Two hashes bind the payload.** `--release-sha` must equal the 40-hex
`RELEASE_SHA` marker and `--manifest-sha256` must equal the separately recorded
SHA-256 of `RELEASE_SHA256SUMS`. Every listed file hash is verified, and the
file inventory must match the manifest exactly—no missing or injected file.
The installer must itself be the hash-bound payload copy and must be invoked as
`sudo bash <PAYLOAD>/IBKR_PAPER_BRIDGE/deploy/linux/install.sh ...`; a detached
checkout copy is rejected before any target-host mutation. All helpers and
templates consumed by the installer come from that same accepted payload tree.

**Masked, not merely disabled.** The first-start unit has no `[Install]`
section, so `systemctl enable` is structurally impossible, and it is installed
masked, so `systemctl start` fails until someone explicitly unmasks it. Two
independent barriers, both requiring a deliberate human action recorded under
KVM2-P4-06.

**`Restart=no` is a safety property, not an oversight.** An automatic restart
of a trading bridge can re-enter the market with unknown risk state. The steady
restart-enabled profile stays a separate, separately hashed artifact until the
fault-injection matrix (crash/kill/reboot) proves DISARMED startup, reconcile
gating, state continuity, duplicate prevention and throttling — and until fresh
Gate 5/Gate 6 accept that specific profile.

**Loopback only, and the firewall is never touched.** The application binds
`127.0.0.1:8790` in code; `install.sh` and `verify.sh` assert that statically
and also assert no non-loopback listener exists on that port. UFW is only ever
*read*: any inbound rule other than SSH fails the check. Adding, removing or
changing a firewall rule is a separately scoped, separately audited,
owner-approved action.

**Secrets are contract-only here.** `install.sh` creates
`/etc/mtc-bridge/mtc-bridge.env` from a comment-only template at `0600`
`root:root` and never writes a value into it. If the file already exists it is
not read and not modified — only its mode and ownership are re-asserted.
`HL_LIVE_ACK` must be absent from the file, the unit and the process
environment; `install.sh` refuses to run if it is set in the invoking shell and
`verify.sh` fails if it appears in the env file.

**State lives outside the release.** The unit sets
`MTC_BRIDGE_STATE_DB=/var/lib/mtc-bridge/bridge.db`, consumed by the
`--state-db` / `MTC_BRIDGE_STATE_DB` plumbing in `bridge/app.py`. With no
override set, the application keeps its existing in-repo default unchanged.

**Start mode is unit-owned, not env-owned.** The first-start unit pins
`MTC_BRIDGE_START_MODE=credential_free_disarmed` via `Environment=`. Defining
`MTC_BRIDGE_START_MODE` in `/etc/mtc-bridge/mtc-bridge.env` would let the env
file override that hashed, accepted DISARMED mode, so `verify.sh` rejects any
`MTC_BRIDGE_START_MODE=` assignment — bare or `export` — found in the env file.

**Rollback preserves evidence.** `rollback.sh` stops and masks the service and
never deletes, moves or resets `/var/lib/mtc-bridge`. Risk history is evidence.

## Known limitations, recorded honestly

- These assets have **never been executed**, on KVM2 or anywhere else. No
  Ubuntu run, no `install.sh` invocation, no `systemctl` call has happened.
  Test coverage in `tests/test_linux_deployment.py` is structural only.
- `requirements.lock` was resolved from package-index metadata for
  `--python-version 3.12 --python-platform linux`. Resolution is not the same as
  a successful install; the Ubuntu install itself remains
  `BLOCKED/UNVERIFIED` at KVM2-P3-03.
- Egress is unrestricted (`RestrictAddressFamilies` limits families, not
  destinations). The bridge needs outbound HTTPS to the exchange. Per-destination
  egress control is deferred to the Phase 6 network gate.
- `MemoryDenyWriteExecute` is deliberately not set: several locked
  cryptographic wheels map W+X pages at import time.
- Same-host isolation is **not** solved by this directory. A loopback listener
  is reachable by any local process; that is the KVM2-P5-10 design problem, and
  AI-lab admission stays BLOCKED until it is solved and accepted.

## Gate order (none of which this directory grants)

1. KVM2-P4-01 — owner authorizes installation and configuration only.
2. KVM2-P4-02 — exactly one bounded `install.sh` attempt; service stays masked.
3. KVM2-P4-03 — owner separately authorizes TESTNET-only secret provisioning.
4. KVM2-P4-04 tabletop → P4-04A quiesce → P4-05 ordered single-writer cutover
   (including the WAL-consistent state capture proved with
   `tools/wal_state_bundle.py`).
5. KVM2-P4-06 — owner authorizes exactly one first DISARMED start;
   KVM2-P4-07 executes it once (`systemctl unmask` then `systemctl start`).
6. KVM2-P4-08 — rollback proof. KVM2-P4-08A/B — any recovery start.
7. KVM2-P5-05/P5-05A — ARM, separately, once, never implied by any of the above.
