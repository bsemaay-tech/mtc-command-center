# AI-memory rotation — T2 status — 2026-08-17

## Scope

The bounded rotation covers only the three live onboarding files and three new
verbatim archives named in
`AI_MEMORY_ROTATION_GATE1_2026-08-17.md`. It is a documentation/evidence scope,
classified **T2**. It authorizes no deletion, worktree retirement, host action,
credential access or trading change.

## Implementer result

Claude `claude-opus-5`, effort `medium`, produced a lossless split:

- live `GLOBAL_HANDOFF.md`: original lines 1–245 plus a reconstruction pointer;
- archive: original lines 246–2828 verbatim;
- live `NEXT_STEPS.md`: original lines 1–230 plus a reconstruction pointer;
- archive: original lines 231–2729 verbatim;
- `START_HERE.md`: stale 2026-08-12/13 banner replaced with a neutral live-state
  pointer; removed banner archived verbatim.

The contract named START_HERE lines 3–9, but the blockquote actually ended at
line 10. The implementer removed and archived lines 3–10 so the last banner line
was not left orphaned. This deviation is explicit in the archive header.

## Lead-reproduced evidence

- `GLOBAL_HANDOFF` reconstruction: 207,895 bytes, SHA-256
  `c6abba25c2e5e9c9832e52259437717326be58e0d176937cff2487d6fda6c08c`.
- `NEXT_STEPS` reconstruction: 198,155 bytes, SHA-256
  `e1c085d82977c96f151f6f29d980fccdf1e8ffce029244b59b53c5e93e869015`.
- `START_HERE` reconstruction with the preserved separating blank line: 7,263
  bytes, SHA-256
  `b3873547f7df4403cbfead91be599a63e7c5d3dbb3996ec42030788d78bc5368`.
- GLOBAL/NEXT live and archive files remain pure LF; START_HERE live/archive
  remain pure CRLF.
- Archive markers are unique; payload moved without summary, reorder or task
  closure; `git diff --check` passes.

## T2 reviewer attempt — no verdict

GLM was unavailable because its usage window had reached quota. The permitted
DeepSeek reviewer independently reproduced all three reconstruction hashes,
the justified START_HERE line-10 deviation, unique markers, line endings and
the neutral live pointer. It then exhausted its 24-iteration harness budget
without calling `finish()` and therefore returned **no formal verdict**.

This is not acceptance. The T2 one-round cap is treated as consumed pending an
explicit cap ruling/waiver. The six rotation files remain uncommitted and must
not be silently accepted, discarded or handed to another reviewer as an extra
round.

## Current decision boundary

The rotation is mechanically proven lossless and would reduce recurring live
onboarding reads substantially, but it remains **review-complete in substance,
formally unaccepted**. Preserve the six-file working-tree diff until the owner
decides whether the missing final verdict may be completed in a fresh bounded
T2 review.

