<!-- LEAD AUDIT NOTE (Claude Fable Lead, 2026-09-13 13:16Z) -->
> **Lead audit of lane P13E deliverable** (source `C:/tmp/CLAUDE_P0_RUN_20260913/laneP13E_plan/P013_DEPENDENCY_RESOLUTION_PLAN_DRAFT.md`, SHA-256 `c0b05a989a4d48119135bee8c706b246721705987f45cb6ccb67b7e732e6b9b1`, independent Claude Max claude-opus-5 xhigh lane, exit 0).
> Mechanical citation check: 254 token/worktree `file:line` citations resolved against the expansions in the document's citation-token table (P13M, PKT13, PKT20, MAP13, DSGN, H13, H20, SH, VER13, PLAN, POL, `P13/`, `P20/`); 0 out of range. The one cited blob `21574df7…` resolves as a blob in the shared object store.
> Content check: B-01 kept `NOT SATISFIED` (controlling text DSGN:1441/1445 quoted, two-part test: accepted P0-20 artifacts plus re-audit); WP-P0-13 kept at WAIT_P020_ACCEPTANCE; the blocked writer was not launched; D-P20-3 write ownership (P020 owns identity.py / mega_walk_forward.py while active) respected. The plan authorizes nothing.
> Lead audit record only, not owner ratification. Recorded in CT13 working tree; commit deferred until the Gemini quiet-window guard is idle.

# WP-P0-13 dependency-resolution and shared-file reconciliation plan — DRAFT

Prepared 2026-09-13 by an independent planning lane (`claude-opus-5`, xhigh) from read-only
inspection of the frozen P013 contract head, the P020 implementation worktree, the takeover
handoffs, the two Lead packets, and the 2026-09-13 dependency-map lane.

**This document is a plan, not authority.** It accepts nothing, ratifies nothing, closes no
blocker, starts no writer and grants no permission. Owner authorization for this lane
(chat 2026-09-13) is: *"Prepare P013's dependency-resolution and shared-file reconciliation
plan. Preserve B-01; identify exactly what would satisfy it. Do not launch the blocked writer
under an assumed exception."* The blocked writer was not launched. Every step below that is
**not authorized today** is marked `NOT AUTHORIZED TODAY`. The Lead audits every citation.

Two binding owner decisions of the same date govern sections 2 and 3:

- **D-P20-3 — YES.** *"P020 owns writes to `identity.py` and `mega_walk_forward.py` while
  active. Preserve P013's existing changes and reconcile both requirements; do not overwrite
  either branch's work. Other lanes remain read-only on these shared files."*
- **D-P20-1** *"...does not satisfy P013 B-01."*

## Citation tokens

| Token | Expands to |
|---|---|
| `P13M` | `C:/tmp/CLAUDE_P0_RUN_20260913/laneP13M_dependency_map/P013_DEPENDENCY_ADOPTION_MAP_DRAFT.md` |
| `PKT13` | `C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md` |
| `PKT20` | `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P020_SCOPE_DECISION_PACKET_20260913.md` |
| `MAP13` | `C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md` |
| `DSGN` | `C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md` |
| `H13` | `C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md` |
| `H20` | `C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md` |
| `SH` | `C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md` |
| `VER13` | `C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md` |
| `PLAN` | `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` |
| `POL` | `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/REVIEW_POLICY.md` |
| `P13/` | `C:/tmp/P013_CONTRACT_V2_20260912/` (worktree, head `da1fb184`) |
| `P20/` | `C:/P020_IMPL_20260912/` (worktree, head `b9b72f85`) |

Blob ids are cited as `git-blob:<oid>` and were read with `git show <oid>` from `P13/`; all
five blobs named in this document resolve in the shared object store.

---

## 1. What exactly satisfies B-01

No reinterpretation is offered here. B-01 is a **WP-P0-13 design-draft blocker**, not a P020
deliverable label, and its controlling text is `DSGN:1441` (heading
*"### B-01 — `P020-ACCEPTANCE-AND-CANONICAL-RECEIPT`"*, under *"## 7. Named blockers — no
defaults"* at `DSGN:1439`) and `DSGN:1445`, read directly by this lane:

> "WP-P0-13 build cannot begin until WP-P0-20 accepts, and the canonical receipt issuer/shape
> is not settled. … B-01 remains open on package acceptance itself, not on the historical
> paper verdicts. **PROVISIONAL-ON-P020** covers every full-kernel choice in this draft.
> Required resolution: accepted P0-20 artifacts plus a re-audit of this draft before build."

`DSGN:1445` is the sentence that fixes the two-part test: **accepted P0-20 artifacts** *plus*
**a re-audit of this draft before build**. Neither half is optional, and neither is satisfiable
by a label.

### 1.1 The six members of a B-01 closure

Each row names the thing, its source, and the one concrete artifact that would evidence it.
"Concrete artifact" means a nameable, hashable object a reviewer can open — not a status word.

| # | What must exist | Source citation | Concrete artifact that would evidence it | State today |
|---|---|---|---|---|
| **1** | **P020 package acceptance at an exact accepted head.** The bundle member `p020_accepted_head: GitSha40` presupposes one. | `PKT13:31`; `PKT13:35` — *"Package acceptance and P020 contract-owner act. Owner signature does not substitute for acceptance."*; stop condition `PKT13:194` — *"Anything short of accepted frozen identity"* | A P020 package-acceptance record naming one 40-character head, with `P20/check_p020_acceptance.py` no longer printing `NOT ACCEPTABLE`, the eight named blockers closed, and the T0 roster reproduced on that exact head. | **NOT SATISFIED.** *"Acceptance remains intentional exit 1: 8/16 criteria MET / `NOT ACCEPTABLE`."* (`H20:30`); *"WP-P0-20 is therefore not package-accepted or merge-ready."* (`H20:51`); eight live blockers at `H20:40-49`. Current head `b9b72f858dc830a9389517f79da5ea3c1fa6122c` (`H20:9`). |
| **2** | **`P020AcceptedCatalogueDependencyV1`** — the twelve ordered members: `contract_version`, `p020_accepted_head`, `p020_package_acceptance_receipt_sha256`, `control_parity_checklist_sha256`, `statistical_battery_definition_sha256`, `rejection_taxonomy_sha256`, `canonical_path_receipt_schema_sha256`, `canonical_path_receipt_issuer_id`, `canonical_path_receipt_verifier_id`, `shared_allocator_import_identity_sha256`, `canonical_kernel_import_identity_sha256`, `p020_verified_acceptance_receipt_sha256`. | `PKT13:31` (member list read and counted by this lane: twelve) | A P020-owned, P020-published typed document plus its focused tests, under P020-owned paths — `PKT13:32`: *"P020-owned paths frozen by its Lead; P013 adapter only after acceptance. P013 must not edit P020."* | **NOT SATISFIED.** A grep for the six B-01 seam symbols across `P20/` returns **zero matches** (`P13M:216`). |
| **3** | **The canonical-path receipt issuer and shape, settled.** Three of the twelve members carry it: the receipt schema digest, the issuer id, the verifier id. | `PKT13:31`; `DSGN:1445` (*"the canonical receipt issuer/shape is not settled"*); `MAP13:7` | A frozen receipt schema whose SHA-256 is recorded, a named issuer id, a named verifier id, and a worked example in which the frozen receipt is independently bound to one completed run. | **NOT SATISFIED.** Same zero-match grep (`P13M:216`). Stop condition `MAP13:83`: *"if P020 is not package-accepted, any member/issuer/verifier identity is absent, or the frozen receipt cannot be independently bound to the completed run, P013 remains `WAIT_P020_ACCEPTANCE`"*. |
| **4** | **`P020VerifiedCanonicalPathResult`** — an opaque result P013 verifies **itself** before minting its own non-public `FullEvidenceSinkCapability`. | `PKT13:31` — *"P020 returns an opaque `P020VerifiedCanonicalPathResult`; P013 independently verifies it and only then mints its own non-public `FullEvidenceSinkCapability`. No `ACCEPTED` status label is trusted."* | A P020-published opaque type, plus the P013-side negative proof required by `PKT13:34`: *"Wrong issuer/run/import identity/nonaccepted head all RED on a trusting verifier and GREEN as the closed refusal. P013 proves no public constructor can obtain the full capability."* | **NOT SATISFIED.** No such type exists (`P13M:216`). The P013 side already encodes the open state in code: `P13/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:424-428` refuses with *"FULL_KERNEL_SIMULATION requires a verified canonical-path receipt from an accepted WP-P0-20; B-01 is open (WAIT_P020_ACCEPTANCE)"* (read directly by this lane). |
| **5** | **The accepted rejection-taxonomy values (B-06).** `TrialRejectionTaxonomyV1(policy_version, entries)`, each ordered entry `reason_code: NonEmptyStr`, `verdict: Literal["FAIL","BLOCKED"]`, `producer_id: NonEmptyStr`, `predicate_id: NonEmptyStr`. | `PKT13:130`; `PKT13:208` — *"B-06 values wait for P020's accepted taxonomy."*; `PKT13:134` — *"actual entries freeze with P020 acceptance"* | A P020-published, version-stamped taxonomy document whose entries are frozen at the accepted head, with `TrialGateAggregator` validating every emitted `rejection_reasons` code against it (`PKT13:130`). | **NOT SATISFIED.** `TrialRejectionTaxonomyV1` returns zero matches in `P20/` (`P13M:216`). |
| **6** | **A P013 design re-audit before build.** | `DSGN:1445` — *"Required resolution: accepted P0-20 artifacts plus a re-audit of this draft before build."*; `MAP13:7`; `PKT13:223` — *"after actual P020 acceptance the Lead re-audits B-01 and authorizes the full-writer package separately"* | A dated re-audit record over `DSGN` at the accepted P020 head, resolving every `PROVISIONAL-ON-P020` marker in the draft, signed as a P013 Lead act and separately authorized. | **NOT SATISFIED.** Not performed; cannot be performed before members 1–5 exist. The re-audit must also re-pin `PKT13:30`'s stale P020 head `556639f591…` to the then-accepted head (`PKT20:211`, `P13M:338-345`). |

**Compatibility constraints that a B-01 closure must not break** (`PKT13:33`): *"Six-member
`evaluation_run_hash` remains unchanged; receipt hash stays absent from the catalogue commit
preimage."* The shipped code already holds both: the six declared members of `RunEnvelopeV1`
match the six arguments of `compute_evaluation_run_hash` (`P13M:102`), and
`canonical_path_receipt_hash` is *"absent by design for screening"* — the stage refuses a
screening receipt that carries one
(`stages_conservation_identity.py:429-433`, read directly).

### 1.2 The P0-20 research/engineering label does not satisfy B-01

Stated plainly, as the brief requires.

The proposed `OD-20260913-P020-SCOPE-1` row would narrow WP-P0-20's **current** acceptance
object to its reviewed research/engineering deliverable under the completion label
*"P0-20 research/engineering scope complete; package acceptance and production admission
pending"* (`PKT20:142`). That row, by its own text, *"Authorizes no package acceptance,
merge-readiness, production admission, P012 admission, B-01 closure, review waiver or new
spend"* (`PKT20:142`).

The sources refuse the substitution directly and in their own words:

- `PKT20:93` — section heading: *"B-01 check — does the proposed P0-20 milestone satisfy it?
  **No.**"*; and `PKT20:130`: *"§4 is written so that it does not touch B-01. **B-01 remains
  `NOT SATISFIED`**; P013 stays at `WAIT_P020_ACCEPTANCE`."*
- `PKT20:357` (Lead audit note) — *"the proposed P0-20 research/engineering milestone does NOT
  satisfy P0-13's B-01 (§3); nothing in this packet or in the P0-12 amendment changes
  `WAIT_P020_ACCEPTANCE`."*
- `SH:42` — *"The narrower P020 milestone is not automatically B-01."*
- `MAP13:35` — *"B-01 is deliberately package-acceptance-bearing. Reinterpreting it as
  component readiness would silently lower the gate and would let a nonaccepted producer mint
  full-kernel lineage."*
- `PKT13:208` — *"B-01 cannot be signed closed; it waits for actual P020 acceptance."*
- Owner decision of 2026-09-13 on D-P20-1, quoted in this lane's BRIEF: *"This does not
  satisfy P013 B-01."*

**The mechanical reason, not just the documentary one.** B-01's test is *package acceptance*
at an exact head. `8/16 MET` is *"the structural ceiling of the reporter as written, and **no
change of P012 state — (i) or (ii) — can move the printed count**"* (`PKT20:79-82`, quoting
`DRD:320-323`); eight probes have no `MET` branch at all (`PKT20:84`). A scope label is
therefore a statement about what P020 is *claiming*, and changes no printed number
(`PKT20:151-153`: *"What the reporter would still say. Unchanged: `8/16 component criteria
MET`, then `NOT ACCEPTABLE -- outstanding:` the eight names … The label is a scope statement,
not a reporter state."*). B-01 tests the reporter state, not the label.

**One further piece of code-level evidence found by this lane.** The migrated-path work that
B-01 depends on is *self-labelled non-accepting inside P020's own engine*. In
`git-blob:21574df7861c79cc430cb41fff5ad0070097e01f`
(`MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py` at P020 head) the successor
path stamps its ledger with `"acceptance_status": "RESEARCH_ONLY_NOT_ACCEPTED"` (blob
line 1003) beside `"semantics_id": "2.1.0"` (blob line 1001). A P013 verifier that trusted a
status label would be trusting a string that reads `RESEARCH_ONLY_NOT_ACCEPTED` — which is
precisely why `PKT13:31` says *"No `ACCEPTED` status label is trusted."*

### 1.3 What B-01 does **not** require

Recorded so the gate is not accidentally raised either:

- It does **not** require production admission or P012 production admission. Those are P020's
  class-B rows (`PKT20:57-60`), separate from package acceptance.
- It does **not** require the historical paper verdicts to be reversed — *"B-01 remains open on
  package acceptance itself, not on the historical paper verdicts"* (`DSGN:1445`).
- It is **not an owner checkbox** — `PKT13:225`: *"P020 acceptance is not an owner checkbox"*;
  `PKT20:196`: *"**B-01 is not an owner checkbox**"*. No owner signature can close it.
- Closing B-01 does **not** by itself unblock the P013 writer. B-15, B-04/B-12 producer
  adoption, B-07 and B-06 remain separately unsatisfied (`P13M:351-361`), and the current
  authorization record independently excludes the writer
  (`P13/DECISIONS.md:24`).


---

## 2. `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py` — reconciliation plan under D-P20-3

Owner decision D-P20-3 (2026-09-13): *"P020 owns writes to `identity.py` and
`mega_walk_forward.py` while active. Preserve P013's existing changes and reconcile both
requirements; do not overwrite either branch's work. Other lanes remain read-only on these
shared files."* The recommendation it answers is `PKT20:194`. Everything in this section is a
plan for the writer P020 already is; this lane wrote nothing.

### 2.1 Three-way analysis

All three blobs were read with `git show` from `P13/`. The common base blob is confirmed
identical at both branches' relevant commits by `git rev-parse`:

| Commit | `identity.py` blob | Bytes | Lines |
|---|---|---|---|
| `a4e79fbe` (P013 accepted base) | `75289fa6a83bab87ed6420732624656778da0163` | 4,854 | 154 |
| `42f99571` (P013/master merge-base) | `75289fa6a83bab87ed6420732624656778da0163` | 4,854 | 154 |
| `da1fb184` (P013 head) | `1e9682ba057d407e4d786a66a935a77244089f72` | 22,853 | 626 |
| `b9b72f85` (P020 head) | `fa57a77176b267e08436e03a0c3bfd371e054ba7` | 13,647 | 368 |

The base blob is byte-identical at `a4e79fbe` and `42f99571`, so the two branches genuinely
diverge from one common ancestor of this file. This confirms `P13M:407` (*"Both branches
diverge from the identical base blob"*) and its recorded diffstat for P020,
`1 file changed, 215 insertions(+), 1 deletion(-)`: 154 + 215 − 1 = 368 reconciles exactly.

**Base (`75289fa6`) declares ten module-level names**, in order: `_json_value`,
`canonical_json`, `_hash_named_parts`, `make_candidate_id`, `compute_package_hash`,
`compute_evaluation_run_hash`, `compute_deployment_identity_hash`, `make_trial_id`,
`make_run_id`, `compute_family_id`.

**What P020 adds (`fa57a771`).** Three module-level constants and nine callables, all
**appended after** the base's last line, occupying blob lines 161-368: `_SHA256_HEX_CHARS`,
`_SELECTED_MANIFEST_FIELDS`, `_SELECTED_ENTRY_FIELDS`, `_digest`, `_require_sha256`,
`_require_text`, `_require_relative_path`, `_require_finite_decimals`,
`_require_schema_valid`, `compute_account_snapshot_id`, `compute_dataset_manifest_sha`,
`compute_selected_dataset_hash`.

**What P020 changes in the shared region: the import prologue only.** It adds
`from collections.abc import Mapping, Sequence` (blob line 7), replaces
`from pydantic import BaseModel` with `from pydantic import BaseModel, ValidationError`
(blob line 13), and adds `from .base import require_utc` and
`from .package import AccountSnapshot` (blob lines 15-16). **P020 alters no base function body
and no base docstring.** Every one of the base's ten names is byte-identical in `fa57a771`.

**What P013 adds (`1e9682ba`).** One private base model, four constants/aliases and
twenty-two callables/classes, all **inserted between** `canonical_json` and
`_hash_named_parts`, occupying blob lines 30-33 and 66-512: `_FrozenIdentityDocument`,
`_snapshot_parameter_value`, `lower_parameters`, `_decimal_parameter_number`,
`_encode_parameter_json`, `_json_object_pairs`, `_reject_nonfinite_json_number`,
`_DECIMAL_PARAMETER_NUMBER`, `_parse_parameter_float`, `_load_canonical_json_object`,
`_load_canonical_parameter_json_object`, `ParamHashPreimageV1`, `IdentityDocumentT`,
`_compute_typed_identity_digest`, `compute_param_hash`, `SearchRegime`, `SimulatorClass`,
`ParameterScalar`, `RegisteredParameterDefinition`, `PreregisteredSpacePreimageV1`,
`_canonical_parameter_definition`, `_materialize_unambiguous_iterable`,
`_materialize_string_members`, `project_preregistered_space`,
`compute_preregistered_space_hash`, `LegacyScreenDeploymentPreimageV1`,
`compute_legacy_screen_deployment_identity`.

**What P013 changes in the shared region.** Four things, and only four:

1. the module docstring, blob line 1 — *"Canonical identity formulae from brief section 6.7."*
   becomes *"Canonical shared identity documents and formulae."*;
2. the import prologue — adds `math`, `re`, `unicodedata`, adds
   `from collections.abc import Iterable, Mapping`, widens `typing` to
   `Annotated, Any, Literal, Self, TypeVar`, widens `pydantic` to eight names, and adds
   `from .base import NonEmptyStr, Sha256`;
3. **`_json_value`, blob lines 43-46** — the F3 change: a non-finite `Decimal` now raises
   `ValueError("non-finite Decimal values are not canonical JSON")` instead of being formatted;
4. the `canonical_json` docstring, blob line 55 (the word *"shared"* added). Its body at blob
   lines 57-63 is byte-identical to base.

The base tail `_hash_named_parts` through `compute_family_id` is retained verbatim at P013 blob
lines 515-626.

#### Overlap classification

| Kind | Finding |
|---|---|
| **Name collisions** | **None.** No module-level name is introduced by both new blocks. The closest pair is P013's `_compute_typed_identity_digest` and P020's `_digest`; they are distinct names with distinct signatures. |
| **Insertion-point overlap in the bodies** | **None.** P013 inserts after base line 40; P020 appends after base line 154. A three-way merge places both blocks without contest. |
| **Textual overlap** | **Confined to the import prologue, base lines 1-14.** Two genuine conflicts: (a) both sides insert a *different* `collections.abc` import at the same anchor before base line 7; (b) both sides rewrite base line 12, `from pydantic import BaseModel`. Both are resolvable by union, not by choice. |
| **Semantic overlap** | **One, and it is the substantive item:** non-finite `Decimal` handling. P013 refuses inside the shared serializer (`1e9682ba` lines 43-46); P020 refuses in a caller-side walker `_require_finite_decimals` (`fa57a771` lines 210-225), raising `ValueError` with a `NONFINITE_DECIMAL:` token and a field path, and additionally `TypeError` with a `FLOAT_MEMBER:` token for a `float` member. |
| **Latent dependency** | P020's `from .package import AccountSnapshot` makes the merged `identity.py` depend on `package.py`, which **P020 also changes** (blob `e24a5aa6` at `a4e79fbe`, `42f99571` and `da1fb184`; `a7e03268` at `b9b72f85`). Recorded as MEDIUM/latent at `P13M:412`; confirmed here by `git rev-parse`. |

**Import-cycle check (performed, negative).** No cycle is created.
`P20/MTC_COMMAND_CENTER/contracts/mtc_contracts/package.py:11-12` imports only
`from .base import ContractModel, NonEmptyStr, Sha256, require_utc` and
`from .sizing import SizingRequest`; `sizing.py:12` imports only from `.base`; `base.py`
defines `Sha256` at `:15`, `NonEmptyStr` at `:16` and `require_utc` at `:92`. None of the three
imports `identity`. `base.py` (blob `e991f746`) and `sizing.py` (blob `3957ac2f`) are
byte-identical at `a4e79fbe`, `42f99571`, `da1fb184` and `b9b72f85` — neither branch touches
them, so both branches' `from .base import ...` lines resolve in the merged tree.

### 2.2 Proposed merged structure

The merge is a **union, with one union-resolved prologue**, in this exact order. It preserves
both branches' requirements and overwrites neither.

1. **Module docstring** — P013's line. P020 did not change this line at all, so taking P013's
   overwrites nothing of P020's.
2. **Import prologue — union, not choice.** Standard library `hashlib`, `json`, `math`, `re`,
   `unicodedata`; `from collections.abc import Iterable, Mapping, Sequence` (the union of
   P013's `Iterable, Mapping` and P020's `Mapping, Sequence`);
   `from datetime import date, datetime`; `from decimal import Decimal`;
   `from enum import Enum`; `from typing import Annotated, Any, Literal, Self, TypeVar`
   (P013's widening already contains P020's `Any`);
   `from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr,
   ValidationError, field_validator, model_validator` (the union of P013's eight names and
   P020's `ValidationError`); `from .base import NonEmptyStr, Sha256, require_utc` (the union
   of P013's two and P020's one); `from .package import AccountSnapshot` (P020).
3. **`_FrozenIdentityDocument`** (P013) — unchanged.
4. **`_json_value` carrying P013's F3 guard** (P013 blob lines 36-51) — unchanged. This is the
   member P013 must not lose: it is the ratified F3 contract
   (`P13/MTC_COMMAND_CENTER/contracts/CHANGELOG.md`, first bullet of the 2026-09-13 section;
   `H13:26`; `P13M:85`).
5. **`canonical_json`** — P013's docstring, byte-identical body. Finite bytes and hashes stay
   unchanged, which is what keeps every frozen digest in *both* test suites valid.
6. **P013's inserted block in full**, in P013's own order: the parameter-lowering grammar,
   `ParamHashPreimageV1` and `compute_param_hash`, `SearchRegime`, `SimulatorClass`,
   `RegisteredParameterDefinition`, `PreregisteredSpacePreimageV1` with
   `project_preregistered_space` and `compute_preregistered_space_hash`, and
   `LegacyScreenDeploymentPreimageV1` with `compute_legacy_screen_deployment_identity`.
7. **The base tail unchanged**: `_hash_named_parts`, `make_candidate_id`,
   `compute_package_hash`, `compute_evaluation_run_hash`, `compute_deployment_identity_hash`,
   `make_trial_id`, `make_run_id`, `compute_family_id`. Both branches keep these byte-identical
   today and the merged file must too, because
   `P20/MTC_COMMAND_CENTER/contracts/tests/test_p020_identity.py:681-715`
   (`test_original_identity_formulae_keep_their_exact_member_sets`) asserts their exact
   parameter lists, and `PKT13:33` requires the six-member `evaluation_run_hash` to remain
   unchanged.
8. **P020's appended block in full**, in P020's own order: `_SHA256_HEX_CHARS` and the two
   field frozensets, `_digest`, `_require_sha256`, `_require_text`, `_require_relative_path`,
   `_require_finite_decimals`, `_require_schema_valid`, `compute_account_snapshot_id`,
   `compute_dataset_manifest_sha`, `compute_selected_dataset_hash`.

**Why both non-finite guards must stay, and why keeping both is safe.** They are not duplicates
of one another:

- P020's `_require_finite_decimals` runs **before** serialization —
  `compute_account_snapshot_id` calls it at `fa57a771` line 262 and digests at line 264. It
  therefore still produces P020's exact typed message with its `NONFINITE_DECIMAL:` token and
  field path, and still rejects a `float` member with `FLOAT_MEMBER:`, which P013's guard does
  not do at all.
- P013's `_json_value` guard runs **inside** `canonical_json` and therefore protects *every*
  caller in the package, including callers P020 has not written and the eight base formulae
  that route through `_hash_named_parts`.

The call order preserves P020's error surface exactly, and nothing of P020's is overwritten.
That is the concrete reading of the owner's *"reconcile both requirements"*.

### 2.3 The one concrete cross-branch regression, and the amendment that resolves it

This lane found exactly one place where the merged file changes a currently-GREEN P020 test.

`P20/MTC_COMMAND_CENTER/contracts/tests/test_p020_identity.py:245-248`, inside
`test_c14_helper_refuses_nonfinite_decimals_that_bypass_validation` (`:229`), asserts that the
shared serializer *"alone would spell NaN/Infinity as an ordinary string"* (`:245`) and then
calls `canonical_json` on the bypassed dump twice inside one `assert` (`:246-248`).

Under the merged serializer that `canonical_json` call **raises** instead of returning a
string, so the assertion never evaluates and the test errors before reaching its real subject —
the `NONFINITE_DECIMAL` refusal at `:249-250`. Four parametrized cases are affected:
`equity_nan`, `margin_inf`, `bucket_neg_inf`, `position_nan` (`:219-227`).

**The exposure is exactly this and no more.** A recursive grep for `NaN` or `Infinity` across
`P20/MTC_COMMAND_CENTER/contracts/tests/` returns exactly one file, `test_p020_identity.py`;
inside it, the only line combining `canonical_json` with a non-finite value is `:246`. No other
P020 contracts test depends on the permissive serializer.

**Required amendment — P020-owned under D-P20-3, because it is P020's own test file.** Replace
the "spelled as an ordinary string" premise with the refusal the merged serializer now gives:
assert that `canonical_json` on the bypassed dump raises, and leave `:249-250` untouched so the
`NONFINITE_DECIMAL` refusal remains the assertion of record. **The test must be amended, not
deleted** — `PKT13:22`: *"No default, placeholder, sentinel, caller label, or passing component
test can stand in for an owner contract or package acceptance."* Deleting the C14 helper test
would remove P020's own proof that a `model_construct` bypass never hashes.

**Everything else in that file survives unchanged**, because P013's change preserves finite
bytes and hashes. P013 pins this itself at
`P13/MTC_COMMAND_CENTER/contracts/tests/test_identity.py:194-199`
(`test_direct_canonical_json_finite_decimal_bytes_and_hash_are_unchanged`), which asserts the
exact serialized bytes for `Decimal("1.500")` and their SHA-256
`8055e491ffbb321194046ac9588a95f9b696711f3fd408d7acbde634f8ae1b98`. That is precisely the
property P020's frozen-digest tests need —
`test_c01_snapshot_id_matches_frozen_preimage_and_digest` (`:134`), `test_c02` (`:151`),
`test_c04` (`:180`), `test_c05` (`:190`),
`test_authoritative_zero_minima_are_preserved_in_canonical_identity` (`:287`),
`test_lead_c06_raw_manifest_and_csv_digests_match_frozen_literals` (`:440`) and
`test_lead_c06_selected_dataset_hash_matches_frozen_preimage_and_digest` (`:464`).

### 2.4 Ownership sequence

Under D-P20-3 the writer is P020 and only P020. Every act is assigned below.

| Step | Act | Owner | Prerequisite | Authorized today? |
|---|---|---|---|---|
| **I-1** | Record D-P20-3 as a `DECISIONS.md` row so the one-writer assignment is repository-resident rather than chat-resident (section 4). | Owner, plus whichever Lead holds `DECISIONS.md` write authority | Owner answer already given, 2026-09-13 | **NOT AUTHORIZED TODAY.** No `DECISIONS.md` write authority for this reconciliation is recorded anywhere this lane read, and `PKT20:239` (NV-07) notes the same file carries a live three-way divergence. |
| **I-2** | P020 brings the `a4e79fbe..da1fb184` `identity.py` change onto its branch, producing the union file of section 2.2, in one commit whose message names both owner records. | **P020 Lead** (sole writer) | I-1; P013 head `da1fb184` frozen and clean (`H13:11`, `:16`) | **NOT AUTHORIZED TODAY.** P020 is `PARKED`: *"After RELEASE remain parked for Claude ownership transfer; do not auto-resume."* (`H20:15`); `H20:118` requires Mentor RELEASE and an explicit ownership claim first. |
| **I-3** | P020 amends `test_p020_identity.py:245-248` per section 2.3. | **P020 Lead** | I-2 | **NOT AUTHORIZED TODAY** (same gate as I-2). |
| **I-4** | P020 runs the combined contracts suite on the merged file and records the RED/GREEN evidence of section 2.5. | **P020 Lead** | I-2, I-3 | **NOT AUTHORIZED TODAY.** |
| **I-5** | Independent review of the merged file at one frozen head, at the tier fixed in section 2.6. | Exact review roster plus independent Lead reproduction | I-4 | **NOT AUTHORIZED TODAY.** Requires a fresh roster booking: `H13:92-94` states the current Sol/Opus/Gemini results *"apply only to frozen head `da1fb184`. Any source/head change invalidates the acceptance evidence."* |
| **I-6** | P013 rebases its branch onto the merged `identity.py` and re-runs its own 219-test suite unchanged. | **P013 Lead** | I-5 | **NOT AUTHORIZED TODAY.** `H13:103-107` makes *"shared-path writer collision"* and head/diff drift stop conditions; `H13:98-101` requires waiting for *"separately authorized integration"*. |
| **I-7** | P013 re-verifies branch, head and clean status plus both diff hashes at the new head, and records a superseding verification entry. | **P013 Lead** | I-6 | **NOT AUTHORIZED TODAY.** Note that `a38248a967d5f9838bf19c13ef4fba8b79f71965` and `46089d3fca63ee263e7389ebe87f360f0303af720bd86742ab315dd1a50ed5b2` (`H13:12-13`) are identities **of `da1fb184`** and cannot survive a rebase; a new pair must be computed and recorded, never the old pair re-quoted. |

**What "preserve P013's existing changes" means operationally.** `da1fb184` and its fourteen
approval-trailered commits are not to be rewritten, squashed, or replayed as fresh authorship.
If step I-6 produces new commit ids, `da1fb184` must remain reachable and named in the record,
because the whole acceptance evidence — `219 passed`, both exact-model verdicts and the Gemini
corroboration — is pinned to it (`VER13:15`, `:46`; `H13:57-64`).

### 2.5 RED/GREEN evidence expected from the merged file

Each row states what must fail without the merged guard and pass with it. None of this is
authorized to be run today; it is the evidence contract the authorized run must satisfy.

| # | Property | RED (must fail without it) | GREEN (must pass with it) | Source of the requirement |
|---|---|---|---|---|
| **G-1** | F3 survives the merge. | A serializer that formats a non-finite `Decimal` as a plain string accepts a `Decimal("NaN")` member. | `P13/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py:59-65` (`test_t1_decimal_nan_and_infinity_are_refused`) passes unchanged. | `H13:26`; `PKT13:18` |
| **G-2** | Finite bytes and hashes are unchanged by the merge. | Any edit that alters finite `Decimal` rendering. | `test_identity.py:194-199` still yields the pinned bytes and SHA-256 `8055e491...`. | `VER13:32-33`; `P13M:85` |
| **G-3** | P020's snapshot refusal keeps its own typed token and field path. | `compute_account_snapshot_id` on a `model_construct` bypass returns a digest, or raises with the wrong token. | `test_p020_identity.py:229-250` passes with `NONFINITE_DECIMAL` still matched, after the `:246` premise is amended. | `fa57a771` lines 210-215 and 262 |
| **G-4** | P020's float-member rule survives. | A `float` member of a snapshot is silently digested. | `_require_finite_decimals` still raises on `FLOAT_MEMBER` — P013's guard does not cover this case, so the helper must remain in the merged file. | `fa57a771` lines 217-218 |
| **G-5** | The eight base formulae are untouched. | Any signature change to `compute_package_hash`, `compute_evaluation_run_hash` or `compute_deployment_identity_hash`. | `test_p020_identity.py:681-715` passes unchanged. | `PKT13:33` |
| **G-6** | Every P020 frozen digest literal still matches. | Any change to finite serialization. | `test_p020_identity.py:134`, `:287`, `:440`, `:464` pass unchanged. | `H20:19` — exact record values preserved, no normalization |
| **G-7** | Every P013 test still passes at the new head. | — | `test_identity.py` (31 test functions) and the full 219-test combined suite pass. | `H13:57`; `VER13:46` |
| **G-8** | No import cycle and no new runtime dependency. | A merged prologue in which `package`, `base` or `sizing` imports `identity`. | The merged module imports cleanly with `package.py` at P020's blob `a7e03268`. | section 2.1 import-cycle check |

`219 passed` is quoted from `VER13:46` and `H13:57`; it was **not** reproduced by this lane
(section 7).

### 2.6 Required review tier for the merged file

**T0, not T1 — and the reason is the file, not the package.**

- `POL:18` defines T0 as *"Sizing, orders, recovery, parity, economics, security, credentials,
  live host/deploy; binding safety, acceptance or evidence logic, including policy changes"*,
  requiring *"Fresh exact `claude-opus-5` **and** `gpt-5.6-sol`, both `xhigh`, plus fresh
  mandatory `gemini-3.7-flash-high` corroboration on the same packet; independent Lead
  reproduction"*.
- `POL:25-26`: *"Highest applicable consequence wins. Extension, line count, a 'docs' label, or
  small diff cannot downgrade safety, acceptance, economic meaning, executable evidence, or a
  changed refusal gate."*
- `identity.py` is acceptance-evidence logic on both sides. It produces the digests that
  identify accepted evidence — `compute_evaluation_run_hash`,
  `compute_deployment_identity_hash`, `compute_account_snapshot_id`,
  `compute_selected_dataset_hash` — and the merge **changes a refusal gate**: `canonical_json`
  goes from formatting a non-finite `Decimal` to refusing it, for every caller in the package.
- Precedent inside P013 itself: the bounded slice was run at T0 with the reason given in one
  line, `VER13:4` — *"Tier: T0 because D-05 changes binding acceptance-evidence logic."*
- Precedent on the P020 side: `PLAN:508` — *"**Audit tier:** **T0** — it decides the trading
  model's research counterpart **and delivers the shared allocator**"*.

WP-P0-13's package-level tier is T1 (`PLAN:415`: *"**Protected surfaces:** research tooling
(not money-adjacent). · **Audit tier:** T1"*), and **that package tier does not govern this
file.** Under the highest-applicable-consequence rule the merged `identity.py` is a T0 review.
The review must also be fresh: `H13:92-94` states the existing exact-model results *"apply only
to frozen head `da1fb184`"*, that *"[a]ny source/head change invalidates the acceptance
evidence and requires the repository's then-current T0 roster"*, and *"do not substitute a
cheaper model for a required exact role"*.

A T1 review of the merged file would be an error of tier, not a matter of economy. This lane
records it as a requirement, not a preference.

---

## 3. `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py` — P020 remains sole writer

### 3.1 Current state, verified

| Commit | blob | Bytes | Lines |
|---|---|---|---|
| `a4e79fbe` (P013 base) | `2f16fffd08a1ca4891060205a456282665f252f3` | 83,403 | 1,856 |
| `da1fb184` (P013 head) | `2f16fffd08a1ca4891060205a456282665f252f3` | 83,403 | 1,856 |
| `b9b72f85` (P020 head) | `21574df7861c79cc430cb41fff5ad0070097e01f` | 89,721 | 1,997 |

**P013 changes this file by exactly zero bytes**: the blob is identical at its base and at its
head (`git rev-parse`, both `2f16fffd`). P020's version differs from that same blob by 189
changed lines, net +141. So this is not a two-writer collision today; it is a **guaranteed
future collision** the moment P013 caller integration is authorized, exactly as `P13M:408`
records it (*"HIGH — future collision, already diverged"*).

**The ownership rule is not in dispute.** Three independent sources agree:

- Owner decision **D-P20-3**: *"P020 owns writes to `identity.py` and `mega_walk_forward.py`
  while active … Other lanes remain read-only on these shared files."*
- `PLAN:507` — *"**Protected surfaces:** **the canonical research engine, the one shared Risk
  Allocator implementation, and the validation tools that call the engine.**"*, with
  `PLAN:489` naming the surface by path and line:
  *"the current canonical path `03_QUANTLENS/tools/mega_walk_forward.py:648 simulate_slice`"*.
- `P13/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/__init__.py:7-8` —
  P013's own package docstring lists *"the migrated `mega_walk_forward.py` caller"* under
  *"Not built here"*.

**Plan citation drift to record.** `PLAN:489` pins the canonical function to line 648. In the
base blob `2f16fffd` line 648 *is* `def simulate_slice(...)`. In P020's head blob `21574df7`
line 648 is `def _resolve_exit_geometry(...)`, and `simulate_slice` has moved to line 675. The
path-and-name half of that citation still resolves; the line half does not. Anyone quoting
`PLAN:489` forward against the current P020 head must re-pin the line.

### 3.2 What P020's change did, and what it deliberately did not do

P020's edit is a **dispatch seam**, not a completed migration. Reading `21574df7` directly:

- Two pure extractions from the legacy body, so one statistics schema serves both paths:
  `_resolve_exit_geometry` (line 648) and `_slice_stats_from_trades` (line 814), whose
  docstring states it *"[o]wns the canonical SliceStats shape for every execution path … so no
  second statistics schema exists"*.
- `simulate_slice` gains two keyword parameters, `p020_profile=None, p020_semantics_id=None`
  (line 675), and calls `_check_p020_dispatch` (line 947) **before any legacy work**.
- Two constants: `P020_SEMANTICS_ID = "2.1.0"` (line 933) and
  `REFUSED_P020_CONTEXT_REQUIRED = "REFUSED_P020_CONTEXT_REQUIRED"` (line 934).
- `simulate_slice_p020` (line 968) requires an explicit profile, calls
  `p020_profile.require_executable_provenance()`, and lazily imports `p020_simulator`.
- The successor path stamps its own ledger with
  `"semantics_id": P020_SEMANTICS_ID` and `"acceptance_status": "RESEARCH_ONLY_NOT_ACCEPTED"`
  (lines 1001 and 1003).

**Two facts about that seam matter to P013 and are easy to misread:**

1. **Nothing inside this file supplies a profile.** The four `simulate_slice` call sites in
   `_worker_impl` — lines 1451, 1452, 1454 and 1495 — pass no `p020_profile` and no
   `p020_semantics_id`, so `_check_p020_dispatch` returns immediately and the legacy body runs.
   The successor path exists and is fail-closed, but the walk-forward driver does not yet run
   it. This is consistent with, and is the code-level shape of, the two P020 acceptance rows
   still blocked on *"canonical-path migration not performed"* (`PKT20:61`, `:62`).
2. **The file's own successor path labels itself non-accepting.** The literal
   `RESEARCH_ONLY_NOT_ACCEPTED` at line 1003 is the reason `PKT13:31`'s rule — *"No `ACCEPTED`
   status label is trusted"* — is a live requirement rather than a hypothetical one.

### 3.3 The emission seam P013 will later attach to (interface, not edits)

P013 never edits this file. The attachment point is an **interface seam that P020 exposes**,
and the design already names both its identity and its timing:

- *"Post-migration `mega_walk_forward.py` | **Sole direct caller of `TrialCatalogWriter`**; no
  best-only JSON remains authoritative after verified migration. **PROVISIONAL-ON-P020**
  because the direct caller is the migrated canonical path. | **Once, at completed-run
  finalization, after every terminal trial and family statistic is available.**"* (`DSGN:486`)
- *"WP-P0-08 identifies the post-migration `mega_walk_forward.py` path as the single direct
  emitter"* (`DSGN:382`).
- *"A completed run that has no strategy × symbol × timeframe cell coordinates cannot have been
  executed as a cell, so the values are a property of the completed run, not an invention of
  the writer."* (`DSGN:634-640`)

**Where that seam lands in the current bytes.** `_worker_impl` (line 1395) returns one dict per
strategy × symbol × timeframe cell, already carrying `strategy`, `symbol`, `timeframe` and
`classification`; `_worker` (line 1378) then stamps `exit_mode`, `engine_version` and
`grid_stride` onto every returned row; `main()` writes the aggregate to
`MEGA_walk_forward_results.json` (lines 1868-1869). That per-cell dict is the natural
completed-run finalization point, and it is where the three coordinates already exist as
emitted values rather than as path segments — which is precisely the property B-15 demands.

**But the per-trial channel does not exist yet.** The per-parameter loop builds a `configs`
list in memory, one entry per parameter set, each with `params`, `fold_train`, `fold_test`,
`lockbox` and two train means (lines 1432-1469). Only `sharpe_train_pool` aggregates
(`trial_count`, `trial_sr_std`, `trial_sr_max`, `boot_p_value`, lines 1608-1610) and one
`summary.best_params` survive into the returned dict. The plan requires *"one row per trial"*
(`PLAN:412`), and `DSGN:486` says *"no best-only JSON remains authoritative after verified
migration"*. So the migration owes P013 a per-trial terminal record that today is computed and
then discarded.

**P013's side of the seam is already built and already fail-closed.** The bounded slice exposes
`CompletedRunInput` with six declared members, `extra="forbid"` and a reserved-key
pre-validator (`P13M:98`), and the lineage classifier refuses `FULL_EVIDENCE_SINK`
unconditionally with
*"FULL_KERNEL_SIMULATION requires a verified canonical-path receipt from an accepted WP-P0-20;
B-01 is open (WAIT_P020_ACCEPTANCE)"*
(`P13/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py:424-428`).
Nothing on the P013 side needs to be opened to make the seam attachable; what is missing is on
the P020 side.

### 3.4 What P020 must expose for P013 to attach without editing the file

Each item names who must settle it and what would evidence it. **None of these is a request
this lane is authorized to make of P020**; they are the contents of a future, separately
authorized coordination.

| # | What P020 must expose | Why P013 cannot supply it | Source | Owner |
|---|---|---|---|---|
| **M-1** | A **declared cell-coordinate channel** carrying the completed run's `strategy`, `symbol`, `timeframe` — its name, its type, and the rule that the factory may read no other source. | B-15 is open and explicitly forbids P013 from inventing the member: *"This design lane will not add the member on its own authority: assembling an input list is the act that produced this finding."* (`DSGN:1706-1716`) | `DSGN:1706-1716`; `PKT13:75` | **P013 build owner jointly with the WP-P0-08 migration owner** — `DSGN` names both. Explicitly *"not P0-20-gated"*. |
| **M-2** | A **completed-run finalization hook** that fires once, after every terminal trial and family statistic is available. | The current driver has no such hook; `main()` writes an aggregate JSON and returns. | `DSGN:486` | P020 / WP-P0-08 migration owner |
| **M-3** | **Per-trial terminal records**, not best-only summaries. | `configs` is discarded; only pool aggregates and `best_params` are returned (lines 1432-1469, 1608-1610). | `PLAN:412`; `DSGN:486` | P020 / WP-P0-08 migration owner |
| **M-4** | The **opaque `P020VerifiedCanonicalPathResult` and its verifier seam**, in the exact narrow form `verify(receipt_bytes, completed_run_identity) -> P020VerifiedCanonicalPathResult or REFUSED(CANONICAL_RECEIPT_MISSING_OR_INVALID)`. | P013 must verify, not trust; and it must not reimplement P020 internals. | `MAP13:60-64`; `PKT13:31` | P020 (B-01 member 4, section 1) |
| **M-5** | The **accepted rejection taxonomy values** feeding `rejection_reasons`. | *"B-06 values wait for P020's accepted taxonomy."* | `PKT13:208`, `:130` | P020 (B-01 member 5) |
| **M-6** | **Stable shared-allocator and canonical-kernel import identities**, as digests, so the row's `simulator_class` and `deployment_identity_hash` mean something. | These are two of the twelve bundle members; P013 consumes digests only. | `MAP13:54-55`; `PLAN:509` (import identity *"proven by import, not asserted"*) | P020 (B-01 member 2) |

**The attachment rule, stated once.** P013's integration is an *adapter that consumes a frozen
P020 seam*, never an edit inside P020's protected surface. `MAP13:70-71` assigns it exactly:
P020 owns *"its accepted dependency bundle, canonical receipt schema/issuer/verifier,
P020-owned verified result, acceptance tests and release evidence"* and must not *"edit P013
worktree"*; P013 owns *"[a]dapter consuming the frozen verifier seam; lineage capability
binding; P013 D026 modified-copy tests"* and must not *"[r]eimplement P020 battery, allocator,
receipt issuer, or acceptance logic"*.

### 3.5 Status and authorization

**BLOCKED_ON_P020_B01, additionally BLOCKED_ON_OWNER, additionally BLOCKED_ON_OTHER (B-15).**
This matches `P13M:379` row 7 and is not weakened by anything in this plan.

- The authorization record independently excludes it today:
  `P13/DECISIONS.md:24` — *"Excluded are the full writer, selection/artifact pipeline, reader
  adoption beyond D-05, **caller integration**, P020 acceptance, push/PR/merge,
  host/credentials/trading/deploy."*
- The handoff makes the collision a stop condition: `H13:104` lists *"shared-path writer
  collision"*, and `H13:100-101` says to *"coordinate one writer for shared files with
  P020/P022 **if later authority is granted**"*.
- `PLAN:414` states why the ordering cannot be reversed: *"The catalog is the evidence surface;
  it is written against the migrated canonical path or its rows are not acceptance-bearing."*

**Nothing about this file is authorized today** — not an edit, not a branch, not a preparatory
patch against P020's bytes. The only P013-side work that survives P020's continuing changes to
this file is design-only: an adapter interface note written against the six M-items above,
which names no line and no byte of `mega_walk_forward.py`. `P13M:379` classifies its rework
risk as **HIGH** for exactly this reason: *"anything written against today's
`mega_walk_forward.py` is written against a file P020 is actively changing."*

---

## 4. `DECISIONS.md` — safe three-way reconciliation order

### 4.1 The four blobs, structurally

Blob ids are taken from `P13M:409`; all four resolve in the shared object store and were read
with `git show`.

| Branch | Blob | Bytes | Lines | Delta against base |
|---|---|---|---|---|
| **base** | `4d5c3dfcaef7c0a3a547e5a6eca9a73d2033b0c8` | 26,429 | 75 | — |
| **P013** | `3c7d0d0ba47c3742945089d0516af4ea47bcea36` | 28,918 | 82 | +5 prose lines at the 15/16 boundary, +2 table rows at the top of the table |
| **P031** | `a3b9390071277e55127911219109d02e31c449da` | 53,199 | 76 | +1 table row at the top of the table |
| **CT13** | `8e8772d14a5d5d7febe5b93a437d7e650dd37af3` | 26,947 | 79 | +4 lines appended at the end of file |

**Base layout.** Prose header lines 1-14; blank line 15; table header and separator at lines
16-17; 58 rows at lines 18-75. The table is date-descending from `OD-20260911-MATERIALIZER-1`
(line 18) down to `D001` (line 71), after which four later rows sit **out of date order** at
lines 72-75: `OD-20260911-R34-1`, `OD-20260911-R35-1`, `OD-20260911-FUNDING-1`,
`OD-20260912-P012-RELEASE-1`. The file therefore already contains a working precedent for
appending at the tail.

**P013's delta.** A four-line prose paragraph plus a blank line become lines 16-20, recording
that *"decisions 128 and 88 are preserved exactly as summarized in [the] packet … their
underlying earlier records are not repository-resident, and this package does not reinterpret
them"* (`P13/DECISIONS.md:16-19`). The table header moves to 21-22, and two new rows are
inserted immediately below the separator: `OD-20260913-P013-CONTRACT-DEFAULTS` (line 23) and
`OD-20260912-P013-CONTRACTS` (line 24). 75 + 5 + 2 = 82.

**P031's delta.** One new row, `OD-20260912-P031-M1-SEQUENCING`, inserted immediately below
the separator at line 18. 75 + 1 = 76. That single row accounts for **+26,770 bytes** — it is
roughly the size of the entire base file. A reviewer must diff this file **by decision id, not
by line**, or one row will visually swamp the change.

**CT13's delta.** Two blank lines and a new prose section at lines 78-79,
`## OD-20260913-CLAUDE-TAKEOVER — owner continuation priority`, appended after the last table
row. 75 + 4 = 79.

### 4.2 Where the conflict actually is

| Insertion point (base coordinates) | P013 | P031 | CT13 | Verdict |
|---|---|---|---|---|
| Between base lines 15 and 16 (prose) | inserts 5 lines | — | — | **Clean.** Only one writer. |
| Immediately after base line 17 (the table separator) | inserts 2 rows | inserts 1 row | — | **CONFLICT — add/add at one anchor.** Content is disjoint; only the ordering is contested. |
| After base line 75 (end of file) | — | — | appends 4 lines | **Clean.** Only one writer, and the anchor is untouched by the other two. |

There is exactly **one** contested hunk, and it is not a semantic disagreement: no row id is
defined twice, no existing row is edited by anybody, and no row is deleted by anybody. Every
change to this file, on all three branches, is an insertion.

### 4.3 Safe reconciliation order

The rule below is stated so the resolution is reproducible by a second person and is not a
judgement call.

**R-1 — Append-only, always.** No existing row is edited, re-worded, re-dated, re-ordered or
removed by the reconciliation. This is the concrete meaning of the owner's *"do not overwrite
either branch's work"* for this file.

**R-2 — Preserve P013's prose paragraph verbatim** at the 15/16 boundary. It carries the
decision-128/88 preservation statement, which `P13/DECISIONS.md:17-18` says is the only
repository-resident record of those two decisions (*"their underlying earlier records are not
repository-resident"*).

**R-3 — Resolve the contested hunk as a union in one deterministic order: decision date
descending, then decision id ascending as the tiebreak.** Applied to the three already-committed
rows that all target the same anchor, that yields, top to bottom:

1. `OD-20260913-P013-CONTRACT-DEFAULTS` — 2026-09-13
2. `OD-20260912-P013-CONTRACTS` — 2026-09-12
3. `OD-20260912-P031-M1-SEQUENCING` — 2026-09-12 (after the P013 row on the id tiebreak)

followed by the unchanged base row `OD-20260911-MATERIALIZER-1`. Stating the tiebreak matters:
without it, the two 2026-09-12 rows have no defined order and a second merger could produce a
different file from the same inputs.

**R-4 — Every *future* row is a tail append, after `OD-20260912-P012-RELEASE-1`.** The base
file already does this for its four most recent rows (base lines 72-75), and a tail append has
no contested anchor, so it cannot produce this conflict again. This is the single change of
practice that prevents the next three-way collision.

**R-5 — Leave CT13's appended prose section where it is, and record the format divergence
rather than resolving it.** `## OD-20260913-CLAUDE-TAKEOVER` is a heading-plus-prose section,
not a four-column table row. The packet that proposes a new row describes the file's form as
the *"four-column shape of `:16-78`"* (`PKT20:137`). Whether `OD-` records may take a prose
form is a governance question about this file's schema; a merger who silently converts the
section into a row, or a row into a section, would be making that decision by hand. Record it;
do not decide it in a merge.

**R-6 — Order of operations across branches.** Because the only contested anchor is the top of
the table, the reconciliation is order-independent *if* R-3 is applied, and order-dependent if
it is not. Recommended sequence, once authorized: apply the base, then P013's prose and rows,
then P031's row under R-3, then CT13's tail section under R-5. The result is reproducible from
the four blobs plus R-3.

**R-7 — No push, PR or merge is implied by any of this.** `VER13:82` — *"No push, PR, merge, or
master integration is authorized."* Reconciliation of the file contents and integration of the
branches are separate acts, and only the first is described here.

### 4.4 The writers this file does not yet have, but is about to

Two further rows are already in the queue for the same file, and both should follow **R-4**
(tail append), not the top-insert that produced the current conflict:

| Candidate row | Status | Where it should go | Source |
|---|---|---|---|
| `OD-20260913-P020-SCOPE-1` | **DRAFT, UNEXECUTED**, pending owner answer D-P20-1 | Tail append under R-4 | `PKT20:142`; `PKT20:359` — *"No `DECISIONS.md` row is added until the owner answers D-P20-1."* |
| A row recording **D-P20-3** itself (the one-writer assignment for `identity.py` and `mega_walk_forward.py`) | Owner answered in chat 2026-09-13; **not repository-resident** | Tail append under R-4 | Section 2.4 step I-1; `PKT20:194` is the question it answers |

`PKT20:239` (NV-07) already flags the hazard: *"Recording the §4 row would touch
`DECISIONS.md`, which carries a live three-way divergence … No Git write was made."* Adding a
fourth top-insert to a file that already has an unresolved three-way top-insert conflict would
make the hunk strictly harder to resolve, for no benefit — the row's position in the table
carries no meaning that R-4 does not preserve.

**A note on D-P20-3 specifically.** Until it is recorded, the one-writer assignment for two
protected surfaces exists only in chat. Every step in sections 2.4 and 5 that depends on "P020
is the sole writer" therefore rests on an unrecorded decision. That is why step I-1 is first in
the ownership sequence, and why this plan does not treat the assignment as already
repository-binding.

### 4.5 Authorization

**NOT AUTHORIZED TODAY.** This lane performed no Git write of any kind and made no change to
`DECISIONS.md`. The reconciliation described here is cross-package — it touches rows owned by
P013, P031 and the CT13 takeover branch — so it is not decidable by any single package Lead,
on the same reasoning `PKT20:194` gives for D-P20-3: *"**Not Lead-decidable** — cross-package
ownership."* Who may perform it, and on which branch the reconciled file should first exist,
are open questions this plan does not answer (section 7).

---

## 5. Dependency-resolution sequence — from today's state to a B-01 closure

Ordered steps. Every step carries an owner, a prerequisite, and the concrete artifact that
would evidence it. **Every step is marked for authorization, and none of them is authorized to
this lane.** The four possible marks are:

- `NOT AUTHORIZED TODAY` — the act requires authority nobody currently holds, or explicitly
  excluded authority.
- `OWNER DECISION PENDING` — the act is an owner answer that has been asked for and not given.
- `APPROVED, NOT STARTED` — authority exists but a stated precondition is unmet.
- `DONE` — already satisfied; listed so the sequence is complete.

Steps are numbered by phase. A phase does not begin until every prerequisite named inside it is
satisfied; steps inside a phase may run concurrently unless a prerequisite says otherwise.

### Phase A — governance records (owner acts)

| Step | Act | Owner | Prerequisite | Evidence artifact | Authorization |
|---|---|---|---|---|---|
| **A-1** | Answer **D1** — the 1D calibration window (the frozen 2048-row window *"exists for 15m/1h/2h/4h but cannot exist for 1D"*). | Owner | none | A recorded answer plus a re-frozen, T0-reviewed preregistration. | `OWNER DECISION PENDING` (`PKT20:191`; `H20:64`) |
| **A-2** | Answer **D-P20-1** — record `OD-20260913-P020-SCOPE-1` or not. | Owner | none | A `DECISIONS.md` tail row under section 4 R-4. | `OWNER DECISION PENDING`. **Answering it either way moves B-01 by zero** — the row itself *"[a]uthorizes no … B-01 closure"* (`PKT20:142`), and the owner has already said *"This does not satisfy P013 B-01."* |
| **A-3** | Answer **D-P20-2** — whether `check_p020_acceptance.py` may gain a research-closure criterion set. | Owner | none | A recorded decision; recommended answer is *"8/16 stays; add no criterion set now"* (`PKT20:193`). | `OWNER DECISION PENDING`. Editing the reporter is itself a T0 acceptance-surface change (`PKT20:88-89`). |
| **A-4** | Record **D-P20-3** as a repository row, so the one-writer assignment for `identity.py` and `mega_walk_forward.py` stops being chat-resident. | Owner plus the Lead holding `DECISIONS.md` write authority | A-2 (so both rows append together under R-4) | A `DECISIONS.md` tail row. | `NOT AUTHORIZED TODAY` — no such write authority is recorded; section 4.5. |

### Phase B — shared-file reconciliation (sections 2, 3, 4)

| Step | Act | Owner | Prerequisite | Evidence artifact | Authorization |
|---|---|---|---|---|---|
| **B-1** | Reconcile `DECISIONS.md` under R-1…R-7. | Cross-package; not Lead-decidable alone (`PKT20:194`) | A-4 | One reconciled file reproducible from the four blobs plus rule R-3. | `NOT AUTHORIZED TODAY` |
| **B-2** | Build the merged `identity.py` (section 2.2 union). | **P020 Lead**, sole writer | A-4; Mentor RELEASE and Claude ownership claim (`H20:15`, `:118`) | One commit naming both owner records; the union prologue; both non-finite guards present. | `NOT AUTHORIZED TODAY` |
| **B-3** | Amend `test_p020_identity.py:245-248` (section 2.3). | **P020 Lead** | B-2 | The amended test still asserting `NONFINITE_DECIMAL` at `:249-250`. | `NOT AUTHORIZED TODAY` |
| **B-4** | Run and record the G-1…G-8 RED/GREEN evidence. | **P020 Lead** | B-2, B-3 | A verification record with the exact suite result at one frozen head. | `NOT AUTHORIZED TODAY` |
| **B-5** | **T0** review of the merged `identity.py` — fresh exact `claude-opus-5` and `gpt-5.6-sol` at `xhigh`, plus `gemini-3.7-flash-high` corroboration, plus independent Lead reproduction. | Review roster | B-4 | Three fresh reports plus the Lead reproduction, all pinned to the new head. | `NOT AUTHORIZED TODAY` (`POL:18`; `H13:92-94`) |
| **B-6** | P013 rebases onto the merged file and re-runs its suite unchanged. | **P013 Lead** | B-5 | `219 passed` reproduced at the new head, plus a fresh diff-object / diff-SHA-256 pair replacing `a38248a9…` / `46089d3f…`. | `NOT AUTHORIZED TODAY` (`H13:98-107`) |
| **B-7** | Record a superseding P013 verification entry naming both the old accepted head `da1fb184` and the new one. | **P013 Lead** | B-6 | An updated verification record. | `NOT AUTHORIZED TODAY` |

Phase B is **independent of B-01**. It resolves a file collision; it closes no blocker. It is
listed first because `H13:104` makes *"shared-path writer collision"* a stop condition, so an
unreconciled `identity.py` blocks work that is otherwise unrelated to P020 acceptance.

### Phase C — WP-P0-20 package acceptance (this is the actual B-01 gate)

The eight live reporter blockers are `H20:40-49`. Closing them is P020 work; P013 has no step
inside this phase and must not attempt to shorten it.

| Step | Act | Owner | Prerequisite | Evidence artifact | Authorization |
|---|---|---|---|---|---|
| **C-1** | **Name the two failing frozen probes.** They are currently unnamed and deliberately not inferred. | **P020 Lead** | none | The two probe identities, then an assigned owner and remedy per probe. | `NOT AUTHORIZED TODAY` — P020 parked. Closes `frozen_probe_compatibility` (`PKT20:59`; NV-01 at `PKT20:223-225`). |
| **C-2** | **Perform the canonical-path migration**, then produce an independently verified real before/after on a frozen candidate, and a **per-consumer** dependent-tool audit. | **P020 Lead** with the WP-P0-08 migration owner | C-1 | A migrated caller; a recorded before/after naming the economic differences; a per-class disposition record that is *performed*, not proposed. | `NOT AUTHORIZED TODAY`. Closes `real_before_after` and `dependent_disposition` (`PKT20:61-62`). Section 3.2 shows the migration is not wired into the walk-forward driver today. |
| **C-3** | **Execute the preregistered benchmark** — freeze and T0-review the preregistration, run the locked 15-trial eligibility check, then the bounded measurement. | **P020 Lead** | A-1; Mentor RELEASE | A measured trials-per-hour figure on named reference hardware, the labelled O-28 extrapolation, and an explicit feasible/infeasible statement (`PLAN:510`). | `APPROVED, NOT STARTED` — *"It is APPROVED BUT NOT STARTED"* (`H20:21`), blocked on D1 and on the required T0 review of the preregistration (`H20:68`). Closes `real_benchmark`. |
| **C-4** | **P012 production cost admission, P012 full acceptance, and production admission.** | Owner plus P012 Lead plus venue/Bridge evidence | none inside P020 | An authentic own-account P012 production admission and an authoritative non-synthetic cost index. | `NOT AUTHORIZED TODAY`. These are the three class-B rows (`PKT20:57-60`); `production_admission` has **no MET branch at all** (`PKT20:60`). |
| **C-5** | **Fresh exact T0 roster on the frozen head.** | Review roster plus independent Lead reproduction | C-1…C-4 landed at one head | Three fresh reports at that head. | `NOT AUTHORIZED TODAY`. Closes the A-half of `independent_reviews` (`PKT20:64`). Note `PKT20:235-237` (NV-06): whether a fresh roster on `b9b72f85` would pass is unknown. |
| **C-6** | **Re-attest 17/17 enabled REQUIRED control coverage** against the canonical single run's nine reported gaps. | **P020 Lead** plus roster | C-5 | One record reconciling the five-fixture 17/17 figure with the canonical run. | `NOT AUTHORIZED TODAY` (`H20:31`; `PKT20:56`, `:214`) |
| **C-7** | **The package-acceptance act at one exact head.** | **P020 Lead** as a separate act | C-1…C-6 | A package-acceptance receipt whose SHA-256 is recorded, at a named 40-character head. | `NOT AUTHORIZED TODAY`. *"Mechanical rows are MET, but package acceptance remains a separate Lead act."* (`PKT20:183`, quoting `CHK:704`) |

**The phase-C caution.** No amount of P013 work shortens this phase, and no P013 artifact can
substitute for any step in it. `PKT13:22` — *"No default, placeholder, sentinel, caller label,
or passing component test can stand in for an owner contract or package acceptance."*

### Phase D — the B-01 artifacts themselves

Phase D cannot begin before C-7. Its six members are section 1.1's six rows; its evidence list
is `MAP13:76-81`, read directly.

| Step | Act | Owner | Prerequisite | Evidence artifact | Authorization |
|---|---|---|---|---|---|
| **D-1** | Publish `P020AcceptedCatalogueDependencyV1` with its twelve ordered members, populated from **accepted** bytes. | **P020** | C-7 | The typed document plus its focused tests. The bundle *"is an engineering proposal until P020 accepts and ratifies it; P013 must not populate it from the current research candidate"* (`MAP13:58`). | `NOT AUTHORIZED TODAY` |
| **D-2** | Publish the **canonical-path receipt** schema, issuer id and verifier id, plus the opaque `P020VerifiedCanonicalPathResult` behind the narrow seam `verify(receipt_bytes, completed_run_identity)`. | **P020** | C-7 | P020 tests proving *"malformed, wrong-issuer, wrong-run, wrong-import-identity and nonaccepted-package receipts all refuse"* (`MAP13:77`). | `NOT AUTHORIZED TODAY` |
| **D-3** | Publish `TrialRejectionTaxonomyV1` with its entries frozen at the accepted head. | **P020** | C-7 | A version-stamped taxonomy document; `TrialGateAggregator` validating every code against it. | `NOT AUTHORIZED TODAY` (`PKT13:130`, `:208`) |
| **D-4** | Independent **D026 RED/GREEN** on the verifier: a faithful implementation that trusts a receipt label or a research-candidate status **must accept** the modified copy in RED, and the frozen verifier **must refuse** it in GREEN. | P020 plus an independent auditor | D-2 | The RED/GREEN pair recorded at one head. | `NOT AUTHORIZED TODAY` (`MAP13:78`) |
| **D-5** | P013 adapter proof that **no public constructor or caller path can obtain `FullEvidenceSinkCapability`**. | **P013 Lead** | D-1, D-2 | A P013 test; the mechanism already exists in the sealed classifier at `stages_conservation_identity.py:414-436`. | `NOT AUTHORIZED TODAY` (`MAP13:79`; `PKT13:34`) |
| **D-6** | P013 reader proof that the acceptance reader does not import the writer or the classifier and maps **all** verifier failures to the single closed reason `CANONICAL_RECEIPT_MISSING_OR_INVALID`. | **P013 Lead** | D-2 | A P013 test; the import isolation is already structural (`trial_catalog/__init__.py:14-18`). | `NOT AUTHORIZED TODAY` (`MAP13:80`) |
| **D-7** | Protected CI green plus the required independent acceptance review **at the frozen P020 identity**. | Roster plus CI | D-1…D-6 | CI result plus review reports pinned to that identity. | `NOT AUTHORIZED TODAY` (`MAP13:81`) |
| **D-8** | **The P013 design re-audit** of `DSGN` at the accepted P020 head, resolving every `PROVISIONAL-ON-P020` marker, and re-pinning `PKT13:30`'s stale head `556639f591…` and `PLAN:489`'s stale line pin. | **P013 Lead** | D-7 | A dated re-audit record. | `NOT AUTHORIZED TODAY` (`DSGN:1445`; `PKT13:223`; `PKT20:211`) |
| **D-9** | **B-01 recorded as closed**, and the full-writer package authorized **separately**. | **P013 Lead** for the closure; **owner** for the authorization | D-8 | A closure record naming the accepted head and the twelve bundle member digests. | `NOT AUTHORIZED TODAY`. *"[A]fter actual P020 acceptance the Lead re-audits B-01 and authorizes the full-writer package separately."* (`PKT13:223`) |

### Phase E — what remains open after B-01 closes

Recorded so that D-9 is not misread as "the writer is unblocked". Closing B-01 closes one of
several gates.

| Still open after D-9 | Why | Owner | Source |
|---|---|---|---|
| **B-15** run-cell coordinate channel | Not P020-gated at all — *"This blocker is **not** P0-20-gated"* — and `CompletedRunInput` still declares no coordinate member. | P013 build owner jointly with the WP-P0-08 migration owner | `DSGN:1706-1716`; `P13M:354` |
| **B-04 / B-12 producer adoption** | Shapes are ratified; producers are not. The stage refuses truthfully today: *"param_hash has a ratified B-04 preimage, but producer inputs and adoption are unavailable in this legacy stage; no value may be computed, defaulted, or accepted"*. | WP-P0-04 identity owner plus the producer's owner | `stages_conservation_identity.py:520-534`; `P13M:352-353` |
| **B-07** selection and flag authorities | Owner half closed by decision 128; the engineering half needs three receipts owned by other packages. | Engineering contract owners; the strategy-type registry owner; P020 and P021 | `PKT13:108-112`; `P13M:374` |
| **View-preimage base-class / member-count ratification** (GM66-F01; B-16 deliberately not opened) | The shipped helpers' absolute digests are self-declared provisional on it. | View-schema owner | `P13M:358` |
| **Authorization for anything beyond the bounded slice** | `P13/DECISIONS.md:24` excludes the full writer, the selection/artifact pipeline, reader adoption beyond D-05, caller integration and P020 acceptance. | Owner | `P13M:361`; `H13:109-110` |

**Consequence.** The shortest true path from today to a first acceptance-bearing catalogue row
runs A → B → C → D → E, and **Phase C is the long pole and is entirely outside P013's
control.** Any plan that shortens it is not a plan; it is a reinterpretation of B-01, which
`MAP13:35` names for what it is: *"Reinterpreting it as component readiness would silently
lower the gate and would let a nonaccepted producer mint full-kernel lineage."*

**No estimate is offered.** `MAP13:164` carries a conditional Lead estimate and states in the
same paragraph that it *"has not been independently measured"* and that calendar time excludes
P020 acceptance, owner decisions, the CI queue and any repair-cap stop. This lane adds nothing
to that and does not repeat the figures as if they were current.

---

## 6. What P013 preparation can proceed now, without the writer

### 6.1 The authorization frame, stated before the list

Two boundaries apply at once, and conflating them is how a preparation list turns into an
unauthorized start.

1. **What the blockers permit.** `MAP13:83` — *"only screening lineage and non-accepting
   preparation may proceed."* Non-accepting preparation is permitted *by the blocker*.
2. **What the authorization record permits.** `P13/DECISIONS.md:24` — *"Excluded are the full
   writer, selection/artifact pipeline, reader adoption beyond D-05, caller integration, P020
   acceptance, push/PR/merge, host/credentials/trading/deploy."* And `H13:109-110` — *"WAITING
   FOR OWNER: Nothing for the completed bounded slice. **New authority is required for
   integration or any excluded/full-package work.**"*

**The consequence, stated plainly: no repository-writing P013 preparation is authorized
today.** The bounded slice is complete and accepted at `da1fb184`; its repair authority is
spent; and every remaining category is either named in the exclusion list or is new work needing
new path authority. The dependency-map lane reached the same boundary and refused to cross it:
*"No statement is made about whether any preparation listed in section 4.2 is authorized …
`DECISIONS.md:23-24` currently excludes all of it, and nothing in this document changes that."*
(`P13M:501-504`).

What **is** available today is **external, non-repository preparation** — the kind this lane
itself is: reading, analysis, and design notes held outside Git. Section 6.2 lists that.
Section 6.3 lists what is *technically* possible against already-ratified contracts and would
need new authority before a single repository byte changes; it is a feasibility reading, not a
recommendation and not a request.

### 6.2 Available now with no new authority — external, non-repository work

| # | Preparation | What it produces | Rework risk | What would invalidate it |
|---|---|---|---|---|
| **E-1** | The **B-01 adapter-seam design note**: the six M-items of section 3.4 plus the narrow verifier signature `verify(receipt_bytes, completed_run_identity) -> P020VerifiedCanonicalPathResult or REFUSED(CANONICAL_RECEIPT_MISSING_OR_INVALID)`. | The exact shape of what P013 will consume, written so it names no P020 line and no P020 byte. | **MEDIUM** | The twelve-member bundle and the verifier signature are Lead **proposals**, not ratified schemas: *"The bundle is an engineering proposal until P020 accepts and ratifies it"* (`MAP13:58`). P020 may freeze a different member set at acceptance. |
| **E-2** | The **merged-`identity.py` union specification** of section 2.2, with the G-1…G-8 evidence contract of section 2.5. | The handover artifact P020 needs at steps B-2 and B-4; it removes the analysis work from P020's critical path. | **LOW** while the two blobs are unchanged | It is derived from `1e9682ba` and `fa57a771`. The moment **either** branch commits again to `identity.py`, the union must be re-derived. Re-check the two blob ids before use. |
| **E-3** | **Documentation-only citation repairs.** `PKT13:30` pins P020 at `556639f591…`, superseded by `b9b72f85` (`H20:9`; `PKT20:211`). `PLAN:489` pins `simulate_slice` to line 648, which is `_resolve_exit_geometry` at P020's head (section 3.1). The `HIST-2026-0045` gap (`P13M:443-449`). | A short corrections note so no stale identity is quoted forward into a binding document. | **LOW** | Only a further head change. Note this fixes *citations*, not the documents — amending `PKT13` or `PLAN` is a separate, owned act. |
| **E-4** | Recording the **`SimulatorClass` duplication question**: `identity.py:263-265` defines a closed enum while `stages_conservation_identity.py:55-56` declares module-level string twins and does not import it; no observed test asserts equality between them (`P13M:471-477`). | One question for the contract owner, with the two locations named. | **LOW** | Nothing; it is a question, not an answer. |
| **E-5** | The **B-15 joint-ratification request package**: the exact question, quoted from `DSGN:1706-1716`, addressed to the P013 build owner and the WP-P0-08 migration owner, with the seam facts of section 3.3 attached. | The shortest path to closing the one open blocker that is *"**not** P0-20-gated"*. | **LOW-MEDIUM** | It asks for a member; it does not propose one. P013 *"will not add the member on its own authority"* (`DSGN:1706-1716`). |
| **E-6** | A **test plan** — not tests — for the Phase-D proofs D-5 and D-6, built on the mechanisms that already exist: the sealed classifier (`stages_conservation_identity.py:414-436`) and the structural import isolation (`trial_catalog/__init__.py:14-18`). | A plan a future authorized writer executes without re-deriving it. | **MEDIUM** | The closed reason `CANONICAL_RECEIPT_MISSING_OR_INVALID` and the capability shape are stable, but the verifier's failure modes come from D-2, which does not exist. |

None of E-1…E-6 writes a repository byte, starts a writer, or claims any closure. All of them
live where this lane lives — outside Git, as mutable evidence files, which `H13:81-83` already
describes as the correct home for such material and warns must not be *"silently promote[d] …
into the repo"*.

### 6.3 Technically possible against ratified contracts — **requires new authority first**

Carried from `P13M:373-380`'s preparation column and re-stated with its authorization status
made explicit. **Listing is not requesting.** Each row would change repository bytes and is
therefore gated by `P13/DECISIONS.md:24` and `H13:109-110`.

| # | Preparation | Why it is technically possible now | Rework risk | Authorization status |
|---|---|---|---|---|
| **W-1** | Further RED/GREEN cases for the **three emittable reader reasons**. | Their contract is ratified and version-pinned at `acceptance_reader.py:44`; no new contract is needed (`P13M:378`). | **LOW-MEDIUM** | `NOT AUTHORIZED TODAY` — new tests in the reader's suite are new work outside the accepted slice. |
| **W-2** | **In-memory conservation fixtures** using `ordinal`, `ordered_trial_ids` and `row_count` only, touching no path. | The hand-off shape `StagedPartRowProjection` already exists and the comparer already consumes it (`P13M:376`). | **LOW** — these fields carry no path and no blocked identity | `NOT AUTHORIZED TODAY` |
| **W-3** | **`TrialRecord` and `ArtifactManifest` V2 fixtures** against the ratified shapes. | Both shapes are ratified and version-enforced; construction fixtures already exist (`P13M:375`). | **MEDIUM** — the manifest contract is stable, but any address derivation depends on `trial_id`, which depends on `param_hash` | `NOT AUTHORIZED TODAY` |
| **W-4** | The **V1-to-V2 commit-preimage read path** in the acceptance reader. | Both preimage types are ratified in the same file; the reader still parses V1 (`P13M:205`, `:378`). | **LOW-MEDIUM** for the shape | `NOT AUTHORIZED TODAY` — and specifically named: *"reader adoption beyond D-05"* is excluded (`P13/DECISIONS.md:24`). |
| **W-5** | A **`TrialRecordAssembler` interface sketch** naming only ratified types. | Every type it would mention exists. | **HIGH** | `NOT AUTHORIZED TODAY`. And the rework risk is structural, not incidental: two of the 48 required fields still have **no emittable value**. The design states the consequence — *"`IdentityValidator` therefore cannot validate a complete identity set, and stage 7's `TrialRecordAssembler` cannot construct a row, until B-04 and B-12 close"* (`DSGN:421`). |

**One correction to carry forward on W-5.** `DSGN:421` is v1.6 controlling text and predates the
2026-09-12/13 ratifications; its clause *"`param_hash` has a named producer but no ratified
preimage (B-04)"* is no longer current — B-04's preimage **is** ratified
(`identity.py:218-232`). What is unchanged is the operative consequence: the two identities
still have no emittable value, because **producer adoption**, not the preimage, is what is
missing. The code says so in its own words:
*"param_hash has a ratified B-04 preimage, but producer inputs and adoption are unavailable in
this legacy stage; no value may be computed, defaulted, or accepted"*
(`stages_conservation_identity.py:520-526`, and the parallel text for
`preregistered_space_hash` at `:528-534`). So no row may be assembled today, for a reason that
has moved but not weakened.

### 6.4 Rework-risk summary

| Risk | Items | Why |
|---|---|---|
| **LOW** | E-2 (while both blobs hold), E-3, E-4, W-2 | Derived from committed bytes or from ratified, version-pinned contracts; no blocked identity and no path is involved. |
| **LOW-MEDIUM** | E-5, W-1, W-4 | Shapes are ratified; what is uncertain is adoption timing and authority, not the bytes. |
| **MEDIUM** | E-1, E-6, W-3 | Depends on P020-owned shapes that are proposals until acceptance (`MAP13:58`), or on `trial_id`, which depends on `param_hash`. |
| **HIGH** | W-5, and anything caller-shaped | Two required identities have no emittable value; and anything written against `mega_walk_forward.py` is written against a file P020 is actively changing (`P13M:379`). |

### 6.5 Preparation that must not be done now

| Trap | Why it is a trap | Source |
|---|---|---|
| Populating `P020AcceptedCatalogueDependencyV1` from the current research candidate. | *"P013 must not populate it from the current research candidate."* The bundle's purpose is *"to bind existing accepted P020 bytes and identities, not to introduce economic values."* | `MAP13:58` |
| Writing anything against today's `mega_walk_forward.py` bytes. | P020 holds the file and is changing it; P013's blob is identical at base and head, and must stay that way. | D-P20-3; `P13M:379`, `:408` |
| Adding the B-15 cell-coordinate member to `CompletedRunInput` on P013's own authority. | *"This design lane will not add the member on its own authority: assembling an input list is the act that produced this finding."* | `DSGN:1706-1716` |
| Deriving any part path, staged part, commit receipt or published-view fixture while B-15 is open. | *"while B-15 is open **no part path may be derived at all**, so every fixture arm whose input is a staged or committed part, a commit receipt, or the published view is a blocked design target"*; and in the contract itself, *"While B-15 is open no component may derive a value for it."* | `DSGN:310`; `trial_catalog.py:280-284` |
| Treating the P0-20 scope label — or the string `RESEARCH_ONLY_NOT_ACCEPTED`, or any other status word — as B-01 satisfaction. | Section 1.2; *"No `ACCEPTED` status label is trusted."* | `PKT13:31`; `PKT20:130` |
| Reusing the `da1fb184` review verdicts on any changed head. | *"Any source/head change invalidates the acceptance evidence and requires the repository's then-current T0 roster; do not substitute a cheaper model for a required exact role."* | `H13:92-94` |
| Promoting any external packet, note or fixture under `C:/tmp/…` into the repository as if it were accepted evidence. | *"External packets, runner scripts, reports, verification record, and this handoff … are deliberately outside Git and remain mutable evidence files. Do not silently promote them into the repo."* | `H13:81-83` |

### 6.6 The instruction the takeover note actually gives

`SH:42` is the sentence that governs this whole section, and it points in both directions at
once:

> "Remaining full work: accepted P020 B-01 interface dependency, reader adoption/coverage,
> selection and artifact pipeline, immutable Parquet writer/DuckDB publication, caller
> integration and final acceptance. The narrower P020 milestone is not automatically B-01.
> Inspect the ratified contracts and dependency/adoption map before claiming writer scope is
> ready; **advance authorized independent preparation while prerequisites are open.** No new
> P013 push/PR/merge authority is inferred."

Preparation is wanted, not merely tolerated — but the adjective is load-bearing. *Authorized*
independent preparation is section 6.2: external, non-repository, claiming nothing. Everything
in section 6.3 is preparation that is *independent* but not yet *authorized*, and the gap
between those two words is exactly one owner act.

---

## 7. NOT VERIFIED

This section is deliberately non-empty. Each item is something this lane did **not** establish,
or established as an unresolved discrepancy.

1. **Nothing was executed.** No test suite, no acceptance reporter, no benchmark, no Python.
   `219 passed` (`VER13:46`; `H13:57`), `304 full P020-plus-identity tests` and `231 CI-selected
   tests` (`H20:29`), and `8/16 criteria MET / NOT ACCEPTABLE` (`H20:30`) are all **quoted, not
   reproduced**.
2. **No Git write of any kind, and no working-tree status or diff command.** Only `git show`,
   `git rev-parse` and `git cat-file -s` were run, all against committed objects, plus
   read-only file reads and greps. No branch, commit, stash, merge, `merge-file`, `merge-tree`
   or `git status` was used.
3. **The merged `identity.py` of section 2.2 was not built.** The claim that a three-way merge
   contests only the import prologue is derived from reading the three blobs side by side, not
   from running a merge. A real merge could differ in hunk boundaries; it cannot differ in the
   *facts* the claim rests on (no shared name, disjoint insertion anchors), but the hunk
   prediction itself is unverified.
4. **The regression at `test_p020_identity.py:246` was reasoned, not executed.** It follows from
   the merged `_json_value` raising where the test expects a returned string. It was not
   observed by running pytest, which this lane cannot do.
5. **The "only one affected test" claim is grep-bounded.** A case-insensitive sweep of the whole
   `C:/P020_IMPL_20260912` worktree for `canonical_json` on a line also matching `nan` or
   `infinity` returned three hits: `test_p020_identity.py:246` (the real one),
   `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_11_GATE_2026-08-28/stage1_freeze.py:359` (a descriptive
   string containing `allow_nan=false`) and `contracts/mtc_contracts/identity.py:53` (a false
   match on `source_provenance`). A test that constructs a non-finite value and serializes it
   across two statements would not be caught by that pattern.
6. **P013's diff identities were not recomputed.** `a38248a967d5f9838bf19c13ef4fba8b79f71965`
   and `46089d3fca63ee263e7389ebe87f360f0303af720bd86742ab315dd1a50ed5b2` (`H13:12-13`) are
   quoted. So are the three review-report SHA-256 values at `H13:71-75` and the packet draft
   SHA-256 `21a3b2f5dab8e57b1b2dff2f22956b73d9139d6dde5b14c024169c2cec3ddcef` (`PKT20:360`).
7. **A citation-pin correction in the source map, recorded not silently fixed.** `P13M:373`
   attributes the wording *"still leave two required non-null `TrialRecord` identities with no
   emittable value, so no row may be assembled"* to `DSGN:310`. This lane located that wording
   at `DSGN:140`, `:170`, `:191`, `:421` and `:1233`; `DSGN:310` instead carries the
   *"no part path may be derived at all"* sentence, which `P13M:376` pins correctly. The
   substance of `P13M:373` is unaffected; only its line pin is.
8. **A second stale line pin, in the plan.** `PLAN:489` names the canonical path as
   `mega_walk_forward.py:648 simulate_slice`. That resolves in the base blob `2f16fffd` and does
   **not** resolve at P020's head `21574df7`, where line 648 is `_resolve_exit_geometry` and
   `simulate_slice` is at 675. This lane records the drift; amending `PLAN` is an owned act
   nobody here holds.
9. **`DSGN:421` is superseded in part and was not reconciled.** Its clause *"`param_hash` has a
   named producer but no ratified preimage (B-04)"* is v1.6 controlling text that predates
   `OD-20260912-P013-CONTRACTS`. Which version of the design the P013 Lead treats as controlling
   after the 2026-09-12/13 ratifications was not established — the same open question
   `P13M:459-465` records about the blocker counts.
10. **`DSGN`'s status as the controlling v2.3 design was not independently confirmed** against an
    owner record. Carried unresolved from `P13M:450-455`.
11. **The `HIST-2026-0045` gap is unresolved.** `H13:22` and `VER13:11` name only
    `HIST-2026-0044`, while the committed `TASK_HISTORY.json` also carries `HIST-2026-0045` /
    `WP-P0-13-CONTRACT-DEFAULTS-20260913`. Whether the 2026-09-13 defaults are covered by
    `HIST-2026-0044` or by `HIST-2026-0045` is established by no source this lane read. Carried
    from `P13M:443-449`.
12. **The four `DECISIONS.md` blob ids were taken from `P13M:409`, not re-derived from branch
    heads.** All four resolve in the shared object store and their line counts were read
    directly, but this lane did **not** confirm that `a3b93900` and `8e8772d1` are the *current*
    head blobs of P031 and the CT13 takeover branch. The P031 worktree was not inspected at all,
    and P031's single 26.7 KB row was read only to its first 70 characters — its content is
    unexamined.
13. **`C:/CT13` is not integrated master.** Carried from `P13M:488-492`. Every `PLAN`, `POL` and
    `PKT20` citation in this document is to that branch checkout.
14. **The D-P20-3 assignment is chat-resident.** No repository record of it was found. Every step
    in sections 2.4 and 5 that rests on "P020 is the sole writer" therefore rests on an
    unrecorded decision; step A-4 exists precisely because of this.
15. **Who may perform the `DECISIONS.md` reconciliation, and on which branch the reconciled file
    should first exist, is not established.** `PKT20:194` says the one-writer question is *"Not
    Lead-decidable — cross-package ownership"*; no source this lane read names the party who
    resolves a three-way `DECISIONS.md` divergence.
16. **The twelve-member bundle and the verifier signature are proposals.** `MAP13:43-64` is Lead
    engineering design, explicitly *"an engineering proposal until P020 accepts and ratifies
    it"* (`MAP13:58`). Section 1.1 cites it as the named requirement because `PKT13:31` and
    `PKT20:117-121` both route B-01 through it — not because any of it is ratified.
17. **No effort or calendar estimate is offered or endorsed.** `MAP13:164` carries one and says
    in the same paragraph that it *"has not been independently measured"*.
18. **`DISP:3`'s *"PROPOSED, not PERFORMED."* was not read at source.** It is quoted here at
    second hand from `PKT20:62`. Likewise `CHK:704` (`PKT20:183`) and the `check_p020_acceptance.py`
    clause line numbers were not read directly; `C:/P020_IMPL_20260912/check_p020_acceptance.py`
    was not opened by this lane.
19. **No P020 file was written, requested, or prepared for writing.** Sections 2, 3 and 5 describe
    acts P020 would perform. They are not requests, and this lane holds no channel to make them.
20. **The blocked writer was not launched**, and no step in this document was executed. The
    owner's constraint — *"Do not launch the blocked writer under an assumed exception"* — was
    treated as absolute, including for the steps this document itself marks as merely
    "technically possible".

---

## 8. Citation index

Grouped by file so each pin is auditable. Token expansions are in the table at the top of this
document. Paths are given as read.

```
C:/tmp/CLAUDE_P0_RUN_20260913/laneP13E_plan/BRIEF.md

C:/tmp/CLAUDE_P0_RUN_20260913/laneP13M_dependency_map/P013_DEPENDENCY_ADOPTION_MAP_DRAFT.md   (P13M)
  :85  :98  :102  :205  :216  :338-345  :351-361  :352-353  :354  :358  :361
  :373-380  :374  :375  :376  :378  :379  :407  :408  :409  :412
  :443-449  :450-455  :459-465  :471-477  :488-492  :501-504

C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md   (PKT13)
  :18  :22  :30  :31  :32  :33  :34  :35  :75  :108-112  :130  :134
  :194  :208  :223  :225

C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md   (MAP13)
  :7  :35  :43-64  :54-55  :58  :60-64  :70-71  :76-81  :77  :78  :79  :80  :81
  :83  :164

C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md   (VER13)
  :4  :11  :15  :32-33  :46  :82

C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P020_SCOPE_DECISION_PACKET_20260913.md   (PKT20)
  :56  :57-60  :59  :60  :61  :62  :64  :79-82  :84  :88-89  :93  :117-121
  :130  :137  :142  :151-153  :183  :191  :193  :194  :196  :211  :214
  :223-225  :235-237  :239  :357  :359  :360

C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md   (H13)
  :11  :12-13  :22  :26  :57  :57-64  :71-75  :81-83  :92-94  :98-101
  :100-101  :103-107  :104  :109-110

C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md   (H20)
  :9  :15  :19  :21  :29  :30  :31  :40-49  :51  :64  :68  :118

C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md   (SH)
  :42

C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md   (DSGN)
  :140  :170  :191  :310  :382  :421  :486  :634-640  :1233
  :1439  :1441  :1445  :1706-1716

C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md   (PLAN)
  :412  :414  :415  :489  :507  :508  :509  :510

C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/REVIEW_POLICY.md   (POL)
  :18  :25-26

C:/tmp/P013_CONTRACT_V2_20260912/DECISIONS.md
  :16-19  :17-18  :23  :24

C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/CHANGELOG.md
  2026-09-13 section, first bullet

C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py
  :43-46  :218-232  :263-265

C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/trial_catalog.py
  :280-284

C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_identity.py
  :194-199

C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/contracts/tests/test_trial_catalog_types.py
  :59-65

C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/__init__.py
  :7-8  :14-18

C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/acceptance_reader.py
  :44

C:/tmp/P013_CONTRACT_V2_20260912/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/trial_catalog/stages_conservation_identity.py
  :55-56  :414-436  :424-428  :429-433  :520-526  :520-534  :528-534

C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/base.py
  :15  :16  :92

C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/sizing.py
  :12

C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/mtc_contracts/package.py
  :11-12  :48

C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/contracts/tests/test_p020_identity.py
  :134  :151  :180  :190  :219-227  :229  :245  :245-248  :246  :249-250
  :287  :440  :464  :681-715

C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_11_GATE_2026-08-28/stage1_freeze.py
  :359   (negative result only, section 7 item 5)
```

### Git objects read (all with `git show` / `git rev-parse` / `git cat-file -s`, from `C:/tmp/P013_CONTRACT_V2_20260912`)

```
75289fa6a83bab87ed6420732624656778da0163   identity.py           base   (4,854 B / 154 lines)
1e9682ba057d407e4d786a66a935a77244089f72   identity.py           P013   (22,853 B / 626 lines)
fa57a77176b267e08436e03a0c3bfd371e054ba7   identity.py           P020   (13,647 B / 368 lines)
2f16fffd08a1ca4891060205a456282665f252f3   mega_walk_forward.py  base and P013 head   (83,403 B / 1,856 lines)
21574df7861c79cc430cb41fff5ad0070097e01f   mega_walk_forward.py  P020   (89,721 B / 1,997 lines)
4d5c3dfcaef7c0a3a547e5a6eca9a73d2033b0c8   DECISIONS.md          base   (26,429 B / 75 lines)
3c7d0d0ba47c3742945089d0516af4ea47bcea36   DECISIONS.md          P013   (28,918 B / 82 lines)
a3b9390071277e55127911219109d02e31c449da   DECISIONS.md          P031   (53,199 B / 76 lines)
8e8772d14a5d5d7febe5b93a437d7e650dd37af3   DECISIONS.md          CT13   (26,947 B / 79 lines)
e991f7469a68f1575867a4dc5b9b18a638db03f6   base.py     identical at a4e79fbe / 42f99571 / da1fb184 / b9b72f85
3957ac2fcda7f1bde93a3d2b9dd3fe9839257a3c   sizing.py   identical at a4e79fbe / 42f99571 / da1fb184 / b9b72f85
e24a5aa6442b01369bed9cd3d7f2e114fa3b4309   package.py  at a4e79fbe / 42f99571 / da1fb184
a7e03268feb785237599cac345755683beed2534   package.py  at b9b72f85
```

Commits referenced: `a4e79fbeb2365c7a4e876ca4f7447d9032851d23` (P013 accepted base),
`da1fb184c71e1ae65e2e348758af7f1a84a1cfbd` (P013 head),
`42f99571e6abb5222744d9345e1c8a9e19c23c15` (P013/master merge-base, from `P13M:32-35`),
`b9b72f858dc830a9389517f79da5ea3c1fa6122c` (P020 clean head),
`fcac0ac67cf2682693ad28138b1a56e15a0846f2` (remote master, quoted only),
`556639f59122e33b664ab918a4241eb96680219b` (superseded P020 pin in `PKT13:30`, quoted only as
stale).

---

**End of draft.** This document authorizes nothing, accepts nothing, and closes no blocker.
B-01 remains `NOT SATISFIED`; WP-P0-13 remains at `WAIT_P020_ACCEPTANCE`; the blocked writer
was not launched.
