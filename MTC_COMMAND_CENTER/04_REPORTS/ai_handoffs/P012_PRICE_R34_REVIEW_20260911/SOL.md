# P012 R34 independent T0 review

**Verdict: PASS** for the bounded synthetic-only price scope.

Target: HEAD `3faed08866e122158e93c626288873ec58a42e3d`, base `3e86faec032407c1af9a75f8b8852222d732f316`, packet manifest SHA-256 `2f4ac4a45f3511a4dadb7426e2007b687284474bf95bd24f4ea123d1c7b480b8`.

Material findings: **none**. Optional nits: **none**. No findings are suppressed.

## Personally executed QA

Runtime:

- `C:\Python314\python.exe`
- Python `3.14.2`
- pytest `9.0.2`
- Import root: `C:\tmp\P012_PRICE_20260910\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2`

Full gate executed with the mandated argv:

```text
C:/Python314/python.exe -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --root C:/tmp/P012_PRICE_20260910/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2 --baseline-root C:/tmp/P012_PRICE_BASELINE34_20260911/CURRENT --output C:/tmp/P012_R34_SOL_T0_A2_20260911/results/full_gate.json
```

Result:

- Exit `0`
- 558 contract selftests passed, 0 failed
- Zero acceptance blockers
- 17 scenarios and 34 surfaces reproduced
- Catalog: 9 RED, 8 GREEN, 10 PROBE
- Expected-source provenance: `MATCH`
- Claim: `BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_ACCEPTED`

Focused tests executed second with the mandated argv:

```text
C:/Python314/python.exe -m pytest C:/tmp/P012_PRICE_20260910/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_price_alignment_policy.py C:/tmp/P012_PRICE_20260910/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_economic_records.py C:/tmp/P012_PRICE_20260910/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_results_corrected.py C:/tmp/P012_PRICE_20260910/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_w285_kernel_remaining.py -q -p no:cacheprovider --basetemp C:/tmp/P012_R34_SOL_T0_A2_20260911/scratch/pytest-temp
```

Result: exit `0`; **113 passed**, 1 environmental `cache_dir` warning, in 0.58 seconds.

A targeted independent edge probe also exited `0`. It covered 11 lattice boundaries, invalid inputs/policy/directions, and exact plain-`int` and `int`-subclass preservation for `2**53+1`, `10**400`, and `10**5000`.

## Standards

**PASS — 0 findings.**

The production Python delta passes `git diff --check`. Alignment is centralized in `core/rounding.py`, while instrument, economics, exits, and runner code dispatch through the typed seam. The legacy scalar branch remains intact. I found no documented-stage violation or actionable code smell.

## Spec

**PASS — 0 findings.**

Independent derivation confirmed:

- The policy enforces exactly six typed fields with the required fixed values.
- The valid domain is `{k/10 | 1 <= k <= 99999}` union positive integers `>=10000`.
- `FLOOR`, `CEIL`, and larger-on-tie `HALF_UP` are correct across the 9999.9/10000 boundary.
- Tiny-positive `FLOOR` refuses; `CEIL` and `HALF_UP` return `0.1`.
- Bool, nonnumeric, nonfinite, nonpositive, invalid-policy, and invalid-direction cases refuse.
- Policy and direction validation occur before the lossless integer shortcut.
- BUY fills dispatch to `CEIL`, SELL fills to `FLOOR`; long/short stops dispatch to `FLOOR`/`CEIL`; targets use `HALF_UP`. Runner paths propagate the evaluated policy into stop, target, trailing, and break-even calculations.
- Legacy scalar rounding remains unchanged.

The production instrument retains `price_tick: null`, `minimum_quantity: null`, `minimum_notional: 10`, `human_reviewer: null`, and no `admission_status`. No config, golden, `DERIVATIONS`, `core/economics.py`, production-cost, or production-funding path changed. PROBE-P012-04-A only adds the identical policy object; the prior replacement-count observation is not a mutation defect.

## Identity and preservation

- Worktree tracked state: clean.
- Current core tree: `ca57ca5e0487f92e05fa68d8217fdde486877a2c`.
- Seal: `54f41e7268442e1167946b587a5920a5ffe4baf99e4aa8964ef69e766bedebad`.
- Anchor: `9b58661ec4bd476eb584b41f9f6e2691e430da5d2374de83ec33fd3a389a22f9`.
- Ratified receipt: `cf82b102ba866fa08a86d8a6cb52ed43c2e2f2b71e35b081304e09e5aa368f11`.
- Structural comparison against original receipt `26748c7b7e09aa4830f507d023a54e7f7aa570c836e607dd2377bb9f42adf2f6` found exactly two differences: the ratification flag and signing time.
- Source and packet hashes matched for seven key policy, dispatch, record, anchor, and receipt files.
- All six receipt items remain `ACCEPTED_WITH_RESIDUAL_RISK`; all 27 production risks, five integration obligations, R29 semantic redo, `NONE_KEEP_REFUSED`, and production refusals remain.

The five `HIST-2026-0030` declaration diagnostics remain report-only historical metadata and are not converted into price-candidate findings.

## Limits

This PASS does not verify or authorize full P012, production data, live behavior, profitability, accounts, capture, deployment, trading, credentials, spend, outbound messages, merge, protected Python 3.12 Bridge CI, integration, the separate Opus review, Gemini 3.7 corroboration, or Lead reconciliation.

Full report: [SOL_T0_A2_REVIEW.md](/C:/tmp/P012_R34_SOL_T0_A2_20260911/results/SOL_T0_A2_REVIEW.md)  
Report SHA-256: `700c7fba7c2673dd067052ca1b9e100aa95ccbada8870547e9efbfd2d74bca57`