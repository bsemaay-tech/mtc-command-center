# KVM2 Cycle 4 — GLM-5.2 bounded documentation repair

Work only in the dedicated worktree passed to `Invoke-GlmTask.ps1`. Read and
obey `AGENTS.md` and `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`.

## Authority and role

Barış explicitly instructed Codex to continue the remaining KVM2 documentation
work and to use GLM-5.2 as coder and as an additional independent auditor.
This starts owner-authorized Cycle 4 after Cycle 3/R3 ended
`REQUEST_CHANGES` at its cap.

You are the bounded GLM-5.2 **coder**. Codex is lead and final authority.
GLM is advisory and does not replace any mandatory Gate 5 or Gate 6 auditor.
Do not invoke/delegate to another model or agent.

These files are exact uncommitted snapshots seeded from the user's dirty main
worktree. Do not run `git checkout`, `git reset`, `git clean`, `git stash`,
branch switching, commit, push, merge, rebase, or destructive commands. Do not
access the VPS/runtime, install/deploy, use secrets, contact brokers/exchanges,
or perform network/trading actions.

## Read-only references

- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_CYCLE4_GLM_AUDIT_CLASSIFICATION_2026-07-26.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`
- `AGENTS.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/DO_NOT_TOUCH.md`

Do not edit those reference files.

## Edit only

1. `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md`
2. `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`
3. `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_MASTER_PLAN_MULTI_MODEL_AUDIT_PROMPT_2026-07-25.md`
4. `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_MASTER_PLAN_MULTI_MODEL_AUDIT_REPORT_2026-07-26.md`
5. `MTC_COMMAND_CENTER/_AI_MEMORY/DECISIONS.md`

## Required repairs

### 1. Final live risk-state transfer

Extend the ordered cutover so that after the old Windows writer is quiesced and
before first VPS start, the accepted P3-01 policy is actually applied:

- final WAL-consistent source capture and SHA-256;
- migrate the exact accepted state or execute the accepted conservative reset;
- SQLite `integrity_check`;
- application semantic checks for daily loss, consecutive loss, foreign
  positions/orders, corrupt/unknown state;
- source/destination artifact hashes and timestamped ordered record;
- block on mismatch/unknown evidence.

P4-07 must verify the exact accepted destination state artifact was loaded
before its one DISARMED start. Reuse/extend existing P4-05/P4-07 rather than
adding a separate task.

### 2. External monitoring/backup authority

Strengthen P5-01 as the separate Barış-only precondition for P5-02/P5-03. It
must cite the secret-inventory hash and separately name, without values:

- external provider/service/account and owner;
- any cost/billing limit and renewal owner;
- credential names, issuer, consumer, least privilege, storage class,
  revocation owner;
- exactly bounded account/credential provisioning and test attempts;
- whether purchase, firewall, DNS, listener, or other network change is
  authorized (none by default).

P5-02/P5-03 block until P5-01 closes. Do not reuse the TESTNET wallet authority.

### 3. Exact per-workload admission

Strengthen P6-05. The owner decision must cite the exact immutable workload
manifest SHA-256 and exact source/version/digest, dependency/SBOM hashes,
tool/MCP/plugin/scheduler allowlists, egress, credentials, unit/sandbox hashes,
resource/observation/rollback/start/end fields, accepting Gate 6 for that exact
manifest, named executor, and exactly one install/start attempt with no retry.
Require preflight and post-install hash verification.

### 4. Actual-identity isolation and final Gate 6

P6-00A authorizes implementation/testing only; it must not claim to close final
security acceptance. Make the sequence explicit:

1. implement isolation;
2. create the real `ai-lab` UID/GID/groups/workspace/environment;
3. implement final cgroup/systemd controls;
4. use P6-04 to run the **complete** P5-10 denial suite plus kill-switch test
   from the actual identity and representative child processes;
5. obtain fresh canonical Gate 6 acceptance over hashed final-identity/control
   evidence before P6-05.

P6-04 evidence includes actual identity manifest, all attack vectors, unchanged
bridge assertions, hashes, and accepting Gate 6. No workload admission before
this closure. Preserve one-shot authorization and rollback/halt behavior.

### 5. Independent post-build clean-host audit

Add exactly one new task, `KVM2-P10-03E`, after either P10-03C or P10-03D and
before P10-04. It is a read-only fresh independent post-build Gate 5/Gate 6
audit of the resulting host—not executor self-attestation. Evidence binds to:

- post-build manifest SHA-256;
- OS provenance plus host/boot/filesystem identity;
- exact restored release/state hashes and allowlist;
- listener/user/group/service/unit/package inventory;
- rotated/revoked credentials by name only;
- absence of lab/KVM2 contamination;
- accepting fresh canonical verdicts with no required repair.

P10-04 blocks unless P10-03E closes. This increases the task count from 84 to
85; update every truthful count.

### 6. Optional and partial-lab exit routes

Preserve the no-lab route and add an explicit partial-lab route:

- every optional additional Phase-7 workload and Phases 8/9 can close
  `NOT_SELECTED`/`NOT_ADMITTED` by a dated owner record proving no related
  install/start/credential/service/listener exists;
- after every actually admitted workload completes its required observation,
  the plan may proceed to Phase 10 with skipped optional work recorded;
- any one-or-more admitted lab workload marks the host contaminated for
  mainnet and still forces Option A or B—never the no-lab shortcut.

Update master dependency/resource policy and companion Phase 7–10 prose without
creating more tasks.

### 7. Primary-agent selection order

Move P7-01A before P7-01. P7-01A selects Hermes or OpenClaw and proves the
unselected agent absent. Rewrite P7-01 as provider-neutral admission of the
selected primary agent. It cites the P7-01A decision and the exact P6-05
manifest/authorization before credential provisioning, install, or start.
Observation task wording must also be provider-neutral.

### 8. No standing document-write authority

In the master authority matrix replace “Authorized by current user request”
with durable wording:

> No standing authority. Every document creation/update needs a task-specific
> explicit owner write authorization. Audit acceptance grants no edit or
> execution authority.

Reference D024 for this Cycle-4 write only and state audit sessions are
read-only.

### 9. Stale historical report

Preserve all historical evidence in
`KVM2_MASTER_PLAN_MULTI_MODEL_AUDIT_REPORT_2026-07-26.md`. Add only a prominent
top banner declaring it **SUPERSEDED HISTORICAL EVIDENCE**, retaining its old
hashes/task count as historical, and pointing readers to D024, the current
master/companion, current audit prompt, and GLM classification. Do not restamp
old evidence as current.

## Cycle 4 / D024 / audit contract

- Add `D024 | 2026-07-26` above D023. Record: owner authorized continuation as
  Cycle 4; GLM-5.2 is bounded coder and additional independent auditor; Codex
  remains lead/final authority; GLM does not replace mandatory Gate 5/Gate 6;
  documentation-only, no Git publication/VPS/deploy/secret/network/trading
  authority.
- Cycle 3 history closes at R3 `REQUEST_CHANGES` and its cap.
- Cycle 4 current state is R1 repair. Record the GLM advisory report SHA
  `0F9CB7870AF7D257D66977163F355BB416EA7A9110435CA08963BAF0F6D4F17A`
  and Codex classification file.
- Synchronize master/companion headers and master audit-plan prose.
- Update the audit prompt to Cycle 4/R1. Require an additional fresh GLM-5.2
  read-only audit whose findings Codex classifies, then a fresh exact
  `gpt-5.6-sol`/`xhigh` ephemeral/read-only direct Codex audit as final
  authority. State GLM cannot replace any mandatory Gate 5/Gate 6 requirement.
  Preserve future exact canonical Gate 5/Gate 6 requirements.
- Do not claim an audit verdict.

## Structural constraints

- Exactly 85 unique standard task IDs after adding only P10-03E.
- Every task retains exactly one `  - Evidence:` and one `  - Stop:` line.
- Crosswalk rows 1–10 appear exactly once.
- Master and companion must each remain below 60,000 bytes. The companion is
  already near the limit: compress redundant prose/table history without
  removing gates, evidence, stop conditions, or safety semantics.
- Zero full `KVM2-P...` IDs in the master.
- Valid UTF-8; no private runtime source path, public IP, secret, wallet,
  private-key path, or connection command.
- Preserve preparation-only / execution-blocked status and all authority
  separations.
- Compute final byte-level SHA-256 for master and companion only after edits
  are stable; update Cycle-4/R1 expected hashes in the audit prompt and retain
  R3 hashes as superseded history.

## Self-QA response

Report:

- changed sections/tasks;
- 85 total / 85 unique;
- malformed Evidence/Stop blocks;
- crosswalk counts;
- byte sizes;
- zero full task IDs in master;
- final SHA-256 values;
- confirmation that only the five whitelisted files changed;
- confirmation that no Git mutation, VPS/runtime, deployment, secret, network,
  broker/exchange, or trading action occurred.

Do not commit, push, or claim acceptance.
