# FINAL T0 review — Codex slot — Plan V6 + annex + launcher v4 + candidate `acdf4e37`

| Field | Value |
|---|---|
| Model identity from runtime/route | **OpenAI Codex `gpt-5.6-sol`** |
| Effort | **xhigh** (required T0 route) |
| Session | Fresh, independent FINAL T0 Codex slot; no sub-delegation |
| Working directory | `C:\AUD62D` |
| Start (UTC+3) | **2026-08-16 16:37:56 +03:00** |
| Stop (UTC+3) | **2026-08-16 16:55:01 +03:00** |
| Owner materiality standard | Applied exactly: only exact-initial-deployment T0 failures are REQUIRED; later/generalized/proof-polish items are disclosed separately |
| **VERDICT** | **REQUEST_CHANGES — 2 REQUIRED, 3 DISCLOSED-FOLLOW-UP, 0 NIT** |

## Execution boundary

Read-only everywhere except this verdict and disposable scratch under
`C:\tmp\codex_t0_final_20260816_1638`. I did not execute the launcher,
installer, verifier, rollback script, removal block, SSH, SCP, `ssh -G`,
systemctl, UFW, auditd, package, service, firewall, or any target-host command.
I did not contact KVM2, another host, or any network endpoint; did not read an
identity key; did not mutate Git state; and did not sub-delegate. Local
falsification used copied source, parser-only PowerShell, syntax-only Bash, and
stubbed commands outside every repository.

## All four subject pins — start and end

| Subject | Required pin | Start | End |
|---|---|---|---|
| Plan V6 | 6207 B; SHA-256 `f433d35ae9516c2a94304f5459fba442209269ee034116b5634fbb320df0ba8f` | exact | exact |
| Command annex | 31283 B; SHA-256 `8cb02ff7fa13eb7e0ac602cfe0f1854b615cb079535ff91385e6c18efc5e5fce` | exact | exact |
| Launcher v4 | 9277 B; SHA-256 `ac68196b4ae99e12892898c0a5bfb2d7d2249fc2bb476619a4c2bdaaebf2a1b5` | exact | exact |
| Candidate | HEAD `acdf4e379fb60ee319854acae19fd3eaf7db71a2`; parent `a7460784c1563c140ee7c75197aeab2b0170da8a` | exact; clean, detached audit worktree | exact; tree `3fa403b4115620a7c16ce377f613d84aae63de48`; local and `origin/` integration refs at HEAD; clean |

No pin mismatch or BLOCK condition occurred.

The local payload also binds correctly: `RELEASE_SHA` is the full candidate,
`RELEASE_SHA256SUMS` hashes to
`e74c59fec82d49090d5ba56d4bf18f1cc0dbdd93375c0c82c07ab44b211530bf`,
`sha256sum --strict --quiet -c` returns 0, and its inventory is the exact 8007
commit files plus `RELEASE_SHA` (no missing Git path).

## Eight-finding closure table

| Round-3 finding / required attack | Independent result | Closure |
|---|---|---|
| **R1 — structural D026 installer/verifier fences**: direct-unwrapped mutator and child-interpreter write | In separate scratch copies I added exact `install -d -o root -g root -m 0755 /opt/codex-unlisted-direct`; the real installer arm failed at the direct-mutator inventory, **rc 1**. I added exact `python3.12 -c '...Path("/tmp/codex-verifier-python").write_text("mutation")'`; the real verifier arm failed at the interpreter inventory, **rc 1**. Unmutated targeted group: **14 passed, 48 deselected**. | **CLOSED** for the shipped, documented grammar. |
| **R2 — UFW LIMIT/profile/forward grammar** | The real parametrized function test rejects `OpenSSH ALLOW IN`, `8790/tcp LIMIT IN`, and `8790/tcp ALLOW FWD`, while retaining the safe numeric tenant case. Parser now processes `ALLOW/LIMIT x IN/FWD`, fails named profiles closed, requires numeric `22/tcp`, and retains the independent 8790 backstop. | **CLOSED**. |
| **R3 — root-executed asset metadata** | Real extracted verifier block rejects mode `0777` and numeric owner `1000:1000`; metadata is checked before byte equality for both the logrotate policy (`0644`, `0:0`, regular non-symlink) and cron runner (`0755`, `0:0`, regular non-symlink). | **CLOSED**. |
| **R4 — launcher comment-injection fingerprint** | Launcher AST errors = 0. Exact wrong-key row with the expected fingerprint only in its comment parses field 2 as `SHA256:AAAA...`, so expected-pin acceptance is **false**; a valid expected field-2 row is accepted; malformed row is rejected. V3 is at its published hash, and the v3→v4 diff is limited to version text, strict parser, and fail routing. | **CLOSED**; no v3 regression found. |
| **R5 — literal command completeness** | Annex contains the full 40-hex candidate and current manifest pin, no forbidden stale identity, no ellipsis path, 8/8 Bash fences parse at rc 0, 3/3 PowerShell fences have zero AST errors, and all three SSH/SCP invocations contain the complete isolated option set. Stage 1–3.5 commands and adjudication are present. | **CLOSED** for the required command-restatement attack. |
| **R6 — never-started rehearsal input** | `install.sh` creates `/var/lib/mtc-bridge` and `/etc/mtc-bridge` before the unit. Annex creates a real tar and measured 64-lowercase-hex hash. Current `rollback.sh:57-62` requires only a regular supplied file and its exact SHA-256; it does not parse JSON, and its absent-DB branch is explicit. Exact release path exists in the payload. | **CLOSED** for rehearsal-input existence and real rollback interface. |
| **R7 — fail-closed D3 evidence contract** | Static mechanism has exact read-only SQLite queries, rc/stderr/three-line shape checks, explicit WAL presence/absence adjudication, DB/WAL hashes, active UID-rule proof, bounded UTC window, exact no-match shape, unchanged numeric lost counter, and exact rule/package cleanup. All related fences parse. This is later-D3 and was not host-executed under the hard exclusion. | **CLOSED** on delivered mechanism; no host result claimed. |
| **R8 — self-contained authorization/removal boundary** | The annex's complete list includes state archive/hash and operator EFS directories, but Plan V6 §3's actual owner sentence omits them and says its shorter list is “nothing else.” The mandatory initial stage creates those omitted objects. See REQUIRED-1. | **NOT CLOSED**. |

## Checks 2–6

### 2. Candidate delta and protected scope — PASS

`a7460784..acdf4e37` is exactly four files, matching the claim:

```text
M IBKR_PAPER_BRIDGE/deploy/linux/README.md
M IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh
M IBKR_PAPER_BRIDGE/deploy/linux/verify.sh
M IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py
```

Stat: **4 files, 373 insertions, 36 deletions**. `git diff --check` returns 0.
No other file changed. `bridge/engine`, `bridge/store`, and `bridge/broker` tree
OIDs are byte-identical at base and candidate; consequently product, trading,
broker, order, risk, store, strategy, Pine, parity, MTC, and schema bytes are
outside the delta.

### 3. Full suite — PASS

Executed from `C:\AUD62D`:

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
python -m pytest -q -p no:cacheprovider IBKR_PAPER_BRIDGE/tests
```

Real result:

```text
1376 passed, 1 warning in 206.98s (0:03:26)
```

Exit code 0. The warning is the existing FastAPI/Starlette `httpx` deprecation
warning. HEAD was the candidate and status count was zero both before and after:
the suite mutated nothing. The exact payload's `install.sh`, `common.sh`,
`verify.sh`, and `rollback.sh` all pass WSL `bash -n`; the Windows audit checkout
uses CRLF conversion, so payload/commit bytes, not converted checkout bytes, are
the deployment syntax subject.

### 4. Annex integrity — PASS on pins, stale identities, parsing, SSH isolation, and rehearsal interface

- Candidate, payload name, and manifest SHA-256 match the pinned package.
- Grep has zero annex hits for `62bf661b`, `be689537`, `a7460784`, `1078ac22`,
  `58705d92`, `2581ed3f`, three dots, or a Unicode ellipsis.
- All 8 Bash and all 3 PowerShell fences parse.
- Exactly three OpenSSH invocations exist (`scp`, `ssh`, `scp`); each has
  `-F NUL`, null identity/global trust, disabled proxy routes, the explicit user
  trust store, `IdentitiesOnly=no`, password and keyboard refusal, batch mode,
  strict checking, forward-failure, and 10-second timeout.
- Stage 3.1 passes the tar and its measured SHA to the real non-JSON
  `rollback.sh` input contract.

The separate failed-attempt removal defect found in the fresh pass is
REQUIRED-2 below.

### 5. Launcher v4 — PASS

AST errors = 0; exact comment injection is rejected; valid field-2 pin is
accepted; malformed row fails closed. V3's published 8651-byte hash was
reverified, and inspection of the complete v3→v4 diff found no change outside
the narrow parser/failure-routing repair and version header. The launcher was
never executed.

### 6. Exact initial deployment boundary — FAIL

Plan V6 §3 is not the self-contained enumeration required by the common
contract and does not match the annex's admitted/removal universe. REQUIRED-1
is a direct initial-deployment contradiction, not documentation polish.

## REQUIRED — material exact-initial-deployment findings

### REQUIRED-1 — known R8 remains open: §3 forbids objects its mandatory initial stages create

Plan V6 §3 lines 43–50 authorizes the never-started state capture, rollback
rehearsal, and off-host restore check, then enumerates the allowed KVM2 objects
and ends **“nothing else.”** That enumeration omits:

- `/home/baris/bridge-state-initial.tar.gz`;
- `/home/baris/bridge-state-initial.sha256`; and
- the named operator-side encrypted backup and restore-check directories.

The annex's authoritative admitted list contains those exact objects at lines
562–565, Stage 3.1 creates the two host files, Stage 3.3 creates the two operator
directories, and removal lines 689–706 remove them. The annex's own draft owner
sentence also names them, but the subject Plan V6 §3 sentence does not.

**Concrete initial-deployment failure:** executing the required Stage 3.1/3.3
sequence creates objects the owner's literal sentence says are outside the
allowed “nothing else” set; refusing to create them makes the authorized
rollback rehearsal/off-host verification impossible. This directly affects
authorization integrity and rollback/removal in the exact initial keyless
DISARMED deployment. It is also the same mechanism class as known round-3 R8,
so R8 is not closed.

### REQUIRED-2 — failed-attempt removal aborts when installation fails before the unit exists

The annex says its removal block runs “after a failed attempt” (line 583), sets
`-Eeuo pipefail` (line 589), then unconditionally executes:

```bash
sudo -n systemctl stop mtc-bridge-first-start.service
```

at line 663, before every Bridge file/user/payload deletion at lines 665–693.
But `install.sh` creates the user, directories, release and venv at lines
297–391 and does not install the unit until lines 409–420. A venv creation,
locked dependency install, checksum, sealing, or env-file failure can therefore
leave an exact in-scope partial install with no loaded unit. `systemctl stop` on
an unloaded unit returns nonzero; under `set -e`, cleanup terminates before any
listed object is removed. An isolated no-host control-flow reproduction with
the missing-unit return `5` exited **rc 5** and never reached the cleanup marker.

**Concrete initial-deployment failure:** if the one authorized install fails
before unit installation, the advertised removal command stops at the absent
unit and leaves the new user/directories/release/payload on KVM2. The clean
baseline is not restored, contradicting Plan §3's mandatory failed-attempt
disposition. This is directly applicable rollback/removal safety, not a future
mutation or proof-strength concern. The Lead can reproduce it without KVM2 by
running the exact branch against a disposable systemd namespace with the unit
absent.

## DISCLOSED-FOLLOW-UP — non-blocking under the owner standard

1. **Later-D3 authority wording:** Plan §3 says it “pre-authorizes” `auditd` and
   the audit rule, omits the D3 evidence directory and `libauparse0`, then says
   “No service start”; the annex correctly requires a later separate D3 sentence
   and temporary `auditd` start/stop. This must be harmonized before D3, but D3
   is explicitly outside the exact initial masked deployment.
2. **Authorization pin presentation:** §3 abbreviates the annex SHA-256 as
   `8cb02ff7…`. The full hash is correctly pinned in §1 and matched at both audit
   observations, so replacing the abbreviation with the full hash is a
   proof-strength improvement rather than a failure on this exact package.
3. **Annex status prose:** the annex header still says repinning remains for the
   Lead and calls the final `acdf4e37` coordinates “round-3” inputs, while Plan
   §1 records the completed final repin. This is stale provenance prose, not an
   executable stale identity or exact-deployment safety failure.

## NIT

None.

## Final verdict

**REQUEST_CHANGES — 2 REQUIRED, 3 DISCLOSED-FOLLOW-UP, 0 NIT.**

The candidate scope, payload integrity, full suite, known D026/UFW/metadata/
launcher/command/rehearsal/evidence mechanisms, and all pins pass. Acceptance
fails because the actual §3 sentence still excludes objects its mandatory
initial sequence creates, and the exact failed-attempt removal path can abort
before cleanup on a normal early install failure. Both are directly applicable
to the owner's exact initial deployment boundary and rollback/removal standard.

No fifth round is authorized. Do not run the launcher, do not contact KVM2, and
do not present the §3 installation-authorization sentence on this package.
