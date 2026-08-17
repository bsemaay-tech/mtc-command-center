# Lead independent verification — RP7 round-4 Codex finding 1

Date 2026-08-10, ~20:15 local. Lead session, Git Bash on the workstation. Read-only with
respect to the repository: the fixture ran entirely inside a `mktemp -d /tmp/rp7-main-bind.XXXXXX`
tree that it removed on exit. No host contact, no network, no repository file edited.

## Why this was run

Round 5 was about to be dispatched on the strength of a single auditor's claim. A finding
that drives a repair round is verified by the Lead before it becomes binding scope. Codex's
finding 1 asserts that the production `wpi_main` binding loop omits `python3`, so the
executable that produces both accepting adjudicator claims is never bound.

## What was run

Codex's published finding-1 fixture, byte-for-byte, against the current round-4 bytes
(`RP7-WPI-RO.sh`, 70941 B, SHA-256
`23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad`). The fixture sources
the real block with only the trailing `wpi_main "$@"` line removed, keeps `wpi_main`, the
capture path, the stream-shape checks and the acceptance logic real, no-ops the unrelated
row functions, and instruments `wpi_bind_tool` so that a genuine `python3` binding would
STOP the run.

Script as executed is preserved at the Lead's scratchpad
`scratchpad/rp7_f1_red.sh` and is identical to the block quoted in
`RP7_CODEX_T0_AUDIT_R4_2026-08-10.md` finding 1.

## Result — RED reproduced exactly

```text
B5_status http=200 json=strict required_fields=8 flags=expected
  body_sha256=8d3962231270c4a4099e67316f9ab15aad67dd86425feab010c00ad3b47e5360
  content=not_printed parser=pinned_system_interpreter isolation=isolated_no_site
RP7_claim establishes=rows_10_23_read_only_predicates_with_attested_preexec_objects_and_service_network_domain;...
RP7 PASS
MAIN_BIND_FALSIFICATION rc=0 bound=[stat,readlink,env,find,sha256sum,systemctl,ss,curl,timeout,]
  python3_bound=no malicious_marker=present accepted_status=1 rp7_pass=1
```

Fixture rc 0. The instrumented `wpi_bind_tool` was never called with `python3`
(`python3_bound=no`), the deviant executable wrote its marker (`malicious_marker=present`),
the block printed `parser=pinned_system_interpreter isolation=isolated_no_site`, and the
run ended `RP7 PASS`.

## Lead conclusion

Finding 1 is confirmed on the real bytes by independent execution. It is binding scope for
round 5, and its GREEN must be produced by a fixture that instruments the **real** caller —
the same instrumentation used here — not by a redeclared tool list.

Findings 2 and 3 are accepted as scope on Codex's executed evidence; finding 3 is
additionally visible by inspection (`SELF_QA_RP7.md:26-30` publishes "Exact command" as
prose plus a fence rather than a literal runnable command).
