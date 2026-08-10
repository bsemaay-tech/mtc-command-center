# KICKOFF — C13 final bounded round: newline-only rc-2 capture fix (finding 1 of the re-audit)

You are Claude Opus 5, implementer of round 3, closing the single surviving code finding
from `RP6_C13_REAUDIT_CODEX_2026-08-10.md`. This is the LAST round under the T0 cap —
the fix must be exact and minimal. Working directory: C:\LAB\Tradingview_LAB_CLEAN.

## The finding (HIGH)

`RP6-P0.sh:673` captures getent output via command substitution, which strips trailing
newlines; the emptiness test at :677-681 therefore admits a newline-only rc-2 capture
as a valid no-match. Required: a capture mechanism that preserves trailing bytes so
newline-only output at rc 2 is classified `error` → caller emits
`identity_unresolvable` rc 3. Canonical shape:

```bash
raw="$(LC_ALL=C "$P0_GETENT" passwd "$acct" 2>&1; printf x)" || rc=$?
raw="${raw%x}"
```

(mind rc capture semantics: the command's rc, not printf's — capture rc inside the
substitution, e.g. `raw="$( { LC_ALL=C "$P0_GETENT" passwd "$acct" 2>&1; printf "x%s" "$?"; } )"` style is NOT required; pick a correct minimal form and prove it in QA).

Lead adjudication of finding 2 (package isolation): the extra committed log file was
added by the Lead at commit time, not by the round-3 implementer; recorded as an
accepted Lead-side deviation — no repair, do not touch it.

## Scope

1. Fix the capture in `RP6-P0.sh` (that one site; if the same substitution-stripping
   pattern exists at other rc-2-adjudicated capture sites in the C13 arm, fix those
   identically and list them).
2. Extend `SELF_QA_RP6.md` harness 1 with the newline-only rc-2 fixture: RED on the
   current bytes (`ef205e20…` — reproduce `FALSE_NOMATCH_REPRODUCED=yes`), GREEN on
   repaired bytes (`identity_unresolvable` rc 3). Real local runs only.
3. Update `STATUS_RP6_P0.md` + append disposition to `RP6_C13_REPAIR_R3_REPORT.md`
   (round 4 section).

`bash -n` PASS; record new SHA-256 + bytes. Touch ONLY those four files. Do not commit.
