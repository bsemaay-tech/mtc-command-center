# WP-P0-10 Kernel Economic Golden Suite — Implementer Repair Report

**Date:** 2026-08-25

**Branch:** `feature/wp-p0-10-golden-suite-20260825`

**Repair starting HEAD:** `c05e596807534845d1665ef38b2e4b006f269089`

**Audit tier:** T0, retained from the package contract; both flagships re-audit after this handoff

**Implementer status:** repair and self-QA complete; 23 families remain built; families 18 and 19 remain formally blocked; independent Lead acceptance is pending

**Acceptance language:** none; this is implementation and executed self-QA evidence, not an audit verdict

## 1. Scope and corrected evidence claim

The binding package contract is
`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:382-389`.
The fixed family catalogue is
`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1763-1804`.
The semantic authority is
`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/CAPABILITY_CANONICALIZATION_TABLE.md`.

No previously accepted expected value was changed. Exactly 11 new assertion records were added as
coverage: eight price-reflected short-twin records in `family_05.json`, and the three GF-06 records
the deciding row says the fixture asserts in `family_16.json`. Family 5 also gained the literal
direction/reflection inputs needed to make that twin reproducible; family 16 gained the deciding
row's literal no-signal bar 3 so its new `events.bar3 = NONE` assertion has an input. Only those two
fixtures' output hashes and manifest-local fixture/binding hashes changed; their existing assertions, stored
final-state hashes, and source-mutation descriptors remain unchanged. No other `family_*.json`,
kernel, optimizer, Pine, Bridge, schema, contract, or existing parity-corpus file was touched. The
existing 858-event companion corpus remains referenced by family 1 at Git blob OID
`31bdafae4d4d94787508043e9681874f9dc43bda` and was not copied or modified.

### D026 status — UNEARNED for all 23 built families

The 23 pairs previously reported as per-family mutation evidence are only **fixture-contract
self-consistency checks**. The verifier copies the expected mapping, substitutes the fixture's GF
field-8 value at one declared path, observes that the two mappings differ, restores the expected
value, and observes byte identity. That proves the comparison seam notices one changed datum. It
does not execute a producer, an exact pre-fix implementation, or an equivalent producer mutation.

**D026 therefore remains UNEARNED for all 23 built families.** GF field 8 names source mutations,
but the canonical kernel subjects they target arrive later in WP-P0-11, WP-P0-12, and WP-P0-20.
D026 can be earned only when those subjects exist and each exact pre-fix behaviour (or equivalent
producer mutation) is demonstrated to fail, followed by a passing execution with the fix present.
This is not partial satisfaction: `earned=0`, `unearned=23`.

### Hash, coherence, and citation limits

The per-fixture semantic and authority-content hashes are stored in `manifest.json`, in the same
tree as the fixtures. They detect an ordinary fixture/manifest mismatch, but they are not an
external trust anchor: a coordinated fixture edit plus recomputation of both manifest hashes is
not detected unless an independent coherence check rejects it.

At audited fixed point `c05e5968`, `validate_coherence` covered only families 4, 5, 22, and 24:
**24 of 230 expected values**, leaving **206** outside coherence validation. This repair does not
extend `validate_coherence`. The 11 new coverage assertions make the current scope **24 of 241**,
leaving **217** outside coherence validation. A self-consistent rehash outside those 24 values is
not detected. Named follow-up **`WP-P0-10-COHERENCE-217`** is to design and add independent
semantic/coherence validation for those 217 current values (the audited 206-value gap plus the 11
assertions added here).

The citation counter is now `citation_line_ranges_validated`. Its final value, 381, proves only
that those 381 ranges are well formed, exist, and carry a structurally matching C/GF,
cross-cutting-rule, or explicit-non-decision label. It does **not** prove that a row is relevant to,
or decides, the assertion carrying it. Renaming was chosen over a binding rule because the corpus
has no sound machine-readable family-to-deciding-row relevance map from which such a rule could be
derived in this repair.

The counters were renamed so no downstream consumer can mistake local dictionary comparison for
mutation evidence:

- old `red=` → `contract_mismatch_detected=`;
- old `restored=` / `green=` → `contract_match_restored=`;
- the summary now also emits `d026_earned=0 d026_unearned=23`.

## 2. All 25 families and authority

| # | Fixed family name | Status / fixture | Deciding WP-P0-09 rows |
|---:|---|---|---|
| 1 | Entry signal | **BUILT** — `fixtures/family_01.json` | C01/GF-01 `:131-141`; C42/GF-42 `:1222-1270` |
| 2 | Direction / flip / regime lock | **BUILT** — `fixtures/family_02.json` | C05/GF-05 `:227-237`; C21/GF-21 `:606-616`; C32/GF-32 `:830-863`; C33/GF-33 `:871-886` |
| 3 | Position sizing | **BUILT** — `fixtures/family_03.json` | C07/GF-07 `:291-316`; C31/GF-31 `:812-822` |
| 4 | Contract multiplier | **BUILT** — `fixtures/family_04.json` | C08/GF-08 `:324-334` |
| 5 | Minimum notional | **BUILT** — `fixtures/family_05.json` | C09/GF-09 `:342-352` |
| 6 | Rounding / qty step / min qty | **BUILT** — `fixtures/family_06.json` | C09/GF-09 `:342-352`; C31/GF-31 `:812-822` |
| 7 | SL calculation (ATR / percent / swing) | **BUILT** — `fixtures/family_07.json` | C11/GF-11 `:411-421`; C24/GF-24 `:660-670` |
| 8 | TP calculation (ATR / percent / R) | **BUILT** — `fixtures/family_08.json` | C12/GF-12 `:429-439`; C24/GF-24 `:660-670` |
| 9 | Multi-TP lifecycle incl. partial TP1 fill | **BUILT** — `fixtures/family_09.json` | C13/GF-13 `:447-457` |
| 10 | Break-even trigger and buffer | **BUILT** — `fixtures/family_10.json` | C14/GF-14 `:465-475`; C36/GF-36 `:938-964` |
| 11 | Trailing activation and monotonicity | **BUILT** — `fixtures/family_11.json` | C15/GF-15 `:483-493`; C37/GF-37 `:972-987` |
| 12 | Opposite-signal exit | **BUILT** — `fixtures/family_12.json` | C05/GF-05 `:227-237`; C16/GF-16 `:501-511`; C21/GF-21 `:606-616` |
| 13 | Time exit (bars / EOD / EOW) | **BUILT** — `fixtures/family_13.json` | C17/GF-17 `:519-529`; C25/GF-25 `:678-688` |
| 14 | Bar gaps through the stop | **BUILT** — `fixtures/family_14.json` | C11/GF-11 `:411-421`; C20/GF-20 `:575-598` |
| 15 | Same-bar SL/TP collision | **BUILT** — `fixtures/family_15.json` | C19/GF-19 `:557-567` |
| 16 | Pyramiding / add / partial reduction | **BUILT** — `fixtures/family_16.json` | C06/GF-06 `:245-281`; C13/GF-13 `:447-457` |
| 17 | Fees, slippage, funding | **BUILT** — `fixtures/family_17.json` | C08/GF-08 `:324-334`; C22/GF-22 `:624-634` |
| 18 | Snapshot drift / bucket-capital divergence | **BLOCKED — UNBUILT** | explicit non-decision `:1282-1287` |
| 19 | Allocator ↔ Guardian boundary | **BLOCKED — UNBUILT** | C07/GF-07 `:291-316`; explicit non-decision `:1282-1287` |
| 20 | Short-side symmetry | **BUILT** — `fixtures/family_20.json` | C24/GF-24 `:660-670`; cross-cutting rule 2 `:1274-1276` |
| 21 | NaN / zero / boundary precision | **BUILT** — `fixtures/family_21.json` | C07/GF-07 `:291-316`; C09/GF-09 `:342-352`; C24/GF-24 `:660-670` |
| 22 | Duplicate and reordered bars | **BUILT** — `fixtures/family_22.json` | C26/GF-26 `:696-706` |
| 23 | Cancellation and revision ordering | **BUILT** — `fixtures/family_23.json` | C26/GF-26 `:696-706` |
| 24 | `OrderIntent` idempotence | **BUILT** — `fixtures/family_24.json` | C26/GF-26 `:696-706` |
| 25 | Venue and session edge cases | **BUILT** — `fixtures/family_25.json` | C09/GF-09 `:342-352`; C17/GF-17 `:519-529`; C22/GF-22 `:624-634`; C25/GF-25 `:678-688`; C27/GF-27 `:716-738` |

Families 18 and 19 remain blocked and unbuilt. No `family_18.json` or `family_19.json` exists,
and this repair does not attempt to decide their missing `SNAPSHOT_MISMATCH` or
`REFERENCE_DIVERGENCE` semantics.

Family 18 is the brief's specified snapshot-drift D026 case, so its absence is a **genuine D026
coverage hole**. It is not cosmetic, not waived, and remains blocked on the exact upstream semantic
decision recorded in the manifest.

## 3. What the 23 declared pairs actually check

The following values are retained as GF field-8 **source-mutation descriptors**. The local
verifier exercises them only by substituting the candidate value into a copy of the expected
mapping. Every row below therefore has the same limited meaning: one fixture-contract mismatch is
detected at the named path, and the contract matches byte-for-byte after restoration.

| # | Stored descriptor exercised against copied expected mapping |
|---:|---|
| 1 | `producer.bar4.raw`: `NONE → LONG` |
| 2 | `events.bar2`: `NONE → ENTER_SHORT` |
| 3 | `request.has_snapshot_id`: `false → true` |
| 4 | `resolution.proposed_qty`: `2 → 20` |
| 5 | `decision.outcome`: `REJECT → ACCEPT` |
| 6 | `round.quantity`: `1.23 → 1.239` |
| 7 | `swing.long.stop`: `97.00 → 90.00` |
| 8 | `missing_stop.outcome`: `BLOCK → TARGET_AT_102.00` |
| 9 | `fills.tp1.qty`: `4 → 10` |
| 10 | `canonical.exit_bar`: `3 → 2` |
| 11 | `canonical.stop_effective_bar`: `2 → 1` |
| 12 | `priority.filter_without_stop_or_opposite`: `ma_filter → htf_trend_filter` |
| 13 | `eod_exit.timestamp`: `2026-01-02T21:45:00Z → 2026-01-05T00:00:00Z` |
| 14 | `fills.long_stop_gap`: `90.00 → 91.00` |
| 15 | `stop_first.fill`: `95.00 → 105.00` |
| 16 | `events.bar5`: `BLOCK:POST_EXIT_COOLDOWN → ENTER_LONG:1@100.00` |
| 17 | `pnl.net`: `17.5599 → 18.00` |
| 20 | `mirror.family_07.stop`: `105.00 → 95.00` |
| 21 | `adx.exact_25`: `BLOCK:adx_filter → PASS` |
| 22 | `duplicate.intent_count`: `1 → 2` |
| 23 | `revision.accepted`: `2 → 1` |
| 24 | `economic_effects.count`: `1 → 2` |
| 25 | `freshness.age_45_001`: `MISSED_DECISION_STALE:NO_ORDER → AGING:ORDER` |

Clean verifier command:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\verify_fixtures.py MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures C:\tmp\wp_p010_adfix_baseline_20260825
```

Real summary:

```text
SUMMARY built=23 blocked=2 fixture_manifest_hashes_matched=23 citation_line_ranges_validated=381 coherence_families=04,05,22,24 coherence_expected_values_validated=24 expected_values_total=241 contract_mismatch_detected=23 contract_match_restored=23 d026_earned=0 d026_unearned=23
```

The two per-family lines are now `FIXTURE_CONTRACT_MISMATCH_DETECTED` and
`FIXTURE_CONTRACT_MATCH_RESTORED`. No output calls them mutation failure/passing evidence.

## 4. Verifier repair

`fixtures/verify_fixtures.py` now:

1. uses explicit `VerificationError` gates throughout; it contains no language-level assertion gate;
2. exits immediately with `VERIFY_FAIL reason=python_optimization_forbidden __debug__=false` under optimized Python;
3. rejects duplicate JSON keys and non-JSON constants;
4. validates the exact 25-entry manifest, 23/2 family partition, blocked evidence, and exact fixture file set;
5. reads the authority document and verifies its LF-normalized SHA-256 (`422f4577…dae16`);
6. validates 381 cited line ranges for syntax, existence, and structural label/range agreement,
   without claiming relevance to the assertion carrying each citation;
7. recomputes the manifest-local semantic fixture hash and authority-content hash for every built
   fixture, without claiming those same-tree hashes reject a coordinated edit plus rehash;
8. recomputes the normalized expected-output and final-state hashes;
9. accounts for exactly 241 expected values; and
10. checks independent arithmetic/coherence relationships for 24 expected values in families 4,
    5, 22, and 24 only.

The other 217 expected values remain outside independent coherence validation. Hash agreement for
those values proves self-consistency with the current manifest, not semantic authority under a
self-consistent rehash.

Outputs are written only after the complete corpus validates, so a rejected later family does not
leave a newly rendered partial result set.

## 5. Executable regression falsification for the verifier repairs

The committed harness is `fixtures/test_verify_fixtures.py`. It copies the corpus to isolated
temporary directories, applies each exact tamper, recomputes the fixture-internal hashes where the
auditor did so, executes the selected verifier as a subprocess, and requires every invalid corpus
to return nonzero.

### 5.1 Exact pre-repair behaviour at `306d8172` — regression harness fails

The old verifier's source content was extracted from Git to
`C:\tmp\wp_p010_verify_fixtures_306d8172.py`, then run through the new regression harness:

```powershell
$oldPath='C:\tmp\wp_p010_verify_fixtures_306d8172.py'
$source = git show '306d8172:MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_10_GOLDEN_SUITE_2026-08-25/fixtures/verify_fixtures.py'
[System.IO.File]::WriteAllText($oldPath, (($source -join "`n") + "`n"), [System.Text.UTF8Encoding]::new($false))
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\test_verify_fixtures.py --verifier $oldPath
```

Real output (command exit `1`):

```text
BASELINE rc=0 clean=true detail=no_named_rejection
TAMPER name=family_04_bug_value optimized=false rc=0 rejected=false detail=no_named_rejection
TAMPER name=family_06_fabricated_citations optimized=false rc=0 rejected=false detail=no_named_rejection
TAMPER name=family_04_incoherent_risk optimized=false rc=0 rejected=false detail=no_named_rejection
TAMPER name=family_05_incoherent_accept optimized=false rc=0 rejected=false detail=no_named_rejection
TAMPER name=family_24_duplicate_effects optimized=false rc=0 rejected=false detail=no_named_rejection
TAMPER name=manifest_built_count_normal optimized=false rc=1 rejected=true detail=unnamed_nonzero_rejection
TAMPER name=manifest_built_count_optimized optimized=true rc=0 rejected=false detail=no_named_rejection
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=1/7 result=FAIL
```

This is the executed falsification of the exact pre-repair verifier. Six invalid states were still
accepted; only the ordinary, non-optimized count corruption happened to return nonzero.

### 5.2 Repaired verifier — all seven tamper cases reject

Command:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\test_verify_fixtures.py
```

Real output (command exit `0`):

```text
BASELINE rc=0 clean=true detail=no_named_rejection
TAMPER name=family_04_bug_value optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=04 coherence=proposed_qty expected=2.00 actual=20
TAMPER name=family_06_fabricated_citations optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=citation_range_out_of_bounds citation=MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/CAPABILITY_CANONICALIZATION_TABLE.md:99999-99999 (C99/GF-99) authority_lines=1290
TAMPER name=family_04_incoherent_risk optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=04 coherence=per_unit_risk expected=50 actual=25
TAMPER name=family_05_incoherent_accept optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=05 coherence=minimum_notional_outcome expected=REJECT actual=ACCEPT
TAMPER name=family_24_duplicate_effects optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=24 coherence=economic_effects_count expected=1 actual=2
TAMPER name=manifest_built_count_normal optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=manifest_built_count expected=23 actual=22
TAMPER name=manifest_built_count_optimized optimized=true rc=1 rejected=true detail=VERIFY_FAIL reason=python_optimization_forbidden __debug__=false
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=7/7 result=PASS
```

No reported tamper still passes. The family-04 case reproduces the auditor's exact bug value
(`proposed_qty=20`), inverted descriptor polarity, and recomputed internal output/state hashes.
The family-06 case reproduces the nonexistent `:99999-99999 (C99/GF-99)` citation. The remaining
three data cases reproduce the contradictory risk, minimum-notional, and duplicate-effect states.
The manifest count corruption rejects under both ordinary Python and optimized Python; optimized
mode rejects before reading the corrupt manifest.

This executed fail-before/pass-after evidence applies to the verifier defects repaired in this
round. It does **not** upgrade the 23 economic fixtures to D026 evidence.

## 6. Counts, determinism, scope, and handoff

Final family counts remain **23 BUILT, 2 BLOCKED, 25 TOTAL**. Built family numbers are
`1..17,20..25`; blocked numbers are exactly `18,19`. The expected-value count is now 241: the
audited 230 plus 11 added completeness assertions, with zero previously accepted values changed.

The clean verifier still renders 23 canonical output files. Two independent final processes and a
byte comparison are run again in Gate 4 before the repair commit. The exact result is recorded in
the final self-QA addendum below; no deterministic-kernel claim is made because no kernel runs.

Protected-surface impact: none. Pine, MTC strategy behaviour, TradingView parity, kernel, optimizer,
Bridge, schemas, broker/exchange code, hosts, credentials, and deployments are untouched.

The required T0 dual-flagship re-audit belongs to the live Claude Lead after this implementer
handoff. No audit, merge, or acceptance claim is issued here. The branch push is explicitly
required by the repair brief and occurs only after the scoped commit and final self-QA.

## 7. Final Gate-4 self-QA addendum

The following is real output from the completed repair, not a command template.

Compilation used `py_compile.compile(..., doraise=True)` for both Python files, with generated
bytecode directed to `C:\tmp` rather than the worktree. Strict JSON parsing enumerated the one
manifest and all 23 family files and invoked `python -m json.tool` on every path.

```text
PY_COMPILE=PASS
JSON_FILES=24/24 PASS
RUFF=NOT_INSTALLED
```

Complete verifier runs:

```text
python fixtures/verify_fixtures.py fixtures C:\tmp\wp_p010_adfix2_complete_run1_20260825
python fixtures/verify_fixtures.py fixtures C:\tmp\wp_p010_adfix2_complete_run2_20260825
SUMMARY built=23 blocked=2 fixture_manifest_hashes_matched=23 citation_line_ranges_validated=381 coherence_families=04,05,22,24 coherence_expected_values_validated=24 expected_values_total=241 contract_mismatch_detected=23 contract_match_restored=23 d026_earned=0 d026_unearned=23
SUMMARY built=23 blocked=2 fixture_manifest_hashes_matched=23 citation_line_ranges_validated=381 coherence_families=04,05,22,24 coherence_expected_values_validated=24 expected_values_total=241 contract_mismatch_detected=23 contract_match_restored=23 d026_earned=0 d026_unearned=23
OUTPUT_FILES_RUN1=23
OUTPUT_FILES_RUN2=23
BYTE_IDENTICAL=23/23
MISMATCHES=0
STDOUT_IDENTICAL=true
```

Committed regression harness:

```text
python fixtures/test_verify_fixtures.py
BASELINE rc=0 clean=true detail=no_named_rejection
TAMPER name=family_04_bug_value optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=04 coherence=proposed_qty expected=2.00 actual=20
TAMPER name=family_06_fabricated_citations optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=citation_range_out_of_bounds citation=MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/CAPABILITY_CANONICALIZATION_TABLE.md:99999-99999 (C99/GF-99) authority_lines=1290
TAMPER name=family_04_incoherent_risk optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=04 coherence=per_unit_risk expected=50 actual=25
TAMPER name=family_05_incoherent_accept optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=05 coherence=minimum_notional_outcome expected=REJECT actual=ACCEPT
TAMPER name=family_24_duplicate_effects optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=24 coherence=economic_effects_count expected=1 actual=2
TAMPER name=manifest_built_count_normal optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=manifest_built_count expected=23 actual=22
TAMPER name=manifest_built_count_optimized optimized=true rc=1 rejected=true detail=VERIFY_FAIL reason=python_optimization_forbidden __debug__=false
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=7/7 result=PASS
```

Retained round-1 hardening, executed on temporary copies after recomputing both fixture-internal and
manifest-local hashes for the family-04 tamper:

```text
RETENTION name=family_04_full_rehash rc=1 rejected=true detail=VERIFY_FAIL reason=family=04 coherence=proposed_qty expected=2.00 actual=20
RETENTION name=built_count_22 mode=python rc=1 rejected=true detail=VERIFY_FAIL reason=manifest_built_count expected=23 actual=22
RETENTION name=built_count_22 mode=python_-O rc=1 rejected=true detail=VERIFY_FAIL reason=python_optimization_forbidden __debug__=false
RETENTION name=built_count_22 mode=PYTHONOPTIMIZE_2 rc=1 rejected=true detail=VERIFY_FAIL reason=python_optimization_forbidden __debug__=false
```

Exact old-value preservation and added-coverage arithmetic:

```text
EXISTING_ASSERTIONS_UNCHANGED family=05 old=6 current=14 added=8 changed=0 result=PASS
ADDED_PATHS short_twin.decision.outcome,short_twin.decision.reason,short_twin.direction,short_twin.fills.count,short_twin.price,short_twin.quantity.floored,short_twin.quantity.notional,short_twin.state.order_emitted
EXISTING_ASSERTIONS_UNCHANGED family=16 old=13 current=16 added=3 changed=0 result=PASS
ADDED_PATHS basket.risk_at_shared_stop,events.bar2.stop_disposition,events.bar3
FAMILY_05_TWIN direction=SHORT reflected_price=8.0 fixture_price=8.0 notional=12.00 min_notional=20.0 below_min=true
FAMILY_16_COMPLETENESS normalized_bars=8 bar3_raw=NONE
FAMILY_16_SHARED_STOP_RISK equation=3*(295/3-95) result=10/1 decimal=10.00
```

Final scope and claim checks:

```text
CHANGED_FILES=6
FAMILY_FILES_CHANGED=2:MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_10_GOLDEN_SUITE_2026-08-25/fixtures/family_05.json,MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_10_GOLDEN_SUITE_2026-08-25/fixtures/family_16.json
PROTECTED_PATH_CHANGES=0
CLAIM_OVERSTATEMENT_HITS=0
ASSERT_GATES=0
VALIDATE_COHERENCE_BODY_CHANGED=0
FAMILY_18_FILE=ABSENT
FAMILY_19_FILE=ABSENT
GIT_DIFF_CHECK=PASS
REPO_GUARD=PASS branch=feature/wp-p0-10-golden-suite-20260825 protected=none risky_untracked=none
```

Temporary-copy limitation probes recomputed the changed fixture's output/state hashes and both
manifest-local hashes before executing the final verifier. Their clean acceptance is the evidence
for the narrowed claims, not a passing semantic-verification claim:

```text
LIMITATION name=family_17_self_consistent_rehash rc=0 accepted=true
SUMMARY built=23 blocked=2 fixture_manifest_hashes_matched=23 citation_line_ranges_validated=381 coherence_families=04,05,22,24 coherence_expected_values_validated=24 expected_values_total=241 contract_mismatch_detected=23 contract_match_restored=23 d026_earned=0 d026_unearned=23
LIMITATION name=family_10_irrelevant_citations replacements=9 rc=0 accepted=true
SUMMARY built=23 blocked=2 fixture_manifest_hashes_matched=23 citation_line_ranges_validated=381 coherence_families=04,05,22,24 coherence_expected_values_validated=24 expected_values_total=241 contract_mismatch_detected=23 contract_match_restored=23 d026_earned=0 d026_unearned=23
```

The family-10 probe replaces the eight break-even assertion citations plus the source-mutation
citation with structurally valid C08/GF-08 ranges. It demonstrates exactly why the counter cannot be
named or described as relevance/authority binding.

Python compilation, strict JSON parsing, the executable verifier, deterministic rendering, and the
tamper regression harness all ran successfully.

Regression-risk note: an ordinary one-sided authority, fixture, output-hash, or manifest-hash change
fails visibly. A coordinated rehash can still pass for the 217 values outside coherence validation;
that limitation is now explicit and assigned to `WP-P0-10-COHERENCE-217`. An intentional future
WP-P0-09/corpus revision must update the pinned self-consistency hashes in the same reviewed package.
There is no strategy/parity runtime risk because this lane is never imported by those runtimes.

**Gate-4 decision:** hand off to the live Claude Lead for the required independent T0 dual-flagship
re-audit. The implementer does not self-accept.

## 8. Owner-authorized AD-FIX3 — self-contained companion inputs

This bounded round starts from accepted HEAD
`d576cd42b6a360167180616ea093f8fa192b1e19`. The T0 three-round cap was already spent;
the owner explicitly authorized this additional repair on 2026-08-25. This implementer records
executed self-QA only and does not self-accept.

### 8.1 Per-fixture repair choice

All six fixtures use **option 1: embed the companion-row inputs in the fixture**. No shipped
assertion uses cross-row imports, and Round 4b supersedes this section by making any `cross_row*`
assertion field reject. These legacy arms are genuinely part of the named family, so carrying their
literal scenario inputs avoids preserving a hidden dependency on another row's prose.

| Fixture | Embedded deciding scenario | Assertions made self-contained | Why option 1 |
|---|---|---|---|
| `family_02.json` | C32/GF-32 config, metadata, and six literal bars | all five `legacy.*reentry*` paths, including bar 3 open `99.00`, bar 4 close `100.00`, and bar 5 close `100.00` | The five retired re-entry modes are the family-2 legacy matrix; one shared six-bar scenario is their actual input. |
| `family_03.json` | C31/GF-31 precision modes, qty step `0.01`, raw quantity `1.234567` | `legacy_precision.off_qty`, `legacy_precision.research_qty` | Both quantities are native position-sizing companion arms over one raw quantity. |
| `family_06.json` | C31/GF-31 precision modes, qty step `0.01`, raw quantity `1.234567` | `legacy_precision.off`, `legacy_precision.research` | The same companion arithmetic directly tests family 6's rounding boundary. |
| `family_10.json` | C36/GF-36 legacy BE config, metadata, and five bars | the three `legacy.*.exit` assertions | The three break-even modes are the legacy half of the family-10 timing scenario. |
| `family_11.json` | C37/GF-37 legacy trailing config, metadata, and four bars | the three `legacy.*.exit` assertions | The three trailing modes are the legacy half of family 11 and share one literal bar sequence. |
| `family_14.json` | C20/GF-20 `LEGACY_CLOSE_ONLY` config, metadata, entry bar, and both adverse-gap bars | both `legacy.*_stop_close_only` assertions | The close-only rival is an explicit named execution profile in the same gap family. |

The companion records live at top-level `companion_scenarios`, separate from the executable primary
`config`, so provenance metadata cannot be mistaken for a kernel configuration key. Each record
names its deciding C/GF citation and maps every covered assertion to exact required input paths.

### 8.2 Targeted proof: no expected value changed

The comparison below loads every `family_*.json` from starting HEAD with `git show`, compares the
complete `path -> value` mapping to the worktree, and separately compares both stored expected-output
hashes. Real output:

```text
EXPECTED_PATH_VALUE_MAPS_UNCHANGED=23/23 changed=[]
EXPECTED_OUTPUT_AND_STATE_HASHES_UNCHANGED=46/46 changed=[]
```

**No asserted value changed.** The fixture edits are input/provenance additions only; the seven
changed `fixture_contract_sha256` values in `manifest.json` bind six companion-input additions plus
family 1's path-status metadata. Every pre-existing expected-output SHA and final-state SHA remains
byte-identical to `d576cd42`.

### 8.3 Assertion-input gate and falsified regression

Round 4b supersedes the automatic primary-source design recorded here. The current verifier requires
every expected assertion to have an explicit checked source: either fixture-local `input_paths` or
required paths inside an embedded companion scenario. Duplicate assignment, an unknown assertion, an
unsupported cross-row field, an undeclared assertion, or a missing/empty required input rejects
before fixture-hash comparison.

Current corpus accounting is bound to the manifest:

```text
assertion_input_sources_validated=241
assertion_input_paths_checked=2649
fixture_assertions_validated=224
companion_assertions_validated=17
```

The committed regression removes `family_03`'s research-mode config input, removes the
`legacy_precision.research_qty` companion assignment, and recomputes the manifest-local fixture
hash. The expected assertion remains. That coordinated rehash prevents the existing hash gate from
being mistaken for semantic coverage: the assertion's input is both absent and undeclared.

RED against the unchanged `d576cd42` verifier, before the gate was added:

```text
OLD_BASELINE rc=0 detail=no_named_rejection
OLD_TAMPER name=family_03_absent_undeclared_input rc=0 detail=no_named_rejection
RED_EXPECTATION expected_nonzero=true observed_rc=0 result=FAIL
```

GREEN with this repair:

```text
BASELINE rc=0 clean=true detail=no_named_rejection
TAMPER name=family_03_absent_undeclared_input optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=03 assertion_input_source_undeclared path=legacy_precision.research_qty
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=8/8 result=PASS
```

This is real D026 RED/GREEN closure evidence for the **verifier defect only**. It does not change the
23 economic fixture families' existing `D026 UNEARNED` status.

### 8.4 Measured coherence summary

`validate_coherence` now returns the exact expected paths it actually validated. The main verifier
derives the family set and value count from those returned sets, checks both against the manifest,
and prints the measured values. The old output literals at former lines 705-707 are gone.

Round 4b supersedes the exact final-summary lines previously recorded here; the live verifier now
prints a path-resolved input counter rather than the old presence counter. See the Round 4b section
below for the current two-run determinism transcript.

```text
current_summary_moved_to_round_4b=true
```

### 8.5 Family-1 companion path resolution

The prompt's claim that the path is absent from branch HEAD did not reproduce. Read-only checks at
`d576cd42` established all three identities:

```text
git ls-tree -r HEAD -- IBKR_PAPER_BRIDGE/tests/fixtures/golden_signals.json
100644 blob 31bdafae4d4d94787508043e9681874f9dc43bda  IBKR_PAPER_BRIDGE/tests/fixtures/golden_signals.json
COMPANION_WORKTREE_PRESENT=True
COMPANION_BLOB=31bdafae4d4d94787508043e9681874f9dc43bda
```

`family_01.json` therefore records the truthful status
`PRESENT_AT_BRANCH_HEAD_AND_WORKTREE` beside the existing exact path and blob OID. The corpus remains
referenced only; it was not copied or modified.

### 8.6 Final Gate-4 checks

Superseded by Round 4b and the Round 4b nit closure for tamper-regression counts; this is a
historical AD-FIX3 snapshot, not the current harness result.

```text
PY_COMPILE=PASS files=2
JSON_PARSE=PASS files=24/24
FIXTURE_MANIFEST_HASHES=23/23 bad=0
EXPECTED_PATH_VALUE_MAPS_UNCHANGED=23/23 changed=[]
EXPECTED_OUTPUT_AND_STATE_HASHES_UNCHANGED=46/46 changed=[]
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=8/8 result=PASS
PROTECTED_PATH_CHANGES=0
GIT_DIFF_CHECK=PASS
```

Families 18 and 19 remain blocked and absent. The coordinated-rehash limitation remains disclosed
and unchanged; this round does not attempt to close it. No Pine, parity, MTC strategy, Bridge,
schema, broker/exchange, host, credential, deployment, or live surface changed.

## 9. Git record

Original fixture corpus commit: `5ff870ee` (`test(wp-p0-10): add 23 cited golden fixtures`).

Repair-round-1 commit: `c05e596807534845d1665ef38b2e4b006f269089`.

Repair-round-2 starting commit: `c05e596807534845d1665ef38b2e4b006f269089`.

Owner-authorized AD-FIX3 starting commit: `d576cd42b6a360167180616ea093f8fa192b1e19`.

The exact repair commit SHA is printed as the last line of the implementer's final output. A tracked
report cannot contain the SHA of the same commit that contains it because inserting that SHA changes
the commit.

## Round 4b — the gate generalizes, and the companion inputs are real

Starting point: `1dcb70665b82df19350c207a83974dd4f738ec10` on
`feature/wp-p0-10-golden-suite-20260825`. This is implementer self-QA only; it is not an
accepting Gate-5 verdict.

### Gate design

The name-prefix gate is removed. Every assertion now needs one explicit checked source:

- Fixture-local assertions carry `input_paths`, and every path must resolve to a non-empty value in
  the same fixture JSON.
- Companion assertions are bound through `companion_scenarios[*].assertion_inputs`, and every path
  must resolve inside that literal companion run.
- Cross-row imports are unsupported in this corpus. Any assertion field whose name starts with
  `cross_row` rejects before hash comparison.
- The summary now separates source count from path count:
  `assertion_input_sources_validated=241`, `assertion_input_paths_checked=2649`,
  `fixture_assertions_validated=224`, `companion_assertions_validated=17`.

This is still an input-presence gate, not a semantic-relevance prover. A coordinated fixture and
manifest rehash can still replace a declared input with an unrelated present path; that remains the
disclosed coordinated-rehash limitation.

### B1 and B2 probes

Committed harness output for the four B1 probes and both B2 probes:

```text
TAMPER name=b1_family_12_empty_primary_inputs optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=12 assertion_input_presence_missing path=priority.stop_plus_opposite input=config.exit_on_htf_trend_block
TAMPER name=b1_family_03_renamed_companion_assertion optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=03 assertion_input_source_undeclared path=compat_precision.research_qty
TAMPER name=b1_family_01_missing_signal_mode optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=01 assertion_input_presence_missing path=producer.bar0.raw input=config.signal_mode
TAMPER name=b1_cross_row_misspelling optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=01 cross_row_import_unsupported field=cross_row_imprt path=producer.bar0.raw
TAMPER name=b2_family_03_cross_row_import optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=03 cross_row_import_unsupported field=cross_row_import path=legacy_precision.research_qty
TAMPER name=b2_family_14_cross_row_imports optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=14 cross_row_import_unsupported field=cross_row_import path=legacy.long_stop_close_only
```

The old round-4 P2b shape using `tw_qty_precision_mode` is now obsolete because family 03 uses the
actual C31 selector, `tw_audit_semantics_mode`. Running the old-shape tamper against the current
verifier still rejects at the selector gate:

```text
B1_P2B_OLDSHAPE rc=1 detail=VERIFY_FAIL reason=family=03 companion_selector_mismatch path=legacy_precision.off_qty selector=tw_audit_semantics_mode expected=off actual=None
```

### Family 20

`family_20.json` now embeds `mirror_expected_values` for the 14 already reflected mirror outputs.
The verifier presence-checks these local values but does not derive them by applying `config.rule`
or `config.reflection_pivot`. Its mirror assertions reference those local values through
`input_paths`, so the family no longer passes with only `reflection_pivot`, `rule`, and an empty bar
list.

```text
TAMPER name=b3_family_20_missing_mirror_expected_value optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=20 assertion_input_presence_missing path=mirror.family_03.qty input=mirror_expected_values.family_03.qty
```

### Companion selectors

The invented selector names are gone from shipped fixtures. The literal companion runs now carry
the actual singular selectors:

```text
family_02: tw_reversal_reentry_mode = local | carry_to_next_bar_after_protective_exit | next_bar_open_after_protective_exit_signal | next_bar_close_after_protective_exit_signal | delay_after_protective_exit
family_03: tw_audit_semantics_mode = off | research
family_06: tw_audit_semantics_mode = off | research
family_10: tw_be_semantics_mode = local | next_bar_confirmed | tradingview
family_11: tw_trailing_semantics_mode = local | tradingview | next_bar_confirmed
```

The selector regression reintroduces the family-02 plural key and is rejected:

```text
TAMPER name=b4_family_02_plural_selector optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=02 companion_selector_mismatch path=legacy.local.reentry_bar selector=tw_reversal_reentry_mode expected=local actual=None
```

No expected value moved:

```text
expected_path_value_maps_unchanged=23/23 changed=[]
output_hashes_unchanged=23/23 changed=[]
state_hashes_unchanged=23/23 changed=[]
```

All 23 `fixture_contract_sha256` values moved because every built fixture now carries explicit
input declarations. The 46 output/state hashes are unchanged.

### Optimization matrix

```text
verifier plain: rc=0 SUMMARY built=23 blocked=2 fixture_manifest_hashes_matched=23 citation_line_ranges_validated=397 coherence_families=04,05,22,24 coherence_expected_values_validated=24 assertion_input_sources_validated=241 assertion_input_paths_checked=2649 fixture_assertions_validated=224 companion_assertions_validated=17 expected_values_total=241 contract_mismatch_detected=23 contract_match_restored=23 d026_earned=0 d026_unearned=23
verifier -O: rc=1 VERIFY_FAIL reason=python_optimization_forbidden __debug__=false
verifier PYTHONOPTIMIZE=2: rc=1 VERIFY_FAIL reason=python_optimization_forbidden __debug__=false
harness plain: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=19/19 result=PASS
harness -O: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=19/19 result=PASS
harness PYTHONOPTIMIZE=2: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=19/19 result=PASS
```

The harness strips ambient `PYTHONOPTIMIZE` for nominal child verifier runs and applies optimization
only to the explicit optimized child case.

### D026-style falsification for the verifier test

The old committed test deleted both the field and the mapping. The current harness adds a direct
field-presence branch for family 03. A pre-fix verifier from `1dcb7066` accepts the missing primary
input after the fixture hash is recomputed; the current verifier rejects it by name:

```text
old_1dcb7066 rc=0 detail=no_named_rejection
current_worktree rc=1 detail=VERIFY_FAIL reason=family=03 assertion_input_presence_missing path=request.accepted input=config.entry_reference_price
```

The companion literal-input branch is also committed:

```text
TAMPER name=b6_family_03_missing_literal_input optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=03 assertion_input_presence_missing path=legacy_precision.research_qty input=literal_inputs.raw_quantity
```

This proves the verifier regression, not economic D026 for the 23 families; their manifest status
remains `D026 UNEARNED`.

### Contract and grep

`fixtures/README.md`, `fixtures/manifest.json`, and the earlier AD-FIX3 report section now describe
the current input-source contract. Repo-wide stale-claim grep:

```text
rg -n <stale round-4 contract phrase set> C:\WPP010_20260825
rc=1 no output
```

The old selector-name grep in the lane now finds only the deliberate plural-selector tamper in
`test_verify_fixtures.py`.

### Discrimination and invented tamper

Every committed new-gate RED mutates one temporary fixture copy and rejects on the named target
family before hash comparison. These were target-fixture-only probes, not cross-applied
discrimination counts:

```text
B1 family12 empty inputs: target=12 target_fixture_only=true cross_applied=false
B1 family03 renamed assertion: target=03 target_fixture_only=true cross_applied=false
B1 family01 missing signal_mode: target=01 target_fixture_only=true cross_applied=false
B1 misspelled cross_row_imprt: target=01 target_fixture_only=true cross_applied=false
B2 family03 cross_row_import: target=03 target_fixture_only=true cross_applied=false
B2 family14 cross_row_import: target=14 target_fixture_only=true cross_applied=false
B3 family20 missing mirror operand: target=20 target_fixture_only=true cross_applied=false
B4 family02 plural selector: target=02 target_fixture_only=true cross_applied=false
B6 family03 missing literal input: target=03 target_fixture_only=true cross_applied=false
B6 family03 missing primary input: target=03 target_fixture_only=true cross_applied=false
```

Invented tamper not listed in the prompt: delete `family_03.config.entry_reference_price`, retain
the assertion declaration, and recompute the fixture hash. Outcome:

```text
TAMPER name=b6_family_03_missing_primary_input optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=03 assertion_input_presence_missing path=request.accepted input=config.entry_reference_price
```

The disputed unrelated-but-present path item was tested separately:

```text
UNRELATED_PRESENT_PATH_PROBE rc=0 accepted=true detail=no_named_rejection
SUMMARY built=23 blocked=2 fixture_manifest_hashes_matched=23 citation_line_ranges_validated=397 coherence_families=04,05,22,24 coherence_expected_values_validated=24 assertion_input_sources_validated=241 assertion_input_paths_checked=2629 fixture_assertions_validated=224 companion_assertions_validated=17 expected_values_total=241 contract_mismatch_detected=23 contract_match_restored=23 d026_earned=0 d026_unearned=23
```

Ruling: this is the disclosed coordinated-rehash limitation, not a separate in-scope repair. The
input gate proves existence of declared fixture paths; it cannot prove arithmetic relevance after an
author rewrites the declaration and the same-tree manifest hash together. The manifest and README now
say that explicitly.

### Final checks

```text
python -m py_compile ...verify_fixtures.py ...test_verify_fixtures.py
rc=0
python ...verify_fixtures.py ...fixtures C:\tmp\wp_p010_r4b_det_1
python ...verify_fixtures.py ...fixtures C:\tmp\wp_p010_r4b_det_2
VERIFY_RUNS_RC=0,0
OUTPUT_FILES=23,23
BYTE_IDENTICAL=23/23 MISMATCHES=[]
STDOUT_IDENTICAL=true
git diff --check
rc=0
```

Families 18 and 19 remain blocked and absent. No Pine, parity, MTC strategy behavior, Bridge
runtime, schema, broker/exchange, host, credential, deployment, or live surface changed.

Not closed here: independent acceptance is still for the Lead/auditors, and the coordinated-rehash
semantic-relevance limitation remains disclosed and out of scope.

## Round 4b nit closure

Starting point: `6c01c0eb` on `feature/wp-p0-10-golden-suite-20260825`. This is implementer
self-QA for the five PASS-WITH-NITS items only; it is not self-acceptance.

### N-1 - optimized harness case has mutation power

Changed `fixtures/test_verify_fixtures.py` case 17,
`manifest_built_count_optimized`, to require the named reason
`VERIFY_FAIL reason=python_optimization_forbidden`. I also deleted the unused `optimize_env`
parameter from `run_verifier`; no dead parameter now implies extra coverage. This was a
regression-coverage hole only: the committed verifier already rejected optimized Python directly.

Crippled-verifier proof, made from a scratch copy with the `__debug__` guard removed:

```text
CRIPPLED_GUARD_HITS=0
CRIPPLED_DIRECT_O rc=0 SUMMARY built=23 blocked=2 fixture_manifest_hashes_matched=23 citation_line_ranges_validated=397 coherence_families=04,05,22,24 coherence_expected_values_validated=24 assertion_input_sources_validated=241 assertion_input_paths_checked=2649 fixture_assertions_validated=224 companion_assertions_validated=17 expected_values_total=241 contract_mismatch_detected=23 contract_match_restored=23 d026_earned=0 d026_unearned=23
CRIPPLED_HARNESS rc=1
TAMPER name=manifest_built_count_optimized optimized=true rc=1 rejected=false detail=VERIFY_FAIL reason=manifest_built_count expected=23 actual=22
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=18/19 result=FAIL
```

Case 17 now fails on the crippled scratch verifier because it no longer accepts any nonzero as
enough. With the real verifier restored, the expanded harness passes 19/19; the extra two cases are
the N-2 and N-4 regressions below.

### N-2 - OHLCV list length pinned

Changed `fixtures/verify_fixtures.py` to validate every `normalized_bars[*].ohlcv` list against the
local `frozen_metadata.ohlcv_fields` declaration `open,high,low,close,volume`. I chose the
frozen-metadata shape route instead of adding per-path length declarations because it pins the bar
schema once per fixture or companion run and covers every indexed OHLCV path without expanding 2649
input-path entries.

All fixture or companion containers that actually carry OHLCV arrays now declare that shape. The
auditor's INV-1 class, deleting a companion OHLCV close from family 10 after rehash, is now rejected
by name:

```text
TAMPER name=n2_family_10_companion_ohlcv_close_deleted optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=10 normalized_bar_ohlcv_length_mismatch context=companion:C36_GF36_legacy_break_even_modes__local index=3 expected=5 actual=4
```

### N-3 - mirror values disclosed honestly

Chose option (b): rename the stored family-20 field to `mirror_expected_values` and disclose exactly
what it is. This is the narrow nit-closure repair: deriving real long-side operands would require new
arithmetic rules, including non-price PnL cases, outside this passing-property closure. No expected
value moved.

`fixtures/README.md` and `fixtures/manifest.json` now state that family 20 stores already reflected
outputs, presence-checked but not derived by applying `config.rule` or `config.reflection_pivot`.
Repo/package grep has no remaining hits for the previous `mirror_` + `operands` field token:

```text
$old = "mirror_" + "operands"
rg -n $old -S MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25
rc=1 no output
```

The family-20 tamper now follows the truthful field name:

```text
TAMPER name=b3_family_20_missing_mirror_expected_value optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=20 assertion_input_presence_missing path=mirror.family_03.qty input=mirror_expected_values.family_03.qty
```

### N-4 - selector-bound assertions cannot opt out

Changed the fixture-local assertion branch to reject any assertion path listed in
`COMPANION_SELECTOR_REQUIREMENTS`. Moving a selector-bound assertion out of its companion scenario
now fails before counter accounting can hide it:

```text
TAMPER name=n4_family_02_selector_rehomed_fixture_local optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=02 companion_selector_fixture_local_forbidden path=legacy.local.reentry_bar
```

### N-5 - stale counts marked and scanned

Added a supersession marker to section 8.6 naming Round 4b and this nit closure. I also scanned the
lane package for other count-bearing snapshots. The historical 381-count and 7/7 snapshots remain in
earlier repair sections as executed history; section 8.3 and 8.5 already had Round 4b supersession
markers; section 8.6 now has one; the Round 4b matrix was updated from 17/17 to the current 19/19.

Relevant grep commands:

```text
rg -n "tamper_rejected=[0-9]+/[0-9]+|assertion_input_paths_checked=[0-9]+|companion_assertions_validated=[0-9]+|fixture_assertions_validated=[0-9]+|citation_line_ranges_validated=[0-9]+|expected_values_total=[0-9]+|contract_mismatch_detected=[0-9]+|contract_match_restored=[0-9]+" -S MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\LANE_REPORT.md MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\README.md MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\manifest.json
$old = "mirror_" + "operands"; rg -n $old -S MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25
```

### Final checks

```text
python -m py_compile ...verify_fixtures.py ...test_verify_fixtures.py
rc=0
JSON_PARSE=PASS files=24/24
EXPECTED_PATH_VALUE_MAPS_UNCHANGED=23/23 changed=[]
EXPECTED_OUTPUT_AND_STATE_HASHES_UNCHANGED=46/46 changed=[]
verifier plain: rc=0 SUMMARY built=23 blocked=2 fixture_manifest_hashes_matched=23 citation_line_ranges_validated=397 coherence_families=04,05,22,24 coherence_expected_values_validated=24 assertion_input_sources_validated=241 assertion_input_paths_checked=2649 fixture_assertions_validated=224 companion_assertions_validated=17 expected_values_total=241 contract_mismatch_detected=23 contract_match_restored=23 d026_earned=0 d026_unearned=23
verifier -O: rc=1 VERIFY_FAIL reason=python_optimization_forbidden __debug__=false
verifier PYTHONOPTIMIZE=2: rc=1 VERIFY_FAIL reason=python_optimization_forbidden __debug__=false
harness plain: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=19/19 result=PASS
harness -O: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=19/19 result=PASS
harness PYTHONOPTIMIZE=2: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=19/19 result=PASS
VERIFY_RUNS_RC=0,0
OUTPUT_FILES=23,23
BYTE_IDENTICAL=23/23 MISMATCHES=[]
STDOUT_IDENTICAL=true
git diff --check
rc=0
```

Families 18 and 19 remain blocked and absent. No Pine, parity, MTC strategy behavior, Bridge runtime,
schema, broker/exchange, host, credential, deployment, or live surface changed.

## Round 4c

Starting point: `88d4180c` on `feature/wp-p0-10-golden-suite-20260825`. This is implementer
self-QA for the second flagship's five required findings; it is not self-acceptance.

### R1 - C32/C36/C37 master gates are declared and enforced

Changed `fixtures/verify_fixtures.py` to require the source-row master gate
`config.tw_audit_semantics_mode` for the C32, C36, and C37 companion assertions. The affected
fixtures now declare that input path explicitly, and the verifier checks the scenario value is
`research` before ordinary input presence/count accounting. `manifest.json` was updated for the
three moved fixture-contract hashes and `assertion_input_path_count=2660`.

Executed RED/GREEN:

```text
BASELINE rc=0 clean=true detail=no_named_rejection
TAMPER name=r1_family_02_c32_master_gate_deleted optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=02 master_gate_mismatch path=legacy.local.reentry_bar input=config.tw_audit_semantics_mode expected=research actual=None
TAMPER name=r1_family_10_c36_master_gate_deleted optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=10 master_gate_mismatch path=legacy.local.exit input=config.tw_audit_semantics_mode expected=research actual=None
TAMPER name=r1_family_11_c37_master_gate_deleted optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=11 master_gate_mismatch path=legacy.local.exit input=config.tw_audit_semantics_mode expected=research actual=None
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=27/27 result=PASS
```

### R2 - bar granularity pinned

Changed the normalized-bar validator to enforce hardcoded OHLCV bar counts for declared OHLCV
contexts, per-bar `ohlcv` presence, five-field OHLCV shape, and `index == position` for indexed
OHLCV sequences. The bar counts live in verifier constants, so a fixture-local metadata edit cannot
legalize a short sequence.

Executed RED/GREEN:

```text
BASELINE rc=0 clean=true detail=no_named_rejection
TAMPER name=r2_family_10_companion_ohlcv_key_deleted optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=10 normalized_bar_ohlcv_missing context=companion:C36_GF36_legacy_break_even_modes__local index=1
TAMPER name=r2_family_10_companion_bar_deleted optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=10 normalized_bar_count_mismatch context=companion:C36_GF36_legacy_break_even_modes__local expected=5 actual=4
TAMPER name=r2_family_10_companion_bars_reordered optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=10 normalized_bar_index_mismatch context=companion:C36_GF36_legacy_break_even_modes__local position=1 actual=2
TAMPER name=r2_family_10_companion_bar_index_scrambled optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=10 normalized_bar_index_mismatch context=companion:C36_GF36_legacy_break_even_modes__local position=2 actual=99
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=27/27 result=PASS
```

### R3 - malformed normalized-bar members reject

The validator no longer filters to already-valid dictionary bars with `ohlcv`; for declared OHLCV
contexts, each member is checked in place and malformed members fail by name.

```text
TAMPER name=r3_family_10_companion_bar_not_object optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=10 normalized_bar_not_object context=companion:C36_GF36_legacy_break_even_modes__local index=2
```

### R4 - executable RED for N-2 and N-4

The missing D026-style RED was supplied with the `6c01c0eb` verifier extracted to a temp file:

```text
cmd /c "git show 6c01c0eb:MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_10_GOLDEN_SUITE_2026-08-25/fixtures/verify_fixtures.py > C:\tmp\wp_p010_old_verify_6c01c0eb.py"
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\test_verify_fixtures.py --verifier C:\tmp\wp_p010_old_verify_6c01c0eb.py | Select-String -Pattern 'BASELINE|n2_family_10_companion_ohlcv_close_deleted|n4_family_02_selector_rehomed_fixture_local|VERIFIER_REGRESSION_SUMMARY'

BASELINE rc=0 clean=true detail=no_named_rejection
TAMPER name=n2_family_10_companion_ohlcv_close_deleted optimized=false rc=0 rejected=false detail=no_named_rejection
TAMPER name=n4_family_02_selector_rehomed_fixture_local optimized=false rc=0 rejected=false detail=no_named_rejection
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=16/27 result=FAIL
```

Current GREEN for those same committed cases:

```text
TAMPER name=n2_family_10_companion_ohlcv_close_deleted optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=10 normalized_bar_ohlcv_length_mismatch context=companion:C36_GF36_legacy_break_even_modes__local index=3 expected=5 actual=4
TAMPER name=n4_family_02_selector_rehomed_fixture_local optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=02 companion_selector_fixture_local_forbidden path=legacy.local.reentry_bar
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=27/27 result=PASS
```

The N-4 tamper now updates manifest-local `companion_assertion_count` and
`assertion_input_path_count` in the temp copy, so a missing selector-local-forbidden check is not
masked by counter drift.

### R5 - cross-kill label corrected

The previous cross-kill-looking lines were relabelled in the historical section as
`target_fixture_only=true cross_applied=false`. No cross-application discrimination was claimed or
measured. The corrected number for those old probes is therefore: cross-applied mutations run `0`;
target-fixture-only probes listed `10`.

### Matrix and invariants

```text
python -m py_compile ...verify_fixtures.py ...test_verify_fixtures.py
rc=0

verifier plain: rc=0
SUMMARY built=23 blocked=2 fixture_manifest_hashes_matched=23 citation_line_ranges_validated=397 coherence_families=04,05,22,24 coherence_expected_values_validated=24 assertion_input_sources_validated=241 assertion_input_paths_checked=2660 fixture_assertions_validated=224 companion_assertions_validated=17 expected_values_total=241 contract_mismatch_detected=23 contract_match_restored=23 d026_earned=0 d026_unearned=23
verifier -O: rc=1
VERIFY_FAIL reason=python_optimization_forbidden __debug__=false
verifier PYTHONOPTIMIZE=2: rc=1
VERIFY_FAIL reason=python_optimization_forbidden __debug__=false
harness plain: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=27/27 result=PASS
harness -O: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=27/27 result=PASS
harness PYTHONOPTIMIZE=2: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=27/27 result=PASS

EXPECTED_PATH_VALUE_MAPS_UNCHANGED=23/23 changed=[]
EXPECTED_OUTPUT_AND_STATE_HASHES_UNCHANGED=46/46 changed=[]
VERIFY_RUNS_RC=0,0
OUTPUT_FILES=23,23
BYTE_IDENTICAL=23/23 MISMATCHES=[]
STDOUT_IDENTICAL=true
git diff --check
rc=0
```

Families 18 and 19 remain blocked and absent. No asserted expected path/value, output hash, or state
hash changed. No Pine, parity, MTC strategy behavior, Bridge runtime, schema, broker/exchange, host,
credential, deployment, or live surface changed.

Not closed here: independent flagship acceptance/adjudication, and the disclosed coordinated-rehash
semantic-relevance limitation outside R1/R2 remains out of scope.
