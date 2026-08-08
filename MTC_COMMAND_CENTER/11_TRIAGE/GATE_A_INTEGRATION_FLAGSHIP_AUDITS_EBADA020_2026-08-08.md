# Integration flagship audits — `ebada020` (2026-08-08)

Continues `GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md` (GLM-5.2 rounds 1–2).
Companion records: `GATE_A_INTEGRATION_RECORD_EBADA020_2026-08-03.md`,
`GATE_A_ARTIFACT_IDENTITY_AND_SECRET_SCAN_EBADA020_2026-08-03.md`.

**Status: Codex flagship PASS, Lead-reproduced. Claude flagship dispatched — see §4.**

| D025 slot | Auditor | Verdict | Executed suite? |
|---|---|---|---|
| Flagship 1 (`claude-opus-5` xhigh) | round 4, dispatched 2026-08-08 | **see §4** | see §4 |
| Flagship 2 (`gpt-5.6-sol` xhigh) | round 3, 2026-08-08 | **PASS**, zero required findings, zero nits | yes, Windows |
| Auditor 4 (GLM-5.2) | rounds 1–2, 2026-08-03 | BLOCK (environmental), then `PASS-WINDOWS-ONLY-WITH-NITS` | round 2 only |

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

**Result: pending at the time of writing. `ebada020` is NOT YET ACCEPTED.**

## 5. Acceptance state

- Round 3 (`gpt-5.6-sol` xhigh): **PASS**, zero required findings, fully Lead-reproduced. One
  flagship slot filled.
- Round 4 (`claude-opus-5` xhigh): dispatched, verdict pending. Second flagship slot open.
- No auditor has produced a required finding against `ebada020` in any round.
- **Gate A must not start until §4 returns an accepting verdict.** If it returns a required finding,
  the Lead reproduces it before any product-code change is proposed.

## 6. Unchanged constraints

`codex/gate-a-integration` stays at `ebada020a59edf539f60acfbb3a6bf870c8679e9` — the artifact's build
SHA. Records go on `feature/donchian-crypto-ladder`. The artifact doc drift decision of 2026-08-03
(option a) is settled and not reopened. KVM2 remains out of scope.
