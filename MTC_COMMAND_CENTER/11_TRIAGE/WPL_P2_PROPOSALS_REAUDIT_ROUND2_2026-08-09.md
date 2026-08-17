# WP-L Phase 2 command-gap proposals — Codex re-audit round 2 (2026-08-09)

## Verdict

**REQUEST_CHANGES.** The repair at frozen commit `75ee8912` closes R1, R2, R3, and the narrow
R5 status-adjudication defect under local reproduction, and it continues to disclose every blocked
item honestly. It does not close R4's fresh-post-rollback requirement, does not fully prove that the
rollback dry run leaves processes unchanged, and its preserved runner does not satisfy the document's
own rerun claim. The frozen repair commit also violates the audit contract's one-file diff scope.

All required findings below were reproduced against the exact repaired proposal blob
`9785bf8eba29c52ac61744986800e7f66c8fd6bf`. This was a documentation-only, local re-audit. No
proposal, product, deploy, runtime, tool, test, schema, Pine, parity, MTC, host, credential, broker,
network, ARM/order, or `C:\PGRK` surface was changed or contacted.

## Frozen identity and scope

- audited commit: `75ee89127ced14344d449fafb13fc8a944c89835`
- audited parent: `1dad319659af6dfc092f29971288362fa60750cc`
- audited proposal: `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md`
- audited proposal blob: `9785bf8eba29c52ac61744986800e7f66c8fd6bf`
- audited proposal SHA-256: `89778b02042306696e6b1d21d5f2401c14eb9a9411498074124ed3c32249e73b`
- repair-spec commit/blob: `9ac60ac6` / `b867bdcf0467c9b77978721f789977ca88fd5d6d`
- round-2 transcript SHA-256 reproduced:
  `e6c991f1a34dcc12ea7af0b3a9bf34070aa6a3016b4f44d826138e432eeed68c`
- exact candidate blobs reproduced:
  `wal_state_bundle.py=26c077e650ab88ba2086efa3a80790769bc055b1`,
  `common.sh=db11010a24edfbb96ba80ec1fbe1db3ff29193c9`,
  `verify.sh=5cfefd709202ff504ae7b7fc3504b8c0b00900b6`,
  `rollback.sh=4b36674dcb1baa7c3b119cac98f8e6017b1f1566`, and
  `mtc-bridge-first-start.service.template=c18232549d96aa200d8c7f796e64de743288940c`.

The seven final block digests independently re-extracted from the frozen proposal exactly match its
§8.1 table and the preserved transcript. All six shell blocks pass Git Bash 5.2.37 `bash -n`; the
Python block passes CPython 3.14.2 `py_compile`. `git show --check 75ee8912` is clean.

## Required findings

### RR2-1 — scope — the frozen repair commit contains two files, not the contracted one

The V2 kickoff requires verification that the repair diff touched only the proposal, and the
implementer report §1 says exactly one file was edited. The exact frozen commit instead reproduces:

```text
git diff-tree --no-commit-id --name-status -r 75ee8912
A  MTC_COMMAND_CENTER/11_TRIAGE/CODEX_REAUDIT_KICKOFF_V2_2026-08-09.md
M  MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md
```

Required repair: the next frozen repair commit must modify exactly the proposal path and no other file;
its implementation report must describe the actual frozen diff.

### RR2-2 — P0 — R4 still accepts a bundle that existed before the rollback

The block requires `C4_POST_BUNDLE_DIR` and all three alleged post-capture hashes as non-empty inputs at
proposal `:1435-1438`, before the dry run (`:1527`) and real rollback (`:1543-1548`). It contains no
post-rollback capture step and no split-stage handoff through which those future values can be supplied.
Its only ordering proof is the two manifest strings compared at `:1726-1733`.

The preserved positive control is itself the falsification. Lead inspection established that
`rp5/bundle_post/bundle_manifest.json` already existed before `run_c4.sh GREEN` invoked the rollback
stub. The exact repaired block nevertheless returned PASS because its embedded timestamp was later
than the stub's rollback timestamp:

```text
bundle_post existed before rollback block: rc=0
bundle_post manifest mtime: 2026-08-09 13:05:34 +0300
C4_post_bundle_generated_at_utc=2026-08-09T12:45:00Z
rolled_back_at_utc=2026-08-09T12:30:00Z
C4_post_bundle_verify_rc=0 verdict=VALID failures=[]
C4_post_rollback_bundle_verified=yes
C4 PASS
rollback manifest mtime after block: 2026-08-09 13:33:39 +0300
BLOCK_RC=0
```

The candidate `create` CLI accepts an operator-supplied `--timestamp`
(`wal_state_bundle.py:1218-1222`), so candidate verification authenticates the bundle contents but does
not turn that timestamp into causal proof of capture order. R4-2 and R4-3 reject only selected identity
or timestamp values; they do not falsify a distinct, valid, pre-existing bundle carrying a later claimed
timestamp. RP5's required **fresh post-rollback** artifact is therefore still absent.

Required repair: make the post artifact causally downstream of the rollback. For example, split mutation
and capture/verification into separately evidenced stages: prove the selected post destination absent
before mutation, perform the authorized rollback, then create and externally record a new candidate
bundle, and only then run verification/equality. An operator-controlled wall-clock field cannot be the
sole ordering proof. Add D026 RED on the current block using the preserved pre-existing positive-control
bundle, then GREEN on the repaired causal sequence.

### RR2-3 — P0 — the dry-run fingerprint does not prove that processes are unchanged

RP5 requires the dry run to cause no process or listener change. `c4_fingerprint` discards the successful
output of `rp0_pgrep_status` and records only `writers_rc=0`; it likewise records only listener and cgroup
counts (`:1463-1475`). Replacing one bridge writer with another therefore leaves the before/after strings
equal. Lead executed the exact repaired function with only surrounding predicates stubbed:

```text
writer_before=1111 /usr/bin/python -m bridge.app
fingerprint_before=[active=active enabled=static mask=absent listeners=1 writers_rc=0 cgroup=1 ...]
writer_after=2222 /usr/bin/python -m bridge.app
fingerprint_after=[active=active enabled=static mask=absent listeners=1 writers_rc=0 cgroup=1 ...]
fingerprints_equal_rc=0
```

The same structural blind spot permits listener or cgroup membership replacement at an unchanged count.
The repaired R5 path-probe/hash STOP handling is correct, but it does not close this no-mutation claim.

Required repair: record and compare fail-closed, canonical inventories that identify the relevant writer
processes, listening sockets, and cgroup membership, not only presence/status/count. Add RED/GREEN for a
same-count identity replacement.

### RR2-4 — evidence — the preserved runner does not allocate fresh identifiers on rerun

Proposal `:1816-1819` says the preserved `run_all_final.sh` allocates fresh identifiers on rerun. The
runner instead hard-codes `RUN-TRAV-F`, `RUN-R2-OKF`, `restore_f0`, and the other restore labels. Running
the preserved command a second time reproduced failures in positive controls rather than a fresh replay:

```text
### R1-4 GREEN positive control
RP0_STOP reason=evidence_allocation_failed .../RUN-R2-OKF ... File exists run_id_burned=yes
BLOCK_RC=3

### R3-0 GREEN positive control
C3_FAIL reason=restore root already exists: ...\rp4\r3_0\restore_f0
BLOCK_RC=1
```

The original 286-line transcript and its hash remain intact, and targeted Lead runs with genuinely new
IDs/restore labels reproduced R1-R3. The advertised one-command reproduction contract, however, is false.

Required repair: make the preserved runner generate one fresh run suffix per invocation and use it for
every create-once run ID and restore root, or document and supply a safe fixture-cloning procedure. Record
a second consecutive full-run transcript proving both runs preserve the expected case outcomes.

## R1-R5 closure disposition

| Round-1 finding | Round-2 disposition |
|---|---|
| R1 | **Closed.** Exact RED still escapes; GREEN rejects traversal, the independent direct-child layer rejects `..`/sibling paths, and a clean positive control succeeds. |
| R2 | **Closed at the claimed block/stub level.** Cgroup survivors fail both post blocks; unevaluable/blank cgroup properties STOP; Scenario A rejects absolute `app_state=ARMED`. Scenario-level C2 remains blocked, as declared. |
| R3 | **Closed.** The exact round-1 block accepts candidate-invalid manifest states; the repaired block calls the frozen candidate `verify_bundle` with both external hashes before restore and rejects them. A clean real bundle passes. |
| R4 | **Not closed — RR2-2.** Verification and field equality work, but the design accepts a distinct verified artifact that demonstrably existed before rollback. |
| R5 | **Narrow defect closed.** Probe/hash failures now return rc 3 and no fingerprint is emitted. The broader dry-run no-process-change predicate remains incomplete — RR2-3. |

## F1-F9 regression and blocked-item check

- F1: evidence no-clobber and containment reproduce; RR2-1 is commit scope, not an F1 regression.
- F2: `RP1-B3` is byte-identical to round 1 (`f40411b0...`); the accepted round-1 closure evidence
  remains applicable, with POSIX mode semantics still disclosed as stubs.
- F3: C1 remains non-runnable with `C1-GAP-A` and `C1-GAP-B` explicitly open.
- F4-F5: exact token/mask predicates and protected-equality design remain present; the repaired post
  blocks add the missing cgroup and absolute `app_state` checks. Both scenarios remain blocked on the
  genuine C1-GAP-B baseline.
- F6: candidate API usage, backup restore, invariant hashing, identities, sidecars, and artifact
  preservation remain present; mandatory candidate re-verification now reproduces.
- F7: the pre-existing rollback-manifest refusal preserves the prior record and remains closed. The
  separate dry-run no-process-change gap is RR2-3.
- F8: **not closed** because RR2-2 still permits a pre-rollback artifact to stand in for the required
  fresh post-rollback capture.
- F9: shared `pgrep`/`is-enabled` three-outcome adjudication remains present; the R5 nested probe/hash
  STOP defect reproduces RED and GREEN correctly.

No blocked item was silently closed: R4-5 remains unexercised for Windows symlink privilege; C1-GAP-A/B
remain open; both C2 scenarios remain blocked on the baseline dependency; platform mode-bit and
`mkdir -m` behavior remain disclosed as MSYS `noacl` stubs; C5 remains an authority statement with no
procedure. The document also continues to disclose that real cgroup-v2 semantics and the real candidate
`rollback.sh` were not exercised.

## Independent reproduction summary

Targeted local commands used the preserved root
`C:\Users\BARSEM~1\AppData\Local\Temp\D026R2.87imLE`, Git Bash 5.2.37, CPython 3.14.2, SQLite
3.50.4, the real candidate module for RP4/RP5 bundle verification, and only the disclosed local stubs for
service/rollback behavior. Results included:

```text
R1 traversal: RED rc 0; GREEN rc 1; clean GREEN rc 0
R2 cgroup survivor: RED C2A PASS rc 0; GREEN C2A_FAIL rc 1
R2 app_state=ARMED: RED C2A PASS rc 0; GREEN C2A_FAIL rc 1
R3 candidate-invalid manifest: RED C3 PASS rc 0; GREEN verify INVALID / C3_FAIL rc 1
R4 unbound string input: GREEN STOP rc 3
R5 path-probe STOP: RED fingerprint rc 0; GREEN fingerprint rc 3 with empty value
```

The Lead did not manufacture runs for C1, scenario-level C2, C5, or the declared Windows-only R4-5
symlink case. Independent audit reruns added only disposable local fixture outputs under the supplied
temporary evidence root; the preserved transcript file and its SHA-256 did not change.

## Disposition

Return RR2-1 through RR2-4 to the same counterpart for repair round 3, the final permitted round, then
perform a fresh re-audit at a new frozen one-file commit. This verdict grants no extraction, host,
deployment, budget, credential, broker, ARM/order, recovery-start, or trading authority.
