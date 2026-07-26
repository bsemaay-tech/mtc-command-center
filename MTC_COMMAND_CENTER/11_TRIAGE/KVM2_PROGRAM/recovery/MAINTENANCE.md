# Maintenance contract

- Status: specification only; drill execution OPEN

Automatic security updates may be configured only after exact scope and
restart behavior are frozen. Automatic host reboot and automatic bridge
service restart are disabled unless separately designed, staged, audited, and
owner-approved.

Each maintenance window requires:

1. owner window and named executor;
2. bridge DISARMED and single-writer assertions;
3. accepted state/recovery artifact before change;
4. pre-change OS package, unit, config, release, venv, listener, user/group,
   disk, and service manifests;
5. exact bounded update command set;
6. post-change manifest diff and unit hash comparison;
7. one separately authorized DISARMED restart when required;
8. reconciliation and state-continuity proof;
9. rollback on drift or failure.

Package/unit/config drift, reboot, restart, reconcile gap, evidence gap,
provider-panel action, or changed service-profile hash resets or reclassifies
the monitoring window as specified by the later accepted P5-04 contract.
Changes affecting isolation require new security acceptance and lab
re-admission. The P4-07A maintenance/reboot drill remains OPEN and must run on
the exact installed candidate, once, under its own owner sentence.
