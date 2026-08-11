# WP-I transport set self-QA — round 3

Round 3 of the T0 cap 3. It closes the four required findings and the nit carried by
the two round-2 flagship re-audits:

- Codex `gpt-5.6-sol` xhigh, `TRANSPORT_CODEX_REAUDIT_R2_2026-08-10.md` —
  REQUEST_CHANGES, F1–F4 plus N1;
- Claude `claude-opus-5` xhigh, `TRANSPORT_CLAUDE_REAUDIT_R2_2026-08-10.md` —
  REQUEST_CHANGES, F1.

Both flagships independently found the same rc-classification defect; that convergence
made it the priority. All 16 round-1 findings stay closed and none is regressed — §7
records which round-2 arms were re-driven this round and which were not.

**Integrity.** No host was contacted. No SSH or SCP connection was opened, no host key
was offered, no credential was read, no RUNID was allocated, no archive was built,
nothing was frozen, and nothing was committed. `C:\WPI_ARTIFACTS` contains **no**
`WPI_TRANSPORT_*` entry (checked after every fixture). The only sockets attempted were
loopback with port 9 closed. The real pinned `ssh.exe` and `scp.exe` were executed
locally — `ssh -G` evaluates configuration and exits, `scp` copied one local file to
another local file — and neither opens a connection; the only hostname passed to `ssh`
was the non-resolving literal `qa-target`, and it was never resolved because `-G`
returns before name resolution. All fixture scratch was removed; the last line of each
transcript proves it.

**Environment.** Windows PowerShell **5.1.26100.8875**; WSL2 running as uid 0 with
**uutils** coreutils and bash 5.3.9; Git Bash 5.2.37;
`OpenSSH_for_Windows_9.5p2, LibreSSL 3.8.2`.

---

## 0. How to re-execute every claim in this document

Four standalone fixture scripts. Each takes no argument, declares no shell state,
creates its own scratch, prints the exact command it is about to run, and removes its
scratch at the end. Their bodies are reproduced **verbatim** in §2–§5 below, and the
transcripts that follow each body are the real output of running exactly that body.

To re-execute: write each body below to the path named in the command beside it — the
paths this round used, and the paths the transcripts therefore contain — with **LF line
endings**, then run it. Nothing else is needed; no fixture takes an argument, reads an
environment variable, or depends on state another fixture left behind. The scratch this
round created has been removed, which is why the paths do not currently exist.

| fixture | closes | run it with |
|---|---|---|
| `f3_attack.sh` | F3 | `wsl.exe -e bash /mnt/c/Users/Public/wpi_r3/f3_attack.sh` |
| `f4_mount.sh` | F4 | `wsl.exe -e bash /mnt/c/Users/Public/wpi_r3/f4_mount.sh` |
| `f1_runner_qa.ps1` | F1 | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\f1_runner_qa.ps1` |
| `f2_config_qa.ps1` | F2 | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\f2_config_qa.ps1` |

`f1_runner_qa.ps1` and `f4_mount.sh` read the **audited round-2 bytes** for their RED
arms. Those bytes are extracted once from commit `9ef4437d` — the exact identity both
round-2 re-audits rejected — with:

```
cd C:\LAB\Tradingview_LAB_CLEAN
mkdir -p /c/Users/Public/wpi_r3/r2
for f in remote_setup_wpi.sh remote_extract_verify_wpi.sh transport_runner.ps1; do
  git show 9ef4437d:MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/$f > "/c/Users/Public/wpi_r3/r2/$f"
done
```

which re-derives to the audited identities, printed by the fixtures themselves:

```
e91bae0827f16cbefe2091980c0a049583bd8ce4173f99e802b2d54a224c29a8  12340  remote_setup_wpi.sh
2f076ed9a928656fddf22969ea4bf70de895f2c84c73f13b4c64b8040e72aa9a  45066  transport_runner.ps1
```

The RED arms are therefore the audited bytes, not a reconstruction of them.

### Declared substitutions — there are six, and no others

Every one is asserted present before it is applied, so a missed anchor throws instead
of silently producing a false RED or a false GREEN.

1. **Stage-1 freeze fills.** `BASE_RUN`, `CONFIRM_TOKEN`, `PREREG_DIR`, `RUNKIT_DIR`,
   `ACCEPTED_DIR`, `RECORD_ROOT`, `PLAN_SHA256`, the pinned-kit digest, the three
   configuration-file paths and digests, and — on the shell side — `EXPECT_PREFIX`,
   `EXPECT_PARENT`, `EXPECT_UID`, `EXPECT_GID` and `EXPECT_PARENT_MOUNT`. These are
   the values Stage 1 fills; without them nothing can run at all, which is exactly
   what arm **L1** demonstrates.
2. **`ssh`/`scp` → `C:\Windows\System32\cmd.exe`** at its real digest, with the pinned
   option block replaced by `@('/d','/c')`, in the **J family only**. This drives each
   operation's native status and output deterministically with no host. It substitutes
   the *program*, not the classifier under test. The **K family** drives the real
   pinned OpenSSH with the real option block, so the substitution hides nothing about
   F2.
3. **Remote `TOOL_*` pins → regular root-owned 0755 copies.** This kernel ships
   `/usr/bin/{stat,sha256sum,mktemp,tr,readlink,find,sort,cmp,rm}` as symlinks into a
   multicall binary, which the derived scripts refuse **by design** (deviation D-3).
   Arm **G0** runs `remote_close_tree_wpi.sh` exactly as it ships and shows that
   refusal, so the retargeting hides nothing.
4. **`EXPECT_OWNER='gatea:gatea'` → `'root:root'`** in the F3 fixture, because the QA
   host runs as uid 0. Applied identically to the RED and the GREEN arm.
5. **`MOUNTINFO` → a fixture file**, in the N arms only, so the malformed and empty
   mount sources can be presented at all.
6. **A hostile `ssh_config` given an owner-only ACL** in the M arms. OpenSSH refuses a
   group/other-writable configuration file outright, and that refusal would mask the
   channel under test. The fixture restores inheritance before removing the tree.

---

## 1. Finding → closing arm

| finding | severity | closing arm | RED | GREEN |
|---|---|---|---|---|
| **F1** — an rc outside `{0,1,3}`, and any native transport or cleanup failure, must be not-evaluable → `TR_RUN STOP` exit 3 | CRITICAL, both flagships | `f1_runner_qa.ps1` J1–J6, K1–K2 | round-2 bytes at `2f076ed9…` | round-3 bytes |
| **F2** — the constructed environment cannot run the real pinned OpenSSH | CRITICAL | `f2_config_qa.ps1` M1–M7, K3, L2, L3; `f1_runner_qa.ps1` K1–K2 | M1/K1: real `ssh.exe`, rc 255, 0 bytes | M6/K2/K3 |
| **F3** — the accepted close program chain is PATH-selected and can mutate closed evidence while reporting PASS | CRITICAL | `f3_attack.sh` RED/G0/GREEN/CTL | accepted 7470 B / `87157f0e…` | `remote_close_tree_wpi.sh` |
| **F4** — setup does not bind the accepted mount object before mutation | HIGH | `f4_mount.sh` RED/GREEN/CTL/PIN/N1–N5 | round-2 bytes at `e91bae08…` | round-3 bytes |
| **N1** — placeholder census inaccurate | nit | §9 | — | re-derived |

---

## 2. Fixture A — the close program chain (F3)

Codex's round-2 F3 falsification, rebuilt and executed: a `sha256sum` planted first on
the inherited `PATH` appends one line to a closed evidence leaf on its first
invocation and then delegates to the real tool, so **both** digest passes observe the
post-mutation bytes and agree.

### A.1 `f3_attack.sh` (verbatim)

```bash
#!/usr/bin/env bash
# F3 falsification: a PATH-first `sha256sum` that mutates a closed evidence leaf
# once and then delegates to the real tool.
#   RED   = the ACCEPTED bytes (02_PREREG/remote_close_tree.sh, 7470 B).
#   GREEN = the DERIVED bytes (WPI_BLOCKS_DRAFT/remote_close_tree_wpi.sh).
# No host is contacted. Everything happens under /tmp/wpi_r3_f3.
set -u

REPO=/mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE
ACCEPTED="$REPO/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/remote_close_tree.sh"
DERIVED="$REPO/WPI_BLOCKS_DRAFT/remote_close_tree_wpi.sh"

QA=/tmp/wpi_r3_f3
rm -rf "$QA"; mkdir -p "$QA"

echo "=== source identities (byte-verified before anything runs) ==="
sha256sum "$ACCEPTED" "$DERIVED"
stat -c '%s %n' "$ACCEPTED" "$DERIVED"

# ---------------------------------------------------------------- declared
# SUBSTITUTION 1 of 2: this host runs as uid 0, so a tree it creates renders
# root:root. Both scripts compare the rendered name against 'gatea:gatea'. The
# same one-line substitution is applied to BOTH arms, and each is asserted
# present before it is replaced so a missed anchor throws instead of silently
# producing a false result.
subst_owner() {
    local src="$1" dst="$2"
    grep -q "^EXPECT_OWNER='gatea:gatea'\$" "$src" || { echo "ANCHOR_NOT_FOUND EXPECT_OWNER in $src"; exit 90; }
    sed "s|^EXPECT_OWNER='gatea:gatea'\$|EXPECT_OWNER='root:root'|" "$src" > "$dst"
    grep -q "^EXPECT_OWNER='root:root'\$" "$dst" || { echo "SUBST_FAILED $dst"; exit 91; }
}

# SUBSTITUTION 2 of 2 (GREEN arm only): this kernel ships /usr/bin/{stat,tr,...}
# as symlinks into a multicall binary, which the derived script refuses BY
# DESIGN (deviation D-3). The pins are retargeted at regular root-owned 0755
# copies so the attack arm exercises the pin mechanism rather than stopping at
# the symlink refusal. Arm G0 below runs the file exactly as it ships and shows
# that refusal, so the substitution hides nothing.
PINBIN="$QA/pinbin"
mkdir -p "$PINBIN"
for t in stat sha256sum mktemp tr readlink find sort cmp rm; do
    cp -L "/usr/bin/$t" "$PINBIN/$t"
    chown 0:0 "$PINBIN/$t"; chmod 0755 "$PINBIN/$t"
done
echo
echo "=== pinned tool copies (regular, root-owned, 0755) ==="
stat -c '%A %u:%g %n' "$PINBIN"/* | head -3
echo "..."

subst_pins() {
    local src="$1" dst="$2" t
    cp "$src" "$dst"
    for t in STAT SHA256SUM MKTEMP TR READLINK FIND SORT CMP RM; do
        local low; low="$(echo "$t" | tr 'A-Z' 'a-z')"
        grep -q "^TOOL_$t='/usr/bin/$low'\$" "$dst" || { echo "ANCHOR_NOT_FOUND TOOL_$t in $dst"; exit 92; }
        sed -i "s|^TOOL_$t='/usr/bin/$low'\$|TOOL_$t='$PINBIN/$low'|" "$dst"
    done
    grep -q "TOOL_STAT='$PINBIN/stat'" "$dst" || { echo "SUBST_FAILED pins $dst"; exit 93; }
}

# ------------------------------------------------------------- the attack
# A PATH-first sha256sum that appends one byte to the evidence leaf on its FIRST
# invocation and then delegates to the real tool, so both digest passes observe
# the post-mutation bytes and agree.
FAKEBIN="$QA/fakebin"
mkdir -p "$FAKEBIN"
cat > "$FAKEBIN/sha256sum" <<'ATTACK'
#!/bin/bash
echo called >> /tmp/wpi_r3_f3/attack_called
if [ ! -e /tmp/wpi_r3_f3/attack_fired ]; then
    : > /tmp/wpi_r3_f3/attack_fired
    printf 'MUTATED_BY_PATH_PLANT\n' >> /tmp/wpi_r3_f3/ev/RUNX/a.txt
fi
exec /usr/bin/sha256sum "$@"
ATTACK
chmod 0755 "$FAKEBIN/sha256sum"

new_tree() {
    rm -rf "$QA/ev" "$QA/attack_fired" "$QA/attack_called"
    mkdir -p "$QA/ev/RUNX"
    chmod 700 "$QA/ev/RUNX"
    printf 'alpha\n' > "$QA/ev/RUNX/a.txt"
    printf 'beta\n'  > "$QA/ev/RUNX/b.txt"
}

run_arm() {
    local label="$1" script="$2" usepath="$3"
    new_tree
    local pre post
    pre="$(sha256sum "$QA/ev/RUNX/a.txt" | cut -d' ' -f1)"
    echo
    echo "=== $label ==="
    echo "COMMAND: env -i PATH=$usepath HOME=/root bash $script $QA/ev/RUNX RUNX"
    local out rc=0
    out="$(env -i PATH="$usepath" HOME=/root bash "$script" "$QA/ev/RUNX" RUNX 2>"$QA/err.txt")" || rc=$?
    post="$(sha256sum "$QA/ev/RUNX/a.txt" | cut -d' ' -f1)"
    echo "RC=$rc"
    echo "PRE_SHA=$pre"
    echo "POST_SHA=$post"
    if [ "$pre" = "$post" ]; then echo "MUTATED=no"; else echo "MUTATED=yes"; fi
    if [ -e "$QA/attack_called" ]; then
        echo "PATH_PLANT_CONSULTED=yes calls=$(wc -l < "$QA/attack_called")"
    else
        echo "PATH_PLANT_CONSULTED=no"
    fi
    echo "--- stdout (CLOSE_DIGEST/CLOSE PASS/CLOSE_STOP lines) ---"
    printf '%s\n' "$out" | grep -E '^(CLOSE_DIGEST |CLOSE PASS|CLOSE_BINDING|CLOSE_NOTE tool |CLOSE_NOTE tool_digest_limit)' | head -20
    echo "--- stderr ---"
    cat "$QA/err.txt"
    echo "STDERR_BYTES=$(stat -c '%s' "$QA/err.txt")"
}

HOSTILE_PATH="$FAKEBIN:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

subst_owner "$ACCEPTED" "$QA/accepted_ownersubst.sh"
subst_owner "$DERIVED"  "$QA/derived_ownersubst.sh"
subst_pins  "$QA/derived_ownersubst.sh" "$QA/derived_green.sh"

run_arm "RED  - ACCEPTED bytes, PATH-first sha256sum plant" "$QA/accepted_ownersubst.sh" "$HOSTILE_PATH"
run_arm "G0   - DERIVED bytes exactly as shipped (/usr/bin pins), same plant" "$QA/derived_ownersubst.sh" "$HOSTILE_PATH"
run_arm "GREEN- DERIVED bytes, pins retargeted at regular root-owned copies, same plant" "$QA/derived_green.sh" "$HOSTILE_PATH"
run_arm "CTL  - DERIVED bytes, retargeted pins, clean PATH (no plant)" "$QA/derived_green.sh" "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

echo
echo "=== cleanup ==="
rm -rf "$QA"
echo "removed $QA"
```

### A.2 transcript (verbatim)

```text
﻿=== source identities (byte-verified before anything runs) ===
87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e  /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/remote_close_tree.sh
fc183751c634c7fd6d1d9bd75143b7229357e52b7eec5f25a8eec0192bd1f75f  /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_close_tree_wpi.sh
7470 /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/remote_close_tree.sh
12039 /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_close_tree_wpi.sh

=== pinned tool copies (regular, root-owned, 0755) ===
-rwxr-xr-x 0:0 /tmp/wpi_r3_f3/pinbin/cmp
-rwxr-xr-x 0:0 /tmp/wpi_r3_f3/pinbin/find
-rwxr-xr-x 0:0 /tmp/wpi_r3_f3/pinbin/mktemp
...

=== RED  - ACCEPTED bytes, PATH-first sha256sum plant ===
COMMAND: env -i PATH=/tmp/wpi_r3_f3/fakebin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOME=/root bash /tmp/wpi_r3_f3/accepted_ownersubst.sh /tmp/wpi_r3_f3/ev/RUNX RUNX
RC=0
PRE_SHA=b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060
POST_SHA=a8201c99853ef0b09daf750483e8cc6a6f5cbe97946d2e4b1c71a1165666dd3f
MUTATED=yes
PATH_PLANT_CONSULTED=yes calls=5
--- stdout (CLOSE_DIGEST/CLOSE PASS/CLOSE_STOP lines) ---
CLOSE_BINDING runid=RUNX dir=/tmp/wpi_r3_f3/ev/RUNX files=2
CLOSE_DIGEST a8201c99853ef0b09daf750483e8cc6a6f5cbe97946d2e4b1c71a1165666dd3f  a.txt
CLOSE_DIGEST f2c82decdd7181cf98945929a62598db7e6b477e11f6e0eb0ae97020eff151ad  b.txt
CLOSE PASS runid=RUNX dir=/tmp/wpi_r3_f3/ev/RUNX files=2 wrote_into_evidence_tree=0
--- stderr ---
STDERR_BYTES=0

=== G0   - DERIVED bytes exactly as shipped (/usr/bin pins), same plant ===
COMMAND: env -i PATH=/tmp/wpi_r3_f3/fakebin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOME=/root bash /tmp/wpi_r3_f3/derived_ownersubst.sh /tmp/wpi_r3_f3/ev/RUNX RUNX
RC=3
PRE_SHA=b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060
POST_SHA=b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060
MUTATED=no
PATH_PLANT_CONSULTED=no
--- stdout (CLOSE_DIGEST/CLOSE PASS/CLOSE_STOP lines) ---
--- stderr ---
CLOSE_STOP reason=tool_is_symlink path=/usr/bin/stat
STDERR_BYTES=53

=== GREEN- DERIVED bytes, pins retargeted at regular root-owned copies, same plant ===
COMMAND: env -i PATH=/tmp/wpi_r3_f3/fakebin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOME=/root bash /tmp/wpi_r3_f3/derived_green.sh /tmp/wpi_r3_f3/ev/RUNX RUNX
RC=0
PRE_SHA=b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060
POST_SHA=b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060
MUTATED=no
PATH_PLANT_CONSULTED=no
--- stdout (CLOSE_DIGEST/CLOSE PASS/CLOSE_STOP lines) ---
CLOSE_NOTE tool name=stat path=/tmp/wpi_r3_f3/pinbin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=sha256sum path=/tmp/wpi_r3_f3/pinbin/sha256sum owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=mktemp path=/tmp/wpi_r3_f3/pinbin/mktemp owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=tr path=/tmp/wpi_r3_f3/pinbin/tr owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=readlink path=/tmp/wpi_r3_f3/pinbin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=find path=/tmp/wpi_r3_f3/pinbin/find owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=sort path=/tmp/wpi_r3_f3/pinbin/sort owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=cmp path=/tmp/wpi_r3_f3/pinbin/cmp owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=rm path=/tmp/wpi_r3_f3/pinbin/rm owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool_digest_limit no_frozen_remote_tool_digest_can_be_known_before_host_contact
CLOSE_BINDING runid=RUNX dir=/tmp/wpi_r3_f3/ev/RUNX files=2
CLOSE_DIGEST b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060  a.txt
CLOSE_DIGEST f2c82decdd7181cf98945929a62598db7e6b477e11f6e0eb0ae97020eff151ad  b.txt
CLOSE PASS runid=RUNX dir=/tmp/wpi_r3_f3/ev/RUNX files=2 wrote_into_evidence_tree=0
--- stderr ---
STDERR_BYTES=0

=== CTL  - DERIVED bytes, retargeted pins, clean PATH (no plant) ===
COMMAND: env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOME=/root bash /tmp/wpi_r3_f3/derived_green.sh /tmp/wpi_r3_f3/ev/RUNX RUNX
RC=0
PRE_SHA=b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060
POST_SHA=b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060
MUTATED=no
PATH_PLANT_CONSULTED=no
--- stdout (CLOSE_DIGEST/CLOSE PASS/CLOSE_STOP lines) ---
CLOSE_NOTE tool name=stat path=/tmp/wpi_r3_f3/pinbin/stat owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=sha256sum path=/tmp/wpi_r3_f3/pinbin/sha256sum owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=mktemp path=/tmp/wpi_r3_f3/pinbin/mktemp owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=tr path=/tmp/wpi_r3_f3/pinbin/tr owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=readlink path=/tmp/wpi_r3_f3/pinbin/readlink owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=find path=/tmp/wpi_r3_f3/pinbin/find owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=sort path=/tmp/wpi_r3_f3/pinbin/sort owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=cmp path=/tmp/wpi_r3_f3/pinbin/cmp owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool name=rm path=/tmp/wpi_r3_f3/pinbin/rm owner_numeric=0:0 mode=755 resolution=pinned_absolute
CLOSE_NOTE tool_digest_limit no_frozen_remote_tool_digest_can_be_known_before_host_contact
CLOSE_BINDING runid=RUNX dir=/tmp/wpi_r3_f3/ev/RUNX files=2
CLOSE_DIGEST b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060  a.txt
CLOSE_DIGEST f2c82decdd7181cf98945929a62598db7e6b477e11f6e0eb0ae97020eff151ad  b.txt
CLOSE PASS runid=RUNX dir=/tmp/wpi_r3_f3/ev/RUNX files=2 wrote_into_evidence_tree=0
--- stderr ---
STDERR_BYTES=0

=== cleanup ===
removed /tmp/wpi_r3_f3
```

### A.3 what it establishes

- **RED, the accepted bytes.** `PATH_PLANT_CONSULTED=yes calls=5`, `MUTATED=yes`,
  `RC=0`, and the emitted record is
  `CLOSE PASS runid=RUNX … files=2 wrote_into_evidence_tree=0` with
  `CLOSE_DIGEST a8201c99…  a.txt` — the **post-mutation** digest. The accepted
  script's own closing sentence is false under the delivered execution environment,
  and the operator-side binder would have bound those post-mutation bytes without any
  discrepancy, because remote and local both describe the mutated file.
- **G0, the derived bytes exactly as they ship.** `CLOSE_STOP reason=tool_is_symlink
  path=/usr/bin/stat`, rc 3, nothing mutated, plant never consulted. Deviation D-3 is
  real on this kernel and the direction is safe.
- **GREEN, the derived bytes with the pins retargeted.** `PATH_PLANT_CONSULTED=no`,
  `MUTATED=no`, rc 0, and `CLOSE_DIGEST b6a98d9c…  a.txt` — the true pre-value. Nine
  `CLOSE_NOTE tool …  resolution=pinned_absolute` lines and the explicit
  `CLOSE_NOTE tool_digest_limit …` line precede the record.
- **CTL** reproduces GREEN with no plant on `PATH` at all, so the GREEN result is not
  an artefact of the plant being present but inert.

---

## 3. Fixture B — the allocation parent's mount object (F4)

Codex's round-2 F4 scenario, executed: a bind mount at the same literal canonical path
presenting the same numeric owner and the same mode. `readlink -f` answers with the
expected path and every component predicate passes.

### B.1 `f4_mount.sh` (verbatim)

```bash
#!/usr/bin/env bash
# F4 falsification: a bind mount at the same literal canonical path, presenting
# the expected owner and mode, receives the four allocations.
#   RED   = the audited round-2 bytes (9ef4437d, remote_setup_wpi.sh,
#           12340 B / e91bae08...), which carry no mount predicate at all.
#   GREEN = the round-3 bytes in the working tree.
# No host is contacted. Everything happens under /wpi_r3_f4.
set -u

DRAFT=/mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT
R2=/mnt/c/Users/Public/wpi_r3/r2/remote_setup_wpi.sh
R3="$DRAFT/remote_setup_wpi.sh"

QA=/wpi_r3_f4
umount "$QA/home/gatea" 2>/dev/null || true
rm -rf "$QA"; mkdir -p "$QA"; chown 0:0 "$QA"; chmod 0755 "$QA"

echo "=== source identities ==="
sha256sum "$R2" "$R3"
wc -c "$R2" "$R3"
echo "EUID=$EUID"

PINBIN="$QA/pinbin"; mkdir -p "$PINBIN"
for t in stat mkdir readlink; do
    cp -L "/usr/bin/$t" "$PINBIN/$t"; chown 0:0 "$PINBIN/$t"; chmod 0755 "$PINBIN/$t"
done

PARENT="$QA/home/gatea"
PREFIX="$PARENT/wpi_staging_"

# ------------------------------------------------------------------ substitutions
# Each anchor is asserted present before it is replaced, so a missed anchor
# throws instead of silently producing a false RED or GREEN.
subst() {   # subst <src> <dst> <mountpin-or-KEEP>
    local src="$1" dst="$2" mountpin="$3" a b
    cp "$src" "$dst"
    while IFS='|' read -r a b; do
        [ -n "$a" ] || continue
        grep -qF -- "$a" "$dst" || { echo "ANCHOR_NOT_FOUND [$a] in $dst"; exit 90; }
        python3 - "$dst" "$a" "$b" <<'PY'
import sys
p,a,b=sys.argv[1],sys.argv[2],sys.argv[3]
d=open(p,encoding='utf-8').read()
assert a in d
open(p,'w',encoding='utf-8').write(d.replace(a,b))
PY
    done <<EOF
EXPECT_PREFIX='/home/gatea/wpi_staging_'|EXPECT_PREFIX='$PREFIX'
EXPECT_PARENT='/home/gatea'|EXPECT_PARENT='$PARENT'
EXPECT_UID='<PIN-AT-FREEZE>'|EXPECT_UID='0'
EXPECT_GID='<PIN-AT-FREEZE>'|EXPECT_GID='0'
TOOL_STAT='/usr/bin/stat'|TOOL_STAT='$PINBIN/stat'
TOOL_MKDIR='/usr/bin/mkdir'|TOOL_MKDIR='$PINBIN/mkdir'
TOOL_READLINK='/usr/bin/readlink'|TOOL_READLINK='$PINBIN/readlink'
EOF
    if [ "$mountpin" != 'KEEP' ]; then
        grep -qF "EXPECT_PARENT_MOUNT='<PIN-AT-FREEZE>'" "$dst" || { echo "ANCHOR_NOT_FOUND mountpin in $dst"; exit 91; }
        python3 - "$dst" "$mountpin" <<'PY'
import sys
p,v=sys.argv[1],sys.argv[2]
a="EXPECT_PARENT_MOUNT='<PIN-AT-FREEZE>'"
d=open(p,encoding='utf-8').read(); assert a in d
open(p,'w',encoding='utf-8').write(d.replace(a,"EXPECT_PARENT_MOUNT='%s'" % v))
PY
    fi
}

fresh_parent() {
    umount "$PARENT" 2>/dev/null || true
    rm -rf "$QA/home" "$QA/decoy"
    mkdir -p "$PARENT"; chown 0:0 "$QA/home" "$PARENT"; chmod 0755 "$QA/home"; chmod 0755 "$PARENT"
    # The decoy presents the SAME owner and the SAME mode as the accepted object.
    mkdir -p "$QA/decoy"; chown 0:0 "$QA/decoy"; chmod 0755 "$QA/decoy"
}

count_dirs() { find "$1" -mindepth 1 -type d 2>/dev/null | wc -l; }

# The attested projection of the ACCEPTED object, taken while nothing is
# substituted. This is what the deploy channel would attest before op 01.
fresh_parent
ATTESTED="$(awk -v p="$PARENT" '
  { dev=$3; root=$4; mp=$5; sep=0;
    for(i=7;i<=NF;i++) if($i=="-"){sep=i;break}
    fstype=$(sep+1); src=$(sep+2);
    covers=0;
    if(mp=="/") covers=1; else if(mp==p) covers=1; else if(index(p, mp "/")==1) covers=1;
    if(covers){ l=length(mp);
      if(l>best){best=l;bmp=mp;shared=1;out="device=" dev " root=" root " mount_point=" mp " fstype=" fstype " source=" src}
      else if(l==best && mp==bmp){shared++;out="device=" dev " root=" root " mount_point=" mp " fstype=" fstype " source=" src} } }
  END{ print out " shared_mount_point_records=" shared }' /proc/self/mountinfo)"
echo
echo "ATTESTED_PROJECTION=[$ATTESTED]"

subst "$R2" "$QA/r2_setup.sh" KEEP
subst "$R3" "$QA/r3_setup_attested.sh" "$ATTESTED"
subst "$R3" "$QA/r3_setup_unfilled.sh" KEEP

run_arm() {   # run_arm <label> <script> <bindmount yes/no>
    local label="$1" script="$2" bind="$3" rc=0 out
    fresh_parent
    if [ "$bind" = yes ]; then
        mount --bind "$QA/decoy" "$PARENT" || { echo "BIND_MOUNT_UNAVAILABLE"; return; }
    fi
    echo
    echo "=== $label ==="
    echo "COMMAND: bash $script $PREFIX QA1"
    echo "PARENT_METADATA: $(stat -c 'owner=%u:%g mode=%a canonical=%n' "$PARENT")  readlink -f => $(readlink -f "$PARENT")"
    out="$(bash "$script" "${PREFIX}QA1" 2>"$QA/err.txt")" || rc=$?
    echo "RC=$rc"
    echo "DIRS_CREATED_IN_VISIBLE_PARENT=$(count_dirs "$PARENT")"
    if [ "$bind" = yes ]; then
        umount "$PARENT" 2>/dev/null || true
        echo "DIRS_CREATED_IN_DECOY=$(count_dirs "$QA/decoy")"
        echo "DIRS_CREATED_IN_ACCEPTED_OBJECT=$(count_dirs "$PARENT")"
    fi
    echo "--- stdout tail ---"
    printf '%s\n' "$out" | grep -E '^(SETUP PASS|SETUP_NOTE parent_mount|SETUP_NOTE allocated|SETUP_NOTE base_absent)' | head -12
    echo "--- stderr ---"
    cat "$QA/err.txt"
}

run_arm "RED   round-2 bytes, decoy bind-mounted over the accepted parent" "$QA/r2_setup.sh" yes
run_arm "GREEN round-3 bytes, same decoy bind mount, attested pin" "$QA/r3_setup_attested.sh" yes
run_arm "CTL   round-3 bytes, no substitution of the mount, attested pin" "$QA/r3_setup_attested.sh" no
run_arm "PIN   round-3 bytes exactly as shipped (pin still unfilled)" "$QA/r3_setup_unfilled.sh" no

# ---------------------------------------------------- the mountinfo reader arms
# Pattern 7: a reader has three exit conditions, not one. MOUNTINFO is retargeted
# at a fixture file (declared substitution, anchor asserted) so the malformed and
# empty sources can actually be presented.
mi_arm() {   # mi_arm <label> <fixture-content-writer> <expect-note>
    local label="$1" writer="$2"
    local script="$QA/r3_setup_mi.sh" fixture="$QA/mi.txt"
    fresh_parent
    "$writer" "$fixture"
    subst "$R3" "$script" "$ATTESTED"
    grep -qF "MOUNTINFO='/proc/self/mountinfo'" "$script" || { echo "ANCHOR_NOT_FOUND MOUNTINFO"; exit 94; }
    sed -i "s|^MOUNTINFO='/proc/self/mountinfo'\$|MOUNTINFO='$fixture'|" "$script"
    echo
    echo "=== $label ==="
    echo "FIXTURE: $(wc -c < "$fixture") bytes, $(wc -l < "$fixture") complete records"
    local rc=0
    bash "$script" "${PREFIX}QA1" >/dev/null 2>"$QA/err.txt" || rc=$?
    echo "RC=$rc"
    echo "DIRS_CREATED=$(count_dirs "$PARENT")"
    cat "$QA/err.txt"
}
w_empty()   { : > "$1"; }
w_short()   { printf '36 35 8:48 / /\n' > "$1"; }
w_nosep()   { printf '36 35 8:48 / / rw,relatime shared:1 ext4 /dev/sdd rw\n' > "$1"; }
w_nofinal() { { printf '36 35 8:48 / /wpi_r3_f4/nowhere rw,relatime - ext4 /dev/x rw\n'
                printf '36 35 8:48 / / rw,relatime - ext4 /dev/sdd rw'; } > "$1"; }
w_nocover() { printf '36 35 8:48 / /somewhere/else rw,relatime - ext4 /dev/sdd rw\n' > "$1"; }

mi_arm "N1 mountinfo source yields no record at all" w_empty
mi_arm "N2 mountinfo record too short to carry a projection" w_short
mi_arm "N3 mountinfo record with no optional-field separator" w_nosep
mi_arm "N4 populated final record carrying NO trailing newline (must still be read)" w_nofinal
mi_arm "N5 no record covers the allocation parent" w_nocover

echo
echo "=== cleanup ==="
umount "$PARENT" 2>/dev/null || true
rm -rf "$QA"
echo "removed $QA"; ls -d "$QA" 2>&1 | head -1
```

### B.2 transcript (verbatim)

```text
﻿=== source identities ===
e91bae0827f16cbefe2091980c0a049583bd8ce4173f99e802b2d54a224c29a8  /mnt/c/Users/Public/wpi_r3/r2/remote_setup_wpi.sh
c0b7caa7f856db6b6d8aad4d407d42d450064a9e55a9cbbacf464f28e97b8d74  /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_setup_wpi.sh
12340 /mnt/c/Users/Public/wpi_r3/r2/remote_setup_wpi.sh
17775 /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_setup_wpi.sh
30115 total
EUID=0

ATTESTED_PROJECTION=[device=8:48 root=/ mount_point=/ fstype=ext4 source=/dev/sdd shared_mount_point_records=1]

=== RED   round-2 bytes, decoy bind-mounted over the accepted parent ===
COMMAND: bash /wpi_r3_f4/r2_setup.sh /wpi_r3_f4/home/gatea/wpi_staging_ QA1
PARENT_METADATA: owner=0:0 mode=755 canonical=/wpi_r3_f4/home/gatea  readlink -f => /wpi_r3_f4/home/gatea
RC=0
DIRS_CREATED_IN_VISIBLE_PARENT=4
DIRS_CREATED_IN_DECOY=4
DIRS_CREATED_IN_ACCEPTED_OBJECT=0
--- stdout tail ---
SETUP_NOTE base_absent path=/wpi_r3_f4/home/gatea/wpi_staging_QA1
SETUP_NOTE allocated path=/wpi_r3_f4/home/gatea/wpi_staging_QA1
SETUP_NOTE allocated path=/wpi_r3_f4/home/gatea/wpi_staging_QA1/evidence
SETUP_NOTE allocated path=/wpi_r3_f4/home/gatea/wpi_staging_QA1/evidence/runkit
SETUP_NOTE allocated path=/wpi_r3_f4/home/gatea/wpi_staging_QA1/kit
SETUP PASS base=/wpi_r3_f4/home/gatea/wpi_staging_QA1 evidence=/wpi_r3_f4/home/gatea/wpi_staging_QA1/evidence runkit=/wpi_r3_f4/home/gatea/wpi_staging_QA1/evidence/runkit kit=/wpi_r3_f4/home/gatea/wpi_staging_QA1/kit owner_numeric=0:0 owner_name=gatea:gatea mode=700
--- stderr ---

=== GREEN round-3 bytes, same decoy bind mount, attested pin ===
COMMAND: bash /wpi_r3_f4/r3_setup_attested.sh /wpi_r3_f4/home/gatea/wpi_staging_ QA1
PARENT_METADATA: owner=0:0 mode=755 canonical=/wpi_r3_f4/home/gatea  readlink -f => /wpi_r3_f4/home/gatea
RC=3
DIRS_CREATED_IN_VISIBLE_PARENT=0
DIRS_CREATED_IN_DECOY=0
DIRS_CREATED_IN_ACCEPTED_OBJECT=0
--- stdout tail ---
SETUP_NOTE parent_mount_observed path=/wpi_r3_f4/home/gatea device=8:48 root=/wpi_r3_f4/decoy mount_point=/wpi_r3_f4/home/gatea fstype=ext4 source=/dev/sdd shared_mount_point_records=1
--- stderr ---
SETUP_STOP reason=parent_mount_differs path=/wpi_r3_f4/home/gatea observed=[device=8:48 root=/wpi_r3_f4/decoy mount_point=/wpi_r3_f4/home/gatea fstype=ext4 source=/dev/sdd shared_mount_point_records=1] attested=[device=8:48 root=/ mount_point=/ fstype=ext4 source=/dev/sdd shared_mount_point_records=1]

=== CTL   round-3 bytes, no substitution of the mount, attested pin ===
COMMAND: bash /wpi_r3_f4/r3_setup_attested.sh /wpi_r3_f4/home/gatea/wpi_staging_ QA1
PARENT_METADATA: owner=0:0 mode=755 canonical=/wpi_r3_f4/home/gatea  readlink -f => /wpi_r3_f4/home/gatea
RC=0
DIRS_CREATED_IN_VISIBLE_PARENT=4
--- stdout tail ---
SETUP_NOTE parent_mount_observed path=/wpi_r3_f4/home/gatea device=8:48 root=/ mount_point=/ fstype=ext4 source=/dev/sdd shared_mount_point_records=1
SETUP_NOTE parent_mount_bound path=/wpi_r3_f4/home/gatea attestation=deploy_channel_before_op_01
SETUP_NOTE base_absent path=/wpi_r3_f4/home/gatea/wpi_staging_QA1
SETUP_NOTE allocated path=/wpi_r3_f4/home/gatea/wpi_staging_QA1
SETUP_NOTE allocated path=/wpi_r3_f4/home/gatea/wpi_staging_QA1/evidence
SETUP_NOTE allocated path=/wpi_r3_f4/home/gatea/wpi_staging_QA1/evidence/runkit
SETUP_NOTE allocated path=/wpi_r3_f4/home/gatea/wpi_staging_QA1/kit
SETUP PASS base=/wpi_r3_f4/home/gatea/wpi_staging_QA1 evidence=/wpi_r3_f4/home/gatea/wpi_staging_QA1/evidence runkit=/wpi_r3_f4/home/gatea/wpi_staging_QA1/evidence/runkit kit=/wpi_r3_f4/home/gatea/wpi_staging_QA1/kit owner_numeric=0:0 owner_name=gatea:gatea mode=700
--- stderr ---

=== PIN   round-3 bytes exactly as shipped (pin still unfilled) ===
COMMAND: bash /wpi_r3_f4/r3_setup_unfilled.sh /wpi_r3_f4/home/gatea/wpi_staging_ QA1
PARENT_METADATA: owner=0:0 mode=755 canonical=/wpi_r3_f4/home/gatea  readlink -f => /wpi_r3_f4/home/gatea
RC=3
DIRS_CREATED_IN_VISIBLE_PARENT=0
--- stdout tail ---
--- stderr ---
SETUP_STOP reason=mount_pin_unfilled field=EXPECT_PARENT_MOUNT

=== N1 mountinfo source yields no record at all ===
FIXTURE: 0 bytes, 0 complete records
RC=3
DIRS_CREATED=0
SETUP_STOP reason=mountinfo_no_records path=/wpi_r3_f4/mi.txt

=== N2 mountinfo record too short to carry a projection ===
FIXTURE: 15 bytes, 1 complete records
RC=3
DIRS_CREATED=0
SETUP_STOP reason=mountinfo_record_short fields=5 record=[36 35 8:48 / /]

=== N3 mountinfo record with no optional-field separator ===
FIXTURE: 53 bytes, 1 complete records
RC=3
DIRS_CREATED=0
SETUP_STOP reason=mountinfo_record_no_separator record=[36 35 8:48 / / rw,relatime shared:1 ext4 /dev/sdd rw]

=== N4 populated final record carrying NO trailing newline (must still be read) ===
FIXTURE: 106 bytes, 1 complete records
RC=0
DIRS_CREATED=4

=== N5 no record covers the allocation parent ===
FIXTURE: 60 bytes, 1 complete records
RC=3
DIRS_CREATED=0
SETUP_STOP reason=mountinfo_no_covering_mount path=/wpi_r3_f4/home/gatea records=1

=== cleanup ===
removed /wpi_r3_f4
ls: cannot access '/wpi_r3_f4': No such file or directory
```

### B.3 what it establishes

- **RED, the audited round-2 bytes.** `PARENT_METADATA: owner=0:0 mode=755` and
  `readlink -f => /wpi_r3_f4/home/gatea` — indistinguishable from the accepted object
  — then `SETUP PASS`, rc 0, `DIRS_CREATED_IN_DECOY=4`,
  `DIRS_CREATED_IN_ACCEPTED_OBJECT=0`. All four allocations landed in the substituted
  object. This is the non-symlink half of "the leaf is not the path", executed.
- **GREEN, the round-3 bytes.** `SETUP_STOP reason=parent_mount_differs`, rc 3, zero
  directories anywhere. The observed projection differs from the attested one in
  exactly the field a metadata check cannot see: `root=/wpi_r3_f4/decoy` against
  `root=/`.
- **CTL** allocates normally when nothing is substituted, so the predicate is not
  simply refusing everything: `parent_mount_bound … attestation=deploy_channel_before_op_01`,
  rc 0, four directories.
- **PIN**, the file exactly as it ships: `SETUP_STOP reason=mount_pin_unfilled
  field=EXPECT_PARENT_MOUNT`, rc 3, zero directories. The attestation is a missing
  input, refused at rc 3 before any path is probed.
- **N1–N5, the reader's exit conditions.** No record at all → `mountinfo_no_records`;
  a record too short to project → `mountinfo_record_short fields=5`; a record with no
  optional-field separator → `mountinfo_record_no_separator`; **a populated final
  record carrying no trailing newline → rc 0 and four directories**, i.e. the record
  was consumed rather than dropped, which a reader handling only clean EOF would have
  discarded into a false `mountinfo_no_covering_mount`; and a mount table where
  nothing covers the parent → `mountinfo_no_covering_mount`, rc 3. Every failing arm
  creates zero directories.

---

## 4. Fixture C — outcome classification through the runner (F1)

Whole-plan arms over the real 12-row plan shape, driven through the runner's own
`Invoke-ExternalProcess`, plus two arms driving the **real** pinned `ssh.exe`.

### C.1 `f1_runner_qa.ps1` (verbatim)

```powershell
# WP-I transport round 3 - transport_runner.ps1 RED/GREEN fixture set.
#   GREEN = the current repaired file in the working tree.
#   RED   = the audited round-2 bytes, read from commit 9ef4437d
#           (45066 B / 2f076ed9...), i.e. the exact identity both round-2
#           re-audits rejected. The RED arms are the audited bytes, not a
#           reconstruction.
# It contacts no host. The only sockets attempted are loopback with a closed
# port. It allocates no RUNID, touches no repository file, and removes its
# scratch root at the end.
Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

$DRAFT = 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT'
$R3SRC = Join-Path $DRAFT 'transport_runner.ps1'
$R2SRC = 'C:\Users\Public\wpi_r3\r2\transport_runner.ps1'
$QA    = 'C:\Users\Public\wpi_r3\qa'

function Sha([string] $p) { return (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() }
function WriteLf([string] $p, [string] $t) {
    [System.IO.File]::WriteAllText($p, ($t -replace "`r`n", "`n"), (New-Object System.Text.UTF8Encoding($false)))
}

Write-Host '=== source identities ==='
Write-Host ('R3 ' + (Sha $R3SRC) + ' ' + (Get-Item $R3SRC).Length + ' ' + $R3SRC)
Write-Host ('R2 ' + (Sha $R2SRC) + ' ' + (Get-Item $R2SRC).Length + ' ' + $R2SRC)
Write-Host ('CMD ' + (Sha 'C:\Windows\System32\cmd.exe'))
Write-Host ('SSH ' + (Sha 'C:\Windows\System32\OpenSSH\ssh.exe'))

if (Test-Path -LiteralPath $QA) { Remove-Item -LiteralPath $QA -Recurse -Force }
foreach ($d in @('prereg','kit','accepted','arms','cfg','rec')) { [void](New-Item -ItemType Directory -Path (Join-Path $QA $d) -Force) }
$PREREG = Join-Path $QA 'prereg'; $KIT = Join-Path $QA 'kit'; $ACC = Join-Path $QA 'accepted'
$ARMS = Join-Path $QA 'arms'; $CFG = Join-Path $QA 'cfg'; $REC = Join-Path $QA 'rec\WPI_TRANSPORT_WPIQA'

# fixture stdin payloads (small, so the pipe write completes before the child exits)
foreach ($n in @('setup.sh','extract.sh','p0.sh','ro.sh','close.sh')) { WriteLf (Join-Path $PREREG $n) ('# fixture ' + $n) }
WriteLf (Join-Path $KIT 'runkit.tar') 'fixture-kit'
WriteLf (Join-Path $CFG 'identity') 'fixture-identity'
WriteLf (Join-Path $CFG 'known_hosts') 'fixture-known-hosts'
WriteLf (Join-Path $CFG 'known_hosts_global') 'fixture-known-hosts-global'

# ---------------------------------------------------------------- arm programs
# Each .cmd is the operation's scripted behaviour: what it prints and what it
# returns. Nothing else about the operation is faked.
function NewArm([string] $name, [string[]] $body) {
    $p = Join-Path $ARMS ($name + '.cmd')
    [System.IO.File]::WriteAllText($p, (($body -join "`r`n") + "`r`n"), (New-Object System.Text.ASCIIEncoding))
    return $p
}
[void](NewArm 'stop3'      @('@echo off','echo SETUP_STOP reason=fixture_setup_could_not_evaluate 1>&2','exit /b 3'))
[void](NewArm 'closefail1' @('@echo off','echo CLOSE_FAIL reason=evidence_dir_absent path=fixture 1>&2','exit /b 1'))
[void](NewArm 'scpfail1'   @('@echo off','echo scp: fixture transfer failed 1>&2','exit /b 1'))
[void](NewArm 'rc255'      @('@echo off','exit /b 255'))
[void](NewArm 'rc2'        @('@echo off','echo bash: fixture: command not found 1>&2','exit /b 2'))
[void](NewArm 'rc0silent'  @('@echo off','exit /b 0'))
[void](NewArm 'rc0marked'  @('@echo off','echo SETUP PASS base=fixture','exit /b 0'))
[void](NewArm 'rc1marked'  @('@echo off','echo EXTRACT_FAIL reason=archive_sha256_mismatch 1>&2','exit /b 1'))
[void](NewArm 'scpok'      @('@echo off','exit /b 0'))

# ------------------------------------------------------------------ QA freeze
# One block, inserted immediately after $UNFILLED_MARKERS - the last constant in
# BOTH runner versions - so every frozen constant is filled exactly as Stage 1
# would fill it. The anchor is asserted present before the insertion, so a
# missed anchor throws instead of producing a false arm.
$ANCHOR = "`$UNFILLED_MARKERS = @('<ALLOCATE-AT-DISPATCH>', '<PIN-AT-FREEZE>')"

function New-RunnerCopy([string] $src, [string] $dst, [string] $planSha, [string] $programBlock, [string] $optionBlock) {
    $text = [System.IO.File]::ReadAllText($src)
    if (-not $text.Contains($ANCHOR)) { throw ('MUTATION_ANCHOR_NOT_FOUND: $UNFILLED_MARKERS in ' + $src) }
    $qa = @"
$ANCHOR
# ---- QA freeze block (fixture only) ----
`$BASE_RUN      = 'WPIQA'
`$CONFIRM_TOKEN = 'WPIQA-EXECUTE'
`$PREREG_DIR    = '$PREREG'
`$RUNKIT_DIR    = '$KIT'
`$ACCEPTED_DIR  = '$ACC'
`$RECORD_ROOT   = '$REC'
`$PLAN_SHA256   = '$planSha'
`$PINNED_FILES  = @( @{ Path = (Join-Path `$RUNKIT_DIR 'runkit.tar'); Sha = '$(Sha (Join-Path $KIT 'runkit.tar'))' } )
`$STDIN_ROOTS   = @{ 'PREREG' = `$PREREG_DIR; 'ACCEPTED' = `$ACCEPTED_DIR }
$programBlock
`$SSH_IDENTITY_FILE          = '$CFG\identity'
`$SSH_IDENTITY_SHA           = '$(Sha (Join-Path $CFG 'identity'))'
`$SSH_USER_KNOWN_HOSTS       = '$CFG\known_hosts'
`$SSH_USER_KNOWN_HOSTS_SHA   = '$(Sha (Join-Path $CFG 'known_hosts'))'
`$SSH_GLOBAL_KNOWN_HOSTS     = '$CFG\known_hosts_global'
`$SSH_GLOBAL_KNOWN_HOSTS_SHA = '$(Sha (Join-Path $CFG 'known_hosts_global'))'
`$CONFIG_PINS = @(
    @{ Name = 'ssh_identity'; Path = `$SSH_IDENTITY_FILE; Sha = `$SSH_IDENTITY_SHA; Print = `$false; Why = 'fixture' },
    @{ Name = 'user_known_hosts'; Path = `$SSH_USER_KNOWN_HOSTS; Sha = `$SSH_USER_KNOWN_HOSTS_SHA; Print = `$true; Why = 'fixture' },
    @{ Name = 'global_known_hosts'; Path = `$SSH_GLOBAL_KNOWN_HOSTS; Sha = `$SSH_GLOBAL_KNOWN_HOSTS_SHA; Print = `$true; Why = 'fixture' }
)
$optionBlock
# ---- end QA freeze block ----
"@
    [System.IO.File]::WriteAllText($dst, $text.Replace($ANCHOR, $qa), (New-Object System.Text.UTF8Encoding($false)))
}

$CMDSHA = Sha 'C:\Windows\System32\cmd.exe'
$PROG_CMD = @"
`$PROGRAM_PINS  = @(
    @{ Name = 'ssh'; Path = 'C:\Windows\System32\cmd.exe'; Sha = '$CMDSHA' },
    @{ Name = 'scp'; Path = 'C:\Windows\System32\cmd.exe'; Sha = '$CMDSHA' }
)
"@
$PROG_SSH = @"
`$PROGRAM_PINS  = @(
    @{ Name = 'ssh'; Path = 'C:\Windows\System32\OpenSSH\ssh.exe'; Sha = '$(Sha 'C:\Windows\System32\OpenSSH\ssh.exe')' },
    @{ Name = 'scp'; Path = 'C:\Windows\System32\OpenSSH\scp.exe'; Sha = '$(Sha 'C:\Windows\System32\OpenSSH\scp.exe')' }
)
"@
$OPT_CMD = "`$SSH_PINNED_OPTIONS = @('/d','/c')"
$K_OPTIONS = @(
    '-F','none','-i',($CFG + '\identity'),
    '-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','IdentitiesOnly=yes','-o','ConnectTimeout=20',
    '-o',('UserKnownHostsFile=' + $CFG + '\known_hosts'),
    '-o',('GlobalKnownHostsFile=' + $CFG + '\known_hosts_global'),
    '-o','ProxyCommand=none','-o','ControlMaster=no','-o','ControlPath=none','-o','PermitLocalCommand=no',
    '-o','ForwardAgent=no','-o','ForwardX11=no','-o','ClearAllForwardings=yes'
)
$OPT_K = "`$SSH_PINNED_OPTIONS = @('" + ($K_OPTIONS -join "','") + "')"

# ------------------------------------------------------------------- plans
$HDR = "op_id`tkind`trun_when`texpect_rc`tcwd`tstdin_file`tstdin_sha256`targv`tpurpose"
function StdinSha([string] $leaf) { return (Sha (Join-Path $PREREG $leaf)) }
function Row([string] $id, [string] $kind, [string] $when, [int] $rc, [string] $cwd, [string] $stdin, [string] $argv, [string] $purpose) {
    $sha = '-'
    if ($stdin -ne '-') { $sha = StdinSha ($stdin.Split(':')[1]) }
    return ($id + "`t" + $kind + "`t" + $when + "`t" + $rc + "`t" + $cwd + "`t" + $stdin + "`t" + $sha + "`t" + $argv + "`t" + $purpose)
}
function A([string] $n) { return ('/d /c ' + (Join-Path $ARMS ($n + '.cmd'))) }

# The 12-row fixture plan mirrors the real plan's kinds, run_when and expect_rc.
function Plan12([hashtable] $behaviour) {
    $ev = Join-Path $REC 'evidence'
    $rows = @($HDR)
    $rows += Row '01' 'ssh_stdin' 'sequence_ok' 0 $PREREG 'PREREG:setup.sh'   ('ssh ' + (A $behaviour['01'])) 'allocate'
    $rows += Row '02' 'scp_up'    'sequence_ok' 0 $KIT    '-'                 ('scp ' + (A $behaviour['02'])) 'upload'
    $rows += Row '03' 'ssh_stdin' 'sequence_ok' 0 $PREREG 'PREREG:extract.sh' ('ssh ' + (A $behaviour['03'])) 'extract'
    $rows += Row '04' 'ssh_stdin' 'sequence_ok' 0 $PREREG 'PREREG:p0.sh'      ('ssh ' + (A $behaviour['04'])) 'p0'
    $rows += Row '05' 'ssh_stdin' 'sequence_ok' 0 $PREREG 'PREREG:ro.sh'      ('ssh ' + (A $behaviour['05'])) 'ro'
    $rows += Row '06' 'tcp_probe' 'sequence_ok' 0 $PREREG '-'                 'tcp_probe 127.0.0.1 9 2000' 'probe'
    $rows += Row '07' 'ssh_stdin' 'always'      0 $PREREG 'PREREG:close.sh'   ('ssh ' + (A $behaviour['07'])) 'close p0'
    $rows += Row '08' 'ssh_stdin' 'always'      0 $PREREG 'PREREG:close.sh'   ('ssh ' + (A $behaviour['08'])) 'close ro'
    $rows += Row '09' 'scp_down'  'always'      0 $ev     '-'                 ('scp ' + (A $behaviour['09'])) 'fetch p0'
    $rows += Row '10' 'scp_down'  'always'      0 $ev     '-'                 ('scp ' + (A $behaviour['10'])) 'fetch ro'
    $rows += Row '11' 'local_bind' 'always'     0 $REC    '-'                 'local_bind 07 09 evidence\WPIQA-P0' 'bind p0'
    $rows += Row '12' 'local_bind' 'always'     0 $REC    '-'                 'local_bind 08 10 evidence\WPIQA-RO' 'bind ro'
    return (($rows -join "`n") + "`n")
}

function Run-Arm([string] $label, [string] $runnerSrc, [string] $planText, [string] $programBlock, [string] $optionBlock, [string[]] $grep) {
    if (Test-Path -LiteralPath $REC) { Remove-Item -LiteralPath $REC -Recurse -Force }
    $planPath = Join-Path $PREREG 'TRANSPORT_PLAN.tsv'
    WriteLf $planPath $planText
    $runner = Join-Path $PREREG 'transport_runner.ps1'
    New-RunnerCopy $runnerSrc $runner (Sha $planPath) $programBlock $optionBlock
    Write-Host ''
    Write-Host ('=== ' + $label + ' ===')
    Write-Host ('COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File ' + $runner + ' -Execute -Confirm WPIQA-EXECUTE')
    $out = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $runner -Execute -Confirm WPIQA-EXECUTE 2>&1
    $rc = $LASTEXITCODE
    foreach ($line in $out) {
        $s = [string]$line
        foreach ($g in $grep) { if ($s -like $g) { Write-Host ('  ' + $s); break } }
    }
    Write-Host ('  RUNNER_RC=' + $rc)
}

$G_CLASS = @('TR_OP_CLASS*','TR_OP_NOT_EVALUABLE*','TR_OP_DEVIANT*','TR_OP_SKIPPED*','TR_RUN_CLASS*','TR_RUN *','TR_STOP*','TR_FIRST*')
$G_ENV   = @('TR_ENV *','TR_ENV_POLICY*','TR_CONFIG*','TR_PROGRAM*','TR_OP_END*','TR_OP_CLASS*','TR_OP_NOT_EVALUABLE*','TR_OP_DEVIANT*','TR_RUN *','TR_STOP*')

# ---- J family: whole-plan classification, program substituted by cmd.exe -----
# DECLARED SUBSTITUTION: the ssh/scp pins are C:\Windows\System32\cmd.exe at its
# real digest and the pinned option block is @('/d','/c'), so each operation's
# native status and output can be driven deterministically with no host. This
# substitutes the PROGRAM, not the classifier under test. The K family below
# drives the real pinned OpenSSH.
$J1 = @{'01'='stop3';'02'='rc0silent';'03'='rc0silent';'04'='rc0silent';'05'='rc0silent';'07'='closefail1';'08'='closefail1';'09'='scpfail1';'10'='scpfail1'}
$J2 = @{'01'='rc255';'02'='rc0silent';'03'='rc0silent';'04'='rc0silent';'05'='rc0silent';'07'='rc0marked';'08'='rc0marked';'09'='scpok';'10'='scpok'}
$J3 = @{'01'='rc2';'02'='rc0silent';'03'='rc0silent';'04'='rc0silent';'05'='rc0silent';'07'='rc0marked';'08'='rc0marked';'09'='scpok';'10'='scpok'}
$J4 = @{'01'='rc0silent';'02'='scpok';'03'='rc0marked';'04'='rc0marked';'05'='rc0marked';'07'='rc0marked';'08'='rc0marked';'09'='scpok';'10'='scpok'}
$J5 = @{'01'='rc1marked';'02'='scpok';'03'='rc0marked';'04'='rc0marked';'05'='rc0marked';'07'='rc0marked';'08'='rc0marked';'09'='scpok';'10'='scpok'}
$J6 = @{'01'='rc0marked';'02'='scpfail1';'03'='rc0marked';'04'='rc0marked';'05'='rc0marked';'07'='rc0marked';'08'='rc0marked';'09'='scpok';'10'='scpok'}

Run-Arm 'J1 RED   round-2 bytes: op01 STOP, then every always row runs' $R2SRC (Plan12 $J1) $PROG_CMD $OPT_CMD $G_CLASS
Run-Arm 'J1 GREEN round-3 bytes: same 12-row fixture'                   $R3SRC (Plan12 $J1) $PROG_CMD $OPT_CMD $G_CLASS
Run-Arm 'J2 RED   round-2 bytes: ssh native rc 255'                     $R2SRC (Plan12 $J2) $PROG_CMD $OPT_CMD $G_CLASS
Run-Arm 'J2 GREEN round-3 bytes: ssh native rc 255'                     $R3SRC (Plan12 $J2) $PROG_CMD $OPT_CMD $G_CLASS
Run-Arm 'J3 RED   round-2 bytes: rc 2 outside the outcome grammar'      $R2SRC (Plan12 $J3) $PROG_CMD $OPT_CMD $G_CLASS
Run-Arm 'J3 GREEN round-3 bytes: rc 2 outside the outcome grammar'      $R3SRC (Plan12 $J3) $PROG_CMD $OPT_CMD $G_CLASS
Run-Arm 'J4 RED   round-2 bytes: ssh rc 0 with NO remote output at all' $R2SRC (Plan12 $J4) $PROG_CMD $OPT_CMD $G_CLASS
Run-Arm 'J4 GREEN round-3 bytes: ssh rc 0 with NO remote output at all' $R3SRC (Plan12 $J4) $PROG_CMD $OPT_CMD $G_CLASS
Run-Arm 'J5 GREEN round-3 bytes: a block that RAN and returned 1 (FAIL must survive)' $R3SRC (Plan12 $J5) $PROG_CMD $OPT_CMD $G_CLASS
Run-Arm 'J6 RED   round-2 bytes: scp transfer failed rc 1'              $R2SRC (Plan12 $J6) $PROG_CMD $OPT_CMD $G_CLASS
Run-Arm 'J6 GREEN round-3 bytes: scp transfer failed rc 1'              $R3SRC (Plan12 $J6) $PROG_CMD $OPT_CMD $G_CLASS

# ---- K family: the REAL pinned OpenSSH, driven by the runner itself ---------
# argv is the pinned option block plus '-G qa-target': ssh evaluates its
# configuration and exits. No connection is attempted and no host is named that
# resolves. This is the operation the round-2 environment could not perform.
$KARGV = 'ssh ' + ($K_OPTIONS -join ' ') + ' -G qa-target'
function PlanK() {
    $rows = @($HDR)
    $rows += Row '01' 'ssh_stdin' 'sequence_ok' 0 $PREREG 'PREREG:setup.sh' $KARGV 'real ssh configuration evaluation'
    return (($rows -join "`n") + "`n")
}
Run-Arm 'K1 RED   round-2 bytes + round-2 child environment + REAL ssh.exe' $R2SRC (PlanK) $PROG_SSH $OPT_K $G_ENV
Run-Arm 'K2 GREEN round-3 bytes + round-3 child environment + REAL ssh.exe' $R3SRC (PlanK) $PROG_SSH $OPT_K $G_ENV

Write-Host ''
Write-Host '=== cleanup ==='
if (Test-Path -LiteralPath $QA) { Remove-Item -LiteralPath $QA -Recurse -Force }
Write-Host ('removed ' + $QA + ' exists=' + (Test-Path -LiteralPath $QA))
```

### C.2 transcript (verbatim)

```text
﻿=== source identities ===
R3 13a57438c12effa108aacc39bbe91345acf7551b76f0991a669059040c5590e4 57826 C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\transport_runner.ps1
R2 2f076ed9a928656fddf22969ea4bf70de895f2c84c73f13b4c64b8040e72aa9a 45066 C:\Users\Public\wpi_r3\r2\transport_runner.ps1
CMD 65ec268add3973b6dca64222985da47caeaee44a340b0ec1466782914fd743d9
SSH 8607ff933e769e77534b1244e39965bcf1c904dbfd4b9da819bbb71034cfef88

=== J1 RED   round-2 bytes: op01 STOP, then every always row runs ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qa\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_FIRST_FAIL id=01 rc=3 expected=0 later_sequence_ops=skip always_ops=run
  TR_OP_NOT_EVALUABLE id=01 rc=3 expected=0
  TR_OP_SKIPPED id=02 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=03 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=04 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=05 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=06 reason=prior_sequence_mismatch
  TR_OP_DEVIANT id=07 rc=1 expected=0
  TR_OP_DEVIANT id=08 rc=1 expected=0
  TR_OP_DEVIANT id=09 rc=1 expected=0
  TR_OP_DEVIANT id=10 rc=1 expected=0
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0
  TR_RUN_CLASS deviant=4 not_evaluable=3 precedence=deviant_outranks_not_evaluable
  TR_RUN FAIL base_run=WPIQA first_fail=01 first_not_evaluable=01 record=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA
  RUNNER_RC=1

=== J1 GREEN round-3 bytes: same 12-row fixture ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qa\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_OP_CLASS id=01 kind=ssh_stdin rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_FIRST_MISMATCH id=01 rc=3 expected=0 class=not_evaluable later_sequence_ops=skip always_ops=run
  TR_OP_NOT_EVALUABLE id=01 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_SKIPPED id=02 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=03 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=04 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=05 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=06 reason=prior_sequence_mismatch
  TR_OP_CLASS id=07 kind=ssh_stdin rc=1 expect_rc=0 class=not_evaluable reason=cleanup_after_unestablished_prerequisite
  TR_OP_NOT_EVALUABLE id=07 rc=1 expected=0 reason=cleanup_after_unestablished_prerequisite
  TR_OP_CLASS id=08 kind=ssh_stdin rc=1 expect_rc=0 class=not_evaluable reason=cleanup_after_unestablished_prerequisite
  TR_OP_NOT_EVALUABLE id=08 rc=1 expected=0 reason=cleanup_after_unestablished_prerequisite
  TR_OP_CLASS id=09 kind=scp_down rc=1 expect_rc=0 class=not_evaluable reason=scp_transfer_did_not_complete
  TR_OP_NOT_EVALUABLE id=09 rc=1 expected=0 reason=scp_transfer_did_not_complete
  TR_OP_CLASS id=10 kind=scp_down rc=1 expect_rc=0 class=not_evaluable reason=scp_transfer_did_not_complete
  TR_OP_NOT_EVALUABLE id=10 rc=1 expected=0 reason=scp_transfer_did_not_complete
  TR_OP_CLASS id=11 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_CLASS id=12 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0 reason=operation_reported_stop
  TR_RUN_CLASS deviant=0 not_evaluable=7 precedence=deviant_outranks_not_evaluable
  TR_RUN STOP base_run=WPIQA first_mismatch=01 first_not_evaluable=01 record=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA
  RUNNER_RC=3

=== J2 RED   round-2 bytes: ssh native rc 255 ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qa\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_FIRST_FAIL id=01 rc=255 expected=0 later_sequence_ops=skip always_ops=run
  TR_OP_DEVIANT id=01 rc=255 expected=0
  TR_OP_SKIPPED id=02 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=03 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=04 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=05 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=06 reason=prior_sequence_mismatch
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0
  TR_RUN_CLASS deviant=1 not_evaluable=2 precedence=deviant_outranks_not_evaluable
  TR_RUN FAIL base_run=WPIQA first_fail=01 first_not_evaluable=11 record=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA
  RUNNER_RC=1

=== J2 GREEN round-3 bytes: ssh native rc 255 ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qa\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_OP_CLASS id=01 kind=ssh_stdin rc=255 expect_rc=0 class=not_evaluable reason=ssh_transport_failure_rc255
  TR_FIRST_MISMATCH id=01 rc=255 expected=0 class=not_evaluable later_sequence_ops=skip always_ops=run
  TR_OP_NOT_EVALUABLE id=01 rc=255 expected=0 reason=ssh_transport_failure_rc255
  TR_OP_SKIPPED id=02 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=03 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=04 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=05 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=06 reason=prior_sequence_mismatch
  TR_OP_CLASS id=07 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=08 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=09 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=10 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=11 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_CLASS id=12 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0 reason=operation_reported_stop
  TR_RUN_CLASS deviant=0 not_evaluable=3 precedence=deviant_outranks_not_evaluable
  TR_RUN STOP base_run=WPIQA first_mismatch=01 first_not_evaluable=01 record=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA
  RUNNER_RC=3

=== J3 RED   round-2 bytes: rc 2 outside the outcome grammar ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qa\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_FIRST_FAIL id=01 rc=2 expected=0 later_sequence_ops=skip always_ops=run
  TR_OP_DEVIANT id=01 rc=2 expected=0
  TR_OP_SKIPPED id=02 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=03 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=04 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=05 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=06 reason=prior_sequence_mismatch
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0
  TR_RUN_CLASS deviant=1 not_evaluable=2 precedence=deviant_outranks_not_evaluable
  TR_RUN FAIL base_run=WPIQA first_fail=01 first_not_evaluable=11 record=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA
  RUNNER_RC=1

=== J3 GREEN round-3 bytes: rc 2 outside the outcome grammar ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qa\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_OP_CLASS id=01 kind=ssh_stdin rc=2 expect_rc=0 class=not_evaluable reason=rc_outside_outcome_grammar
  TR_FIRST_MISMATCH id=01 rc=2 expected=0 class=not_evaluable later_sequence_ops=skip always_ops=run
  TR_OP_NOT_EVALUABLE id=01 rc=2 expected=0 reason=rc_outside_outcome_grammar
  TR_OP_SKIPPED id=02 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=03 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=04 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=05 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=06 reason=prior_sequence_mismatch
  TR_OP_CLASS id=07 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=08 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=09 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=10 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=11 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_CLASS id=12 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0 reason=operation_reported_stop
  TR_RUN_CLASS deviant=0 not_evaluable=3 precedence=deviant_outranks_not_evaluable
  TR_RUN STOP base_run=WPIQA first_mismatch=01 first_not_evaluable=01 record=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA
  RUNNER_RC=3

=== J4 RED   round-2 bytes: ssh rc 0 with NO remote output at all ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qa\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_FIRST_FAIL id=11 rc=3 expected=0 later_sequence_ops=skip always_ops=run
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0
  TR_RUN_CLASS deviant=0 not_evaluable=2 precedence=deviant_outranks_not_evaluable
  TR_RUN STOP base_run=WPIQA first_fail=11 first_not_evaluable=11 record=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA
  RUNNER_RC=3

=== J4 GREEN round-3 bytes: ssh rc 0 with NO remote output at all ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qa\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_OP_CLASS id=01 kind=ssh_stdin rc=0 expect_rc=0 class=not_evaluable reason=no_remote_program_marker_in_capture
  TR_FIRST_MISMATCH id=01 rc=0 expected=0 class=not_evaluable later_sequence_ops=skip always_ops=run
  TR_OP_NOT_EVALUABLE id=01 rc=0 expected=0 reason=no_remote_program_marker_in_capture
  TR_OP_SKIPPED id=02 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=03 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=04 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=05 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=06 reason=prior_sequence_mismatch
  TR_OP_CLASS id=07 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=08 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=09 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=10 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=11 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_CLASS id=12 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0 reason=operation_reported_stop
  TR_RUN_CLASS deviant=0 not_evaluable=3 precedence=deviant_outranks_not_evaluable
  TR_RUN STOP base_run=WPIQA first_mismatch=01 first_not_evaluable=01 record=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA
  RUNNER_RC=3

=== J5 GREEN round-3 bytes: a block that RAN and returned 1 (FAIL must survive) ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qa\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_OP_CLASS id=01 kind=ssh_stdin rc=1 expect_rc=0 class=deviant reason=operation_ran_and_observed_deviant_state
  TR_FIRST_MISMATCH id=01 rc=1 expected=0 class=deviant later_sequence_ops=skip always_ops=run
  TR_OP_DEVIANT id=01 rc=1 expected=0 reason=operation_ran_and_observed_deviant_state
  TR_OP_SKIPPED id=02 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=03 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=04 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=05 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=06 reason=prior_sequence_mismatch
  TR_OP_CLASS id=07 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=08 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=09 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=10 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=11 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_CLASS id=12 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0 reason=operation_reported_stop
  TR_RUN_CLASS deviant=1 not_evaluable=2 precedence=deviant_outranks_not_evaluable
  TR_RUN FAIL base_run=WPIQA first_mismatch=01 first_not_evaluable=11 record=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA
  RUNNER_RC=1

=== J6 RED   round-2 bytes: scp transfer failed rc 1 ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qa\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_FIRST_FAIL id=02 rc=1 expected=0 later_sequence_ops=skip always_ops=run
  TR_OP_DEVIANT id=02 rc=1 expected=0
  TR_OP_SKIPPED id=03 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=04 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=05 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=06 reason=prior_sequence_mismatch
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0
  TR_RUN_CLASS deviant=1 not_evaluable=2 precedence=deviant_outranks_not_evaluable
  TR_RUN FAIL base_run=WPIQA first_fail=02 first_not_evaluable=11 record=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA
  RUNNER_RC=1

=== J6 GREEN round-3 bytes: scp transfer failed rc 1 ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qa\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_OP_CLASS id=01 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=02 kind=scp_up rc=1 expect_rc=0 class=not_evaluable reason=scp_transfer_did_not_complete
  TR_FIRST_MISMATCH id=02 rc=1 expected=0 class=not_evaluable later_sequence_ops=skip always_ops=run
  TR_OP_NOT_EVALUABLE id=02 rc=1 expected=0 reason=scp_transfer_did_not_complete
  TR_OP_SKIPPED id=03 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=04 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=05 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=06 reason=prior_sequence_mismatch
  TR_OP_CLASS id=07 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=08 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=09 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=10 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=11 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_CLASS id=12 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0 reason=operation_reported_stop
  TR_RUN_CLASS deviant=0 not_evaluable=3 precedence=deviant_outranks_not_evaluable
  TR_RUN STOP base_run=WPIQA first_mismatch=02 first_not_evaluable=02 record=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA
  RUNNER_RC=3

=== K1 RED   round-2 bytes + round-2 child environment + REAL ssh.exe ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qa\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_PROGRAM name=ssh path=C:\Windows\System32\OpenSSH\ssh.exe sha256=8607ff933e769e77534b1244e39965bcf1c904dbfd4b9da819bbb71034cfef88 resolution=pinned_absolute chain=trusted
  TR_ENV name=ComSpec value=C:\Windows\System32\cmd.exe
  TR_ENV name=HOMEDRIVE value=C:
  TR_ENV name=HOMEPATH value=\Users\BarışSemaay
  TR_ENV name=PATH value=C:\Windows\System32;C:\Windows
  TR_ENV name=PATHEXT value=.COM;.EXE;.BAT;.CMD
  TR_ENV name=SystemRoot value=C:\Windows
  TR_ENV name=TEMP value=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA\tmp
  TR_ENV name=TMP value=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA\tmp
  TR_ENV name=USERPROFILE value=C:\Users\BarışSemaay
  TR_ENV name=windir value=C:\Windows
  TR_ENV_POLICY cleared=all carried=USERPROFILE,HOMEDRIVE,HOMEPATH inherited_path=never
  TR_OP_END id=01 rc=255 expect_rc=0 elapsed_ms=30 stdout_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  TR_OP_DEVIANT id=01 rc=255 expected=0
  TR_RUN FAIL base_run=WPIQA first_fail=01 first_not_evaluable= record=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA
  RUNNER_RC=1

=== K2 GREEN round-3 bytes + round-3 child environment + REAL ssh.exe ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qa\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_PROGRAM name=ssh path=C:\Windows\System32\OpenSSH\ssh.exe sha256=8607ff933e769e77534b1244e39965bcf1c904dbfd4b9da819bbb71034cfef88 resolution=pinned_absolute chain=trusted
  TR_CONFIG name=ssh_identity path=C:\Users\Public\wpi_r3\qa\cfg\identity sha256=withheld_key_material why=fixture
  TR_CONFIG name=user_known_hosts path=C:\Users\Public\wpi_r3\qa\cfg\known_hosts sha256=3c93622988e8ecd7ffb5b21cd9b256f1fff4130dde6d4442cddb791af51636b9 why=fixture
  TR_CONFIG name=global_known_hosts path=C:\Users\Public\wpi_r3\qa\cfg\known_hosts_global sha256=041ffd2f0e1b4b5d0ab92d6e178a83d8467ee5d82e5760353008c95357d38ae0 why=fixture
  TR_ENV name=ComSpec value=C:\Windows\System32\cmd.exe why=pinned_absolute_so_no_inherited_value_can_name_another_interpreter
  TR_ENV name=PATH value=C:\Windows\System32;C:\Windows why=frozen_to_the_pinned_system_root_the_inherited_PATH_never_reaches_a_child
  TR_ENV name=PATHEXT value=.COM;.EXE;.BAT;.CMD why=frozen_so_extension_search_order_is_not_inherited
  TR_ENV name=PROGRAMDATA value=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA\sshconf why=run_owned_and_empty_OpenSSH_for_Windows_exits_255_with_no_output_when_it_is_unset_and_would_otherwise_read_the_ambient___PROGRAMDATA___ssh_tree
  TR_ENV name=SystemRoot value=C:\Windows why=the_pinned_system_root_every_program_chain_is_adjudicated_against
  TR_ENV name=TEMP value=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA\tmp why=run_owned_under_the_record_root_not_the_operator_temp
  TR_ENV name=TMP value=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA\tmp why=same_value_under_the_second_name
  TR_ENV name=windir value=C:\Windows why=same_value_under_the_legacy_name_some_libraries_still_read
  TR_ENV_POLICY cleared=all carried=none inherited_path=never ambient_ssh_config=disabled_by_-F_none
  TR_OP_END id=01 rc=0 expect_rc=0 elapsed_ms=40 stdout_sha256=4b794585bd843198f570b71c7e11cac29a47874a1acfa6bcbf785c8badbad335 stderr_sha256=d0e14941dee288cc8de19e48436cdf3c2e7939d4b98136c44d954b5f8be73d8a
  TR_OP_CLASS id=01 kind=ssh_stdin rc=0 expect_rc=0 class=not_evaluable reason=no_remote_program_marker_in_capture
  TR_OP_NOT_EVALUABLE id=01 rc=0 expected=0 reason=no_remote_program_marker_in_capture
  TR_RUN STOP base_run=WPIQA first_mismatch=01 first_not_evaluable=01 record=C:\Users\Public\wpi_r3\qa\rec\WPI_TRANSPORT_WPIQA
  RUNNER_RC=3

=== cleanup ===
removed C:\Users\Public\wpi_r3\qa exists=False
```

### C.3 what it establishes

- **J1 — the whole-plan early STOP with every `always` row running.** This is the case
  Codex asked for by name. RED: op 01 STOPs honestly at rc 3, and then the four
  `always` rows that exist to close and retrieve evidence — a close that finds no tree
  (rc 1) twice, and two failed retrievals (rc 1) — are each labelled
  `TR_OP_DEVIANT`, producing `TR_RUN_CLASS deviant=4 not_evaluable=3` and
  **`TR_RUN FAIL` at exit 1**. One honest STOP was outvoted by four consequences of
  itself. GREEN: the same twelve rows give `deviant=0 not_evaluable=7` and
  **`TR_RUN STOP` at exit 3**, with each reason named —
  `cleanup_after_unestablished_prerequisite` for 07/08 and
  `scp_transfer_did_not_complete` for 09/10.
- **J2 — ssh native rc 255.** RED `TR_OP_DEVIANT id=01 rc=255` → `TR_RUN FAIL`, exit 1.
  GREEN `class=not_evaluable reason=ssh_transport_failure_rc255` → `TR_RUN STOP`,
  exit 3.
- **J3 — rc 2, outside the outcome grammar.** RED FAIL exit 1; GREEN
  `reason=rc_outside_outcome_grammar`, STOP exit 3.
- **J4 — the provenance case, and a genuine round-2 false PASS.** ssh returns 0 having
  produced no output whatsoever. RED treats op 01 as a **match** and runs on through
  ops 02–05 — that is, it spends both one-use stage RUNIDs on the strength of an ssh
  that never demonstrated it ran anything — and only STOPs later, at the local bind.
  GREEN STOPs at op 01 with `reason=no_remote_program_marker_in_capture` and skips
  every later `sequence_ok` op.
- **J5 — FAIL must survive.** A block that ran and returned 1, with its
  `EXTRACT_FAIL` marker in the capture, is still `class=deviant reason=operation_ran_and_observed_deviant_state`
  → `TR_RUN FAIL`, exit 1. The repair narrows FAIL; it does not abolish it.
- **J6 — a failed transfer.** RED FAIL exit 1; GREEN
  `reason=scp_transfer_did_not_complete`, STOP exit 3. scp's failure rc is 1, which
  collides with the FAIL class, so the kind decides rather than the integer.
- **K1/K2 — the real pinned `ssh.exe`, through the runner.** K1 runs the audited
  round-2 runner with the audited round-2 child environment and the real program:
  `TR_OP_END id=01 rc=255 … stdout_sha256=e3b0c442… stderr_sha256=e3b0c442…` — the
  empty-file digest on both streams — then `TR_OP_DEVIANT` and `TR_RUN FAIL` exit 1.
  That single arm reproduces F2's `DELIVERED_ENV_RC=255 STDOUT_BYTES=0
  STDERR_BYTES=0` **and** F1's false FAIL simultaneously. K2 runs the round-3 runner:
  the same real program returns rc 0 with real output, the environment lines show
  `carried=none` and a run-owned `PROGRAMDATA`, and the op is classified
  `not_evaluable reason=no_remote_program_marker_in_capture` → `TR_RUN STOP` exit 3,
  which is the truthful classification of an `ssh -G` that evaluated configuration and
  ran no remote program.

---

## 5. Fixture D — configuration identity and the real pinned OpenSSH (F2)

### D.1 `f2_config_qa.ps1` (verbatim)

```powershell
# WP-I transport round 3 - configuration-identity fixture set (F2), plus the
# delivered-file marker gate. Uses the REAL pinned ssh.exe and scp.exe.
# ssh -G evaluates configuration and exits; scp copies local-to-local. Neither
# opens a connection and no host is named that resolves.
Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

$DRAFT = 'C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT'
$R3SRC = Join-Path $DRAFT 'transport_runner.ps1'
$SSH   = 'C:\Windows\System32\OpenSSH\ssh.exe'
$SCP   = 'C:\Windows\System32\OpenSSH\scp.exe'
$SR    = 'C:\Windows'
$QA    = 'C:\Users\Public\wpi_r3\qb'

function Sha([string] $p) { return (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() }
function WriteLf([string] $p, [string] $t) {
    [System.IO.File]::WriteAllText($p, ($t -replace "`r`n", "`n"), (New-Object System.Text.UTF8Encoding($false)))
}

if (Test-Path -LiteralPath $QA) { Remove-Item -LiteralPath $QA -Recurse -Force }
foreach ($d in @('prereg','kit','accepted','cfg','rec','pd_clean\ssh','pd_evil\ssh','tmp')) {
    [void](New-Item -ItemType Directory -Path (Join-Path $QA $d) -Force)
}
$PREREG=Join-Path $QA 'prereg'; $KIT=Join-Path $QA 'kit'; $ACC=Join-Path $QA 'accepted'
$CFG=Join-Path $QA 'cfg'; $REC=Join-Path $QA 'rec\WPI_TRANSPORT_WPIQA'
$PDCLEAN=Join-Path $QA 'pd_clean'; $PDEVIL=Join-Path $QA 'pd_evil'; $TMPD=Join-Path $QA 'tmp'

WriteLf (Join-Path $PREREG 'setup.sh') '# fixture setup'
WriteLf (Join-Path $KIT 'runkit.tar') 'fixture-kit'
WriteLf (Join-Path $KIT 'src.txt') 'wpi-r3-scp-local-arm'
WriteLf (Join-Path $CFG 'identity') 'fixture-identity'
WriteLf (Join-Path $CFG 'known_hosts') 'fixture-known-hosts'
WriteLf (Join-Path $CFG 'known_hosts_global') 'fixture-known-hosts-global'

# ============================================================ M. ambient config
# A hostile system-wide ssh_config planted where __PROGRAMDATA__ resolves. It is
# given an owner-only ACL, because OpenSSH refuses a group/other-writable config
# outright and that refusal would mask the channel under test.
$evilCfg = Join-Path $PDEVIL 'ssh\ssh_config'
[System.IO.File]::WriteAllText($evilCfg, "Host *`r`n    ProxyCommand C:\Windows\System32\cmd.exe /c echo SYSTEM_CONFIG_HIJACK`r`n    StrictHostKeyChecking no`r`n", (New-Object System.Text.ASCIIEncoding))
& icacls.exe $evilCfg /inheritance:r /grant:r ('{0}:(R)' -f $env:USERNAME) | Out-Null
$evilUser = Join-Path $QA 'evil_user_ssh_config'
[System.IO.File]::WriteAllText($evilUser, "Host *`r`n    ProxyCommand C:\Windows\System32\cmd.exe /c echo USER_CONFIG_HIJACK`r`n", (New-Object System.Text.ASCIIEncoding))

function Run-Ssh([hashtable] $envMap, [string[]] $argv) {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $SSH; $psi.Arguments = ($argv -join ' '); $psi.WorkingDirectory = $PREREG
    $psi.UseShellExecute=$false; $psi.CreateNoWindow=$true
    $psi.RedirectStandardOutput=$true; $psi.RedirectStandardError=$true; $psi.RedirectStandardInput=$true
    $psi.EnvironmentVariables.Clear()
    foreach ($k in $envMap.Keys) { $psi.EnvironmentVariables[$k] = $envMap[$k] }
    $p=[System.Diagnostics.Process]::Start($psi); $p.StandardInput.Close()
    $so=$p.StandardOutput.ReadToEnd(); $se=$p.StandardError.ReadToEnd(); $p.WaitForExit()
    $rc=$p.ExitCode; $p.Dispose()
    return [pscustomobject]@{ Rc=$rc; Out=$so; Err=$se }
}
function R2Env([string] $pd) {   # the round-2 constructed environment
    $e=@{}; $e['SystemRoot']=$SR; $e['windir']=$SR; $e['ComSpec']=(Join-Path $SR 'System32\cmd.exe')
    $e['PATHEXT']='.COM;.EXE;.BAT;.CMD'; $e['PATH']=((Join-Path $SR 'System32')+';'+$SR)
    $e['TEMP']=$TMPD; $e['TMP']=$TMPD
    $e['USERPROFILE']=[System.Environment]::GetEnvironmentVariable('USERPROFILE')
    $e['HOMEDRIVE']=[System.Environment]::GetEnvironmentVariable('HOMEDRIVE')
    $e['HOMEPATH']=[System.Environment]::GetEnvironmentVariable('HOMEPATH')
    if ($pd -ne '') { $e['PROGRAMDATA']=$pd }
    return $e
}
function R3Env([string] $pd) {   # the round-3 constructed environment
    $e=@{}; $e['SystemRoot']=$SR; $e['windir']=$SR; $e['ComSpec']=(Join-Path $SR 'System32\cmd.exe')
    $e['PATHEXT']='.COM;.EXE;.BAT;.CMD'; $e['PATH']=((Join-Path $SR 'System32')+';'+$SR)
    $e['TEMP']=$TMPD; $e['TMP']=$TMPD; $e['PROGRAMDATA']=$pd
    return $e
}
$R2OPT = @('-i',(Join-Path $CFG 'identity'),'-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','IdentitiesOnly=yes','-o','ConnectTimeout=20')
$R3OPT = @('-F','none','-i',(Join-Path $CFG 'identity'),
    '-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','IdentitiesOnly=yes','-o','ConnectTimeout=20',
    '-o',('UserKnownHostsFile=' + (Join-Path $CFG 'known_hosts')),
    '-o',('GlobalKnownHostsFile=' + (Join-Path $CFG 'known_hosts_global')),
    '-o','ProxyCommand=none','-o','ControlMaster=no','-o','ControlPath=none','-o','PermitLocalCommand=no',
    '-o','ForwardAgent=no','-o','ForwardX11=no','-o','ClearAllForwardings=yes')

function ShowSsh([string] $lbl, $r, [string[]] $keys) {
    Write-Host ('  ' + $lbl + ' rc=' + $r.Rc + ' stdout_bytes=' + $r.Out.Length + ' stderr_bytes=' + $r.Err.Length)
    foreach ($k in $keys) {
        $hit = '<no ' + $k + ' line>'
        foreach ($l in ($r.Out -split "`n")) { if ($l.Trim().StartsWith($k)) { $hit=$l.Trim(); break } }
        Write-Host ('      | ' + $hit)
    }
}
Write-Host '### M1 RED  - round-2 child environment, exactly as it shipped (no PROGRAMDATA)'
ShowSsh 'M1' (Run-Ssh (R2Env '') (@('-G') + $R2OPT + @('qa-target'))) @()
Write-Host '### M2      - round-2 environment + PROGRAMDATA only: the single load-bearing variable'
ShowSsh 'M2' (Run-Ssh (R2Env $env:ProgramData) (@('-G') + $R2OPT + @('qa-target'))) @()
Write-Host '### M3 RED  - round-2 option set + a reachable ambient system ssh_config'
ShowSsh 'M3' (Run-Ssh (R2Env $PDEVIL) (@('-G') + $R2OPT + @('qa-target'))) @('proxycommand','stricthostkeychecking')
Write-Host '### M4 GREEN- same hostile PROGRAMDATA, round-3 option set'
ShowSsh 'M4' (Run-Ssh (R3Env $PDEVIL) (@('-G') + $R3OPT + @('qa-target'))) @('proxycommand','stricthostkeychecking')
Write-Host '### M5 RED  - a per-user ssh_config selected by -F is honoured'
ShowSsh 'M5' (Run-Ssh (R3Env $PDCLEAN) (@('-G','-F',$evilUser) + $R2OPT + @('qa-target'))) @('proxycommand')
Write-Host '### M6 GREEN- round-3 environment and option set, run-owned empty PROGRAMDATA'
ShowSsh 'M6' (Run-Ssh (R3Env $PDCLEAN) (@('-G') + $R3OPT + @('qa-target'))) @('proxycommand','userknownhostsfile','globalknownhostsfile','identityfile','batchmode','stricthostkeychecking','identitiesonly','connecttimeout','permitlocalcommand','forwardagent','clearallforwardings')
Write-Host '### M7      - one-variable-out bisect of the round-3 environment'
foreach ($drop in @('SystemRoot','windir','ComSpec','PATHEXT','PATH','TEMP','TMP','PROGRAMDATA')) {
    $e = R3Env $PDCLEAN
    [void]$e.Remove($drop)
    $r = Run-Ssh $e (@('-G') + $R3OPT + @('qa-target'))
    Write-Host ('  without_' + $drop.PadRight(12) + ' rc=' + $r.Rc + ' stdout_bytes=' + $r.Out.Length)
}

# ================================================ L/K3. arms through the runner
$ANCHOR = "`$UNFILLED_MARKERS = @('<ALLOCATE-AT-DISPATCH>', '<PIN-AT-FREEZE>')"
$HDR = "op_id`tkind`trun_when`texpect_rc`tcwd`tstdin_file`tstdin_sha256`targv`tpurpose"

function New-RunnerCopy([string] $dst, [string] $planSha, [string] $khSha, [string[]] $options) {
    $text = [System.IO.File]::ReadAllText($R3SRC)
    if (-not $text.Contains($ANCHOR)) { throw 'MUTATION_ANCHOR_NOT_FOUND: $UNFILLED_MARKERS' }
    $optLiteral = "@('" + ($options -join "','") + "')"
    $qa = @"
$ANCHOR
`$BASE_RUN      = 'WPIQA'
`$CONFIRM_TOKEN = 'WPIQA-EXECUTE'
`$PREREG_DIR    = '$PREREG'
`$RUNKIT_DIR    = '$KIT'
`$ACCEPTED_DIR  = '$ACC'
`$RECORD_ROOT   = '$REC'
`$PLAN_SHA256   = '$planSha'
`$PINNED_FILES  = @( @{ Path = (Join-Path `$RUNKIT_DIR 'runkit.tar'); Sha = '$(Sha (Join-Path $KIT 'runkit.tar'))' } )
`$STDIN_ROOTS   = @{ 'PREREG' = `$PREREG_DIR; 'ACCEPTED' = `$ACCEPTED_DIR }
`$PROGRAM_PINS  = @(
    @{ Name = 'ssh'; Path = '$SSH'; Sha = '$(Sha $SSH)' },
    @{ Name = 'scp'; Path = '$SCP'; Sha = '$(Sha $SCP)' }
)
`$SSH_IDENTITY_FILE          = '$CFG\identity'
`$SSH_IDENTITY_SHA           = '$(Sha (Join-Path $CFG 'identity'))'
`$SSH_USER_KNOWN_HOSTS       = '$CFG\known_hosts'
`$SSH_USER_KNOWN_HOSTS_SHA   = '$khSha'
`$SSH_GLOBAL_KNOWN_HOSTS     = '$CFG\known_hosts_global'
`$SSH_GLOBAL_KNOWN_HOSTS_SHA = '$(Sha (Join-Path $CFG 'known_hosts_global'))'
`$CONFIG_PINS = @(
    @{ Name = 'ssh_identity'; Path = `$SSH_IDENTITY_FILE; Sha = `$SSH_IDENTITY_SHA; Print = `$false; Why = 'fixture' },
    @{ Name = 'user_known_hosts'; Path = `$SSH_USER_KNOWN_HOSTS; Sha = `$SSH_USER_KNOWN_HOSTS_SHA; Print = `$true; Why = 'fixture' },
    @{ Name = 'global_known_hosts'; Path = `$SSH_GLOBAL_KNOWN_HOSTS; Sha = `$SSH_GLOBAL_KNOWN_HOSTS_SHA; Print = `$true; Why = 'fixture' }
)
`$SSH_PINNED_OPTIONS = $optLiteral
"@
    [System.IO.File]::WriteAllText($dst, $text.Replace($ANCHOR, $qa), (New-Object System.Text.UTF8Encoding($false)))
}

function Run-Runner([string] $label, [string] $planText, [string] $khSha, [string[]] $options, [string[]] $grep) {
    if (Test-Path -LiteralPath $REC) { Remove-Item -LiteralPath $REC -Recurse -Force }
    if (Test-Path -LiteralPath (Join-Path $KIT 'dst.txt')) { Remove-Item -LiteralPath (Join-Path $KIT 'dst.txt') -Force }
    $planPath = Join-Path $PREREG 'TRANSPORT_PLAN.tsv'
    WriteLf $planPath $planText
    $runner = Join-Path $PREREG 'transport_runner.ps1'
    New-RunnerCopy $runner (Sha $planPath) $khSha $options
    Write-Host ''
    Write-Host ('=== ' + $label + ' ===')
    Write-Host ('COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File ' + $runner + ' -Execute -Confirm WPIQA-EXECUTE')
    $out = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $runner -Execute -Confirm WPIQA-EXECUTE 2>&1
    $rc = $LASTEXITCODE
    foreach ($line in $out) { $s=[string]$line; foreach ($g in $grep) { if ($s -like $g) { Write-Host ('  '+$s); break } } }
    Write-Host ('  RUNNER_RC=' + $rc)
}
$G = @('TR_STOP*','TR_OP_CLASS*','TR_OP_END*','TR_RUN *','TR_CONFIG*')
$KHSHA = Sha (Join-Path $CFG 'known_hosts')

# K3: the REAL pinned scp.exe, driven by the runner, copying local-to-local.
$k3argv = 'scp ' + ($R3OPT -join ' ') + ' src.txt dst.txt'
$k3 = ($HDR + "`n" + ('02' + "`t" + 'scp_up' + "`t" + 'sequence_ok' + "`t0`t" + $KIT + "`t-`t-`t" + $k3argv + "`treal local-to-local transfer, no network") + "`n")
Run-Runner 'K3 GREEN real pinned scp.exe through the runner, local-to-local, no network' $k3 $KHSHA $R3OPT $G
Write-Host ('  DST_CONTENT=[' + (Get-Content -LiteralPath (Join-Path $KIT 'dst.txt') -Raw).Trim() + ']')

# L2: a plan row that drops -F none must not run.
$tampered = @($R3OPT); $tampered[0] = '-o'; $tampered[1] = 'LogLevel=ERROR'
$l2argv = 'scp ' + ($tampered -join ' ') + ' src.txt dst.txt'
$l2 = ($HDR + "`n" + ('02' + "`t" + 'scp_up' + "`t" + 'sequence_ok' + "`t0`t" + $KIT + "`t-`t-`t" + $l2argv + "`ta plan row with the ambient-config refusal removed") + "`n")
Run-Runner 'L2 GREEN plan row drops -F none: the frozen option block refuses it' $l2 $KHSHA $R3OPT $G

# L3: an unfilled configuration pin must not run.
Run-Runner 'L3 GREEN a configuration pin is still unfilled' $k3 '<PIN-AT-FREEZE>' $R3OPT $G

Write-Host ''
Write-Host '=== L1 the delivered file, exactly as it ships, default (dry-run) mode ==='
Write-Host ('COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File ' + $R3SRC)
$o = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $R3SRC 2>&1
Write-Host ('  ' + (($o | ForEach-Object { [string]$_ }) -join "`n  "))
Write-Host ('  RUNNER_RC=' + $LASTEXITCODE)

Write-Host ''
Write-Host '=== cleanup ==='
# The hostile config had its inherited ACEs stripped so OpenSSH would accept it;
# restore inheritance before removing the tree.
if (Test-Path -LiteralPath $evilCfg) { & icacls.exe $evilCfg /inheritance:e /grant ('{0}:(F)' -f $env:USERNAME) | Out-Null }
if (Test-Path -LiteralPath $QA) { Remove-Item -LiteralPath $QA -Recurse -Force }
Write-Host ('removed ' + $QA + ' exists=' + (Test-Path -LiteralPath $QA))
```

### D.2 transcript (verbatim)

```text
﻿### M1 RED  - round-2 child environment, exactly as it shipped (no PROGRAMDATA)
  M1 rc=255 stdout_bytes=0 stderr_bytes=0
### M2      - round-2 environment + PROGRAMDATA only: the single load-bearing variable
  M2 rc=0 stdout_bytes=3915 stderr_bytes=72
### M3 RED  - round-2 option set + a reachable ambient system ssh_config
  M3 rc=0 stdout_bytes=3986 stderr_bytes=72
      | proxycommand C:\Windows\System32\cmd.exe /c echo SYSTEM_CONFIG_HIJACK
      | stricthostkeychecking true
### M4 GREEN- same hostile PROGRAMDATA, round-3 option set
  M4 rc=0 stdout_bytes=3858 stderr_bytes=72
      | <no proxycommand line>
      | stricthostkeychecking true
### M5 RED  - a per-user ssh_config selected by -F is honoured
  M5 rc=0 stdout_bytes=3984 stderr_bytes=72
      | proxycommand C:\Windows\System32\cmd.exe /c echo USER_CONFIG_HIJACK
### M6 GREEN- round-3 environment and option set, run-owned empty PROGRAMDATA
  M6 rc=0 stdout_bytes=3858 stderr_bytes=72
      | <no proxycommand line>
      | userknownhostsfile C:\Users\Public\wpi_r3\qb\cfg\known_hosts
      | globalknownhostsfile C:\Users\Public\wpi_r3\qb\cfg\known_hosts_global
      | identityfile C:\Users\Public\wpi_r3\qb\cfg\identity
      | batchmode yes
      | stricthostkeychecking true
      | identitiesonly yes
      | connecttimeout 20
      | permitlocalcommand no
      | forwardagent no
      | clearallforwardings yes
### M7      - one-variable-out bisect of the round-3 environment
  without_SystemRoot   rc=0 stdout_bytes=3858
  without_windir       rc=0 stdout_bytes=3858
  without_ComSpec      rc=0 stdout_bytes=3858
  without_PATHEXT      rc=0 stdout_bytes=3858
  without_PATH         rc=0 stdout_bytes=3858
  without_TEMP         rc=0 stdout_bytes=3858
  without_TMP          rc=0 stdout_bytes=3858
  without_PROGRAMDATA  rc=255 stdout_bytes=0

=== K3 GREEN real pinned scp.exe through the runner, local-to-local, no network ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qb\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_CONFIG name=ssh_identity path=C:\Users\Public\wpi_r3\qb\cfg\identity sha256=withheld_key_material why=fixture
  TR_CONFIG name=user_known_hosts path=C:\Users\Public\wpi_r3\qb\cfg\known_hosts sha256=3c93622988e8ecd7ffb5b21cd9b256f1fff4130dde6d4442cddb791af51636b9 why=fixture
  TR_CONFIG name=global_known_hosts path=C:\Users\Public\wpi_r3\qb\cfg\known_hosts_global sha256=041ffd2f0e1b4b5d0ab92d6e178a83d8467ee5d82e5760353008c95357d38ae0 why=fixture
  TR_OP_END id=02 rc=0 expect_rc=0 elapsed_ms=97 stdout_sha256=a04c3131d5d2d6a794281b2525967934811d733be6dfce8658ac90f520f8a14f stderr_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  TR_OP_CLASS id=02 kind=scp_up rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_RUN PASS base_run=WPIQA record=C:\Users\Public\wpi_r3\qb\rec\WPI_TRANSPORT_WPIQA
  RUNNER_RC=0
  DST_CONTENT=[wpi-r3-scp-local-arm]

=== L2 GREEN plan row drops -F none: the frozen option block refuses it ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qb\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_STOP reason=plan_row_pinned_option_differs op=02 index=1 actual=[-o] expected=[-F]
  RUNNER_RC=3

=== L3 GREEN a configuration pin is still unfilled ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Public\wpi_r3\qb\prereg\transport_runner.ps1 -Execute -Confirm WPIQA-EXECUTE
  TR_STOP reason=unfilled_marker field=CONFIG_PINS.Sha[user_known_hosts]
  RUNNER_RC=3

=== L1 the delivered file, exactly as it ships, default (dry-run) mode ===
COMMAND: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\transport_runner.ps1
  TR_HEADER base_run=<ALLOCATE-AT-DISPATCH>
  TR_MODE execute=False confirm_supplied=False
  TR_STOP reason=unfilled_marker field=BASE_RUN
  RUNNER_RC=3

=== cleanup ===
powershell.exe : Remove-Item : Cannot remove item C:\Users\Public\wpi_r3\qb\pd_evil\ssh\ssh_config: Yola erişim 
engellendi.
At line:1 char:302
+ ... tch {} } }; powershell.exe -NoProfile -ExecutionPolicy Bypass -File ' ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Remove-Item : C...şim engellendi.:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
At C:\Users\Public\wpi_r3\f2_config_qa.ps1:190 char:35
+ ... th -LiteralPath $QA) { Remove-Item -LiteralPath $QA -Recurse -Force }
+                            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgument: (ssh_config:FileInfo) [Remove-Item], ArgumentException
    + FullyQualifiedErrorId : RemoveFileSystemItemArgumentError,Microsoft.PowerShell.Commands.RemoveItemCommand
```

### D.3 what it establishes

- **M1 — the round-2 environment exactly as it shipped.** The real
  `C:\Windows\System32\OpenSSH\ssh.exe` returns **rc 255 with 0 bytes on both
  streams**. Codex's finding, reproduced independently.
- **M2 — the cause.** Adding `PROGRAMDATA` alone returns rc 0 with 3915 bytes of
  configuration output.
- **M7 — and it is the only cause.** Dropping each constructed variable in turn leaves
  `ssh -G` at rc 0 for `SystemRoot`, `windir`, `ComSpec`, `PATHEXT`, `PATH`, `TEMP`
  and `TMP`; only `without_PROGRAMDATA` returns 255 with 0 bytes. The other variables
  remain justified — they are what keeps the inherited `PATH` and the operator's
  `TEMP` out of the child — but the F2 defect is precisely and only the missing
  `PROGRAMDATA`.
- **M3/M4 — the system-wide configuration channel, which round 2 left open.** With the
  round-2 option set and a reachable ambient `__PROGRAMDATA__\ssh\ssh_config`,
  `ssh -G` reports
  `proxycommand C:\Windows\System32\cmd.exe /c echo SYSTEM_CONFIG_HIJACK`: an external
  program interposed into the transport by inherited state, which is Codex F3's
  principle reaching the one channel its falsification did not. With `-F none` the
  same hostile file produces no `proxycommand` line at all.
- **M5/M6 — the per-user channel.** A configuration file selected by `-F` is honoured
  (`USER_CONFIG_HIJACK`); `-F none` selects nothing. M6 then shows the whole pinned
  set in effect: the pinned `userknownhostsfile`, `globalknownhostsfile` and
  `identityfile`, `batchmode yes`, `stricthostkeychecking true`, `identitiesonly yes`,
  `connecttimeout 20`, `permitlocalcommand no`, `forwardagent no`,
  `clearallforwardings yes`, and no `proxycommand`.
- **K3 — a real, no-network process-capture arm.** The runner drives the **real**
  pinned `scp.exe` under the round-3 environment for a local-to-local copy:
  `TR_OP_END id=02 rc=0`, `class=match`, `TR_RUN PASS`, exit 0, and
  `DST_CONTENT=[wpi-r3-scp-local-arm]` — bytes actually moved, no socket opened.
- **L2 — the option block is a property of the runner, not of the plan.** A plan row
  with `-F none` replaced by `-o LogLevel=ERROR` gives
  `TR_STOP reason=plan_row_pinned_option_differs op=02 index=1 actual=[-o] expected=[-F]`,
  exit 3.
- **L3 — an unfilled configuration pin cannot run.** `TR_STOP reason=unfilled_marker
  field=CONFIG_PINS.Sha[user_known_hosts]`, exit 3. Recorded honestly: the *marker
  gate* fires first, so the later `config_pin_unfilled` branch is reachable only for a
  malformed non-marker value and was **not** driven — see §7.
- **L1 — the delivered file, exactly as it ships.** `TR_STOP reason=unfilled_marker
  field=BASE_RUN`, exit 3, before a path is evaluated. Claude round-1 F6 / V16 is not
  regressed.

---

## 6. Derivation boundary — `remote_close_tree_wpi.sh`

The Lead adjudication was *derive, do not edit*: the accepted `remote_close_tree.sh`
is byte-frozen input and is not touched. It is not touched — its digest is re-verified
at the head of the F3 transcript as `87157f0e…`, 7470 B, and it is read but never
written.

```
git diff --no-index --stat \
  WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/remote_close_tree.sh \
  WPI_BLOCKS_DRAFT/remote_close_tree_wpi.sh
 1 file changed, 115 insertions(+), 30 deletions(-)
```

The insertion side is the header, the nine `TOOL_*` pins, `require_tool`,
`record_tool_digest` and the digest loop. What decides whether the derivation is
bounded is the **deletion** side: every line of accepted logic that no longer exists.
Excluding comments and blank lines, it is exactly seventeen lines:

```
-[ "$#" -eq 2 ] || fail "usage remote_close_tree.sh <EV_DIR> <RUNID> argc=$#"
-    err="$(mktemp)" || stop "probe_tempfile_failed path=$p"
-    kind="$(LC_ALL=C stat -c '%F' -- "$p" 2>"$err")" || rc=$?
-        rm -f "$err"
-    detail="$(tr -d '\r\n' <"$err")"; rm -f "$err"
-CANON="$(readlink -f -- "$EV_DIR")" || stop "canonicalization_failed path=$EV_DIR"
-OWN="$(LC_ALL=C stat -c '%U:%G' -- "$EV_DIR")" || stop "owner_probe_failed path=$EV_DIR"
-MODE="$(LC_ALL=C stat -c '%a' -- "$EV_DIR")"   || stop "mode_probe_failed path=$EV_DIR"
-ODD="$(LC_ALL=C find "$EV_DIR" -mindepth 1 '!' -type d '!' -type f -print)" \
-WORK="$(mktemp -d)" || stop "workdir_failed"
-LC_ALL=C find "$EV_DIR" -type f -print0 > "$RAW" \
-LC_ALL=C sort -z "$RAW" -o "$SORTED" \
-        out="$(LC_ALL=C sha256sum -- "$f")" || { stop "digest_failed path=$f"; }
-LC_ALL=C cmp -s "$PASS1" "$PASS2" \
-    SZ="$(LC_ALL=C stat -c '%s' -- "$f")" || stop "size_probe_failed path=$f"
-SET_SUM="$(LC_ALL=C sha256sum -- "$PASS1")" || stop "digest_set_hash_failed"
-rm -rf -- "$WORK"
```

Sixteen of the seventeen are a bare tool invocation replaced by the same invocation
through its frozen absolute pin — class 2, and nothing else. The seventeenth is the
`usage` diagnostic string, which names the script and therefore names the derived
script. No predicate, no rc, no ordering, no output record and no comparison changed.
The rendered `%U:%G` owner comparison is **retained deliberately**: making it numeric
would be a class 3 change and is outside this derivation's permitted delta. It is
disclosed here and in the script header as an inherited residual rather than repaired
without authority.

Two residuals are disclosed rather than claimed away, both in the script's own header:

1. **Tool bytes are not bound.** The pins bind a locator and that object's metadata.
   Each admitted tool's SHA-256 is emitted as evidence and is deliberately not
   compared to a frozen value, because no digest of a remote tool can be known before
   host contact and a digest a run learns from the object it is attesting is not an
   attestation. The script says so on its own `CLOSE_NOTE tool_digest_limit …` line.
2. **`mktemp` still honours the login `TMPDIR`.** The work directory's location is
   inherited. It is created outside `EV_DIR` by construction and nothing is written
   into the evidence tree either way. Deleting `mktemp` would be a class 3 change.

---

## 7. Coverage accounting

**Driven this round, with real output above:** F3 RED/G0/GREEN/CTL; F4 RED/GREEN/CTL/PIN
and reader arms N1–N5; F1 arms J1–J6 (RED and GREEN, ten runner executions) and K1–K2;
F2 arms M1–M7, K3, L1–L3. Twelve of those executions are the real pinned OpenSSH
programs.

**Deliberately not driven, and the direction each fails in:**

| arm | why not | direction |
|---|---|---|
| `config_pin_unfilled` | the marker gate fires first on the literal placeholder (L3); this branch needs a malformed non-marker value | STOP, rc 3 |
| `Invoke-TcpProbe` `timeout` / `connect_incomplete` / `local_exception` / `socket_error` | need socket states loopback will not produce inside this no-network envelope | all STOP, rc 3 |
| `Test-TrustedProgramChain` reparse-point branch | needs a reparse point under `%SystemRoot%`, i.e. elevation | STOP, rc 3 |
| `program_sha256_mismatch`, `chain_owner_sid_untrusted`, `chain_component_is_reparse_point` | driven and recorded in the round-2 self-QA and re-driven by the Claude round-2 re-audit (`C2`/`C3`/`C4`); unchanged this round | STOP, rc 3 |
| the round-1 closure arms for Codex F2/F4/F6/F8/F9/F10 and Claude F1/F3/F5/F6 | unchanged code paths; re-verified only by the identity table in §9 and by `bash -n` / parser checks | — |
| the six-member happy path against a real `runkit.tar` | the WP-I kit does not exist before Stage 1; `01_RUNKIT` is absent and the runner STOPs at `pinned_file_pin_unfilled` | STOP, rc 3 |
| `remote_close_tree_wpi.sh` against a real WP-I evidence tree | same reason | STOP or FAIL, never a false PASS |

**Counts are bookkeeping, not closure.** Every number above is a count of arms whose
exact command and real output appear in §2–§5; no arm is counted that is not printed.

---

## 8. What this round did not verify

- **Real connection behaviour of `ssh` and `scp`.** `ssh -G` evaluates configuration
  and exits; the local `scp` arm copies between two local paths. Both are real
  executions of the real pinned programs under the real constructed environment, and
  they establish that the programs initialise, parse the pinned option block, and
  apply it. They do **not** establish that the host accepts the pinned host key, that
  the credential authenticates, or that a remote `bash -s` runs. Those need host
  contact authority this session does not have.
- **Remote tool bytes.** See §6 residual 1.
- **`GATEA-STAGING`'s `/usr/bin` tool kinds.** Deviation D-3 remains a hard Stage-1
  precondition: each `/usr/bin/<tool>` in the pin set must be a regular, root-owned,
  not-group/other-writable file or ops 01, 03, 07 and 08 will STOP at dispatch. This
  kernel ships them as symlinks and the scripts refuse them, which is the safe
  direction but is not the target host's state.
- **The `EXPECT_PARENT_MOUNT` value itself.** The predicate is proven; the constant is
  a freeze-gate input that the owner-authorised grant-#6 attestation must supply, and
  the successor preregistration must order that attestation **before op 01**.
- **`RP6-P0.sh` and `RP7-WPI-RO.sh`.** Separate T0 slots, under concurrent repair.
  Neither is a transport target and neither was read or written by this round.

---

## 9. Syntax, placeholders, identities

`bash -n` passes on all five in-scope shell files and on the accepted
`remote_close_tree.sh`. `[Parser]::ParseFile` on `transport_runner.ps1` reports **0
errors** under Windows PowerShell 5.1.26100.8875; the file contains no `&&`, `||` or
ternary. Zero CR bytes in all seven executable/plan files; the runner and the plan are
pure ASCII.

### Placeholder census (N1)

The round-2 self-QA recorded "36 `<ALLOCATE-AT-DISPATCH>`, 40 `<PIN-AT-FREEZE>`". The
36 was the six-file figure and the 40 was not re-derivable from any consistent scope.
Re-derived from the rejected baseline at commit `9ef4437d`, per file:

| file | `<ALLOCATE-AT-DISPATCH>` | `<PIN-AT-FREEZE>` |
|---|---:|---:|
| `run_p0.sh` | 6 | 3 |
| `run_ro.sh` | 6 | 5 |
| `transport_runner.ps1` | 4 | 5 |
| `TRANSPORT_PLAN.tsv` | 20 | 5 |
| `remote_setup_wpi.sh` | 0 | 2 |
| `remote_extract_verify_wpi.sh` | 0 | 7 |
| **six executable/plan files** | **36** | **27** |
| `SELF_QA_TRANSPORT.md` | 4 | 5 |
| `STATUS_TRANSPORT.md` | 1 | 1 |
| **all eight files** | **41** | **33** |

which is exactly the correction both re-audits asked for. The round-3 delivered set is
recorded in `TRANSPORT_REPAIR_R3_REPORT.md` §4 (`Delivered identities`) over its own scope — seven
executable/plan files, since `remote_close_tree_wpi.sh` joins the set — so the census
is stated over the set it closes rather than mixing scopes.

One observation the census surfaced, disclosed rather than silently fixed: a guard that
detects an unfilled placeholder by comparing against the literal placeholder text is
destroyed by a Stage-1 fill that replaces that text globally — the guard would then
hold the real value and STOP on a correctly frozen file. `remote_setup_wpi.sh`
therefore **composes** its marker (`PIN_MARKER="$(printf '<PIN-%s>' 'AT-FREEZE')"`)
rather than writing it out. The runner's pre-existing `$UNFILLED_MARKERS` array carries
the same shape and was accepted in round 2; it is left unchanged this round and flagged
for the Stage-1 fill procedure, which must fill constants individually rather than by
blind global replacement.

All `<ALLOCATE-AT-DISPATCH>` and `<PIN-AT-FREEZE>` markers in the delivered set remain
literal. No RUNID was minted; the only concrete `WPLP2-…` text is `$ACCEPTED_DIR`,
which is accepted-source provenance, not a WP-I allocation.


---

# ROUND 4 - 2026-08-11 - F1-F4 and T5-T8, executed RED/GREEN

Implementer session: Claude Opus 5 xhigh (Max account), under
`KICKOFF_TRANSPORT_REPAIR_R4.md` plus `KICKOFF_TRANSPORT_R4_MAX_ADDENDUM.md`.
Everything below was produced by running code on this machine. Nothing in this
section is narrated: each block is the literal transcript of the harness named
above it, and the harnesses are committed beside the targets so a re-auditor can
re-run them.

**No host was contacted and no network connection was opened.** The Linux
fixtures run against a local WSL2 Ubuntu kernel; every path they touch is under
`/root/wpi_r4*` on that local filesystem. The operator-side fixtures start no
process at all: they inject per-operation `(rc, capture)` pairs into the runner's
own extracted bytes.

## R4-0. The three harnesses and what each proves

| Harness | Executes | Proves |
|---|---|---|
| `_r4_runner_probe.ps1` | named regions of `transport_runner.ps1` extracted **verbatim** and `Invoke-Expression`-ed: the outcome grammar, the marker-family map, the prerequisite map, the provenance test, the prerequisite resolver, the classifier, the per-op classification/counter block and the run rollup | F1 wrong-family, F4 decisive fixture, the Claude scenario, the two distinct cleanup reasons |
| `_r4_wsl_fixtures.sh` | the delivered shell bytes, with declared pin retargeting only | F1 PATH/`BASH_ENV`/launch domain, F2 `TMPDIR`-into-evidence, F3 mixed diagnostic, T6 composition and argv arity |
| `_r4_t5_compose.sh` | the real `run_p0.sh` under the frozen launch domain, and the real `RP6-P0.sh` row-8 gate bytes | T5 wiring of the five `P0_ATTESTED_*` values |

RED is never a description of what round 3 "would have" done. The runner probe
extracts the same regions from the **round-3 blob at commit `78173bfd`**, and the
shell fixtures run the round-3 and superseded close scripts themselves.

The probe's region extractor prints the line range and SHA-256 of every region it
lifts, so the reader can confirm the code under test is the file's own bytes
rather than a paraphrase. Two regions are lifted by unique start/end anchors and
three by brace balance; every slice is brace-balance-checked before execution.

### Declared fixture retargeting, and nothing else

On this kernel the `/usr/bin` coreutils names are symlinks to a multicall binary,
and the delivered `require_tool` correctly refuses a symlink. The fixtures
therefore retarget the declared `TOOL_*` pins to regular, root-owned, mode-0755
copies under `/root/wpi_r4/tools`, fill `EXPECT_UID`/`EXPECT_GID` with this
login's numeric identity, and fill `EXPECT_LAUNCH_HOME` with this login's `HOME`.
`TOOL_BASH` and the attested interpreter stay `/usr/bin/bash`, which IS a regular
root-owned file here. The op-01 allocation case additionally retargets
`EXPECT_PREFIX`/`EXPECT_PARENT` and fills `EXPECT_PARENT_MOUNT` from the observed
projection - which would be **illegitimate in production**, is labelled as such in
the transcript, and proves the allocation shape only, never the mount binding. No
predicate, classification, ordering or emitted record was altered anywhere.

## R4-1. Finding index: which block below is the evidence

| Item | RED | GREEN | Verdict |
|---|---|---|---|
| F1 remote interpreter outside the pinned domain | `F1 RED - a fake bash first on PATH` (rc 0, plant ran, forged marker); `F1 RED - inherited BASH_ENV` (rc 0, plant ran, forged marker) | `F1 GREEN - the frozen launch domain neutralises both plants` (rc 0, `PATH_HIT=no STARTUP_HIT=no`, real record) | **OPEN — verdict corrected in round 5.** Inner child closed; outer SSH account-shell boundary open. The round-4 entry read "closed on the composition; one residual measured and disclosed below" and is WITHDRAWN — see §R5-2 |
| F1 unrelated marker family accepted | probe `FIXTURE D [round3]`: op 07 `class=match` from a `SETUP` marker, run PASS | probe `FIXTURE D [round4]`: `not_evaluable reason=no_remote_program_marker_in_capture expected_family=remote_close_tree_wpi.sh`, run STOP | closed |
| F2 inherited `TMPDIR` writes inside evidence | `F2 RED` - rc 0, a `tmp.*/raw.0` member hashed inside the tree, `wrote_into_evidence_tree=0` | `F2 GREEN` - rc 3 `launch_domain_unexpected_environment_entry name=[TMPDIR]`; the clean run leaves no residue; the class-6 overlap case is refused before `mkdir` | closed |
| F3 mixed probe diagnostic read as absence | `F3 RED` - rc 1 `CLOSE_FAIL reason=evidence_dir_absent` | `F3 GREEN` - rc 3 `CLOSE_STOP reason=path_probe_error ... No such file or directory; Permission denied` | closed |
| F4 global `always` prerequisite | probe `FIXTURE A [round3]`: `deviant=0`, `TR_RUN STOP` - the RO deviation erased | probe `FIXTURE A [round4]`: `deviant=1`, `TR_RUN FAIL` - the RO deviation counted | closed |
| F4 Claude scenario must still hold | - | probe `FIXTURE B [round4]`: `TR_RUN STOP`, cleanup stays not-evaluable | held |
| F4 distinct cleanup reasons | probe `FIXTURE C [round3]`: op 08 `cleanup_after_unestablished_prerequisite` | probe `FIXTURE C [round4]`: op 08 `cleanup_after_earlier_deviation prerequisites=[05=deviant]` | closed |
| T5 `P0_ATTESTED_*` wiring | `A-RED` 0 names exported; `B-RED` the real gate STOPs `preregistered_value_missing` | `A-GREEN` 5 names exported; `B-GREEN2` the real gate prints `P0_GATE_PASSED` | closed |
| T6 close contract vs bytes vs plan | the superseded edit self-STOPs on its own clean launch; its two-argument call returns `CLOSE_FAIL` rc 1 | op 01 allocates `<BASE>/work`; the exact plan argv shape closes the tree at rc 0; the two-argument call is now `CLOSE_STOP` rc 3 | closed |
| T7 inert `WPI_INTERPRETER_TARGET` | round-3 `run_ro.sh:45,118` defined and exported it | static gate: 0 assignments, 0 exports, the block reads it 0 times | closed |
| T8 stale transport summary | - | documentation only; no executable predicate exists and none is claimed | closed as a draft edit |

## R4-2. `_r4_runner_probe.ps1` - round 3 (RED)

```text
RUNNER path=C:\Users\BARSEM~1\AppData\Local\Temp\claude\C--LAB-Tradingview-LAB-CLEAN\8ec0dbac-0511-4a3e-968b-7fe9ff2eebce\scratchpad\r3\transport_runner.ps1
RUNNER sha256=13a57438c12effa108aacc39bbe91345acf7551b76f0991a669059040c5590e4
VARIANT round3
=== FIXTURE A - F4 decisive: independent RO close FAIL after unrelated P0 close STOP [round3] ===
  TR_OP_CLASS id=01 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=02 kind=scp_up rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=03 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=04 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=05 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=06 kind=tcp_probe rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=07 kind=ssh_stdin rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_FIRST_MISMATCH id=07 rc=3 expected=0 class=not_evaluable later_sequence_ops=skip always_ops=run
  TR_OP_NOT_EVALUABLE id=07 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_CLASS id=08 kind=ssh_stdin rc=1 expect_rc=0 class=not_evaluable reason=cleanup_after_unestablished_prerequisite
  TR_ADDITIONAL_MISMATCH id=08 first_mismatch=07
  TR_OP_NOT_EVALUABLE id=08 rc=1 expected=0 reason=cleanup_after_unestablished_prerequisite
  TR_OP_CLASS id=09 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=10 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=11 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_ADDITIONAL_MISMATCH id=11 first_mismatch=07
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_CLASS id=12 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_ADDITIONAL_MISMATCH id=12 first_mismatch=07
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0 reason=operation_reported_stop
  TR_RUN_CLASS deviant=0 not_evaluable=4 precedence=deviant_outranks_not_evaluable
  TR_RUN STOP base_run=PROBE-BASE-RUN first_mismatch=07 first_not_evaluable=07 record=C:\Users\BARSEM~1\AppData\Local\Temp\claude\C--LAB-Tradingview-LAB-CLEAN\8ec0dbac-0511-4a3e-968b-7fe9ff2eebce\scratchpad\probe_round3
  PROBE_EXIT_CODE=3

=== FIXTURE B - genuinely unestablished prerequisite stays not-evaluable [round3] ===
  TR_OP_CLASS id=01 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=02 kind=scp_up rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=03 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=04 kind=ssh_stdin rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_FIRST_MISMATCH id=04 rc=3 expected=0 class=not_evaluable later_sequence_ops=skip always_ops=run
  TR_OP_NOT_EVALUABLE id=04 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_SKIPPED id=05 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=06 reason=prior_sequence_mismatch
  TR_OP_CLASS id=07 kind=ssh_stdin rc=1 expect_rc=0 class=not_evaluable reason=cleanup_after_unestablished_prerequisite
  TR_ADDITIONAL_MISMATCH id=07 first_mismatch=04
  TR_OP_NOT_EVALUABLE id=07 rc=1 expected=0 reason=cleanup_after_unestablished_prerequisite
  TR_OP_CLASS id=08 kind=ssh_stdin rc=1 expect_rc=0 class=not_evaluable reason=cleanup_after_unestablished_prerequisite
  TR_ADDITIONAL_MISMATCH id=08 first_mismatch=04
  TR_OP_NOT_EVALUABLE id=08 rc=1 expected=0 reason=cleanup_after_unestablished_prerequisite
  TR_OP_CLASS id=09 kind=scp_down rc=1 expect_rc=0 class=not_evaluable reason=scp_transfer_did_not_complete
  TR_ADDITIONAL_MISMATCH id=09 first_mismatch=04
  TR_OP_NOT_EVALUABLE id=09 rc=1 expected=0 reason=scp_transfer_did_not_complete
  TR_OP_CLASS id=10 kind=scp_down rc=1 expect_rc=0 class=not_evaluable reason=scp_transfer_did_not_complete
  TR_ADDITIONAL_MISMATCH id=10 first_mismatch=04
  TR_OP_NOT_EVALUABLE id=10 rc=1 expected=0 reason=scp_transfer_did_not_complete
  TR_OP_CLASS id=11 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_ADDITIONAL_MISMATCH id=11 first_mismatch=04
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_CLASS id=12 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_ADDITIONAL_MISMATCH id=12 first_mismatch=04
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0 reason=operation_reported_stop
  TR_RUN_CLASS deviant=0 not_evaluable=7 precedence=deviant_outranks_not_evaluable
  TR_RUN STOP base_run=PROBE-BASE-RUN first_mismatch=04 first_not_evaluable=04 record=C:\Users\BARSEM~1\AppData\Local\Temp\claude\C--LAB-Tradingview-LAB-CLEAN\8ec0dbac-0511-4a3e-968b-7fe9ff2eebce\scratchpad\probe_round3
  PROBE_EXIT_CODE=3

=== FIXTURE C - cleanup after an earlier deviation on its own branch [round3] ===
  TR_OP_CLASS id=01 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=02 kind=scp_up rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=03 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=04 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=05 kind=ssh_stdin rc=1 expect_rc=0 class=deviant reason=operation_ran_and_observed_deviant_state
  TR_FIRST_MISMATCH id=05 rc=1 expected=0 class=deviant later_sequence_ops=skip always_ops=run
  TR_OP_DEVIANT id=05 rc=1 expected=0 reason=operation_ran_and_observed_deviant_state
  TR_OP_SKIPPED id=06 reason=prior_sequence_mismatch
  TR_OP_CLASS id=07 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=08 kind=ssh_stdin rc=1 expect_rc=0 class=not_evaluable reason=cleanup_after_unestablished_prerequisite
  TR_ADDITIONAL_MISMATCH id=08 first_mismatch=05
  TR_OP_NOT_EVALUABLE id=08 rc=1 expected=0 reason=cleanup_after_unestablished_prerequisite
  TR_OP_CLASS id=09 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=10 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=11 kind=local_bind rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=12 kind=local_bind rc=1 expect_rc=0 class=not_evaluable reason=cleanup_after_unestablished_prerequisite
  TR_ADDITIONAL_MISMATCH id=12 first_mismatch=05
  TR_OP_NOT_EVALUABLE id=12 rc=1 expected=0 reason=cleanup_after_unestablished_prerequisite
  TR_RUN_CLASS deviant=1 not_evaluable=2 precedence=deviant_outranks_not_evaluable
  TR_RUN FAIL base_run=PROBE-BASE-RUN first_mismatch=05 first_not_evaluable=08 record=C:\Users\BARSEM~1\AppData\Local\Temp\claude\C--LAB-Tradingview-LAB-CLEAN\8ec0dbac-0511-4a3e-968b-7fe9ff2eebce\scratchpad\probe_round3
  PROBE_EXIT_CODE=1

=== FIXTURE D - F1 wrong marker family on a close operation [round3] ===
  TR_OP_CLASS id=01 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=02 kind=scp_up rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=03 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=04 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=05 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=06 kind=tcp_probe rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=07 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=08 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=09 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=10 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=11 kind=local_bind rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=12 kind=local_bind rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_RUN_CLASS deviant=0 not_evaluable=0 precedence=deviant_outranks_not_evaluable
  TR_RUN PASS base_run=PROBE-BASE-RUN record=C:\Users\BARSEM~1\AppData\Local\Temp\claude\C--LAB-Tradingview-LAB-CLEAN\8ec0dbac-0511-4a3e-968b-7fe9ff2eebce\scratchpad\probe_round3
  PROBE_EXIT_CODE=0
```

## R4-3. `_r4_runner_probe.ps1` - round 4 (GREEN)

```text
RUNNER path=C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\transport_runner.ps1
RUNNER sha256=45123de489ec48dfe7d4318dad7db547bcc03114fe886be16c7f4c616fc45fed
VARIANT round4
=== FIXTURE A - F4 decisive: independent RO close FAIL after unrelated P0 close STOP [round4] ===
  TR_OP_CLASS id=01 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=02 kind=scp_up rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=03 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=04 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=05 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=06 kind=tcp_probe rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_PREREQ_STATE id=07 established=True any_deviant=False prerequisites=[04=match]
  TR_OP_CLASS id=07 kind=ssh_stdin rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_FIRST_MISMATCH id=07 rc=3 expected=0 class=not_evaluable later_sequence_ops=skip always_ops=run
  TR_OP_NOT_EVALUABLE id=07 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_PREREQ_STATE id=08 established=True any_deviant=False prerequisites=[05=match]
  TR_OP_CLASS id=08 kind=ssh_stdin rc=1 expect_rc=0 class=deviant reason=operation_ran_and_observed_deviant_state
  TR_ADDITIONAL_MISMATCH id=08 first_mismatch=07
  TR_OP_DEVIANT id=08 rc=1 expected=0 reason=operation_ran_and_observed_deviant_state
  TR_OP_PREREQ_STATE id=09 established=False any_deviant=False prerequisites=[07=not_evaluable]
  TR_OP_CLASS id=09 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_PREREQ_STATE id=10 established=False any_deviant=True prerequisites=[08=deviant]
  TR_OP_CLASS id=10 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_PREREQ_STATE id=11 established=False any_deviant=False prerequisites=[07=not_evaluable,09=match]
  TR_OP_CLASS id=11 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_ADDITIONAL_MISMATCH id=11 first_mismatch=07
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_PREREQ_STATE id=12 established=False any_deviant=True prerequisites=[08=deviant,10=match]
  TR_OP_CLASS id=12 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_ADDITIONAL_MISMATCH id=12 first_mismatch=07
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0 reason=operation_reported_stop
  TR_RUN_CLASS deviant=1 not_evaluable=3 precedence=deviant_outranks_not_evaluable
  TR_RUN FAIL base_run=PROBE-BASE-RUN first_mismatch=07 first_not_evaluable=07 record=C:\Users\BARSEM~1\AppData\Local\Temp\claude\C--LAB-Tradingview-LAB-CLEAN\8ec0dbac-0511-4a3e-968b-7fe9ff2eebce\scratchpad\probe_round4
  PROBE_EXIT_CODE=1

=== FIXTURE B - genuinely unestablished prerequisite stays not-evaluable [round4] ===
  TR_OP_CLASS id=01 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=02 kind=scp_up rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=03 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=04 kind=ssh_stdin rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_FIRST_MISMATCH id=04 rc=3 expected=0 class=not_evaluable later_sequence_ops=skip always_ops=run
  TR_OP_NOT_EVALUABLE id=04 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_SKIPPED id=05 reason=prior_sequence_mismatch
  TR_OP_SKIPPED id=06 reason=prior_sequence_mismatch
  TR_OP_PREREQ_STATE id=07 established=False any_deviant=False prerequisites=[04=not_evaluable]
  TR_OP_CLASS id=07 kind=ssh_stdin rc=1 expect_rc=0 class=not_evaluable reason=cleanup_after_unestablished_prerequisite prerequisites=[04=not_evaluable]
  TR_ADDITIONAL_MISMATCH id=07 first_mismatch=04
  TR_OP_NOT_EVALUABLE id=07 rc=1 expected=0 reason=cleanup_after_unestablished_prerequisite prerequisites=[04=not_evaluable]
  TR_OP_PREREQ_STATE id=08 established=False any_deviant=False prerequisites=[05=skipped]
  TR_OP_CLASS id=08 kind=ssh_stdin rc=1 expect_rc=0 class=not_evaluable reason=cleanup_after_unestablished_prerequisite prerequisites=[05=skipped]
  TR_ADDITIONAL_MISMATCH id=08 first_mismatch=04
  TR_OP_NOT_EVALUABLE id=08 rc=1 expected=0 reason=cleanup_after_unestablished_prerequisite prerequisites=[05=skipped]
  TR_OP_PREREQ_STATE id=09 established=False any_deviant=False prerequisites=[07=not_evaluable]
  TR_OP_CLASS id=09 kind=scp_down rc=1 expect_rc=0 class=not_evaluable reason=scp_transfer_did_not_complete
  TR_ADDITIONAL_MISMATCH id=09 first_mismatch=04
  TR_OP_NOT_EVALUABLE id=09 rc=1 expected=0 reason=scp_transfer_did_not_complete
  TR_OP_PREREQ_STATE id=10 established=False any_deviant=False prerequisites=[08=not_evaluable]
  TR_OP_CLASS id=10 kind=scp_down rc=1 expect_rc=0 class=not_evaluable reason=scp_transfer_did_not_complete
  TR_ADDITIONAL_MISMATCH id=10 first_mismatch=04
  TR_OP_NOT_EVALUABLE id=10 rc=1 expected=0 reason=scp_transfer_did_not_complete
  TR_OP_PREREQ_STATE id=11 established=False any_deviant=False prerequisites=[07=not_evaluable,09=not_evaluable]
  TR_OP_CLASS id=11 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_ADDITIONAL_MISMATCH id=11 first_mismatch=04
  TR_OP_NOT_EVALUABLE id=11 rc=3 expected=0 reason=operation_reported_stop
  TR_OP_PREREQ_STATE id=12 established=False any_deviant=False prerequisites=[08=not_evaluable,10=not_evaluable]
  TR_OP_CLASS id=12 kind=local_bind rc=3 expect_rc=0 class=not_evaluable reason=operation_reported_stop
  TR_ADDITIONAL_MISMATCH id=12 first_mismatch=04
  TR_OP_NOT_EVALUABLE id=12 rc=3 expected=0 reason=operation_reported_stop
  TR_RUN_CLASS deviant=0 not_evaluable=7 precedence=deviant_outranks_not_evaluable
  TR_RUN STOP base_run=PROBE-BASE-RUN first_mismatch=04 first_not_evaluable=04 record=C:\Users\BARSEM~1\AppData\Local\Temp\claude\C--LAB-Tradingview-LAB-CLEAN\8ec0dbac-0511-4a3e-968b-7fe9ff2eebce\scratchpad\probe_round4
  PROBE_EXIT_CODE=3

=== FIXTURE C - cleanup after an earlier deviation on its own branch [round4] ===
  TR_OP_CLASS id=01 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=02 kind=scp_up rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=03 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=04 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=05 kind=ssh_stdin rc=1 expect_rc=0 class=deviant reason=operation_ran_and_observed_deviant_state
  TR_FIRST_MISMATCH id=05 rc=1 expected=0 class=deviant later_sequence_ops=skip always_ops=run
  TR_OP_DEVIANT id=05 rc=1 expected=0 reason=operation_ran_and_observed_deviant_state
  TR_OP_SKIPPED id=06 reason=prior_sequence_mismatch
  TR_OP_PREREQ_STATE id=07 established=True any_deviant=False prerequisites=[04=match]
  TR_OP_CLASS id=07 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_PREREQ_STATE id=08 established=False any_deviant=True prerequisites=[05=deviant]
  TR_OP_CLASS id=08 kind=ssh_stdin rc=1 expect_rc=0 class=not_evaluable reason=cleanup_after_earlier_deviation prerequisites=[05=deviant]
  TR_ADDITIONAL_MISMATCH id=08 first_mismatch=05
  TR_OP_NOT_EVALUABLE id=08 rc=1 expected=0 reason=cleanup_after_earlier_deviation prerequisites=[05=deviant]
  TR_OP_PREREQ_STATE id=09 established=True any_deviant=False prerequisites=[07=match]
  TR_OP_CLASS id=09 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_PREREQ_STATE id=10 established=False any_deviant=False prerequisites=[08=not_evaluable]
  TR_OP_CLASS id=10 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_PREREQ_STATE id=11 established=True any_deviant=False prerequisites=[07=match,09=match]
  TR_OP_CLASS id=11 kind=local_bind rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_PREREQ_STATE id=12 established=False any_deviant=False prerequisites=[08=not_evaluable,10=match]
  TR_OP_CLASS id=12 kind=local_bind rc=1 expect_rc=0 class=not_evaluable reason=cleanup_after_unestablished_prerequisite prerequisites=[08=not_evaluable,10=match]
  TR_ADDITIONAL_MISMATCH id=12 first_mismatch=05
  TR_OP_NOT_EVALUABLE id=12 rc=1 expected=0 reason=cleanup_after_unestablished_prerequisite prerequisites=[08=not_evaluable,10=match]
  TR_RUN_CLASS deviant=1 not_evaluable=2 precedence=deviant_outranks_not_evaluable
  TR_RUN FAIL base_run=PROBE-BASE-RUN first_mismatch=05 first_not_evaluable=08 record=C:\Users\BARSEM~1\AppData\Local\Temp\claude\C--LAB-Tradingview-LAB-CLEAN\8ec0dbac-0511-4a3e-968b-7fe9ff2eebce\scratchpad\probe_round4
  PROBE_EXIT_CODE=1

=== FIXTURE D - F1 wrong marker family on a close operation [round4] ===
  TR_OP_CLASS id=01 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=02 kind=scp_up rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=03 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=04 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=05 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_CLASS id=06 kind=tcp_probe rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_PREREQ_STATE id=07 established=True any_deviant=False prerequisites=[04=match]
  TR_OP_CLASS id=07 kind=ssh_stdin rc=0 expect_rc=0 class=not_evaluable reason=no_remote_program_marker_in_capture expected_family=remote_close_tree_wpi.sh
  TR_FIRST_MISMATCH id=07 rc=0 expected=0 class=not_evaluable later_sequence_ops=skip always_ops=run
  TR_OP_NOT_EVALUABLE id=07 rc=0 expected=0 reason=no_remote_program_marker_in_capture expected_family=remote_close_tree_wpi.sh
  TR_OP_PREREQ_STATE id=08 established=True any_deviant=False prerequisites=[05=match]
  TR_OP_CLASS id=08 kind=ssh_stdin rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_PREREQ_STATE id=09 established=False any_deviant=False prerequisites=[07=not_evaluable]
  TR_OP_CLASS id=09 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_PREREQ_STATE id=10 established=True any_deviant=False prerequisites=[08=match]
  TR_OP_CLASS id=10 kind=scp_down rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_PREREQ_STATE id=11 established=False any_deviant=False prerequisites=[07=not_evaluable,09=match]
  TR_OP_CLASS id=11 kind=local_bind rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_OP_PREREQ_STATE id=12 established=True any_deviant=False prerequisites=[08=match,10=match]
  TR_OP_CLASS id=12 kind=local_bind rc=0 expect_rc=0 class=match reason=preregistered_rc
  TR_RUN_CLASS deviant=0 not_evaluable=1 precedence=deviant_outranks_not_evaluable
  TR_RUN STOP base_run=PROBE-BASE-RUN first_mismatch=07 first_not_evaluable=07 record=C:\Users\BARSEM~1\AppData\Local\Temp\claude\C--LAB-Tradingview-LAB-CLEAN\8ec0dbac-0511-4a3e-968b-7fe9ff2eebce\scratchpad\probe_round4
  PROBE_EXIT_CODE=3
```

## R4-4. `_r4_wsl_fixtures.sh` - the delivered shell bytes on a real Linux kernel

```text

########## FIXTURE ENVIRONMENT
$ uname -sr; id -u; id -g
Linux 6.18.33.2-microsoft-standard-WSL2
0
0
$ ls -l /usr/bin/bash /usr/bin/stat /usr/bin/env
-rwxr-xr-x 1 root root 1540520 Feb 13 14:16 /usr/bin/bash
lrwxrwxrwx 1 root root      30 Mar 30 19:50 /usr/bin/env -> ../lib/cargo/bin/coreutils/env
lrwxrwxrwx 1 root root      31 Mar 30 19:50 /usr/bin/stat -> ../lib/cargo/bin/coreutils/stat
$ ls -l /root/wpi_r4/tools | head -4
total 89024
-rwxr-xr-x 1 root root    43592 Aug 11 13:30 cmp
-rwxr-xr-x 1 root root 11352352 Aug 11 13:30 env
-rwxr-xr-x 1 root root   216632 Aug 11 13:30 find
superseded_selfstop_lines_deleted=2

########## F2 RED - round-3 bytes, TMPDIR pointed at the evidence tree
# The accepted round-3 close script inherits TMPDIR and calls mktemp. With
# TMPDIR set to the tree it is measuring it writes and hashes its own files
# inside evidence while printing wrote_into_evidence_tree=0.
$ TMPDIR=$EV bash close_r3.sh $EV WPIR4-FIXTURE-P0
RC=0
--- CLOSE_DIGEST lines (note the tmp.* member inside the evidence tree):
CLOSE_DIGEST b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060  a.txt
CLOSE_DIGEST f2c82decdd7181cf98945929a62598db7e6b477e11f6e0eb0ae97020eff151ad  b.txt
CLOSE_DIGEST a22098326ecf89256b460105223d67c696c557096bc5e3afc6d83de2328949a4  tmp.eYE6juigfb/raw.0
CLOSE PASS runid=WPIR4-FIXTURE-P0 dir=/root/wpi_r4/f2red/evidence/runkit/WPIR4-FIXTURE-P0 files=3 wrote_into_evidence_tree=0
--- stderr:

########## F2 GREEN - round-4 bytes, same TMPDIR injection
# TMPDIR is not an entry the frozen launch domain delivers, so the class 5
# sweep refuses it by name before any external program runs. Independently,
# the round-4 bytes contain no mktemp at all.
$ env -i PATH=... LC_ALL=C HOME=... TMPDIR=$EV /usr/bin/bash --noprofile --norc close_r4.sh $EV WPIR4-FIXTURE-P0 $WORK
RC=3
CLOSE_STOP reason=launch_domain_unexpected_environment_entry name=[TMPDIR]
$ grep -cE '^[^#]*mktemp' close_r4.sh ; grep -cE '^[^#]*mktemp' close_r3.sh   # code lines only
round4_mktemp_code_lines=0
round3_mktemp_code_lines=1

########## F2/T6 GREEN - clean run under the frozen launch domain and plan argv
$ env -i ... /usr/bin/bash --noprofile --norc close_r4.sh /root/wpi_r4/clean/evidence/runkit/WPIR4-FIXTURE-P0 WPIR4-FIXTURE-P0 /root/wpi_r4/clean/work
RC=0
CLOSE_NOTE launch_domain interpreter=/usr/bin/bash path=/usr/bin:/bin lc_all=C home=/root exec_environment_entries=3 inherited_functions=0 bash_env=absent env=absent tmpdir=absent attestation=builtins_and_proc_self_environ
CLOSE_NOTE work_root_ok path=/root/wpi_r4/clean/work owner_numeric=0:0 owner_rendered=root:root mode=700 allocator=op_01_remote_setup_wpi.sh
CLOSE_NOTE scratch work_dir=/root/wpi_r4/clean/work/close_work_WPIR4-FIXTURE-P0 owner_numeric=0:0 mode=700 created=once tmpdir=run_owned canonical_non_overlap=proven_before_and_after_create removal=adjudicated_on_every_exit_path
CLOSE_NOTE evidence_files count=2
CLOSE_NOTE digest_set_stable passes=2
CLOSE_BINDING runid=WPIR4-FIXTURE-P0 dir=/root/wpi_r4/clean/evidence/runkit/WPIR4-FIXTURE-P0 files=2
CLOSE_DIGEST b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060  a.txt
CLOSE_DIGEST f2c82decdd7181cf98945929a62598db7e6b477e11f6e0eb0ae97020eff151ad  b.txt
CLOSE PASS runid=WPIR4-FIXTURE-P0 dir=/root/wpi_r4/clean/evidence/runkit/WPIR4-FIXTURE-P0 files=2 wrote_into_evidence_tree=0
--- stderr:
--- the evidence tree after the run (no scratch residue, no new member):
/root/wpi_r4/clean/evidence/runkit/WPIR4-FIXTURE-P0
/root/wpi_r4/clean/evidence/runkit/WPIR4-FIXTURE-P0/a.txt
/root/wpi_r4/clean/evidence/runkit/WPIR4-FIXTURE-P0/b.txt
--- the work root after the run (the run-owned work directory was removed):
/root/wpi_r4/clean/work

########## F3 RED - round-3 bytes, mixed ENOENT+EACCES probe diagnostic
# A stat wrapper that answers the evidence-directory probe with a combined
# diagnostic. Round 3 substring-matches "No such file or directory" and
# reports a completed observation of MISSING EVIDENCE at rc 1.
$ bash close_r3_mixed.sh $EV WPIR4-FIXTURE-P0
RC=1
CLOSE_FAIL reason=evidence_dir_absent path=/root/wpi_r4/f3/evidence/runkit/WPIR4-FIXTURE-P0

########## F3 GREEN - round-4 bytes, same mixed diagnostic
# The absence template is calibrated once from this run own pinned stat and
# compared as a whole string, corroborated by the kernel. A mixed diagnostic
# is an inability to evaluate: CLOSE_STOP at rc 3.
$ env -i ... close_r4_mixed.sh $EV WPIR4-FIXTURE-P0 $WORK
RC=3
CLOSE_STOP reason=path_probe_error path=/root/wpi_r4/f3/evidence/runkit/WPIR4-FIXTURE-P0 rc=1 detail=/root/wpi_r4/f3/evidence/runkit/WPIR4-FIXTURE-P0: No such file or directory; Permission denied

########## F1 RED - a fake bash first on PATH under the round-3 launch (bare `bash -s --`)
$ PATH=$FIX/plant:$PATH bash -s -- <EV_DIR> <RUNID>   # the round-3 plan argv
PATH_RC=0
PATH_HIT=yes
CLOSE PASS runid=WPIR4-FIXTURE-P0 dir=/forged files=2 wrote_into_evidence_tree=0

########## F1 RED - inherited BASH_ENV under an absolute interpreter, no env -i
$ BASH_ENV=$FIX/plant/startup.sh /usr/bin/bash -s -- <EV_DIR> <RUNID>
BASH_ENV_RC=0
BASH_ENV_HIT=yes
CLOSE PASS runid=WPIR4-FIXTURE-P0 dir=/forged files=2 wrote_into_evidence_tree=0

########## F1 GREEN - the frozen launch domain neutralises both plants
$ the frozen argv, with the plant still first on the OUTER PATH and BASH_ENV still set
RC=0
PATH_HIT=no STARTUP_HIT=no
CLOSE_NOTE launch_domain interpreter=/usr/bin/bash path=/usr/bin:/bin lc_all=C home=/root exec_environment_entries=3 inherited_functions=0 bash_env=absent env=absent tmpdir=absent attestation=builtins_and_proc_self_environ
CLOSE PASS runid=WPIR4-FIXTURE-P0 dir=/root/wpi_r4/f1/evidence/runkit/WPIR4-FIXTURE-P0 files=2 wrote_into_evidence_tree=0

########## F1 RESIDUAL - a launch domain that CARRIES BASH_ENV, with an exiting plant
# MEASURED LIMIT, not a repair. bash reads $BASH_ENV before the first byte
# of the delivered script; --norc/--noprofile do not disable that channel.
# A startup plant that exits therefore forges the record before any
# in-script attestation can run. NOTHING inside a stdin-delivered script
# can close this - it is closed on the plan/runner side, by env -i with an
# explicit complete variable list that the runner enforces verbatim, so no
# plan row can introduce BASH_ENV at all. This case is unreachable from the
# frozen plan; it is recorded because the claim must be scoped honestly.
$ env -i PATH=... LC_ALL=C HOME=... BASH_ENV=<exiting plant> /usr/bin/bash --noprofile --norc close_r4.sh ...
CLOSE PASS runid=WPIR4-FIXTURE-P0 dir=/forged files=2 wrote_into_evidence_tree=0
RC=0

########## F1 GREEN - a launch domain that carries BASH_ENV, with a NON-exiting plant
# The stealthier plant - one that mutates state and lets the delivered
# script run so the real record is produced - IS refused: BASH_ENV is still
# in the exec environment the kernel recorded, and the class 5 sweep names
# it. Only the plant that destroys the run outright escapes the sweep, and
# it destroys the very output it was trying to forge into.
$ env -i PATH=... LC_ALL=C HOME=... BASH_ENV=<non-exiting plant> ... close_r4.sh ...
CLOSE_STOP reason=launch_domain_unexpected_environment_entry name=[BASH_ENV]
RC=3
QUIET_PLANT_HIT=yes

########## F1 GREEN - the same script refuses an inherited exported shell function
$ env -i ... BASH_FUNC_a_plant%%=() { :; } /usr/bin/bash --noprofile --norc close_r4.sh ...
CLOSE_STOP reason=launch_domain_inherited_shell_function detail=[declare -fx a_plant]
RC=3

########## T6 - the superseded cf049b6b close script under its own clean launch
# The addendum records this edit as SUPERSEDED. Driven exactly as its own
# header prescribes, it refuses its own clean execution.
$ env -i ... /usr/bin/bash --noprofile --norc close_super.sh <EV_DIR> <RUNID> <WORK_ROOT>
CLOSE_STOP reason=launch_domain_inherited_shell_function
RC=3

########## T6 - argv arity: two arguments against a three-argument contract
# The superseded edit called fail() for a wrong argument count, so an
# operator-side composition error arrived at the runner as a HOST deviation
# at rc 1. The round-4 bytes classify it as an inability to evaluate.
$ close_super.sh <EV_DIR> <RUNID>    (no work root)
CLOSE_FAIL reason=usage remote_close_tree_wpi.sh <EV_DIR> <RUNID> <WORK_ROOT> argc=2
RC=1
$ close_r4.sh <EV_DIR> <RUNID>       (no work root)
CLOSE_STOP reason=argv_count=2 expected=3 usage=remote_close_tree_wpi.sh_EV_DIR_RUNID_WORK_ROOT detail=operator_side_composition_input_not_a_host_observation
RC=3

########## F2/class 6 - a work root inside the evidence tree is refused before mkdir
$ close_r4.sh <EV_DIR> <RUNID> <EV_DIR>/inner
CLOSE_STOP reason=work_dir_inside_evidence_tree phase=before_create path=/root/wpi_r4/overlap/evidence/runkit/WPIR4-FIXTURE-P0/inner/close_work_WPIR4-FIXTURE-P0 evidence=/root/wpi_r4/overlap/evidence/runkit/WPIR4-FIXTURE-P0
RC=3
--- the evidence tree is unchanged (no work directory was created in it):
/root/wpi_r4/overlap/evidence/runkit/WPIR4-FIXTURE-P0
/root/wpi_r4/overlap/evidence/runkit/WPIR4-FIXTURE-P0/a.txt
/root/wpi_r4/overlap/evidence/runkit/WPIR4-FIXTURE-P0/b.txt
/root/wpi_r4/overlap/evidence/runkit/WPIR4-FIXTURE-P0/inner

########## T6 - op 01 allocates the work root the plan passes to ops 07/08
# Two further FIXTURE-ONLY retargetings are declared here, because op 01 is
# path- and mount-bound to the real host: EXPECT_PREFIX/EXPECT_PARENT are
# moved under $FIX, and EXPECT_PARENT_MOUNT is filled from the projection
# this kernel reports. Filling that pin from an observation would be
# ILLEGITIMATE in production - the value is a deploy-channel attestation
# (owner grant #6) and must never be learned from the session under test -
# so this step proves the allocation shape ONLY, not the mount binding.
# Pass 1 carries a grammar-valid DECOY projection, because the unfilled-pin
# gate runs before the projection is taken; the STOP then reports what this
# kernel actually projects.
$ setup_fix.sh <BASE>   # first pass: decoy mount pin
RC=3
SETUP_STOP reason=parent_mount_differs path=/root/wpi_r4/alloc observed=[device=8:48 root=/ mount_point=/ fstype=ext4 source=/dev/sdd shared_mount_point_records=1] attested=[device=0:0 root=/decoy mount_point=/decoy fstype=decoy source=decoy shared_mount_point_records=1]
OBSERVED_PROJECTION=[device=8:48 root=/ mount_point=/ fstype=ext4 source=/dev/sdd shared_mount_point_records=1]
--- nothing was created by the refused pass (STOP precedes the first mkdir):
$ setup_fix2.sh <BASE>  # second pass: mount pin filled from the first pass
RC=0
SETUP_NOTE launch_domain interpreter=/usr/bin/bash path=/usr/bin:/bin lc_all=C home=/root exec_environment_entries=3 inherited_functions=0 bash_env=absent env=absent tmpdir=absent attestation=builtins_and_proc_self_environ
SETUP_NOTE allocated path=/root/wpi_r4/alloc/wpi_staging_FIXTURE
SETUP_NOTE allocated path=/root/wpi_r4/alloc/wpi_staging_FIXTURE/evidence
SETUP_NOTE allocated path=/root/wpi_r4/alloc/wpi_staging_FIXTURE/evidence/runkit
SETUP_NOTE allocated path=/root/wpi_r4/alloc/wpi_staging_FIXTURE/kit
SETUP_NOTE allocated path=/root/wpi_r4/alloc/wpi_staging_FIXTURE/work
SETUP_NOTE work_root_allocated path=/root/wpi_r4/alloc/wpi_staging_FIXTURE/work consumer=ops_07_08_remote_close_tree_wpi.sh disjoint_from=/root/wpi_r4/alloc/wpi_staging_FIXTURE/evidence
SETUP PASS base=/root/wpi_r4/alloc/wpi_staging_FIXTURE evidence=/root/wpi_r4/alloc/wpi_staging_FIXTURE/evidence runkit=/root/wpi_r4/alloc/wpi_staging_FIXTURE/evidence/runkit kit=/root/wpi_r4/alloc/wpi_staging_FIXTURE/kit work=/root/wpi_r4/alloc/wpi_staging_FIXTURE/work owner_numeric=0:0 owner_name=gatea:gatea mode=700
--- what op 01 actually created:
/root/wpi_r4/alloc/wpi_staging_FIXTURE
/root/wpi_r4/alloc/wpi_staging_FIXTURE/evidence
/root/wpi_r4/alloc/wpi_staging_FIXTURE/evidence/runkit
/root/wpi_r4/alloc/wpi_staging_FIXTURE/kit
/root/wpi_r4/alloc/wpi_staging_FIXTURE/work

########## T6 - the allocated work root is exactly what the plan passes to ops 07/08
$ close_r4.sh <BASE>/evidence/runkit/<RUNID> <RUNID> <BASE>/work
RC=0
CLOSE_NOTE work_root_ok path=/root/wpi_r4/alloc/wpi_staging_FIXTURE/work owner_numeric=0:0 owner_rendered=root:root mode=700 allocator=op_01_remote_setup_wpi.sh
CLOSE_NOTE scratch work_dir=/root/wpi_r4/alloc/wpi_staging_FIXTURE/work/close_work_WPIR4-FIXTURE-P0 owner_numeric=0:0 mode=700 created=once tmpdir=run_owned canonical_non_overlap=proven_before_and_after_create removal=adjudicated_on_every_exit_path
CLOSE PASS runid=WPIR4-FIXTURE-P0 dir=/root/wpi_r4/alloc/wpi_staging_FIXTURE/evidence/runkit/WPIR4-FIXTURE-P0 files=1 wrote_into_evidence_tree=0
--- the plan row the runner will send (argv tail after the launch domain):
/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>/evidence/runkit/<ALLOCATE-AT-DISPATCH>-P0 <ALLOCATE-AT-DISPATCH>-P0 /home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>/work
```

### The one residual this section measures rather than repairs

> **WITHDRAWN IN ROUND 5 (Codex round-4 Band B).** The paragraph below is kept
> verbatim as the record of what round 4 claimed, and is **struck**: its
> conclusion — that the residual is *unreachable from the frozen plan* and that
> F1 is therefore closed on the composition — is FALSE. The plan is not the only
> way a startup variable can reach the transport: `sshd` hands the remote command
> string to the account's shell, and that shell processes its own startup
> environment before the string's first token runs, so no plan row is needed. F1
> is **OPEN**: inner child closed, outer SSH account-shell boundary open. The
> corrected statement and its executed reproduction are in **§R5-2**. Everything
> the paragraph says about the *inner* child, and the `F1 GREEN` block that
> follows it, remain true and are unaffected.
>
> **Two other places carry the same withdrawn claim as a literal record and were
> deliberately NOT edited**, because editing them would make a transcript disagree
> with the bytes that produced it: the `F1 RESIDUAL` commentary inside the §R4-4
> transcript above (it is the harness's own stdout), and the `echo` lines at
> `_r4_wsl_fixtures.sh:210-222` that emitted it. That harness is round 4's, is
> frozen as evidence, and is superseded for this claim by `_r5_wsl_fixtures.sh`.
> Read both through this withdrawal.

~~The block titled `F1 RESIDUAL` is a **measured limit, recorded because the claim
has to be scoped honestly**. `bash` reads `$BASH_ENV` before the first byte of a
stdin-delivered script, and `--norc`/`--noprofile` do not disable that channel, so
a startup plant that EXITS forges the record before any in-script attestation can
run. Nothing inside a delivered script can close this. It is closed on the
operator side: the runner freezes `$REMOTE_LAUNCH_DOMAIN` and refuses any plan row
that does not carry it verbatim, and that domain is `env -i` with an explicit,
complete variable list - so no plan row can introduce `BASH_ENV` at all. The case
in the transcript is therefore unreachable from the frozen plan, and it is the
reason the domain is stated and enforced on both sides rather than only inside the
scripts.~~ The stealthier plant - the one that lets the script run, and so is the
only kind that could forge a REAL-looking record - is refused by the class 5 sweep
at rc 3, which the block after it shows. **That last sentence stands; the struck
text does not.**

## R4-5. `_r4_t5_compose.sh` - the `run_p0.sh` -> `RP6-P0.sh` composition

```text

########## A. probe stubs standing in for the three sourced artifacts
total 12
-rw-r--r-- 1 root root  72 Aug 11 13:30 RP0-BOOTSTRAP.sh
-rw-r--r-- 1 root root  20 Aug 11 13:30 RP0-LIB.sh
-rw-r--r-- 1 root root 209 Aug 11 13:30 RP6-P0.sh

########## A-RED. round-3 wrapper: which P0_* names reach the block?
$ env -i ... /usr/bin/bash --noprofile --norc run_p0_r3.sh
RC=0
P0W_PROBE sourced_with_P0_names=6
P0W done runid=T5FIXTURE-P0
--- P0_* environment the round-3 wrapper handed to the block:
  P0_EXPECT_UID=1001
  P0_FORBIDDEN_GIDS=0 988
  P0_STATE_GID=988
  P0_STATE_UID=999
  P0_TOOL_PINS=placeholder
  P0_VENV_ROOT=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b
P0_ATTESTED_names_exported=0

########## A-GREEN. round-4 wrapper, deploy-channel values present
$ env -i ... /usr/bin/bash --noprofile --norc run_p0_r4.sh
RC=0
P0W_launch_domain interpreter=/usr/bin/bash path=/usr/bin:/bin lc_all=C home=/root exec_environment_entries=3 inherited_functions=0 bash_env=absent env=absent tmpdir=absent attestation=builtins_and_proc_self_environ
P0W_attested_inputs user_ns=user:[4026531837] mnt_ns=mnt:[4026531841] pid_ns=pid:[4026531836] net_ns=net:[4026531840] root_mount_id=2049:2 origin=deploy_channel_grant_6_never_learned_from_this_login
P0W_PROBE sourced_with_P0_names=11
P0W done runid=T5FIXTURE-P0
--- P0_* environment the round-4 wrapper handed to the block:
  P0_ATTESTED_MNT_NS=mnt:[4026531841]
  P0_ATTESTED_NET_NS=net:[4026531840]
  P0_ATTESTED_PID_NS=pid:[4026531836]
  P0_ATTESTED_ROOT_MOUNT_ID=2049:2
  P0_ATTESTED_USER_NS=user:[4026531837]
  P0_EXPECT_UID=1001
  P0_FORBIDDEN_GIDS=0 988
  P0_STATE_GID=988
  P0_STATE_UID=999
  P0_TOOL_PINS=placeholder
  P0_VENV_ROOT=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b
P0_ATTESTED_names_exported=5

########## B. the REAL RP6-P0.sh row-8 gate, extracted verbatim
BLOCK path=/mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6-P0.sh sha256=a090ae736cbecd9973e8ae948b052504b21cbe8b61602f4b5ac592394fad0617
GATE_REGION lines=683-744
FIXED_LITERAL_LINES=266,267,268,269,270,
GATE_EXTRACT sha256=c0cf53b14b90342f903c2b433655e3b3d92729689476d73854900ccb9c8be866 bytes=4362

########## B-RED. the real gate, driven with the round-3 wrapper environment

$ env -i P0_ATTESTED_*=... bash gate.sh   # round-3: no P0_ATTESTED_* exported
P0_STOP reason=execution_domain_unattested field=user_namespace detail=preregistered_value_missing
RC=3

########## B-GREEN. the real gate, driven with the round-4 wrapper environment

$ env -i P0_ATTESTED_*=... bash gate.sh   # round-4: five values exported
P0_STOP reason=execution_domain_unattested field=user_namespace detail=freeze_pin_unfilled
RC=3
# The frozen P0_FIXED_ATTESTED_* literals in the block are still
# <PIN-AT-FREEZE>, so the gate now reaches the freeze-pin arm instead of
# the missing-input arm. That is the correct draft-stage state: the block
# side is a Stage-1 fill, not a wrapper defect. The next case fills both.

########## B-GREEN2. both sides filled - the gate passes end to end

$ env -i P0_ATTESTED_*=... bash gate.sh   # round-4 environment, block literals filled to match
P0_GATE_PASSED all_five_attested_inputs_accepted
RC=0

$ env -i P0_ATTESTED_*=... bash gate.sh   # round-3 environment, block literals filled: still missing input
P0_STOP reason=execution_domain_unattested field=user_namespace detail=preregistered_value_missing
RC=3

########## B-GREEN3. a wrapper value that disagrees with the frozen literal

$ env -i P0_ATTESTED_*=... bash gate.sh   # one value differs from the frozen pin
P0_STOP reason=execution_domain_unattested field=pid_namespace detail=prelude_value_differs_from_frozen_pin
RC=3
```

## R4-6. Static gates

```text
########## bash -n on every delivered shell file
$ bash -n remote_setup_wpi.sh ; echo rc=$?
rc=0
$ bash -n remote_extract_verify_wpi.sh ; echo rc=$?
rc=0
$ bash -n remote_close_tree_wpi.sh ; echo rc=$?
rc=0
$ bash -n run_p0.sh ; echo rc=$?
rc=0
$ bash -n run_ro.sh ; echo rc=$?
rc=0

########## per-file identity, marker census and byte-counted CR check
FILE                              BYTES  SHA256                                                           ALOC  PIN  CR NONASCII
run_p0.sh                         12063  6646770f6884dc3e918e87c65f4c097af25b71e2612f67165662825d58709202    6    8   0        0
run_ro.sh                         11925  9ab8fa715f553f743bd23c2d177842d5c32c0c2bf074c9564861f0506f55cf12    6    4   0        0
transport_runner.ps1              69932  45123de489ec48dfe7d4318dad7db547bcc03114fe886be16c7f4c616fc45fed    3    7   0        0
TRANSPORT_PLAN.tsv                 7970  e3c11218a9c70ef5454d8db25c7c9965ebed3ae07bc97a766240429685c50e3c   22    7   0        0
remote_setup_wpi.sh               24938  2176448e710511ca0a7fa0b01c0c630012f0281691b36bf2b8c7bfe49531d8f4    0    3   0       15
remote_extract_verify_wpi.sh      22047  fa57065b85b45fb652d7ef31f4fbc6a13970b7fed763d309daedb8df18323e41    0    7   0       15
remote_close_tree_wpi.sh          28756  29b6412a466c10854ddf09effc8d5216317738a012235ce563c9764a9e0c40ef    0    2   0        4

$ # census over the seven executable/plan targets only (round 3 was 36 alloc / 33 pin)
ALLOCATE-AT-DISPATCH=37  PIN-AT-FREEZE=38
$ grep -c "UNFILLED_MARKERS = @((" transport_runner.ps1   # the guard is composed, not a literal
1
$ # no marker literal may sit on a COMMENT line of a delivered shell file
remote_setup_wpi.sh              comment_line_markers=0
remote_extract_verify_wpi.sh     comment_line_markers=0
remote_close_tree_wpi.sh         comment_line_markers=0
run_p0.sh                        comment_line_markers=0
run_ro.sh                        comment_line_markers=0

########## T7 - the inert pin no longer exists as an assignment or an export
$ grep -cE "^[[:space:]]*WPI_INTERPRETER_TARGET=" run_ro.sh
0
$ grep -cE "^[[:space:]]*export[[:space:]].*WPI_INTERPRETER_TARGET" run_ro.sh
0
$ grep -n "WPI_INTERPRETER_TARGET" run_ro.sh   # what remains is the removal note only
124:# defined `WPI_INTERPRETER_TARGET` as a freeze pin here and exported it. The
$ grep -c "WPI_INTERPRETER_TARGET" RP7-WPI-RO.sh   # the accepted block never read it
0
$ grep -n "WPI_INTERPRETER_TARGET" ../WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md
199:`WPI_INTERPRETER_TARGET` is deliberately **absent** from this table and from
$ grep -n "wpi_assert_interpreter()" RP7-WPI-RO.sh   # the predicate that actually exists
979:wpi_assert_interpreter() {

########## plan structure and launch-domain composition
$ awk -F TAB "{print NR": fields="NF}" TRANSPORT_PLAN.tsv
1: fields=9 2: fields=9 3: fields=9 4: fields=9 5: fields=9 6: fields=9 7: fields=9 8: fields=9 9: fields=9 10: fields=9 11: fields=9 12: fields=9 13: fields=9 
$ grep -c "/usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C HOME=/home/gatea /usr/bin/bash --noprofile --norc -s --" TRANSPORT_PLAN.tsv
6
$ grep -c " bash -s -- " TRANSPORT_PLAN.tsv   # bare-bash launches remaining
0
0
$ awk -F TAB rows 07/08: argc and the argv tail
07 argc=45 tail=/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>/work
08 argc=45 tail=/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>/work

########## Windows PowerShell 5.1 parse of the runner
$ $PSVersionTable.PSVersion.ToString()
5.1.26100.8875
$ [System.Management.Automation.Language.Parser]::ParseFile(transport_runner.ps1, [ref]$t, [ref]$e); $e.Count
PARSE_ERRORS=0
$ # byte-counted CR check on the runner
CR_BYTES=0 BYTES=69932

########## plan/runner composition: every ssh_stdin row checked against the
########## runner's OWN frozen constants, lifted out of transport_runner.ps1
$ # constants as the runner defines them
SSH_PINNED_OPTIONS_COUNT=30 REMOTE_LAUNCH_DOMAIN_COUNT=10 SSH_TARGET=gatea@172.24.55.233
REMOTE_LAUNCH_DOMAIN=[/usr/bin/env] [-i] [PATH=/usr/bin:/bin] [LC_ALL=C] [HOME=/home/gatea] [/usr/bin/bash] [--noprofile] [--norc] [-s] [--]
op=01 stdin=PREREG:remote_setup_wpi.sh argc=43 options_verbatim=True route_ok=True launch_domain_verbatim=True script_args=1
op=03 stdin=PREREG:remote_extract_verify_wpi.sh argc=45 options_verbatim=True route_ok=True launch_domain_verbatim=True script_args=3
op=04 stdin=PREREG:run_p0.sh argc=42 options_verbatim=True route_ok=True launch_domain_verbatim=True script_args=0
op=05 stdin=PREREG:run_ro.sh argc=42 options_verbatim=True route_ok=True launch_domain_verbatim=True script_args=0
op=07 stdin=PREREG:remote_close_tree_wpi.sh argc=45 options_verbatim=True route_ok=True launch_domain_verbatim=True script_args=3
op=08 stdin=PREREG:remote_close_tree_wpi.sh argc=45 options_verbatim=True route_ok=True launch_domain_verbatim=True script_args=3
```

---

# ROUND 5 - 2026-08-11 - BA-1, BA-2, BA-3 and the F1 verdict correction

Implementer session: Claude Opus 5 xhigh (Max account), under
`KICKOFF_TRANSPORT_REPAIR_R5.md`. Inputs: the two Codex round-4 T0 audits,
`TRANSPORT_CODEX_R4_AUDIT_BAND_A_2026-08-11.md` (BA-1, BA-2, BA-3) and
`TRANSPORT_CODEX_R4_AUDIT_BAND_B_2026-08-11.md` (F1), both REQUEST_CHANGES.

**No host was contacted and no network connection was opened.** No socket of any
kind was created; no `ssh.exe`, `scp.exe` or `sshd` process was started. The
Linux fixtures run against the same local WSL2 Ubuntu kernel round 4 used
(`6.18.33.2-microsoft-standard-WSL2`, GNU Bash 5.3.9), and every path they touch
is under `/root/wpi_r5` on that local filesystem.

## R5-0. What round 5 changed, and what it did not

| Finding | Byte change | Evidence |
|---|---|---|
| **F1** (Band B) | comments only, in all five delivered scripts and `transport_runner.ps1` | verdict corrected to OPEN; the boundary reproduced locally in §R5-2 |
| **BA-1** (HIGH) | `remote_close_tree_wpi.sh` create block restructured | D026 RED/GREEN in §R5-1, on the exact pre-repair blob |
| **BA-2** (MEDIUM) | comments only, in all five delivered scripts | the claimed RED executed and falsified in §R5-3 |
| **BA-3** (MEDIUM) | none in this directory — the overstatement lives in the two draft files | §R5-4; the edits were specified in `TRANSPORT_R5_DRAFT_EDITS_PENDING.md` and **applied by the Lead in commit `37a87046`** — §R6-3 |

One harness ships beside the targets: `_r5_wsl_fixtures.sh`. It takes two
arguments — this directory (the repaired working-tree bytes) and a directory
holding the **pre-repair** close script. The pre-repair copy is not a
reconstruction: it is `git cat-file blob HEAD:…/remote_close_tree_wpi.sh`, and the
transcript prints its SHA-256 as `29b6412a466c10854ddf09effc8d5216317738a012235ce563c9764a9e0c40ef`,
which is the frozen round-4 identity named in both the round-4 report §4 and the
Band A audit.

### Declared fixture retargeting, and the declared per-arm mutations

The retargeting is identical to round 4 and is asserted rather than assumed —
`RETARGET_ANCHORS=hit_in_both_arms` in the transcript is a hard check that throws
instead of producing a false RED or GREEN: the `TOOL_*` pins except `TOOL_BASH`
are moved to regular root-owned 0755 copies under `/root/wpi_r5/tools` (this
kernel ships `/usr/bin` coreutils as symlinks, which `require_tool` correctly
refuses), `EXPECT_UID`/`EXPECT_GID` are filled with this login's numeric identity,
and `EXPECT_LAUNCH_HOME` with this login's `HOME`.

Beyond that, four instruments are declared and each is named in its own banner:

| Instrument | Behaviour |
|---|---|
| `mkdir_diag` | creates the requested directory, emits **one** diagnostic, returns **0** — BA-1's exact case |
| `mkdir_fail_clean` | creates nothing, emits a diagnostic, returns 1 |
| `mkdir_fail_dirty` | **creates** the directory, emits a diagnostic, returns 1 |
| `rm_noop` | reports success and removes nothing |

No predicate, classification, ordering or emitted record of the delivered bytes
was altered by the fixture.

## R5-1. BA-1 — the RED and the GREEN

> **ROUND-6 CORRECTION (Codex round-5 audit, R5-F2 — HIGH).** The two sentences
> struck below were **false of the harness that produced them**. Round 5's
> `_r5_wsl_fixtures.sh` ran the RED bytes from `$FIX/red_diag.sh` against
> `$FIX/red_diag`, and the GREEN bytes from `$FIX/green_diag.sh` against
> `$FIX/green_diag`, so the two arms differed in their subject pathname **and** in
> their `EV_DIR`/`WORK_ROOT` arguments, and the two recorded refusals differed in
> their `path=` field. "Same argv" and "byte-identical refusal" were therefore
> claims the published evidence did not support, whatever the code did. **The
> harness is repaired and re-run in round 6** — one subject pathname, one argument
> vector, the common tree reset between arms, only the subject bytes replaced. The
> corrected statement and the real transcript are §R6-1 and §R6-2. The repair's
> *substance* is unaffected: RED still retains the residue, GREEN still removes it,
> and the refusals are now byte-identical as whole lines.

~~The RED arm is the pre-repair blob; the GREEN arm is the repaired file; **both are
driven through the same `mkdir_diag` instrument, the same launch domain and the
same argv**, so the only variable is the delivered bytes.~~

**Corrected (round 6, executed).** The RED arm is the pre-repair blob; the GREEN arm
is the repaired file. Both are installed, in turn, at **one** subject pathname
(`/root/wpi_r5/close_subject.sh`) and launched with **one** argument vector
(`/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0 WPIR5-FIXTURE-P0
/root/wpi_r5/ba1/work`) through the same `mkdir_diag` instrument, with the common
tree reset immediately before each arm — so the only variable is the delivered
bytes. The transcript prints the pathname, the argv and the installed SHA-256 per
arm and asserts `DISTINCT_SUBJECT_ARGV_LINES=1` across all ten BA-1 arms.

| | pre-repair bytes (RED) | repaired bytes (GREEN) |
|---|---|---|
| `SCRIPT_RC` | 3 | 3 |
| refusal | `CLOSE_STOP reason=work_dir_mkdir_diagnostics path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 detail=injected_success_diagnostic` | **byte-identical** (`REFUSAL_BYTE_IDENTICAL=yes`) |
| `RESIDUE_PRESENT` | **yes** | **no** |

That reproduces Codex's Band A result (`SCRIPT_RC=3 … RESIDUE_PRESENT=yes`) on the
pre-repair bytes and removes it on the repaired bytes, while keeping the reasoned
STOP byte-for-byte.

**The carried fence was not weakened**, and the transcript proves it rather than
asserting it. The fence is `[ -z "$MKDIR_OUT" ] || stop "work_dir_mkdir_diagnostics …"`.
The predicate and the reason token are unchanged (only the line number moved,
402 → 483), and the block `BA-1 FENCE DISCRIMINATING POWER` quotes **both** the old
and the new assertion together with the refusal each produced **against the same
injected diagnostic**. Both refuse.

Five further arms bound the claim rather than widening it:

- two clean runs, one per arm, both rc 0 with the same `CLOSE PASS` and no
  residue — the happy path did not move;
- a nonzero `mkdir` that created nothing: both arms STOP, and the repaired arm
  additionally records `rc=1 object_after_failed_create=absent
  cleanup=not_armed_for_a_nonzero_create detail=[…]` where round 4 printed only
  the path;
- **the declared uncovered case** — a nonzero `mkdir` that *did* create. The
  repaired bytes deliberately do not arm cleanup there, so residue remains, and
  the record now **names** it (`object_after_failed_create=present`). A nonzero
  status is not evidence that the object at that path is the one this run
  created, and `rm -rf` on an object it cannot prove it created is the wrong
  answer. The header, the create block and the `CLOSE_NOTE scratch` field all say
  so; nothing claims coverage there;
- `rm_noop` on the newly covered path: the cleanup does **not** accept a removal
  that removed nothing — `CLOSE_STOP reason=work_dir_removal_failed`;
- a late refusal after a clean create (work-directory mode 750): both arms
  `RESIDUE_PRESENT=no`, a control showing the repair did not move an exit path
  round 4 already covered.

The `CLOSE_NOTE scratch` field changed with the code, visible side by side in the
two clean-run arms:
`removal=adjudicated_on_every_exit_path` → `removal=adjudicated_on_every_exit_path_after_a_zero_status_create`.

## R5-2. F1 — the verdict is corrected to OPEN

Round 4 wrote that the exiting-`BASH_ENV` case is *unreachable from the frozen
plan*, because the runner enforces the `env -i` domain verbatim on every plan row
and that domain's variable list is explicit and complete. Band B's finding is that
this reasons about the wrong interpreter. The runner does not execute remote
`/usr/bin/env`; it starts local `ssh.exe` and supplies a remote **command string**.
`sshd` hands that string to the account's shell, and that shell processes its own
startup environment **before** the string's first token. No plan row is involved,
so enforcing the plan row cannot close it, and no command *inside* the same shell
string can act before the shell that interprets the string.

The block `F1 OPEN - the outer account-shell boundary, reproduced locally` executes
that composition step. **Its scope is stated in the transcript before its result:
it is not closure evidence, it is not the real transport path, and no host, socket
or ssh/sshd process is involved.** It is a local model —
`BASH_ENV=<exiting plant> /usr/bin/bash -c "<the frozen command string>" < <the delivered script>` —
in which the command string is byte-identical to the frozen `$REMOTE_LAUNCH_DOMAIN`
and the delivered script is the **repaired round-5 file**. Result: `RC=0`,
`OUTER_PLANT_RAN=yes`, a forged `CLOSE PASS … wrote_into_evidence_tree=0` on
stdout, and `DELIVERED_SCRIPT_RECORD_LINES=0` — the real program never ran. The
runner would accept that capture: `$MARKER_FAMILY_BY_STDIN` registers `CLOSE_` and
`CLOSE ` for the `remote_close_tree_wpi.sh` leaf, the forged line starts with one
of them, and rc 0 is in the grammar. Marker **shape** is bound to the plan row,
not to the process that produced it.

Two controls separate what is still closed from what is not:

- **still closed** — a plant that lets the delivered script *run* (the only kind
  that could forge a *real-looking* record) is refused by name inside the child:
  `CLOSE_STOP reason=launch_domain_unexpected_environment_entry name=[BASH_ENV]`
  at rc 3, with `QUIET_PLANT_RAN=yes` confirming the plant did execute;
- **not closed** — the same exiting plant delivered *inside* the domain still
  forges at rc 0. Round 4 recorded that case and was right that the frozen plan
  cannot introduce `BASH_ENV` into the `env -i` list; what it got wrong is that
  the plan is not the only way in.

**Status wording, used identically everywhere it now appears:** *inner child
closed; outer SSH account-shell boundary open.* No client-side control was
invented. Closure requires an enforcement point that acts before account-shell
startup processing — a deploy-channel-attested forced command / execution
contract, or a transport path with no unbound shell — plus D026 evidence driven
through the real top-level path. That is a successor item. A disclosure is not a
control.

## R5-3. BA-2 — the claimed second `declare -F` defect, falsified

The round-4 report and five delivered scripts said that bare `declare -F` exits 1
when no function exists and would therefore terminate the assignment under
`set -Eeuo pipefail`. Executed on this kernel:

| arm | what it drives | result |
|---|---|---|
| A | bare `declare -F` in a function-free `--noprofile --norc` child | `DIRECT_RC=0` |
| **B** | **the unguarded assignment under `set -Eeuo pipefail` — the claimed RED** | `AFTER_ASSIGN len=0`, `STILL_RUNNING=yes`, `PROCESS_RC=0` |
| C | control: a **named** lookup of a missing function | `PROCESS_RC=1` |
| D | control: `LD_FUNCS="$(false)"` in the identical shell shape | `PROCESS_RC=1` |
| E | the delivered guarded form | `PROCESS_RC=0` |
| F | discriminating power of keeping the guard | `UNGUARDED=[declare -fx foo]` = `GUARDED=[declare -fx foo]` |
| G | the delivered script against a real inherited exported function | `CLOSE_STOP reason=launch_domain_inherited_shell_function detail=[declare -fx a_plant]` rc 3 |

Arm D is what makes arm B a falsification rather than an inactive-option artefact:
`set -e` **is** armed in that exact shell shape and does kill the process for a
genuinely failing command. The claimed RED is therefore not producible by the
command the delivered code actually runs.

**Disposition: the guard is KEPT as explicit no-op hardening and the claim is
withdrawn.** Arm F is the discriminating-power evidence for keeping it — the
guarded and unguarded forms list an inherited exported function identically, so
retaining it removes no detection — and arm G shows the sweep it feeds is live.
The comment in all five scripts now states the executed facts and labels the guard
as hardening rather than a repair. An overclaimed **defect** is still a false
evidence claim.

## R5-4. BA-3 — no executable change; prose narrowed

`transport_runner.ps1`'s classifier returns kind- and status-specific reasons
before the prerequisite-based rc-1 branch is reachable:
`scp_transfer_did_not_complete` for any nonzero `scp` (line 1103 in the round-5
file), `operation_reported_stop` for rc 3 (line 1108), and only the rc-1 fallthrough
at 1116–1120 produces `cleanup_after_unestablished_prerequisite` or
`cleanup_after_earlier_deviation`. Codex's round-4 Fixture B execution shows ops
09/10 reporting `scp_transfer_did_not_complete` and 11/12 reporting
`operation_reported_stop` with prerequisites genuinely unestablished.

Round 5 takes the **narrow-the-prose** branch, not the change-the-classifier
branch, and says so per file. The classifier is correct as written: an operation
whose own kind or status already explains why it is not evaluable should report
that reason, not a prerequisite reason it did not reach. Widening the two tokens
to every broken-branch `always` failure would make the record *less* precise, and
would require re-proving F4's decisive fixture for no gain.

The overstatement is in three places and **none of them is in this directory**:
`WPI_PREREGISTRATION_DRAFT.md:688-691` and
`WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:570,678`, all under
`WPI_PREREG_DRAFT_ROUND1/`, which the round-5 session was instructed not to touch
because a parallel session owned it. The exact replacement text for all three,
byte-semantically identical across the two successor copies as Band A requires, was
recorded in `TRANSPORT_R5_DRAFT_EDITS_PENDING.md`. The round-4 report's own T8
disposition is corrected in place, in this directory.

> **ROUND-6 STATUS UPDATE (Codex round-5 audit, R5-F3 — MEDIUM).** Those three
> edits are no longer outstanding. **The Lead applied all three, plus the BA-1
> draft mirror, and they are present in commit `37a87046`** — the same commit
> Codex froze for the round-5 audit. Verified in round 6 on the committed bytes:
> `grep -c 'The reason recorded is the' WPI_PREREGISTRATION_DRAFT.md` = 1, and
> `grep -c 'first applicable reason recorded'
> WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md` = **2** (the two successor copies
> Band A requires to stay identical). **BA-3 is therefore fully closed.** The
> per-edit record and the bound blob identities are §R6-3.

## R5-5. Static gates on the repaired bytes

| gate | result |
|---|---|
| `bash -n` on all five delivered shell files | rc 0 for each |
| `bash -n _r5_wsl_fixtures.sh` | rc 0 |
| CR bytes (`tr -cd '\r' \| wc -c`) per file | 0 for all seven targets and the harness |
| Windows PowerShell 5.1.26100.8875 parse of `transport_runner.ps1` | `PARSE_ERRORS=0` |
| placeholder census over the seven targets | `alloc=37 pin=38` — **unchanged** from round 4 |
| harness process rc | 0 |

The census is unchanged because every round-5 edit outside the close script's
create block is comment text, and the create block introduces no placeholder.

## R5-6. `_r5_wsl_fixtures.sh` — transcript (WITHDRAWN; superseded by §R6-2)

> **ROUND-6 WITHDRAWAL (Codex round-5 audit, R5-F2).** The transcript that stood
> here was the real output of the round-5 harness, but that harness's BA-1 arms did
> not use the common subject pathname and common argv this file claimed for them,
> so it could not be reproduced against the claim it was published to support, and
> its two recorded refusals were not byte-identical. It is **withdrawn** rather than
> kept beside a corrected copy: D026 makes the published transcript the
> reproducibility target, and two transcripts for one harness would give a
> re-auditor two targets, one of them wrong. The harness is repaired; its verbatim
> output is **§R6-2**, and what the repair did and did not move is **§R6-1**.

---

# ROUND 6 - 2026-08-11 - the three Codex round-5 re-audit findings

Implementer session: Claude Opus 5 xhigh (Max account), under
`KICKOFF_TRANSPORT_REPAIR_R6.md`. Input: `TRANSPORT_CODEX_R5_AUDIT_2026-08-11.md`
(**REQUEST_CHANGES**, frozen commit `37a87046`), read in full; its text binds.

**No host was contacted and no network connection was opened.** No socket of any
kind was created; no `ssh.exe`, `scp.exe` or `sshd` process was started. The fixture
re-run is on the same local WSL2 Ubuntu kernel rounds 4 and 5 used
(`6.18.33.2-microsoft-standard-WSL2`, GNU Bash 5.3.9), and every path it touches is
under `/root/wpi_r5` on that local filesystem.

**No byte of the nine-file transport set changed in round 6.** All seven
executable/plan targets hash exactly as round-5 §4 recorded them (§R6-5). The only
executable change is to the harness that ships beside them,
`_r5_wsl_fixtures.sh` — the object R5-F2 is about.

| finding | disposition |
|---|---|
| **R5-F1** (HIGH) — the main draft still closed the open outer boundary | **applied by the Lead**, commit `008d2dde`; not re-done here, verified read-only — §R6-4 |
| **R5-F2** (HIGH) — the published BA-1 arms did not use the claimed same argv | **REPAIRED, re-run** — §R6-1, §R6-2 |
| **R5-F3** (MEDIUM) — status/evidence still called committed draft edits pending | **CORRECTED** — §R6-3 |

## R6-1. R5-F2 — one subject pathname, one argument vector

**The finding is accepted in full.** Round 5 wrote that the BA-1 RED and GREEN arms
used "the same instrument, the same launch domain and the same argv, so the only
variable is the delivered bytes", and that the GREEN refusal was byte-identical to
the RED one. The harness it shipped did neither: `arm` took a per-arm script path
and a per-arm base directory, so RED ran `$FIX/red_diag.sh` against `$FIX/red_diag`
while GREEN ran `$FIX/green_diag.sh` against `$FIX/green_diag`, and the two recorded
`CLOSE_STOP` lines differed in their `path=` field. Codex's own supplemental
common-argv control returned the same RED/GREEN answer, but that does not repair the
delivered evidence: under D026 the implementer's recorded RED/GREEN and its literal
reproducibility are part of the closure evidence, and a provenance claim the harness
contradicts is a false evidence claim regardless of what the code does.

What changed in `_r5_wsl_fixtures.sh`:

| round 5 | round 6 |
|---|---|
| `arm <label> <script> <base>` — each arm passed its own subject path and its own tree | `arm <label> <built-bytes>` — every arm resets the one tree `$BA1_BASE`, installs the bytes at the one pathname `$BA1_SUBJECT`, and launches **that** with the one argv `<$BA1_EV> <$RUNID> <$BA1_WORK>` |
| instrumented variants were built at the path they were then launched from | variants are built under `$FIX/build/` and are **never launched from there**; the arm copies the chosen build to `$BA1_SUBJECT` |
| the late-refusal control built `mkdir_wide_red` and `mkdir_wide_green` — two instrument pathnames holding identical bytes | one `mkdir_wide` instrument at one pathname serves both arms |
| the two refusals were quoted and compared by eye | `REFUSAL_BYTE_IDENTICAL` is computed on the two whole lines |
| nothing asserted that the arms shared a launch | every arm appends `<subject>\|<ev>\|<runid>\|<work>` to `$BA1_IDENT`, and the **BA-1 LAUNCH IDENTITY** banner asserts the distinct count is 1 |

Executed, round 6 (§R6-2, verbatim):

```text
BA1_ARMS_RECORDED=10
DISTINCT_SUBJECT_ARGV_LINES=1
THE_LINE=/root/wpi_r5/close_subject.sh|/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0|WPIR5-FIXTURE-P0|/root/wpi_r5/ba1/work
```

and the D026 pair itself:

| | pre-repair bytes (RED) | repaired bytes (GREEN) |
|---|---|---|
| `SUBJECT_BUILT_FROM` | `/root/wpi_r5/build/red_diag.sh` | `/root/wpi_r5/build/green_diag.sh` |
| `SUBJECT_PATH` | `/root/wpi_r5/close_subject.sh` | **the same pathname** |
| `SUBJECT_SHA256` | `a61ac611fd8da95338ff9467f81a27f1097d1bd28b7a0da806f7bc79c048b2cf` | `e48e1a07e3ef4e2a4a6f48c830cf0389bb883f42f4a33922008f3fd5957758b4` |
| `ARGV` | `[…/ba1/evidence/runkit/WPIR5-FIXTURE-P0] [WPIR5-FIXTURE-P0] […/ba1/work]` | **the same vector** |
| `SCRIPT_RC` | 3 | 3 |
| refusal | `CLOSE_STOP reason=work_dir_mkdir_diagnostics path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 detail=injected_success_diagnostic` | **byte-identical** — `REFUSAL_BYTE_IDENTICAL=yes` |
| `RESIDUE_PRESENT` | **yes** | **no** |

`SUBJECT_SHA256` is the hash of what is installed at that pathname — the
fixture-retargeted, and where declared instrumented, form of the delivered bytes —
**not** the hash of a delivered file. All ten arms print a different
`SUBJECT_SHA256`, which is the point: the pathname and the argv are constant and the
bytes are the variable. The two delivered identities under test are printed once by
the `FIXTURE ENVIRONMENT` banner —
`29b6412a466c10854ddf09effc8d5216317738a012235ce563c9764a9e0c40ef` (RED, the
pre-repair blob read with `git cat-file blob`) and
`8892574f253ab26d6d48bba270f84ef2da4458a5bca93f2b3c9723991a3732cf` (GREEN, the
working-tree file) — and `SUBJECT_BUILT_FROM` names which of the two each arm's
bytes derive from.

**What the repair did not move.** Every arm reached the same disposition it reached
in round 5: 10 arms, the same `SCRIPT_RC` per arm, the same residue answer per arm,
the same reason tokens. The carried fence is untouched and still refuses in both
arms, exactly as Codex found — `[ -z "$MKDIR_OUT" ] || stop
"work_dir_mkdir_diagnostics …"`, at line 402 in the pre-repair bytes and 483 in the
repaired bytes, with the predicate and the reason token unchanged. The two clean-run
regression arms now differ in exactly one field, visible line-for-line because they
share the tree and the argv:
`removal=adjudicated_on_every_exit_path` → `removal=adjudicated_on_every_exit_path_after_a_zero_status_create`.

The harness's own process rc is 0 and it wrote **0 bytes** to its own stderr.

## R6-2. `_r5_wsl_fixtures.sh` — transcript (verbatim, round-6 re-run)

Exact command (the driver runs the harness under the same launch shape round 5 used;
`FIXTURE_RC` is the harness's own process status):

```text
wsl.exe -u root -- /usr/bin/bash --noprofile --norc \
  /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/_r5_wsl_fixtures.sh \
  /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT \
  <scratch>/r6/pre

FIXTURE_RC=0
FIXTURE_STDERR_LINES=0
FIXTURE_STDERR_BYTES=0
FIXTURE_STDOUT_LINES=280
```

`<scratch>/r6/pre/remote_close_tree_wpi.sh` is
`git cat-file blob 61696132a5f2fce97aad4054d41a780297ff21a1`, the close-script blob
frozen at round 4 and named by the round-5 kickoff; its SHA-256 is printed in the
transcript below and is `29b6412a…`.

```text

########## FIXTURE ENVIRONMENT
$ uname -sr; id -u; id -g; bash --version | head -1
Linux 6.18.33.2-microsoft-standard-WSL2
0
0
GNU bash, version 5.3.9(1)-release (x86_64-pc-linux-gnu)
$ sha256sum <the two close scripts under test>
8892574f253ab26d6d48bba270f84ef2da4458a5bca93f2b3c9723991a3732cf  /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_close_tree_wpi.sh
29b6412a466c10854ddf09effc8d5216317738a012235ce563c9764a9e0c40ef  /mnt/c/Users/BARSEM~1/AppData/Local/Temp/claude/C--LAB-Tradingview-LAB-CLEAN/d99e3b8e-1ade-4486-9408-0cee0036ce6d/scratchpad/r6/pre/remote_close_tree_wpi.sh
RETARGET_ANCHORS=hit_in_both_arms

########## BA-1 RED - PRE-REPAIR bytes + INSTRUMENT 1 (mkdir creates, warns, rc 0)
# Codex round-4 Band A reproduced SCRIPT_RC=3 ... RESIDUE_PRESENT=yes here:
# the directory is created at :401, the diagnostic branch stops at :402, and
# the cleanup trap is not installed until :424.
$ env -i PATH=... LC_ALL=C HOME=... /usr/bin/bash --noprofile --norc $BA1_SUBJECT $BA1_EV $RUNID $BA1_WORK
SUBJECT_BUILT_FROM=/root/wpi_r5/build/red_diag.sh
SUBJECT_PATH=/root/wpi_r5/close_subject.sh
SUBJECT_SHA256=a61ac611fd8da95338ff9467f81a27f1097d1bd28b7a0da806f7bc79c048b2cf
ARGV=[/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0] [WPIR5-FIXTURE-P0] [/root/wpi_r5/ba1/work]
SCRIPT_RC=3
CLOSE_STOP reason=work_dir_mkdir_diagnostics path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 detail=injected_success_diagnostic
RESIDUE_PRESENT=yes path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0
RESIDUE_LISTING:
  /root/wpi_r5/ba1/work
  /root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0
EVIDENCE_TREE_AFTER:
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/a.txt
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/b.txt

########## BA-1 GREEN - REPAIRED bytes + THE SAME INSTRUMENT 1
# Same deviant tool output, and literally the same subject pathname, launch
# and argv as the RED arm above - the tree is reset and only the bytes at
# $BA1_SUBJECT are replaced, so SUBJECT_SHA256 is the one field that moves.
# The reasoned STOP is retained byte-for-byte (reason=work_dir_mkdir_diagnostics
# with the same path and the same detail), and the directory is gone because
# the cleanup is armed on the zero status BEFORE the diagnostic is adjudicated.
$ env -i PATH=... LC_ALL=C HOME=... /usr/bin/bash --noprofile --norc $BA1_SUBJECT $BA1_EV $RUNID $BA1_WORK
SUBJECT_BUILT_FROM=/root/wpi_r5/build/green_diag.sh
SUBJECT_PATH=/root/wpi_r5/close_subject.sh
SUBJECT_SHA256=e48e1a07e3ef4e2a4a6f48c830cf0389bb883f42f4a33922008f3fd5957758b4
ARGV=[/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0] [WPIR5-FIXTURE-P0] [/root/wpi_r5/ba1/work]
SCRIPT_RC=3
CLOSE_STOP reason=work_dir_mkdir_diagnostics path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 detail=injected_success_diagnostic
RESIDUE_PRESENT=no
EVIDENCE_TREE_AFTER:
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/a.txt
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/b.txt

########## BA-1 FENCE DISCRIMINATING POWER - old and new assertion, same deviant output
# The carried fence is `[ -z "$MKDIR_OUT" ] || stop work_dir_mkdir_diagnostics`.
# It was NOT weakened: the predicate and the reason token are unchanged, and
# both the pre-repair and the repaired assertion refuse the same injected
# diagnostic. Quoted from the two arms above. Because both arms ran from one
# subject pathname against one tree, the two refusals are compared as whole
# lines with nothing symbolised away:
OLD_ASSERTION_LINE : 402:[ -z "$MKDIR_OUT" ] || stop "work_dir_mkdir_diagnostics path=$WORK detail=$MKDIR_OUT"
NEW_ASSERTION_LINE : 483:[ -z "$MKDIR_OUT" ] || stop "work_dir_mkdir_diagnostics path=$WORK detail=$MKDIR_OUT"
OLD_REFUSAL        : CLOSE_STOP reason=work_dir_mkdir_diagnostics path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 detail=injected_success_diagnostic
NEW_REFUSAL        : CLOSE_STOP reason=work_dir_mkdir_diagnostics path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 detail=injected_success_diagnostic
REFUSAL_BYTE_IDENTICAL=yes

########## BA-1 REGRESSION - clean run, PRE-REPAIR bytes, no instrument
SUBJECT_BUILT_FROM=/root/wpi_r5/close_red.sh
SUBJECT_PATH=/root/wpi_r5/close_subject.sh
SUBJECT_SHA256=030d8d44f9958d1c13a3025f1573b6a45aeab5124f598f33af978c61dd6b76aa
ARGV=[/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0] [WPIR5-FIXTURE-P0] [/root/wpi_r5/ba1/work]
SCRIPT_RC=0
(no CLOSE_STOP/CLOSE_FAIL on stderr)
RESIDUE_PRESENT=no
EVIDENCE_TREE_AFTER:
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/a.txt
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/b.txt
CLOSE_NOTE scratch work_dir=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 owner_numeric=0:0 mode=700 created=once tmpdir=run_owned canonical_non_overlap=proven_before_and_after_create removal=adjudicated_on_every_exit_path
CLOSE PASS runid=WPIR5-FIXTURE-P0 dir=/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0 files=2 wrote_into_evidence_tree=0

########## BA-1 REGRESSION - clean run, REPAIRED bytes, no instrument
# rc 0, the same record, no residue: the repair did not change the happy path.
# Same subject pathname and same argv as the arm above, so the two records are
# comparable line for line and the one moved field is visible on its own.
SUBJECT_BUILT_FROM=/root/wpi_r5/close_green.sh
SUBJECT_PATH=/root/wpi_r5/close_subject.sh
SUBJECT_SHA256=80b43c7196e884beef9ae2638b8fdbfcd27394e41b18f5c6dc705f29c3713147
ARGV=[/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0] [WPIR5-FIXTURE-P0] [/root/wpi_r5/ba1/work]
SCRIPT_RC=0
(no CLOSE_STOP/CLOSE_FAIL on stderr)
RESIDUE_PRESENT=no
EVIDENCE_TREE_AFTER:
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/a.txt
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/b.txt
CLOSE_NOTE scratch work_dir=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 owner_numeric=0:0 mode=700 created=once tmpdir=run_owned canonical_non_overlap=proven_before_and_after_create removal=adjudicated_on_every_exit_path_after_a_zero_status_create
CLOSE PASS runid=WPIR5-FIXTURE-P0 dir=/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0 files=2 wrote_into_evidence_tree=0

########## BA-1 - a nonzero mkdir that created NOTHING: PRE-REPAIR vs REPAIRED
# Both STOP. The repaired arm additionally records the tool rc, the captured
# diagnostic, and whether an object is present - the round-4 message carried
# only the path.
SUBJECT_BUILT_FROM=/root/wpi_r5/build/red_failclean.sh
SUBJECT_PATH=/root/wpi_r5/close_subject.sh
SUBJECT_SHA256=83704938a96f680600a4c64016255f4dc979d4d442a3e8345538ad2b0a7bef63
ARGV=[/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0] [WPIR5-FIXTURE-P0] [/root/wpi_r5/ba1/work]
SCRIPT_RC=3
CLOSE_STOP reason=work_dir_mkdir_failed path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0
RESIDUE_PRESENT=no
EVIDENCE_TREE_AFTER:
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/a.txt
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/b.txt
SUBJECT_BUILT_FROM=/root/wpi_r5/build/green_failclean.sh
SUBJECT_PATH=/root/wpi_r5/close_subject.sh
SUBJECT_SHA256=99f93e2af27de3423ed48cdcd2d7686e094e8b9e5715bf65d0120ac6cdcec063
ARGV=[/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0] [WPIR5-FIXTURE-P0] [/root/wpi_r5/ba1/work]
SCRIPT_RC=3
CLOSE_STOP reason=work_dir_mkdir_failed path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 rc=1 object_after_failed_create=absent cleanup=not_armed_for_a_nonzero_create detail=[injected_failure_no_object_created]
RESIDUE_PRESENT=no
EVIDENCE_TREE_AFTER:
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/a.txt
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/b.txt

########## BA-1 - THE DECLARED UNCOVERED CASE: a nonzero mkdir that DID create
# The repaired bytes deliberately do NOT arm cleanup here: a nonzero status
# is not evidence that the object at that path is the one this run created,
# and `rm -rf` on an object it cannot prove it created is the wrong answer.
# The header, the create block and the CLOSE_NOTE scratch field all say so.
# Residue in this arm is the honest scope of the claim, not a hidden failure:
# the record now NAMES it (object_after_failed_create=present).
SUBJECT_BUILT_FROM=/root/wpi_r5/build/green_faildirty.sh
SUBJECT_PATH=/root/wpi_r5/close_subject.sh
SUBJECT_SHA256=df32c8ef8c08b5a9a0ed5e74ab6207891791729f2ade9d9ea224bff99ad0fbcf
ARGV=[/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0] [WPIR5-FIXTURE-P0] [/root/wpi_r5/ba1/work]
SCRIPT_RC=3
CLOSE_STOP reason=work_dir_mkdir_failed path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 rc=1 object_after_failed_create=present cleanup=not_armed_for_a_nonzero_create detail=[injected_failure_after_object_created]
RESIDUE_PRESENT=yes path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0
RESIDUE_LISTING:
  /root/wpi_r5/ba1/work
  /root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0
EVIDENCE_TREE_AFTER:
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/a.txt
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/b.txt

########## BA-1 - the removal adjudication is LIVE on the newly covered path
# Instrument 1 (create + diagnostic + rc 0) plus an `rm` that reports success
# and removes nothing. The newly armed cleanup must not accept that.
SUBJECT_BUILT_FROM=/root/wpi_r5/build/green_diag_rmnoop.sh
SUBJECT_PATH=/root/wpi_r5/close_subject.sh
SUBJECT_SHA256=aea905f4e72f2ff34dc2b294a2289d7a55afaa2e22dcb7304d2df103774f7c88
ARGV=[/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0] [WPIR5-FIXTURE-P0] [/root/wpi_r5/ba1/work]
SCRIPT_RC=3
CLOSE_STOP reason=work_dir_mkdir_diagnostics path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 detail=injected_success_diagnostic
CLOSE_STOP reason=work_dir_removal_failed path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0 rc=0 detail=[]
RESIDUE_PRESENT=yes path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0
RESIDUE_LISTING:
  /root/wpi_r5/ba1/work
  /root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0
EVIDENCE_TREE_AFTER:
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/a.txt
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/b.txt

########## BA-1 - cleanup still covers a later refusal after a clean create
# A work-directory mode disagreement STOPs well after the create. Both arms
# had cleanup armed by then, so this is a control showing the repair did not
# move an exit path that round 4 already covered.

--- arm=red
SUBJECT_BUILT_FROM=/root/wpi_r5/build/red_mode.sh
SUBJECT_PATH=/root/wpi_r5/close_subject.sh
SUBJECT_SHA256=3dcf4c7cd2de33c9dd5f386a8ab3949cde6f9a657c50511009f4c26476b3011d
ARGV=[/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0] [WPIR5-FIXTURE-P0] [/root/wpi_r5/ba1/work]
SCRIPT_RC=3
CLOSE_STOP reason=work_dir_mode=750 expected=700 path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0
RESIDUE_PRESENT=no
EVIDENCE_TREE_AFTER:
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/a.txt
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/b.txt

--- arm=green
SUBJECT_BUILT_FROM=/root/wpi_r5/build/green_mode.sh
SUBJECT_PATH=/root/wpi_r5/close_subject.sh
SUBJECT_SHA256=e2ea8c91430d3deceba220d8d926921152039c21dae10d807d1483bba50e8968
ARGV=[/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0] [WPIR5-FIXTURE-P0] [/root/wpi_r5/ba1/work]
SCRIPT_RC=3
CLOSE_STOP reason=work_dir_mode=750 expected=700 path=/root/wpi_r5/ba1/work/close_work_WPIR5-FIXTURE-P0
RESIDUE_PRESENT=no
EVIDENCE_TREE_AFTER:
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/a.txt
  /root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0/b.txt

########## BA-1 LAUNCH IDENTITY - every arm above used ONE pathname and ONE argv
# R5-F2. Each arm appended the subject pathname and the three arguments it
# actually launched with. If the arms had differed in either, the distinct
# count below would exceed 1 and the same-argv claim would be false.
BA1_ARMS_RECORDED=10
DISTINCT_SUBJECT_ARGV_LINES=1
THE_LINE=/root/wpi_r5/close_subject.sh|/root/wpi_r5/ba1/evidence/runkit/WPIR5-FIXTURE-P0|WPIR5-FIXTURE-P0|/root/wpi_r5/ba1/work

########## F1 OPEN - the outer account-shell boundary, reproduced locally
# SCOPE OF THIS ARM, STATED FIRST. This is NOT closure evidence and is NOT
# the real transport path. No host is contacted, no socket is opened and no
# ssh/sshd process is started. It is a LOCAL MODEL of one composition step
# that Codex round-4 Band B judged on the bytes: sshd does not execute the
# remote command string itself - it hands the string to the account shell,
# which processes its own startup environment BEFORE the string first token
# runs. The model is `BASH_ENV=<plant> /usr/bin/bash -c "<the frozen command
# string>" < <the delivered script>`. The command string is byte-identical to
# the frozen $REMOTE_LAUNCH_DOMAIN, and the delivered script is the REPAIRED
# round-5 file - so this shows the boundary is not closed BY the repair.
$ BASH_ENV=<exiting plant> /usr/bin/bash -c '<frozen command string>' < close_green.sh
COMMAND_STRING=/usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C HOME=/root /usr/bin/bash --noprofile --norc -s -- /root/wpi_r5/f1outer/evidence/runkit/WPIR5-FIXTURE-P0 WPIR5-FIXTURE-P0 /root/wpi_r5/f1outer/work
RC=0
OUTER_PLANT_RAN=yes
STDOUT:
  CLOSE PASS runid=WPIR5-FIXTURE-P0 dir=/root/wpi_r5/f1outer/evidence/runkit/WPIR5-FIXTURE-P0 files=2 wrote_into_evidence_tree=0
STDERR:
DELIVERED_SCRIPT_RECORD_LINES=0   (CLOSE_NOTE emitted by the real program)
# The runner would ACCEPT this capture: transport_runner.ps1 registers the
# prefixes CLOSE_ and "CLOSE " for the stdin leaf remote_close_tree_wpi.sh,
# and the forged line starts with one of them at an in-grammar rc 0. Marker
# SHAPE is bound to the plan row, not the process that produced it.
# CONTROL 1 - what the inner-child domain DOES still close. A plant that lets
# the delivered script RUN - the only kind that could forge a REAL-looking
# record rather than a bare line - is refused by name, because BASH_ENV is
# still in the exec environment the kernel recorded for the inner child:
CLOSE_STOP reason=launch_domain_unexpected_environment_entry name=[BASH_ENV]
RC=3  QUIET_PLANT_RAN=yes
# CONTROL 2 - and what it does NOT close, even when BASH_ENV is delivered
# INSIDE the domain: an EXITING plant still forges, at rc 0. Round 4 recorded
# this case and (correctly) noted the frozen plan cannot introduce BASH_ENV
# into the env -i list. What round 4 got wrong, and Band B caught, is that
# the plan is not the only way in: the OUTER account shell above needs no
# plan row at all.
CLOSE PASS runid=WPIR5-FIXTURE-P0 dir=/root/wpi_r5/f1outer/evidence/runkit/WPIR5-FIXTURE-P0 files=2 wrote_into_evidence_tree=0
RC=0

########## BA-2 - the claimed second `declare -F` defect, executed
# The round-4 report and five delivered scripts said bare `declare -F` exits 1
# when no function exists and would end the run under `set -Eeuo pipefail`.
# Arm D proves set -e IS armed in the same shell shape, so arm B falsifies
# the claim rather than merely failing to trigger it. Arm F is the
# discriminating-power check for KEEPING the guard as no-op hardening.
BASH_VERSION=5.3.9(1)-release

===== A. DIRECT no-argument declare -F in a function-free shell =====
DIRECT_RC=0
PROCESS_RC=0

===== B. UNGUARDED assignment under set -Eeuo pipefail (the claimed RED) =====
AFTER_ASSIGN len=0
STILL_RUNNING=yes
PROCESS_RC=0

===== C. CONTROL: a NAMED lookup of a missing function DOES exit 1 =====
PROCESS_RC=1

===== D. CONTROL: set -e really is armed in arm B (deliberate rc-1 command) =====
PROCESS_RC=1

===== E. The delivered guarded form, same function-free shell =====
AFTER_ASSIGN len=0
PROCESS_RC=0

===== F. DISCRIMINATING POWER: both forms still SEE an inherited function =====
UNGUARDED=[declare -fx foo]
GUARDED=[declare -fx foo]
PROCESS_RC=0

===== G. the delivered scripts still refuse an inherited exported function =====
CLOSE_STOP reason=launch_domain_inherited_shell_function detail=[declare -fx a_plant]
RC=3

########## DONE
```

## R6-3. R5-F3 — the four draft edits are applied, committed, and bound

**The finding is accepted in full.** The round-5 evidence chain recorded the four
cross-directory draft edits as outstanding, and that record was true of the
implementer session's boundary but **false as the final status of the frozen
commit**: the Lead applied all four before freezing, and `37a87046` already
contained them when Codex audited it. Round 6 verified this read-only, on the
committed bytes, without writing to `WPI_PREREG_DRAFT_ROUND1/`.

| edit | site | verification on the current committed bytes |
|---|---|---|
| 1 — BA-3 | `WPI_PREREGISTRATION_DRAFT.md` §6 | `grep -c 'The reason recorded is the'` = **1** |
| 2 — BA-3 | `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md` §6 | see below |
| 3 — BA-3 | `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md` Gap 10 | `grep -c 'first applicable reason recorded'` = **2** across the file — the two copies Band A requires to stay identical, both present |
| 4 — BA-1 | `WPI_PREREGISTRATION_DRAFT.md` §4, derivation class 6 | `grep -c 'object_after_failed_create=present\|absent'` = **1** |

Bound identities — the two draft blobs and the commits that carry them:

| file | blob at `37a87046` (BA-3 ×3 + BA-1 mirror) | blob at `008d2dde` = current `HEAD` (R5-F1 applied) |
|---|---|---|
| `WPI_PREREGISTRATION_DRAFT.md` | `f2bc8f682f054d9283922d17501ea0dfa94d0bfc` | `35936fe464c8b1d7faf892bcc809aac38da48b1e` |
| `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md` | `0c6e8030eaf0b5858f1af34fb6fd29fc65cff2a2` | `1aad4f61a76085605cf3a2664f012d4e3d7407ba` |

Neither file is modified in the working tree relative to `HEAD`, so the bytes
verified above are the committed bytes.

**Consequences for the status text.** `STATUS_TRANSPORT.md`'s "until those three
edits land, BA-3 is not fully closed" sentence, the round-5 report's four
NOT APPLIED / outstanding labels, and `TRANSPORT_R5_DRAFT_EDITS_PENDING.md`'s
pending framing are all corrected. **BA-3 is fully closed** and **F1's draft mirror
is aligned.** `TRANSPORT_R5_DRAFT_EDITS_PENDING.md` is **not deleted** — it is
marked superseded and kept as the historical specification of what was handed over,
which is the record a re-auditor needs to check that what landed is what was
specified.

## R6-4. R5-F1 — Lead-applied; verified read-only, not re-done

R5-F1 was applied by the Lead in commit `008d2dde` and this session did **not**
touch `WPI_PREREG_DRAFT_ROUND1/`. Verified read-only on the committed bytes:

| site | disposition now recorded |
|---|---|
| `WPI_PREREGISTRATION_DRAFT.md:343-344` (derivation class 5) | "**Disposition: inner child closed; outer SSH account-shell boundary OPEN.**" |
| `WPI_PREREGISTRATION_DRAFT.md:585-586` (remote-launch domain) | "**This closes the inner child only; the outer SSH account-shell boundary is OPEN.**" |
| `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:408` and `:697` | the inherited "cleared launch domain" clause now ends "…closes the inner child only; the outer SSH account-shell boundary (a server-supplied `BASH_ENV`/`ENV` acting before `env -i`) remains OPEN, and no successor text may present the cleared inner-child domain as an end-to-end F1 closure" — the two occurrences carry the same sentence |

The scoped sweep R5-F1 asked for was repeated read-only over both drafts:
`grep -n -i "unreachable\|closed on the composition\|closed by the operator
side\|cannot select or influence"` returns **no F1-related hit**. The seven
`unreachable` matches are the RP6-P0 `system_manager_unreachable` reason token
(`:813`, `:1063-1066`, `:1089`) and two unrelated sentences (`:91` "a block that
contains an unreachable path will reach it"; `:1206` "structurally unreachable
rather than merely unenumerated"). No hit asserts F1 closure or residual
unreachability.

**F1 remains OPEN.** Nothing in round 6 narrows it: the round changed one harness's
launch provenance and three documents' status text.

## R6-5. Static gates, round 6

| gate | result |
|---|---|
| the seven executable/plan targets, SHA-256 vs round-5 §4 | **7/7 identical — no target byte changed** |
| `bash -n` on all five delivered shell files | rc 0 for each |
| `bash -n _r5_wsl_fixtures.sh` | rc 0 |
| CR bytes per file (`tr -cd '\r' \| wc -c`) | 0 for all seven targets and the harness |
| Windows PowerShell 5.1.26100.8875 parse of `transport_runner.ps1` | `PARSE_ERRORS=0` |
| placeholder census over the seven executable/plan targets | `alloc=37 pin=38` — unchanged from rounds 4 and 5 |
| `_r5_wsl_fixtures.sh` process rc / own stderr | 0 / **0 bytes** |
| BA-1 arms recorded / distinct subject+argv lines | 10 / **1** |
| RED vs GREEN refusal | `REFUSAL_BYTE_IDENTICAL=yes` |

`_r5_wsl_fixtures.sh` after the repair: 21,221 bytes,
`a2bb6f6e3c0022aa001db7adb58189649acab9b23b522dc0544b018f9ce7971b`, 0 CR.
