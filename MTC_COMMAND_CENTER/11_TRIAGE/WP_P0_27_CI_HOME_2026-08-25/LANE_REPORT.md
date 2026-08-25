# Lane K report — WP-P0-27 repo-root CI

**Status:** **RECONCILED WITH MASTER; ACCEPTANCE GATE OPEN ON GC FIX MERGE**
**Role:** Codex implementer under Claude Lead
**Audit tier:** **T1** — the workflow governs whether guards execute
**Branch:** `feature/wp-p0-27-ci-home-20260825`
**Reconciled base:** merged `origin/master` `110305c0` into this feature branch on 2026-08-25.
I used a normal merge, not a rebase, because `origin/feature/wp-p0-27-ci-home-20260825`
already exists and preserving branch history avoids any force-push requirement.

## 2026-08-25 reconciliation record

This package's headline workflow reached `master` before this package was accepted. It was
carried onto the WAL capture-ordering branch by commit `67a53a32` (`ci: carry the T1-audited
day-one workflow onto this branch for the Linux proof run`) and then reached `master` through
merge commit `110305c0` on 2026-08-25. The Lead reported byte-identity between the copies.
The implementer rechecked the Git blob identity during reconciliation:

```text
HEAD:.github/workflows/ci.yml          3394d9ffdb53d3da0d94efe4f308f16a8838d1ba
origin/master:.github/workflows/ci.yml 3394d9ffdb53d3da0d94efe4f308f16a8838d1ba
```

Post-merge, `git diff origin/master...HEAD` shows exactly this package's four documents and no
`.github/workflows/ci.yml` delta. This branch does not undo, replace, or silently overwrite the
workflow already on `master`.

## Acceptance gate dependency

The package gate is not closed. The gate requires a green suite run on `master`. Current `master`
at `110305c0` is still red for the two known GC-referent tests because their repair is on
`fix/gc-referent-tests-20260825` at `25eac11c`, pending audit and not yet merged. With that fix
applied, the Bridge suite was recorded by the GC lane as `1370 passed, 1 warning`. This package
does not copy or reimplement that fix. The unblock condition is: `25eac11c` or its accepted
successor merges to `master`, then the complete Bridge suite and the GitHub check run green on
that master state.

## Owner action text for required check

Do not configure branch protection while `master` is red. After the GC-referent fix merges and the
`Bridge suite (Python 3.12)` check has a green run on the current `master` or PR context, ask Baris
to click exactly this:

1. Open GitHub repository settings for `bsemaay-tech/mtc-command-center`.
2. Open **Rules** or **Branches**, then edit the rule that protects `master`.
3. Turn on **Require status checks to pass before merging** for pull requests.
4. Select the status check named **Bridge suite (Python 3.12)**.
5. Ensure pending, skipped, cancelled, and failed checks cannot satisfy the rule.
6. Keep the explicit owner/Lead/admin bypass for direct pushes enabled.
7. Save the rule, then preserve a screenshot or export of the exact setting in the acceptance
   evidence.

## Scope and boundaries

Lane K originally added the first functioning repo-root GitHub Actions workflow and its
progressive policy, D026 live-demo plan and implementation report. After reconciliation with
`master`, the workflow itself is already upstream and the remaining package diff is documentation
only. This branch changes no Bridge runtime, trading logic, Pine, parity, MTC_V2, schema, host,
venue, credential or deployment surface. It uses no secret, self-hosted runner, scheduled data
job, Docker or WSL. The inert workflows under
`MTC_COMMAND_CENTER/02_MTC_BACKTEST/.github/workflows/` were not read as authority, ported,
enabled, edited or deleted.

## Package artifacts after reconciliation

Current branch delta beyond `origin/master`:

- `CI_POLICY.md` - progressive check policy, current gate dependency, owner action text, resolved
  Windows ledger note and future ops-check slots.
- `RED_GREEN_PLAN.md` - exact GREEN/RED/GREEN demonstration plan, gated on current `master`
  becoming green.
- `LINUX_RED_DIAGNOSIS.md` - Linux CI failure diagnosis, updated with downstream WAL and
  GC-referent repair status.
- `LANE_REPORT.md` - this reconciliation handoff.

Historical implementation artifacts before the workflow reached `master`:

- `.github/workflows/ci.yml` — Ubuntu 24.04, Python 3.12, hash-locked dependency install,
  `compileall`, canonical Bridge suite, stale-run cancellation and GitHub-native failure output.
- `CI_POLICY.md` — progressive PR-required-check policy, direct-Lead-push boundary, red-master
  response, Windows ledger exception and future ops-check slots.
- `RED_GREEN_PLAN.md` — exact Lead-owned GREEN → deliberate RED → revert GREEN demonstration and
  required-check proof.
- `LANE_REPORT.md` — this factual handoff.

## Independent checkout/hash verification

Commands run from the repository root before implementation:

```powershell
git check-attr --all -- MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
git ls-files --eol -- MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
```

Observed state:

```text
MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json: text: auto
i/lf w/crlf attr/text=auto
working_sha256=b6580e31c0a794a83455ce1cfc4efb17a061a34bbe0e9c5b7df1feeb3064114a
working_crlf_pairs=36
git_blob_sha256=f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e
git_blob_crlf_pairs=0
normalized_working_sha256=f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e
```

This independently confirmed the diagnosis at Lane K authoring time: the ledger records the
Git/LF artifact, while Windows checkout conversion alone changed the bytes. This historical note
is now superseded by the CRLF ledger repair that reached `master` before this reconciliation:
`.gitattributes` pins the identity-bearing file to `text eol=lf`, and the CRLF lane recorded a
fresh-checkout regression plus a full Bridge suite pass. The remaining acceptance blocker for this
package is therefore not the ledger file; it is the unmerged GC-referent test fix named above.

## Historical local full-suite evidence

Exact command:

```powershell
$env:PYTHONUTF8='1'
python -m pytest IBKR_PAPER_BRIDGE/tests -q
```

Environment and exact summary:

```text
Python 3.14.2
FAILED IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate
1 failed, 1350 passed, 1 warning in 113.18s (0:01:53)
```

The exception was `kvm2_ledger_validator.LedgerValidationError: publishable artifact hash
mismatch`. No other test failed. This is the one documented Windows-environmental failure allowed
by the resumed Lane K contract; the merged WAL and dashboard repairs are green. Full captured
output is outside the repository at `C:\tmp\LANE_K_FULL_SUITE_20260825.txt`.

## Reconciliation verification

Static workflow/policy checks run after the 2026-08-25 reconciliation edits:

```text
YAML safe_load: PASS (.github/workflows/ci.yml; root mapping; bridge job present)
Workflow semantic assertions: PASS (master PR/push triggers, Ubuntu 24.04, Python 3.12,
canonical suite command, no self-hosted/schedule/secret reference)

python -m compileall -q IBKR_PAPER_BRIDGE
compileall: PASS

git diff --check
git diff --check: PASS

actionlint: not installed

stale-claim sweep over the WP-P0-27 package: PASS, no retained stale claim patterns
```

Local full-suite verification used a fresh detached worktree at reconciliation merge `7aa85ef4`
so the newly merged `.gitattributes` LF pin materialized correctly:

```text
git ls-files --eol -- MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
i/lf    w/lf    attr/text eol=lf       MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json

Get-FileHash SHA256 ledger_schema.json
F4CDECE5098D4E915431F9FD916005BBC3D79EA5AF89A0535E3E21D668BDA90E

python -m pytest tests -q --ignore=TSP1009B.pytest_tmp_s1r1
1370 passed, 1 warning in 158.35s (0:02:38)
```

That Windows/Python 3.14 local result is supplemental only. It does not close the acceptance gate,
because the gate requires a green suite run on `master` in the GitHub/Linux check context, and
that context remains blocked by the unmerged GC-referent fix at `25eac11c`.

## Local workflow validation

Exact commands and output after authoring:

```text
python -c "... yaml.safe_load(Path('.github/workflows/ci.yml').read_text(...)) ..."
YAML safe_load: PASS (.github/workflows/ci.yml; root mapping; bridge job present)
Workflow semantic assertions: PASS (master PR/push triggers, Ubuntu 24.04, Python 3.12,
canonical suite command, and no self-hosted/schedule/secret reference)

python -m compileall -q IBKR_PAPER_BRIDGE
compileall: PASS

git diff --check
git diff --check: PASS
```

`actionlint` is not installed in this worktree. It was not added because Lane K may introduce no
new unpinned dependency. The live GitHub parser/run remains part of the Lead-owned demonstration.

## Reconciliation commit and staged paths

Exact paths intended for the reconciliation commit:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/CI_POLICY.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/LANE_REPORT.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/LINUX_RED_DIAGNOSIS.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/RED_GREEN_PLAN.md
```

## Open items owned by the Lead

1. Perform the independent T1 Gate 5 review and accept or return a focused repair.
2. Wait for the GC-referent test fix at `25eac11c` or its accepted successor to merge to
   `master`; do not duplicate that fix in this branch.
3. After `master` is green, run and preserve the live GREEN/RED/GREEN demonstration in
   `RED_GREEN_PLAN.md`.
4. After that green check context exists, configure and prove the PR required-check repository
   setting while retaining the explicit
   direct-Lead-push bypass.
5. Confirm native GitHub failure email delivery for the subscribed Lead account.

The implementer pushed this reconciliation branch as requested by the dispatch. No live GitHub
repository setting, host, deploy, venue or notification-channel action is claimed.

## Lane R status - 2026-08-25 Linux RED diagnosis

**Status:** **DIAGNOSIS COMPLETE; DOWNSTREAM REPAIR STATUS UPDATED**

**Role:** Codex implementer under Claude Lead

**Audit tier:** **T2** documentation for the original diagnosis; the protected WAL/cutover
repair was separately authorized, implemented, audited, and merged through the WAL lane.

GitHub run `32781394607` was fetched with the requested `gh run view ... --log-failed`
command and traced at its exact PR head,
`3899d6f984ddc7c41b632e99e616941524b0cec1`. The Ubuntu/Python-3.12.14 result was
`25 failed, 1326 passed, 1 warning`: two `test_order_state.py` GC-referent failures
and 23 `test_wal_state_bundle.py` failures.

The order-state pair is classified **TEST defect**. The original diagnosis understated the
blast radius by attributing it only to CPython 3.12: a later standalone CPython 3.13.13 probe also
exposed the Enum-member runtime dictionary through `gc.get_referents`. Those dictionaries are
not backing storage for `_ImmutableMapping`; the adjacent behavioral mutation tests and direct
holder-attack tests pass. The fix is on `fix/gc-referent-tests-20260825` at `25eac11c`,
pending audit and not yet merged.

The WAL cluster was classified **PRODUCT defect - serious on Linux deployment**. That defect is
fixed and merged on `master` through merge `110305c0`. The merged WAL lane includes D026
coverage that can fail for the capture-ordering bug and for the SHM identity fields.

Full original evidence, all 25 node classifications, and the snapshot/locking/order mechanism
are recorded in `LINUX_RED_DIAGNOSIS.md`; that document now also records what happened after the
diagnosis. No WSL, Docker, source edit in this branch, host, deploy, credential, broker, trading,
Pine, parity, schema, or MTC action occurred.
