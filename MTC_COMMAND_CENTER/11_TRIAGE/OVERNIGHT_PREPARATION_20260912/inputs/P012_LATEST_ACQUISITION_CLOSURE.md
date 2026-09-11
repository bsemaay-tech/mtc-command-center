# WP-P0-12 evidence-acquisition closure packet

**Verdict: evidence pass complete; full production remains NONACCEPTED.** No original production requirement was retired. The10OPEN items,27signed risks and five residual obligations remain. This pass supplied stronger bounded observations and identified the precise missing source proof; it did not admit new venue facts into production.

Window:2026-09-11T22:07:15Z to a maximum2026-09-12T00:07:15Z. The original sprint deadline remains2026-09-12T08:57:41Z. This pass finished early because the inspected concrete sources reached useful evidence-backed conclusions, not because the campaign was extended or a missing fact was waived. Final timestamp and worker count are in RUN_STATE.json.

## What is now resolved for evidence review

**Funding.** Lead verified the original asset-context archive against the pinned Git blob and SHA256:1,440BTC observations, exactly60seconds apart. The21:00 sample oracle114296 has no block/state/phase binding to the payment at21:00:00.014877297. The replay script consumes recorded funding amounts, uses mark/trade prices for other reconstruction, and sorts events by milliseconds; it does not establish the consumed spot-oracle or consensus ordering. The replay interval does include the21:00 payment—its failure is missing valuation provenance, not exclusion of that timestamp. No one settlement qualified; complete-period reconciliation therefore did not start. This is a bounded negative result, not proof that no suitable artifact exists anywhere. [Funding findings](funding/FUNDING_FINDINGS.md).

**Fees.** Current first-party documentation distinguishes book-market liquidation from backstop position/margin transfer and states no separate clearance fee. This does not prove zero total cost, waive ordinary fees, or establish historical applicability. Lead verified a pinned derived CSV with5,419BTC rows whose fee column is zero. The publisher says its liquidation-specific extractor is not included. Analogous scripts default missing fee keys to zero, but the actual CSV generator has not been inspected; no claim is made that it generated these zeros that way. Original matching fill objects and extraction provenance remain needed. Existing C10/frontend evidence is reused with its account/date/display limits. [Fee mapping and residual questions](fees/FEES_FINDINGS.md).

**Instrument.** Fresh default metadata confirms nativeBTC szDecimals5 and the existing0.00001grid. Published size precision and10-dollar notional rules do not establish whether a separate quantity floor exists. Null still means unavailable in the current consumer. Confirmed absence would need an explicitly approved representation; neither numeric0 nor the precision step can be substituted now. [Instrument mapping](instrument/INSTRUMENT_FINDINGS.md).

No charged-fee rule, independent quantity-floor fact, consumed-oracle binding, canonical event identity or full funding coverage became production-admissible in this pass. Current-document facts and source-content findings are ready for evidence review with their stated limits.

## External dependencies and practical proposals

[Exact UNSENT requests](UNSENT_REQUESTS.md) name the official Hyperliquid #api-traders route and the publisher-listed ConejoCapital maintainer/licensing contacts. They ask for one qualified settlement bundle, applicable fee rules, an explicit quantity-floor rule, and narrow original fill/source excerpts. The owner is not asked to research or invent those facts; the Lead owns interpreting any response.

No paid archive or node proposal is justified yet: required state/order coverage has not been demonstrated. Known public artifacts and licensing limits are listed; any price or coverage not established is marked unknown. Current paid ceiling:$0. Messages remain UNSENT; account/host/node access remains UNEXECUTED. No narrower product scope is recommended or implemented.

## Remaining production sequence

1. Qualify source authenticity, native asset/account/product/time, each required field and complete interval. Resolve the exact requests above; retain refusals for anything unsupported.
2. Prepare a concrete separately authorized production proposal: final source-event identity/digest and coverage contract; D1 production binding validation; complete record mappings; any quantity representation or executable fee-rounding change. Real data does not automatically enable the synthetic-only D1 tool.
3. A separate authorized flagship implements the approved protected changes in exclusive owned paths. Derive new record digests, dependency identities and effective-interval intersection from complete evidence.
4. Execute the required full production path and meaningful negative/coverage/duplicate/refusal controls with independently derived expectations. Use D026 RED/GREEN for actual repairs; reuse unchanged acceptedR34/R35/PR178/D1/D2 evidence.
5. Freeze one final candidate/packet and finish the retained receipt29 semantic redo and record/Section16 reviews. Preserve the reviewer-family restriction: independent of the Codex kernel implementer and Claude contract-table author. ExistingR35 approval is scope-specific and does not preapprove this candidate.
6. Obtain required fresh exact T0 Opus5/Sol xhigh reviews plus mandatory Gemini3.7 corroboration and independent Lead reproduction, preserving stronger retained P012 obligations. Obtain the actual required owner human ratification; model output cannot substitute for it.
7. Publish/integrate only under new concrete authority with current-head required CI and protected merge. PR179/180 release authority was already consumed. No trading/deployment authority is implied.

[Detailed source-checked implementation dependencies](CLOSURE_SPEC.md) identifies the actual current consumer paths and refusal behavior. These are proposed next steps, not newly executed production tests.

## Routing, worker output and preservation

Three initial Go workers performed useful reads/captures, then hit the included monthly limit; all were stopped, with no balance billing enabled. A ZAI Coding Plan continuation returned HTTP429 without useful inference. After owner login, two Grok4.6 subscription sessions performed source reading and drafted reports. Headless terminal/web/write permission prompts cancelled their tool calls; final proposed write contents were recovered from their saved sessions and checked/corrected by Lead. Gemini3.8 via the guarded Google AI Pro route supplied a literal-input instrument draft; its guessed source reads failed and were not treated as proof. Lead used the actual owned source and corrected the draft. These were research/drafting roles, not acceptance-audit substitutions.

Safe Max check during this pass reported session100% used and week97% used, with displayed resets01:49 and07:59 Europe/Chisinau. No Max inference was dispatched while session capacity was exhausted; no work was invented merely to wait for or spend the reset. No purchases, resets, PAYG, global changes or venue-account access by this task.

Merged master remains42f99571e6abb5222744d9345e1c8a9e19c23c15. Local P012 source head remains4d68b50922cb4440dcd023643885aa30b4f2dadd, clean; production records and D1 bytes unchanged. Sealed release artifacts remain unchanged. The existing CONTROL_TABLE.md remains the single requirement/owner/status/completion register and points to this closure.

**NEXT ACTION:** authorize the concrete UNSENT technical/source requests if desired; on receipt the Lead validates actual bytes, identity, applicability and coverage before proposing protected changes.

**WAITING FOR OWNER:** outreach authorization only for the prepared requests; no purchase, node install, production change or scope reduction is being requested. Eventual production implementation/integration and actual human ratification remain later gates. No fact-by-preference decision is needed.
