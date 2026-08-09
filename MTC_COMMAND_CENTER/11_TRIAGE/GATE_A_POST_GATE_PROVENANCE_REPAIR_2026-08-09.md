# Gate A — Post-Gate Provenance Repair (candidate vs documentation source split)

- **Date:** 2026-08-09.
- **Unit type:** Bounded **documentation-only** repair on a protected Bridge evidence surface.
  **Read-only / local.** No product, deploy, or test file was modified.
- **Model / route:** `claude-opus-5`, effort `xhigh`, fresh independent implementer session.
- **Documentation / governance HEAD:** `851d2aa56be950fda8a3447fca99b20153110721` (detached).
- **Frozen / deployed product candidate:** `2ce41e34bceb599d80af24c5c33d835820ec321b` (**unchanged**).
- **Merge base:** `4d2228cf8985ce755c398cceff23f777a99d5404`.
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

56 exact-pinned entries, 1345 hash lines — matching the Lead's recorded values.

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

**Rule.** Where a blob is *identical* on both refs, either citation is valid and the fact is
ref-invariant. Where blobs *differ*, only the candidate is admissible for product/deploy/runtime/
test/tool facts, and every path **must** be written commit-qualified as
`2ce41e34…321b:<path>:<line>`. Bare `<path>:<line>` is no longer acceptable in post-Gate evidence.

---

## 4. Candidate-vs-documentation blob table

Blob IDs from `git rev-parse <ref>:<path>`; all paths under `IBKR_PAPER_BRIDGE/`.

### 4.1 Identical blobs — ref-invariant, both citations valid

| Path | Blob (both refs) |
|---|---|
| `requirements.lock` | `47f53fa227bf0f18b9bf9bd77e060d8856961728` |
| `deploy/linux/verify_lock.py` | `8ccd6f329154422a85b8e7663e6a079dbd47b4fd` |
| `deploy/linux/rollback.sh` | `4b36674dcb1baa7c3b119cac98f8e6017b1f1566` |
| `deploy/linux/COMMANDS.md` | `3deeefc8da2984d5220482f065e569b74874847a` |

The lock blob being identical is why the Lead's SHA-256
`40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3` (56 entries / 1345 hashes)
**remains valid** and needs no re-derivation.

### 4.2 Differing blobs — candidate only

| Path | Candidate `2ce41e34…321b` | Documentation `851d2aa5` |
|---|---|---|
| `deploy/linux/verify.sh` | `5cfefd709202ff504ae7b7fc3504b8c0b00900b6` | `bce1f0e23e63f9a8d168c751aec99ac84d1334c7` |
| `deploy/linux/systemd/mtc-bridge-first-start.service.template` | `c18232549d96aa200d8c7f796e64de743288940c` | `b175ced7f36df52ad2e55532264f36f49fdc8281` |
| `tools/wal_state_bundle.py` | `26c077e650ab88ba2086efa3a80790769bc055b1` | `aaa2918229a1367ebf1fb6a458a4e65673dc180e` |
| `bridge/app.py` | `572c4178fe804da17601eefd898027e9261492e6` | `6d0abc6351a0d20aef324fb00b936c0f189d036f` |
| `tests/test_partial_fill_protection.py` | differs (contains symbol 11 at :2765) | differs (symbol 11 absent) |
| `tests/test_api.py`, `tests/test_wal_state_bundle.py`, `tests/test_p1_failure_drills.py` | differ (candidate line offsets) | differ |
| `deploy/linux/README.md`, `deploy/linux/env/mtc-bridge.env.template`, `deploy/linux/lib/common.sh` | differ | differ |

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
artifact describing candidate analysis**. Its stated lock identity refers to frozen source
`637307e8` / candidate `1adf9ae5…`, not to `2ce41e34…321b`. The lock *property* (56 exact+hashed
entries; `verify_lock.py` contract) is ref-invariant because the lock blob is byte-identical on both
refs (§4.1), and the candidate lock SHA-256 remains the Lead's
`40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3`.

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

---

## 7. Explicit scope of this unit

| Question | Answer |
|---|---|
| Product defect found? | **No.** The candidate is correct on every point examined; symbol 11 exists, start-mode protections are present and enforced, the WAL tool and verifier behave as documented. |
| Candidate changed? | **No.** `2ce41e34…321b` is untouched. No product, deploy, or test file was written. |
| Staging-host action? | **None.** No SSH, systemctl, sudo, reboot, service, network, broker, credential, ARM, or order command was issued. `GATEA-STAGING` was not contacted. |
| Tests executed? | **None.** All test facts come from `git grep` at the candidate. This is *existence* evidence only, never execution or D026 closure evidence. |
| `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` edited? | **No — and the previously proposed deletion is CANCELLED.** WP0 lines 308 and 364 are correct at the candidate. No replacement symbol is needed. |
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
- [x] Lock re-derived at the candidate: 56 entries / 1345 hashes; blob identity makes the Lead's
      SHA-256 valid unchanged.
- [x] Start-mode enforcement verified at all three layers with candidate line anchors; absence from
      the doc branch verified by empty grep.
- [x] `verify.sh` candidate section map rebuilt; G2's conclusion re-confirmed at the candidate.
- [x] WAL tool subcommand surface and safety mechanics verified at the candidate.
- [x] Egress premise corrected against `bridge/app.py:149`.
- [x] WP0 deletion cancelled; WP0 untouched.
- [x] Exactly two files written; no product/deploy/test file touched; no Git mutation; no host
      command; no test run.
- [ ] **Lead independent acceptance** — re-run §2 commands in a fresh session and confirm.
- [ ] **Gate-7 memory write-back** — Lead only, after acceptance. Not performed in this unit.

---

## 9. Next steps

1. **[Lead]** Independently reproduce §2.2–§2.6 in a fresh session before accepting this repair.
   The single decisive check is
   `git grep -n test_kill_restart_after_request_commit_keeps_killed_and_resumes_once 2ce41e34bceb599d80af24c5c33d835820ec321b -- IBKR_PAPER_BRIDGE/tests`
   → must return `tests/test_partial_fill_protection.py:2765`.
2. **[Lead]** Propagate the correction to the three files carrying the same false claim, which are
   **outside this unit's write scope**:
   - `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md:27`
   - `_AI_MEMORY/GLOBAL_HANDOFF.md:28`
   - `_AI_MEMORY/NEXT_STEPS.md:23`
   Each currently records symbol 11 as an evidence-map problem. Each is wrong for the candidate.
3. **[Lead]** Confirm **no** WP0 edit is made. `WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` is correct.
4. **[AI: Any, local only]** When authoring the run-kit designs (matrix Group B and the C1–C5
   COMMAND GAPs), take every product/deploy/tool line anchor from §5–§6 of this record or re-derive
   it at `2ce41e34…321b`. Do not read product facts from the documentation checkout.
5. **[AI: Any, local only]** Adopt the standing convention: post-Gate evidence cites product facts
   as `2ce41e34…321b:<path>:<line>`. A bare `<path>:<line>` in a post-Gate record should be treated
   as unverified.
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
