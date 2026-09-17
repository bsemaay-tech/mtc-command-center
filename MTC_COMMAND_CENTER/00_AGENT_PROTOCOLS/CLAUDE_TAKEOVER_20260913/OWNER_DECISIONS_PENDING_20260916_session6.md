# Owner decisions pending — batched (2026-09-13)

> **Status at 13:55Z (reconciled per Mentor M002):**
> - **ANSWERED and recorded:** D1 (Option A; applied in V1.1/V1.2 re-freeze), D-P20-1 (YES; row OD-20260913-P020-SCOPE-1), D-P20-2 (YES; row OD-20260913-P020-BENCH-1), D-P20-3 (YES; row OD-20260913-P020-WRITER-1) — CT13 commit c064acc6. Not blockers.
> - **NOW PRESENTED (17:22Z):** D2 — WP-P0-12 ratification of seals #36–#39: the receipt/checker package is finished and the scratch gate dry-run passed; the concrete request is `C:/tmp/CLAUDE_P0_RUN_20260913/P012_RATIFICATION_REQUEST_20260913.md` (CT13 commit 3b5cee79). Owner act pending.
> - **NEW, not yet presentable:** P031 OD-1..OD-12, P030/P026 O-1..O-10, P013 plan — DRAFT packets under correction (Grok BLOCKING findings; V2 in progress). Do not answer until V2 is Lead-re-audited.
> - **Veto window (non-blocking):** Sol (Codex free) T0 round 2 on P020 V1.2 will be launched after Opus round 2 + Grok pre-screen pass unless the owner says "no Sol round 2".

**ANSWERED 2026-09-13 (owner chat, verbatim in CT13 DECISIONS.md rows OD-20260913-P020-SCOPE-1 / -BENCH-1 / -WRITER-1):** D1 = Option A; D-P20-1 = YES; D-P20-2 = YES (reporter unchanged); D-P20-3 = YES (P020 owns identity.py and mega_walk_forward.py while active). P012 ratification: owner will sign only a finished receipt/checker package with the concrete #36-#39 request.

Recommendations first; each item states the consequence of each choice. Nothing below is executed until you answer.

## D1 — WP-P0-20 benchmark preselection: the 1D calibration window

Fact: the only BTCUSDT 1D dataset has 2,409 derived rows. Measurement locks rows 1..2048, so only rows 2049..2409 (361 rows) are disjoint. The frozen 2048-row calibration window exists for 15m/1h/2h/4h but cannot exist for 1D. Indicator warmup is up to 200 bars, so the 1D tail leaves about 161 usable bars. Evidence: `C:/tmp/P020_PRESELECT_20260913/PRESELECTION_PREREG_V1.md` section (d); `REPORT.md` section 4.

- **Option A (recommended): asymmetric window.** 1D calibrates on its maximal disjoint tail (rows 2049..2409, already hashed `bc763cd0…`); the other four keep 2048 rows. Keeps five timeframes and strict disjointness. Consequence: 1D eligibility rests on weak evidence, so a false block is more likely; a false block ends as `BENCHMARK_PROFILE_BLOCKED` (fail-closed, no silent substitution) and comes back to you.
- Option B: drop 1D, run four timeframes. Consequence: contradicts "preserve exactly five BTCUSDT timeframes"; the plan validator expects five.
- Option C: shorten all five calibration windows to 361 rows. Consequence: every timeframe loses evidence, not just 1D.
- Option D: acquire longer 1D data. Consequence: new data acquisition; outside current authorization.

After your choice: amend and re-freeze the preregistration, then run the exact T0 review (Opus xhigh + Sol xhigh + Gemini 3.7) on the frozen bytes, then the one-shot eligibility check. If the eligibility check returns BLOCKED, I stop and report; no second selection.

## D-P20-1 — Record the WP-P0-20 scope amendment row `OD-20260913-P020-SCOPE-1`?

Text as drafted in `C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P020_SCOPE_DECISION_PACKET_20260913.md` section 4: narrows WP-P0-20's current acceptance object to the reviewed research/engineering deliverable at head `b9b72f85` (Option 1 zero-minima carrier, typed TIME_STOP, owner-policy binding, the preregistered benchmark once executed), label "P0-20 research/engineering scope complete; package acceptance and production admission pending", four OPEN preconditions (fresh T0 roster on the frozen head, benchmark eligibility outcome, 17/17 control-coverage re-attested, current-master reconciliation).
- **Recommended: Yes, record it.** Consequence: a truthful label becomes available once the preconditions are met; the acceptance reporter still prints 8/16 NOT ACCEPTABLE; nothing downstream moves; P0-13's B-01 stays open (`WAIT_P020_ACCEPTANCE`).
- No: work stays under the undifferentiated 8/16 state and every status must re-explain the engineering-versus-acceptance gap.

## D-P20-2 — May `check_p020_acceptance.py` gain a research-closure criterion set?

- **Recommended: No; 8/16 stays the reported number under the label.** The reporter carries package truth; editing it is T0 acceptance logic needing a full fresh roster and risks a number reading as progress toward acceptance when none occurred.
- Yes: schedule a T0-reviewed reporter change; nothing else changes.

## D-P20-3 — Single-writer assignment for shared files

`MTC_COMMAND_CENTER/contracts/mtc_contracts/identity.py` is changed by both P0-13 (head `1e9682ba`) and P0-20 (head `fa57a771`) from the same base blob `75289fa6`; `mega_walk_forward.py` is P0-20's protected surface and P0-13's future caller target.
- **Recommended: P0-20 is the sole writer of both while WP-P0-20 is active; P0-13 coordinates and rebases at integration.** Consequence: the collision is resolved before it becomes a merge conflict on two protected surfaces.
- Leave open: both branches keep diverging and P0-13's shared-path stop condition fires at integration.

## D2 — WP-P0-12 ratification (will be presented after the formal Section-16 review completes)

Placeholder: the six-item Gemini 3.8 review is running in parts. When it is complete and checked, I will present the receipt, the reseal chain #36-#39, and the acceptance amendment row for your ratification words. No ratification is applied before that.

## D3 — WP-P0-14 read-only report: the amendment text cannot be located (raised 19:19Z)
Owner decision F YES authorized "the small reproducible read-only report that the P0-14 sequencing amendment allows". The Codex lane and the Lead searched the plan (`### WP-P0-14`, lines 419-432), DECISIONS.md, OWNER_MASTER_PLAN, the traceability register, the explorer fold, the P014 Lead work dirs and the takeover handoffs: the only text is START_HERE.md line 54 ("Owner chose to defer Minimum Explorer behind core Bridge engineering with a small reproducible read-only report meanwhile. Preserve sequencing amendment"). No recorded amendment defines what the report contains or which read-only sources it reads. The lane stopped rather than invent a scope.
**Question:** where is that amendment recorded, or what should the report show (e.g. the current candidate families with lifecycle state and rejection reasons from the P031 M1 ledger fixtures; or the P013 catalog summary)? Recommended: name the two or three questions you want answered from read-only data; the Lead then writes the reproducible report to that scope.

## D4 — P0-20 V1.4: one more exact Opus review on Claude Pro? (raised 19:50Z)
Sol round 3 found three real time-of-check/time-of-use gaps in V1.3 (token vs re-parsed bytes; plan re-read after preflight; ABORTED written to only one file on a final-write failure). Opus round 3 had passed it. A V1.4 repair is being built on Codex Plus (no Claude). REVIEW_POLICY T0 needs BOTH exact flagships on the reviewed bytes. Your cap was "I: round 3 only".
**Question:** YES = authorize one exact claude-opus-5 review of V1.4 on Claude Pro (Sol on Plus, Gemini and Grok run regardless). NO = V1.4 waits at Sol + Gemini + Grok + Lead and eligibility does not run until you decide. Recommended: YES (one review; without it the P0-20 chain stops tonight).


## D5 — WP-P0-20 measurement driver accepts only the ORIGINAL five families (raised 2026-09-14 05:30Z) — **ANSWERED 06:47Z: "D5 A"** (row OD-20260914-P020-DRIVER-FAMILIES-1; folded into V1.5 lane P20R6 6b; gated on D6)
Fact (Lead-verified): `C:/tmp/P020_LEAD_20260912/benchmark/run_bounded_benchmark.py:181-185` refuses any plan whose five families are not exactly `GEN_TRIPLE_EMA_STACK, GEN_MACD_BULL_CROSS, GEN_DONCHIAN_BREAKOUT, GEN_ATR_PULLBACK_TREND, GEN_GOLDEN_CROSS_PULLBACK` (`PLAN_INVALID`). The preregistered preselection (V1.4) may select any five distinct families out of nine; the derived plan for any other matching cannot be consumed by the existing driver. Found by the Grok pre-screen of the plan-derivation tool (GKPD finding 2). The driver is a pinned P020 source (`implementation_sources`), so changing it is engineering on the P020 surface with a new T0 roster.
- **Option A (recommended): authorize a bounded driver change** — replace the hard-coded set with "five distinct families, each present in the frozen `family_order`, each with sizes 512/1024/2048", reviewed by the full T0 roster (exact Opus + Sol + Gemini + Lead) before any measurement. Consequence: one more reviewed change on the P020 surface; the derived plan becomes consumable for whatever matching the oneshot records.
- Option B: keep the driver as is; the measurement runs only if the oneshot selection equals the original five families; otherwise the chain stops at `BENCHMARK_PROFILE_BLOCKED`-equivalent (PLAN_INVALID) and returns to you. Consequence: high chance the preregistered selection is unusable; no driver work.
- Either way the derivation tool itself needs the single-read repair (GKPD finding 1) and the V1.4 re-pin before its own review.

## D6 — P020 V1.4 one-shot ABORTED before any result: the synthetic instrument record does not cover the 15m calibration window (raised 2026-09-14 06:12Z)
Fact (Lead-verified with pure calls; `P020_ELIGIBILITY_RUN_V14/LEAD_TERMINAL_ELIG14.md`): the full round-4 roster accepted V1.4 (Opus + Sol PASS-WITH-NITS, Gemini PASS, Grok NITS, Lead REPRODUCED) and the one-shot started at 05:57Z with the token; the very first calibration cell (family 1 × 15m) raised `InstrumentRecordRefusal: REFUSED_INSTRUMENT_RECORD_OUT_OF_RANGE` because the reviewed synthetic instrument record `SYNTH-P020-BOUNDED-INSTRUMENT-V1.json` ends at `end_exclusive = 2025-09-22T08:00:00Z` — exactly the first timestamp of the 15m calibration window (row 2049). The record was sized for the measurement prefixes (rows 1..2048) only. Both outputs are ABORTED records; the shot is spent by the tool's own rule; **no signal, simulation, matrix, selection or trial was ever computed or seen**. All five reviewers had listed the real profile stack under NOT VERIFIED — a declared-but-unchecked input precondition, not a selection-rule problem.
- **Option A (recommended): repair as V1.5 and re-run once.** (1) Owner ratifies an extended synthetic instrument record V2 (same values; `end_exclusive` moved past the last calibration/measurement timestamp, e.g. `2026-05-01T00:00:00Z`; provenance `human_reviewer` = you; digest re-pinned in `BENCHMARK_PLAN.json` and the frozen artifact). (2) Builder adds a freeze-time check to `preselect_profile.py`: every calibration window's first and last timestamp must lie inside the pinned instrument record interval, refusing `PRESELECT_REFUSED_RECORD_INTERVAL` (plus the six round-4 NIT residuals), re-freezes V1.5. (3) Round-5 roster: Lead + Grok + Gemini 3.7 + Sol (Codex Plus) + **one more exact Opus on Claude Pro** (needs your authorization, like D4). (4) You rule that the spent V1.4 shot may be reset: the two ABORTED files are archived under `P020_ELIGIBILITY_RUN_V14/ABORTED_ARCHIVE/` with their digests (never deleted) so the V1.5 one-shot can reserve fresh outputs. Consequence: one more build + review round (~2-3 h of lanes; one Pro Opus slot); no selection rule changes; nothing was seen, so "do not change selection rules after seeing results" is not engaged.
- Option B: drop the 15m timeframe (four timeframes). Consequence: contradicts "preserve exactly five BTCUSDT timeframes" and the plan validator; the record still needs no change.
- Option C: stop the P020 preselection chain here. Consequence: P020 stays at 8/16; P013 B-01 stays blocked; the measurement plan derivation (D5) becomes moot for now.

## D7 — P020 V1.5 one-shot returned BENCHMARK_PROFILE_BLOCKED (no complete matching of 5 families to 5 timeframes) (raised 2026-09-14 10:45Z)
Fact: the full roster accepted V1.5; the one-shot ran all 45 calibration cells on the real data and found no assignment of five distinct families to the five timeframes in which every cell is trade-bearing. This is the fail-closed outcome you accepted in D1 Option A ("a false block ... ends as BENCHMARK_PROFILE_BLOCKED and comes back to you"). By design the tool does not record WHICH timeframe(s) had no eligible family; the Lead verified with one real cell (family 1 × 15m: trade-bearing) that the block is genuine, not an environment defect (`P020_ELIGIBILITY_RUN_V15/LEAD_TERMINAL_ELIG15.md`). The D1 discussion flagged the 1D window (361 rows, 161 usable after warmup) as the likely weak spot; that is a hypothesis, not a measurement.
- **Option A (recommended): authorize a bounded DIAGNOSTIC read, then decide.** The Lead re-runs the 45-cell binary gate matrix in a scratch copy WITHOUT any matching or selection and reports only, per timeframe, HOW MANY of the nine families are trade-bearing (never which ones), so you can see whether 1D (or another timeframe) is the empty column. Consequence: reveals counts only; the preregistration's "no selection on visible results" stays intact because no family identity or economic value is reported; the spent shot stays spent; you then choose B/C/D below with evidence.
- Option B: revise D1 — accept a four-timeframe profile (drop 1D) and re-freeze V1.6 with a new roster and a new shot. Consequence: contradicts "exactly five BTCUSDT timeframes"; plan validator and driver rule (five timeframes) must change too — engineering + T0; only sensible if the diagnostic shows 1D is the empty column.
- Option C: revise D1 — acquire longer 1D history (Option D of the original D1) so 1D gets a full 2048-row calibration window disjoint from the measurement prefix; re-freeze V1.6 (new data pin) + roster + shot. Consequence: data acquisition lane (outside current authorization), then the same review cycle.
- Option D: stop here. P020 stays 8/16; the measurement plan (B YES) has nothing to derive from; P013 B-01 stays blocked.
Nothing runs until you answer; the Lead recommends A first (cheap, ~5 minutes, no policy change).

## D7 — ANSWERED "D7- A" (10:55Z) → result: 15m 4/9, 1h 0/9, 2h 0/9, 4h 1/9, 1D 0/9 trade-bearing families; all blocks = "no actual trade-bearing 2.1.0 successor result"
## D8 — why do three timeframes have zero trade-bearing families? (raised 11:00Z)
- **Option A (recommended): one more bounded diagnostic, still no selection.** Per timeframe, count families with ≥1 entry signal vs families with ≥1 fill, and the refusal sub-reason (signal-but-no-fill = sizing/policy problem such as the synthetic instrument's `quantity_step = 1` at BTC prices; no-signal = strategy/window problem). Identities withheld. Consequence: tells you whether the preregistration is measuring the strategies or a sizing artefact before you spend anything on V1.6.
- Option B: skip diagnosis; revise the preregistration (windows/data) and re-freeze V1.6 + roster + shot. Consequence: likely the same block if the cause is sizing.
- Option C: stop P020 here.

## D8 — ANSWERED "D8 A" (~11:05Z) → 8 of 9 families SIGNAL on 1h/2h/4h but get NO FILLS: lot quantization (synthetic `quantity_step = 1` at BTC prices, risk fraction 0.0001 floors the quantity to 0). 1D additionally short of signals.
## D9 — resolve the sizing artefact before any V1.6 (raised 11:12Z)
- **Option A (recommended): synthetic instrument record V3 with the venue-realistic quantity step** — `quantity_step = 0.00001` (Hyperliquid BTC per the closure matrix row I-3; `minimum_quantity` stays 0, `minimum_notional` 0 as today), same ratification path as V2 (your word; record stays SYNTHETIC_LABELLED, benchmark-only), then V1.6 re-freeze + roster + new shot. Consequence: the eligibility test measures strategies, not rounding; one more review round (exact Sol on Codex Plus; **Claude Pro is at 0.81 weekly — one more Opus review may not fit before the weekly reset; you may have to accept Sol + Gemini + Lead + a later Opus, or wait**); the same fix unblocks the 15 measurement trials.
- Option B: raise the P020 owner-policy risk fraction (`OD-20260912-P020-VALUES-1`, 0.0001) instead. Consequence: changes your economics policy to work around a synthetic record; not recommended.
- Option C: stop P020 here.


## D9 — ANSWERED "1. D9-A" (12:59Z) → OD-20260914-P020-RECORD-V3-1; V1.6 build P20R7 queued first on Codex Plus (15:08Z)
## Opus slot — ANSWERED "2. Last Opus slot this week it goes to the P020 V1.6 roster" → OD-20260914-P020-OPUS6-1
## D10 — ANSWERED "3. D10 Yes" → OD-20260914-GEMINI-WRAPPER-2 (wrapper repaired 13:06Z, hash eff6a727…)
## TESTNET — "provisioned" (13:45Z) → OD-20260914-BRIDGE-P403-PROVISIONED-1; "smoke GO" (14:03Z) → OD-20260914-BRIDGE-SMOKE-GO-1 (PASS 12/12)
## P012 packet — ANSWERED Q1..Q7 (14:14Z) → OD-20260914-P012-ADMISSION-Q1..Q7 (Q1 = owner himself; self-attestation, not certification)

**Status at 14:15Z: NO owner decision pending.** Next owner-facing items will be: (a) P020 V1.6 round-6 roster outcome and the one-shot result; (b) P031 batch continuation outcome; (c) a scoped work item for the Bridge credential-consuming profile admission (engineering + reviews, not a sentence).

## 2026-09-15 session 4 — answered today
- "no, wait for Grok (Sep 18)" → `OD-20260915-P020-MEASURE-GROK-1`; "A" (P1FIX by the Lead) → `OD-20260915-P012-P1FIX-LEAD-1`; "yes" (P0-27 failure e-mail received); "P028 read go" → `OD-20260915-P028-READ-GO-1`; "A" (P0-26 repair by the Lead) → `OD-20260915-P026-REPAIR-LEAD-1`; two `personal_sign` signatures (Path 1 run r1; P028 eligibility r1).

## ANSWERED 10:50-10:52Z: 1 → "A" (`OD-20260915-P026-ADAPTER-LEAD-1`), 2 → "go" (`OD-20260915-P027-CI-ADDITIONS-GO-1`). Still open: optional "yes/no" on reading the one GitHub failure e-mail for an artifact.

## (was) PENDING at 10:00Z
1. **P0-26 adapter (raised ~09:35Z):** the repaired restore gate refuses the P0-30 closed-partition adapter's isolated restore root (9 of 44 adapter tests, 13 `run_not_complete` refusals). **A** = the Lead extends today's slice by that one file (`p030_closed_partition_backup_adapter.py::_isolated_restore_inputs` copies `COMPLETE.json` + `RUN_MANIFEST.jsonl` into the isolated `runs/<run_id>/`; plus, in its checker `check_p030_closed_partition_backup_adapter.py`, the one mutant test whose expected error text changed — so TWO repo-root files outside the packet's ceiling), re-runs both adapter checks to exit 0, then Gemini delta; same disclosure; new HEAD re-pinned in the Opus lane 4. **B** = park the candidate on its branch until a P0-30 lane (Codex Sep 19) adapts the adapter. Recommended: A (six lines, same author, same roster).
2. **P0-27 CI additions (raised ~09:35Z):** "go" = the Lead opens ONE PR adding to `research-gates.yml` the shared contracts tests, the three P030 checkers and a Ruff step (PR only; the ruleset's required contexts stay the two named today); "later" = leave CI as is; the reconciliation already recommends acceptance of the day-one scope as-is.
Also open on the owner's side (his acts, not decisions): formal acceptance of WP-P0-27 day-one scope; the P0-29 ChatGPT research output; "keys added" (freellmapi).

## 11:45Z — the two 10:00Z one-liners are ANSWERED ("A", "go"); e-mail: "yes but it is in <mailbox masked>" (no connector reaches that account → forward the GitHub "Run failed: CI" mail to the connected address when convenient; optional)
## NEW, not urgent (P0-29 research reconciliation, `P029_RESEARCH_20260915/P029_RESEARCH_RECONCILIATION_20260915.md`)
1. **DD-01:** open `https://app.hyperliquid.xyz/terms` (June 15, 2026 text; Lead capture sha256 `28df55bf…`), read it → "ToS read — HOLD stands" / "ToS read — proceed to the next gate" / "question: …".
2. **DD-05:** fallback candidate for the record → "OKX" / "Binance" / "Bybit" / "none yet" (Lead reading: OKX has trade-only keys + IP allow-list + sub-accounts + demo documented).
Also his acts, no question: formal acceptance of the P0-27 day-one scope; the T1 review/merge word for PR #193 (workflow file).

## 2026-09-15 session 5 (overnight) — PENDING at 14:25Z (sent in chat 13:57Z; defaults apply until answered)
1. **DD-01 Hyperliquid Terms:** "ToS read — HOLD stands" / "ToS read — proceed" / "question: …". Default: HOLD stands.
2. **DD-05 backup venue:** "OKX" / "Binance" / "Bybit" / "none yet". Default: comparison prepared around OKX, not named as chosen. (Fallback deep research delivered ~13:00Z and reconciled by session 4; folded into the addendum §D2 and the P0-28 fallback spec v1 tonight.)
3. **P0-27 day-one CI:** "accept day-one scope" / "not yet". Default: not yet — the acceptance packet is ready (`P027_RECONCILIATION_20260915/P027_ACCEPTANCE_PACKET_20260915.md`; Gemini corroboration recorded).
4. **Builder items tonight:** "build a" (P0-30 O9FIX nits) / "build b" (P0-12 funding intake adapter) / "build c" (`test_opsa.py` into CI, second small PR) / "none". Default: none.
5. **P0-14:** "close as deferred" / "keep open". Default: keep open.
6. **freellmapi keys:** "added" / "not yet". Default: not probed beyond one HTTP call (`401 Invalid API key` = server up, key unknown).
NEW tonight (no rush, one line each):
7. **P0-26 README follow-behind:** `tools/opsa/README.md` lines 61/63 still show `restore.py --latest` (flag removed by candidate `d81b07f6`; README outside the five-file ceiling). "A" = the Lead fixes the two lines + names the completion files in the same branch before the Wednesday Opus lane (disclosed; two-line docs change), "B" = leave it for the merge PR. Default: B (nothing touched).
8. Optional: forward the 08:18 "Run failed: CI" e-mail (demo-run mail) if you want it archived beside the PR #193 one.

## 13:10Z owner: "testnet agent-withdraw test: go" -> `OD-20260915-P029-DD06-TESTNET-PROBE-PREP-1` (PREPARE only). Morning ask: approve the exact execution steps of the DD-06 testnet probe packet ("probe steps approved"), or "changes: ...".

## 18:25Z — morning asks A-G ANSWERED early (`A "probe steps approved"` / `B A` / `C procced` / `D we'd opus` / `E recomended` / `G yes`; F silent → skip). Rows `OD-20260915-P029-DD06-PROBE-STEPS-APPROVED-1`, `-P026-README-A-1`, `-P029-DD01-PROCEED-1`, `-P027-T1-WEDOPUS-1`, `-P021-S2-RECOMMENDED-1`, `-P013-E4-ASK-1`. Item 7 (README) CLOSED by B; item 8 (demo mail) stays optional.
**PENDING now:** "r2 go" for the DD-06 probe re-run on slice 3 `1af85067` (r1 aborted at the control arm on a tick-size rejection; fix shipped and dry-run on KVM2). Nothing else blocks.

## 2026-09-16 08:05 UTC+3 — R2 / H / I / D ANSWERED (`r2 go · H catalogue only · I A A A A A B · D all R`). Rows `OD-20260916-P029-DD06-R2-GO-1`, `-P021-S1-CATALOGUE-ONLY-1`, `-P031-M2-Q1-Q6-1`, `-P012-INTAKE-D1-D6-R-1`. **PENDING now:** F (optional demo mail, default skip). Lead items unlocked: DD-06 r2 execution; P0-31 M2 design half (Q1 A); P0-12 accepting-half slice (D-1..D-6).

## 2026-09-16 11:4x UTC+3 (session 6) — new optional asks after the day blocks (defaults = nothing moves)
- **P0-31 M2 (design half done):** `Q7 A|B|C` (extend table 4a to the live vocabulary), `Q8 A` (identity rule per store), `Q9 A|B|C` (triage decision proxy), `Q10 A|B` (43 advisory orphans), `Q11 A|B` (4b labels' source), `Q12 A` (lower-state order), `Q13 A` (SEED_IMPORT initial event + schema CHECK widening) — `P031_M2_OWNER_QUESTIONS_20260916.md`. Bold recommendations there; the M2 build waits for M1 acceptance (Q6 B) regardless.
- **P0-12 oracle capture (D-4):** `O-1 build|wait`, `O-2 <tolerance>` (rec. 0.05%), `O-3 <window>` when the owner next holds a position — `P012_ORACLE_CAPTURE_DESIGN_NOTE_20260916.md`.
- **DD-06 r3 (optional):** fund the `kvm2-bridge` agent wallet with a few testnet USDC from the faucet (owner's wallet), then `r3 go` for one re-run.
- Still optional: F (demo mail). **Nothing blocks tonight's exact-Opus queue.**
- **DD-06 mainnet probe (owner proposed 12:0x UTC+3 "we can do it in mainnet with real money"):** not authorized yet. Path: `mainnet probe: write the packet` → the Lead writes `DD06_MAINNET_PROBE_STEP_PACKET` (throwaway agent, amounts, stop rules, rollback) + Gemini detection + exact Opus (tonight, optional lane 9) + Sol (Fri) → then the owner's exact word with amounts (e.g. `mainnet probe: approve steps, fund 12 USDC`) and his two wallet actions (approve the throwaway agent with a 1-day expiry; send the USDC). Alternative: `mainnet probe: waive roster` (owner authority; recorded as a waiver) → packet + Gemini only → run the next day. Default: nothing moves. **Owner 12:2x UTC+3: `leave it for now` — parked; no packet, nothing queued.**

## 2026-09-17 09:5x UTC+3 (session 6, Thursday) — state of the asks + two new design one-liners (defaults = nothing moves)
- DD-06 r3: DONE 2026-09-16 (funded, ran, register amended); mainnet probe PARKED ("leave it for now"). F still optional.
- **P0-31 M1 lifecycle semantics (from the exact-Opus reads; not blocking M1 acceptance, but they belong in the acceptance packet):**
  - `N-10 yes|no` — should a registrar refresh (deployment identity A → B) open a NEW evaluation epoch, i.e. require fresh evidence before the first admission under B (today the admission may cite the same `evaluation_run_hash` that justified the revoked composite)? Recommended: **yes** (semantic change → owner's).
  - `N-13 yes|no` — should a refresh permanently retire the previous identity (today "revoked" is reversible: a second refresh B → A is accepted and the candidate re-climbs under A)? Recommended: **yes**, together with N-10 (one small ledger change + two fences, after the third exact-Opus read and Sol).
  - `N-5 A|B` — the "one sentence" rule for owner re-entry reasons: A keep the naive rule (accepts `One; two.`, refuses `v2.0`) / B exactly one terminal `.!?`, decimals allowed, `;` runs refused. Recommended: **B**.
- P0-31 M2: Q7-Q13 still open (see 2026-09-16 block). P0-12 oracle: O-1..O-3 still open.
- **Nothing blocks today's remaining exact-Opus lanes** (P026, P031 third read, P012INTAKE, P021S1, DD06 — after the Pro window reopens 13:00 UTC+3).

## 2026-09-17 09:5x UTC+3 — ANSWERED in one line: `7 A Q8 A Q9 A Q10 A Q11 A Q12 A Q13 A N-10 yes N-13 yes N-5 B O-1 wait O-2 0.05% O-3 now`
- Q7 A ("7 A" read as Q7 A), Q8 A, Q9 A, Q10 A, Q11 A, Q12 A, Q13 A → the M2 mapping/identity/seed rules are RULED as recommended; the M2 build still waits for M1 acceptance (Q6 = B). Row `OD-20260917-P031-M2-Q7-Q13-1`.
- N-10 yes, N-13 yes, N-5 B → M1 semantic changes RULED (refresh opens a new evaluation epoch; refresh retires the previous identity; one-sentence rule B); to be built as one small slice AFTER the third exact-Opus read of `61c56148` and the Sol read, with D026 fences. Row `OD-20260917-P031-M1-N5-N10-N13-1`.
- O-1 wait (no oracle-capture engineering slice now), O-2 0.05 % (bracketing tolerance), O-3 now (capture window: now). Lead reading of the pair: the reviewed tool + adapter fill waits; the READS themselves start now with a minimal scheduled reader (public `metaAndAssetCtxs` + `clearinghouseState` at H−2 s / H+2 s every full hour, raw bytes write-once + sha256, host clock recorded) so the window is not lost; the reads are research evidence and stay usable later (the accepting half names a capture by `<sha256>#<json-pointer>`, it does not open it). At 09:59 UTC+3 the account shows NO open perp position (`clearinghouseState`: accountValue 0.0, assetPositions []), so no funding will accrue until a position is opened — the owner is told. Row `OD-20260917-P012-ORACLE-O1-O3-1`.
- **2026-09-17 14:0x — new one-liner from the third P0-31 read:** `N-16 A|B` — a ledger that used catalog-backed evidence cannot be READ (report/replay/backup) without the exact catalog, and the shipped report command has no way to pass one. A = make committed history readable without the catalog (weaker read-time check) / B = let the report command take the catalog and say in the report whether one was given (keeps the strict check). **Recommended: B.** Default = nothing moves (the feature is opt-in and unused today).
- **2026-09-17 18:2x — new one-liner from the second P0-12 intake read:** `D6-START A|B` — which funding payments belong to a capture window at its START? A payment stamped a few ms after the start hour (e.g. 15:00:00.041Z for a window starting 15:00) settles the PREVIOUS hour. A = keep "by stamp" (it is inside the window) / B = settled-interval rule on both sides, mirroring the end rule you already ruled (exclude it). **Recommended: B.** r1 and r2 are unaffected either way; it matters for the next capture whose start hour carries a payment. Default = nothing moves.
- **2026-09-17 22:1x — from the DD-06 probe read (not urgent; the probe runs again only on your word):** `DD06-ORDER A|B` — the probe's arm order. A = keep the order you approved (withdraw3 first — the only arm that could move funds OFF the venue) / B = run the two in-venue self-transfers first, so a surprise "not refused" trips the stop rule before the withdrawal arm is ever tried. **Recommended: B** (same evidence when everything is refused, strictly safer otherwise). Default = A (your approved order stands).
- **Incident notice (no decision needed):** lane 7's reviewer caused one unintended testnet run at 18:56 (see the chat message and `INCIDENT_20260917_LANE7_DD06/`); the tool is repaired (`a46b2a9d`) and a binding lane rule is in place. Your call, separately: whether to move the agent-wallet key out of `HKCU\Environment` (I do not touch your environment).
