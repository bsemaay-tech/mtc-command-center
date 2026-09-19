# T0 review report — WP-P0-21 S1 catalogue-only slice, candidate `7fecf204c5d457ff19872c97e5d27e2d5a712508`

Reviewer: exact `claude-opus-5`, effort xhigh — the first exact-flagship T0 read of this LEAD-AUTHORED candidate (Claude Opus 5 Lead, session 5 `03c6c8`, disclosed). No delegation, no subagents, no other session resumed.
Brief: `C:/tmp/OPUS_QUEUE_20260916/P021S1/REVIEW_BRIEF.md`; launch instruction `C:/tmp/OPUS_QUEUE_20260916/P021S1/opus/BRIEF.md`.
Scratch (all my working copies): `C:/tmp/OPUS_P021S1_SCRATCH/`. Nothing written into any repository; no `git status`, no working-tree diff, no `add`/`commit`/`checkout`/`push`.

---

## 1. Verified identities

| Item | Value |
|---|---|
| COMPUTED HEAD (`git -c safe.directory=* -C C:/tmp/P021_S1_20260915 rev-parse HEAD`) | `7fecf204c5d457ff19872c97e5d27e2d5a712508` — **matches the required candidate** |
| Base for every byte comparison | `fcac0ac6` (`git diff fcac0ac6 7fecf204 -- <the three paths>`) |
| Catalogue file, git blob | `p021_readiness_rules.py` blob `beea5ad3c52a848b15b4d4776f8d83e430bc9a23`, 19 587 bytes, **content sha256 `d433ef6d90062c3aa4c88eaaef8133eeecab137f0ec1e2f28ba86bbe488a42f3`** |
| Catalogue file, working-tree checkout (CRLF) | 20 053 bytes, sha256 `653bb7c4ef6d7ab1e3b3ee25131aa26719ce546fa097ceb13795c3992880e525` |
| `tests/test_p021_eligibility.py` | blob `cb305b50f5a0b0408db5a06190d2cff83c1af22f`, 69 871 bytes, content sha256 `02559920b2c5aa4199e81dbe3f936450ed85019a6415272b2825de4690eaeabc` |
| `tests/test_strategy_type_policy_set.py` | blob `7cdb720efc137ea8d4a71d5bb427dbf17a8e4b32`, 5 479 bytes, content sha256 `febb8c4d6c65160fcfc97b31be1397ff41bb395078e6b731428a63fbddb09eb9` |

Both hash forms are given deliberately: the checkout is CRLF and its hash is not the repository's bytes. The blob content sha256 is the one to re-pin.

Authorities read as bytes (never through a report's description):
- `C:/CT13/DECISIONS.md:132` — row `OD-20260915-P021-S2-RECOMMENDED-1`, owner's exact word `E recomended`, ~18:25Z 2026-09-15.
- `C:/CT13/.../QUEUED_PACKAGES_20260915/P021_OPTIONS_PACKET_S2_20260915.md` — §1 (option T), §2 (B-17), §3 (B-13), §4 (options M-A/M-B/M-C), §5 (engineering).
- `C:/CT13/.../QUEUED_PACKAGES_20260915/P021_S1_20260915/` — `LEAD_VERIFICATION_P021_S1.md`, `LEAD_*`, `GEMINI/REPORT_RESPONSE_UTF8.md`.
- `C:/CT13/.../P021_GAP_TABLE_20260915.md:33,34,58,73` — B-04 risk-unit source OPEN and deferred to S3; B-05 "CLOSED as a definition".

---

## 2. Fidelity table — the four values/pins vs the DECISIONS row and the S2 packet text

| # | Pin | Authority (bytes) | Code (file:line) | Comparison |
|---|---|---|---|---|
| 1 | **B-02 value + metric** | Row item (1): `P021_DECISION_3 = T`, `gap_ratio_max = 0.0001` on `gap_ratio_metric = "m2_missing_bar_ratio"`, "B-02 CLOSED as a value; coverage stays a separate rule". Packet §1 option **T** = `0.0001` (≈ 24 missing bars in a 245 873-bar 5m series), "one-bar tolerance", "no option is data-calibrated … the choice is an appetite for unseen gapping", "coverage is a separate rule … never through `gap_ratio_max`" | `p021_readiness_rules.py:58` (`"P021_DECISION_3": "T"`), `:174-175` (`ClosedNumber("gap_ratio_max", 0.0001, …)`), `:241` (DATA_QUALITY limit), `:242` (metric), `:178-182` (provenance prose reproducing the packet's own numbers 4 105 966 / 4 477 626 / 245 873 and its "appetite for unseen gapping" wording), `:48` removed from `OPEN_NUMBERS` | **EQUAL** |
| 2 | **B-17 formula pin** | Row item (2) and packet §2 both give the string verbatim | `:199-202` `GAP_RATIO_FORMULA_ID`; `:243` DATA_QUALITY limit | **EQUAL — byte-identical.** Machine comparison: code / DECISIONS row / packet / test literal all `len=110`, `sha256[:16]=70be44c03097144c`. Four-way equality proven, not eyeballed |
| 3 | **B-13 digest pin** | Row item (3): `dataset_hash_required` satisfied by the `ds-v1` digest of the bundle the check scanned, "contract named"; "P0-20/P0-30 hashes stay separate fields". Packet §3 adds the consequence: "the DATA_QUALITY **measured-value object** carries `dataset_manifest_hash = <ds-v1 digest>` and names the contract" | `:244` (`("dataset_hash_contract", "ds-v1")`), `:240` (`dataset_hash_required` True, pre-existing), `:246` (`dataset_hash_contract.B13` removed from `missing_rules`); no equation with any P0-20/P0-30 hash anywhere | **EQUAL for what this slice covers** — the contract is named and the blocker correctly dropped. The `dataset_manifest_hash` half belongs to a measured-value object that does not exist in this bounded step; see **NIT-3** (that field name is recorded nowhere in the repository) |
| 4 | **B-05 divergence metric + definition** | Row item (4): `P021_DIVERGENCE_METRIC = M-C`, "both failure modes recorded in the shadow window; B-05 definition CLOSED; B-06/B-07 stay measure-first". Packet §4 defines the option: **M-C = "both — M-B as the gate on signal fidelity, M-A as the economic divergence, each with its own tolerance"**, Cons "two tolerances to ratify later (**B-06 becomes two numbers**)"; **M-A** = "per-pair **signed** difference of **realized trade return** (forward − backtest), aggregated as the mean over the aligned window, **reported with the count and the standard deviation**", unit "**return fraction per trade**"; **M-B** = "intent-level agreement rate: share of backtest intents that the forward path produced **at the same bar** (**entry/exit decisions match**), **independent of P&L**" | selector `:59` and `:274` are correct; the **definition** `:206-212`; open numbers `:191-193`; `divergence_metric.B05` removed `:276` | **Selector `M-C`: EQUAL (`:59`, `:274`). Definition text: DIFFERENT (REQUIRED-1). Tolerance count: DIFFERENT (REQUIRED-2).** |

Also checked against the row's §5 engineering sentence ("`OPEN_NUMBERS` → `CLOSED_NUMBERS` with policy-v1 provenance; `missing_rules` for B-13/B-17 removed = one small T1 change with RED/GREEN, part of S1"): both `gap_ratio_formula.B17` and `dataset_hash_contract.B13` are gone from DATA_QUALITY's `missing_rules` and nothing else was removed from it (`:246`, base had the three-tuple); the status is PROVISIONAL (`:53`) and the reversibility clause is untouched (`:75-78`). `POLICY_SET.owner_decisions` is extended with both S2 keys and a dated S2 source (`:58-59`, `:62-70`).

---

## 3. Fence proof (commands, cwd, output — all run by me)

**Interpreter.** The brief pins 3.12.12. `python` on PATH here is 3.14.2 and the uv-managed 3.12.12 (`%APPDATA%\uv\python\cpython-3.12.12-windows-x86_64-none\python.exe`) has no pytest. I used `C:\tmp\P012_FUNDING_PY312_20260911\Scripts\python.exe` → **Python 3.12.12, pytest 9.1.1** (subtest reporting is native in pytest 9; `pytest_subtests` is not importable in that venv, and the counts still matched the brief exactly).

### 3.1 Self-check — cwd `C:\tmp\P021_S1_20260915`
```
$env:PYTHONPATH = "MTC_COMMAND_CENTER/contracts;MTC_COMMAND_CENTER/03_QUANTLENS/tools"
<py312> MTC_COMMAND_CENTER/03_QUANTLENS/tools/p021_readiness_rules.py --self-check
```
```
SELF-CHECK PASS: 7 checks all refuse readiness
CLOSED NUMBERS: 13 (profile balanced, provisional)
OPEN NUMBERS: 3
MODIFIED COPY DETECTED: divergence_tolerance refusal wiring removed
S2 CLOSED (catalogue only): gap_ratio_max=0.0001 on m2; B-17 formula pin; B-13 ds-v1 pin; B-05 metric M-C
MODIFIED COPY DETECTED: swing_forward_period closure removed
READY=False
EXIT=0
```

### 3.2 The three test modules — cwd `C:\tmp\P021_S1_20260915`
```
$env:PYTHONPATH = "MTC_COMMAND_CENTER/contracts;MTC_COMMAND_CENTER/03_QUANTLENS/tools"
<py312> -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p021_eligibility.py \
                 MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_strategy_type_policy_set.py \
                 MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_data_gap_ratio.py \
                 -q -p no:cacheprovider --basetemp C:/tmp/OPUS_P021S1_SCRATCH/bt
```
```
59 passed, 108 subtests passed in 0.29s
EXIT=0
```
**Exactly the 59 + 108 the brief predicted.** (The `--basetemp` under `C:/tmp` did not reproduce the known Bridge-staging phantom-failure mode; that defect is specific to `test_mtc_funding_export` and no such test is in this set.)

### 3.3 My own mutants — the ready-fence

Built in `C:/tmp/OPUS_P021S1_SCRATCH/mutants_fence.py`; the candidate catalogue is imported read-only and `RULES` is mutated in memory with `dataclasses.replace`.

| My mutant | Result |
|---|---|
| DATA_QUALITY `missing_rules=()` (its only remaining anchor after S2; it has no open numbers) | `ValueError: P021.DATA_QUALITY could be presented as ready` — **refused by `validate_catalog`** (`:336-338`) |
| REPAINT_CLOSED_BAR `missing_rules=()` | `ValueError: P021.REPAINT_CLOSED_BAR could be presented as ready` — refused |
| **all seven** rules `missing_numbers=()` and `missing_rules=()` | `ValueError: open-number refusal wiring changed; missing=['divergence_min_paired_observations','divergence_tolerance','divergence_window_length']` — refused at the earlier wiring gate (`:325-329`) |
| same all-clear catalogue installed as `p021_readiness_rules.RULES`, then `readiness_record()` | **`readiness_record()` refused to build** with that same `ValueError`; no record was produced |
| BACKTEST_FORWARD_DIVERGENCE `missing_rules=()` with its three open numbers kept | **accepted by `validate_catalog`** — the guard fires only when *both* tuples are empty; the rule's status still comes out `REFUSED` and `_refusal` still names the three open numbers. See **NIT-4** for the exact shape |
| DATA_QUALITY anchor renamed to a placeholder (`validate_catalog` satisfied) | record still `ready=False`, DATA_QUALITY still `REFUSED` |
| source audit for a True path | the only occurrences are `"ready": False,` (`:361`) and `assert record["ready"] is False` (`:385`); **no line assigns True to `ready`** |

So: **a rule that has lost every refusal anchor is refused by `validate_catalog`, and `readiness_record()["ready"]` cannot become True** — it is a literal `False` and the builder calls `validate_catalog` first (`:342`).

### 3.4 RED arms 1 and 2 — reproduced, **with a control arm**

Minimal trees assembled in scratch from git blobs (`git -c safe.directory=* show fcac0ac6:<path>`) plus the four supporting modules and a copy of `MTC_COMMAND_CENTER/contracts`; the 435 MB tools tree was not copied.

| Arm | Contents | Result |
|---|---|---|
| **CTRL** (mine, added so a RED means something) | new catalogue + new tests, same scratch layout | **52 passed, 96 subtests passed**, exit 0 → the layout is valid (52+7 = 59, 96+12 = 108 against §3.2, the difference being `test_data_gap_ratio.py`, which the arms do not include) |
| **RED 1** | `fcac0ac6` catalogue + **new** tests | **47 failed, 5 passed**, exit 1 |
| **RED 2** | **new** catalogue + `fcac0ac6` tests | **47 failed, 5 passed**, exit 1 |

Both counts match `LEAD_VERIFICATION_P021_S1.md` rows RED 1/RED 2 exactly. I then confirmed the *reason* rather than the count (line numbers below are in the copy each arm actually ran — RED 1 runs the **candidate** test files, RED 2 the **`fcac0ac6`** ones, whose numbering differs by two lines):

- RED 1 (candidate test file): `test_strategy_type_policy_set.py:118` → `AssertionError: Items in the first set but not the second: 'gap_ratio_max'`.
- RED 2 (base test files): `test_strategy_type_policy_set.py:116` → `AssertionError: Items in the second set but not the first: 'gap_ratio_max'`, and `test_p021_eligibility.py:98` `setUp` → `:91` `self.assertEqual(len(record["open_numbers"]), 4)` → `AssertionError: 3 != 4`.

The 47-wide blast radius is by design, not accident: `P021ContractTestCase.setUp`/`tearDown` call `assert_readiness_fence()` (`test_p021_eligibility.py:117-121`), so any catalogue/test mismatch reddens every test in the module.

### 3.5 Mutation sweep — does the suite actually pin the S2 bytes?

Thirteen single-edit mutations of the catalogue, each write verified by read-back before the run, file restored byte-identically afterwards (`restore byte-identical: True`, CTRL green again). **First attempt was void** — `Set-Content -Encoding` was rejected in this shell, so no mutation was ever written and all thirteen "52 passed" results were meaningless; re-run through `[System.IO.File]::WriteAllText` with a read-back guard.

| Mutation | `--self-check` | pytest | Verdict |
|---|---|---|---|
| `gap_ratio_max` 0.0001 → 0.001 | exit 0 | 46 failed | CAUGHT |
| formula pin "half-open" → "closed" | exit 0 | 46 failed | CAUGHT |
| `dataset_hash_contract` ds-v1 → ds-v2 | exit 0 | 46 failed | CAUGHT |
| `gap_ratio_metric` m2 → m1 | exit 0 | 46 failed | CAUGHT |
| `P021_DECISION_3` T → F | exit 0 | 46 failed | CAUGHT |
| `P021_DIVERGENCE_METRIC` M-C → M-A | exit 0 | 46 failed | CAUGHT |
| `divergence_metric` limit M-C → M-A | exit 0 | 46 failed | CAUGHT |
| DATA_QUALITY anchor `accepted_corrected_engine.B01` renamed | exit 0 | 46 failed | CAUGHT |
| `gap_ratio_max` limit removed from DATA_QUALITY | exit 0 | 46 failed | CAUGHT |
| `gap_ratio_formula_id` limit removed | exit 0 | 46 failed | CAUGHT |
| `s2_source_document` → "some other undated source …" | exit 0 | **52 passed** | **SURVIVED** → NIT-2 |
| `s2_decided_at` 2026-09-15 → 2020-01-01 | exit 0 | **52 passed** | **SURVIVED** → NIT-2 |
| `gap_ratio_max` provenance prose → "invented with no owner source …" | exit 0 | **52 passed** | **SURVIVED** → NIT-2 |

Two conclusions. (a) Gemini's NIT-1 and NIT-2 are genuinely closed: the formula id is pinned by string equality (`test_p021_eligibility.py:96-100`) and the value by numeric equality in two places (`:94`, `:111`). (b) `--self-check` exits 0 under **every** one of these mutations — it is not a value fence; see NIT-1.

---

## 4. Artifact statement (catalogue `0.0001` vs artifact `None`)

**No consumer on master reads both, and nothing can act on the difference today.**

- `p021_readiness_rules` is imported by exactly two files in the whole worktree — `tests/test_p021_eligibility.py:15` and `tests/test_strategy_type_policy_set.py:13`. There is no production importer, and `check_set_identity` is still `None` (`:363`).
- `strategy_type_policy_set` is imported by `data_gap_ratio.py:9` and `strategy_type_classifier.py:9`, both for `validate_policy_set` only.
- `validate_policy_set` treats `shared.gap_ratio_max` solely as "finite number **or null**" (`strategy_type_policy_set.py:153-155`, `:80-86`) and never compares it with anything; `_SHARED_KEYS:48` only requires the key to be present.
- `data_gap_ratio.py` reads only `policy["methods"]["gap_method_version"]` (`:51`); its docstring states it measures "without sorting, filling, or **applying a policy limit**" (`:48`).
- No policy-set artifact file exists in the worktree. `p021pol-v1:` has exactly **two** occurrences across all file types in the repository: the fixture's `version` string and `_VERSION_PREFIX` in the validator; and no `*.json` under `MTC_COMMAND_CENTER` contains the schema id `p021.strategy_type_policy_set/v1`. The "accepted artifact" therefore exists only as the fixture at `tests/test_strategy_type_policy_set.py:21-57`, with `"gap_ratio_max": None` (`:44`) and version `p021pol-v1:4a807136…` (`:56`), whose hash is reproduced by an equality test (`:61-63`).
- The slice leaves both of those fixture lines untouched — its only edits to that file are the two-line comment at `:94-95` and the removal of `"gap_ratio_max"` from the open-number set inside `test_current_readiness_catalogue_stays_refused` (candidate `:118-122`).

So the contradiction is **latent and harmless now**; it becomes live the moment a first consumer reads either surface, which is exactly the whole-set ratification the owner holds as **B-22**. Not my call, and I make none. The slice is honest about it in two places: `POLICY_SET.s2_scope` (`:67-70`) and the test comment (`tests/test_strategy_type_policy_set.py:94-95`).

---

## 5. Formula-pin honesty statement (B-17)

Pin text: `m2_missing_bar_ratio@data_gap_ratio.py v1 (fixed-step 24/7, half-open span, leading/trailing absence excluded)`. Against `MTC_COMMAND_CENTER/03_QUANTLENS/tools/data_gap_ratio.py` (untouched by this slice):

| Pin clause | Code | Honest? |
|---|---|---|
| `m2_missing_bar_ratio` | emitted under exactly that key, `:100` | yes |
| numerator = "missing bars inside counted gaps" (catalogue unit string `:176-177`) | `detected = [delta for delta in deltas if delta > 1.5 * step]` `:69`; `missing_by_gap = [max(0, round(delta/step) - 1) …]` `:70`; `missing_bars = sum(missing_by_gap)` `:71`; `m2 = missing_bars / expected_bars` `:85` | yes — and the word "**counted** gaps" is the honest one: only intervals above the 1.5·step threshold contribute |
| denominator = "expected bars over the observed span" | `span = values[-1] - values[0]` `:62`; `expected_bars = round(span/step) + 1` `:65` | yes |
| "fixed-step" | `step = TIMEFRAME_SECONDS[timeframe]` `:54`, table `:12-19`; single owner of the step | yes |
| "24/7" | no session calendar, weekend mask or holiday logic anywhere in the module; `span` is raw wall-clock `:62-65`; docstring `:1` | yes |
| "leading/trailing absence excluded" | the span runs first→last **observed** timestamp, so absence outside that range is invisible to both numerator and denominator `:62`; pinned by value in `tests/test_data_gap_ratio.py:90-94` (`[3600, 7200, 10800]` @1h → `expected_bars == 3`, `missing_bar_count == 0`, `series_clean` True) | yes |
| "v1" | the module carries no `__version__`; the only version token is the policy's `gap_method_version == "data_gap_ratio_m2_v1"`, which `measure_data_gaps` **requires** and refuses otherwise `:51-52` (refusal pinned by `tests/test_data_gap_ratio.py:106`) | yes — the "v1" is anchored to a string the helper enforces |
| "half-open span" | `expected_bars = round(span/step) + 1` is the count of **bar-open slots over the inclusive observed range**, which equals the half-open wall-clock cover `[first_open, last_open + step)` divided by `step`. Pinned by value: `[0, 570]` @5m → `expected_bars == 3`, `m2 == 1/3` (`tests/test_data_gap_ratio.py:65-69`); the 1h fixture `[0,3600,7200,14400,18000]` → `m2 == 1/6` (`:51`) | yes under bar-open semantics — **with the caveat below** |

**Caveat to record, not a finding.** "half-open span" is correct for the interval the bars *cover*, but the denominator is **not** `span/step` — the `+1` makes it endpoint-inclusive in slot count. A future implementer reading only the pin string could drop the `+1` and shift every ratio. The arithmetic is pinned by value in three test cases, so the code cannot drift silently; only the prose is under-specified.

Second observation, pre-existing on master and unchanged by this slice: a delta of **exactly** `1.5 · step` is not counted (`> 1.5 * step`, `:69`) even though `round(1.5) - 1 = 1` would attribute one missing bar to it; it lands in `irregular_interval_count` instead (`:75-79`). The pin's phrase "counted gaps" covers this, and `series_clean` still goes False, so nothing is hidden.

---

## 6. Scope statement

- `git -c safe.directory=* diff --name-status fcac0ac6 7fecf204` → exactly three entries, all `M`, all under `MTC_COMMAND_CENTER/03_QUANTLENS/tools/`: `p021_readiness_rules.py`, `tests/test_p021_eligibility.py`, `tests/test_strategy_type_policy_set.py`. No file added, deleted or renamed. `--numstat`: **+53/−9**, **+22/−2**, **+2/−1** → total **+77/−12**.
  - Record-accuracy note (not a code finding): `LEAD_VERIFICATION_P021_S1.md:7` states "+62/−12", "+18/−1", "+3/−1". Those are `--stat` total-changed-line counts (53+9, 2+1) presented as insertion/deletion pairs, so the per-file numbers in that record are mislabelled. The scope claim it supports — three files, artifact untouched — is correct.
- **No protected path.** Checked by hand rather than trusting the hook (which is known to be unenforced): `MTC_COMMAND_CENTER/09_DOCS/PROTECTED_PATHS_POLICY.md:7-12` lists `01_MASTER TEMPLATE_V2/{01_PINE,00_PYTHON,05_PARITY}/` and `MTC_COMMAND_CENTER/MTC Command Center ARCHITECTURE.md` — none of the three files is in or under any of them. The Lead's guard dry-run independently reports `[protected] none`.
- **The pre-existing F401 is not the slice's.** `ruff 0.16.4 check --no-cache --select F,E9` on the three candidate files gives one finding: `F401 'json' imported but unused` at `tests/test_strategy_type_policy_set.py:4`. The same ruff invocation on the `fcac0ac6` blob of that file gives the identical finding, and `import json` appears nowhere in the 190-line slice diff. The candidate catalogue itself is clean (`All checks passed!` on the base copy too).

---

## 7. Findings

### REQUIRED-1 — the pinned B-05 definition is not the M-C the owner ratified
`MTC_COMMAND_CENTER/03_QUANTLENS/tools/p021_readiness_rules.py:206-212` (wired at `:274`; `divergence_metric.B05` dropped from `missing_rules` at `:276`).

Packet §4 defines option **M-C** by reference to the two rows above it in the same table: "both — **M-B** as the gate on signal fidelity, **M-A** as the economic divergence, each with its own tolerance". The owner's word `recomended` selected that option; it did not author prose. The code substitutes a different definition on both halves:

**(b) vs M-A.** Ratified: "per-pair **signed** difference of **realized trade return** (forward − backtest), aggregated as the mean over the aligned window, **reported with the count and the standard deviation**", unit "**return fraction per trade**". Code (`:209-210`): "the outcome-level divergence = **mean absolute** difference of **realised R-multiples** over matched pairs". Three concrete departures:
1. **signed → absolute.** These are different statistics, not a rephrasing. A signed mean of −0.02 (forward worse than backtest) and +0.02 (forward better) are opposite findings; a mean-absolute statistic reports 0.02 for both and cannot be inverted back. The packet's own Pros for M-A — "directly the quantity the owner cares about (did forward behave like the backtest)" — is the direction that is lost.
2. **return fraction per trade → R-multiple.** An R-multiple is P&L divided by the risk unit, and the **risk-unit source is blocker B-04, still OPEN** (`P021_GAP_TABLE_20260915.md:33`, deferred to S3 at `:58`; wired as `risk_unit_source.B04` in `P021.BASIC_FAILURE_FLOOR`'s `missing_rules`, `p021_readiness_rules.py:263`). So this slice declares B-05 closed with a definition denominated in a unit whose defining blocker is open — and `P021.BACKTEST_FORWARD_DIVERGENCE`'s own `missing_rules` (`:276`) does **not** list B-04, so that dependency is recorded nowhere.
3. **count and standard deviation dropped.** The packet specified the reporting triple precisely because M-A's stated Cons is "needs ≥ N pairs (B-07 min pairs) before it is stable". A bare mean is the part that is unsafe at small N.

**(a) vs M-B.** Ratified: "intent-level agreement rate: share of backtest intents that the forward path produced **at the same bar** (**entry/exit decisions match**), **independent of P&L**". Code (`:208-209`): "share of backtest intents with no forward counterpart or **a different side/size class**". Stating it as divergence rather than agreement is fine — the field is named divergence — but the matching criterion is replaced: "**size class**" introduces a classification whose boundaries are defined nowhere (`"size class"`, `"side/size"`, `"outcome-level divergence"`, `"decision-level divergence"` have **zero** occurrences in the repository worktree and zero in CT13 outside this slice's own review folder), it would itself become a new open number, and "entry/exit decisions match" and "independent of P&L" are both dropped.

Why this matters rather than being cosmetic: `divergence_metric_definition` is the field the slice *adds as authoritative* and simultaneously the reason `divergence_metric.B05` may be removed from the refusal list. It is the text a shadow-window schema would be built from. Nothing becomes ready (the rule still refuses on B-01, B-07, B-20 and three open numbers), so this is a specification defect, not a fence breach.

Note for the record: the prior reviewer's fidelity table (`GEMINI/REPORT_RESPONSE_UTF8.md:17`) quotes the packet's M-C row and still grades **EQUAL**, and `:27` calls the code's two halves "verbatim". Its own quoted evidence does not support that grade; M-A and M-B were never expanded and compared. This is the "two reviewers agreeing is not corroboration" shape — I reached the opposite reading from the bytes.

**Fix (either is enough):** (i) restate M-A and M-B verbatim from packet §4 inside `DIVERGENCE_METRIC_DEFINITION`, pin the new string by equality like the B-17 pin, and add `risk_unit_source.B04` to the divergence rule's `missing_rules` if the R-multiple unit is kept anywhere; or (ii) keep the Lead's prose but label it Lead-derived, restore `divergence_metric.B05` to `missing_rules`, and put the definition to the owner as a one-line ask.

### REQUIRED-2 — the catalogue declares one divergence tolerance where the ratified option makes it two
`p021_readiness_rules.py:191` declares a single `MissingNumber("divergence_tolerance", "How much backtest-to-forward difference is permitted?", "B-06")`, while the very definition added three lines earlier says a check "consumes both numbers against **their own tolerances**" (`:211`, plural), and packet §4's M-C row states the consequence explicitly: "two tolerances to ratify later (**B-06 becomes two numbers**)".

So the new bytes contradict themselves, and the catalogue under-declares what stays open under M-C: a later implementer ratifying one blended tolerance would satisfy the open-number list while leaving one of the two ratified failure modes ungated. Nothing is made ready by this (all three open names still refuse).

**Fix:** split `divergence_tolerance` into the two names the option implies (with `EXPECTED_OPEN_NUMBER_NAMES`, the refusal wiring at `:275` and both fence assertions updated), **or** state inside the definition that the split itself is deferred to B-06 and keep one name deliberately.

### NIT-1 — `self_check()` prints a hard-coded S2 claim it never verifies
`p021_readiness_rules.py:418`. The three lines above it derive from the data (`len(RULES)`, `len(CLOSED_NUMBERS)`, `POLICY_SET['profile']`, `len(OPEN_NUMBERS)` — `:414-416`) and the two "MODIFIED COPY DETECTED" lines narrate assertions that actually ran just above. Line 418 asserts nothing. Demonstrated: with `gap_ratio_max` mutated to `0.001` and `dataset_hash_contract` to `ds-v2`, `--self-check` still printed

```
SELF-CHECK PASS: 7 checks all refuse readiness
S2 CLOSED (catalogue only): gap_ratio_max=0.0001 on m2; B-17 formula pin; B-13 ds-v1 pin; B-05 metric M-C
```
and exited 0, while the catalogue actually held `gap_ratio_max = 0.001` and `dataset_hash_contract = 'ds-v2'`.

Graded NIT, not REQUIRED, because the authoritative fence — the test suite — catches every one of those value changes (§3.5). But it is a real honesty hole: this brief itself treats `--self-check` as standalone fence evidence, and the *next* slice (B-22) is expected to change this very value, at which point a lockstep value+test edit would leave a stale literal shipping under "SELF-CHECK PASS". **Fix:** interpolate the values, one line.

### NIT-2 — the S2 provenance is unpinned while the S2 values are pinned
Three mutations survive a fully green suite (§3.5): `POLICY_SET["s2_source_document"]` replaced by "some other undated source …" (`:63-66`), `POLICY_SET["s2_decided_at"]` set to `2020-01-01` (`:62`), and the `gap_ratio_max` `ClosedNumber.source` prose rewritten to "invented with no owner source …" (`:178-182`). The brief lists "`POLICY_SET.owner_decisions` extended with a **dated S2 source**" as a deliverable of this slice, and Gemini's NIT-1/NIT-2 were closed precisely by adding equality pins for the formula id and the value. The same standard applied to the provenance would add `self.assertEqual(record["policy_set"]["s2_decided_at"], "2026-09-15")` and an `assertIn("OD-20260915-P021-S2-RECOMMENDED-1", …s2_source_document)`. Two lines.

### NIT-3 — the B-13 pin's named carrier field exists nowhere
The DECISIONS row's item (3) and packet §3 both name it: the DATA_QUALITY measured-value object "carries `dataset_manifest_hash = <ds-v1 digest>` and names the contract". The catalogue names the contract (`:244`) and drops `dataset_hash_contract.B13` from the refusal list (`:246`), but `dataset_manifest_hash` has **zero** occurrences in the worktree (grepped `*.py`, `*.json`, `*.md` across the repository). Nothing carries that half of the ratified pin forward to the producer that will eventually emit the object. Recording it as a limit alongside the contract — e.g. `("dataset_hash_field", "dataset_manifest_hash")` — is one line and keeps the closure complete. Reasonable to defer, since no measured-value object exists in this bounded step (B-01), but then it should be named in the record rather than dropped.

### NIT-4 — precision on what the ready-fence guarantees (no code change needed)
The brief asks for proof that "a rule with `missing_rules=()` is refused by `validate_catalog`". The exact guarantee is narrower and should be recorded as such: the guard at `:336-338` fires only when **both** `missing_numbers` and `missing_rules` are empty. Proven both ways in §3.3 — DATA_QUALITY with `missing_rules=()` is refused (it has no open numbers), while BACKTEST_FORWARD_DIVERGENCE with `missing_rules=()` is *accepted* by `validate_catalog` because its three open numbers survive. That is coherent design, not a defect: an open number is itself a refusal anchor, and `_refusal` (`:291-293`) still emits `refusing: divergence_tolerance, …` so the rule's status stays `REFUSED`. No change requested; stating the stronger claim in a future record would be wrong.

### NIT-5 — the S2 closed number is appended by rebinding the tuple
`:172-184` does `CLOSED_NUMBERS = CLOSED_NUMBERS + (ClosedNumber("gap_ratio_max", …),)` instead of adding the entry inside the literal at `:84-170`. Consequences are cosmetic but real: a reader of the `CLOSED_NUMBERS` literal counts twelve, and `gap_ratio_max` sorts last in every derived ordering (the `closed_numbers` list in the record, the owner view at `:439-441`). Folding it into the literal removes a footgun for the next editor.

---

## 8. NOT VERIFIED

1. **No real bundle was evaluated, by design.** No evaluator exists (B-01, `accepted_corrected_engine.B01` on all seven rules). `check_set_identity` stays `None` (`:363`). Nothing here says `P021.DATA_QUALITY` would pass on real data — only that its limits are now recorded and it still refuses.
2. **Suitability of `0.0001`, of m2, and of the M-C option is not judged.** The packet says plainly that both scans measured exactly `0.0`, so no option is data-calibrated; this is an owner appetite. I verified the code faithfully records the owner's choice, not that the choice is right.
3. **The "accepted" `strategy_type_policy_set` artifact has no independent record I could reach.** It exists only as the test fixture (`tests/test_strategy_type_policy_set.py:21-57`) and its version string `p021pol-v1:4a807136e78650ef393556f91d3448855fc397ee9f0eee6efb7594c9dbdf69f2` (`:56`); no policy-set JSON exists in the worktree, and that hash appears nowhere in `C:/CT13` except this slice's own `GEMINI/` folder. So "artifact UNTOUCHED" is verified as **byte-unchanged by this slice** (the diff touches neither `:44` nor `:56`; that file's whole change is +2/−1), **not** as matching an externally recorded accepted artifact. If the owner needs the stronger statement, the accepted artifact's hash has to be recorded outside the test that asserts it.
4. **Whole-set ratification (B-22) is the owner's act.** I state only that no consumer can act on the `0.0001`-vs-`None` difference today (§4); I make no ratification recommendation.
5. **Only the three modules the brief names were run**, not the repository's full suite. I did not measure whether any other test in the repo depends on the catalogue (the import grep says none does, but I did not execute the rest of the suite).
6. **Interpreter provenance.** 3.12.12 came from `C:\tmp\P012_FUNDING_PY312_20260911\Scripts\python.exe` with pytest 9.1.1, whose subtest reporting is native; `pytest_subtests` is not importable there. Counts matched the brief exactly, but this is not the same environment string the Lead's `LEAD_PYTEST.txt` may name.
7. **Owner-word chain beyond the DECISIONS row.** I read `DECISIONS.md:132` and the packet; I did not open `OWNER_ANSWERS_20260915.md` to re-verify the raw chat transcript behind the word `E recomended`.
8. **Footprint disclosure.** Every mutation I ran was on my own scratch copies under `C:/tmp/OPUS_P021S1_SCRATCH/`, each restored byte-identically. Re-checked at the end of the review: HEAD is still `7fecf204c5d457ff19872c97e5d27e2d5a712508` and all three worktree source files still carry the sha256 values recorded in §1, so no repository source byte changed. The one side effect I cannot rule out is refreshed `__pycache__` bytecode in `tools/` and `tools/tests/` from running the suite there — untracked, and such caches already existed before my run. `-p no:cacheprovider` was used, so no `.pytest_cache` was created.

---

## 9. Bottom line

The mechanical work on this slice is sound and independently reproducible. HEAD is the required candidate; the three files are exactly the declared scope with no protected surface; the pre-existing F401 is provably not the slice's; the 59 + 108 test result is exactly as predicted; the B-17 formula pin is byte-identical across code, the DECISIONS row, the S2 packet and the test literal, and it honestly describes what `data_gap_ratio.py` computes; both RED arms reproduce with the reasons stated, against a control arm I added; and the ready-fence holds under my own mutants — a rule stripped of every anchor is refused and `ready` cannot become True. Ten of thirteen of my value mutations are caught by the suite, which closes Gemini's NIT-1 and NIT-2 for real.

What blocks acceptance is one pin, B-05. The owner's word chose option M-C; the bytes pin a Lead-authored definition that replaces the ratified M-A (signed return-fraction mean with count and standard deviation) with a mean-absolute R-multiple — a different statistic, in a unit whose source blocker B-04 is still open and is not wired into that rule — and replaces the ratified M-B matching criterion with an undefined "side/size class". The same commit then declares one divergence tolerance where the chosen option requires two, contradicting its own new prose. Both are fixable in the catalogue without touching the fence, and neither makes anything ready. Fix those two, or re-open B-05 and put the definition to the owner; the other five items are nits and can travel with the fix.

VERDICT: REQUEST_CHANGES
