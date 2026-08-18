# P2-09 reproducibility rehearsal summary

- Verdict: **BLOCKED / UNVERIFIED**
- Date: 2026-07-26
- Executor: Codex Lead, local staging preparation only
- Independent verifier: not assigned
- Active KVM2 used: no

The intended environment is one disposable Ubuntu 24.04 Hyper-V VM on the
local Windows host. Inventory found Windows 11 Pro, 31.7 GiB RAM, and
282.1 GiB free on `C:`. Hyper-V is now enabled, with Windows reporting that one
restart is required. A Canonical released Ubuntu 24.04 Azure VHD was selected,
a key-only NoCloud seed was generated, and an elevated SYSTEM startup task was
registered to resume the official download, require its exact published
SHA-256, inspect its archive paths, and only then create, start, and validate
the VM after that restart. No restart, VM, switch, disk conversion, or Linux
execution has occurred yet.

No Ubuntu environment was used; no OS image provenance, installation, package
manifest, service/unit behavior, or rebuild idempotence was evidenced on
Linux. This record cannot be cited as reproducibility proof.
