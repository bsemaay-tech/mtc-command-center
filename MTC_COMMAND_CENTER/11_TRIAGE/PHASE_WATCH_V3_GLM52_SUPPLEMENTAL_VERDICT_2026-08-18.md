# Phase Watch V3 — GLM-5.2 supplemental adversarial verdict (verbatim), 2026-08-18

Captured from the Z.AI GLM-5.2 review session dispatched by the Fable Lead on
2026-08-18 against frozen master `14559c2a`. Context and Lead reproduction:
`PHASE_WATCH_V3_PREAPP_VERIFICATION_2026-08-18.md`.

---

﻿All 12 frozen artifacts read, plus the design doc, provisioning, and the three test scripts. Freeze integrity first, then findings by the four attack categories.

## Freeze-integrity verification (done first)

Every file's **LF-normalized SHA-256 matches the `FREEZE_MANIFEST.md` pinned values exactly** (all 11 verified byte-for-byte). Git plumbing (`hash-object`, `ls-tree`) was blocked in this session, so I could not independently confirm the blob-OID column — the LF content column matching is strong evidence the content is the frozen content.

However, the **working tree here is CRLF** (`file` reports CRLF on all 12), and that matters — see F1.

---

## A. Escape paths — verdict: **clean, with one config-level caveat**

No injection exists. `mtc-watch-collect:7-15` compares `SSH_ORIGINAL_COMMAND` against fixed literals in a `case`; the match arms `exec` fixed command strings that never re-expand the variable. Glob/metacharacters in a client command cannot match `check1`..`check6`. Every menu entry scrubs with `env -i`, uses absolute paths, and issues no writes. Client side, only a table constant crosses the wire, and `collect_kvm2_evidence_v3.ps1:78-81` builds argv via `ArgumentList` (no shell re-parse). Two layers (ForceCommand + `command=,restrict`) genuinely overlap: key `restrict` covers pty/forwarding/agent/user-rc even if the drop-in's `Include` never loads.

**F1 (HIGH — integrity/operational, and it's the freeze's own weak point):** The canonical form is LF; a Windows checkout carries CRLF. Nothing in `provisioning-commands.sh` normalizes line endings or verifies any hash on the host before `install`. Consequences: (a) `#!/bin/sh\r` shebang → none of the three shell scripts execute at all; (b) an operator who hand-fixes that on the host has silently voided byte-exactness — the exact thing the freeze exists to guarantee. The `sshd -t` gate catches some of this loudly, but there is no `sha256sum -c` step anywhere in the application chain. Required: pinned-hash verification on-host (against LF-normalized bytes) plus a documented LF-preserving transfer method, before step 2 of provisioning.

**F2 (MEDIUM — config semantics):** `70-mtc-watch.conf:4-12` opens `Match User mtc-watch` and never terminates it. An unterminated `Match` in an included drop-in can leak the conditional context into later-sorted drop-ins and the remainder of the main config (behavior varies by OpenSSH version). Harmless today, silently wrong the day anyone adds `99-*.conf`. Fix is free: end the file with `Match all`. Also add `sshd -T -C user=mtc-watch,...` to provisioning — it proves Layer 1 is actually in effect (Include present, Match parsed) instead of hoping.

---

## B. Backup contract

**F3 (HIGH — last-line-of-defense guard is dead code):** `mtc-bridge-backup:62` — `[ "$SIZE" -gt 0 ]` where `SIZE=$(du -sb "$STAGE/bundle")`. `du -sb` of a **directory is always ≥ 4096**, even with zero files. The "empty bundle" guard can never fire for a directory-shaped bundle. And on an empty file set, `mtc-bridge-backup:63`'s `xargs -0 sha256sum` (GNU xargs runs once on empty input) makes `sha256sum` hash EOF → a deterministic, valid-looking `HASH`. Net: an empty bundle is promotable with `verify_result: PASS`. The design doc (§3 step 4) specifies "nonzero size" as root's independent check — the design has the same hole. Falsification: `mkdir -p /tmp/b && du -sb /tmp/b` → `4096`; then `find /tmp/b -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum` → non-empty hex. Required: count regular files (`find ... | wc -l`) and require ≥1, plus a total-bytes check.

**F4 (HIGH — the recorded hash is unchecked):** line 63 has no `pipefail`, no `-n "$HASH"` test, and no post-`mv` recompute against `$DEST`. If `find`/`sha256sum` fails or truncates mid-pipeline, a partial composite hash is written into a `PASS` manifest — silently wrong integrity metadata, discovered only at restore time, the worst possible moment. Required: `set -o pipefail` (or explicit per-stage checks) + verify `HASH` non-empty + recompute from `$DEST` after promote and compare before declaring PASS.

**F5 (MEDIUM — design-vs-bytes divergence at the promote gate):** design §3 step 4 says root "lstats the staged bundle (**regular file, expected owner**, nonzero size)". The implementation (lines 60-62) checks neither: no owner check at all, and `-d` accepts any owner's directory. The B4 assurance ("orchestrator lstat checks refuse") is therefore weaker than the design claims. Staging isolation (root-0711 parent + 0700 stage) partially compensates, but the owner check should exist as designed.

**F6 (MEDIUM — least-privilege claim is false in both design and bytes):** design §3 sets `/var/backups/mtc-bridge` 0755 and bundles 0444 — which makes **every bundle world-readable to any local account**, then asserts "the watcher can read the manifest and nothing else." Those two statements are mutually exclusive. The bytes faithfully implement the permissive one. Fix: directory 0700 + `u:mtc-watch:--x` ACL, bundles 0400 (status.json keeps 0644 + ACL). On a two-account VPS impact is modest; it's still a contract violation a freeze review must not wave through, and it widens if the DB snapshots carry anything sensitive.

**F7 (MEDIUM — prune/staging failure semantics):** (a) `chattr -R -i`/`rm -rf` at lines 85-87 are unchecked and the run still exits 0 — a retention failure is reported as success (category 3). (b) **`.staging` is never garbage-collected**: every failure path deliberately preserves its staging dir (per design) and nothing ever sweeps them, so the failure regime — precisely when nobody's watching — accumulates unbounded partial DB snapshots. (c) `chattr -R +i ... 2>/dev/null || true` (line 68) silently accepts immutability failure while the design's B5 premise depends on it.

**F8 (LOW-MEDIUM — the manifest loses history on failure):** `fail_manifest` (17-31) parses only `bundle` and `consecutive_failures` from the prior manifest and blanks `last_success_utc`. After one failure you can no longer distinguish "never succeeded" from "succeeded yesterday". Preserve `last_success_utc` like `bundle` is preserved. Related: if `fail_manifest`'s own writes fail (disk full — unchecked at lines 25-28), the previous `PASS` manifest survives with no failure recorded at all; detection then rests entirely on the 26 h age heuristic.

**Symlink attack — verdict: held.** Ordering is correct: `-L` checks (39-40) precede every write; `$DEST` existence is pre-checked (65); `.staging` inside `$ROOT` makes `mv` a same-FS atomic rename; `chown -R`/`chmod -R`/`chattr -R` don't follow during recursion; prune's `rm -rf` removes symlinks without following. Residual nits: `find -type f` excludes symlinks so a tool-planted symlink inside a bundle is promoted but never hashed; and the unquoted `$(ls -1d ...)` word-split at line 81 is only safe because the directory is root-only.

---

## C. Failure reported as success

1. **F9 (MEDIUM):** `mtc-watch-collect:8` — check1's exit code is that of the *last* command (`systemctl show`), which succeeds for a dead unit. `systemctl is-active` failing is invisible in the exit code; the client (`collect_kvm2_evidence_v3.ps1:103`) marks a dead service `COLLECTED` on exit 0 + non-empty output. Detection is pushed entirely to the out-of-scope summarizer.
2. **F3/F4/F7 above** — empty-bundle PASS, wrong-hash PASS, prune-failure exit 0.
3. **F10 (LOW):** a hung `runuser` holds `flock`; subsequent timer runs exit silently at line 35 with **no manifest update at all** — `consecutive_failures` never rises; only the age heuristic notices. Consider `timeout` on the tool invocations.
4. Clean, for the record: empty client output → `EMPTY` + exit 5; timeout → `ERROR`; agent fingerprint gate → exit 3; missing fixture → exit 1; partial run dirs lack the `COMPLETE` marker. The client's fail-closed discipline is genuinely good.

---

## D. Test matrices — "can each judge false-pass?"

**F11 (HIGH — client is incompatible with its declared platform):** `collect_kvm2_evidence_v3.ps1:81` uses `System.Diagnostics.ProcessStartInfo.ArgumentList` — **.NET Core 2.1+ only; it does not exist in .NET Framework / PowerShell 5.1**, where the context says the client must run. `$psi.ArgumentList` resolves to `$null` and `.Add()` throws, killing the script at the first live check. Worse: **fixture mode never reaches that line, so all fixture-path acceptance evidence passes while live mode is dead.** Required: rebuild argv with `.Arguments` + correct quoting, or an explicit `throw` if `ArgumentList` is absent.

**F12 (HIGH — systematic judge weakness in `tests_T`):** every "refusal" judge is satisfied by an ordinary connection failure. `ssh` to an unreachable/sshd-down host prints *"Connection refused"* — which contains "refused" and exits ≠0:
- **T2/T3** (lines 19-20): false-PASS on any connection-level refusal. Both should anchor to `refused: unknown check id` (the collector prints exactly that for both empty and arbitrary commands — T8 already anchors correctly, proving the authors knew how).
- **T4** (21): alternation `PTY|refused|not permit` + any nonzero exit — "Connection refused" passes it without a PTY ever being requested.
- **T10** (27): judge is `$c -ne 0` — any auth or network failure passes a test whose entire point is *password* auth being refused.
- **T1** (18): `$o -match 'active'` is a substring match — **"inactive" and "failed" output satisfies T1**, so the happy-path test passes against a dead service. Line-anchor it (`(?m)^active\r?$`).
- **T5** (22) is broken in the *opposite* direction: nothing ever uses the tunnel, `-L` needs no server negotiation, sshd's denial only surfaces on channel use — so on a **correctly locked-down server T5 always FAILs**. That's an acceptance blocker that invites the operator to weaken the judge — the exact D026 failure mode. Fix: actually exercise the tunnel (background `ssh -N -L`, then `curl 127.0.0.1:19999` expecting failure) or restructure around a used channel.

**F13 (HIGH — the B matrix is not a falsification suite):** `tests_B_backup_failures.sh` contains **zero executable tests** — comments and one `echo` — while `FREEZE_MANIFEST.md` markets "full T/B/W falsification scripts" and design §4 invokes D026 RED/GREEN evidence. Worse, several inductions are **practically impossible against the frozen bytes**: B4/B5 require interposing *between* two adjacent lines of a running script (`$$` is unpredictable, so "pre-place a colliding target" can't pre-place the right name), and the only clean way to induce them is a patched orchestrator — which the freeze's own change-control forbids. B1 requires repointing the **live** `/opt/mtc-bridge/current` symlink at a broken copy, with no recorded restore/verify step. As frozen, this matrix cannot produce the evidence it promises. Required: either a real script with per-test judges (as T got), or an honest relabel to "manual contract" plus an explicitly sanctioned induction mechanism that doesn't mutate production state or the frozen bytes.

**F14 (LOW):** coverage gaps — no success-path retention test (that prune deletes only beyond 14 and ever deletes at all), no hang/lock-held test, no corrupt-manifest test. And `tests_W_agent.ps1` W4 merely re-checks the fingerprint, while design W4 says "run the collector preflight from the task account" — the task-context run of the actual collector is untested.

**Nits:** `mtc-bridge-backup:83` uses bare `basename`, contradicting the hardening table's "every command absolute" (safe only because PATH is controlled); fixture containment at `collect_kvm2_evidence_v3.ps1:40` is a prefix match without a trailing separator (`C:\LAB\HERMES_WATCH2` passes); `tests_W` names the key `mtc_watch_ro.pub` vs `mtc-watch-ro` elsewhere; provisioning's manual first backup run and the placeholder-substitution precondition live only in comments — and until that run happens, check4 errors on every collection (timer fires at 03:00 UTC only).

---

## Verdict: REQUEST_CHANGES (pre-application)

Nothing here is applied yet, and the escape-path core — the fixed-literal menu, two-layer ForceCommand, sanitized env, no client-influenced server paths — is genuinely sound; I found no path to a shell or beyond the read-only surface. The blocking findings are F1 (no on-host integrity/LF gate), F3/F4 (empty-bundle PASS, unchecked hash in a PASS manifest), F11 (client cannot run on its declared platform), F12 (T-judges that false-pass on connection refusal, T1 false-passes on "inactive"), and F13 (B matrix not executable as frozen). F2, F5, F6, F7, F8, F9, F10, F14 are required repairs of lower urgency but should land before the exact-application gate (c), since any byte change re-opens the freeze anyway — batch them.

I made no writes and ran no state-mutating commands; the only shell activity was hashing and line-ending inspection of the frozen files.
