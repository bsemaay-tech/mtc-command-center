# KICKOFF — Author RP7-WPI-RO.sh (the WP-I read-only check block)

Dispatched by the Claude Lead, 2026-08-10. WP-I is owner-authorized (grants #1/#2); this
task is authoring only — no host contact, no execution against any host, no RUNID minting.

**The repository's two-tier counterpart-implementer rule is suspended by owner amendment
A2/A2a. Implement this yourself. Do not sub-delegate to Claude Max or any other agent.**

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — round 1.4, the BINDING spec.
   RP7-WPI-RO.sh implements section 8.2 rows 10–24 (B3s/B1a/B1/B5/B6) plus every binding
   rule paragraph that follows the table (path-object binding, binding ordering,
   walk-atomicity, metadata-readability, probe-output precedence, probe
   execution-environment, structured-input adjudication, line-reader completion,
   interpreter-exec extension, namespace-binding).
2. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — binding pre-read.
3. `WPI_BLOCKS_DRAFT/RP6-P0.sh` — the P0 block: match its structural conventions
   (result-line grammar, rc 0/1/3 contract, helper style, header discipline). Note it may
   receive small F1/F3/F4 repair edits in parallel — treat its CONVENTIONS as the
   reference, do not copy stale claim text.
4. `WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/07_RUNKIT_B/RP0-LIB.sh` — the accepted
   library (18968 B, SHA-256 `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48`).
   RP7 sources it the same way RP6-P0.sh does. Byte-verify before reading conventions.

Do not read handoff files or GATE_A_A* files.

## Contract highlights (the spec is authoritative — these are reminders, not the contract)

- Three-outcome truthfulness everywhere: FAIL only on positively established deviant
  state, STOP on any inability to evaluate, rc 0/1/3. A check that cannot fail proves
  nothing; a STOP never becomes FAIL by inference.
- Row ordering is binding: sweep budget (12) → walk completeness (13) → write bits (14);
  interpreter (18) and metadata preflight before parity (19); shared netns preflight
  (row 22) before ANY curl/ss interpretation (rows 20–23).
- Path-object binding rule: component-wise non-following walk, numeric ownership, mount
  binding per the round-1.4 rule, atomic with the leaf checks.
- Consume preregistered inputs as variables named exactly as section 2 (`WPI_*`); the two
  `<PIN-BEFORE-DISPATCH>` values arrive as environment/prelude constants — the block must
  refuse to run (rc 3, `reason=prereg_input_missing`) if any is unset or malformed.
- Read-only: stat/lstat/find/silent grep/readlink/ss/curl GET/sha256sum only; no file
  content printed (metadata and digests only); no mutation outside the run's own
  create-once evidence tree; children per the probe execution-environment rule.
- Numeric identity only; names diagnostic.

## Deliverables

1. `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — the block.
2. `WPI_BLOCKS_DRAFT/SELF_QA_RP7.md` — per round-1.4 acceptance rules (§4 + C16):
   - exact paste-and-run commands, REAL captured RED/GREEN output, run locally
     (Git Bash/MSYS available; no host contact, no ssh, no network);
   - MUST include the two §4 STOP-first fixtures: (a) missing `systemctl`/denied
     manager → STOP before any comparison; (b) a `find -perm /222` fixture that emits a
     writable pathname then hits a traversal error → `B3_STOP`, never `B3_FAIL`;
   - plus at least one RED per major row group (B3s, B1a, B1, B5, B6) driven against
     deliberate fixture mutations;
   - `bash -n` PASS on the final bytes; record final SHA-256 + byte count.
3. `WPI_BLOCKS_DRAFT/STATUS_RP7.md` — status `AUTHORED-PENDING-AUDIT`, one-line map of
   row → implementing function.

Touch ONLY those three files. Do not commit — the Lead verifies, routes the independent
audit, and commits.

If an environment limit (MSYS/no systemd locally) makes a fixture unrunnable as written,
emulate the interface with a fixture shim (fake `systemctl` on PATH etc. — the round-1.4
probe-environment rule tells you how the block must resist that in production while the QA
may use it deliberately) and record the shim verbatim; never fake output.
