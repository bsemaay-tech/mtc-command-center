# WP-L Phase 2 command-gap proposals — Codex re-audit round 3 (2026-08-09)

## Verdict

**REQUEST_CHANGES.** The round-3 proposal mechanics at frozen commit `909ab8f7` close the three
round-2 content findings under independent reproduction: the post-rollback bundle is now causally
created after the pinned rollback, the dry-run fingerprint detects same-count identity replacement,
and the preserved runner succeeds on consecutive invocations with fresh identifiers. The repair commit
also touches exactly the one contracted proposal file, so RR2-1 is closed as Lead logistics.

Acceptance is nevertheless withheld because the committed proposal's mandatory block-identity table
binds the new GREEN `RP0-LIB` to the old round-2 RED block's line count and SHA-256. The proposal says
all nine table entries match the executed transcripts, but one does not. This required documentation-
evidence finding is reproduced below.

This is repair/re-audit round 3 of 3. Per the frozen round limit, this non-accepting verdict **escalates
to the owner**; no fourth repair round is authorized or initiated.

The audit was documentation-only and local. No proposal, product, deploy, runtime, tool, test, schema,
Pine, parity, MTC, host, credential, broker, network, ARM/order, or `C:\PGRK` surface was changed or
contacted.

## Frozen identity and scope

- audited commit: `909ab8f7f9fdc5103a66f1176d8bc04d8006ab56`
- audited parent: `9c7121f0591f213503055cf05772182a87cfbe3c`
- audited proposal:
  `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md`
- audited proposal blob: `b4f56862bcafd707129b7e0ae0e357ed3bac34f2`
- audited proposal SHA-256 (Git blob/LF):
  `23c77abb3c8ed8f996bf5a1dbc63cfd4eb98eea055ce5922a4763e1daf5e34fc`
- exact frozen diff:

```text
git diff-tree --no-commit-id --name-status -r 909ab8f7
M  MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md

git diff-tree --no-commit-id --numstat -r 909ab8f7
1051  124  MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md
```

RR2-1 is therefore closed: the final repair commit modified exactly one file. During this audit an
unrelated agent advanced the branch tip from `909ab8f7` to `241c9cd1`; `909ab8f7` remains its immediate
ancestor and the proposal is unchanged. That unrelated Hermes/memory commit and the untracked
`tmprepo_map_inventory.md` were excluded and not assessed.

## Required finding

### RR3-1 — evidence identity — §8.1 assigns the round-2 RED digest to the round-3 GREEN `RP0-LIB`

The proposal says the table at `:2599-2609` contains the SHA-256 of every executable block extracted
from the committed file, and `:2586-2592` says all nine digests must equal both the table and the two
preserved transcripts. Its `RP0-LIB` row at `:2601` instead states:

```text
lines=249
sha256=4cc7ceff721c0eac5beb645a01bbca0630256f3e1d3ee7ad82d5db3ad7467dc8
```

Fresh extraction from the exact committed proposal blob reproduces:

```text
RP0-LIB lines=370
sha256=4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48
table_match=False
```

The discrepancy is not an extraction convention or line-ending artifact:

- both preserved round-3 transcripts record the true GREEN identity at line 17:
  `lines=370`, `sha256=4a404d7b...`;
- both transcripts identify the round-2 RED block separately at line 63 as
  `lines=249`, `sha256=4cc7ceff...`;
- independent extraction of the preserved round-2 proposal reproduces the same 249-line
  `4cc7ceff...` RED identity;
- the other eight committed block digests match §8.1 exactly;
- the implementer report §5 claim that all nine committed-file digests match §8.1 is therefore false.

The executable logic and the independent RED/GREEN runs below remain useful, but the proposal's stated
evidence binding is materially false for the block that contains the RR2-3 repair. This is a required
documentation-quality correction, not a formatting nit. Because the three-round limit is exhausted,
the minimum correction (replacing the row with 370 / `4a404d7b...` and making the binding claim
truthful) may proceed only if the owner explicitly reopens the cycle and defines any required audit.

## RR2 closure disposition

| Round-2 finding | Round-3 disposition |
|---|---|
| RR2-1 | **Closed.** `909ab8f7` changes exactly the proposal path and no second file. |
| RR2-2 | **Closed in the block text and independently reproduced.** Stage A proves the selected destination absent before mutation and after rollback, then create-once pins the rollback manifest. Stage B rebinds that event, proves the destination absent immediately before capture, and calls candidate `create_bundle` without `timestamp`. Stage C rebinds the capture record and live artifact, calls candidate `verify_bundle` with both exact hashes, and compares the candidate invariant hash plus all protected fields. A valid pre-rollback bundle is refused; a genuine A→B→C chain passes. |
| RR2-3 | **Behavioral defect closed; evidence-table defect RR3-1 remains required.** The fingerprint now compares canonical digests of writer PID/argv, listener endpoint/owner, and cgroup-path/PID inventories. Same-count writer, listener-owner, and cgroup-member replacements each reproduce RED `0` / GREEN `1`; an ownerless listener is GREEN STOP `3`. |
| RR2-4 | **Closed.** Two independent consecutive full invocations used distinct suffixes `run.dr9bHu` and `run.YYI0WX`; both returned process rc `0`, 41 expected outcomes, and 0 harness problems. The formerly colliding RP0 run ID and RP4 restore-root controls passed in both. |

## Independent D026 reproduction

The preserved root named by the implementer report was used directly:

```text
C:\Users\BARSEM~1\AppData\Local\Temp\D026R3.QgHw2b
```

The full runner was invoked twice consecutively without cleanup:

```powershell
& 'C:\Program Files\Git\bin\bash.exe' `
  'C:\Users\BARSEM~1\AppData\Local\Temp\D026R3.QgHw2b\run_all_r3.sh'
```

Key real output from each completed run:

```text
run.dr9bHu: S1-1 rc=0; S1-2 rc=0; expected outcomes=41; harness problems=0; PROCESS_RC=0
run.YYI0WX: S1-1 rc=0; S1-2 rc=0; expected outcomes=41; harness problems=0; PROCESS_RC=0

RR2-2 RED pre-rollback bundle: rc=0 (defect reproduced)
RR2-2 GREEN pre-existing destination: rc=1, before mutation
RR2-2 GREEN A/B/C positive chain: rc=0 / 0 / 0
RR2-2 GREEN truthful pre-rollback capture record: candidate VALID, final rc=1 on ns ordering
RR2-2 GREEN altered manifest/database/protected state: rc=1 / 1 / 1

RR2-3 writer replacement:   RED rc=0, GREEN rc=1
RR2-3 listener replacement: RED rc=0, GREEN rc=1
RR2-3 cgroup replacement:   RED rc=0, GREEN rc=1
RR2-3 owner unresolved:     RED rc=0, GREEN rc=3
RR2-3 path-probe STOP:      RED rc=3, GREEN rc=3
```

Two earlier wrapper attempts hit their local 120-second and 180-second process ceilings before a
complete summary returned. Their uniquely suffixed partial fixtures remain preserved and are excluded
from the evidence above. The two named completed runs are the acceptance evidence.

Fresh extraction from the committed file also reproduced:

```text
RP0-LIB          370  4a404d7b...  bash -n OK       # table mismatch, RR3-1
RP0-BOOTSTRAP     36  e7d748f6...  bash -n OK
RP1-B3           117  f40411b0...  bash -n OK
RP3-C2A-POST     104  e233d29b...  bash -n OK
RP3-C2B-POST      74  26a1010c...  bash -n OK
RP4-C3           295  0520cc90...  py_compile OK
RP5-C4A          374  a5b1b2e4...  bash -n + 2 heredoc py_compile OK
RP5-C4B          249  10c4b323...  bash -n + 1 heredoc py_compile OK
RP5-C4C          228  de7301f1...  bash -n + 1 heredoc py_compile OK
```

## Candidate anchors and prior-closure regression

Exact candidate `2ce41e34bceb599d80af24c5c33d835820ec321b` blobs reproduce:

```text
wal_state_bundle.py                       26c077e650ab88ba2086efa3a80790769bc055b1
deploy/linux/lib/common.sh                db11010a24edfbb96ba80ec1fbe1db3ff29193c9
deploy/linux/verify.sh                    5cfefd709202ff504ae7b7fc3504b8c0b00900b6
deploy/linux/rollback.sh                  4b36674dcb1baa7c3b119cac98f8e6017b1f1566
mtc-bridge-first-start.service.template   c18232549d96aa200d8c7f796e64de743288940c
```

Candidate-source inspection confirms the proposal's relevant anchors: `create_bundle` defaults
`timestamp=None` to `datetime.now(UTC)`, rejects source change during capture unless explicitly
allowed, `verify_bundle` requires both exact 64-hex expectations and recomputes DB/invariant hashes,
the rollback no-rebind path writes the documented fields, and dry-run mutations route through
`common.sh::run`.

No prior accepted closure regressed:

- `RP0-BOOTSTRAP`, `RP1-B3`, `RP3-C2A-POST`, `RP3-C2B-POST`, and `RP4-C3` are byte-identical to
  round 2 and retain their accepted digests.
- Function-by-function comparison of `RP0-LIB` reproduces all twelve pre-existing functions as
  byte-identical; only the three inventory functions are new.
- Round-1 and round-2 transcript SHA-256 values remain respectively
  `1bbb4a469aa1503d0d5aa4775835a97c4e6bccfb3c301fde61b9be3703a742e1` and
  `e6c991f1a34dcc12ea7af0b3a9bf34070aa6a3016b4f44d826138e432eeed68c`.
- F1/F2/F4-F9 accepted mechanics remain present; F3 remains honestly blocked rather than converted
  into a runnable claim.

## Blocked-item check

No blocked item is silently closed. The proposal still declares:

- C1 non-runnable with both `C1-GAP-A` and `C1-GAP-B` open;
- both scenario-level C2 paths blocked on the C1-GAP-B baseline;
- C5 blocked as an authority statement with no procedure;
- R4-5 unexercised/blocked by Windows symlink privilege;
- POSIX mode-bit and `mkdir -m` behavior modelled under disclosed MSYS `noacl` stubs;
- real cgroup-v2 behavior and real `ss` parsing unexercised;
- the candidate `rollback.sh` never executed; and
- the three-stage host/operator handoff, hostile-root resistance, and PID-reuse residuals not claimed
  closed.

## Disposition

Escalate RR3-1 and this **REQUEST_CHANGES** verdict to the owner. Do not start a fourth repair/re-audit
round without explicit owner authorization. This verdict grants no extraction, host, deployment,
budget, credential, broker, ARM/order, recovery-start, or trading authority.
