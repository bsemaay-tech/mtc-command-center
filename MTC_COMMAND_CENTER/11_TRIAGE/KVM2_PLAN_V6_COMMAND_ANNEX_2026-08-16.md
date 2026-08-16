# Plan V6 inputs — round-4 R5–R8

Status: **COMMAND ANNEX OF RECORD — executable only under the owner-signed
sentence.** Lead-repinned 2026-08-16 night to the FINAL candidate
`be007fd802bbfd2eb181d66038c374865d1562ee`, payload `C:	mp\payload-be007fd8`,
manifest sha256
`bde1ff7dcd46a8b104ffdaca7a146ba0eca1958dab577a5a8e926dc24ee0b0a3`
(21 identity replacements verified, zero stale pins).

**Stage-0 addition (owner-directed):** before the Stage-1 transfer, remove the
superseded old payload from the host:
`ssh <isolated options> baris@152.239.123.231 'rm -rf ~/payload-acdf4e37'`
— the old payload directory is the only object removed; nothing else existed.

## R5 — complete literal command blocks

The operator uses only the owner-loaded Windows ssh-agent. Every `scp` and `ssh`
invocation below carries the launcher's complete isolated trust/authentication
option set. Any nonzero rc is a STOP. Commands used as evidence also state their
exact stderr disposition; OpenSSH progress/diagnostics are retained for review
and are never treated as success when the native process rc is nonzero.

### Stage 1 — isolated transfer, isolated SSH, dry run

```powershell
& 'C:\Windows\System32\OpenSSH\scp.exe' `
  -F NUL `
  -o IdentityFile=NUL `
  -o ProxyCommand=none `
  -o ProxyJump=none `
  -o GlobalKnownHostsFile=NUL `
  -o 'UserKnownHostsFile=C:\Users\BarışSemaay\.ssh\known_hosts' `
  -o IdentitiesOnly=no `
  -o PasswordAuthentication=no `
  -o KbdInteractiveAuthentication=no `
  -o BatchMode=yes `
  -o StrictHostKeyChecking=yes `
  -o ExitOnForwardFailure=yes `
  -o ConnectTimeout=10 `
  -r 'C:\tmp\payload-be007fd8' `
  'baris@152.239.123.231:~/'
if ($LASTEXITCODE -ne 0) { throw "STOP: payload scp failed rc=$LASTEXITCODE" }

& 'C:\Windows\System32\OpenSSH\ssh.exe' `
  -F NUL `
  -o IdentityFile=NUL `
  -o ProxyCommand=none `
  -o ProxyJump=none `
  -o GlobalKnownHostsFile=NUL `
  -o 'UserKnownHostsFile=C:\Users\BarışSemaay\.ssh\known_hosts' `
  -o IdentitiesOnly=no `
  -o PasswordAuthentication=no `
  -o KbdInteractiveAuthentication=no `
  -o BatchMode=yes `
  -o StrictHostKeyChecking=yes `
  -o ExitOnForwardFailure=yes `
  -o ConnectTimeout=10 `
  'baris@152.239.123.231'
if ($LASTEXITCODE -ne 0) { throw "STOP: isolated SSH failed rc=$LASTEXITCODE" }
```

Inside that isolated SSH session:

```bash
sudo bash ~/payload-be007fd8/IBKR_PAPER_BRIDGE/deploy/linux/install.sh \
  --release-sha be007fd802bbfd2eb181d66038c374865d1562ee \
  --manifest-sha256 bde1ff7dcd46a8b104ffdaca7a146ba0eca1958dab577a5a8e926dc24ee0b0a3 \
  --source ~/payload-be007fd8 --dry-run
```

### Stage 2 — one install and read-only verify

```bash
sudo bash ~/payload-be007fd8/IBKR_PAPER_BRIDGE/deploy/linux/install.sh \
  --release-sha be007fd802bbfd2eb181d66038c374865d1562ee \
  --manifest-sha256 bde1ff7dcd46a8b104ffdaca7a146ba0eca1958dab577a5a8e926dc24ee0b0a3 \
  --source ~/payload-be007fd8

sudo bash /opt/mtc-bridge/releases/be007fd802bbfd2eb181d66038c374865d1562ee/IBKR_PAPER_BRIDGE/deploy/linux/verify.sh \
  --release-sha be007fd802bbfd2eb181d66038c374865d1562ee \
  --manifest-sha256 bde1ff7dcd46a8b104ffdaca7a146ba0eca1958dab577a5a8e926dc24ee0b0a3
```

### Stage 3.1–3.2 — deterministic never-started state and rehearsal

```bash
set -Eeuo pipefail
export LC_ALL=C
sudo tar -C / -czf /home/baris/bridge-state-initial.tar.gz \
  var/lib/mtc-bridge etc/mtc-bridge
sha256sum /home/baris/bridge-state-initial.tar.gz \
  > /home/baris/bridge-state-initial.sha256
STATE_MANIFEST_SHA256="$(awk 'NR == 1 { print $1 }' /home/baris/bridge-state-initial.sha256)"
case "${STATE_MANIFEST_SHA256}" in
  ''|*[!0-9a-f]*)
    printf '%s\n' 'STOP: state archive SHA-256 is not exactly 64 lowercase hex' >&2
    exit 1
    ;;
esac
test "${#STATE_MANIFEST_SHA256}" -eq 64 || {
  printf '%s\n' 'STOP: state archive SHA-256 length is not 64' >&2
  exit 1
}

sudo bash /opt/mtc-bridge/releases/be007fd802bbfd2eb181d66038c374865d1562ee/IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh \
  --state-manifest-file /home/baris/bridge-state-initial.tar.gz \
  --state-manifest-sha256 "${STATE_MANIFEST_SHA256}"

sudo bash /opt/mtc-bridge/releases/be007fd802bbfd2eb181d66038c374865d1562ee/IBKR_PAPER_BRIDGE/deploy/linux/verify.sh \
  --release-sha be007fd802bbfd2eb181d66038c374865d1562ee \
  --manifest-sha256 bde1ff7dcd46a8b104ffdaca7a146ba0eca1958dab577a5a8e926dc24ee0b0a3
```

The first `case` is a character fence; the separate length test is the length
fence. No `bridge.db` is assumed or fabricated.

### Stage 3.3 — encrypted-in-transit/off-host encrypted-at-rest copy and restore

On the operator PC, create an EFS-encrypted directory and prove that `cipher`
accepted it before copying. If EFS is unavailable, STOP; do not silently store
the archive unencrypted.

```powershell
$BackupRoot = 'C:\tmp\KVM2_BRIDGE_ENCRYPTED'
$RestoreRoot = 'C:\tmp\KVM2_BRIDGE_RESTORE_CHECK'
New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null
& "$env:WINDIR\System32\cipher.exe" /E /A $BackupRoot
if ($LASTEXITCODE -ne 0) { throw "STOP: EFS encryption could not be enabled rc=$LASTEXITCODE" }

& 'C:\Windows\System32\OpenSSH\scp.exe' `
  -F NUL `
  -o IdentityFile=NUL `
  -o ProxyCommand=none `
  -o ProxyJump=none `
  -o GlobalKnownHostsFile=NUL `
  -o 'UserKnownHostsFile=C:\Users\BarışSemaay\.ssh\known_hosts' `
  -o IdentitiesOnly=no `
  -o PasswordAuthentication=no `
  -o KbdInteractiveAuthentication=no `
  -o BatchMode=yes `
  -o StrictHostKeyChecking=yes `
  -o ExitOnForwardFailure=yes `
  -o ConnectTimeout=10 `
  'baris@152.239.123.231:/home/baris/bridge-state-initial.tar.gz' `
  'baris@152.239.123.231:/home/baris/bridge-state-initial.sha256' `
  $BackupRoot
if ($LASTEXITCODE -ne 0) { throw "STOP: state archive scp failed rc=$LASTEXITCODE" }

& "$env:WINDIR\System32\cipher.exe" /C "$BackupRoot\bridge-state-initial.tar.gz"
if ($LASTEXITCODE -ne 0) { throw "STOP: copied archive is not proven EFS-encrypted rc=$LASTEXITCODE" }

$CertutilOutput = & "$env:WINDIR\System32\certutil.exe" -hashfile "$BackupRoot\bridge-state-initial.tar.gz" SHA256 2>&1
if ($LASTEXITCODE -ne 0) { throw "STOP: certutil hash failed rc=$LASTEXITCODE" }
$LocalHashLines = @($CertutilOutput | ForEach-Object { $_.ToString().Trim() } | Where-Object { $_ -match '^[0-9A-Fa-f]{64}$' })
if ($LocalHashLines.Count -ne 1) { throw 'STOP: certutil did not emit exactly one 64-hex SHA-256' }
$LocalHash = $LocalHashLines[0].ToLowerInvariant()
$RemoteHashLine = (Get-Content -LiteralPath "$BackupRoot\bridge-state-initial.sha256" -Raw).Trim()
if ($RemoteHashLine -notmatch '^([0-9a-f]{64})  /home/baris/bridge-state-initial\.tar\.gz$') {
  throw 'STOP: remote sha256sum record has unexpected grammar'
}
if ($LocalHash -ne $Matches[1]) { throw 'STOP: off-host archive hash differs from host record' }

New-Item -ItemType Directory -Force -Path $RestoreRoot | Out-Null
& "$env:WINDIR\System32\cipher.exe" /E /A $RestoreRoot
if ($LASTEXITCODE -ne 0) { throw "STOP: restore-check directory could not be EFS-encrypted rc=$LASTEXITCODE" }
& "$env:WINDIR\System32\tar.exe" -tzf "$BackupRoot\bridge-state-initial.tar.gz"
if ($LASTEXITCODE -ne 0) { throw "STOP: tar inventory failed rc=$LASTEXITCODE" }
& "$env:WINDIR\System32\tar.exe" -xzf "$BackupRoot\bridge-state-initial.tar.gz" -C $RestoreRoot
if ($LASTEXITCODE -ne 0) { throw "STOP: tar restore failed rc=$LASTEXITCODE" }
& "$env:WINDIR\System32\tar.exe" -df "$BackupRoot\bridge-state-initial.tar.gz" -C $RestoreRoot
if ($LASTEXITCODE -ne 0) { throw "STOP: restored tree differs from archive rc=$LASTEXITCODE" }
```

The SSH transport encrypts the copy in transit; the proven EFS directory is the
at-rest encryption control. `certutil` binds the copied archive to the host hash,
and Windows 11's built-in `tar` inventories, restores, and compares the restored
tree to the archive.

### Stage 3.4 — monitoring baseline

Run each command separately and capture stdout, stderr, and rc. `df`, both `du`
commands, and `systemctl is-active cron` require rc 0 and empty stderr. The
masked/unstarted Bridge unit must produce stdout exactly `inactive` and rc 1 from
`systemctl is-failed`; any other rc/stdout or any stderr is STOP.

```bash
df -B1 / /opt/mtc-bridge /etc/mtc-bridge /var/lib/mtc-bridge /var/log/mtc-bridge
sudo du -s -B1 /opt/mtc-bridge /etc/mtc-bridge /var/lib/mtc-bridge /var/log/mtc-bridge
sudo du -s -B1 /var/log/mtc-bridge
systemctl is-failed mtc-bridge-first-start.service
systemctl is-active cron
```

STOP if the Bridge total approaches or exceeds 10,000,000,000 bytes, if logs
approach or exceed that tenant budget, if the root filesystem lacks the plan's
recorded headroom, or if the unit/cron dispositions differ from the exact rules
above.

### Stage 3.5 — complete re-inventory command set

This reuses the read-only command set from the original KVM2 Phase-1 inventory
procedure. Execute each row separately; capture raw stdout, stderr, and rc before
interpreting it. Expected-absence rows (`command -v`, container grep, Bridge
pre-install absence) have an explicitly recorded no-match branch; every other
unexpected nonzero rc or stderr is STOP. Diff the results against
`KVM2_READONLY_INVENTORY_2026-08-16.md`; only the complete Bridge tenancy objects
in R8 and the separately authorized auditd objects may differ.

```bash
date -u +%Y-%m-%dT%H:%M:%SZ
cat /etc/os-release
hostnamectl
uname -srm
timedatectl
sudo -n sshd -T
sudo -n ufw status verbose
systemctl is-active fail2ban
systemctl is-enabled fail2ban
sudo -n fail2ban-client status
systemctl is-active unattended-upgrades
cat /etc/apt/apt.conf.d/20auto-upgrades
sudo -n ss -tulpn
systemctl list-unit-files --type=service --state=enabled --no-pager
systemctl list-units --type=service --state=running --no-pager
systemctl list-timers --all --no-pager
getent passwd
awk -F: '$3==0 {print $1}' /etc/passwd
getent group sudo admin wheel
sudo -n sh -c 'cat /etc/sudoers /etc/sudoers.d/* 2>/dev/null'
sudo -n find /root /home -maxdepth 3 -name authorized_keys -printf '%m\n'
dpkg-query -W -f='${Package}\t${Version}\n'
python3 --version
git --version
for c in pip pip3 docker; do command -v "$c" >/dev/null 2>&1 && printf '%s PRESENT\n' "$c" || printf '%s ABSENT\n' "$c"; done
dpkg-query -W -f='${Package}\n' | grep -E '^(docker|containerd|runc|podman)' || echo NO-CONTAINER-PACKAGES
systemctl list-unit-files 'mtc-bridge*' --no-pager
test -e /etc/mtc-bridge && echo /etc/mtc-bridge PRESENT || echo /etc/mtc-bridge ABSENT
test -e /opt/mtc-bridge && echo /opt/mtc-bridge PRESENT || echo /opt/mtc-bridge ABSENT
apt-get -s dist-upgrade
df -h /
free -h
swapon --show
ls -A /opt
date -u +%Y-%m-%dT%H:%M:%SZ
```

Reserved `/opt/hermes`, `/var/lib/hermes`, `/var/log/hermes`, user `hermes`,
user `webapp`, `/opt/web`, and `/var/www` must remain absent/unmodified. Public
port 8790, any unexpected listener/service/timer/user/package, or any firewall
delta is STOP.

## R6 — verified initial-state rehearsal branch

The single branch is the Stage-3.1 tar branch above. On a masked never-started
install, `/var/lib/mtc-bridge/bridge.db` does not exist, so no WAL bundle command
is run. The archive contains the actually existing `/var/lib/mtc-bridge` and
`/etc/mtc-bridge` trees, including `install_manifest.json`.

Verified against current `deploy/linux/rollback.sh`:

- lines 57–59 require a state-manifest path and a 64-hex SHA-256;
- line 60 requires only that the supplied path is a regular file;
- lines 61–62 hash the supplied file and compare that hash;
- no code opens or parses the supplied file as JSON or requires a
  `bundle_manifest.json` schema;
- lines 103–110 explicitly handle an absent canonical database; and
- lines 157 onward write the separate rollback record.

Therefore `/home/baris/bridge-state-initial.tar.gz` satisfies the real input
contract when its measured SHA-256 is passed. This is one deterministic branch,
not a fallback chosen during the attempt.

## R7 — executable fail-closed D3 evidence contract

This section is later-D3 only and requires its separate owner sentence. It is not
part of the masked initial installation authorization.

### Persistence leg

The operator creates `~/mtcbridge-d3-evidence` for this bounded evidence window.
Each snapshot captures `ls` first, then the three exact SQLite observations and
the DB/WAL hashes. Every rc and stderr is adjudicated before comparison.

```bash
set -Eeuo pipefail
export LC_ALL=C
EVIDENCE_DIR=/home/baris/mtcbridge-d3-evidence
DB=/var/lib/mtc-bridge/bridge.db
WAL=/var/lib/mtc-bridge/bridge.db-wal
install -d -m 0700 "${EVIDENCE_DIR}"
command -v sqlite3 >/dev/null 2>&1 || {
  printf '%s\n' 'STOP: preinstalled sqlite3 CLI is required; this plan does not authorize installing it' >&2
  exit 1
}

capture_bridge_snapshot() {
  label="$1"
  sudo -n test -r "${DB}" || { printf '%s\n' "STOP: unreadable DB at ${label}" >&2; return 1; }

  set +e
  sudo -n ls -ln "${DB}" >"${EVIDENCE_DIR}/${label}.db.ls.stdout" 2>"${EVIDENCE_DIR}/${label}.db.ls.stderr"
  db_ls_rc=$?
  set -e
  test "${db_ls_rc}" -eq 0 && test ! -s "${EVIDENCE_DIR}/${label}.db.ls.stderr" || {
    printf '%s\n' "STOP: DB ls failed at ${label} rc=${db_ls_rc}" >&2
    return 1
  }

  set +e
  sudo -n ls -ln "${WAL}" >"${EVIDENCE_DIR}/${label}.wal.ls.stdout" 2>"${EVIDENCE_DIR}/${label}.wal.ls.stderr"
  wal_ls_rc=$?
  set -e
  if [ "${wal_ls_rc}" -eq 0 ] && [ ! -s "${EVIDENCE_DIR}/${label}.wal.ls.stderr" ]; then
    wal_state=PRESENT
  elif [ "${wal_ls_rc}" -eq 2 ] && sudo -n test ! -e "${WAL}" \
      && grep -qF 'No such file or directory' "${EVIDENCE_DIR}/${label}.wal.ls.stderr"; then
    wal_state=ABSENT
  else
    printf '%s\n' "STOP: WAL state is unreadable/ambiguous at ${label} rc=${wal_ls_rc}" >&2
    return 1
  fi
  printf '%s\n' "${wal_state}" >"${EVIDENCE_DIR}/${label}.wal.state"

  set +e
  sudo -n sqlite3 -batch -noheader \
    'file:/var/lib/mtc-bridge/bridge.db?mode=ro' \
    'SELECT COUNT(*) FROM orders; SELECT COALESCE(MAX(rowid),0) FROM orders; PRAGMA schema_version;' \
    >"${EVIDENCE_DIR}/${label}.sqlite.stdout" 2>"${EVIDENCE_DIR}/${label}.sqlite.stderr"
  sqlite_rc=$?
  set -e
  test "${sqlite_rc}" -eq 0 && test ! -s "${EVIDENCE_DIR}/${label}.sqlite.stderr" || {
    printf '%s\n' "STOP: read-only sqlite query failed at ${label} rc=${sqlite_rc}" >&2
    return 1
  }
  test "$(wc -l < "${EVIDENCE_DIR}/${label}.sqlite.stdout")" -eq 3 \
    && awk 'NF != 1 || $1 !~ /^[0-9]+$/ { bad=1 } END { exit bad }' \
      "${EVIDENCE_DIR}/${label}.sqlite.stdout" || {
        printf '%s\n' "STOP: sqlite observation grammar invalid at ${label}" >&2
        return 1
      }

  set +e
  if [ "${wal_state}" = PRESENT ]; then
    sudo -n sha256sum "${DB}" "${WAL}" \
      >"${EVIDENCE_DIR}/${label}.sha256.stdout" 2>"${EVIDENCE_DIR}/${label}.sha256.stderr"
  else
    sudo -n sha256sum "${DB}" \
      >"${EVIDENCE_DIR}/${label}.sha256.stdout" 2>"${EVIDENCE_DIR}/${label}.sha256.stderr"
    printf '%s\n' WAL_ABSENT >>"${EVIDENCE_DIR}/${label}.sha256.stdout"
  fi
  hash_rc=$?
  set -e
  test "${hash_rc}" -eq 0 && test ! -s "${EVIDENCE_DIR}/${label}.sha256.stderr" || {
    printf '%s\n' "STOP: sha256sum failed at ${label} rc=${hash_rc}" >&2
    return 1
  }
}

capture_bridge_snapshot before
# Execute the separately authorized refused ARM request here.
capture_bridge_snapshot after

cmp -s "${EVIDENCE_DIR}/before.sqlite.stdout" "${EVIDENCE_DIR}/after.sqlite.stdout" || {
  printf '%s\n' 'FAIL: orders count/max rowid/schema_version changed' >&2
  exit 1
}
cmp -s "${EVIDENCE_DIR}/before.wal.state" "${EVIDENCE_DIR}/after.wal.state" || {
  printf '%s\n' 'FAIL: WAL presence changed' >&2
  exit 1
}
cmp -s "${EVIDENCE_DIR}/before.sha256.stdout" "${EVIDENCE_DIR}/after.sha256.stdout" || {
  printf '%s\n' 'FAIL: bridge.db or bridge.db-wal hash changed' >&2
  exit 1
}
```

The three SQLite lines are, in order: orders count, maximum orders rowid, and
SQLite `schema_version`. An absent WAL is accepted only when `ls` returns rc 2,
the path is independently absent, and the C-locale stderr names absence. Absent
before and absent after compare equal through the `WAL_ABSENT` sentinel. Any
other missing/unreadable DB/table/tool/output is STOP, never zero/equal evidence.

### Network leg

Local verification found neither `ausearch` nor its man page, so no unverified
claim about its no-match rc is made. The wrapper below admits a no-match only as
the conjunction: rule-active proof, `ausearch` rc 1, stdout exactly
`<no matches>`, empty tool stderr, and an unchanged numeric audit lost counter.
It then writes its own explicit `NO_MATCHES` record to a normalized stderr file.
Any other shape is STOP. Requiring no connect records at all is stronger than
requiring no non-loopback connect records and avoids manual address filtering.

```bash
set -Eeuo pipefail
export LC_ALL=C
EVIDENCE_DIR=/home/baris/mtcbridge-d3-evidence
install -d -m 0700 "${EVIDENCE_DIR}"

for package in auditd libauparse0; do
  set +e
  dpkg-query -W -f='${db:Status-Status}\n' "${package}" \
    >"${EVIDENCE_DIR}/${package}.before.stdout" \
    2>"${EVIDENCE_DIR}/${package}.before.stderr"
  package_rc=$?
  set -e
  if [ "${package_rc}" -ne 1 ] \
      || [ -s "${EVIDENCE_DIR}/${package}.before.stdout" ] \
      || ! grep -qxF "dpkg-query: no packages found matching ${package}" \
        "${EVIDENCE_DIR}/${package}.before.stderr"; then
    printf '%s\n' "STOP: ${package} is not proven absent from the package database rc=${package_rc}" >&2
    exit 1
  fi
done
printf '%s\n' 'BASELINE_ABSENT=auditd,libauparse0' \
  >"${EVIDENCE_DIR}/audit-package-baseline.txt"
sudo -n env DEBIAN_FRONTEND=noninteractive apt-get -s install --no-install-recommends auditd \
  >"${EVIDENCE_DIR}/audit-install.simulation.stdout" \
  2>"${EVIDENCE_DIR}/audit-install.simulation.stderr"
test ! -s "${EVIDENCE_DIR}/audit-install.simulation.stderr" || {
  printf '%s\n' 'STOP: auditd install simulation emitted stderr' >&2
  exit 1
}
# Operator verifies the only Inst rows are auditd and libauparse0, with no Remv
# row and no upgrade; any wider transaction is STOP.
sudo -n env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends auditd
for package in auditd libauparse0; do
  package_status="$(dpkg-query -W -f='${db:Status-Status}' "${package}")"
  [ "${package_status}" = 'installed' ] || {
    printf '%s\n' "STOP: ${package} is not installed after the bounded transaction" >&2
    exit 1
  }
done
sudo -n service auditd start

set +e
MTC_BRIDGE_UID="$(id -u mtc-bridge 2>"${EVIDENCE_DIR}/id-u.stderr")"
uid_rc=$?
set -e
test "${uid_rc}" -eq 0 && test ! -s "${EVIDENCE_DIR}/id-u.stderr" \
  && printf '%s' "${MTC_BRIDGE_UID}" | grep -qxE '[0-9]+' || {
    printf '%s\n' "STOP: mtc-bridge numeric uid cannot be resolved rc=${uid_rc}" >&2
    exit 1
  }

cleanup_mtcbridge_audit_rule() {
  sudo -n auditctl -d always,exit -F arch=b64 -S connect \
    -F uid="${MTC_BRIDGE_UID}" -k mtcbridge_net || {
      printf '%s\n' 'CRITICAL: mtcbridge_net audit rule cleanup failed' >&2
      return 1
    }
}
trap cleanup_mtcbridge_audit_rule EXIT

AUDIT_LOST_BEFORE="$(sudo -n auditctl -s | awk '$1 == "lost" { print $2 }')"
printf '%s' "${AUDIT_LOST_BEFORE}" | grep -qxE '[0-9]+' || {
  printf '%s\n' 'STOP: pre-window audit lost counter is unavailable' >&2
  exit 1
}

sudo -n auditctl -a always,exit -F arch=b64 -S connect \
  -F uid="${MTC_BRIDGE_UID}" -k mtcbridge_net
sudo -n auditctl -l | grep -F mtcbridge_net \
  >"${EVIDENCE_DIR}/audit-rule-active.stdout" \
  2>"${EVIDENCE_DIR}/audit-rule-active.stderr"
test ! -s "${EVIDENCE_DIR}/audit-rule-active.stderr" \
  && grep -qF 'connect' "${EVIDENCE_DIR}/audit-rule-active.stdout" \
  && grep -qF "uid=${MTC_BRIDGE_UID}" "${EVIDENCE_DIR}/audit-rule-active.stdout" || {
    printf '%s\n' 'STOP: exact UID-scoped connect rule is not proven active' >&2
    exit 1
  }

AUDIT_START_DATE="$(date -u +%m/%d/%Y)"
AUDIT_START_TIME="$(date -u +%H:%M:%S)"
date -u +%Y-%m-%dT%H:%M:%SZ >"${EVIDENCE_DIR}/audit-window-start.utc"

# Execute the separately authorized refused ARM request here.

AUDIT_END_DATE="$(date -u +%m/%d/%Y)"
AUDIT_END_TIME="$(date -u +%H:%M:%S)"
date -u +%Y-%m-%dT%H:%M:%SZ >"${EVIDENCE_DIR}/audit-window-end.utc"

set +e
sudo -n ausearch -k mtcbridge_net \
  --start "${AUDIT_START_DATE}" "${AUDIT_START_TIME}" \
  --end "${AUDIT_END_DATE}" "${AUDIT_END_TIME}" \
  >"${EVIDENCE_DIR}/ausearch.stdout" 2>"${EVIDENCE_DIR}/ausearch.stderr"
ausearch_rc=$?
set -e
if [ "${ausearch_rc}" -eq 1 ] \
    && [ "$(cat "${EVIDENCE_DIR}/ausearch.stdout")" = '<no matches>' ] \
    && [ ! -s "${EVIDENCE_DIR}/ausearch.stderr" ]; then
  printf '%s\n' 'NO_MATCHES: ausearch rc=1; stdout exactly <no matches>; tool stderr empty' \
    >"${EVIDENCE_DIR}/ausearch.normalized.stderr"
else
  printf '%s\n' "STOP: ausearch no-match contract not met rc=${ausearch_rc}" >&2
  exit 1
fi

AUDIT_LOST_AFTER="$(sudo -n auditctl -s | awk '$1 == "lost" { print $2 }')"
printf '%s' "${AUDIT_LOST_AFTER}" | grep -qxE '[0-9]+' || {
  printf '%s\n' 'STOP: post-window audit lost counter is unavailable' >&2
  exit 1
}
test "${AUDIT_LOST_AFTER}" = "${AUDIT_LOST_BEFORE}" || {
  printf '%s\n' "STOP: audit lost counter changed ${AUDIT_LOST_BEFORE}->${AUDIT_LOST_AFTER}" >&2
  exit 1
}

sudo -n auditctl -d always,exit -F arch=b64 -S connect \
  -F uid="${MTC_BRIDGE_UID}" -k mtcbridge_net
trap - EXIT
sudo -n auditctl -l >"${EVIDENCE_DIR}/audit-rules.after-removal.stdout" \
  2>"${EVIDENCE_DIR}/audit-rules.after-removal.stderr"
test ! -s "${EVIDENCE_DIR}/audit-rules.after-removal.stderr" || {
  printf '%s\n' 'STOP: audit rule re-list emitted stderr' >&2
  exit 1
}
if grep -F mtcbridge_net "${EVIDENCE_DIR}/audit-rules.after-removal.stdout"; then
  printf '%s\n' 'STOP: mtcbridge_net rule remains after removal' >&2
  exit 1
fi

sudo -n service auditd stop
sudo -n env DEBIAN_FRONTEND=noninteractive apt-get -s purge auditd libauparse0
# Operator verifies the simulation removes exactly auditd + libauparse0 and no
# baseline package; any wider transaction is STOP.
  sudo -n env DEBIAN_FRONTEND=noninteractive apt-get purge -y auditd libauparse0
for package in auditd libauparse0; do
  set +e
  package_after="$(dpkg-query -W -f='${db:Status-Status}' "${package}" 2>&1)"
  package_rc=$?
  set -e
  if [ "${package_rc}" -ne 1 ] \
      || [ "${package_after}" != "dpkg-query: no packages found matching ${package}" ]; then
    printf '%s\n' "STOP: ${package} remains in package database rc=${package_rc}: ${package_after}" >&2
    exit 1
  fi
done
printf '%s\n' 'PACKAGE_DISPOSITION=auditd_and_new_libauparse0_purged_after_window' \
  >"${EVIDENCE_DIR}/auditd-package-disposition.txt"
```

The package disposition is deterministic only if the captured baseline proves
`auditd` and `libauparse0` were both absent and the purge simulation names no
other removal. Otherwise package cleanup is STOP and must be separately decided;
the rule is still removed by the exact trap.

## R8 — self-contained tenancy and removal boundary

### Complete admitted object list

The initial-install sentence may create or modify exactly:

1. `/opt/mtc-bridge/` (including the exact release and per-SHA venv);
2. `/etc/mtc-bridge/` (`mtc-bridge.env`, `install_manifest.json`, and the
   rehearsal-created `rollback_manifest.json`);
3. `/var/lib/mtc-bridge/`;
4. `/var/log/mtc-bridge/`;
5. Linux user `mtc-bridge` and Linux group `mtc-bridge`;
6. `/usr/local/lib/systemd/system/mtc-bridge-first-start.service`;
7. `/etc/systemd/system/mtc-bridge-first-start.service` (the `/dev/null` mask);
8. `/etc/logrotate.d/mtc-bridge`;
9. `/etc/cron.hourly/mtc-bridge-logrotate`;
10. `/home/baris/payload-be007fd8`;
11. `/home/baris/bridge-state-initial.tar.gz` and
    `/home/baris/bridge-state-initial.sha256`; and
12. the operator-side encrypted backup and restore-check directories named in
    Stage 3.3.

The later, separately authorized D3 window may additionally create exactly:

13. `/home/baris/mtcbridge-d3-evidence`;
14. the distro packages `auditd` and, only if baseline-absent and pulled by that
    exact transaction, `libauparse0`, plus their package-owned files/service;
15. one kernel audit rule exactly
    `-a always,exit -F arch=b64 -S connect -F uid=${MTC_BRIDGE_UID} -k mtcbridge_net`,
    where `MTC_BRIDGE_UID` is the uniquely resolved numeric `id -u mtc-bridge`.

Nothing in the Bridge boundary admits `/opt/hermes`, `/var/lib/hermes`,
`/var/log/hermes`, user `hermes`, `/opt/web`, `/var/www`, user `webapp`, another
user/group/service/package/container/port, a firewall change, a public listener,
or any broker/exchange/trading object.

### Exact removal command list

Run only after a failed attempt or separate removal authorization. First use the
exact rule-removal command if the D3 rule exists; then restore the package
disposition under the baseline/simulation gates above. Removal of Bridge files is
limited to the literal paths below.

```bash
set -Eeuo pipefail
export LC_ALL=C

set +e
MTC_BRIDGE_UID="$(id -u mtc-bridge 2>&1)"
uid_rc=$?
set -e
if [ "${uid_rc}" -eq 0 ]; then
  printf '%s' "${MTC_BRIDGE_UID}" | grep -qxE '[0-9]+' || {
    printf '%s\n' 'STOP: existing mtc-bridge user has no numeric uid' >&2
    exit 1
  }
elif [ "${uid_rc}" -eq 1 ] \
    && [ "${MTC_BRIDGE_UID}" = "id: 'mtc-bridge': no such user" ]; then
  MTC_BRIDGE_UID=''
else
  printf '%s\n' "STOP: mtc-bridge user state is unclassified rc=${uid_rc}" >&2
  exit 1
fi

if command -v auditctl >/dev/null 2>&1; then
  set +e
  audit_rules="$(sudo -n auditctl -l 2>&1)"
  audit_rules_rc=$?
  set -e
  test "${audit_rules_rc}" -eq 0 || {
    printf '%s\n' "STOP: audit rule inventory failed rc=${audit_rules_rc}: ${audit_rules}" >&2
    exit 1
  }
  if printf '%s\n' "${audit_rules}" | grep -Fq mtcbridge_net; then
    test -n "${MTC_BRIDGE_UID}" || {
      printf '%s\n' 'STOP: mtcbridge_net rule exists but its uid cannot be reconstructed' >&2
      exit 1
    }
    sudo -n auditctl -d always,exit -F arch=b64 -S connect \
      -F uid="${MTC_BRIDGE_UID}" -k mtcbridge_net
  fi
fi

if [ -f /home/baris/mtcbridge-d3-evidence/audit-package-baseline.txt ]; then
  grep -qxF 'BASELINE_ABSENT=auditd,libauparse0' \
    /home/baris/mtcbridge-d3-evidence/audit-package-baseline.txt || {
      printf '%s\n' 'STOP: audit package baseline marker is malformed' >&2
      exit 1
    }
  sudo -n service auditd stop
  sudo -n env DEBIAN_FRONTEND=noninteractive apt-get -s purge auditd libauparse0
  # STOP unless the simulation removes exactly the two baseline-absent packages.
sudo -n env DEBIAN_FRONTEND=noninteractive apt-get purge -y auditd libauparse0
  for package in auditd libauparse0; do
    set +e
    package_state="$(dpkg-query -W -f='${db:Status-Status}' "${package}" 2>&1)"
    package_rc=$?
    set -e
    if [ "${package_rc}" -ne 1 ] \
        || [ "${package_state}" != "dpkg-query: no packages found matching ${package}" ]; then
      printf '%s\n' "STOP: ${package} remains after purge rc=${package_rc}: ${package_state}" >&2
      exit 1
    fi
  done
else
  for package in auditd libauparse0; do
    set +e
    package_state="$(dpkg-query -W -f='${db:Status-Status}' "${package}" 2>&1)"
    package_rc=$?
    set -e
    if [ "${package_rc}" -ne 1 ] \
        || [ "${package_state}" != "dpkg-query: no packages found matching ${package}" ]; then
      printf '%s\n' "STOP: ${package} exists without the plan's baseline-absent proof" >&2
      exit 1
    fi
  done
fi

# Unit handling (owner-prescribed repair 2026-08-16): a missing unit must not
# abort cleanup; a genuine stop failure of an EXISTING unit stays fail-closed.
if sudo -n systemctl cat mtc-bridge-first-start.service >/dev/null 2>&1; then
  # Unit exists: stop must succeed; under set -e a failure aborts here loudly.
  sudo -n systemctl stop mtc-bridge-first-start.service
  sudo -n systemctl mask mtc-bridge-first-start.service
else
  printf '%s\n' "NOTE: mtc-bridge-first-start.service not installed; skipping stop/mask, continuing removal"
fi
sudo -n rm -f -- \
  /etc/cron.hourly/mtc-bridge-logrotate \
  /etc/logrotate.d/mtc-bridge \
  /etc/systemd/system/mtc-bridge-first-start.service \
  /usr/local/lib/systemd/system/mtc-bridge-first-start.service
sudo -n systemctl daemon-reload
sudo -n rm -rf -- \
  /opt/mtc-bridge \
  /etc/mtc-bridge \
  /var/lib/mtc-bridge \
  /var/log/mtc-bridge
if [ -n "${MTC_BRIDGE_UID}" ]; then
  sudo -n userdel mtc-bridge
fi
set +e
group_record="$(getent group mtc-bridge 2>&1)"
group_rc=$?
set -e
if [ "${group_rc}" -eq 0 ]; then
  sudo -n groupdel mtc-bridge
elif [ "${group_rc}" -ne 2 ] || [ -n "${group_record}" ]; then
  printf '%s\n' "STOP: mtc-bridge group state is unclassified rc=${group_rc}: ${group_record}" >&2
  exit 1
fi
rm -rf -- \
  /home/baris/payload-be007fd8 \
  /home/baris/bridge-state-initial.tar.gz \
  /home/baris/bridge-state-initial.sha256 \
  /home/baris/mtcbridge-d3-evidence
```

On the operator PC, remove the two literal EFS directories unless the owner has
explicitly chosen to retain the encrypted backup. The full-path equality checks
prevent a variable or path-resolution error from widening deletion.

```powershell
$BackupRoot = [IO.Path]::GetFullPath('C:\tmp\KVM2_BRIDGE_ENCRYPTED')
$RestoreRoot = [IO.Path]::GetFullPath('C:\tmp\KVM2_BRIDGE_RESTORE_CHECK')
if ($BackupRoot -cne 'C:\tmp\KVM2_BRIDGE_ENCRYPTED') { throw 'STOP: backup cleanup path changed' }
if ($RestoreRoot -cne 'C:\tmp\KVM2_BRIDGE_RESTORE_CHECK') { throw 'STOP: restore cleanup path changed' }
if (Test-Path -LiteralPath $RestoreRoot) { Remove-Item -LiteralPath $RestoreRoot -Recurse -Force }
if (Test-Path -LiteralPath $BackupRoot) { Remove-Item -LiteralPath $BackupRoot -Recurse -Force }
```

After removal, rerun the complete Stage-3.5 inventory and require the original
clean baseline, except for an explicitly recorded operator-side encrypted backup
that the owner chose to retain. Any retry needs a new owner sentence.

### SUBORDINATED draft sentence — NOT FOR SIGNATURE (owner repair 2026-08-16)

The single authoritative installation-authorization sentence lives in
`KVM2_DEPLOYMENT_PLAN_V6_2026-08-16.md` §3 and only that copy may be signed.
The text below is retained as the drafting source it was and has no
independent authority.

> "I authorize one attempt to transfer `~/payload-be007fd8` and perform the
> masked, never-started, credential-free DISARMED installation and read-only
> operational evidence for exact release
> `be007fd802bbfd2eb181d66038c374865d1562ee` on Hostinger KVM2
> (`srv1856225`), limited exactly to `/opt/mtc-bridge/`, `/etc/mtc-bridge/`,
> `/var/lib/mtc-bridge/`, `/var/log/mtc-bridge/`, the `mtc-bridge` user and
> group, `/usr/local/lib/systemd/system/mtc-bridge-first-start.service`, its
> `/etc/systemd/system/mtc-bridge-first-start.service` `/dev/null` mask,
> `/etc/logrotate.d/mtc-bridge`,
> `/etc/cron.hourly/mtc-bridge-logrotate`,
> `/home/baris/bridge-state-initial.tar.gz`,
> `/home/baris/bridge-state-initial.sha256`, and the named encrypted operator
> backup/restore-check directories. This authorizes payload transfer, dry run,
> one bounded install, verifier execution, the tar-hash rollback rehearsal,
> encrypted-in-transit and encrypted-at-rest backup/restore comparison,
> monitoring, and read-only re-inventory only. A later separate D3 sentence may
> additionally authorize `/home/baris/mtcbridge-d3-evidence`, installation of
> baseline-absent distro `auditd` and transaction-added `libauparse0`, and one
> exact numeric-UID `connect` audit rule keyed `mtcbridge_net`, with the rule
> removed and the packages purged under the recorded baseline/simulation gates;
> that later sentence may also authorize the temporary `auditd` service
> start/stop required for that evidence window. No Bridge service start, any
> service enable, secret, firewall change, public 8790, TESTNET or mainnet
> action, broker, ARM, order, trading action, Hermes/web identity or path, other
> user/group/service/package/container/port, or retry is authorized.
> On failure, stop, remove only the exact listed objects with the Plan V6
> commands, re-inventory to the clean baseline, and report; any retry needs a
> new sentence."
