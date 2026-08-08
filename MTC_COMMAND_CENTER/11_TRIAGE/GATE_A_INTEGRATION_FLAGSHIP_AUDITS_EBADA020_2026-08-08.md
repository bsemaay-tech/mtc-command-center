# Integration flagship audits — `ebada020` (2026-08-08)

Continues `GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md` (GLM-5.2 rounds 1–2).
Companion records: `GATE_A_INTEGRATION_RECORD_EBADA020_2026-08-03.md`,
`GATE_A_ARTIFACT_IDENTITY_AND_SECRET_SCAN_EBADA020_2026-08-03.md`.

**Status: `ebada020` is ACCEPTED as the Gate A integrated candidate (2026-08-08). D025 rule 3 is
satisfied — both flagships returned accepting verdicts with zero required findings from any auditor.**

| D025 slot | Auditor | Verdict | Executed suite? |
|---|---|---|---|
| Flagship 1 (`claude-opus-5` xhigh) | round 4, 2026-08-08 | **PASS-WITH-NITS** — accepting per `AGENTS.md:80`; zero required findings, 3 optional nits | yes — Windows **and** locked Linux, both self-exported |
| Flagship 2 (`gpt-5.6-sol` xhigh) | round 3, 2026-08-08 | **PASS**, zero required findings, zero nits | yes, Windows |
| Auditor 4 (GLM-5.2) | rounds 1–2, 2026-08-03 | BLOCK (environmental), then `PASS-WINDOWS-ONLY-WITH-NITS` | round 2 only |

Three optional nits are recorded in §4.3 as follow-ups. **NIT 1 is operationally significant and the
Lead reproduced it: the credential-free DISARMED start mode is not reachable from any shipped deploy
artifact.** It is not a Gate A blocker and not a merge regression, but it must be closed before a
DISARMED VPS deploy or the 50-hour plan's own goal is not delivered.

---

## 1. Round 3 dispatch — Codex `gpt-5.6-sol` xhigh

| Item | Value |
|---|---|
| Model / effort | `gpt-5.6-sol`, `model_reasoning_effort=xhigh` — header of the run confirms both |
| Route | `Invoke-CodexForClaude.ps1 -Account free` → `CODEX_HOME=C:\Users\BarışSemaay\.codex_OLD` (`bs***y2@gmail.com`) |
| Worktree | `C:\GAAUD_INT_GLM`, detached at `ebada020a59edf539f60acfbb3a6bf870c8679e9` |
| Prompt | committed `CODEX_GATE_A_INTEGRATION_AUDIT_PROMPT_EBADA020_2026-08-03.md`, PROMPT section verbatim, extracted to `C:\tmp\codex_sol_audit_prompt_ebada020.md` (7517 B) |
| Report | `C:\tmp\CODEX_SOL_AUDIT_INTEGRATION_EBADA020_2026-08-08.txt` (258 270 B, 4948 lines) |
| Sandbox | `--dangerously-bypass-approvals-and-sandbox`, owner-authorised for isolated audit execution |
| Tokens | 175.363k |

### 1.1 The execution trap was defeated, not tolerated

Rounds 1–2 and every prior Gate A Codex auditor BLOCKed because the CLI ran `sandbox: read-only` and
refused commands as `blocked by policy` outside a trusted project directory. Two probes proved the fix
**before** the round was spent:

1. `exec --sandbox read-only -m gpt-5.6-sol -c model_reasoning_effort=xhigh` → returned `PROBE_OK`,
   exit 0, header `reasoning effort: xhigh`. Proves the mandated model **and** effort are live on this
   route. (`models_cache.json` in that home still lists no `GPT-5.6-Sol` — it was captured while the
   account was Free. Stale cache; the live probe governs.)
2. In `C:\GAAUD_INT_GLM` with the bypass flag → header `sandbox: danger-full-access`, and
   `git rev-parse HEAD` executed, returning `ebada020a59edf539f60acfbb3a6bf870c8679e9`.

**Routing doc correction owed:** `AI_ACCOUNT_AND_MODEL_ROUTING.md:21` still labels the
`free` / `.codex_OLD` route as plan **Free**. The owner upgraded that account (`bsemaay2@gmail.com`)
to ChatGPT Plus on 2026-08-08, and `gpt-5.6-sol` at `xhigh` is proven live on it. The `secondary`
route was not used — it is the account whose credit window the overnight run exhausted.

**Launcher defect worth recording:** `Invoke-CodexForClaude.ps1` cannot take bare Codex flags —
`-Account free exec --sandbox read-only -m …` dies with
`A positional parameter cannot be found that accepts argument 'exec'`, because PowerShell tries to
bind `-m` / `-c` as script parameters before `ValueFromRemainingArguments` sees them. Working form:
build an array and pass it explicitly as `-CodexArgs $a`.

## 2. Round 3 verdict: **PASS** — zero required findings, zero optional nits

Reported as executed by the auditor itself: identity/status, scope, ancestry, product-ancestor
checks, the full Windows suite, conflict lineage, product-tree comparison, `git remerge` inspection,
test-name set comparison, a live DISARMED + WAL capture exercise, ledger byte checks, complete
artifact-manifest verification, shell CR checks, and the EOL archive interaction. Relied on the Lead
record for the locked-Linux candidate/parent suites only — it reached `GATEA-STAGING` and confirmed
Python 3.12.3 / pytest 9.1.1, but the prior candidate workspace was absent and it uploaded nothing.

Suite execution is real, not paraphrased. Log line 663 carries the invocation
(`$env:PYTEST_ADDOPTS='-p no:cacheprovider'; python -m pytest -q` in
`C:\GAAUD_INT_GLM\IBKR_PAPER_BRIDGE`) and line 700 the result:

```
1359 passed, 1 warning in 222.05s (0:03:42)
```

Matching the Lead's recorded Windows floor exactly on count.

## 3. Lead independent reproduction — every load-bearing claim re-measured

Run by the Lead in `C:\GAAUD_INT_GLM` after the audit, not read from the auditor's report.

| Claim | Auditor | Lead re-measured | Match |
|---|---|---|---|
| `HEAD` | `ebada020a59…` | `ebada020a59edf539f60acfbb3a6bf870c8679e9` | ✅ |
| `git status --porcelain` after audit | clean | empty | ✅ |
| `codex/gate-a-integration` head | unchanged | `ebada020a59edf539f60acfbb3a6bf870c8679e9` | ✅ |
| Scope `637307e8..HEAD` | 9 files | 9 files, identical name-status list | ✅ |
| Ancestry | 4 merges, first-parent from `637307e8` | `ebada020←f6478e53←499ae639←20f44b8f←637307e8` | ✅ |
| Product SHAs ancestors | all 4 | `merge-base --is-ancestor` exit 0 for `82e92c98`, `7aad0377`, `17402a58`, `ebb750da` | ✅ |
| Conflict site | derived form at `:890` | `assert inv["schema_version"] == str(SCHEMA_VERSION_BASELINE)` | ✅ |
| `SCHEMA_VERSION_BASELINE` | `4` | `SCHEMA_VERSION_BASELINE = 4` in `bridge/store/db.py` | ✅ |
| Test-name sets in `test_wal_state_bundle.py` | 58 / 41 / 58 | `f6478e53`=58, `ebb750da`=41, `HEAD`=58, all unique | ✅ |
| `HEAD` set == `f6478e53` set | True | `Compare-Object` → no differences | ✅ |
| `ebb750da` names missing from `HEAD` | 0 | 0 | ✅ |
| Artifact `RELEASE_SHA` | `ebada020a59…` | `ebada020a59edf539f60acfbb3a6bf870c8679e9` | ✅ |
| `RELEASE_SHA256SUMS` SHA-256 | `8FC30864…4700C9` | `8FC30864BA342E53DCFC6B2938124F91D005F02671A332580A723F38FD4700C9` | ✅ |
| Manifest entries | 7059 | 7059 lines | ✅ |
| Artifact `deploy/linux/*.sh` CR bytes | 0 on all five | `install.sh`, `package.sh`, `rollback.sh`, `verify.sh`, `common.sh` — all `cr=0` | ✅ |
| Ledger blob SHA-256 | `f4cdece5…` | `F4CDECE5098D4E915431F9FD916005BBC3D79EA5AF89A0535E3E21D668BDA90E`, 867 B, 0 CR | ✅ |
| Ledger worktree SHA-256 | `f4cdece5…` | identical hash, 867 B, 0 CR | ✅ |

Ledger blob bytes were extracted through `cmd /c "git … cat-file blob … > file"` so no PowerShell
text decoding could alter them. **The A-2 CRLF defect is absent, independently confirmed.**

### 3.1 Audit-conduct safety check on the log

| Check | Result |
|---|---|
| Private-key material printed | `PRIVATE KEY` occurrences: **0** |
| Mutating git commands | `git add/commit/push/checkout/reset/stash`: **0** |
| SSH targets | only `gatea@172.24.55.233` with `-i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519`; key passed, never read |
| KVM2 touched | 29 textual hits, **all** repo paths/strings (`KVM2_PROGRAM/…`, test docstrings); zero connections |
| Worktree mutated | `git status --porcelain` empty before and after |

## 4. Round 4 — `claude-opus-5` xhigh flagship (dispatched 2026-08-08)

**Why this round exists.** `AGENTS.md:66` (D025 rule 3) reads: *acceptance requires accepting
verdicts from both flagship auditors (`claude-opus-5` xhigh and `gpt-5.6-sol` xhigh) plus no
unresolved reproduced required finding from any auditor.* GLM-5.2 is **canonical auditor 4**, which
that same rule says *"add detection, not a veto"* — it holds no flagship slot. The 2026-08-03 records
and handoff described GLM-5.2 as the first flagship and `gpt-5.6-sol` as "the second", which does not
match the rule as written. Barış's **no-Claude owner waiver** is recorded for the four *source* lines
while Claude was quota-blocked; no waiver is recorded for the *integration* SHA, and
`NEXT_SESSION_HANDOFF_2026-08-03B.md:184` explicitly calls a Claude audit of the integrated SHA
"a separate owner decision".

Rather than accept `ebada020` on the weaker reading or stall for a waiver, the Lead filled the slot.
Claude quota is available again, so the gap is closable by evidence instead of by governance
argument.

| Item | Value |
|---|---|
| Model / effort | `claude-opus-5`, `--effort xhigh`, `--no-session-persistence` (fresh independent session) |
| Worktree | `C:\GAAUD_INT_GLM`, same frozen SHA, clean at dispatch |
| Prompt | `C:\tmp\claude_flagship_audit_prompt_ebada020.md` (7979 B) — the committed canonical prompt with only the auditor-identity paragraphs rewritten; all mandatory checks, D025 rules and the anti-anchoring instruction preserved verbatim |
| Report | `C:\tmp\CLAUDE_FLAGSHIP_AUDIT_INTEGRATION_EBADA020_2026-08-08.txt` |

The prompt states that two auditors already reported no defect **and** instructs it not to look less
hard for that reason — the same anti-anchoring construction the committed Codex prompt used. No
desired verdict was supplied.

### 4.1 Verdict: **PASS-WITH-NITS** — accepting, zero required findings

Report: `C:\tmp\CLAUDE_FLAGSHIP_AUDIT_INTEGRATION_EBADA020_2026-08-08.txt` (14 132 B, 123 lines).
Worktree `git status --porcelain` empty after the round; `HEAD` unchanged.

This round went materially deeper than round 3 and relied on the record for **nothing**:

- **Locked Linux executed by itself.** It built its own LF exports
  (`git -c core.autocrlf=false -c core.eol=lf -c tar.umask=0022 archive`) for both SHAs, verified the
  tars byte-identical across transfer by SHA-256, and ran them under the host-locked venv in its own
  directory `~/opus5-audit-20260808`. Candidate `2 failed, 1357 passed`; parent `25 failed,
  1281 passed`; new failure node IDs **empty**; 23 fixed. The Lead's Linux floor is now independently
  reproduced rather than merely reviewed, which makes this a full-platform verdict.
  It also reported its own error honestly: a first attempt showed 3 failures caused by its own export
  omitting `11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`, which
  `test_linux_deployment.py:857` reads. Corrected by re-export.
- **Diff-of-diffs per merge.** For each merge M with parents (p1,p2) it compared `git diff p1 M`
  against `git diff $(git merge-base p1 p2) p2`. All four identical `--stat`; three byte-identical;
  the fourth differed only in hunk offsets and the one conflict line. **No merge smuggled a change.**
- **Mutation-tested the conflict site** instead of reading it (M1/M2 — see §4.3 NIT 2). The merged
  assertion is proven live, not vacuous.
- **Built the untested interaction.** Real app with `MTC_BRIDGE_START_MODE=credential_free_disarmed`,
  `start_runtime=True`, `_build_broker` patched to raise, store left open with a live hot WAL
  (453 232 B WAL, 32 768 B `-shm`): capture returned `CAPTURED`, `app_state DISARMED`,
  `schema_version 4`, `engine None`. Capture succeeding without `--allow-live-source` is correct —
  `wal_state_bundle.py:841` gates on `changed_during_capture and not allow_live_source`, so the flag
  permits mid-capture drift, not liveness.
- **Ran `package.sh` end-to-end on Linux** against a real git repo carrying the new `.gitattributes`,
  real deploy scripts, the real ledger and binary PNGs: exit 0, `MANIFEST SELF-VERIFY OK`, ledger hash
  `f4cdece5…`. Decisive EOL check: `git grep -I -l $'\r' HEAD` → **0 tracked blobs contain a CR
  byte**, so the rule and the `core.eol=lf` pin cannot double-apply or diverge.
- **Artifact verified exhaustively, not sampled:** `sha256sum -c` exit 0, 7059 OK lines, 0 non-OK.
  Explained the 5381 unique hashes as genuine duplicate files rather than a stub.
- **Test-name sets as a union proof:** `637307e8`=41, `7aad0377`=58, `ebb750da`=41, `HEAD`=58; nothing
  missing from either parent, nothing in HEAD from neither parent, 0 duplicates. `HEAD` is the exact
  union, and `git diff 7aad0377 HEAD -- tests/test_wal_state_bundle.py` is precisely the residual
  branch's import plus line 890 and nothing else.

**Conclusion it reached: no defect introduced by the merge.**

### 4.2 Independence limitation — recorded honestly

The four *source* commits were implemented by Codex, so a Claude audit of them is cross-model. The
*integration merge itself* was performed by a Claude Opus 5 Lead session, so round 4 is a same-model
(different, fresh, non-persisted session) audit of Claude-authored merge resolutions. `AGENTS.md`
requires a fresh independent session and this satisfies that, but the cross-model axis on the merge
comes from round 3 (`gpt-5.6-sol`), not round 4. Both rounds independently executed the suite and
neither found a defect, so the pair as a whole carries a cross-model executing verdict.

### 4.3 The three nits — dispositions

**NIT 1 — credential-free DISARMED mode is unreachable from any shipped deploy artifact.
LEAD-REPRODUCED, CONFIRMED. Binding follow-up before any DISARMED VPS deploy.**

Lead reproduction, run at `ebada020`:

```
git grep -n -I -E "MTC_BRIDGE_START_MODE|start-mode|start_mode" HEAD
  -> hits ONLY in bridge/app.py and tests/test_credential_free_disarmed.py. Zero hits under deploy/.
deploy/linux/systemd/mtc-bridge-first-start.service.template:34
deploy/linux/systemd/mtc-bridge-steady.service.template:37
  -> both: ExecStart=/opt/mtc-bridge/venvs/@RELEASE_SHA@/bin/python -m bridge.app   (no --start-mode)
deploy/linux/env/mtc-bridge.env.template
  -> names HL_ACCOUNT_ADDRESS, HL_API_WALLET_KEY, TELEGRAM_*, ANTHROPIC_API_KEY, XAI_API_KEY,
     forbids HL_LIVE_ACK. Does NOT name MTC_BRIDGE_START_MODE.
tests/test_credential_free_disarmed.py:26
  -> resolve_start_mode(env={}) == credentialed   i.e. the default is credentialed
```

So a VPS installed from this artifact starts in **credentialed** mode and calls
`resolve_hyperliquid_credentials()`. This is **not** a merge regression — `17402a58`'s accepted scope
legitimately excluded `deploy/` — and it is **not** a Gate A blocker, because Gate A tests deployment
mechanics rather than start-mode selection. But the 50-hour plan's stated goal is a **DISARMED** VPS,
and this candidate does not deliver a credential-free start on its own. A reader of the earlier
records could reasonably have assumed it did.

**Open question the follow-up must answer, not assume:** the env template is contract-only and
`install.sh` creates it with every variable UNSET, so the first real start would be credentialed mode
with no credentials present. Whether that fails closed (safe, cannot arm) or crash-loops is
undetermined and must be established by execution before WP-V — do not reason about it on paper.

**NIT 2 — record wording overstated.** Applied. `GATE_A_INTEGRATION_RECORD_EBADA020_2026-08-03.md`
§ conflict site now carries a dated correction; the "strictly more robust / strictly weaker" claim is
withdrawn and replaced with the mutation evidence. Resolution itself unchanged and still correct.

**NIT 3 — the locked-Linux floor is amber, and Linux is the production floor.** The two survivors
(`test_order_state.py::test_gc_referents_of_{transitions,raw_aliases}_contain_no_mutable_container`)
are CPython-version-dependent: they fail on the host's 3.12 and pass on Windows 3.14, and they fail
identically on parent `637307e8`. Pre-existing on master and out of Gate A scope — but the KVM2 VPS
venv **is** Python 3.12, so they will be present on the deployed host. Scoped follow-up owed rather
than carrying an amber floor indefinitely.

### 4.4 Housekeeping owed on the staging host

The auditor left its evidence in place deliberately: `gatea@172.24.55.233:~/opus5-audit-20260808/`
(logs `cand.log`, `parent.log`) plus `~/v2_*.tar` and `~/sub_*.tar`. It confirms the locked venv,
KVM2 and the Lead's trees were untouched and no key material was read, printed or copied. **Remove
those paths as Gate A A-0 prep** so the transfer step starts from a clean home directory.

## 5. Acceptance state — `ebada020` ACCEPTED 2026-08-08

D025 rule 3 (`AGENTS.md:66`) requires accepting verdicts from both flagships plus no unresolved
reproduced required finding from any auditor. All three conditions hold:

| Condition | State |
|---|---|
| `claude-opus-5` xhigh accepting | ✅ PASS-WITH-NITS — accepting per `AGENTS.md:80` |
| `gpt-5.6-sol` xhigh accepting | ✅ PASS |
| Unresolved reproduced required finding, any auditor | ✅ none — all three rounds returned zero required findings |

**`ebada020a59edf539f60acfbb3a6bf870c8679e9` is ACCEPTED as the Gate A integrated candidate.**
Gate A may now start from **A-0** per `GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md` as
amended by `GATE_A_PREREGISTRATION_ADDENDUM_A_2026-08-02.md`, transferring the frozen artifact as a
single tar, stopping at the first FAIL.

Carried forward as follow-ups, none of them Gate A blockers: NIT 1 (binding before a DISARMED VPS
deploy), NIT 3 (Python 3.12 gc-referents on the production floor), and the two stale routing-doc lines
in §1.1.

## 6. Unchanged constraints

`codex/gate-a-integration` stays at `ebada020a59edf539f60acfbb3a6bf870c8679e9` — the artifact's build
SHA. Records go on `feature/donchian-crypto-ladder`. The artifact doc drift decision of 2026-08-03
(option a) is settled and not reopened. KVM2 remains out of scope.
