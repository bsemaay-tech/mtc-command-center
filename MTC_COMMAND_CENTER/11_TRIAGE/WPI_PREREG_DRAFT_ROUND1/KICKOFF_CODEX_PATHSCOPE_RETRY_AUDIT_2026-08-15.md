# Pathscope final-override execution audit — owner-authorized transport RETRY — 2026-08-15

**DISPATCH READY.** This is a **retry of the same audit**, not a new cycle and not
a new repair. The subject bytes are unchanged.

## Owner authority

Barış authorized on 2026-08-15, verbatim intent:

> One fresh Pathscope `gpt-5.6-sol` `high` execution-audit retry, because the
> previous audit was transport-blocked before execution. If it finds required
> changes, stop before opening another repair cycle.

This authorizes exactly one fresh execution audit of the already-frozen
candidate. It waives no finding and no acceptance standard, and it authorizes no
repair round. A `REQUEST_CHANGES` or `BLOCK` verdict returns the lane to the
owner boundary immediately.

Prior transport-blocked attempt:
`PATHSCOPE_FINAL_OVERRIDE_CODEX_T1_AUDIT_2026-08-14.md` (verdict `BLOCK`, no
execution performed, enforced `sandbox: read-only`).

## Auditor and transport

- Exact model `gpt-5.6-sol`, effort `high`, T1. Fresh ephemeral session.
- No resume, no continue, no implementer-session context, no sub-delegation.
- **Transport requirement:** the run is launched with
  `--dangerously-bypass-approvals-and-sandbox`. Your session header **must** read
  `sandbox: danger-full-access`. **Before doing any audit work, print the session
  header and confirm it.** If it reads `read-only`, or if any Git/Python/hash
  command is refused by policy, **stop immediately, perform no analysis, and
  report the single line `TRANSPORT-BLOCK: <exact refusal text>`**. Do not spend
  the session doing work you will not be able to write.
- Git mutation is forbidden: no `commit`, `add`, `checkout`, `reset`, `stash`,
  `merge`, `push`, `worktree`. Read-only Git (`rev-parse`, `status`, `cat-file`,
  `show`, `diff`, `log`) is required and expected.
- You may create temporary files under your own scratch directory. In the
  repository you write exactly one new file, named below.

## Frozen subject

- Audit worktree: `C:\PSRETRY` (isolated, detached).
- Frozen subject commit: `40091b2b795be3339dc0df7014df6bfc091e4eca`.
- Required preflight: `git -C C:\PSRETRY rev-parse HEAD` equals that commit and
  `git -C C:\PSRETRY status --porcelain` is empty, before and after your work.

### Identity table — dual form (corrected)

The 2026-08-14 kickoff table was internally inconsistent and **unsatisfiable in
either form**: three rows carried Git-object (LF) identities while
`STATUS_PATHSCOPE.md` carried the working-tree (CRLF) identity. The repository
uses `* text=auto`, so a Windows checkout renders CRLF for the Markdown files
while `pathscope_prover.py` is byte-identical in both forms. Nothing in the
subject bytes changed; only the recorded identity is corrected here.

Both forms below were re-derived by the Lead from commit `40091b2b` on
2026-08-15. **Both must match.** Verify the working-tree form with `sha256sum` /
`Get-FileHash` on the files in `C:\PSRETRY`, and the Git-object form with
`git -C C:\PSRETRY cat-file -p 40091b2b:<path> | sha256sum` plus
`git -C C:\PSRETRY rev-parse 40091b2b:<path>` for the blob OID.

Paths are relative to `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/`.

| artifact | worktree bytes | worktree SHA-256 | git blob bytes | git blob SHA-256 | blob OID |
|---|---:|---|---:|---|---|
| `pathscope_prover.py` | 137520 | `28848d60f74a7c668db3019bbac58550f4a55c1c02038c013153316c711edf9c` | 137520 | `28848d60f74a7c668db3019bbac58550f4a55c1c02038c013153316c711edf9c` | `695ca9c951e31f53da9580d41326583d71086bb3` |
| `SELF_QA_PATHSCOPE.md` | 315514 | `75e5581ea33580d21f3e30d614c2122be3f5ab59156fa0a9746f52801efb4761` | 311577 | `f99d972f46c12ab1eea3fb426b9f9f39d98b6a3724cfcd229140d1433da0703d` | `96af8b035e243a6f39486e4e674dfde7448ae917` |
| `STATUS_PATHSCOPE.md` | 12359 | `6c2c409a338a9084c40a660150b803c916c3383940e5be6cb531e66c0d58a804` | 12197 | `4fb9ab89e369fee8389e33b032f0eff6d6e06d8768ee8b0ca1bd610f4ae6bb57` | `06e963d6915e9627a3e0538631f4b81eaf023ca5` |
| `PATHSCOPE_FINAL_OVERRIDE_REPAIR_REPORT_2026-08-14.md` | 21897 | `595ff2a4a76362550242780f60caf8ba2ad75243296944a8c9a14eedc5c504cf` | 21579 | `3dae5d6d245963254db368bc11f8295cd0b98ef78c16c44a14d690dfa8df5bb0` | `a45fc81a0b9e57f7cc6bfe0ece3c28b8b4079da6` |

If any cell fails to reproduce, that is a finding: record the exact observed
value and stop the identity phase before executing anything.

## Required reading (bounded — do not scan the repository)

Read in full, all inside `C:\PSRETRY`:

1. root `AGENTS.md`
2. `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`
3. Patterns 10, 12, and 13 in
   `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md`
4. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISION_PATHSCOPE_FINAL_OVERRIDE_2026-08-14.md`
5. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CAP_OVERRIDE_CODEX_T1_AUDIT_2026-08-13.md`
   (the verdict whose findings the repair claims to close)
6. the four frozen artifacts in the identity table

Do not read or audit RP6, RP7, transport, or SEC102 material. They are out of
scope and separately adjudicated.

## Mandatory execution audit

1. Extract and run the published PowerShell harness verbatim. Require clean
   outer completion, zero stderr, exact recorded transcript/hash reproduction,
   deterministic pairs, and unchanged identities afterward. Run it under the
   ordinary Turkish Windows profile; manual path substitution is not allowed.
   The 2026-08-13 audit recorded that five harness output hashes did not
   reproduce because Python/PowerShell path rendering defeated `<QA>`
   normalization — verify specifically whether the repair closed that.
2. Independently execute all five C-3 shapes through the frozen prover:
   whitespace list with later relative member, URI plus later absolute member,
   colon-bearing whole pathname, empty-only loader list, and executable command
   text without `/`. Require a terminal disposition or explicit fail-closed
   coverage for every admitted reading; zero facts plus PASS is red.
3. Independently execute both C-4 quoted declaration shapes and controls at
   prefix, `env`, and `export` call sites. Quote recovery must be reachable at
   the caller, not merely present in a helper.
4. Verify the prior C-2 closures and the quoted/escaped-space guard remain
   sound. `X="$ROOT dir/escape"` must remain one forbidden pathname, not two
   allowed pieces.
5. Inspect the complete assignment-member grammar for adjacent silent sinks,
   URI/list ambiguity, provenance loss, duplicate/empty-member collapse, and any
   admitted value with zero terminal accounting.
6. For every claimed closure, require literal D026 execution against the exact
   committed pre-repair blob and the frozen repaired bytes. Narration,
   source-only reasoning, or current-only RED labels are supplemental, not
   closure evidence. Verify every changed carried fence has the required
   discriminating-power proof against the same deviant output.
7. Confirm Python 3.12 feature-compatible parsing, the published self-QA result,
   and no attributable out-of-scope tracked or untracked delta.

## Output

Write exactly one new file:

`C:\PSRETRY\MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md`

It must contain, in order: the verdict line, your session header evidence
(model, effort, sandbox, session id), the identity re-derivation results for all
four artifacts in both forms, the executed commands and their real outputs for
each of the seven mandatory items, every finding classified as REQUIRED or NIT,
and an explicit statement of anything you could not verify.

Output hygiene: redirect bulky harness output to files and quote only summary
lines in the verdict. Do not paste large binary-ish or attack-shaped payload
text into your terminal narration.

Verdict must be exactly one of `PASS`, `PASS-WITH-NITS`, `REQUEST_CHANGES`, or
`BLOCK`. `PASS-WITH-NITS` may contain **no** required repair. If you find any
required change, say so plainly — the Lead will stop the lane at the owner
boundary rather than open another repair round.

## Hard exclusions

No host, network, deployment, service, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, or economic action.
No writing to `C:\LAB\Tradingview_LAB_CLEAN`, `C:\R7FINAL`, or any worktree other
than `C:\PSRETRY`.
