# Identity and filesystem boundary

## Bridge identity

`mtc-bridge` is a dedicated system account with primary group `mtc-bridge`,
home `/var/lib/mtc-bridge`, and a non-login shell. It has no sudo, admin,
Docker, journal-reader, or other privileged supplementary group. An existing
identity with different attributes causes the installer to stop.

## Filesystem matrix

| Path | Owner | Mode | Purpose |
|---|---|---:|---|
| `/opt/mtc-bridge/releases/<exact-sha>` | root:root | dirs 0555; files 0444/0555 | Exact payload/code only |
| `/opt/mtc-bridge/venvs/<exact-sha>` | root:root | dirs/files read-only | Exact Python 3.12 environment |
| `/var/lib/mtc-bridge` | mtc-bridge:mtc-bridge | 0750 | SQLite state/WAL |
| `/var/log/mtc-bridge` | mtc-bridge:mtc-bridge | 0750 | Persistent rotated logs |
| `/etc/mtc-bridge` | root:root | 0750 | Hash manifests and env contract |
| `/etc/mtc-bridge/mtc-bridge.env` | root:root | 0600 | Secret names/values only after P4-03 |
| Installed unit | root:root | 0644 | Exact-SHA service definition |
| Logrotate policy | root:root | 0644 | Frozen retention policy |

Canonical paths must not be symlinks. The release inventory must match
`RELEASE_SHA256SUMS` exactly, with no injected file, and the payload manifest
itself must match an externally accepted SHA-256. The venv distribution set
must equal the fully hashed lock apart from OS-provided venv bootstrap tools.

The unit uses `ProtectSystem=strict`; only the state and log directories are
writable. `PrivateTmp=yes`, `ProtectHome=yes`, `ProtectProc=invisible`,
`NoNewPrivileges=yes`, an empty capability set, and a restrictive system-call
profile reduce the service surface.

## Required denial checks

- Login as `mtc-bridge` is denied.
- The bridge identity cannot write release, venv, unit, config, or env paths.
- A future lab identity cannot read bridge env, state, raw logs, unit control,
  or release-private material.
- No lab identity or child process exists in the current batch; Phase 6 remains
  blocked.
