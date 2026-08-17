# KICKOFF — Claude Pro T0 audit: RP7-WPI-RO.sh round 9, SECOND FLAGSHIP (dual-acceptance gate)

You are `claude-opus-5` xhigh via the default Claude Pro account, AUDITOR — the second
flagship. Codex `gpt-5.6-sol` already holds flagship PASS on these bytes
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R9_2026-08-11.md`: all five
r8 findings closed, including the F1 `ro.status.body`
BLOCK — the fetched body is now bound to the created leaf by descriptor, `wpi_alloc_leaf`
deleted). Claude MAX implemented r9, so YOU (a fresh Claude Pro session that implemented
nothing on this block) are the required independent second flagship. Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. Read-only on the repo: edit nothing except your verdict
file, no git mutation, no remote host, no network. Local fixture execution exactly as the
published harness does it is permitted.

## Bytes under audit
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` as committed on
`feature/donchian-crypto-ladder` — **108301 B**, SHA-256
`0e93f90de7fcefe86fee4137f3ba11ea34b69b120d6a06c304fdde0e9b921e62`. Re-derive and confirm this
identity first; it is also the identity the r9 transcripts record, which is the crux of the
documentary defects below.

*External evidence: that size and digest were re-derived on 2026-08-12 from the current repository
bytes of `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` (repo root
`C:\LAB\Tradingview_LAB_CLEAN`, branch `feature/donchian-crypto-ladder`); the matching transcript
record is the `BYTE_IDENTITY` line at
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:1725`
(`green_bytes=108301 green_sha256=0e93f90d…921e62`). No line of this kickoff proves it locally.*

Start from `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP7.md`, then
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md` (§ROUND 9) and
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_REPAIR_R9_REPORT.md` for the published
harness and evidence, then the Codex r9 verdict at
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CODEX_T0_AUDIT_R9_2026-08-11.md`.
Verify the narrative against the bytes — do not inherit Codex's conclusions.

## The r9 headline you must independently re-establish
The round-6 residual that came due: `ro.status.body` was create-once allocated then
addressed BY NAME by curl, digest, and parser — a hard link or name swap could overwrite
outside the evidence tree or flip an ARMED body to an accepting DISARMED result. r9 binds
the leaf by DESCRIPTOR end to end (curl `--output /dev/fd/3` dup'd from the `O_CREAT|O_EXCL`
open; parser reads the same descriptor as stdin and digests exactly what it parses;
`wpi_alloc_leaf` deleted). Also: descriptor-bind STOP reports measured child rc, not a
caller literal; row-22 `detail` field emitted on both nonzero namespace-read branches.

## KNOWN DOCUMENTARY DEFECTS — found 2026-08-12 evening, NOT yet repaired
A prose-vs-transcript audit
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_RP7_2026-08-12.md`, 461 output lines
checked) found that **`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md`'s narration
of WHICH BYTES its fences ran against is stale, while the pasted transcripts themselves are
correct.** Disclosed so you judge rather than rediscover:

- **FALSE — `:1768-1769`** says the round-7 fence proves the GREEN subject is `92853 B /
  e695a67b…`. The transcript at `:1725` records `green_bytes=108301
  green_sha256=0e93f90d…921e62`.
- **FALSE — `:2552-2556`** says the round-5 fence body is exactly `20050 B`. The pasted output at
  `:197` and `:4391` records `21263`.
- **FALSE — `:4353-4354`** says the round-4 final identity line is `BYTES=77179
  SHA256=393a16ce…`. The actual line at `:4349` records `BYTES=108301 SHA256=0e93f90d…921e62`.
- **SCOPE-WRONG — `:1354`, `:1368-1369`, `:1808`, `:1849-1850`, `:2565-2566`, `:2970-2972`** say
  carried fences were re-executed against "round-8 bytes"; the transcript identity lines at
  `:1725`, `:2403`, `:2915`, `:4349` all show the current round-9 bytes.
- **UNSUPPORTED — `:4421-4429`** states absolutely that the status body is "no longer addressed by
  name at all" and that `wpi_alloc_leaf` is deleted. No pasted line proves `wpi_alloc_leaf=0`.
  *(A GLM advance read-audit independently grepped and found zero `wpi_alloc_leaf` matches, so
  the claim appears TRUE but its evidence lives outside this document.)*
- **UNSUPPORTED — `:4375-4380`** claims six `WRAPPER_STREAM` stderr lines; only
  `RUN_ONE_STDERR_BYTES=210` is pasted.

**The question only you can settle.** The transcripts consistently show `108301 /
0e93f90d…921e62`, which IS the current accepted RP7 identity — so the *evidence* looks sound and
the *narration* looks stale. **Verify that reading rather than assuming it.** If every carried
fence really did run against the current bytes, this is a documentation repair. If any carried
gate genuinely ran against older bytes, then that gate does not cover the artifact under review,
and that is a real finding that changes the acceptance answer.

## Audit contract
1. Run the published SELF-QA harness VERBATIM (record real rc/summary lines).
   **Use the published `sed|bash` extractor exactly; do not retype or invent an ad-hoc
   extractor.** The published invocation is at
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:177-182`, and extraction is how
   that document intends the fence to be run — a third party is explicitly not meant to retype
   it:

   ```
   sed -n '/^# RP7_EXACT_COMMAND_BEGIN$/,/^# RP7_EXACT_COMMAND_END$/p' SELF_QA_RP7.md | bash --noprofile --norc
   ```

   The bare basename in that command is published as shown and must stay as shown. Run it with
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT` as the working directory — that is the directory
   holding `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md`, so the published
   argument resolves unmodified — or substitute that same full repo-relative path into the `sed`
   argument. What is forbidden is a hand-built substitute for that extractor, not extraction
   itself.
2. Adversarially attack the descriptor binding: is there ANY remaining site where an
   evidence leaf is created and later addressed by a rebindable name? Any second reader of
   a name? Any caller-declared rc literal surviving?
3. Confirm rows 10–23 read-only claims now hold inside rows 20–21 (the class the r6
   disclosure admitted), and row 24 stays operator-side only.
4. Thirteen-pattern adjudication table. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES /
   BLOCK. If accepting, state that RP7 reaches DUAL FLAGSHIP ACCEPTANCE — which also
   unlocks the owner-decided rows 1–9 build (BUILD ALL NINE, applied only after this
   acceptance).

Write ONE new file: `RP7_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md` (this directory).
**Delta gate (corrected 2026-08-12 ~20:35 — a global clean-status gate CANNOT pass in this
worktree, which carries ~100 pre-existing untracked run logs, and would have self-blocked this
lane).** Instead:
1. **Before execution** capture `git status --porcelain` → `before`.
2. Run the lane.
3. **At the end** capture `git status --porcelain` → `after`, and prove `after` minus `before`
   contains **only** `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`
   and nothing else. Any other entry in the delta **fails** the gate.
4. Also run `git status --porcelain -- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`
   and record its output as the path-scoped confirmation.
