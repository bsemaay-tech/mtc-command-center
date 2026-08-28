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
external trust anchor: a coordinated declared-value edit plus recomputation of both manifest hashes
is not detected unless an independent coherence check rejects it. The separate declaration-
inventory hash pins which paths are declared by which assertions; it does not pin their values.

At audited fixed point `c05e5968`, `validate_coherence` covered only families 4, 5, 22, and 24:
**24 of 230 expected values**, leaving **206** outside coherence validation. This repair does not
extend `validate_coherence`. The 11 new coverage assertions make the current scope **24 of 241**,
leaving **217** outside coherence validation. A self-consistent declared-value rehash outside those 24 values is
not detected. Named follow-up **`WP-P0-10-COHERENCE-217`** is to design and add independent
semantic/coherence validation for those 217 current values (the audited 206-value gap plus the 11
assertions added here).

The citation counter is now `citation_line_ranges_validated`. Its value at the initial verifier
repair, 381, proved only that those 381 ranges were well formed, exist, and carry a structurally
matching C/GF, cross-cutting-rule, or explicit-non-decision label. The defended current count is
397 (round 4e pin; unchanged in round 4f). It does **not** prove that a row is relevant to,
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
| 18 | Snapshot drift / bucket-capital divergence | **BLOCKED — UNBUILT** | explicit non-decision `:1288-1296` (was `:1282-1287` on the pre-merge table) |
| 19 | Allocator ↔ Guardian boundary | **BLOCKED — UNBUILT** | C07/GF-07 `:291-316`; explicit non-decision `:1288-1296` |
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
5. reads the authority document and verifies its LF-normalized SHA-256 (then `422f4577…dae16`;
   round 4f pins the post-merge value `331feb1d…362adc`);
6. validates cited line ranges for syntax, existence, and structural label/range agreement
   (381 at this repair; the defended current count is 397),
   without claiming relevance to the assertion carrying each citation;
7. recomputes the manifest-local semantic fixture hash and authority-content hash for every built
   fixture, without claiming those same-tree hashes reject a coordinated edit plus rehash;
8. recomputes the normalized expected-output and final-state hashes;
9. accounts for exactly 241 expected values; and
10. checks independent arithmetic/coherence relationships for 24 expected values in families 4,
    5, 22, and 24 only.

The other 217 expected values remain outside independent coherence validation. Hash agreement for
those values proves self-consistency with the current manifest, not semantic authority under a
self-consistent declared-value rehash. The declaration-inventory hash does not compare those
values.

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
fails visibly. A coordinated declared-value rehash can still pass for the 217 values outside coherence validation;
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

At Round 4b this was only an input-presence gate, not a semantic-relevance prover: a coordinated
fixture and manifest rehash could replace a declared input with an unrelated present path. The N1
declaration-inventory hash now refuses that declaration rewrite, but it still does not prove that a
declared path is semantically relevant or compare the value at that path.

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

Round-4b ruling: this was then the disclosed coordinated-rehash limitation. The N1 inventory hash
now refuses the declaration rewrite, while the remaining limitation is narrower: existence and
declaration identity still do not prove arithmetic relevance or pin the value found at a declared
path.

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
MTC_COMMAND_CENTER\tools\repo_guard.ps1
rc=1 RESULT: BLOCKED only because branch merge-base is 45 commits behind local origin/master (limit 30)
MTC_COMMAND_CENTER\tools\repo_guard.ps1 -WarnOnlyStaleBranch
rc=0 RESULT: PASS protected=none risky_untracked=none
```

The freshness discrepancy was not repaired: the owner-fixed lane contract requires work on top of
`2f80357f`, explicitly forbids rebasing, and says repository observations win over prompt figures.
The current local `origin/master` moved while this isolated lane remained fixed, so stale ancestry
is recorded rather than rewritten.

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

Superseded in place by Round 4d: the paragraph below describes the Round 4d verifier-owned bar
contracts; the `27/27` transcript beneath it remains the executed Round 4c historical result.

Changed the normalized-bar validator to enforce hardcoded OHLCV bar counts for verifier-pinned
fixture families and exact companion scenario identities, per-bar `ohlcv` presence, five-field
OHLCV shape, and integer `index == position` for the contexts whose verifier contract requires an
index. The required contexts and counts live in verifier constants, so deleting or rewriting
fixture-local metadata cannot disable the count, member, shape, or required-index checks.

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

## Round 4d — attacker-controlled opt-ins removed

**Date:** 2026-08-28

**Starting point:** `2f80357ff245def22aed80dae0ca831fbddc7702` on
`feature/wp-p0-10-golden-suite-20260825`.

**Audit tier:** T0, retained from the package contract. This is implementer Gate-3/Gate-4 evidence,
not acceptance; the two independent flagship audits occur after this handoff.

### Finding 1 — required bar validation is contract-driven

`validate_normalized_bar_shapes` no longer consults fixture `frozen_metadata` to decide whether the
bar gate runs. Fixture contexts receive their required counts from `FIXTURE_OHLCV_BAR_COUNTS`.
Companion contexts receive count and index requirements only after an exact family/scenario lookup
in `COMPANION_SCENARIO_CONTRACTS`. A required context with absent/short bars, a non-object member,
missing or non-list `ohlcv`, a non-five-field `ohlcv`, or missing/wrong shape metadata rejects.

The new tamper deletes only the companion's `ohlcv_fields` key and recomputes its same-tree fixture
hash. Round 4c accepted it; round 4d rejects it by name.

### Finding 2 — required indexes cannot self-disable

The mutable `any(index)` switch is gone. `FIXTURE_OHLCV_INDEX_FAMILIES` and the exact companion
scenario contracts identify index-required contexts. Every member in those contexts must carry a
value whose exact Python type is `int` and whose value equals its zero-based position; booleans do
not qualify as integers for this gate. The new all-indices-deleted tamper removes every index from
a C36 companion and recomputes its fixture hash.

### Finding 3 — master gates and selectors are bound to pinned identities

`COMPANION_SCENARIO_CONTRACTS` pins the complete shipped inventory of 16 companion scenarios by
family, exact scenario ID, exact C/GF source range, exact assertion inventory, required bar count,
and required-index status. The verifier rejects unknown, missing, renamed, or source-relabelled
scenarios and rejects assertion inventories that differ from the pinned tuple. Master-gate and
selector checks therefore receive canonical assertion paths selected from this verifier-owned
inventory, not paths supplied by the fixture.

The rename tamper retains the C32 companion record and its source mapping, renames both assertion
sides from `legacy.local.reentry_bar` to `compat.local.reentry_bar`, deletes the master gate and
selector plus their declared paths, recomputes both manifest-local hashes and the path count, and
is rejected at the pinned assertion inventory.

### D026 RED — exact round-4c verifier

Exact command:

```powershell
$oldPath='C:\tmp\wp_p010_verify_fixtures_2f80357f_round4d.py'
$source=git show '2f80357ff245def22aed80dae0ca831fbddc7702:MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_10_GOLDEN_SUITE_2026-08-25/fixtures/verify_fixtures.py'
[System.IO.File]::WriteAllText($oldPath,(($source -join "`n")+"`n"),[System.Text.UTF8Encoding]::new($false))
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\test_verify_fixtures.py --verifier $oldPath
```

Real selected output; command exit `1`:

```text
BASELINE rc=0 clean=true detail=no_named_rejection
TAMPER name=r4d_family_10_companion_ohlcv_metadata_deleted optimized=false rc=0 rejected=false detail=no_named_rejection
TAMPER name=r4d_family_10_companion_all_indices_deleted optimized=false rc=0 rejected=false detail=no_named_rejection
TAMPER name=r4d_family_02_c32_retained_mapping_assertion_renamed optimized=false rc=0 rejected=false detail=no_named_rejection
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=27/30 result=FAIL
ROUND4D_RED_RC=1
```

### D026 GREEN — repaired verifier

Exact command:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\test_verify_fixtures.py
```

Real selected output; command exit `0`:

```text
BASELINE rc=0 clean=true detail=no_named_rejection
TAMPER name=r4d_family_10_companion_ohlcv_metadata_deleted optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=10 ohlcv_shape_contract_mismatch context=companion:C36_GF36_legacy_break_even_modes__local
TAMPER name=r4d_family_10_companion_all_indices_deleted optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=10 normalized_bar_index_mismatch context=companion:C36_GF36_legacy_break_even_modes__local position=0 actual=None
TAMPER name=r4d_family_02_c32_retained_mapping_assertion_renamed optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=02 companion_assertion_inventory_mismatch id=C32_GF32_legacy_reentry_modes__local
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=30/30 result=PASS
```

These RED/GREEN demonstrations close verifier defects only. They do not change the 23 economic
families' `D026 UNEARNED` status.

### Independent count and preservation re-measurement

The following read-only PowerShell measurement loaded all 23 family JSON files independently of
the verifier's summary. It counted assertion records and declared paths directly, and checked the
11 hardcoded C32/C36/C37 assertion names for exactly one companion mapping containing
`config.tw_audit_semantics_mode=research` and the corresponding declared input path:

```powershell
$fixtureDir='MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures'
$direct=0; $companion=0; $scenarios=0; $paths=0; $values=0
$required=@{2=@('legacy.local.reentry_bar','legacy.carry.reentry_bar','legacy.next_bar_open.reentry','legacy.next_bar_close.reentry','legacy.delay.reentry');10=@('legacy.local.exit','legacy.next_bar_confirmed.exit','legacy.tradingview.exit');11=@('legacy.local.exit','legacy.tradingview.exit','legacy.next_bar_confirmed.exit')}
$masterReach=0; $masterTotal=0
Get-ChildItem -LiteralPath $fixtureDir -Filter 'family_*.json' | ForEach-Object {
  $d=Get-Content -Raw -LiteralPath $_.FullName | ConvertFrom-Json
  $values+=@($d.expected_output.assertions).Count
  foreach($item in @($d.expected_output.assertions)){if($item.PSObject.Properties.Name -contains 'input_paths'){$direct++;$paths+=@($item.input_paths).Count}}
  foreach($s in @($d.companion_scenarios)){if($null -ne $s){$scenarios++;foreach($prop in @($s.assertion_inputs.PSObject.Properties)){$companion++;$paths+=@($prop.Value).Count}}}
  $family=[int]$d.family.number
  if($required.ContainsKey($family)){foreach($assertionPath in $required[$family]){
    $masterTotal++
    $matches=@($d.companion_scenarios | Where-Object {$_.assertion_inputs.PSObject.Properties.Name -contains $assertionPath})
    if($matches.Count -eq 1){$inputPaths=@($matches[0].assertion_inputs.PSObject.Properties[$assertionPath].Value);if(($inputPaths -contains 'config.tw_audit_semantics_mode') -and $matches[0].config.tw_audit_semantics_mode -eq 'research'){$masterReach++}}
  }}
}
"EXPECTED_VALUES=$values"; "FIXTURE_ASSERTIONS=$direct"; "COMPANION_SCENARIOS=$scenarios"; "COMPANION_ASSERTIONS=$companion"; "ASSERTION_INPUT_PATHS=$paths"; "MASTER_GATE_REACH=$masterReach/$masterTotal"
```

Real output:

```text
EXPECTED_VALUES=241
FIXTURE_ASSERTIONS=224
COMPANION_SCENARIOS=16
COMPANION_ASSERTIONS=17
ASSERTION_INPUT_PATHS=2660
MASTER_GATE_REACH=11/11
```

The exact base-comparison command loaded each current fixture and the same path from
`git show 2f80357ff245def22aed80dae0ca831fbddc7702:<path>`, compared the complete assertion
`path -> JSON(value)` dictionaries, then compared `expected_output.sha256` and
`expected_output.final_state_sha256`:

```powershell
$base='2f80357ff245def22aed80dae0ca831fbddc7702'
$dir='MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_10_GOLDEN_SUITE_2026-08-25/fixtures'
$maps=0; $hashes=0
$files=Get-ChildItem -LiteralPath ($dir -replace '/','\') -Filter 'family_*.json'
foreach($file in $files){
  $rel="$dir/$($file.Name)"
  $oldText=(git show "${base}:$rel") -join "`n"
  $old=$oldText | ConvertFrom-Json
  $cur=Get-Content -Raw -LiteralPath $file.FullName | ConvertFrom-Json
  $oldMap=@{}
  foreach($item in @($old.expected_output.assertions)){$oldMap[$item.path]=($item.value | ConvertTo-Json -Compress)}
  $same=$oldMap.Count -eq @($cur.expected_output.assertions).Count
  foreach($item in @($cur.expected_output.assertions)){$same=$same -and $oldMap.ContainsKey($item.path) -and $oldMap[$item.path] -eq ($item.value | ConvertTo-Json -Compress)}
  if($same){$maps++}
  if($old.expected_output.sha256 -eq $cur.expected_output.sha256){$hashes++}
  if($old.expected_output.final_state_sha256 -eq $cur.expected_output.final_state_sha256){$hashes++}
}
"EXPECTED_PATH_VALUE_MAPS_UNCHANGED=$maps/$($files.Count)"
"EXPECTED_OUTPUT_AND_STATE_HASHES_UNCHANGED=$hashes/$($files.Count*2)"
```

Real output:

```text
EXPECTED_PATH_VALUE_MAPS_UNCHANGED=23/23
EXPECTED_OUTPUT_AND_STATE_HASHES_UNCHANGED=46/46
```

The reported denominators were not copied from this report or from the verifier summary.

Manifest status was re-read independently:

```powershell
$p='MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\manifest.json'
$m=Get-Content -Raw -LiteralPath $p | ConvertFrom-Json
$built=@($m.families | Where-Object {$_.status -eq 'BUILT'})
$blocked=@($m.families | Where-Object {$_.status -eq 'BLOCKED'})
"FAMILIES_BUILT=$($built.Count)"
"FAMILIES_BLOCKED=$($blocked.Count) numbers=$(@($blocked.number)-join ',')"
"FAMILY_18_FILE=$((Test-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\family_18.json').ToString().ToUpper())"
"FAMILY_19_FILE=$((Test-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\family_19.json').ToString().ToUpper())"
```

```text
FAMILIES_BUILT=23
FAMILIES_BLOCKED=2 numbers=18,19
FAMILY_18_FILE=FALSE
FAMILY_19_FILE=FALSE
```

### Final verifier and harness matrix

Commands:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\verify_fixtures.py MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures C:\tmp\wp_p010_r4d_plain_20260828
python -O MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\verify_fixtures.py MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures C:\tmp\wp_p010_r4d_opt_20260828
$env:PYTHONOPTIMIZE='2'; python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\verify_fixtures.py MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures C:\tmp\wp_p010_r4d_envopt_20260828; Remove-Item Env:PYTHONOPTIMIZE
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\test_verify_fixtures.py
python -O MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\test_verify_fixtures.py
$env:PYTHONOPTIMIZE='2'; python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\test_verify_fixtures.py; Remove-Item Env:PYTHONOPTIMIZE
```

Real output:

```text
verifier plain: rc=0 SUMMARY built=23 blocked=2 fixture_manifest_hashes_matched=23 citation_line_ranges_validated=397 coherence_families=04,05,22,24 coherence_expected_values_validated=24 assertion_input_sources_validated=241 assertion_input_paths_checked=2660 fixture_assertions_validated=224 companion_assertions_validated=17 expected_values_total=241 contract_mismatch_detected=23 contract_match_restored=23 d026_earned=0 d026_unearned=23
verifier -O: rc=1 VERIFY_FAIL reason=python_optimization_forbidden __debug__=false
verifier PYTHONOPTIMIZE=2: rc=1 VERIFY_FAIL reason=python_optimization_forbidden __debug__=false
harness plain: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=30/30 result=PASS
harness -O: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=30/30 result=PASS
harness PYTHONOPTIMIZE=2: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=30/30 result=PASS
```

Determinism command:

```powershell
$v='MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\verify_fixtures.py'
$f='MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures'
$a='C:\tmp\wp_p010_r4d_det_a_20260828'; $b='C:\tmp\wp_p010_r4d_det_b_20260828'
$outA=& python $v $f $a 2>&1; $rcA=$LASTEXITCODE
$outB=& python $v $f $b 2>&1; $rcB=$LASTEXITCODE
$filesA=@(Get-ChildItem -File -LiteralPath $a | Sort-Object Name)
$filesB=@(Get-ChildItem -File -LiteralPath $b | Sort-Object Name)
$matches=0
for($i=0;$i -lt [Math]::Min($filesA.Count,$filesB.Count);$i++){if($filesA[$i].Name -eq $filesB[$i].Name -and (Get-FileHash -Algorithm SHA256 -LiteralPath $filesA[$i].FullName).Hash -eq (Get-FileHash -Algorithm SHA256 -LiteralPath $filesB[$i].FullName).Hash){$matches++}}
"VERIFY_RUNS_RC=$rcA,$rcB"; "OUTPUT_FILES=$($filesA.Count),$($filesB.Count)"; "BYTE_IDENTICAL=$matches/$($filesA.Count)"; "STDOUT_IDENTICAL=$((($outA -join "`n") -ceq ($outB -join "`n")).ToString().ToLower())"
```

```text
VERIFY_RUNS_RC=0,0
OUTPUT_FILES=23,23
BYTE_IDENTICAL=23/23
STDOUT_IDENTICAL=true
```

Compilation and diff hygiene:

```text
python -m py_compile MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\verify_fixtures.py MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\test_verify_fixtures.py
rc=0
python -m ruff --version
rc=1 C:\Python314\python.exe: No module named ruff
git diff --check
rc=0
```

### No-overclaim sweep

The round-4c R2 sentence was narrowed from metadata-declared contexts to verifier-pinned fixture
families and exact companion identities, and now states integer indexes only for contexts whose
hardcoded contract requires them. Against final code, a fixture metadata edit cannot switch off the
required count/member/shape/index checks because the gate decision occurs before metadata is read.
Exact scenario IDs, source ranges, and assertion inventories are also verifier-owned.

The entire report was read and the count/claim grep was rerun. No other current claim exceeded the
final predicate. Earlier `1/7`, `7/7`, `8/8`, `18/19`, `19/19`, `16/27`, and `27/27` harness
snapshots and the `2629`, `2649`, and earlier `2660` path snapshots were deliberately retained as
dated historical transcripts; none is presented as the round-4d result. Round 4d's then-current
harness value was `30/30`; round 4e moved it to `34/34`; the path pin was and remains `2660`.
Round 4e pinned only the aggregate declared input-path count at `2660`, so deflation rejected but a
balanced declaration substitution could still pass. The N1 declaration-inventory hash supersedes
that identity claim: additions, removals, swaps, renames, and moves now reject even at the same
count. Value changes remain outside this hash except where separate master-gate, selector,
companion-config, or coherence predicates apply; undeclared fields remain invisible.

```powershell
rg -n 'tamper_rejected=[0-9]+/[0-9]+|assertion_input_paths_checked=[0-9]+|fixture_assertions_validated=[0-9]+|companion_assertions_validated=[0-9]+|bar counts live|metadata edit|cannot opt out|all indices|index' MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\LANE_REPORT.md
```

No Pine, parity, MTC strategy behavior, Bridge runtime, schema, broker/exchange, host, credential,
deployment, or live surface changed. Independent flagship acceptance remains pending.

## Round 4e - final mechanical repair

**Date:** 2026-08-28

**Starting point:** `c5e0fbc639491a9e0755dde5237b5cc4487162ed` on
`feature/wp-p0-10-golden-suite-20260825`.

**Audit tier:** T0, retained from the package contract. This is implementer Gate-3/Gate-4 evidence,
not acceptance.

### R-1 - C20 legacy execution profile is verifier-owned

Family 14 now binds both `legacy.long_stop_close_only` and `legacy.short_stop_close_only` to
`execution_profile=LEGACY_CLOSE_ONLY` in `COMPANION_SELECTOR_REQUIREMENTS`. The value-flip attack
changes it to `STANDING_TOUCH`, recomputes the family fixture-contract hash, and is rejected by the
selector predicate. A second tamper rehomes both assertions as fixture-local declarations and proves
the existing `companion_selector_fixture_local_forbidden` predicate now covers the two family-14
paths too.

The lane prompt cites the R9 authority pin at line 578; the repository version places the same R9
`execution_profile: "LEGACY_CLOSE_ONLY"` statement at line 579. The repository text governs.

### R-2 - declared input-path count is pinned

`EXPECTED_INPUT_PATH_COUNT = 2660` is verifier-owned. Both the manifest declaration and the measured
suite total must equal it. The exact auditor attack retains only the previously verifier-forced
minimum, removes 2,408 of 2,660 paths, updates all 23 affected fixture-contract hashes and the
manifest count to 252, and now rejects before attacked-tree equality can self-attest the result.

At Round 4e the narrower claim was only that aggregate path deflation rejected across fixture-local
and companion declarations. Same-count declaration substitution remained possible until the N1
inventory hash; declared-value changes remain outside that hash unless another specific predicate
covers them.

### Applied nits

- The Round 4d index sentence now says `index-required contexts`.
- The rewritten Round 4c R2 paragraph has an in-place Round 4d supersession marker.
- `EXPECTED_CITATION_LINE_RANGE_COUNT = 397` now defends the printed citation figure. The auditor's
  coordinated citation deflation reaches 326 and rejects.

### D026 RED - pre-fix verifier at `c5e0fbc6`

Exact command run after adding the three regression rows and before changing the verifier:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\test_verify_fixtures.py
```

Real selected output; command exit `1`:

```text
TAMPER name=r4e_family_14_execution_profile_flipped optimized=false rc=0 rejected=false detail=no_named_rejection
TAMPER name=r4e_suite_wide_input_path_deflation optimized=false rc=0 rejected=false detail=no_named_rejection
TAMPER name=r4e_suite_wide_citation_deflation optimized=false rc=0 rejected=false detail=no_named_rejection
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=30/33 result=FAIL
```

### D026 GREEN - repaired verifier

The same command against the repaired verifier returned `0`:

```text
TAMPER name=r4e_family_14_execution_profile_flipped optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=14 companion_selector_mismatch path=legacy.long_stop_close_only selector=execution_profile expected=LEGACY_CLOSE_ONLY actual=STANDING_TOUCH
TAMPER name=r4e_family_14_selector_rehomed_fixture_local optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=14 companion_selector_fixture_local_forbidden path=legacy.long_stop_close_only
TAMPER name=r4e_suite_wide_input_path_deflation optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=manifest_assertion_input_path_count expected=2660 actual=252
TAMPER name=r4e_suite_wide_citation_deflation optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=citation_line_range_count expected=397 actual=326
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=34/34 result=PASS
```

Two carried tamper helpers stopped rewriting `manifest.assertion_input_path_count`, because the new
verifier-owned count would otherwise reject before their existing deeper predicates ran. Before
that bookkeeping adjustment, the repaired verifier returned the new count reason at `2658` and
`2656`; afterward, the unchanged semantic attacks again reached their original named reasons:

```text
TAMPER name=r4d_family_02_c32_retained_mapping_assertion_renamed optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=02 companion_assertion_inventory_mismatch id=C32_GF32_legacy_reentry_modes__local
TAMPER name=n4_family_02_selector_rehomed_fixture_local optimized=false rc=1 rejected=true detail=VERIFY_FAIL reason=family=02 companion_selector_fixture_local_forbidden path=legacy.local.reentry_bar
```

Thus both forms rejected through their then-current gates, but the aggregate count did not preserve
declaration identity: a different balanced declaration inventory could still keep the canonical
count. N1 closes that structural gap with the verifier-owned digest.

### Final matrix and independent remeasurement

```text
verifier plain: rc=0 SUMMARY built=23 blocked=2 fixture_manifest_hashes_matched=23 citation_line_ranges_validated=397 coherence_families=04,05,22,24 coherence_expected_values_validated=24 assertion_input_sources_validated=241 assertion_input_paths_checked=2660 fixture_assertions_validated=224 companion_assertions_validated=17 expected_values_total=241 contract_mismatch_detected=23 contract_match_restored=23 d026_earned=0 d026_unearned=23
verifier -O: rc=1 VERIFY_FAIL reason=python_optimization_forbidden __debug__=false
verifier PYTHONOPTIMIZE=2: rc=1 VERIFY_FAIL reason=python_optimization_forbidden __debug__=false
harness plain: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=34/34 result=PASS
harness -O: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=34/34 result=PASS
harness PYTHONOPTIMIZE=2: rc=0 VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=34/34 result=PASS

ASSERTION_SOURCE_REACH=241/241
ASSERTION_INPUT_PATHS=2660/2660
MASTER_GATE_REACH=11/11
FAMILY14_SELECTOR_REACH=2/2
EXPECTED_PATH_VALUE_MAPS_UNCHANGED=23/23
EXPECTED_OUTPUT_AND_STATE_HASHES_UNCHANGED=46/46
FAMILIES_BUILT=23
FAMILIES_BLOCKED=2 numbers=18,19
FAMILY_18_FILE=FALSE
FAMILY_19_FILE=FALSE

VERIFY_RUNS_RC=0,0
OUTPUT_FILES=23,23
BYTE_IDENTICAL=23/23
STDOUT_IDENTICAL=true
python -m py_compile verify_fixtures.py test_verify_fixtures.py: rc=0
git diff --check: rc=0
```

No fixture JSON, expected path/value map, output/state hash, Pine, parity, MTC strategy behavior,
Bridge runtime, schema, broker/exchange, host, credential, deployment, or live surface changed.
Independent flagship acceptance remains pending.

## Round 4f - class-level companion config rule (owner-authorized)

**Date:** 2026-08-28

**Starting point:** `98150b9a` on `feature/wp-p0-10-golden-suite-20260825`, then merge of
`origin/master` `85c3e17f` (Required 0). Audit tier T0. Implementer Gate-3/Gate-4 only; not
acceptance.

The owner authorized one class-level repair after round 4e's BLOCK. Point-fixes of named keys are
out of scope.

### Required 0 - merge and authority identity

Post-merge authority file is 1309 LF lines. Measured LF-normalized SHA-256:

`331feb1d7578bbf804b527e2a658fecbcbf74d00d1e852312860345029362adc`

Command:

```python
from pathlib import Path
import hashlib
p = Path('MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/CAPABILITY_CANONICALIZATION_TABLE.md')
text = p.read_text(encoding='utf-8').replace('\r\n', '\n').replace('\r', '\n')
print(hashlib.sha256(text.encode('utf-8')).hexdigest())
```

The pre-merge pin `422f4577…dae16` was the stale 1290-line copy. Binding hashes of all 23 built
families changed because cited fragments at the existing C/GF ranges now contain the citation
re-resolution text. Cross-cutting citations `:1272-1276` / `:1274-1276` were retargeted +6 to
`:1278-1282` / `:1280-1282` so the section header at `:1278` is in range; blocked-family
non-decision citations moved `:1282-1287` → `:1288-1296`. **No expected assertion value, output
hash, or state hash was rewritten.**

### Required 1 - F-1 + F-2 class rule

`COMPANION_CONFIG_PINNED` holds verifier-owned constants for every companion-declared path whose
authority value does not vary across siblings. `COMPANION_SELECTOR_REQUIREMENTS` remains the
SIBLING_VARIANT half. `COMPANION_CONFIG_AUTHORITY_SILENT` is empty and must stay explicit.
`require_companion_config_class` classifies every declared companion `config.*` path into exactly
one of those three sets; an unclassified path fails closed.

Census, derived from the fixture data (12 distinct companion `config.*` paths / 52 occurrences):

| Set | Count | Keys |
|---|---:|---|
| PINNED | 7 | `tw_reversal_reentry_delay_bars=2`, `be_trigger_r="1.0"`, `be_buffer_r="0.0"`, `sl_percent="5.0"`, `trail_start_r="1.0"`, `trail_distance_atr_mult="1.5"`, `trail_atr="2.0"` |
| SIBLING_VARIANT | 5 | `tw_reversal_reentry_mode`, `tw_be_semantics_mode`, `tw_trailing_semantics_mode`, `tw_audit_semantics_mode`, `execution_profile` |
| AUTHORITY_SILENT | 0 | — |

Pins verified against the post-merge table: C32 `:832,:840`; C14 `:475`; C36 `:948`; C15 `:493`;
C37 `:982`; C20 `:585`.

**Fixture-local surface (not closed here):** 101 distinct / 1275 `config.*` declarations live on
fixture-local `input_paths`. The same presence-without-value hole exists there. No fixture-local
classification table exists in the repository: the previously cited 87 PINNED / 5 SIBLING_VARIANT
/ 15 AUTHORITY_SILENT figures are therefore NOT VERIFIED, and their total of 107 does not reconcile
with the measured 101 distinct paths. Closing the value hole would require a separately reviewed
classification. Undeclared companion fields such as `execution_profile_id` are also outside the
declared-path class rule.

### Required 2 - F-3 authority anchor

`EXPECTED_AUTHORITY_TEXT_LF_SHA256` is verifier-owned and equal to the post-merge measurement
above. The live file, the constant, and `manifest.authority_text_lf_sha256` must all agree.
Coordinating only the manifest field against a rewritten authority file now fails
`authority_text_lf_sha256_expected`.

### Required 3 - F-4 stale present-tense figures

The round-4d "current values are `30/30`" sentence is now dated; round 4e's harness was `34/34`.
The 381 citation snapshots at `:64` and `:173` are dated as the initial-repair value; current is
397.

### D026

RED against the pre-class-fix verifier at `98150b9a` (current fixtures, old `verify_fixtures.py`):

```text
TAMPER name=r4f_family_02_delay_bars_zero ... rc=0 rejected=false
TAMPER name=r4f_family_10_be_trigger_flipped ... rc=0 rejected=false
TAMPER name=r4f_family_11_trail_atr_flipped ... rc=0 rejected=false
TAMPER name=r4f_companion_config_unclassified ... rc=0 rejected=false
TAMPER name=r4f_authority_r9_rewrite_coordinated ... rc=0 rejected=false
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=34/39 result=FAIL
```

GREEN with the repaired verifier, same five attacks, plus the carried 34:

```text
TAMPER name=r4f_family_02_delay_bars_zero ... rc=1 rejected=true detail=VERIFY_FAIL reason=family=02 companion_config_pinned_mismatch path=legacy.carry.reentry_bar key=tw_reversal_reentry_delay_bars expected=2 actual=0
TAMPER name=r4f_family_10_be_trigger_flipped ... rc=1 rejected=true detail=VERIFY_FAIL reason=family=10 companion_config_pinned_mismatch path=legacy.local.exit key=be_trigger_r expected=1.0 actual=9.9
TAMPER name=r4f_family_11_trail_atr_flipped ... rc=1 rejected=true detail=VERIFY_FAIL reason=family=11 companion_config_pinned_mismatch path=legacy.local.exit key=trail_atr expected=2.0 actual=9.9
TAMPER name=r4f_companion_config_unclassified ... rc=1 rejected=true detail=VERIFY_FAIL reason=family=02 companion_config_unclassified path=legacy.local.reentry_bar key=unclassified_probe
TAMPER name=r4f_authority_r9_rewrite_coordinated ... rc=1 rejected=true detail=VERIFY_FAIL reason=authority_text_lf_sha256_expected expected=331feb1d7578bbf804b527e2a658fecbcbf74d00d1e852312860345029362adc actual=ba2c4b9b379bdccda7529fad5d5b8ab82880a38f50474ec66e22e65cfb80a722
VERIFIER_REGRESSION_SUMMARY baseline_clean=1 tamper_rejected=39/39 result=PASS
```

### Final matrix

```text
verifier plain: rc=0 SUMMARY built=23 blocked=2 fixture_manifest_hashes_matched=23 citation_line_ranges_validated=397 coherence_families=04,05,22,24 coherence_expected_values_validated=24 assertion_input_sources_validated=241 assertion_input_paths_checked=2660 fixture_assertions_validated=224 companion_assertions_validated=17 expected_values_total=241 contract_mismatch_detected=23 contract_match_restored=23 d026_earned=0 d026_unearned=23
verifier -O / PYTHONOPTIMIZE=2: rc=1 python_optimization_forbidden
harness plain / -O / PYTHONOPTIMIZE=2: rc=0 tamper_rejected=39/39 result=PASS
VERIFY_RUNS_RC=0,0 OUTPUT_FILES=23,23 BYTE_IDENTICAL=23/23 STDOUT_IDENTICAL=true
```

No expected assertion values, Pine, parity, MTC strategy behavior, Bridge runtime, schema,
broker/exchange, host, credential, deployment, or live surface changed. Independent flagship
acceptance remains pending.

## N1 - declaration inventory hash and narrowed claim

The verifier now pins SHA-256
`b1d81fb181894fa810ae88b562d9cf85ec7389f9c74af6b36038fe3c1f69d9df` over 241 canonical
declaration records containing 2,660 input paths. Fixture-local records use the explicit
`__fixture__` scenario sentinel. Input paths are sorted with duplicates preserved; the records are
sorted by their full tuple before compact, ASCII-escaped JSON serialization and UTF-8 hashing.

This check guarantees only that the reviewed declaration list is intact: nothing was added,
removed, swapped, renamed, or moved between assertions or companion scenarios. It does **not**
compare declared input values, identify the differing record, prove semantic relevance, or see a
configuration field no assertion declares. A declared value change can therefore leave this hash
unchanged.

The V2 balanced substitution was accepted by the unchanged `9a76818f` verifier at 241 records and
2,660 paths, then refused by the new verifier with `declaration_inventory_hash_mismatch`. V1-V7
all refuse by that reason; the unmodified corpus and an input-list reorder both pass. Full commands
and literal output are recorded in `C:\tmp\LANE_PROMPTS_20260828\N1_P010_HASH_REPORT.md`.

Mechanical corrections included here: the nonexistent 87/5/15 prep-table citation is replaced by
the verified absence and non-reconciling 107-versus-101 totals above; the Round-4d/4e residual now
names round 4f's pinned companion-config values and N1's structural declaration identity instead
of implying that the aggregate count protected a same-count inventory.
