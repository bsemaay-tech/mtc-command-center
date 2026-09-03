# Owner decisions — 2026-08-29 evening session

Recorded by the Lead (Claude Fable 5, evening session). Owner verbatim reply to the six-question
message: **"all defaults / increase the number of paralel lanes to 10"**.

The six questions and the defaults the owner thereby adopted:

| # | Question | Ruling (default adopted) |
|---|---|---|
| 1 | P0-11 residual `run_1`/`run_2`/`run_1_sha256`/`run_2_sha256` receipt names | **Repair 8 — label only** now (same class and scope shape as repair 7), then delta audits, then stage 3 |
| 2 | Bridge fail-closed corrected config | **Yes — prepare a corrected `bridge.yaml` candidate** and present it; the owner approves the exact bytes separately before any build uses it |
| 3 | Migration runbook execution | Owner reads the runbook when he has time; the supervised migration run is **scheduled after P0-11 fully closes**; execution still needs his explicit go |
| 4 | P0-11 v3 second-actor rebuild | **Claude Pro** performs the clean-checkout rebuild (different model family from all Codex builders) |
| 5 | Promotion decision package | **Parked** until the owner has reading time; no lane spends on it |
| 6 | Budget (CodeBurn banner at evening session start read $5,186.30 month spend vs the ~$800–1,200 owner ceiling; the Lead measures no USD itself) | **Continue** at current burn; owner explicitly re-confirmed maximum parallel speed |

Additional owner order, same message: **parallel lanes increased to 10.**

## Addendum — later the same evening (owner verbatim: "1. Done / 2. bridge yes / 3. ı have red the files.")

1. **Secondary Codex account re-login: DONE** (Lead probe confirmed "Logged in using ChatGPT").
2. **BRIDGE CONFIG APPROVED:** the owner approves the exact 350-byte
   `BRIDGE_YAML_CANDIDATE_V1.yaml`, SHA-256
   `58f67c8233df8eb92f43be81c09ab665cbe0a17e75b43eccc2f67ad90c040629`, for a later separately
   authorized W10 build targeting schema 4 + paper mode. Per the terms the approval was asked
   under, it takes effect only when the independent candidate audit (lane P21) returns
   CONFIRMED; if P21 finds defects, the candidate returns to the owner instead.
3. **Runbook and promotion package: READ by the owner.** The promotion package still awaits his
   explicit ruling on its single question (approve the report-only rule + vocabulary for the
   four checks; builds nothing; building later is a separate ~18-26 route-hour decision).

Same message thread also ordered parallel design work on P0-13/21/22 (dispatched as drafts,
design-only, serial build chain unchanged).

## Addendum 2 — late evening (owner verbatim: "promotion yes / speed up the godd work. ı want real progress until the morning")

4. **PROMOTION REPORT-ONLY DECISION: APPROVED.** The owner approves the report-only rule and
   vocabulary of `PROMOTION_REPORT_ONLY_DECISION.md`: the four checks (DSR, BH-FDR,
   `robust_final`, positive raw lockbox excess) may be computed and DISPLAYED as
   PASS / FAIL / STOP in a separate report artifact only. Nothing that decides promotion,
   queue placement, or registry status changes. Building the diagnostic display is a separate,
   separately costed future decision (the document's planning estimate: 18-26 route-hours) and
   is NOT authorized by this approval.
5. **Overnight order:** maximum real progress until morning under the standing rules.

## Addendum 3 — 2026-08-30 ~06:00 (owner verbatim: "bridge v2 yes, papers a, p012 hold" / "continue working with 10 lanes. it's not morning yet")

6. **BRIDGE CONFIG V2 APPROVED — exact bytes.** `BRIDGE_YAML_CANDIDATE_V2.yaml`, 324 bytes,
   SHA-256 `a96fecd10d6966c3e93a829ec4d75869a0851f0136a06e85ab45c255ee0f5842`, P21b-CONFIRMED.
   With the design CONFIRMED and the bytes approved, the fail-closed BUILD lane is authorized
   under the standing ask-10 terms: build + tests + PR only; NO deployment to any host.
7. **P0-20 papers: option (a).** The owner's words were "papers a"; option (a)'s content —
   ONE narrowing edit, relabel falsifier #5 a unit-level probe with injected `trail_atr`,
   nothing else — is the Lead's question wording (sourced from N63-F1's minimal correction),
   which the reply adopted.
8. **P0-12 design: HOLD** at its round cap until P0-11 v3 lessons fold in.
9. Ten concurrent lanes remain the standing order.

## Addendum 4 — 2026-08-30 morning (owner answered four questions, all recommended defaults)

10. **Dashboard scope EXTENDED:** the bridge build may repair the three dashboard files
    outside the original design write-set (`bridge/static/app.js`,
    `bridge/static/help_map.json`, `tests/test_dashboard_static.py`) so the dashboard matches
    the fail-closed config. Same branch/PR, auditable.
11. **v3 merge cadence:** after the owner signs, the whole P0-11 package merges to master as
    ONE unit the same day (signature -> final audit pass -> PR -> merge).
12. **Gemini launcher fix AUTHORIZED:** one-line ignore-list addition for the `.impeccable`
    plugin-cache churn in `Invoke-GeminiProReadOnly.ps1`'s integrity check; edit recorded.
13. **Small items:** papers' three open MEDIUMs stay recorded (folded into P0-20's build
    phase later); a 30-minute OpenCode auto-approve investigation is authorized.

## Addendum 5 — 2026-08-30 ~10:55: THE v3 SIGNATURE

14. **P0-11 v3 SIGNED — "Sign with caveat recorded".** The owner, shown exactly what the
    signature attests (evidence integrity of the package at `2eedfb87`: independent
    second-actor rebuild matched 4/4 deciding blob OIDs, 6/6 tool OIDs, 13/13 file SHA-256,
    commit and tree; gate honestly STOP; no claim beyond measurement) and what it does NOT
    attest (no trading readiness, no deployment, no profitability), and shown the one
    recorded caveat (stage-4 design v2f's A-N recipe carries one step not yet literally
    executable by a stranger — wording, not evidence; parking record `AUDIT_N66E_V2F.md`),
    ruled: **sign now, caveat travels inside the signed record.** This addendum row IS the
    owner's signature act of record; the v3 publication artifacts reference it and no code
    issues a signature on his behalf. Per addendum 4 item 11, the package merges to master as
    ONE unit today after the finalization commit passes its final audit.

## Addendum 6 — 2026-08-30 ~11:25 (two standing rules)

15. **Claude MAX auditor fallback:** MAX may run AUDIT lanes when Claude Pro is capped or
    resetting, to keep audit rounds moving. Hard guard: orchestrator survival first — MAX
    lanes share the orchestrator's 5-hour window, so the Lead watches the shared pool and
    pauses/declines MAX lanes before the orchestrator itself risks capping. This amends the
    earlier "MAX = orchestrator only" rule to "orchestrator FIRST, auditor fallback under the
    pool guard."
16. **Per-session LLM assessment ledger (permanent rule):** every session, the Lead writes
    its measured route/model performance assessment to
    `MTC_COMMAND_CENTER/11_TRIAGE/LLM_ROUTE_ASSESSMENTS.md` (append-only, newest first) so
    route knowledge accumulates instead of dying with the session.

## Addendum 7 — 2026-08-30 ~13:15 (owner verbatim: "p012 round 4 fıll unlock")

17. **P0-12 FULL UNLOCK.** The hold is lifted. Authorized as one chain without further owner
    gates until the merge report: design round 4 (folding the P0-11 stage-3/v3 lessons and
    the parked N57b findings) -> full 4-family re-audit -> on PASS, the CORRECTED_VNEXT
    kernel BUILD starts under the owner's standing 2026-08-29 word ("P0-12 kernel approved",
    build-after-P0-11-accepts — P0-11 merged today as PR #143) -> build audit rounds -> PR ->
    merge. Fail-closed at every audit: a BLOCK at any stage parks and returns to the owner.
    Owner-gated numeric thresholds remain [OPEN]-marked, never invented.

## Addendum 8 — 2026-08-30 ~14:30 (owner verbatim: "p012 round 5")

18. **P0-12 round 5 authorized:** bounded union repair of exactly the round-4 verification
    findings (N72's six — 4 BLOCKER, 2 HIGH — plus P35's nits), then re-verification under
    the same fail-closed clause (clean -> build proceeds under the addendum-7 unlock;
    not clean -> re-park to owner). Owner-gated thresholds stay [OPEN]; nothing invented.

## Addendum 9 — 2026-08-30 ~17:05 (owner verbatim: "p012 loop to clean, cap 8" + widen to ~10 lanes with more startable packages)

19. **P0-12 repair loop STANDING:** repair->verify rounds run autonomously until the
    detection auditor finds zero required findings (then the build proceeds under the
    addendum-7 unlock) or round 8 completes (then hard park regardless). One owner report at
    the end: clean or parked. All other rules unchanged (no invented values; owner-gated
    thresholds stay [OPEN]).
20. **Parallel design-ahead widened:** the owner orders ~10 lanes and authorizes design-stage
    starts on further packages. Started as DESIGN/DRAFT-ONLY (no build, chain intact):
    WP-P0-20 build design, WP-P0-30 design, WP-P0-31 Milestone-2 design, WP-V2A-02 design,
    plus audit/fold rounds on the existing draft fleet.

## Addendum 10 — 2026-08-30 ~17:20 (owner verbatim: "promotion build / P0-16/17 stay parked / out 2 hours, keep lanes busy")

21. **Promotion report-only diagnostic BUILD authorized** — exactly the build the approved
    decision record defines (`PROMOTION_REPORT_ONLY_DECISION.md` §9): compute DSR, BH-FDR,
    robust_final and raw lockbox excess per candidate and emit the PASS/FAIL/STOP report
    artifact. Everything in that decision's untouched column stays untouched (gate scorers,
    queue, registries, schemas, historical labels); missing inputs produce STOP, never
    fabricated values. Build + tests + audit round; PR after audit.
22. **P0-16 / P0-17 remain V-NEXT parked** (owner re-confirmed).
23. **Autonomous window ~2h** — standing rules apply; owner-gated items park and wait.

## Addendum 11 — 2026-08-30 ~19:50 (owner verbatim: "p012 narrow")

24. **P0-12 gate-claim NARROWING authorized:** the design's acceptance gate stops claiming
    total absence of undocumented behavioural differences (unprovable by finite machinery —
    the 8-round record is the evidence) and instead claims exactly what the machinery proves:
    the eight corrections' RULE-2 divergent behaviours, plus equality on the enumerated
    comparison surfaces, with the enumeration itself published and reproducible. One
    narrowing round (folding the N78 parking findings under the narrowed claim) + ONE verify
    pair. Pre-written rule: detection-clean -> the build proceeds under addendum 7;
    otherwise FINAL PARK, no further rounds under any standing authorization.

## Addendum 12 — 2026-08-30 ~21:50 (owner handoff order for the NEXT session)

25. **Standing routing for the next session (refines addendum 6 item 15):** Claude MAX
    **Fable = orchestration only**; Claude MAX **Opus = audit + coding lanes**; hard guard —
    the shared 5-hour MAX window must never fill enough to block Fable (orchestrator survival
    first: pause/decline Opus lanes before Fable risks capping). Routes in play: 4 Codex
    accounts, Grok, Gemini, OpenCode Go subscriptions; OpenRouter API if needed. Ten
    parallel lanes standing. Per-package time spent written to the relevant ledgers
    (N_TIMES.txt + hours file + status-feed session_time_report + Wayfinder hours CSV);
    dashboard files (WP_PACKAGE_STATUS.json + Wayfinder session folder) kept current.

## Addendum 13 — 2026-08-30 ~21:30 (owner verbatim: "P0-12 decision fresh familit")

26. **P0-12 FRESH-FAMILY DESIGN AUTHORIZED.** A model family OTHER than Claude authors a
    completely fresh CORRECTED_VNEXT design (not a repair of v1.8), using the full 10-round
    defect record (N45..N82, parking record `DETECT_N82_P012_V18.md`) as its failure-mode
    specification. Same fail-closed chain terms as addendum 7: design -> full multi-family
    audit round (author family EXCLUDED from auditing its own design; detection by a
    different family) -> on detection-clean PASS the kernel build proceeds under the standing
    2026-08-29 kernel approval -> build audits -> PR -> merge; a BLOCK at any stage parks and
    returns to the owner. Owner-gated numeric thresholds remain [OPEN], never invented.
    Executes in the NEXT session (this one is closing).

## Interpretation notes (Lead) — these notes refer to the ORIGINAL six-question table rows
above (its rows 1, 2 and 6), not to the addendum numbering (6-9); addendum 3's rulings
supersede row 2's "preparation only" edge for the bridge (the bytes are now approved and the
build authorized) and answer row 6's budget question for the night.

- Ruling 1 authorizes exactly the repair-7 pattern: rename the published labels that assert
  unperformed acts, sweep the class by shape, rerun the existing probe, full tests green,
  one commit. Nothing beyond the label class.
- Ruling 2 authorizes PREPARATION only. The candidate file and its per-key rationale go to the
  owner; his approval of the exact bytes (hash-pinned) is a separate future decision, and the
  build lane starts only after that approval.
- Ruling 6 is recorded as the explicit owner answer to the standing budget flag
  (model-routing ceiling); the flag remains open as a fact, closed as a question.

## Addendum 14 — 2026-08-31 ~09:05 (owner verbatim answers to the P0-12 precondition package v2 + session rules)

27. **P0-12 precondition rulings** (answers to
    `11_TRIAGE/P012_BUILD_PRECONDITIONS_OWNER_DECISIONS_2026-08-31.md`, given as
    "1a, 2a, 3a, 4a, 5a"):
    - **Q1a:** ONE bounded design repair fold (DS15-F01 MEDIUM + DS15-F02..F05 as
      [OPEN]-respecting text) + ONE detection re-verify round, explicitly authorized past the
      consumed D028 cap.
    - **Q2a:** "P0-11 accepted" MEANS the owner-signed merged package (PR #143, addendum-5
      signature). Clarification folds into the design; the runnable legacy subject and sealed
      baseline bytes remain precondition-3 obligations.
    - **Q3a:** an AI lane from a non-implementer family (Claude; implementer family is Codex)
      MAY satisfy the CONTRACT_TABLES "person other than the kernel implementer" independence
      role, named in the ledger. Section-16 human review stays with the owner.
    - **Q4a:** ONE bounded legacy-kernel run to freeze BASELINE_BYTES is authorized, ONLY
      after Q3's sealed scenario catalog exists. Results frozen to files; no other execution.
    - **Q5a:** the Lead posts the exact protected T0 kernel-path list + the Gate-2 implementer
      plan in chat; the owner's "approved" on that message is the explicit T0 path grant and
      Gate-2 acceptance trigger. (Not yet given as of this addendum.)
    - **Q6:** OPEN-01..10 dispositions PENDING — plain-language one-pager (self-audited, A4
      9/9 folded) delivered to the owner ~09:40; answers expected same day.
28. **P0-31M1 (7a):** stays TERMINAL-PARKED at v1.4. No fresh-family redesign, no scope
    change, no hold-review.
29. **Wayfinder rev-12 (8a):** the FINAL_CLOSEOUT record is accepted AS RECORDED, including
    the two stale machine fields A3 found; no rev-13 correction attempt.
30. **BUDGET RULING (owner verbatim intent):** "subscription budget is not a problem, I pay
    fixed subscription anyway... my goal is to increase this number not decrease it." High
    subscription utilization is the GOAL. Never throttle subscription lanes for cost;
    pay-as-you-go API routes remain cheapest-suitable. Supersedes the standing budget-flag
    concern for subscription routes; the CodeBurn banner stays report-as-fact.
31. **Session stop time:** 17:00 with full handoff + report.

## Addendum 15 — 2026-08-31 ~10:00 (owner verbatim: OPEN-01..10 dispositions via audited one-pager v2)

Owner's verbatim reply (one-pager numbering, mapped to design rows):
"1 STOP_FIRST, 2 no additional bounds, 3 schema approved, 4 a, 5 Hyperliquid perp BTC from
current doc + venue fetch approved, 6 draft it, 7 i, 8 draft it, 9 draft it, 10 read approved"

32. **OPEN-02** = `STOP_FIRST` is the mandatory same-bar policy for acceptance-bearing 2.0.0 runs.
33. **OPEN-08** = "no additional bounds" — explicit no-additional-bound decision per the design's
    closure column.
34. **OPEN-09** = protected-scope approval GRANTED for the additive result/event schema
    (sections 13-15, gross/net PnL + lifecycle linkage). The separate build authorization
    remains the Q5a "approved"-on-path-list act (addendum 14, not yet given).
35. **OPEN-10** = (a): guards keep GROSS-MINUS-FEES (D017 extended to 2.0.0) for daily-loss,
    consecutive-loss, and time-stop; no per-control divergence requested. RED/GREEN guard
    fixtures per control are a build obligation under this rule.
36. **OPEN-01** = first production instrument is HYPERLIQUID PERPETUAL BTC, effective window
    from the current venue document onward. **VENUE FETCH APPROVED** (verbatim): read-only
    retrieval of the venue's public documents, frozen with digests, nothing else. Record +
    digest package returns for a later one-word owner approval.
37. **OPEN-03** = "draft it": complete event-role fee table (maker/taker per fill-event class,
    exact venue schedule/rounding/minimum) drafted from the fetched venue schedule for later
    owner approval.
38. **OPEN-04** = (i): explicit ZERO-SLIPPAGE base (the design-sanctioned option). No invented
    non-zero parameter; a measured model remains possible later by separate decision.
39. **OPEN-05** = "draft it": funding mechanics (position-snapshot rule, same-timestamp
    ordering, mark-price source, positive-rate payer) drafted from fetched venue
    documentation/history for later owner approval.
40. **OPEN-06** = "draft it": the retained/retired execution-behavior proposal (already
    drafted PROVISIONAL as W126, under audit A6) goes to the owner to confirm or amend;
    owner's later naming closes the row with its migration fixtures.
41. **OPEN-07** = "read approved": READ-ONLY schema read of the Bridge v6 funding ledger is
    authorized for the field-by-field mapping draft; no Bridge write, no deploy, no runtime
    contact. Mapping returns for owner approval.

Lead note: rows 32-35 + 38 are decision-complete (evidence = this record; fixtures/JSON are
build obligations). Rows 36-37/39-41 are decision-named with evidence packages in
preparation; each closes only on the owner's later approval of its prepared package. All ten
transcriptions go verbatim into `open_item_applicability.json` at build start under Gate 2.

## Addendum 16 — 2026-08-31 ~13:05 (owner verbatim: "all approved, fees a, design a, retain all.")

Given in reply to the Lead's consolidated ask (venue bundle post + pending-words list, whose
stated composite example this reply exactly follows). Interpretations recorded with the ask's
own definitions:

42. **"all approved"** closes/grants:
    - **OPEN-01 CLOSED:** InstrumentRecord candidate v1.3 APPROVED (Hyperliquid linear perp
      BTC; min_notional $10 verbatim; step 0.00001 derived; price rule verbatim; remaining
      honest opens: minimum_quantity none-published, §16 human review at build acceptance).
      Evidence: `P012_OPEN01_INSTRUMENT_RECORD_V1.md` v1.3 + candidate JSON + frozen-bytes
      manifest (5 fetches, digests).
    - **OPEN-05 CLOSED:** funding rules v1 APPROVED (hourly 1/8 of 8h rate; spot oracle
      price; snapshot at interval end; positive rate = longs pay shorts).
    - **OPEN-07 CLOSED:** Bridge v6 funding-ledger mapping v1.1 APPROVED as the field-by-field
      closure evidence; the 16/18 unmapped fields and the deployed-v4 non-materialization are
      RECORDED INTEGRATION OBLIGATIONS, not silently waived.
    - **T0 BUILD-PATH GRANT GIVEN:** the owner's "approved" applies to the posted, A7-cleared
      Gate-2 plan v2 path list (`P012_GATE2_PLAN_AND_PATHLIST_V1.md` v2): protected T0 write
      authority for the listed kernel paths only, subject to the remaining preconditions and
      Lead Gate-2 acceptance; no out-of-list file, no git/merge/deploy/venue/trading authority.
43. **"fees a" — OPEN-03 CLOSED:** fee table v1.1 APPROVED with option (a): stop-triggered
    entries use Stop Market semantics (taker). Proposed role mapping adopted: market
    entries/exits = taker; TP/SL = taker (venue text: automatically market orders); base
    tier-0 schedule (perps taker 0.045%/maker 0.015%) with tier/staking alternatives
    transcribed.
44. **"design a" — residual disposition:** ONE bounded micro-fold authorized, scope EXACTLY
    G46-F01 (KERNEL-probe conservation, minimal correction as stated in
    `DETECT_G46_P012_V13.md`) + DS18-F01 (tie-break coverage) + P47-F01 (carry-forward LOW
    nit), followed by ONE terminal detection pass (Grok + Gemini). No further design work
    without new owner word.
45. **"retain all" — OPEN-06 CLOSED (dispositions):** every `[OWNER CHOICE]` row of
    `P012_OPEN06_RETAINED_RETIRED_PROPOSAL_V1.md` v2 is RETAIN (P01, P02, P03, P05, P06,
    P07, P08, P09, P10, P11, P12, P13, P14, P15, P16, P17, P18, P24, P25, P26). Mechanically
    forced rows stand as recorded: P04 RETIRE (pre-final-fill construction), P19 RETIRE
    (close-triggered stop) under the approved always-active-stop correction, P20 RETAIN
    (gap/intrabar stop mechanism), P21 RETIRE (implicit collision policy). P22 = explicit
    STOP_FIRST (owner's OPEN-02 word). P23 recorded not-applicable-under-STOP_FIRST. Every
    row's migration fixture is a build obligation.

Lead act recorded with this addendum: **Gate-2 ACCEPTED by the Lead** (implementer plan v2,
A5 audit folded + A7 re-check zero findings; acceptance checklist adopted). Chain now:
micro-fold + terminal pass -> CONTRACT_TABLES (Claude, Q3a) -> open_item_applicability.json
+ sealed bundle -> ONE legacy baseline run (Q4a) -> kernel build on the granted paths.

## Addendum 17 — 2026-08-31 ~15:05 (owner verbatim: "include")

46. **OPEN-05 same-timestamp snapshot eligibility = INCLUDE.** A position whose fill lands at
    the exact funding-payment timestamp COUNTS for that payment (`position_snapshot_rule`
    same-timestamp choice). This closes the one residual the decision-file audit (G56-F02)
    surfaced: the venue text is silent; this is the owner's economic ruling, distinct from
    the design's deterministic row-order rule (which orders already-eligible events only).
    Funding scenarios with a boundary-timestamp fill are now buildable; the RED/GREEN
    fixture for the boundary case is a build obligation under this rule.

## Addendum 18 — 2026-08-31 ~17:20 (owner verbatim: "RECOMMENDED: keep the two test cases as designed")

47. **D-12 RESOLVED = (a):** the two synthetic RULE2-06 test cases keep their design-declared
    `TARGET_FIRST` input (their purpose is to prove the machinery + tie-break for that
    policy). OPEN-02's `STOP_FIRST` remains the mandatory policy for all acceptance-bearing
    2.0.0 production runs. No table or design change needed; the sealed bundle stands.

## Addendum 19 - 2026-08-31 ~18:45 (owner verbatim: "1a")

48. **P0-12 INPUT-EMBEDDING ADDENDUM AUTHORIZED (option 1a).** Context: W152 input
    materialization honestly blocked 0/17 - design v1.4 states every economic vector value
    but not the mechanical embeddings a runnable input file needs (complete Bar arrays,
    existing-position/target-book premise seeds, the RULE2-01-GREEN NaN wire encoding,
    synthetic test-only CostSchedule values for fill-bearing scenarios). Same gap classes
    the sealed CONTRACT_TABLES recorded as blocked cells (DERIVATIONS D-01..D-05); third
    independent fail-closed stop; the one authorized baseline run remains unconsumed.
    The owner's "1a" authorizes: ONE bounded design addendum (v1.4 -> v1.5) binding ONLY
    the missing mechanical embeddings (no approved economic value changes; economic-bearing
    additions only where design/owner-approved sources exist, otherwise honest [OPEN-EMBED]
    rows), followed by a detection pass, a CONTRACT_TABLES revision + re-seal by the tables
    family, input materialization, digest-pin, dry-run, THE ONE baseline run (Q4a
    unchanged), then the kernel build - continuing tonight without further owner gates
    except the standing sec-16 human review at build acceptance.

## Addendum 20 - 2026-08-31 ~20:55 (owner verbatim: "1a 2a 3a 4a 5a")

49. **OPEN-EMBED-01..05 CLOSED** (the five embedding questions design v1.5 honestly
    refused): (1a) omitted initial equity = 1000 for RULE2-03/04/05/06 families;
    (2a) RULE2-04 entry basis/fill = 100 via the candidate entry/BE path;
    (3a) RULE2-06-EQUAL-PRICE equal-target book is constructed by the corrected (2.0.0)
    target-book test machinery directly - legacy engine untouched, scenario recorded
    honestly as not-runnable-on-legacy for that book; (4a) RULE2-08-RED pre-event entry
    basis/fill = 100; (5a) RULE2-08-GREEN closed-lifecycle premise built with ordinary
    price bars before the observation window (real mechanism, nothing injected).
    These are test-only values under design section 5's synthetic-vector rule; production
    records remain governed by addenda 15-17 evidence packages.

## Addendum 21 - 2026-09-01 morning (owner verbatim: "amendment approved")

50. **P0-12 GATE-GAP AMENDMENT AUTHORIZED.** Context: the kernel build (14 commits)
    reached its authority boundary - the corrected-vs-golden gate stopped on design-gap
    classes the independent G76 adjudication enumerated. The owner's word authorizes ONE
    bounded design amendment (v1.5 -> v1.6) binding EXACTLY: the decision_events
    vocabulary and container shape (D-11/G76-09); the equity-curve window scoping rule
    (V15-D02/G76-04); the fill/exit/result/refusal member sets (D-13/G76-06/07/08); the
    funding-in-guard member disposition (G76-05c) - PLUS one detection pass, the tables
    family's re-derivation of exactly the affected golden classes (including removal of
    the adjudicated GOLDEN-OVER member max_consecutive_losses, G76-05b), and the Lead's
    re-seal of the revised goldens and the 10 probe-row digests. No other design section,
    no approved economic value, and no kernel behavior outside the already-adjudicated
    classes may change. Chain then: probes DETECTED -> terminal receipt (sec-16-only
    refusal) -> 4-family T0 audits -> PR. Sec-16 human review remains the owner's act.

## Addendum 22 - 2026-09-01 ~10:00 (owner verbatim: "Fix all four, then re-check")

51. **P0-12 TERMINAL MICRO-FOLD AUTHORIZED - SCOPE EXACTLY FOUR FINDINGS.** Context: the
    v1.6 -> v1.7 amendment fold (W166B) repaired 12 canonization-bias findings from the
    G78 + GM28 union, but the terminal pass did not come back clean. G79 (grok) verified
    all 12 repairs and raised one new HIGH of the same class; the planned second arm
    (GM29, gemini) failed twice at invocation with zero output - route down, recorded as
    an honest absence, NOT as a pass - and a third family (DS35, opencode/deepseek, on a
    section-23 extract) was substituted. DS35 confirmed the HIGH at three sites, found no
    new sibling of that class, and raised three further findings. The repair budget
    written before the W166B round was spent, so nothing was repaired without this word.
    The owner's word authorizes ONE further micro-fold (v1.7 -> v1.8) binding EXACTLY:
    G79-F01 = DS35-F01 (FUNDING_ELIGIBILITY unlabeled canonization row, three sites);
    DS35-F02 (unenumerated `collision` receipt inside the closed COLLISION_RESOLVED
    decision); DS35-F03 (tables-revision item 1 names a kernel-family removal set the
    tables family cannot satisfy); DS35-F04 (cumulative_funding presence condition
    unstated-as-rule and in tension with tables item 6) - followed by an independent
    re-check. No other design row, no repo/golden/kernel/catalog/seal byte, and no third
    repair round: the pre-written stopping rule is that the re-check must return zero on
    the four repaired rows AND zero new findings of the canonization class, or the residue
    parks again unrepaired for the owner. The two residuals G79 recorded as
    harmless/out-of-union are deliberately left untouched and named as such.

## Addendum 23 - 2026-09-01 ~11:10 (owner verbatim: "Authorize now, run in parallel" / "Prepare a plain-language brief now")

52. **P0-20 RECONCILIATION ROUND AUTHORIZED, PARALLEL.** Context: the three P0-20 documents
    were authored before the fresh P0-12 design was sealed, so N107-F02 (the allocator vs
    ExecutionEconomics seam) and N107-F03 (cost-registry byte-incompatibility, JCS/second-root
    and pending-slippage mechanics) describe superseded mechanisms. W161 folded 12 of the 14
    N107 findings and left exactly these two as DISPUTED-NEEDS-DECISION; W162 repaired the
    three G74 fold-residuals; the final zero-pass was deferred to this round by budget
    discipline. The owner's word authorizes one reconciliation round, running in parallel with
    the P0-12 chain, binding EXACTLY those two disputes and their consequences across the
    build design, the control-parity checklist, and the statistical battery definition. The
    method is retain-and-tag, not delete-and-rewrite (the G74 over-fold lesson), every banner
    re-pointed post-fold, and any passage whose reconciliation would require a mechanism the
    P0-12 design does not state becomes an honest `[OPEN-P020-n] NEEDS OWNER DECISION` row
    rather than an invented reconciliation. No repository byte, code, run or acceptance.

53. **V2A-01 B1 PROPOSAL: OWNER BRIEF AUTHORIZED, NOT ADOPTION.** Probed, not recalled: the
    proposal ends with TEN owner questions and states that until they are answered it is a
    design proposal and not an adopted schema - so "adopt or reject" was not an available
    shape. The owner's word authorizes one lane that converts those ten into a plain-language
    decision brief (question in one sentence, why it is asked, two or three options with what
    each makes impossible later, cost expressed only as revision rounds and re-opened
    artifacts with NOT MEASURABLE where unmeasurable, a labeled recommendation, and an
    explicit deferrable-or-blocking verdict per question). Question 3, which asks the owner to
    name a record type and writer for eight inputs that have no current producer, must be
    reshaped into a yes/no per input rather than an authoring task. The brief authorizes no
    adoption, no draft edit, and no repository write.

## Addendum 24 - 2026-09-01 ~11:30 (owner answers to the four [OPEN-XV] rows)

54. **[OPEN-XV-05] CLOSED - option A** (owner: "No - it must prove it, so define the owner
    now"). The runtime-wiring package may NOT be called finished without proving that two
    strategies cannot double-spend one bucket. A dedicated cross-worker headroom owner is
    therefore authorized to be DESIGNED: principal identity, process cardinality, lease or
    claim rule, durable store, restart rule, and recovery source. None of those exist today,
    so this word authorizes the design act, not an invented mechanism folded in passing; the
    per-worker lease may never be promoted to cross-worker authority.

55. **[OPEN-XV-06] CLOSED - option A** (owner: "The lifecycle ledger's view"). The lifecycle
    ledger's reducer is the single writer of evidence-window truth including the retired
    identity mark; the loader reads only that view at load time; per-worker rows remain local
    projections and are never load-time truth. Honest consequence recorded: the loader's
    revoke branch stays a non-emitted placeholder until the M1 ledger package is un-parked -
    this decision unblocks the DESIGN of that branch, not its probes. It does not close the
    separate out-of-scope row for who marks the old worker file.

56. **[OPEN-XV-07] CLOSED - option A** (owner: "Keep failing closed for now"). The loader keeps
    its fail-closed hold: no version, range, compatibility rule, or fingerprint preimage is
    invented now. Recorded consequences: the ledger-view fingerprint may not be recorded as a
    canonical success value, and the later ledger-growth package stays unconsumable by this
    loader until the owner separately authorizes the round that writes the compatibility rule
    and a fingerprint not poisoned by the rebuild clock.

57. **[OPEN-XV-12] CLOSED - option A** (owner: "amend the official plan to add the
    dependency"). "The same implementation demonstrably runs in backtest and runtime" is
    ruled to mean a worker from the worker-identity package. The canonical delivery plan is
    therefore to be AMENDED so the runtime-wiring package's dependency list carries the
    worker package, rather than the design silently adding the edge. The plan is a repository
    file: the amendment is prepared as an exact quoted before/after edit and applied by the
    Lead on a branch under the repo guard, never by a lane.

    Consistency check performed before recording: 54 and 57 reinforce each other (the
    two-worker fixture stays in the wiring package and that package now honestly waits for
    the worker package); 55 and 56 reinforce each other (trust the ledger view, refuse
    whenever its shape cannot be verified). No contradiction found among the four.

## Addendum 25 - 2026-09-01 ~13:00 (owner answers on B1 and the two P0-20 rows)

58. **B1 - SEVEN DECISIONS CONFIRMED AS A BLOCK** (owner: "Confirm all seven as recommended").
    Each of the seven follows a rule already ratified in the repository, and the brief quoted
    the controlling text for every one: (1) the shared deployment-identity definitions belong
    to the contracts package, not to a downstream consumer; (2) the three existing shapes are
    accepted as shapes, with construction staying blocked until each has a named writer,
    because a schema-only home is not an operational producer; (3) the eight missing facts are
    dispositioned as four routed to obvious owners and four honestly acknowledged as having no
    current single writer and therefore staying blocked - approving this is accepting that
    split, not inventing four names; (4+5, merged) the preparer and the confirmer must be two
    different parties or the independent check is one source in two files, with the admission
    authority as the confirmation writer; (7) a broken package description gets its own refusal
    label rather than borrowing the identity-mismatch label, which would be false while the
    twelve identity inputs are unchanged; (8) the environment-impact declaration belongs to the
    component's own schema per the canonical brief; (10) ship as a NEW contracts version
    co-deployed with v0.1.0 under the already-ratified refuse-mismatch rule, with the exact
    version number deliberately NOT chosen yet. Two loose ends remain open by design: which
    existing research package owns final frozen-package assembly (a fact to be found, not
    decided), and the version number, which the final change set fixes.

59. **B1 #9 - NO SIGNATURE REQUIRED** (owner: "No - outside the threat model"). A compromised
    ledger store, or a compromised operator of it, is ruled OUTSIDE the threat model the loader
    must detect. The accepted trust boundary is therefore two separate writers plus append-only
    history. Recorded consequence: the project may never later claim that the loader
    independently verifies the ledger against a key or an external trust root. Reversing this
    would require designing key ownership, issuance, rotation, revocation, verification and
    failure handling - none of which exists in any document read.

60. **[OPEN-P020-1] and [OPEN-P020-2] - DELIBERATELY HELD** (owner: "Hold - decide when P0-20
    is actually built", both). How the P0-20 allocator requirements enter the single economics
    seam (new seam version versus separately approved adapter), and whether P0-20 retains any
    non-authoritative registry or index responsibility, both stay open rows. Recorded
    distinction that matters: these are now OWNER-SEEN AND DEFERRED, not unnoticed gaps. The
    reconciliation's existing wording already carries them honestly and no document change is
    required; the P0-20 build inherits both as declared undecided boundaries.

## Addendum 26 - 2026-09-01 ~17:30 (owner verbatim: "Every decision actually made")

61. **W167-D04 CLOSED - READING Y.** Context: the v1.8 tables re-derivation surfaced two live
    readings of the design giving materially different `decision_events` arrays on eight of
    seventeen golden rows. The tables family executed the narrow reading (the work instruction
    addressed to it at design `:1178-1181`) and RECORDED the alternative rather than guessing.
    The independent family (G83) opened both cited spans, ruled the design does not settle it -
    **GENUINELY AMBIGUOUS - OWNER MUST DECIDE** - returned **NOT SAFE TO SEAL**, and explicitly
    warned against defaulting to the narrow reading to keep the chain moving. The owner's word
    selects the broad reading: a `decision_events` row is required for every closed reason whose
    named decision is **actually evaluated** on that scenario, even where the prior tables
    artifact never carried that reason (design `:1033-1034` applies to the tables family on its
    own terms). The anti-padding clause continues to bind - a reason is emitted because its
    named decision was evaluated, never to equalize row counts.

    Consequences recorded before the work: eight goldens are re-derived
    (RULE2-01-RED/GREEN, 05-RED/GREEN, 06-RED/GREEN, 06-EQUAL-PRICE-RED, 07-RED); the kernel
    delta `:1211-1212` already tells the kernel to emit on occurrence, so this reading makes the
    two families agree rather than requiring a kernel-instruction amendment; two named exceptions
    survive (RULE2-05-RED takes `MIN_NOTIONAL_ADMITTED` but not `SIZING_COMPUTED` because
    W167-D05 is real on that row; RULE2-05-GREEN may take `SIZING_COMPUTED`). No economic value
    moves; if any Reading Y addition appeared to require moving a sealed economic value, the lane
    is instructed to STOP that row and report rather than proceed.

62. **RECORDED, NOT YET A DECISION - the frozen-package composer has no owner.** The B1
    decisions 4+5 the owner confirmed in addendum 25 require the party that PREPARES the package
    description to be different from the party that CONFIRMS it. The lookup lane returned
    **NO EXISTING PACKAGE OWNS THIS**, quoting the proposal's own admission that no current
    package is assigned that writer. This is an honest gap, not an oversight to be filled by
    nominating a plausible package; it becomes an owner decision when B1 moves to adoption.

63. **PR #146 MERGED** - the addendum 24 [OPEN-XV-12] plan amendment is now on `master`. The
    repo guard blocked the first branch as stale and was not overridden; a fresh branch off
    `master` was used instead and passed.

## Addendum 27 - 2026-09-01 ~17:55 (owner verbatim: "Treat as leftover - authorize one targeted fix")

64. **G84-F01 - ONE TARGETED FIX AUTHORIZED.** Context: G84 verified the W171 one-fold and
    returned the P0-20 checklist (v1.8) and battery (v1.5) CONVERGED, with the build design
    (v1.4) NOT CONVERGED on a single remaining HIGH. The untagged section-5.1 R-2
    acceptance-evidence row still keys evidence on registry membership and ends "Unregistered
    cost model -> BLOCKED evidence, not a number", which reads as a second record-identity gate
    that P0-12 v1.8 supersedes (record identity is the exact file bytes with a detached digest).
    W171 had tagged the sites G82 named but not the neighbouring table. Under W171's pre-written
    stopping rule the round PARKED rather than folding a third time. The owner ruled it a
    leftover and authorized ONE targeted repair: retain the wording verbatim, tag it superseded
    in the same form used on the neighbouring sites, and state the controlling P0-12 rule beside
    it. Explicitly not authorized: any second sweep, any other passage, and any closure of
    `[OPEN-P020-1]` or `[OPEN-P020-2]`, which remain owner-held per addendum 25.

65. **PER-LANE HOURS RECORDING ADOPTED** (owner: "start recording per-lane hours"). Attribution
    is declared at dispatch in a lane registry; timing is measured from each lane's own
    artifacts; a running lane reports a blank duration rather than an estimate. Today's backfill
    from real timestamps: 13 completed lanes, 175.4 lane-minutes (2.92 lane-hours), attributed
    WP-P0-12 60.5, WP-P0-20 60.0, cross-V2A 31.1, WP-V2A-01 23.8. The standing rule is
    unchanged and now enforced in the tool itself: where nothing was measured the dashboard
    keeps printing NOT RECORDED, and that is never to be "fixed" by supplying a number.

66. **LANE PARALLELISM RAISED ON OWNER WORD** (owner: "can you increase the number of parallel
    lanes now?"). Raised from 2 to 5 with work genuinely off the serial kernel chain: the
    owner-authorized XV-05 shared-headroom design act, the section-16 human review aid that
    makes the owner's own un-delegable review performable, the B1 proposal fold, and this
    targeted P0-20 repair. Honest limit recorded: the kernel work is a chain (design seals ->
    answers derive -> re-seal -> code runs), so lanes added to it do not shorten it.

## Addendum 28 - 2026-09-01 ~21:25 (four decisions taken to unblock the night shift)

67. **v1.9 TOKEN AMENDMENT APPROVED** (owner: "Approve - add the names to the design"). Context:
    the sealed goldens assert sixteen tokens, spellings and fixed strings the design never names;
    the kernel is forbidden to invent them, so zero of seventeen gate rows could reach MATCH. The
    alternative - stripping them from the goldens - was costed by the tables' own family and then
    INDEPENDENTLY RE-DERIVED by a second family which confirmed every stuck item and found no
    self-interested misread. The amendment proposal was checked by a third family that authored
    neither the tables nor the proposal and returned SOUND AS DRAFTED. The owner's word authorises
    design v1.8 -> v1.9 naming exactly those tokens, with the eight SEMANTIC ADDITIONS recorded as
    such rather than as clerical spellings, and the four DO-NOT-NAME recommendations honoured.
    Consequence recorded: the tokens already committed by the capped kernel lane become
    LEGITIMATE rather than requiring revert - the G90 revert instruction is superseded by this
    word, not overruled by the Lead.

68. **RULE2-05-RED: THE ROUNDING RULE GOVERNS - QUANTITY ZERO** (owner: "The rounding rule -
    quantity zero"). Two design sections disagreed: section 7 floors the calculation to zero while
    section 11 and the 22.5 scenario binding declare requested quantity 1. The golden deliberately
    withheld the value rather than guess (W167-D05). The owner rules section 7 controls.
    Consequence: the sealed golden for that row currently carries the section-11 outcome and must
    be re-derived by the tables family, followed by a Lead re-seal - this is a golden change and
    only the tables family under this owner word may make it.

69. **SECTION-16: THE UNCERTIFIABLE ITEM IS AN ACCEPTED RESIDUAL RISK** (owner: "Accept as a
    documented known risk"). Whether the engine handles fees, funding and a same-bar stop/target
    collision together cannot be certified by human code review by anyone, because no test covers
    that case. It is STRUCK from the owner's code-correctness list and recorded openly as an
    accepted residual risk; the owner signs the remainder honestly. The gap is written down, not
    hidden, and the review document must say so in terms.

70. **P0-31 MILESTONE 1 UNPARKED FOR REPAIR** (owner: "Yes - authorize the repair round"). Two
    independent passes agree all three terminal HIGH findings are DOCUMENT defects, not design
    defects - the design already contains the answers and the text fails to state them. This
    authorises a bounded fold round on those three findings only. It does not authorise a fresh
    design act, does not accept the milestone, and does not unblock the packages behind it, which
    still require M1 to be accepted.

## Addendum 29 - 2026-09-02 morning (owner answers Q1 and Q2 of the P0-12 gate; Q3 deliberately held)

71. **LIFECYCLE TRADE ROW: EXIT ID LIST ONLY** (owner: "A. Exit ID list only"). Context: the P0-12
    gate stands at 13/17 with four DESIGN-GAP rows; design v1.9 requires `RESULT_SURFACE.trades[]`
    but never closes the member set (`P012_FRESH_DESIGN_V1.md:480`, `:1130-1139`). The sealed
    answer sheets disagree with each other: RULE2-04-RED and RULE2-07-RED carry a single
    `exit_fill_price`, while RULE2-06-RED, RULE2-06-EQUAL-PRICE-RED and RULE2-06-GREEN carry an
    `exit_ids` list, which is also what the kernel emits (`core/results.py:702-728`). The owner rules
    that every completed trade row has exactly: `entry_fill_price` (quantity-weighted over entry
    fills), `quantity`, `exit_ids` (in exit-event sequence order), `gross_realized_pnl`,
    `fee_total`, `funding_total`, `net_trade_pnl`. No `exit_fill_price` member; per-piece exit prices
    live only in the closed `exit_events[]` schema. A trade that exits in several pieces is ONE row
    whose `exit_ids` lists every piece in sequence order. Consequence: RULE2-04-RED and
    RULE2-07-RED goldens must be re-derived by the tables family to this shape, design v1.9 must be
    amended to close the member set, then a Lead re-seal (#8). Kernel unchanged by this decision.
    Rejected: B (add a quantity-weighted average exit price, engine change plus all five sheets),
    C (one row per exit piece, changes trade meaning and profit aggregation).

72. **ALL-TOUCHED EXIT RECEIPT ORDER: STOP FIRST, THEN TARGETS AS DECLARED** (owner: "A. Stop
    first, then targets as declared"). Context: `COLLISION_RESOLVED.touched_exit_ids` is a receipt
    of every stop/target touched in the bar; the design fixes the CHOSEN execution order
    (`P012_FRESH_DESIGN_V1.md:339-353`) but gives no order for the receipt (`:1035`). The kernel
    lists candidates in declared order with the stop first; the two RULE2-06 RED sheets list targets
    first and the stop last. The owner rules the receipt order is the scenario's declared
    exit-candidate order, stop first, then targets in declaration order. This never changes which
    exits execute, their prices, or PnL. Consequence: RULE2-06-RED and RULE2-06-EQUAL-PRICE-RED
    goldens must be re-derived by the tables family (`touched_exit_ids` becomes
    `["STOP","TARGET-NEAR","TARGET-FAR"]` in both), design amended to state the rule, then Lead
    re-seal (#8). Kernel unchanged by this decision. Rejected: B (targets first, stop last),
    C (UTF-8 byte order of `exit_id`), D (price order along the bar).

    **Q3 deliberately held.** The canonical gate refuses with `BASELINE_SEAL_IDENTITY_MISMATCH`
    because the frozen reference results predate the re-sealings. Decisions 71 and 72 change the
    sheets again, so the owner is asked once, after re-seal #8, whether to re-generate the reference
    results or let the frozen ones stand. That is a decision to execute a run and is his alone.
    Until then the refusal stands: no skip flag, no manifest edit, no baseline clearing.

73. **EXECUTION AUTHORIZED FOR DECISIONS 71-72** (owner: "Yes, authorize" / "Yes, run after re-seal
    #8"). Authorises, in the build worktree only: design v1.9 -> v1.10 amendment closing the trade-row
    member set and the receipt order; the tables family re-deriving the four goldens named in 71 and
    72 under protected scope `MTC_V2`; Lead re-seal #8; and one gate rerun after that seal. It does
    not authorise a kernel edit, a repository master change, clearing the canonical gate's baseline
    refusal, or regenerating the frozen reference results (Q3, still held).

74. **GROK NOT TOPPED UP FOR NOW** (owner: "Not now"). The grok route stays out of balance (402
    Payment Required since 2026-09-02 02:41). The review pool is three families - Codex, Claude,
    Gemini/OpenCode. Recorded as a spend decision; it costs independence on four-way checks, not
    speed. Revisit when a fourth opinion is needed.

75. **REGISTER GAINS A FIFTH STATE: "in repair"** (owner: "Add 'in repair'"). Context: the
    dashboard labels ten packages "design converged" although they were re-examined overnight and
    are now under repair; the register's four states have no word for that. The owner adds one
    state word. Consequence: a small change to the register and its dashboard reader, with the
    reader checked to render the new value rather than blank; the ten affected rows move to the
    new state only after that check. Nothing else in the register changes under this word.

76. **Q3: REGENERATE THE FROZEN REFERENCE AGAINST SEAL #8** (owner: "Regenerate against seal #8").
    Context: the canonical P0-12 gate refuses with `BASELINE_SEAL_IDENTITY_MISMATCH` because the
    BASELINE_BYTES reference was frozen before eight re-sealings of the contract tables; the gate
    rerun on seal #8 (W246) measured 15/17 row-by-row with two KERNEL-SHORT rows (equity-curve
    ordered-addition grouping, `core/results.py:790-811` vs design `:1070-1078`). The owner
    authorises ONE baseline regeneration run in the build worktree against seal `4ebcdfc5ad42`,
    after the two engine fixes land and are verified, followed by the canonical gate. No skip flag,
    no manifest hand-edit: the refusal clears only because the reference and the seal agree. This
    is a decision to execute a run and is recorded as the owner's.

    *Lead correction to the decision-76 consequence note, same day:* the sequencing "after the two
    engine fixes land" was the Lead's inference, not the owner's word. The baseline driver runs the
    LEGACY kernel from the master worktree (`C:\WFMERGE54`, core tree `c7f4aa1b`), which the build
    worktree's fix does not touch, so the regeneration is independent of the engine fix and runs in
    parallel. The owner's word stands as given: regenerate against seal #8, one run.

77. **ONE MORE REFERENCE REGENERATION, AGAINST SEAL #10** (owner: "Yes, regenerate against seal
    #10"). Context: re-seal #10 pinned the ten probe artifact digests and the v1.11 design into the
    contract tables (only the catalog's PROBE rows and the derivations worksheet moved; every golden
    and input is byte-identical to seal #8), which moves `EXPECTED_SEAL_SHA` to `d763f62f9a42...`.
    The reference regenerated under decision 76 consumed seal #8, so the canonical gate refuses on
    identity again. The Lead did not foresee this when the probe rows were re-derived; recorded as
    the Lead's miss. The owner authorises ONE run of the legacy baseline driver against seal #10,
    same inputs and same master-branch legacy kernel as decision 76; the run must prove every
    scenario surface byte-identical to the seal-#8 archive and may differ only in recorded identity.
    No skip flag, no manifest hand-edit.

## Addendum 30 - 2026-09-02 ~17:1x (owner arbitration and standing order for the next 16 hours)

78. **THIS SESSION CONTINUES; THE FORK IS RELEASED** (owner: "1. This session"). Two interactive
    Lead sessions were live on one bundle; the fork (`tradingview-lab-clean-50`) froze on request
    and rewrote the next-session handoff on the owner's /handoff order. The owner keeps the day
    session (`tradingview-lab-clean-21`) as Lead. The fork writes nothing further.

79. **STANDING ORDER ADOPTED** (owner: "2. yes", confirming the order first given to the fork):
    (a) the owner will hand over answers to all 41 Phase-0 decisions; use them to close every ready
    package and start as many packages in parallel as they unlock; (b) run the maximum number of
    parallel lanes, an idle route needs a reason; (c) routing: Claude MAX Fable = orchestration
    only; Opus on MAX may audit but must never fill the shared 5-hour window enough to lock the
    orchestrator; **Claude Pro first** for audit and coding lanes; the Codex accounts, Grok,
    OpenCode Go and Gemini as auditors AND coders; (d) a 16-hour work plan with goals at session
    start, updated every 2 hours. Grok's balance is still 402 as last probed; using it requires the
    owner's top-up (decision 74 said not now; this order lists it - the Lead probes before use and
    does not spend on it without a live balance).

80. **KERNEL FIX AUTHORIZED FOR THE THREE FLAGSHIP-1 DEFECTS** (owner: "Yes, fix the three",
    2026-09-02 ~17:4x). Flagship audit 1 (Codex, W276) of the P0-12 engine branch returned BLOCK
    with W276-F01 HIGH (runtime equity state accumulates cash with a different association than
    the design's ordered rule; the serializer's ordered recomputation masks it), W276-F02 MEDIUM
    (DEF-P012-08 funding dedupe keyed by event id instead of `(funding_event_id, lifecycle_id)`),
    W276-F03 MEDIUM (missing production funding events raise `TypeError` before the typed refusal
    `REFUSED_MISSING_FUNDING_EVENT`). The owner authorises one bounded kernel lane in the build
    worktree for exactly those three, each with a failing-then-passing test, legacy replay
    byte-exact, verified by a different family; flagship 2 (W279) and the Gemini detection lane
    then judge the result; the pull-request question follows only after that.

81. **KERNEL FIX AUTHORIZATION EXTENDED TO FLAGSHIP-2'S FOUR ENGINE DEFECTS** (owner: "Yes, all
    seven in one authorized lane set", 2026-09-02 ~17:5x). Flagship audit 2 (Claude Pro, W279)
    returned NOT READY with twelve findings [CORRECTED addendum 31: 22 findings, F01-F22]; four are engine defects of the same class as decision
    80's: W279-F09 (funding events outside the strictly-between-bars window silently dropped, no
    eligibility row, no refusal), W279-F08 (`position_snapshot_rule` echoed but never implemented;
    `interval_boundary_convention` never read), W279-F11 (corrected entry path does not apply the
    capital/margin admission check the legacy path applies), W279-F12 (`PROTECTIVE_STOP_EVALUATED`
    and `COLLISION_RESOLVED` emitted only for LONG positions; decision 72's receipt order not
    enforced). W279-F10 duplicates W276-F02. Same conditions as decision 80: failing-then-passing
    test per item, legacy replay byte-exact, different-family verification, both flagships and the
    detection lane re-run on the result before any pull-request question. Harness findings
    (W279-F01, F03, F04, F05, F07; F02 = the receipt binding already under repair) proceed under the
    standing build authorization and need no further word.

## Addendum 31 - 2026-09-02 19:2x REAL (owner: 41 Phase-0 answers, verbatim; GO to the overnight prompt with all defaults)

Source: the owner's answers message of 2026-09-02 ~19:0x (recorded verbatim in
`C:\tmp\LANE_PROMPTS_20260828\OWNER_ANSWERS_41_2026-09-02.md`) and his `GO` of 19:2x REAL to
`PROMPT_OVERNIGHT_2026-09-02.md`. His rule on the answers message, applied: the V1.2 recommended
answers were proposals only; each row below records the basis kind of the recommendation it
rests on (DOCUMENT / CURRENT-SYSTEM / PRECEDENT / JUDGEMENT); nothing was implemented, built,
committed or pushed from that message; this entry and the fold lanes start on the GO. Rows map
1:1 to `OWNER_PHASE0_DECISIONS_V1.md` V1.1 (row N = decision 81+N). An owner answer needs no
basis kind: it IS the authority; the basis kind describes the recommendation, not the decision.

**Correction to decision 81:** it says flagship 2 (W279) returned "twelve findings"; the report
enumerates 22 (F01-F22: 7 HIGH / 9 MEDIUM / 6 LOW). The four engine items named there (F08, F09,
F11, F12) and "F10 duplicates W276-F02" are correct; only the total was wrong (found by DS102).

### The 41 answers (decisions 82-122)

_Answer first: 1-7 (P0-20 rows 1-5; P0-13 rows 6-7)_

82. **Row 1** (owner verbatim): "Use 1% risk per trade and no leverage. Let each strategy set its own data-freshness limit, no longer than its trading interval. Do not invent the separate stop-loss ceiling: bring that back to me as a separate decision." - recommendation basis: CURRENT-SYSTEM (1 % risk, leverage cap 1.0 from `config.py`); loss-at-stop left OPEN by the owner - **new owner decision to be scheduled**.
83. **Row 2** (owner verbatim): "Ratify the existing exam settings: DSR 0.95, BH-FDR 0.10, at least 30 trades, final 25% held back, with at least 1,500 bars. Call this exam version 1. Leave CPCV and PBO limits open for now, and measure skew and kurtosis properly." - recommendation basis: CURRENT-SYSTEM (values in `mega_walk_forward.py`); CPCV/PBO stay OPEN.
84. **Row 3** (owner verbatim): "Retire and freeze the two old simulators. Do not rebuild them." - recommendation basis: DOCUMENT.
85. **Row 4** (owner verbatim): "Put the portfolio simulator inside P0-20, but keep it research-only." - recommendation basis: JUDGEMENT (gates P0-20 acceptance per `P020_BUILD_DESIGN_V1.md:956`).
86. **Row 5** (owner verbatim): "Use my normal PC as the reference machine. A 100,000-trial run may take one overnight period. Measure the whole chosen grid and report the middle result and the slower-end result." - recommendation basis: JUDGEMENT.
87. **Row 6** (owner verbatim): "Use a combined quality rule, not one score. Keep the top 20 per strategy, market, and timeframe; also keep the best risk-versus-return group, promoted items, robust items, and anything I pin." - recommendation basis: DOCUMENT.
88. **Row 7** (owner verbatim): "Keep settings for every saved trial." - recommendation basis: DOCUMENT.

_P0-21 (rows 8-14)_

89. **Row 8** (owner verbatim): "Decide the formula for measuring data gaps before choosing a gap limit. Use the first real scan to propose the number, and use a 24/7 calendar for BTC perpetual data." - recommendation basis: JUDGEMENT.
90. **Row 9** (owner verbatim): "Require at least 30 trades for every strategy and timeframe." - recommendation basis: CURRENT-SYSTEM (`MIN_TRADES_FOR_PASS = 30`).
91. **Row 10** (owner verbatim): "Initially allow no trade to lose more than its declared stop-loss risk. Revisit this after real gap data is measured." - recommendation basis: JUDGEMENT.
92. **Row 11** (owner verbatim): "Do not set a backtest-versus-live drift limit yet. First publish the measured drift from the first shadow period." - recommendation basis: JUDGEMENT.
93. **Row 12** (owner verbatim): "A missing required safety control may allow shadow testing only; it blocks all higher stages. Informational controls are allowed only when listed openly." - recommendation basis: DOCUMENT.
94. **Row 13** (owner verbatim): "Require both: an internal paper period of 8-16 weeks, at least 30 new trades, and no unexplained breaks; plus separate exchange-testnet proof. Neither replaces the other." - recommendation basis: DOCUMENT (`brief:725,1366,1369`).
95. **Row 14** (owner verbatim): "Adopt the written eligibility checklist as version 1." - recommendation basis: DOCUMENT.

_P0-14 (rows 15-16)_

96. **Row 15** (owner verbatim): "Keep all dashboard colours grey for now." - recommendation basis: DOCUMENT.
97. **Row 16** (owner verbatim): "Show incomplete screening results, but label every tile SCREEN ONLY and hide the detailed report." - recommendation basis: DOCUMENT.

_P0-22 (rows 17-22)_

98. **Row 17** (owner verbatim): "Treat every trial from one approved search-space version, for one strategy, as one family. Do not invent arbitrary parameter buckets." - recommendation basis: JUDGEMENT.
99. **Row 18** (owner verbatim): "Accept conservative over-marking for now. Do not add new record-keeping machinery yet." - recommendation basis: JUDGEMENT.
100. **Row 19** (owner verbatim): "Use one shared UTC clock; allow no hidden clock difference." - recommendation basis: JUDGEMENT.
101. **Row 20** (owner verbatim): "Require an independent clock for access logs." - recommendation basis: JUDGEMENT.
102. **Row 21** (owner verbatim): "Prevent unlogged copying or reading of results by building a proper boundary. This is costly, so record that cost openly." - recommendation basis: JUDGEMENT.
103. **Row 22** (owner verbatim): "Bind the screen's displayed result window directly to its recorded window." - recommendation basis: JUDGEMENT.

_P0-30 (rows 23-28)_

104. **Row 23** (owner verbatim): "Use "bar interval plus 15 seconds" for aging and "bar interval plus 45 seconds" for stale data. Do not set a recovery limit yet. Mark these as a judgement based on illustrative values, not measured proof." - recommendation basis: JUDGEMENT (owner marks it so himself).
105. **Row 24** (owner verbatim): "If data falls back to slow polling and the strategy gives no instruction, stop." - recommendation basis: DOCUMENT.
106. **Row 25** (owner verbatim): "Create one shared rate-limit coordinator. Until it exists, run the collector as one process only." - recommendation basis: PRECEDENT (decision 54 shape).
107. **Row 26** (owner verbatim): "Store market data by month." - recommendation basis: JUDGEMENT.
108. **Row 27** (owner verbatim): "For 15-minute data, warn when only 40 days of venue history remain. Measure the other timeframes before setting their limits." - recommendation basis: JUDGEMENT (illustrative 40-day figure; `P030_DESIGN_DRAFT_V1.md:120-124`).
109. **Row 28** (owner verbatim): "Start only with Hyperliquid BTC perpetual on 15m, 1h, 4h, and 1d intervals." - recommendation basis: PRECEDENT.

_P0-31 Milestone 1 (rows 29-33)_

110. **Row 29** (owner verbatim): "Commission the ledger's own registrar to issue its writer credentials. Keep the authority small and inside the accepted trust boundary." - recommendation basis: JUDGEMENT.
111. **Row 30** (owner verbatim): "Accept milestone 1's refusal proof now, but record that a successful path still must be demonstrated after decision 14." - recommendation basis: JUDGEMENT.
112. **Row 31** (owner verbatim): "Add real tests for simultaneous writing and backup recovery." - recommendation basis: JUDGEMENT.
113. **Row 32** (owner verbatim): "Include a read-only ledger view in milestone 1." - recommendation basis: DOCUMENT (`plan:425`).
114. **Row 33** (owner verbatim): "Use an independent reviewer from a model family that did not author or build the item being reviewed." - recommendation basis: PRECEDENT (design 15.1 / owner Q3a).

_P0-31 Milestone 2 (rows 34-41)_

115. **Row 34** (owner verbatim): "Map the four old unknown labels to CAPTURED, while keeping each original label as a visible tag." - recommendation basis: JUDGEMENT.
116. **Row 35** (owner verbatim): "For composite old statuses, use the highest-ranked status under the written ladder." - recommendation basis: DOCUMENT.
117. **Row 36** (owner verbatim): "For an array of labels, use the lowest-ranked label; keep every label as a tag. Missing labels stay CAPTURED and are marked missing." - recommendation basis: JUDGEMENT.
118. **Row 37** (owner verbatim): "Import all old triage-registry entries as CAPTURED, with a tag that they may be reviewed again later." - recommendation basis: JUDGEMENT.
119. **Row 38** (owner verbatim): "When two sources disagree, mark the record migrated-conflict, keep both values, and let neither win silently." - recommendation basis: DOCUMENT.
120. **Row 39** (owner verbatim): "Do not grandfather old status. No imported record may automatically become higher than CANDIDATE." - recommendation basis: DOCUMENT.
121. **Row 40** (owner verbatim): "Add the small independent refusal test rather than claiming an unproven refusal." - recommendation basis: JUDGEMENT.
122. **Row 41** (owner verbatim): "Do not import scorecards as lifecycle records. Leave them readable as evidence where they are." - recommendation basis: DOCUMENT.

### GO answers to the overnight prompt (decisions 123-125)

123. **KERNEL SCOPE = ALL 14** (owner: "GO", item A default). The seven kernel defects not covered by
    decisions 80-81 are authorized under the same conditions: W279-F06 (HIGH, test constructor with
    override fields inside `mtc_v2/core`), W279-F13 (nine `1e-12` tolerances vs exact-binary64),
    W279-F16 (fee `cash_event_id` from the fee counter), W279-F18, F19, F20, F21 (LOW). NOT covered
    by this GO: the kernel half of W279-F17 (`_state_refusals` cannot emit the four members named
    at design 23.4:1215; exposed when W284-5 removes the harness override) - the Lead had written it
    into this decision by mistake, W293 (Codex secondary check) caught it at 19:44, corrected here;
    it is a separate owner question. Conditions: failing-then-passing test per item, legacy replay
    byte-exact, different-family verification, both flagships and the detection lane re-run on
    the result before any pull-request question. Lane W285 after W283.
124. **PROBE-COPY WHITESPACE STAYS** (owner: "GO", item B default). The whitespace diagnostics inside
    the ten pinned probe copies (W276-F06 = W279-F22) are immutable evidence: left untouched,
    recorded as known and excluded from the hygiene check. The ordinary self-test blank line
    (`test_corrected_config.py:87`) is repaired regardless. [Note 20:4x: this
    sentence was in the Lead's restatement of item B that the owner answered "GO" to, not in the
    prompt text itself; DS103 (second-family check) flagged the difference. The DS102 merged ledger
    recommended it; owner-visible, no value moves.]
125. **SECTION-16 SIGNATURE AFTER THE RE-AUDITS** (owner: "GO", item C default). The owner's
    section-16 review is not spent tonight; it follows the kernel and harness fixes and the
    re-run of both flagships plus detection on the fixed branch.

126. **W279-F17 KERNEL HALF AUTHORIZED** (owner verbatim: "kernel half, yes", 2026-09-02 19:5x REAL,
    answering the Lead's question after W293 removed it from decision 123). The engine's refusal
    writer (`mtc_v2/core/results.py:755-771`, `_state_refusals`) may be changed so it can emit the
    four members named at design 23.4 `:1215`; W284-5 removing the harness override exposes the
    gap. Same conditions as decisions 80, 81, 123: failing-then-passing test, legacy replay
    byte-exact, different-family verification, both flagships and detection re-run before any
    pull-request question. Lane W285 item 7b, one commit.

Notes carried from the answers file: row 1 opens a NEW owner decision (the separate loss-at-stop
ceiling, `brief:1334`, `[OPEN]`) - scheduled, not set; rows 2, 8, 11, 23, 27 deliberately leave a
value open or defer it to a measurement - folds write `OWNER-DEFERRED-TO-MEASUREMENT`, never a
number; row 30's "decision 14" means row 14 (the checklist v1), not ledger decision 14; row 33
ratifies the family rule already binding (design 15.1, Q3a); row 21 requires an explicit cost line
with a source, no estimate without one.

## Addendum 32 - 2026-09-02 ~19:5x-20:0x REAL (owner amendment replacing rows 1, 6, 9, 13 of addendum 31; owner verbatim "1. confirm 2. launch original")

The owner sent the amendment below at ~19:5x with the rule "Record these as proposed owner
amendments. Do not change code, start a build, run tests, commit, push, trade, or treat this as
live-trading permission. Leave every other owner decision unchanged." The Lead recorded it verbatim
outside the ledger (`C:\tmp\LANE_PROMPTS_20260828\OWNER_AMENDMENT_ROWS_1_6_9_13_2026-09-02.md`),
restated its reading, and the owner answered "1. confirm" (this entry) and "2. launch original"
(the fold lanes for P0-20 and P0-21 run first on the addendum-31 text of rows 1, 9, 13, exactly as
the P0-13 lane already running on row 6; a second fold then layers this amendment on each,
retain-and-tag, nothing deleted). Decisions 82, 87, 90 and 94 are SUPERSEDED by 127-130 below;
their text stays in addendum 31 for the record. No other decision changes. Nothing here authorizes
live trading, a build, or a kernel change.

### Owner's amendment, verbatim

> OWNER DECISION ADDENDUM — replaces only decisions 1, 6, 9, and 13
>
> Record these as proposed owner amendments. Do not change code, start a build, run tests, commit, push, trade, or treat this as live-trading permission. Leave every other owner decision unchanged.
>
> 1. Risk and leverage
>
> Risk per trade and leverage must be adjustable, versioned policy settings.
>
> Keep the current settings only as initial research defaults; they are not permanent limits. I may raise or lower risk later through a recorded policy version and a new evidence run.
>
> Leverage is permitted only when a strategy explicitly declares its approved maximum leverage. There must be no unrestricted global leverage. The exact leverage cap may differ by strategy type and instrument, but it must be recorded before that strategy can use it.
>
> Keep the stop-loss ceiling as a separate decision. Do not automatically derive it from the risk-per-trade percentage.
>
> Each strategy sets its own data-freshness limit, no longer than its trading interval.
>
> Any change to risk, leverage, or stop-loss settings creates a new policy version and requires fresh relevant evidence. This does not authorize live trading.
>
> 6. Selecting and retaining winners
>
> Do not choose winners using one score alone. Require all safety and quality checks first, then rank by overall robustness.
>
> Keep the best 20 candidates separately for each strategy type—for example, day trading, swing trading, and position trading—so one type does not crowd out another.
>
> Keep any tied candidates at the cut-off as well.
>
> 9. Minimum trade evidence
>
> Do not require the same 30-trade minimum for every strategy type.
>
> Keep 30 trades as the starting rule for day-trading strategies. For swing-trading and position-trading strategies, prepare separate minimum-evidence rules that reflect their slower trade frequency.
>
> For slower strategies, backtest evidence may carry more weight, but it must pass the full quality, robustness, and data checks. Forward or testnet evidence confirms operational behaviour; it does not need to produce 30 trades before the strategy can be evaluated.
>
> Do not label a strategy live-ready from backtest evidence alone. Record each strategy-type rule as a versioned policy and apply it consistently.
>
> 13. Forward and testnet evidence
>
> Rework the forward-evidence rule by strategy type. Do not require every strategy to wait 8–16 weeks.
>
> For day-trading strategies, use a shorter forward-testing period because they generate evidence faster. Require a meaningful number of real forward trades, no unexplained reconciliation problems, and evidence across more than one normal market condition.
>
> For swing-trading and position-trading strategies, allow a longer calendar period and place more weight on robust backtest evidence because trades happen less often.
>
> Keep internal paper testing and separate exchange-testnet proof as two different requirements; neither replaces the other.
>
> No strategy becomes live-ready from a short forward test alone. The final time and trade requirements must be written as separate, versioned rules for day, swing, and position strategies.

### Decisions 127-130 (each = the owner's numbered section above, verbatim authority)

127. **ROW 1 SUPERSEDED (was decision 82): risk and leverage are adjustable, versioned policy
    settings.** Current 1 % risk / leverage 1.0 = initial research defaults, not permanent limits;
    leverage only where a strategy explicitly declares a recorded approved maximum (no unrestricted
    global leverage; cap may differ by strategy type and instrument, recorded before use); stop-loss
    ceiling stays a SEPARATE decision (still open, decision 82's note stands), never derived from
    risk-per-trade; per-strategy data-freshness limit no longer than its trading interval
    (unchanged); any change = new policy version + fresh relevant evidence; not live-trading
    permission.
128. **ROW 6 SUPERSEDED (was decision 87): winners are not chosen by one score.** All safety and
    quality checks first, then rank by overall robustness; keep the best 20 separately per strategy
    TYPE (e.g. day, swing, position) so no type crowds another out; keep ties at the cut-off.
129. **ROW 9 SUPERSEDED (was decision 90): minimum trade evidence differs by strategy type.** 30
    trades stays the starting rule for day-trading strategies; swing and position strategies get
    separate minimum-evidence rules reflecting slower trade frequency (values not given: folds write
    OWNER-ANSWERED-SHAPE, VALUE PENDING); for slower strategies backtest evidence may carry more
    weight but must pass the full quality, robustness and data checks; forward/testnet evidence
    confirms operational behaviour and need not produce 30 trades before evaluation; no strategy is
    labelled live-ready from backtest alone; each strategy-type rule is a versioned policy applied
    consistently.
130. **ROW 13 SUPERSEDED (was decision 94): forward and testnet evidence rules are per strategy
    type.** Not every strategy waits 8-16 weeks; day-trading: shorter forward period, a meaningful
    number of real forward trades, no unexplained reconciliation problems, evidence across more than
    one normal market condition; swing/position: longer calendar period, more weight on robust
    backtest evidence; internal paper testing and separate exchange-testnet proof remain two
    different requirements, neither replaces the other; no strategy becomes live-ready from a short
    forward test alone; final time and trade requirements are separate versioned rules for day,
    swing and position (values not given: VALUE PENDING).

## Addendum 33 - 2026-09-02 ~20:1x REAL (owner routing amendment, Turkish, translated)

131. **CLAUDE MAX = ORCHESTRATOR ONLY; NO AUDIT LANES ON MAX** (owner, 2026-09-02 ~20:1x, in Turkish:
    "Claude MAX credits started draining very fast after moving to Fable 5.1. Use Claude MAX only
    as orchestrator. Use Codex, Gemini, OpenRouter/Go as auditors"). Supersedes the audit-class
    allowance for Opus-on-MAX in decisions 79 and the addendum-30 standing order: from this word
    no lane of any kind runs on the MAX subscription; Fable orchestrates only. Auditors and
    verifiers: the Codex accounts, Gemini, OpenCode Go (DeepSeek/GLM/Kimi) and OpenRouter PAYG
    per OD-20260829-2. Claude Pro (separate subscription) remains a coding/audit route under
    decision 79. The V283b lane on MAX Opus was stopped at 20:1x; its report had already landed
    and is used.

## Addendum 34 - 2026-09-02 ~22:0x REAL (owner verbatim: "q1 yes")

132. **BASELINE REGENERATION AFTER THE PROBE RE-PIN AUTHORIZED** (owner: "q1 yes", answering plan
    rev 6 Q1). The nine KERNEL probes pin the pre-fix `mtc_v2/core` tree OID; after the authorized
    kernel repairs the gate refuses them with `PROBE_COULD_NOT_EVALUATE / PROBE_BASE_TREE_OID_MISMATCH`.
    Lane W299 re-derives the nine variants mechanically (all nine `modification.patch` files apply to
    the repaired tree with no fuzz, Lead dry-check 20:10), the catalog PROBE rows are re-pinned
    two-party, the bundle is re-sealed (#12), and the baseline `C:\tmp\P012_BASELINE_RUN` is
    regenerated against seal #12 exactly as decision 77 did for seal #10 (W265 method): no sealed
    VALUE moves, only the nine probe digest rows. The design item "bind the baseline to the
    RED/GREEN content digest rather than the whole-bundle seal" stays OPEN for the morning.

## Addendum 35 - 2026-09-02 23:5x / 2026-09-03 00:0x REAL (owner verbatim: "I am sleeping give very short status report and make sure to work until I stop or plan completed"; plan rev 7 defaults applied)

133. **Q4 APPLIED BY DEFAULT: KERNEL PRODUCER CONTRACT LANE W304 AUTHORIZED.** Plan rev 7 (23:2x) put
    Q3/Q4 to the owner with "defaults apply if you say nothing"; at 23:5x the Lead pushed Q4 to the
    owner's phone; the owner answered only with the instruction above (keep working until stopped or
    the plan completes). Under that instruction the Lead applies the stated default: the corrected
    kernel serializer must emit the design's closed result contract (`order_notional`, `admitted`,
    `guards` where §23.4 requires them; exit reason tokens in the §23.3/§13 domain - `PROTECTIVE_STOP`,
    `time_stop`) from the kernel's own computations; plus the two harness rows (runner's real collision
    policy passed into `run_manifest`; the sealed RULE2-08 input's funding events fed to the run, else
    an input question). One commit per outcome, failing-then-passing evidence, legacy replay byte-exact,
    different-family verification, both flagships and detection re-run after. Evidence:
    `C:\WP012BUILD\W284R_VALIDATOR_REPAIR_REPORT.md` (residual table) and `W284R_GATE_RECEIPT.json`.
    Q3 (plan rev 7) is superseded: the RULE2-05-RED value is ABSENT, not 101 (W301 read a stale file).
    The owner may reverse this on waking; nothing is pushed or merged.
134. **Q2 APPLIED BY DEFAULT: RULE2-01-GREEN PROVENANCE EXCEPTION.** The golden was revised by
    design-directed lanes W156 (design v1.5), W167 (v1.8) and W172 (owner Reading Y), each verified at
    the time; the new provenance predicate (W284 item 4) refuses `EXPECTED_PATH_CHANGED_AFTER_BASE`
    without a recorded exception. Default applied: record those three repairs as the authorized §15.4
    exception; no golden byte changes now. The recording mechanism (a provenance exception record
    the gate reads) is harness work for the next harness lane; until then the record stays as an
    expected refusal. The owner may reverse on waking.

## Addendum 36 - 2026-09-03 01:1x REAL (Lead record for the morning; no new owner decision)

- **W304 (decision 133) landed rows 1-6** (order_notional, admitted, guards, PROTECTIVE_STOP, time_stop,
  collision-policy pass-through; 292 tests; legacy replay 34/34). **Row 7 STOPPED honestly:** the sealed
  RULE2-08 inputs bind `cost_schedule_id`/`cost_schedule_sha256` to null while ordinary bars build
  lifecycle state; the kernel refuses the state-building OPEN without a cost record (economics.py:616-626),
  so no funding cash/decision rows can arise; adding a seed is forbidden by the owner binding that GREEN
  lifecycle state is built by ordinary bars with nothing injected. **OWNER ITEM M1** (morning).
- **Design items for the morning (M2):** W279-F18 (numeric node kind value-dependent, design 15.3 binds
  it); W304-D3 (conditional result members need a sealed declaration of the evaluated projection - the
  harness transports `owning_def_ids` today); baseline binding to a content digest (decision 132 left it
  open); V283a discrepancy 1 (no literal runtime-equity accumulation line; derived from :75 + :1107-1108).
- **Second baseline regeneration under decision 132:** the first probe re-pin (W299) patched the old
  variant trees instead of fresh copies of the repaired kernel (gate: PROBE_KERNEL_DIFF_INVALID x9); W299B
  rebuilds them on the final kernel; the seal therefore moves to #13 and the baseline regenerates once
  more in the same shape. The Lead records this here as within decision 132's authorization (same act,
  same shape); the owner may object on waking.
- **Fold verify dispute:** DS111 (DeepSeek flash) claimed two HIGHs on the P0-20 amendment fold (a
  deleted decision-82 row); measurement shows zero deleted lines and the row byte-identical; the fold
  stands. Lead sweep: nine owner-quote tags across the drafts changed from curly to the ledger's straight
  quotation marks (character-exact rule).
- Routes 01:1x: Codex fourth + secondary capped until 05:43; Codex free live; Claude Pro resets 02:41;
  MAX unused since 20:1x (decision 131).

## Addendum 37 - 2026-09-03 02:0x REAL (Lead record: the engine branch reached its honest final state; re-audits started)

- **Chain closed at re-seal #13** (`EXPECTED_SEAL_SHA e4ffde6a...`): W299C rebuilt the nine kernel probe
  variants from a fresh copy of the final core (offset-applied unchanged patches; Lead one-file
  measurement 9/9), catalog re-pinned two-party, baseline regenerated (W300B PASS, 34/34 identical to the
  seal-12 run), all five in-repo bundle copies refreshed (W303D, `a854ab4d`, `8ca003e4`).
- **Canonical gate at HEAD `8ca003e4` (W303D receipt): 9 refusal records, 8/10 probes DETECTED.** Every
  refusal traces to an owner item: (1) `SEMANTIC_COVERAGE_REVIEW_MISSING` = the owner's section-16 review;
  (2) `EXPECTED_PATH_CHANGED_AFTER_BASE` RULE2-01-GREEN = decision 134's exception, mechanism pending in
  the harness; (3-7) the RULE2-08 cluster (missing `cumulative_funding`, cash/decision rows) = morning
  item M1 (sealed input without a cost schedule); (8-9) two probes NOT DETECTED: PROBE-P012-02-A now
  fails first at `/RESULT_SURFACE/admitted` (closed-set check precedes its declared cross-version check
  after W304 made `admitted` a kernel member) and PROBE-P012-08-A collides with M1. **OWNER ITEM M4:**
  the two probe rows' `expected_failed_check` / first-changed-node predictions need re-derivation by the
  tables family (a design-directed re-authoring, owner-visible), or the probes are recorded as
  conditional on M1.
- **Re-audits of the fixed branch started 01:59:** detection GM83B (Gemini, packet at HEAD `8ca003e4`),
  then flagship 1b (Codex) and flagship 2b (Claude Pro) once the worktree is quiet for Gemini.
- Kernel and harness work of the night, all with red-then-green, legacy replay 34/34 byte-exact, and a
  non-author-family verification: W283 (7), W283R (5+1 refuted+1 cleared), W283R2 (9+1+1), W283R3 (1 refuted),
  W285 (6 + item 8; F06 moved to W284, F18 design-bound), W284 (6 + F06), W304 (6; row 7 = M1). Tests 292.

## Addendum 38 - 2026-09-03 02:5x REAL (Lead record: detection re-run GM83B and its triage; no new owner decision)

- **GM83B (Gemini, third family, packet at HEAD `8ca003e4`): 8 findings, no BLOCK.** Triage T83B (DeepSeek
  V4 Pro): F02 REAL MEDIUM (the comparator iterates expected keys only, so an extra observed member escapes
  outside the closed-set validator's scope), F03 REAL MEDIUM (catalog conservation scans only the expected
  root, not OBSERVED_ROOT / PROBE_ROOT; design line 478), F04 REAL LOW (dead `LegacyEconomicsAdapter` seam,
  never invoked), F08 LOW (negative-zero preservation unspecified by the design); F01 already dispositioned
  (W284 item 2: bounded skip with receipt accounting), F05 = W279-F18 (design-bound, M2), F06 = W304-D3
  (declaration transport, M2), F07 = W279-F21 fallback (design-bound, M2). Report
  `C:/tmp/LANE_PROMPTS_20260828/DETECT_GM83B_BRANCH.md`; triage `_packets_T83B/T83B_REPORT.md`.
- **Disposition:** F02 + F03 + the decision-134 provenance-exception mechanism go to one harness lane
  (W305, standing build authorization) on the first Codex slot after flagship 1b; F04/F08 record-and-carry
  into M2. None is a kernel edit.
- Flagship 2b (W279B, Claude Pro) running since 02:41; flagship 1b (W276B) waits for the Codex reset at
  05:43 (all three Codex accounts capped at 02:42).

## Addendum 39 - 2026-09-03 03:1x REAL (Lead record: flagship 2b re-run verdict; no new owner decision)

- **W279B (Claude Pro, flagship 2 re-run on HEAD `8ca003e4`, re-seal #13): BLOCK, 19 findings (6 HIGH,
  8 MEDIUM, 5 LOW).** Its own tally of the 25 DS102 rows: 17 FIXED, 2 partially, 4 NOT FIXED (W276-F05,
  W276-F06 owner-word pending, W279-F14 metrics never produced, W279-F18 design-bound); three highest
  fixes reproduced RED-then-GREEN by the auditor; legacy path byte-exact.
- **Its single sentence to reach PASS-WITH-NITS:** the canonical gate returns the accepting label with
  zero refusals, which requires (a) a funding transcript on both DEF-P012-08 rows (= morning item M1 plus
  W279B-F02: `cumulative_funding` presence keyed on runtime state instead of the declared DEF, a one-line
  kernel fix needing owner word), (b) the owner's signed section-16 review, (c) `IMPLEMENTATION_BASE_SHA`
  at or after the seal commit (W279B-F06: the base is pinned before the sealed bundle exists, so the
  provenance check can never clear; **owner item M5**: re-pin the base to the seal commit or record the
  exception).
- **Harness HIGHs for the next harness lane (standing authorization):** F03 committed OBSERVED_ROOT 2.0.0
  artifacts stale and unpinned (refresh or pin), F04 RULE-2 divergence / GREEN cross-version checks
  computed by the reader from actuals, F05 GATE_READER supplies economic inputs to KERNEL_2 (the D3
  declaration transport), F07 scenario-conditioned closed sets, F14 provenance refusal reports one path
  of nineteen. Folded into W305's scope as items 4-8.
- **Kernel MEDIUM/LOW items needing owner word (morning):** F02 (above), F11 empty-transition key on a
  per-instance object, F13 ordered accumulation applied to equity only (cumulative_funding/fee still
  sum-then-add), F18 stop predicate outside the closed domain reachable, F16 = F18-old node kind.
- **Design items (M2 grows):** F08 accepting label renamed and 96 nodes excluded without a design
  amendment; F09 exit_events[].reason has no closed design vocabulary; F10 design authority and baseline
  producer live at absolute paths outside the repository; F12 metrics never produced (= W279-F14).
- Detection GM83B (8 findings, triage in addendum 38) and flagship 1b (W276B, Codex, waits for the 05:43
  reset) complete the round; the merge decision belongs to the owner in the morning.

## Addendum 40 - 2026-09-03 03:4x REAL (Lead record: second-family cross-check of flagship 2b; no new owner decision)

- **T279B (DeepSeek V4 Pro) agrees with the BLOCK verdict** and confirms all six HIGHs as REAL on HEAD
  `8ca003e4`: F01 (no DEF-P012-08 funding transcript = M1), F02 (`cumulative_funding` keyed on runtime state;
  one-line kernel fix at `core/results.py:968`, needs owner word), F03 (committed observed 2.0.0 artifacts
  stale; 17/17 differ from live), F04 (reader-authored RULE-2 checks), F05 (= W304-D3, `_target_book_overrides`
  re-implements target arithmetic in the harness), F06 (base SHA `108ea066` predates the sealed-bundle commit
  `5e8e5794`; all 19 members refuse; owner item M5). F11 and F13 REAL MEDIUM (kernel, owner word).
- **Kernel lane W306 pre-written** (F02, F13, F11) - fires only on the owner's morning word; harness items
  F03/F04/F05/F07/F14 are in W305 (standing authorization) after flagship 1b at 05:43.
- Route/cost note: MAX unused since 20:1x; the OpenRouter DeepSeek harness has carried every verify and
  triage since 20:2x (29 runs, all under ten minutes).

## Addendum 41 - 2026-09-03 03:5x REAL (Lead record: harness lane W305 partial; folds complete; no new owner decision)

- **W305 (Claude Pro, standing harness authorization) landed items 1-4** at HEAD `b22a912c`: symmetric
  comparator at every level (GM83B-F02), conservation of OBSERVED_ROOT and PROBE_ROOT (GM83B-F03), a recorded
  provenance-exception record read by the predicate for owner decision 134 (exact blob OIDs), observed
  artifacts pinned to the gate's own run and refreshed (W279B-F03). V305a (DeepSeek V4 Pro): items 1-3
  ACCEPT; item 4 verified separately (V305b, from the code part of a 530 KB commit). Pro then hit its session
  cap (resets 07:40); item 5 (W279B-F04) was in progress and is saved as a patch; **W305B** (items 5-8:
  F04, F05, F07, F14) fires on Codex fourth at the 05:43 reset, then flagship 1b (W276B) on Codex free.
- **Goal 2 met:** all seven original folds and the three amendment layers (addendum 32) are done and
  verified by a second family (final snapshot `SNAPSHOTS/20260903_0320`).
- Route reality for the record: Claude Pro's 5-hour window carried three lanes (flagship 2b, one fold, one
  harness lane) before capping; all three Codex accounts capped between 01:04 and 02:42 and reset at 05:43.

## Addendum 42 - 2026-09-03 06:2x REAL (Lead record: harness continuation W305B; two new owner items; no new owner decision)

- **W305B (Codex fourth) landed items 5-8** at HEAD `f06e3a2d`: unsealed RULE-2 projections refused instead of
  computed (W279B-F04); reader-authored economic inputs removed, fail-closed `INPUT_DECLARATION_MISSING`
  (W279B-F05); closed sets derived from the sealed declarations, not scenario ids (W279B-F07 / GM83B-F06);
  provenance refusal reports every changed path (W279B-F14). 308 self-tests. Verify V305C running.
- **The honest gate now refuses 28 records; 21 are new because the harness no longer authors expectations or
  inputs.** They resolve to owner/tables items, not lane work:
  - **M6 (new):** sixteen `EXPECTATION_UNSEALED` records - the sealed tables carry no RULE-2 projection
    declarations (divergence / GREEN cross-version expectations); the tables family must seal them
    (design-directed re-derivation, re-seal follows). *Approve?* default yes.
  - **M7 (new):** the equal-price scenario (RULE2-06-EQUAL-PRICE-RED) has no sealed `target_book` economic
    input; the harness used to construct it. Same shape as M1: a sealed-input change (owner-gated). *Approve?*
    default yes.
  - **M4 grows:** RULE2-06-RED now differs from its golden at one node and PROBE-P012-06-A is not detected,
    because the removed reader shaping used to make them match; re-derivation by the tables family joins the
    two existing probe rows.
  - **M5 confirmed:** 18 sealed members remain changed after the recorded base commit (decision 134 lifts one).
- Flagship 1b (W276B, Codex free) started 06:15 on HEAD `f06e3a2d`.

## Addendum 43 - 2026-09-03 07:3x REAL (Lead record: flagship 1b re-run; the three-verdict round is complete; no new owner decision)

- **W276B (Codex free, flagship 1 re-run on HEAD `f06e3a2d`): REQUEST_CHANGES, 5 findings.** F01 HIGH: the
  accepting predicate still skips every `BLOCKED-*` expected node (bounded label; the design's "every node"
  claim at the accepting label is neither met nor amended) - **owner item M8**: make blocked nodes typed
  acceptance blockers, or amend the design to the bounded claim (Lead default proposal: amend, because the
  96 blocked nodes are design-unenumerated by construction). F02 LOW: the ordinary self-test blank line
  (decision 124 said repair; still present) - one-line hygiene commit, next lane. F03 = M6, F04 = M7,
  F05 = M4 (RULE2-06 evidence). Its own DS102 tally agrees with flagship 2b except W279-F03, which it counts
  NOT FIXED (= M8). Legacy replay 34/34; tests 308 + 142; gate 28 refusals, honest.
- **Round complete:** detection 8 findings (no block), flagship 2b BLOCK (19), flagship 1b REQUEST_CHANGES
  (5). All three agree the remaining work is owner/tables-family decisions (M1, M4, M5, M6, M7, M8, K, review),
  not lane work. V305C accepted W305B items 5-8; every kernel/harness change of the night is now
  independently accepted.
- W308 (cross-draft consistency of the addendum-32 layers): one drift fixed by measurement (the owner's
  "for example" hedge restored in P0-20), echo lines added; design item: one owner for the policy-version
  concept (Lead ruling P0-20; morning confirm).

## Addendum 44 - 2026-09-03 07:5x REAL (Lead close-out of the overnight run; no new owner decision)

- **Final engine branch state:** `C:/WP012BUILD` HEAD `ac2d2ca9` (flagship-audited `f06e3a2d` + W310's one
  hygiene commit under decision 124: 1 ordinary whitespace diagnostic repaired, 99 pinned-probe-copy diagnostics
  preserved), clean, never pushed; bundle re-seal #13 `e4ffde6a`; baseline W300B; tests 308 + 142; legacy replay
  34/34 byte-exact after every commit of the night. Every kernel and harness commit accepted by a non-author
  family.
- **Night tally against the overnight prompt:** goal 1 (branch re-audited clean) NOT MET - the three-verdict round
  (detection 8 findings / flagship 2b BLOCK 19 / flagship 1b REQUEST_CHANGES 5) agrees the remainder is owner or
  tables-family work (M1, M4, M5, M6, M7, M8, K, section-16 review); goal 2 (41 answers folded) MET, 10 folds
  verified; goal 3 (signature) deliberately not spent (decision 125); goal 4 (routes) MET; goal 5 (plans every
  2 h, handoff) MET - plans rev 5-11, handoff at
  `%TEMP%/HANDOFF_OVERNIGHT_2026-09-03_MORNING.md` rev 5 after two outside checks (W307, W309).
- **Owner decisions taken tonight by his word:** 123-126, 131, 132, 127-130 (addendum 32); by default under his
  "work until stopped" instruction: 133, 134 (Q4, Q2). Morning items M1-M8 and K are yes/no with defaults on the
  handoff page.
- Routes at close: Codex x3 live, Claude Pro live (07:40 reset), Gemini idle, OpenRouter DeepSeek harness 25
  distinct verify/triage tasks, MAX untouched since 20:1x, OpenCode/NIM/GLM parked, DeepSeek direct and Grok 402.

## Addendum 45 - 2026-09-03 08:1x REAL (owner verbatim: "I approve M5, K, M1, M6, M7, M4, and M8, with their stated safety conditions. Keep every change strictly limited to those items. For K, require a real failing-then-passing proof, unchanged legacy replay, and independent second-family verification. Do not sign or prepare my Section 16 acceptance yet. First complete the scoped corrections, create one fresh sealed snapshot, and run the required fresh independent audits against that exact snapshot. After that, schedule M2. Include the separate loss-at-stop decision in that session; do not invent a number for me. Before launching new work, classify the four remaining Claude-related background processes and confirm that no old lane is still writing.")

135. **M5 APPROVED - base commit re-pin.** The recorded `IMPLEMENTATION_BASE_SHA` moves from `108ea066` to the
    commit that first carried the sealed bundle (`5e8e5794`), with `core_tree_oid_at_base` re-measured at that
    commit; a Lead act at the fresh seal (#14), bundle anchor and in-repo anchor copy, verified by another family.
136. **K APPROVED - three kernel fixes (W306): W279B-F02, F13, F11.** Conditions (owner's words): a real
    failing-then-passing proof per item, unchanged legacy replay (34/34 byte-exact after every commit),
    independent second-family verification. Scope strictly the three items.
137. **M1 APPROVED - sealed-input change:** the two RULE2-08 inputs receive the cost-schedule record the
    kernel's contract requires, so the funding transcript can exist; tables-family act (Claude Pro), input
    digests re-pinned in the catalog, fresh seal follows; nothing else in those inputs moves.
138. **M6 APPROVED - seal the RULE-2 projection expectations** (divergence and GREEN cross-version) in the
    sealed tables by design-directed derivation; tables-family act; verified by another family before the seal.
139. **M7 APPROVED - sealed-input change:** the equal-price scenario receives its sealed `target_book` economic
    input (same shape as M1).
140. **M4 APPROVED - re-derive** the expected check / first-changed node of probes PROBE-P012-02-A, 06-A, 08-A and
    the one RULE2-06-RED golden node that depended on the removed reader shaping; tables-family act, design-
    directed, verified, fresh seal.
141. **M8 APPROVED - design amendment:** the accepting claim becomes the bounded claim the receipt states (only
    the explicitly decided nodes are compared; the 96 design-unenumerated BLOCKED nodes are listed in the
    receipt); design v1.13 amendment by the design author family, verified; harness label already conforms.
    **Section-16 acceptance: NOT to be signed or prepared** until the scoped corrections land, ONE fresh sealed
    snapshot (#14) exists, and the fresh independent audits (two flagships of different families + detection)
    run against that exact snapshot. **M2 session** scheduled after that; it includes the separate loss-at-stop
    decision; no number is invented for the owner.
    **Process census (owner's precondition), measured 08:11:** the Claude processes are the Claude desktop app
    (pid 52744) with its Chromium helpers, plus three Claude Code engine processes under it: this session
    (pid 24380, started 19:18), and two idle sessions from the day (pids 19312 started 09:34 and 45536 started
    09:35 - the day Lead and its fork, both closed by their Leads; they hold no lane). Codex processes: the
    Codex desktop app (pid 25588), its app-server (pid 11112) and the VS Code Codex extension (pid 53872) - none
    is a lane (lanes run `codex exec` and all have exited). Worktree `C:/WP012BUILD` clean at `ac2d2ca9`; no lane
    DONE file is missing; no old lane is writing.

## Addendum 46 - 2026-09-03 08:2x REAL (Lead record: M1 cannot be executed as a sealed-input change; owner question M1b)

- W311 (Claude Pro, tables family) did M7 (equal-price `target_book` sealed from design line quoted; catalog row 11
  digest; DERIVATIONS insertion-only) and STOPPED M1 honestly: the design does not merely omit a RULE2-08 cost
  record, it binds that there is none (`P012_FRESH_DESIGN_V1.md:788-790` "both cost members are JSON null only
  for RULE2-08, where section 14 says no cost schedule is consumed"; `:443`; `:960-961` "C is absent /
  NOT_CONSUMED"), while owner addendum 20 (4a)/(5a) binds real pre-window fills for both RULE2-08 rows, and the
  kernel refuses the state-building OPEN without a cost record. The conflict is already recorded at
  `DERIVATIONS.md:1735-1741` (V15-D01). No RULE2-08 cost record exists under `core/economic_records/costs/`.
- **Owner question M1b** (decision 137 cannot be carried out without it): (a) amend the design so RULE2-08
  consumes a cost record and name it - the Lead's default proposal binds RULE2-08 to the EXISTING sealed
  RULE2-07 cost record (DEF-P012-07 schedule) by reference, so no new number is invented; or (b) withdraw the
  pre-window fill premise of addendum 20 for RULE2-08 (then no funding transcript can exist and DEF-P012-08's
  evidence must be re-designed). Default if silent: (a).
- W312 (M6 + M4) proceeds for every row except the RULE2-08 rows and probe 08-A, which wait for M1b.

## Addendum 47 - 2026-09-03 08:4x REAL (Lead record: morning program state - K landed, three verifies ACCEPT)

- **K (decision 136) landed** on the engine branch by the kernel author family (Codex, W306): `4b1853c4` (F02:
  `cumulative_funding` membership keyed on the sealed declaration `owning_def_ids` containing DEF-P012-08, value 0
  with no funding event), `4cc00714` (F13: ordered per-row accumulation of `cumulative_funding` and
  `cumulative_fee`), `67f86ad2` (F11: deterministic content identity for empty transitions); receipt `8b9e2964`,
  report `191637e2`. Each item has a quoted RED (failing before) and GREEN (passing after) test; the legacy replay
  reads `SURFACES_EQUAL=34 MISMATCH=0 SKIPPED=0` after each of the three commits. The canonical gate was invoked
  once and refused on `DESIGN_PIN_MISMATCH` only: the in-repo design pin is still v1.12 (1419 lines) while the
  design is v1.13 (1469 lines) after M8 - expected, the re-pin is the later in-repo copy lane. Independent
  second-family verification (V306, DeepSeek V4 Pro) is running at the time of this record.
- **K follow-up (W314, Codex fourth, launched 08:34):** five contract self-test cases in `test_verify_bceg.py` still
  assert the pre-F02 behaviour (absence of `cumulative_funding`; old `CLOSED_SET_VIOLATION`) and contradict the
  design (`P012_FRESH_DESIGN_V1.md:1224-1228`); W306 reported them rather than editing harness bytes. W314 aligns
  exactly those five cases, nothing else; verified by another family before seal #14.
- **Harness residual (not fixed, recorded for the fresh audits):** the gate's early-refusal path does not write
  `--output` (only stdout); W306 preserved the emitted JSON by hand as its receipt.
- **Verifies (DeepSeek V4 Pro, read-only):** V313 = ACCEPT (design v1.13: zero deletions, the three claim
  occurrences struck and superseded by the bounded claim, wording matches the harness labels and
  `comparison_claim_scope=ALL_NON_BLOCKED_EXPECTED_NODES`, honest limit added as L9 in section 17 - the spec's
  "0.2.5" did not exist, C-2 applied). V311 = ACCEPT x3 (M7 `target_book` traceable to design section 22.5; M1
  correctly STOPPED, RULE2-08 inputs byte-identical before/after; catalog delta = the one digest).
- Running: W312 (M6 + M4, Claude Pro; RULE2-08 rows and probe 08-A held for M1b), W314, V306. Next after they
  land: V312, V314, then the Lead sequence repin_base14 (M5) -> reseal14 -> baseline regeneration (decision 132
  shape) -> probe manifests from the W312 table -> in-repo five-file copy + design pin v1.13 -> fresh audits.

## Addendum 48 - 2026-09-03 09:0x REAL (owner decisions 142-143 from the W312 discrepancies; state after the first verify round)

142. **M7b APPROVED (default (a), owner 09:0x "both questions are default"):** the RULE2-06-RED and RULE2-06-GREEN
    sealed inputs receive the `target_book` member (W312 D-7: without it the corrected run keeps the kernel's own
    TP1/TP2 ids and mismatches its golden before probe 06-A runs - the class decision 139 closed for the equal-price
    row). Values quoted from the design's own scenario rows; no invented number; tables-family act (W319, Claude
    Pro), verified, in seal #14.
143. **M4b APPROVED (default (a)):** PROBE-P012-02-A's design-named check is unreachable for a KERNEL-kind probe
    (W312 D-6: the check now compares two sealed producers only). The design family re-targets 02-A to a reachable
    check derived from the design's own RULE-2 fail input (W317); the tables family then derives the row values;
    if no reachable check exists, 02-A is proposed for retirement and the owner decides.
- **Lead dispositions inside the M6 fence (owner may veto):** (i) W312 D-2/D-3 - the design's closed catalog-row
  member list (section 15.2) does not admit the two projection members the harness reads from the row, and their
  JSON container is not pinned; W317 (design family) admits them and pins the shape W312 wrote (V312 ACCEPT), adds
  honest limit L10 (legacy-side states are `DESIGN_DERIVED` declarations until reconciled against the baseline
  bytes by a later lane - W312 D-4/D-5). (ii) W312 D-12 - the harness raises `EXPECTATION_UNSEALED` before reading
  the row and a selftest asserts that for every row; W318 (harness family, Codex free) wires consumption with
  RED/GREEN discriminators. Neither adds a number.
- **Verify round 1 complete:** V306B ACCEPT x3 (K commits, diff-level); V311 ACCEPT x3; V312 ACCEPT (55 members
  on 15 rows; RULE2-08 x2 + 08-A STOPPED for M1b; 12 discrepancies all accepted as recorded); V313 ACCEPT; V314:
  cases 2-5 ACCEPT, case 1 (probe-driver selftest) REQUEST_CHANGES because W314 took its value from a run instead
  of stopping - reverted by W314B (`0c44a447`), the case now fails honestly as an open item of the 08-A cluster.
  Engine HEAD `8112ff0b`. Codex fourth and secondary capped until 10:45; free live.
- **Owner question M1b remains open** (addendum 46; default (a) = bind RULE2-08 to the existing RULE2-07 cost
  record by design amendment). The Lead will apply the default only on the owner's word or at the seal-#14
  deadline stated in the next status; the RULE2-08 rows and probe 08-A stay held until then.
- Revised order: W317 + W319 + W318 (parallel, three families) -> V317/V319/V318 -> W315 (probe variants rebuilt on
  the post-K core + M4/M4b values; Codex) -> Lead repin_base14 + reseal14 -> W300C baseline regeneration -> W316
  in-repo copies + design pin -> fresh audits on that exact snapshot.

## Addendum 49 - 2026-09-03 09:1x REAL (owner decision 144: M1b = (a))

144. **M1b DECIDED (a), owner 09:1x verbatim: "M1b decision a) amends the design so RULE2-08 references the existing
    RULE2-07 cost record".** Consequences, all inside the M1 fence (decision 137): (i) design amendment by the design
    author family (W320, Claude Pro, after W317 releases the design file): RULE2-08-RED and RULE2-08-GREEN consume a
    cost record, bound BY REFERENCE to the existing sealed RULE2-07 cost record (its id and sha256 as sealed in the
    branch), superseding the "no cost schedule is consumed" sentences (design lines 443, 788-790, 960-961) by the
    retain-and-strike convention; no new number. (ii) tables-family act (W321, Claude Pro, bundle): the two RULE2-08
    inputs receive the cost-schedule binding members, catalog digests re-pinned, DERIVATIONS insertion-only; the two
    held M6 projection rows and the held probe 08-A values are then derived from the amended design. (iii) verified
    (V320, V321) before seal #14. The reverted probe-driver selftest (W314B) is closed by the same chain.
- State at this record: V319 ACCEPT (M7b). W317 (design v1.14: members admitted, shape pinned, L10, M4b re-target)
  and W318 (harness consumes the sealed projections) still running.

## Addendum 50 - 2026-09-03 09:2x REAL (Lead record: verify round 2 clean; owner checkpoint prompt; Wayfinder update)

- **Verify round 2 (DeepSeek V4 Pro, read-only): V317 ACCEPT** (design v1.14, 1627 lines, sha `a17e6768...`: zero
  deletions; section 15.2 admits the two projection members; container pinned member-by-member to the sealed bytes
  (tighter than W312 prose where the bytes carry `note` / `refusal_code`); L10 honest limit; M4b: PROBE-P012-02-A
  re-targeted to `CORRECTED_EXPECTATION`, a check a KERNEL-kind variant can fail, no retirement, no invented id).
  **V318 ACCEPT** (harness `3c372de0` consumes the sealed members by the sealed shape, refuses `EXPECTATION_UNSEALED`
  only for rows lacking the member, records `legacy_side_source`, no `BASELINE_BYTES` read; discriminators real;
  replay `SURFACES_EQUAL=34`; selftests 3 failed/310 = the expected pin pair + the reverted probe-driver case).
  **V319 ACCEPT** (M7b). Engine HEAD `f37f2677`.
- **Owner checkpoint prompt (09:1x) applied:** its premise "M1b undecided" is superseded by the owner's own 09:1x
  message (decision 144); the RULE2-08 branch proceeds under that word only: W320 (design v1.15, Claude Pro) launched
  09:23; W321 (tables) follows V320. No duplicate writers; worktree lanes serial; MAX spent on sequencing and owner
  summaries only; mechanical production (Wayfinder update, packets) on DeepSeek.
- **Wayfinder session update** `2026-09-02T1918-claude` revision 1 OPEN_PROVISIONAL written 09:20 (8 packages,
  hours UNKNOWN pending the evidence rollup) and imported by the dashboard at 09:20
  (`data/session-revisions/2026-09-02T1918-claude/revision-000001-...`). Revision 2 with evidence-computed lane
  hours follows; FINAL_CLOSEOUT only at genuine close.
- Next: V320 -> W321 -> V321 -> W315 (Codex, probe variants on the post-K core + M4/M4b/08-A values) -> Lead
  repin_base14 + reseal14 -> W300C -> W316 -> fresh audits on that exact snapshot. Section 16 and M2 remain
  unscheduled until that round is clean.

## Addendum 51 - 2026-09-03 10:1x REAL (Lead record: design v1.15 for decision 144; route reroute; 24h plan)

- **Claude Pro session cap at 09:26 (resets 13:10)** killed W320 at launch. Under the owner's checkpoint rule (cheap
  verified routes for bounded edits) the design amendment was authored by DeepSeek V4 Pro through the repo harness and
  verified by the Codex family (V320C, Codex free) - families still differ between author and verifier.
- **W320 history, recorded honestly:** attempt 1 rejected by the Lead (three v1.14 lines modified in place, blocks
  inserted inside tables, CRLF written by the harness) - design restored from the v1.14 snapshot; attempt 2 met the
  insertion-only convention (minus 1 header / plus 29) but V320C round 1 returned REQUEST_CHANGES with seven findings,
  three substantive: (1) the RED corrected equity chain must become 1000 -> 999.9 (pre-window OPEN fee 0.1 at taker
  0.001 on notional 100, the design's own fee identity) -> 999.8 (funding), so the RULE2-08-RED golden equity/net/cost
  nodes are re-derived by the tables family; (2) RULE2-08-GREEN is NOT fill-free under addendum 20 (5a) - two
  pre-window fills consume the GREEN record; their prices are design-unenumerated (OPEN-EMBED-05 mechanism bound,
  numbers not), so the GREEN numeric equity node carries `BLOCKED-OPEN-EMBED-05` (new honest limit L12) - no price
  invented; (3) L11 wrongly claimed a cost-record interval check (the kernel validates id + digest + JSON form only).
  Repair pass (attempt 3) closed all seven; V320C round 2 = ACCEPT on every substantive check (1-5), REQUEST_CHANGES
  only on the author report's line map. **Lead accepted design v1.15** (LF, sha `137180ae...`, 1664 lines; vs v1.14
  minus 1 / plus 38) and recorded the report defect as a discrepancy; the V320C round-2 report is the line map of
  record. EOL normalization CRLF->LF by the Lead after each harness pass is recorded here.
- **Consequences inside the M1 fence:** W321 (tables, DeepSeek author, Codex verifier) binds the two RULE2-08 inputs
  to the RULE2-07 records, seals the two projection rows, re-derives the RED golden nodes from the 999.8 chain, keeps
  GREEN blocked nodes as the design marks them, and derives the 08-A / re-targeted 02-A probe values.
- **Gemini route:** owner 09:4x - `gemini-3.8-flash-high` replaces 3.7 (both launchers switched; 3.7 kept as fallback).
- **24h plan** sent to the owner (`C:/tmp/LANE_PROMPTS_20260828/PLAN_24H_2026-09-03.md`): one clean fresh audit round
  on seal #14; Section 16 / M2 not scheduled before that.

## Addendum 52 - 2026-09-03 12:3x REAL (owner question: why the design packages still show "Awaiting acceptance"; Lead answer and the acceptance path)

- **Owner (12:xx):** "Why is P0-12, P0-13, P0-14, P0-20, P0-21, P0-22, P0-30 and P0-31 still looks Awaiting acceptance? when do
  we proceed? it look like we are stuck here." **Lead answer:** the dashboard never approves; green comes only from the
  accepted package register, whose rows moved to "in repair" under decision 75 (2026-09-02). The night's folds converged the
  drafts and were fold-verified, but no one asked the owner to accept them, and no detection census had run on the
  post-fold text. P0-12 is genuinely in progress (build authorized) and turns green only when BUILT_MERGED.
- **Post-fold censuses (DeepSeek V4 Pro, read-only, seven drafts) + cross-family triage (Codex, T330):** P0-30 v1.9
  CONVERGED; P0-21 v1.12, P0-22 v1.11, P0-31 M2 v1.9 ACCEPTABLE AS IS (every census finding disputed by measurement -
  retained-text convention misread); P0-13 v2.2 and P0-20 v1.8 ONE FOLD (the strategy-type list stated as closed
  where the owner's addendum-32 wording is "for example") - folds running on DeepSeek V4 Pro (design family capped),
  verified by another family; P0-14 v1.8 NOT READY (three confirmed: open-item count contradiction; "QuantStats
  adopted" vs WP-P0-24 entries REJECTED; finding-record writer unnamed) - W331 fold on Claude Pro after 13:10;
  P0-31 M1 stays PARKED by its stopping rule unless the owner reopens it.
- **Acceptance packet** `C:/tmp/LANE_PROMPTS_20260828/OWNER_ACCEPTANCE_PACKET_DESIGNS_2026-09-03.md` (Issue 2 table
  is the one that stands; the builder's first "last verdict" column was stale and is marked so). Owner words of the
  form `accept design P0-30 v1.9`. Accepting = design accepted for build planning only; the Lead then commits the
  register status change (standing git delegation) and the dashboard turns green on import.
- **P0-12 chain state:** W321 (tables, DeepSeek author) round 1 BLOCKED by the Codex verifier - three digests moved by
  the Lead's own line-ending normalization after the harness wrote CRLF (Lead process defect, fixed by a byte-level
  digest re-pin script, recorded), manifest not re-pinned (expected, reseal #14), and one real defect: GREEN equity
  sealed as 1000 where design v1.15 requires `BLOCKED-OPEN-EMBED-05`. Repair pass landed (GREEN golden nodes carry the
  marker; the GREEN equity projection pair STOPPED as DESIGN-GAP); V321C round 2 running. Catalog sha now `577a6055`.

## Addendum 53 - 2026-09-03 12:4x REAL (Lead record: six designs ready for the owner's acceptance word; P0-12 tables round 2)

- **Folds after the census triage (T330):** P0-13 v2.2 -> v2.3 (FOLD-P013, DeepSeek V4 Pro standing in for the
  design family; two AMENDMENT-CHOICE blocks quoting the owner's addendum-32 wording "for example"; header the only
  changed line, 17 inserted; verified ACCEPT by DeepSeek V4 Flash). P0-20 v1.8 -> v1.9 (FOLD-P020, same shape, 10
  inserted; the verifier passed the draft checks 1-4 and faulted only the fold report's line-count claims - the Lead
  accepted the draft and recorded the report defect). Both drafts LF-normalized by the Lead after the harness pass.
- **Acceptance packet, table that stands (Issue 2 + rows updated):** ACCEPT NOW = P0-30 v1.9, P0-21 v1.12, P0-22 v1.11,
  P0-31 M2 v1.9, P0-13 v2.3, P0-20 v1.9. NOT READY = P0-14 v1.8 (W331 fold on Claude Pro, armed for the 13:10 reset).
  PARKED = P0-31 M1 (owner may reopen). Register transition on the owner's word: `DESIGN_IN_REPAIR` ->
  `DESIGN_CONVERGED` with the draft version; `g1_ia` / `implementation_authorized` untouched; the Lead commits the
  status record; the dashboard re-imports.
- **P0-12 tables (W321) round 2, Codex verifier:** M1 binding, the four re-pinned catalog digests, the projection
  container and values, the probe expectation values and the listed RED (11 nodes) / GREEN (7 nodes) golden deltas
  ACCEPT; still open: F-04 (manifest at seal #13 - closes at the Lead's re-seal #14, by design) and F-06 residue (GREEN
  golden `run_manifest` still `NOT_CONSUMED`; a projection prose still `1000`; two stale locators) - a narrow third
  pass (W321DS3) is fixing exactly those four spots; then V321C round 3, then W315.
- **Process defects recorded against the Lead today:** line-ending normalization after a DeepSeek author lane moved
  three sealed digests (fixed by a byte-level re-pin script, run after every such lane); a snapshot folder mixed
  inputs and goldens of the same basename (restored from the pre-W311 snapshot; hash tables now carry full paths);
  the harness cwd trap killed three launches (standing wrapper `C:/tmp/run_ds.sh`).

## Addendum 54 - 2026-09-03 12:4x REAL (owner decision 145: six designs ACCEPTED for build planning only; register act)

145. **OWNER, verbatim (12:4x):** "I accept these designs for build planning only. This does not authorize
    implementation, merge, execution, trading, or any live action. - accept design P0-13 v2.3 - accept design P0-20
    v1.9 - accept design P0-21 v1.12 - accept design P0-22 v1.11 - accept design P0-30 v1.9 - accept design P0-31-M2
    v1.9. For each accepted item, change the register status from DESIGN_IN_REPAIR to DESIGN_CONVERGED, record the
    exact accepted draft version, and keep g1_ia and implementation_authorized unchanged. Do not accept P0-14 yet.
    Complete its repair, run a fresh census, then bring it back to me. Keep P0-31 M1 parked. Do not reopen it unless
    I explicitly say so. After updating the register, verify the Wayfinder dashboard imports the changes. Publish a
    valid session update with measured hours only; do not estimate missing hours."
- **Register act (Lead, `C:/tmp/P012_LEAD_RESEAL/update_register_20260903_accept6.py`, same surgical byte-edit method
  as the decision-75 script; backup `WAYFINDER_PACKAGE_REGISTER.json.bak-20260903-accept6`; BOM kept):** six rows
  `DESIGN_IN_REPAIR` -> `DESIGN_CONVERGED` (WP-P0-13, -20, -21, -22, -30, -31), each with a new `design_acceptance`
  member recording state `DESIGN_CONVERGED_OWNER_ACCEPTED_2026_09_03`, the accepted draft version, file, sha256, the
  owner's word, the scope sentence and the evidence pointer; `g1_ia` and `implementation_authorized` untouched
  (asserted by the script); the WP-P0-31 row records "M2 v1.9 only; M1 stays PARKED". WP-P0-14 stays
  `DESIGN_IN_REPAIR` (W331 fold armed for the 13:10 Claude Pro reset; fresh census after; back to the owner).
  Top-level `last_progress_update` / `generated_on` / `as_of` updated. Census after: 21 BUILT_MERGED, 6
  DESIGN_CONVERGED, 4 DESIGN_IN_REPAIR, 1 BUILD_AUTHORIZED_IN_PROGRESS, 44 NOT_STARTED.
- **Dashboard import:** the dashboard's register watcher re-scanned at 12:45:25 (before the write); a new source
  snapshot carrying the six acceptances is awaited (the Lead is watching; result recorded in the next addendum). If
  the importer rejects the added member, the Lead restores the backup and re-applies the status change without the
  member, keeping the acceptance record in this ledger.
- Wayfinder session update revision 4 (measured hours only) follows the import verification.

## Addendum 55 - 2026-09-03 12:5x REAL (Lead record: the dashboard's reader rejects the owner's status word; owner question 146)

- **Measured:** after the register act of addendum 54, the dashboard's register watcher reports
  `refreshState: ERROR`, `sourceError: "WP-P0-13 has an unsupported status."` and keeps its last good snapshot
  (12:45:25, the pre-acceptance register). Cause, read in the dashboard code
  (`site/scripts/lib/package-snapshot.mjs:3`): `allowedStatuses = {BUILT_MERGED, IN_PROGRESS,
  BUILD_AUTHORIZED_IN_PROGRESS, DESIGN_IN_REPAIR, NOT_STARTED}` - `DESIGN_CONVERGED` is not in the reader's set
  (the decision-75 repair added `DESIGN_IN_REPAIR` and the reader currently in service was rebuilt without the
  converged word). The added `design_acceptance` member is NOT the cause (the reader does not reject unknown members).
- **Not done:** the Lead did not edit the dashboard (owner rule 09:1x: "Do not edit C:\LAB\WAYFINDER_DASHBOARD, its
  configuration, or its data directly") and did not change the register away from the owner's word. The register
  stands as decided (authority); the dashboard shows the 12:45 snapshot with a visible ERROR state until the reader
  accepts the word.
- **Owner question 146 (default if silent: (a)):** (a) authorize a two-line change to the dashboard reader
  (`allowedStatuses` gains `DESIGN_CONVERGED`; it is bucketed with the active, not-built statuses as it was before
  2026-09-02), made by a coding route and checked by the dashboard's own tests before the service restarts; or (b)
  leave the dashboard on the old snapshot until someone else changes the reader; or (c) replace the word in the
  register by one the reader accepts (would contradict the owner's word - not recommended).
- Wayfinder session update revision 4 (measured hours only) is published regardless; its closeout states the
  register rejection verbatim.

## Addendum 56 - 2026-09-03 13:0x REAL (owner decision 146 = (b))

146. **OWNER, verbatim (13:0x): "b"** - answer to question 146 (addendum 55): leave the dashboard on its last good
    snapshot until someone else changes the reader. Consequences: the register stands as decided in 145 (six rows
    `DESIGN_CONVERGED` with the accepted versions); the dashboard keeps showing the 12:45:25 snapshot with its
    visible `refreshState: ERROR` / `sourceError: "WP-P0-13 has an unsupported status."` until the reader accepts
    the word; the Lead makes NO change to `C:\LAB\WAYFINDER_DASHBOARD` (the staged W332 lane stays gated on an
    authorization marker that will not be written; spec retained for whoever repairs the reader). Session updates
    to the inbox still import normally (that path is unaffected).

## Addendum 57 - 2026-09-03 13:2x REAL (Lead record: P0-12 tables round 3-4; Wayfinder revisions 4-6; P0-14 fold launched)

- **W321 (RULE2-08 tables) verification rounds:** round 3 (Codex free) accepted the M1 binding, the four re-pinned
  catalog digests, the sealed projection values, the GREEN design-gap handling (`BLOCKED-OPEN-EMBED-05`, projection
  pair STOPPED), the probe check ids and the enumerated RED (11 nodes) / GREEN (9 nodes) golden deltas; two
  REQUEST_CHANGES remained: F-07 - PROBE-P012-02-A's comparator-first pointer must be the array pointer
  `/EVENT_SURFACE/cash_events` (the comparator returns the container on a list-length mismatch,
  `verify_bceg.py:1545-1549`), not `/EVENT_SURFACE/cash_events/0/signed_delta`; F-06 - stale design locators in the
  two inputs' `digest_reason` and the RED golden's provenance members (traceability only; economics unchanged). A
  narrow fourth pass (DeepSeek V4 Pro) fixed exactly those; the Lead LF-normalized and re-pinned the RED golden
  digest again (catalog sha `a94aca67...`); V321C round 4 is running. F-04 (manifest at seal #13) is deferred to the
  Lead's re-seal #14 by design.
- **Wayfinder session update:** revision 4 (13:03, imported) states decision 145 and the reader rejection;
  revision 5 (13:16, imported) added W331; its closeout still carried the question-146 text, so the Lead replaced
  that one section by hand and bumped to revision 6 (13:19): "No owner decision pending at this revision; 146 = (b)".
  Hours unchanged since revision 2 (no new lane with both endpoints evidenced was added by the builder; measured
  only, never estimated).
- **P0-14:** W331 fold (three T330-confirmed findings) launched 13:10:30 on Claude Pro after its reset; the fresh
  census (DeepSeek V4 Pro, `_packets_CENSUS_P014_R2`) is staged to run on its DONE; then back to the owner.
- **Route note:** DeepSeek author lanes need three to four verify-repair rounds on sealed-table work (locator drift,
  report accuracy); the substantive content was right from round 2. Codex free carried all four verify rounds.

## Addendum 58 - 2026-09-03 13:3x REAL (Lead handover: old session stopped; results of the last two lanes)

- Owner started the fresh session from `%TEMP%/HANDOFF_NEXT_SESSION_2026-09-03_AFTERNOON.md` (rev with section 0.5);
  the old session stopped launching (no two Leads in parallel). No lane running at handover.
- V321C round 4 (Codex): REQUEST_CHANGES with one metadata finding F-08 (RED golden `authored_value_tokens` ledger
  not synchronized with the fee/cash-event insertion; sealed tokens only, no economic number); F-06/F-07 CLOSED; all
  economics, digests, values and probe pointers ACCEPT; F-04 deferred to reseal #14. Next: narrow fifth pass, round 5.
- CENSUS-P014-R2 (DeepSeek V4 Pro, fresh census after W331): NOT CONVERGED - 0 HIGH / 1 MEDIUM / 2 LOW; the three
  T330 findings judged CLOSED; one new MEDIUM (N1) to be triaged cross-family before P0-14 goes back to the owner.

## Addendum 59 - 2026-09-03 14:0x REAL (Lead record, fresh session: W321 tables ACCEPTED after six verify rounds; P0-14 v1.10 CONVERGED and ready for the owner's word; W315 running)

- **W321 (RULE2-08 tables; decisions 137/144/138/140/143) - ACCEPTED by the Lead 14:0x.** Verification history (author
  DeepSeek V4 Pro through the repo harness, verifier Codex free): round 4 = REQUEST_CHANGES F-08 (the RED golden's
  `authored_value_tokens` ledger still described the pre-fee cash layout; sealed tokens only); fifth narrow pass moved the
  FUNDING entry's pointer to `cash_events/1/kind` and added the two FEE entries; round 5 = checks 1-5 ACCEPT, F-08 CLOSED,
  one locator finding F-09 (the correction entry named section W321-H where the sentence sits in W321-E, line 4769); sixth
  narrow pass appended W321-K; round 6 (scoped, final by the Lead's stopping rule) = ACCEPT: F-09 CLOSED, DERIVATIONS
  insertion-only against the pre-W321 snapshot, the four pinned input/golden digests equal the raw-file SHA-256, no byte
  moved since round 5. Current identities: catalog `74c9511607f28412...`, DERIVATIONS `8eeacb17be2a1d3d...`, RED golden
  `2157c03fc52daa91...`. F-04 (manifest still at seal #13) closes at the Lead's re-seal #14, by design.
- **Lead acts on sealed bytes, recorded:** (i) after each harness pass the Lead LF-normalized the written files and re-pinned
  the RED golden digest in the catalog by byte-level replacement (`repin_catalog_lf.py --write`; `95066157...` ->
  `2157c03f...`); (ii) the fifth-pass author overwrote the lane report with only its own section and re-typed the W315
  handoff table with two columns (dropping `comparator_first_differing_node`) - the Lead restored the round-4 report as
  the base and appended the fifth-pass text with a note; the raw fifth-pass file is kept
  (`W321_TABLES_M1_REPORT_fifthpass_raw.md`); the catalog was not changed by that pass; (iii) at 13:5x, with round 5
  accepting every value and digest, the Lead accepted W321 on values (conditional marker) so that W315 could start, and
  closed the marker unconditionally after round 6; (iv) one Lead slip: the marker file was first written into the build
  worktree by a shell cwd error and moved out within a minute, the worktree measured clean at `f37f2677` before W315 launched.
- **P0-14 (owner decision 145: "Complete its repair, run a fresh census, then bring it back to me").** After W331 the
  fresh census CENSUS-P014-R2 (DeepSeek V4 Pro) returned 0 HIGH / 1 MEDIUM / 2 LOW with the three T330 findings CLOSED;
  the cross-family triage T333 (Codex secondary) CONFIRMED the MEDIUM (a retained W292 change-log sentence saying the banner
  reads v1.8 after W331 bumped line 1 to v1.9, with the correction 87 lines away and no marker at the site - a different
  class from the T330-disputed banner findings) and specified the smallest insertion-only repair; lane W334 (DeepSeek V4
  Pro) inserted three `[W334 note]` lines and a v1.10 change-log section and bumped the header in place (Lead-measured:
  zero deletions, one modified line = the header, 18 inserted; LF; 1305 lines; sha256 `6a932c8f98017a94b6999de323cb62cc73a833f83d683882fc28c95a9ad78fb8`).
  CENSUS-P014-R3 (DeepSeek V4 Pro, fresh, read-only) on v1.10: **CONVERGED - 0/0/0**; N1-N3 CLOSED; T330 F01/F03/F04 still
  CLOSED. The draft carries two honest open items opened by W331 (`[OPEN-P014-PRODUCER-2]`, `[OPEN-P014-FINDING-RECORD-WRITER]`)
  and 18 open entries / 16 distinct questions in its own count; acceptance is for build planning only. **Owner word
  requested:** `accept design P0-14 v1.10` (packet `OWNER_ACCEPTANCE_PACKET_DESIGNS_2026-09-03.md`, Issue 3).
- **P0-12 chain:** W315 (probe variants on the post-K core + M4/M4b/08-A values; Codex fourth, xhigh) launched 13:52 on the
  clean worktree at `f37f2677`. Staged by the Lead for the next blocks: `reseal14.py` design pin v1.13 -> v1.15 (backup kept),
  W316 spec pin v1.15 (sha `137180ae...`, 1664 lines), launchers for W300C/W316, the fresh-audit specs W276C (Codex) /
  W279C (Claude Pro) / GM83C (Gemini 3.8, packet builder `refresh_gm83c.py`) on the seal-#14 snapshot with the disposition
  table for the previous round's 5 + 19 + 8 findings. Plan `PLAN_16H_2026-09-03_PM.md` rev 1 sent 13:37.
- Routes measured 13:35: Codex free / fourth / secondary all live; Claude Pro window 13:10-18:10; Gemini idle; DeepSeek
  V4 Pro carried the two author passes, the fold and both censuses; MAX orchestration only.

## Addendum 60 - 2026-09-03 14:2x REAL (Lead record: W315 accepted; RE-SEAL #14 executed; baseline regeneration W300C launched; no new owner decision)

- **W315 (Codex fourth, xhigh, 13:52-14:19) landed as one commit `af97ec8c` on the engine branch:** the nine KERNEL probe
  variants rebuilt on the post-K core (tree oid `efac9783...`; 0 patch conflicts; patch sha unchanged per probe; the
  Lead's own measurement of every variant against the live core = exactly one differing file, `economics.py`, 119
  members each, no extras); the M4/M4b/08-A expectation values written exactly as handed over by W312 (06-A) and W321
  (02-A, 08-A); the bundle catalog's nine PROBE rows re-pinned, RED/GREEN rows byte-identical; the gate refused only
  the predicted `DESIGN_PIN_MISMATCH`. **V315 (DeepSeek V4 Pro, read-only) = ACCEPT 6/6**; variant bytes themselves
  NOT VERIFIED by packet (stated) - covered by the Lead measurement above. W315 recorded three discrepancies; the one
  that matters for the owner: **two pre-existing manifest-versus-catalog `expected_first_changed_node` differences
  (PROBE-P012-03-A, INPUT-kind, and PROBE-P012-07-A)** lie outside the M4 fence (decision 140 names 02-A, 06-A, 08-A)
  and were NOT changed; the current validator binds `expected_failed_check` only, so both still validate. Recorded
  here as an open tables item for the fresh audits and, if they confirm it, for an owner word (no number invented).
- **Lead re-seal #14 executed 14:1x (`reseal14.py`):** `EXPECTED_SEAL_SHA` `e4ffde6a...` -> `a58b6dea753976a778413dca3e2cc13d47d2dee9b241bdc7d7cff9a04e3b5eba`;
  moved members against the pre-W311 snapshot: `scenario_catalog.json` (26 rows: input digests M1/M1b/M7/M7b, the
  sealed projection members M6 on 17 rows, the nine PROBE rows), `DERIVATIONS.md` (insertion-only, verified),
  `golden/corrected_vnext/RULE2-08-RED.json` and `RULE2-08-GREEN.json` (decision 144 chain); design pin v1.15 (sha
  `137180ae...`, 1664 lines, heading map re-measured); anchor base `5e8e5794` (M5); `files[].bytes` and sha updated;
  `VERIFIED_BY` names twelve verify reports (V306/V306B, V311, V312, V313, V314, V317, V318, V319, V320C r2, V321C r6,
  V315). Catalog sha at seal #14: `555c4441b40c3f6fe5e00729f7d4d496c9a5cf78215fcfddd82d6243d2a7bb14`. Backup of the
  four pre-seal files in `C:/tmp/P012_LEAD_RESEAL/pre_reseal14_backup`. Structural note for the audits: the manifest
  `files[]` carries the catalog, DERIVATIONS and the 17 goldens (19 members); the sealed INPUTS are bound through the
  catalog rows' `input.digest` members, not listed directly (unchanged structure since seal #10).
- **Baseline (decision 132 shape, third run):** the seal-#13 run archived whole to
  `C:/tmp/P012_BASELINE_RUN_seale4ffde6a_archive/out` (36 files, byte-identical copy verified), live `out/` removed,
  dry-run 17/17 ready at driver sha `b7648f71...` and catalog `555c4441...`, Lead note
  `LEAD_DRYRUN_NOTE_2026-09-03_SEAL14.md`. Expected regression: exactly FIVE scenario surfaces may differ from the
  seal-#13 archive (RULE2-06-EQUAL-PRICE-RED, RULE2-06-RED, RULE2-06-GREEN, RULE2-08-RED, RULE2-08-GREEN - the inputs
  the owner's decisions moved); every other surface byte-identical. **W300C launched 14:22 on Codex free.** Next:
  W316 (in-repo copies to seal #14 + design pin v1.15 + one gate run; Codex secondary) -> fresh audits W276C (Codex),
  W279C (Claude Pro, 18:10 window), GM83C (Gemini 3.8; no git writes while it runs) on that exact snapshot.
- Wayfinder: new session `2026-09-03T1332-claude` revision 1 OPEN_PROVISIONAL imported by the dashboard at 14:07
  (measured hours only: WP-P0-12 0.21 h, WP-P0-14 0.35 h; Lead time NOT RECORDED).

## Addendum 61 - 2026-09-03 15:3x REAL (Lead record: the seal-#14 snapshot's gate list; two Lead misses corrected (#14b, provenance record); W300C baseline identical; no new owner decision)

- **W300C (Codex free, 14:22-14:4x; decision 132 shape, third run):** 11/11 preconditions PASS, one run, 17/17 legacy arms;
  regression against the seal-e4ffde6a archive: **34/34 scenario surfaces byte-identical**, including the five scenarios
  whose sealed inputs moved (the legacy kernel does not read the corrected-only members `target_book` /
  `cost_schedule_id`); only `run_status.json` (catalog sha + five `input_sha256` members) and its checksum line differ.
  The Lead's expectation sentence in the spec ("five surfaces may differ") was wrong in the safe direction and is recorded
  as the lane's W300C-F01. Baseline manifest sealed to #14 (sha `d522debe...`).
- **W316 (Codex secondary):** five in-repo copies + design pin v1.15 (`d574a405`), then the two RULE2-08 goldens and five
  inputs (`de0a2404`). Lead spec defect: the golden/input copies were listed after the "Do" list, so the lane ran its
  single gate BEFORE them and the gate refused at the first stale member. **W316B (`443457d7`) ran the gate on the
  complete snapshot: 16 refusals, 9 of 10 probes DETECTED.** Classes: (a) the missing section-16 review record (expected);
  (b) `IMPLEMENTATION_BASE_ANCESTRY_MISMATCH` - the bundle manifest's `seal` / `seal_state` `IMPLEMENTATION_BASE_SHA` still
  read `108ea066` while the anchor read `5e8e5794`: the Lead's M5 script had re-pinned the anchor only. **Corrected by the
  Lead as re-seal #14b** (two members moved to the anchor's value; `EXPECTED_SEAL_SHA` is computed over `files[]` only and
  is UNCHANGED at `a58b6dea...`; `reseal_history` records it; backup kept); (c) ten `OBSERVED_ARTIFACT_STALE` on
  RULE2-06-RED / -EQUAL-PRICE-RED / -GREEN and RULE2-08-RED / -GREEN (1.0.0 and 2.0.0) - the committed observed files
  predate the owner's input changes; W316C materialized exactly those ten by the harness's own `--mode observe`; (d) the
  decision-134 provenance exception record (`contracts/expected_provenance_exceptions.json`) still bound to base
  `108ea066` - W316C's gate refused `EXPECTED_PROVENANCE_EXCEPTION_INVALID` and stopped honestly without committing;
  **W316D (Codex free, launched 15:2x)** commits the W316C work and re-measures that record at the M5 base (read-only git;
  the owner-134 authorization is unchanged), then runs the gate once; (e) **four substantive items, untouched, for the fresh
  audits:** PROBE-P012-02-A NOT DETECTED (expected `CORRECTED_EXPECTATION`, measured `CLOSED_SET_VIOLATION` at
  `/RESULT_SURFACE/admitted` - a decision-143 value that must come from the design's check order, never from the run);
  `OBSERVED_EXTRA_MEMBER` `/RESULT_SURFACE/run_manifest/cost_schedule_digest` on both RULE2-08 rows (the kernel emits the
  member, the golden says ABSENT - a closed-set naming question, design 23.4); `CORRECTED_EXPECTATION_MISMATCH` on
  RULE2-08-RED `/EVENT_SURFACE/cash_events` (kernel two-item array vs the tables' fee/funding array; exact values not
  emitted by the receipt). No RULE2-01-GREEN provenance refusal appeared.
- **Audit specs updated** to name these known refusals as objects to judge (kernel vs design vs tables, inside/outside
  decisions 135-144), not as surprises. The audits (W276C Codex fourth, W279C Claude Pro, GM83C Gemini 3.8) start on
  W316D's HEAD. Routes: Codex secondary capped until 17:12 after three lanes; free and fourth live; Claude Pro window to
  18:10.
- Wayfinder session 2026-09-03T1332-claude revision 2 imported 15:06 (WP-P0-12 1.28 h, WP-P0-14 0.35 h, measured lanes
  only). Owner word still pending: `accept design P0-14 v1.10`.
