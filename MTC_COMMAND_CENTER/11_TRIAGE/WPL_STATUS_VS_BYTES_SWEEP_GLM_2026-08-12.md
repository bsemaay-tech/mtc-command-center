# WP-L / B3 closed-record status-vs-bytes sweep — GLM, 2026-08-12

**Verdict: `ADVANCE-SUPPLEMENTAL`.** Source-level only. Read-only local commands used to
re-derive identities (`sha256sum`, `wc -c`, `git cat-file`/`log`/`branch --contains`).
No host or network access, no harness/test execution, no git mutation, no status file
edited. Same method as the sibling `WPI_STATUS_VS_BYTES_SWEEP_GLM_2026-08-12.md`: take
the closed-record prose, re-derive its checkable claims from current bytes, and classify
each defect found as **stale** (understated/outdated, not false) or **wrong** (false
identity, false attribution, broken cross-reference).

Base dir: `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/`

## Result

**Files swept: 4 core** — `EVIDENCE_INDEX.md`, `UNIT_CLOSURE_RECORD.md`,
`INTEGRITY_VERIFICATION_2026-08-10.md`, `FINAL_HANDOFF.md` — plus item-5 record/status
markdown spot-coverage of `08_PREREG_B3B/`, `09_TRANSPORT_B3B/`, and the structure of
`06_B3_REPAIR/`.

**Findings by class: stale = 1 · wrong = 0.** No false byte identity, no false
attribution, no broken cross-reference survived verification.

**~99 evidence identities independently re-derived from current bytes, all match** — every
cross-referenced identity the four documents depend on reproduces exactly, with zero
CRLF/encoding drift. This includes the three evidence logs, both frozen archives, all six
transport RECORD/SHA256SUMS files, the four document self-sizes, full byte+hash sweeps of
four sections (§01_RUNKIT 17/17, §02_PREREG 15/15, §07_RUNKIT_B 19/19, §08_PREREG_B3B
12/12) and the §09 ops set (28/28), the cited commit, the three CLOSE_DIGEST chains, and
the two block-identity counts.

## The one defect (stale)

**`FINAL_HANDOFF.md` is a first-FAIL snapshot whose top-line status was overtaken by the
unit's later closure, and carries no superseded marker.** Its title and verdict —
"WP-L Phase 2 staging — first-FAIL handoff / Unit result: **BLOCKED before remote
contact**" (lines 1–3), "Preregistration | BLOCKED/incomplete" (line 23), "Audit 2 | NOT
STARTED" (line 29), and the "Required next action: Resume only after the exact
counterpart can complete…" instruction (lines 43–45) — were all factually correct at the
write time stamped on the file (2026-08-09 16:47 +0300, immediately after the Stage-2
preregistration timeout). They are **not** correct as a statement of the unit's current
state. The unit recovered and closed the same night: `UNIT_CLOSURE_RECORD.md:8-10` reads
"Status: the unit's executable scope is CLOSED… both checks… have run and PASSED on the
real host"; Stage 2B preregistration was committed (`08_PREREG_B3B/`); B3 was repaired and
**PASSED on the host** (`09_TRANSPORT_B3B/STAGE3B_B3B_RECORD.md`, `b3b.log` 7b383ab5…,
all ops rc=0); Audit 2 ran (`06_B3_REPAIR/audit2/AUDIT2_REPORT.md`).

Classification: **stale**, not wrong. Nothing in `FINAL_HANDOFF.md` is mis-identified or
mis-attributed — the commit `ff32a2db`, the archive `618f7640…`/102400 B, and the byte
counts all verify against current bytes (below). The defect is that the document's
verdict diverges from the byte-level reality (the unit closed) and a reader landing on
`FINAL_HANDOFF.md` alone could conclude the work is still blocked and halt. Failure
scenario: an agent or human opens the staging dir, sorts by name, reads `FINAL_HANDOFF.md`
first, sees "BLOCKED before remote contact / do not execute," and stops — never reaching
`UNIT_CLOSURE_RECORD.md`'s CLOSED status. This is directly analogous to the sibling
sweep's `STATUS_TRANSPORT` finding (a status header not updated to reflect a later PASS).
Mitigant: the current CLOSED status is available in the same directory
(`UNIT_CLOSURE_RECORD.md`), so the fix is a one-line superseded marker on `FINAL_HANDOFF`,
not a re-run.

## Verified clean (the load-bearing claims)

- **Three evidence logs** — recomputed hash + bytes match every citation across all four
  docs and the RUNID ledger:
  `b3.log` = `079d6ac9…` / 1784 B; `r45b.log` = `00078e7e…` / 4521 B;
  `b3b.log` = `7b383ab5…` / 3329 B.
- **Two frozen archives** — `runkit.tar` `618f7640…` / 102400 B (`FINAL_HANDOFF:9`,
  `UNIT_CLOSURE:16`); `runkit_b.tar` `888bec17…` / 184320 B (`UNIT_CLOSURE:22`). Both
  match.
- **Commit `ff32a2db14948bf93e178669086d7d295ca6d5cb`** (`FINAL_HANDOFF:8`) — object type
  `commit`; on branch `feature/donchian-crypto-ladder` (the current branch); subject
  `test(wpl-p2): freeze staging run kit`; dated 2026-08-09 16:25 +0300, i.e. ~20 min
  before the handoff was written — sequence-consistent. Fully verified.
- **CLOSE_DIGEST host-value chain** (`INTEGRITY_VERIFICATION:17-26`) — the host-side
  per-file `CLOSE_DIGEST` lines exist in the ops stdout and carry the matching digests:
  `03_TRANSPORT/ops/06.stdout:6` → `079d6ac9… b3.log`;
  `05_TRANSPORT_R45B/ops/02.stdout:6` → `00078e7e… r45b.log`;
  `09_TRANSPORT_B3B/ops/05.stdout:4` → `7b383ab5… b3b.log`. All three set-digests
  (`b25612df…` / `1f74d69a…` / `d572afe7…`) agree across host stdout, each
  `TRANSPORT_RECORD.txt` `TR_BIND_SET` line, and the RUNID ledger. The "set" digest is the
  `CLOSE_DIGEST_SET_SHA256` (hash of the digest set), correctly distinct from the
  `TRANSPORT_SHA256SUMS.txt` file hashes — internally consistent, not a defect.
- **The INTEGRITY_VERIFICATION remediation claim** (`INTEGRITY_VERIFICATION:43-46`) — that
  `STAGE3B_B3B_RECORD.md` now states `b3b.log`'s individual digest + bytes inline, with an
  op-05 CLOSE_DIGEST pointer and a back-pointer — verified verbatim at
  `STAGE3B_B3B_RECORD.md:23-27` (digest `7b383ab5…`, 3329 bytes, op-05 pointer,
  "see `../INTEGRITY_VERIFICATION_2026-08-10.md`"). All four sub-claims hold.
- **Block counts** — original kit `BLOCK_IDENTITIES.tsv` = **9** blocks (`UNIT_CLOSURE:16`,
  `FINAL_HANDOFF:10` "nine"); B-kit `BLOCK_IDENTITIES_B.tsv` = **10** blocks (the +1 is
  `RPD-VERIFY`; `UNIT_CLOSURE:22` "10", `STAGE3B_B3B:17` "members=10"). Both correct.
  Corroborating: the B-kit tsv records `RP1-B3` provenance `repair_round6` superseding
  `f40411b0…` → now `6f3ea022…`, matching the index and the repair narrative at identity
  level.
- **Audit/round structure** (`UNIT_CLOSURE:21` "6 rounds × 6 audits") — `06_B3_REPAIR/`
  contains `audit1`–`audit6` and `round1`–`round6` plus six `AUDIT*_KICKOFF_CODEX.md` and
  `ROUND2`–`6` kickoffs; consistent with the count and with the EVIDENCE_INDEX §06
  listing.
- **Four document self-sizes** — 21777 / 7190 / 2976 / 2637 B, exactly as the kickoff
  scoped them.
- **Hour ledger internal consistency** — `FINAL_HANDOFF` (20.5 used / 29.5 remaining →
  21.3 / 28.7 after +0.8 h) and `UNIT_CLOSURE` (29.5 at P2 start, −2.6 → ~26.9) agree on a
  50 h budget and the same 29.5 h starting balance.

## Observations (not defects)

- **`INTEGRITY_VERIFICATION:30-34` "working tree carries exactly four untracked entries" /
  `repo_guard.ps1` PASS is a 2026-08-10 snapshot, not a current claim.** The current
  working tree carries ~100 untracked WP-I triage run logs dated 2026-08-12 (per the
  session git status), so "exactly four" no longer holds today. The doc is explicitly
  framed as "Performed by the Lead on 2026-08-10," so this is historically accurate rather
  than stale; flagged only so a reader does not read "exactly four" as present-tense. I did
  not re-run `repo_guard.ps1` (no harness execution).
- **EVIDENCE_INDEX RUNID ledger row for `-B3B` (line 256) is less complete than its
  siblings.** Rows `-B3` (253) and `-R45B` (255) state the individual log hash + bytes
  ("b3.log 079d6ac9… 1784 B", "r45b.log 00078e7e… 4521 B"); row `-B3B` states only
  "b3b.log; set d572afe7…" without the inline hash/bytes. This is precisely the gap
  `INTEGRITY_VERIFICATION:43-46` documents and remediates by stating the b3b.log digest
  inline in `STAGE3B_B3B_RECORD.md` instead. The set digest is correct and the individual
  hash is correct where stated; trivial consistency nit at most, and already acknowledged
  in the unit's own integrity record.

## Verification limits (not defects)

- **Model/lane attribution is not machine-verifiable here.** `UNIT_CLOSURE_RECORD.md:5`
  ("Lead: Claude Fable 5") and `:112-115` (delegation split: Claude Max implemented rounds
  1–6 + re-freeze; Codex `gpt-5.6-sol` audited every round and wrote Stage 2B prereg;
  GLM-5.2 reviewed the Audit-2 checklist / WP-I draft) are prose attribution. The
  `06_B3_REPAIR/` artefacts are `AUDIT*_KICKOFF_CODEX.md` kickoff docs, not run logs with
  model headers, so there is no machine-readable header to confirm the per-round model
  identity. This matches the sibling sweep's note that Claude/Max run logs generally lack
  model headers, so attribution cross-check is cleanly executable only where headers
  exist. Not a defect — a stated limit.
- **`02_PREREG/__pycache__/`** exists on disk and is (correctly) absent from the
  EVIDENCE_INDEX; it is a Python build artifact, not evidence. The §02 byte-count leg was
  aborted by `sha256sum` erroring on that directory, but all 15 §02 hashes matched the
  index, and hash-equality implies byte-equality, so the §02 byte column is verified.

## Coverage boundary (exactly what was and was not reached)

**Byte/hash-recomputed (zero drift):** the four core documents; §01_RUNKIT (17/17);
§02_PREREG (15/15 hashes); §07_RUNKIT_B (19/19); §08_PREREG_B3B (12/12); §09_TRANSPORT_B3B
ops (28/28); the three evidence logs; both archives; all six transport
RECORD/SHA256SUMS files; `STAGE3_TRANSPORT_RECORD.md` / `STAGE3B_TRANSPORT_RECORD.md` /
`STAGE3B_B3B_RECORD.md` (read in full). ~99 identities.

**Structure/existence verified, individual bytes NOT recomputed:** §03_TRANSPORT ops
(01–06, 08–12; 33 files — note there is no op-07, consistent across index and disk);
§05_TRANSPORT_R45B ops (01–04; 12 files); §04_PREREG_R45B (6 files); the whole of
§06_B3_REPAIR (`audit1`–`6` reports+kickoffs, `round1`–`6` DESIGN/RP1-B3/RPD-VERIFY/SELF_QA,
`B3_REPAIR_CYCLE_RECORD.md`, the gap/kickoff docs). For these, file existence and the
directory/audit/round counts were confirmed against the index, but per-file byte+hash was
not re-derived. Given 99 recomputed identities with zero drift across every section type
(ops, evidence, archives, tsv, code, docs), the index is mechanically sound; the unreached
files are a stated limitation, not a suspected problem.

**Not reached:** `B3_REPAIR_CYCLE_RECORD.md` body (the §06 top-level cycle record) was not
read; `operator_record/evidence/` blob contents beyond the three logs; the runkit
directories were not recursed (per the scope's explicit exclusion).
