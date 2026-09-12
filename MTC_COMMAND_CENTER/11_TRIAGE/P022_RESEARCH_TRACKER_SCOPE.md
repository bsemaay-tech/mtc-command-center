# WP-P0-22 local research tracker — frozen reduced-slice contract

Status: `IMPLEMENTATION_AUTHORIZED_LOCAL_SLICE`; full WP-P0-22 remains open.

## Authority and identity

- Owner authority: `C:/tmp/P022_SIMPLER_SCOPE_20260912/P022_IMPLEMENTATION_PROMPT.md`, supplied as an instruction on 2026-09-12.
- Sealed reduced scope: `SCOPE_AND_ESTIMATE.md`, SHA-256 `618dfdb79851276a3414fc8e864ef43cf2b14993f06bc61b259190996dc9eaeb` (verified before writing).
- Owned branch/worktree: `feature/p022-local-research-tracker-20260912` at `C:/tmp/P022_TRACKER_20260912`.
- Base: local `origin/master` at `42f99571e6abb5222744d9345e1c8a9e19c23c15`; no remote host was contacted.
- External runtime/evidence root: `C:/tmp/P022_LEAD_20260912`.
- Impact tier: retained package contract `T0`. Acceptance requires fresh independent exact `claude-opus-5` and `gpt-5.6-sol`, both `xhigh`, mandatory `gemini-3.7-flash-high` corroboration on the same frozen packet, and Lead reproduction.
- P0-13 status at start: no accepted/frozen consumable interface. This slice therefore uses synthetic fixtures and opaque local references only. Real P0-13 integration remains blocked, without blocking this milestone.

## Authorized product paths

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/p022_research_tracker.py`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p022_research_tracker.py`
- this file
- narrowly factual entries in root `DECISIONS.md` and `MTC_COMMAND_CENTER/03_QUANTLENS/HANDOFF.md`, only if needed at close-out

No P0-12/13/20/21/30 path, shared identity or schema, Pine/parity/MTC/trading code, admission gate, host, deployment, backtest, optimization, paid route, push, PR, or merge is authorized.

## Version 1 local record contract

The single standard-library Python module exposes three CLI commands:

1. `register --db DB --spec SPEC.json`
2. `disclose --db DB --experiment-id LOCAL_ID --revision N --report-id REPORT_ID`
3. `status --db DB --format json|markdown`

`register` accepts a version-1 JSON object with:

- `record_version: 1`;
- `local_experiment_id`, a non-empty local identifier;
- a declared half-open UTC period `period_start_utc < period_end_utc`, both normalized `...Z` timestamps;
- non-empty `references`, each with a unique `reference_id`, one of the roles `strategy`, `configuration`, `dataset`, or `report`, an absolute local `path`, and a lowercase 64-hex `sha256`;
- at least one reference for each required role above;
- optional opaque `family_reference`, `parent_experiment_ids`, and `related_experiment_ids`; missing values remain unknown and are never inferred.

Registration reads and hashes every referenced file before opening a write transaction. A mismatch or missing file writes nothing. The stored manifest is canonical JSON; its hash is named `local_manifest_sha256` and is not a canonical P0-13/P0-22 identity. For one `local_experiment_id`, an identical canonical manifest is idempotent; any changed manifest creates the next immutable local integer revision. Earlier revisions and disclosures are never updated or deleted by the application.

`disclose` resolves exactly one registered report reference, opens and reads that path once into one byte buffer, verifies the registered digest, commits a new append-only disclosure-attempt event, and only then writes that same buffer to stdout. Validation or database/logging failure emits zero report bytes. Duplicate valid attempts create separate events. If output fails or the process crashes after commit, the committed attempt remains and the whole declared experiment period is conservatively exposed in this tracker.

`status` re-hashes current referenced paths and emits compact JSON or Markdown. Every output states both `LOCAL_LOG_ONLY` and `ACCESS_COMPLETENESS_UNVERIFIED`. It lists revisions, disclosure attempts, reference `MATCH`/`MISMATCH`/`MISSING` state, whole-period local exposure, overlapping declared periods, known parent/related/family links, lineage conflicts across revisions, and unresolved lineage/access-history warnings. It emits no untouched duration, clean-window certificate, P0-22 acceptance/admission receipt, or `LIVE_CANDIDATE` eligibility. An empty disclosure log, a new name, or a new local ID never becomes evidence of independence. Already-used or unmonitored history remains development data.

## Explicit limitations retained for the full package

- This application-local SQLite history is transactional, not tamper-proof against the local owner and not an independent clock or observer.
- Notebook, AI, file-browser, export, raw-file, copied-file, and other reader paths are unmonitored. The tracker cannot retroactively establish who accessed prior data.
- Canonical family resolution/completeness, all reader-path instrumentation, independent access/clock evidence, protected history and read prevention, complete displayed-window binding, exact untouched-window computation, P0-13 integration, and downstream acceptance/refusal gates remain future full-P0-22 work.
- Owner decisions 98–103 remain binding. In particular: no arbitrary family bins; conservative whole-period over-marking is accepted; unlogged reads/copies must ultimately be prevented rather than accepted forever; and every displayed result window must ultimately bind directly to its recorded window.

## Acceptance checks for this slice

- Registration: verified bytes, idempotent identical registration, new revision for changed settings/data, persistence after reopen.
- Disclosure: replacement/mismatch refusal with zero bytes, commit-before-output, exact single-buffer bytes, duplicate attempts, logging/commit failure with zero bytes, and post-commit emitter crash with retained exposure.
- Status: missing/conflicting lineage, related revisions, overlap, changed/missing references, durable warnings, and explicit unmonitored-access limitations.
- Refusal boundary: no success path certifies clean confirmation or enables promotion.
- Any same-scope defect repair records a discriminating RED on pre-fix behavior or equivalent mutation and GREEN after repair.

## Upgrade handoff boundary

Version-1 records remain exportable as canonical JSON plus append-only local events. A future separately authorized full package must map—not silently reinterpret—these local records into accepted canonical family identities, complete reader-path evidence, independent protected access/clock history, verified full-window binding, and the downstream refusal/admission surface. Historical uncertainty from this reduced tracker cannot be repaired retroactively.

NEXT ACTION: Build the one module and one independent test module against this frozen local-only contract, then freeze and review the candidate.
WAITING FOR OWNER: Nothing for the authorized reduced slice.
