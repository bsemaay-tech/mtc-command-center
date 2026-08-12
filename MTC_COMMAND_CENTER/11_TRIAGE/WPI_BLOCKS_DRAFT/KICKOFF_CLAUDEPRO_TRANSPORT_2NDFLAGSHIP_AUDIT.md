# KICKOFF — Claude Pro T0 audit: WP-I transport set, SECOND FLAGSHIP (dual-acceptance gate)

You are `claude-opus-5` xhigh via the default Claude Pro account, AUDITOR — the second
flagship. Codex `gpt-5.6-sol` already holds flagship PASS on these bytes
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CODEX_R6B_CONFIRM_2026-08-11.md`,
r4→r6 closed the F1 overclaim, BA-1/BA-2/BA-3,
R5-F1/F2/F3). You are a FRESH session and did not implement any transport round — Max
implemented r4–r6, so implementer/auditor separation holds. Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. Read-only on the repo: edit nothing except your verdict
file, no git mutation, no remote host, no network. Local WSL2 fixture execution under
`/root/wpi_r*` is permitted exactly as the published harness does it.

## Bytes under audit
The transport set as committed on `feature/donchian-crypto-ladder` — start from
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md`, which pins the round-6
state, then `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md` for the
published harness and evidence. Do not trust the status narrative: verify it against the bytes.

**These are the bytes.** The seven executable/plan targets below are the audited set; re-derive
every identity yourself before relying on it. (The nine-file set is these seven plus
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md` and
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md`, which legitimately changed in
round 6 — the round-6 byte-identity claim is scoped to the seven, and that scoping is already
correct.)

| File | Bytes | SHA-256 |
|---|---|---|
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_p0.sh` | 13608 | `4f608ad546402ad9587eeac237c16c7c3c3e707ebf4e6cb589e9459f08413c0c` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_ro.sh` | 13470 | `3dea6e64b087488fda2ab9bac8b66fceac1c13e70719b3ce9d81797a50443e3c` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/transport_runner.ps1` | 71137 | `4db0fbd17f9b32da13564a9ce2d0786283151737d81bcee031ed2bcb7b347fd2` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv` | 7970 | `e3c11218a9c70ef5454d8db25c7c9965ebed3ae07bc97a766240429685c50e3c` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_setup_wpi.sh` | 26483 | `4428a60da02415ef1b7c84561b1bba458ee7f1affcfe9d33c4b1c3f07bcb5aa5` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_extract_verify_wpi.sh` | 23592 | `5b3c0b225fdca18fd0a074a7bcce3c7124930e62eacc9e41da236db28585a55b` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_close_tree_wpi.sh` | 32630 | `8892574f253ab26d6d48bba270f84ef2da4458a5bca93f2b3c9723991a3732cf` |

*External evidence: every Bytes and SHA-256 cell in the table above was re-derived on 2026-08-12
from the current repository bytes at those seven repo-relative paths (repo root
`C:\LAB\Tradingview_LAB_CLEAN`, branch `feature/donchian-crypto-ladder`). No line of this kickoff
proves them locally. Do NOT read them off the earlier per-file census table at
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:2323-2329`: that snapshot is
historical, and six of its seven sizes are smaller than the current bytes (only
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_PLAN.tsv` at 7970 B matches). Re-derive
them yourself.*

## Binding context you must respect
1. **F1 (outer SSH account-shell boundary) is honestly OPEN and OWNER-RATIFIED 2026-08-12
   as ACCEPT-WITH-DISCLOSURE** — an inherent SSH-trust-model limit, not a freeze blocker.
   Do not demand its closure; DO verify no text claims the inner-child `env -i` domain as
   an end-to-end F1 closure, and that the disclosure is carried at every site.
2. `<ALLOCATE-AT-DISPATCH>`/`<PIN-AT-FREEZE>` stay literal with the preflight marker STOP.
3. No host contact, no RUNID allocation, no archive build — confirm the round performed none.

## KNOWN DOCUMENTARY DEFECTS — found 2026-08-12 evening, NOT yet repaired
A prose-vs-transcript audit
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_TRANSPORT_PATHSCOPE_2026-08-12.md`) raised
**four** Transport findings — `F-1`, `F-2`, `U-1`, `U-2` — each a claim in
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md` that its own transcripts do
not support. (That audit's `F-3` and `U-3` are Pathscope findings and are not part of this lane.)
**They are disclosed here so you do not spend your slot rediscovering them — and so you can judge
whether they change any acceptance conclusion:**

- **FALSE — `:23` and `:35-43` claim all fixture scratch was removed** and that each transcript's
  last line proves it. The Fixture D cleanup tail at `:1475-1488` shows `Remove-Item` failing
  **access-denied** on `C:\Users\Public\wpi_r3\qb\pd_evil\ssh\ssh_config`, with no closing
  `removed … exists=False` line. The integrity envelope asserts a cleanup the evidence shows did
  not complete.
- **FALSE — `:1598-1600` says J1–J6 are "RED and GREEN, ten runner executions".** The J-family
  banners number **eleven** (`:910`…`:1096`) and J5 appears only as GREEN at `:1060`.
- **UNSUPPORTED — `:1598-1601` "Twelve of those executions are the real pinned OpenSSH
  programs."** No transcript line prints 12, and neither reading of M7's eight rows yields it.
- **UNSUPPORTED — `:15-18` says `C:\WPI_ARTIFACTS` was checked after every fixture.** No
  transcript line shows that listing or check.

**Your judgement is wanted on one question:** are these documentary defects only, or does F-1's
incomplete cleanup mean a fixture left state behind that could affect a later arm's result? The
first is a repair-the-prose matter; the second would be a real finding.

**Already checked and NOT a defect:** the round-6 byte-identity language at `:2665-2669` is now
correctly scoped to the seven executable/plan targets and explicitly excludes the two QA/status
documents that legitimately changed. Do not re-flag it.

## Audit contract
1. Run the published fixture harness VERBATIM from
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md` (local WSL2 only);
   record real rc/stdout summary lines. Extract-and-run is forbidden — run the published
   commands exactly.

   **The published command is not copy-pasteable as written, and this is the one prerequisite
   you must satisfy first.**
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:2752-2755` carries the literal token
   `<scratch>/r6/pre` as its second argument; that directory is not shipped and no substitution
   is documented inline. The harness itself IS checked in:
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/_r5_wsl_fixtures.sh`, 21221 B, SHA-256
   `a2bb6f6e3c0022aa001db7adb58189649acab9b23b522dc0544b018f9ce7971b`. Per
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_R6_REPORT_2026-08-11.md:269-272`,
   the pre-repair arm needs the round-4 close-script blob materialized first:

   ```
   git cat-file blob 61696132a5f2fce97aad4054d41a780297ff21a1 > <scratch>/r6/pre/remote_close_tree_wpi.sh
   ```

   Then pass that directory as the harness's **second argument** (argument 1 is
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT`), exactly as `:2752-2755` shows. The blob is
   28756 B and its SHA-256 is
   `29b6412a466c10854ddf09effc8d5216317738a012235ce563c9764a9e0c40ef`. `git cat-file` is a read
   operation and mutates nothing; it is the only Git command this lane needs.

   *External evidence: that blob size and full digest are the
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/remote_close_tree_wpi.sh` row of the
   per-file census at
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md:2329`. The 21221 B /
   `a2bb6f6e…` harness identity above was re-derived from the current repository bytes of
   `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/_r5_wsl_fixtures.sh`. Neither is proved by a line
   of this kickoff; confirm both before you run anything.*
2. Adversarially test the first-mismatch semantics, per-branch cleanup prerequisites
   (07<-04, 08<-05, 09<-07, 10<-08, 11<-07+09, 12<-08+10) and the per-operation provenance
   binding — the classes the Codex rounds closed. Look for a class Codex missed.
3. Judge the six derivation classes and the disclosed residuals (F1, inherited-TMPDIR
   removal) for honest scoping: a disclosure is not a control, but an explicitly-labelled
   weaker claim honestly scoped IS acceptable where ratified.
4. Thirteen-pattern adjudication table. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES /
   BLOCK. If accepting, state that transport reaches DUAL FLAGSHIP ACCEPTANCE (Codex + Claude).

Write ONE new file: `TRANSPORT_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md` (this directory).
**Delta gate (corrected 2026-08-12 ~20:35 — a global clean-status gate CANNOT pass in this
worktree, which carries ~100 pre-existing untracked run logs, and would have self-blocked this
lane).** Instead:
1. **Before execution** capture `git status --porcelain` → `before`.
2. Run the lane.
3. **At the end** capture `git status --porcelain` → `after`, and prove `after` minus `before`
   contains **only** `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`
   and nothing else. Any other entry in the delta **fails** the gate.
4. Also run `git status --porcelain -- MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`
   and record its output as the path-scoped confirmation.
