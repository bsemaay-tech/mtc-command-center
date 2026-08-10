# KICKOFF — RP7-WPI-RO.sh round 5: three Codex T0 findings

You are Claude Opus 5, effort xhigh, **IMPLEMENTER**. Codex is the auditor of record for
these findings and will re-audit your bytes, so separation holds. Round 5 is authorised
under owner grant #7 (T0 round cap lifted for this block set until both flagships accept).
Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit.
Write shell files with **UNIX LF only**. Do not `git checkout` any block file (autocrlf
would rewrite it); if you must restore one, use `git cat-file blob HEAD:<path> > <path>`.

## Inputs (relative to `MTC_COMMAND_CENTER\11_TRIAGE\`)

1. `WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R4_2026-08-10.md` — **BLOCK: 3**. That text BINDS,
   including its executed falsification fixtures. Re-run each one on current bytes to see
   it RED before you repair.
2. `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — round-4 bytes, 70941 B, SHA-256
   `23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad`, commit `d6a976aa`.
3. `WPI_BLOCKS_DRAFT/SELF_QA_RP7.md`, `STATUS_RP7.md`, `RP7_REPAIR_R4_REPORT.md`.
4. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` §4, §8.2 rows 10–24. Edit
   narrowly where a repair requires it and list every draft edit in your report.
5. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — binding.

## The three repairs

- **F1 (BLOCK) — `python3` is never bound in the production main path.** The tenth pin is
  accepted at `:594-614`, included in projection v2 at `:443-456`, and its required
  binding is defined at `:546-562` — but the only production binding loop at `:1134-1137`
  lists nine tools and omits it. The unbound executable then runs at `:907` and `:1074`
  while `:947` and `:1105` print `parser=pinned_system_interpreter isolation=isolated_no_site`.
  Codex demonstrated a deviant executable writing a marker, forging `OK fields=8` over an
  `ARMED` body, and still reaching `RP7 PASS` (rc 0, marker present, `python3_bound=no`).
  **Repair:** bind `python3` in the real `wpi_main` loop **before the initial mount window
  closes**. Keep `-I -S` and the startup guards — they only become load-bearing once the
  executable interpreting them is genuinely bound.
- **F2 (HIGH) — a malformed admitted `*.dist-info` object is silently dropped, so row 19
  can print the accepting parity line for a universe it never adjudicated.** `:797-859`
  proves only object kind, ownership and byte readability; the driver at `:919-940` builds
  a `PathDistribution` for every admitted directory without requiring a valid
  `Name`/`Version` or a unique canonical name; the pinned
  `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:68-74` then skips every object whose
  METADATA lacks `Name` and overwrites duplicate canonical names in a dict.
  **Repair:** semantically adjudicate every admitted object's package identity **before**
  parity. Absent, unparseable or duplicate canonical identity is a **STOP** (inability to
  evaluate), never a silent omission and never a FAIL. Do not modify the byte-frozen
  `verify_lock.py`; put the adjudication in the block.
- **F3 (evidence contract) — `SELF_QA_RP7.md`'s only published "Exact command" contains a
  literal placeholder** (`bash <fence-file>`) and returns rc 2 when run as written.
  **Repair:** publish the real content-anchored extract-and-run command that selects the
  fenced body under a unique heading anchor and stops at its closing fence — **no line
  numbers, no placeholders**. Record the extracted-body digest, the command rc and the
  terminal `QA_PASS` from a fresh Git Bash. Codex's working form is shown in its baseline
  section and is one admissible answer.

**Standing rule this round makes explicit:** evidence a third party cannot re-run verbatim
is not freeze-grade. Every evidence command in `SELF_QA_RP7.md` must be literal, bounded,
and anchored by unique content markers (e.g. `^# RP7_F1_HARNESS_BEGIN$` /
`^# RP7_F1_HARNESS_END$`) whose own invocation text cannot reopen the range. Absolute line
ranges are forbidden — the file grows every round.

## D026 evidence required

For F1 and F2 both: a RED on the current round-4 bytes and a GREEN on your repaired bytes,
using a fixture that exercises **the real caller**, not a redeclared helper loop. Codex
found F1 precisely because the published QA declared its own ten-name loop instead of
instrumenting `wpi_main` (defect pattern 10). For F1 the repaired run must STOP before
either adjudicator runs; for F2 the malformed-identity object must produce a STOP with its
reason, and the valid single-distribution case must still PASS.

## Deliverables

Repaired `RP7-WPI-RO.sh` + updated `SELF_QA_RP7.md` (real RED/GREEN transcripts) +
`STATUS_RP7.md` + narrow draft edits + `RP7_REPAIR_R5_REPORT.md` (finding → disposition →
evidence, draft-edit list, freeze-gate inputs). `bash -n` rc 0; re-derive SHA-256 + byte
count; **zero CR bytes** — count bytes with `tr -cd '\r' < file | wc -c`, never
`grep -c $'\r'`. State the disposition of every finding explicitly, including anything you
do not repair and why. Do not commit; the Lead commits after verifying the hash.
