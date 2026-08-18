# Phase Watch V3 — pre-application verification + supplemental review, 2026-08-18

Lead: Claude Fable (same session as `WORKTREE_CLEANUP_EXECUTION_2026-08-18.md`).
Scope: independent Lead verification of the frozen artifact set at master
`14559c2a`, supplemental adversarial review, live T0-capacity probes. **No KVM2
contact, no artifact byte changed, `WATCH_ACTIVE: NO` untouched (live-verified in
`C:\LAB\HERMES_WATCH\PHASE_WATCH.current.md`), no credential touched, no
Telegram send, freeze not voided.**

## 1. Freeze-ledger verification — PASS

- `PHASE_WATCH_FC_FROZEN_V3/` at master `14559c2a` holds exactly 12 files.
- All 11 pinned git blob OIDs match `FREEZE_MANIFEST.md` (authoritative column).
- All 11 SHA-256 values match when computed over the blob (LF) bytes.
- Commands: `git ls-tree master -- …` + `git cat-file blob … | sha256sum`, run in
  the clean control worktree.

## 2. Lead property verification of the frozen bytes — all present

Two-layer confinement (sshd `Match`+`ForceCommand` absolute path; root-owned
`command=…,restrict` authorized_keys), dedicated locked `mtc-watch` account,
root-run backup orchestrator with 0700 staging + `runuser` create/verify +
symlink (`-L`) refusals + atomic same-FS `mv` promote + `chattr +i`, root-owned
`status.json` written tmp-then-rename with the watcher ACL applied pre-rename on
both success and failure paths, `env -i` on every menu entry and both `runuser`
calls, absolute executable paths, `umask 077` / `UMask=0077`, `flock -n` overlap
guard, prune only after full success and never the manifest-named bundle,
provisioning `sshd -t`-before-reload with held-session rollback, client sending
check IDs only with the server menu authoritative.

## 3. Supplemental adversarial review

### GLM-5.2 (Z.AI route) — VERDICT: REQUEST_CHANGES (pre-application), 14 findings

Full text preserved verbatim:
`PHASE_WATCH_V3_GLM52_SUPPLEMENTAL_VERDICT_2026-08-18.md`. Escape-path core
judged sound: "no path to a shell or beyond the read-only surface". Blocking
findings F1, F3, F4, F11, F12, F13.

### Lead's own independent findings (raised before GLM returned)

- **PS 5.1 incompatibility** (= GLM F11): `collect_kvm2_evidence_v3.ps1:81` uses
  `ProcessStartInfo.ArgumentList` — absent from .NET Framework/PowerShell 5.1;
  probe on this host: `.Add()` throws, and **pwsh is not installed here**. The
  LIVE collector `C:\LAB\HERMES_WATCH\collect_kvm2_evidence.ps1:126,141` carries
  the same pattern; every recorded verification ran fixture/probe paths that
  never reach the ssh spawn, which is why it never surfaced. Fail-closed (crash
  before any ssh), but the client is non-functional on its declared platform.
- **T1 judge substring** (= part of GLM F12): `'active'` matches `inactive`.
- T9 automated coverage is absent (manual by design, documented).
- B-matrix is a manual contract, not an executable falsification suite (= GLM F13).

### Gemini read-only cross-check — BLOCKED (environmental), three fail-closed attempts

The launcher's filesystem watcher aborted on (1,2) `.impeccable\hook.cache.json`
churn from the two concurrently-running Claude sessions' hooks, (3) this
cleanup's own worktree-registry mutations. The guard worked exactly as designed;
the route is unusable while the repo hosts concurrent sessions. No Gemini
verdict exists; nothing was substituted for it.

## 4. Lead reproduction of GLM findings (D026 discipline — no unreproduced claim recorded as fact)

| # | Claim | Lead status |
|---|---|---|
| F3 | empty-bundle guard dead (`du -sb` dir ≥ 4096 on ext4) + hash-of-zero-files looks valid | **CONFIRMED**: `find -print0\|sort -z\|xargs -0 sha256sum\|sha256sum` on an empty set executes and emits a valid hash (reproduced live); `du -sb` = 4096 for an empty dir is standard ext4 (target KVM2) semantics — on this Windows probe it returned 0, so the guard's deadness is target-platform-confirmed, environment caveat recorded |
| F4 | no `pipefail`/hash-nonempty/recompute — partial pipeline failure yields PASS manifest | CONFIRMED from bytes (`set -u` only, line 6; no check on `$HASH`) |
| F11 | client dead on PS 5.1 live path | CONFIRMED by direct probe (see §3) |
| F12 | T2/T3/T4/T10 judges false-pass on "Connection refused"; T1 on "inactive"; T5 false-FAILS on a correct server (`-L` binds locally without channel use) | CONFIRMED from bytes + OpenSSH semantics; T8 anchors correctly, proving the tighter form was available |
| F1 | no on-host hash/LF verification step in provisioning; CRLF checkout breaks `#!/bin/sh` | CONFIRMED from bytes (no `sha256sum -c` anywhere; working tree is CRLF) |
| F2 | unterminated `Match` block can leak into later drop-ins | CONFIRMED (sshd Match extends to next Match/EOF across included files); fix `Match all` terminator |
| F13 | B1–B6 not executable as frozen; B4/B5 induction impossible without patching the frozen orchestrator | CONFIRMED from bytes |
| F5–F10, F14, nits | design-vs-bytes divergences, 0755/0444 world-readable bundles vs "nothing else" claim, `.staging` accumulation, `fail_manifest` blanking `last_success_utc`, check1 exit masking, flock-hang blackout, coverage gaps | CONFIRMED from bytes on read-through; none contradicts §2's presence checks — they are quality/semantics defects inside present mechanisms |

## 5. T0 pair capacity — probed live (not assumed from snapshots)

| Route | Probe result (2026-08-18 ~16:40 +03) |
|---|---|
| `claude-opus-5` xhigh (Pro) | "weekly limit — resets Aug 19, 11pm Europe/Chisinau" |
| Codex `secondary` `gpt-5.6-sol` | usage limit — retry Aug 22, 20:09 |
| Codex `fourth` `gpt-5.6-sol` | usage limit — retry Aug 20, 10:20 |
| Codex `free` (ChatGPT Pro) / Claude MAX | deliberately NOT probed/spent — owner-protected |

**The exact pre-application T0 pair cannot be dispatched now.** Additionally,
with a reproduced REQUEST_CHANGES-level supplemental verdict on the frozen
bytes, dispatching the capped T0 pair before repair would spend one of the three
T0 rounds on defects already known — wasteful even if capacity existed.

## 6. Disposition and queue

1. Findings recorded here; **frozen artifacts left byte-identical** (change
   control: any byte change voids the freeze → repair must be a deliberate
   re-freeze round, not a silent patch).
2. Required repair set (F1–F14 + Lead findings; GLM's full text is committed at
   `PHASE_WATCH_V3_GLM52_SUPPLEMENTAL_VERDICT_2026-08-18.md`)
   routes to the counterpart flagship (Codex) per the two-tier model — first
   capacity: `fourth` ~2026-08-20 10:20. After repair: owner re-freeze approval →
   THEN the fresh exact T0 pair (`claude-opus-5` xhigh + `gpt-5.6-sol` xhigh),
   whose first capacity is ~2026-08-19 23:00 (Claude side) / see above (Codex).
3. Nothing is scheduled automatically — no automation exists to dispatch this;
   next session picks it up from `NEXT_STEPS.md`.

## GLM routing record (required)

```
Classification      : Tier 4 — adversarial security/architecture review (forced-command
                      SSH confinement + backup integrity contract, host-touching design)
Protected           : yes (deployment/host security surface) — review-only, no writes
Model + provider    : GLM-5.2 via Z.AI Coding Plan (glm.ps1)
Cheaper-model rationale : Tier 4 explicitly required for adversarial safety review;
                      GLM-4.7 reserved for the routine classification task
Exact paths         : MTC_COMMAND_CENTER/11_TRIAGE/PHASE_WATCH_FC_FROZEN_V3/ + design doc,
                      read-only in clean control worktree
Context/tool budget : file reads + hashing only; ~45 min session
Fallback            : GLM-5.3
External API credits: no
```
