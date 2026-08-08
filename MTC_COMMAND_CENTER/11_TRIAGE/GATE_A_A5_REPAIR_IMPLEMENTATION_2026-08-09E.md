# GATE A — A-5 READINESS REPAIR, IMPLEMENTATION RECORD (run-kit E, 2026-08-09)

## LEAD RE-AUDIT ACCEPTANCE CHECKPOINT — repair round 2 (2026-08-09)

With no PATH override, exact D returned `rc=1`, `RESULT=RED`; E returned `rc=0`, `RESULT=GREEN`,
**28/28 PASS**. The guard resolved `/usr/bin/timeout` through selected Git Bash, identified GNU
coreutils 8.32, and proved rc124. A 45 s probe ended in 3.6 s under deadline3 with no surviving
child; the pre-repair mutation took 18.7 s while repaired E took 2.5 s. Independent `bash -n` and
`python -m py_compile` returned 0; all E artifacts are UTF-8/LF CR0; source SHA-256 remains
`fe06f79e36432a8fa81e4a1c17dc470acd8d03099aa735faa76f737212451380`.

**Lead preliminary verdict: ACCEPT for canonical audit dispatch.** Not final Gate-5 acceptance:
packaging/staging remain blocked pending fresh canonical auditors.

---

## REPAIR ROUND 2 — the regression test resolves GNU `timeout` through the selected Bash
## (round 1 — the hard monotonic wall-clock readiness deadline — is unchanged and stands)

> **STATUS: ROUND 2 IMPLEMENTED LOCALLY; PENDING LEAD RE-AUDIT AND CANONICAL AUDITS.**
> Revision E is **NOT accepted, NOT committed, NOT packaged, NOT transferred, NOT run.** A-5
> has **not** been rerun. Gate state is unchanged: **A-0..A-4 PASS · A-5 FAIL (run-kit D) ·
> A-6..A-9 NOT RUN.** Run-kit D and all D evidence are immutable and untouched; staging is
> unchanged and safe.
>
> **`gatea_A5.sh` WAS NOT TOUCHED IN ROUND 2.** Its SHA-256 is still
> `fe06f79e36432a8fa81e4a1c17dc470acd8d03099aa735faa76f737212451380` at `22531` bytes / `466`
> LF lines — byte-identical to the round-1 file and re-verified this session (§7, E12). Round 2
> changed **only** the local regression test and the records. The script therefore still emits
> `A5_kit_repair_round=1`, which correctly names the round of the *script's* readiness repair.
>
> **The Lead's round-1 evidence is real, is preserved verbatim in §1.1, and supports the
> source repair.** Default exact D → RED as required; default E → RED at **27 of 28 PASS**
> with the **single** failure being `env_deadline_guard_available_and_working`; and the **exact
> same E test with `C:\Program Files\Git\usr\bin` prepended to `PATH` → GREEN, 28 of 28,
> rc `0`**, with the blocked 45 s probe ending in **3.7 s** under a 3 s deadline, **no
> surviving child**, and the pre-repair mutation at **18.8 s** against the repaired wait's
> **2.6 s**. The defect was in the **test**, not the script: it asked *Windows* where `timeout`
> was, and Windows answered `C:\Windows\system32\timeout.EXE`.
>
> **D026 IS STILL NOT SATISFIED BY THIS UNIT — READ §8 BEFORE TREATING THIS AS CLOSURE
> EVIDENCE.** The round-2 default RED/GREEN runs **could not be executed in this session
> either**: `bash`, `bash -lc`, `bash -n`, `python <script>`, `python --version` and
> `python -m py_compile` were all refused with `This command requires approval`, and filesystem
> access outside `C:\GA5E` is sandboxed off. This is recorded as a **BLOCK on the round-2
> demonstration**, not as a pass. Per `AGENTS.md` D026 the test remains **supplemental — not
> closure evidence** until the Lead runs it; §8 gives the exact commands and pass criteria.

Implementer: **counterpart flagship `claude-opus-5`** (AGENTS.md two-tier model), isolated
worktree `C:\GA5E`, branch `codex/gatea-a5-readiness-e`, baseline
`123bb0c49129b29f625fb0c922968ddf8feaed06`. Candidate unchanged:
`2ce41e34bceb599d80af24c5c33d835820ec321b`.

**Actions NOT performed by this unit:** no Git command of any kind (no commit, reset,
checkout, stash, clean, revert, delete); no SSH/SCP; no staging or service operation; no
package/transfer/deploy; no broker/exchange access; no ARM; no order; no TESTNET/mainnet; no
wallet; no credential read or print; no economic action; no Gate-A execution; no product code
or product artifact change; no edit to run-kit D or to any D report/evidence file; no
sub-delegation.

---

## 1. The binding Lead finding this round repairs

The Codex Lead independently ran D026 against the **first E draft** and inspected the real
source. That evidence is preserved exactly:

| Item | Result |
|---|---|
| Exact pre-fix **D** `gatea_A5.sh` | `rc=1`, `RESULT=RED`, **14 checks — 3 PASS / 11 FAIL**, `152 ms` |
| **First E draft** | `rc=0`, `RESULT=GREEN`, **14 of 14 PASS**, `7935 ms` (delayed listener/API ready on attempt 3 after 2 s; active-only timed out under test bound 3; listener-up/API-not-exact timed out under bound 2; no forbidden command ran) |
| Independent `bash -n` | rc `0` |
| Independent `python -m py_compile` | rc `0` |
| Line endings / hashes | all three kit members and both reports UTF-8/LF, **CR count 0**; reported hashes and byte counts reproduced |

So the combined active + listener + exact-API logic **does** discriminate defect 1 (the
run-kit D readiness race). The Lead then returned **REQUEST_CHANGES** on a second, binding
defect:

> `retry 30 post_start_ready` is **attempt-count bounded, not time bounded.**
> `post_start_ready` calls `check_api`, whose `urllib.request.urlopen(..., timeout=10)` may
> consume ten seconds per attempt, and `retry` sleeps one second after each failure. With the
> listener present and the API stalled the wait can take about **330 seconds**. The source
> comments, the preregistration/README/records, and the structured marker
> `ready_max_wait_s=30` were therefore **false**. The immediate-return regression stubs could
> not detect it.

**Both statements are accepted without qualification.** The false claim has been removed from
the script, this record, the preregistration, the kit README and the live memory sections, and
the test now fails the script if any wording of it returns.

### 1.1 The binding Lead finding round 2 repairs (round-1 re-audit, recorded verbatim)

| Run | Result |
|---|---|
| Default exact pre-fix **D** | **RED**, as required |
| Default repaired **E** | **RED — 27 of 28 PASS.** The *only* failing check was `env_deadline_guard_available_and_working`, because Python's `shutil.which("timeout")` selected `C:\Windows\system32\timeout.EXE` and it returned rc `1` |
| Same **E** test with `C:\Program Files\Git\usr\bin` prepended to `PATH` | **GREEN — 28 of 28 PASS, rc `0`.** The 45 s blocked probe ended in **3.7 s** under the 3 s deadline; **no child survived**; the pre-repair mutation measured **18.8 s** against the repaired wait's **2.6 s** |

**What that evidence establishes, stated honestly in both directions.** The round-1 *source*
timing mechanics are **supported by real measurement** — the deadline really terminates a
blocked probe, really leaves no survivor, and really beats the pre-repair construct by ~7× on
identical stubs. But the *test* was defective: it resolved its deadline guard through Windows
while both the script under test and its own behavioural harness resolve theirs through Bash.

> **Lead verdict: REQUEST_CHANGES, repair round 2.** *The test must pass via its documented
> default command on canonical Windows without an undocumented `PATH` override. Resolve and
> execute GNU coreutils `timeout` through the selected Bash environment. Do not accept Windows
> `timeout.EXE`. Keep the production harness evaluation under Bash and preserve every existing
> check.*

**Accepted without qualification.** A green that only appears after a hand-edited `PATH` is not
acceptance — it is an undocumented precondition hidden inside the acceptance step, which is the
same class of defect as the false 30 s ceiling round 1 repaired. §6.1 records the fix.

---

## 2. Files changed (the complete write set — nothing else was written)

**Kit E members (rewritten in place)**

| # | Path | Bytes | LF lines | CR bytes | SHA-256 | Round 2 |
|---|---|---|---|---|---|---|
| 1 | `11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/README.txt` | `29397` | `415` | `0` | `56d688653f90b9cafaed2b57b85455d5b89dd9197b9058e2d49a07969fa097d8` | **rewritten** |
| 2 | `11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/gatea_A5.sh` | `22531` | `466` | `0` | `fe06f79e36432a8fa81e4a1c17dc470acd8d03099aa735faa76f737212451380` | **UNCHANGED — byte-identical to round 1** |
| 3 | `11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/test_gatea_A5_readiness.py` | `53208` | `1164` | `0` | `67823a70d3d4854404cfd15372cd1cf90bb0d6a820caf9858a0448f52ed59c8f` | **rewritten** |

These three are the values a Lead re-hash must reproduce. Rows 1 and 3 **supersede** their
round-1 values (README `8127afb3…`/`25117`, test `f5651aa6…`/`47557`), which identify the
round-1 draft and must not be used for packaging. Row 2 is **deliberately identical** to the
round-1 value — that identity is the proof that round 2 changed nothing on the staging side. The
round-0 values (`gatea_A5.sh` `2a8521b6…`/`12960`, test `a32f85fc…`/`23140`, README
`bdd63847…`/`16847`) identify the **discarded first E draft** and must never be used.

**Reports (updated in place)**

| # | Path | Bytes | LF lines | CR bytes |
|---|---|---|---|---|
| 4 | `11_TRIAGE/GATE_A_A5_REPAIR_PREREGISTRATION_2026-08-09E.md` | `32077` | `478` | `0` |
| 5 | `11_TRIAGE/GATE_A_A5_REPAIR_IMPLEMENTATION_2026-08-09E.md` | ~`47960` | ~`645` | `0` |

Files 4–5 are prose records, are not packaged, and their SHA-256 is deliberately not
self-referenced. Row 5's byte/line counts are the values immediately before this sentence's own
final edit and are recorded for scale, not as an identity.

**Live memory (newest section prepended; no existing content edited)**

6. `_AI_MEMORY/NEXT_STEPS.md` — CRLF preserved, `2991`/`2991` (§7b E15)
7. `_AI_MEMORY/GLOBAL_HANDOFF.md` — `5411`/`5411` (§7b E16 + disclosure)
8. `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` (filename intentionally unchanged) —
   `1040`/`1040`

**Not touched:** every run-kit D file, every D report/evidence file, all product code, all
product artifacts, every other repo file.

> **Note on the superseded draft.** The first E draft was uncommitted, so repairing it replaced
> it in place; it no longer exists on disk. Its identity is preserved by the hashes above, and
> **its exact readiness construct is preserved verbatim inside the regression test** as
> `PRE_REPAIR_POST_START_READY` (driven by the script's own real `retry` helper), which is what
> the round-1 falsification scenario executes.

---

## 3. The authoritative D → E delta (real `diff` output, this session)

Command (read-only; `--strip-trailing-cr` because this repo's Windows checkout presents the
tracked D `.sh` with CRLF while the E members are authored LF-only):

```
diff --strip-trailing-cr \
  MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/gatea_A5.sh \
  MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/gatea_A5.sh
```

Result: **exactly eight hunks, nothing else differs.** This delta is a **round-1** artefact and
is reproduced here unchanged: round 2 did not touch `gatea_A5.sh`, and its SHA-256 is identical
to the round-1 value (§2 row 2, re-verified in §7 E12).

| Hunk | Change | Category |
|---|---|---|
| `2c2` | header revision/date wording | (1) wording |
| `4a5,37` | E scope/supersession block **and the REPAIR ROUND 1 timing-contract block** | (1) wording |
| `20c53,77` | `LOG=` → `/home/gatea/gatea-A5-20260809E.log`, **plus the `E READINESS DEADLINE CONSTANTS` block and the two marker globals** | (2) new log + (3) repair |
| `46a104,107` | four new header evidence echoes (`A5_kit_revision`, `A5_kit_repair_round`, `A5_readiness`, `A5_supersedes`) | (1) wording |
| `53c114,120` | `# retry <max_seconds>` → `# retry <max_attempts>` plus six explanatory comment lines | (4) **comment-only** truthfulness fix; `retry`'s code is byte-for-byte unchanged |
| `172a240,356` | new `mono_now_ds()`, `run_bounded()`, `ready_probe_once()`, `wait_ready_deadline()` + their comments + the `export`/`export -f` transport line | (3) repair |
| `188a373,392` | the four step1 readiness-deadline preconditions and their evidence lines | (3) repair |
| `229c433,434` | `retry 30 wait_active "service active again"` → `wait_ready_deadline "$READY_MAX_S"` with a truthful `fail` reason, plus one structured readiness marker | (3) repair |

**Exactly one D line was replaced** (`retry 30 wait_active …`) besides the header and `LOG=`
lines; **no D assertion was deleted.** `fail "` sites: **D 24 → E 28** — all 24 preserved, the
readiness `fail` reworded in place, and **four added** (the new guard preconditions). The
`retry` helper itself is still present and still used, unchanged, for the cheap step3
dead-window wait, whose probe is one `systemctl show` plus a `/proc` test.

---

## 4. Preserved unweakened (verified against the diff above)

`set -Eeuo pipefail`; the no-clobber evidence-log guard (`exit 2`); the stdout+stderr redirect
into the log; the `EXIT` trap recording the exact rc; `fail()` semantics; the `getprop` helper;
the `retry` helper's **code**; `check_api` **verbatim** (HTTP 200, `state=DISARMED`,
`mode=credential_free_disarmed`, `state_version=1`, network/exchange_conn/credential_lookup
disabled, `exchange_enabled=false`, `arm_enabled=false`, **and its own `urllib` `timeout=10`**);
`check_listener_loopback_only` verbatim (nonempty set, every local address loopback, `ss` LOCAL
column index **3**, never peer index 4, `>= 5` fields required); `db_snapshot` verbatim; every
D step1 precondition; the authorized SIGKILL
`sudo systemctl kill --kill-whom=main --signal=SIGKILL "$UNIT"`; the complete dead-window proof
(`MainPID=0`, old `/proc/PID` gone, `sleep 3`, `ActiveState` failed/inactive, **no** `:8790`
listener, `NRestarts` unchanged, `Result=signal`, `ExecMainStatus=9`); **exactly one**
`reset-failed` and **exactly one** `start`; every step5 post assertion (new numeric `MainPID>0`
differing from the pre PID, `NRestarts` unchanged, `Restart=no`, the **full unsuppressed**
listener check, the **full unsuppressed** exact-DISARMED API check, the DB snapshot,
`A5_dbsnap_identical=yes`); the venv Python for all JSON/SQLite work; no `POST /api/arm`; the
env file is never read; all hard exclusions; and no auto-restart/mask on the script's own
failure.

---

## 5. The repaired readiness semantics

```bash
# constants block (extracted verbatim by the regression test)
READY_MAX_S=30            # WALL-CLOCK seconds, not attempts
READY_POLL_S=1
KILL_GRACE_S=2            # bounded SIGTERM -> SIGKILL escalation
TIMEOUT_BIN="$(command -v timeout || true)"
MONO_CLOCK=bash_seconds
if [[ -r /proc/uptime ]]; then MONO_CLOCK=proc_uptime; fi

mono_now_ds()  # /proc/uptime (CLOCK_BOOTTIME) in tenths of a second
run_bounded()  # "$TIMEOUT_BIN" --signal=TERM --kill-after="$KILL_GRACE_S" <remaining> bash -c <fn>
ready_probe_once()      # wait_active || return 1; listener || return 1; api || return 1
wait_ready_deadline()   # fixes the deadline once; charges probes AND backoff to it

sudo systemctl start "$UNIT"
if ! wait_ready_deadline "$READY_MAX_S"; then fail "deadline: … no second start performed"; fi
echo "A5_READY=yes … ready_bound=monotonic_wall_clock_deadline ready_deadline_s=30 …"
```

| Property | Mechanism |
|---|---|
| **Monotonic** | `mono_now_ds()` reads `/proc/uptime`, Linux `CLOCK_BOOTTIME` — never steps backwards, never jumps on an NTP/operator clock change (which `$SECONDS` and `date +%s` both do). |
| **One budget for everything** | The deadline is fixed once at the first line of `wait_ready_deadline`, called immediately after the single explicit start. Active/listener/API probe duration **and** inter-attempt backoff are charged against it. There is **no attempt counter anywhere in the readiness path**. |
| **Every attempt hard-bounded by the remaining budget** | `run_bounded` runs the attempt under GNU coreutils `timeout` with the remaining deciseconds as its bound. Without `--foreground`, `timeout` places the child in its **own process group** and signals the whole group, so `SIGTERM` at the bound — and `SIGKILL` `KILL_GRACE_S` later if the probe ignores `SIGTERM` — reaches the probe shell **and every descendant** (the venv python, its `ss` subprocess, a stalled socket read). rc 124 = bound expired. **No probe child can outlive the bound.** |
| **Backoff cannot overshoot** | The post-failure sleep is clamped to the remaining budget; the deadline is re-checked before every attempt and before every sleep. |
| **Nothing written by a killed probe** | A terminated attempt only ever interrupts a read-only operation (`systemctl show`, `ss`, `GET /api/status`). |
| **Final evidence untouched** | step5 still re-runs `check_listener_loopback_only` and `check_api` in full and unsuppressed, and `check_api` keeps its own `urllib` `timeout=10`. Only the readiness path is bounded by the remaining deadline. |

**The honest bound, stated identically in the script, the marker, the failure reason, the
README, the preregistration and here:** the readiness operation returns at **30 s of monotonic
time**, **plus at most `KILL_GRACE_S` = 2 s** if and only if a probe ignores `SIGTERM` and must
be `SIGKILL`ed, **plus ordinary process-scheduling slop.** That is the whole claim. It is not a
claim that a probe may never take longer than one second, and it is not an attempt count.

**The deadline is asserted, not assumed.** The repair introduces two runtime prerequisites on
the staging host — GNU coreutils `timeout` on `PATH`, and a readable `/proc/uptime`. Both are
standard on the Debian/Ubuntu staging host; both are checked in step1, all locally and without
touching the unit, the DB, the API or any service state:

| step1 evidence line | Assertion |
|---|---|
| `A5_ready_clock=proc_uptime` | else FAIL — the deadline would not be monotonic |
| `A5_timeout_bin=<path>` | else FAIL — no deadline guard on `PATH` |
| `A5_timeout_guard_rc=124` | a 0.5 s bound on a 30 s sleep must really time out |
| `A5_ready_probe_export_rc=0` | the readiness functions must be visible in the bounded child shell (`export -f` transport) |

A missing or non-functional guard is a **precondition FAIL**, never a silent fall back to an
unbounded probe. A deadline expiry is likewise a genuine FAIL: nonzero exit, **no second
start**, no auto-restart, no mask.

---

## 6. The extended D026 regression test — design

`11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/test_gatea_A5_readiness.py` — standard library only,
`--script <path>`, exit 0 = GREEN / nonzero = RED. Local-only: it never runs on staging, never
executes the Gate-A script, and never invokes `systemctl`, `sudo`, `ss`, `journalctl`, `ssh`,
`scp`, the installed Bridge venv Python, any network call, or any staging action. Those names
are shadowed **twice** — exported shell functions (inherited by every child bash) **and**
executable shims first on `PATH` (reached even by a process that inherits no functions) — and
every shim appends to a private log the harness reports, so a forbidden call **cannot** be
swallowed by the readiness path's per-attempt diagnostics suppression.

**28 named checks.**

**Environment (1)** — `env_deadline_guard_available_and_working`, **repaired in round 2, see
§6.1**: the guard is resolved and exercised **inside the selected Bash**, and must be a
non-Windows GNU coreutils `timeout` that returns `124` for
`timeout --signal=TERM --kill-after=2 0.5 "${BASH:-bash}" -c 'sleep 30'`. If it cannot, the test
goes **RED** rather than claiming a green it did not earn (D025 rule 1: non-execution is never
acceptance).

**Static (2)** — `static_bash_n_syntax_ok` (`bash -n`, parse only, never executes);
`static_embedded_python_heredocs_compile` (every `<<'PYEOF'` block `compile()`s).

**Structural (14)** — `structure_exactly_one_explicit_start`;
`structure_deadline_constants_block` (verbatim `READY_MAX_S=30`, `READY_POLL_S`, `KILL_GRACE_S`,
`TIMEOUT_BIN`, `/proc/uptime` between the BEGIN/END sentinels);
**`structure_no_attempt_count_retry_after_start`** (no `retry <n> <fn>` call site anywhere after
the explicit start — this encodes the Lead's finding as a structural rule);
`structure_wall_clock_deadline_wait_after_start` (the post-start wait is handed the wall-clock
constant `READY_MAX_S`, not an attempt count);
`structure_readiness_requires_active_listener_and_api` (the probe short-circuits `return 1` on
each of the three); `structure_deadline_uses_monotonic_clock`;
`structure_every_attempt_hard_bounded_by_remaining` (the wait calls `run_bounded "$<var>"` where
`<var>` is derived from a remaining-time subtraction, and `run_bounded` uses `$TIMEOUT_BIN`,
`--kill-after`, `$KILL_GRACE_S`); `structure_backoff_never_literal_in_deadline_wait`;
`structure_final_post_assertions_after_readiness`;
`structure_no_fixed_sleep_as_readiness_proof`;
`structure_marker_states_truthful_deadline_contract`;
**`structure_no_retired_false_bound_claim`** (the strings `ready_max_wait_s`, `30 s maximum`,
`30-second maximum`, `30 attempts` must appear **nowhere** in the script);
`structure_final_check_api_timeout_preserved` (`timeout=10` still in the final `check_api`);
`structure_deadline_guard_preconditions_present`.

**Behavioural (11)** — the test extracts the script's **real** constants block and the **real**
`mono_now_ds`, `run_bounded`, `ready_probe_once` and `wait_ready_deadline` definitions and runs
them under `bash -s` (harness fed on stdin, cwd = a private temp dir, so no host path is
interpolated into shell text). `wait_active`, `getprop`, `check_listener_loopback_only` and
`check_api` are replaced by stubs driven by a **file-based** attempt counter, because the
repaired wait runs each attempt in a child process.

| Check | Scenario | Required result |
|---|---|---|
| `behaviour_delayed_readiness_succeeds_before_deadline` | active immediately; listener + exact API from attempt 3; deadline 12 s | succeeds on attempt **3**, within the deadline |
| `behaviour_deadline_wait_actually_polled` | same run | elapsed ≥ the script's own `READY_POLL_S`-derived backoff; ≥ 2 attempts (it waits, it does not spin) |
| `behaviour_readiness_attempt_noise_suppressed` | same run | no per-attempt `listener_count=0` / `api_read_error` in the wait output |
| **`behaviour_deadline_terminates_blocked_probe`** | API probe blocks **45 s**, deadline **3 s** | exits nonzero in **≤ 9 s** and far below the probe duration, having really started the probe |
| **`behaviour_no_probe_child_survives_deadline`** | same run | the blocked probe's **process is gone** afterwards (`kill -0` fails), not orphaned and still running |
| **`mutation_pre_repair_attempt_count_wait_violates_deadline`** | the **verbatim pre-repair wait** — the script's own real `retry` helper driving the old `post_start_ready` — with an **8 s**-blocking API stub and a nominal bound of **2** | must be **measured overrunning** that bound (**> 8 s**; expected ≈ 17 s). If this ever passes inside the bound, the harness is not measuring the defect and the run is not evidence. |
| **`behaviour_repaired_deadline_beats_pre_repair_on_same_stub`** | the repaired wait, **same stub, same nominal bound 2** | nonzero at the deadline, **≤ 8 s**, and **less than half** the pre-repair wall time |
| `behaviour_active_only_deadline_expires` | active on every attempt, listener never bound, deadline 3 s | fails, ≥ 2 attempts — active alone can never satisfy the wait |
| `behaviour_listener_up_but_api_not_exact_deadline_expires` | active + listener true, API never exact, deadline 3 s | fails within the deadline |
| `behaviour_no_forbidden_command_invoked` | all runs | no FORBIDDEN marker in output, no run exited 97, and the shim log is empty for every run |
| `control_synthetic_active_only_would_have_passed` | the **same real** deadline wait with a *synthetic* active-only probe, under the active-only stubs | succeeds on attempt **1** |

The two bold mutation rows are the D026 falsification for the round-1 timing defect, and they
run **inline on every invocation** — the pre-repair behaviour is executed verbatim and required
to be caught, so the test cannot silently stop detecting the defect. The last row is the
harness's own negative control: it proves the active-only timeout is caused by the
listener/API requirements, not by a broken harness.

**Tolerance budget — every source named, nothing else absorbed.** `DEADLINE_TOLERANCE_S = 6` =
`KILL_GRACE_S` (2 s, the script's own honest `SIGTERM`→`SIGKILL` escalation) + 1 s
(coarse-clock rounding when the test host has no `/proc/uptime` and `mono_now_ds` falls back to
`$SECONDS`, whose resolution is one second) + 3 s (python subprocess spawn, bash
startup/teardown, one child shell per attempt, scheduler slop). The overrun the mutation
detects is roughly **8× the nominal bound**, so the tolerance cannot mask it.

CRLF tolerance: the test normalises `\r\n` before parsing and extraction, so RED against the
CRLF working copy of the frozen D script still works.

**Known fidelity limit, stated honestly.** On a host without `/proc/uptime` (e.g. a Windows Git
Bash workstation) the extracted `mono_now_ds` exercises its `$SECONDS` fallback, so the local
harness proves the *deadline arithmetic and the probe termination*, not the monotonic clock
read itself. The script therefore **hard-fails on the run target** if the clock does not resolve
to `/proc/uptime` (`A5_ready_clock`), and records which clock was used in the marker, so the
real A-5 run carries its own proof. Running the test under WSL/Linux exercises the monotonic
path directly and is the stronger check if the Lead wants it.

### 6.1 Round 2 — the deadline guard is resolved and exercised through Bash

**The defect.** Round 1's `find_timeout()` called `shutil.which("timeout")`, i.e. it asked
**Windows** where `timeout` is. Nothing else in the repair does that:

| Consumer | How it resolves `timeout` |
|---|---|
| `gatea_A5.sh` constants block | `TIMEOUT_BIN="$(command -v timeout \|\| true)"` — **Bash** |
| `gatea_A5.sh` step1 guard | `"$TIMEOUT_BIN" --signal=TERM --kill-after="$KILL_GRACE_S" 0.5 "${BASH:-bash}" -c 'sleep 30'` — **Bash**, driving a **Bash child** |
| the test's behavioural harness | the extracted `run_bounded` executed under `bash -s` — **Bash** |
| round-1 `find_timeout()` | `shutil.which("timeout")` — **Windows** ← the defect |

On a canonical Windows workstation Windows answers `C:\Windows\system32\timeout.EXE`, an
unrelated console-pause command that cannot bound a child and exits `1`. So the check that
existed to make non-execution visible **itself became the only failure**, while the mechanism it
was checking was working correctly in the very same run (27/28, Lead, §1.1).

**The fix (test only).** `find_timeout()` is deleted. `probe_deadline_guard(bash_exe)` feeds a
short guard script to the **already-selected Bash** over the **same `bash -s` stdin transport
`run_harness()` uses**, and the check requires all four of its `GUARD_*` facts:

```python
GUARD_SCRIPT  # runs inside the selected bash:
#   _bin=$(command -v timeout ...)                                        -> GUARD_bin
#   "$_bin" --version                                                     -> GUARD_version_rc / GUARD_version
#   "$_bin" --signal=TERM --kill-after=2 0.5 "${BASH:-bash}" -c 'sleep 30' -> GUARD_kill_rc
```

| Requirement | Why |
|---|---|
| `GUARD_bin` non-empty | there must be a guard at all |
| `GUARD_bin` **not** under a Windows `system32` directory | explicit rejection of Windows `timeout.EXE`; both the native `C:\Windows\system32\…` and the MSYS `/c/Windows/system32/…` spellings are matched |
| `GUARD_version_rc == 0` **and** the version line names **GNU coreutils** | `--kill-after` / `--signal` are GNU semantics; a binary that cannot report them is not the documented prerequisite |
| `GUARD_kill_rc == 124` | the guard must **really** terminate a blocked child — behaviour, not presence |

**Non-login on purpose.** The probe uses `bash -s`, not `bash -lc`. A login shell would source a
profile that can add directories the harness's own child shells never see, which would certify a
`PATH` the test does not actually run under. `bash -s` certifies exactly the environment the
behavioural scenarios execute in.

**Stdin hygiene.** The guard shell reads its own script from stdin, so every child it spawns is
given `</dev/null` and cannot consume it.

**Nothing was weakened.** The check became strictly stronger — it now additionally proves the
binary is GNU and mirrors the script's own bash-child kill probe rather than a bare `sleep`. All
**28** named checks survive, none renamed, none removed, none relaxed; the total is still 28. A
genuinely missing, non-GNU or non-functional guard still turns the run **RED** (D025 rule 1),
and the required `PATH` override is now **gone**, not documented.

---

## 7. Evidence actually produced (read-only; no interpreter ran in either session)

### 7a. Round-1 evidence, preserved unchanged

| # | Check | Command | Result |
|---|---|---|---|
| E1 | D → E delta | `diff --strip-trailing-cr <D>/gatea_A5.sh <E>/gatea_A5.sh` | exactly the eight hunks in §3; nothing else differs |
| E2 | `fail "` site accounting | ripgrep count of `fail "` in each script | D **24**, E **28** — 24 preserved + 4 new guard preconditions; none dropped |
| E3 | CR bytes, kit E | ripgrep `\r` over `11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/` | **0 matches across 0 files** — all three members LF-only |
| E4 | CR bytes, preregistration | ripgrep `\r` | **0** |
| E5 | Byte / LF counts | `wc -c -l` | README `25117`/`359`; `gatea_A5.sh` `22531`/`466`; test `47557`/`1071`; preregistration `27070`/`415` |
| E6 | SHA-256 | `sha256sum` | see §2 |
| E7 | Retired false claims removed | ripgrep `ready_max_wait_s\|30 s maximum\|30-second maximum\|30 attempts` over `gatea_A5.sh` | **no matches** — the strings the new `structure_no_retired_false_bound_claim` check forbids are absent |
| E8 | Readiness anchors present | ripgrep for the constants block sentinels, `READY_MAX_S=30`, `READY_POLL_S=1`, `KILL_GRACE_S=2`, `TIMEOUT_BIN=`, `MONO_CLOCK=`, `sudo systemctl start`, `fail "precondition` | constants block at lines 55–73; the four new guard preconditions at lines 376–389; **exactly one** unquoted `sudo systemctl start` command line |
| E9 | Permission probe | `python --version` | `Python 3.14.2` — an interpreter exists; only script execution is gated (§8) |
| E10 | Line endings of the three prepended memory files | ripgrep `\r` count vs `wc -l` | `GLOBAL_HANDOFF.md` **5345/5345** and `NEXT_SESSION_HANDOFF_2026-08-08.md` **978/978** — both uniformly CRLF, convention preserved. **`NEXT_STEPS.md` is 0/2931 — uniformly LF.** No file has mixed endings; see the disclosure below. Byte counts: `NEXT_STEPS.md` `275907`, `GLOBAL_HANDOFF.md` `471414`, `NEXT_SESSION_HANDOFF_2026-08-08.md` `74738`. |
| E11 | Control for the CR probe | ripgrep `\r` on frozen D `gatea_A5.sh` | **261** matches over `261` lines / `9980` bytes — confirms the CR probe really detects CRLF, so the CR-count-0 results above are real and not a silent no-match |

> **Disclosure — `_AI_MEMORY/NEXT_STEPS.md` line endings.** The round-0 evidence recorded that
> file as uniformly CRLF (`2782`/`2782`). It is now uniformly **LF** (`0` CR over `2931` lines).
> Its content is intact and its endings are internally consistent — there are no mixed endings —
> but a `git diff` may therefore present it as a whole-file change rather than a one-section
> prepend. This unit did not run any Git command, so it cannot attribute the conversion; the
> other two prepended files kept CRLF. **None of these three files is ever packaged or
> transferred** (only the three kit E members are, and those are LF-only by requirement), so
> this affects diff readability only. Flagged for the Lead rather than silently corrected,
> because rewriting a 276 KB tracked file to change only its line endings is a larger and
> riskier edit than the disclosure.
>
> **Resolved before round 2.** `_AI_MEMORY/NEXT_STEPS.md` is CRLF again — CR count equals line
> count exactly (E15 below) — so the whole-file line-ending diff the Lead flagged is gone.

### 7b. Round-2 evidence (this session)

| # | Check | How | Result |
|---|---|---|---|
| E12 | **`gatea_A5.sh` untouched by round 2** | `Get-FileHash -Algorithm SHA256` | `fe06f79e36432a8fa81e4a1c17dc470acd8d03099aa735faa76f737212451380`, `22531` bytes, `466` LF lines — **identical to the round-1 value in §2**. This is the load-bearing proof that round 2 changed nothing on the staging side. |
| E13 | New kit-member identities | `Get-FileHash`, `Get-ChildItem` `Length`, ripgrep line count | `README.txt` `56d688653f90b9cafaed2b57b85455d5b89dd9197b9058e2d49a07969fa097d8` / `29397` bytes / `415` lines; `test_gatea_A5_readiness.py` `67823a70d3d4854404cfd15372cd1cf90bb0d6a820caf9858a0448f52ed59c8f` / `53208` bytes / `1164` lines |
| E14 | CR bytes, kit E after the round-2 edits | ripgrep `\r` over `11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/` | **0 matches across 0 files** — all three members still LF-only |
| E15 | `_AI_MEMORY/NEXT_STEPS.md` line endings | ripgrep `\r` count vs line count | **`2991` / `2991` — uniformly CRLF, CR count == line count.** It was `2947`/`2947` before this session's prepend, so the round-1 whole-file LF conversion the Lead flagged is resolved and did not recur. `282973` bytes. |
| E16 | The other two live-memory files | ripgrep `\r` count vs line count | `GLOBAL_HANDOFF.md` **`5411`/`5411`** (`476250` bytes); `NEXT_SESSION_HANDOFF_2026-08-08.md` **`1040`/`1040`** (`79314` bytes) — both uniformly CRLF. See the disclosure below: they were **mixed** on entry. |
| E17 | Reports | `Get-ChildItem` `Length`, ripgrep | `GATE_A_A5_REPAIR_PREREGISTRATION_2026-08-09E.md` `32077` bytes / `478` LF lines / CR **0**; this file ~`47960` bytes / ~`645` LF lines / CR **0** (measured mid-edit; it is a prose record, not a packaged artefact) |
| E18 | Dead code removed | ripgrep `find_timeout\|timeout_bin\|shutil\.` over the test | only `shutil.which("bash")`, `shutil.rmtree(...)`, the script-source key `A5_timeout_bin=`, and the two prose references to the removed `shutil.which("timeout")` remain — **no `find_timeout` and no Python-side timeout lookup survives** |

> **Disclosure — line endings of the two other live-memory files.** On entry to this session
> `_AI_MEMORY/GLOBAL_HANDOFF.md` was `5344` CR over `5356` lines and
> `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` was `977` over `988` — i.e. **mixed**: the
> previous session's newest section had been written LF-only into an otherwise-CRLF file. This
> session's prepends were written through the editing layer, which normalises a file to its
> dominant convention, so both files are now **uniformly CRLF** (E16). The side effect is that
> the `12` and `11` previously-LF lines are rewritten as CRLF and will appear in a diff
> alongside the new section. That is **12 + 11 lines, not a whole-file churn**, it restores each
> file's original and dominant convention, and it removes the mixed-ending state rather than
> extending it. Flagged rather than left silent. None of these three files is ever packaged or
> transferred — only the three kit E members are, and those remain LF-only with CR count 0.

---

## 8. D026 BLOCK — the round-2 default RED/GREEN demonstration is owed

**What happened, round 2 (this session).** Every attempt to execute a shell or an interpreter
was refused by the harness permission layer, and filesystem access outside `C:\GA5E` is
sandboxed off. Read-only in-tree evidence was permitted (`Get-FileHash`, `Get-ChildItem`,
ripgrep), which is how §7b was produced. Interpreters were not:

| Attempted command | Tool | Response |
|---|---|---|
| `bash -lc 'command -v timeout && timeout --version \| head -1'` | Bash | `This command requires approval` |
| `bash -lc 'command -v timeout'` (and `bash --version`) | PowerShell | `This command requires approval` |
| `python …/test_gatea_A5_readiness.py --script …/GATE_A_RUN_KIT_E_2026-08-09/gatea_A5.sh` | Bash **and** PowerShell | `This command requires approval` |
| `python -m py_compile …/test_gatea_A5_readiness.py` | Bash **and** PowerShell | `This command requires approval` |
| `python --version` | PowerShell | `This command requires approval` (round 1 had permitted it; the allowlist is narrower now) |
| `Test-Path "C:\Program Files\Git\usr\bin\timeout.exe"` | PowerShell | blocked — outside the session's allowed directory `C:\GA5E` |

**This unit therefore could not observe its own repair working.** That is stated plainly rather
than papered over: the round-2 change is **reviewed, not executed**.

**What happened, round 1.** The same class of refusal (`bash`, `bash -n`, `python <script>`,
`python -c`, `python -m py_compile`), with only `python --version` → `Python 3.14.2` permitted.

**Consequence under `AGENTS.md` D026.** A regression test is not closure evidence until shown
RED against the pre-fix behaviour and GREEN with the fix, **with the commands and their real
output recorded**. The Lead has now produced that pair for round 1 — but the GREEN half required
a hand-prepended `PATH`, which is exactly what round 2 exists to eliminate, so it does **not**
close round 2. Therefore:

- the `test_gatea_A5_readiness.py` in this kit is **supplemental — not closure evidence**;
- the **round-2 default-command requirement is NOT demonstrated by this unit**;
- **no packaging, transfer, or A-5 rerun may proceed** on this record alone.

**The commands that close it** (repo root of this worktree; local and read-only apart from the
test's own private temp dir; neither executes the Gate-A script). Expect roughly **30–45 s** per
GREEN run — two scenarios deliberately block a stub probe:

```
# RED — MUST exit nonzero, RESULT=RED, against the exact frozen pre-fix D script
python MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/test_gatea_A5_readiness.py --script MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/gatea_A5.sh

# GREEN — MUST exit 0, RESULT=GREEN, against repaired E
python MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/test_gatea_A5_readiness.py --script MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/gatea_A5.sh

# static, standalone
bash -n MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/gatea_A5.sh
python -m py_compile MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/test_gatea_A5_readiness.py
```

**RUN THEM EXACTLY AS PRINTED. No `PATH` override, no other environment edit — that is the
whole point of round 2.** A GREEN obtained after prepending a directory to `PATH` does not
satisfy round 2 and must be reported as a continuing failure.

**Binding pass criteria for the GREEN run** (a bare `RESULT=GREEN` is not enough — these five
named checks must be individually present and PASS, and `SUMMARY total=28`):

```
[PASS] env_deadline_guard_available_and_working          <- the ROUND-2 criterion
[PASS] mutation_pre_repair_attempt_count_wait_violates_deadline
[PASS] behaviour_repaired_deadline_beats_pre_repair_on_same_stub
[PASS] behaviour_deadline_terminates_blocked_probe
[PASS] behaviour_no_probe_child_survives_deadline
```

`env_deadline_guard_available_and_working` now prints the path it resolved through Bash;
**record that path.** If it is empty, or under a Windows `system32` directory, or the version
line does not name GNU coreutils, or the kill probe did not return `124`, the check fails — and
a failure caused by a genuinely missing GNU `timeout` on the workstation is a **BLOCK**, not a
failure of the repair. The four round-1 rows are the timing evidence and must still pass on the
same run, at the same measured margins the Lead recorded (§1.1): ~3.7 s for the 45 s blocked
probe, no survivor, and the mutation an order of magnitude over its nominal bound.

**Expected shape of the RED run against D** (record what is actually observed, not this
prediction): D is syntactically valid, has exactly one explicit start, makes none of the retired
claims and keeps `timeout=10`, so a handful of checks pass on D too; everything readiness-related
fails — no function reaches all three checks from a post-start wait, an attempt-count `retry`
still follows the start, there is no constants block, no monotonic clock, no bounded probe
runner, no readiness marker and no guard preconditions — ending `RESULT=RED` with a nonzero exit.
**The binding requirement is the nonzero exit for the missing wall-clock-deadline contract, not a
particular pass/fail tally.**

**These are expectations, not results.** They must be replaced by real recorded output before
this repair is treated as D026-closed. **If the real GREEN run fails, the finding is real:
repair the source or the test's fidelity and rerun — do not weaken the test to make it pass.**

---

## 9. Residual risk

1. **D026 evidence owed for round 2 (highest).** §8. The Lead's round-1 pair exists and supports
   the source timing mechanics, but its GREEN half needed a hand-prepended `PATH`. Until the
   **default-command** RED/GREEN is recorded, round 2 is unproven at the runtime level.
2. **The round-2 code has never been executed** — same permission BLOCK. Specific first-run
   risks in the new `GUARD_SCRIPT` / `probe_deadline_guard()`, in decreasing likelihood:
   (a) a workstation whose Bash resolves `timeout` to something that is GNU-compatible but does
   not print `coreutils` in `--version` would now fail the check where round 1's looser check
   would have passed it — deliberate, and it fails loudly rather than silently; (b) the
   `_vout=$(…)` / `_vrc=$?` capture and the nested `printf … | head -1 | tr -d '\r'` are
   ordinary Bash but were not parsed by a real shell here; (c) `GUARD_*` parsing in Python is
   the same partition-on-`=` shape already proven by `HARNESS_*`. **Hand review is not a syntax
   check and is not recorded as one.**
3. **The round-1 code has never been executed *by this unit*.** The Lead has since executed it —
   §1.1 — which retires most of the round-1 form of this risk: `bash -n` rc 0, the heredocs
   compile, `mono_now_ds`, `run_bounded` and the `export -f` transport all ran, and the deadline
   really terminated a blocked probe with no survivor. What remains unproven is the `/proc/uptime`
   path (§6 fidelity limit) and everything only the staging host exercises.
4. **New external dependency: GNU coreutils `timeout`.** The deadline guard is `timeout` with
   `--kill-after`, relying on its default (non-`--foreground`) behaviour of putting the child in
   its own process group and signalling the group. This is standard coreutils behaviour and
   standard on the staging host, but it is a new dependency that run-kit D did not have. It is
   asserted in step1 (`A5_timeout_bin`, `A5_timeout_guard_rc=124`), and the test's
   `env_deadline_guard_available_and_working` check refuses to report GREEN without it.
   **Platform note for the Lead's RED/GREEN run.** The target is Linux, where process groups are
   native. The local harness may be run on Windows Git Bash, where process groups are emulated by
   the MSYS layer. If `behaviour_no_probe_child_survives_deadline` is the **only** failing check
   — i.e. the deadline itself held (`behaviour_deadline_terminates_blocked_probe`,
   `behaviour_repaired_deadline_beats_pre_repair_on_same_stub` and the mutation all passed) but
   the grandchild `sleep` outlived the guard — re-run the same command under WSL/Linux **before**
   treating it as a repair defect, and record both runs. A surviving probe child **on Linux** is a
   real defect and must be repaired, not tolerated. Running the whole test under WSL/Linux is in
   any case the stronger check, because it also exercises the `/proc/uptime` monotonic path
   instead of the `$SECONDS` fallback (§6).
5. **New external dependency: `/proc/uptime`.** Required for the monotonic clock on the run
   target and asserted in step1. The `$SECONDS` fallback exists only for the local harness; see
   the fidelity limit in §6.
6. **The environment guard now depends on which Bash the test selects.** `find_bash()` is
   unchanged (`shutil.which("bash")`, then known Git-for-Windows paths), and the guard
   deliberately inherits that choice so it certifies the shell the harness really uses. The
   consequence is that a workstation whose `bash` on `PATH` is *not* the Git Bash the harness
   wants — a WSL launcher stub, for example — would have both the guard and the behavioural
   scenarios follow it together. That is the correct coupling (they can no longer disagree, which
   was the round-1 defect), but it means the run prints, and the auditor must record, the
   `bash=` line and the resolved `GUARD_bin` path. `--bash <path>` remains available for an
   explicit override and is **not** required by the documented default command.
7. **The readiness probe now runs in a child shell.** That is what makes the hard bound
   possible, but it means the readiness functions must survive `export -f`. Step1 proves the
   transport (`A5_ready_probe_export_rc=0`) before the run depends on it; if the transport ever
   failed silently the probe would return 127 every attempt and the run would FAIL at the
   deadline — a loud, honest failure, never a false PASS.
8. **A killed probe is safe but leaves no per-attempt diagnostics.** Suppression is unchanged
   from round 0: the evidence log will not show *why* each not-ready attempt failed. Accepted
   deliberately — the final unsuppressed step5 checks are the authoritative post evidence, and
   the deadline failure reason now reports measured attempts and elapsed seconds.
9. **30 s is still a judgement call.** It matches the preregistered bound. If staging startup
   ever exceeds 30 s the run FAILs honestly rather than hanging — the correct failure mode, but
   a FAIL, not a retry.
10. **Packaging line endings.** Unchanged: build from raw committed blobs (`git cat-file blob`),
    never a bare `git archive` on Windows, which exported CRLF and was rejected in the D round.
    The two rewritten kit members are LF-only (§7b E14); their SHA-256/byte values in §2 changed
    and the round-1 values must not be reused for packaging.
11. **A-6..A-9 still governed by D.** E ships no A-6..A-9 member by design.
12. **Audit scope.** **Round 2 of at most 3 — one round remains.** This remains a new
    runtime-defect repair unit; fresh `claude-opus-5` xhigh **and** `gpt-5.6-sol` xhigh audits
    are required, and any canonical auditor that cannot execute the checks must return BLOCK
    (D025).

---

## 10. Next actions (in order)

1. **`[AI: Claude]` Lead: produce the round-2 D026 evidence.** Run the four commands in §8
   **exactly as printed, with no `PATH` override**, record the exact commands, exit codes and
   real output into §8, and confirm `SUMMARY total=28` plus the five binding named checks —
   including the resolved `GUARD_bin` path and the `bash=` line the run prints. Only then
   re-classify the test as closure evidence.
2. **`[AI: Claude]` Lead: independently re-audit the actual files and evidence** — reproduce §3,
   §7a and §7b yourself, never this self-report; re-verify CR/byte/hash values, and in
   particular re-verify that `gatea_A5.sh` still hashes to
   `fe06f79e36432a8fa81e4a1c17dc470acd8d03099aa735faa76f737212451380` (§7b E12), which is the
   claim that round 2 changed nothing on the staging side; and check that the marker, the failure
   reason, this record, the preregistration, the README and the memory sections all state the
   **same** bound.
3. **`[AI: Claude]` Fresh canonical audits** — `claude-opus-5` xhigh **and** `gpt-5.6-sol`
   xhigh in new independent sessions, per the D025 four-auditor rule. Non-execution ⇒ BLOCK; a
   reproduced required finding from any canonical auditor is binding; **rounds 1 and 2 of 3 are
   consumed — one remains.**
4. **`[AI: Claude]` Only after an accepting audit:** commit, then package **from raw committed
   blobs**, verify LF/CR-0, per-member SHA-256 + bytes, the exact member set and the tar
   hash/size/member count; transfer, extract to the **new** path
   `/home/gatea/gatea-run-kit-20260809E-2ce41e34`, re-verify remotely, **and confirm
   `command -v timeout` and a readable `/proc/uptime` on the VM.** Do not mutate the frozen D
   kit or its evidence.
5. **`[AI: Claude]` Rerun A-5 only**, once, with `/home/gatea/gatea-A5-20260809E.log` confirmed
   absent. Preserve D evidence. Stop on first genuine FAIL and run the preregistered first-FAIL
   response. **A-6 stays blocked** until A-5 PASSES **and** `_AI_MEMORY` is updated.

Companion records: `11_TRIAGE/GATE_A_A5_REPAIR_PREREGISTRATION_2026-08-09E.md`,
`11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/README.txt`,
`11_TRIAGE/GATE_A_A5_FAIL_2026-08-09D.md`,
`11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md`.
