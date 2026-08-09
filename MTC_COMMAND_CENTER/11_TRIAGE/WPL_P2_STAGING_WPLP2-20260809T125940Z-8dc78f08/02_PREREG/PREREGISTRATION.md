# WP-L Phase 2 — Stage 2 immutable preregistration

Status: **PREREGISTERED — no remote invocation has occurred**

Unit: `WPLP2-20260809T125940Z-8dc78f08` · branch `feature/donchian-crypto-ladder`
Frozen candidate: `2ce41e34bceb599d80af24c5c33d835820ec321b`
Authority: `11_TRIAGE/WPL_PHASE2_DISPATCH_PROMPT_2026-08-09.md`,
`11_TRIAGE/WPL_P2_PROPOSALS_LEAD_ACCEPTANCE_2026-08-09.md`,
`11_TRIAGE/CODEX_WPL_P2_STAGING_KICKOFF_2026-08-09.md`.
Designs: `11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md` at `4c0d5fc5`.

This document satisfies the RP0 §1.2 requirement that, **before any remote
invocation**, the operator preregisters locally and immutably: the RUNID, the
evidence parent/runkit paths with expected owner and mode, the stage identifier,
and the expected SHA-256 of every proposed block the stage will carry — plus the
operator-side transport-evidence contract. Nothing here is derived at run time.

Writing this document is not an authorization to transport. **Transport is a
separate authorization** (proposals §1.2, §1.5). Section 12 states exactly what
has and has not happened.

---

## 1. Run identifiers and evidence tree

Two stages run, each with its own **one-use** RUNID. A RUNID is never reused: if
allocation fails for any reason it is **burned**, and a retry requires a new
preregistration, not a second attempt with the same identifier.

| Field | B3 stage | R4-5 stage |
|---|---|---|
| `RUNID` | `WPLP2-20260809T125940Z-8dc78f08-B3` | `WPLP2-20260809T125940Z-8dc78f08-R45` |
| `EV_STAGE_ID` | `b3` | `r45` |
| `EV_DIR` | `/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08/evidence/runkit/WPLP2-20260809T125940Z-8dc78f08-B3` | `…/evidence/runkit/WPLP2-20260809T125940Z-8dc78f08-R45` |
| `EV_LOG` | `<EV_DIR>/b3.log` | `<EV_DIR>/r45.log` |

Shared, preregistered:

| Field | Value | Expected owner | Expected mode |
|---|---|---|---|
| `REMOTE_BASE` | `/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08` | `gatea:gatea` | `0700` |
| `EV_PARENT` | `<REMOTE_BASE>/evidence` | `gatea:gatea` | `0700` |
| `EV_RUNKIT` | `<REMOTE_BASE>/evidence/runkit` | `gatea:gatea` | `0700` |
| `REMOTE_KIT` | `<REMOTE_BASE>/kit` | `gatea:gatea` | `0700` |
| remote archive | `<REMOTE_BASE>/kit/runkit.tar` | — | — |
| `EXTRACT_DIR` | `<REMOTE_BASE>/kit/extracted` | — | `0700`, files `0444` |
| remote R4-5 runner | `<REMOTE_BASE>/R4_5_runner.py` | — | — |

All four identifiers were tested against the **accepted** predicate
`rp0_require_safe_component` from `RP0-LIB.sh` and accepted (rc 0); `../escaped`,
`a/b`, `.`, `..`, `-lead`, empty and `bad name` were refused (rc 1). See
`STAGE2_PREREG_SELF_QA.md` §Q14.

## 2. Preregistered inputs consumed by the accepted blocks

| Variable | Value | Origin |
|---|---|---|
| `B3_RELEASE_MANIFEST_SHA256` | `edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26` | derived read-only from the frozen candidate; see `CANDIDATE_RELEASE_DERIVATION.md` |
| `B3_SWEEP_BUDGET_S` | `120` | per-tree budget for the candidate `find … -perm /222` sweep. `-quit` only shortens a *failing* sweep, so a clean `/opt/mtc-bridge/releases/<sha>` or `/venvs/<sha>` walk is a full walk; exceeding the budget is STOP, never a pass. |
| `EV_PARENT_OWNER` / `EV_RUNKIT_OWNER` | `gatea:gatea` | login user of the recorded SSH route |
| `EV_PARENT_MODE` / `EV_RUNKIT_MODE` | `0700` | created by a single `mkdir -m 0700`, never `mkdir -p` |

`B3_RELEASE_MANIFEST_SHA256` is **never** read back from the target's
`/etc/mtc-bridge/install_manifest.json`. A manifest cannot attest to its own
acceptance.

## 3. Expected SHA-256 of every proposed block the stages carry

Frozen at Stage 1 (`01_RUNKIT/BLOCK_IDENTITIES.tsv`, commit `ff32a2db`); all nine
travel inside `runkit.tar` and are re-verified remotely before anything is
sourced.

| Block | File | Lines | SHA-256 | Carried by |
|---|---|---:|---|---|
| RP0-LIB | `RP0-LIB.sh` | 370 | `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48` | B3, R4-5 |
| RP0-BOOTSTRAP | `RP0-BOOTSTRAP.sh` | 36 | `e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33` | B3, R4-5 |
| RP1-B3 | `RP1-B3.sh` | 117 | `f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af` | B3 |
| RP3-C2A-POST | `RP3-C2A-POST.sh` | 104 | `e233d29b005964e84cd6cbc2af50deccd83bb281dac39696e47de1c8890b5a27` | transferred, **not executed** |
| RP3-C2B-POST | `RP3-C2B-POST.sh` | 74 | `26a1010cd9380289c5b90c08845b2af6ec31074fc5145241978a714b930bb412` | transferred, **not executed** |
| RP4-C3 | `RP4-C3.py` | 295 | `0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5` | R4-5 (function-level only) |
| RP5-C4A | `RP5-C4A.sh` | 374 | `a5b1b2e4d4e5227b3bb1f0ea31e9e547040231913445970efe1046f4eba9e0f2` | transferred, **not executed** |
| RP5-C4B | `RP5-C4B.sh` | 249 | `10c4b3231042101ed9049dbf57ec3123ce902e9b18136769728a1a2e92f4037e` | transferred, **not executed** |
| RP5-C4C | `RP5-C4C.sh` | 228 | `de7301f1deb752bcc63d818348c2fdc33372a6b7d7d4f377b62bdf27d313e3a8` | transferred, **not executed** |

Archive: `01_RUNKIT/runkit.tar`, 102400 bytes,
`618f7640fcb99a42abbe3d440710829e7be61f986050eb330035e46b3e11ac53`.

Only **B3** and the function-level **R4-5** falsification execute. C1, both C2
scenarios, C3, C4 A/B/C and C5 stay BLOCKED and unexecuted, exactly as the
accepted designs require; their blocks travel in the archive because the archive
is frozen, and are verified but never sourced.

## 4. Support-script hashes (every executed artifact)

Everything the operator sends is pinned. Sizes and digests as preregistered:

| File | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `remote_setup.sh` | 4976 | `faee3725325d7155a6309e2371b85a4facba1980f0169c8268e47a75902821b5` | op 01 stdin — create-once remote allocation |
| `remote_extract_verify.sh` | 8270 | `ba0bef0ef6ceb91c445e1d74e2c8d3b6fa7ac01e7e4e10216139b96b28c93db3` | op 04 stdin — archive/member/hash verification + extraction |
| `run_b3.sh` | 5194 | `0e54b0bf08d620035c98986a8fc4872dc7cc59d31788d608028b0c91751aa782` | op 05 stdin — B3 wrapper |
| `remote_close_tree.sh` | 7470 | `87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e` | ops 06 and 08 stdin — §1.5 closed-tree hashing |
| `run_r45.sh` | 4219 | `4b9e5e68cc5959bfdefc2b9996556a986e4004e553b410dc2cfcf65e50c44a7b` | op 07 stdin — R4-5 wrapper |
| `R4_5_runner.py` | 16170 | `8519e2bfc9bf2105bbb8e8c33fa4f271aa8852c7d7b18ad10286e19deddf68d5` | uploaded by op 03, re-verified against this hash inside op 07 |
| `TRANSPORT_PLAN.tsv` | 5817 | `0850f24fb2da47ea406ec328706a4ed2dc6d171af2032ac7cc32f032705a5239` | the ordered op list; pinned inside the runner |
| `transport_runner.ps1` | 18095 | `c5bdb47c9adf5cb65405656786d9da6b649d5ba66cc5ef2618244f098e0b25ed` | operator-side recorder |
| `CANDIDATE_RELEASE_SHA256SUMS` | 1181804 | `edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26` | derived payload manifest; its digest is `B3_RELEASE_MANIFEST_SHA256` |
| `derive_candidate_release_manifest.py` | 16353 | `89587d0be3ef8f2b6267c064c789933e418ddb8ebf987c924ffe4f19062e1927` | read-only derivation tool |

The complete set, including this document, is checksummed in
`PREREG_SHA256SUMS.txt`.

## 5. Exact remote argv

Route (recorded): `gatea@172.24.55.233`, identity
`C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519`. Options are pinned fail-closed on
every op:

```
-i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519
-o BatchMode=yes -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -o ConnectTimeout=20
```

`BatchMode=yes` refuses to prompt rather than hang. `StrictHostKeyChecking=yes`
refuses an unknown or changed host key rather than trusting it: a changed key
means the host identity is not the one this document describes, and silently
accepting it would defeat the preregistration. `IdentitiesOnly=yes` stops any
agent key being substituted for the named identity.

Every argv element is free of spaces and shell metacharacters, so the remote
login shell's re-parse of the command is a no-op. Scripts are delivered **on ssh
stdin** to `bash -s --`; no script is written to the host before it runs.

| op | run_when | kind | remote/local argv after the pinned options |
|---|---|---|---|
| 01 | sequence_ok | ssh stdin `remote_setup.sh` | `gatea@172.24.55.233 bash -s -- /home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08` |
| 02 | sequence_ok | scp up | `runkit.tar gatea@172.24.55.233:/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08/kit/runkit.tar` (cwd `01_RUNKIT`) |
| 03 | sequence_ok | scp up | `R4_5_runner.py gatea@172.24.55.233:/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08/R4_5_runner.py` (cwd `02_PREREG`) |
| 04 | sequence_ok | ssh stdin `remote_extract_verify.sh` | `gatea@172.24.55.233 bash -s -- <base>/kit/runkit.tar <base>/kit/extracted 618f7640fcb99a42abbe3d440710829e7be61f986050eb330035e46b3e11ac53` |
| 05 | sequence_ok | ssh stdin `run_b3.sh` | `gatea@172.24.55.233 bash -s --` |
| 06 | **always** | ssh stdin `remote_close_tree.sh` | `gatea@172.24.55.233 bash -s -- <EV_DIR B3> WPLP2-20260809T125940Z-8dc78f08-B3` |
| 07 | sequence_ok | ssh stdin `run_r45.sh` | `gatea@172.24.55.233 bash -s --` |
| 08 | **always** | ssh stdin `remote_close_tree.sh` | `gatea@172.24.55.233 bash -s -- <EV_DIR R45> WPLP2-20260809T125940Z-8dc78f08-R45` |
| 09 | **always** | scp down | `-r gatea@172.24.55.233:<EV_DIR B3> .` (cwd `<record>\evidence`) |
| 10 | **always** | scp down | `-r gatea@172.24.55.233:<EV_DIR R45> .` (cwd `<record>\evidence`) |
| 11 | **always** | local only | `local_bind 06 09 evidence\…-B3` — no host contact |
| 12 | **always** | local only | `local_bind 08 10 evidence\…-R45` — no host contact |

Every op preregisters `expect_rc = 0`. On the first rc that differs, **first-FAIL
stopping engages**: remaining `sequence_ok` ops are skipped, and only the
`always` ops still run — because a failed stage is exactly when its evidence must
be closed, bound and retrieved. This behaviour is demonstrated, not asserted
(`STAGE2_PREREG_SELF_QA.md` §Q9c).

The scp local paths are bare filenames with the working directory set, so no
argument ever contains a drive-letter colon that `scp` could parse as a host.

## 6. Operator-side transport evidence (RP0 §1.2)

`transport_runner.ps1` records, per op, from the first byte and independently of
anything the remote side writes:

- `ops/<id>.argv` — the exact argv sent, one element per line;
- `ops/<id>.stdout`, `ops/<id>.stderr` — complete, separately captured;
- the exit status, compared against the preregistered `expect_rc`;
- `TRANSPORT_RECORD.txt` — the full narration including every digest;
- `TRANSPORT_SHA256SUMS.txt` — sha256 of every captured file.

Record root, **create-once**:
`C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08`. If it already
exists the runner stops before any process starts; a rerun therefore needs a new
preregistration rather than a silent overwrite.

This matters because `RP0-BOOTSTRAP` calls `exec > "$EV_LOG" 2>&1`: after the
evidence leaf opens, remote output stops reaching ssh stdout. **Every failure
before that point is visible only in the operator-side record** — and those are
precisely the failures that decide whether a RUNID is burned.

Default mode is a dry run. Execution requires **both** `-Execute` and
`-Confirm WPLP2-20260809T125940Z-8dc78f08-EXECUTE`; anything else prints the plan
and opens nothing.

## 7. Closing and binding the evidence tree (RP0 §1.5)

A process never hashes its own still-open evidence. Ops 06 and 08 run
`remote_close_tree.sh` as **separate ssh invocations after the stage connection
has already returned** — that is the structural guarantee the stage shell has
exited. Because a structural guarantee is not a measurement, the script also
computes the digest set **twice** and refuses if the two passes differ, so a tree
that is still being written is never bound as closed.

It writes nothing into the evidence tree (writing a digest file into the
directory being hashed would change the bytes being attested) and emits, on
stdout only:

- `CLOSE_DIGEST <sha256>  <path relative to EV_DIR>` per file, `LC_ALL=C` order;
- `CLOSE_SIZE <relpath> <bytes>` per file — the §1.5 name/byte-count listing;
- `CLOSE_DIGEST_SET_SHA256 <runid> <sha256 of the digest set itself>`.

Ops 11 and 12 then perform the **local half of the binding**: local per-file
digests over the retrieved tree must equal the remote set name-for-name and
digest-for-digest, and the reconstructed digest-set rendering must reproduce
`CLOSE_DIGEST_SET_SHA256`. A remote-only or local-only hash is not a binding.

## 8. Preregistered expectations and predicted first divergence

Preregistering the expected outcome is what stops a result being re-narrated
afterwards. The **recorded** host state (from
`11_TRIAGE/GATE_A_POST_GATE_TRANSITION_INVENTORY_2026-08-09.md`, read-only) is:
only release `2ce41e34…321b` installed at mode `555`; venv counterpart `555`;
`/etc/mtc-bridge` metadata only, `install_manifest.json` 1007 B mode `640`; unit
fragment `/usr/local/lib/systemd/system/mtc-bridge-first-start.service` 3736 B
mode `644`; first-start unit active with `Restart=no`; one loopback listener.

| # | Predicted outcome if it holds | Exact predicted first divergence if it does not |
|---|---|---|
| 1 | release + venv roots are `0555 root:root` | `B3_FAIL reason=path=/opt/mtc-bridge/releases/2ce41e34… mode=<m> expected=555` |
| 2 | no write bit anywhere in either tree | `B3_FAIL reason=writable path inside immutable tree: <path>` |
| 3 | both sweeps finish inside 120 s | `B3_STOP reason=sweep_budget_exceeded root=<r> elapsed_s=<n> budget_s=120` |
| 4 | env file is `/etc/mtc-bridge/mtc-bridge.env`, `0600 root:root` | `B3_FAIL reason=missing path=/etc/mtc-bridge/mtc-bridge.env` — **named risk**: the inventory abbreviates this file as `bridge.env`; `common.sh:19` names it `mtc-bridge.env`. If the host file is actually named `bridge.env`, this is where B3 stops. |
| 5 | install manifest binds both the release SHA and `edb0fd34…` | `B3_FAIL reason=install manifest does not bind release_manifest_sha256` |
| 6 | R4-5 RED arm follows the dangling link and writes a real SQLite DB outside the restore root | `R45_FAIL reason=red_arm_raised_Fail: …` |
| 7 | R4-5 GREEN arm raises exactly `restore destination is a symlink: <path>` and leaves the target absent | `R45_FAIL reason=green_arm_returned_without_Fail` or `green_message_differs …` |

Any B3 `FAIL` — mode/owner drift, a symlink at a canonical deployment path, any
write bit, or a missing binding — is a **STOP requiring Lead adjudication**
(proposals §2.2), i.e. a candidate-repair question, not a documentation outcome.
Any `STOP` (rc 3) from a `stat`, `find`, `grep`, `mktemp` or clock error stops the
stage and is never re-read as a PASS.

**Scope of the R4-5 claim, preregistered:** it is a D026 Arm-1 falsification of
*one* guard — the two-line `dst_path.is_symlink()` `Fail` guard inside `RP4-C3
restore_into`. It is **not** a C3 run: no bundle is verified, no `verify_bundle`
is called, no manifest/db/invariants hash is adjudicated, no candidate release
tree is imported. C3 itself stays BLOCKED. The RED mutant differs from the
accepted bytes by exactly those two lines (accepted 12770 bytes → mutant 12672,
delta 98); the deletion is proven unique file-wide before it is applied.

## 9. What is deliberately NOT preregistered

- No C1, C2-A/C2-B, C3, C4-A/B/C or C5 execution: BLOCKED in the accepted
  designs, and no baseline method exists to unblock them here.
- No mutating step of any kind: no service stop, start, enable, disable, mask or
  unmask; no reboot; no rollback rehearsal; no unit write; no chmod/chown of any
  host object outside the run's own create-once tree.
- No credential read, no `POST /api/arm`, no broker/exchange/order/TESTNET/
  mainnet action, no master merge, no KVM2/WP-V action, no deletion of the old
  payload archive, no host reprovisioning.
- No `git add`, `git commit`, `git push`, branch or worktree action: Git
  sequencing belongs to the Lead.

## 10. Disposition of the five preserved partial files

The first attempt timed out and left five unaccepted partial scripts
(`STAGE2_PREREG_FAILURE_RECORD.md`, left byte-identical as history). Each was
reviewed rather than discarded or blindly reused:

| File | Disposition |
|---|---|
| `remote_setup.sh` | **Kept byte-identical** (`faee3725…`). Reviewed: create-once allocation, lstat-fail-closed classification, canonical/owner/mode assertions all correct. |
| `remote_extract_verify.sh` | **Kept byte-identical** (`ba0bef0e…`). Reviewed: hashes the archive before parsing any header, adjudicates both `tar -tvf` and `tar -tf`, refuses absolute/traversal/non-basename members, create-once extraction, `0444`, nine hashes verified from constants. |
| `R4_5_runner.py` | **Kept byte-identical** (`8519e2bf…`). Its mutation logic was exercised locally against the frozen `RP4-C3.py`: guard uniquely located at lines 124-125, delta exactly 98 bytes, mutant compiles. |
| `run_b3.sh` | **Repaired.** The pinned `B3_RELEASE_MANIFEST_SHA256` value is correct, but its provenance comment claimed a `package.sh` run in a clean detached clone, which was unevidenced and not available under this unit's constraints; the comment now states the real derivation. Also strengthened: block paths are refused if they are symlinks (`-f` dereferences). |
| `run_r45.sh` | **Repaired.** The runner was only existence-tested, so a truncated or altered upload would have executed; its bytes are now pinned and verified. `python3` children now read from `/dev/null` — the wrapper itself arrives on ssh stdin, so a child that read stdin would consume the rest of the script. Same symlink strengthening. |

Their presence granted no host authority before, and this document grants none
either: it grants only the preregistered *plan*.

## 11. Immutability rules

This preregistration is void, and a **new** one with fresh RUNIDs is required, if
any of the following changes: any hash in §3 or §4; the route, user, identity
path or ssh options in §5; any path in §1; either RUNID or stage id; or
`B3_RELEASE_MANIFEST_SHA256`. In particular, **if the staging VM's IP address is
no longer `172.24.55.233`, this preregistration does not describe the run** — the
argv is pinned, and editing it invalidates `TRANSPORT_PLAN.tsv`, whose digest the
runner pins, which is the intended failure mode rather than a silent edit.

A failed allocation burns its RUNID. There is no retry pool and no second RUNID
preregistered for either stage.

## 12. Safety state at the moment of preregistration

- SSH/SCP/remote invocation count: **0**
- Staging host contact: **none**; no socket opened, no process spawned toward it
- Service stop/start/enable/mask, reboot, rollback: **none**
- Credential read, ARM, order, broker/exchange, TESTNET/mainnet: **none**
- C1, C2, C3, C4, C5, B3, R4-5 execution: **none**
- Repository writes: confined to this `02_PREREG` directory; no `git add`,
  `commit`, `push`, checkout, branch or worktree action was performed
- `01_RUNKIT/runkit.tar` re-verified unchanged at
  `618f7640fcb99a42abbe3d440710829e7be61f986050eb330035e46b3e11ac53`
- The untracked `tmprepo_map_inventory.md` at the repository root was not touched

Self-QA evidence — every command and its real output — is in
`STAGE2_PREREG_SELF_QA.md`.
