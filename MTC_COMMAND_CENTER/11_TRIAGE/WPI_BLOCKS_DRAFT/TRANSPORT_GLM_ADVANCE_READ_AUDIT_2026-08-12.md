Verdict file written: `MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\TRANSPORT_GLM_ADVANCE_READ_AUDIT_2026-08-12.md`.

## ADVANCE-SUPPLEMENTAL PASS-WITH-NITS (source-level; harness execution PENDING-LEAD-EXECUTION)

**What this is, and isn't:** a GLM-5.2 read-audit, supplemental only. It does **not** close the transport second-flagship slot — that remains `PENDING` the Claude `claude-opus-5` audit. I executed no harness and fabricated no green run; this is a source-byte + control-flow read.

**Identity re-derivation:** all nine files match the acceptance matrix on bytes and SHA-256, including the three named (`transport_runner.ps1`, `TRANSPORT_PLAN.tsv`, `remote_close_tree_wpi.sh`).

**The four priority targets:**

1. **First-mismatch + per-branch prerequisites** — correctly implemented. Prereqs are resolved per-edge from `$classById` (`transport_runner.ps1:1068-1123, 1179`), and the P0 chain `{04→07→09→11}` shares no edge with the RO chain `{05→08→10→12}`. I could **not** construct a case where an unrelated branch failure demotes a genuine marked rc 1 — the historical global-snapshot demotion is genuinely removed. *One non-binding nit:* the non-crossing guarantee is data-asserted, not runtime-enforced (not exercisable today).

2. **Per-op provenance binding** — correctly implemented. `$MARKER_FAMILY_BY_STDIN` is keyed by the stdin leaf each row sends (`:231-260`); there is **no** global-union variable and no second marker gate. All five families match what the scripts actually emit (`P0W_`/`ROW_`/`SETUP `/`EXTRACT `/`CLOSE_`).

3. **Close-script contract** — the gpt-5.5 ledger reading is **confirmed and strengthened**. Plan ops 07/08 and the close script agree on three-arg `EV_DIR RUNID WORK_ROOT`; with unfilled `<PIN-AT-FREEZE>` pins the script STOPs at `:288-291` before RUNID/EV_DIR validation. `RUNID_MINTING_REVIEW_CODEX_2026-08-11.md:167` is the stale documentary contradiction — and it's stale in **two** respects the ledger only half-flagged: the two-arg claim *and* the "exits FAIL on argc" claim (current bytes return rc 3 STOP, not rc 1 FAIL). Both already corrected.

4. **Marker discipline + F1** — marker gate is first and fail-closed; sentinels are composed not literal. The "F1 IS OPEN" disclosure is carried at all six launch-domain sites; none overclaims `env -i` as end-to-end closure.

Zero required repairs to the nine-file transport set. I respected the dispatch's hard constraint — created only the verdict file, no git/host/network/fixture action, no handoff edits.
