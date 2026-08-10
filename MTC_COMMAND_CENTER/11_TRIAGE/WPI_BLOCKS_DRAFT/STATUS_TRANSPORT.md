# WP-I transport set status

**AUTHORED-PENDING-AUDIT**

No host contact, RUNID allocation, archive build, freeze, execution, or Git
commit was performed. `<ALLOCATE-AT-DISPATCH>` and `<PIN-AT-FREEZE>` remain
literal and intentionally make the draft runner STOP before starting a process.

Op → implementation: 01 `remote_setup_wpi.sh`; 02 pinned `runkit.tar` SCP up;
03 `remote_extract_verify_wpi.sh`; 04 `run_p0.sh`; 05 `run_ro.sh`; 06 bounded
operator-side `tcp_probe`; 07/08 accepted byte-identical `remote_close_tree.sh`;
09/10 SCP down; 11/12 local-only remote/local digest-set binding in
`transport_runner.ps1`.

Self-QA: Bash syntax PASS; Windows PowerShell 5.1 parse PASS; wrapper symlink
and stdin RED/GREEN PASS for both wrappers; P0/system-manager and RO/partial-walk
STOP propagation PASS; TSV clean/unterminated/read-error cases PASS; first-FAIL
RED/GREEN PASS with all `always` ops retained; loopback probe refused/connected/
not-evaluable classifications PASS; setup/extractor derivation RED/GREEN PASS.
See `SELF_QA_TRANSPORT.md` for commands, real output, diffs, bytes, and SHA-256.
