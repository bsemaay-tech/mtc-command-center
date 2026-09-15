# W314 F02 Contract Self-Test Alignment Report

## Verdict

**AUTHORIZED ALIGNMENT COMPLETE; THE TWO EXPECTED DESIGN-PIN FAILURES REMAIN.** Exactly the five
F02 cases named by the lane now pass, and the frozen legacy replay remains byte-exact. The lane
authorizes only the named self-test assertions and forbids harness, kernel, sealed-table, and design
changes (`C:\tmp\LANE_PROMPTS_20260828\LANE_W314_SELFTEST_F02.md:19-25`).

Gate-1 scope is T1 for the contract self-test change, T2 for this report, and T3 for the external
completion marker; the highest-overlap classification is T1. The write lane is
`feature/wp-p0-12-corrected-vnext-20260831` in `C:\WP012BUILD`, and the mandatory preflight started
from a clean worktree at `191637e2` as required
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W314_SELFTEST_F02.md:3-6`).

## Governing design rule

The current design states:

> `cumulative_funding` is required for "every DEF-P012-08 RESULT, whether the schedule event is
> eligible or ineligible," and is required on both rows as the minimal fixed shape.

That is the conditional-member rule at
`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1221-1228`. The accumulator applies each
signed funding cash delta to cumulative funding
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:418-424`); the kernel state initializes the
accumulator to `0.0`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/types.py:433-436`). The W306 projection
therefore keys membership on declared `DEF-P012-08` and emits the state value
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:967-970`).

## Per-case alignment

| Case | Old assertion | New assertion | Design line |
|---|---|---|---|
| `test_probe_driver_refuses_unclosed_base_before_variant_comparison` | The unmodified current-kernel receipt expected `CLOSED_SET_VIOLATION` at `/RESULT_SURFACE/cumulative_funding`; W306 classified that as the pre-F02 expectation (`W306_KERNEL_FLAGSHIP2B_REPORT.md:226-228`). | The unmodified receipt expects `CORRECTED_EXPECTATION` with comparator-first node `/EVENT_SURFACE/cash_events`; it remains `NOT_DETECTED` because the catalog target funding-delta node did not change (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1389-1395`). | A probe is detected only when the failed check matches and the catalog target belongs to the complete changed-node set; comparator-first order is separately recorded (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:481-493`). Kernel substitution preserves the base input and sealed expected artifact (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:495-497`). |
| `test_raw_kernel_result_membership_follows_declared_contract[RULE2-08-RED]` | The expected result-member set omitted `cumulative_funding` (`W306_KERNEL_FLAGSHIP2B_REPORT.md:229-231`). | A declaration containing `DEF-P012-08` adds `cumulative_funding` to the expected set (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1913-1917`). | The member is required for every DEF-P012-08 result (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1221-1228`). |
| `test_raw_kernel_result_membership_follows_declared_contract[RULE2-08-GREEN]` | The expected result-member set omitted `cumulative_funding` (`W306_KERNEL_FLAGSHIP2B_REPORT.md:229-231`). | The same declared-DEF conditional adds `cumulative_funding` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1913-1917`). | The member is required whether the event is eligible or ineligible (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1228`). |
| `test_rule2_08_raw_kernel_is_not_seeded_from_legacy_state[RULE2-08-RED]` | The test asserted that `cumulative_funding` was absent when the raw run emitted no funding events (`W306_KERNEL_FLAGSHIP2B_REPORT.md:232-234`). | With empty cash and funding containers, the result must carry `cumulative_funding == 0` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:2071-2075`). | DEF-P012-08 fixes member presence (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1228`); the accumulator starts at zero (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/types.py:435-436`). |
| `test_rule2_08_raw_kernel_is_not_seeded_from_legacy_state[RULE2-08-GREEN]` | The test asserted that `cumulative_funding` was absent when the raw run emitted no funding events (`W306_KERNEL_FLAGSHIP2B_REPORT.md:232-234`). | With empty cash and funding containers, the result must carry `cumulative_funding == 0` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:2071-2075`). | The ineligible GREEN vector emits no funding row (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:443`), while the result member remains required (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1228`). |

## Failing-then-passing proof

Both commands ran from `C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON`, the location
required by the lane (`C:\tmp\LANE_PROMPTS_20260828\LANE_W314_SELFTEST_F02.md:27-33`).

Before editing:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
7 failed, 304 passed in 6.48s
```

The seven failing cases were:

1. `test_legacy_reproduction_refuses_one_ulp_actual`
2. `test_receipt_accounts_for_every_blocked_expected_node`
3. `test_probe_driver_refuses_unclosed_base_before_variant_comparison`
4. `test_raw_kernel_result_membership_follows_declared_contract[RULE2-08-RED]`
5. `test_raw_kernel_result_membership_follows_declared_contract[RULE2-08-GREEN]`
6. `test_rule2_08_raw_kernel_is_not_seeded_from_legacy_state[RULE2-08-RED]`
7. `test_rule2_08_raw_kernel_is_not_seeded_from_legacy_state[RULE2-08-GREEN]`

After editing:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
2 failed, 309 passed in 6.25s
```

The only remaining failures are `test_legacy_reproduction_refuses_one_ulp_actual` and
`test_receipt_accounts_for_every_blocked_expected_node`. Both call the comparison pipeline
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1303-1343`),
and the pipeline validates sealed producers before comparison
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2243-2251,2307-2311`).
The exact stale-pin refusal is recorded under Discrepancy 1.

## Frozen legacy replay

The W306/W249 no-write replay uses the digest-checked legacy executor and byte comparison functions
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1581-1730`),
as W306 records (`W306_KERNEL_FLAGSHIP2B_REPORT.md:190-210`). The measured result was:

```text
SURFACES_EQUAL=34 MISMATCH=0 SKIPPED=0
```

No baseline-output command was run; the lane forbids generating baseline output
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W314_SELFTEST_F02.md:34-35`). The canonical gate was not
invoked, as required (`C:\tmp\LANE_PROMPTS_20260828\LANE_W314_SELFTEST_F02.md:36`).

## Commits and scope

- W306 F02 kernel authority: `4b1853c48ac94a75d4f633c3dd0af75cc6701580`, recorded by W306
  (`W306_KERNEL_FLAGSHIP2B_REPORT.md:97-98`).
- W314 test commit: `79bc2d4c46ca8949160f4cbe474114b579c6f6ac`, subject
  `test(mtc-v2): align F02 self-tests with declared-DEF funding rule`; the required subject/body and
  explicit staging fence are specified at
  `C:\tmp\LANE_PROMPTS_20260828\LANE_W314_SELFTEST_F02.md:38-41`.
- This report is committed separately with subject
  `docs(mtc-v2): report W314 self-test alignment`; its hash is necessarily resolved after this
  file's bytes are fixed. The test and W306 hashes above are the report's reproducible commit
  anchors.

The implementation commit changes only
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py`;
the three changed assertion sites are visible at lines 1389-1395, 1913-1917, and 2071-2075 of that
file. No canonical gate, push, merge, PR, master write, harness edit, kernel edit, sealed-table edit,
or design edit was authorized (`C:\tmp\LANE_PROMPTS_20260828\LANE_W314_SELFTEST_F02.md:3-6,19-25,36-41`).

## Discrepancies

1. **The in-repository design pin is stale.** The manifest still records design v1.12, SHA-256
   `1f506c923c700df3a2a757ab3d49efabcd4d06bf39c251f8965c55bc10de8b75`, and 1,419 lines
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:13-18`),
   while the named design identifies itself as v1.13
   (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1`). The two residual tests therefore
   refuse in `validate_design_pin`, whose digest/line-count check is at
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2220-2236`.
   The lane explicitly says to leave this for a later re-pin lane
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W314_SELFTEST_F02.md:31-36`).

2. **The cataloged PROBE-P012-08-A variant still contains the pre-F02 projection rule.** Its copied
   `results.py` retains `include_cumulative_funding = bool(state.funding_events)`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-08-A/kernel/results.py:844-852,968-973`),
   whereas the design requires the member for every DEF-P012-08 result
   (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1228`). The modification manifest's only
   patch is the funding-sign change in `economics.py`
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-08-A/modification_manifest.json:1`).
   Consequently, the cataloged modified copy remains `NOT_DETECTED` on the earlier
   `CLOSED_SET_VIOLATION` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1397-1416`)
   instead of reaching the intended sign-flip `CORRECTED_EXPECTATION` at the cash-delta node
   (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:443-447`). Re-pinning or rewriting the
   protected variant was outside W314's one-file authority
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W314_SELFTEST_F02.md:19-25`).

3. **The raw RULE2-08 executor remains unclosed beyond result membership.** The aligned raw tests
   verify empty cash and funding containers and zero cumulative funding
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:2067-2075`),
   while the sealed RED design requires an eligible funding event with cash delta `-0.1`
   (`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:443`). Accordingly, the unmodified
   current-kernel probe receipt reaches `CORRECTED_EXPECTATION` first at
   `/EVENT_SURFACE/cash_events` but does not contain the catalog target node
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1381-1395`).
   W314 was authorized to align the F02 membership/value assertions only, not to close this separate
   scenario-execution gap (`C:\tmp\LANE_PROMPTS_20260828\LANE_W314_SELFTEST_F02.md:19-25`).
