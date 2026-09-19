# T1 review — WP-P0-27 CI workflow additions: PR #193 (`a3325836`) and PR #194 (`63b7bbe0`)

**Reviewer:** exact `claude-opus-5`, effort xhigh, Wednesday 2026-09-16 lane 5 (started by hand after lanes 1-4).
**Role:** independent T1 reviewer of two GitHub Actions workflow changes. Both PRs are Lead-authored (Claude Opus 5 Lead, disclosed); the Lead is not a reviewer here. I merged nothing, pushed nothing, touched no GitHub state; every `gh` call was a GET (listed with output in Appendix B).
**Date of the GitHub reads in this report:** 2026-09-16 (the ruleset and PR states below are my own live reads, not copies from a record).

---

## 0. Verified identities (COMPUTED)

### 0.1 Worktree HEADs

```
git -c safe.directory=* -C C:/tmp/P027_CI_20260915 rev-parse HEAD
a33258367739400017c11a7e498030238f9b1564

git -c safe.directory=* -C C:/tmp/P027_OPSA_CI_20260915 rev-parse HEAD
63b7bbe0981bddafb94018a3520f3c5c82e8e4f4
```

| Worktree | Observed HEAD | Pinned HEAD | Match |
|---|---|---|---|
| `C:/tmp/P027_CI_20260915` | `a33258367739400017c11a7e498030238f9b1564` | `a33258367739400017c11a7e498030238f9b1564` | **YES** |
| `C:/tmp/P027_OPSA_CI_20260915` | `63b7bbe0981bddafb94018a3520f3c5c82e8e4f4` | `63b7bbe0` (prefix) | **YES** |

Neither HEAD differs from its pin, so neither PR takes an automatic `BLOCK`.

### 0.2 The HEADs GitHub reports for the two PRs

| PR | `gh pr view … --json headRefOid` | Worktree HEAD | Match |
|---|---|---|---|
| #193 | `a33258367739400017c11a7e498030238f9b1564` | same | **YES** |
| #194 | `63b7bbe0981bddafb94018a3520f3c5c82e8e4f4` | same | **YES** |

Both PRs: `state: OPEN`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`, `isDraft: false`, `mergedAt: null`, `mergeCommit: null`, `baseRefName: master`, `baseRefOid: fcac0ac67cf2682693ad28138b1a56e15a0846f2`, `latestReviews: []`, `reviewDecision: ""`.
So both are open, unmerged, and neither carries a GitHub review — consistent with "the T1 verdict is this lane's".

### 0.3 File hashes

`git -c safe.directory=* show <rev>:<path>` output, redirected to a scratch file under `C:/tmp/OPUS_P027CI_SCRATCH/`, then `sha256sum`:

| Object | sha256 of the bytes | Git blob OID |
|---|---|---|
| `a3325836:.github/workflows/research-gates.yml` (175 lines) | `1eab2468d75b99ebe333df684034489dcde5945d693ba68a676226070cfc42eb` | `609de49aa9f3db635ba9ed57753028c262148fb7` |
| `63b7bbe0:.github/workflows/opsa-tests.yml` (55 lines) | `dbacda3e29c396f9bd5021ce91398b809b65bc255e2b4361dc63adddcf8cb5d5` | `3e4643445d7b5bca40289af82daa74fb48996b6b` |
| `fcac0ac6:.github/workflows/research-gates.yml` (base) | `cfaa3862fa57ed79915ab6077cca4bdc3a4c0541cc8e92036d68206270e5ba2d` | `e8c520f62a35c1588ac84dcc6cfcc18854e2a009` |
| `55ab90b8:.github/workflows/research-gates.yml` (RED intermediate) | `a274bfc64122854fb2f5d95595c606d02274aabc24662d97d39ccf441537086f` | `ea3ef2b9…` (from the diff index line) |

**Local bytes == GitHub bytes** (this is the identity check that matters, since I reviewed local worktrees and judged runs on GitHub):

| Path @ rev | Local `git rev-parse <rev>:<path>` | `gh api contents …?ref=<rev> --jq .sha` | Match |
|---|---|---|---|
| `.github/workflows/research-gates.yml` @ `a3325836` | `609de49aa9f3db635ba9ed57753028c262148fb7` | `609de49aa9f3db635ba9ed57753028c262148fb7` | **YES** |
| `.github/workflows/opsa-tests.yml` @ `63b7bbe0` | `3e4643445d7b5bca40289af82daa74fb48996b6b` | `3e4643445d7b5bca40289af82daa74fb48996b6b` | **YES** |
| `.github/workflows/opsa-tests.yml` @ `e9314079` (RED demo branch, PR #195) | — | `3e4643445d7b5bca40289af82daa74fb48996b6b` | **identical to #194's head blob** |

The last row matters: PR #195's RED demo exercised the *exact same workflow bytes* as PR #194 — the demo is not a lookalike file.

`e8c520f6` (base) matches the acceptance packet's evidence index E1 and `GH_QUERIES_20260915_NIGHT.txt:24`; `609de49a` matches the packet's E10 line. Both reproduce.

### 0.4 Scope of each diff (full tree, not just `.github/workflows`)

```
git -c safe.directory=* diff fcac0ac6 a3325836 --stat -- .
 .github/workflows/research-gates.yml | 85 +++++++++++++++++++++++++++++++++++-
 1 file changed, 84 insertions(+), 1 deletion(-)

git -c safe.directory=* diff fcac0ac6 63b7bbe0 --stat -- .
 .github/workflows/opsa-tests.yml | 55 ++++++++++++++++++++++++++++++++++++++++
 1 file changed, 55 insertions(+)
```

Each PR changes exactly one file, and `gh pr view … --json files` agrees (#193: one `MODIFIED`, +84/-1; #194: one `ADDED`, +55/-0). Nothing outside `.github/workflows/` moves in either PR.

---

## 1-6. Per-item findings, PR #193 vs PR #194

| # | Item | PR #193 (`research-gates.yml` @ `a3325836`) | PR #194 (`opsa-tests.yml` @ `63b7bbe0`) | Evidence |
|---|---|---|---|---|
| **1a** | `permissions` | `contents: read` at workflow level, `research-gates.yml:29-30`; no job overrides it, so every job (incl. the two new ones) inherits `contents: read` and all other scopes resolve to `none` | `contents: read` at workflow level, `opsa-tests.yml:21-22`; single job, no override | workflow bytes |
| **1b** | `persist-credentials: false` on every checkout | YES — all three checkouts: `:47-48`, `:119-120`, `:152-153` | YES — `:44-45` | workflow bytes |
| **1c** | Secrets referenced | NONE — no `secrets.` token anywhere in the file | NONE | grep over both files: 0 hits for `secrets.` |
| **1d** | `pull_request_target` | ABSENT. Triggers are `pull_request: branches: [master]` (`:22-24`) and `push: branches: [master]` (`:25-27`) | ABSENT. Same two triggers, `:14-19` | workflow bytes |
| **1e** | `schedule:` (P0-27 non-goal) | ABSENT | ABSENT | grep: 0 hits for `schedule:` in either file |
| **1f** | Self-hosted runner | NONE — `ubuntu-24.04` (`:39`, `:144`), `windows-2025` (`:106`), all GitHub-hosted labels; runs confirm hosted runner names (`GitHub Actions 1000000838/839/840`) | NONE — `windows-2025` (`:31`) | `gh api …/runs/34963602576/jobs` `.labels` + `.runner_name` |
| **1g** | Deploy / host / venue contact | NONE. New steps run only `git config`, `pip install`, `python <checker>.py`, `python -m pytest`, `python -m ruff`. Additionally `check_p030_market_data_contracts.py:735-736` monkey-patches `socket.socket.connect`/`socket.create_connection`, restores them at `:1239-1240` and asserts `attempts == []` at `:1242` — the GREEN log prints `NETWORK ATTEMPTS: 0` | NONE. One step: `python -m unittest test_opsa -v`. The suite is stdlib-only; its only `subprocess` use re-invokes the local `restore.py` | workflow bytes; GREEN job log `104362756252` |
| **1h** | Artifact upload | NONE — the only `uses:` are `actions/checkout` and `actions/setup-python` | NONE — same | `grep -n "uses:"` over both files |
| **1i** | Writes to `GITHUB_STEP_SUMMARY` | One, pre-existing and untouched by this PR (`:87-97`, the WP-P0-20 acceptance report). The diff adds nothing to it | NONE | `git diff fcac0ac6 a3325836` — the added hunk starts after `:95` of the base file |
| **2a** | Action pinning | Tag pins: `actions/checkout@v4` (`:46`, `:118`, `:151`), `actions/setup-python@v5` (`:51`, `:123`, `:156`) | Tag pins: `actions/checkout@v4` (`:43`), `actions/setup-python@v5` (`:48`) | workflow bytes |
| **2b** | Consistency with the repo's other workflows | MATCHES. `ci.yml:27,32` = `checkout@v4` + `setup-python@v5`; `pine-defang-guard.yml:15,16` = the same. No workflow in the repo SHA-pins an action | MATCHES, same convention | `git show a3325836:.github/workflows/{ci,pine-defang-guard}.yml` |
| **2c** | Is a SHA pin *required* by policy? | NO. I read all 189 lines of `CI_POLICY.md`; no line requires a SHA pin for actions. I therefore do **not** claim one | NO, same | `CI_POLICY.md` full read |
| **2d** | Python pin | `"3.12"` on all three jobs (`:53`, `:125`, `:158`) | `"3.12"` (`:50`). Load-bearing: the closed-partition checker in #193 uses `Path.is_junction()` (3.12+) | workflow bytes; `check_p030_closed_partition_backup_adapter.py:272` |
| **2e** | Ruff pin | `ruff==0.16.4` by version, no `--require-hashes` (`:170`), in the same job whose `:160-163` install *does* use `--require-hashes`. `MTC_COMMAND_CENTER/contracts/constraints.txt` at `a3325836` carries `ruff==0.16.4` — **verified by `git show`**, so the workflow comment at `:169` is accurate | N/A — the job installs nothing | see **F-01** |
| **3a** | Commands run what they claim | YES. `check_p030_{market_data_contracts,opsa_heartbeat_adapter,closed_partition_backup_adapter}.py` all exist at `a3325836` (repo root, so the default `working-directory` is right); `MTC_COMMAND_CENTER/contracts/tests/` holds 7 test modules; `constraints.txt` and the two lint paths exist | YES. `MTC_COMMAND_CENTER/tools/opsa/test_opsa.py` exists; **33** `def test_` methods, matching the "33 unittest tests on master bytes" claim | `git ls-tree -r a3325836`; `grep -c "^\s\+def test_"` = 33 |
| **3b** | Working directory / interpreter | Correct. `contracts-and-lint` runs pytest with `working-directory: MTC_COMMAND_CENTER/contracts` (`:166`) as `python -m pytest` — the `-m` form puts the CWD on `sys.path`, which is what makes `mtc_contracts` importable (it is **not** in the Bridge lock, so nothing shadows the working tree). Ruff at `:172-175` has no `working-directory`, so its two paths resolve from the workspace root — correct | Correct. `working-directory: MTC_COMMAND_CENTER/tools/opsa` (`:54`); `test_opsa.py:26` also does `sys.path.insert(0, <own dir>)` so the sibling modules import either way | workflow bytes; `git show a3325836:IBKR_PAPER_BRIDGE/requirements.lock \| grep -i mtc` → 0 hits |
| **3c** | Observed test counts | GREEN run `34963602576`: contracts `50 passed in 0.32s`; Ruff `All checks passed!`; Windows job `P030 MARKET DATA CONTRACTS CHECK: PASS`, then `Ran 10 tests … OK` and `Ran 44 tests … OK` | GREEN run `34983809921`: `Ran 33 tests in 1.471s` / `OK` | job logs `104362756214`, `104362756252`, `104430634198` |
| **3d** | `core.longpaths` **before** checkout | YES — `:114-115` precedes the checkout at `:117-118` | YES — `:39-40` precedes `:42-43` | workflow bytes |
| **3e** | Is `core.longpaths` the reason `55ab90b8` failed? | **YES, proved as a controlled experiment.** `git diff 55ab90b8 a3325836 --stat -- .` is `1 file changed, 5 insertions(+)` and the whole diff is exactly the `Enable long paths for the checkout` step. Run `34961383292` @ `55ab90b8`: job `P0-30 checkers (Python 3.12, Windows)` = **failure at step `Check out repository`**, all later steps `skipped`; the other two jobs `success`. Job log `104355519781` line 118: `##[error]error: unable to create file MTC_COMMAND_CENTER/03_QUANTLENS/research/restart_transcript_intake_audit_…: Filename too long`. Run `34963602576` @ `a3325836` (the 5 added lines being the only change): the same job `success` | Inherits the same fix; `opsa-tests.yml:37-38` cites PR #193's first run as the reason | `gh api …/runs/34961383292/jobs`; `gh api …/jobs/104355519781/logs` |
| **3f** | `continue-on-error` / `fail-fast` semantics | No `fail-fast` (no matrix anywhere). `continue-on-error` appears **once**, at `:89`, on the pre-existing WP-P0-20 report-only step, which the diff does not touch. **None of the three new P0-30 steps or the four new contracts/lint steps carries it** — a failure in any of them fails its job | No `continue-on-error`, no matrix, one step | workflow bytes; `grep -n continue-on-error` → `:89` only |
| **3g** | Does the informational job actually go RED on a *test* failure? | **Structurally yes, demonstrated only for the checkout step.** PR #193's RED demo is a *checkout* failure, not a test failure — see **NOT VERIFIED #4** | **YES, demonstrated with a real test failure.** PR #195 run `34983897746`: step `OPS-A unit tests` **failure**; log: `AssertionError: deliberate WP-P0-27 D026 red probe …`, `Ran 34 tests in 0.985s`, `FAILED (failures=1)`, `##[error]Process completed with exit code 1.` (33 real tests + 1 injected probe) | `gh api …/runs/34983897746/jobs`; job log `104430937775` |
| **4a** | Does the PR change the ruleset? | NO — it cannot; and its diff touches one workflow file only | NO — same | `--stat` above; a workflow file cannot edit a ruleset |
| **4b** | Live ruleset (my read, 2026-09-16) | `21444962 "Protect master – required CI"`, `enforcement: active`, `bypass_actors: []`, `current_user_can_bypass: "never"`, rules = `deletion`, `non_fast_forward`, `required_status_checks` with `strict_required_status_checks_policy: true` and **exactly two** contexts: `Bridge suite (Python 3.12)` and `pine-alert-guard` (both `integration_id: 15368`). `updated_at: 2026-08-29T11:25:28.137+03:00` — i.e. **unchanged since before either PR branch existed**. `gh api …/rulesets` returns exactly one ruleset | same ruleset, same reading | `gh api repos/…/rulesets/21444962` (Appendix B.23) |
| **4c** | Do the new job names collide with a required context? | NO. New contexts: `P0-30 checkers (Python 3.12, Windows)`, `Contracts tests and Ruff (Python 3.12)` (plus the pre-existing `Research gate checkers (Python 3.12)`) | NO. New context: `OPS-A tests (Python 3.12, Windows)` | `gh pr view … --json statusCheckRollup` |
| **4d** | **Can a red run of these jobs block a merge into `master`?** | **NO.** The required list is exactly the two contexts named in 4b; every job these PRs add is outside it. A red informational job leaves `mergeStateStatus` driven solely by the two required checks | **NO**, same | ruleset + rollup |
| **4e** | Do any evidence documents claim otherwise? | **NO.** `RED_DEMO_EVIDENCE_20260915.md:10` attributes PR #192's `BLOCKED` to `Bridge suite (Python 3.12): FAILURE` and marks `Research gate checkers: SUCCESS (not required)`; `:15` says explicitly "The `Research gates` and `Vercel` checks are informational (not in ruleset 21444962)" | **NO, and the record pre-empts the misreading.** `P027_OPSA_CI_EVIDENCE_20260915.md:13` states that PR #195's `BLOCKED` "came from the required `Bridge suite (Python 3.12)` check still being pending at that moment, not from the informational OPS-A job (which cannot block a merge by itself)". I reproduced this from `pr195_state_RED.json`: `Bridge suite (Python 3.12)` conclusion `""` (pending), `OPS-A tests …: FAILURE`, `mergeStateStatus: BLOCKED` | grep across both evidence dirs (Appendix B.31) |
| **5** | Records honesty | See §5 below — 2 reproducible NITs (**F-08**, **F-09**), 0 required | See §5 below — the OPS-A evidence note reproduces on every number I checked | §5 |
| **6** | Conflict with the other PR | Touches `.github/workflows/research-gates.yml` only | Touches `.github/workflows/opsa-tests.yml` only | `git diff fcac0ac6 <sha> -- .github/workflows` for each |
| **6b** | Conflict verdict | **No conflict in either merge order** — disjoint paths from a common base (`fcac0ac6`) | same | see §6 |

---

## 5. Records honesty — claim by claim

Every number below I re-derived from the workflow bytes or from my own `gh` GET, not from the record's prose.

| Claim, and where | My independent check | Result |
|---|---|---|
| Packet E1: base workflow blobs `ci.yml 3394d9ff…`, `pine-defang-guard.yml db5a950b…`, `research-gates.yml e8c520f6…` @ `fcac0ac6` | `git diff` index line gives `e8c520f6` for `research-gates.yml`; `GH_QUERIES_20260915_NIGHT.txt:22-24` lists all three | **REPRODUCED** (the `research-gates.yml` one directly) |
| Packet E10 / `P027_CI_ADDITIONS_EVIDENCE:12`: PR #193 head `a3325836`, blob `609de49a…`, all checks SUCCESS, `CLEAN`, OPEN, unmerged | `gh pr view 193`; `gh api contents …?ref=a3325836` | **REPRODUCED**, still true 2026-09-16 |
| Packet §2(c) / E2: ruleset active, 2 required contexts, strict, 0 bypass actors | `gh api …/rulesets/21444962` | **REPRODUCED** verbatim, incl. `updated_at` |
| Packet §5.1 / E6 / `CI_POLICY.md:17`: 61 `ci.yml` runs on `master` — 60 success, 1 failure, the failure being `32846169952` @ `110305c0`, 2026-08-25T12:10:43Z | `gh api …/workflows/ci.yml/runs?branch=master&per_page=100` → `{"total":61,"conclusions":{"failure":1,"success":60}}`; `…&status=failure` → exactly `{"id":32846169952,"head_sha":"110305c0790b…","created_at":"2026-08-25T12:10:43Z"}` | **REPRODUCED exactly** |
| `P027_CI_ADDITIONS_EVIDENCE:13`: "the 50 contracts tests … execute" | GREEN job log `104362756214`: `50 passed in 0.32s` | **REPRODUCED** |
| `P027_CI_ADDITIONS_EVIDENCE:10`: the first run failed at the checkout step with `Filename too long` | job log `104355519781:118` | **REPRODUCED** (exact error line) |
| `P027_CI_ADDITIONS_EVIDENCE:11`: commit 2 added the longpaths step, "nothing else changed" | `git diff 55ab90b8 a3325836 --stat -- .` = `1 file changed, 5 insertions(+)`, and the hunk is exactly that step | **REPRODUCED** |
| `P027_OPSA_CI_EVIDENCE:9`: `Ran 33 tests … OK` on master bytes | 33 `def test_` in `test_opsa.py` @ `a3325836`; GREEN job log `104430634198`: `Ran 33 tests in 1.471s` / `OK` | **REPRODUCED** |
| `P027_OPSA_CI_EVIDENCE:13`: RED run `34983897746` failure at `OPS-A unit tests`, `Ran 34 tests`, `FAILED (failures=1)`; PR #195 closed unmerged | `gh api …/runs/34983897746/jobs`; job log `104430937775`; `gh pr view 195` → `state: CLOSED`, `mergedAt: null`, `closedAt: 2026-09-15T14:47:47Z` | **REPRODUCED** |
| `P027_OPSA_CI_EVIDENCE:13`: PR #195's `BLOCKED` came from the pending required check, not the informational job | `pr195_state_RED.json` shows `Bridge suite (Python 3.12)` conclusion `""` while `OPS-A tests …` is `FAILURE` | **REPRODUCED** — and this is an unusually careful correction to have written down |
| `P027_OPSA_CI_EVIDENCE:15`: "the P0-26 candidate `d81b07f6` (39 tests) is NOT what CI runs — CI runs whatever `test_opsa.py` is on the PR's head/master (33 tests on `fcac0ac6`)" | consistent with the module-name invocation at `opsa-tests.yml:55` | **CONSISTENT** — and it is exactly the mechanism behind **F-06** |
| `CI_POLICY.md:14-25` (Acceptance 2026-09-15 paragraph) | Each cited fact re-checked above; the paragraph is careful to say "This acceptance changes no setting and merges no PR" and lists R12 as backlog "wired in PR #193, unmerged, T1 review pending" | **ACCURATE** |
| `RED_DEMO_EVIDENCE_20260915.md:7`: "no `failure` conclusion existed in the last 200 CI runs before today" | My live query returns one pre-existing failure on `master` (`32846169952`, 2026-08-25). The packet already corrects this at `:60` §5.1 and calls itself the erratum — but the sentence is still in the evidence file uncorrected | **FALSE AS WRITTEN → F-08** |
| `CI_POLICY.md:107-111`: "Only `Bridge suite (Python 3.12)` is in rule 21444962's required list … `pine-alert-guard` … is **not** required" | The live ruleset requires **both**; the same file says so at `:19-20` | **STALE / SELF-CONTRADICTORY → F-09** |

### Two facts that post-date the review brief (not defects; recorded so the verdict rests on current state)

The brief (`REVIEW_BRIEF.md:8`, written 2026-09-15 18:4xZ) says all three Gemini attempts on PR #193 were wrapper-voided and that "PR #194 has had no reviewer yet". Both were true when written; the files show later events:

- `P027_CI_GEMINI/LEAD_ADJUDICATION_P027_CI_GEMINI.md:3`: **attempt 4 COUNTED** at 20:08-20:11Z — PASS-WITH-NITS ×2, 0 REQUIRED, 26 native reads / 0 outside; NITs N-01 = Ruff by version, N-02 = `--system` scope, N-03 = a packet path-naming nit already applied.
- `P027_OPSA_CI_20260915/GEMINI/LEAD_ADJUDICATION.md:3,5`: a Gemini detection read of **PR #194** ran at 20:25-20:27Z — **COUNTED, PASS, 0 findings**; `:5` records that the gap was found by a 20:25Z self-audit and that the morning wording implying otherwise was corrected.

I reached every finding below from the bytes and the API before reading either adjudication. My conclusions agree with Gemini's two NITs on #193 and add three more; on #194 I raise two NITs where Gemini raised none.

---

## Findings

Severity key: **REQUIRED** = the PR must change before merge; **NIT** = record it, merge is not blocked.

### PR #193

**F-01 — NIT — `research-gates.yml:169-170`: Ruff installed by version pin, without `--require-hashes`.**
`python -m pip install ruff==0.16.4` sits eleven lines below `python -m pip install --require-hashes -r IBKR_PAPER_BRIDGE/requirements.lock` (`:160-163`), so the file applies two different standards to two installs in one job. (This is Gemini's F-01 / N-01.)

I judged whether it is REQUIRED and concluded **NIT**, for four reasons, each checkable:

1. **No policy line requires it.** I read all 189 lines of `CI_POLICY.md`. The only `--require-hashes` sentence is `CI_POLICY.md:42`, and it sits inside `## Day-one check` (`:34-44`), whose lead sentence is "Its single day-one check is named `Bridge suite (Python 3.12)` and does the following:" — a numbered description of `ci.yml`'s five steps, not a repo-wide rule. Nothing in `## Progressive required-check policy` (`:105-117`) or `## Future jobs` (`:167-183`) imposes a hash requirement on a new job. I therefore do not claim a policy line, per the brief's instruction.
2. **Blast radius is small and bounded.** The job carries workflow-level `permissions: contents: read` (`:29-30`), uses no secret, checks out with `persist-credentials: false` (`:152-153`), and produces a context that is not in ruleset 21444962. A hostile `ruff` wheel would execute on an ephemeral GitHub-hosted runner holding a read-only token — it could not write to the repository nor satisfy a required check.
3. **Ordering already protects the tested environment.** The Ruff install (`:169-170`) runs *after* the contracts tests (`:165-167`), so it cannot influence the test result it shares a job with.
4. **It did not perturb the locked closure in practice.** GREEN job log `104362756214`: `Collecting ruff==0.16.4` → `Installing collected packages: ruff` → `Successfully installed ruff-0.16.4`. Exactly one package; the hash-locked closure installed above it was untouched.

**This NIT converts to REQUIRED the moment `Contracts tests and Ruff (Python 3.12)` is proposed for ruleset 21444962**, because then an unpinned artifact would gate merges into `master`. The exact change for that day: replace `:170` with a hashed install — e.g. a `MTC_COMMAND_CENTER/contracts/ruff.lock` containing `ruff==0.16.4` plus its `--hash=sha256:…` lines, installed as `python -m pip install --require-hashes -r MTC_COMMAND_CENTER/contracts/ruff.lock`. No change is needed to merge this PR as an informational job.

**F-02 — NIT — `research-gates.yml:114-115`: `git config --system core.longpaths true` uses system scope.**
(Gemini F-02 / N-02.) Correct and harmless as written: `runs-on: windows-2025` (`:106`) is a GitHub-hosted, single-use VM, so the mutation dies with the runner, and the GREEN run proves it works. The step must run before `actions/checkout` (it does, `:117`), and `--global` is not a reliable substitute because the checkout action's git invocations do not all run under the same HOME.
Named trigger for re-review: **if this job is ever moved to a self-hosted runner, `--system` becomes a persistent host mutation.** That move is already forbidden — reconciliation R17 ("no self-hosted runner, no scheduled jobs") is recorded VERIFIED in `P027_ACCEPTANCE_PACKET_20260915.md:38` and is an accepted day-one row — so this is a note, not an action.

**F-03 — NIT — `research-gates.yml:160-163`: the contracts tests take their dependencies from another package's lock file.**
`MTC_COMMAND_CENTER/contracts/pyproject.toml` declares its own pins — `dependencies = ["pydantic==2.13.4"]` and `[project.optional-dependencies] test = ["pytest==9.1.1", "ruff==0.16.4"]` — but the job installs `IBKR_PAPER_BRIDGE/requirements.lock`, a file owned by a different package, and never installs the contracts' own extra.
Today they agree: the lock carries `pydantic==2.13.4` (`requirements.lock:846`) and `pytest==9.1.1` (`:986`), matching the contracts' pins exactly. The hazard is drift: **a future Bridge-side bump silently changes the pydantic the contracts tests run against, while the contracts package's own declared pin does not move** — at which point a green `Contracts tests and Ruff` stops being a statement about the contracts' declared environment.
This is not hypothetical — the two files have already drifted on a package where it does not matter: `packaging==26.2` in the lock (`:791`) vs `packaging==26.3` in `contracts/constraints.txt`. Fix (backlog, not for this PR): give `contracts/` a hashed lock of its own and install that.
Side note, verified: `mtc-contracts` is **not** in the Bridge lock (grep: 0 hits), and `python -m pytest` puts the CWD first on `sys.path`, so the tests exercise the working tree, not an installed copy. That part is correct as written.

**F-04 — NIT — actions pinned by tag, not SHA (`:46,51,118,123,151,156`).**
Not a defect against the stated bar: `ci.yml:27,32` and `pine-defang-guard.yml:15,16` use the same tags, and no repo workflow SHA-pins. Consistency is met and no policy line demands more (see F-01 reason 1), so I do **not** raise this as REQUIRED.
Recorded because the GREEN run surfaced the live consequence — job log `104362756214`: `##[warning]Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@v4, actions/setup-python@v5`. Tag pinning is what lets GitHub carry the repo through that transition automatically; a SHA pin would trade that for supply-chain immutability. If the repo ever SHA-pins, do it as one sweep across all four workflow files, not inside this PR.

**F-05 — NIT — interaction with the red-master rule (applies to BOTH PRs).**
`research-gates.yml:25-27` and `opsa-tests.yml:17-19` both add jobs that run on `push: branches: [master]`. `CI_POLICY.md:119-126` ("Red-master rule") says: "`master` must never stay red. A failed push run is an immediate incident: stop unrelated merges and direct pushes, inspect the first failing check…". That text was written when the only push-triggered failure mode was the required Bridge suite. After these merges, a transient Windows-runner or checkout failure in an **informational** job produces a failed push run on `master` that, read literally, triggers the incident procedure.
The workflow bytes are not wrong; the policy text needs one clarifying sentence distinguishing a red required check (incident) from a red informational job (investigate, does not stop merges). That is a documentary edit (T2/T3), not a change to either PR, and it does not block either merge.

### PR #194

**F-06 — NIT — `opsa-tests.yml:55`: `python -m unittest test_opsa -v` names one module, so a new test file would be silently skipped.**
Correct today: the tree at `63b7bbe0` contains exactly one test file under `MTC_COMMAND_CENTER/tools/opsa/` (`test_opsa.py`), so nothing is missed now, and the GREEN run's `Ran 33 tests` matches the 33 `def test_` methods in the file.
The concrete future case is already named in the project's own record: `P027_OPSA_CI_EVIDENCE_20260915.md:15` says the WP-P0-26 candidate `d81b07f6` carries **39** tests. If that repair lands as an additional module rather than as edits to `test_opsa.py`, this job keeps reporting green over the old 33 with no signal that the new file exists. `python -m unittest discover -v` (working directory unchanged) removes that failure mode. Not a merge blocker.

**F-07 — NIT — `opsa-tests.yml:39-40`: `--system` scope for `core.longpaths`.**
Identical to **F-02**, same disposition, same trigger condition. Correct on `windows-2025` (`:31`), which the GREEN run confirms.

### Records (both packages)

**F-08 — NIT — `RED_DEMO_EVIDENCE_20260915.md:7` carries an uncorrected false claim.**
The line asserts "no `failure` conclusion existed in the last 200 CI runs before today". My live query contradicts it: `ci.yml` on `master` has exactly one failure ever, `32846169952` @ `110305c0`, 2026-08-25T12:10:43Z. The Lead already found and corrected this in `P027_ACCEPTANCE_PACKET_20260915.md:60` (§5.1), which explicitly designates the packet as the erratum and leaves the source file "as written". That is a defensible bookkeeping choice, but it leaves a false sentence in a live evidence file that a later reader may cite without the packet beside it.
Fix: one erratum line appended to `RED_DEMO_EVIDENCE_20260915.md` pointing at packet §5.1. Documentary; blocks nothing.

**F-09 — NIT — `CI_POLICY.md:107-111` contradicts `CI_POLICY.md:19-20` and the live ruleset.**
`:107-111` still reads "Only `Bridge suite (Python 3.12)` is in rule 21444962's required list" and that `pine-alert-guard` "is **not** required — that is this policy operating as designed, not an oversight." The live ruleset requires **both** contexts, and the same file's own acceptance paragraph at `:19-20` says two. The acceptance packet notices the history (`:16`: "…was recorded as NOT required on 2026-08-25 (`CI_POLICY.md`) … and is required now") but the policy section was never updated.
This matters beyond tidiness: `CI_POLICY.md:7` declares the "Live `master` protection" section "the authority on this page", and §Progressive sits *outside* it while making a contrary factual claim about the same ruleset. Fix: correct `:107-111` to name both required contexts. Documentary; blocks neither PR.

**Count: 0 REQUIRED across both PRs. 5 NITs on #193 (F-01…F-05), 2 on #194 (F-06, F-07, plus F-05 which it shares), 2 records NITs (F-08, F-09).**

---

## 6. Merge order and conflicts

```
git -c safe.directory=* -C C:/tmp/P027_CI_20260915      diff fcac0ac6 a3325836 --stat -- .github/workflows
 .github/workflows/research-gates.yml | 85 +++++++++++++++++++++++++++++++++++-

git -c safe.directory=* -C C:/tmp/P027_OPSA_CI_20260915 diff fcac0ac6 63b7bbe0 --stat -- .github/workflows
 .github/workflows/opsa-tests.yml | 55 ++++++++++++++++++++++++++++++++++++++++
```

**They touch different files** from the same base `fcac0ac6`. There is no textual conflict in either order, and no semantic one either: the workflows share no job id, no check-context name, and no concurrency group (`research-gates-…` at `:33` vs `opsa-tests-…` at `:25`).

One real ordering consequence, from the ruleset: `strict_required_status_checks_policy: true` requires the head to be up to date with `master`. Whichever PR merges second must be updated onto the new `master` first, which re-runs its checks. Both are `MERGEABLE` / `CLEAN` right now, so this costs one "Update branch" click and one check cycle.

**Recommended order: #193, then #194.** The reason is signal, not safety. Once #193 is on `master`, updating #194's branch makes its pre-merge run include the three `Research gates` jobs — so #194's own head gets checked by the P0-30 checkers, the contracts tests and the Ruff lint before it merges, at no extra cost. The reverse order is safe and conflicts nowhere; it just buys less. Merging only one of the two is also fine — neither depends on the other.

After either merge, re-read the ruleset once (`gh api repos/bsemaay-tech/mtc-command-center/rulesets/21444962`) and confirm the required list is still exactly two contexts; the merge itself must not add one.

---

## NOT VERIFIED

Named, non-empty, and honest about what a read-only reviewer cannot establish.

1. **I executed neither workflow.** I ran no workflow, re-ran no run, pushed nothing, and made no write of any kind to GitHub. Every runtime statement in this report rests on GitHub's recorded run/job/log API for four runs (`34963602576`, `34961383292`, `34983809921`, `34983897746`) and their job logs. I did not verify that a *future* run reproduces them.
2. **The Ruff "other surfaces are not clean" counts** — 3 findings at the repo root, 21 under `IBKR_PAPER_BRIDGE`, 69 under `03_QUANTLENS/tools` (`research-gates.yml:140-141`, `P027_CI_ADDITIONS_EVIDENCE_20260915.md:14`) — are **NOT VERIFIED**. I did not install or run Ruff. What I did verify is that the claim's *consequence* holds: the job lints only `MTC_COMMAND_CENTER/tools/opsa` and `MTC_COMMAND_CENTER/contracts` (`:175`), and that run was green.
3. **pip's hash enforcement over the whole lock is NOT VERIFIED by execution.** I confirmed the file's shape by reading it (56 `name==version` lines, each continued into `--hash=sha256:…` lines) but I did not run pip; that `--require-hashes` covers every one of the 56 is inferred from the step succeeding, not proved by me.
4. **For PR #193, that a *test* failure (as opposed to a checkout failure) turns the job red is NOT demonstrated.** Run `34961383292` failed at `Check out repository`, with all three checker steps `skipped`. The structural argument is verified from the bytes — no `continue-on-error` on `:127-134`, and the two unittest-based checkers end in `unittest.main(verbosity=2)` (`check_p030_opsa_heartbeat_adapter.py:249`, `check_p030_closed_partition_backup_adapter.py:1792`) while the third ends in bare `assert` / `raise AssertionError` under `main()` (`check_p030_market_data_contracts.py:1247-1248`), all of which exit non-zero — but no run demonstrates it. PR #194 *does* demonstrate it with a real test failure, which is the stronger evidence of the two packages.
5. **No failure-notification artifact exists for either new job.** The packet's e-mail evidence (`E5`, Gmail id `1a0a4d879a3c386d`) is for `ci.yml`/run `34961383292`. Whether a red `OPS-A tests` or `P0-30 checkers` push run on `master` reaches the owner's inbox is untested.
6. **Fork-PR behaviour is untested.** The repository is public (`gh api repos/… --jq .private` → `false`), so `pull_request` runs from forks are possible; no such run exists for either workflow. Both use `pull_request` (not `pull_request_target`) with `contents: read` and no secrets, which is the safe shape — but it is unexercised.
7. **My ruleset read is a point-in-time read (2026-09-16).** I cannot rule out a change between this verdict and the merge. Re-read `rulesets/21444962` immediately before merging.
8. **The GitHub audit log for the 2026-08-29 ruleset update** that added `pine-alert-guard` was not queried (the acceptance packet at `:16` records the same gap). So *when and by whom* the second required context was added is inferred from `updated_at`, not established.
9. **I did not re-run the R19 no-continuous-protection sweep** (`P027_ACCEPTANCE_PACKET_20260915.md:87`). It is outside this T1's object — the sweep belongs to the day-one acceptance, which the owner already made — but its result is therefore not independently confirmed here.
10. **Byte-level review of the checker scripts was targeted, not exhaustive.** I read the entry points, exit semantics, network fence and the `mklink /J` block of the three P0-30 checkers and the header/imports of `test_opsa.py`; I did not audit those ~3,400 lines line by line. They are merged code on `master`'s lineage, not this PR's object — this PR only wires them into CI.

---

## Appendix A — what each new job actually does (for the record)

**PR #193 adds two jobs to an existing workflow:**

- `p030-checkers` / **`P0-30 checkers (Python 3.12, Windows)`** — `windows-2025`, 15-min timeout. Long-paths → checkout → Python 3.12 → three repo-root checkers. Windows is load-bearing, not incidental: `check_p030_closed_partition_backup_adapter.py:265-266` shells out to `cmd /c mklink /J` to build a real NTFS junction and then asserts the backup adapter refuses a junction ancestor (`:272` uses `Path.is_junction()`, Python 3.12+). Observed: `PASS`, `Ran 10 tests … OK`, `Ran 44 tests … OK`; wall time 40 s against a 15-min timeout.
- `contracts-and-lint` / **`Contracts tests and Ruff (Python 3.12)`** — `ubuntu-24.04`, 10-min timeout. Hash-locked install → 50 contracts tests → Ruff `--select E9,F821,F811,F401,F841` over two directories. Observed: `50 passed in 0.32s`, `All checks passed!`; wall time 27 s.

**PR #194 adds one workflow with one job:**

- `opsa-tests` / **`OPS-A tests (Python 3.12, Windows)`** — `windows-2025`, 10-min timeout, installs nothing. Long-paths → checkout → Python 3.12 → `python -m unittest test_opsa -v` in `MTC_COMMAND_CENTER/tools/opsa`. Observed: `Ran 33 tests in 1.471s` / `OK`; wall time 30 s (checkout 20 s of it).

All three timeouts have >20× headroom over observed wall time, so none is a flakiness risk.

## Appendix B — every `gh` call made in this review (all GET / read-only)

| # | Command | Result (condensed; full outputs quoted in the body where they carry a finding) |
|---|---|---|
| 1-2 | `gh pr view 193 --repo … --json …,merged` and the same for 194 | **ERROR, exit 1**: `Unknown JSON field: "merged"` + the field list. No state touched; re-issued as #3/#4 with `mergedAt`/`mergeCommit`. Recorded because the brief requires every call. |
| 3 | `gh pr view 193 --repo bsemaay-tech/mtc-command-center --json number,state,headRefName,headRefOid,baseRefName,baseRefOid,mergeable,mergeStateStatus,isDraft,author,title,url,mergedAt,mergeCommit,files,reviewDecision,latestReviews` | `OPEN`, head `a33258367739400017c11a7e498030238f9b1564`, base `fcac0ac67cf2682693ad28138b1a56e15a0846f2`, `MERGEABLE`/`CLEAN`, `mergedAt: null`, `mergeCommit: null`, `latestReviews: []`, files = one `MODIFIED` `.github/workflows/research-gates.yml` +84/-1, author `bsemaay-tech` |
| 4 | same for PR 194 | `OPEN`, head `63b7bbe0981bddafb94018a3520f3c5c82e8e4f4`, base `fcac0ac6…`, `MERGEABLE`/`CLEAN`, `mergedAt: null`, `latestReviews: []`, files = one `ADDED` `.github/workflows/opsa-tests.yml` +55/-0 |
| 5 | `gh api -X GET repos/…/actions/runs/34963602576 --jq '{…}'` | `conclusion: success`, `event: pull_request`, `head_sha: a3325836…`, `name: Research gates`, `created_at 2026-09-15T11:29:59Z` |
| 6 | `gh api -X GET repos/…/actions/runs/34963602576/jobs` | 3 jobs, all `success`: `Research gate checkers (Python 3.12)` [ubuntu-24.04], `Contracts tests and Ruff (Python 3.12)` [ubuntu-24.04], `P0-30 checkers (Python 3.12, Windows)` [windows-2025]; runner names `GitHub Actions 10000008{38,39,40}` |
| 7 | `gh api -X GET repos/…/actions/runs/34961383292` | `conclusion: failure`, `head_sha: 55ab90b892ae3ecab036ff1701cb3d8bfbf95305`, `name: Research gates` |
| 8 | `gh api -X GET repos/…/actions/runs/34961383292/jobs` (with per-step conclusions) | `Contracts tests and Ruff`: success (all 7 steps). `Research gate checkers`: success. **`P0-30 checkers (Python 3.12, Windows)`: failure — `Check out repository` failure, the three checker steps `skipped`** |
| 9 | same, `--jq` for the failing job id | `104355519781` |
| 10 | `gh api -X GET repos/…/actions/jobs/104355519781/logs` (grepped) | line 118: `##[error]error: unable to create file MTC_COMMAND_CENTER/03_QUANTLENS/research/restart_transcript_intake_audit_2026_05_04_CODEX_20260504_175614/corrected_intakes/CORRECTED_…md: Filename too long` (+3 more of the same shape) |
| 11 | `gh api -X GET repos/…/actions/runs/34983809921` | `conclusion: success`, `head_sha: 63b7bbe0…`, `name: OPS-A tests` |
| 12 | `gh api -X GET repos/…/actions/runs/34983809921/jobs` | one job `OPS-A tests (Python 3.12, Windows)` [windows-2025] `success`; steps: Set up job / **Enable long paths for the checkout** / Check out repository / Set up Python 3.12 / OPS-A unit tests — all success |
| 13 | `gh api -X GET repos/…/actions/runs/34983897746` | `conclusion: failure`, `head_branch: demo/opsa-tests-red-20260915`, `head_sha: e9314079865ce5c9267d6e7b1437f40f0d79f073` |
| 14 | `gh api -X GET repos/…/actions/runs/34983897746/jobs` | job `104430937775`, `failure`, **`OPS-A unit tests` failure**, `Post Set up Python 3.12` skipped |
| 15 | `gh pr view 195 --repo … --json number,state,headRefName,headRefOid,mergedAt,closed,closedAt,title,files` | `state: CLOSED`, `closed: true`, `closedAt: 2026-09-15T14:47:47Z`, **`mergedAt: null`**, title `DEMO (never merge): WP-P0-27 D026 red probe…`, files = `opsa-tests.yml` (+55) and `test_opsa.py` (+5) |
| 16 | `gh api -X GET repos/…/actions/runs/34983809921/jobs --jq '.jobs[].id'` | `104430634198` |
| 17 | `gh api -X GET repos/…/actions/jobs/104430634198/logs` (grepped ×2) | `Ran 33 tests in 1.471s`, `OK` |
| 18 | `gh api -X GET repos/…/actions/jobs/104430937775/logs` (grepped ×2) | `AssertionError: deliberate WP-P0-27 D026 red probe for the OPS-A tests workflow (2026-09-15); never merged`; `Ran 34 tests in 0.985s`; `FAILED (failures=1)`; `##[error]Process completed with exit code 1.` |
| 19 | `gh api -X GET "repos/…/contents/.github/workflows/opsa-tests.yml?ref=e9314079…" --jq .sha` | `3e4643445d7b5bca40289af82daa74fb48996b6b` — identical to #194's head blob |
| 20 | `gh api -X GET "repos/…/contents/.github/workflows/research-gates.yml?ref=a3325836…" --jq .sha` | `609de49aa9f3db635ba9ed57753028c262148fb7` — identical to the local blob |
| 21 | `gh pr view 193 --json statusCheckRollup` | `Bridge suite (Python 3.12)` SUCCESS, `pine-alert-guard` SUCCESS ×2, `Research gate checkers (Python 3.12)` SUCCESS, `P0-30 checkers (Python 3.12, Windows)` SUCCESS, `Contracts tests and Ruff (Python 3.12)` SUCCESS, `Vercel Preview Comments` SUCCESS. (`isRequired` came back `null` for every row — gh does not populate it here; the ruleset in #23 is the authority on what is required.) |
| 22 | `gh pr view 194 --json statusCheckRollup` | `Bridge suite (Python 3.12)` SUCCESS, `OPS-A tests (Python 3.12, Windows)` SUCCESS, `pine-alert-guard` SUCCESS ×2, `Research gate checkers (Python 3.12)` SUCCESS, `Vercel Preview Comments` SUCCESS |
| 23 | `gh api -X GET repos/bsemaay-tech/mtc-command-center/rulesets/21444962` | `enforcement: active`; `conditions.ref_name.include: ["~DEFAULT_BRANCH"]`, `exclude: []`; rules `deletion`, `non_fast_forward`, `required_status_checks` with `strict_required_status_checks_policy: true`, `do_not_enforce_on_create: false`, contexts **exactly** `Bridge suite (Python 3.12)` and `pine-alert-guard` (`integration_id: 15368`); `bypass_actors: []`; `current_user_can_bypass: "never"`; `created_at 2026-08-25T18:24:47.194+03:00`, `updated_at 2026-08-29T11:25:28.137+03:00` |
| 24 | `gh api -X GET repos/…/rulesets` | exactly one ruleset: `21444962 "Protect master – required CI"`, branch, active |
| 25 | `gh api -X GET repos/bsemaay-tech/mtc-command-center` | `private: false`, `visibility: public`, `default_branch: master`, all three merge methods allowed |
| 26 | `gh api -X GET "repos/…/actions/workflows/ci.yml/runs?branch=master&per_page=100"` | `{"total":61,"conclusions":{"failure":1,"success":60}}` |
| 27 | `gh api -X GET "repos/…/actions/workflows/ci.yml/runs?branch=master&per_page=100&status=failure"` | exactly one: `{"id":32846169952,"head_sha":"110305c0790b2451cb13ded914d27e89609c35d5","created_at":"2026-08-25T12:10:43Z","conclusion":"failure"}` |
| 28 | `gh api -X GET repos/…/actions/runs/34963602576/jobs --jq ids+names` | `104362755841` checkers, `104362756214` contracts+ruff, `104362756252` p030 windows |
| 29 | `gh api -X GET repos/…/actions/jobs/104362756214/logs` (grepped) | `50 passed in 0.32s`; `Collecting ruff==0.16.4` → `Successfully installed ruff-0.16.4`; `All checks passed!`; `##[warning]Node.js 20 is deprecated … actions/checkout@v4, actions/setup-python@v5 … forced to run on Node.js 24` |
| 30 | `gh api -X GET repos/…/actions/jobs/104362756252/logs` (grepped) | `… REFUSALS: PASS` ×7, `NETWORK ATTEMPTS: 0`, `P030 MARKET DATA CONTRACTS CHECK: PASS`, `Ran 10 tests in 0.064s / OK`, `Ran 44 tests in 4.482s / OK` |
| 31 | (not `gh`) `grep -rniE "block…\|required check\|cannot be merged" over both evidence dirs` | 6 hits, all correct — listed and adjudicated in item **4e** |

Git commands used, all read-only as the brief requires: `rev-parse HEAD` (×2), `rev-parse <rev>:<path>`, `show <rev>:<path>`, `ls-tree -r --name-only <rev>`, `diff <sha> <sha> [--stat] -- <paths>`. **No `git status`, no diff against a working tree, no `add`, no `commit`, no `checkout`, no `push` — in either worktree or anywhere else.**

---

VERDICT #193: PASS-WITH-NITS
VERDICT #194: PASS-WITH-NITS
T1 MERGE RECOMMENDATION: merge #193 first, then update #194's branch onto the new master and merge #194 — no required change to either PR; re-read ruleset 21444962 before each merge and confirm the required-check list is still exactly the two contexts.
