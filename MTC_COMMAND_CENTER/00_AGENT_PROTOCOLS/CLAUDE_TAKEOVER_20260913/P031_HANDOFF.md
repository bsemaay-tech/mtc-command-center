# P0-31 Claude takeover handoff

Checkpointed 2026-09-13T12:38:55+03:00. P0-31 is parked for ownership transfer. Do not resume
implementation, Git mutation, or provider calls automatically after the current shared P012 window
releases.

## Exact state

- Owned worktree: `C:/tmp/P031_M1_20260913`
- Branch: `feature/p031-m1-20260913-refresh`
- Frozen base/merge-base: `62a42514793f192ca4f706ca99cc2700b16300fe`
- Reviewed HEAD: `c76043b92c70c9f79a6d06630c0896ebe73e68a1`
- Status: clean; staged 0; no P031-scoped process; zero `agy`/Gemini helper processes.
- Current local `origin/master` at last check: `fcac0ac67cf2682693ad28138b1a56e15a0846f2`;
  candidate 19 behind and 3 ahead, within the guard limit of 30.
- Known upstream overlap: only `MTC_COMMAND_CENTER/03_QUANTLENS/HANDOFF.md`; no executable/test
  overlap. Reconcile only under future integration authority.
- Reviewed cumulative diff: `C:/tmp/P031_LEAD_20260912/reviews/P031_M1_C76043B9.diff`,
  362347 bytes, SHA-256
  `93598A24E2ADD222F8073BD04643B55DFB54A929DA3D5C06A215FDFE0F40ECDE`.

Preserve the older foreign/previous checkpoint: `C:/tmp/P031_M1_20260912`, branch
`feature/p031-m1-20260912`, HEAD `5b52d42ac90879437c8dd70659b73127bba084f0`. It still has
two historical R19 dirty paths and must not be reset, cleaned, stashed, committed, or overwritten.

## Owner-authorized scope and boundaries

Source instruction: `C:/tmp/P031_M1_START_20260912/START_PROMPT.md`.

Authorized:

- bounded P0-31 Milestone 1 fixture-only early engineering before accepted P0-13 provenance;
- append-only fixture lifecycle ledger, Registrar research transitions, deterministic replay and
  current view, backup/restore, integrity/checkpoint guards, verified legacy-reader reuse, and a
  small provenance-first read-only report;
- the narrow P0-14 sequencing amendment while P0-14 stays OPEN;
- same-package fixes/tests/evidence, ordinary local forward commits, and required exact reviews;
- task-specific 12–13 September included Claude Pro/Max review routing only, with no PAYG.

Not authorized: real/authoritative producer or consumer integration, fabricated admission receipt,
legacy import/migration, cutover, retirement, de-tracking, deletion, deployment, host/credential
access, TESTNET/mainnet, ARM/orders, trading, paid usage/purchase/reset, push, PR, merge, destructive
Git, acceptance waiver, or new shared lifecycle semantics.

Current shared state: P0-31 replied `HELD` for
`P012-S16-G5-ITEMS14-WINDOW1`. External handoff writes only are allowed until Mentor releases it.
After release remain parked for Claude transfer; do not resume automatically.

## Completed engineering versus acceptance

Completed and Lead-disposed **PASS-WITH-NITS** for the bounded fixture engineering:

- commits `854ffea236c4025bb055095bdd13435b1db7c818`,
  `901f89bcba722220dc0991ce05de43437a54e07b`, and
  `c76043b92c70c9f79a6d06630c0896ebe73e68a1`;
- eight-path cumulative package, including R20 protection against `deepcopy()` stripping fixture
  provenance;
- focused suite 101 tests: 100 pass, one expected Windows symlink skip;
- shared contracts: 50 pass;
- compile, reader self-check, Ruff F 0.16.7, diff-check and repository guard: PASS;
- fresh fixture demo: 3 events/restored, `fixture_only=true`, `accepted=false`,
  `authoritative_records=0`, deterministic report SHA-256
  `85B168B063E4C12C6B90CAF181D7989B5A5A4960D8CBC870A9D62E18164A21C7`;
- R20 exact pre-fix mutation RED (one expected failure) and repaired regression GREEN;
- generic D026 harness: all seven expected guard/mutation observations matched.

Milestone 1/package acceptance remains **NO**. This is a non-authoritative fixture checkpoint, not
an admission ledger release.

## Review and evidence pointers

- Full final Lead handoff:
  `C:/tmp/P031_LEAD_20260912/P031_M1_FINAL_HANDOFF_C76043B9.md`, 8181 bytes, SHA-256
  `9407D2F29AC31F73C80E82E77D19745E7458E475D8AA55D3591DEAD2C0465A3C`.
- R20 scope: `C:/tmp/P031_LEAD_20260912/R20_CORRECTIVE_SCOPE.md`.
- R20 RED evidence:
  `C:/tmp/P031_LEAD_20260912/d026_counterfactuals_r20/RED_EVIDENCE.md` and
  `run_r20_red.py`.
- Exact review packet:
  `C:/tmp/P031_LEAD_20260912/reviews/P031_M1_REVIEW_PACKET_C76043B9.md`.
- Exact Sol `gpt-5.6-sol` `xhigh`: **PASS-WITH-NITS**, no required findings:
  `reviews/P031_M1_SOL_XHIGH_REPORT_C76043B9.md`, SHA-256
  `0874ECA086293B77EB744DDEF6B5864A0DC2D0141E3ADCAF28F159C07F6D1480`.
- Exact included `claude-opus-5` `xhigh`: **PASS-WITH-NITS**, no required executable finding:
  `reviews/P031_M1_CLAUDE_OPUS5_MAX_REPORT_C76043B9.json`, SHA-256
  `7702E1FA9FE419F6A39B14441C90B76B551AEB589AF2CA24A7EA2767F8A8336B`.
- Coordinated Gemini `gemini-3.7-flash-high`: three source-complete
  `SUPPLEMENTAL_UNEXECUTED` slices, each **PASS-WITH-NITS**, no required executable finding.
  Preserve each raw response, footer proof, supervisor verdict-format `FAILED` flag, and the phase-2
  failed canonical-root lookup. Do not call these execution evidence and do not retry.
- Gemini manifest:
  `reviews/p031_c76043b9_gemini_slices/P031_GEMINI_SLICES_MANIFEST.md`, SHA-256
  `A02F74C5D9E8AC4000F735677324003231AB5376FCAFA230D8741A8A5EB3F8E1`.
- Lead Gemini disposition:
  `reviews/P031_M1_GEMINI_ADJUDICATION_C76043B9.md`, SHA-256
  `479CD308ADA2BFC3310CC4BD3F76E9DFDDB173E80206E529BA3ACDD1554FD0E1`.

No tracked or untracked file is mutable/uncommitted in the current P031 worktree. External evidence
under `C:/tmp/P031_LEAD_20260912` and this takeover handoff are not repository commits and must be
preserved. The older worktree's two dirty R19 files are historical evidence, not new work.

## Remaining dependencies and tasks

Full M1 acceptance still requires:

1. exact accepted WP-P0-04 lifecycle/identity/writer provenance;
2. exact accepted WP-P0-13 TrialRecord/catalog provenance actually consumed by P031;
3. owner-ratified active worthiness check-set version;
4. seven fail-closed lifecycle envelopes: DEMOTED target, CHALLENGE incumbent, atomic succession,
   REJECTED purpose/evidence, ambiguous capacity target, deployment refresh, and evaluation-run
   candidate scope;
5. owner decisions for `RETIRED -> RE_ENTRY` and same-epoch reuse of one evaluation run across
   distinct check-set purposes;
6. pre-integration tightening/disposition of provenance-losing delegated Pydantic copy/dump helpers;
7. any authorized current-head refresh plus `03_QUANTLENS/HANDOFF.md` reconciliation, followed by
   the protected acceptance path.

P013 notice `da1fb184c71e1ae65e2e348758af7f1a84a1cfbd` reports an accepted bounded contract
slice, but it grants no caller integration/full-P013 acceptance and is not in this candidate.
Do not infer dependency satisfaction. P0-14 remains OPEN. M2 seed/import and M3 consumer
cutover/retirement remain unstarted and unauthorized.

## Subscription and exact-role requirements

The current frozen candidate already has the required exact Sol, Opus and Gemini reviews above.
If Claude changes any reviewed executable/test/package content, freeze a new exact candidate and
repeat the binding T0 roster: independent `gpt-5.6-sol` `xhigh`, exact `claude-opus-5` `xhigh`, and
coordinated `gemini-3.7-flash-high` supplemental corroboration after both flagships accept. Lead and
implementer remain separate. Use included subscription routes only; verify capacity and process
isolation; no PAYG, substitute model, or reviewer recursion. Every Gemini call requires current
Mentor HOLD/START/END coordination.

## NEXT ACTION

Remain parked. Claude should first verify this handoff, exact Git state and current Mentor release.
Only with fresh authority/dependency evidence should it choose between preserving `c76043b9` or
creating a new owned refresh for the unresolved acceptance/integration work.

## STOP CONDITION

Stop on any missing authority, active shared HOLD, changed candidate identity, upstream overlap not
owned by P031, absent accepted provenance, model/subscription mismatch, paid-route requirement,
host/credential/deploy/trading request, or push/PR/merge need.
