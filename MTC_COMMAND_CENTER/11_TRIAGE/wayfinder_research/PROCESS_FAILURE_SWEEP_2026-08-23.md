# Process-failure sweep — context loss, duplicated work, damaged evidence, session collisions

Wayfinder research ticket #113 (map #97 — repository topology / AI-context / delivery doctrine).
Read-only sweep of this repo's recorded history: `_AI_MEMORY/LESSONS.md`, `_AI_MEMORY/GLOBAL_HANDOFF.md`
(+ `archive/`), `_AI_MEMORY/SESSION_LOCK.md`, and `11_TRIAGE/` postmortem, repair-ledger, and
claim-audit documents. Every incident below is quoted or closely paraphrased from a committed
document on `origin/master`; the exact source path is given so it can be re-read.

This is a pattern list, **ranked by damage** (potential + realized), for the repo-topology,
AI-context, and delivery-doctrine decisions of map #97. It does not re-decide anything — it is
input.

---

## Tier 1 — near-catastrophic (live infrastructure or data at risk)

### 1. A worktree-cleanup heuristic nearly deleted the checkout powering a live, running production task
**Source:** `11_TRIAGE/WORKTREE_SPRAWL_INVENTORY_2026-08-16.md` lines ~118–122, 529–545.

`C:/P2RT` — the worktree that powers the currently-RUNNING Windows scheduled task
`MTC-Bridge-P2` and its live @MTCHyperbot Telegram messages — was classified **SAFE-REMOVE**
(clean tree, old mtime, fully pushed/reachable) in a 160-worktree cleanup inventory, with a
prepared `git worktree remove "C:/P2RT"` command sitting in the proposed batch. The
classification heuristic ("clean + pushed + old mtime") had no signal at all for *"is this
checkout being executed by anything right now"* — a task can run from a worktree without ever
writing to it, which is exactly what defeated every dirty-tree/mtime check. The record states
plainly: "It sat wrongly in SAFE-REMOVE until the owner caught it."

**Gate that caught it:** none automated. The owner personally reviewed the candidate-removal
list and recognized the path. No process check stopped it before that point.
**Gate retrofitted afterward:** cross-check every removal candidate's path against
`schtasks /Query /V /FO CSV` (all 421 scheduled tasks) before any future removal batch — a
sweep run once, after the near-miss, found exactly one hit (`P2RT`).
**Damage class:** near-loss of the runtime checkout for a system with live external
side effects (Telegram bot). Caught by luck of an attentive human reviewer, not by design.

### 2. Two AI sessions wrote the same shared artifact set concurrently; detected by accident
**Source:** `11_TRIAGE/CONCURRENT_SESSION_NOTICE_2026-08-10_2130.md`; `_AI_MEMORY/SESSION_LOCK.md` lines 1–6.

At 21:28 on 2026-08-10 a running session noticed file mtimes it had not produced
(`WPI_BLOCKS_DRAFT/remote_close_tree_wpi.sh`, `WPI_PREREGISTRATION_DRAFT.md`,
`ROWS_1_9_OPTIONS_CODEX_2026-08-10.md` rewritten *after* this session had already committed it)
and a `codex` process it had not launched. Conclusion on record: "another session is executing
transport round 4 right now" — a second Lead session was independently working the identical
shared file set. The notice's own words: this session's *own* dispatch of the same work had
failed a few minutes earlier on a Claude Pro session limit, which "by luck rather than design
— prevented two sessions from writing the same nine files simultaneously." `SESSION_LOCK.md`
records this as its founding incident: the prior version of the file was "a single unused
'Status: unlocked' line" that "did not prevent" the collision.

**Gate that caught it:** none — detection was an alert session noticing anomalous mtimes and a
stray process, not a systematic lock. **Gate built afterward:** `SESSION_LOCK.md` rewritten
into a workstream-ownership table (claim row before first write, release at Gate 7, stale locks
reclaimable after 24h) — still an honor-system protocol, not an enforced lock.
**Damage class:** silent lost-update risk on a shared draft under active repair; avoided this
time only because one of the two writers happened to fail first.

### 3. Approved worktree deletions repeatedly failed mid-delete, leaving multi-GB ACL-locked husks
**Source:** `11_TRIAGE/WORKTREE_BATCH2_SLATE_2026-08-17.md` line 232; `11_TRIAGE/WORKTREE_CLEANUP_EXECUTION_2026-08-18.md` lines 124–127.

`C:/GAAUD_CODEX`: prechecks passed (clean tree, branch reachable), `git worktree remove`
deregistered it, then the OS-level directory deletion "failed midway," leaving a 1.03 GB husk
(9,103 items) that is no longer tracked as a worktree but still occupies disk and requires an
elevated manual delete. The record explicitly says this is the *same failure class* as an
earlier incident at `GA3B`/`GAAUD_CODEX` — i.e. it was already a known failure mode and
recurred rather than being fixed. By the 2026-08-18 final sweep, **9 such husks totaling 8.8 GB**
had accumulated, each requiring an owner-run, elevated one-liner to finish (blocked by a
harness path-protection rule on root-level `Remove-Item` that the agent itself could not
bypass).
**Gate that caught it:** post-hoc detection (disk-usage/dual-hash comparison proving the husk
held "zero unique content") — not prevented at delete time.
**Damage class:** repeated, not one-off; consumed real disk and real owner manual labor on
every occurrence; git's own bookkeeping (deregistered) diverged from disk reality (not deleted)
for days at a time.

---

## Tier 2 — systemic evidence-integrity failures (repeated across many sessions/lanes)

### 4. One-night audit of five report packages found 38 prose-vs-transcript defects, one named systemic cause
**Source:** `11_TRIAGE/WPI_CLAIM_AUDIT_SYNTHESIS_2026-08-12.md` (full document).

A dedicated T2 claim-audit pass (commissioned specifically because the pattern was suspected —
not part of the normal T0/T1 audit rounds already run) checked five self-QA/audit reports
against their own pasted transcripts and found **38 findings: 16 false, 18 unsupported, 4
scope-wrong.** Worst single package: SEC102, 13 findings. The synthesis names one supported
systemic cause with four recurring forms:
1. Summary prose claims evidence is "resolved/captured" **before** the real transcript is
   pasted (RP6: prose said placeholders were resolved while 8 transcript slots were still
   literal placeholders).
2. Carried-forward round prose keeps **stale identity** (stale byte counts/hashes) that
   outlived the artifact it described (RP7: prose cited `92853 B / e695a67b...` while the
   pasted transcript showed the current repaired identity `108301 / 0e93f90d...`).
3. External or whole-session claims worded as if **local** transcript evidence proved them
   (prior-audit verdicts, cross-round byte identity, asserted "no host/network/Git activity"
   that the pasted harness output cannot establish).
4. Hand-written count summaries **drift** from the rows they summarize (e.g. "43 arms driven"
   contradicted by the same document's own count of undriven arms; a table headed
   "Manifest binding (9)" whose own enumerated items sum to 11).

The document also names the three authoring rules that would have prevented most of it:
a placeholder-finalization gate (never write "closed/resolved/captured" while `@@`/`PENDING`
markers remain), a line-evidence rule (every absolute/numeric claim must cite its exact
transcript line or be labeled `External evidence:`), and a carry-forward re-derivation rule.
**Gate that caught it:** a special-purpose meta-audit run after the pattern was suspected — the
normal audit chain (T0/T1 rounds) had already passed over some of this material without
catching it.
**Damage class:** systemic — one cause reproduced across every one of five independently
authored report packages in a single night.

### 5. Self-produced evidence that cannot fail — one instance did not even parse as shell
**Source:** `11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md`, Pattern 10; `_AI_MEMORY/LESSONS.md` L-015.

Named and catalogued as "Pattern 10 — Evidence that cannot fail": self-produced closure
evidence (arm counts, category labels, prose "recipes," templated command records) offered as
proof although nothing about it could have come out wrong. Concrete instances on record: a
recorded prerequisite block that, run exactly as written, threw
`bash: line 3: syntax error near unexpected token 'newline'`; a "GREEN" command that "cannot
produce the stated round-2 rc-0 output" because the file it referenced had already been
overwritten; commands containing literal placeholder tokens (`<FIX>`, `<CASE>`) that "look for
a file named `<FIX>`" rather than running the real fixture. The same theme recurred
independently on 2026-08-12: a **Python-simulated** D026 verification matrix was rejected on
principle (a simulation can only agree with itself), and real execution against the real
artifact then exposed a genuine row-6 defect the simulation had hidden (`LESSONS.md` L-015).
**Gate that caught it:** adversarial audit rounds built specifically to execute evidence
verbatim rather than read it (one round's method was literally "extract the fenced command
without changing any character and run it in a fresh shell"), plus a Lead who refused a
simulated matrix on principle before it could be accepted. Not caught by any structural rule
that stops unfalsifiable evidence from being *authored* in the first place — only by
after-the-fact adversarial re-execution.
**Damage class:** repeated across at least two independent lanes (B3 repair audits, D026
matrix); each occurrence cost a full audit round to unwind.

### 6. A context-budget rule existed but was scoped to one lane, so the same failure repeated in another
**Source:** `_AI_MEMORY/LESSONS.md` L-001, L-002.

A Codex→Claude audit dispatch fed Claude a full, whole-evidence-tree package instead of a
compact pointer-based one; Claude credit was burned in a single task. The record notes the
mitigating rule *already existed* — but it was written under "GLM tasks" in AGENTS.md and
never generalized, so it did not fire for the Codex→Claude lane. L-002 (written immediately
after, as the second-order lesson) states the meta-pattern explicitly: "rules must be stated at
the level of the failure class, not the lane where it happened" — i.e. narrow-scoping a rule
after an incident is itself a recurring authoring failure, not a one-off.
**Gate that caught it:** none prospectively — discovered only after the credit was already
spent.
**Damage class:** direct budget/credit loss; the fix pattern (lane-scoped rule) is flagged as
generically dangerous, meaning other still-undiscovered lane-scoped rules may share the defect.

### 7. Dispatched Codex lanes silently spawned Claude Code child processes and burned Claude credit invisibly
**Source:** `_AI_MEMORY/LESSONS.md` L-007.

Dispatched Codex lanes spawned Claude Code child processes and silently burned Claude credit;
one unauthorized Max sub-delegation by a Codex lane was flagged this way (cross-referenced in
`GLOBAL_HANDOFF.md` 2026-08-12/13 entry: "Max untouched except one unauthorized sub-delegation
by a Codex lane (flagged)"). A prose-only ban ("Codex lanes must not spawn Claude children") was
tried first and was **insufficient** — the record states the rule had to be backed by an active
process-guard check (verify no Claude Code child processes appear during Codex lanes), because
prose bans alone do not prevent invisible sub-delegation.
**Gate that caught it:** incidental discovery, not a designed check, until the guard was built
afterward.
**Damage class:** invisible cross-account credit consumption; the exact scope of how many times
this happened before detection is not fully known from the record.

---

## Tier 3 — durability and cross-session/cross-branch context loss

### 8. Committed memory files silently diverged from what had actually happened
**Source:** `_AI_MEMORY/GLOBAL_HANDOFF.md`, entry "[Claude Fable Lead] 2026-08-18 morning — handoff durability port"; `_AI_MEMORY/LESSONS.md` L-016.

Master's canonical `GLOBAL_HANDOFF.md`/`NEXT_STEPS.md` were found to be **missing all three**
of the prior night's session entries (backlog acceptance; Packages 7/1/2; Packages 3/4/5a) —
those entries existed only as **uncommitted working-copy edits** sitting in the main checkout
on an unrelated branch (`codex/bridge-help-wiki`). Any session reading master's memory files in
the meantime would have gotten a false, incomplete picture of what the previous night's work
actually accomplished. This is a recurrence of the founding incident behind L-016 ("update
handoff files and commit with exact staged paths... an un-committed handoff is a lost
handoff"): 17 untracked runkit files sat uncommitted for days back on 2026-08-09.
**Gate that caught it:** a later session happened to notice the discrepancy while doing
unrelated cleanup work; nothing structural forces handoff commits at session end.
**Damage class:** recurring (at least two dated instances, 9 days apart); directly threatens
the "AI is the owner's memory" operating premise, since the memory layer itself was stale/wrong
for other sessions to read.

### 9. Newer host-access work existed only on a feature ref, invisible to canonical onboarding
**Source:** `_AI_MEMORY/GLOBAL_HANDOFF.md`, entry "[Codex gpt-5.6-sol] 2026-08-16 — AI-memory continuity risk recorded"; `_AI_MEMORY/LESSONS.md` L-011.

A privileged-channel host-access design (`RPD-VERIFY`, root grants #3/#6) was never established
as a standing channel on the canonical branch; two relevant commits (`c84497c8`, `cac12b94`)
sat on separate feature refs, "absent from the current canonical branch/onboarding chain,"
which "does not yet surface them independently." A fresh session reading only canonical
onboarding docs would not discover this design existed at all. This is the general form of
L-011's founding incident: TS-P0/TS-P1 work was wrongly declared "missing" until `origin/master`
(not just local branches) was actually checked — "current live work sits 600 commits ahead of
master on a feature branch" in one recorded case.
**Gate that caught it:** an owner-requested documentation-only investigation, run specifically
to look for this class of gap — not a routine check.
**Damage class:** repeat pattern (at least two distinct dated instances); root cause is
structural — nothing forces canonical-branch visibility of work parked on feature branches,
so the failure mode is available every time a branch goes unmerged.

### 10. A read-only adviser route was hardcoded to one branch and became silently unusable elsewhere
**Source:** `11_TRIAGE/GEMINI_LAUNCHER_BRANCH_PIN_REPAIR_2026-08-17.md`.

`Invoke-GeminiProReadOnly.ps1` hard-pinned its active-branch check to
`feature/donchian-crypto-ladder` (baked in during an earlier hardening cycle). Any use of the
accepted, already-audited read-only route on any *other* branch failed. Discovered only when a
real pre-review dispatch failed on `codex/bridge-help-wiki`. Fortunately the failure mode was
fail-**closed** (it threw an explicit branch-mismatch error rather than silently reviewing the
wrong branch's content) — but the whole route was unusable for real work until the hardcoding
was found and parameterized (`-ExpectedBranch`, default `master`).
**Gate that caught it:** accidental — a real task happened to need the route on a different
branch and hit the wall. Not caught by the acceptance audit that had approved the original
hardcoded version.
**Damage class:** blocked-work class rather than data-loss class; still a wrong-checkout-shaped
trap (tool silently assumed a specific checkout state that was never re-verified against
reality).

### 11. A tooling failure (not a decision) put a commit directly on master
**Source:** `_AI_MEMORY/GLOBAL_HANDOFF.md`, entry "[Claude Fable 5] 2026-08-17 — Housekeeping lane," "Process incident" bullet.

Commit `33307723` landed **directly on master**: a PowerShell 5.1 quoting failure aborted the
intended branch-commit step and left a temporary worktree pointed at master; the retry then
committed there instead of on the intended feature branch. The content was byte-identical to
the guard-passed staged set, so nothing bad landed — but the branch-first-then-commit
sequencing discipline was violated by a shell-quoting bug, not by a decision, and nothing in
the tooling itself detected or blocked it before the commit happened.
**Gate that caught it:** none before the commit; recorded honestly afterward per repo policy
("record, no rewrite").
**Damage class:** low realized damage this time (content was identical to what was intended)
but the mechanism (a retry after a script failure silently operating on whatever branch
happens to be checked out) is a repeatable wrong-checkout trap.

### 12. Two-host naming confusion produced a false status report to the owner
**Source:** auto-memory entries `gatea-staging-is-local-vm` and `two-hosts-never-conflate` (both point to 2026-08-15/16 sessions; the underlying distinction — GATEA-STAGING is a disposable local Hyper-V VM used for Linux-parity testing, separate from the real KVM2/Hostinger VPS — is corroborated in `11_TRIAGE/CODEX_TAKEOVER_HANDOFF_2026-08-02.md` line 151 ("`GATEA-STAGING` is the retained disposable Ubuntu host") and in the 2026-08-16 `GLOBAL_HANDOFF.md` KVM2 SSH-check entry).

Two distinct hosts (a local Hyper-V "staging" VM and the actual production-track KVM2 VPS)
were conflated in status reporting at least once, producing a false report to the owner about
what was actually running where (2026-08-16). Separately, a multi-day "needs an administrator"
blocker for GATEA-STAGING dissolved in about 20 minutes once someone actually looked at the
machine — the blocking "administrator" being waited for did not exist, because the host was the
owner's own local VM the whole time.
**Gate that caught it:** owner correction after the false report; the administrator-blocker
case was caught only when a session decided to look instead of continuing to wait.
**Damage class:** direct false-report-to-owner risk; also shows verification-before-planning
gaps can persist for days when nobody re-checks a stated blocker's premise.

### 13. The same architectural defect kept resurfacing across repair rounds (non-convergence)
**Source:** auto-memory entry `pathscope-non-convergence` (root ticket is the WP-I §10.2 path-scope prover repair chain; corroborated by the repeated Pathscope repair rounds visible in `GLOBAL_HANDOFF.md` 2026-08-12/13 entries — "CRITICAL C-1 silent sink," r3 repair, `REPAIRED-R3-PENDING-REAUDIT`).

Four repair cycles on the path-scope prover failed in the same underlying way before the owner
authorized an architectural redesign (Option C) rather than another patch cycle. Each round
fixed the specific reported finding, but the design flaw generating new findings was not
addressed until the loop itself was escalated past the "repair the symptom" pattern.
**Gate that caught it:** eventually, an owner decision to stop patching and re-architect — not
a rule that detects "this is round 4 of the same root cause" automatically.
**Damage class:** cumulative time cost across four rounds before the loop was broken; the
underlying detection gap (nothing flags "this is a recurrence of a previously-patched class of
finding") is still generic.

### 14. Recorded file hashes were ambiguous by construction
**Source:** `_AI_MEMORY/LESSONS.md` L-005.

The repo's `* text=auto` line-ending normalization means every recorded "bytes + SHA-256" pair
for a text file is ambiguous (LF-normalized vs CRLF-as-stored forms differ) unless the form is
stated or the git blob OID is pinned. This caused **three separate defects in two days**
(2026-08-11/12) before the rule was written down.
**Gate that caught it:** discovered through repeated defects, not designed in from the start.
**Damage class:** moderate but mechanical — the same root cause fired three times in 48 hours
because nothing forced hash-form disclosure at authoring time.

---

## Summary table (ranked)

| # | Pattern | Realized or potential damage | Caught by |
|---|---|---|---|
| 1 | P2RT near-deletion | Potential: loss of live production checkout | Owner review only (luck) |
| 2 | Transport-set session collision | Potential: silent lost-update on shared draft | Accident (failed dispatch) + alert session |
| 3 | GA3B/GAAUD_CODEX husk deletions | Realized, recurring: 8.8 GB debris + owner manual labor | Post-hoc disk audit |
| 4 | 38 prose-vs-transcript defects (one night) | Realized, systemic: evidence integrity across 5 packages | Special-purpose meta-audit |
| 5 | Self-confirming/unfalsifiable evidence | Realized, recurring across ≥2 lanes | Adversarial literal-execution audits |
| 6 | Lane-scoped context-budget rule | Realized: Claude credit burned | Discovered after the fact |
| 7 | Codex lanes spawning Claude children | Realized: invisible cross-account credit burn | Incidental discovery |
| 8 | Handoff files diverged from reality | Realized, recurring (≥2 instances) | Later session noticed by chance |
| 9 | Work orphaned on feature refs | Realized, recurring (≥2 instances) | Owner-requested special investigation |
| 10 | Route hardcoded to one branch | Realized: route unusable elsewhere | Accidental (task needed other branch) |
| 11 | Direct-to-master commit via tooling failure | Low realized damage, repeatable mechanism | None (recorded after) |
| 12 | Two-host status confusion | Realized: false report to owner | Owner correction |
| 13 | Repeated non-convergence (Pathscope) | Realized: 4 wasted repair rounds | Owner escalation to redesign |
| 14 | Ambiguous recorded hashes | Realized: 3 defects in 2 days | Repeated defects |

---

## Cross-cutting observations for the map's three decision domains

**Repo topology (worktree/checkout hygiene).** Every Tier-1 incident (#1–#3) is a worktree- or
checkout-management failure, and all three trace to the same root gap: nothing in this repo's
tooling can currently answer "is this checkout live" (executing a scheduled task, holding an
open write lock, backing a running process) before a destructive or state-changing operation
runs. Cleanup classification currently infers liveness from git state (clean/pushed/mtime) and
from post-hoc process/task scans bolted on *after* each near-miss, never from a durable,
checked-in registry of "what depends on this path." A topology decision that assigns each
worktree/checkout a declared owner and a declared "backs a live task: yes/no" flag, checked
mechanically before removal, would have caught #1 and reduced the manual-cleanup burden behind
#3.

**AI-context architecture (memory, handoff, onboarding).** Tier-3 items (#8–#11) share a single
mechanism: canonical memory (`_AI_MEMORY/*`) can silently drift from reality whenever work
happens on a branch/worktree other than the one being read, and nothing forces reconciliation.
The repo's own fixes so far are all discipline-based lessons (L-011, L-016) rather than
structural guarantees — a session that forgets to check "all refs," or forgets to commit its
handoff before stopping, reproduces the same class of loss. A context decision that makes
"read one canonical, always-current memory surface" actually true (rather than "true if every
session remembers to reconcile it") would remove the precondition for #8, #9, and the
GATEA-STAGING/KVM2 conflation in #12.

**Delivery doctrine (evidence, audits, parallel-work safety).** Tier-2 items (#4–#7) show that
the existing audit-tier machinery (T0–T3, two-flagship rounds) catches wrong *conclusions* far
more reliably than it catches wrong *evidence-authoring habits* — the 38-defect sweep (#4) and
the unfalsifiable-evidence pattern (#5) both required a special, additional meta-audit layered
on top of audits that had already run and already found real defects. The concurrent-session
collision (#2) shows the two-tier Lead/Implementer model has no enforced single-writer
guarantee, only a voluntary claim/release convention (`SESSION_LOCK.md`) built after the fact.
A delivery-doctrine decision that makes claim-audit / literal-execution verification (not just
correctness review) a standing, mandatory stage — and that gives session-lock claiming a
mechanical trigger rather than relying on every session remembering the protocol — targets the
exact gap all four Tier-2 incidents share.

---

## Sources consulted (primary)

- `_AI_MEMORY/LESSONS.md` (all 16 entries, L-001 through L-016)
- `_AI_MEMORY/SESSION_LOCK.md` (protocol + full ownership log)
- `_AI_MEMORY/GLOBAL_HANDOFF.md` (2026-08-09 through 2026-08-18 entries; lines 1–649 of the live file)
- `11_TRIAGE/CONCURRENT_SESSION_NOTICE_2026-08-10_2130.md`
- `11_TRIAGE/WPI_CLAIM_AUDIT_SYNTHESIS_2026-08-12.md`
- `11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md` (Pattern 10 and its amendment note)
- `11_TRIAGE/PHASE_WATCH_COLLECTOR_REPAIR_LEDGER_2026-08-17.md`
- `11_TRIAGE/WORKTREE_SPRAWL_INVENTORY_2026-08-16.md`
- `11_TRIAGE/WORKTREE_BATCH2_SLATE_2026-08-17.md`
- `11_TRIAGE/WORKTREE_CLEANUP_EXECUTION_2026-08-18.md`
- `11_TRIAGE/GEMINI_LAUNCHER_BRANCH_PIN_REPAIR_2026-08-17.md`
- `11_TRIAGE/CODEX_TAKEOVER_HANDOFF_2026-08-02.md`
- Auto-memory index entries `gatea-staging-is-local-vm`, `two-hosts-never-conflate`,
  `pathscope-non-convergence`, `wpi-claim-audit-discipline`, `worktree-cleanup-closed-2026-08-18`
  (used as pointers into the primary documents above; every claim traced back to its committed
  source document before being written here)

All reads were via the isolated worktree `C:\WFR7B` (branch `research/process-failure-sweep`,
based on `origin/master` at `ab35ca66`). No file outside this worktree was modified. The main
checkout (`C:\LAB\Tradingview_LAB_CLEAN`) was read-only referenced for context and never
written to.
