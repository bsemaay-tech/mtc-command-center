# WP-L Phase 2 — Stage 3B immutable re-preregistration (R4-5 only)

Status at writing: **PREREGISTERED — no R45B remote invocation has occurred**

Unit: `WPLP2-20260809T125940Z-8dc78f08` · branch `feature/donchian-crypto-ladder`
Lead session (Claude Fable 5), 2026-08-09 evening.

## Why this document exists

Stage 3's first-FAIL (B3 STOP at op 05, see `../03_TRANSPORT/B3_STOP_ADJUDICATION.md`)
skipped op 07 before R4-5 ran. The skip was collateral sequencing, not an R4-5 defect;
owner authorization for tonight explicitly covered R4-5 execution. Per Stage 2
PREREGISTRATION.md §11, a retry requires a **new** preregistration with a fresh one-use
RUNID — this is that document. Both Stage 2 RUNIDs (`…-B3`, `…-R45`) are burned and are
not reused here.

Writing this document is the RP0 §1.2 preregistration for exactly one stage: R4-5.
B3 is NOT re-preregistered (blocked on `B3-GAP-ENV`, owner decision pending). C1, C2,
C3, C4, C5 remain BLOCKED and are not touched.

## 1. Run identifiers and evidence tree

| Field | Value |
|---|---|
| `RUNID` | `WPLP2-20260809T125940Z-8dc78f08-R45B` (one-use; burned on any allocation failure) |
| `EV_STAGE_ID` | `r45b` |
| `EV_DIR` | `/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08/evidence/runkit/WPLP2-20260809T125940Z-8dc78f08-R45B` |
| `EV_LOG` | `<EV_DIR>/r45b.log` |

`REMOTE_BASE`, `EV_PARENT`, `EV_RUNKIT` (all `gatea:gatea 0700`) are the Stage 3 op-01
allocations, unchanged and re-asserted at run time by the accepted RP0 bootstrap. The
evidence leaf itself is create-once: it does not exist before this run and the bootstrap
refuses an existing leaf.

## 2. Remote artifacts consumed — every one hash-gated at run time

Already on the host from Stage 3 ops 02–04 (`EXTRACT PASS members=9 verified=9
executed=0`). Nothing is trusted from that residue: `run_r45b.sh` refuses symlinks and
re-verifies each byte-for-byte before sourcing or executing anything:

| Remote path | Pinned SHA-256 |
|---|---|
| `kit/extracted/RP0-LIB.sh` | `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48` |
| `kit/extracted/RP0-BOOTSTRAP.sh` | `e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33` |
| `kit/extracted/RP4-C3.py` | `0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5` |
| `R4_5_runner.py` | `8519e2bfc9bf2105bbb8e8c33fa4f271aa8852c7d7b18ad10286e19deddf68d5` |

No new upload is performed: a hash-verified byte set is the same object however it
arrived, and re-transferring it would add an op without adding assurance.

## 3. Operator-side artifacts (every executed file pinned)

| File | SHA-256 | Role |
|---|---|---|
| `run_r45b.sh` | `70d90d3d074e22c409284409e327c5dc7846100f68ec1ab6a319ea1f7fb69670` | op 01 stdin — R4-5 wrapper. Differs from the accepted `run_r45.sh` (`4b9e5e68…`) by exactly three lines: header label, `RUNID` (`…-R45B`), `EV_STAGE_ID` (`r45b`). Diff verified; `bash -n` clean. |
| `remote_close_tree.sh` | `87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e` | op 02 stdin — byte-identical to the Stage 2 accepted script |
| `TRANSPORT_PLAN.tsv` | `48acbea8eefe7c7f5659a5819725d767f3fd84b1c0cad6af215bae35f35de716` | the 4-op list; pinned inside the runner |
| `transport_runner.ps1` | `a48ddc93ace627630b5c95e578799d60e56ae8aaaf75e35660a682234c841b9b` | operator-side recorder. Differs from the Stage 2 accepted runner (`c5bdb47c…`) only in its pinned constants: header label, confirm token, `PREREG_DIR`, `RECORD_ROOT`, `PLAN_SHA256`, and `PINNED_FILES` emptied (this plan transfers no file by name). Execution logic byte-identical. |

## 4. Exact remote argv

Route, identity and the four fail-closed ssh options are **unchanged** from Stage 2
PREREGISTRATION.md §5 (`gatea@172.24.55.233`, `BatchMode=yes`,
`StrictHostKeyChecking=yes`, `IdentitiesOnly=yes`, `ConnectTimeout=20`).

| op | run_when | kind | remote/local argv after the pinned options |
|---|---|---|---|
| 01 | sequence_ok | ssh stdin `run_r45b.sh` | `gatea@172.24.55.233 bash -s --` |
| 02 | **always** | ssh stdin `remote_close_tree.sh` | `gatea@172.24.55.233 bash -s -- <EV_DIR> WPLP2-20260809T125940Z-8dc78f08-R45B` |
| 03 | **always** | scp down | `-r gatea@172.24.55.233:<EV_DIR> .` (cwd `<record>\evidence`) |
| 04 | **always** | local only | `local_bind 02 03 evidence\WPLP2-20260809T125940Z-8dc78f08-R45B` — no host contact |

Every op preregisters `expect_rc = 0`; first-FAIL stopping and the always-ops evidence
discipline are inherited unchanged from the Stage 2 runner logic.

Record root, **create-once**:
`C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08-R45B`. Execution
requires both `-Execute` and `-Confirm WPLP2-20260809T125940Z-8dc78f08-R45B-EXECUTE`.

## 5. Preregistered expectations (identical claims to Stage 2 §8 #6–#7)

| # | Predicted outcome if the guard design holds | Exact predicted first divergence if it does not |
|---|---|---|
| 1 | RED arm (guard deleted): restore follows the dangling symlink and writes a real SQLite DB outside the restore root | `R45_FAIL reason=red_arm_raised_Fail: …` |
| 2 | GREEN arm (accepted bytes): raises exactly `restore destination is a symlink: <path>` and leaves the target absent | `R45_FAIL reason=green_arm_returned_without_Fail` or `green_message_differs …` |

Scope unchanged and preregistered: this is a D026 Arm-1 falsification of the two-line
`dst_path.is_symlink()` `Fail` guard inside `RP4-C3 restore_into` — **not** a C3 run.
No bundle verification, no candidate release tree import. C3 stays BLOCKED. rc contract:
0 = both arms as predicted, 1 = an arm contradicted, 3 = could not evaluate; any rc 3 is
never re-read as a PASS.

## 6. Immutability and safety

Void — requiring a fresh preregistration with a new RUNID — if any hash above, the
route/identity/ssh options, any §1 path, or the RUNID changes. No retry pool exists.

No mutating step of any kind is preregistered: no service/unit/credential/ARM/broker/
TESTNET/mainnet action, no chmod/chown outside the run's create-once evidence leaf, no
master merge. Git sequencing stays with the Lead. At the moment of writing, R45B remote
invocation count: **0**.
