# Network and service blueprint

## Network contract

- Application bind: `127.0.0.1:8790` only.
- Operator access: later owner-authorized SSH tunnel only.
- Inbound firewall: active, default-deny, SSH-only.
- Installer/verifier behavior: read-only UFW assertions; no firewall mutation.
- Port 8790: never public, proxied, or added to an inbound rule.
- Same-host loopback isolation: not solved by loopback alone; lab admission is
  blocked on the separate OS-enforced design and denial suite.

## Service profiles

`mtc-bridge-first-start.service` is the only installer-delivered unit. It has no
`[Install]` section, is installed masked, is never started/enabled by the
installer, uses `Restart=no`, and binds one exact release/venv SHA.

`mtc-bridge-steady.service` is a separate inert template with bounded
`Restart=on-failure`. No script installs or enables it. It cannot be admitted
until crash/kill/reboot tests prove DISARMED startup, reconciliation gating,
state continuity, duplicate prevention, and throttling; fresh security/quality
acceptance and a new service-profile baseline hash remain required.

Both templates include graceful SIGTERM stop, 45-second stop timeout,
`StartLimitIntervalSec`, `StartLimitBurst`, `RestartSec`, persistent stdout/
stderr files, `PrivateTmp=yes`, and the hardening in the identity contract.

## Logs

Daily rotation retains 30 generations, rotates early at 64 MiB, compresses with
one-generation delay, uses `copytruncate`, and recreates files at
`0640 mtc-bridge:mtc-bridge`. The forced-rotation test is specified for the
later first-start matrix and has not been run.
