# KICKOFF — Codex T0 audit: RP7-WPI-RO round 9 (OUTPUT-HYGIENE)

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR of record, fresh session. Read-only:
edit nothing except your verdict file, no git mutation, no host, no network. T0 surface.

## OUTPUT-HYGIENE (prior security-fixture audits were content-filter-killed)
The round-9 D026 fixtures drive a real caller that writes files and simulates a curl body
overwrite + a body-swap — attack-shaped. When you run the fence, redirect its output to files;
in your own output quote only SUMMARY/marker lines (`QA_PASS`, `BODY_BINDING mode=... rc=...`,
`BIND_RC ...`, `RC137_PROVENANCE ...`, `NETNS_DETAIL ...`, `BYTE_IDENTITY ...`). Refer to the
attacks by name (`outside-overwrite`, `body-swap`, `rc-spoof`), never reproduce the attack
shell or the curl invocation in your own text. Do NOT author new attack fixtures — run the
published fence, which extracts its own arms from its own heredocs. Verdict + findings FIRST.

## Bytes under audit — commit `9f597117`

`RP7-WPI-RO.sh` round-9 SHA-256
`0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62`, 108301 B (was 99903 at
round 8 `11621044…`). `SELF_QA_RP7.md`, `STATUS_RP7.md`, `RP7_REPAIR_R9_REPORT.md`.

## Your round-8 findings (BLOCK: 5)

`RP7_CODEX_T0_AUDIT_R8_PART_B_2026-08-11.md` — F1 (BLOCK): `ro.status.body` was both an
outside-tree write primitive and a false-PASS primitive (name not bound to the created leaf);
F2 (row-22 fence prevented the child it claimed to test, false rc 0); F3 (wrapper stream
writable by the bounded body); F4 (carried assertion mapping); F5 (netns detail).

## Round-9 dispositions (Lead ran the R9 fence VERBATIM: `QA_PASS all_assertions=yes`, rc 0,
stderr 0 bytes)
- **F1 → repaired by design change.** `BODY_BINDING`: RED (r8) mode=outside rc 0
  `outside_is_original=no` (outside file overwritten) + mode=reader rc 0 (body-swap accepted);
  GREEN mode=outside rc 3 `outside_is_original=yes` (STOP, outside untouched) + mode=reader
  rc 1 (`B5_FAIL flag_mismatch`, swap caught). The fetched body is bound to the created object.
- F2 → `BIND_RC`: divert modes STOP rc 3, undeclared STOPs, clean rc 0. F3 → wrapper stream
  unwritable by the bounded body. F4 → per-fence mapping, auditor's mutant is the RED (lives in
  the round-6 fence). F5 → `NETNS_DETAIL` green carries `detail_field_present=1` + diagnostic
  file. Two items carried as STATED LIMITATIONS, named in the QA.

## Audit contract
1. Run the published RP7 r9 fence VERBATIM (`SELF_QA_RP7.md` §"Exact command" — the
   `RP7_EXACT_COMMAND` block, and/or the individual `RP7_R9_FENCE`); output to files; quote only
   the marker/summary lines. It is slow (per-fence 900s timeouts, real children) — allow time.
   Confirm `QA_PASS all_assertions=yes` and the RED/GREEN vectors above. Non-execution ≠
   acceptance (D025 r1); confirm each RED is real prior-bytes execution (D026).
2. **F1 is the BLOCK — verify it by outcome, not claim:** confirm the repaired block binds the
   fetched body to the created leaf (curl writes to an inherited descriptor or verifies object
   identity after fetch and STOPs on mismatch), so neither the outside-overwrite nor the
   body-swap can produce an accepting result. A disclosure is not a control.
3. Judge the two carried STATED LIMITATIONS: are they honestly scoped, or do they leave a
   reachable false-PASS?
4. 13 defect patterns (`../DESIGN_DEFECT_PATTERNS_2026-08-10.md`). Verdict: PASS /
   PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.

Write ONE new file: `RP7_CODEX_T0_AUDIT_R9_2026-08-11.md`.
