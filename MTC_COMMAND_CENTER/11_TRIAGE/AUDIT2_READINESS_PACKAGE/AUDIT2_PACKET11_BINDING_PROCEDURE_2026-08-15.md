# Lane L5 — Packet 11 final binding, freeze-time ledger, order proof, and Packet 10 dispatch manifest

Status: **PROCEDURE DEFINITION ONLY — CREATES NO AUTHORITY, NO ACCEPTANCE, NO GATE DECISION,
NO INVENTED FIGURE.**

- Produced: 2026-08-15/16 night, lane L5. Repository read read-only at `C:\RO`, detached at
  `25564449`. No repository file was written, created, deleted, or modified; no index-locking
  Git command was run.
- Purpose: close work-catalogue rows **R18** and **R20** of
  `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md` (R18 at `:57`, R20 at
  `:59`) by defining the exact procedures those rows say must exist before they can be priced:
  R18 — "Time the final binding/ledger procedure after R15" (`:57`); R20 — "Estimate after the
  bundle schema and exact member list exist" (`:59`).
- Standing estimate rule applied throughout: a sourced range or an explicit
  `NO SOURCED ESTIMATE`, never an invented figure
  (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:33-35`).

## 0. Sources read, and what each establishes

| Source | What it establishes here |
|---|---|
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md` | Component definitions P11-01…P11-10 (`:79-88`), P10-10…P10-15 (`:62-67`), combined production order (`:106-122`), counting convention — one row per actual member (`:7`), Packet-11 gap P11-08 (`:90-92`). |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET11_SKELETON_2026-08-12.md` | The unfilled field set to be bound: final identity (`:24-30`), P11-01 fields (`:32-44`), P11-07 (`:124-134`), P11-08 approximate-ratification boundary (`:136-147`), P11-09 matrix (`:149-164`), P11-10 predicates (`:166-176`). |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md` | The authority-content record: 29 grant/decision rows (`:29-57`), 20 exclusion rows (`:66-85`), still-required decisions (`:93-97`), and the instruction that it is content, not final identity — "Re-bind it at the pre-WP-A freeze without changing authority by inference" (`:113`). |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET11_LEDGER_MEASUREMENT_2026-08-15.md` | The fixed measurement method (`:19-21`), reproduction command (`:31-67`), totals 31,497 s = 8 h 44 m 57 s over 38 commits / 10 sessions (`:84`), ~63.75 h composition (`:85`), no-remaining-subtraction rule (`:86`), limits (`:88-90`), signature sentence shape (`:92-94`). |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md` | Tonight's five decisions D1–D5; D3's ratified ~63.75 h and its re-presentation duty (`:62-78`); the post-decision blocker map (`:119-131`). |
| `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md` | R18/R19/R20/R21 row definitions and the ordering `R16 → (R17 ∥ R18) → R19 → R20 → R21` (`:100-101`, Ordering B `:123`). |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md` | Ordered gates 1–6 (`:13-18`), binding sequence incl. STOP rules (`:28-31`). |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md` | Live dispatch blockers (`:47-56`); the fact that the only sourced Stage-1 hour ranges end at the Stage-1 freeze and expressly exclude Packet 11 (`:86`). |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md` | The per-session input bundle (`:44-63`), isolated-worktree contract (`:65-80`), mandated-suite field block (`:91-100`), independence and verdict rules (`:16-18`, `:118-124`). |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md` | Checklist identity rows F1–F3, A2–A3, S2–S4, V1–V3 (`:57-83`); Packet 10/11 packet statements (`:180-193`). |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md` | Dispatch blockers still open for the Lead (`:34-39`, `:59-64`, `:72-77`, `:79-84`). |
| `MTC_COMMAND_CENTER/11_TRIAGE/PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md` | The unresolved plan-authority precedence question and its owner decision block (`:9-13`, `:162-166`). |
| `C:\RO\AGENTS.md` | Audit-tier table (`:37-38`), overlap and identity-escalation rules (`:40-42`), audit session contract — no implementer context (`:93-96`). |

## 1. R18 — Final binding procedure: re-binding the authority-content record at the freeze checkpoint

### 1.1 Position and precondition

The binding is a **freeze-time act** performed only after Packet 9 is complete and immutable and
the pre-WP-A checkpoint exists (combined order steps 12–14,
`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:119-121`; freeze prerequisites gates 4–5,
`AUDIT2_FREEZE_PREREQUISITES.md:16-17`). In the work catalogue this is after R15 and R16, in
parallel with R17 (`DEPLOY_WORK_BREAKDOWN_2026-08-15.md:100-101`). Nothing below may start
earlier; if R15/R16 products do not exist, the correct action is STOP, not a partial binding.

**Precondition check (step B0).** Before any binding step, verify and record:

1. The WP-I closure record (P9-17) exists and is immutable
   (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:41`).
2. The full pre-WP-A frozen checkpoint SHA **F** exists with its base/diff and frozen file list
   (P10-01…P10-03, `AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:53-55`).
3. The source of the binding is the existing content record
   `WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md`, which by its own terms is "the
   authority-content source, not the final frozen Packet-11 identity or proof"
   (`WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:113`).

### 1.2 Exact steps

**B1 — Content refresh, source-cited only.** Refresh the consolidation's content to the
freeze-time state. Every status change must cite the owner record that produced it; the
consolidation's own rule — it "does not infer authority from work having proceeded"
(`WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:6-9`) — binds the refresh too. Known
refreshes required as of tonight:

- The consolidation's §3 says of Pathscope "No option is currently exercised" (`:95`); D1 has
  since exercised **Option C** (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:8-24`). At freeze the
  Pathscope row must show the Option-C outcome: if the one fresh flagship execution audit
  accepted, the row is CONSUMED and freeze-prerequisite gate 2's last open sub-item closes
  (`AUDIT2_FREEZE_PREREQUISITES.md:14`, corrected 2026-08-15 text); if it returned a required
  finding, the lane is back at the owner boundary and R18 cannot complete its matrix — that
  state is an owner-decision blocker, not a fillable value
  (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:21-24`).
- The §3 host-and-credential question (`:96`) is now answered by D2's approved sentence
  (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:32-38`); at freeze the row records whether Commit 1
  and the allocation record were created and the grant then spent exactly against those bytes
  (`:41-52`).
- Add the five 2026-08-15-night decisions D1–D5 and any later owner records as new authority
  rows in their own right.

**B2 — Enumerate the authority-source manifest (P11-01).** One row per actual authority
source, per the scope's counting convention (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:7`).
The content universe today is: 29 grant/decision/waiver rows
(`WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:29-57`), 20 hard-exclusion rows (`:66-85`),
plus post-consolidation decisions (the five of 2026-08-15 night at minimum). Each row carries
the P11-01 fields: source path, date, exact scope, limits, present status, superseding record
if any, and the final path/bytes/SHA-256 binding
(`AUDIT2_PACKET11_SKELETON_2026-08-12.md:36-42`). **UNKNOWN:** the final cardinality — it
depends on owner decisions taken between now and the freeze; it cannot be pre-enumerated, and
must not be (the skeleton's own rule, `:44`).

**B3 — Compute the bindings.** For each source row:

- **In-repo sources** (decision records, kickoff prompts, handoffs, tier policy): hash the
  file's exact bytes **at the frozen SHA F**, not the working tree — e.g.
  `git show F:<path> | sha256sum` plus byte count. This is what makes the binding
  "final": the bytes are the frozen checkpoint's bytes, reproducible by any auditor from F
  alone.
- **Records outside the frozen tree** (run/evidence records, the future Packet-11 record
  itself, the owner ratification record): hash the final committed bytes at their recorded
  final path, and record that identity. This mirrors how the bundle already treats the WP-L
  closure and evidence-index records — handed by exact path, bound by digest, not members of
  the frozen SHA (`AUDIT2_AUDITOR_SESSION_INPUTS.md:57-58`; `AUDIT2_HANDOFF_PACKAGE.md:62`).
- Record for every row: final path, byte count, SHA-256, and the commit/identity at which the
  bytes were hashed.

**B4 — Fill the skeleton into the final Packet-11 record.** Replace each
`<PENDING-STAGE-1>` marker with the measured value for P11-01…P11-06, P11-07 (section 2
below), P11-09 (section 3), P11-10 (section 3). Keep the two marker classes distinct to the
end: technical `<PENDING-STAGE-1>` fills here; the owner-only P11-08 slot stays
`<PENDING-OWNER-RATIFICATION>` until R19, "so no technical marker impersonates owner
authority" (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:128`).

**B5 — Record the Packet-11 final identity.** Fill the skeleton's own pending header — root,
final manifest path, bytes, SHA-256, final status
(`AUDIT2_PACKET11_SKELETON_2026-08-12.md:24-30`) — from the completed record of B4.

**B6 — Two-way binding.** The Packet-11 record cites F; the Packet-10 dispatch manifest
(R20, section 4) carries the Packet-11 identity by path/bytes/SHA (P10-14,
`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:66`). Neither direction may cite an unbound or
working-tree value.

**B7 — Binding verification (mechanical, recorded).**

1. Every authority claim in the final record traces to a bound source row; zero unbound
   claims.
2. A diff of the final record against the 2026-08-15 consolidation shows only changes of the
   B1 class, each with its cited owner record — any uncited status change is a defect.
3. Recomputation proof: a third party, given F and the record, reproduces every SHA-256 by the
   B3 commands.
4. The stale-fill check: the skeleton's P11-08 currently records the superseded ~55 h figure
   (`AUDIT2_PACKET11_SKELETON_2026-08-12.md:136-147`); the final record must carry the
   freeze-time ratified figure from section 2, not ~55 h and not the 2026-08-15 snapshot by
   silent carry.

**Location note (constraint, not a decision).** The sources require the Packet-11 record to be
bound by path/bytes/SHA into the bundle (P10-14) and to bind F, but do not fix whether the
record lives inside the frozen tree or beside it. The procedure above assumes the
beside-the-tree evidence-record treatment (as the WP-L closure record is treated,
`AUDIT2_HANDOFF_PACKAGE.md:62`). Putting it inside F would be self-referential — the owner
ratification (R19) postdates R18 (`DEPLOY_WORK_BREAKDOWN_2026-08-15.md:101`) and would mutate
the frozen SHA. Final location is a Lead Gate-1 call; either way B6's two-way digest binding
is mandatory.

## 2. R18 — Post-WP-I ledger recalculation (P11-07) and the re-signature rule (P11-08 / R19)

### 2.1 What is already fixed and must not change

The method is fixed by the measurement record and must be reused verbatim
(`AUDIT2_PACKET11_LEDGER_MEASUREMENT_2026-08-15.md:19-21`):

- anchor commit `cf2d54c9c5631de10e62de011631babe10ada8e0` (the ~55 h ratification record's
  introducing commit, `:7`);
- committer (`%cI`) timestamps for every commit in the measured range;
- a gap **strictly greater than 90 minutes** starts a new session;
- session span = last timestamp − first timestamp; a one-commit session measures zero;
- total = anchor (~55 h, approximate, owner-ratified 2026-08-13) + measured span (exact under
  the method); the sum is approximate because the anchor is
  (`:84-85`).

The current ratified figure is **approximately 63.75 h**, signed tonight under D3 — "~55 h
owner-ratified anchor of 2026-08-13 plus 8 h 44 m 57 s of measured post-anchor commit-session
span across 38 commits in 10 sessions" (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:66-69`). D3's
own carry-forward: the figure "will drift as remaining WP-I work is booked"; "If the figure at
the real freeze checkpoint differs, it must be re-presented rather than silently carried"
(`:71-76`). The consolidation agrees: "Refresh the calculation at the actual Packet-11 freeze
checkpoint; use the quoted 63.75-hour sentence only if the refreshed figure is still 63.75"
(`WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:111`).

### 2.2 Recalculation procedure (exact steps)

**L0 — Precondition.** All remaining WP-I work is booked (freeze prerequisite gate 6,
`AUDIT2_FREEZE_PREREQUISITES.md:18`); Packet 9 closed; F exists. Otherwise STOP.

**L1 — Declare the cutoff.** Fix a cutoff commit **C_cut** by full hash and committer
timestamp, recorded in the refreshed measurement record. Recommended default (reversible,
loggable): the HEAD at the moment the recalculation runs — i.e. the last commit of the
freeze-preparation sequence that exists when L2 executes. The measurement window is then
`cf2d54c9..C_cut`.

**L2 — Run the reproduction command verbatim** with the new range, capturing full output
(`AUDIT2_PACKET11_LEDGER_MEASUREMENT_2026-08-15.md:31-67`). Do not modify the grouping logic,
the timestamp basis, or the display format.

**L3 — Compute the refreshed figure.** New measured span in seconds → HMS → hours
(six-decimal intermediate); figure = approximately 55 h + new span; display two decimals with
the word "approximately" (`:66`, `:84-85`). Produce the sessions table in the same shape as
`:69-80`.

**L4 — Write the refreshed measurement record** with: anchor section, method section,
sessions table, totals, and the limits section carried in substance — the reproducible result
is the commit-session span, not a claim of true labor hours (`:88-90`). Add one new mandatory
element: a **cutoff disclosure** naming C_cut and listing the known commits that exist after
it (at minimum the ratification record of L6 and the bundle manifest of section 4) as outside
the figure. This is the same honesty class as the existing limits section: the signature can
never contain its own committing session without regress, so the cutoff is declared rather
than hidden. If the Lead or owner prefers those commits included, rerun L1–L4 with the later
cutoff; the regress terminates because the ratified figure is always computed at a cutoff
that precedes the signature record.

**L5 — Compare to the last ratified figure** (currently ~63.75 h). Two outcomes only:

- **Identical displayed figure** → the existing D3 signature stands as the freeze-time
  ratification; P11-08 cites the D3 record and the refreshed measurement record together.
- **Different** → R19: re-present to the owner. The owner ratifies with a new dated sentence
  in the measurement record's own shape ("I, Barış, ratify approximately N hours used at
  Packet 11 freeze-time, based on the approximately 55-hour owner-ratified anchor plus H hours
  M minutes S seconds of measured post-anchor commit-session span", adapted from
  `:92-94`), naming the new span. The superseded ~63.75 h becomes a historical anchor exactly
  as ~55 h did (`WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:51`).

**L6 — Fill P11-07 and P11-08.** P11-07 gets: the anchor, the cutoff, every booked session,
the exact span arithmetic, ledger source paths, and the ratified-vs-booked distinction
(`AUDIT2_PACKET11_SKELETON_2026-08-12.md:124-134`). P11-08 gets: the ratified figure, the
ratification timestamp/source, and the owner's acceptance — with the skeleton's boundary
preserved verbatim in substance: an approximate ratification must never be laundered into an
exact one (`:136-147`).

**Remaining hours:** there is no valid remaining-hours subtraction from the 50 h plan
(`AUDIT2_PACKET11_LEDGER_MEASUREMENT_2026-08-15.md:86`;
`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:78`). P11-08's "remaining hours" field is filled
honestly as **not derivable by subtraction; remaining work is stated by gates** (the R-catalogue
owner/NO-SOURCED rows), never as 50 − used.

### 2.3 Re-signature rule (when a fresh owner signature is required)

A fresh ratification is required whenever **any** of the following holds:

| # | Trigger | Source |
|---|---|---|
| T1 | The refreshed displayed figure differs from the last ratified figure. "Differs", not "differs materially": D3's plain wording governs (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:74-76`); the "materially" phrasing appears only in the older ~55 h context (`AUDIT2_PACKET11_SKELETON_2026-08-12.md:145`), and under the narrower-reading rule the stricter duty wins (`WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:101-103`). The owner may attach an explicit tolerance in the same sentence when ratifying; the Lead may not assume one. |
| T2 | The anchor is superseded by a newer owner ratification of a different anchor figure. | Pattern: `WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:45`, `:51`. |
| T3 | The method changes (session-gap rule, timestamp basis, cutoff basis, display). Recompute and re-present regardless of whether the number moves. | Fixed method: `AUDIT2_PACKET11_LEDGER_MEASUREMENT_2026-08-15.md:19-21`. |
| T4 | The figure's scope changes (what counts as booked time is redefined by the owner). | Honest-booking duty carried unchanged in G2 and the waiver (`WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:30-31`). |

**Expected outcome, stated so it is planned for rather than discovered:** the 2026-08-15
measurement's last measured commit is `ddc8a9c802cc45f66f449b02f18a07448afc5f70`
(`AUDIT2_PACKET11_LEDGER_MEASUREMENT_2026-08-15.md:80`), and the repository HEAD at lane time
is already `25564449` — commits exist beyond the measured cutoff, and R15–R20 themselves add
more. The refreshed figure should therefore be **expected to differ**, and R19 should be
treated as the default path, with the D3 signature as a historical anchor unless the arithmetic
says otherwise.

## 3. R18 — Order/compliance proof (P11-10) and the final go/no-go matrix shape (P11-09)

### 3.1 Authority/order compliance proof (P11-10)

The proof is a mechanical comparison of the recorded action chain against the bound authority
sources and freeze order (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:88`). Each predicate
receives exactly one of **PROVEN (with citation)** / **NOT PROVEN** / **VIOLATED**. Any
NOT-PROVEN or VIOLATED row is a recorded STOP finding escalated to the owner — never papered
over, never converted by inference.

| # | Predicate | Evidence that proves it |
|---|---|---|
| 1 | Commit 1 preceded grant-#6 capture | P9-02 commit object ID and timestamp vs the P9-03 capture record's first field `attestation_prereg_commit=<COMMIT_1>` (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:26-27`). |
| 2 | Commit 2 consumed the bound capture before op 01 | P9-04 record: capture path/bytes/SHA inserted in every consumer, strict Commit-1 ancestry, preflight-emitted `wpi_prereg_commit=<COMMIT_2>` before op 01 (`:28`). |
| 3 | Ops 01–12 stayed inside granted read-only scope | The P9-07 per-op records (argv/stdout/stderr/rc for every op, `:31`) compared against the bound G1/G3/G6 scope rows (`WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:29`, `:32`, `:35`). |
| 4 | Host checks stayed inside granted read-only scope | P9-08/P9-09 immutable P0/RO logs and the op-06 bounded probe record (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:32-34`) against the same grant rows. |
| 5 | No excluded action occurred | Cross-check the complete action record (ops, commits, dispatches) against all 20 bound exclusion rows (`WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:66-85`). Silence is not authority (`:85`). |
| 6 | Packet 9 closed before the pre-WP-A freeze | P9-17 closure record timestamp strictly earlier than F's creation (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:41`, `:119`). |
| 7 | Audit 2 precedes WP-A | Dispatch records strictly earlier than the first WP-A authorization/preregistration/action (`AUDIT2_FREEZE_PREREQUISITES.md:30-31`; V3 row, `AUDIT2_HANDOFF_PACKAGE.md:83`). |
| 8 | Packet 10 binding waited for owner ratification | The bundle's Packet-11 identity row cites a ratified (not pending) P11-08 — "Packet 10 can bind Packet 11 only after that owner action" (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:121`). |

The filled P11-10 replaces the skeleton's all-pending block
(`AUDIT2_PACKET11_SKELETON_2026-08-12.md:166-176`) — which correctly states that none of it
can be filled from documentation before the host chain exists.

### 3.2 Final go/no-go matrix shape (P11-09)

The matrix is a Lead-produced artifact with a fixed schema and **no authority to convert a NO
into a YES** (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:87`). Shape — five blocks:

1. **Headline question:** "May Audit 2 dispatch?" — YES only when every row in blocks 2–4
   permits it and the honest-start condition holds
   (`AUDIT2_HANDOFF_PACKAGE.md:195-202`).
2. **Granted-actions availability:** one row per bound grant with its consumption status
   refreshed at freeze (CONSUMED / PARTLY CONSUMED / UNCONSUMED, vocabulary fixed at
   `WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:11-18`). Content seed: the consolidation's
   29 rows plus D1–D5.
3. **Exclusion standing:** one row per the 20 exclusions, each still IN FORCE unless a bound
   owner record carves it out (`:66-85`).
4. **Still-required owner decisions:** every action needing a fresh owner YES, each with its
   exact blocker/source. Known candidates as of tonight (to be re-derived at freeze, not
   carried blindly): the plan-authority reading
   (`PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:162-166`); the D5 archive sub-question
   (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:112-116`); the freeze-time ledger signature if
   T1–T4 fired (section 2.3); anything the Option-C audit outcome re-opens.
5. **No-silent-YES conversion check:** an explicit attestation line that no NO above was
   converted by inference and no missing authority was supplied by the document — the check
   the skeleton already applies (`AUDIT2_PACKET11_SKELETON_2026-08-12.md:164`).

Column schema for every row: `Question/Action | GO or NO/STOP or OWNER-REQUIRED | Exact
blocker or exact grant | Bound source row (path/bytes/SHA from B3) | The one sentence or
artifact that converts NO to YES`. Current-state inputs (not the final matrix): tonight's
blockder map — Pathscope authorized/Option C in progress; Audit-2 gate 2 open until the
Option-C audit accepts; the Stage-1 host step granted but precondition-unmet (Commit 1 first);
Packet 11 signed at ~63.75 h, re-present at freeze; wallet deferred; risk state fresh-reset
(`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:119-131`).

## 4. R20 — Packet 10 dispatch manifest schema (P10-15)

### 4.1 Publication gate

One authoritative dispatch manifest is published only after P10-01 through P10-14 are resolved
(`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:67`) — concretely: after R16 (frozen SHA F),
R17 (the P10-10/11/12 suite records — still open gaps today, `:69-71`), R18, and R19 (P11-08
ratification, `:121`). Any earlier publication is STOP (`:122`;
`AUDIT2_FREEZE_PREREQUISITES.md:30-31`).

### 4.2 Schema

One row per actual member; cardinalities are filled from the real artifacts, never
pre-enumerated (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:7`). Every member row carries
`path | bytes | SHA-256 | source role`.

| Block | Fields | Binds |
|---|---|---|
| M0 manifest header | manifest version; bundle root path; publication record; frozen SHA **F** (P10-01, repeated identically here and in each dispatch, `:53`); base SHA + exact base-to-freeze diff artifact (P10-02 — carried even when empty, with unchanged-bits only as the derived conclusion, `:100`); frozen file list (P10-03) | R16 |
| M1 identity bundle | candidate identity; every final artifact and manifest path/bytes/SHA-256; binding of each to F (P10-04, `:56`) | R16 |
| M2 payload | the actual diff and frozen file payload handed to each auditor, with no implementer-session context and no unfrozen working-tree substitution (P10-05, `:57`; `AUDIT2_AUDITOR_SESSION_INPUTS.md:44-49`) | R16 |
| M3 WP-L Phase-2 package | closure record, evidence index, accepted proposal/block identities, D026 records, open/BLOCKED registry, repair ledger, historical transport records, RUNID accounting (P10-06, `:58`) | pre-existing, re-hashed |
| M4 Packet-9 package | WP-I closure record, final evidence index, Commit-1/capture/Commit-2 ordering record, ops 01–12 records, rows 1–24 and immutable P0/RO trees — referenced by final path/bytes/SHA (P10-07, `:59`) | R15 |
| M5 acceptance/freeze evidence | exact-current acceptance matrix, completed freeze-input ledger, completed D026 map incl. rows 1–9, accepted section-10.1 grammar, accepted composite section-10.2 proof, final successor identity (P10-08, `:60`) | Stage-1/Commit 2 |
| M6 scope contract | frozen Audit-2 scope contract, adopted plan if any, required repository rules — identical for both auditors, explicitly excluding implementation, host action, WP-A (P10-09, `:61`) | frozen text |
| M7 **R17 baseline — suite definition** | `MANDATED_COMMAND`, `EXPECTED_EXIT_CODE`, pass/fail counts, every accepted failure test ID/signature, skip/xfail counts, `BASELINE_SOURCE` at F (P10-10 fields, `AUDIT2_AUDITOR_SESSION_INPUTS.md:91-100`) | **R17** |
| M8 **R17 baseline — execution record** | exact command, cwd/environment, stdout/stderr, rc, exact counts/test IDs/signatures, output bytes/SHA, proof the run used F (P10-11, `AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:63`) | **R17** |
| M9 **R17 baseline — anomaly register** | zero or more exact anomaly test IDs and output signatures, adjudication/authority for each, frozen baseline source; an empty set must be an observed/adjudicated result, never a hardcoded count (P10-12, `:64`) | **R17** |
| M10 worktree contract | the common isolated-worktree contract: separate worktree per flagship, exact-HEAD equality, pre/post empty `git status --porcelain`, allowed commands only, no edits (P10-13, `:65`; `AUDIT2_AUDITOR_SESSION_INPUTS.md:65-80`). Note: each auditor's *resolved* worktree path and cleanliness outputs are dispatch-time products of the audit sessions, not of this manifest (`:65`). | contract text |
| M11 **final Packet-11 identity** | the R18 final Packet-11 record and the R19 owner-ratification record, each by final path/bytes/SHA, so auditors verify the exact authority and freeze-time balance rather than an estimate (P10-14, `:66`) | **R18 + R19** |
| M12 dispatch events | one entry per flagship session: session id, model/effort (exactly fresh `claude-opus-5` xhigh and `gpt-5.6-sol` xhigh, `AUDIT2_AUDITOR_SESSION_INPUTS.md:11-14`), delivered bundle digest, delivered manifest digest, delivery timestamp, receipt record | R20 |
| M13 self-record | the manifest's own byte count; its SHA-256 is **not** written inside itself — it is recorded in each M12 dispatch entry and in each auditor's receipt, preserving acyclicity | R20 |

### 4.3 Identical-bytes proof for both auditors

1. **Assemble once.** The bundle and manifest are produced in a single publication act from F
   (P10-15: "One authoritative dispatch manifest… with the same manifest delivered to both
   flagship sessions", `AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:67`). Member order is fixed
   by manifest row order so the bundle rendering is deterministic.
2. **Deliver twice, record both.** Each of the two dispatch events records the delivered
   bundle digest and manifest digest (M12). The **equality of the two recorded digest pairs**
   is the primary proof that both auditors received identical bytes.
3. **Auditor-side recomputation.** Each session begins by recomputing every member SHA-256
   against its manifest row, recomputing the manifest digest against its dispatch entry, and
   verifying `git rev-parse HEAD == F` in its isolated worktree with empty pre-review
   `git status --porcelain` (`AUDIT2_AUDITOR_SESSION_INPUTS.md:69-72`). Any mismatch or
   non-empty cleanliness output is **BLOCK** (`:79-80`).
4. **Independent corroboration.** Both auditors' worktrees resolving to the same full SHA F
   (checklist F1, `AUDIT2_HANDOFF_PACKAGE.md:57`) independently proves both reviewed the same
   tree even before bundle digests are compared.
5. **Independence preserved.** Neither auditor receives the other's response, verdict,
   reasoning, or findings before both initial verdicts are sealed, and no implementer-session
   context is included (`AUDIT2_AUDITOR_SESSION_INPUTS.md:16-18`;
   `AGENTS.md:93-96`).

### 4.4 How the manifest binds R17 and Packet 11

- **R17:** M7–M9 carry the R17 outputs by path/bytes/SHA and pin them to F (the suite ran at
  the frozen SHA in the locked environment, per the D-SUITE decision — scope only, exact
  command settled at freeze prep, `WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:52`). This
  closes what the gap result calls the three undefined Packet-10 producers
  (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:69-71`) — the manifest can only index them
  after R17 actually produces them.
- **Packet 11:** M11 binds the final R18 record identity (section 1, B5) and the R19
  ratification record. Until P11-08 is ratified, M11 cannot be filled and the manifest cannot
  publish (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:121`).

## 5. Estimates

| Row | Estimate | Basis |
|---|---|---|
| **R18** (Packet 11 technical completion) | **NO SOURCED ESTIMATE.** | The catalogue row itself (`DEPLOY_WORK_BREAKDOWN_2026-08-15.md:57`). The only sourced hour ranges in the readiness chain are the Stage-1 steps R09–R14 (`AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:62-70`) — different rows, already priced there, and not reusable here (the breakdown's own overlap-removal discipline, `:167-169`). The reconciliation's bounded scenario expressly "ends at Stage-1 freeze" and "excludes … completion of Packet 11" (`:86`). **What would settle it:** timed execution of sections 1–3 at the freeze — per-step elapsed times recorded in the Packet-11 record — exactly as the row instructs ("Time the final binding/ledger procedure after R15", `DEPLOY_WORK_BREAKDOWN_2026-08-15.md:57`). |
| **R20** (dispatch manifest/bundle finalization) | **NO SOURCED ESTIMATE.** | The catalogue row itself (`:59`). The active plan's single 6 h shared reserve covers Audit 2 + Audit 3 + Gate 6 + all re-audits, is assigned to no row, and is excluded from subtotals (`:60`, `:177-179`) — it is not a price for R20. **What would settle it:** the exact member list (M0–M13 cardinalities filled from the real P9-16 final evidence index and P10-04 identity bundle) plus one timed assembly/publication dry run, per the row's own instruction ("Estimate after the bundle schema and exact member list exist", `:59`). This document supplies the schema; the member cardinality still cannot exist before R15–R17 do. |

Sub-observations that are not estimates: the binding's mechanical universe today is bounded
and known — 29 grant rows + 20 exclusion rows (`WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:29-57`,
`:66-85`) plus post-consolidation decisions — and the ledger recalculation is one verbatim
command run plus one comparison (section 2). Boundedness is not a price; no figure is asserted.

**Audit-tier classification inputs for the Lead's Gate 1 (not a verdict):** the tier table
maps docs/evidence work to T2 and dispatch packages/process artifacts to T3
(`AGENTS.md:37-38`); the overlap rule takes the highest applicable tier (`:40`); and any
finding that touches deployed-artifact identity — SHAs, candidate identity, release
manifests, i.e. exactly what R18/R20 produce — escalates that finding to a single-flagship T1
verification (`:41-42`).

## 6. UNKNOWNs and open items

| Item | State | What settles it |
|---|---|---|
| Final authority-source cardinality (P11-01 row count) | UNKNOWN — depends on owner decisions between now and freeze | The freeze-time enumeration of B2 |
| Refreshed freeze-time ledger figure | UNKNOWN — cannot exist before C_cut exists | L1–L4 at the freeze |
| Whether the Option-C audit accepts (gate-2 closure) | UNKNOWN and not this lane's to predict | The Option-C execution audit verdict (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:16-24`) |
| Plan-authority reading (cumulative vs KVM2-own-programme) | Open owner decision; affects which ordering the R-catalogue runs in, not the R18/R20 procedures themselves | One owner sentence from `PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:162-166` |
| Final location of the Packet-11 record (inside vs beside the frozen tree) | Constrained (B6 two-way binding mandatory either way) but not fixed by the sources | Lead Gate-1 decision; this procedure assumes beside-the-tree |
| R17 suite member identities | UNKNOWN — P10-10/11/12 remain producer gaps today (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:69-71`) | R17 execution at F |

## 7. Boundary

This document defines procedures only. It grants no authority, accepts no artifact, opens no
gate, and performs no host, network, deployment, service, credential, broker/exchange, ARM,
order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, or economic action.
It is material for the Lead and the owner; the only acceptance-relevant acts it describes —
the Option-C audit outcome, the R19 ratification, the Audit-2 dispatch decision — belong to
their named owners. Single output file: `C:\tmp\lane_out\L5_PACKET11_BINDING.md`.
