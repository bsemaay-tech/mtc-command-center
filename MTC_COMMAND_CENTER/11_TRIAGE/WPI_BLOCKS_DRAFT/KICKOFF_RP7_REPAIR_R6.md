# KICKOFF — RP7-WPI-RO.sh round 6: four Part-B findings + one recovered test

You are Claude Opus 5, effort xhigh, **IMPLEMENTER**. Codex is the auditor of record for
findings 1–4 and re-audits your bytes, so separation holds. Round 6 is authorised under
owner grant #7. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host contact, no network,
no commit. UNIX LF only, zero CR bytes. Never `git checkout` a block file — use
`git cat-file blob <sha>:<path> > <path>`.

## Input bytes

`WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` round-5 bytes: SHA-256
`393a16ce264b467bec180a2106390e6dcee4dc2605fd019871270fda11d3b0ee`, 77179 B, commit
`1143a9ff`. Round 5's own delta was independently verified clean (`+93/-7`, no unexplained
hunks, no weakened checks) in `RP7_CODEX_DELTA_REVIEW_R5_2026-08-10.md` — do not re-litigate
round 5's repairs, build on them.

## Binding scope

`WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R5_PART_B_2026-08-10.md` — **BLOCK: 4**. That text
binds, including its executed evidence. Reproduce each RED on the round-5 bytes first.

1. **F1 (HIGH) — a malformed listener record is silently normalised and reported as a
   complete PASS.** A record that does not conform must not be repaired into conformance on
   its way through the reader. Every admitted record needs exactly one terminal disposition:
   conformant, or a STOP naming the specific grammar violation. Normalisation that changes
   what a record says is not parsing.
2. **F2 (HIGH) — truncated or invented status-parser result records become semantic FAILs
   instead of STOPs.** A result record that is incomplete, or that the parser did not
   actually produce, is an inability to evaluate. rc 1 means "a completed probe established
   deviant host state" and must not be reachable from a malformed producer result.
3. **F3 (MEDIUM) — invalid HTTP status tokens are reported as completed endpoint
   deviations.** An unparseable status token is a STOP, not an observed deviation.
4. **F4 (MEDIUM) — the published evidence command masks its own failures and is
   unbounded.** Each fence invocation is followed by a `printf`, so the command returns the
   `printf` rc. Codex proved it: two fences exiting 7 and 9, outer command rc **0**. There
   is also no outer timeout; one 188-second successful run does not establish a bound.
   Repair both: the published command must **fail when any fence fails**, and must carry an
   explicit bound it is documented to respect.

## Also in scope — one recovered test

`RP7_R5_SALVAGE_FROM_INTERRUPTED_AUDIT_2026-08-10.md` carries an executed test recovered
from a review the provider interrupted. It shows that `wpi_capture` allocates its leaf with
`noclobber` and then writes to it **without ever re-verifying the leaf's identity**: with the
leaf replaced between the two steps, the capture wrote outside the evidence tree, both paths
resolved to the same object, and the run continued at rc 0 with no STOP.

That test injected the replacement through a hooked function, so it is not a demonstrated
route reachable by the block alone. Treat it accordingly: **the defensible statement is that
the block claims confinement it does not establish.** Either close it — capture the leaf's
device/inode at allocation and write through a retained descriptor, or re-`stat` before the
write and STOP on any identity change — or state precisely and narrowly what the capture
path does establish. A STOP condition, never a FAIL. If you judge it out of scope, say why
in the report rather than passing over it.

## The rule this round keeps hitting

Three separate artifacts tonight failed the same way: RP6's fences exited rc 1 for a reason
unrelated to what they test, and RP7's published command cannot fail at all. **Evidence that
cannot fail proves nothing, and evidence whose exit status does not track what it measures
is worse than none** — it reports success. When you repair F4, make the fence's own rc the
command's rc, and prove it by making a fence fail on purpose and showing the outer command
fail with it.

Check your work against the amended `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — **thirteen**
patterns now. Patterns 11 (declared vs executed instrument), 12 (unmodelled input must not
disappear) and 13 (every admitted member needs a terminal disposition) were added tonight;
F1 and F2 are both pattern-13 shaped.

## Deliverables

Repaired `RP7-WPI-RO.sh` + `SELF_QA_RP7.md` with real RED/GREEN per finding + `STATUS_RP7.md`
+ narrow draft edits if required + `RP7_REPAIR_R6_REPORT.md` (finding → disposition →
evidence, draft-edit list, freeze-gate inputs). `bash -n` rc 0; re-derive SHA-256 and byte
count; zero CR bytes measured with `tr -cd '\r' < file | wc -c`. State the disposition of
every finding explicitly, including anything you do not repair and why. Do not commit — the
Lead verifies the hash and commits.
