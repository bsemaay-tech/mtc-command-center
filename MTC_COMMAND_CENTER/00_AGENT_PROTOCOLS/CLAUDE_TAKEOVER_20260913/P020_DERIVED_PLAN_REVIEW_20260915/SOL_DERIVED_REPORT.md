# Exact Sol executing review — WP-P0-20 derived measurement plan

Reviewer slot: `gpt-5.6-sol`, `xhigh`, executing reviewer  
Date: 2026-09-15  
Scope: `OD-20260914-P020-MEASURE-1`, condition (c), derived plan and derivation tool only

## Result

The derived plan is the deterministic consequence of the frozen V1.6 bytes and the recorded one-shot outputs. All 15 trials are field-equal to their frozen sources, every non-trial base-plan value is preserved, N6-8 and N6-6 are closed, the original tool reproduced the accepted plan byte-for-byte, and the real driver accepted it. All five required driver mutation arms refused.

I found 0 REQUIRED findings and 2 NITs. The important execution condition is that the Lead must compare the installed plan's whole-file SHA-256 to the reviewed digest `d84b043a...` immediately before the one allowed run; merely recording an arbitrary plan digest would not close Q1.

## Verified identities — COMPUTED

I hashed the live files before inspecting subject contents or executing tests. The corresponding packet copies produced the same values.

| Artifact | Computed SHA-256 | Quoted/manifest identity | Result |
|---|---|---|---|
| live and packet `PRESELECTION_FROZEN.json` | `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126` | same | EQUAL |
| live and packet `PRESELECTION_ELIGIBILITY.json` | `fc5f8895a38147cbc76d93560b61f33cdea3b8215088acfbe6f6e8014c7bc6c2` | same | EQUAL |
| live and packet `PRESELECTION_CALIBRATION.json` | `808cbcb4ce529450e7e832baeffae00d00e64a57c456331936a75232c3299427` | same | EQUAL |
| live and packet `derive_benchmark_plan.py` | `0bfd18915a0952cbf8bd1058b5d560a5cd30558a3f2f6d2ae6706947152289d7` | same | EQUAL |
| live and packet `test_derive_benchmark_plan.py` | `185af7b237d11d6e9365716c4ff127eedc967d4a91f82b9107e016d95ad4c22a` | `185af7b2...` / same | EQUAL |
| live and packet `BENCHMARK_PLAN_DERIVED.json` | `d84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580` | same | EQUAL |
| live and packet base `BENCHMARK_PLAN.json` | `c6f07afd14301e640841e7f4ec95dfcef860df3a02e3ef3768c1513c517104c7` | same | EQUAL |
| live and packet `run_bounded_benchmark.py` | `3d4453cd23ad0f56ae0b34f94b21b7b1f3715f180091821b383369aa62fab324` | same | EQUAL |

`PACKET_SHA256SUMS.txt` contains 31 rows; I independently hashed every named packet file and observed `PACKET_MANIFEST_ALL_MATCH`. The manifest file itself computed as `5da3af24aa74423edf99e24d1b134362a210c19ddab57f1170a27c0f65e3f6f1`. The pinned interpreter reported `Python 3.12.12`.

## 1. Trial-by-trial conformance

For every row I compared `trial_id`, `strategy_id`, `strategy_family`, `timeframe`, `dataset_id`, `dataset_sha256`, `normalized_path`, `bar_interval_seconds`, `dataset_selection_order`, `symbol`, `input_rows`, `input_prefix_sha256`, and a deep equality comparison of `parameter_record`. The frozen source notation below means the named `family_order[].fixed_parameter_record`, `datasets[timeframe]`, and `measurement_inputs[timeframe].prefixes[input_rows]` objects.

| Trial | Frozen source | Result |
|---|---|---|
| `p020-01-GEN_TRIPLE_EMA_STACK-BTCUSDT-15m-n512` | `GEN_TRIPLE_EMA_STACK`; `15m`; `n512` | EQUAL |
| `p020-02-GEN_TRIPLE_EMA_STACK-BTCUSDT-15m-n1024` | `GEN_TRIPLE_EMA_STACK`; `15m`; `n1024` | EQUAL |
| `p020-03-GEN_TRIPLE_EMA_STACK-BTCUSDT-15m-n2048` | `GEN_TRIPLE_EMA_STACK`; `15m`; `n2048` | EQUAL |
| `p020-04-GEN_STOCH_OVERSOLD_CROSS-BTCUSDT-1h-n512` | `GEN_STOCH_OVERSOLD_CROSS`; `1h`; `n512` | EQUAL |
| `p020-05-GEN_STOCH_OVERSOLD_CROSS-BTCUSDT-1h-n1024` | `GEN_STOCH_OVERSOLD_CROSS`; `1h`; `n1024` | EQUAL |
| `p020-06-GEN_STOCH_OVERSOLD_CROSS-BTCUSDT-1h-n2048` | `GEN_STOCH_OVERSOLD_CROSS`; `1h`; `n2048` | EQUAL |
| `p020-07-GEN_KELTNER_BREAKOUT-BTCUSDT-2h-n512` | `GEN_KELTNER_BREAKOUT`; `2h`; `n512` | EQUAL |
| `p020-08-GEN_KELTNER_BREAKOUT-BTCUSDT-2h-n1024` | `GEN_KELTNER_BREAKOUT`; `2h`; `n1024` | EQUAL |
| `p020-09-GEN_KELTNER_BREAKOUT-BTCUSDT-2h-n2048` | `GEN_KELTNER_BREAKOUT`; `2h`; `n2048` | EQUAL |
| `p020-10-GEN_MACD_BULL_CROSS-BTCUSDT-4h-n512` | `GEN_MACD_BULL_CROSS`; `4h`; `n512` | EQUAL |
| `p020-11-GEN_MACD_BULL_CROSS-BTCUSDT-4h-n1024` | `GEN_MACD_BULL_CROSS`; `4h`; `n1024` | EQUAL |
| `p020-12-GEN_MACD_BULL_CROSS-BTCUSDT-4h-n2048` | `GEN_MACD_BULL_CROSS`; `4h`; `n2048` | EQUAL |
| `p020-13-GEN_DONCHIAN_BREAKOUT-BTCUSDT-1D-n512` | `GEN_DONCHIAN_BREAKOUT`; `1D`; `n512` | EQUAL |
| `p020-14-GEN_DONCHIAN_BREAKOUT-BTCUSDT-1D-n1024` | `GEN_DONCHIAN_BREAKOUT`; `1D`; `n1024` | EQUAL |
| `p020-15-GEN_DONCHIAN_BREAKOUT-BTCUSDT-1D-n2048` | `GEN_DONCHIAN_BREAKOUT`; `1D`; `n2048` | EQUAL |

There are exactly 15 trials in frozen family order. No requested field differs and no requested field is unbound to the frozen bytes.

## 2. Base-plan preservation

For nested values, “base value” is represented by a type plus the SHA-256 of canonical JSON; equality itself was a deep value comparison, not a digest-only comparison.

| Top-level key | Base value | Result |
|---|---|---|
| `plan_version` | `"p020-bounded-performance-v1"` | EQUAL |
| `task` | `"LOCAL RESEARCH ENGINEERING + BOUNDED PERFORMANCE"` | EQUAL |
| `execution_status` | `"UNEXECUTED"` | EQUAL |
| `owner_authorization` | `"AUTHORIZED_BOUNDED_SUCCESSOR_PATH_MEASUREMENT"` | EQUAL |
| `research_only` | `true` | EQUAL |
| `no_profitability_or_strategy_selection_results` | `true` | EQUAL |
| `not_representative_performance_feasibility_profitability_strategy_selection_or_acceptance` | `true` | EQUAL |
| `trade_bearing_requirement` | object; canonical SHA-256 `493d8fccbc2a745a64493392f45c71798fb4889841316bc0c3cde26b4903f877` | EQUAL |
| `manifest` | object; canonical SHA-256 `9ad21da7f18b3b69615c6a24d05028b19d7b9e22ed9ae7decc77f47cb029bd97` | EQUAL |
| `compatibility` | object; canonical SHA-256 `6dc6ea671b43628c416769368e4f911dc7557c22cd1388f9ea2abff88aab7383` | EQUAL |
| `implementation_sources` | object; canonical SHA-256 `34eac8ecb98cc21606c8afaaff4912a0ef066edd0d4f33d6f2bc28fcc91901c5` | EQUAL |
| `trial_policy` | object; canonical SHA-256 `b39cdf93d0bd25c25edec107b5e24dbd3d5a479eea9bb4f87fe754c9415b8cb0` | EQUAL |
| `p020_profile` | object; canonical SHA-256 `43ff6dd1e59d629ec611cf7fe591fc6e32ea5254c92c1c97bc3d73a478eb41fa` | EQUAL |
| `resource_measurement` | object; canonical SHA-256 `80b172035415755635193a9d96865238ee17dadc456ba4ead361ab9bc937461c` | EQUAL |
| `repetition` | object; canonical SHA-256 `281e765366c7d0bab179d0e3b357a0d28f3397e6f905b6dcf8fbc449c1b60807` | EQUAL |
| `output_contract` | object; canonical SHA-256 `9f50728f41a214bbe74d17fdfc4c2c0c3e03b018443f401cc98586d58b345330` | EQUAL |
| `trials` | list; canonical SHA-256 `7703dbd085e3af1d82396238e3629a549baf83083af0dbfe45ef10feb531132b` | DIFFERENT — required replacement |

No base key is missing. The only added top-level key is `derivation`; the only changed base key is `trials`. In particular, the V3/cost/funding pins and all requested policy, resource, repetition, and output-contract values are preserved.

## 3. Closure of N6-8 and N6-6

| Item | Status | Evidence |
|---|---|---|
| N6-8 — matching re-derivation | CLOSED | `derive_benchmark_plan.py:80-104` faithfully transcribes `preselect_profile.py:412-443`; `derive_benchmark_plan.py:107-138` requires an exact five-timeframe selection, five distinct frozen families, literal-boolean matrix eligibility, independently re-derives the lexicographically first matching, and refuses mismatch; `derive_benchmark_plan.py:141-162` returns only that verified selection. The behavioral difference is limited to refusal class/code. |
| N6-8 regression | CLOSED | `tests/test_derive_benchmark_plan.py:216-242` rewrites both selections and the matrix so the old cross-file/five-distinct/frozen-family checks would pass. It passes against the fixed tool, fails with `DID NOT RAISE SystemExit` when `verified_selection` is neutralized in a scratch copy, and passes again after restoration. |
| N6-6 — dead `base_plan` parameter | CLOSED | `derive_benchmark_plan.py:165` now declares `derive_trials(frozen, selection)` only. The actual base plan remains live where required: it is loaded and hashed at `:212-216`, deep-copied at `:221`, and its `trials` replaced at `:222`. |

The development behavior is the expected RED (pre-fix/neutralized hole) → GREEN (fixed code) → RED when the re-derivation is neutralized. My chronological verification was fixed GREEN → scratch mutation RED → restored GREEN; the restored copy returned to the exact original tool digest.

## 4. Input binding and exclusive output

- `load_json_once` reads a single byte buffer, hashes it, and parses that same buffer at `derive_benchmark_plan.py:31-40`. `derive_plan` calls it once for each of eligibility, calibration, base plan, and frozen artifact at `:212-216`. `tests/test_derive_benchmark_plan.py:271-283` counts exactly one `read_bytes` call for each; the full suite passed.
- Independently computed cross-checks all returned `True`: eligibility status is `PROFILE_ELIGIBLE_NOT_ACCEPTED`; eligibility and calibration both name the computed frozen digest; eligibility names the computed calibration digest; the two selections are equal; the independently re-derived selection equals the recorded selection and consists of five distinct frozen families.
- The derived block equals the computed eligibility, calibration, frozen, base-plan, and tool hashes. Its nine-entry `family_order` equals the frozen order; `selection_rederived` is literal `true`.
- `RUN_LOG.txt:2-6,10-12` contains the same five input/tool identities and output digest. The live re-run made `derived.json` with SHA-256 `d84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580`, byte-identical to the accepted plan.
- `write_once` uses `path.open("xb")` at `derive_benchmark_plan.py:237-242`. A second attempt against the same scratch output exited 2 with `REFUSED: output already exists`; the before/after SHA-256 remained `d84b043a...`.

## 5. Driver acceptance and RED arms

The real harness imports the real driver and changes only `PLAN_PATH` (`validate_derived_plan_harness.py:15-35`). The real accepted plan produced:

```text
driver sha256: 3d4453cd23ad0f56ae0b34f94b21b7b1f3715f180091821b383369aa62fab324
plan under validation: C:/tmp/CLAUDE_P0_RUN_20260913/P020_DERIVED_PLAN_20260914/BENCHMARK_PLAN_DERIVED.json d84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580
PLAN_VALID via run_bounded_benchmark._validate_plan: manifest datasets=93, trials=15, distinct families=5, sizes=[512, 1024, 2048], derivation.family_order=9 ids
EXIT_CODE=0
```

The D5 branch is at `run_bounded_benchmark.py:181-196`. It accepts a derived plan only when the selected `strategy_id` set contains five distinct members of `derivation.family_order`, with exactly sizes 512/1024/2048 for each.

| Scratch mutation | Plan SHA-256 | Exact driver refusal | Exit |
|---|---|---|---|
| all three STOCH `strategy_id` values duplicated as TRIPLE_EMA | `c479e2601845ea4e0f123d7af8b1a38bd4cf36e0f89d220c3e6ebbc59a597f0f` | `PLAN_INVALID: five families must each have sizes 512, 1024, 2048` | 2 |
| all three STOCH `strategy_id` values changed outside `family_order` | `66ab7e897e4a8fb069ec30a0dcd54e9bf813005791e8aa9f2cf194d49e2fad09` | `PLAN_INVALID: five families must each have sizes 512, 1024, 2048` | 2 |
| first `input_rows` changed to 4096 | `735d1069771f0303f8b0038419901f4f1da4ab3c14efb9a92aaffdb5fe7c7247` | `PLAN_INVALID: invalid input size in p020-01-GEN_TRIPLE_EMA_STACK-BTCUSDT-15m-n512` | 2 |
| first `dataset_sha256` tampered | `8dd70f0227e3709d762a0fae953aeb8713fbe8d41fdb4d57738e73779147cfeb` | `PLAN_INVALID: dataset hash mismatch in p020-01-GEN_TRIPLE_EMA_STACK-BTCUSDT-15m-n512` | 2 |
| `execution_status` changed to `EXECUTED` | `ff27d2e4370114e4fb9b2fb725c57826546730442c7756c71172f1fa0f96941e` | `PLAN_INVALID: execution_status must remain UNEXECUTED` | 2 |

The Q1 probe zeroed `eligibility_sha256`, `source_eligibility_sha256`, `calibration_sha256`, and `frozen_sha256` in another scratch plan. It still produced `PLAN_VALID`, exit 0, proving that the driver reads only `derivation.family_order` from that block.

## Q1 — NIT

For this once-only Lead execution, the documentary chain is sufficient only when the installed plan is compared to the reviewed whole-file digest `d84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580` before validation, immediately before `--run`, and after the run. The derivation was independently reproduced from the exact live inputs; the plan hash commits to every derivation digest and every trial; `_source_identity` records the actual plan SHA-256 in the journals/report (`run_bounded_benchmark.py:531-543`); and `_validate_plan` separately binds the executable datasets, manifest, compatibility record, detached records, and implementation sources.

The driver does not itself validate the derivation provenance: `run_bounded_benchmark.py:185-194` consumes only `family_order`, as the zeroed-digest probe demonstrated. That is a defense-in-depth NIT, not a blocker for this one reviewed, digest-pinned Lead run. A future general/repeatable run path should pin or validate the derivation inputs. Changing the driver immediately would itself change the reviewed driver identity and trigger another review cycle; the fixed whole-plan comparison is the smaller safe control here. A launcher that merely records, but does not assert, the installed plan equals `d84b043a...` is not sufficient.

## Q2 — SOUND

The swap does not invalidate an identity check on the measurement path. `--run` has no `--plan` option and loads `ROOT/BENCHMARK_PLAN.json` at `run_bounded_benchmark.py:19-20,85-92,671-688`; it does not compare that file to the frozen artifact's historical base-plan pin. The derived plan records `derivation.base_plan_sha256 = c6f07afd...`, and all non-trial base values are preserved. `verify_frozen_identity` belongs to the completed `--oneshot` path and must not be invoked during the swap.

The sound procedure is a temporary substitution:

1. Before mutation, verify and record the base at `BENCHMARK_PLAN.json` as `c6f07afd...`; create/verify `BENCHMARK_PLAN_BASE_c6f07afd.json`; verify the source derived plan as `d84b043a...`.
2. Install the exact derived bytes at `BENCHMARK_PLAN.json`, update only its line in `SHA256SUMS_V16.txt`, assert the installed digest is `d84b043a...`, and run in-place `--validate-plan`.
3. Immediately before the single `--run`, re-assert plan `d84b043a...`, driver `3d4453cd...`, the selected manifest, compatibility, every implementation source, all three records and sidecars, and the owner/roster terminal. Record UTC time, exact command, exit, and that the chosen external output root did not exist.
4. After the run, record the same source hashes again plus the hash of every output file, journal/checkpoint, and report. Preserve the exact stdout/stderr and terminal result.
5. After all post-run capture, restore the base plan at the canonical path, restore the checksum-manifest line, and verify `c6f07afd...` again. Thus the derived plan occupies `BENCHMARK_PLAN.json` only for the bounded validation/run interval.

Leaving the derived plan permanently at the base path would create avoidable ambiguity for later frozen-identity checks; a temporary substitution is preferable. No `--oneshot` invocation is valid during or after this procedure.

## Q3 — SOUND

The executable rule is a mechanical transcription of the owner-approved shape and `DERIVATION_RULE.md:5-7`:

- five recorded family/timeframe pairs are independently re-derived as the lexicographically first complete matching of five distinct families;
- the pairs are ordered by the frozen family order;
- each pair receives sizes 512, 1024, and 2048, producing exactly 15 trials;
- each trial copies the frozen dataset fields, prefix hash, and one fixed parameter record;
- only `trials` is replaced, `derivation` is added, and all other base values are preserved;
- `PROFILE_ELIGIBLE_NOT_ACCEPTED` is required, so the tool cannot derive from a blocked one-shot; the driver's `_reserve_output_root` requires a new non-existing root at `run_bounded_benchmark.py:586-593`.

The embedded `RULE_TEXT` at `derive_benchmark_plan.py:17-24` is a derivation summary rather than a complete runbook; it does not contradict the fuller matching and run-gate rule enforced by the surrounding code and documents.

There is no choice left to the tool or Lead over what is measured. The small implementation-defined details are deterministic:

- Ordering is frozen-family order, then fixed size order. Iteration over the recorded selection object cannot alter pair order because the verified selection maps each timeframe to a distinct family.
- `symbol_from_dataset` (`derive_benchmark_plan.py:51-65`) prefers an explicit frozen symbol, then deterministically derives it from normalized path or dataset ID. All live sources resolve to `BTCUSDT`, and driver validation requires equality with the pinned manifest. The fallback could influence profile metadata only for a future internally inconsistent frozen artifact; it cannot change these reviewed bytes.
- The `p020-NN-{family}-{symbol}-{timeframe}-n{size}` trial-ID format (`derive_benchmark_plan.py:191-206`) is implementation-defined but deterministic. It influences journal/checkpoint identity and labels, not strategy, dataset, prefix, size, or parameters.
- JSON formatting is deterministic and affects only byte identity, not the measured workload.

## 8. Boundary

The derivation tool reads and compares identity/status/selection structure, the binary eligibility matrix, frozen dataset/parameter records, and the base plan. It does not read or compare returns, PnL, rankings, or any economic result. The derived plan contains no outcome, ranking, or PnL and preserves the publication-boundary booleans and `output_contract` exactly.

The measurement output contract is unchanged. `run_bounded_benchmark.py:596-668` still performs interrupted/resumed and uninterrupted-reference journals, compares semantic results with timing removed, and emits `acceptance_verdict: NOT_EVALUATED`, `profitability_or_strategy_selection_result: NOT_PUBLISHED`, and `semantic_comparison_timing_excluded`.

## 9. Residuals carried

| Residual | Measurement-path effect |
|---|---|
| Opus N6-1/N6-7 and Sol-6-3 — stale annotations/pins | No executable effect. These are documentation/annotation fields; the driver consumes the pinned records and sources. They should be repaired at the next re-freeze, not by changing the reviewed bytes before this run. |
| Opus N6-3 — cost/funding `end_exclusive = 2025-09-22T08:00Z` | The cost/funding records are measurement inputs, but the reported mismatch concerns the later 15m calibration window. The fixed measurement prefixes end within the declared interval (`BENCHMARK_PLAN.json:307-308`), and the pinned economics implementation does not enforce the interval. It is inert for this measurement and remains an owner lever afterward. |
| Opus N6-2 / Sol-6-1 / Sol-6-2 — exclusive-create versus lock and abort recovery | None. These are confined to the completed `--oneshot` transaction path, which must not run again. |

## Findings

1. **NIT — the driver does not validate derivation provenance fields.** `run_bounded_benchmark.py:185-194` reads only `derivation.family_order`; `:531-543` records the whole plan hash but no individual derivation inputs. A plan with zeroed eligibility/calibration/frozen digests still validated. For this run, require exact installed-plan equality to `d84b043a...` before/after as stated in Q1. Future reusable execution should validate the derivation pins.
2. **NIT — derivation-rule documentation retains stale post-fix identities/citations.** `DERIVATION_RULE.md:50-51` labels old tool/test digests as V1.6 pins (`308aa0b8...`, `4adb69a0...`) although the computed current identities are `0bfd1891...` and `185af7b2...`; `DERIVATION_RULE.md:44` also cites the copied `family_order` at old tool line `:167` rather than current `:229`. The packet manifest and executable identities are correct, so this does not touch the measurement path. Repair on the next documentation re-freeze.

There are no REQUIRED findings.

## Commands run and exact observed results

All commands used cwd `C:\tmp\P020_DERIVED_SOL_SCRATCH_20260915`. No command used a repository as cwd.

### Identity and source inspection

- `Get-FileHash -Algorithm SHA256` over the seven explicitly pinned live files and packet copies returned the exact values in the identity table, with no missing file.
- The same command over both live and packet tool tests returned `185af7b237d11d6e9365716c4ff127eedc967d4a91f82b9107e016d95ad4c22a` twice.
- Recursive packet hashing followed by parsing `PACKET_SHA256SUMS.txt` observed:

```text
MANIFEST_ROWS=31
PACKET_MANIFEST_ALL_MATCH
```

- `Get-Content` with numbered ranges covered the complete 261-line derivation tool; `preselect_profile.py:412-443,1102-1154`; complete 336-line derivation tests in continuations; driver `:1-230,430-545,560-692`; complete harness; `DERIVATION_RULE.md`; owner handoff; `RUN_LOG.txt`; `REPORT_FIX2.md`; Lead terminal; relevant adjudication and runbook ranges. `rg -n` located the plan-swap, derivation, owner-decision, interval, and residual references. These read-only commands all exited 0.
- Interpreter:

```text
Python 3.12.12
```

### Mandated tool tests

Command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\tmp\P020_IMPL_20260912\01a0924d-2c4b-7da1-99e1-24e2a7c7685c\.venv\Scripts\python.exe' -m pytest 'C:\tmp\P020_PLAN_DERIVE_20260913\tests' -q -p no:cacheprovider
```

Observed:

```text
................                                                         [100%]
16 passed in 0.97s
```

Targeted fixed regression:

```text
.                                                                        [100%]
1 passed in 0.36s
```

The scratch copy began with the same tool digest `0bfd1891...`. After inserting `return dict(recorded)` before re-derivation, the targeted test observed:

```text
F                                                                        [100%]
E       Failed: DID NOT RAISE SystemExit
FAILED red_tool/tests/test_derive_benchmark_plan.py::test_refuses_consistently_rewritten_matrix_and_selection
1 failed in 0.21s
```

After restoring the scratch copy:

```text
.                                                                        [100%]
1 passed in 0.07s
RESTORED_COPY_SHA256=0bfd18915a0952cbf8bd1058b5d560a5cd30558a3f2f6d2ae6706947152289d7
```

### Original-tool re-derivation

Command:

```powershell
& 'C:\tmp\P020_IMPL_20260912\01a0924d-2c4b-7da1-99e1-24e2a7c7685c\.venv\Scripts\python.exe' 'C:\tmp\P020_PLAN_DERIVE_20260913\derive_benchmark_plan.py' --eligibility 'C:\tmp\P020_PRESELECT_20260913\PRESELECTION_ELIGIBILITY.json' --calibration 'C:\tmp\P020_PRESELECT_20260913\PRESELECTION_CALIBRATION.json' --base-plan 'C:\tmp\P020_LEAD_20260912\benchmark\BENCHMARK_PLAN.json' --out 'C:\tmp\P020_DERIVED_SOL_SCRATCH_20260915\derived.json'
```

Observed:

```text
EXIT_CODE=0
DERIVED_SHA256=d84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580
EXPECTED_SHA256=d84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580
BYTE_IDENTICAL=True
```

Repeating against the existing scratch path observed:

```text
EXIT_CODE=2
BEFORE_SHA256=d84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580
AFTER_SHA256=d84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580
UNCHANGED=True
REFUSED: output already exists: C:\tmp\P020_DERIVED_SOL_SCRATCH_20260915\derived.json
```

### Real-driver harness and mutations

Command form:

```powershell
& 'C:\tmp\P020_IMPL_20260912\01a0924d-2c4b-7da1-99e1-24e2a7c7685c\.venv\Scripts\python.exe' 'C:\tmp\CLAUDE_P0_RUN_20260913\P020_DERIVED_PLAN_20260914\validate_derived_plan_harness.py' [PLAN]
```

The accepted-plan output and all five required refusal messages/exits are reproduced exactly in section 5. The additional zeroed-derivation-digest probe observed:

```text
plan under validation: C:/tmp/P020_DERIVED_SOL_SCRATCH_20260915/plan_unpinned_derivation_digests.json 15c8a942aafd0f6c0e485cbe30663ea3806d5012dae62364a54b9823a459647e
PLAN_VALID via run_bounded_benchmark._validate_plan: manifest datasets=93, trials=15, distinct families=5, sizes=[512, 1024, 2048], derivation.family_order=9 ids
EXIT_CODE=0
```

### Independent conformance helper

The scratch-only `review_checks.py` deep-compared the frozen, calibration, eligibility, base, and derived JSON objects and independently ran the matching search. Its decisive output was:

```text
TRIALS_ALL_EQUAL=True
TRIAL_COUNT=15
MISSING_KEYS=[]
ADDED_KEYS=["derivation"]
CHANGED_KEYS=["trials"]
selection_independently_rederived=True
five_distinct_frozen_families=True
INPUT_BINDING_ALL_EQUAL=True
```

One earlier inline `python -c` version exited 1 with a Windows-quoting `SyntaxError` before loading any review input; it produced no evidence and was replaced by the successful scratch helper above.

## NOT VERIFIED

- I did not run `run_bounded_benchmark.py --run`; this was forbidden. Therefore no throughput, restart result, resource measurement, or measurement output is verified by this report.
- I did not run `preselect_profile.py --oneshot`; this was forbidden and the one-shot is already spent.
- I did not perform the future in-place plan swap or launcher ceremony because every benchmark/procedure/derived directory was read-only to this reviewer. Q2 assesses the procedure from source and computed identities only.
- I did not re-review the settled V1.6 roster, economic-record policy, profitability, strategy quality, or production suitability.
- I made no network call, Git command, repository change, or write into any named read-only directory.
- The unavailable Grok pre-screen slot and the future Gemini result are roster matters for the Lead; this report neither fills nor waives them and does not authorize measurement.

VERDICT: PASS-WITH-NITS
