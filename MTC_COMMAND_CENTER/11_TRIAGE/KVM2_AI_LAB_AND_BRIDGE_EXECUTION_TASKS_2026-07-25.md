# KVM2 AI Laboratory and Bridge — Execution Tasks 2026-07-25

- Status: **PREPARATION ONLY / EXECUTION BLOCKED**
- Date: 2026-07-25 (Cycle-4/R1 repair 2026-07-26; D024)
- D020–D024 apply. Cycle 3 closed at capped R3 `REQUEST_CHANGES`; Cycle 4/R1
  uses advisory GLM-5.2 with Codex final authority.

## Authority and scope

This file details 85 tasks; the Bridge VPS Deploy Task List governs its ten
items. Tasks do not authorize later actions; each operational gate needs
distinct owner authority. Master governance also applies.

**Shorthand:** `bridge assertions` = PID, unit hash, loopback listener, restart
count, reconcile freshness, exchange connectivity. `HL_LIVE_ACK-absent proof`
checks unit/files/process without exposing other secrets.

## 7. Dependency-ordered master task list

### Phase 0 — Governance and scope freeze

- [ ] **KVM2-P0-01 [AI: Any] Refresh static read-only OS and repo facts.**
  - Evidence: dated OS/resource/firewall/service inventory; clean release SHA
    candidates; PR status; sanitized only. Excludes live bridge state, TESTNET
    order/position, writer, or ARM verification — those need P0-01B.
  - Stop: any uncertainty, unexpected service, dirty source, or live
    control-endpoint access needed for a static fact.
- [ ] **KVM2-P0-01B [AI: Barış] Verify owner-controlled live bridge state under separately authorized evidence procedure.**
  - Evidence: live TESTNET order/position evidence; current writer state; ARM
    state; Windows runtime/task/port/state. No AI task may call the
    unauthenticated control API merely to collect facts.
  - Stop: single-writer clarity unestablished; order/position ambiguous or
    inaccessible; ARM state unknown after verification.
- [ ] **KVM2-P0-02 [AI: Barış] Confirm the temporary lifecycle.**
  - Evidence: owner record for bridge-first TESTNET, lab only after stability,
    mainnet only after Option A or B.
  - Stop: owner wants mainnet on the mixed-use image.
- [ ] **KVM2-P0-03 [AI: Any] Reconcile the audit-model contract.**
  - Evidence: one current roster copied from `AGENTS.md` into each future audit
    prompt; the bridge task's older Opus wording must not conflict.
  - Stop: model/effort requirements disagree across authoritative documents.
- [ ] **KVM2-P0-04 [AI: Claude] Freeze the planned artifact layout and raw-evidence retention policy in both governing documents.**
  - Evidence: layout frozen in companion and master (design only — no
    directories, ledger, or fixtures created). Root
    `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/`; paths: `INDEX.md`,
    `rebuild/profiles/`, `rebuild/manifests/`, `boundaries/`,
    `boundaries/loopback_isolation_design.md`, `recovery/`,
    `rehearsals/summaries/`, `admission/contracts/`, `audits/`,
    `evidence/sanitized/`, `evidence/EVIDENCE_LEDGER.jsonl`. Raw restricted
    evidence never in this root/repo/chat; external encrypted, recorded by
    logical ID only; no private path in repo/plan. Records retention/deletion
    policy (owner, duration, trigger, Stop). Frozen before Phase 1.
  - Stop: a path overlaps protected trading/Pine/parity/schema scope; raw
    evidence or a private identifier would be committed; retention/deletion
    policy absent; Phase 1 begins before freeze.
- [ ] **KVM2-P0-04A [AI: Claude] Create and validate artifact index and ledger under separate write authorization.**
  - Evidence: (future) separate owner write authorization received; `INDEX.md`
    and `evidence/EVIDENCE_LEDGER.jsonl` created with validated schema; fixture
    rows for publishable-only, restricted-only, mixed types; rejection tests for
    private paths, public IPs, hostnames, credentials.
  - Stop: created without write authorization; any fixture row accepts a private
    path/public IP/hostname/credential; any row type untested; schema does not
    enforce three row types.
- [ ] **KVM2-P0-05 [AI: Claude] Produce the source-scenario reconciliation artifact after separate write authorization.**
  - Evidence: `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/SOURCE_SCENARIO_RECONCILIATION.md`
    (separate write authorization) with source report SHA-256 (no private path);
    deterministic scenario IDs (heading-slug + local number + normalized title +
    source-line span); every normative set enumerated; zero-unmapped-ID proof per
    set; each item mapped Required/Allowed-later/Deferred/Forbidden with
    section/rationale/conflict note; advisory-only statement and conflict
    precedence (plan+bridge list govern; source report advisory).
  - Stop: created without write authorization; source SHA-256 absent; private
    path present; any normative set not enumerated; any item unmapped; zero-
    unmapped-ID check absent; advisory status or precedence absent.

### Phase 1 — Baseline re-verification

- [ ] **KVM2-P1-01 [AI: Any] Reproduce the hardened-host baseline.**
  - Evidence: raw outputs for OS, kernel, packages, time sync, users, SSH
    policy, UFW, Fail2ban, listening sockets, enabled services, disk, memory,
    swap, `/opt`, pending security updates.
  - Stop: public non-SSH listener, password/root SSH, unknown privileged user,
    or unexplained scheduled service.
- [ ] **KVM2-P1-02 [AI: Any] Create a redacted baseline manifest.**
  - Evidence: timestamp, command list, exit codes, hashes, findings — no IPs,
    usernames, credential paths, secret values.
  - Stop: redaction cannot be proven.
- [ ] **KVM2-P1-03 [AI: Barış] Accept or reject the baseline.**
  - Evidence: explicit owner decision.
  - Stop: no acceptance; no install follows.

### Phase 2 — Prepare the clean rebuild kit now

Preparation artifacts only; no reprovision or install.

- [ ] **KVM2-P2-01 [AI: Claude] Define two machine profiles.**
  - Evidence: `temporary-testnet-lab` and `future-trading-only` profiles with an
    explicit diff of packages, users, services, network, writable paths,
    forbidden components.
  - Stop: the trading-only profile contains an AI agent, coding runner, lab
    user, browser, general automation stack, or restored lab home.
- [ ] **KVM2-P2-02 [AI: Claude] Produce the trusted-input manifest.**
  - Evidence: Ubuntu source/version, repositories, package/version lock, Python
    lock+hashes, release artifact SHA, source commit, systemd-unit hashes,
    bootstrap hash, verification procedure. OS source: official Ubuntu 24.04.x
    LTS Server or documented Hostinger image; at execution record exact image
    ID/version/URL and verify SHA256SUMS.gpg against the Ubuntu CD signing key via
    a separate official channel; if no raw image checksum, record provider
    action/identifiers + first-boot clean-origin evidence; provenance failure
    recorded explicitly.
  - Stop: floating dependency, mutable branch, global pip, unsigned/unverified
    download, unrecorded package source, or OS provenance unestablished via an
    official channel or documented provider evidence.
- [ ] **KVM2-P2-03 [AI: Claude] Define identity and filesystem boundaries.**
  - Evidence: users/groups, login/sudo policy, directories, ownership, modes,
    read-only release path, writable state/log paths, explicit cross-user denial
    tests for both profiles.
  - Stop: lab identity can read or control bridge material.
- [ ] **KVM2-P2-04 [AI: Claude] Define network and service blueprints.**
  - Evidence: firewall manifest, listener inventory, loopback assertions,
    hardened service definitions, restart throttling, resource slices, graceful
    stop, log ownership, hashes. First-start unit: separately hashed,
    `Restart=no`, manual recovery. Restart-enabled only after fault injection
    proves DISARMED startup, reconcile gating, state continuity, duplicate
    prevention, throttling; the initial unit stops when killed. Log
    rotation/retention/compression policy with config hash frozen here;
    forced-rotation test at P4-07.
  - Stop: port 8790 non-loopback; a lab service receives bridge service control;
    first-start unit uses any `Restart` value other than `Restart=no`; log
    rotation policy absent or unhashed.
- [ ] **KVM2-P2-05 [AI: Claude] Define the secret inventory without values.**
  - Evidence: secret name/purpose, owner, issuer, allowed consumer, storage
    class, mode requirement, rotation trigger, revocation procedure, backup
    inclusion/exclusion. Values absent.
  - Stop: any secret value or private key captured.
- [ ] **KVM2-P2-06 [AI: Claude] Define state continuity and recovery.**
  - Evidence: owner-accepted RPO/RTO per class (bridge state, logs/evidence,
    config/release); backup cadence/retention; WAL-consistent capture rules;
    SQLite `integrity_check` plus application-level risk-state invariants;
    off-PC encryption-key recovery; exact-release restore order; WAL-consistent
    or conservative fresh-state option per P3-01; daily/consecutive-loss and
    foreign-order/position handling; backup encryption/retention; isolated
    restore drill. Failed integrity/semantic check blocks ARM/resume.
  - Stop: restore can reset or hide risk evidence; no restore test; RPO/RTO
    undefined or not per-class; integrity check omits application-level
    risk-state invariants; off-PC key recovery untested.
- [ ] **KVM2-P2-07 [AI: Claude] Produce access-recovery and external-dependency inventories.**
  - Evidence: SSH public-key recovery procedure; DNS/domain/certificate
    inventory; provider/account ownership; off-host backup destination;
    emergency-console procedure — all without credentials.
  - Stop: recovery depends on one unavailable PC or one untested credential.
- [ ] **KVM2-P2-08 [AI: Claude] Produce teardown and destructive-reprovision manifests.**
  - Evidence: lab service/user/package/container/cron/timer/network inventory;
    data export list; credential rotation list; verified-only restore allowlist;
    items that must never cross into trading-only.
  - Stop: the plan proposes restoring the lab OS, snapshot, home, cached
    credentials, container storage, or lab package state.
- [ ] **KVM2-P2-09 [AI: Any] Verify rebuild-kit reproducibility.**
  - Evidence: named executor and verifier (not generic AI) recorded before
    execution; checksum/signature verification and rehearsal on an expendable
    clean environment producing the expected manifest without secrets.
    Candidates: Hyper-V, VirtualBox, QEMU VM, or separately authorized scratch
    VPS. If none: record P2-09 BLOCKED/UNVERIFIED; active KVM2 not allowed;
    status carried into Phase 3.
  - Stop: executor/verifier not recorded before execution; manual undocumented
    step; non-idempotent result; missing checksum; unexplained drift; no
    expendable rehearsal environment; active KVM2 proposed as host.
- [ ] **KVM2-P2-10 [AI: Claude] Define the maintenance contract.**
  - Evidence: contract definition only (no drill execution): unattended-upgrade
    config/scope; auto-restart/auto-reboot policy; owner maintenance window;
    pre-update recovery procedure; package/unit/config diff before/after updates;
    DISARMED restart+reconcile sequence; rollback procedure; rules triggering
    monitoring reset, re-audit, or lab re-admission. Drill spec (expected pre/post
    manifest format, unit hash comparison, DISARMED reconcile sequence, pass/fail
    criteria) as design; execution deferred to P4-07A.
  - Stop: auto-reboot or service-restart policy undefined; DISARMED
    restart/reconcile sequence undocumented; rollback absent.
- [ ] **KVM2-P2-11 [AI: Claude] Produce the incident and contamination runbook.**
  - Evidence: runbook with resource/SLO vs. security-boundary classification;
    CONTAMINATED response (kill lab workloads, preserve evidence, DISARM, notify
    owner, revoke/rotate TESTNET credentials, prohibit bridge resume until clean
    reprovision/migration); provider-panel-action branch covering Kodee
    snapshot/restore/reboot/firewall/service action, P5-04 reset/reclassification,
    master stop for unexplained action; incident drill record (table-top with
    hashed outcome).
  - Stop: resource breach and security breach not distinguished; CONTAMINATED
    response omits credential revocation; provider-action branch or drill absent.
- [ ] **KVM2-P2-12 [AI: Barış] Accept the rebuild kit as preparation only.**
  - Evidence: owner acceptance of documentation and recovery design; P2-09
    verdict (VERIFIED or BLOCKED/UNVERIFIED) disclosed and accepted.
  - Stop: acceptance misread as authority to reprovision or install; P2-09
    verdict not disclosed or accepted.

**Critical rule:** a Hostinger snapshot/backup captured after laboratory use is a
recovery snapshot of the lab, not a clean trading image.

### Phase 3 — Bridge release readiness

Phase 3 is BLOCKED pending P3-02's PR #25/equivalent files; Phases 0–2 may
proceed. Trace: P3-01→P3-02→P3-03→P3-04→P3-05.

- [ ] **KVM2-P3-01 [AI: Barış] Choose the risk-state continuity policy and approve its adversarial staging-test specification.**
  - Evidence: owner selection of WAL-consistent migration or conservative
    fresh-state reset; written approval of the pre-cutover staging-test spec
    (cases, failure criteria, pass/fail thresholds) that P3-03 executes.
  - Stop: owner has not selected a policy; staging-test spec not accepted before
    P3-02.
- [ ] **KVM2-P3-02 [AI: Claude] Produce the immutable candidate and all pre-start artifacts.**
  - Evidence: clean source, exact SHA, locked dependencies+hashes, tested
    Ubuntu installation, systemd-unit hashes, rollback artifact, pre-start
    matrix designs (local and Ubuntu), zero protected-scope drift.
  - Stop: branch-only identity; dirty worktree; moving dependency; or the three
    canonical bridge contract files absent from `origin/master`.
  - **Phase 3 BLOCK** — three PR #25 contract files absent from `origin/master`
    (candidate commit `cfb08b819aa9890725344e8315571299718cd554` only); BLOCKED
    until present and verified; candidate text is not merged authority:
    - `IBKR_PAPER_BRIDGE/docs/RUNTIME_BASELINE_CONTRACT.md`
    - `IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md`
    - `IBKR_PAPER_BRIDGE/docs/21_WINDOW_STATE_CONTRACT.md`
- [ ] **KVM2-P3-03 [AI: Claude] Run pre-cutover staging tests on the exact immutable candidate; produce hashed artifacts.**
  - Evidence: exact P3-02 SHA tested per P3-01 spec on local plus one named,
    expendable Ubuntu 24.04 environment from the P2-09 classes; environment
    name/class/identity recorded; active KVM2 forbidden. Tests cover WAL
    consistency, `integrity_check`, risk-state invariants, loss and
    foreign-order/position cases, corruption blocking, loopback, TESTNET; hashed
    at the canonical path. If no environment, record `BLOCKED/UNVERIFIED` plus
    the unavailable/attempted environment for P3-05.
  - Stop: any test fails without blocking continuation; tests not run on exact
    P3-02 SHA; live KVM2 staging or undeclared environment; corruption does not
    block; matrices incomplete; artifact/verdict unhashed.
- [ ] **KVM2-P3-04 [AI: Any] Independently verify the immutable candidate and evidence read-only.**
  - Evidence: named independent reviewer (not generic AI) recorded before
    verification; confirms candidate SHA, P3-02 artifacts, P3-03 evidence
    consistent and complete. No file/service/system changed.
  - Stop: reviewer not recorded; candidate hash mismatch; evidence inconsistent;
    reviewer cannot confirm without a write action.
- [ ] **KVM2-P3-05 [AI: Barış] Close fresh Gate 5/Gate 6 and the pre-cutover canonical subset.**
  - Evidence: lower-level pre-deploy contract closed before P4-01: fresh exact
    `claude-opus-5`, effort `xhigh`, no fallback, no resume/continue, auditing
    the exact repair diff and tests unless a later owner decision amends it. This
    future bridge-candidate gate is not waived by D023. Required Gate 5/6
    verdicts contain no repair; crosswalk items 1, 2, 3, 5 close; P2-09/P3-03
    exact Ubuntu environment and `VERIFIED` verdict carried.
  - Stop: the exact future Claude contract unavailable/stale/resumed/fallback or
    non-accepting; a required gate/item lacks evidence; environment/verdict
    omitted or `BLOCKED/UNVERIFIED`; P4-01 begins before this task closes.

**Canonical bridge-item crosswalk — lower-level items 1–10, once each:**

| Item | Canonical requirement | Companion closure |
|---:|---|---|
| 1 | Exact release candidate | P3-01→05 bind SHA, diff, tests, staging, and fresh canonical audits; PR/report is insufficient. |
| 2 | Reproducible Python | P2-03 freezes Python 3.12, hash-locks, and offline install; P3-02/04 verify it. |
| 3 | Hardened service boundary | P2-04/P3-03/P4-02 bind user, release, writable paths, unit hash/hardening, and masked install. |
| 4 | VPS-only TESTNET wallet | P2-05/P4-03 separately inventory/provision it; no exposed value or `HL_LIVE_ACK`. |
| 5 | Risk-state continuity | P3-01/03 accept/test migration or reset; after old-writer quiesce P4-05 proves final WAL capture, transfer/reset, integrity/semantics, and both hashes. |
| 6 | Ordered single-writer cutover | P4-04A/05 prove flat, stop old writer/listener, revoke, recheck flat, and transfer final state; P4-06/07 separately authorize/start once and load that state. |
| 7 | Private control plane | P1/P2/P4 keep 8790 loopback-only via SSH, UFW SSH-only, no public proxy; changes need separate gates. |
| 8 | Operations evidence | P2-04/06, P4-08, P5-01→06 bind manifests, rollback, logs, external authority, restore, continuity, measurements. |
| 9 | Exact-SHA test matrices | P3-02→05 close local/Ubuntu matrices; P4-07 rechecks hashes and one DISARMED TESTNET loopback start loading exact state. |
| 10 | Final gates | P3-05 keeps canonical audits; D024/GLM cannot replace Gate 5/6. Deploy, start, ARM, monitoring, mainnet remain separate. |

Rows require their evidence; the lower-level bridge list remains authoritative.

### Phase 4 — Separately authorized deploy and cutover

Each Phase-4 action needs separate owner authority; P4-01 grants no secret,
cutover, first-start, or ARM action.

- [ ] **KVM2-P4-01 [AI: Barış] Authorize installation and configuration only.**
  - Evidence: owner authorization covering exact SHA, artifact hash, attempt
    count, TESTNET restriction, named rollback-state artifact/manifest SHA (and
    prior accepted rollback release SHA when one exists), stop conditions, and an
    explicit statement that this covers installation/configuration (service
    disabled or masked) and does NOT authorize secret provisioning, cutover,
    first start, or ARM.
  - Stop: general/plan/audit approval is not install authorization.
- [ ] **KVM2-P4-02 [AI: Claude] Perform exactly one bounded installation and configuration attempt.**
  - Evidence: immutable artifact/unit hashes verified; service installed disabled
    or masked; no TESTNET secret provisioned; service not started; private
    listener prepared (127.0.0.1:8790 only); no unexpected service/process/network
    change.
  - Stop: retry before a new P4-01; service started, enabled, or armed; any
    secret value provisioned or present.
- [ ] **KVM2-P4-03 [AI: Barış] Separately authorize and perform TESTNET-only secret provisioning and transfer under the secret contract.**
  - Evidence: separate authorization for secret provisioning only; TESTNET agent
    wallet at root-owned 0600 path; no secret value in repo, chat, prompt, task
    list, shell history, or backup; `HL_LIVE_ACK` absent from unit,
    EnvironmentFile, and process env (no unrelated env secret prints); not
    provisioned under P4-01.
  - Stop: secret provisioned without a separate P4-03; any secret value in a
    non-encrypted/non-authorized location; P4-01 cited as authority;
    `HL_LIVE_ACK` present in any form.
- [ ] **KVM2-P4-04 [AI: Claude] Finalize and rehearse the cutover-abort procedure before cutover.**
  - Evidence: document walkthrough/tabletop only — no process, service,
    scheduler, listener, network, secret, exchange, or writer mutation. Walk
    through failed mid-cutover and PC-off aborts: VPS authority absent before any
    owner-controlled DISARMED Windows recovery, state/evidence preserved, zero
    dual-writer interval. Any live rehearsal needs a separate future bounded
    owner authorization.
  - Stop: any live mutation; abort/PC-off/dual-writer case unresolved; procedure
    implies permanent Windows dependency; tabletop cited as P4-04A quiesce or
    P4-05 cutover authority.
- [ ] **KVM2-P4-04A [AI: Barış] Authorize Windows-writer quiesce before cutover.**
  - Evidence: owner sentence (separate from deploy/secret/cutover); DISARMED
    confirmed; exactly one quiesce; flat via natural drain or separately
    authorized instrument-scoped flatten naming instrument(s) and attempt count;
    raw exchange-side positions/orders flat proof without secrets; single writer
    confirmed; no VPS start authorized.
  - Stop: P4-05 needs P4-04A closed; flat not achieved; more than one attempt
    without new P4-04A; flatten lacks explicit instrument scope; second writer
    appears; P4-01 or P4-03 cited as authority.
- [ ] **KVM2-P4-05 [AI: Barış] Separately authorize and execute the ordered single-writer cutover proof.**
  - Evidence: separate authorization for single-writer cutover only. Ordered
    checklist: DISARMED confirmed; fresh reconcile; raw empty positions/orders
    from exchange before revocation; Windows task stopped/disabled; child
    processes absent; port 8790 closed on old host; old-host authority revoked;
    second timestamped raw VPS exchange-side positions/orders after revocation;
    pre/post-revocation responses captured without secrets. Then apply the
    accepted P3-01 policy: final WAL-consistent source capture + SHA-256;
    migrate the exact accepted state or execute the accepted conservative reset;
    SQLite `integrity_check` passed; semantic checks for daily-loss,
    consecutive-loss, foreign positions/orders, corrupt/unknown state; source and
    destination artifact hashes + timestamped ordered record. Any mismatch or
    unknown evidence blocks the cutover. Not first-start or ARM authorization.
  - Stop: P4-04A not closed; any non-empty, stale, unknown, failed, reordered, or
    ambiguous check; post-revocation VPS exchange query absent; final
    risk-state capture/migration or SQLite `integrity_check`/semantic check fails
    or is unknown; source/destination hash mismatch; P4-01 or P4-03 cited as
    cutover authority.
- [ ] **KVM2-P4-06 [AI: Barış] Separately authorize exactly one first DISARMED start.**
  - Evidence: separate authorization for exactly one DISARMED TESTNET
    first-start; states one attempt, stop conditions, does NOT grant ARM or
    subsequent starts.
  - Stop: install, deploy, or cutover authorization cited as first-start
    authority.
- [ ] **KVM2-P4-07 [AI: Claude] Perform exactly one first-start attempt; no retry.**
  - Evidence: immutable artifact/unit hashes confirmed; first start DISARMED and
    TESTNET-only; logs captured; health check passed; reconciliation confirmed;
    restart count zero; private listener confirmed (127.0.0.1:8790 only); no
    unexpected service/network change; exact-SHA matrices passed (local and
    Ubuntu); `HL_LIVE_ACK-absent proof`; forced log-rotation test executed and
    passed per P2-04; the exact accepted destination state artifact from P4-05
    verified loaded (recorded hash matched) before this DISARMED start.
  - Stop: retry before a new P4-06; bridge started ARMED or non-TESTNET;
    service starts twice; `HL_LIVE_ACK` present in any form; forced log-rotation
    test not executed/passed; the P4-05 destination state artifact absent,
    unverified, or hash-mismatched before start.
- [ ] **KVM2-P4-07A [AI: Barış] Execute maintenance/reboot drill on KVM2 while DISARMED.**
  - Evidence: owner sentence (not P4-06/P4-07 authority); pre-drill package
    manifest and unit hashes; exactly one drill on exact P4-07 installed
    candidate; post-drill hashes compared; DISARMED restart confirmed; reconcile
    proof; required before P5-05A and P5-06.
  - Stop: not on exact P4-07 candidate; more than one attempt; restart not
    DISARMED; reconciliation absent; automatic ARM triggered; P4-06/P4-07 cited
    as authority.
- [ ] **KVM2-P4-08 [AI: Claude] Prove rollback before ARM.**
  - Evidence: named immutable rollback-state artifact/manifest SHA recorded and
    hash-recorded procedure tested. First-deploy target is the recorded state:
    service stopped/disabled, state/risk artifacts preserved, writer count zero,
    no Windows task/process/listener/exchange authority re-enabled. If a prior
    accepted VPS release exists, its rollback release SHA is recorded too.
    Recovery-start needs P4-08A; Windows-writer restoration needs new authority.
  - Stop: either required SHA absent; rollback theoretical/unhashed; service not
    stopped/disabled; state/risk lost; writer count nonzero; Windows authority,
    recovery-start, or writer restoration attempted under P4-08.
- [ ] **KVM2-P4-08A [AI: Barış] Authorize exactly one post-rollback recovery-start.**
  - Evidence: sentence authorizing exactly one DISARMED TESTNET recovery-start;
    no retry without new P4-08A; does not grant ARM.
  - Stop: rollback or P4-06/P4-08 cited as authority; more than one attempt
    authorized.
- [ ] **KVM2-P4-08B [AI: Claude] Perform exactly one post-rollback recovery-start; no retry.**
  - Evidence: artifact/unit hashes match rolled-back state; DISARMED TESTNET
    start; logs/health/reconciliation confirmed; restart count zero; loopback
    listener confirmed; single-writer verified; `HL_LIVE_ACK-absent proof`.
  - Stop: retry before new P4-08A; ARMED or non-TESTNET; secret reprovisioned
    without P4-03; `HL_LIVE_ACK` present in any form.

### Phase 5 — Bridge-only stabilization

Order: P5-02/03/03A/04 → P5-06 (≥10 accepted DISARMED days; no strategy,
orders, or ARM) → P5-07 → P5-05B/05/05A (one TESTNET strategy/ARM) → P5-08.
P5-09/10 gate every later lab workload.

- [ ] **KVM2-P5-01 [AI: Barış] Separately authorize the external monitoring/backup provider and credentials; precondition for P5-02 and P5-03.**
  - Evidence: separate Barış-only authorization (not ARM/start/lab admission/
    network exposure) citing the P2-05 secret-inventory hash. Names, without
    values: external provider/service/account and owner; any cost/billing limit
    and renewal owner; credential names with issuer, consumer, least-privilege
    scope, storage class, revocation owner; the exactly bounded
    account/credential provisioning and test attempts; and an explicit statement
    of whether any purchase/firewall/DNS/listener/network change is authorized
    (none by default). Distinct from the P4-03 TESTNET wallet authorization;
    must not reuse it.
  - Stop: P5-01 not closed before P5-02/P5-03; provider/account/owner,
    billing/renewal, credential scope/revocation, or provisioning/test bound
    absent; P2-05 secret-inventory hash not cited; a network/purchase/firewall/
    DNS/listener change assumed without an explicit authorized sentence; P4-03
    TESTNET wallet authority reused; start/deploy/ARM/plan approval cited as
    monitoring/backup authority.
- [ ] **KVM2-P5-02 [AI: Claude] Install and test alert-only local telemetry, lightweight configuration-drift detection, evidence continuity, and an independent off-host heartbeat.**
  - Prerequisite: P5-01 closed.
  - Evidence: local observer incapable of mutating the bridge; drift detection
    captures unexpected listener/package/user/service changes and alerts without
    restarting the bridge; evidence continuity tested. Heartbeat: separate
    always-on external system — never KVM2 or the Windows PC; candidates (verify
    availability/terms): third-party uptime monitor, cloud scheduler/function,
    or separately authorized external host. Contract frozen before close:
    endpoint, interval, failure timeout, thresholds, transport, destination,
    alert-only semantics, owner, credential handling, test evidence. Never expose
    port 8790 or mutate bridge state. No external source: record BLOCKER; ARM
    blocked; same-host cannot detect host/network loss.
  - Stop: watchdog can restart, ARM, DISARM, reconcile, or deploy the bridge;
    off-host heartbeat runs on KVM2 or the Windows PC; no independent external
    source and risk not explicitly recorded as BLOCKED.
- [ ] **KVM2-P5-03 [AI: Claude] Test encrypted immutable/versioned backup and restore while DISARMED.**
  - Prerequisite: P5-01 closed.
  - Evidence: WAL-consistent SQLite capture; `integrity_check` passed;
    application-level risk-state invariants (daily/consecutive-loss,
    foreign-order/position preserved); off-host encrypted backup with retention
    lock/versioning; KVM2 credential incapable of deleting versions/changing
    retention; recovery/admin credential confirmed and tested; older-version
    recovery drill; exact-release restore order and isolated restore tested;
    actual RPO/RTO measured per P2-06 class; secrets excluded; off-PC
    encryption-key recovery exercised.
  - Stop: backup claimed without a restore test; integrity or semantic check
    fails without blocking ARM/resume and alerting owner; actual RPO/RTO not
    measured; KVM2 credential can delete versions or change retention;
    older-version recovery untested.
- [ ] **KVM2-P5-03A [AI: Barış] Freeze active service-unit profile hash before P5-04.**
  - Must complete before P5-04.
  - Evidence: owner records exact service unit filename and SHA-256 (baseline
    profile hash). If restart-enabled: fault-injection matrix (crash/kill/reboot)
    proving DISARMED startup, reconciliation gating, state continuity, duplicate
    prevention, throttling complete; fresh Gate 5/Gate 6 must accept the
    restart-enabled profile before close. Baseline hash binds P5-06 through
    P5-10. Any unit/profile change after close invalidates P5-06 through P5-10;
    all rerun with the new hash before Phase 6 opens.
  - Stop: unit unhashed; restart-enabled chosen but fault-injection matrix
    incomplete or unaccepted; P5-04 attempted before close.
- [ ] **KVM2-P5-04 [AI: Barış] Accept and hash the DISARMED bridge-only monitoring/recovery/window contract before P5-06.**
  - Evidence: P5-03A already recorded. Owner reviews and hashes an immutable
    contract defining: ≥10 days DISARMED with no strategy, order submission, or
    ARM; local telemetry coverage;
    independent heartbeat coverage; heartbeat provider ownership with named
    billing/renewal contact; external-provider renewal, quota-limit, and
    billing-failure alert ownership (each named); evidence continuity; incident
    classification; reset/pause/reclassification rules for restart, reconcile-
    gap, evidence-gap, heartbeat-loss, and any provider-panel snapshot/restore/
    reboot/firewall/service action; maintenance treatment; failure/recovery
    thresholds; injected-event classification; raw metric sampling interval;
    raw-series retention covering the full window; storage class sufficient for
    P5-08 percentile derivation. Observation duration and reset/pause are
    contract fields.
  - Stop: P5-03A not complete; contract unhashed; observation semantics
    undefined; sampling interval, retention, or storage class absent;
    reset/pause/reclassification (including provider action) missing; heartbeat
    billing/renewal ownership unnamed; external-provider alerts absent; any
    strategy, order submission, or ARM during P5-06.
- [ ] **KVM2-P5-05 [AI: Barış] After P5-07 acceptance, select exactly one TESTNET strategy and authorize ARM separately.**
  - Evidence: cite P5-04, P5-06 raw-series hash, and P5-07 acceptance; record
    one strategy/configuration hash, explicit TESTNET-only ARM authorization,
    and owner-defined post-ARM observation. No lab/execution authority; P5-05A
    required.
  - Stop: install/start/monitoring/deploy approval cited as ARM authorization;
    required hashes absent; P5-07 not accepting; strategy count not one;
    strategy/configuration mutable; post-ARM observation absent.
- [ ] **KVM2-P5-05B [AI: Barış] Freeze ARMED TESTNET crash/recovery procedure before P5-05A.**
  - Must close before P5-05A; not required for DISARMED P5-06.
  - Evidence: owner records and hashes the ARMED TESTNET crash/recovery
    procedure: named authorizer/executor; one attempt per explicit new
    authorization; restart DISARMED only; raw exchange reconcile before re-ARM;
    open-position/order handling; P5-04 reclassification for crash. Hashed
    injected-crash staging drill record (table-top, hashed scenario/outcome). No
    automatic re-ARM.
  - Stop: procedure absent or unhashed; automatic re-ARM permitted; no
    injected-crash staging drill record; P5-05A starts before close.
- [ ] **KVM2-P5-05A [AI: Claude] Perform exactly one ARM attempt per P5-05; no retry.**
  - Prerequisite: P5-07, P5-05B, P5-05, and P4-07A closed before execution.
  - Evidence: pre-check P5-04/06/07 hashes, P5-03 backup, service-unit hash,
    DISARMED TESTNET, fresh reconcile, listener set, P5-05B, and exact
    strategy/configuration; prove `HL_LIVE_ACK` absent; ARM once; only that
    strategy submits simulated orders; capture logs/observation series.
  - Stop: any pre-check fails; P5-05B not closed; `HL_LIVE_ACK` present in any
    form; more than one attempt; not TESTNET-only after ARM; ARM without P5-05;
    unselected, changed, or multiple strategy/order sources.
- [ ] **KVM2-P5-06 [AI: Claude] Run the canonical bridge-only monitoring window.**
  - Prerequisite: P4-07A closed; P2-10 contract applied and drill verified on
    KVM2; P5-04 accepted before this phase.
  - Evidence: after P5-04, confirm DISARMED and no strategy/order source; apply
    its observation semantics. Record reconciliation, disconnects, restarts,
    resources, log growth, state integrity, and incidents; retain/hash samples
    at the specified interval for ≥10 accepted days. No ARM, strategy, order,
    or lab.
  - Stop: P4-07A not closed; P2-10 not applied/verified on KVM2; P5-04 contract
    undefined; fewer than 10 accepted days; sampling/retention deviates; ARM,
    strategy, order submission, lab, or misclassified interruption.
- [ ] **KVM2-P5-07 [AI: Barış] Accept or reject bridge stability.**
  - Evidence: owner decision based on complete P5-06 monitoring evidence and all
    classified incidents. Elapsed calendar time alone is not acceptance.
  - Stop: evidence incomplete; unresolved incident unclassified; elapsed time is
    the sole basis.
- [ ] **KVM2-P5-08 [AI: Claude] Derive resource capacity and thresholds from accepted Phase 5 raw monitoring data.**
  - Evidence: hash-cite P5-06 DISARMED and post-P5-05A one-strategy series;
    derive peak/percentile resource, bridge, reconcile, restart/log measures,
    lab budget, and bridge reserve mechanically from the worse case.
  - Stop: either series incomplete/unhashed; estimated values; raw metrics do
    not reproduce the budget.
- [ ] **KVM2-P5-09 [AI: Barış] Accept and hash the AI-lab resource admission contract and kill-switch test specification, only after P5-08.**
  - Evidence: owner accepts and hashes a contract from real P5-08 data: sample
    interval; baseline duration/percentile; per-metric absolute/relative
    thresholds; breach count/duration; hysteresis/reset/reclassification; disk
    reserve; per-workload CPU/memory/IO/process ceilings; kill-trigger;
    observation duration/reset/pause; dummy-workload kill-switch spec (workload
    type, trigger, pass/fail, no-bridge-mutation) — executed at
    P6-03/P6-04/P6-05. P5-08 metrics must reproduce every threshold.
  - Stop: values not from P5-08 data; metrics do not reproduce thresholds;
    kill-switch specification absent; contract unhashed; accepted before P5-08.
- [ ] **KVM2-P5-10 [AI: Claude] Produce the OS-enforced same-host loopback/control-plane isolation design and negative-test plan at a canonical artifact path; obtain fresh Gate 5/Gate 6 acceptance before Phase 6 opens.**
  - Evidence: design document at the exact canonical path
    `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/boundaries/loopback_isolation_design.md`
    with an immutable hash accepted by fresh Gate 5 and Gate 6 (PASS or
    PASS-WITH-NITS). The design includes: (a) chosen architecture (dedicated lab
    network namespace with no route to host loopback/control interfaces, or
    permissioned authenticated Unix-socket, or equivalent OS-enforced
    mechanism); (b) creation and verification procedure; (c) route/firewall/
    namespace rules covering `127.0.0.1:8790`, `::1:8790`, all alternate host
    interfaces/routes, proxy variables, inherited file descriptors,
    service-control buses, bridge paths, `/proc`/ptrace, SSH-agent/private-key
    sockets, Docker/root sockets, host metadata, shared `/tmp` and `/dev/shm`,
    journald via `systemd-journal`/`adm` group, abstract AF_UNIX sockets, kernel
    keyrings, and unapproved egress from every admitted lab identity and child
    process; bridge/lab units require `PrivateTmp=yes` where applicable;
    (d) SSH-tunnel preservation proof; (e) rollback procedure; (f) pass/fail
    criteria for each negative test.
  - Stop: design artifact absent, unhashed, or not at a canonical path; any
    Gate 5/Gate 6 audit contains a required repair; SSH-tunnel preservation not
    proven; any Invariant 7 attack vector omitted; Phase 6 opens before close.
### Phase 6 — AI-laboratory admission gate

Phase 6 needs P5-09/P5-10 and P5-03A; failure closes the lab absent a newly
audited architecture. Drift needs new hashes, Gate 6, and owner.

- [ ] **KVM2-P6-00A [AI: Barış] Authorize the Phase-6 control implementation campaign.**
  - Evidence: owner sentence cites exact P5-09 contract and P5-10 design hashes,
    names executor, closes the network/security gate, and authorizes one bounded
    P6-01-through-P6-04 campaign including exactly one P6-04 dummy-workload/
    kill-switch attempt. This authorizes implementation and testing only; it does
    NOT close final security acceptance — fresh canonical Gate 6 acceptance over
    the hashed final identity and controls is required at P6-04 before P6-05. Any
    failure/retry requires a new P6-00A.
  - Stop: either hash/executor/network gate absent; scope exceeds P6-01–P6-04;
    any substep starts without P6-00A; final security acceptance claimed by
    P6-00A or any task before the P6-04 Gate 6 closure; failure or retry
    proceeds without a new one.
- [ ] **KVM2-P6-01 [AI: Claude] Implement and negatively test the accepted OS-enforced isolation design from P5-10, under P6-00A authorization.**
  - Evidence: P6-00A closed; P5-10 isolation design implemented on the live VPS;
    all P5-10 negative tests executed with results recorded; every P5-10 attack
    vector (full list enumerated in P5-10) blocked from every lab identity;
    bridge journals/AF_UNIX/keyrings/PrivateTmp isolation confirmed; SSH-tunnel
    preserved; bridge assertions recorded before and after — none may change;
    regression invokes P5-10(e) rollback and halts Phase 6. Intermediate
    isolation evidence only; the final accepting canonical Gate 6 over the
    complete final identity and controls is obtained at P6-04, not here.
  - Stop: P6-00A not closed; any negative test fails; any bridge assertion
    changes after implementation; final security acceptance claimed before the
    P6-04 Gate 6 closure; real lab workload admitted before P6-04 closes.
- [ ] **KVM2-P6-02 [AI: Claude] Implement the `ai-lab` user/workspace boundary and execute denial tests under P6-00A.**
  - Evidence: P6-00A closed; dedicated unprivileged user and separate workspace/
    clone on the live VPS; no sudo, bridge group, service control, Docker socket,
    Docker-group membership, bridge paths, raw bridge logs, secret paths, or SSH
    private keys; cross-user denial tests executed only under P6-00A. Every
    workload requires the admission manifest enforced at P6-05 (exact
    source/version/digest, dependency lock and SBOM hashes, allowlists, egress,
    credentials, unit/sandbox hashes); where a standard SBOM is unavailable,
    exact pinned install method, dependency tree, package checksums, and an
    SBOM-absence record accepted by Gate 6. Lab-owned secrets reside in a
    separate lab-only namespace; no path/inheritance shared with bridge secrets
    or state. Denial assertions per P6-01 confirmed; bridge assertions captured
    pre/post and unchanged; admission changes need new hashes, Gate 6, owner
    approval. Regression invokes P5-10(e) rollback and halts Phase 6.
  - Stop: P6-00A absent; bridge access/denial succeeds incorrectly; manifest or
    secret separation incomplete; any bridge assertion regresses without
    P5-10(e) rollback and Phase-6 halt; retry without new P6-00A.
- [ ] **KVM2-P6-03 [AI: Claude] Define and implement laboratory resource and execution controls under P6-00A authorization.**
  - Evidence: P6-00A closed; dedicated `systemd` slice/cgroup ceilings,
    kill-switch unit, and execution controls on the live VPS; SHA-256 of each
    unit file recorded; manual start initially; bounded process count/runtime;
    outbound-only where possible; task-scoped credentials; approval mode enabled;
    browser disabled; local host terminal disabled or separately sandboxed;
    bridge assertions captured before and after — all unchanged; regression
    invokes P5-10(e) rollback and halts Phase 6.
  - Stop: P6-00A not closed; any unit file SHA-256 missing; any bridge assertion
    changed after implementation; regression triggers without P5-10(e) rollback;
    retry without new P6-00A.
- [ ] **KVM2-P6-04 [AI: Claude] Run the complete P5-10 denial suite and kill-switch from the final identity, then obtain fresh canonical Gate 6 acceptance.**
  - Prerequisite: P6-00A closed; P6-01, P6-02, P6-03 complete so the real
    `ai-lab` UID/GID/groups/workspace/environment and final cgroup/systemd
    controls exist and are hashed.
  - Evidence: exactly one authorized attempt. Run the COMPLETE P5-10 denial
    suite plus the P5-09 dummy-workload kill-switch from the actual `ai-lab`
    identity and representative child processes; all lab processes stop on
    kill-switch. Evidence binds the actual-identity manifest and every P5-10
    attack vector (full list in P5-10) blocked from the final identity and
    children; pre/post bridge assertions unchanged; artifact hashes recorded.
    Then obtain a fresh canonical Gate 6 acceptance (AGENTS.md roster, fresh
    session, no fallback) over the hashed final-identity/control evidence before
    P6-05. Regression invokes P5-10(e) rollback and halts Phase 6; no workload
    admitted before this closure. One-shot: failure/retry needs new P6-00A.
  - Stop: P6-00A absent; P6-01/P6-02/P6-03 not complete; any denial vector or
    kill-switch fails or deviates; any bridge assertion regresses without
    P5-10(e) rollback and Phase-6 halt; final-identity/control evidence
    unhashed; fresh canonical Gate 6 not accepting on the exact evidence before
    P6-05; more than one attempt or retry without new P6-00A; any workload
    admitted before closure.
- [ ] **KVM2-P6-05 [AI: Barış] Authorize one named laboratory workload by exact manifest.**
  - Prerequisite: P6-01, P6-02, P6-03, P6-04 all closed; P6-03/P6-04
    dummy-workload test chain complete; P6-04 fresh canonical Gate 6 acceptance
    over hashed final-identity/control evidence recorded.
  - Evidence: owner decision cites the exact immutable workload manifest SHA-256
    and its source, version/digest, dependency lock and SBOM hashes,
    tool/MCP/plugin/scheduler allowlists, egress, credentials, unit/sandbox
    hashes, and resource/observation/rollback/start/end fields per the P5-09
    contract; a fresh accepting canonical Gate 6 verdict over that manifest; a
    named executor; exactly one install/start attempt, no retry; preflight and
    post-install hash verification of the loaded manifest. Active unit hash
    matches the P5-03A baseline.
  - Stop: manifest SHA-256 or any manifest field (source/version/digest,
    dependency/SBOM hashes, allowlists, egress, credentials, unit/sandbox hashes,
    resource/observation/rollback/start/end) absent; Gate 6 not accepting on the
    exact manifest; executor unnamed; more than one attempt or any retry; no
    preflight/post-install hash verification; any of P6-01–P6-04 not closed or
    P6-04 final-identity Gate 6 not recorded; active unit hash mismatches
    P5-03A; broad "install the lab" approval insufficient.

Observe every admitted workload for the P5-09 duration before another. A bridge
SLO breach disables it and captures evidence; automation cannot mutate bridge
state.

### Phase 7 — Low-risk AI-lab rollout

Each Phase-7 workload needs its own P6-05-style owner record. Optional work may
close `NOT_SELECTED` with dated no-install/start/credential/service/listener proof.

- [ ] **KVM2-P7-01A [AI: Barış] Select the single primary agent and keep the unselected agent absent.**
  - Evidence: explicit selection of Hermes or OpenClaw as the one primary agent;
    the unselected agent is absent and has no service, user, credential,
    scheduler, or data directory.
  - Stop: no selection recorded before P7-01; concurrent or alternating
    always-on agents proposed without a new capacity and security audit.
- [ ] **KVM2-P7-01 [AI: Claude] Admit the selected primary agent in read-only/reporting mode.**
  - Prerequisite: P7-01A closed.
  - Evidence: cites the P7-01A selection decision and the exact P6-05 manifest/
    authorization before any credential provisioning, install, or start;
    unprivileged install of the selected primary agent; minimal tools; approvals
    enabled; browser off; no host shell or separately audited sandbox; no bridge
    paths/secrets/service control; manual start; resource budget; clean disable/
    removal procedure. Read-only/reporting mode: writes only to admitted
    log/output directory; no subprocess unless allowlisted; no bridge API/path/
    secret/Docker socket; outbound only to manifest allowlist.
  - Stop: P7-01A not closed; credential provisioning, install, or start precedes
    the P7-01A decision or the exact P6-05 manifest/authorization; the selected
    agent requires root, bridge access, Docker socket, or unrestricted
    credential passthrough; any write lands outside its admitted log/output
    directory.
- [ ] **KVM2-P7-02 [AI: Claude] Complete the selected primary-agent observation per the P5-09 contract observation duration.**
  - Evidence: bridge SLO unchanged; resource/log/network usage measured for the
    duration defined in the P5-09 contract; no unauthorized file or service
    access.
  - Stop: bridge degradation or policy violation disables the agent; observation
    duration shorter than specified in the P5-09 contract.
- [ ] **KVM2-P7-03 [AI: Claude] Admit one scheduled transcript/report job class.**
  - Evidence: bounded input/output path, duplicate handling, runtime/resource
    ceiling, failure notification, no auto-commit/push. Barış authorizes
    admission separately per P6-05.
  - Stop: unbounded queue, uncontrolled browser use, or bridge impact.
- [ ] **KVM2-P7-04 [AI: Claude] Admit controlled coding last.**
  - Evidence: before admission, a distinct owner decision ID (not a task ID)
    cites an immutable coding-manifest hash; it cannot reuse
    Hermes/prior-workload authorization. Record permissions, resource budget,
    credential scope, observation duration, rollback, start/end conditions,
    isolated clone, protected-scope rules, patch/report-first output, bounded
    tests.
  - Stop: decision ID/hash or any field absent; prior authority reused; coding
    agent can mutate deployed release, deploy, or exceed its admitted boundary.
- [ ] **KVM2-P7-05 [AI: Barış] Keep GitHub self-hosted runner excluded.**
  - Evidence: no runner service, registration, token, or workflow execution on
    the mixed host.
  - Stop: a workflow runner is proposed; use another environment.

Kodee is out-of-band: require panel MFA and forbid snapshot/restore/reboot/
firewall/service actions while deployed. Any action resets P5-04; unexplained
action invokes the master stop rule.

### Phase 8 — MTC visibility

- [ ] **KVM2-P8-01 [AI: Any] Prefer the existing private static/Sites catalog; produce immutable design manifest.**
  - Evidence: refreshed sanitized private snapshot; no fabricated KPI or
    secret/raw content. If catalog absent/unsuitable, record fallback/scope
    reduction, not a public dashboard. Hash a pre-build design covering scope,
    auth, listener/network/dependencies, rollback, domain/certificate use.
  - Stop: freshness/redaction/fallback unproved; design absent/unhashed; build
    starts.
- [ ] **KVM2-P8-02 [AI: Claude] Validate Linux paths and build/start readiness without building or starting.**
  - Evidence: cite P8-01; hash current repo/Linux paths and readiness for
    dedicated user, private read-only auth/data allowlist, no writer/full-report
    exposure, budget, rollback, unit/config; override stale Windows/legacy
    paths. No build/install/start/listener/firewall/network mutation.
  - Stop: unintended/frozen path; no readiness hash; any forbidden mutation.
- [ ] **KVM2-P8-01A [AI: Barış] Admit one Phase-8 build/start after design and readiness.**
  - Evidence: owner cites P8-01/P8-02 hashes, names executor, authorizes one
    P8-03 attempt with stops/no retry; listener/firewall/domain/public/network
    change has a fresh security gate. Builder cannot self-authorize.
  - Stop: hash/executor/bound/network gate absent; early
    start/self-authority/retry.
- [ ] **KVM2-P8-03 [AI: Claude] Perform exactly one authorized bounded build/start.**
  - Evidence: verify P8-01/P8-02/P8-01A; named executor makes one attempt;
    record unit/config hashes and listener/firewall diff; pre/post bridge
    assertions unchanged.
  - Stop: prerequisite/bound missing; network drift; regression—rollback and
    halt.
- [ ] **KVM2-P8-04 [AI: Claude] Verify network separation and bridge invariants.**
  - Evidence: no public/non-loopback bind or 8790 proxy; audited
    listener/firewall diff and unchanged P8-03 assertions. Domain/certificate
    extends the existing P5-02 monitor with expiry threshold, owner/contact, and
    a tested synthetic expiry alert.
  - Stop: 8790 exposed; assertion differs; second monitor or missing expiry
    proof.

### Phase 9 — Optional services after measurements

Optional services run P9-01→02→02A→03→04; Gate 6/network/credential gates stay
separate. Skips need dated `NOT_SELECTED`/`NOT_ADMITTED` absence proof.

- [ ] **KVM2-P9-01 [AI: Barış] State the concrete need before each optional service.**
  - Evidence: problem, expected value, alternatives, sensitivity, capacity
    estimate, removal plan, and why an existing managed service is insufficient.
  - Stop: installation justified only by unused capacity.
- [ ] **KVM2-P9-02 [AI: Claude] Security/capacity audit; produce immutable service manifest; obtain Gate 6 accepting verdict.**
  - Evidence: dependency/network/secret/storage/backup model and headroom;
    manifest with exact version, source hash, dependency lock/checksums,
    network/secret requirements (noting separate gates), user/sandbox profile,
    removal procedure; fresh independent Gate 6 accepting verdict (claude-opus-5
    xhigh + gpt-5.6-sol xhigh per AGENTS.md roster, fresh sessions, no fallback)
    on the exact P9-02 manifest before P9-02A. Gate 6 acceptance authorizes no
    install, start, network, secrets, or other action. If a domain/certificate is
    proposed, the manifest extends the existing P5-02 monitor with expiry
    threshold, named owner/renewal contact, and a synthetic expiry-alert test.
  - Stop: service expands bridge trust or failure boundary; manifest lacks exact
    version or hash; Gate 6 accepting verdict not obtained via canonical models
    before P9-02A; any canonical model unavailable and Barış has not waived it.
- [ ] **KVM2-P9-02A [AI: Barış] Owner admission decision citing P9-02 manifest hash.**
  - Evidence: sentence citing exact P9-02 manifest hash; names service,
    exactly-one-attempt authorization, stop conditions, rollback, and any
    required separate gates (see Phase 9 header).
  - Stop: manifest hash absent; required gates implied not gated; open-ended
    permission or more than one attempt authorized; Gate 6 accepting verdict on
    the P9-02 manifest not yet recorded.
- [ ] **KVM2-P9-03 [AI: Claude] Bounded one-attempt install/start; prove isolation.**
  - Evidence: exactly one install and start per P9-02A; unit/config hashes
    recorded; bridge SLO and listener/process state unchanged; isolation
    confirmed — no bridge path/secret/service-control/API reachable from
    service identity.
  - Stop: multiple attempts without new P9-02A; isolation fails; bridge state
    changes; removal attempted here.
- [ ] **KVM2-P9-04 [AI: Claude] Observe for P5-09 contract duration; test disable/removal; record bridge SLO comparison.**
  - Evidence: full P5-09 contract duration completed; bridge metrics vs
    pre-admission baseline; no SLO breach; log growth bounded; no unauthorized
    access; at end of observation, service disabled and removed without touching
    bridge (single test; no second install/start authorized); evidence hashed.
    For any domain/certificate, a tested synthetic expiry alert with threshold
    and owner/renewal contact remains in the P5-02 stack.
  - Stop: bridge SLO breached (disable service, capture evidence; automation
    must not mutate bridge state); disable/removal test not performed before
    acceptance; second optional service starts before acceptance.

### Phase 10 — Mainnet fork decision

Phase 10 is mandatory after full lab, recorded partial lab, or P5-07/P5-08 plus
hash-cited P5-06 no-lab evidence. Any admission contaminates the host and forces
Option A/B. All routes retain P10-02, P10-03A/B, P10-03C/D, P10-03E, P10-04.

- [ ] **KVM2-P10-01 [AI: Claude] Produce measured capacity and contamination evidence.**
  - Evidence: cite P5-07 acceptance plus P5-06/P5-08 hashes and demand; record
    lab branch with lab/credential/teardown inventory, or no-lab with Phases 6–9
    `NOT_ADMITTED`.
  - Stop: branch/evidence/measurements missing; no-lab skips Phase 10.
- [ ] **KVM2-P10-02 [AI: Barış] Choose Option A or Option B explicitly.**
  - Evidence: signed/dated owner decision with cost, downtime, recovery,
    isolation rationale.
  - Stop: no implicit choice from an existing subscription.
- [ ] **KVM2-P10-03A [AI: Barış] Accept the immutable Option A packet and authorize its bounded actions before execution.**
  - Evidence: packet hash covers provenance, trading-only first boot, verified
    release/state allowlist, credential rotation, no-lab proof, rollback, G5/G6.
    Prove DISARMED, raw flat exchange, final WAL capture, isolated P2-06/P5-03
    restore, agent trading authority revoked, zero writers. Before action Barış
    separately authorizes (i) one wipe, (ii) one bootstrap/first-boot sequence,
    (iii) one verified restore, naming each
    target/executor/hashes/stops/no-retry.
  - Stop: field/proof missing; lab image/snapshot/credential reused;
    early/open/combined/retry/self-authorized action.
- [ ] **KVM2-P10-03C [AI: Claude] Execute only the already-authorized Option A actions and record evidence.**
  - Evidence: named executor revalidates P10-03A, then performs its one wipe,
    bootstrap/first boot, verified restore. Record provenance, new host/boot/
    filesystem IDs, rotated credentials, exact restore, no-lab/rollback/G5/G6.
  - Stop: executor cannot self-authorize or deviate; failed precheck; excess
    attempt; proof fails.
- [ ] **KVM2-P10-03B [AI: Barış] Accept the immutable Option B packet and authorize its bounded actions before execution.**
  - Evidence: packet hash names provider/target and covers provenance, P2 first
    boot, verified restore, credential rotation, no-KVM2/no-lab tests, rollback,
    G5/G6. Prove DISARMED, raw flat exchange, final WAL capture, isolated
    restore, agent trading authority revoked, zero writers. Before action Barış
    separately authorizes (i) one purchase, (ii) one provisioning/bootstrap
    sequence, (iii) one verified restore, naming each
    provider/target/executor/hashes/stops/no-retry.
  - Stop: field/proof missing; KVM2 image/snapshot/credential reused;
    early/open/combined/retry/self-authorized action.
- [ ] **KVM2-P10-03D [AI: Claude] Execute only the already-authorized Option B actions and record evidence.**
  - Evidence: named executor revalidates P10-03B, then performs its one
    purchase, provisioning/bootstrap, verified restore. Record provenance, new
    host/boot/filesystem IDs, pre-secret rotation, verified-only restore,
    no-KVM2/no-lab/rollback/G5/G6.
  - Stop: executor cannot self-authorize or deviate; failed precheck/excess
    attempt; purchase cited as clean proof; provenance/restore/proof fails.
- [ ] **KVM2-P10-03E [AI: Barış] Obtain a fresh independent post-build clean-host Gate 5/Gate 6 audit before mainnet.**
  - Prerequisite: the executed Option A (P10-03C) or Option B (P10-03D) actions
    complete; read-only audit by an independent auditor, not the executor.
  - Evidence: fresh independent read-only Gate 5/Gate 6 audit of the resulting
    host — not executor self-attestation — binding to: post-build manifest
    SHA-256; OS provenance plus host/boot/filesystem identity; exact restored
    release/state hashes and allowlist; listener/user/group/service/unit/package
    inventory; rotated/revoked credentials by name only; absence of lab/KVM2
    contamination; and accepting fresh canonical verdicts (per AGENTS.md roster,
    fresh sessions, no fallback) with no required repair.
  - Stop: P10-03C/P10-03D not complete; audit performed by the executor or any
    non-independent party; any binding field absent; lab/KVM2 contamination
    present; canonical verdict non-accepting or containing a required repair;
    P10-04 attempted before this task closes.
- [ ] **KVM2-P10-04 [AI: Barış] Authorize mainnet only in a separate final gate.**
  - Prerequisite: P10-03E closed.
  - Evidence: clean-host proof, exact release, risk-state continuity, security
    audits, the accepting P10-03E post-build verdict, rollback, monitoring,
    owner checklist, explicit mainnet sentence.
  - Stop: P10-03E not closed; TESTNET history, reprovision, purchase, deploy, or
    ARM approval is not mainnet approval.

### Phase 11 — Transition and evidence retention

- [ ] **KVM2-P11-01 [AI: Claude] Verify the selected final topology.**
  - Evidence: role/listener/user/service/secret/backup inventories for every
    host, plus single-writer proof and absence of forbidden co-tenancy.
  - Stop: undocumented service, listener, credential, or writer.
- [ ] **KVM2-P11-02 [AI: Claude] Revoke obsolete authority and archive evidence.**
  - Evidence: revoked old wallets/tokens/keys, disabled obsolete services,
    encrypted retained audit/incident/restore records, retention policy.
  - Stop: deletion occurs before recovery and audit evidence is secured.
- [ ] **KVM2-P11-03 [AI: Barış] Close the temporary-lab lifecycle.**
  - Evidence: explicit acceptance of the final trading/lab separation and
    unresolved-risk register.
  - Stop: any host role, credential, writer, or unresolved risk remains unclear.
