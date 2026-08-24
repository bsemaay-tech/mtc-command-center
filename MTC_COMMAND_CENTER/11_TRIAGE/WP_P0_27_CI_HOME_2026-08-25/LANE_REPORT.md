# Lane K report — WP-P0-27 repo-root CI

**Status:** **BUILT, LIVE DEMO PENDING LEAD**
**Role:** Codex implementer under Claude Lead
**Audit tier:** **T1** — the workflow governs whether guards execute
**Branch:** `feature/wp-p0-27-ci-home-20260825`
**Updated base:** fast-forwarded from `4691a9dd` to `cbe92101` (`origin/master`) before work

## Scope and boundaries

Lane K adds the first functioning repo-root GitHub Actions workflow and its progressive policy,
D026 live-demo plan and implementation report. It changes no Bridge runtime, trading logic, Pine,
parity, MTC_V2, schema, host, venue, credential or deployment surface. It uses no secret,
self-hosted runner, scheduled data job, Docker or WSL. The inert workflows under
`MTC_COMMAND_CENTER/02_MTC_BACKTEST/.github/workflows/` were not read as authority, ported,
enabled, edited or deleted.

## Built artifacts

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

This independently confirms the merged diagnosis: the ledger records the Git/LF artifact, while
Windows checkout conversion alone changes the bytes. The Linux CI checkout is expected green;
the Windows checkout remains red until the exact `.gitattributes` LF-pin repair named in
`CI_POLICY.md` lands through its own scope.

## Local full-suite evidence

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

## Commit and staged paths

Mandated commit message:

```text
feat(wp-p0-27): repo-root CI day-one workflow + progressive check policy (T1, lane K 2026-08-25)
```

The implementation commit SHA cannot be embedded in the commit that computes that same SHA;
the final implementer handoff prints the resolved SHA. Exact paths intended for staging:

```text
.github/workflows/ci.yml
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/CI_POLICY.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/RED_GREEN_PLAN.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/LANE_REPORT.md
```

## Open items owned by the Lead

1. Perform the independent T1 Gate 5 review and accept or return a focused repair.
2. Push the feature branch; Lane K performs no push.
3. Run and preserve the live GREEN/RED/GREEN demonstration in `RED_GREEN_PLAN.md`.
4. Configure and prove the PR required-check repository setting while retaining the explicit
   direct-Lead-push bypass.
5. Confirm native GitHub failure email delivery for the subscribed Lead account.

The Windows LF-pin repair is separately scoped and is not an open implementation item inside
Lane K. No live GitHub, repository-setting, host, deploy, venue or notification-channel action is
claimed.
