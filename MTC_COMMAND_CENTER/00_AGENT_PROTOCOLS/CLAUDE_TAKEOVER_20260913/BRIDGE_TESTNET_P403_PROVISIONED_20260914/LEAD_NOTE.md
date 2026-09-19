# KVM2-P4-03 — TESTNET secret provisioning DONE by the owner's hands; Lead read-only post-conditions — 2026-09-14

Owner chat 13:4xZ, verbatim: **`provisioned`** (after the button launcher fix `BRIDGE_TESTNET_BUTTON_FIX_20260914/`). Authorization: `OD-20260914-BRIDGE-TESTNET-GO-1` (KVM2-P4-03 by the owner's hands; ARM excluded).

## Post-conditions (Lead, SSH as `baris` with the pinned key/known_hosts, `sudo -n`, READ-ONLY; script `kvm2_postcond_p403.sh.txt`, output `kvm2_postcond_p403_OUTPUT.txt`; values never read or printed)
| Check | Expected | Observed 13:47Z |
|---|---|---|
| `/etc/mtc-bridge/mtc-bridge.env` mode/owner | 600 root:root | **600 root:root** |
| env file mtime | after the owner's run | 2026-09-14 13:44:19 UTC |
| `^HL_LIVE_ACK=` lines | 0 | **0** |
| `^HL_ACCOUNT_ADDRESS=0x[40 hex]$` lines | 1 | **1** |
| `^HL_API_WALLET_KEY=0x[64 hex]$` lines | 1 | **1** |
| uncommented key names | only the two | `HL_ACCOUNT_ADDRESS,HL_API_WALLET_KEY` (44 lines = 42 template comments + 2 values) |
| wizard temp copy `/tmp/testnet_provision_wizard.sh` | removed | removed |
| `mtc-bridge-first-start.service` | untouched | active, NRestarts 0, listener 127.0.0.1:8790 only |
| `/api/status` | unchanged | `DISARMED`, `credential_free_disarmed`, network/exchange disabled, `credential_lookup: disabled`, `arm_enabled: false`, release `be007fd802bbfd2eb181d66038c374865d1562ee`, service start 2026-09-12T06:20:44Z |
| `install_manifest.json` | install-time record | still `secrets_provisioned: false`, `env_file_populated: false`, `first_start_unit_state: masked`, `service_started: false` (written 2026-08-17 by `install.sh`; not updated by the wizard nor by the 09-12 start — an install-time snapshot, not live state) |

**Verdict: KVM2-P4-03 satisfied** (the wizard's own four post-conditions reproduced from outside). Nothing else changed on the host.

## What the next step is NOT (checked in the accepted release be007fd8 before asking the owner)
- There is no "credential-mode restart" of the running unit: `mtc-bridge-first-start.service` pins `Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed` in its hashed unit (`deploy/linux/systemd/mtc-bridge-first-start.service.template:42`; README "Start mode is unit-owned, not env-owned"); `verify.sh` rejects any `MTC_BRIDGE_START_MODE=` in the env file. Restarting it would re-enter credential-free mode; the provisioned values would stay unused.
- The only credential-consuming unit is the steady profile (`mtc-bridge-steady.service.template`), a GATED artifact: admission needs the KVM2-P2-04 fault-injection matrix, fresh Gate 5/6 acceptance of that profile and a new P5-03A baseline hash. Not an owner sentence — engineering + review.
- The documented owner-approvable next step is the standalone testnet smoke `tools/smoke_p0.py` (`docs/06_HYPERLIQUID_SETUP.md` section 5: "the agent runs this only with your explicit in-session approval — it is an exchange action (testnet/fake money)"). Feasibility verified read-only (`kvm2_smoke_feasibility_OUTPUT.txt`): release tree `555 root:root`, venv Python 3.12.3 imports `hyperliquid`, `eth_account 0.13.7`, `bridge.settings`, `bridge.broker.hyperliquid`, `bridge.engine.types`; `api.hyperliquid-testnet.xyz` resolves; `/tmp` 93 GB free; `tools/smoke_p0.py` on the host sha256 `52d03a81…` == the accepted blob at be007fd8.
- Smoke plan if the owner says GO: byte-identical copy of the release tree to a writable scratch dir on KVM2 (the tool writes `docs/p0_smoke_log.json` under its own tree and the release tree is read-only), run once as the `mtc-bridge` user with the two values passed only through the process environment from the root-owned file (never echoed), leverage 1, one resting LONG BTC limit at 90 % of market (~$11.5 notional, cannot fill), native SL trigger, modify, cancel, flatten only if a position changed, guaranteed cleanup; the bridge service is not touched; the log is copied back with the account address redacted before it enters the repository.
