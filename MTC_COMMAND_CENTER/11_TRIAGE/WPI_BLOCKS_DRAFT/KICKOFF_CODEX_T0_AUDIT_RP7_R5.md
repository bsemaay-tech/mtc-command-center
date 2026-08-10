# KICKOFF — Codex flagship T0 slot: RP7-WPI-RO.sh ROUND-5 bytes (read-only review, xhigh)

You are the Codex flagship slot of the two-flagship T0 review contract: fresh session,
`gpt-5.6-sol`, effort xhigh. Report only — edit nothing except your own output file.
Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.

`RP7-WPI-RO.sh` is a **read-only environment preflight block**: it inspects an
already-provisioned maintenance host, records what it observes, and prints one
machine-readable line per checked row. It changes nothing on the host. Your job is to
confirm every branch reports honestly — an accepting line only when the observation
actually established it, an inability to observe reported as STOP rather than as a
completed negative observation, and no printed claim stronger than what the code proves.

**Owner amendment A2/A2a in force: do the review yourself, no sub-delegation.**

## Subject

`WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — **round-5 bytes**, SHA-256
`393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee`, 77179 B, commit
`1143a9ff`. Re-derive hash, byte count, CR-byte count and `bash -n` yourself first.

Round-4 input for the RED side of any falsification: 70941 B,
`23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad`, commit `d6a976aa`
(retrieve with `git cat-file blob d6a976aa:<path>` — never `git checkout`, autocrlf would
rewrite it).

## What round 5 claims to close — verify each on the real bytes

Your own round-4 review returned `BLOCK: 3`. Round 5 also took two items from the §10.1
reconciliation. The claimed dispositions:

1. **F1 (was BLOCK)** — `python3` is now bound in the production `wpi_main` loop before the
   initial mount window closes. Your fixture must now STOP at the binding instead of
   reaching `RP7 PASS` with an unbound deviant executable.
2. **F2 (was HIGH)** — every admitted `*.dist-info` object's package identity is
   adjudicated before parity; absent, unparseable or duplicate canonical identity is a
   STOP, not a silent omission and not a FAIL.
3. **F3 (evidence contract)** — `SELF_QA_RP7.md` now publishes a content-anchored
   extract-and-run command with no placeholder and no line ranges. **Run the published
   command exactly as written**, from a clean Git Bash, and record its rc. If it is not
   literally re-runnable by a third party, that is a finding regardless of what the fence
   body does when extracted by hand.
4. **F4** — the three `/dev/null` write opens are gone (`builtin type -t` plus `2>&-`),
   with `noclobber` semantics intact.
5. **F5** — a frozen `WPI_FIXED_EVIDENCE_ROOT` now binds `EV_DIR`, which STOPs before any
   leaf allocation unless `EV_DIR` is a strict descendant. Note the implementer's own
   flag: this constant's value is `<REMOTE_BASE>/evidence` and `REMOTE_BASE` is
   allocate-at-dispatch, so it is a freeze-gate input with an ordering consequence.
   Assess whether the STOP grammar and the unfilled-pin arm are honest; the ordering
   question itself is a Stage-1 matter, not a defect in these bytes.

## Review contract

- Row-by-row conformance for rows 10–24 at the exact FAIL/STOP grammar; ordering rules;
  path-object binding including projection v2 (subtree blindness, tie-breaks, record
  grammar, escaped characters).
- STOP-vs-FAIL truthfulness on **every** branch. Inability to evaluate is STOP, never FAIL.
  A check that cannot fail proves nothing — say where you find one.
- Producer status **and shape** adjudicated before any object verdict.
- **No-weakening check:** every arm your round-3 and round-4 reviews closed must still hold
  on these bytes. A repair that reopens an earlier finding is a new BLOCK.
- **The delta is +93/-7 lines and is claimed to contain nothing but the five repairs.**
  Verify that claim against the round-4 blob; an unexplained production change is a finding.
- Re-run the published QA yourself; execute your own falsification fixtures. A finding with
  an executed falsification outranks a code-read claim.
- Check against all ten patterns in `DESIGN_DEFECT_PATTERNS_2026-08-10.md`, with particular
  attention to *the declared instrument is not the executed instrument* — the class that
  produced F1 — and to evidence that tests a helper rather than its real caller.

## Context you may read but must not treat as exhaustive

`RP7_REPAIR_R5_REPORT.md`, `RP7_CODEX_T0_AUDIT_R4_2026-08-10.md`,
`RP7_LEAD_VERIFICATION_R4_2026-08-10.md`,
`WPI_PREREG_DRAFT_ROUND1/SEC101_RECONCILIATION_CODEX_2026-08-10.md`.

## Known freeze-gate items — NOT findings

`WPI_FIXED_TRUSTED_PYTHON`, `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256`,
`WPI_FIXED_EVIDENCE_ROOT` and the accepting `wpi_validate_inputs` arm are `<PIN-AT-FREEZE>`.
§8.2 rows 1–9 are known to be unimplemented by any block and are being decided separately —
do not re-report that here.

## Output

Write **only** `WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R5_2026-08-10.md`: verdict first
(`PASS` / `PASS-WITH-NITS` / `REQUEST_CHANGES` / `BLOCK: <n>`), then the V-row table with
evidence, then findings most severe first, each with the exact command run, its rc, and the
observed output. Touch no other file.
