I have all six input files. Before writing the report, let me note a key cross-check I want to be precise about: the hash bindings that tie the transport evidence together (these are the crux of verifiability). I've confirmed them from `EVIDENCE_INDEX.md`:

- `RP0-LIB.sh` = `4a404d7b…` (18968 B) — matches the RR3-1 correction in the acceptance record and the draft §2.
- B3: `b3.log` = `079d6ac9…` (1784 B), digest-set `b25612df…` (03_TRANSPORT).
- R45B: `r45b.log` = `00078e7e…` (4521 B), digest-set `1f74d69a…` (05_TRANSPORT_R45B).
- RUNID ledger: `-B3` BURNED, `-R45` BURNED (never allocated), `-R45B` CONSUMED (PASS).
- Operator records present for 03_TRANSPORT ops 01–06, 08–12 (no `07` — it was skipped) and 05_TRANSPORT_R45B ops 01–04.

Internal consistency across the three staging files + EVIDENCE_INDEX is high. Now the report.

---

# Audit 2 evidence checklist — T2 review (auditor 4 / GLM-5.2, 2026-08-09)

Read-only. No repository file was read outside the six inputs named in the task; none was modified.

## Verdict (3 bullets)

- **The draft is materially stale.** It was compiled before tonight's Stage 3 (B3 STOP) and Stage 3B (R4-5 PASS) and (a) still lists **R4-5 as BLOCKED** (`AUDIT2_EVIDENCE_CHECKLIST_DRAFT_2026-08-09.md` §2, line 39-41), and (b) carries **no slot at all** for the transport-evidence class — operator records, remote/local digest-set bindings, burned-RUNID accounting, preregistration-before-invocation ordering, and first-FAIL sequencing — which is now the largest body of banked evidence in the unit (`EVIDENCE_INDEX.md` §03_TRANSPORT, §05_TRANSPORT_R45B, §RUNID ledger).
- **Coverage of the draft's own items is mostly PENDING** (Audit 2 has not run; the freeze SHA is not yet cut), with a small set **BANKED** (block-digest table, candidate identity/hashes, R4-5 RED/GREEN, authorization + hard exclusions) and one item now **WRONG** (the R4-5 BLOCKED line). One new BLOCKED-UPSTREAM item (B3 / `B3-GAP-ENV`) is unrepresented.
- **Tonight's evidence is self-verifying and internally consistent** (hashes bind cleanly across `EVIDENCE_INDEX.md`, both transport records, and the RUNID ledger). The single largest verifiability risk is that the actual evidence bytes (`b3.log`, `r45b.log`) are **git-excluded** (`STAGE3_TRANSPORT_RECORD.md` lines 48-51; `STAGE3B_TRANSPORT_RECORD.md` lines 46-49) and are therefore provable on-repo **only** via the digest-set bindings — which the checklist does not tell auditors to check.

---

## 1. Coverage (BANKED / PENDING / BLOCKED-UPSTREAM)

Paths are repo-relative. "Draft §x" = `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_EVIDENCE_CHECKLIST_DRAFT_2026-08-09.md`. `IDX` = `…/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/EVIDENCE_INDEX.md`.

| Draft item | State | Banked evidence / reason |
|---|---|---|
| §1 Exact frozen checkpoint commit SHA (after WP-L P2 + WP-I close, before WP-A) | **PENDING** | Cut at freeze time (D2 sequencing). The candidate commit `2ce41e34…321b` cited in `STAGE3_TRANSPORT_RECORD.md` / `STAGE3B_TRANSPORT_RECORD.md` is the *product* candidate, not the audit freeze SHA. |
| §1 Frozen candidate identity + artifact/manifest hashes (A1/A2) | **BANKED** (restatable) | `IDX §02_PREREG`: `CANDIDATE_RELEASE_SHA256SUMS` (`edb0fd34…`, 1181804 B), `CANDIDATE_RELEASE_DERIVATION.md` (`32b68bcd…`), `PREREG_SHA256SUMS.txt` (`a48730e1…`); `IDX §01_RUNKIT/SOURCE_IDENTITY.txt` (`10110da1…`). |
| §1 Bits unchanged since Gate-A `5af8178b`, or exact diff | **PENDING** (verifiable) | Recompute `CANDIDATE_RELEASE_SHA256SUMS` at the freeze SHA and diff vs the `5af8178b` record. The sums file is banked; the statement/diff is produced at freeze. |
| §2 Final accepted proposals doc + §8.1 block-digest table (bash -n / py_compile) | **BANKED** | `WPL_P2_PROPOSALS_LEAD_ACCEPTANCE_2026-08-09.md` (ACCEPTED; RR3-1 → RP0-LIB `4a404d7b…` / 370 lines). `IDX §01_RUNKIT` recomputes all block hashes incl. `RP0-LIB.sh`=`4a404d7b90d8…` (18968 B), `BLOCK_IDENTITIES.tsv` (`68e833aa…`); `syntax_validation.txt` (`e188cd85…`) banks syntax checks. |
| §2 RED/GREEN for every closed falsification row | **PARTIAL** | R4-5 BANKED: `05_TRANSPORT_R45B/STAGE3B_TRANSPORT_RECORD.md` + `r45b.log` (`00078e7e…`, 4521 B), digest set `1f74d69a…`, both arms held. Other closed rows (RR2-1..4) are named in the acceptance chain-of-custody but their raw RED/GREEN outputs live in reaudit docs **not in my inputs** — verification caveat (see §4). |
| §2 Honest BLOCKED registry (R4-5 example) | **STALE → see §2** | Line is wrong. Registry *class* is PENDING (must be re-stated at freeze); content must move R4-5→CLOSED and add B3→BLOCKED. |
| §2 Repair-round ledger (≤3 bound, who/tier) | **PARTIAL** | `WPL_P2_PROPOSALS_LEAD_ACCEPTANCE_2026-08-09.md` banks 3 repair rounds (r1 `7194b895`, r2 `75ee8912`, r3 `909ab8f7`) + re-audits. **Missing:** per-round auditor-model/tier attribution is not in my inputs (final re-audit noted as "Codex"; others unspecified). |
| §3 Static min-security / secret-scan / egress inventory (A3) | **PENDING** | WP-I evidence; absent from this staging unit. |
| §3 Executed read-only host-check logs (Group B, no-clobber path/SHA/bytes) | **PENDING (overlap BANKED)** | Group B is WP-I. Overlap only: `STAGE3_TRANSPORT_RECORD.md` Preflight banks host-check-style facts (uptime 7d15h, TCP 22, known_hosts ed25519/rsa/ecdsa, `powercfg` STANDBYIDLE=0/HIBERNATEIDLE=0). |
| §3 Current-state proofs: DISARMED / `state_version` / loopback / `Restart=no` / no creds (B5/B6) | **PENDING (partial overlap)** | B3 banks release+venv tree modes (`root:root 555`), `/var/lib`,`/var/log`,`/etc/mtc-bridge` modes, and clean `-perm /222` sweeps (`STAGE3_TRANSPORT_RECORD.md` "What B3 proved"). DISARMED / `state_version` / listener specifics are not in my inputs. |
| §3 Mutating check (Group C) + preregistration reference | **PENDING** | WP-I. The *model* for it is banked in this unit (prereg-before-invoke; see Gaps §3). |
| §4 `OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` | **EXISTS / PENDING** | Existing controlling doc cited by the draft; not in my inputs. |
| §4 Ratified 50h ledger at freeze + consumed hours | **PARTIAL** | `STAGE3B_TRANSPORT_RECORD.md` books Stage3+3B = **0.4 h**, ~28.3 h remaining (baseline 20.5/29.5 per draft §4). Per-stage booking BANKED; full freeze-time ledger PENDING. |
| §4 WP-L P2 + WP-I authorization + hard exclusions | **BANKED** | `WPL_P2_PROPOSALS_LEAD_ACCEPTANCE_2026-08-09.md` §Scope (no host/credential/broker/ARM/TESTNET/mainnet/master-merge/WP-V/KVM2/economic). Both transport records' "Safety state" sections assert zero mutation/ARM/credential. |
| §5 Scope contract (Linux-port + staging acceptance) | **PENDING** | Dispatcher produces; this staging unit is the staging-acceptance subject. |
| §5 Actual diff/files at frozen SHA (no `--resume`) | **PARTIAL** | `IDX` is the full file+hash inventory for the unit (all five stage dirs). Frozen-SHA diff itself PENDING. |
| §5 Mandated test-suite cmd + baseline (2 `test_order_state.py` gc-referent failures) | **PENDING** | Not in my inputs. |
| §5 Isolated worktree + `git status --porcelain` empty per auditor | **PENDING** | Per-auditor at dispatch. |
| §5 D026 per-test RED location | **PARTIAL** | R4-5 RED BANKED (`05_TRANSPORT_R45B`); others PENDING. |
| §6 Verdict & loop bookkeeping (flagship verdicts, ≤3 repair, sequence-before-WP-A) | **PENDING** | Produced by the round itself, which has not run. |
| (new) B3 STOP outcome / `B3-GAP-ENV` | **BLOCKED-UPSTREAM** | Not in the draft. `03_TRANSPORT/B3_STOP_ADJUDICATION.md` classifies STOP rc 3 (could-not-evaluate), checks #1–#3 held, §8 #4 name-risk unresolved, **owner decision required** before B3 can close. Source item is blocked, so this evidence cannot become PASS without a design-repair / re-freeze cycle. |

---

## 2. Staleness (lines wrong after tonight)

**S1 (most severe).** Draft §2, bullet 3 (lines 39-41):

> "☐ Honest BLOCKED registry — including `WPL_P2_R45_CLOSURE_ATTEMPT_2026-08-09.md` (`ce0bc93e`): **R4-5 remains BLOCKED** (WinError 1314 reproduced 2026-08-09); shell-level equivalent closed by R0-2."

**Correction.** R4-5 is **CLOSED**, not BLOCKED. `05_TRANSPORT_R45B/STAGE3B_TRANSPORT_RECORD.md` records `TR_RUN PASS — all 4 ops rc=0`, RUNID `…-R45B` CONSUMED, both RED (silent write outside restore root) and GREEN (guard raises exact predicted message) arms held, guard proven load-bearing on Linux. `IDX §RUNID ledger` binds it (`r45b.log` `00078e7e…`, set `1f74d69a…`). The `ce0bc93e` Windows attempt (WinError 1314) is now a **historical** superseded record; the current truth is the Linux PASS. The acceptance record itself predicted this ("R4-5 is expected to close trivially on the staging host's Linux", `WPL_P2_PROPOSALS_LEAD_ACCEPTANCE_2026-08-09.md` §Scope).

**S2.** The draft has **no line for B3 at all.** Tonight's Stage 3 produced a STOP (rc 3) at op 05 and a new design gap `B3-GAP-ENV` (`03_TRANSPORT/B3_STOP_ADJUDICATION.md`): the accepted B3 assumes an unprivileged operator can `stat` root-protected paths under `/etc/mtc-bridge/` (mode `750 root:root`), which the unprivileged-`gatea` execution model makes structurally impossible. This is a new **BLOCKED-UPSTREAM** item pending owner decision; the draft's BLOCKED registry must add it. No checklist line covers "blocked-by-design-gap transport outcome."

**S3 (minor).** Draft §0 reconciliation flag (lines 20-22) and the whole framing implicitly assume R4-5 unresolved. Not a factual error by itself, but the dispatcher flag is still open — relevant because **auditor 4 is GLM-5.2**, the very role whose inclusion is undecisively flagged. See Finding F8.

---

## 3. Gaps (evidence classes Audit 2 needs that the draft does not mention)

**G1 — Operator-side transport records (argv / stdout / stderr / rc per op).** Largest banked body of evidence, entirely absent from the draft. `IDX §03_TRANSPORT` lists `operator_record/ops/01..12.{argv,stdout,stderr}` plus `TRANSPORT_RECORD.txt` (`c8ec5d53…`) and `TRANSPORT_SHA256SUMS.txt` (`0b025db2…`); `IDX §05_TRANSPORT_R45B` lists the 4-op equivalent. These are the per-op ground truth (e.g. op `08.stderr` `8a0a4d67…`, op `10.stderr` `112d3237…` capture the expected-consequence CLOSE failures). Audit 2 must be handed these.

**G2 — Remote-vs-local digest-set bindings.** The *only* on-repo proof that the git-excluded `b3.log` / `r45b.log` are what they claim. `STAGE3_TRANSPORT_RECORD.md` op 11 binds B3 remote→local (`CLOSE_DIGEST_SET_SHA256 b25612df…` reproduced bit-identical); `STAGE3B_TRANSPORT_RECORD.md` op 04 binds R45B (`1f74d69a…`). The draft's §3 host-check item is adjacent but never names digest-set verification. Without this, an auditor cannot verify the actual evidence bytes.

**G3 — Burned-RUNID accounting.** `IDX §RUNID ledger` records `-B3` BURNED (STOP rc 3), `-R45` BURNED (never allocated; collateral skip — no evidence tree ever existed), `-R45B` CONSUMED (PASS). Needed to prove no RUNID was replayed/double-spent and that the R4-5 retry followed §11's fresh-preregistration rule (it did: `04_PREREG_R45B/` precedes `05_TRANSPORT_R45B/`). Not in the draft.

**G4 — Preregistration-before-invocation ordering proof (git history).** The methodology's load-bearing claim. `STAGE3B_TRANSPORT_RECORD.md` asserts `PREREGISTRATION_R45B.md` was "written and hash-frozen before any R45B remote invocation"; `IDX` orders `04_PREREG_R45B/` before `05_TRANSPORT_R45B/`. The draft mentions preregistration only for WP-I Group C (§3), not the *ordering proof* for the WP-L P2 transport itself. The git commit order is the checkable artifact.

**G5 — First-FAIL sequencing evidence.** `STAGE3_TRANSPORT_RECORD.md` shows first-FAIL engaged at op 05 (B3), cascading: op 07 skipped (`prior_op_did_not_produce_its_preregistered_rc`), ops 08/10/12 fail with expected consequences (`evidence_dir_absent`, `No such file or directory`, `remote_digest_set_empty`). Tellingly, `IDX §03_TRANSPORT` has **no `07.*` files at all** — the skip is literally visible as an absent op. This proves R4-5's original skip was collateral, not a defect (corroborated by `03_TRANSPORT/B3_STOP_ADJUDICATION.md` "Disposition of R4-5"). Not in the draft.

**G6 — Create-once record-root preservation for git-excluded logs.** The actual bytes of `b3.log`/`r45b.log` live off-repo at `C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08{,-R45B}` (`IDX` footer; both transport records). The draft's §5 "actual diff/files" does not tell auditors where the excluded evidence bytes are or how to bind them.

---

## 4. Verifiability (file + property to recompute/compare)

For each kept/added item, the check. "No method = finding."

- **Block-digest table (kept, §2.1):** recompute SHA-256 of each `IDX §01_RUNKIT/RP*.sh|.py` and compare to `BLOCK_IDENTITIES.tsv`; confirm `RP0-LIB.sh`=`4a404d7b90d8…` (18968 B) matches the RR3-1-corrected §8.1 row. Method: solid.
- **Candidate hashes (kept, §1.2):** recompute `CANDIDATE_RELEASE_SHA256SUMS` at the freeze SHA; compare to `edb0fd34…` (1181804 B). Method: solid.
- **R4-5 RED/GREEN (kept, §2.2 / §5.5):** re-hash `05_TRANSPORT_R45B/…/r45b.log` → `00078e7e…` (4521 B); recompute digest set → `1f74d69a…`; confirm RED-arm harm bytes (`target_magic=b'SQLite format 3\x00'`) and GREEN-arm message string in the log. Method: solid.
- **Digest-set binding (added, G2):** recompute the digest set over the evidence leaf from the create-once record root and compare to `b25612df…` (B3) / `1f74d69a…` (R45B); confirm remote `CLOSE_DIGEST_SET_SHA256` line in `TRANSPORT_RECORD.txt` equals the local bind line. Method: solid.
- **Burned-RUNID ledger (added, G3):** confirm each RUNID in `IDX §RUNID ledger` maps to exactly one evidence tree (or declared none) and that state transitions are monotone (BURNED/CONSUMED never revert). Method: solid.
- **Prereg-before-invoke ordering (added, G4):** `git log --follow` the `04_PREREG_R45B/` files vs `05_TRANSPORT_R45B/` files; prereg commits must precede execute commits. Method: solid (git history).
- **First-FAIL cascade (added, G5):** confirm absence of `07.*` in `IDX §03_TRANSPORT` and the rc pattern (05=3, 06=0, 07=skipped, 08=1, 10=1, 12=3) in `TRANSPORT_RECORD.txt`. Method: solid.
- **Authorization/exclusions (kept, §4.3):** grep transport-record "Safety state" sections for the enumerated zero-mutation/zero-ARM/zero-credential assertions; cross-check against acceptance §Scope exclusion list. Method: solid.
- **Budget (kept, §4.2):** re-sum booked hours (Stage3+3B = 0.4 h per `STAGE3B_TRANSPORT_RECORD.md`) and confirm ≤ ratified 50 h / ~28.3 h remaining. Method: solid for the banked slice; the full freeze ledger must name its source file (see F7).
- **RED/GREEN for non-R4-5 closed rows (kept, §2.2):** **WEAK METHOD** — the draft names no file for RR2-1..4 RED demonstrations. Finding F6.
- **GLM-5.2 reconciliation (§0):** no verification method — it is an open dispatcher decision, not evidence. Flagged F8.

---

## Findings (most severe first)

- **F1 — STALE: R4-5 listed BLOCKED; it is CLOSED.** `AUDIT2_EVIDENCE_CHECKLIST_DRAFT_2026-08-09.md` §2 line 39-41 vs `05_TRANSPORT_R45B/STAGE3B_TRANSPORT_RECORD.md` (PASS, `-R45B` CONSUMED). If handed as-is, auditors could re-block a closed item. *(staleness)*
- **F2 — MISSING EVIDENCE CLASS: transport operator records not in checklist.** `IDX §03_TRANSPORT` / `§05_TRANSPORT_R45B` `operator_record/ops/NN.{argv,stdout,stderr}` + `TRANSPORT_RECORD.txt` + `TRANSPORT_SHA256SUMS.txt`. The richest banked evidence is invisible to Audit 2. *(coverage gap)*
- **F3 — MISSING: digest-set bindings (the only on-repo proof of git-excluded logs).** `b3.log`/`r45b.log` are git-excluded; their identity is provable only via `b25612df…` / `1f74d69a…` (`STAGE3_TRANSPORT_RECORD.md` op 11; `STAGE3B_TRANSPORT_RECORD.md` op 04). Draft never asks auditors to verify these. *(verifiability gap)*
- **F4 — MISSING: burned-RUNID accounting.** `-B3`/`-R45`/`-R45B` lifecycle in `IDX §RUNID ledger` is the no-replay / §11-retry proof; absent from draft. *(coverage gap)*
- **F5 — MISSING: prereg-before-invoke ordering proof + first-FAIL cascade.** `04_PREREG_R45B/`→`05_TRANSPORT_R45B/` commit order and the absent `07.*` / rc cascade (`STAGE3_TRANSPORT_RECORD.md`) prove R4-5's skip was collateral. Absent from draft. *(coverage gap)*
- **F6 — WEAK VERIFIABILITY: RED/GREEN for non-R4-5 rows names no file.** Draft §2.2 + §5.5 give only R4-5 a checkable RED location; RR2-1..4 RED demonstrations are unreferenced. *(verifiability)*
- **F7 — WEAK VERIFIABILITY: §4 "ratified 50h ledger" names no source file.** Banked slice (0.4 h, `STAGE3B_TRANSPORT_RECORD.md`) is checkable; the full freeze ledger is not anchored to a file. *(verifiability)*
- **F8 — PROCESS: §0 GLM-5.2 reconciliation flag unresolved.** Auditor 4's own dispatch contract (supplemental-detection vs omitted under two-flagship directive) is undecided. Not evidence, but it determines whether this review's output is even consumed. *(process)*

*No claim above rests on a file outside the six inputs. Hashes were transcribed from `EVIDENCE_INDEX.md` and the transport records and are internally consistent across all sources read.*
