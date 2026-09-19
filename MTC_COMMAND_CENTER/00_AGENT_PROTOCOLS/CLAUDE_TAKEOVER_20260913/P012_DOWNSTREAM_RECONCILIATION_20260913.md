# Downstream dependency reconciliation — RECORDED 2026-09-13 for the WP-P0-12 scope amendment (OD-20260913-P012-SCOPE-1)

**Role and standing.** Independent drafting analyst (`claude-opus-5`, xhigh). NOT a reviewer, NOT an
acceptor, NOT the Lead. **Nothing in this file unblocks anything, accepts anything, or grants any
authority.** Every citation below must be audited by the Lead before use. Read-only analysis only;
no Git write, no network, no execution of the P020 acceptance checker (it documents no read-only
mode, so it was read, not run).

Prepared: 2026-09-13. Lane directory: `C:/tmp/CLAUDE_P0_RUN_20260913/laneP12D_downstream`.

**Owner instruction being reconciled** (verbatim excerpt as supplied in the lane brief,
`BRIEF.md:7`):

> I approve narrowing WP-P0-12's current acceptance scope to its reviewed research/engineering
> deliverable. [...] Report completion as "P0-12 research/engineering scope complete; production
> admission pending." Reconcile downstream dependencies individually; do not automatically unblock
> production-dependent work.

---

## 1. Definitions — two distinct P012 states

The amendment distinguishes two states. They are not two grades of the same thing: the first is a
claim about source, tests and reviews; the second is a claim about authentic external facts. The
quoted sources below define each.

### 1.1 State (i) — "research/engineering scope complete"

Per the lane brief this means: **fixed G5 reviewed and formally Section-16 accepted, owner-ratified,
synthetic/local-consistency only.** It decomposes into the components below.

**(a) A fixed candidate identity.**

> Candidate G5: 6d6a450232c81c4c13d63c9a4e06ce3b1bf4f889.
> Core: 4698e71659d678f50e549e328e78d25816fa16fe.
> Clean and unchanged. Repair counter remains 5; no new product repair or commit was needed during
> this continuation.

— `C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:13-15`

> Owned worktree C:/tmp/P012_PATHD_20260912; branch feature/p012-path-d-20260912; clean
> HEAD6d6a450232c81c4c13d63c9a4e06ce3b1bf4f889; core4698e71659d678f50e549e328e78d25816fa16fe.

— `C:/tmp/CLAUDE_TAKEOVER_20260913/P012_HANDOFF.md:7` (the missing spaces are present in the source
and are reproduced verbatim)

The frozen source packet and its manifests:

> Actual G5: `6d6a450232c81c4c13d63c9a4e06ce3b1bf4f889`; core tree:
> `4698e71659d678f50e549e328e78d25816fa16fe`. The source is frozen at
> `C:/tmp/P012_LEAD_20260912/FINAL_R5/FREEZE_MANIFEST.json` (SHA-256
> `3dcf03be6c3b801a3f43840d064ac45be3689fe5bd35bde428e142b3c4297567`) with hash manifest
> `C:/tmp/P012_LEAD_20260912/FINAL_R5/SHA256_MANIFEST.json` (SHA-256
> `eb403b73b01c4b72b8aad380874ec2c47a747646af8c51cf7f81fe5ec9c2d283`).

— `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:13`

**(b) Engineering complete, with the exact flagship engineering review roles accepted.**

> The authorized engineering, exact flagship reviews, bounded Gemini corroboration, and
> final-ratification preparation are complete. Full package/production acceptance is NOT granted.

— `C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:3`

> ACCEPTED: Exact Sol and Opus engineering review roles; bounded Gemini product-delta corroboration
> only.
> BLOCKED: Formal Section16/R29, owner ratification, authentic real-account admission, funding M,
> experienced-human money gate, and CI/integration.

— `C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:10-11`

> Engineering complete at unchanged G5, repair counter5 retained. Exact gpt-5.6-sol xhigh PASS;
> claude-opus-5 xhigh PASS-WITH-NITS accepted for engineering; three bounded gemini-3.7-flash-high
> product-delta corroborations PASS. No required engineering repair currently established.

— `C:/tmp/CLAUDE_TAKEOVER_20260913/P012_HANDOFF.md:15`

**(c) Formal Section-16 acceptance — NOT YET PRESENT.**

> Gemini REPORTS Items1/4 ACCEPTED_WITH_RESIDUAL_RISK, successorUNCHANGED, overallPARTIAL_REVIEW_ONLY
> and required_scope_unread[]. Lead does NOT accept that as completed formal review. Full
> substantive adjudication is PENDING for Claude; only executive/coverage/terminal sections and
> concrete native read gaps have been checked.

— `C:/tmp/CLAUDE_TAKEOVER_20260913/P012_HANDOFF.md:29`

> **Lead checkpoint is NONACCEPTING_REQUIRED_READ_GAPS**, despite the reviewer's favorable Items1/4
> claims. [...] Item1 is not accepted; Item4 substantive reconciliation remains. [...] B1/B2/B3/C
> prompts are prepared but never launched. No ratification has occurred.

— `C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md:22`

Reviewer eligibility for that formal act is constrained:

> Section16/R29 reviewer must be neither Codex nor Claude and independent of kernel implementer and
> contract-tables author; the experienced-human money gate is separate.

— `C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:33`

> Formal Section16 reviewer MUST be Gemini3.8, neither Codex nor Claude. Gemini3.7 is T0
> corroboration, a different role. [...] Claude takeover does not make Claude an eligible Section16
> signer.

— `C:/tmp/CLAUDE_TAKEOVER_20260913/P012_HANDOFF.md:53`

**(d) Owner ratification — NOT YET PRESENT.** Eight drafts exist and are unapplied; the ratified
chain is short of the proposed chain:

> Current JSON chain: 33 entries through #35. Current Markdown: 28 through #30. Proposed chain: 37
> through #39; builder seals 36–39 remain UNRATIFIED.

— `C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:33`

> Eight unapplied drafts in RATIFICATION_R6 under that Lead root. JSON chain33entries through35,
> Markdown28through30; proposed37entries through39. Seals36–39 remain UNRATIFIED. No schema patches
> or accepting semantic receipt were applied this turn.

— `C:/tmp/CLAUDE_TAKEOVER_20260913/P012_HANDOFF.md:19`

**(e) Synthetic / local-consistency only — the explicit epistemic ceiling of state (i).**

> Status: SOURCE-FROZEN, PRE-REVIEW, SOURCE-ONLY, SYNTHETIC / LOCAL-CONSISTENCY SCOPE, NONACCEPTING.
> This external documentation adaptation records verified existing R5 evidence only. It authorizes
> no paper operation, production or paper-account admission, runtime activation, order, venue
> contact, credentials, host access, spend, outreach, deployment, integration, push, PR, or merge.

— `.../RESEARCH_PAPER_SCOPE_PROPOSAL.md:3`

> Label synthetic results `SYNTHETIC_TEST_ONLY`, byte/hash agreement `LOCAL_CONSISTENCY_ONLY`, and
> unsupported monetary or behavioral risks `UNQUANTIFIED`.

— `.../RESEARCH_PAPER_SCOPE_PROPOSAL.md:23`

> These materials can show deterministic parsing, literal binding, refusal, estimator separation,
> and offline construction. They cannot authenticate venue origin, account ownership, completeness,
> native order association, upstream production, liquidity, fills, strategy performance, profit,
> adverse-cost robustness, extreme funding, or readiness.

— `.../RESEARCH_PAPER_SCOPE_PROPOSAL.md:28`

**(f) The plan's own stated acceptance gate for WP-P0-12 is engineering-only.** This matters for the
amendment, because the plan's gate text contains no production-evidence clause at all:

> - **Acceptance gate:** **no undocumented behavioural difference exists between P0-11 and P0-12.**
>   Phase 0 is not complete without this.

— `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:406`

**Consequence for this draft.** Two of state (i)'s components — formal Section-16 acceptance and
owner ratification — are recorded as **not achieved** as of 2026-09-13. State (i) is therefore a
**prospective** state in this draft, not a current one. Every "state (i) would satisfy" statement in
section 4 is conditional on those two acts actually occurring and being independently verified.
Nothing here asserts that state (i) has been reached.

### 1.2 State (ii) — "production admission"

> Full production still has ten OPEN requirements and 27 retained signed risks. Authentic N=3 native
> BTC maker/taker/near-$10 fill observations need origin, ownership, order association and
> completeness. FEES applies from first authenticated fill; funding needs a separately complete
> forward interval no earlier than 2026-09-12T11:00Z and still-unset M. A human money gate remains.
> Owner's research assumptions do not become verified exchange facts or permission to ARM/trade.
> Code/synthetic arithmetic can finish while real evidence remains open.

— `C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md:25`

> Preserve signed OPEN01/03/05/07, all 10 production OPEN rows and 27 risks. N=3 authentic
> own-account native-BTC maker/taker/near-$10 fills, origin/ownership/order association/completeness,
> first-authenticated-fill FEES interval, distinct complete funding interval starting at or after
> 2026-09-12T11:00Z, and separate funding-M decision remain external requirements.

— `C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:33`

> Signature boundary2026-09-12T11:00Z. Keep forward-only own-account funding, whole-interval refusal
> on any gap, funding M pending after observations. Reported per-fill fee cash; schedule estimator
> comparison-only with5%relative tolerance; first authenticated fill is the distinct fee interval
> start; liquidation remains CANNOT_MAP. [...] N3 authentic nativeBTC maker/taker/near-$10 fills
> remain required. Preserve OPEN01/03/05/07, all10productionOPEN rows and27risks, authentic
> origin/ownership/order association/completeness and separate human money gate.

— `C:/tmp/CLAUDE_TAKEOVER_20260913/P012_HANDOFF.md:11`

> Actual production admission still requires independent origin/account evidence and all remaining
> acceptance gates. Local consistency cannot authenticate origin.

— `.../RESEARCH_PAPER_SCOPE_PROPOSAL.md:20`

> Treat funding as forward-only venue-reported cash for one complete declared whole interval
> beginning at or after `2026-09-12T11:00:00Z`. FEES begin only at the distinct first authenticated
> fill. Never independently revalue funding, infer an oracle value, substitute a context rate,
> back-calculate, or merge the two time boundaries.

— `.../RESEARCH_PAPER_SCOPE_PROPOSAL.md:22`

> OPEN01/03/05/07, all 10 production OPEN rows, all 27 signed risks, funding M, N=3
> maker/taker/near-$10 observations, and the forward-only account/product/whole-interval declaration
> remain pending. No owner choice is reopened.

— `.../RESEARCH_PAPER_SCOPE_PROPOSAL.md:30`

The binding governance anchor that already separates the two states, recorded before this amendment:

> **This ratifies a re-seal only.** It is not WP-P0-12 acceptance: production Item 4 remains
> `NONE_KEEP_REFUSED`, all ten Section-19 rows remain OPEN and `APPLICABLE`, the
> `P012_SYNTHETIC_ONLY_NON_PRODUCTION_MILESTONE_V1` bound still holds, and no capture, account read,
> deployment, runtime, broker or trading authority follows.

— `C:/CT13/DECISIONS.md:22` (OD-20260908-1)

And the standing downstream notice from the P012 side — the text every downstream package currently
holds:

> Read-only engineering evidence and unapplied ratification drafts may be reviewed. No accepted P012
> dependency B01 or production cost admission is available to P020. Typed TIME_LIMIT is also
> unavailable; it is not the sole cause of compatibility gating and adds no P020 scope. Signed
> choices, all ten production OPEN rows, 27 risks, N=3, and funding M remain preserved.

— `C:/tmp/P012_LEAD_20260912/DOWNSTREAM_NOTICE.md:13`

> P020 may consume engineering evidence and drafts only. No accepted B01 or production-cost
> admission exists. P020's newly owner-authorized benchmark/TIME_LIMIT work is separately owned and
> grants no P012 scope or acceptance.

— `C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:35`

> ## P020 boundary
>
> P020 has no accepted P012 dependency B01 or production cost admission. The typed TIME_LIMIT
> artifact is also unavailable; this adds no P020 implementation scope. Compatibility, required
> reviews, real admission, owner ratification, protected CI, and integration remain separate gates.

— `.../RESEARCH_PAPER_SCOPE_PROPOSAL.md:38-40`

### 1.3 What the two definitions do not settle

- No source read for this draft states that state (i) **is** "WP-P0-12 acceptance" for the purposes
  of any particular downstream package's dependency line. The amendment redefines a label; it does
  not edit any downstream gate text. Every row below is therefore evaluated against its own quoted
  wording, with **NO** as the default.
- No source read for this draft contains a mapping from "P0-12 accepted" to a specific downstream
  release action. See NOT VERIFIED item **NV-03**.

---

## 2. Per-package reconciliation tables

Column meanings, fixed for every table below:

- **Gate/criterion id** — the identifier as it exists in the cited source. No id is invented; where a
  source has no id, the row is labelled by its quoted heading and marked `(no id in source)`.
- **Verbatim requirement + citation** — quoted source text with `file:line`.
- **Depends on state** — `(i)`, `(ii)`, `both`, `neither` (the quoted text names no P012 state), or
  `UNKNOWN`.
- **Satisfied by state (i) alone?** — default **NO**. `YES` appears only where the quoted text itself
  is met by engineering acceptance.
- **Remaining follow-up + owner** — what is still required and who owns it.
- **Notes** — verification caveats and cross-source conflicts.

### 2.1 WP-P0-20 — successor / canonical-path migration and shared allocator

Source of record for the criteria: `C:/P020_IMPL_20260912/check_p020_acceptance.py` (read, not
executed). Current reported result:

> Acceptance remains intentional exit 1: 8/16 criteria MET / `NOT ACCEPTABLE`.

— `C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:30`

The eight named blockers, verbatim:

> The live reporter still blocks exactly:
>
> 1. `cost_admission`
> 2. `p012_full_acceptance`
> 3. `frozen_probe_compatibility` (two known failures)
> 4. `production_admission`
> 5. `real_before_after`
> 6. `dependent_disposition`
> 7. `real_benchmark`
> 8. `independent_reviews` (external evidence is not self-certifiable by the reporter)

— `C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:40-49`

#### 2.1.1 The eight currently-MET criteria — none names a P012 state

| Gate/criterion id | Verbatim requirement + citation | Depends on state (i), (ii), or both | Satisfied by state (i) alone? | Remaining follow-up + owner | Notes |
|---|---|---|---|---|---|
| `checklists` | "legacy checklist plus additive research vocabulary" — `check_p020_acceptance.py:659`; probe text "legacy v1 digest preserved (...); additive ... pinned" — `:63-67` | neither | Not applicable — clause names no P012 state | None from P012; P020 Lead retains the pin | Reported MET. Unaffected by the amendment in either direction. |
| `battery_definition` | "statistical-battery definition remains pinned" — `:660`; probe text "definition v1 pinned" — `:74` | neither | Not applicable | None from P012; P020 Lead | Reported MET. |
| `verified_execution_join` | "actual E/X/V/M carrier is computed" — `:661`; UNMET alternative "E/X/V/M carrier is empty or self-asserted" — `:101` | neither | Not applicable | None from P012; P020 Lead | Reported MET. Evidence is the synthetic canonical slice; `:108` refuses a proof that "unexpectedly covered every required control". |
| `d026_uncomputed` | "name-only coverage refuses and REQUIRED gaps block" — `:662`; UNMET alternative "a caller-authored full-coverage name list promoted" — `:131` | neither | Not applicable | None from P012; P020 Lead | Reported MET. |
| `standin_prohibition` | "stand-ins never become acceptance evidence" — `:663`; UNMET alternative "stand-in facts became acceptance-bearing" — `:207` | neither | Not applicable | None from P012; P020 Lead | Reported MET. Plan text withdrawing `ALLOCATOR_NOT_YET_SHARED` as an accepting state: plan `:499`. |
| `allocator_execution_identity` | "canonical allocator object is imported and executed" — `:664`; MET text "canonical allocator object executed exactly once for one actual successor OPEN" — `:157` | neither | Not applicable | None from P012; P020 Lead | Reported MET. Plan gate A-7b requires import identity "proven by import, not asserted" — plan `:509`. |
| `successor_components` | "successor, portfolio and canonical export execute" — `:665` | neither | Not applicable | None from P012; P020 Lead | Reported MET. Resolves semantics id `2.1.0` (`:165`); see §2.1.3(2) for the `2.1.0` divergence from the P012 frozen registry. |
| `required_control_coverage` | "all enabled REQUIRED children need X-and-V" — `:667`; MET text "all enabled REQUIRED controls of the frozen suite configuration are X-and-V covered across ... mutually exclusive fixtures" — `:586-591` | neither | Not applicable | None from P012; P020 Lead + T0 roster for any acceptance use | Reported MET at 17/17 enabled REQUIRED controls, while "the canonical single run still reports nine gaps" — `P020_HANDOFF.md:31`. |

#### 2.1.2 The eight blocked criteria

| Gate/criterion id | Verbatim requirement + citation | Depends on state (i), (ii), or both | Satisfied by state (i) alone? | Remaining follow-up + owner | Notes |
|---|---|---|---|---|---|
| `cost_admission` | "record identity is not P012 cost admission" — `check_p020_acceptance.py:666`. BLOCKED detail: "real positive record-index lookup succeeded, then remained non-accepting: {P012_ADMISSION_REQUIRED}; {NON_AUTHORITATIVE_INDEX}" — `:253-256` | **(ii)** for the `P012_ADMISSION_REQUIRED` half; P020-internal for `NON_AUTHORITATIVE_INDEX` | **NO** | (a) authentic P012 production cost admission — owner + P012 Lead + external evidence; (b) an authoritative, non-synthetic cost record index — P020 Lead | Two independent refusals, only one of which is a P012 matter. The compatibility receipt records the same pair: "the labelled positive record-index lookup succeeds, then remains non-accepting with `P012_ADMISSION_REQUIRED` and `NON_AUTHORITATIVE_INDEX`" — `C:/tmp/P020_LEAD_20260912/p012_compat/P012_P020_COMPATIBILITY_PREP.md:53`. |
| `p012_full_acceptance` | "applicable P012 admission remains prerequisite" — `:668`. BLOCKED detail: "P012 full production admission is not supplied by this research lane; the live cost gate above returns P012_ADMISSION_REQUIRED" — `:594-598` | **(ii)** — the probe text says "full production admission" | **NO** | Authentic own-account admission per §1.2 — owner + P012 Lead. Any change to what this row asserts is a **P020 source change** owned by the P020 Lead, not a P012 reconciliation. | The probe body is an unconditional `return BLOCKED` (`:595`). Narrowing P012's acceptance label cannot alter this row's output; only editing `check_p020_acceptance.py` would, and that is a P020-owned acceptance-surface edit requiring its own authority and review. |
| `frozen_probe_compatibility` | "full frozen probes must be compatible" — `:669`. BLOCKED detail: "the disclosed full frozen-probe compatibility state has 2 known failures caused by additive core changes; this scoped suite does not edit or waive those probes" — `:601-606` | **UNKNOWN** | **NO (UNKNOWN)** | Name the two probes first; only then can ownership and state-dependence be assigned — P020 Lead | Names are undisclosed by the source: "It does not disclose the individual probe names, so they remain UNKNOWN here and are not inferred" — `P012_P020_COMPATIBILITY_PREP.md:52`; classification "Two disclosed frozen-probe failures: INCOMPATIBLE; individual names: UNKNOWN" — `:66`; and "Individual failure names were not disclosed." — `C:/tmp/P020_LEAD_20260912/P20P012_COMPAT_FINAL.md:13`. The P013 adoption map calls them "two disclosed P012 probe failures" — `C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md:30` — a stronger attribution than the checker text supports. See **NV-01** and §5 **D-2**. |
| `production_admission` | "research success never admits production" — `:670`. BLOCKED detail: "actual production-labelled profile refuses; no production admission" — `:628`; UNMET alternative "production-labelled profile executed" — `:630` | **(ii)** | **NO** | Nothing from P012 satisfies it as written; the row is a refusal proof, not an admission path — P020 Lead owns the row's semantics; owner + external evidence own admission itself | Structural: the probe returns BLOCKED **when the refusal works correctly** and UNMET when it does not. It has no MET branch. Reaching MET would require inverting the row's meaning. The refusal constant checked is `REFUSED_P020_PROVENANCE_NOT_EXECUTABLE` (`:627`). |
| `real_before_after` | "real frozen-candidate before/after evidence" — `:671`. BLOCKED detail: "no independently verified before/after run on a real frozen candidate" — `:633-634`. Plan output: "a before/after comparison on at least one real frozen candidate, showing where the economics changed and why" — plan `:504` | **(i)** as the migrated-kernel input; the comparison itself is P020-owned work | **NO** | Perform the canonical-path migration, produce the before/after on a real frozen candidate, and have it independently verified — P020 Lead + T0 roster | The disposition record ties the precondition to source arrival, not acceptance: "none can be until the canonical path is migrated, and that waits on `WP-P0-12` reaching this repository" — `C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_20_DEPENDENT_TOOL_DISPOSITION.md:55-57`. Compare `C:/CT13/DECISIONS.md:10`. See §5 **D-1**. |
| `dependent_disposition` | "dependent consumers require audited disposition" — `:672`. BLOCKED detail: "consumer code is being migrated separately, but no independent per-consumer disposition audit is complete; source text or a PERFORMED label is not proof" — `:637-642` | **(i)** as the migrated-kernel input; the audit is P020-owned | **NO** | Complete the migration and an independent per-consumer disposition audit — P020 Lead + independent auditor | Disposition file: "**Status: PROPOSED, not PERFORMED.**" — `WP_P0_20_DEPENDENT_TOOL_DISPOSITION.md:3`; and "`check_p020_acceptance.py`'s `dependent_disposition` criterion therefore remains `BLOCKED`, and nothing in this section changes that." — `:111-112`. Bounded probes exist but are labelled "EVIDENCED BY BOUNDED EXECUTED PROBES; not migration-PERFORMED and not accepted." — `:69`. |
| `real_benchmark` | "real workload benchmark and feasibility" — `:673`. BLOCKED detail: "only bounded synthetic execution is in scope; no real frozen workload benchmark, O-28 extrapolation or feasibility decision was run" — `:644-649`. Plan gate adds "a **measured full-kernel trials-per-hour figure on named reference hardware**, the **extrapolated wall-clock for an O-28-scale (100,000-trial) sweep under the funnel**, and an explicit **feasible/infeasible statement**" — plan `:510` | **neither** | **NO** | Execute the newly authorized preregistered benchmark profile-selection procedure, then the bounded measurement — P020 Lead, within the bounds at `P020_HANDOFF.md:58-70` | Owner authorized the selection procedure on 2026-09-13 but it is "APPROVED BUT NOT STARTED" — `P020_HANDOFF.md:21`; the same approval is recorded at `C:/CT13/DECISIONS.md:79`. No P012 state is named by this criterion. |
| `independent_reviews` | "mandatory reviews and Lead acceptance" — `:674`. BLOCKED detail: "required independent audits, economic Opus counterpart review, Gemini corroboration and Lead acceptance are external and not self-certifiable" — `:651-656` | **neither** | **NO** | Fresh exact T0 roster plus Lead acceptance at the frozen P020 identity — P020 Lead + T0 roster (exact `claude-opus-5` xhigh + exact `gpt-5.6-sol` xhigh + required `gemini-3.7-flash-high` corroboration, per `P020_HANDOFF.md:113`) | No P012 state is named. The branch separately needs "later current-master reconciliation, required Bridge CI on an up-to-date head, PR review and explicit push/PR/merge authority" — `P020_HANDOFF.md:51`. |

#### 2.1.3 Two structural observations about the P020 reporter (source-derived)

**(1) Eight of the sixteen criteria have no MET branch in the current source.** Read directly from
`check_p020_acceptance.py`:

- Unconditional `return BLOCKED`: `probe_p012_full_acceptance` (`:594-598`),
  `probe_frozen_probe_compatibility` (`:601-606`), `probe_real_before_after` (`:633-634`),
  `probe_dependent_disposition` (`:637-642`), `probe_real_benchmark` (`:644-649`), `probe_reviews`
  (`:651-656`).
- `BLOCKED` on the success path and `UNMET` otherwise, with no `MET` return:
  `probe_cost_admission` (`:239-256`), `probe_production_admission` (`:608-630`).

`8/16 MET` is therefore the structural ceiling of the reporter as written, and **no change of P012
state — (i) or (ii) — can move the printed count.** Any movement requires an edit to
`check_p020_acceptance.py`, which is a P020-owned acceptance-surface change with its own authority
and review requirements. The module's own closing line keeps the same separation:

> Mechanical rows are MET, but package acceptance remains a separate Lead act.

— `check_p020_acceptance.py:704`

**(2) The current P020 branch has diverged from the P012 frozen core in ways the receipt calls
INCOMPATIBLE.** These are interface facts independent of either P012 state:

> - The current P020 `instrument.py` no longer carries the P012 candidate's
>   `minimum_quantity_provenance`, owner-guard accessor, or venue-fact refusal seam. This is
>   INCOMPATIBLE with the P012 candidate's Path-D instrument interface if those members are consumed.
> - The current P020 `economics.py` no longer carries the P012 candidate's `ReportedFillFee`,
>   `reported_fill_fees`, and related admitted-fee refusal surface. This is INCOMPATIBLE with the
>   P012 candidate's Path-D cost/fill interface if those members are consumed.

— `C:/tmp/P020_LEAD_20260912/p012_compat/P012_P020_COMPATIBILITY_PREP.md:42-43`

> - Current P020 semantics registry exact equality: INCOMPATIBLE (additive `2.1.0`); old-ID lookup:
>   COMPATIBLE_SYNTHETIC.

— `P012_P020_COMPATIBILITY_PREP.md:65`

Against the **frozen** core tree the same receipt records full identity:

> After normalizing the P012 core prefix away, the frozen P012 core and requested P020 core contain
> 145 identical files: 17 Python files plus 128 economic-record JSON/sidecar files. The byte hashes
> matched for every common file; there were zero missing and zero differing files.

— `P012_P020_COMPATIBILITY_PREP.md:15`

> - Frozen P012 core and requested P020 core are byte-identical synthetic surfaces.
> - Current P020 has later interface changes and two disclosed frozen-probe failures.

— `C:/tmp/P020_LEAD_20260912/P20P012_COMPAT_FINAL.md:10-11`

A state-(i) hand-off of G5 would therefore have to state **which** P012 core tree the consumer binds
to. The receipt's frozen comparison used P012 candidate commit
`e2fd210411287802676c43ddc66afa7a23c75313` with core subtree
`63f804d945d3a7692aca1bc7eee410d9ae87977e`
(`C:/tmp/P020_LEAD_20260912/p012_compat/P012_P020_COMPATIBILITY.json:7,13`), whereas the current G5
core tree is `4698e71659d678f50e549e328e78d25816fa16fe`
(`FINAL_HANDOFF_20260913.md:14`). Different identities; see §5 **D-3**.

### 2.2 WP-P0-13 — `TrialRecord` contract and trial-catalog writer

P013's plan dependency list does **not** name WP-P0-12 directly. Its P0-12 relationship is
transitive through WP-P0-20:

> - **Depends on:** WP-P0-04, WP-P0-08, **WP-P0-20**. · **Parallel-safe with:** Lane 4, Lane 6.

— plan `:413`

> **Corrected in the R1 correction pass: P0-13 additionally waits on P0-20**, so the catalog is
> written against the migrated canonical engine and the one shared allocator, and **P0-14 inherits
> that dependency transitively**.

— plan `:254`

| Gate/criterion id | Verbatim requirement + citation | Depends on state (i), (ii), or both | Satisfied by state (i) alone? | Remaining follow-up + owner | Notes |
|---|---|---|---|---|---|
| `B-01` | "No accepted P020 package and no frozen acceptance-bearing canonical-path receipt issuer/shape. P020 research commit `556639f59122e33b664ab918a4241eb96680219b` is clean/frozen at `8/16 MET` and explicitly `NOT ACCEPTABLE`; required reviews and material gates remain open." — `C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:30`. Decision row: "Package acceptance and P020 contract-owner act. Owner signature does not substitute for acceptance." — `:35` | **both**, transitively: B-01 requires P020 **package** acceptance, and two of P020's blocked criteria are state-(ii) rows (`cost_admission`, `p012_full_acceptance`) | **NO** | P020 package acceptance at an exact accepted head, publication of `P020AcceptedCatalogueDependencyV1` and the canonical-path receipt issuer/verifier, then the P013 B-01 re-audit — P020 Lead (bundle), P013 Lead (re-audit) | "B-01 cannot be signed closed; it waits for actual P020 acceptance." — `:208`. "P020 acceptance is not an owner checkbox." — `:225`. |
| `B-01` (adoption-map form; same id) | "The narrower WP-P0-20 research milestone does **not** satisfy P013 blocker B-01. B-01 requires both accepted WP-P0-20 artifacts and a settled, acceptance-bearing canonical-path receipt issuer/shape followed by a P013 design re-audit." — `P013_DEPENDENCY_ADOPTION_MAP.md:7` | **both**, transitively | **NO** | Same as above | The same source pre-emptively refuses the milestone-substitution argument: "Reinterpreting it as component readiness would silently lower the gate and would let a nonaccepted producer mint full-kernel lineage." — `:35`. This is the closest existing source statement to the question the amendment raises. |
| `B-05`/`B-08` lineage vocabulary — `FULL_KERNEL_SIMULATION` | "The second is emitted only after P013 independently verifies an opaque `P020VerifiedCanonicalPathResult` after B-01 and mints its own non-public capability." — `P013_CONTRACT_DECISION_PACKET_V2.md:119`. Decision row: "Joint contract-owner act. Full value remains unavailable until P020 accepts." — `:123` | **both**, transitively via B-01 | **NO** | B-01 closure first; then joint WP-P0-04/P020 contract-owner act — P013 Lead + WP-P0-04 owner + P020 Lead | Adoption map: "`FULL_KERNEL_SIMULATION` must remain unreachable" — `P013_DEPENDENCY_ADOPTION_MAP.md:27`. |
| `B-06` rejection taxonomy | "P020 publishes `TrialRejectionTaxonomyV1(policy_version, entries)` ..." — `P013_CONTRACT_DECISION_PACKET_V2.md:130`. Decision row: "Shape is engineering-resolvable; actual entries freeze with P020 acceptance." — `:134` | **both**, transitively via P020 acceptance | **NO** for the entries; the **shape** is separately described as "engineering-resolvable" and is not P012-dependent | Publish the accepted taxonomy values — P020 Lead; validate at boundary — P013 | "B-06 values wait for P020's accepted taxonomy." — `:208`. |
| `B-03`, `B-04`, `B-12`, `B-17`, `B-09`/`D-04`, `D-05` | Owner checklist at `:200-206`; e.g. "B-04: `ParamHashPreimageV1` exact two-member recipe and literal `\"1\"`." — `:201` | **neither** | Not applicable — these name WP-P0-04 / reader-contract-owner ratification, not any P012 state | Owner and named contract owners — `:198` | Listed to record that they are **not** P012-dependent, so the amendment neither helps nor harms them. The P013 takeover handoff reports these as implemented in the accepted bounded slice (`P013_HANDOFF.md:24-40`), which is a different claim from "ratified"; see §5 **D-4**. |
| `P020 dependency` lane row (no id in source) | "\| P020 dependency \| P020-owned bundle/receipt/verifier \| P020 package acceptance \| Anything short of accepted frozen identity \|" — `P013_CONTRACT_DECISION_PACKET_V2.md:194` | **both**, transitively | **NO** | P020 package acceptance and a frozen accepted identity — P020 Lead | The stop condition is explicit about partial evidence: "Anything short of accepted frozen identity". |
| `WAIT_P020_ACCEPTANCE` stop condition | "if P020 is not package-accepted, any member/issuer/verifier identity is absent, or the frozen receipt cannot be independently bound to the completed run, P013 remains `WAIT_P020_ACCEPTANCE`; only screening lineage and non-accepting preparation may proceed." — `P013_DEPENDENCY_ADOPTION_MAP.md:83` | **both**, transitively | **NO** | Same as B-01 | The operative gate name for the whole P013 writer lane. |
| Plan acceptance gate for WP-P0-13 (no id in source) | "a real run produces a queryable catalog; a trial that was rejected can be found **by its rejection reason**; **every row carries a `simulator_class` and a `deployment_identity_hash`, and a row produced from the unmigrated path is stamped `SIGNAL_SCREEN_ONLY`** — proven by a fixture in which an unmigrated-path row is shown unable to pass as acceptance evidence." — plan `:416` | **neither** directly; **(i)** indirectly, because "the migrated canonical path" is the P0-20 output that consumes the P0-12 kernel (plan `:411`) | **NO** | The migrated canonical path plus a real run — P020 Lead then P013 Lead | Plan rationale for the hard dependency: "**The catalog is the evidence surface; it is written against the migrated canonical path or its rows are not acceptance-bearing.**" — plan `:414`. |
| P013 accepted-slice boundary (no id in source) | "This acceptance covers only the authorized shared-contract and bounded P013 repairs at the frozen head above. It does not authorize or accept the full writer, selection/artifact/address pipeline, receipt production, publication, reader adoption, or caller integration. Full P013 remains nonaccepted. P020 acceptance and all remaining prerequisites remain separately binding and nonaccepted here." — `C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md:76-81` | **both**, transitively | **NO** | Separately authorized integration scope — owner; then P013 Lead | The bounded slice is already Lead-accepted at head `da1fb184c71e1ae65e2e348758af7f1a84a1cfbd` (`P013_HANDOFF.md:11`) and needs nothing from P012 to stay accepted. |

**P013 summary.** No P013 gate names a P012 state directly. Every P012-sensitive P013 gate is
sensitive only through **P020 package acceptance**, and P020 package acceptance is itself gated on two
state-(ii) rows plus four P020-owned work items (§2.1.2). State (i) alone therefore moves no P013 gate.

### 2.3 WP-P0-21 — objective eligibility criteria and D026 fixtures

P021 is one of only two packages whose plan dependency line names WP-P0-12 directly.

| Gate/criterion id | Verbatim requirement + citation | Depends on state (i), (ii), or both | Satisfied by state (i) alone? | Remaining follow-up + owner | Notes |
|---|---|---|---|---|---|
| Plan `Inputs` line (no id in source) | "**Inputs:** brief §6.5 check table; WP-P0-04 contracts; WP-P0-12 kernel; frozen datasets with recorded hashes." — plan `:517` | **(i)** | **YES**, for this line only — it names the kernel as an **input artifact**, and a fixed, reviewed, Section-16-accepted, owner-ratified kernel is that artifact | Present the exact G5/core identity plus the Section-16 acceptance and ratification records; verified by P021 Lead reproduction against the frozen manifests — P021 Lead | An input line, **not** P021's acceptance gate; it unblocks nothing on its own. See §4 row **S-2**. |
| Plan `Depends on` line (no id in source) | "**Depends on:** WP-P0-04, WP-P0-12. · **Parallel-safe with:** WP-P0-22 and Lanes 1, 2, 3, 6, 7." — plan `:520` | **(i)** for the P0-12 half, **on the literal text**; `neither` for the WP-P0-04 half | **YES (literal text, P0-12 half only)** — with the interpretive caveat in Notes | Owner or plan owner must record whether the narrowed acceptance label discharges a bare `Depends on: WP-P0-12` row — owner / plan owner; then P021 Lead | A bare package dependency is read elsewhere in the same plan as waiting for **whole-package** acceptance: "an unqualified package dependency waits for whole-package acceptance under the §0 staged-milestone rule" — plan `:427`. Post-amendment, WP-P0-12 whole-package acceptance **is** state (i) — which is exactly the reading the owner's "do not automatically unblock" sentence guards. The §0 rule text itself was not read for this draft: see **NV-02**. |
| Plan acceptance gate, brief `A-7c` | "Every check has a stated threshold and a fixture **shown RED without the check and GREEN with it**; **no subjective phrase survives in the criteria**; an unset threshold yields `BLOCKED` and never `PASS`; and every verdict binds to a `deployment_identity_hash`. The divergence check is likewise D026-falsified, and a missing `[OPEN]` tolerance yields `BLOCKED`, never an invented default." — plan `:522` | **neither** | Not applicable — the gate text names no P012 state | Set the `[OPEN]` thresholds by owner ratification; build the fixtures — owner (thresholds) + P021 Lead (fixtures) | Self-contained gate. Authority boundary: "it **produces verdicts and admits nothing.** Admission is WP-V2A-10." — plan `:524`. |
| P021 remaining-dependency statement (no id in source) | "P021: P012 accepted corrected-engine evidence and P020 accepted evidence remain dependencies; `gap_ratio_max`, `divergence_tolerance`, `divergence_window_length`, and `divergence_min_paired_observations` remain unset/fail-closed; LOOKAHEAD_DECISION_DOMAIN B-12 and qualifying forward evidence remain open. No real bundle or readiness PASS occurred." — `C:/tmp/CLAUDE_TAKEOVER_20260913/P021_P030_HANDOFF.md:39` | **(i)** for "P012 accepted corrected-engine evidence"; **both** for the conjoined "P020 accepted evidence" | **NO** overall — the sentence is a conjunction and the P020 half is unsatisfied | (a) P012 accepted corrected-engine evidence — P012 Lead + owner; (b) P020 accepted evidence — P020 Lead; (c) the four thresholds — owner; (d) B-12 lookahead domain and qualifying forward evidence — P021 Lead + real observations | "corrected-engine evidence" maps to the `CORRECTED_VNEXT` deliverable (plan `:400-403`), i.e. to state (i) — but it is one of four conjuncts. `LOOKAHEAD_DECISION_DOMAIN B-12` is not the same `B-12` as P013's; see **NV-11**. |
| P021 eligibility statement (no id in source) | "P021 actual eligibility still needs upstream acceptance, ratified limits and real forward observations." — `C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md:48` | **both** — "real forward observations" is state-(ii)-class evidence | **NO** | Real forward observations under applicable authorization — owner; ratified limits — owner | Independent of P012 reconciliation. |
| P020-consumption prohibition (no id in source) | "P020 `6f7f495af889437830a6c416f8417f8ced0bcdff` remains NONACCEPTED and cannot be consumed as accepted evidence." — `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/HANDOFF.md:16` | **both**, transitively via P020 | **NO** | P020 package acceptance — P020 Lead | The commit id cited here differs from the current P020 head and from the id the P013 packet cites; see §5 **D-5**. |

### 2.4 WP-P0-30 — restart / replay, observation and provenance contracts

**No WP-P0-12 or P012 dependency was located for P030.** A `P0-12` grep over the master plan returns
no P030 line, and the package's own remaining-dependency statement names no P012 item:

> - P030: needs a concrete backend, operating policy, permission protocol, archive-root/store
>   configuration, general restart-first-message closure beyond identical replay, P026
>   monitoring/delivery acceptance, and separately authorized host work. Decision 7 preserves WS-only
>   restart continuity; it is not production readiness.

— `C:/tmp/CLAUDE_TAKEOVER_20260913/P021_P030_HANDOFF.md:40`

| Gate/criterion id | Verbatim requirement + citation | Depends on state (i), (ii), or both | Satisfied by state (i) alone? | Remaining follow-up + owner | Notes |
|---|---|---|---|---|---|
| P030 remaining-dependency statement (no id in source) | See the block quote above — `P021_P030_HANDOFF.md:40` | **neither** | Not applicable — no P012 item is named | Backend, operating policy, permission protocol, archive-root/store configuration, restart closure, P026 acceptance, authorized host work — owner (authorization) + P030 Lead | P030 is unaffected by the amendment in either direction. |
| P030 no-readiness statement (no id in source) | "No real bundle/archive, qualifying forward window, runtime integration, P026 monitoring/delivery acceptance, host/KVM2 action, credential use, venue contact, TESTNET/mainnet action, ARM/order path, deployment, protected-schema change, readiness activation or package acceptance occurred." — `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/HANDOFF.md:18` | **neither** | Not applicable | Separate authority — owner | Merged offline slices are "scoped implementation milestones, not P021 or P030 package acceptance" — same file `:16`. |

### 2.5 WP-P0-31 — fixture lifecycle ledger, Milestone 1

P031 names **no** direct P012 dependency. Its seven outstanding items name WP-P0-04 and WP-P0-13; the
P012 relationship is second-order (P0-13 → P0-20 → P0-12).

| Gate/criterion id | Verbatim requirement + citation | Depends on state (i), (ii), or both | Satisfied by state (i) alone? | Remaining follow-up + owner | Notes |
|---|---|---|---|---|---|
| M1 dependency 1 (no id in source) | "1. exact accepted WP-P0-04 lifecycle/identity/writer provenance;" — `C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:106` | **neither** | Not applicable | WP-P0-04 acceptance — WP-P0-04 owner | No P012 content. |
| M1 dependency 2 (no id in source) | "2. exact accepted WP-P0-13 TrialRecord/catalog provenance actually consumed by P031;" — `P031_HANDOFF.md:107` | **both**, third-order (P0-13 → P0-20 → P0-12) | **NO** | Full P013 acceptance, which needs `WAIT_P020_ACCEPTANCE` closure — P013 Lead + P020 Lead | The handoff explicitly forbids inferring satisfaction from the accepted bounded slice: "P013 notice `da1fb184c71e1ae65e2e348758af7f1a84a1cfbd` reports an accepted bounded contract slice, but it grants no caller integration/full-P013 acceptance and is not in this candidate. Do not infer dependency satisfaction." — `:118-120`. |
| M1 dependency 3 (no id in source) | "3. owner-ratified active worthiness check-set version;" — `P031_HANDOFF.md:108` | **neither** | Not applicable | Owner ratification — owner | A different ratification from P012's chain ratification; do not conflate. |
| M1 dependency 4 (no id in source) | "4. seven fail-closed lifecycle envelopes: DEMOTED target, CHALLENGE incumbent, atomic succession, REJECTED purpose/evidence, ambiguous capacity target, deployment refresh, and evaluation-run candidate scope;" — `P031_HANDOFF.md:109-111` | **neither** | Not applicable | P031 Lead | Engineering work inside P031. |
| M1 dependency 5 (no id in source) | "5. owner decisions for `RETIRED -> RE_ENTRY` and same-epoch reuse of one evaluation run across distinct check-set purposes;" — `P031_HANDOFF.md:112-113` | **neither** | Not applicable | Owner | — |
| M1 dependency 6 (no id in source) | "6. pre-integration tightening/disposition of provenance-losing delegated Pydantic copy/dump helpers;" — `P031_HANDOFF.md:114` | **neither** | Not applicable | P031 Lead | Relates to the R20 `deepcopy()` repair at `:56-57`. |
| M1 dependency 7 (no id in source) | "7. any authorized current-head refresh plus `03_QUANTLENS/HANDOFF.md` reconciliation, followed by the protected acceptance path." — `P031_HANDOFF.md:115-116` | **neither** | Not applicable | Owner (authority) + P031 Lead | Known upstream overlap is only that one file — `:19-20`. |
| M1/package acceptance status (no id in source) | "Milestone 1/package acceptance remains **NO**. This is a non-authoritative fixture checkpoint, not an admission ledger release." — `P031_HANDOFF.md:67-68` | **both**, third-order | **NO** | All seven items above | The candidate is `fixture_only=true`, `accepted=false`, `authoritative_records=0` — `:61-62`. |

### 2.6 WP-P0-22 — research tracker

P022's plan dependency is on WP-P0-04 and WP-P0-13:

> **Added 2026-08-22:** P0-20 waits on the kernel (P0-12) and the writer inventory (P0-08); P0-21
> waits on P0-04 and P0-12; P0-22 waits on P0-04 and P0-13.

— plan `:254`

| Gate/criterion id | Verbatim requirement + citation | Depends on state (i), (ii), or both | Satisfied by state (i) alone? | Remaining follow-up + owner | Notes |
|---|---|---|---|---|---|
| Remaining full-P022 item 1 (no id in source) | "1. Full P0-13 acceptance and an authorized canonical family resolver/interface. A bounded P0-13 contract slice was reported accepted, but full P0-13 and P0-22 caller integration remain unauthorized." — `C:/tmp/CLAUDE_TAKEOVER_20260913/P022_HANDOFF.md:28` | **both**, third-order (P0-13 → P0-20 → P0-12) | **NO** | Full P013 acceptance and a resolver/interface authorization — P013 Lead + owner | The same conflation guard appears here as in P031: a bounded accepted slice is not full acceptance. |
| Remaining full-P022 items 2–6 (no id in source) | e.g. "3. Independent/protected clock and access evidence plus protected, non-mutable history; local SQLite alone is mutable." — `P022_HANDOFF.md:30`; "5. Downstream admission/promotion gates and any runtime integration under separate scope. Nothing here authorizes live eligibility or trading." — `:32` | **neither** for items 2–4 and 6; **both** for item 5's admission/promotion clause | **NO** | Observation coverage, protected clock/history, window/display binding, CI and reviews — P022 Lead; admission/promotion — separate scope, owner | Item 5 is the only production-dependent one, and it is explicitly deferred to separate scope. |
| P022 stop condition (no id in source) | "Stop if full P0-13 is not accepted, the canonical interface is unavailable, ownership/checkout identity is uncertain, a shared hold is active, exact required review capacity is unavailable without paid usage, or the proposed work reaches protected schemas, runtime, host, deployment or trading scope without separate owner approval." — `P022_HANDOFF.md:54` | **both**, third-order via the P0-13 clause | **NO** | As above | The P0-13 clause is the binding one for this reconciliation. |
| Reduced-milestone label (no id in source) | "It reports `LOCAL_LOG_ONLY` and `ACCESS_COMPLETENESS_UNVERIFIED`; it cannot claim clean-window, admission, promotion, or `LIVE_CANDIDATE` status." — `P022_HANDOFF.md:22`; "This is acceptance of the reduced local milestone only, not full P0-22 package acceptance." — `:24` | **neither** | Not applicable | None | The merged reduced tracker needs nothing from P012 and loses nothing under the amendment. |
| Shared `B-12` registry projector | "Sole registry projector and sole hash function are shared with P0-22; P013 only consumes the digest." — `C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:64` | **neither** | Not applicable — B-12 needs owner/WP-P0-04 ratification, not a P012 state | Owner ratification of the exact B-12 member set — owner — `P013_CONTRACT_DECISION_PACKET_V2.md:202` | Recorded because it is a genuine P013↔P022 shared surface that the amendment does not touch. |

### 2.7 Bridge / `IBKR_PAPER_BRIDGE` — it does consume P012-labelled records

The Bridge is in scope: it carries two explicitly P0-12-labelled surfaces — the retained funding
payload schema v10 and the offline synthetic funding materializer.

> ## 12. Retained funding payload — schema v10 (P0-12, opt-in)

— `C:/P020_IMPL_20260912/IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md:537`

> ## 13. Offline synthetic funding materialization (P0-12 D1, synthetic-only)

— `docs/26_FULL_RECONCILIATION_CONTRACT.md:613`

> """Offline, synthetic-only MTC funding candidate materializer (P0-12 D1).

— `C:/P020_IMPL_20260912/IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py:1`

| Gate/criterion id | Verbatim requirement + citation | Depends on state (i), (ii), or both | Satisfied by state (i) alone? | Remaining follow-up + owner | Notes |
|---|---|---|---|---|---|
| `UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN` | "Production mode is unavailable and stays `UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN`. The only accepted completion-evidence kind is `SYNTHETIC_FIXTURE`. There is no mode switch, boolean approval flag, permissive callback or magic literal that unlocks production; the missing binding-packet schema and `source_event_digest` byte domain must be approved and implemented before any production path exists." — `docs/26_FULL_RECONCILIATION_CONTRACT.md:756-761` | **(ii)** plus two explicitly missing engineering artifacts | **NO** | Approve and implement the binding-packet schema and the `source_event_digest` byte domain — owner (approval) + Bridge/P012 implementer; then production admission per §1.2 — owner | Two distinct blockers in one row: a missing **byte-domain design** (engineering, unowned as of this draft) and production admission itself. State (i) covers neither, because the byte domain is explicitly *not* part of the D1 approval — see the next row. |
| D1 approval boundary (no id in source) | "Approved by D1 of the P0-12 decision packet. D1 grants bounded synthetic implementation only. It approves no source-event digest domain, no real venue capture, no Bridge schema10 activation, no account contact and no promotion of an economic record." — `docs/26_FULL_RECONCILIATION_CONTRACT.md:620-623` | **(ii)** for capture/promotion; **neither** for the digest domain, which is an unapproved engineering design | **NO** | Owner approval of the digest domain, then implementation and review — owner + implementer | Mirrors the governing decision: "D1 production mode, production record/schema/runtime changes, venue facts/capture, account/host/trading/deploy, new spend, reviewer substitution, merge and whole P012 acceptance remain excluded." — `C:/CT13/DECISIONS.md:18` (OD-20260911-MATERIALIZER-1). |
| Non-admission structural shape (no id in source) | "A successful candidate is labelled `SYNTHETIC_ONLY` and its root carries no `schedule_id`, no `events` and no `settlement_currency`. Current MTC record selection therefore cannot consume it: `EconomicRecords.funding_schedule_id` raises and `ExecutionEconomics._resolve_funding` refuses with its own `REFUSED_MISSING_FUNDING_EVENT`. This is a structural shape, not a fake signed receipt and not a promotion gate." — `docs/26_FULL_RECONCILIATION_CONTRACT.md:749-754` | **(ii)** | **NO** | Nothing in state (i) changes this refusal; it is deliberately physical rather than flag-based — Bridge/P012 implementer owns the shape; owner owns admission | Important for the amendment: the refusal is structural, so a narrowed acceptance **label** cannot accidentally admit a synthetic candidate. |
| Schema v10 opt-in default (no id in source) | "**Opt-in only.** The default target stays v4. v10 is reached exclusively via `initialize(target_schema_version=10)` through the proven v4→…→v9 chain. No existing caller or database is upgraded by being opened, and reopening a v10 store at a lower target never downgrades it." — `docs/26_FULL_RECONCILIATION_CONTRACT.md:558-562` | **neither** | Not applicable | Activation would be a separate owner decision — owner | The governing decision explicitly excludes activation: "no runtime activation, no minimum-quantity change, no R35 reseal, no production database or host access and no new spend" — `C:/CT13/DECISIONS.md:74` (OD-20260911-FUNDING-1). |
| Bridge-side P012 status statement (no id in source) | "Full WP-P0-12 remains NONACCEPTED with10production OPEN rows,27risks,5residual obligations. [...] Final evidence-backed records, eligible human reviews and R29 semantic redo stay at final production acceptance." — `C:/P020_IMPL_20260912/IBKR_PAPER_BRIDGE/HANDOFF.md:15` | **both** | **NO** | Production acceptance per §1.2 — owner + P012 Lead | This row also names "5residual obligations", a count appearing in no other source read for this draft; see **NV-04**. |

### 2.8 Other packages and gates naming WP-P0-12

Every remaining `P0-12` occurrence located in the master plan and the traceability register.

| Gate/criterion id | Verbatim requirement + citation | Depends on state (i), (ii), or both | Satisfied by state (i) alone? | Remaining follow-up + owner | Notes |
|---|---|---|---|---|---|
| `WP-V2A-02` parallel-safety clause (no separate id) | "**Parallel-safe with:** WP-V2A-03 — **only after WP-V2A-01 and WP-P0-12 respectively have been accepted; not parallel-safe before that.**" — plan `:687` | **(i)** on the literal text | **YES (literal text, P0-12 half only)** | Confirm whether the narrowed label discharges the clause — owner / plan owner. WP-V2A-01 acceptance — its own owner. | A **parallel-safety/sequencing** clause, not WP-V2A-02's acceptance gate. WP-V2A-02's protected surfaces are "Bridge runtime and per-worker state — the process that will later hold live positions", tier **T0** (plan `:688-689`) — production-dependent work squarely inside the owner's "do not automatically unblock" instruction. See §4 **S-3** and §3 **B-9**. |
| `WP-V2A-03` inputs (no separate id) | "**Inputs:** **WP-P0-20's accepted shared Risk Allocator implementation and migrated canonical simulator**; WP-P0-12 kernel; WP-P0-04 contracts." — plan `:696` | **(i)** for the P0-12 kernel input; **both** for the P0-20 accepted-implementation input | **NO** | P020 package acceptance — P020 Lead | The P0-20 conjunct is unsatisfied regardless of P012 state. |
| `WP-V2A-03` depends-on / parallel-safety (no separate id) | "**Depends on:** **WP-P0-20**, WP-P0-12, WP-P0-04, **WP-V2A-02**." — plan `:698`; "**Parallel-safe with:** WP-V2A-01 — **only once WP-P0-20, WP-P0-12, WP-P0-04 and WP-V2A-02 have been accepted; not parallel-safe before that.**" — plan `:699` | **both** — the conjunction includes WP-P0-20 | **NO** | P020, WP-P0-04 and WP-V2A-02 acceptance — respective owners | Even a YES on the P0-12 conjunct leaves three unsatisfied conjuncts. |
| `WP-V2A-03` acceptance gate, brief `A-10c` | "**the same implementation demonstrably runs in backtest and runtime, proven by import identity rather than assertion**; **an allocator that is not simulated fails acceptance** — this is the single highest-risk regression in the whole design; **a stand-in cannot satisfy this gate**." — plan `:701` | **neither** directly | **NO** | The accepted allocator plus the runtime wiring and equivalence proof — P020 Lead then WP-V2A-03 owner | Gate text names no P012 state; it names the accepted P020 implementation. Authority boundary: "This package wires an accepted implementation; it does not author or re-author one." — plan `:703`. |
| `WP-P0-14` depends-on (no separate id) | "**Depends on:** WP-P0-13, **WP-P0-31 Milestone 1** — **and therefore transitively on WP-P0-20, through WP-P0-13**" — plan `:427` | **both**, third-order | **NO** | P013 and P031-M1 — respective Leads | Also carries the owner's deferral: "Owner chose to defer Minimum Explorer behind core Bridge engineering with a small reproducible read-only report meanwhile. Preserve sequencing amendment; full package is not complete." — `C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md:54`. |
| `WP-P0-14` acceptance gate (no separate id) | "**Added in the R1 correction pass: the viewer explicitly refuses to present rows from the unmigrated path as acceptance-bearing** — every row displays its `simulator_class`, a `SIGNAL_SCREEN_ONLY` row is visibly marked as screening-only wherever it appears, and a fixture proves that such a row cannot be surfaced as promotion or gate evidence." — plan `:430` | **neither** directly | **NO** | The migrated path (via P0-20/P0-13) plus the fixture — respective Leads | A refusal requirement; satisfied by refusing, not by admitting. |
| Gate `G3-K` | "**G3-K — Kernel, canonical simulator, and the T0 evidence gates that bless them** \| **WP-P0-09**, **WP-P0-10**, **WP-P0-11**, **WP-P0-12**, **WP-P0-20**, **WP-V2A-07** ... They require **owner authorization naming the exact capability being changed**, a **T0 audit**, **golden-suite and D026 falsification evidence**, and — for WP-P0-20 — **retention of the frozen legacy path** as the rollback." — plan `:1069` | **(i)** for the named evidence classes (owner authorization, T0 audit, golden/D026 evidence) | **NO** as a whole — the row is a gate **membership** statement covering six packages, not a single satisfiable predicate | Per-package T0 audit and D026 evidence — respective Leads; owner authorization — owner | The governance gate that both P0-12 and P0-20 sit inside. It describes these packages as ones that "decide the trading model, what a promotion number means, or whether the evidence for both is real" — the class the owner's non-auto-unblock instruction protects. |
| `WP-P0-23` / Lane-4 collision (no separate id) | "**P0-23 (Lane 7) and P0-09 → P0-12 (Lane 4) both touch `mtc_v2/core/config.py`.** [...] **They are serialized against each other**, and whichever runs second re-establishes its baseline against the other's result rather than assuming it." — plan `:273` | **neither** — a serialization rule, not an acceptance dependency | Not applicable | Whichever package runs second re-establishes its baseline — respective Leads | Recorded so the amendment is not read as releasing the serialization obligation. |
| `O-05` (traceability register) | "Simplify MTC_V2: essential strategy and position management in the core; advanced filters, exits, transforms optional or retired \| OWNER \| ... \| WP-P0-09, WP-P0-10, WP-P0-11, WP-P0-12 \| COVERED \| A-4; the module split is **DL-23, proposed and not owner-ratified**." — `C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:128` | **neither** for the P012 half; the open item is `DL-23` | **NO** | `DL-23` owner ratification — owner | `DL-23` is a **separate** ratification from P012's chain ratification; do not treat state (i)'s owner ratification as covering it. See **NV-05**. |
| `O-07` (traceability register) | "One authoritative Python Strategy Kernel used by backtest, forward test, paper and live \| OWNER (Q1) \| ... \| WP-P0-09, WP-P0-10, WP-P0-11, WP-P0-12 \| COVERED" — `REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:130` | **both** — the requirement text itself names "paper and live" | **NO** | Runtime/paper/live use is separately gated (WP-V2A-02/03, G3) — respective owners | Marked `COVERED` at the plan level, which is a traceability statement, not an acceptance statement. |
| `O-08` (traceability register) | "**The 7 `tw_*` keys are NOT part of this — six are behaviourally active and the seventh is `[DRIFT/UNKNOWN]` (F-8a), and all belong to WP-P0-09 → WP-P0-12**" — `REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:131` | **neither** — an ownership/scoping statement | Not applicable | Pine/`wt_*` scope is WP-P0-19/WP-P0-23 — their owners | Recorded because it assigns the seven `tw_*` keys to the P0-09→P0-12 chain; the amendment does not move that ownership. |
| `O-40` (traceability register) | "Kernel built as `LEGACY_COMPATIBLE` exact reproduction, then separately documented and tested `CORRECTED_VNEXT` fixes \| OWNER (Q15) \| §16 M6/M7a/M7b \| 4 \| WP-P0-10, WP-P0-11, WP-P0-12 \| COVERED \| A-5, A-6 — no undocumented behavioural difference between the two." — `REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:163` | **(i)** — the requirement is entirely a golden/behavioural-evidence claim | **YES**, on the quoted text, provided the golden evidence named in the same row is presented and independently verified | Present both-branch golden families and the no-undocumented-difference evidence, independently verified — P012 Lead reproduction + T0 roster | The same row excludes one key from the obligation: "`tw_margin_call_split_entries` is excluded from the both-branch obligation while it remains `[DRIFT/UNKNOWN]`". See §4 **S-1**. |
| `D-08` (traceability register) | "Economic golden scenarios and D026 RED/GREEN falsification required for migration and parity claims \| DERIVED \| §9.3, §9.6, §16 M6 \| 4 \| WP-P0-10, WP-P0-11, WP-P0-12, WP-V2A-04, WP-V2A-07 \| COVERED \| A-5, A-6, A-10b, A-12; **25** golden families" — `REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:191` | **(i)** for the P0-12 share — golden scenarios and D026 falsification are engineering evidence | **YES**, for the P0-12 share of the row only, provided the golden/D026 evidence is presented and independently verified | Present the golden-family and D026 RED/GREEN evidence at G5 — P012 Lead + T0 roster. WP-V2A-04/WP-V2A-07 shares — their owners. | The row spans five packages; a YES for the P0-12 share closes none of the others. See §4 **S-1**. |
| `WP-P0-26`, `WP-P0-27`, `WP-P0-28`, `WP-P0-16` | No `P0-12` dependency located. P0-16 appears only in lane ordering — "the lane is therefore ordered **P0-20 → P0-13 → {P0-31 → P0-14, P0-16, P0-22}**" — plan `:254` — and in P020's non-parallel-safe list — plan `:506`. P0-26/P0-27/P0-28 next tasks at `START_HERE.md:51-53` name no P012 item. | **neither** | Not applicable | Their own listed work — respective owners | Recorded for completeness: the amendment neither helps nor harms these four. P0-16's own plan section was not read for this draft; see **NV-06**. |

---

## 3. Gates that MUST stay blocked after the amendment, and why

Each row states the gate, the quoted reason it survives the amendment, and the state it actually
needs. The governing instruction is the owner's own: "**do not automatically unblock
production-dependent work**" (`BRIEF.md:7`).

**B-1 — P020 `cost_admission`.** Needs state (ii). Two refusals, both live:

> if costs.P012_ADMISSION_REQUIRED not in reasons[0]:

— `check_p020_acceptance.py:249`

> "real positive record-index lookup succeeded, then remained non-accepting: ...
> {costs.P012_ADMISSION_REQUIRED}; {costs.NON_AUTHORITATIVE_INDEX}"

— `check_p020_acceptance.py:253-256`

**B-2 — P020 `p012_full_acceptance`.** Needs state (ii), and the row is an unconditional constant:

> "P012 full production admission is not supplied by this research lane; the live cost gate above
> returns P012_ADMISSION_REQUIRED"

— `check_p020_acceptance.py:595-598`

**B-3 — P020 `production_admission`.** Needs state (ii); its criterion clause is literally that
research success must not admit production:

> Criterion("production_admission", "research success never admits production", probe_production_admission),

— `check_p020_acceptance.py:670`

**B-4 — P020 `frozen_probe_compatibility`.** Cannot be reconciled at all until the two failures are
named:

> "the disclosed full frozen-probe compatibility state has 2 known failures caused by additive core
> changes; this scoped suite does not edit or waive those probes"

— `check_p020_acceptance.py:602-606`

**B-5 — P020 `real_before_after`, `dependent_disposition`, `real_benchmark`, `independent_reviews`.**
Each needs P020-owned work or external verification that no P012 state supplies:

> "no independently verified before/after run on a real frozen candidate"

— `check_p020_acceptance.py:634`

> "consumer code is being migrated separately, but no independent per-consumer disposition audit is
> complete; source text or a PERFORMED label is not proof"

— `check_p020_acceptance.py:638-642`

> "only bounded synthetic execution is in scope; no real frozen workload benchmark, O-28
> extrapolation or feasibility decision was run"

— `check_p020_acceptance.py:645-649`

> "required independent audits, economic Opus counterpart review, Gemini corroboration and Lead
> acceptance are external and not self-certifiable"

— `check_p020_acceptance.py:652-656`

**B-6 — P013 `B-01` and `WAIT_P020_ACCEPTANCE`.** The relevant source already answers the
milestone-substitution question in the negative:

> The narrower WP-P0-20 research milestone does **not** satisfy P013 blocker B-01.

— `P013_DEPENDENCY_ADOPTION_MAP.md:7`

> No narrower milestone presently meets B-01. "Local research engineering + bounded performance" is
> valuable progress, but B-01 is deliberately package-acceptance-bearing. Reinterpreting it as
> component readiness would silently lower the gate and would let a nonaccepted producer mint
> full-kernel lineage.

— `P013_DEPENDENCY_ADOPTION_MAP.md:35`

> B-01 cannot be signed closed; it waits for actual P020 acceptance.

— `P013_CONTRACT_DECISION_PACKET_V2.md:208`

**B-7 — P013 `FULL_KERNEL_SIMULATION` (`B-05`/`B-08`) and `FullEvidenceSinkCapability`.**

> Joint contract-owner act. Full value remains unavailable until P020 accepts.

— `P013_CONTRACT_DECISION_PACKET_V2.md:123`

> `FULL_KERNEL_SIMULATION` must remain unreachable

— `P013_DEPENDENCY_ADOPTION_MAP.md:27`

**B-8 — P031 M1 dependency on accepted WP-P0-13 provenance.** The source names the exact failure mode
this amendment could cause:

> Do not infer dependency satisfaction.

— `P031_HANDOFF.md:120`

**B-9 — WP-V2A-02 and WP-V2A-03 runtime work.** Even where a sequencing clause reads as literally
satisfied (§4 **S-3**), the packages themselves are production-dependent:

> - **Protected surfaces:** Bridge runtime and per-worker state — the process that will later hold
>   live positions.
> - **Audit tier:** **T0** (runtime identity and state on the live execution path).

— plan `:688-689`

> **an allocator that is not simulated fails acceptance** — this is the single highest-risk regression
> in the whole design; **a stand-in cannot satisfy this gate**.

— plan `:701`

**B-10 — Bridge production funding path.**

> Production mode is unavailable and stays `UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN`. The only
> accepted completion-evidence kind is `SYNTHETIC_FIXTURE`.

— `docs/26_FULL_RECONCILIATION_CONTRACT.md:756-758`

> Every caller fact in a synthetic run is a fixture. A successful candidate proves nothing about
> real-world interval completeness, a real account, a real payment, authoritative settlement time or
> rate, or venue authenticity.

— `docs/26_FULL_RECONCILIATION_CONTRACT.md:765-769`

**B-11 — P022 full-package integration.**

> Stop if full P0-13 is not accepted, the canonical interface is unavailable ...

— `P022_HANDOFF.md:54`

**B-12 — P021 eligibility and readiness.**

> No real bundle or readiness PASS occurred.

— `P021_P030_HANDOFF.md:39`

> P021 actual eligibility still needs upstream acceptance, ratified limits and real forward
> observations.

— `START_HERE.md:48`

**B-13 — P012's own remaining gates, which are components of state (i) and of state (ii).** State (i)
is not yet reached, so these are blocked before any downstream question arises:

> BLOCKED: Fresh Opus verdict, formal Section16/R29, owner ratification, real-account
> evidence/admission, experienced-human money review, protected CI, and integration.

— `C:/tmp/P012_LEAD_20260912/DOWNSTREAM_NOTICE.md:7`

> BLOCKED: Formal Section16/R29, owner ratification, authentic real-account admission, funding M,
> experienced-human money gate, and CI/integration.

— `C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:11`

(The two lists differ on the Opus verdict; see §5 **D-10**.)

**B-14 — the human money gate and any ARM/trade step.**

> A human money gate remains. Owner's research assumptions do not become verified exchange facts or
> permission to ARM/trade.

— `START_HERE.md:25`

**B-15 — the P020 branch's integration path**, independent of P012:

> WP-P0-20 is therefore not package-accepted or merge-ready. P012 remains an external dependency.
> Current branch also needs later current-master reconciliation, required Bridge CI on an up-to-date
> head, PR review and explicit push/PR/merge authority.

— `P020_HANDOFF.md:51`

---

## 4. Gates that state (i) would satisfy

**Precondition for every row in this section:** state (i) is *not yet reached* (§1.1(c),(d)). Each row
below is conditional on formal Section-16 acceptance and owner ratification actually occurring, being
independently verified, and being presented with the named artifact. **None of these rows releases a
package**; each is a single clause inside a larger, still-unsatisfied gate.

**S-1 — Traceability rows `O-40` and `D-08` (the WP-P0-12 share only).**

- Quoted text satisfied: "no undocumented behavioural difference between the two"
  (`REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:163`) and "Economic golden scenarios and D026
  RED/GREEN falsification required for migration and parity claims"
  (`REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:191`), which is the same predicate as the plan's
  own WP-P0-12 acceptance gate at plan `:406`.
- **Exact evidence artifact to present:** the frozen packet
  `C:/tmp/P012_LEAD_20260912/FINAL_R5/FREEZE_MANIFEST.json` (SHA-256
  `3dcf03be6c3b801a3f43840d064ac45be3689fe5bd35bde428e142b3c4297567`) and
  `C:/tmp/P012_LEAD_20260912/FINAL_R5/SHA256_MANIFEST.json` (SHA-256
  `eb403b73b01c4b72b8aad380874ec2c47a747646af8c51cf7f81fe5ec9c2d283`) at G5
  `6d6a450232c81c4c13d63c9a4e06ce3b1bf4f889` / core
  `4698e71659d678f50e549e328e78d25816fa16fe`
  (`.../RESEARCH_PAPER_SCOPE_PROPOSAL.md:13`); the R5 evidence logs it names —
  "`../LEAD_R5/C5_FOCUSED.log` (125 focused tests passed, GREEN), `../LEAD_R5/BRIDGE_UV.log`,
  `../LEAD_R5/FINAL_MTC.log`, and `../LEAD_R5/FINAL_GATE.json`" and the four behavioural RED
  observations in "`../LEAD_R5/RED.log`" (`.../RESEARCH_PAPER_SCOPE_PROPOSAL.md:32`); plus the R6
  adjudications "REVIEWS_R6/opus_max_resume_20260913/REPORT.md and LEAD_ADJUDICATION.json",
  "REVIEWS_R6/sol/REPORT.md and LEAD_ADJUDICATION.json" and
  "REVIEWS_R6/gemini_compact_20260913/LEAD_ADJUDICATION.json, slice1–3 reports and
  INPUT_RECORD_VERIFICATION.json" (`FINAL_HANDOFF_20260913.md:39-44`); and the formal Section-16
  acceptance record plus the applied owner ratification.
- **Who verifies:** P012 Lead independent reproduction (the Lead already reports reverifying "354
  packet files and 338 source members with no mismatches" — `FINAL_HANDOFF_20260913.md:27`), then the
  T0 roster for the reviewed scope, and the eligible formal Section-16 reviewer — who "MUST be
  Gemini3.8, neither Codex nor Claude" (`P012_HANDOFF.md:53`) — for the semantic coverage.
- **Caveat that must travel with this row:** the full gate is currently RED on the unratified chain —
  "The full gate exits2 with exactly SEMANTIC_COVERAGE_REVIEW_INVALID and CONTRACT_SELFTEST_RED"
  (`FINAL_HANDOFF_20260913.md:27`). Whether applying the eight unapplied ratification drafts clears
  it is stated nowhere read (**NV-08**). Also `O-40` excludes
  `tw_margin_call_split_entries` from the both-branch obligation while it remains `[DRIFT/UNKNOWN]`
  (`REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:163`).

**S-2 — Plan `Inputs` lines that name the WP-P0-12 kernel as an artifact.** Two occurrences:
WP-P0-20's "**Inputs:** WP-P0-12 `CORRECTED_VNEXT` kernel" (plan `:489`) and WP-P0-21's "WP-P0-12
kernel" (plan `:517`).

- **Exact evidence artifact to present:** the G5 commit and core-tree identity above, plus an explicit
  statement of the P012 core tree the consumer binds to, reconciled against the compatibility
  receipt's tree `63f804d945d3a7692aca1bc7eee410d9ae87977e`
  (`P012_P020_COMPATIBILITY.json:13`) and the current G5 core tree
  `4698e71659d678f50e549e328e78d25816fa16fe` (`FINAL_HANDOFF_20260913.md:14`).
- **Who verifies:** the consuming package's Lead, by reproduction against the frozen manifests —
  P020 Lead for plan `:489`, P021 Lead for plan `:517`. Any *acceptance-bearing* consumption also
  needs the T0 roster.
- **Caveat:** an `Inputs` line is not an acceptance gate. For P020 specifically, the current branch
  has removed P012 Path-D instrument/economics members (§2.1.3(2)), so presenting G5 does not make
  the current P020 branch consume it.

**S-3 — Bare `accepted`-conditioned sequencing clauses naming WP-P0-12.** Three occurrences:
WP-P0-21's "**Depends on:** WP-P0-04, WP-P0-12" (plan `:520`); WP-V2A-02's "only after WP-V2A-01 and
WP-P0-12 respectively have been accepted" (plan `:687`); and the WP-P0-12 conjunct inside WP-V2A-03's
"only once WP-P0-20, WP-P0-12, WP-P0-04 and WP-V2A-02 have been accepted" (plan `:699`).

- **Exact evidence artifact to present:** (a) a written owner or plan-owner determination that the
  narrowed acceptance scope discharges a bare `Depends on: WP-P0-12` row — because the plan reads a
  bare package dependency as waiting for "whole-package acceptance under the §0 staged-milestone
  rule" (plan `:427`), and the amendment changes what that phrase denotes; plus (b) the full state-(i)
  evidence bundle from **S-1**.
- **Who verifies:** owner (or the plan owner) for the determination in (a); the consuming package's
  Lead for (b).
- **Caveat that must travel with this row:** each of the three clauses is a conjunction, and in every
  case at least one other conjunct is unsatisfied — WP-P0-04 for plan `:520`; WP-V2A-01 for plan
  `:687`; WP-P0-20, WP-P0-04 and WP-V2A-02 for plan `:699`. WP-V2A-02 and WP-V2A-03 are additionally
  the T0 runtime packages the owner's non-auto-unblock sentence is aimed at (§3 **B-9**). The §0 rule
  text was not read (**NV-02**), and no source names the owner of this determination (**NV-09**).

**S-4 — Gate `G3-K`'s evidence classes, for the WP-P0-12 member only.** The row requires "**owner
authorization naming the exact capability being changed**, a **T0 audit**, **golden-suite and D026
falsification evidence**" (plan `:1069`).

- **Exact evidence artifact to present:** the owner authorization records already indexed —
  `OD-20260907-1` lifting the WP-P0-11/WP-P0-12 stop (`C:/CT13/DECISIONS.md:23`), `OD-20260906-1`
  (`:25`), `OD-20260908-1` for re-seal #29 (`:22`) — plus the golden/D026 evidence and the T0 audit
  records from **S-1**.
- **Who verifies:** the T0 roster for the audit; P012 Lead for reproduction; owner for the
  authorization records.
- **Caveat:** `G3-K` is a membership row covering six packages. Satisfying the WP-P0-12 member closes
  nothing for WP-P0-20, WP-V2A-07 or WP-V2B-02, and `OD-20260908-1` states in terms that it "is not
  WP-P0-12 acceptance" (`C:/CT13/DECISIONS.md:22`).

**S-5 — The dependent-tool disposition's stated precondition, which state (i) is not even needed
for.** The disposition text says the migration "waits on `WP-P0-12` reaching this repository"
(`WP_P0_20_DEPENDENT_TOOL_DISPOSITION.md:55-57`), and the decision index records that the source
already arrived:

> OD-20260907-1's source-absence observation is historical: PR #164 imported corrected-vNext source
> into the current base `e69c7d7`. This does not establish WP-P0-12 acceptance, P0-20 consumer wiring
> or any production authority.

— `C:/CT13/DECISIONS.md:10`

- **Exact evidence artifact to present:** the PR #164 import record and base `e69c7d7` as indexed at
  `C:/CT13/DECISIONS.md:10`, reconciled against the P020 worktree's actual core tree.
- **Who verifies:** P020 Lead, by repository reconciliation.
- **Caveat:** the same sentence disclaims acceptance and consumer wiring, and the disposition remains
  `PROPOSED, not PERFORMED` for reasons unrelated to source arrival
  (`WP_P0_20_DEPENDENT_TOOL_DISPOSITION.md:3`). This row is included because it shows the
  disposition's stated precondition is already met, which is a **disagreement** with the same file's
  framing rather than a state-(i) benefit. See §5 **D-1**.

**Nothing else qualifies.** Every other row in §2 is `NO`, `NO (UNKNOWN)`, or `Not applicable`.

---

## 5. Disagreements between sources

**D-1 — What the dependent-tool migration is actually waiting for.**
`WP_P0_20_DEPENDENT_TOOL_DISPOSITION.md:55-57` says the dispositions cannot be performed until "the
canonical path is migrated, and that waits on `WP-P0-12` reaching this repository".
`C:/CT13/DECISIONS.md:10` records that the source already reached the repository via PR #164. Either
the disposition text is stale, or "reaching this repository" means something narrower (for example,
reaching the P020 worktree's own canonical path) than the import that PR #164 performed. Not resolved
here.

**D-2 — Attribution of the two frozen-probe failures.** `check_p020_acceptance.py:601-606` attributes
them to "additive core changes" and names nothing. `P012_P020_COMPATIBILITY_PREP.md:52` and `:66`, and
`P20P012_COMPAT_FINAL.md:13`, record the names as UNKNOWN and explicitly decline to infer them.
`P013_DEPENDENCY_ADOPTION_MAP.md:30` calls them "two disclosed P012 probe failures", attributing them
to P012. The third statement is stronger than the first two support.

**D-3 — Which P012 core tree is the compatibility baseline.** The receipt compared P012 commit
`e2fd210411287802676c43ddc66afa7a23c75313`, core subtree
`63f804d945d3a7692aca1bc7eee410d9ae87977e` (`P012_P020_COMPATIBILITY.json:7,13`). The current
candidate's core tree is `4698e71659d678f50e549e328e78d25816fa16fe`
(`FINAL_HANDOFF_20260913.md:14`; `.../RESEARCH_PAPER_SCOPE_PROPOSAL.md:13`). The receipt's
`COMPATIBLE_SYNTHETIC` finding therefore does not automatically carry to the current G5 core.

**D-4 — Status of the P013 contract choices `B-03`, `B-04`, `B-12`, `B-17`, `B-09`/`D-04`, `D-05`.**
`P013_CONTRACT_DECISION_PACKET_V2.md:200-206` lists them as an owner checklist and `:217` marks
"Protected identity/schema decisions | WAITING FOR CONTRACT OWNERS". `P013_HANDOFF.md:24-40` lists
them as "Implemented approvals" under binding records `OD-20260912-P013-CONTRACTS` and
`OD-20260913-P013-CONTRACT-DEFAULTS`. The handoff is the later document (2026-09-13 versus the
packet's 2026-09-12 file date) and may supersede, but neither file says so explicitly. Not resolved
here.

**D-5 — Which P020 commit is "the nonaccepted candidate".** Cited ids:
`556639f59122e33b664ab918a4241eb96680219b` (`P013_CONTRACT_DECISION_PACKET_V2.md:30`;
`P013_DEPENDENCY_ADOPTION_MAP.md:7,16`); `6f7f495af889437830a6c416f8417f8ced0bcdff`
(`C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/HANDOFF.md:16`;
`C:/tmp/P020_LEAD_20260912/STATUS.md:88`); `705c99b1a2469518988e9ba88e79e967ea10cb65`
(`STATUS.md:96`); `52422017e032b11d5cdc31aaeb94d8cfda1a42cf` (`P020_HANDOFF.md:10`; `STATUS.md:164`);
and `b9b72f858dc830a9389517f79da5ea3c1fa6122c`, named the "Clean HEAD" (`P020_HANDOFF.md:9`). Only the
last is presented as current. Any downstream statement pinning P020 must name which.

**D-6 — Current `origin/master`.** `START_HERE.md:57`, `P020_HANDOFF.md:12` and `P022_HANDOFF.md:7`
give `fcac0ac67cf2682693ad28138b1a56e15a0846f2`. The repository's own governance handoff says
"Current verified `origin/master` is `ca2f8a68219b03085edc86900a4e15745e67a504`"
(`C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/HANDOFF.md:5`). `FINAL_HANDOFF_20260913.md:37`
reports "cached origin/master 42f99571". Three values; the in-repository one is the closeout's own
pre-merge base, and `P021_P030_HANDOFF.md:7` warns "do not assume that ref remains current without a
permitted refresh."

**D-7 — The compatibility receipt's line citations into the acceptance checker are stale.** It cites
"`check_p020_acceptance.py:203-216`" for the synthetic fixtures
(`P012_P020_COMPATIBILITY_PREP.md:27`) and `:265-268`, `:225-241`, `:258-261`, `:272-283`
(`P012_P020_COMPATIBILITY_PREP.md:52-55`). In the file read for this draft the corresponding code is
at `:217-236`, `:601-606`, `:239-256`, `:594-598` and `:608-630`. The receipt's quoted **content**
matches the current file; only its line numbers do not.

**D-8 — Section-16 reviewer claim versus Lead disposition.** The reviewer reported "Items1/4
ACCEPTED_WITH_RESIDUAL_RISK, successorUNCHANGED, overallPARTIAL_REVIEW_ONLY"; the Lead checkpoint is
`NONACCEPTING_REQUIRED_READ_GAPS` (`P012_HANDOFF.md:29`; `START_HERE.md:22`). Any downstream
statement must use the Lead disposition, not the reviewer headline.

**D-9 — Where the production requirements for WP-P0-12 are recorded.** The master plan's WP-P0-12
acceptance gate is engineering-only (plan `:406`), and a grep for `Section 19`, `Section-19`,
`Section 16`, `Section-16`, `ten OPEN` and `10 OPEN` over both the master plan and the traceability
register returned no match. The ten production OPEN rows, the 27 risks, N=3 and funding M appear only
in the P012 Lead/takeover files and in `C:/CT13/DECISIONS.md:22`. The plan and register therefore do
not, on their own text, describe the two-state boundary this amendment narrows.

**D-10 — The Opus engineering verdict.** `DOWNSTREAM_NOTICE.md:9` says "Opus hit its session limit
before review; no verdict, retry, substitution, or PAYG" and lists "Fresh Opus verdict" as BLOCKED
(`:7`). `FINAL_HANDOFF_20260913.md:21` records "Opus claude-opus-5 xhigh | PASS-WITH-NITS, exit0, 80
turns, 04:03:53–04:29:11Z; Lead accepted after reading report and actual execution records". The later
file states it supersedes: "It supersedes reviewer/capacity statuses in FINAL_HANDOFF.md and
FINAL_STATE.json" (`FINAL_HANDOFF_20260913.md:5`) — it does not name `DOWNSTREAM_NOTICE.md`, so the
supersession is inferred rather than stated.

**D-11 — Characterization of the MTC suite failure.** `FINAL_HANDOFF_20260913.md:27` reports "MTC 705
passed / 1 failed / 1 skipped, exit1; the sole failure is the unratified-chain schema".
`P012_HANDOFF.md:17` reports the same counts as "MTC705passed/1expected schema failure/1skipped". Same
numbers, different label ("failed" versus "expected ... failure"). Downstream text should use the
first, which names the cause.

---

## 6. NOT VERIFIED

Non-empty by requirement, and non-empty in fact.

- **NV-01** — The identities of the two frozen-probe failures behind P020's
  `frozen_probe_compatibility`. The checker discloses a count and a cause only
  (`check_p020_acceptance.py:601-606`); the receipt declines to infer names
  (`P012_P020_COMPATIBILITY_PREP.md:52`). Not inferred here.
- **NV-02** — The §0 staged-milestone rule's own text. It is referenced at plan `:427` and relied on
  by §2.3 and §4 **S-3**, but the §0 section itself was not read for this draft.
- **NV-03** — No source read contains a mapping from "P0-12 accepted" to a specific downstream
  release action. Every §4 row is therefore an inference from the quoted dependency text, not a quoted
  release rule.
- **NV-04** — The "5residual obligations" named at
  `C:/P020_IMPL_20260912/IBKR_PAPER_BRIDGE/HANDOFF.md:15` were not enumerated in any source read.
- **NV-05** — Whether P012's owner ratification of the seal chain also ratifies `DL-23`
  (`REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:128`). No source read says so; treated here as
  separate.
- **NV-06** — The plan sections for WP-P0-16, WP-P0-26, WP-P0-27 and WP-P0-28, and the brief texts
  referenced as §6.5, §9.1a, §9.2, A-7b, A-7c, A-10b, A-10c and A-12, were not read. Every reference
  to them here is as quoted by the plan or register.
- **NV-07** — `check_p020_acceptance.py` was **not executed** (it documents no read-only mode). All
  P020 criterion states are as reported by `P020_HANDOFF.md:30` and `:40-49` and the `STATUS.md` rows
  cited, not reproduced by this draft.
- **NV-08** — The P012 full-gate state "exits2 with exactly SEMANTIC_COVERAGE_REVIEW_INVALID and
  CONTRACT_SELFTEST_RED" (`FINAL_HANDOFF_20260913.md:27`) was not reproduced, and no source read
  states whether applying the eight unapplied ratification drafts clears it.
- **NV-09** — No source read names who owns the determination "does state (i) discharge a bare
  `Depends on: WP-P0-12` row". §4 **S-3** attributes it to the owner or plan owner by inference from
  plan `:427`.
- **NV-10** — Whether the `IBKR_PAPER_BRIDGE` copy read here (inside `C:/P020_IMPL_20260912`) is
  byte-current with the copy on `origin/master` was not checked.
- **NV-11** — `LOOKAHEAD_DECISION_DOMAIN B-12` (`P021_P030_HANDOFF.md:39`) was not located in any
  source read and is **not** the same `B-12` as P013's `preregistered_space_hash` item
  (`P013_CONTRACT_DECISION_PACKET_V2.md:59-64`). Not reconciled.
- **NV-12** — No repository-wide consumer census of P012 records was performed. Only the
  `IBKR_PAPER_BRIDGE` tree inside `C:/P020_IMPL_20260912` was searched, for `P0-12`, `P012` and
  `FundingEventRecord`. Other consumers may exist outside that tree.
- **NV-13** — The exact wording of the owner instruction was taken from `BRIEF.md:7` as supplied; the
  original owner message was not read.
- **NV-14** — Whether the narrowed label changes text printed by any tool (for example, a status
  string anywhere reading "WP-P0-12 NONACCEPTED") was not surveyed beyond the files cited here.

---

## 7. Citation index

One citation per line. Paths as read.

```
C:/tmp/CLAUDE_P0_RUN_20260913/laneP12D_downstream/BRIEF.md:7
C:/P020_IMPL_20260912/check_p020_acceptance.py:63-67
C:/P020_IMPL_20260912/check_p020_acceptance.py:74
C:/P020_IMPL_20260912/check_p020_acceptance.py:101
C:/P020_IMPL_20260912/check_p020_acceptance.py:108
C:/P020_IMPL_20260912/check_p020_acceptance.py:131
C:/P020_IMPL_20260912/check_p020_acceptance.py:157
C:/P020_IMPL_20260912/check_p020_acceptance.py:165
C:/P020_IMPL_20260912/check_p020_acceptance.py:207
C:/P020_IMPL_20260912/check_p020_acceptance.py:217-236
C:/P020_IMPL_20260912/check_p020_acceptance.py:239-256
C:/P020_IMPL_20260912/check_p020_acceptance.py:249
C:/P020_IMPL_20260912/check_p020_acceptance.py:253-256
C:/P020_IMPL_20260912/check_p020_acceptance.py:535-591
C:/P020_IMPL_20260912/check_p020_acceptance.py:586-591
C:/P020_IMPL_20260912/check_p020_acceptance.py:594-598
C:/P020_IMPL_20260912/check_p020_acceptance.py:595
C:/P020_IMPL_20260912/check_p020_acceptance.py:595-598
C:/P020_IMPL_20260912/check_p020_acceptance.py:601-606
C:/P020_IMPL_20260912/check_p020_acceptance.py:602-606
C:/P020_IMPL_20260912/check_p020_acceptance.py:608-630
C:/P020_IMPL_20260912/check_p020_acceptance.py:627
C:/P020_IMPL_20260912/check_p020_acceptance.py:628
C:/P020_IMPL_20260912/check_p020_acceptance.py:630
C:/P020_IMPL_20260912/check_p020_acceptance.py:633-634
C:/P020_IMPL_20260912/check_p020_acceptance.py:634
C:/P020_IMPL_20260912/check_p020_acceptance.py:637-642
C:/P020_IMPL_20260912/check_p020_acceptance.py:638-642
C:/P020_IMPL_20260912/check_p020_acceptance.py:644-649
C:/P020_IMPL_20260912/check_p020_acceptance.py:645-649
C:/P020_IMPL_20260912/check_p020_acceptance.py:651-656
C:/P020_IMPL_20260912/check_p020_acceptance.py:652-656
C:/P020_IMPL_20260912/check_p020_acceptance.py:659
C:/P020_IMPL_20260912/check_p020_acceptance.py:660
C:/P020_IMPL_20260912/check_p020_acceptance.py:661
C:/P020_IMPL_20260912/check_p020_acceptance.py:662
C:/P020_IMPL_20260912/check_p020_acceptance.py:663
C:/P020_IMPL_20260912/check_p020_acceptance.py:664
C:/P020_IMPL_20260912/check_p020_acceptance.py:665
C:/P020_IMPL_20260912/check_p020_acceptance.py:666
C:/P020_IMPL_20260912/check_p020_acceptance.py:667
C:/P020_IMPL_20260912/check_p020_acceptance.py:668
C:/P020_IMPL_20260912/check_p020_acceptance.py:669
C:/P020_IMPL_20260912/check_p020_acceptance.py:670
C:/P020_IMPL_20260912/check_p020_acceptance.py:671
C:/P020_IMPL_20260912/check_p020_acceptance.py:672
C:/P020_IMPL_20260912/check_p020_acceptance.py:673
C:/P020_IMPL_20260912/check_p020_acceptance.py:674
C:/P020_IMPL_20260912/check_p020_acceptance.py:704
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_20_DEPENDENT_TOOL_DISPOSITION.md:3
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_20_DEPENDENT_TOOL_DISPOSITION.md:55-57
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_20_DEPENDENT_TOOL_DISPOSITION.md:69
C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_20_DEPENDENT_TOOL_DISPOSITION.md:111-112
C:/P020_IMPL_20260912/IBKR_PAPER_BRIDGE/HANDOFF.md:15
C:/P020_IMPL_20260912/IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py:1
C:/P020_IMPL_20260912/IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md:537
C:/P020_IMPL_20260912/IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md:558-562
C:/P020_IMPL_20260912/IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md:613
C:/P020_IMPL_20260912/IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md:620-623
C:/P020_IMPL_20260912/IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md:749-754
C:/P020_IMPL_20260912/IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md:756-758
C:/P020_IMPL_20260912/IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md:756-761
C:/P020_IMPL_20260912/IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md:765-769
C:/tmp/P020_LEAD_20260912/P20P012_COMPAT_FINAL.md:10-11
C:/tmp/P020_LEAD_20260912/P20P012_COMPAT_FINAL.md:13
C:/tmp/P020_LEAD_20260912/p012_compat/P012_P020_COMPATIBILITY_PREP.md:15
C:/tmp/P020_LEAD_20260912/p012_compat/P012_P020_COMPATIBILITY_PREP.md:27
C:/tmp/P020_LEAD_20260912/p012_compat/P012_P020_COMPATIBILITY_PREP.md:42-43
C:/tmp/P020_LEAD_20260912/p012_compat/P012_P020_COMPATIBILITY_PREP.md:52
C:/tmp/P020_LEAD_20260912/p012_compat/P012_P020_COMPATIBILITY_PREP.md:52-55
C:/tmp/P020_LEAD_20260912/p012_compat/P012_P020_COMPATIBILITY_PREP.md:53
C:/tmp/P020_LEAD_20260912/p012_compat/P012_P020_COMPATIBILITY_PREP.md:65
C:/tmp/P020_LEAD_20260912/p012_compat/P012_P020_COMPATIBILITY_PREP.md:66
C:/tmp/P020_LEAD_20260912/p012_compat/P012_P020_COMPATIBILITY.json:7
C:/tmp/P020_LEAD_20260912/p012_compat/P012_P020_COMPATIBILITY.json:13
C:/tmp/P020_LEAD_20260912/STATUS.md:88
C:/tmp/P020_LEAD_20260912/STATUS.md:96
C:/tmp/P020_LEAD_20260912/STATUS.md:164
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:9
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:10
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:12
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:21
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:30
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:31
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:40-49
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:51
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:58-70
C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md:113
C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:11
C:/tmp/CLAUDE_TAKEOVER_20260913/P013_HANDOFF.md:24-40
C:/tmp/CLAUDE_TAKEOVER_20260913/P021_P030_HANDOFF.md:7
C:/tmp/CLAUDE_TAKEOVER_20260913/P021_P030_HANDOFF.md:39
C:/tmp/CLAUDE_TAKEOVER_20260913/P021_P030_HANDOFF.md:40
C:/tmp/CLAUDE_TAKEOVER_20260913/P022_HANDOFF.md:7
C:/tmp/CLAUDE_TAKEOVER_20260913/P022_HANDOFF.md:22
C:/tmp/CLAUDE_TAKEOVER_20260913/P022_HANDOFF.md:24
C:/tmp/CLAUDE_TAKEOVER_20260913/P022_HANDOFF.md:28
C:/tmp/CLAUDE_TAKEOVER_20260913/P022_HANDOFF.md:30
C:/tmp/CLAUDE_TAKEOVER_20260913/P022_HANDOFF.md:32
C:/tmp/CLAUDE_TAKEOVER_20260913/P022_HANDOFF.md:54
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:19-20
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:56-57
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:61-62
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:67-68
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:106
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:107
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:108
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:109-111
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:112-113
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:114
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:115-116
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:118-120
C:/tmp/CLAUDE_TAKEOVER_20260913/P031_HANDOFF.md:120
C:/tmp/CLAUDE_TAKEOVER_20260913/P012_HANDOFF.md:7
C:/tmp/CLAUDE_TAKEOVER_20260913/P012_HANDOFF.md:11
C:/tmp/CLAUDE_TAKEOVER_20260913/P012_HANDOFF.md:15
C:/tmp/CLAUDE_TAKEOVER_20260913/P012_HANDOFF.md:17
C:/tmp/CLAUDE_TAKEOVER_20260913/P012_HANDOFF.md:19
C:/tmp/CLAUDE_TAKEOVER_20260913/P012_HANDOFF.md:29
C:/tmp/CLAUDE_TAKEOVER_20260913/P012_HANDOFF.md:53
C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md:22
C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md:25
C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md:48
C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md:51-53
C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md:54
C:/tmp/CLAUDE_TAKEOVER_20260913/START_HERE.md:57
C:/tmp/P012_LEAD_20260912/DOWNSTREAM_NOTICE.md:7
C:/tmp/P012_LEAD_20260912/DOWNSTREAM_NOTICE.md:9
C:/tmp/P012_LEAD_20260912/DOWNSTREAM_NOTICE.md:13
C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:3
C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:5
C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:10-11
C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:11
C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:13-15
C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:14
C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:21
C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:27
C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:33
C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:35
C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:37
C:/tmp/P012_LEAD_20260912/FINAL_HANDOFF_20260913.md:39-44
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:30
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:35
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:59-64
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:64
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:119
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:123
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:130
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:134
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:194
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:198
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:200-206
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:201
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:202
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:208
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:217
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md:225
C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md:7
C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md:16
C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md:27
C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md:30
C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md:35
C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md:83
C:/tmp/P013_LEAD_20260912/P013_CONTRACT_V2_VERIFICATION.md:76-81
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:254
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:273
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:400-403
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:406
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:411
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:413
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:414
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:416
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:427
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:430
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:489
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:499
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:504
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:505
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:506
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:509
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:510
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:517
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:520
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:522
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:524
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:687
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:688-689
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:696
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:698
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:699
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:701
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:703
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:1069
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:128
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:130
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:131
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:163
C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/REQUIREMENTS_TRACEABILITY_REGISTER_2026-08-22.md:191
C:/CT13/DECISIONS.md:10
C:/CT13/DECISIONS.md:18
C:/CT13/DECISIONS.md:22
C:/CT13/DECISIONS.md:23
C:/CT13/DECISIONS.md:25
C:/CT13/DECISIONS.md:74
C:/CT13/DECISIONS.md:79
C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/HANDOFF.md:5
C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/HANDOFF.md:16
C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/HANDOFF.md:18
C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:3
C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:13
C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:20
C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:22
C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:23
C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:28
C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:30
C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:32
C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY/RATIFICATION_DRAFTS_UNEXECUTED/RESEARCH_PAPER_SCOPE_PROPOSAL.md:38-40
```

---

**End of draft.** No recommendation to unblock is made or implied. The Lead audits every citation
above; where a line number proves stale (see §5 **D-7** for a worked example), the quoted content is
the authority and the line reference must be re-derived.

---

## 8. Lead audit and recording note (Claude Fable 5.1, 2026-09-13)

- This is closure-checklist artifact A-13 of `P012_ACCEPTANCE_AMENDMENT_20260913.md`. It records that **no downstream gate is unblocked** by the narrowed WP-P0-12 acceptance: every P020 acceptance criterion stays as reported (8/16 MET is the reporter's structural ceiling; the eight blocked rows need state (ii) evidence, P020-owned work or external review), P013 waits on P020 package acceptance (`WAIT_P020_ACCEPTANCE`), P031/P022 wait on full P013, the Bridge production funding path stays `UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN`, and the only literal YES rows (§4 S-1..S-4) are input/sequencing clauses that still require an owner or plan-owner determination and other unsatisfied conjuncts. Nothing here releases a package.
- Citation audit: all 217 index entries resolved mechanically against their files with valid line bounds; no unresolved or over-range citation.
- Lead resolutions of the drafter's open items: D-6 — the Lead fetched `origin/master` at 10:0xZ on 2026-09-13 and verified `fcac0ac67cf2682693ad28138b1a56e15a0846f2`; the in-repository governance handoff value `ca2f8a68` is the closeout's pre-merge base. D-8 — the first partial Section-16 call is NOT accepted; Item 1 is being re-reviewed in bounded parts (Part A complete with full native coverage, `C:/tmp/P012_S16_REVIEWS_20260913/A2_ITEM1A_TABLES_CODE/LEAD_ADJUDICATION.md`). D-10 — `FINAL_STATE_20260913.json` records `opus: PASS_WITH_NITS_EXACT_ROLE_ACCEPTED`, so `DOWNSTREAM_NOTICE.md` (2026-09-12T23:40Z) is superseded on that point. NV-13 — the owner's original chat message was read by the Lead and is quoted verbatim in the amendment record §0. NV-01 (names of the two frozen-probe failures) and D-1/D-2/D-3 (compatibility baseline core `63f804d9` versus G5 core `4698e716`) remain open P020-side facts to be resolved by the P020 lane before any P012 hand-off is consumed.
- Recording act: file added under the takeover mirror in the control checkout `C:/CT13`; ordinary local commit after the Gemini quiet window; no push. Grants no acceptance and uses no completion label.
- Source draft preserved unchanged at `C:/tmp/CLAUDE_P0_RUN_20260913/laneP12D_downstream/DOWNSTREAM_RECONCILIATION_DRAFT.md` (SHA-256 f1b1f06ae87a98fc789bd0f883034c670b66eb9e83a7e9b405698f4943e622ca).
