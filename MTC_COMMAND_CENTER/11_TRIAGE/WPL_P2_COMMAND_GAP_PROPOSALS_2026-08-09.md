# WP-L Phase 2 — Command-Gap Proposals for Gate-A Post-Gate Matrix (2026-08-09)

> ## ⚠ STATUS: PROPOSED ONLY — not accepted, not executed, not preregistered, not authorized.
>
> **Repair round 3 of at most 3 — the final permitted round** against the accepted repair
> specification `WPL_P2_COMMAND_GAP_PROPOSALS_REPAIR_SPEC_2026-08-09.md` at commit
> `9ac60ac652f4a221316465cdbc24516aa391f5ce`, implementing RP0–RP6 in response to findings
> F1–F9 of `WPL_P2_COMMAND_GAP_PROPOSALS_AUDIT_2026-08-09.md` (the single authorized round-1
> audit of the rejected source proposal `779bd038957a192db47ff7ad68eb51304a2fba46`).
>
> Round 2 repaired the five reproduced findings **R1–R5** of
> `WPL_P2_PROPOSALS_REAUDIT_ROUND1_2026-08-09.md`, which returned REQUEST_CHANGES against the
> round-1 repair at commit `7194b895` (blob `690d40f5cdbb66efd24cf6c63a8bf661cbe961ee`):
> R1 evidence-leaf containment (RP0), R2 C2 post-reboot cgroup/`app_state` postconditions (RP3),
> R3 mandatory candidate re-verification (RP4), R4 fresh verified post-rollback bundle (RP5), and
> R5 dry-run fingerprint adjudication (RP5). R1, R2, R3 and the narrow R5 defect were accepted as
> closed by the round-2 re-audit.
>
> Round 3 repairs exactly the three **content** findings of
> `WPL_P2_PROPOSALS_REAUDIT_ROUND2_2026-08-09.md`, which returned REQUEST_CHANGES against the
> round-2 repair at commit `75ee8912` (blob `9785bf8eba29c52ac61744986800e7f66c8fd6bf`):
> **RR2-2** the R4 post-rollback bundle was still satisfiable by a candidate-valid bundle that
> existed before the rollback (RP5, now split into three separately evidenced stages);
> **RR2-3** the dry-run fingerprint recorded statuses and counts and so could not see a same-count
> writer, listener or cgroup-member replacement (RP0-LIB identity inventories + RP5 stage A); and
> **RR2-4** the preserved round-2 runner hard-coded its create-once identifiers, so its advertised
> one-command rerun contract was false (§8.1, plus a new round-3 runner proven by two consecutive
> full runs). `RR2-1` was commit scope, not document content, and is the Lead's to resolve.
> Nothing else was rewritten, and every item declared BLOCKED in earlier rounds stays BLOCKED.
>
> No block in this document has been run against a host. No host was touched to produce it —
> no SSH, transport, `sudo`, `systemctl`, network, staging, credential, broker or Git-history
> action was taken while repairing it. The only execution performed is the local, host-free
> D026 falsification harness recorded in §8, which runs in a fresh OS temporary root against
> local stubs.
>
> This document is a **design artifact**. It is **not** acceptance, **not** permission to
> extract any block into a runnable file, **not** host authorization, **not** a statement that
> the server is ready, and **not** a closure, reopening or repair of the separate blocked
> `C:\PGRK` design loop. Per `OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` §5 the *repaired
> proposal document* — this file — carries the full **T0-grade** review bar: Lead verification
> with independently reproduced falsifications, then flagship re-audit. Every path, mode, hash,
> flag, status token and API claim below must be re-checked against the frozen candidate
> `2ce41e34bceb599d80af24c5c33d835820ec321b` source, never against this document and never
> against a documentation-branch checkout.

---

## 0. Scope, sources, and block classification

### 0.1 What this covers

Design for the **COMMAND GAP** markers in
`GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md` (hereafter "the gap matrix").
Candidate identity throughout: **`2ce41e34bceb599d80af24c5c33d835820ec321b`**. Candidate blobs
used for every source claim below (frozen in
`WPL_P2_COMMAND_GAP_PROPOSALS_CANDIDATE_ANCHOR_MAP_2026-08-09.md`):

| Candidate path | Git blob |
|---|---|
| `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` | `26c077e650ab88ba2086efa3a80790769bc055b1` |
| `IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh` | `db11010a24edfbb96ba80ec1fbe1db3ff29193c9` |
| `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh` | `5cfefd709202ff504ae7b7fc3504b8c0b00900b6` |
| `IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh` | `4b36674dcb1baa7c3b119cac98f8e6017b1f1566` |
| `.../systemd/mtc-bridge-first-start.service.template` | `c18232549d96aa200d8c7f796e64de743288940c` |

| # | Gap matrix marker | Repair item | Section | Status of this design |
|---|---|---|---|---|
| 1 | **B3** (concrete instance of **G2**) | RP1 | §2 | **EXECUTABLE PROPOSAL BLOCK** |
| 2 | **C1 / E8** (WP0 I-R4) | RP2 | §3 | **BLOCKED** — two open design gaps |
| 3 | **C2** (with **G1**'s two mask scenarios) | RP3 | §4 | **BLOCKED** on the C1-GAP-B baseline method; post-reboot halves are executable proposal blocks that STOP without the baseline |
| 4 | **C3** restore-into-temp | RP4 | §5 | **EXECUTABLE PROPOSAL BLOCK** |
| 5 | **C4** rollback stop+mask-only | RP5 | §6 | **EXECUTABLE PROPOSAL BLOCK** ×3 — stages A/B/C, separately authorized |
| — | **C5** egress capture | RP6 | §7 | **BLOCKED** — authority statement only, no procedure |
| — | shared evidence + predicate bootstrap | RP0 | §1 | **EXECUTABLE PROPOSAL BLOCK** |

### 0.2 Block classification legend — read before reading any fenced block

Every fenced block in this document carries exactly one of these markers on its first line:

- `# ===== BLOCK-ID: <id> ===== [EXECUTABLE PROPOSAL BLOCK]`
  An **API-consistent design block**. Every such block is syntax/import validated — including
  every embedded Python heredoc, which `bash -n` does not look inside; `RP0-LIB`,
  `RP0-BOOTSTRAP`, `RP1-B3`, `RP4-C3`, `RP5-C4A`, `RP5-C4B` and `RP5-C4C` additionally have their
  adjudication exercised locally, RED and GREEN, in a fresh temporary root (§8). `RP3-C2A-POST` and
  `RP3-C2B-POST` are syntax-validated only, because the scenarios they serve are BLOCKED (§4.1).
  None of them is **host-runnable**: no block has been run against `/home/gatea`, a real
  `systemctl`, the candidate `rollback.sh`, or any host, and extracting one into a deployable
  file is a **separate, not-yet-granted authorization**.
- `[BLOCKED DESIGN — NON-RUNNABLE]`
  Requirements expressed deliberately as `text`, never as a command sequence, because at least
  one prerequisite is an unresolved design gap. Converting one of these into commands is a stop
  condition (repair spec §10), not an improvement.

### 0.3 Outcome vocabulary — three outcomes everywhere, never two

Every path, process, systemd and pipeline predicate in this document resolves to exactly one of:

| Outcome | rc | Meaning |
|---|---|---|
| **TRUE** | `0` | The predicate held, on evidence. |
| **FALSE** | `1` | The predicate genuinely did not hold, on evidence. |
| **COULD NOT EVALUATE** | `3` | A tool, permission, parse or status error prevented adjudication. **This is always STOP.** |

A `COULD NOT EVALUATE` is never re-read as FALSE, never re-read as "absent", never re-read as
"no process", and never re-read as "unmasked". Empty output alone never establishes absence.
`|| true` does not appear on any predicate path in this document.

### 0.4 Standing constraints honoured by every block

- The bridge stays **DISARMED and credential-free**. No block reads
  `/etc/mtc-bridge/mtc-bridge.env` contents, prints a secret, or issues `POST /api/arm`.
- The env file cannot override the pinned start mode — the candidate rejects any
  `MTC_BRIDGE_START_MODE=` assignment in the env file (`verify.sh:143-146`). No block attempts
  or relies on such an override.
- The first-start unit has `Restart=no` and **no `[Install]` section** (template `:55`; no
  `^[Install]$` anywhere in the 93-line blob; comment `:11-12` states enable is structurally
  unavailable). The steady unit is gated/inert and never installed. No block below starts,
  enables, unmasks or arms anything.
- Any HTTP probe is loopback-only, `GET`-only, on `http://127.0.0.1:8790/api/status`.
- No block deletes, renames aside, retries in place, or truncates prior evidence.

---

## 1. RP0 — shared evidence channel and predicate bootstrap

Closes **F1** (every proposed evidence log could follow a dangling symlink) and the shared part
of **F9** (process/tool failures collapsed).

### 1.1 What was wrong and what replaces it

The rejected proposal used a **fixed** evidence path under `/home/gatea/` guarded only by
`[[ -e "$LOG" ]]` before `exec > "$LOG" 2>&1`. `-e` is **false** for a dangling symlink, so the
redirection then followed the link and created/truncated its target — destroying evidence
outside the intended path while the document claimed global no-clobber. The replacement is a
**preregistered per-run evidence tree**, allocated create-once, with a canonical non-link parent
proven first.

### 1.2 Preregistration and operator-side transport evidence (design requirement)

```text
[BLOCKED-FREE DESIGN REQUIREMENT — not a command sequence]

Before any remote invocation the operator preregisters, locally and immutably:

  RUNID                 a fresh run identifier, never reused. If allocation fails for any
                        reason the identifier is BURNED: it is never retried in place.
  EV_PARENT             the exact evidence parent path, expected owner:group, expected mode
  EV_RUNKIT             the exact runkit directory, expected owner:group, expected mode
  EV_STAGE_ID           the stage identifier that names the single evidence leaf
  expected SHA-256 of every proposed block that the stage will carry

The transport itself is evidence. The operator-side transport record MUST capture, from the
first byte and independently of anything the remote side writes:

  - the exact remote argv actually sent,
  - the complete transport stdout,
  - the complete transport stderr,
  - the transport exit status.

Reason: every failure BEFORE remote evidence allocation succeeds is invisible to a remote-only
log. Those failures are exactly the ones that decide whether the run ID is burned.

This document does not contain a transport command line. Transport is a separate authorization.
```

### 1.3 Shared library — three-outcome predicates

```bash
# ===== BLOCK-ID: RP0-LIB ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 — shared evidence + predicate bootstrap library (PROPOSED DESIGN).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b (credential-free DISARMED).
# NOT host-authorized. Definitions only: sourcing this block performs no filesystem,
# service, network, credential or economic action.
#
# rc contract for every predicate defined here:
#   0 = TRUE   1 = FALSE   3 = COULD NOT EVALUATE (always STOP)
RP0_STOP_RC=3

rp0_stop() { printf 'RP0_STOP reason=%s\n' "$*" >&2; return "$RP0_STOP_RC"; }
rp0_fail() { printf 'RP0_FAIL reason=%s\n' "$*" >&2; return 1; }
rp0_note() { printf 'RP0_NOTE %s\n' "$*"; }

# --- monotonic clock -------------------------------------------------------
# Wall-clock seconds are not a bound. /proc/uptime is monotonic; if it cannot be
# read, elapsed time COULD NOT BE EVALUATED and the caller must STOP.
rp0_monotonic_ms() {
    local up rest
    read -r up rest < /proc/uptime || { rp0_stop "monotonic_clock_unreadable"; return 3; }
    LC_ALL=C awk -v u="$up" 'BEGIN { printf "%.0f\n", u * 1000 }'
}

# --- three-outcome path classification -------------------------------------
# Prints exactly one of: absent regular dir link_live link_dangling other
# rc 0 = classified, rc 3 = COULD NOT EVALUATE. A probe error is NEVER "absent",
# and a dangling link is NEVER "absent" — that conflation was defect F1.
# `stat` without -L does not dereference, so a dangling link is still classified.
rp0_probe_path() {
    local p="$1" kind rc=0 err detail
    err="$(mktemp)" || { rp0_stop "probe_tempfile_failed path=$p"; return 3; }
    kind="$(LC_ALL=C stat -c '%F' -- "$p" 2>"$err")" || rc=$?
    if [ "$rc" -eq 0 ]; then
        case "$kind" in
            "symbolic link")
                rc=0
                LC_ALL=C stat -L -c '%F' -- "$p" >/dev/null 2>"$err" || rc=$?
                if [ "$rc" -eq 0 ]; then printf 'link_live\n'; rm -f "$err"; return 0; fi
                detail="$(tr -d '\r\n' <"$err")"; rm -f "$err"
                case "$detail" in
                    *"No such file or directory"*) printf 'link_dangling\n'; return 0 ;;
                esac
                rp0_stop "link_target_probe_error path=$p rc=$rc detail=$detail"; return 3 ;;
            "regular file"|"regular empty file") printf 'regular\n'; rm -f "$err"; return 0 ;;
            "directory")                         printf 'dir\n';     rm -f "$err"; return 0 ;;
            *)                                   printf 'other\n';   rm -f "$err"; return 0 ;;
        esac
    fi
    detail="$(tr -d '\r\n' <"$err")"; rm -f "$err"
    case "$detail" in
        *"No such file or directory"*) printf 'absent\n'; return 0 ;;
    esac
    rp0_stop "path_probe_error path=$p rc=$rc detail=$detail"
    return 3
}

# --- canonical non-link parent with preregistered owner/mode ---------------
# args: <path> <expected owner:group> <expected octal mode>
rp0_require_canonical_dir() {
    local p="$1" want_own="$2" want_mode="${3#0}" kind canon own mode
    kind="$(rp0_probe_path "$p")" || return 3
    case "$kind" in
        dir) : ;;
        absent)                  rp0_fail "evidence_parent_absent path=$p"; return 1 ;;
        link_live|link_dangling) rp0_fail "evidence_parent_is_symlink kind=$kind path=$p"; return 1 ;;
        *)                       rp0_fail "evidence_parent_kind=$kind path=$p"; return 1 ;;
    esac
    canon="$(readlink -f -- "$p")" || { rp0_stop "canonicalization_failed path=$p"; return 3; }
    [ "$canon" = "$p" ] || { rp0_fail "evidence_parent_not_canonical path=$p canonical=$canon"; return 1; }
    own="$(LC_ALL=C stat -c '%U:%G' -- "$p")" || { rp0_stop "owner_probe_failed path=$p"; return 3; }
    mode="$(LC_ALL=C stat -c '%a' -- "$p")"   || { rp0_stop "mode_probe_failed path=$p"; return 3; }
    [ "$own" = "$want_own" ]   || { rp0_fail "evidence_parent_owner=$own expected=$want_own path=$p"; return 1; }
    [ "$mode" = "$want_mode" ] || { rp0_fail "evidence_parent_mode=$mode expected=$want_mode path=$p"; return 1; }
    rp0_note "evidence_parent_ok path=$p owner=$own mode=$mode"
    return 0
}

# --- preregistered identifier must be ONE safe path component --------------
# args: <variable name> <value>
# A run ID or stage ID that carries a separator, `.`, `..`, a leading `-`, or
# any character outside [A-Za-z0-9._-] can place the ACTIVE evidence leaf beside
# or above the directory §1.5 later hashes. Non-empty is not the predicate:
# `EV_STAGE_ID=../escaped` is non-empty and escapes the closed tree, which
# silently defeats the remote/local binding while the run still reports success.
rp0_require_safe_component() {
    local name="$1" val="$2"
    case "$val" in
        ""|"."|"..")       rp0_fail "component_reserved name=$name value=[$val]";     return 1 ;;
        -*)                rp0_fail "component_leading_dash name=$name value=[$val]"; return 1 ;;
        *[!A-Za-z0-9._-]*) rp0_fail "component_charset name=$name value=[$val]";      return 1 ;;
    esac
    rp0_note "component_ok name=$name value=$val"
    return 0
}

# --- prove a derived path is a DIRECT child of the allocated directory -----
# args: <allocated dir> <derived leaf>
# Independent of the string check above, and applied after allocation: the leaf
# must be spelled exactly `<dir>/<basename>`, and its canonical parent must be
# the canonical allocated directory. A symlinked intermediate is therefore
# refused too, even when every literal component looked safe.
rp0_require_leaf_inside() {
    local dir="$1" leaf="$2" base parent canon_dir canon_parent
    base="${leaf##*/}"
    parent="${leaf%/*}"
    [ "$leaf" = "$dir/$base" ] || { rp0_fail "leaf_not_direct_child dir=$dir leaf=$leaf"; return 1; }
    canon_dir="$(readlink -f -- "$dir")"       || { rp0_stop "canonicalization_failed path=$dir";    return 3; }
    canon_parent="$(readlink -f -- "$parent")" || { rp0_stop "canonicalization_failed path=$parent"; return 3; }
    [ "$canon_parent" = "$canon_dir" ] \
        || { rp0_fail "leaf_parent_escapes dir=$canon_dir parent=$canon_parent leaf=$leaf"; return 1; }
    rp0_note "leaf_contained dir=$canon_dir name=$base"
    return 0
}

# --- create-once evidence directory ----------------------------------------
# ONE plain `mkdir -m 0700`. Never `mkdir -p`: a missing intermediate must fail,
# not be silently manufactured. Any non-zero rc is STOP and burns the run ID.
rp0_allocate_evidence_dir() {
    local evdir="$1" out rc=0
    out="$(mkdir -m 0700 -- "$evdir" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        rp0_stop "evidence_allocation_failed dir=$evdir rc=$rc detail=$out run_id_burned=yes"
        return 3
    fi
    rp0_note "evidence_dir_allocated dir=$evdir"
    return 0
}

# --- create-once evidence leaf ---------------------------------------------
# `noclobber` makes the shell open with O_CREAT|O_EXCL, so an existing regular
# file, a LIVE symlink and a DANGLING symlink are all refused with EEXIST. This
# is the exact predicate the rejected `[[ -e "$LOG" ]]` guard did not provide.
# No append, no truncation of an existing path, no rename-aside, no retry.
rp0_open_evidence_leaf() {
    local leaf="$1" rc=0 kind size
    set -o noclobber
    : > "$leaf" || rc=$?
    set +o noclobber
    if [ "$rc" -ne 0 ]; then
        rp0_stop "evidence_leaf_not_creatable leaf=$leaf rc=$rc"; return 3
    fi
    kind="$(rp0_probe_path "$leaf")" || return 3
    [ "$kind" = "regular" ] || { rp0_stop "evidence_leaf_kind=$kind leaf=$leaf"; return 3; }
    size="$(LC_ALL=C stat -c '%s' -- "$leaf")" || { rp0_stop "evidence_leaf_stat_failed leaf=$leaf"; return 3; }
    [ "$size" = "0" ] || { rp0_stop "evidence_leaf_not_empty leaf=$leaf size=$size"; return 3; }
    exec > "$leaf" 2>&1
    return 0
}

# --- pgrep: 0 matched / 1 none / anything else STOP ------------------------
# Defect F9 was `pgrep ... || true` plus "empty temp file means no process".
# rc 2 (syntax/fatal) with empty output then read as "no writer survived".
rp0_pgrep_status() {
    local pat="$1" out rc=0
    out="$(pgrep -af "$pat" 2>&1)" || rc=$?
    case "$rc" in
        0) printf '%s\n' "$out"; return 0 ;;
        1) if [ -n "$out" ]; then rp0_stop "pgrep_rc1_with_output pattern=$pat out=$out"; return 3; fi
           return 1 ;;
        *) rp0_stop "pgrep_status pattern=$pat rc=$rc out=$out"; return 3 ;;
    esac
}

# --- systemctl is-enabled: token and status adjudicated TOGETHER -----------
# Defect F4/F9 was `systemctl is-enabled ... || true`, after which empty or
# error output satisfied `!= masked`. A preregistered token may only PASS when
# the command status is one of the documented token-producing statuses.
# Blank or unparsable output is STOP.
rp0_is_enabled_token() {
    local unit="$1" out rc=0
    out="$(systemctl is-enabled -- "$unit" 2>/dev/null)" || rc=$?
    case "$rc:$out" in
        0:enabled|0:enabled-runtime|0:alias|0:linked|0:linked-runtime|0:generated)
            printf '%s\n' "$out"; return 0 ;;
        1:static|1:masked|1:masked-runtime|1:disabled|1:indirect|1:transient)
            printf '%s\n' "$out"; return 0 ;;
    esac
    rp0_stop "is_enabled_unadjudicable unit=$unit rc=$rc token=[$out]"
    return 3
}

# --- systemctl show: one property, status adjudicated ----------------------
rp0_show_property() {
    local unit="$1" prop="$2" out rc=0
    out="$(systemctl show -p "$prop" --value -- "$unit" 2>/dev/null)" || rc=$?
    if [ "$rc" -ne 0 ]; then rp0_stop "systemctl_show_failed unit=$unit prop=$prop rc=$rc"; return 3; fi
    if [ -z "$out" ]; then rp0_stop "systemctl_show_blank unit=$unit prop=$prop"; return 3; fi
    printf '%s\n' "$out"; return 0
}

# --- systemd cgroup survivors: fail-closed, three outcomes -----------------
# "No writer pattern match and no listener" does NOT prove the unit is empty: a
# process that no longer matches the writer pattern, or that never opened the
# control port, still survives inside the unit's cgroup. Prints the survivor
# count for the whole cgroup SUBTREE. An unreadable property, an unparsable
# property line, a walk error, `find` stderr with rc 0, or an unreadable
# `cgroup.procs` is COULD NOT EVALUATE — never "0 survivors". Only an explicitly
# empty ControlGroup, or a cgroup directory classified absent, is zero.
rp0_cgroup_survivors() {
    local unit="$1" root="${RP0_CGROUP_ROOT:-/sys/fs/cgroup}"
    local out rc=0 cg dir kind err detail content f total=0
    local -a procfiles=() pids=()
    out="$(systemctl show -p ControlGroup -- "$unit" 2>/dev/null)" || rc=$?
    [ "$rc" -eq 0 ] || { rp0_stop "cgroup_property_failed unit=$unit rc=$rc"; return 3; }
    case "$out" in
        ControlGroup=*) cg="${out#ControlGroup=}" ;;
        *) rp0_stop "cgroup_property_unparsable unit=$unit out=[$out]"; return 3 ;;
    esac
    if [ -z "$cg" ]; then printf '0\n'; return 0; fi
    kind="$(rp0_probe_path "$root")" || return 3
    [ "$kind" = "dir" ] || { rp0_stop "cgroup_root_kind=$kind path=$root"; return 3; }
    dir="$root$cg"
    kind="$(rp0_probe_path "$dir")" || return 3
    case "$kind" in
        absent) printf '0\n'; return 0 ;;
        dir)    : ;;
        *)      rp0_stop "cgroup_dir_kind=$kind path=$dir"; return 3 ;;
    esac
    err="$(mktemp)" || { rp0_stop "cgroup_tempfile_failed unit=$unit"; return 3; }
    rc=0
    out="$(find "$dir" -type f -name cgroup.procs -print 2>"$err")" || rc=$?
    detail="$(tr -d '\r\n' <"$err")"; rm -f "$err"
    [ "$rc" -eq 0 ] || { rp0_stop "cgroup_walk_failed dir=$dir rc=$rc detail=$detail"; return 3; }
    [ -z "$detail" ] || { rp0_stop "cgroup_walk_stderr dir=$dir detail=$detail"; return 3; }
    if [ -n "$out" ]; then mapfile -t procfiles <<<"$out"; fi
    for f in "${procfiles[@]}"; do
        rc=0
        content="$(LC_ALL=C cat -- "$f" 2>/dev/null)" || rc=$?
        [ "$rc" -eq 0 ] || { rp0_stop "cgroup_procs_unreadable file=$f rc=$rc"; return 3; }
        if [ -n "$content" ]; then mapfile -t pids <<<"$content"; total=$(( total + ${#pids[@]} )); fi
    done
    printf '%s\n' "$total"
    return 0
}

# --- pipeline discipline ---------------------------------------------------
# Rule: any pipeline runs under `set -o pipefail` AND its complete component
# status vector (${PIPESTATUS[@]}) is adjudicated; empty output is never
# sufficient. Where a pipeline can be avoided it is avoided — that is strictly
# stronger than adjudicating one. The listener count below uses no pipeline.
rp0_listener_count() {
    local port="$1" raw rc=0
    local -a lines=()
    raw="$(ss -H -ltn "sport = :${port}" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then rp0_stop "ss_status port=$port rc=$rc out=$raw"; return 3; fi
    if [ -n "$raw" ]; then mapfile -t lines <<<"$raw"; fi
    printf '%s\n' "${#lines[@]}"
    return 0
}

# --- identity inventories: a count is NOT an identity ----------------------
# A before/after comparison assembled from statuses and COUNTS cannot see a
# same-count replacement. Swap one bridge writer for another, one listening
# socket for another, or one cgroup member for another, and every status and
# every count stays equal while the host has in fact changed. That is exactly
# how a "nothing was mutated" claim can be satisfied by a mutated host.
# Each function below therefore emits a CANONICAL, fail-closed INVENTORY that
# identifies the objects themselves. Same three outcomes as every other
# predicate: an inventory that cannot be taken is never rendered as an empty,
# partial or defaulted value, and is never re-read as "nothing there".

# args: <pgrep pattern>
# Prints one `<pid> <full command line>` line per match, LC_ALL=C sorted, or the
# single literal `none`. rc 1 is not an outcome here: "no process matches" is a
# legitimate inventory VALUE, because callers compare inventories, not statuses.
rp0_writer_inventory() {
    local pat="$1" out rc=0 sorted
    out="$(pgrep -af "$pat" 2>&1)" || rc=$?
    case "$rc" in
        0) if [ -z "$out" ]; then rp0_stop "writer_inventory_rc0_empty pattern=$pat"; return 3; fi ;;
        1) if [ -n "$out" ]; then rp0_stop "writer_inventory_rc1_with_output pattern=$pat out=$out"; return 3; fi
           printf 'none\n'; return 0 ;;
        *) rp0_stop "writer_inventory_status pattern=$pat rc=$rc out=$out"; return 3 ;;
    esac
    sorted="$(LC_ALL=C sort <<<"$out")" || { rp0_stop "writer_inventory_sort_failed pattern=$pat"; return 3; }
    printf '%s\n' "$sorted"
    return 0
}

# args: <port>
# Prints one canonical identity line per listening socket, LC_ALL=C sorted, or
# the single literal `none`. `-p` attaches the OWNING process, so a replacement
# behind an unchanged count is visible; a socket line carrying no `users:((…))`
# field means the owner COULD NOT BE DETERMINED, which is rc 3 — never "the same
# listener as before". Recv-Q/Send-Q are deliberately dropped: they are live
# queue gauges, not identity, and comparing them would report a benign
# accept-queue movement as a mutation. No pipeline is used.
rp0_listener_inventory() {
    local port="$1" raw rc=0 line st rq sq loc peer rest ident acc sorted
    local -a lines=()
    raw="$(ss -H -ltnp "sport = :${port}" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then rp0_stop "listener_inventory_status port=$port rc=$rc out=$raw"; return 3; fi
    if [ -z "$raw" ]; then printf 'none\n'; return 0; fi
    mapfile -t lines <<<"$raw"
    acc=""
    for line in "${lines[@]}"; do
        case "$line" in
            *users:*) : ;;
            *) rp0_stop "listener_owner_unresolved port=$port line=[$line]"; return 3 ;;
        esac
        st=""; rq=""; sq=""; loc=""; peer=""; rest=""
        read -r st rq sq loc peer rest <<<"$line"
        if [ -z "$st" ] || [ -z "$loc" ] || [ -z "$rest" ]; then
            rp0_stop "listener_line_incomplete port=$port line=[$line]"; return 3
        fi
        ident="state=$st local=$loc peer=$peer owner=$rest"
        acc="${acc}${ident}"$'\n'
    done
    sorted="$(LC_ALL=C sort <<<"${acc%$'\n'}")" \
        || { rp0_stop "listener_inventory_sort_failed port=$port"; return 3; }
    printf '%s\n' "$sorted"
    return 0
}

# args: <unit>
# Prints one `cgroup=<path relative to the root> pid=<pid>` line per member of
# the unit's cgroup SUBTREE, LC_ALL=C sorted, or the single literal `empty`.
# Fail-closed exactly like rp0_cgroup_survivors: an unreadable or unparsable
# property, a walk error, `find` stderr with rc 0, or an unreadable
# `cgroup.procs` is COULD NOT EVALUATE, never "no member". PID identity is the
# membership predicate; a kernel PID recycled onto a different process inside the
# compared window is not distinguished, and that residual is disclosed in §8.7.
# The counting predicate above is left byte-identical rather than refactored to
# share this walk, so its already-exercised falsifications keep standing.
rp0_cgroup_inventory() {
    local unit="$1" root="${RP0_CGROUP_ROOT:-/sys/fs/cgroup}"
    local out rc=0 cg dir kind err detail content f p rel acc sorted
    local -a procfiles=() pids=()
    out="$(systemctl show -p ControlGroup -- "$unit" 2>/dev/null)" || rc=$?
    [ "$rc" -eq 0 ] || { rp0_stop "cgroup_inventory_property_failed unit=$unit rc=$rc"; return 3; }
    case "$out" in
        ControlGroup=*) cg="${out#ControlGroup=}" ;;
        *) rp0_stop "cgroup_inventory_property_unparsable unit=$unit out=[$out]"; return 3 ;;
    esac
    if [ -z "$cg" ]; then printf 'empty\n'; return 0; fi
    kind="$(rp0_probe_path "$root")" || return 3
    [ "$kind" = "dir" ] || { rp0_stop "cgroup_inventory_root_kind=$kind path=$root"; return 3; }
    dir="$root$cg"
    kind="$(rp0_probe_path "$dir")" || return 3
    case "$kind" in
        absent) printf 'empty\n'; return 0 ;;
        dir)    : ;;
        *)      rp0_stop "cgroup_inventory_dir_kind=$kind path=$dir"; return 3 ;;
    esac
    err="$(mktemp)" || { rp0_stop "cgroup_inventory_tempfile_failed unit=$unit"; return 3; }
    rc=0
    out="$(find "$dir" -type f -name cgroup.procs -print 2>"$err")" || rc=$?
    detail="$(tr -d '\r\n' <"$err")"; rm -f "$err"
    [ "$rc" -eq 0 ] || { rp0_stop "cgroup_inventory_walk_failed dir=$dir rc=$rc detail=$detail"; return 3; }
    [ -z "$detail" ] || { rp0_stop "cgroup_inventory_walk_stderr dir=$dir detail=$detail"; return 3; }
    if [ -n "$out" ]; then mapfile -t procfiles <<<"$out"; fi
    acc=""
    for f in "${procfiles[@]}"; do
        rc=0
        content="$(LC_ALL=C cat -- "$f" 2>/dev/null)" || rc=$?
        [ "$rc" -eq 0 ] || { rp0_stop "cgroup_inventory_procs_unreadable file=$f rc=$rc"; return 3; }
        [ -n "$content" ] || continue
        mapfile -t pids <<<"$content"
        rel="${f#"$root"}"
        for p in "${pids[@]}"; do
            [ -n "$p" ] || continue
            acc="${acc}cgroup=${rel} pid=${p}"$'\n'
        done
    done
    if [ -z "$acc" ]; then printf 'empty\n'; return 0; fi
    sorted="$(LC_ALL=C sort <<<"${acc%$'\n'}")" \
        || { rp0_stop "cgroup_inventory_sort_failed unit=$unit"; return 3; }
    printf '%s\n' "$sorted"
    return 0
}
```

### 1.4 Bootstrap sequence

```bash
# ===== BLOCK-ID: RP0-BOOTSTRAP ===== [EXECUTABLE PROPOSAL BLOCK]
# Runs after RP0-LIB is sourced. Preregistered inputs only; nothing is derived
# at run time, nothing is defaulted, nothing is created with `mkdir -p`.
set -Eeuo pipefail

: "${RUNID:?preregistered run identifier is required}"
: "${EV_PARENT:?preregistered evidence parent is required}"
: "${EV_PARENT_OWNER:?preregistered evidence parent owner:group is required}"
: "${EV_PARENT_MODE:?preregistered evidence parent octal mode is required}"
: "${EV_RUNKIT:?preregistered runkit directory is required}"
: "${EV_RUNKIT_OWNER:?preregistered runkit owner:group is required}"
: "${EV_RUNKIT_MODE:?preregistered runkit octal mode is required}"
: "${EV_STAGE_ID:?preregistered stage identifier is required}"

# Non-empty is NOT sufficient. Both identifiers name ONE component each; a
# separator or `..` would put the active evidence leaf outside the tree that
# §1.5 hashes, so the remote/local binding would attest to the wrong bytes.
rp0_require_safe_component RUNID       "$RUNID"       || exit $?
rp0_require_safe_component EV_STAGE_ID "$EV_STAGE_ID" || exit $?

# Parent chain first: canonical, non-link, preregistered owner and mode.
rp0_require_canonical_dir "$EV_PARENT" "$EV_PARENT_OWNER" "$EV_PARENT_MODE" || exit $?
rp0_require_canonical_dir "$EV_RUNKIT" "$EV_RUNKIT_OWNER" "$EV_RUNKIT_MODE" || exit $?

# One-shot create-once allocation; the run ID is burned on any failure.
EV_DIR="$EV_RUNKIT/$RUNID"
rp0_require_leaf_inside "$EV_RUNKIT" "$EV_DIR" || exit $?
rp0_allocate_evidence_dir "$EV_DIR" || exit $?

# Only now may output be redirected, and only into the directory just created,
# after the derived leaf is PROVEN to be a direct child of it.
EV_LOG="$EV_DIR/${EV_STAGE_ID}.log"
rp0_require_leaf_inside "$EV_DIR" "$EV_LOG" || exit $?
rp0_open_evidence_leaf "$EV_LOG" || exit $?

printf 'RP0_EVIDENCE run_id=%s dir=%s leaf=%s\n' "$RUNID" "$EV_DIR" "$EV_LOG"
```

### 1.5 Closing and binding the evidence tree (post-exit, operator-side)

```text
[BLOCKED-FREE DESIGN REQUIREMENT — runs only after the stage process has exited]

A process never hashes its own still-open evidence. After the stage exits and the tree is
closed, the operator hashes the CLOSED TREE externally, remote side and again locally after
transfer, and binds the two:

  find <EV_DIR> -type f -print0 | sort -z | xargs -0 sha256sum   # per-file digests
  find <EV_DIR> -type f -printf '%P %s\n' | sort                 # names and byte counts

Both sides must produce an identical per-file digest set. The pair is recorded against RUNID.
A remote-only or local-only hash is not a binding. Transfer is a separate authorization and no
transport command appears in this document.
```

### 1.6 Required RP0 falsifications

All six are exercised locally in §8: (1) existing regular evidence leaf; (2) dangling evidence
symlink; (3) parent path replaced by a symlink; (4) denied/path-probe error; (5) `pgrep`
synthetic rc `2` with empty output; (6) `systemctl is-enabled` synthetic non-token error with
empty output.

A seventh is required and is also exercised in §8: **(7) evidence-tree escape** — a preregistered
identifier carrying a separator or `..` (`EV_STAGE_ID=../escaped`, and the same for `RUNID`) must
be refused before allocation, so the active leaf can never sit outside the directory §1.5 hashes.
An eighth, **(8) cgroup-survivor evaluation failure**, covers the predicate added for RP3/RP5: an
unreadable or unparsable cgroup property is STOP, never "no survivor".

A ninth is required and is exercised in §8.5: **(9) same-count identity replacement** — one bridge
writer, listening socket or cgroup member replaced by a different one at an unchanged count must
change the inventory, because a status/count comparison cannot see it. The listener inventory must
additionally STOP when a socket line carries no owning-process field, so an unresolvable owner is
never read as "the same listener".

---

## 2. RP1 — B3 bounded post-start permissions/ownership subcheck

Closes **F2**. A full `deploy/linux/verify.sh` run is not usable post-start: it also asserts the
unit is masked and inactive (`verify.sh:207-214`), which after Gate-A it is neither, so a whole
run would produce a fabricated FAIL (Gap G2). This block reproduces only the filesystem
predicates of `verify.sh:79-81`, `:105-106`, `:124-128` and `:129-135`, at **candidate strength**.

### 2.1 What was wrong

| Rejected behaviour | Candidate requirement | Repair |
|---|---|---|
| accepted root mode `^(555\|444)$` | exactly `0555 root:root` (`verify.sh:79,105` via `common.sh:80-93`) | exact `0555 root:root`; `0444` is a mismatch |
| `find ... -perm -0200` (owner-write only) | `find "$root" ! -type l -perm /222 -print -quit` (`common.sh:98`) | candidate `/222` any-write-bit predicate, reproduced verbatim |
| claimed to reproduce `verify.sh:123-136` but never checked the binding at `:129-135` | install manifest must bind **both** the release SHA and the release/payload manifest SHA | both silent fixed-string bindings checked |
| whole-tree `find` called "bounded" | candidate `-quit` only shortens a *failing* sweep | honest: full walk of a clean tree, under a preregistered budget, exceeding it is STOP |
| `find` failure fell through to an empty-PASS | `common.sh:98-100` fails closed | tool failure is STOP, including partial output |

### 2.2 Block

```bash
# ===== BLOCK-ID: RP1-B3 ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 — B3 post-start permissions/ownership subcheck (PROPOSED DESIGN).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Read-only `stat`/`find`/silent `grep` only. No file content is printed, no
# credential value is read, no POST /api/arm, no broker/exchange/order/TESTNET/
# mainnet/economic action. Requires RP0-LIB sourced and RP0-BOOTSTRAP completed.
set -Eeuo pipefail

CAND="2ce41e34bceb599d80af24c5c33d835820ec321b"
REL="/opt/mtc-bridge/releases/$CAND"
VENV="/opt/mtc-bridge/venvs/$CAND"
STATE_DIR="/var/lib/mtc-bridge"
LOG_DIR="/var/log/mtc-bridge"
CONF_DIR="/etc/mtc-bridge"
ENV_FILE="/etc/mtc-bridge/mtc-bridge.env"
INSTALL_MANIFEST="/etc/mtc-bridge/install_manifest.json"
UNIT_FILE="/usr/local/lib/systemd/system/mtc-bridge-first-start.service"

# Preregistered, never derived here:
: "${B3_RELEASE_MANIFEST_SHA256:?preregistered accepted RELEASE_SHA256SUMS sha256 is required}"
: "${B3_SWEEP_BUDGET_S:?preregistered per-tree sweep budget in seconds is required}"

b3_stop() { printf 'B3_STOP reason=%s\n' "$*"; exit 3; }
b3_fail() { printf 'B3_FAIL reason=%s\n' "$*"; exit 1; }

# --- exact mode + owner, candidate strength --------------------------------
# Reproduces candidate common.sh assert_mode_owner (:80-93): exact octal mode and
# exact owner:group. There is no accepted alternative mode.
b3_assert_mode_owner() {
    local p="$1" want_mode="${2#0}" want_own="$3" kind mode own
    kind="$(rp0_probe_path "$p")" || exit 3
    case "$kind" in
        regular|dir) : ;;
        absent)                  b3_fail "missing path=$p" ;;
        link_live|link_dangling) b3_fail "canonical deployment path is a symlink kind=$kind path=$p" ;;
        *)                       b3_fail "unexpected object kind=$kind path=$p" ;;
    esac
    mode="$(LC_ALL=C stat -c '%a' -- "$p")"   || b3_stop "mode_probe_failed path=$p"
    own="$(LC_ALL=C stat -c '%U:%G' -- "$p")" || b3_stop "owner_probe_failed path=$p"
    printf 'B3_stat path=%s owner=%s mode=%s\n' "$p" "$own" "$mode"
    [ "$mode" = "$want_mode" ] || b3_fail "path=$p mode=$mode expected=$want_mode"
    [ "$own"  = "$want_own"  ] || b3_fail "path=$p owner=$own expected=$want_own"
}

# --- candidate any-write-bit sweep, budgeted, fail-closed ------------------
# Candidate common.sh:95-105 predicate, reproduced verbatim:
#     find "$root" ! -type l -perm /222 -print -quit
# `/222` matches ANY write bit (owner, group OR other). `-perm -0200` is
# owner-write-only and silently passes a 0020 or 0002 offender — that was F2.
# Honest cost: `-quit` shortens only a FAILING sweep; a clean tree is a full
# walk. The operator preregisters B3_SWEEP_BUDGET_S; exceeding it is STOP.
b3_assert_no_writable_paths() {
    local root="$1" offenders errf rc=0 t0 t1 elapsed_s
    errf="$(mktemp)" || b3_stop "sweep_tempfile_failed root=$root"
    t0="$(rp0_monotonic_ms)" || exit 3
    offenders="$(find "$root" ! -type l -perm /222 -print -quit 2>"$errf")" || rc=$?
    t1="$(rp0_monotonic_ms)" || exit 3
    if [ "$rc" -ne 0 ]; then
        b3_stop "writable_inventory_failed root=$root rc=$rc detail=$(tr -d '\r\n' <"$errf") partial=[$offenders]"
    fi
    rm -f "$errf"
    elapsed_s=$(( (t1 - t0) / 1000 ))
    printf 'B3_sweep root=%s elapsed_s=%s budget_s=%s\n' "$root" "$elapsed_s" "$B3_SWEEP_BUDGET_S"
    [ "$elapsed_s" -le "$B3_SWEEP_BUDGET_S" ] \
        || b3_stop "sweep_budget_exceeded root=$root elapsed_s=$elapsed_s budget_s=$B3_SWEEP_BUDGET_S"
    [ -z "$offenders" ] || b3_fail "writable path inside immutable tree: $offenders"
    printf 'B3_no_write_bit root=%s\n' "$root"
}

# --- install-manifest binding, silent, three-outcome ----------------------
# Candidate verify.sh:129-135 binds BOTH the candidate release SHA and the
# release/payload manifest SHA. `grep -qsF` prints nothing, so no unrelated
# manifest content reaches the evidence log. rc 0 = bound, rc 1 = not bound,
# any other rc = read/tool error = STOP (never "not bound").
b3_assert_manifest_binding() {
    local manifest="$1" release_sha="$2" manifest_sha="$3" kind rc=0
    kind="$(rp0_probe_path "$manifest")" || exit 3
    [ "$kind" = "regular" ] || b3_fail "install manifest kind=$kind path=$manifest"
    LC_ALL=C grep -qsF -- "\"release_sha\": \"$release_sha\"" "$manifest" || rc=$?
    case "$rc" in
        0) : ;;
        1) b3_fail "install manifest does not bind release_sha" ;;
        *) b3_stop "install_manifest_unreadable path=$manifest grep_rc=$rc" ;;
    esac
    rc=0
    LC_ALL=C grep -qsF -- "\"release_manifest_sha256\": \"$manifest_sha\"" "$manifest" || rc=$?
    case "$rc" in
        0) : ;;
        1) b3_fail "install manifest does not bind release_manifest_sha256" ;;
        *) b3_stop "install_manifest_unreadable path=$manifest grep_rc=$rc" ;;
    esac
    printf 'B3_manifest_binding path=%s bound=both\n' "$manifest"
}

printf 'B3_SECTION header candidate=%s\n' "$CAND"

printf 'B3_SECTION release_tree\n'
b3_assert_mode_owner "$REL" 0555 root:root
b3_assert_no_writable_paths "$REL"

printf 'B3_SECTION venv_tree\n'
b3_assert_mode_owner "$VENV" 0555 root:root
b3_assert_no_writable_paths "$VENV"

printf 'B3_SECTION ancillary_paths\n'
b3_assert_mode_owner "$STATE_DIR"        0750 mtc-bridge:mtc-bridge
b3_assert_mode_owner "$LOG_DIR"          0750 mtc-bridge:mtc-bridge
b3_assert_mode_owner "$CONF_DIR"         0750 root:root
b3_assert_mode_owner "$ENV_FILE"         0600 root:root
b3_assert_mode_owner "$INSTALL_MANIFEST" 0640 root:root
b3_assert_mode_owner "$UNIT_FILE"        0644 root:root

printf 'B3_SECTION manifest_binding\n'
b3_assert_manifest_binding "$INSTALL_MANIFEST" "$CAND" "$B3_RELEASE_MANIFEST_SHA256"

printf 'B3_SECTION done\n'
printf 'B3 PASS\n'
```

**Candidate anchors for each asserted value.** `0555 root:root` release and venv roots —
`verify.sh:79,105`. `/222` sweep — `common.sh:98`, invoked at `verify.sh:80,106`. State/log
`0750 mtc-bridge:mtc-bridge`, conf `0750 root:root`, env `0600 root:root`, install manifest
`0640 root:root` — `verify.sh:124-128`. Manifest binding — `verify.sh:129-135`. Installed unit
`0644 root:root` — the candidate installs it with `install -o root -g root -m 0644`
(`rollback.sh:149`); `verify.sh:156` asserts only that it is a regular file, so this mode claim
rests on the installer anchor, not on `verify.sh`.

**FAIL disposition:** any mode/owner drift, symlink at a canonical deployment path, any write
bit, or a missing binding is a **STOP requiring Lead adjudication** — a candidate-repair
question, not a documentation outcome. **STOP disposition:** any `stat`, `find`, `grep`,
`mktemp` or clock error stops the stage with rc 3; it is never re-read as a PASS.

### 2.3 Required RP1 fixtures

Exercised locally in §8: root mode `0444`; group-writable-only child (`0020`); other-writable-only
child (`0002`); wrong candidate SHA; wrong payload-manifest SHA; unreadable manifest; failed
`find` after emitting partial output; and one ancillary-path mode/owner drift fixture.

---

## 3. RP2 — C1 graceful-stop verification remains **BLOCKED**

Closes **F3** only through prior gap closure. **There is no runnable C1 block in this document,
and adding one is a stop condition.** The rejected proposal's C1 script is removed, not softened.

### 3.1 Why the rejected C1 could not close WP0 I-R4

- It recorded **no protected persistent-state baseline before the stop**, so its post-stop DB
  check proved only integrity and `app_state != ARMED`. Any same-size or otherwise valid change
  to orders, trades, fills, risk days, environments, counts or max IDs passed unnoticed. The
  candidate exposes the exact invariant set at `wal_state_bundle.py:417-467` and its hash at
  `:561-562`; nothing less is a persistence proof.
- Its SIGTERM predicate used `date +%s` (one-second resolution) and accepted exactly 45 s while
  its own prose classified `>= 45` as timeout/SIGKILL evidence.
- It recorded only `Result`, not a preregistered exit tuple, and no bounded journal evidence.
- Source intent is not host proof: the candidate's credential-free shutdown path having no
  engine stop does not establish what a real SIGTERM produced.

### 3.2 The two open gaps

```text
[BLOCKED DESIGN — NON-RUNNABLE]

C1-GAP-A — exact successful shutdown tuple
  The candidate's uvicorn/systemd SIGTERM result must be pinned from the exact locked
  dependency version and the systemd mapping, and the accepted
      ExecMainCode / ExecMainStatus / Result
  tuple must be FROZEN BEFORE any stop is issued.
  Not acceptable as closure: `Result=success` alone; elapsed time alone; a tuple observed
  post-hoc and then declared to have been the expectation.
  The unit template alone cannot close this. KillSignal=SIGTERM (:48), KillMode=mixed (:49),
  TimeoutStopSec=45 (:51), FinalKillSignal=SIGKILL (:52) and Restart=no (:55) bound the
  mechanism; they do not predict the successful exit tuple.

C1-GAP-B — safe active-writer pre-stop baseline
  An exact method must be specified AND INDEPENDENTLY ACCEPTED for capturing the candidate
  `wal_state_bundle` protected invariants while the service is ACTIVE, without using the
  warning-class `--allow-live-source` as proof and without mutating or unsafely locking the
  production database. The baseline must exist BEFORE `systemctl stop`.
  Note the candidate's own constraint: `_connect_readonly` (:342-381) fails closed when the
  source has a hot WAL without a usable `-shm`, and recovering that needs a read-write
  connection under separate owner authorization. A method that ignores this is not safe.

STATUS: both gaps OPEN. No partial PASS exists while either is open. Editing prose cannot
convert them into execution readiness.
```

### 3.3 Future requirements, preserved as non-runnable design

```text
[BLOCKED DESIGN — NON-RUNNABLE — applies only once BOTH gaps above are closed]

A future C1 command design must require, all of them, with three-outcome predicates:

  1. monotonic high-resolution elapsed time STRICTLY BELOW the timeout boundary
     (strictly < 45 s; equality is timeout evidence, not success);
  2. the exact frozen ExecMainCode/ExecMainStatus/Result tuple from C1-GAP-A;
  3. a bounded journal window for the stop, carrying no timeout, SIGKILL or result-signal
     marker; an unreadable or truncated journal is STOP, not absence of markers;
  4. zero bridge.app writers, zero listeners on 127.0.0.1:8790 and zero cgroup survivors,
     each adjudicated with the fail-closed tool statuses of RP0-LIB;
  5. a post-stop quiescent bundle whose protected invariants HASH and FIELDS equal the genuine
     pre-stop baseline of C1-GAP-B, with `app_state` never `ARMED`;
  6. integrity and foreign-key checks run on a SAFE COPY, never on the production database;
  7. no recovery start of any kind inside C1 — KVM2-P4-08A/B remains separate.

Deferred explicit C1 falsification list. This list is NOT exercised in this document because
C1 is blocked; it becomes MANDATORY, RED and GREEN, if and only if both gaps close:

  C1-F1  stop elapsed exactly at the 45 s boundary is rejected, not accepted;
  C1-F2  a one-second-resolution clock is rejected in favour of a monotonic source;
  C1-F3  an exit tuple that differs from the frozen tuple in ANY component fails;
  C1-F4  `Result=success` with a SIGKILL marker present in the journal window fails;
  C1-F5  an unreadable or truncated journal window is STOP, not PASS;
  C1-F6  a same-size, valid mutation of a protected table between baseline and post-stop
         bundle is detected by invariant-hash inequality;
  C1-F7  a missing pre-stop baseline is STOP, never "compare against post-stop only";
  C1-F8  `pgrep` rc 2 with empty output is STOP, never "no writer survived";
  C1-F9  integrity/FK executed against the production database instead of a safe copy fails
         the design review.
```

---

## 4. RP3 — C2 post-reboot DISARMED subcheck (both mask paths, per G1)

Closes **F4** and **F5**. Two **preregistered** scenarios; the scenario is chosen and recorded
**before** the reboot and **never** branched on the state observed afterwards. A runtime branch
lets a wrong assumption pass silently — that was the shape of F4.

### 4.1 Status of this section

```text
[SCENARIO-LEVEL STATUS]

Scenario A — plain reboot, expect inactive + exact `static`, unmasked. TERMINAL branch.
Scenario B — separately authorized pre-reboot stop+mask, then reboot, expect inactive + masked.

BOTH scenarios require a REAL PRE-MUTATION protected-invariant baseline captured while the
service is still active. That capture method is exactly C1-GAP-B and it is OPEN. Therefore:

  * the pre-reboot baseline step of BOTH scenarios is BLOCKED and is not expressed as a command;
  * Scenario B additionally depends on RP2's baseline method for its pre-stop persistence
    predicate, and its stop+mask mutation inherits that block;
  * the POST-REBOOT assertion halves are executable proposal blocks. They require the
    preregistered baseline as an INPUT and STOP when it is absent, so neither scenario can
    produce a PASS while C1-GAP-B is open.

Scenario A is TERMINAL. Reaching C1 afterwards requires a separately authorized recovery start
plus a fresh Stage-B admission; neither is part of C2-A and neither is authorized here.
```

### 4.2 Scenario A — preregistered pre-reboot state and baseline

```text
[BLOCKED DESIGN — NON-RUNNABLE]

Preregistered BEFORE the reboot, and recorded:

  * ActiveState = active
  * is-enabled token = exactly `static`
    (the first-start unit has NO [Install] section, so the unmasked token is `static`.
     "anything except masked" is NOT the predicate — that was F4.)
  * canonical fragment path = /usr/local/lib/systemd/system/mtc-bridge-first-start.service
  * mask path /etc/systemd/system/mtc-bridge-first-start.service: NO object and NO link
  * protected-invariant baseline captured by the C1-GAP-B method  <-- OPEN, BLOCKS THIS STEP

The reboot itself is a separately authorized host mutation. This document issues no reboot.
```

### 4.3 Scenario A — post-reboot assertion

```bash
# ===== BLOCK-ID: RP3-C2A-POST ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 — C2 Scenario A post-reboot assertion (PROPOSED DESIGN).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Read-only: no service mutation, no reboot, no start, no unmask, no credential
# read, no POST /api/arm. Requires RP0-LIB and RP0-BOOTSTRAP. The scenario is
# preregistered; this block NEVER selects a branch from what it observes.
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
FRAGMENT="/usr/local/lib/systemd/system/$UNIT"
MASK_PATH="/etc/systemd/system/$UNIT"
PORT="8790"

: "${C2_SCENARIO:?preregistered scenario identifier is required}"
: "${C2_BASELINE_INVARIANTS_SHA256:?preregistered pre-reboot protected-invariant hash is required}"
: "${C2_BASELINE_INVARIANTS_JSON:?preregistered pre-reboot protected-invariant document is required}"
: "${C2_POST_INVARIANTS_SHA256:?post-reboot invariant hash, produced by the accepted quiescent capture, is required}"
: "${C2_POST_INVARIANTS_JSON:?post-reboot protected-invariant document is required}"
: "${PY:?candidate venv interpreter path is required}"

c2a_stop() { printf 'C2A_STOP reason=%s\n' "$*"; exit 3; }
c2a_fail() { printf 'C2A_FAIL reason=%s\n' "$*"; exit 1; }

[ "$C2_SCENARIO" = "A_plain_reboot_expect_static_unmasked" ] \
    || c2a_fail "wrong preregistered scenario: $C2_SCENARIO"

# The baseline is an INPUT. Its absence is STOP, never "compare post against post".
for f in "$C2_BASELINE_INVARIANTS_JSON" "$C2_POST_INVARIANTS_JSON"; do
    kind="$(rp0_probe_path "$f")" || exit 3
    [ "$kind" = "regular" ] || c2a_stop "invariant_document_kind=$kind path=$f"
done

printf 'C2A_SECTION step1_active_state\n'
active="$(rp0_show_property "$UNIT" ActiveState)" || exit 3
printf 'C2A_active=%s\n' "$active"
[ "$active" = "inactive" ] || c2a_fail "ActiveState=$active expected inactive (unexpected auto-start)"

printf 'C2A_SECTION step2_enablement_and_mask\n'
enabled="$(rp0_is_enabled_token "$UNIT")" || exit 3
printf 'C2A_is_enabled=%s\n' "$enabled"
[ "$enabled" = "static" ] || c2a_fail "is-enabled=$enabled expected exactly static"

frag_kind="$(rp0_probe_path "$FRAGMENT")" || exit 3
[ "$frag_kind" = "regular" ] || c2a_fail "canonical fragment kind=$frag_kind path=$FRAGMENT"

mask_kind="$(rp0_probe_path "$MASK_PATH")" || exit 3
printf 'C2A_mask_path_kind=%s\n' "$mask_kind"
[ "$mask_kind" = "absent" ] || c2a_fail "mask path must be absent as object AND link, found $mask_kind"

printf 'C2A_SECTION step3_no_writer_no_listener\n'
procs=""; prc=0
procs="$(rp0_pgrep_status 'bridge\.app')" || prc=$?
case "$prc" in
    0) printf 'C2A_dangling_procs_begin\n%s\nC2A_dangling_procs_end\n' "$procs"
       c2a_fail "a bridge.app process is running after reboot with no authorised start" ;;
    1) printf 'C2A_writers=0\n' ;;
    *) exit 3 ;;
esac
listeners="$(rp0_listener_count "$PORT")" || exit 3
printf 'C2A_listener_count=%s\n' "$listeners"
[ "$listeners" -eq 0 ] || c2a_fail "control port $PORT has a listener after reboot"

# A cgroup survivor is a THIRD, independent way the unit can still hold a
# process: it need not match the writer pattern and need not hold the port.
# Omitting this check was the gap; the predicate is fail-closed (STOP on any
# unevaluable property, walk or read).
cgsurv="$(rp0_cgroup_survivors "$UNIT")" || exit 3
printf 'C2A_cgroup_survivors=%s\n' "$cgsurv"
[ "$cgsurv" -eq 0 ] || c2a_fail "the unit cgroup still holds $cgsurv process(es) after reboot"

printf 'C2A_SECTION step4_app_state_not_armed\n'
# ABSOLUTE assertion, not a comment and not implied by equality: equality alone
# would happily accept "ARMED before the reboot and ARMED after it".
app_state=""; asrc=0
app_state="$("$PY" - "$C2_POST_INVARIANTS_JSON" <<'PYEOF'
import json, sys
try:
    with open(sys.argv[1], "r", encoding="utf-8") as handle:
        doc = json.load(handle)
except Exception as exc:
    print(f"app_state_document_unreadable: {exc.__class__.__name__}: {exc}", file=sys.stderr)
    raise SystemExit(3)
if not isinstance(doc, dict) or "app_state" not in doc:
    print("app_state_field_missing", file=sys.stderr)
    raise SystemExit(3)
print("" if doc["app_state"] is None else str(doc["app_state"]))
PYEOF
)" || asrc=$?
[ "$asrc" -eq 0 ] || c2a_stop "app_state_unevaluable path=$C2_POST_INVARIANTS_JSON rc=$asrc"
printf 'C2A_app_state=%s\n' "$app_state"
[ "$app_state" != "ARMED" ] || c2a_fail "app_state=ARMED after reboot; the unit must not return armed"

printf 'C2A_SECTION step5_protected_invariant_equality\n'
# EXACT equality of both the candidate invariants hash and the invariant document.
# Presence, size or "recorded" are NOT this predicate; `app_state != ARMED` is a
# separate REQUIRED assertion (step 4) and never a substitute for equality.
[ "$C2_POST_INVARIANTS_SHA256" = "$C2_BASELINE_INVARIANTS_SHA256" ] \
    || c2a_fail "protected invariants hash differs across reboot (baseline=$C2_BASELINE_INVARIANTS_SHA256 post=$C2_POST_INVARIANTS_SHA256)"
cmp -s -- "$C2_BASELINE_INVARIANTS_JSON" "$C2_POST_INVARIANTS_JSON" \
    || c2a_fail "protected invariant documents differ across reboot"
printf 'C2A_invariants_equal=yes sha256=%s\n' "$C2_POST_INVARIANTS_SHA256"

printf 'C2A_SECTION done\n'
printf 'C2A PASS (terminal branch: no recovery start is authorised by this result)\n'
```

### 4.4 Scenario B — pre-reboot stop+mask

```text
[BLOCKED DESIGN — NON-RUNNABLE]

Scenario B's pre-stop persistence predicate depends on RP2's genuine pre-stop baseline method
(C1-GAP-B, OPEN). Its mutations are therefore NOT expressed as commands here. Recorded design:

  * `stop` and `mask` are two SEPARATE, SEPARATELY NAMED mutations, each with its own
    preregistered pre-state, its own authorization, and its own evidence leaf. They are never
    a single fused step.
  * required post-stop/pre-reboot state, adjudicated with the RP0-LIB predicates:
      - ActiveState = inactive
      - mask path /etc/systemd/system/mtc-bridge-first-start.service is a LIVE symlink whose
        RAW target is exactly `/dev/null` (not merely "some link", not merely "resolves
        somewhere") and whose is-enabled token is exactly `masked`
      - zero writers, zero listeners, zero cgroup survivors
  * a post-stop / pre-reboot QUIESCENT protected-invariant baseline is captured and recorded.
    This baseline is the comparison basis after the reboot. The pre-stop baseline is captured
    separately and is what the stop itself is measured against.
  * no start, unmask, recovery or arm action is part of Scenario B.

Because a stop precedes the reboot in this scenario, the post-reboot comparison basis MUST be
the post-stop/pre-reboot quiescent baseline. Comparing post-reboot state against the pre-STOP
baseline would make any change caused by the stop indistinguishable from reboot drift — that
conflation was F5.
```

### 4.5 Scenario B — post-reboot assertion

```bash
# ===== BLOCK-ID: RP3-C2B-POST ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 — C2 Scenario B post-reboot assertion (PROPOSED DESIGN).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Runs only in the preregistered Scenario B, after C2-B-PRE completed and the
# separately authorized reboot occurred. Read-only; no mutation of any kind.
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
MASK_PATH="/etc/systemd/system/$UNIT"
PORT="8790"

: "${C2_SCENARIO:?preregistered scenario identifier is required}"
: "${C2_QUIESCENT_INVARIANTS_SHA256:?post-stop/pre-reboot quiescent invariant hash is required}"
: "${C2_QUIESCENT_INVARIANTS_JSON:?post-stop/pre-reboot quiescent invariant document is required}"
: "${C2_POST_INVARIANTS_SHA256:?post-reboot invariant hash is required}"
: "${C2_POST_INVARIANTS_JSON:?post-reboot invariant document is required}"

c2b_stop() { printf 'C2B_STOP reason=%s\n' "$*"; exit 3; }
c2b_fail() { printf 'C2B_FAIL reason=%s\n' "$*"; exit 1; }

[ "$C2_SCENARIO" = "B_pre_reboot_stop_mask_expect_masked" ] \
    || c2b_fail "wrong preregistered scenario: $C2_SCENARIO"

for f in "$C2_QUIESCENT_INVARIANTS_JSON" "$C2_POST_INVARIANTS_JSON"; do
    kind="$(rp0_probe_path "$f")" || exit 3
    [ "$kind" = "regular" ] || c2b_stop "invariant_document_kind=$kind path=$f"
done

printf 'C2B_SECTION step1_active_state\n'
active="$(rp0_show_property "$UNIT" ActiveState)" || exit 3
printf 'C2B_active=%s\n' "$active"
[ "$active" = "inactive" ] || c2b_fail "ActiveState=$active expected inactive"

printf 'C2B_SECTION step2_mask_survived_reboot\n'
enabled="$(rp0_is_enabled_token "$UNIT")" || exit 3
printf 'C2B_is_enabled=%s\n' "$enabled"
[ "$enabled" = "masked" ] || c2b_fail "is-enabled=$enabled expected exactly masked"

mask_kind="$(rp0_probe_path "$MASK_PATH")" || exit 3
printf 'C2B_mask_path_kind=%s\n' "$mask_kind"
[ "$mask_kind" = "link_live" ] || c2b_fail "mask path kind=$mask_kind expected a live symlink"
raw_target="$(readlink -- "$MASK_PATH")" || c2b_stop "mask_link_read_failed path=$MASK_PATH"
printf 'C2B_mask_raw_target=%s\n' "$raw_target"
[ "$raw_target" = "/dev/null" ] || c2b_fail "mask link raw target=$raw_target expected exactly /dev/null"

printf 'C2B_SECTION step3_no_writer_no_listener\n'
procs=""; prc=0
procs="$(rp0_pgrep_status 'bridge\.app')" || prc=$?
case "$prc" in
    0) printf 'C2B_dangling_procs_begin\n%s\nC2B_dangling_procs_end\n' "$procs"
       c2b_fail "a bridge.app process is running after a masked reboot" ;;
    1) printf 'C2B_writers=0\n' ;;
    *) exit 3 ;;
esac
listeners="$(rp0_listener_count "$PORT")" || exit 3
printf 'C2B_listener_count=%s\n' "$listeners"
[ "$listeners" -eq 0 ] || c2b_fail "control port $PORT has a listener after a masked reboot"

# Third independent survivor class, fail-closed exactly as in Scenario A. A
# masked unit whose cgroup still holds a process is not a DISARMED host.
cgsurv="$(rp0_cgroup_survivors "$UNIT")" || exit 3
printf 'C2B_cgroup_survivors=%s\n' "$cgsurv"
[ "$cgsurv" -eq 0 ] || c2b_fail "the unit cgroup still holds $cgsurv process(es) after a masked reboot"

printf 'C2B_SECTION step4_protected_invariant_equality\n'
# Comparison basis is the POST-STOP / PRE-REBOOT quiescent baseline, never the pre-stop one.
[ "$C2_POST_INVARIANTS_SHA256" = "$C2_QUIESCENT_INVARIANTS_SHA256" ] \
    || c2b_fail "protected invariants hash differs across reboot (quiescent=$C2_QUIESCENT_INVARIANTS_SHA256 post=$C2_POST_INVARIANTS_SHA256)"
cmp -s -- "$C2_QUIESCENT_INVARIANTS_JSON" "$C2_POST_INVARIANTS_JSON" \
    || c2b_fail "protected invariant documents differ across reboot"
printf 'C2B_invariants_equal=yes sha256=%s\n' "$C2_POST_INVARIANTS_SHA256"

printf 'C2B_SECTION done\n'
printf 'C2B PASS (no start, unmask or recovery action is authorised by this result)\n'
```

### 4.6 Required RP3 falsifications

```text
[DEFERRED — these become mandatory RED/GREEN when C1-GAP-B closes and a scenario is authorized]

  C2-F1  failed `systemctl is-enabled` (non-token rc) is STOP, never "not masked";
  C2-F2  blank is-enabled token is STOP, never "not masked";
  C2-F3  a mask-path link resolving to an ARBITRARY target is rejected in both scenarios;
  C2-F4  a DANGLING mask-path link is rejected, and is never read as "absent"/"unmasked";
  C2-F5  an unexpected REGULAR FILE at the mask path is rejected in both scenarios;
  C2-F6  a same-size content mutation of a protected table is caught by invariant inequality;
  C2-F7  the wrong preregistered scenario fails immediately, before any assertion.

C2-F1, C2-F2, C2-F4 and C2-F5 are already closed at the predicate level by the RP0-LIB
falsifications executed in §8 (`rp0_is_enabled_token` and `rp0_probe_path`); the entries above
remain required at the SCENARIO level once a scenario is authorized. C2-F3, C2-F6 and C2-F7 are
scenario-level only and are NOT claimed closed by this document.

  C2-F8  a cgroup survivor is caught in BOTH scenarios even when no writer pattern matches and
         no listener is present, and an unevaluable cgroup property is STOP, never "no survivor";
  C2-F9  `app_state = ARMED` after the reboot fails Scenario A even when the invariant documents
         are equal on both sides.

C2-F8 and C2-F9 are exercised at PREDICATE/BLOCK level in §8.6. That is evidence about the block
text under local stubs; both scenarios remain BLOCKED and neither entry is claimed closed at the
scenario level.
```

---

## 5. RP4 — C3 restore-into-temp verification wrapper

Closes **F6**. The candidate `wal_state_bundle.py` exposes exactly two subcommands under a
required subparser — `create` (`:1218`) and `verify` (`:1232`); there is no `restore`. This
wrapper never invents one.

### 5.1 What was wrong

The rejected wrapper called `collect_invariants(db_path)`. The candidate's public
`collect_invariants` takes an **open `sqlite3.Connection`** (`:417`) and its first operation
reaches `conn.execute` (`:425` via `_table_names` at `:400-402`), so a string argument raises
`AttributeError: 'str' object has no attribute 'execute'` — reproduced in §8. The rejected
wrapper also:

- re-implemented the invariants hash instead of calling public `invariants_hash` (`:561-562`);
- carried an "open technical point" caveat about canonicalization on its PASS path, which was
  both stale — candidate `_canonical_json` at `:212-213` is exactly
  `json.dumps(..., sort_keys=True, separators=(",", ":"))` — and misdirected. **That caveat is
  deleted, not softened: no acknowledged assumption remains on any PASS path in this document.**
- copied bytes with `cp` and called it a restore;
- printed `restored_sha` without ever comparing it;
- deleted the restore directory with `sudo rm -rf` in an EXIT trap on **every** exit, destroying
  the primary artifact on failure.

### 5.2 Design

```python
# ===== BLOCK-ID: RP4-C3 ===== [EXECUTABLE PROPOSAL BLOCK]
"""WP-L Phase 2 — C3 restore-into-temp verification (PROPOSED DESIGN).

Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.

Uses only the candidate's public API. Never invents a `restore` subcommand, never
copies files and calls it a restore, never deletes an artifact, never touches the
production database read-write, never reads a credential, never issues POST /api/arm.

rc contract: 0 = PASS, 1 = FAIL, 3 = COULD NOT EVALUATE (STOP).
"""

import hashlib
import json
import os
import sqlite3
import sys
from pathlib import Path

PASS_RC, FAIL_RC, STOP_RC = 0, 1, 3

# Protected invariant fields, exactly the keys candidate collect_invariants
# returns (wal_state_bundle.py:457-467).
PROTECTED_FIELDS = (
    "schema_version", "app_state", "counts", "open_trades", "live_orders",
    "closed_trades", "max_ids", "environments", "risk_days",
)


class Fail(Exception):
    """A genuine predicate failure."""


class Stop(Exception):
    """Could not evaluate — always stops the stage, never re-read as FAIL."""


def load_candidate_api(release_root: Path):
    """Import the candidate's own public API. No reimplementation of its logic."""
    sys.path.insert(0, str(release_root))
    try:
        from tools.wal_state_bundle import (  # noqa: E402
            BUNDLE_DB_NAME, FORBIDDEN_SIDECARS, MANIFEST_NAME,
            collect_invariants, invariants_hash, verify_bundle,
        )
    except Exception as exc:  # import/tool error is never a FAIL
        raise Stop(f"candidate_api_import_failed: {exc.__class__.__name__}: {exc}") from exc
    return {
        "collect_invariants": collect_invariants,
        "invariants_hash": invariants_hash,
        "verify_bundle": verify_bundle,
        "MANIFEST_NAME": MANIFEST_NAME,
        "BUNDLE_DB_NAME": BUNDLE_DB_NAME,
        "FORBIDDEN_SIDECARS": FORBIDDEN_SIDECARS,
    }


def candidate_verify(api, bundle_dir: Path, expect_bundle_db_sha256: str,
                     expect_invariants_sha256: str, out=print) -> None:
    """Re-verify the accepted bundle with the CANDIDATE's own verification, in
    THIS evaluation, with both exact expected hashes.

    `verify_bundle(bundle_dir, expect_bundle_sha256, expect_invariants_sha256)`
    (wal_state_bundle.py:1125-1205) additionally validates the full manifest
    contract, the manifest integrity hash, the source/arrival snapshot contract,
    the sidecar-hash contract, source and bundle integrity/FK cleanliness, and
    the re-derived invariants. A prior `verify` PASS is a statement about a past
    run; the local checks further down are a partial reimplementation. Neither
    is this predicate, and neither replaces it.

    Fail-closed adjudication: an exception is COULD NOT EVALUATE, and only the
    exact accepted verdict `(0, "VALID")` may proceed. Both expected hashes are
    REQUIRED by the candidate itself: it raises `BundleError` when either is
    missing or is not 64 hex characters.
    """
    try:
        code, report = api["verify_bundle"](
            bundle_dir=bundle_dir,
            expect_bundle_sha256=expect_bundle_db_sha256,
            expect_invariants_sha256=expect_invariants_sha256,
        )
    except Exception as exc:
        raise Stop(f"candidate_verify_unevaluable: {exc.__class__.__name__}: {exc}") from exc
    verdict = report.get("verdict")
    failures = report.get("failures")
    out(f"C3_candidate_verify_rc={code} verdict={verdict} failures={failures}")
    if code != 0 or verdict != "VALID":
        raise Fail(
            f"candidate verify did not return the accepted verdict "
            f"(rc={code} verdict={verdict} failures={failures})"
        )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def identity(path: Path):
    """(device, inode) from lstat — never follows a link."""
    st = os.lstat(path)
    return (st.st_dev, st.st_ino)


def open_readonly(db_path: Path) -> sqlite3.Connection:
    """Open the bundle DB strictly read-only, in the candidate's own URI form
    (`mode=ro`, wal_state_bundle.py:342-381). The source is never mutated."""
    try:
        uri = f"{db_path.resolve().as_uri()}?mode=ro"
        conn = sqlite3.connect(uri, uri=True)
        conn.execute("SELECT name FROM sqlite_master LIMIT 1").fetchone()
    except (OSError, ValueError, sqlite3.Error) as exc:
        raise Stop(f"readonly_open_failed: {exc.__class__.__name__}: {exc}") from exc
    return conn


def restore_into(src_conn: sqlite3.Connection, dst_path: Path) -> sqlite3.Connection:
    """Restore through the EXACT candidate primitive `src_conn.backup(dst_conn)`
    (wal_state_bundle.py:797-806) into a FRESH destination. A file copy is not a
    restore. The destination must not pre-exist as an object OR as a link."""
    if dst_path.is_symlink():
        raise Fail(f"restore destination is a symlink: {dst_path}")
    if dst_path.exists():
        raise Fail(f"restore destination already exists: {dst_path}")
    try:
        dst_conn = sqlite3.connect(str(dst_path))
        src_conn.backup(dst_conn)
        dst_conn.execute("PRAGMA journal_mode=DELETE")
        dst_conn.commit()
    except (OSError, sqlite3.Error) as exc:
        raise Stop(f"backup_failed: {exc.__class__.__name__}: {exc}") from exc
    return dst_conn


def integrity_and_fk(conn: sqlite3.Connection):
    """quick_check and foreign_key_check on the RESTORED connection."""
    try:
        qc = ";".join(str(r[0]) for r in conn.execute("PRAGMA quick_check").fetchall())
        fk = len(conn.execute("PRAGMA foreign_key_check").fetchall())
    except sqlite3.Error as exc:
        raise Stop(f"integrity_probe_failed: {exc.__class__.__name__}: {exc}") from exc
    return qc, fk


def assert_no_sidecars(db_path: Path, forbidden) -> None:
    """No `-wal`/`-shm`/`-journal` beside the bundle or restored database
    (candidate forbidden set, wal_state_bundle.py:87, :568-569)."""
    present = [
        db_path.with_name(db_path.name + suffix).name
        for suffix in forbidden
        if db_path.with_name(db_path.name + suffix).exists()
    ]
    if present:
        raise Fail(f"sidecar present beside {db_path.name}: {','.join(present)}")


def run(source_db: Path, bundle_dir: Path, restore_root: Path, release_root: Path,
        expect_manifest_file_sha256: str, expect_bundle_db_sha256: str,
        expect_invariants_sha256: str, out=print) -> int:
    """One evaluation. Preserves EVERY artifact: nothing is deleted on any path.

    The three `expect_*` arguments are the externally recorded acceptance values
    for this bundle. They are inputs, never read back out of the manifest: a
    manifest cannot attest to its own acceptance.
    """
    api = load_candidate_api(release_root)
    manifest_path = bundle_dir / api["MANIFEST_NAME"]
    bundle_db = bundle_dir / api["BUNDLE_DB_NAME"]

    # 1. External manifest-FILE sha, recorded separately from the hashes the
    #    manifest embeds. A manifest cannot attest to its own file identity.
    if not manifest_path.is_file():
        raise Stop(f"bundle manifest is not a regular file: {manifest_path}")
    actual_manifest_file_sha = sha256_file(manifest_path)
    out(f"C3_manifest_file_sha256={actual_manifest_file_sha}")
    if actual_manifest_file_sha != expect_manifest_file_sha256:
        raise Fail("bundle manifest FILE sha256 does not match the accepted value")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Stop(f"manifest_unreadable: {exc.__class__.__name__}: {exc}") from exc

    expect_bundle_db_sha = manifest["bundle"]["db_sha256"]
    expect_invariants_sha = manifest["invariants_sha256"]
    expect_invariants = manifest["invariants"]

    # 2. The manifest's own hashes must be the externally recorded accepted
    #    ones. Without this, every check below would be self-referential.
    if expect_bundle_db_sha != expect_bundle_db_sha256:
        raise Fail("manifest bundle db_sha256 is not the externally recorded accepted value")
    if expect_invariants_sha != expect_invariants_sha256:
        raise Fail("manifest invariants_sha256 is not the externally recorded accepted value")

    # 3. MANDATORY candidate re-verification, with both exact expected hashes,
    #    BEFORE anything is restored. Nothing below may run if it does not
    #    return the exact accepted verdict.
    candidate_verify(api, bundle_dir, expect_bundle_db_sha256,
                     expect_invariants_sha256, out=out)

    # 4. Bundle DB hash equality, and no sidecar in the bundle root.
    if not bundle_db.is_file() or bundle_db.is_symlink():
        raise Fail(f"bundle database is not a regular file: {bundle_db}")
    actual_bundle_db_sha = sha256_file(bundle_db)
    out(f"C3_bundle_db_sha256={actual_bundle_db_sha}")
    if actual_bundle_db_sha != expect_bundle_db_sha:
        raise Fail("bundle database sha256 does not match the accepted manifest value")
    assert_no_sidecars(bundle_db, api["FORBIDDEN_SIDECARS"])

    # 5. Fresh, no-clobber restore root. NEVER deleted, on any exit path.
    if restore_root.is_symlink():
        raise Fail(f"restore root is a symlink: {restore_root}")
    if restore_root.exists():
        raise Fail(f"restore root already exists: {restore_root}")
    try:
        restore_root.mkdir(mode=0o700)
    except OSError as exc:
        raise Stop(f"restore_root_allocation_failed: {exc.__class__.__name__}: {exc}") from exc
    restored_db = restore_root / "restored.db"

    # 6. Read-only source connection; restore via src_conn.backup(dst_conn).
    src_conn = open_readonly(bundle_db)
    try:
        dst_conn = restore_into(src_conn, restored_db)
    finally:
        src_conn.close()

    try:
        # 7. quick_check and foreign_key_check on the RESTORED connection.
        qc, fk = integrity_and_fk(dst_conn)
        out(f"C3_restored_quick_check={qc}")
        out(f"C3_restored_fk_violations={fk}")
        if qc != "ok":
            raise Fail(f"restored quick_check != ok ({qc})")
        if fk != 0:
            raise Fail(f"restored foreign_key_check found {fk} violation(s)")

        # 8. Candidate public API on the RESTORED CONNECTION, then candidate hash.
        try:
            restored_invariants = api["collect_invariants"](dst_conn)
            restored_hash = api["invariants_hash"](restored_invariants)
        except Exception as exc:
            raise Stop(f"invariant_derivation_failed: {exc.__class__.__name__}: {exc}") from exc
        out(f"C3_restored_invariants_sha256={restored_hash}")
    finally:
        dst_conn.close()

    # 9. Protected equality: the candidate hash AND every protected field.
    if restored_hash != expect_invariants_sha:
        raise Fail("restored invariants hash does not equal the accepted bundle value")
    for field in PROTECTED_FIELDS:
        if restored_invariants.get(field) != expect_invariants.get(field):
            raise Fail(f"protected invariant field differs after restore: {field}")
    out("C3_protected_fields_equal=yes")

    # 10. Identity separation and sidecar absence in the restore root.
    idents = {
        "source": identity(source_db),
        "bundle": identity(bundle_db),
        "restored": identity(restored_db),
    }
    out("C3_identity=" + json.dumps({k: list(v) for k, v in idents.items()}, sort_keys=True))
    if len(set(idents.values())) != 3:
        raise Fail(f"source/bundle/restored are not three distinct files: {idents}")
    assert_no_sidecars(restored_db, api["FORBIDDEN_SIDECARS"])
    out("C3_sidecars_absent=yes")

    out("C3 PASS")
    return PASS_RC


def main(argv) -> int:
    """Artifacts are preserved under distinct labels; nothing is published as
    accepted on a failing path and nothing partial is ever deleted."""
    (source_db, bundle_dir, restore_root, release_root, expect_manifest_file_sha256,
     expect_bundle_db_sha256, expect_invariants_sha256) = argv[1:8]
    try:
        return run(Path(source_db), Path(bundle_dir), Path(restore_root),
                   Path(release_root), expect_manifest_file_sha256,
                   expect_bundle_db_sha256, expect_invariants_sha256)
    except Fail as exc:
        print(f"C3_FAIL reason={exc}")
        print(f"C3_ARTIFACTS_PRESERVED label=failed root={restore_root}")
        return FAIL_RC
    except Stop as exc:
        print(f"C3_STOP reason={exc}")
        print(f"C3_ARTIFACTS_PRESERVED label=stopped root={restore_root}")
        return STOP_RC


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

### 5.3 Prerequisite and disposition

Prerequisite: a candidate `create` **without** `--allow-live-source` already exists for the bundle
directory; the manifest's `source.changed_during_capture` is `false`; and the manifest **file**
SHA-256, the bundle `db_sha256` and the `invariants_sha256` were all recorded externally at
acceptance time. This wrapper consumes an already-accepted bundle; it creates none.

**The prior `verify` PASS is a prerequisite, never the predicate.** A past PASS attests to the
bundle as it was then. Step 3 of the block therefore re-runs the candidate's own
`verify_bundle(bundle_dir, expect_bundle_sha256, expect_invariants_sha256)` **in this evaluation**,
with both externally recorded hashes, and proceeds only on the exact `(0, VALID)` verdict. That
call — not the local checks around it — is what binds the full manifest contract, the manifest
integrity hash, the source/arrival snapshot contract, the sidecar-hash contract, source and bundle
integrity/FK cleanliness and the re-derived invariants. Equivalently at the CLI:
`python -m tools.wal_state_bundle verify --bundle-dir <dir> --expect-bundle-sha256 <db-sha>
--expect-invariants-sha256 <inv-sha>` (`wal_state_bundle.py:1232-1235`), whose rc `0` is the same
verdict, rc `2` is INVALID, and rc `3` is a tool error that must be read as STOP.

FAIL disposition: drift, corruption, hash inequality, identity aliasing or a sidecar is a STOP
requiring Lead adjudication. STOP disposition: an import, connection, backup or integrity tool
error stops the stage with rc 3 and is never re-read as drift. On **both** paths the restore
root and every partial artifact are preserved and their exact path is printed.

### 5.4 Required RP4 falsifications

Exercised locally in §8: old path argument raises the reproduced `AttributeError`; wrong
invariant; wrong DB hash; wrong external manifest-file SHA; pre-existing destination; aliased
inode; sidecar appearance; failed backup/open; failed integrity/FK; partial-output
preservation; **a bundle the candidate `verify` rejects but every local check accepts**; and
**preregistered expected hashes that the candidate `verify` refuses**.

**One required RP4 falsification is NOT closed.** The *dangling destination link* case could not
be constructed at the Python level on the local harness — CPython there cannot create a symlink
(`WinError 1314`) and does not recognise a junction or the MSYS `.lnk` emulation as one. It is
recorded as **BLOCKED, not closed** (§8.4 R4-5, §8.6). The equivalent shell-level predicate is
closed by §8.2 R0-2.

---

## 6. RP5 — C4 rollback stop+mask-only (no rebind), in three separately evidenced stages

Closes **F7** and **F8**. Uses the candidate's own `deploy/linux/rollback.sh`
(blob `4b36674dcb1baa7c3b119cac98f8e6017b1f1566`) with **neither** `--to-release-sha` **nor**
`--to-manifest-sha256`, so the rebind pairing guard (`:63-68`) is never entered and the rebind
install/daemon-reload/remask branch (`:117-155`) is skipped.

### 6.1 What was wrong

- The rejected block invoked the real rollback immediately without asserting
  `/etc/mtc-bridge/rollback_manifest.json` absent. The candidate guard at `:70-71` calls
  `assert_not_symlink` **only**; `:157-180` then writes with an unconditional `cat >`, which
  **overwrites an existing regular manifest** and destroys the earlier rollback record.
- It had no dry-run rehearsal, although `rollback.sh:48` supports `--dry-run` and `common.sh:42-48`
  routes every mutating command through `run()`, which prints and returns without executing when
  `MTC_DRY_RUN=1`.
- It compared only `find` output containing basename and byte count, then called the result
  "byte-for-byte" preservation. **Any same-size content change passed.**
- It never validated the rollback manifest's fields, and never proved the mask link resolves
  exactly to `/dev/null`.
- **Round-2 defect, structural (`RR2-2`).** The round-2 repair was ONE block that required
  `C4_POST_BUNDLE_DIR` and all three post-capture hashes as non-empty **inputs**, evaluated before
  the dry run and before the rollback. Values that exist before a rollback cannot describe a
  capture taken after it, and the block had no capture step and no stage handoff through which
  future values could arrive. Its only ordering evidence was two manifest strings compared at the
  end, and the candidate `create` CLI accepts an operator-supplied `--timestamp`
  (`wal_state_bundle.py:1218-1222`), so that comparison authenticated bundle *contents* while
  proving nothing about capture *order*. A distinct, candidate-valid bundle that existed before the
  rollback and carried a later claimed timestamp was accepted — reproduced by the Lead against the
  frozen block, and reproduced again as this round's RED (§8.5).
- **Round-2 defect, structural (`RR2-3`).** The dry-run fingerprint recorded a `pgrep` **status**
  and listener and cgroup **counts**, discarding the process inventory it had already obtained.
  Replacing one bridge writer, listening socket or cgroup member with a different one left every
  recorded field equal, so "the dry run mutated nothing" was satisfiable by a mutated host.

### 6.2 Why three stages, and exactly what each one may prove

A single block cannot honestly assert a post-rollback capture, because its inputs are fixed before
its first line runs. The design is therefore split, and each stage is evidenced on its own:

| Stage | Block | Mutation class | Proves | Does NOT prove |
|---|---|---|---|---|
| A | `RP5-C4A` | mutating-host | dry run mutated nothing; exactly one real stop+mask-only invocation; postconditions; rollback-manifest fields; capture destination **absent before the mutation and still absent after it** | nothing whatsoever about state preservation |
| B | `RP5-C4B` | mutating-filesystem | the destination was still absent immediately before capture, then **this block itself** created the bundle there via the candidate's own API | that the bundle's contents match the pre-rollback state |
| C | `RP5-C4C` | read-only | candidate verification of the fresh bundle against both externally recorded hashes, and protected-invariant equality with the accepted C3 bundle | anything about a bundle other than the one stage B created |

**The causal chain, and why it does not rest on a wall-clock field.** Stage A proves the selected
destination absent *before* any mutation and again *after* the rollback, and hands that proof
forward in one create-once stage record that also pins the rollback manifest's `sha256`,
`(st_dev, st_ino)` and `st_mtime_ns`. Stage B refuses to run unless that same rollback manifest is
still live and byte-identical, proves the destination *still* absent immediately before capturing,
and then performs the capture itself. An artifact at a path that was empty one instruction earlier
must have been produced by the capture that followed, and the capture cannot start before the
rollback it is pinned to. Three independent witnesses are required, in this order of authority:

1. **Absence, then creation, inside one authorized stage** — the primary and only structural proof.
2. **`st_mtime_ns` strictly greater** than the rollback manifest's, from the OS clock at nanosecond
   resolution — corroboration, never the sole ordering evidence.
3. **The candidate's own `generated_at_utc`**, produced by `_validate_timestamp(None)` →
   `datetime.now(UTC)` because stage B passes **no** `timestamp`. Compared at second granularity
   only, since both ISO strings are second-truncated.

**Disclosed residual.** These predicates bind an operator who follows the sequence; they do not
defeat a root operator who forges records, back-dates files, or plants an artifact between two
stages *and* rewrites the create-once records to match. That is a trust boundary, not a predicate,
and it is why every record here is create-once and its digest is externally recorded per §1.5.

### 6.3 Stage A block — rollback

```bash
# ===== BLOCK-ID: RP5-C4A ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 — C4 stage A: rollback stop+mask-only, no rebind (PROPOSED DESIGN).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Mutation class: mutating-host. Requires its own explicit named authority and
# budget lift; this document grants none. No credential read, no POST /api/arm,
# no broker/exchange/order/TESTNET/mainnet/economic action, no start, no unmask.
# Requires RP0-LIB and RP0-BOOTSTRAP.
#
# This stage captures, verifies and compares NOTHING, and therefore establishes
# nothing about state preservation. It ends by proving the capture destination is
# still absent and writing ONE create-once stage record that stages B and C bind
# to. That is the point of the split: a post-rollback artifact can only be shown
# to postdate the rollback if the rollback stage first proved its destination
# empty and then handed that proof forward.
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
MASK_PATH="/etc/systemd/system/$UNIT"
UNIT_FILE="/usr/local/lib/systemd/system/$UNIT"
RELEASE_ROOT="/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE"
ROLLBACK_SH="$RELEASE_ROOT/deploy/linux/rollback.sh"
ROLLBACK_MANIFEST="/etc/mtc-bridge/rollback_manifest.json"
STEADY_UNIT_A="/usr/local/lib/systemd/system/mtc-bridge-steady.service"
STEADY_UNIT_B="/etc/systemd/system/mtc-bridge-steady.service"
PORT="8790"

# Preregistered, never derived here:
: "${C4_STATE_MANIFEST_FILE:?accepted C3 bundle manifest file path is required}"
: "${C4_STATE_MANIFEST_SHA256:?externally recorded C3 manifest FILE sha256 is required}"
: "${C4_ROLLBACK_SH_SHA256:?preregistered candidate rollback.sh sha256 is required}"
: "${C4_EXPECT_UNIT_SHA256:?preregistered installed first-start unit sha256, or the literal ABSENT_PREREGISTERED}"
: "${C4_START_ACTIVE:?preregistered starting ActiveState is required}"
: "${C4_START_ENABLED:?preregistered starting is-enabled token is required}"
: "${C4_PRE_INVARIANTS_SHA256:?preregistered pre-rollback protected-invariant hash is required}"
# The post side is preregistered as an EMPTY DESTINATION — a path, its parent, and
# the parent's expected owner/mode. No post-rollback hash may be supplied here:
# a value available before the rollback necessarily describes a bundle that
# existed before the rollback, which was exactly the accepted-bypass defect.
: "${C4_POST_BUNDLE_DIR:?post-rollback capture destination path is required, and must be absent}"
: "${C4_POST_BUNDLE_PARENT:?capture destination parent directory is required}"
: "${C4_POST_BUNDLE_PARENT_OWNER:?capture destination parent owner:group is required}"
: "${C4_POST_BUNDLE_PARENT_MODE:?capture destination parent octal mode is required}"
: "${C4_STAGE_RECORD:?create-once stage-A record path is required}"
: "${PY:?candidate venv interpreter path is required}"

c4_stop() { printf 'C4_STOP reason=%s\n' "$*"; exit 3; }
c4_fail() { printf 'C4_FAIL reason=%s\n' "$*"; exit 1; }

# Three outcomes, like every other predicate: a hash that CANNOT be taken is
# never rendered as a value. Callers adjudicate rc 3 themselves.
c4_sha256() {
    local p="$1" out rc=0
    out="$(LC_ALL=C sha256sum -- "$p" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        printf 'C4_STOP reason=sha256_failed path=%s rc=%s detail=%s\n' "$p" "$rc" "$out" >&2
        return 3
    fi
    printf '%s\n' "${out%% *}"
    return 0
}

# Digest of an inventory STRING. `<<<` avoids a pipeline, so there is no
# component status to lose; the added trailing newline is deterministic.
c4_sha256_string() {
    local label="$1" data="$2" out rc=0
    out="$(LC_ALL=C sha256sum <<<"$data" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        printf 'C4_STOP reason=inventory_hash_failed label=%s rc=%s detail=%s\n' "$label" "$rc" "$out" >&2
        return 3
    fi
    printf '%s\n' "${out%% *}"
    return 0
}

# Fingerprint used to prove the dry run mutated NOTHING.
# EVERY component is evaluated and adjudicated in its OWN assignment before the
# final `printf`. Nesting a probe or a hash inside the printf arguments makes
# `printf`'s status the function status, so a STOP is rendered as an empty field
# and the function still succeeds — that was the first defect here.
# The writers, listeners and cgroup members are compared as canonical fail-closed
# INVENTORIES, not as a status code and two counts: a same-count replacement left
# a status/count fingerprint identical, so "nothing was mutated" was satisfiable
# by a mutated host — that was the second defect. The full inventories go to the
# evidence log on stderr; their digests go into the compared string, so an
# inequality is both detected and diagnosable.
c4_fingerprint() {
    local a e m r c w l g wd ld gd
    a="$(rp0_show_property "$UNIT" ActiveState)"       || return 3
    e="$(rp0_is_enabled_token "$UNIT")"                || return 3
    m="$(rp0_probe_path "$MASK_PATH")"                 || return 3
    r="$(rp0_probe_path "$ROLLBACK_MANIFEST")"         || return 3
    c="$(c4_sha256 "$C4_STATE_MANIFEST_FILE")"         || return 3
    w="$(rp0_writer_inventory 'bridge\.app')"          || return 3
    l="$(rp0_listener_inventory "$PORT")"              || return 3
    g="$(rp0_cgroup_inventory "$UNIT")"                || return 3
    wd="$(c4_sha256_string writers   "$w")"            || return 3
    ld="$(c4_sha256_string listeners "$l")"            || return 3
    gd="$(c4_sha256_string cgroup    "$g")"            || return 3
    printf 'C4_INVENTORY writers_begin\n%s\nC4_INVENTORY writers_end\n'     "$w" >&2
    printf 'C4_INVENTORY listeners_begin\n%s\nC4_INVENTORY listeners_end\n' "$l" >&2
    printf 'C4_INVENTORY cgroup_begin\n%s\nC4_INVENTORY cgroup_end\n'       "$g" >&2
    printf 'active=%s enabled=%s mask=%s manifest=%s c3=%s writers=%s listeners=%s cgroup=%s\n' \
        "$a" "$e" "$m" "$r" "$c" "$wd" "$ld" "$gd"
    return 0
}

printf 'C4_SECTION step0_prerequisites\n'

# 1. accepted C3 manifest file plus its externally recorded FILE sha256.
kind="$(rp0_probe_path "$C4_STATE_MANIFEST_FILE")" || exit 3
[ "$kind" = "regular" ] || c4_fail "C3 manifest kind=$kind path=$C4_STATE_MANIFEST_FILE"
got="$(c4_sha256 "$C4_STATE_MANIFEST_FILE")" || c4_stop "c3_manifest_hash_unevaluable path=$C4_STATE_MANIFEST_FILE"
[ "$got" = "$C4_STATE_MANIFEST_SHA256" ] || c4_fail "C3 manifest file sha256=$got expected=$C4_STATE_MANIFEST_SHA256"
printf 'C4_c3_manifest_sha256=%s\n' "$got"

# 2. rollback-manifest path proven absent as OBJECT AND LINK, immediately before use.
#    The candidate guard (:70-71) rejects a symlink only; it supplies NO regular-file
#    no-clobber protection, and :157-180 overwrites with an unconditional `cat >`.
kind="$(rp0_probe_path "$ROLLBACK_MANIFEST")" || exit 3
printf 'C4_rollback_manifest_pre_kind=%s\n' "$kind"
[ "$kind" = "absent" ] || c4_fail "rollback manifest must be absent as object AND link, found $kind"

# 3. steady unit absent at both paths; candidate script and C3 manifest re-hashed.
for p in "$STEADY_UNIT_A" "$STEADY_UNIT_B"; do
    kind="$(rp0_probe_path "$p")" || exit 3
    [ "$kind" = "absent" ] || c4_fail "unexpected steady unit kind=$kind path=$p"
done
got="$(c4_sha256 "$ROLLBACK_SH")" || c4_stop "rollback_sh_hash_unevaluable path=$ROLLBACK_SH"
[ "$got" = "$C4_ROLLBACK_SH_SHA256" ] || c4_fail "rollback.sh sha256=$got expected=$C4_ROLLBACK_SH_SHA256"

# 4. preregistered starting state captured and matched.
active="$(rp0_show_property "$UNIT" ActiveState)" || exit 3
enabled="$(rp0_is_enabled_token "$UNIT")"         || exit 3
printf 'C4_start_active=%s C4_start_enabled=%s\n' "$active" "$enabled"
[ "$active"  = "$C4_START_ACTIVE"  ] || c4_fail "starting ActiveState=$active expected=$C4_START_ACTIVE"
[ "$enabled" = "$C4_START_ENABLED" ] || c4_fail "starting is-enabled=$enabled expected=$C4_START_ENABLED"

unit_kind="$(rp0_probe_path "$UNIT_FILE")" || exit 3
if [ "$unit_kind" = "regular" ]; then
    installed_unit_sha="$(c4_sha256 "$UNIT_FILE")" || c4_stop "installed_unit_hash_unevaluable path=$UNIT_FILE"
    [ "$C4_EXPECT_UNIT_SHA256" != "ABSENT_PREREGISTERED" ] \
        || c4_fail "installed unit present but its absence was preregistered"
    [ "$installed_unit_sha" = "$C4_EXPECT_UNIT_SHA256" ] \
        || c4_fail "installed unit sha256=$installed_unit_sha expected=$C4_EXPECT_UNIT_SHA256"
    expect_manifest_unit_sha="$C4_EXPECT_UNIT_SHA256"
elif [ "$unit_kind" = "absent" ]; then
    [ "$C4_EXPECT_UNIT_SHA256" = "ABSENT_PREREGISTERED" ] \
        || c4_fail "installed unit absent but a hash was preregistered"
    expect_manifest_unit_sha=""
else
    c4_fail "installed unit kind=$unit_kind path=$UNIT_FILE"
fi
printf 'C4_installed_unit_kind=%s\n' "$unit_kind"

# 5. THE CAPTURE DESTINATION MUST BE EMPTY BEFORE ANY MUTATION.
#    This is the structural half of the freshness proof: whatever stage B later
#    finds there cannot be an artifact that predates this rollback. The parent is
#    proven canonical, non-link, with preregistered owner/mode, and the
#    destination is proven a DIRECT child of it, so no symlinked intermediate and
#    no manufactured intermediate can redirect the capture.
rp0_require_canonical_dir "$C4_POST_BUNDLE_PARENT" "$C4_POST_BUNDLE_PARENT_OWNER" "$C4_POST_BUNDLE_PARENT_MODE" \
    || exit $?
rp0_require_leaf_inside "$C4_POST_BUNDLE_PARENT" "$C4_POST_BUNDLE_DIR" || exit $?
kind="$(rp0_probe_path "$C4_POST_BUNDLE_DIR")" || exit 3
printf 'C4_post_dest_pre_kind=%s\n' "$kind"
[ "$kind" = "absent" ] \
    || c4_fail "capture destination must be absent as object AND link before any mutation, found $kind"
kind="$(rp0_probe_path "$C4_STAGE_RECORD")" || exit 3
[ "$kind" = "absent" ] || c4_fail "stage record path must be absent, found $kind"

printf 'C4_SECTION step1_mutation_free_dry_run\n'
fp_before="$(c4_fingerprint)" || c4_stop "fingerprint_unevaluable phase=before"
dry_out="$(MTC_DRY_RUN=1 "$ROLLBACK_SH" --dry-run \
    --state-manifest-file "$C4_STATE_MANIFEST_FILE" \
    --state-manifest-sha256 "$C4_STATE_MANIFEST_SHA256" 2>&1)" || c4_fail "rollback.sh --dry-run exited nonzero"
printf 'C4_dry_run_output_begin\n%s\nC4_dry_run_output_end\n' "$dry_out"
LC_ALL=C grep -qF -- "[dry-run] systemctl stop $UNIT" <<<"$dry_out" \
    || c4_fail "dry run did not print the expected stop line"
LC_ALL=C grep -qF -- "[dry-run] systemctl mask $UNIT" <<<"$dry_out" \
    || c4_fail "dry run did not print the expected mask line"
fp_after="$(c4_fingerprint)" || c4_stop "fingerprint_unevaluable phase=after"
[ "$fp_before" = "$fp_after" ] || c4_fail "dry run mutated observable state: [$fp_before] -> [$fp_after]"
kind="$(rp0_probe_path "$ROLLBACK_MANIFEST")" || exit 3
[ "$kind" = "absent" ] || c4_fail "dry run created a rollback manifest ($kind)"
printf 'C4_dry_run_mutation_free=yes\n'

printf 'C4_SECTION step2_single_real_invocation\n'
# Exactly one invocation. No --to-release-sha, no --to-manifest-sha256: no rebind.
"$ROLLBACK_SH" \
    --state-manifest-file "$C4_STATE_MANIFEST_FILE" \
    --state-manifest-sha256 "$C4_STATE_MANIFEST_SHA256" \
    || c4_fail "rollback.sh (stop+mask-only) exited nonzero"

printf 'C4_SECTION step3_postconditions\n'
active="$(rp0_show_property "$UNIT" ActiveState)" || exit 3
enabled="$(rp0_is_enabled_token "$UNIT")"         || exit 3
printf 'C4_post_active=%s C4_post_enabled=%s\n' "$active" "$enabled"
[ "$active"  = "inactive" ] || c4_fail "ActiveState=$active expected inactive"
[ "$enabled" = "masked"   ] || c4_fail "is-enabled=$enabled expected exactly masked"

mask_kind="$(rp0_probe_path "$MASK_PATH")" || exit 3
[ "$mask_kind" = "link_live" ] || c4_fail "mask path kind=$mask_kind expected a live symlink"
raw_target="$(readlink -- "$MASK_PATH")" || c4_stop "mask_link_read_failed path=$MASK_PATH"
printf 'C4_mask_raw_target=%s\n' "$raw_target"
[ "$raw_target" = "/dev/null" ] || c4_fail "mask link raw target=$raw_target expected exactly /dev/null"

procs=""; prc=0
procs="$(rp0_pgrep_status 'bridge\.app')" || prc=$?
case "$prc" in
    0) printf 'C4_dangling_procs_begin\n%s\nC4_dangling_procs_end\n' "$procs"
       c4_fail "a bridge.app process survived rollback stop+mask" ;;
    1) printf 'C4_writers=0\n' ;;
    *) exit 3 ;;
esac
listeners="$(rp0_listener_count "$PORT")" || exit 3
printf 'C4_listener_count=%s\n' "$listeners"
[ "$listeners" -eq 0 ] || c4_fail "control port $PORT still has a listener after rollback"

# Third survivor class, fail-closed: a stopped-and-masked unit whose cgroup
# still holds a process has not been stopped.
cgsurv="$(rp0_cgroup_survivors "$UNIT")" || exit 3
printf 'C4_cgroup_survivors=%s\n' "$cgsurv"
[ "$cgsurv" -eq 0 ] || c4_fail "the unit cgroup still holds $cgsurv process(es) after rollback stop+mask"

printf 'C4_SECTION step4_rollback_manifest\n'
kind="$(rp0_probe_path "$ROLLBACK_MANIFEST")" || exit 3
[ "$kind" = "regular" ] || c4_fail "rollback manifest kind=$kind expected a newly created regular file"
rm_mode="$(LC_ALL=C stat -c '%a' -- "$ROLLBACK_MANIFEST")"   || c4_stop "rollback_manifest_mode_probe_failed"
rm_own="$(LC_ALL=C stat -c '%U:%G' -- "$ROLLBACK_MANIFEST")" || c4_stop "rollback_manifest_owner_probe_failed"
printf 'C4_rollback_manifest_mode=%s owner=%s\n' "$rm_mode" "$rm_own"
[ "$rm_mode" = "640" ]      || c4_fail "rollback manifest mode=$rm_mode expected 640"
[ "$rm_own"  = "root:root" ] || c4_fail "rollback manifest owner=$rm_own expected root:root"

# Every expected field and value validated. In no-rebind mode the candidate
# leaves rollback_release_sha and rollback_release_manifest_sha256 EMPTY
# (rollback.sh:164-165 with unset TARGET_*), while first_start_unit_sha256 is
# the INSTALLED unit hash when that unit is present (:113-116, :168) and empty
# only when the unit file is absent.
"$PY" - "$ROLLBACK_MANIFEST" "$C4_STATE_MANIFEST_SHA256" "$UNIT" "$expect_manifest_unit_sha" <<'PYEOF' \
    || c4_fail "rollback manifest field validation failed"
import json, re, sys
path, state_sha, unit, expect_unit_sha = sys.argv[1:5]
with open(path, "r", encoding="utf-8") as handle:
    m = json.load(handle)
expected = {
    "schema_version": "1.0.0",
    "rollback_release_sha": "",
    "rollback_release_manifest_sha256": "",
    "state_bundle_manifest_sha256": state_sha,
    "first_start_unit": unit,
    "first_start_unit_sha256": expect_unit_sha,
    "first_start_unit_state": "masked",
    "service_active": False,
    "service_enabled": False,
    "service_started_by_this_script": False,
    "state_dir_preserved": True,
    "secrets_touched": False,
    "firewall_modified": False,
    "windows_writer_restored": False,
}
problems = []
missing = sorted((set(expected) | {"rolled_back_at_utc"}) - set(m))
if missing:
    problems.append(f"missing_fields={missing}")
extra = sorted(set(m) - set(expected) - {"rolled_back_at_utc"})
if extra:
    problems.append(f"unexpected_fields={extra}")
for key, want in expected.items():
    got = m.get(key)
    if got != want or type(got) is not type(want):
        problems.append(f"{key}={got!r} expected {want!r}")
if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(m.get("rolled_back_at_utc", ""))):
    problems.append(f"rolled_back_at_utc={m.get('rolled_back_at_utc')!r}")
if problems:
    print("C4_manifest_problems=" + "; ".join(problems))
    raise SystemExit(1)
print("C4_manifest_fields_validated=all")
PYEOF

printf 'C4_SECTION step5_stage_record_handoff\n'
# The destination must STILL be absent AFTER the rollback: the rollback is not
# permitted to leave anything at the capture path, and stage B must be able to
# attribute whatever it finds there to its own capture and to nothing else.
kind="$(rp0_probe_path "$C4_POST_BUNDLE_DIR")" || exit 3
printf 'C4_post_dest_post_kind=%s\n' "$kind"
[ "$kind" = "absent" ] || c4_fail "capture destination is no longer absent after the rollback ($kind)"

# ONE create-once stage record. It pins the rollback manifest by content hash AND
# by (st_dev, st_ino, st_mtime_ns), so stage B can prove it is binding itself to
# THIS rollback event and not to a later rewrite of the same path.
srrc=0
"$PY" - "$C4_STAGE_RECORD" "$ROLLBACK_MANIFEST" "$C4_STATE_MANIFEST_FILE" \
    "$C4_STATE_MANIFEST_SHA256" "$C4_PRE_INVARIANTS_SHA256" "$C4_POST_BUNDLE_DIR" "$UNIT" <<'PYEOF' || srrc=$?
import hashlib, json, os, stat as statmod, sys

(record, rollback_manifest, c3_manifest, c3_sha, pre_inv_sha, post_dir, unit) = sys.argv[1:8]


def stop(reason):
    print(f"C4_STOP reason={reason}")
    raise SystemExit(3)


def fail(reason):
    print(f"C4_FAIL reason={reason}")
    raise SystemExit(1)


def sha256_file(path):
    try:
        digest = hashlib.sha256()
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError as exc:
        stop(f"hash_failed path={path} {exc.__class__.__name__}: {exc}")


try:
    st = os.lstat(rollback_manifest)
except OSError as exc:
    stop(f"rollback_manifest_stat_failed {exc.__class__.__name__}: {exc}")
if not statmod.S_ISREG(st.st_mode):
    fail(f"rollback manifest is not a regular non-link file: mode={st.st_mode:#o}")
try:
    with open(rollback_manifest, "r", encoding="utf-8") as handle:
        rollback = json.load(handle)
except Exception as exc:
    stop(f"rollback_manifest_unreadable {exc.__class__.__name__}: {exc}")

payload = {
    "schema": "wpl-p2-c4-stage-a/1",
    "unit": unit,
    "c3_manifest_path": c3_manifest,
    "c3_manifest_sha256": c3_sha,
    "pre_invariants_sha256": pre_inv_sha,
    "capture_destination": post_dir,
    "capture_destination_absent_before_mutation": True,
    "capture_destination_absent_after_rollback": True,
    "rollback_manifest_path": rollback_manifest,
    "rollback_manifest_sha256": sha256_file(rollback_manifest),
    "rollback_manifest_dev": st.st_dev,
    "rollback_manifest_ino": st.st_ino,
    "rollback_manifest_mtime_ns": st.st_mtime_ns,
    "rolled_back_at_utc": rollback.get("rolled_back_at_utc"),
}
blob = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
# Create-once: O_CREAT|O_EXCL refuses an existing regular file and an existing
# symlink, live or dangling. No append, no truncation, no rename-aside, no retry.
# The write is BINARY: a text-mode write translates newlines on some platforms,
# after which the digest printed below would not be the digest of the bytes on
# disk and the external recording would bind nothing.
try:
    handle_fd = os.open(record, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
except FileExistsError:
    fail(f"stage record already exists: {record}")
except OSError as exc:
    stop(f"stage_record_not_creatable path={record} {exc.__class__.__name__}: {exc}")
with os.fdopen(handle_fd, "wb") as handle:
    handle.write(blob)
print("C4_stage_record_path=" + record)
print("C4_stage_record_sha256=" + hashlib.sha256(blob).hexdigest())
print("C4_rollback_manifest_mtime_ns=" + str(payload["rollback_manifest_mtime_ns"]))
PYEOF
case "$srrc" in
    0) : ;;
    1) c4_fail "stage record handoff refused" ;;
    *) c4_stop "stage_record_unevaluable rc=$srrc" ;;
esac

printf 'C4_SECTION done\n'
printf 'C4A PASS (unit stopped and masked; capture destination proven empty; NOTHING about state\n'
printf '          preservation is established yet, and no start, unmask or recovery is authorised)\n'
```

### 6.4 Stage B block — fresh post-rollback capture

```bash
# ===== BLOCK-ID: RP5-C4B ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 — C4 stage B: fresh post-rollback capture (PROPOSED DESIGN).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Mutation class: mutating-filesystem. Creates exactly ONE new bundle directory,
# at a path proven absent, and reads the state database READ-ONLY through the
# candidate's own capture API. No service action, no start, no unmask, no
# daemon-reload, no credential read, no POST /api/arm, no network, no broker/
# exchange/order/TESTNET/mainnet/economic action. Requires its own explicit named
# authority; this document grants none. Requires RP0-LIB and RP0-BOOTSTRAP.
#
# Runs ONLY after RP5-C4A completed and wrote its stage record. The capture is
# performed HERE, into a destination this block proves absent immediately
# beforehand, so the artifact is causally downstream of the rollback pinned in
# that record. No post-rollback hash is an INPUT: all three are OUTPUTS, printed
# for external recording, and stage C consumes them.
#
# Capture must run AFTER the stop+mask, never before. With allow_live_source unset
# — and this block never sets it — the candidate REJECTS a capture whose source
# changed while it was being captured (`source_changed_during_capture`,
# wal_state_bundle.py:840-842). A stopped, masked unit is what makes that
# predicate satisfiable at all; a running writer would earn the rejection.
set -Eeuo pipefail

RELEASE_ROOT="/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE"
ROLLBACK_MANIFEST="/etc/mtc-bridge/rollback_manifest.json"

: "${C4_STAGE_RECORD:?stage-A record path is required}"
: "${C4_STAGE_RECORD_SHA256:?externally recorded stage-A record sha256 is required}"
: "${C4_POST_BUNDLE_DIR:?capture destination is required, and must still be absent}"
: "${C4_POST_BUNDLE_PARENT:?capture destination parent directory is required}"
: "${C4_POST_BUNDLE_PARENT_OWNER:?capture destination parent owner:group is required}"
: "${C4_POST_BUNDLE_PARENT_MODE:?capture destination parent octal mode is required}"
: "${C4_STATE_DB:?live state database path is required}"
: "${C4_CAPTURE_RECORD:?create-once stage-B capture record path is required}"
: "${PY:?candidate venv interpreter path is required}"

c4b_stop() { printf 'C4B_STOP reason=%s\n' "$*"; exit 3; }
c4b_fail() { printf 'C4B_FAIL reason=%s\n' "$*"; exit 1; }

printf 'C4B_SECTION step0_prerequisites\n'
for p in "$C4_STAGE_RECORD" "$C4_STATE_DB"; do
    kind="$(rp0_probe_path "$p")" || exit 3
    [ "$kind" = "regular" ] || c4b_fail "expected a regular non-link file, kind=$kind path=$p"
done
kind="$(rp0_probe_path "$C4_CAPTURE_RECORD")" || exit 3
[ "$kind" = "absent" ] || c4b_fail "capture record path must be absent, found $kind"

# Same parent-chain and direct-child proof as stage A, re-run here: between the
# two stages the parent could have been replaced by a symlink.
rp0_require_canonical_dir "$C4_POST_BUNDLE_PARENT" "$C4_POST_BUNDLE_PARENT_OWNER" "$C4_POST_BUNDLE_PARENT_MODE" \
    || exit $?
rp0_require_leaf_inside "$C4_POST_BUNDLE_PARENT" "$C4_POST_BUNDLE_DIR" || exit $?
kind="$(rp0_probe_path "$C4_POST_BUNDLE_DIR")" || exit 3
printf 'C4B_dest_pre_capture_kind=%s\n' "$kind"
[ "$kind" = "absent" ] \
    || c4b_fail "capture destination is not absent ($kind): a pre-existing artifact is never adopted as the fresh capture"

printf 'C4B_SECTION step1_bind_rollback_then_capture\n'
cbrc=0
"$PY" - "$RELEASE_ROOT" "$C4_STAGE_RECORD" "$C4_STAGE_RECORD_SHA256" "$C4_POST_BUNDLE_DIR" \
    "$C4_POST_BUNDLE_PARENT" "$C4_STATE_DB" "$C4_CAPTURE_RECORD" "$ROLLBACK_MANIFEST" <<'PYEOF' || cbrc=$?
import hashlib, json, os, stat as statmod, sys
from pathlib import Path

(release_root, stage_record, stage_record_sha, post_dir, post_parent, state_db,
 capture_record, rollback_manifest) = sys.argv[1:9]


def stop(reason):
    print(f"C4B_STOP reason={reason}")
    raise SystemExit(3)


def fail(reason):
    print(f"C4B_FAIL reason={reason}")
    raise SystemExit(1)


def sha256_file(path):
    try:
        digest = hashlib.sha256()
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError as exc:
        stop(f"hash_failed path={path} {exc.__class__.__name__}: {exc}")


def load(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception as exc:
        stop(f"unreadable_json path={path} {exc.__class__.__name__}: {exc}")


sys.path.insert(0, release_root)
try:
    from tools.wal_state_bundle import MANIFEST_NAME, create_bundle
except Exception as exc:
    stop(f"candidate_api_import_failed: {exc.__class__.__name__}: {exc}")

# 1. the stage record is exactly the externally recorded one.
actual_stage_sha = sha256_file(stage_record)
print(f"C4B_stage_record_sha256={actual_stage_sha}")
if actual_stage_sha != stage_record_sha.lower():
    fail("stage record sha256 does not match the externally recorded value")
record = load(stage_record)
if record.get("schema") != "wpl-p2-c4-stage-a/1":
    fail(f"stage record schema={record.get('schema')!r} is not the stage-A contract")
if record.get("capture_destination") != post_dir:
    fail("stage record names a different capture destination than this stage was given")
if record.get("capture_destination_absent_before_mutation") is not True:
    fail("stage record does not assert the destination was absent before the mutation")
if record.get("capture_destination_absent_after_rollback") is not True:
    fail("stage record does not assert the destination was absent after the rollback")

# 2. the SAME rollback event, not a later rewrite of the same path.
try:
    rst = os.lstat(rollback_manifest)
except OSError as exc:
    stop(f"rollback_manifest_stat_failed {exc.__class__.__name__}: {exc}")
if not statmod.S_ISREG(rst.st_mode):
    fail(f"rollback manifest is not a regular non-link file: mode={rst.st_mode:#o}")
live = (rst.st_dev, rst.st_ino, rst.st_mtime_ns, sha256_file(rollback_manifest))
pinned = (record.get("rollback_manifest_dev"), record.get("rollback_manifest_ino"),
          record.get("rollback_manifest_mtime_ns"), record.get("rollback_manifest_sha256"))
print(f"C4B_rollback_identity_live={live}")
print(f"C4B_rollback_identity_pinned={pinned}")
# A malformed record is COULD NOT EVALUATE, not FALSE: without this the type error
# below would surface as a Python traceback and be adjudicated as a plain FAIL.
if not isinstance(pinned[2], int):
    stop(f"pinned_rollback_mtime_ns_not_an_integer: {pinned[2]!r}")
if live != pinned:
    fail("the rollback manifest changed since stage A: this capture cannot be bound to that rollback")
rolled = str(record.get("rolled_back_at_utc") or "")
if not rolled:
    stop("stage_record_missing_rolled_back_at_utc")

# 3. the parent must ALREADY be a real directory, so the candidate's
#    out_dir.mkdir(parents=True) has no intermediate left to manufacture.
try:
    pst = os.lstat(post_parent)
except OSError as exc:
    stop(f"parent_stat_failed path={post_parent} {exc.__class__.__name__}: {exc}")
if not statmod.S_ISDIR(pst.st_mode):
    fail(f"capture destination parent is not a real directory: mode={pst.st_mode:#o}")

# 4. destination absent as OBJECT AND LINK immediately before the capture. This
#    is the structural freshness proof: an artifact at a path that was empty one
#    instruction earlier was produced by the capture that follows.
try:
    dst = os.lstat(post_dir)
except FileNotFoundError:
    pass
except OSError as exc:
    stop(f"destination_probe_failed path={post_dir} {exc.__class__.__name__}: {exc}")
else:
    fail(f"capture destination exists immediately before capture: mode={dst.st_mode:#o}")

# 5. the state database must be a regular non-link file.
try:
    sst = os.lstat(state_db)
except OSError as exc:
    stop(f"state_db_stat_failed path={state_db} {exc.__class__.__name__}: {exc}")
if not statmod.S_ISREG(sst.st_mode):
    fail(f"state database is not a regular non-link file: mode={sst.st_mode:#o}")

# 6. the capture itself, through the candidate's own API. timestamp is NOT passed:
#    _validate_timestamp(None) uses datetime.now(UTC), so generated_at_utc is the
#    candidate's own clock and not an operator-chosen string. force is NOT passed,
#    so an unexpected artifact at the destination is refused by the candidate too.
try:
    code, report = create_bundle(source=Path(state_db), out_dir=Path(post_dir))
except Exception as exc:
    stop(f"candidate_create_unevaluable: {exc.__class__.__name__}: {exc}")
print(f"C4B_capture_rc={code} verdict={report.get('verdict')} failures={report.get('failures')}")
if code != 0 or report.get("verdict") != "CAPTURED":
    fail(f"candidate capture did not produce a bundle: {report.get('failures')}")

manifest_path = Path(post_dir) / MANIFEST_NAME
try:
    mst = os.lstat(manifest_path)
except OSError as exc:
    stop(f"fresh_manifest_stat_failed {exc.__class__.__name__}: {exc}")
if not statmod.S_ISREG(mst.st_mode):
    fail(f"fresh bundle manifest is not a regular non-link file: mode={mst.st_mode:#o}")
manifest = load(manifest_path)
manifest_sha = sha256_file(manifest_path)
captured = str(manifest.get("generated_at_utc", ""))
if not captured:
    stop("fresh_manifest_missing_generated_at_utc")

# 7. corroborating ordering witnesses. The OS-set nanosecond mtime is strict; the
#    candidate's own second-truncated timestamp may legitimately land inside the
#    rollback's second, so only an EARLIER second is a failure there. Neither is
#    the primary proof — step 4 is.
print(f"C4B_fresh_manifest_mtime_ns={mst.st_mtime_ns} rollback_mtime_ns={pinned[2]}")
print(f"C4B_generated_at_utc={captured} rolled_back_at_utc={rolled}")
if mst.st_mtime_ns <= pinned[2]:
    fail("fresh bundle manifest is not strictly newer than the rollback manifest")
if captured < rolled:
    fail(f"candidate capture clock predates the rollback ({captured} < {rolled})")

payload = {
    "schema": "wpl-p2-c4-stage-b/1",
    "stage_record_path": stage_record,
    "stage_record_sha256": actual_stage_sha,
    "capture_destination": post_dir,
    "post_manifest_path": str(manifest_path),
    "post_manifest_sha256": manifest_sha,
    "post_manifest_dev": mst.st_dev,
    "post_manifest_ino": mst.st_ino,
    "post_manifest_mtime_ns": mst.st_mtime_ns,
    "post_bundle_db_sha256": manifest.get("bundle", {}).get("db_sha256"),
    "post_invariants_sha256": manifest.get("invariants_sha256"),
    "generated_at_utc": captured,
    "rolled_back_at_utc": rolled,
}
for key in ("post_bundle_db_sha256", "post_invariants_sha256"):
    if not isinstance(payload[key], str) or len(payload[key]) != 64:
        fail(f"fresh manifest {key}={payload[key]!r} is not a sha256")
blob = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
# Create-once, and BINARY for the same reason as the stage record: the digest
# printed below must be the digest of the bytes actually on disk.
try:
    handle_fd = os.open(capture_record, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
except FileExistsError:
    fail(f"capture record already exists: {capture_record}")
except OSError as exc:
    stop(f"capture_record_not_creatable path={capture_record} {exc.__class__.__name__}: {exc}")
with os.fdopen(handle_fd, "wb") as handle:
    handle.write(blob)
print("C4_POST_MANIFEST_SHA256=" + manifest_sha)
print("C4_POST_BUNDLE_DB_SHA256=" + payload["post_bundle_db_sha256"])
print("C4_POST_INVARIANTS_SHA256=" + payload["post_invariants_sha256"])
print("C4B_capture_record_path=" + capture_record)
print("C4B_capture_record_sha256=" + hashlib.sha256(blob).hexdigest())
PYEOF
case "$cbrc" in
    0) : ;;
    1) c4b_fail "fresh capture refused" ;;
    *) c4b_stop "capture_unevaluable rc=$cbrc" ;;
esac

printf 'C4B_SECTION done\n'
printf 'C4B PASS (one fresh bundle captured downstream of the recorded rollback; the three digests\n'
printf '          above are OUTPUTS to be recorded externally, and NOTHING is verified or compared yet)\n'
```

### 6.5 Stage C block — candidate verification and protected equality

```bash
# ===== BLOCK-ID: RP5-C4C ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 — C4 stage C: verification and protected equality (PROPOSED DESIGN).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Mutation class: read-only. Reads the two create-once stage records, the rollback
# manifest, the accepted C3 manifest and the fresh bundle; writes nothing except
# its own RP0 evidence leaf. No service action, no credential read, no network,
# no POST /api/arm, no broker/exchange/order/TESTNET/mainnet/economic action.
# Requires RP0-LIB and RP0-BOOTSTRAP, and runs only after RP5-C4B.
#
# The three post-rollback digests ARE inputs here, and that is now sound: they
# were produced by stage B AFTER the rollback and are re-bound to stage B's
# create-once capture record and to the live artifact's own identity. String
# equality of two supplied variables is still NOT the predicate — it passes for
# stale values, for values never derived from any bundle, and for the accepted C3
# bundle handed back as its own "post" artifact. Filename and byte-count equality
# remain DIAGNOSTIC ONLY and are never described as byte equality.
set -Eeuo pipefail

RELEASE_ROOT="/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE"
ROLLBACK_MANIFEST="/etc/mtc-bridge/rollback_manifest.json"

: "${C4_STAGE_RECORD:?stage-A record path is required}"
: "${C4_STAGE_RECORD_SHA256:?externally recorded stage-A record sha256 is required}"
: "${C4_CAPTURE_RECORD:?stage-B capture record path is required}"
: "${C4_CAPTURE_RECORD_SHA256:?externally recorded stage-B capture record sha256 is required}"
: "${C4_STATE_MANIFEST_FILE:?accepted C3 bundle manifest file path is required}"
: "${C4_STATE_MANIFEST_SHA256:?externally recorded C3 manifest FILE sha256 is required}"
: "${C4_PRE_INVARIANTS_SHA256:?preregistered pre-rollback protected-invariant hash is required}"
: "${C4_POST_BUNDLE_DIR:?fresh post-rollback bundle directory is required}"
: "${C4_POST_MANIFEST_SHA256:?externally recorded fresh post-rollback manifest FILE sha256 is required}"
: "${C4_POST_BUNDLE_DB_SHA256:?externally recorded fresh post-rollback bundle db sha256 is required}"
: "${C4_POST_INVARIANTS_SHA256:?externally recorded fresh post-rollback invariants sha256 is required}"
: "${PY:?candidate venv interpreter path is required}"

c4c_stop() { printf 'C4C_STOP reason=%s\n' "$*"; exit 3; }
c4c_fail() { printf 'C4C_FAIL reason=%s\n' "$*"; exit 1; }

printf 'C4C_SECTION step0_prerequisites\n'
for p in "$C4_STAGE_RECORD" "$C4_CAPTURE_RECORD" "$C4_STATE_MANIFEST_FILE" "$ROLLBACK_MANIFEST"; do
    kind="$(rp0_probe_path "$p")" || exit 3
    [ "$kind" = "regular" ] || c4c_fail "expected a regular non-link file, kind=$kind path=$p"
done
kind="$(rp0_probe_path "$C4_POST_BUNDLE_DIR")" || exit 3
[ "$kind" = "dir" ] || c4c_fail "fresh bundle directory kind=$kind path=$C4_POST_BUNDLE_DIR"

printf 'C4C_SECTION step1_chain_verify_and_equality\n'
pbrc=0
"$PY" - "$RELEASE_ROOT" "$C4_STAGE_RECORD" "$C4_STAGE_RECORD_SHA256" "$C4_CAPTURE_RECORD" \
    "$C4_CAPTURE_RECORD_SHA256" "$C4_STATE_MANIFEST_FILE" "$C4_STATE_MANIFEST_SHA256" \
    "$C4_PRE_INVARIANTS_SHA256" "$C4_POST_BUNDLE_DIR" "$C4_POST_MANIFEST_SHA256" \
    "$C4_POST_BUNDLE_DB_SHA256" "$C4_POST_INVARIANTS_SHA256" "$ROLLBACK_MANIFEST" <<'PYEOF' || pbrc=$?
import hashlib, json, os, stat as statmod, sys
from pathlib import Path

(release_root, stage_record, stage_record_sha, capture_record, capture_record_sha,
 c3_manifest, c3_manifest_sha, pre_inv_sha, post_dir, post_manifest_sha,
 post_db_sha, post_inv_sha, rollback_manifest) = sys.argv[1:14]

PROTECTED_FIELDS = (
    "schema_version", "app_state", "counts", "open_trades", "live_orders",
    "closed_trades", "max_ids", "environments", "risk_days",
)


def stop(reason):
    print(f"C4C_STOP reason={reason}")
    raise SystemExit(3)


def sha256_file(path):
    try:
        digest = hashlib.sha256()
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError as exc:
        stop(f"hash_failed path={path} {exc.__class__.__name__}: {exc}")


def load(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception as exc:
        stop(f"unreadable_json path={path} {exc.__class__.__name__}: {exc}")


sys.path.insert(0, release_root)
try:
    from tools.wal_state_bundle import MANIFEST_NAME, verify_bundle
except Exception as exc:
    stop(f"candidate_api_import_failed: {exc.__class__.__name__}: {exc}")

problems = []

# 1. both create-once records are exactly the externally recorded ones, and the
#    capture record names the stage record it was produced from.
actual_stage_sha = sha256_file(stage_record)
actual_capture_sha = sha256_file(capture_record)
print(f"C4C_stage_record_sha256={actual_stage_sha}")
print(f"C4C_capture_record_sha256={actual_capture_sha}")
if actual_stage_sha != stage_record_sha.lower():
    problems.append("stage record sha256 does not match the externally recorded value")
if actual_capture_sha != capture_record_sha.lower():
    problems.append("capture record sha256 does not match the externally recorded value")
stage = load(stage_record)
capture = load(capture_record)
if stage.get("schema") != "wpl-p2-c4-stage-a/1" or capture.get("schema") != "wpl-p2-c4-stage-b/1":
    stop("record_schema_unrecognised")
if capture.get("stage_record_sha256") != actual_stage_sha:
    problems.append("capture record was not produced from this stage record")
if stage.get("capture_destination") != post_dir or capture.get("capture_destination") != post_dir:
    problems.append("the records do not agree with the bundle directory under verification")
if stage.get("c3_manifest_sha256") != c3_manifest_sha or stage.get("pre_invariants_sha256") != pre_inv_sha:
    problems.append("the accepted C3 identity supplied here is not the one stage A rolled back against")

# 2. the accepted C3 manifest is still exactly the accepted artifact.
actual_c3_sha = sha256_file(c3_manifest)
print(f"C4C_c3_manifest_sha256={actual_c3_sha}")
if actual_c3_sha != c3_manifest_sha.lower():
    problems.append("accepted C3 manifest FILE sha256 changed since stage A")

# 3. the SAME rollback event is still live and unrewritten.
try:
    rst = os.lstat(rollback_manifest)
except OSError as exc:
    stop(f"rollback_manifest_stat_failed {exc.__class__.__name__}: {exc}")
live_rollback = (rst.st_dev, rst.st_ino, rst.st_mtime_ns, sha256_file(rollback_manifest))
pinned_rollback = (stage.get("rollback_manifest_dev"), stage.get("rollback_manifest_ino"),
                   stage.get("rollback_manifest_mtime_ns"), stage.get("rollback_manifest_sha256"))
if live_rollback != pinned_rollback:
    problems.append("the rollback manifest changed after stage A: the chain no longer describes one rollback")

# 4. the artifact verified here is the one stage B created, unchanged since.
post_manifest_path = Path(post_dir) / MANIFEST_NAME
try:
    mst = os.lstat(post_manifest_path)
except OSError as exc:
    stop(f"post_manifest_stat_failed path={post_manifest_path} {exc.__class__.__name__}: {exc}")
if not statmod.S_ISREG(mst.st_mode):
    stop(f"post_bundle_manifest_not_a_regular_file path={post_manifest_path}")
actual_post_manifest_sha = sha256_file(post_manifest_path)
live_post = (mst.st_dev, mst.st_ino, mst.st_mtime_ns, actual_post_manifest_sha)
pinned_post = (capture.get("post_manifest_dev"), capture.get("post_manifest_ino"),
               capture.get("post_manifest_mtime_ns"), capture.get("post_manifest_sha256"))
print(f"C4C_post_identity_live={live_post}")
print(f"C4C_post_identity_pinned={pinned_post}")
if live_post != pinned_post:
    problems.append("the fresh bundle manifest is not the artifact stage B captured, or changed since")
print(f"C4C_post_manifest_file_sha256={actual_post_manifest_sha}")
if actual_post_manifest_sha != post_manifest_sha.lower():
    problems.append("fresh bundle manifest FILE sha256 does not match the recorded capture value")

# 5. the post bundle must be a DIFFERENT artifact from the accepted C3 bundle.
try:
    c3st = os.lstat(c3_manifest)
except OSError as exc:
    stop(f"identity_probe_failed: {exc.__class__.__name__}: {exc}")
print(f"C4C_post_bundle_identity=({mst.st_dev},{mst.st_ino}) c3_identity=({c3st.st_dev},{c3st.st_ino})")
if (c3st.st_dev, c3st.st_ino) == (mst.st_dev, mst.st_ino):
    problems.append("post bundle manifest IS the accepted C3 manifest: no fresh capture happened")

# 6. the recorded digests must be the capture's own, and the ordering witnesses
#    recorded by stage B must still hold. The structural proof stays stage A/B's
#    absent-then-create sequence; these are corroboration.
if capture.get("post_bundle_db_sha256") != post_db_sha.lower():
    problems.append("recorded post bundle db sha256 is not the value stage B captured")
if capture.get("post_invariants_sha256") != post_inv_sha.lower():
    problems.append("recorded post invariants sha256 is not the value stage B captured")
captured_at = str(capture.get("generated_at_utc") or "")
rolled_at = str(stage.get("rolled_back_at_utc") or "")
print(f"C4C_generated_at_utc={captured_at} rolled_back_at_utc={rolled_at} "
      f"post_mtime_ns={pinned_post[2]} rollback_mtime_ns={pinned_rollback[2]}")
if not captured_at or not rolled_at:
    stop("capture_or_rollback_timestamp_missing")
if not isinstance(pinned_post[2], int) or not isinstance(pinned_rollback[2], int):
    stop("recorded_mtime_ns_not_an_integer")
if pinned_post[2] <= pinned_rollback[2]:
    problems.append("the recorded capture is not strictly newer than the recorded rollback")
if captured_at < rolled_at:
    problems.append(f"the capture clock predates the rollback ({captured_at} < {rolled_at}): it is stale")

pre_manifest = load(c3_manifest)
post_manifest = load(post_manifest_path)

# 7. neither hash may be a free string: each must be its own bundle's value.
if pre_manifest.get("invariants_sha256") != pre_inv_sha:
    problems.append("preregistered pre-rollback hash is not bound to the accepted C3 bundle")
if post_manifest.get("invariants_sha256") != post_inv_sha:
    problems.append("recorded post-rollback hash is not the fresh bundle's own value")

# 8. candidate verification with BOTH exact expected hashes; fail-closed.
try:
    code, report = verify_bundle(bundle_dir=Path(post_dir),
                                 expect_bundle_sha256=post_db_sha,
                                 expect_invariants_sha256=post_inv_sha)
except Exception as exc:
    stop(f"candidate_verify_unevaluable: {exc.__class__.__name__}: {exc}")
print(f"C4C_post_bundle_verify_rc={code} verdict={report.get('verdict')} "
      f"failures={report.get('failures')}")
if code != 0 or report.get("verdict") != "VALID":
    problems.append(f"candidate verify rejected the fresh post-rollback bundle: {report.get('failures')}")

# 9. protected equality: the candidate hash AND every protected field.
if post_inv_sha != pre_inv_sha:
    problems.append(f"protected invariants changed across rollback (pre={pre_inv_sha} post={post_inv_sha})")
pre_inv = pre_manifest.get("invariants", {})
post_inv = post_manifest.get("invariants", {})
for field in PROTECTED_FIELDS:
    if pre_inv.get(field) != post_inv.get(field):
        problems.append(f"protected invariant field differs across rollback: {field}")

if problems:
    print("C4C_post_bundle_problems=" + "; ".join(problems))
    raise SystemExit(1)
print("C4C_post_rollback_bundle_verified=yes")
PYEOF
case "$pbrc" in
    0) : ;;
    1) c4c_fail "fresh post-rollback bundle binding failed (see C4C_post_bundle_problems)" ;;
    *) c4c_stop "post_rollback_bundle_unevaluable rc=$pbrc" ;;
esac
printf 'C4C_invariants_equal=yes sha256=%s\n' "$C4_POST_INVARIANTS_SHA256"

printf 'C4C_SECTION done\n'
printf 'C4C PASS (protected state preserved across the rollback, on a bundle captured downstream of\n'
printf '          it; no start, unmask or recovery is authorised by this result)\n'
```

### 6.6 Required RP5 falsifications

Exercised locally in §8: pre-existing regular rollback manifest; dangling manifest link; dry-run
that mutates; same-size protected DB mutation; wrong state-manifest hash; unexpected rebind flag;
failed post-rollback invariant equality; **a dry-run fingerprint component that cannot be
evaluated**; **a post-rollback value not bound to any fresh verified bundle**; and **a stale post
bundle captured before the rollback**. **Wrong mask target** is required and remains exercised **in
round 1 only** (`R5-6`); rounds 2 and 3 could not present that fixture on this mount and make no
claim for it — §8.7 gap 7.

Round 3 adds, and §8.5 exercises: **a candidate-valid bundle that already exists at the capture
destination** (refused before any mutation, and again at capture time); **a bundle honestly captured
before the rollback and offered to stage C with its own record digest recorded externally** (refused
by the ordering witness); **a fresh bundle altered after capture** (refused by artifact identity);
**a rollback manifest rewritten between stages** (refused by the pinned rollback identity); and
**a same-count writer, listener or cgroup-member replacement across the dry run** (refused by the
inventory fingerprint), plus a listening socket whose owning process cannot be resolved (STOP).

---

## 7. RP6 — C5 (egress capture) remains **BLOCKED**

```text
[BLOCKED DESIGN — NON-RUNNABLE — AUTHORITY STATEMENT ONLY]

At the candidate, the deployed credential-free DISARMED start mode constructs NO BROKER AT ALL,
so there is no broker egress to capture from the current staging runtime at any authority level.

C5 therefore remains an open COMMAND GAP. This repair cycle adds NO command, NO credential name
or value procedure, NO alternate start mode, NO TESTNET endpoint, NO network allow rule, NO ARM
request and NO order action.

Scoping C5 requires a human with explicit credential and broker/TESTNET network authority. None
of that authority exists here, and none is implied by anything in this document.
```

---

## 8. D026 local falsification evidence

### 8.1 What was executed, and what was not

Every RP0, RP1, RP4 and RP5 falsification that can be exercised without a real host was run
**locally, for real**, in a **fresh OS temporary root**, before this document was returned. Each
repair round adds its own independent root; **no earlier root is touched, and nothing in any root
is deleted.**

- **Round-1 preserved evidence root (exact path, unchanged):**
  `C:\Users\BARSEM~1\AppData\Local\Temp\D026.mR6q2g` (POSIX form `/tmp/D026.mR6q2g`).
  Transcript `D026_FULL_TRANSCRIPT.md`, 1605 lines, SHA-256
  `1bbb4a469aa1503d0d5aa4775835a97c4e6bccfb3c301fde61b9be3703a742e1`.
- **Round-2 preserved evidence root (exact path, unchanged):**
  `C:\Users\BARSEM~1\AppData\Local\Temp\D026R2.87imLE` (POSIX form `/tmp/D026R2.87imLE`).
  Transcript `D026_R2_TRANSCRIPT.md`, 286 lines, SHA-256
  `e6c991f1a34dcc12ea7af0b3a9bf34070aa6a3016b4f44d826138e432eeed68c`, produced in one pass by the
  preserved `run_all_final.sh`. Runner scripts, stub trees and every fixture are preserved beside it.
  **Correction, round 3 — finding RR2-4.** Round 2 asserted here that re-running
  `run_all_final.sh` allocates fresh identifiers. That assertion was **false and is withdrawn**:
  the runner hard-codes `RUN-TRAV-F`, `RUN-R2-OKF`, `restore_f0` and its other create-once
  identifiers, so a second consecutive invocation fails its own positive controls with
  `File exists` / `restore root already exists` instead of replaying them. The 286-line transcript
  and its SHA-256 are unaffected — they record a genuine first run, and the re-audit reproduced
  R1-R3 with fresh identifiers by hand — but that runner is **single-shot**, and the round-2 root
  is preserved as a first-run record only. It advertises no rerun contract any more.
- **Round-3 preserved evidence root (exact path):**
  `C:\Users\BARSEM~1\AppData\Local\Temp\D026R3.QgHw2b` (POSIX form `/tmp/D026R3.QgHw2b`).
  Two transcripts, `D026_R3_TRANSCRIPT_RUN1.md` and `D026_R3_TRANSCRIPT_RUN2.md`, produced by two
  **consecutive** invocations of the preserved `run_all_r3.sh`. Every earlier pass is also preserved
  rather than deleted — `PREFLIGHT_RUN.md` from harness development and `REHEARSAL_RUN1..4.md` from
  runs taken before the last two corrections (a block comment that misdescribed the candidate's
  `allow_live_source` behaviour, and a runner label that asserted a hard-coded seconds figure). Those
  rehearsals are **not** the evidence of record; they are kept so the sequence is auditable.
  `run_all_r3.sh` allocates **one fresh suffix per invocation** from
  `mktemp -d` and derives *every* create-once identifier from it — fixture roots, evidence run IDs,
  stage IDs, restore roots, stage records, capture records and capture destinations — so
  consecutive invocations cannot collide. Both runs are compared on their `OUTCOME` lines, which
  are identical; only paths, inode numbers, timestamps and the digests of freshly captured bundles
  differ, exactly as they must. Runner scripts, stubs, extractors and every fixture are preserved
  beside the transcripts.
- **The harness executes the blocks in this document, not a paraphrase.** Each runner extracts
  its block from this file by `BLOCK-ID` marker and executes that extracted text. Round-1 REDs
  extract the **exact rejected text** from
  `git show 779bd038957a192db47ff7ad68eb51304a2fba46:<this file>`. Round-2 REDs extract the
  **exact round-1 repaired text** from `git show 7194b895:<this file>` by the same marker — the
  seven round-1 digests reproduce byte for byte, so each R1-R5 RED is the audited blob itself.
  Round-3 REDs extract the **exact round-2 repaired text** from
  `git show 75ee8912:<this file>` (blob `9785bf8eba29c52ac61744986800e7f66c8fd6bf`, the audited
  one); the re-extracted `RP5-C4` digest is `dbab2306…` and `RP0-LIB` is `4cc7ceff…`, both equal to
  the round-2 §8.1 table and to the values the round-2 re-audit reproduced, so each RR2-2/RR2-3 RED
  is the audited blob itself.
- **Nothing host-side was touched.** No `/home/gatea`, no real `systemctl`, no candidate
  `rollback.sh`, no host, no SSH, no transport, no credential, no broker, no order. `systemctl`,
  `pgrep`, `ss` and the rollback script are **local stubs**; the candidate `rollback.sh` is
  **never invoked**.
- **Environment:** Git Bash / MSYS2 bash 5.2.37 on Windows 11, CPython 3.14.2, SQLite 3.50.4.
- **Honest stub scope.** The harness filesystem is an MSYS `noacl` NTFS mount that cannot
  represent POSIX mode bits. Where a fixture needs `0555`/`0444`/`0020`/`0002`/`0640`, `stat`
  and `find` answer from a per-case fixture table modelling documented GNU semantics
  (`-perm /222` = any write bit; `-perm -0200` = owner write only). `mkdir -m` is stubbed for
  the same reason, preserving only its create-once semantics. Round 2 adds three disclosed stubs:
  a `systemctl show -p ControlGroup` responder, a fixture cgroup tree under `RP0_CGROUP_ROOT`
  holding real `cgroup.procs` files, and a **local stub `rollback.sh`** that models only the
  stop+mask-only no-rebind path and the manifest the candidate writes. Round 2 also interposes a
  `python` wrapper that translates POSIX argument paths to Windows paths before exec'ing the real
  CPython, because this MSYS shell hands POSIX paths to a Windows interpreter; it adds, removes
  and reinterprets no argument. Everything else is real: real files, real MSYS symlinks, real
  `readlink`, `sha256sum`, `find`, `sort`, `mktemp`, `grep`, `/proc/uptime`, real Python, real
  SQLite, and the real candidate `wal_state_bundle` module (blob
  `26c077e650ab88ba2086efa3a80790769bc055b1`), including its own `create` and `verify_bundle`.
- **Round-3 stub changes, all disclosed.** (1) `pgrep` and `ss` become **fixture-driven**: they
  print the inventory a nominated fixture file holds, so a same-count identity replacement can be
  presented. `ss -H -ltnp` output is modelled on documented iproute2 formatting; **this machine has
  no real `ss`**, so the owner-field parsing is falsified against modelled text, not against a live
  socket. (2) The `stat` stub gains a nominated-path **probe-ERROR** mode, so the
  COULD-NOT-EVALUATE branch is exercised inside the **real** `rp0_probe_path`; round 2 replaced
  `rp0_probe_path` itself with a local stand-in for that case, which was weaker. (3) The round-3
  `rollback.sh` stub writes `rolled_back_at_utc` from a **real clock reading** instead of a fixed
  literal, so the ordering witnesses are compared against real time. (4) The `python` wrapper now
  translates an absolute argument **whether or not it already exists** — required here, because the
  capture destination is by design absent when stage B receives it. It still adds, removes and
  reinterprets no argument. (5) The C4 stages are run with `RP0-LIB` sourced but **without**
  `RP0-BOOTSTRAP`'s evidence redirect, so block output lands in the transcript instead of an
  evidence leaf; that changes no predicate, and `RP0-BOOTSTRAP` is exercised separately in §8.2.
- **Path rewrites.** The RP5 harness copies differ from the published blocks **only** in absolute
  path constants repointed at the fixture root: six in `RP5-C4A` and in the round-2 `RP5-C4` RED
  (`MASK_PATH`, `UNIT_FILE`, `RELEASE_ROOT`, `ROLLBACK_MANIFEST`, `STEADY_UNIT_A`,
  `STEADY_UNIT_B`), and two each in `RP5-C4B` and `RP5-C4C` (`RELEASE_ROOT`,
  `ROLLBACK_MANIFEST`); the RP3 copies differ only in `FRAGMENT`/`MASK_PATH`. Every predicate and
  comparison line is byte-identical; the rewriter prints its own unified diff into the transcript
  and the rewritten copies are preserved beside it. The round-1 RED block's `mktemp` was shimmed
  away from `/home/gatea` — that is the only change to rejected text, and it exists precisely so
  the harness could not touch that path.

**How the transcripts bind to this file.** Each round-3 transcript records the SHA-256 of the
proposal snapshot the harness actually executed, together with the nine block digests it extracted
from it. That snapshot digest does **not** equal the committed file's, and cannot: the transcript
excerpts quoted in §8.5 were pasted into §8.5 *after* the runs that produced them. **The binding is
the block digest table below** — re-extract the blocks from the committed file and every one of the
nine digests must equal both the table and the transcripts. No block, comment or predicate was
touched after the runs; only §8.5 prose was.

**Block identity, syntax and import validation.** SHA-256 of each block exactly as extracted
from this file by its `BLOCK-ID` marker up to (not including) the closing fence, LF line endings.
Round 2 writes every extracted copy in binary with LF, so the digest of the file the harness
actually executed equals the digest below.

| Block | Lines | SHA-256 (LF) | Check | Result |
|---|---|---|---|---|
| `RP0-LIB` | 370 | `4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48` | `bash -n` | OK |
| `RP0-BOOTSTRAP` | 36 | `e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33` | `bash -n` | OK |
| `RP1-B3` | 117 | `f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af` | `bash -n` | OK |
| `RP3-C2A-POST` | 104 | `e233d29b005964e84cd6cbc2af50deccd83bb281dac39696e47de1c8890b5a27` | `bash -n` | OK |
| `RP3-C2B-POST` | 74 | `26a1010cd9380289c5b90c08845b2af6ec31074fc5145241978a714b930bb412` | `bash -n` | OK |
| `RP4-C3` | 295 | `0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5` | `py_compile` | OK |
| `RP5-C4A` | 374 | `a5b1b2e4d4e5227b3bb1f0ea31e9e547040231913445970efe1046f4eba9e0f2` | `bash -n` + heredoc `py_compile` ×2 | OK |
| `RP5-C4B` | 249 | `10c4b3231042101ed9049dbf57ec3123ce902e9b18136769728a1a2e92f4037e` | `bash -n` + heredoc `py_compile` | OK |
| `RP5-C4C` | 228 | `de7301f1deb752bcc63d818348c2fdc33372a6b7d7d4f377b62bdf27d313e3a8` | `bash -n` + heredoc `py_compile` | OK |

`RP0-BOOTSTRAP`, `RP1-B3`, `RP3-C2A-POST`, `RP3-C2B-POST` and `RP4-C3` are **unchanged in round 3**
and keep their round-2 digests exactly, which the round-3 extraction reproduces; their existing
evidence stands. `RP5-C4` no longer exists: it is replaced by the three stage blocks, and its
round-2 digest `dbab23064cc25f5b2837caa534b204aa07d07ee263f1c6c3193c11a8cfbab6c4` now identifies the
**RED** text.

`RP0-LIB` changed, and the change is **purely additive**. The harness compares the two versions
function by function and records the result in the transcript: all twelve pre-existing functions —
including `rp0_probe_path`, `rp0_pgrep_status`, `rp0_listener_count` and `rp0_cgroup_survivors` — are
**byte-identical**, and the only difference is the three new inventory functions. The RP1 and RP3
evidence that depends on those predicates therefore still stands even though the library's own
digest moved.

`RP3-C2A-POST` and `RP3-C2B-POST` were **syntax-validated only in round 1**. Round 2 additionally
exercises them **at stub level** (§8.6) to falsify the two postconditions added there. That is
predicate evidence about the block text, **not scenario closure**: both C2 scenarios remain
BLOCKED on C1-GAP-B, no real baseline capture exists, and **no C1, C2-scenario or C5 falsification
is claimed closed.**

### 8.2 RP0 — evidence channel and predicate bootstrap (F1, shared F9)

RED = exact rejected text, lines `122-127` (log guard), `275-279` (`pgrep`), `388-395`
(`is-enabled`). GREEN = this document's `RP0-LIB` / `RP0-BOOTSTRAP`.

| # | Falsification | RED rc | RED observed | GREEN rc | GREEN observed |
|---|---|---|---|---|---|
| R0-1 | existing regular evidence leaf | `2` | old `[[ -e ]]` guard **already refuses**; prior evidence intact — **recorded as no-defect at this point**, not as a manufactured RED | `3` | `RP0_STOP reason=evidence_leaf_not_creatable … rc=1`; prior evidence intact |
| R0-1b | retry-in-place / run-ID reuse | `0` | the rejected rc-2 contract permits a re-run with a new leaf name in the same directory; a second leaf was created | `3` | `RP0_STOP reason=evidence_allocation_failed … File exists run_id_burned=yes` |
| R0-2 | **dangling evidence symlink (F1)** | `0` | `-e` false for a dangling link → guard passed → redirection followed the link and **created the target outside the evidence path** (`victim exists after RED: yes`) | `3` | `RP0_STOP reason=evidence_leaf_not_creatable`; `victim exists after GREEN: no` |
| R0-3 | parent replaced by a symlink | `0` | no parent-chain check exists; wrote through the link into the real target directory | `1` | `RP0_FAIL reason=evidence_parent_is_symlink kind=link_live` |
| R0-4 | denied / path-probe error | `0` | under a stub `stat` returning rc 1 "Permission denied", the old block never probes and proceeds | `3` | `RP0_STOP reason=path_probe_error … rc=1 detail=… Permission denied` |
| R0-5 | `pgrep` rc `2`, empty output | `0` | `RED_OLD_BLOCK_CONCLUDED_NO_WRITER_SURVIVED` | `3` | `RP0_STOP reason=pgrep_status pattern=bridge\.app rc=2 out=` |
| R0-6 | `is-enabled` non-token error, empty output | `0` | `C2A_is_enabled=Failed to get unit file state: Connection timed out` → `RED_OLD_BLOCK_CONCLUDED_UNMASKED` | `3` | `RP0_STOP reason=is_enabled_unadjudicable … rc=4 token=[]` |
| R0-7 | positive control, clean fixture | — | — | `0` | parent chain OK, `evidence_dir_allocated`, leaf created and holding `RP0_EVIDENCE run_id=RUN-7 …` |
| R0-8 | positive control, documented `static` token | — | — | `0` | `rp0_is_enabled_token` returns `static` for rc `1` |

**Round 2 — evidence-tree escape (finding R1).** RED = the exact round-1 `RP0-LIB` +
`RP0-BOOTSTRAP` (blob digests `ecb665f4…` / `d909ceaf…`, reproduced from `7194b895`); GREEN = the
blocks above. Same fixture, same stubs, same runner; only the identifier values differ.

| # | Falsification | RED rc | RED observed | GREEN rc | GREEN observed |
|---|---|---|---|---|---|
| R1-1 | **`EV_STAGE_ID=../escaped-t` (R1)** | `0` | allocation and the block both succeed; `leaf created outside EV_DIR: fx_r1/parent/runkit/escaped-t.log`, `files inside EV_DIR: 0` — §1.5 would hash an empty tree while the real evidence sits beside it | `1` | `RP0_FAIL reason=component_charset name=EV_STAGE_ID value=[../escaped-g]`; nothing created |
| R1-2 | **`RUNID=../evilrun-t` (R1)** | `0` | `evidence_dir_allocated dir=…/runkit/../evilrun-t`; the whole evidence **directory** lands outside the runkit (`fx_r1/parent/evilrun-t`) | `1` | `RP0_FAIL reason=component_charset name=RUNID value=[../evilrun-g]`; nothing created |
| R1-3 | second containment layer, called directly with the string validator bypassed | — | — | `1`,`1`,`0` | `leaf_not_direct_child` for `…/RUN-TRAV/../escaped.log` **and** for a sibling-directory leaf; `leaf_contained` rc `0` for a genuine direct child |
| R1-4 | positive control, clean identifiers | — | — | `0` | `component_ok` ×2, `leaf_contained` ×2, `evidence_dir_allocated`, leaf `…/RUN-R2-OK2/stage-c2.log` created **inside** `EV_DIR` |
| R1-5 | cgroup property unreadable / blank (falsification 8) | — | — | `3` | see §8.6 R2-3 and R2-3b: `RP0_STOP reason=cgroup_property_failed …` and `RP0_STOP reason=cgroup_property_unparsable … out=[]` |

### 8.3 RP1 — B3 bounded admission (F2)

RED = exact rejected B3 text, lines `144-181`, except R1 `B3-8` which uses a deliberate mutation
of the repaired helper (a mode **set** `^(want|770)$` instead of the candidate's exact mode).
GREEN = this document's `RP1-B3`.

| # | Fixture | RED rc | RED observed | GREEN rc | GREEN observed |
|---|---|---|---|---|---|
| B3-0 | candidate-conformant baseline | `0` | `B3 PASS` | `0` | `B3 PASS` |
| B3-1 | release root mode `0444` | `0` | `B3 PASS` — the regex `^(555\|444)$` accepts it | `1` | `B3_FAIL … mode=444 expected=555` |
| B3-2 | group-writable-only child `0020` | `0` | `B3 PASS` — `-perm -0200` does not match a group-only write bit | `1` | `B3_FAIL reason=writable path inside immutable tree: …/lib/group_writable_0020` |
| B3-3 | other-writable-only child `0002` | `0` | `B3 PASS` — same owner-write-only blind spot | `1` | `B3_FAIL reason=writable path inside immutable tree: …/lib/other_writable_0002` |
| B3-4 | wrong candidate release SHA | `0` | `B3 PASS` — the rejected block has no binding check at all | `1` | `B3_FAIL reason=install manifest does not bind release_sha` |
| B3-5 | wrong release/payload manifest SHA | `0` | `B3 PASS` | `1` | `B3_FAIL reason=install manifest does not bind release_manifest_sha256` |
| B3-6 | unreadable install manifest (`grep` rc 2) | `0` | `B3 PASS` | `3` | `B3_STOP reason=install_manifest_unreadable … grep_rc=2` |
| B3-7 | failed `find` after partial output | `1` | `B3_FAIL reason=find over release tree failed` — fails, but as an assertion failure with the tool error text conflated into the offender variable | `3` | `B3_STOP reason=writable_inventory_failed … rc=1 detail=… Permission denied partial=[…/partial_entry]` — the two outcome classes are kept apart and the partial output is preserved |
| B3-7b | `find` rc `0` with stderr noise | `1` | `B3_FAIL reason=release tree has a write bit set somewhere` — a **fabricated offender**, because `2>&1` puts stderr into the offender variable | `0` | `B3 PASS` — stderr is captured separately |
| B3-8 | ancillary path mode drift `0750`→`0770` | `0` | `B3 PASS` under the mutated mode-set comparison | `1` | `B3_FAIL reason=path=/var/log/mtc-bridge mode=770 expected=750` |

### 8.4 RP4 — C3 restore-into-temp (F6)

**Fully real execution:** real CPython, real SQLite, the real candidate module, real bundles
produced by the candidate's own `create` subcommand (`rc=0`, verdict `CAPTURED`). No stub.

| # | Fixture | rc | Observed |
|---|---|---|---|
| R4-0 | positive control | `0` | `C3_restored_quick_check=ok`, `C3_restored_fk_violations=0`, `C3_restored_invariants_sha256=76af567e…` equal to the candidate-produced `invariants_sha256`, `C3_protected_fields_equal=yes`, three distinct inodes, `C3_sidecars_absent=yes`, `C3 PASS` |
| R4-1 **RED** | exact rejected call `collect_invariants(<str path>)` | `1` | `AttributeError: 'str' object has no attribute 'execute'` at candidate `wal_state_bundle.py:401` via `:425` — the F6 defect, reproduced |
| R4-1 **GREEN** | `collect_invariants(conn)` + candidate `invariants_hash` | `0` | `GREEN_invariants_sha256=76af567ea61fcf3de52bd0e1cd2fec9591f9bbd21837aaec2cfdf343070b1318` |
| R4-2 | wrong invariant in the accepted bundle | `1` | `C3_FAIL reason=protected invariant field differs after restore: counts`; `C3_ARTIFACTS_PRESERVED label=failed root=…`; `restored.db exists = True` |
| R4-3 | wrong bundle DB hash | `1` | `C3_FAIL reason=bundle database sha256 does not match the accepted manifest value` |
| R4-3b | wrong external manifest-**file** SHA | `1` | `C3_FAIL reason=bundle manifest FILE sha256 does not match the accepted value` |
| R4-4 | pre-existing restore destination | `1` | `C3_FAIL reason=restore root already exists: …`; prior artifact intact (`b'PRIOR-ARTIFACT'`) |
| R4-5 | dangling restore-destination link | — | **NOT EXERCISED — BLOCKED.** `os.symlink` refused (`WinError 1314`, privilege not held); a junction is not `Path.is_symlink()`; MSYS `.lnk` emulation is invisible to CPython. **Not claimed closed.** The equivalent shell-level predicate is closed by R0-2. |
| R4-6 | aliased inode (real hard link) | `1` | `C3_FAIL reason=source/bundle/restored are not three distinct files: {…}` with the two identical `(device, inode)` pairs printed |
| R4-7 | sidecar appearance | `1` | `C3_FAIL reason=sidecar present beside bridge.db: bridge.db-wal` |
| R4-8 | corrupted bundle DB | `3` | `C3_STOP reason=integrity_probe_failed: DatabaseError: database disk image is malformed`; `C3_ARTIFACTS_PRESERVED label=stopped root=…` |
| R4-9 | real foreign-key violation in the restored DB | `1` | `C3_restored_quick_check=ok`, `C3_restored_fk_violations=1`, `C3_FAIL reason=restored foreign_key_check found 1 violation(s)` |

**Round 2 — mandatory candidate re-verification (finding R3).** RED = the exact round-1 `RP4-C3`
(blob digest `4e1b7c64…`); GREEN = the block above. Fully real: real CPython, real SQLite, the real
candidate module, and a real bundle produced by the candidate's own `create`
(`verdict=CAPTURED`, `invariants_sha256=3de368ef…`). The tampered cases alter **only manifest
fields that no local check in either block reads**, and the externally recorded manifest-FILE SHA
is taken from the tampered file — so manifest-identity equality is satisfied and only the
candidate's own verification can see the defect.

| # | Fixture | RED rc | RED observed | GREEN rc | GREEN observed |
|---|---|---|---|---|---|
| R3-0 | positive control, untampered accepted bundle | — | — | `0` | `C3_candidate_verify_rc=0 verdict=VALID failures=[]`, then `quick_check=ok`, `fk=0`, restored hash equal, three distinct inodes, `C3 PASS` |
| R3-1 | **manifest `source.integrity_check` tampered (R3)** | `0` | `C3 PASS` — every local check passes; the block never asks the candidate | `1` | `C3_candidate_verify_rc=2 verdict=INVALID failures=['source_checks_not_clean']` → `C3_FAIL`, artifacts preserved |
| R3-2 | **manifest records bundle sidecars (R3)** | `0` | `C3 PASS` — `assert_no_sidecars` inspects the filesystem, never the manifest's own record | `1` | `C3_candidate_verify_rc=2 verdict=INVALID failures=['manifest_records_bundle_sidecars']` → `C3_FAIL` |
| R3-3 | manifest `bundle.db_sha256` is not a SHA-256 | `1` | fails, but as `C3_FAIL reason=bundle database sha256 does not match…` — a candidate **contract** violation misread as drift, and only after the restore | `3` | `C3_STOP reason=candidate_verify_unevaluable: BundleError: expect_bundle_sha256 must be exactly 64 hex characters`, before any restore |
| R3-4 | preregistered invariants hash is not the manifest's | — | RED takes no such argument | `1` | `C3_FAIL reason=manifest invariants_sha256 is not the externally recorded accepted value` |

### 8.5 RP5 — C4 rollback stop+mask-only (F7, F8)

RED = exact rejected C4 text, lines `751-786`. GREEN = this document's `RP5-C4`.

| # | Fixture | RED rc | RED observed | GREEN rc | GREEN observed |
|---|---|---|---|---|---|
| R5-0 | positive control | — | — | `0` | `C4_dry_run_mutation_free=yes`, mask raw target `/dev/null`, `C4_rollback_manifest_mode=640 owner=root:root`, `C4_manifest_fields_validated=all`, `C4 PASS` |
| R5-1 | **pre-existing regular rollback manifest (F7)** | `0` | `C4 PASS` — and the prior record `{"PRIOR":"ROLLBACK-RECORD-2026-08-01"}` **was overwritten** by the unconditional `cat >` | `1` | `C4_FAIL reason=rollback manifest must be absent as object AND link, found regular`; prior record **intact** |
| R5-2 | dangling rollback-manifest link | `1` | `C4_FAIL reason=rollback.sh (stop+mask-only) exited nonzero` — it fails, but only **after** invoking the mutating script | `1` | `C4_FAIL … found link_live` — refused **before** any invocation; the link target was never created |
| R5-3 | dry run that mutates | `0` | `C4 PASS` — the rejected block performs no dry-run rehearsal at all | `1` | `C4_FAIL reason=dry run mutated observable state: [active=active enabled=static mask=absent …] -> [active=inactive enabled=masked mask=link_live …]` |
| R5-4 | **same-size protected DB mutation (F8)** | see note | the rejected `find -printf '%f %s'` snapshots are **EQUAL** before and after a real SQLite mutation (`orders.status 'OPEN'→'FILL'`, `trades.pnl -5.0→-9.0`, `size_before=size_after`), so the rejected block reports "byte-for-byte preservation" — a **false PASS** | `1` | `C4_FAIL reason=protected invariants changed across rollback (pre=91189251… post=1927f86b…)` using the candidate `invariants_hash` |
| R5-5 | wrong accepted C3 state-manifest hash | `1` | `C4_FAIL reason=rollback.sh … exited nonzero` — caught only by the candidate script, after invocation | `1` | `C4_FAIL reason=C3 manifest file sha256=baa13447… expected=eeee…` — caught at prerequisite 1 |
| R5-6 | wrong mask-link target | `0` | `C4 PASS` — only `is-enabled == masked` is checked | `1` | `C4_FAIL reason=mask link raw target=…/decoy_target expected exactly /dev/null` |
| R5-7 | unexpected rebind fields in the manifest | `0` | `C4 PASS` — the manifest is only `stat`-ed, never validated | `1` | `C4_manifest_problems=rollback_release_sha='deadbeef…' expected ''; rollback_release_manifest_sha256='bbbb…' expected ''` |
| R5-8 | failed post-rollback invariant equality | `0` | `C4 PASS` — no invariant comparison exists in the rejected block | `1` | `C4_FAIL reason=protected invariants changed across rollback (pre=INV-BASELINE post=INV-DRIFTED)` |
| R5-9 | rollback manifest mode drift `0640`→`0644` | `0` | `C4 PASS` — the mode is printed, never asserted | `1` | `C4_FAIL reason=rollback manifest mode=644 expected 640` |

**Round-1 rows R5-4 and R5-8 are superseded.** They proved only that two *unequal* injected
strings are rejected. They did **not** establish that the post-rollback value comes from a fresh
verified bundle, which is the actual persistence predicate; that gap is finding R4 and is closed
by the round-2 table below, not by those rows.

**Round 2 — fresh verified post-rollback bundle and fingerprint adjudication (findings R4, R5).**
**Superseded, and retained only as a record.** The block these rows exercised no longer exists: the
round-2 re-audit falsified its freshness predicate (`RR2-2`) and its fingerprint (`RR2-3`), and §6 is
now three stage blocks. Rows `R4-0`…`R4-4` are **not** closure evidence for the post-rollback
requirement — that is the round-3 evidence below. Rows `R4-5`…`R4-9` and `R5-10`…`R5-12` describe
predicates that survive into `RP5-C4A`/`RP5-C4C` and are re-exercised there.
RED = the exact round-1 `RP5-C4` (blob digest `e13b8666…`); GREEN = the round-2 block. The fixture
holds three **real** candidate bundles created by the candidate's own `create` from one unchanged
source database, so their protected invariants are genuinely equal
(`3de368ef…`) while the artifacts are distinct: `bundle_pre` (accepted C3, captured
`2026-08-09T12:00:00Z`), `bundle_post` (`12:45:00Z`, after the stub rollback's recorded
`12:30:00Z`) and `bundle_stale` (`11:00:00Z`).

| # | Fixture | RED rc | RED observed | GREEN rc | GREEN observed |
|---|---|---|---|---|---|
| R4-0 | positive control | — | — | `0` | `C4_post_bundle_verify_rc=0 verdict=VALID failures=[]`, distinct pre/post identity pairs, `generated_at_utc=2026-08-09T12:45:00Z > rolled_back_at_utc=2026-08-09T12:30:00Z`, `C4_post_rollback_bundle_verified=yes`, `C4_cgroup_survivors=0`, `C4 PASS` |
| R4-1 | **unbound strings — the exact audited reproduction (R4)** | `0` | `C4_c3_manifest_sha256=fd51e6c3…` over a dummy `{"accepted":"c3-bundle-manifest"}` file, `C4_invariants_equal=yes sha256=INV-BASELINE`, `C4 PASS` | `3` | `C4_STOP reason=candidate_verify_unevaluable: BundleError: expect_invariants_sha256 must be exactly 64 hex characters` → `C4_STOP reason=post_rollback_bundle_unevaluable rc=3` |
| R4-2 | **accepted C3 bundle re-submitted as the "fresh" post bundle (R4)** | `0` | `C4 PASS` — two equal strings are all the rejected predicate ever compares | `1` | `C4_post_bundle_problems=post bundle manifest IS the accepted C3 manifest: no fresh capture happened; post bundle predates the rollback (12:00:00Z <= 12:30:00Z): it is stale` |
| R4-3 | stale bundle captured **before** the rollback | `0` | `C4 PASS` | `1` | `C4_post_bundle_problems=post bundle predates the rollback (2026-08-09T11:00:00Z <= 2026-08-09T12:30:00Z): it is stale` — candidate verify had already returned `VALID`, so only the freshness binding catches it |
| R4-4 | post manifest FILE sha ≠ the recorded capture value | `0` | `C4 PASS` | `1` | `C4_post_bundle_problems=fresh bundle manifest FILE sha256 does not match the recorded capture value` |
| R4-5 | **cgroup survivor after rollback (R4)** | `0` | `C4 PASS` — no cgroup predicate exists; the writer pattern and the port both report clean | `1` | `C4_cgroup_survivors=1` → `C4_FAIL reason=the unit cgroup still holds 1 process(es) after rollback stop+mask` |
| R4-6 | fresh bundle the candidate `verify` rejects | `0` | `C4 PASS` | `1` | `C4_post_bundle_verify_rc=2 verdict=INVALID failures=['source_checks_not_clean']` → `C4_FAIL` |
| R4-7 | regression: dry run that mutates | — | — | `1` | `C4_FAIL reason=dry run mutated observable state: [… cgroup=0 manifest=absent …] -> [active=inactive enabled=masked mask=link_live …]` — the fingerprint now also carries the cgroup count |
| R4-8 | regression: rebind field in the rollback manifest | — | — | `1` | `C4_manifest_problems=rollback_release_sha='deadbeef…' expected ''` → `C4_FAIL` |
| R4-9 | regression: pre-existing regular rollback manifest (F7) | — | — | `1` | `C4_FAIL reason=rollback manifest must be absent as object AND link, found regular`; prior record `{"PRIOR":"ROLLBACK-RECORD-2026-08-01"}` **intact** |

**Fingerprint adjudication (R5).** The exact `c4_sha256` + `c4_fingerprint` text was extracted from
each version and executed with the surrounding predicates stubbed, so the only variable is the
function body itself.

| # | Condition | RED rc | RED observed | GREEN rc | GREEN observed |
|---|---|---|---|---|---|
| R5-10 | clean control | `0` | full fingerprint string | `0` | full fingerprint string, now including `cgroup=0` |
| R5-11 | **rollback-manifest path probe returns STOP (R5)** | `0` | `FINGERPRINT=[… writers_rc=1 manifest= c3=cbf30559…]` — the STOP became an **empty field** and the function still succeeded | `3` | `FINGERPRINT_RC=3`, `FINGERPRINT=[]`; no before/after equality is computed |
| R5-12 | **C3 manifest hash cannot be taken (R5)** | `0` | worse than an empty field: `c3=C4_STOP reason=sha256_failed path=…` — the STOP **message** is captured as the hash value, so two failing fingerprints could compare equal | `3` | `C4_STOP reason=sha256_failed … rc=1 detail=sha256sum: … No such file or directory` on stderr, `FINGERPRINT_RC=3`, `FINGERPRINT=[]` |

**Round 3 — the accepted bypass, and the three-stage causal repair (finding RR2-2).**
RED = the exact audited round-2 `RP5-C4` (blob digest `dbab2306…`, re-extracted from `75ee8912`);
GREEN = `RP5-C4A` → `RP5-C4B` → `RP5-C4C`. Fully real where it matters: real CPython, real SQLite,
the real candidate module, real bundles produced by the candidate's own `create`, and real candidate
`verify_bundle`. Only `systemctl`, `pgrep`, `ss`, `stat`, `mkdir` and `rollback.sh` are local stubs.

The RED fixture is the falsification the re-audit demanded. A **candidate-valid** bundle is created
at the capture destination **before anything runs**, from the same unchanged source database, with an
operator-supplied `--timestamp` one hour in the future — the exact lever
`wal_state_bundle.py:1218-1222` provides. Its three digests are then handed to the block as its
preregistered post-rollback inputs, which is the only thing the round-2 design allowed.

| # | Fixture | RED rc | RED observed | GREEN rc | GREEN observed |
|---|---|---|---|---|---|
| RR2-2-1 | **candidate-valid bundle already at the capture destination (the audited bypass)** | `0` | `C4_post_bundle_verify_rc=0 verdict=VALID`, `C4_post_rollback_bundle_verified=yes`, `C4 PASS` — on an artifact whose manifest mtime is **seconds older** than the rollback manifest the same run wrote | `1` | `C4_post_dest_pre_kind=dir` → `C4_FAIL reason=capture destination must be absent as object AND link before any mutation, found dir`, raised in `step0_prerequisites`; mask link absent, `sysd` unchanged, no rollback manifest, no stage record, and the planted bundle left intact — **the refusal costs no mutation at all** |
| RR2-2-2 | a candidate-valid bundle planted **between** stages A and B | — | the round-2 block has no such stage boundary | `1` | `C4B_dest_pre_capture_kind=dir` → `C4B_FAIL reason=capture destination is not absent (dir): a pre-existing artifact is never adopted as the fresh capture` |
| RR2-2-3 | **a truthful capture record for a bundle captured before the rollback** — every identity field honest, the record's own digest recorded externally, the candidate accepting the bundle | `0` | the same acceptance as RR2-2-1: the round-2 block has no stage record and no capture step, so a bundle taken before the rollback and carrying a later claimed timestamp is precisely what its predicates admit | `1` | `C4C_post_bundle_verify_rc=0 verdict=VALID` — the candidate accepts it, artifact identity matches, the second-granularity clock check passes — and it is still refused: `C4C_post_bundle_problems=the recorded capture is not strictly newer than the recorded rollback` |
| RR2-2-4 | the fresh bundle **manifest** altered after capture | — | no capture stage exists to bind to | `1` | `the fresh bundle manifest is not the artifact stage B captured, or changed since; …FILE sha256 does not match the recorded capture value; candidate verify rejected…['source_checks_not_clean']` |
| RR2-2-5 | the fresh bundle **database** mutated same-size after capture (the F8 shape, `size_before=size_after=65536`) | — | — | `1` | manifest identity still matches, so only the candidate can see it: `C4C_post_bundle_verify_rc=2 verdict=INVALID failures=['bundle_db_hash_mismatch', 'bundle_db_hash_not_expected', 'invariants_drift', 'invariants_hash_mismatch', 'invariants_hash_not_expected']` |
| RR2-2-6 | protected invariants genuinely drift: the **live** state DB is mutated same-size after the rollback, then captured | — | — | `1` | stage B legitimately captures a valid bundle of the drifted state; stage C refuses — `protected invariants changed across rollback (pre=3de368ef… post=…)` plus the differing protected fields |
| RR2-2-7 | the rollback manifest **rewritten** between stages A and B | — | — | `1` | `C4B_FAIL reason=the rollback manifest changed since stage A: this capture cannot be bound to that rollback`, with the live and pinned `(dev, ino, mtime_ns, sha256)` tuples both printed |
| RR2-2-8 | the externally recorded **stage-record digest** does not match | — | — | `1` | `C4B_FAIL reason=stage record sha256 does not match the externally recorded value` |
| RR2-2-0 | **positive control** — A, then B, then C, on a genuinely fresh capture | — | — | `0`,`0`,`0` | A: `C4_dry_run_mutation_free=yes`, mask target `/dev/null`, `C4_manifest_fields_validated=all`, `C4_post_dest_post_kind=absent`, `C4A PASS`. B: `C4B_capture_rc=0 verdict=CAPTURED`, fresh manifest `mtime_ns` strictly greater than the rollback's, `C4B PASS`. C: `C4C_post_bundle_verify_rc=0 verdict=VALID failures=[]`, `C4C_post_rollback_bundle_verified=yes`, `C4C PASS` |

Regressions re-exercised on stage A in the same run, each `1`: pre-existing regular rollback manifest
(F7 — `C4_FAIL reason=rollback manifest must be absent as object AND link, found regular`, prior
record `{"PRIOR":"ROLLBACK-RECORD-2026-08-01"}` intact); a dry run that mutates (and the failure line
now carries the inventory digests); a rebind field in the rollback manifest
(`C4_manifest_problems=rollback_release_sha='deadbeef…' expected ''`); and a cgroup survivor after
the rollback (`the unit cgroup still holds 1 process(es) after rollback stop+mask`).

**The wrong-mask-target case is still not presentable here, and no claim is made for it.** On this
MSYS mount the stub `ln -s` to a non-`/dev/null` target fails outright, so stage A refuses at
`C4_FAIL reason=rollback.sh (stop+mask-only) exited nonzero` and **never reaches** the mask-target
predicate. The transcript row is labelled that way rather than as a mask-target falsification. This
is the same standing limitation as §8.7 gap 7; the round-1 `R5-6` record stands on its own evidence.

The decisive line is `RR2-2-3`. It is the round-2 bypass reduced to its strongest form — an artifact
the candidate itself calls `VALID`, described by a record in which nothing is a lie — and it is still
refused, because the ordering witness is the OS-set `st_mtime_ns` of two files rather than a field an
operator can choose. `RR2-2-1` and `RR2-2-2` are the structural refusals that make that witness
sufficient rather than decorative.

```text
# RED — the audited round-2 RP5-C4, on a bundle planted BEFORE the rollback
planted manifest mtime      : 2026-08-09 14:38:47.763027300 +0300
rollback manifest before run: absent
C4_post_bundle_generated_at_utc=2026-08-09T12:38:47Z rolled_back_at_utc=2026-08-09T11:38:55Z
C4_post_bundle_verify_rc=0 verdict=VALID failures=[]
C4_post_rollback_bundle_verified=yes
C4 PASS (unit stopped and masked; no start, unmask or recovery is authorised by this result)
BLOCK_RC=0
rollback manifest mtime after: 2026-08-09 14:38:55.891541300 +0300

# GREEN — RP5-C4A on the SAME fixture: refused in step0, nothing mutated
C4_post_dest_pre_kind=dir
C4_FAIL reason=capture destination must be absent as object AND link before any mutation, found dir
BLOCK_RC=1
mask symlink   : absent
sysd           : IsEnabled=static ActiveState=active ControlGroup=/system.slice/mtc-bridge-first-start.service 
rollback mfst  : absent
stage record   : absent
planted bundle : INTACT

# GREEN — RP5-C4C on a TRUTHFUL capture record for a pre-rollback bundle
FORGED_post_mtime_ns=1786275586007141200
PINNED_rollback_mtime_ns=1786275594650652400
C4C_generated_at_utc=2026-08-09T12:38:47Z rolled_back_at_utc=2026-08-09T11:39:54Z post_mtime_ns=1786275586007141200 rollback_mtime_ns=1786275594650652400
C4C_post_bundle_verify_rc=0 verdict=VALID failures=[]
C4C_post_bundle_problems=the recorded capture is not strictly newer than the recorded rollback
C4C_FAIL reason=fresh post-rollback bundle binding failed (see C4C_post_bundle_problems)
BLOCK_RC=1
```

**Round 3 — identity inventories in the dry-run fingerprint (finding RR2-3).** RED = the exact
`c4_sha256` + `c4_fingerprint` text of the audited round-2 `RP5-C4`; GREEN = the same functions from
`RP5-C4A`. Everything else is shared and real: the same fixture, the same stubs, and the **real**
`RP0-LIB` predicates on both sides — no `rp0_*` function is replaced by a local stand-in. Each case
takes a fingerprint, changes exactly one thing **without changing any count**, and takes it again.

| # | Condition | RED rc | RED observed | GREEN rc | GREEN observed |
|---|---|---|---|---|---|
| RR2-3-0 | clean control, nothing changed | `0` | fingerprints equal | `0` | fingerprints equal, now carrying `writers=`/`listeners=`/`cgroup=` inventory digests |
| RR2-3-1 | **one bridge writer replaced by another at the same count** (`pid 1111` → `pid 2222`, identical command line) | `0` | `writers_rc=0` both sides, `FP_EQUAL=yes` — the block concludes the dry run mutated nothing | `1` | `writers=` digest differs, `FP_EQUAL=no` — the block FAILS with `dry run mutated observable state` |
| RR2-3-2 | **one listening socket replaced by another at the same count** (same address, owner `pid 1111` → `pid 2222`) | `0` | `listeners=1` both sides, `FP_EQUAL=yes` | `1` | `listeners=` digest differs, `FP_EQUAL=no` |
| RR2-3-3 | **one cgroup member replaced by another at the same count** (`cgroup.procs` `1111` → `2222`) | `0` | `cgroup=1` both sides, `FP_EQUAL=yes` | `1` | `cgroup=` digest differs, `FP_EQUAL=no` |
| RR2-3-4 | a listening socket whose **owning process cannot be resolved** (no `users:((…))` field) | `0` | counted as one listener and read as unchanged | `3` | `RP0_STOP reason=listener_owner_unresolved port=8790 line=[…]`, `FP_BEFORE=[]`, and **no** equality is computed |
| RR2-3-5 | regression: the rollback-manifest path probe returns COULD NOT EVALUATE | `3` | already correct after round 2 — `FP_RC=3`, empty value | `3` | `RP0_STOP reason=path_probe_error … Permission denied`, `FP_BEFORE=[]`; here the STOP comes from the **real** `rp0_probe_path` driven by a failing `stat`, not from a stubbed predicate |

Rows `RR2-3-1` to `RR2-3-3` are the re-audit's reproduction, re-derived independently: a status code
and two counts cannot express identity, so "the dry run mutated nothing" was satisfiable by a mutated
host. Row `RR2-3-4` is the fail-closed half — an unresolvable owner must not be read as the same
listener.

```text
# RED — round-2 fingerprint, one writer replaced by another at the same count
FP_BEFORE_RC=0 FP_BEFORE=[active=active enabled=static mask=absent listeners=1 writers_rc=0 cgroup=1 manifest=absent c3=3f3783254814413407abc4ecf8ea79a199bd6f23305e3553ccf0062428520ecd]
FP_AFTER_RC=0 FP_AFTER=[active=active enabled=static mask=absent listeners=1 writers_rc=0 cgroup=1 manifest=absent c3=3f3783254814413407abc4ecf8ea79a199bd6f23305e3553ccf0062428520ecd]
FP_EQUAL=yes  -> the block concludes "the dry run mutated nothing"
FP_SCRIPT_RC=0   (0 = fingerprints equal, 1 = differ, 3 = STOP)

# GREEN — RP5-C4A fingerprint, identical fixture and identical change
FP_BEFORE_RC=0 FP_BEFORE=[active=active enabled=static mask=absent manifest=absent c3=3f3783254814413407abc4ecf8ea79a199bd6f23305e3553ccf0062428520ecd writers=5a16423f0d424f5a455cebb278054df35a8b8cec852579f5a0034bfb37646d2b listeners=d0f012a1f9078ee071a629dbc769534db078857518a4adbaf371498ef04267f9 cgroup=97f2a4c4f288beff6085b1f887971a8a6ab8159a1095142427803da52cab3dfd]
FP_AFTER_RC=0 FP_AFTER=[active=active enabled=static mask=absent manifest=absent c3=3f3783254814413407abc4ecf8ea79a199bd6f23305e3553ccf0062428520ecd writers=04142051bb47c4c069493a8ce11a18237d8d4b635846515fa3332f509090ac2e listeners=d0f012a1f9078ee071a629dbc769534db078857518a4adbaf371498ef04267f9 cgroup=97f2a4c4f288beff6085b1f887971a8a6ab8159a1095142427803da52cab3dfd]
FP_EQUAL=no   -> the block FAILS: dry run mutated observable state
FP_SCRIPT_RC=1   (0 = fingerprints equal, 1 = differ, 3 = STOP)

# GREEN — a listening socket whose owning process cannot be resolved
RP0_STOP reason=listener_owner_unresolved port=8790 line=[LISTEN 0 4096 0.0.0.0:8790 0.0.0.0:*]
RP0_STOP reason=listener_owner_unresolved port=8790 line=[LISTEN 0 4096 0.0.0.0:8790 0.0.0.0:*]
FP_BEFORE_RC=3 FP_BEFORE=[]
FP_VERDICT=STOP rc=3 (no before/after equality is computed)
```

**Round 3 — the rerun contract (finding RR2-4).** The two cases below are precisely the positive
controls that failed on a second invocation of the round-2 runner. `run_all_r3.sh` was invoked twice
in a row, with no cleanup between the runs.

| # | Case | Run 1 | Run 2 |
|---|---|---|---|
| RR2-4-1 | `RP0-BOOTSTRAP` positive control with a per-invocation run ID and stage ID | `0` — `evidence_dir_allocated`, leaf created inside `EV_DIR`, `RP0_EVIDENCE run_id=RUN-R3-<suffix>` | `0` — same, under a **different** suffix; round 2 failed here with `evidence_allocation_failed … File exists run_id_burned=yes` |
| RR2-4-2 | `RP4-C3` positive control with a per-invocation restore root | `0` — `C3 PASS` | `0` — `C3 PASS`; round 2 failed here with `C3_FAIL reason=restore root already exists` |

Every `OUTCOME` line of the two runs is identical, and the run summary of each reports the same
number of expected outcomes with zero harness problems. What differs between the runs is only what
must: the run suffix, fixture paths, inode numbers, mtimes, and the digests of the bundles the
candidate freshly captured.

```text
# two CONSECUTIVE invocations of the preserved run_all_r3.sh, no cleanup between them
run 1 summary : run suffix        : run.jfw3ap expected outcomes : 41 harness problems  : 0 
run 2 summary : run suffix        : run.ob05NQ expected outcomes : 41 harness problems  : 0 

# the two runs OUTCOME-line comparison:
diff of all OUTCOME lines: IDENTICAL (41 lines)

# the two cases the round-2 runner could not replay, in run 2:
OUTCOME S1-1 RP0-BOOTSTRAP positive control, fresh run ID: rc=0 as expected
OUTCOME S1-2 RP4-C3 positive control, fresh restore root: rc=0 as expected
RP0_EVIDENCE run_id=RUN-R3-run.ob05NQ dir=/tmp/D026R3.QgHw2b/fx/run.ob05NQ/rp0/parent/runkit/RUN-R3-run.ob05NQ leaf=/tmp/D026R3.QgHw2b/fx/run.ob05NQ/rp0/parent/runkit/RUN-R3-run.ob05NQ/stage-run.ob05NQ.log
C3 PASS
```

### 8.6 RP3 — C2 post-reboot postconditions (F4/F5 follow-up, finding R2)

**Status first: this closes nothing at the scenario level.** Both C2 scenarios remain BLOCKED on
C1-GAP-B, no real pre-mutation baseline exists, and no host was involved. What is exercised below
is the **block text** of the two post-reboot assertion halves under local stubs, to falsify the two
postconditions that were missing. RED = the exact round-1 `RP3-C2A-POST` / `RP3-C2B-POST` (blob
digests `e17a8e32…` / `6ed40735…`); GREEN = the blocks above. `systemctl`, `pgrep` and `ss` are
stubs; the cgroup tree is a fixture directory with real `cgroup.procs` files; the invariant
documents are fixtures supplied as the blocks' declared INPUTS.

| # | Fixture | RED rc | RED observed | GREEN rc | GREEN observed |
|---|---|---|---|---|---|
| R2-1 | **Scenario A: one cgroup survivor, no writer match, no listener (R2)** | `0` | `C2A_writers=0`, `C2A_listener_count=0`, `C2A PASS` — a surviving process is simply invisible to the two predicates present | `1` | `C2A_cgroup_survivors=1` → `C2A_FAIL reason=the unit cgroup still holds 1 process(es) after reboot` |
| R2-2 | **Scenario A: `app_state=ARMED` on both sides (R2)** | `0` | `C2A_invariants_equal=yes`, `C2A PASS` — equality accepts "ARMED before, ARMED after"; the round-1 block mentioned `app_state != ARMED` only in a comment | `1` | `C2A_app_state=ARMED` → `C2A_FAIL reason=app_state=ARMED after reboot; the unit must not return armed` |
| R2-3 | cgroup property unreadable (`systemctl show` rc 1) | — | no predicate exists | `3` | `RP0_STOP reason=cgroup_property_failed unit=mtc-bridge-first-start.service rc=1` |
| R2-3b | cgroup property blank / unparsable | — | no predicate exists | `3` | `RP0_STOP reason=cgroup_property_unparsable unit=… out=[]` — never "no survivor" |
| R2-4 | Scenario A positive control | — | — | `0` | `C2A_cgroup_survivors=0`, `C2A_app_state=DISARMED`, `C2A_invariants_equal=yes`, `C2A PASS` |
| R2-5 | **Scenario B: two cgroup survivors (R2)** | `0` | `C2B PASS` | `1` | `C2B_cgroup_survivors=2` → `C2B_FAIL reason=the unit cgroup still holds 2 process(es) after a masked reboot` |
| R2-6 | Scenario B positive control | — | — | `0` | `C2B_cgroup_survivors=0`, `C2B_invariants_equal=yes`, `C2B PASS` |

### 8.7 Standing D026 gaps — explicitly not closed

1. **R4-5** (dangling restore destination, Python level) — no execution route on this machine.
   Unchanged in round 2: CPython here still cannot create a symlink (`WinError 1314`).
2. **All C1 falsifications** (`C1-F1`…`C1-F9`, §3.3) — C1 is BLOCKED; manufacturing runs for a
   blocked path is forbidden.
3. **All scenario-level C2 falsifications** (`C2-F1`…`C2-F7`, §4.6) — the scenarios are BLOCKED
   on C1-GAP-B. The predicate-level cases `C2-F1`, `C2-F2`, `C2-F4` and `C2-F5` are covered by
   the RP0-LIB runs above; `C2-F3`, `C2-F6` and `C2-F7` are **not claimed closed**. §8.6 exercises
   the two **newly added postconditions** of the post-reboot blocks at stub level only; it makes
   no scenario-level claim and does not close any entry in §4.6.
4. **C5** — has no procedure and therefore no falsification.
5. **The real `/sys/fs/cgroup` semantics** were not exercised: this machine has no systemd, so the
   cgroup predicate ran against a fixture tree and a stub `systemctl show -p ControlGroup`. The
   adjudication logic is falsified; its behaviour against a live cgroup v2 hierarchy is not.
6. **The candidate `rollback.sh` itself was never run** — rounds 1, 2 and 3 all used a local stub
   for it. Every RP5 claim is about this document's blocks, never about the candidate script's own
   behaviour.
7. **An arbitrary-target mask link** could not be presented on this MSYS mount: `ln -s` to a
   non-`/dev/null` target materialises a copy, so the repaired block refused the fixture as
   `kind=regular` rather than as a wrong link target. The round-1 `R5-6` record stands on its own
   evidence; rounds 2 and 3 make no new claim for that case.
8. **No real `ss` exists on this machine.** `rp0_listener_inventory` is falsified against
   `ss -H -ltnp` output modelled on documented iproute2 formatting, including the ownerless-line
   STOP. Its parsing of a live socket table, and the privilege conditions under which real `ss`
   omits the `users:((…))` field, are **not** exercised. The predicate's adjudication is falsified;
   its behaviour against real `ss` is not.
9. **PID identity is the cgroup-membership predicate.** A kernel PID recycled onto a different
   process inside the compared window would not be distinguished. Nothing here closes that; it is
   bounded by the dry-run window's length and is disclosed rather than defended.
10. **The three C4 stages were exercised stage by stage, never as an authorized sequence on a
    host.** Each stage boundary in the harness is a shell invocation, not the operator hand-off and
    external recording the design requires. What is falsified is the blocks' adjudication of that
    hand-off, not the hand-off itself.
11. **The causal chain binds a compliant operator, not a hostile root.** Absence-then-creation
    inside one stage, create-once records and `st_mtime_ns` ordering refuse a stale or planted
    artifact; they do not refuse a root who back-dates files, forges both records and rewrites the
    external digests to match. That is a trust boundary. It is why every record is create-once and
    its digest is recorded externally per §1.5, and it is **not** claimed as closed.
12. **`RP1-B3`, `RP3-C2A-POST`, `RP3-C2B-POST` and `RP4-C3` were not re-run in full in round 3.**
    They are byte-identical to round 2 (§8.1 digest table), the twelve `RP0-LIB` predicates they
    call are byte-identical too, and the round-3 runner re-exercises the two positive controls that
    the round-2 runner could not replay. Their remaining rows rest on the round-1/round-2 evidence,
    not on a round-3 execution.

The Lead is expected to reproduce every claimed run independently. Nothing in this section is a
verdict.

---

## 9. What this document is not

- **Not an execution record.** No block above has been run against a host; no host was touched.
- **Not acceptance.** The Lead and fresh auditors own acceptance. This is repair round **3 of at
  most 3** — the final permitted round — for this proposal-repair cycle; it repairs exactly the
  three content findings `RR2-2`, `RR2-3` and `RR2-4` of the re-audit at
  `WPL_P2_PROPOSALS_REAUDIT_ROUND2_2026-08-09.md` and claims nothing beyond them. `RR2-1` is commit
  scope and belongs to the Lead. No round-1 or round-2 finding is reopened, and nothing that was
  BLOCKED is quietly closed.
- **Not permission to extract scripts.** Turning any block into a deployable file is a separate,
  not-yet-granted authorization (repair spec §9.5).
- **Not host authority, budget lift, or per-mutation authorization.** Those remain separate
  later gates. `RP5-C4A` is `mutating-host` and `RP5-C4B` is `mutating-filesystem`; each requires
  its **own** explicit named authority, separately from the other, and neither is granted here.
  `RP5-C4C` is read-only and still confers no authority to act on what it reports.
- **Not a statement that the server is ready.**
- **Not a closure, reopening or repair of the separate blocked `C:\PGRK` design loop.** RP0
  specifies a possible closure route for a similar pre-evidence-root contradiction; it does not
  close, reopen or repair that draft.
- **Not a claim of exact 50-hour reproducibility.** The ledger baseline is the owner-ratified
  figure in `OWNER_DECISION_AUDIT_TIERS_2026-08-09.md` §1; this document reconstructs nothing.
- **Not a change to any other file.** No product, deployment, runtime, tool, test, schema,
  prompt, handoff or AI-memory file was edited to produce this repair.
