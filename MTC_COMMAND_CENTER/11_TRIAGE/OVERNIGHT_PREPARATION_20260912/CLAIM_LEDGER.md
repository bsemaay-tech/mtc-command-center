# Claim ledger — P013/P021/P022/P030 (nonbinding preparation)

Pin `42f99571e6abb5222744d9345e1c8a9e19c23c15`. Branch `3e704c2d` (foreign, unmerged).
Reports under `reports/` are drafts, not authority. Lead wording wins on conflict.
This file is a claim inventory, not implementation, schema, policy, or Gate5 authority.
New fixtures remain `PROPOSED_NOT_EXECUTED`. Existing `qa/` logs are Lead-executed component evidence only.
Provenance of the P021 catalogue (preserve current source values; **not** an owner-retrieval item): `inputs/OWNER_PROVISIONAL_POLICY_20260906.md` and commits `a63bd4b053648e4a7008e5f2fe5f999b94947650` then `380a26aacf960ee33fd610ec699dcc2180e4eb8a`. No new scope granted.

## Source coverage (exact)

| Tree | Pin | Files | Identity |
|---|---|---|---|
| `qa/source_lf/` | 42f9957 | **538** | exact Git blobs; `qa/EXACT_LF_SOURCE_VERIFICATION.json` `raw_blob_mismatches: []` |
| `inputs/source/` | same pin | **538** | `qa/SOURCE_IDENTITY_VERIFICATION.json`: **120 raw match / 418 CRLF-only**; CRLF ≠ raw identity |
| `inputs/additional_source/` | same pin, `git show` | **4** additional exact raw files | `qa/ADDITIONAL_SOURCE_VERIFICATION.json` |
| `inputs/P013_BRANCH/` + `qa/p013_lf/` | **3e704c2d** | `trial_catalog.py` + tests; `contracts/` copied from 42f9957 | reader/schema only |

**Four additional exact raw sources** (not in the 538-file archive; Lead-verified):

| Path | git_blob | sha256 |
|---|---|---|
| `IBKR_PAPER_BRIDGE/bridge/engine/types.py` | `3598f95f4c3829b85e096d4da09caee8c5e8539f` | `9c383d0930112ed5b243ba60d793b40af6f54e3ba5fd5f6de0dc685e5679445d` |
| `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/data/io.py` | `ff09fa52d3e17b436d6b2ed2520d1a42fa81476a` | `5183a91156500f4193bd0c14437e39f3097d07f852d5b880c149eb1a9a797555` |
| `.../src/data/cache.py` | `85fa97702649d442fcc600b64cbff333c2a17745` | `f83a82195a891f3f6fce26e3b70258397a231ac01efec4ade500ec1e890c03d4` |
| `.../src/data/download.py` | `eba9f25611824bcfc1c56c997241b0ca5cbbb5dd` | `9c243a60a5f4358f6e6065333c879286534ddb32bc8c5a1825cf638c5d5944d3` |

Tracked 538 + those 4: contracts, `p021_readiness_rules.py`, `create_optimization_data_bundle.py`, registry, collector/checker, `tools/opsa/*`, `mega_walk_forward.py`, `results.py:BacktestResult`, root `unsimulated_controls.py`, branch reader, Lead qa, profiles, `DurableRiskPolicy`, `validate_dataset`, `CacheManager`, `download_ohlcv`.
**Still outside this coverage:** live stores, phone delivery, deployed collector.

**Statuses:** `SOURCE_VERIFIED` · `BRANCH_ONLY` · `EXECUTED_COMPONENT_CHECK` · `PROPOSED_NOT_IMPLEMENTED` · `NOT_ESTABLISHED`.

## Overclaims (do not promote)

| Pattern | What is true | What is not true |
|---|---|---|
| Policy design = built | v2.1/v2.3/v1.12 text exists | classifier, `p021pol-v1`, M2 helper, ds-v1 bytes, eligibility module |
| Caller-supplied covered hashes = verified catalogue | reader checks path/schema/row of hashes the **caller already lists** | independent commit completeness / admission verifier |
| Heartbeat = market freshness | OPSA emit/watch of `emitted_at` | last closed bar, reconciliation, collector health |
| Log backup = live snapshot | per-file SHA-256 copy/read-back (33 local tests) | consistent live append-only snapshot, installed watchdog, phone |
| Family hash helper = family resolver | `compute_family_id` → `FAM-<16hex>` | conflict check, `FAM-UNKNOWN`, siblings, ledger, freeze store |
| Collector replay works | `MonthlyArchive.append_bar` → `IDENTICAL_REPLAY_NOOP` | `ingest` duplicate `WS_LIVE` refuses |
| Build-ready / local gates satisfied | candidate for a **future explicit bounded scope** | authorization in this window (Lead §§1,5) |
| 21 d vs 4 wk “resolved as rounding” | applied `day_forward_period=21`; profiles **median wait = 4 weeks** | one metric; preserve both labels (Lead §3) |
| `DurableRiskPolicy` / `validate_dataset` / cache / ccxt download = P021/P030 admission | files exist (4 extra sources) | import/alter Bridge; P030 admission validator; collector trust identity; Hyperliquid backend |

## Claims

| ID | Pkg | Precise claim | path:symbol | Status | Correction |
|---|---|---|---|---|---|
| CL001 | P013/P021/P022 | `canonical_json` + `_hash_named_parts` shipped | `identity.py:canonical_json` `:31-44` | SOURCE_VERIFIED | none |
| CL002 | P013/P021/P022 | Six-member evaluation hash; env excluded | `identity.py:compute_evaluation_run_hash` `:76-95` | SOURCE_VERIFIED | none |
| CL003 | P013/P022 | `compute_package_hash` six members; env excluded | `identity.py:compute_package_hash` `:54-73` | SOURCE_VERIFIED | recipe ≠ freeze store |
| CL004 | P013/P022 | `compute_family_id` always `FAM-<digest[:16]>` | `identity.py:compute_family_id` `:144-154` | SOURCE_VERIFIED | **not** a family resolver |
| CL005 | P013 | `make_candidate_id`/`make_trial_id`/`make_run_id` exist; **no** `compute_param_hash` / `compute_preregistered_space_hash` | `identity.py:47-154`; fields `trials.py:24,28` | SOURCE_VERIFIED | B-04/B-12 functions unbuilt |
| CL006 | P013 | `TrialRecord` 47 declared + inherited `contract_version` (48) | `trials.py:TrialRecord` `:14-74` | SOURCE_VERIFIED | none |
| CL007 | P013 | `ArtifactManifest` 10 fields; no `trial_id`/`param_hash` | `trials.py:ArtifactManifest` `:77-87` | SOURCE_VERIFIED | B-09/D-04 open |
| CL008 | P013 | `ContractModel` frozen `extra=forbid`; `CONTRACT_VERSION="0.1.0"` | `base.py:12,59-89` | SOURCE_VERIFIED | inherited 7th member ≠ writer |
| CL009 | P013/P022 | `EnvironmentLineage` / `UnsimulatedControl` / `EvidenceIdentity` / `Environment` enum | `lineage.py:10-40` | SOURCE_VERIFIED | none |
| CL010 | P013/P022 | `StrategyPackage` has `candidate_id`/`family_id`/`package_hash`; **no** strategy-name/timeframe | `package.py:27-45` | SOURCE_VERIFIED | B-15 cell not on package |
| CL011 | P013 | `unsimulated_controls.py` exists at **repo root** | `unsimulated_controls.py` | SOURCE_VERIFIED | report path `03_QUANTLENS/tools/unsimulated_controls.py` is **wrong** |
| CL012 | P013 | Named contract tests exist (not re-run here) | `test_trials_and_eligibility.py:27,58,89` | SOURCE_VERIFIED | not Lead-executed this window |
| CL013 | P013 | **No writer** on master or branch (named writer types 0 hits) | 42f9957 + `trial_catalog.py` docstring `:1-6` | SOURCE_VERIFIED | reader ≠ writer |
| CL014 | P013 | Branch PyArrow reader/schema + searches | `P013_BRANCH/.../trial_catalog.py:41,94,139,197,209,221` | BRANCH_ONLY + EXECUTED_COMPONENT_CHECK | 3 tests passed; unmerged |
| CL015 | P013 | `covered_commit_hashes` is **caller-supplied** | `read_catalog_view` `:139-159` | SOURCE_VERIFIED (branch) | not a verified catalogue |
| CL016 | P013 | No commit-admission verifier / independent covered-commit set | branch module + tests | SOURCE_VERIFIED absence | copy ≠ accept branch |
| CL017 | P013 | `mega_walk_forward.py` JSON/MD/checkpoint only, not Parquet writer | `mega_walk_forward.py` | SOURCE_VERIFIED | future caller, not writer |
| CL018 | P013 | “Build-ready now / no gate” | report §7 | PROPOSED_NOT_IMPLEMENTED | future bounded scope only |
| CL019 | P021 | 7 REFUSED checks, 12 closed / 4 open, `ready=false`, `check_set_version=2` (source value preserved) | `p021_readiness_rules.py:readiness_record` `:298-320` | SOURCE_VERIFIED + EXECUTED_COMPONENT_CHECK | not an evaluator; not an owner-retrieval item |
| CL020 | P021 | `validate_catalog` + two modified-copy detections | `:253-296`, `:340-377` | EXECUTED_COMPONENT_CHECK | self-check only |
| CL021 | P021 | `day_forward_period=21`; four opens unset | `CLOSED_NUMBERS` `:73-159`; `OPEN_NUMBERS` `:165-170` | SOURCE_VERIFIED | reporter numbers ≠ production limits |
| CL022 | P021 | 21 d applied minimum vs 4-week expected median wait | module `:103-110`; profiles median-wait rows | SOURCE_VERIFIED | preserve both labels; do not rewrite 21→28 |
| CL023 | P021 | Eligibility **shapes** exist; no module builds results for the 7 checks | `admission.py:28,49` | SOURCE_VERIFIED | shape ≠ eligibility service |
| CL024 | P021 | `dataset_hash` field exists; `ds-v1:` construction absent | `results.py:110`; `trials.py:81` | SOURCE_VERIFIED | third identity; never silent alias |
| CL025 | P021 | `DurableRiskPolicy` exists; `create` validates finite numerics and hashes canonical JSON with `float.hex`; prefix `rpol-v1` | `additional_source/.../types.py:DurableRiskPolicy` `:1327` | SOURCE_VERIFIED | **pattern only**; do not import/alter Bridge or force a P020 carrier |
| CL026 | P021 | B-22 taxonomy / `p021pol-v1` / classifier files | no those files in 538 | PROPOSED_NOT_IMPLEMENTED | design ≠ built |
| CL027 | P021 | Divergence / gap-M2 helpers unbuilt | no `data_gap_ratio.py` | PROPOSED_NOT_IMPLEMENTED | M2 uses `round`; producer uses `int` |
| CL028 | P021 | `TIMEFRAME_SECONDS` has **no `5m`**; unknown tf silent skip; `int()` truncation | `create_optimization_data_bundle.py:51,314-324,354` | SOURCE_VERIFIED | 5m is fresh-series cadence (CL032) |
| CL029 | P021 | `compute_deployment_identity_hash` hashes **12** named members, not 11 | `identity.py:116-129` | SOURCE_VERIFIED | count **12**; env still excluded |
| CL030 | P021 | “Build-ready now … decision 186” for three new files | report §5–§7 | PROPOSED_NOT_IMPLEMENTED | provenance known (header); still needs package-specific scope |
| CL031 | P021 | T-P021-01 / T-P021-02 / T-P021-03 short / T-P021-03 duplicate / T-P021-04 against **existing catalogue** | `qa/P021_LITERAL_FIXTURE_CHECK.json` Python 3.12.12 | EXECUTED_EXISTING_CATALOGUE_ONLY | T04 first error is `closed-number catalogue changed; missing=[]; extra=['gap_ratio_max']`, **not** the overlap branch. T-P021-05…09 / F-1…F-3 and bank 24 cases remain `PROPOSED_NOT_EXECUTED` |
| CL032 | P021 | Fresh 17 CSVs, **4,105,966** rows, hash/count match | `qa/P021_FRESH_DATA_VERIFICATION.json` | EXECUTED_COMPONENT_CHECK | Binance 5m only; not OHLCV/HL evidence |
| CL033 | P022 | Registry **63** STG001–063; **46** `heuristic_auto` / **17** `explicit_metadata`; **no** `strategy_family` | `STRATEGY_RESEARCH_REGISTRY.json` | SOURCE_VERIFIED | not `family_id` |
| CL034 | P022 | `LIVE_CANDIDATE` + `leakage_record_id`; no `FAM-UNKNOWN` binding | `admission.py:24,106`; `trials.py:22` | SOURCE_VERIFIED | OQ-5 unbuilt |
| CL035 | P022 | No observation **ledger** / appender / chain / `FAMILY_OBSERVED` / `siblings()` / `family_resolver.py` | 42f9957 tools | SOURCE_VERIFIED absence | identity components ≠ control service |
| CL036 | P022 | No `evidence_window_start` / `frozen_at` on contracts | contracts `*.py` | SOURCE_VERIFIED | none |
| CL037 | P022 | No **ledger-specific** `observation_id` implementation | ledger absent; `MarketBar.observation_id` `:91` | SOURCE_VERIFIED | cannot say “no `observation_id` anywhere” |
| CL038 | P022 | No DuckDB/Parquet catalogue **on master** | 42f9957 (0 `trial_catalog`) | SOURCE_VERIFIED | Parquet reader BRANCH_ONLY (CL014) |
| CL039 | P022 | Decision-98 adapter + R2/R3 files | report T14 / R2/R3 | PROPOSED_NOT_IMPLEMENTED | P022 correctly refuses build-ready-now |
| CL040 | P030 | Offline core + start refused rc2; checker NETWORK 0 | `market_data_collector.py`; `main` `:459-476` | SOURCE_VERIFIED + EXECUTED_COMPONENT_CHECK | not a runtime collector |
| CL041 | P030 | `INITIAL_SYMBOLS=("BTC",)` + 4 intervals; 17 unset numerics | `:23-52` | SOURCE_VERIFIED | none |
| CL042 | P030 | Archive identical replay NOOP; ingest duplicate REFUSED; rows=1 | `append_bar` `:308-314`; `ingest` `:354-374` | SOURCE_VERIFIED + EXECUTED_COMPONENT_CHECK | specify entry point |
| CL043 | P030 | Durable families `["bars"]` only; no live `HyperliquidPublicSource` import | `check_market_data_collector.py:197,513-539` | SOURCE_VERIFIED | no sidecar `events/`; no ratified backend |
| CL044 | P030 | OPSA local emit/watch/backup/restore **components** | `tools/opsa/{heartbeat,watchdog,backup,restore}.py` | SOURCE_VERIFIED + EXECUTED_COMPONENT_CHECK | 33 tests; not installed/phone/live-archive |
| CL045 | P030 | Collector emits no `.hb.json`; adapter unbuilt | collector vs `heartbeat.py:emit` | SOURCE_VERIFIED / PROPOSED_NOT_IMPLEMENTED | beat ≠ freshness ≠ reconciliation |
| CL046 | P030 | No reconciliation, 7-state freshness, reconnect, CORRECTION, provenance writer, N6 alarm | collector + opsa | SOURCE_VERIFIED absence | complete VEN-E service absent; core present (CL040) |
| CL047 | P030 | Per-file backup hashes = live snapshot / “local gates satisfied” | `backup.py` + report §7 | NOT_ESTABLISHED | closed partitions or snapshot+HWM; own future scope |
| CL048 | P030 | Proposed duplicate-ingest fix, T7–T8, U1–U6, S1–S8 | report §1A, §4–§6B | PROPOSED_NOT_IMPLEMENTED | future unit; not authorized now |
| CL049 | P030 | `validate_dataset`, `CacheManager`, `download_ohlcv` **exist** | additional `io.py:108`, `cache.py:23,263`, `download.py:97` | SOURCE_VERIFIED | **reuse limits:** `validate_dataset` is not P030 admission (dup timestamps permitted; volume/gaps warnings); cache key truncated MD5, no venue/provenance, `get_or_download` must not be invoked here; ccxt Binance `download_ohlcv` is proxy-research only, **not** Hyperliquid/admitted backend |
| CL050 | ALL | All **new** package fixtures in the four reports | reports §4 | PROPOSED_NOT_EXECUTED | executed = existing qa only |
| CL051 | P013 | No staged-selection policy / strategy-TYPE / policy-version member on `TrialRecord` | design `:574-576`; `trials.py` | SOURCE_VERIFIED absence | decision-128 binding unbuilt |
| CL052 | P013 | No `P020CanonicalPathReceiptVerifier` / canonical-receipt issuer | 0 hits in 538 | SOURCE_VERIFIED absence | B-01 half; waits P020 acceptance |
| CL053 | P013 | No committed-byte home for `cost_model_json` / `evaluation_config_json` | evaluation hash params only | SOURCE_VERIFIED absence | preimage types unbuilt (CL013) |
| CL054 | P021 | B-01 accepted corrected engine unmet; every rule lists it | `RULES` `missing_rules`; P012 NONACCEPTED | SOURCE_VERIFIED | synthetic-only milestone; not an evaluator |
| CL055 | P021 | B-08/B-19, B-12/B-21/B-16, B-09 remain open | catalogue `missing_rules` + design v2.1 open table | SOURCE_VERIFIED absence | not implemented |
| CL056 | P022 | `TAG_DICTIONARY.json` present adjacent to registry | `05_REGISTRY/TAG_DICTIONARY.json` | SOURCE_VERIFIED | not `family_id` |
| CL057 | P022 | `simulate_slice` exists; no prior-package/provenance/warm-start read hook | `mega_walk_forward.py:648,1310-1354` | SOURCE_VERIFIED | file ≠ OQ-3 hook |
| CL058 | P030 | 21-field persisted-record fence in existing checker | `check_market_data_collector.py:229-301` | EXECUTED_COMPONENT_CHECK | component fence, not live admission |
| CL059 | P030 | No executable P021 data-quality/replay/lookahead/repaint verdict suite in inventory | P021 catalogue REFUSED; no P030 consumer | SOURCE_VERIFIED absence | M9; do not inherit OPEN-N13 |
| CL060 | P022 | PR #140 promotion-label guard merged; ancestor of 42f9957 | `qa/PR140_REGISTRY_VERIFICATION.json`; `build_strategy_research_registry.py` `_promotion_maturity` `:571`, `build_strategy_entry` `:625-639` | SOURCE_VERIFIED (inspection only; not executed) | merge `2e8a649a9052429b60b236dbab8b8376d8d5b065`; **not** P013 freeze/enumeration store; no retrieval blocker |
| CL061 | P020 | Interface freeze verified for nonaccepting candidate implementation | `qa/P020_FREEZE_VERIFICATION.json`; `inputs/P020_FROZEN/FREEZE_RECEIPT.json` | SOURCE_VERIFIED (Lead qa) | receipt SHA256 `a0a94105dea818f152453eadfcd05be5b91a3bfde70f64192de947ce2e95b6c5`; status `FROZEN_FOR_NONACCEPTING_CANDIDATE_IMPLEMENTATION`; **not draft**; full integration `WAIT_P020_ACCEPTANCE`; six-member hash unchanged; no new carrier |

## Appendix — numbered I/M coverage (combine equivalents; none silent)

**P013 implemented 1–10 / missing 11–16**

| Report | CL |
|---|---|
| I1 canonical_json | CL001 |
| I2 six-member eval hash | CL002 |
| I3 identity helpers; no param/space hash fn | CL005 (also CL003, CL004, CL029) |
| I4 TrialRecord 48 | CL006 |
| I5 ArtifactManifest | CL007 |
| I6 ContractModel | CL008 |
| I7 lineage/unsimulated/EvidenceIdentity | CL009 |
| I8 StrategyPackage | CL010 |
| I9 unsimulated_controls path | CL011 |
| I10 contract test trio | CL012 |
| M11 no writer; branch reader | CL013 + CL014 + CL015 + CL016 |
| M12 no staged-selection / TYPE member | CL051 |
| M13 no P020CanonicalPathReceiptVerifier | CL052 |
| M14 no CatalogCommitPreimageV1 and coined types | CL013 |
| M15 mega JSON/MD only | CL017 |
| M16 no committed cost/eval-config bytes | CL053 |

**P021 §2.1 I1–7 / §2.2 1–4 / §2.3 1–4**

| Report | CL |
|---|---|
| I1 7 REFUSED catalogue | CL019 |
| I2 validate_catalog + mutants | CL020 |
| I3 eligibility shapes | CL023 |
| I4 identity formulae | CL001, CL002, CL003, CL029 |
| I5 eligibility state ladder | CL023 + CL034 |
| I6 UnsimulatedControl | CL009 |
| I7 DurableRiskPolicy | CL025 |
| 2.2-1 B-22 policy set | CL026 |
| 2.2-2 divergence machinery | CL027 |
| 2.2-3 B-17 M2 + missing 5m | CL027 + CL028 |
| 2.2-4 ds-v1 construction | CL024 |
| 2.3-1 no eligibility module | CL023 |
| 2.3-2 B-01 engine | CL054 |
| 2.3-3 B-08/19, B-12/21/16, B-09 | CL055 |
| 2.3-4 four unset limits | CL021 |

**P022 implemented 1–10 / missing 11–16**

| Report | CL |
|---|---|
| I1 compute_family_id | CL004 |
| I2 family/candidate/package fields | CL010 |
| I3 preregistered_space_hash field | CL005 |
| I4 LIVE_CANDIDATE + BLOCKED | CL034 |
| I5 Environment enum | CL009 |
| I6 env excluded from hashes | CL002 + CL003 |
| I7–I9 registry 63 / 46/17 / no strategy_family | CL033 |
| I10 TAG_DICTIONARY.json | CL056 |
| M11 no FAM-UNKNOWN binding | CL034 |
| M12 no ledger / observation_id-in-any-py | CL035 + CL037 |
| M13 no FAMILY_OBSERVED / window / siblings | CL035 |
| M14 no evidence_window_start / frozen_at | CL036 |
| M15 no master Parquet/DuckDB catalogue | CL038 |
| M16 simulate_slice, no provenance hook | CL057 |
| PR140 promotion-label guard (not P013 freeze store) | CL060 |

**P030 I1–I6 / M1–M12**

| Report | CL |
|---|---|
| I1 offline core | CL040 |
| I2 21-field record fence | CL058 |
| I3 start-refusal + socket tripwire | CL040 |
| I4 D026 mutant battery | CL043 |
| I5 OPSA local components | CL044 |
| I6 closed-bar + replay/same-slot | CL042 |
| M1 no sidecar events | CL043 |
| M2–M6, M12 recon/freshness/reconnect/provenance/CORRECTION/N6 | CL046 |
| M7 no runtime Hyperliquid backend | CL043 |
| M8 no collector heartbeat wiring | CL045 |
| M9 no P021 check-suite consumer | CL059 |
| M10 ccxt downloader / P3 proxy | CL049 |
| M11 io.py / cache.py | CL049 |

**Unmapped numbered I/M claims:** none.

## Remaining facts (short)

1. P0-04 must still freeze `param_hash` / `preregistered_space_hash` preimages.
2. P013 freeze-receipt / cell coordinates / covered-commit **producer** unbuilt.
3. Four P021 numeric limits unset; M2/ds-v1/classifier unbuilt; 5m missing from bundle `TIMEFRAME_SECONDS`.
4. P022 ledger/anchor/resolver unbuilt; P013 freeze/enumeration store unbuilt. PR #140 promotion-label guard is **verified** by source inspection (`qa/PR140_REGISTRY_VERIFICATION.json`, merge `2e8a649a9052429b60b236dbab8b8376d8d5b065` ancestor of 42f9957; `_promotion_maturity` `:571`, `build_strategy_entry` `:625-639`) and is **not** that store. No PR140 retrieval blocker. Code not executed.
5. P020 freeze **verified** (`qa/P020_FREEZE_VERIFICATION.json`, `FROZEN_FOR_NONACCEPTING_CANDIDATE_IMPLEMENTATION`, receipt SHA256 `a0a94105dea818f152453eadfcd05be5b91a3bfde70f64192de947ce2e95b6c5`); not a draft. Full integration remains `WAIT_P020_ACCEPTANCE`. Six-member evaluation hash unchanged; no new carrier.
6. P026 phone-push / G9 host / live collector backup consistency not evidenced.

No product/schema/operational authority. Stop.
