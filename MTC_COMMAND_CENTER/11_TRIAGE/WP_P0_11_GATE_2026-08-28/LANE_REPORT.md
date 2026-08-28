# WP-P0-11 gate build lane report

Date: 2026-08-28

Branch/worktree: `feature/wp-p0-11-kernel-legacy-compatible-20260825` at
`C:\WPP011_20260825`. The implementation-A source authority is frozen at
`5c5603065c994d545c0eaa8c137fa9edd5cdfc28`.

## Outcome

Stage 1 is frozen. The Stage 2 sequence builder, closed observation adapter, keyed comparator,
double-build verifier, 76-row field/component discrimination harness, and 17 structural/provenance
mutations are built and executed. Stage 3 row-arm batch 1 adds C01-C05: five real isolated producer
mutations are RED and the same five scenarios are GREEN against clean frozen implementation A.

The full gate outcome is **STOP**, not PASS or FAIL. Of 40 applicable C-rows, 5 are GREEN after RED
and 35 remain STOP; C25 and C27 remain policy-only. Independent flagship reproduction and any future
subject comparison are also absent. The frozen candidate receipt and external anchor remain
untouched and still truthfully report the pre-Stage-3 row arm as absent; the additive Stage-3
candidate evidence is not substituted into either frozen artifact.

This is the prompt's permitted truthful partial. No kernel, A, B, Pine, MTC_V2, backtest, adapter,
schema, Bridge, broker, venue, host, testnet, live, credential, repository-setting, or other
worktree file was edited.

Gate-1 tier is T0 because the builder executes strategy code. Repository writes are confined to
`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_11_GATE_2026-08-28/**`; the only non-repository write is the
authorized external anchor at
`C:\LAB\P011_TRUST_ANCHORS\P011-LC-GATE-v1.owner-signed.json`. Stage 3 only read that anchor and did
not modify it.

## Stage 1 freeze

- Both approved profiles contain all 184 values returned by the frozen `resolve_config`.
  - Range Filter profile SHA-256:
    `35d40915d9813265d1cc1f4474a770471d3ea443e5a67b12ccb4f9e7270944d8`.
  - Supertrend profile SHA-256:
    `c1570317e0dd9ffc2eb9d4ad652891bce65e3ff2007cbbcbba1523ddb33b78f0`.
- `P011_OBSERVATION_SCHEMA_v1.json` is closed and contains 76 declared scalar paths, including 56
  state-digest components and all 11 event components. SHA-256:
  `c18fb1622ab38b374d65a1304994f0e9f5d8993f948e75d99694bdfceb5fdb2e`.
- The CSV binding is exact: header `ts,open,high,low,close,volume`; `timestamp=ts`; OHLCV comes from
  the same-named columns; `Bar.bar_index` is the zero-based physical data-row ordinal after the
  header. A supplied index column, non-increasing timestamp, non-finite value, duplicate
  observation key, skipped/duplicate event ordinal, unknown schema child, or unexplained count is
  rejected.
- `p011_legacy_manifest.json` contains C01-C42 once each: 40 `APPLICABLE` rows and two
  `NOT_A_LEGACY_REPRODUCTION_ROW` rows (C25 and C27). Each applicable row has a named legacy
  authority, complete frozen scenario inputs, literal pre-subject expected observation/final state,
  exact comparison rule, corroboration requirement, and producer-mutation requirement. The
  expectations remain uncorroborated until the row adapters run. Manifest SHA-256:
  `13075e23bc2db8517320098f38608851cee123fe57026e9e8607db2a5f08eb2b`.
- P0-10 is not an input: dependency variant `DIRECT_BUILD`, fixture-suite commit
  `NONE_DIRECT_BUILD`.
- Families 18 and 19 remain separately visible as outside the C01-C42 legacy-row universe and
  receive no C18 or acceptance credit.
- Final candidate receipt SHA-256:
  `34823d99e606812bed09325c15381ea03face9b52a6684ec0f7e1152f1aad007`.
  The external anchor matches this receipt and the frozen legacy manifest, records zero subject
  runs, and states that a P0-11 commit touching the anchor is an automatic STOP.

Stage-1 command and real output:

```powershell
python -I MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\stage1_freeze.py
```

```text
{"external_anchor":"C:\\LAB\\P011_TRUST_ANCHORS\\P011-LC-GATE-v1.owner-signed.json","gate_version":"P011-LC-GATE-v1","legacy_manifest_sha256":"13075e23bc2db8517320098f38608851cee123fe57026e9e8607db2a5f08eb2b","outcome":"PASS","profiles":[{"path":"MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_11_GATE_2026-08-28/profiles/mtc_v2_legacy_supertrend_default_v1.json","profile_id":"mtc_v2_legacy_supertrend_default_v1","resolved_key_count":184,"sha256":"c1570317e0dd9ffc2eb9d4ad652891bce65e3ff2007cbbcbba1523ddb33b78f0"},{"path":"MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_11_GATE_2026-08-28/profiles/mtc_v2_legacy_range_filter_default_v1.json","profile_id":"mtc_v2_legacy_range_filter_default_v1","resolved_key_count":184,"sha256":"35d40915d9813265d1cc1f4474a770471d3ea443e5a67b12ccb4f9e7270944d8"}],"receipt_sha256":"6c023441d79eacb59736809f9dfab26ea97c6a6806141c24d2bb735847459dd3","schema_sha256":"c18fb1622ab38b374d65a1304994f0e9f5d8993f948e75d99694bdfceb5fdb2e","subject_runs":0}
```

The shown receipt hash is the Stage-1 skeleton hash. It was superseded, as designed, when the real
candidate artifact hashes were inserted and the external anchor was updated; the final hash is the
one listed above.

## Built behavior

`p011_gate.py build-baseline`:

- refuses a source commit other than `5c560306...`, checks the A tree OID
  `7aa6f867d821df08a00358adf2dd4400b9c719e8`, rejects modified A worktree bytes, and
  refuses a committed checkout with any post-source change outside this gate package;
- imports A only after the identity checks and rejects any resolved `mtc_v2` module outside the
  pinned source root;
- invokes the real `mtc_v2.core.runner.Runner.run` once per profile over the ordered `Bar` stream;
- observes raw signals at the real gate seam, entry/exit calls at `PositionManager`, and end-of-bar
  `Runner.state` at iterable boundaries; it does not accept precomputed observations;
- encodes every float with `float.hex()`, sorts only the fields whose schema declares sorting, and
  writes canonical JSONL;
- produces `mtc_v2_legacy_sequence.jsonl`, `final_states.json`, `row_corroboration.json`, and
  `baseline_manifest.json`.

`p011_gate.py compare` verifies the external receipt/manifest pins first, baseline artifact hashes,
closed-schema shape and state-digest preimages, exact input/profile conservation, unique observation
keys, ordering, values, and row/independent/subject prerequisites. It emits rc 0 for PASS, rc 1 for
an observed deviation, and rc 3 for inability to evaluate. Missing keys are compared by identity,
so one removed middle record does not cascade all later records into opaque value mismatches.

## Final double build

The same command was run from two absent output paths. These are the literal producer commands
executed by the two hidden background processes:

```powershell
python -I MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\p011_gate.py build-baseline --source-commit 5c5603065c994d545c0eaa8c137fa9edd5cdfc28 --producer A --data IBKR_PAPER_BRIDGE\tests\fixtures\BTC_1h_real.csv --profile MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\profiles\mtc_v2_legacy_supertrend_default_v1.json --profile MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\profiles\mtc_v2_legacy_range_filter_default_v1.json --legacy-manifest MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\p011_legacy_manifest.json --out C:\tmp\p011_gate_committed_run1
python -I MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\p011_gate.py build-baseline --source-commit 5c5603065c994d545c0eaa8c137fa9edd5cdfc28 --producer A --data IBKR_PAPER_BRIDGE\tests\fixtures\BTC_1h_real.csv --profile MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\profiles\mtc_v2_legacy_supertrend_default_v1.json --profile MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\profiles\mtc_v2_legacy_range_filter_default_v1.json --legacy-manifest MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\p011_legacy_manifest.json --out C:\tmp\p011_gate_committed_run2
```

Each emitted this real result, differing only in `output_directory`:

```text
{"artifact_status":"SEQUENCE_BUILT_ROW_ARM_STOP_INDEPENDENT_REPRODUCTION_PENDING","command":"build-baseline","full_gate_outcome":"STOP","full_gate_stop_reason":"row producer corroboration/mutations and independent reproduction are not earned","outcome":"PASS","output_directory":"C:\\tmp\\p011_gate_committed_run1","profile_metrics":[{"events":3509,"final_state_digest":"9a7c449c202f3a83b57e7964f4fbe2521f54b5c9ba3fa6cce3617d8fffe8e541","input_bars":48077,"observations":48077,"profile_id":"mtc_v2_legacy_range_filter_default_v1"},{"events":1206,"final_state_digest":"8a3eded32dada6d7a164f52b475974a598ed6b5386c2c1aa71c3f730d18c8055","input_bars":48077,"observations":48077,"profile_id":"mtc_v2_legacy_supertrend_default_v1"}],"sequence_sha256":"727e438181bf1cd74ae0a90774afddf963ff03a382ee0646eaf2bb6d6010086e","total_observations":96154}
```

Byte-identity command:

```powershell
python -I MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\p011_gate.py verify-double-build --run1 C:\tmp\p011_gate_committed_run1 --run2 C:\tmp\p011_gate_committed_run2
```

Real output:

```text
{"artifacts":[{"artifact":"mtc_v2_legacy_sequence.jsonl","byte_identical":true,"run1_sha256":"727e438181bf1cd74ae0a90774afddf963ff03a382ee0646eaf2bb6d6010086e","run2_sha256":"727e438181bf1cd74ae0a90774afddf963ff03a382ee0646eaf2bb6d6010086e"},{"artifact":"final_states.json","byte_identical":true,"run1_sha256":"1a73b5fa3864bd434aca94cde8ac26d2b8147fa84f1fe87803c9cf122958008d","run2_sha256":"1a73b5fa3864bd434aca94cde8ac26d2b8147fa84f1fe87803c9cf122958008d"},{"artifact":"row_corroboration.json","byte_identical":true,"run1_sha256":"d28acdb573c18bda004d520c5aa6efb7208151fcae1eee3cdfbace918865baaf","run2_sha256":"d28acdb573c18bda004d520c5aa6efb7208151fcae1eee3cdfbace918865baaf"},{"artifact":"baseline_manifest.json","byte_identical":true,"run1_sha256":"5219d0243d9dc85b4c6ff9f12f82788babbe417307c81cd300b19edcaecd5e20","run2_sha256":"5219d0243d9dc85b4c6ff9f12f82788babbe417307c81cd300b19edcaecd5e20"}],"byte_identical":true,"outcome":"PASS"}
```

The canonical sequence is 312,842,545 bytes. It contains 96,154 unique observation keys: 48,077
per profile. Range Filter has 3,509 observed entry/exit events; Supertrend has 1,206. The first key
for each profile is bar 0 at `2021-01-01T06:00:00+00:00`; the last is bar 48,076 at
`2026-06-28T00:00:00+00:00`.

## Mutation evidence

Field/component matrix command and real output:

```powershell
python -I MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\p011_gate.py mutation-harness --baseline C:\tmp\p011_gate_committed_run1 --out MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\evidence\discrimination_matrix
```

```text
{"digest_components":56,"event_components":11,"matrix_rows":76,"matrix_sha256":"533184d7049abefa346352c58d4e3fa70d27e18dd37ba25cb4b2874b1c306b86","outcome":"PASS","output_directory":"C:\\WPP011_20260825\\MTC_COMMAND_CENTER\\11_TRIAGE\\WP_P0_11_GATE_2026-08-28\\evidence\\discrimination_matrix","red":76,"restored_green":76,"transcript_sha256":"85e6d19ebbf2d60caf129aef1f0b75ce63a21243f73b8051a6cf481f6045beb9"}
```

The generated
`evidence/discrimination_matrix/mutation_transcript.jsonl` contains, for every one of the 76
declared paths, the literal subprocess argv, mutated before/after values, expected and actual
changed-record count, failing key, RED stdout/stderr/rc/evidence hash, and restored GREEN
stdout/stderr/rc/evidence hash. It is the per-mutation real-output record; the matrix is generated
from the schema catalog rather than a hand-picked field list.

Structural/provenance mutation command and real output:

```powershell
python -I MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\evidence\structural_mutations.py
```

```text
{"expected_results":17,"mutations":17,"outcome":"PASS","restored_results":17,"sha256":"60dcfd312e8573b753d69fdcf2ee9767006251e980dceeab0349b12ae9cd48db"}
```

`evidence/structural_mutations.json` records every canonical command argv and real output for: missing,
duplicate and reordered observations; undeclared child; duplicate/deleted/added/moved event;
inverted side; changed position state; changed OHLCV observation; parser failure classified STOP;
coordinated local receipt rehash; wrong producer identity; deleted applicable C-row; changed resolved
configuration; and changed input-data byte. Each executed case produced its pre-committed rc and its
restoration produced the pre-committed clean result. The transcript replaces only the Python,
repository-root, and run-specific scratch path prefixes with the declared `<PYTHON>`,
`<REPO_ROOT>`, and `<SCRATCH>` tokens; semantic values and return codes are unchanged. The
generator was rerun twice after this normalization; both runs produced the same
`60dcfd31...8db` artifact hash.

Not executed and not claimed: the 40 row-producer GF-field-8 mutations, a future independent
subject's import/delegation mutation, P0-10 mutations (direct-build branch uses none), and physically
moving the authoritative external anchor. These omissions keep the full gate at STOP.

## Final comparator result

```powershell
python -I MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\p011_gate.py compare --receipt MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\P011_GATE_RECEIPT.json --baseline C:\tmp\p011_gate_committed_run1 --subject-mode LEGACY_COMPATIBLE --mismatch-ledger C:\tmp\p011_final_mismatch_ledger.json
```

```text
{"outcome":"STOP","reason":"row-semantic arm is not evaluable: 40 direct-build producer adapters and their D026 mutations are frozen but not executed by this sequence builder"}
RC=3
```

No mismatch ledger is emitted when comparison stops before a subject observation exists.

## Independent remeasurement

All counts and identities above were remeasured from bytes, independently of builder-reported
counts, with:

```powershell
python -I MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\evidence\remeasure.py --run1 C:\tmp\p011_gate_committed_run1 --run2 C:\tmp\p011_gate_committed_run2
```

The real output re-established:

- fixture SHA-256 `3a3a...7bb`, exact six-column header, 48,077 data rows, and the two declared
  endpoints;
- source commit `5c560306...` separately from checkout HEAD, A tree `7aa6f867...`, controller
  freeze `77a10e65...`, and B freeze
  `b5ed1afa...`;
- two 184-key profile files with the hashes above;
- 42 manifest rows = 40 applicable + 2 policy-only;
- 76 schema fields, 56 digest components, and 11 event components;
- 96,154 unique sequence keys, the per-profile/event counts above, and identical run hashes;
- four byte-identical candidate artifacts;
- current gate-tool SHA-256
  `7797908a5570c14fa5133dc544f00eba03082cea35bfe41f3dd022acc1655529`, exactly matching the
  adapter hash inside both baseline manifests;
- row arm = 40 STOP + 2 not-applicable + 0 GREEN;
- matrix = 76 RED + 76 restored GREEN;
- structural mutations = 17 unique IDs + 17 expected RED/STOP results + 17 expected
  restorations, with no failures and SHA-256 `60dcfd31...8db`;
- external receipt/manifest pin matches and subject-run count remains zero.

## Stage 3 row arm — batch 1 (C01-C05)

The required merge of `origin/master` `85c3e17f97efa1ba83ef9c679de319a50ad3be04` landed first as
merge commit `7dfccae1`. The re-resolved WP-P0-09 authority is now Git blob
`1c39ab939dfcf5589e5ec8fba4af8966947a67fc`, SHA-256
`7d48871a3e45dab118e97969d701912edb5d7c16a4d822d816beca1d03a42249`. The additive
`row_arm.py` pins that current identity, the frozen manifest/receipt/anchor identities, A commit
`5c560306...`, and A tree `7aa6f867...` before any producer executes. It rejects committed or
worktree drift in A. Mutations are applied only to temporary copies of `mtc_v2`; no A, B, Pine,
Stage-1 artifact, receipt, or external-anchor byte is changed.

The actual build command was:

```powershell
python -I MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\row_arm.py build --out MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\evidence\row_arm
```

Real output:

```text
{"artifacts":{"row_corroboration.json":"ea66cab4fee8f8018a50a46bdea752187f7fbdfe57b28ac3329a0b1538ff9dec","row_results.jsonl":"c9eab1b7baf569e98af7a68d9795fa1c50b9a70dde28ee6763a551149e7d1689"},"command":"build","counts":{"clean_green":5,"green":5,"mutation_red":5,"not_applicable":2,"stop":35,"total":42},"outcome":"STOP","output_directory":"C:\\WPP011_20260825\\MTC_COMMAND_CENTER\\11_TRIAGE\\WP_P0_11_GATE_2026-08-28\\evidence\\row_arm","rows_executed":["C01","C02","C03","C04","C05"]}
```

`evidence/row_arm/row_results.jsonl` is the complete per-row transcript. It records the literal
subprocess argv, stdout, stderr and return code; exact before/after source hashes; the one replaced
source seam; pinned inputs/oracle; every mismatch; every resolved `mtc_v2` import; and the clean
comparison. Only path prefixes are normalized: the executed Python, repository root and random
temporary authority-copy root become `<PYTHON>`, `<REPO_ROOT>` and `<SCRATCH>`. No argument,
semantic value, output line or return code is otherwise changed.

| Row | Frozen legacy authority and arithmetic citation | Producer mutation RED | Clean producer GREEN |
|---|---|---|---|
| C01 | A `5c560306...` / tree `7aa6f867...`; `runner.py:495-514`, `:1527-1531` | `C01-GF8-MUT-001`, rc 1: conflict branch disabled; actual `gated_long=true`, `gated_short=true`, `reason=fixture_conflict` | rc 0: 5/5 leaves exact; conflict clears both sides and emits `signal_conflict` |
| C02 | A `5c560306...`; `gates.py:27-39`, `:389-402` | `C02-GF8-MUT-001`, rc 1: missing MA returns both false; three exact mismatches | rc 0: 5/5 leaves exact; both unready MA and HTF gates pass open |
| C03 | A `5c560306...`; `runner.py:832-847`, `:860-884`; Pine `MTC_V2.pine:1680-1721` corroborates source only | `C03-GF8-MUT-001`, rc 1: refresh reset `0→1`; actual new-pulse/hold counts `1/0`, fires, direction clears | rc 0: 4/4 leaves exact; new-pulse/hold counts `0/1`, no fire, direction long |
| C04 | A `5c560306...`; `runner.py:895-921` | `C04-GF8-MUT-001`, rc 1: proximity comparator inverted; wait remains and retest does not fire | rc 0: 5/5 leaves exact; IEEE-754 distance `0x1.999999999999ap-5`, fires, wait clears |
| C05 | A `5c560306...`; `runner.py:592-607`, `:928-939` | `C05-GF8-MUT-001`, rc 1: exit-block removed; same-bar short opens and final position remains | rc 0: 4/4 leaves exact; `opp_signal` exits first, short is deferred, final state flat |

Three anti-regression properties are enforced at the accepting top-level caller:

1. **Every expected value is compared.** The verifier recursively compares the exact expected and
   actual key union after `float.hex()` encoding. Batch 1 independently remeasures 23 expected
   leaves and 23 compared leaves. A missing key, extra key, wrong type, list-length drift, or wrong
   value is a terminal mismatch; no declared value can be skipped.
2. **Scenario identity is verifier-pinned.** `row_arm.py` owns the ordered C-row → scenario-ID,
   adapter, authority, full inputs, literal oracle, citations and mutation-ID registry. It refuses
   any manifest value that differs; it never learns an accepting identity from the scenario file.
3. **Required fields fail closed.** The top-level caller requires exactly one scenario and all eight
   frozen scenario members before producer execution, then requires exact full input/oracle equality
   to its pinned contract. Omission returns STOP; an omitted expected/actual leaf cannot turn into a
   skipped check.

The contract mutation command
`python -I MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\row_arm.py contract-harness
--out MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\evidence\row_arm_contract_mutations.json`
executed four top-level cases. Real output was
`{"artifact_sha256":"85c92c2cc88535c5a59f1a0f94bd75482224af9f84efc32bb29107359771d120","cases":["scenario_identity_changed","required_input_omitted","expected_leaf_omitted","required_scenario_member_omitted"],"counts":{"fail":3,"stop":1,"total":4},"outcome":"PASS"}`.

Independent remeasurement command:

```powershell
python -I MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\evidence\row_arm_remeasure.py --evidence MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\evidence\row_arm --manifest MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_11_GATE_2026-08-28\p011_legacy_manifest.json
```

Real output:

```text
{"artifact_hashes":{"batch_manifest.json":"1a26ac5d4b2365091d1cb2f24bf7bc86032b317fbc165aa905557a6f86ee98e5","row_corroboration.json":"ea66cab4fee8f8018a50a46bdea752187f7fbdfe57b28ac3329a0b1538ff9dec","row_results.jsonl":"c9eab1b7baf569e98af7a68d9795fa1c50b9a70dde28ee6763a551149e7d1689"},"compared_expected_leaves":23,"counts":{"applicable":40,"clean_green":5,"green":5,"mutation_red":5,"not_applicable":2,"red_mismatches":14,"stop":35,"total":42},"expected_leaves":23,"outcome":"PASS","p009_blob_oid":"1c39ab939dfcf5589e5ec8fba4af8966947a67fc","p009_sha256":"7d48871a3e45dab118e97969d701912edb5d7c16a4d822d816beca1d03a42249","rows":["C01","C02","C03","C04","C05"]}
```

A second build into a separate output path produced the same three artifact hashes. The exact
`verify-double-build` result was `byte_identical=true`, with `row_results.jsonl c9eab1b7...`,
`row_corroboration.json ea66cab4...`, and `batch_manifest.json 1a26ac5d...` identical. The scratch
second-build artifacts were removed after verification; the quoted command/output remains part of
this report and the committed candidate is `evidence/row_arm/`.

Unresolved/pending rows: C06-C24, C26, and C28-C42 (35 applicable rows) are intentionally STOP
because the pre-committed batching rule prefers a truthful partial; no authority-silence claim is
made for them yet. C25 and C27 are not legacy reproduction rows. This row arm does **not** yet cover
sizing, stops, MultiTP, break-even, trailing, collisions, costs, warm-up, invalid bars, duplicate
handling, de-fanged controller inputs, the `tw_*` modes, B's pivot/event-mode authorities, HTF
alignment/readiness equations, or both signal-producer equations. It also does not cover a subject,
subject import/delegation mutation, independent flagship reproduction, kernel consolidation, or any
live/economic action. Therefore the full gate remains **STOP**.

## Discrepancies and non-claims

1. Shared Git churn moved local `master` from `5c560306...` through `cd3b8486...` to
   `85c3e17f...` during the lane. The source commit object, A tree, tags, and inputs remained pinned.
   Package commits change only this gate directory; the builder rejects any checkout with other
   post-source changes rather than treating the expected shared-ref move itself as tampering.
2. Repository A cannot accept its own full resolved snapshot as `Runner` input: `Runner.__init__`
   calls `resolve_config` again, and five derived `use_tp*` output keys are not accepted input keys.
   The first attempt stopped before any observation with:

   ```text
   {"outcome":"STOP","reason":"unhandled ValueError: Unknown config keys: ['use_tp', 'use_tp_multi', 'use_tp_single_atr', 'use_tp_single_pct', 'use_tp_single_r']"}
   ```

   The adapter now passes the three frozen explicit inputs and immediately asserts that
   `Runner.config` equals the frozen 184-key snapshot exactly. No A code was changed. The failed
   scratch directory `C:\tmp\p011_gate_baseline_run1` contains only a zero-byte sequence from that
   stopped attempt and is not referenced by the receipt.
3. Stage 1 froze before the P0-09 citation refresh and therefore still pins blob `f96b5325...` /
   SHA-256 `6464e6f0...`. The required `85c3e17f...` merge changed the repository authority to blob
   `1c39ab93...` / SHA-256 `7d48871a...`. The frozen manifest was not changed; Stage 3 pins and
   records the new identity separately and uses direct frozen-source `file:line` citations.
4. Current master A/Pine has no `wt_*` surface. C28-C30 use
   `legacy/pine-controller/2026-08-25` at `77a10e65...`; current master is not mislabeled as their
   legacy producer.
5. The upstream normalized BTC file hash `521d30ca...bac` differs from the emitted fixture hash
   `3a3a4939...7bb`. Both identities remain in the receipt.
6. The sequence is a deterministic capture candidate, not an instrument-faithful BTC profile, not
   a profitability or safety result, and not an independent economic proof for a future
   `WRAP_MOVE_OF_A` subject.
7. Pine is source corroboration only. No TradingView export/runtime was executed. B and the
   controller freeze were read for identity and frozen row authority but their row producers were
   not executed in this partial.
8. No subject exists, no subject classification/import graph is recorded, no independent flagship
   reproduced the build, and this implementer issues no acceptance verdict.
9. The first committed candidate required checkout `HEAD` itself to equal the frozen A commit,
   which made the committed gate package impossible to rerun in place. Before push, that check was
   replaced with the stricter usable invariant described above: every committed change since the
   source freeze must be inside this gate directory, while A's tree and worktree bytes must still
   match the source freeze exactly. Both profiles were rebuilt twice into the `committed_run*`
   directories and the receipt/anchor were repinned. The superseded `final_run*` candidates are
   not referenced by the final receipt.
10. Before the required master merge, the routed repository rules still required a GitHub issue
    claim, so issue #133 was created for this exact branch/worktree/package. The merged rules retire
    that mandatory mechanism under OD-20260826-6. Issue #133 is therefore only a narrow durable lane
    record, not an accepting guard or authority expansion.

## Remaining work

1. Continue in manifest order with C06-C24, C26, and C28-C42 against their exact current-A,
   controller-freeze, or B-freeze authority. C26-C30 and every de-fanged surface must use
   `legacy/pine-controller/2026-08-25` (`77a10e65...`), never current master A.
2. Execute and record each of the remaining 35 rows' isolated producer mutation RED and
   clean-authority GREEN; update the additive Stage-3 `row_corroboration.json` only from real
   evidence. Frozen Stage-1 expected values and artifacts must not change.
3. Execute the remaining subject/import and external-anchor mutation cases once an actual subject
   adapter exists; classify that subject as `INDEPENDENT_REIMPLEMENTATION` or `WRAP_MOVE_OF_A` and
   pin its tree and import/call graph.
4. Have a flagship other than the builder independently check out the fixed commit, rerun the
   exact commands, and reproduce all pinned identities, candidate-baseline hashes, counts, and
   mutation outcomes. This lane must not perform that step.
5. Only after those prerequisites are evaluable may `compare` return PASS or FAIL for a real
   subject. Kernel consolidation remains separately owner-gated and has not started.
