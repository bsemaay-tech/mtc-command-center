# WP-P0-27 CI policy

**Status:** reconciled 2026-08-25 (lane AK) with the protection that is actually enforced. The
required-check configuration this page previously described as "unconfigured" is **live**:
repository ruleset **21444962 — "Protect master – required CI"**, enforcement `active`, created
2026-08-25T18:24:47+03:00. The exact configuration and the enforcement behavior actually observed
are recorded in "Live `master` protection" below; that section is the authority on this page and
supersedes the future-tense owner instructions this document previously carried. The workflow
itself reached `master` early, through WAL-branch carry commit `67a53a32` and master merge
`110305c0`, before this package's own acceptance. It deploys nothing and contacts no host or
venue. **Audit tier:** T1 for the workflow package (unchanged); the 2026-08-25 reconciliation
edit is documentation-only (T2).

The GC-referent dependency this page carried is closed: the repair merged to `master` as
`cef1d070` with the CI check green at 2026-08-25T15:04:24Z, **before** the ruleset was created
(15:24:47Z), so protection was switched on against an already-green `master` — the ordering this
policy required. The first merge through the protection was PR #127 (WP-P0-23) at `59bf7723`,
with `Bridge suite (Python 3.12)` green. Whether the WP-P0-27 package gate now closes is the
Lead's acceptance call, not this page's.

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
secret is introduced. Re-verified 2026-08-25 against the file as it stands on `master`;
unchanged.

## Live `master` protection (ruleset 21444962)

Recorded 2026-08-25 from the GitHub API (`gh api`), not the settings page. Re-verify with the
same read-only commands before relying on this section after any owner settings change:

```text
gh api repos/bsemaay-tech/mtc-command-center/rulesets
gh api repos/bsemaay-tech/mtc-command-center/rulesets/21444962
gh api repos/bsemaay-tech/mtc-command-center/rules/branches/master
gh api repos/bsemaay-tech/mtc-command-center/branches/master/protection
```

Observed:

- Exactly one ruleset exists: id `21444962`, name **"Protect master – required CI"**, target
  `branch`, source `bsemaay-tech/mtc-command-center` (Repository), enforcement **`active`**,
  created and updated `2026-08-25T18:24:47+03:00`.
- Conditions: `ref_name` includes `~DEFAULT_BRANCH` only and excludes nothing — the ruleset
  applies to the repository's default branch, `master`, and to nothing else.
- Exactly three rules reach `master`; the branch endpoint confirms all three come from ruleset
  21444962 and that no other rule, repository- or org-level, applies:
  1. `deletion` — `master` cannot be deleted.
  2. `non_fast_forward` — force-push and history-rewrite updates to `master` are rejected.
  3. `required_status_checks` — one required context, **`Bridge suite (Python 3.12)`**, reported
     by GitHub Actions (`integration_id` 15368), with
     `strict_required_status_checks_policy: true` (the PR head must be up to date with `master`
     before merging) and `do_not_enforce_on_create: false` (no create-time exemption).
- `bypass_actors` is **empty** and the querying credential's `current_user_can_bypass` is
  `never`: no actor, role or account holds a bypass in this ruleset.
- Legacy branch protection is absent — `branches/master/protection` returns 404 "Branch not
  protected". Protection is rulesets-only.

Enforcement behavior actually observed on 2026-08-25, recorded in the merge commit message of
`59bf7723` on `master`:

- A **direct push** to `master` was rejected with **GH013** ("required check expected").
- A check run on a non-`master`, non-PR ref cannot satisfy the rule, because `ci.yml` triggers
  only on pushes to `master` and PRs into `master`; a commit that has never been a PR head has
  no `Bridge suite (Python 3.12)` run. In practice `master` is therefore reached through a pull
  request whose head carries the green check.
- The PR was additionally required to **update its branch** against `master` before merging
  (the strict policy above).
- PR #127 then merged with `Bridge suite (Python 3.12)` green on `fff0ba8b`. **No admin
  override was used; the empty bypass list is deliberate.**

This corrects what this page and `LANE_REPORT.md` §"Owner action text" previously planned: an
explicit owner/Lead/admin bypass for direct pushes was **not** configured, and a direct push is
not a merge-around path. Changing that is an owner edit of ruleset 21444962, never a lane
action. Consequence for every lane: work reaches `master` only through a PR into `master` with
`Bridge suite (Python 3.12)` green on an up-to-date head — plan merges accordingly.

## Progressive required-check policy

The first required check is enforced today; the set is what stays progressive. Only
`Bridge suite (Python 3.12)` is in rule 21444962's required list. `master` also runs the
repo-root workflow `.github/workflows/pine-defang-guard.yml` (WP-P0-23), whose
`pine-alert-guard` check is green on `59bf7723` but is **not** required — that is this policy
operating as designed, not an oversight.

A later guard becomes required only after its owning package delivers the executable check, D026
RED/GREEN evidence exists, the applicable audit tier accepts it, and the Lead asks the owner to
add its stable check context to rule 21444962. Adding or removing a required context is a
repository-setting change owned by the owner/Lead; no implementation lane performs it. Day one
requires only the Bridge suite and compile check.

## Red-master rule

`master` must never stay red. A failed push run is an immediate incident: stop unrelated merges
and direct pushes, inspect the first failing check, then either fix forward with the smallest
accepted repair or revert the offending commit with a new revert commit. Do not rewrite history
or bypass the workflow. The native GitHub failure notification is the day-one signal; the
WP-P0-26 paging channel may become an additional channel only after that separate package lands
and is accepted.

Historical record (2026-08-25): the last red run on `master` was `110305c0`
(2026-08-25T12:10:43Z, failure). The GC-referent repair then merged as `cef1d070` ("repair the
two GC-referent tests that kept master red", T1 accepted 2026-08-25) and the run on it was green
at 15:04:24Z; `master` has been green since (`d5e5e98e` 15:08:03Z; `59bf7723` 15:53:06Z, with
both `CI` and `Pine Defang Guard` successful). The named open dependency this page previously
carried is closed, and protection was activated only after `master` turned green.

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
the pin. Neither the ledger file nor the GC-referent pair remains an open blocker for this
package; both are repaired and merged.

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
remove its required-check context from the repository rule (ruleset 21444962). No runtime, host
or deployment state is coupled to the workflow.
