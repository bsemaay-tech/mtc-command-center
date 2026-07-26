# Incident and contamination response

## Resource or SLO breach

Stop/disable only the newest optional lab workload, preserve evidence, compare
bridge assertions, notify the owner, and block further admission. Automation
must not restart, DISARM, ARM, reconcile, deploy, or modify bridge state.

## Security-boundary breach

If a lab process reaches a bridge secret/state/path/control route, service bus,
privileged socket, kernel trust surface, or credential store:

1. kill all lab workloads;
2. preserve evidence without mutation;
3. mark the host `CONTAMINATED`;
4. notify the owner immediately;
5. perform human-controlled DISARM and containment under separate authority;
6. revoke and rotate every TESTNET credential by name;
7. prohibit bridge resume/ARM;
8. require destructive trusted reprovision or migration to a separately clean
   bridge host.

## Provider-panel action

Any provider-panel snapshot, restore, reboot, firewall, or service action while
the bridge is deployed resets/reclassifies P5-04 monitoring. An unexplained
action invokes the global stop rule and is treated as a possible boundary
incident until resolved.

## Evidence and drill

Record UTC time, classification, sanitized event summary, restricted raw
logical ID, hashes, responsible roles, containment, credential-name actions,
recovery decision, and retry history. Do not record private identifiers or
secret values. The required tabletop incident drill and hashed outcome remain
OPEN.
