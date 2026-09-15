# P012 R34 independent Sol T0 price review

Reviewer: `gpt-5.6-sol`, xhigh, fresh independent T0 session  
Date: 2026-09-11  
Scope: frozen synthetic price-policy candidate only

## Verdict

**PASS** for the bounded synthetic-only `HYPERLIQUID_PX_V1` price candidate at exact HEAD `3faed08866e122158e93c626288873ec58a42e3d` against base `3e86faec032407c1af9a75f8b8852222d732f316`.

Material findings: **none**. Optional nits: **none**. No findings are suppressed.

This verdict is not full P012 acceptance and grants no production, trading, deployment, capture, credential, spend, messaging, merge, CI, or integration authority.

## Personally executed QA

Runtime identity:

- Executable: `C:\Python314\python.exe`
- Version: `3.14.2 (tags/v3.14.2:df79316, Dec 5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)]`
- `pytest`: `9.0.2`
- Imported `mtc_v2` root: `C:\tmp\P012_PRICE_20260910\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2`

Required full gate, executed first with the original Python argv and PowerShell stdout/stderr redirection to the requested log:

```text
C:/Python314/python.exe -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --root C:/tmp/P012_PRICE_20260910/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2 --baseline-root C:/tmp/P012_PRICE_BASELINE34_20260911/CURRENT --output C:/tmp/P012_R34_SOL_T0_A2_20260911/results/full_gate.json
```

- Actual exit: `0`
- Wall time observed by the command runner: `33.1s`
- Contract selftests: `558 passed`, `0 failed`, return code `0`
- Gate: zero acceptance blockers; 17 scenarios / 34 surfaces reproduced; catalog 9 RED, 8 GREEN, 10 PROBE; expected-source provenance `MATCH`
- Claim: `BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_ACCEPTED`
- Results: `C:\tmp\P012_R34_SOL_T0_A2_20260911\results\full_gate.json`
- Log: `C:\tmp\P012_R34_SOL_T0_A2_20260911\results\full_gate.log`

Required focused tests, executed second:

```text
C:/Python314/python.exe -m pytest C:/tmp/P012_PRICE_20260910/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_price_alignment_policy.py C:/tmp/P012_PRICE_20260910/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_economic_records.py C:/tmp/P012_PRICE_20260910/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_results_corrected.py C:/tmp/P012_PRICE_20260910/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_w285_kernel_remaining.py -q -p no:cacheprovider --basetemp C:/tmp/P012_R34_SOL_T0_A2_20260911/scratch/pytest-temp
```

- Actual exit: `0`
- Result: `113 passed`, `1 warning`, in `0.58s`
- Log: `C:\tmp\P012_R34_SOL_T0_A2_20260911\results\focused_pytest.log`
- The warning is the environment's unknown `cache_dir` pytest option. It did not fail QA and is not a price-candidate finding.

I also executed a local-only targeted edge probe:

```text
C:/Python314/python.exe C:/tmp/P012_R34_SOL_T0_A2_20260911/scratch/price_edge_probe.py
```

It exited `0` and checked 11 independently selected lattice boundaries, invalid input/policy/direction refusals, and exact plain-`int` plus `int`-subclass preservation for `2**53+1`, `10**400`, and `10**5000`. The subclass deliberately raises if converted to text, so the pass confirms the retained integer shortcut avoids lossy/string conversion. Log: `C:\tmp\P012_R34_SOL_T0_A2_20260911\results\targeted_edges.log`.

## Frozen identity checks

- Actual Git HEAD matched `3faed08866e122158e93c626288873ec58a42e3d`; tracked worktree status was clean.
- Packet manifest file SHA-256 matched `2f4ac4a45f3511a4dadb7426e2007b687284474bf95bd24f4ea123d1c7b480b8`.
- Section-16 reviewed source `b7975ae6c935c461c479768c5f252f930fbc1800` is an ancestor. Its successor delta contains exactly `DECISIONS.md`, `semantic_coverage_review.json`, and `P012_PRICE_R34_RESUME_20260911.md`; no core or seal member changed.
- Current `mtc_v2/core` tree matched `ca57ca5e0487f92e05fa68d8217fdde486877a2c`.
- Gate-reported seal matched `54f41e7268442e1167946b587a5920a5ffe4baf99e4aa8964ef69e766bedebad` and implementation anchor matched `9b58661ec4bd476eb584b41f9f6e2691e430da5d2374de83ec33fd3a389a22f9`.
- Ratified receipt SHA-256 matched `cf82b102ba866fa08a86d8a6cb52ed43c2e2f2b71e35b081304e09e5aa368f11`. A structural comparison with original receipt `26748c7b7e09aa4830f507d023a54e7f7aa570c836e607dd2377bb9f42adf2f6` found exactly two changes: `owner_ratification.ratified` (`false` to `true`) and `signed_at`.
- `OWNER_APPROVAL.md` records the contextual exact words `ı approve continue`; I treated this only as continuation authority, not semantic evidence.
- I independently SHA-256 compared the source and packet copies of `rounding.py`, `instrument.py`, `exits.py`, `runner.py`, the Hyperliquid instrument record, `implementation_anchor.json`, and the ratified receipt. All seven pairs matched.

## Standards

**PASS — 0 findings.** The four production Python changes pass `git diff --check`. The policy is centralized in `core/rounding.py`; instrument, fill, exit, and runner code dispatch through that seam without introducing another state owner or changing the legacy scalar branch. I found no documented stage-rule violation or actionable smell in the bounded price delta. Required probe-kernel copies are test-harness artifacts, not a second production implementation.

## Spec

**PASS — 0 findings.** My independent derivation agrees with the implementation:

- `core/rounding.py:12-54` enforces the typed policy's exact six fields, exact values, and field types.
- `core/rounding.py:57-115` admits exactly `{k/10 | 1 <= k <= 99999}` plus positive integers at and above 10000. Below 10000 it chooses adjacent tenths; from 10000 it chooses adjacent integers. `FLOOR`, `CEIL`, and larger-on-tie `HALF_UP` therefore match the required order statistics, including the discontinuity at 9999.9/10000 and tiny-positive refusal for `FLOOR`.
- Policy and direction validation precede the integer shortcut. Bool, nonnumeric, nonfinite, and nonpositive inputs refuse. Positive Python integers and subclasses return without float conversion or precision loss.
- `core/instrument.py:219-223,324-359,374-411` enforces scalar-versus-policy exclusivity, constructs the typed policy, and exposes the same public rounding methods.
- `core/economics.py:262-280` dispatches BUY to `CEIL` and SELL to `FLOOR`. `core/exits.py:185-223` dispatches long stops to `FLOOR`, short stops to `CEIL`, and target construction to `HALF_UP`; trailing and break-even stops reuse the same stop alignment. `core/runner.py` passes the evaluated instrument policy into actual stop/target/trailing/break-even paths.
- The scalar `price_tick` fallback remains intact and the focused tests confirm unchanged legacy scalar behavior.

The production Hyperliquid record has `price_tick: null`, the exact six-field policy, `minimum_quantity: null`, `minimum_notional: 10`, and `provenance.human_reviewer: null`; it has no `admission_status`. Its diff adds only the policy object. No config, golden, `DERIVATIONS`, `core/economics.py`, production cost, or production funding path changed. The PROBE-P012-04-A instrument patch likewise only adds that policy object; its current bytes equal the core instrument record. The earlier naive replacement count of two is therefore not a mutation defect.

All six receipt items remain `ACCEPTED_WITH_RESIDUAL_RISK`. The receipt retains the 27 production residuals, five Section-19 integration obligations, R29 production-semantic redo, synthetic-only isolation, and fail-closed production posture. `NONE_KEEP_REFUSED` remains controlling; successful synthetic QA does not publish or validate production facts.

## Report-only diagnostics and limits

The full gate reports five declaration diagnostics under historical `HIST-2026-0030` report-only mode: four chain-unverifiable entries and one stale Section-16 status declaration. They are unenforced, produce no acceptance blocker, and predate this price-code successor; I do not convert them into a new candidate finding. Baseline `EXPECTED_SEAL_SHA_consumed` is treated only as Lead attestation, not as proof of driver consumption.

I did not repeat Section 16, re-review the 191 unchanged historical hunks, or claim whole-domain/formal verification beyond the simple price lattice and targeted checks. I did not verify full P012, production data, live behavior, profitability, account/capture state, Bridge Python 3.12 protected CI, authorized integration, the separate Opus review, mandatory Gemini 3.7 corroboration, or Lead reconciliation. Those gates and every production refusal remain outstanding and outside this verdict.

Summary: Standards `0` findings, Spec `0` findings; no worst issue on either axis. **Bounded verdict: PASS.**
