# NEXT SESSION — FULL HANDOFF (2026-08-03)

**Supersedes `NEXT_SESSION_HANDOFF_2026-08-02.md`.** Paste everything below the line as the new
session's first message. Written to stand alone — no prior conversation needed.

---

Repo: `C:\LAB\Tradingview_LAB_CLEAN`

Read `AGENTS.md`, then `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` (RESUME HERE), then
`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RESULT_2026-08-02.md` and
`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RECON_DEFECT_LIST_2026-08-02.md`.

You are **Lead Orchestrator and acceptance authority**. Codex CLI `gpt-5.6-sol` is the implementer.
This supersedes the plan's §23c/§39-10 actor assignment and weakens no safety, testing, scope, audit,
model or evidence requirement.

## 1. Headline — Gate A ran for real, and FAILED at A-2

The 50-hour programme's central rehearsal happened on the night of 2026-08-02. **A-0 and A-1 passed.
A-2 failed hard.** The WP-I candidate artifact cannot install on Linux, and reconnaissance behind
that failure found three more blockers. **The candidate artifact
`1adf9ae51b0ddfe81057860aec5c23bb842f5a84` must be rebuilt.**

This is the gate doing exactly its job. Had the install been attempted directly on KVM2, the single
bounded `KVM2-P4-02` attempt would have been spent on a payload that could never have worked.

## 2. The four defects

| # | Defect | Status |
|---|---|---|
| 1 | **CRLF in the built payload.** `install.sh` dies at line 37 with `$'\r': command not found`. **The repository is CLEAN** — committed blobs are LF-only. `package.sh:73` runs bare `git archive` while the repo has `core.autocrlf=true`, so the export converts. One-line build fix. | **This is the A-2 FAIL** |
| 2 | **`lib/common.sh:98` can never seal a venv.** `find "$root" -perm /222` has no `-type` filter; symlink modes are always 0777 on Linux and meaningless. A venv always has symlinks. | Blocks install even after #1 |
| 3 | **The suite floor is wrong.** Recorded `2 failed, 1304 passed` was measured on **Python 3.14**; the locked runtime is **3.12** and the dev machine has no 3.12. On the real runtime: **26 failed, 1280 passed**. | Baseline invalid |
| 4 | **The service cannot start without broker credentials**, which Gate A §0 forbids. A-4 is unexecutable as pre-registered. | **Needs your decision** |
| 5 | **The build is not reproducible.** The same `RELEASE_SHA` yields different payload bytes and a different manifest hash depending on the builder's line-ending config. Defect 1 is a *symptom* of this. | The real disease |

**An independent `gpt-5.6-sol` xhigh audit was commissioned specifically to falsify these findings**
(`GATE_A_INDEPENDENT_AUDIT_2026-08-02.md`). Verdict **REQUEST_CHANGES**: it refuted my original CRLF
root-cause attribution, corrected two overstatements, and identified defect 5 as the thing I had
missed. All findings were reproduced on real source and applied. The A-2 FAIL itself is unaffected.

Full evidence, including exact hashes, CR counts, root-cause attribution and the falsification of
prediction P3, is in `GATE_A_RECON_DEFECT_LIST_2026-08-02.md`.

### Defect 3 deserves emphasis

Within the 26 Linux failures, ~21 are `tests/test_wal_state_bundle.py`, all reporting
`source_changed_during_capture` with `changed_components: ['wal','shm']` while the database itself is
stable. SQLite's sidecar files are necessarily touched on Linux by opening a WAL-mode database, so
the capture trips its own drift detector.

**This is safety-relevant.** `wal_state_bundle.py` is the tool `COMMANDS.md` Stage E uses for the
KVM2 **ordered single-writer cutover**, and Stage E states explicitly *"Do not pass
`--allow-live-source`."* As written, **the cutover cannot produce a valid state bundle on Linux.**

## 3. THE DECISION ONLY YOU CAN MAKE — defect 4

The installed unit runs `python -m bridge.app`; `app.py:113-114` builds a real `HyperliquidBroker`,
which at `:201` demands `HL_ACCOUNT_ADDRESS` + `HL_API_WALLET_KEY` and raises without them.

- Gate A §0: *"DISARMED only. … **No broker credentials.**"*
- Gate A A-4: *"**Start the service.**"*

Both cannot hold. A-4 is the check the runbook calls *"the most important check in the gate"* and
*"the whole point of the 50 hours"*, and it **could not be executed**.

Choose one:

- **(a)** Give the bridge a genuine credential-free DISARMED start mode. A DISARMED bridge that
  cannot trade arguably should not need trading credentials merely to boot. *(Lead's
  recommendation — it makes the DISARMED guarantee testable without ever holding a secret.)*
- **(b)** Re-scope A-4 to run after Stage D with TESTNET credentials provisioned. This **breaches
  Gate A's own §0 boundary** and needs your explicit authorisation.

`--dry-run` is **not** an answer: it wires `MockBroker.from_csv(tests/fixtures/BTC_1h.csv)`. Starting
the production service against a test fixture must not be used to manufacture an A-4 pass.

## 4. What is NOT established — do not let anyone claim otherwise

- **A-3 through A-9 were NOT run as Gate A checks.** The gate stopped at A-2 as the runbook requires.
  Everything after that is explicitly-labelled reconnaissance on a *normalised copy* and **cannot be
  cited as gate evidence**.
- **The ARM-refusal path is UNTESTED.** The A-4 script logged a `PASS` when `curl` returned
  `http=000` — connection refused, because the service had died. Nothing was listening, so nothing
  was proven. That PASS is counted nowhere.
- **A-5 never ran** — it needs a live service.
- WP-L Phase 2, WP-I staging, Audit 2 and WP-A are all **blocked** behind the rebuild.

## 4b. Defects 1, 2 and 5 are ALREADY FIXED and validated — branch waiting for you

Branch **`codex/gate-a-build-determinism` @ `a1dd5b46`** (pushed, **not merged**, no Gate 5 audit yet).
Codex implemented; Lead audited and validated. Full evidence:
`GATE_A_REPAIR_VALIDATION_2026-08-02.md`.

Two files, three hunks: pin `git archive` to `core.autocrlf=false core.eol=lf` per-invocation, add a
post-export assertion that fails the build on any surviving CR byte, and give
`assert_no_writable_paths` a `-type` filter.

What it demonstrably achieves:

- **Deterministic build** — rebuilding the same `RELEASE_SHA` with `core.autocrlf` forced to a
  different value produces an identical manifest `d25d4464…`. Payload files now equal their committed
  blob sizes exactly.
- **The new guard was falsified deliberately** — a temporary commit carrying a real CRLF blob made
  the build die. It is not decorative.
- **Installs on Ubuntu unaided** — `install.sh` EXIT=0, both release tree and venv sealed, unit
  masked, not started, no secret, no firewall change; `verify.sh` **VERIFY PASS**. No host file was
  edited, which was A-2's FAIL condition.
- **`test_linux_deployment.py`: 34 passed, 0 failed** (was 4 failed / 30 passed). The ledger-hash
  test the programme has carried as an accepted pre-existing failure was never a defect — it was
  this build bug.
- Full suite: **25 failed, 1281 passed**, matching the prediction made before the run.

Still broken after it, by design: defects **3a, 3b and 4**. The Linux floor is 25, not 2;
`wal_state_bundle` (the Stage E cutover tool) is still broken on Linux; and A-4 is still
unexecutable, so the ARM-refusal path remains untested.

**Before merging:** it needs a Gate 5 audit at the canonical floor. Codex implemented it, so Codex
cannot be one of its auditors this round.

## 5. Required repair (steps 1-3 DONE on the branch above; the rest outstanding)

1. **Fix the build, not the repo.** `package.sh:73` must export without line-ending conversion:
   `git -c core.autocrlf=false -c core.eol=lf archive …`. Verified to produce byte-exact LF output
   equal to the blob sizes. Building on Linux would also work.
2. Optionally add explicit `eol=lf` attributes for `IBKR_PAPER_BRIDGE/deploy/linux/**` so the export
   is deterministic whatever a builder's local `core.autocrlf` is. **Do NOT `git add --renormalize`**
   — the committed bytes are already correct.
3. Fix `lib/common.sh:98` →
   `find "$root" \( -type f -o -type d \) -perm /222 -print -quit`. If symlink *targets* matter,
   write that as its own assertion rather than conflating it with write bits.
4. Decide defect 4 (§3 above), then fix accordingly.
5. Investigate the `wal_state_bundle` sidecar drift — this one is not cosmetic.
6. Rebuild the payload. **This produces a new `RELEASE_SHA` and a new manifest SHA-256**; every
   record quoting `1adf9ae5…` / `bfefea2f…` becomes historical.
7. Re-run Gate A **from A-0**. Nothing below A-2 is established for a corrected artifact.

**The repository needs no content change at all.** An earlier version of this handoff called for a
repo-wide renormalisation; that was based on a root-cause attribution that an independent
`gpt-5.6-sol` audit refuted, and it is withdrawn. Committed blobs are LF; only the export was wrong.
(TS-P0-001 was never at risk either way — `RUNTIME_BASELINE_CONTRACT.md` lines 67-68 normalise CRLF
to LF before hashing.)

## 6. The staging host — keep it

| Item | Value |
|---|---|
| VM | `GATEA-STAGING`, Hyper-V Gen 2, Ubuntu 24.04.4 LTS, Python 3.12.3 |
| IP | `172.24.55.233` (Default Switch NAT — **changes when the Windows host reboots**) |
| SSH | `ssh -i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519 gatea@<ip>` — key-only, **no password exists** |
| Assets | `C:\HyperV\GATEA-STAGING\` — scripts, seed ISO, `console-shot.ps1` |
| On host | `~/payload` (pristine, hash-verified), `~/recon` (normalised copy), `~/gate-a-0*.sh` |

The plan requires this host be **retained through WP-L Phase 2, WP-I staging and WP-A** — do not
destroy it. It is expendable in the sense that it may be wiped and rebuilt, and rebuilding is cheap:
the verified Canonical ISO and the autoinstall seed are both on disk.

`console-shot.ps1` captures the VM console via the Hyper-V WMI thumbnail API — useful when a VM looks
wedged and you need to see the screen.

## 7. Also true, and unrecorded before last night

An **undocumented prior effort exists**: VM `KVM2-Ubuntu-2404-Staging`, created 2026-07-27, plus ~50
scripts under `C:\HyperV\KVM2-Staging\`. Nothing under `MTC_COMMAND_CENTER/` referenced it. Its own
records show `bridge_rehearsal: NOT_RUN` and `classification: "local infrastructure-only"`, so the
safety boundary was never breached — but the 2026-08-02 handoff's host inventory was wrong.

That VM was **not** used as the Gate A host (it ran dummy install/rollback rehearsals and undocumented
hand-repairs, so it cannot be shown clean) and was **left untouched — not started, not modified, not
deleted.** Its disposal is your call. Details: `GATE_A_STAGING_HOST_PROVENANCE_2026-08-02.md`.

## 8. Commits from the 2026-08-02 night session

Branch `feature/donchian-crypto-ladder`, all pushed, guard PASS on each:

```
27a3a9d7  pre-register installer host preconditions before any run
027f6b33  record staging host provenance and an unrecorded prior effort
55bf677f  Gate A FAILS at A-2 - artifact ships CRLF, cannot run on Linux
aede7078  recon defect list - three blockers behind the A-2 failure
9b3d27c1  defect 4 - service needs credentials that Gate A forbids
```

## 9. Safety — unchanged and unbreached

No ARM, no order, no broker connection, no TESTNET, no mainnet, no wallet action, no credential value
at any point. The env file was never populated; `HL_LIVE_ACK` was never set. KVM2 was never touched.

**WP-V / the KVM2 install was deliberately NOT started.** The 2026-08-02 handoff requires telling
Barış before the KVM2 install begins even though standing approval exists — he was asleep, so it
waits. It is also now moot until the artifact is rebuilt.

Standing boundaries hold: DISARMED only; live-capital actions are never pre-authorised; never invent
position size, leverage, loss limits or credentials; never modify system/security settings even with
approval — hand him the command instead.

**Git delegation:** commit, push, PR and merge to master are delegated to the Lead — act, then report.
Migration execution, deployment, P2RT, runtime, broker/TESTNET/mainnet, force-push and starting a
brand-new task still need Barış explicitly.

## 10. Open owner actions

1. **Decide defect 4** (§3). Everything downstream of A-4 waits on it.
2. Authorise the rebuild of the WP-I candidate artifact (§5), accepting that the frozen anchors move.
3. Refresh `ZAI_GLM_CODING_PLAN_KEY` in Windows Credential Manager — auditor 4 returned
   `401 token expired or incorrect`. Needed for Audit 2's roster, not for Gate A.
4. Decide the fate of `KVM2-Ubuntu-2404-Staging` (§7).

## 11. Lessons this cycle added

1. **A hash-verified artifact can still be unrunnable.** Every prior WP-I check hashed files, and a
   CRLF file hashes perfectly. Verification of *identity* is not verification of *function*.
2. **A test suite that has never run on the target platform is not coverage.** The Linux tests caught
   the CRLF instantly — they had simply only ever been executed on Windows.
3. **Check which interpreter your baseline was measured on.** A floor recorded on Python 3.14 says
   nothing about a service that runs on 3.12.
4. **A check that passes because its target is absent is not a pass.** The A-4 script reported success
   on a connection-refused. Recorded openly rather than quietly dropped.
