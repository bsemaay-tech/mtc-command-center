# KICKOFF — RP6-P0 round-9 review: reason grammar, exit-code truthfulness, evidence contract

Fresh `gpt-5.6-sol` session, effort xhigh. Report only; edit nothing except your output
file. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.

`RP6-P0.sh` is a **read-only preflight stage** for a maintenance job. It establishes which
identity the later work will run as and which tools it will use, records what it observes,
and prints one machine-readable line per check. It changes nothing. Your job is to confirm
**each branch reports an honest result**, and specifically that every printed line matches
the grammar the preregistration declares.

**Scope: the reason-token grammar, exit-code truthfulness, and the evidence contract.**
Namespace, privilege and filesystem-escape behaviour are **out of scope for this run** and
are being covered separately — do not construct fixtures for them. Keeping each run narrow
is deliberate: two earlier reviews of this file were terminated by the provider partway
through, and the terminations tracked fixture-heavy bands.

## Subject

`WPI_BLOCKS_DRAFT/RP6-P0.sh` — round-9 bytes, SHA-256
`08e0a93562bb04f4f78bac77d973a26da5b609aa305491d3bfa51743adbcf10c`, 104683 B, commit
`9bc25721`. Re-derive hash, byte count, CR bytes and `bash -n` first.

Predecessors, for before/after work — materialise with `git cat-file blob`, never
`git checkout`:
- round 8 / 9a: `e7ca9ff1e6d44b838b6d8bfddbb24bb68e2642b9f65abfc941f9482e465a0839`, commit `ab53a012`
- round 7: `fa852d7e0a984f977a489bd565834c1ced32eab4fd81221388a25a6bad6483cd`, commit `d9d7420f`

## What rounds 9a and 9b claim

Your round-6 review returned REQUEST_CHANGES ×5. Round 7 closed corrections 1–3; round 8
repaired the fences' arm construction; then executing those repaired fences surfaced a
defect **three reviews had missed**: one reason token, `input_pin_freeze_unfilled`, was
being emitted in two shapes, neither matching the single declared form.

- **Round 9a** made the generic emit site carry the `name=` of the constant it names, via a
  new `P0_FROZEN_CONST_NAME` set for all twelve tools.
- **Round 9b** adjudicated the second site rather than patching it: it was a round-5 relic
  `detail=` value for what is really a **distinct condition**, so it becomes
  `input_pin_omitted`, and `input_pin_freeze_unfilled` now has exactly one shape.
- Round 9b also ran an **emit-site sweep** — every `p0_stop` / `p0_fail` site compared
  against the declared grammar. Its results are in `RP6_REPAIR_R9_REPORT.md`.

## What to review

1. **Verify the sweep rather than trusting it.** Independently enumerate every `p0_stop` and
   `p0_fail` emit site in the block and compare each against the reason grammar declared in
   `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md`. Report any site whose emitted
   fields differ from the declared form — an undeclared field present, a declared field
   absent, or a `detail=` value the draft never names. The sweep missing something is the
   most likely defect in this round.
2. **Judge the round-9b adjudication.** Is `input_pin_omitted` genuinely a distinct condition
   from `input_pin_freeze_unfilled`, or is that a convenient relabelling? Does the draft now
   declare both, with a clear statement of when each fires?
3. **Exit-code truthfulness.** rc 1 means a completed observation established deviant state;
   rc 3 means inability to evaluate. Find any path where a configuration or input deficiency,
   an unparseable producer result, or an internal error can reach rc 1.
4. **Evidence contract.** Every fence must be extractable by unique content anchors, runnable
   verbatim by a third party, bounded, and its own exit status must track what it measures.
   The Lead ran all nine on these bytes at rc 0 — `R9_GRAMMAR` 5/5, plus the eight carried
   fences. **Extend that, do not repeat it:** check whether any carried fence has been
   changed in a way that reduces its discriminating power, and whether `R9_GRAMMAR`'s RED
   arm genuinely fails on a relic-restored mutant.

**A note that is directly relevant.** In the parallel RP7 work last night, a repair round
changed a carried regression fence's assertion so that it accepted any exit status, and
justified the change with a false statement about what the old assertion measured. Treat
every changed assertion here with that in mind.

## Known freeze-gate items — not findings

The `<PIN-AT-FREEZE>` constants, including `P0_FIXED_TRUSTED_PYTHON` and the row-8
attestation literals. §8.2 rows 1–9 are implemented by no block and are a separate owner
decision.

## Patterns

`DESIGN_DEFECT_PATTERNS_2026-08-10.md`, **thirteen** patterns — 11, 12 and 13 were added
last night from that day's evidence.

## Output

Write **only** `WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_R9_2026-08-11.md`: verdict for your band
first (`PASS` / `PASS-WITH-NITS` / `REQUEST_CHANGES` / `BLOCK: <n>`), then the emit-site
table, then findings most severe first with exact command, rc and observed output. State
plainly which bands were out of scope.
