# WP-I minimum security baseline

- Date: 2026-08-01
- Status: **PRE-GATE-A / STATIC ONLY**
- Frozen source: `637307e83951ffe23e768ed8e50ddaf8712b0660`
- Candidate release SHA: `1adf9ae51b0ddfe81057860aec5c23bb842f5a84`
- Stable artifact path: `C:\WPI_ARTIFACTS\1adf9ae51b0ddfe81057860aec5c23bb842f5a84`
- Built from clean `C:\WPL` using existing `package.sh`; RELEASE_SHA matched; RELEASE_SHA256SUMS SHA-256 `bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02`; `sha256sum -c` exited 0 for every entry.
- 7,061 regular files and 1,051,904,669 bytes scanned.
- After-build content-redacted path-hit counts: private_key_block=0, aws_access_key=0, github_token=0, slack_token=0, openai_token=0, anthropic_token=0, xai_token=0, telegram_bot_token=0, ethereum_private_key=0, TOTAL_CATEGORY_PATH_HITS=0; no value printed.
- Candidate/path manifest and repository/payload scan: statically/local satisfied.
- Execution boundary: no Ubuntu install, service action, backup/restore, rollback,
  reboot, SIGTERM, broker, exchange, TESTNET, mainnet, order, or live-capital
  action has occurred.

This artifact closes the WP-I outbound-network inventory SMALL-GAP and records
the local dependency and secret-scan evidence required before final Gate A. It
does not authorize staging or any later gate.

## 1. Pinned dependency inventory contract

| Item | Frozen evidence |
|---|---|
| Direct dependency input | `IBKR_PAPER_BRIDGE/requirements.in`: 10 direct entries |
| Resolved inventory | `IBKR_PAPER_BRIDGE/requirements.lock`: 56 exact pinned distributions in the transitive closure, including the direct entries |
| Lock validator | `IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py` requires an exact `==` version and at least one SHA-256 artifact hash for every distribution; it rejects URLs, VCS references, and index overrides |
| Installer | `IBKR_PAPER_BRIDGE/deploy/linux/install.sh` installs only the lock into a per-release-SHA Python 3.12 virtual environment |
| Git blob | `47f53fa227bf0f18b9bf9bd77e060d8856961728` |
| Raw Git-blob SHA-256 | `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e` |

The online installer arguments are `--require-hashes --no-deps
--only-binary=:all: --no-input --no-cache-dir --disable-pip-version-check` and
the exact lock path. The offline wheelhouse mode adds `--no-index --find-links`
and uses the same hash and binary-wheel restrictions. Online mode may contact
the Python package index selected by the target host's pip configuration;
wheelhouse mode is fully offline.

This is an SBOM-equivalent pinned inventory for the bounded WP-I gate. It is
not a CycloneDX or SPDX SBOM, does not contain license or vulnerability
analysis, does not map installed files to packages, and is not proof that the
lock installs successfully on Ubuntu. Exact installed-distribution equality
and Python 3.12 compatibility remain post-Gate-A Ubuntu evidence.

## 2. Secret-scan contract and result

The scan is content-redacted: it reports category counts and paths only, never
matched text. It searches every non-binary tracked blob at the exact frozen Git
tree for high-confidence private-key and provider-token signatures:

- PEM/OpenSSH/PGP private-key blocks;
- AWS access keys;
- GitHub, Slack, OpenAI, Anthropic, and xAI token forms;
- Telegram bot-token form; and
- a `0x`-prefixed 32-byte Ethereum private-key form.

Result on 2026-08-01: **zero category/path hits across the frozen tracked
tree**. Because `package.sh` constructs its source tree with `git archive` of
that exact commit, the scan covers the source files that would enter the
payload. Built payload at `C:\WPI_ARTIFACTS\1adf9ae51b0ddfe81057860aec5c23bb842f5a84` with RELEASE_SHA=1adf9ae51b0ddfe81057860aec5c23bb842f5a84; RELEASE_SHA256SUMS SHA-256 bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02; `sha256sum -c` exit 0 on all 7,060 manifest entries; the payload contains 7,061 regular files; after-build content-redacted scan zero hits.

| Signature category | Frozen-tree category/path hits |
|---|---:|
| Private-key block | 0 |
| AWS access key | 0 |
| GitHub token | 0 |
| Slack token | 0 |
| OpenAI token | 0 |
| Anthropic token | 0 |
| xAI token | 0 |
| Telegram bot token | 0 |
| Ethereum private key | 0 |

A second content-redacted pass over the three allowlisted working-copy
documents after authoring also returned zero category/path hits.

Existing secret-safety coverage also includes:

- `test_program_tree_has_no_private_host_ip_user_or_key_path`;
- `test_env_template_contains_names_and_comments_but_no_definitions`;
- `test_secret_safe_output`; and
- `test_manifest_leaks_no_path_or_identifier`.

The first two were reproduced in a credential-scrubbed child process:
`2 passed in 0.89s`. The last two remain cited existing coverage; they are not
represented as a clean rerun in this artifact.

Limitations: `git grep -I` excludes binary blobs; the scan excludes untracked
and ignored files, Git history other than the frozen tree, process environment,
OS credential stores, user registries, shell history, and remote systems. After-build scan of the immutable payload occurred and returned zero hits. It is
signature-based rather than entropy-based and does not replace a dedicated
secret-scanning product. A future match must be handled without printing the value and is a hard BLOCK
until the owner confirms remediation.

## 3. Outbound-network inventory

| Class | Destination | Protocol / port | Activation condition | Code evidence | Data / credential class | Fail-closed disposition | Ubuntu confirmation owed |
|---|---|---|---|---|---|---|---|
| Runtime-required for non-dry-run paper operation | `api.hyperliquid-testnet.xyz` | HTTPS and secure WebSocket, TCP 443 | Runtime starts with `dry_run=False`; both Hyperliquid credential names resolve; the SDK clients connect | `bridge/app.py:191-208` constructs only `network="testnet"`; `bridge/broker/hyperliquid.py:2171-2183` selects `constants.TESTNET_API_URL` and creates REST/WebSocket-capable SDK clients | Account identifier, market/account/reconciliation/order data, signed requests; the agent/API wallet private key is used locally for signing and must never be logged or documented | Missing credentials raise before client construction; the selected app path is TESTNET only | Yes: DNS, HTTPS, WebSocket, destination, certificate, and absence of mainnet traffic must be observed on the Gate-A-authorised host |
| Runtime-optional | `api.telegram.org` | HTTPS, TCP 443 | Notification is enabled and both `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are present | `bridge/engine/notify.py:40-57` constructs the HTTPS POST only after both names resolve | Bot token in the HTTPS request path; chat identifier and alert text in the request body | Missing credentials disable the notifier; send failures are swallowed, so Telegram delivery is not a safety gate | Yes if enabled; otherwise confirm the notifier is disabled and makes no request |
| Install-time-only | Host-configured Python package index | Normally HTTPS, TCP 443; exact destination follows pip configuration | `install.sh` runs without `--wheelhouse` | `deploy/linux/install.sh` builds `pip install` arguments from the exact lock | Package names, versions, artifact hashes; any externally configured index authentication remains outside this repository | Exact hashes, no dependencies, binary wheels only, no input, and no cache; any download or hash mismatch aborts installation | Yes for online mode; alternatively prove `--wheelhouse` with `--no-index` is fully offline |
| Local listener, not external outbound | `127.0.0.1:8790` | Local HTTP and WebSocket, TCP 8790 | Bridge runtime is explicitly started | `bridge/app.py:214-234`; `deploy/linux/install.sh` and `verify.sh` assert the loopback source/boundary | Local status, control, and WebSocket data; no public bind | Hard-coded loopback bind; pre-start checks reject an existing listener and public listener assertions remain required | Yes: prove loopback-only and no non-loopback listener on Ubuntu |
| Forbidden / unselected | Hyperliquid mainnet SDK base (`api.hyperliquid.xyz`) | HTTPS and secure WebSocket, TCP 443 | **No permitted activation condition in this program** | The SDK exposes a mainnet branch, but `bridge/app.py:202-205` supplies only `network="testnet"` | None permitted | Mainnet is forbidden; static app selection is TESTNET only. Any observed mainnet attempt is BLOCK | Yes: confirm absence of mainnet traffic during every authorised Ubuntu capture |
| Unused settings; no endpoint claimed | Anthropic and xAI | None established by runtime Bridge source | Settings names and a locked Anthropic dependency exist, but targeted runtime source search found no Anthropic or xAI client import/use | `bridge/settings.py:31-37`; zero targeted runtime-client hits | Secret names only; no value and no outbound data flow claimed | No runtime client path was found; do not infer an endpoint from settings or a dependency | Re-run the source search at the final frozen SHA; no network exercise is owed for an unused path |

The units' `RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX` limits address
families, not destinations. Destination egress control is therefore absent and
remains deferred. Host DNS resolver behavior and proxy configuration are also
host-dependent and must be captured during authorised Ubuntu verification.

## 4. Hard boundaries

- **No public surface:** the only application listener is
  `127.0.0.1:8790`; this artifact does not open a firewall, reverse proxy, SSH
  tunnel, or non-loopback listener.
- **No mainnet:** mainnet selection, credentials, connectivity, signatures,
  orders, transfers, or live-capital action are forbidden.
- **No order:** no broker or exchange call was made and no order was sent,
  signed, simulated, or authorised by this work.
- **No secret disclosure observed:** no credential value was intentionally
  inspected, printed, copied into output, or persisted. Earlier unsanitized
  pytest collection inherited settings variables and may therefore have loaded
  their values into `Settings()` in memory. No disclosure was observed. The
  fresh pytest evidence below removes the seven named variables from each child
  environment without inspecting their values.
- **No execution claim:** Ubuntu install/runtime/backup/restore/rollback,
  reboot, systemd, and SIGTERM evidence remains owed after final Gate A.
- **No premature WP-L claim:** `WP-L Phase 2 — Ubuntu revalidation` remains a
  post-Gate-A activity on the retained authorised staging host.

## 5. Reproducible local validation

Each block is standalone and read-only.

### Frozen identity and allowed worktree scope

```powershell
Set-Location -LiteralPath 'C:\WPL'
$expectedHead = '637307e83951ffe23e768ed8e50ddaf8712b0660'
$allowed = @(
  'IBKR_PAPER_BRIDGE/deploy/linux/README.md',
  'IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md',
  'MTC_COMMAND_CENTER/11_TRIAGE/WPI_READINESS_RECORD_2026-08-01.md'
)
$actualHead = git rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $actualHead -ne $expectedHead) { throw "Unexpected HEAD: $actualHead" }
$changed = @(git status --porcelain=v1 --untracked-files=all | ForEach-Object { $_.Substring(3).Replace('\','/') })
$outside = @($changed | Where-Object { $_ -notin $allowed })
if ($outside.Count -ne 0) { throw "Out-of-scope paths: $($outside -join ', ')" }
"HEAD=$actualHead"
"CHANGED_PATHS=$($changed.Count)"
```

### Lock identity and inventory

```powershell
Set-Location -LiteralPath 'C:\WPL'
$expectedHead = '637307e83951ffe23e768ed8e50ddaf8712b0660'
$lockPath = 'IBKR_PAPER_BRIDGE/requirements.lock'
$expectedBlob = '47f53fa227bf0f18b9bf9bd77e060d8856961728'
$expectedSha256 = 'a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e'
$actualBlob = git rev-parse "$expectedHead`:$lockPath"
if ($LASTEXITCODE -ne 0 -or $actualBlob -ne $expectedBlob) { throw "Unexpected lock blob: $actualBlob" }
@'
import hashlib
import importlib.util
import subprocess
from pathlib import Path

root = Path(r"C:\WPL")
head = "637307e83951ffe23e768ed8e50ddaf8712b0660"
lock_rel = "IBKR_PAPER_BRIDGE/requirements.lock"
raw = subprocess.check_output(["git", "cat-file", "blob", f"{head}:{lock_rel}"])
actual_sha256 = hashlib.sha256(raw).hexdigest()
expected_sha256 = "a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e"
if actual_sha256 != expected_sha256:
    raise SystemExit(f"unexpected raw blob SHA-256: {actual_sha256}")
spec = importlib.util.spec_from_file_location(
    "verify_lock", root / "IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
locked = module.parse_lock(root / lock_rel)
direct = [
    line.strip()
    for line in (root / "IBKR_PAPER_BRIDGE/requirements.in").read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.lstrip().startswith("#")
]
if len(direct) != 10 or len(locked) != 56:
    raise SystemExit(f"unexpected inventory: direct={len(direct)} pinned={len(locked)}")
print(f"LOCK_RAW_SHA256={actual_sha256}")
print(f"DIRECT_ENTRIES={len(direct)}")
print(f"PINNED_DISTRIBUTIONS={len(locked)}")
'@ | python -
```

### Content-redacted tracked-tree secret scan

```powershell
Set-Location -LiteralPath 'C:\WPL'
$expectedHead = '637307e83951ffe23e768ed8e50ddaf8712b0660'
$actualHead = git rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $actualHead -ne $expectedHead) { throw "Unexpected HEAD: $actualHead" }
$patterns = [ordered]@{
  private_key_block = '-----BEGIN (RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----'
  aws_access_key = 'AKIA[0-9A-Z]{16}'
  github_token = '(gh[pousr]_[A-Za-z0-9]{36,255}|github_pat_[A-Za-z0-9_]{50,255})'
  slack_token = 'xox[baprs]-[A-Za-z0-9-]{20,}'
  openai_token = 'sk-(proj|svcacct)-[A-Za-z0-9_-]{20,}'
  anthropic_token = 'sk-ant-[A-Za-z0-9_-]{20,}'
  xai_token = 'xai-[A-Za-z0-9_-]{20,}'
  telegram_bot_token = '[0-9]{8,10}:[A-Za-z0-9_-]{35}'
  ethereum_private_key = '0x[0-9a-fA-F]{64}'
}
$total = 0
foreach ($entry in $patterns.GetEnumerator()) {
  $paths = @(git grep -I -l -E -e $entry.Value $expectedHead -- 2>$null)
  $scanExit = $LASTEXITCODE
  if ($scanExit -notin 0,1) { throw "git grep failed for $($entry.Key), exit $scanExit" }
  $count = @($paths | Where-Object { $_ }).Count
  $total += $count
  "{0}={1}" -f $entry.Key,$count
  $paths | Where-Object { $_ } | ForEach-Object { "PATH[{0}]={1}" -f $entry.Key,$_.Substring($expectedHead.Length + 1) }
}
if ($total -ne 0) { throw "Secret-signature category/path hits=$total; do not print matched text" }
"TOTAL_CATEGORY_PATH_HITS=$total"
```

### Focused static deployment tests

```powershell
$start = [System.Diagnostics.ProcessStartInfo]::new()
$start.FileName = 'python'
$start.Arguments = '-m pytest -q -p no:cacheprovider --ignore=TSP1009B.pytest_tmp_s1r1 tests/test_linux_deployment.py::test_lock_is_exact_fully_hashed_and_contains_every_direct_dependency tests/test_linux_deployment.py::test_lock_generation_contract_targets_python_312_linux_with_hashes tests/test_linux_deployment.py::test_installer_uses_per_sha_venv_hashes_and_binary_wheels_only tests/test_linux_deployment.py::test_rollback_is_exact_preserves_state_and_never_starts'
$start.WorkingDirectory = 'C:\WPL\IBKR_PAPER_BRIDGE'
$start.UseShellExecute = $false
foreach ($name in @('HL_ACCOUNT_ADDRESS','HL_API_WALLET_KEY','HL_LIVE_ACK','ANTHROPIC_API_KEY','XAI_API_KEY','TELEGRAM_BOT_TOKEN','TELEGRAM_CHAT_ID')) {
  [void]$start.Environment.Remove($name)
}
$process = [System.Diagnostics.Process]::Start($start)
$process.WaitForExit()
if ($process.ExitCode -ne 0) { throw "Focused deployment tests failed with exit $($process.ExitCode)" }
```

Fresh credential-scrubbed child result: **4 passed in 0.68s**. The auditor's
earlier **4 passed in 0.55s** run was functionally passing but inherited the
parent settings environment.

### Secret-safety structural tests

```powershell
$start = [System.Diagnostics.ProcessStartInfo]::new()
$start.FileName = 'python'
$start.Arguments = '-m pytest -q -p no:cacheprovider --ignore=TSP1009B.pytest_tmp_s1r1 tests/test_linux_deployment.py::test_program_tree_has_no_private_host_ip_user_or_key_path tests/test_linux_deployment.py::test_env_template_contains_names_and_comments_but_no_definitions'
$start.WorkingDirectory = 'C:\WPL\IBKR_PAPER_BRIDGE'
$start.UseShellExecute = $false
foreach ($name in @('HL_ACCOUNT_ADDRESS','HL_API_WALLET_KEY','HL_LIVE_ACK','ANTHROPIC_API_KEY','XAI_API_KEY','TELEGRAM_BOT_TOKEN','TELEGRAM_CHAT_ID')) {
  [void]$start.Environment.Remove($name)
}
$process = [System.Diagnostics.Process]::Start($start)
$process.WaitForExit()
if ($process.ExitCode -ne 0) { throw "Secret-safety structural tests failed with exit $($process.ExitCode)" }
```

Fresh credential-scrubbed child result: **2 passed in 0.89s**. The auditor's
earlier **2 passed in 0.53s** run was functionally passing but inherited the
parent settings environment. In both earlier auditor runs, pytest collection
may have loaded credential values into `Settings()` in memory; no disclosure
was observed.

### Payload verification (read-only)

```powershell
$payload = 'C:\WPI_ARTIFACTS\1adf9ae51b0ddfe81057860aec5c23bb842f5a84'
$releaseSha = (Get-Content -Raw -LiteralPath (Join-Path $payload 'RELEASE_SHA')).Trim()
if ($releaseSha -ne '1adf9ae51b0ddfe81057860aec5c23bb842f5a84') { throw 'RELEASE_SHA mismatch' }
$manifestHash = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $payload 'RELEASE_SHA256SUMS')).Hash.ToLower()
if ($manifestHash -ne 'bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02') { throw 'manifest hash mismatch' }
& 'C:\Program Files\Git\bin\bash.exe' -lc "cd '/c/WPI_ARTIFACTS/1adf9ae51b0ddfe81057860aec5c23bb842f5a84' && sha256sum -c RELEASE_SHA256SUMS >/dev/null" ; if ($LASTEXITCODE -ne 0) { throw 'sha256sum verify failed' }
```

### Runtime endpoint selection and unused-client search

```powershell
Set-Location -LiteralPath 'C:\WPL'
$hits = @(rg -n -i --glob '*.py' '(^|[[:space:]])(from|import)[[:space:]]+(anthropic|xai)([[:space:].]|$)|Anthropic\(|xai\.' 'IBKR_PAPER_BRIDGE/bridge')
$searchExit = $LASTEXITCODE
if ($searchExit -eq 0) { $hits; throw 'Anthropic/xAI runtime client use found' }
if ($searchExit -ne 1) { throw "rg failed with exit $searchExit" }
$app = Get-Content -Raw -LiteralPath 'IBKR_PAPER_BRIDGE/bridge/app.py'
if ($app -notmatch 'network="testnet"' -or $app -match 'network="mainnet"') { throw 'Unexpected app broker-network selection' }
Set-Location -LiteralPath 'C:\WPL\IBKR_PAPER_BRIDGE'
python -c "from hyperliquid.utils import constants; print('TESTNET_API_URL=' + constants.TESTNET_API_URL); print('MAINNET_API_URL=' + constants.MAINNET_API_URL)"
if ($LASTEXITCODE -ne 0) { throw "SDK constant inspection failed with exit $LASTEXITCODE" }
"ANTHROPIC_XAI_RUNTIME_CLIENT_HITS=0"
```

## 6. Static conclusion

The pinned inventory, content-redacted repository scan, outbound-network inventory, and immutable built-payload verification are complete as local artifacts. The outbound-network SMALL-GAP is therefore closed **as an artifact only**. Only Ubuntu/install/runtime proof remains open.
