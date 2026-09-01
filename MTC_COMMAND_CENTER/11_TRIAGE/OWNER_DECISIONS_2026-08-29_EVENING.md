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
