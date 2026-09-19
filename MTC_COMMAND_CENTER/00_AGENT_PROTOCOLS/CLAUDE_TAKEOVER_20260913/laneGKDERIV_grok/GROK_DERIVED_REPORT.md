# GROK_DERIVED_REPORT — WP-P0-20 derived measurement plan + derivation tool

Slot: grok-4.6, independent detection pre-screen (lane GKDERIV). Supplemental: cannot accept; does not replace exact reviewers. Owner rows `OD-20260914-P020-MEASURE-1` condition (c) and `OD-20260915-P020-MEASURE-GROK-1`. Worked only in `C:/tmp/GROK_SCRATCH_GKDERIV/` after copying the tool dir and the derived-plan dir. Originals were not written. No `--run`, no `--oneshot`, no git, no network.

Pinned interpreter: `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe` — `Python 3.12.12 (main, Jan 27 2026, 23:45:36) [MSC v.1944 64 bit (AMD64)]`.

## Verified identities (COMPUTED before reading subject contents)

| Artifact | Computed SHA-256 | Brief pin | Result |
|---|---|---|---|
| `P020_DERIVED_PLAN_20260914/BENCHMARK_PLAN_DERIVED.json` | `d84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580` | `d84b043a…` | EQUAL |
| `P020_PLAN_DERIVE_20260913/derive_benchmark_plan.py` | `0bfd18915a0952cbf8bd1058b5d560a5cd30558a3f2f6d2ae6706947152289d7` | `0bfd1891…` | EQUAL |
| scratch copy of the tool (same bytes) | `0bfd18915a0952cbf8bd1058b5d560a5cd30558a3f2f6d2ae6706947152289d7` | `0bfd1891…` | EQUAL |
| `tests/test_derive_benchmark_plan.py` | `185af7b237d11d6e9365716c4ff127eedc967d4a91f82b9107e016d95ad4c22a` | (Lead/packet) | EQUAL |
| `PRESELECTION_FROZEN.json` | `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126` | `cb756020…` | EQUAL |
| `PRESELECTION_ELIGIBILITY.json` | `fc5f8895a38147cbc76d93560b61f33cdea3b8215088acfbe6f6e8014c7bc6c2` | `fc5f8895…` | EQUAL |
| `PRESELECTION_CALIBRATION.json` | `808cbcb4ce529450e7e832baeffae00d00e64a57c456331936a75232c3299427` | `808cbcb4…` | EQUAL |
| `benchmark/run_bounded_benchmark.py` | `3d4453cd23ad0f56ae0b34f94b21b7b1f3715f180091821b383369aa62fab324` | `3d4453cd…` | EQUAL |
| `benchmark/BENCHMARK_PLAN.json` | `c6f07afd14301e640841e7f4ec95dfcef860df3a02e3ef3768c1513c517104c7` | `c6f07afd…` | EQUAL |

Cross-checks on the parsed buffers: eligibility `status` is `PROFILE_ELIGIBLE_NOT_ACCEPTED`; eligibility `frozen_sha256` and calibration `frozen_sha256` equal the frozen file digest; eligibility `calibration_sha256` equals the calibration file digest; the two recorded selections are equal; `derivation.*_sha256` / `tool_sha256` / `family_order` / `selection_rederived is True` match the files and the frozen nine-id order. `EXPECTED_FROZEN_SHA256` in the tool is the V1.6 digest.

Calibration top-level keys (the only JSON the tool compares besides frozen/base/eligibility): `eligibility_matrix_binary_only`, `frozen_sha256`, `kind`, `selection`.

## (1) Trial-by-trial conformance

Every requested field of all 15 trials was compared against the frozen artifact: `datasets[tf]` for `dataset_id`, `dataset_sha256`, `normalized_path`, `bar_interval_seconds`, `selection_order`; `measurement_inputs[tf].prefixes[size].sha256` for `input_prefix_sha256`; `family_order[].fixed_parameter_record` (deep-equal) for `parameter_record`; recorded selection × frozen family order for the pair sequence; sizes 512/1024/2048.

Frozen `datasets[*]` have **no `symbol` field**. `symbol` is derived by `symbol_from_dataset` (`derive_benchmark_plan.py:51-65`) from `normalized_path` (timeframe parent segment `BTCUSDT`). That is still a function of frozen bytes. `trial_id` is the deterministic format string at `:194`. `strategy_family` is set equal to the frozen `strategy_id`. Frozen `datasets[*].row_count` is not copied (unused). Tool `TIMEFRAMES` equals frozen `timeframe_order`.

| Trial | Frozen source | Result |
|---|---|---|
| `p020-01-GEN_TRIPLE_EMA_STACK-BTCUSDT-15m-n512` | TRIPLE_EMA × 15m × n512 | EQUAL |
| `p020-02-GEN_TRIPLE_EMA_STACK-BTCUSDT-15m-n1024` | TRIPLE_EMA × 15m × n1024 | EQUAL |
| `p020-03-GEN_TRIPLE_EMA_STACK-BTCUSDT-15m-n2048` | TRIPLE_EMA × 15m × n2048 | EQUAL |
| `p020-04-GEN_STOCH_OVERSOLD_CROSS-BTCUSDT-1h-n512` | STOCH × 1h × n512 | EQUAL |
| `p020-05-GEN_STOCH_OVERSOLD_CROSS-BTCUSDT-1h-n1024` | STOCH × 1h × n1024 | EQUAL |
| `p020-06-GEN_STOCH_OVERSOLD_CROSS-BTCUSDT-1h-n2048` | STOCH × 1h × n2048 | EQUAL |
| `p020-07-GEN_KELTNER_BREAKOUT-BTCUSDT-2h-n512` | KELTNER × 2h × n512 | EQUAL |
| `p020-08-GEN_KELTNER_BREAKOUT-BTCUSDT-2h-n1024` | KELTNER × 2h × n1024 | EQUAL |
| `p020-09-GEN_KELTNER_BREAKOUT-BTCUSDT-2h-n2048` | KELTNER × 2h × n2048 | EQUAL |
| `p020-10-GEN_MACD_BULL_CROSS-BTCUSDT-4h-n512` | MACD × 4h × n512 | EQUAL |
| `p020-11-GEN_MACD_BULL_CROSS-BTCUSDT-4h-n1024` | MACD × 4h × n1024 | EQUAL |
| `p020-12-GEN_MACD_BULL_CROSS-BTCUSDT-4h-n2048` | MACD × 4h × n2048 | EQUAL |
| `p020-13-GEN_DONCHIAN_BREAKOUT-BTCUSDT-1D-n512` | DONCHIAN × 1D × n512 | EQUAL |
| `p020-14-GEN_DONCHIAN_BREAKOUT-BTCUSDT-1D-n1024` | DONCHIAN × 1D × n1024 | EQUAL |
| `p020-15-GEN_DONCHIAN_BREAKOUT-BTCUSDT-1D-n2048` | DONCHIAN × 1D × n2048 | EQUAL |

15 trials, frozen family order, no unexpected trial keys. No requested field is unbound to the frozen bytes.

## (2) Base-plan key preservation

Value-for-value deep equality against base `c6f07afd…`. `trials` is the mandated replacement. `derivation` is the only added key. No base key is missing.

| Top-level key | Result |
|---|---|
| `plan_version` | EQUAL |
| `task` | EQUAL |
| `execution_status` | EQUAL (`UNEXECUTED`) |
| `owner_authorization` | EQUAL |
| `research_only` | EQUAL |
| `no_profitability_or_strategy_selection_results` | EQUAL |
| `not_representative_performance_feasibility_profitability_strategy_selection_or_acceptance` | EQUAL |
| `trade_bearing_requirement` | EQUAL |
| `manifest` | EQUAL |
| `compatibility` | EQUAL |
| `implementation_sources` | EQUAL |
| `trial_policy` | EQUAL |
| `trials` | DIFFERENT (required replacement) |
| `p020_profile` | EQUAL (V3/cost/funding pins preserved) |
| `resource_measurement` | EQUAL |
| `repetition` | EQUAL |
| `output_contract` | EQUAL |
| `derivation` | ADDED |

## (3) Matching re-derivation

`lexicographic_first_matching` (`derive_benchmark_plan.py:80-104`) is a faithful transcription of `preselect_profile.py:412-443`. Signature, `assignment`/`used`, nested `search`, family-order try, backtrack, and `return dict(zip(timeframes, assignment))` are the same. Only the docstring and the refusal class/code differ (`PreselectRefused("BENCHMARK_PROFILE_BLOCKED", …)` → `DerivationRefused("DERIVE_REFUSED_SELECTION_MISMATCH: …")`).

`verified_selection` (`:107-138`) requires an exact five-timeframe selection, five distinct frozen families, `matrix.get(sid, {}).get(tf) is True` (literal boolean), independently re-derives the lexicographically first matching, and refuses on mismatch. `verify_inputs` (`:162`) returns only that verified selection.

N6-8 is closed on the fixture: packaged `test_refuses_consistently_rewritten_matrix_and_selection` passes; neutralizing `verified_selection` to `return dict(recorded)` before the lex-first call makes that test fail with `DID NOT RAISE SystemExit` (the pre-fix hole).

Beyond the packaged RED: on the **real** calibration matrix (no matrix rewrite), swapping 15m from `GEN_TRIPLE_EMA_STACK` to `GEN_RSI_OVERSOLD_REVERSAL` in both records is five distinct frozen families, each marked eligible, selections equal — and the original tool still refuses `DERIVE_REFUSED_SELECTION_MISMATCH` because lex-first of the recorded matrix remains TRIPLE on 15m. Non-boolean truthy cells `1` and `"true"` on TRIPLE/15m refuse (`is True`). Omitting 1D, or duplicating a family onto 1D, refuse `REFUSED_SELECTION_NOT_FIVE_DISTINCT`. JSON objects cannot carry a duplicated timeframe key; that case cannot be represented, and a missing/extra key fails the five-key checks.

## (4) Input binding and `tool_sha256`

`load_json_once` (`:31-40`) reads one byte buffer, hashes it, and parses that same buffer. `derive_plan` (`:212-216`) calls it once each for eligibility, calibration, base plan, and the hardcoded `FROZEN_PATH`. `test_each_input_is_read_once` is in the 16-passed suite. Output is exclusive-create (`open(..., "xb")` at `:237-242`).

Re-running the **original** tool file to a scratch path reproduced `d84b043a…` byte-identical to the accepted plan; a second write to the same path exited 2 with `REFUSED: output already exists` and left the bytes unchanged.

`tool_sha256` is **not** taken from that single-read discipline. It is a later `sha256_path(Path(__file__))` (`:231`) — a second independent read of the executing file. A comment-only modified copy hashes to `bdea0a9e…` and emits a plan whose **only** difference from the accepted plan is `derivation.tool_sha256`; the plan digest becomes `3175d5b7…`, not `d84b043a…`. So if the self-hash is the only honest difference, a modified tool **cannot** emit the accepted plan bytes, and a launcher that asserts `d84b043a…` catches it.

The same modified tool with `"tool_sha256": "<original digest>"` hardcoded **does** emit `d84b043a…` byte-identical to the accepted plan. The self-hash is a claim, not a binding of the executing file. That matters for the derivation review chain (which tool ran). It does not change this measurement: the derivation tool is not on the `--run` path; the Lead `RUN_LOG.txt` hashed the original tool **before** the single derivation; the installed plan bytes are what will be measured.

`derivation.frozen_sha256` is copied from `eligibility["frozen_sha256"]` (`:227`), not from the `frozen_sha256` variable returned by `load_json_once`. Both are required to equal `EXPECTED_FROZEN_SHA256`, so the recorded value matches the hashed frozen buffer on this run.

## (5) Driver `_validate_plan` vs frozen params/prefixes

`_validate_plan` (`run_bounded_benchmark.py:95-207`) with a `derivation` block reads `derivation.family_order` only (`:185-194`). It binds datasets and the manifest (and compatibility, V3/cost/funding records + sidecars, implementation sources, 15-trial shape, sizes, five timeframes). It does **not** read `PRESELECTION_FROZEN.json`, eligibility, or calibration, and it does **not** compare `parameter_record` or `input_prefix_sha256` to the frozen artifact. `input_prefix_sha256` is not even in the required-trial key tuple (`:154-158`).

Observed on scratch copies of the accepted plan, real driver imported from its real directory via the Lead harness (benchmark dir not touched):

| Scratch plan | Plan SHA-256 | `_validate_plan` |
|---|---|---|
| accepted derived plan | `d84b043a…` | PLAN_VALID, exit 0 |
| `trials[0].parameter_record.stop_lookback` 10 → 99 | `3b574595…` | PLAN_VALID, exit 0 |
| `trials[0].input_prefix_sha256` → `0*64` | `59a3e799…` | PLAN_VALID, exit 0 |
| STOCH `strategy_id` duplicated as TRIPLE (control) | `dc896643…` | REFUSED `PLAN_INVALID: five families must each have sizes 512, 1024, 2048`, exit 2 |

`--run` **does** consume `parameter_record` as the live measurement input (`:483` `build_signals(..., dict(trial["parameter_record"]))`). A param-swapped plan that passed `_validate_plan` would measure different parameters. `--run` does **not** consume the plan's `input_prefix_sha256`; it recomputes the prefix from the CSV (`:469`) and writes that computed hash into the journal (`:517`). A prefix-field swap in the plan is documentary only on the run path.

### What the launcher whole-file digest assertion (`d84b043a…` before validate, before `--run`, after) does and does not close

**Closes:** any byte change to the installed `BENCHMARK_PLAN.json`, including the param swap and the prefix-field swap above, a family-order rewrite, a derivation-digest rewrite, and an honest comment-only re-derivation (self-hash changes the plan). Combined with `_source_identity.plan_sha256` (`:531-533`) it also records the hash that actually sat at `PLAN_PATH` in the journals/report. An after-hash confirms the file was not mutated during the run.

**Does not close:** the driver still never re-reads the frozen/eligibility/calibration files; it still will not itself reject a param-swapped plan if the launcher only checks `PLAN_VALID` and does not assert `d84b043a…`; it does not prove which derivation-tool file produced the plan (self-hash can be spoofed); it does not read `SHA256SUMS_V16.txt`. For this once-only Lead measurement the assertion is sufficient **if it is an assert, not a log line**. That is a NIT on the driver, not a blocker of these reviewed plan bytes.

## (6) Plan swap

`PLAN_PATH` is the module constant `ROOT / "BENCHMARK_PLAN.json"` (`:20`). There is no `--plan` argument (`main` `:671-688`). `--run` loads that path, validates, then measures.

The driver never reads `SHA256SUMS_V16.txt`. Swapping the plan line there for the interval (and restoring it) is documentary only. Forgetting to refresh it does not change what `--run` measures; refreshing it without copying the derived bytes would leave `--run` on the base plan.

Frozen `source_pins["BENCHMARK_PLAN.json"]` is `c6f07afd…` (`PRESELECTION_FROZEN.json:437-438`). The only code that asserts that pin is `preselect_profile.verify_frozen_identity` (`:549-594`), on the `--oneshot` path, which is spent (`PRESELECT_REFUSED_ALREADY_RUN`) and must not run again. `_validate_plan` / `_run` do not compare the plan file to that pin. After the swap, `_source_identity` will record `plan_sha256 = d84b043a…`, which is the correct measurement identity. No identity check **on the `--run` path** is broken by the swap.

Sound procedure: keep the base as `BENCHMARK_PLAN_BASE_c6f07afd.json`; install the exact derived bytes at `BENCHMARK_PLAN.json` only for the validate+run interval; assert `d84b043a…` on the installed file before `--validate-plan`, immediately before `--run`, and after; record driver `3d4453cd…`, records, sidecars, implementation sources, and every output; restore the base and the checksum line afterwards. Leaving the derived plan permanently at the canonical path would make a later oneshot-path pin check fail and would confuse the frozen source pin.

## (7) Boundary

The tool reads the binary matrix, the selection, the frozen artifact, and the base plan. Calibration JSON contains no economic keys. The tool source has no PnL/ranking/returns comparison (the substring `return` is Python `return`). The derived plan carries no result, ranking, or PnL. Publication-boundary booleans and `output_contract` are value-equal to the base.

The measurement driver's output contract is unchanged by the derived plan: `_run` (`:596-668`) still writes interrupted/resumed vs reference journals, compares semantics with timing excluded, and emits `acceptance_verdict: NOT_EVALUATED` and `profitability_or_strategy_selection_result: NOT_PUBLISHED`.

## Findings

| # | severity REQUIRED / NIT | file:line | what is wrong | why it matters |
|---|---|---|---|---|
| 1 | NIT | `run_bounded_benchmark.py:154-194` (consume `:469`, `:483`, `:517`) | `_validate_plan` accepts a plan whose `family_order` is right but whose `parameter_record` or `input_prefix_sha256` do not match the frozen artifact. Observed: `stop_lookback` 10→99 still PLAN_VALID; prefix field zeroed still PLAN_VALID. `--run` uses `parameter_record` as live input and recomputes the prefix from the CSV. | Without a whole-file assert of `d84b043a…`, PLAN_VALID is not a frozen-parameter gate. The launcher digest assertion before validate / before `--run` / after closes this for the once-only measurement. Do not treat PLAN_VALID alone as that gate. |
| 2 | NIT | `derive_benchmark_plan.py:231` | `tool_sha256` is a late self-hash of `Path(__file__)`, not a digest of a buffer captured at start. A modified tool whose only honest output difference is that field cannot emit `d84b043a…`. The same modified tool with the original hash spoofed emits `d84b043a…` byte-identical. | The accepted plan digest binds a claimed tool hash, not the executing file. The derivation tool is not on the `--run` path; `RUN_LOG.txt` hashed the original tool before the derivation. Record the tool-file digest independently if the chain is ever re-run. |
| 3 | NIT | `DERIVATION_RULE.md:50-51` (also `:44` citing old line `:167`) | The rule file still labels pre-fix tool/test identities `308aa0b8…` / `4adb69a0…` as “V1.6 pins”; live bytes are `0bfd1891…` / `185af7b2…`. | Documentary drift only. Executable identities are the live files hashed above. Repair on the next documentation freeze; do not retouch reviewed executable bytes before this measurement. |

No REQUIRED finding. The 15 trials are frozen-bound; the base keys are preserved; N6-8/N6-6 stay closed; the original tool reproduces `d84b043a…`.

## Commands run with observed output

Cwd for tests: `C:\tmp\GROK_SCRATCH_GKDERIV\P020_PLAN_DERIVE_20260913`. Cwd for probes: `C:\tmp\GROK_SCRATCH_GKDERIV`. Interpreter as pinned. `PYTHONDONTWRITEBYTECODE=1`. `-p no:cacheprovider`.

### Identities

`Get-FileHash -Algorithm SHA256` on the nine live files in the identity table returned the values in that table (EQUAL on every pin). Interpreter: `Python 3.12.12`.

### Tool tests (16)

```text
................                                                         [100%]
16 passed in 0.37s
```

### Original-tool re-derivation (original file, scratch output)

```text
exit 0
digest d84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580
matches accepted True
byte-identical True
second write exit 2
second stderr REFUSED: output already exists: C:\tmp\GROK_SCRATCH_GKDERIV\probes\derived_rerun.json
unchanged True
```

### Comment-only modified tool

```text
modified tool sha256 bdea0a9e5c072a111427b65bb59ee9bc332178622b082a45899dd79fc5ecf6d6
emits accepted plan bytes? False
digest 3175d5b79e7bc7337f21e1ce93b70b055f43644eb6e0cd6e7e7e08ec9ba66a61
identical except tool_sha256? True
```

### Spoofed `tool_sha256` + comment

```text
spoofed tool file sha256 40543630bf1ad0cf3fb8a3feed63b6c225a0a9a6da003850f292ced1775d7565
modified+spoofed tool emits accepted plan bytes? True
byte-identical to accepted? True
digest d84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580
```

### Harness on the real derived plan

```text
run: 2026-09-18T05:09:07+00:00
driver sha256: 3d4453cd23ad0f56ae0b34f94b21b7b1f3715f180091821b383369aa62fab324
plan under validation: C:/tmp/CLAUDE_P0_RUN_20260913/P020_DERIVED_PLAN_20260914/BENCHMARK_PLAN_DERIVED.json d84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580
PLAN_VALID via run_bounded_benchmark._validate_plan: manifest datasets=93, trials=15, distinct families=5, sizes=[512, 1024, 2048], derivation.family_order=9 ids
exit 0
```

### Driver mutations (scratch copies; benchmark directory not written)

```text
tampered param plan sha256 3b574595f3905093b70c1c1a940d1816bead645f957f35971abdf5ad42e73c02
PLAN_VALID ... exit 0

tampered prefix plan sha256 59a3e7998f23befc3d2d762fab274a9b900714c7ed1e58a99445e4951125e0f0
PLAN_VALID ... exit 0

dup family control sha256 dc89664384dd30632540c02786ea211dae1dce654be226202055d5e85033738c
REFUSED: PLAN_INVALID: five families must each have sizes 512, 1024, 2048
exit 2
```

### Three original RED probes (original tool, scratch inputs)

**RED 1 — rewritten matrix+selection PAIR on the real matrix, no matrix rewrite.** Both records' 15m family set to `GEN_RSI_OVERSOLD_REVERSAL` (already `true` on 15m; five distinct frozen families; selections equal). Lex-first of the recorded matrix is still TRIPLE on 15m.

```text
exit 2
stderr DERIVE_REFUSED_SELECTION_MISMATCH: recorded selection is not the lexicographically first matching of the recorded matrix
output exists False
```

**RED 2 — non-boolean truthy matrix cells.** `GEN_TRIPLE_EMA_STACK` / `15m` set to `1`, then to `"true"`, selection unchanged, calibration digest cross-pinned.

```text
value=1 type=int exit=2
stderr DERIVE_REFUSED_SELECTION_MISMATCH: GEN_TRIPLE_EMA_STACK is not marked eligible on 15m
output exists False
value='true' type=str exit=2
stderr DERIVE_REFUSED_SELECTION_MISMATCH: GEN_TRIPLE_EMA_STACK is not marked eligible on 15m
output exists False
```

**RED 3 — omit / duplicate.** (a) drop timeframe `1D` from both selections. (b) set `1D` to `GEN_TRIPLE_EMA_STACK` (duplicate family; JSON cannot duplicate a timeframe key).

```text
3a omit 1D: exit 2
stderr REFUSED_SELECTION_NOT_FIVE_DISTINCT: selection must name five distinct families
output exists False
3b duplicate family on 1D: exit 2
stderr REFUSED_SELECTION_NOT_FIVE_DISTINCT: selection must name five distinct families
output exists False
```

### N6-8 neutralize (scratch tool copy; packaged RED must fail to refuse)

```text
neutralized packaged RED exit 1
Failed: DID NOT RAISE SystemExit
FAILED tests/test_derive_benchmark_plan.py::test_refuses_consistently_rewritten_matrix_and_selection
1 failed in 0.22s
```

## NOT VERIFIED

- `--run` was not executed (forbidden). Prefix hashes in the plan were compared to frozen recorded prefix hashes; the CSV prefix bytes were not independently re-hashed in this lane. The harness `PLAN_VALID` path did hash the selected dataset files, manifest, compatibility, records, sidecars, and implementation sources as the real driver does.
- `--oneshot` was not executed (forbidden; the shot is spent).
- The in-place plan swap (`BENCHMARK_PLAN.json` replacement, `SHA256SUMS_V16.txt` line edit, restore) was not performed; the benchmark directory is read-only here. Swap conclusions are from reading `PLAN_PATH` / `_load_plan` / `_source_identity` / `verify_frozen_identity` and from `SHA256SUMS_V16.txt` not being referenced by the driver.
- Packet copies under `_gemini_packets_20260913` were not re-hashed; live `C:/tmp` paths were.
- Economic records' interval vs the 15m calibration window (Opus N6-3) was not re-opened; it is a carried residual, inert at the pinned HEAD for this measurement.
- No git command of any kind.

GROK_DERIVED_VERDICT: NITS
