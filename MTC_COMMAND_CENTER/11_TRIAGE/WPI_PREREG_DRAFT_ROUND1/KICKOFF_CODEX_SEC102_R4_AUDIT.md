# KICKOFF — Codex T1 audit: SEC102 composite pathproof round 4 (OUTPUT-HYGIENE)

Date: 2026-08-11. Codex `gpt-5.6-sol` xhigh, AUDITOR. Max implemented r4 (closing your 3 r3
MEDIUMs); you are the independent cross-model check. Fresh session, read-only: edit nothing
except your verdict file, no git mutation, no host, no network. T1. Prove `git status
--porcelain` clean at the end.

## OUTPUT-HYGIENE (fixtures include an attack-shaped evil member). Redirect fixture output to
files; quote only `COMPOSITE_PATHPROOF verdict=`, `CLAIM id=... verdict=`, `CASES=`,
`FAILED_COUNT=`, `FREEZE_INPUT ... disposition=`, `RESIDUAL ...` lines. Refer to the evil
fixture by name; never reproduce its body or forbidden-path/exfil literals. Do NOT author new
attack fixtures. Verdict first.

## Bytes — commit `28b5c06b`
`composite_pathproof.py` (+335/−9 from r3). NEW `MTC_COMMAND_CENTER/11_TRIAGE/
WPI_PREREG_DRAFT_ROUND1/.gitattributes`. `sec102_r4_fixtures/` (10). `SELF_QA_SEC102_R4.md`,
`STATUS_SEC102.md`, `SEC102_R4_REPORT_2026-08-11.md`. Both r2 CRITICALs stay closed.

## Your r3 findings (REQUEST_CHANGES ×3, all MEDIUM)
R3-F1 RENDER coverage shared the graph detector's blind spot. R3-F2 F10 passed without a
terminal disposition for every plan allocation (an allocation absent from constants produced no
F10 failure — Pattern 9). R3-F3 clean Windows checkout changed pinned fixture bytes (Pattern 10
durability).

## Round-4 dispositions (Lead reran verbatim)
- Matrix `CASES=40 FAILED_COUNT=0` (37 r3 + 3 new).
- R3-F2 CLOSED: `red_freeze_allocation_absent` → `CLAIM id="F10" verdict="STOP"
  reason="allocation_absent_from_pinned_constants"`, and CRUCIALLY F5+F6 are PASS on BOTH sides
  — F10 itself moves, no downstream STOP hides behind it (your exact requirement). rc 3.
- R3-F1 CLOSED: RENDER coverage blind spot fixed (new RED that previously passed now STOPs).
- R3-F3 CLOSED: scoped `.gitattributes` — fixtures `-text` (binary, no EOL conversion), the two
  tools `text eol=lf` (byte-stable + diffable). Measured load-bearing: the fixtures-only sketch
  was still RED (pathscope_prover.py materialised 125222 B vs its 122446 B pin, F4
  frozen_identity_mismatch), so the tool pins were required. Scope: this directory only, no
  global change; demonstrated durable in a throwaway repo with autocrlf on. Lead confirmed the
  attribute does not renormalize the tools (git status clean for them).
- Grammar battery 32/32; 5 mutation discriminators restore the defective PASS. Also fixed the
  r3 harness `if($failed){exit 1}` → `else{exit 0}` rc bug.
- Residuals stated: detection vocabulary is a list (an interpreter not in it, under a literal
  name, derives no edge — pathscope scope); F10 STOPs on every absent allocation (chosen
  conservative false-stop); wrapper detection safe false-stops; no new adapter arm (5 of 33).

## Audit contract
1. Re-run the matrix + the 3 new RED fixtures VERBATIM (output to files); confirm 40/40 and that
   R3-F1/F2's REDs reach STOP with F10 (not a downstream check) doing the work for F2.
2. **Verify R3-F3 durability** yourself: read `.gitattributes`; confirm it is scoped to this
   directory, that `-text` on the fixture globs + `text eol=lf` on the two tools makes the
   checked-out bytes equal the committed bytes under `core.autocrlf=true`, and that it does not
   renormalize or alter `pathscope_prover.py`'s committed blob. A local-clone prerequisite would
   NOT close it; the committed attribute must.
3. **Adversarial (describe by mechanism, no attack shell):** any remaining silent composite PASS
   over a real sink, any allocation/variable the reconciliation still misses, any render/freeze
   member the graph derivation skips. Re-opens a CRITICAL if found.
4. Judge the stated residuals: honestly scoped limits, or reachable false-PASS?
5. 13 patterns. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK. If PASS, note the T1
   gate still needs the GLM-5.2 second opinion (>300 lines) — GLM returns ~05:28.

Write ONE new file: `SEC102_CODEX_T1_AUDIT_R4_2026-08-11.md`.
