# AI Memory File Classification — Batch 2

**Date:** 2026-08-17
**Mode:** read-only classification; this report is the only write
**Repository:** `C:\LAB\Tradingview_LAB_CLEAN`
**Result:** all 62 files currently present under `_AI_MEMORY` reconcile to Batch 1 or this Batch 2, with no missing or duplicate path.

## 1. Scope and safety boundary

This report completes the file-by-file classification begun in `AI_MEMORY_FILE_CLASSIFICATION_BATCH1_2026-08-17.md`. It classifies the 19 current files that Batch 1 deliberately excluded or did not substantively cover. Batch 1's 43 classifications are carried forward without reinterpretation.

This task did not edit, move, archive, compact, delete, stage, or commit any memory file. It did not touch the pending six-file rotation, `IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md`, code, hosts, secrets, or an existing report.

Verdicts have the same no-loss meaning as Batch 1:

- **KEEP:** retain as a current authority, stable pointer, operational record, or deliberately ignored tool artifact.
- **HOLD:** leave in place until a named dependency, acceptance step, or ambiguity is resolved.
- **ROTATE-CANDIDATE:** retain a stable entry point while losslessly moving historical payload behind it.
- **ARCHIVE-CANDIDATE:** preserve a historical artifact verbatim behind an indexed old-path-to-new-path record.

No verdict authorizes deletion.

## 2. Full coverage reconciliation

The filesystem inventory, including the hidden ignored tool cache, contains **62 files, 1,289,332 bytes, and 16,124 physical lines**.

| Coverage set | Files | Bytes | Lines | Reconciliation |
|---|---:|---:|---:|---|
| Batch 1 substantive classifications | 43 | 773,240 | 8,721 | Carried forward unchanged |
| Batch 2 classifications below | 19 | 516,092 | 7,403 | Every remaining current file |
| **Total current `_AI_MEMORY` inventory** | **62** | **1,289,332** | **16,124** | **Missing 0; duplicate 0** |

Batch 1 already covers the current provider/routing record, strategy-research workflow and checklist, generated repository map, canonical rules/decision/safety files, three pre-August archives, 11 historical programme files, and 14 June parallel prompt/report files. Batch 2 therefore does not reclassify them.

Batch 1's carried-forward verdict count is:

- **KEEP:** 12 files
- **HOLD:** 4 files
- **ROTATE-CANDIDATE:** 2 files
- **ARCHIVE-CANDIDATE:** 25 files

The important carried-forward dependencies remain:

- `AI_ACCOUNT_AND_MODEL_ROUTING.md`: KEEP as the operational provider/account index; `AGENTS.md` remains policy authority.
- `STRATEGY_RESEARCH_WORKFLOW.md` and `STRATEGY_CODE_REVIEW_CHECKLIST.md`: KEEP as permanent workflow authorities.
- `AI_RULES.md`, `PROJECT_MEMORY.md`, `REVIEW_CHECKLIST.md`, and `SPRINT_WORKFLOW.md`: HOLD until stale memory-routing or audit-round wording is repaired.
- `REPO_MAP.md` and `STRATEGY_COMPONENT_LIBRARY.md`: ROTATE-CANDIDATE because generated counts or role descriptions are stale.
- The 11 June plans/snapshots and 14 parallel prompt/report files: ARCHIVE-CANDIDATE, verbatim only.

## 3. Pending six-file lossless rotation — HOLD

These files are concurrently owned by the shared-memory workstream. Their current content describes a deterministic, lossless split, but the changes are still uncommitted in this worktree. This report does not accept, alter, or complete that rotation.

| File | Bytes | Lines | Current role | Verdict | Prerequisite before final KEEP |
|---|---:|---:|---|---|---|
| `GLOBAL_HANDOFF.md` | 17,025 | 259 | Current cross-session handoff plus archive pointer | HOLD | Independently reconstruct and hash the pre-rotation 207,895-byte/2,828-line original; verify pointer and open-item discoverability; review and commit the exact pair |
| `archive/GLOBAL_HANDOFF_2026-08-01_to_2026-08-15.md` | 192,596 | 2,598 | Verbatim historical payload for the live handoff split | HOLD | Same paired reconstruction, SHA-256, byte-boundary, diff, and commit verification |
| `NEXT_STEPS.md` | 15,969 | 243 | Current work queue plus archive pointer | HOLD | Independently reconstruct and hash the pre-rotation 198,155-byte/2,729-line original; prove archived open items remain searchable; review and commit the exact pair |
| `archive/NEXT_STEPS_2026-08-01_to_2026-08-10.md` | 183,969 | 2,514 | Verbatim historical payload for the live queue split | HOLD | Same paired reconstruction, SHA-256, byte-boundary, diff, and commit verification |
| `START_HERE.md` | 6,881 | 66 | Canonical onboarding index and current-state router | HOLD | Verify the new live-state directions against current authorities and verify the archived banner is exact before accepting the rotation |
| `archive/START_HERE_STALE_BANNER_2026-08-12.md` | 1,584 | 24 | Verbatim preservation of the removed stale onboarding banner | HOLD | Verify its recorded original-line range and SHA-256, then review and commit it with `START_HERE.md` |

The live/archive handoff and queue pairs record deterministic reconstruction hashes (`c6abba25...` and `e1c085d8...`). Those are claims to verify, not acceptance evidence from this classification. After exact reconstruction, pointer, review, and commit checks pass, all six should become KEEP: the live files as compact stable entry points and the archive files as immutable history.

## 4. Large historical working-set journal

| File | Bytes | Lines | Current authority/dependencies | Verdict | Exact reason and prerequisite |
|---|---:|---:|---|---|---|
| `ACTIVE_FILES.md` | 66,766 | 1,007 | Historical active-set journal, dated 2026-07-20 through 2026-08-01; still referenced by `AI_RULES.md`, `PROJECT_MEMORY.md`, `REVIEW_CHECKLIST.md`, prompts, and older records | HOLD | It is the largest remaining live-path outlier outside the pending rotation, but retiring it now would break workflow instructions and could hide unresolved ownership. First repair current authorities, map every still-open item to `GLOBAL_HANDOFF.md`/`NEXT_STEPS.md`, preserve the full old payload verbatim with SHA-256 and old/new paths, and leave a stable redirect or tombstone |

`ACTIVE_FILES.md` is not safe for immediate archival merely because its newest heading is dated 2026-08-01. The prerequisite is semantic reconciliation: every record that is still operational must have an explicit current destination, while superseded records remain searchable in a verbatim archive.

## 5. Live concurrency authority

| File | Bytes | Lines | Current authority/dependencies | Verdict | Exact reason and prerequisite |
|---|---:|---:|---|---|---|
| `SESSION_LOCK.md` | 15,768 | 228 | Canonical one-writer-per-workstream protocol, ownership table, and lock history; consumed by concurrent agents and memory workflow rules | KEEP | It currently records active owners, including the shared-memory and Help/System Map workstreams. Moving or compacting it during active work could create a write collision. Keep the protocol and current table at the stable path. Any later rotation may move only closed log history after all active rows and references are rechecked |

The current shared-memory ownership row belongs to Codex Lead `01a00921` for the owner-authorized overnight programme. That is an additional reason this classification report stays outside `_AI_MEMORY` and makes no memory edit.

## 6. June 7–8 recovery/result cohort — ARCHIVE-CANDIDATE

These ten small files are point-in-time completion, fix, run-enrichment, selector, strategy-label, and verdict records. They remain useful provenance, but none is a current execution, promotion, backtest, or trading authority. Preserve them together and verbatim.

| File | Bytes | Lines | Authority/dependency | Verdict |
|---|---:|---:|---|---|
| `SESSION_RECOVERY_2026-06-07.md` | 2,013 | 45 | Final recovery summary marked “ALL DONE”; linked by the June result chain | ARCHIVE-CANDIDATE |
| `RESULT_AI_STRATEGY_NAMES_codex.md` | 1,665 | 41 | June 8 strategy-display naming result; provenance for its registry work | ARCHIVE-CANDIDATE |
| `RESULT_BATCH023_034_MCC_TAIL_codex.md` | 1,649 | 61 | June 8 finished-run MCC enrichment evidence | ARCHIVE-CANDIDATE |
| `RESULT_EXPERT_QUANTLENS_VERDICTS_codex.md` | 1,678 | 44 | June 8 expert-verdict layer provenance | ARCHIVE-CANDIDATE |
| `RESULT_FULL_SWEEP_MCC_TAIL_codex.md` | 1,654 | 61 | June 8 full-sweep MCC enrichment evidence | ARCHIVE-CANDIDATE |
| `RESULT_MCC_NIGHT_TAIL_D009_codex.md` | 1,436 | 51 | June 8 D009/D008 guard result | ARCHIVE-CANDIDATE |
| `RESULT_NEEDS_BACKTEST_SELECTOR_codex.md` | 1,313 | 38 | June 8 read-only selector result; not current launch authority | ARCHIVE-CANDIDATE |
| `RESULT_NIGHT_1M_MCC_TAIL_codex.md` | 2,155 | 48 | June 8 overnight-container/MCC visibility result | ARCHIVE-CANDIDATE |
| `RESULT_SCIPY_SHIM_TOPLEVEL_codex.md` | 1,437 | 53 | June 8 top-level SciPy shim fix record | ARCHIVE-CANDIDATE |
| `RESULT_STRAY_PROCESS_CHECK_codex.md` | 507 | 21 | June 8 process check; explicitly time-bound | ARCHIVE-CANDIDATE |
| **Cohort total** | **15,507** | **463** | Historical provenance | **ARCHIVE-CANDIDATE** |

Prerequisites:

1. Build one manifest containing every old path, destination path, byte count, line count, SHA-256, Git identity, and incoming reference.
2. Preserve the entire payload of every file; do not merge apparently duplicate run prose.
3. Repair links from `CODEX_PICKUP_2026-06-08.md`, the June programme cohort, and any tracked checksum/provenance record.
4. Keep current backtest and promotion instructions pointed only to current canonical rules and runbooks.
5. Leave redirects at any old path still named by onboarding or an operational tool; otherwise record the mapping in a stable archive index.

## 7. Hidden generated cache

| File | Bytes | Lines | Current authority/dependencies | Verdict | Exact reason and prerequisite |
|---|---:|---:|---|---|---|
| `.impeccable/hook.cache.json` | 27 | 1 | Ignored tool cache (`.gitignore` covers `.impeccable/`); current payload is version 1 with an empty sessions object | KEEP | It is not AI-memory authority, is not loaded by onboarding, and offers no meaningful token saving. Leave it tool-owned and ignored; do not archive, track, or treat it as provenance |

## 8. No-loss repair and rotation order

### P0 — accept or reject the in-flight six-file rotation

1. Respect the current shared-memory lock owner.
2. Reconstruct the two pre-rotation originals byte-for-byte and verify their recorded SHA-256, byte, and line claims.
3. Verify the `START_HERE.md` banner extraction the same way.
4. Check archive pointers, open-item discoverability, whitespace/diff, and exact changed-file scope.
5. Apply the appropriate documentation review and commit the rotation as one coherent accepted package. Until then, all six remain HOLD.

### P0 — repair current memory authorities before retiring dependencies

1. Update `AI_RULES.md`, `PROJECT_MEMORY.md`, and `REVIEW_CHECKLIST.md` so the accepted live handoff/queue design is authoritative and retired `SESSION_LOG.md`/historical `ACTIVE_FILES.md` behavior is no longer prescribed.
2. Correct `SPRINT_WORKFLOW.md` so repair caps come from the tier policy rather than a blanket three-round statement.
3. Verify `START_HERE.md` links only to current authorities plus clearly labelled historical pointers.

This package must precede any `ACTIVE_FILES.md` move.

### P1 — rotate `ACTIVE_FILES.md` losslessly

1. Classify each record as current, closed, superseded, or unresolved without deleting any category.
2. Move current/unresolved actions into the accepted current handoff/queue with provenance links.
3. Archive the full original bytes with SHA-256 and deterministic reconstruction instructions.
4. Keep a compact stable-path pointer if any incoming reference remains.
5. Verify all incoming links before accepting the rotation.

### P1 — refresh generated indexes from source

1. Regenerate `REPO_MAP.md` mechanically from the current repository.
2. Regenerate `STRATEGY_COMPONENT_LIBRARY.md` from the current registries/directories.
3. Independently verify counts and authority wording. Preserve human guidance that is not generated elsewhere.

### P2 — archive the June historical cohorts

Archive, as separate indexed groups:

- the ten recovery/result files in Section 6;
- Batch 1's 11 June programme/snapshot files;
- Batch 1's 14 prompt/report pairs.

Each group needs a manifest, verbatim payloads, hashes, old/new path mapping, reference repair, and stable redirect where required. Do not deduplicate decisions, evidence, gates, commands, or provenance across groups.

### P2 — consider `SESSION_LOCK.md` history rotation only after quiescence

The protocol and current ownership table must remain live at the same path. A future package may move only closed historical log entries after all active claims are released or deliberately preserved and all consumers are verified. This is optional and lower priority than correctness repairs.

## 9. Do-not-touch and retention invariants

- Never delete or summarize away owner decisions, provenance, audit gates, rejected findings, unresolved work, deployment identities, hashes, commands, or evidence links.
- Never infer that an archived open item is closed merely because it left the live file.
- Never rotate a file while it or its workstream has an active `SESSION_LOCK.md` owner without that owner's serialized package.
- Never collapse prompt/report or decision/evidence pairs into one prose summary.
- Never use historical June backtest records as current promotion or execution authority.
- Keep stable entry points for onboarding and for any old filename with unresolved incoming references.
- Verify byte counts, SHA-256, deterministic reconstruction, link repair, diff scope, review status, and commit identity before calling any rotation lossless.

## 10. Final classification result

Batch 2 verdicts for its 19 files are:

- **KEEP:** 2 (`SESSION_LOCK.md` and the ignored tool cache)
- **HOLD:** 7 (`ACTIVE_FILES.md` and the six pending rotation files)
- **ARCHIVE-CANDIDATE:** 10 (the June recovery/result cohort)
- **ROTATE-CANDIDATE:** 0 newly assigned in this batch

Combined with Batch 1, every one of the 62 current files is classified exactly once. No file remains UNKNOWN. HOLD is used where acceptance, live ownership, or dependency repair prevents a safe archival conclusion.
