#!/bin/sh
# FROZEN V3 provisioning sequence — NOT to be executed until the owner's separate
# exact KVM2 application approval. Run as root, with a SECOND root session held
# open for the entire window (rollback lifeline). Stop on any failure.
set -eu
umask 022

# 1. account
/usr/sbin/useradd --system --create-home --home-dir /home/mtc-watch --shell /bin/sh mtc-watch
/usr/bin/passwd -l mtc-watch

# 2. forced-command script
/usr/bin/install -o root -g root -m 0755 mtc-watch-collect /usr/local/bin/mtc-watch-collect

# 3. authorized key (template must already carry the owner-supplied pubkey)
/usr/bin/install -d -o root -g root -m 0755 /etc/ssh/authorized_keys.d
/usr/bin/install -o root -g root -m 0644 authorized_keys.mtc-watch /etc/ssh/authorized_keys.d/mtc-watch

# 4. sshd drop-in — sshd -t MUST pass before reload; reload (never restart)
/usr/bin/install -o root -g root -m 0644 70-mtc-watch.conf /etc/ssh/sshd_config.d/70-mtc-watch.conf
/usr/sbin/sshd -t
/usr/bin/systemctl reload ssh

# 5. log ACLs (exact files only; default ACL covers rotated files)
/usr/bin/setfacl -m u:mtc-watch:rx /var/log/mtc-bridge
/usr/bin/setfacl -m u:mtc-watch:r  /var/log/mtc-bridge/bridge.log /var/log/mtc-bridge/bridge.err.log
/usr/bin/setfacl -d -m u:mtc-watch:r /var/log/mtc-bridge

# 6. backup system
/usr/bin/install -o root -g root -m 0755 mtc-bridge-backup /usr/local/sbin/mtc-bridge-backup
/usr/bin/install -o root -g root -m 0644 mtc-bridge-backup.service /etc/systemd/system/mtc-bridge-backup.service
/usr/bin/install -o root -g root -m 0644 mtc-bridge-backup.timer   /etc/systemd/system/mtc-bridge-backup.timer
/usr/bin/systemctl daemon-reload
/usr/bin/systemctl enable --now mtc-bridge-backup.timer

# 7. acceptance: run tests_T (from Windows), one manual backup run + tests_B, then tests_W.
echo "PROVISIONED. Now run the T/B/W matrices before the watcher may use the account."

# ROLLBACK (manual, from the held session):
#   rm -f /etc/ssh/sshd_config.d/70-mtc-watch.conf /etc/ssh/authorized_keys.d/mtc-watch
#   /usr/sbin/sshd -t && /usr/bin/systemctl reload ssh
#   /usr/bin/systemctl disable --now mtc-bridge-backup.timer
#   confirm normal login from a second session; record.
