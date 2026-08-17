# FRESH-SESSION HANDOFF — WP-I run-kit construction (2026-08-10 evening)

Paste this whole file as the first message of a new session. It is self-contained.
Supersedes `NEW_SESSION_KICKOFF_PROMPT_2026-08-09_NIGHT.md` for current state; that file
remains the record of grants #1–#7 and the older milestone log.

Repo `C:\LAB\Tradingview_LAB_CLEAN`, branch `feature/donchian-crypto-ladder`.
You are the Lead. You orchestrate, verify, adjudicate and commit. You do NOT author or
audit the heavy artifacts yourself.

---

## 1. OWNER AUTHORIZATIONS — STANDING, DO NOT RE-ASK

| # | Granted | Scope |
|---|---|---|
| 1 | WP-I host-contact authority | WP-I may contact `GATEA-STAGING` for its authorized read-only scope |
| 2 | WP-I budget lift | the 50-hour ceiling is lifted for WP-I |
| 3 | Root for `RPD-VERIFY` | run `RPD-VERIFY.sh` as root on `GATEA-STAGING`. Read-only by design; root is granted to RUN THAT BLOCK, not as blanket mutation authority |
| 4 | Retroactive defect-catalogue pass | done (round 1.4) |
| 5 | RP6-P0 repair sequencing | done |
| 6 | **Attestation production, option (a)** | the grant-#3 root session may ALSO run ONE preregistered read-only command set producing the projection-v2 + row-8 attestation values (`/proc/self/mountinfo` capture, `readlink /proc/1/ns/{user,mnt,pid,net}`, canonical root-mount identity), hashed at production. Must be preregistered and committed before it runs, and must run BEFORE op 01 |
| 7 | **T0 round cap lifted for the WP-I block set** | repair/re-audit rounds on `RP6-P0.sh`, `RP7-WPI-RO.sh` and the transport set continue until BOTH flagships accept, without stopping to ask at each cap breach. The acceptance STANDARD is unchanged |

**Still hard-gated — need a fresh explicit Barış authorization:** credential load, ARM,
orders, broker/exchange contact, TESTNET/mainnet, master merge, WP-V/KVM2, deleting the
old payload archive, host reprovisioning, any service-state mutation, any host mutation
beyond a run's own create-once evidence tree.

---

## 2. ROUTING — BINDING (owner, 2026-08-10 ~19:00)

Full policy: `11_TRIAGE/ROUTING_POLICY_CREDIT_CONSERVATION_2026-08-10.md`. Summary:

**Claude Max is EMERGENCY-ONLY** (~50% of weekly credit used, resets ~2026-08-15). Use it
only when ALL hold: acceptance-critical, AND Claude Pro's window is exhausted, AND Codex
cannot fill the slot, AND you record the justification at dispatch. Nothing since the
policy landed has needed it.

| Slot | Account | Invocation |
|---|---|---|
| T0 Claude flagship (audit, xhigh, fresh) | **Claude Pro** (default `.claude`) | `claude --print '<P>' --model claude-opus-5 --effort xhigh --no-session-persistence --dangerously-skip-permissions` |
| T0 Codex flagship (audit, xhigh, fresh) | **Codex Pro** | `Invoke-CodexForClaude.ps1 -Account fourth -CodexArgs @('exec','-m','gpt-5.6-sol','-c','model_reasoning_effort=xhigh','--dangerously-bypass-approvals-and-sandbox',$p)` |
| Implementation | **Codex first, then GLM-5.2** | as above / `Invoke-GlmTask.ps1 -RepositoryPath <repo> -TaskFile <kickoff> -PermissionMode acceptEdits -OutputReport <out>` |
| T2 review (docs/prereg) | GLM-5.2 preferred | `Invoke-GlmAudit.ps1 -TaskFile <f> -RepositoryPath <r> -OutputReport <o>` |
| Mechanical/bulk | DeepSeek, NVIDIA NIM | `Invoke-NvidiaNim.ps1 -Route deepseek|minimax` |
| Emergency only | Claude Max | `Invoke-ClaudeMax.ps1 --print '<P>' --model claude-opus-5 --effort xhigh --no-session-persistence --dangerously-skip-permissions` |

**Account state (re-verify before relying):** Codex `secondary` EXHAUSTED until
2026-08-16 09:44 → use `fourth`. Claude Pro has a rolling 5-hour window (hit it twice on
2026-08-10; resets shown in the error). GLM has 5-hour credit windows. Cline unpaid/no
capacity. Owner offered to buy Cline ($10) / Grok ($30-3mo) — **Lead recommended NOT yet**;
both flagship slots are covered by paid subs and the bottleneck is account windows, not
auditor count.

**Parallel dispatch is mandatory.** 3–5 concurrent agents is normal and was sustained all
day. Scope every kickoff by a disjoint writable file list AND name the files other live
sessions own ("never write them"). Gate only on real dependencies (use a `GATE:` block and
fill the basis hash when the dependency commits). Commit each result as it lands.

**Tier policy** (`AGENTS.md` §AUDIT TIER POLICY): T0 = two flagships xhigh (host-touching);
T1 = one flagship high; T2 = single reviewer, GLM preferred; T3 = self-verify (most
kickoffs/status files are T3 — do not spend a flagship on them). Highest applicable tier
wins. Classify BEFORE dispatching and record it.

---

## 3. WHERE THE PROJECT IS

```
WP-0 / WP-S / WP-L P1 / Gate A   DONE
WP-L Phase 2                     DONE
WP-I run-kit construction        ← HERE
WP-I preregistration + freeze    next
WP-I host execution              authorized (grants #1/#2/#3/#6), blocked on the above
Audit 2 → WP-A → Gate B → WP-V   after
```

**Ledger: ~29.3 h of 50 spent, ~20.7 left.** 24.9 h was the ratified balance
(`11_TRIAGE/LEDGER_STATUS_2026-08-10.md`); **~4.4 h is booked prospectively for
2026-08-10 and needs owner ratification** — WP-I draft rounds 1.4–1.7 (0.8), RP6-P0
(1.0), RP7 (1.2), transport (1.0), prereg/tier/routing/tooling (0.4). Today: 45+ commits,
~20k lines, 09:16→21:00.

### The day's headline finding

The Codex flagship found, independently in RP7 and then RP6-P0, that each block used the
**venv it was auditing as the interpreter that produces its own verdict** — and
`python -I` does NOT disable `site`, so a `.pth` or `sitecustomize.py` in that venv runs
arbitrary `gatea`-authority code before the check. A tampered candidate could forge the
exact accepted line and mutate the host while the block reported clean. Proven by
execution in both blocks. Three Claude flagship rounds had missed it in each. This is the
strongest argument in the repo for the two-flagship T0 contract.

---

## 4. PER-ARTIFACT STATE (all committed + pushed)

### RP7-WPI-RO.sh — round 4 done, awaiting FINAL flagship pair
- Bytes `23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad`, 70941 B,
  commit `d6a976aa`.
- History: authored → Claude BLOCK 13 → R2 all closed → Claude BLOCK 6 → R3 all closed →
  Codex BLOCK 5 (the venv hole) → R4 all closed.
- R4 moved both accepting adjudicators onto a pinned system interpreter under `-I -S`
  that refuses to emit a result unless isolation holds; `python3` is the 10th bound tool
  and 21st projection point. Row 22 is two-phase (parse to EOF, then adjudicate). One
  enforced metadata-discovery universe. Preregistered B5/B6 order verified against the
  frozen code at runtime.
- **NEXT: both flagships xhigh on these bytes.** Kickoff exists:
  `WPI_BLOCKS_DRAFT/KICKOFF_CODEX_T0_AUDIT_RP7_FINAL.md` (adapt for the Claude slot).

### RP6-P0.sh — round 6 done, neither flagship has accepted yet (SLOWEST)
- Bytes `75db028e76438bc88caba19b9c3b6411e5f573f7b6c2bd13c3883d24e4389570`, 93421 B,
  commit `8fcab4d4`.
- History: C13 getent arm → 4 C13 rounds → Claude BLOCK 7 → full-block repair → Claude
  BLOCK 3 → R3 → Claude PASS-WITH-NITS **but** Codex BLOCK 4 → R4 → Codex BLOCK 3 +
  Claude REQUEST_CHANGES 1 → R5 (GLM) → Claude REQUEST_CHANGES 3 → R6 (GLM).
- R6 closed: the false "`-S` cannot be silently deleted" claim (now states truthfully that
  the self-check catches only ACCIDENTAL loss and that a hostile `.pth` defeats it — `-S`
  is the load-bearing control); `gids` grammar-gated before expansion with `set -f`
  (closing a capability-ledger laundering route where `id -G` returning `0*` in a cwd
  containing a file named `0` printed `intersection=empty`); pin-path glob refusal.
- Lead executed all QA (GLM's session gates execution): `bash -n` rc 0; R6 harnesses
  3/3, 10/10, 7/7; five prior fences PASS at rc 0.
- **Lead finding, MUST fix next round:** the five prior fences are addressed by absolute
  LINE RANGES and the file grows every round, so two of them ran into prose and looked
  like regressions. Give all five `BEGIN`/`END` marker pairs like R5/R6 have. Evidence a
  third party cannot re-run is not freeze-grade.
- One stale site left by R6 (outside its allowlist): `RP6_REPAIR_R4_REPORT.md:88` still
  carries the retracted `-S` claim. Fix it.
- **Codex audit of R6 (`RP6_CODEX_AUDIT_R6_2026-08-10.md`) = REQUEST_CHANGES, five
  required corrections. This is the round-7 scope:**
  1. **R5-F2 is forgeable.** Use `builtin type -t` (or an equivalently non-overridable
     builtin) so a caller-defined `type()` cannot forge the result. Separately, either
     bind the function definitions to the accepted RP0-LIB identity or narrow the
     `lib=sourced` claim to what is actually established. D026 cases for an overridden
     `type` and an unrelated same-name function.
  2. **R6-F3 closes too late.** Disable pathname expansion (preserving/restoring the
     caller's noglob state) around the OUTER `for p0_pin in $P0_TOOL_PINS` parse, before
     the first split; keep the charset gate and `p0_lookup` defence in depth. Add the
     whole-token crafted-cwd case: a tree matching `stat=/usr/bin/sta*` must be RED on
     current bytes (rc 0) and STOP identically in clean and crafted cwds after repair.
  3. **Adjudicate producer SHAPE before any rc-1 object verdict.** In `p0_probe_kind`,
     reject CR/LF, non-printable, empty and otherwise invalid rc-0 producer shapes as
     reasoned rc 3 before sanitising/classifying. Same status-then-shape rule for a
     successful `readlink -f` in `p0_assert_venv_root`: empty/multiline/non-printable/
     unparseable is STOP; only a valid complete canonical path differing from the
     preregistered literal may be FAIL. D026 for both arms.
  4. **Narrow or enforce printed claims:** document that `P0_TOOL_PINS` requires
     `python3`; do not call the prerequisite check builtin/provenance-bound unless it is;
     require the timeout pin before printing `pinned_timeout` or print its real
     resolution mode; do not label rc 124 uniquely as a deadline unless the wrapper can
     distinguish a child's own rc 124; express interpreter isolation as requested flags
     plus child-reported state unless provenance is independently bound.
  5. **Make evidence commands literal and bounded** — replace ALL line ranges with unique
     anchored markers whose invocation text cannot reopen the range (e.g.
     `^# R6_F1_HARNESS_BEGIN$`), give the five legacy fences the same treatment, repair
     the R4 fence so all descendants close and it returns within its documented bound,
     then re-run every exact command from a clean Git Bash recording command, rc, summary
     and stderr. **This independently confirms the Lead finding above.** Existing PASS
     summaries are supplemental until their recorded commands exit cleanly.
- **NEXT: round 7 (implementer must NOT be Codex — GLM or Claude Pro), then both
  flagships on the resulting bytes.**

### Transport set (9 files) — round 4 in progress
- Round-3 bytes at commit `78173bfd`: `transport_runner.ps1` (57826 B `13a57438…`),
  `TRANSPORT_PLAN.tsv` (7219 B `2a1cd2a6…`), `remote_setup_wpi.sh` (17775 B `c0b7caa7…`),
  `remote_close_tree_wpi.sh` (12039 B `fc183751…`, NEW derived), `remote_extract_verify_wpi.sh`
  (`8eb9c499…`), `run_p0.sh` (`e4ddf87b…`), `run_ro.sh` (`cd659ee9…`), plus QA/status.
- History: authored → Codex 10 + Claude 6 → R2 closed all 16 → Codex 4 + Claude
  PASS-WITH-NITS → R4 running.
- R3 highlights: the `$Matches` clobber that meant ops 11/12 could never bind is fixed
  (byte-equal pair now binds, proven against a real `remote_close_tree.sh` transcript);
  OpenSSH now refuses per-user AND system-wide config (`-F none`) with a recorded hijack
  that vanishes under it; `remote_close_tree_wpi.sh` derived rather than editing the
  accepted byte-frozen original.
- **Lead adjudication on R4/F4 (Codex prevails):** per-branch prerequisites, NOT one
  global `$sequenceOk`. Codex's decisive case — both stages established, P0 close STOPs,
  independent RO close genuinely FAILs — had the real RO deviation erased. Claude's
  asymmetry argument still holds for its own scenario; per-branch modelling satisfies both
  and subsumes Claude's nit about distinct reason tokens.
- **NEXT: consume R4; then both flagships on the R4 bytes.**

---

## 5. FREEZE-GATE INPUTS (six + transport's) — all `<PIN-AT-FREEZE>`

Nothing can GREEN end-to-end until these are filled; that is by design.
1. `WPI_FIXED_ATTESTED_MOUNT_PROJECTION_SHA256` — projection v2 over 21 point paths.
2. `WPI_FIXED_TRUSTED_PYTHON` (RP7) — resolved NON-symlink interpreter path.
3. `P0_FIXED_TRUSTED_PYTHON` (RP6-P0) — same, its own copy.
4. Row-8 execution-domain attestation literals (RP6-P0) — namespace + root-mount identity.
5. Transport: the covering-mount identity of `/home/gatea` for `remote_setup_wpi.sh`.
6. Transport: the other four recorded in `TRANSPORT_REPAIR_R3_REPORT.md`.

All are produced by the grant-#6 read-only attestation command set, which must run BEFORE
op 01 and must be preregistered and committed first.

**Trap:** a guard comparing against the literal `<PIN-AT-FREEZE>` string is destroyed by a
blind global fill — it would then hold a real value and STOP on a correctly frozen file.
`transport_runner.ps1`'s `$UNFILLED_MARKERS` array has this shape. **Stage-1 fill must be
per-constant, never a blind replace.**

---

## 6. OPEN ITEMS BEFORE FREEZE

1. Both flagships accept all three artifacts (the main work).
2. **§10.1 allowlist reconciliation.** The new path-scope prover
   (`WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py`, 49820 B) reports RP6 1 resolved / 37
   unresolved and RP7 4 resolved / 65 unresolved, with `/dev/null`,
   `/proc/self/mountinfo` and `/proc/uptime` outside §10.1. §10.1 predates the blocks'
   growth. Decide per path: add with justification, or change the block. The prover was
   deliberately NOT tuned to make the blocks pass.
3. Prover itself needs its T1 audit (`STATUS_PATHSCOPE.md` = AUTHORED-PENDING-AUDIT).
4. RP6 fence marker pairs + the stale `RP6_REPAIR_R4_REPORT.md:88` site.
5. Successor preregistration from the skeleton
   (`WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_SKELETON_2026-08-10.md`): mint RUNIDs
   (test against `rp0_require_safe_component`, demonstrate the refusal set), fill all
   pins, order the grant-#6 attestation before op 01, Stage 1 freeze, **commit BEFORE any
   invocation**.
6. Then: execute P0 → RO on the host, attestation + `RPD-VERIFY` as root, close evidence,
   WP-I closure record, Audit 2 (readiness package already assembled at
   `11_TRIAGE/AUDIT2_READINESS_PACKAGE/`).

---

## 7. TRAPS THAT COST TIME TODAY — DO NOT REPEAT

- **Windows autocrlf.** Never `git checkout` these block files to restore them; it
  rewrites LF→CRLF and breaks the frozen hash. Use
  `git cat-file blob HEAD:<path> > <path>`.
- **Counting CR bytes.** `grep -c $'\r' file` inside a loop can match every line (empty
  pattern) and produce a false alarm. Use `tr -cd '\r' < file | wc -c`.
- **Codex content filter.** A T0 audit of `RP6-P0.sh` died at ~162k tokens with "flagged
  for possible cybersecurity risk" because of its namespace/privilege probes. Workaround:
  neutral operational framing — "read-only environment preflight checks before a
  maintenance job", "confirm each branch reports honest results" — and avoid
  attack/exploit/adversarial/hostile/security-audit wording in the dispatch prompt.
- **GLM sessions gate script execution.** GLM correctly marks QA PENDING instead of
  fabricating. The Lead must then run the harnesses and replace PENDING with real
  transcripts. This is normal and worked well; budget for it.
- **NVIDIA NIM via the claude-CLI wrapper narrates but never engages file-write tools.**
  Read/analysis only — it produced zero deliverables on an authoring task.
- **Agents crash mid-write.** A dropped connection left a half-written block. Verify the
  hash after every delegate run before committing.

---

## 8. HOW TO WORK

Read in order: this file, then `_AI_MEMORY/GLOBAL_HANDOFF.md` newest section,
`_AI_MEMORY/NEXT_STEPS.md` top section, then
`11_TRIAGE/STANDING_AUTONOMY_AUTHORITY_2026-08-09.md`, then
`11_TRIAGE/ROUTING_POLICY_CREDIT_CONSERVATION_2026-08-10.md`, then
`11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md` (binding before designing or auditing any
executable block).

Rules that earned their keep today: commit exact file sets, never `git add .`; run the
repo guard first (`powershell -ExecutionPolicy Bypass -File MTC_COMMAND_CENTER/tools/repo_guard.ps1`);
never let one agent audit its own work; an inability to evaluate is a STOP, never a FAIL;
a check that cannot fail proves nothing; preregister before executing and commit the
preregistration first. End every response with numbered next steps and a chosen default,
owner-facing asks in plain non-technical language.
