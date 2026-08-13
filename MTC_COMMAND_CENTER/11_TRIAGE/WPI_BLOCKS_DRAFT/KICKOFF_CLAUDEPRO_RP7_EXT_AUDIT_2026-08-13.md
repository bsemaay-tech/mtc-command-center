# KICKOFF — Claude Pro T0 audit of the extended RP7 bytes (rows 1-9, round-2 repaired)

Tier T0. Model `claude-opus-5` xhigh, fresh session, non-implementer. Read-only except your
single verdict file:
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CLAUDE_T0_EXT_AUDIT_2026-08-13.md`.
No git mutation. **Foreground only — never background a command, never end your turn while
anything is running.** Path-scoped delta gate on your verdict file governs; whole-status delta
advisory with attribution (concurrent lanes commit in this worktree).

## Subject and history

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` — current identity
**127046 B, SHA-256 `a2ec1d0c47db53a756b7abe0803e7c6e62d42dd4c6b69934332c2eb501c714ad`**
(re-derive before anything else).

History you inherit (verify identities, do not re-litigate closed rounds):
- The r9 bytes (108301 B / `0e93f90d…`) hold dual flagship acceptance: Codex
  `RP7_CODEX_T0_AUDIT_R9_2026-08-11.md` PASS + Claude
  `RP7_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md` PASS-WITH-NITS.
- The owner-decided rows 1-9 extension (BUILD ALL NINE, design of record
  `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROWS_1_9_OPTIONS_CODEX_2026-08-10.md`
  §D) was applied after that acceptance, then round-2 repaired the same night per
  `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_ROWS_1_9_GLM_ADVANCE_READ_2026-08-13.md`
  (4 REQUIRED + 2 NIT, all addressed or refuted in
  `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_ROWS_1_9_REPORT_2026-08-13.md`).
- Implementers of the extension: Codex free (gpt-5.5-class) sessions. You are the first
  flagship on these bytes. **An accepting verdict fills the Claude slot only; dual acceptance
  additionally needs a fresh Codex `gpt-5.6-sol` audit (blocked on account limits until
  08-16/08-18).**

## Known context, disclosed so you judge rather than rediscover

1. The first D026 delivery for rows 1-9 was a Python re-implementation and was REJECTED by
   the Lead; the rebuild fence executes the block's own extracted functions
   (`sed -n '/^# RP7_ROWS_1_9_REBUILD_FENCE_BEGIN$/,/^# RP7_ROWS_1_9_REBUILD_FENCE_END$/p'
   SELF_QA_RP7.md | bash --noprofile --norc`, run from `WPI_BLOCKS_DRAFT` under WSL). The
   Lead's verbatim run: rc 0, `red_green_pairs=23 controls=3 result=PASS`, 49 transcript
   lines byte-matching the doc. **Run it yourself verbatim; do not trust either of us.**
2. Row 1 reads `ActiveState` instead of the preregistered verbatim `systemctl is-active` —
   recorded as a labelled preregistration-amendment note, NOT silently amended. Adjudicate
   whether that amendment is acceptable or must be built as written.
3. Carried finding C1 (mount-projection digest over a re-resolved name) is disclosed on its
   own terms; the code repair was scoped to a future round with the rows-10-19 reader class.
   Judge whether the rows 1-9 additions widen or narrow that class (they must not add any
   name-readdressed leaf — `wpi_alloc_leaf` must remain absent).
4. The ten row-8 sandbox pins are asserted renderings whose host derivation is a freeze-time
   act (disclosed). Judge the disclosure's honesty, not the absent derivation.

## Contract

1. Re-derive both identities (`RP7-WPI-RO.sh`, `SELF_QA_RP7.md` — state the SELF_QA identity
   you audited). `bash -n` the block. CR-byte check.
2. Execute the rebuild fence verbatim (WSL). Compare your transcript to the pasted one.
3. Audit the two new sections (`B2_rows_1_7`, `B4_rows_8_9`) adversarially against §D:
   presence-before-value everywhere, absent record → STOP not default, bounded captures via
   `wpi_capture` unchanged, descriptor discipline intact, every fixture RED failing for the
   row's own reason, no evidence that cannot fail, thirteen-pattern adjudication.
4. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES, with per-question adjudication, exact
   citations, delta-gate proof, session model/effort line.
