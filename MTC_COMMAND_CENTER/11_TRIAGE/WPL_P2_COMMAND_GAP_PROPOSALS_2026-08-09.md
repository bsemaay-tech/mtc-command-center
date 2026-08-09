# WP-L Phase 2 — Command-Gap Proposals for Gate-A Post-Gate Matrix (2026-08-09)

> ## ⚠ STATUS: PROPOSED ONLY — not accepted, not executed, not preregistered.
> **Drafted by subagent (sonnet) under T2 tier; requires Lead review before any use.**
> No command in this document has been run. No host was touched to produce it. No SSH,
> sudo, systemctl, network, staging, or Git command was executed while drafting it — this
> was a read-only documentation task (source files read, one new local file written). Per
> `OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` §2, this is a T2 (docs/prereg text) surface:
> single reviewer, single round, medium effort — **not** the two-flagship T0 bar that
> `deploy/linux/verify.sh`, systemd units, and rollback scripts themselves require. Nothing
> here may be run until (a) a human with the matrix's own authority (§1 of the gap matrix;
> G7/budget was cleared by `OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` §1, and WP-L Phase 2 +
> WP-I staging execution is authorized per `WPL_PHASE2_DISPATCH_PROMPT_2026-08-09.md` — but each
> specific mutating step still follows that dispatch's own gating) is satisfied, and
> (b) a qualified reviewer has checked every path, hash, flag, and citation below against
> the frozen candidate `2ce41e34bceb599d80af24c5c33d835820ec321b` source, not against this
> document.

---

## 0. Scope and sources

This document drafts exact, copy-pasteable command blocks for the **COMMAND GAP** markers in
`GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md` (hereafter "the gap matrix"), in the
Gate-A house style established by the accepted run-kit D/E scripts
(`GATE_A_RUN_KIT_D_2026-08-08/gatea_A7.sh`, `gatea_A8.sh`, `gatea_A9.sh`) and recorded in
`GATE_A_A9_PASS_FINAL_2026-08-09D.md`. Constraints honoured throughout, per the gap matrix and
`OWNER_DECISION_AUDIT_TIERS_2026-08-09.md`:

- The bridge stays **DISARMED and credential-free** in every script below. No script reads
  `/etc/mtc-bridge/mtc-bridge.env` contents, prints a secret, or issues `POST /api/arm`.
- The first-start unit has `Restart=no` and no `[Install]` section; the steady unit is
  gated/inert and also has no `[Install]` (gap-matrix §A4). A reboot **preserves** rather than
  creates mask state (gap-matrix §G1). No script below assumes an auto-start or an auto-restart
  promise.
- The env file cannot override the pinned start mode
  (`2ce41e34…321b:…/verify.sh:143-146` rejects any `MTC_BRIDGE_START_MODE=` assignment in the
  env file) — no script below attempts to set or rely on such an override.
- Any HTTP probe is a loopback-only, GET-only call to `http://127.0.0.1:8790/api/status`
  (never `/api/arm`, never a non-loopback address).
- Candidate identity throughout: **`2ce41e34bceb599d80af24c5c33d835820ec321b`**. All paths and
  line citations below are candidate-qualified per the gap matrix's own G8 mitigation — do not
  re-derive them from the documentation checkout.

**Gaps covered (5 of the 5 requested at minimum).** One further COMMAND GAP marker exists in the
matrix (C5, egress capture) and is explicitly addressed in §6 below as **not safely specifiable**
— it is blocked on an authority class (credentials + broker/TESTNET network access) that this
task's own constraints forbid touching even in draft form.

| # | Gap matrix marker | Predicate | Proposed artifact |
|---|---|---|---|
| 1 | **B3** — "a single bounded post-start permissions-subcheck command is not yet authored" (also the concrete instance of **G2**'s general "bounded subchecks replace a failing full `verify.sh`") | paths/ownership/permissions correct post-start | §2 — `wplp2_B3_permissions.sh` |
| 2 | **C1 / E8** — "no existing verifier that asserts 'no dangling state after SIGTERM'" (WP0 I-R4, OPEN) | clean SIGTERM shutdown, no dangling state | §3 — `wplp2_C1_sigterm_no_dangling.sh` |
| 3 | **C2** — post-reboot DISARMED subcheck, "must be designed first"; **G1**'s two distinct mask scenarios | reboot leaves the bridge DISARMED-by-absence, in the *preregistered* mask state | §4 — `wplp2_C2A_postreboot_unmasked.sh`, `wplp2_C2Bpre_stop_mask.sh`, `wplp2_C2Bpost_postreboot_masked.sh` |
| 4 | **C3** restore-into-temp — "does not exist and must be authored locally" (`wal_state_bundle.py` exposes only `create`/`verify`, no `restore`) | a restored temp copy re-derives the same invariants | §5 — `wplp2_C3restore_wrapper.sh` |
| 5 | **C4** — "the stop+mask-only run-kit step (with the C3 manifest hash wired in) is not yet authored" | rollback stops+masks, preserves state, proves zero writers, no rebind attempted | §6 — `wplp2_C4_rollback_stop_mask.sh` |
| — | **C5** — egress capture, "COMMAND GAP until the separate credential/network authority exists" | TESTNET-only egress, no mainnet | §7 — **not drafted; see reasoning** |

## 1. Shared script contract (every script below)

Identical to the accepted run-kit D/E contract, unchanged:

- `set -Eeuo pipefail`.
- A **fixed, no-clobber evidence log** under `/home/gatea/`: if the log path already exists the
  script refuses to run and exits **2** — this is the *only* meaning of rc 2. It never overwrites
  prior evidence.
- `exec > "$LOG" 2>&1` immediately after the no-clobber check; an `EXIT` trap prints
  `<ID>_TRAP_EXIT rc=<n>` as the last line, whatever the outcome.
- A `fail()` helper: prints `<ID>_FAIL reason=…` and exits **1**. Every assertion failure —
  including a mismatch a human might consider "probably fine" — goes through `fail()`. A script
  ends with exactly `<ID> PASS` on its last content line **only if every assertion held**.
- **rc contract:** `0` = full PASS (last line is `<ID> PASS`); `1` = an assertion failed, or a
  required precondition (unset variable, `mktemp` failure, `sudo` failure) was not met —
  requires Lead adjudication, never auto-dismissed; `2` = the no-clobber guard fired (log path
  already exists) — re-run with a new log name after confirming the prior evidence is intentional.
- **A script never hashes its own still-open log from inside itself.** SHA-256 pairing is a
  separate post-run step, run after the script has exited and the log is closed:
  ```bash
  sha256sum /home/gatea/<log-name>.log
  stat -c '%s' /home/gatea/<log-name>.log
  ```
  Record the remote hash/size, transfer the log, and record the local hash/size identically —
  the same no-clobber + paired-hash convention `GATE_A_A9_PASS_FINAL_2026-08-09D.md` used for
  `gatea-A9-20260808D.log` (remote/local SHA-256 identical, byte count recorded).
- No script reads env-file contents, prints a secret, or issues `POST /api/arm`. Any HTTP call is
  a loopback-only `GET` on `127.0.0.1:8790`.
- **First-FAIL stops.** If any script in a sequence fails, preserve its log, run only read-only
  diagnostics, and stop — do not improvise the next step or auto-retry.

---

## 2. Gap 1 — B3: post-start bounded permissions/ownership subcheck

Replaces the parts of a full `deploy/linux/verify.sh` run that assert filesystem
ownership/permissions (`2ce41e34…321b:…/verify.sh` §2 lines 77–102, §4 lines 123–136). A full
`verify.sh` run is not usable post-start: it also asserts the unit is **masked** and **inactive**
(lines 206–214), which after Gate-A it is neither (Gap G2) — running it whole would produce a
fabricated FAIL. This script asserts only the ownership/mode facts from the filesystem matrix
(`KVM2_PROGRAM/boundaries/IDENTITY_AND_FILESYSTEM.md`) and the gap matrix (§A3/§A4/§B1a), using
read-only `stat`/`find` only — no file content is ever read.

```bash
#!/usr/bin/env bash
# WP-L Phase 2 -- B3 post-start permissions/ownership subcheck (PROPOSED, NOT EXECUTED)
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b (credential-free DISARMED)
# Replaces a full deploy/linux/verify.sh run post-start (Gap G2: verify.sh also asserts
# masked+inactive, so a full run intentionally fails once the service is unmasked/active).
# Read-only stat/find only. No file content is read, no credential value, no POST /api/arm,
# no broker/exchange/order/TESTNET/mainnet/economic action. First genuine FAIL stops.
set -Eeuo pipefail

REL="/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b"
VENV="/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b"
STATE_DIR="/var/lib/mtc-bridge"
LOG_DIR="/var/log/mtc-bridge"
ETC_DIR="/etc/mtc-bridge"
ENV_FILE="/etc/mtc-bridge/mtc-bridge.env"
MANIFEST="/etc/mtc-bridge/install_manifest.json"
UNIT_FILE="/usr/local/lib/systemd/system/mtc-bridge-first-start.service"
LOG="/home/gatea/gatea-WPLP2-B3-20260809.log"

if [[ -e "$LOG" ]]; then
    printf 'ERROR: evidence log already exists (%s); refusing to overwrite\n' "$LOG" >&2
    exit 2
fi

exec > "$LOG" 2>&1

finish() {
    local rc=$?
    printf '\nB3_TRAP_EXIT rc=%s\n' "$rc"
}
trap finish EXIT

fail() {
    printf 'B3_FAIL reason=%s\n' "$*"
    exit 1
}

echo "B3_SECTION header"
echo "B3_candidate=2ce41e34bceb599d80af24c5c33d835820ec321b"
echo "B3_note=read-only stat/find only; no file content read; no POST /api/arm; env file contents not read"

check_path() {
    # args: path expect_owner expect_group expect_mode_regex label
    local p="$1" eo="$2" eg="$3" emre="$4" label="$5"
    if sudo test -L "$p"; then fail "$label ($p) is a symlink"; fi
    sudo test -e "$p" || fail "$label ($p) missing"
    local meta ow gr mo
    meta=$(sudo stat -c '%U %G %a' "$p") || fail "$label ($p) stat failed"
    ow=$(awk '{print $1}' <<<"$meta"); gr=$(awk '{print $2}' <<<"$meta"); mo=$(awk '{print $3}' <<<"$meta")
    echo "B3_stat path=$p owner=$ow group=$gr mode=$mo"
    [[ "$ow" == "$eo" ]] || fail "$label ($p) owner=$ow expected $eo"
    [[ "$gr" == "$eg" ]] || fail "$label ($p) group=$gr expected $eg"
    [[ "$mo" =~ $emre ]]  || fail "$label ($p) mode=$mo does not match /$emre/"
}

echo "B3_SECTION release_tree"
check_path "$REL" root root '^(555|444)$' "release_root"
writable=$(sudo find "$REL" -perm -0200 2>&1) || fail "find over release tree failed"
[[ -z "$writable" ]] || { echo "B3_writable_paths_begin"; printf '%s\n' "$writable"; echo "B3_writable_paths_end"; fail "release tree has a write bit set somewhere"; }

echo "B3_SECTION venv_tree"
check_path "$VENV" root root '^(555|444)$' "venv_root"
venv_writable=$(sudo find "$VENV" -perm -0200 2>&1) || fail "find over venv tree failed"
[[ -z "$venv_writable" ]] || { echo "B3_venv_writable_begin"; printf '%s\n' "$venv_writable"; echo "B3_venv_writable_end"; fail "venv tree has a write bit set somewhere"; }

echo "B3_SECTION state_and_log_dirs"
check_path "$STATE_DIR" mtc-bridge mtc-bridge '^750$' "state_dir"
check_path "$LOG_DIR" mtc-bridge mtc-bridge '^750$' "log_dir"

echo "B3_SECTION etc_dir"
check_path "$ETC_DIR" root root '^750$' "etc_dir"
check_path "$ENV_FILE" root root '^600$' "env_file"
check_path "$MANIFEST" root root '^640$' "install_manifest"

echo "B3_SECTION unit_file"
check_path "$UNIT_FILE" root root '^644$' "installed_unit_file"

echo "B3_SECTION done"
echo "B3 PASS"
```

**PASS:** every `check_path` and every `find -perm -0200` sweep passes; last line is `B3 PASS`.
**FAIL disposition:** any mode/owner/group drift, symlink, or stray write bit is a STOP requiring
Lead adjudication (candidate-repair question, not a documentation outcome) — matches the gap
matrix's own B3 failure disposition ("mode/owner drift = STOP").

---

## 3. Gap 2 — C1: post-SIGTERM no-dangling-state check (WP0 I-R4)

Closes the explicitly OPEN predicate: "no test asserts SIGTERM/lifespan shutdown leaves no
dangling state" (WP0 I-R4, gap-matrix §C1). Uses the unit's own directives
(`KillSignal=SIGTERM` `:48`, `KillMode=mixed` `:49`, `TimeoutStopSec=45` `:51`,
`FinalKillSignal=SIGKILL` `:52`) as the pass/fail boundary: an elapsed stop time at or above 45 s
is itself evidence SIGKILL fired, not a clean SIGTERM exit. **Mutation class: `mutating-host`** —
this script issues one `systemctl stop`; it does **not** perform the separate recovery start
(KVM2-P4-08A/B is a distinct, separately authorised step) and deliberately leaves the unit
stopped afterward.

```bash
#!/usr/bin/env bash
# WP-L Phase 2 -- C1 post-SIGTERM no-dangling-state check (PROPOSED, NOT EXECUTED)
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b (credential-free DISARMED)
# Mutation class: mutating-host (one authorised `systemctl stop`). Requires its own explicit
# authority + budget lift beyond WP-L Phase 2 preparation (gap-matrix §1); PROPOSED ONLY.
# Closes WP0 I-R4 (OPEN). Does NOT perform the separate recovery start (KVM2-P4-08A/B is a
# distinct, separately authorised step) -- the unit is left stopped on exit.
# No credential value is read. Only HTTP call is one loopback GET of /api/status BEFORE the
# stop, for the record -- no POST /api/arm. No broker/exchange/order/TESTNET/mainnet/economic
# action. First genuine FAIL stops.
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
PY="/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python"
DB="/var/lib/mtc-bridge/bridge.db"
LOG="/home/gatea/gatea-WPLP2-C1-20260809.log"

if [[ -e "$LOG" ]]; then
    printf 'ERROR: evidence log already exists (%s); refusing to overwrite\n' "$LOG" >&2
    exit 2
fi

exec > "$LOG" 2>&1

PROCS_FILE=""
finish() {
    local rc=$?
    [[ -n "$PROCS_FILE" && -f "$PROCS_FILE" ]] && rm -f "$PROCS_FILE"
    printf '\nC1_TRAP_EXIT rc=%s\n' "$rc"
}
trap finish EXIT

fail() {
    printf 'C1_FAIL reason=%s\n' "$*"
    exit 1
}

echo "C1_SECTION header"
echo "C1_unit=$UNIT"
echo "C1_candidate=2ce41e34bceb599d80af24c5c33d835820ec321b"
echo "C1_note=one authorised systemctl stop; GET-only loopback probe before stop; no env-file read; no POST /api/arm; recovery start is a separate, later step"

# ---- step 0: pre-stop status (loopback GET only, read-only) --------------------
echo "C1_SECTION step0_pre_stop_status"
pre_out=$(curl -sS --max-time 5 http://127.0.0.1:8790/api/status) || fail "pre-stop GET /api/status failed"
echo "C1_pre_stop_status=$pre_out"
pre_nrestarts=$(systemctl show -p NRestarts --value "$UNIT") || fail "pre-stop NRestarts read failed"
echo "C1_pre_stop_nrestarts=$pre_nrestarts"
[[ "$pre_nrestarts" == "0" ]] || fail "pre-stop NRestarts != 0 ($pre_nrestarts) -- do not proceed"

# ---- step 1: one authorised stop; bounded elapsed time -------------------------
echo "C1_SECTION step1_stop"
t0=$(date +%s)
sudo systemctl stop "$UNIT" || fail "systemctl stop exited nonzero"
t1=$(date +%s)
elapsed=$((t1 - t0))
echo "C1_elapsed_s=$elapsed"
(( elapsed <= 45 )) || fail "stop took ${elapsed}s (>= TimeoutStopSec=45) -- SIGKILL likely fired"

# ---- step 2: systemd's own verdict on how the unit stopped ---------------------
echo "C1_SECTION step2_systemd_verdict"
result=$(systemctl show -p Result --value "$UNIT") || fail "Result read failed"
active=$(systemctl show -p ActiveState --value "$UNIT") || fail "ActiveState read failed"
nrestarts=$(systemctl show -p NRestarts --value "$UNIT") || fail "post-stop NRestarts read failed"
echo "C1_result=$result C1_active=$active C1_nrestarts=$nrestarts"
[[ "$result" == "success" ]] || fail "systemd Result != success ($result) -- abnormal stop (watchdog/timeout/core-dump)"
[[ "$active" == "inactive" ]] || fail "ActiveState != inactive ($active)"
[[ "$nrestarts" == "$pre_nrestarts" ]] || fail "NRestarts changed across stop ($pre_nrestarts -> $nrestarts)"

# ---- step 3: no dangling bridge.app writer, no listener ------------------------
echo "C1_SECTION step3_no_writer_no_listener"
PROCS_FILE=$(mktemp /home/gatea/gatea-C1-procs.XXXXXX) || fail "mktemp failed"
pgrep -af 'bridge\.app' >"$PROCS_FILE" 2>&1 || true
if [[ -s "$PROCS_FILE" ]]; then
    echo "C1_dangling_procs_begin"; cat "$PROCS_FILE"; echo "C1_dangling_procs_end"
    fail "a bridge.app process survived the stop"
fi
listeners=$(ss -H -ltn 'sport = :8790' | wc -l)
echo "C1_listener_count=$listeners"
[[ "$listeners" -eq 0 ]] || fail "control port 8790 still has a listener after stop"

# ---- step 4: DB integrity + app_state, read-only --------------------------------
echo "C1_SECTION step4_db"
db_out=$(sudo "$PY" - "$DB" <<'PYEOF'
import sqlite3, sys
db = sys.argv[1]
con = sqlite3.connect("file:%s?mode=ro" % db, uri=True)
qc = con.execute("PRAGMA quick_check").fetchall()[0][0]
fk = con.execute("PRAGMA foreign_key_check").fetchall()
meta = dict(con.execute("SELECT key, value FROM meta").fetchall())
con.close()
print("db_quick_check=%s" % qc)
print("db_foreign_key_violations=%d" % len(fk))
print("db_app_state=%s" % meta.get("app_state"))
print("db_schema_version=%s" % meta.get("schema_version"))
PYEOF
) || fail "post-stop DB read failed"
printf '%s\n' "$db_out"
db_qc=$(sed -n 's/^db_quick_check=//p' <<<"$db_out")
db_fk=$(sed -n 's/^db_foreign_key_violations=//p' <<<"$db_out")
db_app=$(sed -n 's/^db_app_state=//p' <<<"$db_out")
[[ "$db_qc" == "ok" ]] || fail "post-stop quick_check != ok ($db_qc)"
[[ "$db_fk" == "0" ]] || fail "post-stop foreign_key_check found $db_fk violation(s)"
[[ "$db_app" != "ARMED" ]] || fail "post-stop app_state is ARMED -- must never be ARMED"

echo "C1_SECTION done"
echo "C1 PASS"
```

**PASS:** clean exit ≤45 s, `Result=success`, `NRestarts` unchanged, zero `bridge.app` processes,
zero listeners, `quick_check=ok`, zero FK violations, `app_state != ARMED`.
**FAIL disposition:** timeout-to-SIGKILL, a dangling writer, or invariant drift is a STOP and a
candidate-repair question (matches gap-matrix §C1), not a documentation outcome. **D026:** a new
SIGTERM-shutdown regression test offered as closure must still be shown RED-then-GREEN, per §5 of
the gap matrix — this script is a host proof, not a substitute for that test.

---

## 4. Gap 3 — C2: post-reboot DISARMED subcheck (both mask paths, per G1)

Gap-matrix §C2 requires preregistering **one of two distinct scenarios**, not a single script that
branches at runtime on whatever it finds — a runtime branch would let a wrong assumption slip
through silently. Two independent, fully-specified paths follow:

- **Scenario A** — plain reboot from the current accepted state (active, unmasked). Expected:
  `inactive` + **unmasked**.
- **Scenario B** — a separately authorised pre-reboot `stop`+`mask` step, then reboot. Expected:
  `inactive` + **masked**.

In both scenarios the safety predicate is **DISARMED-by-absence**: no process, no listener, and
persisted DB state not `ARMED`. Per Gap G1, the absence of `[Install]` on either unit template is
**not** treated as a product defect here, and no script below starts the unit to "check" it.

### 4a. Scenario A — post-reboot assertion, expect unmasked

```bash
#!/usr/bin/env bash
# WP-L Phase 2 -- C2-A post-reboot DISARMED subcheck, SCENARIO A: plain reboot from the
# current unmasked/active state (PROPOSED, NOT EXECUTED)
# Expected result: inactive + UNMASKED (no pre-reboot mask step was authorised in this
# scenario). Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b.
# Per Gap G1: the first-start unit has Restart=no and no [Install] section, so it cannot
# auto-start at boot; the steady profile is gated/inert/never installed. This script does
# NOT start the unit, does NOT assume any auto-restart, and does NOT infer a product defect
# from the absence of [Install]. It asserts the state found AFTER an already-authorised,
# separately-performed reboot -- it does not reboot the host itself.
# Read-only only: no service mutation, no credential read, no POST /api/arm. First genuine
# FAIL stops.
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
UNIT_LINK="/etc/systemd/system/${UNIT}"
PY="/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python"
DB="/var/lib/mtc-bridge/bridge.db"
LOG="/home/gatea/gatea-WPLP2-C2A-20260809.log"

if [[ -e "$LOG" ]]; then
    printf 'ERROR: evidence log already exists (%s); refusing to overwrite\n' "$LOG" >&2
    exit 2
fi

exec > "$LOG" 2>&1

PROCS_FILE=""
finish() {
    local rc=$?
    [[ -n "$PROCS_FILE" && -f "$PROCS_FILE" ]] && rm -f "$PROCS_FILE"
    printf '\nC2A_TRAP_EXIT rc=%s\n' "$rc"
}
trap finish EXIT

fail() {
    printf 'C2A_FAIL reason=%s\n' "$*"
    exit 1
}

echo "C2A_SECTION header"
echo "C2A_scenario=A_plain_reboot_expect_unmasked"

echo "C2A_SECTION step1_active_state"
active=$(systemctl show -p ActiveState --value "$UNIT") || fail "ActiveState read failed"
echo "C2A_active=$active"
[[ "$active" == "inactive" ]] || fail "unit is not inactive after reboot (ActiveState=$active) -- unexpected auto-start"

echo "C2A_SECTION step2_mask_state"
enabled=$(systemctl is-enabled "$UNIT" 2>&1) || true
echo "C2A_is_enabled=$enabled"
if sudo test -L "$UNIT_LINK"; then
    target=$(sudo readlink -f "$UNIT_LINK")
    echo "C2A_unit_link_target=$target"
    [[ "$target" != "/dev/null" ]] || fail "unit is masked (symlinked to /dev/null) -- expected unmasked in scenario A"
fi
[[ "$enabled" != "masked" ]] || fail "systemctl is-enabled reports masked -- expected unmasked in scenario A"

echo "C2A_SECTION step3_no_writer_no_listener"
PROCS_FILE=$(mktemp /home/gatea/gatea-C2A-procs.XXXXXX) || fail "mktemp failed"
pgrep -af 'bridge\.app' >"$PROCS_FILE" 2>&1 || true
if [[ -s "$PROCS_FILE" ]]; then
    echo "C2A_dangling_procs_begin"; cat "$PROCS_FILE"; echo "C2A_dangling_procs_end"
    fail "a bridge.app process is running after reboot with no authorised start"
fi
listeners=$(ss -H -ltn 'sport = :8790' | wc -l)
echo "C2A_listener_count=$listeners"
[[ "$listeners" -eq 0 ]] || fail "control port 8790 has a listener after reboot with no authorised start"

echo "C2A_SECTION step4_db"
db_app=$(sudo "$PY" - "$DB" <<'PYEOF'
import sqlite3, sys
con = sqlite3.connect("file:%s?mode=ro" % sys.argv[1], uri=True)
meta = dict(con.execute("SELECT key, value FROM meta").fetchall())
con.close()
print(meta.get("app_state"))
PYEOF
) || fail "post-reboot DB read failed"
echo "C2A_db_app_state=$db_app"
[[ "$db_app" != "ARMED" ]] || fail "persisted app_state is ARMED after reboot"

echo "C2A_SECTION done"
echo "C2A PASS"
```

### 4b. Scenario B — pre-reboot stop+mask, then post-reboot assertion, expect masked

Two scripts: the pre-reboot mutation, run and confirmed PASS *before* the reboot, and the
post-reboot assertion, run *after*.

```bash
#!/usr/bin/env bash
# WP-L Phase 2 -- C2-B-PRE authorised pre-reboot stop+mask (PROPOSED, NOT EXECUTED)
# Must run and PASS before the reboot in Scenario B. Mutation class: mutating-host.
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. No credential read, no POST /api/arm.
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
LOG="/home/gatea/gatea-WPLP2-C2Bpre-20260809.log"

if [[ -e "$LOG" ]]; then
    printf 'ERROR: evidence log already exists (%s); refusing to overwrite\n' "$LOG" >&2
    exit 2
fi

exec > "$LOG" 2>&1

finish() {
    local rc=$?
    printf '\nC2BPRE_TRAP_EXIT rc=%s\n' "$rc"
}
trap finish EXIT

fail() {
    printf 'C2BPRE_FAIL reason=%s\n' "$*"
    exit 1
}

echo "C2BPRE_SECTION header"
sudo systemctl stop "$UNIT" || fail "stop failed"
sudo systemctl mask "$UNIT" || fail "mask failed"
active=$(systemctl show -p ActiveState --value "$UNIT") || fail "ActiveState read failed"
enabled=$(systemctl is-enabled "$UNIT" 2>&1) || true
echo "C2BPRE_active=$active C2BPRE_is_enabled=$enabled"
[[ "$active" == "inactive" ]] || fail "not inactive after stop ($active)"
[[ "$enabled" == "masked" ]] || fail "not masked after mask ($enabled)"

echo "C2BPRE_SECTION done"
echo "C2BPRE PASS"
```

```bash
#!/usr/bin/env bash
# WP-L Phase 2 -- C2-B-POST post-reboot DISARMED subcheck, SCENARIO B: expect masked
# (PROPOSED, NOT EXECUTED). Run only after C2-B-PRE PASSed and the reboot occurred.
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. Read-only only: no service mutation,
# no credential read, no POST /api/arm. First genuine FAIL stops.
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
UNIT_LINK="/etc/systemd/system/${UNIT}"
PY="/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python"
DB="/var/lib/mtc-bridge/bridge.db"
LOG="/home/gatea/gatea-WPLP2-C2Bpost-20260809.log"

if [[ -e "$LOG" ]]; then
    printf 'ERROR: evidence log already exists (%s); refusing to overwrite\n' "$LOG" >&2
    exit 2
fi

exec > "$LOG" 2>&1

PROCS_FILE=""
finish() {
    local rc=$?
    [[ -n "$PROCS_FILE" && -f "$PROCS_FILE" ]] && rm -f "$PROCS_FILE"
    printf '\nC2BPOST_TRAP_EXIT rc=%s\n' "$rc"
}
trap finish EXIT

fail() {
    printf 'C2BPOST_FAIL reason=%s\n' "$*"
    exit 1
}

echo "C2BPOST_SECTION header"
echo "C2BPOST_scenario=B_pre_reboot_mask_expect_masked"

echo "C2BPOST_SECTION step1_active_state"
active=$(systemctl show -p ActiveState --value "$UNIT") || fail "ActiveState read failed"
echo "C2BPOST_active=$active"
[[ "$active" == "inactive" ]] || fail "unit is not inactive after reboot (ActiveState=$active)"

echo "C2BPOST_SECTION step2_mask_state"
enabled=$(systemctl is-enabled "$UNIT" 2>&1) || true
echo "C2BPOST_is_enabled=$enabled"
sudo test -L "$UNIT_LINK" || fail "unit link ($UNIT_LINK) is not a symlink -- expected masked (-> /dev/null) in scenario B"
target=$(sudo readlink -f "$UNIT_LINK")
echo "C2BPOST_unit_link_target=$target"
[[ "$target" == "/dev/null" ]] || fail "unit link target is not /dev/null ($target) -- mask did not survive reboot"
[[ "$enabled" == "masked" ]] || fail "systemctl is-enabled != masked ($enabled) -- expected masked in scenario B"

echo "C2BPOST_SECTION step3_no_writer_no_listener"
PROCS_FILE=$(mktemp /home/gatea/gatea-C2Bpost-procs.XXXXXX) || fail "mktemp failed"
pgrep -af 'bridge\.app' >"$PROCS_FILE" 2>&1 || true
if [[ -s "$PROCS_FILE" ]]; then
    echo "C2BPOST_dangling_procs_begin"; cat "$PROCS_FILE"; echo "C2BPOST_dangling_procs_end"
    fail "a bridge.app process is running after a masked reboot"
fi
listeners=$(ss -H -ltn 'sport = :8790' | wc -l)
echo "C2BPOST_listener_count=$listeners"
[[ "$listeners" -eq 0 ]] || fail "control port 8790 has a listener after a masked reboot"

echo "C2BPOST_SECTION step4_db"
db_app=$(sudo "$PY" - "$DB" <<'PYEOF'
import sqlite3, sys
con = sqlite3.connect("file:%s?mode=ro" % sys.argv[1], uri=True)
meta = dict(con.execute("SELECT key, value FROM meta").fetchall())
con.close()
print(meta.get("app_state"))
PYEOF
) || fail "post-reboot DB read failed"
echo "C2BPOST_db_app_state=$db_app"
[[ "$db_app" != "ARMED" ]] || fail "persisted app_state is ARMED after a masked reboot"

echo "C2BPOST_SECTION done"
echo "C2BPOST PASS"
```

**PASS (either scenario):** the *preregistered* mask state for that scenario, no writer, no
listener, DB state not `ARMED`. **FAIL disposition:** any writer, listener, `ARMED` state, or
mask-state mismatch against the scenario's own prediction is a STOP (matches gap-matrix §C2).

---

## 5. Gap 4 — C3: restore-into-temp wrapper around `wal_state_bundle.py`

`2ce41e34…321b:IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` exposes exactly **two** subcommands
under a required subparser (`:1216`) — `create` (`:1218`) and `verify` (`:1232`). There is **no**
`restore` subcommand, which is exactly why this wrapper is needed (gap-matrix §C3). It must never
invent a subcommand the tool does not have; instead it copies the bundle's own already-`verify`
-PASSed database bytes into an independent temp path and re-derives invariants there using the
tool's own public `collect_invariants` (`:417`), then compares against the invariants hash already
recorded by a prior `verify` PASS.

**Prerequisite (must already exist before this runs):** a `create` (never `--allow-live-source`
for this proof) + `verify` PASS already exists for `$BUNDLE_DIR`, with `EXPECT_BUNDLE_SHA256` /
`EXPECT_INVARIANTS_SHA256` already recorded from that PASS (the C3 capture flow already described
in the gap matrix; this wrapper does not create a manifest, only consumes an already-accepted one).

**Open technical point — flag before use, do not treat as settled.** This wrapper assumes
`collect_invariants(db_path)` returns a JSON-serialisable structure and that hashing
`json.dumps(inv, sort_keys=True, separators=(",", ":"))` reproduces the same
`EXPECT_INVARIANTS_SHA256` the tool's own `verify` subcommand already computed. That
canonicalisation must be confirmed against the actual `verify` implementation at
`2ce41e34…321b:tools/wal_state_bundle.py` before this script is finalised for execution. If the
hash format cannot be matched byte-for-byte, compare the invariants **structurally** (dict
equality) instead of by hash, and treat a hash-format mismatch alone as inconclusive — not as FAIL
evidence of drift. This caveat exists precisely so nobody upgrades an untested assumption into an
observed fact, per the gap matrix's own G10 mitigation.

```bash
#!/usr/bin/env bash
# WP-L Phase 2 -- C3-RESTORE restore-into-temp wrapper around wal_state_bundle.py
# (PROPOSED, NOT EXECUTED). Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b.
# wal_state_bundle.py exposes only `create` and `verify` -- no `restore` subcommand
# (2ce41e34...321b:IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py:1216,:1218,:1232). This
# wrapper proves "restored into a temp copy re-derives the same invariants" by copying the
# bundle's already-verified database bytes into a fresh, independent temp path and
# re-deriving invariants with the tool's own public collect_invariants (:417), then
# comparing against the invariants hash already recorded by `verify`.
# PREREQUISITE: a `create` (never --allow-live-source) + `verify` PASS already exists for
# BUNDLE_DIR, with EXPECT_BUNDLE_SHA256 / EXPECT_INVARIANTS_SHA256 already recorded from
# that PASS. The exact bundle-internal database filename is NOT assumed -- step 1 discovers
# it and FAILS CLOSED on anything other than exactly one match, rather than guessing.
# CAVEAT (see prose above): the invariants-hash canonicalisation used here must be confirmed
# against the tool's own `verify` implementation before this script is finalised.
# Never touches /var/lib/mtc-bridge/bridge.db (the active DB) -- only the bundle copy and a
# temp restore target are read/copied. No credential read, no POST /api/arm. First genuine
# FAIL stops.
set -Eeuo pipefail

PY="/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python"
TOOL="/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py"
RELEASE_ROOT="/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE"
BUNDLE_DIR="${BUNDLE_DIR:?set BUNDLE_DIR to the already-verified bundle directory}"
EXPECT_BUNDLE_SHA256="${EXPECT_BUNDLE_SHA256:?set to the value already recorded by the prior verify PASS}"
EXPECT_INVARIANTS_SHA256="${EXPECT_INVARIANTS_SHA256:?set to the value already recorded by the prior verify PASS}"
LOG="/home/gatea/gatea-WPLP2-C3restore-20260809.log"

if [[ -e "$LOG" ]]; then
    printf 'ERROR: evidence log already exists (%s); refusing to overwrite\n' "$LOG" >&2
    exit 2
fi

exec > "$LOG" 2>&1

TMPDIR2=""
finish() {
    local rc=$?
    [[ -n "$TMPDIR2" && -d "$TMPDIR2" ]] && sudo rm -rf -- "$TMPDIR2"
    printf '\nC3RESTORE_TRAP_EXIT rc=%s\n' "$rc"
}
trap finish EXIT

fail() {
    printf 'C3RESTORE_FAIL reason=%s\n' "$*"
    exit 1
}

echo "C3RESTORE_SECTION header"
echo "C3RESTORE_bundle_dir=$BUNDLE_DIR"

echo "C3RESTORE_SECTION step0_reverify"
"$PY" "$TOOL" verify --bundle-dir "$BUNDLE_DIR" \
    --expect-bundle-sha256 "$EXPECT_BUNDLE_SHA256" \
    --expect-invariants-sha256 "$EXPECT_INVARIANTS_SHA256" \
    || fail "bundle failed re-verification before restore"

echo "C3RESTORE_SECTION step1_locate"
mapfile -t cands < <(find "$BUNDLE_DIR" -maxdepth 1 -type f -name '*.db')
echo "C3RESTORE_candidate_count=${#cands[@]}"
[[ "${#cands[@]}" -eq 1 ]] || fail "expected exactly one *.db file directly under $BUNDLE_DIR, found ${#cands[@]}"
BUNDLE_DB="${cands[0]}"
echo "C3RESTORE_bundle_db=$BUNDLE_DB"
sudo test -f "$BUNDLE_DB" || fail "$BUNDLE_DB is not a regular file"
sudo test -L "$BUNDLE_DB" && fail "$BUNDLE_DB is a symlink"

echo "C3RESTORE_SECTION step2_restore_into_temp"
TMPDIR2=$(mktemp -d /home/gatea/gatea-C3-restore.XXXXXX) || fail "mktemp -d failed"
chmod 700 "$TMPDIR2"
RESTORED_DB="$TMPDIR2/restored.db"
sudo cp --no-clobber -- "$BUNDLE_DB" "$RESTORED_DB" || fail "copy into temp failed"
sudo chown "$(id -u):$(id -g)" "$RESTORED_DB" || true
restored_sha=$(sha256sum "$RESTORED_DB" | awk '{print $1}')
echo "C3RESTORE_restored_sha256=$restored_sha"

echo "C3RESTORE_SECTION step3_reverify_restored"
out=$("$PY" - "$RESTORED_DB" "$RELEASE_ROOT" <<'PYEOF'
import sys, sqlite3, json, hashlib
db_path, release_root = sys.argv[1], sys.argv[2]
sys.path.insert(0, release_root)
from tools.wal_state_bundle import collect_invariants
con = sqlite3.connect("file:%s?mode=ro" % db_path, uri=True)
qc = con.execute("PRAGMA quick_check").fetchall()[0][0]
fk = con.execute("PRAGMA foreign_key_check").fetchall()
con.close()
print("restored_quick_check=%s" % qc)
print("restored_fk_violations=%d" % len(fk))
inv = collect_invariants(db_path)
canon = json.dumps(inv, sort_keys=True, separators=(",", ":")).encode()
print("restored_invariants_sha256=%s" % hashlib.sha256(canon).hexdigest())
PYEOF
) || fail "restored-copy integrity/invariants re-derivation failed"
printf '%s\n' "$out"
r_qc=$(sed -n 's/^restored_quick_check=//p' <<<"$out")
r_fk=$(sed -n 's/^restored_fk_violations=//p' <<<"$out")
r_inv=$(sed -n 's/^restored_invariants_sha256=//p' <<<"$out")
[[ "$r_qc" == "ok" ]] || fail "restored copy quick_check != ok ($r_qc)"
[[ "$r_fk" == "0" ]] || fail "restored copy has $r_fk foreign-key violation(s)"
[[ "$r_inv" == "$EXPECT_INVARIANTS_SHA256" ]] || fail "restored invariants hash mismatch (got $r_inv, expected $EXPECT_INVARIANTS_SHA256) -- see canonicalisation caveat above before escalating"

echo "C3RESTORE_SECTION done"
echo "C3RESTORE PASS"
```

**PASS:** re-`verify` PASS, exactly one candidate db file, restored copy `quick_check=ok`, zero FK
violations, invariants hash matches. **FAIL disposition:** drift/corruption/hash mismatch is a
STOP per gap-matrix §C3 — but per the caveat above, a hash-format mismatch alone must first be
checked against the canonicalisation assumption before being escalated as data drift. **D026:**
the existing `wal_state_bundle` tests remain existing coverage, not new closure evidence for a
newly named defect (gap-matrix §C3, §5).

---

## 6. Gap 5 — C4: rollback stop+mask-only (no rebind)

Uses the candidate's own `deploy/linux/rollback.sh` (blob `4b36674dcb1baa7c3b119cac98f8e6017b1f1566`,
**ref-invariant**) with **neither** `--to-release-sha` **nor** `--to-manifest-sha256` supplied, so
the release-rebind pairing guard (`:65`) is never entered — Gap G3's unmet prerequisite (no second
installed immutable release exists; only `2ce41e34…321b` is installed) does not block this
stop+mask-only proof. `--state-manifest-file` / `--state-manifest-sha256` are hard-required
(`:57-58`); they must be the **same** accepted state-bundle manifest hash already produced and
`verify`-PASSed by the C3 flow — this script does not create a manifest, only consumes an
already-accepted one.

```bash
#!/usr/bin/env bash
# WP-L Phase 2 -- C4 rollback: stop+mask-only, no rebind (PROPOSED, NOT EXECUTED)
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b.
# Uses rollback.sh (blob 4b36674dcb1baa7c3b119cac98f8e6017b1f1566, ref-invariant) with
# NEITHER --to-release-sha NOR --to-manifest-sha256, so the rebind pairing guard (:65) is
# never entered -- Gap G3's unmet prerequisite (no second installed release) does not block
# this stop+mask-only proof. --state-manifest-file / --state-manifest-sha256 are hard-
# required (:57-58) and must be an already-accepted hash from the C3 flow; this script does
# not create a manifest. Mutation class: mutating-host (systemctl stop :82, mask :86). No
# credential read, no POST /api/arm. First genuine FAIL stops.
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
ROLLBACK_SH="/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh"
STATE_MANIFEST_FILE="${STATE_MANIFEST_FILE:?set to the path of the already-accepted state-bundle manifest}"
STATE_MANIFEST_SHA256="${STATE_MANIFEST_SHA256:?set to the already-accepted manifest SHA-256 (from C3)}"
ROLLBACK_MANIFEST="/etc/mtc-bridge/rollback_manifest.json"
STATE_DIR="/var/lib/mtc-bridge"
LOG="/home/gatea/gatea-WPLP2-C4-20260809.log"

if [[ -e "$LOG" ]]; then
    printf 'ERROR: evidence log already exists (%s); refusing to overwrite\n' "$LOG" >&2
    exit 2
fi

exec > "$LOG" 2>&1

PROCS_FILE=""
finish() {
    local rc=$?
    [[ -n "$PROCS_FILE" && -f "$PROCS_FILE" ]] && rm -f "$PROCS_FILE"
    printf '\nC4_TRAP_EXIT rc=%s\n' "$rc"
}
trap finish EXIT

fail() {
    printf 'C4_FAIL reason=%s\n' "$*"
    exit 1
}

echo "C4_SECTION header"
echo "C4_state_manifest_file=$STATE_MANIFEST_FILE"
echo "C4_state_manifest_sha256=$STATE_MANIFEST_SHA256"
echo "C4_note=no --to-release-sha / --to-manifest-sha256 supplied: stop+mask-only, no rebind attempted"

echo "C4_SECTION step0_pre_state_snapshot"
pre_files=$(sudo find "$STATE_DIR" -maxdepth 1 -type f -printf '%f %s\n' | sort)
echo "C4_pre_state_files_begin"; printf '%s\n' "$pre_files"; echo "C4_pre_state_files_end"

echo "C4_SECTION step1_rollback_stop_mask"
sudo "$ROLLBACK_SH" \
    --state-manifest-file "$STATE_MANIFEST_FILE" \
    --state-manifest-sha256 "$STATE_MANIFEST_SHA256" \
    || fail "rollback.sh (stop+mask-only) exited nonzero"

echo "C4_SECTION step2_postcheck"
active=$(systemctl show -p ActiveState --value "$UNIT") || fail "ActiveState read failed"
enabled=$(systemctl is-enabled "$UNIT" 2>&1) || true
echo "C4_active=$active C4_is_enabled=$enabled"
[[ "$active" == "inactive" ]] || fail "unit not inactive after rollback ($active)"
[[ "$enabled" == "masked" ]] || fail "unit not masked after rollback ($enabled)"

PROCS_FILE=$(mktemp /home/gatea/gatea-C4-procs.XXXXXX) || fail "mktemp failed"
pgrep -af 'bridge\.app' >"$PROCS_FILE" 2>&1 || true
if [[ -s "$PROCS_FILE" ]]; then
    echo "C4_dangling_procs_begin"; cat "$PROCS_FILE"; echo "C4_dangling_procs_end"
    fail "a bridge.app process survived rollback stop+mask"
fi
listeners=$(ss -H -ltn 'sport = :8790' | wc -l)
echo "C4_listener_count=$listeners"
[[ "$listeners" -eq 0 ]] || fail "control port 8790 still has a listener after rollback"

echo "C4_SECTION step3_state_preserved"
post_files=$(sudo find "$STATE_DIR" -maxdepth 1 -type f -printf '%f %s\n' | sort)
echo "C4_post_state_files_begin"; printf '%s\n' "$post_files"; echo "C4_post_state_files_end"
[[ "$pre_files" == "$post_files" ]] || fail "state directory file set/sizes changed across rollback"

echo "C4_SECTION step4_rollback_manifest"
sudo test -f "$ROLLBACK_MANIFEST" || fail "$ROLLBACK_MANIFEST was not written"
rm_meta=$(sudo stat -c '%U %G %a' "$ROLLBACK_MANIFEST") || fail "stat on rollback manifest failed"
echo "C4_rollback_manifest_stat=$rm_meta"

echo "C4_SECTION done"
echo "C4 PASS"
```

**PASS:** masked, inactive, no `bridge.app` writer, port closed, state-dir file set unchanged
byte-for-byte, `rollback_manifest.json` written. **FAIL disposition:** a surviving writer or state
loss is a STOP (matches gap-matrix §C4). **D026:** n/a — operational proof, not a regression test.

---

## 7. C5 (egress capture) — not drafted, and why

The gap matrix marks C5 (`api.hyperliquid-testnet.xyz`-only egress, no mainnet, Telegram
disposition) as a **COMMAND GAP** but is explicit that it is **"not a current-unit item"**: at the
candidate, the deployed credential-free DISARMED start mode constructs **no broker at all**
(`2ce41e34…321b:bridge/app.py:149`), so there is no broker egress to capture from the current
staging runtime **at any authority level**. A real capture would require a **different,
separately authorised start mode** plus **credential and broker/TESTNET network authority** — none
of which this task, or the standing budget/authority envelope (§1 of the gap matrix, Gap G7), makes
available.

This proposal deliberately does **not** draft a command for C5, for two independent reasons:

1. **This task's own constraints forbid it.** Any exact command here would necessarily either read
   credential material, select a non-DISARMED start mode, or open outbound broker/exchange network
   access — all explicitly out of bounds for this drafting task ("no credential reads," "no ARM,"
   DISARMED-only).
2. **Drafting it would itself be a small act of scope creep the matrix warns against.** A
   plausible-looking but unauthorised capture procedure, sitting in a proposal file, risks being
   copy-pasted under time pressure before the credential/network authority genuinely exists —
   exactly the failure mode Gate-A's own house rules exist to prevent ("do not improvise… where an
   exact safe command cannot yet be specified, the cell reads COMMAND GAP rather than improvising
   one").

C5 should stay an open COMMAND GAP until a human with explicit credential + broker/TESTNET network
authority scopes it — at which point it needs its own T0-tier two-flagship review
(`OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` §2), not a T2 documentation pass.

---

## 8. What this document is not

- Not an execution record. No script above has run; no host was touched.
- Not a preregistration acceptance. Every log path, flag, and citation must be checked by a Lead
  against the frozen candidate `2ce41e34bceb599d80af24c5c33d835820ec321b` source before any of
  this is treated as ready to run.
- Not an authorisation. Every script marked `mutating-host` (C1, C2-B-PRE, C4) additionally
  requires its own explicit named authority + budget lift per gap-matrix §1 — none of that
  authority is granted by this document.
- Not a change to any existing file. No product code, run-kit script, test, or prior
  preregistration record was edited to produce this proposal.

**Suggested next step (for the Lead, not self-executing):** review this file against the gap
matrix and `2ce41e34…321b` source; if accepted, fold the accepted scripts into a numbered run-kit
package (mirroring `GATE_A_RUN_KIT_D_2026-08-08/`) with its own README, local `bash -n` syntax
validation, and manifest/tar packaging step — before any transfer or execution is even considered.
