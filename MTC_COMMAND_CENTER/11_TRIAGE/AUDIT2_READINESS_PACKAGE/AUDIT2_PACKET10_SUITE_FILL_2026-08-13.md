# Audit 2 Packet 10 — mandated-suite fill (2026-08-13)

**Status: PARTIALLY FILLED.** The *scope* of P10-10 is closed by owner decision. The
*command string*, the *execution record* (P10-11) and the *accepted anomaly register*
(P10-12) are not. This document records a freeze-prep command **template** and the
reconciliation still owed; it is not a baseline and it is not an execution record.

**Executed in this session: nothing.** No test, no pytest collection, no lint, no compile,
no host, network, service or credential action, and no Git mutation. No suite run of any
kind was performed, and no count, exit code, duration, failure identity or anomaly set is
stated anywhere below.

Tier: T2 documentation. Repository HEAD before this document was written: `c2861d88`,
branch `feature/donchian-crypto-ladder`.

---

## 1. The owner decision this fills

`WPI_OWNER_DECISIONS_2026-08-13.md:31-37` (2026-08-13 ~10:00, owner answer `3. ok`):

> P10-10 — mandated suite **DECIDED: full Bridge suite at the frozen SHA** … with the
> exact command settled during freeze prep after reconciling README/cwd/ACL/plugin
> requirements … Historical baselines ("1359 passed" etc.) are explicitly non-referent.

This is **Option A** of `AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:243-286`, and it is the
option that document recommended (`:432-455`). What the owner decided is the *contract* —
which surface the two flagships are bound to execute. The owner was explicitly **not** asked
for and did not supply any count (`AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:459-475`).

Consequences carried forward unchanged:

- Every historical baseline is **non-referent**. `1359` was old-SHA Windows evidence at
  `ebada020`, superseded by `1360` at `2ce41e34`; the two `test_order_state.py` gc-referent
  failures were dated Linux history, and current product memory names a *different* later
  two-failure set (`AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:106-121`, H13/H14 at `:103-104`).
  `AUDIT2_AUDITOR_SESSION_INPUTS.md:84-87` forbids repeating either as a current baseline.
- Option A's stated cost stands: it proves nothing about test files outside
  `IBKR_PAPER_BRIDGE`, and **if the freeze diff reaches outside the Bridge, Option A must be
  revisited rather than stretched** (`AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:451-455`).

---

## 2. Freeze-prep command template — NOT an executed baseline

The following is the invocation the freeze-prep reconciliation is to **confirm and then
freeze**. It is a template: `<FROZEN_WORKTREE>` is unallocated because the pre-WP-A
checkpoint does not exist yet (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:119-120`).

```text
CWD                 : <FROZEN_WORKTREE>\IBKR_PAPER_BRIDGE
process environment : PYTHONUTF8=1
                      PYTHONIOENCODING=utf-8
command             : python -m pytest -q -p no:cacheprovider -p no:randomly --ignore=TSP1009B.pytest_tmp_s1r1
```

Both environment variables are set as **process environment for the run**, recorded before
the run, not reconstructed after it (`AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:377-384`).

### Why each element is present

| Element | Basis |
|---|---|
| CWD `…\IBKR_PAPER_BRIDGE` | Product memory requires CWD `IBKR_PAPER_BRIDGE` (`PROJECT_MEMORY.md:70-72`); the only historical invocations written out with their CWD used it (`GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md:84-88`). |
| `PYTHONUTF8=1` | The documented product command sets it (`IBKR_PAPER_BRIDGE\README.md:44`). |
| `PYTHONIOENCODING=utf-8` | Companion encoding pin so captured stdout/stderr bytes are stable for the byte-exact retention P10-11 demands (`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:63`). Not inherited from any historical record. |
| `-p no:cacheprovider` | Historical practice already pinned this plugin control in the invocation line (`GATE_A_INTEGRATION_FLAGSHIP_AUDITS_EBADA020_2026-08-08.md:68-70`). |
| `-p no:randomly` | The `no:randomly`-class control the options document lists as an open preflight question (`AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:252-258`); pinned so ordering cannot vary between the two flagship runs and the rerun. |
| `--ignore=TSP1009B.pytest_tmp_s1r1` | Product memory: that directory is ACL-locked and plain `pytest` aborts collection with `PermissionError` (`PROJECT_MEMORY.md:70-72`). |

### The README-versus-history reconciliation, stated openly

Three descriptions of "the Bridge suite" disagree, and the disagreement is **not yet
resolved by observation** (`AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:173-182`):

1. **README root form.** `IBKR_PAPER_BRIDGE\README.md:43-46` runs from the repository root
   (`cd C:\LAB\Tradingview_LAB_CLEAN`) with a **path argument** (`python -m pytest
   IBKR_PAPER_BRIDGE\tests -q`) and **no ignore flag**. Root CWD changes the resolved
   rootdir, and therefore changes whether the ACL-locked directory is under collection at all.
2. **Historical product-CWD form.** The audit runs of record used CWD
   `…\IBKR_PAPER_BRIDGE` with `python -m pytest -q`, **no ignore flag**, and succeeded
   (`GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md:84-88`), later with the
   `-p no:cacheprovider` control (`GATE_A_INTEGRATION_FLAGSHIP_AUDITS_EBADA020_2026-08-08.md:68-70`).
3. **Current product memory.** CWD `IBKR_PAPER_BRIDGE` **plus**
   `--ignore=TSP1009B.pytest_tmp_s1r1`, because plain `pytest` aborts collection with
   `PermissionError` (`PROJECT_MEMORY.md:70-72`).

The template above adopts form 3 (memory) with form 2's plugin discipline, because form 3 is
the only description that is current *and* names the ACL hazard. The likeliest explanation
for the contradiction — that the ACL-locked directory appeared after 2026-08-03 — is a
**hypothesis, not a measurement** (`AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:179-182`),
and the reconciliation is a **bytes-only, no-test preflight** owed at freeze prep. It must
settle, by reading bytes at the frozen SHA: the exact CWD; whether the ignore flag is
required from that CWD or a no-op; whether the two `-p no:` disables are correct for the
plugins actually installed; and every environment pin
(`AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:252-258`).

A collection error or an ACL `PermissionError` is a **STOP**, never a pass and never an
accepted failure (`AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:410-415`;
`AUDIT2_AUDITOR_SESSION_INPUTS.md:102-104`).

---

## 3. P10-10 fields — what is filled and what stays pending

| Field | State |
|---|---|
| Suite **scope** | **FILLED** — full `IBKR_PAPER_BRIDGE` suite, Option A. `WPI_OWNER_DECISIONS_2026-08-13.md:31-37` |
| `MANDATED_COMMAND` | **PENDING** — template in §2; frozen only after the freeze-prep reconciliation, and only with `<FROZEN_WORKTREE>` resolved. |
| `<FROZEN_WORKTREE>` | **PENDING** — the pre-WP-A checkpoint does not exist. `AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:119-120` |
| Frozen SHA | **PENDING** — P10-01, produced by the post-WP-I pre-WP-A freeze. `AUDIT2_HANDOFF_PACKAGE.md:57` |
| Interpreter (absolute path + version) | **PENDING** — must be recorded before the run. `AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:377-384` |
| `EXPECTED_EXIT_CODE` | **PENDING** — observed only. |
| `EXPECTED_PASS_COUNT` | **PENDING** — observed only. |
| `EXPECTED_FAIL_COUNT` | **PENDING** — observed only; `0` is legal **only** if both runs observed empty. `AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:406-409` |
| `EXPECTED_FAILURE_1` / `EXPECTED_FAILURE_2` | **PENDING** — exact node IDs and signatures, observed only. |
| `EXPECTED_SKIP_XFAIL_COUNTS` | **PENDING** — observed only. |
| Anomalies / accepted anomaly set | **PENDING** — P10-12, observed and adjudicated only. |
| `BASELINE_SOURCE` | **PENDING** — must be a path at the frozen SHA, bound by bytes and SHA-256. `AUDIT2_AUDITOR_SESSION_INPUTS.md:99`, `AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:416-418` |

**No count, rc, duration, failure identity or baseline path is stated in this document.**
Writing one would be the Pattern-10 "evidence that cannot fail" defect the kickoff names
directly, by analogy to RP6's `dynamic_targets=0` literal
(`AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:64-80`).

---

## 4. P10-11 and P10-12 remain gated on a real two-run observed anomaly gate

P10-11 (frozen-SHA execution record) and P10-12 (accepted anomaly register) are **not
unblocked by this document.** They open only when the nine-step gate at
`AUDIT2_MANDATED_SUITE_OPTIONS_2026-08-12.md:370-424` is actually executed at the frozen
SHA, under separate authorization. In summary, and unchanged:

1. Freeze SHA, command, CWD, interpreter, dependency lock, every environment and plugin
   control, and platform — **recorded before the run**.
2. Run only under authorization in a clean isolated worktree, one per flagship, with empty
   pre- and post-run `git status --porcelain` (`AUDIT2_AUDITOR_SESSION_INPUTS.md:65-80`).
3. Retain byte-exact stdout, stderr and rc with byte count and SHA-256.
4. Capture terminal counts **and** every `FAILED`/`ERROR`/`SKIP`/`XFAIL`/`XPASS` node ID
   with its signature — identity over count.
5. Adjudicate every non-passing member against a source-linked authority.
6. **Rerun independently and require two-way set equality** between run 1 and run 2.
7. Record an empty set **only** if both runs observed it empty.
8. Inability to evaluate is STOP, never a result.
9. Freeze `BASELINE_SOURCE` by path, bytes and hash at the frozen SHA.

**Nothing in steps 1–9 has been performed, in this session or any prior one.** This document
records the gate; it does not open it.

Ordering is unchanged: the mandated suite is defined and executed at step 13 of the combined
production order, after the pre-WP-A freeze at step 12 and before Audit-2 dispatch at step 15
(`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:119-122`). Packet 9 must be complete and
immutable first (`AUDIT2_FREEZE_PREREQUISITES.md:16-17`).

---

## 5. Effect on the Packet-10 gap count

`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:71` records Packet 10 as 15 components with 3
having no defined producing step (P10-10, P10-11, P10-12).

- **P10-10:** producing step now **defined** — owner-decided scope plus a freeze-prep
  reconciliation that yields the frozen command string. The component is **not yet filled**.
- **P10-11 and P10-12:** producing step now **defined by dependency** (the §4 gate at the
  frozen SHA), but both remain **unproduced and unfillable** until that gate is executed.

The honest current statement is therefore: **three Packet-10 components remain unfilled;
none of the three can be filled from a pre-freeze tree.**
