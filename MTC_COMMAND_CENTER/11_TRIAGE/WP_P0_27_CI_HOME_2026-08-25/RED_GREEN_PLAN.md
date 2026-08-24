# WP-P0-27 live RED/GREEN and required-check plan

**Executor:** Claude Lead after T1 acceptance. Lane K does not push, change repository settings,
or run the live demonstration. Preserve the green and red run URLs, job logs, notification
evidence and repository-rule screenshot/export in the final acceptance package.

## 1. Establish GREEN on the implementation branch

From the accepted Lane K worktree, record the immutable implementation identity and push only
the feature branch:

```powershell
git status --short --branch
$laneCommit = git rev-parse HEAD
git push -u origin feature/wp-p0-27-ci-home-20260825
```

Open a pull request from `feature/wp-p0-27-ci-home-20260825` into `master`. In GitHub Actions,
open workflow `CI`, job `Bridge suite (Python 3.12)`, and verify all four executable phases are
green: checkout/setup, hash-locked install, compile, and
`python -m pytest IBKR_PAPER_BRIDGE/tests -q`. The Linux checkout must pass the canonical ledger
test described in `CI_POLICY.md`; a skip, xfail or filtered suite is not GREEN. Record the run URL,
head SHA, runner OS, Python version, exact pytest summary and job conclusion.

## 2. Make the check required for PRs into master

After GitHub has registered the green check context, configure the `master` ruleset or branch
protection to require `Bridge suite (Python 3.12)` for pull requests. Pending, skipped, cancelled
and failed conclusions must not satisfy the rule. Retain the explicit Lead/admin bypass so direct
Lead pushes remain possible; do not disable the push-to-`master` workflow trigger. Demonstrate
that the green PR is merge-eligible and record the exact setting. Do not merge merely to prove
the setting.

## 3. Falsify the check: RED

Create a throwaway branch from the accepted Lane K commit and add exactly one deliberate failing
test. The mutation file is `IBKR_PAPER_BRIDGE/tests/test_ci_red_probe.py`; it changes no Bridge
runtime behavior.

```powershell
git switch -c demo/wp-p0-27-red-20260825 $laneCommit
@'
def test_ci_red_probe():
    assert False, "deliberate WP-P0-27 D026 red probe"
'@ | Set-Content -LiteralPath 'IBKR_PAPER_BRIDGE\tests\test_ci_red_probe.py' -Encoding utf8NoBOM
git add -- IBKR_PAPER_BRIDGE/tests/test_ci_red_probe.py
git commit -m "test(ci): deliberate WP-P0-27 red probe"
$redCommit = git rev-parse HEAD
git push -u origin demo/wp-p0-27-red-20260825
```

Open a throwaway PR from `demo/wp-p0-27-red-20260825` into `master`. Verify all of the following:

- `Bridge suite (Python 3.12)` is RED at the `Run Bridge test suite` step;
- the log names `test_ci_red_probe` and the deliberate assertion message;
- the required check blocks merge; and
- GitHub produces the native failure notification/email for the subscribed Lead account.

Record the run URL, `$redCommit`, exact failure output, blocked-merge evidence and notification
timestamp. If no email arrives, verify the GitHub Actions notification settings and rerun the
demonstration; an error annotation alone does not prove email delivery.

## 4. Revert the falsification: GREEN again

Revert the red commit on the same throwaway branch, push, and observe the same PR return to green:

```powershell
git revert --no-edit $redCommit
$greenAgainCommit = git rev-parse HEAD
git push origin demo/wp-p0-27-red-20260825
```

Verify that `test_ci_red_probe.py` is absent, the complete unfiltered Bridge suite is green, and
the required check again permits the PR to merge. Record the second green run URL, SHA and exact
pytest summary. Do not merge the throwaway PR. Retain or close it according to the Lead's normal
evidence policy; do not delete the branch without the required authority.

## 5. D026 evidence table the Lead must complete

| Arm | Commit | Run URL | Required-check result | Pytest evidence | Notification evidence |
|---|---|---|---|---|---|
| GREEN (implementation) | Pending Lead run | Pending | Pending | Pending | Not applicable |
| RED (deliberate probe) | Pending Lead run | Pending | Must block | Must name `test_ci_red_probe` | Pending email proof |
| GREEN (revert) | Pending Lead run | Pending | Must allow | Full suite, no filtering | Not applicable |

The package remains `LIVE DEMO PENDING LEAD` until all three arms and the repository setting are
recorded. A source review of the YAML is supplemental and cannot replace this execution.
