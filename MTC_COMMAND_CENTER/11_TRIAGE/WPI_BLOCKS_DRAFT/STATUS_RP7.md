# RP7 status

Status: **AUTHORED-PENDING-AUDIT**

Scope: `RP7-WPI-RO.sh` implements the remote RO-stage predicates for rows
10–23 and enforces row 24's domain boundary without falsely probing it from the
remote shell. Row 24 remains operator-side transport op 06, exactly as the
binding preregistration orders it.

Row → implementation map (one line): **10 → `wpi_assert_tree(release)`; 11 → `wpi_assert_tree(venv)`; 12 → `wpi_run_find` budget adjudication; 13 → `wpi_run_find` rc/diagnostic adjudication; 14 → `wpi_assert_tree` NUL-path parser; 15 → `wpi_assert_metadata_dir`; 16 → `wpi_validate_inputs` plus mandatory Stage-1 static path-scope proof; 17 → `wpi_assert_regular_digest`; 18 → `wpi_assert_interpreter`; 19 → `wpi_assert_metadata_readable` then `wpi_assert_lock_parity`; 20 → `wpi_assert_status` HTTP gate; 21 → `wpi_assert_status` strict-JSON gate; 22 → `wpi_assert_netns_binding` then `wpi_assert_listener_set`; 23 → `wpi_assert_listener_set` non-loopback rejection; 24 → `wpi_record_external_probe_boundary` (operator op 06, not evaluated remotely).**

No host contact, network probe, SSH/SCP, RUNID minting, commit, or change
outside the three RP7 deliverables occurred.
