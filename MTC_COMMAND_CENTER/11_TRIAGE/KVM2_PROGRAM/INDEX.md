# KVM2 program artifact index

- Prepared: 2026-07-26
- Scope: local TESTNET-only bridge/VPS readiness artifacts
- Authority: preparation only; no install, secret, runtime, cutover, start,
  TESTNET mutation, ARM, VPS access, or deployment authority
- Base merged commit: `423897b76b32f68cdabcae16b39c078fdd1f67cb`
- Release candidate: **OPEN** until the completed diff is committed, hashed,
  staged on Ubuntu 24.04, and independently accepted

## Status at handoff

| Gate | Status | Reason |
|---|---|---|
| P0 artifact structure and sanitized ledger | PREPARED LOCALLY | Independent verification remains open |
| P1 host baseline | OPEN / BLOCKED | No VPS access was authorized; dated facts were not refreshed |
| P2-09 reproducibility rehearsal | BLOCKED / UNVERIFIED | No named expendable Ubuntu environment was provided or used |
| P3-01 owner risk-state choice | OPEN | WAL-consistent migration is implemented as the recommended path, not approved |
| P3-02 immutable release | OPEN | Worktree changes are intentionally uncommitted |
| P3-03 Ubuntu staging matrix | BLOCKED / UNVERIFIED | Local specification exists; Ubuntu execution did not occur |
| P3-04 independent verification | OPEN | This implementation session is not an independent reviewer |
| P3-05 final acceptance | OPEN | Codex Lead remains final acceptance authority |
| Install/deploy/start/ARM | BLOCKED / NOT AUTHORIZED | Separate owner gates remain required |

PR #25 is merged at the base above. The three canonical TS-P0 contract files
are now present in `origin/master`; the old “contract files absent” Phase-3
block is resolved. It does not close any later release, staging, audit, owner,
install, deployment, cutover, start, or ARM gate.

The merged master/companion still contain their older dated “files absent”
sentence. Those governing files were outside this batch's write whitelist, so
they were not rewritten. This index and the lower Bridge VPS task record the
current local proof; a future plan-maintenance authorization should reconcile
the stale sentence without weakening any remaining Phase-3 gate.

## Artifact map

| Area | Artifact |
|---|---|
| Evidence | `evidence/EVIDENCE_LEDGER.jsonl`, `evidence/ledger_schema.json`, `evidence/validate_ledger.py`, `evidence/fixtures/` |
| Profiles | `rebuild/profiles/temporary-testnet-lab.md`, `rebuild/profiles/future-trading-only.md`, `rebuild/profiles/PROFILE_DIFF.md` |
| Trusted inputs | `rebuild/manifests/TRUSTED_INPUTS.md` |
| Release freeze | `rebuild/manifests/release_candidate_manifest.template.json` |
| Identity/filesystem | `boundaries/IDENTITY_AND_FILESYSTEM.md` |
| Network/service | `boundaries/NETWORK_AND_SERVICE.md` |
| Future lab isolation | `boundaries/loopback_isolation_design.md` |
| Secret names | `recovery/SECRET_INVENTORY.md` |
| State continuity | `recovery/STATE_CONTINUITY.md` |
| Access recovery | `recovery/ACCESS_RECOVERY.md` |
| Teardown/reprovision | `recovery/TEARDOWN_AND_REPROVISION.md` |
| Maintenance | `recovery/MAINTENANCE.md` |
| Incident response | `recovery/INCIDENT_RESPONSE.md` |
| Staging | `rehearsals/STAGING_MATRIX.md`, `rehearsals/summaries/` |
| Audit state | `audits/READINESS_STATUS.md` |
| Source mapping | `SOURCE_SCENARIO_RECONCILIATION.md` |

## Evidence handling

Publishable evidence is allowlisted, sanitized, hash-linked, and stored only
under this program root. Raw command output, live exchange evidence, host facts,
private identifiers, and credential material remain encrypted outside the
repository and are referenced only by a logical `RAW-...` ID.

The retention owner, retention duration, deletion trigger, and encrypted
storage selection are **OPEN owner decisions**. Until all four are recorded,
Phase 1 raw evidence collection is blocked. Deletion must stop if an incident,
audit hold, restore dependency, or unresolved discrepancy exists.

Validation command (local and non-networking):

```text
python MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/validate_ledger.py --ledger MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/EVIDENCE_LEDGER.jsonl --repo-root . --verify-artifacts
```

Fixture validation is covered by
`IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py`, including publishable-only,
restricted-only, mixed, private-path, IP, host-detail, credential, traversal,
and malformed-row cases.
