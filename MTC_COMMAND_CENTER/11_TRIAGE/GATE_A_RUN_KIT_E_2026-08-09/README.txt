================================================================================
GATE A RUN KIT E - A-5 ONLY (readiness repair) - 2026-08-09
Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b
REPAIR ROUND 1 (script)    - hard monotonic wall-clock readiness deadline
REPAIR ROUND 2 (test only) - the deadline guard is resolved and exercised through the
                             selected Bash, so the documented default command passes on a
                             canonical Windows workstation with NO PATH override
================================================================================

NOTE ON THE TWO ROUNDS. Round 2 changed the LOCAL regression test and these records ONLY.
gatea_A5.sh is BYTE-IDENTICAL to the round-1 file and therefore still emits
A5_kit_repair_round=1 - that field records the round of the SCRIPT's readiness repair, which
round 2 did not touch. The staging-side contract, the readiness semantics, the step1
preconditions and every assertion below are exactly as round 1 left them.

AUTHORIZED ONLY FOR THE OWNER-APPROVED PREREGISTERED GATE A RERUN on gatea-staging.
This kit exercises a DISARMED staging service. It does not change product code.
Hard exclusions (unchanged): no credential value, broker/exchange access, successful ARM,
order, TESTNET/mainnet, wallet, master merge, or economic action. First genuine FAIL stops.

STATUS: LOCAL REPAIR SOURCE ONLY. REPAIR ROUND 2 IMPLEMENTED LOCALLY; PENDING LEAD RE-AUDIT
AND CANONICAL AUDITS. NOT accepted, NOT committed, NOT packaged, NOT transferred, NOT
executed. A-5 has NOT been rerun. Gate state is unchanged: A-0..A-4 PASS; A-5 FAIL (run-kit D,
2026-08-09); A-6..A-9 NOT RUN. (AGENTS.md canonical audit roster + D025/D026.)

--------------------------------------------------------------------------------
SCOPE: WHAT REVISION E IS AND IS NOT
--------------------------------------------------------------------------------
E is an A-5-ONLY REPAIR KIT. It supersedes run-kit D for the A-5 RERUN ONLY.

- A-6, A-7, A-8 (remote + host) and A-9 remain NOT RUN and remain governed by the
  already-accepted run-kit D source
  (MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/) until A-5 PASSES and
  _AI_MEMORY is updated. E adds no A-6..A-9 member and changes none of them.
- Run-kit D is FROZEN FAILED EVIDENCE. Neither D nor any D report/evidence file is edited
  by this revision. The remote D kit /home/gatea/gatea-run-kit-20260808D-2ce41e34 and the
  D evidence log /home/gatea/gatea-A5-20260808D.log are preserved unchanged and are NEVER
  overwritten or reused.

--------------------------------------------------------------------------------
WHY E EXISTS - DEFECT 1, THE READINESS RACE (run-kit D)
--------------------------------------------------------------------------------
A-5 ran once from run-kit D on 2026-08-09 and returned a genuine exit 1 in about 4.7 s.
Every pre-check, the authorized SIGKILL, and the full dead-window proof PASSED; exactly one
reset-failed + start was performed; post MainPID=187338, NRestarts=0, Restart=no. Then the
post-start listener assertion saw listener_count=0 and the script printed:

    RESULT=FAIL
    A5_FAIL reason=post listener not loopback-only

with the EXIT trap recording rc=1. Cause: D's post-start wait was `retry 30 wait_active`,
which returns as soon as systemd reports ActiveState=active - before the application has
bound 127.0.0.1:8790. An independent read-only check seconds later found the unit
active/running (PID 187338), the listener exactly 127.0.0.1:8790 (non-loopback 0), the API
HTTP 200 exact credential-free DISARMED (state_version=1), and the DB quick_check=ok /
app_state=DISARMED / schema_version=4 with table counts identical to preflight
(POSTFAIL_SAFE_STATE=PASS). Staging was therefore proven safe and the preregistered
conditional stop/mask response was NOT required and NOT performed.

Diagnosis (Lead): a reproduced RUN-KIT READINESS RACE - the kit lacked a real
application-readiness wait after the explicit start. It is NOT a product persistence or
DISARMED invariant failure. A-5 remains FAIL under D and cannot be promoted to PASS from
later diagnostics. Full record: 11_TRIAGE/GATE_A_A5_FAIL_2026-08-09D.md.

--------------------------------------------------------------------------------
WHY THIS IS REPAIR ROUND 1 - DEFECT 2, THE FALSE BOUND (first E draft)
--------------------------------------------------------------------------------
The Codex Lead independently reproduced the D026 evidence for the FIRST E draft:

    exact pre-fix D  ->  rc=1, RESULT=RED,   14 checks, 3 PASS / 11 FAIL,  152 ms
    first E draft    ->  rc=0, RESULT=GREEN, 14/14 PASS,                  7935 ms
    independent `bash -n` rc 0; independent `python -m py_compile` rc 0;
    hashes / byte counts / LF / CR-count-0 evidence reproduced.

The combined active+listener+exact-API logic therefore does discriminate defect 1. But the
Lead then found a BINDING second defect and returned REQUEST_CHANGES:

    the first draft's `retry 30 post_start_ready` is ATTEMPT-COUNT bounded, not time
    bounded. `post_start_ready` calls check_api, whose
    urllib.request.urlopen(..., timeout=10) can block for ten seconds inside ONE attempt,
    and `retry` then sleeps another second. With the listener present but the application
    stalled, that wait could run for roughly 330 SECONDS while the script, the marker and
    every E document claimed a 30 s ceiling. The claim was false, and the original
    regression stubs returned immediately, so they could not see it.

Repair round 1 replaces that claim with a real wall-clock deadline (below) and extends the
regression test so the timing defect is falsified BEHAVIOURALLY, not by wording.

--------------------------------------------------------------------------------
WHY THIS IS REPAIR ROUND 2 - DEFECT 3, THE TEST'S OWN `timeout` LOOKUP (round-1 draft)
--------------------------------------------------------------------------------
The Codex Lead re-audited round 1 and reproduced its evidence:

    default exact D  ->  RED, as required
    default E        ->  RED, 27 of 28 PASS. The ONLY failing check was
                         env_deadline_guard_available_and_working, because Python's
                         shutil.which("timeout") selected C:\Windows\system32\timeout.EXE
                         (rc 1) instead of GNU coreutils timeout.
    E with "C:\Program Files\Git\usr\bin" prepended to PATH
                     ->  GREEN, 28 of 28 PASS, rc 0. The blocked 45 s probe ended in 3.7 s
                         under the 3 s deadline with NO surviving child; the pre-repair
                         mutation took 18.8 s against the repaired wait's 2.6 s.

So the SOURCE timing repair of round 1 is supported by real measurement. The defect was in the
TEST: it asked WINDOWS where `timeout` was, while the script under test - and the test's own
behavioural harness - ask BASH. Lead verdict: REQUEST_CHANGES, repair round 2, on the binding
rule that the test must pass via its documented default command on a canonical Windows
workstation WITHOUT an undocumented PATH override.

Repair round 2 therefore resolves and exercises the deadline guard INSIDE the Bash the test
already selects, over the same `bash -s` transport the behavioural harness uses, mirroring the
script's own step1 guard (`command -v timeout`, `timeout --version`, and the kill probe
`timeout --signal=TERM --kill-after=2 0.5 "${BASH:-bash}" -c 'sleep 30'` -> rc 124). A Windows
system32 `timeout.EXE` is rejected explicitly and can never satisfy the check. All 28 named
checks are preserved; nothing was weakened to make the check pass; gatea_A5.sh is unchanged.

--------------------------------------------------------------------------------
EXACTLY WHAT E CHANGES vs THE FROZEN D gatea_A5.sh
--------------------------------------------------------------------------------
gatea_A5.sh is a copy of the frozen D member and differs ONLY in:

(1) Revision / date / header / path wording for E (plus the new header evidence lines
    A5_kit_revision=E, A5_kit_repair_round=1, A5_readiness=..., A5_supersedes=...).
(2) A NEW no-clobber evidence log: LOG="/home/gatea/gatea-A5-20260809E.log".
(3) The runtime readiness repair: the E readiness-deadline constants block, mono_now_ds(),
    run_bounded(), ready_probe_once(), wait_ready_deadline(), the `export -f` transport
    line, the four new step1 deadline-guard preconditions, the replacement of D's
    `retry 30 wait_active` with `wait_ready_deadline "$READY_MAX_S"` after the single
    explicit start, and ONE structured readiness marker line (A5_READY=...).
(4) A comment-only truthfulness fix on D's retry() helper: it is attempt-count bounded, not
    second bounded. Its CODE is byte-for-byte unchanged and it is still used, unchanged, for
    the cheap step3 dead-window wait (whose probe is one `systemctl show` plus a /proc test).

NOTHING ELSE CHANGED. Preserved verbatim and unweakened: set -Eeuo pipefail; the no-clobber
evidence-log guard (exit 2); the stdout+stderr redirect into the log; the EXIT trap that
records the exact rc; fail() semantics; every D step1 precondition (ActiveState=active,
Restart=no, numeric MainPID>0, numeric NRestarts, loopback-only listener, exact
credential-free DISARMED API, logical DB snapshot); the authorized SIGKILL
`sudo systemctl kill --kill-whom=main --signal=SIGKILL $UNIT`; the complete dead-window
proof (MainPID=0, old /proc/PID gone, 3 s sleep, ActiveState failed/inactive, no :8790
listener, NRestarts unchanged, Result=signal, ExecMainStatus=9); exactly ONE explicit
reset-failed + start; every step5 post assertion (new numeric MainPID>0 differing from the
pre PID, NRestarts unchanged, Restart=no, full unsuppressed loopback-only listener check,
full unsuppressed exact credential-free DISARMED API check, DB snapshot, byte-identical
logical snapshot comparison); the ss LOCAL column index 3 (never peer index 4); check_api's
own urllib timeout=10 in the FINAL evidence check; the venv Python for all JSON/SQLite work;
no POST /api/arm; the env file is never read; all hard exclusions; and no auto-restart/mask
on the script's own failure.

--------------------------------------------------------------------------------
THE READINESS CONTRACT (the repair, as repaired in round 1)
--------------------------------------------------------------------------------
After `sudo systemctl start "$UNIT"` and BEFORE the step5 post assertions, the script runs

    wait_ready_deadline "$READY_MAX_S"          # READY_MAX_S=30 SECONDS, not 30 attempts

ready_probe_once() - one attempt - is satisfied ONLY when ALL THREE hold in the SAME attempt:

    1. systemd ActiveState=active                            -> wait_active
    2. a nonempty loopback-only :8790 listener set           -> check_listener_loopback_only
    3. GET /api/status HTTP 200 + exact credential-free DISARMED (state=DISARMED,
       mode=credential_free_disarmed, state_version=1, network/exchange_conn/
       credential_lookup disabled, exchange_enabled=false, arm_enabled=false)
                                                             -> check_api

It returns nonzero at the FIRST of the three checks that fails, so ActiveState=active alone
can NEVER satisfy the wait. It reuses the existing D check functions unchanged; only their
PER-ATTEMPT diagnostic output is suppressed (>/dev/null 2>&1) so the evidence log is not
filled with expected not-ready noise.

WHAT MAKES THE 30 s REAL (this is the round-1 repair):

- MONOTONIC CLOCK. mono_now_ds() reads /proc/uptime (Linux CLOCK_BOOTTIME) in tenths of a
  second. It never steps backwards and never jumps when NTP or an operator moves the wall
  clock, which $SECONDS and `date +%s` both do. step1 REQUIRES it: if /proc/uptime is
  unreadable the run FAILS the precondition instead of silently using a weaker clock. (A
  $SECONDS fallback exists in the function only so the local regression harness can exercise
  the identical arithmetic on a host without /proc/uptime; the marker records which clock was
  actually used as ready_clock=...)
- ONE BUDGET FOR EVERYTHING. The deadline is fixed once, at the first line of
  wait_ready_deadline, immediately after the single explicit start. Probe duration (active +
  listener + API) AND the backoff between attempts are charged against that same budget.
  There is no attempt counter anywhere in the readiness path.
- EVERY ATTEMPT IS HARD-BOUNDED BY THE REMAINING BUDGET. run_bounded runs each attempt under
  GNU coreutils `timeout` with the REMAINING deciseconds as its bound. Without --foreground,
  `timeout` places the child in its OWN PROCESS GROUP and signals the whole group, so SIGTERM
  at the bound - and SIGKILL KILL_GRACE_S=2 s later if the probe ignores SIGTERM - reaches the
  probe shell AND every descendant it spawned (the venv python, its `ss` subprocess, a stalled
  socket read). No probe child can outlive the bound. A killed probe only ever interrupts a
  read-only operation (systemctl show / ss / GET /api/status); it writes nothing.
- BACKOFF CANNOT OVERSHOOT. The sleep after a failed attempt is clamped to the remaining
  budget, and the deadline is re-checked before every attempt and before every sleep.
- HONEST BOUND, STATED IDENTICALLY EVERYWHERE. The readiness operation returns at 30 s of
  monotonic time, PLUS at most KILL_GRACE_S=2 s if and only if a probe ignores SIGTERM and
  must be SIGKILLed, PLUS ordinary process-scheduling slop. That is the claim - no more.

STEP1 PROVES THE MECHANISM BEFORE THE RUN DEPENDS ON IT (four new preconditions, all local,
all read-only with respect to the service):

    A5_ready_clock=proc_uptime          else FAIL (clock would not be monotonic)
    A5_timeout_bin=<path>               else FAIL (no deadline guard on PATH)
    A5_timeout_guard_rc=124             a 0.5 s bound on a 30 s sleep must really time out
    A5_ready_probe_export_rc=0          the readiness functions must be visible in the
                                        bounded child shell (`export -f` transport)

STAGING PREREQUISITES introduced by the repair: GNU coreutils `timeout` on PATH and a
readable /proc/uptime. Both are standard on the Debian/Ubuntu staging host; both are asserted,
never assumed, and a missing one is a precondition FAIL, never a silent fall back to an
unbounded probe.

- On success: exactly one structured marker is printed -
    A5_READY=yes ready_requires=active+loopback_only_listener_nonempty+exact_credential_free_disarmed_api ready_bound=monotonic_wall_clock_deadline ready_deadline_s=30 ready_clock=<clock> ready_probe_guard=timeout_TERM_then_KILL ready_kill_grace_s=2 ready_elapsed_s=<measured> ready_attempts=<n> ready_second_start=none
  and the step5 assertions then RE-RUN both check_listener_loopback_only and check_api IN
  FULL, unsuppressed. Those remain the authoritative post evidence, and check_api keeps its
  own urllib timeout=10 there - only the READINESS path is bounded by the remaining deadline.
- On deadline expiry: the script fails explicitly via fail() ("deadline: service did not
  become application-ready within the 30s monotonic wall-clock deadline ..."), reporting the
  measured attempts and elapsed time; it exits NONZERO, performs NO second start, and performs
  NO auto-restart/mask. The Lead handles the first-FAIL response.
- A fixed sleep is NEVER used as the readiness proof, and the wait is never unbounded.

--------------------------------------------------------------------------------
FROZEN FACTS
--------------------------------------------------------------------------------
- Release SHA         : 2ce41e34bceb599d80af24c5c33d835820ec321b
- Release app root    : /opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE
- venv Python (PY)    : /opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python
- systemd unit        : mtc-bridge-first-start.service
- State DB            : /var/lib/mtc-bridge/bridge.db
- API                 : 127.0.0.1:8790  (GET /api/status only; never POST /api/arm)
- Env file            : /etc/mtc-bridge/mtc-bridge.env  (NEVER read by A-5, never printed)
- NEW E evidence log  : /home/gatea/gatea-A5-20260809E.log   (no-clobber; must not exist)
- FROZEN D log        : /home/gatea/gatea-A5-20260808D.log   (preserve; never overwrite)
- Planned E remote dir: /home/gatea/gatea-run-kit-20260809E-2ce41e34  (new path; not D's)
- Readiness deadline  : READY_MAX_S=30 s monotonic; READY_POLL_S=1 s; KILL_GRACE_S=2 s
- Baseline state      : A-0..A-4 PASS; A-5 FAIL (D); A-6..A-9 NOT RUN; service active/static,
                        credential-free DISARMED, Restart=no, state_version=1, no
                        broker/credentials.

--------------------------------------------------------------------------------
KIT MEMBERS (3 files; SHA256SUMS is added by the Lead at package time)
--------------------------------------------------------------------------------
README.txt                     this file
gatea_A5.sh                    A-5 unclean SIGKILL / manual-restart consistency, repaired
test_gatea_A5_readiness.py     LOCAL-ONLY D026 regression test for the readiness repair

ONLY gatea_A5.sh is ever executed on gatea-staging. test_gatea_A5_readiness.py is a
local-only regression artifact: it is run on the Windows workstation against the script
SOURCE and MUST NOT be invoked on the staging VM. It never runs the Gate-A script and never
invokes systemctl, sudo, ss, ssh, scp, the installed Bridge venv Python, any network call, or
any staging action - those names are shadowed both by exported shell functions and by
executable shims placed first on PATH, and every shim appends to a log the harness reports, so
a forbidden call cannot be hidden by the readiness path's diagnostics suppression. The round-2
environment guard adds no new reach: it runs only `command -v timeout`, `timeout --version`,
and a 0.5 s-bounded local `bash -c 'sleep 30'`, inside the same Bash, writing nothing.

--------------------------------------------------------------------------------
SHARED SCRIPT CONTRACT (unchanged from run-kit D)
--------------------------------------------------------------------------------
- set -Eeuo pipefail ; fixed evidence log per gate under /home/gatea ; refuses to overwrite
  an existing log (exit 2); redirects stdout+stderr to the log; EXIT trap records exact rc.
- Uses the installed venv Python for all JSON/SQLite work; NEVER assumes the sqlite3 CLI.
- No writes outside /home/gatea except the runbook-authorized service/DB state caused by the
  A-5 SIGKILL + one explicit start (Restart=no).
- Output is structured key=value evidence. Ends with exactly `A-5 PASS` only if ALL
  assertions hold.
- The script NEVER hashes its own still-open log from inside itself; evidence-log hashes are
  captured post-run by the commands below.
- Never POSTs /api/arm; never reads /etc/mtc-bridge/mtc-bridge.env.

--------------------------------------------------------------------------------
LOCAL VALIDATION  (Lead, BEFORE packaging/transfer/execution)
--------------------------------------------------------------------------------
Run from the repo root. Every command is local and read-only apart from the test's own
private temporary directory. The repaired test takes roughly 30-45 s per GREEN run, because
two of its scenarios deliberately block a stub readiness probe.

1) D026 RED - the test MUST exit NONZERO against the exact frozen pre-fix D script:
     python MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/test_gatea_A5_readiness.py --script MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/gatea_A5.sh
   Expect RESULT=RED: D reaches none of the three checks from a post-start wait, still uses
   an attempt-count `retry` after the start, has no readiness-deadline constants block, no
   monotonic clock, no bounded probe runner, no readiness marker and no guard preconditions.
   (Read-only on D; D is never edited.)

2) D026 GREEN - the same test MUST exit ZERO against E:
     python MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/test_gatea_A5_readiness.py --script MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/gatea_A5.sh
   Expect RESULT=GREEN with, in particular, these four named checks passing:
     mutation_pre_repair_attempt_count_wait_violates_deadline
         the VERBATIM pre-repair wait (the script's own `retry` helper driving the old
         post_start_ready) is run against an 8 s-blocking API stub with a nominal bound of 2
         and MUST be measured overrunning it (~17 s). If this ever passes inside the bound,
         the harness is not measuring the defect and the run is not evidence.
     behaviour_repaired_deadline_beats_pre_repair_on_same_stub
         same stub, same nominal bound, the repaired wait returns nonzero at the deadline in
         under half the pre-repair wall time.
     behaviour_deadline_terminates_blocked_probe
         a 45 s-blocking API probe under a 3 s deadline must exit nonzero in <= 9 s.
     behaviour_no_probe_child_survives_deadline
         that blocked probe's process must be GONE afterwards, not orphaned and still running.
   The run also reports env_deadline_guard_available_and_working. THIS IS THE ROUND-2 REPAIR.
   The guard is now resolved and exercised INSIDE the Bash the test already selected, over the
   same `bash -s` transport the behavioural harness uses, and it mirrors the script's own step1
   guard exactly:
        command -v timeout                         (the script's own TIMEOUT_BIN lookup)
        timeout --version                          (must identify GNU coreutils)
        timeout --signal=TERM --kill-after=2 0.5 "${BASH:-bash}" -c 'sleep 30'   -> rc 124
   Round 1 asked Python instead (shutil.which("timeout")), which asks WINDOWS where `timeout`
   is; on a canonical Windows workstation Windows answers C:\Windows\system32\timeout.EXE - an
   unrelated console-pause command that cannot bound a child and exits 1. The behavioural
   scenarios were meanwhile running GNU `timeout` correctly through Git Bash's own PATH, so the
   Lead's default round-1 run reported 27/28 PASS with this single check failing, and only a
   hand-prepended PATH made it 28/28. That workaround is now neither needed nor documented:
   RUN THE COMMAND EXACTLY AS PRINTED ABOVE, WITH NO PATH OVERRIDE. A Windows system32
   `timeout.EXE` is rejected explicitly and can never satisfy the check. If GNU coreutils
   `timeout` is genuinely missing, is not GNU, or does not return 124 on a blocked child, the
   test still goes RED rather than claiming a green it did not earn (D025 rule 1 -
   non-execution is never acceptance).
   Expect SUMMARY total=28. The run prints the `bash=` line it selected and the check prints
   the `command -v timeout` path it resolved through that Bash: RECORD BOTH.

   PLATFORM NOTE. The run target is Linux, where process groups are native; this test may be
   run on Windows Git Bash, where MSYS emulates them. If behaviour_no_probe_child_survives_
   deadline is the ONLY failing check - the deadline itself held, but the grandchild sleep
   outlived the guard - re-run the same command under WSL/Linux BEFORE treating it as a repair
   defect, and record both runs. A surviving probe child ON LINUX is a real defect and must be
   repaired, not tolerated. Running the whole test under WSL/Linux is the stronger check
   anyway: it also exercises the /proc/uptime monotonic clock path rather than the $SECONDS
   fallback the script uses only when /proc/uptime is absent.

   The test also performs, on whichever script it is pointed at, the two static checks the
   Lead would otherwise run by hand - each is reported as its own named check:
     static_bash_n_syntax_ok                  `bash -n <script>` rc 0 (PARSE ONLY; the
                                              Gate-A script is never executed)
     static_embedded_python_heredocs_compile   every <<'PYEOF' block `compile()`s (3 blocks
                                              in gatea_A5.sh); nothing is executed
   They may also be run standalone:
     bash -n MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/gatea_A5.sh

3) Test byte-compiles (must be rc 0):
     python -m py_compile MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/test_gatea_A5_readiness.py

4) CR-byte check (must be 0 for every new kit E file and both new reports):
     grep -c $'\r' MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/README.txt \
       MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/gatea_A5.sh \
       MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/test_gatea_A5_readiness.py
   Note: this repo's Windows checkout can present tracked .sh files with CRLF. The E members
   are authored LF-only; the packaging step below must therefore be built from RAW COMMITTED
   BLOBS, not from a bare `git archive` on Windows. The test normalises CRLF before parsing,
   so RED against the CRLF working copy of the D script still works.

5) NO Gate-A execution during validation. No SSH/SCP, no staging, no service action.

--------------------------------------------------------------------------------
PACKAGE + TRANSFER + REMOTE VERIFICATION  (Lead; only AFTER an accepting audit)
--------------------------------------------------------------------------------
- Build the tar from RAW COMMITTED BLOBS (`git cat-file blob`), never a bare `git archive`
  on Windows - the D packaging round proved `git archive` exports CRLF here and that tar was
  rejected before transfer.
- Verify BEFORE transfer: every member LF-only (CR count 0); the exact member set
  (README.txt, gatea_A5.sh, test_gatea_A5_readiness.py, SHA256SUMS); per-file SHA-256 and
  byte counts; tar SHA-256 + tar byte size + tar member count.
- Transfer to /home/gatea and extract to the NEW path
  /home/gatea/gatea-run-kit-20260809E-2ce41e34. Do NOT extract into, over, or beside the
  frozen D directory in a way that mutates it.
- Re-verify on the VM: identical tar SHA-256/bytes/member set; `sha256sum -c SHA256SUMS`
  all OK; `bash -n gatea_A5.sh` rc 0; every member CR count 0; byte/LF counts match the
  pre-transfer record.
- Confirm the repaired script's two new runtime prerequisites on the VM, read-only, BEFORE
  invoking A-5 (the script asserts both itself in step1, but confirming first avoids burning
  the one no-clobber evidence-log identity on a missing tool):
      command -v timeout && timeout --version | head -1
      test -r /proc/uptime && head -c 40 /proc/uptime
- Confirm /home/gatea/gatea-A5-20260809E.log does NOT exist before invoking A-5.
- Run-kits B, C and D stay intact. E is a sibling A-5-only revision.

--------------------------------------------------------------------------------
EXECUTION  (on gatea-staging, as the gatea user with passwordless sudo for
systemctl/sqlite/journalctl/stat/sha256sum). A-5 ONLY. STOP AT FIRST FAIL.
--------------------------------------------------------------------------------
  1) A-5:  bash /home/gatea/gatea-run-kit-20260809E-2ce41e34/gatea_A5.sh
           # SIGKILL main + one explicit start; 30 s monotonic readiness deadline; DB unchanged

Do NOT run A-6..A-9 from this kit - E contains no A-6..A-9 member. A-6 remains BLOCKED
until A-5 PASSES and _AI_MEMORY (NEXT_STEPS.md, GLOBAL_HANDOFF.md) plus
11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md are updated. Only then does the sequence
continue under run-kit D (A-6 -> A-7 -> A-8 remote+host -> A-9).

FIRST-FAIL / SAFETY: at the first genuine FAIL, preserve the evidence log, run only
read-only diagnostics as needed, then STOP. If the failure leaves the service in an unsafe
state, safe-stop and mask the unit (`sudo systemctl stop mtc-bridge-first-start.service`,
`sudo systemctl mask mtc-bridge-first-start.service`) and write the result + memory. Do NOT
auto-restart or mask on a script's internal failure; the Lead handles the safe first-FAIL
response. A readiness-deadline expiry is a genuine FAIL: it exits nonzero and performs no
second start. So is any of the four new step1 deadline-guard precondition failures.

--------------------------------------------------------------------------------
POST-RUN EVIDENCE-LOG HASH + SIZE  (run AFTER the script exits and its log is closed)
--------------------------------------------------------------------------------
On gatea-staging:
     sha256sum /home/gatea/gatea-A5-20260809E.log
     stat -c '%s %a %U %G' /home/gatea/gatea-A5-20260809E.log

Preserve a local copy as C:\WPI_ARTIFACTS\gatea-A5-20260809E.log and confirm both copies
share one SHA-256 and byte size. NEVER overwrite the D artefacts
/home/gatea/gatea-A5-20260808D.log or C:\WPI_ARTIFACTS\gatea-A5-20260808D.log (SHA-256
3e282516dfea7e66d9196ad5f3d929b7d1a50257bae501a5b89c35e007eb31c9, 1933 bytes).

These hashes/sizes are recorded in the result + memory; they are NOT produced by the script.

Companion records:
  11_TRIAGE/GATE_A_A5_REPAIR_PREREGISTRATION_2026-08-09E.md   (E acceptance criteria)
  11_TRIAGE/GATE_A_A5_REPAIR_IMPLEMENTATION_2026-08-09E.md    (E implementation + D026)
  11_TRIAGE/GATE_A_A5_FAIL_2026-08-09D.md                     (the failed D evidence)
  11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md       (A-5..A-9 criteria, first-FAIL)
================================================================================
