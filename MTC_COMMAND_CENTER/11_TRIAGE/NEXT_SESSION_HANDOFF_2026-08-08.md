# NEXT SESSION HANDOFF — `2ce41e34` accepted; 20260808B local run kit ready; staging authorization required (2026-08-08)

> ## ▶ NEWEST CHECKPOINT — Codex audit rerun 2 still environment-BLOCKED (2026-08-09)
>
> Fresh Codex xhigh at clean detached `C:\GAEAX2` could use writable temp/pycache, but the Codex
> subprocess sanitized PATH: Git coreutils disappeared, `mkdir` failed, and Windows `timeout.exe`
> was selected. E was RED 18/28; verdict BLOCK. Lead then ran the exact no-PATH-edit commands in the
> same worktree: D RED 6/28 and E GREEN 28/28 with Git Bash `/usr/bin/timeout`; status remained
> clean. No source defect reproduced, but D025 acceptance remains blocked. **Next:** third fresh
> Codex xhigh at frozen `61d88f12`, dedicated worktree, unsandboxed command runtime under strict
> read-only instructions. No integration/package/transfer/staging. A-5 FAIL; A-6..A-9 NOT RUN.
>
> ---

> ## ▶ NEWEST CHECKPOINT — E canonical audit round 1 BLOCK; executable Codex rerun next (2026-08-09)
>
> Frozen candidate `61d88f12054c` remains unintegrated/unpackaged/untransferred/unrun. Claude Opus
> 5 xhigh executed D RED and E GREEN 28/28 and returned PASS. Codex 5.6-sol xhigh returned BLOCK:
> its sandbox had no usable writable temp/pycache and its fallback Bash exposed Windows
> `timeout.exe`, so mandatory E did not complete. DeepSeek ClinePass was unavailable; GLM-5.2 was
> denied execution; both are supplemental BLOCKs with no required finding. All four detached audit
> worktrees are clean. **Next:** fresh Codex xhigh audit in a new detached worktree with writable
> temp/pycache and normal Git Bash. No integration/package/transfer/staging before acceptance.
> A-5 remains FAIL; A-6..A-9 NOT RUN. Repair rounds remain 2/3; this is an audit environment rerun.
> Record: `11_TRIAGE/GATE_A_A5_E_CANONICAL_AUDIT_ROUND1_2026-08-09.md`.
>
> ---

> ## ▶ NEWEST CHECKPOINT — E round 2 Lead re-audit ACCEPT; four canonical audits next (2026-08-09)
>
> Default D is RED; E is GREEN 28/28 without PATH override. GNU timeout, hard deadline,
> blocked-child termination, mutation falsification, syntax/compile and byte/scope evidence reproduce.
> Lead preliminary ACCEPT freezes E for fresh Claude, Codex, DeepSeek and GLM audits. E is not finally
> accepted, packaged, transferred, or run. A-5 FAIL; A-6..A-9 NOT RUN; no staging action.
>
> ---

> ## ▶ NEWEST CHECKPOINT — Claude Opus 5 repair round 2: the deadline guard is resolved through Bash; default-command RED/GREEN owed (2026-08-09)
>
> **Supersedes the Lead REQUEST_CHANGES block below as live state for *next action*.** The
> round-2 finding is accepted and repaired **in the local regression test only**.
> **`gatea_A5.sh` was not touched** — SHA-256 `fe06f79e…451380`, `22531` bytes, `466` LF lines,
> identical to round 1 and re-verified — so it still emits `A5_kit_repair_round=1`, which
> correctly names the round of the *script's* readiness repair. **A-5 is still FAIL and
> A-6..A-9 are still NOT RUN — nothing was rerun.** E is **implemented locally; NOT accepted,
> NOT committed, NOT packaged, NOT transferred, NOT run.** Worktree `C:\GA5E`, branch
> `codex/gatea-a5-readiness-e`, baseline `123bb0c4`. No Git, SSH/SCP, staging/service,
> package/transfer/deploy, credential, broker/exchange, ARM, order, TESTNET/mainnet, wallet,
> merge or economic action. **Run-kit D and every D report/evidence file untouched; staging
> unchanged and safe.**
>
> **The defect (Lead, round-1 re-audit).** The test resolved its deadline guard with Python's
> `shutil.which("timeout")` — it asked *Windows*, which answers
> `C:\Windows\system32\timeout.EXE`, an unrelated console-pause command that cannot bound a
> child (rc `1`). Everything else asks *Bash*: the script's
> `TIMEOUT_BIN="$(command -v timeout || true)"`, its step1 guard, and the test's own harness
> under `bash -s`. So default E was **RED at 27/28** with that as the *only* failure, while the
> mechanism it checked worked; only a hand-prepended `PATH` reached **GREEN 28/28 rc 0** (45 s
> blocked probe ended in **3.7 s** under a 3 s deadline, **no surviving child**; pre-repair
> mutation **18.8 s** vs repaired **2.6 s** — real support for the round-1 source repair).
>
> **The fix.** `find_timeout()` deleted. `probe_deadline_guard(bash_exe)` feeds a guard script
> to the **already-selected Bash over the same `bash -s` stdin transport the harness uses**
> (non-login on purpose) and requires all four facts: non-empty `command -v timeout`; **not**
> under a Windows `system32` directory (native and MSYS spellings rejected); `timeout --version`
> rc `0` naming **GNU coreutils**; kill probe
> `timeout --signal=TERM --kill-after=2 0.5 "${BASH:-bash}" -c 'sleep 30'` → **`124`**. **No
> `PATH` override required, requested or accepted.** All **28** checks preserved, unrenamed and
> unrelaxed; the check is strictly stronger. New identities: test `67823a70…d59c8f` (`53208` B /
> `1164` L), README `56d68865…097d8` (`29397` B / `415` L); CR count `0` on all three members.
>
> **D026 BLOCK — this unit could not observe its own repair working.** `bash`, `bash -lc`,
> `bash -n`, `python <script>`, `python --version` and `python -m py_compile` were all refused
> (`This command requires approval`); filesystem access outside `C:\GA5E` is sandboxed off. The
> round-2 change is **reviewed, not executed**, and the Lead's round-1 pair does not close it
> because its GREEN half needed the very `PATH` override round 2 removes.
>
> **NEXT ACTION (Lead).** Run both documented commands **exactly as printed, no `PATH`
> override**: exact D → RED/nonzero, E → GREEN/0 with `SUMMARY total=28`,
> `env_deadline_guard_available_and_working` PASS plus the four round-1 timing checks, and
> record the printed `bash=` line and resolved `GUARD_bin` path. Then re-audit the files
> directly, re-verify the `gatea_A5.sh` hash, and run the fresh `claude-opus-5` xhigh +
> `gpt-5.6-sol` xhigh canonical audits. **Rounds 1 and 2 of 3 consumed — one remains.**
> Records: `11_TRIAGE/GATE_A_A5_REPAIR_IMPLEMENTATION_2026-08-09E.md` (§1.1, §6.1, §7b, §8),
> `11_TRIAGE/GATE_A_A5_REPAIR_PREREGISTRATION_2026-08-09E.md` (§4.4),
> `11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/README.txt`.
>
> ---

> ## ▶ NEWEST CHECKPOINT — E round-1 Lead re-audit REQUEST_CHANGES: default Windows harness resolves wrong timeout (2026-08-09)
>
> Default E reached 27/28 PASS but Python selected Windows `timeout.EXE`. With Git Bash `usr\bin`
> first on PATH it was GREEN 28/28: hard deadline killed the blocked probe, no child survived, and
> repaired E beat the pre-repair mutation. **Repair round 2:** resolve GNU timeout through selected
> Bash so the default command passes; preserve all checks; update records/current memory; restore
> NEXT_STEPS CRLF. No staging action; E unaccepted/unrun; A-5 FAIL; A-6..A-9 NOT RUN.
>
> ---

> ## ▶ NEWEST CHECKPOINT — Claude Opus 5 repair round 1: E now has a hard monotonic readiness deadline; D026 round-1 evidence still owed (2026-08-09)
>
> **Supersedes the Lead REQUEST_CHANGES block below as live state for *next action*.** The
> binding timing finding is accepted and repaired. **A-5 is still FAIL and A-6..A-9 are still
> NOT RUN — nothing was rerun.** E is **implemented locally; NOT accepted, NOT committed, NOT
> packaged, NOT transferred, NOT run.** Worktree `C:\GA5E`, branch
> `codex/gatea-a5-readiness-e`, baseline `123bb0c4`. No Git, SSH/SCP, staging/service,
> package/transfer/deploy, credential, broker/exchange, ARM, order, TESTNET/mainnet, wallet,
> merge or economic action occurred. **Run-kit D and every D report/evidence file were left
> untouched; staging is unchanged and safe.**
>
> **Lead-run round-0 evidence, preserved exactly:** exact pre-fix D → `rc=1`, `RESULT=RED`,
> **14 checks / 3 PASS / 11 FAIL**, `152 ms`; first E draft → `rc=0`, `RESULT=GREEN`, **14/14
> PASS**, `7935 ms`; independent `bash -n` rc `0`, `python -m py_compile` rc `0`;
> hashes/bytes/LF/CR-0 reproduced. **Binding finding:** `retry 30 post_start_ready` was
> attempt-count bounded, not time bounded — `check_api`'s `urllib` open can block 10 s per
> attempt and `retry` sleeps 1 s after each failure, so listener-present/API-stalled could run
> ≈ **330 s** while the marker claimed a 30 s ceiling.
>
> **The repair.** `wait_ready_deadline "$READY_MAX_S"` (`READY_MAX_S=30` **seconds**) fixes a
> **monotonic wall-clock deadline** once, from `/proc/uptime` (`CLOCK_BOOTTIME`), right after
> the single explicit start, and charges **probe duration and the inter-attempt backoff to that
> one budget**. Every attempt runs under GNU coreutils `timeout` with the **remaining** time as
> its hard bound; `timeout` signals the child's whole **process group**, so SIGTERM at the bound
> and SIGKILL 2 s later reach the probe shell **and every descendant** — **no probe child can
> outlive the bound**, and a killed attempt only interrupts a read-only operation. Backoff is
> clamped to the remaining budget. All three conditions still required in the **same** attempt;
> step5 still re-runs the listener and API checks **in full, unsuppressed**, and the final
> `check_api` keeps its own `timeout=10`. **Honest bound stated identically everywhere:** returns
> at 30 s monotonic **plus at most 2 s** if a probe ignores SIGTERM, plus scheduler slop. Four
> new step1 preconditions assert the mechanism instead of assuming it —
> `A5_ready_clock=proc_uptime`, non-empty `A5_timeout_bin`, `A5_timeout_guard_rc=124`,
> `A5_ready_probe_export_rc=0`. **New staging prerequisites: GNU `timeout` on `PATH` and a
> readable `/proc/uptime`** (asserted, never assumed).
>
> **Real evidence (read-only, this session):** `diff --strip-trailing-cr` D→E = **eight hunks**,
> **exactly one D line replaced** (`retry 30 wait_active …`); `retry`'s code byte-for-byte
> unchanged (comment-only fix) and still used for the step3 dead-window wait; `fail "` sites
> D `24` → E `28` (24 preserved + 4 new guards). CR **0** for all three kit members and the
> preregistration. `wc -c -l`: README `25117`/`359`, `gatea_A5.sh` `22531`/`466`, test
> `47557`/`1071`, preregistration `27070`/`415`. SHA-256 `gatea_A5.sh` `fe06f79e…`, test
> `f5651aa6…`, README `8127afb3…` — these **supersede** the round-0 hashes (`2a8521b6…`,
> `a32f85fc…`, `bdd63847…`), which now identify only the discarded first draft.
>
> **D026 extended (28 named checks).** The falsification pair runs inline every time, identical
> stubs and identical nominal bound: `mutation_pre_repair_attempt_count_wait_violates_deadline`
> drives the **verbatim pre-repair wait** against an 8 s-blocking API stub with a nominal bound
> of 2 and requires it to be **measured overrunning** it (≈ 17 s), while
> `behaviour_repaired_deadline_beats_pre_repair_on_same_stub` requires the repaired wait to exit
> nonzero at the deadline in under half that time.
> `behaviour_deadline_terminates_blocked_probe` (45 s probe, 3 s deadline, ≤ 9 s) and
> `behaviour_no_probe_child_survives_deadline` (the probe process must be **gone**) prove
> termination, not waiting-it-out. `env_deadline_guard_available_and_working` turns a missing or
> non-functional GNU `timeout` into **RED**, never an unearned green (D025 rule 1).
>
> **HONEST BLOCK — round-1 D026 evidence still owed.** `bash`, `bash -n`, `python <script>`,
> `python -c` and `python -m py_compile` are all outside this session's permission allowlist
> (every attempt returned `This command requires approval` through both the Bash and PowerShell
> tools; only `python --version` → `3.14.2` was permitted). **The repaired script and the
> extended test have never been executed.** The extended test is therefore **supplemental — NOT
> closure evidence**, and the timing defect is **NOT closed**; nothing may be packaged,
> transferred or rerun on this record alone.
>
> **Next:** run the four commands in `11_TRIAGE/GATE_A_A5_REPAIR_IMPLEMENTATION_2026-08-09E.md`
> §8 (RED on exact D, GREEN on E, `bash -n`, `py_compile`) — GREEN counts only if
> `mutation_pre_repair_attempt_count_wait_violates_deadline`,
> `behaviour_repaired_deadline_beats_pre_repair_on_same_stub`,
> `behaviour_deadline_terminates_blocked_probe`, `behaviour_no_probe_child_survives_deadline` and
> `env_deadline_guard_available_and_working` each PASS; then Lead re-audits the **actual files**;
> then fresh canonical audits (`claude-opus-5` xhigh **and** `gpt-5.6-sol` xhigh, new independent
> sessions, D025 binding, **repair round 1 of 3 consumed**). Only after acceptance: commit,
> package from raw committed blobs, transfer, re-verify remotely (including `command -v timeout`
> and a readable `/proc/uptime`), and rerun **A-5 only**. **If the real GREEN run fails, the
> finding is real — repair the source, do not weaken the test.**
>
> ---

> ## ▶ NEWEST CHECKPOINT — Codex Lead audit REQUEST_CHANGES: E's claimed 30-second bound is false (2026-08-09)
>
> **D026 has now been independently executed:** exact pre-fix D → `rc=1`, `RESULT=RED`, 3/14
> checks PASS; E → `rc=0`, `RESULT=GREEN`, 14/14 PASS. Independent `bash -n` and `py_compile`
> returned 0; LF/CR/hash/byte evidence reproduced. The combined active+listener+exact-API logic
> does discriminate the original D race.
>
> **Lead verdict: REQUEST_CHANGES (repair round 1).** The current E script/docs claim
> `retry 30 post_start_ready` is a 30-second maximum. It is not: `check_api` can block for 10 s
> (`urllib.request.urlopen(..., timeout=10)`) in each attempt and `retry` sleeps 1 s after a failure.
> With listener present but API stalled, the current path can take roughly 330 s. Therefore the
> `A5_READY ... ready_max_wait_s=30` marker and matching docs are false; the current immediate-stub
> regression misses the timing defect.
>
> **Next:** same Claude Opus 5 counterpart repairs E with a real monotonic 30-second deadline that
> includes probe time and bounds each readiness API probe by remaining time, while retaining the
> final full API/listener checks and all D assertions. Extend D026 with a slow/hanging-API case that
> is RED on current E and GREEN after repair; update all E records/current memory; Lead re-audits,
> then fresh canonical audits. No staging action occurred. E remains unaccepted/uncommitted/
> unpackaged/untransferred/unrun; A-5 remains FAIL; A-6..A-9 remain NOT RUN; D evidence is immutable.
>
> ---

> ## ▶ NEWEST CHECKPOINT — Claude Opus 5 protected repair: Gate A A-5 readiness repair E IMPLEMENTED LOCALLY; D026 RED/GREEN still owed; pending Lead inspection + canonical audit (2026-08-09)
>
> **Supersedes the "A-5 FAIL — reproduced post-start readiness race" block below as live state
> for *next action*** (the A-5 D FAIL facts, the A-0..A-4 PASS history, the run-kit D
> package/transfer facts, and the repair-round blocks below all remain unchanged history).
> **A-5 is still FAIL and A-6..A-9 are still NOT RUN — nothing was rerun.** The counterpart
> flagship implementer `claude-opus-5` built run-kit revision **E** in the isolated worktree
> `C:\GA5E` on branch `codex/gatea-a5-readiness-e`, baseline `123bb0c4`
> (`123bb0c49129b29f625fb0c922968ddf8feaed06`). **E is NOT packaged, NOT transferred, NOT
> audited, NOT accepted, NOT run.** Candidate `2ce41e34bceb599d80af24c5c33d835820ec321b` and the
> product/artifact are unchanged. No Git command, SSH/SCP, staging/service operation,
> package/transfer/deploy, broker/exchange, ARM, order, TESTNET/mainnet, wallet, credential read,
> or economic action occurred. **Run-kit D and every D report/evidence file were left untouched.**
> Standalone records: `11_TRIAGE/GATE_A_A5_REPAIR_IMPLEMENTATION_2026-08-09E.md` and
> `11_TRIAGE/GATE_A_A5_REPAIR_PREREGISTRATION_2026-08-09E.md`.
>
> **What E is.** `11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/` — an **A-5-only repair kit**
> (`README.txt`, `gatea_A5.sh`, `test_gatea_A5_readiness.py`). It supersedes run-kit D **for the
> A-5 rerun only**; **A-6..A-9 remain NOT RUN and remain governed by the accepted run-kit D
> source** until A-5 PASSES and `_AI_MEMORY` is updated. New no-clobber evidence log
> `/home/gatea/gatea-A5-20260809E.log`; planned new remote path
> `/home/gatea/gatea-run-kit-20260809E-2ce41e34`. The frozen D log
> `/home/gatea/gatea-A5-20260808D.log` (SHA-256
> `3e282516dfea7e66d9196ad5f3d929b7d1a50257bae501a5b89c35e007eb31c9`, `1933` bytes) is never
> overwritten or reused. Only `gatea_A5.sh` ever runs on staging — the test is local-only.
>
> **The repair.** After the single explicit `sudo systemctl start` and before the step5 post
> assertions, `retry 30 post_start_ready` is a bounded **30-second maximum** readiness wait
> satisfied only when **all three** hold in the **same attempt**: systemd `ActiveState=active`
> **plus** a nonempty loopback-only `:8790` listener set **plus** `GET /api/status` HTTP 200 exact
> credential-free DISARMED. It returns nonzero at the first failing check, so
> `ActiveState=active` alone can **never** satisfy the wait. Only per-attempt diagnostics are
> suppressed; step5 re-runs both checks **in full, unsuppressed**. On timeout: explicit `fail`,
> nonzero exit, **no second start**, no auto-restart/mask. One structured `A5_READY=yes …` marker
> on success. A real `diff` vs frozen D shows **exactly six hunks** (header wording, E scope
> block, `LOG=`, two header echoes, the readiness function, the retry/marker replacement) and
> `fail "` sites are unchanged at **24 in both** — no D assertion, dead-window proof,
> DB/API/listener condition, hard exclusion, no-clobber behaviour, authorized SIGKILL,
> `Restart=no`, or exactly-one-explicit-start contract was weakened.
>
> **HONEST GAP — D026 IS NOT SATISFIED.** The **RED and GREEN runs were NOT executed**: `bash`
> and `python <script>` are outside that session's Bash-tool permission allowlist (every attempt
> returned `This command requires approval`; read-only `diff`/`sha256sum`/`wc`/`grep` were
> allowed). `bash -n` on E and `python -m py_compile` on the test were blocked the same way. Per
> `AGENTS.md` D026 the new test is **supplemental — NOT closure evidence** and **the readiness
> defect is NOT closed**; the two exact closing commands and expected output are in
> `GATE_A_A5_REPAIR_IMPLEMENTATION_2026-08-09E.md` §8. Evidence that *was* produced: the D→E
> `diff`; `fail "` parity 24/24; **CR bytes 0** for all three kit E members and both new reports;
> `wc -c -l` README `16847`/`254`, `gatea_A5.sh` `12960`/`309`, test `23140`/`580`; SHA-256
> `gatea_A5.sh` `2a8521b66eef00a58b1cde07342dcf812a3d1640d5b439f567512d944c604066`, test
> `a32f85fc3ab9341029c31627876346db19e0c4704de9a317f181371c9ee2aa22`, README
> `bdd638475bb971bfbafd8bb877b5d3ccb5e6922d18b9dbbf2ebcca104f6ce727`.
>
> **Next steps contract:**
> 1. `[AI: Claude]` **Produce the D026 evidence first** — run the §8 **RED** (nonzero,
>    `RESULT=RED`, against the exact frozen pre-fix D `gatea_A5.sh`) and **GREEN** (exit 0,
>    `RESULT=GREEN`, against E) commands, plus `bash -n` on E and `python -m py_compile` on the
>    test; record real commands, exit codes and output. If GREEN fails, the finding is real —
>    repair the code, **never adjust the test to make it pass.**
> 2. `[AI: Claude]` **Lead independently inspect the actual E diff and files** — never the
>    implementer's self-report — and reproduce the RED/GREEN, syntax, compile, CR and byte/hash
>    evidence.
> 3. `[AI: Claude]` **Run fresh canonical audits** required by `AGENTS.md` for this protected
>    repair: new independent sessions, `claude-opus-5` effort `xhigh` **and** `gpt-5.6-sol` effort
>    `xhigh`. D025 binds — non-execution ⇒ **BLOCK**; **any reproduced required finding from any
>    canonical auditor is binding**; max 3 repair/re-audit rounds. This is a **new runtime-defect
>    repair unit**; the three prior run-kit D source-review rounds do **not** cover it.
> 4. `[AI: Claude]` **Only after an accepting audit:** build the package **from raw committed
>    blobs** (`git cat-file blob`) — **not** a bare `git archive` on Windows, which exported CRLF
>    and was rejected in the D round — verify LF/CR-0, per-member SHA-256 + bytes, the exact
>    member set (`README.txt`, `gatea_A5.sh`, `test_gatea_A5_readiness.py`, `SHA256SUMS`) and the
>    tar hash/size/member count; transfer, extract and re-verify under the **new** remote path
>    `/home/gatea/gatea-run-kit-20260809E-2ce41e34`. **Never overwrite D evidence.**
> 5. `[AI: Claude]` **Rerun A-5 (E) only**, once, with `/home/gatea/gatea-A5-20260809E.log`
>    confirmed absent. **Preserve D evidence. Stop on first genuine FAIL** and perform the
>    preregistered first-FAIL response. **A-6 remains BLOCKED** until A-5 PASSES **and**
>    `_AI_MEMORY` plus this handoff are updated.
>
> Hard exclusions unchanged: no credential value, broker/exchange access, successful ARM, order,
> TESTNET/mainnet, wallet, master merge, or economic action. The service intentionally remains
> active/static, loopback-only, credential-free DISARMED, `state_version=1`, no
> broker/credentials.

---

> ## ▶ PREVIOUS CHECKPOINT — GLM-5.2 bounded documentation: Gate A A-5 FAIL — reproduced post-start readiness race; staging proven safe; protected run-kit repair next (2026-08-09)
>
> **Supersedes the "run-kit D packaged, transferred, extracted, and verified; A-5 first next" block
> below as live state for *next action*** (the run-kit D package/transfer/verify facts, A-0..A-4
> PASS, and the repair-round blocks below remain unchanged history). **A-5 has now RUN and FAILED.**
> A-5 ran exactly once from `/home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A5.sh` over the
> preregistered key-only SSH route and returned a genuine **exit `1`** (about `4.7 s`). **Verdict
> (honest): A-0..A-4 PASS · A-5 FAIL · A-6..A-9 NOT RUN.** The frozen script's `wait_active` returned
> on systemd-active, then immediately asserted the post-start loopback listener before the application
> had bound it (`listener_count=0` → `RESULT=FAIL` → `A5_FAIL reason=post listener not loopback-only`;
> trap `rc=1`). A-5 **cannot be promoted to PASS** from later diagnostics. **Lead diagnosis:
> reproduced run-kit readiness-race defect** — the kit lacks a bounded application-readiness wait after
> the explicit `start`; **not** a product persistence/DISARMED invariant failure. No product code or
> product artifact changed; no credential, broker/exchange access, successful ARM, order,
> TESTNET/mainnet, wallet, master merge, or economic action is authorized or occurred. GLM-5.2 recorded
> it and edited only the four task-named files (this handoff prepend plus `_AI_MEMORY/NEXT_STEPS.md`,
> `_AI_MEMORY/GLOBAL_HANDOFF.md`, and the new standalone
> `11_TRIAGE/GATE_A_A5_FAIL_2026-08-09D.md`). Standalone record:
> `11_TRIAGE/GATE_A_A5_FAIL_2026-08-09D.md`. Active integration branch before this task:
> `feature/donchian-crypto-ladder` at `7421bc34` (`7421bc34ec67215f496e9a546dcadbb00bca0254`).
> Accepted source candidate unchanged: `2ce41e34bceb599d80af24c5c33d835820ec321b`.
>
> **Evidence identity (exact).** Remote `/home/gatea/gatea-A5-20260808D.log`; local preserved copy
> `C:\WPI_ARTIFACTS\gatea-A5-20260808D.log`; both SHA-256
> `3e282516dfea7e66d9196ad5f3d929b7d1a50257bae501a5b89c35e007eb31c9`, `1933` bytes; remote mode `664`,
> owner/group `gatea`. Independent preflight immediately before A-5 PASS (evidence log absent;
> `gatea_A5.sh: OK` vs `SHA256SUMS`; service active/static, `Restart=no`, `MainPID=183225`,
> `NRestarts=0`, `Result=success`, `ExecMainStatus=0`; listener exactly `127.0.0.1:8790`; API HTTP 200
> exact credential-free DISARMED, `state_version=1`, all conn/exchange fields disabled/false; DB
> `quick_check=ok`, `app_state=DISARMED`, `schema_version=4`). A-5 in-script: all pre-checks PASS;
> frozen authorized SIGKILL
> `sudo systemctl kill --kill-whom=main --signal=SIGKILL mtc-bridge-first-start.service`; dead-window
> proof PASS; exactly one `reset-failed`+`start`; post `MainPID=187338`, `NRestarts=0`, `Restart=no`;
> then `listener_count=0` → failure line, trap `rc=1`.
>
> **Staging proven safe a few seconds later (read-only) — conditional stop/mask was NOT required.**
> Independent post-failure verification PASS: unit loaded/static, active/running, `MainPID=187338`,
> `Restart=no`, `NRestarts=0`, `Result=success`, `ExecMainStatus=0`; listener count 1 exactly
> `127.0.0.1:8790`, non-loopback 0; API exact credential-free DISARMED, same `state_version=1`; DB
> `quick_check=ok`, `app_state=DISARMED`, `schema_version=4`, exact same table counts as preflight;
> `POSTFAIL_SAFE_STATE=PASS`. Because staging was independently proven safe, active, loopback-only,
> credential-free DISARMED, and DB-consistent, the preregistered conditional stop/mask response (§5)
> was not required and was not performed. The frozen run-kit D and its evidence are preserved
> unchanged; never overwrite/reuse `/home/gatea/gatea-A5-20260808D.log`.
>
> **Next steps contract — protected run-kit repair:**
> 1. `[AI: Claude]` **Repair the A-5 runtime-evidence defect in a NEW run-kit revision** (do not
>    mutate the preserved D kit/log): add a bounded post-start readiness wait requiring systemd active
>    **plus** loopback listener **plus** exact credential-free DISARMED API before final assertions.
> 2. `[AI: Claude]` **Apply D026** — RED against the exact readiness-race behavior or an equivalent
>    falsification/mutation, then GREEN with the fix; record commands and real output.
> 3. `[AI: Claude]` **Independently audit** the actual repair and protected surface under the canonical
>    roster / Lead acceptance rules — a new runtime-defect repair unit, not covered by the prior three
>    source-review rounds.
> 4. `[AI: Claude]` **Preregister/package/transfer a new revision** with a new evidence-log identifier
>    (e.g. revision E); verify hashes/bytes/LF/member set before any rerun; **do not overwrite D
>    evidence.**
> 5. `[AI: Claude]` **Rerun A-5 only** after the repaired revision is accepted and staged; **stop
>    again on any genuine FAIL.** **A-6 remains blocked** until A-5 passes and memory is updated.
>
> Ordered actions: `_AI_MEMORY/NEXT_STEPS.md`. Live state: `_AI_MEMORY/GLOBAL_HANDOFF.md`.
>
> ---

> ## ▶ NEWEST CHECKPOINT — GLM-5.2 bounded documentation: Gate A run-kit D packaged, transferred, extracted, and verified; A-5 first next (2026-08-09)
>
> **Supersedes the "Lead ACCEPTED run-kit D source; package/transfer next" block below as live state
> for *next action*** (the run-kit D source acceptance, A-0..A-4 PASS, and the repair-round blocks
> below remain unchanged history). **A-0..A-4 remain PASS; A-5..A-9 remain NOT RUN.** The Lead-accepted
> run-kit D source was packaged, transferred to `gatea-staging`, extracted, and independently
> re-verified. **No Gate-A script ran** during packaging, transfer, extraction, or verification. No
> product code or product artifact changed; no credential, broker/exchange access, successful ARM,
> order, TESTNET/mainnet, wallet, master merge, or economic action is authorized or occurred. The
> packaging/transfer/extraction/verification actions recorded were authorized Lead staging actions
> under the preregistered `gatea-staging` Gate A rerun sequence; GLM-5.2 recorded them and edited only
> the four task-named files (this handoff prepend plus `_AI_MEMORY/NEXT_STEPS.md`,
> `_AI_MEMORY/GLOBAL_HANDOFF.md`, and the new standalone
> `11_TRIAGE/GATE_A_RUN_KIT_D_PACKAGE_TRANSFER_2026-08-09.md`). Standalone record:
> `11_TRIAGE/GATE_A_RUN_KIT_D_PACKAGE_TRANSFER_2026-08-09.md`. Active integration branch before this
> task: `feature/donchian-crypto-ladder` at `acc41e73` (`acc41e732d0825058e25e7e89652d61811a8cde6`).
> Accepted source candidate unchanged: `2ce41e34bceb599d80af24c5c33d835820ec321b`.
>
> **Package identity (exact).** A first `git archive` packaging attempt exported CRLF and was
> **rejected before transfer** — preserved (not deleted) at
> `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34.rejected-crlf.tar`, SHA-256
> `66ce7a1e148d17626f68962ccdd3bb6bcacdf4c49a6eb815713caa64899634a8`, `71680` bytes. The accepted
> package was rebuilt from raw committed blobs with `git cat-file blob` (reads from the object
> database, avoiding worktree/archive line-ending conversion):
> `C:\WPI_ARTIFACTS\gatea-run-kit-20260808D-2ce41e34.tar`, SHA-256
> `e8a52e3cdeaa9da9315d0cbeb1fde7dd75e9ecc8a4ad4c926e4084c37c55e0d3`, `71680` bytes; **9 tar members
> (root dir + 8 files), 8 extracted files, 7 manifest lines**, all manifest hashes verified, all
> members CR count `0`, Bash + PowerShell parser + embedded-Python syntax checks passed. Transferred
> to `/home/gatea/gatea-run-kit-20260808D-2ce41e34.tar` preserving the exact same SHA-256, bytes, and
> member set, and extracted to `/home/gatea/gatea-run-kit-20260808D-2ce41e34`.
>
> **Transport defect recorded, not concealed.** The first remote verifier had a PowerShell-to-SSH
> quoting defect after extraction and emitted `test: \\8: integer expression expected`; **no Gate-A
> script ran** — this is a verifier transport defect, not a package or Gate-A failure. A clean remote
> re-verification then passed: all 7 manifest members verified; `bash -n` passed for A5/A6/A7/A8/A9;
> exact extracted file count 8 and exact member set; manifest lines 7; every file CR count 0;
> byte/LF counts README 13934/197, SHA256SUMS 551/7, A5 9719/261, A6 13863/283, A7 6191/139, A8
> 4124/108, A8_host 3195/87, A9 3937/109; embedded Python blocks compiled A5 3, A6 3, A7 2, A8 1,
> A9 0.
>
> **Staging safety — unchanged after transfer/verification.** Service active/static; exact
> credential-free DISARMED status; no credentials; no broker; state version 1. This is the A-5
> prerequisite state, preserved through the package/transfer/verify unit.
>
> **Next steps contract — A-5 first (state clearly):**
> 1. `[AI: Claude]` **Execute A-5 only** from `/home/gatea/gatea-run-kit-20260808D-2ce41e34/gatea_A5.sh`.
> 2. `[AI: Claude]` **Preserve and inspect** `/home/gatea/gatea-A5-20260808D.log`; independently
>    verify service/API/DB/listener/systemd state before assigning a verdict.
> 3. `[AI: Claude]` **Stop on the first genuine FAIL** and perform the preregistered safe response
>    (`GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` §5); **do not run A-6.**
> 4. `[AI: Claude]` **If A-5 passes,** update the relevant `_AI_MEMORY` files before starting A-6.
> 5. `[AI: Claude]` **Continue one gate at a time** under the existing preregistration. Hard
>    exclusions remain: no credentials, broker/exchange, successful ARM, orders, TESTNET/mainnet,
>    wallet, master merge, or economic action.
>
> Ordered actions: `_AI_MEMORY/NEXT_STEPS.md`. Live state: `_AI_MEMORY/GLOBAL_HANDOFF.md`.
>
> ---

> ## NEWEST CHECKPOINT - Lead ACCEPTED run-kit D source; package/transfer next (2026-08-08)
>
> Supersedes the repair-round-3 block below as live next action. Codex Lead independently accepted
> the third/final repair: all Bash/PowerShell/Python syntax checks pass, `git diff --check` is clean,
> new kit/preregistration files are LF-only, and all A-5..A-9 safety/evidence bindings reproduce
> against the installed accepted candidate. **A-5..A-9 remain NOT RUN.** The source is not yet
> packaged, transferred, or executed. Next: package run-kit D; transfer and verify only; update
> `_AI_MEMORY`; then execute A-5 first and stop at first genuine FAIL. B/C remain preserved. No
> credentials, broker/exchange access, successful ARM, orders, TESTNET/mainnet, wallet, master merge,
> or economic action are authorized by this checkpoint.
>
> Full preregistration: `11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md`. Accepted source:
> `11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/`.
>
> ---

> ## ▶ NEWEST CHECKPOINT — GLM-5.2 final focused repair round 3: Gate A run-kit D A-6/A-7 (NOT RUN; bindings await Lead final acceptance) (2026-08-08)
>
> **Supersedes the repair-round-2 block below as live state for *next action* (the round-2, round-1,
> and A-4 PASS blocks below remain unchanged).** Same worktree and unit; only the task-named files
> were edited (`gatea_A6.sh`, `gatea_A7.sh`, `README.txt`, the preregistration doc
> `GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` new §13, and these three memory/handoff prepends).
> **A-5..A-9 are NOT RUN.** No product code/artifact changed; no new files/Git/SSH/staging/execution/
> product edits/credentials/ARM/orders/broker-network access/packaging/transfer. No gate result is
> claimed. Candidate `2ce41e34…` unchanged; A-0..A-4 PASS remain the last completed state.
>
> **Round-3 repairs:** (1) **A-6 pre-import env isolation** — the six keys (`HL_ACCOUNT_ADDRESS`,
> `HL_API_WALLET_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `MTC_BRIDGE_START_MODE`,
> `MTC_BRIDGE_STATE_DB`) are popped via `os.environ.pop` BEFORE `from bridge.app import create_app`
> / `from bridge.broker.mock import MockBroker` and before explicit app construction (order: stdlib
> imports + release `sys.path`; pop loop; then bridge imports; then `create_app(...)`), so even
> module-level default app construction cannot see the parent values; (2) **A-6 wording** —
> `os.environ.pop` removes and discards process-local values; no value is printed/copied/persisted/
> retained; it is NOT claimed the values are "never read"; Gate-A preconditions already established
> the keys absent (clearing is defense in depth); the env FILE is not opened by A6 (A-9 keeps its
> truthful statement that it scans bytes but emits paths/counts only); (3) **A-7 explicit equality**
> — after separately validating API state and DB `app_state`, A-7 explicitly asserts and records
> `db_app == api_state` (not merely the two DISARMED checks); on mismatch it exits nonzero; all
> existing A-7 checks preserved.
>
> **Lead re-audit evidence (supplied; syntax/compile only — worker did NOT run it):** all five Bash
> scripts `bash -n` rc 0; PS parser 0 errors; `git diff --check` clean; every embedded Python
> heredoc compiled (A-5 3, A-6 3, A-7 2, A-8 1). Round-2 lifecycle/sidecar/notifier work accepted.
> STATUS unchanged: A-5..A-9 NOT RUN, not packaged/transferred; the round-3 bindings await the
> Lead's final acceptance. Next action unchanged: before A-5 the **Lead** independently validates +
> packages + transfers + verifies the kit, then A-5 first, strict order, stop at first FAIL. Full
> record: `11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` §13.

> ## ▶ NEWEST CHECKPOINT — GLM-5.2 bounded follow-up: Gate A run-kit D A-6 repair round 2 (NOT RUN; bindings await Lead re-audit) (2026-08-08)
>
> **Supersedes the repair-round-1 block below as live state for *next action* (the round-1 block and
> the A-4 PASS block below it remain unchanged).** A focused follow-up repaired exactly the three
> remaining REQUIRED A-6 defects in `gatea_A6.sh` ONLY (A5/A7/A8/A8_host/A9 unchanged); only the
> task-named files were edited (`gatea_A6.sh` + `README.txt` in `GATE_A_RUN_KIT_D_2026-08-08/`, the
> preregistration doc `GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` new §12, and these three
> memory/handoff prepends). **A-5..A-9 are NOT RUN.** No product code/artifact changed; no
> packaging/transfer/install/service mutation, credential, broker/exchange access, successful ARM,
> order, TESTNET/mainnet, wallet, master merge, or economic action occurred. No gate result is
> claimed. Candidate `2ce41e34…` unchanged; A-0..A-4 PASS remain the last completed state.
>
> **A-6 round-2 repairs (all in `gatea_A6.sh`):** (1) **partial-start cleanup** — `stop_required` is
> set immediately BEFORE `engine.start()` so `finally` always attempts `await engine.stop()` whenever
> start was invoked (incl. timeout/start exception); a stop exception stays nonzero, and if start
> already failed the original start exception is preserved while the stop failure is still recorded
> (no false PASS); (2) **SQLite sidecar cleanup** — strict target validation (exact
> `/home/gatea/gatea-A6-temp.` prefix + EXACTLY six alphanumeric mktemp chars, real directory, not a
> symlink), then delete only maxdepth-1 REGULAR files exactly named `bridge.db` / `bridge.db-wal` /
> `bridge.db-shm`, require no entries remain, then `rmdir` (never recursive; invalid target/residue
> forces nonzero) so a valid run no longer falsely fails on leftover WAL/SHM sidecars;
> (3) **notifier/outbound hardening** — before `create_app`, `HL_ACCOUNT_ADDRESS`, `HL_API_WALLET_KEY`,
> `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `MTC_BRIDGE_START_MODE`, `MTC_BRIDGE_STATE_DB` are popped
> from the isolated process env without reading/printing any value; explicit `start_mode='credentialed'`,
> explicit temp `store_path`, injected `MockBroker(bars=[])`; require `engine.notifier is None or
> engine.notifier.enabled is False`; print only `notifier_disabled=true/false`; bind it into the PASS
> assertion; no env value printed. STATUS unchanged: A-5..A-9 NOT RUN, not packaged/transferred; the
> round-2 bindings await the Lead's final re-audit. Worker validation beyond provided Lead evidence is
> not claimed. Next action unchanged: before A-5 the **Lead** independently validates + packages +
> transfers + verifies the kit, then A-5 first, strict order, stop at first FAIL. Full record:
> `11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` §12.

> ## ▶ NEWEST CHECKPOINT — GLM-5.2 bounded documentation: Gate A run-kit D A-5..A-9 source/preregistration (Lead-audit repair round 1; NOT RUN) (2026-08-08)
>
> **Supersedes the A-4 PASS block below as live state for *next action* (A-4 PASS itself
> remains the last completed gate).** Run-kit D **source** (Lead-audit repair round 1 applied)
> and the A-5..A-9 preregistration are **NOT packaged, transferred, or executed**; **A-5..A-9
> are NOT RUN.** No product
> code or product artifact changed; no packaging/transfer/install/service mutation, credential,
> broker/exchange access, successful ARM, order, TESTNET/mainnet, wallet, master merge, or
> economic action occurred. No gate result is claimed. Candidate `2ce41e34…` unchanged; A-0..A-4
> PASS remain the last completed state.
>
> **Next (ordered).** Before A-5 the **Lead** must independently validate the scripts (`bash -n`
> each `.sh`; PowerShell parser for `gatea_A8_host.ps1`; CR-byte check = 0 on every file), create
> the manifest (`SHA256SUMS`) + tar, transfer to `/home/gatea`, and verify exact tar
> SHA-256/bytes + member set + `sha256sum -c` all OK + the five on-host `bash -n`. Then **[AI:
> Claude] A-5 first**, strict order A-5→A-6→A-7→A-8(remote+host)→A-9, **stop at first FAIL**;
> after every gate PASS update `_AI_MEMORY` (`NEXT_STEPS.md`/`GLOBAL_HANDOFF.md`) + this handoff
> **before** the next gate; at first FAIL preserve evidence, read-only diagnostics only, STOP,
> and safe-stop + mask the unit if unsafe (no auto-restart/mask on a script's internal failure).
> **No product/artifact change; no gate result; no prohibited action.**
>
> **Lead-audit repair round 1 applied (Lead source review authoritative over the implementer's
> older records-branch read) — see `GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md` §9.** Repairs:
> A-5/A-8 collect the `ss -H -ltn` LOCAL column at index 3 (not peer col 4); A-6 restores
> `start_mode='credentialed'` (installed candidate authoritative; MockBroker blocks
> `_build_broker`/credentials/network), fixes the false PASS (nonzero on timeout / start
> exception / failed assertion / stop exception; `try/finally` always stops; requires
> `status()['deferred_event_queue_depth']==0` AND `len(_queued_events)==0`), and validates temp
> cleanup (no `rm -rf`); A-8 host exits nonzero (`A8_HOST_FAIL`) on probe fail; A-9 uses
> `-e`/`--`, canonical nine category names, and a truthful content statement (reads bytes incl.
> the env file but emits counts + paths only). Lead evidence already supplied: `bash -n` all 5
> rc 0, PS parser 0 errors, CR=0 on new kit/prereg files (syntax/byte checks only). STATUS
> unchanged: A-5..A-9 NOT RUN, not packaged/transferred; repaired bindings await re-audit. Full
> record: `11_TRIAGE/GATE_A_A5_A9_PREREGISTRATION_2026-08-08D.md`; ops:
> `11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/README.txt`.

> ## ▶ NEWEST CHECKPOINT — GLM-5.2 bounded documentation: Gate A A-4 PASS; seven conditions evidenced (2026-08-08)
>
> **Supersedes the A-3 postcheck block below as live state.** Lead verdict: **Gate A A-4 PASS under Addendum
> D** (§D.4 / §C.4). Gate A is **IN PROGRESS through A-4**; **A-5–A-9 NOT RUN** (first-FAIL rule). Candidate
> `2ce41e34…` and the product/artifact are **unchanged** by this unit; candidate acceptance, D025
> acceptance, and the repair-round count unaltered. No pytest rerun. Full record:
> `11_TRIAGE/GATE_A_A4_PASS_2026-08-08C.md`. Ordered actions: `_AI_MEMORY/NEXT_STEPS.md`.
>
> **Worker scope (accurate).** GLM-5.2 **only edited documentation** (the four files named in the task). The
> A-4 staging execution and the read-only on-disk diagnostics recorded here were **authorized staging actions
> performed earlier** under the owner-approved preregistered `gatea-staging` rerun sequence and their results
> were **Lead-verified before this checkpoint** — this is **not** "no staging action or diagnostic results
> occurred"; they did, within the authorized boundary, and the GLM worker recorded rather than performed or
> mutated them. No product/artifact change; no install mutation, credential, broker/exchange access,
> successful ARM, orders, TESTNET/mainnet, master merge, or economic action.
>
> **Main A-4 execution (run-kit C `gatea_A4.sh`, SHA-256 `78aa7fca…fd9b4`).** Main log
> `/home/gatea/gatea-A4-20260808C.log`, SHA-256
> `19ed99773ca8dbfb84bfc6a93289daf4077419dd6d46c23343f5d4cfbf007c06`, `10152` B; script exit `0` bound to
> the step-8 refusal-probe exit `0`. Service start exit `0`; active/running PID `183225`; unit static;
> resolved running `Environment=` exactly includes `MTC_BRIDGE_STATE_DB=/var/lib/mtc-bridge/bridge.db` and
> `MTC_BRIDGE_START_MODE=credential_free_disarmed`; env file remained empty / no credentials. Listener
> exactly local `127.0.0.1:8790`; no non-loopback listener. GET `/api/status` 200: state `DISARMED`, mode
> `credential_free_disarmed`, network/exchange_conn/credential_lookup disabled, `exchange_enabled=false`,
> `arm_enabled=false`, `state_version=1`. All fail-closed preconditions passed before POST; POST `/api/arm`
> with `X-Confirm: 1` returned application HTTP **409**, exact body `ARM unavailable in credential-free
> DISARMED start mode; exchange access is disabled`; post GET remained identical `DISARMED`, `state_version`
> unchanged `1`. No broker attempt in journal, `/var/log/mtc-bridge/bridge.err.log`, or outbound sockets;
> errlog only normal Uvicorn startup, SHA-256
> `179d162d67d0aa48e66fe51cb1ca7184bf6cff2d759ce74807417f27d71d0f24`, `199` B.
>
> **Main-script evidence defect and Lead closure.** The main script's step 0 and step 10 nested
> `sudo bash -c` SQLite commands had shell-quoting syntax errors, so the main script could not itself
> harvest its planned pre/post SQLite meta reads — a run-script evidence-harvesting defect, not a candidate
> defect; the step-8 refusal probe (gate-critical) and other steps are unaffected. The Lead therefore **did
> not accept A-4 from the main exit alone** and obtained canonical read-only evidence instead. `dbdiag3`
> closes the required post-attempt persisted-DB evidence; `postdiag2` separately closes the pre-POST
> timing gap for listener/sockets/logs/environment/API. A-4 PASS rests on the main log **plus** those two
> canonical clean read-only logs.
>
> **Canonical read-only diagnostics (helper defects superseded; non-accepting/noncanonical logs preserved).**
> Canonical DB log `/home/gatea/gatea-A4-dbdiag3-20260808C.log`, SHA-256
> `530f846c7fc2f4f50de6a13eecd2274726b32947082dfcbf9ffaa12baef8a5c8`, `497` B: active; WAL/SHM present; meta
> exactly `app_state=DISARMED` / `schema_version=4`; `PRAGMA quick_check=ok`; PASS; rc `0`. Canonical post
> log `/home/gatea/gatea-A4-postdiag2-20260808C.log`, SHA-256
> `ed06554cf93951921b15d378b9c2ac01f019c7c58815942cdf561e5168672183`, `1111` B: active; running env exact;
> local-address column exactly `127.0.0.1:8790`; journal/errlog/outbound broker hits all `0`; API exact
> credential-free `DISARMED`, `state_version=1`; failures `0`, rc `0`. Superseded helper logs preserved:
> dbdiag `2c31405659ace6c2acb0d5f21e02fbd9761ecfefc9ad44a35d523664c686cf08` (`558` B, falsely expected stale
> schema `2`, exited `1`); dbdiag2 `b4488d46559610c532e93b044fbb3073905fc330f102e1fe2b3aae502a411341`
> (`497` B, accepted schema `4` but PASS line said schema `2`, noncanonical); postdiag
> `043d59017eea1887943ce41bfbdb45d17a1d83bd6a2a806df411433d6f39bfb6` (`1079` B, misread `ss` peer
> `0.0.0.0:*` as local exposure, exited `1`).
>
> **Seven-condition map — all hold, each with primary evidence plus independent read-only confirmation.**
> (1) active/running PID `183225` (main + postdiag2); (2) `127.0.0.1:8790` only (main + postdiag2
> local-address); (3) `GET /api/status` durably `DISARMED` (main pre/post + postdiag2); (4) application
> HTTP `409` refusal, not connection-refused (main step-8 probe, exit `0`); (5) no broker attempt (main +
> postdiag2); (6) persisted `app_state=DISARMED`, `state_version=1` unchanged (main pre/post GET + dbdiag3);
> (7) resolved start mode `credential_free_disarmed` recorded (main `Environment=` + postdiag2). The helper
> defects are run-script-only; no criterion went unobtained.
>
> **State.** The service **intentionally remains active/static**, loopback-only, credential-free `DISARMED`,
> `state_version=1`, no broker connection, no credentials — the prerequisite for the A-5 unclean-restart
> test. Existing authorization covers preregistered A-5–A-9 only; hard exclusions unchanged (credentials,
> broker/exchange access, successful ARM, orders, TESTNET/mainnet, master merge, economic action).
>
> **Next step only:** `[AI: Claude]` first recover the exact A-5–A-9 commands from the canonical runbook and
> addenda and preregister a bounded command/evidence plan (do not improvise protected tests); then execute
> **A-5 first** (unclean kill/restart; state/DB consistency / `DISARMED`), stopping at first FAIL — on
> failure preserve evidence, stop+mask the service safely, and write result/memory, on PASS update
> `_AI_MEMORY` before A-6. `[AI: Any]` preserve old `GATE_A_RESULT_2026-08-08.md`; final rerun record
> `GATE_A_RESULT_2026-08-08B.md`.
>
> ---

> ## ▶ NEWEST CHECKPOINT — GLM-5.2 bounded documentation: run-kit C transferred; A-3 retained-log postcheck PASS (2026-08-08)
>
> **Supersedes the C-freeze "next unit" below as live state.** The next unit defined there (transfer the
> run-kit C tar; re-check A-3 without rerunning pytest) was executed on `gatea-staging`. This records the
> result; it does not alter candidate acceptance, the product bits, the artifact, D025 acceptance, or the
> repair-round count. No pytest rerun.
> No product code or product artifact changed; no install, service start, credentials,
> broker/exchange access, successful ARM, orders, TESTNET/mainnet, master merge, or economic action. The
> authorized staging actions in this unit were exactly run-kit C transfer/verification and read-only
> retained-log A-3 postcheck/replay, producing the two recorded logs. The GLM worker itself only edited
> documentation and did not perform staging/Git mutation. Full record:
> `11_TRIAGE/GATE_A_LOCAL_RUN_KIT_2026-08-08C.md` (addendum). Ordered actions:
> `_AI_MEMORY/NEXT_STEPS.md`.
>
> **Transfer + remote verification (B intact):** tar SHA-256
> `4ee5ba920800ceff8f55338bcba5b388d39d2457f9970795af89c9333767f855`, `53760` B, exact 9 members at
> `/home/gatea/gatea-run-kit-20260808C-2ce41e34.tar`; extracted to
> `/home/gatea/gatea-run-kit-20260808C-2ce41e34`; 7 manifest entries; `sha256sum -c` all seven OK; six
> `bash -n` PASS; corrected remote `gatea_A3.sh`
> `2bfec1c230d77d70f30bda5560f824fe970b4c2fca098d3fdda49129f2465d1c` OK.
>
> **Retained-log A-3 postcheck — PASS (no pytest rerun):** retained
> `/home/gatea/gatea-A3-suite-20260808B.log` SHA-256
> `569e79c7d68623b9f2ad51ee48053a04e6938e3277398861760dc1dd8d61c848` verified; outer retained log exact
> `pytest rc=1`; terminal `2 failed, 1358 passed, 1 warning in 169.85s (0:02:49)` matches the corrected
> anchored optional-elapsed regex; observed failures exactly equal the two permitted
> `test_order_state.py` gc-referents node IDs both ways; failures `0`; `A-3 CHECKER PASS`. Canonical VM
> logs `/home/gatea/gatea-A3-postcheck-20260808C.log` and `…-clean.log`: both SHA-256
> `56a80d53155ac73b39dac064260ff702532fad36562eafbbe75f28c2f6414878`, `738` B, byte-identical.
>
> **Transport noise — recorded, not concealed:** the first PowerShell stdin stream inserted a BOM before
> the shebang and printed a harmless `#!/usr/bin/env` command error outside the captured log after the
> postcheck had already returned PASS (the captured log itself was clean). A second byte-preserving Git
> Bash stream replay to the separate clean log had no transport error and produced the same 738
> bytes/hash/PASS. Non-gate transport noise. Clean-replay postcheck script `19003ef0…415f1`; runner
> `7a03c61d…6da16`; both `bash -n` rc `0`, 0 CR.
>
> **State:** service reverified `inactive`/`masked`, listener 8790 absent, no credentials loaded. Gate A
> IN PROGRESS after accepted A-3; A-4 not started. Existing owner authorization covers A-4 within the
> preregistered sequence; hard exclusions unchanged (credentials, broker/exchange access, successful ARM,
> orders, TESTNET/mainnet, master merge, economic action).
>
> **Next step only:** `[AI: Claude]` execute the transferred C `gatea_A4.sh` under Addendum D, capturing
> all seven conditions (active/running; loopback 127.0.0.1:8790 only; status durably not ARMED;
> application-level exact credential-free 409 with correct X-Confirm; no broker attempt in
> journal/bridge.err.log/sockets; persisted DISARMED and unchanged version; resolved running
> environment/start mode); stop at first FAIL; on failure run only read-only diagnostic, then stop+mask and
> write result/memory; on PASS update `_AI_MEMORY` before preregistering the exact A-5–A-9 commands (do not
> improvise them). Preserve old `GATE_A_RESULT_2026-08-08.md`; later write `GATE_A_RESULT_2026-08-08B.md`.
>
> ---

> ## ▶ NEWEST CHECKPOINT — GLM-5.2 bounded documentation: corrected A-3 checker frozen as run-kit C (2026-08-08)
>
> **Supersedes this document's stale B-era header** (`20260808B local run kit ready; staging
> authorization required`): Gate A has rerun through A-3 and the owner already authorized the
> preregistered `gatea-staging` teardown/rerun sequence, so staging authorization is no longer
> pending. The historic title is retained as-is; this newest checkpoint is the live state.
>
> **Evidence-checker repair only — not an implementation or audit.** This freezes the corrected A-3
> run-script checker as run-kit **C**. It does **not** alter candidate acceptance, the product bits, the
> artifact, D025 acceptance, or the repair-round count. Run-kit **B is preserved unchanged**; C differs
> only in the corrected `gatea_A3.sh` and the README — the other five scripts are byte-identical to B.
> **No transfer or remote execution is claimed:** the C bundle was frozen and validated locally only and
> the checker has **not** been re-run on staging. No code/scripts/artifacts/results/staging action/
> transfer/commit/push/git mutation occurred. Full record:
> `11_TRIAGE/GATE_A_LOCAL_RUN_KIT_2026-08-08C.md` (cites the B record and the A-3 checkpoint).
>
> **Frozen run-kit C bundle (local, not transferred):**
> `C:\WPI_ARTIFACTS\gatea-run-kit-20260808C-2ce41e34` (+ `.tar`); tar SHA-256
> `4ee5ba920800ceff8f55338bcba5b388d39d2457f9970795af89c9333767f855`; tar bytes `53760`; exact 9 members
> (root dir + `README.txt`, `SHA256SUMS`, six scripts); 7 manifest entries. Corrected `gatea_A3.sh`
> `2bfec1c230d77d70f30bda5560f824fe970b4c2fca098d3fdda49129f2465d1c` / `5087` B (B `33934221…604443` /
> `4064`). README `47278c48e1e183c15013be583279dcec0e82db88174427e53ba8906fccd12883`. Unchanged scripts:
> A0_A1 `0d456a8e…f1c11`, A2 `07a715aa…c053`, A4 `78aa7fca…fd9b4`, A4_diag `f75912a2…f101d`, teardown
> `19016d8f…c0b3`.
>
> **Independent local validation:** extracted the frozen tar to a unique disposable `C:\tmp` directory →
> 8 files, 7 manifest entries; `sha256sum -c` all OK; six `bash -n` rc `0`; every shell 0 CR bytes;
> corrected A-3 checker falsification RED/GREEN `10 passed, 0 failed`, rc `0`. Cleanup of the disposable
> `C:\tmp\gatea-c-verify-929e34808c0e47699d8964f879309072` was blocked by local command policy after
> exact-path verification; it remains isolated under `C:\tmp`, is **not** in either tar, is **not** in
> the repo, and was **not** removed — remove only by an allowed exact-literal cleanup.
>
> **State unchanged by this C freeze unit:** candidate `2ce41e34…` accepted; product/artifact/staging
> install not modified during this unit; Gate A **IN PROGRESS through A-3**; A-4 **not** started; current
> accepted `2ce41e34` install masked/inactive/not enabled, no listener, **no credentials.** No host
> contact, teardown, install, service start, credential, broker/exchange access, ARM, order,
> TESTNET/mainnet, master merge, or economic action occurred **in this C freeze unit** — this scopes only
> the C unit; A-0 through A-3 of the overall rerun did run on `gatea-staging` (see the A-3 rerun
> checkpoint below). The owner already explicitly authorized the preregistered `gatea-staging`
> teardown/rerun sequence, so no additional authorization is required to transfer run-kit C, run the
> retained-log A-3 postcheck, or run A-4 within that sequence; hard exclusions remain (credentials,
> broker/exchange access, successful ARM, orders, TESTNET/mainnet, master merge, economic action).
>
> **Next unit (precise):** (1) transfer run-kit C tar only to
> `/home/gatea/gatea-run-kit-20260808C-2ce41e34.tar`; verify hash/bytes/9-member set; extract to
> `/home/gatea/gatea-run-kit-20260808C-2ce41e34`; `sha256sum -c` + six `bash -n`. **Do not replace/delete
> B.** (2) Re-check A-3 without rerunning pytest: against `/home/gatea/gatea-A3-suite-20260808B.log`
> require last non-empty line to match the corrected anchored optional-elapsed regex; require
> `/home/gatea/gatea-A3-20260808B.log` to contain exact line `pytest rc=1`; require exact two-way
> equality between observed `FAILED ` node-ID lines and the two permitted gc-referents failures;
> preserve output at `/home/gatea/gatea-A3-postcheck-20260808C.log` — any mismatch is Gate A FAIL, else
> A-3 checker PASS. (3) Update `_AI_MEMORY` before A-4. (4) Run A-4 exactly under Addendum D, stop at
> first FAIL. No credentials/broker/successful ARM/orders/TESTNET/mainnet/master merge/economic action.
>
> ---

> ## ▶ NEWEST CHECKPOINT — GLM-5.2 bounded documentation: Gate A reran through A-3 (2026-08-08)
>
> **Routing:** the exact Claude Opus 5 implementation call was attempted first but returned
> `session limit — resets 11:50pm` before any edit. This checkpoint was therefore routed to **GLM-5.2
> as bounded documentation only** — not a substitute for a mandatory flagship audit or protected
> implementation. Only the three `_AI_MEMORY` / `11_TRIAGE` handoff files were edited; no code,
> scripts, artifacts, results, staging action, commit, push, or git mutation occurred.
>
> **Authorization scope:** owner (Barış) explicitly authorized the preregistered `gatea-staging`
> teardown/rerun sequence; **no credential, broker, successful ARM, order, TESTNET/mainnet, master
> merge, or economic action is authorized.** Gate A is **IN PROGRESS after A-3**; A-4 has **not**
> started; the service remains **masked/inactive** and **no credentials were loaded.**
>
> **Lead-verified facts through A-3 (recorded exactly):**
>
> - **Host teardown:** `gatea-staging` `172.24.55.233` verified Ubuntu 24.04; old `ebada020`
>   installation masked/inactive, no listener/process; bounded teardown **PASS** with leftovers `0`;
>   evidence retained at `/home/gatea/teardown-ebada020-20260808B`.
> - **Run-kit B tar** transferred and verified: SHA-256
>   `ac0fbaf2fefa8241c5c92f5bf35a3f9fc5258a4b7e30614988ed305afa61c0fb`, `61440` bytes, exact 9 members,
>   seven manifest entries OK, all six scripts `bash -n` clean.
> - **Product tar** `/home/gatea/payload_2ce41e34.tar` matched SHA-256
>   `d78b9e82e4138714fd5eabfb4996d8d831f28d14cf0b9e1149c8751739fe05f2`, `1047265280` bytes.
> - **A-0 PASS:** release `2ce41e34bceb599d80af24c5c33d835820ec321b`; manifest
>   `edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26`; 7059 manifest entries, 7060
>   regular files, `1033362481` bytes, nonregular `0`, full manifest check clean, CR bytes `0`.
> - **A-1 PASS:** Ubuntu 24.04.4, kernel `6.8.0-136-generic`, x86_64, Python 3.12.3, required commands,
>   UFW active/default deny/SSH only, clean install paths/user/process/port.
> - **A-2 PASS:** dry-run side effects `0`; install and verify PASS; unit SHA
>   `538c1c6038b475e87fb0e9b9c35fd4ebd8451b40ff93538f8fea5aa0b49279bd`; masked/inactive/not enabled;
>   env assignments `0`; no credential material; release/venv sealed. D.5 override probe caused verify
>   rc `1` with guard, byte-identical restore, post-restore verify rc `0`. The pre-start
>   `systemctl show -p Environment` output was empty and **must be captured again after start in A-4**.
> - **A-3 product suite PASS under Addendum D:** pytest rc `1`, terminal
>   `2 failed, 1358 passed, 1 warning in 169.85s (0:02:49)`, and exactly the two permitted
>   `test_order_state.py` gc-referents node IDs. Real log retained at
>   `/home/gatea/gatea-A3-suite-20260808B.log`.
> - **Checker defect — not a candidate failure:** the B A-3 wrapper falsely rejected the valid summary
>   because `grep -qxF` did not allow pytest's elapsed suffix; the first SSH wrapper timeout did not
>   kill the remote suite. This is a run-kit checker defect, not a candidate failure.
> - **GLM-5.2 repair round 1 accepted by Codex:** old predicate RED on the real log; repaired predicate
>   GREEN; prefix collision, changed counts, arbitrary suffix, non-terminal summary, malformed clock,
>   and missing `s` all rejected; `bash -n` both files rc `0`; falsification `10 passed, 0 failed`,
>   rc `0`. **The corrected checker has NOT yet been propagated/frozen/transferred to staging.**
>
> **Preserve old `GATE_A_RESULT_2026-08-08.md`; later write `GATE_A_RESULT_2026-08-08B.md`.** Ordered
> next steps are in `_AI_MEMORY/NEXT_STEPS.md`.
>
> ---

> ## ▶ CURRENT STATE — PICK UP EXACTLY HERE
>
> The accepted repair candidate remains **`2ce41e34` under D025**. The locally prepared 20260808B
> Gate A run kit is now validated and recorded in
> `11_TRIAGE/GATE_A_LOCAL_RUN_KIT_2026-08-08B.md`. This work did not change product code, the
> candidate, the artifact, acceptance, or the repair-round count. **Gate A has not rerun.**
>
> The frozen single transfer tar is ready locally but **not transferred**:
> `C:\WPI_ARTIFACTS\2ce41e34bceb599d80af24c5c33d835820ec321b.tar`, SHA-256
> `d78b9e82e4138714fd5eabfb4996d8d831f28d14cf0b9e1149c8751739fe05f2`, `1047265280` bytes.
> Six scripts in `C:\tmp` are re-baselined to Addendum D and pass Git Bash `bash -n`; their exact
> hashes are frozen in the run-kit record.
>
> **Important A-4 correction:** `/api/arm` checks `X-Confirm` before the credential-free guard.
> Therefore a POST without the current confirmation value can only return `409 stale state_version`,
> which is non-evidence and fails A-4. Corrected `C:\tmp\gatea_A4.sh` first requires the running
> process to report the exact credential-free/DISARMED fail-closed fields and a valid state version;
> any mismatch exits with `BLOCKED - NO POST ISSUED`. Only after those preconditions pass does it send
> `X-Confirm`, require the exact credential-free 409, and prove state/version remain unchanged.
> Five no-network falsification cases and the candidate's real in-process refusal test passed.
>
> **DO NOT contact staging, transfer, tear down, install, start the service, or run Gate A.** Explicit
> Barış authorization is still required. The old `ebada020` host state was not rechecked in this work;
> its last verified state remains masked, inactive, no listener, no credentials, nothing armed.
>
> **Offline validation and supplemental audit (same 20260808B checkpoint):** offline local A-0 passed
> every A-0 identity check against the real frozen tar in a fresh disposable HOME (tar SHA
> `d78b9e82…fe05f2`, `1047265280` B; `RELEASE_SHA` exact `2ce41e34…`; manifest `edb0fd34…20d26`;
> 7059 entries / 7060 regular files / 1033362481 B / 0 non-regular; `sha256sum -c` rc 0, 0 problem
> lines; 0 CR bytes on all five `deploy/linux/*.sh`). The same script then stopped at A-1 because this
> workstation is Windows and `/etc/os-release` is absent — **A-1 was NOT executed/accepted; no Linux
> or Gate A claim is promoted.** DeepSeek supplemental audit attempt 1 exhausted `max_iters` with no
> verdict and the focused retry stopped without finish/verdict — **supplemental non-accepting evidence
> only.** Hardening: A-4 records `start_rc` as `PIPESTATUS[0]`; A-3 uses `grep -qxF`; A-4/A-4_diag
> query only meta keys `app_state` and `schema_version`; all six scripts pass `bash -n`; the exact
> embedded A-4 five-case no-network falsification and the real in-process refusal test
> (`1 passed, 1 warning in 0.52s`) still pass. Replaced hashes (A3 `33934221…604443`/4064 B, A4
> `78aa7fca…fd9b4`/16228 B, A4_diag `f75912a2…f101d`/3053 B) are in the run kit; unchanged hashes
> remain as written. Cleanup of the disposable
> `C:\tmp\gatea-a0-offline-bb964b4106b24ea192f830065a1b9992` was refused twice by local command
> policy after exact path verification; it remains isolated under `C:\tmp` and must be removed only by
> an allowed exact-literal cleanup — **do not claim it was removed.** Candidate/artifact/acceptance/
> repair-round state unchanged; no staging contact or hard-gated action; explicit staging
> authorization still required.
>
> **Frozen local-only run-kit bundle:**
> `C:\WPI_ARTIFACTS\gatea-run-kit-20260808B-2ce41e34.tar`, SHA-256
> `ac0fbaf2fefa8241c5c92f5bf35a3f9fc5258a4b7e30614988ed305afa61c0fb`, `61440` B, exact 9-member
> archive. All seven manifest entries match and all six shell files have 0 CR bytes. Its README
> explicitly says local preparation only, not authorized to transfer or run. The bundle was **not
> transferred or executed** and does not change the staging gate.
>
> **Next steps:** when local command policy permits, remove only the exact disposable directory named
> above. After explicit staging authorization, transfer the run-kit bundle, verify its tar hash and
> `SHA256SUMS`, run the prepared teardown first and require leftovers `0`, transfer the one product
> tar, and run Gate A from A-0 under Addendum D and stop
> at first FAIL; bind A-4 to the corrected step-8 result; capture `systemctl show -p Environment`,
> `bridge.err.log`, and verifier override rejection/restoration/clean re-verification; preserve the
> old result and write `GATE_A_RESULT_2026-08-08B.md`. Update `_AI_MEMORY/` before the next work unit.
>
> ---
>
> ## PRIOR PICKUP — accepted-candidate state before local run-kit validation
>
> Session closed cleanly on 2026-08-08. **Nothing is broken, nothing is half-written, no work is in
> flight.** The A-4 repair candidate is **accepted** and the artifact is built and verified.
>
> **State:** the env-override defect from round 1 is repaired and the new candidate
> **`2ce41e34` is ACCEPTED under D025** (`11_TRIAGE/GATE_A_DISARM_FIX_AUDIT_ROUND2_2CE41E34_2026-08-08.md`):
> `gpt-5.6-sol` xhigh **PASS**, `claude-opus-5` xhigh **PASS-WITH-NITS** (0 required), `GLM-5.2` **PASS**
> and executed the suite; DeepSeek V4 Flash returned a non-execution BLOCK (`No access to ClinePass
> subscription models yet.`), which is supplemental per D025 and does not veto acceptance. The accepted
> artifact is at `C:\WPI_ARTIFACTS\2ce41e34bceb599d80af24c5c33d835820ec321b` (manifest
> `EDB0FD34…20D26`, 7059 entries / 7060 files / 1 033 362 481 B, 0 CR bytes on all five deploy scripts;
> first-start pin 1, steady pin 0, env guard 1, behavioral test 1). Gate A inputs are re-baselined in
> `GATE_A_PREREGISTRATION_ADDENDUM_D_2026-08-08.md`.
>
> **This accepts the repair CANDIDATE, not the Gate A result.** Gate A has not rerun. A-4 remains
> historically failed until the `2ce41e34` artifact passes on staging.
>
> **DO NOT transfer, install, tear down, or run Gate A.** Those await explicit staging authorization from
> Barış. The old `ebada020` install is still on `gatea-staging`: **masked, inactive, no listener on 8790,
> no credentials provisioned, nothing armed** — left in a known safe state pending the authorized
> clean-host teardown. `2ce41e34` supersedes the unaccepted `ed3d0534`; do not transfer or install the
> `ed3d0534` artifact.
>
> **Next safe step (owner-gated):**
> 1. Barış authorizes staging action.
> 2. Tear down the stale `ebada020` install on `gatea-staging` with the proven `C:\tmp\gatea_teardown.sh`
>    (leftovers 0 last time). `rollback.sh` takes `--to-release-sha` and is **not** an uninstaller.
> 3. Transfer the `2ce41e34` artifact as **one tar**.
> 4. Run Gate A from **A-0** per Addendum D, stopping at the first FAIL. Expected Linux A-3:
>    `2 failed, 1358 passed, 1 warning` (the same two pre-registered gc-referents failures; one new
>    passing test function). **Required host evidence** for the A-4 round (capture verbatim, redact any
>    value): `systemctl show -p Environment mtc-bridge-first-start.service`, and an explicit verifier
>    rejection of a temporary `MTC_BRIDGE_START_MODE=` env-file override (then remove the temp line and
>    re-run `verify.sh` to confirm a clean PASS).
> 5. Preserve the existing `GATE_A_RESULT_2026-08-08.md` intact and write
>    `GATE_A_RESULT_2026-08-08B.md` for the new run, either way.
>
> **Hard stop — unchanged:** merge to master, WP-V / deployment, credential handling, broker or exchange
> access, ARM, orders, TESTNET, mainnet, KVM2, Pine/parity/MTC/trading changes, any economic action.
>
> ---
>
> The blocks below this line are the **prior** state (round-1 `ed3d0534`, NOT ACCEPTED) preserved as
> history. They remain accurate for how the repair got here; the section above is the live pickup.

---

# (HISTORY — round 1, `ed3d0534`, superseded by the current state above)

> ## ▶ PICK UP EXACTLY HERE (round-1 state — superseded 2026-08-08 by the section above)
>
> Session closed cleanly on 2026-08-08. **Nothing is broken, nothing is half-written, no work is in
> flight.** Both flagship audits finished before shutdown.
>
> **State:** the A-4 repair is built and committed at **`ed3d0534`**, the artifact is rebuilt and
> verified, Gate A is pre-registered in Addendum C — and **`ed3d0534` was audited and NOT ACCEPTED.**
> `claude-opus-5` xhigh returned PASS-WITH-NITS; `gpt-5.6-sol` xhigh returned **REQUEST_CHANGES** with
> one required finding, which the Lead reproduced. D025 rule 3 needs both accepting.
>
> **THE ONE THING TO FIX — needs Barış's authorization first, it is a product change.**
> `EnvironmentFile=` **overrides** `Environment=` in systemd. So the start-mode pin at
> `deploy/linux/systemd/mtc-bridge-first-start.service.template:42` is defeated by any
> `MTC_BRIDGE_START_MODE=credentialed` written into `/etc/mtc-bridge/mtc-bridge.env` (declared at
> line 45) — and `verify.sh:138` rejects only `HL_LIVE_ACK=`, so the verifier reports PASS while the
> override wins.
>
> **Minimum repair, agreed by both auditors, inside the existing file family:**
> 1. `deploy/linux/verify.sh` — reject any `MTC_BRIDGE_START_MODE=` definition in `${MTC_ENV_FILE}`,
>    one needle in the same section as the existing `HL_LIVE_ACK` check at line 138.
> 2. `tests/test_linux_deployment.py` — regression test proving that rejection, falsified first (D026).
> 3. Docs nit, ride along: `deploy/linux/README.md` and `deploy/linux/env/mtc-bridge.env.template` say
>    nothing about the start mode, while `MTC_BRIDGE_STATE_DB` gets both. Add "set by the unit;
>    defining it here would override the unit" — now literally true.
>
> **Then:** new SHA → rebuild artifact → **repair round 2 of max 3** with both flagships → only then
> tear down the stale `ebada020` install on `gatea-staging` with `C:\tmp\gatea_teardown.sh`, transfer
> the new artifact as one tar, and run Gate A from **A-0** per Addendum C. Stop at the first FAIL.
> Write `GATE_A_RESULT_2026-08-08B.md`, keeping the first result document intact.
>
> **Capture on the host next round** — the one thing neither auditor could execute (no systemd on this
> workstation), so precedence currently rests on `man systemd.exec`:
> `systemctl show -p Environment mtc-bridge-first-start.service`
>
> **`ebada020` is still the last accepted candidate.** The rebuilt artifact
> `C:\WPI_ARTIFACTS\ed3d0534…` is a valid build of an **unaccepted** commit — **do not transfer or
> install it.**
>
> **Do not mistake this for a failed repair.** Both flagships ran a real `python -m bridge.app` with no
> credentials and got a listener on `127.0.0.1:8790`, status `DISARMED / credential_free_disarmed`, and
> **`POST /api/arm` → 409 "ARM unavailable in credential-free DISARMED start mode"** — exactly the
> application-level refusal A-4 could not obtain. The fix works; it is the *enforcement* of it that has
> a hole.

---

## Since this handoff was first written (2026-08-08, later the same day)

| Step | State |
|---|---|
| A-4 repair implemented | **`ed3d0534`**, 3 files, 6 insertions, 1 deletion. Codex `gpt-5.6-sol` under Lead scope; Lead verified diff, constants, D026 red-then-green and suite against the files |
| Lead suite reproduction | `1359 passed, 1 warning in 198.90s` — matches the floor |
| Artifact rebuilt | manifest `8964CC43…EE4B`, 7059 entries, 7060 files, 1 033 359 494 B, 0 CR bytes on all five deploy scripts, fix present in payload, steady clean |
| Gate A re-baselined | `GATE_A_PREREGISTRATION_ADDENDUM_C_2026-08-08.md` (`783335e3`) |
| **Two flagship audits of `ed3d0534`** | **OWED — dispatched, then lost to the shutdown. Re-run from scratch.** |
| Gate A rerun | **not started**, correctly blocked on the audits |

**What the repair does:** pins `Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed` in the
first-start unit, adds the same declaration to `verify.sh`'s unit-assertion list so every install
re-checks it on the host, and asserts in the deployment tests that the first-start unit declares it
while the **steady** unit does not. Placed in the unit rather than the `EnvironmentFile` (contract-only,
values never written) or an `ExecStart` flag (the unit is hashed into `install_manifest.json`, so it
cannot drift silently). Name and value read from `bridge/app.py:30,32`, not guessed.

**Deferred by explicit owner decision — do not slip it into a later commit:** whether module-level
`create_app()` at `bridge/app.py:282` should construct a broker at import time at all. Barış chose the
small fix only, on the reasoning that it is sufficient for a staging gate and the deeper change does
not fit the remaining budget. "Told not to ask for credentials" is weaker than "cannot ask" — revisit
as its own decision, not as a side effect.

**A-4's bar is higher now, and it is pre-registered.** Addendum C §C.4 lists seven conditions. The one
that failed before must now genuinely hold: `POST /api/arm` must be **refused by the application**, and
a connection refusal explicitly does not count. Also pre-recorded: read
`/var/log/mtc-bridge/bridge.err.log`, because the unit appends stderr to a file and tracebacks never
reach `journalctl`.

**Open question the rerun should answer (recording obligation, not pass/fail):** `EnvironmentFile` is
declared *after* the unit's `Environment=` lines, so if an operator ever placed
`MTC_BRIDGE_START_MODE` in that file, systemd's precedence decides whether pinned DISARMED survives.
Establish it by execution rather than assumption.

**Machine note:** `GATEA-STAGING` is a Hyper-V VM on this workstation, so it stops with the machine.
Nothing was running on it at shutdown — the `ebada020` install is installed-but-masked, inactive, no
listener, nothing armed, no credentials provisioned.

---

## Original handoff — Gate A ran, A-4 FAILED (2026-08-08, earlier)

**Supersedes `NEXT_SESSION_HANDOFF_2026-08-03B.md` entirely.** That file's "single remaining blocker"
(the second flagship audit) is closed, and Gate A has since run.

Companion records, in read order:
1. `11_TRIAGE/GATE_A_RESULT_2026-08-08.md` — the Gate A run, with the A-4 traceback.
2. `11_TRIAGE/GATE_A_INTEGRATION_FLAGSHIP_AUDITS_EBADA020_2026-08-08.md` — D025 acceptance.
3. `11_TRIAGE/GATE_A_PREREGISTRATION_ADDENDUM_B_2026-08-08.md` — the re-baselined Gate A inputs.

---

## State in one screen

| Thing | State |
|---|---|
| Candidate `ebada020a59edf539f60acfbb3a6bf870c8679e9` | **ACCEPTED** 2026-08-08 under D025. Both flagships accepting, zero required findings from any auditor |
| Gate A A-0 identity · A-1 clean-host · A-2 install · A-3 Linux suite | **PASS · PASS · PASS · PASS** |
| Gate A **A-4** starts DISARMED | **FAIL** — service exits 1 in 482 ms, never listens |
| Gate A A-5 … A-9 | **NOT RUN** — first-FAIL rule; each presupposes a running service |
| `origin/master` | `637307e8`, unchanged — nothing Gate A is merged |
| Docs line | `feature/donchian-crypto-ladder` @ `cc413dc3` (pushed) |
| Staging host | `gatea-staging` / `172.24.55.233`, `ebada020` install retained, unit re-masked, inactive, no listener |

## The blocker, stated exactly

A-4 fails because **the shipped deploy artifact never selects the credential-free DISARMED start
mode.** This is flagship NIT 1, which Addendum B §B.3 declared in advance, now reproduced in
production form.

```
bridge/app.py:282   module-level  runtime_app = create_app(
bridge/app.py:150                 runtime_broker = broker or _build_broker(root, dry_run)
bridge/app.py:244                 resolve_hyperliquid_credentials()
bridge/settings.py:113            raise RuntimeError
RuntimeError: Hyperliquid credentials not found: set both HL_ACCOUNT_ADDRESS and HL_API_WALLET_KEY …
```

Confirmed on the host, executed as the service account: `resolve_start_mode` → **`credentialed`**. The
installed unit's `ExecStart` is bare `python -m bridge.app`; the env template names no
`MTC_BRIDGE_START_MODE`; `install.sh` leaves every env variable unset by design. So the
credential-free path that `17402a58` added, and that both flagships verified in-process, is
**unreachable from the deployment**.

**It fails closed — say this accurately.** Nothing armed. **Zero** broker connection attempts: the
exception fires while *constructing* the broker, before any network I/O, and both the journal and
`ss -tnp` show nothing. No listener ever opened. The store persisted `app_state=DISARMED`,
`schema_version=4`. A-4 fails because one of its three required confirmations — *the ARM path
refuses* — **cannot be obtained at all** (`POST /api/arm` → `Errno 111 Connection refused`, i.e. no
application refusal to observe). Non-execution is never acceptance.

**Not a regression of `ebada020`.** The identical failure is in the unit's journal at
`Aug 01 23:35:27`. It was invisible on 2026-08-02 because that run died at A-2 and never reached A-4.
Repairing the CRLF defect is precisely what let the gate advance far enough to expose this. The gap
lives in `deploy/`, outside the nine-file merge scope, so `ebada020` is **not** retroactively rejected.

## What the next session must do — and what it must not do

**No product code was modified during the Gate A run. The repair is a product change and needs a new
explicit authorization from Barış.**

1. **Get authorization, then wire the start mode into the deploy artifact.** Either
   `ExecStart=… -m bridge.app --start-mode credential_free_disarmed` in
   `deploy/linux/systemd/mtc-bridge-first-start.service.template:34` and
   `mtc-bridge-steady.service.template:37`, or name `MTC_BRIDGE_START_MODE` in
   `deploy/linux/env/mtc-bridge.env.template` and have `install.sh` set it.
2. **Ask the design question rather than assuming:** should module-level `create_app()` at
   `app.py:282` construct a broker at import time at all? A first DISARMED start arguably should not,
   under any mode. That is a bigger change than the wiring and should be decided, not slipped in.
3. **Fold in the cosmetic-but-misleading message** at `bridge/settings.py:113`: it tells a Linux
   operator to set variables in `HKEY_CURRENT_USER\Environment`, a Windows registry path, in the
   failure message of a Linux-only systemd service.
4. **Then: new frozen SHA → rebuilt artifact → fresh flagship round under D025 → Gate A from A-0.**
   Do not restart mid-gate. A-0→A-3 passing gives high confidence the rerun reaches A-4 quickly.
5. **NIT 3 stays separately owed:** `test_order_state.py::test_gc_referents_of_{transitions,raw_aliases}_contain_no_mutable_container`
   fail on CPython 3.12 and pass on 3.14. The production venv **is** 3.12, so the production floor is
   amber until this is scoped. Pre-existing on `637307e8`, out of Gate A scope.

**Hard stop — unchanged, needs a new explicit instruction from Barış:** merge to master, WP-V /
deployment, credential handling, broker or exchange access, ARM, orders, TESTNET, mainnet, KVM2,
Pine/parity/MTC/trading changes, any economic action.

## Facts worth not rediscovering

**Gate A is re-runnable cheaply.** The step scripts are on the host at `/tmp/a01.sh`, `/tmp/a2.sh`,
`/tmp/a3.sh`, `/tmp/a4.sh`, `/tmp/a4d.sh`, sources in `C:\tmp\gatea_*.sh`. They are already
re-baselined onto `ebada020`; a new SHA needs only the constants at the top changed. Host logs:
`~/gatea-A0A1-20260808.log`, `~/gatea-A2-dryrun-20260808.log`, `~/gatea-A2-install-20260808.log`,
`~/gatea-A3-suite-20260808.log`, `~/gatea-A3-20260808.log`, `~/gatea-A4-20260808.log`,
`~/gatea-A4-diag-20260808.log`, `~/gatea-teardown-20260808.log`, plus
`/var/log/mtc-bridge/bridge.err.log` — **which is where the real traceback lives; the journal shows
only systemd's lines**, because the unit sets `StandardError=append:…`.

**The host was carrying a stale install and roughly 14 G of debris.** Both were cleared under Barış's
explicit authorization on 2026-08-08 (disk 64% → 30%). The torn-down install was release `a1dd5b46…`
from the failed 2026-08-02 attempt, and **its venv was the `a1dd5b46…` interpreter every prior Linux
run used** — that is why Addendum B's venv pin is superseded and A-3 ran on the venv A-2 installed
(same CPython 3.12.3 / pytest 9.1.1). Teardown evidence preserved at
`~/teardown-a1dd5b46-20260808/`. `rollback.sh` takes `--to-release-sha` and is **not** an uninstaller.

**Codex routing corrections are now in `AI_ACCOUNT_AND_MODEL_ROUTING.md`** — the `free` /
`.codex_OLD` route is **Plus**, not Free, and carried the binding flagship audit; a home's
`models_cache.json` is **not** evidence of model availability (a live probe overrides it); the
launcher needs its Codex flags as `-CodexArgs $array`; an isolated audit worktree needs
`--dangerously-bypass-approvals-and-sandbox`, and a non-repo scratch dir needs
`--skip-git-repo-check`.

**D025 rule 3 names the flagship pair as `claude-opus-5` xhigh + `gpt-5.6-sol` xhigh** (`AGENTS.md:66`).
GLM-5.2 is canonical auditor 4 and holds no flagship slot. The 2026-08-03 records had described
GLM-5.2 as the first flagship; that reading does not match the rule, so a fourth round was run rather
than accepting on the weaker reading. Recorded honestly: the integration merge was authored by a Claude
Lead session, so the cross-model axis on the merge comes from round 3 (`gpt-5.6-sol`), not round 4.

## Budget

≈14–17 h of the 50-hour plan remained before this session; WP-A (3 h), WP-R (6 h) and WP-V (8 h) total
17 h and are all still ahead. The A-4 repair, its artifact rebuild and its flagship round are **again
unbudgeted work**, as the Gate A repair queue was. **Re-plan with Barış before committing to the
remainder** rather than absorbing it silently.
