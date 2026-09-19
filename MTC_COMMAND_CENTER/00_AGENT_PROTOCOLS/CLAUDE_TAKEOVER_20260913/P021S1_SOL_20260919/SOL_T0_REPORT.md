# Independent T0 Review — WP-P0-21 S1

Independent second-flagship review of candidate `eada65edfeacef9ebbe5b237d8e111caf36052e4` against base `fcac0ac6`. I did not read any Opus report or any Lead adjudication.

## Verified identities

- Required worktree: `C:/tmp/P021_S1_20260915`.
- COMPUTED HEAD, using only the permitted command `git -c safe.directory=* -C C:/tmp/P021_S1_20260915 rev-parse HEAD`: `eada65edfeacef9ebbe5b237d8e111caf36052e4` — exact match.
- Catalogue worktree-file SHA-256: `B8FA0AE82F7ED2EA12072720E46FCDB16426E7EAC2FCC52A936CCB6AA0AF095B`.
- Catalogue committed-blob SHA-256, computed directly from the permitted `git show eada65ed...:MTC_COMMAND_CENTER/03_QUANTLENS/tools/p021_readiness_rules.py` byte stream: `84FC82CAB8A84AE7492E48A26EB67E370A8F5B5B0B0C52D88051ED86968BCEDF`. The two SHA-256 values differ only because the checked-out file has CRLF line endings and the committed blob has LF line endings.
- Primary decision identity: `C:/CT13/DECISIONS.md:132` records `OD-20260915-P021-S2-RECOMMENDED-1` and the four selected values/pins. The owner-word provenance is independently present at `OWNER_ANSWERS_20260915.md:82-86`.

## Fidelity

| Owner-selected item | Code evidence | Result |
|---|---|---|
| B-02: `P021_DECISION_3 = T`; `gap_ratio_max = 0.0001` on `m2_missing_bar_ratio` | `p021_readiness_rules.py:58`, `:172-184`, `:252-254`; decision row `C:/CT13/DECISIONS.md:132`; packet `P021_OPTIONS_PACKET_S2_20260915.md:13-20` | **EQUAL** |
| B-17 formula pin: `m2_missing_bar_ratio@data_gap_ratio.py v1 (fixed-step 24/7, half-open span, leading/trailing absence excluded)` | `p021_readiness_rules.py:199-203`, `:254`; decision row `:132`; packet `:22-23` | **EQUAL** |
| B-13: `dataset_hash_required` is satisfied by the `ds-v1` digest of the scanned bundle | `p021_readiness_rules.py:251`, `:255`; decision row `:132`; packet `:25-26` | **EQUAL** for the selected pin; see NIT-2 about naming the carrier field |
| B-05: option M-C, M-B signal-fidelity gate plus M-A signed mean realized-return difference, each with its own B-06 tolerance | `p021_readiness_rules.py:59`, `:190-194`, `:205-223`, `:283-292`; decision row `:132`; packet `:28-35` | **EQUAL** |

The M-A/M-B/M-C word content is preserved, with only Unicode table punctuation normalized to ASCII. The candidate contains signed realized return, count, standard deviation, intent agreement, and two independently open tolerances. It contains none of the repaired-out `absolute`, `R-multiple`, or `size class` concepts and adds no B-04 dependency.

## Fence proof

All commands below ran from `C:/tmp/P021_S1_20260915`. Scratch-only artifacts and pytest basetemp were under `C:/tmp/SOL_P021S1_SCRATCH`.

### Pinned self-check

Command (the interpreter path reports Python 3.12.12):

```powershell
$py312='C:\Users\BarışSemaay\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\python.exe'
$env:PYTHONPATH='MTC_COMMAND_CENTER/contracts;MTC_COMMAND_CENTER/03_QUANTLENS/tools'
& $py312 --version
& $py312 MTC_COMMAND_CENTER/03_QUANTLENS/tools/p021_readiness_rules.py --self-check
```

Output:

```text
Python 3.12.12
SELF-CHECK PASS: 7 checks all refuse readiness
CLOSED NUMBERS: 13 (profile balanced, provisional)
OPEN NUMBERS: 4
MODIFIED COPY DETECTED: divergence tolerance refusal wiring removed
S2 CLOSED (catalogue only): gap_ratio_max=0.0001 on m2_missing_bar_ratio; B-17 formula pin 'm2_missing_bar_ratio@data_gap_ratio.py v1 (fixed-step 24/7, half-open span, leading/trailing absence excluded)'; B-13 ds-v1 pin; B-05 metric M-C
MODIFIED COPY DETECTED: swing_forward_period closure removed
READY=False
```

### Exact three-module suite

The bare 3.12 installation did not contain pytest. I ran the suite with that exact 3.12.12 interpreter and already-installed local dependencies: pytest 9.0.2 plus a CPython-3.12-compatible pydantic 2.13.4 / pydantic-core 2.46.4. Nothing was installed or changed in the repository.

```powershell
$env:PYTHONPATH='MTC_COMMAND_CENTER/contracts;MTC_COMMAND_CENTER/03_QUANTLENS/tools;C:\Users\BarışSemaay\AppData\Roaming\uv\tools\litellm\Lib\site-packages;C:\Users\BarışSemaay\AppData\Roaming\Python\Python314\site-packages'
& $py312 -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p021_eligibility.py MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_strategy_type_policy_set.py MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_data_gap_ratio.py -q -p no:cacheprovider --basetemp C:/tmp/SOL_P021S1_SCRATCH/bt
```

```text
........................................................... [100%]
59 passed, 108 subtests passed in 0.36s
```

### Independent fail-closed mutant

My scratch mutant replaced `P021.DATA_QUALITY.missing_rules` with `()`. Direct `validate_catalog` rejected it with `P021.DATA_QUALITY could be presented as ready`. With that mutant temporarily installed as `RULES`, `readiness_record()` raised the same validation error before it could return any record. The unmodified control returned `ready is False`. This agrees with `p021_readiness_rules.py:352-354` and the hard refusal at `:357-378`.

### Independent repair mutants

- Restoring the exact pre-repair definition from `7fecf204` was caught by the packet-text fence; it lacks signed realized return and intent-agreement wording and contains the forbidden absolute R-multiple/side-size statistic.
- Collapsing B-06 back to a single `divergence_tolerance` was caught by the two-name assertion and by `validate_catalog`: `missing=['divergence_tolerance_intent', 'divergence_tolerance_return']; extra=['divergence_tolerance']`.

### RED arms 1-2

- RED arm 1 loaded exact `fcac0ac6` catalogue bytes into the candidate test fence. It failed in setup because `DATA_QUALITY.limits` had no `gap_ratio_max` (`KeyError`).
- RED arm 2 loaded exact `fcac0ac6` test bytes against the candidate catalogue. It failed on the open-name set: the candidate has `divergence_tolerance_intent` and `divergence_tolerance_return`, while the old test expects `gap_ratio_max` and one `divergence_tolerance`.

Both RED arms used only permitted `git show <rev>:<path>` byte reads inside `C:/tmp/SOL_P021S1_SCRATCH/red_arms_1_2.py`.

## Artifact statement

The catalogue/artifact difference is real and intentionally non-actionable in this slice:

- Catalogue: `gap_ratio_max = 0.0001` (`p021_readiness_rules.py:172-184`, `:252`).
- Accepted hashed fixture: `gap_ratio_max = None` and version `p021pol-v1:4a807136e78650ef393556f91d3448855fc397ee9f0eee6efb7594c9dbdf69f2` (`test_strategy_type_policy_set.py:21-57`, specifically `:44` and `:56`).
- `git diff fcac0ac6 eada65ed... -- MTC_COMMAND_CENTER/03_QUANTLENS/tools/strategy_type_policy_set.py` is empty. The base-to-candidate diff of the fixture test changes only a comment and the catalogue open-name expectation; the fixture and hash are byte-unchanged. The repair diff `7fecf204..eada65ed` changes only the catalogue open-name expectation at `test_strategy_type_policy_set.py:116-123`.
- Repository-wide consumer tracing found no master production consumer that imports/reads both sources. `data_gap_ratio.py:9` and `strategy_type_classifier.py:9` consume only the hashed-policy validator. The sole file importing both APIs is `tests/test_strategy_type_policy_set.py:13-18`, which asserts refusal and cannot act on trading/readiness.

Therefore no consumer on master can act on the `0.0001`/`None` difference. Ratifying and re-hashing the whole policy-set artifact remains the owner's B-22 act, not this review's.

## Formula-pin statement

`data_gap_ratio.py` computes m2 honestly as pinned:

- Fixed-step 24/7 calendar: `TIMEFRAME_SECONDS` at `:12-19`, selected at `:53-56`.
- Numerator: adjacent timestamp deltas only (`:58-60`); gaps above `1.5 * step`, missing slots `round(delta / step) - 1`, and their sum (`:69-71`).
- Denominator: observed endpoint span `last - first` (`:62`) converted to expected bars with the final observed bar included (`round(span / step) + 1`, `:65`), equivalent to the half-open bar interval `[first, last + step)` for fixed-step timestamps.
- m2: `missing_bars / expected_bars` at `:85`, returned as `m2_missing_bar_ratio` at `:100`.
- Leading/trailing absence is excluded because only the first-through-last observed timestamps define the span; the direct test at `test_data_gap_ratio.py:90-94` confirms this.

## Scope

A full permitted two-SHA comparison (`git diff fcac0ac6 eada65ed... -- .`) contains exactly three files:

1. `MTC_COMMAND_CENTER/03_QUANTLENS/tools/p021_readiness_rules.py`
2. `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p021_eligibility.py`
3. `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_strategy_type_policy_set.py`

All are under `03_QUANTLENS/tools`; none is a protected path. The unused `import json` at `test_strategy_type_policy_set.py:4` is present in exact `fcac0ac6` bytes and was not touched by this slice, so the known F401 is not a candidate regression.

## Findings

### Standards

- **NIT-1 — stale module contract prose:** `p021_readiness_rules.py:7-15` still says “the gap ratio and the three divergence numbers stay open.” The candidate closes the gap ratio and represents M-C using two B-06 tolerances plus two B-07 quantities (`:172-194`). Runtime behavior, self-check, and tests are correct; update the docstring when convenient.
- No new hard documented-standard violation or material Fowler-baseline smell in the diff. The slice is narrow, uses existing catalogue types, and introduces no speculative dependency or abstraction.

### Spec

- **NIT-2 — B-13 carrier name is implicit:** `p021_readiness_rules.py:251-255` records `dataset_hash_required=True` and `dataset_hash_contract='ds-v1'`, but does not name the decision/packet's measured-value carrier `dataset_manifest_hash` (`C:/CT13/DECISIONS.md:132`; packet `:25-26`). The selected contract itself is faithful and there is no consumer yet, so this is optional precision rather than a required correction.
- No REQUIRED finding. All four owner-selected values/pins are equal to the primary decision and packet, every check remains refused, and the repair-specific regressions are fenced.

Summary: Standards — 1 NIT, no hard violation. Spec — 1 NIT, no REQUIRED finding.

## NOT VERIFIED

- Ruff was not installed or available locally, so I did not produce a Ruff run. The specified pytest/self-check suite and direct base-byte attribution of the pre-existing F401 were completed.
- I did not inspect any Opus report, Lead verification report, Gemini report, or Lead adjudication; all conclusions above come from primary decision/packet bytes, candidate/base bytes, repository sources, and my own executions.
- No live, testnet, deployment, merge, commit, or trading behavior was exercised; none is authorized or part of this catalogue-only review.

VERDICT: PASS-WITH-NITS
