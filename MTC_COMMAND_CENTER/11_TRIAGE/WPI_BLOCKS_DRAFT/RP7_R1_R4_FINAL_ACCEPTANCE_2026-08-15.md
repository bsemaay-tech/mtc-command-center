# RP7 rows 1-9 R1-R4 final acceptance — 2026-08-15

Status: **ACCEPTED — DUAL T0 FLAGSHIP FLOOR SATISFIED**.

This is the Lead's combined disposition for the single owner-authorized R1-R4
repair cycle. It closes RP7 rows 1-9 on the frozen candidate bytes below. It
does not accept Pathscope, authorize Stage 1, or open any host or trading gate.

## Frozen subject

- Candidate commit: `80cbed461d0b0371e6eabbfff0e732e5001affaf`.
- Audit-contract commit: `4d28debbc69f35d21c022fd314309aa052e3a4aa`.
- Branch: `codex/rp7-r1-r4-repair-20260815`.

| artifact | bytes | SHA-256 |
|---|---:|---|
| `RP7-WPI-RO.sh` | 137981 | `4caed4aecc91cada3b8b99f8ff06d7ba0d7376b2bc07e92c298f4a7b7ca0900c` |
| `SELF_QA_RP7.md` | 585132 | `b1031cc5e71f2a19e05a400a0d3754b9cf37b5917848868e61ae0764a5b1c8ae` |
| `STATUS_RP7.md` | 19165 | `f1fbe2e1d8381b2c5d762e6c69fff2718b7f90ae8d09e8b32d1947fab8ea5a46` |
| `RP7_ROWS_1_9_REPORT_2026-08-13.md` | 54481 | `0a434a98393a6c8ecf41a01d6696326c814c44bf69a5d51734f1b44cbe738c46` |

## Mandatory T0 results

| slot | exact execution | verdict | durable verdict identity |
|---|---|---|---|
| Codex | fresh isolated `gpt-5.6-sol`, `xhigh`, exit 0 | **PASS** | 9727 bytes, SHA-256 `3a70ecda92db20eb7ea4b317d4d06b24554ba3aad99ca2d96b7dc2d53ab8d1b4`, Git blob `e2ad8edfefc08bbd174c8d979e84fda2230aaf47` |
| Claude | fresh isolated `claude-opus-5`, `xhigh`, exit 0 | **PASS-WITH-NITS** | 38057 bytes, SHA-256 `e480c5dd097fef883783722fca0ced60389a35242889058b44c3ac1d6cce367e`, Git blob `7358d8cb65811c71a702da3a1f62ac9449f037b6` |

The Codex process used the isolated fourth account and its JSONL ended with
`turn.completed`; the command line selected `gpt-5.6-sol` with
`model_reasoning_effort=xhigh`. Claude's successful result records canonical
model `claude-opus-5`; the launcher command line supplied `--effort xhigh`, with
no resume/continue and no session persistence. Claude telemetry listed a
22-output-token Haiku utility call; it did not write the verdict or fill an
auditor slot.

Each auditor wrote only its kickoff-named verdict file. Neither read the other
same-round verdict before sealing its own. Both verdict files were copied into
this branch only after both processes exited.

## Lead adjudication

The Lead independently inspected the repaired diff and reproduced the complete
rows-1-9 fence twice before dispatch. Both runs returned rc 0, 250 lines, zero
stderr, and the same 54284-byte published transcript with SHA-256
`d0788122c132e43c25aea52315d53b3596c40c57598e2bbded9b2efa11cae8ab`.
The raw transcripts and internal scratch/mount identities differed, proving
that deterministic publication did not reuse runtime state.

Both auditors then independently executed the mandatory fence twice from exact
Git-object materializations. They reproduced closure of all four required
findings:

1. R1: row 9 is bound to the real manager-normalization and row-7 source
   attestation boundary; the raw mid-name quote attack cannot false PASS.
2. R2: the three chronology tables are coherent and byte-identical, with no
   premature auditor or Lead claim.
3. R3: published transcripts are exactly reproducible while hidden runtime
   identities remain live, different, re-derivable, and fail closed under
   falsification.
4. R4: bare-CR, multi-CR, CR-only, and adjacent terminator behavior follows the
   live systemd oracle; the prior false PASSes are RED on old bytes and GREEN on
   the repaired bytes under D026.

Codex found no nit. Claude recorded six optional nits: qualifier clarity on
single-subject counts, oracle naming in canonical output, asymmetric line
matching, implementer-run attribution wording, retained binding-record depth,
and one conservative NUL STOP. None is a required repair and none contradicts
the predicates or acceptance evidence. They are backlog only; changing the
accepted bytes to address them would reopen T0 and is not part of this consumed
cycle.

## Final disposition and remaining boundary

RP7 rows 1-9 at candidate `80cbed46` are **T0 accepted**. The earlier
`RP7_CAP_OVERRIDE_FINAL_OWNER_BOUNDARY_2026-08-15.md` remains a truthful
historical record for the rejected 132886-byte candidate; it is superseded for
current RP7 disposition by this record and the 137981-byte accepted candidate.

WP-I Stage-1 freeze is still not reachable because Pathscope's final authorized
T1 audit ended in a transport `BLOCK` without execution. That Pathscope cycle is
exhausted and must not be rerun without a new explicit owner decision.

> **[correction 2026-08-15, later the same day]** The paragraph above was true
> when written and is now superseded on its Pathscope facts only. Barış
> authorized one fresh execution-audit **retry** because the previous attempt
> never executed. That retry ran under `sandbox: danger-full-access` and
> returned **REQUEST_CHANGES** with three REQUIRED findings — it did not end in
> a transport block. Pathscope remains NON-ACCEPTED and its lane is stopped at
> the owner boundary pending one of Options A-D. See
> `WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md`,
> `.../PATHSCOPE_OWNER_BOUNDARY_2026-08-15.md`, and
> `.../PATHSCOPE_DECISION_OPTIONS_2026-08-15.md`. **The RP7 disposition recorded
> in this file is unaffected**; RP7 rows 1-9 stay T0 accepted at `80cbed46`.

Packet 10
still needs the frozen-SHA Bridge-suite execution; Packet 11 remains partial;
Packet 9 and freeze-time bindings remain downstream of an accepted Pathscope and
the Stage-1 allocation/fill sequence.

No host, deployment, credential, service, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, or economic action was authorized or
performed by this acceptance.
