# KICKOFF — RP7 round-5 review, PART B of two: rows 20–24 and the QA evidence contract

Fresh `gpt-5.6-sol` session, effort xhigh. Report only; edit nothing except your output
file. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.

`RP7-WPI-RO.sh` is a read-only environment preflight block for a maintenance job: it looks
at an already-provisioned host, records what it finds, and prints one machine-readable line
per checked row. It changes nothing. Confirm **each branch reports an honest result** — an
accepting line only when the observation established it, an inability to observe reported
as STOP rather than as a completed negative observation, and no printed wording stronger
than the code supports.

**Scope discipline: rows 20–24 and the evidence/QA contract only.** The five round-5
repairs and rows 10–19 are Part A, a separate run. Stay inside your band.

## Subject

`WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — round-5 bytes, SHA-256
`393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee`, 77179 B, commit
`1143a9ff`. Re-derive hash, byte count, CR bytes and `bash -n` first.

## Band 1 — rows 20–24

Conformance at the exact FAIL/STOP wording in
`WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` §8.2, plus the ordering rules.
Specifically:

- The two accepting adjudicators run under a pinned interpreter with `-I -S` that refuses to
  emit a result unless the isolation it asked for is reported back by the child. Is the
  printed wording about isolation limited to *requested flags plus child-reported state*, or
  does it assert more than that?
- Row 22 is two-phase: parse to end of input first, then adjudicate. Confirm a malformed
  record anywhere in the table cannot be adjudicated before the parse completes.
- The declared B5/B6 ordering is checked against the frozen code at run time. Confirm the
  check is real and that a table with one malformed row STOPs rather than reporting.
- Row 24 is operator-side and is not evaluated by this block — confirm it is not silently
  claimed.
- Structured status parsing: strict field requirements, and any grammar deviation STOPs.

## Band 2 — the evidence contract

Round 5 replaced a placeholder QA command with a content-anchored extract-and-run command.

- **Run the published command exactly as written**, from a clean Git Bash, and record its
  rc. If a third party cannot re-run it verbatim, that is a finding regardless of what the
  fence body does when extracted by hand.
- Confirm no evidence command anywhere in `SELF_QA_RP7.md` uses absolute line ranges. The
  file grows every round, so a line range silently drifts into unrelated prose — this has
  already produced false regressions elsewhere in this block set.
- Confirm each published anchor's own invocation text cannot re-open its range.
- Confirm the recorded rc, summary and stderr match what you observe when you re-run them,
  and that every command terminates inside its documented bound.

## Method

Prefer executed tests over code reading — a test with recorded output outranks an argument.
Keep each test self-contained under a `mktemp -d` tree you remove. Record the exact command,
its rc, and observed output for everything you claim.

## Known freeze-gate items — not findings

`WPI_FIXED_TRUSTED_PYTHON`, `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`,
`WPI_FIXED_EVIDENCE_ROOT` and the accepting `wpi_validate_inputs` branch are
`<PIN-AT-FREEZE>`, so no whole-block accepting run can exist before freeze. §8.2 rows 1–9
are implemented by no block and are being decided separately.

## Output

Write **only** `WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R5_PART_B_2026-08-10.md`: verdict for
your band first (`PASS` / `PASS-WITH-NITS` / `REQUEST_CHANGES` / `BLOCK: <n>`), then a row
table with evidence, then findings most severe first with command, rc and output. State
plainly that the five round-5 repairs and rows 10–19 were out of scope for this run.
