# Work item (scoping only): letting the KVM2 Bridge SERVICE use the provisioned TESTNET credentials — 2026-09-14

Status: **PROPOSAL / scoping note. Nothing authorized, built or executed.** Written by the Lead after KVM2-P4-03 (`OD-20260914-BRIDGE-P403-PROVISIONED-1`) because the owner asked what "the next real step" for the Bridge is; the earlier phrase "DISARMED credential-mode restart" was wrong and is corrected here.

## Facts (release `be007fd8`, verified in bytes)
- `bridge/app.py:31-33` defines two start modes: `credentialed` (default when `MTC_BRIDGE_START_MODE` is unset — builds the broker with the env credentials; the app still starts DISARMED, `app_state` DISARMED unless KILLED) and `credential_free_disarmed` (no broker, `credential_lookup: disabled`).
- The ONLY installed unit, `mtc-bridge-first-start.service`, pins `Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed` (`deploy/linux/systemd/mtc-bridge-first-start.service.template:42`); `verify.sh` rejects any `MTC_BRIDGE_START_MODE=` in the env file (README "Start mode is unit-owned, not env-owned"). Restarting it keeps credential-free mode; the KVM2-P4-03 values stay unused.
- The steady profile (`mtc-bridge-steady.service.template`) is the restart-enabled profile, gated: never installed by `install.sh`, `verify.sh` fails if present; admission needs the fault-injection matrix (crash/kill/reboot proving DISARMED startup, reconcile gating, state continuity, duplicate prevention, restart throttling), fresh Gate 5/Gate 6 acceptance of THAT profile, and a new KVM2-P5-03A baseline hash (template header lines 12-17; README lines 86-90). Note: README calls the matrix "KVM2-P2-04" while `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:119` uses P2-04 for network/service blueprints — the identifier needs reconciling in the plan before anyone cites it.
- Today's P012 evidence path did NOT need the service: the standalone smoke (`OD-20260914-BRIDGE-SMOKE-GO-1`) and Path 1 (owner's own trades + read-only capture) produced venue evidence with the service untouched.

## Options for the owner (later; no answer needed now)
| Option | What it is | Engineering | Reviews | When it matters |
|---|---|---|---|---|
| **C — stay credential-free (default, recommended for now)** | keep the service as is; venue evidence via standalone tools and Path 1 | none | none | until the Bridge itself must trade on testnet |
| **A — credentialed DISARMED first-start variant** | a second hashed unit (Restart=no, `MTC_BRIDGE_START_MODE=credentialed`, testnet) + `install.sh`/`verify.sh` support for it + one bounded start attempt (P4-06/P4-07 analogue) + `/api/status` and reconcile evidence | 1-2 builder lanes (Bridge tree, T0 host surface) | full T0 roster (exact Opus + Sol + Gemini + Lead); Opus after the Pro reset | first step toward the Bridge trading on testnet (P5 ARM chain) |
| **B — steady-profile admission** | the operational restart-enabled profile | fault-injection matrix + baseline hash | Gate 5 + Gate 6 + P5-03A | required before Phase 6 regardless of A |

Nothing here grants ARM, mainnet or live authority. If the owner wants A, the Lead writes the builder brief and the roster plan as a separate owner-decision packet.
