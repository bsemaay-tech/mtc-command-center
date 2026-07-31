# Profile: future-trading-only

- Status: future definition only
- Entry condition: destructive trusted reprovision of KVM2 or a separately
  clean trading VPS, followed by fresh post-build acceptance

This profile contains only the bridge, minimal host security/monitoring,
encrypted recovery tooling, and owner access recovery. It inherits the
immutable release, Python 3.12 hash-lock, identity, filesystem, loopback,
firewall, secret, state, backup, maintenance, and incident contracts.

It must contain no lab user, lab home, agent, coding runner, browser automation,
container engine/storage, self-hosted workflow runner, lab scheduler, lab
credential, cached lab data, lab package state, or lab snapshot. Only verified
release/config/state artifacts on the restore allowlist may cross into this
profile. All bridge and monitoring credentials are reissued or rotated before
use.

Mainnet remains forbidden until the bounded clean-host build completes, an
independent post-build Gate 5/Gate 6 accepts the resulting host, and the owner
gives a separate explicit final mainnet authorization.
