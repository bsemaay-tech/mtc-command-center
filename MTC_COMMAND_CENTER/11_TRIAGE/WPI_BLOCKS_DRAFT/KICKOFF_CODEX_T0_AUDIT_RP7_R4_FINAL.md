# KICKOFF — Codex flagship T0 slot: RP7-WPI-RO.sh ROUND-4 bytes (read-only review, xhigh)

You are the Codex flagship slot of the two-flagship T0 review contract: fresh session,
`gpt-5.6-sol`, effort xhigh. Report only — do not edit any file except your own output.

Context in plain operational terms: `RP7-WPI-RO.sh` is a **read-only environment
preflight block**. It inspects an already-provisioned maintenance host, records what it
observes, and prints one machine-readable line per checked row. It changes nothing on the
host. Your job is to confirm that **every branch reports honestly** — that a row can only
print an accepting result when the underlying observation actually established it, that an
inability to observe is reported as STOP rather than as a completed negative observation,
and that the printed claims are no stronger than what the code establishes.

**Owner amendment A2/A2a in force: do the review yourself, no sub-delegation.**

## Inputs (relative to `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\`)

1. `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — **round-4 bytes**, SHA-256
   `23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad`, 70941 B,
   commit `d6a976aa`. Re-derive the hash and byte count yourself before reviewing.
2. `WPI_BLOCKS_DRAFT/RP7_REPAIR_R4_REPORT.md` — what round 4 changed and why.
3. `WPI_BLOCKS_DRAFT/SELF_QA_RP7.md` — the QA fence (Git Bash / GNU coreutils
   environment; narrow fixture substitutions are tabulated there).
4. `WPI_BLOCKS_DRAFT/STATUS_RP7.md` — current state.
5. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — §8.2 rows 10–24, all binding
   rule paragraphs, and the projection-v2 definition. The block must conform to this.
6. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — the ten recurring defect patterns. Check the
   bytes against all ten.
7. Prior review trail for context only, not exhaustive:
   `RP7_CODEX_T0_AUDIT_2026-08-10.md` (your slot's round-3 review, 5 findings),
   `RP7_CLAUDEPRO_AUDIT_2026-08-10.md`, `RP7_CLAUDEPRO_REAUDIT_R2_2026-08-10.md`.

## What round 4 claims to have fixed — verify each on the real bytes

- Both accepting adjudicators now run under a **pinned system interpreter with `-I -S`**
  that refuses to emit a result unless the isolation it requests is actually reported by
  the child. Previously the interpreter under review produced its own verdict, and
  `python -I` alone does not disable `site`, so start-up code inside the reviewed tree
  could run before the check. Confirm the new path genuinely closes that, and that the
  printed claim about isolation matches what is established rather than what is requested.
- `python3` is now the 10th bound tool and the 21st projection point.
- Row 22 is two-phase: parse to EOF first, then adjudicate.
- One enforced metadata-discovery universe.
- Preregistered B5/B6 ordering is verified against the frozen code at runtime.

## Review contract

- Row-by-row conformance for rows 10–24 at the exact FAIL/STOP grammar; ordering rules;
  path-object binding including projection v2 — probe it hard: subtree blindness,
  tie-breaks, record grammar, escaped-character handling.
- STOP-vs-FAIL truthfulness on **every** branch. An inability to evaluate is a STOP and
  never a FAIL. A check that cannot fail proves nothing — say so where you find one.
- Producer status **and shape** must both be adjudicated before any object verdict:
  an rc-0 producer emitting empty / multi-line / non-printable / unparseable output is a
  STOP, not a usable value.
- Printed claims must be narrow: if the code cannot distinguish two causes, it must not
  label the result as one of them.
- Evidence commands in the QA fence must be literal, anchored and re-runnable by a third
  party. Absolute line ranges are not freeze-grade because the file grows between rounds.
- Re-run the QA fence yourself from the published bytes; `bash -n`; execute your own
  falsification fixtures where practical. **A finding with an executed falsification
  outranks a code-read claim.**

## Known freeze-gate items — NOT findings

`WPI_FIXED_TRUSTED_PYTHON` and the attestation digest are still `<PIN-AT-FREEZE>`; the
accepting `wpi_validate_inputs` arm is filled at freeze. Do not report these as defects.

## Output

Write **only** `WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R4_2026-08-10.md`:
verdict first (`PASS` / `PASS-WITH-NITS` / `REQUEST_CHANGES` / `BLOCK: <n>`), then the
V-row table with evidence, then findings most severe first, each with the exact command
you ran, its rc, and the observed output. Touch no other file. Do not commit.
