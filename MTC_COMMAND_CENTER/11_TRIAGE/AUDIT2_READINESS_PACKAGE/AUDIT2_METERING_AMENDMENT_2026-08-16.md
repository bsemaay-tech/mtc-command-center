Status: METERING AMENDMENT DRAFT — FOR LEAD REVIEW — implements owner decision §4 of 2026-08-16

# Audit 2 metering amendment (draft for Lead review)

Amends `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md` (its §2 dispatch plan, §6 reserve conclusion, §7 measurement record). The Lead applies this text to that plan; this file edits nothing, dispatches nothing, accepts nothing, authorizes nothing, and spends no pool time. It adds measurement only — no auditor, no round, no verdict rule changes; roster, effort, independence, and verdict standards stay exactly as the dispatch plan and `AGENTS.md` fix them.

Authority — owner decision 2026-08-16 §4, adopted verbatim: "The six-hour pool stays a hard cap and I accept BLOCK if it is exhausted; meter both Audit 2 sessions and bring me the measured actuals before Audit 3/Gate 6 so I can set that reserve on evidence, not a guess." (`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:47-51`). Decision 4 "changes no artifact today; it binds the Audit 2 dispatch plan (metering both sessions is now mandatory)" (`OWNER_DECISIONS_2026-08-16_MORNING.md:80`). The dispatch plan already requires the measurement fields (`AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:166-177`); this amendment supplies the missing mechanism: meter lines, recording roles, cap arithmetic, stop semantics, and the owner block.

Citation aliases (paths repo-relative to the snapshot at `C:\RO`, `c84497c8`):

- **[DEC]** = `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md`
- **[DISPATCH]** = `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md`
- **[INPUTS]** = `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md`
- **[PLAN50]** = `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md`
- **[WBD]** = `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md`
- **[ROUTING]** = `MTC_COMMAND_CENTER/_AI_MEMORY/AI_ACCOUNT_AND_MODEL_ROUTING.md`
- **[RUNLOG]** = `MTC_COMMAND_CENTER/11_TRIAGE/PATHSCOPE_RETRY_CODEX_RUN_2026-08-15.log`
- **[BURN]** = `MTC_COMMAND_CENTER/09_DOCS/AI_TOOLING/pilots/codeburn_pilot.md`
- **[AGENTS]** = `AGENTS.md`

## 1. What is metered

**Primary meter (binding): wall-clock elapsed time per auditor session**, taken from two lines the auditor itself writes into its own verdict file (the one-report/one-verdict contract of [INPUTS]:118-124; recommended names `AUDIT2_CLAUDE_T0_<date>.md` / `AUDIT2_CODEX_T0_<date>.md` at [DISPATCH]:61-66).

START line — the first content line of the report, written **before any audit work begins** (the same prove-your-session-first pattern the Codex Pathscope audit already used for its session header, [RUNLOG]:52-60):

```
METER: START <YYYY-MM-DDThh:mm:ss±hh:mm> session=<ID> model=<exact> effort=<exact> worktree=<resolved path> frozen_sha=<full frozen SHA>
```

STOP line — the last line of the report, written after the verdict is decided:

```
METER: STOP <YYYY-MM-DDThh:mm:ss±hh:mm> session=<ID> verdict=<PASS|PASS-WITH-NITS|REQUEST_CHANGES|BLOCK> round=<1|2|3>
```

Timestamps are wall-clock ISO-8601 with explicit offset (working convention +03:00, [DEC]:3), both lines from one clock. Session IDs: `AUDIT2-CLAUDE-R<n>` and `AUDIT2-CODEX-R<n>`; `R1` is the first pass, `R2`/`R3` re-audit rounds under the T0 cap of three ([AGENTS]:33-35).

**Charged elapsed = STOP − START, full wall-clock, no deductions.** The finer breakdowns [DISPATCH]:169-175 already requires (active review vs mandated-suite runtime vs evidence reproduction vs report writing, plus commands/counts/findings) remain required report content for the owner review, but none of them reduces the charged amount.

**Secondary meter (record only where the route reports it): per-session tokens/cost.** These never gate the pool — the pool is denominated in hours ([PLAN50]:845-847); they are context for the owner's reserve decision.

| Route | Wall-clock | Tokens | Cost |
|---|---|---|---|
| Claude `claude-opus-5` effort `xhigh` ([AGENTS]:54-61) | Measurable — the auditor's own START/STOP lines; Lead cross-check from its independently captured dispatch/completion times. | Measurable post-hoc at model level: `codeburn` reads local Claude session logs (`~/.claude/projects/...`) and reports per-model token totals and a JSON export ([BURN]:6, [BURN]:11). **Per-session attribution for one named audit session: UNKNOWN** pending a live export check. The auditor writes a token figure only if its route prints one to it — never an estimate of its own. | **UNKNOWN by construction** — Claude Pro/Max are flat subscriptions, not per-token billing ([ROUTING]:223-226); any `codeburn` dollar figure is a LiteLLM-priced estimate and must be labeled as such, never invoiced spend ([BURN]:31). |
| Codex `gpt-5.6-sol` effort `xhigh`, always via the mandatory launcher ([ROUTING]:39-43) | Measurable — same START/STOP lines; the launcher preserves the child exit code and the Lead captures the run log ([ROUTING]:43). | Measurable — the Codex CLI prints a per-session `tokens used` figure at session end; the two real sessions captured in [RUNLOG] printed `279.452` and `77.940` ([RUNLOG]:15268-15269, [RUNLOG]:16076-16077). Record verbatim; the unit is unlabeled in the captured output, so the unit is **UNKNOWN** — never converted. | **UNKNOWN by construction** — Plus/Pro subscriptions ([ROUTING]:17-22); `login status` proves login only and reports neither quota nor spend ([ROUTING]:97-99). |

**UNKNOWN for both routes:** remaining account/window quota at session time is not readable from any repo artifact — provider console only ([ROUTING]:97-99).

## 2. Who records, where

- **The auditor records its own clock.** The two METER lines above become part of the required verdict-file contract for both flagship sessions. Each auditor writes only its own lines; neither session sees the other's anything before both initial verdicts are sealed ([INPUTS]:16-18, [DISPATCH]:39-41).
- **The Lead transcribes both sessions into one actuals table**, in one new file per checkpoint, recommended `AUDIT2_METERED_ACTUALS_<date>.md` placed beside the sealed reports. Exact template:

| Session | Auditor | Start | Stop | Elapsed (min) | Tokens/cost (if known) | Verdict | Repeat-rounds consumed |
|---|---|---|---|---|---|---|---|
| AUDIT2-CLAUDE-R1 | claude-opus-5 xhigh | | | | | | 0 of 3 after R1 |
| AUDIT2-CODEX-R1 | gpt-5.6-sol xhigh | | | | | | 0 of 3 after R1 |
| LEAD-REPRO-A2 | Lead | | | | n/a | n/a (finding reproduction) | n/a |

- Fill rules: Start/Stop verbatim from the sealed METER lines; Elapsed = the difference in minutes; tokens/cost verbatim from the route or `UNKNOWN`; Verdict from the report's single overall verdict ([INPUTS]:120-121); repeat-rounds = rounds consumed at that checkpoint once this session closes, against the T0 cap of three ([AGENTS]:33-35, [PLAN50]:853).
- The `LEAD-REPRO-A2` row is mandatory whenever the Lead reproduced any required finding — Lead reproduction time is part of the measured amount charged to the pool ([DISPATCH]:177).
- Provenance rule: every cell comes from a sealed report line or a captured run log/launcher capture; nothing is reconstructed from memory.

## 3. Cap accounting

- The pool is the single WP-R **6 h audit-only** reserve funding Audit 2, Audit 3, Gate 6, and every re-audit; it funds no implementation or repair, and exhaustion while a required audit remains is BLOCK ([PLAN50]:845-847). R21/R24 remain `NO SOURCED ESTIMATE` until these actuals exist ([WBD]:60, [WBD]:63).
- **Accounting default, binding until the owner rules otherwise: additive per-session hours.** Every session's full elapsed charges individually; running the two Audit 2 sessions in parallel does not compress their charge. [DISPATCH]:158 records that the Plan does not state additive-labor vs elapsed-wall-clock accounting — that **UNKNOWN** stands; the additive default is the conservative reading for a hard cap and matches the dispatch plan's own statement that parallel execution "does not create more aggregate auditor-session hours" ([DISPATCH]:158). The §4 block explicitly asks the owner to confirm or replace this default.
- Charged amount after Audit 2 = both auditor sessions' elapsed + Lead reproduction elapsed ([DISPATCH]:177). Remaining pool = 360 min − charged to date, carried forward across checkpoints and re-audits.
- **Pre-dispatch check — every session, every round:** the Lead computes the remaining pool before launching. Remaining ≤ 0 with a required session outstanding → do not dispatch; write the BLOCK record below.
- **Exhaustion mid-review:** the Lead stops the session visibly at the moment cumulative charge reaches 360 min. The stop is external and is recorded by the Lead in the actuals file — never inside the auditor's report — as:

```
METER: EXTERNAL-STOP <YYYY-MM-DDThh:mm:ss±hh:mm> session=<ID> reason=POOL-EXHAUSTION
```

Stop semantics: the review **stops visibly** (the session is not "finished"); partial findings are preserved exactly as written, each labeled `PARTIAL — STOPPED AT POOL EXHAUSTION`; **nothing is silently finished** — an externally stopped session cannot return PASS or PASS-WITH-NITS, because an incomplete or non-executed review is never acceptance ([AGENTS]:87, [INPUTS]:102-104), so its outcome is BLOCK with the partial annex; elapsed charges to the external-stop timestamp.
- **BLOCK record sentence** (fill the brackets, keep the structure verbatim):

```
BLOCK — WP-R audit reserve exhausted: charged <X h Y min> of the 6 h pool
(sessions: <each session ID with elapsed, plus Lead reproduction>), with
<N> required audit/re-audit session(s) outstanding (<IDs>). Per the 50-hour
plan §20 the overrun is not contingency-funded and no other work package may
fund it ([PLAN50]:845-847); per owner decision 2026-08-16 §4 the six-hour pool
remains a hard cap and BLOCK on exhaustion is accepted ([DEC]:47-51). Partial
findings from the stopped session are preserved and labeled partial at
<file:lines>. Repairs are not funded from this pool ([PLAN50]:851).
```

## 4. The owner review — exact fill-in block, presented before Audit 3/Gate 6

Present this block to Barış after both Audit 2 reports are sealed and the actuals table is complete ([DEC]:47-51; [DISPATCH]:177):

```
## Audit 2 metered actuals — owner review before Audit 3/Gate 6

Pool: the single WP-R 6 h (360 min) audit-only reserve covering Audit 2 +
Audit 3 + Gate 6 + all re-audits ([PLAN50]:845-847). Charged by Audit 2:
<X h Y min> (Claude <..> min + Codex <..> min + Lead reproduction <..> min).
Remaining: <X h Y min>. Two further first-pass xhigh flagship sessions
(Claude + Codex for combined Audit 3/Gate 6) are still required
([AGENTS]:33-35; [DISPATCH]:74), leaving an arithmetic average of <X min>
per remaining first-pass session before any re-audit.

[transcribe the AUDIT2_METERED_ACTUALS table here, verbatim]

Tokens/cost as reported by the routes: <verbatim figures, or UNKNOWN per
route and why>.

Accounting used: additive per-session hours (parallel sessions charge in
full). The plan does not state its accounting ([DISPATCH]:158); confirm or
replace it below.

Question: on these measured actuals, do you (a) keep the six-hour hard cap
as is — accepting BLOCK on exhaustion for Audit 3/Gate 6 and any re-audit —
or (b) authorize and ratify a specific larger audit-only reserve and state
its accounting (additive per-session hours vs elapsed wall-clock)? Repair
funding stays separate and is never borrowed from or into this pool
([PLAN50]:851).
```

If Audit 2 itself exhausts the pool, the §3 BLOCK record accompanies this same block — the owner review happens before Audit 3/Gate 6 in every case.

## 5. Check honesty — what makes each rule fail

1. **Missing START line** → start falls back to the Lead's captured dispatch timestamp; if neither exists, elapsed is `UNKNOWN` and charges at the full remaining pool — never zero.
2. **Missing STOP line** → elapsed is `UNKNOWN` and counts as consumed at the cap, never as free time; an auditor that cannot close its own clock cannot discount it.
3. **Clock divergence or backdating** (the auditor's pair disagrees with the Lead's independent captures by >5 min) → record both values and charge the larger elapsed.
4. **Tokens/cost absent, unlabeled, or garbled** → record `UNKNOWN`; never infer tokens from output length, report size, or duration; never assign a unit to the unlabeled Codex figure; never present a codeburn estimate as invoiced cost.
5. **Additive default quietly swapped for elapsed accounting** (parallel sessions charged once) → understates consumption; only the owner may change the accounting, in writing, in the §4 block — until then the additive remaining figure is restated before every dispatch.
6. **Lead reproduction left unmetered** → the pool is under-charged; repro time is part of the measured amount ([DISPATCH]:177), so a missing repro row is a defect in the actuals table, not a saving.
7. **An externally stopped session still issues an accepting verdict** → invalid; incomplete review is never acceptance ([AGENTS]:87) — the outcome is BLOCK plus the partial annex, and the attempt is recorded.
8. **Actuals reconstructed after the fact** → transcription comes only from sealed METER lines and captured run logs; any cell without provenance is `UNKNOWN`, not a recollection.
9. **Pre-dispatch check skipped** (a session launched against an empty pool) → the launch is itself the BLOCK trigger, recorded in the §3 sentence with the just-launched session counted among the outstanding.
