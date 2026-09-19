# WP-P0-13 dependency and adoption map — RECORDED 2026-09-13 (preparation artifact; no authority)

Prepared 2026-09-13 by an independent analyst lane (`claude-opus-5`, xhigh) from read-only
inspection of the frozen P013 contract head, the takeover handoffs, the P013 Lead decision
packet and verification record, the master work-package plan, and the P020 / P022 / P031
worktrees.

**This document is analysis only.** It is not authority, acceptance, ratification, a schema
change, or permission to start any writer, pipeline, publication, adoption or integration
work. Every classification below is a reading of cited bytes, not a decision. The Lead audits
every citation. No recommendation to start implementation appears anywhere in this document.

---

## 1. Identity check

### 1.1 Head and cleanliness

| Check | Command | Observed | Required by BRIEF | Verdict |
|---|---|---|---|---|
| Head | `git rev-parse HEAD` in `C:/tmp/P013_CONTRACT_V2_20260912` | `da1fb184c71e1ae65e2e348758af7f1a84a1cfbd` | `da1fb184c71e1ae65e2e348758af7f1a84a1cfbd` | MATCH |
| Working tree | `git status --porcelain` | empty (zero lines) | empty | MATCH |
| Branch | `git rev-parse --abbrev-ref HEAD` | `feature/p013-contract-v2-20260912` | `feature/p013-contract-v2-20260912` | MATCH |
| Base resolves | `git diff --stat a4e79fbe..HEAD` | resolves against `a4e79fbeb2365c7a4e876ca4f7447d9032851d23` | same | MATCH |
| Changed-path count | `git diff --name-only a4e79fbe..HEAD` | 15 | 15 | MATCH |
| Aggregate diff | `git diff --stat a4e79fbe..HEAD` | `15 files changed, 1917 insertions(+), 107 deletions(-)` | — | recorded |
| Forward commits | `git rev-list --count a4e79fbe..HEAD` | 14 | 14 (`P013_HANDOFF.md:14`) | MATCH |
| Approval trailers | `git log --format=%B a4e79fbe..HEAD \| grep -c "APPROVED-PATCH-PLAN: WP-P0-13-CONTRACT-V2-20260912"` | 14 | "every commit carrying" (`P013_HANDOFF.md:14-15`) | MATCH (14 of 14) |

No STOP condition on identity was reached.

**Position relative to integrated master.** `git merge-base fcac0ac6 HEAD` is
`42f99571e6abb5222744d9345e1c8a9e19c23c15`; `git rev-list --left-right --count
fcac0ac6...HEAD` is `51 16`. The branch is therefore 51 behind and 16 ahead of
`fcac0ac67cf2682693ad28138b1a56e15a0846f2`, and the accepted base `a4e79fbe` is itself two
commits ahead of the merge-base, not equal to it. That is consistent with the handoff, which
states no push, PR, merge or master integration is authorized
(`C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:52-53`).

### 1.2 The 15 changed paths with blob OIDs at HEAD

All OIDs from `git ls-tree -r HEAD --format='%(objectname) %(objectsize) %(path)'` at
`da1fb184`. Sizes are the tree-recorded blob byte sizes.

| # | Path (repo-relative) | Blob OID at HEAD | Bytes |
|---|---|---|---|
| 1 | `DECISIONS.md` | `3c7d0d0ba47c3742945089d0516af4ea47bcea36` | 28918 |
| 2 | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/test_trial_catalog_acceptance_reader.py` | `3949cc312c9ce3fa11592e301d90b1d025c13c13` | 19274 |
| 3 | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/test_trial_catalog_stages.py` | `b99729e38124c19389ef8fce52e9d830a5f2c523` | 19757 |
| 4 | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/__init__.py` | `cf3b7ec6fdd78a8a98bb0ea7890989b6e090b509` | 1192 |
| 5 | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py` | `5b2e213da49161f7c63b4b0993bc0577d9bba773` | 12905 |
| 6 | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py` | `381bd6659cef619a742ddc28dd870775f3232f61` | 22932 |
| 7 | `MTC_COMMAND_CENTER/02_TASKS/TASK_HISTORY.json` | `ea319ec7dffe5731988a12a443c4f7fa4e1100c8` | 47396 |
| 8 | `MTC_COMMAND_CENTER/contracts/CHANGELOG.md` | `922b15395395381c799d53c8dad0d32a1e649055` | 3367 |
| 9 | `MTC_COMMAND_CENTER/contracts/README.md` | `9172e59297f9f869790c7306c49205a194d40b79` | 5012 |
| 10 | `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py` | `1e9682ba057d407e4d786a66a935a77244089f72` | 22853 |
| 11 | `MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py` | `7dec1e1c8bc1fc4082285b9dd3d340cfb3f8d17c` | 18415 |
| 12 | `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py` | `94735265de678e9dd2808a9e8ae414e136a3a75a` | 2890 |
| 13 | `MTC_COMMAND_CENTER/contracts/tests/test_identity.py` | `9a0d2cab8a8b97f846ce54d6b19d0f59cb25f230` | 24468 |
| 14 | `MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py` | `450ffd52808cb334e49cd3f103e728a46a74e48f` | 24505 |
| 15 | `MTC_COMMAND_CENTER/contracts/tests/test_trials_and_eligibility.py` | `79a100297d68e431e409895dfa3bc539889dd122` | 5413 |

Note on tooling: `git diff --stat` abbreviates the five `01_MTC_PROJECT` paths with an
ellipsis. The full names above come from `git diff --name-only`, which does not abbreviate.
A reader who takes the `--stat` spellings literally will not find those files.

### 1.3 Identity facts this lane did NOT re-verify

The handoff and verification record also pin an aggregate diff Git object
`a38248a967d5f9838bf19c13ef4fba8b79f71965` and a raw diff SHA-256
`46089d3fca63ee263e7389ebe87f360f0303af720bd86742ab315dd1a50ed5b2`
(`C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:12-13`;
`C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md:16-19`). Recomputing them was not
part of this lane's brief and was not done. See section 6.

---

## 2. Contract inventory

One row per ratified contract at `da1fb184`. "Owner decision id" cites the binding record.
Both owner rows exist **only on this branch**; see section 3.6.

| Contract | Definition file:line | Version literal | Owner decision id | What it fixes |
|---|---|---|---|---|
| Finite-only canonical serializer (F3) | `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:43-46`, `:54-63` | none (function contract) | `OD-20260912-P013-CONTRACTS` | `_json_value` raises `non-finite Decimal values are not canonical JSON`; `canonical_json` uses `sort_keys=True`, `separators=(",", ":")`, `ensure_ascii=False`, `allow_nan=False`. Finite bytes and hashes unchanged. |
| Parameter-only V1 lowering grammar | `identity.py:122-131`, `:134-137`, `:140-156` | V1, bound to `ParamHashPreimageV1` | `OD-20260913-P013-CONTRACT-DEFAULTS` | `lower_parameters` renders each finite `Decimal` as an uppercase-`E` JSON number preserving exact coefficient and exponent. Explicitly does not change shared `canonical_json` bytes (`MTC_COMMAND_CENTER/contracts/README.md:57-64`). |
| `ParamHashPreimageV1` (B-04) | `identity.py:218-232` | `param_preimage_version: Literal["1"]` (`:225`) | `OD-20260912-P013-CONTRACTS` | Exactly two declared members: `param_preimage_version`, `parameters_canonical_json`. Sole digest `compute_param_hash` at `identity.py:249-254`. |
| `SearchRegime` | `identity.py:257-260` | none | `OD-20260912-P013-CONTRACTS` (B-12) | Closed three-value regime vocabulary `grid` / `tpe` / `random`. |
| `SimulatorClass` (B-05) | `identity.py:263-265` | none | `OD-20260912-P013-CONTRACTS` | Closed two-value lineage vocabulary `SIGNAL_SCREEN_ONLY` / `FULL_KERNEL_SIMULATION`. |
| `RegisteredParameterDefinition` | `identity.py:271-336` | none (member of the V1 space) | `OD-20260912-P013-CONTRACTS` (B-12) | One closed integer range, float range, or typed categorical domain; unambiguity validator at `:282-336`. |
| `PreregisteredSpacePreimageV1` (B-12) | `identity.py:339-388` | `space_preimage_version: Literal["1"]` (`:340`) | `OD-20260912-P013-CONTRACTS`; budget type by `OD-20260913-P013-CONTRACT-DEFAULTS` | Seven declared members including `strategy_type`, `search_regime`, complete typed `parameter_definitions`, and `adaptive_trial_budget: Annotated[StrictInt, Field(gt=0)]` (`:345`). Canonicaliser `project_preregistered_space` at `:423-478`; sole digest `compute_preregistered_space_hash` at `:481-486`. |
| `LegacyScreenDeploymentPreimageV1` (B-08) | `identity.py:489-502` | `preimage_version: Literal["1"]` (`:490`) | `OD-20260912-P013-CONTRACTS` | Seven declared members; `simulator_class: Literal["SIGNAL_SCREEN_ONLY"]` (`:496`) so a screening digest cannot spell full-kernel. Separate digest `compute_legacy_screen_deployment_identity` at `:505-512`. |
| `TrialRecord` 48-field row (B-03) | `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:14-74` | inherited `contract_version` `0.1.0` (`MTC_COMMAND_CENTER/contracts/README.md:18-19`) | `OD-20260912-P013-CONTRACTS` | Field count asserted at `MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:582`: `len(TrialRecord.model_fields) == 48`. `parameters: dict[str, Any]` at `trials.py:31`; no `strategy` / `symbol` / `timeframe` row fields. |
| 53-column base view (B-03) | asserted at `test_trial_catalog_types.py:373`, `:583` | `PublishedViewSchemaDocumentV1.document_version: Literal["1"] = "1"` (`trial_catalog.py:492`) | `OD-20260912-P013-CONTRACTS` | `len(document.columns) == 53`; `len(TOP_LEVEL_CELLS) == 48` at `test_trial_catalog_types.py:368`. |
| Typed parameter companion columns (B-03) | `MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:411-462` | none | `OD-20260912-P013-CONTRACTS` | Deterministic `p__<percent-encoded name>` columns, ordered by raw UTF-8 name, Arrow type derived from the registered definition, always `nullable=True`; name collision refuses at `:456-457`. |
| `ArtifactManifest` V2 (B-09 / D-04) | `trials.py:77-91` | `artifact_manifest_version: Literal["2"]` (`:78`) | `OD-20260912-P013-CONTRACTS` | Adds required `trial_id` (`:80`) and `param_hash` (`:81`) so a manifest carries per-trial identity. Version-`"1"` refusal asserted at `MTC_COMMAND_CENTER/contracts/tests/test_trials_and_eligibility.py:148`. |
| Writer-boundary refusal and reserved keys (F-2) | `trial_catalog.py:72-114`, `:212-219` | none | `OD-20260912-P013-CONTRACTS` | Single typed reason `RESERVED_BOUNDARY_KEY`; an 18-name `RESERVED_BOUNDARY_KEYS` frozenset refused before any field conversion. |
| `CompletedRunInput` closed boundary | `trial_catalog.py:195-219` | inherited `contract_version` | `OD-20260912-P013-CONTRACTS` | Six required members, `extra="forbid"`, reserved-key pre-validator. |
| `ProvisionalBoundaryPayload` | `trial_catalog.py:122-134` | `ratification_status: Literal["UNRATIFIED"] = "UNRATIFIED"` (`:133`) | `OD-20260912-P013-CONTRACTS` | Keeps an unratified boundary contract representable as pending rather than invented; `blocked_by` names the open blocker (used with `"B-01"` at `test_trial_catalog_types.py:127`, `:129`). |
| `LineageOriginReceipt` / `SinkCapabilityClass` / `WriterAdapterId` (B-05) | `trial_catalog.py:168-192` | none | `OD-20260912-P013-CONTRACTS` | Exactly two adapters and two capability classes; `canonical_path_receipt_hash` optional and absent by design for screening. |
| `RunCellDimensionsReceiptV1` (B-17) | `trial_catalog.py:222-238` | `receipt_version: Literal["1"]` (`:229`) | `OD-20260912-P013-CONTRACTS` | Digest-bound coordinate receipt shape. The docstring states `No factory in this slice produces one` (`:223`). Compatibility alias `RunCellDimensionsReceipt` at `:238`. |
| `RunEnvelopeV1` (commit preimage item 2) | `trial_catalog.py:246-275` | inherited `contract_version`, the seventh serialized member, stated at `:247` and `:15-19` | `OD-20260912-P013-CONTRACTS` | Six declared members exactly matching the six arguments of `compute_evaluation_run_hash`; declared-member tuple at `:268-275`. |
| `_CatalogCommitPreimageV1` | `trial_catalog.py:310-328` | `preimage_version: Literal["1"]` (`:324`) | `OD-20260912-P013-CONTRACTS` | Unchanged V1 with four operands. Its own docstring at `:316-321` states the `Literal["1"]` choice is an unratified analogy and is reported as one. |
| `_CatalogCommitPreimageV2` (B-17) | `trial_catalog.py:331-339` | `preimage_version: Literal["2"]` (`:334`) | `OD-20260912-P013-CONTRACTS` | V1's four operands plus `run_cell_dimensions_receipt_sha256` as the digest binding. |
| View schema document and type vocabulary | `trial_catalog.py:348-359`, `:398-408`, `:465-493` | `document_version: Literal["1"] = "1"` (`:492`) | `OD-20260912-P013-CONTRACTS` | Closed eight-word physical type vocabulary; collapse rule at `:368-390`; the one nested entry is a separate type at `:465-481`. |
| Reader taxonomy V2 (D-05) | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:44`, `:47-70` | `ACCEPTANCE_READER_REFUSAL_TAXONOMY_VERSION = "2"` (`:44`) | `OD-20260912-P013-CONTRACTS` | Closed nine reasons; adds `COMMIT_RECEIPT_STRUCTURE_INVALID` (`:63`) while preserving `COMMIT_PREIMAGE_MEMBER_MISSING` (`:62`) and `COMMIT_HASH_MISMATCH` (`:64`). Version asserted at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/test_trial_catalog_acceptance_reader.py:486`. |
| Non-`ACCEPTED` reader outcome | `acceptance_reader.py:84-91` | none | `OD-20260912-P013-CONTRACTS` | The strongest non-refusal outcome is `PARSE_AND_REHASH_OK`; `ACCEPTED` is deliberately unspellable in this slice. |
| Stage refusal taxonomy (write side) | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:59-81` | none | `OD-20260912-P013-CONTRACTS` | Twelve typed write-side reasons, deliberately disjoint from the reader taxonomy (`:61-65`), including `FULL_LINEAGE_WAIT_P020_ACCEPTANCE` (`:73`) and `IDENTITY_PRODUCER_ADOPTION_UNAVAILABLE` (`:79`). |
| Conservation trio and seal | `stages_conservation_identity.py:124-153`, `:156-328` | none | `OD-20260912-P013-CONTRACTS` | Sole expected producer, sole observed producer, and a comparer owning neither operand; receipts minted only under a module-private seal. |
| `LineageClassifier` lock | `stages_conservation_identity.py:331-341`, `:414-436` | none | `OD-20260912-P013-CONTRACTS` | `FULL_EVIDENCE_SINK` always refuses today: legacy adapter gives `LEGACY_ADAPTER_CANNOT_REQUEST_FULL_SINK` (`:419-423`), otherwise `FULL_LINEAGE_WAIT_P020_ACCEPTANCE` (`:424-428`). Only `SIGNAL_SCREEN_ONLY` is mintable (`:434`). |
| `IdentityValidator` truthful refusals | `stages_conservation_identity.py:489-534` | none | `OD-20260912-P013-CONTRACTS` | `validate_param_hash` (`:520-526`) and `validate_preregistered_space_hash` (`:528-534`) both refuse with `IDENTITY_PRODUCER_ADOPTION_UNAVAILABLE`: the preimages are ratified, but no producer adoption exists in this stage. |

### 2.1 The two owner decision records and the protected-path approval

- `OD-20260912-P013-CONTRACTS` — `DECISIONS.md:24` (P013 branch). Names the approved choices
  F3, D-05, B-03, B-04, B-12, B-17, B-09/D-04 and B-05/B-08, and states the exclusions
  verbatim: *"Excluded are the full writer, selection/artifact pipeline, reader adoption
  beyond D-05, caller integration, P020 acceptance, push/PR/merge,
  host/credentials/trading/deploy."*
- `OD-20260913-P013-CONTRACT-DEFAULTS` — `DECISIONS.md:23` (P013 branch). Ratifies the
  uppercase-E parameter grammar and `adaptive_trial_budget` as `StrictInt > 0`, and states:
  *"This adds no full writer, pipeline, receipt production/adoption, reader/caller
  integration, P020 or full P013 acceptance, push/PR/merge, host, credential, trading,
  deployment, or paid-usage authority."*
- Protected-path approval `HIST-2026-0044` / task `WP-P0-13-CONTRACT-V2-20260912` — added to
  `MTC_COMMAND_CENTER/02_TASKS/TASK_HISTORY.json` by this branch, alongside a second event
  `HIST-2026-0045` / task `WP-P0-13-CONTRACT-DEFAULTS-20260913`. The handoff and the
  verification record name only `HIST-2026-0044`
  (`C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:22`;
  `C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md:11`). `HIST-2026-0045` exists in
  the committed JSON but is cited by neither. See section 6.
- `DECISIONS.md:16-17` (P013 branch) records that decisions 128 and 88 are preserved as
  summarized in `C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:11-12`, and
  that *"Their underlying earlier records are not repository-resident"*.

---

## 3. Adoption map

### 3.0 Method and the one fact that governs every row

Greps run inside the frozen P013 worktree (`rg -n --word-regexp <symbol> --glob '!.git'`,
plus `rg -n --type py "from mtc_contracts|import mtc_contracts" -l`), then repeated in
`C:/P020_IMPL_20260912` (HEAD `b9b72f858dc830a9389517f79da5ea3c1fa6122c`),
`C:/tmp/P031_M1_20260913` (HEAD `c76043b92c70c9f79a6d06630c0896ebe73e68a1`) and
`C:/CT13` (HEAD `51fc2437f84061e0e164ff7965e036a143167003`).

**Governing fact: the ratified contract bytes exist on the P013 branch only.**

| Path | Blob at P013 `da1fb184` | Blob at `C:/CT13` HEAD | Blob at P020 `b9b72f85` | Blob at P031 `c76043b9` |
|---|---|---|---|---|
| `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py` | `94735265de678e9dd2808a9e8ae414e136a3a75a` | `a6a5758e125505d6a93d24d2fecddb517b1c0710` | `a6a5758e125505d6a93d24d2fecddb517b1c0710` | `a6a5758e125505d6a93d24d2fecddb517b1c0710` |
| `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py` | `1e9682ba057d407e4d786a66a935a77244089f72` | `75289fa6a83bab87ed6420732624656778da0163` | `fa57a77176b267e08436e03a0c3bfd371e054ba7` | `75289fa6a83bab87ed6420732624656778da0163` |
| `MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py` | `7dec1e1c8bc1fc4082285b9dd3d340cfb3f8d17c` | **absent** (`git cat-file -e HEAD:...` returns `fatal: path ... does not exist in 'HEAD'`) | absent | absent |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/` | 3 modules plus 2 test files | **absent** (`git ls-tree HEAD ...trial_catalog/` returns nothing) | absent | absent |

Consequence: at `C:/CT13`, `C:/P020_IMPL_20260912` and `C:/tmp/P031_M1_20260913` the
pre-V2 `ArtifactManifest` is still in force. It has no `artifact_manifest_version`, no
`trial_id` and no `param_hash`
(`C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:77-89`).
No package outside the P013 branch can adopt a contract whose bytes it does not have.

A second structural limiter: `MTC_COMMAND_CENTER/contracts/mtc_contracts/__init__.py` is
**not** among the 15 changed paths. Its identity re-export block at `:28-37` still lists only
`canonical_json`, `compute_deployment_identity_hash`, `compute_evaluation_run_hash`,
`compute_family_id`, `compute_package_hash`, `make_candidate_id`, `make_run_id` and
`make_trial_id`. None of `ParamHashPreimageV1`, `compute_param_hash`,
`PreregisteredSpacePreimageV1`, `project_preregistered_space`,
`compute_preregistered_space_hash`, `LegacyScreenDeploymentPreimageV1`,
`compute_legacy_screen_deployment_identity`, `RegisteredParameterDefinition`,
`SearchRegime` or `SimulatorClass` is re-exported from the package root, and the whole
`mtc_contracts.trial_catalog` module is reachable only by explicit submodule import, as the
tests do at `MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:15`, `:21`.

Status vocabulary used below:

- **ADOPTED** — a non-test production module produces or consumes the contract.
- **PARTIAL** — a production module consumes the type, but the behaviour it gates is refused
  or unreachable today.
- **NOT_ADOPTED** — a named intended producer or consumer exists and does not use it.
- **NO_CONSUMER_YET** — no producer or consumer exists anywhere except the contract's own
  focused tests.

### 3.1 Per-contract adoption

| Contract | Producers today (file:line) | Consumers today (file:line) | Status |
|---|---|---|---|
| `canonical_json` finite-only (F3) | `identity.py:54-63` | `identity.py:246`, `:326`, `:358`, `:401`, `:516`, `:521`; recipe cited at `trial_catalog.py:10-13`; `acceptance_reader.py:30`, `:240`, `:293` | **ADOPTED** inside the shared contracts package and the bounded reader; no external caller |
| `lower_parameters` V1 grammar | `identity.py:122-131` | none outside `identity.py` itself and `MTC_COMMAND_CENTER/contracts/tests/test_identity.py` | **NO_CONSUMER_YET** |
| `ParamHashPreimageV1` / `compute_param_hash` (B-04) | `identity.py:218-232`, `:249-254` | `test_identity.py:20`, `:25`, `:171-378` only. The production path refuses at `stages_conservation_identity.py:520-526` with `IDENTITY_PRODUCER_ADOPTION_UNAVAILABLE` | **NO_CONSUMER_YET**; the refusal is explicit, not accidental |
| `PreregisteredSpacePreimageV1` / `project_preregistered_space` / `compute_preregistered_space_hash` (B-12) | `identity.py:339-388`, `:423-478`, `:481-486` | `test_identity.py:26`, `:28`, `:386-615` only. The production path refuses at `stages_conservation_identity.py:528-534` | **NO_CONSUMER_YET** |
| `RegisteredParameterDefinition` | `identity.py:271-336` | `identity.py:343`, `:391-404`; `trial_catalog.py:37`, `:412`, `:422`, `:427`; tests `test_identity.py:21`, `test_trial_catalog_types.py:18` | **PARTIAL** — consumed only by the companion-column projector, which nothing calls in production |
| `LegacyScreenDeploymentPreimageV1` / `compute_legacy_screen_deployment_identity` (B-08) | `identity.py:489-502`, `:505-512` | `test_identity.py:19`, `:24`, `:626-720` only | **NO_CONSUMER_YET** |
| `SimulatorClass` / `SearchRegime` vocabulary (B-05, B-12) | `identity.py:263-265`, `:257-260` | `identity.py:342`, `:426`, `:473`; tests `test_identity.py:22-23`. String twins re-declared, not imported, at `stages_conservation_identity.py:55-56` | **PARTIAL** — the bounded stage declares its own `SIGNAL_SCREEN_ONLY` / `FULL_KERNEL_SIMULATION` string constants rather than importing the enum; see section 6 |
| `TrialRecord` 48-field row (B-03) | `trials.py:14-74` | `MTC_COMMAND_CENTER/contracts/mtc_contracts/__init__.py:74`, `:126`; tests `test_trials_and_eligibility.py:10`, `:28`; `test_deep_immutability.py:12`, `:85`; `test_trial_catalog_types.py:40`, `:582`. Explicitly not assembled: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/__init__.py:7`; `stages_conservation_identity.py:5` | **NO_CONSUMER_YET** — no row assembler exists in any inspected worktree |
| 53-column base view and companion columns (B-03) | `trial_catalog.py:411-462`, `:484-493` | `test_trial_catalog_types.py:368`, `:373`, `:555-667` only | **NO_CONSUMER_YET** |
| `ArtifactManifest` V2 (B-09 / D-04) | `trials.py:77-91` | `__init__.py:74`, `:85`; tests `test_trials_and_eligibility.py:5`, `:105`, `:120-148` only | **NO_CONSUMER_YET** on-branch; **NOT_ADOPTED** at `C:/CT13`, P020 and P031, which all still carry blob `a6a5758e...` |
| Reserved boundary keys / `ReservedBoundaryKeyRefusal` (F-2) | `trial_catalog.py:78-87`, `:93-114`, `:212-219` | `trial_catalog.py:195-219` (`CompletedRunInput`); tests in `test_trial_catalog_types.py` | **PARTIAL** — live inside the closed boundary type; no production caller constructs `CompletedRunInput` |
| `CompletedRunInput` | `trial_catalog.py:195-219` | `stages_conservation_identity.py:30`, `:213`, `:215-219` (`CompletedRunTrialUniverseProjector.project`) | **PARTIAL** — a real consumer exists, but its only caller is the focused test suite |
| `ProvisionalBoundaryPayload` | `trial_catalog.py:122-134` | `trial_catalog.py:206-208` (three `CompletedRunInput` members); `blocked_by="B-01"` used at `test_trial_catalog_types.py:127`, `:129` and `test_trial_catalog_stages.py:54`, `:56` | **PARTIAL** — this is the mechanism keeping B-01 and B-07 blocked members representable as pending |
| `LineageOriginReceipt` / `WriterAdapterId` / `SinkCapabilityClass` (B-05) | `trial_catalog.py:168-192` | `stages_conservation_identity.py:29-35`, `:414-436` (`LineageClassifier.lock`) | **PARTIAL** — only `SIGNAL_SCREEN_ONLY` is reachable; `FULL_EVIDENCE_SINK` always refuses at `:417-428` |
| `RunCellDimensionsReceiptV1` (B-17) | `trial_catalog.py:222-238`; docstring states `No factory in this slice produces one` (`:223`) | `trial_catalog.py:339` (digest member of the V2 preimage); tests `test_trial_catalog_types.py:30`, `:483-542` | **NO_CONSUMER_YET** |
| `RunEnvelopeV1` | `trial_catalog.py:246-275` | `stages_conservation_identity.py:33`, `:358-374` (`build_envelope`), `:376-390` (`compute`), `:505-518` (`validate_evaluation_run_hash`) | **PARTIAL** — genuinely consumed by the bounded stage, but no production caller feeds it |
| `_CatalogCommitPreimageV1` | `trial_catalog.py:310-328` | `acceptance_reader.py:31`, `:189`, `:249-251` | **PARTIAL** — the read side is real; nothing writes a commit receipt |
| `_CatalogCommitPreimageV2` (B-17) | `trial_catalog.py:331-339` | `test_trial_catalog_types.py:491`, `:542` only. The acceptance reader still parses **V1** (`acceptance_reader.py:31`) | **NO_CONSUMER_YET**; the V2-written / V1-read gap is a stated slice boundary, carried into section 4 |
| Reader taxonomy V2 (D-05) | `acceptance_reader.py:44`, `:47-70` | `acceptance_reader.py:204-272`, `:292-298`; tests `test_trial_catalog_acceptance_reader.py:25`, `:485-486` | **PARTIAL** — only 3 of the 9 reasons are emittable here, stated at `acceptance_reader.py:55-60` |
| Stage refusal taxonomy | `stages_conservation_identity.py:59-81` | same module at `:113-121`, `:234-238`, `:252-316`, `:419-433`, `:440-463`, `:513-534` | **PARTIAL** — `REFUSED_PREIMAGE_NOT_RATIFIED` is declared an enum-only, non-emitted compatibility token (`:80-81`) |
| Conservation trio and seal | `stages_conservation_identity.py:124-153`, `:156-328` | same module; tests `test_trial_catalog_stages.py:11`, `:26` | **PARTIAL** |

### 3.2 WP-P0-20 — explicit

| Question | Evidence | Answer |
|---|---|---|
| Does P020 code import the shared contracts package? | `rg -n --type py "from mtc_contracts\|import mtc_contracts" -l` in `C:/P020_IMPL_20260912` returns `p020_simulator.py`, `p020_owner_policy.py`, `statistical_battery.py`, `portfolio_simulator.py`, `research_verification/p020/test_owner_policy.py`, `research_verification/p020/test_execution_proofs.py`, `unsimulated_controls.py`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/p020_economics.py`, plus the contracts package's own tests | Yes, but against its own diverged `identity.py` blob `fa57a771...`, not the P013 ratified bytes |
| Does P020 reference any ratified P013 symbol? | Word-boundary grep for `TrialRecord`, `ArtifactManifest`, `ParamHashPreimageV1`, `PreregisteredSpacePreimageV1`, `LegacyScreenDeploymentPreimageV1`, `SimulatorClass`, `trial_catalog`, `canonical_path_receipt` in `C:/P020_IMPL_20260912`: the only code hits are `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:1`, `:14`, `:71`, `:77` and `MTC_COMMAND_CENTER/contracts/mtc_contracts/__init__.py:74`, `:85`, `:126` — the pre-V2 contract's own definition and re-export. Every other hit is planning prose under `11_TRIAGE` | **NOT_ADOPTED** |
| Does P020 publish the B-01 seam the decision packet proposes? | `rg -n "P020AcceptedCatalogueDependencyV1\|P020CanonicalPathReceiptVerifier\|P020VerifiedCanonicalPathResult\|canonical_path_receipt\|TrialRejectionTaxonomyV1\|FullEvidenceSinkCapability"` across `C:/P020_IMPL_20260912` returns **zero matches** | None of the proposed B-01 artifacts exists |

### 3.3 WP-P0-22 — explicit

`C:/CT13/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p022_research_tracker.py` (772 lines) imports
`argparse`, `datetime`, `hashlib`, `json`, `os`, `pathlib.Path`, `re`, `sqlite3`, `sys`,
`unicodedata` and `typing` at `:8-20`. It imports nothing from `mtc_contracts`, and a
word-boundary grep for `TrialRecord`, `ArtifactManifest`, `PreregisteredSpacePreimageV1`,
`project_preregistered_space`, `compute_preregistered_space_hash`,
`RegisteredParameterDefinition`, `canonical_json`, `compute_param_hash` and `SimulatorClass`
in that file returns **zero matches**.

Status: **NOT_ADOPTED**. This matches the frozen P022 scope at
`C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/P022_RESEARCH_TRACKER_SCOPE.md:13`: *"P0-13 status at
start: no accepted/frozen consumable interface. This slice therefore uses synthetic fixtures
and opaque local references only. Real P0-13 integration remains blocked, without blocking
this milestone."* The same document states at `:41` that its stored `local_manifest_sha256`
*"is not a canonical P0-13/P0-22 identity"*, and at `:53` that *"P0-13 integration"* remains
future full-P0-22 work.

**Disagreement to record.** `OD-20260912-P013-CONTRACTS` (`DECISIONS.md:24` on the P013
branch) says the registered-space implementation is *"shared … with full P0-22"*, and the
decision packet says the *"Sole registry projector and sole hash function are shared with
P0-22"* (`C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:62`). No P022 code
shares it today. The sharing is a ratified intent, not an implemented fact, and P022's own
remaining-work list still requires *"an authorized canonical family resolver/interface"*
(`C:/tmp/CLAUDE_TAKEOVER_20260913/P022_HANDOFF.md:28`).

### 3.4 WP-P0-31 — explicit

`C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:25`
imports exactly `from mtc_contracts.execution import LifecycleEvent, LifecycleWriterClass`.
A word-boundary grep for `canonical_json`, `compute_package_hash`,
`compute_deployment_identity_hash`, `compute_evaluation_run_hash`, `make_trial_id`,
`make_run_id`, `compute_family_id` and `make_candidate_id` in that file returns **zero
matches**. A grep for `TrialRecord`, `ArtifactManifest`, `ParamHashPreimageV1`,
`PreregisteredSpacePreimageV1`, `LegacyScreenDeploymentPreimageV1`, `SimulatorClass`,
`AcceptanceReaderRefusalReason`, `CompletedRunInput` and `trial_catalog` across the whole
P031 worktree hits only the contracts package's own pre-V2 `trials.py` and planning prose.

Status: **NOT_ADOPTED**, and P031 says so itself.
`C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:105` lists *"exact accepted WP-P0-13
TrialRecord/catalog provenance actually consumed by P031"* as an open Milestone 1
requirement, and `:118-121` states that the `da1fb184` notice *"grants no caller
integration/full-P013 acceptance and is not in this candidate. Do not infer dependency
satisfaction."*

### 3.5 `MTC_COMMAND_CENTER/contracts/` — explicit

Every ratified contract lives here, and every consumer of the new symbols is either the
contracts package's own focused tests or one of the two bounded P013 slice modules
(`stages_conservation_identity.py`, `acceptance_reader.py`). There is no third consumer in
any inspected worktree. The one shared file that a different package also edits is
`identity.py`; see section 5.

### 3.6 Governance-record adoption

| Record | On the P013 branch | At `C:/CT13` HEAD `51fc2437` | Status |
|---|---|---|---|
| `OD-20260912-P013-CONTRACTS` | `DECISIONS.md:24` | absent — `grep -ni "p013\|p0-13\|hist-2026-0044" DECISIONS.md` returns only `:79`, the takeover-priority note | **NOT_ADOPTED** in the control checkout |
| `OD-20260913-P013-CONTRACT-DEFAULTS` | `DECISIONS.md:23` | absent (same grep) | **NOT_ADOPTED** |
| `HIST-2026-0044`, `HIST-2026-0045` | added to `MTC_COMMAND_CENTER/02_TASKS/TASK_HISTORY.json` by this branch | absent — `grep -n "HIST-2026-0044\|HIST-2026-0045" MTC_COMMAND_CENTER/02_TASKS/TASK_HISTORY.json` returns nothing; the CT13 blob is `1ebd9d49f5eabcbf9619166d43f83b187b9fc09e`, byte-identical to the P013 **base** | **NOT_ADOPTED** |

This is consistent with the stated acceptance boundary, *"No push, PR, merge, or master
integration is authorized"*
(`C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md:82`). It does mean a reader of
`C:/CT13` alone would find no repository record that these contracts were ratified.

---

## 4. Dependency map for the remaining full-P013 work

### 4.0 Where "B-01" is defined, and its current acceptance status

The BRIEF asks where B-01 is defined. The answer is **not** in the WP-P0-20 plan section and
**not** in any P020 artifact.

- A standalone-token grep `rg -n --word-regexp "B-01"` across `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/`
  returns exactly two matches, both in an unrelated 2026-07-19 audit:
  `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/CODEX_TSP0_AUDIT_2026-07-19.md:124` (*"B-01 — MAJOR —
  valid JSON with wrong `hashes` shape crashes validation"*) and `:211`. Every other apparent
  hit in that directory is a substring of `WP-V2B-01`, `LB-01` or `WP-P0-28`.
- The same grep across `C:/P020_IMPL_20260912` returns only those same two audit lines.
- The only other CT13 occurrence is the takeover instruction itself,
  `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/START_HERE.md:42`
  (equivalently `C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md:42`): *"Remaining full work:
  accepted P020 B-01 interface dependency … The narrower P020 milestone is not automatically
  B-01."*

B-01 is a **WP-P0-13 design-draft blocker**, not a P020 deliverable label. Its definition is
at `C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1441`
under the heading *"### B-01 — `P020-ACCEPTANCE-AND-CANONICAL-RECEIPT`"*, inside
*"## 7. Named blockers — no defaults"* (`:1439`). Its controlling text is `:1445`:

> "WP-P0-13 build cannot begin until WP-P0-20 accepts, and the canonical receipt issuer/shape
> is not settled. … B-01 remains open on package acceptance itself, not on the historical
> paper verdicts. **PROVISIONAL-ON-P020** covers every full-kernel choice in this draft.
> Required resolution: accepted P0-20 artifacts plus a re-audit of this draft before build."

The same file lists B-01 among the open blockers at `:358` (*"11 open blockers are B-01,
B-03, B-04, B-05, B-06, B-07, B-08, B-09, B-12, B-15, B-17"*) and repeats the build gate at
`:310`, `:328`, `:1135`, `:1348`.

The decision packet restates it at
`C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:26-35`, and at `:208` says
plainly: *"B-01 cannot be signed closed; it waits for actual P020 acceptance."* The earlier
Lead map says the same: *"B-01 requires both accepted WP-P0-20 artifacts and a settled,
acceptance-bearing canonical-path receipt issuer/shape followed by a P013 design re-audit"*
(`C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md:7`), and pins the definition to
*"design lines 1441-1445"* at `:14`.

**Current acceptance status of the prerequisite: NOT SATISFIED.**

| Evidence | Citation |
|---|---|
| *"Acceptance remains intentional exit 1: 8/16 criteria MET / `NOT ACCEPTABLE`."* | `C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:30` |
| *"WP-P0-20 is therefore not package-accepted or merge-ready."* | `C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:51` |
| Eight named live blockers: `cost_admission`, `p012_full_acceptance`, `frozen_probe_compatibility`, `production_admission`, `real_before_after`, `dependent_disposition`, `real_benchmark`, `independent_reviews` | `C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:40-49` |
| *"Latest recorded full acceptance is 8/16 MET, NOT ACCEPTABLE."* | `C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md:34` |
| No canonical-receipt issuer, verifier, opaque result type, dependency bundle, rejection taxonomy or full-evidence capability exists in P020 code | zero grep matches in `C:/P020_IMPL_20260912`, section 3.2 |
| The P013 code itself encodes the open state | `stages_conservation_identity.py:424-428`: refusal text *"FULL_KERNEL_SIMULATION requires a verified canonical-path receipt from an accepted WP-P0-20; B-01 is open (WAIT_P020_ACCEPTANCE)"* |

**One stale citation to flag.** The earlier Lead map pins P020 at *"frozen research commit
`556639f59122e33b664ab918a4241eb96680219b`"*
(`C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md:7`, `:23`). The current verified
P020 head is `b9b72f858dc830a9389517f79da5ea3c1fa6122c`
(`C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:9`), confirmed by
`git rev-parse HEAD` in `C:/P020_IMPL_20260912`. The conclusion (`8/16 MET`,
`NOT ACCEPTABLE`) is unchanged between the two heads per `P020_HANDOFF.md:30`, but the commit
id in the 2026-09-12 map should not be quoted forward as current.

### 4.1 The other standing prerequisites, with current status

| Prerequisite | Definition citation | Status today | Evidence |
|---|---|---|---|
| **B-01** P020 acceptance and canonical receipt | `P013_DESIGN_DRAFT_V1.md:1441-1445` | **NOT SATISFIED** | section 4.0 |
| **B-04** `param_hash` preimage | `P013_DESIGN_DRAFT_V1.md:1451`; packet `:48-57` | Shape **RATIFIED** (`identity.py:218-232`, `:249-254`); **producer adoption NOT SATISFIED** | `stages_conservation_identity.py:520-526`: *"param_hash has a ratified B-04 preimage, but producer inputs and adoption are unavailable in this legacy stage; no value may be computed, defaulted, or accepted"* |
| **B-12** `preregistered_space_hash` preimage | packet `:59-68` | Shape **RATIFIED** (`identity.py:339-388`); **producer adoption NOT SATISFIED** | `stages_conservation_identity.py:528-534` (same refusal, `preregistered_space_hash`) |
| **B-15** run-cell coordinate channel | `P013_DESIGN_DRAFT_V1.md:1706-1716`; packet `:70-79` | **NOT SATISFIED** — `CompletedRunInput` still declares no cell-coordinate member | `trial_catalog.py:205-210` lists six members, none carrying `strategy` / `symbol` / `timeframe`; `trial_catalog.py:280-284`: *"While B-15 is open no component may derive a value for it"*; `P013_DESIGN_DRAFT_V1.md:310`: *"while B-15 is open no part path may be derived at all"* |
| **B-17** committed independent coordinate operand | `P013_DESIGN_DRAFT_V1.md:1734`; packet `:81-90` | Shape **RATIFIED** (`trial_catalog.py:222-238`, `:331-339`); **receipt production and reader adoption NOT SATISFIED** | `trial_catalog.py:223`: *"No factory in this slice produces one"*; `acceptance_reader.py:7-8`: *"the B-17 V2 coordinate-receipt shape is ratified, while R-8 receipt production and adoption remain outside this bounded slice"* |
| **B-07** selection and flag authorities | `P013_DESIGN_DRAFT_V1.md:1463-1468`; packet `:103-112` | **NOT SATISFIED** — owner half closed (decision 128), engineering half open | `P013_DESIGN_DRAFT_V1.md:1465-1466`: *"The owner half is decided; the engineering half remains open"*; packet `:112`: *"Engineering contract owners must freeze source/version/evidence identities"*; in code the member is a `ProvisionalBoundaryPayload` (`trial_catalog.py:207`) |
| **B-06** trial rejection taxonomy values | packet `:125-134` | **NOT SATISFIED** | packet `:208`: *"B-06 values wait for P020's accepted taxonomy"*; zero `TrialRejectionTaxonomyV1` matches in P020 |
| **View-preimage base-class / member-count ratification** (GM66-F01; B-16 deliberately not opened) | `trial_catalog.py:20-24` | **NOT SATISFIED** | *"the design records that base-class/member-count question as still open for the view preimage (GM66-F01, B-16 deliberately not opened), so the absolute digest values these helpers produce are PROVISIONAL on that ratification"* |
| **`_CatalogCommitPreimageV1.preimage_version` literal** | `trial_catalog.py:316-321` | **SELF-DECLARED UNRATIFIED** | *"This analogy is an unratified choice and is reported as one."* |
| **Plan-level dependency on WP-P0-20** | `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:411`, `:413`, `:414` | **NOT SATISFIED** | `:414`: *"The catalog is the evidence surface; it is written against the migrated canonical path or its rows are not acceptance-bearing."* `:506`: *"WP-P0-13 now depends on it outright"* |
| **Authorization scope for anything beyond the bounded slice** | `DECISIONS.md:23`, `:24` | **NOT SATISFIED** | `DECISIONS.md:24`: *"Excluded are the full writer, selection/artifact pipeline, reader adoption beyond D-05, caller integration, P020 acceptance, push/PR/merge, host/credentials/trading/deploy."* |

### 4.2 Remaining-deliverable dependency table

Classifications: **READY_NOW**, **BLOCKED_ON_P020_B01**, **BLOCKED_ON_OWNER**,
**BLOCKED_ON_OTHER (named)**. Where more than one blocker applies, the governing one is given
first and the rest are named. "Bounded independent preparation" describes what is
*technically* possible against already-ratified contracts; it does **not** assert that any of
it is authorized, and `DECISIONS.md:24` currently excludes all of it.

| # | Remaining deliverable | Exact prerequisite(s) with citation | Satisfied today? | Classification | Bounded independent preparation possible without the prerequisite | Risk of rework |
|---|---|---|---|---|---|---|
| 1 | **Catalog writer / `TrialRecord` row assembly** | B-04 producer adoption (`stages_conservation_identity.py:520-526`); B-12 producer adoption (`:528-534`); B-15 coordinate channel (`P013_DESIGN_DRAFT_V1.md:1706-1716`); B-01 for any non-screening lineage (`:1441-1445`); B-06 for `rejection_reasons` values (packet `:208`) | **NOT SATISFIED** on all five. Quoted refusals in section 4.1. `trial_catalog/__init__.py:7-12`: *"Not built here: `TrialRecord` assembly … B-15, B-07, and WP-P0-20 acceptance (B-01) remain prerequisites, so this package stays fail-closed."* | **BLOCKED_ON_OTHER (B-15 coordinate channel and B-04/B-12 producer adoption)**, additionally **BLOCKED_ON_P020_B01** for any row that is not `SIGNAL_SCREEN_ONLY` | Design-only: a written assembler interface sketch naming only already-ratified types. Fixture-only: `TrialRecord` construction fixtures already exist at `test_trials_and_eligibility.py:28` and `test_deep_immutability.py:85` and can be extended without a producer. | **HIGH.** Two of the 48 required fields (`param_hash`, `preregistered_space_hash`) have no emittable value, so any assembler written now must be rewritten once producers exist. `P013_DESIGN_DRAFT_V1.md:310` states B-04 and B-12 *"still leave two required non-null `TrialRecord` identities with no emittable value, so no row may be assembled"*. |
| 2 | **Selection pipeline** (`trial_catalog/stages_selection_artifacts.py`) | Packet's write-package row, `P013_CONTRACT_DECISION_PACKET_V2.md:190`: entry condition *"B-07/B-09 and owner expansion"*, stop condition *"Missing lifecycle/pin or accepted policy evidence"*. B-07 mechanism at packet `:107` requires opaque receipts minted by a strategy-type registry owner, by P020 and by P021 | **NOT SATISFIED.** B-09 shape is ratified (`trials.py:77-91`) but B-07 is not: no `SelectionPolicyV1`, `StrategyTypeRegistryProjector` or `VerifiedStrategyTypeReceipt` exists in any inspected worktree, and the boundary member is still a `ProvisionalBoundaryPayload` (`trial_catalog.py:207`) | **BLOCKED_ON_OWNER** (packet `:112`: engineering contract owners must freeze source/version/evidence identities; plus *"owner expansion"* at `:190`), additionally **BLOCKED_ON_P020_B01** (P020 gate receipt) and **BLOCKED_ON_OTHER (WP-P0-21 accepted robustness receipt)** | Design-only: the receipt-consumption seam. Tests-only: negative tests proving no public constructor can forge a receipt, using the existing seal pattern at `stages_conservation_identity.py:156-328` as the reference mechanism. | **HIGH.** Three of the required receipt types are owned by other packages and unfrozen; their member sets are proposals (packet `:107`). |
| 3 | **Artifact / address pipeline** | B-09 / D-04 ratified shape (`trials.py:77-91`); per-trial address `artifacts/<package_hash>/<trial_id>/` (packet `:96`); `ArtifactCommitVerifier` reads committed manifest and address bytes (packet `:96`) | **PARTIALLY SATISFIED.** The manifest shape is ratified and version-`"2"`-enforced (`test_trials_and_eligibility.py:148`). The verifier's operands do not exist: no committed bytes, and `trial_id` depends on `param_hash` via `make_trial_id` (`identity.py:604-607`), which is unemittable | **BLOCKED_ON_OTHER (upstream row assembly — B-04 producer adoption)** | Design-only: the address-derivation and verifier seam. Tests-only: manifest-identity fixtures against the ratified V2 shape (`test_trials_and_eligibility.py:105`, `:120-148`) extend cleanly. | **MEDIUM.** The manifest contract itself is ratified and stable, so fixtures written against it should survive; the address derivation depends on `trial_id`, which changes if B-04 inputs change. |
| 4 | **Immutable Parquet writer** | B-15 (`P013_DESIGN_DRAFT_V1.md:1706-1716`); `CommitPartEntry.path_slot` rule at `trial_catalog.py:280-284`; upstream row assembly (row 1) | **NOT SATISFIED.** `P013_DESIGN_DRAFT_V1.md:310`: *"while B-15 is open **no part path may be derived at all**, so every fixture arm whose input is a staged or committed part, a commit receipt, or the published view is a blocked design target"* | **BLOCKED_ON_OTHER (B-15)**, additionally blocked on row 1 | Design-only. The serializer's hand-off shape already exists as `StagedPartRowProjection` (`stages_conservation_identity.py:100-110`) and the conservation comparer consumes it, so in-memory conservation fixtures are possible without writing a byte. | **HIGH** for anything path-shaped; **LOW** for conservation fixtures, which use `ordinal` / `ordered_trial_ids` / `row_count` only and touch no path. |
| 5 | **DuckDB publication** | View-preimage base-class / member-count ratification (`trial_catalog.py:20-24`); the ordered column document `PublishedViewSchemaDocumentV1` (`trial_catalog.py:484-493`); upstream rows 1 and 4 | **NOT SATISFIED.** The digest values the shipped helpers produce are self-declared *"PROVISIONAL on that ratification"* (`trial_catalog.py:22-23`) | **BLOCKED_ON_OWNER (view-preimage ratification; B-16 deliberately not opened)**, additionally blocked on rows 1 and 4 | Design-only. The column count and collapse rule are already ratified and tested (`test_trial_catalog_types.py:373`, `:583`; `trial_catalog.py:368-390`), so schema-document fixtures are stable in *shape* even while absolute digests are provisional. | **MEDIUM.** Shape work survives; any pinned digest constant does not. `trial_catalog.py:23-24` notes the DETECTED/accepted matrix does not depend on the open question, which bounds the exposure. |
| 6 | **Reader adoption and coverage** | The full reader sequence at `acceptance_reader.py:3-10`: *"typed parse → rehash → path derivation → evaluation recompute → dependent `trial_id` → lineage / path-run-id / path-cell comparers → canonical receipt"*, of which *"Only the first two steps are implemented here"*. Path derivation and the two path comparers need B-15; evaluation and `trial_id` recomputes need committed rows and caller adoption; *"the canonical-receipt verifier needs accepted WP-P0-20 (B-01)"* (`:10`). Authorization limit at `DECISIONS.md:24`: *"reader adoption beyond D-05"* is excluded | **NOT SATISFIED.** 6 of the 9 taxonomy reasons cannot fire (`acceptance_reader.py:55-60`). The reader still parses `_CatalogCommitPreimageV1` (`:31`) although B-17 ratified V2 (`trial_catalog.py:331-339`) | **BLOCKED_ON_P020_B01** for the canonical-receipt step; **BLOCKED_ON_OTHER (B-15)** for the three path steps; **BLOCKED_ON_OWNER** for the authorization to adopt beyond D-05 | Design-only: the V1-to-V2 read path, since both preimage types are already ratified in the same file. Tests-only: further RED/GREEN cases for the three emittable reasons, which need no new contract. | **LOW-to-MEDIUM** for the three implemented reasons (their contract is ratified and version-pinned at `acceptance_reader.py:44`). **HIGH** for anything touching path derivation. |
| 7 | **Caller integration** (migrated `mega_walk_forward.py`) | `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:411`: inputs include *"WP-P0-20's migrated canonical path and the one shared Risk Allocator it delivers"*; `:413`: *"Depends on: WP-P0-04, WP-P0-08, WP-P0-20"*. P013 names the caller explicitly at `trial_catalog/__init__.py:8` (*"the migrated `mega_walk_forward.py` caller"*). Authorization limit: *"caller integration"* excluded at `DECISIONS.md:24` | **NOT SATISFIED.** P020 is not accepted (section 4.0). The file is also not P013's to write today: see section 5 | **BLOCKED_ON_P020_B01**, additionally **BLOCKED_ON_OWNER** (authorization) and **BLOCKED_ON_OTHER (shared-path writer collision with WP-P0-20)** | Design-only: an adapter interface note. Nothing executable, because the target file's current contents are P020's in-flight work. | **HIGH.** The migrated canonical path does not yet exist in accepted form; anything written against today's `mega_walk_forward.py` is written against a file P020 is actively changing. |
| 8 | **Final P013 acceptance** | `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:416`: *"a real run produces a queryable catalog; a trial that was rejected can be found by its rejection reason; every row carries a `simulator_class` and a `deployment_identity_hash`, and a row produced from the unmigrated path is stamped `SIGNAL_SCREEN_ONLY` — proven by a fixture in which an unmigrated-path row is shown unable to pass as acceptance evidence."* Audit tier T1 at `:415`; the bounded slice was run at T0 because D-05 changes acceptance-evidence logic (`P013_CONTRACT_V2_VERIFICATION.md:4`) | **NOT SATISFIED.** No run, no row, no catalog, no queryable view exists. Every clause of the gate depends on rows 1–7 | **BLOCKED_ON_OTHER (every preceding row)**, with **BLOCKED_ON_P020_B01** as the governing external gate; also requires the B-01 design re-audit (`P013_DESIGN_DRAFT_V1.md:1445`: *"accepted P0-20 artifacts plus a re-audit of this draft before build"*) | The negative half of the gate is partly pre-built: the lineage seal already makes `FULL_KERNEL_SIMULATION` unreachable (`stages_conservation_identity.py:417-428`), which is the mechanism the *"unable to pass as acceptance evidence"* fixture will rely on. | **N/A** — acceptance cannot be prepared, only earned. Recording it here is scope tracking, not preparation. |

### 4.3 Summary of classifications

| Classification | Deliverables |
|---|---|
| READY_NOW | **none** |
| BLOCKED_ON_P020_B01 (governing) | 7 caller integration; 8 final acceptance (jointly); 6 reader adoption for the canonical-receipt step only |
| BLOCKED_ON_OWNER (governing) | 2 selection pipeline; 5 DuckDB publication |
| BLOCKED_ON_OTHER (governing, named) | 1 catalog writer (B-15 plus B-04/B-12 producer adoption); 3 artifact/address pipeline (upstream row assembly); 4 Parquet writer (B-15); 6 reader adoption (B-15) |

No remaining deliverable classifies as READY_NOW. Every one of the eight is gated by at least
one prerequisite that is unsatisfied today, and in every case the current authorization record
(`DECISIONS.md:23-24`) independently excludes it.

---

## 5. Shared-path collisions (one-writer rule)

Paths that remaining P013 work would touch, cross-referenced against what P020, P022, P031
and the CT13 takeover branch already own or change. Change sets measured as
`git diff --name-only <merge-base>...HEAD`: P020 40 paths against `fcac0ac6` (merge-base
`42f99571`), P031 8 paths against `62a42514`, CT13 20 paths against `fcac0ac6`, P013 15 paths
against `a4e79fbe`.

| Shared path | P013 state | Other owner and state | Severity | Notes |
|---|---|---|---|---|
| `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py` | Changed by P013: base blob `75289fa6a83bab87ed6420732624656778da0163` → head `1e9682ba057d407e4d786a66a935a77244089f72` (+480 lines per `git diff --stat`) | **Changed by P020** from the *same* base blob `75289fa6...` → `fa57a77176b267e08436e03a0c3bfd371e054ba7` (`git diff --stat fcac0ac6...HEAD` in `C:/P020_IMPL_20260912`: `1 file changed, 215 insertions(+), 1 deletion(-)`) | **HIGH — active two-writer collision today** | Both branches diverge from the identical base blob. P020's version adds `from .base import require_utc` and `from .package import AccountSnapshot` plus a `_require_finite_decimals` helper; P013's version instead makes `_json_value` raise on non-finite `Decimal` at `identity.py:43-46`. The two treat the same concern differently in the same file. Remaining P013 work (B-04/B-12 producer adoption) targets this file again. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py` | Unchanged by P013 (blob `2f16fffd08a1ca4891060205a456282665f252f3`, identical to `C:/CT13` HEAD). It is P013's named caller-integration target (`trial_catalog/__init__.py:8`) | **Changed by P020** to blob `21574df7861c79cc430cb41fff5ad0070097e01f`; present in P020's 40-path change set; `git log --oneline -- <path>` in `C:/P020_IMPL_20260912` shows `77c0bc68`, `ef633d9a`, `0134fc82`, `54989afe`, `6442b000` | **HIGH — future collision, already diverged** | The plan names this file as WP-P0-20's protected surface (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:489`, `:507`). P013 caller integration cannot be the writer here while P020 holds it. |
| `DECISIONS.md` | Changed by P013: base blob `4d5c3dfcaef7c0a3a547e5a6eca9a73d2033b0c8` → `3c7d0d0ba47c3742945089d0516af4ea47bcea36` | **Changed by P031** from the same base `4d5c3dfc...` → `a3b9390071277e55127911219109d02e31c449da`; **changed by the CT13 takeover branch** → `8e8772d14a5d5d7febe5b93a437d7e650dd37af3` | **HIGH — three-way collision** | Three branches append rows to the same append-oriented table from the same base blob. All three are unmerged. |
| `MTC_COMMAND_CENTER/02_TASKS/TASK_HISTORY.json` | Changed by P013: base `1ebd9d49f5eabcbf9619166d43f83b187b9fc09e` → `ea319ec7dffe5731988a12a443c4f7fa4e1100c8` (adds `HIST-2026-0044`, `HIST-2026-0045`) | Unchanged by P020, P031 and CT13 (the CT13 blob is `1ebd9d49...`, byte-identical to the P013 base) | **LOW** | P013 is the sole current writer among the four inspected checkouts. |
| `MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py` | Changed by P013 (ArtifactManifest V2) | Unchanged by P020, P031, CT13 (all `a6a5758e...`) | **MEDIUM — ownership, not concurrency** | The plan assigns this schema to a different package: *"The `TrialRecord` schema belongs to P0-04; P0-13 consumes it and does not redefine it"* (`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:255`), and `:320` lists `TrialRecord` among WP-P0-04's outputs. The decision packet routes the change through *"WP-P0-04 schema"* (`P013_CONTRACT_DECISION_PACKET_V2.md:188`). The owner decision authorized it (`DECISIONS.md:24`); the plan-level ownership statement is unchanged. Recorded as a disagreement, not a defect. |
| `MTC_COMMAND_CENTER/contracts/mtc_contracts/package.py` | Unchanged by P013 | **Changed by P020** (in its 40-path set) | **MEDIUM — latent** | P020's `identity.py` now imports `AccountSnapshot` from it, so any P013 edit to `identity.py` inherits an ordering dependency on P020's `package.py` after integration. |
| `MTC_COMMAND_CENTER/contracts/tests/test_identity.py` | Changed by P013: `a6edb6251695eaad34c9e81db9f3c930969bbdd4` → `9a0d2cab8a8b97f846ce54d6b19d0f59cb25f230` | Unchanged by P020 (still `a6edb625...`), which adds a sibling `MTC_COMMAND_CENTER/contracts/tests/test_p020_identity.py` instead | **LOW** | Same directory, different files. No textual collision. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/p022_research_tracker.py` | Unchanged by P013; the ratified B-12 registry is *"shared with full P0-22"* (`DECISIONS.md:24`), so future sharing work touches this file | **Owned by P022**, merged on master via PR190 (`C:/tmp/CLAUDE_TAKEOVER_20260913/P022_HANDOFF.md:8`, `:20`) | **MEDIUM — future** | P022 is parked; `P022_HANDOFF.md:52` says keep it parked behind full P013. Any P013-side sharing work must be coordinated, not performed here. |
| `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` and `.../MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md` | Unchanged by P013 | **Changed by P031** (plan blob `7081c88169d121afc9f3547af93641fe16ac8c65` vs CT13 `5570e55475d9175b8a2307c483b771af4ccc8b18`) | **LOW for P013 today** | Relevant only if P013 work later amends the plan. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/HANDOFF.md` | Unchanged by P013 | **Changed by P031**; P031 names it as its only known upstream overlap (`C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:16`) | **NONE for P013** | Recorded for completeness. |

**Net collision picture.** Two hard collisions exist right now — `identity.py` (P013 versus
P020, both diverged from the same base blob) and `DECISIONS.md` (P013 versus P031 versus
CT13). One hard collision is guaranteed the moment P013 caller integration is authorized:
`mega_walk_forward.py`, which P020 has already changed. This is the concrete content of the
P013 handoff's instruction to *"coordinate one writer for shared files with P020/P022 if
later authority is granted"* (`C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:100-101`) and
of its stop condition on *"shared-path writer collision"* (`:104`).

---

## 6. NOT VERIFIED

This section is deliberately non-empty. Each item is something this lane did **not**
establish, or established as an unresolved discrepancy.

1. **Aggregate diff object and raw diff SHA-256 were not recomputed.**
   `a38248a967d5f9838bf19c13ef4fba8b79f71965` and
   `46089d3fca63ee263e7389ebe87f360f0303af720bd86742ab315dd1a50ed5b2`
   (`C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:12-13`) are quoted, not verified here.
2. **The `219 passed` suite result was not reproduced.** The BRIEF forbids running test
   suites. `219 passed` is quoted from `P013_CONTRACT_V2_VERIFICATION.md:46` and
   `P013_HANDOFF.md:57`, not observed.
3. **Review-report SHA-256 values were not recomputed** for
   `P013_OPUS_T0_REPORT_DA1FB184_R4_EXEC_CONFIRM.json` or
   `P013_GEMINI_T0_REPORT_DA1FB184_FINAL.txt`.
4. **`HIST-2026-0045` is uncited by the handoff and the verification record.** Both name only
   `HIST-2026-0044` / `WP-P0-13-CONTRACT-V2-20260912`
   (`P013_HANDOFF.md:22`; `P013_CONTRACT_V2_VERIFICATION.md:11`), yet the committed
   `TASK_HISTORY.json` carries a second APPROVED event `HIST-2026-0045` /
   `WP-P0-13-CONTRACT-DEFAULTS-20260913`. Whether the protected-path approval for the
   2026-09-13 defaults is `HIST-2026-0045` or is covered by `HIST-2026-0044` is not
   established by any source this lane read.
5. **The P013 design draft read for B-01 lives outside the BRIEF's source list.**
   `C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md`
   was located via the earlier Lead map's pointer
   (`P013_DEPENDENCY_ADOPTION_MAP.md:13-14`). Its status as the controlling v2.3 design was
   not independently confirmed against an owner record; its own title line reads
   `# WP-P0-13 TrialRecord catalog writer — DESIGN DRAFT v2.3`.
6. **Decisions 128 and 88 could not be read at source.** `DECISIONS.md:16-17` states their
   *"underlying earlier records are not repository-resident"*. Only the packet summary at
   `P013_CONTRACT_DECISION_PACKET_V2.md:11-12` was available.
7. **Blocker-count disagreement across sources, unreconciled.** The design draft's own
   section 8 count says *"10 open blockers … B-01, B-03, B-04, B-05, B-06, B-07, B-08, B-09,
   B-12, B-15"* at `:320` and *"11 open blockers are B-01, B-03, B-04, B-05, B-06, B-07,
   B-08, B-09, B-12, B-15, B-17"* at `:358` (successive versions). The decision packet says
   *"Fifteen open items remain"* at `:7`, counting eleven blockers plus D-02, D-03, D-04 and
   D-05. This lane did not determine which count the Lead treats as controlling after the
   2026-09-12/13 ratifications closed several of them.
8. **Stale P020 commit id in the prior Lead map.**
   `P013_DEPENDENCY_ADOPTION_MAP.md:7`, `:23` pin P020 at
   `556639f59122e33b664ab918a4241eb96680219b`. The current verified P020 head is
   `b9b72f858dc830a9389517f79da5ea3c1fa6122c` (`P020_HANDOFF.md:9`). The `8/16 MET` /
   `NOT ACCEPTABLE` conclusion is unchanged, but the commit id must not be quoted forward.
9. **Vocabulary duplication, not reconciled.** `identity.py:263-265` defines
   `SimulatorClass` as a closed enum; `stages_conservation_identity.py:55-56` separately
   declares module-level strings `SIGNAL_SCREEN_ONLY = "SIGNAL_SCREEN_ONLY"` and
   `FULL_KERNEL_SIMULATION = "FULL_KERNEL_SIMULATION"` and does not import the enum. The
   values agree today. Whether the duplication is intended (the module's comment at `:52-54`
   says it *"consumes the vocabulary"*) or is a latent drift risk was not established; no
   test observed here asserts equality between the two.
10. **V2 commit preimage is written-only-in-tests and read-as-V1.** `trial_catalog.py:331-339`
    ratifies `_CatalogCommitPreimageV2`, while `acceptance_reader.py:31` imports and parses
    `_CatalogCommitPreimageV1`. The reader docstring explains the boundary (`:6-8`), but no
    source read here states when or by whom the reader is expected to adopt V2.
11. **Owner-record visibility gap.** The `OD-20260912-P013-CONTRACTS` and
    `OD-20260913-P013-CONTRACT-DEFAULTS` rows and both `HIST-` events exist only on the
    unmerged P013 branch. A reader of `C:/CT13` finds no record of them (section 3.6). This is
    consistent with the no-integration boundary, but it means branch-local decision records
    are the only evidence, and this lane could not cross-check them against an owner-side
    artifact other than the packet.
12. **`C:/CT13` HEAD is not integrated master.** `git rev-parse HEAD` returns
    `51fc2437f84061e0e164ff7965e036a143167003` (`git log -1`:
    `docs: record preserved checkpoint formatting accurately`), which is 20 paths ahead of
    `fcac0ac67cf2682693ad28138b1a56e15a0846f2`. All CT13 citations above are to that branch
    head, not to master.
13. **P022 and P031 worktree heads were read but their cleanliness was not checked.** Only
    `HEAD` ids were taken. `C:/tmp/P022_TRACKER_20260912` was not inspected at all; P022
    evidence comes from the merged tracker in `C:/CT13` plus `P022_HANDOFF.md`.
14. **Plan-ownership disagreement, unresolved.**
    `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:255` says the `TrialRecord`
    schema belongs to WP-P0-04 and *"P0-13 consumes it and does not redefine it"*, while
    `OD-20260912-P013-CONTRACTS` (`DECISIONS.md:24`) authorizes the P013 package to change
    `trials.py`. Both statements are quoted; this lane does not adjudicate between them.
15. **No statement is made about whether any preparation listed in section 4.2 is
    authorized.** Section 4.2's preparation column is a technical feasibility reading only.
    `DECISIONS.md:23-24` currently excludes all of it, and nothing in this document changes
    that.

---

## 7. Citation index

One citation per line. Paths are given as read.

```
C:/tmp/CLAUDE_P0_RUN_20260913/laneP13M_dependency_map/BRIEF.md
C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:12
C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:13
C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:14
C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:15
C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:22
C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:52
C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:53
C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:57
C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:100
C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:101
C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:104
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:9
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:30
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:40
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:41
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:42
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:43
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:44
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:45
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:46
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:47
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:48
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:49
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:51
C:/tmp/CLAUDE_TAKEOVER_20260913/P022_HANDOFF.md:8
C:/tmp/CLAUDE_TAKEOVER_20260913/P022_HANDOFF.md:20
C:/tmp/CLAUDE_TAKEOVER_20260913/P022_HANDOFF.md:28
C:/tmp/CLAUDE_TAKEOVER_20260913/P022_HANDOFF.md:52
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:16
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:105
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:118
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:119
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:120
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:121
C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md:34
C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md:42
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:7
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:11
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:12
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:26
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:35
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:48
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:57
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:59
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:62
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:68
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:70
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:79
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:81
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:90
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:96
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:103
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:107
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:112
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:125
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:134
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:188
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:190
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:208
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md:4
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md:11
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md:16
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md:17
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md:18
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md:19
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md:46
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md:82
C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md:7
C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md:13
C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md:14
C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md:23
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:310
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:320
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:328
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:358
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1135
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1348
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1439
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1441
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1445
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1451
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1463
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1465
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1466
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1468
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1706
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1716
C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md:1734
C:/tmp/P013_CONTRACT_V2_20260912/DECISIONS.md:16
C:/tmp/P013_CONTRACT_V2_20260912/DECISIONS.md:17
C:/tmp/P013_CONTRACT_V2_20260912/DECISIONS.md:23
C:/tmp/P013_CONTRACT_V2_20260912/DECISIONS.md:24
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/02_TASKS/TASK_HISTORY.json
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/CHANGELOG.md
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/README.md:18
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/README.md:19
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/README.md:20
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/README.md:21
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/README.md:57
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/README.md:64
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/__init__.py:28
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/__init__.py:37
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/__init__.py:74
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/__init__.py:85
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/__init__.py:126
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:43
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:46
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:54
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:63
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:122
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:131
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:134
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:137
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:140
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:156
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:218
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:225
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:232
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:246
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:249
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:254
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:257
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:260
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:263
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:265
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:271
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:282
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:326
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:336
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:339
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:340
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:342
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:343
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:345
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:358
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:388
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:391
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:401
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:404
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:423
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:426
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:473
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:478
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:481
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:486
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:489
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:490
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:496
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:502
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:505
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:512
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:516
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:521
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:604
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:607
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:5
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:10
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:13
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:15
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:19
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:20
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:22
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:23
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:24
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:37
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:72
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:78
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:87
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:91
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:93
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:114
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:122
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:127
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:133
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:134
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:168
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:192
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:195
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:205
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:206
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:207
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:208
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:210
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:212
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:219
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:222
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:223
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:229
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:238
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:246
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:247
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:268
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:275
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:280
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:284
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:310
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:316
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:321
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:324
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:328
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:331
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:334
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:339
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:348
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:359
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:368
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:390
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:398
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:408
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:411
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:412
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:422
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:427
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:456
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:457
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:462
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:465
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:481
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:484
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:492
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py:493
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:14
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:31
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:74
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:77
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:78
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:80
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:81
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:91
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_deep_immutability.py:12
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_deep_immutability.py:85
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:19
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:20
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:21
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:22
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:23
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:24
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:25
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:26
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:28
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:171
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:378
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:386
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:615
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:626
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:720
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:15
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:18
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:21
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:30
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:40
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:127
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:129
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:368
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:373
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:483
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:491
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:542
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:555
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:582
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:583
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:667
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trials_and_eligibility.py:5
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trials_and_eligibility.py:10
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trials_and_eligibility.py:28
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trials_and_eligibility.py:105
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trials_and_eligibility.py:120
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trials_and_eligibility.py:137
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trials_and_eligibility.py:148
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/__init__.py:7
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/__init__.py:8
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/__init__.py:11
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/__init__.py:12
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:3
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:6
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:7
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:8
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:10
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:30
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:31
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:44
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:47
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:55
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:60
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:62
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:63
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:64
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:70
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:84
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:91
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:189
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:204
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:240
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:249
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:251
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:272
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:292
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:293
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py:298
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:5
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:6
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:8
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:29
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:30
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:33
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:35
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:52
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:54
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:55
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:56
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:59
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:61
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:65
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:73
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:79
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:80
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:81
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:100
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:110
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:113
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:121
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:124
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:153
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:156
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:213
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:215
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:219
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:234
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:238
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:252
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:316
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:328
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:331
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:341
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:358
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:374
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:376
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:390
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:414
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:417
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:419
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:423
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:424
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:428
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:433
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:434
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:436
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:440
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:463
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:489
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:505
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:513
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:518
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:520
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:526
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:528
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:534
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/test_trial_catalog_acceptance_reader.py:25
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/test_trial_catalog_acceptance_reader.py:485
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/test_trial_catalog_acceptance_reader.py:486
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/test_trial_catalog_stages.py:11
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/test_trial_catalog_stages.py:26
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/test_trial_catalog_stages.py:54
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/test_trial_catalog_stages.py:56
C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:1
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:14
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:71
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:77
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:89
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/__init__.py:74
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/__init__.py:85
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/__init__.py:126
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/package.py
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/tests/test_p020_identity.py
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py
C:/P020_IMPL_20260912/p020_simulator.py
C:/P020_IMPL_20260912/p020_owner_policy.py
C:/P020_IMPL_20260912/statistical_battery.py
C:/P020_IMPL_20260912/portfolio_simulator.py
C:/P020_IMPL_20260912/unsimulated_controls.py
C:/P020_IMPL_20260912/research_verification/p020/test_owner_policy.py
C:/P020_IMPL_20260912/research_verification/p020/test_execution_proofs.py
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/p020_economics.py
C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:25
C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/HANDOFF.md
C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md
C:/tmp/P031_M1_20260913/DECISIONS.md
C:/CT13/DECISIONS.md:79
C:/CT13/MTC_COMMAND_CENTER/02_TASKS/TASK_HISTORY.json
C:/CT13/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p022_research_tracker.py:8
C:/CT13/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p022_research_tracker.py:20
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/P022_RESEARCH_TRACKER_SCOPE.md:13
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/P022_RESEARCH_TRACKER_SCOPE.md:41
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/P022_RESEARCH_TRACKER_SCOPE.md:53
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/CODEX_TSP0_AUDIT_2026-07-19.md:124
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/CODEX_TSP0_AUDIT_2026-07-19.md:211
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:255
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:267
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:320
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:409
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:410
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:411
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:412
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:413
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:414
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:415
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:416
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:417
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:483
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:489
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:506
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:507
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:509
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:651
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:665
C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/START_HERE.md:42
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:193
```

---

## 8. Closing statement

Every remaining full-P013 deliverable is blocked today, and no reading in this document
constitutes permission to begin any of them. The governing external gate is B-01, defined at
`P013_DESIGN_DRAFT_V1.md:1441-1445` as a *WP-P0-13* blocker requiring actual WP-P0-20 package
acceptance; WP-P0-20 currently reports `8/16 MET` / `NOT ACCEPTABLE`
(`P020_HANDOFF.md:30`) and publishes none of the canonical-receipt artifacts B-01 names. The
takeover instruction's warning that *"The narrower P020 milestone is not automatically B-01"*
(`START_HERE.md:42`) is confirmed by direct inspection: zero B-01 seam symbols exist in P020
code.

Independently of B-01, four internal prerequisites (B-15, B-07, B-06, and the view-preimage
ratification) and the producer-adoption halves of B-04 and B-12 are unsatisfied, and the
current authorization record (`DECISIONS.md:23-24`) excludes every remaining deliverable by
name. Two shared-file collisions — `identity.py` with WP-P0-20 and `DECISIONS.md` with
WP-P0-31 and the takeover branch — are live now, and a third (`mega_walk_forward.py`) is
guaranteed the moment caller integration is authorized.

---

## 9. Lead audit and recording note (Claude Fable 5.1, 2026-09-13)

- Purpose: the takeover instruction requires inspecting the ratified contracts and the dependency/adoption map before claiming any P013 writer scope is ready. This map answers that: **no remaining P013 deliverable is READY_NOW** (§4.3); governing blockers are P020 B-01 (caller integration, final acceptance, canonical-receipt reader step), owner ratifications (selection pipeline, DuckDB view preimage) and named engineering prerequisites (B-15 coordinate channel, B-04/B-12 producer adoption). The current authorization record (`DECISIONS.md:23-24`) independently excludes every remaining deliverable.
- Integration facts to act on before any P013 or P020 integration: active two-writer collision on `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py` (P013 head `1e9682ba` and P020 head `fa57a771` both diverge from base blob `75289fa6`); three-way append collision on root `DECISIONS.md` (P013, P031, CT13 takeover branch); guaranteed future collision on `mega_walk_forward.py` (P020-owned protected surface) the moment caller integration is authorized. One writer per shared file; reconcile serially at integration.
- Citation audit: 401 index entries resolved mechanically; 399 valid; two line references exceed their file by one to two lines (`P013_CONTRACT_V2_20260912/.../trials.py:91`, file has 90 lines; `P020_IMPL_20260912/.../trials.py:89`, file has 87 lines) — harmless end-of-file references, left as written and noted here.
- Lane outcome: 78 turns; the draft was complete through §8 when the Claude Pro five-hour session limit ended the lane (reset 15:20Z). No Git write, no execution of test suites.
- Recording act: file added under the takeover mirror in the control checkout; ordinary local commit after the Gemini quiet window; no push. Grants no P013 scope, authority or acceptance.
- Source draft preserved unchanged at `C:/tmp/CLAUDE_P0_RUN_20260913/laneP13M_dependency_map/P013_DEPENDENCY_ADOPTION_MAP_DRAFT.md` (SHA-256 5357d3fe74099ef349e5ee996244e0d2e0d29f5865778d05888e76581de47f96).
