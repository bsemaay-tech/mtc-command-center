# RIC4 UFW trailing-comment repair report

Date: 2026-08-16  
Workspace: `C:\BRIDGE_RELEASE_INTEGRATION_20260815`  
Frozen HEAD: `acdf4e379fb60ee319854acae19fd3eaf7db71a2`  
Audit tier: **T0** (host-facing deployment safety predicate)

## Outcome

The bounded repair is implemented in the worktree and all local functional checks pass. It is **not T0-accepted** because the final required Claude confirmation timed out in audit round 3 of 3. Codex returned final Gate 5 PASS and Gate 6 PASS; no final-round Claude verdict was produced. Repository policy forbids a fourth audit round, so this report records a concrete audit-transport blocker rather than claiming dual-review closure.

No host or network was contacted. No installation, service, firewall mutation, rebuild, re-pin, commit, checkout, reset, stash, push, or other Git mutation was performed.

## Worktree edits

Only the authorized files differ from HEAD:

- `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh`
  - Immediately after each raw UFW rule is copied to `rule`, strips exactly one trailing `[[:space:]]+#[^\n]*$` comment.
  - Both the structured parser and independent substring backstop use the stripped `rule`.
  - The backstop still scans the complete non-comment rule text, including real port fields, so an exposed `8790/tcp` remains rejected.
- `IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py`
  - Adds the exact live IPv4/IPv6 `# SSH` pair.
  - Adds commented 8790, unknown-verb, and named-profile fail-closed cases.
  - Pins the three negative cases to their required post-normalization diagnostics and proves the stripped comment is absent from the diagnostic.
  - Adds `comment_mentions_bridge_port`, which is the discriminating fence for the backstop normalization line.

Final hashes:

```text
git blob 044cf0f83d5b266e44df4442ea30a22c9397f71d  IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh
sha256  73e42d6f63698ce6f2bc6813f02d34eba4b526124967678130f89ceecbba6e6e  IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh
git blob 55acafc785364b49eb35d9812f93deb0082f386c  IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py
sha256  def892e804396d276a457583984da781e016a8129a40ff1a17aa7144ff98d5b8  IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py
```

## Required RED before repair

The pristine function was sourced directly from HEAD and given the exact live fixture through a mocked local `ufw` function:

```powershell
$script = @'
ufw() {
  printf '%s\n' \
    'Status: active' \
    'Logging: on (low)' \
    'Default: deny (incoming), allow (outgoing), disabled (routed)' \
    'To                         Action      From' \
    '--                         ------      ----' \
    '22/tcp                     ALLOW IN    Anywhere                   # SSH' \
    '22/tcp (v6)                ALLOW IN    Anywhere (v6)              # SSH'
}
. <(git show HEAD:IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh)
MTC_FAILURES=0
assert_ufw_bridge_safe
rc=$?
printf 'PREFX_LIVE_COMMENT_FIXTURE_RC=%s\n' "$rc"
'@
& 'C:\Program Files\Git\bin\bash.exe' -c $script
```

Real output:

```text
FAIL  ufw has an unmodelled inbound rule or application profile; enumerate it as an explicit numeric port/range before Bridge verification: UNMODELLED source field is not an explicit address 22/tcp ... Anywhere # SSH UNMODELLED source field is not an explicit address 22/tcp (v6) ... Anywhere (v6) # SSH
PREFX_LIVE_COMMENT_FIXTURE_RC=1
```

The same exact live fixture on repaired bytes produced:

```text
PASS  ufw active, default-deny incoming; SSH port 22 allowed; Bridge port 8790 not exposed
POSTFIX_LIVE_COMMENT_FIXTURE_RC=0
```

## D026 falsification evidence

### Strengthened negative assertions versus pristine HEAD

Pristine HEAD produced rc 1 for all three cases, but for the pre-repair/wrong diagnostic paths shown below. The strengthened committed assertions are RED on these outputs and GREEN on repaired bytes.

```text
PREFX_BRIDGE_RC=1
FAIL ... source field is not an explicit address ... 8790/tcp ALLOW IN Anywhere # temporary

PREFX_UNKNOWN_RC=1
FAIL ... rule action/direction is not a modelled inbound UFW status verb ... 22/tcp WEIRD IN Anywhere # x

PREFX_NAMED_RC=1
FAIL ... source field is not an explicit address ... OpenSSH ALLOW IN Anywhere # SSH
```

Candidate outputs are instead pinned to:

```text
commented_bridge_port_exposed: ufw exposes Bridge port 8790
commented_unknown_verb: rule action/direction is not a modelled inbound UFW status verb
commented_named_profile: port field is not an explicit numeric port/range
```

For all three, the committed test also asserts that ` #` is absent from stderr, proving the diagnostic row was comment-stripped.

### Backstop-only mutation

The candidate was executed normally and through an in-memory/process-substitution mutation that removes only line 311, the backstop `sub()` call:

```bash
. "$1"                         # candidate
. <(sed '311d' "$1")          # equivalent mutation: backstop strip removed only
```

Fixture:

```text
22/tcp ALLOW IN Anywhere # was 8790 before
```

Real output:

```text
BACKSTOP_CANDIDATE_RC=0
PASS  ufw active, default-deny incoming; SSH port 22 allowed; Bridge port 8790 not exposed

BACKSTOP_MUTANT_RC=1
FAIL  ufw inbound substring backstop found Bridge port 8790: 22/tcp ALLOW IN Anywhere # was 8790 before
```

Thus the added `comment_mentions_bridge_port` test is RED when only the backstop normalization is removed and GREEN on the candidate.

## GREEN validation

Focused parameter arm and shell syntax:

```powershell
$env:PYTHONUTF8='1'
python -m pytest -v -p no:cacheprovider 'IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py::test_ufw_bridge_safe_invariant_is_multi_tenant_and_fail_closed'
& 'C:\Program Files\Git\bin\bash.exe' -n 'C:/BRIDGE_RELEASE_INTEGRATION_20260815/IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh'
```

Real output summary:

```text
collected 16 items
16 passed in 7.39s
FOCUSED_RC=0 BASH_N_RC=0
```

All requested named cases passed, including:

```text
live_commented_ssh_pair PASSED
commented_bridge_port_exposed PASSED
commented_unknown_verb PASSED
commented_named_profile PASSED
comment_mentions_bridge_port PASSED
```

Exact full suite from repository root:

```powershell
$env:PYTHONUTF8='1'
python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests
```

Real output summary:

```text
1381 passed, 1 warning in 162.15s (0:02:42)
```

The single warning is the pre-existing Starlette/httpx deprecation warning from site-packages. There were zero failures.

Diff validation:

```powershell
git status --short --untracked-files=all
git diff --stat
git diff --numstat
git diff --check
```

Real output:

```text
 M IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh
 M IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py
 IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh     | 16 ++++++--
 IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py | 47 ++++++++++++++++++++++++
 2 files changed, 60 insertions(+), 3 deletions(-)
13  3  IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh
47  0  IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py
git diff --check: rc 0, no findings
```

## T0 audit record

| Round | Claude Opus 5 xhigh | Codex gpt-5.6-sol xhigh | Result |
|---|---|---|---|
| 1 | Transport timeout; no verdict | Output lost in combined transport timeout; no usable verdict | BLOCK; candidate unchanged |
| 2 | REQUEST_CHANGES | REQUEST_CHANGES | Reproduced D026 gaps; test-only repair applied |
| 3 | Transport timeout; no verdict | Gate 5 PASS; Gate 6 PASS; no required repairs | BLOCK at T0 round cap |

Round-2 required findings were repaired and independently reproduced as closed. Round-3 Codex confirmed no findings, the production blob frozen, all prior fences discriminating, exact two-file scope, and no auditor edits. However, acceptance requires both flagship confirmations. Claude round 3 produced no verdict before the bounded transport expired, and the maximum of three T0 rounds is exhausted.

## Final status / blocker

- Worktree repair: **implemented and locally GREEN**.
- Codex final confirmation: **PASS / PASS**.
- Required Claude final confirmation: **missing due transport timeout**.
- T0 acceptance: **BLOCKED at round cap; do not claim accepted**.
- Installation continuation, host contact, rebuild/re-pin, and any Git sequencing remain unauthorized and were not performed.

