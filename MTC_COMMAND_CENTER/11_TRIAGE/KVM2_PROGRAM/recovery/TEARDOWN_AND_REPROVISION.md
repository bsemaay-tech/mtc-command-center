# Teardown and destructive-reprovision manifest

## Inventory to remove before a future clean trading build

Every admitted lab service, user/group, package, repository, scheduler, timer,
unit, output directory, credential name, network rule, namespace, container
artifact, browser profile, cache, and monitoring extension must be enumerated.
Absence must be proved after destructive reprovision; uninstalling is not clean
proof.

## Export allowlist

Only owner-reviewed sanitized reports and separately verified bridge release,
configuration, and WAL-consistent state artifacts may be exported. Secret
values are reissued/rotated, not copied through ordinary backup.

## Never restore into trading-only

The lab OS image or snapshot, lab home, agent workspace, cached credential,
package environment, container storage, browser data, scheduled task, lab log,
or lab backup.

Option A requires one separately authorized wipe/bootstrap/restore packet.
Option B requires one separately authorized purchase/provision/restore packet.
Either route needs trusted-image provenance, new host/boot/filesystem evidence,
rotated credentials, verified-only restore, no-lab proof, rollback, and fresh
independent post-build acceptance before any final mainnet decision.
