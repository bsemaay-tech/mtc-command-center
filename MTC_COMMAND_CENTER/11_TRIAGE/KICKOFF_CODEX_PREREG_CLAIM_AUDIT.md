# KICKOFF — Codex: claim audit of the successor preregistration and the Audit-2 package

You are Codex, ANALYST. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no
commit, no block-byte edits. Write exactly ONE new file:
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_PACKAGE_CLAIM_AUDIT_2026-08-12.md`.
Never git checkout/reset/stash.

## Why
The same claim-audit method has now been run against the SELF_QA documents and the round
reports, and it found real defects in both:

- `SELF_QA_TRANSPORT.md` claims a cleanup its own transcript shows failed; a count off by one.
- `SELF_QA_PATHSCOPE.md` calls a sixteen-row pattern "the four CRITICAL findings".
- `SELF_QA_RP7.md` cites three stale byte identities its own transcripts contradict.
- The RP6 **r16 report** says evidence placeholders were resolved; three are still unresolved
  (`SELF_QA_RP6.md:15807`, `:18690`, `STATUS_RP6_P0.md:284`).

**The two documents that have never been checked this way are the ones freeze actually depends
on**: `WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md` and the files in
`AUDIT2_READINESS_PACKAGE/`. Both were edited repeatedly today.

## What to check

1. **The preregistration's conservation accounting.** It claims Lane-B 15/15, R2 19/19, combined
   34/34, and that the new §4.4.1 disclosure set is "disjoint from the 34-member universe".
   **Recount every one of those from the actual rows.** A conservation claim that does not
   reconcile is the most serious thing you could find here, because freeze depends on it.
2. **§4.4.1 and §4.4.2 as added today.** Four trusted-base assumptions plus one GLM nit. Does
   each cite a real source that says what the citation claims? Is §4.4.2's subordination of the
   §10.2 acceptance language actually placed before that language?
3. **Owner-decision statements.** The prereg records MC-01/02/03 as RATIFIED, transport F1 as
   accept-with-disclosure, and the interpreter vocabulary as decision C. Do those match
   `OWNER_DECISIONS_2026-08-11.md`, `STATUS_SEC102.md`, and
   `SEC102_ACCEPT_WITH_DISCLOSURE_RECOMMENDATION_2026-08-12.md`? An overstated owner decision is
   a finding of the highest severity — the Lead must never appear to have decided something the
   owner did not.
4. **The Audit-2 package's cross-document arithmetic.** The handoff changelog says 16 closed / 1
   partial / 3 not-yet-available. The acceptance matrix, the D026 map, the freeze-input ledger
   and the packets 9/10/11 scope all quote each other. Do the numbers and statuses agree across
   those five documents?
5. **Anything presented as a measurement that is not one** — the `dynamic_targets=0` pattern.
   Report how many candidate lines you checked.

## Rules
- `file:line` for both sides of every finding. Classify **false** / **unsupported** /
  **scope-wrong**.
- **Distinguish history from staleness.** Several documents deliberately retain superseded values
  labelled or struck through; those are correct and are not findings.
- Do not edit anything. Report; the Lead edits.
- A clean result is useful — say so plainly.
- State coverage honestly; **do not imply coverage you did not achieve.**

Print: documents covered, findings by class, conservation recount results, and the most
consequential finding.
