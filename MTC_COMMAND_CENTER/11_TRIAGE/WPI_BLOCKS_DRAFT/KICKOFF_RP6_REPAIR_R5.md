# KICKOFF — RP6-P0 round 5: three Codex final-audit findings (bounded)

You are GLM-5.2 acting as IMPLEMENTER for this bounded round. Codex is the auditor for
this block — you did not audit it, so implementer/auditor separation holds. Working
directory: C:\LAB\Tradingview_LAB_CLEAN. No host contact, no network. Do not commit.

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/`)

1. `RP6_CODEX_FINAL_AUDIT_2026-08-10.md` — findings F1–F3 with executed falsifications
   and "Required repair" text. That text BINDS.
2. `RP6-P0.sh` — target. Current bytes: SHA-256
   `e93d07adcc9ae03ad15e0b0f10c76be54517251ab461c8fe789d160072d253c6`, 85540 B,
   commit `945e20f5`. Verify before editing.
3. `SELF_QA_RP6.md`, `STATUS_RP6_P0.md` — extend/update.
4. `../DESIGN_DEFECT_PATTERNS_2026-08-10.md` — binding pre-read.

## The three fixes

- **F1 (HIGH)** — the freeze gate's polarity is backwards: supplying the `python3` pin
  engages the `P0_FIXED_TRUSTED_PYTHON` check, omitting it disables it. After parsing
  pins, REQUIRE an explicit `python3` entry bound to `P0_FIXED_TRUSTED_PYTHON` (or
  require the complete frozen RP7 pin set) before any host observation. D026 omission
  evidence: current bytes admit the missing-pin fixture (reproduce
  `PIN_NONE rc=0` and `PIN_NO_PYTHON rc=0`), repaired bytes must emit a named rc-3 STOP
  for both, and the complete pin set must stay GREEN.
- **F2 (MEDIUM)** — `command -v` does not establish command type; a PATH executable
  named `rp0_require_safe_component` satisfies it and then runs. Use a builtin type
  assertion (`declare -F`, or exact `type -t … = function`) for BOTH RP0 symbols before
  calling either. RED fixture: PATH-shadow files of those names must no longer satisfy
  the source precondition (and must not execute); GREEN: genuinely sourced functions
  still pass.
- **F3 (MEDIUM)** — `P0_FORBIDDEN_GIDS` is pathname-expanded before validation at
  `:395` and again at `:842-845`, so cwd contents can rewrite the ledger. Validate the
  COMPLETE raw value against an exact digits-plus-separator grammar BEFORE any
  expansion, then parse with pathname expansion disabled (`set -f` around the split) or
  an array mechanism that cannot glob. D026: drive the `P0_FORBIDDEN_GIDS='*'` fixture
  from a cwd containing entries named `0` and `988` — current bytes accept
  (`count=2`), repaired bytes must STOP on the charset grammar regardless of cwd.

Preserve everything else: rc 0/1/3 contract, STOP-vs-FAIL truthfulness, numeric
identity, read-only scope, all other arms byte-identical where not named above.

## Deliverables

Repaired `RP6-P0.sh` + extended `SELF_QA_RP6.md` (REAL local RED/GREEN for each fix —
the auditor's own three fixtures must flip) + updated `STATUS_RP6_P0.md` +
`RP6_REPAIR_R5_REPORT.md` (finding → disposition → evidence). Write UNIX LF only, never
CRLF. `bash -n` PASS; re-run the mandated harnesses named in `STATUS_RP6_P0.md` and
report their results; record new SHA-256 + byte count. Touch ONLY those four files.

If your environment gates script execution, say so explicitly and mark the affected
evidence PENDING rather than fabricating output — that is the correct behaviour and the
Lead will execute the QA.
