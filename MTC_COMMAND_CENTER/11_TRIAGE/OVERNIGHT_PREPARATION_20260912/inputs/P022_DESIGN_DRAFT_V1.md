# WP-P0-22 — Family-lineage and observation-leakage control — DESIGN DRAFT v1.11

**Status:** DESIGN ONLY. No code, no ledger created, no registry edit, no commit. Repository read
only at `C:\WFMERGE54`. This draft is re-audited after WP-P0-13 accepts, before any build
(lane spec, authorization edge).

**Provisional-label convention.** Every choice that depends on the WP-P0-13 trial catalog /
evidence-store contract is tagged `PROVISIONAL-ON-P013`. **Blanket scope (added v1.1, F-2):**
every §1.3 resolution step and every §2.3 writer class that reads the P0-13 trial catalog is
`PROVISIONAL-ON-P013` whether or not the tag is repeated at that line. W51 is drafting that
contract in parallel; per lane spec its in-progress draft was not read. These choices are
designed against plan text only and will move when P0-13 accepts.

**Vocabulary (C-7):** probe, variant, modified copy, DETECTED / NOT DETECTED, refused, accepted.

---

## Change log — v1 → v1.1

Fold of detection audit `DETECT_P24_P022_DRAFT.md` (lane P24, 12 findings — 0 High, 3 Medium,
9 Low). All 12 dispositioned **FIXED**; no finding refuted, none deferred as honest-CANNOT.
The draft remains DESIGN ONLY and its build stays gated on WP-P0-13 acceptance + re-audit (OQ-10).
`PROVISIONAL-ON-P013` labels are unchanged in meaning and were widened, not narrowed (F-2).

| # | Sev | Finding (short) | Disposition | Where changed |
|---|---|---|---|---|
| F-1 | MED | §5(a) makes only Producer 1 falsifiable; Producer 2 (`ACCESS_RECONCILIATION`) is self-checking w.r.t. its own coverage | **FIXED** — added a Producer-2 falsifying probe, a by-construction coverage argument, and an explicit residual class routed to §3.3 → ledger state INCOMPLETE; full falsifiability of Producer 2 is conceded impossible and backstopped fail-closed via §3.3 positive-completeness (refinement folded into OQ-9) | §5(a), §3.3, §6.1, OQ-9 |
| F-2 | MED | catalog-dependent choices not individually `PROVISIONAL-ON-P013` | **FIXED** — blanket scoping sentence in the convention block; tags added to §1.3 step 2 and §2.3 classes 1/2/4/5 | header convention, §1.3, §2.3 |
| F-3 | MED | no concurrency model for the ledger writer (5 writer classes, one hash chain, wall-clock-monotonic `observed_at`) | **FIXED** — §2.4 now specifies a single serialising appender; §2.1 ordering rule restated as append-order, `observed_at` informational + per-writer-monotonic only | §2.1, §2.4 |
| F-4 | LOW | §5(b) fixtures b2/b3 not runnable now, not marked blocked | **FIXED** — b2 → OQ-8, b3 → OQ-9 annotated "not runnable until the named blocker resolves"; b1 and b4 marked runnable-now | §5(b) |
| F-5 | LOW | §2.1 `family_id` "resolved at observation time" contradicts §1.5 freeze-time-once rule | **FIXED** — row reworded to "records the package's frozen `family_id` (may be `FAM-UNKNOWN`)" | §2.1 |
| F-6 | LOW | mis-cite `plan:422` for the `mcc_readonly` layer | **FIXED** — corrected to `plan:420` (verified: `mcc_readonly` phrase at `:420`; `:422` is the map #123 / Perspective amendment) | §2.3 class 1 |
| F-7 | LOW | `brief:1432` labelled "§6.7" in §3.1, "§6.6 rule 2" in §2.1 | **FIXED** — "§6.6 rule 2" used throughout (verified: line 1432 sits under the §6.6 header `:1427`; §6.7 header is `:1447`) | §3.1 |
| F-8 | LOW | `STRATEGY_RESEARCH_REGISTRY.json:1-65` does not evidence "63 `STGxxx` entries" | **FIXED** — cite now names the count method (`grep -c '"strategy_id": "STG'` → 63, verified) and the last entry `:3430`; `:1-65` covers only STG001 | §0 inputs table |
| F-9 | LOW | `plan:317-340` overruns the WP-P0-04 block | **FIXED** — corrected to `plan:317-333` (verified: `:334` is the `### WP-P0-05` header) | §0 inputs table |
| F-10 | LOW | D-1 over-frames a dependency listing as a "pending" claim | **FIXED** — D-1 downgraded to the D-5 "no conflict, recorded for completeness" form; no plan line asserts P0-04 is incomplete | Discrepancies D-1 |
| F-11 | LOW | §5(c) present-tense "real command output recorded" in a design-only draft | **FIXED** — reworded to "the fixture, once built, records real command output (D026 shape)" | §5(c) |
| F-12 | LOW | producer-token folder examples uncited (C-4) | **FIXED** — registry line cites added: `ql_alpha` `:10`, `ql_avwap_brian` `:180`, `ql_connell` `:389`, `ql_deepak` `:491`, `ql_episodic_pivot_christian` `:642` | §1.2 |

**Verified against the repository during this fold (read-only, `C:\WFMERGE54`, branch `master`,
HEAD `50580df1`):** `MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:310-348`,
`:405-438`, `:524-543`, `:943-953`; `MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1424-1453`,
`:3068-3081`; `contracts/mtc_contracts/identity.py:140-154`;
`05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json` (3493 lines; `strategy_id` count 63; last STG063 `:3430`;
`source_folder` lines 10/70/125/180/231/284/338/389/491/541/642).

---

## Change log — v1.1 → v1.2

Fold of detection audit `DETECT_N74_P022_V11.md` (lane N74, detection round 2, 5 findings —
0 High, 3 Medium, 2 Low; no acceptance verdict). All 5 dispositioned **FIXED**; 0 refuted,
0 honest-CANNOT. The draft remains DESIGN ONLY and its build stays gated on WP-P0-13 acceptance
+ re-audit (OQ-10). `PROVISIONAL-ON-P013` labels unchanged in meaning. No finding closed by
narrowing a label or a claim: N74-F1 and N74-F3 **widen** the fail-closed surface, N74-F2 **adds**
production paths, N74-F3 **adds** a named blocker and marks a gate row BLOCKED.

| # | Sev | Finding (short) | Disposition | Where changed |
|---|---|---|---|---|
| N74-F1 | MED | Producer-2 blind spot not actually routed fail-closed: §3.3 positive-completeness only demands attestation for intervals where a reader was **known** to be running, so a read both producers miss is never flagged; §5(a) still claims Probe 2 is "routed to zero" | **FIXED** — §3.3 "positively established completeness" rewritten to be **continuous over all of `W_B`** (coverage by a ledger row **or** a no-read attestation required for every sub-interval, not only known-reader intervals); §5(a) Probe 2 disposition point 3 and the closing summary reworded to drop the "routed to zero" claim and state the affected window is **incomplete** until continuous-completeness attestation, an independent unavoidable copy/export producer, or a prevention boundary exists; OQ-9 extended to name that three-way choice; §6.1 enumeration row updated | §3.3, §5(a), §6.1, OQ-9 |
| N74-F2 | MED | W66's two-named-producer discipline present only in §5(a); b1–b4, §5(c), and the §6.1 map rows name conditions/outcomes but no independent truth producer + verdict producer — a fixture builder can feed the same derived value to setup and expected result | **FIXED** — §5(b) preamble + each of b1–b4, §5(c), and every §6.1 A-7d row now name the **two independent producers** (immutable fixture timeline / corruption manifest = truth-side; resolver / ledger verifier / gate = verdict-side), the **compared operands**, and a **truth-side-only mutation variant** that must be DETECTED by the verdict-side producer | §5(b), §5(c), §6.1 |
| N74-F3 | MED | §2.4 titled "enforced structurally" but relies on interface/permission conventions (only-writer declaration, lock, read-only files, add-only dir, `append()`-only library) + a planned-and-unbuilt anchor; hash chain only detects an unrecomputed edit; §6.1 still asserts edit/delete → CI RED | **FIXED** — §2.4 rewritten to specify the enforcing boundary: clients have **no filesystem write access** to the store; a **distinct appender identity** may create but cannot overwrite/delete retained objects (storage-level deny-update/deny-delete / retention lock); part-file publication and manifest-head advance are **atomic or recoverably journaled**; an **independently controlled immutable anchor must cover the exact head** before evidence counts. New **OQ-11** names the access-control + atomicity contract as a blocker; §6.1 append-only row marked **BLOCKED until OQ-8 + OQ-11** | §2.4, §6.1, OQ-11 (new) |
| N74-F4 | LOW | §1.4 (sentinel satisfies `NonEmptyStr`) and OQ-5 (enforcement gap) are correct, but D-4 says the contract "can neither represent nor enforce" `FAM-UNKNOWN` — overstated; `family_id: NonEmptyStr` (`trials.py:22`) **can** carry the non-empty string `FAM-UNKNOWN` | **FIXED** — D-4 retitled to an **enforcement / semantic-constraint gap**: the current type can carry `FAM-UNKNOWN` but does not define it or bind it to `LIVE_CANDIDATE` refusal | Discrepancies D-4 |
| N74-F5 | LOW | draft says **every** sampled registry row is `heuristic_auto` and concludes every derived-triple family inherits that uncertainty; current registry has `heuristic_auto` **and** `explicit_metadata` | **FIXED** — re-censused this fold (recorded method below): **46 `heuristic_auto` + 17 `explicit_metadata` = 63**; §0 taxonomy-seed row, §1.3 step 3, OQ-6, and D-2 updated to cite both classes; the forced-`FAM-UNKNOWN` rule is **scoped to rows whose producer evidence is heuristic or otherwise unconfirmed**; `explicit_metadata` rows are not treated as heuristic; the canonical-producer question stays open | §0, §1.3, OQ-6, Discrepancies D-2 |

**Verified against the repository during this fold (read-only, `C:\WFMERGE54`, working tree at
commit `c18b6f3e`):**
`MTC_COMMAND_CENTER/05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json` — 3493 lines;
`classification_confidence` census method
`grep -oE '"classification_confidence": *"[a-z_]+"' <file> | sort | uniq -c` →
`heuristic_auto` 46, `explicit_metadata` 17 (63 total = 63 `STGxxx` entries); `heuristic_auto`
still present at `:64` (STG001), `explicit_metadata` present at `:2427` (STG047);
`MTC_COMMAND_CENTER/contracts/mtc_contracts/trials.py:22` (`family_id: NonEmptyStr`, no
allowed-value set); `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:144-154`
(`compute_family_id` returns `f"FAM-{digest[:16]}"`, never `UNKNOWN`);
`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:534-537` (A-7d text, rollback,
non-goals). The v1.1 change-log line records HEAD `50580df1`; the working tree is now at
`c18b6f3e` — see Discrepancies (fold note).

---

## Change log — v1.2 → v1.3

Fold of detection audit `DETECT_G28_P022_V12.md` (lane G28, 1 finding — 0 High, 1 Medium,
0 Low; no acceptance verdict). G28-F01 is **FIXED**; 0 refuted, 0 honest-CANNOT. The parallel
Gemini census `DETECT_GM12_P022_V12.md:28-31` reported 0 findings, but G28 identified a real
internal contradiction between the whole-window rule and fixture `b3`
(`DETECT_G28_P022_V12.md:33-70`). Repository authority controls: plan A-7d and brief rule 8 both
require an absent or incomplete ledger to yield **zero confirmation evidence**
(`MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:534`;
`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1443`; D-15 at
`REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:198`).

| # | Sev | Finding (short) | Disposition | Where changed |
|---|---|---|---|---|
| G28-F01 | MED | §3.3's table zeroed the whole window on a coverage gap, while the completeness prose and `b3` zeroed/subtracted only the uncovered sub-interval, allowing positive confirmation duration from an incomplete ledger | **FIXED** — selected the fail-closed whole-window consequence required by A-7d: one uncovered sub-interval makes the ledger incomplete for all of `W_B`; §3.3 and §5(a) now say `untouched(B) = ∅` for the whole window; `b3` expects duration 0; its non-zero mutation must supply valid coverage over the gap **and every remaining sub-interval**; §6.1 states the same consequence explicitly | §3.3, §5(a), §5(b) `b3`, §6.1 |

The draft remains DESIGN ONLY; build remains gated on WP-P0-13 acceptance + re-audit (OQ-10).
`PROVISIONAL-ON-P013` labels and all owner-gated open values are unchanged.

---

## Change log — v1.3 → v1.4

Fold of detection audit `DETECT_N86_P022_V13.md` (lane N86, 1 finding — 0 High, 0 Medium,
1 Low; no acceptance verdict). N86-F01 is **FIXED**; 0 refuted, 0 honest-CANNOT. The required
shape census of the unqualified runnable-now set found the same label defect in `b4`: both `b1`
and `b4` have a primary zero-duration arm designable now, but their mandatory non-zero mutation
arm requires a positively complete window and is blocked on OQ-9. Both fixtures now carry the
same split status, and neither remains in an unqualified runnable-now set. No fixture semantics,
open-question value, or build authorization changed. The retained literal v1.3→v1.4 unified diff
is `W109_RUN.log:7044-7136`; its before/after content identities are recorded at `:7046`.

---

## v1.5 change log — N96 fold

Fold of detection audit `DETECT_N96_P022_V14.md` (lane N96, 1 finding — 0 High, 0 Medium,
1 Low; no acceptance verdict). N96-F01 is **FIXED**: N96 correctly found that its named evidence
set contained only the v1.3 and v1.4 identities, not independently inspectable change evidence
(`DETECT_N96_P022_V14.md:5-20`). The already-retained W109 run record contains the literal
v1.3→v1.4 unified diff, including before/after content identities and every draft hunk
(`W109_RUN.log:7044-7136`). That diff is now cited at the v1.4 minimality statement above; no
reconstruction or invented value was needed. The shape sweep covered the title, v1.4 change log,
fixture-status preamble, `b1`, `b4`, runnable-now summary, and final v1.4 fold summary; all match
the retained diff, so no design, fixture, open-question, or build-authorization text changed in
this fold.

---

## v1.6 change log — W147 fold

Fold of fresh full-body detection audit `DETECT_N99_P022_V15.md` (lane N99, 6 findings —
0 High, 5 Medium, 1 Low; no acceptance verdict). All 6 are dispositioned **FIXED**; 0 refuted,
0 honest-CANNOT. The draft remains DESIGN ONLY; owner-gated values remain `[OPEN]`, and build
remains gated on WP-P0-13 acceptance + re-audit (OQ-10).

| # | Sev | Finding (short) | Disposition | Where changed |
|---|---|---|---|---|
| N99-F01 | MED | D026 time mutation used `t2' > t2`, which need not cross the skew boundary `t2 + δ` | **FIXED** — clean mutation moved to the actual strict-comparison boundary (`t2' >= t2 + δ`); variants immediately below and at the boundary are required; the arm is BLOCKED ON OQ-7 until `δ` or the single-time-source alternative is ratified | §5(c), §6.1, OQ-7 |
| N99-F02 | MED | §5(c) promised positive evidence without whole-window completeness | **FIXED** — §5(c) is BLOCKED ON OQ-9 and OQ-11; after unblock, both toggle arms receive the same independently verified whole-window coverage so sibling marking is the only changed input | §5(c), §6.1 |
| N99-F03 | MED | first-confident-wins precedence could split one `candidate_id` across families | **FIXED** — narrowed “by construction” to a required resolver invariant; explicit-lineage and candidate-catalog results are compared before either can win; disagreement is refused to `FAM-UNKNOWN`; named two-family conflict variant added | §1.1, §1.3, §6.1 |
| N99-F04 | MED | completeness coverage was not identity-bound | **FIXED** — defined `coverage_key(B)`, relevant ledger-row and scoped-attestation predicates, including the declared-global-domain case; wrong package/family/`D`/`E` variant must be refused | §3.3, §5(b) b3, §6.1, OQ-9 |
| N99-F05 | MED | OQ-9/OQ-11 unblock text alternated between OR and AND | **FIXED** — one `COMPLETENESS-UNBLOCK` Boolean now controls §3.3, §5(a), §6.1, OQ-9, and OQ-11; a single mechanism may discharge both duties only through two independently checked outputs | §3.3, §5(a), §6.1, OQ-9, OQ-11 |
| N99-F06 | LOW | downstream-gate map row lacked producers, operands, and mutation | **FIXED** — narrowed the claim to the family/confirmation precondition and named immutable eligibility input, each exact downstream gate, expected/observed operands, and an invalid→valid truth-side-only variant | §6.1 |

The repeat/count sweep covered the version header; `candidate_id` invariant and resolution order;
all positive-completeness, OQ-9/OQ-11, b3, §5(c), D026, and downstream-gate repetitions; the
open-question/discrepancy/finding summaries. Open questions remain 11; discrepancies remain 5.

---

## v1.7 change log — W159 fold

Fold of detection audit `DETECT_G67_P022_V16.md` (lane G67, 3 findings — 0 High, 2 Medium,
1 Low; no acceptance verdict). All 3 are dispositioned **FOLDED**; 0 disputed. The draft remains
DESIGN ONLY; owner-gated values remain `[OPEN]`, and build remains gated on WP-P0-13 acceptance +
re-audit (OQ-10).

| # | Sev | Finding (short) | Disposition | Where changed |
|---|---|---|---|---|
| G67-F01 | MED | `COMPLETENESS-UNBLOCK` omitted the exact-head-anchor conjunct already required by §2.4/§3.3 (`DETECT_G67_P022_V16.md:49-92`) | **FOLDED** — added OQ-8 to the single predicate and to every complete-window / positive-evidence blocker that used it | §3.3; §5(a); §5(b) b1/b3/b4 and status summary; §5(c); §6.1; OQ-8/OQ-9/OQ-11 (`draft v1.7:484-497`, `:630-683`, `:742-745`, `:790-833`) |
| G67-F02 | MED | `row_hash` had no declared preimage, so the chain-break check did not bind observation fields (`DETECT_G67_P022_V16.md:94-126`) | **FOLDED** — bound the preimage to the ordered list of every declared §2.1 field except `row_hash`, including `prev_hash`; left the canonical byte encoding honestly `[OPEN]` as OQ-12; added field-only, one-row-recompute, and whole-chain-recompute variants | §2.1; §2.4; §5(b) b2; §6.1; OQ-12 (`draft v1.7:306`, `:400-413`, `:641-650`, `:741`, `:834-840`) |
| G67-F03 | LOW | §6.1 said every row named two producers and a mutation, but the non-goals row was inspection-only (`DETECT_G67_P022_V16.md:128-147`) | **FOLDED** — narrowed the preamble to falsification rows and explicitly labelled the non-goals row inspection-only with no A-7d falsification claim | §6.1 (`draft v1.7:734-747`) |

The v1.7 fold adds no numeric threshold, duration, bin edge, or hash value. Open questions are now
12 because the previously unspecified canonical `row_hash` byte encoding is recorded as OQ-12;
discrepancies remain 5.

---

## v1.8 change log — W193 / DS47 fold

Fold of repair patch `DS48_P022_PATCH.md` for the seven findings in the DS47 census.

**Record corrected v1.9 (W196-F01).** Superseded v1.8 wording, retained as the record of what the
W193 lane reported: ~~"Six repairs landed fully; DS47-F03 Patch A was stopped because its quoted
preimage omitted the draft's two-space Markdown continuation indent and therefore did not match
verbatim."~~ That sentence was true of the W193 lane and false of this document. After W193 stopped,
the Lead applied DS47-F03 Patch A by hand, restoring the two-space Markdown continuation indent the
patch quote had omitted. **All seven repairs are in the body.** Patch A's text is present at §5(a)'s
Producer-2 clause and matches `DS48_P022_PATCH.md:144-149` except for that indent — verified by the
W196 verification (`DETECT_W196_P022.md:328-336`) and re-read at the site during this v1.9 fold.
DS47-F03 Patches B–D landed against exact preimages. No checker was invented. The draft remains
DESIGN ONLY; owner-gated values remain `[OPEN]`, and build remains gated on WP-P0-13 acceptance +
re-audit (OQ-10).

| # | Sev | Finding (short) | Disposition | Where changed |
|---|---|---|---|---|
| DS47-F01 | MED | `FAMILY_OBSERVED` marking row had no schema or integrity binding | **FOLDED / BLOCKED** — OQ-13 added and every marking-row consumer names it | §5(c), §6.1, OQ-13 |
| DS47-F02 | MED | self-reported `observed_at` could fire the §4.1 time test without an independent timestamp check | **FOLDED** — Producer-2/Producer-1 reconciliation now refuses a beyond-`δ` mismatch as `MISDATED_OBSERVATION`; predicate remains blocked on OQ-7 | §5(a), §6.1, OQ-7 |
| DS47-F03 | MED | Producer-2 optimizer channel and `OPTIMIZER` linkage were not source-bound | **FOLDED** (record corrected v1.9, W196-F01; superseded cell text retained: ~~"**PARTIAL — PATCH A STOPPED** on a non-verbatim preimage; Patches B–D folded the linkage and OQ extensions"~~). Patch A stopped in the W193 lane on a non-verbatim preimage and was then applied by hand with the two-space continuation indent restored; Patches B–D folded the linkage and OQ extensions | §5(a) Producer-2 clause (hand-applied), §4.1, OQ-3, OQ-7 (superseded cell text retained: ~~"§5(a) source-site label did not land"~~ — it did land) |
| DS47-F04 | MED | family-lineage graph-store immutability was declared but unenforced | **FOLDED / BLOCKED** — OQ-14 added | OQ-14 |
| DS47-F05 | LOW | §3.3 clean-case row omitted the no-contaminating-sibling condition | **FOLDED** — clean case now states the joint absence condition | §3.3 |
| DS47-F06 | LOW | `writer_seq` monotonicity had no consumer or verifier | **FOLDED** — the existing serialising appender now refuses non-monotonic rows | §2.4 |
| DS47-F07 | LOW | `observation_id` had no composition, generator, or uniqueness check | **FOLDED / BLOCKED** — OQ-15 added | OQ-15 |

The three new named blockers are **OQ-13** (`FAMILY_OBSERVED` marking-row schema and integrity
binding), **OQ-14** (family-lineage graph-store binding), and **OQ-15** (`observation_id`
composition, generator, and uniqueness). OQ-3 and OQ-7 are extended, not closed. Open questions
increase 12 → 15; discrepancies remain 5. Earlier version change logs and their historical counts
are retained as superseded records rather than rewritten.

**Scope of these three, as of v1.9 (W196-F02/F03/F04) — this paragraph records the v1.8 titles;
all three were subsequently narrowed, none closed.** OQ-13 is now the marking row's **schema and
store** (its integrity duty is bound to the §3.2/§4.2 recompute); OQ-14 is now the graph store's
**enforcement, head anchor and chain binding** (its contamination-detection duty is bound to the
chain-bound `family_id` cross-check in §4.1); OQ-15 is now `observation_id` **composition and
generator** (its uniqueness duty is bound to the single serialising appender in §2.4). See the v1.9
change log below. Open questions remain 15.

---

## v1.9 change log — W197 / W196 refold

Fold of fold-verification `DETECT_W196_P022.md` (lane W196, 10 findings — 0 High, 6 Medium,
4 Low; verdict NOT-CONVERGED). All 10 are dispositioned **REPAIRED**; 0 disputed. The verification
was produced by a family that authored neither the census, the patch, nor the apply. The draft
remains DESIGN ONLY; owner-gated values remain `[OPEN]`, and build remains gated on WP-P0-13
acceptance + re-audit (OQ-10).

| # | Sev | Finding (short) | Disposition | Where changed |
|---|---|---|---|---|
| W196-F01 | MED | the v1.8 record said the hand-applied DS47-F03 Patch A did not land; the body carries it | **REPAIRED** — v1.8 change-log prose, the DS47-F03 changelog row, and the terminal v1.8 fold summary corrected against the body; superseded wording retained struck through; every banner and cite re-read last | v1.8 change log, v1.8 fold summary |
| W196-F02 | MED | OQ-15 was opened over a component that exists — the single serialising appender, given a refusal duty nine paragraphs earlier for `writer_seq` | **REPAIRED** — the appender now **refuses** a candidate row whose `observation_id` it has already accepted, through the same dropped-row → coverage-gap exit; OQ-15 narrowed to composition + generator, which do need bytes the sources do not supply | §2.1 `observation_id` row, §2.4 appender, OQ-15 |
| W196-F03 | MED | OQ-13's premise "no named check fails" is contradicted by §5(c)'s comparison and by §3.2's recompute | **REPAIRED** — premise corrected; the marking row's content must equal the §4.1 recomputation from `ledger + graph` at every gate evaluation, disagreement DETECTED → INCOMPLETE; §5(c)'s "§3 subtracts" narration reconciled with §3.2's recompute; OQ-13 narrowed to the marking row's schema and store | §4.1, §5(c), §6.1 rows 5 and 7, OQ-13 |
| W196-F04 | MED | OQ-14's premise "no named component fails" is contradicted by the chain-bound `family_id` field | **REPAIRED** — premise corrected; `siblings(B)` must include every package whose chain-bound ledger rows carry `family_id = F`, disagreement DETECTED and fail-closed; OQ-14 narrowed to the graph store's own enforcement, head anchor and chain binding, and to the no-ledger-rows package that leaves no chain-bound trace | §1.5, §1.6, §4.1, OQ-14 |
| W196-F05 | MED | the DS47-F02 repair widened the §6.1 A-7d enumeration row past the clause it maps | **REPAIRED** — `UNLEDGERED_OBSERVATION` restored as the sole satisfier of that clause; `MISDATED_OBSERVATION` retained as a separate check on a read the ledger **was** told about, explicitly not evidence for the enumeration clause | §5(a) Probe 1, §6.1 row 3 |
| W196-F06 | MED | DS47-F04 and DS47-F07 changed no body text; five defect sites carry no blocker pointer, against the draft's own convention | **REPAIRED** — inline pointers added at §1.5, §1.6, §2.1 `observation_id`, §4.1 marking append, and §2.4 "No mutable status field", in the OQ-4/OQ-5/OQ-12 form the draft already uses | §1.5, §1.6, §2.1, §2.4, §4.1 |
| W196-F07 | LOW | `observed_at` still labelled "Informational only" while the repair makes it decide completeness | **REPAIRED** — relabelled: informational for *ordering* only; it decides the §4.1 time test and, since v1.8, ledger completeness via `MISDATED_OBSERVATION`; superseded label retained | §2.1 `observed_at` row |
| W196-F08 | LOW | the assumption the DS47-F02 check rests on was said to be flagged in OQ-7; it was not | **REPAIRED** — OQ-7 now states the Producer-2 server-side-timestamp independence assumption and marks it NOT VERIFIED; §5(a) Probe 1 points at it | §5(a), OQ-7 |
| W196-F09 | LOW | three of four v1.8 body repairs carry no version/finding tag | **REPAIRED** — tags added to the §5(a) Producer-2 clause, the §5(a) Probe-1 timestamp arm, and the §3.3 clean-case row | §3.3, §5(a) |
| W196-F10 | LOW | the hand-applied edit silently shifted every draft cite above line 586 in the paired report | **REPAIRED** — recorded as a Discrepancies fold note with the v1.8 mapping; no earlier report is edited, and cross-artifact cites are to be resolved by anchor text | Discrepancies |

**The rule the v1.8 round applied unevenly, applied again here.** DS48 declared a blocker only
where nothing in the document could fail, and completed the predicate on the existing component
otherwise — it did that for DS47-F02 and DS47-F06 and not for DS47-F01, DS47-F04 and DS47-F07.
W196-F02/F03/F04 are exactly that gap, and each is closed by binding the duty to the component the
verification names, with the failing input and the observable result stated. **No blocker was closed
outright** — each of OQ-13, OQ-14 and OQ-15 retains the part that would require inventing a
preimage, a producer or an owner decision the sources do not supply, and says why the named
component does not carry that part. Open questions therefore stay 15; discrepancies stay 5.

---

## v1.10 change log — W231 / DS66 fold

Fold of fresh census `DS66_RUN.log` (8 findings — **1 High**, 3 Medium, 4 Low), patch
`DS71_P022_PATCH.md`. **7 of 8 folded; 1 hunk STOPPED on a byte-for-byte anchor mismatch**
(DS66-F07's OQ-6 extension — see the row below and Discrepancies D-6). The draft remains DESIGN
ONLY; owner-gated values remain `[OPEN]`, and build remains gated on WP-P0-13 acceptance +
re-audit (OQ-10).

| # | Sev | Finding (short) | Disposition | Where changed |
|---|---|---|---|---|
| DS66-F01 | **HIGH** | `window_start`/`window_end` are Producer-1 self-report; no named check binds the recorded slice to what was shown — "a leak gets past" | **WITHDRAWN + BLOCKER OPENED** — the "actually shown" claim is withdrawn at its own site (superseded wording retained struck through) and the gap opened as **OQ-16**. No component was invented and no prose asserts the binding is verified: the site now states that nothing here names a component that would refuse a narrowed window | §2.1 `window_start`/`window_end` row, OQ-16 (new), Findings count |
| DS66-F02 | MED | `package_hash` has no stated preimage, no named producer and — alone among the document's identities — no open question | **REPAIRED** — a named question opened in the document's own form, folded into OQ-1 (the package-identity blocker). **No byte tuple written**: the owner must name the preimage and producer before build | OQ-1 |
| DS66-F03 | MED | the §4.2 marking-integrity guard is either decoration or permanently-firing | **REPAIRED** — the applied text now says **which**: gates do consume markings (§6.1 row 7), so the guard is the **permanently-firing** case — under "Additive only" (§4.2) a correct-as-appended marking mismatches every later recompute. The guard's referent is rebound to the marking's own **append-time** recompute, which §4.1 already computes and writes, and legitimate additive growth is stated **not** to be a failure | §4.2 marking-row integrity duty |
| DS66-F04 | MED | the planted-`untouched` refusal is attributed to OQ-5, which covers `family_id`/`FAM-UNKNOWN`, not `untouched` | **REPAIRED** — the mis-cite is withdrawn at both sites; a planted value is stated to be **inert** (nothing reads it; the recompute ignores it), not refused. Superseded wording retained struck through | §3.2 "Never asserted", §6.1 row 4 |
| DS66-F05 | LOW | "what *is* checked today" overstates components §2.4/§4.1 mark BLOCKED | **REPAIRED** — relabelled "**designed but not live today**", agreeing with the document's own blocked list (the cross-check's chain-binding force inherits OQ-12 + OQ-8, §4.1). Superseded wording retained struck through | §1.5 |
| DS66-F06 | LOW | `observed_at` "monotonic per writer sequence" has no verifier and no consumer | **WITHDRAWN** — the monotonicity claim is withdrawn (no verifier, no consumer; ordering uses `append_index`, the §4.1 time test and §5(a) use single values). What remains true is restated. Superseded wording retained struck through | §2.1 `observed_at` row |
| DS66-F07 | LOW | `source_provenance`'s non-registry branch is an unbound predicate; non-registry producer-token confirmation has no named path | **PARTIALLY APPLIED** — the site now states the branch is unbound and its actual consequence (unconfirmable → `FAM-UNKNOWN`, fail-closed). **The paired OQ-6 extension was STOPPED**: its anchor was authored with a three-space indent against the draft's two, so it did not match byte-for-byte and was not hand-adjusted. The site's "folded into OQ-6" cite is therefore forward-looking, not yet satisfied — recorded as D-6 | §1.2 `source_provenance`; OQ-6 **not** changed |
| DS66-F08 | LOW | `observer_identity` composition is unnamed and unblocked | **REPAIRED** — marked at its site and folded into OQ-15, matching that entry's existing "same class" discipline (as it already folds `access_path`'s query-text hash) | §2.1 `observer_identity` row, OQ-15 |

**The rule this round applied.** The HIGH was **not** repaired by a sentence. The census's defect was
that the window bound is the producer's own self-report with nothing named that could refuse it;
writing prose asserting the binding holds would have restated the defect as its own fix. No such
component exists in the in-fence sources — §5(a) Probe 1 reconciles on read identity and timestamp
only — so the claim was withdrawn to what the document actually enforces and the gap opened as a
named blocker. **Open questions therefore rise 15 → 16**: OQ-16 added; OQ-1, OQ-15 extended in scope,
not added; no blocker closed. Discrepancies rise 5 → 6 (D-6, the stopped hunk). A count that rises
because a question was opened rather than answered is the honest direction.

---

## v1.12 change log — W289 owner-fold (owner addendum 31, decisions 98-103)

Fold of the owner's Phase-0 answers to rows 17-22 of `OWNER_PHASE0_DECISIONS_V1.md`, recorded as
decisions **98-103 of owner addendum 31** in the decision ledger
(`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:720-769`; the six
rows at same file `:764-769`). Each of the six rests on the owner's word as the sole authority —
recommendation basis JUDGEMENT at every row, and addendum 31 states that an owner answer "IS the
authority; the basis kind describes the recommendation, not the decision" (same file `:729-730`).

**Retain-and-tag, zero deletions.** No pre-existing line of this draft was edited or removed by this
fold. Every closed choice stays where it stands; the added block restates it struck through,
character for character, and appends the decision and its consequence — the same convention this
draft has used since v1.8.

| Row | Decision | Site | What the owner closed | What stays open |
|---|---|---|---|---|
| 17 | 98 | OQ-4 (`:1115-1118`), §1.2 (`:367-372`), D-3 (`:1503-1507`) | the bucketing rule: there are no buckets — one approved search-space version, for one strategy, is one family | the WP-P0-04 contract change that expresses it, and which recorded fields carry "approved search-space version" and "strategy" (engineering; P0-04 / P0-13) |
| 18 | 99 | OQ-7 limb (a) (`:1165-1167`) | fail-closed over-marking accepted; no decision-provenance link captured at freeze | the `OPTIMIZER`-branch run-identity limb (`:1167-1171`), which was not put to the owner as row 18 |
| 19 | 100 | OQ-7 limb (b) (`:1187-1190`) | one shared UTC clock for the five §2.3 writer classes, so `δ = 0` by this row's own text | which UTC source, how the five classes are moved onto it, and what shows no hidden difference remains (engineering) |
| 20 | 101 | OQ-7 limb (c) (`:1184-1186`) | an independent time source for the Producer-2 channels is **required**; the "record the unverified assumption" arm is refused | the source is unbuilt and unnamed, so independence stays NOT VERIFIED; and the cross-producer tolerance the two clock decisions leave unstated (OQ-7, extended v1.12) |
| 21 | 102 | OQ-11 copy/export limb (`:1292-1296`) | option (b), a boundary that **prevents** the unlogged copy/export/raw-read paths; (a) and (c) refused | the boundary is undelivered, so the `COMPLETENESS-UNBLOCK` conjunct stays unresolved; **COST: UNPRICED** (recorded at the OQ-11 site) |
| 22 | 103 | OQ-16 (`:1439`) | the window control is **not** withdrawn: the displayed window must be bound to the recorded one | the component that binds it and the input that makes it refuse — `OWNER-ANSWERED-SHAPE, VALUE PENDING`; OQ-16 stays BLOCKED |

**Counts unchanged: 16 open questions, 6 discrepancies.** No blocker is closed outright. Four —
OQ-4, OQ-7, OQ-11, OQ-16 — have their owner half closed and keep an engineering or delivery residue
that no owner answer can carry. OQ-7 is **extended**, not added (the cross-producer tolerance created
by decisions 100 and 101 together). Nothing here authorizes a build: the draft stays DESIGN ONLY and
gated on WP-P0-13 acceptance + re-audit (OQ-10).

**Cross-draft echo (census `W269_PHASE0_OWNER_QUESTIONS.md:624-629`, group X-1).** Row 17 is the
family-side member of the "same search" group; the sibling sites are
`P013_DESIGN_DRAFT_V1.md:1315-1337` (B-12 — the `preregistered_space_hash` preimage and sole
producer) and `P014_DESIGN_DRAFT_V1.md:847`, `:1012-1014`. Decision 98 fixes the family rule here; it
does not supply that preimage, which those two lanes still carry. Rows 18-22 have no cross-draft
group in §2 of the census — they are P0-22-only.

**Version note.** This fold is **v1.12**. The title line at `:1` still reads `v1.11` and is left
byte-identical on purpose: this lane's standing rule forbids deleted lines, and rewriting `:1` would
delete one. The bump is recorded here and in the fold paragraph at the end of the document. Recorded
separately, not repaired here: no `v1.11` change-log section exists in this draft although the body
carries `corrected v1.11, W234` tags at 23 lines (count method: `grep -c 'v1\.11, W234'`).

---

## 0. Inputs read and verified

| Source | What it fixes | Cite |
|---|---|---|
| Plan WP-P0-22 block | outputs, deps, gate A-7d, non-goals | `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:527-537` |
| Plan WP-P0-13 block | TrialRecord fields, `family_size`, SIGNAL_SCREEN_ONLY stamp; not started | same file `:409-417` |
| Plan WP-P0-04 block | contracts own `family_id` formula, lineage types, TrialRecord | same file `:317-333` (block ends at `:333`; `:334` is the `### WP-P0-05` header — corrected v1.1, F-9) |
| Brief §6.6 rules 6–8 | family lineage recorded; sibling contamination; ledger-computed untouched window | `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1437-1445` |
| Brief §6.6 rules 1–5 | package-level rules P0-22 must NOT change | same file `:1429-1435` |
| Brief §6.7 identity model | `candidate_id` STABLE family lineage; `evidence_window_start`; `PRIOR_IDENTITY` | same file `:1453-1516` |
| Brief §10.3 mechanism 2 | family clustering = source / producer / parameter neighbourhood | same file `:1987-1993` |
| Brief A-7d / D-15 | acceptance gate text; required before first `LIVE_CANDIDATE` | same file `:3075`, `:216` |
| D026 rule | RED on exact pre-fix behaviour or equivalent mutation, then GREEN, real output recorded | `AGENTS.md:46-47` |
| Contracts package v0 (merged) | `compute_family_id`, `TrialRecord`, `EnvironmentLineage`, `EvidenceIdentity` | `MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py:144-154`, `trials.py:14-74`, `lineage.py:10-41` |
| Taxonomy seed (READ ONLY, rebuilds FROZEN by PR #140) | `STRATEGY_RESEARCH_REGISTRY.json` (63 `STGxxx` entries — count method `grep -c '"strategy_id": "STG'` → 63; STG001 at `:1-65`, last entry STG063 at `:3430`, file 3493 lines — cite corrected v1.1, F-8), `TAG_DICTIONARY.json`. **`classification_confidence` is NOT uniform (re-censused v1.2, N74-F5):** method `grep -oE '"classification_confidence": *"[a-z_]+"' \| sort \| uniq -c` → `heuristic_auto` **46**, `explicit_metadata` **17** (63 total). `heuristic_auto` at `:64` (STG001); `explicit_metadata` at `:2427` (STG047). | `MTC_COMMAND_CENTER/05_REGISTRY/STRATEGY_RESEARCH_REGISTRY.json:9-10` (first `source_folder`), `:64` + `:2427` (both confidence classes), `:3430` (last STG); `TAG_DICTIONARY.json:1-253` |

---

## 1. `family_id` resolution design

### 1.1 Unit of resolution

The resolved thing is the **package** (`package_hash`), per §6.6 rule 6 "every package carries a
`family_id`" (`brief:1441`). Registry `STGxxx` entries are **seed material only** — they carry no
package identity (see Discrepancies D-2). `candidate_id` is stable family lineage
(`brief:1454`, `:1515`): all packages sharing a `candidate_id` **must** share one `family_id`.
That is a resolver invariant to verify, not a property supplied by the current contract; §1.3
refuses conflicting producer results rather than assuming the invariant holds.

### 1.2 Signals

The three inputs of `compute_family_id(source_provenance, producer, parameter_neighbourhood)`
(`identity.py:144-154`), each normalized before use:

- **`source_provenance`** — the origin record: the registry `source_folder` /
  `producer_spec.json` path (`STRATEGY_RESEARCH_REGISTRY.json:9-10`), or the transcript / idea id
  for packages not in the registry. **Non-registry branch unbound (added v1.10, DS66-F07):** the
  transcript / idea id has no named source, owner, or open question, and a non-registry package has
  no `source_folder`, so §1.3 step 3's "producer token is confirmed" is **unreachable for it** — its
  derived triple is unconfirmable and refused → `FAM-UNKNOWN` (fail-closed). The document implies a
  resolution path it does not name; the gap is folded into OQ-6.
- **`producer`** — the author / generator token parsed from the `source_folder` name
  (`ql_alpha` — `STRATEGY_RESEARCH_REGISTRY.json:10`; `ql_avwap_brian` — `:180`;
  `ql_connell` — `:389`; `ql_deepak` — `:491`; `ql_episodic_pivot_christian` — `:642`;
  cites added v1.1, F-2/F-12 — list is illustrative, not exhaustive)
  and cross-checked against `TAG_DICTIONARY.json` `harvested_tags` author names
  (`brian`, `christian`, `minervini`, `deepak`, `connell`, `weinstein`, …, `TAG_DICTIONARY.json:57-251`).
- **`parameter_neighbourhood`** — a **bucket spec, not raw parameters**. The contract test passes
  `{"period": [18, 22]}` (`test_identity.py:108`), i.e. an axis with a bin range. The caller
  computes it from `TrialRecord.preregistered_space_hash` (`trials.py:28`) plus a per-axis bin
  assignment; packages whose optimized parameters land in the same bin-tuple on the same
  preregistered axes share the neighbourhood key. Exact parameter values are NOT hashed (see D-3,
  and OQ-4 for the undefined bin rule).
  **OWNER-CLOSED at OQ-4 (added v1.12, W289; owner addendum 31 decision 98,
  `OWNER_DECISIONS_2026-08-29_EVENING.md:764`).** The owner refused bucketing outright, so the
  bin-assignment half of this bullet falls away. Superseded half retained character for character
  (the sentences above are left unedited): ~~"The caller computes it from
  `TrialRecord.preregistered_space_hash` (`trials.py:28`) plus a per-axis bin assignment; packages
  whose optimized parameters land in the same bin-tuple on the same preregistered axes share the
  neighbourhood key."~~ **DECIDED — owner addendum 31 decision 98 (2026-09-02), owner verbatim:**
  "Treat every trial from one approved search-space version, for one strategy, as one family. Do not
  invent arbitrary parameter buckets." What survives is the first half — the neighbourhood is
  computed from the approved search-space version identity (`TrialRecord.preregistered_space_hash`,
  `trials.py:28`) — with no per-axis bin assignment on top. The contract change that expresses this
  is WP-P0-04's (`identity.py:149-154` hashes the object exactly): see OQ-4, engineering half open.

### 1.3 Resolution order

First reconcile the two lineage producers; only then may the first step that yields a
**confident, non-conflicting** answer win. Otherwise `UNKNOWN`.

0. **Cross-producer conflict check (precedes acceptance).** Resolve both (a) the explicit
   parent/package lineage edge and (b) the existing `candidate_id` family in the catalog whenever
   both inputs exist. If they disagree — for example parent → `F1` while the candidate catalog →
   `F2` — refuse both results and emit `FAM-UNKNOWN`; neither source wins by list order. Also
   verify that every already-resolved package under one `candidate_id` has exactly the same
   `family_id`; any two-family split is the same refusal. `PROVISIONAL-ON-P013` because the
   package/candidate join is OQ-1. **Named variant `candidate-family-conflict`:** an immutable
   fixture supplies parent → `F1` and candidate → `F2`; the resolver must return
   `FAM-UNKNOWN`, then changing only the candidate result to `F1` must allow the shared `F1`.

1. **Explicit lineage edge.** If the package freeze record names a parent `package_hash` or a
   `candidate_id` (succession, optimization-from-baseline, manual fork) → inherit that parent's
   `family_id`. `PROVISIONAL-ON-P013` — the freeze record / catalog is where this edge is read.
2. **Shared `candidate_id`.** If the package's `candidate_id` already has a resolved family among
   its other packages → adopt it. `PROVISIONAL-ON-P013` (added v1.1, F-2) — the
   `package_hash ↔ candidate_id` join this step reads does not exist yet (OQ-1).
3. **Derived triple.** `compute_family_id(source_provenance, producer, parameter_neighbourhood)`
   with §1.2 normalization → `FAM-<16 hex>` (`identity.py:154`). Accept **only if** all three
   signals are present, mutually consistent, and the `producer` token is confirmed. **Confirmed
   (scoped v1.2, N74-F5):** the row's `classification_confidence` is `explicit_metadata`
   (17 of 63 rows — `STRATEGY_RESEARCH_REGISTRY.json:2427` is one), OR an independent
   producer-registry entry confirms the token. A row resting on
   `classification_confidence: "heuristic_auto"` alone (46 of 63 —
   `STRATEGY_RESEARCH_REGISTRY.json:64`) is **not** confirmed and its derived triple is refused
   → `FAM-UNKNOWN`. `explicit_metadata` rows are **not** forced to `FAM-UNKNOWN` on confidence
   grounds; the separate canonical-producer question (OQ-6) still applies.
4. **Otherwise → `UNKNOWN`.**

### 1.4 The `UNKNOWN` state

- Literal sentinel: **`FAM-UNKNOWN`** (a non-empty string, so it satisfies
  `TrialRecord.family_id: NonEmptyStr`, `trials.py:22` — but the contract does not yet *enforce*
  it; see D-4 / OQ-5).
- `FAM-UNKNOWN` **blocks `LIVE_CANDIDATE`** (§6.6 rule 6, `brief:1441`). It never coalesces to
  "unrelated". Two `FAM-UNKNOWN` packages are neither same-family nor different-family — they are
  unresolved, and unresolved is fail-closed.
- Consequence carried into §3: `family_id == FAM-UNKNOWN` makes the sibling set unbounded →
  untouched window = ∅ → zero confirmation evidence.

### 1.5 Recorded, not inferred

`family_id` and the signals / confidence / resolver identity / timestamp that produced it are
written **once** into the family-lineage graph store at package freeze and are immutable
thereafter. A later change of `family_id` requires a new package (consistent with §6.6 rule 3,
`brief:1433`). Resolution at query time is forbidden — a query reads the recorded value.

**Enforcement of that immutability is a NAMED BLOCKER — OQ-14** (pointer added v1.9, W196-F06;
the v1.8 round added OQ-14 without marking this, its defect site). What is **designed but not live
today** (corrected v1.10, DS66-F05; superseded wording retained: ~~"What *is* checked today"~~):
every observation row carries the frozen `family_id` as a §2.1 field inside the §2.4 `row_hash` preimage,
so the chain-bound rows are a second, independent record of family membership and the §4.1
graph↔ledger cross-check (added v1.9, W196-F04) DETECTS a graph edge that disagrees with them. What
is **not** checked is the graph store's own append-only enforcement, head anchor and chain binding —
see OQ-14.

### 1.6 The family-lineage graph

- **Nodes:** packages (`package_hash`), candidates (`candidate_id`), families (`family_id`).
- **Edges:** `derived-from` (package→parent package), `member-of` (package→candidate,
  candidate→family), `sibling-of` (derived from shared family).
- **Location:** a new append-only store co-located with the observation ledger (§2.2).
  **NOT** written back into `STRATEGY_RESEARCH_REGISTRY.json` (rebuilds FROZEN, PR #140) and
  **NOT** into the contracts package. `PROVISIONAL-ON-P013` on exact path and catalog
  registration. **"Append-only" here is a declaration, not an enforced boundary — OQ-14**
  (pointer added v1.9, W196-F06): the §2.4 access + atomicity contract, hash chain and OQ-8
  exact-head anchor are scoped to the observation ledger's §2.1 rows and do not extend to this
  store's nodes and edges.

---

## 2. Observation-ledger design

### 2.1 Record shape

Per plan `:530` and §6.6 rule 8 (`brief:1443`), each appended row carries:

| Field | Meaning |
|---|---|
| `observation_id` | opaque unique id. **Composition and generator are `[OPEN]` (OQ-15)** — pointer added v1.9, W196-F06. **Uniqueness is checked (added v1.9, W196-F02):** the single serialising appender (§2.4) is the only writer of the store and **refuses** a candidate row carrying an `observation_id` it has already accepted. |
| `observer_kind` | `HUMAN` \| `OPTIMIZER` \| `AUTOMATED_READER` |
| `observer_identity` | person id, or process id + code sha. **Composition open (added v1.10, DS66-F08 → OQ-15):** no source names "person id" or "code sha"; the chain binds the value, not its composition. |
| `observed_at` | UTC instant the read occurred. **Informational for ordering only — not informational overall (relabelled v1.9, W196-F07; superseded label retained: ~~"Informational only (revised v1.1, F-3)"~~).** **Withdrawn v1.10, DS66-F06 (superseded wording retained, character for character: ~~"Unchanged and still true: it is monotonic *per writer sequence*, NOT globally wall-clock-monotonic"~~):** no verifier checks `observed_at` monotonicity and no consumer uses it — the appender refuses non-monotonic `writer_seq` and duplicate `observation_id` but never `observed_at`; ledger order is append order via `append_index`, never `observed_at`; the §4.1 time test and §5(a) reconciliation use single values, not monotonicity. The monotonicity claim is declared without check or consumer, so it is withdrawn. What remains true, unchanged: ledger order is append order, never `observed_at` order. What the v1.1 label got wrong: this field **decides two outcomes**. (1) The §4.1 time test compares it against `B.frozen_at` with the skew margin `δ` and so decides contamination marking (`δ` is `[OPEN]` — OQ-7). (2) Since v1.8 / DS47-F02 it decides **ledger completeness**: a matched pair whose Producer-2 timestamp and this field disagree beyond `δ` is refused as `MISDATED_OBSERVATION`, making the ledger INCOMPLETE for every package whose window overlaps that read (§5(a)). A field that zeroes a window is not informational. It is **self-reported by the producing writer** — OQ-7. |
| `writer_seq` | per-writer-class monotonic counter, assigned by that writer before it hands the row to the serialising appender (added v1.1, F-3) |
| `package_hash` | the package whose record was surfaced |
| `family_id` | the package's **frozen** `family_id` as written at freeze into the family-lineage graph (§1.5) — may be `FAM-UNKNOWN`; never re-resolved at observation time (revised v1.1, F-5) |
| `deployment_identity_hash` | the composite the observation belongs to (§6.6 rule 2, `brief:1432`) |
| `environment` | `FORWARD_SHADOW` \| `INTERNAL_PAPER` \| `EXCHANGE_TESTNET` \| … (`lineage.py:10-15`) |
| `window_start`, `window_end` | the slice of the evidence window the producing writer recorded for the observer. **Withdrawn v1.10, DS66-F01 (superseded wording retained, character for character: ~~"the slice of the evidence window actually shown to the observer"~~):** "shown" is the producer's own self-report — no named check binds this recorded slice to what was actually displayed, so a bounded-but-narrow window is indistinguishable from an honest one and a leak gets past. Nothing here names a component that would refuse it. This row is self-report until OQ-16 names the binding. |
| `access_path` | which surface: Explorer view id, query-text hash, notebook id |
| `source_producer` | which producer emitted the row: `INSTRUMENTED_WRITE` \| `ACCESS_RECONCILIATION` (§5a) |
| `append_index` | strictly increasing integer assigned by the single serialising appender (§2.4); defines ledger order (added v1.1, F-3) |
| `prev_hash`, `row_hash` | hash chain. `prev_hash` names the prior row's `row_hash`; `row_hash` binds the ordered preimage declared in §2.4. The field binding is fixed, but its canonical byte encoding is `[OPEN]` (OQ-12). |

"Which window" is a real interval, never "all". A read with no bounded window recorded is
treated as covering the **whole** current evidence window of that `deployment_identity_hash`.

**Ordering rule (added v1.1, F-3).** Ledger order is **append order**, established by the single
serialising appender (§2.4), not wall-clock order. ~~`observed_at` is informational; it is monotonic
only within one writer class's own `writer_seq`.~~ `observed_at` is informational for ordering only;
no verifier checks its monotonicity and no consumer uses one (corrected v1.11, W234, propagating the
v1.10 DS66-F06 withdrawal; superseded sentence retained character for character). Ordering two ledger rows relative to each other
uses `append_index`, never a raw `observed_at` comparison between two different writers. The §4.1
time test compares `r.observed_at` against a package freeze instant `B.frozen_at`; it is kept on
the wall-clock value and is **fail-closed** — when `r.observed_at` is within a bounded clock-skew
margin of `B.frozen_at`, `r` is treated as potentially-visible-to-`B` (contaminating). Clock skew
between the five writer classes therefore cannot turn a contaminating row into a clean one.

### 2.2 Where it lives

New store `MTC_COMMAND_CENTER/05_REGISTRY/observation_ledger/` (research domain, sibling of the
registry) — `PROVISIONAL-ON-P013` on exact path, retention and artifact tier, because P0-13
owns the evidence-store layout and the "new evidence" destinations
(`plan:951` names P0-13 as such a destination). Format: append-only Parquet part-files plus a
hash-chain manifest, DuckDB-queryable — mirrors the TrialRecord catalog choice (`plan:412`).
Survivability is WP-P0-26's job (`plan:580`); the ledger is **append-only and never rolled
back** (`plan:535`).

### 2.3 Every writer class

1. **`HUMAN` — Minimum Explorer / WP-P0-14 read-only viewer** (`plan:419-432`) and the
   `mcc_readonly` web-app layer it extends (`plan:420` — cite corrected v1.1, F-6; `:422` is the
   map #123 / Perspective reuse amendment, not the `mcc_readonly` line): every candidate / trial
   detail view, chart render, or filter that returns rows bound to a package under an open
   decision. `PROVISIONAL-ON-P013` (added v1.1, F-2) — this class reads the P0-13 trial catalog.
2. **`HUMAN` — direct catalog queries:** a person running DuckDB / Parquet / notebook reads
   against the TrialRecord catalog. `PROVISIONAL-ON-P013` (added v1.1, F-2) — reads the P0-13
   trial catalog.
3. **`OPTIMIZER` — the canonical research simulator / walk-forward optimizer** (migrated
   `mega_walk_forward` path, `plan:489`) whenever it reads a prior package's forward / shadow
   record as input to a new trial (succession, warm start, baseline-informed search).
   `PROVISIONAL-ON-P013` / NOT VERIFIED — the exact read site is in the not-yet-migrated
   canonical path (OQ-3).
4. **`AUTOMATED_READER` — batch report / dashboard / scorecard generators** that read
   shadow / forward records (`enrich_gate3_evidence`-style consumers). `PROVISIONAL-ON-P013`
   (added v1.1, F-2) — reads the P0-13 trial catalog.
5. **`AUTOMATED_READER` — eligibility / promotion tooling** (WP-V2A-10, WP-V3-03, WP-V4-01)
   reading forward evidence. Recorded even though these are the *consumers* of this control — a
   read is a read. `PROVISIONAL-ON-P013` (added v1.1, F-2) — reads the P0-13 trial catalog.

### 2.4 Append-only: the enforcing boundary

**Honest status (revised v1.2, N74-F3).** v1.1 titled this "enforced structurally" but the
mechanisms it listed — an only-writer declaration, a lock, read-only file bits, an add-only
directory, and an `append()`-only library — are **interface and permission conventions**, and
the hash chain by itself only detects an *unrecomputed* edit while full-store rewrite detection
depends on the planned-and-unbuilt anchor (OQ-8). Real append-only enforcement requires the
**access + atomicity contract** below; until it and OQ-8 are resolved, the A-7d append-only
clause is **BLOCKED** (§6.1), not satisfied.

- **Access + atomicity contract (added v1.2, N74-F3) — the enforcing boundary, `PROVISIONAL-ON-P013`
  / OQ-11.**
  - **No client filesystem write access.** The five writer classes of §2.3, and every human or
    tool, have **read-only** access to the store's directory and objects at the OS/permission
    layer; they can reach the store only by handing a candidate row to the serialising appender
    over an IPC/RPC channel — they cannot open a part-file for write at all.
  - **Distinct appender identity, create-only.** The appender runs as a **separate principal**
    (its own service account / uid) that is the **only** identity with write access, and that
    write access is **create-only**: a storage-level retention lock / object-lock (WORM bucket
    policy or an equivalent `chattr +a` / immutable-object setting) makes retained part-files
    and manifest generations **impossible to overwrite or delete**, including by the appender
    itself and by root-equivalent tooling short of a deliberate, logged policy change.
  - **Atomic or recoverably journaled publication.** Appending a row is a two-part write (new
    part-file content + manifest head advance). It is **atomic** (single-object manifest swap
    that references the already-durable part-file) **or** recoverably journaled (write-ahead
    record → part-file fsync → manifest swap → journal clear), so a crash mid-append leaves the
    store either at the old head or at the new head, never partway. The verifier treats a
    dangling part-file with no manifest reference as absent.
  - **Anchor must cover the exact head before evidence counts.** An independently controlled
    immutable anchor (OQ-8) must record the **exact** head hash that a gate computed against;
    a gate evaluation whose head hash is not covered by the anchor is treated as INCOMPLETE
    (§3.3), so a full-store rewrite that also rewrites the local manifest still fails to produce
    usable confirmation evidence.
- **Single serialising appender (added v1.1, F-3).** The five writer classes of §2.3 do **not**
  write the store directly. Each emits a candidate row (carrying its own `writer_seq`) to one
  serialising appender process, which is the **only** writer of part-files and the **only**
  advancer of the hash chain. It verifies, per writer class, that each candidate row's
  `writer_seq` is strictly greater than the last it accepted from that class and **refuses** a
  non-monotonic row — the refusal is a dropped candidate row handled fail-closed below, never a
  silent accept (added v1.8, DS47-F06: nothing else verifies or consumes `writer_seq`
  monotonicity). **It also verifies, across all writer classes, that the candidate row's
  `observation_id` is not one it has already accepted into this store, and refuses a duplicate
  (added v1.9, W196-F02: nothing else refuses a duplicate `observation_id`; the chain binds the
  value, not its uniqueness).** Failing input: a second candidate row carrying an `observation_id`
  already held by an accepted row. Observable result: the row is **refused** — the identical
  fail-closed exit as the `writer_seq` refusal, a dropped candidate row → coverage gap → §3.3
  incomplete → `untouched(B) = ∅`, never a silent accept. This needs no invented bytes: the
  appender is the **only** writer of the store, so every `observation_id` that can enter the store
  passes this one check. The accepted-`observation_id` set is recovered from the store's retained
  rows when the appender restarts, on the same store-durability contract as the manifest head
  (OQ-2 / OQ-11, both open). What composes an `observation_id` and what issues it stay `[OPEN]`
  (OQ-15, narrowed v1.9). It assigns `append_index`, sets `prev_hash` from the current head,
  computes `row_hash` from the bound preimage below, appends, and updates the manifest head — one row at a time, under a single
  lock. Concurrent producers therefore cannot interleave on the chain or race a `prev_hash` base.
  If the appender is unavailable, producers **block** (buffer locally with a bounded queue and
  retry); a dropped candidate row is a coverage gap handled by §3.3 / §5(a) Producer 2, not a
  silent loss. A per-writer-sub-chain design (deterministic merge at read time) is the documented
  alternative if a single appender becomes a throughput bottleneck; the single appender is the
  v1.1 default because it is the simplest structure that makes "append order = ledger order" true.
- **WORM storage.** Part-files are written once; the `append()`-only library and the read-only
  file bits / add-only directory are the **convention layer** on top of the create-only storage
  retention lock above — they make accidental misuse hard, but the retention lock (not the file
  bit) is what makes overwrite/delete **impossible** (revised v1.2, N74-F3).
- **Hash chain (field binding added v1.7, G67-F02).** Each row's `prev_hash` = prior row's
  `row_hash`; a manifest records the head hash. The `row_hash` preimage is the following ordered
  tuple of **every §2.1 field except `row_hash` itself**, with no omitted observation field:
  (`observation_id`, `observer_kind`, `observer_identity`, `observed_at`, `writer_seq`,
  `package_hash`, `family_id`, `deployment_identity_hash`, `environment`, `window_start`,
  `window_end`, `access_path`, `source_producer`, `append_index`, `prev_hash`). The exact canonical
  byte encoding of that tuple is **`[OPEN]` (OQ-12)**; until it is ratified, the per-row hash
  verifier and every claim that depends on it are BLOCKED, rather than silently choosing an
  encoding. After OQ-12 resolves, changing any one bound field without recomputing `row_hash` must
  be DETECTED by recomputing the row hash. Changing a bound field and recomputing only that row
  must be DETECTED by the successor's unchanged `prev_hash`; recomputing that row and every
  successor through the manifest head must be DETECTED against the OQ-8 anchor. A rewrite that
  recomputes the whole chain and manifest is **not** caught by the local chain alone — only the
  anchor catches it (revised v1.2, N74-F3).
- **External anchor.** The head hash is periodically committed to the text-class GitHub mirror
  (WP-P0-26, "text-class also to GitHub", `plan:580`) and/or a tag, so a full-store rewrite is
  still DETECTED against the anchor, and a gate may only count evidence whose head hash the
  anchor covers (see the contract above). (**OQ-8 — the anchor channel is planned-and-unbuilt;
  until it exists, full-store-rewrite detection does not exist and the A-7d append-only clause
  stays BLOCKED.**)
- **CI guard.** WP-P0-27 (`plan:590-595`) runs the chain verifier on every PR and against the
  anchor; RED if broken.
- **No mutable status field.** Contamination is expressed by **appending a marking row** (§4),
  never by editing an observation row. **The `FAMILY_OBSERVED` marking row is not a §2.1
  observation row**: its set-valued content has no §2.1 schema and is not inside the `row_hash`
  preimage above, so none of this section's enforcement covers it. Its schema and its store are a
  NAMED BLOCKER — **OQ-13** (pointer added v1.9, W196-F06; the v1.8 round added OQ-13 without
  marking this, one of its producing sites). What *is* checked is the marking's **content**.
  **Superseded referent retained character for character:** ~~"§4.1's
  integrity duty requires it to equal the recomputation from `ledger + graph` at every gate
  evaluation"~~. At every gate
  evaluation, the integrity duty requires the marking to equal the §4.1 recomputation **as it stood
  when the marking was appended**; legitimately-added later siblings or ledger rows are not a
  failure (corrected v1.11, W234, propagating the v1.10 DS66-F03 append-time rule).

---

## 3. Untouched-window computation

### 3.1 Inputs

For candidate package `B` with `deployment_identity_hash = D`, environment `E`, and evidence
window `W_B = [B.evidence_window_start, now]` (§6.6 rule 2, `brief:1432` — §-label corrected
v1.1, F-7; line 1432 is under the §6.6 header `:1427`, §6.7 begins `:1447`): the observation
ledger head hash, and the family graph.

### 3.2 Formula (COMPUTED, never asserted)

```
observed_direct(B) = ⋃ { [r.window_start, r.window_end]
                         : r ∈ ledger, r.package_hash = B.package_hash,
                           r.deployment_identity_hash = D, r.environment = E }

observed_family(B) = ⋃ { contaminated_interval(B, A, r)   (see §4)
                         : A ∈ siblings(B), r ∈ ledger observations of A }

observed(B)   = observed_direct(B) ∪ observed_family(B)        # interval-set union
untouched(B)  = W_B  \  observed(B)                            # interval-set difference
confirmation_evidence_duration(B) = Σ length(untouched(B))
```

Only observations / trades falling **entirely inside** `untouched(B)` may be cited as
confirmation (§6.6 rule 5, `brief:1435`; rule 7/8, `brief:1442-1443`).

**Never asserted:** no field anywhere stores an untouched-window value. It is recomputed from
`ledger + graph` at every gate evaluation, and the gate records the **ledger head hash** it
computed against. A persisted "untouched = X" is inert — nothing reads it (recomputed from `ledger + graph` at every gate evaluation) — and it is **not** OQ-5's subject, which is the `family_id`/FAM-UNKNOWN sentinel (corrected v1.10, DS66-F04; superseded wording retained: ~~"A persisted \"untouched = X\" is a bug and OQ-5's contract check should refuse it"~~). The recompute simply ignores it; no contract check refuses it.

### 3.3 Edge cases

| Case | Result |
|---|---|
| **No observations of `B`, no contaminating sibling observation (`observed_family(B) = ∅`), ledger present + verified + complete for `E`/`W_B`** | `untouched(B) = W_B` (legitimately clean). Completeness must be **positively** established (below). A sibling row of `B` that passes the §4.1 time + linkage tests makes `observed_family(B) ≠ ∅` and `untouched(B) < W_B` even with zero direct observations of `B` (§3.2); only the joint absence of both yields the full window (joint-absence condition added v1.8, DS47-F05 — tag added v1.9, W196-F09). |
| **Ledger absent** | `untouched(B) = ∅` → zero confirmation evidence (§6.6 rule 8, `brief:1443`; `plan:534-535`). |
| **Ledger incomplete** — head hash ≠ anchor, OR a coverage gap (**widened v1.2, N74-F1; identity-bound v1.6, N99-F04:** any sub-interval of `W_B` not covered by a relevant ledger row **or** a scoped no-read attestation under `coverage_key(B)` — whether or not a reader was independently known to be running there; the §5a Producer 2 "reader provably ran over `[t1,t2]`" case is one instance, not the whole class), OR `family_id(B) = FAM-UNKNOWN`, OR (**added v1.9, W196-F03/F04**) the graph-derived `siblings(B)` disagrees with the chain-bound `family_id` of the ledger rows (§4.1 cross-check), OR ~~a `FAMILY_OBSERVED` marking row presented for `B` disagrees with the §4.1 recomputation from `ledger + graph` (§4.2 integrity duty)~~ a `FAMILY_OBSERVED` marking row presented for `B` disagrees with the §4.1 recomputation **as it stood when the marking was appended** (§4.2 integrity duty; corrected v1.11, W234; superseded referent retained character for character); legitimately-added later siblings or ledger rows do not create this incompleteness | `untouched(B) = ∅`. |
| **Overlapping / adjacent / touching observed windows** | collapsed by interval-set **union** before the difference; no double subtraction; zero-length rows ignored. |
| **`UNKNOWN` family** | sibling set unbounded → `observed_family(B)` cannot be bounded → `untouched(B) = ∅`, independent of direct observations. This is why `FAM-UNKNOWN` blocks `LIVE_CANDIDATE`. |
| **`evidence_window_start` missing** (package frozen but composite not minted) | no window exists → not eligible; not "clean". |
| **`D` changed mid-window** (`PRIOR_IDENTITY`, `brief:1433`) | only rows bound to the *current* `D` count toward `W_B`; the pre-change portion is a different identity's window and does not transfer. |

"Positively established completeness" (**made continuous v1.2, N74-F1**) = head hash matches the
anchor **and** **every** sub-interval of `W_B` — not only those in which a reader was already
known to be running — is covered by either a **relevant** ledger row or a **scoped** no-read
attestation **and** (added v1.9, W196-F03/F04) neither of the two agreement checks in the row above
is DETECTED: the graph-derived `siblings(B)` agrees with the chain-bound `family_id` of the ledger
rows (§4.1), and ~~every `FAMILY_OBSERVED` marking row presented for `B` equals the §4.1
recomputation from `ledger + graph` (§4.2).~~ every `FAMILY_OBSERVED` marking row presented for `B`
equals the §4.1 recomputation **as it stood when the marking was appended** (§4.2); legitimately-
added later siblings or ledger rows do not create a disagreement (corrected v1.11, W234;
superseded referent retained character for character). A DETECTED disagreement on either is an incompleteness
of the same kind as a coverage gap: the window is incomplete for all of `W_B`, not repaired by
re-deriving the disputed value.

**Identity binding (added v1.6, N99-F04).** Define
`coverage_key(B) = (B.package_hash, family_id(B), D, E)`. A ledger row covers time for `B` only if
it passes the same identity predicate as §3.2: it names `B.package_hash`, `D`, and `E`, or it names
a sibling in the same resolved `family_id`, with the same `D` and `E`. A no-read attestation covers
time only if its declared scope names that exact package or family plus `D` and `E`, or names a
declared global read domain whose membership independently includes that package/family, `D`, `E`,
and every relevant access surface. A row or attestation for a wrong package, family, `D`, or `E`
does **not** cover any part of `W_B`. The OQ-9 format must carry and authenticate this scope.

**One unblock predicate (added v1.6, N99-F05; anchor conjunct added v1.7, G67-F01;
window-bounds conjunct added v1.11, W234):
**Superseded predicate retained character for character:**
~~`COMPLETENESS-UNBLOCK = OQ-8 exact-head-anchor duty resolved AND OQ-9 interval-attestation duty
resolved AND OQ-11 residual read-path producer/prevention duty resolved`.~~
`COMPLETENESS-UNBLOCK = OQ-8 exact-head-anchor duty resolved AND OQ-9 interval-attestation duty
resolved AND OQ-11 residual read-path producer/prevention duty resolved AND OQ-16 window-bounds
binding duty resolved`. A single mechanism
may satisfy both duties only if it produces two independently checked outputs: exhaustive
read-event observations and identity-bound no-read interval attestations.**

The "known-reader" wording of v1.1 left a hole: a read that **both** §5(a) producers miss is never
"known", so its interval was never required to carry an attestation and the §5(a) Probe 2
fail-closed route did not actually fire. Continuous coverage removes that hole: absent a
positive "nobody read this" record over even one sub-interval, the ledger is **incomplete for the
whole `W_B`** and `untouched(B) = ∅` for that whole window. Until the no-read attestation
emitter exists (OQ-9), **no** window is positively complete, so `untouched(B) = ∅` for every
`B` — this is the intended fail-closed state, not a regression. Non-empty `untouched` is restored
only when `COMPLETENESS-UNBLOCK` is true and every coverage item passes the identity binding above.

---

## 4. `FAMILY_OBSERVED` contamination marking

### 4.1 Rule (from §6.6 rule 7, `brief:1442`)

For candidate `B`, `family_id = F ≠ FAM-UNKNOWN`, freeze instant `B.frozen_at`:

- `siblings(B) = { A : A.family_id = F, A ≠ B }`.
- For each sibling `A` and each ledger observation row `r` of `A`:
  - **time test:** `r.observed_at < B.frozen_at` **and** `A.evidence_window_start < B.frozen_at`
    (rule 7 text). **Fail-closed on skew (added v1.1, F-3):** if `r.observed_at` is within the
    bounded inter-writer clock-skew margin `δ` of `B.frozen_at` (i.e. `r.observed_at < B.frozen_at + δ`),
    `r` counts as time-eligible. `δ` is a NAMED BLOCKER — see OQ-7 (extended).
    **`δ = 0` (added v1.12, W289; owner addendum 31 decision 100,
    `OWNER_DECISIONS_2026-08-29_EVENING.md:766` — owner verbatim "Use one shared UTC clock; allow no
    hidden clock difference").** The single-time-source arm of OQ-7 is taken, so the margin is zero
    and the time test reads `r.observed_at < B.frozen_at` — rule 7's own text. The fail-closed
    intent is unchanged: with one clock there is no skew for a contaminating row to hide in. The
    margin stays written above as the design's general form, and the shared clock itself is unbuilt
    (OQ-7).
  - **linkage test (fail-closed):** the observer/decision that produced `B` *could have seen* `r`
    — operationalized as `r.observer_kind = HUMAN` who is also `B`'s approver, **or**
    `r.observer_kind = OPTIMIZER` whose run produced `B` (run-identity link NOT VERIFIED — OQ-7), **or** — when the decision link
    cannot be established — **any** `r` passing the time test (OQ-7).
  - `contaminated_interval(B, A, r) = [r.window_start, r.window_end] ∩ [B.evidence_window_start, now]`
    — "intersection of A's observed window with B's evidence window, computed, not estimated"
    (rule 7).
- If any `contaminated_interval` is non-empty → **append** a `FAMILY_OBSERVED` marking row for
  `B` naming: `B.package_hash`, sibling `A.package_hash`, the ledger row ids `r`, the computed
  interval(s), `F`, timestamp, and the ledger head hash computed against. **The marking row's own
  schema and store are a NAMED BLOCKER — OQ-13** (pointer added v1.9, W196-F06; this is one of the
  two producing sites the v1.8 round left unmarked).

**Graph↔ledger sibling cross-check (added v1.9, W196-F04).** `siblings(B)` above is derived from
the family-lineage graph store (§1.6), whose own append-only enforcement is open (OQ-14). It is not
the only record of family membership: every observation row carries the package's frozen `family_id`
as a §2.1 field, and that field is inside the §2.4 `row_hash` preimage. The resolved sibling set is
therefore **checked against the ledger**: `siblings(B)` must contain every package whose ledger rows
carry `family_id = F`. *Failing input:* a `member-of` / `sibling-of` edge for a sibling `A` edited or
removed from the graph store, where `A` has ledger rows asserting `family_id = F`. *Observable
result:* the graph-derived `siblings(B)` omits `A` while `A`'s rows still assert `F` → the two
records disagree → **DETECTED**; the disagreement is fail-closed exactly as an unresolved family is
— `siblings(B)` is not bounded by a record that agrees with itself, so `untouched(B) = ∅` for the
whole `W_B` (§3.3). Editing `A`'s rows instead of the edge, so that they stop asserting `F`, changes
a bound preimage field and must be DETECTED by the row-hash / successor-link / anchor checks of §2.4
— which are themselves **BLOCKED on OQ-12 and OQ-8** until the canonical byte encoding and the
anchor exist, so the chain-binding force of this cross-check inherits those blockers. **What this
cross-check does not cover** stays in OQ-14: the graph store's own enforcement, head anchor and
chain binding, and a package that has **no ledger rows at all** — it leaves no chain-bound trace, so
removing its edge is undetectable by this route.

### 4.2 Propagation

- The contaminated portion of `B`'s evidence is **navigational only** — subtracted in §3
  exactly as direct observation is (rule 7 ⇒ rule 4).
- **Transitivity within the family.** If a further sibling `C` is later derived from `B`, `C`
  inherits `FAMILY_OBSERVED` over `(B`'s contaminated intervals ∩ `W_C) ∪ (direct observations
  of B before C.frozen_at ∩ W_C)`. Marking is **re-derived from the ledger for every new
  sibling** — never copied as a flag.
- **Marking-row integrity duty (added v1.9, W196-F03).** Because marking is re-derived and never
  asserted, the marking row is a **record of** a computation, not an input to one — and that makes
  it checkable without any new component. At **every gate evaluation**, each `FAMILY_OBSERVED`
  marking row presented for `B` must equal the §4.1 recomputation **as it stood when the marking
  was appended** (the computed interval(s), sibling `A`, row ids `r`, and `F` that §4.1 wrote at
  append time) — the guard's referent is the marking's own append-time recompute, not the unbounded
  current recompute (added v1.10, DS66-F03; superseded wording retained: ~~"must equal the §4.1
  recomputation from `ledger + graph` at every gate evaluation"~~). *Failing input:* a marking
  row whose interval, sibling, row ids or `F` was edited after it was appended — a disagreement
  with its own append-time recompute. Legitimately-added later siblings or ledger rows (Additive
  only, `:682`) are **not** a failure: they produce new or extended marks, they do not invalidate
  an as-appended mark.
  *Observable result:* the recomputation disagrees with the row → **DETECTED**; the marking is
  refused as gate input and the ledger is treated as INCOMPLETE for `W_B` under §3.3, so
  `untouched(B) = ∅` for the whole window. **No gate may consume a `FAMILY_OBSERVED` marking that
  did not pass this comparison at that same evaluation** — this binds §6.1 row 7, where downstream
  gates consume markings as their input. The two components that carry this are already named and
  already run at gate time: §3.2's "recomputed from `ledger + graph` at every gate evaluation" and
  the re-derivation rule directly above. What the duty does **not** supply is the marking row's
  schema or its store — OQ-13, narrowed.
- **Succession** (map #54 ticket #64, `brief:1445`): a challenger built from an incumbent's
  observations is the sibling case with no exception.
- **`UNKNOWN` family:** siblings cannot be computed → `B` is not *marked* `FAMILY_OBSERVED` but
  is treated as maximally contaminated (§3 sets `untouched = ∅`). Absence of a marking here is
  **not** cleanliness.
- **Additive only.** A new sibling or a newly discovered ledger row can only ever *add*
  contamination. Nothing removes a `FAMILY_OBSERVED` marking — no retroactive laundering
  (`plan:537` non-goal).

---

## 5. A-7d falsification designs

### 5(a) Enumeration finds an observation it was not told about — **both producers named**

The ledger must not be its own only witness (self-confirming-check pattern). Two **independent**
producers of observation rows:

- **Producer 1 — `INSTRUMENTED_WRITE`.** The viewer / optimizer / reader libraries call
  `observation_ledger.append(...)` inline when they surface a record. This is the "told about"
  path.
- **Producer 2 — `ACCESS_RECONCILIATION`.** A separate collector built from surfaces Producer 1
  does not control: the Explorer / `mcc_readonly` HTTP access log; the DuckDB / Parquet catalog
  query log plus file access times; and the optimizer run manifests (which prior `package_hash`
  values each trial consumed as warm-start input, from `TrialRecord` provenance — **NOT VERIFIED /
  `PROVISIONAL-ON-P013`:** the TrialRecord field recording consumed warm-start `package_hash`
  values is not cited under the read fence; the run-manifest channel and its provenance are
  BLOCKED on OQ-3, extended). Producer 2
  emits candidate observation rows independently.
  *(The `NOT VERIFIED` / `PROVISIONAL-ON-P013` label in this clause was added v1.8, DS47-F03 —
  Patch A, applied by hand after the W193 lane stopped on a preimage that omitted this list's
  two-space continuation indent; tag added v1.9, W196-F09, and the v1.8 record corrected under
  W196-F01.)*

**Probe 1 — falsifies Producer 1.** Create a read Producer 1 is not told about — e.g. a person
opens a candidate detail page by a path where the `append` call is stubbed, or runs a raw
`duckdb` query against the catalog Parquet with no instrumentation. **Enumeration** = reconcile
Producer 2's access-derived rows against Producer 1's ledger rows on **read identity and
timestamp**: a Producer-2 row with no matching ledger row → `UNLEDGERED_OBSERVATION`; a matched
pair whose Producer-2 access-log timestamp and Producer-1 `observed_at` disagree beyond the §4.1
skew margin `δ` → reconciliation refuses it as `MISDATED_OBSERVATION` (a stamp running ahead of
real time by more than `δ` would otherwise fire the §4.1 time test in the leak direction — read
recorded, contamination not marked, confirmation counted; timestamp-agreement arm added v1.8,
DS47-F02 — tag added v1.9, W196-F09). **Expected:** either mismatch → ledger
state = INCOMPLETE → §3 yields zero confirmation evidence for every package whose window overlaps
that read. The timestamp-agreement predicate is **BLOCKED on OQ-7** until `δ` is ratified or a
single time source makes `δ = 0`, **and it rests on Producer-2 timestamps being server-side and
independent of the producing writer's clock — NOT VERIFIED, now stated in OQ-7 (extended v1.9,
W196-F08)**.

**Owner-closed inputs to this arm (added v1.12, W289).** Two of the three things this arm waits on
are now ratified. (1) `δ = 0` — owner addendum 31 decision 100
(`OWNER_DECISIONS_2026-08-29_EVENING.md:766`, "Use one shared UTC clock; allow no hidden clock
difference") takes the single-time-source arm of OQ-7, so the timestamp-agreement predicate compares
with zero tolerance rather than an unratified margin. (2) The Producer-2 timestamp independence this
arm rests on is now a **requirement**, not an assumption — decision 101 (`OWNER_DECISIONS_2026-08-29_EVENING.md:767`, "Require an
independent clock for access logs"). Neither is built: the arm stays BLOCKED on delivery (a shared
clock, and a named independent Producer-2 time source), not on the owner, and independence stays
**NOT VERIFIED** because no built Producer-2 implementation is named anywhere in this draft. What
neither decision states is the tolerance for the **cross-producer** comparison itself — `δ = 0` is
the inter-writer margin, while this arm compares a writer's `observed_at` against an
independently-clocked access-log stamp. That is folded into OQ-7 (extended v1.12, W289); no value is
invented here.

**Which arm evidences the A-7d clause (scoped v1.9, W196-F05).** The `UNLEDGERED_OBSERVATION` arm
— and only that arm — is the concrete reading of A-7d "its enumeration is shown capable of finding
an observation it was not told about" (`plan:534`): it produces an observation the ledger was not
told about. A `MISDATED_OBSERVATION` is by construction a **matched** pair — the ledger **was** told
about that read — so it is a real and useful check with the same INCOMPLETE consequence, but it does
**not** evidence the enumeration clause and may not be substituted for the `UNLEDGERED_OBSERVATION`
arm in the §6.1 row. Superseded v1.8 wording, retained: ~~"This is the concrete reading of A-7d …"
attached to both mismatches jointly.~~

**Probe 2 — falsifies Producer 2 (added v1.1, F-1).** The v1 design left Producer 2 unprobed, so
the enumeration was only self-checking with respect to Producer 2's own coverage — a read that
**both** producers miss is invisible. Probe: perform a read over a surface neither logging
channel records — copy the catalog Parquet off-box and read it on another machine; mount the
catalog volume `noatime` and read a part-file; read via a surface added after Producer 2's
collector was configured. **Expected: NOT DETECTED by either producer.** This is a real,
demonstrable blind spot, not a hypothetical.

**Disposition of Probe 2 — by-construction coverage plus a declared residual class:**

1. **By construction, where achievable.** For the surfaces the platform *does* control, the
   design requires that every catalog read path is forced through a logged surface:
   the `mcc_readonly` layer serves catalog rows only through request handlers that emit the HTTP
   access log; direct `duckdb`/Parquet access on the research host is only via a wrapper that
   writes the query log; `atime` is left enabled on the catalog volume. A read on a
   platform-controlled surface that reaches a logged channel is inside Producer 2's coverage.
2. **Named residual class (cannot be closed by construction).** Reads that leave the
   platform-controlled surfaces — an off-box copy of the Parquet, a `noatime` mount outside the
   research host, any future surface not yet wired into Producer 2 — are a **residual coverage
   class** that Producer 2 provably cannot enumerate. The design does **not** claim it can.
3. **Fail-closed route (corrected v1.2, N74-F1; unified v1.6, N99-F05).** The residual class is handled by §3.3's
   positive-completeness requirement, now made **continuous over all of `W_B`** — an interval of
   `W_B` counts as *untouched* only if head-hash matches the anchor **and** that interval is
   covered by a relevant ledger row **or** a scoped no-read attestation under `coverage_key(B)`,
   **whether or not a reader was
   independently known to be running there**. The v1.1 wording ("every sub-interval during which
   a reader was known to be running") did not close this: a read both producers miss is never
   "known", so its interval was never required to carry an attestation and this route did not
   fire. Under the continuous rule, absent a positive "nobody read this" record over even one
   sub-interval, the ledger is incomplete for the whole `W_B` and `untouched(B) = ∅` for that
   whole window. **This design does not claim Probe 2's blind spot is "routed to zero" today.**
   **Superseded predicate retained character for character (corrected v1.11, W234):**
   ~~`COMPLETENESS-UNBLOCK = OQ-8 exact-head-anchor duty resolved AND OQ-9 interval-attestation
   duty resolved AND OQ-11 residual read-path producer/prevention duty resolved`.~~
   **`COMPLETENESS-UNBLOCK = OQ-8 exact-head-anchor duty resolved AND OQ-9 interval-attestation
   duty resolved AND OQ-11 residual read-path producer/prevention duty resolved AND OQ-16
   window-bounds binding duty resolved`. A single mechanism may satisfy both duties only if it
   produces two independently checked outputs: exhaustive read-event observations and
   identity-bound no-read interval attestations.** Until that predicate is true, the entire
   `W_B` is **incomplete** and no confirmation evidence can be drawn from it.

So the enumeration is falsifiable for **both** producers: Probe 1 shows Producer 2 catches what
Producer 1 misses; Probe 2 shows the class Producer 2 itself cannot catch. That class is
**named**, and it makes the whole `W_B` **incomplete** (→ zero confirmation
evidence) until `COMPLETENESS-UNBLOCK` is true — it is **not** claimed to be independently routed to
zero by the current design, and it is not silently assumed absent (corrected v1.2, N74-F1).

### 5(b) Absent / incomplete ledger → ZERO confirmation evidence

Fixture set (each: RED = some positive confirmation duration reported without the check;
GREEN = zero with it — D026 shape, `AGENTS.md:46-47`). **Runnable-now status marked per arm
(revised v1.4, N86-F01 + v1.6 N99-F05 sweep):** b1 and b4 have a primary arm designable now but
 their mandatory complete-window mutation is blocked on ~~OQ-8 + OQ-9 + OQ-11~~
 OQ-8 + OQ-9 + OQ-11 + OQ-16 (corrected v1.11, W234; superseded blocker list retained character
 for character); b2 and b3 depend on their
named blockers.

**Two independent producers per fixture (added v1.2, N74-F2).** No b-fixture may feed the same
derived value to its own setup and its own expected result. Each names:
**truth-side producer** = an **immutable fixture manifest** authored before the run that declares
the store's ground state (present / absent / corrupted-at-row-k / family = `FAM-UNKNOWN`) and the
**expected** `confirmation_evidence_duration`; **verdict-side producer** = the gate's
`untouched(B)` computation (§3.2) + the chain verifier, run against the store, producing the
**observed** duration. The compared operands are `expected_duration` (truth) vs
`observed_duration` (verdict). Each fixture also carries a **truth-side-only mutation variant**:
change only the manifest's ground-state declaration, rebuild the store to match, and require the
verdict-side producer to move — proving the verdict is not just echoing the manifest.

- **b1 — ledger dir/file absent** *(PRIMARY ABSENT-LEDGER ARM DESIGNABLE NOW;
  ~~COMPLETE-WINDOW MUTATION BLOCKED ON OQ-8 + OQ-9 + OQ-11~~
  COMPLETE-WINDOW MUTATION BLOCKED ON OQ-8 + OQ-9 + OQ-11 + OQ-16 — corrected v1.11, W234;
  superseded blocker list retained character for character)*.
  - *Truth:* manifest declares "no store", `expected_duration = 0`. *Verdict:* gate computes
    `untouched(B)` → store-not-found → `∅` → `confirmation_evidence_duration = 0` →
    forward-evidence precondition BLOCKED (not PASS). Operands match at 0.
  - *Mutation variant:* manifest declares "store present, complete, one un-observed window of
    length `L` for `E`/`W_B`", store built to match → verdict must now report
    `observed_duration = L` (not 0). ~~A planted persisted `untouched = L` value in the store must
    be **refused** by the OQ-5 contract check, not read (ties §3.2 "never asserted").~~ A planted
    persisted `untouched = L` value is **inert** — nothing reads it; the gate recomputes from
    `ledger + graph`, and OQ-5 does **not** refuse the planted value because OQ-5 governs the
    `family_id`/`FAM-UNKNOWN` sentinel (corrected v1.11, W234, propagating DS66-F04; superseded
    sentence retained character for character). This
    complete-window mutation is **~~BLOCKED ON OQ-8 + OQ-9 + OQ-11~~ BLOCKED ON OQ-8 + OQ-9 +
    OQ-11 + OQ-16** (corrected v1.11, W234; superseded blocker list retained character for
    character) because positive completeness
    requires the anchor and both coverage duties in `COMPLETENESS-UNBLOCK`.
- **b2 — head hash ≠ anchor** (a row edited/deleted).
  - *Truth:* manifest declares "corrupted at row k", `expected_duration = 0`. *Verdict:* chain
    verifier DETECTS the break → state INCOMPLETE → `untouched(B) = ∅`.
  - *Mutation variant:* manifest declares "intact, anchor-covered head, un-observed window `L`"
    → verdict reports `L`. *(~~NOT RUNNABLE until OQ-8, OQ-9, OQ-11, and OQ-12 resolve~~
    NOT RUNNABLE until OQ-8, OQ-9, OQ-11, OQ-16, and OQ-12 resolve (corrected v1.11, W234;
    superseded blocker list retained character for character) — the
    external anchor channel (WP-P0-26 / WP-P0-27) is planned-and-unbuilt, positive whole-window
    coverage still needs both `COMPLETENESS-UNBLOCK` coverage duties, and the canonical row-hash
    byte encoding is `[OPEN]`. After OQ-12 resolves, the field-only and one-row-recompute variants
    in §2.4 exercise the local chain; after OQ-8 also resolves, the whole-chain-recompute variant
    exercises the anchor.)*
- **b3 — coverage gap.**
  - *Truth:* immutable read-timeline fixture declares a reader active over `[t1,t2]` with **no**
    ledger row and **no** attestation, `expected_duration = 0`. *Verdict:* one uncovered
    sub-interval makes the ledger INCOMPLETE for the whole `W_B`; the gate returns
    `untouched(B) = ∅` and `observed_duration = 0` rather than subtracting only `[t1,t2]`.
  - *Mutation variant:* change the truth-side manifest to declare no reader active over
    `[t1,t2]`, supply a valid identity-bound no-read attestation there **and** relevant-ledger-row-
    or-scoped-attestation coverage
    over every remaining sub-interval of `W_B`, then rebuild the store to match. Only this
    positively complete variant may produce a non-zero duration, and the verdict-side computation
    must report the manifest's independently declared `L > 0`. *(NOT RUNNABLE
    ~~until OQ-8, OQ-9, and OQ-11 resolve~~ until OQ-8, OQ-9, OQ-11, and OQ-16 resolve
    (corrected v1.11, W234; superseded blocker list retained character for character) — the
    exact-head anchor, attestation format/identity binding, and residual read-path
    boundary are undefined.)* **Wrong-key variant:** replace only the `[t1,t2]` coverage item
    with a row or attestation for the wrong package, family, `D`, or `E`; the verifier must refuse
    it as coverage and keep `observed_duration = 0`.
- **b4 — `family_id(B) = FAM-UNKNOWN`** *(PRIMARY UNKNOWN-FAMILY ARM DESIGNABLE NOW;
  ~~COMPLETE-WINDOW MUTATION BLOCKED ON OQ-8 + OQ-9 + OQ-11~~
  COMPLETE-WINDOW MUTATION BLOCKED ON OQ-8 + OQ-9 + OQ-11 + OQ-16 — corrected v1.11, W234;
  superseded blocker list retained character for character)*.
  - *Truth:* manifest freezes `B` with `family_id = FAM-UNKNOWN`, `expected_duration = 0`.
    *Verdict:* sibling set unbounded → `untouched(B) = ∅` regardless of direct rows.
  - *Mutation variant:* manifest freezes `B` with a resolved `FAM-<hex>` and a bounded sibling
    set with no contaminating rows → verdict reports the full direct-only duration (not 0).
    This complete-window mutation is **~~BLOCKED ON OQ-8 + OQ-9 + OQ-11~~ BLOCKED ON OQ-8 + OQ-9 +
    OQ-11 + OQ-16** (corrected v1.11, W234; superseded blocker list retained character for
    character) because a non-zero duration
    requires `COMPLETENESS-UNBLOCK` plus positive coverage over every sub-interval of `W_B`.

**Unqualified runnable-now set = ∅.** Split-status set = {b1 primary absent-ledger arm designable
now / complete-window mutation → ~~OQ-8 + OQ-9 + OQ-11~~ OQ-8 + OQ-9 + OQ-11 + OQ-16;
b4 primary unknown-family arm designable now / complete-window mutation →
~~OQ-8 + OQ-9 + OQ-11~~ OQ-8 + OQ-9 + OQ-11 + OQ-16}. Blocked full-fixture set =
{b2 → ~~OQ-8 + OQ-9 + OQ-11 + OQ-12~~ OQ-8 + OQ-9 + OQ-11 + OQ-16 + OQ-12,
b3 → ~~OQ-8 + OQ-9 + OQ-11~~ OQ-8 + OQ-9 + OQ-11 + OQ-16} (all four lists corrected
v1.11, W234; each superseded blocker list retained character for character).

### 5(c) D026 fixture — deliberately contaminated sibling RED without the control, GREEN with it

**Superseded blocker list retained character for character (corrected v1.11, W234):**
~~"BLOCKED ON OQ-8, OQ-9, OQ-11, and OQ-13"~~.
**BLOCKED ON OQ-8, OQ-9, OQ-11, OQ-16, and OQ-13 (OQ-8 added v1.7, G67-F01; OQ-13 added v1.8,
DS47-F01 — the verdict-side operand is the `FAMILY_OBSERVED` marking row, whose schema and store
are unresolved; narrowed v1.9, W196-F03 — superseded wording retained: ~~"whose schema and binding
are unresolved"~~ — the row's *content* is now bound by the §4.2 integrity duty, so what blocks
this fixture is the row's schema and store, not the integrity of its operand).** This fixture
cannot promise positive
confirmation evidence until `COMPLETENESS-UNBLOCK` is true. After unblock, the immutable setup
must provide independently verified, identity-bound coverage over every sub-interval of `W_B` in
**both** toggle arms. The coverage, ledger rows, freezes, trades, and all other inputs are
byte-identical between arms; only the sibling-marking control is toggled.

**Setup.** Family `F`, two packages. `A` frozen at `t0`, composite minted, `FORWARD_SHADOW`
window opens and accumulates forward data. At `t1 > t0` person `P` opens `A`'s shadow record in
the Explorer and keeps the feed open through `t3`; the surfaced window is `[t0, t3]` → ledger
row `r_A` (`observer_kind = HUMAN`, observer `P`, `window = [t0, t3]`). At `t2` with
`t1 < t2 < t3`, person `P` freezes `B` — same `F` (same producer, same parameter-neighbourhood
bin) — choosing `B`'s parameters after seeing `A`'s window. `B`'s evidence window opens at `t2`;
the confirmation-grade trades of `B` fall in `[t2, t3]`.

- **RED (control disabled** — §4 marking off, or §3 ignores `FAMILY_OBSERVED`): `untouched(B)`
  = `[t2, now]` minus direct observations of `B` only ≈ the whole window → `B` shows full
  confirmation evidence → `B` passes the forward-evidence precondition → contaminated candidate
  is promotable. This reproduces gap O-12 (`brief:3486`).
- **GREEN (control enabled):** `siblings(B) = {A}`; `r_A.observed_at = t1 < t2 = B.frozen_at`;
  `A.evidence_window_start = t0 < t2`; `contaminated_interval = [t0, t3] ∩ [t2, now] = [t2, t3]`
  → `FAMILY_OBSERVED` marking row for `B` over `[t2, t3]` → §3 **recomputes** `observed_family(B)`
  from `ledger + graph` and subtracts `[t2, t3]` → `untouched(B)` no longer contains the
  confirmation-grade trades → `confirmation_evidence_duration` falls below the precondition → `B`
  BLOCKED. **(Clarified v1.9, W196-F03; superseded wording retained: ~~"→ §3 subtracts `[t2, t3]`"~~,
  which read as though §3 consumed the marking row as its input.)** §3.2 defines the subtraction as a
  recompute from `ledger + graph` at every gate evaluation; ~~the marking row **records** that
  recomputation and, per §4.2's integrity duty, must equal it — a disagreement is DETECTED and the
  window is INCOMPLETE.~~ **Append-time referent (corrected v1.11, W234; superseded sentence retained
  character for character):** the marking row records the §4.1 recomputation **as it stood when the
  marking was appended** and must equal that append-time recompute at every gate evaluation; an
  edited marking is DETECTED and the window is INCOMPLETE, while legitimately-added later siblings
  or ledger rows are not a failure. The marking row is this fixture's **verdict-side operand**, compared against
  the truth-side manifest below; it is not the value §3 subtracts.

After the named blockers resolve, flipping the single control toggle flips RED↔GREEN with every
other input identical. Before then, both arms remain at zero evidence and no RED/GREEN claim is made.

**Two independent producers (added v1.2, N74-F2).** *Truth-side producer* = an immutable
scenario manifest fixing `t0..t3`, the two package freezes, and `r_A`'s window `[t0, t3]`, and
declaring the **expected** contaminated interval `[t2, t3]` and the expected verdict (GREEN:
`B` BLOCKED). *Verdict-side producer* = §4's `contaminated_interval` computation + §3's
interval-set difference + the forward-evidence precondition check, run against the built store.
Compared operands: `expected_contaminated_interval` / `expected_verdict` (truth) vs the
`FAMILY_OBSERVED` marking row's interval and the gate's PASS/BLOCK (verdict). **Truth-side-only
mutation variant:** move `r_A.observed_at` to `t2' >= t2 + δ` in the manifest and rebuild — under
§4.1's strict `< t2 + δ` comparison the time test now fails, no marking row is produced, and the
verdict-side producer must independently return PASS. Require two boundary variants at the clock's
actual precision: the last representable instant below `t2 + δ` remains time-eligible and BLOCKED;
the instant at `t2 + δ` is not time-eligible and returns PASS. **This mutation arm is BLOCKED ON
OQ-7** until `δ` is ratified or a single time source makes `δ = 0`; no value is invented here.
This proves §4 reads the ledger rather than replaying the manifest's "expected" field.

**Owner-closed input to this mutation arm (added v1.12, W289).** Owner addendum 31 decision 100
(`OWNER_DECISIONS_2026-08-29_EVENING.md:766`) mandates one shared UTC clock, so `δ = 0` and the
boundary variants sit at `t2` at the clock's actual precision: the last representable instant below
`t2` remains time-eligible and BLOCKED, the instant at `t2` is not time-eligible and returns PASS.
The arm stays BLOCKED until the single time source is built (OQ-7). No value is invented here.

The fixture, once built, records real command output (D026 shape, `AGENTS.md:46-47`); no fixture
has been built or run under this DESIGN ONLY draft (reworded v1.1, F-11 — the v1 wording read as
a completion claim).

---

## 6. Acceptance-gate mapping and open questions

### 6.1 A-7d clause → design element → falsification

Every **falsification row** names the **truth-side producer** / **verdict-side producer** and a
truth-side-only mutation variant (added v1.2, N74-F2; scope narrowed v1.7, G67-F03). The non-goals
row is an inspection-only scope fence, not an A-7d falsification claim.

| A-7d clause (`brief:3075`, `plan:534`) | Design element | Falsification (truth-side producer → verdict-side producer; mutation variant) |
|---|---|---|
| lineage graph resolves or explicitly marks `UNKNOWN` | §1.3 resolution order + §1.4 `FAM-UNKNOWN` | *Truth:* fixture registry rows with declared confidence + expected `family_id`. *Verdict:* §1.3 resolver. A `heuristic_auto`-only row → `FAM-UNKNOWN` → BLOCKED for `LIVE_CANDIDATE`. *Mutations:* flip the row to `explicit_metadata` with a confirmed producer token → resolver must now return a `FAM-<hex>` (N74-F5); named `candidate-family-conflict` variant supplies explicit parent → `F1` and existing candidate → `F2` → resolver must refuse both to `FAM-UNKNOWN`, while changing only candidate → `F1` permits `F1` (N99-F03) |
| ledger is append-only | §2.4 access+atomicity contract + retention lock + hash chain + anchor + CI guard | *Truth:* corruption manifest (one bound field changed without recomputing `row_hash` / one bound field changed and only that row recomputed / whole chain rewritten / intact). *Verdict:* row-preimage verifier + successor-link verifier + anchor check. After OQ-12 resolves, a field-only change must be DETECTED by row-hash recomputation; a one-row recompute must be DETECTED by the successor link; after OQ-8 resolves, a whole-chain recompute must be DETECTED by anchor mismatch. **BLOCKED until OQ-8 + OQ-11 + OQ-12:** the retention lock, distinct appender identity, atomic publication, anchor channel, and canonical row-hash byte encoding are unbuilt or `[OPEN]`, so this clause is **not satisfied**. |
| enumeration finds an observation it was not told about | §5(a) two-producer reconciliation, **both producers probed** (v1.1, F-1) | Probe 1: un-instrumented read surfaced by Producer 2 as `UNLEDGERED_OBSERVATION` (truth = read-timeline fixture; verdict = reconciliation) — **this arm alone evidences this clause** (scope restored v1.9, W196-F05; superseded v1.8 wording retained: ~~"…, or a matched row whose Producer-2 timestamp and Producer-1 `observed_at` disagree beyond `δ` refused as `MISDATED_OBSERVATION`"~~ offered as an alternative satisfaction). The `MISDATED_OBSERVATION` refusal (a matched pair whose Producer-2 timestamp and Producer-1 `observed_at` disagree beyond `δ`) is the DS47-F02 check, runs in the same reconciliation and carries the same INCOMPLETE consequence — but a matched pair is by construction a read the ledger **was** told about, so it is **not** evidence for this clause and may not substitute for the `UNLEDGERED_OBSERVATION` arm; it also rests on the NOT VERIFIED Producer-2 timestamp-independence assumption (OQ-7, W196-F08). Probe 2: off-box / unlogged read is NOT DETECTED by either producer → **named residual class**; §3.3 positive-completeness is continuous over all `W_B`, so one uncovered sub-interval makes the whole `W_B` incomplete → `untouched = ∅`. **Superseded predicate retained character for character (corrected v1.11, W234):** ~~`COMPLETENESS-UNBLOCK = OQ-8 exact-head-anchor duty resolved AND OQ-9 interval-attestation duty resolved AND OQ-11 residual read-path producer/prevention duty resolved`.~~ **`COMPLETENESS-UNBLOCK = OQ-8 exact-head-anchor duty resolved AND OQ-9 interval-attestation duty resolved AND OQ-11 residual read-path producer/prevention duty resolved AND OQ-16 window-bounds binding duty resolved`. A single mechanism may satisfy both duties only if it produces two independently checked outputs: exhaustive read-event observations and identity-bound no-read interval attestations.** |
| untouched window **computed** from the ledger, not asserted | §3.2 recompute-at-gate, no stored value, records ledger head hash | *Truth:* fixture store with a planted persisted `untouched = X` field. *Verdict:* gate recompute path. No code path reads the planted value; it is inert (nothing reads it) — and OQ-5 does **not** refuse it, being the `family_id` sentinel question, not `untouched` (corrected v1.10, DS66-F04; superseded wording retained: ~~"OQ-5 contract check refuses it"~~). *Mutation:* change the ledger rows so the true untouched span differs from `X` → gate output tracks the rows, not `X` |
| absent or incomplete ledger → zero confirmation evidence | §3.3 whole-window rule + §5(b) b1–b4 | *Truth:* each fixture manifest declares the ledger state and expected duration. *Verdict:* §3.2 + verifier. Any absent ledger or any incompleteness anywhere in `W_B` → `untouched(B) = ∅` for the whole window and duration 0; `b3` does not subtract only the gap. *Mutation:* a non-zero result is permitted only after the truth-side variant supplies an OQ-8 anchor-covered exact head plus identity-bound relevant-ledger-row-or-scoped-attestation coverage over **every** sub-interval of `W_B`, which the verdict side independently verifies; a wrong package/family/`D`/`E` item is refused (v1.3 G28-F01; v1.6 N99-F04; v1.7 G67-F01) |
| D026 contaminated sibling RED without / GREEN with | §5(c) | **Superseded blocker list retained character for character (corrected v1.11, W234):** ~~"BLOCKED ON OQ-8 + OQ-9 + OQ-11 for completeness, OQ-7 for the time-boundary arm, and OQ-13 for the marking-row verdict operand."~~ **BLOCKED ON OQ-8 + OQ-9 + OQ-11 + OQ-16 for completeness, OQ-7 for the time-boundary arm, and OQ-13 for the marking-row verdict operand.** After unblock: single-toggle fixture; truth = immutable scenario manifest plus an anchor-covered head and independently verified, identity-bound whole-window coverage in both arms; verdict = §4 + §3; boundary mutations put `r_A.observed_at` immediately below and at `B.frozen_at + δ`; only the latter produces no marking and PASS. **OQ-13 narrowed v1.9 (W196-F03):** the marking row's *content* is now checked — ~~it must equal the §4.1 recomputation from `ledger + graph` at every gate evaluation, and a disagreement is DETECTED → INCOMPLETE (§4.2 integrity duty)~~ it must equal the §4.1 recomputation **as it stood when the marking was appended** at every gate evaluation; an edited-row disagreement is DETECTED → INCOMPLETE, while legitimately-added later siblings or ledger rows are not a failure (§4.2 integrity duty; corrected v1.11, W234; superseded referent retained character for character) — so what OQ-13 still blocks here is the marking row's **schema and store**, not the integrity of the verdict operand (v1.6 N99-F01/F02; v1.7 G67-F01; v1.8 DS47-F01; v1.9 W196-F03) |
| required family/confirmation precondition before first `LIVE_CANDIDATE`; WP-V2A-10 / WP-V3-03 / WP-V4-01 consume it (`brief:1445`) | design emits `family_id`(/`FAM-UNKNOWN`), `FAMILY_OBSERVED` markings, `confirmation_evidence_duration` as those gates' input | *Truth-side producer:* immutable eligibility-input fixture, with every unrelated gate input held eligible, declares invalid `FAM-UNKNOWN` or `untouched = ∅` and expected refusal at this precondition. *Verdict-side producers:* the exact WP-V2A-10 candidate-eligibility gate, WP-V3-03 Promotion Authority gate, and WP-V4-01 live-admission gate implementations. *Operands:* fixture `expected_precondition_verdict` vs each gate's observed accepted/refused result and reason. *Truth-side-only mutation:* replace the invalid family/confirmation input with a valid resolved family and positively complete non-zero confirmation input; each gate must cease refusing **for this precondition only**. This does not assert an overall promotion/admission outcome. **Marking-row input is now guarded (added v1.9, W196-F03):** ~~no gate may consume a `FAMILY_OBSERVED` marking that did not equal the §4.1 recomputation from `ledger + graph` at that same evaluation (§4.2 integrity duty); an edited marking is DETECTED and the window is INCOMPLETE.~~ At every gate evaluation, no gate may consume a `FAMILY_OBSERVED` marking unless it equals the §4.1 recomputation **as it stood when the marking was appended**; an edited-row disagreement is DETECTED and the window is INCOMPLETE, while legitimately-added later siblings or ledger rows are not a failure (§4.2 integrity duty; corrected v1.11, W234; superseded sentence retained character for character). Superseded blocker list retained character for character (corrected v1.11, W234): ~~"BLOCKED until those exact downstream implementations, `COMPLETENESS-UNBLOCK`, and the OQ-13 marking-row **schema and store** exist"~~. BLOCKED until those exact downstream implementations, `COMPLETENESS-UNBLOCK` (including its OQ-16 window-bounds binding conjunct), and the OQ-13 marking-row **schema and store** exist (v1.6 N99-F06; v1.8 DS47-F01; v1.9 W196-F03) |
| non-goals (`plan:537`) | design computes/marks only — no promotion decision; §6.6 rules 1–5 untouched; markings append-only (no retroactive cleaning) | **Inspection-only scope fence; no A-7d falsification claim.** |

### 6.2 Open questions — each a NAMED BLOCKER (no default)

- **OQ-1 `PROVISIONAL-ON-P013` — package enumeration.** "Every package" needs the authoritative
  package list and the `package_hash ↔ candidate_id` join. Today only 63 `STGxxx` registry
  entries and an unpopulated `TrialRecord` schema exist. Blocks resolving `family_id` "per
  package" until P0-13 defines the package/candidate catalog and its keys.
  **Package-hash preimage open (added v1.10, DS66-F02):** `package_hash` — the resolution unit (§1.1) and the predicate key for `observed_direct` and `coverage_key(B)` — has no stated preimage, no named producer, and no open question, unlike every other identity here (`row_hash` → OQ-12, `observation_id` → OQ-15, `FAM-UNKNOWN` → OQ-5). No §0 input names the source of its bytes/order/encoding; the "package freeze record" that carries it (`:311`, `:343`) is not a named store. As written, two implementations could produce different `package_hash` for one package and misbind observer rows, inflating `untouched(B)`. Owner must name `package_hash`'s preimage and producer before build. Open question, no byte tuple invented.
- **OQ-2 `PROVISIONAL-ON-P013` — ledger store location and tier.** Exact path, retention, DuckDB
  registration, artifact tier deferred to P0-13 (`plan:951`).
- **OQ-3 `PROVISIONAL-ON-P013` / NOT VERIFIED — optimizer read instrumentation point.** The
  exact function in the migrated canonical path (WP-P0-20 delivers it; P0-13 depends on it) that
  reads prior-package forward records is the Producer 1 hook for `OPTIMIZER` observations. Cannot
  be cited against code now. **Extended v1.8 (DS47-F03):** the Producer-2 `ACCESS_RECONCILIATION`
  optimizer channel has the same status — the run manifests recording which prior `package_hash`
  values a trial consumed as warm-start input (from `TrialRecord` provenance) name a field that
  is not cited in `trials.py`; until the canonical path is migrated and that field exists and is
  cited, the channel is NOT VERIFIED and the `OPTIMIZER` branch of the §4.1 linkage test cannot be
  operationalized (see OQ-7, extended).
- **OQ-4 — `parameter_neighbourhood` bucketing rule.** `compute_family_id` hashes the
  neighbourhood spec (`identity.py:149-154`); the test uses `{"period":[18,22]}`
  (`test_identity.py:108`). Bin edges, per-axis vs joint bucketing, bin count are undefined.
  An invented bin rule would be a self-serving threshold (C-4). Owner / P0-04 must ratify it.
  **OWNER-CLOSED (added v1.12, W289) — owner addendum 31 decision 98, row 17, 2026-09-02.**
  Superseded open-choice text retained character for character (the sentences above are left
  unedited; nothing is deleted): ~~"Bin edges, per-axis vs joint bucketing, bin count are undefined.
  An invented bin rule would be a self-serving threshold (C-4). Owner / P0-04 must ratify it."~~
  **DECIDED — owner addendum 31 decision 98 (2026-09-02), owner verbatim:** "Treat every trial from
  one approved search-space version, for one strategy, as one family. Do not invent arbitrary
  parameter buckets." (`OWNER_DECISIONS_2026-08-29_EVENING.md:764`; recommendation basis JUDGEMENT —
  the owner's word is the sole authority, same file `:729-730`).
  **Consequence in this draft's vocabulary.** There is no bin rule left to ratify: bucketing is
  refused, so `parameter_neighbourhood` may not be a bin-tuple. The family key is (approved
  search-space version, strategy), and every trial under one such version for one strategy is one
  family. §1.2's reading (`:368-372`) keeps its first half — the caller computes the
  neighbourhood from `TrialRecord.preregistered_space_hash` (`trials.py:28`) — and loses its second,
  the per-axis bin assignment. D-3's reconciliation (`:1503-1507`), "pass a pre-bucketed
  spec", is read the same way: the pre-bucketed spec is the space-version identity, not a bin-tuple.
  **Not closed by this decision (a decision closes only what it names).** (a) `compute_family_id`
  hashes `parameter_neighbourhood` exactly (`identity.py:149-154`), so expressing "one approved
  search-space version, one strategy" as its input is a **WP-P0-04 contract change** this draft may
  not make — the same fence as OQ-5. (b) Which recorded field carries "strategy" is not stated: the
  §1.2 triple names `source_provenance` and `producer`, not a strategy id, and the registry `STGxxx`
  rows are seed material only (§1.1, D-2). (c) What makes a search-space version **approved** — the
  approval record, its store, its version identity — is named by no §0 input, and
  `preregistered_space_hash`'s own preimage and sole producer are the P0-13 blocker B-12 (census
  X-1, `W269_PHASE0_OWNER_QUESTIONS.md:624-629`). No value, identity or byte tuple is invented here.
  **OQ-4 therefore remains a NAMED BLOCKER on its engineering half** (owner: the WP-P0-04 /
  WP-P0-13 lanes), with its owner half closed.
- **OQ-5 — `UNKNOWN` sentinel not enforceable by the current contract.**
  `TrialRecord.family_id` is `NonEmptyStr` with no allowed-value set (`trials.py:22`);
  `compute_family_id` always returns `FAM-<hex>`, never `UNKNOWN` (`identity.py:154`). A P0-04
  contract change is needed to define literal `FAM-UNKNOWN` and to refuse a `LIVE_CANDIDATE`
  carrying it. P0-22 may not edit that schema.
- **OQ-6 — producer token source of truth.** Producer is parsed from `source_folder` naming
  (`STRATEGY_RESEARCH_REGISTRY.json:10`) vs `harvested_tags` author names
  (`TAG_DICTIONARY.json:57-251`); no canonical producer list. **Confidence is not uniform
  (re-censused v1.2, N74-F5):** of 63 rows, **46** are `classification_confidence:
  "heuristic_auto"` (`:64`) and **17** are `"explicit_metadata"` (`:2427`) — census method
  `grep -oE '"classification_confidence": *"[a-z_]+"' | sort | uniq -c`. Without a ratified
  producer registry, a derived-triple `family_id` whose row is `heuristic_auto` **and** whose
  producer token is not independently confirmed inherits heuristic uncertainty and collapses to
  `FAM-UNKNOWN` (§1.3 step 3). An `explicit_metadata` row is not forced to `FAM-UNKNOWN` on
  confidence grounds; the canonical-producer question (which of `source_folder` vs
  `harvested_tags` is authoritative, and how they are reconciled) stays open for all rows.
- **OQ-7 — "decision could have seen `r`" linkage (§4.1), and the clock-skew margin `δ` (extended
  v1.1, F-3; extended v1.8, DS47-F02/F03).** Whether a given human observation fed a given freeze
  decision is recorded nowhere today. Design fails closed (any time-eligible sibling row
  contaminates), which may over-mark.
  Owner must decide: accept fail-closed over-marking, or require a decision-provenance link (who
  approved `B`, from which session) captured at freeze — likely a WP-P0-31 lifecycle-ledger
  field. **Extended v1.8 (DS47-F03):** the `OPTIMIZER` branch of the linkage test —
  `r.observer_kind = OPTIMIZER` whose run produced `B` — is doubly unbound: neither the ledger
  row's run identity nor a freeze record naming the producing run is stated. Owner must decide
  how the producing run is recorded on the row and at freeze, or the branch stays
  fail-closed-only (any time-eligible `r`, which may over-mark). **Extended v1.8 (DS47-F02):**
  `observed_at` is self-reported by the producing writer and drives the §4.1 time test; the §5(a)
  Probe-1 reconciliation (extended to compare timestamps) is the named check, and its tolerance
  is `δ` — so the timestamp-agreement predicate is BLOCKED on this same OQ.
  **Extended v1.9 (W196-F08) — the independence assumption that check rests on.** The Probe-1
  timestamp-agreement check assumes Producer-2 timestamps (the `mcc_readonly` HTTP access log and
  the DuckDB / Parquet query log) are **server-side and independent of the producing writer's
  clock**. If that server shares the writer's skew, a self-reported `observed_at` running ahead by
  more than `δ` agrees with a Producer-2 stamp carrying the same skew, and the check does not fire —
  which is the leak direction §5(a) names. `DS48_P022_PATCH.md:367` recorded this assumption as
  "flagged in OQ-7"; it was **not** in OQ-7 until this fold, so the sole named check closing
  DS47-F02 rested on an assumption the draft never stated. Status: **NOT VERIFIED** — no built
  Producer-2 implementation is named anywhere in this draft, and the applying lane recorded the same
  (`W193_P022_APPLY_REPORT.md:117-119`). Owner must either require a time source for the Producer-2
  channels that is independent of the five writer classes, or record that DS47-F02's closure rests
  on an unverified independence assumption.
  **Added v1.1:** the §4.1 time test now uses a bounded inter-writer clock-skew margin
  `δ` (`r.observed_at < B.frozen_at + δ` counts as time-eligible). `δ` has no ratified value; an
  invented value would be a self-serving threshold (C-4). Owner / P0-04 must set it, or mandate a
  single time source for all five writer classes so `δ = 0`. The §5(c) clean mutation and its
  immediately-below/at-boundary variants remain BLOCKED until that choice is ratified.
  **OWNER-CLOSED (added v1.12, W289) — owner addendum 31 decision 99, row 18, 2026-09-02 —
  limb (a), the over-marking choice.** Superseded open-choice text retained character for character
  (the sentences above are left unedited): ~~"Owner must decide: accept fail-closed over-marking, or
  require a decision-provenance link (who approved `B`, from which session) captured at freeze —
  likely a WP-P0-31 lifecycle-ledger field."~~ **DECIDED — decision 99 (2026-09-02), owner
  verbatim:** "Accept conservative over-marking for now. Do not add new record-keeping machinery
  yet." (`OWNER_DECISIONS_2026-08-29_EVENING.md:765`).
  **Consequence.** The §4.1 linkage test keeps its fail-closed third arm — "when the decision link
  cannot be established, **any** `r` passing the time test" (`:736-739`) — as the
  accepted design, not as a placeholder. No decision-provenance field is captured at freeze and none
  is requested of WP-P0-31 by this draft. Over-marking (a clean sibling marked `FAMILY_OBSERVED`
  because some time-eligible row exists) is an **accepted** outcome, not a defect awaiting repair.
  "For now" is the owner's own qualifier: the choice is revisitable, and this draft records it as
  revisitable rather than permanent.
  **Not closed by this decision.** The `OPTIMIZER` limb above (`:1167-1171`) — how the
  producing run is recorded on the row and at freeze — was split out of this row by the census
  (`W269_PHASE0_OWNER_QUESTIONS.md:379-387`) and was **not** put to the owner as row 18. It stays
  open and stays fail-closed-only. Recording a producing-run identity is arguably the "new
  record-keeping machinery" decision 99 declines, but this draft does not close an unasked row by
  inference.
  **OWNER-CLOSED (added v1.12, W289) — owner addendum 31 decision 100, row 19, 2026-09-02 —
  limb (b), the clock-skew margin `δ`.** Superseded open-choice text retained character for
  character: ~~"`δ` has no ratified value; an invented value would be a self-serving threshold
  (C-4). Owner / P0-04 must set it, or mandate a single time source for all five writer classes so
  `δ = 0`."~~ **DECIDED — decision 100 (2026-09-02), owner verbatim:** "Use one shared UTC clock;
  allow no hidden clock difference." (`OWNER_DECISIONS_2026-08-29_EVENING.md:766`).
  **Consequence.** The second arm of this row's own alternative is taken: a single time source is
  mandated for all five §2.3 writer classes (`:508-529`), so **`δ = 0`**. The value is
  not invented here — it is this row's own stated consequence of that arm (`:1190`, and
  identically at `:840-841` and `:1063`); the authority for taking the arm is
  decision 100. With `δ = 0`: the §4.1 time test reads `r.observed_at < B.frozen_at`
  (`:725-728`); the §5(a) `MISDATED_OBSERVATION` predicate compares the two stamps with
  zero tolerance (`:828-842`); and the §5(c) boundary variants sit at `t2` at the
  clock's actual precision rather than at `t2 + δ` (`:1058-1063`). "Allow no hidden clock
  difference" also refuses the reading in which a difference exists but is left unmeasured.
  **Not closed by this decision.** Which UTC source the five writer classes share, how each is moved
  onto it, and what component demonstrates that no hidden difference remains are engineering (owner:
  the build lane, with WP-P0-04 for any contract surface). Until that exists, `δ = 0` is a ratified
  value with unbuilt enforcement, so the timestamp-agreement arm stays BLOCKED on delivery rather
  than on the owner.
  **OWNER-CLOSED (added v1.12, W289) — owner addendum 31 decision 101, row 20, 2026-09-02 —
  limb (c), Producer-2 timestamp independence.** Superseded open-choice text retained character for
  character: ~~"Owner must either require a time source for the Producer-2 channels that is
  independent of the five writer classes, or record that DS47-F02's closure rests on an unverified
  independence assumption."~~ **DECIDED — decision 101 (2026-09-02), owner verbatim:** "Require an
  independent clock for access logs." (`OWNER_DECISIONS_2026-08-29_EVENING.md:767`).
  **Consequence.** The first arm is taken: the Producer-2 channels — the `mcc_readonly` HTTP access
  log and the DuckDB / Parquet query log (`:1176-1178`) — must carry a time source
  independent of the five §2.3 writer classes. The "record the assumption in writing" arm is
  **refused**, so independence is now a requirement to be met, not an assumption to be disclosed.
  The W196-F08 status is unchanged in substance — no built Producer-2 implementation is named
  anywhere in this draft, so independence stays **NOT VERIFIED** — but it is now unverified against
  a requirement, and the §5(a) Probe-1 timestamp arm may not be claimed until an independent source
  is named and shown.
  **Extended v1.12 (W289) — the item decisions 100 and 101 open together, not closed.** Decision 100
  puts the five writer classes on one shared UTC clock (`δ = 0`); decision 101 requires the access
  log's clock to be independent of them. Both can hold — a shared UTC time base with an independent
  clock for the Producer-2 channels is the reading recorded here — but together they leave the
  **cross-producer** comparison without a stated tolerance: `δ = 0` is the inter-writer margin,
  while the §5(a) Probe-1 comparison is between a writer's `observed_at` and an independently-clocked
  access-log stamp. Neither decision names a value for that comparison and none is invented here.
  This is an extension of OQ-7, not a new blocker and not a closed row: **cross-producer tolerance —
  NOT DECIDED**, to be put to the owner as its own question.
- **OQ-8 — external anchor mechanism.** WP-P0-26 (text-class to GitHub, `plan:580`) and
  WP-P0-27 (CI home, `plan:590`) are both planned-and-unbuilt. Until one exists, append-only is
  chain-verifiable only after OQ-12 resolves and is not independently anchored. OQ-8's exact-head-
  anchor duty is a conjunct of `COMPLETENESS-UNBLOCK`; no non-empty `untouched` window may be
  restored without it. Named dependency, not resolvable inside P0-22.
- **OQ-9 — no-read attestation format, incl. the Producer-2 residual class (extended v1.1, F-1;
  extended again v1.2, N74-F1).**
  §3.3 coverage-gap handling needs a positive "no reader ran / nothing surfaced" record for
  intervals; its shape and emitter are undefined. Blocks distinguishing "clean" from "unknown".
  **v1.1:** the attestation must also cover the residual class Producer 2 provably cannot
  enumerate — off-box copies of the catalog Parquet, `noatime` mounts outside the research host,
  and any read surface not yet wired into `ACCESS_RECONCILIATION` (§5(a) Probe 2).
  **v1.2 (N74-F1):** §3.3 positive-completeness is now **continuous over all of `W_B`** — a
  sub-interval is complete only if a relevant ledger row **or** a scoped attestation under
  `coverage_key(B)` covers it, regardless of
  whether a reader was independently known there. Consequence: **until this attestation emitter
  exists, no window is positively complete, so `untouched(B) = ∅` for every `B`.** This is the
  intended fail-closed state. **Superseded predicate retained character for character (corrected
  v1.11, W234):**
  ~~`COMPLETENESS-UNBLOCK = OQ-8 exact-head-anchor duty resolved AND
  OQ-9 interval-attestation duty resolved AND OQ-11 residual read-path producer/prevention duty resolved`.~~
  **`COMPLETENESS-UNBLOCK = OQ-8 exact-head-anchor duty resolved AND
  OQ-9 interval-attestation duty resolved AND OQ-11 residual read-path producer/prevention duty
  resolved AND OQ-16 window-bounds binding duty resolved`. A single mechanism may satisfy both
  duties only if it produces two independently checked outputs: exhaustive read-event observations
  and identity-bound no-read interval attestations.** The attestation must bind the
  exact §3.3 `coverage_key(B)` or an independently declared global domain; wrong package/family/
  `D`/`E` coverage is refused.
- **OQ-10 — re-audit checkpoint.** Per lane spec this draft is re-audited after P0-13 accepts,
  before any build. No build authorization exists; design frozen pending P0-13 acceptance and
  re-audit.
- **OQ-11 — ledger access-control + atomicity contract, and the copy/export producer-or-prevention
  choice (added v1.2, N74-F1 / N74-F3).** §2.4's real append-only enforcement needs: clients with
  no filesystem write access to the store; a distinct appender principal whose write access is
  create-only under a storage-level retention/object lock (no overwrite, no delete, including by
  the appender and root-equivalent tooling); atomic-or-recoverably-journaled part-file + manifest
  publication; and the anchor (OQ-8) covering the exact computed head before evidence counts.
  None of this exists today — the store layout is P0-13's (OQ-2). **Separately**, the §5(a)
  Probe 2 residual class (off-box copy, `noatime` mount, un-wired surface) needs an owner
  decision: either (a) an independent, structurally unavoidable producer that emits an
  observation row for every copy/export and raw-file access, or (b) a boundary that *prevents*
  those paths, or (c) accept that the entire `W_B` stays incomplete (`untouched = ∅`).
  **Superseded predicate retained character for character (corrected v1.11, W234):**
  ~~`COMPLETENESS-UNBLOCK = OQ-8 exact-head-anchor duty resolved AND OQ-9 interval-attestation
  duty resolved AND OQ-11 residual read-path producer/prevention duty resolved`.~~
  **`COMPLETENESS-UNBLOCK = OQ-8 exact-head-anchor duty resolved AND OQ-9 interval-attestation
  duty resolved AND OQ-11 residual read-path producer/prevention duty resolved AND OQ-16
  window-bounds binding duty resolved`. A single mechanism may satisfy both duties only if it
  produces two independently checked outputs: exhaustive read-event observations and
  identity-bound no-read interval attestations.** Until OQ-11 resolves, the A-7d append-only
  clause is BLOCKED (§6.1) and the enumeration clause cannot claim the residual class is routed
  to zero.
  **OWNER-CLOSED (added v1.12, W289) — owner addendum 31 decision 102, row 21, 2026-09-02 — the
  copy/export producer-or-prevention choice.** Superseded open-choice text retained character for
  character (the sentences above are left unedited): ~~"the §5(a) Probe 2 residual class (off-box
  copy, `noatime` mount, un-wired surface) needs an owner decision: either (a) an independent,
  structurally unavoidable producer that emits an observation row for every copy/export and raw-file
  access, or (b) a boundary that *prevents* those paths, or (c) accept that the entire `W_B` stays
  incomplete (`untouched = ∅`)."~~ **DECIDED — decision 102 (2026-09-02), owner verbatim:** "Prevent
  unlogged copying or reading of results by building a proper boundary. This is costly, so record
  that cost openly." (`OWNER_DECISIONS_2026-08-29_EVENING.md:768`).
  **Consequence.** Option **(b)** is chosen: a boundary that prevents the off-box copy, the
  `noatime` mount and the un-wired read surface (§5(a) Probe 2). Options (a) and (c) are
  **refused** — the residual class may not be closed by watching it, and the arm that accepts
  `untouched = ∅` forever is off the table. The `COMPLETENESS-UNBLOCK` conjunct "OQ-11 residual
  read-path producer/prevention duty resolved" is therefore specifically a **prevention** duty from
  here on.
  **COST: UNPRICED - owner requires it recorded; no sourced figure exists.** Decision 102 requires
  the cost recorded openly, and the ledger repeats the rule ("row 21 requires an explicit cost line
  with a source, no estimate without one", `OWNER_DECISIONS_2026-08-29_EVENING.md:834`). No sourced
  figure exists to record: this draft carries no cost, budget or effort figure for the boundary (its
  only "estimated" is §4.1's "computed, not estimated", `:741`), the ledger carries none, and
  the decisions page says only "(a) and (b) cost real engineering"
  (`OWNER_PHASE0_DECISIONS_V1.md:67`). No number is invented; the line stands as UNPRICED until a
  lane produces a sourced one.
  **Not closed by this decision.** The boundary does not exist: what enforces it, at which layer, and
  what proves a prevented path stays prevented are all unstated, so the `COMPLETENESS-UNBLOCK`
  conjunct stays **unresolved** and `untouched(B) = ∅` for every `B` (§3.3) exactly as before. The
  ledger access-control + atomicity half of OQ-11 (`:1286-1292`) is engineering and is
  untouched by this decision. OQ-11 remains a NAMED BLOCKER with its owner half closed.
- **OQ-12 — canonical `row_hash` byte encoding (added v1.7, G67-F02).** The preimage field set and
  order are fixed in §2.4 to every existing §2.1 field except `row_hash`, including `prev_hash`.
  The exact canonical byte encoding is **`[OPEN]`**: string normalization, timestamp encoding,
  enum representation, length framing, and nullability rules are not ratified in the cited
  repository sources. Until that encoding is ratified, the appender and verifier cannot be shown
  to compute the same bytes, so the per-row hash check and dependent chain-break claims remain
  BLOCKED. No serialization rule is invented by this draft.
- **OQ-13 — `FAMILY_OBSERVED` marking-row schema and store (added v1.8, DS47-F01; premise
  corrected, integrity duty bound, blocker narrowed v1.9, W196-F03).**
  §4.1 appends a `FAMILY_OBSERVED` marking row for `B` naming `B.package_hash`, sibling
  `A.package_hash`, the ledger row ids `r`, the computed interval(s), `F`, a timestamp, and the
  ledger head hash; §6.1 row 7 consumes these markings as gate input and §5(c) compares the
  marking row's interval as its verdict operand. The row's set-valued content cannot be
  represented in the §2.1 observation schema, and none of it is inside the §2.4 `row_hash`
  preimage.
  **Superseded v1.8 premise, retained:** ~~"…, so no named check fails if the marking row's content
  is edited."~~ **Corrected (W196-F03): that was false — two named things in this document fail on
  an edited marking.** (1) §5(c) already compares `expected_contaminated_interval` /
  `expected_verdict` (truth side, an immutable scenario manifest) against the marking row's interval
  and the gate's PASS/BLOCK (verdict side); an edited interval moves the verdict-side operand away
  from the manifest, which is the comparison that fixture exists to fail. (2) The production path
  never reads a marking as an assertion: `observed_family(B)` is defined over **ledger rows**
  (§3.2), the untouched window is "recomputed from `ledger + graph` at every gate evaluation"
  (§3.2), and marking is "re-derived from the ledger for every new sibling — never copied as a flag"
  (§4.2).
  **Integrity duty, bound to that existing recompute (§4.2, added v1.9).** ~~At every gate evaluation
  each `FAMILY_OBSERVED` marking row presented for `B` must equal the §4.1 recomputation from
  `ledger + graph` — same sibling, same ledger row ids, same interval(s), same `F`.~~ **Append-time
  referent (corrected v1.11, W234; superseded sentence retained character for character):** at
  every gate evaluation each `FAMILY_OBSERVED` marking row presented for `B` must equal the §4.1
  recomputation **as it stood when the marking was appended** — the same sibling, ledger row ids,
  interval(s), and `F` written then. Legitimately-added later siblings or ledger rows are not a
  failure. *Failing input:*
  a marking row edited after it was appended. *Observable result:* recomputation disagrees →
  **DETECTED** → the marking is refused as gate input and the ledger is INCOMPLETE for `W_B` under
  §3.3, so `untouched(B) = ∅`. No gate may consume a marking that did not pass that comparison at
  the same evaluation.
  **What remains open, and why the recompute does not carry it.** The comparison detects an edited
  marking; it does not give the marking row a **schema** or a **store**. Nothing in this document
  makes the marking row's own storage append-only, chain-bound or anchored, the recompute cannot
  supply a canonical shape for set-valued content the §2.1 schema cannot express, and the ledger
  head hash the marking records is not itself verifiable until OQ-12 and OQ-8 resolve. Owner must
  decide the marking row's schema and its store — extend the §2.1 schema + preimage with a
  marking-row shape, or give the marking row its own append-only schema, chain, and anchor — before
  build. Until that resolves, §5(c) and §6.1 row 7 stay BLOCKED on this OQ for the schema/store
  question, no longer for the integrity of the operand.
- **OQ-14 — family-lineage graph store enforcement, head anchor and chain binding (added v1.8,
  DS47-F04; premise corrected, contamination-detection duty bound, blocker narrowed v1.9,
  W196-F04).** §1.5 declares
  `family_id` and its producing signals written once at freeze and "immutable thereafter"; §1.6
  declares the store "append-only" and co-located with the observation ledger. The §2.4
  access+atomicity contract, the hash chain, the OQ-8 exact-head anchor, and
  `COMPLETENESS-UNBLOCK` are scoped to the observation-ledger store and its §2.1 row preimage;
  the graph store's nodes/edges are not §2.1 fields — yet `siblings(B)` (§4.1) and therefore
  `observed_family(B)` (§3.2) and the `coverage_key(B)` identity predicate (§3.3) derive from it.
  **Superseded v1.8 premise, retained:** ~~"…so no named component fails if a family edge is edited
  or removed"~~. **Corrected (W196-F04): that was false for the leak-direction defect the census
  actually named** — "graph-edge removal undetected → a sibling's reads stop contaminating"
  (`DS47_RUN.log:83`). Every observation row already carries the package's **frozen** `family_id` as
  a first-class §2.1 field (§2.1, "never re-resolved at observation time"), and that field is inside
  the §2.4 `row_hash` preimage, so the ledger is a second, chain-bound record of family membership.
  **Cross-check bound to it (§4.1, added v1.9):** `siblings(B)` must contain every package whose
  ledger rows carry `family_id = F`. *Failing input:* an edge for sibling `A` edited or removed
  while `A`'s rows still assert `F`. *Observable result:* graph-derived `siblings(B)` omits `A`
  while the chain-bound rows assert `F` → **DETECTED** → fail-closed, `untouched(B) = ∅` for the
  whole `W_B` (§3.3). Editing `A`'s rows instead changes a bound preimage field and must be DETECTED
  by §2.4's row-hash / successor-link / anchor checks.
  **What remains open, and why the cross-check does not carry it.** (a) The cross-check's
  chain-binding force is itself BLOCKED on OQ-12 (canonical `row_hash` byte encoding) and OQ-8
  (exact-head anchor) — until those resolve, "chain-bound" is a declaration like any other. (b) A
  package with **no ledger rows at all** leaves no chain-bound trace, so removing its edge is
  invisible to this route. (c) The cross-check detects a *disagreement*; it does not make the graph
  store append-only, does not anchor its head, and does not bind its nodes and edges into any chain
  — a coordinated edit of the graph alone, for a package with no rows, still passes. Owner must
  decide the graph store's enforcement, head anchor, and chain binding (extend the §2.4 contract to
  cover the co-located store, or a separate contract) before build.
- **OQ-15 — `observation_id` composition and generator (added v1.8, DS47-F07; uniqueness duty
  bound and blocker narrowed v1.9, W196-F02).**
  §2.1 declares `observation_id` "opaque unique id"; the §2.4 preimage binds the value, but the
  bytes that compose it and the generator that issues it are unstated. Same class as the
  `access_path` "query-text hash" (§2.1), folded here. Owner must state the identity's composition
  and its generator.
  **Also folded here (added v1.10, DS66-F08):** `observer_identity` ("person id, or process id +
  code sha", §2.1) — same class; the chain binds the value, not its composition. It feeds the §4.1
  linkage test (`r.observer_kind = HUMAN` who is also `B`'s approver), which cannot match without
  a defined person id plus an approver record; the `OPTIMIZER` branch is separately unbound (OQ-7).
  **Superseded v1.8 wording, retained:** ~~"…, and any check that refuses a duplicate are unstated.
  Two rows carrying the same `observation_id` both hash correctly — the chain binds the value, not
  its uniqueness. … Owner must state … the component that verifies uniqueness, or the uniqueness
  guarantee is declared but unchecked."~~ **Corrected (W196-F02): the uniqueness half needed no
  invented bytes and no new component.** The single serialising appender (§2.4) is the **only**
  writer of the store — the same choke point the v1.8 round gave a refusal duty for `writer_seq`
  monotonicity (DS47-F06) — so every `observation_id` that can enter the store passes through it.
  *Failing input:* a candidate row carrying an `observation_id` the appender has already accepted.
  *Observable result:* the row is **refused** → dropped candidate row → coverage gap → §3.3
  incomplete → `untouched(B) = ∅` (§2.4, §5(a) Producer 2) — the identical fail-closed exit as the
  `writer_seq` refusal.
  **What remains open, and why the appender does not carry it.** The composition half does need
  bytes the in-fence sources do not supply: nothing cited states what an `observation_id` is made
  of or what issues it, and inventing either would be a manufactured preimage. **Residual, stated
  honestly:** the appender's check is scoped to rows it accepted into **this** store — it binds no
  external meaning to the identity, and its durability across an appender restart rests on
  recovering the accepted-id set from the retained rows, i.e. on the store contract (OQ-2 / OQ-11),
  which is itself open.
- **OQ-16 — window-bounds binding (added v1.10, DS66-F01).** `window_start` / `window_end` record the slice of the evidence window the producing writer says it showed; nothing in this document names a component that binds that recorded slice to what was actually displayed. §5(a) Probe 1 reconciles Producer 2 against Producer 1 on read identity and timestamp only, never on window bounds; the fail-closed default covers only the *omitted*-window case, not a bounded-but-narrow window. This is the same self-report defect class the timestamp arm closes with `MISDATED_OBSERVATION` (DS47-F02), but for the window no named check exists and no `window`-equivalent refusal is defined. Owner must name the component that binds the recorded window to the observed data and the input that makes it refuse, or withdraw the window as a control and accept the leak direction explicitly. BLOCKED until then.
  **OWNER-CLOSED (added v1.12, W289) — owner addendum 31 decision 103, row 22, 2026-09-02.**
  Superseded open-choice text retained character for character (the row above is left unedited):
  ~~"Owner must name the component that binds the recorded window to the observed data and the input
  that makes it refuse, or withdraw the window as a control and accept the leak direction
  explicitly."~~ **DECIDED — decision 103 (2026-09-02), owner verbatim:** "Bind the screen's
  displayed result window directly to its recorded window."
  (`OWNER_DECISIONS_2026-08-29_EVENING.md:769`).
  **Consequence.** The withdraw-the-control arm is **refused**: `window_start` / `window_end` stay a
  control, and the displayed window must be bound to the recorded one. The §2.1 row's self-report
  status (`:478`) and the v1.10 withdrawal of the "actually shown" claim stand as statements of
  what is enforced **today**; the binding is now required rather than optional.
  **`OWNER-ANSWERED-SHAPE, VALUE PENDING`.** The owner named the direction, not the component: the
  binding component and the input that makes it refuse are still unnamed, and this draft may not name
  them — naming one would be inventing an identity (C-4). **OQ-16 stays BLOCKED** and stays a
  conjunct of `COMPLETENESS-UNBLOCK` (`:699-703`, `:1277-1278`,
  `:1301-1303`); no §5 fixture and no §6.1 row is unblocked by it. What changed is that
  one of its two arms is gone.

---

## Discrepancies

Recorded per C-2 (repository wins over the prompt).

- **Fold note (v1.2, N74-F5 / N74):** the v1.1 change log records "verified against … HEAD
  `50580df1`". The working tree during the v1.2 fold is at commit `c18b6f3e` (observed once,
  read-only). N74's own report could not verify that identity (its lane prohibited Git). The
  repository line content re-checked this fold (`trials.py:22`, `identity.py:144-154`, the
  registry census, `plan:534-537`) still resolves; the stale HEAD string in the v1.1 block is
  left as the record of what W66 did and is superseded by the v1.2 verification block above.
- **Fold note (v1.9, W196-F10) — cross-artifact line cites drift with every fold; resolve them by
  anchor text.** The hand-applied DS47-F03 Patch A added 3 lines inside §5(a)'s Producer-2 clause
  *after* the W193 lane finished, so that report's cites into this draft above that site stopped
  resolving. Mapping as it stood at v1.8 (recorded by `DETECT_W196_P022.md:242-249`, re-checked in
  this fold): `W193_P022_APPLY_REPORT.md`'s `:590-601` → 593-604, `:892-920` → 895-923, `:978` →
  981, `:1030-1035` → 1033-1038; its cites below the edit site (`:411-420`, `:492`, `:545-546`,
  `:717-719`, `:782-783`) still resolved. **This v1.9 fold shifts every one of them again**, so no
  fixed offset is given here. `W193_P022_APPLY_REPORT.md`, `DETECT_W196_P022.md` and the earlier
  detection reports are **not** edited: each is the record of the draft its lane read. Any later
  lane resolving a cross-artifact cite into this draft must locate it by **section and anchor
  text**, not by a line number carried from an earlier version. No repository file is involved.
- **D-1 — no conflict, recorded for completeness (downgraded v1.1, F-10).** Plan WP-P0-22
  Inputs (`plan:529`) and Depends-on (`plan:531`) list "WP-P0-04 identity and lineage types" as a
  dependency. The plan does **not** state P0-04 is unbuilt or pending — the v1 wording
  ("WP-P0-04 is merged, not pending") over-framed a plain dependency listing as a discrepancy the
  plan text does not create. Observed state, recorded for completeness: the contracts package v0
  is present on `master` (`contracts/mtc_contracts/identity.py:144-154` `compute_family_id`;
  `trials.py:22` `family_id: NonEmptyStr`; `lineage.py:10-41` `EnvironmentLineage` /
  `EvidenceIdentity`), so this design targets real merged symbols. This matches the D-5 form for
  the identical P0-13 dependency listing. No repository/prompt contradiction. (Commit SHAs
  unverifiable under the read-only + no-git fence and are not asserted here.)
- **D-2 — the "taxonomy seed" carries no family assignments.** Brief §6.6 rule 6 (`brief:1441`)
  and §10.3 mechanism 2 (`brief:1993`) say the registry / tag dictionary taxonomy is "already
  present" and "seeds" `family_id`. Repository: `STRATEGY_RESEARCH_REGISTRY.json` has **no**
  `family_id`, `candidate_id`, `package_hash`, or parent field (field list read from the file;
  63 `STGxxx` entries). **`classification_confidence` is split (re-censused v1.2, N74-F5):**
  **46** `heuristic_auto` (`:64`) + **17** `explicit_metadata` (`:2427`) — method
  `grep -oE '"classification_confidence": *"[a-z_]+"' | sort | uniq -c`. The seed supplies raw
  signals (`source_folder`, `method[]`, `tags[]`, producer name in folder) but no family
  assignments; `family_id` derivation is net-new. Its confidence is bounded by heuristic-auto
  classification **only for the 46 `heuristic_auto` rows**; the 17 `explicit_metadata` rows are
  not treated as heuristic (v1 wording "every sampled entry is `heuristic_auto`" was drift
  against the current file).
- **D-3 — `compute_family_id` hashes the neighbourhood exactly.** `identity.py:149-154` hashes
  `parameter_neighbourhood` as given, so family identity is exact-match on that object; §6.6
  rule 6 / §10.3 intend a *neighbourhood* (cluster), not exact equality. Reconciled by requiring
  the caller to pass a pre-bucketed spec (`test_identity.py:108` `{"period":[18,22]}` supports
  this reading), but the bucketing rule is undefined → OQ-4.
  **OWNER-CLOSED (added v1.12, W289; owner addendum 31 decision 98,
  `OWNER_DECISIONS_2026-08-29_EVENING.md:764`).** Superseded clause retained character for character:
  ~~"but the bucketing rule is undefined → OQ-4."~~ The bucketing rule is no longer
  undefined-pending-ratification — the owner refused buckets outright ("Do not invent arbitrary
  parameter buckets"), so the reconciliation above holds with the pre-bucketed spec read as the
  **approved search-space version identity**: one family per (approved search-space version,
  strategy). The exact-match behaviour of `identity.py:149-154` is unchanged; what must change is
  the caller's input, which is WP-P0-04's contract surface — OQ-4, engineering half still open.
- **D-4 — the contract does not *define or enforce* `FAM-UNKNOWN` (retitled v1.2, N74-F4;
  was "the contract cannot represent `UNKNOWN`").** `TrialRecord.family_id` is `NonEmptyStr`
  with no allowed-value set (`trials.py:22`), so it **can carry** the non-empty string
  `FAM-UNKNOWN` — exactly as §1.4 states (`FAM-UNKNOWN` satisfies `NonEmptyStr`). What the
  merged contract does **not** do is (a) define `FAM-UNKNOWN` as a distinguished literal
  (`compute_family_id` only ever returns `FAM-<hex>` — `identity.py:154`), or (b) bind it to the
  §6.6 rule 6 `LIVE_CANDIDATE` refusal. This is an **enforcement / semantic-constraint gap**,
  not a representation gap → OQ-5. The v1.1 "can neither represent nor enforce it" wording
  overstated the mismatch.
- **D-5 — no conflict, recorded for completeness.** Plan says P0-22 "Depends on WP-P0-04,
  WP-P0-13" and is "Parallel-safe with WP-P0-21" (`plan:531`); lane spec says design against
  plan text and do not read W51's in-progress P0-13 draft. No contradiction — all
  catalog-shaped choices are therefore `PROVISIONAL-ON-P013` and unverifiable now.
- **D-6 — fold note: one v1.10 patch hunk was STOPPED on an anchor mismatch, leaving one cite
  unsatisfied (added v1.10, DS66-F07).** The `DS71_P022_PATCH.md` hunk that would have extended
  **OQ-6** with the non-registry producer-confirmation gap carried its anchor at a **three-space**
  continuation indent; §6.2's OQ-6 tail (`harvested_tags` is authoritative, and how they are
  reconciled) stays open for all rows.`) is authored at **two**. The anchor therefore did not match
  byte-for-byte and the hunk was **not** hand-adjusted, per the apply contract. Consequence, stated
  rather than papered over: the §1.2 `source_provenance` text applied by the same finding says the
  gap "is folded into OQ-6", and **OQ-6 does not yet carry that fold**. OQ-6 already holds the
  canonical-producer question for all rows, so the cite is directionally right but not yet
  satisfied. Owner action: re-issue the OQ-6 extension at the correct indent, or restate the §1.2
  cite. No repository file is involved; this is a design-document fold note in the W196-F10 form.

---

## Findings count

16 open questions (named blockers) · 6 discrepancies · 0 code changes (design only). *(v1.10: OQ-16
added for the DS66-F01 window-bounds gap — the count rose because a question was opened, not
answered; OQ-1 and OQ-15 extended in scope, not added; no blocker closed. D-6 added as the fold
note for the one STOPPED hunk.)* *(v1.9: three of the then-fifteen — OQ-13, OQ-14, OQ-15 — were
narrowed by binding a duty to an existing named component; none was closed and none was added, so
the count was unchanged.)*

**v1.12 (W289 owner-fold).** Counts unchanged: **16 open questions · 6 discrepancies**. Owner
addendum 31 decisions 98-103 close the **owner half** of four blockers — OQ-4 (row 17), OQ-7 (rows
18, 19, 20), OQ-11 (row 21) and OQ-16 (row 22) — and none of the four closes outright: each keeps an
engineering or delivery residue no owner answer can carry. OQ-7 is **extended** (the cross-producer
tolerance decisions 100 and 101 leave unstated), not added; no blocker is added and none is removed.
Nothing was deleted: every closed choice is retained where it stood and restated struck through in
its added block.

**v1.1 fold:** 12 detection findings (`DETECT_P24_P022_DRAFT.md`) folded — all 12 FIXED
(3 Medium, 9 Low; 0 refuted, 0 honest-CANNOT). OQ count unchanged (OQ-7 and OQ-9 extended in
scope, not added; the clock-skew margin `δ` folded into OQ-7). Discrepancy count unchanged (D-1
downgraded to the D-5 "no conflict" form, not removed).

**v1.2 fold:** 5 detection findings (`DETECT_N74_P022_V11.md`, lane N74) folded — all 5 FIXED
(3 Medium, 2 Low; 0 refuted, 0 honest-CANNOT). **OQ-11 added** (ledger access-control + atomicity
contract, and the copy/export producer-or-prevention choice — N74-F1 / N74-F3); OQ-6 and OQ-9
extended in scope. Discrepancy count unchanged (D-4 retitled to an enforcement/semantic gap, not
removed). §3.3 positive-completeness made continuous over all `W_B`; the A-7d append-only clause
is now explicitly BLOCKED until OQ-8 + OQ-11 (was asserted as satisfied). Every A-7d falsification
row now names two independent producers. Still DESIGN ONLY; build gated on P0-13 acceptance +
re-audit (OQ-10).

**v1.3 fold:** 1 detection finding (`DETECT_G28_P022_V12.md`, lane G28) folded — G28-F01
FIXED (1 Medium; 0 refuted, 0 honest-CANNOT). The parallel Gemini census reported 0 findings.
The whole-window fail-closed consequence now governs §3.3, §5(a), `b3`, and §6.1 consistently:
any coverage gap makes the ledger incomplete for all of `W_B`, so confirmation duration is 0;
only a positively complete whole-window mutation may restore a non-zero duration. Still DESIGN
ONLY; build gated on P0-13 acceptance + re-audit (OQ-10).

**v1.4 fold:** 1 detection finding (`DETECT_N86_P022_V13.md`, lane N86) folded — N86-F01
FIXED (1 Low; 0 refuted, 0 honest-CANNOT). The required runnable-now shape census found the same
defect in `b4`; `b1` and `b4` now split their primary designable-now arm from the mandatory
complete-window mutation blocked on OQ-9, and the unqualified runnable-now set is empty. Still
DESIGN ONLY; build gated on P0-13 acceptance + re-audit (OQ-10).

**v1.5 fold:** 1 detection finding (`DETECT_N96_P022_V14.md`, lane N96) folded — N96-F01
FIXED (1 Low; 0 refuted, 0 honest-CANNOT). The retained literal v1.3→v1.4 unified diff is now
cited as the evidence for the v1.4 minimality statement (`W109_RUN.log:7044-7136`). The shape
sweep found no inconsistent repetition or count. Open-question and discrepancy counts are
unchanged. Still DESIGN ONLY; build gated on P0-13 acceptance + re-audit (OQ-10).

**v1.6 fold:** 6 detection findings (`DETECT_N99_P022_V15.md`, lane N99) folded — all 6 FIXED
(5 Medium, 1 Low; 0 refuted, 0 honest-CANNOT). The clock-skew mutation now crosses the actual
`t2 + δ` boundary and stays blocked on OQ-7; §5(c) stays blocked until whole-window completeness
exists; lineage producers are conflict-checked before precedence; completeness is identity-bound;
one AND predicate governs OQ-9/OQ-11; and the downstream row now measures only the named
family/confirmation precondition with independent producers and a truth-side mutation. The full
repeat/count sweep found no stale current-version or corrected-design claim. Open-question and
discrepancy counts are unchanged.
Still DESIGN ONLY; build gated on P0-13 acceptance + re-audit (OQ-10).

**v1.7 fold:** 3 detection findings (`DETECT_G67_P022_V16.md`, lane G67) folded — all 3 FOLDED
(2 Medium, 1 Low; 0 disputed). `COMPLETENESS-UNBLOCK` now includes OQ-8's exact-head-anchor duty;
the row-hash preimage binds every declared observation field while its uninvented canonical byte
encoding is `[OPEN]` as OQ-12; and §6.1 labels the non-goals row as inspection-only instead of
claiming it has two-producer falsification. Open questions are 12; discrepancies remain 5.
Still DESIGN ONLY; build gated on P0-13 acceptance + re-audit (OQ-10).

**v1.8 fold (record corrected v1.9, W196-F01):** 7 census findings (`DS47-F01` through `DS47-F07`,
repair patch `DS48_P022_PATCH.md`) processed — **all 7 APPLIED** (4 Medium, 3 Low; 0 disputed).
DS47-F03 Patch A was stopped inside the W193 lane and then applied by hand with the two-space
continuation indent restored; it is in the body at §5(a)'s Producer-2 clause. Superseded v1.8
wording, retained: ~~"6 fully APPLIED; DS47-F03 is PARTIAL because Patch A was STOPPED on a
non-verbatim preimage while Patches B–D applied"~~. OQ-13, OQ-14, and OQ-15 are new named blockers;
OQ-3 and OQ-7 are extended without closing any pre-existing open question. Open questions are 15;
discrepancies remain 5. Still DESIGN ONLY; build gated on P0-13 acceptance + re-audit (OQ-10).

**v1.9 fold:** 10 verification findings (`DETECT_W196_P022.md`, lane W196 — 0 High, 6 Medium,
4 Low) folded — all 10 REPAIRED; 0 disputed. The v1.8 record is corrected against the body
(W196-F01). Three blockers opened in v1.8 are **narrowed, not closed**, by binding the duty an
existing named component can carry: OQ-15's uniqueness duty to the single serialising appender
(W196-F02), OQ-13's marking-row integrity duty to the §3.2/§4.2 recompute (W196-F03), and OQ-14's
contamination-detection duty to the chain-bound `family_id` cross-check (W196-F04). Each of the
three keeps the part no existing component can carry — composition and generator for OQ-15, schema
and store for OQ-13, graph-store enforcement / head anchor / chain binding for OQ-14 — so **open
questions remain 15**: none closed, none added. The §6.1 enumeration row is narrowed back to the
clause it maps (W196-F05); the five untagged defect sites now carry their blocker pointers
(W196-F06); `observed_at` is relabelled to what it now decides (W196-F07); OQ-7 states the
Producer-2 timestamp-independence assumption the DS47-F02 check rests on (W196-F08); the three
untagged v1.8 body repairs carry version/finding tags (W196-F09); and the cross-artifact cite drift
caused by the hand-applied edit is recorded as a fold note (W196-F10). No superseded text was
deleted; every replaced sentence is retained and struck through in place. Discrepancies remain 5.
Still DESIGN ONLY; build gated on P0-13 acceptance + re-audit (OQ-10).

**v1.10 fold:** 8 census findings (`DS66_RUN.log`, lane DS66 — **1 High**, 3 Medium, 4 Low) folded
via `DS71_P022_PATCH.md` — 7 applied, **1 hunk STOPPED** on a byte-for-byte anchor mismatch
(DS66-F07's OQ-6 extension; D-6). The High is **not** closed and was **not** repaired by a sentence.
DS66-F01 found that `window_start`/`window_end` are the producer's own self-report with no named
check binding the recorded slice to what was shown; adding prose asserting the binding holds would
have restated the defect as its own fix. No such component exists in the in-fence sources — §5(a)
Probe 1 reconciles Producer 2 against Producer 1 on read identity and timestamp only, never on
window bounds — so the claim is **withdrawn at its site** to what the document actually enforces,
with the superseded wording retained struck through, and the gap opened as **OQ-16**. Two further
claims are withdrawn rather than shored up: the `untouched` planted-value "refusal", which was
mis-attributed to OQ-5 and is in fact inert because nothing reads it (DS66-F04, both sites), and
`observed_at`'s "monotonic per writer sequence", which has neither verifier nor consumer
(DS66-F06). Two overstatements are brought back to the document's own blocked list: §1.5's "what
*is* checked today" now reads "designed but not live today", inheriting OQ-12 + OQ-8 (DS66-F05).
The §4.2 marking-integrity guard is stated to be the **permanently-firing** case, not decoration —
gates do consume markings (§6.1 row 7) and "Additive only" growth made every as-appended marking
mismatch a later recompute — and its referent is rebound to the append-time recompute §4.1 already
writes, so it discriminates (DS66-F03). Two unnamed identities get named questions in the
document's own form and **no invented bytes**: `package_hash`'s preimage and producer folded into
OQ-1 (DS66-F02), `observer_identity`'s composition folded into OQ-15 (DS66-F08). No superseded text
was deleted; every replaced sentence is retained and struck through in place. **Open questions rise
15 → 16** and **discrepancies rise 5 → 6** — both because something was opened, not answered. Still
DESIGN ONLY; build gated on P0-13 acceptance + re-audit (OQ-10).

**v1.12 fold:** the owner's Phase-0 answers to rows 17-22, recorded as **owner addendum 31**
decisions 98-103 (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:764-769`),
folded retain-and-tag. Decision 98 refuses parameter bucketing and makes one approved search-space
version, for one strategy, one family (OQ-4, §1.2, D-3); decision 99 accepts fail-closed over-marking
and adds no provenance machinery (OQ-7); decision 100 mandates one shared UTC clock, so `δ = 0`
(OQ-7, §4.1, §5(a), §5(c)); decision 101 requires an independent clock for the access logs (OQ-7,
§5(a)); decision 102 chooses the prevention boundary for the copy/export residual and requires its
cost recorded — recorded as `COST: UNPRICED - owner requires it recorded; no sourced figure exists`
(OQ-11); decision 103 refuses withdrawing the window control and requires the displayed window bound
to the recorded one, leaving OQ-16 `OWNER-ANSWERED-SHAPE, VALUE PENDING` and BLOCKED. No blocker is
closed outright, no number, identity or byte tuple is invented, and every engineering half stays open
with its owner named. Open questions remain **16**, discrepancies **6**. **Zero lines deleted:** no
pre-existing line was edited or removed by this fold. Still DESIGN ONLY; build gated on P0-13
acceptance + re-audit (OQ-10).
