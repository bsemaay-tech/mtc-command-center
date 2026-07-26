# Exact-SHA staging matrix specification

- Status: specification prepared; **not executed**
- Active KVM2 is forbidden as a staging host
- P3-01 policy: owner choice OPEN; matrix is written for recommended WAL
  migration but is not owner-approved

Every run binds one committed source SHA, payload-manifest SHA-256, lock hash,
unit hashes, state-tool hash, and test-tree hash. A failure stops the matrix;
rerun requires a new recorded attempt. Local and Ubuntu artifacts are separate
and hash-recorded.

## Matrix A — local, non-runtime

| Case | Pass condition |
|---|---|
| Python syntax/compile | Changed Python files compile |
| Shell syntax/static | Every deployment shell file passes available non-starting checks |
| Lock structure | Direct inputs match `requirements.txt`; every transitive entry exact and hashed; no URL/VCS/index override |
| App state path | Default remains unchanged; env override works; CLI wins; empty/relative values fail |
| Units | First unit masked design, no `[Install]`, `Restart=no`; steady unit separate/inert; both exact-SHA, hardened, `PrivateTmp=yes` |
| Installer | Exact SHA plus payload-manifest hash required; clean binary-wheel venv; no start/enable/unmask/UFW mutation/secret definition |
| Verifier/rollback | Exact hashes, immutable inventory, no auto-start; rollback preserves state and proves no local bridge process/listener |
| WAL happy path | Hot-WAL source captures to one file; integrity/foreign keys/invariants/hashes pass |
| WAL failures | Drift, corruption, sidecar, tamper, path injection, malformed manifest/hash, missing schema, and partial backup fail closed |
| Ledger | Canonical row artifact hash plus three row fixtures validate; all synthetic invalid cases reject |
| Full bridge suite | Pass from repository root and from `IBKR_PAPER_BRIDGE` |
| Scope | Git diff/status contains whitelist only; protected-scope diff zero; `git diff --check` passes |

## Matrix B — named expendable Ubuntu 24.04

The environment class must be named and recorded before execution (Hyper-V,
VirtualBox, QEMU, or separately authorized scratch VPS). Required cases:

1. verify OS/image provenance and exact Python 3.12 package source;
2. build an external payload from a clean exact-SHA checkout;
3. record `RELEASE_SHA256SUMS` SHA-256;
4. run installer dry-run with exact SHA/hash;
5. run exactly one disposable install with service remaining masked, disabled,
   inactive, and secret-free;
6. prove per-SHA venv installs only locked binary wheels and exact versions;
7. verify users, groups, paths, ownership, modes, no symlinks, immutable trees;
8. verify rendered first-start unit hash/hardening and steady unit absence;
9. verify UFW SSH-only assertion and no non-loopback listener without changing
   firewall state;
10. run structural/full bridge tests without starting the service;
11. create/verify WAL bundles for normal, hot-WAL, corruption, drift, missing
    schema, sidecar, and tamper cases;
12. test idempotent re-verification and fail-closed mismatched SHA/hash/identity/
    path/env cases;
13. verify rollback in a disposable stopped setup, with state preserved and no
    local process/listener;
14. remove the disposable environment or record teardown evidence.

The following are deliberately excluded: active KVM2, broker/exchange calls,
secret provisioning, service first start, cutover, ARM, firewall mutation, and
mainnet.

## P3-01 adversarial state scenarios

- WAL-resident committed rows survive.
- Daily realized loss and consecutive-loss streak remain equal.
- Open local trades and live owned-order counts remain equal.
- Corrupt DB, missing bridge schema, foreign-key failure, hash mismatch,
  manifest traversal/private identifier, unknown state, and source drift block.
- Exchange-side foreign positions/orders are explicitly separate owner-run raw
  checks; SQLite success cannot satisfy them.

Owner acceptance of this staging specification remains OPEN.
