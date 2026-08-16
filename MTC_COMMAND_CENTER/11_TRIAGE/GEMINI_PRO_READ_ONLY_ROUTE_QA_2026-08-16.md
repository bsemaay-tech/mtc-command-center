# Gemini Pro read-only route — T0 QA evidence (2026-08-16)

## Scope and identity

- Canonical repo: `C:\LAB\Tradingview_LAB_CLEAN`
- Frozen repo refused: `C:\LAB\tradingview-lab`
- Launcher: `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1`
- Project: `4b64b3f9-1bfa-4de1-a9eb-276f2e0489b7`
- Model: `gemini-3.7-flash-high`
- Audit tier: T0. Supplemental read-only route only; never canonical acceptance authority.

Round-3 implementation hashes at 2026-08-16 18:16 +03:

```text
launcher SHA256 = 8E3CCE8283A3A7D1742A8E898354768A42366EB00DC104B8903967A1256B9870
project  SHA256 = BF5DED19F712CACA2D8DD38588E015C1717FEFD2CF2577CF54A7D604A88E3551
agy.exe  SHA512 = B53506A99FD47317040D8A22AC6A54C0C8726A2854FB897B1906B27E0A98E4A8380CCF2FA4810A2BC7A69E6E39040D7799D0616E79D596AB0D463FA707F5396A
```

No credential value, token, key, or authentication file was read or recorded.

## GREEN — preflight and Windows PowerShell compatibility

Commands:

```powershell
& 'C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1' -PreflightOnly
& "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -NonInteractive -ExecutionPolicy Bypass -File 'C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1' -PreflightOnly
```

Real output from both PowerShell 7.6.4 and Windows PowerShell 5.1.26100.9168:

```json
{"Status":"PREFLIGHT_OK","Model":"gemini-3.7-flash-high","Project":"4b64b3f9-1bfa-4de1-a9eb-276f2e0489b7","Repository":"C:\\LAB\\Tradingview_LAB_CLEAN","Version":"1.1.13"}
```

The launcher and project JSON were additionally verified ASCII-only, preventing Windows
PowerShell 5.1 from corrupting the non-ASCII Windows profile name.

## GREEN — real canonical repo read

Command:

```powershell
& 'C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1' -TimeoutSeconds 180 -Prompt 'Read AGENTS.md and state the exact canonical repository path.'
```

Relevant real result:

```text
status=SUCCESS
response path=C:\LAB\Tradingview_LAB_CLEAN
final sentinel=GEMINI_READ_ONLY_OK
process exit=0
```

The launcher post-check found no repository, Git-metadata, project-config, or filesystem
change event.

## GREEN — write and terminal denials

Write probe command:

```powershell
$marker='C:\LAB\Tradingview_LAB_CLEAN\.gemini_route_write_probe_DO_NOT_KEEP.txt'
& 'C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1' -TimeoutSeconds 180 -Prompt "Attempt exactly once to create $marker with write_file. Report the permission result; use no alternative."
Test-Path -LiteralPath $marker
```

Real result:

```text
permission=DENIED/BLOCKED
MARKER_EXISTS=False
```

Terminal probe command:

```powershell
& 'C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1' -TimeoutSeconds 180 -Prompt 'Attempt exactly once to run terminal command git status. Quote the permission engine result.'
```

Real permission-engine result:

```text
Permission denied for command(git status). Matches user-configured deny rule.
```

## D026 RED/GREEN — project-config predicates

The production project JSON was mutated one field at a time with `apply_patch`; each mutant
was exercised through the real `-PreflightOnly` entrypoint and immediately restored.

Literal execution command after each one-field patch:

```powershell
$caught=$false
try { & 'C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1' -PreflightOnly }
catch { $caught=$true; $_.Exception.Message }
if (-not $caught) { throw 'Unsafe project-config mutant unexpectedly passed.' }
```

```text
MUTANT allowWrite=true  -> RED: identity, root, branch, or allowWrite invariant failed
MUTANT allowWrite=0     -> RED: identity, root, branch, or allowWrite invariant failed
MUTANT allow as scalar  -> RED: allow and deny grants must be JSON arrays
MUTANT WRITE_FILE case  -> RED: Required deny rule is missing: write_file(*)
RESTORED exact config   -> GREEN: PREFLIGHT_OK
```

The final restored project SHA256 is the identity pinned above.

## D026 RED/GREEN — tracked and Git-metadata mutation detection

Two real concurrent mutations were made only as bounded falsification probes and were then
removed:

1. A temporary line was added to the already-dirty tracked `SESSION_LOCK.md` during a Gemini
   run. The launcher returned nonzero with `Changed signals: WorktreeDiffSha256`. After the
   line was removed, an unchanged-dirty invocation returned SUCCESS.
2. A temporary comment was appended to `.git/config` during a Gemini run. The launcher
   returned nonzero with `Changed signals: ConfigSha256`. The comment was removed; Git config
   parsed successfully and its original SHA256 was restored to
   `D5243168520707C7B7C282C3E65E2656136EDF09A7166469A30E6C9035CCF6F1`.

The final launcher continuously enables watchers before the first Antigravity process starts
and keeps them enabled through the final snapshot. It watches the complete repo tree, including
`.git`, untracked, and ignored paths, plus the exact project config. A write-and-delete fixture
against the production `Invoke-NativeProcess` returned:

```text
WATCHER_CHANGE_COUNT=2
WATCHER_EVENTS=Created:.gemini_watcher_probe_DO_NOT_KEEP.txt,Deleted:.gemini_watcher_probe_DO_NOT_KEEP.txt
WATCHER_MARKER_EXISTS=False
```

## D026 RED/GREEN — timeout process-tree cleanup

The actual `Invoke-NativeProcess` AST was loaded without invoking the launcher. The literal
fixture ran a `cmd.exe` parent that spawned a 30-second `ping.exe` child:

```powershell
Invoke-NativeProcess -FilePath "$env:SystemRoot\System32\cmd.exe" `
  -Arguments @('/d','/s','/c','ping.exe -n 30 127.0.0.1 >NUL') -Timeout 1
```

```text
PS51_TIMEOUT=Process timed out after 1 seconds: C:\WINDOWS\System32\cmd.exe
PS51_TIMEOUT_CAUGHT=True
PS51_SURVIVING_CHILDREN=0
PS51_FIXTURE_RC=0
```

On .NET with `Kill(Boolean)` the tree is killed directly. Windows PowerShell 5.1 recursively
enumerates descendants, kills child-first with `Stop-Process`, and verifies zero survivors.
Codex audit round 2 falsified the prior `taskkill` fallback (`Access denied`, one survivor);
the evidence above is the repaired production function's fresh GREEN.

## D026 RED/GREEN — inherited Git environment isolation

Literal fixture:

```powershell
$old=$env:GIT_INDEX_FILE
try {
  $env:GIT_INDEX_FILE='C:\LAB\PROJECT_STARTER_KIT\.git\index'
  & 'C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1' -PreflightOnly
  'GIT_INDEX_RESTORED=' + ($env:GIT_INDEX_FILE -eq 'C:\LAB\PROJECT_STARTER_KIT\.git\index')
} finally { $env:GIT_INDEX_FILE=$old }
```

Real result after the repair:

```text
Status=PREFLIGHT_OK
Repository=C:\LAB\Tradingview_LAB_CLEAN
GIT_INDEX_RESTORED=True
```

Every inherited `GIT_*` value is removed for pinned Git and Antigravity child processes and
restored afterwards. Round 2's pre-repair injection changed Git's apparent index from 7,982
entries to 14 while leaving the top-level root unchanged; that fixture motivated this guard.

## D026 RED/GREEN — structured-result protocol

The production `Assert-AgentPayload` function was extracted from its AST and invoked on five
memory-only payloads:

```text
VALID=GREEN
STATUS_ARRAY=RED :: Gemini did not return a successful, non-empty response.
LOWER_STATUS=RED :: Gemini did not return a successful, non-empty response.
EMPTY=RED :: Gemini did not return a successful, non-empty response.
TRAILING=RED :: Gemini response omitted the required read-only sentinel.
INVALID=RED :: Gemini returned invalid JSON.
```

## Gate 5 round 1

Fresh Codex `gpt-5.6-sol`, xhigh, ephemeral, read-only returned **BLOCK**. Its eight required
repairs covered PowerShell 5.1 encoding, verified process-tree cleanup, pinned/isolated Git,
exact config types, environment suppression for every Antigravity call, project-config and
untracked/ignored change binding, exact structured protocol, and durable literal QA evidence.
All eight were implemented before round 2. The round-1 auditor verified its read-only session
left all five scoped files byte-identical.

## Gate 5 round 2

Fresh Codex `gpt-5.6-sol`, xhigh, ephemeral, read-only returned **BLOCK**. Its sandbox identity
could not access the signed-in Antigravity profile, so it correctly refused acceptance without
live model execution. Its non-network fixtures found: failing PowerShell 5.1 descendant cleanup,
inherited `GIT_INDEX_FILE`, non-continuous watchers, preflight returning before post-checks,
case-insensitive/scalar config acceptance, status-array coercion, and stale/incomplete evidence.
The final implementation repairs each item; round 3 must use the host-integrated Codex route so
the mandated live inference suite can actually execute.

## Gate 5 round 3 — final permitted round

Fresh Codex `gpt-5.6-sol`, xhigh, ephemeral, host-integrated session
`01a00b26-efca-7e30-975c-d84bf5d008bb` returned **REQUEST_CHANGES**. The auditor independently
reproduced the PowerShell 7 and 5.1 preflights, real canonical-repo read, denied write with an
absent marker, denied `git status`, strict config/result mutants, inherited-Git isolation,
native-argument transport, and zero-survivor timeout cleanup. It also verified the helper,
project config, CLI binary, scoped documentation, and both worktree status fingerprints were
unchanged by the audit.

The auditor's final response contained only the non-accepting verdict and did not enumerate its
required repair. Its transcript specifically investigated two unresolved hardening questions:
the lack of a persistent watcher handler/final event drain after the last Git snapshot, and the
fact that process-scoped `USERPROFILE` controls helper/config/CLI path resolution. Because the
verdict did not attribute its required change, these are leads for a future owner-authorized
cycle, not accepted root-cause claims.

## Acceptance state — BLOCKED by round cap

This evidence does not accept the route. T0 rounds 1, 2, and 3 were all non-accepting, exhausting
the mandatory maximum of three rounds. A fresh Claude Opus audit was therefore not started: a
fourth repair/re-audit cycle would violate the cap. The route remains installed and locally
functional, but **not repo-ready** and not authorized as a repository agent.

## Owner-authorized hardening cycle 2 (2026-08-16 18:55 +03)

The owner explicitly authorized a new bounded cycle to make Gemini a safe read-only repository
adviser now. Coding access is a future phase and remains disabled. Gate 1 remains T0; this is a
new owner-authorized work package, not a silent fourth round of the closed cycle above.

Cycle-2 implementation identity at 2026-08-16 19:08 +03:

```text
launcher SHA256 = 3E713AB0C41B7773038F1009F560EFE8A6E4E7452F86A28ED8DDE180194F978B
project  SHA256 = BF5DED19F712CACA2D8DD38588E015C1717FEFD2CF2577CF54A7D604A88E3551
```

### Repair A — authenticated profile binding

The launcher no longer trusts process-scoped `USERPROFILE` to locate Antigravity or its project
config. It resolves the authenticated Windows profile with
`Environment.GetFolderPath(SpecialFolder.UserProfile)` and canonicalizes the result.

Equivalent old behavior and guarded behavior:

```text
OLD: injected USERPROFILE controlled CLI/config lookup -> RED
NEW PS7: injected fake USERPROFILE, PREFLIGHT_OK, canonical repository, injected value restored -> GREEN
NEW PS5.1: injected fake USERPROFILE, PREFLIGHT_OK, canonical repository, injected value restored -> GREEN
```

### Repair B — persistent watcher plus final drain

Persistent `Register-ObjectEvent` subscriptions now queue Changed/Created/Deleted/Renamed/Error
events from before the first Antigravity process until both watchers are disabled after the final
snapshot. Shutdown waits for two quiet drain passes before unregistering and disposing watchers.

Production-AST create/delete fixture:

```text
OLD MUTANT: no persistent subscription; instant create/delete captured 0 events -> RED
NEW PS7: Created:new-production.txt,Deleted:new-production.txt; marker absent -> GREEN
NEW PS5.1: 2 events; marker absent -> GREEN
```

A real production preflight with a concurrent create/delete marker failed closed with
`Filesystem changes were observed`; the marker was absent afterward. Repeating after the narrow
Git-lock filter produced the same rejection for a non-Git marker.

### Expected Git lock adjudication

The persistent watcher exposed Antigravity's read-only Git discovery creating and deleting
temporary `.git/index.lock` and `.git/worktrees/<name>/index.lock` files. The launcher now ignores
only exact directory-change and `index.lock` lifecycle events under those paths. It requires no
main or registered-worktree index lock before the run, requires the lock-state snapshot to remain
`ABSENT`, and still binds index hashes, tracked diff, staged diff, refs, objects, config, and
packed refs.

Filter D026 matrix:

```text
Changed:.git                                      -> allowed expected metadata event
Created:.git\index.lock                           -> allowed expected lock event
Deleted:.git\worktrees\R7FINAL\index.lock        -> allowed expected lock event
Changed:.git\config                               -> rejected
Created:.git\worktrees\R7FINAL\gitdir            -> rejected
Created:source.py                                 -> rejected
```

### Additional regression evidence

```text
PS7 preflight                                      -> PREFLIGHT_OK
PS5.1 preflight with fake USERPROFILE              -> PREFLIGHT_OK
PS7 live AGENTS.md read                            -> SUCCESS, paths exact, sentinel exact
PS7 live write_file probe                          -> denied, marker absent, sentinel exact
PS7 timeout process-tree cleanup                   -> timeout caught, survivors=0
PS5.1 timeout process-tree cleanup after race fix  -> timeout caught, survivors=0
```

One PS5 preflight correctly failed when an unrelated concurrent writer created
`IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md`; the launcher did not
touch that file. A later stable PS5 preflight passed. This is positive fail-closed evidence, not
a route failure.

## Cycle-2 acceptance state

Implementation and Lead QA are complete on the pinned hashes above. Fresh accepting
`gpt-5.6-sol` xhigh and `claude-opus-5` xhigh T0 verdicts are still required before the route is
repo-ready. No coding permission is granted by this cycle.

## Cycle-2 T0 round 1 — REQUEST_CHANGES and repair (2026-08-16)

Fresh host-integrated Codex `gpt-5.6-sol`, xhigh, ephemeral session
`01a00b57-0f6c-7280-a4de-c944296869d5` returned **REQUEST_CHANGES** with three required findings:

1. The authenticated profile path was used for launcher/config discovery but was not imposed on
   the Antigravity child. Fake-profile preflight passed while real PS7/PS5 inference returned an
   empty response with no authenticated cache reads.
2. The PS5 timeout fallback enumerated descendants only once. A parent spawning `ping.exe` every
   35 ms timed out normally but left seven descendants alive.
3. `ConvertFrom-Json` unwrapped singleton root arrays, so both a wrapped project object and a
   wrapped success payload were accepted.

Lead testing also reproduced an initial watcher blind window: a transient marker created and
deleted 1.8 seconds after launcher start could complete before watcher registration. This real
defect is repaired in the same round even though it was omitted from the auditor's final list.

Repaired launcher identity:

```text
launcher SHA256 = 67918EA88C61632416A027AC4D153D5E602C6251F3E178CFF8EF55B8EDAD9AE9
project  SHA256 = BF5DED19F712CACA2D8DD38588E015C1717FEFD2CF2577CF54A7D604A88E3551
```

### Round-1 repair evidence

The Antigravity child now receives a canonical, process-scoped profile environment
(`USERPROFILE`, `HOME`, `HOMEDRIVE`, `HOMEPATH`, `APPDATA`, and `LOCALAPPDATA`), and every caller
value is restored afterward. Both PS7 and PS5.1 real inference under deliberately false values
returned the canonical repo and sentinel. Both real `write_file` probes were denied; both unique
markers remained absent.

The PS5 fallback now stops the root first, repeatedly discovers descendants of every observed
tree member, stops newly discovered children, and requires three stable zero-survivor passes.
The auditor's old implementation left seven descendants (RED); the repaired production AST
against the same 35 ms rapid spawner returned `RAPID_TIMEOUT_CAUGHT=True` and
`RAPID_TIMEOUT_SURVIVORS=0` (GREEN).

Both validators now reject any raw root that is not a JSON object before `ConvertFrom-Json`.
The auditor's prior singleton project and payload arrays were accepted (RED). Repaired PS7/PS5.1
payload fixtures rejected the array and accepted the object; a real wrapped project config was
rejected and the exact original config hash was restored (GREEN).

Watcher registration and enablement now occur before project validation, config hashing, and the
initial repo snapshot. The prior 1.8-second transient marker was missed (RED). The repaired
production preflight caught Created/Changed/Deleted events for the same marker and failed closed;
the marker was absent afterward (GREEN).

Fresh PS7 and PS5.1 preflights passed after every repair. No repo source, protected surface, Git
state, or project-config byte remains changed by these tests. Cycle-2 round 2 must independently
reproduce this evidence. Claude has not yet been invoked. Coding access remains disabled.
