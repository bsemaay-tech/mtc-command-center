# Access recovery and external dependencies

- Status: design only; owner/provider details remain OPEN

The host uses key-only SSH, root login disabled, and an SSH-only inbound
firewall. Recovery must not depend on one powered-on PC or one untested
credential.

Before execution, the owner must record without private identifiers:

- primary and secondary SSH public-key custody roles;
- provider-panel account ownership, MFA, and emergency-console procedure;
- a second-device recovery test;
- who can revoke/replace an access key;
- backup-provider ownership and separately held recovery credential;
- DNS/domain/certificate inventory, or explicit `NONE`;
- expiry, billing, quota, and renewal alert owner for any admitted external
  service.

Provider-panel snapshot, restore, reboot, firewall, or service action while the
bridge is deployed is forbidden without a separate authorization. Any such
action resets/reclassifies the monitoring window; unexplained action invokes
the master stop rule.

No key path, host, IP, username, connection command, credential value, or
provider account identifier is stored here.
