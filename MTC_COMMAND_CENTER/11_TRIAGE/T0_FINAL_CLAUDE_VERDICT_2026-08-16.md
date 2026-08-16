# FINAL T0 verdict (round 4, the final round) — Plan V6 + command annex + launcher v4 + candidate `acdf4e37` — Claude slot

| Field | Value |
|---|---|
| Reviewer slot | Claude — one of the two final T0 flagships, **round 4 (FINAL)** under the owner's round-4 override |
| Model identity (runtime-reported) | `claude-opus-5` — "Opus 5", Claude 5 family |
| Effort | `xhigh` as configured by the dispatching route. **In-session introspection of the effort setting is not possible**; I applied no lower-effort override. Same caveat of record as rounds 1–3. |
| Session | Fresh, independent, adversarial; no state carried from my round-1/2/3 sessions beyond the two published round-3 verdicts I was told to verify |
| Working directory | `C:\AUD62D` |
| Start (UTC+3) | 2026-08-16 16:37:41 |
| Stop (UTC+3) | 2026-08-16 16:59:29 |
| Materiality standard applied | `OWNER_DECISION_ROUND4_FINAL_2026-08-16.md`, read first, verbatim in force |
| **VERDICT** | **REQUEST_CHANGES — 1 REQUIRED, 9 DISCLOSED-FOLLOW-UP, 0 blocking NIT** |

## Subject pins — start and end

| # | Subject | Required pin | Start | End |
|---|---|---|---|---|
| 1 | `KVM2_DEPLOYMENT_PLAN_V6_2026-08-16.md` | 6207 B / `f433d35a…0df0ba8f` | 6207 B / `f433d35ae9516c2a94304f5459fba442209269ee034116b5634fbb320df0ba8f` ✅ | identical ✅ |
| 2 | `KVM2_PLAN_V6_COMMAND_ANNEX_2026-08-16.md` | 31283 B / `8cb02ff7…5f0e5fce` | 31283 B / `8cb02ff7fa13eb7e0ac602cfe0f1854b615cb079535ff91385e6c18efc5e5fce` ✅ | identical ✅ |
| 3 | `KVM2_RUNKIT/Open-BridgeDashboard.ps1` (v4) | 9277 B / `ac68196b…ebf2a1b5` | 9277 B / `ac68196b4ae99e12892898c0a5bfb2d7d2249fc2bb476619a4c2bdaaebf2a1b5` ✅ | identical ✅ |
| 4 | Candidate commit | `acdf4e37…`, parent `a7460784…` | HEAD `acdf4e379fb60ee319854acae19fd3eaf7db71a2`, parent `a7460784c1563c140ee7c75197aeab2b0170da8a` ✅, tip of `integration/bridge-release-20260815` (local + `origin/`), `git status --porcelain` empty ✅ | identical, still clean ✅ |

**All four pins matched at start and at end. No STOP condition occurred.**

The pinned launcher is byte-identical to the implementer's produced artifact:
`C:\tmp\lane_out\Open-BridgeDashboard_v4.ps1` and `…\KVM2_RUNKIT\Open-BridgeDashboard.ps1`
both hash `ac68196b…ebf2a1b5`.

### Exclusions honoured

Read-only everywhere except this file plus disposable scratch **outside any repo**
(`…\scratchpad\t0final\{ufw,meta,repo,r6,fences}`). **No launcher execution — I never
dot-sourced or ran `Open-BridgeDashboard.ps1`; I extracted its shipped regex literal
by text match and exercised that. No ssh or scp invocation of any kind, not even a
non-connecting `ssh -G`. No host or network contact. No git mutation anywhere. No
identity-key read. No sub-delegation.** `C:\LAB\Tradingview_LAB_CLEAN` untouched;
`C:\R7FINAL` and `C:\tmp\payload-acdf4e37` read only. The repository worktree was
clean at start, immediately after the full suite, and at the final pin.

---

## Required check 1 — eight-finding closure, verified on mechanism

I re-ran every round-3 attack against the **real candidate bytes** rather than reading
`RIC3_REPAIR_REPORT_2026-08-16.md`.

| # | Round-3 finding | Attack I re-ran | Real result | Closure |
|---|---|---|---|---|
| **Codex R1a** | dry-run manifest arm accepts a direct unwrapped mutator | Codex's exact `install -d -o root -g root -m 0755 /opt/codex-unlisted-direct`, no `run`/`run_action`, no manifest row | **1 failed, rc 1** | **CLOSED** |
| **Codex R1b** | verifier read-only arm accepts a child-interpreter write | Codex's exact `python3.12 -c '…Path("/tmp/codex-verifier-python").write_text("mutation")'` in `verify.sh` | **1 failed, rc 1** | **CLOSED** |
| **Codex R2** | UFW parser exempts the `OpenSSH` application profile | `OpenSSH ALLOW IN Anywhere` + `80/tcp` (Codex's exact fixture, and again as the only rule) | **rc 1** — `unmodelled inbound rule or application profile` | **CLOSED** |
| **Codex R3** | verifier admits `0777` / `1000:1000` on root-executed logrotate assets | byte-identical accepted bytes, my own `stat` stub returning `777` + `1000:1000`, driving the **real** section-8 block extracted from the shipped `verify.sh` | **`MTC_FAILURES=2`**, `mode 777, expected 644` / `expected 755`; the `cmp` never runs | **CLOSED** |
| **Codex R4** | launcher fingerprint suppliable from a wrong key's comment | Codex's exact spoof row `256 SHA256:AAA…A wrong-key-comment-SHA256:8b6bl/…HBC8 (ED25519)` through v4's shipped regex | fingerprints = `[SHA256:AAA…A]` only; `-notcontains` true → **Fail, dashboard not opened** | **CLOSED** |
| **Codex R5** | "exact executable command set" incomplete / unsafe | option-set audit of all three native `scp`/`ssh` invocations; ellipsis grep; stage-3 command presence | 3/3 invocations carry the complete isolated set + rc STOP guard; **zero** Unicode ellipses in the annex; stages 3.3–3.5 all have literal commands and rc/stderr rules | **CLOSED** |
| **Codex R6** / **Claude R2** | rehearsal input cannot exist on a never-started install | built the annex's exact tar + `sha256sum` artifacts against a simulated never-started state (`bridge.db` absent), then drove `rollback.sh`'s real lines 38–62 | **accepted, rc 0**; the round-3 defect (`bundle_manifest.json`) reproduces as `state manifest file is missing`, rc 1; wrong sha → `hash does not match`, rc 1 | **CLOSED** |
| **Codex R7** | §3 permits self-confirming "zero side effects" evidence | read the annex's R7 contract against each of Codex's seven demands | literal commands ✓, rc+stderr adjudicated before comparison ✓, STOP on missing DB/table/tool/unmodelled WAL ✓, rule bound to resolved numeric UID ✓, active-rule proof + lost-counter equality across the delimited window ✓, every result attributed ✓, exact rule removal by trap ✓ | **CLOSED** (D3-only; residuals → DFU-3) |
| **Codex R8** | authorization/removal boundary not self-contained, omits the cron asset | compared Plan V6 §3's object clause against the annex's complete R8 admitted list and its removal commands | annex enumeration and removal list are **complete**; **§3's clause is not** | **PARTIALLY CLOSED → REQUIRED-1** |
| **Claude R1** | `assert_ufw_bridge_safe` passes a `LIMIT` rule on 8790 | my exact round-3 fixture `8790/tcp LIMIT IN Anywhere` | **rc 1** — `ufw exposes Bridge port 8790` | **CLOSED** |

**9 of the 10 addressed findings are CLOSED on mechanism. One (Codex R8) is partially
closed.** None regressed. My round-3 NIT-1 (bare `mkdir -p /opt/hermes`, bare
`install -d`, `eval`-wrapped mutator) and NIT-3 (`python3 -c 'open(…,"w")'`) — which I
graded optional in round 3 — are also now **RED**, all five reproduced by me.

`RIC3_REPAIR_REPORT_2026-08-16.md`'s RED/GREEN claims are consistent with everything I
measured independently, and its `1376 passed, 1 warning` matches my own run. **I found
no overstatement in that report.**

### Owner repair-scope item 2 (honesty of the D026 claim) — satisfied

The README delta states the fences are "closed controls over the shipped scripts'
modeled statement grammar, **not a claim to understand arbitrary future shell or
child-interpreter semantics**." That is the owner's required wording in substance, and
it is true of the mechanism I measured: the fences are structural (statement
extraction, allow-listed executable heads, positive redirection-target set, exact
interpreter-line inventory), not a denylist.

---

## Required check 2 — candidate delta `a7460784..acdf4e37`

```
 IBKR_PAPER_BRIDGE/deploy/linux/README.md         |  10 +
 IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh     |  83 +++++--
 IBKR_PAPER_BRIDGE/deploy/linux/verify.sh         |  26 +-
 IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py | 290 ++++++++++++++++++++++-
 4 files changed, 373 insertions(+), 36 deletions(-)
```

**Exactly the 4 claimed files, +373/−36**, matching Plan V6 `:17`. `--name-status` = 4×`M`,
no adds, deletes or renames, nothing outside `IBKR_PAPER_BRIDGE/`. `git diff --check`
returned 0. **Scope: PASS.**

Product/engine/store/broker byte-identity, verified by tree OID rather than inspection:
this round changed **no Python outside `tests/`** and no shell outside `deploy/linux/`.
`bridge/` as a whole, `bridge/engine`, `bridge/store`, `bridge/broker` and `config/` are
unchanged, so no engine, store, broker, routes, app, Pine, parity, `MTC_V2`, trading,
order, risk, schema, backtest or strategy byte moved.

### Payload bound to the commit (beyond the required checks)

- `sha256sum RELEASE_SHA256SUMS` = `e74c59fec82d49090d5ba56d4bf18f1cc0dbdd93375c0c82c07ab44b211530bf` ✅ matches the Plan V6 `:19` pin;
- `sha256sum --strict --quiet -c RELEASE_SHA256SUMS` → **rc 0**, 8008 entries;
- `RELEASE_SHA` contains `acdf4e379fb60ee319854acae19fd3eaf7db71a2` ✅;
- **every one of the 8007 tracked files re-read from the payload and compared byte-for-byte against the commit's blob content via `git cat-file --batch`: 0 mismatches, 0 missing**; payload extras = exactly `RELEASE_SHA` and `RELEASE_SHA256SUMS`.

**Line endings — checked deliberately, because this repo carries `* text=auto`.** Every
shipped shell asset in the payload has **CR = 0**: `install.sh`, `verify.sh`,
`rollback.sh`, `lib/common.sh`, `cron/mtc-bridge-logrotate` (263 B), `logrotate/mtc-bridge`.
The ambiguity that has produced three defects on this project is not present here.

---

## Required check 3 — full suite, executed by me

```
PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests
```

run from `C:\AUD62D` at HEAD `acdf4e37`. Exact final line:

```
1376 passed, 1 warning in 195.03s (0:03:15)
```

Exit code 0. The one warning is the existing Starlette/httpx deprecation warning.
**Required `1376 passed, 1 warning` — MET.** `git status --porcelain` empty immediately
afterward, HEAD unchanged. **The run mutated nothing.** (Third independent timing:
implementer 189.98 s, Lead 196.12 s, this run 195.03 s.)

---

## Required check 4 — annex integrity

| Leg | Result |
|---|---|
| Pins match | Annex contains exactly two identities: `acdf4e37…` (9 occurrences) and `e74c59fe…` (4). No third 40-hex or 64-hex token exists in the file. |
| Stale identities | `grep -E '62bf661b\|be689537\|a7460784\|1078ac22\|58705d92\|2581ed3f'` → **zero hits in the annex and zero in launcher v4**. Plan V6 hits are 3, all inside retirement/lineage notes (`:16` lineage chain, `:17` "Round-4 delta vs `a7460784`", `:23` "Retired pins") — none is an executable pin. **PASS.** |
| Bash fences parse | 8 bash fences extracted; `bash -n` on each → **8/8 OK**. |
| PowerShell fences parse | 3 PowerShell fences extracted; `Parser::ParseFile` → **0 errors each**. |
| The three ssh/scp invocations | 3 native invocations (annex `:23` scp, `:41` ssh, `:127` scp). Each carries **all twelve** isolated options — `-F NUL`, `IdentityFile=NUL`, `ProxyCommand=none`, `ProxyJump=none`, `GlobalKnownHostsFile=NUL`, the named `UserKnownHostsFile`, `PasswordAuthentication=no`, `KbdInteractiveAuthentication=no`, `BatchMode=yes`, `StrictHostKeyChecking=yes`, `ExitOnForwardFailure=yes`, `ConnectTimeout=10` — plus an explicit `IdentitiesOnly=no` (a superset of the launcher; `no` is the OpenSSH default, so semantically equal). Each is immediately followed by its `if ($LASTEXITCODE -ne 0) { throw "STOP: …" }` guard. No bare `ssh user@host` anywhere in the annex. **PASS.** |
| Rollback branch vs `rollback.sh` real code | Every line citation in annex R6 is exact against the candidate bytes: `:57–59` require the path and a 64-hex sha; `:60` requires only a regular file; `:61–62` hash and compare; **no code opens or parses the supplied file as JSON** (`STATE_MANIFEST_FILE` appears only at `:40, 46, 57, 60, 61`); `:103–110` handle an absent canonical DB; `:157` onward write the separate rollback record. Empirically confirmed above. **PASS.** |

---

## Required check 5 — launcher v4

`diff v3 → v4` is **exactly the R4 repair and nothing else**: the header line, the
rebuilt `Get-Sha256Fingerprints` (strict full-row grammar, field-2 extraction, throw on
a malformed row) and the `try/catch` that routes that throw into `Fail`. **The entire
option array, `Invoke-NativeCapture`, `Get-SshExitMessage`, `Test-DashboardReady`,
`Start-Process`/readiness loop, `try/finally` cleanup and every `Fail` path are
byte-identical to v3** — so every property rounds 2 and 3 verified survives by
construction. PowerShell AST: **0 parse errors**, 1143 tokens.

Fail-closed in every direction I constructed, using v4's own shipped regex:

| Fixture | Result |
|---|---|
| Codex's comment-injection row | only the wrong field-2 fingerprint returned → **Fail** |
| comment containing `(SHA256:8b6bl/…)` before a valid `(ED25519)` type | field 2 still the wrong key → **Fail** |
| row ending `…(SHA256:8b6bl/…)` (fingerprint in the type slot) | malformed → **throw → Fail** |
| leading-space row / no-comment row | malformed → **throw → Fail** |
| rc-0 agent list with no parsable row | empty array, `-notcontains` true → **Fail** |
| genuine expected key, alone and alongside a second key | **accepted** (the only accepting cases I found) |

`ssh-add` rc 2 / rc 1 / any other nonzero still fail before the comparison; a
`Invoke-NativeCapture` catch leaves `ExitCode = -1`, which falls to the `-ne 0` branch.
No identity-key file of any kind is opened; the one file read remains `known_hosts` via
`ssh-keygen -F`, which is the public host-key pin store. **No regression from v3.**

---

## Required check 6 — exact initial deployment boundary

**This is the one check that fails.** Detail in REQUIRED-1 below.

- Self-contained: **yes** — §3 names its objects inline; the round-3 defect of delegating scope to "the V2 §0 Bridge tenancy boundary" is gone.
- Enumerates every allowed object: **no**.
- Matches the annex's removal enumeration: **no**.

The annex's own R8 admitted-object list (12 items) and its removal command list are
**complete and mutually consistent** — the removal commands touch every admitted object
including the cron runner, the current payload, both state artifacts, the D3 evidence
directory, the audit rule and the package disposition, with full-path equality fences on
the operator-side deletions. The defect is confined to the sentence texts.

---

## Required check 7 — fresh material-only adversarial pass

Everything below was attacked against the real bytes. **Nothing here produced a new
REQUIRED finding under the owner's standard.**

- **UFW predicate, 24 fixtures of my own construction.** Correct in all 24: `LIMIT IN`, `ALLOW FWD`, `LIMIT FWD`, destination-address-before-port, inclusive ranges (`8000:9000`, `8789:8791`), no-protocol `8790`, `8790/udp`, `(v6)`, `on eth0`, tab-separated rows, `Anywhere ALLOW IN 10.0.0.0/8` (allow-all-ports, correctly treated as exposing), an app profile crafted to contain the literal `ALLOW IN` in its name (→ STOP), `OpenSSH`/`Nginx Full` (→ STOP), a ufw rule comment (→ STOP), `DENY`-only control (correctly PASS), `22/tcp`+`22/tcp (v6)` clean baseline (PASS), `20:25/tcp` SSH range (PASS), inactive (FAIL), `Default: allow (incoming)` (FAIL), and an active firewall with no rules at all (FAIL — no numeric 22/tcp). **I found no false "not exposed".** The main parser reaches `mark_unmodelled → exit 2` for every row that is not an explicit DENY/REJECT-inbound or any-verb-OUT row, and the independent substring backstop is a second, unreachable-by-parser-edit leg.
- **awk portability.** Re-ran the key fixtures with `gawk --posix` forced onto `PATH`: **identical results**, so the parser relies on no GNU extension. I did not measure `mawk` (KVM2's default awk); every construct used — POSIX classes, `match`/`RSTART`/`RLENGTH`, `substr`, regex `split` — is mawk-1.3.4 supported, and any mawk failure would exit nonzero into the `fail` branch, i.e. fail-closed. Stated as reasoning, not measurement (→ DFU-9).
- **Do the new fail-closed assertions self-inflict a failed attempt on the real host?** No, and this was the highest-value thing I checked. `install.sh:445,447` install both assets with `-o root -g root -m 0644` / `-m 0755`, so `verify.sh`'s new `0:0` numeric-owner and exact-mode assertions pass on a genuine root install. `KVM2_READONLY_INVENTORY_2026-08-16.md:29–30` records the only allow rule as numeric `22/tcp (v4+v6)` — exactly my clean fixture, which PASSES; a profile-style rule would have STOPped the new parser on the real host. `cron` is in the inventory's running-services list, so annex stage 3.4's `systemctl is-active cron` returns 0.
- **Payload tree assertions against the real payload.** Emulated `assert_regular_directory_tree` (no non-regular entry) and `assert_exact_payload_tree` (manifest path set vs `find`): **MATCH under both `LC_ALL=C` and `C.UTF-8`**, despite 71 non-ASCII filenames. The commit tree contains no symlink (mode 120000) or gitlink (160000) blob, so `cp -a` cannot carry a special entry into the release.
- **Secret exposure via the payload.** The payload is the whole repository, and `install.sh` copies all of it into `/opt/mtc-bridge/releases/<sha>/` at 0555 (world-readable). I scanned it: **no private-key body** (all four `-----BEGIN … PRIVATE KEY-----` hits are detector regexes inside security docs/scripts), no live API token (the only `sk-…` hits are redaction-test fixtures asserting non-leakage), `SECRET_INVENTORY.md` is names-only by design, exactly one file mentions the host IP, and **no file contains the launcher's pinned fingerprint**. No material exposure → DFU-6.
- **Rollback rehearsal end-to-end trace on the never-started state.** `systemctl mask` on an already-masked unit is idempotent; `:88` finds the unit inactive; `:91–101` writer/port assertions pass with nothing running; `:105` takes the "no state database present" branch; `:117` skips the `--to-*` re-bind; `:158–181` writes `/etc/mtc-bridge/rollback_manifest.json` — an object the annex admits (item 2). The subsequent stage-3.2 `verify.sh` re-run is unaffected by that new file.

---

## REQUIRED

### REQUIRED-1 — the §4 sentence the owner signs does not enumerate two KVM2 objects the attempt it authorizes creates, and the package supplies two different §4 sentences with no precedence rule

**T0 property affected:** the exact initial KVM2 deployment boundary (and, through it,
rollback/removal) — one of the five items the owner's round-4 decision requires both
auditors to verify, and required check 6 of this brief.

**The mismatch, measured.** The annex's R8 "Complete admitted object list" for the
initial install has 12 items. Plan V6 §3 — headed *"the single authorization ask"* — ends
its object clause with the absolute words **"— nothing else."** and omits two of them:

| Object | Plan V6 §3 clause | Annex R8 admitted list | Annex §4 sentence | Annex removal commands |
|---|---|---|---|---|
| `/home/baris/bridge-state-initial.tar.gz` | **absent** | present (item 11) | present | removed |
| `/home/baris/bridge-state-initial.sha256` | **absent** | present (item 11) | present | removed |
| `/home/baris/payload-acdf4e37` | present | present (item 10) | **absent from "limited exactly to"** | removed |

**The self-contradiction is inside one sentence.** §3's action clause explicitly
authorizes *"Bridge-scoped operational evidence in the annex's stage-3 order
(**never-started state capture**, …)"*. Annex stage 3.1 *is* that state capture, and it
creates exactly the two files §3 then forbids:

```bash
sudo tar -C / -czf /home/baris/bridge-state-initial.tar.gz var/lib/mtc-bridge etc/mtc-bridge
sha256sum /home/baris/bridge-state-initial.tar.gz > /home/baris/bridge-state-initial.sha256
```

**Concrete initial-deployment failure.** §3 also authorizes stage 3.5, the tenancy
re-inventory, as the closing step of the one bounded attempt. At that point KVM2 holds
two root-owned objects that are on the annex's allowed list and on its removal list but
are outside the boundary the owner signed. The annex says *"only the complete Bridge
tenancy objects in R8 … may differ"* → continue; §3 says the allowed objects are its
shorter list and **nothing else** → STOP. **The operator must adjudicate a direct
conflict between the signed authorization and the pinned annex, in the middle of the
single attempt the owner signs for, and no text in either file resolves it** — I grepped
both for a precedence rule (`supersede`/`governs`/`authoritative`) and there is none.
The conflict is sharpened by the package carrying **two competing §4 sentences**: Plan V6
§3 ("the single authorization ask") and annex `:713` ("Self-contained authorization
sentence for Plan V6 §4"), which are not the same text and disagree on the object list in
both directions.

**What this is not.** Nothing unsafe is authorized. Both sentences forbid service start,
enable, secrets, firewall changes, public 8790, TESTNET/mainnet, broker, ARM, orders and
the reserved Hermes/web identities identically. The two omitted files are benign
operator-home artifacts and the removal list already deletes them. This is a boundary
precision defect on the one instrument that defines what may exist on the host — not a
capability defect.

**Fix (contained, text only, no code and no candidate change).** Pick one sentence as
§4, delete or explicitly subordinate the other, and make the survivor carry the annex's
complete 12-item R8 list verbatim — i.e. add `/home/baris/bridge-state-initial.tar.gz`,
`/home/baris/bridge-state-initial.sha256` and the two named operator-side EFS directories
to Plan V6 §3, and add `/home/baris/payload-acdf4e37` to the "limited exactly to"
enumeration. One edit to each file. It disturbs nothing verified closed above, and it
does not touch the candidate, the payload, the suite or the launcher — the four pinned
subjects would keep their hashes except the plan and annex.

---

## DISCLOSED-FOLLOW-UP

Recorded, per the owner's standard, as follow-up work rather than a repair cycle: none of
these affects the exact initial keyless DISARMED deployment.

1. **DFU-1 — the annex's own status block is stale and now false after the Lead's repin.** Annex `:3–10` reads *"Until that repin, the literal `acdf4e379fb60ee319854acae19fd3eaf7db71a2` coordinates below are the task-mandated round-3 subject coordinates, not authority to deploy changed worktree bytes."* `acdf4e37` is the round-4 candidate; the round-3 subject was `a7460784`. The Lead's 21 pin replacements rewrote the identity inside the caveat that was meant to describe the *pre*-repin state. Fail-safe direction — an operator reading it would hold, not proceed — but it is a factual error inside the hash-pinned instrument the owner's sentence cites.
2. **DFU-2 — neither §4 sentence names the D3 objects the annex admits.** `/home/baris/mtcbridge-d3-evidence` and `libauparse0` appear in the annex's D3 admitted list (items 13–14) and in its removal commands, but in neither sentence. D3 requires its own separate owner sentence, so this is out of the initial scope; fold it into REQUIRED-1's edit.
3. **DFU-3 — annex R7 residuals (D3-only).** The contract is genuinely executable and fail-closed, and the annex is honest that local verification found neither `ausearch` nor its man page, so the no-match rc is stated as an admitted conjunction rather than a claim. Residuals: the `trap cleanup_mtcbridge_audit_rule EXIT` is armed at `:449` before the rule is added at `:457`, so an exit in that window runs a delete of a non-existent rule and prints `CRITICAL`; and `-F arch=b64` scopes the rule to 64-bit syscalls. Neither runs under the initial sentence.
4. **DFU-4 — launcher `-notcontains` is case-insensitive.** PowerShell's `-notcontains` compares case-insensitively; an SSH fingerprint is case-sensitive base64. Carried from my round-3 NIT-5. v4's exact `{43}`-char, `[A-Za-z0-9+/]` field-2 grammar narrows the exposure further, but `-cnotcontains` still costs one character.
5. **DFU-5 — two launcher robustness NITs carried unchanged from rounds 2 and 3.** `:216` `Wait-Process -Id $tunnel.Id -ErrorAction Stop` turns an ssh death in the browser-launch window into *"Cannot find a process with the process identifier …"* instead of `Get-SshExitMessage`'s real class; and `Fail()`'s trailing `Read-Host` at `:24` throws under `$ErrorActionPreference='Stop'` with redirected stdin, so `exit 1` never executes. Both only affect message quality / non-interactive use.
6. **DFU-6 — the payload is the whole repository.** 7768 of 8007 files are `MTC_COMMAND_CENTER` planning documents unrelated to the Bridge, and all of them are copied to `/opt/mtc-bridge/releases/<sha>/` at 0555. I verified there is **no secret material** in it (details in check 7), so there is nothing to leak today, and this is the composition rounds 1–3 already accepted. Worth narrowing before the reserved `hermes`/`webapp` tenants ever exist on the host.
7. **DFU-7 — a ufw rule comment STOPs verification.** `22/tcp ALLOW IN Anywhere # admin ssh` renders the source field unmodelled and halts the whole assertion. That is the correct fail-closed direction and I am not asking for it to be relaxed, but rule comments are ordinary practice; the runbook should say a commented rule stops verification and how to proceed. Carried from my round-3 NIT-13.
8. **DFU-8 — the strict `ssh-add -l` grammar STOPs on legitimate-but-unusual rows.** A key held in the agent with an empty comment renders without a comment field and is rejected as malformed. Fail-closed and correct, but the owner should be told that "identity row malformed" usually means *another key in your agent looks unusual*, not an attack.
9. **DFU-9 — awk flavour not measured on the target.** I verified the UFW parser under GNU awk 5.3.2 and again under `gawk --posix`; KVM2's default is `mawk`. Every construct used is mawk-supported and any mawk failure lands in the fail branch, but I am recording that I reasoned this rather than measured it.

## NIT

- Plan V6 §3's owner sentence quotes the annex hash truncated as `` `8cb02ff7…` ``. The full 64-hex is in §1 and the annex itself contains **zero** ellipses, so no executable path is affected — but the ellipsis sits in the text the owner signs. Fold into REQUIRED-1's edit.

---

## Verdict

**REQUEST_CHANGES — 1 REQUIRED, 9 DISCLOSED-FOLLOW-UP, 1 NIT.**

The round-4 work is the strongest of the four rounds, and I want that on the record
before the finding. **All eight round-3 findings were repaired on mechanism and nine of
the ten are fully closed** — I reproduced every attack myself on the real bytes rather
than reading `RIC3`, and found no overstatement in that report. The two D026 arms are no
longer denylists: the installer fence extracts logical statements, allow-lists executable
heads, closes the redirection-target set to exactly `{/dev/null, ${MTC_INSTALL_MANIFEST}}`
and rejects direct mutators including `eval`-wrapped ones; the verifier fence pins the
exact interpreter-line inventory. Both of my own round-3 optional NITs are now RED as a
side effect. The UFW predicate survived 24 fixtures of my construction across two awk
modes with no false "not exposed". The metadata assertion gates the byte comparison, so
Codex's `0777`/`1000:1000` root-execution hole is shut. Launcher v4's diff from v3 is
exactly the R4 repair, and the comment-injection spoof is dead. The rehearsal branch now
runs: I built the annex's tar and drove `rollback.sh`'s real precondition code with it.
The suite is `1376 passed, 1 warning` under my own hand with the worktree clean before
and after, the delta is exactly 4 files with `bridge/` byte-identical by tree OID, and the
payload binds blob-for-blob to the commit across all 8007 files with LF preserved on every
shipped script. The annex carries zero stale identities, all eleven fences parse, and all
three ssh/scp invocations carry the complete isolated option set with STOP guards.

One finding stops it, and it is the remaining third of Codex R8. The instrument the owner
actually signs — Plan V6 §3 — authorizes the stage-3 state capture and then says the
allowed objects on KVM2 are a list that excludes the two files that capture creates,
closing with "nothing else". The annex, which the same sentence pins by hash, allows them
and removes them. The package also carries a second, differently-worded §4 sentence, and
nothing says which one governs. The operator meets that contradiction at the last step of
the one attempt the owner signs for. It is a text-only defect, it authorizes nothing
unsafe, and it is one edit to each of two files — but required check 6 asks precisely
whether the §3 sentence enumerates every allowed object and matches the annex's removal
enumeration, and it does not.

**I am not softening it to fit the schedule, and I am equally not inflating it.** Under
the owner's standard the honest report is: the engineering is done and verified; the
authorization sentence is not yet an accurate description of what the authorized attempt
creates. **The §4 sentence should not be presented on these exact bytes**; with the two
enumerations reconciled, everything else in this package passed under my own hand.

In plain terms for the owner: the code, the tests, the release package and the launcher
all check out — every problem raised last round is genuinely fixed, and I re-attacked each
one myself instead of trusting the report. The one thing left is the permission sentence
you would sign. It lists the files the installation is allowed to create and ends with
"nothing else", but the plan also tells the operator to make two backup files in your home
folder that the list forgets to mention — and there are two slightly different versions of
that sentence in the package, with nothing saying which is the real one. Nothing dangerous
is being allowed; the two files are harmless and the cleanup already deletes them. It is a
wording fix in two documents, not new engineering.

---

*Reviewer: Claude slot, `claude-opus-5`, round 4 (final) of the owner's round-4 override.
Read-only outside this file and disposable scratch; no host or network contact; launcher
never executed; no ssh or scp invocation of any kind; no git mutation; no sub-delegation.
All four subject pins verified identical at start and at end.*
