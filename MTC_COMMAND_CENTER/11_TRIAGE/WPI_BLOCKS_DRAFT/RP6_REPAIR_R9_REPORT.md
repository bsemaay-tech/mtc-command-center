# RP6-P0 round 9 repair report — grammar drift close (the second emit site)

Implementer: Claude (fresh session, GLM-5.2 having hit its window limit mid-round-9
and left the two-site adjudication undone — see `RP6_R9A_LEAD_QA_EXECUTION_2026-08-11.md`).
Auditor of record: Codex (`gpt-5.6-sol`, T0 re-audit pending). Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network, no commit. UNIX LF
only, zero CR bytes. The block **unfroze for this round**; round 8 was evidence-only.

Audit tier: **T0** (host/execution-domain preflight). Owner grant #7 (2026-08-10)
lifts the T0 round cap for this block set; the acceptance standard is unchanged.
The block remains a draft: not frozen, accepted, dispatchable, or authorised for
host execution.

## Scope carried in from 9a, and what 9b closes

Round 9a (commit `ab53a012`, already applied) closed the **generic** emit site:
`p0_frozen_tool_path` now sets `P0_FROZEN_CONST_NAME` for all twelve tools and the
in-loop site (`:616`) emits `name=$P0_FROZEN_CONST_NAME`, so the live
`PIN_FREEZE_EXACT` assert in `RP6_R4_D026` matches the preregistered line
character for character. All eight fences went green for the first time on bytes
`e7ca9ff1…` (103808 B). 9a explicitly left three things open — the second emit
site, the emit-site sweep, and the report/QA/status layer. **This round (9b)
closes all three.**

## The defect (the remaining, second emit site)

`WPI_PREREGISTRATION_DRAFT.md` §8.1 row 1 declares exactly one shape for the
freeze-unfilled condition:

```text
P0_STOP reason=input_pin_freeze_unfilled tool=python3 name=P0_FIXED_TRUSTED_PYTHON detail=deploy_channel_value_never_derived_here
```

and, separately (the round-7 correction-7 amendment to the same row), declares a
**different reason token** for a missing pin:

```text
P0_STOP reason=input_pin_omitted tool=<t> detail=every_preregistered_tool_requires_one_frozen_pin
```

The block had two `input_pin_freeze_unfilled` emit sites. 9a fixed the in-loop
site (`:616`). The post-loop site still emitted an undeclared second shape:

```text
:616  (in-loop, 9a)   p0_stop "input_pin_freeze_unfilled tool=$p0_pin_name name=$P0_FROZEN_CONST_NAME detail=deploy_channel_value_never_derived_here"   <- declared, conforms
:655  (post-loop)     p0_stop "input_pin_freeze_unfilled tool=python3 name=P0_FIXED_TRUSTED_PYTHON detail=trusted_python_pin_omitted_freeze_gate_load_bearing"  <- NOT declared
```

So one reason token still had two shapes, one of which the draft never names.

## Adjudication — which closure, and why

The kickoff required a decision between (a) two distinct conditions → draft
declares both, or (b) one condition reached twice → same line. **The answer is
neither, for a specific reason that the round-7 history makes decisive.**

The two sites are semantically distinct:

- `:616` (in-loop) fires when a pin entry exists but its frozen deploy-channel
  literal is still the unfilled `<PIN-AT-FREEZE>` placeholder — the genuine
  *unfilled-placeholder* condition.
- `:655`/`:668` (post-loop) fires when `P0_TRUSTED_PYTHON_BOUND != yes` — i.e.
  python3 was not bound to `P0_FIXED_TRUSTED_PYTHON`. In the round-5 design this
  was the *omission* detector, and the `detail=` value distinguished it from the
  in-loop placeholder case under one shared reason token.

**Round 5's "two details of one token" design was superseded by round 7's
correction 7.** Correction 7 added the omission-rejection loop (`:632-637`):

```text
for p0_t in $P0_RO_TOOLS; do
    case "$P0_PIN_SEEN" in *" $p0_t "*) : ;;
        *) p0_stop "input_pin_omitted tool=$p0_t detail=every_preregistered_tool_requires_one_frozen_pin" ;;
    esac
done
```

That loop (a) emits the **declared** `input_pin_omitted` token for any
preregistered tool absent from `P0_PIN_SEEN`, python3 included, and (b) fires
*before* the post-loop gate. The draft row was amended in round 7 to declare
`input_pin_omitted`. The post-loop gate's round-5 relic detail was never declared
and never removed — it survived three reviews because no executable fence could
reach it (see reachability below).

**Reachability proof (static trace).** After the loop, for `:668` to fire we need
`P0_TRUSTED_PYTHON_BOUND=no` while the omission loop passed (all twelve tools,
python3 included, in `P0_PIN_SEEN`). But `python3` is appended to `P0_PIN_SEEN`
only inside the loop, and only after the python3 branch set
`P0_TRUSTED_PYTHON_BOUND=yes` (otherwise it STOPped earlier at the in-loop
`:616` placeholder gate or the `:619` disagreement gate). So:

```
python3 ∈ P0_PIN_SEEN  ⟹  python3 was processed in the loop
                        ⟹  reached the python3 branch without STOPping at :616
                        ⟹  passed the :618 equality check (else STOP at :619)
                        ⟝  therefore set P0_TRUSTED_PYTHON_BOUND=yes at :620
```

Any input leaving `P0_TRUSTED_PYTHON_BOUND=no` is therefore already caught — by
the omission loop's `input_pin_omitted` (python3 absent), by the in-loop
`input_pin_freeze_unfilled` (placeholder unfilled), or by
`input_pin_not_frozen_trusted_python` (disagreement). **The post-loop gate is an
unreachable defense-in-depth backstop while correction 7 stands** — which the
block's own round-5 comment already half-admitted ("Correction 7's
omission-rejection loop above also forces a python3 entry; this re-check stays
as the named python3-binding assertion").

**Closure chosen.** Because the post-loop gate's condition *is the omission
condition, already declared under `input_pin_omitted`*, the correct fix is not to
declare a second form of `input_pin_freeze_unfilled` (option a) — that would
declare a redundant, unreachable condition that no fence could ever RED/GREEN-prove
(D026: a declared token no executable path can exercise is a declared token with
no closure evidence). Nor is it to emit the `:616` line (option b) — that would
be a lie, since the deploy-channel value *is* filled when the post-loop gate is
reached. The honest fix is to make the backstop emit the already-declared
`input_pin_omitted` token, matching the omission loop verbatim. This:

1. collapses `input_pin_freeze_unfilled` to exactly one declared shape, at exactly
   one live site (`:616`);
2. makes every emit site carry only a reason the draft declares;
3. preserves the backstop — it still STOPs at rc 3 if a future change ever lets an
   unbound python3 slip past the earlier gates, now with a conformant token;
4. touches no draft byte (the draft already declares `input_pin_omitted`).

Per the kickoff instruction ("do not change the draft to match the code without
saying so explicitly"): **the draft is not changed.** The block is made to conform
to the draft as it already stands.

## The repair (exact bytes changed)

Two regions in `RP6-P0.sh`, both in the post-loop python3-binding backstop. No
control-flow, variable, or structural change — a comment expansion plus one
string-literal reason label.

**1. Emit line `:667-668`** (was `:654-655`):

```diff
-[ "$P0_TRUSTED_PYTHON_BOUND" = yes ] \
-    || p0_stop "input_pin_freeze_unfilled tool=python3 name=P0_FIXED_TRUSTED_PYTHON detail=trusted_python_pin_omitted_freeze_gate_load_bearing"
+[ "$P0_TRUSTED_PYTHON_BOUND" = yes ] \
+    || p0_stop "input_pin_omitted tool=python3 detail=every_preregistered_tool_requires_one_frozen_pin"
```

**2. Preceding comment `:641-666`** — rewritten to state that correction 7's
omission loop is now the canonical omission detector and fires first, that this
gate is an unreachable defense-in-depth backstop, and that round 9 replaced its
undeclared round-5 relic detail with the declared `input_pin_omitted` token. The
omission-vs-unfilled-placeholder distinction is now between two reason tokens,
not two `detail=` values of one token.

No other byte of `RP6-P0.sh` changed.

## Emit-site sweep — every `p0_stop` / `p0_fail` site vs the declared grammar

Method: `grep -nE 'p0_stop "|p0_fail "'` over `RP6-P0.sh` (174 emit sites, lines
`:399`-`:1753`), each cross-checked against §8.1 rows 1-9 (P0 preflight) of
`WPI_PREREGISTRATION_DRAFT.md`. Sites grouped by reason-token family:

| Family | Representative tokens | Sites | Declared at | Result |
|---|---|---|---|---|
| Bootstrap / RP0-lib | `rp0_lib_not_sourced`, `rp0_bootstrap_not_run`, `evidence_identifier_refused` | `:399-413` | §1 contract / RP0-LIB | conforms |
| Numeric input gate | `input_missing`, `input_charset`, `input_range` | `:426-431` | row 1 input pattern | conforms |
| `P0_FORBIDDEN_GIDS` gate | `input_charset`, `input_range` (gid list) | `:459-486` | row 3 / F3 | conforms |
| `P0_VENV_ROOT` gate | `input_missing`, `input_not_absolute`, `input_path_traversal`, `input_not_canonical_spelling`, `input_not_candidate_bound` | `:493-514` | row 18 / B3s | conforms |
| Pin parse loop | `input_pin_malformed`, `input_pin_unknown_tool`, `prereg_input_malformed`, `input_pin_not_absolute`, `input_pin_charset`, `input_pin_freeze_unfilled` `:616`, `input_pin_not_frozen_trusted_python`, `input_pin_not_frozen_path` | `:570-623` | row 1 | conforms (`:616` fixed in 9a) |
| Pin count / omission | `input_pin_omitted` `:635`, `input_pin_count_unexpected` `:639` | `:632-639` | row 1 (correction 7) | conforms |
| **Post-loop python3 backstop** | **`input_pin_omitted` `:668`** | **`:667-668`** | **row 1** | **was undeclared → FIXED this round** |
| Execution-domain attestation inputs | `execution_domain_unattested` (field/detail variants), `execution_domain_mismatch` | `:663-723`, `:1302-1385` | row 8 | conforms |
| Tool resolution / inventory | `missing_tool`, `tool_resolution_unparsable`, `tool_pin_uncanonicalizable`, `tool_pin_mismatch`, `tool_pin_unpinned`, `tool_not_evaluable` | `:763-825`, `:874-893` | row 1 | conforms |
| Metadata helpers | `metadata_unreadable`, `metadata_multiline`, `metadata_unparsable` | `:839-865` | field grammar | conforms |
| Evidence binding | `evidence_binding_unprobeable`, `evidence_binding_unparsable`, `evidence_leaf_not_bound` | `:921-949` | §7 | conforms |
| Identity (getent / id) | `group_query_not_evaluable`, `identity_probe_*`, `capability_wider_than_ledger`, `identity_unexpected`, `identity_unresolvable`, `state_account_resolution_unexpected` | `:976-1278` | rows 2-3 | conforms |
| System-manager query | `system_manager_unreachable` (rc/budget/detail variants) | `:1476-1490` | row 9 | conforms |
| Path probe (B3) | `path_probe_empty/multiline/ambiguous/error/unclassified/denied` | `:1550-1607` | rows 10-11 / B3s | conforms |
| Venv root (B3s) | `venv_root_absent/is_symlink/kind_unexpected/canonicalization_*/not_literal_canonical` | `:1618-1653` | rows 10-11-15 | conforms |
| Interpreter (B1) | `interpreter_absent/symlink_dangling/kind_unexpected/not_executable/exec_*/probe_*/startup_not_isolated` | `:1668-1753` | row 18 | conforms |

**Deviation found: exactly one — the post-loop python3 backstop (`:668`), fixed
this round.** No other site emits a reason token or `detail=` value the draft
does not declare. No site where the draft looks wrong (so no draft edit is
recommended). The sweep is recorded as machine-checkable in the `R9_GRAMMAR`
harness in `SELF_QA_RP6.md`, which fails (RED) on a mutant that restores the
relic and passes (GREEN) on these bytes.

## Fence impact (the eight green fences from 9a)

The change is a comment expansion plus one token label at an **unreachable** site.
The eight fences that went green on `e7ca9ff1…` (`RP6_R4_D026`,
`RP6_FULLBLOCK_D026`, `R7_F2`, `R7_F3`, `R7_C3`, `C13_R3_BACKSTOP`,
`F2_FREEZE_GATE`, `C13_R4B`) do not assert the post-loop gate's token. Confirmed
by `grep trusted_python_pin_omitted_freeze_gate_load_bearing SELF_QA_RP6.md`: the
only matches are inside the **round-5** `R5_F1` polarity harness (lines ~3955-4068)
and its prose — which is NOT one of the eight current fences and runs its own
self-contained round-5 replica, not the block. `RP6_R4_D026`'s `PIN_FREEZE_EXACT`
(line ~2947) asserts the `:616` line, which is unchanged. The omission path in the
real block is caught by the `:632-637` loop (`input_pin_omitted tool=<first
missing tool>`), also unchanged. **The eight fences are expected to pass unchanged
on these bytes; their re-run is PENDING-LEAD-EXECUTION.**

The `R5_F1` harness is now stale relative to the block's post-loop gate (its
replica still models the round-5 token). A supersession note is added at that
harness in `SELF_QA_RP6.md`; the round-5 replica is not rewritten (it is
historical evidence of the round-5 polarity fix, and it still proves that
omission STOPs — only the spelling it expects is round-5). The current
block-grammar proof is the `R9_GRAMMAR` harness.

## RED / GREEN proof (D026)

`SELF_QA_RP6.md` gains the `R9_GRAMMAR` harness (marker-delimited,
line-offset-independent). It reads the block source and asserts the closed
invariant:

1. exactly one emit site uses `p0_stop "input_pin_freeze_unfilled`;
2. that site carries `detail=deploy_channel_value_never_derived_here` and
   `name=$P0_FROZEN_CONST_NAME`;
3. zero sites emit the relic `trusted_python_pin_omitted_freeze_gate_load_bearing`;
4. the post-loop backstop emits the declared
   `input_pin_omitted tool=python3 detail=every_preregistered_tool_requires_one_frozen_pin`.

Polarity is falsifiable: a mutant that restores the relic at `:668` flips all
four checks (count 1→2, relic 0→1, backstop token 1→0) and the harness exits 1
(RED); the round-9 bytes exit 0 (GREEN). The Lead runs both and records real
output; this session gates `bash`, so the run is `PENDING-LEAD-EXECUTION`, not
fabricated.

## Artefact identity

```text
file        = WPI_BLOCKS_DRAFT/RP6-P0.sh
sha256      = 08e0a93562bb04f4f78bac77d973a26da5b609aa305491d3bfa51743adbcf10c
bytes       = 104683
cr_bytes    = 0            (tr -cd '\r' < RP6-P0.sh | wc -c)
line_endings= LF_only
bash_n      = PENDING-LEAD-EXECUTION  (session gates bash; change is comment + one string literal)
pre_9b_sha256   = e7ca9ff1e6d44b838b6d8bfddbb24bb68e2642b9f65abfc941f9482e465a0839 (103808 B, the 9a commit ab53a012)
relic_residual  = 0            (grep -c trusted_python_pin_omitted_freeze_gate_load_bearing RP6-P0.sh)
frozen_ro_basis= RP7-WPI-RO.sh@d6a976aa sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad bytes=70941
```

Draft touched: **none.** Files written this round: `RP6-P0.sh`,
`SELF_QA_RP6.md` (R9 section + R5-F1 supersession note), `STATUS_RP6_P0.md` (R9
layer), this report. Nothing committed; no host contacted; no network command
run.

## PENDING-LEAD-EXECUTION (this session gates `bash`)

In an unhindered Git Bash against `08e0a935…` / 104683 B:

```text
bash -n RP6-P0.sh                                                          -> expect rc 0
tr -cd '\r' < RP6-P0.sh | wc -c                                            -> expect 0   (DONE this session)
sha256sum RP6-P0.sh                                                         -> 08e0a935…  (DONE this session)
sed -n '/R9_GRAMMAR_HARNESS_BEGIN/,/R9_GRAMMAR_HARNESS_END/p' SELF_QA_RP6.md | bash --noprofile --norc  -> expect R9_GRAMMAR_SUMMARY result=PASS
# D026 RED twin (revert :668 to the relic in a temp copy, re-run the harness)  -> expect result=FAIL
# the eight 9a fences by anchored marker, all rc 0 (unchanged):
#   RP6_R4_D026 / RP6_FULLBLOCK_D026 / R7_F2 / R7_F3 / R7_C3 / C13_R3_BACKSTOP / F2_FREEZE_GATE / C13_R4B
```

The freeze gate still has seventeen `<PIN-AT-FREEZE>` literals, so no end-to-end
`P0 PASS` is possible and nothing here is dispatchable regardless of this round's
verdict.
