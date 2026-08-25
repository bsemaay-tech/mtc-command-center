# WP-P0-10 Kernel Economic Golden Suite — Implementer Lane Report

**Date:** 2026-08-25

**Branch:** `feature/wp-p0-10-golden-suite-20260825`

**Dispatched base / starting HEAD:** `c053648a25b8f7c37d0a7e20e4706098b8076ef1`

**Audit tier:** T0 (as assigned by the WP-P0-10 package contract)

**Implementer status:** STOPPED before fixture authoring because the required semantic authority is incomplete

**Acceptance language:** none; this implementer report is not an audit verdict

## 1. Scope and pre-implementation checks

The binding package contract is
`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:382-389`.
It requires deterministic fixtures for all 25 fixed families, expected outputs derived from
WP-P0-09 decided semantics, family 18 as an additional D026 RED/GREEN snapshot-drift case,
and a deliberate-mutation RED plus restored GREEN for every fixture.

The fixed family catalogue is
`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1763-1804`.
The WP-P0-09 semantic authority is
`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/CAPABILITY_CANONICALIZATION_TABLE.md`.

Before any write, the worktree was clean and `HEAD`, local `master`, and `origin/master` all
resolved to `c053648a25b8f7c37d0a7e20e4706098b8076ef1`. No kernel, optimizer, Pine, Bridge,
parity-corpus, contract, schema, or existing-fixture file was changed.

## 2. Blocking authority gap

### 2.1 Family 18 has no decided WP-P0-09 row

Family 18 requires **Snapshot drift / bucket-capital divergence** and specifically requires a
fixture that is RED without the `SNAPSHOT_MISMATCH` guard and GREEN with it
(`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1795`). The lane instruction
requires every expected output to cite the specific WP-P0-09 row from which it is derived and
forbids deriving an oracle directly from current implementation behaviour.

The merged WP-P0-09 package expressly withholds that decision:

- `CAPABILITY_CANONICALIZATION_TABLE.md:72` says no speculative row for snapshot drift was added.
- `CAPABILITY_CANONICALIZATION_TABLE.md:1287` says WP-P0-09 **does not decide snapshot-drift
  handling** and places it outside WP-P0-09 scope.
- `COVERAGE_SWEEP.md:300` says snapshot-drift handling was explicitly not added as a capability
  row. It distinguishes carrying snapshot identity from deciding mismatch handling.

C07 carries `snapshot_id` on `BoundSizingIntent` and states ownership of quantity calculation
(`CAPABILITY_CANONICALIZATION_TABLE.md:283-317`), but it does not specify a
`SNAPSHOT_MISMATCH` event, rejection, state transition, expected quantity, or D026 discriminator.
The literal `SNAPSHOT_MISMATCH` does not occur anywhere in the WP-P0-09 canonicalization table.
Therefore no family-18 expected output can truthfully cite a decided WP-P0-09 row.

The architecture brief does specify mismatch behaviour elsewhere at lines 1222-1229, but using
that text directly would violate this lane's stricter requirement that the expectation be derived
from and cite a decided WP-P0-09 row. I did not silently substitute that separate authority.

### 2.2 Family 19 has the same row-level gap for `REFERENCE_DIVERGENCE`

Family 19 requires the Allocator ↔ Guardian boundary, authorize-or-reject with no resize path,
and `REFERENCE_DIVERGENCE` behaviour
(`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1796`). C07 does restate that the
Guardian authorizes RA's quantity unchanged or rejects
(`CAPABILITY_CANONICALIZATION_TABLE.md:294`), and C18 assigns account vetoes to the Guardian.
However, neither row specifies the required `REFERENCE_DIVERGENCE` output or its discriminator;
the literal `REFERENCE_DIVERGENCE` does not occur in the canonicalization table. The same
explicit non-decision at `CAPABILITY_CANONICALIZATION_TABLE.md:1287` covers the internal
Allocator/Guardian split.

Consequently family 19 also lacks a complete row-derived oracle under the dispatched citation
rule. The architecture brief supplies the missing behaviour at lines 1223-1226, but it is not a
WP-P0-09 row and was not used as a substitute.

### 2.3 Required stop

The lane's honesty rule says to stop on any family whose expected output cannot be derived from a
decided WP-P0-09 row. Authoring a fixture anyway would either invent a value, derive the oracle
from current code, or bypass the required authority chain. All three are prohibited. Because all
25 families are mandatory, the package cannot meet its gate while families 18 and 19 have no
row-derived oracle.

No fixture, test harness, mutation, snapshot, or deterministic output was created. This prevents
partial artifacts from being mistaken for an acceptance-bearing suite.

## 3. The 25 fixed families and candidate row map

This is a routing map only. A `candidate row` identifies where fixture work would begin after the
authority gap is repaired; it is not an expected-output citation and no fixture is claimed.

| # | Fixed family name | Candidate WP-P0-09 row(s) | Fixture | Mutation RED / restored GREEN | Two-run byte determinism |
|---:|---|---|---|---|---|
| 1 | Entry signal | C01, C02, C03, C04, C38, C39, C40, C41, C42 | NOT CREATED | NOT RUN | NOT RUN |
| 2 | Direction / flip / regime lock | C05, C21, C32, C33 | NOT CREATED | NOT RUN | NOT RUN |
| 3 | Position sizing | C07, C31 | NOT CREATED | NOT RUN | NOT RUN |
| 4 | Contract multiplier | C08 | NOT CREATED | NOT RUN | NOT RUN |
| 5 | Minimum notional | C09 | NOT CREATED | NOT RUN | NOT RUN |
| 6 | Rounding / qty step / min qty | C09, C31 | NOT CREATED | NOT RUN | NOT RUN |
| 7 | SL calculation (ATR / percent / swing) | C11, C24 | NOT CREATED | NOT RUN | NOT RUN |
| 8 | TP calculation (ATR / percent / R) | C12, C24 | NOT CREATED | NOT RUN | NOT RUN |
| 9 | Multi-TP lifecycle incl. partial TP1 fill | C13 | NOT CREATED | NOT RUN | NOT RUN |
| 10 | Break-even trigger and buffer | C14, C36 | NOT CREATED | NOT RUN | NOT RUN |
| 11 | Trailing activation and monotonicity | C15, C37 | NOT CREATED | NOT RUN | NOT RUN |
| 12 | Opposite-signal exit | C05, C16, C21, C32, C33 | NOT CREATED | NOT RUN | NOT RUN |
| 13 | Time exit (bars / EOD / EOW) | C17, C25 | NOT CREATED | NOT RUN | NOT RUN |
| 14 | Bar gaps through the stop | C11, C20 | NOT CREATED | NOT RUN | NOT RUN |
| 15 | Same-bar SL/TP collision | C19 | NOT CREATED | NOT RUN | NOT RUN |
| 16 | Pyramiding / add / partial reduction | C06, C13 | NOT CREATED | NOT RUN | NOT RUN |
| 17 | Fees, slippage, funding | C08, C22 | NOT CREATED | NOT RUN | NOT RUN |
| 18 | Snapshot drift / bucket-capital divergence | **BLOCKED — no decided WP-P0-09 mismatch row** | NOT CREATED | NOT RUN | NOT RUN |
| 19 | Allocator ↔ Guardian boundary | **PARTIALLY ROUTABLE to C07/C18, but `REFERENCE_DIVERGENCE` has no row-derived oracle** | NOT CREATED | NOT RUN | NOT RUN |
| 20 | Short-side symmetry | C24 plus WP-P0-09 cross-cutting rule 2 | NOT CREATED | NOT RUN | NOT RUN |
| 21 | NaN / zero / boundary precision | C07, C09, C24 | NOT CREATED | NOT RUN | NOT RUN |
| 22 | Duplicate and reordered bars | C26 | NOT CREATED | NOT RUN | NOT RUN |
| 23 | Cancellation and revision ordering | C26 | NOT CREATED | NOT RUN | NOT RUN |
| 24 | `OrderIntent` idempotence | C26 | NOT CREATED | NOT RUN | NOT RUN |
| 25 | Venue and session edge cases | C09, C17, C22, C25, C27 | NOT CREATED | NOT RUN | NOT RUN |

The family names above reproduce the binding catalogue without merging, splitting, or renaming a
family. The table intentionally does not claim that the candidate mapping is sufficient until the
two blocked expected-output authorities are repaired and rechecked.

## 4. RED/GREEN and determinism evidence

There is no RED/GREEN or determinism evidence to report. No command was run that purported to
exercise a golden fixture, because no honest complete fixture set could be authored from the
dispatched authority. In particular:

- no mutation output is presented as if it came from an executable fixture;
- no self-consistency check is presented as economic-behaviour evidence;
- no deterministic hash is presented for a fixture that does not exist; and
- family 18's required snapshot-drift D026 case remains unexecuted, not silently waived.

## 5. Required upstream repair before redispatch

The Lead needs one of these explicit authority repairs before WP-P0-10 can resume:

1. Amend WP-P0-09 with decided capability row(s) that specify the exact family-18
   `SNAPSHOT_MISMATCH` oracle and family-19 `REFERENCE_DIVERGENCE` oracle, including complete
   eight-field GF specifications and deliberate RED discriminators; or
2. Amend the WP-P0-10 lane contract to authorize a named non-WP-P0-09 decided source for those
   two expectations, while preserving exact citations and D026 requirements.

Any amended protected/economic authority should complete its required review before this lane is
redispatched. This implementer did not change WP-P0-09, because the lane allows fixtures only.

## 6. Implementer self-QA

The following read-only checks were executed after writing this report:

- `MTC_COMMAND_CENTER/tools/repo_guard.ps1` returned rc 0; it reported the dispatched branch,
  merge-base equal to `c053648a25b8f7c37d0a7e20e4706098b8076ef1`, zero commits behind local
  `origin/master`, no protected-scope change, and no risky untracked file. It also reported that
  this new branch had no upstream before the required push.
- A PowerShell anchored-row extraction over this report returned
  `REPORT_FAMILY_ROWS=25` and sequence
  `1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25`.
- Exact literal searches of the WP-P0-09 canonicalization table returned
  `SNAPSHOT_MISMATCH_IN_WPP009_TABLE=0` and
  `REFERENCE_DIVERGENCE_IN_WPP009_TABLE=0`.

No economic fixture test was run or claimed; section 4 records why.

## 7. Git record

Only this blocker report is intended for the lane commit. The pushed branch HEAD is printed as the
last line of the implementer's final output. A tracked report cannot contain the SHA of the same
commit that contains it (adding that SHA changes the commit), so this field is stated honestly
rather than populated with a false self-reference.

**Final pushed commit SHA:** supplied in implementer output after commit and push.
