# KICKOFF — Claude Pro T0 audit: WP-I transport set, SECOND FLAGSHIP (dual-acceptance gate)

You are `claude-opus-5` xhigh via the default Claude Pro account, AUDITOR — the second
flagship. Codex `gpt-5.6-sol` already holds flagship PASS on these bytes
(`TRANSPORT_CODEX_R6B_CONFIRM`, r4→r6 closed the F1 overclaim, BA-1/BA-2/BA-3,
R5-F1/F2/F3). You are a FRESH session and did not implement any transport round — Max
implemented r4–r6, so implementer/auditor separation holds. Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. Read-only on the repo: edit nothing except your verdict
file, no git mutation, no remote host, no network. Local WSL2 fixture execution under
`/root/wpi_r*` is permitted exactly as the published harness does it.

## Bytes under audit
The transport set as committed on `feature/donchian-crypto-ladder` — start from
`STATUS_TRANSPORT.md` (this directory) which pins the round-6 state, then
`SELF_QA_TRANSPORT.md` for the published harness and evidence. Do not trust the status
narrative: verify it against the bytes.

## Binding context you must respect
1. **F1 (outer SSH account-shell boundary) is honestly OPEN and OWNER-RATIFIED 2026-08-12
   as ACCEPT-WITH-DISCLOSURE** — an inherent SSH-trust-model limit, not a freeze blocker.
   Do not demand its closure; DO verify no text claims the inner-child `env -i` domain as
   an end-to-end F1 closure, and that the disclosure is carried at every site.
2. `<ALLOCATE-AT-DISPATCH>`/`<PIN-AT-FREEZE>` stay literal with the preflight marker STOP.
3. No host contact, no RUNID allocation, no archive build — confirm the round performed none.

## KNOWN DOCUMENTARY DEFECTS — found 2026-08-12 evening, NOT yet repaired
A prose-vs-transcript audit (`WPI_SELFQA_CLAIM_AUDIT_TRANSPORT_PATHSCOPE_2026-08-12.md`) found
five claims in `SELF_QA_TRANSPORT.md` that its own transcripts do not support. **They are
disclosed here so you do not spend your slot rediscovering them — and so you can judge whether
they change any acceptance conclusion:**

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
1. Run the published fixture harness VERBATIM from `SELF_QA_TRANSPORT.md` (local WSL2 only);
   record real rc/stdout summary lines. Extract-and-run is forbidden — run the published
   commands exactly.
2. Adversarially test the first-mismatch semantics, per-branch cleanup prerequisites
   (07<-04, 08<-05, 09<-07, 10<-08, 11<-07+09, 12<-08+10) and the per-operation provenance
   binding — the classes the Codex rounds closed. Look for a class Codex missed.
3. Judge the six derivation classes and the disclosed residuals (F1, inherited-TMPDIR
   removal) for honest scoping: a disclosure is not a control, but an explicitly-labelled
   weaker claim honestly scoped IS acceptable where ratified.
4. Thirteen-pattern adjudication table. Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES /
   BLOCK. If accepting, state that transport reaches DUAL FLAGSHIP ACCEPTANCE (Codex + Claude).

Write ONE new file: `TRANSPORT_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md` (this directory).
Prove `git status --porcelain` shows only that file at the end.
