# KICKOFF — Author the WP-I transport set (ROUND 2 — contract amended after your STOP)

Dispatched by the Claude Lead, 2026-08-10. Authoring only — no host contact, no RUNID
minting (placeholders stay `<ALLOCATE-AT-DISPATCH>`), no execution against any host.

**ROUND 2 NOTE.** Your STOP was correct and is recorded in the draft (round 1.5,
section 0 note + amended section 4). Both contradictions are resolved by amendment:
`remote_setup_wpi.sh` and `remote_extract_verify_wpi.sh` are now WP-I-specific minimal
derivations of the accepted bytes (prefix constant / archive-constants block are the
ONLY semantic changes; prove minimality by recorded diff in self-QA); only
`remote_close_tree.sh` stays byte-identical. Re-read the amended section 4 before
starting. Two extra deliverables are added to your write whitelist below.

**The repository's two-tier counterpart-implementer rule is suspended by owner amendment
A2/A2a. Implement this yourself. Do not sub-delegate to Claude Max or any other agent.**

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — round 1.4, BINDING spec.
   Sections 1 (identifiers/evidence tree), 4 (support scripts + wrapper repairs), 5
   (op list + first-FAIL + runner evidence rules), 7 (close/bind), and every
   cross-cutting rule (probe execution-environment, structured-input, line-reader
   completion — the runner and wrappers are named consumers of the line-reader rule).
2. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — binding pre-read.
3. `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` + `WPI_BLOCKS_DRAFT/RP6-P0.sh` — the two blocks the
   wrappers drive (result grammar, rc contract, prelude-constant expectations).
4. Stage-2-accepted transport artifacts for convention reference (byte-identical reuse,
   do NOT edit): `WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/` and
   `09_TRANSPORT_B3B/` — the accepted `transport_runner.ps1` variants
   (18095/`c5bdb47c…`, 17849/`a48ddc93…`), `remote_setup.sh` (4976/`faee3725…`),
   `remote_extract_verify.sh` (8270/`ba0bef0e…`), `remote_close_tree.sh`
   (7470/`87157f0e…`). Byte-verify digests before trusting a copy.

Do not read handoff files or GATE_A_A* files.

## Contract highlights (spec is authoritative)

- Both wrappers inherit the two accepted Stage-2 repairs: refuse symlink block paths
  (`-f` dereferences — not a refusal on its own), and every child reads from
  `/dev/null` (wrapper arrives on ssh stdin; a child reading stdin would eat the rest
  of the script).
- Wrappers demonstrate the STOP-first contract per §4 acceptance rules before freeze.
- `TRANSPORT_PLAN.tsv`: the ordered op list of §5 with `<ALLOCATE-AT-DISPATCH>`
  placeholders intact; the runner pins the TSV internally (hash placeholder marked
  `<PIN-AT-FREEZE>`); the WP-I op list differs from Stage 2's, so the runner is
  re-pinned, not assumed.
- Runner: operator-side recorder per §5 — first-FAIL ordering, per-op
  stdout/stderr/rc/elapsed capture, evidence records, remote-vs-local binding ops
  local-only; line-reader completion rule applies to its TSV reader (clean EOF vs
  unterminated final record vs read error — falsify all three in QA).
- Row 24 (external TCP probe) is operator-side op 06 — the runner implements the
  bounded probe with the round-1.4 classified-outcome grammar
  (`connection_refused`/`timeout`/`connected`/not-evaluable).

## Deliverables (all in `WPI_BLOCKS_DRAFT/`)

1. `run_p0.sh`, `run_ro.sh` — the two ssh-stdin wrappers.
2. `transport_runner.ps1` — WP-I op list, Windows PowerShell 5.1-compatible.
3. `TRANSPORT_PLAN.tsv` — ordered op list, placeholders intact.
3b. `remote_setup_wpi.sh` — minimal derivation of the accepted `remote_setup.sh`
   (02_PREREG copy, byte-verify `faee3725…` first): ONLY the base-prefix constant
   changes `wpl_p2_staging_` → `wpi_staging_`. Record the full diff in self-QA.
3c. `remote_extract_verify_wpi.sh` — minimal derivation of the accepted
   `remote_extract_verify.sh` (byte-verify `ba0bef0e…` first): ONLY the pinned
   archive-constants block changes (expected bytes + member list + per-member digests
   become the WP-I kit: RP0-LIB.sh, RP0-BOOTSTRAP.sh, RP6-P0.sh, RP7-WPI-RO.sh,
   run_p0.sh, run_ro.sh — RP1-B3.sh excluded; concrete digests/bytes stay
   `<PIN-AT-FREEZE>` placeholders in a clearly marked constants block that Stage 1
   freeze fills). Member-count and ordering logic must match the new member set.
   Record the full diff in self-QA.
4. `SELF_QA_TRANSPORT.md` — per round-1.4 acceptance rules: exact paste-and-run
   commands, REAL RED/GREEN output, run locally (no host contact, no ssh, no network;
   loopback-free). Must include: wrapper symlink-refusal RED/GREEN, stdin-consumption
   guard demonstration, runner TSV line-reader falsifications (all three cases),
   first-FAIL ordering demonstration against a fixture op list, external-probe outcome
   classification against local fixtures (e.g. a closed local port for refused —
   127.0.0.1 loopback is acceptable ONLY for this probe-classification fixture).
   `bash -n` / PSScriptAnalyzer-or-parse check PASS; record SHA-256 + bytes per file.
5. `STATUS_TRANSPORT.md` — `AUTHORED-PENDING-AUDIT`, one-line op → implementation map.
   Self-QA additionally covers 3b/3c: derivation-diff minimality proof + RED/GREEN for
   the changed constants (setup accepts `wpi_staging_<safe>` and refuses
   `wpl_p2_staging_<safe>`, `..`, nested, empty; extractor refuses a nine-member
   fixture archive containing RP1-B3.sh and accepts a placeholder-complete WP-I member
   list fixture — placeholder digests may be fixture values in QA only).

Touch ONLY those eight files. Do not commit — the Lead verifies, routes the independent
audit, and commits.
