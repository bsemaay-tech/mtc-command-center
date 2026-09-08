# W318 Harness Projection Consumption Report

## Verdict

**IMPLEMENTED AND SELF-VERIFIED; READY FOR INDEPENDENT ACCEPTANCE.** The harness now consumes the
sealed `rule2_divergent_projection` and `rule2_green_projection` member shapes, evaluates legacy
`DESIGN_DERIVED` declarations against corrected selectors or declared refusals, retains
`EXPECTATION_UNSEALED` for a row whose bound member is absent, and records
`legacy_side_source` in projection and scenario receipts
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3426-3462,3475-3675,3957-3971`).
This is implementer evidence, not an independent acceptance verdict. The canonical gate was not
run, as expressly required (`C:\tmp\LANE_PROMPTS_20260828\LANE_W318_HARNESS_CONSUME_M6.md:35-37`).

## Authority, preconditions, and write lane

Gate-1 classification is **T1**: the change is non-economic harness product code and selftests; it
does not change strategy logic, economic values, Pine, parity corpora, broker behavior, deployment,
or trading. Authority and the exact two harness/selftest scopes are stated by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W318_HARNESS_CONSUME_M6.md:11-19`).

- Worktree: `C:\WP012BUILD`.
- Branch: `feature/wp-p0-12-corrected-vnext-20260831`.
- Starting HEAD: `8112ff0bae07aee3036a9e0a3f470f1e4a92bc1f`.
- Preconditions measured before the first write: clean worktree; `W314B_DONE.txt` contained
  `exit=0`; `W312_ACCEPTED.txt` existed. These are the lane's hard STOP conditions
  (`C:\tmp\LANE_PROMPTS_20260828\LANE_W318_HARNESS_CONSUME_M6.md:3-9`).
- Write paths: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py`,
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py`,
  and this report. Live/scheduled dependency status: none; all execution was local selftest or the
  authorized read-only legacy replay. No push, merge, PR, master write, baseline generation, or
  external endpoint action was performed (scope rules:
  `C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-36`).

## Reader change against design v1.13 and the sealed shape

The v1.13 meaning retained by W312 says each member is a pair of tagged states and that unequal
present kinds count as divergence; it also identifies `BASELINE_BYTES` versus `CONTRACT_TABLES`
for RED and equality for GREEN
(`C:\tmp\LANE_PROMPTS_20260828\W312_TABLES_M6_M4_REPORT.md:77-94`). The sealed five-member JSON
shape is `selector`, `legacy`, `corrected`, `expected_relation`, and `derivation`; W312 records the
legacy declaration, corrected selector/refusal forms, source labels, and raw-value rule
(`C:\tmp\LANE_PROMPTS_20260828\W312_TABLES_M6_M4_REPORT.md:96-124`). The accepted bundle carries
that shape on 15 rows and 55 members
(`C:\tmp\LANE_PROMPTS_20260828\W312_TABLES_M6_M4_REPORT.md:126-140`;
`C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:1`).

The implementation follows that shape as follows:

1. Catalog validation admits the two optional role-bound members without requiring them, so the
   later in-repo catalog refresh can carry them while RULE2-08 can remain honestly absent
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2335-2347`).
2. Legacy declarations accept only the currently authorized `DESIGN_DERIVED` source and the sealed
   `PRESENT`/`ABSENT`/`REFUSAL` forms. Container cardinalities are expanded only far enough for
   `_present` to canonicalize `A:n`/`O:n`; an unpinned PRESENT is accepted only on a DIFFERS member
   with its required note
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3475-3558`).
3. Corrected declarations either resolve their string/integer token path through
   `_projection_value` or materialize the sealed corrected refusal. Node-kind validation includes
   the colon-free null token `N`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3381-3415,3561-3609`).
4. `build_projection_results` reads the role-bound array, validates the exact five top-level
   members and relation, compares the two tagged states by equality, and refuses only a missing or
   empty bound array with `EXPECTATION_UNSEALED`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3612-3675`).
5. Projection call sites pass an explicit sentinel instead of legacy actual/baseline projection
   bytes, and scenario receipts expose `legacy_side_source`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1842-1846,2997-3012,3908-3913,3957-3971`).

The current v1.14 amendment, which landed while this lane was running, now pins the same container,
cardinality, source, unpinned-value, corrected-selector/refusal, and relation rules explicitly
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:609-674`). Its L10 states that
`DESIGN_DERIVED` is a declaration rather than a measurement of baseline bytes
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:798`). No declared legacy projection was
reconciled against `BASELINE_BYTES` in W318; therefore a declaration-versus-baseline mismatch is
**NOT VERIFIED**, not asserted absent.

## RED/GREEN proof

The fixture is the sealed five-member catalog-row shape and uses `I:1` versus `F:1.0` to prove that
unequal kinds discriminate independently of numeric equality. The tests pass a baseline sentinel
and assert `legacy_side_source == DESIGN_DERIVED`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:2078-2160`).

Before the reader change, the exact two-test command produced:

```text
FFFF                                                                     [100%]
4 failed in 0.53s
```

All four cases stopped at the old unconditional `EXPECTATION_UNSEALED`. After the reader change,
the same command produced:

```text
....                                                                     [100%]
4 passed in 0.06s
```

The four dispositions are: unequal kinds -> divergence PASS; equal states -> divergence FAIL;
equal states -> GREEN PASS; unequal kinds -> GREEN FAIL
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:2115-2160`).

The direct read-only bundle exercise used the accepted bundle row plus its in-repo corrected golden,
passed a baseline sentinel, and measured:

```text
SEALED_ROWS=15 MEMBERS=55 FAILURES=0
```

This directly covers all sealed rows/members identified by W312, including container cardinalities,
the corrected refusal, and the two deliberately unpinned legacy stop-id declarations
(`C:\tmp\LANE_PROMPTS_20260828\W312_TABLES_M6_M4_REPORT.md:136-140,187-205,249-280`).

## Revised pre-existing tests

No always-refuse test was simply deleted. At starting HEAD `8112ff0b`, the first two tests below
encoded individual RED/GREEN unconditional refusals and the third encoded the catalog-wide
unconditional refusal (`test_verify_bceg.py:2078-2145` at that commit). They were revised as follows:

1. `test_rule2_02_red_projection_refuses_without_sealed_selector_declaration` became
   `test_rule2_divergent_projection_discriminates_sealed_states` with unequal/equal cases
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:2115-2136`).
2. `test_w305_item5_refuses_reader_authored_green_projection_when_catalog_has_none` became
   `test_rule2_green_projection_discriminates_sealed_states` with equal/unequal cases
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:2139-2160`).
3. `test_all_projection_rows_refuse_without_sealed_selector_declarations` retained its name but now
   skips rows that carry their bound member and asserts `EXPECTATION_UNSEALED` only for rows that do
   not (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:2163-2186`).

## Contract selftests

Command, run after the implementation commit from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
3 failed, 310 passed in 5.04s
```

The failures are exactly the expected three:

1. `test_legacy_reproduction_refuses_one_ulp_actual`.
2. `test_receipt_accounts_for_every_blocked_expected_node`.
3. `test_probe_driver_refuses_unclosed_base_before_variant_comparison`.

The first two enter the comparison pipeline and stop at `validate_design_pin`; the validator compares
the external design's measured bytes and line count to the sealed manifest pin
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2210-2242`;
tests at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1304-1350`). The third is the deliberately
reverted probe-driver case and currently observes `CORRECTED_EXPECTATION` rather than its asserted
pre-F02 `CLOSED_SET_VIOLATION` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1364-1395`). No other
selftest failed, matching the lane's required expected-failure set
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W318_HARNESS_CONSUME_M6.md:35-36`).

## Frozen legacy replay after the implementation commit

The authorized W249/W306 no-write replay loaded the digest-checked frozen driver, executed KERNEL_1
in memory, and compared both surfaces for all catalog RED/GREEN rows. It ran after commit
`3c372de04205a08fe0fd1d7622b97eab48cb98db` and measured:

```text
SURFACES_EQUAL=34 MISMATCH=0 SKIPPED=0
```

The replay uses the harness's frozen-driver loader and byte comparator
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1636-1730`).
It generated no baseline output.

## Commit and final scope

Implementation commit:

```text
3c372de04205a08fe0fd1d7622b97eab48cb98db
feat(mtc-v2): consume sealed RULE-2 projection members (decision 138, W312 D-12)
```

The commit contains exactly the authorized harness and selftest paths. `git diff --check`, Python
byte-compilation, the focused five-case projection/refusal selection, the all-55 bundle exercise,
the full selftest directory, and the frozen replay were run. The report is committed separately as
required by the lane (`C:\tmp\LANE_PROMPTS_20260828\LANE_W318_HARNESS_CONSUME_M6.md:39-46`).

## Discrepancies

1. **The external design advanced from v1.13 to v1.14 while W318 was running.** The lane explicitly
   forecast W317 in parallel and instructed W318 to take the member shape from W312 plus the accepted
   bundle (`C:\tmp\LANE_PROMPTS_20260828\LANE_W318_HARNESS_CONSUME_M6.md:6-7,13-14`). The current
   file now identifies itself as v1.14 and retains the tagged-state meaning while adding the exact
   JSON container (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1,607-674`). W318 used the
   v1.13 meaning recorded in W312 and verified the finished reader against the now-landed v1.14
   clarification; no conflicting shape was found.
2. **The repository design pin is deliberately stale, and the root decision index does not yet list
   owner decision 138.**
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:1`
   still pins the older 1,419-line design,
   while the current external design is v1.14 (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1`).
   That explains the two expected `validate_design_pin` failures and was not changed because this
   lane forbids the canonical gate/re-pin (`C:\tmp\LANE_PROMPTS_20260828\LANE_W318_HARNESS_CONSUME_M6.md:35-37`).
   Separately, root `DECISIONS.md` enumerates its current binding index without decision 138
   (`DECISIONS.md:7-48`); W318 authority therefore comes from the explicit lane specification
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W318_HARNESS_CONSUME_M6.md:11-19`).

Finding count: **2 discrepancies**, both expected governance/evidence drift; **0 sealed-member
relation failures** in the measured 15-row/55-member bundle exercise.
