Status: SCOPING AND PRICING MATERIAL ONLY — NO AUTHORITY, NO GATE OPENED, NO ACCEPTANCE DECISION

> **Correction, 2026-08-16 morning:** the plan-precedence question is resolved —
> owner decision §3 (`OWNER_DECISIONS_2026-08-16_MORNING.md`) ratifies the
> cumulative reading, which is the same union this file's interim rule already
> applied; the interim rule's substance therefore continues as the ratified
> rule. The Pathscope R01→R02 live-programme dependency at line ~95 is
> superseded by §6 (supplemental-with-disclosure; not a join condition).
> Retention/RPO-RTO and other owner facts named here remain open — they are not
> among the six decisions.

# Lane L8 — R27 / KVM2 Phase-0 technical governance: P0-01, P0-03, P0-04, P0-04A, P0-05

- Lane input: `C:\tmp\lane_kick\L8.md` (2026-08-15).
- Repository inspected **read-only** at `C:\RO`, detached at `25564449` (verified
  `git rev-parse HEAD`). No write, index-lock, or host/network action was taken.
- This file is the lane's single output. It produces material for the Lead and
  the owner; it decides no gate, asserts no authorization, and closes no task.
- Method: read the four governing/context documents named in the kickoff, the
  documents they directly cite, the `KVM2_PROGRAM` artifact tree itself, and the
  roster/routing records. Searches run: repo-wide glob for
  `KVM2_PROGRAM*/EVIDENCE_LEDGER*/SOURCE_SCENARIO*`; grep for `P0-01|P0-03`
  across `MTC_COMMAND_CENTER` (4 hits, all planning documents — no status or
  tracker document names either task); read-only `git log`/`git show` for the
  artifact tree and roster-drift commit.
- Citation aliases used below:
  - `COMPANION` = `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md` (sole detailed authority for task text)
  - `MASTER` = `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md`
  - `WBD` = `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md`
  - `PAR` = `MTC_COMMAND_CENTER/11_TRIAGE/PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md`
  - `REFRESH` = `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md`
  - `DTL` = `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`
  - `INDEX` = `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/INDEX.md`
  - `READY` = `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/audits/READINESS_STATUS.md`
  - `SSR` = `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/SOURCE_SCENARIO_RECONCILIATION.md`
  - `LEDGER` = `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/EVIDENCE_LEDGER.jsonl`
  - `DEC` = `MTC_COMMAND_CENTER/_AI_MEMORY/DECISIONS.md`
  - `ROUTING` = `MTC_COMMAND_CENTER/_AI_MEMORY/AI_ACCOUNT_AND_MODEL_ROUTING.md`

## 0. Headline

1. **The `KVM2_PROGRAM/` artifact tree exists and is committed** (created at
   commit `6fe0130f`, 2026-07-26 21:28:59 +03, "feat(kvm2): complete Cycle 4
   VPS bridge readiness"; `git log --follow` shows no later commit touching it).
   This makes two of the five tasks **partially executed** in artifact terms
   (P0-04A created-but-unverified; P0-05 a recorded placeholder), one **partially
   frozen** (P0-04: layout frozen, retention policy not), and leaves two
   **unexecuted as defined** (P0-01, P0-03).
2. The master plan's own "not yet created" sentence about
   `SOURCE_SCENARIO_RECONCILIATION.md` (`MASTER:568-569`) is **stale** relative
   to the committed tree; `INDEX:30-34` already discloses that governing files
   retain stale sentences because they were outside the 2026-07-26 batch's write
   whitelist. This is the same staleness class `PAR:74` records for the
   Phase-3 blocker text.
3. **Every one of the five tasks, and R27 as a whole: `NO SOURCED ESTIMATE`.**
   No document read by this lane prices any Phase-0 unit. The nearest hour
   figures in `REFRESH:332-341` price other rows (Pathscope, release
   integration, baseline+install, operations, cutover, first start) and are
   already allocated by `WBD` to R02/R04/R29+R37/R41/R42/R44; the readiness
   record's 2–4 h baseline/install bundle is deliberately assigned to neither
   R29 nor R37 because it is inseparable (`WBD:68`, `WBD:180-183`), and it
   covers P1-01 baseline work, not P0-01 static facts.
4. Plan authority is contested. **Both formally articulated readings require
   these five tasks** (`PAR:122-124` cumulative; `PAR:144` KVM2-own-programme).
   The reading under which they would *not* be required — the 50-hour plan as
   sole governing chain — has **no supporting owner sentence anywhere found**
   (`PAR:11`, `PAR:86`). Detail in §2.

## 1. Phase-0 frame (from the governing documents)

- Phase 0 = "Governance and scope freeze"; hard predecessor **None**; phase
  close gate = "Owner lifecycle decision (P0-02); audit-model reconciliation
  (P0-03)" (`MASTER:243`). So of this lane's five tasks only **P0-03 is itself a
  named Phase-0 close gate**; P0-01/P0-04/P0-04A/P0-05 are required tasks within
  the phase, and P0-04 must be frozen **before Phase 1 begins**
  (`COMPANION:53`, `MASTER:399-403`).
- The phase also contains P0-01B (owner-controlled live-state verification) and
  P0-02 (owner lifecycle confirmation) (`COMPANION:28-37`). Those are **R28,
  an `OWNER` row, not part of R27** (`WBD:67`). Context only: D021 (2026-07-25)
  already records the owner selecting the bridge-first TESTNET → conditional lab
  → clean-host-fork lifecycle (`DEC:22`), which is the substance P0-02 asks for;
  whether it closes P0-02 is an owner/Lead call outside this lane.
- All Phase-0 tasks are `[AI: Any]` (P0-01, P0-03) or `[AI: Claude]` (P0-04,
  P0-04A, P0-05) per the companion task titles (`COMPANION:22,38,42,56,64`).
- Standing constraints that shape every row below: no task authorizes later
  actions and each operational gate needs distinct owner authority
  (`COMPANION:10-12`); the master grants no standing edit authority — every
  plan update needs task-specific owner write authorization (`MASTER:470`);
  read-only fact refresh is "not granted by plan alone" (`MASTER:471-472`).

## 2. Contested plan authority — what each reading implies for these five tasks

The conflict is real as a prerequisite-chain conflict; the 50-hour plan calls
itself the active delivery layer, the KVM2 family assigns detail to the
companion and grants no operational authority, and **no sentence in either
family supersedes the other** (`PAR:9-13`). No owner decision record found
resolves the precedence question (`PAR:11`), and the July 31 owner approval of
the 50-hour programme nowhere retires D021 or the KVM2 Phase 0–4 chain
(`PAR:86`). The owner decision list of 2026-08-15 night still names plan
authority as outstanding (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:129-131`).

| Reading | Are P0-01/03/04/04A/05 required? | Consequence for these tasks |
|---|---|---|
| **Cumulative (Scenario A)** — both plans' gates jointly mandatory (`PAR:118-138`) | **Yes.** Scenario A step 3: "After Gate A, close any still-open KVM2 Phase 0 facts/owner decisions…" (`PAR:124`) | R27 runs as early parallel preparation: wave 1 puts `R27 + R28` in parallel with Pathscope `R01 → R02` (`WBD:90-92`). Phase-0 close (needing R28's owner items) still precedes the KVM2 Phase-1/2 chain, and nothing host-side proceeds until both plans' joins. Risk named for this reading: false deduplication (`PAR:138`). |
| **KVM2 as its own programme (Scenario B)** — KVM2 family governs through Phase 4 (`PAR:140-156`) | **Yes.** Scenario B step 1 is exactly "Phase 0 P0-01, P0-01B, P0-02, P0-03, P0-04, P0-04A, and P0-05" (`PAR:144`); `WBD` Ordering B keeps the same rows (`WBD:117-118`) | These five tasks stop being "parallel preparation" beside the 50-hour chain and become the **front of the controlling chain**. The 50-hour §23a protections are then not prerequisites and cannot be silently imported (`PAR:152`). |
| **50-hour-plan-governs-alone (the unratified third reading)** — the practical position implied by the handoff labelling the 50-hour steps "the canonical sequence" (`PAR:13`, citing `GLOBAL_HANDOFF.md:607-623`) | **Not as gates.** The overlap map classes the P0/P1 governance units against 50-hour WP-0/WP-S/Gate A as **Genuinely different**: "WP-0 … does not close the KVM2 P0/P1 decisions" (`PAR:102`) | Under this reading the five tasks become optional governance hygiene of a preserved-but-not-executed programme. Two cautions: (a) no owner sentence supports this supersession (`PAR:11`, `PAR:86`) — adopting it is itself the outstanding owner decision; (b) it would drop the KVM2-specific gates these tasks feed (separate secret gate, ordered cutover, single-attempt first start — classed Genuinely different at `PAR:108-111`). Some products would remain load-bearing regardless: the evidence ledger, INDEX and roster discipline are already used by active non-KVM2 work. |

**Interim rule now in force** (until the owner ratifies one reading): only
already-authorized read-only repository analysis and non-gate-crossing local
preparation; no phase or gate may be claimed closed (`PAR:158-160`). This lane
operated inside that rule. Nothing below should be read as claiming any Phase-0
task closed.

## 3. Task-by-task

### 3.1 KVM2-P0-01 — Refresh static read-only OS and repo facts `[AI: Any]`

- **Definition:** `COMPANION:22-27`.
- **Artifact produced:** a dated, sanitized static inventory — OS/resource/
  firewall/service facts, clean release-SHA candidates, PR status — explicitly
  excluding live bridge state, TESTNET order/position, writer and ARM
  verification (those are P0-01B's scope) (`COMPANION:23-25`).
- **Does it exist?** **Absent as a P0-01 artifact; split status on its two
  halves.**
  - *Repo-side facts:* exist, refreshed and dated, but inside other records, not
    as a P0-01 deliverable: `DTL:29-47` (verified locally 2026-07-26: PR #25
    merged, base `423897b7…`, Windows runtime facts UNKNOWN);
    `REFRESH:38-58,82-102` (2026-08-15: accepted staging candidate `2ce41e34`
    not an ancestor of the current checkout; no accepted candidate for the
    current tree; release SHA UNVERIFIED/not frozen).
  - *OS-side facts:* **never refreshed.** The only OS snapshot is the historical
    2026-07-25 owner-supplied one (`DTL:8-27`; copied at `MASTER:104-119`),
    explicitly "not refreshed … because VPS access was not authorized" and "not
    current deployment evidence" (`DTL:10-11,25-27`). `INDEX:16` records
    "dated facts were not refreshed". The newest status doc confirms "no
    current KVM2 facts were collected" (`REFRESH:9-10`) and lists the whole
    2026-07-25 snapshot as UNVERIFIED (`REFRESH:353-357`). The master's
    re-verification rule stands: none of the dated facts may be reused without
    live read-only verification (`MASTER:121-122`).
  - Grep for `P0-01` across `MTC_COMMAND_CENTER` hits only the four planning
    documents — no execution or status record exists.
- **Acceptance condition (evidence + stop):** evidence per `COMPANION:23-25`;
  stop on any uncertainty, unexpected service, dirty source, or if a live
  control-endpoint access would be needed for a static fact
  (`COMPANION:26-27`).
- **Dependencies:** no hard predecessor (Phase 0, `MASTER:243`). Practical
  dependency for the OS half: **separately authorized read-only host access** —
  not granted by the plan alone (`MASTER:471-472`) and currently affirmatively
  excluded: D2's approved narrow grant covers `GATEA-STAGING` only and
  "explicitly still excluded … the Hostinger KVM2 production server"
  (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:54-60`). Repo-side facts can be
  refreshed locally at any time under existing read-only practice. Downstream:
  P1-01 baseline re-verification consumes current host facts, and Phase 1 is
  blocked until retention decisions exist (`INDEX:64-67`) — P0-01 feeds, and is
  fed by, that chain.
- **Estimate:** **NO SOURCED ESTIMATE.** What would produce one: (a) the
  repo-side half — time one bounded, frozen-command-list local refresh
  (git/PR/SHA fact capture) and record it; (b) the OS-side half — an owner
  read-only KVM2 access grant (not currently spendable, see D2) plus a timed
  bounded static-facts capture under a frozen command list. No timed execution
  of either half exists in any document this lane read.

### 3.2 KVM2-P0-03 — Reconcile the audit-model contract `[AI: Any]` — a Phase-0 close gate

- **Definition:** `COMPANION:38-41`.
- **Artifact produced:** a reconciliation showing one current roster copied from
  `AGENTS.md` into each future audit prompt, with the bridge task's older Opus
  wording no longer conflicting (`COMPANION:39-40`).
- **Does it exist?** **No dedicated P0-03 reconciliation artifact** (grep for
  `P0-03` across `MTC_COMMAND_CENTER`: only the four planning documents;
  `INDEX:13-23` tracks other gates but names no P0-03 row). Its **substance is
  largely already carried by the decision chain**, and one **live drift point**
  makes the reconciliation still necessary:
  - The canonical roster exists and is current in structure: exact
    `claude-opus-5` (`AGENTS.md:56-57`), exact `gpt-5.6-sol` (`AGENTS.md:65-66`),
    GLM-5.2 as owner-authorized auditor 4 (`AGENTS.md:78-80`), with binding
    execution/finding/verdict rules (`AGENTS.md:89-91`) and the tier policy
    controlling slots/effort/cadence (`AGENTS.md:35-37,46`; D028 at `DEC:3`).
  - The older-Opus-wording conflict was resolved by owner decisions: D022
    upgraded the Claude auditor to exact `claude-opus-5`/`xhigh` and superseded
    the D020 model clause (`DEC:20`); D024 states that for all future KVM2
    Gate 5/Gate 6 work the current `AGENTS.md` roster "governs and supersedes
    conflicting older KVM2 policy text" (`DEC:11`); D025 expanded the roster
    for audit authority only (`DEC:9`).
  - In the documents this lane read, no live conflicting Opus wording remains:
    the bridge task's item 10 now requires the audit "under the current
    owner-authorized roster" (`DTL:157-158`), and the companion's own audit
    gates name exact `claude-opus-5`/`xhigh` consistent with `AGENTS.md`
    (e.g. `COMPANION:239-240`).
  - **Live drift:** `AGENTS.md:78-80` still names **GLM-5.2** as canonical
    auditor 4, while `ROUTING:115-117` records **GLM-5.3** as "live and
    selectable (probed 2026-08-15)" with an owner routing note (added at commit
    `47c54122`, 2026-08-15 21:43 +03). Whether auditor-slot 4 identity must be
    re-reconciled is exactly the class of question P0-03 exists to settle;
    `ROUTING:119-123` itself preserves the constraint that GLM verdicts stay
    supplemental on anything requiring a run.
  - **UNKNOWN:** whether every *future audit prompt* already embeds the roster
    copy. Verifying that requires enumerating the audit-prompt population,
    which this lane did not do. What would settle it: a sweep of all
    KVM2/bridge audit-prompt artifacts against the current `AGENTS.md` roster
    block.
- **Acceptance condition (evidence + stop):** one current roster in each future
  audit prompt; older Opus wording non-conflicting (`COMPANION:39-40`); stop if
  model/effort requirements disagree across authoritative documents
  (`COMPANION:41`).
- **Dependencies:** no hard predecessor; it is one of the two named Phase-0
  close gates (`MASTER:243`). Inputs exist (`AGENTS.md` roster; `DEC`
  D022/D024/D025/D028). Producing the reconciliation record in the governing
  documents would itself need task-specific write authorization
  (`MASTER:470`).
- **Estimate:** **NO SOURCED ESTIMATE.** What would produce one: freeze the
  write/validation contract (which documents and which audit-prompt artifacts
  are in scope, what the reconciliation record must contain, how the
  GLM-5.2/5.3 drift is dispositioned), then time one authoring+sweep pass. No
  timed execution exists in any document read.

### 3.3 KVM2-P0-04 — Freeze artifact layout and raw-evidence retention policy `[AI: Claude]`

- **Definition:** `COMPANION:42-56` (title :42; evidence :43-53; stop :54-56).
- **Artifact produced:** the planned artifact layout (root
  `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/` plus the exact path list) and the
  raw-evidence **retention/deletion policy (owner, duration, trigger, Stop)**
  frozen **in both governing documents** — design only, no directories created
  (`COMPANION:43-53`; mirrored at `MASTER:375-405`).
- **Does it exist?** **Half exists.**
  - *Layout half:* **frozen in both governing documents.** The identical root
    and path list appears in the companion (`COMPANION:44-50`) and the master
    (`MASTER:380-397`), with the freeze attributed to P0-04 and required before
    Phase 1 (`MASTER:399-405`). Two ledger-row-type/sanitization rules the
    policy requires are also frozen (`MASTER:583-608`).
  - *Retention-policy half:* **absent.** `INDEX:64-67` records "The retention
    owner, retention duration, deletion trigger, and encrypted storage
    selection are **OPEN owner decisions**. Until all four are recorded, Phase 1
    raw evidence collection is blocked." The master still carries the
    requirement as unfilled: "Define raw evidence retention duration and
    deletion policy before Phase 1 begins" (`MASTER:635-636`). No document read
    by this lane records any of the four fields.
- **Acceptance condition (evidence + stop):** evidence per `COMPANION:43-53`;
  stop if a path overlaps protected trading/Pine/parity/schema scope, raw
  evidence or a private identifier would be committed, the retention/deletion
  policy is absent, or Phase 1 begins before the freeze (`COMPANION:54-56`).
  No stop condition is violated today: Phase 1 is OPEN/BLOCKED
  (`INDEX:16`; `DTL:25-27`).
- **Dependencies:** owner decisions on the four retention fields; then
  separately authorized edits to **both** governing documents (no standing edit
  authority — `MASTER:470`; D024's write grant was task-specific and exhausted,
  `DEC:11`). Must precede Phase 1 (`COMPANION:53`) and gates P0-04A-style
  execution (`LEDGER:1` lists `KVM2-P0-04` as the prerequisite of the
  P0-04A-PREP row).
- **Estimate:** **NO SOURCED ESTIMATE.** The remaining work is owner-decision
  gathering plus a bounded two-document edit; no source prices either. What
  would produce one: record the four owner decisions, freeze the exact edit
  contract (the sentences to be added to master and companion), and time one
  authorized edit+verify pass.

### 3.4 KVM2-P0-04A — Create and validate artifact index and ledger `[AI: Claude]`

- **Definition:** `COMPANION:56-63` (title :56; evidence :57-60; stop :61-63).
- **Artifact produced:** under separate owner write authorization — `INDEX.md`
  and `evidence/EVIDENCE_LEDGER.jsonl` with a validated schema, fixture rows
  for publishable-only / restricted-only / mixed row types, and rejection tests
  for private paths, public IPs, hostnames, credentials (`COMPANION:57-60`).
- **Does it exist?** **Yes — created, committed, not independently verified.**
  All named artifacts exist in the committed tree (creation commit `6fe0130f`,
  2026-07-26; no later commit touches them):
  `INDEX.md`; `evidence/EVIDENCE_LEDGER.jsonl`; `evidence/ledger_schema.json`;
  `evidence/validate_ledger.py`; fixtures `valid_publishable_only.jsonl`,
  `valid_restricted_only.jsonl`, `valid_mixed.jsonl`,
  `invalid_case_definitions.json` (paths listed at `INDEX:40`; verified by
  direct glob). Validation/rejection coverage exists as claimed:
  `test_canonical_ledger_and_all_three_row_fixtures_validate`
  (`IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py:407-417`),
  `test_ledger_rejects_all_declared_synthetic_invalid_cases` covering
  private-path/hostname/credential and declared invalid cases
  (`IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py:419-448`), and
  `test_program_tree_has_no_private_host_ip_user_or_key_path`
  (`IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py:456`); the local
  validation command is recorded at `INDEX:69-73`, fixture coverage summarized
  at `INDEX:75-78`.
  **State of acceptance:** the ledger contains a single row,
  `KVM2-P0-04A-PREP`, verdict **OPEN** — "Prepared locally; independent
  verification pending" (`LEDGER:1`); `INDEX:15` records "P0 artifact structure
  and sanitized ledger — PREPARED LOCALLY — Independent verification remains
  open"; `READY:5` records "Independent audit verdict: NONE / OPEN", builder
  self-QA only (`READY:3-4,26-27`).
  **Authorization provenance:** the ledger row's authorizer is "Owner batch
  authorization 2026-07-26" (`LEDGER:1`). The same-dated owner implementer
  waiver/authorization for that batch is recorded in
  `DTL:49-56` and `READY:10-16`, but **no D-numbered decision in `DEC` covers
  creation of the `KVM2_PROGRAM` tree** (D024's enumerated scope is the master,
  companion, audit prompt, banner and the decision record — `DEC:11`). The raw
  owner sentence for the batch write authorization was **not located** in the
  documents this lane read; `UNKNOWN`. What would settle it: the 2026-07-26
  owner prompt/record for the "first executable preparation batch" (`DTL:4`),
  or an owner confirmation that the ledger row's authorizer field is accurate.
- **Acceptance condition (evidence + stop):** separate write authorization
  received; artifacts created with validated schema; all three fixture row
  types; rejection tests (`COMPANION:57-60`); stop if created without write
  authorization, any fixture row accepts a private path/public IP/hostname/
  credential, any row type untested, or the schema does not enforce the three
  row types (`COMPANION:61-63`). Mechanical coverage exists (tests above);
  independent verification does not.
- **Dependencies:** P0-04 (`LEDGER:1` prerequisite field; layout frozen,
  §3.3); separate owner write authorization (claimed, provenance partly
  UNKNOWN, above); an independent verifier distinct from the builder session,
  since the implementer "cannot accept its own work" (`DTL:58-60`;
  `READY:18-19`).
- **Estimate:** **NO SOURCED ESTIMATE.** The creation work is already spent
  (2026-07-26, unbilled/disjoint timing not recorded anywhere read); the
  remaining work is a named independent verification run. What would produce
  one: name the verifier, freeze the verification contract (validator run
  against ledger+fixtures+schema, the three rejection-test groups, and the
  tree-scan), and time that single execution. No timed verification exists yet.

### 3.5 KVM2-P0-05 — Source-scenario reconciliation `[AI: Claude]`

- **Definition:** `COMPANION:64-74` (title :64; evidence :65-71; stop :72-74).
- **Artifact produced:** under separate write authorization,
  `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/SOURCE_SCENARIO_RECONCILIATION.md`
  containing the external source report's SHA-256 (no private path),
  deterministic scenario IDs (heading-slug + local number + normalized title +
  source-line span), every normative set enumerated, a zero-unmapped-ID proof
  per set, each item mapped Required/Allowed-later/Deferred/Forbidden with
  section/rationale/conflict note, and the advisory-only statement with
  precedence (plan + bridge list govern; source report advisory)
  (`COMPANION:65-71`).
- **Does it exist?** **The path exists as an explicit BLOCKED/PLACEHOLDER; the
  artifact does not exist.** `SSR:3-5` declares "Status: **BLOCKED /
  PLACEHOLDER**"; the external scenario source "was not supplied or available
  in this authorized local batch", so no mapping is invented (`SSR:7-14`); the
  recorded result is "UNAVAILABLE SOURCE / ZERO CLAIMED MAPPINGS / P0-05 OPEN"
  (`SSR:24-25`). The external source report itself is **absent from the
  repository** — nothing in the documents read identifies it beyond "the
  external scenario source referenced by KVM2-P0-05". The master's "not yet
  created" sentence at `MASTER:568-569` is therefore stale as to the file's
  existence but accurate as to the artifact: a placeholder is not the
  reconciliation. (Staleness class already disclosed at `INDEX:30-34`.)
- **Acceptance condition (evidence + stop):** evidence per `COMPANION:65-71`;
  stop if created without write authorization, source SHA-256 absent, private
  path present, any normative set unenumerated, any item unmapped,
  zero-unmapped-ID check absent, or advisory status/precedence absent
  (`COMPANION:72-74`). Note the deterministic-ID and full-enumeration
  requirements originate from the Cycle-2 audit repair set ("deterministically
  enumerate the source-scenario reconciliation"), recorded in
  `GLOBAL_HANDOFF.md:2756-2761`.
- **Dependencies:** (a) the owner supplying the external scenario source
  document — currently absent, UNKNOWN identity/content; (b) separate write
  authorization for the real artifact (`COMPANION:65`; `SSR:13-14`); (c) no
  other technical predecessor.
- **Estimate:** **NO SOURCED ESTIMATE.** The work's size is a direct function
  of the source's scenario count, which is UNKNOWN while the source is absent.
  What would produce one: owner supplies the source under separate
  authorization; freeze the enumeration/ID/mapping procedure; time one full
  pass including the mechanical zero-unmapped-ID check.

## 4. Row-level conclusion for R27

- `WBD:66` defines R27 as exactly these five tasks and prices it **NO SOURCED
  ESTIMATE** with the instruction to "Estimate each artifact after its
  write/validation contract is frozen." This lane's findings **confirm that
  classification** and refine it per task (§3): no sourced range exists for any
  of the five; three tasks have concrete, frozen next contracts whose timing
  would produce prices (P0-04A verification; P0-03 reconciliation sweep; P0-04
  retention-policy edit), while two are blocked on absent inputs (P0-01 OS-half
  on a not-yet-spendable host grant; P0-05 on an absent external source).
- Existence findings the Lead can reuse: P0-04 layout frozen in both governing
  docs; P0-04A artifacts committed at `6fe0130f` with verdict OPEN; P0-05
  placeholder committed with zero claimed mappings; P0-01 and P0-03 unexecuted
  as defined; live roster drift GLM-5.2 (`AGENTS.md:78-80`) vs GLM-5.3
  (`ROUTING:115-117`) outstanding.
- Two stale-text items in the governing documents materially affect any
  Phase-0 close claim and should ride the next authorized plan-maintenance
  pass: the master's "not yet created" sentence (`MASTER:568-569`) and the
  Phase-3 blocker sentence (`MASTER:256-261`, stale per `PAR:74` and
  `INDEX:25-34`).

## 5. Boundary statement

This lane performed repository reads and read-only Git only. No host, network,
SSH, deployment, service, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, or economic
action was performed or authorized by this document. No gate, task, phase, or
plan-authority reading was decided; every verdict-shaped statement above is a
report of what existing documents record. No sub-delegation occurred.
