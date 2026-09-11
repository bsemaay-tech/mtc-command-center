# P0-12 Bridge funding-evidence retention — build record (2026-09-11)

Task ID: `WP-P012-FUNDING-RETENTION-20260911`
Decision: `OD-20260911-FUNDING-1` · Task history event: `HIST-2026-0042`
Status: **CANDIDATE, NONACCEPTED.** No acceptance verdict, no merge claim, no runtime activation.

## Source and ownership

| Item | Value |
|---|---|
| Base commit | `d1485eee5b2cc02f85d81610d89b7ec7bbf46a6a` |
| Branch | `feature/p012-funding-evidence-retention` |
| Owned worktree | `C:/tmp/P012_FUNDING_RETENTION_20260911` (created solely for this package) |
| Git owner | Astra Lead, sole. The builder performs no `add`/`commit`/`push`/`checkout`/`reset`/`stash`. |
| Builder | Bounded flagship implementer `claude-opus-5` (included first-party Claude Pro), not an independent acceptance reviewer |
| Approved scope document | `C:/tmp/P012_FUNDING_BUILD_20260911/APPROVED_SCOPE.md` (build output root, outside the repository) |
| Runtime | `C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe` — isolated Python 3.12, repository `requirements.lock` unchanged |
| Results root | `C:/tmp/P012_FUNDING_BUILD_20260911/results` (logs are never published into the repository) |

## Owner approval

The owner's current words are `ı approve`, answering the concrete proposal to build this local
Bridge funding-evidence retention capability. The approval covers the local build, its synthetic
offline tests, the named independent reviews, ordinary forward local commits, and conditional
push/PR/normal merge **only after** the required checks pass. It does not grant acceptance,
deployment, live-data capture, new spend, or any venue-fact conclusion.

## Owned write scope

Implementation, tests and documentation (builder-exclusive):

1. `IBKR_PAPER_BRIDGE/bridge/store/db.py`
2. `IBKR_PAPER_BRIDGE/tests/test_funding_payload_retention.py` (new)
3. `IBKR_PAPER_BRIDGE/tests/test_store.py`
4. `IBKR_PAPER_BRIDGE/tests/test_reconciliation.py`
5. `IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md`

Governance (this package):

6. `DECISIONS.md` — appended `OD-20260911-FUNDING-1`, all prior rows preserved.
7. `MTC_COMMAND_CENTER/02_TASKS/TASK_HISTORY.json` — appended `HIST-2026-0042`, all 41 prior events preserved.
8. `MTC_COMMAND_CENTER/_AI_MEMORY/P012_FUNDING_RETENTION_20260911.md` — this note.

`IBKR_PAPER_BRIDGE/HANDOFF.md` is deliberately **not** touched by the builder; the Lead owns the
stage writeback.

## What the capability is

An additive, explicitly opt-in schema **v10** adds one append-only `funding_event_payloads` table
keyed to the existing immutable `funding_events` ledger. It stores the canonical JSON of the exact
existing `FundingEventRecord.authoritative()` domain — the same eight fields already hashed into
the ledger's `payload_digest` — so that `funding_rate`, `position_szi` and `n_samples` survive a
restart instead of being lost to a digest that cannot be inverted.

Preserved unchanged: the default target stays `SCHEMA_VERSION_BASELINE` (v4); v4–v9 behavior and
topology; no downgrade on reopen; broker normalization; the exchange-`hash` event identity; the
existing digest, economic, order, risk and KILL semantics.

## What it is explicitly not

It retains the **normalized** payload the Bridge already computes, not the original HTTP bytes or
the original decimal strings. It therefore establishes no venue authenticity, no coverage
completeness, no settlement-oracle association and no final 18-field MTC funding mapping. Missing
historical payloads are reported unavailable; nothing is reconstructed, backfilled or re-fetched.

## Dependencies and open items

- Independent missing-case report (separate lane) — verified missing requirements inside the
  approved scope are to be integrated by the builder.
- Required reviews for a persistence/evidence change: fresh exact Opus 5 and Sol xhigh, mandatory
  Gemini 3.7 corroboration, independent Lead reproduction, then protected current-head CI.
- Baseline full-suite evidence is the Lead's parallel responsibility; no failure is attributed as
  pre-existing without that comparison.
- The outstanding Hyperliquid venue questions remain open and are not addressed here.

## Actual status

Implementation and offline synthetic tests written and executed in the isolated Python 3.12
environment; the executed RED/GREEN/mutation and full-suite evidence lives in
`C:/tmp/P012_FUNDING_BUILD_20260911/results/IMPLEMENTATION_REPORT.md`. Acceptance is **NOT
VERIFIED** by this builder.

## Lead checkpoint after implementation — 2026-09-11

The owner approval is active. The additional necessary corrective path is
`IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py`: its unsupported target
10 became supported by this approved package, so the Lead changed only that
literal to11. The same rejection assertions remain; all five parameters passed.
This is the standing Package repair rule, not a new behavior approval.

The primary Opus builder produced scoped code and a1462-pass full-suite result,
then was stopped by the Lead after out-of-scope Claude auto-memory writes.
Its terminal exit is-1, not a successful completed-worker result. Its source
and test artifacts were preserved. The prior memory index content was recovered
from the actual pre-compaction read and the new note quarantined; no raw private
memory contents belong in this repository. Original index line-ending byte
identity had not been separately captured, so restoration is a content claim.

A separate native exact `gpt-5.6-sol` xhigh flagship repaired the independently
reproduced NaN/Infinity/-Infinity generic-error leakage into a stable
`FUNDING_PAYLOAD_MALFORMED` refusal. It added only missing test cases in the
already-owned retention test. Its focused suite passed275 tests, exit0, and it
released both source paths. This repair author is not an accepting reviewer or
an additional subscription CLI lane.

Lead independently ran the final full Bridge suite:1467passed,0failed,0errors,
exit0 on Python3.12, compared with1423passed on the unchanged Bridge baseline.
Lead reproduced the missing-persistence RED, repaired restart GREEN, and an
isolated persistence-suppression mutant that failed the new restart assertion.
A separate executed call-trace probe confirmed the checkpoint rollback test
actually invokes the injected payload-write failure for `0xfund2` exactly once.
All values and databases are synthetic. Local Windows dependency derivation
omits only the unsupported uvloop lock stanza; all other55 pins/hashes and the
repository/Linux CI lock are unchanged.

Final independent fresh Opus5/Sol xhigh reviews and mandatory Gemini3.7
corroboration are still pending at this checkpoint. No technical acceptance,
push, PR, merge, deployment, runtime activation or venue-fact acceptance follows
from these local results. R34/R35 and the entire existing MTC tree are preserved.

NEXT ACTION: freeze the tested candidate, reconcile the required independent
reviews and current-head protected CI, then the already-authorized normal merge.
WAITING FOR OWNER: Nothing for this approved unit.

## Final local T0 reconciliation — supersedes pending-review checkpoint

Source8fe2ede61ca8bf6cd6c564063680542e6101b276: Lead, fresh exact Opus5 xhigh and fresh exact Sol xhigh each personally passed1467full/275focused tests. Both flagships returned PASS. Required Gemini3.7 corroboration completed SUPPLEMENTAL_UNEXECUTED; wrong foreignlinks/timing wording is explicitly qualified. No required finding remains. Public evidence and optional dispositions are under ../04_REPORTS/ai_handoffs/P012_FUNDING_RETENTION_REVIEW_20260911/README.md.

OpusPro ran tests but exhausted its subscription before a verdict. Existing isolated ClaudeMax supplied the fresh completed exactOpus review; an initial launcher binding failure was corrected before that successful session. No failed attempt was counted as accepting. The earlier native repair author was separate from the accepting Sol reviewer. All reviewers and writers have released the source. Final code/test/contract identity remains the accepted candidate; only declared factual closeout and stagehandoff follow. Protected current-head CI and normal PR integration are mandatory and will be recorded separately; local acceptance grants no operational authority.

NEXT ACTION: verify protected integration, then the next separately scoped funding-export proposal and source-evidence incorporation. WAITING FOR OWNER: Nothing for this approved package.
