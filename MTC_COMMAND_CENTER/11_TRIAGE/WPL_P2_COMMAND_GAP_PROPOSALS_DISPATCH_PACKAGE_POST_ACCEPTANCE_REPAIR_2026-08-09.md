# WP-L P2 dispatch package — post-acceptance finding and repair (2026-08-09)

## Status

**REQUEST_CHANGES — package repair round 2/3, fresh re-audit required.** GLM-5.2 source-fidelity audit of candidate
anchor-map commit `331c383c` found two required §4 errors. Lead independently reproduced the underlying
candidate control flow and found the first error had propagated into the previously accepted Claude
prompt and Lead checklist. Their prior acceptance records are superseded.

Dispatch-package round 1 commit `2bd4ae8d` received GLM-5.2 `PASS-WITH-NITS` but fourth-account Codex
`REQUEST_CHANGES` with three Lead-reproduced required findings. This is dispatch-package repair round
2/3. It is separate from proposal implementation, which remains 0/3 because Claude has not edited the
rejected proposal.

## Reproduced required finding R1 — exact no-rebind fields

Candidate `2ce41e34:IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh` proves:

- `:113` initializes `UNIT_SHA=""`;
- `:114-116` hashes the currently installed first-start unit when present, before the rebind branch;
- `:117-155` enters rebind behavior only when `TARGET_SHA` is non-empty;
- `:164-165` writes target release SHA fields, which are empty in no-rebind;
- `:168` writes `first_start_unit_sha256` from `UNIT_SHA`, so it is the installed unit hash when present
  and empty only if that unit file was absent.

Therefore "all no-rebind fields empty" is false. The accepted repair specification did not contain that
rule; it entered as an optional spec-audit nit and propagated into the prompt/checklist. The repair now
requires only the two target-release fields empty and validates the unit hash against preregistered unit
presence/hash.

## Reproduced required finding R2 — stop/mask control-flow wording

Candidate `rollback.sh:79-86` performs stop/mask before the optional rebind block. A no-rebind invocation
does not make stop/mask conditional; it omits the target SHA arguments so the additional install,
daemon-reload, and re-mask branch at `:117-155` is skipped. The anchor map now states that exact flow.

## Folded line-range nits

Corrected ranges: `common.sh:95-105`; `verify.sh:129-135,155-205`; and
`rollback.sh:42-52,70-78,79-101`. These do not change semantics but keep the map line-exact.

## Round-1 re-audit required findings and round-2 repair

1. Normative pins to superseded prompt `fbb5ca61` and checklist `456968bb` could reintroduce the false
   empty-all-fields rule. They are now marked historical-only/forbidden; Lead use is gated on the exact
   repaired package commit accepted by fresh canonical audits.
2. GLM+Codex is not the canonical acceptance floor. Fresh package acceptance requires accepting
   `claude-opus-5` xhigh and `gpt-5.6-sol` xhigh verdicts plus no unresolved Lead-reproduced required
   finding from any canonical auditor. GLM-5.2 and DeepSeek remain canonical detection auditors; inability
   to execute is `BLOCK`/non-acceptance for that auditor and never supplies acceptance.
3. Listing future RED/GREEN cases did not satisfy implementer D026 duty. The Claude repair prompt now
   requires safe local temporary/stub-based execution of actual proposed predicates, commands and real
   outputs recorded in the one writable proposal document. Inability to execute safely is `BLOCK`.

## Superseded artifacts

- prompt audit PASS-WITH-NITS;
- checklist audit/re-audit PASS-WITH-NITS and byte-exact checklist `456968bb` acceptance;
- fourth-account Codex package PASS-WITH-NITS.

The histories remain recorded, but none accepts the repaired package.

## Next steps

1. Freeze this bounded package repair and all continuity records.
2. Fresh `claude-opus-5` xhigh and `gpt-5.6-sol` xhigh package re-audits; both must accept.
3. Fresh GLM-5.2 package re-audit; attempt DeepSeek, recording any route non-execution as `BLOCK` and never
   treating it as acceptance.
4. Only after the canonical floor above is met and no reproduced required finding remains, dispatch a
   separate fresh Claude implementation session for proposal repair round 1/3.
5. Preserve every host/trading/deployment hold.
