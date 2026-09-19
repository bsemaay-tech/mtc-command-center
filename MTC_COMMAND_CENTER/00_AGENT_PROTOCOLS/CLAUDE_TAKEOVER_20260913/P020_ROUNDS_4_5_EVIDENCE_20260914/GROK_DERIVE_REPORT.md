# GROK_DERIVE_REPORT — WP-P0-20 plan-derivation tool pre-screen

Auditor: grok-4.6 (lane GKPD). Supplemental detection only: this report cannot accept anything and does not replace the gpt-5.6-sol / gemini reviewers.

Work copy: `C:/tmp/GROK_SCRATCH_GKPD_20260914/pkg/` (deliverable set copied from `C:/tmp/P020_PLAN_DERIVE_20260913/`; original left untouched). Synthetic fixtures only. No `run_bounded_benchmark.py --run` / `--validate-plan`, no `preselect_profile.py --oneshot`, no T0 token, no git, no network.

**Known stale pin (reported once, then audited as if current):** `derive_benchmark_plan.py:12` hard-codes `EXPECTED_FROZEN_SHA256 = "2e67f3f4ea357b4b974313ddd4a427564860e5618f24d48758f07b599da4b614"` (V1.3). Current frozen file `C:/tmp/P020_PRESELECT_20260913/PRESELECTION_FROZEN.json` hashes to `f839c9602b6d210dcdf87a0c4ac20f3d04ad68e26949d0f40a5c66f1fdbaf0ff` (V1.4 `artifact_version` `p020-preselection-frozen-v1.4`). Per the lane brief this pin will be re-pointed to the roster-accepted digest before use. The rest of this audit treats the pin as the intended authority.

## Conformance

| requirement | MET / NOT MET / PARTLY | file:line evidence |
| --- | --- | --- |
| SHA256SUMS.txt digests of the four hashed deliverables | MET | All four listed files match. `derive_benchmark_plan.py` = `6aaa4f7d3c50281cc585e28c64c59924421db33bbbba6cf3a3c809252d4dfb71`; `tests/test_derive_benchmark_plan.py` = `88fa148c666b2f5c81210f32f3a1c651561bd711bdbdb868440ecde44e8788c9`; `DERIVATION_RULE.md` = `934c5ebfe3c8fbd68c94b3292588dd5adb7781d40c26385222cadc2c6c28ebcd`; `REPORT.md` = `8394279ef22e6d6ea410f73d4d633c88c46d810cfafbffe07d354d70099075bb`. SHA256SUMS is LF, no CR, final LF. |
| Builder pytest count 11 | MET | Pinned interpreter: `...........` / `11 passed in 0.24s` (builder reported `11 passed in 0.25s`). |
| (a) Replace ONLY `trials` (+ add `derivation`); keep every other base-plan field | PARTLY | `derive_plan:162-163` `output = copy.deepcopy(base_plan)` then `output["trials"] = derive_trials(...)`. Probe A: extra top-level `extra_top` and nested `manifest.extra_nested` preserved; no non-trial key dropped or value-mutated; only added key is `derivation`. Not literal original-file bytes: `dump_bytes:45` re-serializes the whole object with `json.dumps(..., indent=2)`. Compact arrays in the real `BENCHMARK_PLAN.json` (e.g. `"sizes_per_strategy_dataset": [512, 1024, 2048]`) expand under that dump (`orig_len 19814` vs round-trip `20722`). Values of extra nested fields survive. |
| (b) 15 trials = frozen family order × sizes 512/1024/2048; driver-required fields filled; would `--validate-plan` accept the shape? | PARTLY | Probe B: 15 trials, families `GEN_A..GEN_E` in frozen `family_order`, sizes `[512,1024,2048]` repeating, `parameter_record` from frozen, dataset fields and prefix hashes from frozen timeframe entries, `trial_id` `p020-{nn}-{family}-{symbol}-{tf}-n{size}`. All driver required keys at `run_bounded_benchmark.py:154-157` are present. Frozen V1.4 datasets have no `symbol`; `symbol_from_dataset:48-62` recovered `BTCUSDT` from `normalized_path` / `dataset_id`. `dataset_selection_order` is copied from frozen (`0,1,9,11,12` on the real artifact) which is a valid index into the 93-row selected manifest. **Driver `--validate-plan` would still reject any selection whose `strategy_id` set is not exactly the five hard-coded names** at `run_bounded_benchmark.py:181-185` (`GEN_TRIPLE_EMA_STACK`, `GEN_MACD_BULL_CROSS`, `GEN_DONCHIAN_BREAKOUT`, `GEN_ATR_PULLBACK_TREND`, `GEN_GOLDEN_CROSS_PULLBACK`). Extra keys (`derivation`, `input_prefix_sha256`, `bar_interval_seconds`) are not rejected. Reasoned from source; `--validate-plan` was not run. |
| (c) Refusals: status, frozen_sha256 (eligibility vs pin vs file), calibration_sha256, selection mismatch, fewer than five distinct families, existing output, malformed JSON | MET | Cited and probed below. All probed refusals exit 2, write nothing (except the pre-existing output case). |
| (d) Same-bytes: parse and hash are two reads; can a swap emit unverified bytes while recording the verified digest? | NOT MET | Yes. `derive_plan:153-159` parses with `load_json` (`read_text`) then hashes with `sha256_path` (`read_bytes`). Probe D frozen swap: trials carried `{"rank": 1, "injected": "UNVERIFIED"}` while `derivation.frozen_sha256` was the verified digest. Base-plan swap: `extra_top.injected = UNVERIFIED_BASE` while `base_plan_sha256` was the verified digest. Coordinated eligibility+calibration swap: trials included `GEN_F` (not in the hashed eligibility selection) while `source_eligibility_sha256` matched the verified eligibility file. |
| (e) Determinism; ASCII; LF; final LF; `sort_keys`? | MET | Probe E: two writes byte-identical; ASCII; LF only; final LF. `dump_bytes:45` is `json.dumps(value, indent=2, ensure_ascii=True) + "\n"` — **no `sort_keys`**. Key order is deepcopy insertion order plus `derivation` appended. Deterministic without `sort_keys` on CPython 3.7+. |
| (f) No economic leakage from eligibility/calibration records | MET | `derive_benchmark_plan.py` never reads returns, PnL, R, drawdown, profit_factor, ranking, or `eligibility_matrix_binary_only` cell values. Consumed fields are identities, `status`, `selection`, and hashes. The only `return` hits are Python `return` statements. |
| (g) `derivation` block hashes present and correct (no-swap case) | MET | Probe G keys: `source_eligibility_sha256`, `calibration_sha256`, `frozen_sha256`, `base_plan_sha256`, `tool_sha256`, `rule_text`. Each matched the file that was on disk after a clean run. `tool_sha256` = `6aaa4f7d3c50281cc585e28c64c59924421db33bbbba6cf3a3c809252d4dfb71` = SHA256SUMS of the running file. `frozen_sha256` is copied from `eligibility["frozen_sha256"]` (`derive_plan:167`), not from the `sha256_path` local; equal in the no-swap case, which is the TOCTOU hole in (d). |
| (h) DERIVATION_RULE.md file:line citations vs current files | PARTLY | Driver and handoff citations checked EQUAL. All checked `preselect_profile.py` citations MOVED (V1.3 → V1.4); quoted text still exists at the new lines. T0 packet still names V1.3 frozen digest `2e67f3f4…` and procedure digest `ac8848c3…`; current files are `f839c960…` and `c2d43525…`. No WRONG quote found in the sample. Table below. |
| (i) TASK.md conformance | PARTLY | CLI flags, exclusive create `open("xb")` at `:177`, LF+final LF, 15 trials, frozen family order, sizes, frozen parameter records, synthetic tests for happy path / most refusals / determinism / non-trial equality: MET. Hard-coded pin is fail-closed strengthening of TASK.md:6 “digest above”, not a substitute for reading `eligibility["frozen_sha256"]` (that field is still read and checked at `:85-86`). Gaps: tests do not cover malformed JSON / non-object JSON / frozen-file digest mismatch (TASK.md:12 “each refusal”); same-bytes identity is two reads; real-plan whitespace is not kept byte-for-byte; current driver family-set is not encoded. |
| TASK: never overwrite existing output | MET | `write_once:177-180` `path.open("xb")` / `REFUSED: output already exists`. Probe C `exists`: exit 2, file left as `occupied`. |
| TASK: refuse `status != PROFILE_ELIGIBLE_NOT_ACCEPTED` | MET | `verify_inputs:93-94`. Probe C `status`: `REFUSED: status is not PROFILE_ELIGIBLE_NOT_ACCEPTED`. |

## Findings

| # | severity REQUIRED / NIT | file:line | what is wrong | why it matters |
| --- | --- | --- | --- | --- |
| 1 | REQUIRED | `C:/tmp/GROK_SCRATCH_GKPD_20260914/pkg/derive_benchmark_plan.py:153-159` and `:165-168` | `load_json` and `sha256_path` are two I/O operations on the same path. Frozen, base plan, eligibility and calibration are parsed first and hashed later. `derivation.frozen_sha256` records `eligibility["frozen_sha256"]` rather than the bytes that were parsed. A swap (or coordinated eligibility+calibration swap) between the two reads emits trials/fields from unverified bytes while the derivation block records the verified digest. | The derivation block is the identity binding for T0. A digest that does not describe the bytes that produced `trials` is a false attestation. Probe D demonstrated this on synthetic files. |
| 2 | REQUIRED | `C:/tmp/P020_LEAD_20260912/benchmark/run_bounded_benchmark.py:181-185` vs `derive_trials:107-108` | The derive tool emits whatever five frozen families the eligibility `selection` names, in frozen `family_order`. The current driver’s `_validate_plan` requires `set(by_family)` to equal a hard-coded original five (`GEN_TRIPLE_EMA_STACK`, `GEN_MACD_BULL_CROSS`, `GEN_DONCHIAN_BREAKOUT`, `GEN_ATR_PULLBACK_TREND`, `GEN_GOLDEN_CROSS_PULLBACK`). A mechanically correct derived plan for any other matching is `PLAN_INVALID`. The tool does not fail closed on that consumer constraint. | The stated purpose is a drop-in replacement of the existing plan’s trial list for the existing driver. Until the driver check is generalized (or the tool refuses a non-driver set), a real oneshot selection other than those five families cannot be consumed. |
| 3 | NIT | `derive_benchmark_plan.py:44-45` | Whole-document re-dump, not a surgical byte splice of `trials`. Real `BENCHMARK_PLAN.json` compact arrays are expanded by `indent=2`. | Non-trial *values* are preserved (Probe A). Anyone comparing the derived file bytes to the base plan bytes outside `trials`/`derivation` will see whitespace drift. The driver `json.loads` the plan, so this does not by itself fail validation. TASK.md:11 said “byte-for-byte”. |
| 4 | NIT | `tests/test_derive_benchmark_plan.py:138-183` | TASK.md:12 asks for “each refusal”. Tests cover status, eligibility `frozen_sha256`, `calibration_sha256`, selection mismatch, non-distinct / non-frozen families, and existing output. They do not cover malformed JSON (`load_json:37-38`), non-object JSON (`:39-40`), or frozen-*file* digest vs pin (`verify_inputs:87-88`). | Those refusals exist in the tool (Probe C) but are not locked by the test file T0 is asked to trust. |
| 5 | NIT | `derive_benchmark_plan.py:65-69` | `strategy_family` is taken from leftover *base-plan* trials when `strategy_id` matches, else falls back to `strategy_id`. Probe B: `GEN_A` → `"family A label"`; `GEN_B` → `"GEN_B"`. Frozen V1.4 has no family-label field; preselect `_trial:831` always writes `strategy_id`. | Mixed labels across a derived plan. Driver requires the key (`:155`) but does not check the string. Not economic leakage; still an identity inconsistency. |
| 6 | NIT | `DERIVATION_RULE.md:11-20` and T0 packet `:45-50` | Preselect citations are V1.3 line numbers (MOVED under V1.4). Packet still lists frozen sha256 `2e67f3f4…` and `preselect_profile.py` sha256 `ac8848c3…`. Current files: frozen `f839c960…`, procedure `c2d43525…`. Driver and `BENCHMARK_PLAN.json` packet digests still MATCH. | Reviewers following the packet will pin the wrong frozen/procedure bytes unless this is updated with the re-pin. Quoted text of the MOVED lines is still correct at the new locations. |

## Citation spot-check (DERIVATION_RULE.md vs current files)

At least eight citations. EQUAL = quoted text lives at that line today. MOVED = quoted text exists at a new line (V1.4 `preselect_profile.py`). WRONG = quoted text is not in the current file.

| claimed citation | quoted text (from DERIVATION_RULE.md) | current location | result |
| --- | --- | --- | --- |
| `preselect_profile.py:657` | `"family_order": families,` | `:670` (current `:657` is `"impl_head": head,`) | MOVED |
| `preselect_profile.py:659` | `"timeframe_order": list(TIMEFRAMES),` | `:672` | MOVED |
| `preselect_profile.py:660` | `"datasets": datasets,` | `:673` | MOVED |
| `preselect_profile.py:661` | `"measurement_inputs": measurement,` | `:674` | MOVED |
| `preselect_profile.py:702` | `"selection_rule": "lexicographically first complete matching of five distinct families to the five timeframes over the frozen ordering",` | `:715` | MOVED |
| `preselect_profile.py:1084-1088` | `calibration = {` / `"kind": "calibration",` / `"frozen_sha256": frozen_sha256,` / `"eligibility_matrix_binary_only": matrix,` / `"selection": selection,` | `:1104-1108` | MOVED |
| `preselect_profile.py:1112` | `status = "BENCHMARK_PROFILE_BLOCKED" if blocked else "PROFILE_ELIGIBLE_NOT_ACCEPTED"` | `:1132` | MOVED |
| `preselect_profile.py:1113-1122` | `eligibility = {` … `"blocked": blocked,` | `:1133-1142` (V1.4 inserts `"one_shot": True` and `"second_selection": "FORBIDDEN"` between `status` and `selection`) | MOVED |
| `preselect_profile.py:1099` | `for timeframe in TIMEFRAMES:` | oneshot measurement loop is `:1119` (current `:1099` is `if ok:`) | MOVED |
| `run_bounded_benchmark.py:85` | `def _load_plan() -> dict:` | `:85` | EQUAL |
| `run_bounded_benchmark.py:154-157` | required trial key tuple including `trial_id` … `input_rows` | `:154-157` | EQUAL |
| `run_bounded_benchmark.py:452` | `data_path = MANIFEST_PATH.parent / trial["normalized_path"]` | `:452` | EQUAL |
| `run_bounded_benchmark.py:587` | `trials = [dict(trial, parameters=trial) for trial in plan["trials"]]` | `:587` | EQUAL |
| `P020_HANDOFF.md:60` | Preserve three measured sizes … 512, 1024, 2048 … 15 trials | `:60` | EQUAL |
| `P020_HANDOFF.md:65` | Preserve five distinct families … lexicographically first … never choose the best economic result | `:65` | EQUAL |
| `P020_HANDOFF.md:70` | extend the existing external driver/plan/runbook; do not build a general optimizer | `:70` | EQUAL |

V1.4 `_run_oneshot` schema the tool must consume (not cited in DERIVATION_RULE.md at current lines): calibration dict `:1104-1108`; eligibility dict `:1133-1142` with extra `one_shot` / `second_selection`. The tool ignores those extra keys and does not require `kind`. That is compatible with the written records.

## RED probes (synthetic only)

Working directory: `C:/tmp/GROK_SCRATCH_GKPD_20260914/pkg/probes/`. Interpreter: pinned venv Python. `FROZEN_PATH` / `EXPECTED_FROZEN_SHA256` monkeypatched to synthetic files; real frozen / real eligibility / real driver were not used as derive inputs.

### Probe A — extra nested fields

Observed: exit 0; `dropped_non_trial_keys []`; `mutated_non_trial_keys []`; `extra_top preserved True`; `manifest.extra_nested preserved True`; `only_new_keys ['derivation']`. Compact original started `{"plan_version":"synthetic",...}`; derived started `{\n  "plan_version": "synthetic",...}`; `compact_reformatted True`; `non_trial_json_dumps_mismatches []`.

### Probe B — trial construction

Observed first trial:

```json
{
  "trial_id": "p020-01-GEN_A-BTCUSDT-15m-n512",
  "strategy_id": "GEN_A",
  "strategy_family": "family A label",
  "symbol": "BTCUSDT",
  "timeframe": "15m",
  "dataset_selection_order": 0,
  "parameter_record": {"rank": 1, "nested": {"k": "GEN_A"}},
  "input_rows": 512
}
```

`count 15`; family order `GEN_A..GEN_E`; sizes repeating 512/1024/2048; `missing_required_keys_in []`; `prefix_hashes_match True`. V1.4-shaped datasets with no `symbol` field: `nosymbol_symbols {'BTCUSDT'}`. Unseen families: `strategy_family` falls back to `strategy_id`.

Driver shape (reasoned, not executed): required keys at `:154-157` are filled; `input_rows` in `{512,1024,2048}`; `dataset_selection_order` is an int copied from frozen. Family-set check at `:181-185` is independent of that shape and will fail for any other five ids.

### Probe C — refusals (nine cases; brief asked for at least three)

| case | exit | wrote output | stderr (observed) |
| --- | --- | --- | --- |
| status | 2 | no | `REFUSED: status is not PROFILE_ELIGIBLE_NOT_ACCEPTED` |
| eligibility frozen_sha256 | 2 | no | `REFUSED: eligibility frozen_sha256 mismatch` |
| frozen *file* vs pin | 2 | no | `REFUSED: frozen artifact SHA-256 mismatch` |
| calibration_sha256 | 2 | no | `REFUSED: eligibility calibration_sha256 mismatch` |
| calibration selection mismatch | 2 | no | `REFUSED: calibration selection mismatch` |
| four distinct families | 2 | no | `REFUSED: selection must name five distinct families` |
| existing output | 2 | pre-existing kept | `REFUSED: output already exists: ...\c_exists\refused.json` |
| malformed JSON | 2 | no | `REFUSED: cannot read JSON ... Expecting property name enclosed in double quotes: line 1 column 2 (char 1)` |
| JSON array root | 2 | no | `REFUSED: JSON object required: ...\PRESELECTION_ELIGIBILITY.json` |

Code citations: status `:93-94`; eligibility frozen vs pin `:85-86`; frozen file vs pin `:87-88`; calibration hash `:89-90`; calibration `frozen_sha256` vs eligibility `:91-92` (not separately probed; same `verify_inputs`); selection mismatch `:98-99`; five distinct `:100-101`; existing output `:177-180`; malformed / non-object `:34-40`.

### Probe D — parse/hash swap (TOCTOU)

Frozen file: `load_json` saw malicious `fixed_parameter_record` `{"rank": 1, "injected": "UNVERIFIED"}`; `sha256_path` hashed the original bytes.

Observed:

- `emitted_unverified_bytes True`
- `trial0_parameter_record {'rank': 1, 'injected': 'UNVERIFIED'}`
- `recorded_frozen_sha256 281f41120c90125c31f1912adbdffc1e62c52b7d767afec7fda54517eabf1820` (= verified digest, not the malicious file)
- `text_reads 1 bytes_reads 1`

Base plan: `emitted_unverified_base_field True`; `preserved_extra_top {'injected': 'UNVERIFIED_BASE'}`; `recorded_equals_real_base True`.

Eligibility+calibration coordinated swap: hashed eligibility selection was `GEN_A..GEN_E`; parsed selection replaced 15m with `GEN_F`. Observed trials include `p020-13-GEN_F-BTCUSDT-15m-n512` while `recorded_equals_real_elig True`. First trial is `GEN_B` because `derive_trials:107` walks *frozen family order*, not timeframe order.

### Probe E — determinism / encoding

`byte_identical True`; `endswith_lf True`; `has_cr False`; `ascii_ok True`; `dump_bytes_uses_sort_keys False`; both writes sha256 `d67859f8c5f6bef18d107167b0980c00d7d12802d0b14665b8e2618896e715b3` (synthetic fixture, not a deliverable digest).

### Probe G — derivation block (clean run)

All six fields present. `tool_sha256` matched the running `derive_benchmark_plan.py` digest `6aaa4f7d…`. Input file digests matched `source_eligibility_sha256`, `calibration_sha256`, `base_plan_sha256`, and `frozen_sha256`.

## Commands run (observed output)

SHA256SUMS verification (pinned Python, work copy):

```text
MATCH derive_benchmark_plan.py
  expected 6aaa4f7d3c50281cc585e28c64c59924421db33bbbba6cf3a3c809252d4dfb71
  got      6aaa4f7d3c50281cc585e28c64c59924421db33bbbba6cf3a3c809252d4dfb71
MATCH tests/test_derive_benchmark_plan.py
  expected 88fa148c666b2f5c81210f32f3a1c651561bd711bdbdb868440ecde44e8788c9
  got      88fa148c666b2f5c81210f32f3a1c651561bd711bdbdb868440ecde44e8788c9
MATCH DERIVATION_RULE.md
  expected 934c5ebfe3c8fbd68c94b3292588dd5adb7781d40c26385222cadc2c6c28ebcd
  got      934c5ebfe3c8fbd68c94b3292588dd5adb7781d40c26385222cadc2c6c28ebcd
MATCH REPORT.md
  expected 8394279ef22e6d6ea410f73d4d633c88c46d810cfafbffe07d354d70099075bb
  got      8394279ef22e6d6ea410f73d4d633c88c46d810cfafbffe07d354d70099075bb
```

Pytest (cwd `C:/tmp/GROK_SCRATCH_GKPD_20260914/pkg`):

```text
C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider

...........                                                              [100%]
11 passed in 0.24s
```

Packet digest check (current files vs DERIVATION_RULE.md T0 packet):

```text
preselect_profile.py          got c2d435251e58fe372bf422e7f68b81cd9d95e9a1c2c7c720e0c6fbffb664a3af  claim ac8848c3…  MISMATCH
run_bounded_benchmark.py      got 4b293de6c26ae61ffec22c8205b81a1bad0c6561c0c642e19a37596b5fd62736  claim 4b293de6…  MATCH
BENCHMARK_PLAN.json           got 1d98291fea2783fb4e5dbff37386f21563c9a7c8757ee127eea404a1f6c1201d  claim 1d98291f…  MATCH
PRESELECTION_FROZEN.json      got f839c9602b6d210dcdf87a0c4ac20f3d04ad68e26949d0f40a5c66f1fdbaf0ff  claim 2e67f3f4…  MISMATCH
```

Probes: `python.exe probes\run_probes.py` → `ALL PROBES COMPLETE` (full observed text in sections above).

Real-plan `json.dumps(..., indent=2)` round-trip (parse only; derive not invoked on the real plan): `full_roundtrip_byte_identical False`; first mismatch is compact `[512, 1024, 2048]` vs pretty-printed array.

## NOT VERIFIED

- `--validate-plan` / `--run` were not executed on any derived plan, including synthetic ones that copy real manifest paths. Driver acceptance of trial *shape* is reasoned from `run_bounded_benchmark.py:95-193` only.
- No real `PRESELECTION_ELIGIBILITY.json` / `PRESELECTION_CALIBRATION.json` exists in this lane. Happy-path behaviour against a oneshot result is unproven. Citation: `C:/tmp/P020_PRESELECT_20260913/REPORT_R4.md` (builder REPORT.md already quotes `:433` that no eligibility result exists).
- Whether a future lexicographic matching of the V1.4 9×5 matrix will land on the driver’s hard-coded five families is unknown until oneshot runs.
- The parse/hash swap was simulated by hooking `Path.read_text` / `Path.read_bytes` in-process, not by a second OS process racing the files.
- V1.3 frozen bytes were not present to independently confirm the brief’s claim that V1.4 changed only `artifact_version` / `procedure_sha256`. Current V1.4 file was read; `family_order`, `timeframe_order`, `datasets`, `measurement_inputs`, `selection_rule` are present.
- `verify_inputs:91-92` calibration `frozen_sha256` mismatch was not a dedicated RED probe (code path exists; tests do not cover it).
- Windows `open("xb")` exclusive-create semantics vs a second process were not probed beyond the existing-file case.

## TASK.md pin vs eligibility digest (Detect i)

TASK.md:11 says the tool “reads the frozen artifact digest from the eligibility file; verifies `frozen_sha256`”. TASK.md:6 also names the V1.3 digest as the frozen artifact identity.

The tool does both: it reads `eligibility["frozen_sha256"]` and requires it equal `EXPECTED_FROZEN_SHA256` (`:85-86`), and requires the frozen *file* hash equal the same pin (`:87-88`). Eligibility cannot retarget a different frozen artifact. That is fail-closed strengthening of the TASK.md:6 pin, not a silent replacement of the eligibility read. It becomes a live deviation only while the pin lags V1.4 — already noted as known, to be re-pinned before use.

GROK_DERIVE_VERDICT: REQUIRED_FOUND
