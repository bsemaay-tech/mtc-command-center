# P014 Execution Report

## What was built
- `P014_READONLY_REPORT.md` corrected in place per the Grok P14B detection audit (lane P14FIX2G).
- `reproduce_report.py` now executes and prints `SELECT json_extract(canonical_event, '$.next_state') AS next_state, COUNT(*) FROM lifecycle_events GROUP BY 1` (the query that actually returns CANDIDATE/CAPTURED/TRIAGED = 1/1/1). Standard library only (`ast`, `json`, `sqlite3`, `pathlib`).
- `REPORT.md` regenerated with verbatim reproducer output and the pinned interpreter.
- `DISPOSITION_FIX2.md` records prior-9 and new-1/2/3.
- `SHA256SUMS.txt` regenerated last (LF).

## SHA file

- `SHA256SUMS.txt` (same directory) contains SHA-256 checksums for:
  - copied inputs used by this task
  - `P014_READONLY_REPORT.md`
  - `reproduce_report.py`
  - `REPORT.md`
  - `DISPOSITION_FIX1.md`
  - `DISPOSITION_FIX2.md`

## Interpreter used

- `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe` (CPython 3.12.12)

## Reproducer output (verbatim)

```text
# Q-A. Fixture lifecycle report
| candidate / family | current lifecycle state | last transition | check_set_purpose | failing_checks / rejection reason | source (file:line or command) |
| --- | --- | --- | --- | --- | --- |
| QLC-20260912-demo0001 | CANDIDATE | 2026-09-12T20:00:02Z CANDIDATE (writer=REGISTRAR) | not persisted in this fixture evidence | [] | SELECT * FROM lifecycle_events ORDER BY global_sequence on file:C:/tmp/P014_RO_20260914/fixture-ledger.sqlite?mode=ro |

Q-A event_counts_per_state:
command: SELECT json_extract(canonical_event, '$.next_state') AS next_state, COUNT(*) FROM lifecycle_events GROUP BY 1 on file:C:/tmp/P014_RO_20260914/fixture-ledger.sqlite?mode=ro
- CANDIDATE: 1
- CAPTURED: 1
- TRIAGED: 1

Q-A unresolved_lifecycle_contracts JSON snapshot (older demo run):
source: C:\tmp\P014_RO_20260914\fixture-status-report.json:88-92
- DEMOTED TARGET RUNG MAPPING: UNRESOLVED
- CHALLENGE INCUMBENT DEPLOYMENT IDENTITY FIELD: MISSING
- ATOMIC SUCCESSION PROMOTED ACROSS TWO CANDIDATES: UNRESOLVED

Q-A unresolved_lifecycle_contracts current reader source (_render_status_report; this is the current reader's list):
source: C:\tmp\P014_RO_20260914\p031_lifecycle_ledger.py:1259-1267
- DEMOTED TARGET RUNG MAPPING: UNRESOLVED
- CHALLENGE INCUMBENT DEPLOYMENT IDENTITY FIELD: MISSING
- ATOMIC SUCCESSION PROMOTED ACROSS TWO CANDIDATES: UNRESOLVED
- REJECTED FAILED-GATE PURPOSE: UNRESOLVED
- ADMISSION WITHHELD CAPACITY TARGET: UNRESOLVED
- DEPLOYMENT REFRESH ENVELOPE: UNRESOLVED
- EVALUATION RUN CANDIDATE SCOPE: UNRESOLVED
Q-A reader CLI: not executed from this directory; C:\tmp\P014_RO_20260914\p031_lifecycle_ledger.py:25 imports mtc_contracts (ModuleNotFoundError: No module named 'mtc_contracts')

# Q-B. Contract/type scan
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

Q-B public_type_count: 19
Q-B refusal_reasons: RESERVED_BOUNDARY_KEY
Q-B test_count: 29
Q-B test_count_basis: top-level def test_* via ast (file C:\tmp\P014_RO_20260914\test_trial_catalog_types.py); suite was not collected
Q-B parametrized_defs: test_t6_the_other_reserved_groups_are_refused_the_same_way:5@179, test_t18_shape_every_bound_boundary_member_refuses_at_parse_when_missing:6@195, test_b03_typed_companion_refuses_ambiguous_scalar_containers:3@622
Q-B pytest_collection_if_imported: 40 (not collected; mtc_contracts missing)
Q-B catalog_data_exists:
search: rglob of ['equity.parquet', 'intents.jsonl', 'levels.parquet', 'trades.parquet'] under C:\tmp\P013_CONTRACT_V2_20260912
- NONE FOUND

# Appendix
Q-A fixture inputs: C:\tmp\P014_RO_20260914\fixture-ledger.sqlite, C:\tmp\P014_RO_20260914\fixture-ledger.restored.sqlite, C:\tmp\P014_RO_20260914\fixture-ledger.backup.sqlite, C:\tmp\P014_RO_20260914\fixture-status-report.json
Q-B test file: C:\tmp\P014_RO_20260914\test_trial_catalog_types.py
P0-31 scope/status source: C:\tmp\P014_RO_20260914\P031_M1_SCOPE_AND_STATUS.md
P0-31 ledger reader source: C:\tmp\P014_RO_20260914\p031_lifecycle_ledger.py
```

## NOT VERIFIED

- Fixture data only; no live candidates; no catalog writer targets (`trades.parquet` / `equity.parquet` / `intents.jsonl` / `levels.parquet` NONE FOUND under `C:/tmp/P013_CONTRACT_V2_20260912`); nothing accepted; no Explorer.
- Copied `p031_lifecycle_ledger.py report` could not be executed: `ModuleNotFoundError: No module named 'mtc_contracts'` (import at `C:/tmp/P014_RO_20260914/p031_lifecycle_ledger.py:25`). The seven-item unresolved list is source text, not a printed report for this fixture.
- Pytest was not collected or run. 29 is the `def test_*` count only. Collection would be 40 if imported.
- Worktree HEADs quoted in TASK.md were not verified (git forbidden).
- Nothing in this report is a decision, acceptance, or authorization.
