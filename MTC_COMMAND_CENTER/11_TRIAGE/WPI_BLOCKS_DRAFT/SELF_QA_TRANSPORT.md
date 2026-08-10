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
recorded in `TRANSPORT_REPAIR_R3_REPORT.md` §6 over its own scope — seven
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
