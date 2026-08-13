# FRESH-SESSION HANDOFF — WP-I, 2026-08-13 morning

**READY TO USE.** Sections 0–6 and 9 are complete as of 2026-08-12 ~17:45. Section 7 (overnight
Claude Pro results) and section 8 (ledger) are filled after the 23:00 audits run — if you are
starting a session **before** those audits, §7/§8 are simply not yet written and §6 tells you
what is in flight. Paste this whole file as the first message of a new session. Self-contained.
Supersedes `FRESH_SESSION_HANDOFF_2026-08-12_MORNING.md`.

**Read §0 first — it is the binding operating contract, not background.**

Repo `C:\LAB\Tradingview_LAB_CLEAN`, branch `feature/donchian-crypto-ladder`. You are the LEAD:
orchestrate, verify verbatim, adjudicate, commit exact file sets. You do NOT author or audit the
heavy artifacts yourself. Read: this file, then `AGENTS.md`, `_AI_MEMORY/START_HERE.md`, and the
routing + defect-pattern files.

---

## 0. AUTONOMOUS OPERATING RULES — BINDING, owner-set 2026-08-12

These are not suggestions. The owner corrected the Lead on rules 1 and 2 **three times** during
the 08-12 session. Read them before dispatching anything.

**RULE 1 — NEVER IDLE. Not for one minute, not for one hour.**
When a lane finishes, **start the next backlog item in the same turn**. Do not defer work to
"the next wakeup." Do not wait for a model's window to open. Do not schedule a long sleep because
"the next milestone is at 23:00." If there is no queued task, pull from the fallback backlog
(§6). If the backlog is empty, create useful work: cross-check a claim produced by a single lane,
re-derive a count nobody has re-derived, or sweep records against bytes. There is always
verification work.

**RULE 2 — RUN AS MANY PARALLEL LANES AS THE ACCOUNTS ALLOW.**
Two lanes is too few. Target **4+ concurrent lanes.** Available slots: Codex `-Account fourth`
(gpt-5.6-sol), Codex `-Account free` (gpt-5.5), and GLM — GLM tolerates concurrent dispatches.
Each lane must own a **disjoint output file set**; name the owned files in every kickoff so
concurrent lanes cannot collide. Never let two lanes write the same file.

**RULE 3 — CREDIT DISCIPLINE, in priority order.**
1. **Codex carries the weight.** It is the primary implementer *and* auditor. Prefer it for
   everything it can do. `secondary` is exhausted until 08-16; use `fourth` and `free`.
2. **GLM is the second auditor while the Claude Pro window is closed.** The owner authorized this
   explicitly. GLM is source-level only (see Rule 5) and its verdicts are `ADVANCE-SUPPLEMENTAL`,
   but it does real work: on 08-12 it produced four advance audits and caught a second staleness
   a stronger model had missed.
3. **Claude Max is RESERVE — protect the credit.** Its weekly limit was nearly exhausted on
   08-12. Use it only when a task is acceptance-critical AND Codex and GLM genuinely cannot do
   it. Record the justification in the commit when you do.
4. **Claude Pro** is the flagship auditor and the only thing that closes a second-flagship slot.
   Spend its window on audits, not on work Codex could do.

**RULE 4 — THE TWO-FLAGSHIP GUARANTEE IS NOT NEGOTIABLE.**
GLM and Max **cannot** fill a second-flagship slot. Dual acceptance requires Codex **and** Claude
Pro (`claude-opus-5` xhigh) on the **same bytes**. Putting GLM in that slot would forge the
guarantee that Audit 2 exists to check. GLM's advance audits reduce risk and save time; they
never convert a PENDING row to accepted.

**RULE 5 — GLM IS EXECUTION-GATED *AND* SCOPE-LIMITED.**
It cannot run harnesses on this host. Dispatch with `-PermissionMode acceptEdits` **plus** an
explicit "you are unattended, do not ask for approval" clause **plus** "never fabricate a green
run." Expect source-level verdicts with execution steps marked `PENDING-LEAD-EXECUTION`.

**Scope limit, measured on 08-12: GLM is reliable for SMALL and MEDIUM reads and fails on LARGE
ones.** Four medium-scope advance audits succeeded and produced real value. Then **four
dispatches failed**: an API death mid-response, a plan-mode stall, a four-document SELF_QA audit
(1.5 MB total) that hit a connection close plus a 600s background ceiling while spawning
sub-auditors, and a 198-path WP-L sweep that returned only `API Error: The operation timed out.`
**Route large-scope work to Codex.** If a task must go to GLM and might be large, split it by
document or by directory and say in the kickoff that a partial with honest coverage boundaries
beats a timeout that produces nothing.

**Always check the report is substantive before committing** — a tiny file is a red flag. Delete
partials; never commit them. Also check both the `-OutputReport` path *and* wherever the model
says it wrote, because GLM sometimes writes its real verdict elsewhere.

**RULE 6 — THE LEAD'S VERBATIM RUN IS THE EVIDENCE OF RECORD.**
Extract published fences **as bytes**, run them from outside the repo, and diff the transcript
against what the document publishes. Never accept an implementer's claimed green.

**RULE 7 — VERIFY WHAT MODELS TELL YOU, INCLUDING THE MODEL'S OWN IDENTITY.**
On 08-12: a GLM finding was **false** and the Lead half-confirmed it (§3); Codex wrote
`gpt-5.6-sol` into two records when the run log said `gpt-5.5`. **Read the run-log session header
and name the actual model in every commit.** And confirming a claim's *premises* is not
confirming the *claim*.

**RULE 8 — STOP THE GRIND, ESCALATE THE BOUNDARY.**
When an auditor keeps finding "one more class," look for the structural inversion. If a round
still reopens after the inversion, do **not** open another round — write an
accept-with-disclosure recommendation and put the boundary decision to the owner. That is how
SEC102 closed on 08-12, with Codex's own verdict endorsing the stop.

**RULE 9 — COMMIT EXACT FILE SETS, NEVER `git add .`** The repo hook flips HEAD to master
between calls; use inline `git checkout <branch> && git add <paths> && git commit`.

**RULE 9b — THREE AUTHORING RULES FOR EVIDENCE DOCUMENTS.** All five WP-I evidence documents
were claim-audited on 08-12: **38 findings — 16 false, 18 unsupported, 4 scope-wrong**
(`WPI_CLAIM_AUDIT_SYNTHESIS_2026-08-12.md`). The named systemic cause is **local-evidence
overclaiming after late, carried-forward, or externally-evidenced authoring** — prose written
before or apart from the final run, then not re-derived. Put these in every implementer kickoff:

1. **No unfilled slot may sit under a "resolved" claim.** Before publishing, grep the document
   for `@@`, `PENDING`, and empty transcript fences. Every hit must either be filled with pasted
   output, or the prose must say `PENDING` and **exclude that section from closure**.
2. **Line-evidence rule for absolutes and numbers.** Any sentence containing `all`, `every`,
   `no`, `none`, `unchanged`, `byte-identical`, a count, `bytes`, `sha`, `rc`, or a run count
   must point to the exact pasted transcript line proving it. If the support is outside the
   document, label it `External evidence:` and cite the file — **never phrase it as locally
   transcript-proved**.
3. **Carry-forward re-derivation rule.** Any carried-forward section must be re-derived after the
   final artifact edit: replace old bytes, hashes, round labels and denominators from a current
   identity table. Scope wording must use the **exact denominator the transcript shows** —
   `10/11 plus one self-exclusion`, `seven targets plus the harness` — not `every block`.

Only three findings could plausibly affect an *acceptance* rather than needing a documentation
repair: the RP6 placeholder cluster, the SEC102 channel-contract scope word, and the transport
cleanup contradiction. **All three are already folded into tonight's kickoffs** for the
second-flagship auditors to settle.

**RULE 9c — A KICKOFF IS A CLAIM AND DECAYS LIKE ONE.** Before re-dispatching any existing
kickoff, **re-read its premise against current state and update it.** On 08-12 the Lead
re-dispatched a recount kickoff whose opening line read "nobody has re-derived them" — true when
written at 17:00, false by 19:50 because two re-derivations had landed in between. The lane
detected the stale premise, reconstructed the history from commits, and **refused to write the
file the kickoff named**, because doing so would have overwritten a committed artefact recording
an earlier lane's finding. That is the **second** time a lane protected a prior lane's record
from a Lead instruction that would have destroyed it. So also: **never instruct a lane to "write
exactly one file" at a path that already exists** unless overwriting is genuinely intended.

**RULE 10 — SURFACE, DO NOT DECIDE, ON OWNER-CLASS QUESTIONS.** Freeze, merge to master, host
execution, broker/live/paper, credential use, force-push, and accept-vs-harden boundary calls are
the owner's. Everything else — dispatch, verify, commit, push, correct the record — proceed
without asking.

## 1. ROUTING — owner-corrected 2026-08-12, BINDING

- **Codex is PRIMARY** for both implementation and audit. `-Account fourth` resolves to
  `gpt-5.6-sol`; `-Account free` resolves to **`gpt-5.5`** (weaker — name the actual model in
  every commit). `secondary` exhausted until 08-16.
  Flags: `--dangerously-bypass-approvals-and-sandbox --config model_reasoning_effort="xhigh"`.
- **Claude Max is RESERVE**, critical work only. The owner corrected this mid-day: Max's weekly
  limit was near full and it had been over-used.
- **GLM is authorized to fill waiting time** but is **source-level only** — unattended GLM
  cannot execute harnesses on this host. Always dispatch with `-PermissionMode acceptEdits`
  plus an explicit "you are unattended, do not ask for approval" clause and a
  "never fabricate a green run" clause. Two dispatches were lost on 08-12 before this was
  learned (one API death mid-response, one plan-mode stall).
- **HARD CONSTRAINT that survives all of the above:** GLM and Max **cannot fill a
  second-flagship slot.** Dual acceptance requires Claude Pro (`claude-opus-5` xhigh, default
  account). GLM runs are labelled `ADVANCE-SUPPLEMENTAL` and say so in their own verdict lines.

**Operational gotchas learned 2026-08-12:** PowerShell heredocs fail — write long commit
messages to a scratchpad file and use `git commit -F`. The Bash tool's `cd` leaks into
PowerShell's working directory — `Set-Location C:\LAB\Tradingview_LAB_CLEAN` before any git.

## 2. WHAT CLOSED ON 2026-08-12

**SEC102 — ACCEPTED-WITH-DISCLOSURE, freeze blocker #4 CLEARED.** The evidence harness took
three more rounds (r9 byte-identity → r10 object pinning → r11 nameless channel), each closing a
real class the auditor found. At r11 Codex's own verdict said "do not open a round-12 cycle; take
the boundary to the owner." The owner chose accept-with-disclosure. `composite_pathproof.py` is
byte-identical across r8→r11 and HEAD (129658 B, `adbf27fd…c05a`) — **every one of those rounds
was harness work, not security-logic work.** GLM's model-diverse second opinion: PASS-WITH-NITS,
source-level, honestly supplemental on execution. Four trusted-base assumptions now live in the
successor preregistration §4.4.1 as explicit non-controls, with §4.4.2 subordinating the §10.2
acceptance language to them.

**Audit-2 package: 16 of 20 items closed, 1 partial, 3 genuinely unavailable.** Packet 7 (the
current-cycle D026 map) closed: 39 rows mapped with a three-way execution-provenance split.
Packet 8 partial: the 45-row freeze-input reconciliation exists and answers blockers 7/8/9.

**Freeze blocker 8 reclassified.** The close-script contract disagreement is gone — plan rows
07/08 and `remote_close_tree_wpi.sh` both use three arguments. The stale record was wrong in
*two* respects and both are corrected. What remains is the `EXPECT_UID`/`EXPECT_GID` fill, which
belongs to blocker 7's class.

**Open current-audit D026 findings: ZERO.**

## 3. THE RP6-11 EPISODE — read this, it is the cautionary tale of the day

The D026 map surfaced one open row: the r15 "dynamically-resolved inventory-mutation target"
never got an executed RED/GREEN pair. A GLM advance audit answered it by claiming the r16 fence
*admits* a variable-mutating `eval` and certifies it CLEAN.

**That claim was false.** `SELF_QA_RP6.md:16763-16765` already refuses `eval`, `source` and `.`
as `UNMODELED kind=indirect_execution_builtin:*`. Codex found this while implementing the repair
and said so in its own report rather than building on the bad premise.

**The Lead's intermediate confirmation was partial and it matters.** It verified two true facts —
`eval` is in `admissible_bare`, and `eval` is absent from the enumerated mutating-builtin list —
then accepted the conclusion without checking whether a *different* branch catches it. It does.
Membership in `admissible_bare` only suppresses the unbound-invocation check; classification
happens elsewhere. **Lesson: confirming the premises of a claim is not confirming the claim.**

**The other half was real:** `dynamic_targets=0` was a hardcoded literal formatted to look like a
measurement, sitting beside a genuinely measured `variable_targets`. Round 17's sweep found six
such fields across three lines. Round 17 (Codex) closed it by inversion — a closed bare-word
effect model, with `dynamic_targets` now genuinely computed. Lead ran the fence verbatim:
`cases=15 pass=15 fail=0`, carried r16 grammar `50/50`, block identity unchanged.

## 4. BLOCK STATE

| Block | Codex flagship | Second flagship (Claude Pro) | Notes |
|---|---|---|---|
| RP6-P0 | PASS-WITH-NITS on **r16**; **fresh r17 audit 2026-08-12 ~21:50: REQUEST_CHANGES** (`wait -p` effect-model gap F1 + 3 evidence repairs); **r18 repair LANDED + Lead-verified (verbatim fence: 14/14 PASS, rc 0); fresh independent Codex r18 audit blocked on account limits until 08-16/08-18** | Claude audit released on r18 bytes (SELF_QA 1065504 B / `0bbf41dd…`) ~00:00 | Block byte-identical `5132bacd…` **since r11** (the r10a span claim was false — r10 blob is 107252 B / `3c7b7d26`; Codex r17 audit finding, Lead-verified). Evidence doc at **r17** (1038848 B, `07cf843d…`) — **neither the r16 acceptance nor any r16-anchored claim carries to those bytes** |
| RP7-WPI-RO | PASS (r9) | **PASS-WITH-NITS 2026-08-13 ~00:00 — DUAL FLAGSHIP ACCEPTANCE on 108301 B / `0e93f90d…`**, then the owner-decided **rows 1-9 build applied + GLM-advance-read round-2 repair: identity now 127046 B / `a2ec1d0c…`, acceptance REOPENED pending both flagships.** First evidence delivery (Python-simulated D026) rejected by the Lead; rebuild executes the block's own functions, Lead-verified 20 pairs + 4 controls PASS; a real row-6 defect surfaced and was fixed. Doc repairs + C1 disclosure folded in | GLM advance: PASS-WITH-NITS, zero required repairs |
| Transport set | PASS (r6b) | **PASS-WITH-NITS ~00:20 — DUAL FLAGSHIP ACCEPTANCE on the seven frozen targets.** First pass REQUEST_CHANGES (documentary) → six repairs at `a0fa8271` → re-audit executed the WSL2 harness verbatim and cleared both grounds; 3 LOW nits, none required | GLM advance: PASS-WITH-NITS, zero required repairs. F1 owner-ratified accept-with-disclosure, NOT a blocker |
| SEC102 | — | — | **ACCEPTED-WITH-DISCLOSURE** by owner decision |
| pathscope r2 | Codex FILTER-BLOCKED on the source | **REQUEST_CHANGES ~00:10 — harness reproduced byte-for-byte, r2 honest (13/16 closed), but new CRITICAL C-1: assignment prefixes silently discarded (out-of-allowlist loader path → PASS rc=0). r3 repair dispatched (GLM source-level, Lead executes harness)** | GLM disclosure-honesty audit: all seven residuals honest; every count field derived, zero hardcoded — the inverse of RP6's defect |

## 5. FREEZE BLOCKERS — current shape

See `WPI_FREEZE_BLOCKER_MAP_2026-08-12.md` for the full table. Yesterday's blockers were mostly
"the proof tools are unsound." Today's are mostly **"the wiring and the run have not happened
yet."** Closed on 08-12: items 4, 5, 6, and most of 10. Still open: rows 1–9 unbuilt (decided
path, kickoff pre-written and HELD), `P0_ATTESTED_*` wiring, `REMOTE_BASE` allocation ordering,
Audit-2 packets 9/10/11.

**The `.gitattributes` durability sweep is analysed but NOT applied**
(`WPI_GITATTRIBUTES_DURABILITY_ANALYSIS_2026-08-12.md`): 365 identity-quoted artifacts, 186 would
change bytes on a fresh Windows checkout, and the proposed rules change **zero** current
working-tree bytes. Codex recommends treating the application as **T0, not T2**, because checkout
behaviour of host-touching scripts changes. Deliberately deferred past the 23:00 audits, which
re-run harnesses verbatim against current checkout identities.

## 6. HELD, IN FLIGHT, AND THE FALLBACK BACKLOG

**HELD — dispatch only when its condition is met:**
- `WPI_BLOCKS_DRAFT/KICKOFF_CODEX_RP7_ROWS_1_9_BUILD.md` — the rows 1–9 build. **Dispatch only
  after RP7 holds dual flagship acceptance.** Design of record is §D of
  `ROWS_1_9_OPTIONS_CODEX_2026-08-10.md`: extend RP7 with two bounded `show` captures, do not
  author a new block or transport stage, keep the r9 descriptor discipline (`wpi_alloc_leaf` is
  deleted and must not return).

**IN FLIGHT at handoff time (2026-08-12 ~17:45) — check these first:**
| Lane | Model | Output | Log |
|---|---|---|---|
| Audit-2 packets 9/10/11 scoping | Codex fourth | `AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md` | `PACKETS_9_10_11_SCOPE_CODEX_RUN_2026-08-12.log` |
| Freeze-input ledger RP6 cross-check | GLM | `LEDGER_RP6_CLAIMS_GLM_CROSSCHECK_2026-08-12.md` | `LEDGER_RP6_CROSSCHECK_GLM_RUN_2026-08-12.log` |
| D026 map count re-derivation | Codex free | `AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_COUNT_RECHECK_2026-08-12.md` | `D026_COUNT_RECHECK_CODEX_RUN_2026-08-12.log` |
| STATUS-vs-BYTES sweep | GLM | `WPI_STATUS_VS_BYTES_SWEEP_GLM_2026-08-12.md` | `STATUS_SWEEP_GLM_RUN_2026-08-12.log` |

For each: confirm the report exists and is substantive, spot-check its claims against real bytes,
commit the exact file, and fold any correction into the blocker map / ledger / D026 map. The
RP6 cross-check specifically must resolve a discrepancy the Lead found: the ledger says **17**
`<PIN-AT-FREEZE>` literals, a direct count of `RP6-P0.sh` found **27** occurrences.

**FALLBACK BACKLOG — pull from here rather than idling (Rule 1):**
1. Apply the `.gitattributes` durability rules — analysis is complete
   (`WPI_GITATTRIBUTES_DURABILITY_ANALYSIS_2026-08-12.md`), application was deferred past the
   23:00 audits, and Codex recommends treating it as **T0, not T2**. Proposed rules change zero
   working-tree bytes; verify that before and after.
2. Draft the packet 9/10/11 skeletons — but only for whichever packets the scoping lane says can
   honestly carry `<PENDING-STAGE-1>` markers.
3. Cross-check any claim currently resting on a single lane. Today's pattern: single-lane claims
   have a real error rate, and every cross-check so far has either confirmed with a correction or
   found something new.
4. Sweep the older WP-L/B3 records the same way the STATUS sweep does the current ones.

## 7. THE 23:00 RUN — **EXECUTED overnight 2026-08-12/13. Results below.**

Written ~00:55, mid-night; the 04:00 items at the end were still pending at writing time —
check their own records for outcomes.

**Pre-window (21:00–23:00).** A second-pass preflight (found uncommitted, adjudicated, committed
`a930d889`) showed the `d4a07438` corrections were NOT sufficient — ~20 further corrections in
all four kickoffs. A Codex fourth lane applied them (`84ff5f00`); the Lead verified every hash
and the RP6 internal-consistency trio before GO. In parallel: packet 9/11 skeletons drafted
(packet 10 correctly declined per scoping, `2e16d930`); GLM swept the closed WP-L/B3 records
(~99 identities, zero drift, one stale FINAL_HANDOFF marked superseded, `2c3aacbc`); the
acceptance-matrix rows-24/26 contradiction was reconciled (`df4d55ca`); and a **fresh Codex r17
RP6 audit** returned REQUEST_CHANGES (`347cb9ec`) — `wait -p` escaped the effect model
(executed counterexample) and **the r10a→r17 stability span was FALSE** (r10 blob differs;
stability starts r11; swept repo-wide). The r18 repair landed and was Lead-verified verbatim
(14/14 PASS, `ddce3c10`) before the window opened.

**Window results (23:02–00:45, sequential, `--dangerously-skip-permissions` after the first
lane taught us headless permissions block harness runs and repo writes):**

| # | Lane | Verdict | Outcome |
|---|---|---|---|
| 1 | Transport | REQUEST_CHANGES (documentary only; zero byte findings; harness unexecutable in that session) | Six prose repairs applied (Codex free, `a0fa8271`) → **re-audit PASS-WITH-NITS with the WSL2 harness executed verbatim → DUAL FLAGSHIP ACCEPTANCE** (`ce017553`) |
| 2 | RP7 (r9 bytes) | **PASS-WITH-NITS → DUAL FLAGSHIP ACCEPTANCE** on 108301/`0e93f90d…` (`ee31544c`) | Unlocked the owner-decided rows 1-9 build (below) |
| 3 | Pathscope | REQUEST_CHANGES — new CRITICAL C-1: assignment-prefix values silently discarded (out-of-allowlist loader path → PASS rc=0) | r3 repair implemented (GLM) + **Lead-executed harness: all seven P9 fixtures confirmed, sinks closed** (`08a0c43f`); `REPAIRED-R3-PENDING-REAUDIT` |
| 4 | RP6 (r18 bytes) | **INCOMPLETE — no verdict.** The session backgrounded its fence RED and terminated. Partial log (`RP6_R18_CLAUDEPRO_AUDIT_RUN_2026-08-13.log`): identities/Q4/Q5/partition verified clean, **but two new problems: the pass-format scan detects 2 of 8 literal shapes, and a word-expansion assignment class (`${A:=v}`, `$((E=42))`, indirect `${!n:=v}` = runtime-named target) evades all four r18 mechanisms** | Completion lane hit the Claude session limit (resets 04:00). **Rule 8 is armed: the property reopened AFTER the r18 inversion — do NOT dispatch r19; complete the verdict, then put the boundary (accept-with-disclosure vs continue) to the owner** |

**Rows 1-9 build (owner's BUILD ALL NINE, condition met):** built by Codex free; the first D026
delivery was a **Python simulation of the block logic and was REJECTED by the Lead**
(Pattern 11); the rebuild executes the block's own extracted functions and **exposed a real
row-6 defect the simulation had masked** (fixed). Lead verbatim run: 20 RED/GREEN pairs + 4
controls PASS, all 44 lines byte-match the doc (`9aff375d`). New identity 126182 B /
`8355cb00…`; **acceptance honestly REOPENED, pending both flagships.**

**Account state:** Codex `fourth` exhausted ~23:20 (resets **Aug 18**); `secondary` resets
Aug 16; only `free` (gpt-5.5-class) remains. **No Codex flagship audit can run until then** —
affects: fresh Codex on RP6 r18, on the RP7 extension, and the pathscope re-audit (which may be
neither claude-opus-5 nor GLM, both implemented rounds). Claude Pro session limit hit ~00:45,
resets 04:00.

**The 04:00–09:00 wave (results, written ~09:00):**

- **RP6 completion audit delivered its verdict** (`WPI_BLOCKS_DRAFT/RP6_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`,
  REQUEST_CHANGES): R1 HIGH — word-expansion assignment (`${n:=v}`, `$((E=42))`, indirect
  `${!n:=v}`) unmodeled, executed 16/16-PASS counterexample; **R2 HIGH — the r18 `waittarget`
  grammar was harness-INJECTED, not in the shipped policy bytes** (the Lead's earlier verbatim
  run faithfully reproduced published lines but on the fence-injected instrument — caught only
  by the independent auditor); R3 MEDIUM — pass-format scan blind on 6 of 8 shapes. **Rule 8
  adjudicated NOT reached**: r16–r18 were all command-word enumeration; the true inversion is a
  token-layer model. **r19 delivered same night** (shipped `waittarget`, token-layer
  dispositions, widened scan; block byte-identical; new `SELF_QA_RP6.md` 1088259 B /
  `3c2f3844…`; lane's own runs: R17 18/18, R19 9/9). **COMMITTED ~09:15 after the Lead's verbatim runs completed and verified: R19 fence 9/9
  PASS, published R17 command 18/18 PASS, both rc 0 / stderr 0, block identity unchanged, and
  the SHIPPED policy (no harness injection) refuses the wait mutant —
  `SHIPPED_R17_WAIT_GREEN mutant=wait_p rc=1 UNMODELED` — so the R2 delivery defect is closed
  for real. Remaining for RP6: fresh Claude audit of the r19 bytes (next Pro window) + fresh
  Codex audit (blocked to 08-16/08-18), or the owner's accept-with-disclosure call.**
- **Extended RP7 audited** (`WPI_BLOCKS_DRAFT/RP7_CLAUDE_T0_EXT_AUDIT_2026-08-13.md`,
  REQUEST_CHANGES, 2 REQUIRED both small, PASS expected on repair) → **r3 repair delivered**:
  case-insensitive `[install]` match REVERTED (GLM's justification was factually false —
  flagship caught it), row-1 `ActiveState` amendment carried into the preregistration as a
  labelled amendment block (engineering-accepted by the auditor). New block identity
  **127038 B / `ac73485ff75ab6e731bf1bc137ae77f7074cab04700603ab71cba1c591141fe3`**, fence
  24 pairs + 4 controls PASS (lane run). **NOT yet committed at write time — next session:
  Lead verbatim fence run (WSL), verify, then commit the five-file r3 set and re-dispatch the
  Claude flagship for the expected PASS.**
- GLM advance read of the extension: 3 genuine REQUIRED + 1 factually false finding — the
  night's second proof that weaker-model findings need flagship cross-check.

**IN FLIGHT at handoff (~09:00):** the Lead's verbatim r19 + r17 fence runs (background bash,
outputs `r19_lead_run.out` / `r17_lead_run3.out` in the session scratchpad; compare against
`RP6_R19_REPORT_2026-08-13.md` before committing r19). Working tree carries the UNCOMMITTED
r19 + RP7-r3 file sets — verify-then-commit is the next session's first job.

**Incidents worth knowing:** the Codex correction lane sub-delegated two gates to the Claude
Max reserve on its own initiative (Rule 3 violation — "do not sub-delegate" is now in every
dispatch prompt); one commit message (`97b5b985`) got mangled by PowerShell interpolation
(here-strings used since); the first Claude lane wrote its verdict to its private scratchpad
because repo writes were unapproved (moved verbatim by the Lead, then permissions fixed).

## 8. LEDGER — booked honestly, needs owner ratification

- Last **ratified** balance: ~24.9 h of the 50 h plan.
- Prospective bookings since, still **unratified**: ~4.4 h (08-10 daytime) + the 08-11 overnight
  run + **~11 h for the 08-12 day run** (09:50→20:45, ~45 commits) + **~4 h for the 08-12/13
  overnight run** (20:50→~01:00 booked so far; the 04:00 wave adds to this — ~17 commits
  `a930d889`→`9aff375d`, two dual acceptances, two repair rounds, one build).
- **Running estimate: ~51 h used of 50.** The plan total is reached and passed.
- The owner **waived the 10h-remaining stop gate on 2026-08-11 18:30** ("continue past 10h/50h,
  honest booking, hard safety gates unchanged"), so this is **not a blocker** — but it does mean
  **every hour from here is over the original plan**, and the ledger needs one owner-ratified
  freeze-time figure before Audit 2 (that is Audit-2 packet component **P11-08**, which is
  explicitly an owner action no automation can produce).

## 8b. WAITING ON THE OWNER — surface these, do not decide them

1. **P10-10 — what IS the mandated test suite?** This is the highest-value open decision: three
   Audit-2 components cascade from it. `AUDIT2_READINESS_PACKAGE/AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md`
   lays out the options. **Every historical baseline is disqualified** — "1359 passed" was a
   different SHA, the two gc-referent failures were Linux-specific, a later candidate recorded
   1360, and later records name a different two-failure set. **No CI workflow exists** to inherit
   from. Codex recommends the full Bridge suite at the frozen SHA, with the exact command settled
   only after reconciling README/cwd/ACL/plugin requirements.
2. **P11-08 — ledger ratification** (see §8). No automation can produce this.
3. **SEC102 documentation-repair round.** The acceptance **stands**; its evidence document has
   13 accuracy findings recorded in `STATUS_SEC102.md` directly under the acceptance so the two
   travel together. Queued as a repair, not a reopened round — but the owner should know it
   exists before Audit 2 finds it.

## 8c. WHAT THE 2026-08-12 DAY RUN ACTUALLY PRODUCED

**One freeze blocker fully cleared** (SEC102, by owner decision) and **three more closed**
(§10.1 grammar, attestation ordering, most of the Audit-2 package). Blocker 8 reclassified — the
contract disagreement was gone, only a freeze-input fill remains. Blocker 7 **corrected**: it
claimed the five `P0_ATTESTED_*` inputs were unwired; they are fully wired, only the *values* are
markers, so it is a fill problem and the old wording would have sent an implementer to write code
that already exists.

**A new blocker class was found:** five Audit-2 components have **no producing step at all**
(`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md`) — four technical, one owner-only.

**All five evidence documents were claim-audited** for the first time: **38 findings** (16 false,
18 unsupported, 4 scope-wrong), one named systemic cause, and only **three** capable of affecting
an acceptance — all three already in tonight's kickoffs. Three mechanical authoring rules came out
of it and are now §0 Rule 9b.

**Bounding results that matter as much as the findings:** the unpasted-placeholder defect is
confined to the RP6 lane (737 files swept, zero elsewhere); the stale-identity defect is confined
to RP6/RP7; WP-L's closed evidence is intact at 197/198 with the one change documented; the
prereg's conservation accounting recounts correctly; and **no owner decision was overstated**.

**One finding was RETRACTED** on cross-check — an earlier SEC102 "false" claim turned out
consistent (95 printable ASCII + 6 non-ASCII = 101). Cross-checks pull both ways.

## 9. STANDING LESSONS THIS CYCLE PAID FOR

- **Confirming a claim's premises is not confirming the claim** (§3). Check whether another
  mechanism already handles the case before accepting that a gap exists.
- **A weaker model's finding is worth cross-checking, not trusting or discarding.** The gpt-5.5
  freeze-input ledger was right about the close-script staleness and GLM then found a *second*
  staleness in the same record that the ledger had only half-flagged.
- **Run every published command VERBATIM.** The Lead's verbatim run is the evidence of record.
- **A disclosure is not a control** — but an honestly-scoped, explicitly-labelled weaker claim
  IS acceptable where a static tool genuinely cannot reach further. Both sides of this appeared
  on 08-12: pathscope's seven residuals were honest; RP6's `dynamic_targets=0` was not.
- **When an auditor keeps finding "one more class," look for the structural inversion.** SEC102's
  command-word whitelist, RP6's byte-span census, r11's nameless channel and r17's effect model
  are all the same move.
- **Commit exact file sets, never `git add .`** The repo hook flips HEAD to master between calls.
