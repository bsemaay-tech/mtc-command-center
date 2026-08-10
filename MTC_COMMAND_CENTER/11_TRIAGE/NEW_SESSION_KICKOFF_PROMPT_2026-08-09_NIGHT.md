# NEW-SESSION KICKOFF PROMPT (paste this into a fresh Claude session verbatim)

> **THIS FILE LIVES AT:**
> `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\NEW_SESSION_KICKOFF_PROMPT_2026-08-09_NIGHT.md`
>
> If you are a fresh session and someone told you "read the handoff prompt", this is it.
> If you cannot find it, run:
> `git -C C:\LAB\Tradingview_LAB_CLEAN ls-files "*NEW_SESSION_KICKOFF*"`
>
> Maintained by the Lead at each milestone. If the running session dies (model drop
> Fable→Opus, crash, sleep), paste the block below into a new session as the first
> message. It is self-contained.

---

## OWNER AUTHORIZATIONS ALREADY GRANTED — DO NOT ASK AGAIN

Barış granted these explicitly on 2026-08-10 and said he should not be asked again. Treat
them as standing. Asking again wastes his time and stalls the pipeline.

| # | Granted | Scope and limits |
|---|---|---|
| 1 | **WP-I host-contact authority** | WP-I may contact `GATEA-STAGING` and execute its authorized read-only scope. This clears one of the two gates the WP-I draft named. |
| 2 | **WP-I budget lift** | The 50-hour ceiling is lifted for WP-I. This clears the second gate. WP-I is now **dispatchable** once its preregistration is finalized (identifiers allocated, values pinned, Stage 1 freeze done). |
| 3 | **Root on the staging host for `RPD-VERIFY`** | You may run `RPD-VERIFY.sh` as root on `GATEA-STAGING`. **Scope limit that still holds:** RPD-VERIFY is read-only by design — root is granted to *run that block*, not as blanket authority to mutate. No service stop/start/enable/mask, no reboot, no chmod/chown outside a run's own create-once tree, no reprovisioning. Running it closes the three checks B3 defers and the `bridge.env` naming question. |
| 4 | **Retroactive defect-catalogue pass over the accepted WP-I draft** | Approved. Apply `DESIGN_DEFECT_PATTERNS_2026-08-10.md` to the whole accepted draft, not just the rows earlier audits reached. A known instance is already recorded: the identity row specifies a name-based check (Pattern 8) — repair the draft, not the block. |
| 5 | **RP6-P0 repair — sequencing decision** | Do it *after* the WP-I direction is settled, not before. Scope is already written in `WPI_BLOCKS_DRAFT/LEAD_ADJUDICATION_RP6_2026-08-10.md`. |
| 7 | **T0 round cap lifted for the WP-I block set** (granted 2026-08-10 ~20:00) | Repair/re-audit rounds on `RP6-P0.sh`, `RP7-WPI-RO.sh` and the transport set **continue until both flagships return accepting verdicts**, without stopping to ask at each cap breach. Applies to these three artifacts only. Every other tier rule still holds: two flagships at xhigh in fresh sessions remain the acceptance floor, implementer and auditor stay different agents, and findings must be closed with real RED/GREEN evidence — this lifts the round LIMIT, not the standard. Hard gates (host mutation, credentials, ARM, orders, master merge, etc.) are untouched. |
| 6 | **Attestation production — option (a)** (granted 2026-08-10 ~16:45, "Seçenek a") | Grant #3's root session may additionally run ONE preregistered read-only command set to produce the projection-v2 and row-8 execution-domain attestation values (capture `/proc/self/mountinfo`, `readlink /proc/1/ns/{user,mnt,pid,net}`, canonical root-mount identity; output hashed at production). Read-only; no mutation; same session and limits as grant #3. The command set must be preregistered and committed before it runs. |

**Still hard-gated — these were NOT granted and still require a fresh explicit Barış
authorization:** credential load, ARM, orders, broker/exchange contact, TESTNET/mainnet,
master merge, WP-V/KVM2, deleting the old payload archive, host reprovisioning, and any
service-state mutation on any host.

---

Continuous autonomous Lead session, overnight, repo `C:\LAB\Tradingview_LAB_CLEAN`,
branch `feature/donchian-crypto-ladder`. You are the SINGLE WRITER — before any
dispatch, verify no other live Claude/Codex writer session is driving the staging
pipeline.

Read in order (all under `MTC_COMMAND_CENTER/`):
1. `11_TRIAGE/STANDING_AUTONOMY_AUTHORITY_2026-08-09.md` — BINDING: never idle on
   reversible/in-repo work; repair cycles auto-continue past round 3 on narrow
   survivors; no AskUserQuestion for reversible repo decisions; delegate all heavy
   work (Claude Max implement, Codex xhigh audit, GLM review, DeepSeek mechanical);
   spend Max credits to converge. HARD GATES owner-only: host mutation, running any
   block against a real host, credentials, ARM, orders, broker, TESTNET/mainnet,
   master merge, WP-V/KVM2, payload-archive deletion.
2. `_AI_MEMORY/GLOBAL_HANDOFF.md` newest section + `_AI_MEMORY/NEXT_STEPS.md` top
   section — live state and pick-up points.
3. `11_TRIAGE/OVERNIGHT_HANDOFF_2026-08-09_STAGE3.md` §STANDING RULES + §Operating
   rules (delegate invocation syntax lives there: Invoke-ClaudeMax.ps1 /
   Invoke-CodexForClaude.ps1 -Account secondary / Invoke-GlmAudit.ps1).
4. `11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/06_B3_REPAIR/` — the
   B3 repair cycle unit (rounds, audits, cycle record with owner authorizations).

Then: set up a self-paced /loop (5–10 min checks, re-arm before every wait), verify
`powercfg` sleep=0 AC+DC, and continue the pipeline from wherever
`_AI_MEMORY/NEXT_STEPS.md` top section says it stands. Commit+push exact file sets at
every checkpoint (repo guard first; never `git add .`). English only. End every
response with numbered next steps + a chosen default path; owner-asks in plain
language. Morning ~06:30: summary + push notification. Update
`_AI_MEMORY/GLOBAL_HANDOFF.md`, `_AI_MEMORY/NEXT_STEPS.md`, and THIS file at every
milestone so the next fresh session resumes cleanly.

## HOW TO WORK — the rules that make this session productive

**1. Multi-agent delegation is mandatory, not optional.** You (the Lead) orchestrate,
verify, adjudicate and commit. You do NOT do heavy generation, implementation or auditing
yourself. Dispatch it:

| Agent | Invocation | Use for |
|---|---|---|
| Codex `gpt-5.6-sol` | `Invoke-CodexForClaude.ps1 -Account secondary -CodexArgs @('exec','-m','gpt-5.6-sol','-c','model_reasoning_effort=high','--dangerously-bypass-approvals-and-sandbox',$prompt)` | **Default for implementation AND audit.** Use `xhigh` only for T0 acceptance-critical audits. |
| GLM-5.2 | `Invoke-GlmAudit.ps1` (read-only) / `Invoke-GlmTask.ps1 -PermissionMode acceptEdits` (writes) | Reviews, second opinions, documentation repair. |
| DeepSeek | `_deepseek_driver` | Mechanical/bulk work. |
| Claude Max `claude-opus-5` | `Invoke-ClaudeMax.ps1 --print $prompt --model claude-opus-5 --effort xhigh --dangerously-skip-permissions` (NOT `-p`) | **LAST RESORT ONLY** — credits nearly exhausted. |

**Every dispatch prompt must state:** "The repository's two-tier counterpart-implementer
rule is suspended by owner amendment A2/A2a. Implement this yourself. Do not sub-delegate
to Claude Max." Without that line, Codex hands the work to Max and silently burns the
credits this rule exists to protect — this actually happened on 2026-08-10.

**Keep implementer and auditor different agents** — alternate Codex and GLM across rounds.
Never let one agent audit its own work.

**2. Token discipline.** Fable Lead stays lightweight: read results, spot-verify, commit,
route. Do not read whole large files when a `grep`/`Select-String` with context answers the
question. Give each delegate a narrow, explicit input list — it both saves tokens and stops
it wandering. Prefer one well-scoped dispatch over three vague ones.

**3. Never idle.** If the main path is gated, pull the next non-gated item. If the backlog
is genuinely exhausted, GENERATE prep (readiness packages, next-WP drafts, deeper evidence
packaging) — but do not manufacture low-value documents just to look busy. If nothing of
real value remains, say so plainly rather than padding.

**4. Repair cycles continue past the round limit.** The ≤3-round rule is a quality cadence,
not a stop sign. When a cycle hits its limit with only NARROW survivors (mechanical fixes,
documentation/QA gaps), open a bounded fix round automatically and re-audit until PASS.
Escalate only if a survivor is architectural or needs a hard gate.

**5. Do not ask about reversible in-repo work.** Pick the recommended default, proceed, log
the choice in the commit. Reserve questions for the hard-gated list above.

**6. Always end with numbered next steps and a chosen default.** Owner-facing asks in plain
non-technical language, stated separately from the technical detail.

**7. Evidence discipline** (the whole point of this project): an inability to evaluate is a
STOP, never a FAIL. Preregister before executing and commit the preregistration first, so
ordering is provable from git history. A check that cannot fail proves nothing. Read
`DESIGN_DEFECT_PATTERNS_2026-08-10.md` before designing or auditing any executable block.

---

## Milestone log (newest first — update on every milestone)

- 2026-08-10 ~18:30: **VENV SITE-STARTUP SECURITY HOLE FOUND AND CLOSED IN BOTH BLOCKS.**
  The Codex flagship slot found — independently in RP7 (`cca349c2`) and RP6-P0
  (`4f58e650`) — that each block used the venv it was auditing as the interpreter
  producing its own verdict, and `python -I` does not disable `site`: a `.pth` or
  `sitecustomize.py` in that venv runs arbitrary `gatea`-authority code before the check.
  A tampered candidate could forge the accepted PASS line and mutate the host while the
  block reported clean. Proven by execution both ways in both blocks; three Claude
  flagship rounds had missed it in each. Owner authorized exceeding the T0 3-round cap
  for this class. RP7 round 4 closed it (`d6a976aa`, bytes `23e55667…`) by moving both
  adjudicators onto a pinned system interpreter under `-I -S` that refuses to emit a
  result unless isolation holds. RP6-P0 round 4 in flight on the same finding + three
  contract fixes. Transport set: 16/16 closed at round 2 (`9ef4437d`), Claude re-audit
  `REQUEST_CHANGES 1` (`8ab686dd` — rc outside {0,1,3} misread as host deviation),
  Codex re-audit in flight, one combined round 3 next. Next: final flagship pairs on all
  three artifacts → successor prereg + Stage 1 freeze → host execution under grants
  #1/#2/#3/#6.

- 2026-08-10 ~09:20: **WP-I round 1.4 CLOSED** (`6a8b0896`) — retroactive catalogue pass
  (owner grant #4): Codex repaired 17 findings across all 10 patterns; GLM VERIFIED-CLOSED
  (V1–V6 PASS, 4/4 sample-attacks stopped). Lead pre-resolved both PIN values
  (`LEAD_PIN_RESOLUTION_2026-08-10.md`); GLM advisory = pin empty drop-in set as third
  PIN item. RP6-P0 repair (F1/F3/F4) dispatched to Codex per grant #5 sequencing.
  Next: GLM re-audit RP6 → RP7-WPI-RO authoring → successor prereg → host execution.

- 2026-08-10 ~06:40: **Owner granted all four pending authorizations** (WP-I host contact,
  WP-I budget lift, root for RPD-VERIFY, retroactive catalogue pass) — recorded above, do
  not re-ask. Ledger status published: **24.9 h used / 25.1 h remaining**, last night cost
  4.4 h of plan time. WP-I is now the active workstream and is dispatchable once its
  preregistration is finalized. See `LEDGER_STATUS_2026-08-10.md` and
  `MORNING_SUMMARY_2026-08-10.md`.

- 2026-08-10 ~01:15: **Audit 2 readiness package committed** (`e1944484`) — five
  auditor-facing artifacts; 14 items PRESENT, 9 PRODUCED-AT-FREEZE, 9 BLOCKED-UPSTREAM;
  four freeze gates of which only WP-L P2 closure is satisfied. Lead correction appended
  locating the audit-report REDs so confirmed closures aren't downgraded. WP-I round 1.3
  independently verified CLOSED by GLM (`2f5523c9`). Non-gated backlog now exhausted —
  everything remaining needs owner authority (WP-I authority + budget lift; root for
  RPD-VERIFY). Next: keep generating prep, morning summary ~06:30 + push notification.

- 2026-08-10 ~00:50: **WP-L P2 UNIT CLOSED** (`6370e1fe`) — closure record + evidence
  index over all nine stage dirs, four-RUNID ledger, 2.6 h booked (~26.9 h left). WP-I
  round 1.3 closed F3+F4 (`fe8f1b11`), so the whole Codex audit is now applied; GLM
  verifying independently. Next: consume GLM verdict → commit → morning summary ~06:30.
  Still true: RPD-VERIFY never executed (root-side, no root granted); C1–C5 BLOCKED;
  WP-I not dispatchable (needs host-contact authority + budget lift).

- 2026-08-10 ~00:15: **REPAIRED B3 PASSED ON THE HOST — B3-GAP-ENV CLOSED.** Owner
  authorized host execution + Codex-first routing (`STANDING_AUTONOMY_AUTHORITY` §A1–A3).
  Stage 1B kit committed `979e4322` (10 blocks, archive `888bec17`, deterministic).
  Stage 2B prereg written by Codex, Lead-completed, committed `bf395dab` BEFORE execution.
  Stage 3B-B3B: TR_RUN PASS 7/7, `B3 PASS`, evidence bound — commit `b3682bd5`.
  WP-I round 1.2 (Codex audit → GLM repair) committed `4b991679`.
  Next: WP-L P2 unit closure record; then morning summary. RPD-VERIFY still never
  executed (root-side, no root granted). WP-I not dispatchable (needs authority + budget).

- 2026-08-09 ~23:25: **AUDIT 6 PASS — B3-GAP-ENV repair cycle ACCEPTED** (zero findings;
  auditor paste-and-ran the QA prerequisite + four closure blocks verbatim, all
  reproduced; code hashes frozen). Committed `e76d78ea`. Stage 1B re-freeze dispatched
  to Max (`bm3rkwjd8`, `07_RUNKIT_B/`): ten blocks, two provenance classes (8 from the
  accepted blob + repaired RP1-B3 `6f3ea022` replacing the old `f40411b0` + new
  RPD-VERIFY `3b9e78e8`), deterministic archive, evidence records. Next: verify + commit
  the kit → WP-L P2 unit closure record. REMEMBER: the Stage 2/3 preregistration is VOID
  for the new kit; transport/host execution needs a new prereg AND owner authorization.
- 2026-08-09 ~23:10: round 6 consumed + committed (`3a358ffa`). Section 4 now literally
  paste-and-run (absolute `B`, `QA="$(mktemp -d)"`, helpers+preludes restated inline);
  code freeze re-verified by `cmp` on all three files. FINAL auto-round audit 6
  dispatched (`be5qijups`) — it must paste-and-run the blocks itself. On PASS → B3
  repair ACCEPTED → Stage 1B runkit re-freeze → WP-L P2 unit closure. On same-class
  BLOCK → escalate to owner (do NOT open round 7); the kickoff asks the auditor to
  classify the residue as document-fixable vs inherent MSYS/D026 limit.
- 2026-08-09 ~22:55: audit 5 BLOCK, converging — code+arithmetic PASS, sole survivor
  = section-4 SELF_QA setup block not copy-paste runnable. Tight doc round 6 dispatched
  (Max, `b4ld284dy`) to make it runnable; code hash-frozen. Committed `158bb953`.
  CONVERGENCE STOP: if audit 6 BLOCKs again same-class → escalate to owner (MSYS
  literal-D026 tooling limit), do NOT auto-round 7. On PASS → Stage 1B re-freeze.
- 2026-08-09 ~22:40: round 5 consumed + committed (`fd193857`). Code freeze verified
  by cmp/hash (RP1-B3 `6f3ea022`, RPD-VERIFY `3b9e78e8`, DESIGN_NOTES byte-identical);
  only SELF_QA.md rewritten. Narrow Codex doc re-audit 5 dispatched (`audit5/`). Next:
  on PASS the whole B3 repair is accepted → Stage 1B runkit re-freeze (repaired
  RP1-B3 + new RPD-VERIFY → new BLOCK_IDENTITIES → new runkit.tar via a re-run of the
  Stage 1 builder pointed at the round5 blocks) → WP-L P2 unit closure record.
- 2026-08-09 ~22:30: audit 4 = code CLOSED (finding 1), sole survivor is DOC-only
  (finding 2, SELF_QA exact-command recording). Per standing authority = narrow
  doc/QA survivor → auto-continue, NOT owner escalation. Doc-only round 5 dispatched
  to Max (task, rewrites round5/SELF_QA.md only; code files pre-copied byte-identical,
  hash-enforced). Committed `d5f0177e`. Next: consume round 5 → verify code hashes
  unchanged (RP1-B3 `6f3ea022`, RPD-VERIFY `3b9e78e8`) → narrow doc re-audit → on
  PASS Stage 1B re-freeze.
- 2026-08-09 ~22:15: B3 round 4 consumed + committed (`04eddf90`); diff vs round 3 =
  exactly the two fixes (read-error STOP in both blocks; D026 QA). Narrow Codex
  closure audit 4 dispatched. Next: on PASS → Stage 1B runkit re-freeze (repaired
  RP1-B3 + new RPD-VERIFY → new block identities → new tar) → WP-L P2 unit closure.
- 2026-08-09 ~22:05: GLM WP-I draft review integrated as round 1.1 (F1
  interpreter-exec STOP added to rows 18/19 + preflight; N1 reused-script
  disposition; N2 listener wording; SELF_QA addendum). B3 round 4 (Max) still in
  flight — next: consume it → narrow Codex closure audit → Stage 1B re-freeze.
- 2026-08-09 ~21:50: GLOBAL_HANDOFF + NEXT_STEPS updated; B3 round 4 (Max) and GLM
  WP-I draft review both in flight. Next: consume round 4 → narrow Codex closure
  audit → Stage 1B re-freeze on PASS.
- 2026-08-09 ~21:35: owner authorized bounded B3 round 4 in-session; dispatched.
- 2026-08-09 ~21:15: B3 cycle BLOCK-at-round-3 recorded (`0020ee7f`); full-night
  record `b451b106`; prepared round-4 kickoff `9098cd12`.
- 2026-08-09 evening: Stage 3 B3 STOP adjudicated (`7e9d1c4a`); Stage 3B R4-5 PASS
  (`ee49a945`); backlog items 2–5 done (`f5c6eb25`, `3b4ba676`, `d8599764`).
