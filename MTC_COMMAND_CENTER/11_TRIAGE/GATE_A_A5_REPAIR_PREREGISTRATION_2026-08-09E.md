# GATE A — A-5 READINESS-REPAIR PREREGISTRATION (run-kit E, 2026-08-09)

> **STATUS: FINAL REPAIR ROUND 3 — IMPLEMENTED LOCALLY; PENDING LEAD RE-AUDIT AND FRESH
> CANONICAL AUDITS. NOT ACCEPTED · NOT INTEGRATED · NOT COMMITTED · NOT PACKAGED · NOT
> TRANSFERRED · NOT RUN.** This
> document freezes the A-5 **rerun** command/evidence plan for run-kit revision **E** and the
> E *source* only. No gate result is claimed. **A-5 remains FAIL** under the frozen
> run-kit D evidence and **A-6..A-9 remain NOT RUN.** This document does not authorize
> execution: the A-5 rerun awaits the owner's existing preregistered authorization, an
> accepting canonical audit, and the Lead's own packaging/transfer/verification.
>
> **REPAIR ROUND 1 (2026-08-09).** The Codex Lead independently reproduced the D026 evidence
> for the first E draft (exact D `rc=1` / `RESULT=RED` / 14 checks 3 PASS 11 FAIL / 152 ms;
> first E draft `rc=0` / `RESULT=GREEN` / 14 of 14 PASS / 7935 ms; independent `bash -n` rc 0
> and `python -m py_compile` rc 0; hashes, byte counts, LF and CR-count-0 evidence
> reproduced) and returned **REQUEST_CHANGES** on a binding second defect: the first draft's
> `retry 30 post_start_ready` was **attempt-count bounded, not time bounded**, so with the
> listener present and the API stalled it could run for roughly **330 seconds** while the
> marker and every document claimed a 30 s ceiling. §4 below now records the repaired
> semantics — a real monotonic wall-clock deadline — and every false ceiling/attempt-count
> claim has been removed from the script, this document, the implementation record, the kit
> README and the live memory sections.
>
> **REPAIR ROUND 2 (2026-08-09) — the test's own `timeout` lookup.** The Lead re-audited
> round 1 and reproduced its evidence: **default exact D → RED** as required; **default E →
> RED with 27 of 28 PASS**, the single failure being
> `env_deadline_guard_available_and_working` because Python's `shutil.which("timeout")`
> selected `C:\Windows\system32\timeout.EXE` (rc `1`) rather than GNU coreutils `timeout`;
> and, with `C:\Program Files\Git\usr\bin` prepended to `PATH`, **the exact same E test →
> GREEN, 28 of 28 PASS, rc `0`** — the blocked 45 s probe ended in **3.7 s** under the 3 s
> deadline with **no surviving child**, and the pre-repair mutation took **18.8 s** against
> the repaired wait's **2.6 s**. The **round-1 source timing repair is therefore supported by
> real measurement**; the defect was in the **test**, which asked *Windows* where `timeout`
> was while both the script under test and the test's own behavioural harness ask *Bash*.
> Lead verdict: **REQUEST_CHANGES, repair round 2**, on the binding rule that the test must
> pass **via its documented default command on canonical Windows, with no undocumented `PATH`
> override**. §4.3 records the round-2 repair. `gatea_A5.sh` is **byte-identical to round 1**
> (SHA-256 `fe06f79e36432a8fa81e4a1c17dc470acd8d03099aa735faa76f737212451380`, `22531` bytes):
> round 2 changed the local regression test and the records only.
>
> **REPAIR ROUND 3 (2026-08-09) — FINAL. Readiness could be emitted past the deadline.** A
> fresh Codex `gpt-5.6-sol` xhigh canonical audit executed all mandatory evidence — exact D
> RED, E **GREEN 28 of 28**, `bash -n`, `python -m py_compile`, frozen-diff review, clean
> worktree — and returned **REQUEST_CHANGES** on one required **source** finding: in
> `wait_ready_deadline()` the **successful-probe branch** read the post-probe monotonic time
> and recorded it as the elapsed time, then returned `0` **without comparing it to the
> deadline**. The Lead reproduced the exact committed function at a one-second budget with the
> monotonic reading sequence `0, 0, 11`: `BOUNDARY_RESULT=SUCCESS`, `BOUNDARY_ELAPSED_DS=11`,
> `HARNESS_rc=0` — readiness declared at 1.1 s against a 1.0 s hard deadline. **The finding is
> binding and is accepted without qualification.** §4.5 records the repair and the exact
> equality boundary; §4.1 gains the corresponding row. Nothing in the round-1 mechanics is
> retracted — the deadline is monotonic, probes are hard-bounded and terminated, and backoff is
> clamped; the single missing guard was on the way *out* of a successful attempt. The script
> now emits `A5_kit_repair_round=3` (there was deliberately never a round-2 value: round 2 did
> not touch the script). **Round 3 is the last allowed source repair round** — a further
> non-accepting source verdict is a hard stop, not a round 4.

Candidate: `2ce41e34bceb599d80af24c5c33d835820ec321b` (credential-free DISARMED).
Worktree/branch of this repair unit: `C:\GA5E` on `codex/gatea-a5-readiness-e`, baseline
`123bb0c49129b29f625fb0c922968ddf8feaed06`. Implementer: **counterpart flagship
`claude-opus-5`** under the `AGENTS.md` two-tier model. Protected Gate-A evidence tooling
only — no product code or product artifact changed; no SSH/SCP, staging/service operation,
package/transfer/deploy, broker/exchange, ARM, order, TESTNET/mainnet, wallet, credential
read, or economic action was performed or is authorized by this unit. No Git command was run.

---

## 1. Recorded failed-D evidence (exact — this is what E repairs)

| Item | Value |
|---|---|
| Failed revision | run-kit **D**, `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/gatea_A5.sh` |
| Remote invocation | `bash /home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A5.sh` (once, preregistered key-only SSH route) |
| Exit code / elapsed | `1` / about `4.7 s` |
| Remote evidence log | `/home/gatea/gatea-A5-20260808D.log` |
| Local preserved copy | `C:\WPI_ARTIFACTS\gatea-A5-20260808D.log` |
| SHA-256 (remote **and** local — identical) | `3e282516dfea7e66d9196ad5f3d929b7d1a50257bae501a5b89c35e007eb31c9` |
| Bytes | `1933` |
| Remote file metadata | mode `664`, owner `gatea`, group `gatea` |
| Standalone record | `11_TRIAGE/GATE_A_A5_FAIL_2026-08-09D.md` |

**The failure.** All D pre-checks PASSED (`ActiveState=active`, `Restart=no`,
`MainPID=183225`, `NRestarts=0`, listener count 1 loopback-only, exact credential-free
DISARMED API, DB `quick_check=ok` / `app_state=DISARMED` / `schema_version=4` with the full
per-table counts). The frozen authorized SIGKILL
(`sudo systemctl kill --kill-whom=main --signal=SIGKILL mtc-bridge-first-start.service`) ran,
and the dead-window proof PASSED in full (`MainPID=0`, old PID `183225` gone, 3 s wait,
`ActiveState=failed`, no `:8790` listener, `NRestarts` unchanged at `0`, `Result=signal`,
`ExecMainStatus=9`). Exactly one `reset-failed` + `start` was performed; post `MainPID=187338`,
`NRestarts=0`, `Restart=no`. Then, **immediately after systemd reported active**, the
post-start listener check saw **`listener_count=0`** and the script printed:

```
RESULT=FAIL
A5_FAIL reason=post listener not loopback-only
```

with the `EXIT` trap recording **`rc=1`**.

**Independent safe-state proof a few seconds later (read-only) — PASS.** Unit loaded/static,
`active`/`running`, `MainPID=187338`, `Restart=no`, `NRestarts=0`, `Result=success`,
`ExecMainCode=0`, `ExecMainStatus=0`; listener count `1`, exactly `127.0.0.1:8790`,
non-loopback `0`; `GET /api/status` HTTP 200 exact credential-free DISARMED (mode
`credential_free_disarmed`, `state_version=1`, network/exchange_conn/credential_lookup
disabled, `exchange_enabled=false`, `arm_enabled=false`); DB `quick_check=ok`,
`app_state=DISARMED`, `schema_version=4`, **table counts exactly unchanged** from preflight;
recorded verdict line `POSTFAIL_SAFE_STATE=PASS`.

**Diagnosis (Lead, recorded).** A **reproduced run-kit readiness race**: D's post-start wait
was `retry 30 wait_active`, which returns the instant systemd reports `ActiveState=active`,
before the application has bound `127.0.0.1:8790`. It is **not** a product
persistence/DISARMED invariant failure — the persisted store stayed `DISARMED` /
`schema_version=4` with unchanged counts, `state_version` stayed `1`, the unit reached
`Result=success`, and the listener came up loopback-only.

**Because staging was independently proven safe, active, loopback-only, credential-free
DISARMED and DB-consistent, the preregistered conditional stop/mask response
(`GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` §5) was NOT required and was NOT performed.**

**Gate state (unchanged by this unit):** **A-0 · A-1 · A-2 · A-3 · A-4 PASS · A-5 FAIL ·
A-6 · A-7 · A-8 · A-9 NOT RUN.** A-5 cannot be promoted to PASS from the later diagnostics.

---

## 2. Scope of revision E

E is an **A-5-only repair kit**. It **supersedes run-kit D for the A-5 rerun ONLY**.

- **A-6..A-9 remain NOT RUN** and remain governed by the already-accepted run-kit D source
  until **A-5 PASSES and `_AI_MEMORY` is updated**. E ships no A-6..A-9 member.
- **Run-kit D is frozen failed evidence.** No D file, D report, or D evidence artefact is
  edited by this unit. The remote D kit and `/home/gatea/gatea-A5-20260808D.log` are
  preserved unchanged.
- E changes **no product code and no product artifact**. The accepted candidate
  `2ce41e34…` is untouched and its acceptance is unaffected.

---

## 3. Exact future E paths (frozen)

| Item | Value |
|---|---|
| Local kit dir | `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/` |
| Kit members (source) | `README.txt`, `gatea_A5.sh`, `test_gatea_A5_readiness.py` |
| Manifest | `SHA256SUMS` — created by the Lead at package time (4 packaged members total) |
| Local package tar | `C:\WPI_ARTIFACTS\gatea-run-kit-20260809E-2ce41e34.tar` |
| Remote tar | `/home/gatea/gatea-run-kit-20260809E-2ce41e34.tar` |
| Remote extraction dir (**new**) | `/home/gatea/gatea-run-kit-20260809E-2ce41e34` |
| A-5 invocation | `bash /home/gatea/gatea-run-kit-20260809E-2ce41e34/gatea_A5.sh` |
| **New** remote evidence log | `/home/gatea/gatea-A5-20260809E.log` |
| Local preserved copy of it | `C:\WPI_ARTIFACTS\gatea-A5-20260809E.log` |
| Frozen D log (**never touched**) | `/home/gatea/gatea-A5-20260808D.log` |
| Release SHA / app root | `2ce41e34…` / `/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE` |
| venv Python (`PY`) | `/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python` |
| systemd unit | `mtc-bridge-first-start.service` |
| State DB | `/var/lib/mtc-bridge/bridge.db` |
| API | `127.0.0.1:8790` (`GET /api/status` only; **never** `POST /api/arm`) |
| Env file | `/etc/mtc-bridge/mtc-bridge.env` — **never read by A-5, never printed** |
| Readiness deadline | `READY_MAX_S=30` s monotonic · `READY_POLL_S=1` s · `KILL_GRACE_S=2` s |
| Readiness prerequisites (new) | GNU coreutils `timeout` on `PATH`; readable `/proc/uptime` — both asserted in step1, never assumed |

**No-clobber rule (binding).** `gatea_A5.sh` refuses to run and exits `2` if its evidence log
already exists. `/home/gatea/gatea-A5-20260809E.log` must **not** exist before the rerun.
`/home/gatea/gatea-A5-20260808D.log` and `C:\WPI_ARTIFACTS\gatea-A5-20260808D.log` are
**never** overwritten, reused, appended to, or deleted. The E kit extracts to a **new** remote
directory; the D directory is not mutated.

---

## 4. The readiness repair (preregistered behaviour — repair rounds 1 and 3)

After the single explicit `sudo systemctl start "$UNIT"` and **before** the step5 post
assertions, `gatea_A5.sh` runs

```
wait_ready_deadline "$READY_MAX_S"      # READY_MAX_S=30 SECONDS, not 30 attempts
```

`ready_probe_once()` — one attempt — is satisfied **only when all three hold in the SAME
attempt**:

1. systemd `ActiveState=active` — via the existing `wait_active`;
2. a **nonempty loopback-only** `:8790` listener set — via the existing
   `check_listener_loopback_only` (LOCAL `ss` column index 3, never peer index 4);
3. `GET /api/status` HTTP 200 and **exact credential-free DISARMED** — via the existing
   `check_api` (`state=DISARMED`, `mode=credential_free_disarmed`, `state_version=1`,
   network/exchange_conn/credential_lookup disabled, `exchange_enabled=false`,
   `arm_enabled=false`).

It returns nonzero at the **first** failing check, so `ActiveState=active` alone can **never**
satisfy the wait. Only the **per-attempt diagnostic output** of the two heavyweight checks is
suppressed; the step5 assertions **re-run both checks in full, unsuppressed**, and remain the
authoritative post evidence — including `check_api`'s own `urllib` `timeout=10`, which the
readiness bounding does not touch.

### 4.1 What makes the 30 s real (the round-1 repair)

| Property | Mechanism |
|---|---|
| Monotonic clock | `mono_now_ds()` reads `/proc/uptime` (Linux `CLOCK_BOOTTIME`) in tenths of a second. It never steps backwards and never jumps on an NTP/operator clock change, which `$SECONDS` and `date +%s` both do. |
| One budget for everything | The deadline is fixed once, at the first line of `wait_ready_deadline`, immediately after the single explicit start. **Probe duration (active + listener + API) and the backoff between attempts are charged against that same budget.** There is no attempt counter anywhere in the readiness path. |
| Every attempt hard-bounded | `run_bounded` runs each attempt under GNU coreutils `timeout` with the **remaining** deciseconds as its bound. Without `--foreground`, `timeout` places the child in its **own process group** and signals the whole group, so `SIGTERM` at the bound — and `SIGKILL` `KILL_GRACE_S=2 s` later if the probe ignores `SIGTERM` — reaches the probe shell **and every descendant** (the venv python, its `ss` subprocess, a stalled socket read). **No probe child can outlive the bound.** rc 124 = bound expired. |
| Backoff cannot overshoot | The post-failure sleep is clamped to the remaining budget; the deadline is re-checked before every attempt and before every sleep. |
| **Success is bounded too (round 3)** | After a **successful** bounded probe the wait takes one more monotonic reading, records it as the elapsed time, and re-checks the deadline with the **same** rule as the other two guards. A probe that reports success only **at or after** the deadline is **not** readiness: the wait returns nonzero. See §4.5. |
| Nothing is written by a killed probe | A terminated readiness attempt only ever interrupts a read-only operation (`systemctl show`, `ss`, `GET /api/status`). |

**HONEST BOUND — stated identically in the script, the marker, the failure reason, the README
and this record.** The readiness operation returns at **30 s of monotonic time**, **plus at
most `KILL_GRACE_S` = 2 s** if and only if a probe ignores `SIGTERM` and must be `SIGKILL`ed,
**plus ordinary process-scheduling slop.** That is the entire claim. It is *not* a claim that
a probe may never take longer than one second, and it is *not* an attempt count.

### 4.2 New step1 preconditions (the deadline is asserted, never assumed)

The repair introduces two runtime prerequisites on the staging host — GNU coreutils `timeout`
on `PATH` and a readable `/proc/uptime`. Both are standard on the Debian/Ubuntu staging host;
neither is assumed. step1 records and asserts four items, all local and none of which touches
the unit, the DB, the API or any service state:

| Evidence line | Assertion |
|---|---|
| `A5_ready_clock=proc_uptime` | else FAIL — the deadline would not be monotonic |
| `A5_timeout_bin=<path>` | else FAIL — no deadline guard on `PATH` |
| `A5_timeout_guard_rc=124` | a 0.5 s bound on a 30 s sleep must really time out |
| `A5_ready_probe_export_rc=0` | the readiness functions must be visible in the bounded child shell (`export -f` transport) |

A missing or non-functional guard is a **precondition FAIL**, never a silent fall back to an
unbounded probe.

### 4.3 Outcomes

- **On success:** exactly one structured marker is printed —
  `A5_READY=yes ready_requires=active+loopback_only_listener_nonempty+exact_credential_free_disarmed_api ready_bound=monotonic_wall_clock_deadline ready_deadline_s=30 ready_clock=<clock> ready_probe_guard=timeout_TERM_then_KILL ready_kill_grace_s=2 ready_elapsed_s=<measured> ready_attempts=<n> ready_second_start=none`
  The marker is printed **only** when the post-probe monotonic reading is **strictly before**
  the deadline, so `ready_elapsed_s` can never exceed `ready_deadline_s` (§4.5).
- **On deadline expiry:** explicit `fail()` (`A5_FAIL reason=deadline: service did not become
  application-ready within the 30s monotonic wall-clock deadline …`), reporting the measured
  attempts and elapsed seconds, **nonzero exit**, **no second start**, no auto-restart, no
  mask. First-FAIL handling belongs to the Lead (§7). **This includes the round-3 case**: a
  probe that succeeded, but only once the deadline had been reached, is a deadline expiry and
  takes exactly this path.
- The proof is a wall-clock-bounded wait — **never** an unbounded wait, and **never** a fixed
  `sleep` used as the readiness proof.

**Nothing else changed vs frozen D.** The real `diff --strip-trailing-cr` between the frozen D
`gatea_A5.sh` and E is **still exactly eight hunks after round 3** — the round-3 edit lands
inside two hunks that already existed and creates none: `2c2`, `4a5,53`, `20c69,93`,
`46a120,123`, `53c130,136`, `172a256,387`, `188a404,423`, `229c464,465` — i.e. (1)
revision/date/header/path
wording, (2) the new no-clobber evidence log, (3) the readiness repair (constants block,
`mono_now_ds`, `run_bounded`, `ready_probe_once`, `wait_ready_deadline`, the `export -f`
transport line, the four step1 guard preconditions, the wait call and the single marker), and
(4) a **comment-only** truthfulness fix on D's `retry()` helper (it is attempt-count bounded,
not second bounded) whose code is byte-for-byte unchanged and which is still used, unchanged,
for the cheap step3 dead-window wait. Exactly **one** D line was replaced
(`retry 30 wait_active "service active again"`). `fail "` sites go 24 (D) → 28 (E): all 24
preserved, one readiness `fail` reworded in place, four new guard preconditions added. Every D
assertion, the dead-window proof, every DB/API/listener condition, every hard exclusion,
`fail()` behaviour, no-clobber behaviour, the authorized SIGKILL, the `Restart=no` requirement,
and the exactly-one-explicit-start contract are preserved unweakened.

### 4.4 Repair round 2 — the regression test resolves the deadline guard through Bash

**Round 2 changed no staging-side behaviour.** `gatea_A5.sh` is byte-identical to the round-1
file (SHA-256 `fe06f79e36432a8fa81e4a1c17dc470acd8d03099aa735faa76f737212451380`, `22531`
bytes, `466` LF lines), so §4.1–§4.3, §5, §6 and §7 above were untouched by round 2. At that
point the kit script still emitted `A5_kit_repair_round=1`, which correctly recorded the round
of the *script's* readiness repair. (Round 3 later changed that field to `3` and edited one
branch of `wait_ready_deadline` — see §4.5. The round-2 statements in this subsection are
preserved as the historical record of round 2 and are not re-asserted for the current source.)

The round-1 regression test located its GNU `timeout` with Python's
`shutil.which("timeout")`. That asks **Windows** where `timeout` is. The script under test does
not: it resolves `TIMEOUT_BIN="$(command -v timeout || true)"` and proves it in step1 with
`"$TIMEOUT_BIN" --signal=TERM --kill-after="$KILL_GRACE_S" 0.5 "${BASH:-bash}" -c 'sleep 30'`
— a **Bash** PATH lookup driving a **Bash** child. Neither does the test's own behavioural
harness, which runs the extracted `run_bounded` under `bash -s`. On a canonical Windows
workstation Windows answers `C:\Windows\system32\timeout.EXE`, an unrelated console-pause
command that cannot bound a child, so the environment check failed (rc `1`) while the mechanism
it was checking worked — the Lead's default run was RED at 27/28 with **only** that check
failing, and only a hand-prepended `PATH` made it GREEN at 28/28.

Round 2 removes the Windows lookup entirely. `probe_deadline_guard()` feeds a short guard
script to the **already-selected Bash** over the **same `bash -s` stdin transport the
behavioural harness uses** (non-login and non-interactive — a login shell could source a profile
adding directories the harness's own child shells never see, certifying a PATH the test does not
run under), and reports four `GUARD_*` facts that
`env_deadline_guard_available_and_working` requires together:

| Guard fact | Requirement |
|---|---|
| `GUARD_bin` — `command -v timeout` inside Bash | non-empty, **and not** under a Windows `system32` directory (both the native `C:\Windows\system32\…` and the MSYS `/c/Windows/system32/…` spellings are rejected) |
| `GUARD_version_rc` / `GUARD_version` — `timeout --version` | rc `0` and a version line identifying **GNU coreutils** |
| `GUARD_kill_rc` — `timeout --signal=TERM --kill-after=2 0.5 "${BASH:-bash}" -c 'sleep 30'` | rc **`124`** — the guard must really terminate a blocked child |

**Binding rule this encodes:** the test must reach GREEN via its **documented default command**
on canonical Windows with **no `PATH` override**, and a Windows `timeout.EXE` must **never** be
accepted. **Nothing was weakened to make the check pass** — the check became strictly stronger
(it now also proves the binary is GNU and mirrors the script's own bash-child kill probe), and
all **28** named checks were preserved with no renaming and no removal (round 3 later added a
twenty-ninth and renamed/removed none — §4.5). D025 rule 1 still binds: a genuinely missing,
non-GNU or non-functional guard still turns the run **RED**.

### 4.5 Repair round 3 — the deadline boundary on the success path (FINAL source round)

**The defect.** Round 1 checked the deadline before every attempt and before every backoff
sleep. It did **not** check it after a **successful** attempt. The branch read:

```bash
if run_bounded "$rem_ds" ready_probe_once; then
    now=$(mono_now_ds)
    READY_ELAPSED_DS=$(( now - t0 ))
    return 0                      # <-- no comparison of `now` against `deadline`
fi
```

so a probe reporting success only after the deadline had passed was accepted as readiness, and
the script could print its positive marker with `ready_elapsed_s` **larger than**
`ready_deadline_s`. Lead reproduction on the exact committed function, budget 1 s, monotonic
readings `0, 0, 11`: `BOUNDARY_RESULT=SUCCESS`, `BOUNDARY_ELAPSED_DS=11`, `HARNESS_rc=0`.

**The preregistered equality boundary, stated once and applied identically at all three
guards.** A monotonic reading `now` has **EXPIRED** the deadline when

```
now >= deadline      i.e.      deadline - now <= 0        EQUALITY IS EXPIRY
```

This is the rule round 1 already used at its two guards; round 3 does not redefine it, it
applies it at the third. All three guards use the same predicate form — `(( rem_ds <= 0 ))` on a
freshly computed `rem_ds=$(( deadline - now ))` — so the same reading
can never be treated as expired at one guard and in time at another. No existing
preregistration required a different rule.

**The repair (smallest correct change).**

```bash
if run_bounded "$rem_ds" ready_probe_once; then
    now=$(mono_now_ds)
    READY_ELAPSED_DS=$(( now - t0 ))
    rem_ds=$(( deadline - now ))
    if (( rem_ds <= 0 )); then
        return 1                  # succeeded, but only at/after the deadline: NOT readiness
    fi
    return 0
fi
```

`READY_ELAPSED_DS` and `READY_ATTEMPTS` are still set on **every** path, so the failure reason
reports what was really measured. A late success now takes the ordinary deadline-expiry path of
§4.3: `fail()`, nonzero exit, **no second start**, no auto-restart, no mask.

**Preserved unweakened by round 3.** Hard bounded termination (SIGTERM at the bound, SIGKILL
`KILL_GRACE_S=2 s` later, whole process group); exactly one explicit `reset-failed` + `start`;
the three-condition readiness definition (`ActiveState=active` **and** nonempty loopback-only
`:8790` listener **and** exact credential-free DISARMED `/api/status`) satisfied in **one**
attempt; the four step1 guard preconditions; the full unsuppressed step5 re-runs of
`check_listener_loopback_only` and `check_api` including its own `urllib timeout=10`; the
complete dead-window proof; the DB snapshot comparison; the no-clobber evidence-log guard; and
every hard exclusion. No named check was renamed, removed, weakened or skipped.

**Regression evidence (D026).** One focused named check is added —
`behaviour_probe_success_at_or_after_deadline_is_rejected` — bringing the total from **28** to
**29**. It runs the **real** `wait_ready_deadline`, the **real** `run_bounded` and the **real**
probe against real fast stubs, replacing **only** `mono_now_ds()` with a scripted reading
sequence (`0`, `0`, then a late reading), so a successful probe deterministically lands on a
post-probe reading that has reached the deadline. Both sides of the boundary are exercised —
exactly **at** the deadline (30 ds vs 30 ds) and **one decisecond past** it (31 ds vs 30 ds) —
and the wait must return nonzero for both while still recording the measured elapsed
deciseconds and one attempt. RED/GREEN pair, both recorded in the implementation record:

| Run | Required result |
|---|---|
| Exact pre-repair `61d88f12` source, materialized **outside** the repo | **RED**, `total=29 passed=28 failed=1`, the single failure being this check, `HARNESS_rc=0` for both readings |
| Repaired E source | **GREEN**, `total=29 passed=29 failed=0`, `HARNESS_rc=1` for both readings |
| Exact frozen run-kit D (preserved broader control) | **RED**, unchanged in role |

---

## 5. Acceptance criteria — A-5 rerun under E

A-5 is **PASS** only if the single run of `gatea_A5.sh` from the E extraction path ends with
exactly `A-5 PASS`, the `EXIT` trap records `rc=0`, and **every** item below holds in the
preserved evidence log:

**Preconditions (step1).** `ActiveState=active`; `Restart=no`; numeric `MainPID>0` (captured
as the pre PID); numeric `NRestarts` (captured); **the four new readiness-deadline guards of
§4.2 — `A5_ready_clock=proc_uptime`, a non-empty `A5_timeout_bin`, `A5_timeout_guard_rc=124`,
`A5_ready_probe_export_rc=0`**; listener check PASS (nonempty, loopback-only); API check PASS
(exact credential-free DISARMED); DB snapshot PASS (`quick_check=ok`, `app_state=DISARMED`,
`schema_version=4`, full sorted per-table counts recorded).

**Kill + dead window (steps 2–3).** The exact authorized command
`sudo systemctl kill --kill-whom=main --signal=SIGKILL mtc-bridge-first-start.service`;
`MainPID=0` and the old `/proc/<pre PID>` gone within the bounded wait; the 3-second sleep
completed; `ActiveState` `failed` or `inactive`; **no** `:8790` listener; `NRestarts`
unchanged; `Result=signal`; `ExecMainStatus=9`.

**Restart + readiness (step 4).** Exactly one `reset-failed` and exactly one `start`; then
`wait_ready_deadline "$READY_MAX_S"` succeeds inside the 30 s monotonic deadline and the single
`A5_READY=yes …` marker is present, carrying `ready_bound=monotonic_wall_clock_deadline`,
`ready_deadline_s=30`, `ready_clock=proc_uptime`, `ready_probe_guard=timeout_TERM_then_KILL`,
`ready_kill_grace_s=2`, a measured `ready_elapsed_s` **strictly below 30.0** (round 3: equality
is expiry, so a marker carrying exactly `30.0` or more is impossible and, if it ever appeared,
would itself be a FAIL), a measured `ready_attempts`, and `ready_second_start=none`.

**Post assertions (step 5).** New numeric `MainPID>0` that differs from the pre PID;
`NRestarts` unchanged; `Restart=no`; the **full unsuppressed** listener check PASS; the
**full unsuppressed** exact credential-free DISARMED API check PASS; DB snapshot PASS; and
`A5_dbsnap_identical=yes` (the recomputed logical snapshot is byte-identical to the pre
snapshot).

**Independent Lead verification (outside the script, read-only).** Before assigning the
verdict the Lead independently confirms: the evidence log did not exist beforehand;
`sha256sum -c SHA256SUMS` OK for the extracted kit; the unit is loaded/static, active/running,
`Restart=no`, `NRestarts=0`, `Result=success`, `ExecMainStatus=0`; listener count 1, exactly
`127.0.0.1:8790`, non-loopback 0; the API exact credential-free DISARMED with
`state_version=1`; DB `quick_check=ok`, `app_state=DISARMED`, `schema_version=4` with table
counts unchanged from preflight; and the E evidence-log SHA-256 + byte size on both the remote
and the local preserved copy.

**A readiness-deadline expiry is a genuine FAIL**, not a retryable condition — and so is any
of the four step1 deadline-guard precondition failures. Any nonzero exit, any `A5_FAIL` line,
or any missing item above is a FAIL. **A-5 must not be promoted to PASS from post-failure
diagnostics** — that rule produced the honest D verdict and it still binds.

---

## 6. Invocation (A-5 only)

```
bash /home/gatea/gatea-run-kit-20260809E-2ce41e34/gatea_A5.sh
```

Run **once**, as the `gatea` user over the preregistered key-only SSH route, with
`/home/gatea/gatea-A5-20260809E.log` confirmed absent beforehand. **Do not run A-6..A-9 from
this kit** — E contains no A-6..A-9 member. **A-6 remains BLOCKED** until A-5 PASSES **and**
`_AI_MEMORY/NEXT_STEPS.md`, `_AI_MEMORY/GLOBAL_HANDOFF.md`, and
`11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` are updated. Only then does the sequence
continue under run-kit D: A-6 → A-7 → A-8 (remote + host) → A-9, one gate at a time with a
memory update before each.

---

## 7. First-FAIL response (unchanged from `GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` §5)

At the first genuine FAIL: **preserve the evidence log** (never overwrite/reuse it), run only
**read-only** diagnostics as needed, then **STOP**. Do **not** run A-6. Do **not** rerun A-5
without a new preregistered revision and a new evidence-log identifier. If — and only if —
the failure leaves the service in an unsafe state, safe-stop and mask the unit
(`sudo systemctl stop mtc-bridge-first-start.service`, then
`sudo systemctl mask mtc-bridge-first-start.service`) and write the result + memory. A
script's own internal failure triggers **no** auto-restart and **no** mask; the Lead performs
the safe first-FAIL response. Record the honest verdict, the exact failure line, the evidence
log SHA-256/bytes, and the independent safe-state proof — exactly as the D FAIL was recorded.

---

## 8. Package / transfer verification requirements (Lead-owned, only after an accepting audit)

1. **Build from raw committed blobs.** Create the tar from `git cat-file blob` output — **not**
   from a bare `git archive` on Windows. The D round proved `git archive` exports CRLF here;
   that tar was rejected before transfer and preserved as
   `…-2ce41e34.rejected-crlf.tar`. This repo's Windows checkout can present tracked `.sh`
   files with CRLF, so worktree copies must not be trusted for packaging.
2. **Pre-transfer verification.** Every member LF-only (**CR count 0**); the exact member set
   (`README.txt`, `gatea_A5.sh`, `test_gatea_A5_readiness.py`, `SHA256SUMS`); per-member
   SHA-256 + byte count + LF count; tar SHA-256, tar byte size, tar member count; `bash -n`
   on `gatea_A5.sh`; every embedded Python heredoc compiles.
3. **Transfer + extract** to the **new** path `/home/gatea/gatea-run-kit-20260809E-2ce41e34`.
   Do not mutate, overwrite, or extract over the frozen D directory.
4. **Remote re-verification.** Identical tar SHA-256/bytes/member set; `sha256sum -c
   SHA256SUMS` all OK; `bash -n gatea_A5.sh` rc 0; every member CR count 0; byte/LF counts
   match the pre-transfer record; `/home/gatea/gatea-A5-20260809E.log` absent. **Plus the two
   runtime prerequisites the round-1 repair introduces** (read-only; the script asserts both
   itself in step1, but confirming first avoids burning the one no-clobber evidence-log
   identity on a missing tool): `command -v timeout && timeout --version | head -1`, and
   `test -r /proc/uptime && head -c 40 /proc/uptime`.
5. **Only `gatea_A5.sh` is ever executed on staging.** `test_gatea_A5_readiness.py` is a
   local-only regression artifact and must not be invoked on the VM.
6. **No Gate-A script runs** during packaging, transfer, extraction, or verification.

---

## 9. Required audit before any rerun (AGENTS.md canonical roster · D025 · D026)

This is a **new runtime-defect repair unit** on a protected Gate-A evidence surface. The three
prior run-kit D source-review rounds do **not** count as testing this runtime defect.

1. **Lead independent inspection** of the actual E diff and files — never the implementer's
   self-report — plus reproduction of the RED/GREEN, `bash -n`, `py_compile`, heredoc-compile
   and CR-byte evidence on real source.
2. **Fresh canonical audits** in new independent sessions: `claude-opus-5` at effort `xhigh`
   and `gpt-5.6-sol` at effort `xhigh` (protected surface ⇒ xhigh, not `high`). Exact
   model/effort unavailable ⇒ **BLOCK** unless Barış explicitly waives it.
3. **D025 rules bind:** an auditor that cannot execute the mandated checks must return
   **BLOCK**; acceptance requires accepting verdicts from **both** flagship auditors plus no
   unresolved reproduced required finding from **any** canonical auditor; any required finding
   from any canonical auditor is binding once the Lead reproduces it on real source; a finding
   the Lead cannot reproduce is recorded as unreproduced with its evidence, never silently
   dropped. (ClinePass/DeepSeek auditor 3 availability must be checked, not assumed.)
4. **D026 binds, and now covers BOTH defects:** the readiness regression test is closure
   evidence only with a demonstrated **RED** against the exact frozen pre-fix D script and
   **GREEN** against E, with the real commands and their real output recorded. For the
   round-1 timing defect the falsification is executed **inline on every run** — the test
   drives the **verbatim pre-repair readiness construct** (the script's own `retry` helper
   plus the old `post_start_ready`) against an 8 s-blocking API stub with a nominal bound of
   2, and requires it to be **measured overrunning** that bound (~17 s), while the repaired
   wait under identical stubs and the identical nominal bound must return nonzero at the
   deadline in under half that wall time. A second scenario blocks a probe for 45 s under a
   3 s deadline and requires both a bounded exit and proof that **the probe process is gone**
   afterwards. Auditors must **verify** that demonstration rather than accept the claim, and
   must state whether they verified it. `env_deadline_guard_available_and_working` makes
   non-execution visible: if GNU `timeout` is missing, is not GNU, or does not return 124 on a
   blocked child the test goes **RED**, never a green it did not earn (D025 rule 1).
   **Round 2 adds a binding execution rule:** both runs must be made with the **documented
   default command exactly as printed**, from the repo root, with **no `PATH` override and no
   other environment edit**. A GREEN that required a hand-edited `PATH` is **not** acceptance.
   Auditors must record the resolved `GUARD_bin` path reported by the environment check.
   **Round 3 adds a third required demonstration:** the boundary RED/GREEN pair of §4.5. The
   RED is run against the exact pre-repair `61d88f12` blob **materialized outside the repo**
   (`git show 61d88f12054cdc81896ca7596c699aff1a7b9a71:<kit path>/gatea_A5.sh`; `22531` bytes,
   CR 0, SHA-256 `fe06f79e36432a8fa81e4a1c17dc470acd8d03099aa735faa76f737212451380`), and must
   show `total=29 passed=28 failed=1` with the single failure being
   `behaviour_probe_success_at_or_after_deadline_is_rejected` at `HARNESS_rc=0`. The GREEN
   against E must show `total=29 passed=29 failed=0` with that check at `HARNESS_rc=1` for both
   the equality reading and the past-the-deadline reading. **Run-kit D is never modified**, and
   its own RED remains the separate broader control.
5. **Repair-loop bound:** maximum 3 repair/re-audit rounds. **Round 1 was consumed** by the
   Lead's REQUEST_CHANGES on the false wall-clock bound, **round 2 by the REQUEST_CHANGES on
   the test's Windows `timeout` lookup**, and **round 3 — the final round — by the reproduced
   success-path deadline-boundary defect (§4.5)**. **No round remains.** A further
   non-accepting source verdict is a hard stop: stop and report to Barış rather than repairing
   again.

Only after an accepting audit may the Lead package, transfer, verify, and rerun A-5.

---

## 10. Routing / authority record

```
Classification      : Tier 4 — protected Gate-A restart/readiness evidence tooling (run-kit repair)
Protected           : yes — the script exercises a DISARMED staging service; it changes no product code
Role                : counterpart flagship IMPLEMENTER (AGENTS.md two-tier); Lead owns scope/acceptance
Model + provider    : claude-opus-5 (Claude Max account route)
Sub-delegation      : none — protected repair retained by the flagship implementer
Exact write paths   : 11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/{README.txt,gatea_A5.sh,
                      test_gatea_A5_readiness.py};
                      11_TRIAGE/GATE_A_A5_REPAIR_PREREGISTRATION_2026-08-09E.md;
                      11_TRIAGE/GATE_A_A5_REPAIR_IMPLEMENTATION_2026-08-09E.md;
                      11_TRIAGE/GATE_A_A5_E_CANONICAL_AUDIT_ROUND1_2026-08-09.md;
                      _AI_MEMORY/{NEXT_STEPS.md,GLOBAL_HANDOFF.md};
                      11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md
Execution performed : ROUND 3 — the interpreters ran. `bash -n`, `python -m py_compile` with the
                      byte-cache outside the repo, and all three D026 runs (exact D control RED,
                      exact pre-repair `61d88f12` RED, repaired E GREEN) were executed with the
                      documented default commands and no PATH override, plus read-only file
                      evidence (bytes, SHA-256, CR/LF counts) and `git diff --check` /
                      `git status`. Rounds 1–2 were BLOCKED at this step; that block is now
                      cleared. Only read-only Git plumbing (`show`, `diff`, `status`) was used.
                      One file was written outside the repo, under `C:\tmp`: the materialized
                      pre-repair blob used for the RED.
Not performed       : Git, SSH/SCP, staging/service action, package/transfer/deploy, broker/
                      exchange, ARM, orders, TESTNET/mainnet, wallet, credential read, economic action
External API credits: no
```

---

## 11. Authorization boundary & hard exclusions

Existing owner authorization covers the preregistered A-5..A-9 sequence; this revision
re-scopes only the **A-5 rerun** onto repaired tooling with a new evidence-log identity. Hard
exclusions unchanged: **no credential value, no broker/exchange access, no successful ARM, no
order, no TESTNET/mainnet, no wallet, no master merge, no economic action.** The service
intentionally remains active/static, loopback-only, credential-free DISARMED
(`state_version=1`), no broker connection, no credentials — the prerequisite for A-5. No
product/artifact change; no gate result claimed; no prohibited action performed.

---

## 12. Records (companion, read order)

- `11_TRIAGE/GATE_A_A5_REPAIR_IMPLEMENTATION_2026-08-09E.md` — the E implementation record and
  the D026 RED/GREEN + syntax/compile/CR evidence.
- `11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/README.txt` — E invocation, validation, packaging,
  transfer, execution, post-run hashing.
- `11_TRIAGE/GATE_A_A5_FAIL_2026-08-09D.md` — the frozen A-5 D FAIL evidence this repairs.
- `11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` — A-5..A-9 criteria, shared script
  contract, **§5 first-FAIL response** (still governing A-6..A-9).
- `11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/README.txt` — the frozen D kit (A-6..A-9 remain here).
- `11_TRIAGE/GATE_A_RUN_KIT_D_PACKAGE_TRANSFER_2026-08-09.md` — the D package/transfer record
  (source of the CRLF/`git archive` lesson in §8).
- `_AI_MEMORY/GLOBAL_HANDOFF.md`, `_AI_MEMORY/NEXT_STEPS.md`,
  `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` — live state (newest section first).
