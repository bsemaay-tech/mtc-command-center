# RP7 cap-override Codex T0 Lead adjudication — 2026-08-15

Status: **BLOCK / OWNER BOUNDARY**. This is the Lead adjudication of the fresh
Codex T0 slot only. It is not combined T0 acceptance. The required Claude slot
is still pending after a quota-only interruption and is scheduled after the
04:50 Europe/Chisinau reset.

## Frozen subject and auditor identity

- Frozen subject commit: `2d0f24d0965c4ba7e7942dddac4fcac3bbb3240b`.
- Filled prompt commit: `d4e90cb05bfbe227d17ce6264f0d3c19d3b5337f`.
- Auditor launch: fresh ephemeral `gpt-5.6-sol`, effort `xhigh`, isolated clean
  worktree `C:\R7AX`, verdict-file-only write authority.
- Auditor verdict: `BLOCK`.
- Original isolated verdict identity: 7041 bytes / SHA-256
  `6D78C44D906558FD9F8BBC82A0F5C6C7EEAA383D2DC5B7213A3CA884C2ACCF35`.
  The durable repository copy has one repository-final newline added: 7042
  bytes / SHA-256
  `39DEAB0DCBA11CCD4131A1B0C15FB7ECDA3EA17D14A9D8D012505CAB5FE3333E`.
- Audit-attributable isolated-worktree delta: exactly the Codex verdict file.

## Lead adjudication

### Transport/execution BLOCK — ACCEPTED AS BLOCK, not a source finding

The Codex sandbox could not see the local Ubuntu WSL distribution and received
`Wsl/Service/WSL_E_DISTRO_NOT_FOUND`, so it could not execute the mandatory
systemd-backed fence. Outside that audit sandbox, the Lead rechecked that Ubuntu
and `docker-desktop` are installed and had independently executed the complete
fence against the frozen candidate at rc 0 in 124.8 seconds. Therefore this is
an audit-route limitation, not evidence that the candidate fence fails. Under
the T0 execution rule, however, non-execution is still `BLOCK` and cannot fill
an accepting flagship slot.

### REQUIRED-1 — ACCEPTED / REPRODUCED

The row-9 D026 mid-name quote arm bypasses the production observation boundary.
The real caller obtains `Environment` from `systemctl show` and passes the
effective property value to `wpi_assert_environment_start_mode`
(`RP7-WPI-RO.sh:917-946`). The repaired parser rejects the raw spelling
`MTC_BRIDGE"_START_MODE=...` but accepts the normalized clean spelling; the
Lead's complete-fence run reproduced those exact dispositions. The production
comment itself records that systemd removes the quote before storing the
spliced target name. Feeding the raw pre-normalization spelling directly into
fake `systemctl show` output therefore does not prove that production can reject
the attack. The required D026 claim is not closed.

### REQUIRED-2 — ACCEPTED / REPRODUCED

The frozen provenance package is internally contradictory. `STATUS_RP7.md` and
the report's current prose record the 2026-08-15 Lead run, while
`SELF_QA_RP7.md:10-11` and `:1050-1053` still say no Lead run exists; the
report's earlier current-identity block still contains
`independent_lead_run=none_yet_against_these_bytes`. These are mutually
exclusive statements in the same frozen package.

### REQUIRED-3 — ACCEPTED / REPRODUCED

The dispatched audit contract requires **exact transcript reproduction**. The
package explicitly records only 155/156 normalized lines matching and excludes
the run-varying `HARNESS_ATTESTED_MOUNTINFO sha256=` line; raw paths also vary
by design. The variation is explained, but the contract contains no such
exception. The frozen candidate therefore does not satisfy the exact condition
as dispatched. A future authorized cycle must either emit a deterministic
canonical transcript while retaining run-owned scratch isolation or explicitly
ratify the allowed normalization/exclusion before dispatch.

## Boundary

All three required findings reproduce on the frozen source/evidence contract.
The single owner-authorized RP7 cap-override repair has already been consumed;
no further RP7 repair/audit cycle is authorized. Do not modify or re-audit the
candidate beyond completing the already-required Claude T0 detection slot.
After that slot, return the combined non-acceptance and required findings to the
owner for a new decision. All host, deployment, credential, service, broker,
ARM, order, TESTNET, mainnet, Pine, parity, MTC, and trading gates remain closed.
