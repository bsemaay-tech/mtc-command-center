# P014 Read-Only Report (Fixture Ledger and Contract Snapshot)

This report is fixture data only. Recorded `accepted=false` is `C:/tmp/P014_RO_20260914/P031_M1_SCOPE_AND_STATUS.md:718` (quote: `` - `accepted`: `false` ``). `authoritative` is `false` at `C:/tmp/P014_RO_20260914/fixture-status-report.json:10` (quote: `"authoritative": false,`). P0-14 sequencing amendment is preserved at `C:/tmp/P014_RO_20260914/START_HERE.md:54` (quote: `P0-14 | Owner chose to defer Minimum Explorer behind core Bridge engineering with a small reproducible read-only report meanwhile. Preserve sequencing amendment; full package is not complete.`). It answers exactly Q-A and Q-B from copied P0-31 fixture ledger inputs and the P0-13 trial-catalog contract. It is not product code, not Explorer work, not a decision, and not an acceptance.

- `source_kind` is `FIXTURE` at `C:/tmp/P014_RO_20260914/fixture-status-report.json:16` (quote: `"source_kind": "FIXTURE"`).
- JSON `scope` is `"FIXTURE LEDGER DATA"` at `C:/tmp/P014_RO_20260914/fixture-status-report.json:82` (quote: `"scope": "FIXTURE LEDGER DATA",`).
- The JSON snapshot has no `accepted` key and no `fixture_only` key.

## Q-A. Candidate families in P0-31 fixture lifecycle ledger

| candidate / family | current lifecycle state | last transition | check_set_purpose | failing_checks / rejection reason | source (file:line or command) |
| --- | --- | --- | --- | --- | --- |
| QLC-20260912-demo0001 | CANDIDATE | 2026-09-12T20:00:02Z `CANDIDATE` (writer=REGISTRAR) | not persisted in this fixture evidence | `[]` | `SELECT * FROM lifecycle_events ORDER BY global_sequence` on `file:C:/tmp/P014_RO_20260914/fixture-ledger.sqlite?mode=ro`; purpose cell from `C:/tmp/P014_RO_20260914/reproduce_report.py:353` because evidence has no `check_set_purpose` key (derivation `C:/tmp/P014_RO_20260914/reproduce_report.py:98-101`) |

`lifecycle_current` for this candidate: `current_state=CANDIDATE`, `last_sequence=3`, `source_kind=FIXTURE`, `authoritative=0` (same sqlite URI, `SELECT * FROM lifecycle_current`).

### Q-A event counts per state

Command: `SELECT json_extract(canonical_event, '$.next_state') AS next_state, COUNT(*) FROM lifecycle_events GROUP BY 1` on `file:C:/tmp/P014_RO_20260914/fixture-ledger.sqlite?mode=ro`. `PRAGMA table_info(lifecycle_events)` has no `next_state` column; `next_state` lives in the `canonical_event` JSON blob. The cited command is the query `reproduce_report.py` executes (`C:/tmp/P014_RO_20260914/reproduce_report.py:313` and prints at `C:/tmp/P014_RO_20260914/reproduce_report.py:371`).

- CANDIDATE: 1
- CAPTURED: 1
- TRIAGED: 1

### Q-A unresolved lifecycle contracts

Two lists exist. The JSON snapshot from the older demo run has THREE items. The copied reader's `_render_status_report` encodes SEVEN. The current reader's list is the seven-item source list. The reader CLI cannot be executed from this directory.

JSON snapshot (three), `C:/tmp/P014_RO_20260914/fixture-status-report.json:88-92`:

- DEMOTED TARGET RUNG MAPPING: UNRESOLVED
- CHALLENGE INCUMBENT DEPLOYMENT IDENTITY FIELD: MISSING
- ATOMIC SUCCESSION PROMOTED ACROSS TWO CANDIDATES: UNRESOLVED

Current reader source (seven), `C:/tmp/P014_RO_20260914/p031_lifecycle_ledger.py:1259-1267`:

- DEMOTED TARGET RUNG MAPPING: UNRESOLVED
- CHALLENGE INCUMBENT DEPLOYMENT IDENTITY FIELD: MISSING
- ATOMIC SUCCESSION PROMOTED ACROSS TWO CANDIDATES: UNRESOLVED
- REJECTED FAILED-GATE PURPOSE: UNRESOLVED
- ADMISSION WITHHELD CAPACITY TARGET: UNRESOLVED
- DEPLOYMENT REFRESH ENVELOPE: UNRESOLVED
- EVALUATION RUN CANDIDATE SCOPE: UNRESOLVED

Reader CLI observed traceback (not a printed status report for this fixture):

```
File "C:\tmp\P014_RO_20260914\p031_lifecycle_ledger.py", line 25, in <module>
    from mtc_contracts.execution import LifecycleEvent, LifecycleWriterClass
ModuleNotFoundError: No module named 'mtc_contracts'
```

The seven contracts were derived from that source text instead.

## Q-B. `trial_catalog` public types

19 public types: class/enum/alias names in `__all__` at `C:/tmp/P014_RO_20260914/trial_catalog.py:39-63` excluding `RESERVED_BOUNDARY_KEYS`, `VIEW_SCHEMA_TYPE_VOCABULARY`, `build_typed_parameter_companion_columns`, and `collapse_parquet_type_cell`. Count also printed as `Q-B public_type_count: 19` by `reproduce_report.py`.

Purpose column quotes the docstring (whitespace-collapsed), never paraphrased. Alias `RunCellDimensionsReceipt` has no docstring; purpose is the comment at `C:/tmp/P014_RO_20260914/trial_catalog.py:237`.

| name | fields | purpose from docstring | source |
| --- | --- | --- | --- |
| ArtifactKind | TRADES_PARQUET='trades.parquet', EQUITY_PARQUET='equity.parquet', INTENTS_JSONL='intents.jsonl', LEVELS_PARQUET='levels.parquet' | The four selected-artifact payload kinds named by the design (§2.1). | C:\tmp\P014_RO_20260914\trial_catalog.py:148 |
| BoundaryRefusalReason | RESERVED_BOUNDARY_KEY='RESERVED_BOUNDARY_KEY' | Typed writer-boundary refusal reasons. Bare ``REFUSED`` is forbidden. | C:\tmp\P014_RO_20260914\trial_catalog.py:72 |
| CommitPartEntry | ordinal:int=Field(ge=0), path_slot:NonEmptyStr, staged_byte_length:int=Field(ge=0), staged_sha256:Sha256, row_count:int=Field(ge=0), ordered_trial_ids:tuple[NonEmptyStr, ...] | Item 3 member: one staged part slot, hash-free by construction.  ``path_slot`` is the partition directory plus ordinal and never a final hash-bearing name, which is what keeps the commit digest non-self-referential. While B-15 is open no component may *derive* a value for it. | C:\tmp\P014_RO_20260914\trial_catalog.py:278 |
| CompletedRunInput | terminal_trial_receipts:tuple[TerminalTrialReceipt, ...], family_statistics:ProvisionalBoundaryPayload, selection_decisions:ProvisionalBoundaryPayload, caller_run_envelope:ProvisionalBoundaryPayload, lineage_origin_receipt:LineageOriginReceipt, selected_artifact_payload_receipts:tuple[SelectedArtifactPayloadReceipt, ...] | The closed writer boundary: ``write_completed_run``'s only parameter.  Closed in both directions. ``extra="forbid"`` refuses an undeclared member; every member below is required, so an omitted P0-20-bound or P0-21-bound member refuses at parse before any staged byte or path exists (F-2/F-3/F-8 shape, T18). Reserved keys are refused earlier still, by ``refuse_reserved_boundary_keys`` — a caller label is unrepresentable here rather than merely unknown. | C:\tmp\P014_RO_20260914\trial_catalog.py:195 |
| LineageOriginReceipt | issuer_adapter_id:WriterAdapterId, capability_class:SinkCapabilityClass, canonical_path_receipt_hash:Sha256 \| None=None | The single adapter-issued lineage-origin receipt on ``CompletedRunInput``.  It carries a capability, not a class: ``LineageClassifier`` derives the locked ``simulator_class``. ``canonical_path_receipt_hash`` is absent by design for screening (§4.1.3 exclusion table). | C:\tmp\P014_RO_20260914\trial_catalog.py:182 |
| NestedSchemaColumnEntry | name:NonEmptyStr, type:NonEmptyStr, nullable:bool, fields:tuple[SchemaColumnEntry, ...] | The one nested entry: ``{name, type, nullable}`` plus an ordered ``fields`` array.  A separate type rather than an optional ``fields`` member, so a non-nested entry carries no ``fields`` key at all and the design's "each entry is {name, type, nullable}" is literally true of the serialized bytes. | C:\tmp\P014_RO_20260914\trial_catalog.py:465 |
| ProvisionalBoundaryPayload | blocked_by:NonEmptyStr, ratification_status:Literal['UNRATIFIED']='UNRATIFIED', payload:dict[str, Any] | Clearly-marked carrier for a boundary member whose owning contract is unratified.  The payload is opaque: nothing in this slice interprets it, defaults it, or hashes it into an identity. It exists so an unratified contract is representable as *pending* rather than invented (B-01 statistics/producers, B-07 selection policy, and the caller-supplied run-envelope structure whose mapping onto ``RunEnvelopeV1`` the design explicitly does not decide — §2.1 v1.8 note, G102-F04). | C:\tmp\P014_RO_20260914\trial_catalog.py:122 |
| PublishedViewSchemaDocumentV1 | document_version:Literal['1']='1', columns:tuple[SchemaColumnEntry \| NestedSchemaColumnEntry, ...] | The closed schema document: exactly ``document_version`` and ``columns``.  ``columns`` is an ordered array; ``canonical_json`` sorts object keys but preserves array order, so column order is part of the digest. ``document_version`` is the design constant ``"1"`` (§4.2.1, v1.8) and no producer may compute it. | C:\tmp\P014_RO_20260914\trial_catalog.py:484 |
| ReservedBoundaryKeyRefusal |  | Raised before conversion when a caller supplies a reserved boundary key (F-2). | C:\tmp\P014_RO_20260914\trial_catalog.py:78 |
| RunCellDimensionsReceipt | alias_of=RunCellDimensionsReceiptV1 | Compatibility name for the provisional type; no digest API is attached to either name. | C:\tmp\P014_RO_20260914\trial_catalog.py:238 |
| RunCellDimensionsReceiptV1 | receipt_version:Literal['1'], strategy:NonEmptyStr, symbol:NonEmptyStr, timeframe:NonEmptyStr, source_adapter_id:WriterAdapterId, source_contract_id:NonEmptyStr | The digest-bound cell receipt shape; production remains outside this slice.  ``str_strip_whitespace`` plus ``NonEmptyStr`` refuse an empty or whitespace-only coordinate. No factory in this slice produces one. | C:\tmp\P014_RO_20260914\trial_catalog.py:222 |
| RunEnvelopeV1 | package_hash:Sha256, dataset_manifest_sha:Sha256, cost_model_json:NonEmptyStr, simulator_class:NonEmptyStr, simulator_version:NonEmptyStr, evaluation_config_json:NonEmptyStr | Item 2 of the commit preimage: six declared members, seven serialized.  The six members are exactly the six arguments of ``identity.compute_evaluation_run_hash``. Because this is a ``ContractModel`` subclass, the inherited ``contract_version`` is the seventh serialized member — the v1.8 correction of v1.7's "exactly these six members and no others". None of the six carries a default, so an omitted member refuses at parse (R-7); ``contract_version`` does carry a default, so its omission is filled, not refused — ACCEPTED, not DETECTED, and bounded by the pattern and validator that admit exactly one value. | C:\tmp\P014_RO_20260914\trial_catalog.py:246 |
| SchemaColumnEntry | name:NonEmptyStr, type:NonEmptyStr, nullable:bool | One non-nested schema-document entry: exactly ``{name, type, nullable}``. | C:\tmp\P014_RO_20260914\trial_catalog.py:398 |
| SelectedArtifactCommitEntry | trial_id:NonEmptyStr, manifest_sha256:Sha256, members:tuple[SelectedArtifactMemberEntry, ...] | Item 4 member: one selected trial's committed manifest and payload membership. | C:\tmp\P014_RO_20260914\trial_catalog.py:302 |
| SelectedArtifactMemberEntry | artifact_kind:ArtifactKind, byte_length:int=Field(ge=0), sha256:Sha256 | Item 4 inner member: one committed artifact payload. | C:\tmp\P014_RO_20260914\trial_catalog.py:294 |
| SelectedArtifactPayloadReceipt | trial_id:NonEmptyStr, artifact_kind:ArtifactKind, producer_id:NonEmptyStr, staged_handle:NonEmptyStr, byte_length:int=Field(ge=0), sha256:Sha256 | Closed, immutable payload receipt: exactly the design's member set (§2.1). | C:\tmp\P014_RO_20260914\trial_catalog.py:157 |
| SinkCapabilityClass | SCREEN_SINK='SCREEN_SINK', FULL_EVIDENCE_SINK='FULL_EVIDENCE_SINK' | Opaque adapter-issued capability. Callers never pass a lineage label. | C:\tmp\P014_RO_20260914\trial_catalog.py:175 |
| TerminalTrialReceipt | trial_id:NonEmptyStr | One terminal trial disposition, reduced to what this slice may consume.  Row assembly remains outside this bounded slice, so only the conserved identity is declared here. ``extra="forbid"`` means a caller cannot smuggle row values through this type. | C:\tmp\P014_RO_20260914\trial_catalog.py:137 |
| WriterAdapterId | LEGACY_SIGNAL_SCREEN_RUN_ADAPTER='LegacySignalScreenRunAdapter', MIGRATED_CANONICAL_RUN_ADAPTER='MigratedCanonicalRunAdapter' | The two adapters at the lineage seam (design §2.2). There is no third. | C:\tmp\P014_RO_20260914\trial_catalog.py:168 |

`LineageOriginReceipt.canonical_path_receipt_hash` source text at `C:/tmp/P014_RO_20260914/trial_catalog.py:192`: `canonical_path_receipt_hash: Sha256 | None = None`. Docstring at `C:/tmp/P014_RO_20260914/trial_catalog.py:186-187`: "``canonical_path_receipt_hash`` is absent by design for screening (§4.1.3 exclusion table)."

Refusal reasons enum (`BoundaryRefusalReason` at `C:/tmp/P014_RO_20260914/trial_catalog.py:72`): `RESERVED_BOUNDARY_KEY` (`C:/tmp/P014_RO_20260914/trial_catalog.py:75`).

`test_trial_catalog_types.py` contains 29 tests: 29 is the count of top-level `def test_*` definitions via `ast` on `C:/tmp/P014_RO_20260914/test_trial_catalog_types.py`. Pytest collection would be 40 with parametrization (5 cases at `:169-177` + 6 members of `_completed_run_members` at `:121-144` used by `:194` + 3 cases at `:621` = 29 - 3 + 14 = 40). The suite was not collected (`mtc_contracts` missing).

Catalog data: NONE FOUND. Search: `rglob` of `trades.parquet` / `equity.parquet` / `intents.jsonl` / `levels.parquet` under `C:/tmp/P013_CONTRACT_V2_20260912`. P0-13 handoff `C:/tmp/P014_RO_20260914/P013_HANDOFF.md:50`: "Still excluded and nonaccepted: full catalog writer, selection/artifact/address pipeline,"
