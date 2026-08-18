# KVM2 program artifact index

- Prepared: 2026-07-26
- Scope: local TESTNET-only bridge readiness artifacts and the controlling
  existing-KVM2 deployment sequence
- Authority: preparation only; no install, secret, runtime, cutover, start,
  active-KVM2 access, TESTNET mutation, ARM, VPS access, purchase, or deployment
  authority
- Base merged commit: `f61ed91919110e8856b2bc309c2c807365bb5fea`
- Exact-base payload probe: **PASS**; the local-only payload was built from a
  clean detached worktree and its `RELEASE_SHA256SUMS` hash is
  `d2a4275268d27a911ea74d97d57ab2132e0da137a037bce663b3a98d37d12a21`
- Release candidate: **OPEN** until the current 12-path readiness package, including
  the three-path readiness repair and two-file owner-sequence amendment, is
  accepted, committed, re-packaged, staged on Ubuntu 24.04, and accepted

## Controlling deployment sequence

1. Use the existing KVM2; do not purchase another VPS/KVM.
2. Deploy only the MTC Bridge and start it DISARMED.
3. Complete and owner-accept at least 10 monitoring days with no selected
   strategy, order submission, ARM, or AI-lab workload.
4. Only then, select exactly one strategy and obtain separate authorization
   for simulated-money/TESTNET ARM and trading.
5. Admit other KVM2 lab workloads only through their later isolation,
   capacity, audit, and owner gates.
6. Do not purchase KVM1 or another VPS before a separately authorized
   real-money transition.

## Status at handoff

| Gate | Status | Reason |
|---|---|---|
| P0 artifact structure and sanitized ledger | LEAD LOCAL CHECKS PASS | Ledger, 85-task, Evidence/Stop, UTF-8, size, scope, stale-model, hash-binding, and diff checks pass; independent verification remains open |
| P1 host baseline | OPEN / BLOCKED | No active-KVM2 access was authorized; dated remote-host facts were not refreshed |
| P2-09 reproducibility rehearsal | BLOCKED / UNVERIFIED | Hyper-V is enabled but requires one Windows restart; the local Ubuntu cloud-image VM is prepared but not yet created |
| P3-01 owner risk-state choice | OPEN | WAL-consistent migration is implemented as the recommended path, not approved |
| P3-02 immutable release | OPEN | Exact-base payload probe passed, but the current 12-path readiness package remains uncommitted |
| P3-03 Ubuntu staging matrix | BLOCKED / UNVERIFIED | Local specification and restart-resume automation exist; the Hyper-V Ubuntu VM awaits the required restart |
| P3-04 independent verification | OPEN | This implementation session is not an independent reviewer |
| P3-05 final acceptance | OPEN | Codex Lead remains final acceptance authority |
| Install/deploy/start/ARM | BLOCKED / NOT AUTHORIZED | Separate owner gates remain required |

PR #29 is merged at the base above. The exact merged base was packaged locally
from a clean detached worktree into an outside-repository payload; all 6,963
files passed the generated checksum manifest. The payload is a reproducibility
probe only, not an install candidate, because post-merge checks exposed two
narrow defects: checkout-dependent hash behavior plus its stale master hash
binding, and a hard-coded schema-version assertion. Their repair changes
`.gitattributes`, the audit prompt hash, and the WAL bundle test. The owner then
authorized a two-file canonical-plan sequencing amendment; no production bridge
logic changed.

Hyper-V was enabled locally and a restart-resume VM build was registered for
the disposable Ubuntu 24.04 staging environment. No VM, active-KVM2/VPS
access, purchase, service, secret, exchange, TESTNET, cutover, bridge start,
ARM, commit, push, or deployment action was performed.

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
