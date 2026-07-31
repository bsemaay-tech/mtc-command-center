# Profile: temporary-testnet-lab

- Status: definition only; no host was changed
- Trading mode: Hyperliquid TESTNET only
- Bridge priority: mandatory; laboratory admission optional and later

## Required bridge baseline

- Ubuntu 24.04.x LTS Server from a verified official or documented provider
  image.
- Python 3.12 plus the OS venv package; no global application pip install.
- Dedicated non-login `mtc-bridge` identity with no sudo or privileged groups.
- Immutable exact-SHA code and per-SHA venv under `/opt/mtc-bridge/`.
- Writable state only under `/var/lib/mtc-bridge`; logs only under
  `/var/log/mtc-bridge`; root-owned `0600` environment contract.
- Control listener only on `127.0.0.1:8790`; inbound firewall remains SSH-only.
- First-start unit is masked, disabled, `Restart=no`, and never automatically
  installed into boot targets.

## Optional laboratory layer

No lab identity, package, service, credential, listener, browser, scheduler,
container runtime, or agent is part of this executable batch. Each remains
forbidden until bridge stabilization, measured admission limits, OS-enforced
same-host control-plane isolation, denial tests, fresh security acceptance, and
a separate one-workload owner authorization are complete.

## Forbidden

Mainnet, public bridge endpoints, reverse proxying port 8790, Docker socket
access, self-hosted workflow runners, heavy backtests, local large models,
mutable-branch deployment, automatic pulls/deploys, shared bridge/lab secrets,
and restoring a laboratory image into a future trading host.
