# KICKOFF — Codex T2: the freeze-input ledger (Audit-2 packet 8 + freeze blockers 7/8/9)

You are Codex `gpt-5.6-sol` xhigh, ANALYST. Working dir `C:\LAB\Tradingview_LAB_CLEAN`.
No host, no network, no commit, **no block-byte edits**. Write exactly ONE new file:
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md`.
Do not touch `RP6-P0.sh`, `RP7-WPI-RO.sh`, the transport set, `composite_pathproof.py`,
`pathscope_prover.py`, prereg drafts, or any STATUS/SELF_QA file. Never git checkout/reset/stash.

## Why this exists
Three current freeze blockers are all the same missing artifact seen from different angles
(`WPI_FREEZE_BLOCKER_MAP_2026-08-12.md`):

- **Item 7** — `run_p0.sh` wires none of the five `P0_ATTESTED_*` inputs.
- **Item 8** — the close-script's preregistered contract and its actual bytes disagree.
- **Item 9** — `REMOTE_BASE` must be allocated *before* the RO block is frozen.

and Audit-2 missing-material packet 8 asks for the same thing: **one ledger that reconciles every
duplicate consumer of every freeze-time input.** This is analysis over bytes that already exist,
so it can be produced now, before tonight's second-flagship audits.

## What to produce — one row per FREEZE INPUT, not per file
For each input: its exact name, what produces it, **every** consumer (file + line), the exact
form each consumer expects, whether the consumers agree, and what STOPs if it is unfilled.

Cover at minimum, reading the real bytes:

1. **RP6's six embedded pins** — and whether RP6 has any end-to-end PASS while they are literals.
2. **RP7's pins** — projection digest, trusted-Python, evidence-root; the three values it
   requires and its recorded accepting-input arm.
3. **Both tool maps** — RP6's twelve-entry `P0_TOOL_PINS` and RP7's shared pins; prove they agree
   entry-for-entry or name the divergence. (The twelve exact pins with no PATH fallback are
   owner-RATIFIED as of 2026-08-12 — FAM-01.)
4. **The five `P0_ATTESTED_*` values** and their wrapper copies — this is blocker item 7. State
   exactly which consumer reads each, and what `run_p0.sh` currently does instead.
5. **Transport inputs** — mount identity, OpenSSH configuration and credential digests.
6. **Close-script identity** — this is blocker item 8. Compare the preregistered contract
   (prereg §4.7, plan rows 07/08, the derivation contract, the launch-domain claim, the
   scratch-location semantics) against `remote_close_tree_wpi.sh`'s actual bytes and state the
   disagreement precisely: argv shape, `WORK_ROOT`, the two-argument inherited-TMPDIR question,
   and whether the script reaches its RUNID/`EV_DIR` validation or fails earlier on argv shape.
7. **Archive / member digests, block and wrapper hashes.**
8. **Allocation values** — `REMOTE_BASE`, both RUNIDs and every derived name; this is blocker
   item 9. State the ordering constraint as a dependency chain: what must be allocated before
   what is frozen, and which current text (if any) violates it.
9. **Evidence-root provenance** — the FAM-03 frozen-composite derivation, owner-RATIFIED
   2026-08-12.
10. **The `P0_VENV_ROOT` exact-equality requirement** — FAM-02, owner-RATIFIED 2026-08-12.

## Rules
- **Read the bytes; do not trust the narrative.** Where a STATUS file and the code disagree, the
  code wins and you say so.
- Every claim carries a `file:line`.
- Mark each input `FILLED` / `LITERAL-MARKER` / `MISSING-CONSUMER` / `CONTRADICTED`.
- For anything you cannot determine from local bytes (host-side values), say
  `REQUIRES-HOST — not determinable locally` rather than guessing.
- Do not propose block edits. This is a ledger, not a repair. Where a repair is implied, state
  it as a one-line requirement the Lead can turn into a scoped kickoff later.

## Deliverable shape
Preamble stating scope and method; the per-input ledger table; then three focused sections that
answer blockers 7, 8 and 9 directly and completely; then a summary count of
FILLED / LITERAL-MARKER / MISSING-CONSUMER / CONTRADICTED / REQUIRES-HOST, and a plain statement
of which of the three blockers this ledger makes *actionable* (none of them CLOSE on a document —
they close when the wiring changes and is re-audited).

Print the summary counts when done.
