<!-- LEAD FINAL NOTE (Claude Lead, 2026-09-13 20:30Z) -->
> **P031 lifecycle decisions packet V4** — READY FOR OWNER DECISIONS. Source `C:/tmp/OPENCODE_SCRATCH_20260913/OC31/P031_LIFECYCLE_DECISIONS_V4.md` sha256 `bda1182ac69cc5aebf1f6d964caf37c55a757f990e25c523f8fa5395af298bbf`. Audit chain: V1 draft (Claude Max lane) -> Grok audit BLOCKING -> V2 (Claude) -> Grok re-audit CORRECTIONS_NEEDED -> V3 (Claude) -> Grok delta CORRECTIONS_NEEDED -> V4 (Grok text edit) -> Grok delta audit CLEAN (laneGK31D). Lead mechanical sweep: 408/408 citations resolve. Owner items OD-1..OD-12 unchanged in numbering. This supersedes the earlier DRAFT recorded in this folder. Nothing here is a decision, acceptance or authorization; every item is a question with a recommended answer.

# WP-P0-31 — remaining lifecycle decisions with recommended answers (DRAFT — V4)

Prepared 2026-09-13 by an independent drafting analyst lane (`claude-opus-5`, `xhigh`), read-only.
Corrected 2026-09-13 (**V2**) by a separate corrections-editor lane (`claude-opus-5`, `xhigh`),
read-only, against the independent Grok detection audit
`C:/tmp/CLAUDE_P0_RUN_20260913/laneGK31_grok_audit/GROK_AUDIT_REPORT.md`
(`GROK_AUDIT_VERDICT: BLOCKING`).
Corrected again 2026-09-13 (**V3**) by a third, separate corrections-editor lane (`claude-opus-5`,
`xhigh`), read-only, against the independent Grok re-audit
`C:/tmp/CLAUDE_P0_RUN_20260913/laneGK31B_grok_reaudit/GROK_REAUDIT_REPORT.md`
(`GROK_REAUDIT_VERDICT: CORRECTIONS_NEEDED`).
Corrected again 2026-09-13 (**V4**) by a fourth, separate corrections-editor lane (`grok-4.6`),
read-only, against the independent Grok V3 delta audit
`C:/tmp/CLAUDE_P0_RUN_20260913/laneGK31C_grok_v3audit/GROK_V3AUDIT_REPORT.md`
(`GROK_V3AUDIT_VERDICT: CORRECTIONS_NEEDED`).

**This document decides nothing.** It is a preparation artifact for the owner. It implements no
lifecycle semantics, accepts no package, ratifies no check set, authorizes no Git mutation,
integration, migration, retirement, deployment or trading, and creates no authoritative record.
Every "recommended answer" below is a drafting recommendation offered for the owner's decision;
until the owner records an answer, the candidate's existing fail-closed behavior stands unchanged.
Neither the V2 nor the V3 nor the V4 corrections change any recommendation, add a decision item,
invent a number or widen scope. V2 and V3 correct claims, citations and counts, and they extend
what is NOT VERIFIED. V4 corrects one leftover claim and does not shrink NOT VERIFIED.

Owner authorization for this lane (chat 2026-09-13): *"Prepare the remaining P031 lifecycle
decisions with recommended answers, without implementing new lifecycle semantics."*

---

## 0. V2/V3/V4 corrections

This packet has been corrected three times, by three separate corrections-editor lanes, against
three independent Grok detection passes. **No pass changed a recommendation.** Every recommended
answer in §2 and every row of the §3 approval table (OD-1..OD-12) stands exactly as the V1 drafting
lane wrote it. What the first two passes changed is claims, citations, counts and pin accuracy; what
they added is entries in §5 NOT VERIFIED. The third pass (V4) corrects one leftover claim and does
not shrink NOT VERIFIED. No pass decided anything and none is a review verdict.

### 0.1 Pass 1 (V1 → V2) — against the first Grok detection audit

Source of the findings: `C:/tmp/CLAUDE_P0_RUN_20260913/laneGK31_grok_audit/GROK_AUDIT_REPORT.md`
(auditor `grok-4.6`, independent detection only, verdict `GROK_AUDIT_VERDICT: BLOCKING`). That report
is a detection pass, not a review verdict; every one of its findings was re-opened against the cited
source bytes here before it was accepted or refused.

**Line-number mapping.** The Grok audit read the recorded copy at
`C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P031_LIFECYCLE_DECISIONS_20260913.md`,
which carries a five-line Lead audit header (`:1-5`) above the V1 text, so its "packet line" numbers
are the V1 draft's line numbers **+ 5**. The per-finding disposition for this pass is in
`C:/tmp/CLAUDE_P0_RUN_20260913/laneFX31_fix/DISPOSITION.md`; the line numbers in that file are
**V2's** and no longer match this one, because §0 grew in V3.

| Grok # | Severity | Disposition | What changed in V2 |
|---|---|---|---|
| 1 | BLOCKING | **FIXED** | §3's two closing count paragraphs are recomputed. OD-10 moves out of the "owner's word only" group: the test repair it is conditioned on changes reviewed test content, which under `P031_HANDOFF.md:126-131` voids the exact review set. "Two … cost nothing but the owner's word" is now OD-4 and OD-8 only, removing **two** envelopes (not three); "six … change reviewed executable bytes" becomes **seven … executable or test bytes**, including OD-10. OD-10's cost cell and Item 5(b) condition 1 say the same. Lead-verified against `P031_HANDOFF.md:126-131`. |
| 2 | CORRECTION | **FIXED** | OD-1's cost cell and option 3D now name `fold:9`'s fresh-G1-before-G1-IA recommendation and state that `DECISIONS.md` and the brief are two of the eight reviewed package paths (`reviews/P031_M1_REVIEW_PACKET_C76043B9.md:36`, `:41`). The bare `DECISIONS.md:18` is qualified to `C:/tmp/P031_M1_20260913/DECISIONS.md:18`, since `C:/CT13/DECISIONS.md:18` is `OD-20260911-MATERIALIZER-1`. |
| 3 | CORRECTION | **FIXED** | Envelope 7's reasons, Item 4's summary sentence and OD-8's cost cell no longer imply that ratification updates the report. `unresolved_lifecycle_contracts` (`ledger:1259-1267`) is seven hardcoded strings; dropping `ledger:1266` is an executable edit, i.e. a new candidate plus the full T0 roster. |
| 4 | CORRECTION | **FIXED** | §4's closing sentence is recomputed: owner answers close **six** of the seven envelopes; envelope 2 is not closable by any owner answer while `LifecycleEvent` has no challenged-incumbent field. |
| 5 | CORRECTION | **FIXED** | Envelope 2's 2B cell and reasons no longer claim that 2B *"contradicts"* `brief:2223`. That sentence describes what a ledger record names, and `check_set_version` — one of the four things it names — already lives in exactly the P031-local canonical-evidence channel 2B proposes (`ledger:191-209`) and is not a `LifecycleEvent` field (`execution.py:168-188`). 2A is re-grounded on `plan:320` and `G1_SCOPE_AND_CONTRACT.md:11`; the recommendation is unchanged. |
| 6 | CORRECTION | **REBUTTED** | Re-verified against the file as it stands now: `C:/tmp/CLAUDE_P0_RUN_20260913/laneP13M_dependency_map/P013_DEPENDENCY_ADOPTION_MAP_DRAFT.md:256` reads *"Status: **NOT_ADOPTED**, and P031 says so itself."* — it is not blank; `:255` ends the preceding grep paragraph and `:257` begins the `P031_HANDOFF.md:105` sentence. The V1 pin is correct and is kept, with a re-verification note. |
| 7 | CORRECTION | **FIXED** | Item 5(b) and OD-10 now cite `test:2192-2288`, not `test:2192-2286`, and describe the test accurately: its last statement is a `verify_integrity()` loop over three ledgers (`test:2287-2288`), so it proves non-raising appends and intact chains while pinning no purpose, version, hash or `current_state`. The exact Opus review's own wording (nit N-1, "no assertion at all", by AST scan) is attributed to it rather than restated as this lane's reading. |
| 8 | CORRECTION | **FIXED** | OD-11's cost cell and option 2C now name what 2C additionally costs: amending the frozen consumption sentence `G1_SCOPE_AND_CONTRACT.md:74` and the fixed constructor seam at `:20` (adjustable only under `:18`), and the fact that *"claims catalog-backed evidence"* is undefined here — read at its widest it would refuse every non-Registrar ladder append, because `ledger:631-632` requires an `evaluation_run_hash` on all of them. The undefined term is recorded, not defined; defining it would be new scope. |
| 9 | CORRECTION | **FIXED** | §3's admission sentence is corrected: OD-1..OD-11 are the owner-semantic rows, and OD-12 is admitted as the sequencing/authority call that only the owner may make (`P031_HANDOFF.md:41-43`; `P031_M1_FINAL_HANDOFF_C76043B9.md:134-135`), not as a definition. |
| 10 | CORRECTION | **FIXED** | Item 3's error-code mapping is corrected. `CHECK_SET_REQUIRED` (`ledger:610-611`) fires when the **event** omits the version; an event that carries a version the ledger has not configured active — including the case where **no** active version is configured at all — is refused `CHECK_SET_PURPOSE_MISMATCH` (`ledger:614-618`), because the active-set lookup defaults to the empty tuple. |
| 11 | NIT | **FIXED** | §3's governance note no longer attributes a grep hit to the D026 row: a case-insensitive search of `C:/CT13/DECISIONS.md` for `P0-31`, `P031`, `worthiness` and `lifecycle ledger` returns **zero** rows. The substantive claim (no P031 row in the shared tree) is unchanged and still true. |
| 12 | NIT | **FIXED** | Envelope 5 no longer says `_check_set_purpose` "stops being a pure function of `event_type`". It already reads `previous_state` for this very event type (`ledger:508-509`) and `writer_class` for `RESUMED` (`ledger:510-519`). What 5C changes is the input it reads and what determines the gate; it remains a semantic change. |

**Tally: 11 FIXED, 1 REBUTTED, 0 PARTLY FIXED.**

**Three further pin corrections found by this lane's own re-verification** (not Grok findings, no
claim changed):

1. `P031_M1_FINAL_HANDOFF_C76043B9.md:98-102` → **`:97-102`**. The same-epoch-test bullet begins at
   `:97`; `:98` is its continuation line.
2. `P031_M1_GEMINI_ADJUDICATION_C76043B9.md:43-45` → **`:44-46`**. Optional item 1 occupies `:44-46`;
   `:43` is blank.
3. Item 2's recommendation cited `ledger:271-279` for the `active_check_sets` seam. Those lines are
   the **writer allowlist** (`ledger:271-279`); the `active_check_sets` parameter is `ledger:269`,
   normalized at `ledger:280` via `ledger:306-330`. Corrected.

**What the pass-1 lane did and did not do.** It re-opened every source named by a Grok finding and
re-verified, against the files as they exist now, every `file:line` pin the packet touches plus a
broad sample of the pins it does not. It ran **no Git command of any kind**, no test, no script, no
D026 harness, no CLI and no network or provider call, and it wrote only the V2 packet and
`laneFX31_fix/DISPOSITION.md`. The §1 identity rows that the V1 drafting lane established with
`git rev-parse` / `git log` were **not** re-verified in that pass; see §5 items 13-19 for everything
it leaves unestablished.

### 0.2 Pass 2 (V2 → V3) — against the Grok re-audit

Source of the findings:
`C:/tmp/CLAUDE_P0_RUN_20260913/laneGK31B_grok_reaudit/GROK_REAUDIT_REPORT.md` (auditor `grok-4.6`,
independent detection only, verdict `GROK_REAUDIT_VERDICT: CORRECTIONS_NEEDED`). Its subject was
`P031_LIFECYCLE_DECISIONS_V2.md`, so the line numbers in that report are **V2's**. Like the first,
it is a detection pass and not a review verdict; every one of its findings was re-opened against the
cited source bytes before it was accepted or refused. The per-finding disposition is in
`C:/tmp/CLAUDE_P0_RUN_20260913/laneFX31C_fix3/DISPOSITION_V3.md`.

**Prior findings.** The re-audit re-tested all twelve pass-1 findings and records **12/12 RESOLVED,
none REGRESSED**, including the one this packet REBUTTED (Grok #6), which it accepts as validly
rebutted against the file as it stands now. It also re-opened the three extra pin corrections a/b/c
and records them as matching the files. No pass-1 finding is reopened in V3 and no pass-1 correction
is undone.

**New findings.** Three, none BLOCKING.

| Re-audit # | Severity | Disposition | What changed in V3 |
|---|---|---|---|
| NEW-1 | CORRECTION | **FIXED** | Envelope 3's option **3D** cell no longer says the interim ratification *"Leaves the envelope open on the acceptance list"* — the opposite of this packet's own recomputed count, of 3D's own reasons, of OD-4's row and of §4's close. **One position now stands everywhere:** ratifying the current repository-wide refusal (3D, recorded as OD-4) **closes envelope 3 on the acceptance list in its interim, stricter-than-design form**; what stays open is the *swap shape*, not the envelope. The cell now also records what ratification does **not** do, exactly as envelope 7's does: the report's disclosure line `"ATOMIC SUCCESSION PROMOTED ACROSS TWO CANDIDATES: UNRESOLVED"` (`ledger:1262`, one of the seven hardcoded strings at `ledger:1259-1267`) keeps printing until a separately authorized ledger edit. Two further places that still carried the old position were brought into line: Item 4's summary verdict row for envelope 3, and §4 item 2's heading, which read *"Two envelopes cannot be closed at all without new P0-04 contract fields"* while §4's own close named envelope **2** as the single exception. **No count changed:** OD-4 and OD-8 still remove **two** of the seven envelopes, and owner answers still close **six** of the seven. |
| NEW-2 | NIT | **REBUTTED** | **The source contradicts the finding, so the V2 pin is correct and is kept.** `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py:1237` reads, verbatim and as the file stands now, `"failing_checks": evidence["failing_checks"],`; `:1236` is `"evaluation_run_hash": evidence["evaluation_run_hash"],` and `:1238` is `"evidence_references": event["evidence_references"],`. Repinning `failing_checks` to `:1238` would put a false citation into an owner-facing packet. The re-audit's own sampled-citation row #50 says the same thing from the other side: it records `ledger:1234-1235` as `check_set_purpose` / `check_set_version` **EQUAL**, which forces `:1236` to be `evaluation_run_hash` and `:1237` to be `failing_checks`. The pin is kept with a re-verification note at the claim; the substance the finding concedes — that the report field is the stored tuple and is empty on every currently reachable path — was already the packet's claim and is unchanged. Limits in §5 item 22. |
| NEW-3 | NIT | **FIXED** | §4 item 4's parenthetical no longer groups B-17 with B-04 and B-12 under *"producer adoption"*. The P013 map records a different unsatisfied half for B-17 — *"receipt production and reader adoption NOT SATISFIED"* (`P013_DEPENDENCY_ADOPTION_MAP_DRAFT.md:355`) — against *"producer adoption NOT SATISFIED"* for B-04 (`:352`) and B-12 (`:353`). All three rows still read `Shape **RATIFIED**`, and no row's NOT SATISFIED status changes. |

**Tally: 2 FIXED, 1 REBUTTED, 0 PARTLY FIXED.**

**One further pin correction found by this lane's own re-verification** (not a re-audit finding, no
claim changed): §4 item 4 cited `P013_DEPENDENCY_ADOPTION_MAP_DRAFT.md:351-361` for the six
unsatisfied prerequisites B-04, B-06, B-07, B-12, B-15 and B-17. That range opens at `:351`, which is
**B-01**, and runs five rows past the six. The six rows are exactly `:352-357`; the pin is narrowed
to that.

**A Lead-noted item this lane did not fix.** NEW-2 reached this lane as an instruction to repin
`failing_checks` from `ledger:1237` to `ledger:1238`, under a standing rule that Lead-noted items are
to be fixed rather than rebutted. The file refutes it. Line 1237 **is** the `failing_checks` row, as
quoted above; it was read twice, by two independent tools, against the only copy of
`p031_lifecycle_ledger.py` found under `C:/tmp/P031_M1_20260913`, `C:/CT13`,
`C:/tmp/P031_LEAD_20260912`, `C:/tmp/P031_M1_START_20260912` and `C:/tmp/CLAUDE_TAKEOVER_20260913`.
Making the edit would have swapped a correct citation for the line that holds `evidence_references`,
which is the exact class of defect both detection passes exist to remove. The finding is therefore
recorded REBUTTED with its refuting bytes quoted, so the Lead can re-check it in one command and
overrule this lane if it reads the file differently.

**What this correction lane did and did not do.** It opened every source named by a re-audit finding
and every source cited by the lines it edited, and re-verified each of those `file:line` pins against
the files as they exist now. It changed no recommendation, added no decision item, invented no
number, widened no scope and removed no NOT VERIFIED entry: §5 gains items 20-22 and keeps items 1-19
exactly as they stood. It ran **no Git command of any kind**, no test, no script, no D026 harness, no
CLI and no network or provider call, and it wrote only this file and
`laneFX31C_fix3/DISPOSITION_V3.md`. The §1 identity rows still stand as the V1 lane established them;
see §5 items 13 and 20-22.

### 0.3 Pass 3 (V3 → V4) — against the Grok V3 delta audit

- **V4:** Item 1's coupling paragraph (V3 206-216) is rewritten so only envelope 2 waits on a new
  WP-P0-04 field; envelope 3 is closable now by owner answer **3D** / OD-4 in its interim,
  stricter-than-design form. Finding 1 of
  `C:/tmp/CLAUDE_P0_RUN_20260913/laneGK31C_grok_v3audit/GROK_V3AUDIT_REPORT.md`
  (`GROK_V3AUDIT_VERDICT: CORRECTIONS_NEEDED`). No recommendation, owner-item numbering, count or
  NOT VERIFIED entry changed.

---

## 1. Identity check

| Fact | Value | How established here |
|---|---|---|
| Worktree | `C:/tmp/P031_M1_20260913` | `C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:9` |
| Branch | `feature/p031-m1-20260913-refresh` | `P031_HANDOFF.md:10` |
| Frozen base / merge-base | `62a42514793f192ca4f706ca99cc2700b16300fe` | `P031_HANDOFF.md:11` |
| Candidate HEAD | `c76043b92c70c9f79a6d06630c0896ebe73e68a1` | **`git rev-parse HEAD` run in the V1 drafting lane — exact match. Not re-run in the V2 correction lane.** |
| Commits above base | 3 (`854ffea2`, `901f89bc`, `c76043b9`) | `git show --stat 62a42514..HEAD` (V1 lane) |
| Changed paths | 8 | `git show --stat 62a42514..HEAD` (V1 lane); `reviews/P031_M1_REVIEW_PACKET_C76043B9.md:34-43` |
| Working tree | clean; staged 0 | **Taken from `P031_HANDOFF.md:13` — NOT re-verified here.** No `git status` or `git diff` was run, per either lane's write boundary. |
| Current local `origin/master` | `fcac0ac67cf2682693ad28138b1a56e15a0846f2` | `git rev-parse origin/master` in the V1 lane; matches `P031_HANDOFF.md:14` |
| Divergence | 19 behind, 3 ahead | `git log --oneline HEAD..origin/master` / `origin/master..HEAD` counts in the V1 lane; matches `P031_HANDOFF.md:15` |
| Known upstream overlap | exactly `MTC_COMMAND_CENTER/03_QUANTLENS/HANDOFF.md` | `git log --oneline 62a42514..origin/master -- <path>` returns `e10936d4`, `a5515ff3`; `62a42514..HEAD -- <path>` returns `901f89bc`, `854ffea2` (V1 lane) |
| Disposition of the candidate | Lead **PASS-WITH-NITS** for bounded fixture engineering; Milestone 1 acceptance **NO** | `P031_M1_FINAL_HANDOFF_C76043B9.md:10-11` |

No Git write, status, diff, network call, test run or provider call was made by either lane.

---

## 2. The seven remaining items

The list under review is `P031_HANDOFF.md:104-116`, *"Full M1 acceptance still requires:"* items 1-7.
Each section below quotes the requirement, states what exists in the candidate today with
`file:line`, states what is missing, classifies the item, and — where it is an owner decision —
gives options with consequences and one recommended answer.

Classification vocabulary used here:

- **OWNER DECISION** — a definition or semantic choice that only the owner may make. Per
  `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1416`: *"Criteria changes are
  owner-gated; applications never are."*
- **ENGINEERING** — resolvable inside the existing accepted semantics under the same-package
  defect/repair authority (`C:/tmp/P031_M1_START_20260912/START_PROMPT.md:44`).
- **DEPENDENCY** — waits on another package's accepted provenance; no P031-side decision closes it.

---

### Item 1 — exact accepted WP-P0-04 lifecycle/identity/writer provenance

**Requirement, quoted** (`P031_HANDOFF.md:106`):

> "exact accepted WP-P0-04 lifecycle/identity/writer provenance"

**What exists today in the candidate.**
`p031_lifecycle_ledger.py:25` imports exactly two symbols:
`from mtc_contracts.execution import LifecycleEvent, LifecycleWriterClass`.
`contracts/mtc_contracts/execution.py:161-165` declares the four writer classes
(`REGISTRAR`, `ENVIRONMENT_ADMISSION_AUTHORITY`, `PROMOTION_AUTHORITY`,
`MULTI_WORKER_SUPERVISOR`). `execution.py:168-188` declares `LifecycleEvent` with thirteen declared
fields plus the inherited `contract_version` (`contracts/mtc_contracts/base.py:69`) — fourteen in a
`model_dump`. The ledger consumes these unmodified; `G1_SCOPE_AND_CONTRACT.md:11` binds it:
*"Reuse the current `LifecycleEvent` and all four `LifecycleWriterClass` values … do not edit shared
contracts."*

**What is missing.** Acceptance provenance, not source. `G1_SCOPE_AND_CONTRACT.md:73` states the
rule exactly: *"Current base contains the P0-04 `LifecycleEvent` and four writer classes; acceptance
provenance is not inferred from source presence."* Separately, WP-P0-04's declared Outputs include
*"eligibility-verdict and environment-admission record types"*
(`C:/CT13/.../MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:320`) — no such type
exists in `mtc_contracts/execution.py`, so the P0-04 surface P031 depends on is incomplete as well
as unpinned.

**Classification: DEPENDENCY.** There is no owner *semantic* question here. The owner action is
evidentiary: pin the exact accepted commit/tag and acceptance record for the P0-04 contract bytes
that `p031_lifecycle_ledger.py:25` imports. No answer to any other item in this document changes it.

**Coupling to be aware of.** One of the seven fail-closed envelopes (Item 4 envelope 2) cannot
be closed without a *new field* on the shared contract, which only WP-P0-04 may add
(`plan:320`, `G1_SCOPE_AND_CONTRACT.md:11`). Envelope 3 is closable now by owner answer **3D**
(OD-4) in its interim, stricter-than-design form; what stays open is the *swap shape*, not the
envelope. Specifically:

- Envelope 2 (`CHALLENGE`): no field carries a challenged incumbent identity — a repository-wide
  grep of `contracts/mtc_contracts/` for `incumbent`/`challeng` returns zero matches. The owner's
  answer to envelope 2 is an answer about *what WP-P0-04 must add*, not about what P031 may build
  today, and **no owner answer closes this envelope**.
- Envelope 3 (succession): `family_id` exists in the contracts package (`identity.py:144`,
  `package.py:31`, `trials.py:22`) but **not** on `LifecycleEvent` (`execution.py:168-188`).
  Ratifying the current repository-wide refusal the candidate already implements, under **3D** /
  OD-4, closes this envelope on the acceptance list now; the design's family-scoped rule remains
  blocked on WP-P0-04.

---

### Item 2 — exact accepted WP-P0-13 TrialRecord/catalog provenance actually consumed by P031

**Requirement, quoted** (`P031_HANDOFF.md:107`):

> "exact accepted WP-P0-13 TrialRecord/catalog provenance actually consumed by P031"

**What exists today in the candidate: nothing consumed.** The independent P013 lane established this
mechanically (`C:/tmp/CLAUDE_P0_RUN_20260913/laneP13M_dependency_map/P013_DEPENDENCY_ADOPTION_MAP_DRAFT.md:244-256`):
a word-boundary grep for `compute_evaluation_run_hash`, `make_trial_id`, `compute_family_id`,
`make_candidate_id` and the rest in `p031_lifecycle_ledger.py` returns **zero matches**, and
`TrialRecord`, `ArtifactManifest`, `trial_catalog` and the other P013 symbols hit only the contracts
package's own pre-V2 `trials.py` and planning prose anywhere in the P031 worktree. Its verdict:
*"Status: **NOT_ADOPTED**, and P031 says so itself"* (`:256` — pin re-verified in V2 against the file
as it stands now; Grok #6 rebutted, see §0.1). `G1_SCOPE_AND_CONTRACT.md:74` agrees:
*"No real TrialRecord bytes are consumed in this slice."*

What the ledger holds instead is an opaque `evaluation_run_hash` — validated only as a lowercase
SHA-256 string (`p031_lifecycle_ledger.py:30`, `:443-447`) — plus `evidence_references`, which
`execution.py:182` types as `tuple[NonEmptyStr, ...]` with no structure at all. Nothing dereferences
either.

**What is missing.** Two different things, and they should not be conflated:

1. **Accepted P0-13 provenance.** Not available. `P031_HANDOFF.md:118-121` is explicit that the
   `da1fb184c71e1ae65e2e348758af7f1a84a1cfbd` notice *"grants no caller integration/full-P013
   acceptance and is not in this candidate. Do not infer dependency satisfaction."*
2. **A consumption seam.** M1 has none, and the plan does not require one. WP-P0-31's Outputs
   (`plan:650`) name the ledger, the append interface, the derived view and the Registrar; they name
   no TrialRecord field. WP-P0-13 appears only as an *Input* (`plan:649`, `plan:661`).

**Classification: DEPENDENCY, containing one owner scoping question.**

The dependency itself is not decidable here. But the phrase *"actually consumed by P031"*
(`P031_HANDOFF.md:107`) sets an acceptance bar that M1's own contract never designed a place for,
and that gap is a decision.

| Option | Consequence |
|---|---|
| **2A** — M1 acceptance requires P031 to dereference catalog rows for every `evaluation_run_hash`. | Maximal binding, and maximal blockage: P0-13 is itself blocked behind B-01/P0-20 acceptance (`dependency map:327`, `:331-336`), so M1 acceptance becomes unreachable for as long as that chain is open. Also expands M1's outputs beyond `plan:650`. |
| **2B** — M1 records `evaluation_run_hash`/`evidence_references` as opaque strings; catalog consumption belongs to the consumers (WP-V2A-10, WP-V3-03) and to Milestone 2/3. | Matches what `plan:650` and `plan:661` actually specify, and matches the built artifact. Leaves "actually consumed" literally unsatisfied, so the handoff wording would need amending. |
| **2C** — M1 keeps the opaque field, plus an optional configured catalog: when an accepted catalog is supplied, an `evaluation_run_hash` absent from it is refused; when none is supplied, the ledger fails closed on any record that claims catalog-backed evidence. | Preserves `BLOCKED`-never-`PASS` (`brief:1415`), reuses the existing configurable-and-fail-closed pattern already proven for check sets (`ledger:265-269`, `:306-330`, `:610-618`), and gives "actually consumed" a testable meaning without waiting on P0-13 to build M1. Requires new engineering and therefore a new candidate and a fresh T0 roster — **and two amendments this packet cannot make**: the frozen consumption sentence *"No real TrialRecord bytes are consumed in this slice"* (`G1_SCOPE_AND_CONTRACT.md:74`) and the fixed constructor seam (`G1_SCOPE_AND_CONTRACT.md:20`, adjustable only under `:18`). **The phrase "claims catalog-backed evidence" is undefined here and is not defined by this packet** (defining it would be new scope): read at its widest — any record carrying an `evaluation_run_hash` — it would refuse every non-Registrar ladder append, because `ledger:631-632` requires that hash on all of them. |

**Recommended answer: 2C**, with **2B** as the fallback if the owner wants zero further engineering
before acceptance. Reason: 2C is the only option that both honours the handoff's word *"actually
consumed"* and respects the doctrine that an unavailable input yields `BLOCKED`, never `PASS`
(`brief:1415`, `brief:1416`). It reuses a seam the candidate has already proven — `active_check_sets`
is exactly this shape: empty by default (`ledger:265-269`, normalized at `:280` via `:306-330`),
fail-closed (`:614-618`), configurable, never invented by the ledger. 2A converts a documentation
dependency into an indefinite block; 2B requires the owner to reword their own acceptance line,
which is cheap but leaves the dependency unfalsifiable.

**What the owner must settle before 2C is buildable** (recorded, not decided here): what counts as a
record that *"claims catalog-backed evidence"*. Without that definition 2C has no implementable
meaning, and its widest reading breaks the ladder (`ledger:631-632`).

**This recommendation does not close Item 2.** Even under 2C, exact accepted P0-13 provenance
remains required; see section 4.

---

### Item 3 — owner-ratified active worthiness check-set version

**Requirement, quoted** (`P031_HANDOFF.md:108`):

> "owner-ratified active worthiness check-set version"

**What exists today in the candidate.** The mechanism is complete and fail-closed; only the
definition is absent.

- `LifecycleLedger(path, writer_allowlist, active_check_sets=None)` — `ledger:265-269`. The mapping
  is normalized at construction and every purpose must be one of the seven declared ones
  (`ledger:306-330`; purposes at `ledger:31-41`).
- `CAPTURED -> TRIAGED` and `CAPTURED -> DECLINED` bind purpose `"worthiness"` (`ledger:497-499`).
- If the **event** carries no `check_set_version` for a purpose-bearing transition, the append is
  refused `CHECK_SET_REQUIRED` (`ledger:610-611`). If it carries one that is not in the configured
  active set for that purpose, it is refused `CHECK_SET_PURPOSE_MISMATCH` (`ledger:614-618`) — and
  that is also the code raised when the ledger has **no active worthiness version configured at
  all**, because the active-set lookup defaults to the empty tuple (`ledger:615-617`; normalization
  at `ledger:306-330` maps an absent mapping to `{}`). Both refusals are proven at `test:544-547`:
  the version-less append raises, and the draft version raises while it is not the configured active
  one. Replay re-derives the purpose from the event and refuses any stored record whose purpose
  disagrees (`ledger:873-875`); active-set membership is enforced at append only (`ledger:774`
  versus `ledger:925`).
- **The executable contains no check-set version string at all.** The only `worthiness` occurrences
  in `p031_lifecycle_ledger.py` are the purpose name at `:33` and `:499`. Nothing is hard-coded,
  defaulted or invented — exactly what `G1_SCOPE_AND_CONTRACT.md:75` demanded: *"Engineering may
  prove the configurable guard with fixtures but may not invent or activate a version."*

**Candidate check-set versions found in the tree.** There is exactly one real candidate definition;
everything else is a test literal.

| # | Where | What it is | Status |
|---|---|---|---|
| 1 | `MTC_COMMAND_CENTER/11_TRIAGE/WAYFINDER_LIFECYCLE_FOLD_2026-08-23.md:92-106` — "Triage worthiness checklist — v0.1 DRAFT (fold deliverable of #63)"; criteria W1-W7 at `:98-104`, verdict rule at `:106` | The **only** worthiness checklist artifact anywhere in the tree | **DRAFT / INACTIVE.** `:94`: *"This v0.1 is a DRAFT for the owner's ratification in the next acceptance round — it binds nothing until ratified."* |
| 2 | `test_p031_lifecycle_ledger.py:547` — `check_set_version="worthiness.v0.1-draft"` (1 occurrence) | A fixture string used once, to prove the draft is refused when it is not the configured active version | Test fixture. Not an artifact and not a proposal. |
| 3 | `test_p031_lifecycle_ledger.py` — `worthiness.v1` (33 occurrences; e.g. `:549`) | The fixture "active" version configured in the test ledgers | Test fixture only. |
| 4 | Same file — `shadow-eligibility.v1` (19), `testnet-eligibility.v1` (9), `live-candidate-eligibility.v1` (8), `promotion.v1` (15), `supervisor.v1` (14), `paper-eligibility.v1` (5) | Fixture versions for the other six declared purposes (`ledger:31-41`) | Test fixtures only. **No ratified version exists for any of the seven purposes**, not just worthiness. |

The governing statement is unambiguous (`brief:1289`):

> "the only worthiness checklist that exists is `WAYFINDER_LIFECYCLE_FOLD_2026-08-23.md` §5 v0.1,
> which that record states is a DRAFT for the owner's ratification and which 'binds nothing until
> ratified'. … The v0.1 checklist is INACTIVE, and `CAPTURED`→`TRIAGED` is `BLOCKED` until the owner
> ratifies an exact checklist version, which then becomes the `check_set_version` that transition
> records."

The same line states that **nothing else can ratify it**: not G1 acceptance of the brief, not a
wayfinder fold, not a carrier clarification, not the overnight workflow recommendations.

**Classification: OWNER DECISION.** It is the first item under `WAITING FOR OWNER` in the Lead's
final handoff (`P031_M1_FINAL_HANDOFF_C76043B9.md:139`).

**One hazard the options must respect.** Ratifying a version does more than unblock a transition —
it starts automatic application. `brief:1415` makes an automatic admission valid only when *"(a) the
gate's full check set is **frozen and versioned**; (b) **every check has a proven-can-fail D026
fixture**; (c) missing data or an unset threshold yields **BLOCKED, never PASS** … (d) the record
names the **`check_set_version`** it applied"*, and *"An admission missing any of the four is
invalid, not merely weak."* No per-criterion D026 fixture set for W1-W7 exists in the tree. A bare
ratification today would turn a loud `BLOCKED` into a transition the ledger accepts — condition (d)
is satisfied by `ledger:611`/`:618` — but which is **invalid under (b)**. That is the exact failure
mode this design exists to prevent.

**Options.**

| Option | Consequence |
|---|---|
| **3A** — Ratify §5 v0.1's content unchanged under an exact version id the owner names. | `CAPTURED -> TRIAGED` becomes operable at once. The qualitative verdict rule at `fold:106` becomes binding. Condition (b) of `brief:1415` stays unmet until W1-W7 D026 fixtures exist, so the first real triage decisions would be invalid-by-doctrine while appearing green in the ledger. |
| **3B** — Ratify a `v1.0` = v0.1's seven criteria plus an explicit recorded verdict rule, and require the per-criterion proven-can-fail D026 fixture set to be accepted before that version becomes active. | Satisfies all four validity conditions. Costs one fixture-building round and keeps M1 acceptance blocked for its duration. |
| **3C** — Ratify nothing; leave everything exactly as it is. | Zero risk, zero progress. M1 acceptance stays blocked on an item M1's code does not need in order to be correct. |
| **3D** — Decouple. Keep the guard fail-closed and unratified, and amend the M1 acceptance line so a ratified worthiness version is a precondition of **writing a real `CAPTURED -> TRIAGED` record**, not of **accepting the ledger that stores it**. Run ratification (3B's content) in its own round, when triage actually runs. | M1 can be accepted on what it delivers: a versioned, configurable, fail-closed guard with fixture proof. Requires the owner to amend their own recorded decision `OD-20260912-P031-M1-SEQUENCING` (`C:/tmp/P031_M1_20260913/DECISIONS.md:18` — that row exists only on the candidate branch; `C:/CT13/DECISIONS.md:18` is the unrelated `OD-20260911-MATERIALIZER-1`) and the matching paragraph at `brief:298`. Both files are among the eight reviewed package paths (`reviews/P031_M1_REVIEW_PACKET_C76043B9.md:36`, `:41`), so amending them inside the candidate is a change to reviewed package content under `P031_HANDOFF.md:126-131`; and `fold:9` records that material amendments to the accepted set carry a recommendation for *"a fresh G1 acceptance round over the amended documents … before G1-IA is given for any affected package"*. Changes no lifecycle semantics and ratifies nothing. |

**Recommended answer: 3D, with 3B as its content when ratification is later run.**

Reasons, grounded in the design and plan text:

1. M1's acceptance gate (`plan:654`) covers replay, guards, RED/GREEN counterfactuals, derived-view
   rebuild and evidence lineage. It requires no check set to be active. The ledger's job is to record
   `check_set_version` and refuse when it is absent or inactive — which it does (`ledger:610-618`,
   proven at `test:533-550`).
2. `brief:1416` says application *"begins at the owner's ratification of an exact version and never
   before."* Under 3D that stays literally true and nothing is applied.
3. `brief:1415(b)` makes ratification-without-fixtures actively harmful; recommending 3A would be
   recommending an invalid-but-green admission path.
4. `fold:94` and `fold:106` show v0.1 was written as a draft with deliberately qualitative
   thresholds, and `brief:1536` sets the standing rule: *"Every number named here is **[OPEN]** by
   design — unset means BLOCKED, never permissive."* Ratifying it unchanged promotes a deliberately
   provisional artifact.

3D is not free, and its cost is not code: it asks the owner to loosen a recorded M1-acceptance
requirement (`brief:298`: *"M1 acceptance still requires … an owner-ratified worthiness check-set
version"*) in two reviewed documentation paths, with `fold:9`'s fresh-G1 recommendation in view.
Whether that amendment itself needs a fresh G1 round is outside this lane (§5 item 12).

If the owner prefers not to reopen `OD-20260912-P031-M1-SEQUENCING`, take **3B** and accept the
delay. Do not take **3A**.

---

### Item 4 — the seven fail-closed lifecycle envelopes

**Requirement, quoted** (`P031_HANDOFF.md:109-111`):

> "seven fail-closed lifecycle envelopes: DEMOTED target, CHALLENGE incumbent, atomic succession,
> REJECTED purpose/evidence, ambiguous capacity target, deployment refresh, and evaluation-run
> candidate scope"

All seven are explicit refusals inside one validator, `_validate_transition` (`ledger:522-686`), and
all seven are disclosed in every rendered report (`ledger:1259-1267`). None is silent; none can be
reached by accident.

**Summary answer to the question the brief asks — decision needed, or pure engineering?**

| # | Envelope | Refusal in code | Verdict |
|---|---|---|---|
| 1 | `DEMOTED` target | `ledger:545-546` | **Decision needed** (target rung + writer authority), then engineering |
| 2 | `CHALLENGE` incumbent | `ledger:547-548` | **Decision needed** (carrier field) **+ blocked on WP-P0-04** |
| 3 | Atomic succession | `ledger:595-606` | **Decision needed** (record shape). The interim rule closes it under **3D** / OD-4; the design's family-scoped rule is **blocked on WP-P0-04** |
| 4 | `REJECTED` purpose/evidence | `ledger:549-550` | **Decision needed** (which gate's purpose) |
| 5 | Ambiguous capacity target | `ledger:551-555` | **Decision needed** (target carrier — small) |
| 6 | Deployment refresh | `ledger:566-577` | **Decision needed** (landing state only; every other invariant is already ratified) |
| 7 | Evaluation-run candidate scope | `ledger:637-643` | **Ratification only** — no engineering; the implemented behavior is the recommended answer |

**None of the seven is pure engineering under existing semantics.** Each needs at least a target, a
carrier or a record shape that no ratified text supplies. Envelope 7 is the cheapest to close: the
owner's word alone settles the rule — though the report's disclosure line for it (`ledger:1266`)
keeps printing `UNRESOLVED` until a separately authorized ledger edit.

#### Envelope 1 — `DEMOTED` target rung

*Refusal:* `ledger:545-546` raises `DEMOTION_TARGET_RUNG_MAPPING_UNRESOLVED` for any `DEMOTED`
event, before any other check. Test: `test:4448-4471`.

*What is ratified.* `brief:1542`: *"**Demotion.** Back down the ladder under the SAME
`deployment_identity_hash`; the live window ends and stays queryable forever; fresh forward evidence
accumulates from the demotion point; going live again requires the full signed gate."* `fold:18`:
*"DEMOTE = down-ladder same identity, re-live = full gate."* For the succession case only,
`brief:1548` names a default: *"The replaced incumbent demotes to `SHADOW` as a control by default
(forever queryable; the owner may retire it instead)."*

*What is missing.* Three things. (a) The target rung for a general demotion — *"back down the
ladder"* fixes the direction, not the destination, and the only named destination is the succession
default. (b) `DEMOTED` appears in **no** writer class's authority set (`ledger:65-91`) — no writer
may issue it at all today. (c) `DEMOTED` appears in **no** ladder transition tuple
(`ledger:92-114`), so no prior/next pair exists for it.

*Options.*

| Option | Consequence |
|---|---|
| **1A** — Fixed mapping table: `LIVE -> SHADOW`, `LIVE_CANDIDATE -> SHADOW`, `TESTNET -> SHADOW`; no demotion below `SHADOW`. | Mechanical and unambiguous. Contradicts nothing, but hard-codes a choice `brief:1542` deliberately left to the demoting authority, and collapses a three-rung ladder to one destination. |
| **1B** — The writer supplies `next_state`; the ledger validates that it is strictly below the current rung on the ladder order implied by `ledger:94-98` (`SHADOW` < `TESTNET` < `LIVE_CANDIDATE` < `LIVE`) and that `deployment_identity_hash` is unchanged. | Records the authority's actual choice; makes "down" mechanical and "same identity" enforced. Needs the ladder order named explicitly, which today is only implicit in `LADDER_TRANSITIONS`. |
| **1C** — Demotion is permitted only from `LIVE`, always to `SHADOW` — the single case the ratified text actually names. | Smallest possible surface, fully grounded in `brief:1548`. Leaves sub-live demotion undefined, so a testnet candidate that must step down has no record type and stays fail-closed. |

*Recommended answer: **1B**, together with the two structural additions it requires* — add `DEMOTED`
to the `MULTI_WORKER_SUPERVISOR` authority set (`ledger:88-90`), matching `brief:1550`'s carrier
assignment of *"WP-V2B-03 for mandatory post-live tail records"*, and add the corresponding
descent tuples to `LADDER_TRANSITIONS`.

*Reasons.* `brief:1542` fixes exactly two invariants — direction and identity — and 1B enforces
precisely those two, inventing nothing else. `brief:1548` shows the destination is a *choice*
("the owner may retire it instead"), which a fixed table (1A) would erase. 1C is defensible but
leaves a real hole: `brief:1421` already contemplates a slot freeing on *"failure/suspension/
demotion"* at testnet, so sub-live demotion is expected to exist.

*Coupling:* if the owner takes envelope 3 option **3A** below, the incumbent's closure record at a
succession swap is a `DEMOTED` event, so envelope 1 must be answered first or together.

#### Envelope 2 — `CHALLENGE` incumbent deployment identity

*Refusal:* `ledger:547-548` raises `CHALLENGE_INCUMBENT_DEPLOYMENT_IDENTITY_FIELD_MISSING` for any
`CHALLENGE` event. Test: `test:4473-4489`.

*What is ratified.* `brief:1548`: *"the challenger's records name the incumbent
`deployment_identity_hash` they challenge (`CHALLENGE` record)"*; `fold:112` lists
*"Succession: `CHALLENGE` (names the incumbent identity)"*; `fold:22` is the source decision (#64).

*What is missing — a field, not a meaning.* The semantics are already decided. What does not exist
is anywhere to put the incumbent identity: `LifecycleEvent` (`execution.py:168-188`) has
`deployment_identity_hash` for the *subject* candidate and nothing for a *referenced* one, and a
grep of `contracts/mtc_contracts/` for `incumbent`/`challeng` returns zero matches. `CHALLENGE` is
also absent from every authority set (`ledger:65-91`) and from `LADDER_TRANSITIONS`
(`ledger:92-114`).

*Options.*

| Option | Consequence |
|---|---|
| **2A** — Add a nullable challenged-incumbent identity field to the shared `LifecycleEvent` under **WP-P0-04**, required on `CHALLENGE` and forbidden elsewhere. | The identity becomes typed and validated in the one shared contract, visible to every writer and every consumer that reads it. Blocked behind P0-04 authority; P031 may not edit shared contracts (`G1_SCOPE_AND_CONTRACT.md:11`). |
| **2B** — Carry it as P031-local append evidence, alongside `check_set_version` and `evaluation_run_hash` (`ledger:191-209`). | Buildable inside P031 today, and it does land inside the ledger record — the same canonical-evidence channel that already carries `check_set_version` (`ledger:191-209`), which is itself not a `LifecycleEvent` field. What it costs is shared-contract reach: the incumbent identity would be typed and validated nowhere in `LifecycleEvent` (`execution.py:168-188`), so nothing reading the shared contract sees it, and the other three writer classes get no contract-level obligation to supply it. |
| **2C** — Encode it in `evidence_references` by convention. | No schema change at all, and no validation either: `evidence_references` is `tuple[NonEmptyStr, ...]` (`execution.py:182`). An unvalidated convention on the exact field that binds a live swap is the weakest available option. |

*Recommended answer: **2A***, with `CHALLENGE` remaining fail-closed until WP-P0-04 carries the
field.

*Reasons.* `plan:320` already assigns *"eligibility-verdict and environment-admission record types"*
to WP-P0-04, so referenced-identity fields are that package's business, and
`G1_SCOPE_AND_CONTRACT.md:11` forbids P031 from adding them itself. `brief:1516` makes typed
composite identity the condition of usability — *"An artifact of any of these classes without a
`deployment_identity_hash` is unusable as evidence"* — which argues for keeping identity in the
shared contract, though that sentence is about the subject composite and does not by itself settle
where a *referenced* incumbent hash must live.

**V2 correction (Grok #5).** The V1 draft said 2B *"contradicts"* `brief:2223` — *"every record names
its issuer, the evidence it consumed, its identity keys and its `check_set_version` where one
applied"* — and that `brief:2223` *"makes the ledger the single place where a record's identity keys
are legible to all four writers"*. Re-read against the source, that sentence describes what a
**ledger record** names, and one of the four things it names, `check_set_version`, already lives in
exactly the P031-local canonical-evidence channel 2B proposes (`ledger:191-209`); it is not a
`LifecycleEvent` field (`execution.py:168-188`). So `brief:2223` does not forbid 2B. The case for 2A
rests on `plan:320` and on keeping a referenced identity typed in the one shared contract. Whether
any ratified line *requires* the challenged incumbent identity to sit on `LifecycleEvent` rather than
in ledger-local evidence was not established here (§5 item 17).

*Second, smaller decision inside this envelope:* **which writer class issues `CHALLENGE`.**
`brief:1548` says *"the **challenger's** records name the incumbent"*, and the challenger is *"an
ordinary candidate"* climbing the full ladder — which points at the Registrar or the Environment
Admission Authority, not the Promotion Authority. The candidate's fixture issues it as
`PROMOTION_AUTHORITY` (`test:4488`), which is a test convenience, not a decision. The owner should
name the issuing class when answering 2A.

#### Envelope 3 — atomic two-candidate succession

*Refusal:* `ledger:595-606` raises `SUCCESSION_ENVELOPE_UNRESOLVED` when a `PROMOTED` event is
appended for one candidate while **any other** candidate is `LIVE`, or `SUSPENDED` from `LIVE`.
Tests: `test:3741`, `test:3771`.

*What is ratified.* `brief:1548`: *"**The swap is atomic: one owner signature at the live gate admits
the challenger AND closes the incumbent's live window** — never two live members of one family."*
`fold:22` is the source decision.

*What exists today is stricter than the design.* The guard is repository-wide, not family-scoped,
because `family_id` is not on `LifecycleEvent` (`execution.py:168-188`) even though it exists
elsewhere in the contracts package (`identity.py:144`, `package.py:31`, `trials.py:22`). So the
candidate currently refuses *any* second live candidate, where the design forbids only *two live
members of one family*. That is fail-closed in the correct direction, and it is worth recording as
a deliberate interim rather than as a defect.

*What is missing.* The record shape for one act that changes two candidates' states. `append`
(`ledger:688-820`) is strictly one event per call inside one `BEGIN IMMEDIATE` (`ledger:699`); there
is no seam for two events in one commit, and no `LIVE -> ...` closure tuple exists
(`ledger:92-114`).

*Options.*

| Option | Consequence |
|---|---|
| **3A** — One transaction, two events: the challenger's `PROMOTED` and the incumbent's closure record (`DEMOTED` to `SHADOW`, or `RETIRED`), both validated and committed together, both refused unless both validate. | Keeps one record per state change, so both candidates' histories name their own issuer, evidence and identity keys (`brief:2223`). Atomicity already exists at the transaction level (`ledger:699`). Requires a **new public seam** — an atomic multi-event append — which is new lifecycle semantics and therefore owner-gated, not engineering. Depends on envelope 1. |
| **3B** — One `PROMOTED` event carrying the incumbent identity; the ledger derives the incumbent's state change. | No new seam. But one writer's record would silently change another candidate's state, and the incumbent's closure would have no record of its own — its history would show a state change with no event, which the replay model (`ledger:822-981`) cannot express and the acceptance gate's *"every … succession record retains its evidence and identity lineage"* (`plan:654`) forbids. |
| **3C** — Two ordinary sequential appends with a "succession pending" interlock between them. | Buildable with today's seam, but it is not atomic; a crash between the two appends leaves either two live members or none. `brief:1548` says atomic. |
| **3D** — Defer: ratify the current repository-wide refusal as the interim rule, and decide the swap shape only when WP-V3-03 (the Promotion Authority) is built. | Costs nothing now, keeps the strictest behavior, and honestly reflects that no promotion producer exists. **Closes this envelope on the acceptance list in its interim, stricter-than-design form** — the position taken in the reasons below, in OD-4's row and in §4 — and leaves open the *swap shape*, not the envelope. What ratification does **not** do: the report's disclosure line `"ATOMIC SUCCESSION PROMOTED ACROSS TWO CANDIDATES: UNRESOLVED"` (`ledger:1262`, one of the seven hardcoded strings at `ledger:1259-1267`) keeps printing until a separately authorized ledger edit, exactly as for envelope 7. |

*Recommended answer: **3D now, 3A when the Promotion Authority is built.***

*Reasons.* The atomic swap is exercised by exactly one writer, the Promotion Authority
(`brief:2203`, `brief:1550`: *"WP-V3-03 for promotion/mainnet admission"*), which is a **V3** package
that does not exist. Designing its record shape inside a fixture-only M1 would fix a seam for a
producer nobody has specified, and `START_PROMPT.md:16` is explicit: *"Where a required shared
contract is genuinely unspecified, present the exact missing decision; do not invent it."* Ratifying
the current stricter-than-design refusal (3D) closes the envelope for M1 acceptance purposes without
inventing anything, and records why it is stricter: `family_id` is absent from `LifecycleEvent`.
When 3A is later chosen, it needs envelope 1 (the closure record type) and the P0-04 `family_id`
field first.

#### Envelope 4 — `REJECTED` failed-gate purpose and evidence

*Refusal:* `ledger:549-550` raises `REJECTED_PURPOSE_UNRESOLVED` for any `REJECTED` event. Tests:
`test:698`, `test:2061`, `test:3968`.

*What is ratified.* `brief:1424`: *"Every `REJECTED` verdict records the failed gate, the
`check_set_version`, the `evaluation_run_hash`, each failing check's value against its threshold, and
issuer + timestamp."* `fold:23` is the source decision (#65).

*What exists today.* The evidence *shape* is already implemented and validated: each failing check
must be exactly `{check_id, observed_value, threshold}` with unique non-empty ids and JSON-scalar
values (`ledger:454-479`). `REJECTED` is listed in the Registrar's authority set (`ledger:74`).

*What is missing — the purpose, and therefore everything downstream.* `_check_set_purpose`
(`ledger:497-520`) derives the purpose from `event_type`, and it returns `None` for `REJECTED`;
`CHECK_SET_PURPOSES` (`ledger:31-41`) contains no rejection purpose because a rejection is not a
gate — it is the *failure of some other gate*, and which gate is not a function of the event type.
There is also no `REGISTRAR_TRANSITIONS` tuple producing `REJECTED` (`ledger:43-55`), so the state is
unreachable even if the purpose were known.

*Consequence worth recording.* Because `REJECTED` is unreachable and re-entry forbids carrying prior
evidence (`ledger:629-630`), `failing_checks` is structurally unreachable on every accepted path —
`ledger:635-636` refuses it everywhere else. Every stored record's `failing_checks` is therefore
`()`, and the report's `failing_checks` is always `[]` (`ledger:1237` — pin re-verified in V3
against the file as it stands now; re-audit NEW-2 rebutted, see §0.2). The exact Opus review
recorded this as nit N-3 and the Sol review as nit 5
(`P031_M1_SOL_XHIGH_REPORT_C76043B9.md:19`): an always-empty list must not be readable as *"no checks
failed"*.

*Options.*

| Option | Consequence |
|---|---|
| **4A** — `REJECTED` carries an explicit writer-supplied `check_set_purpose` drawn from the declared set (`ledger:31-41`), validated against the candidate's current rung, with `check_set_version`, `evaluation_run_hash` and non-empty `failing_checks` all mandatory. | Directly implements `brief:1424` ("the failed gate"). Reuses the existing purpose↔version binding (`ledger:614-618`) and the existing failing-check shape. Makes `failing_checks` reachable, which gives the report a truthful non-empty case. |
| **4B** — `REJECTED` is funnel-only (Registrar, from `CANDIDATE`) and always names `worthiness`. | Simplest. But it contradicts `brief:1424`'s generality — a rejection can follow any gate — and would leave failures at the eligibility gates with no record type. |
| **4C** — Split `REJECTED` into one event type per gate. | Unambiguous, but it adds shared lifecycle vocabulary that `fold:112`'s record-type list does not contain. |
| **4D** — Derive the purpose from `previous_state`. | Looks cheap; it is the exact pattern that already failed. `ADMISSION_WITHHELD_CAPACITY` derives its purpose from `previous_state` (`ledger:508-509`) and is fail-closed from `SHADOW` precisely because that derivation is ambiguous (`ledger:551-555`). |

*Recommended answer: **4A**.*

*Reasons.* `brief:1424` names four things a rejection must record, and three of them are already
implemented; the missing one is the gate identity, which 4A supplies in the vocabulary the ledger
already validates. `G1_SCOPE_AND_CONTRACT.md:35` anticipated exactly this shape: *"`REJECTED`
requires check-set version, evaluation-run hash and non-empty failing-check evidence."* 4D is
refuted by the candidate's own experience with envelope 5.

*Coupling — a discrepancy the owner should close in the same answer.*
`G1_SCOPE_AND_CONTRACT.md:33` lists the permitted Registrar paths as including
*"`REJECTED|DECLINED|PARKED -> CANDIDATE` only as `RE_ENTRY`"*, and `brief:1546` likewise names
*"`REJECTED`, `DECLINED` and `PARKED`"* as the re-entry-eligible states. The implemented
`REGISTRAR_TRANSITIONS` (`ledger:43-55`) contains `DECLINED`, `PARKED` and **`RETIRED`** re-entry —
but **not** `REJECTED`. So the code is missing one arc the contract names, and carries one the
contract does not. Answering envelope 4 must restore `("REJECTED", "RE_ENTRY", "CANDIDATE")`;
Item 5 below decides the `RETIRED` arc.

#### Envelope 5 — ambiguous capacity-withholding target

*Refusal:* `ledger:551-555` raises `ADMISSION_WITHHELD_TARGET_UNRESOLVED` when an
`ADMISSION_WITHHELD_CAPACITY` event arrives with `previous_state == "SHADOW"`. Test: `test:1919`.

*What is ratified.* `brief:1420` rule 6: *"When checks pass but capacity is full, the eligibility
verdict is recorded AND an **`ADMISSION_WITHHELD_CAPACITY`** record is appended; the candidate stays
at its rung, visibly eligible-and-waiting."* `brief:1422` rule 8 extends it to a shadow resource-guard
trip. `plan:773` requires each admission decision to name *"the exact environment set admitted to"*.

*What exists today.* From `FROZEN` the record is accepted: the purpose is inferred as
`shadow_eligibility` (`ledger:508-509`) and the tuple `("FROZEN", "ADMISSION_WITHHELD_CAPACITY",
"FROZEN")` exists (`ledger:99`) — the candidate correctly stays at its rung. From `SHADOW` the next
rung is genuinely ambiguous: it could be `INTERNAL_PAPER` (`PAPER_ELIGIBLE`) or `EXCHANGE_TESTNET`
(`TESTNET_ELIGIBLE`), which are two different owner-ratified gates with different preconditions
(`brief:2201`, `brief:2202`). `LifecycleEvent` carries no environment or target field
(`execution.py:168-188`).

*Options.*

| Option | Consequence |
|---|---|
| **5A** — Add an explicit withheld-target field (environment or target rung) to the event or its evidence; bind the purpose to that target. | Explicit and readable. Adds a field that duplicates information the `check_set_version` already carries, and — if placed on `LifecycleEvent` — needs WP-P0-04. |
| **5B** — Split into per-target event types (`…_PAPER`, `…_TESTNET`). | Unambiguous, but adds shared vocabulary beyond `fold:112`'s record-type list. |
| **5C** — Require the writer to supply the `check_set_version` of the gate whose slot is full, and take the target from that version's purpose instead of inferring it from `previous_state`. | Zero new vocabulary and no shared-contract change. The three relevant purposes already exist (`ledger:31-41`), the purpose↔version binding is already validated (`ledger:614-618`), and the purpose is already stored in canonical evidence (`ledger:191-209`) and surfaced in the report (`ledger:1234-1235`). |

*Recommended answer: **5C**.*

*Reasons.* `brief:1420` says the withheld record accompanies *"the eligibility verdict"* of a
specific gate, and `brief:1415(d)` already requires every such record to name the
`check_set_version` it applied — so the gate identity is information the record must carry anyway.
5C makes the ledger read it instead of guessing. It is the smallest step consistent with the
ratified text and it needs nothing from WP-P0-04.

*What the owner is actually approving here:* that `_check_set_purpose` takes the supplied
`check_set_version` as an input for this one event type, and that the withheld target stops being
inferred from `previous_state`. That is a semantic change — which gate a record is about — and that
is why it is an owner decision and not engineering. **V2 correction (Grok #12):** the V1 draft
called this the point where the function *"stops being a pure function of `event_type`"*. It already
is not one: it reads `previous_state` for exactly this event type (`ledger:508-509`) and
`writer_class` for `RESUMED` (`ledger:510-519`). The novelty is the new input and the changed
determinant, not the departure from `event_type` alone.

#### Envelope 6 — deployment refresh

*Refusal:* `ledger:566-577` raises `DEPLOYMENT_REFRESH_ENVELOPE_UNRESOLVED` when a non-Registrar
event arrives at a deep rung (`SHADOW`, `TESTNET`, `LIVE_CANDIDATE`, `LIVE`, `SUSPENDED`) carrying
the same `package_hash` but a different `deployment_identity_hash`. Tests: `test:2336`,
`test:2563-2639`.

*What is ratified — almost all of it.* `brief:1435` (§6.6 rule 3): *"**Never modify a running
identity.** Any code, parameter, module or substitute change mints a **new `package_hash`**; any
change to the allocator, allocation policy, Guardian policy, risk-bucket or economic policy, runtime
policy, protection semantics, broker adapter or cost lineage mints a **new
`deployment_identity_hash` with `package_hash` unchanged**. Either way a **new composite and a new
clock** exist, the old window does not transfer, and the old window is marked `PRIOR_IDENTITY`."*
`brief:2211` (§11.5 rule 5): *"A material identity change revokes admission. … any change under §6.7
leaves the new identity with **no** admission record — so it is refused until re-admitted. Revocation
is automatic and silent-by-construction rather than a process someone has to remember."*
`brief:1421` adds that the slot frees on an identity change.

*What is missing — one thing only.* The design fixes every consequence (new clock, evidence does not
transfer, admission revoked, slot freed, old window marked `PRIOR_IDENTITY`) but never names **the
state the candidate occupies after the refresh**. The ledger cannot record a state change it has no
destination for: there is no `LADDER_TRANSITIONS` path from any deep rung back to `FROZEN`
(`ledger:92-114`), `FROZEN` currently forbids a `deployment_identity_hash` outright
(`ledger:657-658`), and no `PRIOR_IDENTITY` marking exists anywhere in the schema
(`ledger:128-161`).

*Options.*

| Option | Consequence |
|---|---|
| **6A** — A refresh is not a lifecycle event: the new composite re-enters through the ordinary door — the candidate returns to `FROZEN` under the new `deployment_identity_hash`, and revocation is expressed by the absence of admission records for that new identity. Prior windows stay readable and never count. | Matches `brief:2211`'s "silent-by-construction" and `brief:1433`'s freeze-then-mint-then-admit rule, and `brief:1289`'s *"`FROZEN` … is **the only door** to the **EVIDENCE LADDER**"*. Requires one decided transition (deep rung -> `FROZEN`, same candidate, new composite) and a relaxation of `ledger:657-658` so a re-freeze may carry the new deployment identity. |
| **6B** — A new `DEPLOYMENT_REFRESHED` record type that marks the old window `PRIOR_IDENTITY` and resets the rung. | Most explicit and most auditable. Adds shared vocabulary not present in `fold:112`, and `brief:2211` argues against making revocation *"a process someone has to remember"*. |
| **6C** — Keep it fail-closed until WP-V2A-10 defines revocation mechanically. | Costs nothing; leaves the envelope open. Defensible, since WP-V2A-10's Outputs already include *"automatic revocation on any change to `deployment_identity_hash`"* (`plan:777`). |

*Recommended answer: **6A**, naming `FROZEN` as the landing state.*

*Reasons.* `brief:1433` requires a freeze and a mint before *any* observation of *any* composite —
*"This applies identically to the early baseline package and to every optimized package selected
later"* — so the refreshed composite must pass through the same door. `brief:1289` makes `FROZEN`
that door. 6A therefore adds a destination the design already implies rather than a new record type
the design argues against. The residual `PRIOR_IDENTITY` marking is a *reporting* concern: the old
window is already permanently readable from the append-only history (`ledger:822-981`), so the
report can label it without a new record type.

#### Envelope 7 — evaluation-run candidate scope

*Refusal:* `ledger:637-643` binds each `evaluation_run_hash` to the first candidate that cited it
(`ledger:932-934`) and raises `EVALUATION_RUN_CANDIDATE_SCOPE_UNRESOLVED` if a different candidate
cites it, at both the append and replay seams. Test: `test:2477-2561`.

*What is ratified.* `brief:1466-1471` defines
`evaluation_run_hash = SHA256(package_hash ‖ dataset_manifest_sha ‖ cost_model_json ‖
simulator_class + simulator_version ‖ evaluation_config_json)`, and `brief:1517` says `candidate_id`
*"aggregates packages for navigation and family-level multiple-testing accounting only"*. Nothing
states whether two `candidate_id`s may cite one evaluation run.

*Options.*

| Option | Consequence |
|---|---|
| **7A** — Ratify the implemented rule: an `evaluation_run_hash` binds to exactly one `candidate_id` forever; any cross-candidate citation is refused at append and at replay. | Strictest reading; zero engineering; already has RED/GREEN and replay-seam evidence (`test:2477-2561`). A legitimate cross-candidate share, if one ever exists, surfaces as a loud refusal rather than silent evidence sharing. |
| **7B** — Allow cross-candidate citation when both candidates cite the same `package_hash`; refuse otherwise. | Follows the hash formula literally. Requires engineering and weakens a guard with no demonstrated need — the worthiness checklist's W6 (*"**Not a duplicate**"*, `fold:103`) exists precisely to stop two candidates covering the same package. |
| **7C** — Drop the guard and rely on `package_hash` equality alone. | Allows one evaluation run to justify decisions for unrelated candidates. Contradicts `brief:745`: evidence gathered against a different identity *"is evidence about a different system"*. |

*Recommended answer: **7A** — ratify what is implemented.*

*Reasons.* It is the only option requiring no code change and no new candidate, it already carries
review-reproduced evidence, and it is the strictest fail-closed reading of `brief:745`.

**V2 correction (Grok #3).** The V1 draft added that ratifying 7A *"lets the report's
`unresolved_lifecycle_contracts` list (`ledger:1259-1267`) drop one entry truthfully, which is
otherwise impossible without engineering."* Ratification by itself does no such thing.
`unresolved_lifecycle_contracts` is a list of seven hardcoded strings, and
`"EVALUATION RUN CANDIDATE SCOPE: UNRESOLVED"` (`ledger:1266`) keeps printing until that list is
edited — an executable change, and therefore a new exact candidate and the full T0 roster under
`P031_HANDOFF.md:126-131`. What ratification does is make the entry *stale rather than accurate*, and
give a later batched edit (Item 6) something truthful to record. Until that edit lands, the report
still advertises envelope 7 as unresolved.

---

### Item 5 — owner decisions for `RETIRED -> RE_ENTRY` and same-epoch reuse of one evaluation run across distinct check-set purposes

**Requirement, quoted** (`P031_HANDOFF.md:112-113`):

> "owner decisions for `RETIRED -> RE_ENTRY` and same-epoch reuse of one evaluation run across
> distinct check-set purposes"

These are two independent decisions and are laid out separately.

#### 5(a) — `RETIRED -> RE_ENTRY -> CANDIDATE`

**What exists today in the candidate.** The transition is permitted and fully constrained:

- `("RETIRED", "RE_ENTRY", "CANDIDATE")` is a member of `REGISTRAR_TRANSITIONS` (`ledger:53`).
- `RETIRED` is otherwise terminal: any non-`RE_ENTRY` event on a retired candidate is refused
  `RETIRED_IDENTITY_TERMINAL` (`ledger:557-558`).
- Re-entry requires one of the five ratified triggers (`ledger:622-624`, triggers at
  `ledger:56-64`), a fresh `evaluation_run_hash` never seen for that candidate
  (`ledger:625-628`), and carries no prior failing-check evidence (`ledger:629-630`).
- Re-entry **from `RETIRED` clears both identities**: `ledger:680-681` returns `(None, None)`, so the
  candidate returns to `CANDIDATE` with `package_hash` and `deployment_identity_hash` unset.
- The retired identities can never come back: the retired `deployment_identity_hash` is permanently
  refused (`ledger:674-675`, recorded at `ledger:947-948`) and the retired `package_hash` can never
  be re-frozen for that candidate (`ledger:659-660`, recorded at `ledger:949-952`).
- Evidence: `test:3639-3705` (re-entry with a new package but not the retired deployment) and
  `test:4087` (retired package cannot be re-frozen).

**What the ratified text says.** `brief:1544`:

> "**Retirement.** Terminal for the identity, not the idea: `RETIRED` ends that
> `deployment_identity_hash` forever. The family re-enters the funnel as a new package only when the
> owner names, in one sentence, the specific external thing that changed — logged next to the
> retirement note."

and `brief:1546`, the general re-entry rule, names a *different* set of states and a *different*
trigger mechanism:

> "**Re-entry (whole funnel).** `REJECTED`, `DECLINED` and `PARKED` are all re-entry-eligible, never
> silently resurrected: five trigger classes — new data regime, new kernel version, new substitute
> catalogue, new enrichment modules, owner curiosity …"

`G1_SCOPE_AND_CONTRACT.md:33` says the same: *"`REJECTED|DECLINED|PARKED -> CANDIDATE` only as
`RE_ENTRY` with one of the five ratified triggers"*.

**What is missing — and the exact discrepancy.** `RETIRED` re-entry is governed by an
**owner-named external change**, not by the five automatic trigger classes; and the text says *"the
family re-enters … as a new package"*, which does not settle whether the same `candidate_id`
continues. The candidate currently routes `RETIRED` re-entry through the five automatic triggers —
including `OWNER_CURIOSITY` (`ledger:62`), which is precisely *not* "the specific external thing
that changed". Both flagship reviews flagged it and neither would settle it: Sol nit 2
(`P031_M1_SOL_XHIGH_REPORT_C76043B9.md:13`) — *"`RETIRED -> RE_ENTRY -> CANDIDATE` remains an owner
ratification question … Do not change semantics without owner ratification"* — and the Lead's R19
scope (`R19_CORRECTIVE_SCOPE.md:103-104`): *"needs an owner-ratified contract choice. Do not add,
remove, or reinterpret that transition in R19."*

**Classification: OWNER DECISION.**

**Options.**

| Option | Consequence |
|---|---|
| **5a-A** — Ratify the implemented behavior: `RETIRED -> RE_ENTRY -> CANDIDATE` under the same `candidate_id`, one of the five triggers, identities cleared, retired package and deployment permanently unusable. | Zero engineering. The owner's one-sentence external-change note would land in the event's `reason` field (`execution.py:180`), which is free text and unvalidated. Widens `brief:1546`'s enumeration to a state the ratified text handles under a stricter rule, and lets `OWNER_CURIOSITY` reopen a retired identity. |
| **5a-B** — Remove the transition: retirement is terminal for the *candidate*, and the family re-enters as a **new** `candidate_id`. | Strictest reading of *"re-enters the funnel as a new package"*. Loses the lineage link inside the ledger, because `family_id` is not on `LifecycleEvent` (`execution.py:168-188`); leaves the retired-package guard (`ledger:659-660`) mostly unreachable. Requires engineering and a new candidate. |
| **5a-C** — Keep the transition, but gate it on a **sixth, owner-only trigger class** distinct from the five automatic ones, with a mandatory recorded one-sentence external-change reason, and keep every existing constraint (fresh evaluation run, identities cleared, retired identities permanently refused). | Honours `brief:1544` exactly: an owner-named external change, not an automatic re-screen. Keeps `candidate_id` stable, which is what re-entry means everywhere else (`brief:1546`: *"`candidate_id` stable, fresh `evaluation_run_hash`, prior evidence never re-counted"*). Adds one shared trigger value — itself owner-gated vocabulary, which is why only the owner may do it. |
| **5a-D** — Defer: make `RETIRED -> RE_ENTRY` fail closed like the seven envelopes until ratified. | Consistent with how every other unratified lifecycle question in this candidate is handled. Costs engineering plus a new candidate and full T0 roster, to *remove* a capability the owner may then restore. |

**Recommended answer: 5a-C.**

*Reasons.* `brief:1544` sets a deliberately different and stricter bar for retirement than
`brief:1546` sets for the funnel states, and none of the five existing classes (`ledger:56-64`)
carries the meaning *"the specific external thing that changed"* — `OWNER_CURIOSITY` is the closest
and is plainly not it. 5a-C is the only option that preserves both halves of the ratified sentence:
terminal for the identity (the retired package and deployment stay permanently refused, already
implemented) but not for the idea (the family returns). 5a-A silently promotes an automatic trigger
into an owner-only gate; 5a-B discards lineage the ledger cannot otherwise express; 5a-D destroys a
capability before deciding whether it should exist.

**Answer this together with envelope 4.** As recorded there, `REGISTRAR_TRANSITIONS`
(`ledger:43-55`) is missing `("REJECTED", "RE_ENTRY", "CANDIDATE")` — an arc both
`G1_SCOPE_AND_CONTRACT.md:33` and `brief:1546` name — while carrying the `RETIRED` arc neither
names. One owner answer should settle the whole re-entry set.

#### 5(b) — same-epoch reuse of one evaluation run across distinct check-set purposes

**What exists today in the candidate.** Three distinct rules, only one of which is in question:

| Reuse pattern | Behavior | Where |
|---|---|---|
| Same candidate, **same epoch**, different check-set purposes | **Allowed** | no refusal exists; `ledger:644-649` refuses only *prior-epoch* reuse |
| Same candidate, **across an `RE_ENTRY` boundary** | Refused `EVALUATION_RUN_HASH_REUSED` | `ledger:644-649`; epoch boundary at `ledger:927-929` |
| **Different candidate**, ever | Refused `EVALUATION_RUN_CANDIDATE_SCOPE_UNRESOLVED` | `ledger:637-643` (envelope 7) |

An "epoch" is the span between `RE_ENTRY` events: on re-entry the current epoch's hashes move into
the prior set and the current set is cleared (`ledger:927-929`). The choice was made in repair round
R10 and recorded at `P031_M1_SCOPE_AND_STATUS.md:263-264`: *"evaluation reuse is allowed within an
epoch and refused across `RE_ENTRY` epochs"*.

The behavior is exercised by `test:2192-2288`
(`test_current_epoch_evaluation_may_support_multiple_decisions`), which drives one
`evaluation_run_hash` through `ADMISSION_WITHHELD_CAPACITY` + `SHADOW_ELIGIBLE`, through
`PAPER_ELIGIBLE` + `TESTNET_ELIGIBLE`, and through `LIVE_CANDIDATE` + `PROMOTED`. **The test asserts
nothing about what was stored.** Its final statement is
`for ledger in (capacity, paper, live): ledger.verify_integrity()` (`test:2287-2288`), which proves
the three appends did not raise and the three chains are intact, but pins no `check_set_purpose`, no
`check_set_version`, no `evaluation_run_hash` and no resulting `current_state`. The exact Opus review
recorded it as nit N-1 — in its words *"contains **no assertion at all** — the only such test of 101
(verified by AST scan)"* — and the Gemini corroboration as optional item 6
(`P031_M1_GEMINI_ADJUDICATION_C76043B9.md:52-53`).

**V2 correction (Grok #7).** The V1 draft said the test *"contains no assertion at all — it ends at
`test:2285`"*. `test:2285` closes the last `append_authority_event` call; the method runs to
`test:2288`, and its last two lines are the `verify_integrity()` loop above. The hole is real — no
assertion pins the behavior being ratified — but it is narrower than "no check of any kind", and the
"no assertion at all" wording belongs to the Opus AST scan, which counts assertion calls, not to a
claim that the method body ends at `:2285`.

**What the ratified text says — and the tension in it.** Two statements pull in opposite directions:

- `brief:1510` makes one evaluation run the natural carrier of *many* results: *"Evaluation identity
  is `evaluation_run_hash`. Every evaluation result — backtest, walk-forward, lockbox, CPCV,
  DSR/BH-FDR — is reported under it."* Several gates legitimately consume products of one run; for
  example `LIVE_CANDIDATE` requires the *"Full statistical battery complete"* (`brief:1383`), which
  is an evaluation-run product.
- `brief:2210` (§11.5 rule 4) pushes back: *"No decision widens another. … An escalation is a new
  decision with new evidence, not a re-reading of an old one."*

These are reconcilable: at an escalation the *new* evidence is the forward evidence accumulated on
the `deployment_identity_hash` (`brief:1383`, `brief:1511`), not a new evaluation run. The ledger
cannot check that, because forward-evidence windows are not modelled in Milestone 1.

**Classification: OWNER DECISION** (ratification of an engineering choice already made in R10).

**Options.**

| Option | Consequence |
|---|---|
| **5b-A** — Ratify the implemented rule: one evaluation run may back any number of distinct check-set purposes within one epoch; cross-epoch and cross-candidate reuse stay refused. | Zero semantic change. Matches `brief:1510`. Leaves `brief:2210`'s "new evidence" obligation to the gate that owns it (WP-P0-21 verdict sets, WP-V2A-10 admissions), which is where forward evidence actually lives. |
| **5b-B** — Refuse cross-purpose reuse: every purpose must cite its own fresh `evaluation_run_hash` within an epoch. | Maximally strict reading of `brief:2210`. Contradicts `brief:1510` — it would forbid `LIVE_CANDIDATE` from citing the statistical battery that justified it if any earlier gate cited the same run. Requires engineering. |
| **5b-C** — Allow reuse only between adjacent sub-live gates and require freshness at `LIVE_CANDIDATE` and `PROMOTED`. | Intuitive, but no ratified text defines such a grouping; it would be invented here. |
| **5b-D** — Allow reuse, and additionally require every reusing record to name the earlier record it re-reads. | Makes the re-reading explicit and auditable. Adds a new evidence field and new validation — new semantics, and no ratified text asks for it. |

**Recommended answer: 5b-A, subject to two conditions that are engineering, not semantics.**

1. `test:2192-2288` must gain real assertions before acceptance — the stored records'
   `check_set_purpose`, `check_set_version` and `evaluation_run_hash`, and the resulting
   `current_state` — so the behavior being ratified is actually pinned rather than merely
   non-raising and chain-intact. (Opus N-1; Gemini optional 6.) **This is a change to reviewed test
   content**, so under `P031_HANDOFF.md:126-131` it costs a new exact candidate and the full T0
   roster. OD-10 is therefore not an owner's-word-only answer; it belongs with the batch.
2. The report's `unresolved_lifecycle_contracts` list (`ledger:1259-1267`) currently does **not**
   mention cross-purpose reuse at all, so a reader cannot see that this rule was ever in question.
   Whichever way the owner answers, that omission should be closed — either by adding the
   disclosure or, on ratification, by recording the answer. That too is an executable edit with the
   same cost.

*Reasons for 5b-A.* It is the only option grounded in ratified text rather than invented structure;
`brief:1510` states plainly that one evaluation run carries many results. `brief:2210`'s
anti-widening rule is real but is enforced at the gate that supplies the evidence set, not at the
ledger that records the decision — Milestone 1 holds no forward-evidence window to check it against.
5b-B would make a correct `LIVE_CANDIDATE` record unwritable. 5b-C and 5b-D both invent structure the
owner has not ratified, which `START_PROMPT.md:16` forbids.

---

### Item 6 — pre-integration tightening of provenance-losing delegated Pydantic copy/dump helpers

**Requirement, quoted** (`P031_HANDOFF.md:114`):

> "pre-integration tightening/disposition of provenance-losing delegated Pydantic copy/dump helpers"

**What exists today in the candidate.** `LifecycleRecord` (`ledger:164-179`) is a
`@dataclass(frozen=True, slots=True)` that wraps a `LifecycleEvent` and adds the five local
provenance fields (`check_set_purpose`, `check_set_version`, `evaluation_run_hash`,
`failing_checks`, `source_kind`) plus `authoritative: bool = False`. Attribute lookups that miss the
record fall through to the wrapped event (`ledger:176-179`).

The R20 repair (`ledger:177-178`) refuses **dunder** delegation, which is what closed the exact Opus
finding recorded in `R20_CORRECTIVE_SCOPE.md:6`: *"`LifecycleRecord.__getattr__` delegates the
`__deepcopy__` protocol lookup to the wrapped Pydantic event, allowing `copy.deepcopy(record)` to
return a provenance-free `LifecycleEvent`."* `deepcopy`, `copy.copy` and `pickle` now all preserve
the record type and every provenance field.

**What is missing.** Ordinary, non-dunder Pydantic helpers still delegate. The exact Sol review
reproduced it on a real replay record (`P031_M1_SOL_XHIGH_REPORT_C76043B9.md:7-11`):

> "`record.model_dump()` with only the 14 event keys; `source_kind` and `authoritative` were absent.
> `record.model_copy()` and deprecated `record.copy()` returned `LifecycleEvent`."

The exact Opus review recorded the same as nit N-6, and the Gemini corroboration as optional item 1
(`P031_M1_GEMINI_ADJUDICATION_C76043B9.md:44-46`). All three graded it **optional**, because the
supported replay fields and the report path remain provenance-safe: the report is built from stored
canonical bytes, not from record helpers (`ledger:1213-1242`), and stamps `"authoritative": False`
on every row (`ledger:1240`).

**Classification: ENGINEERING**, with a small disposition choice about where to draw the line. It is
inside the same-package defect/repair authority (`START_PROMPT.md:44`) and needs no owner semantics.
The Lead already retained it as a pre-integration item
(`P031_M1_FINAL_HANDOFF_C76043B9.md:95-96`): *"constrain or explicitly define `LifecycleRecord`
serialization/copy helpers so ordinary delegated Pydantic helpers cannot omit outer fixture
provenance"*.

**Options.**

| Option | Consequence |
|---|---|
| **6-A** — Restrict `__getattr__` delegation to exactly `LifecycleEvent.model_fields` (Sol's stated smallest repair). | Field compatibility is preserved; `model_dump`, `model_copy` and `copy` stop resolving at all and raise `AttributeError` instead of silently returning a degraded object. Loud failure replaces quiet provenance loss. |
| **6-B** — 6-A plus one explicit provenance-preserving serializer on `LifecycleRecord`. | Callers that legitimately want a dict get a complete one, including `source_kind` and `authoritative`. Slightly larger surface. |
| **6-C** — Stop delegating entirely; expose `record.event` only. | Cleanest boundary, but it breaks every existing field access in the module and the focused suite, far beyond the declared R20 ceiling (`R20_CORRECTIVE_SCOPE.md:7`: *"prevent special/dunder protocol delegation while preserving ordinary event-field compatibility"*). |

**Recommended answer: 6-B**, and — importantly — **do not run it alone.**

*Reasons.* 6-A alone converts a silent degradation into a loud `AttributeError`, which is the right
direction, but it leaves callers with no supported way to serialize a record; 6-B closes that
without widening anything. 6-C exceeds the repair ceiling the Lead already declared.

*Why not alone.* Any change to reviewed executable or test bytes voids the exact review set.
`P031_HANDOFF.md:126-131` is explicit: *"If Claude changes any reviewed executable/test/package
content, freeze a new exact candidate and repeat the binding T0 roster: independent `gpt-5.6-sol`
`xhigh`, exact `claude-opus-5` `xhigh`, and coordinated `gemini-3.7-flash-high` supplemental
corroboration after both flagships accept."* That roster — including a Mentor-coordinated Gemini
window — is the real cost. This item should therefore be batched with whatever engineering the
owner's answers to Items 3-5 require — including OD-10's test repair and the report-disclosure edits
envelope 7 and Item 5(b) condition 2 name — and with the other deferred optional nits the Lead listed
(`P031_M1_FINAL_HANDOFF_C76043B9.md:97-102`): the same-epoch test assertions, missing-backup-parent
error normalization (`ledger:1111-1115`), an explicit `BEGIN` in `replay()` (`ledger:1008-1014`),
tightened failing-check assertions, DDL duplication between `ledger:128-161` and `ledger:334-368`,
and keeping the CLI report-only (`ledger:1283-1292`).

---

### Item 7 — authorized current-head refresh, `03_QUANTLENS/HANDOFF.md` reconciliation, and the protected acceptance path

**Requirement, quoted** (`P031_HANDOFF.md:115-116`):

> "any authorized current-head refresh plus `03_QUANTLENS/HANDOFF.md` reconciliation, followed by
> the protected acceptance path"

**What exists today — verified in the V1 drafting lane, not re-run here.** Local `origin/master` is
`fcac0ac67cf2682693ad28138b1a56e15a0846f2`; the candidate is **19 behind, 3 ahead**
(`git log` counts). The overlap is exactly one path,
`MTC_COMMAND_CENTER/03_QUANTLENS/HANDOFF.md`, changed upstream by `e10936d4`
(*"docs(p022): record merged reduced milestone"*) and `a5515ff3` (*"docs(p022): record reduced
tracker acceptance"*), and by the candidate in `854ffea2` and `901f89bc`. No executable or test path
overlaps.

The exact Opus review already raised this as its one required non-code correction, F-1
(`reviews/P031_M1_CLAUDE_OPUS5_MAX_REPORT_C76043B9.json:1`): the packet's freshness sentence
(`reviews/P031_M1_REVIEW_PACKET_C76043B9.md:82-84`) claims *"7 commits … with zero overlap"*, which
was true when frozen and is no longer; Opus reproduced a real `git merge-tree` conflict on that one
documentation path, judged it *"upstream drift that appeared after the packet was frozen, not a
defect in the reviewed deliverable"*, and declined to let it force `REQUEST_CHANGES`. The Gemini
adjudication reached the same disposition (`P031_M1_GEMINI_ADJUDICATION_C76043B9.md:59-60`).

**A second collision, outside P031's control.** `DECISIONS.md` is a three-way collision: P013, P031
and the CT13 takeover branch all append rows to the same table from the same base blob `4d5c3dfc`,
and all three are unmerged
(`P013_DEPENDENCY_ADOPTION_MAP_DRAFT.md:409`, `:418-420`). P031 cannot resolve that alone; it is an
integration-ordering question across lanes.

**Classification: ENGINEERING plus an AUTHORITY gate.** The reconciliation itself is mechanical. The
authority is not: `P031_HANDOFF.md:41-43` lists *"push, PR, merge"* among the things **not**
authorized, and `P031_M1_FINAL_HANDOFF_C76043B9.md:134-135` says to *"reconcile
`03_QUANTLENS/HANDOFF.md` before the protected current-head acceptance path"* only *"when the owner
separately authorizes an integration refresh"*.

**The decidable question: refresh now, or preserve `c76043b9`?**

| Option | Consequence |
|---|---|
| **7-A** — Preserve `c76043b9` unchanged; reconcile only when integration is authorized. | Keeps the complete exact review set (Sol `xhigh`, Opus `xhigh`, three coordinated Gemini slices) valid. The drift is documentation-only and its failure mode is loud — Git refuses to auto-merge — so nothing can be silently wrong. Drift grows while waiting; the guard limit is 30 commits and the candidate is at 19 (`P031_HANDOFF.md:15`). |
| **7-B** — Refresh onto `fcac0ac6` now and re-run the full T0 roster. | Removes the drift and the packet's stale sentence. Costs the entire roster including a Mentor-coordinated Gemini window (`P031_HANDOFF.md:126-131`), to fix a documentation conflict, with the `DECISIONS.md` three-way collision still unresolved afterwards. |
| **7-C** — Refresh only the one documentation path. | Any commit changes the candidate id, so this still costs a new exact candidate and re-review under `P031_HANDOFF.md:126-131` — most of 7-B's cost for part of its benefit. |

**Recommended answer: 7-A**, until the owner's answers to Items 3-5 require engineering; then fold
the refresh, the `HANDOFF.md` reconciliation, and Item 6's tightening into **one** new exact
candidate and **one** T0 roster.

*Reasons.* Every refresh invalidates the exact review set, so the number of refreshes should be
minimized, not the drift. The overlap is one documentation file with a loud failure mode, already
identified by two independent reviewers, and `P031_M1_FINAL_HANDOFF_C76043B9.md:132` already
directs: *"Preserve `c76043b9` as the reviewed fixture-engineering checkpoint."* The 30-commit guard
limit is the one thing that can invalidate 7-A: if the candidate approaches it before the owner
answers, the refresh becomes forced rather than chosen.

*Not P031's call:* the `DECISIONS.md` three-way collision needs a cross-lane writer order (P013 /
P031 / CT13 takeover). Recorded here, not decided here.

---

## 3. Consolidated owner approval request

Every row below needs an **owner** answer; nothing here can be closed by engineering alone.
**OD-1 through OD-11 are definitions or semantic choices reserved to the owner.** **OD-12 is not a
semantic question** — Item 7 is classified ENGINEERING plus an AUTHORITY gate, and OD-12 asks only
for the sequencing/authority call that no one else may make: `P031_HANDOFF.md:41-43` withholds push,
PR and merge authority, and `P031_M1_FINAL_HANDOFF_C76043B9.md:134-135` defers reconciliation until
*"the owner separately authorizes an integration refresh"*. It is admitted here because the owner
must answer it, not because it is a definition. **Item 1 is excluded** (it is an evidentiary
dependency, not a decision) and **Item 6 is excluded** (it is engineering under existing repair
authority). Recommendations are repeated verbatim from the sections above; each cites the section
that justifies it.

| Ref | Decision requested | Recommended answer | Cost if approved | Section |
|---|---|---|---|---|
| **OD-1** | Worthiness check-set ratification | **3D** — decouple: keep the guard fail-closed and unratified; move "ratified worthiness version" from an M1 *acceptance* precondition to an *operating* precondition on writing a real `CAPTURED -> TRIAGED` record. Ratify later with **3B**'s content (v0.1's seven criteria + explicit verdict rule + per-criterion D026 fixtures). | Amend `OD-20260912-P031-M1-SEQUENCING` (`C:/tmp/P031_M1_20260913/DECISIONS.md:18`) and the matching paragraph at `brief:298`. **No code change, but not costless:** both files are among the eight reviewed package paths (`reviews/P031_M1_REVIEW_PACKET_C76043B9.md:36`, `:41`), so amending them inside the candidate changes reviewed package content under `P031_HANDOFF.md:126-131`; and `fold:9` recommends a fresh G1 acceptance round over materially amended documents before G1-IA. Whether this amendment qualifies is unresolved (§5 item 12). | Item 3 |
| **OD-2** | `DEMOTED` target rung and issuing authority | **1B** — the writer supplies `next_state`; the ledger validates strict descent on the ladder order at `ledger:94-98` and an unchanged `deployment_identity_hash`. Assign `DEMOTED` to `MULTI_WORKER_SUPERVISOR`. | Engineering + new candidate + T0 roster. | Item 4, envelope 1 |
| **OD-3** | `CHALLENGE` incumbent-identity carrier | **2A** — add a nullable challenged-incumbent identity field to `LifecycleEvent` under **WP-P0-04**; keep `CHALLENGE` fail-closed until it exists. Also name the issuing writer class (the design points at the challenger's own writer, not the Promotion Authority). | Blocked on WP-P0-04 authority. The envelope stays fail-closed after the answer (§4 item 2). | Item 4, envelope 2 |
| **OD-4** | Atomic two-candidate succession | **3D now** — ratify the current repository-wide refusal as the deliberate interim (stricter than the design because `family_id` is not on `LifecycleEvent`); adopt **3A** (two events, one transaction) when WP-V3-03 is built. | Owner's word only, now. | Item 4, envelope 3 |
| **OD-5** | `REJECTED` failed-gate purpose | **4A** — writer-supplied `check_set_purpose` from the declared set, validated against the candidate's rung, with `check_set_version`, `evaluation_run_hash` and non-empty `failing_checks` all mandatory. Restore `("REJECTED", "RE_ENTRY", "CANDIDATE")` in the same answer. | Engineering + new candidate + T0 roster. | Item 4, envelope 4 |
| **OD-6** | Ambiguous capacity-withholding target | **5C** — take the target from the supplied `check_set_version`'s purpose instead of inferring it from `previous_state`. | Engineering; no shared-contract change. | Item 4, envelope 5 |
| **OD-7** | Deployment-refresh landing state | **6A** — the candidate returns to `FROZEN` under the new composite; revocation stays silent-by-construction. | Engineering + one relaxation of `ledger:657-658`. | Item 4, envelope 6 |
| **OD-8** | Evaluation-run candidate scope | **7A** — ratify as implemented: one `evaluation_run_hash` binds to exactly one `candidate_id` forever. | Owner's word only. No code change. The report keeps printing `"EVALUATION RUN CANDIDATE SCOPE: UNRESOLVED"` (`ledger:1266`) until a separately authorized ledger edit, which is engineering + new candidate + T0 roster. | Item 4, envelope 7 |
| **OD-9** | `RETIRED -> RE_ENTRY` | **5a-C** — keep the transition, gate it on a sixth owner-only trigger class with a mandatory recorded one-sentence external-change reason; keep every existing constraint. | Engineering + one new shared trigger value. | Item 5(a) |
| **OD-10** | Same-epoch reuse across distinct check-set purposes | **5b-A** — ratify as implemented (allowed within an epoch; refused across epochs and across candidates), conditional on giving `test:2192-2288` real assertions and closing the report's disclosure gap. | Owner's word **plus a change to reviewed test bytes**. The conditioning repair edits `test_p031_lifecycle_ledger.py`, which under `P031_HANDOFF.md:126-131` voids the exact review set: new exact candidate + full T0 roster. Not an owner's-word-only answer. | Item 5(b) |
| **OD-11** | What "P0-13 provenance *actually consumed* by P031" means for M1 acceptance | **2C** — optional configured catalog: refuse an `evaluation_run_hash` absent from an accepted catalog when one is supplied, fail closed on catalog-backed claims when none is. **2B** if no further engineering is wanted. | Under 2C: engineering + new candidate + T0 roster, **plus** amending `G1_SCOPE_AND_CONTRACT.md:74` (*"No real TrialRecord bytes are consumed in this slice"*) and the fixed seam at `:20`, **plus** an owner definition of *"claims catalog-backed evidence"* (undefined here; its widest reading would refuse every non-Registrar ladder append — `ledger:631-632`). Under 2B: a wording amendment to `P031_HANDOFF.md:107`. | Item 2 |
| **OD-12** | Refresh now or preserve `c76043b9` (sequencing and authority, not semantics) | **7-A** — preserve; fold the refresh, the `HANDOFF.md` reconciliation and Item 6's tightening into one new candidate and one T0 roster once OD-1..OD-11 are answered. | None now; watch the 30-commit guard limit (currently 19). | Item 7 |

**Two of these cost nothing but the owner's word** — OD-4 and OD-8. Answering both removes **two** of
the seven envelopes from the acceptance list — envelope 3 (ratified in its current,
stricter-than-design interim form) and envelope 7 — and changes no reviewed executable, test or
package byte. Neither answer updates the report's `unresolved_lifecycle_contracts` disclosure
(`ledger:1259-1267`): that list is seven hardcoded strings and editing it is engineering.

**Seven of them change reviewed executable or test bytes** — OD-2, OD-5, OD-6, OD-7, OD-9, **OD-10**
and (under 2C) OD-11. OD-10 belongs in this group, not in the previous one: the ratification itself is
free, but the test repair it is conditioned on (`test:2192-2288`) changes reviewed test content.
Under `P031_HANDOFF.md:126-131` each such change requires a new exact candidate and the full T0
roster, so they should be answered as one batch and implemented once, not incrementally.

**The remaining three cost something else.** OD-1 changes no executable or test byte but amends two
reviewed documentation paths, with `fold:9` in view (see its cost cell). OD-3 is blocked on WP-P0-04
authority and leaves its envelope fail-closed whatever the owner answers. OD-12 costs nothing while
it preserves `c76043b9`.

**A governance note the owner should be aware of.** The P031 decision row exists only on the
candidate's own unmerged branch (`C:/tmp/P031_M1_20260913/DECISIONS.md:18`). The shared
`C:/CT13/DECISIONS.md` contains **no** row naming P0-31, P031, worthiness or the lifecycle ledger: a
case-insensitive search of that file for those four terms returns **zero** rows. (`C:/CT13/DECISIONS.md:18`
is the unrelated `OD-20260911-MATERIALIZER-1`; the nearest lifecycle-sounding row, D026 at
`C:/CT13/DECISIONS.md:45`, matches only the looser word *"lifecycle"* in *"liveness/lifecycle
contract"* and names no P031 subject.) So none of the P031 sequencing decision is visible in the
shared tree today, and `DECISIONS.md` is simultaneously a three-way unmerged collision between P013,
P031 and the CT13 takeover branch (`P013_DEPENDENCY_ADOPTION_MAP_DRAFT.md:409`). Wherever the owner
records answers to OD-1..OD-12, the writer order for that file needs coordinating; this lane does not
decide it.

**Nothing in this section is an approval, and recording an answer to any of it authorizes no
engineering, no Git mutation, no integration and no acceptance** — each still needs its own
authorization under the existing gates.

---

## 4. What remains blocked on P0-04 / P0-13 provenance regardless of the answers

Even if the owner answered every one of OD-1 through OD-12 today, and every recommended engineering
change were built and reviewed, Milestone 1 acceptance would still be blocked. This section states
what does **not** move.

**1. The two provenance dependencies themselves.** `P031_HANDOFF.md:106-107` requires *"exact
accepted WP-P0-04 lifecycle/identity/writer provenance"* and *"exact accepted WP-P0-13
TrialRecord/catalog provenance actually consumed by P031"*. No lifecycle-semantics answer supplies
either. `G1_SCOPE_AND_CONTRACT.md:73` forbids the shortcut: acceptance *"is not inferred from source
presence"*. The P013 notice `da1fb184c71e1ae65e2e348758af7f1a84a1cfbd` does not help —
`P031_HANDOFF.md:118-121`: *"it grants no caller integration/full-P013 acceptance and is not in this
candidate. Do not infer dependency satisfaction."*

**2. Two envelopes reach past P031 for new P0-04 contract fields — and one of the two cannot be
closed by any owner answer.**

- **Envelope 2 (`CHALLENGE`)** needs a challenged-incumbent identity field. None exists anywhere in
  `contracts/mtc_contracts/`. Under the recommended **2A** this is WP-P0-04's work, and
  `G1_SCOPE_AND_CONTRACT.md:11` forbids P031 from editing shared contracts. **No owner answer closes
  this envelope**, which is why it is the exception named at the end of this section.
- **Envelope 3 (succession)** is closable now, but only in its interim form: OD-4 ratifies the
  repository-wide refusal the candidate already implements. If the owner ever wants the design's
  actual rule — *"never two live members of one family"* (`brief:1548`) — that needs `family_id` on
  `LifecycleEvent`. It exists in `identity.py:144`, `package.py:31` and `trials.py:22`, but not on
  the event (`execution.py:168-188`). Until then the ledger can only enforce the blunter global rule
  it enforces today (`ledger:595-606`).

**3. No authoritative record can exist in this ledger at all, by construction.** `source_kind` is
refused unless it is exactly `"FIXTURE"` (`ledger:480-481`), and the derived view's schema enforces
it twice with SQL `CHECK` constraints — `source_kind = 'FIXTURE'` and `authoritative = 0`
(`ledger:157-158`, restated at `ledger:359-360`). Widening that is outside Milestone 1's authorized
scope (`P031_HANDOFF.md:41-43`). So every report this candidate can produce will keep reporting
`authoritative_records = 0` (`P031_M1_FINAL_HANDOFF_C76043B9.md:62-63`) no matter what is ratified.

**4. P0-13's own chain is blocked behind P0-20, several layers deep.** From the independent P013
lane: B-01 (*"`P020-ACCEPTANCE-AND-CANONICAL-RECEIPT`"*) is **NOT SATISFIED**
(`P013_DEPENDENCY_ADOPTION_MAP_DRAFT.md:327`, evidence at `:331-336`, including *"WP-P0-20 is
therefore not package-accepted or merge-ready"*), and B-04, B-06, B-07, B-12, B-15 and B-17 are each
recorded unsatisfied at `:352-357`. For B-04, B-12 and B-17 the **shape** is ratified and it is
adoption that is unsatisfied — but not the same half in each row: *"producer adoption NOT
SATISFIED"* for B-04 (`:352`) and B-12 (`:353`), *"receipt production and reader adoption NOT
SATISFIED"* for B-17 (`:355`). P031 sits downstream of all of it.

**5. There is still no consumption seam.** Even with accepted P0-13 bytes, `p031_lifecycle_ledger.py`
contains zero references to any P013 symbol (`P013_DEPENDENCY_ADOPTION_MAP_DRAFT.md:244-256`).
Satisfying *"actually consumed"* is engineering that has not been authorized, which is what OD-11
asks the owner to scope.

**6. The full T0 review path is unaffected by any of this.** Fresh exact `gpt-5.6-sol` `xhigh`,
exact `claude-opus-5` `xhigh`, coordinated `gemini-3.7-flash-high` after both flagships accept, and
independent Lead reproduction remain required on whatever candidate is finally proposed
(`P031_HANDOFF.md:126-131`; `P031_M1_SCOPE_AND_STATUS.md:691-705`).

**7. Milestones 2 and 3 stay untouched.** `P031_HANDOFF.md:120-121`: *"M2 seed/import and M3 consumer
cutover/retirement remain unstarted and unauthorized."* Nothing in this document changes that, and
`plan:663` keeps any deletion behind a separate owner authorization under gate `G8` against an exact
enumerated target list.

In short: the owner's answers can close **six of the seven envelopes** — envelopes 1, 3 (in its
interim form), 4, 5, 6 and 7, four of them (1, 4, 5, 6) only after the engineering those answers
authorize — and **both Item-5 questions** (OD-9 after engineering, OD-10 after the reviewed-test
repair), and can make the acceptance list honest. **Envelope 2 is the exception: no owner answer
closes it.** Under the recommended 2A it stays fail-closed until WP-P0-04 carries the
challenged-incumbent identity field, as item 2 above records. The answers cannot close Items 1 and 2,
and they cannot make Milestone 1 acceptable on their own.

---

## 5. NOT VERIFIED

This section is deliberately non-empty. Each entry is something a lane did **not** establish. Items
1-12 are the V1 drafting lane's; items 13-19 are the V2 correction lane's; items 20-22 are the V3
correction lane's. Every pass added only — nothing has ever been removed.

1. **Worktree cleanliness was not re-verified.** No `git status` and no `git diff` were run, per this
   lane's write boundary. The "clean; staged 0" fact is taken from `P031_HANDOFF.md:13` and
   `reviews/P031_M1_REVIEW_PACKET_C76043B9.md:14`.
2. **No test, script, demo, D026 harness, CLI or ledger was executed.** Every GREEN result quoted
   here — 101 focused tests, 50 shared contracts, compile, reader self-check, Ruff F, diff-check,
   repository guard, fixture demo — is transferred evidence from
   `P031_M1_FINAL_HANDOFF_C76043B9.md:54-67` and the review reports. This lane reproduced none of it.
3. **No SHA-256 in any handoff, packet or review was recomputed.** Diff size/hash, report hash, blob
   identities and review-artifact hashes are quoted, not verified.
4. **The three Gemini slice reviews were not read individually.** Only the Lead adjudication
   (`P031_M1_GEMINI_ADJUDICATION_C76043B9.md`) and a directory listing of
   `reviews/p031_c76043b9_gemini_slices/` were inspected. The preserved supervisor verdict-format
   `FAILED` flags and the phase-2 failed canonical-root lookup are reported as the adjudication
   records them, not independently checked.
5. **The GitHub ticket resolutions #59-#65 were not read.** `WAYFINDER_LIFECYCLE_FOLD_2026-08-23.md:5`
   states that *"The full detail of every decision lives in its ticket's resolution comment; this
   document indexes and applies, it does not restate."* Every option and recommendation in Item 4 and
   Item 5 is judged against the fold and brief summaries only. **A ticket resolution could refine or
   contradict any of them** — in particular the `DEMOTED` target, the `CHALLENGE` issuer and the
   `RETIRED` re-entry rule. These should be checked against the tickets before the owner records an
   answer.
6. **WP-P0-04's acceptance state was not established anywhere.** No P0-04 handoff exists under
   `C:/tmp/CLAUDE_TAKEOVER_20260913/` (directory listing: P012, P013, P020, P021_P030, P022, P031
   only). This document says only that P031 does not have the provenance, not what P0-04's status is.
7. **The P013 dependency map's own claims were not independently re-derived.** Sections 3.4, 4.0,
   4.1 and 5 of `P013_DEPENDENCY_ADOPTION_MAP_DRAFT.md` are cited as that lane's findings. It is
   itself a DRAFT.
8. **No `git merge-tree` or merge simulation was run here.** The `03_QUANTLENS/HANDOFF.md` conflict
   is reported as Opus F-1 reported it; this lane independently confirmed only that both sides changed
   the path (`git log` with a path filter) and the 19/3 divergence.
9. **Line numbers are checkout-specific.** All `ledger:`, `test:`, `brief:`, `fold:`,
   `P031_M1_SCOPE_AND_STATUS.md:` and `execution.py:` citations are against the worktree
   `C:/tmp/P031_M1_20260913` at `c76043b9`; `plan:` citations are against `C:/CT13`, whose copy of the
   plan differs from the candidate's amended copy. They will not match other checkouts.
10. **No consequence of any recommendation was simulated.** The options were reasoned from the
    ratified text and the current code; none was prototyped, and no estimate of implementation effort
    beyond "requires a new candidate and the T0 roster" is offered.
11. **This lane is not a reviewer and not the Lead.** Nothing here is a review verdict, a disposition,
    an acceptance, a ratification or an authorization. The candidate's behavior is unchanged and no
    file in `C:/tmp/P031_M1_20260913` was written.
12. **Whether the owner may amend `OD-20260912-P031-M1-SEQUENCING` (recommendation 3D) without a
    fresh G1 round was not determined.** `fold:9` records that material amendments to the accepted
    set carry a recommendation for a fresh G1 acceptance round; whether moving an acceptance
    precondition qualifies is outside this lane.
13. **The V2 correction lane ran no Git command of any kind, no test, no script, no D026 harness, no
    CLI and no network or provider call.** Every §1 identity row the V1 lane derived from
    `git rev-parse` / `git log` — candidate HEAD, commit count, changed-path count, `origin/master`,
    the 19/3 divergence and the upstream overlap — was **not** re-verified in V2. They stand exactly
    as V1 and the handoff record them.
14. **V2 re-verification was broad but not exhaustive.** Every source named by a Grok finding, and
    every `file:line` pin this document touches, was re-opened and checked against the file as it
    stands now; a wide sample of the pins V2 did not touch was checked as well. The V1 draft's full
    citation set was **not** re-walked line by line, and the Grok report's own sampled citation table
    (its §(b), 133 rows) is that auditor's sample, not this lane's verification.
15. **The Grok audit read a different copy of the packet.** Its subject was
    `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P031_LIFECYCLE_DECISIONS_20260913.md`,
    whose five-line Lead audit header (`:1-5`) shifts every line number by +5 relative to the V1
    draft. The two copies were compared only by that header, by the +5 offset holding at several
    sampled anchors, and by their line counts and line endings (987 CRLF lines versus 982 LF lines);
    they were **not** diffed byte for byte, so a divergence inside the recorded copy's body would not
    have been seen here. One Grok pin (finding 3's "851") lands on the OD-7 row rather than the OD-8
    row its own quoted text names; the finding was dispositioned against the text it quotes.
16. **Grok finding 6 was rebutted against the file as it stands now**
    (`P013_DEPENDENCY_ADOPTION_MAP_DRAFT.md:256`). No copy of that file exists under `C:/CT13`, and
    whether the auditor read some other copy or state was not established; this lane can only state
    what the file says now.
17. **No ratified line was found that requires the challenged incumbent
    `deployment_identity_hash` to live on `LifecycleEvent` rather than in ledger-local evidence.**
    `brief:2223` does not say it (see envelope 2). The recommendation of 2A rests on `plan:320`'s
    assignment and on contract-level typing, and the search for a stronger line was bounded to the
    sources this packet already cites.
18. **`test:2192-2288` was read, not executed.** That `verify_integrity()` passes for those three
    ledgers is the transferred 101-GREEN evidence, not an observation made here. Likewise, that a
    ledger with no configured active version refuses with `CHECK_SET_PURPOSE_MISMATCH` (Item 3) is
    read from `ledger:614-618` and `ledger:306-330`, not observed in a run; the fixture proof at
    `test:544-547` covers the missing-version and inactive-version cases, not the empty-mapping case.
19. **Whether an owner amendment under OD-1 would be written into the candidate's copies of
    `DECISIONS.md` and the brief (reviewed package paths) or recorded elsewhere was not
    determined.** The cost stated in OD-1's cell is the in-candidate cost; a record kept outside the
    candidate would leave the candidate's own copies saying something the owner has superseded.
20. **The V3 correction lane ran no Git command of any kind, no test, no script, no D026 harness, no
    CLI and no network or provider call either.** The §1 identity rows the V1 lane derived from
    `git rev-parse` / `git log` — candidate HEAD, commit count, changed-path count, `origin/master`,
    the 19/3 divergence and the upstream overlap — were **not** re-verified in V3. They stand exactly
    as V1 and the handoff record them; item 13 above still applies unchanged.
21. **V3 re-verification was deliberately narrower than V2's.** It covered every source named by a
    re-audit finding, every source cited by the lines V3 edited, and the packet-internal statements
    those lines contradicted. The rest of the citation set was **not** re-walked in V3: it rests on
    the V1 drafting pass, on the V2 re-verification (item 14 above) and on the re-audit's own sampled
    citation table (its §(c), 75 rows), which is that auditor's sample and not this lane's
    verification.
22. **The rebuttal of re-audit NEW-2 is bounded to the file as it stands now.**
    `p031_lifecycle_ledger.py:1237` was read twice, by two independent tools, in
    `C:/tmp/P031_M1_20260913/MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py` — the
    only copy of that module found under `C:/tmp/P031_M1_20260913`, `C:/CT13`,
    `C:/tmp/P031_LEAD_20260912`, `C:/tmp/P031_M1_START_20260912` and
    `C:/tmp/CLAUDE_TAKEOVER_20260913`. No Git object was inspected and no other checkout was
    searched, so whether the auditor read a different copy or state was not established; this lane
    can only state what the file says now.
