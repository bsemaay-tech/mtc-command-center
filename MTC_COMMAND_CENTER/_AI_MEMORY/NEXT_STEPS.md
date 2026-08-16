# NEXT_STEPS

> **Rotation policy (2026-08-15):** entries dated before 2026-08-01 are in
> `archive/NEXT_STEPS_pre-2026-08-01.md`. Grep the archive before claiming an entry does
> not exist. When this live file exceeds ~2500 lines, rotate again.

## OWNER-REQUESTED BLOCKED — Gemini 3.7 Flash Pro read-only repo route (2026-08-16)

**Execution tier: T0.** The owner explicitly directed Codex to perform the implementation
instead of waiting for Claude. Installation, authentication, live completion, dedicated
project isolation, launcher implementation, preflight, canonical repo read, and denied-write
probe are complete. Repo authorization is blocked after the final permitted Codex audit returned
`REQUEST_CHANGES`; Claude Max remains emergency-only and was not used.

1. **T0 cap exhausted.** Literal commands and outputs are in
   `11_TRIAGE/GEMINI_PRO_READ_ONLY_ROUTE_QA_2026-08-16.md`. Codex rounds 1 and 2 returned
   BLOCK; round 3 returned `REQUEST_CHANGES`. The final response did not enumerate its repair,
   although its transcript investigated watcher final-drain and `USERPROFILE` path-binding risks.
2. **[AI: Barış] Decision required before any continuation.** Do not silently run round 4.
   The owner may authorize a new bounded diagnosis/repair cycle or leave the installed route
   outside repo governance. Fresh accepting `gpt-5.6-sol` xhigh and `claude-opus-5` xhigh
   reviews are still required before this route can be called repo-ready.
3. **Scope remains narrow.** Do not alter shared legacy Antigravity permission storage,
   protected source, trading/Pine/parity/MTC behavior, schemas, credentials, hosts, or deploys.

## OWNER-REQUESTED OPEN — AI-memory continuity audit and repair (2026-08-16)

**Registration tier: T3** (documentation / audit planning only). Future audit or repair work
must be separately tier-classified against the actual surfaces touched at execution time.

1. **[AI: Any] Read-only continuity audit.** Before calling any work missing: read canonical
   onboarding/memory against all refs and registered worktrees. Reverify snapshots; specifically
   inspect root-gap commit `cac12b94` and the six owner-decision commit `c84497c8` to confirm
   current state is reachable from canonical onboarding.

2. **[AI: Any] Route distinction.** GATEA-STAGING (the Hyper-V VM) and the ordinary `gatea`
   SSH route are recorded. The later privileged read-only / root-channel design (`RPD-VERIFY`,
   grants #3/#6) was not established as a standing channel. Never call the VM forgotten; the
   gap is in the privileged-channel design, not in VM existence.

3. **[AI: Claude] Worktree and branch inventory + risk report.** Re-count and re-classify all
   registered worktrees and detached HEADs first (last snapshot: 152 worktrees / 85 detached —
   reverify at execution). Produce a compact evidence-backed risk report covering: long-horizon
   coding drift, audit surface coverage, external infrastructure lifecycle, branch/worktree
   propagation, and canonical propagation gaps. No deletion, move, prune, stage, or cleanup
   without separate owner approval.

4. **[AI: Claude] Canonical reconciliation proposal.** After Lead verification: reconcile
   accepted current facts and decisions into canonical `_AI_MEMORY`. Propose one canonical
   secret-safe infrastructure-metadata registry with enforceable write-back and
   branch-visibility checks. Never guess or silently fill an UNKNOWN value; resolve it
   only from independently verified evidence.

5. **Acceptance criteria.** A fresh session finds current state through canonical onboarding
   alone; no authoritative latest decision is stranded only on another ref or temp output;
   infrastructure metadata shows purpose, lifecycle, provenance, current authority-status, and
   secret-safe access metadata; conflicts and staleness are explicit; all refs and worktrees
   are reverified at execution time.

6. **Safety fence.** Audit read-only first. This registration authorizes no host, network, or
   credential access; no trading, Pine, parity, or MTC source change; no repo cleanup,
   worktree or branch deletion, or history rewrite. All existing hard gates remain unchanged.

## READ FIRST — fresh-session handoff (2026-08-10 evening)

**`11_TRIAGE/NEW_SESSION_KICKOFF_2026-08-10_EVENING.md` is self-contained and current.**
It carries owner grants #1–#7, the binding routing policy (Max emergency-only; Claude Pro
fills the T0 Claude flagship slot; Codex Pro `-Account fourth`; parallel dispatch and tier
classification mandatory), per-artifact state with exact hashes, the six freeze-gate pins,
the open items, and the traps that cost time today. Everything below is background.

**Immediate pick-up, in order:**

1. **[AI: Lead]** Dispatch RP6-P0 round 7 — implementer must NOT be Codex (GLM or Claude
   Pro). Scope = the five required corrections in `RP6_CODEX_AUDIT_R6_2026-08-10.md`,
   spelled out in the handoff file's RP6 section: `builtin type -t` so an overridden
   `type` cannot forge the prerequisite check; disable pathname expansion around the
   OUTER pin parse before the first split; adjudicate producer SHAPE before any rc-1
   object verdict in `p0_probe_kind` and `p0_assert_venv_root`; narrow five printed
   claims to what is established; and replace ALL fence line ranges with anchored
   markers, repair the R4 fence so it closes its descendants, then re-run every command
   from a clean Git Bash. Also fix the stale retracted-`-S` claim at
   `RP6_REPAIR_R4_REPORT.md:88` (left out of round 6's allowlist).
2. **[AI: Lead]** Transport round 4 — NOT started. Kickoff ready at
   `WPI_BLOCKS_DRAFT/KICKOFF_TRANSPORT_REPAIR_R4.md` with the F4 Lead adjudication
   (per-branch prerequisites, Codex prevails). GLM hit its window mid-run; its partial
   edits were restored to the committed blobs and verified byte-identical, so the round is
   un-started, not half-done.
3. **[AI: flagships]** RP7 final pair on `23e55667…` — the only artifact ready for its
   acceptance audits right now. Kickoff:
   `WPI_BLOCKS_DRAFT/KICKOFF_CODEX_T0_AUDIT_RP7_FINAL.md`.
4. **[AI: Any]** §10.1 allowlist reconciliation against the new prover's output, and the
   prover's own T1 audit.
5. **[AI: Lead]** Successor preregistration from the skeleton → Stage 1 freeze → host
   execution under grants #1/#2/#3/#6 → WP-I closure → Audit 2.

**Owner ask (plain language):** today's work booked ~4.4 hours of the 50-hour plan,
bringing it to ~29.3 used and ~20.7 left. That figure is an estimate made at the time, as
the rules require — please confirm it looks right, or adjust it.

## PERMANENT AUDIT TIERS — apply immediately to active RP7/WP-I work (2026-08-10)

**[AI: Claude Lead]** Re-read `AGENTS.md` §AUDIT TIER POLICY — PERMANENT DEFAULT and record the
current Gate-1 tier before the next audit dispatch. `RP7-WPI-RO.sh` is T0 because it is a run-kit script
intended for staging-host execution: two fresh flagships (`claude-opus-5` + `gpt-5.6-sol`) at xhigh,
maximum three rounds. Count the existing Claude audit only if fresh-session + xhigh launch evidence is
confirmed; its report currently omits effort. After repair/green evidence, run the fresh Codex xhigh slot.
Do not add GLM/DeepSeek unless an explicit tier slot or later owner contract requires it.

## WP-I: venv site-startup security hole found + closed in BOTH blocks (2026-08-10 ~18:30)

**The headline of the day.** The Codex flagship slot found, independently in RP7 and then
RP6-P0, that the blocks used the very venv they were auditing as the interpreter that
produces their verdict — and `python -I` does NOT disable `site`, so a `.pth` or
`sitecustomize.py` in that venv executes arbitrary `gatea`-authority code before the
check runs. A tampered candidate could forge the exact accepted PASS line and mutate the
host while the block reported clean. Executed proof both ways in both blocks. Three
Claude flagship rounds had missed it in each — this is the two-flagship T0 contract
paying for itself, and the single strongest argument in the repo for keeping it.

Owner authorized exceeding the T0 3-round cap for this class (RP7 explicitly; the Lead
extended it to RP6-P0 on the identical finding and logged it).

State (all committed + pushed):

- **RP7-WPI-RO** — round 4 done, `d6a976aa`, bytes `23e55667…`, 70941 B. Both
  adjudicators moved onto a pinned system interpreter under `-I -S` that refuses to emit
  a result unless isolation actually holds; `python3` is the 10th bound tool + 21st
  projection point. Also: row-22 two-phase parse (both auditor orderings STOP), one
  enforced metadata-discovery universe (`ghost.egg-info` now STOPs), preregistered B5/B6
  order verified against frozen code at runtime, row-specific tokens. Needs its FINAL
  flagship pair on these bytes.
- **RP6-P0** — Claude flagship ACCEPTED at round 3 (`PASS-WITH-NITS`, `209babca`); Codex
  flagship BLOCK 4 on the same bytes (`4f58e650`): same venv hole (F1), unbounded row-9
  `systemctl` (F2), stale RO tool inventory that rejects RP7's pin set (F3), getent
  divergence grammar (F4). **Round 4 IN FLIGHT**, gated on and pointed at RP7's frozen
  10-tool set.
- **Transport set** — round 2 closed all 16 findings from both flagships (`9ef4437d`,
  incl. the `$Matches` clobber that meant ops 11/12 could never bind). Claude re-audit
  `REQUEST_CHANGES 1` (`8ab686dd`): an rc outside `{0,1,3}` — ssh transport failure, dead
  host, rejected key — is recorded as completed deviant state, so `TR_RUN FAIL` accuses
  the host after the one-use RUNIDs burn. Codex re-audit IN FLIGHT; ONE combined round 3
  will close both lists.
- **Prereg** — skeleton ready (`WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_SKELETON_2026-08-10.md`),
  owner grant #6 chose attestation option (a). Freeze-gate pins now enumerated: projection-v2
  digest over 21 points, `WPI_FIXED_TRUSTED_PYTHON` (resolved non-symlink path), row-8
  execution-domain attestation literals.
- **Routing** — Codex `secondary` exhausted until 2026-08-16 → use `-Account fourth`.
  Claude Pro default hit its 5h window mid-day. Max carried the surge. NVIDIA NIM via the
  claude-CLI wrapper narrates but does NOT engage file-write tools — read/analysis only.
- **Windows trap (matters at freeze):** never `git checkout` these block files — autocrlf
  rewrites them to CRLF and breaks the frozen hash. Restore with
  `git cat-file blob HEAD:<path> > <path>`.

**PICK UP EXACTLY HERE:**

1. **[AI: Lead]** Consume RP6 R4 + Codex transport re-audit; dispatch ONE combined
   transport round 3.
2. **[AI: flagships]** Final flagship pairs on final bytes: RP7 (`23e55667…`), RP6-P0
   (post-R4), transport (post-R3). Both slots xhigh, fresh.
3. **[AI: Lead]** Successor prereg from the skeleton: mint RUNIDs, fill all pins, Stage 1
   freeze (incl. §10.2 parsed path-scope proof — the prover tool is still unwritten and
   is the one piece of freeze tooling missing), commit BEFORE any invocation.
4. **[AI: Lead]** Execute P0 → RO on GATEA-STAGING (grants #1/#2), attestation command set
   + RPD-VERIFY as root (grants #3/#6). Evidence closed + bound.
5. **[AI: Any]** WP-I closure record → Audit 2.

## WP-I block set built + in adversarial T0 cycles; re-audits in flight (2026-08-10 ~13:30)

Day session progress (committed + pushed through `f503af55`). Tier classification for the
whole WP-I block set recorded per the policy above:
`11_TRIAGE/WPI_BLOCKS_DRAFT/AUDIT_TIER_CLASSIFICATION_2026-08-10.md` — all executable
transport/block artifacts are **T0** (two fresh flagships xhigh acceptance floor).

- **Draft at round 1.6.** 1.4 catalogue pass (17 repairs, GLM VERIFIED-CLOSED at
  `6a8b0896`); 1.5 transport-contract repair after a correct Codex authoring STOP (two
  reused remote scripts carried WP-L-specific constants → `remote_setup_wpi.sh` /
  `remote_extract_verify_wpi.sh` minimal derivations, `6f929112`); 1.6 RP7-audit
  adjudications (row 19a verifier identity, row-21 STOP/FAIL split, non-symlink
  interpreter, normalised mount projection v1, WPI_LOG_DIR pinned literal, `f503af55`).
- **RP6-P0** through C13 rounds (GLM getent arm → Lead-executed QA `cbaf3ec8` → Codex
  audit BLOCK 3 `4e3ab2c1` → Claude Pro repair `8d2f25a5`). Current `ef205e20…`,
  55467 B. Codex cycle re-audit IN FLIGHT; both T0 xhigh flagship slots still to run on
  final bytes.
- **RP7-WPI-RO** round 1 (Codex, `3c929a3a`) → Claude Pro xhigh audit BLOCK 13
  (`ee21369a`; F1: argv[0] prefix killed every *_absent FAIL) → Codex round-2 repair of
  all 13 (`f503af55`). Current `ed9aa6b3…`, 54001 B. Claude Pro xhigh re-audit IN
  FLIGHT; Codex xhigh T0 slot on green bytes next.
- **Transport set** authored round 2 (8 files, `3c929a3a`). No audit yet — first audit
  at the T0 contract.
- **Routing:** GLM hit its 5h window (~19:56 reset); Claude Pro (default account,
  owner-verified) is auditor 2 / relief implementer. NVIDIA NIM live
  (`Invoke-NvidiaNim.ps1`, deepseek/minimax).

**PICK UP EXACTLY HERE:**

1. **[AI: Lead]** Consume both in-flight re-audits. On green: dispatch the missing T0
   xhigh flagship slots (Codex xhigh for RP7; opus-5 xhigh + Codex xhigh for RP6-P0
   final bytes). On narrow BLOCK: bounded rounds within the T0 cap of 3.
2. **[AI: flagships]** Transport-set T0 audit (both flagships xhigh).
3. **[AI: Lead]** Successor preregistration: mint RUNIDs + unit id, fill pins
   (LEAD_PIN_RESOLUTION + empty-dropin-set + mount-projection-v1 attestation digest),
   Stage 1 freeze incl. §10.2 parsed path-scope proof, commit BEFORE any invocation.
4. **[AI: Lead]** Execute P0 → RO on GATEA-STAGING (owner grants #1/#2), then
   RPD-VERIFY as root (grant #3). Evidence closed + bound.
5. **[AI: Any]** WP-I closure record → Audit 2 dispatch.

## WP-I round 1.4: catalogue pass CLOSED; RP6-P0 repair in flight (2026-08-10 ~09:20)

**Round 1.4 committed `6a8b0896`:** Codex applied all 10 defect patterns to the whole
accepted WP-I draft — 17 findings repaired, 0 patterns clean. GLM independently verified
**VERIFIED-CLOSED** (V1–V6 all PASS, 4/4 sample-attacks stopped). Pins untouched. Lead
pre-resolved both pins in `WPI_PREREG_DRAFT_ROUND1/LEAD_PIN_RESOLUTION_2026-08-10.md`:
R1 = full unit-fragment SHA `538c1c60…279bd`; R2 = `WPI_LOG_DIR=/var/log/mtc-bridge`
(source-derived from the candidate's unit template, non-circular). GLM advisory (LOW):
pin the drop-in allowlist as a third PIN item at finalization — install.sh at the
candidate creates no drop-ins, so the source-derived expectation is an EMPTY drop-in set.

**RP6-P0 repair dispatched to Codex** (F1/F3/F4 per `WPI_BLOCKS_DRAFT/
LEAD_ADJUDICATION_RP6_2026-08-10.md`; F2 closed; draft-side Pattern 8 already fixed by
round 1.4 C13/C14). GLM re-audit follows, then commit.

**PICK UP EXACTLY HERE — remaining order:**

1. **[AI: GLM]** Re-audit repaired RP6-P0 + SELF_QA_RP6; on PASS commit.
2. **[AI: Codex]** Author RP7-WPI-RO.sh + run_p0.sh + run_ro.sh + transport_runner.ps1 +
   TRANSPORT_PLAN.tsv per draft round 1.4 (section 4 acceptance rules). GLM/Codex
   adversarial rounds until PASS.
3. **[AI: Claude Lead]** Successor preregistration: allocate RUNIDs (`rp0_require_safe_component`
   transcript in self-QA), fill pins from LEAD_PIN_RESOLUTION + empty drop-in set pin,
   Stage 1 freeze (path-scope proof per round-1.4 §10.2 — parsed closed-set expansion,
   not literal scan), commit BEFORE any invocation.
4. **[AI: Claude Lead]** Execute WP-I: P0 stage → RO stage on GATEA-STAGING (owner grants
   #1/#2), then RPD-VERIFY as root (grant #3). Evidence closed + bound.
5. **[AI: Any]** Close WP-I with evidence → dispatch Audit 2 (readiness package at
   `11_TRIAGE/AUDIT2_READINESS_PACKAGE/`).

## ALL FOUR OWNER GATES GRANTED — WP-I is the active workstream (2026-08-10 morning)

Barış granted, and asked not to be asked again (recorded in
`11_TRIAGE/NEW_SESSION_KICKOFF_PROMPT_2026-08-09_NIGHT.md`, top section):
**WP-I host-contact authority**, **WP-I budget lift**, **root on the staging host for
`RPD-VERIFY`** (read-only block; root to run it, NOT blanket mutation authority), and the
**retroactive defect-catalogue pass** over the accepted WP-I draft. RP6-P0 repair waits
until the WP-I direction settles.

Ledger: **24.9 h used / 25.1 h remaining** (`11_TRIAGE/LEDGER_STATUS_2026-08-10.md`).

**PICK UP EXACTLY HERE — in this order:**

1. **[AI: Codex]** Retroactive catalogue pass over the accepted WP-I draft. A known
   instance is already found: the identity row specifies a name-based check (Pattern 8) —
   repair the draft, not the block. Sweep for the other nine patterns too.
2. **[AI: Claude Lead]** Finalize the WP-I preregistration: allocate identifiers, fill
   every `<PIN-BEFORE-DISPATCH>` from its cited record, run Stage 1 freeze. Commit the
   preregistration BEFORE any invocation.
3. **[AI: Claude Lead]** Execute WP-I read-only scope, then run `RPD-VERIFY` as root —
   this closes the three checks B3 defers and the long-open `bridge.env` naming question.
4. **[AI: Any]** Close WP-I with evidence, then dispatch Audit 2 (readiness package is
   already assembled at `11_TRIAGE/AUDIT2_READINESS_PACKAGE/`).
5. **[AI: Any]** RP6-P0 repair, scope in `WPI_BLOCKS_DRAFT/LEAD_ADJUDICATION_RP6_2026-08-10.md`.

Still hard-gated: credentials, ARM, orders, broker/exchange, TESTNET/mainnet, master merge,
WP-V/KVM2, payload-archive deletion, host reprovisioning, service-state mutation.

## WP-L P2 UNIT CLOSED + WP-I draft audit-clean (2026-08-10 overnight)

**WP-L P2 unit closed** (`6370e1fe`): `UNIT_CLOSURE_RECORD.md` + `EVIDENCE_INDEX.md` over all
nine stage dirs, four-RUNID ledger. Both checks ever authorized to run (R4-5, repaired B3)
ran and PASSED on the real host. Booked 2.6 h → ~26.9 h remaining.

**WP-I draft is audit-clean** at round 1.3 (`fe8f1b11`, verified `2f5523c9`): Max authored →
GLM reviewed → Codex audited (6 findings) → GLM repaired F1/F2/F5/F6 → Codex repaired F3/F4 →
GLM independently verified both CLOSED with no regression.

**PICK UP EXACTLY HERE:**

- **[AI: Barış]** WP-I is NOT dispatchable and needs TWO things only you can give: explicit
  written host-contact authority for the WP-I unit, and a budget lift (the 50 h balance is
  recorded NOT REPRODUCIBLE). Until both exist, no WP-I host execution may be planned or run.
- **[AI: Barış]** `RPD-VERIFY.sh` is accepted and sits in the kit but has NEVER executed — it
  is root-side and no root/sudo was granted. It holds the three checks B3 defers, including
  the unresolved `bridge.env` naming risk. Opening a privileged channel is your call.
- **[AI: Any]** Next natural unit is Audit 2 per the v2 checklist (`AUDIT2_EVIDENCE_CHECKLIST_DRAFT_2026-08-09.md`),
  which now has the §2b transport-evidence package. Its dispatcher must resolve the GLM
  supplemental-vs-omitted flag.
- **[AI: Any]** Routing is Codex-first, Max last resort (`STANDING_AUTONOMY_AUTHORITY` §A2).

## WP-L P2 — repaired B3 PASSED ON THE HOST; B3-GAP-ENV CLOSED (2026-08-09 night)

**The gap is closed end to end.** Owner authorized host execution in-session; a new
preregistration (`08_PREREG_B3B/`, unit `WPLP2B-20260809T210610Z-834380c5`) was committed at
`bf395dab` BEFORE any invocation, then Stage 3B-B3B ran: **TR_RUN PASS, 7/7 ops rc=0, `B3 PASS`**
(`09_TRANSPORT_B3B/`, commit `b3682bd5`). Re-frozen kit `runkit_b.tar` `888bec17…` verified
remotely (10/10 blocks). Evidence closed, retrieved, digest-set bound.

Numeric service identity resolved without circularity: `install.sh` allocates the account
dynamically, so the NAME is the contract — a recorded `getent` preflight probe gave uid **999**,
gid **988** (they differ). B3 proves the state/log dirs belong to the account systemd runs.

**PICK UP EXACTLY HERE:**

- **[AI: Claude Lead]** Write the WP-L P2 unit closure record (Stage 1→3B, repair cycle rounds
  1–6 + audits 1–6, re-freeze, B3B execution) and close the unit.
- **[AI: Any]** `RPD-VERIFY.sh` is accepted and travels in the kit but has NEVER executed — it is
  root-side. Running it needs root on the host, which is NOT granted. Treat as design-only until
  the owner opens a privileged channel.
- **[AI: Any]** WP-I draft is at round 1.2 (Codex audit applied by GLM). F3/F4 (system-manager
  access) remain OPEN for a successor round. WP-I is NOT dispatchable: it still needs explicit
  host-contact authority and a budget lift.
- **[AI: Any]** Routing is now Codex-first, Max last resort (`STANDING_AUTONOMY_AUTHORITY` §A2).

## WP-L P2 — B3 repair ACCEPTED (audit 6 PASS); Stage 1B re-freeze in flight (2026-08-09 night)

State: R4-5 CLOSED on Linux (banked, bound). **B3-GAP-ENV Option 1 repair cycle ACCEPTED at round 6**
(audit 6 PASS, zero findings — auditor paste-and-ran the QA blocks verbatim and all reproduced).
Repaired `RP1-B3.sh` `6f3ea022…` + new root-side `RPD-VERIFY.sh` `3b9e78e8…` are the accepted artifacts
(`06_B3_REPAIR/round6/`). WP-I draft is at round 1.1 (GLM review integrated). Standing autonomy authority
active (`11_TRIAGE/STANDING_AUTONOMY_AUTHORITY_2026-08-09.md`). Paste-ready continuation prompt:
`11_TRIAGE/NEW_SESSION_KICKOFF_PROMPT_2026-08-09_NIGHT.md`.

**PICK UP EXACTLY HERE:**

- **[AI: Claude Lead]** Consume the Stage 1B re-freeze build (Max, `07_RUNKIT_B/`) → verify ten block
  identities + two provenance classes + deterministic archive → commit.
- **[AI: Claude Lead]** Write the WP-L P2 unit closure record (Stage 1→3B + repair cycle + re-freeze).
- **[AI: Claude Lead]** NOTE: the Stage 2/3 preregistration is VOID for the new kit (block hashes and
  archive digest changed). Transporting or running the repaired B3 on the host needs a NEW
  preregistration AND a fresh owner authorization — host execution stays owner-gated.
- **[AI: Any]** Morning summary ~06:30 + push notification; update this file + GLOBAL_HANDOFF at each
  milestone (owner instruction: model can silently drop Fable→Opus; a fresh session must resume cleanly).

## WP-L P2 — round-2 package Claude flagship PASS-WITH-NITS (2026-08-09)

Fresh `.claude-max` `claude-opus-5` xhigh audit accepted exact package `3fa33555`: zero required findings,
clean isolated worktree. Record:
`11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_DISPATCH_PACKAGE_ROUND2_AUDIT_2026-08-09.md`.

**PICK UP EXACTLY HERE:**

- **[AI: Codex]** Fresh fourth-account `gpt-5.6-sol` xhigh audit of byte-exact `3fa33555`.
- **[AI: Any]** Fresh GLM-5.2 detection audit; DeepSeek nonexecution never acceptance.
- **[AI: Claude]** Do not implement yet; package awaits Codex and unresolved-finding floor.

## WP-L P2 — dispatch package repair round 2/3; canonical re-audit next (2026-08-09)

Round-1 package re-audits: GLM `PASS-WITH-NITS`; Codex `REQUEST_CHANGES`. Lead reproduced three findings:
superseded normative pins, incorrect GLM+Codex acceptance floor, and missing implementer-executed D026
evidence. Round-2 repair removes old pins, restores Claude+Codex flagship floor, requires safe local actual
RED/GREEN commands+outputs, and corrects `verify.sh:155-205`. Record:
`11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_DISPATCH_PACKAGE_POST_ACCEPTANCE_REPAIR_2026-08-09.md`.

**PICK UP EXACTLY HERE:**

- **[AI: Claude]** Fresh Opus-5 xhigh package audit first; not implementation.
- **[AI: Codex]** Fresh `gpt-5.6-sol` xhigh package re-audit; GLM fresh detection audit.
- **[AI: Claude]** Proposal implementation stays 0/3 until canonical package floor accepts.
- **[AI: Any]** No host/authority hold changed.

## WP-L P2 — post-acceptance package defect repaired; re-audit required (2026-08-09)

GLM source audit found and Lead reproduced that no-rebind `first_start_unit_sha256` is the installed unit
hash when present, not empty. The bad rule entered as an optional audit nit and propagated into the
prompt/checklist; prior package acceptances are superseded. Exact repair record:
`11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_DISPATCH_PACKAGE_POST_ACCEPTANCE_REPAIR_2026-08-09.md`.

**PICK UP EXACTLY HERE:**

- **[AI: Any]** Freeze and fresh re-audit repaired package; do not dispatch Claude yet.
- **[AI: Codex]** Require executing GLM-5.2 and `gpt-5.6-sol` xhigh re-audits before package acceptance.
- **[AI: Claude]** Proposal implementation remains 0/3; wait for repaired-package acceptance.
- **[AI: Any]** No host/authority hold changed.

## WP-L P2 — candidate anchor map frozen (2026-08-09)

Created `11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_CANDIDATE_ANCHOR_MAP_2026-08-09.md` with exact candidate
`2ce41e34` paths, Git blob IDs, line-qualified APIs/predicates, and proposal implications for
`wal_state_bundle.py`, `lib/common.sh`, `verify.sh`, `rollback.sh`, and first-start systemd template.

**PICK UP EXACTLY HERE:**

- **[AI: Claude]** Run proposal round 1/3 from the audited prompt when exact account capacity returns.
- **[AI: Codex]** Freeze the one-file result; verify against anchor map + checklist `456968bb`.
- **[AI: Any]** This map is read-only evidence, not host/script/trading/deployment authority.

## WP-L P2 — dispatch package accepted by fourth-account Codex (2026-08-09)

Fresh `gpt-5.6-sol` xhigh fourth-account audit returned `PASS-WITH-NITS`, zero required findings, after
446 s with exact candidate/source and byte-equality checks; Git status clean. Record:
`11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_DISPATCH_PACKAGE_CODEX_AUDIT_2026-08-09.md`.

The one optional wording nit matches GLM and remains unapplied to preserve checklist `456968bb`. This is
package acceptance only; proposal implementation remains 0/3.

**PICK UP EXACTLY HERE:**

- **[AI: Claude]** Run audited one-file prompt at first exact account-capacity window, proposal round 1/3.
- **[AI: Codex]** Freeze result and execute checklist `456968bb`; future proposal acceptance still needs
  fresh canonical protected-scope audit.
- **[AI: Any]** No host/authority hold changed.

## WP-L P2 — Codex fourth-account package audit non-execution (2026-08-09)

Fresh `gpt-5.6-sol` xhigh fourth-account audit returned `BLOCK` without reading package files because the
prompt's phrase `do not run host commands` was interpreted as forbidding local read-only file/Git access.
No file changed and no package finding was produced. This is audit-prompt non-execution, not rejection.

**PICK UP EXACTLY HERE:** retry fresh with local read-only `rg`/file/Git commands explicitly allowed and
remote host/SSH/service/reboot/rollback plus all mutation still forbidden. Do not count a repair round.

## WP-L P2 — Lead acceptance checklist ACCEPTED PASS-WITH-NITS (2026-08-09)

Fresh GLM-5.2 re-audit accepted exact checklist commit
`456968bbc694c90d7c30878059a96020c298d8a7`: `PASS-WITH-NITS`, zero required repairs, clean Git status.
Corrected candidate path/symbol/predicate/call sites and both optional hardenings were reproduced. Full
record: `11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_LEAD_ACCEPTANCE_CHECKLIST_AUDIT_2026-08-09.md`.

One optional wording nit is intentionally unapplied to preserve exact audited SHA; current D026 and
non-execution=`BLOCK` language already prevents the hypothetical false acceptance.

**PICK UP EXACTLY HERE:**

- **[AI: Claude]** At first exact account capacity, run audited repair prompt as proposal round 1/3.
- **[AI: Codex]** Freeze the returned one-file diff and execute exact accepted checklist `456968bb`.
- **[AI: Any]** No host/script extraction/budget/credential/broker/TESTNET/ARM/order/WP-V/KVM2/master/
  old-payload/economic action or `C:\PGRK` reopening is authorized.

## WP-L P2 — Lead checklist round 1 repaired; re-audit next (2026-08-09)

GLM-5.2 returned `REQUEST_CHANGES` on checklist commit `313bc187`: candidate `/222` anchor incorrectly
named `deploy/linux/common.sh`; exact path is `deploy/linux/lib/common.sh`. Lead reproduced absent/present
blob checks and the exact symbol. Round-1 repair plus two optional standalone hardenings are recorded in
`11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_LEAD_ACCEPTANCE_CHECKLIST_AUDIT_2026-08-09.md`.

**PICK UP EXACTLY HERE:**

- **[AI: Any]** Freeze and fresh re-audit the repaired checklist; it is not accepted yet.
- **[AI: Claude]** Proposal implementation is still 0/3 and may start from the separately audited prompt
  when exact account capacity returns.
- **[AI: Codex]** Keep checklist repair accounting separate from proposal repair accounting; no host action.

## WP-L P2 — DeepSeek checklist audit route unavailable (2026-08-09)

Fresh isolated worktree `C:\WP2CL` at exact `313bc187` remained clean. ClinePass DeepSeek V4 Flash
returned `hook dispatch failed: session.hook requires a valid hook event payload` and `No access to
ClinePass subscription models yet` before reading/auditing. No verdict and no repair round.

**PICK UP EXACTLY HERE:**

- **[AI: Any]** Continue the same read-only checklist audit through an available subscription route.
- **[AI: Codex]** Treat DeepSeek as non-execution; do not use paid API fallback merely to manufacture a
  verdict and do not weaken the canonical acceptance floor.
- **[AI: Claude]** The audited one-file repair prompt remains ready for the first exact account window.

## WP-L P2 — Lead acceptance/falsification checklist prepared (2026-08-09)

Prepared future verification contract:
`11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_LEAD_ACCEPTANCE_CHECKLIST_2026-08-09.md`. It maps F1-F9 and
RP0-RP6 to exact scope/source checks and local D026 RED/GREEN fixtures. It forbids host/service/reboot/
rollback execution and does not pre-accept a future Claude result.

**PICK UP EXACTLY HERE:**

- **[AI: Any]** Read-only adversarially audit this checklist against the accepted spec and D025/D026.
- **[AI: Claude]** Dispatch the already-audited repair prompt through the first available exact flagship
  route; freeze its one-file diff before another agent touches it.
- **[AI: Codex]** Run the accepted checklist against the actual repaired proposal before canonical audit.
- **[AI: Any]** All host, script extraction, budget, credential/broker/TESTNET/ARM/order, WP-V/KVM2/
  master/old-payload/economic and `C:\PGRK` holds remain unchanged.

## WP-L P2 — Claude repair prompt audited and hardened (2026-08-09)

GLM-5.2 executed a five-file read-only contract audit: `PASS-WITH-NITS`, zero required repairs, clean
worktree. Full record:
`11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_CLAUDE_REPAIR_PROMPT_AUDIT_2026-08-09.md`. Lead folded all four
optional hardenings into the durable prompt without changing scope or authority.

**PICK UP EXACTLY HERE:**

- **[AI: Claude]** Execute the audited prompt as fresh repair round 1/3 through the first available exact
  flagship account route.
- **[AI: Codex]** While capacity is blocked, prepare only read-only Lead acceptance/falsification checks;
  after implementation, inspect actual diff and reproduce F1-F9 before freezing it.
- **[AI: Any]** No host, script extraction, budget, credential/broker/TESTNET/ARM/order, WP-V/KVM2/master/
  old-payload/economic action or `C:\PGRK` reopening is authorized.

## WP-L P2 — alternate Claude route checked; capacity blocked (2026-08-09 10:10 +03:00)

Explicit `.claude` dispatch of the frozen one-file repair prompt returned before any edit with:
`You've hit your session limit · resets 1:50pm (Europe/Chisinau)`. Working tree remained clean. The
separate `.claude-max` route's previously observed reset is 11:10. This is an account-capacity blocker,
not a repair verdict, and it consumes no repair round.

**PICK UP EXACTLY HERE:**

- **[AI: Any]** Read-only audit the durable dispatch prompt while Claude is unavailable.
- **[AI: Claude]** At the first available exact flagship route, execute repair round 1/3 from the frozen
  prompt; do not resume a prior implementation/audit session.
- **[AI: Codex]** Continue independent scope/evidence checks; do not substitute GLM/DeepSeek as protected
  implementer and do not perform host actions.

## WP-L P2 — exact Claude repair prompt ready (2026-08-09)

Durable counterpart contract:
`11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_CLAUDE_REPAIR_PROMPT_2026-08-09.md`. It freezes accepted spec
`9ac60ac6`, limits writes to the rejected proposal document, implements RP0-RP6, folds the four optional
nits, and preserves every host/trading/deployment hold.

**PICK UP EXACTLY HERE:**

- **[AI: Codex]** Verify the alternate Claude CLI account without exposing credentials.
- **[AI: Claude]** If exact flagship access is available, execute this prompt as repair round 1/3.
- **[AI: Codex]** Independently inspect the resulting one-file diff and reproduce F1-F9 closure before
  freezing or auditing it. Do not accept the implementer report by itself.
- **[AI: Any]** No host action, script extraction, budget lift, credential/broker/TESTNET/ARM/order action,
  WP-V/KVM2/master/old-payload action, or reopening of `C:\PGRK` is authorized.

## WP-L P2 — F1-F9 repair specification ACCEPTED PASS-WITH-NITS (2026-08-09)

Accepted exact commit `9ac60ac652f4a221316465cdbc24516aa391f5ce`. GLM-5.2 executed the independent
read-only candidate-source audit and returned `PASS-WITH-NITS`, zero required repairs; Lead reproduced
RP0-RP6 and all candidate anchors. Codex secondary timed out at 604 s; Claude alternate account returned
session-limit/no verdict. Those are supplemental non-execution. Full record:
`11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_REPAIR_SPEC_AUDIT_2026-08-09.md`.

Optional nits: ancillary path fixture; explicit empty C4 no-rebind fields; deferred C1 falsification list;
name `src_conn.backup(dst_conn)`. None weakens the accepted contract.

**PICK UP EXACTLY HERE:**

- **[AI: Codex]** Prepare the exact one-file counterpart implementation prompt from the accepted spec.
- **[AI: Claude]** Implement only when an exact counterpart flagship CLI account is available; current
  known account resets are 11:10 (`.claude-max`) and 13:50 (`.claude`). Do not substitute GLM/DeepSeek.
- **[AI: Any]** Acceptance is specification-only. Rejected proposal `779bd038` remains non-executable;
  `C:\PGRK` remains blocked; no host/script transfer/credentials/broker/TESTNET/ARM/orders/WP-V/KVM2/
  master/old-payload/economic action. Exact 50 h balance remains NOT REPRODUCIBLE.

## WP-L P2 — F1-F9 bounded repair specification authored; audit next (2026-08-09)

Lead-only specification (no proposal/product edit, no host action):
`11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_REPAIR_SPEC_2026-08-09.md`. It freezes a future one-file repair
scope for rejected proposal `779bd038`: RP0 evidence bootstrap/status mapping; RP1 exact B3 admission;
RP2 C1 remains BLOCKED on exact exit tuple + safe active-writer baseline; RP3 two preregistered C2
branches with real invariant baselines; RP4 correct `sqlite3.Connection` + `invariants_hash` restore;
RP5 dry-run/no-clobber/invariant C4; RP6 C5 remains blocked. It specifies required RED/GREEN
falsifications and a three-round future repair cap. It does not reopen or repair `C:\PGRK`.

**PICK UP EXACTLY HERE:**

- **[AI: Codex|Claude]** Freeze and independently audit the repair specification itself before any
  counterpart edits the rejected proposal.
- **[AI: Claude]** No implementation yet. After spec acceptance and a confirmed new bounded proposal
  cycle, edit only `11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md`.
- **[AI: Any]** No host/server execution, script transfer, credentials, broker/TESTNET, ARM, orders,
  WP-V, KVM2, master merge, old-payload deletion, or economic action. Exact 50 h balance remains NOT
  REPRODUCIBLE.

## WP-L P2 — `779bd038` command-gap proposal REQUEST_CHANGES (read-only audit, 2026-08-09)

Independent Lead audit record:
`11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_AUDIT_2026-08-09.md`. **Do not transfer or execute the proposed
scripts.** Required defects reproduced: dangling-link evidence clobber in every script; B3 accepts `0444`,
misses group/other write bits, and omits manifest binding; C1 has no pre-stop invariant baseline and an
insufficient exit/timeout proof; C2-A can convert failed `is-enabled`/link probes into an unmasked PASS;
both reboot scenarios lack pre/post persistence equality; C3 passes a path to candidate
`collect_invariants(Connection)` and raises `AttributeError`; C4 can overwrite the rollback manifest and
calls filename+size equality "byte-for-byte" preservation; `pgrep || true` collapses fatal/tool errors.
C5 correctly remains blocked.

External review status: Claude Opus 5 xhigh and GLM-5.2 each timed out at 604 s with no verdict;
DeepSeek ClinePass failed subscription/hook access; API fallback exhausted 24 iterations without a
verdict. These are supplemental non-execution. All audit worktrees remained clean. Codex Lead reproduced
the decisive findings against candidate `2ce41e34`.

**PICK UP EXACTLY HERE:**

- **[AI: Codex]** Next autonomous safe unit: write a bounded, no-edit repair specification for
  `779bd038` F1-F9, explicitly separating the proposal repair from the exhausted `C:\PGRK` design loop.
- **[AI: Claude]** Implement only after that specification is frozen and a new bounded implementation
  cycle is authorised; protected Bridge design work must not be routed to a secondary model.
- **[AI: Any]** No host/server execution, script transfer, credentials, broker/TESTNET, ARM, orders,
  WP-V, KVM2, master merge, old-payload deletion, or economic action. Exact 50 h balance remains NOT
  REPRODUCIBLE.

## GATE A — local run-kit design BLOCKED after third repair round (2026-08-09)

**Do not commit, integrate, implement, or audit the current draft.** Lead inspection after the third
non-accepting repair round found an evidence-root bootstrap contradiction: `RK-B0` requires every host
command and STOP to be captured under `<EVROOT>`, but it verifies Python, allocates the timestamp, and
creates the parent/leaf directories before `<EVROOT>` exists. Parent canonical/non-symlink proof and the
no-clobber `EXPECTATIONS.md` transfer are also not closed. A fourth silent repair is forbidden.

Unaccepted draft: `C:\PGRK`, base `4599b466`, one untracked file
`11_TRIAGE/GATE_A_POST_GATE_LOCAL_RUN_KIT_DESIGN_2026-08-09.md`, SHA-256
`d12e25fb06273b006c47342fac093d4afc99e32bda815fb5e428b8a3da584107`, 194207 bytes / 2332 lines.
No canonical audit was launched and no host action occurred. Full blocker record:
`11_TRIAGE/GATE_A_POST_GATE_LOCAL_RUN_KIT_DESIGN_BLOCKER_2026-08-09.md`.

**PICK UP EXACTLY HERE:**

- **[AI: Any]** Next autonomous safe unit: read-only independent audit of live commit `779bd038` and
  `11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md`. Determine candidate qualification, scope,
  command safety, and whether any bootstrap evidence is reusable. This is separate from the blocked
  design and does not reopen its repair loop.
- **[AI: Barış]** A new repair cycle for the `C:\PGRK` design requires explicit owner direction. The
  cycle must first close the pre-`<EVROOT>` evidence channel; `D-GAP-C1-1` and `D-GAP-C1-3` remain
  independently blocking.
- **[AI: Any]** Keep all existing holds: no server execution, credential/broker/TESTNET action, ARM,
  orders, WP-V, KVM2, master merge, old-payload deletion, or economic action. Exact 50 h balance remains
  NOT REPRODUCIBLE.

## GATE A — candidate provenance repair ACCEPTED; run-kit design contract next (2026-08-09)

**Accepted live commits:** `970c95a6` + `03444271`; frozen audited snapshot
`2fa120b928045704405c0a5156d73b3b930d1837`. Candidate
`2ce41e34bceb599d80af24c5c33d835820ec321b` is unchanged. The documentation branch and candidate
diverge at merge base `4d2228cf8985ce755c398cceff23f777a99d5404`; product, deploy, runtime,
tool, and differing-test facts must be candidate-qualified.

**Corrected facts:** all 11 WP0-mapped test symbols exist at the candidate; symbol 11 is
`IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:2765`. WP0 is correct and remains untouched.
Lock provenance is: Git blob object ID `47f53fa227bf0f18b9bf9bd77e060d8856961728`; expected raw LF
blob/package content SHA-256 `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e`;
local Windows CRLF checkout SHA-256 `40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3`
is never a candidate/Linux/host predicate. The observed installed-host lock hash is **NOT IN EVIDENCE**
and remains open as read-only item B1a.

**Candidate safety:** the first-start unit pins `credential_free_disarmed`, the env-file verifier rejects
an override, and the application constructs no broker in that mode. The ref-invariant steady template
does not carry the start-mode pin; treat that as a future admission prerequisite, not a current defect.

**Acceptance:** Claude Opus 5 xhigh `PASS-WITH-NITS`; Codex gpt-5.6-sol xhigh `PASS`; GLM-5.2
`PASS`. DeepSeek V4 Flash could not run through ClinePass, and the fallback driver could not execute
the mandated Git/hash suite, so its result is supplemental `BLOCK`/non-execution. All four audit
worktrees stayed clean; the Lead reproduced the decisive claims; no required finding remains.

**PICK UP EXACTLY HERE:**

- **[AI: Claude]** Author the corrected **local-only run-kit design contract** from candidate-qualified
  product reads. It must cover Stage B static admission, C1 graceful stop/no-dangling-state, C2 reboot,
  C3 no-clobber bundle/restore-into-temp, C4 stop+mask rollback, and blocked C5 egress. Design only.
- **[AI: Claude|Codex]** Independently audit that design before any implementation. Stage-B/run-kit
  implementation begins only after design acceptance.
- **[AI: Any]** Keep `GATEA-STAGING` retained and credential-free DISARMED. No server execution,
  credential load, broker/TESTNET access, ARM, order, WP-V, KVM2, master merge, or economic action.
- **[AI: Barış]** Budget/authority holds are unchanged: exact 50 h balance remains NOT REPRODUCIBLE;
  server execution requires a human re-plan/ceiling extension and any separately named authority lift.

**Canonical records:** `11_TRIAGE/GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md` and
`11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md`.

## GATE A — Post-Gate preregistration & gap matrix (WP-L Phase 2 → WP-I → Audit 2 → WP-A) (read-only) (2026-08-09)

**Read-only documentation unit; no staging command run.** Starting HEAD `52b8f496`; candidate
`2ce41e34…321b` unchanged. Full record:
`11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md`. Worker scope: GLM-5.2 edited
only the four task-named files and ran no SSH/Gate-A-script/sudo/systemctl/reboot/test/package/Git/
staging-mutation/credential-read/broker-network command.

**Result:** the correct post-Gate sequence **`WP-L Phase 2 → WP-I staging verification → Audit 2 →
WP-A`** is verified from source (roadmap §23a steps 3–5 + §"Audit 2"; runbook `:137`). Its obligations,
reusable evidence, and unresolved command gaps are explicitly mapped; it is **not execution-ready**.
**Do not start WP-V; do not rerun Gate A.** Gate-A A-0..A-9 PASS is staging acceptance
only — reuse its immutable evidence where predicates overlap, but it is not WP-L/WP-I/WP-A completion.
56-entry hash-locked closure re-confirmed at the candidate checkout (56 entries, 1345 hashes).

**Matrix groups:** A reusable immutable Gate-A evidence · B read-only post-start host checks · C
mutating host checks · D Audit 2 (**superseded 2026-08-10:** D028 permanent tier policy now controls
auditor count/cadence; use the current `AGENTS.md`, not this historical four-auditor label) · E WP-A targeted Ubuntu verification. All host commands **NOT EXECUTED**; **COMMAND GAP**
markers where an exact safe command is not yet specified. **Superseded by the accepted provenance
repair above:** all 11 requested symbols exist at the candidate, including
`test_kill_restart_after_request_commit_keeps_killed_and_resumes_once` at `:2765`; WP0 is correct and
untouched. D026 still binds (existing tests ≠ new closure evidence).

**Key gaps:** (G1) reboot DISARMED must be defined precisely — first-start `Restart=no` + no `[Install]`
= cannot auto-start; steady profile gated/inert/no-`[Install]`; reboot preserves mask state, so plain
reboot from the current unmasked state expects inactive+unmasked, while inactive+masked requires a
separate pre-reboot mask step. Either path must prove no process/listener/order and DB not ARMED; no
defect yet. (G2) full `verify.sh` intentionally fails
post-start — use bounded subchecks. (G3) rollback rebind unmet prerequisite (only candidate installed).
(G5) A-5 = SIGKILL not SIGTERM/reboot; A-6 ≠ queue/full-reconcile. (G6) README "never executed" stale
post-Gate. (G7) exact 50 h balance NOT REPRODUCIBLE → all host execution blocked.

**Lead correction:** actual TESTNET egress observation needs credentials plus broker/TESTNET network
authority, **not ARM**; any future capture remains DISARMED and no-order. **Superseded hash correction:**
the expected LF package-content SHA-256 is `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e`;
`40873556…` is only a local CRLF checkout hash and must never be used as a Linux predicate.

**Blockers:** (1) budget — 50 h balance not reproducible; human re-plan/ceiling extension required
before any server-executed WP-L/WP-I/WP-A work. (2) authority — WP-V/KVM2/master/credentials/broker/
ARM/orders/TESTNET-mainnet/economic action each need a new named lift.

**PICK UP EXACTLY HERE:**

- **[AI: Any]** Next autonomous safe unit = **local run-kit design/validation only**: author Group B
  read-only subchecks + the five COMMAND-GAP procedures (post-start verifier, post-SIGTERM
  no-dangling-state, post-reboot subcheck, restore-into-temp wrapper, stop+mask-only rollback step) as
  *designs* from candidate-qualified reads; WP0 requires no refresh. **No staging execution.**
- **[AI: Any]** Keep `GATEA-STAGING` retained, active, credential-free DISARMED; do not discard (needed
  through WP-A).
- **[AI: Barış]** Re-plan remaining hours vs the hard 50 h ceiling, or issue an explicit ceiling
  extension, before any server-executed post-Gate work.
- **[AI: Barış]** Named explicit lift required before WP-V/KVM2/master/credentials/broker/ARM/orders/
  TESTNET-mainnet/economic action/old-payload deletion.

**Stop conditions:** any WP-V/KVM2/master/ARM/credentials/broker/orders/economic action without a named
lift; any evidence needing a product repair; any unevidenced hour claim; inventing a rollback target,
running `verify.sh` wholesale post-start, or destructively testing the active DB; any service drift on
`GATEA-STAGING`.

## GATE A — 50h ledger reconstructed; current exact balance NOT REPRODUCIBLE (read-only) (2026-08-09)

**Read-only documentation checkpoint; no staging command run.** Starting HEAD `921449f1`. Full record:
`11_TRIAGE/GATE_A_50H_LEDGER_RECONSTRUCTION_2026-08-09.md`.

**Result (five states):** (1) EXACT BOOKED checkpoint **20.5 used / 29.5 nominal remainder**
(`WPL_PHASE1_VERIFICATION_RECORD_2026-08-01.md:134`: WP-0 2.0 + WP-S 12.0 + contingency 3.0 + WP-R 3.5);
(2) S3-STRUCT actual **UNEVIDENCED** — outside the 50 h ledger; ~6 h was a warning threshold, not an
actual; never record as 6 h (`WPS_S3STRUCT_ACCEPTANCE_RECORD_2026-08-01.md:150-153`); (3) APPROXIMATE
NON-LEDGER Aug03 only ≈33–36 used / ≈14–17 remaining, exact booking deferred
(`GATE_A_QUEUE_D_INTEGRATION_STATUS_2026-08-03.md:182-186`); (4) UNBOOKED/UNCLASSIFIED — exact WP-L/WP-I
booking and all post-Aug03 Gate-A work, **no package actual-hour record** (repair queue = *"unplanned work
that did not exist in the original 29.5 h"*, same record `:186`); (5) **CURRENT EXACT USED AND REMAINING =
NOT REPRODUCIBLE.** Never invent or retroactively book hours. Hard 50 h ceiling: WP-0 2 · WP-S 12 · WP-L 8
· WP-I 6 · WP-A 3 · WP-R 6 · WP-V 8 · contingency 5.

**Consequence:** budget compliance for server-executed post-Gate work cannot be proven; do not commit
server execution against the unknown hard ceiling. Budget-evidence blocker, not idle. *"Repair budget
exhausted"* = repair-round count (max 3), **not** contingency = 0 (contingency had 2.0 h left). Routing:
ClinePass DeepSeek V4 Flash had no subscription; the `deepseek-chat` harness stopped unfinished on
path-resolution loops — **no allowlisted repository target changed**, but it persisted its report and
transcript at `C:/tmp/gatea_hour_ledger_ds_report.md` and removed the temporary task JSON (do **not** read
the route as mutating nothing globally); **DeepSeek did not produce this — GLM-5.2 did.**

**PICK UP EXACTLY HERE:**

- **[AI: Any]** Build the read-only/local preregistration gap matrix for **WP-L Phase 2 + WP-I staging
  verification + Audit 2 + WP-A** — exact command scope, evidence paths, PASS/FAIL, stop conditions,
  per-unit authority/budget status. No server execution.
- **[AI: Any]** Keep `GATEA-STAGING` retained and credential-free DISARMED — **do not discard it.**
- **[AI: Barış]** Re-plan the remaining hours against the 50 h ceiling, or issue an explicit ceiling
  extension, before any server-executed post-Gate work.
- **[AI: Barış]** WP-V / KVM2 / master / credentials / broker / ARM / orders / TESTNET/mainnet / economic
  action / old-payload deletion each need a **new explicit named lift.**

## GATE A — post-Gate roadmap + authority discovery complete (read-only); WP-V is NOT next (2026-08-09)

**Read-only discovery only — no staging command was run.** Starting HEAD `51e666b0`; product candidate
remains `2ce41e34bceb599d80af24c5c33d835820ec321b`. Gate A A-0..A-9 PASS is **staging acceptance only**.

**Canonical sequence after Gate A** (plan §23a, exact): 3 one named expendable Ubuntu staging action →
4 Audit 2 after WP-L Phase 2 + WP-I staging verification → 5 WP-A on the retained host → 6 discard host
only after WP-A evidence → 7 freeze final exact SHA/artifact → 8 Audit 3 Gate-5 + Gate-6 → 9 Gate B →
10 WP-V only after deployment approval → 11 Gate C. Runbook line 137 gives the immediate chain:
`Gate A verification → WP-L Phase 2 → WP-I staging → Audit 2 → WP-A`, all DISARMED. **Audit 2 restores
the flagship acceptance floor.**

**Therefore WP-V is NOT next.** No record proves WP-L Phase 2, WP-I staging verification, Audit 2, or
WP-A completed after the final Gate-A pass. `GATEA-STAGING` still exists, active/running, credential-free
DISARMED, only candidate `2ce41e34…321b` installed — **not discarded**, and it is the host steps 3–5 need.

**Authority:** standing owner authorization (`OWNER_AUTH_50H_EXECUTION_PROMPT_2026-07-31.md:20-56`) does
cover WP-L/WP-I/WP-A/WP-R/WP-V, Ubuntu staging, the named host, KVM2, and pre-grants WP-V/ARM/first-TESTNET
— **subject to every objective prerequisite.** Narrower later constraints control the current transition:
`CODEX_TAKEOVER_HANDOFF_2026-08-02.md:261-263` and `NEXT_SESSION_HANDOFF_2026-08-08.md:1452-1454`. A
generic continue instruction does not name or lift those stops. **Do not infer WP-V authority from
Gate-A PASS or from generic continue wording.**

**Budget blocker:** ≈14–17 h remained before the 2026-08-08 session; WP-A+WP-R+WP-V alone total 17 h;
Gate-A repairs/rebuild/audits were unbudgeted. Exact current ledger **not reconstructed**; hard 50 h
ceiling, no silent overrun. **This does not require idling.**

**Line-citation provenance.** The `NEXT_SESSION_HANDOFF_2026-08-08.md` line citations `1452-1454` (that
file's **Hard stop** block) and `1489-1492` (its `## Budget` section) are taken from starting HEAD
`51e666b0`. That file was later prepended, so these citations are shifted by the prepend (+59 lines
added, 0 deleted) and the cited content now sits ~59 lines later in the working copy; locate it by the
stable target text `Hard stop — unchanged, needs a new explicit instruction from Barış` and `## Budget`
instead of raw line numbers.

**PICK UP EXACTLY HERE:**

- **[AI: Any]** Reconstruct package-by-package hour accounting; classify Gate-A repair work as
  contingency vs outside-budget. Do not invent hours — mark unevidenced figures unevidenced. Read-only.
- **[AI: Any]** Build the post-Gate preregistration/gap matrix for WP-L Phase 2 + WP-I staging
  verification + Audit 2 + WP-A from existing records and exact candidate/service state. Read-only/local.
- **[AI: Any]** No server execution until that package proves command scope, evidence outputs, stop
  conditions, and budget/authority fit.
- **[AI: Any]** Keep `GATEA-STAGING` retained and credential-free DISARMED — **do not discard it.**
- **[AI: Barış]** Re-plan the remaining hours against the 50 h ceiling before committing further execution.
- **[AI: Barış]** WP-V, KVM2, master merge, credential load, broker/exchange access, ARM, orders,
  TESTNET/mainnet, economic action, and old-payload deletion each need a **new explicit named lift**.
- Record: `11_TRIAGE/GATE_A_POST_GATE_ROADMAP_AUTHORITY_DISCOVERY_2026-08-09.md`.

---

## GATE A — post-Gate transition inventory complete (read-only); old install already absent (2026-08-09)

Post-Gate transition inventory is **complete and read-only**. Gate A A-0..A-9 PASS remains **staging
acceptance only**. **Critical correction:** the old installed release `ebada020a59edf539f60acfbb3a6bf870c8679e9`
and its venv are **already absent** (teardown evidence `/home/gatea/teardown-ebada020-20260808B` exists),
so **no old-install cleanup mutation is required** — the prior "THEN perform old-install cleanup" step is
moot. Only installed release: `/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b` (root
mode `555`) + venv counterpart (root mode `555`); **no** steady/legacy `mtc-bridge` unit; **no**
`current`/`previous` symlinks under `/opt/mtc-bridge`. Service `mtc-bridge-first-start.service`
active/running PID `189813`, `Restart=no`, `NRestarts=0`, exactly one `127.0.0.1:8790` listener, DISARMED
`state_version=1`, all flags off. Candidate `2ce41e34…321b` unchanged; repo HEAD `5af8178b`.

**PICK UP EXACTLY HERE:**

- **[AI: Any]** Read-only discover the canonical post-Gate workflow, roadmap, and WP-V / deployment /
  promotion gate chain; determine whether explicit transition authority exists. If none, record a blocker.
- **[AI: Any]** Do not rerun Gate A or mutate staging during discovery; keep the service credential-free
  DISARMED.
- **[AI: Barış]** Deletion of `/home/gatea/payload_ebada020.tar` (inert, 1,039,774,720 B) requires a
  separate explicit archive-cleanup scope — not authorized here.
- **[AI: Barış]** ARM, credential load, broker connectivity, orders, TESTNET/mainnet, production
  promotion, and master merge each require separate explicit owner authorization; Gate-A PASS grants none.
- Record: `11_TRIAGE/GATE_A_POST_GATE_TRANSITION_INVENTORY_2026-08-09.md`.

---

## GATE A — A-0..A-9 PASS; final staging acceptance; post-Gate inventory next (2026-08-09)

A-9 executed exactly once at branch checkpoint `6073c30c`; accepted candidate
`2ce41e34bceb599d80af24c5c33d835820ec321b` unchanged. Command:
`bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A9.sh`; SSH rc0, transport stdout/stderr
empty because the script redirects to its no-clobber evidence log. Evidence
`/home/gatea/gatea-A9-20260808D.log` preserved to `C:\WPI_ARTIFACTS\gatea-A9-20260808D.log`;
remote/local SHA-256 identical `23d61687…b3004bd5e9`
(`23d61687ce6cbf290b134d6bd72763f7bb4be27b15daae457373d6bb004bd5e9`), 876 B. Exactly nine canonical
category lines in order — `private_key_block`, `aws_access_key`, `github_token`, `slack_token`,
`openai_token`, `anthropic_token`, `xai_token`, `telegram_bot_token`, `ethereum_private_key` — each
exactly `rc=1 matches=0`; `A9_any_hit=0`; one `A-9 PASS`; one `A9_TRAP_EXIT rc=0`; zero `A9_FAIL`,
zero path blocks, zero grep-error blocks. No matched path, text, or value existed or was printed.
Exact scan roots recorded: release candidate root and `/etc/mtc-bridge`; venv and `/home/gatea`
excluded. A-9 truthfully read bytes including the root-readable env file while `grep -l` emitted no
matched content; no secret value entered Lead output. Independent postcheck rc0 artifact
`C:\WPI_ARTIFACTS\postcheck_gatea_a9_d.out` (stderr empty): evidence hash/bytes, all nine exact
rc1/matches0 lines, aggregate hit0/PASS/trap/no-fail/no-path/no-error, zero A9 err/preflight temp
leftovers, exact safe API, service active/running PID189813, Restart=no, NRestarts0, one loopback
listener; `A9_POSTCHECK=PASS`.

- Gate state: **A-0 through A-9 PASS.** A-5 used accepted run-kit E; A-6 through A-9 used accepted
  run-kit D; candidate remained `2ce41e34…321b`.
- Staging safe: active/static (Restart=no), PID189813, NRestarts0, loopback-only `127.0.0.1:8790`,
  exact credential-free DISARMED `state_version=1`, all credential/network/exchange/ARM flags off.
  No credentials loaded, no broker/exchange/order action.
- **Scope:** staging Gate-A acceptance only. Evidence-backed, but it does not itself authorize or
  claim old-install deletion, master merge, production/live capital, successful ARM, orders,
  TESTNET/mainnet, wallet, or economic action.
- **[AI: Codex] NEXT:** read-only post-Gate transition inventory — reconstruct the exact A-0..A-9
  reports and hashes, identify the exact old masked installation targets versus the accepted current
  candidate, verify current systemd/release/symlink/package state without reading secrets, and write
  a cleanup/cutover scope checkpoint. No deletion or mutation in that inventory unit.
- **[AI: Codex] THEN:** only after exact-target verification and a fresh `_AI_MEMORY` checkpoint,
  perform any already-authorized old-install cleanup using explicit paths and recoverable/safe
  ordering, preserving the accepted candidate and all evidence. If authorization scope is not
  explicit for a target, record a blocker rather than guess.
- **[AI: Codex] DO NOT:** rerun Gate A, ARM, load credentials, connect broker/exchange, place
  orders, merge to master, or begin TESTNET/mainnet/economic action merely because Gate A passed.
- Record: `11_TRIAGE/GATE_A_A9_PASS_FINAL_2026-08-09D.md`.

---

## GATE A — A-9 redaction-aware preflight PASS; execute A-9 D next (2026-08-09)

Lead-performed read-only, non-executing A-9 preflight at checkpoint `0641c534`; accepted candidate
`2ce41e34bceb599d80af24c5c33d835820ec321b` unchanged. The A-9 script did not run and the real
release and `/etc` roots were not scanned. Accepted D tar
`/home/gatea/gatea-run-kit-20260808D-2ce41e34.tar` (SHA-256 `e8a52e3c…e0d3`, 71680 B); all seven
manifest members OK. Accepted A-9 script
`/home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A9.sh`: SHA-256 `2c7e73be…fada4d`, 3937 B, CR0,
bash syntax rc0; A-9 evidence `/home/gatea/gatea-A9-20260808D.log` absent; zero
`/home/gatea/gatea-A9-err.*` leftovers before and after. Exact real scan roots verified present and
readable — `/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b` and `/etc/mtc-bridge`;
venv and `/home/gatea` excluded by the accepted script. Static contract verified: nine canonical
category names in order; `sudo grep -RIlE --binary-files=without-match -e $ere -- $REL $ETC`;
per-category rc/count; path list only on hit; A-9 truthfully reads bytes in the exact real roots
including the root-readable env file but emits only counts and paths, never matched text/values;
any count>0 is FAIL/BLOCK and rc>1 is FAIL. Permission/redaction falsification: one disposable
`/home/gatea/gatea-A9-preflight.<6>` temp with one synthetic token-like line was created; the exact
`grep -l` command returned exactly the synthetic file path and no matched text/value; the synthetic
value was never printed; guarded nonrecursive cleanup removed temp file and dir; real release and
`/etc` roots were NOT scanned; `grep_path_only_fixture_falsification=true`; post-cleanup no
A9-preflight/A9-err leftovers. Production safe: active/running PID189813, Restart=no, NRestarts0,
one loopback listener, exact HTTP200 credential-free DISARMED state_version1 and all external/ARM
flags off. Local evidence `C:\WPI_ARTIFACTS\preflight_gatea_a9_d.out/.err`, rc0, stderr empty;
`A9_PREFLIGHT=PASS`.

- **[AI: Codex] NEXT:** execute A-9 exactly once with
  `bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A9.sh`.
- **[AI: Codex] THEN:** preserve/hash `/home/gatea/gatea-A9-20260808D.log` locally; inspect only the
  structured per-category rc/count and matching paths, never matched text/value. PASS requires nine
  categories each rc=1 and matches=0, `A9_any_hit=0`, one `A-9 PASS`, trap rc0, no
  `A9_FAIL`/grep-error blocks, and no temp leftover; any hit/nonzero error is FAIL/BLOCK and Gate A
  is not complete.
- **[AI: Codex] THEN:** independently postcheck the safe service and update `_AI_MEMORY` with the
  final Gate A verdict. Do not clean the old deployment or start another gate until the final
  checkpoint is accepted.
- Gate state: **A-0..A-8 PASS; A-9 NOT RUN.** Record: `11_TRIAGE/GATE_A_A9_PREFLIGHT_2026-08-09D.md`.

---

## GATE A — A-8 PASS under run-kit D; A-9 preflight next (2026-08-09)

Both A-8 halves executed exactly once at checkpoint `8cba7897`; accepted candidate
`2ce41e34bceb599d80af24c5c33d835820ec321b` unchanged. Remote:
`bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A8.sh`, SSH rc0, transport stdout/stderr
empty because the script redirects to its no-clobber evidence log. Evidence
`/home/gatea/gatea-A8-20260808D.log` preserved to `C:\WPI_ARTIFACTS\gatea-A8-20260808D.log`;
remote/local SHA-256 identical `a7ef34a1…829f0d7`, 1087 B; exactly one `A-8 PASS`, one
`A8_TRAP_EXIT rc=0`, one `RESULT=PASS`, zero `A8_FAIL`/`RESULT=FAIL`. In-script: `ss_rc=0`,
`listener_count` 1, `local_addresses` exactly `127.0.0.1:8790`, non-loopback/wildcard/VM-IP listener
lists empty, `A8_ufw_rc=0`; IP and UFW evidence captured in the log with the raw payload
deliberately not reproduced. Host: one run of
`powershell -NoProfile -ExecutionPolicy Bypass -File C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34\gatea_A8_host.ps1`,
rc0, command stderr empty, stdout exactly including `port22_ok=True`, empty `port22_err`,
`port8790_ok=False`, `port8790_err=timeout_3000ms`, `host_probe_ok=True`, `A8_HOST_PASS`. Host
evidence `C:\WPI_ARTIFACTS\gatea-A8-host-20260808D.log`: SHA-256 `abad3225…03fee2e6`, 321 B, UTF-8
no BOM, CR0/LF-only, fixed VM/candidate/timeout and the same booleans — note `A8_HOST_PASS` is
command stdout and is not stored in the evidence log. Independent postchecks both rc0 with empty
stderr: `C:\WPI_ARTIFACTS\postcheck_gatea_a8_remote_d.out` (evidence hash/bytes/markers/binding
assertions, exact credential-free DISARMED API, production active/running PID189813, Restart=no,
NRestarts0, one loopback listener) → `A8_REMOTE_POSTCHECK=PASS`; and
`C:\WPI_ARTIFACTS\postcheck_gatea_a8_host_d.out` (evidence hash/bytes/no BOM/CR0, command stdout
includes `A8_HOST_PASS`, independent `TcpClient` reprobe port22 True and port8790 False) →
`A8_HOST_POSTCHECK=PASS`. Combined acceptance held, so A-8 PASS. Contract held: no `/api/arm`, env
file not opened, no credential content, no broker/exchange/order/economic action, read-only
networking and firewall evidence only.

- **[AI: Codex] NEXT:** preflight the accepted D A-9 script — identity and syntax, absence of the
  remote A-9 log, safe service, the exact scan roots and command permissions, and the
  output-redaction contract. A-9 truthfully reads bytes under the release directory and
  `/etc/mtc-bridge` including the environment file, but may emit only category counts and matching
  paths, never matched text or values. Do not execute A-9 during preflight.
- **[AI: Codex] THEN:** update `_AI_MEMORY` before execution.
- **[AI: Codex] THEN:** execute A-9 exactly once, only after the preflight checkpoint; preserve and
  hash the evidence, and inspect only counts and paths, never matched content. A genuine A-9 hit or
  failure is BLOCK/FAIL and stops Gate A completion.
- Gate state: **A-0..A-8 PASS; A-9 NOT RUN.** Record:
  `11_TRIAGE/GATE_A_A8_PASS_2026-08-09D.md`.

---

## GATE A — A-8 remote+host preflight PASS; execute preregistered A-8 D next (2026-08-09)

Lead-performed read-only, non-executing two-part A-8 preflight at checkpoint `4caa553f`; accepted
candidate `2ce41e34` unchanged. Neither A-8 script ran. Accepted D tar
`/home/gatea/gatea-run-kit-20260808D-2ce41e34.tar` (SHA-256 `e8a52e3c…e0d3`, 71680 B); all seven
manifest members OK. Remote packaged A-8 `/home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A8.sh`:
SHA-256 `1fa14524…9d19`, 4124 B, CR0, bash syntax rc0; remote evidence
`/home/gatea/gatea-A8-20260808D.log` absent. Remote production safe: active/running PID189813,
Restart=no/NRestarts0, one `127.0.0.1:8790` listener, exact HTTP200 credential-free DISARMED
state_version1 and all network/exchange/credential/ARM flags off; `ip -brief address` available and
exact `sudo ufw status verbose` noninteractive with output suppressed; `A8_REMOTE_PREFLIGHT=PASS`.
Accepted Windows host packaged A-8
`C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34\gatea_A8_host.ps1`: SHA-256 `57899687…b281`,
3195 B, CR0/LF-only, PowerShell parser errors 0; host evidence
`C:\WPI_ARTIFACTS\gatea-A8-host-20260808D.log` absent. Windows host port-22 reachability control to
172.24.55.233 passed within 3000 ms, proving host route/SSH control; port8790 deliberately not
probed (reserved for the actual host A-8 script); `A8_HOST_PREFLIGHT=PASS`. Local evidence
`C:\WPI_ARTIFACTS\preflight_gatea_a8_remote_d.out/.err` and `preflight_gatea_a8_host_d.out/.err`;
both rc0, stderr empty.

- **[AI: Codex] NEXT:** execute the remote half exactly once with
  `bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A8.sh`.
- **[AI: Codex] THEN (only if remote rc0/evidence ends `A-8 PASS`):** execute the packaged Windows
  host half exactly once with
  `powershell -NoProfile -ExecutionPolicy Bypass -File C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34\gatea_A8_host.ps1`.
- **[AI: Codex] ACCEPTANCE:** A-8 PASS requires both remote `A-8 PASS` and host `port22_ok=True`,
  `port8790_ok=False`, `host_probe_ok=True`, `A8_HOST_PASS`, host rc0. Preserve/hash both evidence
  logs, independently postcheck safe service, update `_AI_MEMORY` before A-9. On either genuine
  subpart FAIL do not run A-9; if the remote half fails, do not run the host half.
- Gate state: **A-0..A-7 PASS; A-8..A-9 NOT RUN** (A-8 not executed). Record:
  `11_TRIAGE/GATE_A_A8_PREFLIGHT_2026-08-09D.md`.

---

## GATE A — A-7 PASS under run-kit D; A-8 preflight next (2026-08-09)

A-7 executed exactly once at checkpoint `519223e2` with
`bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A7.sh`; SSH rc0, transport stdout/stderr
empty because the script redirects to its no-clobber evidence log. Accepted candidate `2ce41e34`
unchanged. Evidence `/home/gatea/gatea-A7-20260808D.log` preserved to
`C:\WPI_ARTIFACTS\gatea-A7-20260808D.log`; remote/local SHA-256 identical `09443b51…2bbf5`, 4269 B;
exactly one `A-7 PASS`, one `A7_TRAP_EXIT rc=0`, one `RESULT=PASS`, zero `A7_FAIL`/`RESULT=FAIL`.
API: HTTP200, DISARMED, mode credential_free_disarmed, state_version1, reconcile_ready False
(expected, not required true), reconcile_error None, all network/exchange/credential/ARM flags off.
Production DB via preregistered read-only sudo: quick_check ok, app_state DISARMED, schema_version4,
explicit cross-source equality `A7_db_app_eq_api_state=DISARMED==DISARMED`. Point-in-time documented
logs: `bridge.log` 1554 B, mode600 root:root, SHA `efda2d19…d02d`; `bridge.err.log` 597 B, mode600
root:root, SHA `0b906765…d207`. Journal query succeeded with exactly 22 payload lines bounded by
begin/end; `A7_journal_credgrep=not performed (forbidden by contract)`, raw payload deliberately not
printed into Lead output. Accepted postcheck rc0 (`C:\WPI_ARTIFACTS\postcheck_gatea_a7_d.v2.out`,
stderr empty): evidence hash/bytes/markers, exact DISARMED API, production DB
quickcheck/appstate/schema, explicit evidence equality, journal count/bounds, current logs
regular/non-empty, service active/running PID189813, Restart=no, NRestarts0, one loopback listener.
The first postcheck passed API and production DB, then stopped because it over-strictly required the
current mutable `bridge.log` hash to equal A-7's point-in-time snapshot; independent GET status
checks append benign lines (1554 → 1616 → 1678 B, current hash at accepted v2 `d6bb3a2a…5b13ab`,
`bridge.err.log` unchanged at 597 B/same hash) — a verifier-design defect, not an A-7 failure. V2
validates the authoritative snapshot identity inside the immutable A-7 evidence and that current
logs are regular/non-empty, instead of demanding a live append-only log stay byte-identical; no raw
log content printed. Contract held: no `/api/arm`, env file not opened, no `/api/health`, no
credential grep or content, read-only production inspection.

- **[AI: Codex] NEXT:** preflight both accepted D A-8 scripts (`gatea_A8.sh` remote and
  `gatea_A8_host.ps1` Windows host) — exact hashes/syntax, remote and host evidence paths absent,
  service safe, required host/SSH connectivity — without executing A-8.
- **[AI: Codex] THEN:** update `_AI_MEMORY`, execute the preregistered A-8 remote+host sequence
  exactly once, preserve/hash both evidence logs, independently postcheck. Do not run A-9 on genuine
  A-8 FAIL.
- Gate state: **A-0..A-7 PASS; A-8..A-9 NOT RUN.** Record:
  `11_TRIAGE/GATE_A_A7_PASS_2026-08-09D.md`.

---

## GATE A — A-7 preflight PASS; execute preregistered A-7 D next (2026-08-09)

Lead-performed read-only A-7 preflight at checkpoint `cfccd617`; accepted candidate `2ce41e34`
unchanged. Remote D tar `/home/gatea/gatea-run-kit-20260808D-2ce41e34.tar` (SHA-256
`e8a52e3c…e0d3`, 71680 B) and extracted kit verify: seven SHA256SUMS members OK, A-7 syntax rc0,
A-7 script SHA-256 `1b3dd379…9445f` / 6191 B / CR0. A-7 evidence log absent. Production safe:
active/running PID189813, Restart=no/NRestarts0, one `127.0.0.1:8790` listener, exact HTTP200
credential-free DISARMED state_version1, all network/exchange/credential/ARM flags off.
Noninteractive command-family sudo preflight (protected output suppressed): installed-candidate
Python executable; DB path readable; both documented log files regular with stat/sha256sum;
journalctl works; only booleans/identities printed, no DB rows/log/journal/credential/env values.
First verifier stopped at generic `sudo -n -v` (`a password is required`) — verifier-design
defect, not an A-7 or sudo failure: timestamp validation is not a valid proxy for command-specific
NOPASSWD rules. No A-7 script ran. Only `sudo -n -v` removed, exact command families reran rc0
`A7_PREFLIGHT=PASS` (`C:\WPI_ARTIFACTS\preflight_gatea_a7_d.v2.out`, stderr empty).

- **[AI: Codex] NEXT:** execute A-7 exactly once with
  `bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A7.sh`.
- **[AI: Codex] AFTER A-7:** preserve/hash `/home/gatea/gatea-A7-20260808D.log`, inspect exact
  API/DB equality and log/journal evidence without exposing credential content, independently
  postcheck unchanged production safe state, record verdict, update memory before A-8. Do not run
  A-8 on genuine A-7 FAIL.
- Gate state: **A-0..A-6 PASS; A-7..A-9 NOT RUN** (A-7 not executed). Record:
  `11_TRIAGE/GATE_A_A7_PREFLIGHT_2026-08-09D.md`.

---

## GATE A — A-6 PASS under run-kit D; A-7 preflight next (2026-08-09)

A-6 executed exactly once at checkpoint `b8776ca6` with
`bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A6.sh`; SSH rc0, transport stdout/stderr
empty because the script redirects to its no-clobber evidence log. Evidence
`/home/gatea/gatea-A6-20260808D.log` preserved to `C:\WPI_ARTIFACTS\gatea-A6-20260808D.log`;
remote/local SHA-256 identical `75ed4262…488c`, 2007 B; exactly one `A-6 PASS`, one
`A6_TRAP_EXIT rc=0`, four `RESULT=PASS`, zero `A6_FAIL`/`RESULT=FAIL`. Production unchanged before
and after: active, MainPID189813, exact HTTP200 DISARMED, mode credential_free_disarmed,
state_version1, all network/exchange/credential/ARM flags off. Isolated temp app: engine present,
notifier_disabled=true, DISARMED, dry_run, reconcile_ready True/error None, queue depth 0,
queued_events_len 0, MockBroker connected orders0/fills0/position None, engine stopped,
`RESULT=PASS`; temp DB quick_check ok, app_state DISARMED, schema_version4. Scope is empty-broker
startup/no raise/no hang/no leftover queue — not queue-drain-under-load and not full reconcile
(schema4 baseline disables it). Temp `/home/gatea/gatea-A6-temp.FLfBfh` cleaned; postcheck found
zero `/home/gatea/gatea-A6-temp.*` leftovers. Accepted postcheck rc0
(`C:\WPI_ARTIFACTS\postcheck_gatea_a6_d.v2.out`, stderr empty): hash/bytes/markers, cleanup,
active/running PID189813, Restart=no, NRestarts0, one `127.0.0.1:8790` listener, exact
credential-free DISARMED API. The first postcheck attempted one extra out-of-contract read-only open
of `/var/lib/mtc-bridge/bridge.db` as unprivileged `gatea` after all prior assertions passed;
SQLite returned `unable to open database file` — a verifier permission defect, not an A-6 failure
(A-6 targets only its temp DB; production PID/API unchanged). That probe was removed and v2 passed;
A-7 itself preregisteredly uses sudo for the production persisted-state check. Hardening held: no
`/api/arm`, env file not opened, six process env keys removed/discarded before bridge imports with
no values printed/copied/persisted/retained, MockBroker `bars=[]` blocked credential resolver and
broker/exchange network, notifier absent/disabled bound into PASS.

- **[AI: Codex] NEXT:** independently verify accepted D kit A-7 identity/syntax, A-7 evidence log
  absent, service safe, and that preregistered A-7 sudo permissions are noninteractive/available
  without printing protected content; checkpoint memory before execution.
- **[AI: Codex] THEN:** execute A-7 exactly once with
  `bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A7.sh`, preserve/hash evidence,
  independently postcheck. Do not run A-8 on genuine A-7 FAIL.
- Gate state: **A-0..A-6 PASS; A-7..A-9 NOT RUN.** Record:
  `11_TRIAGE/GATE_A_A6_PASS_2026-08-09D.md`.

---

## GATE A — A-6 preflight PASS; execute preregistered A-6 D next (2026-08-09)

Lead-performed read-only A-6 preflight at checkpoint `e48cba48`; accepted candidate `2ce41e34`
unchanged. Remote D tar `/home/gatea/gatea-run-kit-20260808D-2ce41e34.tar` (SHA-256
`e8a52e3c…e0d3`, 71680 B) and extracted kit verify: seven SHA256SUMS members OK, A-6 syntax rc0,
A-6 script SHA-256 `4bd3cbc3…6625` / 13863 B / CR0. A-6 evidence log absent, no A-6 temp leftover.
Production safe: active/running PID189813, Restart=no/NRestarts0, one `127.0.0.1:8790` listener,
exact HTTP200 credential-free DISARMED state_version1, all external/ARM flags off; systemctl resolves
exactly `MTC_BRIDGE_START_MODE=credential_free_disarmed` (no secret/unrelated value printed). First
verifier stopped on `kill -0` "Operation not permitted" (root PID; read-only verifier defect, not a
Gate-A failure; no Gate-A script ran); replaced with `test -d /proc/189813`, rerun rc0
`A6_PREFLIGHT=PASS`.

- **[AI: Codex] NEXT:** execute A-6 exactly once with
  `bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A6.sh`.
- **[AI: Codex] AFTER A-6:** preserve/hash `/home/gatea/gatea-A6-20260808D.log`, independently verify
  no temp leftover and unchanged PID/service/listener/API, record verdict, update memory before A-7.
  Do not run A-7 on genuine A-6 FAIL.
- Gate state: **A-0..A-5 PASS; A-6..A-9 NOT RUN** (A-6 not executed). Record:
  `11_TRIAGE/GATE_A_A6_PREFLIGHT_2026-08-09D.md`.

---

## GATE A — A-5 PASS under E; A-6 preregistered D gate next (2026-08-09)

A-5 E executed once, rc0. Evidence remote/local SHA-256 `83d947a3…d19c`, 3284 B; old PID187338
died with MainPID0/no listener/NRestarts0, exactly one explicit start produced PID189813; readiness
active+loopback+exact DISARMED in 1.1s/2 attempts; post listener/API PASS; DB snapshot identical;
trap rc0. Independent postcheck confirms active/running, Restart=no/NRestarts0, one loopback
listener, exact credential-free DISARMED state_version1, all external/ARM flags off, DB invariant.

- **[AI: Codex] NEXT:** recover/verify the exact preregistered A-6 command and contract from accepted
  run-kit D; confirm A-6 log absent and live safe state, then execute A-6 only.
- **[AI: Codex] AFTER A-6:** preserve/hash evidence, independent postcheck, update memory before A-7.
- Gate state: **A-0..A-5 PASS; A-6..A-9 NOT RUN.** Record:
  `11_TRIAGE/GATE_A_A5_PASS_2026-08-09E.md`.

---

## GATE A — E transferred/remote-verified; safe preflight PASS; run A-5 once next (2026-08-09)

Remote tar hash, exact members, manifest, mode, syntax, LF/CR and Linux E regression GREEN 29/29 all
pass at `/home/gatea/gatea-run-kit-20260809E-2ce41e34`. Immediate preflight: E log absent; service
active/running PID187338, Restart=no, NRestarts=0; one loopback listener; exact HTTP200
credential-free DISARMED state_version1; arm/credentials/broker/exchange/network all off.

- **[AI: Codex] NEXT:** execute A-5 exactly once with
  `bash /home/gatea/gatea-run-kit-20260809E-2ce41e34/gatea_A5.sh`; preserve the E log.
- **[AI: Codex] AFTER RUN:** copy/hash evidence locally, independently postcheck service/listener/API,
  update memory. Stop A-6 on genuine FAIL; A-6 only after A-5 PASS and checkpoint.
- Record: `11_TRIAGE/GATE_A_A5_E_TRANSFER_2026-08-09.md`.

---

## GATE A — E package built and locally verified; transfer/re-verify next (2026-08-09)

Raw committed `b2c369f7` blobs produced
`C:\WPI_ARTIFACTS\gatea-run-kit-20260809E-2ce41e34.tar`, SHA-256
`895fe530f4fe85b9dc0c86332776899c88492197c2748c1de14f950f0e6f1cef`, 133120 B. Exact five-member
archive, manifest, LF/CR, modes and extracted bytes pass. Extracted package test: D RED 6/29,
pre-repair RED 28/29, E GREEN 29/29; Bash syntax and manifest rc0.

- **[AI: Codex] NEXT:** verify remote tar/extraction/E-log paths absent, transfer tar, verify tar
  hash, extract, verify members/manifest/mode/syntax and run extracted E local-only regression.
- **[AI: Any] HOLD:** update memory before A-5. No staging service action yet; A-5 FAIL;
  A-6..A-9 NOT RUN. Record: `11_TRIAGE/GATE_A_A5_E_PACKAGE_2026-08-09.md`.

---

## GATE A — accepted E integrated and pushed; raw-blob package next (2026-08-09)

Active `feature/donchian-crypto-ladder` fast-forwarded cleanly from `123bb0c4` to
`7453ea7ffb427d86d5d2a9a65143603873d18906` and pushed to origin. Accepted source remains exact
`b2c369f7`; later commits are audit/current-memory records only. No package, transfer, or staging
action yet.

- **[AI: Codex] NEXT:** build `gatea-run-kit-20260809E-2ce41e34` from raw committed kit blobs at
  `b2c369f7`, add SHA256SUMS, create deterministic tar, extract locally and re-run package-level
  D RED/pre-repair RED/E GREEN plus syntax/hash/LF/CR/member checks.
- **[AI: Any] HOLD:** update memory again before transfer. A-5 FAIL; A-6..A-9 NOT RUN.

---

## GATE A — run-kit E canonically ACCEPTED at `b2c369f7`; integrate/package next (2026-08-09)

Claude Opus 5 xhigh and Codex 5.6-sol xhigh both executed D RED 6/29, exact pre-repair E RED
28/29, repaired E GREEN 29/29, syntax/compile/hash/diff/clean checks and returned
**PASS-WITH-NITS** with zero required repairs. DeepSeek ClinePass is unavailable and GLM-5.2 could
not execute; both are supplemental BLOCKs with clean/no-finding static results. No unresolved
reproduced required finding. D025/D026 acceptance is satisfied for source `b2c369f7`.

- **[AI: Codex] NEXT:** fast-forward active `feature/donchian-crypto-ladder` to the accepted
  candidate/history and push; then build E from raw committed blobs and verify locally.
- **[AI: Codex] AFTER PACKAGE CHECKPOINT:** transfer/extract/re-verify on staging, update memory,
  confirm E log absent, then run A-5 exactly once. Stop on genuine FAIL; A-6 only after A-5 PASS
  and a new memory checkpoint.
- **[AI: Any] SAFETY:** A-5 remains FAIL until rerun; A-6..A-9 NOT RUN. Hard exclusions unchanged.
  Record: `11_TRIAGE/GATE_A_A5_E_CANONICAL_ACCEPTANCE_2026-08-09.md`.

---

## GATE A — round-3 canonical audits: Claude accepts; Codex evidence-capture rerun required (2026-08-09)

At frozen source `b2c369f7`: Claude Opus 5 xhigh executed all three cases and returned
**PASS-WITH-NITS**, zero required repairs. Codex 5.6-sol xhigh returned **PASS** but its final report
was one word and the wrapper discarded its execution transcript, so D025 execution cannot yet be
independently confirmed; do not count it as acceptance. DeepSeek ClinePass route is unavailable;
GLM-5.2 could not execute tools and returned BLOCK after clean static review. All worktrees clean.

- **[AI: Codex] NEXT:** fresh Codex xhigh audit in a new detached worktree with JSON execution
  transcript captured; require explicit D RED 6/29, `61d88f12` RED 28/29, E GREEN 29/29,
  syntax/compile, source/diff and clean status in the final evidence.
- **[AI: Any] HOLD:** no integration/package/transfer/staging. Repair budget exhausted.

---

## GATE A — final E source frozen at `b2c369f7`; four canonical audits running next (2026-08-09)

Lead-accepted round-3 source/test/docs are committed at
`b2c369f73abd3d90b17000e601c6f9cdc21c4cf1`; branch was clean immediately after commit. This is
the exact canonical audit target. No integration, push, package, transfer, or staging action yet.

- **[AI: Codex] RUN:** fresh Claude Opus 5 xhigh, Codex 5.6-sol xhigh, DeepSeek V4 Flash and
  GLM-5.2 audits at `b2c369f7`; require D RED 6/29, exact `61d88f12` RED 28/29, E GREEN 29/29,
  source/diff/syntax/compile and final cleanliness. Both flagship verdicts must accept.
- **[AI: Any] HOLD:** A-5 FAIL; A-6..A-9 NOT RUN. Repair budget exhausted.

---

## GATE A — final repair round 3 Lead re-audit ACCEPT; freeze and canonical audits next (2026-08-09)

Lead independently reproduced D RED 6/29, exact `61d88f12` RED 28/29 solely on the boundary check,
and repaired E GREEN 29/29. Existing 28 checks are preserved; equality/past-deadline success is
rejected; blocked child termination/no survivor, mutation timing, forbidden-command isolation,
syntax, compile, immutable D, scope and diff checks pass. A wording inconsistency was corrected
before freeze and E reran GREEN. Final identities: script `25066` B / `497` LF / CR0 /
`74161fb4…`; test `59469` B / `1265` LF / CR0 / `0e50ebb9…`; README `35289` B / `495` LF / CR0 /
`60bb9caf…`.

- **[AI: Codex] NEXT:** commit/freeze the exact repaired candidate; run fresh Claude Opus 5 xhigh,
  Codex 5.6-sol xhigh, DeepSeek V4 Flash and GLM-5.2 canonical audits at that SHA. Mandatory D RED,
  pre-repair RED, E GREEN and executable syntax/compile evidence; both flagship verdicts accepting.
- **[AI: Any] HOLD:** no integration/package/transfer/staging before canonical acceptance. A-5 FAIL;
  A-6..A-9 NOT RUN. Repair budget exhausted; any reproduced required source finding is hard stop.

---

## GATE A — final repair round 3 IMPLEMENTED (not accepted); Lead re-audit next (2026-08-09)

The reproduced boundary defect is repaired. `wait_ready_deadline`'s successful-probe branch now
recomputes `rem_ds=$(( deadline - now ))` after the post-probe monotonic reading and returns
failure when `rem_ds <= 0`. The equality boundary is stated once and applied identically at all
three guards — **`now >= deadline` is expiry** — which is the rule round 1 already used at the
other two. `READY_ELAPSED_DS`/`READY_ATTEMPTS` are set on every path; a late success takes the
ordinary expiry path (`fail()`, nonzero exit, no second start). Header now emits
`A5_kit_repair_round=3`. D→E diff still exactly 8 hunks; `fail "` sites still 24 (D) → 28 (E).

One focused named check added, **28 → 29**, nothing renamed/removed/weakened/skipped:
`behaviour_probe_success_at_or_after_deadline_is_rejected` — real wait/runner/probe with only
`mono_now_ds()` replaced by a scripted reading sequence, covering both the equality reading
(30 ds vs 30 ds) and the past-the-deadline reading (31 ds vs 30 ds).

D026 executed with the documented default commands, no PATH override, GNU coreutils 8.32:
exact pre-repair `61d88f12` blob materialized outside the repo → **RED 28/29** with the single
failure being the new check at `HARNESS_rc=0`; repaired E → **GREEN 29/29** rc 0; exact frozen
run-kit D control → **RED 6/29**. `bash -n` rc 0; `python -m py_compile` rc 0 with the
byte-cache outside the repo; `git diff --check` rc 0. All kit members UTF-8/LF, CR 0.

- **[AI: Claude] LEAD RE-AUDIT the actual files and evidence** — never this self-report. Rerun
  all three D026 runs (README §1, §1b, §2), `bash -n`, `python -m py_compile`, and re-hash the
  three kit members: `gatea_A5.sh` `25066` B / `497` LF / `74161fb4…`;
  `test_gatea_A5_readiness.py` `59469` B / `1265` LF / `0e50ebb9…`; `README.txt` `35289` B /
  `495` LF / `60bb9caf…`. The old script hash `fe06f79e…` is now the DEFECTIVE source and must
  never be packaged.
- **[AI: Claude] THEN FRESH CANONICAL AUDITS** per D025 in new detached worktrees with a normal
  Git Bash environment and writable temp/pycache. Every auditor must execute D RED, pre-repair
  RED and E GREEN; non-execution is BLOCK, never acceptance.
- **[AI: Claude] ONLY AFTER ACCEPTANCE:** commit, package from raw committed blobs (never a bare
  `git archive` on Windows), transfer to `/home/gatea/gatea-run-kit-20260809E-2ce41e34`, verify,
  then rerun A-5 once with `/home/gatea/gatea-A5-20260809E.log` confirmed absent.
- **[AI: Any] REPAIR BUDGET EXHAUSTED.** All three rounds are consumed. A further non-accepting
  source verdict is a hard stop — report to Barış, do not repair again.
- **[AI: Any] SAFETY STATE:** no staging action in this unit; no Git write, no integration, no
  package/transfer. Run-kit D and every D evidence artifact are immutable and untouched. A-5
  remains FAIL; A-6..A-9 NOT RUN. Record:
  `11_TRIAGE/GATE_A_A5_REPAIR_IMPLEMENTATION_2026-08-09E.md` §R3.

---

## GATE A — Codex REQUEST_CHANGES reproduced; final repair round 3 next (2026-08-09)

The executable Codex xhigh audit ran D RED/E GREEN 28/28 and found one required boundary defect:
after a successful bounded probe, E records a new monotonic time but returns success even when that
time is past the deadline. Lead reproduced exact frozen behavior with budget 1s and readings
`0,0,11`: SUCCESS, elapsed 11ds, rc0. Finding is binding.

**Next:** Claude Opus 5 final repair round 3: reject post-probe success beyond deadline; add a
focused D026 boundary RED/GREEN test; preserve every existing check and safety property; update
records. Then Lead re-audit and fresh canonical audits. No integration/package/transfer/staging.
A-5 FAIL; A-6..A-9 NOT RUN. A further non-accepting source verdict after round 3 is a hard stop.

---

## GATE A — Codex audit rerun 2 still environment-BLOCKED; unsandboxed read-only-intent rerun next (2026-08-09)

Codex xhigh rerun at clean detached `C:\GAEAX2` gained writable temp/pycache but its subprocess
sanitized PATH: Git coreutils were absent, `mkdir` failed, and Windows `timeout.exe` was selected;
E ended 18/28 and verdict stayed BLOCK. Lead then ran the exact no-PATH-edit commands in the same
worktree: D RED 6/28, E GREEN 28/28 with Git Bash and `/usr/bin/timeout` coreutils 8.32; status clean.

**Next:** third fresh Codex xhigh audit at frozen `61d88f12`, dedicated worktree, unsandboxed command
runtime under strict read-only instructions. Do not integrate/package/transfer/stage until Codex
executes and accepts. A-5 remains FAIL; A-6..A-9 NOT RUN.

---

## GATE A — E canonical audit round 1 BLOCK; fresh executable Codex audit next (2026-08-09)

Frozen E candidate `61d88f12054c`: Claude Opus 5 xhigh **PASS** after executing D RED and E GREEN
28/28. Codex 5.6-sol xhigh **BLOCK** because its assigned sandbox had no usable writable temp or
pycache and its fallback Bash exposed Windows `timeout.exe`; it could not complete mandatory E.
DeepSeek ClinePass was unavailable and GLM-5.2 execution was denied, so both are supplemental
BLOCKs with no required finding. All four detached audit worktrees are clean.

**Next:** fresh Codex 5.6-sol xhigh audit in a new detached worktree with writable temp/pycache and
normal Git Bash resolution. It must execute exact D RED/E GREEN, syntax/compile, inspect the frozen
diff, and prove cleanliness. Do not integrate, package, transfer, or touch staging before an
accepting Codex verdict. State: A-0..A-4 PASS; A-5 FAIL; A-6..A-9 NOT RUN. Record:
`11_TRIAGE/GATE_A_A5_E_CANONICAL_AUDIT_ROUND1_2026-08-09.md`.

---

## GATE A — E repair round 2 Lead re-audit ACCEPT; four fresh canonical audits next (2026-08-09)

Default exact D is RED; E is GREEN **28/28**, no PATH override. GNU timeout, hard deadline,
blocked-child termination/no survivor, mutation falsification, Bash syntax, pycompile, CR/hash/byte
and scope evidence reproduce. Lead preliminary **ACCEPT for audit dispatch**; E is not finally
accepted/packaged/transferred/run.

**Next:** freeze this exact candidate and run fresh independent Claude Opus 5 xhigh, Codex 5.6-sol
xhigh, DeepSeek V4 Flash and GLM-5.2 audits. Every auditor must execute default D RED/E GREEN;
non-execution is BLOCK. Flagship accepting verdicts plus no unresolved reproduced required finding
are mandatory. Gate state A-0..A-4 PASS, A-5 FAIL, A-6..A-9 NOT RUN; no staging action.

---

## GATE A — E REPAIR ROUND 2: deadline guard resolved through Bash; default-command RED/GREEN owed (2026-08-09)

**Accepted and repaired, in the local regression test only.** `find_timeout()` /
`shutil.which("timeout")` is deleted. `probe_deadline_guard(bash_exe)` now resolves and exercises
the guard **inside the Bash the test already selected**, over the **same `bash -s` stdin transport
the behavioural harness uses**, mirroring the script's own step1 guard: `command -v timeout`;
`timeout --version` must be rc `0` and name **GNU coreutils**;
`timeout --signal=TERM --kill-after=2 0.5 "${BASH:-bash}" -c 'sleep 30'` must return **`124`**; and
a path under a Windows `system32` directory is **rejected explicitly** (native and MSYS spellings).
**No `PATH` override is required, requested or accepted.** All **28** named checks preserved,
unrenamed and unrelaxed — the check got strictly stronger, nothing was weakened to make it pass.

**`gatea_A5.sh` untouched:** SHA-256 `fe06f79e…451380`, `22531` bytes, `466` LF lines — identical to
round 1, re-verified. New: test `67823a70…d59c8f` (`53208` B / `1164` L), README `56d68865…097d8`
(`29397` B / `415` L); CR count `0` on all three.

**NEXT ACTION — Lead, and it is the binding one.** Run both documented commands **exactly as
printed, from the repo root, with no `PATH` override and no other environment edit**:

```
python MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/test_gatea_A5_readiness.py --script MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/gatea_A5.sh   # MUST be RED / nonzero
python MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/test_gatea_A5_readiness.py --script MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/gatea_A5.sh   # MUST be GREEN / 0
```

Require `SUMMARY total=28`, `env_deadline_guard_available_and_working` PASS, and the four round-1
timing checks PASS; record the printed `bash=` line and the resolved `GUARD_bin` path. A GREEN that
needed a hand-edited `PATH` is **not** acceptance. Then re-audit the files directly (not this
self-report), re-verify the `gatea_A5.sh` hash above, and run the fresh `claude-opus-5` xhigh +
`gpt-5.6-sol` xhigh canonical audits.

**D026 BLOCK — this unit could not observe its own repair working.** `bash`, `bash -lc`, `bash -n`,
`python <script>`, `python --version` and `python -m py_compile` were all refused by the permission
layer, and filesystem access outside `C:\GA5E` is sandboxed off. The round-2 change is **reviewed,
not executed**; the Lead's round-1 pair does not close it, because its GREEN half needed the very
`PATH` override round 2 removes.

**State unchanged.** E is implemented locally and is **NOT accepted, NOT committed, NOT packaged,
NOT transferred, NOT run**. **A-0..A-4 PASS · A-5 FAIL (run-kit D) · A-6..A-9 NOT RUN.** Run-kit D
immutable and untouched; staging unchanged and safe; no Git, SSH/staging, package/transfer,
credential, broker, ARM, order or economic action. **Repair rounds 1 and 2 of 3 consumed — one
remains.**

---

## GATE A — E repair round 1 Lead re-audit REQUEST_CHANGES: Windows test resolves the wrong `timeout` (2026-08-09)

Default D remained RED. Default E returned RED with `27/28` PASS only because Python
`shutil.which("timeout")` selected `C:\Windows\system32\timeout.EXE`, not GNU coreutils. The
behavioral source checks all passed. With Git Bash `usr\bin` first on PATH, the exact E test returned
**28/28 PASS, RESULT=GREEN, rc0**: a 45 s API probe ended in 3.7 s under a 3 s deadline with no
surviving child; the pre-repair mutation took 18.8 s versus repaired E at 2.6 s.

**Lead verdict: REQUEST_CHANGES (repair round 2).** Resolve/run GNU `timeout` through the already
selected Bash environment, not Windows `shutil.which`; preserve all 28 checks; rerun the documented
default D RED/E GREEN; update E records/current memory; restore this file's prior CRLF convention to
avoid a whole-file line-ending diff. E remains unaccepted/uncommitted/unpackaged/untransferred/unrun;
A-5 FAIL; A-6..A-9 NOT RUN; no staging action.

---

## GATE A — E REPAIR ROUND 1: hard monotonic readiness deadline implemented; pending Lead re-audit + canonical audits (2026-08-09)

**The Lead's binding timing finding is accepted and repaired.** The counterpart flagship
implementer `claude-opus-5` rewrote the run-kit E readiness path in the isolated worktree
`C:\GA5E` on `codex/gatea-a5-readiness-e`, baseline `123bb0c4`. **E is implemented locally and
is NOT accepted, NOT committed, NOT packaged, NOT transferred, NOT run.** Gate state unchanged:
**A-0..A-4 PASS · A-5 FAIL (run-kit D) · A-6..A-9 NOT RUN.** Run-kit D and every D evidence
artefact are immutable and untouched; staging is unchanged and safe; no Git, SSH/SCP,
staging/service, package/transfer/deploy, credential, broker/exchange, ARM, order,
TESTNET/mainnet, wallet, merge or economic action was performed.

**Lead-run round-0 evidence, preserved exactly (this is what proved defect 1 closed and defect
2 open):** exact pre-fix D → `rc=1`, `RESULT=RED`, **14 checks / 3 PASS / 11 FAIL**, `152 ms`;
first E draft → `rc=0`, `RESULT=GREEN`, **14/14 PASS**, `7935 ms`; independent `bash -n` rc `0`
and `python -m py_compile` rc `0`; hashes/bytes/LF/CR-0 reproduced. **Binding finding:**
`retry 30 post_start_ready` was **attempt-count bounded, not time bounded** — `check_api`'s
`urllib.request.urlopen(..., timeout=10)` can consume ten seconds per attempt and `retry` sleeps
one second after each failure, so listener-present/API-stalled could run ≈ **330 s** while the
marker claimed a 30 s ceiling. The immediate-return stubs could not see it.

**The repair (replaces every false ceiling/attempt-count claim).** `retry 30 post_start_ready`
is gone from the post-start path. `wait_ready_deadline "$READY_MAX_S"` (`READY_MAX_S=30`
**seconds**) fixes a **monotonic wall-clock deadline** once, from `/proc/uptime`
(`CLOCK_BOOTTIME`), immediately after the single explicit start, and charges **probe duration
(active + listener + API) and the inter-attempt backoff against that one budget**. Every attempt
runs through `run_bounded` under GNU coreutils `timeout` with the **remaining** time as its hard
bound; without `--foreground` `timeout` signals the child's **whole process group**, so SIGTERM
at the bound — and SIGKILL `KILL_GRACE_S=2 s` later if the probe ignores SIGTERM — reaches the
probe shell **and every descendant** (venv python, its `ss`, a stalled socket read). **No probe
child can outlive the bound**, and a killed attempt only ever interrupts a read-only operation.
The backoff is clamped to the remaining budget. All three conditions still required in the same
attempt; step5 still re-runs the listener and API checks **in full, unsuppressed**, and the final
`check_api` keeps its own `timeout=10`. **Honest bound, stated identically everywhere:** returns
at 30 s monotonic, **plus at most 2 s** if a probe ignores SIGTERM, plus scheduler slop — not a
bare ceiling claim and not an attempt count. Four new step1 preconditions assert the mechanism
rather than assume it: `A5_ready_clock=proc_uptime`, non-empty `A5_timeout_bin`,
`A5_timeout_guard_rc=124`, `A5_ready_probe_export_rc=0`. New staging prerequisites: GNU
`timeout` on `PATH` and a readable `/proc/uptime` — both asserted, never assumed.

**Real diff evidence (this session, read-only):** `diff --strip-trailing-cr` D→E = **exactly
eight hunks** (`2c2`, `4a5,37`, `20c53,77`, `46a104,107`, `53c114,120`, `172a240,356`,
`188a373,392`, `229c433,434`); **exactly one D line replaced** (`retry 30 wait_active …`); the
`retry` helper's code byte-for-byte unchanged (comment-only truthfulness fix) and still used for
the cheap step3 dead-window wait; `fail "` sites D `24` → E `28` (24 preserved + 4 new guard
preconditions). CR count **0** for all three kit members and the preregistration. `wc -c -l`:
README `25117`/`359`, `gatea_A5.sh` `22531`/`466`, test `47557`/`1071`, preregistration
`27070`/`415`. SHA-256 `gatea_A5.sh`
`fe06f79e36432a8fa81e4a1c17dc470acd8d03099aa735faa76f737212451380`, test
`f5651aa6c6c7fc3e88958e4780c38c898fd1dc6d2ccf00828a4af2fc355713f2`, README
`8127afb360e4ce1f60cc695a3b2f64890049b079b21af9037630328fca237aee` (these **supersede** the
round-0 hashes, which now identify the discarded first draft). Ripgrep confirms the retired
strings `ready_max_wait_s` / `30 s maximum` / `30-second maximum` / `30 attempts` appear
**nowhere** in the script.

**D026 extended to falsify the timing defect behaviourally (28 named checks).** The test now
extracts the script's real constants block and its real `mono_now_ds` / `run_bounded` /
`ready_probe_once` / `wait_ready_deadline` definitions and runs them against stubs, including a
stub probe that blocks far past the deadline. Two scenarios form the falsification pair, run
inline on **every** invocation with identical stubs and an identical nominal bound:
`mutation_pre_repair_attempt_count_wait_violates_deadline` drives the **verbatim pre-repair
wait** (the script's own `retry` helper + the old `post_start_ready`) against an 8 s-blocking API
stub with a nominal bound of 2 and requires it to be **measured overrunning** it (≈ 17 s), while
`behaviour_repaired_deadline_beats_pre_repair_on_same_stub` requires the repaired wait to exit
nonzero at the deadline in under half that time. `behaviour_deadline_terminates_blocked_probe`
(45 s probe, 3 s deadline, ≤ 9 s exit) and `behaviour_no_probe_child_survives_deadline` (the
probe process must be **gone**) prove termination rather than waiting-it-out.
`env_deadline_guard_available_and_working` makes non-execution visible: missing/non-functional
GNU `timeout` ⇒ **RED**, never an unearned green (D025 rule 1). Forbidden commands are shadowed
**twice** (exported functions **and** PATH shims) and every shim writes to a log the harness
reports, so suppression cannot hide one.

**HONEST BLOCK — round-1 D026 evidence is still owed.** `bash`, `bash -n`, `python <script>`,
`python -c` and `python -m py_compile` are all outside this session's permission allowlist —
every attempt returned `This command requires approval` via both the Bash and PowerShell tools
(only `python --version` → `3.14.2` was permitted). **The repaired script and the extended test
have never been executed.** Per D026 the extended test is **supplemental — not closure
evidence**, and **the timing defect is NOT closed.** Exact commands + binding pass criteria:
`11_TRIAGE/GATE_A_A5_REPAIR_IMPLEMENTATION_2026-08-09E.md` §8.

**Next steps:**

- **[AI: Claude] RUN THE ROUND-1 D026 EVIDENCE FIRST.** `RED` (nonzero, `RESULT=RED`) against
  the exact frozen pre-fix D script and `GREEN` (exit 0, `RESULT=GREEN`) against repaired E,
  plus `bash -n` on E and `python -m py_compile` on the test. GREEN is only evidence if
  `mutation_pre_repair_attempt_count_wait_violates_deadline`,
  `behaviour_repaired_deadline_beats_pre_repair_on_same_stub`,
  `behaviour_deadline_terminates_blocked_probe`, `behaviour_no_probe_child_survives_deadline`
  and `env_deadline_guard_available_and_working` all individually PASS. Allow ≈ 30–45 s per
  GREEN run. **If GREEN fails, the finding is real — repair the source, do not weaken the test.**
- **[AI: Claude] LEAD RE-AUDIT the actual files and evidence** — never this self-report.
  Reproduce the diff/hash/byte/CR evidence and check that the script, marker, failure reason,
  README, preregistration, implementation record and these memory sections all state the **same**
  bound.
- **[AI: Claude] THEN FRESH CANONICAL AUDITS** per D025: new independent sessions,
  `claude-opus-5` effort `xhigh` **and** `gpt-5.6-sol` effort `xhigh` (protected surface).
  Non-execution ⇒ **BLOCK**; any reproduced required finding from any canonical auditor is
  binding. **Repair round 1 of 3 is consumed.**
- **[AI: Claude] ONLY AFTER ACCEPTANCE:** commit, package **from raw committed blobs**
  (`git cat-file blob`, never a bare `git archive` on Windows), verify LF/CR-0 + per-member
  SHA-256/bytes + member set + tar hash/size/count, transfer, extract to the **new**
  `/home/gatea/gatea-run-kit-20260809E-2ce41e34`, re-verify remotely, **confirm `command -v
  timeout` and a readable `/proc/uptime` on the VM**, confirm `/home/gatea/gatea-A5-20260809E.log`
  is absent, then rerun **A-5 only**, once. A-6 stays blocked until A-5 PASSES and `_AI_MEMORY`
  is updated.
- **[AI: Any] SAFETY STATE:** no staging action occurred in this unit. Run-kit D and its evidence
  (`/home/gatea/gatea-A5-20260808D.log`, SHA-256
  `3e282516dfea7e66d9196ad5f3d929b7d1a50257bae501a5b89c35e007eb31c9`, `1933` bytes) remain
  immutable; the service remains active/static, loopback-only, credential-free DISARMED,
  `state_version=1`, `Restart=no`; no ARM, credential, broker/exchange, order, TESTNET/mainnet,
  wallet, merge or economic action.

---

## GATE A — E Lead audit REQUEST_CHANGES: D026 reproduced, but the claimed 30-second bound is false (2026-08-09)

**Codex Lead independently reproduced the new test and inspected the real D→E diff.** D026 is now
real evidence: exact pre-fix D returned `rc=1`, `RESULT=RED` (`14` checks: `3` PASS, `11` FAIL;
`152 ms`); E returned `rc=0`, `RESULT=GREEN` (`14/14` PASS; delayed listener/API became ready on
attempt 3 after 2 s; active-only timed out under test bound 3; listener-up/API-not-exact timed out
under bound 2; no forbidden command ran). Independent `bash -n` and `python -m py_compile` both
returned `0`; all three kit members and both new reports are UTF-8/LF with CR count `0`; reported
hashes/bytes reproduce.

**Lead verdict: REQUEST_CHANGES (repair round 1).** `gatea_A5.sh` and all current E docs claim
`retry 30 post_start_ready` is a **30-second maximum**, but `post_start_ready` calls the existing
`check_api`, whose `urllib.request.urlopen(..., timeout=10)` can block for 10 seconds per attempt.
The existing `retry` also sleeps one second after every failed attempt. If the listener is present
but the API stalls, 30 attempts can take roughly **330 seconds**, so both the safety bound and
`A5_READY ... ready_max_wait_s=30` evidence are false. The current regression stubs return
immediately and do not detect this timing defect. E remains unaccepted/uncommitted/unpackaged/
untransferred/unrun; A-5 remains FAIL and A-6..A-9 remain NOT RUN.

**Next steps:**

- **[AI: Claude] REPAIR ROUND 1:** enforce a real monotonic 30-second wall-clock deadline that
  includes listener/API attempt time; bound each readiness API probe by the remaining deadline;
  preserve the full final API check at its existing timeout and every D assertion; no second start.
- **[AI: Claude] EXTEND D026:** add a behavioral slow/hanging-API scenario that would exceed the
  deadline under the current attempt-count implementation and proves the repaired wait exits
  nonzero at the wall-clock bound. Demonstrate RED on the current E and GREEN after repair.
- **[AI: Claude] UPDATE** the E README, preregistration, implementation record, and current memory/
  handoff sections with real commands/output and truthful timing semantics. Then Lead re-runs the
  complete evidence before fresh canonical audits.
- **[AI: Any] SAFETY STATE:** no staging action occurred in this unit. Run-kit D/evidence remain
  immutable; service remains active/static, loopback-only, credential-free DISARMED; no ARM,
  credential, broker/exchange, order, TESTNET/mainnet, wallet, merge, or economic action.

---

## GATE A — A-5 readiness repair E IMPLEMENTED LOCALLY; D026 RED/GREEN still owed; pending Lead inspection + canonical audit (2026-08-09)

**Protected run-kit repair by the counterpart flagship implementer `claude-opus-5`** in the
isolated worktree `C:\GA5E` on branch `codex/gatea-a5-readiness-e`, baseline `123bb0c4`
(`123bb0c49129b29f625fb0c922968ddf8feaed06`). **Revision E is implemented locally and is NOT
packaged, NOT transferred, NOT audited, NOT accepted, NOT run.** Gate state unchanged:
**A-0..A-4 PASS · A-5 FAIL (run-kit D) · A-6..A-9 NOT RUN.** Candidate `2ce41e34…` and the
product/artifact are unchanged. No Git command, SSH/SCP, staging/service operation,
package/transfer/deploy, broker/exchange, ARM, order, TESTNET/mainnet, wallet, credential read,
or economic action was performed. Run-kit D and its evidence were not edited. Standalone
records: `11_TRIAGE/GATE_A_A5_REPAIR_IMPLEMENTATION_2026-08-09E.md` (implementation + limits)
and `11_TRIAGE/GATE_A_A5_REPAIR_PREREGISTRATION_2026-08-09E.md` (E paths, acceptance criteria,
invocation, first-FAIL, package/transfer requirements).

**What E is.** An **A-5-only repair kit**, `11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/`
(`README.txt`, `gatea_A5.sh`, `test_gatea_A5_readiness.py`). It supersedes run-kit D **for the
A-5 rerun only**; **A-6..A-9 remain NOT RUN and remain governed by the accepted run-kit D
source** until A-5 PASSES and `_AI_MEMORY` is updated. New no-clobber evidence log
`/home/gatea/gatea-A5-20260809E.log`; planned new remote path
`/home/gatea/gatea-run-kit-20260809E-2ce41e34`. The frozen D log
`/home/gatea/gatea-A5-20260808D.log` is never overwritten or reused.

**The repair.** After the single explicit `sudo systemctl start` and before the step5 post
assertions, `retry 30 post_start_ready` performs a bounded **30 s maximum** readiness wait that
is satisfied only when **all three** hold in the **same attempt**: systemd `ActiveState=active`
(`wait_active`) **plus** a nonempty loopback-only `:8790` listener set
(`check_listener_loopback_only`) **plus** `GET /api/status` HTTP 200 exact credential-free
DISARMED (`check_api`). It returns nonzero at the first failing check, so `ActiveState=active`
alone can never satisfy the wait. Only per-attempt diagnostics are suppressed; step5 re-runs
both checks **in full, unsuppressed**. On timeout: explicit `fail`, nonzero exit, **no second
start**, no auto-restart/mask. One structured marker `A5_READY=yes …` on success. Real `diff`
proves E differs from frozen D in exactly six hunks (header wording, E scope block, `LOG=`, two
header echoes, the readiness function, the retry/marker replacement); `fail "` sites unchanged
at 24 in both.

**Evidence produced:** `diff` D→E (six hunks); `fail "` parity 24/24; CR bytes **0** for all
three kit E members and both new reports; `wc -c -l` README 16847/254, `gatea_A5.sh` 12960/309,
test 23140/580; SHA-256 `gatea_A5.sh`
`2a8521b66eef00a58b1cde07342dcf812a3d1640d5b439f567512d944c604066`, test
`a32f85fc3ab9341029c31627876346db19e0c4704de9a317f181371c9ee2aa22`, README
`bdd638475bb971bfbafd8bb877b5d3ccb5e6922d18b9dbbf2ebcca104f6ce727`.

**HONEST GAP — D026 NOT SATISFIED.** The **RED and GREEN runs were NOT executed**: `bash` and
`python <script>` are outside this session's Bash-tool permission allowlist (every attempt
returned `This command requires approval`; read-only `diff`/`sha256sum`/`wc`/`grep` were
allowed, `python --version` → 3.14.2 was allowed). `bash -n` on E and `python -m py_compile` on
the test were blocked for the same reason. Per `AGENTS.md` D026 the new test is therefore
**supplemental — NOT closure evidence**, and **the readiness defect is NOT closed**. The two
exact closing commands and the expected output are recorded in
`GATE_A_A5_REPAIR_IMPLEMENTATION_2026-08-09E.md` §8.

**Failed-D evidence being repaired (unchanged, exact):** remote
`/home/gatea/gatea-A5-20260808D.log` and local `C:\WPI_ARTIFACTS\gatea-A5-20260808D.log`, both
SHA-256 `3e282516dfea7e66d9196ad5f3d929b7d1a50257bae501a5b89c35e007eb31c9`, `1933` bytes; after
systemd-active the immediate post listener check saw `listener_count=0` → `RESULT=FAIL` →
`A5_FAIL reason=post listener not loopback-only`, trap `rc=1`; an independent safe-state proof
seconds later found active/running `PID187338`, listener exactly `127.0.0.1:8790`, exact
credential-free DISARMED API, DB `quick_check=ok` / `app_state=DISARMED` / `schema_version=4`
with unchanged counts (`POSTFAIL_SAFE_STATE=PASS`). Diagnosis: **reproduced run-kit readiness
race, not a product persistence/DISARMED invariant failure.** Staging remained safe, so **no
conditional stop/mask was required or performed.**

**Next steps contract:**

- **[AI: Claude] PRODUCE THE D026 EVIDENCE FIRST.** Grant/obtain local execution and run the two
  commands in `GATE_A_A5_REPAIR_IMPLEMENTATION_2026-08-09E.md` §8 — **RED** (nonzero,
  `RESULT=RED`) against the exact frozen pre-fix D `gatea_A5.sh` and **GREEN** (exit 0,
  `RESULT=GREEN`) against E — plus `bash -n` on E `gatea_A5.sh` and `python -m py_compile` on the
  test. Record real commands, exit codes and output into §8. If the real GREEN run fails, the
  finding is real: repair the code, **do not adjust the test to make it pass.**
- **[AI: Claude] LEAD INDEPENDENTLY INSPECT** the **actual E diff and files** — never this
  self-report — and reproduce the RED/GREEN, `bash -n`, compile, CR-byte, byte-count and SHA-256
  evidence yourself.
- **[AI: Claude] RUN FRESH CANONICAL AUDITS** required by `AGENTS.md` for this protected repair:
  new independent sessions, `claude-opus-5` effort `xhigh` **and** `gpt-5.6-sol` effort `xhigh`
  (protected surface ⇒ xhigh). D025 binds: an auditor that cannot execute the checks must return
  **BLOCK**; **any reproduced required finding from any canonical auditor is binding**; max 3
  repair/re-audit rounds. This is a **new runtime-defect repair unit** — the three prior run-kit D
  source-review rounds do **not** cover it.
- **[AI: Claude] ONLY AFTER AN ACCEPTING AUDIT:** build the package **from raw committed blobs**
  (`git cat-file blob`) — **not** a bare `git archive` on Windows, which exported CRLF and was
  rejected in the D round — then verify LF/CR-0, per-member SHA-256 + bytes, the exact member set
  (`README.txt`, `gatea_A5.sh`, `test_gatea_A5_readiness.py`, `SHA256SUMS`) and the tar
  hash/size/member count; transfer, extract and re-verify under the **new** remote path
  `/home/gatea/gatea-run-kit-20260809E-2ce41e34`. **Never overwrite D evidence.**
- **[AI: Claude] RERUN A-5 (E) ONLY**, once, with `/home/gatea/gatea-A5-20260809E.log` confirmed
  absent; only `gatea_A5.sh` ever runs on staging (the test is local-only). **Preserve all D
  evidence. Stop on first genuine FAIL** and perform the preregistered first-FAIL response.
  **A-6 remains BLOCKED** until A-5 PASSES **and** `_AI_MEMORY` plus
  `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` are updated.
- **[AI: Any] STATE.** Candidate `2ce41e34…` and the product/artifact unchanged; no gate result
  beyond A-0..A-4 PASS and A-5 FAIL. Hard exclusions unchanged: no credentials, broker/exchange
  access, successful ARM, orders, TESTNET/mainnet, wallet, master merge, or economic action. The
  service remains active/static, loopback-only, credential-free DISARMED, `state_version=1`, no
  broker/credentials.

---

## GATE A — A-5 FAIL (run-kit D): reproduced post-start readiness race; staging safe; protected run-kit repair next (2026-08-09)

**Bounded documentation checkpoint by GLM-5.2 — records the Lead-performed A-5 staging execution +
read-only diagnostics only.** A-5 ran exactly once from
`/home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A5.sh` over the preregistered key-only SSH route
and returned a genuine **exit `1`** (elapsed about `4.7 s`). **Verdict (honest): A-0..A-4 PASS ·
A-5 FAIL · A-6..A-9 NOT RUN.** The frozen script's `wait_active` returned on systemd-active and then
immediately asserted the post-start loopback listener, which the application had not yet bound
(`listener_count=0` → `RESULT=FAIL` → `A5_FAIL reason=post listener not loopback-only`; trap `rc=1`).
A-5 **cannot be promoted to PASS** from later diagnostics. **Lead diagnosis: reproduced run-kit
readiness-race defect** — the kit lacks a bounded application-readiness wait after the explicit
`start`; it is **not** a product persistence/DISARMED invariant failure (store stayed `DISARMED` /
`schema_version=4`, counts unchanged, `state_version=1`, unit reached `Result=success`, listener came
up loopback-only). Full standalone record:
`11_TRIAGE/GATE_A_A5_FAIL_2026-08-09D.md`.

**Evidence identity (exact):**
- Remote evidence log `/home/gatea/gatea-A5-20260808D.log`; local preserved copy
  `C:\WPI_ARTIFACTS\gatea-A5-20260808D.log`; both SHA-256
  `3e282516dfea7e66d9196ad5f3d929b7d1a50257bae501a5b89c35e007eb31c9`, `1933` bytes; remote mode
  `664`, owner/group `gatea`.
- Independent preflight immediately before A-5 PASS: evidence log absent; `gatea_A5.sh: OK` vs
  `SHA256SUMS`; service active/static, `Restart=no`, `MainPID=183225`, `NRestarts=0`,
  `Result=success`, `ExecMainStatus=0`; listener exactly `127.0.0.1:8790`; API HTTP 200 exact
  credential-free DISARMED, mode `credential_free_disarmed`, `state_version=1`,
  network/exchange_conn/credential_lookup disabled, `exchange_enabled=false`, `arm_enabled=false`;
  DB `quick_check=ok`, `app_state=DISARMED`, `schema_version=4`.
- A-5 in-script: all pre-checks PASS; frozen authorized SIGKILL
  (`sudo systemctl kill --kill-whom=main --signal=SIGKILL mtc-bridge-first-start.service`); dead-window
  proof PASS (MainPID0, old PID gone, 3 s wait, ActiveState failed, no listener, NRestarts 0,
  Result signal, ExecMainStatus 9); exactly one `reset-failed`+`start`; post `MainPID=187338`,
  `NRestarts=0`, `Restart=no`; then the failing post-start listener check (`listener_count=0`).
- Independent post-failure verification a few seconds later PASS: unit loaded/static, active/running,
  `MainPID=187338`, `Restart=no`, `NRestarts=0`, `Result=success`, `ExecMainCode=0`,
  `ExecMainStatus=0`; listener count 1 exactly `127.0.0.1:8790`, non-loopback 0; API exact
  credential-free DISARMED, same `state_version=1` and disabled fields; DB `quick_check=ok`,
  `app_state=DISARMED`, `schema_version=4`, exact same table counts as preflight;
  `POSTFAIL_SAFE_STATE=PASS`. Because staging was independently proven safe, active, loopback-only,
  credential-free DISARMED, and DB-consistent, **the conditional stop/mask response was not required
  and was not performed.**

**Next steps contract — protected run-kit repair (`[AI: Claude]`):**

- **[AI: Claude] REPAIR A-5 IN A NEW RUN-KIT REVISION** (do not mutate the preserved remote D
  kit/log `/home/gatea/gatea-A5-20260808D.log`): add a bounded post-start readiness wait requiring
  systemd active **plus** loopback listener **plus** exact credential-free DISARMED API before the
  final assertions.
- **[AI: Claude] APPLY D026** (`AGENTS.md`): demonstrate RED against the exact readiness-race
  behavior or an equivalent deliberate falsification/mutation, then GREEN with the fix; record
  commands and real output.
- **[AI: Claude] INDEPENDENT AUDIT** of the actual repair and protected surface under the canonical
  roster / Lead acceptance rules — this is a new runtime-defect repair unit; the prior three
  source-review rounds do **not** count as testing this runtime defect.
- **[AI: Claude] PREREGISTER / PACKAGE / TRANSFER A NEW REVISION** with a new evidence-log identifier
  (for example revision E); verify hashes/bytes/LF/member set before any rerun. **Do not overwrite D
  evidence.**
- **[AI: Claude] RERUN A-5 ONLY** after the repaired revision is accepted and staged; **stop again on
  any genuine FAIL.** **A-6 remains blocked** until A-5 passes and memory is updated.
- **[AI: Any] STATE.** Candidate `2ce41e34…` and the product/artifact unchanged; no gate result
  beyond A-0..A-4 PASS and A-5 FAIL. Hard exclusions unchanged: no credentials, broker/exchange
  access, successful ARM, orders, TESTNET/mainnet, wallet, master merge, or economic action. The
  service remains active/static, loopback-only, credential-free DISARMED, `state_version=1`, no
  broker/credentials.

---

## GATE A — run-kit D packaged, transferred, extracted, and verified; A-5 first next (2026-08-09)

**Bounded documentation checkpoint by GLM-5.2 — records the Lead-performed package/transfer/verify
unit only.** The Lead-accepted run-kit D source was packaged, transferred to `gatea-staging`,
extracted, and independently re-verified. **A-0..A-4 remain PASS; A-5..A-9 remain NOT RUN.** **No
Gate-A script ran** during packaging, transfer, extraction, or verification. No product code or
product artifact changed; no credential, broker/exchange access, successful ARM, order,
TESTNET/mainnet, wallet, master merge, or economic action is authorized or occurred. Full standalone
record: `11_TRIAGE/GATE_A_RUN_KIT_D_PACKAGE_TRANSFER_2026-08-09.md`.

**Package identity (exact):**
- Accepted tar `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34.tar`, SHA-256
  `e8a52e3cdeaa9da9315d0cbeb1fde7dd75e9ecc8a4ad4c926e4084c37c55e0d3`, `71680` bytes; 9 tar members
  (root + 8 files); 8 extracted files; 7 manifest lines; all hashes verified; all members CR=0.
- A first `git archive` attempt exported CRLF and was **rejected before transfer**, preserved at
  `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34.rejected-crlf.tar` (SHA-256
  `66ce7a1e148d17626f68962ccdd3bb6bcacdf4c49a6eb815713caa64899634a8`, `71680` bytes). The accepted
  package was rebuilt from raw committed blobs with `git cat-file blob` (no worktree/archive
  line-ending conversion).
- Transferred to `/home/gatea/gatea-run-kit-20260808D-2ce41e34.tar` (same SHA-256/bytes/member set)
  and extracted to `/home/gatea/gatea-run-kit-20260808D-2ce41e34`. A clean remote re-verification
  passed: 7 manifest members verified; `bash -n` for A5/A6/A7/A8/A9; file count 8; manifest lines 7;
  every file CR=0; byte/LF counts and embedded-Python-block compiles match the standalone record.
- **Transport defect recorded, not concealed:** the first remote verifier had a PowerShell-to-SSH
  quoting defect (`test: \\8: integer expression expected`) after extraction; no Gate-A script ran —
  a verifier transport defect, not a package or Gate-A failure. The clean re-verification then passed.
- Staging remained safe and unchanged: service active/static, exact credential-free DISARMED, no
  credentials, no broker, state version 1.

**Next steps contract — A-5 first:**

- **[AI: Claude] EXECUTE A-5 ONLY** from `/home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A5.sh`.
  Preserve and inspect `/home/gatea/gatea-A5-20260808D.log`; independently verify
  service/API/DB/listener/systemd state before assigning a verdict. This is the next executable
  action because it is protected staging verification.
- **[AI: Claude] STOP ON FIRST GENUINE FAIL** and perform the preregistered safe response
  (`11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` §5); **do not run A-6.**
- **[AI: Claude] IF A-5 PASSES,** update the relevant `_AI_MEMORY` files before starting A-6.
- **[AI: Claude] CONTINUE ONE GATE AT A TIME** under the existing preregistration (A-5 → A-6 → A-7 →
  A-8 remote+host → A-9), updating `_AI_MEMORY` (`NEXT_STEPS.md`, `GLOBAL_HANDOFF.md`) and
  `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` before each next gate.
- **[AI: Any] STATE.** Candidate `2ce41e34…` and the product/artifact unchanged; no gate result
  beyond A-0..A-4 PASS. Hard exclusions unchanged: no credentials, broker/exchange access, successful
  ARM, orders, TESTNET/mainnet, wallet, master merge, or economic action. The service intentionally
  remains active/static, loopback-only, credential-free DISARMED, `state_version=1`, no
  broker/credentials — the prerequisite for A-5.

---

## GATE A - run-kit D source ACCEPTED by Lead; package/transfer checkpoint next (2026-08-08)

**Lead final verdict: ACCEPT.** The third/final repair round is independently accepted. All five
Bash scripts pass `bash -n`; the A-8 PowerShell parser reports zero errors; every embedded Python
heredoc compiles; `git diff --check` is clean; all new kit/preregistration files are LF-only with
zero CR bytes. Lead inspection against the accepted installed candidate confirms exact local-address
column parsing, nonzero failure exits, pre-import environment isolation, disabled notifier, bounded
non-recursive temp cleanup, explicit API-vs-DB equality, dual-sided A-8 reachability proof, and
content-redacted nine-category A-9 scanning. **A-5..A-9 remain NOT RUN.** Nothing is packaged,
transferred, or executed yet; no product/artifact or prohibited surface changed.

- **[AI: Claude] PACKAGE RUN-KIT D.** Copy the seven accepted source members to a new external
  `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34` directory, generate `SHA256SUMS`, create the
  tar, and independently verify member set, hashes, syntax, and LF bytes. Preserve run-kits B/C.
- **[AI: Claude] TRANSFER + VERIFY ONLY.** Transfer the D tar to `gatea-staging`, verify tar hash,
  member set, manifest, `bash -n`, and extraction path. Do not execute A-5 in the same unit.
- **[AI: Any] MEMORY CHECKPOINT.** Record package/transfer evidence in `_AI_MEMORY` before A-5.
- **[AI: Claude] THEN EXECUTE A-5 FIRST.** Stop at the first genuine FAIL; after PASS update
  `_AI_MEMORY` before A-6. Hard exclusions remain credentials, broker/exchange access, successful
  ARM, orders, TESTNET/mainnet, wallet, master merge, and economic action.

## GATE A — run-kit D A-6/A-7 repair round 3 (Lead-audit repair round 3); NOT RUN; bindings await Lead final acceptance (2026-08-08)

**Final focused GLM-5.2 repair round — same worktree and unit as rounds 1-2.** Edited only the
task-named files: `11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/gatea_A6.sh` + `gatea_A7.sh` + `README.txt`,
the preregistration doc `11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` (new §13), and these
three memory/handoff prepends. **A-5..A-9 are NOT RUN.** No product code/artifact changed; no new
files/Git/SSH/staging/execution/product edits/credentials/ARM/orders/broker-network access/
packaging/transfer. No gate result is claimed. The round-3 bindings await the Lead's final
acceptance; worker validation beyond the provided Lead evidence is not claimed.

Round-3 repairs: (1) **A-6 pre-import env isolation** — the six keys (`HL_ACCOUNT_ADDRESS`,
`HL_API_WALLET_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `MTC_BRIDGE_START_MODE`,
`MTC_BRIDGE_STATE_DB`) are popped via `os.environ.pop` BEFORE `from bridge.app import create_app` /
`from bridge.broker.mock import MockBroker` and before explicit app construction (order: stdlib
imports + release `sys.path`; pop loop; then bridge imports; then `create_app(...)`), so even
module-level default app construction cannot see the parent values; (2) **A-6 wording** —
`os.environ.pop` removes and discards process-local values; no value is printed/copied/persisted/
retained; it is NOT claimed the values are "never read"; Gate-A preconditions already established
the keys absent (clearing is defense in depth); the env FILE is not opened by A6 (A-9 keeps its
truthful statement: scans bytes but emits paths/counts only); (3) **A-7 explicit equality** — after
separately validating API state and DB `app_state`, A-7 explicitly asserts and records
`db_app == api_state` (not merely the two DISARMED checks); on mismatch it exits nonzero; all
existing A-7 checks preserved. Lead re-audit evidence (supplied; syntax/compile only — worker did
not run it): `bash -n` all 5 rc 0; PS parser 0; `git diff --check` clean; every embedded Python
heredoc compiled (A-5 3, A-6 3, A-7 2, A-8 1). Round-2 lifecycle/sidecar/notifier work accepted.
Full record: `GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` §13; ops:
`GATE_A_RUN_KIT_D_2026-08-08/README.txt`.

- **[AI: Any] NEXT ACTION UNCHANGED.** Before A-5 the Lead must independently validate the scripts
  (`bash -n` each `.sh`; PowerShell parser for `gatea_A8_host.ps1`; CR-byte = 0; `git diff --check`),
  create the manifest + tar, transfer to `/home/gatea`, and verify; then A-5 first, strict order,
  stop at first FAIL. The round-3 A-6/A-7 bindings are part of that Lead final acceptance.
- **[AI: Any] STATE.** No product/artifact change; no gate result; no prohibited action. The service
  remains active/static, loopback-only, credential-free DISARMED, `state_version=1`, no
  broker/credentials. Hard exclusions unchanged.

---

## GATE A — run-kit D A-6 repair round 2 (Lead-audit repair round 2); NOT RUN; bindings await Lead re-audit (2026-08-08)

**Bounded GLM-5.2 follow-up — repairs exactly the three remaining REQUIRED A-6 defects in
`gatea_A6.sh` only.** A5/A7/A8/A8_host/A9 are unchanged. Only the task-named files were edited:
`11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/gatea_A6.sh` + `README.txt`, the preregistration doc
`11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` (new §12), and these three memory/handoff
prepends. **A-5..A-9 are NOT RUN.** No product code/artifact changed; no packaging/transfer/install/
service mutation, credential, broker/exchange access, successful ARM, order, TESTNET/mainnet, wallet,
master merge, or economic action occurred. No gate result is claimed. The round-2 bindings await the
Lead's final re-audit; worker validation beyond the provided Lead evidence is not claimed.

Round-2 A-6 repairs: (1) **partial-start cleanup** — `stop_required` is set immediately BEFORE
`engine.start()`, so `finally` always attempts `await engine.stop()` whenever start was invoked
(including after a timeout/start exception); a stop exception stays nonzero, and if start already
failed the original start exception is preserved while the stop failure is still recorded (no false
PASS); (2) **SQLite sidecar cleanup** — strict target validation (exact `/home/gatea/gatea-A6-temp.`
prefix + EXACTLY six alphanumeric mktemp chars, real directory, not a symlink), then delete only
maxdepth-1 REGULAR files named exactly `bridge.db` / `bridge.db-wal` / `bridge.db-shm`, require no
entries remain, then `rmdir` (never recursive; invalid target or residue forces nonzero) so a valid
run no longer falsely fails on leftover WAL/SHM sidecars; (3) **notifier/outbound hardening** —
before `create_app`, `HL_ACCOUNT_ADDRESS`, `HL_API_WALLET_KEY`, `TELEGRAM_BOT_TOKEN`,
`TELEGRAM_CHAT_ID`, `MTC_BRIDGE_START_MODE`, `MTC_BRIDGE_STATE_DB` are popped from the isolated
process env without reading/printing any value; explicit `start_mode='credentialed'`, explicit temp
`store_path`, and injected `MockBroker(bars=[])` are passed; `engine.notifier is None or
engine.notifier.enabled is False` is required, only `notifier_disabled=true/false` is printed, and
it is bound into the PASS assertion (no env value printed). STATUS unchanged: A-5..A-9 NOT RUN, not
packaged/transferred. Full record: `GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` §12; ops:
`GATE_A_RUN_KIT_D_2026-08-08/README.txt`.

- **[AI: Any] NEXT ACTION UNCHANGED.** Before A-5 the Lead must independently validate the scripts
  (`bash -n` each `.sh`; PowerShell parser for `gatea_A8_host.ps1`; CR-byte = 0; `git diff --check`),
  create the manifest + tar, transfer to `/home/gatea`, and verify; then A-5 first, strict order,
  stop at first FAIL. The round-2 A-6 bindings are part of that Lead re-audit.
- **[AI: Any] STATE.** No product/artifact change; no gate result; no prohibited action. The service
  remains active/static, loopback-only, credential-free DISARMED, `state_version=1`, no
  broker/credentials. Hard exclusions unchanged.

---

## GATE A — run-kit D A-5..A-9 source/preregistration (Lead-audit repair round 1); NOT RUN; A-5 first next (2026-08-08)

**Bounded GLM-5.2 tooling/documentation checkpoint — freezes the run-kit D SOURCE and the
A-5..A-9 preregistration only.** GLM-5.2 edited only the files named in the task (the
preregistration doc `11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md`, the run-kit D
members `README.txt` + `gatea_A5.sh`/`gatea_A6.sh`/`gatea_A7.sh`/`gatea_A8.sh`/
`gatea_A8_host.ps1`/`gatea_A9.sh` under `11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/`, and this
memory/handoff prepend). **A-5..A-9 are NOT RUN.** No product code or product artifact changed;
no packaging, transfer, install, service mutation, credential, broker/exchange access,
successful ARM, order, TESTNET/mainnet, wallet, master merge, or economic action occurred. No
gate result is claimed. Candidate `2ce41e34…` unchanged; A-0..A-4 PASS remain the last completed
state. Full record: `11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md`; operational detail:
`11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/README.txt`.

Run-kit D freezes A-5 (unclean SIGKILL/manual-restart consistency; Restart=no; byte-identical
logical DB snapshot; no `/api/arm`; no env read), A-6 (in-process empty-startup reconcile
dry-run with injected `MockBroker(bars=[])`, temp DB, no network), A-7 (read-only
status/DB/log/journal evidence), A-8 (remote loopback-binding proof + Windows host `TcpClient`
probes; two-part gate — neither alone passes), and A-9 (content-redacted 9-ERE secret scan of
the release + `/etc/mtc-bridge` only). Shared contract: `set -Eeuo pipefail`; fixed
`/home/gatea` evidence log per gate (refuses overwrite); venv Python for all JSON/SQLite work
(no `sqlite3` CLI); `EXIT` trap records exact rc; ends `A-<n> PASS` only if all assertions
hold; never hashes its own open log; never `POST /api/arm`; A-5/A-6/A-7/A-8 do not read the env
file while A-9 scans bytes under the release + `/etc/mtc-bridge` (incl. the root-readable env
file) via `grep -l`, emitting paths only — no value/matched text printed, copied, or persisted
(category counts + paths only). The kit has NOT been packaged/transferred/executed.

- **[AI: Any] BEFORE A-5 — LEAD VALIDATION + PACKAGING + TRANSFER (gate to proceed).** The
  Lead must independently validate the scripts (`bash -n` each `.sh`; PowerShell parser for
  `gatea_A8_host.ps1`; CR-byte check = 0 on every file), create the manifest (`SHA256SUMS`) +
  tar, transfer to `/home/gatea`, and verify exact tar SHA-256/bytes + member set +
  `sha256sum -c` all OK + the five on-host `bash -n`. Do not execute before this.
- **[AI: Claude] A-5 FIRST — STOP AT FIRST FAIL.** Run strict order A-5 → A-6 → A-7 → A-8
  (remote + host) → A-9. After every gate PASS, update `_AI_MEMORY` (`NEXT_STEPS.md`,
  `GLOBAL_HANDOFF.md`) + `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` BEFORE the next gate.
- **[AI: Claude] FIRST-FAIL / SAFETY.** At first FAIL preserve the evidence log, run only
  read-only diagnostics, then STOP; if the state is unsafe, safe-stop + mask the unit
  (`sudo systemctl stop` then `sudo systemctl mask mtc-bridge-first-start.service`) and write
  result + memory. No auto-restart/mask on a script's internal failure (Lead handles safe
  first-FAIL; A-5's `reset-failed`+`start` is the runbook-authorized restart, not auto-restart).
- **[AI: Any] LEAD-AUDIT REPAIR ROUND 1 (Lead source review authoritative; see prereg §9).**
  Repaired bindings: A-5/A-8 use the `ss` LOCAL column (index 3); A-6 restores
  `start_mode='credentialed'` (installed candidate authoritative; MockBroker blocks
  `_build_broker`/credentials/network), fixes the false PASS (nonzero on timeout / start
  exception / failed assertion / stop exception; requires `status()['deferred_event_queue_depth']==0`
  AND `len(_queued_events)==0`), and validates temp cleanup (no `rm -rf`); A-8 host exits nonzero
  on probe fail; A-9 uses `-e`/`--`, canonical nine category names, and a truthful content
  statement. Lead evidence: `bash -n` all 5 rc 0, PS parser 0, CR=0. STATUS unchanged: A-5..A-9
  NOT RUN, not packaged; repaired bindings await re-audit.
- **[AI: Any] STATE.** No product/artifact change; no gate result; no prohibited action. The
  service remains active/static, loopback-only, credential-free DISARMED, `state_version=1`, no
  broker/credentials. Hard exclusions unchanged (credentials, broker/exchange access, successful
  ARM, orders, TESTNET/mainnet, master merge, economic action).

---

## GATE A — A-4 PASS (run-kit C); seven conditions evidenced; A-5 first next (2026-08-08)

**Bounded documentation checkpoint by GLM-5.2 — records the already-executed, already-Lead-verified A-4
step.** GLM-5.2 **only edited documentation** (the four files named in the task). The A-4 staging execution
and the read-only on-disk diagnostics recorded here were **authorized staging actions performed earlier**
under the owner-approved preregistered `gatea-staging` rerun sequence and their results were
**Lead-verified before this checkpoint** — this is **not** "no staging action or diagnostic results
occurred"; they did, within the authorized boundary. Lead verdict: **Gate A A-4 PASS under Addendum D**
(§D.4 / §C.4). Gate A is **IN PROGRESS through A-4**; **A-5–A-9 NOT RUN**. Candidate `2ce41e34…` and the
product/artifact are unchanged; no pytest rerun; candidate acceptance, D025 acceptance, and the
repair-round count unaltered. No product/artifact change; no credential, broker/exchange access, successful
ARM, orders, TESTNET/mainnet, master merge, or economic action. Full record:
`11_TRIAGE/GATE_A_A4_PASS_2026-08-08C.md`.

A-4 PASS rests on main log `/home/gatea/gatea-A4-20260808C.log` (SHA-256
`19ed99773ca8dbfb84bfc6a93289daf4077419dd6d46c23343f5d4cfbf007c06`, `10152` B, script exit `0` bound to
the step-8 application-refusal probe exit `0`) **plus** two canonical clean read-only logs: DB
`/home/gatea/gatea-A4-dbdiag3-20260808C.log` (`530f846c…8a5c8`, `497` B; meta exactly
`app_state=DISARMED` / `schema_version=4`; `PRAGMA quick_check=ok`; PASS; rc `0`) and post
`/home/gatea/gatea-A4-postdiag2-20260808C.log` (`ed06554c…72183`, `1111` B; local-address exactly
`127.0.0.1:8790`; broker hits `0`; API `DISARMED` / `state_version=1`; rc `0`). The main script's step 0
and step 10 nested `sudo bash -c` SQLite quoting errors and the dbdiag/dbdiag2/postdiag helper
false-negatives are run-script-only defects; each missing/false-negative check was reproduced and replaced
by a canonical clean read-only log — no criterion went unobtained. All seven conditions hold.

- **[AI: Claude] PREREGISTER A-5–A-9 BEFORE EXECUTION.** Recover the exact A-5–A-9 commands from the
  canonical runbook and addenda and preregister a bounded command/evidence plan. Do not improvise protected
  tests.
- **[AI: Claude] EXECUTE A-5 FIRST — STOP AT FIRST FAIL.** A-5 is the unclean kill/restart test (state/DB
  consistency / `DISARMED`). On PASS update `_AI_MEMORY` before A-6. On failure preserve evidence, stop+mask
  the service safely, and write result/memory.
- **[AI: Any] RESULT DOCUMENT.** Preserve old `GATE_A_RESULT_2026-08-08.md`; the final rerun record will be
  `GATE_A_RESULT_2026-08-08B.md`.
- **[AI: Any] STATE.** The service **intentionally remains active/static**, loopback-only, credential-free
  `DISARMED`, `state_version=1`, no broker connection, no credentials — the prerequisite for the A-5
  unclean-restart test. Existing authorization covers preregistered A-5–A-9 only; hard exclusions unchanged
  (credentials, broker/exchange access, successful ARM, orders, TESTNET/mainnet, master merge, economic
  action).

---

## GATE A — run-kit C transferred; A-3 retained-log postcheck PASS (2026-08-08)

**Bounded documentation checkpoint by GLM-5.2 — records the executed next unit of the run-kit C
checkpoint (evidence-checker repair only).** Does not alter candidate acceptance, the product bits, the
artifact, D025 acceptance, or the repair-round count. No pytest rerun.
No product code or product artifact changed; no install, service start, credentials,
broker/exchange access, successful ARM, orders, TESTNET/mainnet, master merge, or economic action. The
authorized staging actions in this unit were exactly run-kit C transfer/verification and read-only
retained-log A-3 postcheck/replay, producing the two recorded logs. The GLM worker itself only edited
documentation and did not perform staging/Git mutation. Full record:
`11_TRIAGE/GATE_A_LOCAL_RUN_KIT_2026-08-08C.md`
(addendum).

The two "next unit" actions from the section below (transfer run-kit C; re-check A-3 without rerunning
pytest) are now DONE on `gatea-staging`. Transfer (B intact): tar SHA-256
`4ee5ba920800ceff8f55338bcba5b388d39d2457f9970795af89c9333767f855`, `53760` B, exact 9 members at
`/home/gatea/gatea-run-kit-20260808C-2ce41e34.tar`; extracted to
`/home/gatea/gatea-run-kit-20260808C-2ce41e34`; 7 manifest entries; `sha256sum -c` all seven OK; six
`bash -n` PASS; corrected remote `gatea_A3.sh`
`2bfec1c230d77d70f30bda5560f824fe970b4c2fca098d3fdda49129f2465d1c` OK. A-3 postcheck PASS (no pytest
rerun): retained `/home/gatea/gatea-A3-suite-20260808B.log` SHA-256
`569e79c7d68623b9f2ad51ee48053a04e6938e3277398861760dc1dd8d61c848`; outer log exact `pytest rc=1`;
terminal `2 failed, 1358 passed, 1 warning in 169.85s (0:02:49)` matches the corrected anchored
optional-elapsed regex; observed failures exactly equal the two permitted `test_order_state.py`
gc-referents node IDs both ways; failures `0`; `A-3 CHECKER PASS`. Canonical VM logs
`/home/gatea/gatea-A3-postcheck-20260808C.log` and `…-clean.log`: both SHA-256
`56a80d53155ac73b39dac064260ff702532fad36562eafbbe75f28c2f6414878`, `738` B, byte-identical.

Transport noise recorded transparently (not concealed): the first PowerShell stdin stream inserted a BOM
before the shebang and printed a harmless `#!/usr/bin/env` command error outside the captured log after
the postcheck had already returned PASS (the captured log was clean); a second byte-preserving Git Bash
replay to the separate clean log had no transport error and reproduced the same 738 bytes/hash/PASS.
Clean-replay postcheck script `19003ef0…415f1`; runner `7a03c61d…6da16`; both `bash -n` rc `0`, 0 CR.

- **[AI: Claude] EXECUTE A-4 UNDER ADDENDUM D — STOP AT FIRST FAIL.** Run the transferred C `gatea_A4.sh`
  on `gatea-staging` and capture all seven conditions: active/running; loopback 127.0.0.1:8790 only;
  status durably not ARMED; application-level exact credential-free 409 with correct `X-Confirm`; no
  broker attempt in journal/`bridge.err.log`/sockets; persisted `DISARMED` and unchanged version;
  resolved running environment/start mode. On failure run only read-only diagnostic as needed, then
  stop+mask the service and write result/memory. On PASS update `_AI_MEMORY` before preregistering the
  exact A-5–A-9 commands — do not improvise them.
- **[AI: Any] RESULT DOCUMENT.** Preserve old `GATE_A_RESULT_2026-08-08.md`; later write
  `GATE_A_RESULT_2026-08-08B.md`.
- **[AI: Any] STATE.** After postcheck the service was reverified `inactive`/`masked`, listener 8790
  absent, no credentials loaded. Gate A IN PROGRESS after accepted A-3; A-4 not started. Existing owner
  authorization covers A-4 within the preregistered sequence; hard exclusions unchanged (credentials,
  broker/exchange access, successful ARM, orders, TESTNET/mainnet, master merge, economic action).

---

## GATE A — corrected A-3 checker frozen as run-kit C (evidence-checker repair only) (2026-08-08)

**Bounded documentation checkpoint by GLM-5.2 — evidence-checker repair only, not an implementation or
audit.** Freezes the corrected A-3 run-script checker as run-kit **C**; does not alter candidate
acceptance, the product bits, the artifact, D025 acceptance, or the repair-round count. Run-kit B is
preserved unchanged; C differs only in `gatea_A3.sh` and the README. No transfer or remote execution is
claimed — validated locally only; the checker has **not** been re-run on staging. Full record:
`11_TRIAGE/GATE_A_LOCAL_RUN_KIT_2026-08-08C.md` (cites the B record and the A-3 checkpoint).

Frozen run-kit C bundle (local, not transferred): `C:\WPI_ARTIFACTS\gatea-run-kit-20260808C-2ce41e34`
(+ `.tar`); tar SHA-256 `4ee5ba920800ceff8f55338bcba5b388d39d2457f9970795af89c9333767f855`; `53760` B;
exact 9 members (root dir + `README.txt`, `SHA256SUMS`, six scripts); 7 manifest entries. Corrected
`gatea_A3.sh` `2bfec1c230d77d70f30bda5560f824fe970b4c2fca098d3fdda49129f2465d1c` / `5087` B (B:
`33934221…604443` / `4064`). README `47278c48…2883`. Five unchanged: A0_A1 `0d456a8e…f1c11`, A2
`07a715aa…c053`, A4 `78aa7fca…fd9b4`, A4_diag `f75912a2…f101d`, teardown `19016d8f…c0b3`. Independent
validation: 8 files / 7 manifest entries; `sha256sum -c` all OK; six `bash -n` rc `0`; 0 CR bytes;
checker falsification `10 passed, 0 failed`, rc `0`. Cleanup of
`C:\tmp\gatea-c-verify-929e34808c0e47699d8964f879309072` blocked by policy after exact-path check —
remains isolated, not in either tar, not in repo, not removed.

- **[AI: Claude] TRANSFER RUN-KIT C ONLY — DO NOT REPLACE/DELETE B.** Transfer only the run-kit C
  tar to `/home/gatea/gatea-run-kit-20260808C-2ce41e34.tar`; verify exact tar SHA-256
  `4ee5ba92…7f855`, `53760` bytes, and the exact 9-member set (root dir + 8 files); extract to
  `/home/gatea/gatea-run-kit-20260808C-2ce41e34`; run `sha256sum -c` and the six `bash -n` checks.
- **[AI: Claude] RE-CHECK A-3 WITHOUT RERUNNING PYTEST.** Against the retained
  `/home/gatea/gatea-A3-suite-20260808B.log`: require the last non-empty line to match the corrected
  anchored optional-elapsed regex; require `/home/gatea/gatea-A3-20260808B.log` to contain the exact
  line `pytest rc=1`; require exact two-way equality between observed `FAILED ` node-ID lines and the
  two permitted `test_order_state.py` gc-referents failures. Preserve output at
  `/home/gatea/gatea-A3-postcheck-20260808C.log`. Any mismatch is Gate A FAIL; otherwise A-3 checker
  PASS.
- **[AI: Any] UPDATE `_AI_MEMORY/` BEFORE A-4.**
- **[AI: Claude] RUN A-4 EXACTLY UNDER ADDENDUM D AND STOP AT FIRST FAIL.** Bind A-4 to the corrected
  step-8 result. No credentials/broker/successful ARM/orders/TESTNET/mainnet/master merge/economic
  action. Capture `systemctl show -p Environment`, `bridge.err.log`, listener, status, the exact
  application 409, unchanged state/version, and no broker attempt. Leave the service masked/inactive on
  failure.
- **[AI: Any] STATE UNCHANGED BY THIS C FREEZE UNIT.** Candidate `2ce41e34…` accepted;
  product/artifact/staging install not modified during this unit; Gate A IN PROGRESS through A-3; A-4
  not started; current accepted `2ce41e34` install masked/inactive/not enabled, no listener, no
  credentials. No staging contact, teardown, install, service start, credential, broker/exchange
  access, ARM, order, TESTNET/mainnet, master merge, or economic action occurred **in this C freeze
  unit** — this scopes only the C unit; A-0 through A-3 of the overall rerun did run on `gatea-staging`
  (see the A-3 rerun checkpoint). The owner already explicitly authorized the preregistered
  `gatea-staging` teardown/rerun sequence, so no additional authorization is required to transfer
  run-kit C, run the retained-log A-3 postcheck, or run A-4 within that sequence; hard exclusions
  remain (credentials, broker/exchange access, successful ARM, orders, TESTNET/mainnet, master merge,
  economic action).
- **[AI: Any] CLEANUP RESIDUE.** `C:\tmp\gatea-c-verify-929e34808c0e47699d8964f879309072` remains
  isolated; remove only by an allowed exact-literal cleanup. **Do not claim it was removed.**

---

## GATE A — reran through A-3; A-4 not started; Gate A IN PROGRESS (2026-08-08)

**Bounded documentation checkpoint by GLM-5.2.** The exact Claude Opus 5 implementation call was
attempted first but returned `session limit — resets 11:50pm` before any edit; this checkpoint is
bounded documentation only, not a substitute for a flagship audit or protected implementation. The
corrected A-3 checker has NOT yet been propagated/frozen/transferred to staging. Full evidence:
`11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md`.

- **[AI: Claude] FREEZE A CORRECTED RUN-KIT REVISION.** Do not overwrite run-kit B silently. Regenerate
  `SHA256SUMS`/tar, independently verify member set / hash / `bash -n` syntax / falsification, document
  it, transfer only the correction/revision, and verify the remote hash.
- **[AI: Claude] RE-RUN ONLY THE A-3 CHECKER POST-PROCESSING** against the already-completed retained
  suite log; do not rerun the 170-second product suite unless necessary. Require wrapper/checker PASS.
- **[AI: Claude] RUN A-4 UNDER ADDENDUM D.** Capture all seven conditions plus the resolved
  `systemctl show -p Environment`, `bridge.err.log`, listener, status, the exact application 409,
  unchanged state/version, and no broker attempt. Stop at first FAIL and leave the service
  masked/inactive on failure.
- **[AI: Claude] IF A-4 PASSES,** recover and preregister the exact A-5 through A-9 commands before
  execution; do not improvise protected tests. Continue the first-FAIL rule.
- **[AI: Claude] WRITE `GATE_A_RESULT_2026-08-08B.md`,** update `_AI_MEMORY`, then — only after the
  Gate A verdict — consider separately authorized follow-up. No master merge/deploy/credentials/broker/
  ARM/orders.

---

## GATE A — 20260808B local run kit validated; staging authorization still required (2026-08-08)

**This is the live pickup.** Full evidence and all six hashes:
`11_TRIAGE/GATE_A_LOCAL_RUN_KIT_2026-08-08B.md`. Candidate acceptance remains unchanged at
`2ce41e34bceb599d80af24c5c33d835820ec321b`; Gate A has not rerun.

- **[AI: Any] LOCAL PREPARATION COMPLETE.** The single transfer tar is frozen and not transferred.
  Six A-0/A-1, A-2, A-3, A-4, A-4 diagnostic, and teardown scripts are re-baselined to Addendum D;
  all pass Git Bash `bash -n`. A-0/A-2/A-3 claims are exit-bearing, and teardown is exact-target,
  fresh-evidence, no-overwrite, and explicitly not authorized to run.
- **[AI: Any] A-4 SCRIPT EVIDENCE DEFECT CORRECTED — candidate unchanged.** The route checks
  `X-Confirm` before the credential-free guard. Therefore `409 stale state_version` is non-evidence
  and fails A-4. Corrected step 8 first requires exact credential-free/DISARMED fail-closed status;
  any mismatch exits `2` with zero POST. Only then it sends the returned state version, requires the
  exact credential-free 409, and requires unchanged status/version afterward.
- **[AI: Any] LOCAL VALIDATION.** Five no-network falsification cases passed: bad mode and boolean
  version blocked with zero POST; exact refusal passed; stale-confirm and changed-version failed.
  The candidate's real in-process refusal test passed `1 passed, 1 warning in 0.52s`.
- **[AI: Any] OFFLINE A-0 PASS / A-1 PLATFORM STOP.** Offline local A-0 executed against the real
  frozen tar in a fresh disposable HOME and passed every A-0 identity check (tar SHA
  `d78b9e82e4138714fd5eabfb4996d8d831f28d14cf0b9e1149c8751739fe05f2`, `1047265280` B; `RELEASE_SHA`
  exact `2ce41e34…`; manifest `edb0fd34…20d26`; 7059 entries / 7060 regular files / 1033362481 B /
  0 non-regular; `sha256sum -c` rc 0, 0 problem lines; 0 CR bytes on all five `deploy/linux/*.sh`).
  The same script then stopped at A-1 because this workstation is Windows and `/etc/os-release` is
  absent — **A-1 was NOT executed/accepted; no Linux or Gate A claim is promoted.**
- **[AI: Any] DEEPSEEK NO-VERDICT — supplemental only.** Attempt 1 exhausted `max_iters` with no
  verdict; the focused retry read all ten files but stopped without finish/verdict. DeepSeek is
  supplemental non-accepting evidence only.
- **[AI: Any] HARDENING.** A-4 `start_rc` now recorded explicitly as `PIPESTATUS[0]` (the claimed
  pipeline loss did not reproduce; `set -o pipefail` returned upstream rc 7). A-3 changed to
  `grep -qxF` (the `grep -qF` substring concern reproduced; exact fixture rc 0, prefixed rc 1). A-4
  and A-4_diag hardened to query only meta keys `app_state` and `schema_version`. All six scripts
  pass `bash -n`; the exact embedded A-4 five-case no-network falsification still passes; the real
  in-process refusal test still passes `1 passed, 1 warning in 0.52s`.
- **[AI: Any] NEW HASHES BY REFERENCE.** Replaced script hashes are recorded in the run kit: A3
  `33934221…604443` / 4064 B; A4 `78aa7fca…fd9b4` / 16228 B; A4_diag `f75912a2…f101d` / 3053 B;
  unchanged hashes remain as written.
- **[AI: Any] CLEANUP RESIDUE.** Cleanup of the disposable
  `C:\tmp\gatea-a0-offline-bb964b4106b24ea192f830065a1b9992` was refused twice by local command
  policy after exact path verification; the directory remains isolated under `C:\tmp` and must be
  removed only by an allowed exact-literal cleanup. **Do not claim it was removed.**
- **[AI: Any] SINGLE RUN-KIT BUNDLE FROZEN — NOT TRANSFERRED.**
  `C:\WPI_ARTIFACTS\gatea-run-kit-20260808B-2ce41e34.tar`, SHA-256
  `ac0fbaf2fefa8241c5c92f5bf35a3f9fc5258a4b7e30614988ed305afa61c0fb`, `61440` B, exact 9-member
  archive. All seven manifest entries match; all six archived shell files have 0 CR bytes. README
  hash `45b480ac5ce949f051e4f30753a5e85c7871b634f0ca9b1b646ae24927981353`; it explicitly says local
  preparation only, not authorized to transfer or run.
- **[AI: Barış] HARD GATE — explicit staging authorization required.** No host contact, transfer,
  teardown, install, service start, credential, broker/exchange access, ARM request, order,
  TESTNET/mainnet, or economic action occurred. The old host state was not rechecked.
- **[AI: Claude|Codex] AFTER AUTHORIZATION ONLY.** Transfer the run-kit bundle, verify its tar hash
  and `SHA256SUMS`, then run the prepared teardown and require leftovers `0`; transfer the one
  product tar; run Gate A from A-0 under Addendum D and stop at first FAIL. Bind A-4 to corrected
  step 8; capture `systemctl show -p Environment`,
  `bridge.err.log`, and verifier override rejection/restoration/clean re-verification. Preserve the
  old result and write `GATE_A_RESULT_2026-08-08B.md`.
- **[AI: Any] WHILE THE GATE IS CLOSED.** Continue only safe local evidence/package validation and
  record-consistency work. Update `_AI_MEMORY/` before starting the next work unit.

---

## GATE A — A-4 repair `2ce41e34` ACCEPTED and packaged; Gate A rerun awaiting staging authorization (2026-08-08)

**This section supersedes the `## GATE A — RUN COMPLETE … A-4 FAIL` section immediately below** (and its
round-1 bullet trail). That older top status is preserved below as history. Live pickup:
`11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md`.

- **[AI: Any] THE A-4 REPAIR CANDIDATE IS ACCEPTED — `2ce41e34`.** Round 2 closes the round-1 env-override
  defect. **ACCEPTED under D025** per
  `11_TRIAGE/GATE_A_DISARM_FIX_AUDIT_ROUND2_2CE41E34_2026-08-08.md`: `gpt-5.6-sol` xhigh **PASS**,
  `claude-opus-5` xhigh **PASS-WITH-NITS** (0 required), `GLM-5.2` **PASS** (executed the suite);
  DeepSeek V4 Flash returned a non-execution BLOCK (`No access to ClinePass subscription models yet.`) —
  supplemental per D025, no veto. Both flagships accept; no reproduced required finding remains.
- **[AI: Any] THE REPAIR — 4 files, 59 insertions.** `deploy/linux/verify.sh` rejects any
  `MTC_BRIDGE_START_MODE=` definition in `${MTC_ENV_FILE}` (the channel that defeated `ed3d0534`: systemd
  `EnvironmentFile=` overrides `Environment=`); a new behavior test proves the rejection; `README.md` and
  `env/mtc-bridge.env.template` document the variable as unit-set. No product-runtime file touched.
- **[AI: Any] LEAD EVIDENCE at `2ce41e34`.** Targeted `1 passed in 0.81s`; deployment file `48 passed in
  12.57s`; full suite **`1360 passed, 1 warning in 122.86s`** (Windows floor +1 over `1359` — one new test
  function). D026 honored: RED-A (require-export / bare-assignment mutation) and RED-B (invert branches)
  both independently RED, expected `FAIL_BRANCH` vs actual `PASS_BRANCH`; GREEN restored.
- **[AI: Any] ARTIFACT VERIFIED.** `C:\WPI_ARTIFACTS\2ce41e34bceb599d80af24c5c33d835820ec321b`, manifest
  `EDB0FD34E3D976B872868CC3DFBF745CBC4B08F6C4C5D21B8D6CDA47A3E20D26`, 7059 entries / 7060 files /
  1 033 362 481 B, **0 CR bytes on all five `deploy/linux/*.sh`**; payload property counts: first-start
  pin 1, steady pin 0, env guard 1, behavioral test 1.
- **[AI: Any] GATE A INPUTS RE-BASELINED — Addendum D.** `GATE_A_PREREGISTRATION_ADDENDUM_D_2026-08-08.md`
  supersedes Addendum C **only** for frozen candidate/artifact/test-count facts; C.2 (host prep) and C.4
  (A-4 seven-condition standard) remain in force by reference. Expected Linux A-3: **`2 failed, 1358
  passed, 1 warning`** — same two pre-registered `test_order_state.py` gc-referents failures, one new
  passing test function; **expected count, must be checked on the host.**
- **[AI: Barış] ACCEPTANCE IS OF THE CANDIDATE, NOT GATE A. Gate A has not rerun; A-4 stays historically
  failed.** **Do NOT transfer, install, tear down, or run Gate A** until Barış authorizes staging action.
  The old `ebada020` install on `gatea-staging` is masked / inactive / no listener / no credentials /
  nothing armed. `2ce41e34` supersedes the unaccepted `ed3d0534`; do not transfer or install the
  `ed3d0534` artifact.
- **[AI: Barış] NEXT SAFE STEP (owner-gated).** (1) Barış authorizes staging action; (2) tear down the
  stale `ebada020` install with proven `C:\tmp\gatea_teardown.sh` (`rollback.sh` is not an uninstaller);
  (3) transfer the `2ce41e34` artifact as **one tar**; (4) run Gate A from **A-0** per Addendum D, stop at
  first FAIL, capturing **required host evidence** for A-4: `systemctl show -p Environment
  mtc-bridge-first-start.service`, and an explicit verifier rejection of a temporary
  `MTC_BRIDGE_START_MODE=` env-file override (redact any value; remove the temp line after and re-run
  `verify.sh` for a clean PASS); (5) preserve `GATE_A_RESULT_2026-08-08.md` intact, write
  `GATE_A_RESULT_2026-08-08B.md` for the new run either way.
- **[AI: Any] QUEUED NITS (not repaired here, no product edits).** (1) verifier does not inspect systemd
  drop-ins — future scoped follow-up; (2) steady profile has no start-mode pin (correct for now) — address
  at the steady profile's future gate; (3) remaining cosmetic / over-strict / test-structure notes are
  non-blocking.
- **[AI: Any] OWNER OPERATING PROTOCOL (recorded 2026-08-08; full text in `PROJECT_MEMORY.md` →
  *Owner operating preference*).** End every work unit with explicit practical next steps; refresh
  `_AI_MEMORY/` records before starting the next one; continue autonomously through the next safe,
  already-authorized work unit without routine questions; use available subscription routes
  proactively while keeping exact-model / counterpart / canonical-audit / token-routing /
  Lead-verification rules intact. **The current hard gate is staging authorization from Barış:** safe
  preparation and evidence work may continue autonomously (docs, audits, artifact verification, host
  scripts staged locally in `C:\tmp`), but transfer, teardown, install, and the Gate A rerun may not —
  at that gate, record the exact authorization required instead of crossing it.

---

## GATE A — RUN COMPLETE: A-0→A-3 PASS, **A-4 FAIL**, stopped per first-FAIL rule (2026-08-08)

**START HERE:** `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` (standalone pickup, supersedes
`…_2026-08-03B.md`), then `11_TRIAGE/GATE_A_RESULT_2026-08-08.md` for the A-4 traceback,
`11_TRIAGE/GATE_A_INTEGRATION_FLAGSHIP_AUDITS_EBADA020_2026-08-08.md` and
`11_TRIAGE/GATE_A_PREREGISTRATION_ADDENDUM_B_2026-08-08.md`.
This section supersedes the 2026-08-03 section below.

- **[AI: Any] GATE A RESULT:** A-0 **PASS** · A-1 **PASS** · A-2 **PASS** · A-3 **PASS** ·
  **A-4 FAIL** · A-5…A-9 **NOT RUN** (first-FAIL rule; all of them presuppose a running service).
  Host logs on `gatea-staging`: `~/gatea-A0A1-20260808.log`, `~/gatea-A2-dryrun-20260808.log`,
  `~/gatea-A2-install-20260808.log`, `~/gatea-A3-suite-20260808.log`, `~/gatea-A3-20260808.log`,
  `~/gatea-A4-20260808.log`, `~/gatea-A4-diag-20260808.log`, `~/gatea-teardown-20260808.log`,
  and `/var/log/mtc-bridge/bridge.err.log`. Step scripts `/tmp/a01.sh`, `/tmp/a2.sh`, `/tmp/a3.sh`,
  `/tmp/a4.sh`, `/tmp/a4d.sh` (sources in `C:\tmp\gatea_*.sh`).
- **[AI: Barış] A-4 FAIL CAUSE — flagship NIT 1, now in production form. THIS IS THE BLOCKER.** The
  service exits 1 in 482 ms and never listens. `bridge/app.py:282` module-level `create_app()` →
  `:150` → `_build_broker` `:244` → `settings.py:113`
  `RuntimeError: Hyperliquid credentials not found`. Confirmed on the host:
  `resolve_start_mode` → **`credentialed`**, because the unit's `ExecStart` is bare
  `python -m bridge.app` and the env file names no `MTC_BRIDGE_START_MODE`. The credential-free
  DISARMED path exists in code and is unreachable from the deployment.
- **[AI: Any] IT FAILS CLOSED — record this accurately.** No arm, **zero** broker connection attempts
  (exception is raised while *constructing* the broker, before any network I/O), no listener ever
  opened, and the store persisted `app_state=DISARMED` / `schema_version=4`. A-4 fails because its
  required "the ARM path refuses" confirmation is **unobtainable** (`Errno 111 Connection refused`),
  not because anything armed. Non-execution is never acceptance.
- **[AI: Any] NOT A REGRESSION OF `ebada020`.** The identical failure is in the journal from
  `Aug 01 23:35:27`. It was invisible on 2026-08-02 because that run died at A-2 and never reached
  A-4. Fixing the CRLF defect is what let the gate get far enough to expose this. `ebada020` is not
  retroactively rejected — the gap is in `deploy/`, outside the nine-file merge scope.
- **[AI: Any] A-4 REPAIR IS BUILT AND COMMITTED — `ed3d0534` on `codex/gate-a-disarmed-start-mode`**
  (branched from `ebada020`, pushed). Barış authorised the **small fix only** on 2026-08-08; the deeper
  change is deferred (see below). Three files, 6 insertions, 1 deletion:
  `deploy/linux/systemd/mtc-bridge-first-start.service.template` gains
  `Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed`; `deploy/linux/verify.sh` adds it to the
  unit-assertion list so every install re-checks it on the host; `tests/test_linux_deployment.py`
  asserts the first-start unit declares it **and that the steady unit does not** (steady is the future
  credentialed profile — pinning DISARMED there would be wrong).
  Placed in the unit rather than the `EnvironmentFile` (contract-only, values never written) and rather
  than an `ExecStart` flag (the unit is hashed into `install_manifest.json` as
  `first_start_unit_sha256`, so it cannot drift silently) — the precedent the template already states
  for `MTC_BRIDGE_STATE_DB`. Name and value taken from `bridge/app.py:30,32`, not guessed.
  **D026 honoured:** real `AssertionError` at `test_linux_deployment.py:226` against the unmodified
  template (`1 failed, 1 passed`) before the fix, green after. Lead reproduced the full Windows suite
  independently: **`1359 passed, 1 warning in 198.90s`**. Implemented by Codex `gpt-5.6-sol` under Lead
  scope; diff, constants, D026 evidence and suite all verified against the files, not the report.
  Log `C:\tmp\CODEX_DISARMED_START_MODE_IMPL_2026-08-08.txt`, spec
  `C:\tmp\codex_disarmed_start_mode_impl.md`, worktree `C:\GADISARM`.
- **[AI: Any] ARTIFACT REBUILT AND VERIFIED at `ed3d0534`** (Barış authorised review + rebuild + rerun
  on 2026-08-08). `C:\WPI_ARTIFACTS\ed3d053432fb496123ac43bcb7d40cfb64edbb8b`, manifest
  **`8964CC43B802BADA1AD5611E5B445E19B4332C45133AF3E8473A85BB57E7EE4B`**, 7059 entries, 7060 files,
  1 033 359 494 bytes (+336 B over `ebada020` = the six added lines), **0 CR bytes on all five
  `deploy/linux/*.sh`**, fix present in the built payload at
  `…/mtc-bridge-first-start.service.template:42`, steady template correctly clean. Built once via
  `package.sh --release-sha ed3d0534… --repo C:\GADISARM --out …`, exit 0. Frozen in
  `11_TRIAGE/GATE_A_PREREGISTRATION_ADDENDUM_C_2026-08-08.md` (`783335e3`), which also **re-registers
  A-4's expectation in advance** — seven conditions, and an application-level arm refusal is required
  (`Errno 111 Connection refused` explicitly does not count).
- **[AI: Any] BOTH FLAGSHIP AUDITS OF `ed3d0534` COMPLETED 2026-08-08 — `ed3d0534` IS NOT ACCEPTED.**
  Record: `11_TRIAGE/GATE_A_DISARM_FIX_AUDIT_ROUND1_ED3D0534_2026-08-08.md`.
  `claude-opus-5` xhigh **PASS-WITH-NITS** (0 required, `1359 passed`); `gpt-5.6-sol` xhigh
  **REQUEST_CHANGES** (1 required finding). D025 rule 3 needs both accepting, so acceptance fails.
  **Both found the same defect independently** — they differ only on severity, and the stricter reading
  governs. Reports `C:\tmp\CLAUDE_AUDIT_DISARM_FIX_2026-08-08.txt`,
  `C:\tmp\CODEX_AUDIT_DISARM_FIX_2026-08-08.txt`.
- **[AI: Barış] THE BINDING FINDING — Lead-reproduced, so it binds.** `EnvironmentFile=` **overrides**
  `Environment=` in systemd, so the start-mode "pin" at
  `mtc-bridge-first-start.service.template:42` is defeated by any
  `MTC_BRIDGE_START_MODE=credentialed` written into `/etc/mtc-bridge/mtc-bridge.env` (declared at
  line 45). And `verify.sh:138` rejects only `HL_LIVE_ACK=` in the env file — Lead confirmed the sole
  `MTC_BRIDGE_START_MODE` occurrence in `verify.sh` is line 166, the *unit* needle, **not** an env-file
  rejection. So the verifier passes while the override wins. **The DISARMED property is currently
  conventional, not enforced.**
  **Minimum repair (both auditors agree, within existing scope):** `verify.sh` must reject any
  `MTC_BRIDGE_START_MODE=` in `${MTC_ENV_FILE}`, plus a regression test proving the rejection. Fold in
  the docs nit — the README and env template document `MTC_BRIDGE_STATE_DB` but say nothing about the
  start mode; "set by the unit; defining it here would override the unit" is now literally true.
- **[AI: Any] CORRECTION TO THE RECORD:** `ed3d0534`'s commit message and Addendum C §C.1 justified the
  placement as "cannot drift silently". True for **unit** drift (`verify.sh:184-190` `cmp -s` plus
  `first_start_unit_sha256`), **wrong as a general claim** — the env file is a second, unguarded
  channel that outranks the unit. Placement is still correct; the rationale was overstated.
- **[AI: Any] EXECUTION LIMIT — settle it on the host next round.** Neither auditor could execute
  systemd precedence (no systemd/WSL on this workstation); both cite `man systemd.exec`. One command on
  staging settles it and must be captured:
  `systemctl show -p Environment mtc-bridge-first-start.service`.
- **[AI: Any] THE REPAIR ITSELF WORKS — do not mistake this for a failed fix.** Both flagships ran a
  real `python -m bridge.app` with no credentials: listener on `127.0.0.1:8790`, `GET /api/status` →
  `200 DISARMED / credential_free_disarmed / exchange_enabled=False`, **`POST /api/arm` → 409
  `"ARM unavailable in credential-free DISARMED start mode"`**, status unchanged after. That is exactly
  the application-level refusal A-4 could not obtain. Near-miss values raise `ValueError` (fail closed),
  never silently degrade to `credentialed`. D026 falsified in both directions.
- **[AI: Any] `ebada020` remains the last accepted candidate. Gate A must not start.** The rebuilt
  artifact `C:\WPI_ARTIFACTS\ed3d0534…` is a valid build of an **unaccepted** commit — **do not transfer
  or install it.** Repair round 1 of a maximum 3 is available.
- **[AI: Any] BEFORE A-0 NEXT TIME:** the `ebada020` install is still on `gatea-staging` and A-1 will
  fail 7 of 8 assertions against it. Tear it down first with the proven `C:\tmp\gatea_teardown.sh`
  (leftovers 0 last time). `rollback.sh` takes `--to-release-sha` and is **not** an uninstaller.
- **[AI: Barış] DEFERRED BY OWNER DECISION — do not slip it in:** whether module-level `create_app()`
  at `bridge/app.py:282` should construct a broker at import time at all. Barış chose the small fix
  only. "Told not to ask for credentials" is weaker than "cannot ask"; revisit as its own decision.
- **[AI: Barış] SUPERSEDED — the original authorization note read:** product change needed.
  Wire `--start-mode credential_free_disarmed` into both unit templates (or `MTC_BRIDGE_START_MODE`
  into the env template + `install.sh`), and consider whether `app.py:282` should construct a broker at
  import time at all on a first DISARMED start. Fold in the cosmetic-but-misleading
  `HKEY_CURRENT_USER\Environment` Windows registry path in `settings.py:113`'s Linux failure message.
  That means a new frozen SHA, a rebuilt artifact, a fresh flagship round, then Gate A again from A-0.
- **[AI: Any] HOST LEFT SAFE AND REUSABLE:** unit `reset-failed` then re-`mask`ed →
  `is-active inactive`, `is-enabled masked`, no listener on 8790. The `ebada020` install is left in
  place so the A-4 repair can be retested without reinstalling. Nothing armed, no credential
  provisioned, no firewall change.
- **[AI: Any] THE 2026-08-02 A-2 FAILURE IS DISPROVED ON LINUX, not inferred from Windows.** After a
  real one-tar transfer: `install.sh`/`common.sh`/`package.sh`/`rollback.sh`/`verify.sh` all `cr=0`.
- **[AI: Any] A-2 PASSED WITH NO HOST EDITS**, so the artifact is self-contained — the thing WP-I
  exists to prove. `verify.sh` exit 0 on every assertion; unit masked, unstarted, unenabled; env file
  600 `root:root` with zero populated assignments.
- **[AI: Any] ADDENDUM B VENV PIN IS SUPERSEDED.** The stale 2026-08-02 install was torn down (see
  result doc §1), and its venv was the `a1dd5b46…` interpreter all prior Linux evidence used. A-3 ran
  on the venv **A-2 installed** — same CPython 3.12.3 / pytest 9.1.1, expectation unaffected.
- **[AI: Any] NEXT — A-4, the gate's most important check**, carrying the declared NIT 1 risk. Record
  which start mode the service selects and whether any broker connection is attempted. Method is
  pre-registered: the unit installs masked with `Restart=no`, so A-4 needs `systemctl unmask` then
  `systemctl start`.

- **[AI: Any] D025 SATISFIED — `ebada020` IS ACCEPTED.** Both flagships accepting with zero required
  findings from any auditor: `gpt-5.6-sol` xhigh **PASS** (round 3) and `claude-opus-5` xhigh
  **PASS-WITH-NITS** (round 4, accepting per `AGENTS.md:80`). Round 4 relied on the record for nothing
  — it executed the locked-Linux floor itself and reproduced it exactly, making the verdict
  full-platform rather than Windows-only. Reports
  `C:\tmp\CODEX_SOL_AUDIT_INTEGRATION_EBADA020_2026-08-08.txt`,
  `C:\tmp\CLAUDE_FLAGSHIP_AUDIT_INTEGRATION_EBADA020_2026-08-08.txt`.
- **[AI: Barış] BLOCKED ON YOU — Gate A execution authorization.** Everything is pre-registered and
  ready. Gate A installs and starts a service on the staging host, which the standing hard-stop list
  names as requiring a new explicit instruction. Nothing else blocks A-0.
- **[AI: Any] GATE A INPUTS ARE RE-BASELINED — use Addendum B, not runbook §2.** The runbook and
  Addendum A still freeze the superseded artifact `1adf9ae5…`/`bfefea2f…`/7060 entries, and A-3 still
  expects failures the repairs fixed. Authoritative: artifact
  `C:\WPI_ARTIFACTS\ebada020a59edf539f60acfbb3a6bf870c8679e9`, manifest `8FC30864…4700C9`, **7059
  entries, 7060 files, 1 033 359 158 bytes**. A-3 expects `2 failed, 1357 passed` with the only
  permitted failures being the two `test_order_state.py` gc-referents tests.
- **[AI: Any] A-4 RISK DECLARED IN ADVANCE (flagship NIT 1, Lead-reproduced).** The credential-free
  DISARMED start mode is **not reachable from any shipped deploy artifact** — zero `start-mode` hits
  under `deploy/`, both unit templates `ExecStart=… python -m bridge.app`, env template does not name
  the variable, resolver defaults to **credentialed**. The service under test will start credentialed
  against an env file `install.sh` leaves unset. A-4's FAIL condition is NOT softened. Binding
  follow-up before any DISARMED VPS deploy: "did not arm" is weaker than "cannot arm, having never
  held credentials".
- **[AI: Barış] STAGING HOST IS NOT A CLEAN HOST — decide the cleanup scope before A-0.** `/` is 64%
  full, 14 G free of 39 G, and `~gatea` holds ≈14 G of accumulated audit debris from many prior rounds
  (`lead-ga3br2-*` 2 G each, `payload*`/`fixpay*`/`recon` ≈1 G each, `opus5-audit-20260808` 544 M plus
  four `v2_*`/`sub_*` tars). Some of it is cited evidence in accepted records, so the Lead did not
  delete any of it. A-1 is a *clean-host* precondition and A-9 rescans the installed tree.
- **[AI: Any] CARRIED NITS:** NIT 3 — the two surviving gc-referents failures are CPython
  3.12-dependent and the production venv **is** 3.12, so the production floor is amber; scoped fix
  owed. Stale docs — `AI_ACCOUNT_AND_MODEL_ROUTING.md:21` still calls the `.codex_OLD` route Free (it
  is Plus, `gpt-5.6-sol` xhigh proven live), and `Invoke-CodexForClaude.ps1` needs its Codex flags
  passed as `-CodexArgs $array` or PowerShell rejects `exec`.

---

## GATE A — FOUR REPAIRS ACCEPTED, INTEGRATED AT `ebada020`, RERUN PENDING (2026-08-03, SUPERSEDED)

**Superseded by the section above.** Its "only one blocker left" line is closed: the
`gpt-5.6-sol` audit ran on 2026-08-08 and a `claude-opus-5` flagship round was added.

**START HERE:** `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-03B.md`, then
`11_TRIAGE/GATE_A_QUEUE_D_INTEGRATION_STATUS_2026-08-03.md`.
This section **supersedes** the 2026-08-02 "ALL THREE NOT ACCEPTED" section below — all four
candidates were subsequently repaired and accepted under Barış's explicit no-Claude owner waiver.

- **[AI: Any] STATE:** 3b `7aad0377` PASS · build `82e92c98` PASS · Queue C `17402a58` PASS ·
  residual `ebb750da` PASS. Integrated into `codex/gate-a-integration` = `ebada020` (pushed, clean,
  nine-file diff vs `origin/master`). Windows full `1359 passed`. Artifact rebuilt exactly once:
  `C:\WPI_ARTIFACTS\ebada020…\`, manifest `8FC30864…4700C9`, 7059 entries.
- **[AI: Any] NEXT — ONLY ONE BLOCKER LEFT: run the second flagship `gpt-5.6-sol` xhigh audit of
  `ebada020`.** Reusable prompt `C:\tmp\glm_round2_prompt.md`, detached worktree `C:\GAAUD_INT_GLM`
  (clean, at `ebada020`). After it accepts, Gate A can restart at A-0.
- **[AI: Any] GATEA-STAGING IS LIVE AND USABLE:** `172.24.55.233`, user `gatea`, identity
  `C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519` (recovered from
  `11_TRIAGE/CODEX_TAKEOVER_HANDOFF_2026-08-02.md:125`). Verified `gatea-staging` / Ubuntu 24.04.4 /
  Python 3.12.3 / SQLite 3.45.1. Host-locked venv for suites:
  `/opt/mtc-bridge/venvs/a1dd5b46…/bin/python` (pytest 9.1.1, root-owned read-only — do not install
  anything). **Never touch KVM2; never handle key contents.**
- **[AI: Any] LOCKED-LINUX FLOOR CLOSED:** candidate `ebada020` `2 failed, 1357 passed` vs parent
  `637307e8` `25 failed, 1281 passed` — **zero new failure node IDs, 23 fixed**. The 2 remaining are
  the known Python-3.12 order-state GC assertions, present on the parent. Logs
  `C:\tmp\LINUX_FULL_EBADA020_LEAD_2026-08-03.log`, `…PARENT_637307E8_LEAD_2026-08-03.log`.
- **[AI: Any] GLM LAUNCH RULE:** `glm.ps1` makes a fresh empty `CLAUDE_CONFIG_DIR` per run, so an
  unmodified GLM session can execute nothing and will always D025-BLOCK. Launch with an explicit
  permissions mode and `--add-dir` for what it must read, or its verdict is predetermined.
- **[AI: Any] SUPERSEDED — original five-gap list:** (a) **DONE**, see locked-Linux floor above;
  (b) write the integration record; (c) **DONE** — artifact
  identity + secret-scan record at
  `11_TRIAGE/GATE_A_ARTIFACT_IDENTITY_AND_SECRET_SCAN_EBADA020_2026-08-03.md`: manifest hash
  recomputed and matching, nine-category content-redacted scan **0 hits**, built payload shell
  scripts **0 CR bytes** so the A-2 defect is absent from this payload; (d) **PARTIAL** — GLM-5.2
  round 1 BLOCK (environmental), round 2 with granted permissions
  **`PASS-WINDOWS-ONLY-WITH-NITS`, zero required findings**; second flagship still owed;
  (e) **DONE** — host verified live, see above.
- **[AI: Any] DECIDED 2026-08-03 — artifact doc drift ACCEPTED (Barış, option a):** the rebuilt
  `ebada020` artifact ships without `deploy/linux/SECURITY_BASELINE.md` and
  `11_TRIAGE/WPI_READINESS_RECORD_2026-08-01.md` (7,060 → 7,059 entries) because both live on the
  records branch and never landed on `origin/master`. Neither is referenced by Bridge source or the
  Gate A runbook. **No rebuild. `ebada020` stays the frozen build SHA; the security baseline is
  authoritative on the records branch.**
- **[AI: Any] INTEGRATION AUDIT ROUND 1 — `ebada020` NOT ACCEPTED:** GLM-5.2 returned **BLOCK** on
  2026-08-03, **environmental not substantive** — its session could not execute `pytest` (allowlist
  gate, not sandbox) or read `C:\WPI_ARTIFACTS`. **Zero required findings, zero nits.** Every
  read-only claim was reproduced by the Lead, including the decisive one: **the merge dropped,
  duplicated and weakened no test** (name sets HEAD ≡ `f6478e53`, `ebb750da` a strict subset).
  Lead-reproduced Windows floor `1359 passed, 1 warning in 130.09s` in fresh worktree
  `C:\GAAUD_INT_GLM`. Still owed: second flagship `gpt-5.6-sol` xhigh, and the Linux floor. Record
  `11_TRIAGE/GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md`. **To make an auditor session
  count, its allowlist must permit `python -m pytest` and reading `C:\WPI_ARTIFACTS\ebada020…`.**
- **[AI: Any] INTEGRATION RECORD (partial):**
  `11_TRIAGE/GATE_A_INTEGRATION_RECORD_EBADA020_2026-08-03.md` — merge structure, nine-file scope,
  the single `test_wal_state_bundle.py` conflict with before/after and justification, the ledger LF
  refresh with matching `f4cdece5…` hashes, Windows floor `1359 passed`. **Linux floor is `PENDING`
  inside it. It is NOT an acceptance.** Committed on the records branch on purpose — never commit to
  `codex/gate-a-integration`, whose head must stay equal to the artifact's build SHA `ebada020`.
- **[AI: Any] THEN — Gate A from A-0:** transfer as a **single tar**, run A-0…A-9 per
  `11_TRIAGE/GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md` + Addendum A, stop at the
  first FAIL, write `GATE_A_RESULT_2026-08-03.md` either way. A-0 has not been entered; the last
  real verdict is the 2026-08-02 **FAIL at A-2**, and A-3…A-9 have never run.
- **[AI: Any] TRAPS:** bare `git archive` on Windows converts to CRLF and reproduces the A-2 failure
  — use `git -c core.eol=lf archive` and verify zero CR bytes; a `.gitattributes` rule does not
  retroactively renormalise an already-checked-out file; an auditor that cannot execute must BLOCK.
- **[AI: Any] REFS:** `origin/master` `637307e8` (unchanged, nothing merged). Main checkout's local
  `master` is stale at `8721bce0` — always resolve `origin/master`.
- **[AI: Barış] HOURS:** ≈33–36 h of 50 estimated used, ≈14–17 h remaining, exact booking deferred
  to Lead Gate-7. WP-A + WP-R + WP-V total 17 h and are all still ahead. **Re-plan before
  committing to the remainder.**
- **[AI: Any] HOLD:** no master merge, WP-V/deployment, service or runtime change, credentials,
  broker connection, ARM, orders, TESTNET, mainnet, KVM2, Pine/parity/MTC/trading change, or
  economic action.

## GATE A — ALL THREE FROZEN CANDIDATES NOT ACCEPTED (2026-08-02) — SUPERSEDED, see above

- **[AI: Barış] NEXT — OWNER AUTHORIZATION REQUIRED:** open a new protected Bridge repair cycle for
  defect 3b candidate `df00634fc2e5fb19cddb34a6ad16d9764c4779a4`. A non-empty WAL plus a
  zero-byte SHM bypasses the preconnection guard; Lead reproduced `CAPTURED`, three SQLite connects,
  SHM `0 -> 32768`, and bundle/manifest creation on Windows and locked Linux. Repair must refuse
  absent, empty, or invalid SHM before any connection and must provide D026 RED/GREEN evidence.
- **[AI: Any] 3B RECORD:**
  `11_TRIAGE/GATE_A_3B_RETROSPECTIVE_FLAGSHIP_ROUND_2026-08-02.md`. Retrospective round 1 is
  **NOT ACCEPTED / REQUEST_CHANGES**. Claude quota interruption produced no verdict; both detached
  auditor worktrees are restored and clean at `df00634f`.
- **[AI: Any] BUILD:** `c5a4070a` remains **NOT ACCEPTED** under
  `11_TRIAGE/GATE_A_C5A4070A_FLAGSHIP_ROUND_2026-08-02.md`.
- **[AI: Any] QUEUE C:** `5a9bb922` remains **NOT ACCEPTED** under
  `11_TRIAGE/GATE_A_QUEUE_C_FLAGSHIP_ROUND_2026-08-02.md`.
- **[AI: Any] HOLD:** no Queue D integration, artifact rebuild, Gate A rerun, master merge, KVM2,
  credentials, broker connection, ARM, orders, TESTNET, mainnet, wallet, or economic action.

## QUEUE C FROZEN / EXECUTING AUDIT BLOCKED (2026-08-02)

- **[AI: Claude] NEXT AFTER ROSTER RESTORATION:** fresh canonical executing audit of frozen
  credential-free DISARMED candidate `5a9bb922d5255c6a9cb2e8d8b3e7bf9305438002`; reproduce exact
  parent RED, candidate GREEN, and full Windows/Linux floors. It is pushed but **not accepted**.
- **[AI: Any] EVIDENCE:**
  `11_TRIAGE/GATE_A_CREDENTIAL_FREE_DISARMED_CANDIDATE_2026-08-02.md` records exact scope, Lead
  RED/GREEN, unchanged Windows floor, both D025 audit BLOCKs, safety, and cleanup.
- **[AI: Any] DO NOT CLAIM:** Queue C has no temporary acceptance label. Two GLM sessions returned
  no complete executing ledger before timeout/window expiry.
- **[AI: Any] HOLD:** Queue D integration/rebuild/Gate A rerun remains blocked by the defect-3b hard
  stop; no master merge, KVM2, credentials, broker, ARM, orders, TESTNET, mainnet, or economic action.

## GATE A CODEX TAKEOVER - BUILD ACCEPTED / 3B HARD STOP (2026-08-02)

- **[AI: Claude] REQUIRED RETROSPECTIVE:** audit frozen build candidate
  `c5a4070a4836bbb9ee010dc63db69313066667c4` with exact `claude-opus-5` xhigh before any master
  merge or KVM2 action.
- **[AI: Any] BUILD DONE:** `codex/gate-a-build-determinism` is pushed and temporarily accepted as
  `TEMPORARY OWNER-AUTHORIZED CODEX+GLM ACCEPTED - CLAUDE RETROSPECTIVE AUDIT OWED`. It is not
  merged and is not a Gate A pass. Evidence: `11_TRIAGE/GATE_A_REPAIR_VALIDATION_2026-08-02.md`.
- **[AI: Baris] 3B HARD STOP:** `df00634f` is not accepted after the maximum three non-accepting
  audit results. Do not launch round 4. Reopen only as an owner-directed new cycle or through the
  required retrospective flagship route. Evidence: `11_TRIAGE/GATE_A_3B_AUDIT_ROUND1_2026-08-03.md`.
- **[AI: Codex] NEXT, ONLY IF TEMPORARY ROSTER REMAINS ACTIVE:** Queue C - explicit credential-free,
  truthful DISARMED start mode; no broker/network/credential construction; prove ARM rejection and
  D026 RED/GREEN without fake credentials.
- **[AI: Any] HOLD:** Queue D integration/rebuild/Gate A rerun; master merge; KVM2; credentials;
  broker connection; ARM; orders; TESTNET; mainnet; wallet or economic action.

## CODEX TAKEOVER — CLAUDE QUOTA WINDOW (2026-08-02)

- **[AI: Codex] START HERE:** `11_TRIAGE/CODEX_TAKEOVER_HANDOFF_2026-08-02.md`.
- **[AI: Codex] ACTIVE:** collect the exited build repair round 2's two-file uncommitted result in
  `C:\GATEAFIX`; independently audit actual diff/evidence, then exact GLM-5.2 executing audit. Do not
  launch another writer there first.
- **[AI: Codex] NEXT:** adjudicate defect 3b at `df00634f`, then implement the owner-approved explicit
  credential-free DISARMED start mode, integrate accepted commits, rebuild once, and Gate A from A-0.
- **[AI: Any] TEMPORARY ROSTER:** Codex app Lead + isolated secondary Codex CLI implementer + GLM-5.2
  cross-model auditor. Mark temporary acceptance honestly; fresh Claude Opus 5 xhigh retrospective
  audit is owed when quota returns.
- **[AI: Any] HOLD:** no master merge during the temporary window; no KVM2/WP-V, credentials, broker
  connection, TESTNET, mainnet, ARM transition, order, or live-capital action.

## AI ACCOUNT / PROVIDER ROUTING — INSTALLED (2026-08-02)

- **[AI: Any] USE:** canonical secret-free index `AI_ACCOUNT_AND_MODEL_ROUTING.md` for Codex account homes and GLM, Cline, DeepSeek, Grok/xAI, and NVIDIA NIM routes; re-check all usage figures live.
- **[AI: Claude] MANDATORY:** launch Codex only through `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1`; default `secondary` keeps `C:\Users\BarışSemaay\.codex` reserved for the Codex desktop app.
- **[AI: Barış] OPTIONAL/PENDING:** complete device authorization for the isolated `fourth` route (`C:\Users\BarışSemaay\.codex-bsemaay`) when useful. It was still unauthenticated and at 0% until its 2026-08-08 reset at this handoff.

## 50-HOUR DISARMED SAFETY MVP — WP-L/WP-I LOCAL ACCEPTED; GATE A HOST-BLOCKED (2026-08-01)

**START HERE:** `11_TRIAGE/WPI_CANDIDATE_ACCEPTANCE_RECORD_2026-08-01.md` — local/static WP-I candidate evidence accepted. Then `_AI_MEMORY/GLOBAL_HANDOFF.md` RESUME HERE. Acceptance scope is owner-continuity / Claude-waiver local/static WP-I candidate evidence only.

- **[AI: Codex] DONE — WP-L Phase 1:** verification only, accepted. WPL branch `codex/50h-wpl-verification` pushed at `d9d38d9b…`; record `11_TRIAGE/WPL_PHASE1_VERIFICATION_RECORD_2026-08-01.md`.
- **[AI: Codex] DONE — WP-I local/candidate evidence:** accepted. Candidate SHA `1adf9ae5…`, path `C:\WPI_ARTIFACTS\1adf9ae5…`, manifest `bfefea2f…`; 7,060 manifest entries / 7,061 files / 1,051,904,669 bytes / nine content-redacted categories all zero. Record `11_TRIAGE/WPI_CANDIDATE_ACCEPTANCE_RECORD_2026-08-01.md`.
- **[AI: Barış] NEXT — identify one expendable Ubuntu 24.04 host and non-secret reachability:** credentials owner-held and never handled by an agent. Active KVM2 is forbidden as a substitute.
- **[AI: Codex] THEN — Gate A verification:** followed by WP-L Phase 2, WP-I staging, Audit 2, WP-A on the same retained host.
- **[AI: Any] HOLD:** active KVM2 and all ARM / order / live-capital actions.
- **[AI: Any] HOURS:** historical hours remain **20.5 h used / 29.5 h remaining**; exact WP-L / WP-I booking deferred to **Lead Gate-7**.

## 50-HOUR DISARMED SAFETY MVP — S3-STRUCT CYCLE AUTHORISED (2026-08-01)

**START HERE:** `11_TRIAGE/WPS_S3_STRUCTURAL_CYCLE_HANDOFF_2026-08-01.md` — standalone handoff with
Gate-1 scope, allowlist, exact CLI recipe, ten operational hazards, funding position and definition
of done. Then `_AI_MEMORY/GLOBAL_HANDOFF.md` RESUME HERE. Authorisation
`11_TRIAGE/OWNER_AUTH_50H_EXECUTION_PROMPT_2026-07-31.md` + **D027**.
Roles this execution only: **Claude Lead/acceptance, Codex `gpt-5.6-sol` implementer.**

- **[AI: Claude] DONE — WP-0 (2.0/2 h):** merged via PR #36.
- **[AI: Claude] DONE — WP-S S2 closure:** **ACCEPTED at `0c65a731`**, both flagships PASS-WITH-NITS.
- **[AI: Claude] HARD-STOPPED — minimum S3:** `732b37c3` NOT accepted after 3 rounds. Five required
  findings, both flagships, three classes. Record `11_TRIAGE/WPS_S3_HARD_STOP_2026-08-01.md`.
- **[AI: Codex] NEXT — S3-STRUCT round 1 (D027):** structural fix. **S3T-A** validated accessor
  boundary over durable `orders`/`fills`/`trades` reads returning a containable fault instead of
  raising · **S3T-B** close path re-derives, inside its existing `BEGIN IMMEDIATE`, that the trade is
  still bound to the active episode · **S3T-C** `_event_symbol` and `_canonical_status` routed
  through the boundary · **S3T-D** matrix-generated acceptance suite over every durable column ×
  {NULL, non-numeric TEXT, out-of-range int, non-finite float}. **A hand-listed test covering only
  the five known findings does not close the class and will not be accepted.**
- **[AI: Claude] THEN:** independently reproduce representative REDs, re-run the suite against the
  `2 failed, 1140 passed` floor, freeze the SHA, dispatch canonical audits. Max 3 non-accepting
  rounds; a third stops the cycle and goes to Barış.
- **[AI: Claude] AFTER Audit 1 accepts:** merge WP-S, then **WP-L Phase 1 as verification only** —
  F-0-1 proved the Linux package at `6fe0130f` is already an ancestor of master and byte-identical,
  so there is no porting and no cross-branch Git operation. **No Ubuntu execution before Gate A.**
- **[AI: Cline] THEN — WP-I mechanical artifacts:** SBOM, secret scan, outbound-network inventory,
  lockfile verification, staging test plan, rollback procedure. Unprotected and bounded; Cline is
  owner-verified at `3.0.48`. Lead audits every result on real data, never the report.
- **[AI: Claude] CARRY TO WP-A — I-R4 SIGTERM clean shutdown:** highest-risk minimum restart
  invariant. §19 forbids SMALL-GAP treatment — resolve with executed evidence on the retained
  staging host, or BLOCK. No shutdown-path code change authorised on the WP-0 record alone.
- **[AI: Claude] BEFORE any TESTNET work:** write the TESTNET-phase pre-registration and pass it
  through one fresh Gate-5 audit. The 50-hour plan's acceptance does not cover that phase.
- **[AI: Barış] BUDGET:** S3-STRUCT does not fit the remaining 2.0 h of contingency. Hours are
  recorded as an owner-authorised extension, not absorbed. If implementation exceeds ~6 h it is
  reported rather than continued quietly.
- **[AI: Barış] EXTERNAL CEILING:** WP-L Phase 2, WP-I staging, WP-A and WP-V need a named Ubuntu
  24.04 host **and access to it**. Credentials are owner-held and must never be handled by an agent.
- **[AI: Barış] LIVE-CAPITAL GATE — unchanged.** Mainnet readiness work with no economic effect is
  authorised; mainnet capital is not.
- **[AI: Any] HOLD:** no Ubuntu execution, staging, VPS, deployment, TESTNET, ARM, broker or runtime
  action until its own documented gate prerequisites objectively pass.

## CANONICAL AUDIT ROSTER EXPANDED — D025 (2026-08-01)

- **[AI: Any] APPLY:** four canonical Gate-5/6 auditors now — `claude-opus-5` xhigh,
  `gpt-5.6-sol` xhigh, `cline-pass/deepseek-v4-flash` via Cline, GLM-5.2 via Z.AI. Rules in
  `AGENTS.md` §CANONICAL AUDIT ROSTER: an auditor that cannot execute the suite must **BLOCK**;
  a required finding from any auditor binds **after the Lead reproduces it on real source**;
  acceptance needs both flagships accepting plus no unresolved reproduced required finding.
- **[AI: Any] REMEMBER:** GLM-5.2 once returned PASS-WITH-NITS on a commit carrying two severe
  defects while unable to run the suite at all. That event is why the BLOCK-on-non-execution rule
  exists.
- **[AI: Any] AUDIT AUTHORITY ONLY:** D025 grants secondary models **no** implementation authority.
  Protected Bridge/core-runtime implementation stays with the flagship implementer.
