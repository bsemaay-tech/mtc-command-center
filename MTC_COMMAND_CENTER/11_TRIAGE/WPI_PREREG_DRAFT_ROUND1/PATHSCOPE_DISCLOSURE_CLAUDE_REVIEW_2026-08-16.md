REQUEST_CHANGES

# T2 flagship review — Pathscope supplemental-use disclosure record

**Reviewer model identity:** `claude-opus-5` (Claude Code session). The kickoff
requires effort `xhigh`; the effort setting is a harness-side configuration I
cannot read from inside the session, so I state the requested discipline rather
than assert a measurement of it.

**Metering (UTC+3):** start `2026-08-16 08:13:30` — stop `2026-08-16 08:21:24`
(timestamp taken immediately before writing this file; both from
`TZ=Etc/GMT-3 date`). Elapsed ≈ 8 minutes.

**Subject:** `C:\tmp\lane_out\PD1_PATHSCOPE_DISCLOSURE.md` (103 lines).
**Snapshot:** `C:\RO`, detached `c84497c8`. Read-only everywhere; this file is
the only write.

**Verdict: `REQUEST_CHANGES`.** Five REQUIRED findings. None of them is a
paraphrase defect — the two mandated quotations are faithful (see §0) — and none
of them says the record is dishonest. They say the record understates the gap in
three specific ways, its forward rule is not mechanically enforceable as written,
and its propagation table misses live gate documents that would deadlock or
contradict downstream work if left as they are.

---

## 0. What the record gets right (stated first, because it is most of it)

- **REQUIRED-1 and REQUIRED-2 are quoted verbatim and in full.** Subject
  lines 26-35 against
  `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:505-514`,
  and subject lines 41-48 against the same file `:516-523`. Compared line by line
  after stripping the `> ` blockquote prefix: 10/10 and 8/8 lines match, including
  `2645`/`2685`, `1330`, `33 of 92`, `161 options`, `${LD_PRELOAD[0]:=…}`, `§10.1`,
  `§11.1`, `2084-2089`, `2349-2355`, `§3.3/§4`, `§12.3`, `separator_count + 1`.
  Method limitation disclosed in §3 below.
- **Every evidence citation I checked resolves and supports its sentence.** I
  opened audit `:3-6`, `:133-139`, `:139-163`, `:165-176`, `:178-184`, `:202-225`,
  `:240-297`, `:327-331`, `:333-357`, `:391-430`, `:432-437`, `:443-475`,
  `:571-591`, `:593-606`; owner decisions `:62-72`, `:74-82`; restricted-grammar
  scoping `:24-39`. The "0/2 blocks, 0/2 compositions, 100% rejected" claim in §6
  is exact (`PATHSCOPE_RESTRICTED_GRAMMAR_OPTION_SCOPING_2026-08-16.md:29-30`).
- **§2 correctly sources its "genuinely established" claims to the auditor's own
  re-measurement**, not the implementer's report — the audit says so itself at
  `:137` ("Not one number below is copied from the implementer's report").
- **Propagation search scope is complete at the repository level.** I re-ran it:
  outside `11_TRIAGE/` and `_AI_MEMORY/` there are **zero** `Pathscope` matches
  anywhere in `C:\RO`. Nothing was missed by looking in the wrong place; the
  findings below are about filtering, not about coverage of directories.
- **No sentence in the record grants anything.** I looked specifically for
  acceptance of code, authorization of a cycle, or conferred authority. §1 line 9
  and §5's edit column stay inside "record what the owner decided". The one place
  where an authority-relevant *consequence* is produced without being stated is
  REQUIRED-2 below, and that is an omission, not a grant.

---

## 1. REQUIRED findings

### REQUIRED-1 — the record never says which Pathscope bytes it governs, and the audited bytes are not the ones in this repository

`C:\tmp\lane_out\PD1_PATHSCOPE_DISCLOSURE.md:5-20` (§1 and §2).

§1 declares "Pathscope is a supplemental aid" with no identity. §2 pins its
established facts to commit `ec98cbd4d629d7e035f99da70d5e73fb7f610da1`. Those are
not the same object, and the difference is load-bearing:

- The audited Option C prover is **185272 B** on branch
  `codex/pathscope-accounting-redesign-20260815`
  (`PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:89-90`, `:56-58`).
- The prover actually present in this snapshot at
  `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py` is
  **137520 B** — measured by me — which is `R5_FROZEN` in the audit's own pinned
  table (`:126`), i.e. the pre-Option-C round-5 code, whose status file still
  reads `REPAIRED-R5-PENDING-FINAL-REAUDIT`
  (`WPI_PREREG_DRAFT_ROUND1/STATUS_PATHSCOPE.md:3`, identity at `:61-62`).

**Failure scenario.** A reviewer three weeks from now reads §1 ("supplemental
aid"), reads §2 ("pool text deduplication, the single-empty Boolean, RHS-wide
source union and missing dispositions are gone; F1, F2 and F3 as filed are
closed"), then runs the copy that exists in the repository. That copy is R5, on
which F1/F2/F3 are exactly the findings that were **open** — the audit's RED
fixtures `f1_command_words`, `f1_uri_bare`, `f2_provenance` are `r5_rc=0`
against it (`:181-184`). The reviewer's "supplemental" signal is then the *worse*
prover, with §2's clean bill of health attached to it. Nothing in the record
prevents this, and the record does not state that the audited bytes are unmerged.

### REQUIRED-2 — applying the propagation table literally closes prerequisite gate 2, which §1 says the record does not do

`PD1_PATHSCOPE_DISCLOSURE.md:9` versus `:73` and `:93`.

§1 line 9: "does not close any technical, evidence, freeze, audit, host,
deployment, or economic gate." But:

- `AUDIT2_FREEZE_PREREQUISITES.md:14` states gate 2 is **"OPEN ONLY ON PATHSCOPE
  WITHIN GATE 2"** and "Pathscope is the only remaining open sub-item in gate 2".
- `_AI_MEMORY/GLOBAL_HANDOFF.md:110-111` repeats it: "within prerequisite gate 2,
  Pathscope is now the **only open sub-item**".
- `NIGHT_CLAIM_VERIFICATION_2026-08-15.md:19-31` `CONFIRMED` the same claim from
  primary records.
- Table row `:93` instructs: "calculate gate 2 only from non-Pathscope
  prerequisites." Row `:73` instructs the same removal in `GLOBAL_HANDOFF`.

Remove the only open sub-item and gate 2 is satisfied. That is a gate closing as
a mechanical consequence of edits this record mandates, while the record's own
first page says it closes none.

**Failure scenario.** An operator applies the table, greps gate 2, finds no open
sub-item, and treats prerequisite gate 2 as SATISFIED — including its three
accept-with-disclosure adjudications (SEC102, RP6, and now Pathscope), none of
which is a clean acceptance (`NIGHT_CLAIM_VERIFICATION_2026-08-15.md:29-30`). The
record needs one explicit sentence stating what gate 2's state becomes and on
whose authority, or an explicit statement that gate 2's residual is left
`UNKNOWN` pending an independent re-derivation.

### REQUIRED-3 — the forward rule is not mechanically enforceable in the two ways that matter

`PD1_PATHSCOPE_DISCLOSURE.md:56-62` (§4).

The exact sentence exists and is quotable — that half is done properly. Two
defects remain.

(a) **The rule's universe contradicts §5's universe.** §4 line 58: "Every
downstream document that mentions Pathscope must carry this exact sentence."
`Pathscope` occurs **4191 times across 226 files** under `11_TRIAGE/` plus 36
across 5 files under `_AI_MEMORY/` (my count, read-only). §5 lists 27 targets and
explicitly excludes audit transcripts and historical reports (`:66`). A compliance
check therefore cannot decide, from the record alone, whether a file without the
sentence is a violation or an intentional exclusion.

(b) **Presence is not the property being enforced.** The rule is written as
"carries this sentence"; the prohibition it means is "contains no Pathscope gate
input" (`:62`). Those come apart. Row `:88` even instructs a document to "Replace
checklist C3 with the mandatory sentence" — while
`STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:208` currently reads "C3:
Pathscope Option C exact bytes have one executing accepting audit and zero
required repair."

**Failure scenario.** A later runbook carries the mandatory sentence in its
header and keeps a Pathscope acceptance predicate in its checklist body. A grep
for the sentence returns "compliant"; the gate survives untouched. This is the
project's own recurring defect — a check that passes without proving the thing it
claims (`SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:12`, `:50`). What would make
this check fail? Only a typo in the sentence. Making it real needs a stated
forbidden form (e.g. "no document may condition any gate, step, checklist row or
estimate on a Pathscope verdict") and a named universe, so a violation is
detectable without a human reading the whole file.

### REQUIRED-4 — §2 omits the auditor's own "what I could not verify"

`PD1_PATHSCOPE_DISCLOSURE.md:11-20` (§2).

Owner decision §6 requires the record to state "precisely what is not proved"
(`OWNER_DECISIONS_2026-08-16_MORNING.md:66-67`). §2 lists what is established and
closes with a limit about the admission boundary only. The audit's §7
(`PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md:614-639`) lists seven things the
auditor could not verify; the record carries exactly one of them (the
`${NAME[0]:=v}` bash semantics, at `:39` — correctly). The omitted ones bear
directly on §2's own bullets:

- The published PowerShell harness was **never executed verbatim**; its `throw`
  paths, `Assert-Sha256`, the transcript-leak assertion, and
  `OUTER_RC=0 STDOUT_BYTES=7661 STDERR_BYTES=0` are **unconfirmed** (`:616-623`).
  The reproduction §2 relies on came from a Python re-implementation.
- No Python 3.12 interpreter exists here; everything ran on CPython 3.14.2
  (`:624-627`).
- The attack batteries are ~90 fixtures and explicitly not exhaustive, "particularly
  for REQUIRED-1 route (c)" (`:637-639`).

**Failure scenario.** A freeze or identity record cites this disclosure's §2 for
"the published harness reproduces byte-exactly" and pins the harness as validated
evidence, when the harness's own control flow has never run. §2 as written is the
sentence someone would cite.

### REQUIRED-5 — three live documents that gate on Pathscope are missing from the propagation table

Re-run search (read-only, case-insensitive, `11_TRIAGE/` + `_AI_MEMORY/`,
cross-checked against the 27 listed rows):

1. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:197-199`
   — "Audit 2 can honestly begin only after final post-repair RP6, rows 1-9/RP7,
   transport, SEC102, **pathscope**, and successor artifacts hold their required
   accepting reviews"; also `:20` and `:205-210` ("pathscope still has pending
   review work"). This document carries no supersession banner, is a maintained
   `[refreshed 2026-08-12]` readiness assembly, and sits in the same directory as
   four other rows the table *does* list. **Failure scenario:** under §6 Pathscope
   will never hold an accepting review, so this sentence makes Audit 2
   permanently undispatchable — a deadlock created by leaving the file alone.
2. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_PATH_SYNTHESIS_2026-08-15.md:130` — critical-path
   row 1 is "Pathscope disposition implemented and accepted | 6-10 [h]"; `:76`
   calls it the chain's first row; `:126` assumes Option C. Its correction banner
   (`:3-29`) refutes the §4 *total* and contests §1's parallelism claim but never
   touches the Pathscope row, and `_AI_MEMORY/GLOBAL_HANDOFF.md:114-115` still
   sends readers to this file for "two deploy findings that move the schedule".
   This is the same class as `BRIDGE_VPS_DEPLOY_READINESS_REFRESH` and
   `DEPLOY_ESTIMATE_REGISTER`, both of which are listed. **Failure scenario:** the
   next schedule is built from a critical path whose first row is a disposition
   the owner already took off the critical path.
3. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:32-33`
   — the Pathscope rows still record "Acceptance still missing: **Fresh flagship
   execution acceptance**" and an r3-repair-then-re-audit next step. This file is
   cited **by name** inside `AUDIT2_FREEZE_PREREQUISITES.md:14`, which is itself
   row 24 of the table, so it meets the record's own inclusion criterion ("targets
   still cited by those records"). **Failure scenario:** row 24 is edited to point
   at §6, an auditor follows its citation one hop, and lands on an unedited matrix
   that says a fresh accepting audit is still owed.

---

## 2. NIT findings

- **NIT-1** `:15` — "the relevant checks use independent inputs". The audit's
  claim is narrower: "the checks **that would catch their return**" (the R5
  defects) use independent inputs (`:571-576`). REQUIRED-2 is precisely a check
  the design designated independent and that is not. "Relevant" is undefined and
  a hurried reader can generalize it.
- **NIT-2** `:7` — "Its output may inform review". On the known bypass the tool
  does not merely stay silent; it emits a positive clean bill of health, in one
  case with `PATH value=/safe/f verdict=ALLOW-LEXICAL … PATHSCOPE verdict=PASS
  rc=0` attached (`audit:271-281`). A sentence saying a `PASS` carries **zero**
  evidential weight on the admission-boundary property — not merely "not proof" —
  would close the gap between §1's permission and §3's content.
- **NIT-3** `:100` — "Five cycles were completed" cited to `audit:590-591`, which
  actually says "the fifth appearance of one pattern". The claim is true and the
  cleaner primary is `PATHSCOPE_OWNER_BOUNDARY_2026-08-16.md:66`, which the record
  already cites elsewhere.
- **NIT-4** `:89` — the D026 row edit says "exclude them from closure totals" but,
  unlike rows `:84` and `:85`, does not require the affected totals to be
  re-derived or labelled `UNKNOWN`. A closure count can silently improve.
- **NIT-5** `:66` — the scope paragraph gives exclusion *criteria* but no
  exclusion *list*, so a reader cannot tell whether these were considered and
  excluded or simply not seen:
  `NEW_CHAT_HANDOFF_2026-08-15_AFTER_RP7_ACCEPTANCE.md:30,33` ("Cannot start until
  Pathscope is accepted" — banner-covered, but still the entrypoint named by
  `_AI_MEMORY/START_HERE.md:3-5` and `_AI_MEMORY/ACTIVE_FILES.md:5`),
  `STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:81` ("Stage-1 remains blocked
  until Pathscope closes" — V1, superseded by the listed V2),
  `DEPLOY_WORK_BREAKDOWN_2026-08-15.md:40-41,117` (V1, conserved into the listed
  V2), `AUDIT2_D026_RED_LOCATIONS.md:47` ("the fresh flagship execution audit …
  [is] pending"). I judge each of these individually defensible to exclude; naming
  them costs one line and removes the ambiguity.

---

## 3. STOP / UNEVALUATED — stated, not silently passed

1. **Byte-level equality of the two quotations was verified by line-by-line human
   comparison, not by a diff tool.** This session's policy refused, in four
   distinct forms, every mechanical comparison I attempted: bash process
   substitution (`Contains process_substitution`), `awk` over the two files
   (`requires approval`), `md5sum`/`cat -A` (`requires approval`), and PowerShell
   `Get-Content` + `-cne` compare (`complex path expression … requires manual
   approval`). I read both ranges in full and compared them token by token; the
   result is 18/18 lines identical. What this method would **not** catch: a
   zero-width character, a homoglyph, or a non-breaking space substitution. If the
   lane wants a byte-level guarantee, it needs a session whose policy permits one
   `diff`/`Compare-Object` call.
2. **9 of the 27 propagation rows had their "what it currently says" column
   verified against the cited lines** — `START_HERE.md:7-9`,
   `ACTIVE_FILES.md:13-22`, `SESSION_LOCK.md:63-65`, `GLOBAL_HANDOFF.md:110-111`,
   `NEXT_STEPS.md:21-25`, `AUDIT2_FREEZE_PREREQUISITES.md:14`,
   `STAGE1_TO_AUDIT2_RUNBOOK_V3_PATCH_2026-08-16.md:208`,
   `NIGHT_CLAIM_VERIFICATION_2026-08-15.md:21-31`, `STATUS_PATHSCOPE.md:3`. All
   nine are accurate. **The remaining 18 rows' line anchors and paraphrases are
   `UNEVALUATED`** — a wrong anchor there would be a defect I did not look for.
3. **The correctness of the flagship audit itself is out of scope.** I treated
   `PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md` as the source of record and
   checked only whether the disclosure represents it faithfully. I did not re-run
   the prover, the composite, the QA runner, or any fixture.
4. **The propagation edits are `UNEVALUATED` as applied**, because they do not
   exist yet. My REQUIRED-2 is derived from the instructions' stated effect, not
   from an applied diff.
5. **Whether owner decision §6 is the right disposition is not reviewed.** It is
   an owner decision; the record implements it, and that is what I assessed.

---

## 4. Scope compliance

Read-only in `C:\RO` and `C:\tmp`; `C:\tmp\lane_out\AUD_PD1_VERDICT.md` is the
only file written. No repository file, index, ref, or Git state was modified — no
`add`, `commit`, `checkout`, `branch`, `stash`, `merge`, `push`. No repair or edit
was made to the subject: findings only. No sub-delegation — no `codex`, `glm`,
`gemini`, `hermes`, `cline`, or nested `claude` process was invoked, and no
subagent was spawned. No host, network, deployment, service, credential,
broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, or
economic action was performed or authorized.
