# Gate A — Post-Gate Transition Inventory Checkpoint (2026-08-09)

> **Routing:** Tier 4 protected post-Gate evidence checkpoint · Model GLM-5.2 via Z.AI Coding Plan
> (owner-requested exact model; evidence protected). **Worker scope:** GLM-5.2 only edited the four
> task-named files and recorded this checkpoint. It ran **no** SSH, Gate-A script, scan, sudo, service,
> package, Git, staging-mutation, credential-read, broker/exchange, ARM, order, TESTNET/mainnet,
> master-merge, or network command. The read-only inventory it records was an authorized discovery unit
> whose captured artifacts are referenced below by path/size/hash; GLM-5.2 recorded rather than performed
> it, and did not mutate staging or read any secret value.

## Conclusion

Gate A **A-0 through A-9 PASS** remains **staging acceptance only** — evidence-backed, but it authorizes
or implies **no** ARM, credential load, broker connectivity, orders, TESTNET/mainnet, production
promotion, or master merge. The post-Gate transition inventory is **complete and read-only**. It
confirms staging is a single, clean, credential-free DISARMED install, and it records **one critical
correction** to the prior A-9 checkpoints: **the old installed release `ebada020…` and its venv are
already absent** (teardown evidence exists), so **no old-install cleanup mutation is required or
pending**. The previously-framed "THEN perform already-authorized old-install cleanup" next step is
therefore moot. The inert old payload archive is **out of scope** and **must not** be deleted.

## PICK UP EXACTLY HERE

1. **Read-only discover** the canonical post-Gate workflow, roadmap, WP-V / deployment / promotion
   gates, and whether any explicit transition authority exists. Stop and report if none is found.
2. **Do not** rerun Gate A or mutate staging during discovery.
3. **Keep** the current service credential-free DISARMED.
4. **Do not delete** the inert old payload archive absent an explicit archive-cleanup scope.

---

## Observed current facts (read-only)

- Repo HEAD `5af8178b`; product candidate remains `2ce41e34bceb599d80af24c5c33d835820ec321b` (unchanged).
- **Safe staging runtime:** `mtc-bridge-first-start.service` active/running, PID `189813`, `Restart=no`,
  `NRestarts=0`; exactly one loopback listener `127.0.0.1:8790`; credential-free DISARMED
  `state_version=1`; all credential/network/exchange/ARM flags off; no credentials, broker, or orders.
- **Critical correction:** old installed release `ebada020a59edf539f60acfbb3a6bf870c8679e9` **and its
  venv are already absent**. Teardown evidence `/home/gatea/teardown-ebada020-20260808B` exists.
  **Therefore no old-install cleanup mutation is needed.**
- **Only installed release:** `/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b`
  (root, mode `555`) and venv counterpart (root, mode `555`). **No** steady or legacy `mtc-bridge` unit
  exists. **No** `current`/`previous` symlinks exist under `/opt/mtc-bridge`.
- **Current unit fragment:** `/usr/local/lib/systemd/system/mtc-bridge-first-start.service`, SHA-256
  `538c1c6038b475e87fb0e9b9c35fd4ebd8451b40ff93538f8fea5aa0b49279bd`, 3736 B, root mode `644`.
- `/etc/mtc-bridge` contains **metadata only**: `bridge.env` 2492 B, root mode `600` (**contents not
  read**) and `install_manifest.json` 1007 B, root mode `640`.
- `/var/lib/mtc-bridge` contains `bridge.db` / WAL / SHM only; `/var/log/mtc-bridge` contains
  `bridge.log` / `bridge.err`.
- **Inert old payload archive:** `/home/gatea/payload_ebada020.tar`, 1,039,774,720 B, SHA-256
  `351923f3d72cef1c928d1c54405cfbade9bf6b67b839c69d1260026bc692cbc9`. Inert — not installed or
  referenced. **Not** covered by old-install cleanup; **deletion not authorized.**
- **Current payload archive:** `/home/gatea/payload_2ce41e34.tar`, 1,047,265,280 B, SHA-256
  `d78b9e82f5f28a35a51033c5405fc1501e2c8fd4385b6d7fe012e92745b905f2`.
- **Disk:** 40.8 GB total, 16.0 GB used, 22.7 GB available.

## Install-time manifest facts (distinct from current runtime)

From `/etc/mtc-bridge/install_manifest.json` (install-time record, **not** a live read of the running
service): `env_file_populated=false`, `secrets_provisioned=false`, `firewall_modified=false`,
`steady_unit_installed=false`, `schema_version=1.0.0`; install-time `service_started=false` and
`service_enabled=false`. **Note:** the actual first-start unit **is currently running** because Gate A
started it — the install-time `started`/`enabled=false` flags are consistent (the install did not start
or enable the unit; Gate A performed the explicit start). These install-time flags are **not** evidence
of a current runtime fault.

## Local inventory evidence (captured; all .err files empty)

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `C:\WPI_ARTIFACTS\post_gate_transition_inventory_20260809.out` | 6481 | `b715363b9027479f3520ba0216bd486880e08852cdc7cb08eadf0c1f42719051` |
| `C:\WPI_ARTIFACTS\post_gate_transition_inventory_detail_20260809.out` | 1184 | `232bb01e30f61418de411342af9d762d0649480f56b2bdd723c613077fa5157b` |
| `C:\WPI_ARTIFACTS\post_gate_transition_inventory_manifest_flags_20260809.out` | 687 | `c68c75e0be47a3cab0cc71aab4f4a51395cdc68e0ec99032b02d8103413a9fea` |

## Canonical Gate-A evidence index (immutable)

| Name | Bytes | SHA-256 |
|---|---|---|
| `A0-A1 gatea-A0A1-20260808.log` | 2349 | `b8a81d77c79c1925861e16fae5aa83f639c2645b4aa28b18efb44d61f6eea5a2` |
| `A2 dryrun` | 1350 | `b3c260b570067e51265da304835f2a45dce1a9bd6616bb0cbd02ea737c7f9e7d` |
| `A2 install` | 27061 | `0376c57659ee074a81deecd831c09a8009b3b2280059f6b7cf7a3a5610f49bc1` |
| `A3 suite B` | 3907 | `569e79c7d68623b9f2ad51ee48053a04e6938e3277398861760dc1dd8d61c848` |
| `A3 postcheck C` | 738 | `56a80d53155ac73b39dac064260ff702532fad36562eafbbe75f28c2f6414878` |
| `A4 main C` | 10152 | `19ed99773ca8dbfb84bfc6a93289daf4077419dd6d46c23343f5d4cfbf007c06` |
| `A4 DB diag3` | 497 | `530f846c7fc2f4f50de6a13eecd2274726b32947082dfcbf9ffaa12baef8a5c8` |
| `A4 postdiag2` | 1111 | `ed06554cf93951921b15d378b9c2ac01f019c7c58815942cdf561e5168672183` |
| `A5 E` | 3284 | `83d947a3285a595a1df21652c8c85aa9b8e14a8a0ec2eab229f1384516fdd19c` |
| `A6 D` | 2007 | `75ed426247c2a26f6c4377f8e910826ecb4f0669565f292d538df65f2e52488c` |
| `A7 D` | 4269 | `09443b51fe01498e6530d8729b73bf2e26671b24b2a7e7b1085f8a700bbb2bf5` |
| `A8 remote D` | 1087 | `a7ef34a18145aee61196110dda6882c80992e189573003eb7fbf1119f829f0d7` |
| `A8 host local` | 321 | `abad3225fe530c00c1ef60a9cd46a0048fa1cac40135525484389d2703fee2e6` |
| `A9 D` | 876 | `23d61687ce6cbf290b134d6bd72763f7bb4be27b15daae457373d6bb004bd5e9` |

Canonical reports: `GATE_A_LOCAL_RUN_KIT_2026-08-08C.md` (A0-A3), `GATE_A_A4_PASS_2026-08-08C.md`,
`GATE_A_A5_PASS_2026-08-09E.md`, `GATE_A_A6_PASS_2026-08-09D.md`, `GATE_A_A7_PASS_2026-08-09D.md`,
`GATE_A_A8_PASS_2026-08-09D.md`, `GATE_A_A9_PASS_FINAL_2026-08-09D.md`.

## Supersedes

This checkpoint **supersedes** only the "THEN: perform already-authorized old-install cleanup" framing
carried in the A-9 final checkpoints (`GATE_A_A9_PASS_FINAL_2026-08-09D.md`,
`_AI_MEMORY/GLOBAL_HANDOFF.md`, `_AI_MEMORY/NEXT_STEPS.md`,
`11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md`). The Gate-A evidence, the A-0..A-9 PASS verdict, the
candidate identity, and the staging safety facts all **remain unchanged**; only the old-install-cleanup
step is corrected to **not required**, because that install is already gone.

## Next steps (Claude-style)

- **[AI: Any]** Read-only discovery of the canonical post-Gate workflow/roadmap and the WP-V / deployment
  / promotion gate chain. Determine whether explicit transition authority exists; if not, record a
  blocker rather than inferring it from Gate-A PASS.
- **[AI: Any]** During discovery, do **not** rerun Gate A and do **not** mutate staging; keep the service
  credential-free DISARMED.
- **[AI: Barış]** Any deletion of `/home/gatea/payload_ebada020.tar` requires an explicit, separate
  archive-cleanup scope; it is out of scope here.
- **[AI: Barış]** ARM, credential load, broker connectivity, orders, TESTNET/mainnet, production
  promotion, and master merge each require separate explicit owner authorization — Gate-A staging
  acceptance grants none of them.

## Stop conditions

- **STOP** if no explicit post-Gate transition/promotion authority is discoverable — record the blocker
  and surface to Barış; do not infer authority from Gate-A PASS.
- **STOP** if any staging mutation, Gate-A rerun, credential load, ARM, broker connectivity, order,
  TESTNET/mainnet, or master-merge action is requested without separate explicit authorization.
- **STOP** if the inventory's single-install / DISARMED / loopback-only invariant is observed to have
  drifted (more than one listener, non-loopback bind, ARM enabled, credentials present, or an unexpected
  second release) — investigate read-only and report before any further action.
