Status: P9-15 POLICY GRAMMAR DRAFT V1 — UNREVIEWED — NOT CANONICAL — precondition-3 input for producer dispatch

# Lane PL1 — Canonical P9-15 egress policy grammar, DRAFT V1

This document is the precondition-3 input required before the corrected P9-15 producer
kickoff may dispatch: "Supply the reviewed exhaustive egress grammar for the canonical
`p9_15_policy.json`, including its exact bytes or an exact closed grammar matrix from
which those bytes are mechanically produced" (`C:\tmp\lane_out\P9K_PACKET9_KICKOFF_REPAIR.md:71`,
committed as `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_PRODUCER_KICKOFF_REPAIR_2026-08-16.md`).

What this document is: a draft of the egress-axis content of `p9_15_policy.json`,
derived from the normative sources and grounded in the actual tracked universe, plus
the exact proposed canonical JSON bytes of that draft.

What this document is not: it is not a review (a separate independent review follows;
the drafter does not review the draft), not an adoption, not the canonical policy
(the spec holds the final grammar bytes UNKNOWN until a reviewed policy is frozen at
Commit 2 — `P9_15_PRODUCER_SPEC_2026-08-15.md:533`), not a producer implementation,
and not scan evidence. Nothing here was executed against any source tree as
production evidence; the greps cited below were read-only grounding on the snapshot,
which is what the task orders ("read-only grep of the snapshot").

No host, network, SSH, deployment, service, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, or economic
action was performed or authorized by this lane.

## 0. Authority chain and derivation sources

The policy artifact is one of exactly three Commit-2-tracked producer artifacts, and
the contract assigns to it "versioned signature categories, modeled network
constructs, expected disposition grammar, and exact source-universe rules"
(`AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:47-51`). The implementable spec
fixes what the policy must contain on the egress axis and how the engine must treat
a gap: the six egress classes are policy data
(`P9_15_PRODUCER_SPEC_2026-08-15.md:158`), and "the generic implementation MUST
treat an absent category, unknown policy key, unconsumed network-capable token,
unsupported nested form, or non-exhaustive policy declaration as `UNRESOLVED` and
`STOP/3/POLICY_COVERAGE_INCOMPLETE`" (`P9_15_PRODUCER_SPEC_2026-08-15.md:160`),
implementing the fail-closed rule of
`DESIGN_DEFECT_PATTERNS_2026-08-10.md:919-929` ("a recognised primitive with any
unconsumed token or unsupported semantic form must STOP with a coverage reason").

Sources used, with the role each plays:

| Source | Role |
|---|---|
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:47-51,99-109,126,147-164` | assigns policy content; defines the three sub-universes; the six-class seed; egress-row grammar incl. explicit expected-absence rows; result classification; required falsifications |
| `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:148-160,286-292,376-385,520-538` | egress universe definition; fail-closed boundary; egress.jsonl schema and dispositions; POLICY_INVALID / POLICY_COVERAGE_INCOMPLETE / EGRESS_POLICY_DEVIATION mappings; falsification duty; honest-unknowns boundary |
| `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:899-929` (Pattern 12) and `:933-967` (Pattern 13) | fail-closed coverage rule and its concrete past failures (`ssh`/`getent hosts` losing endpoints, `find -exec`, the `<>` token, zero-facts-plus-PASS); terminal-disposition conservation |
| `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:47-77` | the test applied to this draft's own completeness rule in §1.7 |
| `IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:94-108` (six-class seed), `:44-54,196-225` (secret axis, out of scope here) | the prior outbound-network inventory the contract names as seed-only, to be re-derived, never copied (`AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:109`) |
| The tracked tree under `IBKR_PAPER_BRIDGE/` at snapshot `c84497c8` (read-only Glob/Grep) | the real universe the grammar must cover: 131 tracked paths, of which 2 are expected binaries (`docs/screenshots/overview.png`, `docs/screenshots/trading.png`) |

Honest grounding note: the producer will scan the **Commit-2** tree, which does not
exist yet and which this draft cannot know. Every construct statement below is
grounded at snapshot `c84497c8` and is labeled with its real occurrences. The
closure rule (§1.5) is what makes a Commit-2 construct outside this matrix
detectable rather than silently passed. This is recorded as limitation
`UNIVERSE_GROUNDED_AT_SNAPSHOT_c84497c8_RECHECK_AT_COMMIT2`.

## Part 1 — the closed grammar matrix

### 1.1 Egress universe and terminal file dispositions

Universe: every `text_utf8` tracked blob at `SOURCE_SHA` below `IBKR_PAPER_BRIDGE/`
(`P9_15_PRODUCER_SPEC_2026-08-15.md:150`). Not claimed: worktree untracked content,
ignored files, history other than `SOURCE_SHA`, process environment, registry,
credential stores, shell history, remote hosts (`AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:99`).

Every admitted blob receives exactly one terminal egress disposition
(`P9_15_PRODUCER_SPEC_2026-08-15.md:281-283`):

| Disposition | Meaning in this grammar |
|---|---|
| `analyzed` | executable or configuration file; every network-capable token in it was consumed by a family rule (§1.3) or emitted as `UNRESOLVED` |
| `not_executable_or_network_relevant` | documentation/data blob no program path executes; endpoint-like tokens are **censused** (recorded, kind + path) — never silently dropped |
| `unresolved` | the file contains an unconsumed network-capable token or unsupported form → forces `STOP/3/POLICY_COVERAGE_INCOMPLETE` |
| `not_in_egress_universe` | text blobs outside the prefix (appears in `universe.jsonl` only) |

### 1.2 Endpoint catalog — the six classes mapped to the real universe

The six classes are policy-declared classification labels, **not** expected current
results; all rows are re-derived at `SOURCE_SHA`
(`P9_15_PRODUCER_SPEC_2026-08-15.md:158`). Disposition vocabulary of `egress.jsonl`
(`P9_15_PRODUCER_SPEC_2026-08-15.md:290`): an allowed class resolved to a real
activation path → `resolved_allowed`; the forbidden class with **no** activating
construction site → `expected_absent` (an explicit row, per
`AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:126`); an activating forbidden path
→ `resolved_forbidden` (FAIL); a construct resolving to a host outside the catalog →
`resolved_unexpected` (FAIL).

| # | Endpoint | Class | Proto/port | Endpoint extractor | Activation predicate | Disposition | Evidence |
|---|---|---|---|---|---|---|---|
| E1 | `api.hyperliquid-testnet.xyz` | runtime-required | HTTPS+WSS / 443 | `base_url = constants.TESTNET_API_URL` passed to `Info(base_url, skip_ws=False)` / `Exchange(wallet, base_url)`; frozen constant→host mapping in the policy, verified against the hash-pinned SDK wheel (`requirements.lock:601` pins `hyperliquid-python-sdk==0.24.0`) | `HyperliquidBroker(network="testnet")` with owned clients and credentials resolved (env or HKCU registry), reached from `python -m bridge.app` non-dry-run or the smoke tools; dry-run uses `MockBroker` and does not activate | ALLOWED-ENDPOINT-CLASS | `IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py:1954-1966`; `bridge/app.py:113-114,191-208,234`; `bridge/settings.py:73-117`; `tools/smoke_p0.py:47-53`; `tools/smoke_fill.py:67`; `tools/probe_user_events.py:31`; `SECURITY_BASELINE.md:98` |
| E2 | `api.telegram.org` | runtime-optional | HTTPS / 443 | URL f-string literal at `bridge/engine/notify.py:41` passed to `httpx.AsyncClient().post`; policy records **scheme+host only** — the URL path embeds the bot token and must never be recorded (content-redaction rule: `P9_15_PRODUCER_SPEC_2026-08-15.md:288` forbids match text; `AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:107` category/path only) | notifier enabled AND both `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` resolve; `notify.telegram_enabled: true` (`config/bridge.yaml:36-38`); send failures swallowed — never a safety gate | ALLOWED-ENDPOINT-CLASS | `bridge/engine/notify.py:13,40-58`; `bridge/settings.py:142-145`; `SECURITY_BASELINE.md:99` |
| E3 | `HOST_CONFIGURED_PYTHON_INDEX` (destination host **UNKNOWN**) | install-time-only | HTTPS / 443 | `pip install --require-hashes --no-deps --only-binary=:all: ...` argument vector (`install.sh:292-306`); the destination lives in host pip configuration, not in any repository token | installer venv-creation branch runs with `WHEELHOUSE` unset; a set `WHEELHOUSE` adds `--no-index --find-links` and is fully offline (`install.sh:299-303`) | ALLOWED-ENDPOINT-CLASS with UNKNOWN destination host (see §1.9) | `install.sh:292-306`; `SECURITY_BASELINE.md:31-36,100` |
| E4 | `127.0.0.1:8790` | local-listener | HTTP+WS (loopback) / 8790 | `uvicorn.run(..., host="127.0.0.1", port=8790)` literals (`app.py:234`); `server.host`/`server.port` (`config/bridge.yaml:51-53`); browser side same-origin `window.location.host` (`app.js:24,239-240`); loopback asserted by `common.sh:182-206` | `bridge.app` executed via `python -m bridge.app` (systemd `ExecStart` in both unit templates; `run_bridge_p2.ps1:13`) or direct module run | ALLOWED-ENDPOINT-CLASS (loopback only; non-loopback bind token is forbidden — §1.4) | `bridge/app.py:234`; `deploy/linux/systemd/mtc-bridge-first-start.service.template:34`; `mtc-bridge-steady.service.template:37`; `deploy/linux/lib/common.sh:30,182-206`; `SECURITY_BASELINE.md:101` |
| E5 | `api.hyperliquid.xyz` (mainnet) | forbidden-unselected | HTTPS+WSS / 443 | `constants.MAINNET_API_URL` branch of the same constructor expression (`hyperliquid.py:1962`) | **NONE PERMITTED**: mainnet requires the triple lock (`hyperliquid.py:1948-1952`) and every first-party construction site supplies `network="testnet"` only (`app.py:202-208`) | FORBIDDEN: dormant branch without an activating site → `expected_absent` row; any activating mainnet path → `resolved_forbidden` + `FAIL/1/EGRESS_POLICY_DEVIATION` | `hyperliquid.py:1948-1952`; `app.py:202-208`; `SECURITY_BASELINE.md:102` |
| E6 | (none) Anthropic/xAI | unused-setting-no-endpoint | — | none: settings names exist (`settings.py:34-35`), `anthropic==0.120.0` is locked (`requirements.lock:11`), but **no runtime client import or construction exists**; `NullLLMGate` "never calls external APIs" (`llm_gate.py:22-26`); both LLM switches false (`config/bridge.yaml:39-50`) | none at `c84497c8`. Any `anthropic`/`xai` client construct appearing at `SOURCE_SHA` is outside this entry → `UNRESOLVED` until a policy revision adds it | ALLOWED (as a no-endpoint fact): do **not** infer an endpoint from a setting or a locked dependency | `SECURITY_BASELINE.md:103`; `settings.py:34-35`; `llm_gate.py:22-26` |

Credential names recorded per class (names only, never values —
`P9_15_PRODUCER_SPEC_2026-08-15.md:126`): E1 → `HL_ACCOUNT_ADDRESS`, `HL_API_WALLET_KEY`;
E2 → `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`; E6 → `ANTHROPIC_API_KEY`, `XAI_API_KEY`.
`HL_LIVE_ACK` is forbidden anywhere in the tracked tree
(`deploy/linux/env/mtc-bridge.env.template:31-38`; `deploy/linux/verify.sh:141`).

### 1.3 Language-family matrix

Each family carries: exact recognized tokens, endpoint extractor, activation
predicate, disposition, and an explicit **outside-matrix clause**. The selector
assigns every egress-universe blob to exactly one family; a blob matching no family
while containing sweep-detector hits (§1.6) is `unresolved`.

#### F1 `python-runtime` — `bridge/**/*.py`, `tools/**/*.py` (executable)

| Recognized token (exact) | Endpoint extractor | Activation predicate | Disposition |
|---|---|---|---|
| `from hyperliquid.exchange import Exchange` / `from hyperliquid.info import Info` / `from hyperliquid.utils import constants` / `from hyperliquid.utils.types import Cloid` | marks module SDK-client-bearing; endpoint from constructor argument | see E1 | entry of constructed client |
| `Info(` / `Exchange(` constructors | `base_url` argument; `skip_ws` toggles WSS | see E1 | resolve to catalog |
| `constants.TESTNET_API_URL` / `constants.MAINNET_API_URL` | frozen constant→host mapping, verified against the locked wheel | selector value | E1 / E5 |
| `.subscribe(` on an SDK `Info` client (incl. `subscribe_bars`, `subscribe_user_events`) | inherits owning client `base_url`; WSS | subscription registered before/after `connect()` | same class as owning client — `hyperliquid.py:274-311`; `bridge/engine/bars.py:124` |
| `self.info.<method>` / `self.exchange.<method>` REST calls (`user_state`, `open_orders`, `user_fills_by_time`, `user_funding_history`, `query_user_abstraction_state`, `meta`, `historical_bars`, `cancel_by_cloid`, …) | inherits owning client `base_url`; HTTPS | owning client connected | same class as owning client |
| `import httpx` / `httpx.AsyncClient(` / `client.post(` | first positional/f-string URL argument; scheme+host only | see E2 | E2 |
| `uvicorn.run(` | `host`/`port` keyword literals | `python -m bridge.app` executed | E4; non-loopback host token forbidden |
| `allow_origins=[` | URL literals in list | n/a (declaration) | consumed as local origins — `app.py:100` |
| `@app.get` / `@app.post` / `@app.put` / `@app.websocket` / `websocket.accept(` | serves on owning app listener | listener active | E4 surface — `bridge/api/routes.py:21-61`; `bridge/api/ws.py:17-49` |
| `from eth_account import Account` | none (local signing) | — | consumed `LOCAL_SIGNING_NO_ENDPOINT` |
| `import winreg` / `QueryValueEx(` | none (credential-source read) | — | consumed `CREDENTIAL_SOURCE_READ` — `settings.py:96-108` |
| URL string literal (regex `https?://…`) | scheme://host(:port) | context | resolve to catalog; uncatalogued host in runtime code → UNRESOLVED |
| credential env-name tokens | record name only | — | `credential_names` of the class |

**Outside-matrix clause:** any other network-capable import or call — `socket`,
`ssl`, `requests`, `urllib`, `http.client`, `aiohttp`, websockets-client,
`asyncio.open_connection`/`start_server`, `smtplib`, `telnetlib`, `ftplib`,
`imaplib`, `poplib`, DNS-resolution calls, or `subprocess`/`os.system` to a network
command — is `UNRESOLVED` → `STOP/3/POLICY_COVERAGE_INCOMPLETE`. Zero occur at
`c84497c8` (verified by the sweep in §1.6).

#### F2 `python-tests` — `tests/**/*.py` (executable)

| Recognized token | Extractor | Activation | Disposition |
|---|---|---|---|
| URL string literal in fixture data (e.g. `http://x` at `tests/test_llm_gate.py:33`) | scheme+host | none (fixture input to the sanitizer) | consumed `TEST_FIXTURE_INERT`, host recorded, never an EGRESS row |
| `subprocess.run(` / `subprocess.Popen(` / `os.system` | argv dispatch: `sys.executable`/`python` → python grammar recursion; `git` → git verb table (§1.4); `bash -c` → F3 recursion; any other argv0 → UNRESOLVED | local child processes | recursive dispatch — `tests/test_linux_deployment.py:67-79`; `tests/test_order_state.py:516-523`; `tests/test_release_evidence.py:229-241`; `tests/test_runtime_baseline.py:26-32`; `tools/check_runtime_baseline.py:71-86` |
| `import hyperliquid.*` in tests | type/wire helpers only; no live-base_url client construction | — | consumed `TEST_HELPER_IMPORT` — `tests/test_hyperliquid_broker.py:20-22` |

**Outside-matrix clause:** a test constructing an SDK client with a non-testnet
base_url, or shelling to `curl`/`wget`/`ssh`, is `UNRESOLVED`.

#### F3 `shell-deploy` — `deploy/linux/**/*.sh` (executable)

| Recognized token | Extractor | Activation | Disposition |
|---|---|---|---|
| `pip install --require-hashes --no-deps --only-binary=:all: --no-input --no-cache-dir --disable-pip-version-check -r <lock>` (+`--no-index --find-links` when `WHEELHOUSE` set) | destination = host-configured index; wheelhouse removes the endpoint | venv branch without `WHEELHOUSE` | E3 — `install.sh:292-306` |
| `getent passwd` / `getent group` | endpointless local NSS lookup (backend host-configured) | always (verify/install) | consumed `NAME_SERVICE_LOCAL` — `install.sh:134,200-225`; `verify.sh:37,55-58`. `getent hosts|ahosts|networks` is endpoint-bearing → UNRESOLVED (the exact Pathscope failure: `DESIGN_DEFECT_PATTERNS_2026-08-10.md:914-915`) — OWNER-CHOICE-2 (§1.8) |
| `git rev-parse` / `cat-file` / `archive` / `status` (local verbs) | none | local object ops | consumed `LOCAL_GIT`; git network verbs forbidden (§1.4) — `package.sh:50,60-74` |
| `ufw status verbose` (read-only) | none | verify | consumed `LOCAL_FIREWALL_ASSERTION` — `common.sh:153-179` |
| `ss -H -ltn` | local listener enumeration | verify | consumed `LOCAL_LISTENER_ASSERTION` — `common.sh:195-206` |
| `systemctl is-active`/`is-enabled`/`start`/`stop`/`mask` | local service manager IPC | install/verify/rollback | consumed `LOCAL_SERVICE_MANAGER` — `verify.sh:207-213`; `rollback.sh:81` |
| `require_cmd` list (`stat find systemctl sha256sum sed cmp sort awk mktemp getent id pgrep`) | none | preflight | consumed `LOCAL_TOOLS` — `verify.sh:37`; `install.sh:134` |

**Outside-matrix clause:** `curl`, `wget`, `ssh`, `scp`, `sftp`, `rsync`, `nc`,
`ncat`, `socat`, `telnet`, `ftp`, `ping`, `dig`, `nslookup`, `host`, `/dev/tcp`
redirections, or any unknown command in an executable shell file → `UNRESOLVED`
→ STOP. **Zero occur at `c84497c8`** — the only `curl`/`ssh` strings under
`deploy/linux/` live in `COMMANDS.md` (documentation, F11).

#### F4 `powershell-tools` — `tools/*.ps1` (executable)

| Recognized token | Extractor | Activation | Disposition |
|---|---|---|---|
| call operator invoking `python -m bridge.app` (`& python -m bridge.app`) | process launch → F1 activation of E4 and (non-dry-run) E1 | supervisor loop | consumed `PROCESS_LAUNCH_ACTIVATION` — `tools/run_bridge_p2.ps1:13` |
| `New-Item` / `Set-Location` / `Get-Date` / `Out-File` / `Start-Sleep` | none | — | consumed `LOCAL_TOOLS` |

**Outside-matrix clause:** `Invoke-WebRequest`, `Invoke-RestMethod`,
`Net.WebClient`, `Invoke-Expression`, `Start-Process` of a network binary, or any
network cmdlet in an executable `.ps1` → `UNRESOLVED`. Zero occur at `c84497c8`
(the `Invoke-RestMethod` strings are in `docs/17_DEPLOYMENT.md:58-59`, F11).

#### F5 `javascript-static` — `bridge/static/*.js` (executable in browser origin)

| Recognized token | Extractor | Activation | Disposition |
|---|---|---|---|
| `fetch(<relative path>)` — `app.js:24` | same-origin → serving origin `127.0.0.1:8790` | dashboard open | E4; absolute-URL argument resolves via URL extractor |
| `new WebSocket(\`${scheme}://${window.location.host}/ws\`)` — `app.js:239-240` | same-origin WSS/WS → serving origin | dashboard open | E4 |
| `document.createElementNS(<namespace URI>)` — `app.js:194-213` | `non_endpoint_uri.namespaces` | — | consumed `NON_ENDPOINT_URI` |

**Outside-matrix clause:** `XMLHttpRequest`, `EventSource`, `sendBeacon`, `axios`,
or an absolute external URL → `UNRESOLVED` unless it resolves to a catalog entry.
Zero occur at `c84497c8`.

#### F6 `html-static` — `bridge/static/*.html` (executable in browser origin)

`src=`/`href=` attribute values (`index.html:7,108`): relative → same-origin local
(E4); absolute → scheme://host → catalog or UNRESOLVED. Inline `<script>` with
network calls dispatches to F5. No other network form is modeled; anything else →
UNRESOLVED.

#### F7 `css-static` — `bridge/static/*.css` (executable in browser origin)

`url(` and `@import`: relative → same-origin; absolute → scheme://host. **Expected
absent at `c84497c8`** (no hits); an occurrence resolves to catalog or is UNRESOLVED.

#### F8 `yaml-config` — `config/**/*.yaml` (declarative, consumed by the runtime)

| Key | Extractor | Activation | Disposition |
|---|---|---|---|
| `broker.network` (`config/bridge.yaml:2-3`) | selects catalog SDK branch | E1 path | `testnet` → E1; `mainnet` → E5 |
| `server.host` / `server.port` (`bridge.yaml:51-53`) | listener declaration | E4 | must equal `127.0.0.1`/`8790`; any other host → forbidden |
| `notify.telegram_enabled` (`bridge.yaml:36-38`) | activation input for E2 | E2 | runtime-optional |
| `llm.regime_enabled` / `llm.veto_enabled` (`bridge.yaml:39-50`) | must be false while no provider client exists | — | unused-setting (E6); `true` with no modeled client → UNRESOLVED |
| any URL-valued key | scheme://host | — | catalog or UNRESOLVED |

**Outside-matrix clause:** any other endpoint- or credential-bearing key →
UNRESOLVED. `config/strategies/keltner_trail_ema8.yaml` contains no network keys at
`c84497c8`.

#### F9 `systemd-unit-template` — `deploy/linux/systemd/*.template` (declarative)

| Directive | Extractor | Disposition |
|---|---|---|
| `ExecStart=/opt/mtc-bridge/venvs/@RELEASE_SHA@/bin/python -m bridge.app` (first-start:34; steady:37) | command line → owning grammar | activation path for E4 and E1 |
| `Environment=` / `EnvironmentFile=` (first-start:37-43; steady:39-42) | credential-name source | names only; `HL_LIVE_ACK` presence forbidden |
| `RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX` (first-start:78; steady:75) | socket-family declaration; restricts families, **not** destinations | consumed `DECLARATION_NO_ENDPOINT` with limitation `DESTINATION_CONTROL_DEFERRED_HOST` (`deploy/linux/README.md:128`; `SECURITY_BASELINE.md:105-108`) |
| `Documentation=file://…` (first-start:23; steady:26) | `non_endpoint_uri.schemes` | consumed `NON_ENDPOINT_URI` |

**Outside-matrix clause:** `IPAddressAllow`/`IPAddressDeny`, `ListenStream`,
socket-unit forms, or any network-bearing directive not listed → UNRESOLVED. Zero
occur at `c84497c8`.

#### F10 `env-template` — `deploy/linux/env/*.template` (declarative)

Credential variable names in comments only; each name maps to its class's
`credential_names`. Any `NAME=value` definition is forbidden
(`mtc-bridge.env.template:1-38`); any other variable or value form → UNRESOLVED.

#### F11 `docs-and-data` — `docs/**`, `README.md`, `**/*.md`, `**/*.json`,
`**/*.csv`, `requirements.in`/`.lock`/`.txt`, `deploy/linux/logrotate/*`
(non-executable)

Endpoint-like tokens (URLs such as `https://app.hyperliquid-testnet.xyz` at
`docs/06_HYPERLIQUID_SETUP.md:28`, `http://127.0.0.1:8790` at `README.md:51`,
operator command examples `curl -s http://127.0.0.1:8790/api/status` and
`ssh -N -L 8790:127.0.0.1:8790` at `deploy/linux/COMMANDS.md:219-233`,
`Invoke-RestMethod` at `docs/17_DEPLOYMENT.md:58-59`) are **censused** (token kind
+ path, recorded) and never produce EGRESS rows: no program path executes them.
File disposition `not_executable_or_network_relevant`, reason
`DOCUMENTATION_OR_DATA_NOT_EXECUTABLE`. This classification is OWNER-CHOICE-1
(§1.8). Notes: `docs/audits/AUDIT_DeepSeek_V4_Pro_2026-07-05.md:77` mentions
`smtplib` only as a rejected future idea; `docs/*.json` smoke/probe logs carry no
endpoint tokens at `c84497c8`; `requirements.lock`'s network-capable members
(`anthropic`, `httpx`, `hyperliquid-python-sdk`, transitive `requests`,
`urllib3`, `httpcore`, `anyio`, `websockets`, `uvicorn`, `fastapi`) belong to the
dependency axis and cross-check E6 (locked-but-unused) — they are not themselves
egress rows.

#### F12 `binary-excluded` — `docs/screenshots/*.png`

Counted and hashed by the universe axis; never egress-analyzed.

### 1.4 Cross-cutting consumption rules

1. **Non-endpoint URIs:** `http://www.w3.org/2000/svg` (XML namespaces, `app.js:194-213`) and the `file://` scheme (systemd `Documentation=`) are identifiers/local references — consumed with reason `NON_ENDPOINT_URI`, never EGRESS rows. Any other bare URI in executable code is endpoint-bearing until modeled.
2. **Forbidden tokens:** bind addresses `0.0.0.0` / `::` (`common.sh:182-189` asserts their absence); git network verbs `clone|fetch|pull|push|ls-remote|remote|submodule`; `HL_LIVE_ACK` presence. An observed *activating* occurrence → `FAIL/1/EGRESS_POLICY_DEVIATION`; an unconsumed token → `STOP/3/POLICY_COVERAGE_INCOMPLETE`.
3. **Nested-form dispatch:** `subprocess` argv, `ExecStart=`, `bash -c`, and the PowerShell call operator are not endpoints themselves — they dispatch into the grammar of the launched command. An unsupported nesting (unknown argv0, unknown option on a recognized command, unconsumed operand on an endpoint-bearing command) → UNRESOLVED. This directly implements the Pathscope falsification set (`DESIGN_DEFECT_PATTERNS_2026-08-10.md:915-917`).
4. **Content redaction:** credential **names** only, never values; the Telegram URL path embeds the bot token and is never recorded; EGRESS row `credential_names` is the only credential field (`P9_15_PRODUCER_SPEC_2026-08-15.md:290`).
5. **SDK constant mapping:** `constants.TESTNET_API_URL`→`api.hyperliquid-testnet.xyz`, `constants.MAINNET_API_URL`→`api.hyperliquid.xyz` is frozen in the policy and must be verified by the child against the hash-pinned `hyperliquid-python-sdk` wheel (`requirements.lock:601`); a mismatch → `STOP/3/ARTIFACT_IDENTITY_MISMATCH`.

### 1.5 Closure property

The matrix is closed by construction: (a) every family lists its exact recognized
tokens; (b) every family carries an explicit outside-matrix clause; (c) any
network-capable token, option, operand, redirection, or nested form in an
executable or declarative file that the matrix does not recognize maps to
`UNRESOLVED`, and an `UNRESOLVED` row forces `STOP/3/POLICY_COVERAGE_INCOMPLETE`
(`P9_15_PRODUCER_SPEC_2026-08-15.md:160,379`). **Everything outside the matrix maps
to UNRESOLVED → STOP/3.** An unknown command capable of executing or opening
anything is an opaque sink, not a no-op (`DESIGN_DEFECT_PATTERNS_2026-08-10.md:927`).

### 1.6 Completeness rule — what makes "policy does not cover X" detectable

Three conservation laws, each mechanically checkable:

1. **File level:** admitted egress-universe blobs = `analyzed` + `not_executable_or_network_relevant` + `unresolved`, exactly one terminal disposition each (`DESIGN_DEFECT_PATTERNS_2026-08-10.md:933-967`; `AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:136`).
2. **Token level (the sweep):** in every `analyzed` file, hits from a family-independent detector set (URL/WSS regexes; host:port patterns; per-language network import/call/command/cmdlet/API lists — frozen in the policy, broader than the matrix) must equal consumed-by-matrix + censused-non-endpoint + `UNRESOLVED`. A surplus hit is itself an `UNRESOLVED` row; a deficit (a matrix rule claiming consumption of a token the sweep cannot see) is `STOP/3/CONSERVATION_ERROR`. This is the direct answer to "zero facts plus PASS" (`DESIGN_DEFECT_PATTERNS_2026-08-10.md:922`): a modeled file with zero EGRESS rows still proves it swept and consumed or censused every detected token.
3. **Row level:** every resolved activation path yields exactly one EGRESS row; every policy-declared absence yields exactly one `expected_absent` row — expected absence is an explicit row, not missing output (`AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:126`; `P9_15_PRODUCER_SPEC_2026-08-15.md:290`).

Declared absences (each must appear as an explicit `expected_absent` row): python
direct socket/ssl/requests/urllib/http.client/aiohttp/websockets-client usage;
smtplib/telnetlib/ftplib/imaplib/poplib and DNS calls;
`asyncio.open_connection`/`start_server`; shell `curl`/`wget`/`ssh`/`scp`/`nc`/
`socat`/`ping`/`dig` in executable scripts; PowerShell network cmdlets; CSS
`url()`/`@import`; systemd `IPAddress*`/`Listen*` directives; a **mainnet
activating construction site**; `HL_LIVE_ACK` value in the tree; `getent
hosts`-family lookups; git network verbs.

Policy self-description: the policy JSON declares `key_policy.closed=true`, its
exact `known_top_level_keys`, and `unknown_key_disposition=STOP/3/POLICY_INVALID`
(`P9_15_PRODUCER_SPEC_2026-08-15.md:376`) — so an unknown key introduced by a
future edit is itself a detectable, specified failure rather than a silent ignore.

### 1.7 What would make MY completeness rule fail (self-confirming-check analysis)

Applied test — "what would have to be true for this check to fail?"
(`SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:47-51`):

The completeness rule can pass without proving coverage in one specific way: **the
sweep-detector list is a closed list authored by the same process that authored the
matrix.** A network-capable construct whose token appears in NEITHER list passes
silently, and both conservation laws stay green because nothing was ever counted.
That is the self-confirming seam, and it is recorded in the policy itself
(`SWEEP_DETECTOR_CLOSED_LIST_IS_DRAFT_SEAM`). Concrete worlds in which the rule
goes silently green while coverage is false:

- a construct spelling neither list contains, e.g. a raw `socket` used through a
  re-exported alias, an endpoint assembled at runtime from parts (so the URL regex
  never matches), or an endpoint encoded (base32/hex) in a config value;
- a **new file type or language** enters the tree at Commit 2 (a `Dockerfile` with
  `RUN curl`, a `.ts`/`.vue` asset, a `Makefile` target) whose selector matches no
  family while its tokens also evade the per-language detector lists (which are
  python/shell/powershell/js/css/systemd-shaped);
- a **locked-SDK change**: `hyperliquid-python-sdk` at Commit 2 adds a second base
  URL constant or renames `TESTNET_API_URL`; the frozen constant→host mapping then
  verifies against a wheel that no longer matches the construction site;
- a **git alias/config** in-tree that turns a "local" git verb into a network one;
- a **new pip-style tool** invocation (`uv`, `pipx`) whose network semantics differ
  from the modeled `pip install` argument vector.

Follow-ups from the pattern doc (`SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:53-63`):

- *Where does the expected value come from?* The expected universe is the tree at
  `SOURCE_SHA` — an input the drafter does not control (it is Commit 2, after this
  draft). The matrix, however, came from the same snapshot the drafter grepped: the
  grounding and the expectation share an author, which is exactly why independent
  review of this draft is a precondition, not a courtesy.
- *What is outside the universe?* Everything the egress universe excludes by
  contract (`P9_15_PRODUCER_SPEC_2026-08-15.md:150`): untracked/ignored/history
  content, host state (pip index destination, NSS backend, UFW state), and runtime
  behavior — a static scan cannot see any of them, and the policy says so as
  limitations rather than implying coverage.
- *Enforced or asserted?* Enforced only once the producer exists and its
  falsification #3 ("add one unknown or nested network sink and prove `UNRESOLVED`
  plus STOP/3", `P9_15_PRODUCER_SPEC_2026-08-15.md:524`) runs against **this**
  matrix with a sink chosen by someone other than the drafter. Until then it is
  asserted-by-draft.

Standing sentence carried verbatim (`SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:75-77`):
**"State what would make this check fail, and show it failing."** For this draft
the showing must come from the independent review and the producer's RED runs; the
red worlds above are the concrete candidates a reviewer should aim at.

### 1.8 OWNER-CHOICE entries (do not silently pick)

| ID | Exact question | Draft default (marked in the JSON, not silently chosen) | Consequence if flipped |
|---|---|---|---|
| OWNER-CHOICE-1 | Must network-capable commands appearing only in operator documentation (`curl` to `127.0.0.1:8790` in `COMMANDS.md:220`; the `ssh -N -L` port-forward in `COMMANDS.md:233`; `Invoke-RestMethod` in `docs/17_DEPLOYMENT.md:58-59`) be modeled as potential activation paths with endpoint extraction, or remain documentation-class with a token census? | documentation-class with census — nothing in the program executes them and a static producer cannot observe operator execution | doc endpoints enter the catalog and doc files become `analyzed` rather than `not_executable_or_network_relevant` |
| OWNER-CHOICE-2 | Is host name-service resolution (`getent passwd`/`group`; NSS) a local non-network lookup, or must any NSS-backed lookup be treated as potentially network egress requiring host evidence? | local non-endpoint lookup, limitation `NSS_BACKEND_HOST_CONFIGURED`; `getent hosts`-family stays endpoint-bearing UNRESOLVED | `install.sh`/`verify.sh` `getent` rows become a named egress class with UNKNOWN destination pending host capture |

Both are open because the producer contract and its six-class seed are
program-path-centric and silent on exactly these two semantics
(`AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:105,109`; `SECURITY_BASELINE.md:96-108`).
The draft bytes carry `owner_choices` with these questions verbatim; a reviewer or
the Lead must resolve them before adoption.

### 1.9 UNKNOWN entries (no source establishes a value)

| ID | Value | What settles it |
|---|---|---|
| Package-index destination host | UNKNOWN | authorized Ubuntu capture of the host pip configuration — static analysis cannot resolve it (`SECURITY_BASELINE.md:35,100`) |
| Commit-2 universe | UNKNOWN | re-derivation over the `SOURCE_SHA` tree; any construct outside the matrix forces STOP until a policy revision (limitation `UNIVERSE_GROUNDED_AT_SNAPSHOT_c84497c8_RECHECK_AT_COMMIT2`) |
| SDK constant hosts at Commit 2 | UNKNOWN | verification of the frozen mapping against the hash-pinned SDK wheel actually locked at Commit 2 |
| Actual hits, counts, classes, rc | UNKNOWN | executing the frozen producer; the skeleton forbids filling them prospectively (`AUDIT2_PACKET9_SKELETON_2026-08-12.md:232-242`) |

## Part 2 — the mechanical `p9_15_policy.json` bytes

Production rule: the bytes below are produced from Part 1 by serializing the matrix
(endpoint catalog, language families, sweep detectors, conservation rules, stop
rules, owner choices, unknowns, limitations, derivation record) as canonical JSON
per the section-5 grammar — UTF-8 without BOM, LF-only, ASCII keys sorted by
unsigned UTF-8 bytes, no insignificant whitespace, exactly one terminal LF
(`P9_15_PRODUCER_SPEC_2026-08-15.md:195-197`). The single line in the fenced block
below **is** the exact byte content: the line plus its terminating LF.

**Honest execution disclosure:** the drafting session's permission gate denied
every command execution (python, git, pwsh) except the read-only file/search tools.
Two consequences, stated rather than papered over:

1. **The canonical serialization below was performed manually** from the matrix
   (every object's keys sorted by unsigned ASCII byte order, all insignificant
   whitespace removed, strings unchanged). The reviewer's first act must be to
   re-serialize the parsed document under the section-5 grammar and require
   byte-equality — any mismatch is a review finding against this draft, exactly as
   the verification recipe below specifies.
2. **No SHA-256 is recorded here, because none was computed.** Writing a
   hand-waved digest would fabricate an integrity value, which this repo treats as
   a hard defect class. The hash field is therefore left explicitly uncomputed with
   its one-line recipe; the independent reviewer (who has execution) computes it,
   and the Lead records the **adopted** policy's SHA-256 in the P9-06 pin after
   review — which precondition 3 requires anyway, and which will differ from this
   draft's hash because adoption changes at least the `draft_status` object.

```json
{"canonical_grammar":{"byte_grammar":"UTF-8 without BOM; LF only; no CR; exactly one terminal LF","json_grammar":"canonical form of P9_15_PRODUCER_SPEC_2026-08-15.md section 5: objects arrays strings non-negative integers true false null only; floats forbidden; ASCII keys sorted by unsigned UTF-8 bytes; no insignificant whitespace","policy_input_role":"data only, never executed"},"conservation_rules":{"file_level":"admitted egress-universe blobs equal analyzed plus not_executable_or_network_relevant plus unresolved, exactly one terminal disposition each (DESIGN_DEFECT_PATTERNS_2026-08-10.md:933-967)","row_level":"every resolved activation path yields exactly one EGRESS row; every policy-declared absence yields exactly one expected_absent row; zero facts never justify PASS (AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:126; P9_15_PRODUCER_SPEC_2026-08-15.md:290)","token_level":"per analyzed file: sweep-detector hits equal consumed-by-matrix plus censused-non-endpoint plus UNRESOLVED; a surplus or deficit is STOP/3/CONSERVATION_ERROR"},"derivation":{"drafted_utc_date":"2026-08-16","egress_universe_tracked_paths":131,"expected_binary_paths":["IBKR_PAPER_BRIDGE/docs/screenshots/overview.png","IBKR_PAPER_BRIDGE/docs/screenshots/trading.png"],"grounded_at":"repository snapshot c84497c8 detached clean worktree; read-only Glob and Grep over the tracked IBKR_PAPER_BRIDGE tree","normative_sources":["MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:47-51,99-109,126,147-164","MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/P9_15_PRODUCER_SPEC_2026-08-15.md:148-160,290,376-385,520-538","MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:899-967","MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:47-77","C:/tmp/lane_out/P9K_PACKET9_KICKOFF_REPAIR.md:71 dispatch precondition 3"],"secret_categories_note":"the nine sourced secret categories and their regexes live in the policy secret axis per P9_15_PRODUCER_SPEC_2026-08-15.md:156 and SECURITY_BASELINE.md:203-213; this grammar draft covers the EGRESS axis"},"draft_status":{"adopted":false,"adopted_bytes_note":"the adopted policy will differ at least in draft_status and any review fixes, so its SHA-256 can be recorded only after review and adoption","becomes_canonical_only_after":"independent review plus Lead adoption recorded in the P9-06/Commit-2 pin; until then these bytes are DRAFT-UNREVIEWED and a real producer PASS is unavailable","drafted_utc_date":"2026-08-16","draft_lane":"PL1"},"egress_classes":{"forbidden-unselected":"endpoint family the program may never activate; any activation path is FAIL EGRESS_POLICY_DEVIATION","install-time-only":"egress reachable only by the installer, never by the runtime","local-listener":"loopback-bound listener; not external outbound","runtime-optional":"outbound endpoints active only when an optional feature is enabled and its credentials resolve","runtime-required":"outbound endpoints the non-dry-run paper runtime requires","unused-setting-no-endpoint":"names settings and locked distributions with no runtime endpoint claim; absence of a client construct is the fact, not an endpoint"},"egress_universe":{"admitted":"every text_utf8 tracked blob at SOURCE_SHA below the prefix","cited":"P9_15_PRODUCER_SPEC_2026-08-15.md:148-150; AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:105","file_dispositions_terminal":"exactly one of analyzed / not_executable_or_network_relevant / unresolved per admitted blob","not_claimed":["worktree untracked content","ignored files","git history other than SOURCE_SHA","process environment","OS registry","credential stores","shell history","remote hosts"],"path_prefix":"IBKR_PAPER_BRIDGE/"},"endpoint_catalog":{"127.0.0.1:8790":{"activation_predicate":"bridge.app executed via python -m bridge.app (systemd ExecStart at deploy/linux/systemd/mtc-bridge-first-start.service.template:34 and mtc-bridge-steady.service.template:37; tools/run_bridge_p2.ps1:13) or direct module run","citations":["IBKR_PAPER_BRIDGE/bridge/app.py:234","IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:101"],"credential_names":[],"endpoint_extractor":"uvicorn.run literal host and port at bridge/app.py:234; config server.host and server.port at config/bridge.yaml:51-53; browser side is same-origin window.location.host at bridge/static/app.js:24,239-240; loopback assertion helpers at deploy/linux/lib/common.sh:30,182-206","egress_class":"local-listener","port":8790,"protocols":["HTTP","WS"]},"HOST_CONFIGURED_PYTHON_INDEX":{"activation_predicate":"install.sh venv-creation branch executes with WHEELHOUSE unset; a set WHEELHOUSE adds --no-index --find-links and is fully offline (install.sh:299-303)","citations":["IBKR_PAPER_BRIDGE/deploy/linux/install.sh:292-306","IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:100"],"credential_names":[],"destination_host":"UNKNOWN: host-configured pip index; static analysis cannot resolve it","endpoint_extractor":"pip install argument vector in deploy/linux/install.sh:292-306; the destination lives in host pip configuration, not in a repository token","egress_class":"install-time-only","port":443,"protocols":["HTTPS"]},"NONE:ANTHROPIC_XAI_UNUSED":{"activation_predicate":"none at snapshot c84497c8; any anthropic or xai client import or construction appearing at SOURCE_SHA is a construct outside this entry and MUST be UNRESOLVED until a policy revision adds it","citations":["IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:103","IBKR_PAPER_BRIDGE/bridge/settings.py:34-35"],"credential_names":["ANTHROPIC_API_KEY","XAI_API_KEY"],"endpoint_extractor":"none: settings names exist and anthropic==0.120.0 is locked (requirements.lock:11) but no runtime client import or construction exists in first-party code; NullLLMGate never calls external APIs (bridge/engine/llm_gate.py:22-26) and both llm switches are false (config/bridge.yaml:39-50)","egress_class":"unused-setting-no-endpoint","port":null,"protocols":[]},"api.hyperliquid-testnet.xyz":{"activation_predicate":"HyperliquidBroker constructed with network=testnet and owned clients (bridge/broker/hyperliquid.py:1954-1966), reached from python -m bridge.app with dry_run false (bridge/app.py:113-114,191-208,234) or from tools/smoke_p0.py:47-53, tools/smoke_fill.py:67, tools/probe_user_events.py:31; requires HL_ACCOUNT_ADDRESS and HL_API_WALLET_KEY to resolve via env or HKCU registry (bridge/settings.py:73-117); dry_run uses MockBroker and does not activate","citations":["IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:98","IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py:1954-1966","IBKR_PAPER_BRIDGE/bridge/app.py:191-208"],"credential_names":["HL_ACCOUNT_ADDRESS","HL_API_WALLET_KEY"],"endpoint_extractor":"constructor argument base_url = constants.TESTNET_API_URL on Info(base_url, skip_ws=False) and Exchange(wallet, base_url); frozen symbolic-constant mapping in this policy; the child MUST verify the mapping against the locked hyperliquid-python-sdk wheel before interpreting subjects","egress_class":"runtime-required","port":443,"protocols":["HTTPS","WSS"],"sdk_constant":"constants.TESTNET_API_URL","sdk_constant_verification":"requirements.lock:601 pins hyperliquid-python-sdk==0.24.0 with artifact hashes; a constant-to-host mismatch is STOP/3/ARTIFACT_IDENTITY_MISMATCH"},"api.hyperliquid.xyz":{"activation_predicate":"NONE PERMITTED: mainnet requires the triple lock (bridge/broker/hyperliquid.py:1948-1952) and every first-party construction site supplies network=testnet only; the dormant SDK branch without an activating construction site yields an expected_absent row; an activating mainnet path is FAIL EGRESS_POLICY_DEVIATION","citations":["IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:102","IBKR_PAPER_BRIDGE/bridge/app.py:202-208"],"credential_names":[],"endpoint_extractor":"constants.MAINNET_API_URL branch of the same constructor expression (bridge/broker/hyperliquid.py:1962)","egress_class":"forbidden-unselected","port":443,"protocols":["HTTPS","WSS"]},"api.telegram.org":{"activation_predicate":"build_notifier(enabled=true) with both TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID resolving via env or HKCU registry (bridge/engine/notify.py:50-58; bridge/settings.py:142-145); config notify.telegram_enabled=true (config/bridge.yaml:36-38); failure is swallowed and never gates trading","citations":["IBKR_PAPER_BRIDGE/bridge/engine/notify.py:13,40-58","IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:99"],"credential_names":["TELEGRAM_BOT_TOKEN","TELEGRAM_CHAT_ID"],"endpoint_extractor":"URL f-string literal in bridge/engine/notify.py:41; record scheme and host ONLY; the path embeds the bot token and MUST NOT be recorded under the content-redaction rule","egress_class":"runtime-optional","port":443,"protocols":["HTTPS"]}},"expected_absent":["python direct socket ssl requests urllib http.client aiohttp websockets-client usage in first-party runtime code","python smtplib telnetlib ftplib imaplib poplib and DNS-resolution calls","asyncio.open_connection and asyncio.start_server in first-party code","shell curl wget ssh scp nc socat ping dig in executable deploy scripts","powershell network cmdlets in tools ps1","css url() and @import","systemd IPAddress or Listen network directives","mainnet activating construction site; the dormant api.hyperliquid.xyz branch is the expected state","HL_LIVE_ACK value anywhere in the tracked tree","getent hosts ahosts networks endpoint-bearing lookups","git network verbs in executable scripts"],"file_dispositions":{"analyzed":"executable or configuration file whose every network-capable token was consumed by a language_families rule or emitted as UNRESOLVED","not_executable_or_network_relevant":"documentation and data blobs that no program path executes; endpoint-like tokens are censused, never silently dropped","not_in_egress_universe":"text blobs outside IBKR_PAPER_BRIDGE/ (universe.jsonl only)","unresolved":"file containing an unconsumed network-capable token or unsupported form; forces STOP/3/POLICY_COVERAGE_INCOMPLETE"},"forbidden":{"bind_addresses":["0.0.0.0","::"],"bind_assertions":"IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:182-189","disposition":"an observed activating occurrence is FAIL/1/EGRESS_POLICY_DEVIATION; an unconsumed token is STOP/3/POLICY_COVERAGE_INCOMPLETE","env_value_with_definition":"deploy/linux/env/mtc-bridge.env.template must carry names and comments only","git_network_verbs":["clone","fetch","pull","push","ls-remote","remote","submodule"],"hl_live_ack":"HL_LIVE_ACK presence in the env file or unit is forbidden (deploy/linux/env/mtc-bridge.env.template:31-38; deploy/linux/verify.sh:141)"},"key_policy":{"closed":true,"known_top_level_keys":["canonical_grammar","conservation_rules","derivation","draft_status","egress_classes","egress_universe","endpoint_catalog","expected_absent","file_dispositions","forbidden","key_policy","language_families","limitations","non_endpoint_uri","owner_choices","schema","stop_rules","sweep_detector","unknowns"],"unknown_key_disposition":"STOP/3/POLICY_INVALID per P9_15_PRODUCER_SPEC_2026-08-15.md:376"},"language_families":[{"executable":true,"id":"python-runtime","outside_matrix":"any other network-capable import or call (socket, ssl, requests, urllib, http.client, aiohttp, websockets client, asyncio.open_connection, asyncio.start_server, smtplib, telnetlib, ftplib, imaplib, poplib, DNS resolution, subprocess to a network command) is UNRESOLVED and forces STOP/3/POLICY_COVERAGE_INCOMPLETE","recognized_tokens":[{"disposition":"endpoint_catalog entry of the constructed client","extractor":"marks the owning module as SDK-client-bearing; endpoint comes from the constructor argument","token":"from hyperliquid.exchange import Exchange / from hyperliquid.info import Info / from hyperliquid.utils import constants / from hyperliquid.utils.types import Cloid"},{"disposition":"client constructor; resolve to endpoint_catalog","extractor":"base_url argument; skip_ws argument toggles WSS","token":"Info("},{"disposition":"client constructor; resolve to endpoint_catalog","extractor":"base_url argument","token":"Exchange("},{"disposition":"testnet maps to runtime-required; mainnet maps to forbidden-unselected","extractor":"frozen sdk_constant mapping in endpoint_catalog, verified against the locked wheel","token":"constants.TESTNET_API_URL / constants.MAINNET_API_URL"},{"disposition":"same class as owning client (bridge/broker/hyperliquid.py:274-311; bridge/engine/bars.py:124)","extractor":"inherits the owning client base_url; WSS","token":".subscribe( on an SDK Info client incl. subscribe_bars / subscribe_user_events"},{"disposition":"same class as owning client","extractor":"inherits owning client base_url; HTTPS","token":"self.info.<method> / self.exchange.<method> REST calls"},{"disposition":"endpoint_catalog api.telegram.org runtime-optional (bridge/engine/notify.py:13,41,44-45)","extractor":"first positional or f-string URL argument; record scheme and host only","token":"import httpx / httpx.AsyncClient( / client.post("},{"disposition":"local-listener; a non-loopback host token is forbidden","extractor":"host and port keyword literals","token":"uvicorn.run("},{"disposition":"declaration consumed as local origins (bridge/app.py:100)","extractor":"URL literals in the list","token":"allow_origins=["},{"disposition":"local-listener surface (bridge/api/routes.py:21-61; bridge/api/ws.py:17-49)","extractor":"serves on the owning app listener","token":"@app.get / @app.post / @app.put / @app.websocket / websocket.accept("},{"disposition":"consumed LOCAL_SIGNING_NO_ENDPOINT","extractor":"none: local signing","token":"from eth_account import Account"},{"disposition":"consumed CREDENTIAL_SOURCE_READ (bridge/settings.py:96-108)","extractor":"none: local credential-source read, names only","token":"import winreg / QueryValueEx("},{"disposition":"resolve to endpoint_catalog; an uncatalogued host in runtime code is UNRESOLVED","extractor":"scheme host and optional port","token":"URL string literal"},{"disposition":"credential_names of the relevant class","extractor":"record name only, never a value","token":"credential env-name tokens"}],"selector":["IBKR_PAPER_BRIDGE/bridge/**/*.py","IBKR_PAPER_BRIDGE/tools/**/*.py"]},{"executable":true,"id":"python-tests","outside_matrix":"a test constructing an SDK client with a non-testnet base_url, or shelling to curl wget or ssh, is UNRESOLVED","recognized_tokens":[{"disposition":"consumed TEST_FIXTURE_INERT with the host recorded; never an EGRESS row","extractor":"scheme and host","token":"URL string literal in fixture data (tests/test_llm_gate.py:33)"},{"disposition":"recursive dispatch (tests/test_linux_deployment.py:67-79; tests/test_order_state.py:516-523; tests/test_release_evidence.py:229-241; tests/test_runtime_baseline.py:26-32; tools/check_runtime_baseline.py:71-86)","extractor":"argv dispatch: sys.executable or python maps to python grammar recursion; git maps to the git verb table; bash -c maps to shell-deploy grammar recursion; any other argv0 is UNRESOLVED","token":"subprocess.run( / subprocess.Popen( / os.system"},{"disposition":"consumed TEST_HELPER_IMPORT (tests/test_hyperliquid_broker.py:20-22)","extractor":"type and wire helpers only; no client construction with a live base_url","token":"import hyperliquid.* in tests"}],"selector":["IBKR_PAPER_BRIDGE/tests/**/*.py"]},{"executable":true,"id":"shell-deploy","outside_matrix":"curl, wget, ssh, scp, sftp, rsync, nc, ncat, socat, telnet, ftp, ping, dig, nslookup, host, /dev/tcp redirections, or any unknown command in an executable shell file are UNRESOLVED and force STOP; zero occur at c84497c8","recognized_tokens":[{"disposition":"install-time-only (install.sh:292-306)","extractor":"destination HOST_CONFIGURED_PYTHON_INDEX; wheelhouse adds --no-index --find-links and removes the endpoint","token":"pip install --require-hashes --no-deps --only-binary=:all: --no-input --no-cache-dir --disable-pip-version-check -r <lock>"},{"disposition":"consumed NAME_SERVICE_LOCAL (install.sh:134,200-225; verify.sh:37,55-58); any getent hosts ahosts or networks form is endpoint-bearing and UNRESOLVED (DESIGN_DEFECT_PATTERNS_2026-08-10.md:914-915)","extractor":"endpointless local NSS lookup; the NSS backend is host-configured","token":"getent passwd / getent group"},{"disposition":"consumed LOCAL_GIT; git network verbs are forbidden (package.sh:50,60-74)","extractor":"none: local object operations","token":"git rev-parse / cat-file / archive / status local verbs"},{"disposition":"consumed LOCAL_FIREWALL_ASSERTION (common.sh:153-179)","extractor":"none","token":"ufw status verbose read-only"},{"disposition":"consumed LOCAL_LISTENER_ASSERTION (common.sh:195-206)","extractor":"local listener enumeration","token":"ss -H -ltn"},{"disposition":"consumed LOCAL_SERVICE_MANAGER (verify.sh:207-213; rollback.sh:81)","extractor":"local service manager IPC","token":"systemctl is-active / is-enabled / start / stop / mask"},{"disposition":"consumed LOCAL_TOOLS (verify.sh:37; install.sh:134)","extractor":"none","token":"require_cmd list stat find systemctl sha256sum sed cmp sort awk mktemp getent id pgrep"}],"selector":["IBKR_PAPER_BRIDGE/deploy/linux/**/*.sh"]},{"executable":true,"id":"powershell-tools","outside_matrix":"Invoke-WebRequest, Invoke-RestMethod, Net.WebClient, Invoke-Expression, Start-Process of a network binary, or any network cmdlet in an executable ps1 is UNRESOLVED; zero occur at c84497c8","recognized_tokens":[{"disposition":"consumed PROCESS_LAUNCH_ACTIVATION (tools/run_bridge_p2.ps1:13)","extractor":"process launch maps to python-runtime activation of the local listener and, when not dry-run, the testnet endpoint","token":"call operator invoking python -m bridge.app"},{"disposition":"consumed LOCAL_TOOLS","extractor":"none","token":"New-Item / Set-Location / Get-Date / Out-File / Start-Sleep"}],"selector":["IBKR_PAPER_BRIDGE/tools/*.ps1"]},{"executable":true,"id":"javascript-static","outside_matrix":"XMLHttpRequest, EventSource, sendBeacon, axios, or an absolute external URL is UNRESOLVED unless it resolves to an endpoint_catalog entry; zero occur at c84497c8","recognized_tokens":[{"disposition":"local-listener (app.js:24); an absolute-URL fetch argument resolves via the URL extractor","extractor":"same-origin: destination is the serving origin 127.0.0.1:8790","token":"fetch(relative path)"},{"disposition":"local-listener (app.js:239-240)","extractor":"same-origin WSS or WS to the serving origin","token":"new WebSocket with scheme and window.location.host"},{"disposition":"consumed NON_ENDPOINT_URI (app.js:194-213)","extractor":"non_endpoint_uri.namespaces","token":"document.createElementNS(namespace URI)"}],"selector":["IBKR_PAPER_BRIDGE/bridge/static/*.js"]},{"executable":true,"id":"html-static","outside_matrix":"inline script with network calls dispatches to javascript-static; any other network form is UNRESOLVED","recognized_tokens":[{"disposition":"local-listener (index.html:7,108); an external absolute reference is UNRESOLVED","extractor":"relative maps to same-origin local; absolute maps to scheme and host","token":"src= / href= attribute values"}],"selector":["IBKR_PAPER_BRIDGE/bridge/static/*.html"]},{"executable":true,"id":"css-static","outside_matrix":"any other network-capable CSS form is UNRESOLVED","recognized_tokens":[{"disposition":"expected_absent at c84497c8; an occurrence resolves to endpoint_catalog or is UNRESOLVED","extractor":"relative maps to same-origin; absolute maps to scheme and host","token":"url( and @import"}],"selector":["IBKR_PAPER_BRIDGE/bridge/static/*.css"]},{"executable":true,"id":"yaml-config","outside_matrix":"any other endpoint- or credential-bearing key is UNRESOLVED; config/strategies/keltner_trail_ema8.yaml contains no network keys at c84497c8","recognized_tokens":[{"disposition":"testnet maps to runtime-required; mainnet maps to forbidden-unselected (bridge.yaml:2-3)","extractor":"value selects the endpoint_catalog SDK branch","token":"broker.network"},{"disposition":"local-listener and must equal 127.0.0.1 and 8790 (bridge.yaml:51-53); any other host is forbidden-unselected","extractor":"listener declaration","token":"server.host / server.port"},{"disposition":"runtime-optional (bridge.yaml:36-38)","extractor":"activation input for api.telegram.org","token":"notify.telegram_enabled"},{"disposition":"unused-setting-no-endpoint (bridge.yaml:39-50); true with no modeled client is UNRESOLVED","extractor":"must be false while no provider client construct exists","token":"llm.regime_enabled / llm.veto_enabled"},{"disposition":"resolve to endpoint_catalog or UNRESOLVED","extractor":"scheme and host","token":"any URL-valued key"}],"selector":["IBKR_PAPER_BRIDGE/config/**/*.yaml"]},{"executable":true,"id":"systemd-unit-template","outside_matrix":"IPAddressAllow, IPAddressDeny, ListenStream, socket-unit forms, or any network-bearing directive not listed is UNRESOLVED; zero occur at c84497c8","recognized_tokens":[{"disposition":"activation path for local-listener and testnet (mtc-bridge-first-start.service.template:34; mtc-bridge-steady.service.template:37)","extractor":"command line dispatched to the owning grammar (venv python -m bridge.app)","token":"ExecStart="},{"disposition":"names only; HL_LIVE_ACK presence forbidden (first-start:37-43; steady:39-42)","extractor":"credential name source","token":"Environment= / EnvironmentFile="},{"disposition":"consumed DECLARATION_NO_ENDPOINT with limitation DESTINATION_CONTROL_DEFERRED_HOST (first-start:78; steady:75; deploy/linux/README.md:128)","extractor":"socket-family declaration; restricts families, not destinations","token":"RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX"},{"disposition":"consumed NON_ENDPOINT_URI (first-start:23; steady:26)","extractor":"non_endpoint_uri.schemes","token":"Documentation=file reference"}],"selector":["IBKR_PAPER_BRIDGE/deploy/linux/systemd/*.template"]},{"executable":true,"id":"env-template","outside_matrix":"any other variable or value form is UNRESOLVED","recognized_tokens":[{"disposition":"credential names of their classes; any NAME=value definition is forbidden (mtc-bridge.env.template:1-38)","extractor":"names only","token":"credential variable names in comments"}],"selector":["IBKR_PAPER_BRIDGE/deploy/linux/env/*.template"]},{"executable":false,"id":"docs-and-data","note":"docs/audits/AUDIT_DeepSeek_V4_Pro_2026-07-05.md:77 mentions smtplib only as a rejected future idea; docs json logs carry no endpoint tokens at c84497c8","outside_matrix":"nothing in this family can activate; OWNER-CHOICE-1 asks whether operator-documentation commands must additionally be modeled as activation paths","recognized_tokens":[{"disposition":"not_executable_or_network_relevant with reason DOCUMENTATION_OR_DATA_NOT_EXECUTABLE; the census makes the tokens visible rather than silently dropped (COMMANDS.md:219-233; docs/17_DEPLOYMENT.md:58-59; docs/06_HYPERLIQUID_SETUP.md:28; README.md:51)","extractor":"census record only: token kind plus path; never an EGRESS row","token":"endpoint-like tokens: URLs, host:port pairs, command names such as curl or ssh in operator examples"}],"selector":["IBKR_PAPER_BRIDGE/docs/**","IBKR_PAPER_BRIDGE/README.md","IBKR_PAPER_BRIDGE/**/*.md","IBKR_PAPER_BRIDGE/**/*.json","IBKR_PAPER_BRIDGE/**/*.csv","IBKR_PAPER_BRIDGE/requirements.in","IBKR_PAPER_BRIDGE/requirements.lock","IBKR_PAPER_BRIDGE/requirements.txt","IBKR_PAPER_BRIDGE/deploy/linux/logrotate/*"]},{"executable":false,"id":"binary-excluded","outside_matrix":"binary blobs are counted and hashed, never egress-analyzed (universe content_class binary)","recognized_tokens":[],"selector":["IBKR_PAPER_BRIDGE/docs/screenshots/*.png"]}],"limitations":["STATIC_ONLY_NO_RUNTIME_CAPTURE","DESTINATION_CONTROL_DEFERRED_HOST","NSS_BACKEND_HOST_CONFIGURED","DOC_COMMANDS_NOT_ACTIVATION_OWNER_CHOICE_1","GETENT_CLASSING_OWNER_CHOICE_2","SDK_CONSTANT_MAPPING_TO_VERIFY_AT_COMMIT2","UNIVERSE_GROUNDED_AT_SNAPSHOT_c84497c8_RECHECK_AT_COMMIT2","SEED_CLASSES_ARE_LABELS_NOT_RESULTS","SWEEP_DETECTOR_CLOSED_LIST_IS_DRAFT_SEAM"],"non_endpoint_uri":{"namespaces":["http://www.w3.org/2000/svg"],"rule":"these URI literals are identifiers or local references, not fetch targets; they are consumed with reason NON_ENDPOINT_URI and never produce EGRESS rows; any other bare URI in executable code is endpoint-bearing until modeled","schemes":["file"]},"owner_choices":[{"consequence_if_flipped":"the doc endpoints enter endpoint_catalog and doc files become analyzed rather than not_executable_or_network_relevant","draft_default":"documentation-class with census; nothing in the program executes them and the static producer cannot observe operator execution","id":"OWNER-CHOICE-1","question":"Must network-capable commands that appear only in operator documentation (curl to 127.0.0.1:8790 in COMMANDS.md:220, the ssh port-forward in COMMANDS.md:233, Invoke-RestMethod in docs/17_DEPLOYMENT.md:58-59) be modeled as potential activation paths with endpoint extraction, or remain documentation-class with a token census?","why_open":"the producer contract and its six-class seed cover program paths only and are silent on documentation commands (AUDIT2_PACKET9_PRODUCER_CONTRACT_2026-08-15.md:105,109)"},{"consequence_if_flipped":"install.sh and verify.sh getent rows become a named egress class with UNKNOWN destination pending host capture","draft_default":"local non-endpoint lookup with declared limitation NSS_BACKEND_HOST_CONFIGURED; getent hosts-family remains endpoint-bearing UNRESOLVED","id":"OWNER-CHOICE-2","question":"Is host name-service resolution (getent passwd group; NSS) classed as a local non-network lookup, or must any NSS-backed lookup be treated as potentially network egress requiring host evidence?","why_open":"the NSS backend is host state invisible to a static scan; the baseline does not class it (SECURITY_BASELINE.md:96-108)"}],"schema":"p9-15-policy/v1","stop_rules":{"observed_forbidden_or_unexpected_activation":"FAIL/1/EGRESS_POLICY_DEVIATION (P9_15_PRODUCER_SPEC_2026-08-15.md:385)","sdk_constant_mapping_mismatch":"STOP/3/ARTIFACT_IDENTITY_MISMATCH","unconsumed_network_capable_token":"STOP/3/POLICY_COVERAGE_INCOMPLETE (P9_15_PRODUCER_SPEC_2026-08-15.md:379)","unknown_policy_key_or_noncanonical_policy":"STOP/3/POLICY_INVALID (P9_15_PRODUCER_SPEC_2026-08-15.md:376)","unsupported_nested_form_or_option":"STOP/3/POLICY_COVERAGE_INCOMPLETE (DESIGN_DEFECT_PATTERNS_2026-08-10.md:919-929)"},"sweep_detector":{"detectors":{"css_network_forms":["url(","@import"],"host_port_patterns":["[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}:[0-9]{1,5}","localhost:[0-9]{1,5}"],"js_network_apis":["WebSocket","fetch(","XMLHttpRequest","EventSource","sendBeacon","axios"],"powershell_network_cmdlets":["Invoke-WebRequest","Invoke-RestMethod","Net.WebClient","Invoke-Expression"],"python_network_calls":["asyncio.open_connection","asyncio.start_server","create_connection","getaddrinfo","gethostbyname","urlopen","websockets.connect","socket.socket"],"python_network_imports":["aiohttp","ftplib","http.client","http.server","imaplib","nntplib","paramiko","poplib","requests","socket","socketserver","smtplib","ssl","telnetlib","urllib.request","urllib3","websockets","xmlrpc.client"],"shell_network_commands":["curl","wget","ssh","scp","sftp","rsync","nc","ncat","netcat","socat","telnet","ftp","ping","dig","nslookup","getent","openssl"],"systemd_network_directives":["IPAddressAllow","IPAddressDeny","ListenStream","RestrictAddressFamilies"],"url_regex":"https?://[A-Za-z0-9._:/~?=&%#-]+","ws_regex":"wss?://[A-Za-z0-9._:/~?=&%#-]+"},"honesty":"this detector list is itself a closed list drafted by the same author as the matrix; a construct outside BOTH the matrix and this list passes silently. Reviewers must attack exactly this seam; see limitations","purpose":"family-independent conservation sweep: in every analyzed file, the count of hits from these detectors MUST equal modeled-consumed tokens plus UNRESOLVED tokens; any surplus hit is itself UNRESOLVED. This makes silence impossible: a modeled file with zero EGRESS rows still proves it swept and consumed or censused every token"},"unknowns":[{"id":"package-index-destination-host","settled_by":"authorized Ubuntu capture of the host pip configuration; static analysis cannot resolve it","value":"UNKNOWN"},{"id":"commit2-universe","settled_by":"re-derivation over the SOURCE_SHA tree; this policy is grounded at snapshot c84497c8 and any Commit-2 construct outside the matrix forces STOP until a policy revision","value":"UNKNOWN"},{"id":"sdk-constant-hosts-at-commit2","settled_by":"verification of the frozen mapping against the hash-pinned hyperliquid-python-sdk wheel actually locked at Commit 2","value":"UNKNOWN"},{"id":"actual-hits-and-counts","settled_by":"executing the frozen producer; the skeleton forbids filling them prospectively (AUDIT2_PACKET9_SKELETON_2026-08-12.md:232-242)","value":"UNKNOWN"}]}
```

**SHA-256: NOT COMPUTED IN THIS SESSION (execution denied by the session permission
gate).** Recording a hand-waved digest would fabricate an integrity value, so the
field is left honestly empty. Recipe for the reviewer, who has execution — extract
the fenced block's single line as bytes plus one LF and hash it:

```text
python -c "import hashlib,sys;b=open('<extracted_policy_line_file>','rb').read();print(len(b),hashlib.sha256(b).hexdigest())"
```

Byte length is likewise left uncounted for the same reason; the recipe above prints
it as its first field.

### Verification recipe for the independent reviewer

1. Extract the fenced `json` block's single line as bytes, append one LF, and
   compute SHA-256 with the recipe above; record it in the review as the DRAFT hash.
2. `json.loads` those bytes; require `sorted(keys)` to equal the declared
   `key_policy.known_top_level_keys` (19 keys, listed above in sorted order).
3. Re-serialize the parsed document with sorted keys and no insignificant
   whitespace and require **byte-equality** with the extracted line — this is the
   check that catches any manual-serialization slip in this draft (see the honest
   execution disclosure above; a mismatch is a review finding, not a reviewer chore).
4. Cross-check the matrix tables of Part 1 against the JSON semantically (families,
   catalog entries, detector lists, owner choices, unknowns, limitations).
5. Attack the declared seam: try to name a network-capable construct that evades
   BOTH the matrix and `sweep_detector.detectors` (§1.7 lists the candidate worlds).

### Status of these bytes

These bytes are **DRAFT-UNREVIEWED**. They become canonical only after independent
review and Lead adoption, recorded with reviewer identity and the adopted SHA-256
in the P9-06/Commit-2 pin, exactly as precondition 3 demands
(`C:\tmp\lane_out\P9K_PACKET9_KICKOFF_REPAIR.md:71`). The adopted policy will
differ from this draft at least in the `draft_status` object (and in whatever the
review fixes), so its SHA-256 can only be recorded after that review; until then
the spec's boundary holds — the final egress policy grammar bytes are UNKNOWN and
a real producer PASS is unavailable (`P9_15_PRODUCER_SPEC_2026-08-15.md:533`).
No part of this draft may be cited as a P9-15 result, as coverage evidence, or as
the canonical policy.

## Boundary statement

This lane drafted policy **data** only. It did not implement the producer, did not
run any scan as production evidence, did not execute, authorize, or simulate any
host, network, SSH, deployment, service, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, merge, push, or economic action, and
does not claim the policy is canonical or that Packet 9 exists. Repository access
was read-only (Glob/Grep on the clean snapshot worktree at `c84497c8`); no git
status/add/commit/amend/push was run, and the only file written is this one.
