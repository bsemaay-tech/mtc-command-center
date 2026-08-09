I have read all five inputs. This is a read-only audit — I have touched no file and will not. Below is the structured report.

---

# AUDIT REPORT — WP-I preregistration DRAFT (round 1)
**Auditor:** GLM-5.2 (Auditor 4) · **Mode:** read-only (T2) · **Files touched:** 0
**Inputs reviewed:** the five files named in the task; nothing else.

## Overall verdict
The draft is sound. It correctly internalizes the `B3-GAP-ENV` lesson (terminal-`stat` vs. path-prefix), keeps placeholder discipline clean, and leaves Group C entirely non-executable. Template parity with the Stage 2 rigor template is strong. **One substantive feasibility finding** (B1, Q1) and a handful of minor parity/wording notes. No misclassification forces a row out of the run plan into `DEFER-ROOT-SIDE` on the B3-GAP-ENV criterion, but one INCLUDE half rests on an unverified premise its own divergence table cannot catch safely.

---

## Q1 — Feasibility soundness of every INCLUDE-READ-ONLY half

I walked each INCLUDE-READ-ONLY half against POSIX permission semantics and the recorded modes/owners, applying the B3-GAP-ENV test ruthlessly (stats/reads inside a root-only dir, reads a root-only file, or needs a privileged syscall ⇒ DEFER).

| Check (TSV row) | INCLUDE-READ-ONLY scope claimed | Verdict | Reason |
|---|---|---|---|
| **B1** (line 13) | `verify_lock.py --check-installed`; `<venv>/bin/python -V` | **"yes" is over-confident — see finding F1** | Trees are `0555` (r-x for other ⇒ traversable+readable), and the burned-B3 walk (M3) proves traverse/read. **But executing the venv interpreter needs the file's execute bit, which no Input records.** Not a DEFER case (exec is not a privileged syscall; root-side is not the fix), but the "yes" is under-supported. |
| **B1a** digest half (line 14) | `sha256sum` of installed `requirements.lock` | **INCLUDE — sound** | File sits inside the `0555` release tree ⇒ world-readable. Manifest half correctly DEFER (`/etc/mtc-bridge` `0750 root:root`, manifest `0640 root:root`). Split is exactly right. |
| **B2** (line 15) | `systemctl is-active/show -p/cat`; read/`sha256sum` the `0644` fragment | **INCLUDE — sound** | polkit gates *jobs*, not property reads; fragment is `0644`. `/etc/systemd/system` world-searchability is a standard-default assumption, low risk. |
| **B3** feasible half (line 16) | walks of both `0555` trees + `find -perm /222` + **terminal** `stat` of the three metadata dirs | **INCLUDE — sound; this is the crux repair and it is correct** | `stat /etc/mtc-bridge` needs search only on `/` and `/etc` (world-searchable), returns the dir's own mode/owner without entering it. `stat /etc/mtc-bridge/<child>` needs search on the dir itself ⇒ EACCES. The terminal-vs-prefix line is drawn exactly where B3-GAP-ENV says it must be. Children correctly DEFER. |
| **B4** (line 17) | `systemctl show -p <named>` | **INCLUDE — sound** | Property reads unprivileged; `-p` selection guard prevents banking unnamed env. |
| **B5** (line 18) | loopback `GET /api/status` | **INCLUDE — sound** | Loopback TCP connect is not privilege-gated. Auth-token/curl-presence unknowns are M4, fail-closed to STOP. |
| **B6** listener half (line 19) | `ss -ltn` (no `-p`) + operator-side external reprobe | **INCLUDE — sound** | `/proc/net/tcp{,6}` world-readable; `-p` (process map) correctly excluded; `ufw status` correctly DEFER. |

**Misclassifications forcing DEFER-ROOT-SIDE on the B3-GAP-ENV criterion: none.** Every INCLUDE half stays inside `0555` trees, world-readable files, unprivileged syscalls, or terminal stats via world-searchable parents. Every privileged half is already DEFER.

### Finding F1 (substantive) — B1's "yes" rests on an unverified interpreter execute-bit, and rows 18/19 cannot fail safely on it
- **Premise gap.** B1's `unpriv_why` (TSV line 13) argues only traverse+read from the `0555` *root* and the burned-B3 walk. Neither establishes that `<venv>/bin/python` has the execute bit for "other". `SELF_QA.md` M4-9 (lines 304-306) admits per-file modes inside the trees are unrecorded — **but links that gap only to the write-bit sweep (row 12), never to interpreter execution (rows 18/19).** The connection is missed.
- **Why it bites (the sharp part).** If the interpreter lacks the "other" x bit, `<venv>/bin/python -V` fails with EACCES/126. Draft §8.2 row 18 (line 351) has only `B1_FAIL reason=interpreter_version observed=<v> expected=3.12.*` — **no STOP-on-EACCES case.** Row 19 (line 352) has a `metadata_unreadable` STOP, but that fires only *after* python is already running; an interpreter that cannot start never reaches metadata enumeration. The binding ordering rule (lines 359-366) guards `.dist-info` reads, not the exec itself. **Net effect: an exec-permission denial would be rendered as a version/parity B1_FAIL — a false finding against a correct host. That is precisely the B3-GAP-ENV failure shape ("an unreachable path read as a finding") arriving through a different door — the exact regression the whole draft exists to prevent.**
- **Correct characterization (not a DEFER misclassification).** This is *not* B3-GAP-ENV-class: executing a venv binary is no privileged syscall and reads no root-only path, so B1 must stay in the run plan, not move to DEFER-ROOT-SIDE (root-side is not the remediation channel; the file mode is).
- **Recommended fix for the successor (non-binding):** either (a) downgrade B1 to `partial` with a named risk, or (b) add a P0 preflight row asserting the venv interpreter is executable by `gatea` (e.g. `test -x`/invoke `--version`), and (c) extend rows 18/19 with an explicit `B1_STOP reason=interpreter_not_executable path=<p>` divergence so exec denial can never read as a parity FAIL. This mirrors how row 14 already guards row 19.

---

## Q2 — Template parity with the Stage 2 rigor template

Every load-bearing section is present. Mapping (template § → draft §):

| Load-bearing element | Template | Draft | Status |
|---|---|---|---|
| One-use RUNIDs + burn rule | §1 | §1 | ✅ Present; cites burned `…-B3` as precedent |
| Preregistered inputs | §2 | §2 | ✅ Present; `<PIN-BEFORE-DISPATCH>` for un-pinned values |
| Block SHA-256 table | §3 | §3 | ✅ Present; reused blocks at recorded digests, new blocks PIN-at-Stage-1 |
| Support-script hashes | §4 | §4 | ✅ Present; runner re-pinned (op list changed) |
| Pinned fail-closed argv | §5 | §5 | ✅ Identical ssh-option discipline + scp colon guard |
| Operator-side evidence contract | §6 | §6 | ✅ Present; create-once record root, `exec>$EV_LOG` rationale carried + B3 example |
| Closing/binding (double-pass, remote-vs-local) | §7 | §7 | ✅ Present; ops 07/08/11/12 |
| Per-check expectation table + exact predicted first divergence | §8 | §8.1/§8.2 | ✅ **Stronger** — 29 rows (5 P0 + 24 RO) vs template's 7 |
| What is deliberately NOT preregistered | §9 | §9 | ✅ Present; C1-C5 + DEFER list |
| (template §10 = disposition of preserved partial files) | §10 | **§10 repurposed → RPD-VERIFY** | ⚠️ See note N1 |
| Immutability rules | §11 | §11 | ✅ Present + 2 WP-I additions (P0 identity; pin-from-record-only) |
| Safety state | §12 | §12 | ✅ Present, itemized |

**Appropriately deferred, not gaps (because this is a draft):** first-FAIL *demonstration* and `rp0_require_safe_component` *demonstration* are stated as obligations on the successor (§1, §5) rather than shown — correct, since no runner/blocks exist yet.

**Note N1 (minor parity).** The template's §10 dispositioned five reused/partial scripts with a per-file "reviewed, kept byte-identical, rationale" table. The draft §4 reuses `remote_setup.sh` / `remote_extract_verify.sh` / `remote_close_tree.sh` at identical digests but drops the per-script review rationale (it instead repurposes §10 for the new RPD-VERIFY pattern, which is a necessary WP-I addition). Risk is low (byte-identical to already-accepted scripts), but a one-line "unchanged contract, kept byte-identical" per reused script would mirror the template's discipline.

**No load-bearing section is missing.** The only "weaker" points are N1 above and the wording note N2 below.

---

## Q3 — Placeholder discipline

**Clean.** No concrete one-use RUNID, date-stamped unit id, or collision-prone record-root path is minted.

- RUNIDs: `<ALLOCATE-AT-DISPATCH>-P0` / `-RO` (§1, line 72). Unit id: `<ALLOCATE-AT-DISPATCH>` (line 5). `REMOTE_BASE`: `/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>` (line 81). Record root: `C:\WPI_ARTIFACTS\WPI_TRANSPORT_<ALLOCATE-AT-DISPATCH>` (§6, line 256). All placeholders. ✅
- The two existing roots (`…WPLP2_TRANSPORT_WPLP2-…-8dc78f08` and `-R45B`) are **cited as collision-avoidance targets** (§1 lines 99-101, §6 line 259), not minted — correct. ✅
- The burned `WPLP2-…-B3` RUNID (§1 line 68) is cited as burn-rule precedent, not allocated. ✅
- Un-pinned values use `<PIN-BEFORE-DISPATCH: …>` with the cited source record and a named risk (`WPI_UNIT_FRAGMENT_SHA256` R1 line 118; `WPI_LOG_DIR` R2 line 123). New-block hashes use `<PIN-AT-STAGE-1>` (§3/§4). ✅
- Concrete values that *are* present (candidate SHA, lock SHA, reused-block digests, byte sizes) are preregistered inputs/accepted artifacts, not minted identifiers. ✅

**No placeholder violation found.**

---

## Q4 — Group C (no mutating check preregistered executable)

**Confirmed: no Group C check has any executable form in the draft; each is in §9 with its blocker.**

- §9 (lines 409-440): "Group C — mutating checks. No block, no command, no argv, no conditional branch," then C1-C5 each with authority+budget blocker **and** a command-gap/unmet-prerequisite blocker (C1 no dangling-state verifier; C2 undefined A/B predicate; C3 no `restore` subcommand; C4 absent prior release; C5 no broker in DISARMED mode). ✅
- Block table §3: only RP0-LIB, RP0-BOOTSTRAP (reused), RP6-P0, RP7-WPI-RO (new). **No C blocks travel** — strictly stronger than the template, which carried frozen-but-unexecuted C blocks. ✅
- Op table §5 (ops 01-12): no C reference; op 04/05 = P0/RO wrappers only. ✅
- §8.2 rows 1-24: B2/B4/B3s/B1a/B1/B5/B6 only — no C rows. ✅
- §12 (line 558): "C1-C5 execution: none, and no executable form of any of them exists in this draft." ✅
- `RP1-B3.sh` (the infeasible B3 block) is explicitly excluded from the kit (§3 lines 160-167); B3 is re-scoped into the new `RP7-WPI-RO.sh`, not executed via the old block. ✅
- Permitted host writes are confined to the run's own create-once tree under `/home/gatea/` (op 01); op 06 is a payload-less TCP probe (acknowledged host contact, not a mutation). Neither is a Group C mutation. ✅

**No mutating check is preregistered executable.**

---

## Additional observations (minor)

- **N2 (wording, §8 intro vs R5).** §8 intro (line 302) states "exactly one loopback listener `127.0.0.1:8790`." Named risk R5 (lines 382-387) then clarifies this means *one bridge listener on 8790* (sshd:22 is necessarily also listening). The intro phrasing literally overstates ("exactly one loopback listener" is false while sshd is up). R5 resolves it, but the successor should tighten the intro to "exactly one bridge listener on 8790" so the §8 preamble and R5 do not contradict on a careless read.
- **N3 (residual assumption, recorded).** The terminal-stat argument for `WPI_STATE_DIR`/`WPI_LOG_DIR` (§10.1 lines 480-481, §8.2 row 15) assumes `/var/lib` and the log parent are world-searchable and that `gatea` is not in the state/log group. These are unverified (SELF_QA M4-4) but **safe if wrong**: an EACCES there surfaces as `B3_STOP` (RP0 fail-closed), never a false pass. Acceptable; flag only for completeness.
- **B3 corroboration cite (TSV line 16 / SELF_QA Q3).** `b3.log` is cited as *corroboration, not closure*, and the `…-B3` RUNID is correctly treated as burned (a STOP never re-read as PASS). Sound; the draft avoids the bookkeeping error of promoting a STOP into closure.
- **No git/host contact.** §12's claim of zero host contact and zero repo writes outside `WPI_PREREG_DRAFT_ROUND1` is internally consistent with everything else in the unit.

---

## Summary of actionable items for the successor (non-binding)
1. **(F1, must-fix before dispatch)** Close the B1 interpreter-exec gap: add a STOP-on-EACCES divergence to §8.2 rows 18/19 (and/or a P0 preflight asserting the venv python is executable by `gatea`), and have `SELF_QA.md` connect M4-9's "per-file modes unrecorded" premise to interpreter execution, not only to the write-bit sweep. B1 stays INCLUDE — it is not a DEFER case.
2. **(N1)** Add a one-line "kept byte-identical, unchanged contract" disposition per reused support script to match template §10 discipline.
3. **(N2)** Tighten the §8 intro listener wording to "one bridge listener on 8790."
4. **(R1/R2)** The two `<PIN-BEFORE-DISPATCH>` values (`WPI_UNIT_FRAGMENT_SHA256`, `WPI_LOG_DIR`) remain dispatch blockers as the draft already states — no action beyond filling them from the cited records at dispatch.

No file was created, modified, or deleted. Audit complete.
