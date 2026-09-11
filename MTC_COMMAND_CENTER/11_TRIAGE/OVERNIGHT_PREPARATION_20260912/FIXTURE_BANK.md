# Proposed fixture bank (nonbinding preparation)

Status of every case below: **PROPOSED_NOT_EXECUTED**. This file is not implementation, schema, policy, or acceptance authority. It does not authorize a build.

Authority used: baseline source `qa/source_lf` (Git tree `42f99571e6abb5222744d9345e1c8a9e19c23c15`); P013 reader/schema branch `qa/p013_lf` / `inputs/P013_BRANCH` at `3e704c2d` (contracts copied from `42f9957`, unmerged). Designs are historical; newest applicable sections plus actual code control. Working reports under `reports/` are drafts, not inputs. Lead wording in `reports/LEAD_DECISIONS.md` wins conflicts.

Lead independently derived exact canonical JSON and SHA256 with stdlib only (no production helper) in `qa/FIXTURE_EXPECTED_VALUES.json` (`EXPECTED_VALUES_DERIVED_STDLIB_ONLY; TARGET_FIXTURES_NOT_EXECUTED`). Those **literal digests and the valid quoted EVAL preimage** are inserted below. That arithmetic/hash derivation is **executed**. Every target fixture case remains **PROPOSED_NOT_EXECUTED**. Existing `qa/*.log` and `qa/P030_independent_probe.json` are **component evidence only**, never imported as a fixture-run result.

No production numeric policy is minted. Constants are fixture-only (`FB_*`). Cut-off ranking/tie **formula** is not supplied: owner keep-tied-at-cut-off is recorded; any “round to 20 / drop the 21st” rule is incorrect.

| Package | Cases | Failure targets (no duplicates) |
|---|---|---|
| P013 | 5 | identity preimage; field tamper; receipt substitution; two trials/one package; publish-before-complete |
| P021 | 5 | M1/M2/M3 measurement; lookahead future-bar removal; policy-version mismatch; null policy refusal; unset gap limit BLOCKED≠PASS |
| P022 | 5 | complete window untouched=70; absent coverage=0; strategy family split; search-space family split; rehashed truncation |
| P030 | 5 | CURRENT ingest-dup REFUSE vs archive NOOP, PROPOSED identical ingest NOOP; month-boundary gap; forming bar; observation_id collision; process-alive/feed-stale |
| P026 | 4 | injected silence bound OK; injected silence bound silent; backup byte tamper; live append ≠ snapshot |

Proposed consumer paths are the exact modules in `reports/IMPLEMENTATION_MAP.md`. They do not exist as executed QA for these cases. No new tests under the P026 opsa tree: P026 files stay unchanged; P026 cases are consumed by future P030 adapter checkers.

---

## Shared fixture-only identity atoms

UTF-8 JSON encoding is the repository formula (`identity.py` `canonical_json`: `sort_keys=True`, `separators=(",",":")`, `ensure_ascii=False`, Decimals as `format(v,"f")`). Environment lineage is **excluded** from package/evaluation/deployment preimages.

| Atom | Literal |
|---|---|
| `FB_SHA_A` | `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` |
| `FB_SHA_B` | `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` |
| `FB_SHA_C` | `cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` |
| `FB_SHA_D` | `dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd` |
| `FB_SHA_E` | `eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee` |
| `FB_TIME` | `2026-09-12T00:00:00+00:00` |
| `FB_STEP_MS` | `900000` (15m; `INTERVAL_MS["15m"]`) |
| `FB_FEB1_MS` | `1769904000000` (independently: 2026-02-01T00:00:00Z = 1769904000 s) |
| `FB_JAN_LAST_MS` | `1769903100000` (`FB_FEB1_MS - FB_STEP_MS` = 2026-01-31T23:45:00Z) |

**PKG-PREIMAGE-1** (named parts of `compute_package_hash`; exact UTF-8 bytes):

```
{"exact_params_json":{"n":1},"instrument_metadata_json":{"symbol":"BTC"},"kernel_code_sha":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","modules_enabled_json":["mod"],"spec_json":{"k":"v"},"substitute_catalogue_versions_json":{"cat":"1"}}
```

`FB_PKG = 9c7adc2a9f34aaaf46b264d13b2f9dbf47c869f67ab8842c448c16526f26d4dc` (Lead stdlib SHA256 of PKG-PREIMAGE-1; derivation executed).

**EVAL-PREIMAGE-1** (valid quoted JSON; six named members of `compute_evaluation_run_hash`; `package_hash` is the evaluated PKG digest):

```
{"cost_model_json":{},"dataset_manifest_sha":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","evaluation_config_json":{},"package_hash":"9c7adc2a9f34aaaf46b264d13b2f9dbf47c869f67ab8842c448c16526f26d4dc","simulator_class":"CANONICAL","simulator_version":"1"}
```

`FB_EVAL = a06ff5247611889ede3aa8eae67a9d8f32a37cc18f17708d154cbb949c7b1662` (Lead stdlib SHA256 of EVAL-PREIMAGE-1; derivation executed).

**FAM-PREIMAGE-1**:

```
{"parameter_neighbourhood":{"approved_search_space":"FB022-SPACE-1"},"producer":"FB022-PROD","source_provenance":{"src":"FB022","strategy":"FB-STG-A"}}
```

`FB_FAM = FAM-e1b5a524cd606fad` (Lead stdlib; first 16 hex of SHA256(FAM-PREIMAGE-1); derivation executed). Current `compute_family_id` always returns `FAM-<hex>`, never `UNKNOWN`. Decision 98 refuses parameter buckets; this preimage is a space+strategy object, not a bin tuple. Binding that object into the three hashed members is a future P0-04 contract, not minted here.

`trial_id` composition already in source: `make_trial_id(evaluation_run_hash, param_hash, sequence)` → `{eval}.{param}.{sequence}` with `sequence >= 0`.

---

## P013 — catalog writer/reader fixtures

Existing executed component (not these cases): `qa/P013_existing_reader.log` — 3 tests pass on the unmerged reader; no writer, no commit-admission verifier, no independently validated covered-commit set (`LEAD_DECISIONS`). `param_hash` and `preregistered_space_hash` preimages remain P0-04-owned and **unset**; fixtures below use `FB_SHA_*` as stand-ins and must not be treated as those recipes.

| ID | Literal input | Expected semantic result | Independent derivation | Failure mutation | Proposed path | Status |
|---|---|---|---|---|---|---|
| FB013-01 identity | Package members = PKG-PREIMAGE-1. Evaluation members = EVAL-PREIMAGE-1 (valid quoted JSON with `package_hash` = `9c7adc2a9f34aaaf46b264d13b2f9dbf47c869f67ab8842c448c16526f26d4dc`). Lineage `{"python_version":"3.12.12","dependency_lockfile_hash":FB_SHA_C,"os_name":"Windows","os_version":"11","golden_suite_hash":FB_SHA_D,"golden_suite_bit_identical":false}` passed as call context. | `package_hash=9c7adc2a9f34aaaf46b264d13b2f9dbf47c869f67ab8842c448c16526f26d4dc`, `evaluation_run_hash=a06ff5247611889ede3aa8eae67a9d8f32a37cc18f17708d154cbb949c7b1662`. Same hashes if JSON keys are reordered before `canonical_json`. Lineage change must **not** change either hash. | Lead stdlib SHA256 of the exact preimage bytes in `qa/FIXTURE_EXPECTED_VALUES.json` (derivation executed). Source `identity.py` hashes named parts via sorted compact JSON and excludes lineage. Six evaluation members are exactly `package_hash, dataset_manifest_sha, cost_model_json, simulator_class, simulator_version, evaluation_config_json`. | Reorder keys only → still match. Changing `n:1`→`n:2` changes **package** identity (exact_params are in PKG-PREIMAGE-1); that is not two trials of one package (see FB013-04). | `MTC_COMMAND_CENTER/contracts/tests/test_identity.py` and `MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_preimages.py` (map S4) | PROPOSED_NOT_EXECUTED |
| FB013-02 field tamper | Committed receipt parses EVAL-PREIMAGE-1 and stores `catalog_commit_hash` claimed as SHA256 of the closed commit preimage that includes those six members (plus inherited `contract_version:"0.1.0"`). After commit, rewrite only `dataset_manifest_sha` to `FB_SHA_C`; leave stored hashes untouched. | Reader parses typed model **before** digest; recomputes evaluation hash from stored six members; **REFUSE** `COMMIT_HASH_MISMATCH` (or equivalent named mismatch). Rows are not query-visible. | Source: omission of a required envelope member is a parse failure (`extra="forbid"`; required members have no default). A changed byte that still parses must fail the recompute comparison. Inherited `contract_version` default `"0.1.0"` is **filled, not refused** if omitted — this case therefore tampers a **required six-member field**, not `contract_version`. | Tamper `simulator_version` `"1"`→`"2"` must also mismatch. Rehashing the tampered receipt and overwriting the stored hash (making it self-consistent) is **not** this case; that is silent self-consistency and must still fail an independent expected-preimage comparer. | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/tests/test_acceptance_reader.py` (map S6) | PROPOSED_NOT_EXECUTED |
| FB013-03 receipt substitution | Part path `lineage=CANONICAL/run_id=FB-RUN/strategy=FB-STG-A/symbol=BTC/timeframe=15m/part-{FB_SHA_A}-00000.parquet` containing one well-typed row. Receipt file `commits/{FB_SHA_B}.json` is a fully valid receipt for a **different** preimage (EVAL members with `dataset_manifest_sha=FB_SHA_C`). Publisher injects covered hash `FB_SHA_B`. | Publication/read **REFUSE**: covered-commit set does not match the part filename hash, or path/receipt cell mismatch. Substituting a well-formed foreign receipt must not admit the part. | Reader `trial_catalog.py` only loads parts whose filename commit hex is in `covered_commit_hashes`. Filename hash and receipt identity are different channels; a valid receipt for other bytes is not coverage of this part. | Swap only the receipt `catalog_commit_hash` string to `FB_SHA_A` while preimage members still hash to `FB_SHA_B` → still REFUSE (hash/preimage disagree). | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/tests/test_writer_commit.py` and `.../test_acceptance_reader.py` (map S6) | PROPOSED_NOT_EXECUTED |
| FB013-04 two trials same package | One completed run: `package_hash=FB_PKG`, `evaluation_run_hash=FB_EVAL`, `family_size=2`. **Same** `parameters={"n":1}` and **same** `param_hash=FB_SHA_C` on both trials (`package_hash` already binds exact_params; do **not** use `n:1` vs `n:2`). Trial0: `sequence=0`, `trial_id="{FB_EVAL}.{FB_SHA_C}.0"`. Trial1: `sequence=1`, `trial_id="{FB_EVAL}.{FB_SHA_C}.1"`. Same `candidate_id`, strategy/symbol/timeframe cell. | Both rows conserved. **Two distinct artifact paths succeed:** `artifacts/{FB_PKG}/{FB_EVAL}.{FB_SHA_C}.0/` and `artifacts/{FB_PKG}/{FB_EVAL}.{FB_SHA_C}.1/`. Distinct `trial_id`s. Same `package_hash` and `evaluation_run_hash`. Refuse **only** a conflicting rewrite of the **same** `trial_id`. Do not assert that `n:1`/`n:2` packages remain identical. | Source `make_trial_id` binds eval+param+sequence, so sequence 0 vs 1 yields two ids under one param hash. Map S6 pass: two trials same `package_hash` → distinct artifact dirs; conflicting same `trial_id` refuses. Exact_params live in PKG-PREIMAGE-1, so different `n` would be a different package. | Second write of **same** `trial_id` with different payload → REFUSE. Second distinct `trial_id` succeeding is the pass arm, not a mutation. | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/tests/test_conservation.py` (map S6) | PROPOSED_NOT_EXECUTED |
| FB013-05 publish-before-complete | Same two-trial run as FB013-04 (same parameters/`param_hash`, sequence 0 and 1) except trial1 (`sequence=1`) is absent (`family_size` still 2) **or** `has_full_artifacts=false` for a selected row, and publisher is invoked anyway. | **REFUSE publication**. No `trial_catalog` view, no covered-commit injection. Incomplete conservation cannot become query-visible. Distinct artifact dirs for sequence 0/1 are not created as a published view. | Design: no part is query-visible until conservation and identity checks pass; writer has no complete receipt while required identities/rows are missing. Existing `trial_catalog.py` is read-only and cannot be used as a passing publisher. | After both sequence-0 and sequence-1 trials are present (FB013-04) and conservation passes, the same publisher call is the distinct success arm — not claimed executed here. | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/tests/test_writer_commit.py` (map S6) | PROPOSED_NOT_EXECUTED |

**Tie semantics (not a sixth case; do not implement a ranking).** Owner addendum 32: after safety/quality checks, keep the best 20 **per strategy TYPE**, and keep every candidate tied at the cut-off. The robustness comparison formula, TYPE taxonomy, and policy version are **unset** (P013 B-07 engineering / P0-04). Required semantics when unknown: **do not drop a tied 21st by rounding, truncation, or arbitrary order**. A fixture that ranks `{score:1.0}×21` and keeps 20 is wrong. A fixture that keeps all 21 because they tie is the only currently named keep-rule; the score itself is not supplied here.

---

## P021 — eligibility / data-quality fixtures

Existing executed component: `qa/P021_existing_check.log` — 7 checks all `REFUSED`, 12 closed provisional fields, 4 open numerical fields, `ready=false`, two modified-copy detections. Fresh 17-series scan `qa/P021_FRESH_DATA_VERIFICATION.json` is historical-CSV integrity, not Hyperliquid evidence and not a gap-limit ratification. Source `create_optimization_data_bundle.py` still lacks `5m` in `TIMEFRAME_SECONDS` and uses `int(delta/expected_step)-1` (truncates). Catalogue source field `check_set_version` is integer `2`; the **adapter uses string `"2"`**. Int/string diagnostic alone is **not** a mismatch. `check_set_identity` is `null`; `POLICY_SET.policy_version` is `"v1"` provisional.

**Detection-gate conflict (state, do not pick a production value):** engineering M1 prose says gap iff `Δ_j > 1.5 s`; the cited tool at `:318` uses `delta > expected_step * 1.5`. Fixture publishes measurements under **both** gates. No `gap_ratio_max` is minted.

Hand series **FB021-GAP** (UTC seconds, `s=900`, 15m, strictly increasing):

`t = [0, 900, 2700, 3600]`<br>
`Δ = [900, 1800, 900]`<br>
`m = 4`<br>
`t_last - t_first = 3600`<br>
`expected_bars = round(3600/900)+1 = 5`<br>
Missing interior slot at `1800` only (leading/trailing absence is not a gap).

| Method | Gate `Δ > 1.5s` (literal prose) | Gate `Δ > 1.5·s` = 1350 (tool `:318`) |
|---|---|---|
| M1 `count(Δ_j > gate)/(m-1)` | `3/3 = 1` | `1/3` |
| M2 `Σ max(0,round(Δ_j/s)-1) / expected_bars` | `1/5` | `1/5` |
| M3 `Σ(Δ_j − s)/(t_last−t_first)` | `900/3600 = 1/4` | `1/4` |

Tool truncation `int(1800/900)-1 = 1` agrees here; a 1.9-step hole would disagree (`int`→0, `round`→1). That disagreement is **not** this case.

| ID | Literal input | Expected semantic result | Independent derivation | Failure mutation | Proposed path | Status |
|---|---|---|---|---|---|---|
| FB021-01 M1/M2/M3 | Series FB021-GAP; timeframe `"15m"`; no `gap_ratio_max` supplied (`null`). | Emit M1/M2/M3 exactly as the table (both gates labelled). **Do not PASS/FAIL against a limit.** Measured members may be recorded; overall DATA_QUALITY remains `BLOCKED`/`REFUSED` while B-02/B-17 open. M2 is the only method the engineering draft compares to a future max; this bank still does not apply a max. | Formulas from newest engineering §d.2–d.4; hand arithmetic above; source tool gate vs prose gate recorded, not silently unified. 24/7 calendar for BTC perpetual (decision 89) makes these four timestamps legal interior slots. Mutation arithmetic in `qa/FIXTURE_EXPECTED_VALUES.json` `gap_mutant` (derivation executed). | Drop `2700` leaving `[0, 900, 3600]` (`m=3`, two intervals `Δ=[900, 2700]`). Missing slots `1800` and `2700` (`expected_bars` still 5). **M1 at 1.5·step = 1/2** (only the 2700 delta exceeds 1350; `1/(3-1)`). **M2 = 2/5**. **M3 = 1/2**. The old draft M1=`1/3` is wrong (that used the original four-point denominator). If the checker still reports the original 1-missing triple or M1=`1/3`, DETECTED. | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_data_gap_ratio.py` (map S1) | PROPOSED_NOT_EXECUTED |
| FB021-02 lookahead | Bars `(t,o,h,l,c,v)`: `(0,10,11,9,10,1)`, `(900,10,12,9,11,1)`, `(1800,11,99,10,99,1)`. Decision time `t=900`. **Fixture intent rule (deterministic, not a production policy):** lookahead `LONG` iff **next** close `> 50` else `FLAT`; causal `LONG` iff **latest closed** close `> 50` else `FLAT`. Absent next bar ⇒ next close is not `> 50` ⇒ `FLAT`. Prefix producer physically deletes the `t=1800` row. | **Lookahead mismatch** compares the **same** lookahead series: full lookahead `LONG` vs prefix lookahead `FLAT`. **Causal control** compares full causal `FLAT` vs prefix causal `FLAT` (equal). Do **not** define mismatch as lookahead vs causal. Catalogue `intent_mismatch_count_max=0` is a **count**, not a PASS: B-12/B-21 remain open, so `FAIL` on lookahead full-vs-prefix mismatch **or** `BLOCKED` if the domain/hash contract is missing — **never PASS from an empty prefix**. Zero-decision outcome is **UNKNOWN** (B-12). | The LONG/FLAT tokens follow the stated fixture rule from the literal closes; no imported kernel expected result. Catalogue question: lookahead decision must change when later bars are physically removed; causal must not. Intent-hash bytes remain undefined (B-21); compare the tokens, not a minted hash recipe. | Restore the `t=1800` bar to the prefix producer (lookahead hidden) → full and prefix lookahead both `LONG`; that mutant must be DETECTED by keeping truncation independent. | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p021_eligibility.py` (map S8b, not S8, not S1) | PROPOSED_NOT_EXECUTED |
| FB021-03 policy version mismatch | Adapter `check_set_version="1"` (string) against required adapter value `"2"`. Source catalogue integer `2` **maps to string `"2"`**; that mapping is **not** a mismatch. Also bind `allocation_policy_version="allocation-v1"` and readiness `POLICY_SET.policy_version="v1"` as **separate** fields. | **REFUSE / BLOCKED** because `"1" ≠ "2"`, and because allocation/guardian/readiness are different domains (Lead). A matching string `"v1"` on allocation does **not** satisfy readiness. Do **not** refuse solely because source stored an int `2` and the adapter carries string `"2"`. | Source catalogue returns integer `2`; map: no owner action to map `check_set_version` int 2; adapter uses string `"2"`. `compute_deployment_identity_hash` hashes `allocation_policy_version` separately from eligibility `check_set_version`. | Set adapter `check_set_version="2"` **and** treat allocation `"v1"` as the readiness version → still REFUSE the cross-domain alias. Inventing a fail from int-vs-string of the same `2` is itself a defect. | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p021_eligibility.py` (map S8b, not S8, not S1) | PROPOSED_NOT_EXECUTED |
| FB021-04 null policy refusal | Same verdict-set shape with adapter `check_set_version=null` **or** `POLICY_SET.policy_version=null` **or** `check_set_identity=null` presented as sufficient for PASS. | **REFUSE / BLOCKED**, `ready=false`. Null/unset is fail-closed, never PASS. Existing catalogue already has `check_set_identity: null` and `ready: false` with all seven checks `REFUSED` — cited as component evidence that null identity does not currently yield ready. | Contracts README: unset numeric policy is `[OPEN]`/`None` and fail-closed. `EligibilityCheckResult` requires `blocked_reason` when outcome is BLOCKED. Catalogue `readiness_record()` hard-sets every check `REFUSED` while missing rules/numbers remain. | Fill only adapter `check_set_version="2"` and leave gap/divergence numbers null → still REFUSE (four open numbers). That is FB021-05’s surface, not a PASS arm. | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p021_eligibility.py` (map S8b, not S8, not S1) | PROPOSED_NOT_EXECUTED |
| FB021-05 unset gap limit | FB021-GAP measurements from FB021-01 plus `gap_ratio_max=null` (open number B-02). Duplicate/out-of-order/invalid OHLCV counts all 0. | DATA_QUALITY `BLOCKED`/`REFUSED` because the max is unset. **Not PASS** (clean bars do not close an open limit). **Not FAIL** (no ratified max was breached). `BLOCKED ≠ FAIL ≠ PASS`. | Catalogue wires `missing_numbers=("gap_ratio_max",)` on `P021.DATA_QUALITY`. Invariant: unset threshold yields BLOCKED, never PASS. | Inject a fixture-only max `FB_GAP_MAX=0.10` **as a local test constant** and then FAIL M2=`1/5` against it would mint a policy if labelled production — **forbidden**. The mutation for this case is removing the null-refusal so a null max yields PASS: DETECTED. | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_data_gap_ratio.py` (map S1) | PROPOSED_NOT_EXECUTED |

Lead reminder used: `day_forward_period=21` days is the applied minimum in the catalogue; the profile’s 4-week median wait is a **different labelled metric**. This bank does not rewrite 21→28 and does not use those production numbers as fixture expected results.

---

## P022 — family / untouched-window fixtures

Newest completeness rule (draft v1.3+ and later folds): one uncovered sub-interval makes the **whole** `W_B` incomplete; `untouched(B)=∅`; confirmation duration 0. Non-empty untouched requires independent access enumeration **and** exact-head anchor bound to `coverage_key(B)=(package_hash, family_id, D, E)`. Hash chain alone cannot detect rehashed truncation (Lead).

Half-open intervals. Length of `[a,b)` is `b-a`.

| ID | Literal input | Expected semantic result | Independent derivation | Failure mutation | Proposed path | Status |
|---|---|---|---|---|---|---|
| FB022-01 complete 70 | `W_B=[0,100)`. Observed union `observed(B)=[10,40)`. Independent coverage: attestation rows covering `[0,10)`, `[10,40)`, `[40,100)` under `coverage_key=(FB_PKG, FB_FAM, D=FB_SHA_A, E=FORWARD_SHADOW)`. Exact-head anchor equals ledger head. No sibling observation. `family_id=FB_FAM` ≠ `FAM-UNKNOWN`. | `untouched(B)=[0,10)∪[40,100)`; duration `10+60=70`. Confirmation evidence may cite only events entirely inside that set. Planted stored field `untouched=70` is **inert** (recompute ignores it). | Interval difference: `[0,100)\[10,40)` = 70. Completeness is whole-window, identity-bound, and requires both coverage and anchor (Lead + newest §3.3). | Delete the `[40,100)` attestation only → whole window incomplete, duration **0** (not 10). That mutant is FB022-02’s class; here it proves 70 depends on full coverage. | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_untouched_window.py` (map S2) | PROPOSED_NOT_EXECUTED |
| FB022-02 absent coverage 0 | Same `W_B` and same observed union `[10,40)`, **no** coverage rows and **no** head anchor (or wrong `coverage_key` package). | `untouched(B)=∅`; duration `0`. Must **not** report 70. Ledger absent/incomplete ⇒ zero confirmation evidence. | Fail-closed whole-window rule; A-7d / brief rule 8. Coverage that names a different package/family/`D`/`E` does not cover `W_B`. | Add valid coverage+anchor over **all** of `W_B` (the FB022-01 input) as the only mutation that may restore 70. Partial fill of the hole must still yield 0. | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_untouched_window.py` (map S2) | PROPOSED_NOT_EXECUTED |
| FB022-03 family vs strategy | Two completed trials, identical `preregistered_space_hash=FB_SHA_E`, different strategy ids `FB-STG-A` vs `FB-STG-B`. Resolver inputs otherwise equal. | **Two families**, not one. Disagreement across explicit strategy identity vs derived triple → **REFUSE** silent merge; do not emit a single `FB_FAM` for both. `FAM-UNKNOWN` is allowed only as a named refuse-to-unknown, and `FAM-UNKNOWN` ⇒ `untouched=∅` / blocks `LIVE_CANDIDATE`. Current `compute_family_id` will happily hash different `source_provenance.strategy` into different `FAM-*`; the defect is an adapter that **drops** strategy. | Decision 98: one approved search-space version **for one strategy** is one family. Lead: future adapter binds one space version and one strategy; no silent rewrite of historical family IDs. Map S2: missing strategy refuses; freeze vs catalog conflict → `FAM-UNKNOWN`. | Drop `strategy` from the hashed triple so both trials share `FB_FAM` → DETECTED. | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_family_resolver.py` (map S2) | PROPOSED_NOT_EXECUTED |
| FB022-04 family vs search-space | Two trials, same strategy `FB-STG-A`, different space identities `FB022-SPACE-1` vs `FB022-SPACE-2` (`preregistered_space_hash` `FB_SHA_E` vs `FB_SHA_D`). | **Two families**. Do not bucket parameters; do not merge because `parameters.n` is adjacent. Exact neighbourhood bytes differ ⇒ different `compute_family_id`. | Same decision 98 / Lead. Source hashes `parameter_neighbourhood` exactly (`test_identity.py` uses `{"period":[18,22]}` as an object, not a bin rule). Map S2: missing search-space version refuses. | Replace both neighbourhoods with a bin tuple `{"n_bin":1}` so distinct spaces collide → DETECTED (bucket invention). | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_family_resolver.py` (map S2) | PROPOSED_NOT_EXECUTED |
| FB022-05 rehashed truncation | Ledger rows R0,R1,R2 with `writer_seq` 0,1,2. Each `row_hash = SHA256(canonical bytes of every declared field except row_hash, including prev_hash)`. Independently recorded head anchor = R2 hash; independent enumeration count = 3. Then **delete R2** and recompute R0–R1 so the remaining chain verifies. | Chain-only verifier would see a consistent shorter chain. Required result: **INCOMPLETE**. Enumeration count 2≠3 and/or head ≠ frozen anchor. `untouched=∅`. | Lead: hash chain cannot detect rehashed truncation; independent access enumeration **and** exact-head anchor must bind the same package/deployment/environment/window. Canonical row_hash byte encoding remains `[OPEN]` (OQ-12); this case still holds with any stable encoding because both the truncated and original encodings are produced by the same function. | Recompute and **overwrite the anchor** to the new head so chain+anchor agree; enumeration must still DETECT count mismatch. If enumeration is also rewritten, that is no longer an independent producer. | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_observation_ledger.py` (map S7) | PROPOSED_NOT_EXECUTED |

`row_hash` canonical bytes are **not minted**. Until OQ-12 closes, implementations must pin one encoding in the test module and use it for both producers; this bank does not choose it.

---

## P030 — collector fixtures

Existing executed components: `qa/P030_existing_check.log` (offline checker PASS, 0 network attempts, forming-bar/gap/mutant fences); `qa/P030_independent_probe.json` (archive identical replay `IDENTICAL_REPLAY_NOOP`; identical `WS_LIVE` ingest `REFUSED: bar sequence is non-increasing or off interval`; persisted rows 1; gap 2 missing bars). Those prove **current** entry points; they are not this bank’s expected-result import.

Universe: symbol `BTC`, interval `15m` only. `HashContract` serialization `json-array-compact` over declared fields.

**FB030-BAR(t)** payload (closed iff `ingest_time >= t + 900000`):

`{"t":t,"T":t+900000,"s":"BTC","i":"15m","o":"100","h":"102","l":"99","c":"101","v":"10"}`

| ID | Literal input | Expected semantic result | Independent derivation | Failure mutation | Proposed path | Status |
|---|---|---|---|---|---|---|
| FB030-01 ingest vs archive dup | Clock `ingest_time=FB_JAN_LAST_MS+5*FB_STEP_MS`. First `ingest(FB030-BAR(FB_JAN_LAST_MS),"WS_LIVE")` appends. Then (a) `archive.append_bar` of that **same** `MarketBar`; (b) second `ingest` of the same raw bar as `WS_LIVE`. | **CURRENT characterization (executed component evidence, not this fixture):** (a) `IDENTICAL_REPLAY_NOOP`, 1 row; (b) ingest **REFUSE** `bar sequence is non-increasing or off interval`, still 1 row (`qa/P030_independent_probe.json`). “Replay works” must name the entry point. **PROPOSED-FIX acceptance (S0 T7; still PROPOSED_NOT_EXECUTED):** identical `WS_LIVE` second ingest → `IDENTICAL_REPLAY_NOOP`, still 1 row. Readonly duplicate lookup **before** any write or `detect_gap`. No append-before-gap shortcut. A missing-gap or other refusal **must not write the incoming bar**. Same-id different-bytes still refuses. **Successful desired fix is not a regression.** | Archive no-ops on same `observation_id` **and** same `producer_payload_hash`. Current `ingest` calls `detect_gap(previous, next)` first and refuses `distance <= 0` on duplicates. Map S0: `ingest` consults archive dedupe **before** `detect_gap`. | **Proposed failure mutation:** restore old detect_gap-first rejection so identical ingest still REFUSE. Treating S0 NOOP as a regression is itself wrong. Append incoming bar then refuse gap → DETECTED (bar must not be written). | `check_market_data_collector.py` T7 arm (map S0; do not split writers) | PROPOSED_NOT_EXECUTED |
| FB030-02 gap + month boundary | `ingest(FB030-BAR(FB_JAN_LAST_MS),"WS_LIVE")` then `ingest(FB030-BAR(FB_JAN_LAST_MS+3*FB_STEP_MS),"WS_LIVE")` with snapshot source holding the two interior bars at **`+1*FB_STEP_MS` and `+2*FB_STEP_MS`** (February; not +1s/+2s). | Gap `window_start=FB_FEB1_MS`, `window_end=FB_JAN_LAST_MS+3*FB_STEP_MS`, `missing_bars=2`. Fill via `CANDLE_SNAPSHOT`. Durable files: `bars/HYPERLIQUID/BTC/15m/2026-01.jsonl` **and** `2026-02.jsonl`. Four closed bars stored. If snapshot cannot fill, **do not write the incoming live bar**. | `detect_gap`: `distance=3*step`, `missing=2`, window `[prev+step, next)`. `_month` uses UTC. 23:45Z January vs 00:00Z February is a calendar month roll, not an interval fault. Probe used `previous=0,next=2700000` → missing 2; same arithmetic, different epoch. | Snapshot omits the February bar → REFUSE “snapshot left N bar(s) missing” and incoming `+3*step` bar is **not** persisted. Writing both months into `2026-01.jsonl` → DETECTED. | `check_market_data_collector.py` (map S0) | PROPOSED_NOT_EXECUTED |
| FB030-03 forming bar | Clock `now=FB_JAN_LAST_MS+5*FB_STEP_MS`. Ingest `FB030-BAR(FB_JAN_LAST_MS+5*FB_STEP_MS)` (`close_time=now+900000 > now`). | `normalize_bar` returns `None`; `ingest` returns `None`; **zero** new archive rows. Forming bars are not persisted. | Source: `if close_time > ingest_time: return None` before identity/archive. | Persist anyway after `None` (the existing “forming bar written” mutant class) → DETECTED. Component evidence: carried forming-bar fence in `qa/P030_existing_check.log`. | `check_market_data_collector.py` (map S0) | PROPOSED_NOT_EXECUTED |
| FB030-04 identity collision | Two `MarketBar` values, **forced** `observation_id=FB_SHA_E`, `producer_payload_hash` `FB_SHA_A` vs `FB_SHA_B`, same `source_producer="WS_LIVE"`, `symbol="BTC"`, `interval="15m"`, `bar_open_time=FB_JAN_LAST_MS`. Direct `append_bar` of both. | First `APPENDED`. Second **REFUSE** `same observation_id has different producer bytes`. | Archive equality is `observation_id` then payload hash. Distinct payload under one id is a collision, not a replay. (Current observation contract includes `producer_payload_hash`, so `normalize_bar` would not naturally collide; this case is the archive predicate, not a request to drop fields.) | Same id **and** same payload hash → `IDENTICAL_REPLAY_NOOP` (FB030-01 archive/proposed ingest). Same slot different id without correction contract → the separate “differing same-producer bar” refusal; not this case. | `check_market_data_collector.py` (map S0) | PROPOSED_NOT_EXECUTED |
| FB030-05 process alive / feed stale | Injected **fixture-only** bounds `FB_PROCESS_SILENCE_S=120`, `FB_FEED_STALE_S=600` (not OPEN-F1/F2, not production). Heartbeat payload `emitted_at=2026-09-12T00:00:00Z`, `now=2026-09-12T00:01:00Z` (age 60s ≤ 120). Last **closed** bar open `FB_JAN_LAST_MS`, `now_ms=FB_JAN_LAST_MS+10*FB_STEP_MS` (age 9000s > 600). Reconciliation cursor stale or idle. | Process heartbeat **alive**. Market feed **stale**. Collector health **not** healthy. Fresh process beat alone cannot mark market data healthy (Lead). | Three clocks: process payload UTC, last closed bar, reconciliation high-water. Watchdog `classify` uses payload `emitted_at`, never mtime. Forming/open bar is not “latest closed”. | Health aggregator ORs process-ok into feed-ok → DETECTED. | `check_p030_opsa_heartbeat_adapter.py` (map S9; does not edit P026) | PROPOSED_NOT_EXECUTED |

---

## P026 — watchdog / backup interface fixtures

P026 implementation is **not** in this campaign (Lead). P026 files stay unchanged; **no new tests under `MTC_COMMAND_CENTER/tools/opsa/`**. Existing executed component: `qa/P026_existing_interfaces.log` — 33 local tests OK, including tampered-backup restore failure and stale heartbeat → `silent`. These cases are consumed by **future P030 adapter checkers** (map S9/S10) of unchanged P026 payload/exit-code contracts.

Silence bound is **always injected** (`silence_seconds=FB_SILENCE_S`). Do not treat `FUTURE_TOLERANCE_SECONDS=60.0` or CLI help `900` as production policy.

`FB_SILENCE_S=120`<br>
`FB_NOW=2026-09-12T00:02:00Z`

Heartbeat file `fb026-collector.hb.json` schema `mtc.opsa_heartbeat/v1`.

| ID | Literal input | Expected semantic result | Independent derivation | Failure mutation | Proposed path | Status |
|---|---|---|---|---|---|---|
| FB026-01 injected bound OK | Bound `120`. Payload `emitted_at=2026-09-12T00:01:00Z` (age 60s). `--now=FB_NOW`. | State `ok`; overall `ok` if this is the only id. Age computed from payload, not mtime. | `watchdog.classify`: `age=(now-emitted_at).total_seconds()`; `ok` iff not future-skewed and `age <= silence_seconds`. | Touch file mtime to `FB_NOW` while leaving `emitted_at` at `2026-09-12T00:00:00Z` (age 120s **equal** bound remains ok; age 121s with fresh mtime must still be `silent` — FB026-02). | `check_p030_opsa_heartbeat_adapter.py` (map S9; P026 `watchdog.py` unchanged) | PROPOSED_NOT_EXECUTED |
| FB026-02 injected bound silent | Bound `120`. Payload `emitted_at=2026-09-12T00:00:00Z` (age 120s is `<=`; use `2026-09-11T23:59:59Z` so age `121`). `--now=FB_NOW`. | State `silent`; overall `alert`; exit 2. Not `ok`, not `missing`, not `unreadable`. | Strict `age > silence_seconds` in source. Equality at 120s is `ok`; 121s is `silent`. No policy default is consulted. | Classify 121s as `ok` because a module default 900s is used instead of the injected 120 → DETECTED. | `check_p030_opsa_heartbeat_adapter.py` (map S9; P026 unchanged) | PROPOSED_NOT_EXECUTED |
| FB026-03 backup tamper | Backup run copies `ledger.jsonl` bytes `{"row":1}\n` (`backup_literal_utf8`; SHA256 `c805f1e47450a7698e2e0b9f59b08d1f8945598a99ef24b5f25dbe046567307f`, Lead stdlib, derivation executed). After backup, flip one byte in the **backup copy**. Restore to a fresh target. | Restore **FAIL** (rc 1 class in existing tool). Target file must not be installed. Per-file hash mismatch is DETECTED. | Existing `test_restore_refuses_tampered_backup` is component evidence of the copier/verifier. Adapter must not treat a mismatched copy as a consistent snapshot. | Restore succeeding on the flipped byte → DETECTED. | `check_p030_closed_partition_backup_adapter.py` (map S10; P026 `backup.py`/`restore.py` unchanged) | PROPOSED_NOT_EXECUTED |
| FB026-04 concurrent append ≠ snapshot | Live archive `2026-02.jsonl` has 1 row. Backup starts hashing that file. During copy, a second bar is appended (size/hash change mid-walk). Copier still emits per-file `readback=match` for whatever bytes it copied. | Adapter **must not claim** “consistent live snapshot”. Required result: `SNAPSHOT_INCONSISTENT` / refuse snapshot identity, unless the recipe is **frozen closed partitions** or a **stable snapshot + committed high-water mark** taken before copy. Per-file hashes alone are insufficient (Lead). | Backup tool walks and hashes files; it has no collector HWM and no freeze. Append-only jsonl can change between walk and copy. P030 must supply the snapshot/partition recipe; P026 copier stays unchanged. | Label the run `snapshot_ok=true` solely because `readback=match` → DETECTED. | `check_p030_closed_partition_backup_adapter.py` (map S10; P026 unchanged) | PROPOSED_NOT_EXECUTED |

P026 does not install a watchdog, deliver phone alerts, or prove recoverability of a deployed collector. Exit codes remain 0 ok / 2 alert / 3 check-failed as in `watchdog.py`.

---

## Explicit non-claims

- No Gate 5 / acceptance verdict.
- No new product, schema, or operational authority.
- No production `gap_ratio_max`, silence bound, freshness offset, or family-bin rule.
- Dataset identities: original raw manifest digest, selected-dataset manifest digest, and any P021 ds-v1 recipe stay **three named fields**; this bank never assigns `FB_PKG` or `FB_EVAL` to a dataset digest.
- P013 branch reader tests are not a covered-commit set and not a writer.
- `qa/P030_independent_probe.json` supports FB030-01’s **CURRENT** entry-point split only; it is not S0 T7 acceptance.
- `qa/FIXTURE_EXPECTED_VALUES.json` is executed stdlib hash/arithmetic derivation, not a fixture run.
- Future implementation still needs package-specific scope; nothing here is that scope.
