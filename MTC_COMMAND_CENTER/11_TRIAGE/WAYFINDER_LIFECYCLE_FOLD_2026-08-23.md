# WAYFINDER LIFECYCLE FOLD — 2026-08-23 (map #54)

**Status:** owner-decision record and plan-amendment pass. Planning only — **implementation authorized: NO.** Per D-12, nothing in this document is an authorization: no store is created, no registry is deleted, no import is run, no package starts because of it.

**What this is.** GitHub map issue [#54](https://github.com/bsemaay-tech/mtc-command-center/issues/54) ("Strategy lifecycle decision map — discovery to retirement, queue 1/8") charted the strategy lifecycle as 12 tickets: 4 AFK research tickets and 7 owner-grilled decision tickets plus this fold task, every one resolved and closed on 2026-08-23 with the owner answering each question personally. This document is the **fold**: it records those owner decisions and carries them into the planning set under the documents' own change control. **The full detail of every decision lives in its ticket's resolution comment; this document indexes and applies, it does not restate.**

**Change-control position.** This fold amends the master planning set as it stands on branch `feature/wayfinder-fold-20260823` (the map #37 fold at `46fb8159`, itself amending the G1-accepted base `764da27f`). **Owner outcome documents are untouched. The requirement count stays 60 = 44 + 16. The work-package count stays 75.** No package is added or removed; amendments land inside existing sections and existing packages' text. One acceptance criterion (**A-18**, §19) is re-worded to name the lifecycle ledger instead of the retired registry file — that is a requirement-text change.

**Materiality statement: these amendments are MATERIAL to the accepted set** (they retire a named registry file from service, re-word an acceptance criterion, declare the sub-live pipeline automatic, and add a designed post-live tail). A fresh G1 acceptance round over the amended documents is recommended before G1-IA is given for any affected package — the same recommendation the map #37 fold carries. Whether and when to run that round is the owner's call, outside this fold.

---

## 1. The seven owner decisions (index — detail lives in each ticket)

| Ticket (resolution holds the detail) | Decision gist |
|---|---|
| [Decide: the canonical lifecycle state machine (#59)](https://github.com/bsemaay-tech/mtc-command-center/issues/59) | One pipeline, two named domains, one door: RESEARCH FUNNEL (`CAPTURED`→`TRIAGED`→`CANDIDATE`→`FROZEN`\|`PARKED`\|`REJECTED`\|`DECLINED`, lifecycle starts BEFORE candidate creation, re-entry everywhere) ⇒ freeze/mint ⇒ EVIDENCE LADDER (`SHADOW`→`TESTNET`→`LIVE_CANDIDATE` auto→`LIVE` via the sole owner signature→tail). Portfolio-fit = parallel evidence lane, not serial step 17. Plan vocabulary is the ONLY lifecycle vocabulary; 7-stage ladder retired via the §4 mapping table; 9 diagnostic labels demoted to tags; `MTC_ENGINE_VALIDATED` dropped as a state. `INTERNAL_PAPER` lane brownfield on the existing Bridge soak-window machinery; ARM/DISARM/KILL named in §6.4. Pre-freeze research permanently navigational. |
| [Decide: the post-live tail — suspension, demotion, retirement, re-entry (#60)](https://github.com/bsemaay-tech/mtc-command-center/issues/60) | Two trigger buckets (automatic-numeric auto-suspends new risk, values [OPEN]; judged-decay is the only thing that pages the owner, via the written four-mechanism checklist). Resume asymmetric: auto below LIVE, owner one-click at LIVE, flap escalation everywhere. DEMOTE = down-ladder same identity, re-live = full gate. RETIRE = terminal for the identity, not the idea. Clock pauses with recorded gap. SUSPENDED = no new entries only; closing is the safety map's FLATTEN. |
| [Decide: lifecycle-state authority — the single source of truth (#61)](https://github.com/bsemaay-tech/mtc-command-center/issues/61) | ONE append-only lifecycle ledger (fresh artifact, working name `LIFECYCLE_LEDGER`) is the sole authority for all state changes funnel→tail; current state always derived. Writers = research-side **Registrar** (funnel) + Environment Admission Authority (automatic sub-live) + Promotion Authority (sole owner signature) + supervisor (tail, act-first-record-mandatory). `PROMOTION_REGISTRY.json` (F-6) and `STRATEGY_REGISTRY.json` retired from service (§3 below). Five scattered stores demoted to legacy display + one-time seed import (§4). "Scorecard" located = the `scorecard_v2` artifact family, bounded as evaluation evidence; `AI_QUANTLENS_VERDICT_REGISTRY` = advisory triage input. Research/planning domain owns the ledger; execution reads fail-closed. Every record names issuer + evidence + identity keys + timestamp; deepest identity per stage. |
| [Decide: the automation boundary below the live gate (#62)](https://github.com/bsemaay-tech/mtc-command-center/issues/62) | Automation of APPLICATION, owner control of DEFINITIONS. Zero manual lifecycle transitions below live. Auto-admission valid only on: frozen+versioned check set, proven-can-fail fixtures (D026), BLOCKED-never-PASS, `check_set_version` in the record. Check-set CHANGES owner-gated under register change control. Notify-after each admission + dashboard feed. No veto machinery (owner demote = veto). Capacity-full → explicit admission-withheld-capacity record. Venue enablement = separate owner-gated infrastructure gate, never a lifecycle state. |
| [Decide: cohort and capacity governance (#63)](https://github.com/bsemaay-tech/mtc-command-center/issues/63) | Shadow uncapped by policy (measured resource guard only). Testnet slot ranking = information value (family diversity > statistical strength > waiting age), rule owner-gated, application automatic, weights [OPEN]. NO preemption — windows sacred. CAPTURED→TRIAGED = versioned owner-gated worthiness checklist (v0.1 draft in §5). Capacity figures measured and published — Bridge V2 map measures on DL-20's dimensions, safety map guards, lifecycle consumes. Operator attention never a required input below live. |
| [Decide: succession for live strategies (#64)](https://github.com/bsemaay-tech/mtc-command-center/issues/64) | Succession = the normal machine run twice. Triggered-only refresh (no calendar cadence). Challenger climbs the FULL ladder as an ordinary candidate; incumbent holds its live slot. Challenge relationship recorded (challenger's records name the incumbent identity). ATOMIC SWAP — one owner signature at the live gate admits the challenger AND closes the incumbent's live window; never two live members of one family. Incumbent demotes to SHADOW as control by default. Position wind-down → bridge/safety maps. §6.6 leakage rules untouched. |
| [Decide: rejection records and re-entry (#65)](https://github.com/bsemaay-tech/mtc-command-center/issues/65) | Rejection record = failed gate + `check_set_version` + `evaluation_run_hash` + each failing check's value-vs-threshold + issuer/timestamp — "would it pass NOW?" is a mechanical input-diff. Five re-entry trigger classes (new data regime / kernel version / substitute catalogue / enrichment modules / owner curiosity); automatic re-screen through `SIGNAL_SCREEN_ONLY`; survivors re-enter `CANDIDATE`; every re-entry a Registrar-recorded event. Pool unbounded. Same machinery funnel-wide (`DECLINED`/`PARKED` own trigger lists). Explorer browses; lifecycle records. |

Research inputs (all closed 2026-08-23): stage inventory (#55), intake front (#56), prior art (#57), state stores (#58) — findings on `research/lifecycle-*` branches under `MTC_COMMAND_CENTER/11_TRIAGE/wayfinder_research/`.

---

## 2. Amendments applied to the brief

All in `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`, each anchored to a unique string, applied by script:

| # | Where | What |
|---|---|---|
| A1 | §6.3 head | Banner: the map #54 ratified reading of the lifecycle — two named domains, `CAPTURED` start, portfolio-fit as a parallel lane (step 17's serial placement abolished), step 21 superseded by the designed tail (§6.9), vocabulary consolidation. Diagram retained as history under the banner. |
| A2 | §6.4 carrier subsection | `INTERNAL_PAPER` carrier declared **brownfield** on the existing Bridge soak-window machinery (`bridge/engine/window.py`); ARM/DISARM/KILL named as the execution interlock (mechanics stay with the safety map). |
| A3 | §6.5 tail | New block "Admission mechanics below the live gate": EAA is an automatic component; the four validity requirements; criteria changes owner-gated; notify-after; no veto machinery; withheld-capacity record + information-value ranking + no-preemption + shadow resource guard; venue-enablement prerequisite; `LIVE_CANDIDATE` = automatic bookkeeping; rejection-record content. |
| A4 | §6.6 rules 6–8 tail | One clarifying sentence: succession rides the computed-leakage machinery; no exception added. |
| A5 | new §6.9 (before section 7) | "The post-live tail, re-entry and succession — ratified macro design": compact normative text for #60, #65, #64 with ticket links. |
| A6 | §11.5 tail paragraph | **Superseded paragraph replaced**: the old text revived `PROMOTION_REGISTRY.json` and kept admission records in a separate store; the ratified design is ONE append-only lifecycle ledger holding all record types, written by the three authorities + supervisor (Registrar added for the funnel), with the atomic-swap signature statement. Loader fail-closed rule unchanged. |
| A7 | §19 A-18 | Re-worded to name the lifecycle ledger's PROMOTED record instead of `PROMOTION_REGISTRY.json` (**requirement-text change — MATERIAL**). Leakage-record clause unchanged. |
| A8 | §17.2b scope | Cross-reference: testnet fleet capacity remains Q17/DL-20 capacity-driven, with slot allocation under the §6.5 cohort rules. |

Verification discipline: every anchor asserted to occur exactly once before replacement; repo-wide grep for changed values after the pass.

---

## 3. Registry retirement — decided, with a declared execution deferral

Ticket #61 retires **`05_REGISTRY/PROMOTION_REGISTRY.json`** (F-6, proven never written: byte-identical SHA-256 across migration manifests, zero code references) and **`05_REGISTRY/STRATEGY_REGISTRY.json`** (zero effective readers) **from service**: nothing may be designed against them, and the lifecycle ledger is minted fresh (working name `LIFECYCLE_LEDGER`; final name settled at implementation).

**Physical deletion is deferred, deliberately, and this is a deviation from the ticket option's literal "old files removed at fold time" wording — declared here rather than done silently.** Two reasons: (1) the dashboard's `read_model.py` `READ_MODEL_FILES` tuple still lists `STRATEGY_REGISTRY.json` — removing the file without the one-line reader change (implementation, D-12-gated) risks breaking a running read path; (2) the migration manifests and the repo file inventory (§18/§21 tables) cite both paths as evidence for F-6 — deleting them mid-plan would orphan recorded evidence. The deletion is an early step of the ledger's implementing package, executed with the reader change, under its own approval.

---

## 4. The one-time mapping table (fold deliverable of #59 and #61)

Specification for the later, separately-authorized seed import. **Governing principle (#59): no retroactive hash blessing — nothing in today's data carries a §6.7 identity, so NO migrated entry may land on the Evidence Ladder. The highest state migration can assign is `CANDIDATE`.** Every seed record is marked `migrated_2026`, carries its source store + source value verbatim, and counts toward no gate.

### 4a. Old 7-stage promotion ladder (`STRATEGY_RESEARCH_REGISTRY.json.current_status`, rules doc §9)

| Old value | New state | Tag added |
|---|---|---|
| `REJECTED` | `REJECTED` (funnel; no evaluation identity — record marked `migrated-no-identity`) | — |
| `KEEP_AS_RESEARCH_NOTE` | `PARKED` | `legacy:research_note` |
| `PROMOTE_TO_SANDBOX` | `CANDIDATE` | `legacy:sandbox` |
| `PROMOTE_TO_FORWARD_PAPER_TRADE` | `CANDIDATE` | `legacy:forward_paper_aspirant` |
| `MTC_ENGINE_VALIDATED` | `CANDIDATE` (state dropped per #59) | `legacy:mtc_engine_validated` |
| `PROMOTE_TO_PARITY_CANDIDATE` | `CANDIDATE` | `legacy:parity_candidate` |
| `APPROVED_FOR_MTC_V2_INTEGRATION` | `CANDIDATE` | `legacy:approved_v2_integration` |

Composite values (`A\|B`) take the row of their highest-ranked component and carry every component's tag.

### 4b. The nine diagnostic labels (rules doc §6) → descriptive tags, never states

`TRUE_ALPHA_CANDIDATE`, `BENCHMARK_BEATER`, `BETA_DISGUISED_AS_ALPHA`, `REGIME_SPECIFIC_EDGE`, `OVERFIT_SUSPECT`, `STATISTICALLY_UNCONFIRMED`, `INSUFFICIENT_TRADES`, `NO_DATA`, `REJECTED` — each becomes tag `label:<lowercased>`. The label `REJECTED` (a classification) is distinct from the ladder value `REJECTED` (a status): as a label it becomes `label:rejected`; only the ladder value maps to the funnel state.

### 4c. Scattered stores — seed disposition (#61)

| Store / field | Disposition |
|---|---|
| `producer_spec.json.promotion_status` (44/63 filled, two independent writers) | Seed via table 4a. Where it disagrees with `STRATEGY_RESEARCH_REGISTRY.current_status`, the seed record is marked `migrated-conflict` and carries BOTH values; neither wins silently. |
| `VARIANT_LOG_REGISTRY.json.promotable` | Tag `legacy:promotable` on the variant's family record; never a state. |
| `TRIAGE_CANDIDATE_REGISTRY.json` (172 candidates) | Funnel seeds: a candidate with a recorded extract-or-decline decision → `TRIAGED`; otherwise → `CAPTURED`. `eligible_for_retriage` becomes tag `legacy:retriage_eligible`. |
| `AI_QUANTLENS_VERDICT_REGISTRY.json.decision` | Advisory tags `advisory:needs_clarification` / `advisory:research_only` / `advisory:salvage`; never states (#61 bounded role). |
| `scorecard_v2` files | Not migrated — they are evaluation evidence artifacts, not state; remain readable in place. |

After the import: no field outside the ledger is authoritative for lifecycle state; the old fields freeze as legacy display until surfaces move to the derived view.

---

## 5. Triage worthiness checklist — v0.1 DRAFT (fold deliverable of #63)

**Owner-gated definition artifact (versioned, like a check set). This v0.1 is a DRAFT for the owner's ratification in the next acceptance round — it binds nothing until ratified.** Applied per idea at `CAPTURED`→`TRIAGED`; verdict + reason recorded by the Registrar.

| # | Criterion (all answerable YES/NO from the capture record) |
|---|---|
| W1 | **Provenance recorded** — source (video/doc/chat) linked; capture date stamped. |
| W2 | **Mechanism stated** — the idea names a cause or edge, not only a result claim. |
| W3 | **Rules extractable** — entries/exits/sizing statable as rules, or the gaps are enumerable in a Missing-Rule Ledger. |
| W4 | **Data reachable** — the needed market/timeframe data exists in-house or via an already-allowed unauthenticated source. |
| W5 | **Kernel expressible** — within the canonical kernel's config space, or the missing module is nameable. |
| W6 | **Not a duplicate** — no existing family covers it (else route as a variant/challenger inside that family, not a new capture). |
| W7 | **No standing disqualifier** — not repaint-dependent, not sub-infrastructure-latency arbitrage, not tied to a venue the venue line forbids. |

Verdict rule (v0.1): W1–W2 both NO → `DECLINED` (reason recorded, re-entry-eligible). Any single NO elsewhere → owner-visible `DECLINED` or `PARKED` per the recorded reason. All YES → extract (`TRIAGED`). Thresholding stays qualitative in v0.1 by design; numbers arrive only with evidence.

---

## 6. Lifecycle-ledger record types (register, macro level — schema belongs to the Explorer map)

Funnel: `CAPTURED`, `TRIAGED`, `DECLINED`, `CANDIDATE`, `FROZEN`, `PARKED`, `REJECTED` (content per #65), `RE_ENTRY` (names its trigger class). Ladder: `SHADOW_ELIGIBLE`, `TESTNET_ELIGIBLE`, `ADMISSION_WITHHELD_CAPACITY`, `LIVE_CANDIDATE`, `PROMOTED` (the §11.5 artifacts, now record types). Tail: `SUSPENDED`, `RESUMED`, `DEMOTED`, `RETIRED` (per #60). Succession: `CHALLENGE` (names the incumbent identity), the swap being a `PROMOTED` record that also closes the incumbent's live window. Migration: `SEED_IMPORT` (marked `migrated_2026`). Every record: issuer, evidence/check consumed, `check_set_version` where a check set applied, identity keys at the stage's deepest depth, timestamp.

---

## 7. What this fold does not do

No store is created; no import is run; no registry file is deleted (§3); no thresholds are set (every number stays [OPEN]); no package is added, started, or authorized; no owner document is edited. KILL/FLATTEN mechanics, venue onboarding, capacity measurement machinery, notification surfaces, and ledger schema/browsing belong to their named neighbour maps. D-12 throughout: a decision is never an authorization.
