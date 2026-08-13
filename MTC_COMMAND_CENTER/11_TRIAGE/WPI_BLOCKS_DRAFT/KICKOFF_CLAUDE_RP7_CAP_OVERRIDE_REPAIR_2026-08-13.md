# RP7 cap-override repair - Claude implementer

You are the counterpart flagship IMPLEMENTER in a fresh session. Model must be
`claude-opus-5`; effort `xhigh`. This is the single owner-authorized T0 cycle
beyond the normal cap. No sub-delegation and no git mutation.

Working directory: `C:\LAB\Tradingview_LAB_CLEAN`.

Read, in order:

1. root `AGENTS.md` and `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`;
2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-13.md`, section 4;
3. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CLAUDE_T0_POST_R4_AUDIT_2026-08-13.md` in full;
4. current `RP7-WPI-RO.sh`, `SELF_QA_RP7.md`, `STATUS_RP7.md`, and
   `RP7_ROWS_1_9_REPORT_2026-08-13.md`.

The two REQUIRED findings are the binding work order:

1. Restore trailing carriage-return handling before row-6 continuation
   detection so LF and CRLF fragments model real systemd consistently. Do not
   regress the trailing-space-after-backslash behavior. Add a literal D026
   CRLF pair, RED against the current pre-repair bytes and GREEN against the
   repaired bytes.
2. Make the package itself execute the six existing row-6 D026 pairs against
   both subjects: materialize the actual round-4 pre-fix blob and run the same
   extracted production functions against pre-fix and repaired bytes. The
   published fence and transcript must contain the real two-subject commands,
   outputs, identities, and polarity assertions. Narration alone is forbidden.

Adopt NIT-1 by adding a trailing-space control if cheap. Preserve every closure
already confirmed by the final audit. Never reimplement production logic in the
harness; extract and execute the actual block functions. Keep scratch outside
the repository, execute strictly sequentially, and use a run-owned scratch root
to avoid the prior fixed `/tmp` collision.

Owned files only:

- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP7.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_ROWS_1_9_REPORT_2026-08-13.md`

Run the complete published rows-1-9 fence verbatim after editing. Re-derive all
byte/SHA identities and ensure the pasted transcript matches the real output
exactly. Run syntax checks and `git diff --check` on owned files. Report every
command/result honestly. Do not claim T0 acceptance; the Lead and two fresh
flagship auditors decide it. Stop after the owned files are complete.
