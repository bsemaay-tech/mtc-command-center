# Evidence index and reproduction notes

This is a preparation packet, not implementation or acceptance evidence. Read [MORNING_DECISION_PACKET](MORNING_DECISION_PACKET.md) first. [LEAD_DECISIONS](LEAD_DECISIONS.md) controls scope and interface qualifications. The [claim ledger](CLAIM_LEDGER.md) maps all numbered implemented/missing claims to inspected source or an explicit proposed/unbuilt status.

## Source identity

- Base `42f99571e6abb5222744d9345e1c8a9e19c23c15`; P013 foreign reader branch `3e704c2d`.
- The original 538-file archive used Windows newline conversion. `qa/SOURCE_BLOB_VERIFICATION.json` preserves the initial failed raw-identity check; `qa/SOURCE_IDENTITY_VERIFICATION.json` classifies 120 raw matches and 418 CRLF-only files with no unresolved content mismatch. It does not turn normalized bytes into raw identity.
- `qa/EXACT_LF_SOURCE_VERIFICATION.json` verifies a separately materialized 538-file archive against raw Git blobs. All existing component checks were repeated on that exact LF source.
- `qa/ADDITIONAL_SOURCE_VERIFICATION.json` pins four targeted sources subsequently read outside the original selection. `qa/PR140_REGISTRY_VERIFICATION.json` verifies the merged promotion guard; it does not establish a package-freeze store.
- Original design inputs are under `inputs/`; their seven original hashes are checked before packaging. Historical owner/design documents are evidence, not a transfer of authority to this task.

## Executed checks

Full local working evidence remains at `C:/tmp/P0_OVERNIGHT_CONTROL_20260912`. `inputs/source`, `qa/source_lf`, `qa/p013_lf`, raw CSVs and provider session logs are not duplicated into this Git packet. Source paths in detailed reports are relative to their named Git baseline or that external root. All future test paths are proposals, not delivered implementation.

| Check | Result | Evidence |
|---|---|---|
| Existing P030 offline checker, exact LF source | PASS; existing mutants detected; network attempts 0 | `qa/P030_exact_lf.log` and `.exit` |
| Existing P021 diagnostic checker, exact LF source | 7 REFUSED / 12 closed / 4 open; deliberate modified copies detected | `qa/P021_exact_lf.log` and `.exit` |
| Existing P026 local component suite | 33 passed | `qa/P026_exact_lf.log` and `.exit` |
| Existing foreign P013 reader tests | 3 passed, Python 3.14.2 | `qa/P013_exact_lf.log` and `.exit` |
| Independent existing collector probe | Archive replay NOOP; ingest duplicate REFUSE; one row; two-slot gap derived | `qa/P030_independent_probe.json` |
| Existing identity helper vs separately authored canonical JSON | Expected hash matched; reordering/lineage unchanged; cost mutation detected | `qa/IDENTITY_INDEPENDENT_PROBE.json` |
| Historical CSV inventory | 17 hashes/counts matched; 4,105,966 rows; no internal cadence faults | `qa/P021_FRESH_DATA_VERIFICATION.json` |
| Existing catalogue literal negatives | Five specific calls refused; exact T04 first-error corrected | `qa/P021_LITERAL_FIXTURE_CHECK.json` |
| P012/P020 supplied handoff evidence | Supplied report/record and freeze-member hashes matched | `qa/P012_HANDOFF_VERIFICATION.json`, `qa/P012_LATEST_CLOSURE_VERIFICATION.json`, `qa/P020_FREEZE_VERIFICATION.json` |
| Proposed fixture expected values | Literal hash/arithmetic derivation only, no new target tests | `qa/FIXTURE_EXPECTED_VALUES.json` |

Python 3.12.12 executable: `C:/Users/BarışSemaay/AppData/Roaming/uv/python/cpython-3.12.12-windows-x86_64-none/python.exe`. The P013/identity checks used existing `C:/Python314/python.exe` (3.14.2) because its required dependencies were available. No packages were installed. The 3.14.2 subset is not the mandatory Python 3.12 Bridge acceptance suite.

Repeat existing checks from the external root's `qa/source_lf` with bytecode disabled and temporary files under its `qa/tmp`: `python check_market_data_collector.py`; `python MTC_COMMAND_CENTER/03_QUANTLENS/tools/p021_readiness_rules.py --self-check`; and `python -m unittest discover -s MTC_COMMAND_CENTER/tools/opsa -p test_opsa.py -q`. For P013 use Python 3.14.2 and `python -m pytest -q -p no:cacheprovider MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_trial_catalog.py` from `qa/p013_lf`, with its supplied contracts path available. Exact recorded runtime outputs remain authoritative if a different environment fails.

The 24 cases in [FIXTURE_BANK](FIXTURE_BANK.md) are proposed target fixtures. Existing component evidence and expected-value derivations do not execute those future tests or accept any full package. No fresh model acceptance audit was requested or claimed; nonbinding prose received Lead content/source/link checks under current T2 policy.

## Delivery integrity

`MANIFEST.json` records each delivered file's SHA256 and byte length (excluding itself) and the two current handoff files outside this folder. `PREVIOUS_GOVERNANCE_HANDOFF.md` preserves the prior governance handoff byte-for-byte. The owned branch and exact stop state are recorded in `RUN_STATE.md`.

Package-local `.gitattributes` preserves recorded evidence bytes across Git checkouts. The two outside-handoff hashes describe delivered Windows files, not a cross-host byte-identity promise. Historical input documents are byte-preserved; their original relative links refer to their source locations, not this packet.
