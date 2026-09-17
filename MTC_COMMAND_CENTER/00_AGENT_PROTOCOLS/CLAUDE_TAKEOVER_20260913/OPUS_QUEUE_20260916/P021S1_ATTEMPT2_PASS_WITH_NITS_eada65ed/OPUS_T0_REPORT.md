# T0 review report — WP-P0-21 S1 catalogue-only slice, candidate `eada65edfeacef9ebbe5b237d8e111caf36052e4`

Reviewer: exact `claude-opus-5`, effort xhigh. **Second exact-flagship read, T0 repair round 1 of 3** on this LEAD-AUTHORED slice (Claude Opus 5 Lead, disclosed builder of both the slice and the repair). No delegation, no subagents, no other session resumed.
Brief: `C:/tmp/OPUS_QUEUE_20260916/P021S1/REVIEW_BRIEF.md` + its 2026-09-17 addendum. Launch instruction: `C:/tmp/OPUS_QUEUE_20260916/P021S1/opus/BRIEF.md`.
Scratch (every working copy and every mutant): `C:/tmp/OPUS_P021S1_SCRATCH/`. Nothing written into any repository; no `git status`, no working-tree diff, no `add`/`commit`/`checkout`/`push`.

**Pin contradiction inside my own launch instruction, resolved and disclosed.** `opus/BRIEF.md` line 1 (title) says the candidate was **RE-PINNED 2026-09-17 19:0x to `eada65ed`**, while its line 3 still carries the stale sentence "if HEAD is not `7fecf204…`, your verdict must be BLOCK". `REVIEW_BRIEF.md:11` — the document that same line 3 orders me to "read and execute exactly" — requires HEAD `eada65ed`, and the addendum (`:28-31`) re-pins the lane explicitly. I therefore treat `eada65ed` as the required HEAD and did **not** BLOCK on the stale clause. Recorded here so the lane owner can fix line 3 before the Friday Sol lane, which reads the same file.

---

## 1. Verified identities

| Item | Value |
|---|---|
| COMPUTED HEAD (`git -c safe.directory=* -C C:/tmp/P021_S1_20260915 rev-parse HEAD`) | `eada65edfeacef9ebbe5b237d8e111caf36052e4` — **matches the re-pinned candidate** |
| Base for every byte comparison | `fcac0ac6` (`git diff fcac0ac6 eada65ed -- …`), repair delta against `7fecf204` |
| **Catalogue file, git blob content sha256** | `p021_readiness_rules.py` = **`84fc82cab8a84ae7492e48a26eb67e370a8f5b5b0b0c52d88051ed86968bcedf`**, 20 822 bytes |
| Catalogue file, working-tree checkout (CRLF) | 21 311 bytes, sha256 `b8fa0ae82f7ed2ea12072720e46fcdb16426e7eac2fcc52a936ccb6aa0af095b` |
| `tests/test_p021_eligibility.py` | blob content sha256 `efe49452e405568707f91943059a12d01163d7097d152f11c711bfbcc7997409`, 71 818 bytes |
| `tests/test_strategy_type_policy_set.py` | blob content sha256 `a489b1952252357eb69939f2015601ae844da65adf178219a76331c7cac27420`, 5 608 bytes |
| `fcac0ac6` blobs used for the RED arms | `27a7e6ed…` / `97ef543b…` / `9cebde27…` |

Both hash forms are given deliberately: the checkout is CRLF and **its hash is not the repository's bytes**. The blob content sha256 is the one to re-pin. I proved the checkout is only a line-ending transform of the blobs rather than assuming it (`C:/tmp/OPUS_P021S1_SCRATCH/normcmp.py`):

```
p021_readiness_rules.py:          normalized IDENTICAL blob_sha256=84fc82ca…
test_p021_eligibility.py:         normalized IDENTICAL blob_sha256=efe49452…
test_strategy_type_policy_set.py: normalized IDENTICAL blob_sha256=a489b195…
```

So the bytes I executed are HEAD's bytes.

Authorities read as bytes, never through a report's description:

- `C:/CT13/DECISIONS.md:132` — row `OD-20260915-P021-S2-RECOMMENDED-1`, owner's exact word `E recomended`, ~18:25Z 2026-09-15. Also read `:135` (`OD-20260916-P021-S1-CATALOGUE-ONLY-1`, owner word `H catalogue only`).
- `P021_OPTIONS_PACKET_S2_20260915.md` §1–§5. Both copies (CT13 `QUEUED_PACKAGES_20260915/` and `C:/tmp/CLAUDE_P0_RUN_20260913/`) are byte-identical, sha256 `d49ad653013e00741a8abf37456078e2438a3797e7a4e54fa0ce9397987dc619`.
- `QUEUED_PACKAGES_20260915/P021_S1_20260915/REPAIR_R1_20260917/` — `LEAD_VERIFICATION_P021_R1.md`, `LEAD_GUARD_R1.txt`, `LEAD_PYTEST_GREEN_R1.txt`, `GEMINI/REPORT_RESPONSE_UTF8.md`.
- The round-1 report `OPUS_QUEUE_20260916/P021S1_ATTEMPT1_REQUEST_CHANGES_7fecf204/OPUS_T0_REPORT.md` (250 lines), to know exactly which five NITs were carried.

---

## 2. Fidelity table — the four values/pins vs the DECISIONS row and the S2 packet text

All code line numbers are `MTC_COMMAND_CENTER/03_QUANTLENS/tools/p021_readiness_rules.py` unless stated.

| # | Pin | Authority (bytes) | Code (file:line) | Comparison |
|---|---|---|---|---|
| 1 | **B-02 value + metric** | `DECISIONS.md:132` item (1): `P021_DECISION_3 = T`, `gap_ratio_max = 0.0001` on `gap_ratio_metric = "m2_missing_bar_ratio"`, "coverage stays a separate rule". Packet `:16` option **T** = `0.0001` ("≈ 24 missing bars in a 245 873-bar 5m series"); `:18` "no option is data-calibrated … an appetite for unseen gapping … coverage is a separate rule … never through `gap_ratio_max`" | `:58` (`"P021_DECISION_3": "T"`), `:172-183` (`ClosedNumber("gap_ratio_max", 0.0001, …)`, value at `:175`), `:252` DATA_QUALITY limit, `:253` metric; provenance prose `:178-182` reproduces the packet's own 4 105 966 / 4 477 626 / 245 873 and its "appetite for unseen gapping" wording and repeats "Coverage is a separate rule, never this one" | **EQUAL** |
| 2 | **B-17 formula pin** | Row item (2) and packet `:23` give the string; both read as bytes | `:200-203` `GAP_RATIO_FORMULA_ID`, `:254` DATA_QUALITY limit, test literal `test_p021_eligibility.py:97-101` | **EQUAL — byte-identical** (unchanged by the repair; independently re-read this round) |
| 3 | **B-13 digest pin** | Row item (3): `dataset_hash_required` satisfied by the `ds-v1` digest of the bundle the check scanned, "contract named", P0-20/P0-30 hashes stay separate. Packet `:26` adds the consequence "the DATA_QUALITY measured-value object carries `dataset_manifest_hash = <ds-v1 digest>` and names the contract" | `:255` (`("dataset_hash_contract", "ds-v1")`), `:251` `dataset_hash_required` True, `:257` `missing_rules` reduced to `accepted_corrected_engine.B01` alone; no equation with any P0-20/P0-30 hash anywhere | **EQUAL for what this slice covers.** The `dataset_manifest_hash` half belongs to a measured-value object that does not exist under B-01 — still recorded nowhere: **NIT-3, re-raised** |
| 4 | **B-05 divergence metric + definition** | Row item (4): `P021_DIVERGENCE_METRIC = M-C`, "B-05 definition CLOSED; B-06/B-07 stay measure-first". Packet `:32-35` rows **M-A**, **M-B**, **M-C** and M-C's Cons "two tolerances to ratify later (B-06 becomes two numbers)" | selector `:59` and `:285`; `DIVERGENCE_METRIC_M_A` `:210-214`, `DIVERGENCE_METRIC_M_B` `:215-218`, `DIVERGENCE_METRIC_DEFINITION` `:219-223`; the two B-06 names `:191-192`; wiring `:286-291` | **EQUAL** — see §2.1 for the character-level proof. **Both round-1 REQUIREDs are closed.** |

### 2.1 REQUIRED-1 and REQUIRED-2 — decided with my own comparison, not the builder's claim

I parsed packet §4's table rows out of the file and compared them to the module constants character by character (`C:/tmp/OPUS_P021S1_SCRATCH/verbatim.py`, run against my scratch copy of the candidate module):

```
M-B: code == '<row>; unit: <unit>' ?  True
M-A: code == '<row>; unit: <unit>' ?  False
     first difference at char 66: packet '−' (U+2212) vs code '-' (U+002D)
     packet: ...rence of realized trade return (forward − backtest), aggregated as the mean over...
     code:   ...rence of realized trade return (forward - backtest), aggregated as the mean over...
     equal after ASCII-folding the dashes?  True
M-C row present verbatim (ASCII-folded)?   True
```

- **M-B is exactly the packet row**, character for character, with the option label prefixed and the Unit column appended as `; unit: fraction`. "at the same bar", "(entry/exit decisions match)" and "independent of P&L" — the three clauses the first spelling dropped — are all present.
- **M-A is exactly the packet row** after one substitution: the packet's U+2212 MINUS SIGN in "forward − backtest" is an ASCII hyphen in the code. Semantically identical, and it follows the standing ASCII-only convention for these records. "signed", "realized trade return", "the mean over the aligned window", "reported with the count and the standard deviation", unit "return fraction per trade" — all present.
- **M-C** is the packet's M-C metric cell verbatim (em dash ASCII-folded), followed by the packet's own Cons clause expanded into the two catalogue names, then M-B and M-A in full.
- **No hidden B-04 dependency.** Token scan of the composed definition: `absolute` **False**, `R-multiple` **False**, `size class` **False**, `B-04` **False**, `risk unit`/`risk_unit` **False**. The divergence rule's `missing_rules` (`:292`) is `accepted_corrected_engine.B01`, `divergence_alignment.B07`, `divergence_provenance.B20` — B-04 is correctly absent, because the unit is now a return fraction and not an R-multiple.
- **REQUIRED-2** is closed structurally, not just in prose: `OPEN_NUMBERS` `:191-192` declares `divergence_tolerance_intent` (question text framed on M-B: "how much intent-level disagreement … is permitted?") and `divergence_tolerance_return` (framed on M-A: "how much signed mean difference of realized trade return (forward - backtest) is permitted?"), both blocker `B-06`; the rule's `missing_numbers` `:286-291` carries four names; `EXPECTED_OPEN_NUMBER_NAMES` `:197` derives from the tuple, so the wiring gate in `validate_catalog` `:341-345` enforces the pair.

Everything else the addendum claimed for the repair also holds: `POLICY_SET` carries `s2_decided_at` `:62` and a dated `s2_source_document` naming the decision row `:63-66`; the self-check's S2 line now interpolates the catalogue values `:434-441`.

---

## 3. Fence proof (commands, cwd, output — all run by me)

**Interpreter.** The brief pins 3.12.12. `python` on PATH here is 3.14.2, and the uv-managed 3.12.12 has no packages, so I built my own venv: `uv venv --python 3.12.12 C:/tmp/OPUS_P021S1_SCRATCH/venv312` + `pytest 9.1.1`, `pytest-subtests 0.15.0`, `pydantic 2.13.5` → **Python 3.12.12**. (The repo's `mtc_contracts` needs pydantic; without it collection errors out, which is how I confirmed the import path is real and not stubbed.)

### 3.1 The three mandated modules — cwd `C:\tmp\P021_S1_20260915`

```
$env:PYTHONPATH = "MTC_COMMAND_CENTER/contracts;MTC_COMMAND_CENTER/03_QUANTLENS/tools"
<venv312> -m pytest MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p021_eligibility.py \
                    MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_strategy_type_policy_set.py \
                    MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_data_gap_ratio.py \
                    -q -p no:cacheprovider --basetemp C:/tmp/OPUS_P021S1_SCRATCH/bt
```
```
59 passed, 108 subtests passed in 0.46s
exit=0
```

**Exactly the 59 + 108 the brief predicted**, and exactly what `LEAD_PYTEST_GREEN_R1.txt` records. (The `--basetemp` under `C:/tmp` did not reproduce the known Bridge-staging phantom-failure mode; that defect is specific to `test_mtc_funding_export`, which is not in this set.)

### 3.2 Self-check — cwd `C:\tmp\P021_S1_20260915`

```
<venv312> MTC_COMMAND_CENTER/03_QUANTLENS/tools/p021_readiness_rules.py --self-check
```
```
SELF-CHECK PASS: 7 checks all refuse readiness
CLOSED NUMBERS: 13 (profile balanced, provisional)
OPEN NUMBERS: 4
MODIFIED COPY DETECTED: divergence tolerance refusal wiring removed
S2 CLOSED (catalogue only): gap_ratio_max=0.0001 on m2_missing_bar_ratio; B-17 formula pin 'm2_missing_bar_ratio@data_gap_ratio.py v1 (fixed-step 24/7, half-open span, leading/trailing absence excluded)'; B-13 ds-v1 pin; B-05 metric M-C
MODIFIED COPY DETECTED: swing_forward_period closure removed
READY=False
exit=0
```

Note `OPEN NUMBERS: 4`, where round 1 printed `3`, and an S2 line that now carries the full formula-pin string because it is interpolated from the catalogue rather than hard-coded.

### 3.3 My own mutant trees

To keep the repository untouched I assembled a **self-contained scratch tree** mirroring the repo layout (`tools/`, `tools/tests/`, `contracts/mtc_contracts/`), so the tests' own `sys.path.insert(str(parents[1]))` resolves to **my** copy and never to the worktree (`build_tree.py`). Control first, because a RED means nothing without it:

```
CTRL (unmutated scratch tree): 59 passed, 108 subtests passed — exit 0
```

Identical to §3.1, so the layout is faithful. Each mutant then got its **own freshly built tree** — no restore step exists, so no restore can fail. Every mutation is an exact string replacement verified by read-back (`applied=True` means the new text is present *and* the old text is gone) before the suite runs (`mutants.py`).

| My mutant | read-back | pytest | `--self-check` | Verdict |
|---|---|---|---|---|
| **M1** old (round-1) `DIVERGENCE_METRIC_DEFINITION` restored | applied | **46 failed**, 13 passed | exit 0 | **CAUGHT** — REQUIRED-1's fix is fenced |
| **M2** B-06 collapsed back to one `divergence_tolerance` (OPEN_NUMBERS + wiring + self-check probe, self-consistently) | applied | **47 failed**, 12 passed | exit 0 | **CAUGHT** — REQUIRED-2's fix is fenced |
| **M3** M-A tail → "mean absolute R-multiple / R-multiple per trade" | applied | **46 failed** | exit 0 | CAUGHT (the `assertNotIn` guards) |
| **M4** "each with its own tolerance" → "under one blended tolerance (B-06 stays one number" | applied | **46 failed** | exit 0 | CAUGHT |
| **M5** M-B "at the same bar (entry/exit decisions match), independent of P&L" → "somewhere in the window" | applied | **46 failed** | exit 0 | CAUGHT |
| **M6** `gap_ratio_max` 0.0001 → 0.001 | applied | **46 failed** | exit 0, and the S2 line printed **`gap_ratio_max=0.001`** | CAUGHT — **round-1 NIT-1 is genuinely closed**: no stale literal can ship |
| **M7** `s2_decided_at` → 2020-01-01 | applied | **46 failed** | exit 0 | CAUGHT — **round-1 NIT-2 closed** (this mutation *survived* a green suite in round 1) |
| **M8** `s2_source_document` → "some other undated source" | applied | **46 failed** | exit 0 | CAUGHT — **round-1 NIT-2 closed** |

M2 reddens one more test than the others because it also breaks `test_strategy_type_policy_set.py:118-123`, which is the file the repair had to follow.

### 3.4 The ready-fence, under my own mutants (`fence.py`, in-memory on my scratch copy)

```
missing_rules=() on P021.DETERMINISTIC_REPLAY:        REFUSED: … could be presented as ready
missing_rules=() on P021.LOOKAHEAD_PREFIX:            REFUSED: … could be presented as ready
missing_rules=() on P021.REPAINT_CLOSED_BAR:          REFUSED: … could be presented as ready
missing_rules=() on P021.DATA_QUALITY:                REFUSED: … could be presented as ready
missing_rules=() on P021.BASIC_FAILURE_FLOOR:         REFUSED: … could be presented as ready
missing_rules=() on P021.UNSIMULATED_CONTROLS:        REFUSED: … could be presented as ready
missing_rules=() on P021.BACKTEST_FORWARD_DIVERGENCE: ACCEPTED by validate_catalog

divergence rule with BOTH tuples empty: REFUSED: open-number refusal wiring changed;
    missing=['divergence_min_paired_observations','divergence_tolerance_intent',
             'divergence_tolerance_return','divergence_window_length']
all seven rules stripped:               REFUSED: (same wiring error)
readiness_record() on the all-clear catalogue: REFUSED TO BUILD (same wiring error)
divergence rule with missing_rules=() only: record ready=False, that check status='REFUSED',
    reason='no limit or required rule set, refusing: divergence_tolerance_intent,
            divergence_tolerance_return, divergence_window_length, divergence_min_paired_observations'
```

Source audit for a True path — the only occurrences of `ready` are `:354` (the guard's message), **`:377` `"ready": False,`**, `:401` `assert record["ready"] is False`, `:469` the owner-view string. **No line assigns True to `ready`.**

So: **a rule that has lost every refusal anchor is refused by `validate_catalog`, and `readiness_record()["ready"]` cannot become True.** The precise guarantee is narrower than the brief's phrasing and is restated as **NIT-4** below — the guard at `:352-354` fires only when *both* tuples are empty, which is why the divergence rule survives `missing_rules=()` while still coming out `REFUSED` on its four open numbers.

### 3.5 RED arms 1 and 2 — reproduced from `fcac0ac6` blobs, against the control above

| Arm | Contents | Result |
|---|---|---|
| **CTRL** (mine) | candidate catalogue + candidate tests, scratch layout | 59 passed, 108 subtests, exit 0 |
| **RED 1** | `fcac0ac6` catalogue + **candidate** tests | **47 failed**, 12 passed, exit 1 |
| **RED 2** | **candidate** catalogue + `fcac0ac6` tests | **47 failed**, 12 passed, exit 1 |

Reasons, not just counts (first failure under `-x`):

- **RED 1** — `test_p021_eligibility.py:95` inside `assert_readiness_fence`, reached from `setUp` at `:148`: `KeyError: 'gap_ratio_max'`. The old catalogue's DATA_QUALITY has no such limit.
- **RED 2** — `test_p021_eligibility.py:92` (base numbering) inside `assert_readiness_fence`: `AssertionError: Items in the first set but not the second: 'divergence_tolerance_return', 'divergence_tolerance_intent'; Items in the second set but not the first: 'gap_ratio_max', 'divergence_tolerance'`. That single assertion catches **both** the S2 closure and the M-C split at once.

The 47-wide blast radius is by design: `P021ContractTestCase.setUp`/`tearDown` (`:147-151`) call `assert_readiness_fence()`, so any catalogue/test mismatch reddens every test in the module.

---

## 4. Artifact statement (catalogue `0.0001` vs artifact `None`)

**No consumer on master reads both, and nothing can act on the difference today.**

- `p021_readiness_rules` is imported by exactly two files in the whole worktree — `tests/test_p021_eligibility.py:15` and `tests/test_strategy_type_policy_set.py:13`. **There is no production importer**, and `check_set_identity` is still `None` (`:380`).
- `strategy_type_policy_set` is imported by `data_gap_ratio.py:9` and `strategy_type_classifier.py:9`, both for `validate_policy_set` only.
- `_SHARED_KEYS` (`strategy_type_policy_set.py:42-52`) only requires the key to be *present*; `data_gap_ratio.py` reads only `policy["methods"]["gap_method_version"]` (`:51`) and its docstring states it measures "without sorting, filling, or **applying a policy limit**" (`:48`).
- The only file that touches both surfaces is `tests/test_strategy_type_policy_set.py`, and it asserts them **separately and deliberately**: the artifact's `None` at `:93` and the catalogue's open-number set at `:118-123`. It never compares the two values.
- The "accepted artifact" exists only as the fixture at `:21-57`, with `"gap_ratio_max": None` (`:44`) and version `p021pol-v1:4a807136…` (`:56`). **Byte-unchanged by this slice:** across the whole slice (`fcac0ac6 → eada65ed`) that file's entire change is +4/−2 — a two-line comment at `:94-95` and the open-number set at `:118-122`; across the repair alone it is **+2/−1**, lines 118-122 only. Neither `:44` nor `:56` is in any hunk.

So the contradiction is **latent and harmless now**; it becomes live the moment a first consumer reads either surface — which is exactly the whole-set ratification the owner holds as **B-22**. Not my call, and I make none.

**One thing the repair changed here that the recorded scope does not mention — see NIT-6.** The artifact's `shared` block carries a single `divergence_tolerance` key (`tests/test_strategy_type_policy_set.py:45`, required by `_SHARED_KEYS:49`), while the catalogue now declares **two** B-06 names. `POLICY_SET.s2_scope` (`:67-70`) names only the `gap_ratio_max` divergence. That is a second, structural catalogue-vs-artifact difference, introduced by this repair and recorded nowhere.

---

## 5. Formula-pin honesty statement (B-17)

Pin: `m2_missing_bar_ratio@data_gap_ratio.py v1 (fixed-step 24/7, half-open span, leading/trailing absence excluded)`, against `MTC_COMMAND_CENTER/03_QUANTLENS/tools/data_gap_ratio.py` (untouched by this slice).

| Pin clause | Code | Honest? |
|---|---|---|
| `m2_missing_bar_ratio` | emitted under exactly that key, `:100` | yes |
| numerator = missing bars inside **counted** gaps | `detected = [delta for delta in deltas if delta > 1.5 * step]` `:69`; `missing_by_gap = [max(0, round(delta/step) - 1) …]` `:70`; `missing_bars = sum(...)` `:71`; `m2 = missing_bars / expected_bars` `:85` | yes — "counted" is the honest word: only intervals above 1.5·step contribute |
| denominator = expected bars over the observed span | `span = values[-1] - values[0]` `:62`; `expected_bars = round(span/step) + 1` `:65` | yes |
| "fixed-step" | `step = TIMEFRAME_SECONDS[timeframe]` `:54`, table `:12-19` — single owner of the step | yes |
| "24/7" | no session calendar, weekend mask or holiday logic anywhere in the module; `span` is raw wall-clock `:62-65`; docstring `:1` | yes |
| "leading/trailing absence excluded" | the span runs first→last **observed** timestamp `:62`, so absence outside that range is invisible to both numerator and denominator — exactly the POLUSDT leading-absence case of packet `:10` | yes |
| "v1" | the module has no `__version__`; the only version token is `gap_method_version == "data_gap_ratio_m2_v1"`, which `measure_data_gaps` **requires** and refuses otherwise `:51-52` | yes — anchored to a string the helper enforces |
| "half-open span" | `expected_bars = round(span/step) + 1` | yes **under bar-open semantics**, with the caveat below |

**Caveat, recorded rather than filed as a finding** (the round-1 reviewer reached the same reading independently; I re-derived it rather than adopting it). The denominator is *not* `span/step`: the `+1` makes it endpoint-inclusive in slot count. It is correct precisely if each timestamp labels the half-open bar `[t, t+step)`, so N contiguous observations cover `[t₀, t_last+step)` = N·step and yield N expected bars — which is what `round(span/step)+1` computes. The prose is the only part of the pin no single line mechanises, and a future implementer reading only the string could drop the `+1` and shift every ratio. The arithmetic is pinned by value in `tests/test_data_gap_ratio.py`, so it cannot drift silently. The residual error of the alternative reading is one bar in ~245 873 — four orders of magnitude below the `0.0001` limit — so nothing in this slice turns on it.

---

## 6. Scope statement

- `git -c safe.directory=* diff --name-status fcac0ac6 eada65ed` → **exactly three entries, all `M`**, all under `MTC_COMMAND_CENTER/03_QUANTLENS/tools/`: `p021_readiness_rules.py`, `tests/test_p021_eligibility.py`, `tests/test_strategy_type_policy_set.py`. Nothing added, deleted or renamed. `--numstat`: **+78/−11**, **+53/−3**, **+4/−2** → total **+135/−16** for the whole slice. `git show eada65ed --stat` for the repair alone: **+69/−15**, matching the addendum.
- **No protected path.** Checked by hand rather than trusting the hook (known unenforced): `MTC_COMMAND_CENTER/09_DOCS/PROTECTED_PATHS_POLICY.md:5-12` lists `MTC_V2.pine`, `01_MASTER TEMPLATE_V2/{01_PINE,00_PYTHON,05_PARITY}/`, TradingView export archives, canonical feature contracts and `MTC_COMMAND_CENTER/MTC Command Center ARCHITECTURE.md` — none of the three files is in or under any of them. `LEAD_GUARD_R1.txt:13` independently reports `[protected] none`.
- **The pre-existing F401 is provably not the slice's.** `ruff 0.16.8 check --no-cache --isolated --select F,E9` on the three **candidate blobs** → one finding, `F401 'json' imported but unused` at `test_strategy_type_policy_set.py:4`. The identical invocation on the three **`fcac0ac6` blobs** → the same single finding. `import json` appears in no hunk of the slice diff. With ruff's default rule set: **12 errors on the base blobs, 12 on the candidate blobs — 0 new**, independently confirming `LEAD_VERIFICATION_P021_R1.md:16`.

---

## 7. Findings

**Both round-1 REQUIRED findings are closed** — verified by my own comparison against the packet bytes (§2.1) and by my own mutants M1–M5 (§3.3), not by the builder's evidence. **No new REQUIRED.**

Round-1 NITs 1 and 2 are closed for real: the three mutations that survived a green suite in round 1 (`s2_decided_at`, `s2_source_document`, and the value behind the self-check's S2 line) are each RED now (M6, M7, M8). What remains:

### NIT-3 (re-raised) — the B-13 pin's named carrier field exists nowhere
`DECISIONS.md:132` item (3) and packet `:26` both name it: the DATA_QUALITY measured-value object "carries `dataset_manifest_hash = <ds-v1 digest>` and names the contract". The catalogue names the contract (`p021_readiness_rules.py:255`) and drops `dataset_hash_contract.B13` from the refusal list (`:257`), but **`dataset_manifest_hash` still has zero occurrences in the entire worktree** (re-grepped this round). Nothing carries that half of the ratified pin forward to the producer that will eventually emit the object. Recording it as a limit beside the contract — e.g. `("dataset_hash_field", "dataset_manifest_hash")` — is one line. Deferring is reasonable (no measured-value object exists under B-01), but the deferral should then be *named* in the catalogue rather than silently dropped. `LEAD_VERIFICATION_P021_R1.md:30` already lists it as carried.

### NIT-4 (re-raised, no code change) — state the ready-fence guarantee precisely
The guard at `p021_readiness_rules.py:352-354` fires only when **both** `missing_numbers` and `missing_rules` are empty. Proven both ways in §3.4: six of seven rules are refused by `missing_rules=()` alone, while `P021.BACKTEST_FORWARD_DIVERGENCE` is *accepted* by `validate_catalog` because its four open numbers survive — and still comes out `REFUSED`, with `_refusal` (`:307-309`) naming all four. That is coherent design, not a defect: an open number is itself a refusal anchor. No change requested; I flag it only because the brief's phrasing ("a rule with `missing_rules=()` is refused by `validate_catalog`") is stronger than what the code guarantees, and a future record should not repeat the stronger claim.

### NIT-5 (re-raised) — the S2 closed number is appended by rebinding the tuple
`:172-184` does `CLOSED_NUMBERS = CLOSED_NUMBERS + (ClosedNumber("gap_ratio_max", …),)` instead of adding the entry inside the literal at `:84-170`. Cosmetic but real: a reader of the literal counts twelve, and `gap_ratio_max` sorts last in every derived ordering (`closed_numbers` in the record, the owner view at `:461-464`). Folding it into the literal removes a footgun for the next editor — who, at B-22, is editing exactly this block.

### NIT-6 (new, introduced by this repair) — the recorded S2 scope names one catalogue-vs-artifact divergence, and there are now two
`POLICY_SET.s2_scope` (`:67-70`) says "catalogue only: `gap_ratio_max` closed here; the hashed `strategy_type_policy_set` artifact still carries `gap_ratio_max = None` until the whole set is ratified (B-22)". True, and honest about the *value* difference. But splitting B-06 created a **structural** difference the same sentence does not mention: the artifact's `shared` block has one `divergence_tolerance` field (`tests/test_strategy_type_policy_set.py:45`, required by `strategy_type_policy_set.py:49`, and `_SHARED_KEYS` is an exact-key contract), while the catalogue now declares `divergence_tolerance_intent` + `divergence_tolerance_return`. So B-22 is no longer "fill in one null" — it is a schema change to `_SHARED_KEYS`, the fixture, and therefore the accepted version hash `p021pol-v1:4a807136…`. Nothing anywhere records that consequence. **Fix:** one clause in `s2_scope`, e.g. "…and one `divergence_tolerance` field where the catalogue now declares two B-06 numbers; B-22 must split that field and re-mint the version hash." Graded NIT, not REQUIRED: no consumer reads both (§4), nothing is made ready, and B-22 is the owner's act — but this is precisely the "value changed, field left behind" shape, one ratification event ahead.

### Precision note (no change requested) — one non-ASCII character was folded
The M-A row's U+2212 MINUS SIGN is an ASCII hyphen in `:211` (§2.1). Identical in meaning, consistent with the ASCII-only convention for these records, and the fence pins the folded form by equality — so the two cannot drift apart. Recorded only so that "VERBATIM" in the commit message and in `LEAD_VERIFICATION_P021_R1.md:13` is read as "verbatim modulo that fold", which `:13` does itself disclose.

---

## 8. NOT VERIFIED

1. **No real bundle was evaluated, by design.** No evaluator exists (`accepted_corrected_engine.B01` on all seven rules). `check_set_identity` stays `None` (`:380`). Nothing here says `P021.DATA_QUALITY` would pass on real data — only that its limits are recorded and it still refuses.
2. **Suitability of `0.0001`, of m2, and of the M-C option is not judged.** The packet states both scans measured exactly `0.0`, so no option is data-calibrated; this is an owner appetite. I verified the code faithfully records the owner's choice, not that the choice is right.
3. **The "accepted" `strategy_type_policy_set` artifact still has no record outside the test that asserts it.** It exists only as the fixture (`tests/test_strategy_type_policy_set.py:21-57`) and its version string at `:56`. "Artifact UNTOUCHED" is verified as **byte-unchanged by this slice**, **not** as matching an externally recorded accepted artifact. Carried by the Lead (`LEAD_VERIFICATION_P021_R1.md:30`); still open.
4. **Whole-set ratification (B-22) is the owner's act.** I state only that no consumer can act on either catalogue-vs-artifact difference today (§4, NIT-6); I make no ratification recommendation.
5. **Only the three modules the brief names were run**, not the repository's full suite. The import grep says no other module depends on the catalogue, but I did not execute the rest of the suite.
6. **Interpreter provenance differs from the builder's.** Mine is a venv I created from uv's CPython 3.12.12 with pytest 9.1.1 / pytest-subtests 0.15.0 / pydantic 2.13.5, not the "pinned Bridge 3.12 interpreter" of `LEAD_PYTEST_GREEN_R1.txt`. Version is 3.12.12 as the brief requires and the counts match exactly (59 + 108), but the environment string is not identical.
7. **Owner-word chain beyond the DECISIONS rows.** I read `DECISIONS.md:132` and `:135` and the packet; I did not open `OWNER_ANSWERS_20260915.md` to re-verify the raw chat behind `E recomended` / `H catalogue only`.
8. **The `7fecf204` Gemini review was not re-audited.** I read the round-1 report's note that it graded the definition EQUAL on evidence that did not support it, and I checked that the **repair-round** Gemini report (`REPAIR_R1_20260917/GEMINI/REPORT_RESPONSE_UTF8.md:16-28`) did expand the packet rows cell by cell this time. My own §2.1 comparison is independent of both; I did not re-run either Gemini lane.
9. **Footprint disclosure.** Every mutant ran in its own freshly built scratch tree under `C:/tmp/OPUS_P021S1_SCRATCH/`; no repository file was ever mutated, so no restore step existed to fail. Re-checked at the end: HEAD is still `eada65edfeacef9ebbe5b237d8e111caf36052e4` and the three worktree files still carry the sha256 values in §1. The only side effect I cannot rule out is refreshed `__pycache__` bytecode under `tools/` and `tools/tests/` from the §3.1/§3.2 runs — untracked, and such caches pre-existed. `-p no:cacheprovider` was used, so no `.pytest_cache` was created.
10. **The stale BLOCK clause in `opus/BRIEF.md:3`** is reported, not fixed — I write nothing outside my report directory.

---

## 9. Bottom line

The repair does exactly what round 1 asked, and it does it in the catalogue rather than around it. **REQUIRED-1 is closed:** `DIVERGENCE_METRIC_M_A` and `DIVERGENCE_METRIC_M_B` are packet §4's rows character for character (one U+2212 folded to ASCII), `DIVERGENCE_METRIC_DEFINITION` is the ratified M-C composed of them "each with its own tolerance", and the Lead-authored statistic is gone — no "absolute", no "R-multiple", no "size class", and therefore no unrecorded dependency on the still-open B-04. **REQUIRED-2 is closed:** B-06 is two names, declared, wired into the rule's `missing_numbers`, enforced by the wiring gate and asserted as the whole B-06 set. I reached both conclusions from the packet bytes and my own mutants (M1 → 46 failed, M2 → 47 failed), not from the builder's evidence.

The rest holds as it did: HEAD is the re-pinned candidate and the worktree bytes are HEAD's bytes; scope is exactly three files, +135/−16, no protected surface, 12 ruff findings on base and 12 on the candidate; the B-17 pin is byte-identical and honestly describes what `data_gap_ratio.py` computes; the accepted policy-set fixture and its version hash are byte-untouched; both RED arms reproduce against a control I built, for reasons I read rather than counted; the ready-fence refuses a rule stripped of every anchor and `ready` cannot become True; and the two round-1 NITs that mattered are genuinely closed — the provenance and the self-check's S2 line are now mutation-sensitive where they previously were not.

Four nits travel with it: the B-13 carrier field `dataset_manifest_hash` is still named nowhere (NIT-3), the ready-fence guarantee should be stated at its true width (NIT-4, no code), the closed number is still appended by tuple rebinding into the block B-22 will edit next (NIT-5), and the recorded S2 scope now understates the catalogue-vs-artifact gap by one structural field (NIT-6, new). None of them changes a ratified value, none is reachable by any consumer, and none makes anything ready.

VERDICT: PASS-WITH-NITS
