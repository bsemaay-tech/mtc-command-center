# W299B KERNEL probe variant rebuild report

Date: 2026-09-03
Actor: Codex implementer lane
Verdict: **STOPPED - PATCH RE-AUTHORING REQUIRED**
Finding count: **1**

## Result

No KERNEL variant was rebuilt. All nine unchanged `modification.patch` files apply to the current
HEAD core only at a non-zero line offset. The lane requires zero fuzz and zero offset and says to
stop the affected probe instead of editing its patch
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W299B_PROBE_VARIANT_REBUILD.md:29-31`). Because the same
condition affects every named KERNEL probe, steps 3-6 and the final probe-mode run were not reached
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W299B_PROBE_VARIANT_REBUILD.md:32-47`).

The repository rule for a KERNEL probe requires the base-to-variant change list to equal the one
declared file, then independently replays the recorded patch and compares the result to the variant
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2393-2402,2471-2497`).
The design likewise requires a fresh exact base copy plus exactly one recorded file patch, with no
other changed member
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:495-497`).

## Scope, preflight, and measurements

- Gate-1 classification: **T2**, because the only changed byte is this evidence report; no
  executable variant or kernel byte was changed. The repository defines T2 as docs/evidence
  (`AGENTS.md:38-40`).
- The prerequisite marker contains `exit=0`
  (`C:\tmp\LANE_PROMPTS_20260828\W304_DONE.txt:1`), and the requested branch/worktree conditions are
  defined at `C:\tmp\LANE_PROMPTS_20260828\LANE_W299B_PROBE_VARIANT_REBUILD.md:3-7`.
- The measured start commit was `858b02cb3d4a1c9ad956cbc68d04a4409a6edb92` and the mandated
  `git rev-parse HEAD:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core` measurement returned
  `457a06d6e5e67b255c2830be8989f4e0610fba63`; the lane mandates that exact measurement
  (`C:\tmp\LANE_PROMPTS_20260828\LANE_W299B_PROBE_VARIANT_REBUILD.md:23-24`).
- The live `economics.py` SHA-256 measured
  `2e5ff35807b9700a476e7cc645083a9e11143a79923a58290aaf8d5719304b9f`. Each current one-line
  modification manifest records that same `before_sha256`, declares `economics.py`, and binds its
  existing patch (for example,
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-A/modification_manifest.json:1`;
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-08-A/modification_manifest.json:1`).
- Dry-run method for every row: `git -c core.autocrlf=false apply --check --verbose --unidiff-zero`
  and GNU `patch --dry-run --fuzz=0 --batch -p1`, both executed against the live core. Both returned
  process exit 0 but explicitly reported the same non-zero offset per row. Exit 0 therefore does not
  satisfy this lane's stricter zero-offset condition
  (`C:\tmp\LANE_PROMPTS_20260828\LANE_W299B_PROBE_VARIANT_REBUILD.md:29-31`).
- No backtest, optimization, server, launcher, broker, venue, host, or network action was run. Only
  read-only patch checks were used; local tests and verifiers are permitted
  (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:33-36`).

## Per-probe stop table

The patch header and live-line citations below show the exact reason for each measured offset. In
every row, the declared changed file is `economics.py`; `after_sha256`, the two new manifest
digests, diff stat, and artifact check are **NOT PRODUCED / NOT RUN** because the mandatory stop
occurs before those steps
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W299B_PROBE_VARIANT_REBUILD.md:29-41`).

| Probe | Core tree OID | Patch target -> live line | Measured dry-run result | after SHA-256 | New modified-copy / modification-manifest digests | Diff stat | Artifact check |
|---|---|---|---|---|---|---|---|
| `PROBE-P012-01-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | 240 -> 242 (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-A/modification.patch:3-5`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:242`) | `Hunk #1 succeeded at 242 (offset 2 lines)` | NOT PRODUCED | NOT PRODUCED / NOT PRODUCED | NOT RUN | NOT RUN |
| `PROBE-P012-01-B` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | 241 -> 243 (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-B/modification.patch:3-5`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:243`) | `Hunk #1 succeeded at 243 (offset 2 lines)` | NOT PRODUCED | NOT PRODUCED / NOT PRODUCED | NOT RUN | NOT RUN |
| `PROBE-P012-02-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | 646 -> 649 (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-02-A/modification.patch:3-5`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:649`) | `Hunk #1 succeeded at 649 (offset 3 lines)` | NOT PRODUCED | NOT PRODUCED / NOT PRODUCED | NOT RUN | NOT RUN |
| `PROBE-P012-04-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | 544 -> 547 (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-04-A/modification.patch:3-5`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:547`) | `Hunk #1 succeeded at 547 (offset 3 lines)` | NOT PRODUCED | NOT PRODUCED / NOT PRODUCED | NOT RUN | NOT RUN |
| `PROBE-P012-05-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | 275 -> 277 (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-05-A/modification.patch:3-5`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:277`) | `Hunk #1 succeeded at 277 (offset 2 lines)` | NOT PRODUCED | NOT PRODUCED / NOT PRODUCED | NOT RUN | NOT RUN |
| `PROBE-P012-05-B` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | 275 -> 277 (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-05-B/modification.patch:3-5`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:277`) | `Hunk #1 succeeded at 277 (offset 2 lines)` | NOT PRODUCED | NOT PRODUCED / NOT PRODUCED | NOT RUN | NOT RUN |
| `PROBE-P012-06-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | 787 -> 791 (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-06-A/modification.patch:3-5`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:791`) | `Hunk #1 succeeded at 791 (offset 4 lines)` | NOT PRODUCED | NOT PRODUCED / NOT PRODUCED | NOT RUN | NOT RUN |
| `PROBE-P012-07-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | 299 -> 302 (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-07-A/modification.patch:3-5`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:302`) | `Hunk #1 succeeded at 302 (offset 3 lines)` | NOT PRODUCED | NOT PRODUCED / NOT PRODUCED | NOT RUN | NOT RUN |
| `PROBE-P012-08-A` | `457a06d6e5e67b255c2830be8989f4e0610fba63` | 1132 -> 1172 (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-08-A/modification.patch:3-5`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py:1172`) | `Hunk #1 succeeded at 1172 (offset 40 lines)` | NOT PRODUCED | NOT PRODUCED / NOT PRODUCED | NOT RUN | NOT RUN |

## Finding

### W299B-F01 - All nine existing patch headers are stale against the current core

The patches still identify their intended old line by exact content, but every hunk requires a
non-zero offset on the current HEAD core. This is the lane's explicit probe re-authoring stop, so
the Lead must decide whether to authorize new patch bytes; this lane expressly forbids changing
`modification.patch`
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W299B_PROBE_VARIANT_REBUILD.md:8-11,29-31`).

No variant-tree, tree-manifest, modification-manifest, catalog, main manifest, anchor, core,
harness, golden, or patch byte changed. Probe commit hashes: **none**, because all nine stopped at
step 2. The only planned commit is this required report
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W299B_PROBE_VARIANT_REBUILD.md:49-52`).

## Discrepancies

1. The lane's normal rebuild path cannot execute with the repository as observed: every unchanged
   patch requires a non-zero offset, while the task requires zero offset and forbids patch edits
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W299B_PROBE_VARIANT_REBUILD.md:29-31`; per-probe patch and
   live-core citations in the table above). This discrepancy is handled by the specified STOP.
2. The lane's explanatory citation says the verifier's KERNEL diff check is at
   `verify_bceg.py:2339-2382`
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W299B_PROBE_VARIANT_REBUILD.md:14-16`), but current HEAD
   performs the member-set and changed-file checks at
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2393-2402`.
   The cited line range moved after the prompt was written; the behavior remains the described
   exact-one-file check.
