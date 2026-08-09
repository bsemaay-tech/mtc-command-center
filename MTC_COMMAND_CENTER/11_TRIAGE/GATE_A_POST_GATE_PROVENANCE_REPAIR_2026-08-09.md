# Gate A — Post-Gate Provenance Repair (candidate vs documentation source split)

- **Date:** 2026-08-09.
- **Unit type:** Bounded **documentation-only** repair on a protected Bridge evidence surface.
  **Read-only / local.** No product, deploy, or test file was modified.
- **Model / route:** `claude-opus-5`, effort `xhigh`, fresh independent implementer session.
  **Round 2 (2026-08-09):** a second, fresh `claude-opus-5` `xhigh` session repaired this record and
  the matrix in place under the same protected scope — see the round-2 block below and §2.7, §5.1,
  §6.7, §10.
  **Round 3 (2026-08-09):** a third, fresh `claude-opus-5` `xhigh` session, same two-file scope,
  separating the **expected** payload byte hash from the **observed** installed-host bytes — see the
  round-3 block below and §2.7(e), §2.7(g), §3, §9.2a, §11.
- **Documentation / governance HEAD:** round 1 `851d2aa56be950fda8a3447fca99b20153110721`;
  round 2 `f8a6bc0f1a7fa00fcd1637297e05424732386da7` (detached, clean tree). The commits between
  them are documentation-only: every `IBKR_PAPER_BRIDGE` blob compared in §4 was re-resolved at
  `f8a6bc0f` this round and is **identical to its `851d2aa5` value**, so every round-1 blob
  comparison stands unchanged at the current HEAD.
  **Round 3** was applied at the same HEAD `f8a6bc0f`, with the round-1/round-2 edits present as
  **uncommitted working-tree changes to these two files only**. Nothing was committed, staged, or
  otherwise mutated in Git; `IBKR_PAPER_BRIDGE` blob state is unchanged from the round-2 reading.
- **Frozen / deployed product candidate:** `2ce41e34bceb599d80af24c5c33d835820ec321b` (**unchanged**).
- **Merge base:** `4d2228cf8985ce755c398cceff23f777a99d5404` — re-derived at `f8a6bc0f` this round;
  both `--is-ancestor` tests still exit 1, so the refs remain divergent.
- **Exact writes (two files only):**
  1. this record (new);
  2. `11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md` (repaired in place;
     all valid content preserved).
- **Commands executed:** read-only Git only (`git rev-parse`, `git merge-base`, `git cat-file`,
  `git grep`, `git show`, `git diff --stat`, `git status`). **No** SSH, sudo, systemctl, reboot,
  service, test run, package/install, network/broker/exchange, credential, ARM/order, or
  staging-host command. **No Git mutation** of any kind (no add/commit/push/checkout/switch/reset/
  stash/clean/worktree-mutation/branch/tag).

> **Working-directory note.** The task named `C:\tmp\postgate_runkit_design_claude` as the work
> root. That path is outside this session's permitted filesystem scope and could not be read. The
> repo at `C:\PGR` was already detached at the required documentation HEAD `851d2aa5` with a clean
> working tree, i.e. the required state, so the unit was performed there. Both frozen refs and the
> merge base were re-verified before any write (§2). This changes the location of the work, not any
> fact in it.

---

> # ⛔ ROUND-3 SUPERSEDING CORRECTION — expected payload bytes vs observed installed-host bytes
>
> **Where this block conflicts with anything below — including the round-2 block — this block
> governs.** Reproduction in §2.7(e) and the new §2.7(g).
>
> **What stands, unchanged.**
> `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e` is the correct **expected
> source/payload byte hash** of `requirements.lock`: the SHA-256 of the raw **LF** Git-blob content,
> re-derived a third time this round (`git cat-file blob 47f53fa2… | sha256sum` → `a1881296…`;
> `git cat-file -s 47f53fa2…` → `117762`). Because
> `2ce41e34…321b:…/deploy/linux/package.sh:78-83` exports the payload with
> `-c core.autocrlf=false -c core.eol=lf`, that same byte stream is what the LF release archive ships.
> `40873556…` remains a Windows CRLF worktree artifact and remains uncitable — that conclusion rests
> on byte arithmetic over the blob (§2.7a–c) and does not depend on anything corrected below.
>
> **What is corrected.** Rounds 1 and 2 took one step further than their evidence and stated as
> **fact** that the file installed on `GATEA-STAGING` hashes to `a1881296…`, and that
> `/etc/mtc-bridge/install_manifest.json` → `requirements_lock_sha256` carries that value. That is a
> **derivation from source and packaging mechanics — not an observation.** **No Gate-A evidence
> located in this repair records either the observed SHA-256 of
> `/opt/mtc-bridge/releases/2ce41e34…321b/IBKR_PAPER_BRIDGE/requirements.lock` or the observed
> `requirements_lock_sha256` value on the host.** Enumerated in §2.7(g).
>
> | Value class | Status |
> |---|---|
> | **Expected source/payload byte hash** — raw blob content SHA-256, LF, 117 762 B: `a1881296…` | ✅ **Established** by read-only Git at the candidate plus the LF pin in `package.sh`. This is what a run-kit step preregisters as the *expected* value. |
> | **Observed installed-host byte hash** — `sha256sum` of the installed lock, and `install_manifest.json` → `requirements_lock_sha256` | ⛔ **NOT IN EVIDENCE.** No record located here reports it. It is an **open read-only host predicate**, not a known fact, and it is blocked by the §1 budget/authority hold. |
> | **Windows worktree checkout SHA-256** — CRLF, 119 274 B: `40873556…` | ⛔ **Never cite.** Unchanged from round 2. |
>
> **Consequence for preregistration.** A run-kit step must read: *expected* `a1881296…`, **to be
> compared** against a host value that has not yet been read — never as a restatement of something
> already verified on the host. On a mismatch the disposition is **investigate read-only**, weighing
> **both** possibilities (a wrong expected value *and* genuine drift) rather than presuming either.
> Round 2's disposition — "a mismatch produced by using `40873556…` is a documentation error, not lock
> drift" — remains correct, but it is specific to *that* value and does **not** extend to a mismatch
> against `a1881296…`.
>
> **What this does NOT change.** No product defect. The candidate is unchanged. No staging action, no
> host read, no test execution, no Git mutation, no commit. The 56-entry / 1345-hash counts stand.
> `40873556…` stays withdrawn, G4 stays withdrawn, WP0 stays uneditable, and every other round-1 and
> round-2 conclusion stands.

---

> # ⛔ ROUND-2 SUPERSEDING CORRECTION — lock byte provenance
>
> **Where this block conflicts with anything below, this block governs** — except where the round-3
> block above governs it. Full reproduction in §2.7.
>
> Round 1 (and the Lead item it inherited) conflated **three different values** into one "candidate
> lock hash". They are separated here for good:
>
> | Value | What it actually is | Where it is valid |
> |---|---|---|
> | `47f53fa227bf0f18b9bf9bd77e060d8856961728` | **Git blob object ID (SHA-1)** of `IBKR_PAPER_BRIDGE/requirements.lock` — a hash of `"blob 117762\0" + content`, *not* a content hash | Ref-invariant: identical at the candidate `2ce41e34…321b`, at `851d2aa5`, at `f8a6bc0f`, **and** at the SECURITY_BASELINE frozen source `637307e8` |
> | `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e` | **SHA-256 of the raw blob content** — LF line endings, **117 762 bytes**. The candidate lock's canonical content identity | Everywhere the lock is handled as committed or deployed bytes: `git cat-file blob` and the `git archive` payload (**established**); and, as the ⛔ **expected** value pending an observed host read (round 3), `RELEASE_SHA256SUMS` and `/etc/mtc-bridge/install_manifest.json` → `requirements_lock_sha256` |
> | `40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3` | **SHA-256 of a Windows documentation-worktree CRLF checkout** — **119 274 bytes**, produced by this machine's `core.autocrlf=true` (`i/lf`, `w/crlf`, `attr/text=auto`) | **Nowhere in the candidate and nowhere in host evidence.** It is a property of a local Windows working copy, not of the frozen candidate |
>
> `119 274 − 117 762 = 1 512`, which is exactly the blob's line count — one `\r` inserted per line.
> The two SHA-256 values are hashes of **different byte streams**, so neither can substitute for the
> other.
>
> **The defect.** This record's §4.1, §6.3 and §8, and the matrix's Lead-corrections bullet, §0.5 and
> A3, all call `40873556…` "the candidate lock blob SHA-256" and assert it "remains valid and needs
> no re-derivation". That is wrong twice over: it is not a *blob* hash (that is `47f53fa2…`), and it
> is not a hash of anything the candidate contains. Blob **identity** across the refs is genuine —
> and was correctly established — but it licences the wrong number.
>
> **Why this is operational, not cosmetic (all candidate-verified, §2.7):**
> `2ce41e34…321b:…/deploy/linux/package.sh:78-82` builds the payload with
> `git -c core.autocrlf=false -c core.eol=lf … archive`, so the deployed lock is **LF**;
> `…/install.sh:401,416` hashes the *installed* lock and records it as `requirements_lock_sha256` in
> `/etc/mtc-bridge/install_manifest.json`; `…/verify.sh:82-91` re-verifies every release file against
> `RELEASE_SHA256SUMS`. The installed lock is therefore **expected** to hash to `a1881296…`
> (⛔ round-3 precision: expected **by construction**, not observed — no host read of that value is in
> evidence; see §2.7g). Preregistering `40873556…` as the expected host value — which the matrix's A3
> "Output artifact" line invited — would have been wrong either way: it is a hash of no byte stream
> the candidate contains, so against a host that does match the payload it produces a **false STOP** —
> a fabricated "lock drift" alarm on a protected surface where a STOP halts the whole post-Gate chain.
>
> **Corroboration (this was already right before round 1 broke it).** The accepted pre-Gate records
> carry the correct value *and* the correct label:
> `f8a6bc0f:IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:28-29` records "Git blob
> `47f53fa2…`" and "Raw Git-blob SHA-256 `a1881296…`" as two separate rows; its own verification
> snippet at `:155-174` computes the value the same way this repair does (`git cat-file blob` →
> `hashlib.sha256`, `:172-174`); and `WPI_READINESS_RECORD_2026-08-01.md:52` records both together.
> `40873556…` appears in **no** product file and in no record predating 2026-08-08.
>
> **Consequently the A3 "lock-identity precision" caveat is also corrected:** the lock blob at
> SECURITY_BASELINE's frozen source `637307e8` is *also* `47f53fa2…`, so that document's lock
> identity **is** the current candidate's lock identity. There is no separate `1adf9ae5` lock hash to
> avoid citing.
>
> **What this does NOT change.** No product defect. The candidate is unchanged. No staging action, no
> test execution, no Git mutation. The 56-entry / 1345-hash counts stand (re-derived again this
> round). Every round-1 finding other than the lock-hash label stands.

---

## 1. Defect statement and impact

### 1.1 Defect

`GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md` was authored by reading **product**
files (tests, `verify.sh`, `bridge/app.py`, `wal_state_bundle.py`, `deploy/linux/README.md`) out of
the **documentation/governance checkout** at `851d2aa5`, and then attributing those readings to the
**frozen, deployed product candidate** `2ce41e34…321b`.

The two refs are **divergent** — neither is an ancestor of the other (§2.2). The documentation
branch is therefore **not** a valid source for candidate product behaviour. Where the blobs differ,
every fact the matrix took from the checkout is a fact about a *different tree* than the one
installed on `GATEA-STAGING`.

### 1.2 Primary false claim

The matrix asserted that the WP0-cited regression symbol
`test_kill_restart_after_request_commit_keeps_killed_and_resumes_once` is **ABSENT** from source,
recorded this as gap **G4** ("stale evidence-map node"), propagated it to §0 (Lead acceptance
corrections), A5, E2, §4 row 11, §5, §7, and Next-steps step 1, and proposed a **WP0 edit** to
delete the citation from `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` lines 308 and 364.

**This is false for the frozen, deployed candidate.** The symbol exists at
`2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:2765`. It is absent only from
the divergent documentation checkout. **All 11 target symbols exist at the candidate** (§5).

### 1.3 Impact

| Impact | Severity | Detail |
|---|---|---|
| **Near-miss destructive edit to accepted baseline evidence** | **High** | The matrix directed a deletion of a *correct* WP0 I-R2 citation. Executing it would have removed true coverage evidence from an accepted baseline record and manufactured a real evidence gap on a protected persistence/kill surface. **Cancelled** — see §7. |
| **Understated candidate safety posture** | **High** | The matrix contains no mention of the candidate's credential-free DISARMED start-mode enforcement (unit `Environment=` pin, `verify.sh` env-override rejection, `bridge/app.py` no-broker construction). Those protections are **absent from the documentation-branch blobs** and so were invisible to the author. The strongest safety property of the deployed candidate went unrecorded. |
| **Unusable line citations** | Medium | Every `verify.sh`, `README.md`, and test line number in the matrix is a documentation-checkout offset. Against the candidate they point at the wrong lines, so a run-kit author following them would preregister the wrong assertions. |
| **Mis-scoped source-of-truth for `SECURITY_BASELINE.md`** | Medium | Cited as the canonical source for A3 and C5 as though it were candidate payload. It does **not exist** at the candidate (§4); it is a later governance/evidence artifact. |
| **Overstated egress premise** | Medium | C5 states "source constructs the TESTNET broker before any human ARM transition." At the candidate, in the mode the host actually runs, **no broker is constructed at all** (§6.5). |
| **Contamination beyond the matrix** | Medium | The same false claim was propagated into three further governance files (§9). Those are outside this unit's write scope and are handed to the Lead. |
| **⛔ Round-2 addition — wrong lock hash preregistered as a host predicate** | **High** | Round 1 endorsed `40873556…` (a Windows CRLF working-copy artifact) as "the candidate lock blob SHA-256". The install path records and re-verifies the hash of the **LF** payload, whose expected value is `a1881296…`. Comparing the CRLF value against a host that matches the payload would fail and raise a fabricated lock-drift STOP. Corrected in the round-2 block and §2.7; propagation to three out-of-scope files handed to the Lead (§9). |
| **⛔ Round-3 addition — a derived expectation recorded as an observed host fact** | Medium | Rounds 1–2 wrote that the installed lock "therefore hashes to `a1881296…`" and attributed that value to `install_manifest.json` on `GATEA-STAGING`. The value is right as an **expectation**; the **observation** was never made and appears in no evidence located here (§2.7g). Left as written, a run-kit author would treat an untested host predicate as already-verified evidence — the same class of error as G8/G9, one step further out — and a future mismatch would be misdiagnosed in whichever direction the record implied. Corrected in the round-3 block, §2.7(e)/(g), §3 and §9.2a; the observed value is now carried as an open, blocked read-only item. |

### 1.4 What is *not* defective

**No product defect was found.** The candidate is correct on every point examined; the defect is
entirely in the documentation's provenance discipline. See §7.

---

## 2. Exact reproduction (read-only Git only)

All commands were run at repo root with the documentation HEAD checked out. Output is verbatim.

### 2.1 Refs

```
$ git rev-parse HEAD
851d2aa56be950fda8a3447fca99b20153110721

$ git cat-file -t 2ce41e34bceb599d80af24c5c33d835820ec321b
commit

$ git status --short
(no output — clean)
```

### 2.2 Divergence proof

```
$ git merge-base 851d2aa5 2ce41e34bceb599d80af24c5c33d835820ec321b
4d2228cf8985ce755c398cceff23f777a99d5404

$ git merge-base --is-ancestor 2ce41e34bceb599d80af24c5c33d835820ec321b 851d2aa5
→ exit 1   (candidate is NOT an ancestor of the documentation HEAD)

$ git merge-base --is-ancestor 851d2aa5 2ce41e34bceb599d80af24c5c33d835820ec321b
→ exit 1   (documentation HEAD is NOT an ancestor of the candidate)
```

**Both exit 1 ⇒ the refs are divergent.** Neither tree may stand in for the other.

### 2.3 The 11 target symbols at the **candidate** (all present)

```
$ git grep -n -E 'def (test_gates_persist_across_restart|test_kill_persists_across_restart|test_killed_alive_is_interrupted|test_bundle_never_contains_a_wal_shm_trio|test_invariants_preserve_risk_and_history)' 2ce41e34bceb599d80af24c5c33d835820ec321b -- IBKR_PAPER_BRIDGE/tests
2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_api.py:69:def test_kill_persists_across_restart(tmp_path):
2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py:333:def test_gates_persist_across_restart(tmp_path):
2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py:856:def test_bundle_never_contains_a_wal_shm_trio(tmp_path, bundle_dir, capsys):
2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py:882:def test_invariants_preserve_risk_and_history(source_db, bundle_dir, capsys):
2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_window_state.py:82:def test_killed_alive_is_interrupted():

$ git grep -n -E 'def (test_drill_disconnect_reconnect_dedupes_to_one_order|test_drill_data_stale_auto_disarms|test_drill_ws_death_triggers_auto_reconnect|test_data_stale_emits_and_disarms_once|test_active_recovery_suppresses_ordinary_reconcile_repair|test_kill_restart_after_request_commit_keeps_killed_and_resumes_once)' 2ce41e34bceb599d80af24c5c33d835820ec321b -- IBKR_PAPER_BRIDGE/tests
2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_bars.py:27:def test_data_stale_emits_and_disarms_once():
2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py:16:def test_drill_disconnect_reconnect_dedupes_to_one_order(tmp_path):
2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py:87:def test_drill_data_stale_auto_disarms(tmp_path):
2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py:319:def test_drill_ws_death_triggers_auto_reconnect():
2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:1871:def test_active_recovery_suppresses_ordinary_reconcile_repair(tmp_path):
2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:2765:def test_kill_restart_after_request_commit_keeps_killed_and_resumes_once(
```

**11 / 11 present.** Symbol 11 is at `test_partial_fill_protection.py:2765`.

### 2.4 The same grep at the **documentation** ref (10 only) — the contamination signature

```
$ git grep -n -E 'def (…same 11 alternatives…)' 851d2aa5 -- IBKR_PAPER_BRIDGE/tests
851d2aa5:IBKR_PAPER_BRIDGE/tests/test_api.py:61:def test_kill_persists_across_restart(tmp_path):
851d2aa5:IBKR_PAPER_BRIDGE/tests/test_bars.py:27:def test_data_stale_emits_and_disarms_once():
851d2aa5:IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py:333:def test_gates_persist_across_restart(tmp_path):
851d2aa5:IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py:16:def test_drill_disconnect_reconnect_dedupes_to_one_order(tmp_path):
851d2aa5:IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py:40:def test_drill_data_stale_auto_disarms(tmp_path):
851d2aa5:IBKR_PAPER_BRIDGE/tests/test_p1_failure_drills.py:272:def test_drill_ws_death_triggers_auto_reconnect():
851d2aa5:IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:1867:def test_active_recovery_suppresses_ordinary_reconcile_repair(tmp_path):
851d2aa5:IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py:289:def test_bundle_never_contains_a_wal_shm_trio(tmp_path, bundle_dir, capsys):
851d2aa5:IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py:315:def test_invariants_preserve_risk_and_history(source_db, bundle_dir, capsys):
851d2aa5:IBKR_PAPER_BRIDGE/tests/test_window_state.py:82:def test_killed_alive_is_interrupted():
```

10 hits — symbol 11 missing. **Every line number in this output matches the matrix's §4 table
exactly** (`test_api.py:61`, `p1_failure_drills:40/272`, `partial_fill:1867`,
`wal_state_bundle:289/315`). That byte-level agreement is conclusive: the matrix was built from the
documentation checkout, not from the candidate.

### 2.5 Scale of the divergence

```
$ git diff --stat 2ce41e34bceb599d80af24c5c33d835820ec321b 851d2aa5 -- IBKR_PAPER_BRIDGE
 …33 files changed, 624 insertions(+), 14372 deletions(-)
```

Relative to the candidate the documentation tree is missing ~14.4k lines of product and test code,
including the whole of `tests/test_credential_free_disarmed.py`
(candidate blob `ce0ae7c24f795dc8e5d56bf7cca82e1a75351402`; **absent** at `851d2aa5`).

### 2.6 Lock counts re-derived at the candidate

```
$ git grep -c -E '^[A-Za-z0-9][^ ]*==' 2ce41e34…321b -- IBKR_PAPER_BRIDGE/requirements.lock
2ce41e34…321b:IBKR_PAPER_BRIDGE/requirements.lock:56

$ git grep -c -E 'hash=sha256:' 2ce41e34…321b -- IBKR_PAPER_BRIDGE/requirements.lock
2ce41e34…321b:IBKR_PAPER_BRIDGE/requirements.lock:1345
```

56 exact-pinned entries, 1345 hash lines — matching the Lead's recorded values. Re-derived again in
round 2 at the same ref with the same output.

### 2.7 Lock byte provenance — exact reproduction (round 2)

**(a) One blob, four refs.** The lock is byte-identical everywhere it has ever been cited:

```
$ git rev-parse HEAD
f8a6bc0f1a7fa00fcd1637297e05424732386da7

$ git rev-parse HEAD:IBKR_PAPER_BRIDGE/requirements.lock \
                851d2aa5:IBKR_PAPER_BRIDGE/requirements.lock \
                2ce41e34bceb599d80af24c5c33d835820ec321b:IBKR_PAPER_BRIDGE/requirements.lock
47f53fa227bf0f18b9bf9bd77e060d8856961728
47f53fa227bf0f18b9bf9bd77e060d8856961728
47f53fa227bf0f18b9bf9bd77e060d8856961728

$ git rev-parse 637307e83951ffe23e768ed8e50ddaf8712b0660:IBKR_PAPER_BRIDGE/requirements.lock
47f53fa227bf0f18b9bf9bd77e060d8856961728        ← SECURITY_BASELINE's frozen source: same blob
```

**(b) The blob ID is not a content hash.** `47f53fa2…` is SHA-1 over `"blob 117762\0" + content`.
The content hash must be derived separately:

```
$ git cat-file -s 47f53fa227bf0f18b9bf9bd77e060d8856961728
117762

$ git cat-file blob 47f53fa227bf0f18b9bf9bd77e060d8856961728 | sha256sum
a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e *-

$ git cat-file blob 47f53fa227bf0f18b9bf9bd77e060d8856961728 | wc -l
1512
```

**(c) The Windows checkout is a different byte stream.** The same logical file, as it sits in this
documentation worktree:

```
$ sha256sum IBKR_PAPER_BRIDGE/requirements.lock
40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3 *IBKR_PAPER_BRIDGE/requirements.lock

$ wc -c IBKR_PAPER_BRIDGE/requirements.lock
119274 IBKR_PAPER_BRIDGE/requirements.lock

$ git ls-files --eol IBKR_PAPER_BRIDGE/requirements.lock
i/lf    w/crlf  attr/text=auto          IBKR_PAPER_BRIDGE/requirements.lock

$ git config --get core.autocrlf
true
```

`119274 − 117762 = 1512`, and the blob has exactly **1512** lines. The conversion is fully accounted
for: one `\r` per line, no other difference. `40873556…` is therefore a **local Windows working-copy
artifact**, reproducible only by hashing a CRLF checkout — it is not a property of the blob, of the
candidate, or of anything installed on `GATEA-STAGING`.

**(d) The deployed payload is LF — the candidate says so itself.** The packager pins line endings
*specifically* to defeat the conversion that produced `40873556…`:

```
$ git grep -n -B 4 'core.autocrlf=false -c core.eol=lf' 2ce41e34…321b -- IBKR_PAPER_BRIDGE/deploy/linux/package.sh
…/package.sh:78:log "exporting ${RELEASE_SHA} via git archive"
…/package.sh:79:# Both line-ending pins are required: the repository's `* text=auto`
…/package.sh:80:# attribute makes core.eol load-bearing.  On Windows, its native default would
…/package.sh:81:# emit CRLF even with core.autocrlf=false.
…/package.sh:82:git -c core.autocrlf=false -c core.eol=lf -c tar.umask=0022 -C "${REPO}" \
…/package.sh:83:  archive --format=tar "${RELEASE_SHA}" | tar -x -C "${OUT}"
```

The candidate's own deploy tooling anticipated this exact hazard. The documentation walked into it
anyway.

**(e) The installed lock hash is a live host predicate.** It is computed, recorded, and re-checked by
the candidate's own deploy code. ⛔ **Round-3 scope note:** this establishes the *mechanism* and the
*expected* value — it is source-side reading, not an observation of the installed bytes (see (g)).

```
$ git grep -n -E 'requirements\.lock|requirements_lock_sha256' 2ce41e34…321b -- IBKR_PAPER_BRIDGE/deploy/linux/install.sh
…/install.sh:401:LOCK_SHA="$(sha256_of "${DEST}/IBKR_PAPER_BRIDGE/requirements.lock")"
…/install.sh:416:  "requirements_lock_sha256": "${LOCK_SHA}",

$ git grep -n RELEASE_SHA256SUMS 2ce41e34…321b -- IBKR_PAPER_BRIDGE/deploy/linux/verify.sh
…/verify.sh:82:  actual_manifest_sha="$(sha256_of "${DEST}/RELEASE_SHA256SUMS")"
…/verify.sh:88:  if ( cd "${DEST}" && sha256sum --strict --quiet -c RELEASE_SHA256SUMS ); then
…/verify.sh:89:    pass "release payload matches RELEASE_SHA256SUMS"
…/verify.sh:91:    fail "release payload does not match RELEASE_SHA256SUMS"
```

`install.sh:401` hashes the *installed* file and `:416` writes it into
`/etc/mtc-bridge/install_manifest.json` as `requirements_lock_sha256`; `verify.sh:82-91` re-verifies
every release file, `requirements.lock` included, against `RELEASE_SHA256SUMS`. The installed value is
therefore **expected** to be the LF hash `a1881296…` — expected because the payload is exported
LF-pinned and the installed tree is manifest-verified, **not** because any record here reports what
the host actually holds (g). A run-kit step preregistering `40873556…` is wrong independently of that:
it is the hash of a byte stream the candidate does not contain, so against a host that does match the
payload it fails and manufactures drift.

**(f) Independent corroboration — the correct value predates the error.**

```
$ git grep -n 'a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e' f8a6bc0f
f8a6bc0f:IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:29:| Raw Git-blob SHA-256 | `a1881296…` |
f8a6bc0f:IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:160:$expectedSha256 = 'a1881296…'
f8a6bc0f:IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md:174:expected_sha256 = "a1881296…"
f8a6bc0f:MTC_COMMAND_CENTER/11_TRIAGE/WPI_READINESS_RECORD_2026-08-01.md:52:… Git blob `47f53fa2…`; raw blob SHA-256 `a1881296…` …
```

`SECURITY_BASELINE.md:28-29` keeps "Git blob" and "Raw Git-blob SHA-256" as **two separate rows**,
and its own snippet at `:155-174` derives the value exactly as (b) does — `git rev-parse` for the
blob ID (`:159-162`), then `git cat-file blob` → `hashlib.sha256` for the content (`:172-174`).
`40873556…` appears in **no**
product file and in **no** record predating 2026-08-08:

```
$ git grep -n '40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3' f8a6bc0f
MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:101
MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md:252
MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md:208
MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md:344
MTC_COMMAND_CENTER/11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md:46
MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md:49
MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md:37
        ← seven, repo-wide, all documentation; none outside MTC_COMMAND_CENTER

$ git grep -n '40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3' 2ce41e34…321b
(no output — the value does not exist anywhere in the frozen candidate)
```

Four of those seven are in this unit's two files and are corrected here. The remaining three are
outside write scope and are handed to the Lead (§9).

**(g) ⛔ What is NOT established (round 3) — there is no observed installed-host lock hash.**

Everything in (a)–(f) is **source-side**: Git blobs, the candidate's own packaging and install code,
and records that predate the error. None of it is a reading of `GATEA-STAGING`. The local searches
run this round are listed below with what they actually returned; none yields an observed installed
lock hash.

| Where an observed value could have been recorded | What is actually recorded |
|---|---|
| `GATE_A_POST_GATE_TRANSITION_INVENTORY_2026-08-09.md` §"Install-time manifest facts" (`:57-65`) — the one located record that reads `/etc/mtc-bridge/install_manifest.json` for this candidate | Boolean / schema fields only: `env_file_populated=false`, `secrets_provisioned=false`, `firewall_modified=false`, `steady_unit_installed=false`, `schema_version=1.0.0`, install-time `service_started=false`, `service_enabled=false`. **No hash field of any kind**, and no `requirements_lock_sha256`. |
| The raw `A2 install` capture (27 061 B, indexed by SHA-256 in the same inventory), and the local `C:\WPI_ARTIFACTS\` captures generally | **Read locally by the Lead — the expected value is there, the observed one is not.** `C:\WPI_ARTIFACTS\2ce41e34bceb599d80af24c5c33d835820ec321b\RELEASE_SHA256SUMS:99` records the **expected package-member** hash `a1881296…` for `./IBKR_PAPER_BRIDGE/requirements.lock`; `C:\WPI_ARTIFACTS\post_gate_transition_inventory_detail_20260809.out` records `requirements_lock_sha256` **only as a `manifest_top_keys` entry — the field value is not printed**. No targeted local-artifact hit records the observed installed-host lock hash or the host manifest field value. `/home/gatea/` remains **uninspected**; no host was contacted. The A-2 capture is in any case unlikely to carry the value: `install.sh` computes `LOCK_SHA` at `:401` and writes it **only** into the manifest at `:416`; its completion log lines at `:431-433` print the release SHA and the **unit** SHA-256, never the lock hash. (Read from the ref-invariant blob `40983e5a…`, so this reading is not provenance-sensitive.) |
| `GATE_A_RESULT_2026-08-08.md:126,133-149` — the only local record combining a `verify_lock` PASS, a `RELEASE_SHA256SUMS` match and an `install_manifest.json` field dump | Belongs to the **superseded** release: the dump reads `release_sha ebada020…`. It records `verify_lock: PASS: lock; packages=56` — a **count**, not a hash — and quotes `first_start_unit_sha256`, never `requirements_lock_sha256`. |
| `GATE_A_RECON_DEFECT_LIST_2026-08-02.md:47-48,135`; `GATE_A_REPAIR_VALIDATION_2026-08-02.md:111-112` | Same pattern one release earlier (`1adf9ae5` era): `packages=56` counts, no lock hash. |
| The A-0..A-9 canonical PASS reports for `2ce41e34…321b` | No `requirements.lock` hash appears in any of them (repo-wide grep for `requirements_lock_sha256` / `lock … SHA-256` returns only documentation records, the product `SECURITY_BASELINE.md`, a KVM2 manifest **template** with the placeholder `"REQUIRED_64_HEX"`, and these two repair files). |

**Contrast — observed host hashes *are* recorded where someone captured them.** The same transition
inventory carries the first-start unit fragment SHA-256 `538c1c6038…79bd` (3736 B, `:44-45`) and both
payload archives' SHA-256s (`:50-54`) as measured host values. The installed lock's hash is simply not
among the values anyone measured, which is why it cannot be asserted here.

**How it can be closed — NOT EXECUTED, currently blocked.** One read-only host read suffices: either
`sha256sum /opt/mtc-bridge/releases/2ce41e34…321b/IBKR_PAPER_BRIDGE/requirements.lock`, or a root read
of `/etc/mtc-bridge/install_manifest.json` (mode `0640 root:root`) for `requirements_lock_sha256`.
Both are `read-only-host`; both are blocked by the §1 budget/authority hold; **neither was run in this
unit and no host was contacted.** Until one is captured and recorded with its command and output, the
installed value's status is exactly: **expected `a1881296…`, unobserved.**

### 2.8 Documentation-branch drift check (round 2)

Round 1 compared blobs at `851d2aa5`; the current HEAD is `f8a6bc0f`. Every path in §4 was
re-resolved at `f8a6bc0f` and returned the **same** documentation-side blob ID recorded in round 1
(`verify.sh` `bce1f0e2…`, first-start template `b175ced7…`, `bridge/app.py` `6d0abc63…`,
`wal_state_bundle.py` `aaa29182…`, `SECURITY_BASELINE.md` `8db2e6dd…`, and the ref-invariant four).
The three intervening commits are documentation-only. Divergence was also re-proven at the current
HEAD: `git merge-base f8a6bc0f 2ce41e34…321b` → `4d2228cf…`, and both `--is-ancestor` tests exit 1.

---

## 3. Source-of-truth split (binding)

| Fact class | Authoritative source | Never use |
|---|---|---|
| Current roadmap, sequencing, §23a / Audit-2 wording | documentation/governance branch (`851d2aa5`) | the candidate tree (stale governance) |
| Authority envelope, owner authorisations, hard stops | documentation branch | candidate tree |
| Canonical audit roster, D025 / D026 rules (`AGENTS.md`) | documentation branch | candidate tree |
| Handoffs, `_AI_MEMORY`, Gate-A evidence index | documentation branch | candidate tree |
| Gate-A A0–A9 evidence, host inventory | immutable captured evidence, explicitly tied to `2ce41e34…321b` | either checkout |
| **Product source** (`bridge/**`) | `git show` / `git grep` at `2ce41e34…321b` | documentation checkout |
| **Deploy assets** (`deploy/linux/**`) | `2ce41e34…321b`, or installed-host evidence tied to it | documentation checkout |
| **Runtime / start-mode behaviour** | `2ce41e34…321b`, or A-5/A-7/A-8/A-9 evidence | documentation checkout |
| **Test symbols, paths, line numbers** | `2ce41e34…321b` | documentation checkout |
| **Tooling behaviour** (`tools/wal_state_bundle.py`) | `2ce41e34…321b` | documentation checkout |
| **⛔ Content hashes of any committed file** (round 2) | `git cat-file blob <id> \| sha256sum`, or installed-host evidence | **any hash of a Windows worktree file** — CRLF conversion makes it a different byte stream (§2.7) |
| **⛔ What the host actually holds** (round 3) | a **captured** read-only host measurement, recorded with its command and its output | **a source-derived expectation** — a sound derivation from blob + packaging rules is still not an observation (§2.7g) |

**Rule.** Where a blob is *identical* on both refs, either citation is valid and the fact is
ref-invariant. Where blobs *differ*, only the candidate is admissible for product/deploy/runtime/
test/tool facts, and every path **must** be written commit-qualified as
`2ce41e34…321b:<path>:<line>`. Bare `<path>:<line>` is no longer acceptable in post-Gate evidence.

**Round-2 corollary.** Ref-invariance is a statement about *bytes in Git*, not about bytes on disk.
A blob identical on both refs still has **two** different SHA-256 values in play — its LF content
hash and this Windows worktree's CRLF checkout hash — and only the first is a candidate or host
fact. Every recorded hash must therefore name its input: *blob object ID (SHA-1)*, *raw blob content
SHA-256 (LF)*, or *worktree checkout SHA-256*. An unlabelled hash is unverified.

**Round-3 corollary.** A hash carries a second, independent property: its **epistemic status**. It is
either *derived from source* — the Git blob's content, or a payload the packaging rules make
byte-equal to it — or *observed on the host*: a `sha256sum` someone actually ran there, or a manifest
field someone actually read. These are not interchangeable, and a derivation, however sound, may not
be written as though the observation had been made. Every hash in a post-Gate record must therefore
carry **both** labels: *what was hashed*, and *expected-from-source* vs *observed-on-host*. Where the
observation has not been made, say so and carry it as an open predicate — as the installed
`requirements.lock` hash now is (§2.7g).

---

## 4. Candidate-vs-documentation blob table

Blob IDs from `git rev-parse <ref>:<path>`; all paths under `IBKR_PAPER_BRIDGE/`.

### 4.1 Identical blobs — ref-invariant, both citations valid

⛔ **Completed in round 2.** Round 1 listed four; the full set across every path either document
cites is **nine**. The five added rows matter: they identify facts the provenance defect *could not*
have corrupted, which narrows what still needs re-derivation.

| Path | Blob (both refs) | Added round 2 |
|---|---|---|
| `requirements.lock` | `47f53fa227bf0f18b9bf9bd77e060d8856961728` | |
| `deploy/linux/verify_lock.py` | `8ccd6f329154422a85b8e7663e6a079dbd47b4fd` | |
| `deploy/linux/rollback.sh` | `4b36674dcb1baa7c3b119cac98f8e6017b1f1566` | |
| `deploy/linux/COMMANDS.md` | `3deeefc8da2984d5220482f065e569b74874847a` | |
| `deploy/linux/install.sh` | `40983e5a675728dbdefe68e46dfe6d055d2841a1` | ✅ |
| `deploy/linux/systemd/mtc-bridge-steady.service.template` | `121229ea5b0fc8c67c8bc5e49d4ffcc3f25f4fba` | ✅ |
| `tests/test_bars.py` | `17453080ed330ed2f4cc72bbe5e245164420a2ad` | ✅ |
| `tests/test_interim_risk_wiring.py` | `29214adae7006ac6b60bf53240b2e507f3ad858d` | ✅ |
| `tests/test_window_state.py` | `e9d39129587f7d8e2b26e2f3d5221b7a02d4b106` | ✅ |

⛔ **Corrected lock statement (round 2).** The lock blob being identical proves **blob identity**, and
nothing more. It does **not** validate `40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3`,
which round 1 wrongly called "the Lead's SHA-256 [of the lock blob]" and declared exempt from
re-derivation. That value is the SHA-256 of a **Windows CRLF worktree checkout** (119 274 B). The
lock's actual content SHA-256 is **`a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e`**
(LF, 117 762 B), and *that* is what blob identity makes ref-invariant. The counts (56 entries /
1345 hash lines) were correct and are re-confirmed. Full reproduction: §2.7.

⛔ **Round-3 boundary on the same statement.** Blob identity and the LF export pin fix the **expected**
bytes; they say nothing about what is on `GATEA-STAGING`. `a1881296…` is therefore ref-invariant *as a
property of the committed and packaged file*, and remains an **unobserved expectation** with respect to
the installed copy and to `install_manifest.json` → `requirements_lock_sha256` (§2.7g).

### 4.2 Differing blobs — candidate only

⛔ **Completed in round 2.** Round 1 left six paths as an unresolved "differ / differ"; their exact
IDs are supplied here so the table is independently checkable rather than merely asserted.

| Path | Candidate `2ce41e34…321b` | Documentation (`851d2aa5` = `f8a6bc0f`) |
|---|---|---|
| `deploy/linux/verify.sh` | `5cfefd709202ff504ae7b7fc3504b8c0b00900b6` | `bce1f0e23e63f9a8d168c751aec99ac84d1334c7` |
| `deploy/linux/systemd/mtc-bridge-first-start.service.template` | `c18232549d96aa200d8c7f796e64de743288940c` | `b175ced7f36df52ad2e55532264f36f49fdc8281` |
| `tools/wal_state_bundle.py` | `26c077e650ab88ba2086efa3a80790769bc055b1` | `aaa2918229a1367ebf1fb6a458a4e65673dc180e` |
| `bridge/app.py` | `572c4178fe804da17601eefd898027e9261492e6` | `6d0abc6351a0d20aef324fb00b936c0f189d036f` |
| `deploy/linux/README.md` | `f3f1d75e7e4369609cd0eb299466b2ceb62a0a16` ⛔ | `666b79d834f50433cd0cba7c88224fb674fdbb56` |
| `deploy/linux/env/mtc-bridge.env.template` | `c03d6e47ab57c00ef95f4122607fc7ba88119e35` ⛔ | `fbf8cb833c58a30c8262f14027512bbfdedae3e8` |
| `deploy/linux/lib/common.sh` | `db11010a24edfbb96ba80ec1fbe1db3ff29193c9` ⛔ | `7d5aa166ac2f3b703e9543a42d49564c66e34002` |
| `deploy/linux/package.sh` | `add6478d33cce8d929d58f895407abe01d51da20` ⛔ | `150c18c36447ecc122332a992581ca6d9bba4007` |
| `tests/test_partial_fill_protection.py` | `7b0b9ea36dd8b15108f6befcbcb00015ed2f51fb` ⛔ (symbol 11 at :2765) | `42c55c09afc93edb4d7364008da4b702176721c3` (symbol 11 absent) |
| `tests/test_api.py` | `40d31925ac93c4bfe13a877f060b5abaf6c0cd6e` ⛔ | `d9da63e7f66afd6db7e24eef774296dce9487c16` |
| `tests/test_wal_state_bundle.py` | `07de7b206f56c7442c3ea07ec160dc7ef2497415` ⛔ | `edc02108c9829aa7b2409fd3eca774d00cb1b5b2` |
| `tests/test_p1_failure_drills.py` | `9e50c1b51cd6d60967f5481adfeda9779815efd9` ⛔ | `f2e3a32171c12c53bd31bba35dbcc691417b53b6` |

⛔ = ID first recorded in round 2. `package.sh` is a path neither document previously cited; it is
added because §2.7(d) depends on it.

### 4.3 Presence asymmetry

| Path | Candidate | Documentation |
|---|---|---|
| `deploy/linux/SECURITY_BASELINE.md` | **ABSENT** | present, blob `8db2e6dd7e782c96f585f6672c4489c4ce5c1488` |
| `tests/test_credential_free_disarmed.py` | present, blob `ce0ae7c24f795dc8e5d56bf7cca82e1a75351402` | **ABSENT** |

```
$ git rev-parse 2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md
fatal: path 'IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md' exists on disk,
       but not in '2ce41e34bceb599d80af24c5c33d835820ec321b'
```

`SECURITY_BASELINE.md` is a **later governance/evidence artifact**, not a member of the deployed
candidate payload. It may legitimately *describe* analysis of the candidate, but it must be cited as
governance evidence with that distinction stated — never as candidate source.

---

## 5. Corrected all-11 test map (candidate-qualified)

All rows verified at `2ce41e34bceb599d80af24c5c33d835820ec321b`. Paths are relative to
`IBKR_PAPER_BRIDGE/`. The final column shows the documentation-checkout line the matrix had wrongly
recorded.

| # | Symbol | Candidate path:line | Maps to | Doc-ref line (wrong) |
|---|---|---|---|---|
| 1 | `test_gates_persist_across_restart` | `tests/test_interim_risk_wiring.py:333` | E1 / I-R1 | 333 (coincides) |
| 2 | `test_kill_persists_across_restart` | `tests/test_api.py:69` | E2 / I-R2 | 61 |
| 3 | `test_killed_alive_is_interrupted` | `tests/test_window_state.py:82` | E2 / I-R2 | 82 (coincides) |
| 4 | `test_bundle_never_contains_a_wal_shm_trio` | `tests/test_wal_state_bundle.py:856` | E3 / I-R3, C3 | 289 |
| 5 | `test_invariants_preserve_risk_and_history` | `tests/test_wal_state_bundle.py:882` | E3 / I-R3, C3 | 315 |
| 6 | `test_drill_disconnect_reconnect_dedupes_to_one_order` | `tests/test_p1_failure_drills.py:16` | E4 | 16 (coincides) |
| 7 | `test_drill_data_stale_auto_disarms` | `tests/test_p1_failure_drills.py:87` | E5 | 40 |
| 8 | `test_drill_ws_death_triggers_auto_reconnect` | `tests/test_p1_failure_drills.py:319` | E6 | 272 |
| 9 | `test_data_stale_emits_and_disarms_once` | `tests/test_bars.py:27` | E5 | 27 (coincides) |
| 10 | `test_active_recovery_suppresses_ordinary_reconcile_repair` | `tests/test_partial_fill_protection.py:1871` | E7 | 1867 |
| 11 | `test_kill_restart_after_request_commit_keeps_killed_and_resumes_once` | `tests/test_partial_fill_protection.py:2765` | **E2 / I-R2** | **claimed ABSENT** |

**Status: 11 / 11 EXIST at the frozen, deployed candidate.** There is no stale evidence-map node.
`WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` lines 308 and 364 are **correct as written** and require
no edit. D026 is unaffected: these remain *existing* coverage, not new closure evidence.

### 5.1 "Coincides" ≠ ref-invariant (round-2 precision)

The table's four "(coincides)" rows are **not** one category. Three of the seven test files that hold
the eleven symbols are byte-identical on both refs (§4.1), and four differ:

| Symbol | File | Blob status | Why the line numbers agree |
|---|---|---|---|
| 1 `test_gates_persist_across_restart` | `tests/test_interim_risk_wiring.py` | **ref-invariant** `29214ada…` | **Structural.** Same bytes on both refs; `:333` cannot disagree. |
| 3 `test_killed_alive_is_interrupted` | `tests/test_window_state.py` | **ref-invariant** `e9d39129…` | **Structural**, as above (`:82`). |
| 9 `test_data_stale_emits_and_disarms_once` | `tests/test_bars.py` | **ref-invariant** `17453080…` | **Structural**, as above (`:27`). |
| 6 `test_drill_disconnect_reconnect_dedupes_to_one_order` | `tests/test_p1_failure_drills.py` | **differs** (`9e50c1b5…` vs `f2e3a321…`) | **Coincidence only.** The divergence in this file begins after line 16 — symbols 7 and 8 in the same file shift by 47. |

Practical consequence: rows 1, 3 and 9 are genuinely ref-invariant and a documentation-checkout
reading of them was harmless. Row 6 agreed **by luck**, and must still be treated as
candidate-sourced. Do not generalise from a matching line number to a matching file.

---

## 6. Corrected implications

### 6.1 Start mode — the candidate's strongest safety property (previously unrecorded)

```
$ git grep -n 'MTC_BRIDGE_START_MODE' 2ce41e34…321b -- IBKR_PAPER_BRIDGE/deploy/linux
…/README.md:113,114,116
…/env/mtc-bridge.env.template:40,42
…/systemd/mtc-bridge-first-start.service.template:42:Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed
…/verify.sh:143,144,146,171

$ git grep -n 'MTC_BRIDGE_START_MODE' 851d2aa5 -- IBKR_PAPER_BRIDGE/deploy/linux
(no output)
```

Candidate-verified, three layers:

1. **Unit pins the mode.**
   `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:42`
   → `Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed`.
2. **Verifier enforces it and blocks override.**
   `…/verify.sh:171` adds `MTC_BRIDGE_START_MODE=credential_free_disarmed` to the required unit
   needle list; `…/verify.sh:143-146` **fails** if any `MTC_BRIDGE_START_MODE=` assignment (bare or
   `export`) appears in `/etc/mtc-bridge/mtc-bridge.env`, so the env file cannot override the unit.
   `…/env/mtc-bridge.env.template:40-42` documents that the key must stay absent.
3. **Application implements it.** `2ce41e34…321b:IBKR_PAPER_BRIDGE/bridge/app.py`:
   - `:32` `CREDENTIAL_FREE_DISARMED_START_MODE = "credential_free_disarmed"`;
   - `:113` rejects `--dry-run` combined with the mode; `:115` rejects being handed a broker;
   - `:138-147` forces `network="disabled"`, `exchange_conn="disabled"`,
     `exchange_enabled=False`, `credential_lookup="disabled"`, **`arm_enabled=False`**;
   - `:149` `if start_runtime and not credential_free_disarmed:` — the broker build
     (`_build_broker`, which resolves credentials at `:244` and selects `network="testnet"` at
     `:246`) is **never reached** in this mode.

**None of this exists in the documentation-branch blobs.** Any future citation of start-mode
behaviour must be candidate-qualified or drawn from installed-host / Gate-A evidence.

### 6.2 Verifier (`verify.sh`) — corrected candidate line anchors

Every `verify.sh` line citation in the matrix was a documentation offset. Candidate anchors:

| Region | Candidate lines | Matrix had (doc) |
|---|---|---|
| §1 service identity | 54–76 | — |
| §2 immutable release tree | 77–102 | 78–135 (as "§2/§4") |
| §3 hash-locked venv | 103–122 | 104–121 |
| §4 writable state/log/config | 123–136 | (folded into 78–135) |
| §5 secret hygiene (incl. start-mode env rejection 143–146) | 137–154 | — |
| §6 unit state | 155–222 | 150–199 |
| — unit needle list (incl. start-mode needle at 171) | 160–171 | 155–165 |
| — template byte-compare (`cmp`) | 186–195 | 182–190 |
| — `[Install]` absent check | 197–201 | — |
| — masked assertion | 206–211 | — |
| — ACTIVE ⇒ fail ("must not be running before KVM2-P4-07") | 213–214 | 207–211 |
| §7 steady profile must be absent | 223–232 | — |
| §8 logs / rotation / control plane | 233–251 | 233–244 |
| — masked/unstarted-mode comment | 240–242 | 234–236 |
| — zero `bridge.app` writer | 243–247 | 237–241 |
| — control port closed | 248 | 242 |
| §9 summary | 252– | — |

The **substance** of matrix gap G2 is unchanged and re-confirmed at the candidate: `verify.sh` is a
*pre-start, masked-mode* verifier. At `…:214` an ACTIVE unit is a failure; at `…:243-247` any
`bridge.app` writer is a failure; at `…:248` the control port must be closed; the comment at
`…:240-242` states the mode explicitly ("This verifier is specifically the masked/unstarted mode…
this mode requires both zero writer processes and a completely closed port, including loopback").
A wholesale post-start `verify.sh` run will therefore still **intentionally fail**. Only the line
numbers were wrong, not the conclusion.

### 6.3 `SECURITY_BASELINE.md`

Absent from the candidate (§4.3). Reclassified from "canonical source" to **governance/evidence
artifact describing candidate analysis** — that reclassification stands.

⛔ **Round-2 correction to the lock sentence.** Round 1 said the document's "stated lock identity
refers to frozen source `637307e8` / candidate `1adf9ae5…`, not to `2ce41e34…321b`", and then
endorsed `40873556…` as the candidate's SHA-256. Both halves are wrong:

- **The lock identity does apply.** `git rev-parse 637307e8:IBKR_PAPER_BRIDGE/requirements.lock`
  returns `47f53fa227bf0f18b9bf9bd77e060d8856961728` — the *same blob* as the candidate's (§2.7a).
  `SECURITY_BASELINE.md:28-29` is therefore an accurate statement of the current candidate's lock
  identity, not a stale one. There is no separate "`1adf9ae5` lock blob hash" to avoid citing.
- **The SHA-256 it records is the correct one.** `SECURITY_BASELINE.md:29` gives
  `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e`, matching the reproduction in
  §2.7b. `40873556…` is a Windows CRLF worktree artifact and must not be cited as a candidate or
  host value anywhere.
  ⛔ **Round-3 precision:** `SECURITY_BASELINE.md` is itself a **source-side** record — its own snippet
  derives the value with `git cat-file blob` → `hashlib.sha256` (`:172-174`). It corroborates the
  *expected* payload hash; it is not, and never was, a reading of the staging host (§2.7g).

The lock *property* (56 exact+hashed entries; `verify_lock.py` contract) remains ref-invariant
because the blob is byte-identical (§4.1), and the ref-invariant content hash is `a1881296…`. Note
the distinction this document preserves and round 1 lost: `47f53fa2…` is the **blob object ID**,
`a1881296…` is the **content SHA-256**. They are different hashes of different inputs and neither is
a substitute for the other.

### 6.4 WAL tool (`tools/wal_state_bundle.py`)

The candidate blob `26c077e6…` is the product source of truth; the documentation blob `aaa29182…`
differs and must not be used for line references. Candidate-verified:

- CLI exposes exactly two subcommands — `create` (`…:1218`) and `verify` (`…:1232`), under a
  required subparser (`…:1216`). There is no third subcommand and no built-in
  "restore-into-temp" mode.
- `collect_invariants` is public at `…:417`.
- `--allow-live-source` exists on `create` (`…:1223`; usage banner `…:48`).
- Safety mechanics hold: `PRAGMA integrity_check` / `PRAGMA foreign_key_check` on both ends
  (`…:405-411`, `:786-788`, `:821-823`, `:1116-1118`); SQLite online-backup API `src.backup(dst)`
  (`…:801`) rather than copying the db/wal/shm trio; fail-closed on sidecar presence
  (`…:814-816`, `:1157-1159`, `:1120-1121`).

Matrix item C3's substance stands. Because there is no `restore` subcommand, the C3 **COMMAND GAP**
(a restore-into-temp wrapper must be authored) is confirmed rather than removed — and it is now
confirmed *against the candidate* instead of against the wrong blob.

### 6.5 Egress (C5) — corrected premise

The matrix stated: *"source constructs the TESTNET broker before any human ARM transition."* At the
candidate this is true **only** for a non-credential-free `start_runtime` launch. In the mode the
staging host actually runs (`credential_free_disarmed`), `bridge/app.py:149` gates broker
construction off entirely: no credential resolution, no `network="testnet"` selection, no
exchange connection, `arm_enabled=False`.

Corrected implication: **a runtime egress capture cannot be obtained from the current staging
runtime at all** — not because ARM is missing, but because the deployed start mode constructs no
broker and therefore emits no broker egress. Any authorised future capture requires a *different*,
separately authorised start mode plus credential and TESTNET-network authority — none of which
exists now. This makes C5 a harder blocker than the matrix recorded, not a softer one. The
Lead's standing correction that such a capture **does not require ARM** remains valid, and ARM
remains forbidden.

### 6.6 `deploy/linux/README.md` (G6)

Candidate anchors: line 4 `Status: **PREPARATION ONLY — nothing here has been executed on any
host.**`; lines 123–125 `These assets have **never been executed**, on KVM2 or anywhere else…`.
The matrix cited doc-ref lines 4 / 118–120. G6's conclusion is unchanged: after Gate A A-0..A-9 the
candidate **has** been installed and started on `GATEA-STAGING`, so that README text is
**historical only**.

### 6.7 Remaining candidate qualification (round 2) — anchors for the citations round 1 left bare

Round 1 qualified the citations it had *corrected*. It left the ones it had not disputed as bare
`<path>` references — which its own §3 rule declares unverified. Those are resolved here. All line
numbers verified by `git grep` at `2ce41e34…321b`.

**(a) First-start unit template** — candidate-only blob `c1823254…` (A4, C1, C2):

| Directive | Candidate line |
|---|---|
| `Environment=MTC_BRIDGE_STATE_DB=/var/lib/mtc-bridge/bridge.db` | 40 |
| `Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed` | 42 |
| `KillSignal=SIGTERM` | 48 |
| `KillMode=mixed` | 49 |
| `TimeoutStopSec=45` | 51 |
| `FinalKillSignal=SIGKILL` | 52 |
| `Restart=no` | 55 |

No `[Install]` section exists; the only match for `[Install]` is the explanatory comment at line 11
("`systemctl enable` is structurally impossible"). This confirms C1's SIGTERM/45 s/SIGKILL premise
and G1's no-auto-start premise **at the candidate** — round 1 asserted both from an unqualified
"unit template".

**(b) Steady (gated) profile** — `deploy/linux/systemd/mtc-bridge-steady.service.template`,
blob `121229ea…`, **ref-invariant** (§4.1). `Restart=on-failure` at line 52; no `[Install]` (comment
at 19); `KillSignal=SIGTERM` 44, `TimeoutStopSec=45` 47, `FinalKillSignal=SIGKILL` 48.

⛔ **New candidate-verified fact, and the one asymmetry worth preregistering:** the steady template
carries **no** `Environment=MTC_BRIDGE_START_MODE=` line. Its `Environment=` set is lines 39–41
(`PYTHONUTF8`, `PYTHONDONTWRITEBYTECODE`, `MTC_BRIDGE_STATE_DB`) only. The three-layer credential-free
DISARMED enforcement of §6.1 is therefore **specific to the first-start unit**, not a property of
the deployed candidate in general. **This is not a defect claim** — the steady profile is gated,
never installed, never enabled, and its admission is a separately authorised Gate-B/WP-V step. It is
recorded because any future admission preregistration must not assume the start-mode pin carries
over; that assumption would be false, and §0.6/§6.1 as written could invite it.

**(c) `verify_lock.py`** — blob `8ccd6f32…`, **ref-invariant** (A3, A6, B1): `parse_lock` at 28;
`main` at 75; `--check-installed` flag at 78; the PASS line
`print(f"verify_lock: PASS: {mode}; packages={len(expected)}")` at 97 — i.e. B1's expected
`packages=56` is emitted from the lock's parsed entry count, not a hard-coded constant.

**(d) `rollback.sh`** — blob `4b36674d…`, **ref-invariant** (C4, G3): usage banner 25–27; flag
parsing `--to-release-sha` 44, `--to-manifest-sha256` 45, `--state-manifest-file` 46,
`--state-manifest-sha256` 47; the two hard requirements at 57–58 (`"--state-manifest-file is
required"`, `"--state-manifest-sha256 is required"`); the paired-flag guard at 65
(`"--to-release-sha and --to-manifest-sha256 must be supplied together"`); `rollback_manifest.json`
path at 70; `systemctl stop` at 82; `systemctl mask` at 86 and 153; target-release manifest
verification at 122–124. This confirms C4's flag contract and G3's "the `--to-*` pair is optional"
reading **at the candidate**.

**(e) `COMMANDS.md`** — blob `3deeefc8…`, **ref-invariant** (C3, C4, G2): Stage A 20, B 44, C 63,
D 96, E 116, F 205, G 240. Lines 90–92 instruct the operator to record "the first-start unit SHA-256
and `requirements.lock` SHA-256 (also written to `/etc/mtc-bridge/install_manifest.json`)" — the
step that makes §2.7's lock-hash correction operationally live.

**(f) `install.sh`** — blob `40983e5a…`, **ref-invariant**, newly cited: payload manifest
verification 109–120 and 156–162; installed-tree re-verification 267–269; lock presence and
exact+hashed check 168–174; venv/lock parity via `verify_lock.py --check-installed` at 287–288 and
308–309; installed lock hash 401 → `"requirements_lock_sha256"` 416.

**(g) `package.sh`** — candidate-only blob `add6478d…` (doc `150c18c3…`), newly cited: `git archive`
export with `-c core.autocrlf=false -c core.eol=lf` at 78–83, with the comment at 79–81 naming the
Windows CRLF hazard explicitly. §2.7(d).

**(h) `verify.sh`** — candidate-only blob `5cfefd70…`, anchors additional to the §6.2 section map:
release-manifest SHA compare at 82–86; whole-tree `sha256sum -c RELEASE_SHA256SUMS` at 88–91;
`verify_lock.py --check-installed` invocation at 117; `install_manifest.json` release-manifest grep
at 130; first-start unit SHA-256 log at 159.

**Net effect.** Every product, deploy and tool path cited by either document now resolves to an
explicit candidate blob (§4.1/§4.2) and, where a behaviour is asserted, to a candidate line anchor.
Nothing product-related in either file now rests on a bare `<path>` reference.

---

## 7. Explicit scope of this unit

| Question | Answer |
|---|---|
| Product defect found? | **No.** The candidate is correct on every point examined; symbol 11 exists, start-mode protections are present and enforced, the WAL tool and verifier behave as documented. |
| Candidate changed? | **No.** `2ce41e34…321b` is untouched. No product, deploy, or test file was written. |
| Staging-host action? | **None.** No SSH, systemctl, sudo, reboot, service, network, broker, credential, ARM, or order command was issued. `GATEA-STAGING` was not contacted. |
| Tests executed? | **None.** All test facts come from `git grep` at the candidate. This is *existence* evidence only, never execution or D026 closure evidence. |
| `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` edited? | **No — and the previously proposed deletion is CANCELLED.** WP0 lines 308 and 364 are correct at the candidate. No replacement symbol is needed. |
| Installed-host lock hash observed? | **No — and not in any located evidence (round 3).** No host was contacted here, and no prior record captures it. `a1881296…` is the **expected** payload value; the observed value remains open (§2.7g, B1a in the matrix). |
| Git mutations? | **None.** Read-only Git only. |
| Files written | Exactly two: this record (new) and the matrix (repaired in place). |
| Budget / authority posture | Unchanged. The 50 h balance remains NOT REPRODUCIBLE; all host execution remains blocked. This unit was local and read-only and consumed no host budget. |

---

## 8. Acceptance checklist

- [x] Both refs resolved; divergence proven by two failing `--is-ancestor` tests; merge base
      `4d2228cf…` recorded.
- [x] All 11 symbols located at the candidate with commit-qualified `path:line`.
- [x] Documentation-ref grep reproduced, showing 10 hits and line numbers byte-identical to the
      matrix's §4 table — establishing the contamination mechanism, not merely asserting it.
- [x] Four identical blobs confirmed by `git rev-parse` on both refs.
- [x] Five differing blobs confirmed with both-side IDs.
- [x] `SECURITY_BASELINE.md` proven absent at the candidate; `test_credential_free_disarmed.py`
      proven present at the candidate and absent at the doc ref.
- [x] ~~Lock re-derived at the candidate: 56 entries / 1345 hashes; blob identity makes the Lead's
      SHA-256 valid unchanged.~~ ⛔ **Second clause WITHDRAWN in round 2.** Counts stand (56 / 1345,
      re-derived twice). Blob identity (`47f53fa2…`, ref-invariant across four refs) does **not**
      validate `40873556…`, which is a Windows CRLF worktree artifact. The lock's content SHA-256 is
      `a1881296…` — §2.7.
- [x] Start-mode enforcement verified at all three layers with candidate line anchors; absence from
      the doc branch verified by empty grep.
- [x] `verify.sh` candidate section map rebuilt; G2's conclusion re-confirmed at the candidate.
- [x] WAL tool subcommand surface and safety mechanics verified at the candidate.
- [x] Egress premise corrected against `bridge/app.py:149`.
- [x] WP0 deletion cancelled; WP0 untouched.
- [x] Exactly two files written; no product/deploy/test file touched; no Git mutation; no host
      command; no test run.

**Round 2 additions:**

- [x] Three lock values separated and each independently reproduced: blob ID `47f53fa2…`
      (four refs), content SHA-256 `a1881296…` (117 762 B, 1512 lines), Windows CRLF checkout
      SHA-256 `40873556…` (119 274 B) — with the byte arithmetic closing exactly (§2.7a–c).
- [x] Lock-hash error shown to be operationally live, not cosmetic: `package.sh:78-83`
      (LF-pinned `git archive`), `install.sh:401,416` (`requirements_lock_sha256` in
      `install_manifest.json`), `verify.sh:82-91` (`RELEASE_SHA256SUMS` re-verification) — §2.7d–e.
- [x] Correct value corroborated against records predating the error: `SECURITY_BASELINE.md:28-29`
      and `:161-174`, `WPI_READINESS_RECORD_2026-08-01.md:52` (§2.7f).
- [x] All seven repository occurrences of `40873556…` enumerated; the four in scope corrected, the
      three out of scope handed to the Lead (§2.7f, §9).
- [x] Documentation-branch drift check: every §4 path re-resolved at the current HEAD `f8a6bc0f`
      and identical to its `851d2aa5` value; divergence and merge base re-proven (§2.8).
- [x] Ref-invariant blob set completed 4 → 9; all previously unresolved "differ / differ" rows given
      exact both-side IDs (§4.1, §4.2).
- [x] "Coincides" rows separated into three structurally ref-invariant and one accidental (§5.1).
- [x] Every remaining bare product/deploy/tool citation qualified with candidate blob + line anchors
      (§6.7 a–h).
- [x] Steady-profile start-mode asymmetry recorded as a preregistration prerequisite, explicitly
      **not** as a defect claim (§6.7b).
**Round 3 additions:**

- [x] Expected payload byte hash re-derived a third time and unchanged:
      `git cat-file blob 47f53fa2… | sha256sum` → `a1881296…`; `git cat-file -s` → `117762`.
      `a1881296…` is **retained** as the correct expected source/payload value for the LF archive.
- [x] Observed-vs-expected separated wherever rounds 1–2 asserted the installed host value:
      round-2 block, §1.3, §2.7(e), §4.1, §6.3 — each now says *expected*, with the observation
      marked absent.
- [x] The absence itself evidenced rather than assumed (§2.7g): transition-inventory manifest read
      records boolean/schema fields only; `install.sh` writes `LOCK_SHA` to the manifest (`:416`) but
      never logs it (`:431-433`), so it is not expected in the A-2 capture either; the only local
      `verify_lock` / `RELEASE_SHA256SUMS` PASS records belong to the superseded `ebada020` and
      `1adf9ae5` releases and carry package **counts**, not hashes.
- [x] Contrast recorded — observed host hashes exist where captured (unit fragment `538c1c60…79bd`,
      both payload archives), so the gap is specific to the lock, not a general absence of host
      measurement.
- [x] Closure method for the observed value written as a bounded read-only host read, marked
      **NOT EXECUTED** and blocked by the §1 authority/budget hold.
- [x] §3 extended with the epistemic-status rule (expected-from-source vs observed-on-host).
- [x] Round-2's `40873556…` withdrawal re-checked and **left standing** — it rests on byte arithmetic
      over the blob, not on any host claim, so nothing in round 3 weakens it.
- [x] No product/deploy/test file touched; no host contacted; no test run; no Git mutation; no commit.
- [ ] **Lead independent acceptance** — re-run §2 (including §2.7) in a fresh session and confirm.
      The single decisive round-2 check is
      `git cat-file blob 47f53fa227bf0f18b9bf9bd77e060d8856961728 | sha256sum` → must be
      `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e`.
      ⛔ The decisive **round-3** check is the negative one: search the Gate-A evidence set for an
      observed `requirements_lock_sha256` or an installed-lock `sha256sum` for `2ce41e34…321b` and
      confirm there is none (§2.7g). The Lead's local read of `C:\WPI_ARTIFACTS\` has now been made:
      it confirms the package-manifest **expected** hash (`…\2ce41e34…321b\RELEASE_SHA256SUMS:99` →
      `a1881296…`) and the mere existence of the `requirements_lock_sha256` key
      (`post_gate_transition_inventory_detail_20260809.out`, `manifest_top_keys` only, value not
      printed), and supplies **no** installed-host value. `/home/gatea/` is the one place left to
      check; it remains uninspected and no host was contacted.
- [ ] **Observed installed-host lock hash** — OPEN. Requires one authorised read-only host read; not
      performed and not authorised here (§2.7g, §9.2a).
- [ ] **Gate-7 memory write-back** — Lead only, after acceptance. Not performed in this unit.

---

## 9. Next steps

1. **[Lead]** Independently reproduce §2.2–§2.8 in a fresh session before accepting this repair.
   Two decisive checks:
   - `git grep -n test_kill_restart_after_request_commit_keeps_killed_and_resumes_once 2ce41e34bceb599d80af24c5c33d835820ec321b -- IBKR_PAPER_BRIDGE/tests`
     → must return `tests/test_partial_fill_protection.py:2765`.
   - ⛔ `git cat-file blob 47f53fa227bf0f18b9bf9bd77e060d8856961728 | sha256sum`
     → must return `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e`.
     Hashing the *worktree file* on Windows instead returns `40873556…`; that is the error being
     repaired, and reproducing it that way confirms the diagnosis rather than refuting the fix.
2. **[Lead]** Propagate **both** corrections to the three files outside this unit's write scope.
   Each carries the withdrawn symbol-11 claim **and** the wrong lock hash:
   - `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` — symbol 11 at `:27`, lock hash at `:46`
   - `_AI_MEMORY/GLOBAL_HANDOFF.md` — symbol 11 at `:28`, lock hash at `:49`
   - `_AI_MEMORY/NEXT_STEPS.md` — symbol 11 at `:23`, lock hash at `:37`
   The symbol-11 lines record a correct citation as an evidence-map problem. The lock-hash lines
   record `40873556…` as re-derived candidate evidence; replace with content SHA-256 `a1881296…`
   (blob ID `47f53fa2…`), or drop the value and cite §2.7. ⛔ **Round 3:** if the replacement value is
   written, label it *expected raw blob content SHA-256 (LF) — source-derived*; do **not** restate it
   as the installed-host or `install_manifest.json` value (§2.7g).
2a. **[Lead / AI: Any, local only]** ⛔ **Round 3 — carry the installed-host lock hash as an open
   item, not a fact.** No located evidence records the observed
   `/opt/mtc-bridge/releases/2ce41e34…321b/IBKR_PAPER_BRIDGE/requirements.lock` hash or the host
   `requirements_lock_sha256` (§2.7g). Preregister `a1881296…` as the **expected** value and leave the
   observed side open until an authorised read-only host read is captured and recorded with its
   command and output. Until then, no record may say "the installed lock hashes to …". The read
   itself stays blocked under §1 with every other host action.
3. **[Lead]** Confirm **no** WP0 edit is made. `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` is correct.
4. **[AI: Any, local only]** When authoring the run-kit designs (matrix Group B and the C1–C5
   COMMAND GAPs), take every product/deploy/tool line anchor from §5–§6 of this record or re-derive
   it at `2ce41e34…321b`. Do not read product facts from the documentation checkout.
5. **[AI: Any, local only]** Adopt the standing convention: post-Gate evidence cites product facts
   as `2ce41e34…321b:<path>:<line>`. A bare `<path>:<line>` in a post-Gate record should be treated
   as unverified.
5a. **[AI: Any, local only]** ⛔ **Companion rule for hashes (round 2).** Every hash in a post-Gate
   record must state **what was hashed**, using these three labels and no others:
   *Git blob object ID (SHA-1)* · *raw blob content SHA-256 (LF)* · *worktree checkout SHA-256*.
   Never hash a file from a Windows working tree and record the result as candidate or host
   evidence: this repo is `core.autocrlf=true` with `* text=auto`, and this `requirements.lock`
   checkout differs from the committed and deployed bytes because line-ending conversion is **proven**
   for it (§2.7c); other text files subject to that conversion **may** differ too. Derive candidate
   content hashes from Git blob/archive bytes — `git cat-file blob <id> | sha256sum` — rather than
   assuming them from a converted worktree; that is the method the candidate's own
   `SECURITY_BASELINE.md:172-174` already prescribes.
6. **[Lead]** Gate-7 memory write-back after acceptance — record the source-split rule (§3) as the
   durable lesson, not the individual line numbers.
7. **[AI: Barış]** Unchanged and unaffected by this unit: the 50 h re-plan / ceiling extension, and
   the named explicit lifts required before WP-V, KVM2, master merge, credentials, broker/exchange,
   ARM, orders, TESTNET/mainnet, or economic action.

## Stop conditions (inherited, unchanged)

- Any request to execute WP-V / KVM2 / master merge / ARM / credentials / broker / orders /
  economic action without an explicit named lift.
- Any finding that would require a **product repair** (would change the frozen SHA → re-audit
  picture). This unit found none.
- Any attempt to edit `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` on the strength of the withdrawn
  G4 claim.
- Any citation of documentation-checkout product blobs as candidate behaviour.

**Round-2 additions:**

- ⛔ Any use of `40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3` as a candidate,
  payload, or host lock value — including as a preregistered PASS predicate against
  `/etc/mtc-bridge/install_manifest.json` or `RELEASE_SHA256SUMS`. A mismatch produced that way is a
  **documentation error, not lock drift**, and must not be escalated as a STOP.
- ⛔ Any hash recorded in a post-Gate record without stating what was hashed (blob object ID vs raw
  blob content vs worktree checkout), or derived by hashing a file out of a Windows working tree.
- ⛔ Any assumption that the gated steady profile inherits the first-start unit's
  `MTC_BRIDGE_START_MODE=credential_free_disarmed` pin. It does not (§6.7b).

**Round-3 additions:**

- ⛔ Any statement that the installed `/opt/mtc-bridge/…/requirements.lock`, or
  `/etc/mtc-bridge/install_manifest.json` → `requirements_lock_sha256`, **is** `a1881296…` as an
  observed fact, without a captured read-only host read recorded with its command and output. The
  accurate status is **expected `a1881296…`, unobserved** (§2.7g).
- ⛔ Any automatic disposition of a future host mismatch **against `a1881296…`** — neither
  "documentation error" nor "lock drift" may be assumed; both sides are investigated read-only before
  any STOP is escalated or dismissed. (Round 2's automatic-documentation-error disposition applies
  only to a mismatch produced by the withdrawn `40873556…`.)
- ⛔ Any host read — including the read-only one that would close §2.7g — performed without the named
  authority/budget lift required by §1.

---

## Routing record

```
Classification      : Tier 4, protected Bridge evidence provenance repair; documentation only.
Protected           : yes — Bridge deployment/runtime/persistence/restart/egress evidence surface.
Model + provider    : claude-opus-5, effort xhigh, fresh independent implementer session.
Refs                : documentation HEAD 851d2aa5 (detached, clean); frozen candidate
                      2ce41e34bceb599d80af24c5c33d835820ec321b (unchanged); merge base 4d2228cf.
Exact paths         : writes — MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md (new),
                               MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md (repair in place).
                      reads  — read-only Git at both refs: rev-parse, merge-base, cat-file, grep, show, diff --stat, status.
Commands            : read-only Git only. No SSH/sudo/systemctl/reboot/service/test/package/
                      network/broker/exchange/credential/ARM/order/staging-host command.
                      No Git mutation of any kind.
Product change      : none. No candidate change; no product/deploy/test file written.
Memory/handoff      : none in this unit. Gate-7 write-back belongs to the Lead after acceptance.
Context/tool budget : targeted candidate-qualified greps only; no broad repo scan.
External API credits: no paid API; subscription route only.
```

## 10. Round-2 routing record (2026-08-09)

```
Classification      : Tier 4, protected Bridge evidence provenance repair, round 2; documentation only.
Protected           : yes — same surface. Same two-file write scope, no widening.
Model + provider    : claude-opus-5, effort xhigh, fresh independent implementer session.
Repaired commit     : f8a6bc0f1a7fa00fcd1637297e05424732386da7 (clean worktree C:\PGR).
Refs                : documentation HEAD f8a6bc0f (detached, clean; round-1 HEAD 851d2aa5 — no
                      product-blob drift between them, §2.8);
                      frozen candidate 2ce41e34bceb599d80af24c5c33d835820ec321b (UNCHANGED);
                      merge base 4d2228cf8985ce755c398cceff23f777a99d5404, divergence re-proven.
Defects repaired    : (1) lock byte provenance — 40873556… (Windows CRLF worktree checkout) was
                          recorded as the candidate lock blob SHA-256 and declared exempt from
                          re-derivation; corrected to blob ID 47f53fa2… + content SHA-256
                          a1881296… (§2.7, §4.1, §6.3, §8);
                      (2) remaining candidate qualification — bare product/deploy/tool citations
                          left unqualified by round 1 (§6.7), incomplete blob tables (§4.1/§4.2),
                          and the conflation of ref-invariance with line-number coincidence (§5.1).
Corrections applied : header refs + round-2 superseding block; §1.3 impact row; §2.7 lock byte
                      provenance reproduction; §2.8 doc-branch drift check; §4.1 ref-invariant set
                      4→9 with corrected lock statement; §4.2 exact both-side IDs for all differing
                      paths; §5.1 coincidence vs ref-invariance; §6.3 SECURITY_BASELINE lock
                      identity corrected (637307e8 carries the same blob); §6.7 anchors (a)–(h)
                      incl. the steady-profile start-mode asymmetry; §8 checklist; §9 steps 1, 2, 5a;
                      stop conditions. Matrix repaired in parallel (see its round-2 addendum).
Commands            : read-only Git only (rev-parse, merge-base, cat-file, ls-files --eol, grep,
                      config --get, status) plus local sha256sum/wc over the worktree lock file.
                      No SSH/sudo/systemctl/reboot/service/test/package-install/network/broker/
                      exchange/credential/ARM/order/staging-host command. No Git mutation. No commit.
Product change      : none. No candidate change; no product/deploy/test file written.
Files written       : exactly two — this record and
                      GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md.
Out of scope        : NEXT_SESSION_HANDOFF_2026-08-08.md, _AI_MEMORY/GLOBAL_HANDOFF.md,
                      _AI_MEMORY/NEXT_STEPS.md — each carries both errors; handed to the Lead (§9.2).
Memory/handoff      : none in this unit; Gate-7 write-back belongs to the Lead after acceptance.
External API credits: no paid API; subscription route only.
```

## 11. Round-3 routing record (2026-08-09)

```
Classification      : Tier 4, protected Bridge evidence provenance repair, round 3; documentation only.
Protected           : yes — same surface. Same two-file write scope, no widening.
Model + provider    : claude-opus-5, effort xhigh, fresh independent implementer session.
Repaired at         : documentation HEAD f8a6bc0f1a7fa00fcd1637297e05424732386da7, worktree C:\PGR,
                      with the round-1/round-2 edits present as uncommitted changes to these two
                      files only. Nothing committed or staged; no Git mutation of any kind.
Refs                : frozen candidate 2ce41e34bceb599d80af24c5c33d835820ec321b (UNCHANGED).
Defect repaired     : rounds 1-2 recorded a source-derived expectation as an observed host fact —
                      "the installed lock therefore hashes to a1881296…", attributed to
                      /etc/mtc-bridge/install_manifest.json → requirements_lock_sha256. No Gate-A
                      evidence located in this repair records the observed installed-lock SHA-256 or
                      the host manifest value.
Retained            : a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e as the correct
                      EXPECTED source/payload byte hash for the LF archive (re-derived this round:
                      git cat-file blob 47f53fa2… | sha256sum; git cat-file -s → 117762).
                      40873556… stays withdrawn; blob ID 47f53fa2… stays ref-invariant; counts
                      56 / 1345 stand; G4 stays withdrawn; WP0 stays uneditable.
Now open            : observed installed-host lock hash — NOT IN EVIDENCE; closable by one authorised
                      read-only host read; blocked by the §1 authority/budget hold (§2.7g, §9.2a).
Corrections applied : header refs; round-3 superseding block; round-2 block sentences qualified;
                      §1.3 impact row; §2.7(e) scope note and conclusion; §2.7(g) NEW (the negative
                      evidence enumeration); §3 source-split row + epistemic-status corollary;
                      §4.1 boundary note; §6.3 source-side precision; §8 round-3 checklist incl. two
                      new open items; §9 step 2 qualifier and NEW step 2a; stop conditions;
                      this record. Matrix repaired in parallel (see its round-3 addendum).
Commands            : read-only Git only (rev-parse, cat-file blob/-s) plus local read-only content
                      search over MTC_COMMAND_CENTER and one read of the ref-invariant install.sh.
                      No SSH/sudo/systemctl/reboot/service/test/package-install/network/broker/
                      exchange/credential/ARM/order/staging-host command. No host contacted.
                      No Git mutation. No commit.
Product change      : none. No candidate change; no product/deploy/test file written.
Files written       : exactly two — this record and
                      GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md.
Memory/handoff      : none in this unit; Gate-7 write-back belongs to the Lead after acceptance.
External API credits: no paid API; subscription route only.
```
