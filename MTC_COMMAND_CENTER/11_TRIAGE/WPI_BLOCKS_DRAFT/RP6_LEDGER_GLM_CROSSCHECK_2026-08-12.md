# RP6 half of the freeze-input ledger — GLM-5.2 cross-check (2026-08-12)

> Distinct from the sibling file `RP6_GLM_ADVANCE_READ_AUDIT_2026-08-12.md`
> (the prior RP6-11 `eval`/dynamic-target advance read-audit). That file is a
> different audit's verdict and was left untouched. This file cross-checks only
> the **RP6 claims in `WPI_FREEZE_INPUT_LEDGER_2026-08-12.md`** — the unverified
> half (transport and RP7 halves were already independently cross-checked by the
> two sibling GLM advance read-audits in this directory).

## Verdict: ADVANCE-SUPPLEMENTAL, PASS-WITH-NITS (source-level). Zero required repairs.

The RP6 half of `WPI_FREEZE_INPUT_LEDGER_2026-08-12.md` is **substantively
accurate**. Its single most consequential claim — that RP6 cannot produce an
end-to-end P0 PASS while the freeze literals remain, and that the Codex r16
acceptance was therefore a source/audit acceptance rather than a host
end-to-end PASS — **holds under independent byte re-derivation**. The Lead's
spot-check discrepancy ("27 occurrences of `PIN-AT-FREEZE`, not 17") is **not a
defect**: 17 and 27 are both correct counts of different things. The one genuine
defect is a **stale line citation** (`STATUS_RP6_P0.md:311-312`), which the
kickoff explicitly anticipated ("round 17 added content and the Lead corrected
the status file after the ledger was written").

I am GLM-5.2 via the Z.AI route, running unattended and read-only. I created only
this verdict file. No git mutation, no host contact, no network, no block-byte
edit, no overwrite of any existing file.

## Scope and method

I re-derived every RP6-relevant claim from current local bytes, not from the
ledger or any report. Sources read: `WPI_BLOCKS_DRAFT/RP6-P0.sh`,
`WPI_BLOCKS_DRAFT/run_p0.sh`, `WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md`,
`WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_R16_2026-08-12.md`, and the ledger itself.
Tools used: targeted `grep`, full/offset `Read`, and `sha256sum`/`wc` for
identity.

**Byte identity (my own `sha256sum` + `wc -l`):**

- `RP6-P0.sh` → `5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`,
  1896 lines. Matches the ledger anchor (ledger line 11) **and** the r16 audit
  (`RP6_CODEX_T0_AUDIT_R16_2026-08-12.md:174-176`). This hash is unchanged since
  r16, which means **round 17 did not modify `RP6-P0.sh`** — so the ledger's
  `RP6-P0.sh` line citations were expected to be stable, and (below) they are.

## The consequential claim (ledger §Blocker 7, lines 82-88) — CONFIRMED

The ledger claims: with current bytes RP6 cannot produce an end-to-end P0 PASS
because 17 `<PIN-AT-FREEZE>` literals remain; the wrapper defines the five
attested values as markers, exports them, prints the attestation line on
placeholders, then sources RP6, which refuses the markers. Every link in that
chain is byte-verified.

**Premise A — 17 freeze-input literals are present.** My `grep` of `RP6-P0.sh`
finds exactly **17 distinct `P0_FIXED_*` definitions set to `'<PIN-AT-FREEZE>'`**:

| Range | Literals | Count |
|---|---|---:|
| `:266-270` | `P0_FIXED_ATTESTED_{USER,MNT,PID,NET}_NS`, `P0_FIXED_ATTESTED_ROOT_MOUNT_ID` | 5 |
| `:278` | `P0_FIXED_TRUSTED_PYTHON` | 1 |
| `:289-299` | `P0_FIXED_{STAT,READLINK,ENV,FIND,SHA256SUM,SYSTEMCTL,SS,CURL,TIMEOUT,ID,GETENT}` | 11 |
| | **Total** | **17** |

This triple-reconciles: the raw byte count (17 definitions), the status-file
text `freeze_gate_literal_count=17 (12 tool pins + 5 attestation values)`
(`STATUS_RP6_P0.md:274,572,809,996,1166,1287,1387`), and the decomposition
(12 tool pins = trusted Python + 11 tool binaries; + 5 attested = 17). The
status file counts the trusted-Python literal as one of the "12 tool pins"; the
ledger's "12-entry P0 map: 9 RO-shared + python3 + id + getent" (ledger line
115) is the same 12. All three agree.

**Premise B — the fence refuses unfilled markers.** `RP6-P0.sh:707-718`
(`p0_validate_attested_ns_input`) tests `[ "$value" != '<PIN-AT-FREEZE>' ] ||
p0_stop …` at `:709`; the root-mount marker check is at `:724`; the five
`P0_FIXED_ATTESTED_*` unfilled checks are at `:733-742`. These `p0_stop` calls
exit non-zero (the wrapper's `p0w_stop` exits 3). So with marker values in hand,
RP6 **STOPs before any PASS evidence line**. (This is the same fence the kickoff
notes a prior advance read-audit *falsely* claimed was bypassable via a
variable-mutating `eval`; the fence does not resolve or mutate — it compares and
stops. The eval-class question is outside this cross-check's scope; see the
sibling `RP6_GLM_ADVANCE_READ_AUDIT_2026-08-12.md`.)

**Premise C — the wrapper hands RP6 exactly those markers.** Verified in
`run_p0.sh`: the five `P0_ATTESTED_*` are defined as `'<PIN-AT-FREEZE>'` at
`:151-155`; exported at `:237-240`; the attestation line is printed on the
still-placeholder values at `:241-243`; RP6 is sourced at `:245`. RP6 consumes
those exported values via the presence checks at `RP6-P0.sh:691-700` and the
validation at `:707-752`.

A∧B∧C ⇒ RP6 cannot PASS end-to-end on current bytes. The claim is proven by
reasoning from the bytes, not asserted.

## The r16 characterization (ledger line 88) — CONFIRMED

The ledger says the r16 acceptance was "a source/audit acceptance, not a host
end-to-end P0 PASS," citing `RP6_CODEX_T0_AUDIT_R16_2026-08-12.md:1` and
`:23-26`. Verified:

- `:1` is `VERDICT: PASS-WITH-NITS`.
- `:23-26` are the five static harness summaries (`R16_GRAMMAR`,
  `R16_F1_RED`, `R11_GUARDS`, `R10_F4_QA` all `PASS`; `R9_GRAMMAR` an
  intentional `FAIL`/RED).
- The audit explicitly states "No host, namespace, service, or privilege-domain
  observation was made" (Pattern 2, `:159-161`) and "grants no freeze,
  dispatch, host, deployment, credential, broker, exchange, ARM, order, or
  trading authority" (`:183-185`). It closes "only the Codex flagship slot for
  the round-16 **census hardening** cycle."

So r16 was always a static census/grammar QA and never claimed to be a host
end-to-end P0 PASS. The ledger's framing is accurate and fair — it is
classifying r16 correctly, not accusing it of overclaiming (the status file
itself repeatedly says "no end-to-end `P0 PASS` is possible … nothing here is
dispatchable," e.g. `STATUS_RP6_P0.md:396-397,670-671,883-884,1059-1060` and
~7 more). The ledger and the status file agree; r16 agrees about its own scope.

## The 17-vs-27 "discrepancy" — RESOLVED, not a defect

The Lead's spot-check found **27 occurrences** of `PIN-AT-FREEZE` in `RP6-P0.sh`;
the ledger/status file say **17**. Both are correct:

- **17** = distinct freeze-input literal **definitions** (the table in Premise A).
- **27** = total raw string **occurrences** = 17 definitions + **10 fence/guard
  occurrences** that are not freeze inputs but the enforcement logic and its
  comments.

The 10 fence occurrences (my own grep): `:607` (comment), `:615` (pin-unfilled
check), `:645` (comment), `:709` (marker check), `:724` (root-mount marker
check), `:733, :735, :737, :739, :741` (the five `P0_FIXED_ATTESTED_*` unfilled
checks). 17 + 10 = 27.

The ledger's phrase "17 remaining `<PIN-AT-FREEZE>` literals" uses "literals" to
mean *freeze-input value definitions still set to the marker* — which is exactly
the set that must be filled before freeze. That is the correct count for its
purpose. The 10 fence occurrences are the *opposite* of a problem: they are the
load-bearing guard that makes "17 unfilled ⇒ no PASS" true. Resolved as
**distinct-definitions (17) vs total-occurrences (27)**; neither count is wrong
and they do not contradict.

## The one genuine defect — stale status-file line citation (NIT)

The ledger (line 88) cites `STATUS_RP6_P0.md:311-312` for the "17 literals ⇒ no
end-to-end P0 PASS" statement. That line range **no longer holds the claim** —
round 17's added content and the Lead's status-file correction shifted it. The
canonical statement is now at `STATUS_RP6_P0.md:396-397` and recurs at
`:670-671, :883-884, :1059-1060, :1214-1215, :1333-1334, :1420-1421, :1499-1500,
:1563-1564, :1652-1653`; the count field is at `:274` (and recurs). **Claim
content: true and present. Cited line number: stale.** This is the drift the
kickoff told me to expect, and it is the only substantive documentation defect
in the RP6 half. Recommended fix (optional, low): repoint the citation to
`STATUS_RP6_P0.md:396-397` (or `:274` for the count).

## RP6-P0.sh consumer line citations — all verified against current bytes

Every `RP6-P0.sh` line range the ledger cites was checked against current bytes
and is accurate (the file is hash-unchanged since r16, so this is expected):

| Ledger claim | Cited range | Byte content I verified |
|---|---|---|
| Requires all five wrapper values (presence) | `:691-700` | `[ -n "${P0_ATTESTED_*:-}" ] \|\| p0_stop …` for all 5 ✓ |
| Rejects unfilled marker + malformed grammar | `:707-724` | `p0_validate_attested_ns_input` → `!= '<PIN-AT-FREEZE>'` + grammar; root-mount check ✓ |
| Embedded-literal / wrapper equality | `:733-752` | 5× `P0_FIXED_*` unfilled check + 5× `P0_ATTESTED_* = P0_FIXED_*` ✓ |
| Live namespace reads vs attested | `:1390-1393` | four `p0_read_domain_ns … "$P0_ATTESTED_*_NS"` calls ✓ |
| Canonical root-mount identity compare | `:1394-1414` | readlink `-f /` = `/`, stat `%d:%i`, compare to `P0_ATTESTED_ROOT_MOUNT_ID` ✓ |
| `python3` must equal trusted Python | `:617-623` | `if python3: pin_path = P0_FIXED_TRUSTED_PYTHON` ✓ |
| Expected pin-count check (twelve) | `:632-639` | `[ "$P0_PIN_COUNT" -eq "$P0_TOOL_COUNT_EXPECTED" ]` ✓ |
| P0-only `id`/`getent` declaration | `:355-357` | `P0_RP7_RO_TOOLS="… python3"`, `P0_P0_ONLY_TOOLS="id getent"` ✓ |
| Venv-root validation | `:488-515` | presence/charset/absolute/traversal/canonical/candidate-bound chain ✓ |
| Derives interpreter | `:759` | `P0_PY="$P0_VENV_ROOT/bin/python"` ✓ |
| Asserts before execution | `:1871-1872` | `p0_assert_venv_root`, `p0_assert_interpreter_executable` ✓ |
| Trusted-Python literal | `:278` | `P0_FIXED_TRUSTED_PYTHON='<PIN-AT-FREEZE>'` ✓ |
| Tool-pin literals | `:289-299` | 11 `P0_FIXED_*='<PIN-AT-FREEZE>'` ✓ |
| Attested literals | `:266-270` | 5 `P0_FIXED_ATTESTED_*='<PIN-AT-FREEZE>'` ✓ |

(Note: the ledger refers to the variables as `P0_ATTESTED_USER_NS` etc.; the
frozen-literal definitions are named `P0_FIXED_ATTESTED_USER_NS`. This is
harmless shorthand — the ledger's row 8 text itself uses both forms correctly,
the `P0_ATTESTED_*` being the wrapper-supplied input and `P0_FIXED_ATTESTED_*`
the embedded literal, and `:743-752` is the equality that binds them.)

## What I did NOT do (honestly stated)

- I did **not** execute `RP6-P0.sh` or `run_p0.sh`. RP6 is a host
  execution-domain prover and its run is host-gated for this unattended session;
  in any case it would `p0_stop` on the marker at `:709` rather than PASS, which
  is the claim under test. I did not need to run it: the claim is a static
  consequence of premises A/B/C, all byte-proven.
- I did **not** re-run the r16 D026 harnesses. The ledger's r16 claim is about
  *what kind of acceptance r16 was*, which I verified by reading the r16 verdict
  (`:1`, `:23-26`, `:159-161`, `:183-185`), not by re-executing it.
- I did **not** verify the non-RP6 halves of the ledger (transport, RP7). Those
  were already independently cross-checked by the two sibling GLM advance
  read-audits in this directory; my scope was the RP6 half.
- I did **not** re-verify every ledger citation into `run_p0.sh`/`run_ro.sh`/
  `remote_*`/`TRANSPORT_PLAN.tsv` — only the `run_p0.sh` citations load-bearing
  for Blocker 7 (`:151-155, :237-240, :241-243, :245`), all of which held.
- I did **not** touch the RP6-11 `eval`/dynamic-target question. That belongs to
  the sibling `RP6_GLM_ADVANCE_READ_AUDIT_2026-08-12.md` and is outside this
  cross-check's scope.

## Summary

| Claim | Verdict |
|---|---|
| 17 freeze-input literals remain unfilled in RP6 | **CONFIRMED** (17 distinct `P0_FIXED_*` definitions, triple-reconciled with status text) |
| Fence refuses unfilled markers ⇒ RP6 cannot PASS end-to-end | **CONFIRMED** (`:709, :724, :733-742` `p0_stop`; wrapper supplies markers) |
| r16 was source/audit acceptance, not host end-to-end P0 PASS | **CONFIRMED** (r16 verdict `:1,:23-26,:159-161,:183-185`) |
| 27 vs 17 "discrepancy" | **RESOLVED** — distinct definitions (17) vs total occurrences (27); both correct |
| Ledger RP6-P0.sh consumer line citations | **ALL VERIFIED** against current bytes |
| `STATUS_RP6_P0.md:311-312` citation | **STALE** (now at `:396-397` + recurs; `:274` for count) — the one defect, anticipated by the kickoff |

**Bottom line:** the RP6 half of the gpt-5.5 ledger is reliable. Its most
consequential claim survives an independent byte-level re-derivation, the
Lead's 27-vs-17 spot-check is explained (not a contradiction), and the only
defect is a stale status-file line citation that the kickoff already flagged as
likely. This cross-check is supplemental; it does not close any acceptance slot
and grants no freeze, dispatch, host, or deployment authority.
