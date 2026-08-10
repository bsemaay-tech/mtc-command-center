# NEXT_STEPS

## PERMANENT AUDIT TIERS — apply immediately to active RP7/WP-I work (2026-08-10)

**[AI: Claude Lead]** Re-read `AGENTS.md` §AUDIT TIER POLICY — PERMANENT DEFAULT and record the
current Gate-1 tier before the next audit dispatch. `RP7-WPI-RO.sh` is T0 because it is a run-kit script
intended for staging-host execution: two fresh flagships (`claude-opus-5` + `gpt-5.6-sol`) at xhigh,
maximum three rounds. Count the existing Claude audit only if fresh-session + xhigh launch evidence is
confirmed; its report currently omits effort. After repair/green evidence, run the fresh Codex xhigh slot.
Do not add GLM/DeepSeek unless an explicit tier slot or later owner contract requires it.

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

## GLM SUPPLEMENTAL ROUTING POLICY — IMPLEMENTED 2026-07-27

Policy codified in `AGENTS.md` §GLM SUPPLEMENTAL ROUTING (canonical, do not copy table elsewhere). Cross-references added to all required files. Stale `claude-opus-4-8` → `claude-opus-5` fixed in `SPRINT_WORKFLOW.md`.

- **[AI: Barış] AUTHORIZE (separate gate):** reconfigure the external helper that currently hard-maps all three tiers to GLM-5.2. No external config was changed in this update; this requires explicit Barış authorization before any helper change.
- **[AI: Any] MONITOR (Sep 2026):** temporary 1× off-peak quota cap expires Sep 2026. When quota rules change or new model entitlements are confirmed, update `AGENTS.md` §GLM SUPPLEMENTAL ROUTING (time-stamped facts are there).
- **[AI: Any] VERIFY on route change:** if active Z.AI route changes, confirm GLM-5.1 Coding Plan entitlement and update Tier 3 in `AGENTS.md` accordingly.
- **[AI: Any] HOLD:** no runtime, tool, broker, Pine, or schema changes in scope. Changes are doc/memory only.

## KVM2 MASTER PROGRAM — REPAIR CYCLE 2 ACTIVE / CLAUDE QUOTA BLOCKER (2026-07-26)

- **[AI: Codex] SCHEDULED:** one-time same-thread continuation
  `resume-kvm2-plan-repair-after-claude-reset` will run at 10:51
  Europe/Chisinau after the reported Claude reset.
- **[AI: Claude] FIRST AFTER 10:50 EUROPE/CHISINAU:** run the preserved focused
  repair prompt
  `11_TRIAGE/KVM2_MASTER_PLAN_REPAIR_CYCLE2_ROUND1_PROMPT_2026-07-26.md`
  against only the two plan documents and joint audit prompt. This is repair
  round 1 of the newly authorized cycle; do not replace Claude with another
  implementer.
- **[AI: Codex] THEN:** independently verify 77 unique exact Evidence/Stop task
  blocks, hashes, task counts, P5-05A/P5-06 and P6-03/P6-04/P6-05 dependencies,
  Phase-9 independent Gate 6 manifest acceptance and install→observe→remove
  sequencing, authority separation, privacy, sizes, crosswalk 1–10, and all
  original R3/DS findings.
- **[AI: Codex + Claude Opus] AUDIT:** only after lead validation passes, run fresh
  exact `gpt-5.6-sol` `xhigh` and `claude-opus-5` `xhigh` no-fallback audits. A
  non-accepting verdict returns to the same Claude implementer; maximum three
  repair/re-audit rounds in this new cycle.
- **[AI: Any] HOLD:** the current working hashes are not execution acceptance.
  No VPS/runtime, install, secret, network, deploy, cutover, TESTNET, ARM, lab,
  reprovision, purchase, mainnet, staging, commit, push, or PR action.

Current unaccepted working hashes: master
`3C61B08B17867C2EEB602FD407CF327C95FF7446DB492304DDB6A926A3E8EF3C`;
execution companion
`CB4C686A161CA8D40DC6C1C235B6371A4ADE1DCDDA23D2535259F39E0177C885`.

## KVM2 MASTER PROGRAM — FINAL AUDIT REQUEST_CHANGES / LOOP EXHAUSTED (2026-07-26)

Canonical joint inputs:

- `11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md`
- `11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`
- `11_TRIAGE/KVM2_MASTER_PLAN_MULTI_MODEL_AUDIT_REPORT_2026-07-26.md`

- **[AI: Barış] NEW-CYCLE GATE:** explicitly authorize a new bounded repair cycle.
  The prior three-round repair/re-audit limit is exhausted; do not silently start
  a fourth round.
- **[AI: Claude] REQUIRED REPAIR:** apply only R3-01 through R3-07 and DS-F-01
  from the consolidated report. Preserve preparation-only status and all runtime
  authority separations.
- **[AI: Codex] REQUIRED RE-AUDIT:** after new joint hashes are frozen,
  independently reproduce the dependency graph, authority chain, task schema,
  crosswalk, privacy scan, and all required findings at exact
  `gpt-5.6-sol` `xhigh`.
- **[AI: Claude] DEFERRED CANONICAL AUDIT:** when credits are available, run a
  fresh exact `claude-opus-5` `xhigh`, no-fallback/no-resume audit. The current
  missing Opus verdict is not evidence.
- **[AI: Any] HOLD:** no install, deploy, secret transfer, runtime/API/process,
  cutover, TESTNET, ARM, lab admission, network change, reprovision, purchase,
  or mainnet action. The lower Bridge VPS Deploy task remains BLOCKED.

Frozen current hashes: master
`10C79396D63DE330BD4F920146B8CDB0C39C10C342233AEAE4E1C8B9CCD12F02`;
execution companion
`8706621CE52010465B408B265267F7320078E2A79F01533E85513335619615D9`.

## KVM2 MASTER PROGRAM — PLAN READY / ALL EXECUTION GATED (2026-07-25)

Canonical master plan:
`11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md`.

- **[AI: Any] FIRST:** re-verify drift-prone VPS, repo, PR, SHA, Windows writer,
  bridge state, listener, and audit facts. Resolve the audit-model wording conflict
  between current `AGENTS.md`/D020 and the older Bridge VPS task before launching
  any audit.
- **[AI: Claude] PREPARATION:** produce the two-profile clean rebuild kit
  (`temporary-testnet-lab` and `future-trading-only`) with trusted inputs, locked
  dependencies, service/firewall/ownership manifests, secret inventory without
  values, consistent state recovery, encrypted off-host restore proof, teardown,
  credential rotation, and reproducible bootstrap evidence. Do not install.
- **[AI: Any] AUDIT:** submit the immutable master plan and each executable child
  artifact to fresh exact-model Gate 5/Gate 6 review under the current canonical
  roster. Maximum three non-accepting repair rounds; no fallback.
- **[AI: Barış] OWNER GATES:** bridge deploy, cutover, ARM, each AI-lab workload,
  network exposure, destructive reprovision, purchase, and mainnet remain separate
  explicit decisions. AI-lab admission is forbidden until the canonical
  bridge-only stability window is accepted.
- **[AI: Any] HOLD:** no GitHub self-hosted runner, public bridge/webhook control
  path, agent Docker socket, heavy backtest, local large LLM, or mainnet on the
  mixed/lab image.

No install, deploy, secret, runtime, cutover, TESTNET, ARM, lab, network,
reprovision, purchase, or mainnet action is currently authorized.

## BRIDGE VPS DEPLOY — VPS READY / DEPLOY BLOCKED (2026-07-25)

Canonical preparation task:
`11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`.

- **[AI: Claude] BUILD/AUDIT HANDOFF GATE:** prepare an exact clean merged release
  SHA containing accepted TS-P0 plus Linux deployment repairs, pinned/hash-locked
  Python 3.12 venv dependencies, non-root hardened systemd, private loopback-only
  control access, state-continuity policy, and complete release/rollback evidence.
  Obtain fresh independent Gate 5 and Gate 6 acceptance; do not deploy.
- **[AI: Any] READ-ONLY VERIFICATION GATE:** before any owner decision, re-verify
  live PR/SHA/runtime/reconcile/order/position/port/audit state because the task
  snapshot can drift. Preserve the dirty-main-worktree ban and single-writer stop
  sequence. The current exact `gpt-5.6-sol` `xhigh` verdict is **BLOCK with zero
  optional nits**; the HTTP-429 Opus attempt is not evidence.
- **[AI: Barış] OWNER GATES:** formally choose database migration versus a
  conservative risk-state reset; later authorize deploy only after exact audits;
  authorize ARM separately, if ever. The >=10-day counter starts only at the final
  approved VPS ARM. No current merge/deploy/install/secret/runtime/TESTNET/ARM
  authority; mainnet remains forbidden.

## TS-P1-001 SECOND-REPAIR RE-AUDIT BLOCK — immutable holder repair required

- **[AI: Claude] NOW:** run
  `11_TRIAGE/CLAUDE_TSP1001_REPAIR3_PROMPT_2026-07-21.md` against exact parent
  `a15a6b1f6648016fe99278fe993daa2c1b49b923`. Fix only the writable `_pairs`
  holder; create one new local child commit.
- **[AI: Codex] AFTER REPAIR:** independently audit the new immutable commit without
  repairing it in the audit pass.
- **[AI: Baris] OWNER GATE:** only after technical PASS, accept or reject the PROPOSED
  TS-P1-001 contract and five open design questions.
- **[AI: Any] HOLD:** do not create or execute TS-P1-002; no push/PR/merge/migration/
  testnet/P2RT/deployment authority.

Verified: parent RED 5 failed/80 passed; repaired focused 85/85; full 303/303 both
CWDs; compile clean; oracle 44/121; F2-R closed. Residual direct-slot mutation evidence
is in `11_TRIAGE/CODEX_TSP1001_REAUDIT2_2026-07-21.md` (**BLOCK**).

## TS-P1-001 RE-AUDIT BLOCK — second bounded repair required

- **[AI: Claude] NOW:** run
  `11_TRIAGE/CLAUDE_TSP1001_REPAIR2_PROMPT_2026-07-20.md` against exact parent
  `851d88a084875e48b63fba455cb7b27f357c5ac4`. Fix only mutable proxy referents and
  hostile-metaclass error escape; create one new local child commit.
- **[AI: Codex] AFTER REPAIR:** independently re-audit the new immutable commit; do
  not repair it in the audit pass.
- **[AI: Baris] OWNER GATE:** only after technical PASS, accept or reject the PROPOSED
  TS-P1-001 invariant contract and its five open design questions.
- **[AI: Any] HOLD:** do not create or execute TS-P1-002. No push, PR mutation, merge,
  migration, testnet, P2RT, or deployment authority is implied.

Verified evidence: repair regressions RED on parent (5 failed/75 passed), repaired
focused 80/80, full 298/298 from both CWDs, compile clean, scope clean, oracle 44/121.
Residual F1-R/F2-R runtime attacks are in
`11_TRIAGE/CODEX_TSP1001_REAUDIT_2026-07-20.md` (**BLOCK**).

## TS-P1-001 AUDIT BLOCK — repair commit and independent re-audit required

- **[AI: Claude] NOW:** run
  `11_TRIAGE/CLAUDE_TSP1001_REPAIR_PROMPT_2026-07-20.md` in a fresh session against
  audited parent `5140e062b8c1f3fcc78e96c7357060c60a51285d`. Fix only the reproduced
  mutable-policy and exception-contract findings; create one new local repair commit.
- **[AI: Codex] AFTER REPAIR:** independently re-audit the new immutable commit. Do
  not act as builder in the re-audit pass.
- **[AI: Baris] OWNER GATE:** after a passing re-audit, accept or reject the PROPOSED
  TS-P1-001 invariant contract, including the five open design questions.
- **[AI: Any] HOLD:** do not create or execute a TS-P1-002 build prompt yet. No push,
  PR mutation, merge, migration, testnet, P2RT, or deployment authority is implied.

Audit evidence: `11_TRIAGE/CODEX_TSP1001_AUDIT_2026-07-20.md` (**BLOCK**). Scope,
semantic parent RED, 74 focused tests, 292 full tests from both CWDs, compile, and the
121-pair/44-legal oracle passed; the mutable backing seeds and unsafe/unreason-coded
exceptions block acceptance.

## 🟦 39-TASK SEQUENCE START — TS-P1-001 builder then independent Codex audit

Barış selected the workflow: Claude builds one backlog task and reports; Codex audits
the immutable commit, routes BLOCK back to repair or PASS forward to the next task.
First task: TS-P1-001 canonical order-state invariants. Prompts:

- Claude builder: `11_TRIAGE/CLAUDE_TSP1001_BUILD_PROMPT_2026-07-20.md`
- Codex auditor/manager: `11_TRIAGE/CODEX_TSP1001_AUDIT_MANAGER_PROMPT_2026-07-20.md`

One task at a time. No next task, push, merge, deploy, migration, or testnet action is
implied by build/audit success. TS-P1-001 invariant contract remains Barış-accepted only
after the independent audit and explicit owner review.

## ✅ TS-P0 DOCUMENTATION CLOSEOUT DONE — PR #25 ready at `cfb08b81`

N3/N4/N5 are closed. The tracked contract markers and N5 limitation were committed
as `cfb08b81` and pushed; PR #25 is OPEN, non-draft, CLEAN, with available checks
passing: https://github.com/bsemaay-tech/mtc-command-center/pull/25. N3/N4 live only
in pre-existing untracked main-worktree docs and remain deliberately uncommitted;
they were not smuggled into the TSP0 branch.

- **[AI: Barış] MERGE GATE:** still requires an explicit “merge PR #25” instruction.
- **[AI: Barış] DEPLOY GATE/TIMING:** separately decide after merge and after the chosen
  Day 1 v2 checkpoint; deployment would interrupt the current window.
- **[AI: Codex|Claude] NEXT LARGE TASK AFTER TS-P0 MERGE:** design TS-P1-001 canonical
  order-state invariant contract for Barış review; no implementation before its gate.

Report: `11_TRIAGE/CODEX_TSP0_DOC_CLOSEOUT_REPORT_2026-07-20.md`.

## ✅ TS-P0 published + Day 1 v2 OPEN 2026-07-20

Owner gates are closed: hash scope approved, release-evidence contract approved, and
sticky reset policy confirmed with 300-second tolerance. Exact audited commit
`44338d61` was pushed on `feature/ts-p0-baseline`; draft PR #25 targets `master`:
https://github.com/bsemaay-tech/mtc-command-center/pull/25. **No merge or deploy.**

Day 1 v2: monitoring PC awake policy verified (sleep/hibernate/lid action all disabled
on AC and DC); exactly one task start and one ARM succeeded. Run
`paper-20260720090332` is ARMED paper/testnet from `2026-07-20T09:05:10Z`, task Running,
fresh reconcile, positions/orders empty, P2RT clean at `008e065e`, thresholds unchanged.
Record: `11_TRIAGE/CODEX_TSP0_PUBLICATION_DAY1V2_2026-07-20.md`.

- **[AI: Any] MONITOR DAY 1 v2 READ-ONLY:** keep evidence categories separate; any
  interruption resets the continuous window under the confirmed sticky policy.
- **[AI: Codex] NEXT DOCS-ONLY CLOSEOUT:** execute
  `11_TRIAGE/CODEX_TSP0_REMAINING_DOCS_PROMPT_2026-07-20.md` for N3/N4/N5 and approval
  markers. No commit/push/PR mutation until a separate reviewed docs-only gate.
- **[AI: Barış] PR #25:** merge and deploy remain explicitly unapproved.

## ✅ INCIDENT FOLLOW-UP 2026-07-20: Day 1 v1 closed; Day 1 v2 opened

Bridge died with system sleep; logon-trigger restart at 08:57 died again in ~66s
(second standby). Continuous window = ARM 18:52Z → ~04:27Z ≈ **9h35m**, then INTERRUPTED.
Not related to any TSP0 session. Record: `11_TRIAGE/INCIDENT_D1V1_SLEEP_STOP_2026-07-20.md`.

- **RESOLVED:** Barış selected the awake-PC policy and authorized Day 1 v2. Exactly one
  task start and one ARM succeeded; see the top entry and execution record.
- **STANDING LIMIT:** local remains validation-tier; definitive uninterrupted evidence
  remains planned for VPS.

## ✅ TS-P0 BLOCK REPAIR RE-AUDIT PASS 2026-07-20 — published at `44338d61`

Fable independently re-audited the Codex nine-file repair: **PASS, zero new findings**
(`11_TRIAGE/FABLE_TSP0_BLOCK_REPAIR_AUDIT_2026-07-20.md`). Reproduced: 218×2 both CWDs;
RED 9F/45P vs HEAD (copy-aside, byte-exact restore); F1a×4/F1b/F2×5/F3 replays all
fail-closed; overbroad-denylist attack clean (real-tree hash set unchanged); real-pair
exit 2 incl. `repo_dirty`; P2RT untouched. Auditor committed the audited state as
**`44338d61`** to end the uncommitted-repair hazard. Barış later closed all three owner
gates and authorized exact-SHA publication; draft PR #25 is open with no merge/deploy.

- **[AI: Any] DOCS NITS (small, unblocked):** close N3 integration-note, N4 three stale
  ADR "Proposed status" sentences, N5 symlink limitation — docs-only pass.
- **DONE:** hash scope approved; release contract approved; sticky reset policy confirmed
  with 300-second tolerance; exact `44338d61` pushed and draft PR #25 opened.
- **[AI: Barış] REMAINING GATE:** any docs follow-up commit/push, PR merge, or deploy needs
  a separate explicit instruction.

Repair report: `11_TRIAGE/CODEX_TSP0_BLOCK_REPAIR_REPORT_2026-07-19.md`.

## ⛔ CODEX TS-P0 CROSS-AUDIT BLOCK 2026-07-19 — repair before push/PR

- **[AI: Claude] TS-P0-003 REQUIRED REPAIR:** malformed persisted timestamp
  evidence (especially `window_interrupted_ts`) must fail DOWN, and future
  liveness must not count as fresh. Add committed invalid-meta/future-clock tests.
- **[AI: DeepSeek] TS-P0-002 REQUIRED REPAIR:** validate manifest container and
  scalar types before dereference; re-signed `"hashes": []` must return a
  structured exit 2 without traceback. Add wrong-shape tests.
- **[AI: DeepSeek] TS-P0-001 REQUIRED REPAIR:** extend/document secret exclusions
  for conventional `*.env` and `*.secrets`; decide `key.txt`; add spy/no-leak tests.
- **[AI: Codex] RE-AUDIT AFTER REPAIR:** rerun focused 14/11/21, 210/210 both
  CWDs, real-pair integration, and the three failed adversarial probes. Keep
  `C:\P2RT` read-only. Report: `11_TRIAGE/CODEX_TSP0_AUDIT_2026-07-19.md`.
- **[AI: Barış] PUSH/PR GATE:** remains blocked. The final-HEAD integration's
  third `source_tree_hash_mismatch` reason is correct and must not be removed by
  weakening the declared hash scope.

## ✅ DEPLOYED + WINDOW OPEN 2026-07-19 — Day 1 v1 ARMED on `008e065e`; monitor + TS-P0-001 next

Barış approved and Fable executed the full deploy gate: PR #24 merged (`008e065e`),
`C:\P2RT` deployed + verified (32/164 tests in deployed tree), `MTC-Bridge-P2` started
18:50:25Z, run `paper-20260719185026` paper/testnet ARMED ~18:52:44Z. Record:
`11_TRIAGE/DEPLOY_TSP1007_WINDOW_D1_2026-07-19.md`.

- **[AI: Any] WINDOW MONITORING:** check bridge log + `/api/status` + events periodically;
  this window's risk-gate enforcement evidence COUNTS (first deployed audited wiring).
  Categories stay separate (connectivity / reconnect / scheduler / risk-enforcement).
  Definitive ≥10d D3 on VPS remains end-of-month plan.
- ~~**[AI: Claude] PHASE 0 BUILD CHAIN (Barış directed 2026-07-19, Fable builds)**~~
  **DONE 2026-07-19:** TS-P0-001..004 built in `C:\TSP0` (`feature/ts-p0-baseline`,
  commits `fa449ce2`/`42d0ca9f`/`7777273f` + docs-only P0-004), 210/210 both CWDs,
  no push/deploy, window untouched. Report: `11_TRIAGE/FABLE_TSP0_BUILD_REPORT_2026-07-19.md`.
- ~~**[AI: Codex] INDEPENDENT TS-P0 AUDIT**~~ **FABLE AUDIT DONE 2026-07-19:
  PASS-WITH-NITS** (`11_TRIAGE/FABLE_TSP0_INDEPENDENT_AUDIT_2026-07-19.md`).
  Fresh Fable session executed the full 12-point checklist: 210/210 both CWDs,
  3 RED proofs reproduced, real-pair integration exit 2 + P2RT untouched, re-sign
  attack caught, exhaustive window sweep verified. 5 nits: N1 release_evidence
  exit-1 crash on re-signed non-dict `hashes`; N2 `prod.env` denylist gap;
  N3 handoff's stale integration expectation (3 drift reasons at HEAD is CORRECT);
  N4 three residual "Proposed status" sentences (ADR-0020:62/0025:51/0029:49);
  N5 symlink digest-oracle note. **[AI: Barış]** decide: accept Fable audit or
  also run Codex cross-audit per `CODEX_TSP0_AUDIT_PROMPT_2026-07-19.md`; push/PR
  of `feature/ts-p0-baseline` stays gated until then.
- **[AI: Codex|Claude] TS-P0 NIT-FIX BUILD (after Codex audit reconciled):**
  execute `11_TRIAGE/TSP0_NITFIX_BUILD_PROMPT_2026-07-19.md` — N1 exit-code fix
  (TDD, subprocess RED), N2 conditional on Barış hash-scope answer, N4 three ADR
  wording fixes, N5+N3 doc corrections; one commit in C:\TSP0, no push. Stage 2
  push/PR separately gated on Barış's 3 approvals.
- **[AI: Barış] TS-P0 decisions after audit:** (1) TS-P0-001 hash scope confirm
  (RUNTIME_BASELINE_CONTRACT.md), (2) TS-P0-002 release-evidence contract approval
  (currently DRAFT), (3) TS-P0-003 window reset-policy confirm (currently PROPOSED).
- **[AI: Claude|Codex] NON-BLOCKING NITS (fold into full TS-P1-007):**
  add committed tests for `ORDER_OVERFILL` + `FILL_ROLE_CONFLICT`; persist the conflicting
  role fill as evidence (retention asymmetry); close the narrow ENTRY_REMAINDER_LIVE
  crash window (missed DISARM only); fix stale "INSERT OR REPLACE" comment at
  `tests/test_interim_risk_wiring.py:674`.
- **[AI: Barış]** live/mainnet remains BLOCKED (gate unsigned); D017 funding exclusion
  stands until TS-P1-005 funding ledger.

## ✅ INTERIM TS-P1-007 ROUND-4 AUDIT PASS-WITH-NITS 2026-07-19 — deploy executed above

Fable independently audited `acb83b5b` and issued **PASS-WITH-NITS**
(`11_TRIAGE/FABLE_INTERIM_TSP1007_ROUND4_AUDIT_2026-07-19.md`). All builder evidence
reproduced (32×2 focused, 164×2 full, parent red 8F/24P exact-match, half-exit 1F vs
`066b49cc`) plus 14 independent adversarial probes, all pass. All five round-3 BLOCK
findings closed.

## INTERIM TS-P1-007 ROUND-4 REPAIR BUILT 2026-07-18 - audited PASS-WITH-NITS above

Codex commit **`acb83b5b`** in clean `C:\P1IF` repairs the round-3 late/conflicting-fill,
partial-decision, live-entry-remainder, overfill, atomic-close, and semantic-test findings.
Evidence: **32x2 focused; 1x2 regression; 164x2 full; parent semantic red 8F/24P; old-code
half-exit red 1F; final clean 32P**. Audit brief:
`11_TRIAGE/FABLE_INTERIM_TSP1007_ROUND4_AUDIT_HANDOFF_2026-07-19.md`.

- ~~**[AI: Claude] FABLE INDEPENDENT AUDIT 2026-07-19**~~ DONE 2026-07-19: PASS-WITH-NITS.
- **[AI: Barış] DEPLOY GATE:** remains separate and unspent. No push, PR, merge, or deploy before
  explicit owner approval. D017 funding exclusion is unchanged.
- The round-3 repair bullets immediately below are completed by `acb83b5b` and now
  independently confirmed by Fable; retained as audit trace.

## ⛔ INTERIM TS-P1-007 ROUND-3 RE-AUDIT BLOCKED 2026-07-18 — do not push/deploy

Codex audited `3fa13f3e` code plus documentation-only D017 commit `b11a2e36`. Scope and reported suites passed (**24×2 focused; 156×2 full; regression ×2; semantic red 5F/19P**), but late/conflicting fills can still rewrite closed PnL or leave unprotected exposure. Report: `11_TRIAGE/CODEX_INTERIM_TSP1007_REAUDIT2_2026-07-18.md`.

- **[AI: Claude] REQUIRED REPAIR:** closed trades must be immutable. Detect `exit_qty > entry_qty`, mixed SL/TP/CLOSE races, and any distinct post-close fill; persist the anomaly separately and force reconciliation/quarantine without rewriting canonical PnL. Make close + `TRADE_CLOSED` atomic.
- **[AI: Claude] REQUIRED REPAIR:** replace mutable `INSERT OR REPLACE` fill semantics with insert-once outcomes. Exact duplicates are no-ops; changed payloads for an existing `fill_id` fail closed; partial-exit decisions remain idempotent across restart.
- **[AI: Claude] REQUIRED REPAIR:** do not terminally close a flat partial entry while its owned entry remainder is live. Cancel/confirm or quarantine it; a later entry fill must never become `FOREIGN_POSITION_IGNORED`. Add restart/reconcile proof.
- **[AI: Claude|DeepSeek] TEST REPAIR:** make the half-exit engine test cross the old `-2000` daily boundary; its current old-code phantom loss is only `-100`, so the test is not semantic red evidence.
- **[AI: Codex] RE-AUDIT:** rerun both-CWD suites and semantic red proof, plus mixed SL/TP, conflicting duplicate, partial-decision duplicate, late-entry, crash-window, and reconciliation attacks.
- **[AI: Barış] DEPLOY GATE:** remains separate and unspent. D017 funding exclusion is accepted and is not the current blocker; no monitoring window may count before a non-BLOCK audit and separate deploy approval.

## 2026-07-18 REVIEW OUTCOME — pending Barış approvals + corrections applied [AI: Fable]

Devil's-advocate review of the 2026-07-17 package: **PROCEED WITH REQUIRED CORRECTIONS** (full record: GLOBAL_HANDOFF 2026-07-18). Corrections applied same day. Pending Barış approvals, in priority order:

1. ⛔ **Interim TS-P1-007 round-3 audit BLOCK.** D017 accepted interim funding exclusion, but `3fa13f3e` remains unsafe under post-close overfill/mixed-role fills, conflicting duplicate IDs, and late fills from a remaining partial-entry order. Complete the narrow repairs above, then independent re-audit; no push/PR/deploy or risk-control monitoring window yet.
2. ✅ **PR #23 MERGED 2026-07-18T12:20:45Z** (merge commit `abda6717`; Barış approval, executed by Fable). Verified: `74e0990b` is an ancestor of `origin/master` and `git diff 74e0990b origin/master -- IBKR_PAPER_BRIDGE/` is empty — master bridge tree is byte-identical to the deployed runtime. TS-P0-001 manifests must baseline against post-merge master.
3. ✅ **ADR ratification COMPLETE — D016 + same-day addendum (2026-07-18):** Barış accepted ALL TWELVE (ADR-0018 through 0029); files + index flipped. Qualifications: 0020/0024 direction-only (evidence-gated); 0029 framework-only — live gate UNSIGNED, live/mainnet BLOCKED, nothing operational signed.
4. ✅ **Scheduler policy — DONE 2026-07-18:** `StopIfGoingOnBatteries=False` on `MTC-Bridge-P2` (set by Fable; task stayed `Ready`); Task Scheduler history ENABLED (Barış ran the admin wevtutil command). `DisallowStartIfOnBatteries` remains True (untouched — task will not START while on battery; flag to Barış if unwanted).

## TRADING-SYSTEM ROADMAP — SINGLE IMMEDIATE NEXT TASK 2026-07-17 [AI: DeepSeek]

**TS-P0-001 — Add a read-only repository/runtime baseline manifest and drift checker.**

Governing ADRs: ADR-0019 and ADR-0027. Canonical task card:
`09_DOCS\ROADMAPS\TRADING_SYSTEM\05_IMPLEMENTATION_BACKLOG.md#ts-p0-001--add-a-read-only-repositoryruntime-baseline-manifest-and-drift-checker`.

Exact scope:

- Add an offline CLI that compares an explicitly supplied repository root and runtime root.
- Read Git HEAD/status and selected bridge source/config hashes; emit deterministic JSON and Markdown evidence.
- Exit `0` for exact clean match, `2` for drift/dirty/missing runtime, and `3` for invalid evidence input.

Required files:

- `IBKR_PAPER_BRIDGE\tools\check_runtime_baseline.py`
- `IBKR_PAPER_BRIDGE\tests\test_runtime_baseline.py`
- `IBKR_PAPER_BRIDGE\docs\RUNTIME_BASELINE_CONTRACT.md`
- One dated run report plus normal `GLOBAL_HANDOFF.md`/`NEXT_STEPS.md`/`ACTIVE_FILES.md` updates.

Acceptance criteria and tests:

- Manifest reports schema version, canonical paths, repository/runtime commits and dirty flags, selected hashes, config hash and explicit verdict.
- Unit coverage: clean match, commit drift, dirty repo/runtime, missing runtime, changed config, invalid Git output, stable ordering, secret-safe output and no-mutation behavior.
- One audited read-only local invocation must report the current repository/runtime relationship while leaving both trees unchanged.

Explicit out of scope: no branch merge, checkout, deploy, restart, ARM/DISARM/KILL, HTTP/exchange call, credential read, database or scheduler action, dependency/config/schema change, or trading/risk/order/strategy behavior change. `C:\P2RT` remains protected. The bridge API was unavailable during the 2026-07-17 roadmap baseline, so the prior Day 0 v5 window must not be represented as currently active or uninterrupted.

## ❌ P2 DAY 0 v5 CLOSED 2026-07-18 — killed by scheduler battery policy 2026-07-16 ~17:32 (see `11_TRIAGE/INCIDENT_P2_BATTERY_STOP_2026-07-16.md`); 300s fix remains deployed + field-proven; NO active window; daily D3 check suspended until next approved window

Task B (`79976577`+`74e0990b`, PR #23 draft) Fable-audited **PASS** and deployed same day:
P2RT detached `74e0990b`, 132×2 both CWDs (incl. inside P2RT), supervisor `MTC-Bridge-P2`, run
`paper-20260716132819`, >13-min gate, ONE ARM, flat. **Live proof: a real HL outage during the
gate ended with the first fresh bar 118s after reconnect — the old 60s trigger (v4 killer)
would have disarmed; the 300s window absorbed it** (zero DATA_STALE/ERROR). Full record:
`11_TRIAGE/FABLE_AUDIT_P2_TIMEOUT_FIX_2026-07-16.md` + GLOBAL_HANDOFF same date.
- **[AI: Any]** daily D3 check: `/api/status` ARMED + fresh reconcile + `[]`/`[]` + P2RT pinned
  `74e0990b` clean. Benign ~10-min feed cycles + `RECONCILE_FAILED_TOLERATED` WARNs = expected.
  **Jul-18 planned PC-off = window boundary (v5 resets), NOT an incident.** Definitive ≥10-day
  D3 on the VPS (end of month).
- **[AI: Codex]** NEXT: PR #22 edit round —
  `11_TRIAGE/CODEX_PR22_REQUIRED_EDITS_PROMPT_2026-07-16.md` (10 required edits + A2
  claim-narrowing + adversarial tests proven failing on `f72b377a`); STOP for Fable re-review.
- **[AI: Claude]** re-review the edit round on real code; then the single formal run-approval
  question to Barış.
- **[AI: Barış]** merge decisions: PR #23 (deployed fix), PRs #20/#21 (docs-only) — any time.

## ~~🔴 P2 DISARMED — Day 0 v4 died 2026-07-15T20:22:44Z~~ RESOLVED by Day 0 v5 above

Day 0 v4 lived 8h20m; reconcile N=3 tolerance WORKED; killer was `data_restore_timeout_s=60s`.
Barış approved 60→300s 2026-07-16 → Codex Task A (Gate-5, BLOCK, Fable-verified) + Task B
(timeout fix) both delivered 2026-07-16; deploy = Day 0 v5 (section above).

## 🔴 FAZ3B PR #22 — independent Gate-5 = BLOCK (Fable-verified 2026-07-16); 10 REQUIRED EDITS queued

Codex Gate-5 (`11_TRIAGE/CODEX_GATE5_FINDINGS_PR22_2026-07-16.md`) found 4 FATAL areas; Fable
confirmed ALL on real code (`11_TRIAGE/FABLE_AUDIT_CODEX_GATE5_PR22_2026-07-16.md`): A4 primary
DSR non-executable (engine NaN at grid_n=1, no du_cell tool exists), A5 gauntlet geometry
mutable/unasserted, A6 runner argv+manifest+commit+post-run guard bypasses, A9 pre-reg §8↔§10
decision-table contradictions. 108/108 tests reproduce; engine byte-identity holds; virginity
scan clean (local corpus). **No run, no approval question, D016 unspent** until:
- **[AI: Codex]** execute `11_TRIAGE/CODEX_PR22_REQUIRED_EDITS_PROMPT_2026-07-16.md` (after
  Task B): 10 edits + A2 claim-narrowing + adversarial tests proven failing on `f72b377a`.
- **[AI: Claude]** independent re-review of the edit round on real code; then present the
  run-approval question to Barış.

## ✅ P2 DAY 0 v4 ARMED 2026-07-15T12:02:42.856537Z + ALL PRs MERGED (Fable audit PASS)

Outage-tolerance fix deployed (P2RT detached `1465f8f0`, 130 tests); one ARM; zero
FAILED/TOLERATED/STALE since; flat. **Master consolidated `8721bce0`: PR #16/#17/#18/#19 all
MERGED** (Fable finished #19 registry + handoff union after Codex correctly stopped; e0651f94
Day-0-v4 report folded in; bridge suite 130 on master). Full record: GLOBAL_HANDOFF
`[Claude Fable 5] 2026-07-15 — DEPLOY (Day 0 v4) + PR MERGE AUDIT`.
- **[AI: Any]** daily D3 check unchanged; **Day 0 v4 resets at the Jul 18 planned PC-off — that
  is a window boundary, NOT a safety incident.** Definitive ≥10-day D3 runs on the VPS (end of
  month). Benign feed noise now suppressed from Telegram; `RECONCILE_FAILED_TOLERATED` (WARN, no
  disarm) during a real outage = correct new behavior, not a failure.
- **[AI: Any, low priority]** tidy master `NEXT_STEPS.md` union artifacts (superseded FAZ3B/bridge
  sections) next session; remove merged worktrees C:/BTOL, C:/FZ3G5.

## CRYPTO PAPER BRIDGE P2 — TIMEOUT FIX BUILT; FABLE AUDIT/DEPLOY LOCKED 2026-07-16 [AI: Claude]

Approved 60-to-300-second data-restore timeout wiring is built in commit `79976577` on
`feature/ibkr-bridge-final`. Final focused tests failed on pre-fix code (`1 failed, 2 passed`), then
passed after the fix (`3 passed`); both full suites pass `132 passed, 1 warning` from both
supported CWDs. `bars.py` is unchanged. Report:
`11_TRIAGE/P2_DATA_RESTORE_TIMEOUT_REPORT_2026-07-16.md`.

- **[AI: Claude]** independently audit real code at `79976577`, rerun both full suites, and
  reproduce the focused failure against pre-fix code. Do not trust the Codex report.
- **[AI: Claude|Codex]** only after Fable records PASS, execute the existing single testnet
  deploy window: detach `C:\P2RT` to the audited tip, rerun both suites, supervisor start,
  at least 10-minute gate including verified fresh bars, then exactly one authorized ARM.
- **[AI: Any]** until audit PASS, keep the runtime DISARMED and leave clean detached
  `C:\P2RT` at `1465f8f0`. Mainnet remains forbidden.

## SUPERSEDED — CRYPTO PAPER BRIDGE P2 ARMED, NEW DAY 0 2026-07-15T06:48:16.619336Z

Fable-audited race fix `da44d1ff` is deployed in detached `C:\P2RT` at `cc4ce67d`. Run
`paper-20260715063657` passed the required 10-minute reconnect gate and two post-ARM reconciles.
Exactly one ARM request/transition occurred; final state was ARMED and reconcile-ready with
positions/orders `[]` and zero ERROR/reconcile-failure/defer events.

- **[AI: Any]** daily read-only D3 check: state/reconcile freshness, WARN/ERROR events, equity,
  process/commit identity, all positions/orders, and native stops for any owned position.
- **[AI: Claude|Codex]** on any safety anomaly: preserve evidence, DISARM safely if necessary,
  diagnose, and do not repeat ARM without a fresh complete gate.
- **[AI: Barış]** keep the host/supervisor available for at least 10 uninterrupted calendar days;
  any shutdown or critical runtime change resets the P2 clock.
- Evidence: `IBKR_PAPER_BRIDGE/docs/03_STATUS.md` and
  `MTC_COMMAND_CENTER/11_TRIAGE/P2_RACE_FIX_REPORT_2026-07-14.md`.

## SUPERSEDED — P2 RACE FIX BUILT; AUDIT/DEPLOY LOCKED 2026-07-14

Commit `da44d1ff` on `feature/ibkr-bridge-final` implements the atomic reconnect client swap,
narrow rebuild-only reconcile deferral, and deterministic regressions. Both full suites passed
`127 passed, 1 warning`; report: `11_TRIAGE/P2_RACE_FIX_REPORT_2026-07-14.md`.

- **[AI: Claude]** Fable adversarial audit on the real commit and independent suite rerun.
- **[AI: Barış]** only after Fable PASS, explicitly approve or reject Task 4's single deploy/re-arm
  window. No approval is inferred from the build request.
- **[AI: Claude|Codex]** after both gates, execute Task 4 exactly once with its stop conditions;
  otherwise leave `C:\P2RT` and the DISARMED runtime untouched.

## SUPERSEDED — P2 ARMED, D3 STARTED 2026-07-13

Day 0 started `2026-07-13T13:00:28.6218649Z` after incident containment, commit `59c334c0`, full
tests `119 passed` from both roots, and a real
`DISCONNECT -> RECONNECT -> DATA_RESTORED -> two reconciles` gate. Runtime is pinned at `C:\P2RT`;
## BRANCH CONSOLIDATION — FABLE AUDIT DONE 2026-07-13: content PASS + 1 MAJOR finding

Codex's queue 2a–2c + Telegram test-isolation work **VERIFIED PASS** on real code/runs (Fable,
2026-07-13): golden ancestor confirmed, 122/122 both CWDs independently re-run at `960369b9`,
secret greps 0, no push (branches absent on origin), bridge-vs-master conflict probe clean.
Full audit record: GLOBAL_HANDOFF `[Claude Fable 5] 2026-07-13 — CONSOLIDATION AUDIT`.
- ~~P2RT git identity repair~~ **DONE 2026-07-13 (Barış approved, Fable executed):**
  `git -C C:/P2RT checkout --detach 54278b66` — pre/post diffs empty, zero file writes, bridge
  stayed ARMED. P2RT `git log` truthful again; branch freed. Daily pinned-identity check can use
  `git -C C:/P2RT log --oneline -1` (= `54278b66` detached) + `diff 54278b66 --stat` empty.
- ~~push/open four PRs~~ **DONE 2026-07-13 (Barış approved):** PR #16 bridge → #17 UI →
  #18 faz3b-prereg → #19 donchian, merge in that order; secret scans zero; recommended
  union-resolution for `GLOBAL_HANDOFF.md`/`NEXT_STEPS.md` conflicts noted in PR bodies.
- **[AI: Barış]** merge PRs #16→#17→#18→#19 in order on GitHub (union-resolve shared handoff
  files in #17..#19). P2RT sync to the consolidated tip stays a planned restart-window decision.
- ~~queue 3: Gate-5 adversarial review~~ **DONE 2026-07-13**: Codex verdict FATAL (`1859910c`),
  Fable re-verified decisive claims on raw artifacts/code — CONFIRMED. Prereg marked BLOCKED
  (`f32a354c`); PR #18 updated. See FAZ 3B section below for the D016 decision now owed by Barış.

## CRYPTO PAPER BRIDGE P2 — 🔴 DISARMED 2026-07-15T08:40:06Z (real HL outage; Day 0 v3 dead after 1h52m); POLICY DECISION PENDING

Second real Hyperliquid testnet outage in ~26h (`ServerError` on reconnect ×5 AND on the
reconcile REST call) → fail-closed disarm. **Race fix HELD (zero DEFERRED, zero
NotConfigured) — not a code defect.** Both safety triggers (reconcile single-strike +
DATA_STALE after ~80s) fire on any ~2-min exchange outage → **P2 ≥10 days unreachable
without an outage-tolerance policy change.** Zero exposure; equity intact; reconcile
recovered 08:42:07Z. ⚠️ No `DATA_RESTORED` seen after recovery yet — verify fresh bars
before any ARM.
- ~~policy decision~~ **DONE 2026-07-15: Barış approved option (a).** Codex prompt written:
  `11_TRIAGE/CODEX_P2_OUTAGE_TOLERANCE_PROMPT_2026-07-15.md` — reconcile N=3 consecutive-strike
  tolerance + ~5-min reconnect budget before DATA_STALE + notify-threshold (suppress routine
  DISCONNECT/RECONNECT-attempt1/DATA_RESTORED) + tests. Fail-closed principle preserved.
- ~~build policy fix (Tasks 1-4)~~ **DONE + Fable audit PASS 2026-07-15** (`0e644b52`, 130 tests
  both CWDs, 4 new tests proven failing on pre-fix code, trade-path safety verified). Task 5
  deploy CLEARED on Barış go; Task 6 PR merges CLEARED.
- **[AI: Barış] 🔴 P2 bridge PROCESS is DOWN** (supervisor exited ~09:57Z; DISARMED/flat/safe —
  monitoring gap only, no trading risk). Your go on the Task-5 deploy is now the clean restart
  (brings the audited fix live, Day 0 v4 validation-tier). Or say the word to relaunch the
  supervisor on old code just to restore monitoring. Runbook:
  `11_TRIAGE/CODEX_P2_OUTAGE_TOLERANCE_PROMPT_2026-07-15.md` §Task 5.
- **[AI: Codex]** on Barış go: Task 5 deploy (child already stopped → detach P2RT to audited tip
  → suites → supervisor → gate → ONE ARM → Day 0 v4) + Task 6 PR merges #16→#19.
- **[AI: Any]** do NOT re-ARM before Fable audit PASS + full gate incl. verified fresh bars.
- **PC uptime (Barış 2026-07-15):** ON now → Jul 18 Sat (~2h off) → ON → Jul 20 (~2h off am)
  → 6 days uninterrupted → pattern continues. **VPS end of month.** No pre-VPS window reaches
  ≥10 uninterrupted days — any PC ARM is policy VALIDATION; the definitive D3 clock starts on
  the VPS. Planned PC-offs are window boundaries, NOT safety incidents.

Superseded record (Day 0 v3, dead): DAY 0 v3 = 2026-07-15T06:48:16.619336Z [AI: Any]

Race incident (Day 0 v2 died 16:46:42Z Jul 13) → fix `da44d1ff` (atomic client swap +
RECONCILE_DEFERRED guard; 127 tests; new tests proven failing on pre-fix code) → Fable audit
PASS → Task-4 single restart window executed 2026-07-15: `C:\P2RT` detached at `cc4ce67d`
(race fix + conftest Telegram isolation + golden all live), run `paper-20260715063657`,
pre-ARM gate passed, ONE ARM at 06:48:16Z, zero ERROR/FAILED/DEFERRED, live proof: reconcile
succeeded INSIDE a reconnect window (06:47:26). Deploy audit: GLOBAL_HANDOFF
`[Claude Fable 5] 2026-07-15 — DEPLOY AUDIT: PASS`. PR #16 tip `8e53439e`.
- **[AI: Any]** daily read-only D3 check: state/reconcile freshness, WARN+ events (benign =
  ~10-min DISCONNECT→RECONNECT attempt=1→DATA_RESTORED; occasional single RECONCILE_DEFERRED
  during a rebuild is expected and harmless), equity, positions/orders + native stops,
  process identity, pinned check = P2RT detached `cc4ce67d` + clean status.
- **[AI: Claude|Codex]** any safety anomaly: preserve evidence, DISARM if needed, diagnose;
  no re-ARM without fresh complete gate. **D3 target: ≥10 uninterrupted days → 2026-07-25+.**

Previous window record (superseded): Day 0 RESET to `2026-07-13T15:17:05.383618Z` after the approved EMA-8 trail fix `f209acd2`
(SMA-8 → exact QuantLens EMA convention) landed in `C:\P2RT` and one clean deploy+re-ARM cycle
(run `paper-20260713150651`, tests `121 passed` from both roots, one ARM_REQUEST, post-ARM
reconnect gate passed). Fable audited 2026-07-13 against real code/runs: PASS. Earlier Day 0
(`13:00:28Z`, `59c334c0`, 119 tests) is superseded — that run auto-disarmed at `13:29:59Z` on
`DATA_STALE` (fail-closed worked). Runtime is pinned at `C:\P2RT` at `54278b66`;
Task Scheduler must never be redirected to the parallel-agent research checkout.
- **[AI: Any]** daily read-only D3 check: state/reconcile freshness, WARN/ERROR events, equity,
  process/commit, all positions/orders, and native stops for any owned position.
- **[AI: Claude|Codex]** any safety anomaly: preserve evidence, DISARM safely if needed, diagnose;
  do not repeat ARM without a fresh complete gate.
- Evidence: `IBKR_PAPER_BRIDGE/docs/19_P2_RECONNECT_INCIDENT_2026-07-13.md`.
- ~~**[AI: Codex]** test-suite Telegram leak fix~~ **DONE 2026-07-13** in `960369b9`: autouse
  conftest fixture patches `resolve_telegram_credentials` at both import sites; focused tests
  `2 passed`, both full suites `122 passed`. Runtime code untouched. `C:\P2RT` was not synced, so
  its old conftest can still emit test messages until the next planned sync window.
- Known-benign noise: Hyperliquid testnet WS expires connections ~every 10-11 min
  (`opcode=8 'Expired'` in runtime log); `DISCONNECT -> RECONNECT attempt=1 -> DATA_RESTORED`
  chains in Telegram are normal. Optional notify-threshold change (only attempt>1 / STALE)
  deferred to the VPS restart window — P2 config frozen.
- Evidence committed on `feature/ibkr-bridge-final` at `59352bb3`:
  `IBKR_PAPER_BRIDGE/docs/19_P2_RECONNECT_INCIDENT_2026-07-13.md`.

## ✅ DONCHIAN CRYPTO LADDER DONE 2026-07-13 (Claude Fable 5) — NULL
GEN_DONCHIAN_BREAKOUT × {BTCUSD, ETHUSD} × {1h, 4h} through the full canonical ladder
(pre-approved 2026-07-13): **0/4 PASS, 0 robust_final — 3 REJECTED + 1 INSUFFICIENT_TRADES
(ETHUSD 4h, 9 trades). Nothing promotable, nothing forward-paper; bridge export NOT READY.**
The US-equities-10m Donchian lead does NOT transfer to crypto 1h/4h. Verdict report:
`11_TRIAGE/DONCHIAN_CRYPTO_LADDER_VERDICT_2026-07-13.md`; artifacts
`03_QUANTLENS/research/donchian_crypto_ladder_2026-07-13/`; registries updated (validator PASS).
- **[AI: Barış]** optional: if crypto Donchian is ever revisited, it needs a NEW pre-registered
  design (longer-history crypto source + multi-symbol family + Faz-3b swept exits) — re-running
  this grid is deterministic and yields identical nulls (A19).

## 🚀 CRYPTO PAPER BRIDGE — Hyperliquid (was "IBKR"; broker PIVOTED 2026-07-06, design FINAL on `feature/ibkr-bridge-final` 52b13f6f; read `IBKR_PAPER_BRIDGE/docs/` 00→01→05→02→07 before touching. IBKR closed (KKTC), Signum rejected (no native stop) — see 07_BROKER_DECISION)
- ~~run external design audits~~ DONE 2026-07-06: 7 reports in `IBKR_PAPER_BRIDGE/docs/audits/`.
- ~~triage audit reports, adopt accepted findings~~ **DONE 2026-07-06** (Claude Fable 5): 21 adopted clusters amended in place; record + rejections in `IBKR_PAPER_BRIDGE/docs/05_AUDIT_RESOLUTION.md`. Build plan now honestly **2 days** (Day 1 mock core, Day 2 IBKR hardening).
- **[AI: Barış]** review corrected `IBKR_PAPER_BRIDGE/docs/03_STATUS.md` and commits `d431dfab..0f6e241d`; decide whether to merge/continue `feature/ibkr-bridge-final`.
- ~~**[AI: Barış]** prep Hyperliquid **testnet** API wallet per `06_HYPERLIQUID_SETUP.md`.~~ DONE 2026-07-12: dedicated `MTC-bridge-test` agent authorized; Windows user credential formats validated without disclosure.
- ~~**[AI: Claude|Codex]** BUILD DAY: execute `IBKR_PAPER_BRIDGE/docs/02_BUILD_PLAN_1DAY.md` tasks 1-11 in order, commit per task, mock-first.~~ DONE 2026-07-07 (Codex GPT-5): 13 task commits through Task 11; tests pass; dry-run demo verified; P0 smoke written but not run.
- ~~**[AI: Codex]** corrective scaffold-to-P1 pass from `docs/09_CODEX_FIX_PROMPT.md`.~~ DONE 2026-07-07: Broker protocol decoupling, strategy stops/live positions, resting order lifecycle, persisted duplicate guard, persisted KILL, Hyperliquid native trigger fake-SDK tests, dashboard real rows/status/bars/screenshots, and lifecycle tests. Full suite 37 passed. Caveat: chart screenshot uses local SVG fallback; actual Lightweight Charts visible rendering remains a focused follow-up.
- **[AI: Codex|Claude]** focused dashboard chart follow-up: make the visible Trading chart use a reliable bundled/local Lightweight Charts path or formally accept the SVG fallback for P1 mock demo; verify with screenshots.
- ~~**[AI: Codex]** support Hyperliquid Unified account balances, preserve string-shaped exchange errors, and cleanly disconnect the smoke websocket.~~ DONE 2026-07-12 in `944a5323`; both full suites `70 passed`.
- **[AI: Barış]** do not transfer funds or change account mode; `unifiedAccount` correctly shares the 999 mock USDC balance across Spot/Perps.
- ~~**[AI: Codex]** add conservative Hyperliquid price rounding and run exactly one approved P0 attempt.~~ DONE 2026-07-12 in `42018032`; local suites `72 passed`, attempt failed cleanly on real `positionTpsl` response cardinality, zero open orders/positions.
- ~~**[AI: Codex]** locally harden `positionTpsl` response-shape handling, redacted diagnostics, and deterministic owned-cloid cleanup.~~ DONE 2026-07-12 in `09a7a92f`; both full suites `89 passed`.
- ~~**[AI: Codex]** implement E1 user-registry fallback and run one re-approved P0 smoke.~~ DONE 2026-07-12 in `25cee696`; source=`user_registry`, both suites `92 passed`, attempt 5 reached testnet and exposed the native trigger-type rejection.
- ~~**[AI: Codex]** implement G1 normalTpsl entry grouping and the bounded G2 fallback, then run attempt 6.~~ DONE 2026-07-12 in `a4de4a6e`; both suites `98 passed`, normalTpsl returned a resting entry plus `waitingForFill` child state, and C3 cleanup passed.
- **[AI: Any] 🔴 ACTIVE — GO-LIVE PLAN: `IBKR_PAPER_BRIDGE/docs/16_GO_LIVE_PLAN.md` is the single
  authoritative task ladder from here to P2 (testnet live loop).** Barış 2026-07-12 blanket-approved
  ALL of it incl. bounded P0 smokes until pass, B6 fill smoke, and ALL of Phase D (P2 ARM). Any model
  picks the first unchecked box in its §3 and executes per its §1 rules WITHOUT asking; human input
  only at its §0-İ points (Telegram creds, PC uptime, mainnet=forbidden; QuantLens registration İ4
  is now complete).
  P1 audited PASS; P0 attempt 6 proved the wire format (resting entry + `waitingForFill` child); W1
  (pending-child parser) is the current first task.
- ~~**[AI: Barış]** approve QuantLens İ4 registration and unblock the real golden.~~ **DONE
  2026-07-13**: `keltner_trail_ema8` is registered and the real golden is ready; 858/858 entry
  signals match. Evidence: `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md`. Honest caveat: the
  bridge exit trail is SMA-8 while QuantLens `trail_ema8` is EMA-8, so exit parity is not claimed.
- **[AI: Claude|Codex]** P3 later (≥30d): produce the slippage + operational signal-parity report
  to `11_TRIAGE/`; the QuantLens/golden prerequisite is complete.

## 🔧 MCC APP AUDIT FOLLOW-UPS (audit 2026-07-05: `11_TRIAGE/MCC_APP_AUDIT_2026-07-05.md`; Barış answered all open questions; quick wins DONE same session on `feature/mcc-audit-fixes`)
- ~~fix backtest_reader nested-run glob + heartbeat_reader parents index~~ DONE 2026-07-05 (115 tests pass; July runs + heartbeat visible).
- ~~register faz3b_stage1 in RESEARCH_RUN_REGISTRY~~ DONE 2026-07-05.
- ~~refresh REPORT_MANIFEST + CURRENT_STATUS; retire SESSION_LOG~~ DONE 2026-07-05.
- ~~parity artifacts migrated to `12_PARITY_PINETS/`~~ DONE 2026-07-05 (byte-identical parity status; paths.local.json updated locally — git-ignored, other machines must update their own).
- ~~scoring pass `mcc_night_tail.sh` over July stage dirs~~ **DONE 2026-07-05** (Barış approved): 716 new scorecard_v2 cards (turtle_sweep 36, stageA_v2_multiasset 302, variants 182, archetypes 196), **promotable=0 across all 716** (consistent with known nulls). Dashboard verified: scorecards 837→1553, all 4 runs listed. Gotchas: `mcc_night_tail.sh` needs `MEGA_BUNDLE_MANIFEST` set (else CPCV = all N_A "No dataset found") + Windows-style `C:/` RUN_DIR + `PYTHONUTF8=1` (run_python_clean exec wrapper decodes as cp1254 otherwise). Tail's own "dashboard visible" check greps stage-name run_id → false NO now that reader names runs `<run>/<stage>` — cosmetic [AI: DeepSeek].
- ~~fix 39 VARIANT_LOG_REGISTRY.json validator errors~~ **DONE 2026-07-05**: added `research_run_id` to all 19 variants (derived from real `impl`+`created_utc`: archetypes→overnight_archetypes_2026-07-03, turtle→turtle_heavy_2026-07-01, missing-knobs→overnight_full_2026-07-02), registered those 3 runs in RESEARCH_RUN_REGISTRY, removed schema-invalid top-level `note` (content lives in overnight NEXT_STEPS sections). Validator now PASS.
- ~~build CURRENT_STATUS auto-derive tool~~ **DONE 2026-07-05**: `03_QUANTLENS/tools/derive_current_status.py` (dry-run default; `--apply` writes; `--check` exits 1 on drift). Derives phase from newest GLOBAL_HANDOFF `## ` topic + summary from its first paragraph + next_recommended_action from first open NEXT_STEPS bullet. Safety fields (mode=read_only, live_trading=false) hardcoded. Hand-refresh dies.
- ~~Home + tail visibility + header pills cleanup~~ **DONE 2026-07-05**: Home "Data as of" freshness line (already shipped); `mcc_night_tail.sh` dashboard-visible check now resolves MCC root by name-walk + matches `<run>/<stage>` run_id (was false NO); removed hardcoded "Local Engine: Idle"/"Token Mode" header pills → single "Read-only" pill.
- **[AI: Claude, optional]** Strategy Intelligence per-section "as of" chips (Home done; SI still could show evidence date per gate/verdict section).
- ~~System Test / Fake Money Lab page~~ **DONE 2026-07-05** (Barış approved design+impl): new read-only nav page `system_test_reader.py` + renderSystemTest; scans `03_QUANTLENS/system_test/*/`, shows plumbing counts only (888/888/888/≈444, 0 unexplained), sticky amber firewall banner, V1.1-V5 gate ladder. Renamed 'Paper Trading'->'Promotion Readiness' to kill the naming collision. Design: `11_TRIAGE/SYSTEM_TEST_LAB_PAGE_DESIGN_2026-07-05.md`. 120 API tests, live render verified.
- **[AI: Barış]** run-manifest discovery contract (audit §6.1) — decide if wanted before next big orchestrated sweep.


## FAZ 3B — SWEPT EXIT_MODE (D016 Path A scope freeze approved; passive accrual only)
## 🔶 FAZ 3B — SWEPT EXIT_MODE (Stage-2 prereg BLOCKED by Gate-5 FATAL 2026-07-13 — D016 decision now = path choice)
Scope: `00_AGENT_PROTOCOLS/FAZ3B_EXIT_SWEEP_SCOPE.md`. Chain D013→D014→D015 done: engine landed,
self-parity byte-identical (goldens never recaptured), Stage-1 discovery run COMPLETE 2026-07-05
(`03_QUANTLENS/research/faz3b_stage1_20260705/STAGE1_REPORT.md`): H1 confirmed at 1h — clean cell
GEN_KELTNER_BREAKOUT × AAPL × 1h × trail_ema8 STRONG_PASS union-DSR 0.581; H0 holds at 10m;
honest confound: first-ever 1h fixed_2R baseline itself robust on KELTNER SPY/QQQ. PR #15 merged.
- ~~Original Stage-2 draft + Gate-5~~ **CLOSED/BLOCKED 2026-07-13**: Codex FATAL findings
  `11_TRIAGE/CODEX_GATE5_FINDINGS_FAZ3B_STAGE2_2026-07-13.md` were independently confirmed by
  Fable; all six proposed held-out symbols were historically contaminated, the 12-grid was
  re-optimization, and existing gauntlet tools were exit-blind. The old draft can never run.
- ~~**[AI: Barış] choose Path A/B**~~ **DONE — D016 PATH A APPROVED 2026-07-13**. New temporal
  holdout frozen in `00_AGENT_PROTOCOLS/FAZ3B_STAGE2_FORWARD_CONFIRM_PREREG_2026-07-13.md`:
  scored 1h sessions 2026-07-14 through 2028-07-13; SPY/IWM, XLF/XLE, XLV/XLP across three
  diversity groups; primary `{50,10,2.0}` only plus four diagnostic star points. Earliest possible
  evaluation 2028-07-14. Today: zero compute and no data ingestion.
- **[AI: Codex, needs separate Barış approval]** build exit-aware CPCV/multi-window/PBO tooling
  exactly to the new prereg section 8 contract; default fixed-2R self-parity must stay byte-identical.
- **[AI: Any]** before any future-data unblinding, complete the artifact-level historical Keltner
  trial ledger. Registry-only checks are forbidden; scan result JSONs in both backtest-result roots.
- **[AI: Barış]** after the fixed window closes: separately approve non-performance data inventory,
  then Gate-5, then exactly one smoke/full evaluation. D016 itself authorizes none of these.
- ~~draft Stage-2 pre-reg~~ DONE 2026-07-13, then ~~Gate-5 adversarial review~~ **DONE 2026-07-13
  — VERDICT FATAL, Fable-verified on raw artifacts/code (findings `1859910c`, banner `f32a354c`,
  PR #18):** (1) all 6 "held-out" symbols already swept — June-29 overnight covered ALL 51 bundle
  symbols at Keltner 1h → NO untouched 1h symbol exists in the canonical bundle; registry proved
  NOT to be an evidence inventory; (2) CPCV/multiwindow tools are exit-blind (simulate_slice
  defaults fixed_2R) and PBO lacks a per-config matrix → §6 gauntlet unexecutable as written;
  (3) 12-set grid = 75% of discovery grid = re-optimization. Current draft can NEVER get D016.
- **[AI: Barış] 🔴 D016 DECISION = choose path:** **(a) RECOMMENDED — deferred forward
  confirmation:** freeze a pre-registered forward window now (bars after 2026-06-26, evaluate
  e.g. after 2026-12-31, pre-named symbols + ≥2 diversity groups); zero compute today, truly
  virgin data. **(b) close Faz3b as INCONCLUSIVE** (Stage-1 AAPL stays research-only, family
  gets no confirmation attempt). Either way requires NEW prereg + fresh Gate-5 before any run.
- **[AI: Codex, needs Barış approval — prerequisite for path (a) and any future exit-mode
  confirmation]** exit-aware gauntlet tooling task: `cpcv_validator.py` + `multiwindow_oos.py`
  must pass `row.exit_mode` into `simulate_slice` and stamp it in outputs; PBO needs a
  per-config×period return-matrix contract (Gate-5 findings §F/§G/§J + REQUIRED EDITS 9-11 are
  the spec). Own code review + self-parity discipline; separate approval.
- **[AI: Any]** register `overnight_multiasset_2026-06-29` in RESEARCH_RUN_REGISTRY; add the
  "virginity check = scan 05_BACKTEST_RESULTS + research JSONs, never registry-only" rule to
  prereg templates.
- **[AI: Barış]** 2026-08-01: Gate V5 day-30 review of the SYSTEM_TEST vertical-slice track (CLOSED at
  V1.1; legs V2-V4 deliberately unopened).

## SYSTEM_TEST_ONLY VERTICAL SLICE - Gate V0 planning approved 2026-07-02

Baris approved Gate V0 planning and selected `STG002 / QL_ALPHA_LINK_8EMA_1H`
as the benchmark. This is a fake-money systems-plumbing benchmark only:
SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY.

**Next:**
- ~~**[AI: Codex|Claude]** write a draft implementation plan only for the local
  core slice: signal emitter, localhost receiver, reconciliation reporter, and
  induced-failure drills. No code yet.~~ DONE 2026-07-02:
  `00_AGENT_PROTOCOLS/SYSTEM_TEST_VERTICAL_SLICE_IMPLEMENTATION_PLAN.md`.
- ~~**[AI: Codex|Claude]** prepare a narrow Fable audit prompt for that
  implementation plan before any code is approved.~~ DONE 2026-07-02:
  `11_TRIAGE/FABLE_AUDIT_PROMPT_SYSTEM_TEST_VERTICAL_SLICE_PLAN_2026-07-02.md`.
- ~~**[AI: Baris]** send the Fable audit prompt to Fable and bring back the
  report before implementation approval.~~ DONE 2026-07-02: Fable verdict was
  `SAFE ONLY AFTER PLAN FIXES`; Codex applied the plan-text fixes.
- ~~**[AI: Baris]** approve or reject the implementation plan.~~ DONE
  2026-07-02: Baris approved implementation with the exact SYSTEM_TEST_ONLY
  sentence. Codex implemented V1 local modules/tests only. No replay run,
  schema files, backtests, servers, broker/exchange/testnet, TradingView,
  WunderTrading, Pine, parity, `MTC_V2`, `02_MTC_BACKTEST`, or `07_ADAPTERS`
  work was performed.
- ~~**[AI: Baris|Codex]** before the first local replay run, resolve the output
  root guard.~~ DONE 2026-07-02: Baris approved the pre-run readiness patch.
  `.gitignore` now ignores `MTC_COMMAND_CENTER/03_QUANTLENS/system_test/`,
  `git check-ignore` confirms `_probe` is ignored, and
  `run_local_replay(...)` exists as a tested importable entry function. No real
  STG002 replay run was performed.
- ~~**[AI: Baris|Codex]** approve/run the separate Step 9.1 replay-run
  sentence.~~ DONE 2026-07-02: Baris approved exactly one local
  SYSTEM_TEST_ONLY replay. Codex ran it through `run_local_replay(...)` into
  `03_QUANTLENS/system_test/stg002_system_test_replay_20260702T171958Z/`.
  Result: `status=OK`, `EXPECTED=888`, `ENTRY=444`, `EXIT=444`,
  `RECEIVED accepted=888`, `duplicates=0`, `rejected=0`,
  `simulated_fills=888`, `round_trips=444`, `unexplained=0`.
- ~~**[AI: Baris|Codex]** review the completed local run artifacts and decide
  whether to send a narrow read-only Fable audit prompt for the result.~~ DONE
  2026-07-02/04: Fable audited run + implementation (PASS), drafted the V1.1
  LOW-fix dispatch; executor implemented (7-file allowlist); Fable audited the
  diff and committed. Focused pytest **43 passed**. **Slice V1.1 CLOSED** —
  clean pause point reached. Remaining slice work only via new gates:
  V2 (TV alerts) / V3 (Wunder demo) / V4 (testnet), each Baris-approval-gated
  and deliberately NOT opened (no robust strategy exists to justify them);
  Gate V5 day-30 review due **2026-08-01**.
- **[AI: Baris]** separate explicit approval is required before any server,
  CLI, dashboard execution UI, engine-forward signal generation, schema file,
  broker, exchange, testnet, TradingView, WunderTrading, Pine, parity,
  `MTC_V2`, paper trading, or live trading path.
- **[AI: Baris|Codex] Optional separate approval:** decide whether to add a
  SUPERSEDED banner to stale STG002 `PROMOTE_TO_*` / forward-paper docs. This
  is not part of the vertical slice implementation plan.

## 🔷 STRATEGY PARAM-SPEC REGISTRY — Faz 1-4 DONE 2026-07-01 (Claude Opus 4.8) → PR #15 open
Branch `feature/strategy-param-specs`, pushed, **PR [#15](https://github.com/bsemaay-tech/mtc-command-center/pull/15) open (NOT merged)**. Faz 1: declarative per-strategy param spec (generator code=truth + overlay → `05_REGISTRY/STRATEGY_PARAM_SPECS.json`, 20 strat, 1122 combos, 1,201,662 cases) surfaced in Strategy Detail §4. Faz 2: honest MTC_V2/Pine parity readiness (no 1:1 Pine impl for the 20 generics → `deferred_until_promotion` + `parity_contract` that a Pine port must replicate the global exec model; 2 review-Pine refs marked needs_reconciliation). Faz 3: first missing-knob variant `GEN_DONCHIAN_TURTLE` (Turtle structural stop) via monkey-patch `03_QUANTLENS/tools/variant_missing_knobs.py` (engine untouched), origin=variant/UNVALIDATED, in VARIANT_LOG, smoke OK. Faz 4: runbook §3.5 canonical case-count definition. API 112 passed, renders verified.
**Next:**
- **[AI: Barış]** review + merge PR #15.
- **[AI: Claude, approval-gated] Faz 3b:** TRUE trailing opposite-channel EXIT + short-side need an engine-core `simulate_slice` change (dynamic stop / direction) — affects ALL strategies → explicit approval before touching the shared simulator.
- ~~validate `GEN_DONCHIAN_TURTLE`~~ **DONE 2026-07-01** (turtle_heavy overnight): 357-cell full-universe + deep CPCV/PBO. **robust_final 0**; structural stop beat base in only 40% of cells (no systematic edge). Confirmed A21 (CPCV/PBO ≠ DSR) at 51×7 scale. Report: `05_BACKTEST_RESULTS/turtle_heavy_2026-07-01/MORNING_REPORT.md`; lessons `OVERNIGHT_LESSONS_2026-07-01.md`. **Do NOT pursue Faz 3b trailing-exit** — the structural-stop result does not motivate the engine-core change.
- **[AI: Claude] extend variants:** the remaining Faz-3 missing_knobs across the 20 strategies (promote fixed knobs like TRIPLE_EMA 5/13/50, BB mult, 8EMA period; add filters) — each a NEW variant in VARIANT_LOG, not a mutation of the base strategy.

## ✅ OVERNIGHT MULTI-ASSET SWEEP DONE 2026-06-30 (Claude Opus 4.8) — nothing promotable
Largest sweep to date: 7,140 cells (51 sym × 7 TF × 20 strat) on `native_multiasset_alpaca_2026-06-28`, 20 workers, one clean ~27-min pass. PASS 184 / STRONG_PASS 172 / BH-FDR 19 / **dsr_robust 2 (tiny-sample) / robust_final 0**. Report: `05_BACKTEST_RESULTS/overnight_multiasset_2026-06-29/MORNING_REPORT.md`. Dashboard shows run COMPLETED. **No existing strategy is robust on any asset class/TF — confirmed at scale.**
**Next [AI: Barış|Claude]:** the open path is **NEW strategy logic** (the crypto-era library does not transfer; re-sweeping is deterministic and yields identical nulls). If a lead is pursued (e.g. metals/DONCHIAN-intraday showed largest raw returns), require portfolio/CPCV + a pre-registered confirmation grid — expect the same null per prior pooled-DSR test. Results dir `overnight_multiasset_2026-06-29/` (17MB JSON + checkpoint) is local research output — not committed (git-ignored bulk); regenerable.

## ✅ ONBOARDING / AI_MEMORY HARDENING DONE 2026-06-29 (Claude Opus 4.8) — PR #5–#8 merged
2-round cold-onboarding audit (6 models). Closed all consensus gaps → onboarding now uniform across all 7 job types (backtest/scoring/dashboard/verdict/memory/git/tools). Fixes: repo-identity + DATA & LAUNCH (PR #5); W3 results→dashboard map + runner/DSR/pickup doc-sync (PR #6); W4 verdict authoring procedure `03_QUANTLENS/_user_guide/13_AI_VERDICT_AUTHORING_PROCEDURE.md` (PR #7); engine soft-guard for unset MEGA_BUNDLE_MANIFEST (PR #8). Audit prompts: `11_TRIAGE/COLD_ONBOARDING_AUDIT_PROMPT_{,v2_}2026-06-29.md` [AI: Any].
**Optional follow-ups [AI: Claude|Barış]:** (1) re-run the v2 audit as a regression to confirm W3/W4 now score PASS; (2) promote v2 prompt to a permanent `_AI_MEMORY/ONBOARDING_SELFTEST.md` run after every onboarding-contract change; (3) author real QuantLens verdicts using the new procedure (212 strategies currently un-verdicted/`NEEDS_CLARIFICATION`).

## ✅ IMPECCABLE UI PILOT (2026-06-21 → 2026-07-13) — COMPLETE on `feature/mcc-ui-impeccable-fixes`
Setup DONE: product context `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MCC_PRODUCT_CONTEXT.md` + design context `MTC_COMMAND_CENTER/11_TRIAGE/STRATEGY_INTELLIGENCE_DESIGN_CONTEXT.md` (North Star "The Quiet Terminal"; preserves existing dark command-center identity) + `.claude/launch.json`. Original Strategy-Detail critique = **30/40 Good** (`.impeccable/critique/2026-06-21T15-56-19Z__r-08-dashboard-app-apps-web-app-js-strategy-detail.md`).
Polish pass **COMPLETE**; honest re-score = **32/40 Good** (not inflated to impeccable): `MTC_COMMAND_CENTER/11_TRIAGE/UI_AUDITS/IMPECCABLE_PILOT_R3/CRITIQUE_RESCORE_2026-07-13.md`. Frontend scope remained `08_DASHBOARD_APP/apps/web/{app.js,styles.css}`.
1. ~~[P1] a11y contrast~~ **DONE 2026-06-28 (DeepSeek v4 Pro + Codex + Claude audit)** — empty-state values now use `--muted #94a3b8` (~7.4:1 on all dark backgrounds, AA safe). Styled via `styles.css` only (10 selectors). Claude audit: PASS WITH NITS; no code fix required. Temporary reports removed after audit.
2. ~~[P1] a11y focus~~ **DONE 2026-06-28 (Codex GPT-5 + Claude audit PASS WITH NITS)** — global `:focus-visible` ring added, the 4 STAGE workflow cards are native `<button type="button">` controls, reduced-motion CSS disables the pulsing amber dot, and `tests/test_strategy_detail_a11y_static.py` guards the contract. Claude audit required no code fix.
3. ~~[P2] side-stripe bars~~ **DONE 2026-06-21 (Claude Opus 4.8, commit `0172d940`)** — `.gate-card .bar` was removed and replaced with full-border tint + faint background per state.
4. ~~[P2] boilerplate dedup~~ **DONE** — implementation `6da2735c`; before/after screenshot evidence committed in `adeb889b`. Full-credit notes are hidden; partial/zero notes remain.
5. ~~[P2] triple gate-state~~ **DONE** — implementation `e819ac02`; dead helper/CSS cleanup + before/after evidence committed in `93114a61`. Persistent right rail is canonical.
Verification: live `:8765/dashboard` Strategy Detail, committed screenshots under `11_TRIAGE/UI_AUDITS/IMPECCABLE_PILOT_R3/screenshots/`, `node --check` PASS, focused a11y test `2 passed`, canonical dashboard API suite `120 tests` / `OK`. No trading/Pine/MTC_V2/parity/schema/data-contract change.

## ▶ AI TOOL INTEGRATION ROADMAP (filed 2026-06-20, Claude Opus 4.8) — STATUS 2026-06-22: ALL PHASES 1–5 COMPLETE. Remaining = operator config only (n8n notify channel) + re-open DEFERs (LiteParse on scanned PDF, Claude-Video on indicator-screencast, Taste-Skill on a marketing page).
Source backlog + actionable plan + Claude critique live in `09_DOCS\AI_TOOLING\`:
- `MTC_AI_TOOLS_MASTER_INTEGRATION_BACKLOG.md` (catalog), `AI_TOOL_INTEGRATION_PLAN.md` (do this), `CLAUDE_REVIEW_OF_CODEX_BACKLOG.md` (what to drop).
Read `AI_TOOL_INTEGRATION_PLAN.md` before ANY AI-tool work. Phases (each Barış-approval-gated):
1. **Phase 1 — docs/instructions/memory** `[AI: Claude|Barış]` — DONE in part (this filing). PENDING APPROVAL: add a tool-roadmap + DeepSeek-routing pointer block to `AGENTS.md` and `_AI_MEMORY/START_HERE.md` (high-traffic contracts → don't edit without approval). Diffs first.
2. **Phase 2 — knowledge consolidation (light)** `[AI: Any]` — keep decisions in `09_DOCS\AI_TOOLING\`, research in `09_DOCS`, ops state in `_AI_MEMORY`. Do NOT build a new `00_KNOWLEDGE_BASE` tree.
3. **Phase 3 — local tools (pilot-gated, run §6 checklist FIRST)** `[AI: Claude|Barış]` — order: MarkItDown → LiteParse → CodeBurn → Graphify (Graphify downgraded to pilot). Compare MarkItDown/LiteParse to built-in pdf/docx/xlsx skills before adding a dependency.
   - DONE 2026-06-21: **MarkItDown** (0.1.6, `C:\tmp\mtc_markitdown_venv`, Py3.13) + **CodeBurn** (v0.9.12 global npm) piloted on real data → **both KEEP**. Reports `09_DOCS/AI_TOOLING/pilots/{markitdown,codeburn}_pilot.md`. CodeBurn finding: DeepSeek harness underused (Opus $563 + Codex $377 vs DeepSeek $2.44).
   - DONE 2026-06-21: **LiteParse piloted → ⏸️DEFER** (`liteparse` 2.0.0, ephemeral `C:\tmp\mtc_liteparse_venv`, Py3.13; 2.1.1 has no win/py3.13 wheel). Synthetic-PDF A/B ties MarkItDown on text PDFs; real edge (scanned-PDF OCR+spatial) untestable — 0 PDFs in repo — and needs Tesseract/LibreOffice/ImageMagick. Overlaps kept MarkItDown → not promoted. Report `09_DOCS/AI_TOOLING/pilots/liteparse_pilot.md`. Re-open when a real scanned strategy PDF lands. **→ Phase 3 now COMPLETE** (MarkItDown KEEP+promoted, CodeBurn KEEP, Graphify KEEP-on-demand, LiteParse DEFER).
   - DONE 2026-06-21: **Graphify piloted → KEEP on-demand** (`graphifyy` 0.8.44 via uv tool; local/keyless code graph; accurate `affected`/`explain`/`query`; graphs git-ignored; not auto, not whole-repo; `graphify install` skill-reg deferred). Report `09_DOCS/AI_TOOLING/pilots/graphify_pilot.md`.
   - DONE 2026-06-21 (Barış item 1): **MarkItDown promoted to permanent** — committed wrapper `03_QUANTLENS/tools/markitdown_ingest.py` (self-bootstraps git-ignored Py3.13 venv at `03_QUANTLENS/tools/.venvs/markitdown`, converts intake docs→.md; dry-run default). `.gitignore` updated; old `C:\tmp` venv removed; composes with (doesn't edit) `route_user_intake.py`. Still open: periodic `codeburn status` at session boundaries (CodeBurn stays global npm, no repo change).
4. **Phase 4 — research/UI pilots (branch-isolated)** `[AI: Claude|Barış]` — Claude-Video, Impeccable, Design-Extract, Taste-Skill on `feature/ui-*` only; no data-contract/registry/backtest change.
   - DONE: **Impeccable** (Strategy Detail polish, merged).
   - DONE 2026-06-22: **Design-Extract** (`designlang`) → KEEP on-demand inspiration only; wrapper `03_QUANTLENS/tools/design_extract.ps1`. `pilots/design-extract_pilot.md`.
   - DONE 2026-06-22: **Taste-Skill** (`leonxlnx/taste-skill`) → **DEFER/do-not-install**: its SKILL.md self-excludes dashboards/data-tables/product-UI (MTC's domain); Impeccable already owns that. Evaluated via `C:\tmp` clone, not installed. `pilots/taste-skill_pilot.md`. Reusable idea: its anti-default discipline + variance/motion/density dials as a checklist when running Impeccable.
   - DONE 2026-06-22: **Claude-Video** (`bradautomates/claude-video`) → **DEFER/do-not-install**. Piloted on a real Barış-supplied strategy video (TradingLab pullback, `youtu.be/Ju-cTa_dHAk`, 9m52s) via a reproduced pipeline (yt-dlp + already-installed ffmpeg + YouTube auto-captions + Claude vision; no repo install, all in `C:\tmp`). **A/B:** transcript-only already gave the full strategy; 24-frame sample added ~zero — the video is an animated explainer / pure price-action (no platform UI, no indicator settings to recover). Frame value is **content-gated**: only an indicator-config *screencast* beats transcript. Tool itself unnecessary (pipeline reproducible with installed tools). Report `pilots/claude-video_pilot.md`.
   - DONE 2026-06-22 (Claude Opus 4.8): the two doc-only branches are now MERGED to master (merge `5bcb66c9`) + deleted (local+remote): `feature/ui-design-extract` → `pilots/design-extract_pilot.md`; `feature/audit-second-eyes` (superset, contained design-extract) → `09_DOCS/AI_TOOLING/SECOND_EYES_AUDIT_2026-06-22.md`. Only `AI_TOOL_INTEGRATION_PLAN.md` + this file conflicted; resolved `--ours` (kept master's corrected §5/Phase4). Net delta = the 2 new docs only. Stale empty `feature/handoff-note` also removed; `C:\tmp` pilot leftovers (design_extract_out, second_eyes_*) cleaned.
   - **→ Phase 4 now COMPLETE** (Impeccable + Design-Extract = KEEP on-demand; Taste-Skill + Claude-Video = DEFER). Next AI-tool work = Phase 5 (n8n watchdog), which is BLOCKED until a stable backtest progress/log emitter exists.
5. **Phase 5 — side-service automation** `[AI: Barış|Claude]` — n8n watchdog for long backtests; needs a stable progress/log emitter first.
   - DONE 2026-06-22 (Claude Opus 4.8) — **stable emitter prerequisite SHIPPED** (branch `feature/run-progress-emitter`, TDD). Design: `09_DOCS/AI_TOOLING/RUN_PROGRESS_EMITTER_DESIGN_2026-06-22.md`. Canonical contract `mtc.run_progress/v1` + `mtc.run_status/v1` under `03_QUANTLENS/tools/overnight_runs/progress/<run_id>/` (heartbeat.json · events.jsonl · status.json · `_latest.json`; git-ignored). Parts: `progress_emitter.py` (lib+CLI, atomic writes, env-gated `MTC_RUN_EMITTER` → NullEmitter off so opted-out runs byte-identical), `run_emitter_supervisor.py` (liveness tick + guaranteed terminal status even on crash + `republish_native_status` adapter that reads the sweep runner's EXISTING `run_status.json` → **engine NOT edited, parity-safe**), and `heartbeat_reader.py` upgraded to strict v1 with two-timestamp **dead/stalled/running** derivation + legacy `_heartbeat*.json` fallback. Tests: tools 15 passed, API suite 86 passed (no regression); CLI smoke proved ok + crash paths.
   - DONE 2026-06-22 (Claude Opus 4.8) — **Phase 5 proper SHIPPED → Phase 5 COMPLETE.** `run_watchdog.py` (TDD): one-shot poll of `progress/_latest.json` → derives running/stalled/dead/done/failed (shared `derive_run_state` in `progress_emitter.py`), fires ONE notification per (run_id,state) alert transition (de-dupe via `_watchdog_state.json`), local log always + opt-in `--webhook-url` (no outward send without a URL). n8n workflow `03_QUANTLENS/tools/n8n/mtc_backtest_watchdog.workflow.json` + ops `09_DOCS/AI_TOOLING/PHASE5_WATCHDOG_OPS.md` (n8n or Windows Task Scheduler). AGENTS.md AI-TOOL-AUTO-USE gained a long-backtest→supervisor+watchdog trigger. Tools tests 22 passed; API suite 86 passed; CLI dedupe smoke verified. **Only operator action left:** wire the n8n Notify node to a real Telegram/Email/Slack channel + activate schedule.
REJECTED beyond Codex's list (see critique): **Headroom** (MITM proxy, ~5% saving), **NotebookLM-py** (unofficial API), **Webwright** (redundant with existing browser MCPs). Already-exists (don't rebuild): model routing = `_deepseek_driver`; review prompts = `04_SHARED\prompts\05_ai_workflow`. Hard rule: no install/integration without explicit Barış approval, tool by tool; no pine/MTC_V2/parity/schema/broker touch.

## ▶ DASHBOARD night-artifact contract LIVE 2026-06-15 (Claude Opus 4.8) — reader done, artifacts pending
Read-only `night_artifacts` reader + 5 schemas shipped; dashboard wired to consume run_plan/run_status/backtest_profile_result/top_results/artifact_index/leaderboard_delta/benchmark_update_candidate. **No such artifacts exist yet** → official profile buckets correctly empty, legacy scorecard rows quarantined.
Next when ready:
1. DONE 2026-06-15 (run_plan part + audit patch): `build_run_plan.py` generates draft review-only `run_plan.json`+`artifact_index.json`+`run_plan.md`; reader discovers usable; Planner/Advanced Artifacts/SI §4/Result Explorer artifact panel populated. Audit follow-up applied: no silent BTCUSDT default (universe `needs_freeze` when unresolved), schema enforces read-only/no-execution safety fields, SI §4 wired to run plan. STILL NEEDED: real `backtest_profile_result.json` + `top_results.json` for a validated strategy/profile to populate official buckets + KPIs (writer outside read-only app). No fakes. Also: freeze the US_EQUITIES symbol universe (`--symbols`) before any approval.
2. Implement interactive Result Explorer filters (currently placeholder; enable when profile rows real).
3. Snapshot warm-up prefetch at server start to kill ~12s cold load.
4. No promotion / no KPI fabrication; absent metrics stay `—`.
5. DONE 2026-06-15: Home metric aggregation fix — strategy-level counts deduped by base id (no count > Total), Evidence/System row counts split out + labelled; SI Gate1 section shows best Gate 1 passing version + All Versions. Report: `11_TRIAGE/HOME_METRIC_AGGREGATION_PATCH_REPORT_2026-06-15.md`.
6. DONE 2026-06-15 (RESOLVED open decision): Home canonical universe — `Total Strategies` = pipeline rows (registry fallback), Total back to **176**; scorecard-only ids shown as "Scorecard-only Strategy IDs" orphan metric (36). Gate metrics canonical-only. Report: `11_TRIAGE/HOME_CANONICAL_UNIVERSE_PATCH_REPORT_2026-06-15.md`.
7. DONE 2026-06-15: Hardening — invariant test `tests/test_home_metric_invariants.py` (no strategy count > Total; orphan exclusion; registry fallback); "Needs Attention"→"Needs Review" rename + tooltip (broad heuristic, not strict blockers); audit prompt `11_TRIAGE/NEXT_CODEX_AUDIT_PROMPT_HOME_CANONICAL_UNIVERSE_2026-06-15.md`. PENDING USER: run that Codex audit. FUTURE: orphan-id drill-down + promotion path; real action-queue/blocker model to make Needs Review precise; jsdom JS test harness to retire Python mirror.
8. DONE 2026-06-16: First profile-separated result artifact pilot (Option A). Read-only converter `03_QUANTLENS/tools/build_profile_result_artifact.py` turned real soak `MEGA_results_iter_1_*` into schema-valid `backtest_profile_result.json` (pilot dir, 4 SOURCE_NAKED rows, RESEARCH_ONLY, universe_mismatch recorded). Reader shows profile_result_rows=4. Report: `11_TRIAGE/FIRST_PROFILE_RESULT_ARTIFACT_PILOT_REPORT_2026-06-15.md`.
9. DONE 2026-06-16: Research-only UI hardening — badges (RESEARCH ONLY/UNIVERSE MISMATCH/NON-ROBUST/PROFILE MAPPING INTERPRETED) across Result Explorer/SI §5/Leaderboard/Advanced Artifacts; reader forwards provenance+profile_mapping. Report: `11_TRIAGE/PROFILE_RESULT_RESEARCH_ONLY_UI_HARDENING_REPORT_2026-06-15.md`. Resolves item (a) above.
10. DONE 2026-06-16: OPS BLOCKER resolved — `run_dashboard_server.ps1` now single-instance. Root cause (from server log): supervisor restarted `pythonw serve` every 5s; when port 8765 already bound each new process failed bind + exited same-second (endless churn), and multiple unguarded launcher copies raced → pile-up. Fix: launcher checks port 8765 + `/healthz mode=read_only` and logs `skip launch` (exit 0) if already running; supervised loop re-checks port each iteration and exits instead of churning; flags `-StatusOnly`/`-ForceRestart`/`-KillStaleMccOnly`; strict kill filter (python/pythonw + cmdline mcc_readonly + serve only — never unrelated python; default mode kills nothing); bounded `dashboard_launcher.log` + 256KB truncation on `dashboard_server.log`. Verified: 2 launches → both skip, proc count stays **1**; `POST`→405; `/healthz`+`/api/snapshot?refresh=1`=200; **69 API tests OK**; `node --check` PASS. NOTE: no auto-start trigger exists (launcher comment names a non-existent task; no Run key/Startup/VBS). If logon auto-start wanted, register ONE guarded scheduled task calling the launcher (self-skips) — left as manual user action. Report: `11_TRIAGE/DASHBOARD_LAUNCHER_SINGLE_INSTANCE_PATCH_REPORT_2026-06-15.md`.
11. BLOCKED 2026-06-28: (b) native US-equities-10m soak cannot be generated from current repo data. DeepSeek audit + Codex verification found no US equities provider, no US equities 10m OHLCV on disk, no frozen symbol universe, and only crypto proxy/research-only result evidence. Status: **DATA PROVIDER / SYMBOL UNIVERSE REQUIRED**. Codex assessment: `11_TRIAGE/NATIVE_US_EQUITIES_10M_CODEX_ASSESSMENT_2026-06-28.md`; worker report: `11_TRIAGE/_tmp_native_us_equities_10m_audit_2026-06-28/WORKER_REPORT.md`. UPDATE 2026-06-28: Baris exported TradingView `BATS:SPY` 10m Chart Data CSV chunks into `00_INBOX/USER_INTAKE/`; next worker should run the prepared handoff `11_TRIAGE/CLAUDE_PROMPT_FINISH_TRADINGVIEW_SPY_10M_NATIVE_SMOKE_2026-06-28.md` to consolidate/validate data, build a SPY 10m bundle if valid, and run only a `SMOKE ONLY / NOT PROMOTABLE` one-symbol smoke if safe. **DONE 2026-06-28 (Claude Opus 4.8) — SMOKE SHIPPED, infra blocker partially lifted for SPY.** Consolidated SPY export validated PASS (20,094 clean RTH-only 10m bars, 0 dups/gaps/OHLC-violations, no volume, adjustment unknown) → `11_TRIAGE/TRADINGVIEW_SPY_10M_DATA_VALIDATION_2026-06-28.md`. Built native bundle `03_QUANTLENS/data/native_us_equities_10m_spy_tradingview_2026-06-28/` (`normalized/BATS_SPY_10m.csv` + `manifests/dataset_manifest.json`). Ran the smallest cell (1 strat × SPY × 10m, 75 trials, `MEGA_OUTPUT_DIR` redirected so nothing touched `05_BACKTEST_RESULTS`): exit 0, **real** result = `INSUFFICIENT_TRADES` (17 lockbox trades, net −0.773% vs B&H +8.90%, robust_final=false). `SMOKE ONLY / NOT PROMOTABLE`. Report `11_TRIAGE/SPY_10M_NATIVE_SMOKE_REPORT_2026-06-28.md`. NO `backtest_profile_result.json` / `top_results.json` generated (one-row insufficient-trades smoke). **UPDATE 2026-06-28 (Barış approved multi-symbol):** QQQ+AAPL validated PASS (identical clean structure); 3-symbol bundle `03_QUANTLENS/data/native_us_equities_10m_us3_tradingview_2026-06-28/` + 3-cell smoke (exit 0, output redirected): SPY/QQQ=INSUFFICIENT_TRADES, AAPL=FAIL, all net-negative & below buy&hold, all robust_final=false → still SMOKE ONLY / NOT PROMOTABLE, no artifacts. All 10m chart data is in `00_INBOX/USER_INTAKE/` (SPY/QQQ/AAPL only). **PARAM SWEEP DONE 2026-06-28 (Barış approved) → 8EMA SHELVED on US equities.** All 75 grid configs × SPY/QQQ/AAPL, full + lockbox OOS: 0/75 positive SPY, 0/75 QQQ, 1/75 AAPL (breakeven noise, 16 OOS trades). Zero beat buy&hold. Report `11_TRIAGE/SPY_QQQ_AAPL_10M_8EMA_PARAM_SWEEP_2026-06-28.md`. Pipeline proven on native US-equities 10m; **strategy is the blocker, not infra.** No full soak, no engine gating, no artifacts. **MULTI-STRATEGY SWEEP DONE 2026-06-28 (Barış "do all options"):** all 15 distinct engine strategies × SPY/QQQ/AAPL on native bundle. Exploratory best-of-grid flagged DONCHIAN/VWAP/GOLDEN_CROSS; honest engine walk-forward+DSR on top 3 × 3 symbols (9 cells) = only 1 PASS (DONCHIAN/AAPL +2.18% OOS, not DSR-robust p=0.215), 0 robust_final. Stage-A survivors = multiple-testing noise. **No promotable strategy on SPY/QQQ/AAPL 10m — crypto-era library does not transfer.** Report `11_TRIAGE/US_EQUITIES_10M_MULTI_STRATEGY_SWEEP_2026-06-28.md`. **Infra blocker FULLY CLOSED** (pipeline proven end-to-end on native US-equities 10m). Created discoverable data inventory `03_QUANTLENS/data/README.md` (native bundles + crypto locations + `MEGA_BUNDLE_MANIFEST` reuse contract). **Next human decision:** pursue NEW strategy logic and/or more symbols+longer history; adjustment policy + equity-session gating moot until a real edge exists. **UPGRADE 2026-06-28 (Alpaca):** Barış gave Alpaca paper key → wrote `03_QUANTLENS/tools/alpaca_download_us_equities_10m.py`, pulled 7 symbols (SPY/QQQ/AAPL/MSFT/NVDA/AMZN/TSLA) ~57.7k bars each (~6yr, adjusted, with volume) → bundle `native_us_equities_10m_alpaca_2026-06-28`. Full engine sweep (140 cells): **15 PASS (was 1), still 0 DSR-robust.** **GEN_DONCHIAN_BREAKOUT = lead: +OOS on 5/7 symbols, beats buy&hold on AAPL+TSLA.** Report `11_TRIAGE/US_EQUITIES_10M_ALPACA_6YR_SWEEP_2026-06-28.md`. Still NOT PROMOTABLE (no cell DSR-robust; best DSR confidence 0.46, need ≥0.95 — DSR is higher=better, earlier "≤0.05" wording was backwards, corrected). **DONCHIAN cross-sectional DSR DONE → LEAD CLOSED:** one shared config on all 7 symbols, 488 pooled OOS trades, mean R +0.03, PF 1.06, bootstrap p=0.27, DSR conf 0.22 → not significant, not robust; "5/7 positive" was per-symbol cherry-picking (only QQQ/AAPL positive under shared config). Report `11_TRIAGE/DONCHIAN_CROSS_SECTIONAL_DSR_2026-06-28.md`. **No existing strategy has a robust edge on native US-equities 10m even with 6yr×7sym.** Infra fully done + reusable; productive path = NEW strategy logic. 24MB CSVs + run outputs git-ignored; manifest/script/reports committed. **COMPLETE DATASET BUILT 2026-06-29 (Barış request, ran overnight):** `tools/alpaca_download_dataset.py` → bundle `native_multiasset_alpaca_2026-06-28`: **51 symbols × 7 TF (10m..1d) = 357 datasets, 357/357 PASS, ~11.86M bars, 711MB.** Indices+stocks+commodity/bond/sector ETF proxies+VXX+intl+12 crypto. Adjusted, with volume. NO forex/futures (Alpaca limit — deferred to other providers). 711MB CSVs git-ignored; manifest+script+README committed. **This is now the PRIMARY research substrate.** Next: test NEW strategy logic across asset classes/TFs on it (no existing strategy is DSR-robust). Still open after data decision: (c) top_results.json only once a real same-bucket multi-row set exists; (d) keep converter as only sanctioned path. DONE 2026-06-28: (e) converter/read-model now expose `provenance.universe_mismatch` as a strict boolean and carry text in `universe_mismatch_reason`, with legacy string artifacts normalized at read time.
12. DONE 2026-06-16: Launcher single-instance follow-up (audit nits). `-StatusOnly` now truly non-mutating (moved before `Limit-LogSize`, prints via `Write-Output` not the launcher log) — verified log size/mtime unchanged across 2 runs. Startup auto-start CORRECTED: one per-user Startup VBS `MTC_Command_Center_Dashboard.vbs` exists and points to the guarded `run_dashboard_server.ps1` (prior "no auto-start found" was stale); no duplicate VBS; nothing created/deleted. Re-verified: 2 launches skip, count=1, `POST`→405, `/healthz`+snapshot=200, 69 tests OK, PARSE_OK. Report: `11_TRIAGE/DASHBOARD_LAUNCHER_SINGLE_INSTANCE_FOLLOWUP_REPORT_2026-06-15.md`.
13. AUDITED 2026-06-16 (impl pending): `/api/snapshot` perf. Measured **115.56 MB** (121,172,209 B), warm fetch 10.2s / cold ~60s. Root cause = scorecard data embedded 3-4×. Biggest: `scorecards.by_strategy` 31.6MB (**UI never reads it**), `scorecards.cards` 30MB (used; gates1/1B/2/3 sub_scores ~26MB), `candidate_audit` 8.4MB (**UI-unused**, CLI/tests only), `candidate_pipeline.rows[].scorecard_v2_cases` 7.1MB (**UI uses count only**, app.js:400 already accepts a number). Full analysis + UI dependency map: `11_TRIAGE/SNAPSHOT_PAYLOAD_PERFORMANCE_AUDIT_2026-06-16.md`.
   - DONE 2026-06-16 (L1+L2+L3): snapshot slimmed **115.56MB → 44.64MB (−61%)**. `read_model._slim_http_snapshot()` drops `scorecards.by_strategy`, omits top-level `candidate_audit` (reader/CLI/tests intact), collapses `candidate_pipeline.rows[].scorecard_v2_cases` arrays → int count. Zero frontend change. 69 API tests OK; `node --check` OK; `/healthz`=200 read_only; `POST`→405. Report: `11_TRIAGE/SNAPSHOT_PAYLOAD_SLIM_LOW_RISK_PATCH_REPORT_2026-06-16.md`.
   - DONE 2026-06-16 (M1): snapshot **44.64MB → 4.45MB** (−90%; vs original 115.56MB = −96%). `read_model._slim_http_snapshot` strips per-card gate `sub_scores` + collapses `notes`→count/preview (all 837 cards) and strips pipeline `scorecard_v2` gate sub_scores; scores+statuses+gate_summary kept inline. Full cards retained in `_FULL_SCORECARDS_CACHE`; new read-only `GET /api/scorecard-detail?strategy_id=` (server.py, param-validated, no path read, 400/404/200, POST→405) + `build_scorecard_detail`. app.js: `state.detailCards`, `loadStrategyDetail`/`detailBestCard`, fetch-on-open in renderIntelligence, subscoreList loading/summary-only states, advancedSection uses loaded detail. 69 API tests OK; `node --check` OK; `/healthz`=200; `POST` both endpoints 405; detail GEN_ATR_PULLBACK_TREND→11 cards/565KB/has_sub. Report: `11_TRIAGE/SNAPSHOT_GATE_DETAIL_LAZY_LOAD_PATCH_REPORT_2026-06-16.md`.
   - ▶ OPTIONAL (polish, not bloat): gzip JSON responses (transport-only); cache detail-by-id across views. Snapshot size goal achieved.
Report: `11_TRIAGE/BACKTEST_ARTIFACT_READER_INTEGRATION_REPORT_2026-06-15.md`.

## ARCHIVED / HISTORICAL - night_3M_2026-06-08 run notes (launched 2026-06-08 23:29)

Launched by DeepSeek v4 Pro. 59 strategies, 20 workers, ~210K evals/iter, target 15+ iters = 3M+ cases. Post-loop validation auto-runs after 8h deadline (~07:29).

### Morning tasks [AI: Any|DeepSeek]:
1. **Verify completion:** read heartbeat + log
   - `cat tools/overnight_runs/night_3M_2026-06-08.log`
   - `cat tools/overnight_runs/_heartbeat_night_3M_2026-06-08.json`
   - Check for `=== ALL DONE ===` marker
2. **Read morning report:** `05_BACKTEST_RESULTS/night_3M_2026-06-08/MORNING_REPORT.md`
3. **MCC visibility:** Run `mcc_night_tail.sh` on the best iter if scorecards need enrichment (D009: use `run_python_clean.py`). Verify `/api/snapshot?refresh=1` shows new run.
4. **Write lessons:** `11_TRIAGE/lessons_archive/OVERNIGHT_LESSONS_2026-06-08.md`
5. **No promotion:** All results are research-only per deterministic soak nature (A19). Gates must prove edge independently.

## ▶ CODEX PICKUP 2026-06-08 — 5 open items (full detail: `_AI_MEMORY/CODEX_PICKUP_2026-06-08.md`)

1. **Night-runs → MCC** `[AI: Codex]` — DONE 2026-06-08 by Codex GPT-5. `full_sweep_2026-06-07` (122), `batch023_034_2026-06-07` (111), and final validation iter `night_1m_2026-06-07/iter_05` (122) are enriched into `scorecard_v2`. MCC scorecard reader now scans nested scorecard runs and sees 715 total cards / 46 distinct strategies. No promotion: all three 2026-06-07 batches have 0 promotable cards.
2. **UI Round-2 remainder** `[AI: Codex]` — DONE 2026-06-08 by Codex GPT-5 except Barış screenshot re-check. R2-04/05 fixed as a compact verdict/badge ladder tooltip. R2-13-deep fixed: every scorecard sub-score now carries `max_points` and a short `deduction_reason`, and the gate detail table shows the reason. R2-31 fixed: Strategy Detail now surfaces the selected scorecard file timestamp, falling back to snapshot timestamp only when no scorecard is linked. R2-36 closed as a no-code audit: Gate2 tooltip references real emitted `metrics.wfo_pass`, not a ghost requirement. Plan: `_AI_MEMORY/UI Reviev/ROUND2_PLAN.md`.
3. **QuantLens = Claude/Codex verdict** `[AI: Codex|Barış]` — DONE 2026-06-08 by Codex GPT-5 as opinion-only metadata. Added `05_REGISTRY/AI_QUANTLENS_VERDICT_REGISTRY.json`, read-only `expert_quantlens` snapshot key, row/scorecard attachment, and a Strategy Detail `QuantLens Expert Verdict` section. Current verdicts: 141 NEEDS_CLARIFICATION, 46 RESEARCH_ONLY, 25 SALVAGE, 0 PASS. Scorecard remains the only scoring authority.
4. **AI strategy naming** `[AI: Codex|Barış]` — DONE 2026-06-08 by Codex GPT-5 as display-only metadata. Added `05_REGISTRY/AI_STRATEGY_NAME_REGISTRY.json` and read-only API attachment; current snapshot applies names to 176/176 pipeline rows and 715/715 scorecards. Barış can still rename individual entries later if desired.
5. **Backlog** — UI-30 producer_spec field-fill (needs approval), Gate3 builder (no scorer; binding decisions in memory mcc-gate3-promotion-decisions), W1 parity-in-night-flow. W2 auto-backtest-selector closed 2026-06-08 by Codex GPT-5: `03_QUANTLENS/tools/build_needs_backtest_selector.py` writes `NEEDS_BACKTEST_SELECTOR.{json,md}`; current output has 89 objective candidates. Dead `renderDecisionPanel()` cleanup closed 2026-06-08 by Codex GPT-5. Stray hung python PID cleanup checked 2026-06-08 by Codex GPT-5: PIDs 18480/57724/21200 were already absent, no kill needed.

## Dashboard UI architecture (2026-06-07)

### UI-36-CANONICAL-ROW | DONE 2026-06-07 (Codex GPT-5) | API canonical display row [AI: Codex]
- `scorecard_reader.py` now attaches `canonical` to every scorecard-merged row.
- `read_model.py` now scorecard-merges `candidate_pipeline.rows` as well as audit rows.
- Summary/schema written to `_AI_MEMORY/UI Reviev/RESULT_UI36_codex.md`.
- Validation: py_compile PASS; API unittest discovery 35 passed; live snapshot smoke PASS.
- Follow-up [AI: Claude|Codex]: migrate frontend panels to read `row.canonical` instead of raw stage/legacy fields.

## Strategy coding sprint (2026-06-07 — autonomous)

### N5-AUDIT | DONE 2026-06-07 (Claude) | 63-strateji kodlanabilirlik audit
- Kayıt: `_AI_MEMORY/N5_CODABILITY_AUDIT.md`
- 34 ALREADY_IN_ENGINE · 16 CODEABLE · 9 PRE_REG_NEEDED · 4 DISCRETIONARY · 6 PARKED_NO_DATA
- STG061+STG063: N5 agent CODEABLE dedi ama kendi spec'leri "thresholds unknown" → PRE_REG_NEEDED düzeltildi

### A1-PRODUCER-SPEC | DONE 2026-06-07 (Claude) | 41 producer_spec.json üretildi
- Script: `03_QUANTLENS/tools/generate_producer_specs.py`
- 63/63 strateji artık producer_spec.json'a sahip (41 yeni, 22 mevcut)
- 41 gerçek MEGA metrik; 22 dürüst placeholder (hiç uydurulmuş sayı yok)

### FULL-59-SWEEP | DONE 2026-06-07 (Claude + DeepSeek) | full_sweep_2026-06-07.sh dispatch [AI: Claude]
- Script: `03_QUANTLENS/tools/full_sweep_2026-06-07.sh`.
- 59 strategies via strat_batch_remaining.py chain, 18 workers.
- Result: 5015 cells, 122 evaluation artifacts, report written to `03_QUANTLENS/05_BACKTEST_RESULTS/full_sweep_2026-06-07/REPORT_full-2026-06-07.md`.
- Alpha summary: passes=122, beat_buyhold=55, premium=0, down_market_alpha=0.
- D009 shim confirmed working; scipy.stats intercepted, no BLAS hang.

### NIGHT-1M-QUIET-2026-06-07 | ARCHIVED / HISTORICAL 2026-06-07 (Codex GPT-5) | 1M quiet overnight sweep [AI: Codex|Any]
- User requested no questions, max 10 workers, quiet machine, about 1,000,000 cases after UI-audit work.
- Launcher: `03_QUANTLENS/tools/night_1m_2026-06-07.sh`; keep-awake wrapper: `03_QUANTLENS/tools/start_night_1m_2026-06-07_keepawake.ps1`.
- Output root: `03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/`.
- Live heartbeat: `03_QUANTLENS/tools/overnight_runs/_heartbeat_night_1m_2026-06-07.json` and dashboard-facing `_heartbeat.json`.
- Plan: 5 full MEGA passes at 10 workers, about 215,645 estimated configs/pass, target about 1,078,225, then validation tail on final successful pass.
- Morning action [AI: Any]: verify heartbeat/logs, read `SUMMARY_night_1m_2026-06-07.md`, validate artifacts from the final successful iter, and keep the conclusion research-only unless gates prove otherwise. Repeated passes are deterministic soak/current-code evidence, not independent statistical proof.

### STG028-034-046-053-CODING | DONE 2026-06-07 (DeepSeek v4 Pro recovery) | 5 strategies swept + validated
- File: `03_QUANTLENS/tools/strat_batch_remaining.py`
- QL_CANSLIM_SHAKEOUT_v1 (STG028) · QL_ANTI_CHASE_CRABEL_v1 (STG033)
  QL_EMA_RETEST_v1 (STG034) · QL_VWAP_TREND_CONT_v1 (STG046) · QL_HARRIS_50DMA_v1 (STG053)
- Recovery sweep: 425 jobs, 4 workers, 109.3s → 11 PASS candidates
- Gate2: 4 OK/PASS, 7 FAIL. Promotable: 0/11 (Gate3 INCOMPLETE).
- D009 fixed (scipy shim). STG061/063 remain PRE_REG_NEEDED.
- Run: `remaining_2026-06-07-recovery/`

### PRE_REG_NEEDED — Barış threshold tanımlamalı (9 strateji):
| STG | İhtiyaç |
|---|---|
| STG007 | Stage2 EMA/MA eşiği |
| STG021 | VCP kontraksiyon % eşiği |
| STG027 | RSI diverjans + CHoCH bölge genişliği |
| STG037 | 7-mum pattern geometri |
| STG054 | Fishhook derinlik/hız eşiği |
| STG058 | Parabolic SAR çarpan + "champion" filtresi |
| STG061 | Pierpont extension eşiği + danger-zone sınırı |
| STG062 | Weinstein Stage2 MA eğim + hacim eşiği |
| STG063 | Tito RS eşiği + crossback trigger |

## Overnight spec sprint (2026-06-06 — autonomous)

### SPEC-SPRINT-ALL-35 | DONE 2026-06-06 (Claude, autonomous) | 35 deterministic spec files [AI: Claude]
- Barış approved: "Tüm 35 strateji için spec yaz / Gate3: başla / ben uyuyorum sen başla"
- Written: 35 × `07_deterministic_spec.md` for STG001-022 (method reconstruction), STG023-034 (translated from run_batch.py Python functions), STG046 (parsed from Pine review script)
- All existing specs (STG035-045, STG047-063) already present → **63/63 strategies now have spec files**
- Committed as `915611f` (62 files, 2333 insertions)
- Registry regenerated: review_needed 1447 → 1251 (−196 placeholders)
- Known limit: STG001-034 and STG046 have no `01_candidate_metadata.yaml` → `known_strengths`/`known_weaknesses` registry fields remain review_needed until those files are created

### GATE3-LIFECYCLE-INVEST | DONE 2026-06-06 (Claude, autonomous) | Gate3 lifecycle test investigation [AI: Claude]
- Investigated "5 failing lifecycle tests" from prior context
- Result: **286 tests pass, 0 failures** across all test suites (35 + 251)
- The prior "lifecycle failures" were scorecard-level blockers, NOT pytest failures
- MEV-004 still open: `pending_queue`, EOD/EOW time-stop, consecutive-loss reset, max-pyramid guard = real test failures in the MTC engine lifecycle test suite (not the pytest suite)
- Gate3 score: 97.0/100 INCOMPLETE for `QL_FAM_MOMENTUM_CONTINUATION|TRXUSDT|4h`
- No code changes made; no tests broken

### PINE-BACKTEST-CHECK | DONE 2026-06-06 (Claude, autonomous) | Pine code availability check [AI: Claude]
- Checked all Pine files in pinets/ — 3 found, none are strategies ready for overnight backtest without additional setup
- No new backtests started (insufficient setup for autonomous execution)

## S6 worker monitor UI (2026-06-06)

### S6-D3B-WORKER-MONITOR | DONE 2026-06-06 (Codex GPT-5) | Overnight runner heartbeat widget [AI: Codex]
- Added embedded Worker Monitor card to Backtest Summary, using `snapshot.overnight_heartbeat`; no new top-level tab.
- Current source snapshot renders offline state with reason `overnight_runs dir not found`.
- Files changed: `08_DASHBOARD_APP/apps/web/app.js`, `08_DASHBOARD_APP/apps/web/index.html`, `08_DASHBOARD_APP/apps/web/styles.css`, `_AI_MEMORY/PARALLEL_AGENT_REPORTS/S6_D3B_WORKER_MONITOR_REPORT.md`.
- Validation: D3a prerequisite PASS; `node --check app.js` PASS; clean dashboard server health PASS; browser verification PASS on `http://127.0.0.1:8766/dashboard`; API pytest blocked by missing `pytest`; DeepSeek review blocked by missing `openai`.

## S5 dashboard acceptance panel (2026-06-06)

### S5-CODEX-A8 | DONE 2026-06-06 (Codex GPT-5) | Global acceptance criterion panel [AI: Codex]
- Added global `MCC System Status` panel at the top of the main dashboard content, visible on the default Pipeline screen without opening a strategy.
- Panel derives from `snapshot.scorecards.cards`: best candidate, blocked count/reason, scorecard totals, Gate2 PASS, Gate3 OK, and next action.
- Live values verified: 349 scorecards, 1 promotable, 125 Gate2 PASS, 1 Gate3 OK, 348 blocked; best `QL_FAM_MOMENTUM_CONTINUATION|TRXUSDT|4h`.
- Validation: `node --check app.js` PASS; dashboard health PASS; browser verification PASS; API pytest blocked by missing `pytest`; DeepSeek review blocked by missing `openai`.

## S2 dashboard UI components (2026-06-06)

### S2-CODEX-UI | DONE 2026-06-06 (Codex GPT-5) | A5/A6/A7/D4 dashboard components [AI: Codex]
- Implemented detail-page Gate2 Backtest Evidence renderer from `scorecard_v2.gate2.metrics`, Not Promotable blockers panel, Pipeline gate-status filters, and Backtest run detail panel.
- Files changed: `08_DASHBOARD_APP/apps/web/app.js`, `08_DASHBOARD_APP/apps/web/index.html`, `08_DASHBOARD_APP/apps/web/styles.css`, `_AI_MEMORY/PARALLEL_AGENT_REPORTS/S2_CODEX_UI_REPORT.md`.
- Validation: `node --check app.js` PASS; dashboard health PASS; browser verification PASS for A6, A7, D4, and A5 no-data state. API pytest blocked by missing `pytest`; DeepSeek adversarial review blocked by missing `openai`.
- Caveat: current live snapshot scorecards have empty `gate2.metrics`, so positive metric-card rendering remains data-dependent. No metrics were fabricated.

> **MASTER PLAN (2026-06-06):** MCC mimarisini tamamen bitirme + tüm stratejileri ilerletme iş planı → [[MCC_COMPLETION_MASTER_PLAN]] (`_AI_MEMORY/MCC_COMPLETION_MASTER_PLAN.md`). Workstream A (UI), B (pipeline), C (Gate3 — asıl blocker, builder yok), D (gece-veri→UI), E (promosyon hattı). Barış kararı bekleyen: C0 (production tanımı), B3 (confirmation grid), C2/C3 (entegrasyon onayı).

## Codex continuation closure (2026-06-06)

### C3-DRY-RUN-GATE3 | DONE 2026-06-06 (Codex GPT-5) | Dry-run adapter evidence, no live path [AI: Codex]
- Added `07_ADAPTERS/liveops/dry_run_adapter.py`, tests, and README. Generated C3 evidence for the 9 `fam_templates_2026-06-06` all-gate artifacts under `03_STATUS/dry_run_evidence_2026-06-06/`.
- `LIVEOPS_STATUS.json` now records dry-run mode only: live trading false, webhook sending false, broker integration false, 9 simulated-signal events, 0 live orders, 0 webhook sends.
- Gate3 moved from 46.0 to 91.0 for the family-template readiness artifacts, but remains **INCOMPLETE** and `promotable=0` because MTC risk-engine compatibility and backtest-to-live matching are still unproven.
- Validation: py_compile PASS, dry-run tests 4 PASS, 9/9 readiness artifacts schema-valid, clean score_gate3 pass=0, score_all_gates promotable=0.

### B2-REMAINING-SHORT-MR | PARKED 2026-06-06 (Codex GPT-5) | STG047/STG054/STG055 not safe on crypto data [AI: Baris|Codex]
- STG047 Brian Lee small-cap gap MR short requires US-equity gap-up scanner, low-float context, prior resistance, borrow/short frictions, and session/EOD behavior.
- STG054 fishhook EP day-1 retake requires equity episodic-pivot gap+run/day-after retake and session semantics.
- STG055 Gon low-float momentum requires low-float scanner, halt/resume events, premarket momentum, and float/volume filters.
- Decision: do **not** code crypto proxy variants. They are parked until a US-equity data source with session/float/halt fields exists.

### A3-GAP-MATRIX-DEEPSEEK-DISPATCH | DONE 2026-06-06 (Codex GPT-5) [AI: Codex|DeepSeek]
- Added `_AI_MEMORY/A3_GAP_MATRIX.md`.
- Added `_AI_MEMORY/DEEPSEEK_DISPATCH.md` with five read-only/skeptical review prompts: family mapping, no-lookahead safety, C3 adapter safety, documentation cleanup, and MOMENTUM_CONTINUATION 4h skeptical review.

## New-strategy coding (2026-06-06)

### NEWSTRAT-STG056 | DONE 2026-06-06 (Claude) | Oliver Kell price cycle coded + swept [AI: Claude]
- Registry had 63 strategies but engine GRIDS only 43 → coded one genuinely-missing backtestable candidate. Picked **STG056 Oliver Kell** (clean objective spec, pure-EMA, crypto/daily fit). STG052 (CANSLIM — needs fundamentals, no data), STG047/STG054 (equity gap plays, weak crypto fit), STG057 (LBR — needs threshold/pattern judgment, pre-register first) deliberately NOT auto-coded.
- New file `03_QUANTLENS/tools/strat_extra_runner.py` (monkey-patch layered on overnight_v2_runner, **no edit to mega_walk_forward.py or v2**). Faithful long-side mapping of `07_deterministic_spec.md`: 10/20-EMA green-light + snapback (was-below-slow within snap_lb) + wedge-pop crossback above fast EMA + higher-low; swing-low stop. All `.shift(1)` — no lookahead. Grid 36 configs.
- Smoke PASS (non-degenerate: 40-50 trades/fold). Full sweep: 68 cells (17 sym × {1h,2h,4h,1D}), **2 PASS** (TRX 4h/2h), DSR 0.031/0.041. CPCV (extra-runner loaded): both TRX **15/15 splits pass** (120/158 trades). Gate2 80.4/83.5 **INCOMPLETE** (single/few-candidate PBO insufficient — not FAIL). Output: `05_BACKTEST_RESULTS/new_strategies_2026-06-06/` (+ top-level `_results.json`, dashboard COMPLETED).
- **Verdict: works + CPCV-robust on TRX but DSR-floored + likely TRX bull-beta → NO promotion, no Pine/MTC/parity/live.** Same night-wide pattern (deeper validation can't beat DSR). Strategy reusable in engine via `strat_extra_runner.py`.
- **Carry-forward:** STG057 LBR (ROC2-reversal / 3-bar-breakout / coil-expansion) + STG054 fishhook + STG047 smallcap-gap-short are codeable the same way once Barış pre-registers the threshold/pattern definitions (avoids me inventing params → keeps DSR valid). STG056 not registered in generated registries (AGENTS.md: generator-produced); logged here + handoff only.

## Confirmation Run Follow-up (2026-06-04)

### NIGHT-CONFIRM-2026-06-04 | DONE | Quiet pre-registered confirmation run + validation tail [AI: Codex GPT-5]
- Resumed Claude's interrupted Option B path and launched the quiet confirmation run with 4 workers.
- Output: `03_QUANTLENS/05_BACKTEST_RESULTS/confirm_2026-06-04/MORNING_REPORT_confirm_2026-06-04.md`.
- Result: 306 cells / ~3,672 configs / 16 PASS / 1 BH-FDR survivor / 0 DSR-robust / 0 final robust.
- A18 fixed in output: down-market alpha count/table now matches canonical `alpha_summary.json` (`down_market_alpha=6`).
- Validation tail done: CPCV, PBO, 16 evaluation artifacts, 16 Gate-2 scorecards. Scorecards: all INCOMPLETE, 0 pass.
- Morning watchdog active until 2026-06-05 07:30 local: `03_QUANTLENS/tools/overnight_runs/_heartbeat_confirm_morning_watchdog.json`.
- No Pine/MTC/parity/live-trading action is authorized by these results.

### NIGHT-CONFIRM-2026-06-05-REVIEW | DONE 2026-06-05 (Claude) | Morning review of confirmation artifacts [AI: Claude|Baris]
- Reviewed report + CPCV/PBO + 16 scorecards. A18 verified (down_market_alpha=6 == ALPHA_DONE).
- DSR rose wide→narrow (0.0→0.34-0.38 best) but none ≥0.50; Gate-2 16/16 INCOMPLETE (metric gap, not FAIL).
- **Decision:** no promotion. Forward-paper observation OPTIONAL for 2 least-weak cells: 8EMA LINK 1h, Donchian ETH 2h. No Pine/MTC/parity/live action.
- Closure done: lessons C4-C6, runbook A19 + CHANGELOG, INDEX already had 06-05 line.

### NIGHT-FOLLOWUP-HEAVY-TIER | PARTIAL DONE 2026-06-05 (Claude) | Compute-filling heavy-validation tier [AI: Claude|Barış]
- **Problem (A19):** deterministic narrow confirmation finishes in minutes; machine sat idle-awake on watchdog the rest of the night. Tekrar = sıfır bilgi (seed=md5, mega:731).
- **DONE 2026-06-05 evening (Claude):** built `heavy_night_2026-06-05.sh` + `heavy_night_report.py`. Ran first **43-strategy** enriched sweep (3655 cells, 72 PASS+ vs 38 in the 20-strategy run) + **3×-deeper CPCV** (n_groups=10 → 45 splits, 24 cells ≥0.80) + PBO + 72 eval artifacts + Gate2 (53 PASS/19 FAIL) + scorecard_v2 (0 promotable, Gate3 INCOMPLETE). Output: `05_BACKTEST_RESULTS/heavy_tier_2026-06-05/` (+ top-level `heavy_tier_2026-06-05_results.json` for dashboard; verified visible, COMPLETED). Report: `heavy_tier_2026-06-05/HEAVY_TIER_MORNING_REPORT.md`. Closure: lessons C7/C8 + runbook A20/A21 + CHANGELOG.
- **Key finding (C7/A21):** deeper CPCV does NOT rescue DSR — Gate2 PASS ∧ CPCV-deep≥0.80 ∧ DSR≥0.50 = **0/72**. DSR trial count = grid size, not split count (A17). Re-confirms: go narrow (NIGHT-FOLLOWUP-002), not deeper/broader.
- **STILL OPEN (deliberately not autonomous):** multi-seed bootstrap stability is statistically trivial at n_boot=50k (MC SE ~0.002 → seed jitter negligible; "multi-seed DSR" moot under determinism). ±2-step pre-registered grid + 4h/1D neighborhood backtests = genuinely-new param-evals but need Barış design sign-off (A17: wider grids harm DSR). `probabilistic_pbo` lazy/random combo sampling fix (A20) for deep-CPCV PBO.
- **No Pine/MTC/parity/live action taken. No promotion (Gate3 blocker stands).**

## SP-004 rubric sign-off (2026-06-04)

### SP-004-SIGNOFF | DONE | D1-D6 owner decisions resolved [AI: Claude | Barış]
- Barış signed D1-D6 (DECISIONS D007). Rubric `12_STRATEGY_EVALUATION_RUBRIC.md` updated: D1 Gate 1B → /100 PASS≥75 (criteria rescaled ×2), D3 parity → advisory (PARITY_WARNING, non-blocking), D2/D4/D6 accepted, D5 deferred to Phase 1.5. **Unblocks Phase 2 scoring lock.**

### SP-004-PHASE1-EVALARTIFACT | DONE | evaluation_artifact writer [AI: DeepSeek/Claude]
- Done (2026-06-04 Batch G/H): `03_QUANTLENS/tools/build_evaluation_artifact.py`. CLI `--mega --cpcv --pbo --out-dir`; pure `build_artifact()`; status-enveloped metrics (OK only when computed, else NOT_COMPUTED/N_A, never auto-zero); hard_flags/flags bare per schema; version 'v1'. Claude-audited on real 5MB MEGA: 149 artifacts, 0 schema errors (Draft2020-12+$ref), 0 fabricated numbers.
- Known limits (intentional): per-fold arrays dropped from metrics (scalars only); repaint_status=null (no repaint stage), parity_status='N_A', has_benchmark=false — fill when those stages exist.

### SP-004-PHASE2-SCORINGREADER | DONE | gate2 scoring reader [AI: DeepSeek/Claude]
- Done (2026-06-04 Batch I/J): `03_QUANTLENS/tools/score_gate2.py` (`score_gate2(artifact)->dict`, CLI `--in-dir --out-dir`). 25 criteria /100 per rubric §5.1-5.7; status-gated (non-OK metric → not scored → gate INCOMPLETE, never auto-zero); REJECT_REPAINT→FAIL; PBO≥0.5→OVERFIT_SUSPECT advisory; parity advisory; pass=(OK and ≥75). Batch J reconciled Phase-1 writer to emit schema metric vocabulary. Claude-audited real 5MB: 149 artifacts 0 schema-err, 149 scorecards all INCOMPLETE (22-43, 0 pass, 0 fabricated).

### SP-004-PHASE3-GATESCORERS | DONE | Gate1/1B/3 + unified composer [AI: Grok/Claude]
- Done (2026-06-05, dispatched to Grok grok-4 via `ds_agent.py`, Claude-audited on real data; DeepSeek was 402 Insufficient Balance).
- New files under `03_QUANTLENS/tools/`: `score_gate1.py` (intake /100, 35 criteria, `intake.*` envelopes), `score_gate1b.py` (MTC feasibility /100 PASS≥75, `feasibility.*`, D1 verdict PASS/CONDITIONAL/FAIL), `score_gate3.py` (production-readiness /100, reads `production_readiness_artifact_v1` groups per D4, 37 criteria), `score_all_gates.py` (unified composer → one `scorecard_v2`, no top-level number; `gate_summary.promotable` honest = all four OK+pass).
- All mirror `score_gate2.py`: pure `score_gateX(artifact)->dict` + CLI `--in-dir --out-dir`; status-envelope (only OK scores, non-OK → `points_awarded=None` → gate INCOMPLETE, never auto-zero); `REJECT_REPAINT`→FAIL; parity advisory; utf-8 stdout.
- Claude audit (real 16 confirm-2026-06-04 eval artifacts + synthetic): py_compile PASS ×4; full-OK→100/OK/pass; empty→INCOMPLETE; gate1 MEDIUM-repaint→98; REJECT_REPAINT→FAIL; composer all-OK→promotable. **Real 16/16 = all gates INCOMPLETE, 0 pass, 0 promotable** — correct honest status (intake/feasibility/readiness artifacts not emitted yet). Inline fix: gate1b verdict PASS-under-REJECT_REPAINT → hard-fail override.
- Carry-forward: these gates stay INCOMPLETE until writer artifacts exist (intake/feasibility for Gate1/1B; `production_readiness_artifact_v1` for Gate3; Gate2 metric-enrichment below). Scorers ready to score the moment those are emitted. Nothing committed.

### SP-004-METRIC-ENRICHMENT | DONE + COMMITTED (88a79e0) | enrich builder + engine output [AI: Claude/DeepSeek | Barış approved 2026-06-05]
- Barış approved 2026-06-05 (touches MTC strategy OUTPUT, not signal/Pine/parity logic). Done via DeepSeek dispatch + Claude audit.
- **Builder (`build_evaluation_artifact.py`, Task A):** replaced the blanket-N_A block with honest per-metric derivation from data MEGA already emits — `return_pct_compound`, `recovery_factor`, `calendar_days` (from data_start/end), `multi_window_pass` (folds_positive==n_folds), `net_after_fees_pct` (cost already in net), `avg_trade_vs_cost` — plus forward-compatible passthrough for engine-emitted fields. **Integrity call (Claude): `sharpe`/`sortino` kept N_A** because MEGA's lockbox `sharpe` is a t-stat-like per-trade scaled value, NOT the annualized Sharpe the rubric scores — mapping it would inflate the gate. `param_stability_score`, `regime.*`, `long_short_ratio`, `net_after_slippage_pct` honestly N_A. Audit: rebuilt real 16 confirm artifacts, **0 schema errors** (Draft2020-12+$ref), values hand-verified; gate2 scores moved **22–43 → 42–60** (still INCOMPLETE, 0 pass, 0 fabricated — correct).
- **Engine (`mega_walk_forward.py`, Task B):** additive OUTPUT only — added `max_consecutive_losses`, `top_trade_concentration`, `equity_curve_health` to `SliceStats`/`simulate_slice` (computed from the existing per-trade `arr`/`eq`; `asdict` auto-propagates into `lockbox_oos`). No existing field/value/trade-logic changed (verified: diff additive, formulas hand-checked mcl=1/conc=0.3333/health=0.6, import-failure is pre-existing/environmental on HEAD too). Builder passthrough will surface these on the **next** MEGA run.
- **Still N_A until further work:** sharpe/sortino (need annualized definition or time-series equity), regime.* (no regime stage), benchmark.excess_alpha/beats_ema (needs B&H-on-same-window stage), worst_window_drawdown_pct, param_stability_score. Full Gate-2 PASS also needs a **fresh sweep** under the enriched engine (Barış OPS — not run here; existing artifacts built from old MEGA JSON so the 3 new engine metrics are still N_A in them).
- **NOT COMMITTED (deliberate):** `mega_walk_forward.py` carries ~245/-50 of pre-existing uncommitted Batch A–J engine work; `build_evaluation_artifact.py` is untracked Batch G/H/J. Per the standing "leave Batch edits for Barış" rule, my enrichment rides on top uncommitted — Barış decides when to commit the combined engine/builder state.

### SP-004-METRIC-ENRICHMENT-RUN | DONE | fresh sweep under enriched engine [AI: Claude, Barış go-ahead 2026-06-05]
- Ran 2026-06-05 (Claude): full MEGA sweep under enriched engine (commit 88a79e0). 1700 cells / 14m43s / 8 workers; 38 PASS+STRONG_PASS. Validation tail: CPCV (v2 patch) + PBO. Built 38 enriched artifacts + 38 Gate-2 scorecards.
- **Result (regeneration, NOT promotion):** new engine metrics (max_consecutive_losses/top_trade_concentration/equity_curve_health) + builder-derived (recovery/calendar_days/multi_window_pass/net_after_fees/avg_trade_vs_cost) + cpcv/pbo now OK 38/38. Gate-2 scores **22–43 → 39–64 (mean 51.8, top 63.6)**. Still all INCOMPLETE / 0 pass / 0 fabricated / 0 schema errors — sharpe/sortino/regime/benchmark honestly N_A.
- Output (on disk, untracked like other run dirs): `05_BACKTEST_RESULTS/enriched_metrics_2026-06-05/` (results json, cpcv, pbo, evaluation_artifacts, scorecards, ENRICHED_RUN_SUMMARY.md). No Pine/MTC/parity/live action authorized.
- **Remaining for full Gate-2 PASS (genuine future work, not fakeable):** annualized Sharpe/Sortino (needs time-series equity, not per-trade R), a regime-split stage, and a same-window Buy&Hold benchmark stage. These are the only blockers between INCOMPLETE and a scorable PASS.
- **Finding:** all 149 cells score INCOMPLETE because MEGA/CPCV/PBO don't produce: sharpe, sortino, recovery_factor, worst_window_drawdown_pct, max_consecutive_losses, calendar_days, regime_coverage_count, top_trade_concentration, long_short_ratio, param_stability_score, multi_window_pass, net_after_fees_pct, net_after_slippage_pct, avg_trade_vs_cost, equity_curve_health, return_pct_compound, benchmark.excess_alpha_pct/beats_ema, regime.* (and CPCV only ran on a few cells → cpcv_pass_ratio mostly N_A).
- To make Gate 2 fully scorable: enrich the backtest engine (mega_walk_forward) to emit these per-cell (OOS sharpe/sortino/recovery/regime split/benchmark), and run CPCV across all PASS cells. Backtest-side work — needs design + Barış. Until then INCOMPLETE is the correct honest status.

### SP-004-GATE2-BENCHMARK | DONE + COMMITTED (7175ff6) | same-window Buy&Hold benchmark [AI: DeepSeek/Codex GPT-5]
- Done 2026-06-05 via DeepSeek dispatch + Codex audit. `mega_walk_forward.py` now emits `summary.buy_hold_lockbox` for the exact lockbox window: buy at first lockbox open, hold to final lockbox close, with return, positive max drawdown, and finite return/DD ratio.
- Codex audit fixes applied: entry baseline included in the B&H equity curve so immediate drawdown is counted; helper returns JSON-native floats.
- `build_evaluation_artifact.py` now sets `benchmark.excess_alpha_pct` and `benchmark.beats_bh_risk_adjusted` to OK when real B&H inputs exist, and marks `completeness.has_benchmark` dynamically. `beats_ema_benchmark` remains N_A until a separate EMA benchmark stage exists.
- Validation PASS: py_compile, synthetic helper smoke, synthetic builder smoke, and real one-cell audit `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL LINKUSDT 1h`. Real artifact benchmark OK (`excess_alpha_pct=97.989`, `beats_bh_risk_adjusted=true`), Gate2 score 56 but still INCOMPLETE due remaining N_A fields.
- Fresh sweep DONE 2026-06-05: `05_BACKTEST_RESULTS/bh_benchmark_2026-06-05_7175ff6/`. MEGA 1700 cells / 38 PASS+STRONG_PASS; CPCV+PBO+38 eval artifacts+38 Gate2+38 scorecard_v2 rebuilt. Audit: 38/38 artifacts B&H benchmark OK, `has_benchmark=true`, 0 schema errors. Gate2 scores 38.59-69.0 mean 52.1; still 38/38 INCOMPLETE, 0 pass, 0 promotable.
- Remaining blockers after B&H closure: annualized Sharpe/Sortino, worst-window drawdown, param stability, slippage, EMA benchmark, and regime split.

### SP-004-GATE2-WORST-WINDOW | DONE + COMMITTED (283d198) | worst-window drawdown metric [AI: DeepSeek/Codex GPT-5]
- Done 2026-06-05 via DeepSeek dispatch + Codex audit. `mega_walk_forward.py` now emits `summary.worst_window_drawdown_pct` as max absolute fold-test drawdown for the selected config; `build_evaluation_artifact.py` maps `metrics.worst_window_drawdown_pct` from that summary field first and does not fabricate it from lockbox max drawdown.
- Validation PASS: py_compile, diff-check, synthetic builder primary/fallback/missing checks, and real one-cell audit `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL LINKUSDT 1h` emitted `worst_window_drawdown_pct=19.452`; artifact metric OK; Gate2 worst-window criterion scored 4/4; schema errors 0.
- Fresh sweep DONE 2026-06-05: `05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/`. MEGA 1700 cells / 38 PASS+STRONG_PASS; CPCV+PBO+38 eval artifacts+38 Gate2+38 scorecard_v2 rebuilt. Audit: 38/38 artifacts B&H benchmark OK and worst-window OK, 0 schema errors. Gate2 scores 42.59-73.0 mean 56.04; still 38/38 INCOMPLETE, 0 pass, 0 promotable.
- Remaining blockers after worst-window closure: annualized Sharpe/Sortino, param stability, slippage, EMA benchmark, and regime split.

### SP-004-GATE2-ANNUALIZED-RISK | DONE + COMMITTED (15e8d47) | annualized Sharpe/Sortino [AI: DeepSeek/Codex GPT-5]
- Done 2026-06-05 via DeepSeek investigation + implementation dispatch, Codex audited. MEGA now emits `lockbox_oos.annualized_sharpe` and `lockbox_oos.annualized_sortino` from a daily strategy equity curve; old MEGA `sharpe`/`sharpe_pt` are preserved and not reused for Gate2 annualized Sharpe.
- `build_evaluation_artifact.py` maps Gate2 `metrics.sharpe` and `metrics.sortino` only from the new annualized lockbox fields. Backward rebuild of pre-annualized 38 artifacts kept Sharpe/Sortino N_A 38/38.
- Validation PASS: py_compile, diff-check, real one-cell audit, existing lockbox fields unchanged, one-cell annualized_sharpe=1.307 and annualized_sortino=2.6959, Gate2 Sharpe 5/5 and Sortino 4/4, schema errors 0.
- Fresh sweep DONE 2026-06-05: `05_BACKTEST_RESULTS/annualized_risk_2026-06-05_15e8d47/`. MEGA 1700 cells / 38 PASS+STRONG_PASS; CPCV+PBO+38 eval artifacts+38 Gate2+38 scorecard_v2 rebuilt. Audit: 38/38 artifacts Sharpe/Sortino/B&H/worst-window OK, 0 schema errors. Gate2 scores 46.25-82.0 mean 61.88; still 38/38 INCOMPLETE, 0 pass, 0 promotable because param stability/slippage/EMA/regime remain N_A.
- Remaining blockers after annualized-risk closure: param stability, slippage, EMA benchmark, and regime split.

### SP-004-GATE2-SLIPPAGE | DONE + COMMITTED (5c68419) | post-hoc slippage stress [AI: DeepSeek/Codex GPT-5]
- Done 2026-06-05 via DeepSeek dispatch + Codex audit. MEGA now emits `lockbox_oos.net_after_slippage_pct` using `SLIPPAGE_BPS_PER_SIDE=2.0` (4 bps round trip) subtracted from each existing per-trade net return before compounding; existing `COST_BPS` and `net_return_pct` are unchanged.
- `build_evaluation_artifact.py` maps Gate2 `metrics.net_after_slippage_pct` only from the new lockbox field. Backward rebuild of pre-slippage 38 artifacts kept slippage N_A 38/38.
- Validation PASS: py_compile, diff-check, real one-cell audit, existing lockbox fields unchanged, one-cell net_return_pct=75.374 / net_after_slippage_pct=67.119, Gate2 slippage 2/2, schema errors 0.
- Fresh sweep DONE 2026-06-05: `05_BACKTEST_RESULTS/slippage_2026-06-05_5c68419/`. MEGA 1700 cells, 8 workers, 1212.3s, 31 PASS + 7 STRONG_PASS = 38 candidate cells; CPCV `--v2`, PBO, 38 evaluation artifacts, 38 Gate-2 scorecards, 38 scorecard_v2. Audit: 38/38 artifacts have annualized_sharpe, annualized_sortino, net_after_slippage_pct, B&H benchmark, and worst_window_drawdown_pct OK; 38/38 schema-valid (0 errors). Gate2 scores 48.25–84.0, mean 63.69; all 38 INCOMPLETE, 0 Gate2 pass, 0 promotable. Top cell 8EMA LINK 1h score 84.0 INCOMPLETE.
- Carry-forward: slippage is no longer a Gate2 blocker. Remaining blockers: param stability, EMA benchmark, and regime split.

### SP-004-GATE2-FINAL-METRICS | DONE + COMMITTED (39b51db) | param stability, EMA benchmark, regime split [AI: DeepSeek/Codex GPT-5]
- Baris approved APPROVE GATE2 DEFINITIONS. Done 2026-06-05 via DeepSeek dispatch + Codex audit.
- Implemented output-only definitions: `param_stability_score` from per-fold selected best params with numeric-closeness fallback; EMA50/EMA200 same-window long-flat benchmark mapped to `benchmark.beats_ema_benchmark`; regime split trend/range/high_vol/low_vol using EMA200, ADX14, ATR percentile buckets mapped to regime fields and `regime_coverage_count`.
- Codex audit fixes: preserved `simulate_slice` `return_trades` two-value compatibility via `return_trade_events` flag; removed EMA lookahead by acting on previous-close cross at next open; schema-null regime safeguards.
- Validation before commit: py_compile, diff-check, real one-cell MEGA LINK 8EMA 1h, existing lockbox fields unchanged vs prior slippage audit, one-cell new fields OK (`param_stability_score` 0.899, EMA benchmark present, `regime_coverage_count` 4, schema errors 0); one-cell Gate2 score 95/INCOMPLETE only because single-candidate PBO is insufficient.
- **Fresh sweep DONE 2026-06-05:** `05_BACKTEST_RESULTS/final_gate2_2026-06-05_39b51db/`. MEGA full sweep: 1700 cells, 8 workers, 1517.4s, 31 PASS + 7 STRONG_PASS = 38 candidate cells; CPCV rerun with `--max-candidates 9999` (default 20 was corrected), CPCV 38/38 OK, PBO status OK pbo=0.014569; 38 evaluation artifacts, 38 Gate2 scorecards, 38 scorecard_v2.
- **Gate2 result: 25 OK/pass, 13 FAIL, 0 INCOMPLETE.** Top scores: 100.0 8EMA LINK 1h; 100.0 GEN_ATR_PULLBACK_TREND DOGE 4h; 99.18 GEN_RSI_OVERSOLD_REVERSAL LINK 2h; 96.06 GEN_KELTNER_BREAKOUT LINK 15m; 92.31 GEN_ZSCORE_MEAN_REVERSION DOT 15m.
- **Original scorecard_v2 still promotable=0** because Gate1/Gate1B/Gate3 envelopes were absent at sweep time.
- **Gate2 metric blockers are now fully cleared.** Subsequent all-gate evidence work below fills Gate1/Gate1B from coded MEGA evidence; Gate3 remains the real blocker.

### SP-004-ALL-GATE-EVIDENCE | DONE | Gate1/Gate1B evidence + dashboard scorecard refresh [AI: DeepSeek/Codex GPT-5]
- Done 2026-06-05 after user requested all possible remaining work. DeepSeek was delegated the bounded helper; it timed out and left partial output, then Codex audited/fixed it.
- New helper: `03_QUANTLENS/tools/build_all_gate_evidence.py`. It reads final Gate2 eval artifacts plus `MEGA_walk_forward_results.json` and emits combined all-gate artifacts with `intake`, `feasibility`, production-readiness groups, and reproducibility envelopes.
- Evidence rule: Gate1/Gate1B are scored only from coded MEGA/backtest evidence. Gate3 production readiness is not fabricated; alert adapter/state sync/fail-safe and unproven MTC risk compatibility stay N_A/NOT_COMPUTED.
- CPCV safety fix: `cpcv_validator.py --max-candidates` default is now `0` = no cap; rows are sliced only when an explicit positive cap is passed.
- Real output: `05_BACKTEST_RESULTS/final_gate2_2026-06-05_39b51db/all_gate_artifacts/` (38/38 artifacts, all MEGA-matched), plus `gate1_scorecards/`, `gate1b_scorecards/`, `gate3_scorecards/`, `scorecard_v2_all_gate/`, and refreshed dashboard-visible `scorecard_v2/`.
- Validation: py_compile PASS; 38/38 all-gate artifacts validate against both `evaluation_artifact_v1` and `production_readiness_artifact_v1`; Gate1 38 OK/pass (93-96), Gate1B 38 OK/pass (80), Gate2 25 OK/pass + 13 FAIL, Gate3 38 INCOMPLETE/0 pass, promotable 0/38.
- Dashboard/API: `http://127.0.0.1:8765/api/snapshot?refresh=1` sees the final run with 38 cards: 25 `OK/OK/OK/INCOMPLETE`, 13 `OK/OK/FAIL/INCOMPLETE`.
- Remaining blocker: Gate3 production-readiness evidence source. Needs real alert/adapter/state-sync/fail-safe/live-integration artifacts before any production OK envelopes or promotion claim. [AI: Claude|Baris]

### SP-004-SCHEMA-PARITY | DONE | Move parity to advisory in schema [AI: DeepSeek/Claude]
- Done (2026-06-04 Batch F): `06_SCHEMAS/evaluation_artifact_v1.schema.json` — `parity_gate` removed from `hard_flags`; new advisory `flags.parity_status` ∈ {PASS, WARN, N_A, null}. Claude-audited: json.load VALID, Draft2020-12 check_schema VALID, parity_gate gone everywhere, completeness intact.
- **Reader carry-forward (Phase 2):** the future scoring reader must read `flags.parity_status` (NOT `hard_flags.parity_gate`) and treat WARN as non-blocking. Captured for the Phase-2 build.

## Local YouTube Transcript Collector (2026-06-04)

### YT-TRANSCRIPT-001 | DONE | Local transcript collector utility [AI: Codex GPT-5]
- Added isolated Python tool under `YT_TRANSCRIPT_COLLECTOR/`.
- Reads `urls.txt`, extracts YouTube video IDs, fetches transcripts with `youtube-transcript-api`, prefers `tr` then `en` then any available transcript, writes Markdown under `transcripts/`, and writes `reports/transcript_index.csv` plus `reports/failed_videos.csv`.
- Safety boundary: no YouTube login, no password request, no video/audio download, no browser automation, and no account actions.
- Validation: py_compile PASS, 2 offline URL extraction tests PASS from tool folder and repo root, CLI help PASS.
- Run update 2026-06-04: fetched `2NuvYsXMehw` successfully; output `YT_TRANSCRIPT_COLLECTOR/transcripts/2NuvYsXMehw.md`; metadata `Turkish (auto-generated) (tr)`. Added UTF-8 BOM URL-file regression fix/test after PowerShell input exposed it.
- Organization update 2026-06-04: moved Hermes-related transcript files into `YT_TRANSCRIPT_COLLECTOR/transcripts/hermes/`; moved contents of `Temp/HERMES/` there and deleted the old empty folder.
- No open follow-up unless Baris explicitly requests Playwright/browser fallback after transcript-api failures.

## Hermes Agent Layer (2026-06-04)

### HERMES-001 | DONE | Install Hermes and create MTC profiles [AI: Codex GPT-5]
- Installed Hermes Agent `0.15.2` in `%LOCALAPPDATA%/hermes/hermes-pypi-venv` after the official git installer clone timed out.
- Created profiles: `mtc-steward`, `quantlens-research`, `dashboard-qa`, `backtest-monitor`, `repo-hygiene`.
- Wrote profile-specific `SOUL.md` plus shared `memories/USER.md`, `memories/MEMORY.md`, and `MTC_WORKSPACE.md` guardrails.
- PATH updated for new terminals; current shells may need restart.
- Model/provider setup intentionally not selected to avoid unapproved paid/remote model routing.

### HERMES-002 | OPEN | Configure model/provider per profile [AI: Baris]
- Run one of: `<profile> setup`, `hermes -p <profile> model`, or `hermes -p <profile> config set model <provider/model>`.
- Desktop path is now also available: open Hermes Desktop, click Settings, and choose a provider/model there. Do this only when remote/paid routing is approved.

### HERMES-003 | DONE | Install Hermes Desktop app [AI: Codex GPT-5]
- Installed official Hermes Desktop under `%LOCALAPPDATA%/hermes/hermes-agent/apps/desktop/release/win-unpacked/Hermes.exe`.
- Created Desktop and Start Menu shortcuts.
- Verified normal app launch after fixing the bootstrap marker.
- Screenshot: `C:\tmp\hermes_desktop_final.png`.
- Choose cost/routing policy before using Hermes for live agent sessions.

### HERMES-004 | CLOSED 2026-08-09 (superseded) | Install proposed MTC memory package into Hermes core memory
- Package path moved to archive: `C:\LAB\MTC_LOCAL_ONLY_ARCHIVE\2026-06-21\_HERMES_MEMORY_IMPORT\`
- Closure reason (Claude Fable 5, verified on disk): live Hermes memory already exists at
  `%LOCALAPPDATA%\hermes\memories\USER.md` + `MEMORY.md` (written 2026-06-05..07) and is NEWER and richer
  than the proposed package (adds token discipline / ds_agent rules, Telegram gateway watchdog runbook,
  multi-agent landscape). Installing the June package would be a downgrade. No copy performed.
- Residual: live MEMORY.md still tells Hermes to update SESSION_LOG.md (retired 2026-07-05) — fix when
  Hermes is next actively used.

### HERMES-005 | OPEN 2026-08-09 | openai-codex token invalidated → re-auth [AI: Baris]
- Diagnosis (request dump 2026-08-09): HTTP 401 `token_invalidated` from `chatgpt.com/backend-api/codex` —
  not quota. `auth reset` + desktop restart did not help; OAuth device token itself is dead.
- Fix: `hermes auth add openai-codex --type oauth` → complete device-code sign-in in browser with the
  ChatGPT Pro account. DeepSeek provider verified working meanwhile (`-m deepseek-v4-pro --provider deepseek`).

## SP-005 Wave A status update (2026-06-04)

### SP-005 | DONE WAVE A | Strategy Detail Page Redesign [AI: Codex GPT-5]
- Status: **SP-005 Wave A implemented; Wave B/C pending.**
- Files changed: `08_DASHBOARD_APP/apps/web/app.js`, `08_DASHBOARD_APP/apps/web/styles.css`, `08_DASHBOARD_APP/apps/api/mcc_readonly/pipeline_reader.py`.
- Implemented live Strategy Detail Page Wave A: terminal single-scroll layout, human title fallback, merged Verdict & Decision block, Scorecard placeholder directly below verdict, Strategy Taxonomy shell, Review Journey, expanded Trading Rules with visible "Not defined yet", honest Backtest Evidence unavailable state/checklist, Salvageable Ideas placeholder, de-emphasized Source Material, and collapsed Technical Details carrying raw IDs/legacy composite/debug data.
- Intentionally not implemented: SP-004 scoring math, `scorecard_v2`, QuantLens structured reader, backtest-case visualizations, source-claim-vs-reproduced visuals, filter migration to gate status, Pine/MTC/parity/backtest behavior changes, audit-data deletion.
- Validation: `node --check app.js` PASS; `py_compile pipeline_reader.py` PASS; dashboard API tests PASS (`35 passed` with `PYTHONPATH` set); browser check on `http://127.0.0.1:8765/dashboard` confirms all Wave A sections render, first tested title is not raw ID, Technical Details collapsed, missing fields visible, no desktop horizontal overflow after CSS containment.
- Data caveat: current snapshot has no row with real `metrics`, so metrics-present Backtest Evidence could not be visually verified. Missing-rules, legacy-score-only, and no-QuantLens states were verified from snapshot data.

### SP-005 | DONE WAVE B | QuantLens structured reader + detail-page card [AI: Claude]
- Reader DONE (2026-06-05, dispatched to Grok grok-4, Claude-audited): read-only `08_DASHBOARD_APP/apps/api/mcc_readonly/quantlens_reader.py` parses `03_SALVAGE_IDEAS/<candidate>/01_candidate_metadata.yaml` (PyYAML, guarded import). Emits per-candidate `quantlens_verdict` (decision label, commercial-value band §8.6, complexity, testability §8.7, risks — commentary/labels, NO computed score), structured `salvageable_ideas[]` from `candidate_kind` flags, derived `stop_state` (CLOSED_SOURCE_STOP from closed_source_risk HIGH / COMPLEXITY_OVERLOAD from complexity≥8 / GARBAGE), `reference_files` repo-relative links, JSON-safe `raw`. Wired `quantlens` key into `read_model.py`. Fixed 2 audit bugs (ref-files→dir; date→str coercion). Dashboard API tests 35 passed.
- UI DONE (2026-06-05, Claude): `apps/web/app.js` — `findQuantlensCandidate` (joins by candidate_id===row.id, confirmed all 3 match pipeline/audit rows), new `renderQuantlensVerdict` card (decision badge, stop-state banner, commercial/complexity/testability/instrument facts, risk chips, recommended next step), real `renderSalvageableIdeas` from `salvageable_ideas[]`, `buildWaveADecision` now surfaces the real QuantLens label. Section order Verdict→Scorecard→QuantLens Verdict→Taxonomy. `styles.css` adds `.quantlens-stop`. Verified live in the running dashboard (preview): QL strategy renders full card (Equilibrium: SALVAGE, 4/10, 4 components), non-QL strategy shows clean "Not in QuantLens" fallback, no JS error, `node --check` PASS. Not committed.
- Carry-forward: stop-state banner code path (CLOSED_SOURCE_STOP/COMPLEXITY_OVERLOAD) is wired but unverified live (no on-disk candidate currently has a stop_state; all 3 are SALVAGE/no-stop).

### SP-005 | DONE WAVE C | scorecard_v2 gate render [AI: Codex GPT-5]
- Implemented 2026-06-05 as read-only dashboard consumption of real `scorecard_v2` artifacts.
- Added `mcc_readonly/scorecard_reader.py`; `read_model.py` now exposes top-level `scorecards` and attaches `scorecard_v2` / `scorecard_v2_cases` to matching audit/pipeline rows by base strategy id.
- Generated 38 real all-gate scorecard_v2 files for `05_BACKTEST_RESULTS/enriched_metrics_2026-06-05/scorecard_v2`; snapshot currently links 10 audit rows.
- `app.js` renders Gate 1 Intake, Gate 1B MTC Feasibility, Gate 2 Backtest Evidence, and Gate 3 Production Readiness separately; no blended score; null/non-OK scores display as `N/A`; missing/not-scored fields are visible; missing artifacts have a clean fallback.
- Validation: API py_compile PASS, API tests PASS (`35 passed, 1 subtest`), `node --check app.js` PASS, browser check PASS for one linked scorecard row and one missing-artifact fallback row with no JS console errors.
- Honest state: 38/38 scorecard_v2 are still non-promotable/INCOMPLETE because intake, feasibility, production-readiness, annualized sharpe/sortino, regime, and same-window benchmark fields are not available yet. This is expected and not a UI failure.

## MTC-Engine Validation step (2026-06-04)

### MEV-001 | DONE | MTC-Engine Validation implementation [AI: Claude]
- Implemented additive stage in `02_MTC_BACKTEST`: light-risk profile, manual producer adapter
  scaffold, bridge CLI, Supertrend standalone Pine producer adapter, docs, and tests.
- Entry command: `cd MTC_COMMAND_CENTER/02_MTC_BACKTEST && python -m src.cli.mtc_engine_validate --producer supertrend --data <ohlcv> --symbol <symbol> --timeframe <tf>`.
- Verification 2026-06-04: 4 focused tests PASS, compileall PASS, BTCUSDT 1d real-data smoke PASS.
- `MTC_V2.pine` untouched; `MTCRunner` untouched; parity is producer-level raw-signal only.

### MEV-002A | DONE 2026-06-06 | First real QuantLens Python producer adapter + MTC risk run [AI: Codex]
- Selected `QL_FAM_MOMENTUM_CONTINUATION|TRXUSDT|4h` because it is the strongest current forward-paper cohort and maps cleanly to raw long entries without embedding stop/risk/lifecycle logic.
- Added `QuantLensMomentumContinuationProducerAdapter` under `02_MTC_BACKTEST/src/modules/signals/producers/` and registered aliases `ql_fam_momentum_continuation`, `producer_ql_fam_momentum_continuation`, and `momentum_continuation`.
- Params file: `02_MTC_BACKTEST/configs/producer_params/ql_fam_momentum_continuation_trx_4h.json` (`mom_lb=10`, `trend_ema=50`, `breakout_lb=10`).
- Generated scoped dataset: `02_MTC_BACKTEST/data/mev_validation/TRXUSDT_4h_20240101_RESEARCH.csv` from existing Binance futures 5m research data.
- Real MTC run: `02_MTC_BACKTEST/results/mtc_engine_validation_runs/ql_fam_momentum_continuation_trx_4h_2026-06-06/`; status `COMPLETED`, 51 trades, MTC light-risk stop_loss/take_profit/break_even/multi_tp/trailing enabled, parity `NOT_RUN`.
- Gate3 delta for selected family artifact: 91.0 -> 95.0, still `INCOMPLETE`; all-gate promotable remains 0/9. The run proves adapter/risk-engine compatibility only, not edge quality or promotion.
- Validation: py_compile PASS; producer tests 4 PASS; MEV CLI tests 2 PASS; real MEV run PASS; MEV readiness schema 9/9 valid; score_all_gates promotable=0.

### MEV-002B | DONE 2026-06-06 | Standalone PineTS adapter for real QuantLens producer [AI: Codex]
- Added standalone PineTS adapter `01_MTC_PROJECT/parity_oracles/feature_adapters/pinets/producer_ql_fam_momentum_continuation_v1.pine`.
- Adapter emits raw long/short only and does not touch `MTC_V2.pine`, broker, webhook, or live trading paths.
- Exact same-data parity against Python producer passed on TRXUSDT 4h: 5123/5123 long matches and 5123/5123 short matches.

### MEV-003 | DONE 2026-06-06 | Callable producer-level parity command for bridge reports [AI: Codex]
- Added `02_MTC_BACKTEST/tools/parity/run_quantlens_producer_parity.py`.
- Command runs PineTS, exports `pine_signals.csv`, compares with the Python producer via `compare_signals`, writes `parity_compare.json` and `PARITY_REPORT.md`, and exits nonzero on mismatch.
- `mtc_engine_validate` was rerun with native `--pine-signals-csv`; report now records `parity_status=PASS`.
- Parity-backed readiness set: `03_STATUS/producer_parity_2026-06-06/`; selected TRXUSDT 4h Gate3 score is now 97.0 but still INCOMPLETE; promotable remains 0/9.

### MEV-004 | BLOCKED | Reverse/re-entry/cooldown lifecycle mapping not clean [AI: Claude|Codex|Baris]
- Attempted focused lifecycle proof with MTC engine tests after parity PASS.
- Command result: 16 passed, 5 failed across pending-queue, time-stop EOD/EOW, consecutive-loss reset daily, and max-pyramid config guard tests.
- Evidence note: `03_STATUS/producer_parity_2026-06-06/reverse_reentry_cooldown_mapping.md`.
- Do not mark Gate3 complete until these lifecycle failures are fixed or a narrower approved mapping proof is defined. This may require MTC engine behavior changes and therefore is not safe to patch casually.

## Immediate — Sabah Görevleri (2026-06-03)

### NIGHT-2026-06-03 | DONE | 21-iter overnight sweep + morning report [Claude]
- 21 iter / 0 crash / ~3.6M param-eval. Rapor: `05_BACKTEST_RESULTS/MORNING_REPORT.md`.
- 149 robust PASS, 89 beat b&h, 8 down-market alpha — hepsi DSR p<0.50 (kanıtsız).

### NIGHT-FOLLOWUP-001 | OPEN | Down-market 8 adayı forward-paper-trade [Barış onayı]
- APT/ADA/LINK 1h hücreleri en güçlü. Live-bar OOS topla, parity öncesi izle.
- Kaynak: `05_BACKTEST_RESULTS/alpha_summary.json` (down_market_alpha).

### NIGHT-FOLLOWUP-002 | OPEN | DSR ~0 kök neden: search-space inflation [AI: Claude|DeepSeek]
- Tüm adaylar DSR'da çakılıyor. Dar pre-registered hipotez grid'i ile confirmation-only run (küçük family → yüksek DSR gücü).

### NIGHT-FOLLOWUP-003 | DONE | generate_morning_report.py legacy hardcoded OUTPUT_DIR fix [AI: Claude]
- Hâlâ `C:\LAB\tradingview-lab\...` okuyordu (A1). Rapor elle üretildi. `hardcoded_path_rewrite_TODO`'ya bağlıydı.
- Fix (2026-06-05 Claude): replaced the hardcoded legacy path with env-overridable repo-relative default mirroring `mega_walk_forward.py` — `MEGA_OUTPUT_DIR` env else `Path(__file__).parent.parent/"05_BACKTEST_RESULTS"`; added `import os`. Verified: py_compile PASS; default resolves to `03_QUANTLENS/05_BACKTEST_RESULTS` (no `tradingview-lab`); env override honored. Not committed.

### MORNING-001 | OPEN | Buy&Hold baseline güncelle [AI veya Barış]
- Aggregate tamamlandı: 16 iter, 149 robust winner (≥8/16).
- Çalıştır: `python buy_hold_baseline.py --sprint-dir sprint_runs`
- Amaç: TRXUSDT (+107%) / XRPUSDT (+124%) bull market etkisini filtrele, net alpha gör.

### MORNING-002 | OPEN | Promotion assessment güncelle [Barış onayı]
- Mevcut assessment 2026-06-01 tarihli, sadece 13 iter bazlı.
- 149 robust cell ile ADAUSDT/LINKUSDT/SOLUSDT stratejiler ELITE adayı.
- Güncelle: `sprint_runs/PROMOTION_ASSESSMENT_2026-06-01.md`
- Önerilen ELITE onaylar: `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY/TRXUSDT/2h`, `QL_DEEPAK_153_FILTER_1D/SOLUSDT/2h`

### MORNING-003 | OPEN | Transcript manual review [Barış — 31 aday]
- 31 aday bekliyor: 17 LIKELY_MISCLASSIFIED + 14 REVIEW_HUMAN
- Dosya: `11_TRIAGE/reclassification_audit_2026-06-01.md`

---

## Strategy Research Lab (infra eklendi 2026-06-03)

### RESEARCH-001 | REVIEWED — BLOCKED (stale as written), do NOT mass-move [AI: Claude → Barış]
- Reviewed 2026-06-05 (Claude). The literal task is unsafe/obsolete as written:
  1. **`03_SALVAGE_IDEAS/` is now LIVE reader data** — `mcc_readonly/quantlens_reader.py` (SP-005 Wave B) parses those candidate dirs into the dashboard. Moving them WOULD BREAK the QuantLens Verdict card. Exclude from any move.
  2. **`route_user_intake.py` targets a different inbox** (`00_INBOX/USER_INTAKE`, currently EMPTY — dry-run "nothing to route"), NOT `00_INBOX_REPORTS/`.
  3. **`00_INBOX_REPORTS/` = 206 files in Turkish date-folders** (`1 Haziran`, `3 Mayıs`, `Transcrips`). Mapping each to one of 63 STG strategies needs per-file content judgment; auto-token-matching risks misfiling 206 files.
- **Recommendation:** do NOT auto-move. If consolidation is wanted: (a) leave `03_SALVAGE_IDEAS` in place; (b) review `00_INBOX_REPORTS` in small human-confirmed batches, routing only files whose target STG is unambiguous; (c) extend `route_user_intake.py` to accept `00_INBOX_REPORTS` as a source only after a dry-run confirms matches. Left for Barış to greenlight a batch.

### RESEARCH-003 | DONE | Full indicator inventory from MTC_V2.pine [AI: Claude]
- Done 2026-06-05 (Claude), read-only. Extracted the MTC_V2 indicator set from `01_MTC_PROJECT/01_PINE/MTC_V2.pine` (2079 lines) via `ta.*` primitives + plot/variable titles — WITHOUT modifying the `.pine` and without ingesting the full 128K (token-efficient). Output: `05_REGISTRY/MTC_V2_INDICATOR_INVENTORY.md`.
- Inventory: Supertrend (signal producer), MACD (+regime/cross/zero-dist/HTF variants), ADX/DMI, ATR (stops/targets/vol-floor), MA filter, MA slope, **McGinley Dynamic (new)**, **Choppiness (new)**, Donchian/Highest-Lowest, EMA/SMA/WMA/RMA, HTF trend/MACD, barssince. McGinley + Choppiness are the likely gaps vs the current 27-entry seed.
- **Did NOT hand-edit `INDICATOR_REGISTRY.json`** (AGENTS.md: it is generator-produced). The inventory is a reference to feed the generator's curated seed when desired. Full per-gate semantic map (exact lengths/sources/conditions) deferred — needs a dedicated heavy `.pine` read.

### RESEARCH-002 | OPEN | Classification review for review_needed fields [AI: Claude|Barış]
- 63 strategies have at least one `review_needed` placeholder after the 2026-06-04 re-triage refresh.
- Edit each `STGxxx/01_candidate_metadata.yaml` / `producer_spec.json`, then
  re-run `python 03_QUANTLENS/tools/build_strategy_research_registry.py`.
- Track via **Strategy Research Lab → Missing Metadata** tab.

### RESEARCH-003 | OPEN | Full indicator inventory from MTC_V2.pine [AI: Claude]
- INDICATOR_REGISTRY.json is seeded from strategy references + curated list.
- Extract the complete MTC_V2 indicator set (read-only; do NOT modify the .pine).

### RESEARCH-004 | DONE | Re-triage transcript-now-present candidates [AI: Claude — batched]
- Completed 2026-06-04 by Codex. Ledger: `11_TRIAGE/retriage_progress.json` now shows `done=87 pending=0 next_stg=STG064`; plus pilot entries `Stg082`, `Stg083`, `Stg087` = all 90 eligible candidates accounted for.
- Final dispositions log: `11_TRIAGE/retriage_dispositions_2026-06-04.md`.
- New/updated matured strategy folders from final batch:
  - `STG061_ryan_pierpont_breakout_discipline` repaired with spec + source intake for Stg154-Stg158.
  - `STG062_stan_weinstein_stage_analysis` created for Stg160-Stg166.
  - `STG063_tito_options_aware_rs_breakout` created for Stg167-Stg169 and marked `needs_manual_review`.
  - Stg170, Stg171, Stg172 marked duplicates and transcripts attached to existing STG032, STG022, STG056.
- Validation after refresh: `build_strategy_research_registry.py` wrote 63 strategies / 27 indicators / 78 components; `--check` PASS; `validate_research_registries.py` PASS; `build_triage_registry.py` PASS; `node --check app.js` PASS; dashboard API tests `35 passed` with `PYTHONPATH` set; snapshot `strategy_research` includes STG061-STG063.
- Pilot batch (3 HIGH) done 2026-06-04, review-first. Dispositions: `11_TRIAGE/retriage_dispositions_2026-06-04.md`.
  - Stg083 -> CANDIDATE -> created `03_QUANTLENS/strategies/STG047_brian_lee_smallcap_gap_mr_short`.
  - Stg082 -> WIKI_ONLY (Ted Zhang momentum podcast). Stg087 -> DUPLICATE (8EMA exit; overlaps STG002/042/043).
- Finding: top HIGH candidates are interview/educational -> expect WIKI/SALVAGE/DUPLICATE for most; far fewer than 90 new strategies.
- 172 triage worklist now reconciled with on-disk transcripts: 159 have transcripts,
  **90 eligible** (87 HIGH + 3 MEDIUM) — previously rejected only for missing transcript.
- Worklist: `11_TRIAGE/retriage_worklist_2026-06-04.md`. Live registry:
  `05_REGISTRY/TRIAGE_CANDIDATE_REGISTRY.json` (regen `build_triage_registry.py`).
- Visible in **Strategy Research Lab → Triage Worklist** tab.

### RESEARCH-005 | OPEN | Manual review STG063 options-aware proxy assumptions [AI: Claude|Barış]
- `STG063_tito_options_aware_rs_breakout` is a partial deterministic spec. Decide whether to keep it as manual options-aware research or build a stock-only proxy with explicit caveats.
- Do not backtest options returns from stock-only data.

---

## Completed Sprint (2026-06-01 — overnight)
- T-01 Buy&Hold baseline: DONE (117→ şimdi 149 robust, güncelleme gerekli)
- T-02 CPCV + PBO gate: DONE
- T-03 Promotion assessment: DONE (güncelleme gerekli — MORNING-002)
- T-04 MEGA overnight loop: DONE (16 iter, tamamlandı 06:33 yerel)
- T-05 QQE smoke test: DONE (FILTER_OVERLAY — overfitting, kaydedildi)
- T-07 SP-001 MVP-0 CLI: DONE (`mtc_cli/`, 8 test PASS)
- T-08 SP-002 vectorbt enrichment: DONE (`vbt_enrichment.py`, smoke PASS)

## Active (2026-06-01 — overnight workflow consolidation aftermath)

### IM-001 | DONE | analyze_transcripts.py path-resolution fix + basename fallback
- Completed 2026-06-01 by Codex (initial). Verified + basename fallback added by DeepSeek V4 Pro 2026-06-01.
- 165/165 transcripts now resolved and analyzed. 67 had legacy `06_QUANTLENS_LAB\` prefix → basename fallback finds them in `03_QUANTLENS/00_INBOX_REPORTS/Transcrips/`.
- Audit results: 115 ALREADY_OK, 17 LIKELY_MISCLASSIFIED, 14 REVIEW_HUMAN, 19 KEEP_REJECTED, 0 SPLIT_RECOMMENDED.
- 17 + 14 = 31 candidates need Barış manual review. See `11_TRIAGE/reclassification_audit_2026-06-01.md`. [AI: Barış]

### IM-002 | DONE | OUTPUT_DIR / hardcoded path audit script
- Completed 2026-06-01 by Codex. Added `03_QUANTLENS/tools/audit_hardcoded_paths.py`; pre-commit hook calls staged audit. Full default scan currently reports 2,488 existing legacy references.
- `tools/audit_hardcoded_paths.py` yaz — repo'da `C:\LAB\tradingview-lab\` veya benzeri legacy işaretleri grep'le, listele.
- CI/precommit hook'a ekle.
- Mevcut bilinen: `mega_walk_forward.py:32-36` (DATA_BUNDLE_PATH hala legacy işaret ediyor — `MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427` yolu).

### IM-003 | DONE | mega_walk_forward resumable iter
- Completed 2026-06-01 by Codex. `mega_walk_forward.py` supports `--resume`, periodic checkpoint pickle, partial JSON, completed-job skip, and atomic final JSON replace. Verification used synthetic checkpoint helpers; full engine run not executed.
- Crash sonrası iter baştan başlıyor; %94 hesap kayıp.
- `--resume <pickle>` arg ekle. Her N iter'de pickled checkpoint.
- Atomik temp-rename ile partial JSON.

### IM-004 | DONE | Heartbeat in-iter granularity
- Completed 2026-06-01 by Codex. Mega now refreshes heartbeat during in-iteration progress events using `MEGA_HEARTBEAT_*`; loop scripts export context. Verification: Python helper PASS; bash syntax check unavailable.
- Mevcut: heartbeat sadece iter-arası. 75dk sessizlik mümkün.
- Mega'nın `[N/total] elapsed=Xs counts=...` her dakika print'ini parse et, heartbeat dakikalık güncelle.
- Monitor script anomaly threshold için bu lazım.

### IM-005 | DONE | Windows taskschd kurulum
- Completed 2026-06-01 by Codex. `MCC_Overnight_Monitor` scheduled task registered successfully; state `Ready`.
- `tools/register_overnight_monitor.ps1` admin PS ile TEK SEFER çalıştır.
- Çift kanal (taskschd + wakeup) — wakeup tek mekanizma riski yeniden yaşanmasın.

### IM-006 | DONE | CPCV (Combinatorial Purged Cross-Validation)
- Completed 2026-06-01 by Codex. Added `cpcv_validator.py` and rules CPCV Gate. Smoke report: `03_QUANTLENS/tools/cpcv_runs/smoke/CPCV_VALIDATION_REPORT.md`.
- Mevcut 4-gate'e **5. gate** olarak eklenecek.
- Rolling WF + lockbox bağımlı fold'lar yaratıyor; CPCV tüm `(N choose k)` train/test ayrımlarını test eder.
- Embargo + purge (overlap silme) lookahead riskini sıfırlar.
- Referans: López de Prado, "Advances in Financial Machine Learning" Ch.12
- Hedef: `03_QUANTLENS/tools/cpcv_validator.py` — mevcut `mega_walk_forward.py` `_worker` çıktısını alıp CPCV yeniden çalıştırır
- Rules dosyası §8'e "CPCV Gate" satırı eklenecek

### IM-007 | DONE | Probabilistic OOS / PBO
- Completed 2026-06-01 by Codex. Added `probabilistic_pbo.py` and PBO Gate. Smoke report: `03_QUANTLENS/tools/pbo_runs/smoke/PBO_REPORT.md`.
- Mevcut bootstrap_p_positive zaten Probabilistic Sharpe Ratio'nun bir formu
- **Probabilistic Backtest Overfitting (PBO)** ekle — combinatorically symmetric cross-validation
- DSR + PBO birlikte → en katı statistical layer
- Hedef: `tools/probabilistic_pbo.py`

### IM-008 | DONE | In-day single strategy hizli akis scripti
- Completed 2026-06-01 by Codex. Added `single_strategy_backtest.py`; MEGA supports `--strategy/--symbol/--tf`. Smoke output: `03_QUANTLENS/tools/single_strategy_runs/smoke_IM008/`.
- `tools/single_strategy_backtest.py <strategy_id> <symbol> <tf>`
- Tek komut → veri validation + sandbox WF + 4-gate + buy&hold + morning_report
- "1 strateji 5dk" akışı 4-gate atlanmadan otomatik
- Rules §2'deki "Standard Backtest Workflow" 10 adımını sırayla çalıştırır

### IM-009 | DONE | data_check module
- Completed 2026-06-01 by Codex. Added `data_check.py` and wired `single_strategy_backtest.py` to it. Smoke output: `03_QUANTLENS/tools/single_strategy_runs/smoke_IM009/`.
- `tools/data_check.py` — `verify_actual_range(symbol, tf)` API
- Rules §3 "Mandatory Data Validation Rules" first-class destek
- Cache disk içeriği (parquet/csv) ilk/son timestamp ve bar count
- Yanlış manifest claim'lerine karşı tek-doğru-kaynak

## Waiting On
- (none)

## Audit Backlog — LLM Code Review Findings (2026-06-02)

Aşağıdakiler ChatGPT 5.5 / DeepSeek V4 Pro audit'inden çıkan, henüz fix edilmemiş bulgular.
Her item yanında hangi modelin yapması uygun yazıyor.

### AUDIT-001 | DONE | ADX yön hatası [AI: DeepSeek — 1 satır fix]
- `overnight_v2_runner.py:594` — `QL_QTREND_V2_STRONG_ADX` strateji `adx_14 < adx_threshold` kullanıyor.
- Strateji ismi "STRONG ADX" → yüksek ADX (trend) demek; ama kod düşük ADX'de giriyor.
- **KARAR (Barış 2026-06-04, D004): strong-trend intent → `>=`.** İsim aynı kalır (zaten `strong_buy` gate ile tutarlı).
- Fix (2026-06-04 DeepSeek): `adx_14 < ...` → `adx_14 >= ...`. py_compile PASS, line 594 verified.

### AUDIT-002 | DONE | CPCV 3-tuple short strategy desteği [AI: DeepSeek]
- `cpcv_validator.py:86` — CPCV `build_signals()` her zaman 2-tuple varsayıyor.
- `QL_QTREND_V1_SHORT` 3-tuple döndürüyor → crash veya yanlış direction.
- Fix (2026-06-04 DeepSeek): canonical 3-tuple parse from mega_walk_forward.py:654-658; `evaluate_split` gets `direction` param → `simulate_slice`; validated via CPCV smoke.

### AUDIT-003 | DONE | rigorous_walk_forward.py short desteği yok [AI: DeepSeek]
- `rigorous_walk_forward.py:266` ve `rigorous_walk_forward_parallel.py:254` — `simulate_slice` `direction` parametresi yok.
- Short strategy feed edilirse sıfır trade / NaN sonuç üretir sessizce.
- Fix: `mega_walk_forward.py:simulate_slice` ile aynı short branch'i ekle (direction param + is_short logic).
- Fix (2026-06-04 DeepSeek): added `direction="long"` default + 3-tuple-safe `build_signals` parsing to both rigorous walk-forward tools; ported mega short branch with short stop above entry, target below entry, no short trailing-EMA exit, `raw=entry/exit-1`, and short R `(entry-exit)/risk`. Verified py_compile PASS, long 2-tuple regression byte-identical, synthetic short smoke PASS for both iat and numpy loops.

### AUDIT-004 | DONE | BUNDLE_MANIFEST env override yok [AI: DeepSeek]
- `mega_walk_forward.py:35-38` — `BUNDLE_MANIFEST` hardcoded arşiv path, `MEGA_OUTPUT_DIR` gibi env override yok.
- Fix (2026-06-04 DeepSeek): `MEGA_BUNDLE_MANIFEST` env var with legacy fallback; env override + fallback both verified.

### AUDIT-005 | DONE | PBO asimetrik CSCV split sorunu [AI: DeepSeek]
- `probabilistic_pbo.py:54` — default CPCV 15 sütun emit eder (tek sayı), PBO `n_splits // 2` ile 7/8 asimetrik partition oluşturur.
- Fix (2026-06-04 DeepSeek): `usable = n_splits_available - (n_splits_available % 2)` → even splits; dropped column tracked via `splits_used`/`splits_available`/`partition_note`; validated 15→14 even split, pbo=0.102564.

### AUDIT-006 | DONE | rolling_fold_indices min bars guard [AI: DeepSeek]
- `mega_walk_forward.py:590` — `span_end < 1000` guard. 1000 bar altı dataset (yüksek TF, kısa tarih) sessizce `[]` döner; cell test edilmeden skip.
- Fix (2026-06-04 DeepSeek): added `fold_feasibility(n_bars)` sibling helper (mirrors rolling_fold_indices guards), `warnings.warn` + `INSUFFICIENT_DATA` classification in `_worker` after MIN_BARS_REQUIRED. Verified fold_feasibility(500)→(False,...), (50000)→(True,""). Did not change fold math/step/overlap.

### AUDIT-008 | DONE | Rolling fold OOS window overlap [AI: DeepSeek/Claude]
- `mega_walk_forward.py:604` — `step = remaining//(NUM_FOLDS-1)` = 0.10·span = half of test_size → structural 50% OOS overlap; `folds_positive` inflated.
- **KARAR (Barış 2026-06-04, D006): disjoint OOS — `step = test_size`** + PASS tightened to `pos == n_folds`.
- Fix (2026-06-04 DeepSeek Batch D): line 604 `step = test_size`; line 732 PASS elif `pos >= ceil(n_folds/2)` → `pos == n_folds` (STRONG inner unchanged). Claude-audited: py_compile PASS; disjoint verified n=1500/6000/50000/100000 (always 2 folds, prev OOS ke == next ks, 0 overlap); n<1000-span → []. No lockbox/CPCV/PBO change.
- **OPEN op (Barış, not code): re-run existing sweep** — 149 robust-PASS (DSR-unconfirmed) were computed under old overlapping geometry; must re-run under disjoint folds + `pos==n_folds` before DSR-lock.

### AUDIT-007 | DONE | paths.py empty dir silent select [AI: DeepSeek/Claude]
- `paths.py:30` — `03_QUANTLENS` boş olsa da ilk `exists()` match seçiliyor.
- Fix (2026-06-04 DeepSeek Batch C): `default_quantlens_root` artık non-empty dir tercih ediyor (`any(c.iterdir())`, OSError-skip), fallback first-existing→candidates[0]. registry_reader + audit_reader inherit. Claude-audited: py_compile + 5/5 mock selection cases (a-e) PASS.

### AUDIT-009 | DONE | bars_per_day=78 crypto'ya yanlış [AI: DeepSeek/Claude]
- Fix (2026-06-04 DeepSeek Batch E): mega `EQUITY_ONLY_STRATEGIES` set (empty default) + `EQUITY_EXCHANGES={NYSE,NASDAQ,ARCA,AMEX,BATS}`; gate in `_worker` after find_ds → `SKIPPED_RULE` if strategy equity-only AND `ds.exchange` not equity. `overnight_v2_runner` registers the 4 OR strategies. Data is 100% Binance crypto → all 4 skip now; auto-run if US-equity data added. Claude-audited: py_compile PASS, end-to-end `_worker(GAP_5M,BTCUSDT,15m)`→SKIPPED_RULE(exchange=BINANCE), no over-skip (NASDAQ would run), pure-mega unaffected (empty set). bars_per_day=78 unchanged (correct for equity).
- `overnight_v2_runner.py:418,447,474,506,509` — `bars_per_day = 78` hardcoded (US equity 5m session = 6.5h).
- Etkilenen 4 OR stratejisi: QL_CONNELL_EVENT_DRIVEN_GAP_5M, QL_AVWAP_BRIAN_INTRADAY_OR_5M, QL_EPISODIC_PIVOT_CHRISTIAN_5M, QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M.
- Crypto 24/7 → session open yok. `bar_idx % 78` her 24h crypto gününün ilk 78 barını yanlışlıkla "opening range" etiketliyor.
- **KARAR (Barış 2026-06-04, D005): US-equity-session-only.** `bars_per_day=78` doğru, crypto'ya GENELLEŞTİRME. Crypto/24-7 data'da bu 4 strateji skip + `INSUFFICIENT_DATA`/`N_A` not ile (opening-range session open olmadan anlamsız). Symbol-aware/288 YOK.
- Fix: 4 OR stratejisini US-equity sembol/session'a gate et; crypto feed'de signal üretme, explicit skip-reason döndür.
- Doğrulandı: kod incelendi 2026-06-02 (Mimo v2.5 audit Run 7,11 — gerçek bulgu).

### AUDIT-010 | DONE | ingest.py transcript re-write race [AI: DeepSeek/Claude]
- `ingest.py:249-251` — `if not target.exists() or sha != state_sha:` dış koşul, ama iç `if not target.exists():` sadece yeni dosya append ediyor.
- Bug: dosya VAR + içerik DEĞİŞTİ (sha farklı) durumunda → dış koşul True, iç koşul False → **dosya hiç güncellenmiyor**, sadece `transcript_main_sha` state set ediliyor.
- Fix (2026-06-04 DeepSeek Batch C): iç guard kaldırıldı; `new_transcripts.append(...)` dış koşul altında koşulsuz çalışıyor → sha-mismatch overwrite queue ediyor. Writer (L341 `target.write_text`) koşulsuz overwrite — safe. Claude-audited: py_compile + on-disk read confirm, surroundings untouched.

## Side Projects (parked — pick up when ready)

### SP-005 | Strategy Detail Page Redesign (trading-review dashboard) [AI: Claude lead + Barış]
Status: plan v3 ready, not started. Proposed 2026-06-02, revised 2026-06-03 (v2→v3).
Trigger: Barış flagged the strategy-detail page as confusing/too technical.
**Direction LOCKED: terminal** (`proto_B2_terminal.html`; single-scroll; A/clinical/
editorial dropped). v3 structural rules: (1) ONE scoring system = Scorecard;
QuantLens = commentary that references it, no double scoring. (2) Verdict & Decision
MERGED into one top block. (3) Scorecard directly under verdict, click-to-expand
gates. (4) Backtest = TradingView-tester-style CASES (video-settings + optimized
best, each w/ settings·symbol·timeframe on one standard window). (5) Stage prototypes
built (rules-extracted/testability/backtested/promotion). Prototypes + shared
`proto_terminal.css` in `08_DASHBOARD_APP/apps/web/prototypes/`.

Problem: current page (`08_DASHBOARD_APP/apps/web/app.js:389` `renderUnifiedStrategyDetail`)
is a debug dump — raw ID as title, two dense parallel tables, one misleading
`57/100` headline, bare machine terms. Raw decision sentence from
`mtc_v2_reader.py:217` (interpolates raw ID + raw status).

Fix: single-scroll trading-review dashboard — English-only UI, human name +
translated-to-English description, sticky mini-summary, decision summary,
**QuantLens Verdict** (ruthless audit layer), **Strategy Taxonomy** chips,
review-journey stepper, expanded trading rules, 4 gate bars, honest backtest
evidence, **Salvageable Ideas** (mandatory), debug collapsed into Technical.

KEY FINDING (2026-06-03): QuantLens is **already a real pipeline** —
`03_QUANTLENS/03_SALVAGE_IDEAS/<candidate>/` has 7 artifacts each;
`01_candidate_metadata.yaml` already carries `quantlens_decision`,
`commercial_value_score`, `complexity_score`, `repaint_risk`, `lookahead_risk`,
`closed_source_risk`, `candidate_kind` (salvage categories), `market_type`,
`recommended_next_step`. Dashboard readers **ignore these today**. QuantLens
Verdict section surfaces existing data via a new read-only `quantlens_reader.py`.

**Full plan:** `03_QUANTLENS/_user_guide/11_STRATEGY_DETAIL_PAGE_REDESIGN_PLAN.md` (v3)
**Prototypes (DONE, approved 2026-06-03):** `08_DASHBOARD_APP/apps/web/prototypes/` —
terminal set: `proto_B2_terminal.html` (blocked), `proto_stage_rules_extracted.html`,
`proto_stage_testability.html`, `proto_stage_backtested.html`, `proto_stage_promotion.html`.
English-only, single-scroll, CSS inlined.
**Depends on:** SP-004 (scoring) for Wave C gate bars.
**NEXT: awaiting Barış go-ahead to start Wave A coding (not yet authorized).**

Three waves:
- Wave A — single-scroll UI/wording/layout on EXISTING data: `ui_labels` map,
  decision-object refactor (ID-free), header + sticky summary + decision summary,
  taxonomy shell, review-journey stepper, trading-rules card ("Not defined yet"),
  Technical `<details>`, source slim-down, responsive CSS. [Claude/Any]
- Wave B — QuantLens structured data: new `quantlens_reader.py` (parses salvage
  YAML/markdown), QuantLens Verdict card, Salvageable Ideas section, conditional
  render matrix (garbage/closed-source/complexity stops), repaint/lookahead/
  marketing/unverified-claim warnings, commercial-value + testability +
  evidence-level + documented-vs-proven derivations. Schema add for
  CLOSED_SOURCE_STOP/COMPLEXITY_OVERLOAD + structured `salvageable_ideas[]`. [Claude]
- Wave C — `scorecard_v2` (SP-004 P2) gate bars + N/A + backtest-evidence visuals
  (equity, metrics, B&H, source-claim-vs-result) + filter migration. [Claude]

Files: `apps/web/{app.js,index.html,styles.css}`, `mtc_v2_reader.py` (decision
object), new `mcc_readonly/ui_labels.py`, new `mcc_readonly/quantlens_reader.py`,
`audit_reader.py` (join verdict to row). No scoring math here (consumes
`scorecard_v2`). Constraint: presentation + read-only QuantLens reader — no live
trading, no Pine/parity/pipeline change, audit data moved not deleted.

Barış decisions (2026-06-03, all = plan's recommended): QuantLens above Taxonomy;
AI-generated names (editable); provisional commercial-value bands; **ship Wave A
first**; closed-source → still show independent sub-ideas; derive stop-states (no
YAML schema change now). No open questions. Awaiting go-ahead to start Wave A
(not yet authorized).

### SP-004 | Strategy Scorecard Redesign (gate-based, edge-weighted) [AI: Claude lead + DeepSeek + Barış]
Status: **P0A+D1-D6 signed; P1A/P1/P2 DONE; Gate scorers DONE; Gate2 final metrics DONE; all possible Gate1/Gate1B evidence emitted for final run; dashboard-visible scorecard_v2 refreshed. Next: real Gate3 production-readiness evidence source + Baris promotion policy.**
Proposed 2026-06-02.
Trigger: when ready to fix the strategy-detail score Barış flagged as
"yetersiz ve hatalı".

**P0A delivered (spec only, no code, no Pine/MTC/parity change):**
- Canonical rubric `03_QUANTLENS/_user_guide/12_STRATEGY_EVALUATION_RUBRIC.md`
  (English; Gate2 rebalanced Regime 5→10 / Perf 20→18 / Sample 15→12; added
  Sharpe/Sortino/recovery/WFO/CPCV/PBO as Gate2 metrics; Gate1B /50+derived PASS;
  Gate1B-vs-Gate3 de-dup; parity hard gate; SAFE_WITH_DELAY −3 / NEEDS_MODIFICATION
  block; PBO≥0.5→OVERFIT_SUSPECT; field map per sub-criterion).
- Schemas `06_SCHEMAS/{status_envelope, evaluation_artifact_v1,
  production_readiness_artifact_v1}.schema.json` (validated: meta-schema + $ref +
  sample instance + negative case all pass).
- Template `03_QUANTLENS/_templates/strategy_evaluation_record_template.yaml`.
- **Barış must approve D1-D6** (rubric §"Owner decisions") before P2 scoring locks:
  D1 Gate1B mode, D2 PBO policy, D3 parity gate, D4 Gate3 separate artifact,
  D5 bands (set in P1.5), D6 thesis-title author. Draft uses recommended defaults.

Problem: current `build_scorecard()` (`08_DASHBOARD_APP/apps/api/mcc_readonly/presentation_reader.py:65`)
is one flat 100-blend that measures **pipeline progress, not edge** — 25/35
backtest points are pure stage maturity, return/PF are risk-blind, no drawdown /
Sharpe / benchmark / OOS / PBO / repaint hard-fail.

Fix: replace single composite with 4 separate gates + hard-fail flags
(Gate1 intake /100, Gate1B feasibility /50, repaint pass/fail, Gate2 backtest
/100 risk-adjusted, Gate3 production /100). Never recollapse to one number.
~Half the Gate2 inputs (WFO/CPCV/PBO/B&H) already computed by overnight tooling.

**Full plan:** `03_QUANTLENS/_user_guide/10_STRATEGY_SCORECARD_REDESIGN_PLAN.md`
**Source rubric (DELETE when done):** `11_TRIAGE/_eval_pipeline_source_TEMP/`

Phases (~8–10 days, order revised after 2 LLM audits — see plan §9):
- P0A rubric mapping + 2 JSON schemas (eval + production_readiness) + template
  fields (thesis_en, hard-fail reasons, run_id, phase_current) [Claude → Barış] — **DONE 2026-06-04, awaiting sign-off**
- P1A fix CPCV 3-tuple (AUDIT-002) + PBO split (AUDIT-005) + N_A fallback
  BEFORE hard-gating [DeepSeek] — **DONE 2026-06-04**
- P1 emit `evaluation_artifact_v1` w/ status envelope on 5–10 strategies [Claude/DeepSeek]
- P1.5 finalize numeric bands FROM real distributions, not guessed [Claude → Barış]
- P2 gate scoring engine → `scorecard_v2` (parallel to legacy) + golden tests [Claude, cross-model review]
- P3 dashboard: thesis title + gate bars + migrate filters to gate-status [Claude/Any]
- P4 backfill w/ completeness check + ranking validation [DeepSeek + Barış]
- P5 cleanup: legacy flag removal + **delete TEMP** (only now) [Claude]

Open for Barış (plan §8): numeric bands (set in P1.5), trade-count minimums,
PBO≥0.5→OVERFIT_SUSPECT?, AI-vs-human thesis title, Gate1B /50-vs-PASS,
Gate3 separate production artifact.
Constraint: read-only on trading/Pine/parity — only adds output writer + scoring + UI.

### SP-003 | Python Live Trading Engine (Pine Script bypass) [AI: Claude]
Status: planned, not started. Proposed 2026-06-01.

**Sistem Özeti:**
Mevcut MTC pipeline (backtest → optimizasyon → sinyal) çıktısını doğrudan
Binance'e bağlayan, TradingView/Pine Script bağımlılığını kaldıran tam otonom
canlı trade altyapısı.

**Mimari:**
```
mega_walk_forward.py        → optimal parametre çıktısı
      ↓
signal_generator.py         → BUY/SELL/HOLD sinyali (mevcut strateji mantığı)
      ↓
binance_executor.py         → ccxt ile Binance API order
      ↓
VPS (Hetzner/DigitalOcean)  → 7/24 çalışır, bilgisayardan bağımsız
```

**Neden Pine Script'e gerek kalmaz:**
- Pine Script sadece görsel + alert üretir; trade execution yok
- ccxt kütüphanesi 100+ exchange destekler, Binance tam uyumlu
- Python: backtest + sinyal + execution tek yerde → debug kolaylığı
- ML entegrasyonu, CPCV, PBO gibi mevcut katmanlar doğrudan bağlanabilir

**Teknik Bileşenler:**
- `ccxt` → Binance Spot / USD-M Futures / COIN-M Futures API
- Binance Testnet → gerçek para olmadan tam test (`set_sandbox_mode(True)`)
- `systemd` service veya `nohup` → VPS'te arka plan çalışma
- Position sizing → risk per trade sabit ($, % veya ATR bazlı)
- Stop-loss / take-profit → `create_order` ile OCO order

**VPS Gereksinimi:**
- Minimum: 1 CPU, 1GB RAM → Hetzner CX11 (~4€/ay)
- Lokasyon: Frankfurt veya Tokyo (Binance sunuculara düşük latency)
- Scalping varsa lokasyon kritik; swing/daily için fark yok

**Scope:**
- Yeni klasör: `MTC_COMMAND_CENTER/05_LIVE_ENGINE/` (önerilir)
- `binance_executor.py` — order yönetimi, rate limit handling
- `signal_bridge.py` — mevcut backtest çıktısını live sinyale dönüştürür
- `risk_manager.py` — position sizing, max drawdown kill switch
- `monitor_live.py` — açık pozisyon takip, heartbeat log

**Kritik Riskler:**
- Backtest → live performans farkı (slippage, funding rate, latency)
- API key güvenliği → .env, IP whitelist zorunlu
- Kill switch eksikliği → runaway loss riski
- Pine Script'te olan görsel analiz burada yok → TV charts korunabilir

**TradingView korunabilir mi:**
- Evet. TV sadece görsel analiz + chart için tutulabilir
- Sinyal ve execution Python'a taşınır
- Hibrit mimari mümkün: TV chart → alert → Python webhook → ccxt order

**Pickup trigger:**
- Backtest pipeline stabil ve tutarlı OOS sonuç ürettiğinde
- En az 3 ay paper trading (testnet) başarısı sonrası canlıya geçiş

**Out of scope (bu SP altında yapılmaz):**
- Pine Script veya MTC_V2.pine değişikliği
- Mevcut backtest/WF/CPCV pipeline değişikliği
- High-frequency / scalping (swing/daily ile başla)
- Multi-exchange (sadece Binance ile başla)

### SP-002 | vectorbt analytics layer (post-processing enrichment) [AI: Claude|DeepSeek]
Status: planned, not started. Proposed 2026-06-01.
Goal: wire vectorbt as post-processing layer on top of TradingView trade data.
`data_get_trades` MCP → `vbt.Portfolio.from_orders()` → richer metrics (Calmar,
Sortino, Omega, rolling Sharpe, underwater equity curve, Monte Carlo) not
natively available in TV. Does NOT replace Pine strategies or MCP tooling.
Optionally: validate/replace `cpcv_validator.py` with vectorbt's built-in CPCV.

Scope: new helper `03_QUANTLENS/tools/vbt_enrichment.py` only.
No Pine / MTC / parity edits. No replacement of `mega_walk_forward.py`.
Pre-req: `pip install vectorbt` (or `vectorbt-pro` if available).

Acceptance:
- Takes a list of TV trade dicts (from `data_get_trades`) + price series
- Returns enriched stats dict + optional HTML report
- Integrates as optional post-step in `single_strategy_backtest.py`

Pickup trigger: whenever a sprint or single-strategy result needs deeper
analytics than the current 4-gate pipeline provides.

### SP-001 | Internal CLI layer + dashboard buttons (`mtc_cli/`) [AI: Claude]
Status: planned, not started. Approved 2026-05-31 by Barış.
Goal: agent-native CLI surface + 1:1 dashboard buttons so any AI model (and
Barış) can drive recurring workflows without memorizing commands or scanning
the repo. Cuts next-session context cost. Wraps existing scripts + MCP — no
replacement of `MTC_V2.pine`, parity logic, or TradingView MCP tools.

Decision reference: `DECISIONS.md` D002 (adopt internal CLI; reject CLI-Anything).

Hard constraint: at scaffold time, re-read all `_AI_MEMORY/` anchors,
`AGENTS.md`, `AI_RULES.md`, `DO_NOT_TOUCH.md`, run `git status` +
`git log --oneline -20`, diff intent vs reality, surface drift to Barış,
**no write until approval**. Treat plan below as intent, not contract.

Must obey 7-gate workflow (AI_RULES.md). Start at Gate 1.

#### MVP-0 — CLI skeleton + read-only audit (~1 evening)
- Whitelist (declare in G1): new folder `mtc_cli/` only.
- Deliverables: `mtc_cli/__main__.py`, `mtc_cli/contract.py` (envelope,
  exit codes, error categories), `mtc_cli/commands/audit.py`,
  `mtc_cli/tests/`.
- Command: `python -m mtc_cli audit repo [--json]` — read-only snapshot.
- Acceptance: valid JSON envelope, exit 0 on clean repo, exit 2 on missing
  memory file fixture, byte-stable on unchanged repo.
- Touches Pine / MTC / parity: **no**. Skip explicit Barış approval gate.
- Gates: G1 → G2 → G3 → G4 → G5 (reviewer must be Codex or Gemini, not
  Claude) → G6 (subprocess + file IO surface = required) → G7.

#### MVP-0.5 — One dashboard button (~1 evening)
- Whitelist: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/` only.
- Deliverable: minimal page with "Audit Repo" button calling the CLI via
  existing API. Tooltip = one-line explanation.
- Acceptance: click → JSON envelope rendered to screen, no business logic
  in dashboard (thin wrapper only).
- Reuses existing `08_DASHBOARD_APP/apps/api` pattern. No new app.

#### MVP-1 — Memory + handoff writes (~2–3 evenings)
- Whitelist: `mtc_cli/` + dashboard button extensions only.
- Deliverables: `mtc memory append`, `mtc handoff write`,
  `mtc handoff lock/unlock`. `.bak` rotation, mtime guard, append-only
  defaults, `--dry-run` default for first week.
- CLI becomes sole programmatic writer for `GLOBAL_HANDOFF.md`,
  `SESSION_LOG.md`, `NEXT_STEPS.md`, `DECISIONS.md` — automates Gate 7.
- Hand-edits still allowed (Barış) but a pre-commit hook warns.
- Acceptance: idempotent (run twice unchanged repo = byte-identical),
  hostile-input tests pass, generated handoff < 2KB.
- Gates: full G1 → G7. G6 mandatory.

#### MVP-2+ (later, not committed)
- `mtc pine check` (wrap MCP `pine_smart_compile` — read-only).
- `mtc report build` (deterministic report from backtest artifact dir).
- `mtc route classify` (cheap-model intake classifier with JSON-schema gate).
- CLI-Anything evaluation: deferred indefinitely. Revisit Q3 2026 only if
  trigger condition (need to drive an unscriptable external GUI) appears.

#### Out of scope (do NOT do under SP-001)
- Any edit to `MTC_V2.pine`, parity files, or MTC strategy behavior.
- Live trading anything.
- New root-level handoff files.
- New prompt folder at root — templates (if any) go in
  `04_SHARED/prompts/05_ai_workflow/`.
- Replacing `mcp__tradingview__*` tools. CLI wraps, never replaces.
- Auto-execution of `next_action` suggestions in CLI output.
- New runtimes (node, rust, go). Python + PowerShell only.

#### Open risks to carry into G1
- `PROJECT_MEMORY.md` (stable) vs `ACTIVE_FILES.md` (volatile) boundary —
  CLI's audit must respect, not blur.
- Gate 5 cross-model review not hook-enforced — must invoke Codex/Gemini
  manually for MVP-0.
- Parity smoke command not pinned — N/A for MVP-0/0.5/1, but record gap
  forward to first parity-touching sprint.

## Recently Closed (2026-05-31, Phase 6 follow-ups)
- I: source-parent cleanup completed for the Command Center audit. `QLR_*` parent rows that share a YouTube URL with extracted child candidates, or contain multi-case split evidence, are now `SOURCE_PARENT`, hidden from normal strategy/MTC_V2 queues, and protected by tests. Remaining visible rejected rows have transcripts and are rejected for source/classification reasons, not missing transcript.
- G: transcript/source-map repair for `11_TRIAGE/2026-05-30_rejected_worklist.xlsx` completed in the clean repo. The 99 HAS_URL_NO_TRANSCRIPT worklist candidates now resolve with transcript links in the refreshed audit; NO_URL_NO_TRANSCRIPT remains unresolved by user report.
- H: repeated-URL audit completed for the same workbook. See `MTC_COMMAND_CENTER/11_TRIAGE/duplicate_url_strategy_audit_2026-05-31.md`; no clear accidental duplicate group found.
- A: audit artifacts committed (`2a38d19`).
- B: legacy freeze policy ratified — accept + document, no NTFS DACL (`dcdf913`).
- C: xlsx-missing warning suppressed in CSV-only mode + AUTO_002 smoke PASS (`d35e620`).
- D: Phase 4 manifest full SHA256 + Phase 5 divergence notes (`c3e78f4`).
- E: `update_tracker.py` documented as deferred one-shot (`1b7caff`).
- F: Phase 1 verification reviewed — PASS; path rewrite policy ratified
  (active set complete, deferred set fix-on-demand). See
  `docs/migration_manifests/PATH_REWRITE_POLICY.md`.

## Reference Documents
- Migration audit: `docs/migration_manifests/phase6_audit_report.md`
- Legacy freeze policy: `docs/migration_manifests/LEGACY_FREEZE_POLICY.md`
- Path rewrite policy: `docs/migration_manifests/PATH_REWRITE_POLICY.md`
- Per-script TODO: `MTC_COMMAND_CENTER/02_MTC_BACKTEST/hardcoded_path_rewrite_TODO.md`

## Codex lifecycle closure (2026-06-06)

### MTC-LIFECYCLE-FIXES | DONE 2026-06-06 (Codex GPT-5) | Approved by Baris [AI: Codex]
- Applied approved lifecycle fixes in `02_MTC_BACKTEST/src/engine/mtc_runner.py`: max-pyramid config guard, time-stop enabled/use_bars semantics, EOD/EOW previous-bar boundary closes, daily consecutive-loss reset timing, `_is_end_of_day/_is_end_of_week`, explicit once-per-bar unrealized equity update, and TRAIL close-price fills.
- Fixed `data_tools/validate.py` gap severity to use timeframe-relative thresholds (`>=3x` WARN, `>=15x` ERROR).
- Refreshed producer parity: `02_MTC_BACKTEST/results/producer_parity/ql_fam_momentum_continuation_trx_4h_2026-06-06_after_lifecycle_exit_fix/` PASS.
- Refreshed MEV: `02_MTC_BACKTEST/results/mtc_engine_validation_runs/ql_fam_momentum_continuation_20260606_120640Z/`, `parity_status=PASS`, `strategy_return_pct=-103.9416`, B&H `214.6469`.
- Refreshed lifecycle readiness: `03_STATUS/lifecycle_fixed_2026-06-06/`; Gate3 `OK=1 INCOMPLETE=8 FAIL=0`; all-gates `promotable=1 not_promotable=8`.
- Warning: `promotable=True` is a scorecard result only. No live trading, no broker/webhook enablement, no MTC_V2/Pine production change.

### MTC-FULL-SUITE-RESIDUALS | OPEN 2026-06-06 (Codex GPT-5) [AI: Codex|Baris]
- `02_MTC_BACKTEST` full suite after fixes: `250 passed, 10 skipped, 5 failed`.
- Residuals: `test_optimizer_migration_script.py` expects old `MTC_COMMAND_CENTER/mtc_backtest` cwd; `test_parity_smoke.py` expects missing TV debug CSV; `test_reports_ui_static.py` expects old `mtc_backtest/app.py`; `test_ui_phase31_static.py` expects old navigation labels.
- Do not fake the TV CSV or add compatibility wrappers casually. Treat as a separate data/UI compatibility cleanup.

### STRATEGY-INTELLIGENCE-UI-PILOT | DONE 2026-06-14 (Codex GPT-5) | STG084 Strategy Intelligence Page v2 pilot [AI: Codex]
- Implemented the pilot from `11_TRIAGE/ui_references/strategy_intelligence_lovable/CODEX_MTC_STRATEGY_INTELLIGENCE_UI_PILOT_PROMPT.md`.
- Files: `08_DASHBOARD_APP/apps/web/app.js`, `index.html`, `styles.css`.
- Adds sidebar entry for STG084 Strategy Detail plus `Backtest Result Explorer` and `Strategy Leaderboard` pilot pages.
- Uses real snapshot data for STG084 where available; profile/run-plan/leaderboard data stays explicitly unavailable because those artifacts/readers do not exist yet.
- Validation: `node --check` PASS; dashboard API `39 tests` PASS; local API health and snapshot smoke PASS. Browser visual QA blocked by in-app Browser policy for `127.0.0.1:8777`.
- Future [AI: Codex|Claude]: implement real read-only readers for `run_plan.json`, `backtest_profile_result.json`, and `leaderboard_snapshot.json` only after those artifact contracts are approved.

### STRATEGY-INTELLIGENCE-UI-RESCUE | DONE 2026-06-14 (Codex GPT-5) | simplify main Strategy Detail UX [AI: Codex]
- Follow-up rescue patch applied after the pilot was judged too close to the old raw audit/scorecard screen.
- Main page now keeps the exact high-level flow: Hero Summary, Workflow Bar, Strategy Overview, LLM Evaluation, Backtest Plan & Evidence, Paper Trading Readiness, collapsed Advanced Technical Details.
- Demoted raw/secondary material into Advanced Technical Details: raw gates, scorecard rows, linked legacy backtest rows, Review Journey, QuantLens details, Gemini Pre-Screen, Salvageable Ideas, artifact paths, technical IDs, raw snapshots.
- Main-flow tables were replaced with compact cards where practical; the Parameter Space Preview remains a compact table as requested by the prompt.
- Validation: `node --check` PASS; dashboard API `39 tests` PASS; snapshot smoke PASS. Cheap-agent review failed due harness file-selection drift; no writes from the harness.

### GOOGLE-STRATEGY-INTELLIGENCE-FINAL-CLEANUP | DONE 2026-06-14 (Codex GPT-5) | read-only final integration cleanup [AI: Codex]
- Applied the final `google_strategy_intelligence_v2_final` prompt as a safe frontend-only cleanup on top of the existing Strategy Intelligence pilot/rescue work.
- Backtest Result Explorer now supports global sidebar scope and strategy-scoped links from Strategy Intelligence; its selector is populated from snapshot scorecards, pipeline rows, and registry entries instead of hardcoded STG084 text.
- Strategy Registry remains separate from Pipeline and now shows catalog columns plus row/button navigation into the generic Strategy Intelligence view by exact/base strategy id.
- Night backtest artifact contract is displayed as design/read-model status in Result Explorer and Diagnostics only; no ingestion, watcher, parser, schema engine, DB write, backtest launch, or execution path was added.
- Validation: `node --check` PASS; dashboard API `39 tests` PASS; `/healthz` PASS; `/api/snapshot?refresh=1` smoke PASS with 176 pipeline rows, 837 scorecards, 14 registry candidates; active UI forbidden-word/hardcoded-business-data search PASS. Browser visual QA blocked by in-app Browser policy for `127.0.0.1:8777`.

### DASHBOARD-SHELL-REPLACEMENT-CORRECTION | DONE 2026-06-14 (Codex GPT-5) | rejected result corrected [AI: Codex]
- Replaced the active served `/dashboard` shell instead of extending the old tab shell. The served page now defaults to Command Center Home and uses the Strategy Intelligence Command Center sidebar.
- Implemented reachable vanilla JS renderers for Home, Pipeline, Registry, generic Strategy Intelligence, Backtest Planner, Backtest Runs, Backtest Result Explorer, Leaderboard, Paper Trading, AI Knowledge Base, Advanced Artifacts, Diagnostics, Reports, and Read Model / Data Model.
- Updated the stale API dashboard contract test to expect `Strategy Intelligence Command Center`.
- Validation: `node --check` PASS; API unittest discovery `39 tests` PASS; served `/dashboard` has no old tab markers and served `/web/app.js?v=1` contains the required route/render markers.
- Browser visual QA remains blocked by in-app Browser enterprise policy for `127.0.0.1:8765`; direct HTTP served-route evidence is recorded in `GLOBAL_HANDOFF.md`.
- Future [AI: Codex|Claude]: a visual pass can be repeated only if Browser localhost policy is available; do not use alternate browser workarounds for the blocked policy.

### STRATEGY-INTELLIGENCE-DARK-VISUAL-FIDELITY | DONE 2026-06-14 (Codex GPT-5) | light skeleton corrected [AI: Codex]
- Applied the corrective visual-fidelity prompt against the final `google_strategy_intelligence_v2_final` screenshots/source, keeping the vanilla served app.
- Replaced the light admin visual system with a dark command-center theme: compact sidebar/header, dense dark cards, dark tables, workflow cards, strategy cards, status accents, right decision rails, result rail, chart placeholder, and leaderboard category cards.
- Preserved the read-only routing contract: default Command Center Home, generic `renderStrategyIntelligence(strategy_id)`, Pipeline/Registry navigation, global/strategy Result Explorer, and missing-artifact states.
- Validation: `node --check` PASS; API unittest discovery `39 tests` PASS; `/healthz` `overall_ok=True` and `mode=read_only`; served HTML/CSS/JS marker checks PASS; forbidden execution wording and hardcoded pilot data search PASS.
- Visual QA limitation: Browser screenshots remain blocked by enterprise policy for `127.0.0.1:8765`; no alternate browser workaround used. Direct served CSS/JS checks are recorded in `GLOBAL_HANDOFF.md`.
- Future [AI: Codex|Claude]: if Browser localhost policy becomes available, capture visual screenshots for Home, Pipeline, Registry, Strategy Intelligence, Planner, Explorer, Leaderboard, Diagnostics, and Read Model.

### TS-P1-001 | Canonical order-state machine | REPAIRED TWICE 2026-07-20, awaiting third re-audit (Claude Sonnet 5) [AI: Codex|Baris]
Built in `C:\TSP1001` (branch `feature/ts-p1-001-order-state`, base `cfb08b81` = TS-P0 HEAD/PR #25). Build commit `5140e062` BLOCKed (F1 named mutable seed dicts, F2 unreason-coded/repr-unsafe exceptions) → repair `851d88a0` BLOCKed again on re-audit (F1-R: `MappingProxyType`'s backing dict is still reachable via standard `gc.get_referents()` regardless of naming; F2-R: `type(raw).__name__` unsafe against a hostile metaclass) → second repair `a15a6b1f6648016fe99278fe993daa2c1b49b923` (parent verified = `851d88a0`, same 3 files) replaces `MappingProxyType(dict)` with a private tuple-backed `_ImmutableMapping` (no dict/list anywhere in its `gc.get_referents` closure) and makes `UnknownRawOrderStatusError`'s message a constant per reason_code touching no attribute of `raw` at all. 85 tests focused, 303/303 full suite both required CWDs.
Next: [AI: Codex] independent re-audit of `a15a6b1f` (see `11_TRIAGE/CLAUDE_TSP1001_REPAIR2_REPORT_2026-07-20.md`). [AI: Baris] accept or reject the invariant contract only after re-audit passes — 5 open design questions unchanged by either repair round (PENDING→SUBMITTED alias choice, PENDING_CANCEL→OPEN cancel-reject edge, direct terminal edges bypassing PENDING_CANCEL, WAITING_CHILD exclusion, UNKNOWN_SUBMISSION's wide resolution set). Blocks TS-P1-002 (durable identity) which depends on P1-001.
### P2-OUTAGE-TOLERANCE-AUDIT | DONE 2026-07-15 | code `0e644b52` [AI: Claude]
- Fable independently audited the outage-tolerance build PASS; Barış then authorized the single deploy/re-ARM window.

### P2-DAY0-V4-POST-ARM-AUDIT | OPEN 2026-07-15 | runtime `1465f8f0` [AI: Claude]
- Audit run `paper-20260715105547`, the single `12:02:42.856537Z` ARMED transition, fresh-bar proof, two post-ARM reconciles, empty positions/orders, and final master merge evidence.
- Monitor Day 0 v4 as validation-tier until the planned July 18 PC-off; record that shutdown as a planned boundary, not a safety incident. [AI: Any]
- Start definitive D3 only after VPS migration at end of month. [AI: Barış|Claude]

### P2-PR-MERGE-REGISTRY-CONFLICT | BLOCKED 2026-07-15 | PR #19 [AI: Claude|Barış]
- PR #16 is merged remotely at `20237733`; PRs #17–#19 remain open.
- Local isolated master contains unpushed #17/#18 merge commits `60415b08` and `89725dfe`.
- PR #19 adds an out-of-scope conflict in `05_REGISTRY/RESEARCH_RUN_REGISTRY.json`; do not resolve or push without Fable review and explicit direction. The attempted #19 merge was aborted cleanly.

### GATE-A-SECOND-FLAGSHIP | BLOCKED 2026-08-02 | `c5a4070a` + `5a9bb922` [AI: Barış]
- Both frozen candidates now hold an executing **ACCEPT** from `claude-opus-5` xhigh. Records:
  `11_TRIAGE/GATE_A_C5A4070A_RETROSPECTIVE_AUDIT_2026-08-02.md`,
  `11_TRIAGE/GATE_A_QUEUE_C_FLAGSHIP_AUDIT_2026-08-02.md`.
- D025 rule 3 still needs `gpt-5.6-sol`. It cannot execute: Codex CLI 0.145.0 forces every command
  through `powershell.exe -Command` and stays `sandbox: read-only`, which is `blocked by policy`
  outside a trusted project directory. Quota is not the constraint — `.codex-hesap2` has ~99% left.
- [AI: Barış] choose one: (a) authorize `--dangerously-bypass-approvals-and-sandbox` for audit-only
  Codex runs; (b) mark the audit worktrees trusted from an interactive `codex` session, which this
  non-interactive harness cannot do; (c) downgrade/upgrade the Codex CLI to a build whose `--sandbox`
  flag is honoured; (d) substitute a different canonical auditor for the second flagship slot.
- Until then: **do not** integrate, rebuild the payload, rerun Gate A, merge to `master`, or touch
  KVM2 on either branch.

### GATE-A-QUEUE-C-F1 | OPEN 2026-08-02 | `5a9bb922` [AI: Codex|Claude]
- `tests/test_credential_free_disarmed.py:64` — `assert not hasattr(app.state, "bridge_broker")` is
  vacuous; `app.state.bridge_broker` is never set anywhere in `bridge/` and measures `False` in both
  start modes. Replace with a real check, e.g. `"bridge.broker.hyperliquid" not in sys.modules`
  after a credential-free start. Fold into the next authorized touch of this branch — it does not
  justify a repair round of its own.

### GATE-A-BUILD-NITS | OPEN 2026-08-02 | `c5a4070a` [AI: Codex|Claude]
- N1 `test_package_builder_pins_export_inputs_and_has_fail_closed_cr_guard` asserts on the text of a
  code comment. Prefer the behavioural fixture recorded in the retrospective audit §4.
- N2 `test_package_manifest_is_identical_across_c_and_en_us_utf8_locales` fails rather than skips on
  a builder without a generated `en_US.UTF-8` locale.

### GATE-A-3B | HARD STOP unchanged 2026-08-02 | `df00634f` [AI: Barış]
- Untouched this session. Three-result ceiling reached; reopening needs an owner-directed new cycle.
