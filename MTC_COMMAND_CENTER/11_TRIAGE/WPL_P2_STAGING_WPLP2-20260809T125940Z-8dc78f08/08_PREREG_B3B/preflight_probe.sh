set -Eeuo pipefail
export LC_ALL=C
printf 'PROBE_BEGIN purpose=resolve_service_account_name_to_numeric_ids readonly=yes\n'
printf 'PROBE_passwd %s\n' "$(getent passwd mtc-bridge || echo ABSENT)"
printf 'PROBE_group %s\n'  "$(getent group mtc-bridge || echo ABSENT)"
for p in /var/lib/mtc-bridge /var/log/mtc-bridge /etc/mtc-bridge; do
    printf 'PROBE_stat %s\n' "$(stat -c '%n uid=%u gid=%g owner=%U:%G mode=%a' -- "$p" 2>&1)"
done
printf 'PROBE_unit_identity %s\n' "$(grep -E '^(User|Group)=' /usr/local/lib/systemd/system/mtc-bridge-first-start.service 2>&1 | tr '\n' ' ')"
printf 'PROBE_END\n'
