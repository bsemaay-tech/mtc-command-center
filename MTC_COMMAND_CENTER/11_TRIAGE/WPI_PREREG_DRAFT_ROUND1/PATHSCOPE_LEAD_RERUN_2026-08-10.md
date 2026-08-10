# Lead re-run of the path-scope prover — 2026-08-10 ~20:45

## Why

`PATHSCOPE_RUN_2026-08-10.log` is not a run record. Its complete content is
`You've hit your session limit · resets 3pm (Europe/Chisinau)`.
`PATHSCOPE_RUN_NVIDIA_2026-08-10.log` is narration, not output. The §10.1 reconciliation
flagged this independently. So the "RP6 1 resolved / 37 unresolved, RP7 4 resolved / 65
unresolved" figures quoted in the handoff had **no committed backing** until now.

## What was run

The exact invocation published in `SELF_QA_PATHSCOPE.md`, with the same constants and the
same machine-form §10.1 allowlist. `<REMOTE_BASE>` was set to the disclosed
non-authoritative static value `/home/gatea/wpi_staging_STAGE1_STATIC_BINDING`, because the
real value is still `<ALLOCATE-AT-DISPATCH>` and the prover correctly STOPs at rc 3 on the
placeholder. **This is diagnostic depth, not acceptance evidence** — the same status the
self-QA gives it.

Inputs at scratchpad `real.constants` / `real.allowlist`. Blocks analysed at current bytes:
RP6-P0.sh `75db028e…4389570` (93421 B), RP7-WPI-RO.sh `23e55667…01aad` (70941 B).

## Result — the quoted figures reproduce exactly

```text
PATHSCOPE shell=...\RP6-P0.sh
PATHSCOPE resolved_count=1 unresolved_count=37
PATH value=/dev/null verdict=FORBID rule=- sources=NONE uses=line=359:redirection >,line=361:redirection >
UNRESOLVED line=371 reason=opaque command argument: unpinned variable RUNID expression="$RUNID"
UNRESOLVED line=371 reason=opaque command rp0_require_safe_component has no registered path-argument contract
UNRESOLVED line=373 reason=opaque command argument: unpinned variable EV_STAGE_ID expression="$EV_STAGE_ID"
rc=3

PATHSCOPE shell=...\RP7-WPI-RO.sh
PATHSCOPE resolved_count=4 unresolved_count=65
PATH value=/dev/null verdict=FORBID rule=- sources=NONE uses=line=183:redirection >,line=624:redirection >,line=625:redirection >
PATH value=/opt/mtc-bridge/venvs/<SHA>/bin/python verdict=ALLOW rule=/opt/mtc-bridge/venvs/<SHA>/** sources=WPI_VENV_ROOT uses=line=763:test
PATH value=/proc/self/mountinfo verdict=FORBID rule=- sources=NONE uses=line=413:redirection <
PATH value=/proc/uptime verdict=FORBID rule=- sources=NONE uses=line=173:redirection <
rc=3
```

## Amendment, ~20:40 — the tool is now under REQUEST_CHANGES

`PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md` returned **REQUEST_CHANGES: 9**, four of them
CRITICAL under-reporting: complete Bash fragments reach filesystem or network primitives
while the prover emits no path, no `UNRESOLVED` marker, and `verdict=PASS rc=0`. Its
independent re-run reproduced this file's numbers and lines exactly.

Consequence for everything below: these counts are a **deterministic lower-bound
diagnostic from a currently unsound analyzer**. A `FORBID` or `UNRESOLVED` it prints is
real; a `PASS` or an absence of output proves nothing. They must not be used to freeze a
block, to assert complete scope, or as the §10.1 reconciliation's primary basis — the
reconciliation derived its table by reading the block sources and used the prover only as
a cross-check, which is the correct order and remains valid.

## Lead conclusions

1. The handoff figures are now backed by a reproducible run on the current bytes — as a
   lower bound only; see the amendment above.
2. The `/dev/null` `FORBID` verdicts land on **exactly** the lines the §10.1 reconciliation
   named (RP6 359/361, RP7 183/624/625). Two independent methods agree, and the Lead also
   confirmed those lines by inspection. The removal item in the R5 and R7 kickoffs is
   sound scope.
3. `/proc/self/mountinfo` and `/proc/uptime` are `FORBID` purely because §10.1 does not
   list them yet — they are EXTEND candidates in the reconciliation, not block defects.
4. The RP6 unresolved set begins at the evidence-allocation boundary (`RUNID`,
   `EV_STAGE_ID`, and `rp0_require_safe_component` having no registered path-argument
   contract). This is the same gap the reconciliation calls "evidence-root provenance":
   Stage 1 cannot close either block's path set without analysing the composite
   wrapper + RP0-LIB + RP0-BOOTSTRAP + block input.
5. `PATHSCOPE_RUN_2026-08-10.log` and `PATHSCOPE_RUN_NVIDIA_2026-08-10.log` should be
   deleted or renamed to `*_FAILED_DISPATCH.log` at the next commit that touches them —
   as they stand they read like run records and are not.
