# WP-P0-13 Claude takeover handoff

Checkpoint: 2026-09-13  
State: PARKED; bounded contract slice complete and Lead-accepted; full P013 nonaccepted.

## Frozen repository state

- Worktree: `C:/tmp/P013_CONTRACT_V2_20260912`
- Branch: `feature/p013-contract-v2-20260912`
- Base: `a4e79fbeb2365c7a4e876ca4f7447d9032851d23`
- Head: `da1fb184c71e1ae65e2e348758af7f1a84a1cfbd`
- Git diff object: `a38248a967d5f9838bf19c13ef4fba8b79f71965`
- Raw diff SHA-256: `46089d3fca63ee263e7389ebe87f360f0303af720bd86742ab315dd1a50ed5b2`
- Package: 15 changed paths, 14 forward local commits, every commit carrying
  `APPROVED-PATCH-PLAN: WP-P0-13-CONTRACT-V2-20260912`
- Current worktree: clean; no tracked or untracked candidate files.

## Exact approved scope and owner decisions

Binding records: `OD-20260912-P013-CONTRACTS`,
`OD-20260913-P013-CONTRACT-DEFAULTS`, and protected-path approval
`HIST-2026-0044` / `WP-P0-13-CONTRACT-V2-20260912`.

Implemented approvals:

1. F3: reject Decimal NaN/infinity in shared `identity.py`; preserve finite bytes/hashes.
2. D-05: reader taxonomy V2 plus `COMMIT_RECEIPT_STRUCTURE_INVALID`, preserving
   missing-member and real hash-mismatch reasons.
3. B-03: 48-field row, 53-column base view, canonical parameter JSON, typed companions.
4. B-04: two-member `ParamHashPreimageV1`, version literal `"1"`.
5. B-12: authoritative registered-space recipe with strategy/search regime and complete
   typed definitions; shared by P013/P022.
6. B-17: digest-bound coordinate receipt; commit preimage V2; V1 unchanged.
7. B-09/D-04: `ArtifactManifest` V2 adds `trial_id` and `param_hash`; per-trial identity.
8. B-05/B-08: screening/full-kernel vocabulary and separate seven-member
   `LegacyScreenDeploymentPreimageV1`; screening never establishes full-kernel acceptance.
9. Owner defaults: uppercase-E Decimal JSON-number grammar is parameter-only V1 identity;
   shared finite `canonical_json` bytes stay unchanged. `adaptive_trial_budget` is
   positive `StrictInt`.

Decisions 128/88 are preserved without reinterpretation.

## Completed versus nonaccepted scope

Lead accepted only the bounded shared-contract and named P013 repairs at this exact head.
It includes snapshot-safe caller-input handling, truthful unavailable-producer refusals,
receipt-specific required `Literal["1"]`, focused RED/GREEN tests, documentation and
decision records.

Still excluded and nonaccepted: full catalog writer, selection/artifact/address pipeline,
receipt production/publication, reader adoption, caller integration, full P013, and P020.
No push, PR, merge, master integration, host contact, credentials, trading or deployment
is authorized. P020 acceptance and remaining prerequisites stay binding.

## Tests and reviews

- Lead Python 3.12.12 combined suite: `219 passed`.
- Exact `gpt-5.6-sol` / `xhigh`: `PASS-WITH-NITS`, no required findings; reproduced
  `219 passed` and RED/GREEN evidence.
- Exact execution-capable `claude-opus-5` / `xhigh`: `PASS-WITH-NITS`, no required
  findings; Python 3.12.12 / pytest 9.1.1 / Pydantic 2.13.4, `219 passed in 0.52s`,
  post-run clean.
- Coordinated `gemini-3.7-flash-high`: supplemental `PASS-WITH-NITS`, no required
  findings, provider `SUCCESS`, `GEMINI_READ_ONLY_OK`, one call, zero helpers after.
- Ruff 0.16.4 introduced no new diagnostics; the same 10 diagnostics exist at base/head.
- `git diff --check` and every commit's `git show --check` passed.

Evidence:

- `C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md`
  - SHA-256 `96ca7a26e45f713ad385b27f10d98c135ee71877c57cb73772cafcf4461372d9`
- `C:/tmp/P013_LEAD_20260912/P013_OPUS_T0_REPORT_DA1FB184_R4_EXEC_CONFIRM.json`
  - SHA-256 `c5f12aaa196313f4f9e6c6e7cb21885d8ca3ec6c34d4a3e70bf8a52e644f659d`
- `C:/tmp/P013_LEAD_20260912/P013_GEMINI_T0_REPORT_DA1FB184_FINAL.txt`
  - SHA-256 `986dbfa8648d80520aed04c86c43c0cd79bc2366f456c1efc04e43eef307e8c8`
- Decision packet: `C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md`

## Mutable/uncommitted state

- Candidate worktree has no uncommitted state.
- External packets, runner scripts, reports, verification record, and this handoff under
  `C:/tmp/P013_LEAD_20260912` and `C:/tmp/CLAUDE_TAKEOVER_20260913` are deliberately
  outside Git and remain mutable evidence files. Do not silently promote them into the repo.
- No P013 writer/helper/provider job is active at checkpoint: `agy=0`, `gemini=0`,
  P013-scoped `claude=0`, P013-scoped Python/PowerShell=0. Other persistent Claude desktop
  processes are foreign and must not be stopped.

## Subscriptions and exact roles

Completed reviews used included subscription routes only; no PAYG fallback, overage route,
reset credit, or paid provider substitution was invoked. The current exact Sol/Opus and
Gemini results apply only to frozen head `da1fb184`. Any source/head change invalidates the
acceptance evidence and requires the repository's then-current T0 roster; do not substitute
a cheaper model for a required exact role.

## Resume rule

NEXT ACTION: Claude should first re-read the verification record, then independently verify
branch/head/clean status and both diff hashes. Preserve the accepted bounded candidate and
wait for separately authorized integration or full-package scope; coordinate one writer for
shared files with P020/P022 if later authority is granted.

STOP CONDITION: Stop on any head/diff drift, dirty or foreign ownership, shared-path writer
collision, missing P020 acceptance, new scope/economic/production fact, paid-route need,
credential/host action, push/PR/merge request without explicit authority, or attempted waiver
of an exact-model review. Do not resume implementation automatically after the current quiet
window releases.

WAITING FOR OWNER: Nothing for the completed bounded slice. New authority is required for
integration or any excluded/full-package work.
