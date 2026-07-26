# KVM2 Master Program — Consolidated Multi-Model Audit Report

> **SUPERSEDED HISTORICAL EVIDENCE — NOT CURRENT AUDIT AUTHORITY**
>
> This report preserves an earlier frozen audit, including its old hashes,
> 71-task count, findings, and verdict. Do not use it as current readiness
> evidence. Current Cycle-4 authority is D024 together with the current master,
> execution companion, Cycle-4 audit prompt, and
> `KVM2_CYCLE4_GLM_AUDIT_CLASSIFICATION_2026-07-26.md`. The historical body
> below is intentionally unchanged.

- Date: 2026-07-26
- Scope: documentation and task-plan audit only
- Status: **REQUEST_CHANGES / REPAIR LOOP EXHAUSTED / EXECUTION BLOCKED**
- Runtime authority: none

## Frozen joint input

| Artifact | SHA-256 | Size |
|---|---|---:|
| `KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md` | `10C79396D63DE330BD4F920146B8CDB0C39C10C342233AEAE4E1C8B9CCD12F02` | 34,300 bytes |
| `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md` | `8706621CE52010465B408B265267F7320078E2A79F01533E85513335619615D9` | 52,786 bytes |

The master and companion are a joint document set. The master contains policy,
architecture, authority, recovery, and evidence rules. The companion contains 71
dependency-ordered task blocks and the canonical bridge-item 1–10 crosswalk.

Lead validation before the final audit found:

- 71 unique task IDs;
- exactly one AI tag, Evidence line, and Stop line per task;
- phases 0–11 present;
- ten bridge crosswalk rows, items 1–10 exactly once;
- both joint inputs below the 60,000-byte harness limit;
- no non-loopback public IP, private local path, SSH connection command,
  private-key material/path, wallet/account identifier, or secret value.

## Audit provenance and verdict normalization

| Auditor route | Invocation identity | Raw verdict | Normalized disposition |
|---|---|---|---|
| Codex CLI | exact `gpt-5.6-sol`, effort `xhigh`, fresh ephemeral read-only session | `REQUEST_CHANGES` | **Non-accepting** |
| Direct DeepSeek harness | `deepseek-v4-pro`, fresh read-only task | `PASS-WITH-NITS` plus one MEDIUM required repair | **Invalid accepting verdict; non-accepting by verdict standard** |
| Grok harness | `grok-4`, fresh read-only task | `PASS` | Accepting advisory verdict |
| Cline plan mode | metadata: `cline-pass/deepseek-v4-pro`, fresh read-only session | `PASS-WITH-NITS` | Accepting advisory verdict; report identity prose was inconsistent with metadata |
| Canonical Claude audit | exact `claude-opus-5`, effort `xhigh` | Not run; credits unavailable | **Required audit deferred; no fallback** |

Raw-output SHA-256:

- Codex: `33140873AEBFA18D5B11077D6F88DAB2D9DF18C2A8AF967F977702F2A56C37C5`
- DeepSeek: `CD9FAD9CA21F345270490C4F6AC0A12545FB9A88CA4294FC5C3A9F87AD72E3D2`
- Grok: `09317ABEBEAAB795A9FC98FA7CBD343B78352FEBF0B48CDA5E4B5622301D688E`
- Cline JSONL: `63D51F5D1904CB9F2C9C7BE957F679B5F68EC264978155AE1D7C12AFE96811D7`

Raw logs remain outside the repository. This report contains only sanitized
findings and hashes.

## Required repair backlog

### R3-01 — Remove the resource-admission cycle (HIGH)

P5-09 currently requires a successful kill-switch breach test, but the controls
and test do not exist until P6-03/P6-04; Phase 6 cannot open until P5-09 closes.
P5-09 must accept the contract and test specification only. P6-05 must remain
blocked until P6-03/P6-04 implement and pass the dummy-workload test.

### R3-02 — Define the post-rollback path to a running, ARMED bridge (HIGH)

P4-08 leaves the service stopped/disabled. No later task separately authorizes
one post-rollback DISARMED recovery start, and P5-05 authorizes ARM without a
bounded ARM-execution task. Add distinct recovery-start authorization/execution
and ARM authorization/execution, each with single-attempt evidence.

### R3-03 — Prevent restart-profile requalification bypass (HIGH)

A restart-enabled unit admitted after the `Restart=no` stability baseline can
change recovery and resource behavior while Phase 6 still relies on old P5-09/
P5-10 evidence. Decide the active unit profile before the monitoring contract,
or invalidate and rerun P5-06 through P5-10 after any profile/hash change.

### R3-04 — Add a named Phase-9 service admission/install gate (HIGH)

Need + audit cannot authorize installation. Every optional service must receive
the same immutable manifest, explicit owner admission, bounded install attempt,
separate network/secret approvals, isolation tests, removal proof, and observation
required for a Phase-6 workload.

### R3-05 — Make Option B clean-host proof equivalent to Option A (HIGH)

The separate-VPS route must inherit the applicable trusted-image provenance,
new host/filesystem identity, no old/lab volume or snapshot, verified-only restore,
credential rotation, pre-secret negative tests, and fresh Gate 5/Gate 6 evidence.

### R3-06 — Separate artifact-layout freeze from ledger initialization (MEDIUM)

P0-04 simultaneously says it creates/validates the index and that it creates no
files. Add a separately authorized initialization task that creates `INDEX.md`,
the ledger, and validation fixtures for publishable-only, restricted-only, and
mixed rows. Require rejection tests for private paths, public IPs, credentials,
and malformed rows.

### R3-07 — Give source-scenario reconciliation immutable scope (MEDIUM)

Record the scenario source hash without its private path. Define deterministic
IDs using section heading, local number, title, and source-line span; enumerate
which numbered sets are normative; require zero unmapped IDs and a mechanical
completeness check.

### DS-F-01 — Freeze the isolation-design filename (MEDIUM)

Direct DeepSeek correctly identified that P5-10 says the isolation artifact path
is an example. Replace the example with the exact canonical path
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/loopback_isolation_design.md`
and add it to the frozen artifact index.

## Optional improvements retained

- Assign named executor/verifier roles to P2-09 and P3-04 before execution.
- Add external-provider renewal, billing failure, backup-quota, and retention-
  policy-change alerts.
- Clarify the lower bridge task's `[AI: Any]` cutover tag as mechanical work only
  after explicit owner authorization.

## Repair-loop decision

The third independent repair/re-audit round is non-accepting. Repository rules
limit the task to three non-accepting rounds. No fourth repair was started.

The next session must begin as a new explicitly owner-authorized repair cycle,
apply only the backlog above through the required counterpart implementer, freeze
new joint hashes, and obtain fresh exact-model audits. The exact
`claude-opus-5` `xhigh` audit remains mandatory when credits are available.

## Safety statement

No VPS connection, package installation, service change, firewall/network
change, secret provisioning, runtime/API/process action, broker/exchange action,
TESTNET action, cutover, ARM action, reprovision, purchase, mainnet action, git
stage, commit, push, or PR action occurred in this audit program.
