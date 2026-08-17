# DEFECT 3B — GATE 5 ROUND 1 (2026-08-03)

Both flagship auditors returned non-accepting verdicts on `f1ac2565`. Every finding below was
**independently reproduced by the Lead before being treated as binding** (D025 rule 2).

| Auditor | Model | Verdict |
|---|---|---|
| Flagship 1 | `gpt-5.6-sol` xhigh | **BLOCK** |
| Flagship 2 | `claude-opus-5` xhigh | **REQUEST_CHANGES** |
| Supplemental | GLM-5.2 | PASS-WITH-NITS — **no acceptance weight**, see §4 |
| Supplemental | `deepseek-v4-flash` | not dispatched |

Repair round 1 of a maximum 3 dispatched. The product fix itself is **correct and retained**.

## 1. BLOCKING — the fix makes the tool accept a crashed writer

`_connect_readonly`'s docstring promises that a hot `-wal` with no `-shm` *"fails closed here …
**it is never done silently by this tool**."*

It is now done silently. The check only fires after SQLite raises. In a writable directory SQLite
does not raise — it **creates the `-shm`** and opens the database. The new schema read triggers that
before `source_snapshot_before`, so the materialised SHM lands in the arrival→before window, where
SHM-only change is deliberately ignored, and nothing is reported.

**Lead reproduction — Ubuntu 24.04 / Python 3.12.3 / SQLite 3.45.1, real `Store`-seeded bridge
database, real crashed-writer state (`db` + non-empty `-wal`, no `-shm`):**

```
UNFIXED tool (master 637307e8) : RC=2  verdict INVALID    bundle written: False
FIXED tool   (f1ac2565)        : RC=0  verdict CAPTURED   bundle written: True
                                 shm created by tool: True  (both cases)
```

**This is a regression introduced by the commit**, not pre-existing: the unfixed tool refuses the
same input on the same platform. The Stage E cutover tool would produce a bundle from a database
whose writer died mid-transaction and report it `CAPTURED`.

The branch has **zero test coverage**, before and after the commit — which is why it broke unnoticed.

## 2. The regression test was vacuous — proven, not argued

`claude-opus-5` replaced the fix with `conn.execute("SELECT 2").fetchone()` — touches no table,
leaves the Linux defect fully intact — and **the new test passed green**.

The test discriminated on the string literal `"SELECT 1"`, not on whether the main database was
read. Failing on the old literal is necessary, not sufficient. On a protected surface whose defect
cannot reproduce on the dev platform, that test was the only durable guard.

Both auditors reached this independently.

## 3. What both auditors confirmed is correct — retained

- The one-line product fix repairs the defect. Verified on two SQLite versions.
- **The drift detector is not weakened in any ordinary class.** `_capture_changed_components` is
  byte-identical to the parent; arrival→before catches db/wal, before→after catches all three with
  zero carve-outs. Enumerated class-by-class by both auditors.
- `.fetchone()` is load-bearing, not decoration — without it a read transaction could linger past
  `_connect_readonly`.
- The concurrent-writer test is deterministic and non-vacuous: 20/20 and 10/10 clean repeats across
  two independent audits.

## 4. Roster notes — two process defects this round exposed

**The Linux access grant did not take effect.** The owner granted auditors read-only SSH to
`GATEA-STAGING` specifically to satisfy D025 rule 1. The Codex sandbox denied outbound network
*before* SSH authentication (`connect to host … port 22: Permission denied`), so rule 1 bit anyway
and contributed to the BLOCK. Future audit dispatches must enable network access explicitly. No key
value was ever placed in a prompt — only the local key path, per the owner's standing instruction.

**GLM-5.2 executed nothing.** The route itself is repaired and returned a substantive report — it
independently confirmed the root-cause mechanism and located a relevant existing carve-out test —
but it ran no tests and cited the Lead's numbers back. Under D025 rule 1 that is non-acceptance
whatever label it prints. **Second occurrence of this exact failure mode.**

**A dispatch was lost to a role misread.** The first repair dispatch on the build branch read
`AGENTS.md` §TWO-TIER's "Codex is lead" line, tried to delegate to Claude Code CLI, timed out and
blocked without touching a file. Implementer dispatches now carry an explicit role-override header
naming the handoff's actor assignment. Not counted as a repair round — no implementation occurred.

## 5. Corrections to earlier Lead records

- The Windows half of the 3b mechanism was wrong; corrected in `DEFECT_3B_ROOT_CAUSE_2026-08-03.md`
  (`d9b00b37`). The original probe measured `connect()` and `SELECT 1` together.
- The 3b audit prompt asserted an existing test covers the hot-WAL fail-closed path. There is none.
  Lead error, corrected here.
- `claude-opus-5` offered a "positive finding" that the fix makes the previously-dead `BundleError`
  branch reachable. **The opposite is true**, as §1 shows: it makes the branch unreachable by
  satisfying the open. Recorded because it was explicitly flagged as reasoning rather than evidence,
  and measurement refuted it.

## 6. Safety

Read-only diagnosis throughout. No ARM, no order, no broker connection, no TESTNET, no mainnet, no
wallet action, no credential value. No service started. No installer, verifier, rollback, systemd or
firewall command run. Work confined to a throwaway copy on the disposable staging VM; the `~/payload`
and `~/fixpay` evidence trees were restored and re-verified against the manifest. KVM2 untouched;
`KVM2-Ubuntu-2404-Staging` remains powered off and quarantined.

## 7. Codex takeover — `df00634f` evidence and three-result hard stop

The temporary Codex Lead independently inspected frozen candidate
`df00634fc2e5fb19cddb34a6ad16d9764c4779a4` and reproduced strong product evidence on
`GATEA-STAGING`:

- focused `tests/test_wal_state_bundle.py`: **45 passed**
- real crashed-writer source: non-empty WAL, no SHM; rejected with `connect_calls=0`, no created
  SHM, no bundle database, and no manifest
- genuine concurrent-writer detector: **10/10** separate passes
- exact `SELECT 2` mutation: both attachment guards RED; whole file restored **25 failed,
  20 passed**
- complete locked Bridge suite: **2 failed, 1308 passed, 1 warning**; only the two known
  Python-3.12 `order_state` GC-referent failures remained
- bundle `SCHEMA_VERSION`, `MANIFEST_NAME`, and `BUNDLE_DB_NAME` unchanged

That evidence does **not** override D025's executing-auditor requirement:

1. The first takeover GLM session printed PASS, but the Lead classified it **BLOCK** because it
   created a new venv instead of using the locked interpreter, omitted the 1,310-test floor and raw
   command ledger, used `SELECT 1` instead of the mandated `SELECT 2`, and did not prove five
   independent concurrent repetitions.
2. A fresh GLM retry returned explicit **BLOCK** because the Windows argument route truncated the
   quoted mutation instruction before the model received it. It completed focused/hot-WAL/concurrent
   checks but could not execute D026 or the full floor as specified.
3. Counting the documented `f1ac2565` non-accepting Gate-5 result plus these two non-accepting
   executing-audit attempts reaches the branch's maximum-three-result ceiling.

**HARD STOP:** no fourth 3b audit or repair round was launched. Candidate `df00634f` remains pushed,
clean, and **not accepted**. Integration and Gate A rebuild remain blocked on 3b. Reopening requires
an owner-directed new cycle or the required retrospective flagship path; the temporary Lead did not
silently waive the ceiling.

Safety remained read-only and DISARMED. All exact Lead/GLM scratch roots were validated and removed.
No service, deployment, credential, broker, ARM, order, TESTNET, mainnet, wallet, KVM2, or economic
action occurred.
