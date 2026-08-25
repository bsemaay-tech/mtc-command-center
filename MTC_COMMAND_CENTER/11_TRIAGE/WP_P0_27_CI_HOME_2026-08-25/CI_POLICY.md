# WP-P0-27 CI policy

**Status:** the day-one workflow is already on `master` through WAL-branch carry commit
`67a53a32` and master merge `110305c0`, before this package's own acceptance. The repository
required-check configuration remains unconfigured. **Audit tier: T1.** The workflow reports and
will gate repository changes only after the owner configures the required status check. It deploys
nothing and contacts no host or venue.

Do not mark the package gate closed yet. The gate requires a green suite run on `master`;
current `master` is red for two known GC-referent tests whose fix is on
`fix/gc-referent-tests-20260825` at `25eac11c`, pending audit and not yet merged. Required-check
activation waits for that fix to merge and for the check context to be green.

## Day-one check

The repo-root workflow `.github/workflows/ci.yml` runs on GitHub-hosted Ubuntu 24.04 runners
for pull requests into `master` and pushes to `master`. Its single day-one check is named
`Bridge suite (Python 3.12)` and does the following:

1. checks out the repository without persisting Git credentials;
2. selects Python 3.12, the version targeted by `IBKR_PAPER_BRIDGE/requirements.lock`;
3. installs only the exact hash-locked dependency closure with `--require-hashes`;
4. runs `python -m compileall -q IBKR_PAPER_BRIDGE` as the light lint/syntax check; and
5. runs the canonical suite command, `python -m pytest IBKR_PAPER_BRIDGE/tests -q`.

The workflow has read-only repository permission, uses no repository secret, runs no external
service integration, and cancels a stale run when a newer commit arrives for the same pull
request or ref. A failed job emits a GitHub error annotation and failure summary. GitHub's
native Actions failure notification/email is the day-one notification channel; delivery is
subject to each recipient's GitHub notification settings. No custom mail credential or paging
secret is introduced.

## Progressive required-check policy

After the GC-referent fix merges and the first Lead-run green workflow establishes the check
context, the Lead asks the owner to configure the repository rules for `master` as follows:

- Pull requests into `master` must pass `Bridge suite (Python 3.12)` before merge.
- The rule applies to every PR author and does not permit a PR to merge around a pending,
  skipped, cancelled or failed check.
- Direct Lead pushes remain allowed through the repository's explicit Lead/admin bypass. The
  bypass does not suppress CI: every direct push to `master` still starts the same workflow.
- The Lead records the exact ruleset or branch-protection setting and the first required-check
  demonstration in the acceptance evidence. This repository change is not performed by this lane.

Plain owner click path:

1. Open GitHub repository settings for `bsemaay-tech/mtc-command-center`.
2. Open **Rules** or **Branches**, then edit the rule that protects `master`.
3. Enable **Require status checks to pass before merging**.
4. Select **Bridge suite (Python 3.12)**.
5. Leave the explicit owner/Lead/admin bypass for direct pushes enabled.
6. Save the rule and preserve a screenshot or export of the setting.

Activation is intentionally progressive. Day one requires only the Bridge suite and compile
check. A later guard becomes required only after its owning package delivers the executable
check, D026 RED/GREEN evidence exists, the applicable audit tier accepts it, and the Lead adds
its stable check context to the repository rule.

## Red-master rule

`master` must never stay red. A failed push run is an immediate incident: stop unrelated merges
and direct pushes, inspect the first failing check, then either fix forward with the smallest
accepted repair or revert the offending commit with a new revert commit. Do not rewrite history
or bypass the workflow. The current red state is a named open dependency: two GC-referent tests
remain red on `master`, and their fix exists at `25eac11c` pending audit. The package gate closes
only after that fix merges and the suite is green. The native GitHub failure notification is the
day-one signal; the WP-P0-26 paging channel may become an additional channel only after that
separate package lands and is accepted.

## Resolved Windows checkout exception for the canonical ledger test

This section records a historical blocker that is no longer open on `master`. The earlier local
Windows result was a checkout-environment exception, not a waiver inside CI. The failing node was:

```text
IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate
```

`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json` is stored in Git with LF
bytes whose SHA-256 is the ledger's recorded
`f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e`. The root
`.gitattributes` supplied only `* text=auto`; on that Windows checkout Git reported
`i/lf w/crlf attr/text=auto`, producing working-tree SHA-256
`b6580e31c0a794a83455ce1cfc4efb17a061a34bbe0e9c5b7df1feeb3064114a`. Normalizing those 36
CRLF pairs back to LF reproduces the ledger hash exactly.

That test was therefore expected green on the Linux GitHub-hosted CI checkout and red on Windows
checkouts until the named repair landed. The repair was to pin the identity-bearing file in the
root `.gitattributes` as:

```gitattributes
MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json text eol=lf
```

That repair is now on `master`; `.gitattributes` resolves the file as `text eol=lf`, and the CRLF
ledger lane recorded a discriminating fresh-checkout regression plus full-suite evidence. If a
long-lived Windows worktree still reports `w/crlf` after merging the attribute change, that is a
stale checkout materialization issue, not a remaining policy exception; a fresh checkout honors
the pin. The current open blocker for this package is the GC-referent fix, not the ledger file.

## Future jobs: named slots, not built

The workflow is deliberately one job today. These future ops-verification classes get separate,
stable jobs when their owning packages provide accepted local fixtures and evidence sources:

| Future job ID | Responsibility | Day-one state |
|---|---|---|
| `ops_restore_proof_freshness` | Fail closed when the latest accepted restore proof is absent, malformed, stale or of unknown identity. | Placeholder only; unbuilt. |
| `ops_drill_currency` | Check that required failure, recovery and break-glass drills remain inside their owner-ratified currency windows. | Placeholder only; unbuilt. |
| `ops_credential_expiry` | Warn before accepted credential-expiry thresholds without reading, printing or storing credential values. | Placeholder only; unbuilt. |
| `ops_monitoring_health` | Verify accepted monitoring evidence and surface `UNKNOWN` as a stop rather than inferring health. | Placeholder only; unbuilt. |

The same home will later receive the package-owned golden, no-`alert(`, admission, parity,
contract, concurrent-writer and cleanup-ownership guards. None is represented as active today.
Any future check that contacts a host, reads account state, handles a credential or changes a
protected surface must be separately authorized and re-tiered; placement in this workflow does
not grant that authority.

## Rollback

Revert the workflow commit or remove the workflow through an accepted follow-up commit, then
remove its required-check context from the repository rule. No runtime, host or deployment state
is coupled to the workflow.
