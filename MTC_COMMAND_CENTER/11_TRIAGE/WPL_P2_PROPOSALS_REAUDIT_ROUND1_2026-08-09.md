# WP-L Phase 2 command-gap proposals — Codex re-audit round 1 (2026-08-09)

## Verdict

**REQUEST_CHANGES.** The repair at frozen commit `7194b895` materially improves the rejected
proposal and honestly preserves the declared blocked items, but it does not yet satisfy the frozen
repair specification at `9ac60ac6`. Five required findings below reproduce against the exact repaired
blob `690d40f5cdbb66efd24cf6c63a8bf661cbe961ee`.

This was a fresh documentation-only re-audit. No proposal, product, deploy, runtime, tool, test,
schema, Pine, parity, MTC, host, credential, broker, network, ARM/order, or `C:\PGRK` surface was
changed or contacted.

## Frozen scope and identity

- audited commit: `7194b895`
- audited path: `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md`
- audited Git blob: `690d40f5cdbb66efd24cf6c63a8bf661cbe961ee`
- audited file SHA-256 with LF: `001be881b0cdc9e56d848936252c76e642630d54dd46d4f2fd2460163963a83b`
- repair-spec commit/blob: `9ac60ac6` / `b867bdcf0467c9b77978721f789977ca88fd5d6d`
- diff scope: `git diff-tree --no-commit-id --name-status -r 7194b895` returned exactly the one
  proposal path above; `git show --check 7194b895` was clean.
- exact candidate `2ce41e34bceb599d80af24c5c33d835820ec321b` blobs reproduced:
  `wal_state_bundle.py=26c077e650ab88ba2086efa3a80790769bc055b1`,
  `common.sh=db11010a24edfbb96ba80ec1fbe1db3ff29193c9`,
  `verify.sh=5cfefd709202ff504ae7b7fc3504b8c0b00900b6`,
  `rollback.sh=4b36674dcb1baa7c3b119cac98f8e6017b1f1566`, and
  `mtc-bridge-first-start.service.template=c18232549d96aa200d8c7f796e64de743288940c`.

## Required findings

### R1 — P0 — RP0 permits the evidence leaf to escape the directory that is later hashed

The bootstrap requires only that `EV_STAGE_ID` be non-empty (`:333`) and constructs
`EV_LOG="$EV_DIR/${EV_STAGE_ID}.log"` (`:344`). It does not require a single safe path component.
Consequently `EV_STAGE_ID=../escaped` opens the active evidence log beside `EV_DIR`, while §1.5
hashes only `<EV_DIR>` (`:350-364`). `RUNID` is likewise not constrained to one safe component.
This violates RP0's requirement that the leaf be inside the newly owned directory and defeats the
remote/local closed-tree binding even though the block returns success.

Lead reproduction used the exact extracted `RP0-LIB` and `RP0-BOOTSTRAP` blocks with a fresh local
fixture and only the preserved mode-setting stub:

```text
RUNID=RUN-TRAVERSAL
EV_STAGE_ID=../escaped
BLOCK_RC=0
EV_DIR_FILE_COUNT=0
ESCAPED_LOG_EXISTS=True
ESCAPED_LOG_CONTENT=RP0_EVIDENCE ... leaf=.../RUN-TRAVERSAL/../escaped.log|
```

Required repair: validate `RUNID` and `EV_STAGE_ID` as preregistered single components under a strict
allowlist, prove the derived leaf remains directly beneath the allocated `EV_DIR`, and add a
falsification for separator/`..` traversal.

### R2 — P0 — the C2 post-reboot blocks omit mandatory postconditions

Repair-spec RP3 requires Scenario A after reboot to establish no writer, listener, **or cgroup
survivor**, `app_state != ARMED`, and protected-invariant equality (`repair spec :133-134`). Scenario B
also requires no cgroup survivor (`:143-144`). The exact `RP3-C2A-POST` and `RP3-C2B-POST` blocks
contain zero cgroup predicate calls. Scenario A mentions `app_state != ARMED` only in a comment
(`proposal :732`) and never asserts it. Both blocks stop after process/listener checks (`:717-728`,
`:819-830`) and then compare supplied hash strings/files.

Static reproduction against the exact block boundaries returned:

```text
BLOCK=RP3-C2A-POST lines=72 cgroup=0; app_state assertion=0
BLOCK=RP3-C2B-POST lines=68 cgroup=0; app_state assertion=0
```

The scenario-level tests are correctly declared blocked, but that does not permit the published
post-reboot design to omit required predicates. Add fail-closed cgroup-survivor checks to both blocks
and an absolute `app_state != ARMED` assertion to Scenario A before either can be accepted.

### R3 — P0 — C3 does not perform the required candidate `verify` step

Repair-spec RP4 step 1 requires re-verifying the accepted bundle with candidate `verify` and exact
expected hashes (`repair spec :154`). The repaired `RP4-C3` imports only constants,
`collect_invariants`, and `invariants_hash` (`proposal :929-945`) and performs a partial local
reimplementation of bundle checks. It contains no call to candidate `verify_bundle` and no candidate
`verify --expect-bundle-sha256 --expect-invariants-sha256` invocation. Section 5.3 instead weakens the
requirement to a prior `verify` PASS (`:1131-1136`).

Candidate `wal_state_bundle.py:1125-1205` shows that `verify_bundle` additionally validates the full
manifest contract, integrity hash, source/arrival contract, expected DB hash, expected invariant hash,
sidecars, integrity/FK, and re-derived invariants. Exact-block inspection returned
`candidate_verify=0` for all 237 lines of `RP4-C3`.

Required repair: call the frozen candidate verification API/CLI in this evaluation with both exact
expected hashes, adjudicate its statuses fail-closed, and then proceed to restore only after it returns
the exact accepted verdict.

### R4 — P0 — C4 can PASS without a fresh verified post-rollback bundle

Repair-spec RP5 requires a fresh post-rollback candidate bundle to verify and its protected invariants
to equal the preregistered values (`repair spec :189-190`). The repaired block merely requires two
non-empty environment strings (`proposal :1207-1208`) and compares them for string equality
(`:1386-1392`). It never invokes candidate bundle creation/verification, never derives either value
with the candidate API, and never binds the post value to a fresh artifact. It also omits the required
post-rollback cgroup-survivor check (`repair spec :187`; exact `RP5-C4` block `cgroup=0`).

The preserved RP5 harness itself falsifies the claimed closure. Its setup writes the dummy file
`{"accepted":"c3-bundle-manifest"}` and sets both invariant variables to the non-SHA string
`INV-BASELINE`; the independently replayed exact repaired block still returned:

```text
rc=0
C4_c3_manifest_sha256=baa1344794e5843e27acaeacc7fa03f282e88bd07cbb12626d3ee279557e2220
C4_invariants_equal=yes sha256=INV-BASELINE
C4 PASS (unit stopped and masked; no start, unmask or recovery is authorised by this result)
```

Therefore R5-4 proves only that unequal injected strings are rejected; it does not satisfy D026 for the
named persistence defect. Required repair: bind pre/post values and protected fields to accepted
candidate-generated artifacts, re-run candidate verification with exact expected hashes, add the
cgroup predicate, and falsify stale/equal/unbound inputs.

### R5 — P0 — C4's dry-run fingerprint swallows a path-probe STOP

`c4_fingerprint` correctly adjudicates its first four command substitutions, but nests the rollback
manifest probe and C3 hash inside arguments to `printf` (`proposal :1229-1232`). The status of `printf`,
not either nested predicate, becomes the function status. A probe failure is thus rendered as an empty
field and the function returns success, contrary to the three-outcome contract and repair-spec RP5's
fail-closed dry-run requirement.

Lead executed the exact function text extracted from `7194b895`, with `rp0_probe_path` returning the
required STOP rc `3` only for the rollback manifest:

```text
RP0_STOP simulated
FINGERPRINT_RC=0
FINGERPRINT=[active=active enabled=static mask=absent listeners=0 writers_rc=1 manifest= c3=abc]
```

Required repair: evaluate and adjudicate every fingerprint component in its own assignment before the
final `printf`; a failed probe/hash must return STOP and no before/after equality may be evaluated.

## F1-F9 closure disposition

| Prior finding | Re-audit disposition |
|---|---|
| F1 | **Not closed** — R1 defeats evidence-tree containment/binding. |
| F2 | Closure mechanics reproduced; POSIX mode fixtures remain honestly stubbed. |
| F3 | Acceptably remains BLOCKED on C1-GAP-A/B; no runnable C1 was introduced. |
| F4-F5 | **Not closed** — R2 omits required C2 postconditions. |
| F6 | **Not closed** — R3 omits the mandatory candidate re-verification. |
| F7 | The regular/dangling rollback-manifest refusal and dry-run ordering reproduced. |
| F8 | **Not closed** — R4 accepts stale/unbound strings instead of a fresh verified bundle proof. |
| F9 | **Not closed cross-cutting** — R5 converts a path-probe STOP into fingerprint success. |

## Independent evidence reproduction

The preserved implementer transcript exists and its SHA-256 reproduced as
`1bbb4a469aa1503d0d5aa4775835a97c4e6bccfb3c301fde61b9be3703a742e1`.
The Lead replayed the preserved sources in their required shared-root order under
`C:\tmp\CODEX_REAUDIT_R1B_20260809_123340`. The first isolated-root attempt was discarded because
RP1/RP5 require the `with.sh` helper generated by RP0; only the corrected ordered replay below counts.

```text
bash run_rp0.sh <root> <root>/rp0_record.md       -> runner rc 0
bash run_rp1.sh <root> <root>/rp1_record.md       -> runner rc 0
bash -lc "python run_rp4.py ..."                  -> runner rc 0
bash run_rp5.sh <root> <root>/rp5_record.md ...   -> runner rc 0

rp0_record.md  sha256=840f45f5c90af4efb213a1462bef18083ab41e3555839d9f07db048c213d7aee
rp1_record.md  sha256=3bed797228254277402c865c47f031b5dca9e4515355098051a4f061126f3ccc
rp4b_record.md sha256=96379c07e806e2b7969fbd7388c28f78124a3fc07bef76eb23eca75b7a5ffbe8
rp5_record.md  sha256=7b83d17c068b9e75d7f0f3eaf4708dd33c5a88623c2ee5515572f46fca72aca4
```

The replay reproduced the claimed RP0, RP1, RP4, and RP5 case outcomes, including the original F6
`AttributeError`, the same-size F8 RED, and corrected GREEN adjudications. R4-5 remained unexecuted for
the declared Windows symlink-privilege reason. All seven exact block hashes matched the proposal's §8
table; six shell blocks passed `bash -n`, and `RP4-C3` compiled successfully from its extracted file.

## Declared open items

The following are stated honestly and are not additional findings:

- C1 remains non-runnable with `C1-GAP-A` and `C1-GAP-B` open (`§3`).
- Both C2 scenarios remain blocked on the C1-GAP-B baseline dependency; scenario-level C2 tests are
  not claimed closed (`§4`, `§8.6`).
- R4-5 remains explicitly unexercised because this Windows session cannot present CPython with the
  required dangling symlink (`§5.4`, `§8.4`, `§8.6`).
- POSIX mode-bit and `mkdir -m` fixtures are explicitly disclosed as GNU-semantics stubs on the MSYS
  `noacl` NTFS mount (`§8.1`).
- C5 remains blocked and contains no executable credential/network/broker procedure (`§7`).

## Disposition

Do not extract or run the proposed blocks against a host. Return R1-R5 to the same counterpart for the
next bounded repair round, then perform a fresh re-audit with D026 RED/GREEN evidence for each repaired
defect. This verdict grants no host, budget, credential, broker, ARM/order, deployment, or trading
authority.
