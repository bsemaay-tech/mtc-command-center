# Legacy Repository Freeze Policy

- Decision date: 2026-05-31
- Applies to: `C:\LAB\tradingview-lab` (the pre-migration legacy tree)
- Phase 6 audit finding addressed: CHECK 1 ("Legacy frozen state" FAIL — informational)

## Verdict

Legacy tree is frozen by convention + Windows ReadOnly attribute. **No NTFS DACL deny-write is applied.**

## State at Decision Time (2026-05-31)

Verified directly:

```
C:\LAB\tradingview-lab git status  →  only `?? ARCHIVE_NOTICE.md` untracked (expected — Phase 3 output)
C:\LAB\tradingview-lab attrib       →  R (directory ReadOnly attribute set)
CLAUDE_CONTINUATION_2026-05-31.md   →  IsReadOnly=True, no tracked modifications vs HEAD
git diff HEAD --stat                →  empty (no tracked content diverges from last commit `3b484f87`)
```

The transient modification recorded in `phase6_audit_report.md` CHECK 1
(`M CLAUDE_CONTINUATION_2026-05-31.md` with the "Codex continuing" one-line
edit) is no longer present. Either the edit was reverted, or the working
copy was restored before this policy decision was applied. Either way, the
clean-tree migration is unaffected and Pine byte-stability is intact
(Phase 6 CHECK 4: 24/24 SHA256 match).

## Why Accept-And-Document, Not NTFS Deny-Write

NTFS DACL deny-write (`icacls C:\LAB\tradingview-lab /deny "Users:(W)" /T`)
was considered and rejected for these reasons:

1. **Reversibility cost.** Removing a recursive deny ACE requires `icacls /remove:d`
   per principal, and mistakes compound (e.g. denying SYSTEM or a wrong SID can
   make the tree harder to clean up without elevation).
2. **Blast radius.** A deny ACE applies to *all* operations by the targeted
   principal, including read-side workflows like SHA recomputation, archive
   copy, or future forensic investigation. The directory ReadOnly attribute
   plus the convention is lower-impact.
3. **No measurable benefit over current state.** The clean tree is the only
   active workspace. Legacy is referenced only for SHA cross-checks and
   evidence inspection — both read-only operations.
4. **Phase 6 audit confirmed the migration delivered its safety invariant.**
   Pine bytes match the manifest. The transient legacy edit did not propagate
   into the clean tree.

## Policy

Going forward:

- **Do not edit anything under `C:\LAB\tradingview-lab`.** Treat the tree as
  read-only by convention. The directory ReadOnly attribute is advisory but
  is the only access-control gate.
- **Active work happens exclusively in `C:\LAB\Tradingview_LAB_CLEAN`.**
- **ARCHIVE_NOTICE.md** is the canonical signal that the tree is frozen.
  Any agent that lands in legacy should read it and stop.
- **If an agent must read from legacy** (SHA cross-check, evidence lookup),
  use read-only Git operations (`git log`, `git show`, `git diff`,
  `git ls-files`) and never `git add` / `git commit` inside legacy.
- **If accidental modification happens**, revert via
  `git -C C:\LAB\tradingview-lab restore <path>` and document the incident
  in this file under "Incident log" below.
- **Periodic verification** can be run from the clean tree:
  ```powershell
  Push-Location C:\LAB\tradingview-lab
  git status --porcelain
  Pop-Location
  ```
  Expected output: a single `?? ARCHIVE_NOTICE.md` line and nothing else.

## When NTFS Deny-Write Would Be Reconsidered

The accept-and-document stance can be revisited if:

- Repeated unintentional modifications to legacy are observed despite the
  convention (≥2 separate incidents), OR
- A specific compliance / audit requirement mandates immutable archive
  evidence, OR
- The tree is moved to a long-term archive volume where read access is
  the only required permission for any future user.

If reconsidered, the safer alternatives in order of preference would be:

1. Rename to `tradingview-lab_ARCHIVE_2026-05-31` (already covered by the
   restore command in `ARCHIVE_NOTICE.md`) and move under a clearly
   archival path.
2. Copy to a 7-zip archive with stored hash and remove the working tree.
3. NTFS DACL deny-write only on `Modify` for the specific principal that
   was observed modifying the tree, not recursive blanket-deny on `Users`.

## Incident Log

- 2026-05-31, Phase 6 audit: transient `M CLAUDE_CONTINUATION_2026-05-31.md`
  observed by audit, reverted/restored before this policy was written.
  Resolution: convention proved sufficient — no follow-up required.
