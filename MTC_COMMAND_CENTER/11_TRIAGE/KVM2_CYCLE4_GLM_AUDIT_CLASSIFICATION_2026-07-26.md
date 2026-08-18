# KVM2 Cycle 4 — GLM-5.2 Advisory Audit Classification

- Date: 2026-07-26
- GLM report: runtime-local `GLM_AUDIT.md`
- GLM report SHA-256:
  `0F9CB7870AF7D257D66977163F355BB416EA7A9110435CA08963BAF0F6D4F17A`
- Authority: advisory only; GLM does not replace mandatory Gate 5/Gate 6
  auditors. Codex remains final acceptance authority.
- Scope: current KVM2 master, execution companion, audit prompt, lower-level
  bridge authority, and D020–D023.

## Overall GLM conclusion

**REJECTED.** GLM stated that all eight final Codex Cycle-3/R3 findings were
resolved, but its reproduction table used a different, older finding set
(`resource-admission cycle`, `post-rollback→ARMED`, `restart-profile bypass`,
and similar items). It did not reproduce the final R3 findings concerning live
risk-state transfer, monitoring/backup authority, exact workload-manifest
admission, post-build audit, or standing document-write authority. That
statement is not evidence of closure.

## Finding-by-finding classification

### GLM NEW-1 — post-implementation Gate 6 can precede the real `ai-lab` identity

**ACCEPTED.** The execution companion creates the actual Unix identity and
workspace in P6-02, after P6-01 says fresh Gate 6 accepted its test evidence.
P6-02 has denial tests but no required fresh accepting Gate 6 verdict over the
actual UID/GID/groups/environment/cgroup and child-process evidence. This
reproduces final Codex finding KVM2-R3-04.

Required repair: implementation authorization must not be described as final
security acceptance. The full P5-10 suite must run from the final identity and
controls, with fresh canonical Gate 6 acceptance before workload admission.

### GLM NEW-2 — primary-agent selection follows a Hermes-specific admission task

**ACCEPTED.** P7-01 hardcodes Hermes admission before P7-01A selects Hermes or
OpenClaw. Selecting OpenClaw makes the two tasks contradictory. This reproduces
final Codex finding KVM2-R3-07.

Required repair: selection closes first; the admission task becomes
provider-neutral and cites the selection decision and exact manifest.

### GLM NEW-3 — partial lab admission has no Phase-10 route

**ACCEPTED WITH CORRECTED RATIONALE.** The reachability defect is real and
reproduces final Codex finding KVM2-R3-06: after one admitted workload, later
optional Phase 7/8/9 work cannot be declined while still reaching Phase 10.
GLM's claim that the current text could thereby bypass Option A/B is incorrect;
the current Phase-10 text retains Option A/B for both documented branches.

Required repair: add explicit per-phase/per-workload `NOT_SELECTED` records and
a partial-lab route to Phase 10. Any actual lab admission remains contamination
and still requires Option A or B before mainnet.

### GLM NEW-4 — consolidated audit report is stale

**ACCEPTED.** The historical consolidated report freezes old hashes and 71
tasks, while the current frozen pair has different hashes and 84 tasks. It does
not carry a clear superseded banner and can be mistaken for current evidence.

Required repair: preserve the historical body, but add a prominent
`SUPERSEDED` banner pointing to the Cycle-3/R3 result and current Cycle-4
artifacts. Do not rewrite historical hashes or verdicts as if they were current.

### GLM NEW-5 — `[AI: Any]` tags conflict with named accountability

**REJECTED.** P2-09 and P3-04 use `Any` only as the dispatch category. Their
Evidence/Stop contracts explicitly require a named executor and/or named
independent reviewer before work. The master forbids `Any` as the *final
accountable* executor/verifier, which these tasks already enforce. Retagging is
not required.

## Cycle-4 accepted repair set

1. Final live risk-state transfer after old-writer quiesce and before first VPS
   start, including final WAL hash, SQLite integrity, semantic risk invariants,
   and exact-state load proof.
2. Separate owner authority for external monitoring/backup provider accounts,
   billing, credentials, provisioning/tests, and any network/purchase action.
3. P6-05 exact workload-manifest SHA-256, full supply-chain/permission hashes,
   named executor, and exactly one install/start attempt with no retry.
4. Final actual-identity isolation suite and fresh canonical Gate 6 acceptance
   after final identity/resource controls exist.
5. Fresh independent post-build Gate 5/Gate 6 audit of the resulting Option A/B
   host before the separate mainnet gate.
6. Explicit optional/partial-lab skip records and an acyclic path to Phase 10;
   any admitted lab workload still forces Option A or B.
7. Primary-agent selection before manifest acceptance, credential provisioning,
   installation, or start.
8. Replace transient standing plan-write authority with task-specific explicit
   owner authorization; audit acceptance grants no write authority.
9. Mark the old consolidated audit report clearly superseded without rewriting
   its historical evidence.

This classification authorizes no VPS, Git publication, deployment, secret,
network, broker/exchange, ARM, reprovision, purchase, or mainnet action.
