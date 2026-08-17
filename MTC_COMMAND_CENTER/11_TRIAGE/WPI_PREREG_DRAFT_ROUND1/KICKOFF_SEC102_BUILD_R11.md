# KICKOFF — SEC102 round 11: the STRUCTURAL FIXPOINT for executed-byte binding (Codex r10, last two findings)

You are `claude-opus-5` xhigh via the Max account, IMPLEMENTER. Codex audits r11. Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no commit. Scope fence: touch ONLY
`SELF_QA_SEC102_R11.md` (new — carry forward r10, replace the §13 wrapper), `STATUS_SEC102.md`,
`SEC102_R11_REPORT_2026-08-12.md`, scoped `.gitattributes` (only if you add a fixture).
`composite_pathproof.py` MUST stay UNTOUCHED (129658 B, SHA-256
`adbf27fd908439e1d48e6c95a4eecba956c0607c42ae5a3bfa9cb210b636c05a`). Do NOT touch
`pathscope_prover.py`, block files, RP6/RP7, prereg drafts. Never git checkout/reset/stash.

## This is the FIXPOINT round — read this framing first
This is the FOURTH consecutive evidence-harness round (r7 child-status → r8 newline → r9
direct-object TOCTOU → r10 transient rebind). Each round closed the previous instance and the
auditor found a subtler temporal variant of the SAME executed-byte-binding class. STOP patching
instances. The lesson from this project's two other regresses — RP6's exact-byte-span census and
SEC102's command-word whitelist — is that the regress ends only when you INVERT to a
fail-closed structural construction that removes the whole leaky layer at once. Here the leaky
layer is **mutable name resolution**: every finding since r9 exploits that
`powershell.exe -File <pathname>` (and every path component) is re-resolved through DOS-device/
volume/drive-letter mappings that a same-session actor can transiently re-point. Do not add a
third temporal sample. Remove the name resolution.

## Codex r10's two findings (both MEDIUM, Pattern 11) — the class, not two instances
1. `SELF_QA_SEC102_R10.md:1647-1654,1841-1852,2608-2617`: a transient volume/drive-letter rebind
   applied AFTER the pre-launch sample and restored BEFORE the post-run sample lets the child
   resolve the same pathname to different bytes; both snapshots match, alternate output is
   accepted. A post-run snapshot detects only a PERSISTENT rebind.
2. `SELF_QA_SEC102_R10.md:2514-2533,2557-2605`: leaf-to-root acquisition stores handles + a count
   but never proves the seven handles form ONE coherent current root-to-leaf chain; an ancestor
   renamed/replaced before its turn lets the set pin components from different historical chains;
   the already-passed lower name in the new live chain is unpinned. `PATH_PIN_HELD=7` proves
   seven opens, not that they bind the path PowerShell later resolves.

## Required structural repair (Codex's named route — implement the fixpoint, not a patch)
Bind execution to the pinned object through a channel with NO mutable name resolution. Concrete
route (choose the one you can prove; A preferred):

- **(A) Stable device/volume-GUID path + handle-relative chain.** From the leaf handle opened in
  r10, derive the STABLE identity that cannot be rebound by DOS-device/drive-letter remapping:
  `GetFinalPathNameByHandleW` with `VOLUME_NAME_GUID` (`\\?\Volume{GUID}\...`) or
  `FILE_NAME_NORMALIZED | VOLUME_NAME_NT` (`\Device\HarddiskVolumeN\...`), and hand THAT path to
  the interpreter, not the drive-letter path. Build the component chain by opening each child
  RELATIVE TO the already-pinned parent handle (`NtCreateFile`/`CreateFileW` with the parent as
  the root directory, or `O_*`-relative equivalents), so no intermediate name is resolved through
  a mutable mapping — every component's identity is proven adjacent to the one below it and the
  whole chain is one coherent current chain by construction. Assert the volume-GUID/device
  identity is stable (re-derive from the held handle and require equality) so a drive-letter
  remap cannot change what the child opens.
- **(B) Nameless consumption.** Feed the pinned, compared bytes to the interpreter with no path at
  all (child stdin pipe: `powershell -NoProfile -Command -`), only if you prove every published
  block's rc/`$ErrorActionPreference`/stderr contract is conserved under `-Command -`. If any
  block's contract changes, use A.

Explain in the report WHY the chosen construction removes the ENTIRE transient-rebind and
mixed-chain class (no post-run sample is load-bearing; there is no mutable resolution left to
race), the same way byte-span granularity closed RP6's line-granularity class.

## D026 evidence (required; harmless, deterministic, symbolic names — no attack fixture)
1. RED against the exact r10 wrapper for BOTH r10 findings: (a) a transient volume/drive-letter
   rebind applied across the child open and restored before the post-run sample — show r10
   FALSE-ACCEPTS; (b) an ancestor swap during pin acquisition — show r10 pins a mixed chain.
   If a live transient remap cannot be made deterministic, demonstrate the window's existence
   deterministically (hold the r10 sequence at the boundary and prove a remap+restore round-trips
   undetected by its two samples).
2. GREEN under r11: both attacks FAIL — the device/volume-GUID path the child opens is unchanged
   by the drive-letter remap (or there is no name), and the relative-open chain refuses a
   swapped ancestor. Show the real OS-level evidence.
3. Conserve ALL r10 gates verbatim behind the new binding (measured share-exclusion
   `WINERROR=32`, byte identity, status, stderr, subset) and re-run the eleven published blocks +
   outer wrapper from exact published bytes.
4. Make the "no path executes unproven bytes / terminal detection" sentences TRUE, or — if a
   provable residual genuinely remains below the filesystem (e.g. a raw-disk/kernel actor) —
   state it as an explicitly out-of-model, out-of-threat-model disclosure, not as a detected
   control. Update STATUS: item 43 names the fully closed class; retire/rewrite residuals 45-49
   as the construction closes them.

## Deliverables
`SELF_QA_SEC102_R11.md` + `STATUS_SEC102.md` + `SEC102_R11_REPORT_2026-08-12.md`. 58-case matrix
and all carried fences pass. No commit — the Lead commits and reproduces the wrapper + D026
verbatim. **If this construction still leaves a same-session, in-model divergence path, say so
plainly in the report** — the Lead will then stop the harness hardening and bring an
accept-with-disclosure recommendation to the owner rather than open round 12.
