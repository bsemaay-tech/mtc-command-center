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
| RP6-P0 | PASS-WITH-NITS on **r16** | see §7 | Block byte-identical `5132bacd…` since r10a. Evidence doc moved to **r17** (1038848 B, `07cf843d…`) — **the r16 acceptance does not carry to those bytes** |
| RP7-WPI-RO | PASS (r9) | see §7 | GLM advance: PASS-WITH-NITS, zero required repairs |
| Transport set | PASS (r6b) | see §7 | GLM advance: PASS-WITH-NITS, zero required repairs. F1 owner-ratified accept-with-disclosure, NOT a blocker |
| SEC102 | — | — | **ACCEPTED-WITH-DISCLOSURE** by owner decision |
| pathscope r2 | Codex FILTER-BLOCKED on the source | see §7 (execution audit) | GLM disclosure-honesty audit: all seven residuals honest; every count field derived, zero hardcoded — the inverse of RP6's defect |

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

## 7. OVERNIGHT CLAUDE PRO RESULTS — **TO BE FILLED AFTER 23:00**

<!-- Fill: probe result; per-block verdicts for transport → RP7 → RP6(r17) → pathscope;
     which blocks reached dual acceptance; any repair rounds dispatched to Codex; whether the
     rows 1-9 build was released. -->

## 8. LEDGER — **TO BE FILLED**

<!-- Fill: honest hours booked for the 08-12 day + overnight, running total against the 50h
     plan, and the note that the owner waived the 10h-remaining stop gate on 08-11 with honest
     booking required. Last estimate was ~40h used. -->

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
