# KVM2 AI Laboratory and Bridge Master Deployment Plan

- Date: 2026-07-25 (Cycle-4/R1 repair 2026-07-26)
- Audit-cycle map (D023 ratifies Cycle 3; D024 authorizes Cycle 4):
  - Cycle 1: original rounds 1–3; closed non-accepting at the cap.
  - Cycle 2: R1 = round-5 focused repair; R2 = staged round-6/7 repair; R3 = final-repair-sync/slices; closed by the final non-accepting Opus verdict and STOP.
  - Cycle 3: owner-authorized by D023; R1 = exact `gpt-5.6-sol`/`xhigh` `REQUEST_CHANGES`; R2 = transport `BLOCK` after hash verification but before content audit; R3 = exact Codex `REQUEST_CHANGES`; closed non-accepting at its cap.
  - Cycle 4: owner-authorized by D024 for this artifact-only repair; current state R1. GLM-5.2 is a bounded coder and additional advisory auditor; Codex remains lead/final authority. GLM does not replace mandatory Gate 5/Gate 6 auditors.
- Hash history (most recent first):
  - Superseded Cycle-3/R3 master input (`REQUEST_CHANGES`):
    `2F2CB58785A06ACC7BDEFC790C1466B8072E8355504438F1C79BBDF4426EC7E2`
  - Superseded Cycle-3/R3 companion input (`REQUEST_CHANGES`):
    `C98AADA35C2D8175A45945ADF583F72A4853CF9F23E825ECDE45E3339E92659C`
  - GLM-5.2 advisory report:
    `0F9CB7870AF7D257D66977163F355BB416EA7A9110435CA08963BAF0F6D4F17A`
  - Superseded Cycle-3/R1 audit input (`REQUEST_CHANGES`):
    `A595A85A36CCA6BEB2C9D9568CD4BE368BC0F4A3A930622F62B91E13D2FAC68A`
  - Superseded Cycle-2 final-repair-sync input (before Cycle-3/R1):
    `CA0A8943916F653A11656A3A415B516100252D436DFA928C7BCCB96569BA9F38`
  - Superseded round-7 repair input (before final-repair-sync):
    `BAA3EDE4B2E22674AD1EBFF210AEE012CA7EF0DFAEFCBC738D534E4325693747`
  - Superseded round-6 repair input (before round-7 repair):
    `C88C12E6B3EB8AC3BC87D706472240F391ED0B221E241C62B849EA238B34BF44`
  - Superseded round-5 repair input (before round-6 repair):
    `10468C8A12F72F467CD0105CC4C3049862498E45E0E816A2C43827895DE77C5C`
  - Superseded round-4 repair input (before round-5 repair):
    `3C61B08B17867C2EEB602FD407CF327C95FF7446DB492304DDB6A926A3E8EF3C`
  - Superseded split-intermediate (before P5-06 ref fix):
    `3B275B846B2D09804428C44A70B7155AF987DE0D941BBB5B1E99A7A0234E3FBA`
  - Superseded pre-split master input (round-3 post-repair, before split):
    `3C7764DD006026274F9677FF2B8E81F4240B39BF638BB42427AE256860286475`
  - Superseded round-2 repair input (before round-3 repair):
    `C8D4CFBEA2BF7C3F5E831D4A5748E25F875429A8B3445CDAD900B98C198140CE`
  - Execution companion initial frozen input hash:
    `8706621CE52010465B408B265267F7320078E2A79F01533E85513335619615D9`
- Status: **PREPARATION ONLY / EXECUTION BLOCKED**
- Host role: bridge-first Hyperliquid TESTNET host, then a conditional temporary
  AI laboratory
- Scope: end-to-end planning, task ordering, clean-rebuild preparation, evidence
  requirements, and owner/audit gates
- Authority: this document authorizes no installation, deployment, secret
  provisioning, network exposure, runtime action, broker/exchange action, TESTNET
  action, ARM action, reprovision, purchase, or mainnet/live action

The lower-level bridge authority remains
`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`.
Nothing here duplicates, bypasses, or weakens its ten ordered bridge tasks.

## 1. Brutally honest architecture verdict

| Scenario | Verdict | Reason |
|---|---|---|
| Bridge-first, controlled TESTNET co-tenancy after proven stability | **CONDITIONAL GO** | Acceptable as a temporary learning/laboratory compromise if every admission, isolation, resource, and rollback gate below passes |
| Bridge plus unmanaged AI agents, CI, Docker socket, public apps, and automation | **NO-GO** | Too many privileged and failure-prone workloads share one kernel, disk, network, and failure domain |
| Mainnet/live trading on an OS image previously used as an AI laboratory | **ABSOLUTE NO-GO** | Removing Hermes, containers, users, or packages does not restore trust in the host |
| Mainnet after destructive clean reprovision, or on a separate clean VPS | **CONDITIONAL FUTURE GO** | Requires a trading-only build, rotated credentials, verified restore, fresh audits, and separate owner authorization |

Unix users, file permissions, containers, and `systemd` resource controls reduce
risk. They do **not** create a separate hardware, kernel, administrator, disk, or
network trust boundary.

Maximizing the VPS's value means maximizing **verified useful uptime and
recoverability**, not maximizing the number of installed services.

## 2. Owner decisions captured

1. The Windows PC cannot remain continuously powered.
2. Getting the bridge ready and safely deployed to KVM2 is the first priority.
3. The canonical Bridge VPS Deploy Task List remains blocked until its repairs,
   exact audits, and separate owner gates are complete.
4. During TESTNET only, KVM2 may become a temporary, restricted AI laboratory
   after a bridge-only stability period succeeds.
5. A mainnet decision will be made in several months:
   - **Option A:** destructively reprovision KVM2 from a trusted clean Ubuntu image
     and rebuild it as trading-only; or
   - **Option B:** obtain a separate clean trading VPS and keep KVM2 as the lab.
6. The reproducible clean-image/rebuild kit must be prepared now, without
   reprovisioning or installing anything now.
7. D024 authorizes only this Cycle-4 document repair. It grants no standing
   document-write, Git, runtime, VPS, deployment, secret, network, trading,
   purchase, reprovision, or mainnet authority.

## 3. Success definition

This program is successful only when all of the following are true:

- the bridge runs from one exact, immutable, independently accepted release;
- there is exactly one writer;
- the bridge starts DISARMED, stays TESTNET-only, reconciles correctly, and has
  tested rollback and state recovery;
- monitoring and encrypted off-host recovery are proven, not merely configured;
- AI-lab workloads cannot read bridge secrets/state, control the service, or
  exhaust resources outside measured limits;
- every lab service is admitted separately and can be stopped without touching
  the bridge;
- the future trading-only host can be rebuilt from trusted inputs without
  restoring the lab operating system, lab home directories, or lab snapshots;
- a clean-mainnet transition requires either destructive reprovision of KVM2
  from a trusted clean image or a separate clean trading VPS; uninstalling lab
  software and using a lab snapshot are never accepted as clean proof.

## 4. Dated facts — re-verify before every action

These are copied from the canonical 2026-07-25 bridge task and are drift-prone:

- KVM2 has Ubuntu 24.04, key-only SSH, disabled root SSH, UFW default-deny with
  only port 22 allowed, Fail2ban, automatic security updates, and time sync.
- The observed capacity was 96G disk and 7.8 GiB RAM.
- Python 3.12 and git were present; pip, Docker, the bridge application, and
  `/opt` application contents were absent.
- `origin/master` and the clean active Windows runtime worktree `C:\P2RT` were at
  `008e065e8e0ffa68f46134da6698d58f91ef2dcb`.
- The Windows runtime was still a writer; its exact state was deliberately
  unknown and possibly ARMED.
- PR #25 was open and unmerged at
  `cfb08b819aa9890725344e8315571299718cd554`.
- Local TS-P1-001 was unpublished and unaccepted.
- No canonical clean, merged, independently accepted deployment SHA existed.
- The bridge deployment verdict was **BLOCK**.

None of these facts may be reused in a later session without live read-only
verification.

## 5. Non-negotiable invariants

1. Bridge first; laboratory services are optional guests.
2. TESTNET only on the mixed-use host. Mainnet is forbidden.
3. Exactly one bridge writer at all times.
4. The dirty main worktree is never a deployment source.
5. Deploy only an immutable exact SHA with accepted independent evidence.
6. First start is DISARMED. Deploy, start, ARM, lab admission, and network
   exposure are separate approvals.
7. The unauthenticated bridge control API remains on `127.0.0.1:8790` and is
   reached only through an SSH tunnel. **UFW inbound rules, Unix user
   accounts, and loopback-only bind do not prevent a same-host lab process
   from connecting directly to `127.0.0.1:8790` or `::1:8790`.** Lab
   admission is BLOCKED until an OS-enforced isolation design receives fresh
   Gate 5/Gate 6 acceptance. Acceptable designs: (a) a dedicated lab network
   namespace with no route to the host loopback or control interfaces, or (b) a
   permissioned authenticated Unix-socket or equivalent OS-enforced
   architecture. The design and its negative tests must cover
   `127.0.0.1:8790`, `::1:8790`, alternate host interfaces and routes, proxy
   variables, inherited file descriptors, service-control buses, bridge paths,
   `/proc`/ptrace, SSH-agent/private-key sockets, Docker/root sockets, host
   metadata, shared `/tmp` and `/dev/shm`, journald access via
   `systemd-journal`/`adm` group, abstract AF_UNIX sockets, kernel keyrings,
   and unapproved egress from every admitted lab identity and child process.
   Bridge and lab service units must use `PrivateTmp=yes` where applicable.
   The authorized owner SSH-tunnel route must remain functional.
   Tailscale and private overlay networks do not solve same-host loopback
   isolation; their admission is DEFERRED to a separate network Gate 6.
8. UFW remains inbound port 22 only unless a separate network change is scoped,
   audited, and explicitly authorized. Port 8790 is never reverse-proxied.
9. No secret value enters the repository, chat, prompt, task list, shell history,
   logs, screenshots, or plaintext backups.
10. AI-lab processes cannot read bridge secrets, state/database, writable
    directories, raw logs, service credentials, or SSH private keys.
11. AI-lab processes cannot start, stop, restart, enable, disable, ARM, DISARM,
    reconcile, deploy, update, or otherwise control the bridge.
12. No automatic repository pull, automatic production deployment, or mutable
    branch-based release.
13. Resident lab agents NEVER receive root, sudo, bridge, service, credential,
    or control authority. Hostinger Kodee is an out-of-band provider control-plane
    actor, not a resident `ai-lab` Unix-user workload; guest Unix permissions do
    not constrain it or provide assurance against provider-panel action. The
    panel account requires MFA. While the bridge is deployed, Kodee must not
    initiate snapshot, restore, reboot, firewall, or service action. Any such
    action forces P5-04 monitoring reset/reclassification; an unexplained action
    triggers the master stop rule. A fresh, externally invoked, owner-authorized
    management-plane Claude/Codex implementer remains distinct from resident lab
    agents and may receive bounded elevated scope only through a separate owner
    authorization for the named task.
14. No AI agent receives the Docker daemon socket. Docker-group membership is
    treated as host-root authority.
15. A lab snapshot or backup is never accepted as a clean trading image.
16. Uninstalling agents is not cleaning; future reuse for mainnet requires a
    destructive reprovision from trusted installation media.
17. Any confirmed breach of a security boundary, kernel trust, credential
    storage, bridge path, control route, or service-control bus by any lab
    process requires: (a) killing all lab workloads; (b) preserving all evidence
    without mutation; (c) marking the host CONTAMINATED; (d) human-controlled
    DISARM and containment; (e) TESTNET credential revocation and rotation;
    (f) prohibition of bridge resume or ARM until a trusted destructive reprovision
    or migration to a separately clean bridge host is complete. No watchdog or
    automated process may mutate bridge state as part of incident response. A
    resource or SLO breach (not a security boundary breach) stops only the newest
    lab workload.

## 6. Workload classification

| Workload | Classification | Admission rule |
|---|---|---|
| MTC Paper Bridge TESTNET | Required, but currently BLOCKED | Canonical bridge task and all separate gates |
| Local process/health telemetry | Allowed with bridge | Read-only and incapable of bridge mutation |
| Alert-only watchdog | Allowed after bridge deploy | No automatic bridge restart initially |
| Encrypted off-host backup | Required | Consistent capture plus successful restore drill |
| External host-down heartbeat | Required | Outbound signal; no bridge control endpoint exposure |
| Sanitized static MCC snapshot/catalog | Allowed later | No secrets, raw reports, writer CLI, or bridge control |
| Hermes or OpenClaw read-only analysis/reporting | Allowed later | Select only one primary agent; Phase 6 admission and isolated execution. Read-only minimum: writes only to admitted own log/output path, no subprocess unless allowlisted, no bridge API/path/secret, no Docker/socket, egress only to manifest allowlist |
| Scheduled transcript/report jobs | Allowed later | One job class at a time after measurements |
| Controlled coding workspace | Allowed later | Patch/report output first; no deployment authority |
| Browser automation | Deferred | Separate capacity/security audit; initially disabled |
| n8n, PostgreSQL, Redis, Grafana/Loki stack | Deferred | Proven need and measured headroom required |
| Docker Engine | Deferred — separate admission required | Installation of Docker Engine requires a separate owner/security admission review demonstrating that a container-free alternative is insufficient; no agent Docker socket at any point; separate rootless/isolation design required |
| Docker Compose or management platform | Deferred | Requires separately audited need and measured headroom; no agent Docker socket; separate rootless/isolation design required |
| Uptime Kuma or similar uptime dashboard | Deferred | Same-host monitoring never counts as host-down detection; requires separately audited need and capacity measurement |
| Telegram alert bot | Deferred; if admitted: outbound alert-only | No chat command or control path; inbound trigger is forbidden; outbound alert message only |
| Netdata/Glances or similar host-metrics UI | Deferred | Requires separately audited need; same-host dashboard never counts as host-down monitoring |
| Tailscale or private overlay network | Deferred — network Gate 6 | Does not solve same-host loopback isolation; requires separate network scope, security audit, and owner approval |
| GitHub self-hosted runner | **Forbidden on mixed host** | Persistent workflow compromise risk |
| Public webhook that can reach the bridge | **Forbidden** | Creates a public trading control path |
| Public bridge/dashboard control endpoint | **Forbidden** | Violates loopback/private control invariant |
| Heavy backtests or optimization | **Forbidden** | Keep on suitable separate compute |
| Local large LLM | **Forbidden** | Resource and reliability conflict |
| Mainnet/live trading on lab image | **Forbidden** | Requires clean reprovision or separate clean VPS |

## 7. Dependency-ordered master task list

The complete dependency-ordered task list (all phases 0–11, all 85 task blocks,
canonical bridge-item crosswalk items 1–10, Phase 3 BLOCK, and per-task Evidence
and Stop lines) is the sole detailed authority of the execution companion:

`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`

That companion is **PREPARATION ONLY / EXECUTION BLOCKED**. No task *definition*
appears in this master; shorthand cross-references (such as 'P4-07') appearing in
phase summary rows are pointers to companion task definitions only. The companion
governs task text; any conflict between a master cross-reference and the companion
task definition is a BLOCK until reconciled by the owner. No full `KVM2-P...` task
ID appears in this master. No task completion in the companion authorizes the next
action or any installation, deployment, secret provisioning, cutover, first start,
ARM, lab admission, network exposure, reprovision, purchase, or mainnet/live action.
Every execution, audit, owner, network, secret, deploy, cutover, ARM, lab, and
mainnet gate remains separate and requires a distinct explicit owner sentence.

Auditors must read and evaluate this master and the execution companion together.
Neither is complete without the other.

### Phase summary

| Phase | Purpose | Hard Predecessor | Close Gate |
|---|---|---|---|
| 0 | Governance and scope freeze | None | Owner lifecycle decision (P0-02); audit-model reconciliation (P0-03) |
| 1 | Baseline re-verification | Phase 0 | Owner baseline acceptance (P1-03) |
| 2 | Prepare clean rebuild kit (preparation only — no install) | Phase 1 | Owner rebuild-kit acceptance as preparation only (P2-12) |
| 3 | Bridge release readiness — **BLOCKED** pending PR #25 merge or equivalent | Phase 2; three PR #25 contract files present in `origin/master` | Acyclic trace P3-01 → P3-02 → P3-03 → P3-04 → P3-05; named expendable Ubuntu 24.04 P2-09-class environment, never active KVM2; P3-05 closes the lower-level pre-deploy audit contract under the current `AGENTS.md` roster with fresh exact `claude-opus-5`/`xhigh`, no fallback/resume, on the exact candidate diff/tests unless a later explicit owner decision amends it |
| 4 | Separately authorized deploy and cutover | Phase 3 | P4-04 is tabletop-only; P4-04A/P4-05 separately quiesce the old writer, capture/migrate or conservatively reset final WAL-consistent risk state, prove SQLite/application semantics and source/destination hashes, then P4-07 proves the exact accepted destination artifact was loaded before one DISARMED start. Rollback and recovery-start remain separate |
| 5 | Bridge-only stabilization | Phase 4 | P5-01 separately authorizes any named external monitoring/backup account, cost, credential, provisioning/test, purchase, firewall, DNS, listener, or network scope; none is implicit. Unit/ARM/recovery/monitoring/capacity gates remain ordered. Optional lab additionally needs P5-09/P5-10; rejection does not bypass Phase 10 |
| 6 | AI-laboratory admission gate | P5-09 and P5-10 both closed | P6-00A authorizes implementation/testing only. P6-01–P6-03 create isolation, the actual `ai-lab` identity, and final controls; P6-04 runs the complete denial/kill-switch suite from that identity and children and obtains fresh final-evidence Gate 6 acceptance. P6-05 then admits exactly one immutable-manifest workload, one install/start attempt, no retry |
| 7 | Low-risk AI-lab rollout | Phase 6 | P7-01A first selects Hermes or OpenClaw and proves the other absent; P7-01 then admits the selected agent provider-neutrally. Every workload has separate manifest/owner authority; optional additions may close `NOT_SELECTED`; GitHub runner remains excluded |
| 8 | MTC visibility | Phase 7 or recorded optional skip | Design/readiness/admission/build/verification remain ordered; optional Phase 8 may close `NOT_SELECTED`/`NOT_ADMITTED` with dated absence proof |
| 9 | Optional services after measurements | Phase 8 or recorded optional skip | Each admitted service retains manifest, Gate 6, owner, one-attempt install, observation and removal gates; optional Phase 9 may close `NOT_SELECTED`/`NOT_ADMITTED` with dated absence proof |
| 10 | Mandatory mainnet fork decision | Full-lab, partial-lab, or no-lab route after mandatory bridge evidence | Any admitted lab workload contaminates the host and forces Option A or B. After bounded Option A/B execution, P10-03E obtains fresh independent post-build Gate 5/Gate 6 acceptance before separate P10-04 mainnet authority |
| 11 | Transition and evidence retention | Phase 10 | Temporary-lab lifecycle closed; unresolved-risk register accepted (P11-03) |

**Phase 3 BLOCK:** Three canonical bridge contract files are currently absent from
`origin/master` (referenced from PR #25 candidate commit
`cfb08b819aa9890725344e8315571299718cd554` only). Phase 3 tasks P3-02 onward
remain BLOCKED until these files are present in `origin/master` and independently
verified. Phases 0–2 may reference the candidate commit as the expected future
source; candidate text is not merged authority. See Section 15 for the file list.

## 8. Resource admission policy

**Three acyclic routes:** Phases 6–9 are optional and conditional; Phase 10 is
mandatory. After P5-07 acceptance, completed P5-08 evidence, and hash-cited P5-06
monitoring history:

- full lab: P5-09/P5-10 → Phases 6–9 → Phase 10;
- partial lab: after each admitted workload completes its required observation,
  record later optional Phase-7 work and Phases 8/9 as `NOT_SELECTED` or
  `NOT_ADMITTED`, then proceed to Phase 10;
- no lab: reject/not admit the lab for instability, headroom, or security; record
  Phases 6–9 as `NOT_ADMITTED`; proceed directly to Phase 10.

Every skipped item needs a dated owner record proving no related install, start,
credential, service, or listener exists. Any admitted workload marks the host
contaminated and still forces Option A or B. No route bypasses the fork choice,
bounded action packets, fresh independent post-build Gate 5/Gate 6 audit, or
separate final mainnet gate. Unaccepted bridge evidence blocks Phase 10.

Do not predeclare that 7.8 GiB RAM or two vCPUs are sufficient. Derive limits from
the bridge-only monitoring window (P5-08).

Before admitting a lab workload, record:

- bridge CPU, memory, swap pressure, disk/IO, network, latency, reconciliation
  freshness, restart count, and log-growth baseline;
- reserved bridge headroom and lab hard ceilings;
- disk warning/stop thresholds and minimum recovery space;
- maximum lab runtime, process count, memory, CPU, IO, and browser concurrency;
- the lab kill switch and the exact evidence that it leaves the bridge untouched.

Any bridge SLO breach, unexplained reconcile delay, restart loop, sustained swap
pressure, disk pressure, or state-integrity anomaly stops new admissions and
disables the newest lab workload. It does not trigger an automated bridge restart.

An owner-accepted, immutably hashed AI-lab resource admission contract
(see Phase 5 in the execution companion) is required before any lab workload may
be admitted under Phase 6.
The contract must be derived from real Phase 5 monitoring data; provisional or
invented threshold values are not permitted. Raw metrics must mechanically
reproduce the admission or rejection result.

## 9. Monitoring, restart, and backup policy

- Before external monitoring or backup work, P5-01 requires a separate
  Barış-only decision citing the secret-inventory hash and naming, without
  values, each provider/service/account and owner; cost/billing limit and
  renewal owner; credential issuer, consumer, least privilege, storage class,
  and revocation owner; bounded provisioning/test attempts; and whether any
  purchase, firewall, DNS, listener, or other network change is authorized.
  Default is none. TESTNET wallet authority cannot be reused.
- Initial watchdog behavior is alert-only.
- Automatic bridge restart is prohibited until restart safety, DISARMED startup,
  reconciliation, state continuity, throttling, and duplicate-action protection
  are separately proven and accepted. The initial bridge service unit must use
  `Restart=no`; a separately hashed restart-enabled profile may be admitted only
  after those proofs are completed and independently accepted (see P2-04).
- Local telemetry covers process/service state; an off-host heartbeat covers host
  or network loss. The off-host heartbeat must originate from a separate always-on
  external source, never from KVM2 or the Windows PC. Its contract (endpoint,
  interval, timeout, thresholds, transport, destination, alert-only semantics,
  owner, credential handling, and test evidence) must be frozen before the
  heartbeat is considered active. It must never expose or call port 8790 or mutate
  bridge state. Same-host monitoring cannot detect host or network loss.
- If an admitted Phase 8/9 service uses a domain or certificate, extend this same
  off-host monitor—do not create another stack—with an expiry threshold, named
  owner/renewal contact, and a tested synthetic expiry alert.
- Backups are encrypted off-host, integrity-checked, retention-controlled, and
  periodically restored in isolation. Backup storage must use versioned or
  retention-locked storage. The KVM2-held backup credential may create objects
  but must not have permission to delete object versions or change retention
  policies. A separately held recovery and admin credential is required for
  version deletion and retention changes. Proof that an older retained version
  can be recovered must be demonstrated before ARM (P5-03).
- SQLite/state capture must be WAL-consistent or follow the accepted conservative
  reset policy.
- Persistent-log rotation, retention, and compression policy must be frozen and
  hashed during Phase 2 (P2-04); a forced-rotation test must pass before first
  start (P4-07).
- Recovery requires owner-accepted RPO and RTO per bridge-state class, logs/
  evidence class, and config/release class, as defined in P2-06. A failed
  `integrity_check` or application-level semantic check blocks ARM/resume and
  alerts the owner.
- Secret values and private keys are excluded from ordinary backups; recovery uses
  documented reissuance/rotation unless a separately approved encrypted secret
  recovery design exists.

## 10. Clean rebuild artifact checklist

- [ ] Two-profile machine contract
- [ ] Trusted OS/source manifest
- [ ] Package/version/repository lock
- [ ] Python dependency lock with hashes
- [ ] Immutable release SHA/artifact/hash
- [ ] User/group/sudo/login matrix
- [ ] Directory/ownership/mode matrix
- [ ] Firewall/listener contract
- [ ] Hardened service definitions and hashes
- [ ] Resource-slice definitions
- [ ] Secret inventory without values
- [ ] State migration/reset and WAL-consistent capture procedure
- [ ] Encrypted off-host backup and retention policy
- [ ] Successful isolated restore record
- [ ] SSH public-key/emergency-console recovery procedure
- [ ] DNS/domain/certificate inventory
- [ ] Audit/log/incident retention policy
- [ ] Lab teardown and credential-rotation manifest
- [ ] Trading-only restore allowlist
- [ ] Reproducible bootstrap design and rehearsal record
- [ ] Checksums/signatures and verification procedure
- [ ] Rollback and disaster-recovery runbook

### KVM2 program artifact root

The canonical artifact root for this program is:
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/`

Exact planned paths under that root:
- `INDEX.md`
- `rebuild/profiles/`
- `rebuild/manifests/`
- `boundaries/`
- `boundaries/loopback_isolation_design.md`
- `recovery/`
- `rehearsals/summaries/`
- `admission/contracts/`
- `audits/`
- `evidence/sanitized/`
- `evidence/EVIDENCE_LEDGER.jsonl`

Restricted raw evidence (raw shell output, exchange evidence, private identifiers)
never enters this root, the repository, or any chat session. Its external encrypted
location is owner-selected and recorded only by a logical ID — no private path
appears in the repository or in this plan. The evidence ledger captures only
sanitized hash-linked artifacts suitable for the repository.

Task P0-04 freezes the planned artifact layout and the restricted raw-evidence
retention and deletion policy (owner, duration, deletion trigger, stop condition)
in both governing documents; this must be frozen before Phase 1 begins. A future
separately authorized P0-04A execution creates and validates `INDEX.md`, the
evidence ledger, and all validation fixtures. Do not create artifact directories
or files as part of this planning document. This plan-edit session creates no
artifact directories or files.

### No-secret decision record template

```text
Decision ID:
Date/time:
Owner:
Phase/task:
Exact artifact or document hash:
Current role/profile:
Requested action:
Authorized attempt count:
Required preconditions:
Observed evidence references:
Rollback/stop trigger:
Secret names involved (names only, no values):
Decision: APPROVE / REJECT / DEFER
Explicitly NOT authorized:
```

## 11. Cross-model audit plan

This master plan and every executable child artifact are **NOT YET independently
audited**.

D023's Cycle 3 closed non-accepting at capped R3. D024 authorizes only this
Cycle-4 documentation repair and its fresh read-only audits. Cycle 4/R1 requires
an additional independent GLM-5.2 read-only audit, after which Codex verifies
and classifies every finding as ACCEPTED, REJECTED, or NEEDS_VERIFICATION.
A fresh exact `gpt-5.6-sol`/`xhigh` ephemeral/read-only direct Codex audit then
acts as final acceptance authority. No resume/continue, alias, or fallback is
allowed. GLM is advisory and cannot replace any mandatory Gate 5/Gate 6 auditor.
The future lower-level bridge-candidate gate still requires the exact canonical
roster in `AGENTS.md`, including fresh `claude-opus-5`/`xhigh`, unless a later
explicit owner decision amends it.

Audit package:

1. scope and authority contract;
2. immutable hash of this master plan and the execution companion (both required);
3. actual files/diff;
4. evidence and raw validation outputs;
5. relevant repo rules and canonical bridge task;
6. explicit request for PASS, PASS-WITH-NITS, REQUEST_CHANGES, or BLOCK.

Cycle 4 starts a fresh count under D024; this repair is R1. Each independent
audit is read-only and grants no edit or execution authority. Any required
repair remains non-accepting; PASS-WITH-NITS contains optional nits only.
Model/session limits block the gate and never authorize fallback.

**Audit verdict scope:** An audit verdict assesses whether the master plan is
complete, acyclic, safe, and executable as a task plan. A truthfully declared
future dependency — such as absent PR contract files, future Phase 5 monitoring
data, or a pending owner decision — is not by itself a document defect when it
has a documented predecessor, assigned owner, evidence requirement, stop condition,
and clear downstream block. Auditors must still report any missing or ambiguous
gate, even for a correctly declared future dependency. The distinction: a correctly
gated future dependency earns a note; an ungated claim of current readiness earns
a REQUIRED_REPAIR.

## 12. Execution authority matrix

| Action | Current authority | Required next gate |
|---|---|---|
| Create/update this plan | No standing authority. D024 authorizes this Cycle-4 write only | Every later creation/update needs task-specific explicit owner write authorization. Audit acceptance grants no edit or execution authority |
| Read-only fact refresh | Not granted by plan alone | Bounded task scope and current owner consent where runtime/exchange evidence is involved |
| Install packages/services | Not authorized | Accepted scoped design/security audit plus explicit P4-01 install authorization. P4-01 install authorization does NOT grant secret provisioning, cutover, first start, or ARM. |
| Build/merge release | Not authorized | Existing repo workflow, exact audits, and separate merge authority |
| Provision/transfer secrets | Not authorized | Separate P4-03 Barış-only secret authorization; explicitly not granted by install/deploy/audit acceptance |
| Provision external monitor/backup accounts or credentials | Not authorized | Separate P5-01 owner decision cites the secret inventory and names provider/account/owner, billing limit, credential roles, bounded attempts, and any purchase/network scope; none by default |
| Deploy bridge (install + configure) | Not authorized | P4-01 (install authorization, service disabled/masked) then P4-02 (bounded install attempt, no start) |
| Execute single-writer cutover | Not authorized | P4-04 document walkthrough/tabletop only—no process, service, scheduler, listener, network, secret, exchange, or writer mutation; any live rehearsal needs a future bounded owner authorization. Actual action remains P4-04A quiesce plus P4-05 cutover, with raw exchange flat proof before and after authority revocation |
| First DISARMED start | Not authorized | P4-06 (separate Barış first-start authorization) then P4-07 (exactly one attempt); post-rollback recovery-start requires separate P4-08A authorization then P4-08B execution; not granted by install, cutover, or deploy authorization |
| Prove rollback before ARM | Not authorized | P4-08 requires a named immutable rollback-state artifact/manifest SHA and hash-recorded tested rollback procedure yielding stopped/disabled service, preserved state/risk, zero writers, and no Windows authority; if a prior accepted VPS release exists, record its rollback release SHA too. Recovery-start remains separately P4-08A/P4-08B |
| ARM bridge | Not authorized | P5-05 explicit Barış ARM authorization citing P5-04 contract hash; P5-05B crash/recovery procedure frozen and staging drill complete before P5-05A; then P5-05A bounded one-attempt ARM execution; no automatic re-ARM or retry; never implied by start, deploy, monitoring, or lab authorization |
| Admit one AI-lab service | Not authorized | P6-00A permits isolation implementation/testing only. Actual identity/final controls, complete denial/kill-switch suite, and fresh exact-evidence Gate 6 acceptance close first; P6-05 then cites one immutable manifest, named executor, and exactly one install/start attempt with no retry |
| Admit controlled coding | Not authorized | Distinct P6-05-style owner decision ID plus immutable coding-manifest hash, permissions, resource budget, credential scope, observation duration, rollback, and start/end conditions; selected-agent or prior-workload authority cannot be reused |
| Phase 8 bounded build/start | Not authorized | P8-01 design hash → P8-02 no-build/readiness hash → P8-01A owner admission citing both plus any network gate → P8-03 exactly one named-executor build/start → P8-04 network/bridge proof; no self-authorization |
| Change firewall/private network/public exposure | Not authorized | Separate network scope, security audit, and owner approval |
| Provider-panel action while bridge deployed | Forbidden | Panel-account MFA required; Kodee must not initiate snapshot, restore, reboot, firewall, or service action; any such action resets/reclassifies P5-04 monitoring and an unexplained action triggers the master stop rule |
| Reprovision/wipe KVM2 | Not authorized | P10-03A Barış-only packet acceptance/pre-action sentence closes first and separately authorizes one named wipe, one bootstrap/first-boot sequence, and one verified restore with target, executor, hashes, stops, no retry; P10-03C only executes that packet. P10-02 is no authority |
| Purchase another VPS | Not authorized | P10-03B Barış-only packet acceptance/pre-action sentence closes first and separately authorizes one purchase, one provisioning/bootstrap sequence, and one verified restore with provider/target, executor, hashes, stops, no retry; P10-03D only executes that packet. P10-02 is no authority |
| Mainnet/live action | Forbidden | Option A/B bounded build, fresh independent post-build Gate 5/Gate 6 acceptance on the resulting host, then separate explicit final owner authorization |

## 13. Global stop and rollback triggers

Stop the current phase and report before retrying when any of these occurs:

- unexpected writer, position, order, exposure, or bridge state;
- stale/failed reconciliation or unknown risk-state continuity;
- dirty/mutable/unidentified release source;
- failed or missing exact-model audit;
- secret exposure or uncertain credential scope;
- bridge control listener outside loopback;
- unexpected inbound port, privileged user, service, timer, or container;
- restart loop, duplicate action, resource exhaustion, swap/disk pressure, or
  material bridge latency regression;
- lab access to bridge files, logs, state, secrets, service control, or Docker
  socket;
- failed SQLite `integrity_check` or application-level semantic check (see P2-06, P5-04);
- any confirmed lab process route to the bridge control endpoint at
  `127.0.0.1:8790` or `::1:8790`;
- failed backup integrity or restore test;
- unexplained Kodee/provider-panel snapshot, restore, reboot, firewall, or service
  action while the bridge is deployed (an explained authorized action still
  forces P5-04 monitoring reset/reclassification);
- deviation from the single permitted attempt;
- any proposal to reuse the laboratory image for mainnet;
- any confirmed breach of a security boundary, kernel trust, credential storage,
  bridge path, control route, or service-control bus by any lab process: mark
  host CONTAMINATED; kill all lab workloads; preserve all evidence without
  mutation; notify owner immediately; require human-controlled DISARM and
  containment; revoke and rotate all TESTNET credentials; prohibit bridge resume
  or ARM until trusted destructive reprovision or migration to a separately clean
  bridge host is complete; no watchdog or automated process may mutate bridge
  state as part of incident response. A resource or SLO breach (not a security
  boundary breach) stops only the newest lab workload.

Rollback means disabling/removing the newest lab workload or reverting the bounded
deployment according to the accepted recovery procedure. It never means
automatically changing bridge trading state.

## 14. Future-chat pickup

Read in this order:

1. repository `AGENTS.md`;
2. `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`;
3. this master plan;
4. `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`
   (execution companion — sole detailed authority for the 85 task blocks);
5. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`;
6. newest sections of `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, and `ACTIVE_FILES.md`.

Then re-verify every dated VPS, repo, PR, SHA, runtime, state, order, position,
listener, audit, and provider-availability fact. Do not infer install, merge,
deploy, secret, cutover, TESTNET, ARM, lab-admission, network, reprovision, purchase,
or mainnet authority from the existence or completion of this plan.

## 15. Canonical references

- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`
  (execution companion — sole detailed authority for the 85 task blocks;
  initial frozen input hash:
  `8706621CE52010465B408B265267F7320078E2A79F01533E85513335619615D9`)
- `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`
- `IBKR_PAPER_BRIDGE/docs/17_DEPLOYMENT.md`
- `IBKR_PAPER_BRIDGE/docs/RUNTIME_BASELINE_CONTRACT.md` (currently referenced
  from the PR #25 candidate and absent from this checkout)
- `IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md` (currently referenced
  from the PR #25 candidate and absent from this checkout)
- `IBKR_PAPER_BRIDGE/docs/21_WINDOW_STATE_CONTRACT.md` (currently referenced
  from the PR #25 candidate and absent from this checkout)

**Phase 3 BLOCK:** While the three files above are absent from `origin/master`,
Phase 3 tasks P3-02 onward remain BLOCKED (see Phase 3 header and P3-02 for full
detail). This is a correctly gated external dependency (PR #25 merge or equivalent)
with a documented predecessor, assigned owner, stop condition, and clear downstream
block — not a plan defect. Phases 0–2 preparation work may reference the PR #25
candidate commit as the expected future source, but candidate text is not merged
authority.

- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/SOURCE_SCENARIO_RECONCILIATION.md`
  (planned under P0-05 write authorization; not yet created)

- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/README.md`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/README.md`
- `MTC_COMMAND_CENTER/00_CONFIG/paths.example.json`
- `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/ACTIVE_FILES.md`

## 16. Evidence and accountability

### Canonical evidence ledger (future artifact)

Before any runtime or security-critical task is executed, define one canonical
future evidence ledger with one row per task ID containing:

- task ID and description;
- prerequisite task IDs;
- authorizer (named person or role, not a generic AI tag);
- named executor (for runtime/security-critical tasks, not `[AI: Any]`);
- independent verifier (for runtime/security-critical tasks, not `[AI: Any]`);
- `publishable_artifact_path` (sanitized artifact path under the canonical
  artifact root defined in P0-04; suitable for the repository; may be absent
  for restricted-only rows);
- `restricted_raw_evidence_logical_id` (logical identifier for raw evidence
  stored externally encrypted; never a private filesystem path, private IP,
  hostname, or credential; may be absent for publishable-only rows);
- artifact SHA-256 hash;
- UTC timestamp;
- data classification (`public-sanitized` / `restricted-encrypted` / `mixed`);
- verdict (`PASS` / `FAIL` / `BLOCKED` / `OPEN`);
- stop/retry history.

The ledger schema must support three row types: (a) publishable-only rows
(artifact in repo, no external restricted evidence); (b) restricted-only rows
(no publishable artifact; logical ID only); (c) mixed rows (both a publishable
summary artifact and a restricted raw evidence logical ID). A `publishable_artifact_path`
must point to a file under the canonical artifact root; a `restricted_raw_evidence_logical_id`
must never contain a private filesystem path, private IP, hostname, or credential.
Validate all three row types before deploying the ledger schema.

Runtime-critical and security-critical tasks cannot retain `[AI: Any]` as the
final accountable executor or verifier. Static read-only fact collection (P0-01,
P1-01, P1-02) may use `Any` for the fact-gathering role, but owner-only live
exchange/order/position/ARM verification requires a named human executor.

Note: the creation of this plan document does not create any artifact directories
or files. The future separately authorized P0-04A execution task creates and
validates the `INDEX.md` file, the evidence ledger, and all validation fixtures
at that time.

### Two-tier evidence handling

Raw evidence (shell output, SSH session logs, exchange/position/order evidence)
is restricted: store encrypted outside the repository and outside any chat
session. Sanitized hash-linked artifacts (redacted manifests, checksums, command-
list summaries without values or private identifiers) are publishable in the
repository under the canonical artifact root.

Before publishing any artifact:
- apply allowlisted field filters;
- run automated secret and PII scans;
- complete manual review;
- confirm no public IP, private-key path, SSH command, credential, wallet
  address, account identifier, or private identifier appears.

Define raw evidence retention duration and deletion policy before Phase 1 begins.
No private identifier may appear in this plan or in any artifact committed to the
repository.
