# KICKOFF — B3-GAP-ENV repair round 2 (apply audit findings)

You are the same counterpart implementer (Claude Max) continuing the repair cycle.
Round 1 received REQUEST_CHANGES. Apply the required changes and nothing else. Write
the revised full deliverable set into `round2/` next to this file. ASCII only. English
only. Do not touch any file outside `round2/`.

## Inputs (read these, nothing else)

- This file.
- `audit1/AUDIT1_REPORT.md` — the adversarial audit. Its findings F1–F6, nit N1, and
  open-item rulings O1/O2/O3/O5 (must change) + O4/O6/O7 (accept as-is) are BINDING;
  the Lead has reproduced F4 and F6 on the real library source.
- `KICKOFF_B3_GAP_ENV_OPTION1.md` — the original brief (still in force except where
  the audit supersedes it: the audit's F1 explicitly changes the binding-check brief
  from grep to a structural JSON parse, and F5 narrows the blanket
  "any other error class is STOP").
- `round1/` — your previous deliverables (the baseline you are revising).
- `../01_RUNKIT/RP0-LIB.sh` — library context (do not modify it; where its helpers are
  unsound for your blocks — F4 temp files, F6 unguarded `tr` — implement local
  replacements inside your scripts instead, with a comment naming the library line you
  are deliberately not using and why).

## Required changes (map each to the audit)

1. **F1**: replace both `grep -qsF` binding checks in RPD-VERIFY with a silent
   structural JSON verification via `python3` (host has 3.12): parse the whole file,
   reject duplicate keys (`object_pairs_hook`), require a single top-level object, and
   compare the two top-level string values exactly. rc 1 = semantic mismatch (either
   value wrong or key absent), rc 3 = read/parse/tool failure, including python3
   absent. No manifest content is ever printed.
2. **F2**: before touching either leaf, assert `/etc/mtc-bridge` at the literal
   canonical path is a non-symlink directory with the expected numeric mode/owner, and
   add a fail-closed mount-boundary predicate (no mount target under the directory per
   `/proc/self/mounts`; unreadable proc = STOP).
3. **F3**: all ownership comparisons numeric (`stat -c '%u:%g'` vs `0:0`); add a
   fail-closed namespace check binding execution to the initial namespaces (compare
   `/proc/self/ns/user` and `/proc/self/ns/mnt` identity to `/proc/1/ns/*`; unreadable
   = STOP, mismatch = STOP with its own reason).
4. **F4 + O3**: no temp files anywhere in the new code. Replace `rp0_probe_path` usage
   in RPD-VERIFY and in the B3 boundary probe with local no-temp classifiers
   (capture stderr into a shell variable, classify from the captured text and rc).
   State the mutation surface honestly in both headers (none).
5. **F5 + O1**: in the B3 boundary probe, route ENOENT to `b3_fail` with a dedicated
   reason (search permitted, name absent = host more open than accepted state); STOP
   only for outcomes that do not establish whether entry was permitted.
6. **F6 + O5**: every diagnostic-sanitization step (`tr`, variable capture) explicitly
   adjudicated; on its failure emit a STOP reason and exit 3. No raw tool status may
   escape as the script's exit code.
7. **O2**: both blocks emit a reasoned STOP (rc 3) for a missing preregistered input.
8. **N1**: SELF_QA reports three separate exact counts — delivered-code arms actually
   run, stubbed arms, inherited arms not re-run — and claims only what was run.
9. Errno discipline from audit §2: where the code classifies EACCES, prefer a
   mechanism closer to the errno than prose matching if achievable in portable bash;
   if you keep message matching, pin `LC_ALL=C` on every producer and say in the
   header that the classification is message-based and why that is acceptable here.

Keep O4/O6/O7 as they are (accepted). Do not weaken anything that passed round 1.
Update DESIGN_NOTES with a per-finding "how addressed" section. Deliverables: the same
four files, revised, in `round2/`.
