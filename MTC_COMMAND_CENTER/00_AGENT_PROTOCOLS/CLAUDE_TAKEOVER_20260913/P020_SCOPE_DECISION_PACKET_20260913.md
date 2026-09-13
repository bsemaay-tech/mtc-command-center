# WP-P0-20 scope / dependency decision packet — RECORDED 2026-09-13 (owner decisions D-P20-1..3 pending; nothing applied)

**Role.** Independent drafting analyst (`claude-opus-5`, xhigh). NOT a reviewer, NOT an acceptor, NOT
the Lead. **Nothing here accepts anything, waives any requirement, unblocks anything, or authorizes
work.** Every citation must be audited by the Lead. Read-only; no Git write, no network, no execution
of `check_p020_acceptance.py`, no benchmark, no test. Prepared 2026-09-13.

**Tokens.** `HND`=`C:/tmp/CLAUDE_TAKEOVER_20260913/P020_HANDOFF.md` · `HO/`=`C:/tmp/CLAUDE_TAKEOVER_20260913/` ·
`CHK`=`C:/P020_IMPL_20260912/check_p020_acceptance.py` · `DISP`=`C:/P020_IMPL_20260912/MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_20_DEPENDENT_TOOL_DISPOSITION.md` ·
`L20/`=`C:/tmp/P020_LEAD_20260912/` · `PREP`=`L20/p012_compat/P012_P020_COMPATIBILITY_PREP.md` ·
`MAP13`=`C:/tmp/P013_LEAD_20260912/P013_DEPENDENCY_ADOPTION_MAP.md` · `PKT13`=`C:/tmp/P013_LEAD_20260912/P013_CONTRACT_DECISION_PACKET_V2.md` ·
`DSGN`=`C:/tmp/P0_OVERNIGHT_20260912/MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_PREPARATION_20260912/inputs/P013_DESIGN_DRAFT_V1.md` ·
`LANE/`=`C:/tmp/CLAUDE_P0_RUN_20260913/` · `DRD`=`LANE/laneP12D_downstream/DOWNSTREAM_RECONCILIATION_DRAFT.md` ·
`P13M`=`LANE/laneP13M_dependency_map/P013_DEPENDENCY_ADOPTION_MAP_DRAFT.md` · `CT13/`=`C:/CT13/` ·
`PROT/`=`CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/` · `AMD`=`PROT/CLAUDE_TAKEOVER_20260913/P012_ACCEPTANCE_AMENDMENT_20260913.md` ·
`PLAN`=`CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md` ·
`PRE`=`C:/tmp/P020_PRESELECT_20260913/PRESELECTION_PREREG_V1.md` · `DSN`=`C:/tmp/P012_LEAD_20260912/DOWNSTREAM_NOTICE.md`.

---

## 1. Identity

| Field | Value | Cite |
|---|---|---|
| Worktree / branch | `C:/P020_IMPL_20260912` · `feature/p020-successor-20260912` | `HND:7-8` |
| Clean HEAD | `b9b72f858dc830a9389517f79da5ea3c1fa6122c` | `HND:9` |
| Reviewed candidate | `52422017e032b11d5cdc31aaeb94d8cfda1a42cf` | `HND:10` |
| Remote master (read-only) | `fcac0ac67cf2682693ad28138b1a56e15a0846f2`; 51 behind / 25 ahead, 40 paths | `HND:12-13` |
| Reporter | "Acceptance remains intentional exit 1: 8/16 criteria MET / `NOT ACCEPTABLE`." | `HND:30` |
| Package | "WP-P0-20 is therefore not package-accepted or merge-ready." | `HND:51` |

**Approved benchmark work.** "Newly authorized on 2026-09-13: preregistered benchmark
profile-selection procedure. […] It is APPROVED BUT NOT STARTED" (`HND:21`; `CT13/DECISIONS.md:80`);
procedure at `PRE`. **Its one open blocker is D1**: the only BTCUSDT 1D dataset has 2,409 derived rows
and measurement locks rows 1..2048, so "The frozen 2048-row calibration window exists for 15m/1h/2h/4h
but cannot exist for 1D" (`LANE/OWNER_DECISIONS_PENDING.md:7`; `PRE:148,161`). Nothing executes until
D1 is answered and `PRE` is re-frozen and T0-reviewed (`PRE:195-197`; `HND:68`).

---

## 2. Criterion map — all 16

**A** = required for research/engineering closure now · **B** = proposed production-admission
follow-up · **C** = unresolved, with the exact blocker. Clauses are the `Criterion(...)` second
arguments at `CHK:659-674` (read, not executed). "in object" = already inside the §4 acceptance object.

| id | verbatim clause (`CHK:`) | state | class | closes it / who | note |
|---|---|---|---|---|---|
| `checklists` | "legacy checklist plus additive research vocabulary" (`:659`) | MET | A | in object; P020 Lead | Names no P012 state. |
| `battery_definition` | "statistical-battery definition remains pinned" (`:660`) | MET | A | in object; P020 Lead | — |
| `verified_execution_join` | "actual E/X/V/M carrier is computed" (`:661`) | MET | A | in object; P020 Lead | Synthetic slice only. |
| `d026_uncomputed` | "name-only coverage refuses and REQUIRED gaps block" (`:662`) | MET | A | in object; P020 Lead | — |
| `standin_prohibition` | "stand-ins never become acceptance evidence" (`:663`) | MET | A | in object; P020 Lead | `PLAN:499`. |
| `allocator_execution_identity` | "canonical allocator object is imported and executed" (`:664`) | MET | A | in object; P020 Lead | `PLAN:509`. |
| `successor_components` | "successor, portfolio and canonical export execute" (`:665`) | MET | A | in object; P020 Lead | `2.1.0` drives the registry `INCOMPATIBLE` finding (`PREP:65`). |
| `required_control_coverage` | "all enabled REQUIRED children need X-and-V" (`:667`) | MET | A | 17/17 evidence re-attested by fresh T0 — P020 Lead + roster | "nine gaps" in the canonical run (`HND:31`); **D-P20-B**. |
| `cost_admission` | "record identity is not P012 cost admission" (`:666`) | BLOCKED | **B** | (a) authentic P012 production cost admission — owner + P012 Lead + venue/Bridge evidence; (b) an authoritative non-synthetic cost index — P020 Lead | "{P012_ADMISSION_REQUIRED}; {NON_AUTHORITATIVE_INDEX}" (`:253-256`); state (i) insufficient (§2.1). |
| `p012_full_acceptance` | "applicable P012 admission remains prerequisite" (`:668`) | BLOCKED | **B** | authentic own-account P012 production admission — owner + P012 Lead | Unconditional `return BLOCKED` (`:594-598`); `DRD:300`. |
| `frozen_probe_compatibility` | "full frozen probes must be compatible" (`:669`) | BLOCKED | **C** | **Blocker: the two failing probes are unnamed.** Name them, then assign owner/remedy — P020 Lead | Names "remain UNKNOWN … and are not inferred" (`PREP:52`); cause only "additive core changes" (`:601-606`). **NV-01**, **D-2**. |
| `production_admission` | "research success never admits production" (`:670`) | BLOCKED | **B** | nothing from P012 satisfies it; it is a refusal proof, not an admission path | **No MET branch** (`:608-630`). |
| `real_before_after` | "real frozen-candidate before/after evidence" (`:671`) | BLOCKED | **C** | **Blocker: canonical-path migration not performed** (**D-1** disputes what it waits for); then an independently verified before/after — P020 Lead + roster | `:633-634`; `PLAN:504`. |
| `dependent_disposition` | "dependent consumers require audited disposition" (`:672`) | BLOCKED | **C** | **Blocker: migration not performed; no per-consumer audit** — "PROPOSED, not PERFORMED." (`DISP:3`) — P020 Lead + auditor | "source text or a PERFORMED label is not proof" (`:637-642`). |
| `real_benchmark` | "real workload benchmark and feasibility" (`:673`) | BLOCKED | **A, blocked on D1** | Answer D1; re-freeze/T0-review `PRE`; run the locked 15-trial eligibility check; then the bounded measurement — P020 Lead | `:644-649`; `PLAN:510` also wants trials/hour + O-28 extrapolation — **D-P20-C**. |
| `independent_reviews` | "mandatory reviews and Lead acceptance" (`:674`) | BLOCKED | **A** (roster) / **B-C** (Lead acceptance) | Fresh exact T0 roster on the frozen head closes the A half — `claude-opus-5` xhigh + `gpt-5.6-sol` xhigh + `gemini-3.7-flash-high` + Lead reproduction (`PROT/REVIEW_POLICY.md:20`; `HND:113`) | "external and not self-certifiable" (`:651-656`); acceptance also needs `HND:51`. |

### 2.1 The revised P0-12 scope moves none of the three P012-facing rows

`OD-20260913-P012-SCOPE-1` narrows P012 to its research/engineering deliverable under the label "P0-12
research/engineering scope complete; production admission pending", leaving `OPEN-01`..`OPEN-10`, the
27 signed risks and Item 4 `NONE_KEEP_REFUSED` unchanged (`CT13/DECISIONS.md:76`); "A row being Class B
never means 'resolved'" (`AMD:32`). That is P012 **state (i)**. `DRD` classifies all three rows
state-**(ii)**, answer **NO**: `p012_full_acceptance` — "the probe text says 'full production
admission'" (`DRD:300`); `production_admission` — "**(ii)** | **NO**" (`DRD:302`); `cost_admission` —
"**(ii)** for the `P012_ADMISSION_REQUIRED` half" (`DRD:299`). P012 agrees: "No accepted P012
dependency B01 or production cost admission is available to P020" (`DSN:13`).

### 2.2 `8/16` cannot rise without editing the reporter — that edit is its own decision

> `8/16 MET` is therefore the structural ceiling of the reporter as written, and **no change of P012
> state — (i) or (ii) — can move the printed count.** Any movement requires an edit to
> `check_p020_acceptance.py`, which is a P020-owned acceptance-surface change with its own authority
> and review requirements. — `DRD:320-323`

Eight probes have no `MET` branch: `CHK:594-598`, `:601-606`, `:633-634`, `:637-642`, `:644-649`,
`:651-656` (unconditional `BLOCKED`) and `:239-256`, `:608-630` (`BLOCKED` on success, `UNMET`
otherwise); `main()` returns 1 with `"NOT ACCEPTABLE -- outstanding: …"` (`CHK:693-705`). **§4 changes
no line of that file and no printed number.** Whether the reporter may gain a research-closure
criterion set is **D-P20-2** (§6): acceptance/evidence logic is T0 (`PROT/REVIEW_POLICY.md:20`), not a
Lead act (`PROT/AUTONOMY_AUTHORIZATION.md:13`).

---

## 3. B-01 check — does the proposed P0-20 milestone satisfy it? **No.**

**Definition.** B-01 is a WP-P0-13 design-draft blocker, not a P020 deliverable: `DSGN:1441`, heading
"### B-01 — `P020-ACCEPTANCE-AND-CANONICAL-RECEIPT`" (`P13M:288-308`). Controlling text `DSGN:1445`,
quoted `P13M:306-313` (**NV-03**): "WP-P0-13 build cannot begin until WP-P0-20 accepts, and the
canonical receipt issuer/shape is not settled. … B-01 remains open on package acceptance itself, not
on the historical paper verdicts. … Required resolution: accepted P0-20 artifacts plus a re-audit of
this draft before build."

**Stop condition** (`MAP13:83`): "if P020 is not package-accepted, any member/issuer/verifier identity
is absent, or the frozen receipt cannot be independently bound to the completed run, P013 remains
`WAIT_P020_ACCEPTANCE`; only screening lineage and non-accepting preparation may proceed."

**The sources refuse the substitution directly:** "The narrower WP-P0-20 research milestone does
**not** satisfy P013 blocker B-01." (`MAP13:7`); "No narrower milestone presently meets B-01. […] B-01
is deliberately package-acceptance-bearing. Reinterpreting it as component readiness would silently
lower the gate and would let a nonaccepted producer mint full-kernel lineage." (`MAP13:35`); "B-01
cannot be signed closed; it waits for actual P020 acceptance." (`PKT13:208`); "The narrower P020
milestone is not automatically B-01" (`HO/START_HERE.md:42`).

**What B-01 needs that the §4 milestone does not supply:**

1. P020 **package acceptance** at an exact accepted head — "Owner signature does not substitute for
   acceptance." (`PKT13:35`); stop "Anything short of accepted frozen identity" (`PKT13:194`).
2. The **`P020AcceptedCatalogueDependencyV1`** bundle — twelve ordered members incl. `p020_accepted_head`,
   `p020_package_acceptance_receipt_sha256`, receipt schema hash / issuer id / verifier id, allocator
   and kernel import identities (`PKT13:31`).
3. An opaque **`P020VerifiedCanonicalPathResult`** P013 verifies before minting its own non-public
   `FullEvidenceSinkCapability`; "No `ACCEPTED` status label is trusted." (`PKT13:31`).
4. A **settled receipt issuer/shape, then a P013 design re-audit before build** (`MAP13:7`; `DSGN:1445`).
5. The **accepted rejection-taxonomy values** — "B-06 values wait for P020's accepted taxonomy." (`PKT13:208`).

**None exists today.** A grep for the six B-01 seam symbols across `C:/P020_IMPL_20260912` returns
**zero matches** (`P13M:216`); P013's code encodes the open state — "FULL_KERNEL_SIMULATION requires a
verified canonical-path receipt from an accepted WP-P0-20; B-01 is open (WAIT_P020_ACCEPTANCE)"
(`stages_conservation_identity.py:424-428`, quoted `P13M:336`; **NV-04**).

**Conclusion.** §4 is written so that it does not touch B-01. **B-01 remains `NOT SATISFIED`**
(`P13M:327,351`); P013 stays at `WAIT_P020_ACCEPTANCE`.

---

## 4. One recommended scope amendment

Proposed row for `CT13/DECISIONS.md` (four-column shape of `:16-78`), modelled on
`OD-20260913-P012-SCOPE-1` (`:76`). **DRAFT, UNEXECUTED.**

| Decision | Date | Binding summary | Source |
|---|---|---|---|
| **OD-20260913-P020-SCOPE-1** | 2026-09-13 | Narrow WP-P0-20's **current** acceptance object to its reviewed research/engineering deliverable at clean head `b9b72f858dc830a9389517f79da5ea3c1fa6122c`, branch `feature/p020-successor-20260912`: Option 1 zero-minima carrier (authoritative `min_qty`/`min_notional` may be zero; `tick_size`, lot/quantity step and `contract_multiplier` stay positive), the narrow typed `FillDecision.exit_id = TIME_STOP` holding-limit exit, owner-policy binding, and the preregistered benchmark profile-selection procedure once executed. Exact completion label: "P0-20 research/engineering scope complete; package acceptance and production admission pending." Closure preconditions, all OPEN at recording: fresh exact T0 roster on the frozen head; recorded benchmark eligibility outcome; 17/17 enabled REQUIRED control-coverage evidence; current-master reconciliation. `check_p020_acceptance.py` still reports 8/16 MET / NOT ACCEPTABLE and the label does not change that. Authorizes no package acceptance, merge-readiness, production admission, P012 admission, B-01 closure, review waiver or new spend. | Owner chat 2026-09-13; identity `HND:9`; scope `HND:19-20`; reporter `HND:30`; label form per `CT13/DECISIONS.md:76` |

`Binding summary` measured by this lane with a read-only count over the saved file: **1,085 characters**
(ceiling 1,200). Re-measure after any edit.

**Label form.** P012's shape, with `package acceptance` named explicitly because P020's downstream gate
(B-01) is package-acceptance-bearing, not admission-bearing (§3). Precedent: the bounded labelled
`P012_SYNTHETIC_ONLY_NON_PRODUCTION_MILESTONE_V1 — NOT WP-P0-12 ACCEPTANCE` (`AMD:78-85`).

**What the reporter would still say.** Unchanged: `8/16 component criteria MET`, then `NOT ACCEPTABLE
-- outstanding:` the eight names of `HND:40-49`, exit 1 (`CHK:693-705`). **The label is a scope
statement, not a reporter state.**

**Non-authorizations.** No package acceptance or merge-readiness; no P012 state-(i)/(ii) consequence;
no B-01 closure and no change to `WAIT_P020_ACCEPTANCE`; no edit to `CHK` (that is D-P20-2); no review
waiver; no push, PR or merge ("**EXISTING PERMISSION:** None added by this decision.",
`PROT/AUTONOMY_AUTHORIZATION.md:15`); and none of §5.

---

## 5. Retained production restrictions — verbatim, unchanged

1. "No live/production trading, host, credentials, ARM, orders, deploy, PAYG,
   profitability/strategy-quality claim, full grid, 100,000-trial execution, destructive Git, push, PR
   or merge authority." — `HND:23`
2. "Push/PR/merge only under prior standing permission and after package acceptance, required audits,
   up-to-date head, and protected CI green." — `PROT/AUTONOMY_AUTHORIZATION.md:15`
3. "Eligibility is binary only: an actual committed P020 2.1.0 successor trade event exists and ledger
   projection succeeds. Do not expose/compare returns, PnL, ranking or strategy metrics." — `HND:63`
4. "If any trial is non-trade-bearing, return `BENCHMARK_PROFILE_BLOCKED`; no adaptive second selection
   or silent substitution without new owner direction." — `HND:66`
5. "The exact preregistration/fixture must receive the applicable independent T0 review before
   eligibility execution because it controls economic-path evidence." — `HND:68`
6. **All P012 state-(ii) prerequisites stay in force:** "`OPEN-01`..`OPEN-10`, 27 signed risks, five
   residual obligations, Item 4 `NONE_KEEP_REFUSED` and all record refusals unchanged; downstream
   dependencies reconcile individually, production-dependent work stays blocked."
   — `CT13/DECISIONS.md:76`; also `DSN:13`.
7. **B-01 not satisfied; P013 stays at `WAIT_P020_ACCEPTANCE`** — §3; `MAP13:7,35,83`.
8. **The `identity.py` collision must be reconciled before integration** — "**HIGH — active two-writer
   collision today**": P013 `75289fa6…`→`1e9682ba…`, P020 same base→`fa57a771…` (`P13M:407`).
   `mega_walk_forward.py` is a second, already-diverged collision and P013's caller target (`P13M:408`).
9. "Mechanical rows are MET, but package acceptance remains a separate Lead act." — `CHK:704`

---

## 6. Consolidated approval request — only what is genuinely needed

| id | Question | Recommended | Consequence of each option |
|---|---|---|---|
| **D1** (recorded; reference only) | 1D calibration window. Four options at `LANE/OWNER_DECISIONS_PENDING.md:5-12`. | **Option A**: asymmetric window; 1D on rows 2049..2409 (`bc763cd0…`). | As recorded at `:9-12`. Unanswered, the benchmark cannot start, `real_benchmark` stays BLOCKED, the §4 label cannot be claimed. |
| **D-P20-1** | Record `OD-20260913-P020-SCOPE-1` as written in §4? | **Yes, record it.** | **Record:** a truthful label becomes available once the four preconditions are met; nothing downstream moves; the reporter still says 8/16. **Do not record:** work stays under the undifferentiated "8/16 NOT ACCEPTABLE" state and each status report must re-explain the engineering-vs-acceptance gap. **Neither accepts the package.** |
| **D-P20-2** | May `CHK` gain a research-closure criterion set, or does **8/16** stay the reported number under the label? | **8/16 stays; add no criterion set now.** | **Stays:** acceptance surface untouched; label carries scope, reporter carries package truth (`CHK:704`). **Edit:** modifies the module deciding P020 acceptance while six probes are unconditional `BLOCKED` — T0 logic (`PROT/REVIEW_POLICY.md:20`) needing a full fresh roster, and risks a number reading as progress toward acceptance when none occurred (`DRD:320-323`). |
| **D-P20-3** | One-writer assignment for `identity.py` (P013 vs P020, same base blob) and later `mega_walk_forward.py`. | **P020 sole writer of both while WP-P0-20 is active** (`PLAN:489,507`); P013 coordinates. | **Assign:** resolves the collision before it becomes a merge conflict on two protected surfaces. **Leave open:** both branches keep diverging and P013's "shared-path writer collision" stop (`HO/P013_HANDOFF.md:104`) fires at integration. **Not Lead-decidable** — cross-package ownership. |

Nothing else is requested. **B-01 is not an owner checkbox** (`PKT13:225`); §3 shows the sources settle
it. The benchmark procedure is already approved (`CT13/DECISIONS.md:80`) and §5 is already recorded.

---

## 7. Unresolved contradictions

- **D-1** (reused) — `DISP:55-57` says migration waits on "WP-P0-12 reaching this repository";
  `CT13/DECISIONS.md:10` says it arrived via PR #164. Blocker text for two class-C rows. (`DRD:796-802`)
- **D-2** (reused) — `CHK:601-606` blames "additive core changes", names none; `PREP:52,66` and
  `L20/P20P012_COMPAT_FINAL.md:13` say UNKNOWN; `MAP13:30` says "two disclosed P012 probe failures". (`DRD:804-808`)
- **D-3** (reused) — Receipt baseline `e2fd2104…`/core `63f804d9…` (`L20/p012_compat/P012_P020_COMPATIBILITY.json:7,13`)
  vs current G5 core `4698e716…`, so `COMPATIBLE_SYNTHETIC` does not carry forward. (`DRD:810-815`)
- **D-5** (reused) — Five ids for "the nonaccepted candidate"; only `b9b72f85…` is current (`HND:9`),
  which is why §4 pins it. (`DRD:825-832`)
- **NEW D-P20-A** — `PKT13:30` pins B-01's contract to stale head `556639f591…` (`P13M:338-345`); the
  `8/16` conclusion is unchanged (`HND:30`), but a B-01 re-audit must re-pin to `b9b72f85…`.
- **NEW D-P20-B** — `required_control_coverage` MET at 17/17 while "the canonical single run still
  reports nine gaps" (`HND:31`; `L20/STATUS.md:24`); no document reconciles them, hence the §4 precondition.
- **NEW D-P20-C** — `CHK:644-649` and `PLAN:510` require the O-28 (100,000-trial) extrapolation while
  `HND:23` prohibits 100,000-trial execution; no source reconciles the two, so §4 claims only the
  preregistered benchmark, not the full feasibility statement.

---

## 8. NOT VERIFIED

- **NV-01** (reused) — Identities of the two frozen-probe failures: count and cause only
  (`CHK:601-606`); the receipt declines to infer names (`PREP:52`). **Not inferred here**; that class-C
  row cannot close until the names exist.
- **NV-02** — `CHK` was **not executed** (no documented read-only mode). Every criterion *state* is as
  reported by `HND:30,40-49` and `L20/STATUS.md:24`; the clauses (`:659-674`) and `main()` (`:693-705`)
  were read directly.
- **NV-03** — `DSGN:1441-1445`, the primary B-01 definition, was **not read by this lane** (outside the
  brief's source list and this lane's directories); quoted at second hand from `P13M:306-313`. The Lead
  must audit that quotation against the original before B-01 language is used anywhere binding.
- **NV-04** — `stages_conservation_identity.py:424-428` not read directly; quoted from `P13M:336`.
- **NV-05** — No benchmark, test, acceptance run or Git write was performed; the clean-HEAD, 51/25 and
  40-path facts are as recorded at `HND:9,13`, not re-verified.
- **NV-06** — Whether a fresh T0 roster on `b9b72f85…` would PASS is unknown: recorded reviews are on
  `52422017…` (`HND:31-34`); the prose-only repair to `b9b72f85…` was "self-checked as T2 prose under
  current policy" (`HND:35`) — not a fresh T0 result.
- **NV-07** — Recording the §4 row would touch `DECISIONS.md`, which carries a live three-way
  divergence (P013 vs P031 vs CT13 from base blob `4d5c3dfc…`, `P13M:409`). No Git write was made.
- **NV-08** — The 1,085-character count in §4 is this lane's own measurement; re-measure after edits.
- **NV-09** — `L20/STATUS.md` was read only by targeted grep (`8/16`, `NOT ACCEPTABLE`, `benchmark`)
  per the brief; `PREP` and `L20/P20P012_COMPAT_FINAL.md` were used only through quotations already
  carried in `DRD:299-357`. Surrounding context in all three is unexamined.

---

## 9. Citation index

Tokens expand as listed in the header block.

```
HND:7-8
HND:9
HND:10
HND:12-13
HND:13
HND:19-20
HND:21
HND:23
HND:30
HND:31
HND:31-34
HND:35
HND:40-49
HND:51
HND:63
HND:66
HND:68
HND:113
HO/START_HERE.md:42
HO/P013_HANDOFF.md:104
CHK:239-256
CHK:253-256
CHK:594-598
CHK:601-606
CHK:608-630
CHK:633-634
CHK:637-642
CHK:644-649
CHK:651-656
CHK:659-674
CHK:693-705
CHK:704
DISP:3
DISP:55-57
DISP:69
L20/STATUS.md:24
PREP:52
PREP:65
PREP:66
L20/p012_compat/P012_P020_COMPATIBILITY.json:7,13
L20/P20P012_COMPAT_FINAL.md:13
PRE:148
PRE:161
PRE:195-197
LANE/OWNER_DECISIONS_PENDING.md:5-12
LANE/OWNER_DECISIONS_PENDING.md:7
LANE/OWNER_DECISIONS_PENDING.md:9-12
DRD:299
DRD:299-357
DRD:300
DRD:302
DRD:320-323
DRD:796-802
DRD:804-808
DRD:810-815
DRD:825-832
P13M:216
P13M:288-308
P13M:306-313
P13M:327
P13M:336
P13M:338-345
P13M:351
P13M:407
P13M:408
P13M:409
PKT13:30
PKT13:31
PKT13:35
PKT13:194
PKT13:208
PKT13:225
MAP13:7
MAP13:30
MAP13:35
MAP13:83
DSN:13
CT13/DECISIONS.md:10
CT13/DECISIONS.md:16-78
CT13/DECISIONS.md:76
CT13/DECISIONS.md:80
AMD:32
AMD:78-85
PROT/REVIEW_POLICY.md:20
PROT/AUTONOMY_AUTHORIZATION.md:13
PROT/AUTONOMY_AUTHORIZATION.md:15
PLAN:489
PLAN:499
PLAN:504
PLAN:507
PLAN:509
PLAN:510
DSGN:1441
DSGN:1445
stages_conservation_identity.py:424-428
```

---

## 10. Lead audit and recording note (Claude Fable 5.1, 2026-09-13)

- Owner task (chat, 2026-09-13): prepare a concise P0-20 scope/dependency decision packet alongside the approved benchmark work, 30-minute timebox, independent read-only lane, no acceptance change, no waived requirement. Lane ran 11:41Z–12:10Z on the included Max route (54 turns); no Git write, no execution.
- Citation audit: all 95 index entries resolved mechanically with valid line bounds. The two second-hand quotations the drafter flagged (NV-03, NV-04) were verified by the Lead against the originals: `P013_DESIGN_DRAFT_V1.md:1441-1445` (B-01 heading and "WP-P0-13 build cannot begin until WP-P0-20 accepts, and the canonical receipt issuer/shape is not settled") and `stages_conservation_identity.py:424-428` ("B-01 is open (WAIT_P020_ACCEPTANCE)") — both match.
- Lead correction to §7 D-P20-C: not a contradiction. `BENCHMARK_PLAN.json` defines the O-28 figure as "100000 / measured aggregate trials_per_second, clearly labelled estimate only; never execute 100000 trials"; the handoff prohibits 100,000-trial *execution*. The approved benchmark therefore can supply the labelled extrapolation without executing it. §4 remains correct in claiming only the preregistered benchmark.
- Lead note on §7 D-P20-B: the P020 handoff itself explains the pair (17/17 across five mutually exclusive fixtures versus nine gaps in the canonical single run); it is a known evidence-shape limit, not an unreconciled contradiction, and the §4 precondition to re-attest 17/17 under the fresh roster stands.
- Answer to the owner's explicit question: the proposed P0-20 research/engineering milestone does NOT satisfy P0-13's B-01 (§3); nothing in this packet or in the P0-12 amendment changes `WAIT_P020_ACCEPTANCE`.
- Decisions genuinely needed from the owner are D-P20-1 (record the scope amendment row as written in §4), D-P20-2 (leave the acceptance reporter untouched at 8/16 under the label, recommended), D-P20-3 (single-writer assignment for `identity.py` and later `mega_walk_forward.py`), plus the already-recorded D1. They are batched in `C:/tmp/CLAUDE_P0_RUN_20260913/OWNER_DECISIONS_PENDING.md`.
- Recording act: file added under the takeover mirror in the control checkout; ordinary local commit after the Gemini quiet window; no push. No `DECISIONS.md` row is added until the owner answers D-P20-1.
- Source draft preserved unchanged at `C:/tmp/CLAUDE_P0_RUN_20260913/laneP20S_scope_packet/P020_SCOPE_DECISION_PACKET_DRAFT.md` (SHA-256 21a3b2f5dab8e57b1b2dff2f22956b73d9139d6dde5b14c024169c2cec3ddcef).
