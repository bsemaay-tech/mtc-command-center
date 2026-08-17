# GATE A — PRE-REGISTRATION ADDENDUM C: re-baseline to `ed3d0534` (2026-08-08)

Amends `GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md`,
`…_ADDENDUM_A_2026-08-02.md` and `…_ADDENDUM_B_2026-08-08.md`. **Written before the rerun, not during
it.**

**Why.** The 2026-08-08 Gate A run passed A-0→A-3 and **failed A-4** because the deploy artifact never
selected the credential-free DISARMED start mode. That is repaired at `ed3d0534` on
`codex/gate-a-disarmed-start-mode`, built directly on accepted candidate `ebada020`. Addendum B's
frozen inputs name the `ebada020` artifact and are therefore superseded, and — critically — **A-4's
expected outcome changes**, so it is re-registered here rather than judged after the fact.

---

## C.1 Frozen inputs — supersede Addendum B §B.1

| Item | Addendum B (superseded) | **Authoritative** |
|---|---|---|
| Release SHA | `ebada020a59edf539f60acfbb3a6bf870c8679e9` | `ed3d053432fb496123ac43bcb7d40cfb64edbb8b` |
| Artifact path | `C:\WPI_ARTIFACTS\ebada020…` | `C:\WPI_ARTIFACTS\ed3d053432fb496123ac43bcb7d40cfb64edbb8b` |
| Manifest SHA-256 | `8FC30864…4700C9` | `8964CC43B802BADA1AD5611E5B445E19B4332C45133AF3E8473A85BB57E7EE4B` |
| Manifest entries | 7,059 | **7,059** (unchanged — no files added or removed) |
| Files on disk | 7,060 | **7,060** |
| Total bytes | 1,033,359,158 | **1,033,359,494** (+336 B — the 6 added lines across 3 files) |
| `origin/master` | `637307e8` | `637307e8`, unchanged |
| Records branch | `feature/donchian-crypto-ladder` | same |

Built once with `package.sh --release-sha ed3d0534… --repo C:\GADISARM --out C:\WPI_ARTIFACTS\ed3d0534…`,
exit 0. The builder refused an earlier attempt with `FATAL: repo HEAD is not the requested release
sha` when pointed at the docs checkout — the dirty/mismatched-worktree ban is structural, and it
fired correctly.

Lead-verified after build: `RELEASE_SHA` matches; manifest hash as above; 7,059 entries / 7,060 files
/ 1,033,359,494 bytes; **0 CR bytes on all five `deploy/linux/*.sh`**; the fix is present in the built
payload at `…/mtc-bridge-first-start.service.template:42`; the steady template does **not** carry it.

## C.2 Host preparation — mandatory before A-0

**The `ebada020` install from the 2026-08-08 run is still on the host.** It was deliberately retained
so the repair could be retested, but A-1 is a *clean-host* precondition and will fail 7 of 8
assertions against it, exactly as the `a1dd5b46…` install did.

Tear it down first, by the same recorded method: stop, unmask, `reset-failed`, remove both unit paths,
`daemon-reload`, then remove `/opt/mtc-bridge`, `/etc/mtc-bridge`, `/var/lib/mtc-bridge`,
`/var/log/mtc-bridge`, `/etc/logrotate.d/mtc-bridge`, and delete the `mtc-bridge` user/group. Preserve
`/etc/mtc-bridge/install_manifest.json` and the unit hash to the home directory first. `rollback.sh`
takes `--to-release-sha` and is **not** an uninstaller — do not reach for it again.

Script: `C:\tmp\gatea_teardown.sh` (already proven, teardown leftovers 0).

## C.3 A-0 through A-3 — unchanged except the constants

A-0's expected values are C.1's. A-1 is unchanged. A-2 is unchanged.

**A-3's expectation is unchanged at `2 failed, 1357 passed, 1 warning`** with the only permitted
failures being the two `test_order_state.py` gc-referents node IDs. The repair adds two assertions
inside two *existing* test functions, so the test count does not move; the Windows floor stays
`1359 passed, 1 warning`, independently reproduced by the Lead at `ed3d0534`
(`1359 passed, 1 warning in 198.90s`).

## C.4 A-4 — the expectation CHANGES, and is registered here in advance

Under Addendum B, A-4 was expected to expose the missing start mode, and it did. **That is now
repaired, so A-4 must be held to its full original standard.**

Method unchanged (Addendum A §A.4): the unit installs masked with `Restart=no`, so A-4 requires
`systemctl unmask` then `systemctl start`.

**A-4 PASSES only if all of the following hold, each evidenced:**

1. The unit reaches and stays `active (running)` — it does **not** exit non-zero.
2. A listener exists on **`127.0.0.1:8790` only**, and on no non-loopback address.
3. `GET /api/status` responds and reports a state that is durably **not** `ARMED`.
4. `POST /api/arm` is **refused by the application** — an HTTP status and body from the bridge itself.
   **`Errno 111 Connection refused` is NOT a refusal** and does not satisfy this; that is what failed
   the previous run.
5. **No broker connection is attempted** — nothing in the journal, in
   `/var/log/mtc-bridge/bridge.err.log`, or in `ss -tnp` for the service.
6. The persisted store still reports `app_state=DISARMED` after the arm attempt, with the state
   version unchanged.
7. The run records **which start mode was actually selected**, read from the running service's
   environment rather than inferred.

**A-4 FAILS if** the service arms, attempts a broker connection, reports an ambiguous state, exits
non-zero, or if any required confirmation above cannot be obtained. A confirmation that cannot be
performed is not a pass — the same principle D025 rule 1 applies to auditors.

**Read `/var/log/mtc-bridge/bridge.err.log`, not just the journal.** The unit sets
`StandardError=append:`, so a Python traceback never reaches `journalctl`. That cost real time on the
previous run.

## C.5 Robustness question A-4 should answer while it is there

`EnvironmentFile=/etc/mtc-bridge/mtc-bridge.env` is declared **after** the `Environment=` lines in the
unit. If a future operator ever placed `MTC_BRIDGE_START_MODE` in that file, systemd's precedence
decides whether the pinned DISARMED mode survives. Record the answer as evidence rather than
assuming it — it determines whether this safety property is robust or merely conventional. This is a
recording obligation, not a pass/fail condition for A-4.

## C.6 A-5 through A-9

Unchanged from the runbook. They were never reached on 2026-08-08. Stop at the first FAIL. Write
`GATE_A_RESULT_2026-08-08B.md` either way, keeping the first run's result document intact.

## C.7 Gate A may not start until `ed3d0534` is accepted

Two flagship audits were dispatched on `ed3d0534` on 2026-08-08 (`gpt-5.6-sol` xhigh in
`C:\GAAUD_DISARM`, `claude-opus-5` xhigh in `C:\GAAUD_DISARM_CLA`, separate worktrees so neither
disturbs the other's suite run). D025 requires both accepting, with no unresolved reproduced required
finding, before the candidate is accepted. **A rebuilt artifact is not acceptance.** If either
flagship returns a required finding, Gate A does not start.
