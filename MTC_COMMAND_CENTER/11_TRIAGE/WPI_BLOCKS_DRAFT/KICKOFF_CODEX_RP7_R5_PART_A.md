# KICKOFF — RP7 round-5 review, PART A of two: the five repairs and rows 10–19

Fresh `gpt-5.6-sol` session, effort xhigh. Report only; edit nothing except your output
file. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.

`RP7-WPI-RO.sh` is a read-only environment preflight block for a maintenance job. It looks
at an already-provisioned host, records what it finds, and prints one machine-readable line
per checked row. It changes nothing. Your job is to confirm **each branch reports an honest
result**: an accepting line only when the observation really established it, an inability to
observe reported as STOP rather than as a completed negative observation, and no printed
wording stronger than what the code supports.

**Scope discipline: this run covers only the five round-5 repairs and rows 10–19.** Rows
20–24 and the QA evidence contract are Part B, a separate run. Stay inside your band —
keeping each run narrow is deliberate.

## Subject

`WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — round-5 bytes, SHA-256
`393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee`, 77179 B, commit
`1143a9ff`. Re-derive hash, byte count, CR-byte count and `bash -n` first.

Round-4 predecessor for before/after comparison: 70941 B,
`23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad`, commit `d6a976aa`.
Retrieve it with `git cat-file blob d6a976aa:<path> > <tmp>` — never `git checkout`, which
would rewrite line endings.

## The five repair claims to confirm

1. **`python3` is now bound in the production `wpi_main` loop** before the initial mount
   window closes. Previously the tenth pin was validated and projected but never bound, so
   the program producing both accepting adjudicator lines was unverified. Confirm the
   binding is in the real main path, not only in a helper or a test loop.
2. **Package identity is adjudicated before parity.** Every admitted `*.dist-info` object
   must have its package identity established first; absent, unparseable or duplicate
   canonical identity is a STOP. Confirm no object can be silently dropped from the parity
   universe, and that a clean single-distribution case still reports normally.
3. **`/dev/null` writes are gone** (`builtin type -t` plus `2>&-`), with `noclobber`
   semantics unchanged where they were relied on.
4. **`WPI_FIXED_EVIDENCE_ROOT` binds `EV_DIR`**, stopping before any leaf is allocated
   unless `EV_DIR` is a strict descendant. Confirm the STOP wording and the unfilled-pin
   branch are honest, and that a prefix-lookalike directory is refused.
5. **The claimed delta is +93/-7 lines and nothing but these repairs.** Verify that against
   the round-4 blob. Any unexplained production change is worth reporting.

## Rows 10–19

Row-by-row conformance at the exact FAIL/STOP wording in
`WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` §8.2. For each row: can it print its
accepting line without the observation that would justify it, and can an unreadable or
malformed input reach a FAIL where a STOP is correct? A check that cannot fail proves
nothing — say where you find one. Producer status **and** output shape must both be
adjudicated before any object verdict: an rc-0 producer emitting empty, multi-line or
non-printable output is a STOP, not a usable value.

Also confirm nothing the round-3 and round-4 reviews closed has reopened.

## Method

Prefer executed counter-example tests over code reading — a test with recorded output
outranks an argument. Keep each test self-contained under a `mktemp -d` tree you remove.
Record the exact command, its rc, and the observed output for everything you claim.

## Known freeze-gate items — not findings

`WPI_FIXED_TRUSTED_PYTHON`, `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`,
`WPI_FIXED_EVIDENCE_ROOT` and the accepting `wpi_validate_inputs` branch are
`<PIN-AT-FREEZE>`, so no whole-block accepting run can exist before freeze. §8.2 rows 1–9
are known to be implemented by no block and are being decided separately.

## Context (read, but not exhaustive)

`RP7_REPAIR_R5_REPORT.md`, `RP7_CODEX_T0_AUDIT_R4_2026-08-10.md`,
`RP7_R5_SALVAGE_FROM_INTERRUPTED_AUDIT_2026-08-10.md` — the last of these carries one
recovered, executed capture-leaf test from an earlier interrupted run; confirm or dismiss it
if it falls inside your band.

## Output

Write **only** `WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R5_PART_A_2026-08-10.md`: verdict for
your band first (`PASS` / `PASS-WITH-NITS` / `REQUEST_CHANGES` / `BLOCK: <n>`), then a row
table with evidence, then findings most severe first with command, rc and output. State
plainly that rows 20–24 and the QA evidence contract were out of scope for this run.
