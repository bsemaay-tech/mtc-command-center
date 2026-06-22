# Second-Eyes Audit - AI Tooling + Repo Guard - 2026-06-22

Branch: `feature/audit-second-eyes`

Scope: read-mostly verification of repo guard, AI-tool cold-start behavior, Claude skill sanity, and doc consistency. No backtests, optimizations, servers, launchers, broker/live/paper actions, or repo artifact generation were run.

## Findings

### [repo_guard] · CLAIM
Clean feature branch returns `RESULT: PASS` and exit 0.

WHAT I RAN
```powershell
git show feature/mtc-repo-guard-skill:MTC_COMMAND_CENTER/tools/repo_guard.ps1 | Set-Content C:\tmp\second_eyes_repo_guard.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\tmp\second_eyes_repo_guard.ps1
```

RESULT: PASS

evidence
```text
[branch]    feature/audit-second-eyes
[dirty]     clean
[staged]    none
[protected] none
[untracked] no risky files
[unpushed]  no upstream set
WARN: no upstream tracking branch
RESULT: PASS
EXIT_CODE: 0
```

is-it-better-able? Treat "no upstream set" as expected for new branches or add a quieter pre-push mode; no safety issue.

### [repo_guard] · CLAIM
Running on `master`/`main` blocks.

WHAT I RAN
```powershell
git checkout master
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\tmp\second_eyes_repo_guard.ps1
git checkout feature/audit-second-eyes
```

RESULT: PASS

evidence
```text
[branch]    master
[dirty]     clean
[staged]    none
[protected] none
[untracked] no risky files
[unpushed]  in sync with upstream
BLOCK: on 'master' - branch first (feature/<scope>)
RESULT: BLOCKED
EXIT_CODE: 1
```

is-it-better-able? none.

### [repo_guard] · CLAIM
Risky untracked files are reported.

WHAT I RAN
```powershell
New-Item -ItemType File some_server.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\tmp\second_eyes_repo_guard.ps1
Remove-Item some_server.ps1
```

RESULT: PASS

evidence
```text
[dirty]     1 entr(y/ies):
            ?? some_server.ps1
[untracked] risky local-only file(s):
            some_server.ps1
WARN: risky untracked file(s) present - do NOT commit (some_server.ps1)
RESULT: PASS
EXIT_CODE: 0
```

is-it-better-able? If the protocol intends "risky untracked" to stop a commit, change this from WARN to BLOCK. Current behavior is documented as warning-like, not a false PASS.

### [repo_guard] · CLAIM
Protected-scope changes are blocked.

WHAT I RAN
```powershell
New-Item MTC_COMMAND_CENTER\07_ADAPTERS\__repo_guard_temp_untracked.txt
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\tmp\second_eyes_repo_guard.ps1
Remove-Item MTC_COMMAND_CENTER\07_ADAPTERS\__repo_guard_temp_untracked.txt
```

RESULT: PASS

evidence
```text
[dirty]     1 entr(y/ies):
            ?? MTC_COMMAND_CENTER/07_ADAPTERS/__repo_guard_temp_untracked.txt
[protected] CHANGES in protected scope:
            MTC_COMMAND_CENTER/07_ADAPTERS/__repo_guard_temp_untracked.txt
BLOCK: protected-scope change needs Baris approval (MTC_COMMAND_CENTER/07_ADAPTERS/__repo_guard_temp_untracked.txt)
RESULT: BLOCKED
EXIT_CODE: 1
```

is-it-better-able? none for actual protected paths.

### [repo_guard] · CLAIM
Protected-scope matching is correct.

WHAT I RAN
```powershell
New-Item -ItemType Directory MTC_COMMAND_CENTER\07_ADAPTERS_FAKE
New-Item MTC_COMMAND_CENTER\07_ADAPTERS_FAKE\__repo_guard_false_positive.txt
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\tmp\second_eyes_repo_guard.ps1
Remove-Item MTC_COMMAND_CENTER\07_ADAPTERS_FAKE\__repo_guard_false_positive.txt
Remove-Item MTC_COMMAND_CENTER\07_ADAPTERS_FAKE
```

RESULT: FAIL

evidence
```text
[dirty]     1 entr(y/ies):
            ?? MTC_COMMAND_CENTER/07_ADAPTERS_FAKE/
[protected] CHANGES in protected scope:
            MTC_COMMAND_CENTER/07_ADAPTERS_FAKE/
BLOCK: protected-scope change needs Baris approval (MTC_COMMAND_CENTER/07_ADAPTERS_FAKE/)
RESULT: BLOCKED
EXIT_CODE: 1
```

is-it-better-able? Replace `if ($f -like "$p*")` with a boundary-aware match such as `if ($f -eq $p -or $f -like "$p/*")`. This is a false BLOCK, not a false PASS.

### [repo_guard] · CLAIM
PowerShell 5.1-safe.

WHAT I RAN
```powershell
powershell.exe -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'
rg -n '\?\?|\?:|\.\?' C:\tmp\second_eyes_repo_guard.ps1
```

RESULT: PASS

evidence
```text
5.1.26100.8655
EXIT_CODE: 0

rg ... 
EXIT_CODE: 1
```

The script also executed every verdict path above under `powershell.exe` 5.1. No ternary/null-coalescing/null-conditional syntax was found.

is-it-better-able? none.

### [repo_guard] · CLAIM
Guard is cold-start available from read-first docs.

WHAT I RAN
```powershell
Test-Path MTC_COMMAND_CENTER\00_AGENT_PROTOCOLS\MTC_REPO_GUARD_PROTOCOL.md
Test-Path MTC_COMMAND_CENTER\00_AGENT_PROTOCOLS\MTC_REPO_GUARD_USAGE.md
git cat-file -e feature/mtc-repo-guard-skill:MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md
git ls-tree -r --name-only master | rg "MTC_REPO_GUARD|repo_guard\.ps1|\.claude/skills/mtc-repo-guard"
```

RESULT: FAIL

evidence
```text
False
False
protocol_on_feature_exit=0
usage_on_feature_exit=0
master_search_exit=1
```

The protocol and script exist on `feature/mtc-repo-guard-skill`, but not on this audit branch or `master`.

is-it-better-able? Merge or cherry-pick the guard protocol and script before claiming cold-start availability.

### [MarkItDown] · CLAIM
Wrapper is discoverable, dry-run by default, converts XLSX, and keeps the venv git-ignored.

WHAT I RAN
```powershell
python MTC_COMMAND_CENTER\03_QUANTLENS\tools\markitdown_ingest.py --help
python MTC_COMMAND_CENTER\03_QUANTLENS\tools\markitdown_ingest.py MTC_COMMAND_CENTER\01_MTC_PROJECT\05_PARITY\CASE_SETUP_GUIDE_L4_120_baseline.xlsx --out C:\tmp\second_eyes_markitdown_dryrun
python MTC_COMMAND_CENTER\03_QUANTLENS\tools\markitdown_ingest.py MTC_COMMAND_CENTER\01_MTC_PROJECT\05_PARITY\CASE_SETUP_GUIDE_L4_120_baseline.xlsx --apply --out C:\tmp\second_eyes_markitdown_apply
git check-ignore -v MTC_COMMAND_CENTER\03_QUANTLENS\tools\.venvs\markitdown\pyvenv.cfg
```

RESULT: PASS

evidence
```text
usage: markitdown_ingest.py [-h] [--apply] [--out OUT] [--bootstrap] [paths ...]
Default is a DRY RUN ... Pass ``--apply`` to write.

DRY RUN - would convert:
  ...CASE_SETUP_GUIDE_L4_120_baseline.xlsx  ->  C:\tmp\second_eyes_markitdown_dryrun\CASE_SETUP_GUIDE_L4_120_baseline.md
1 file(s). Re-run with --apply to write.

OK     CASE_SETUP_GUIDE_L4_120_baseline.xlsx  ->  C:\tmp\second_eyes_markitdown_apply\CASE_SETUP_GUIDE_L4_120_baseline.md
1/1 converted.
Length: 69087

.gitignore:148:MTC_COMMAND_CENTER/03_QUANTLENS/tools/.venvs/
VENV_EXISTS
```

I did not delete the existing venv to force a first-run bootstrap. Code-read evidence confirms bootstrap logic:
```text
VENV_DIR = TOOLS_DIR / ".venvs" / "markitdown"
def ensure_venv(force: bool = False)
[bootstrap] creating venv ...
[bootstrap] installing markitdown...
py = ensure_venv()
```

is-it-better-able? If strict cold-start proof is required, test in a clone or temp copy with the venv absent. Do not delete the working repo venv just to prove it.

### [Design-Extract] · CLAIM
`designlang` works on Windows with `--system-chrome`; the documented cosmetic exit-1 reproduces and outputs still land.

WHAT I RAN
```powershell
npx -y designlang --help
npx -y designlang -o C:\tmp\second_eyes_design_extract_out -n second-eyes-linear --dark https://linear.app --system-chrome
```

RESULT: WARN

evidence
```text
Usage: designlang [options] [command] <url>
--system-chrome  use the system Chrome install instead of the bundled Chromium

Output files:
  ✓ second-eyes-linear-design-language.md
  ✓ second-eyes-linear-design-tokens.json
  ...
  ✓ second-eyes-linear-form-states.json
EXIT_CODE: 1
FILE_COUNT: 42

- Launching browser...
√ Extraction complete!
× Extraction failed
The "string" argument must be of type string or an instance of Buffer or ArrayBuffer. Received undefined
```

is-it-better-able? Wrap this command when used in automation: accept exit 1 only if expected output files exist, or wait for a designlang version that exits 0 after successful extraction.

### [Graphify] · CLAIM
Wrapper executes on Windows, builds in temp, answers impact queries, and leaves repo clean.

WHAT I RAN
```powershell
python MTC_COMMAND_CENTER\03_QUANTLENS\tools\graphify_impact.py --help
python MTC_COMMAND_CENTER\03_QUANTLENS\tools\graphify_impact.py build MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly
python MTC_COMMAND_CENTER\03_QUANTLENS\tools\graphify_impact.py affected read_model.py
python MTC_COMMAND_CENTER\03_QUANTLENS\tools\graphify_impact.py explain pipeline_reader
python MTC_COMMAND_CENTER\03_QUANTLENS\tools\graphify_impact.py query "what builds the dashboard snapshot"
git status --short
```

RESULT: PASS

evidence
```text
Safe Graphify wrapper for on-demand code impact analysis.
This wrapper always works on a copy of the scoped source under a temp dir.

[graphify] scoped 28 file(s) -> C:\Users\...\AppData\Local\Temp\mtc_graphify_work\src
[graphify watch] Rebuilt (no clustering): 446 nodes, 1597 edges

Affected nodes for read_model.py
- cli.py
- health.py
- server.py
- __main__.py

Node: pipeline_reader.py
Degree: 50
<-- audit_reader.py
<-- read_model.py

Traversal ... Start: ['build_dashboard_snapshot()', 'build_dashboard_snapshot_cached()', ...]
```

`git status --short` printed no paths after the run.

is-it-better-able? none.

### [CodeBurn] · CLAIM
CodeBurn executes on Windows and supports the pilot commands.

WHAT I RAN
```powershell
codeburn status
codeburn models
```

RESULT: PASS

evidence
```text
Today  $9.72  63 calls    Month  $882.04  8196 calls

Provider       Model              Total    Cost
Claude         Opus 4.8           670.8M   $621.60
Codex          GPT-5.5            445.9M   $404.04
OpenCode       DeepSeek v4 Pro     85.0M   $2.47
Total                            1601.5M  $1296.31
```

is-it-better-able? none.

### [skill sanity] · CLAIM
`.claude/skills/mtc-repo-guard/SKILL.md` exists, has valid frontmatter, and references the protocol.

WHAT I RAN
```powershell
@'
from pathlib import Path
import yaml
p=Path('.claude/skills/mtc-repo-guard/SKILL.md')
text=p.read_text(encoding='utf-8')
fm=text.split('---',2)[1]
data=yaml.safe_load(fm)
print('YAML_PARSE: PASS')
print('name:', data.get('name'))
print('description_present:', bool(data.get('description')))
print('references_protocol:', 'MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md' in text)
print('references_usage:', 'MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_USAGE.md' in text)
'@ | python -
git check-ignore -v .claude\skills\mtc-repo-guard\SKILL.md
git status --short --ignored .claude\skills\mtc-repo-guard\SKILL.md
```

RESULT: WARN

evidence
```text
YAML_PARSE: PASS
name: mtc-repo-guard
description_present: True
references_protocol: True
references_usage: True

.gitignore:19:.claude/ ".claude\\skills\\mtc-repo-guard\\SKILL.md"
!! .claude/
```

The local skill is syntactically fine, but `.claude/` is ignored and the referenced protocol files are not present on this branch/master.

is-it-better-able? Decide whether this is intentionally local-only. If it should reach clones, move the rule to tracked docs or force-add a minimal tracked skill intentionally.

### [doc consistency] · CLAIM
AI-tool docs agree on current status.

WHAT I RAN
```powershell
rg -n "PREP ONLY|nothing installed|Phase 3|Phase 4|MarkItDown|CodeBurn|Graphify|Design-Extract|venv lives in|C:\\tmp|promoted|DONE|Pilot|PASS|KEEP|DEFER|IN PROGRESS|COMPLETE" MTC_COMMAND_CENTER\09_DOCS\AI_TOOLING\AI_TOOL_INTEGRATION_PLAN.md MTC_COMMAND_CENTER\09_DOCS\AI_TOOLING\pilots\*.md MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md
```

RESULT: FAIL

evidence
```text
AI_TOOL_INTEGRATION_PLAN.md:3:Status: PREP ONLY - nothing installed.
AI_TOOL_INTEGRATION_PLAN.md:95:Phase 1 ... DONE 2026-06-21
AI_TOOL_INTEGRATION_PLAN.md:116:Phase 3 ... COMPLETE 2026-06-21
AI_TOOL_INTEGRATION_PLAN.md:148:MarkItDown ... DONE ... promoted
AI_TOOL_INTEGRATION_PLAN.md:150:CodeBurn ... DONE
AI_TOOL_INTEGRATION_PLAN.md:151:Graphify ... DONE
AI_TOOL_INTEGRATION_PLAN.md:158:Design-Extract ... DONE 2026-06-22

NEXT_STEPS.md:13:AI TOOL INTEGRATION ROADMAP ... PREP ONLY, nothing installed
NEXT_STEPS.md:21:Phase 3 now COMPLETE
NEXT_STEPS.md:23:MarkItDown promoted to permanent
NEXT_STEPS.md:26:Design-Extract ... DONE 2026-06-22

markitdown_pilot.md:5:PROMOTED 2026-06-21 ... No longer a C:\tmp pilot.
markitdown_pilot.md:40:Venv lives in C:\tmp (ephemeral). If promoted...
```

Contradictions:
- `AI_TOOL_INTEGRATION_PLAN.md` header still says `PREP ONLY - nothing installed`, but the same file marks Phase 1 done, Phase 3 complete, and multiple tools done.
- `NEXT_STEPS.md` roadmap header still says `PREP ONLY, nothing installed`, but its Phase 3/4 bullets mark tools done/promoted.
- `markitdown_pilot.md` promoted block says no longer `C:\tmp`, while the older caveat still says the venv lives in `C:\tmp` and should be relocated if promoted.

is-it-better-able? Update the stale headers/caveat. Keep historical pilot details, but label old pilot state as "historical pilot environment".

### [AGENTS auto-use] · CLAIM
`AGENTS.md` has the AI TOOL AUTO-USE block and points to the right wrappers/harness.

WHAT I RAN
```powershell
rg -n "AI TOOL AUTO-USE|markitdown_ingest.py|graphify_impact.py|codeburn status|_deepseek_driver|TOKEN DISCIPLINE" AGENTS.md MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md MTC_COMMAND_CENTER\09_DOCS\AI_TOOLING\AI_TOOL_INTEGRATION_PLAN.md
```

RESULT: PASS

evidence
```text
AGENTS.md:7:TOKEN DISCIPLINE - dispatch mechanical work to cheap models
AGENTS.md:9:Harness: _deepseek_driver\ds_agent.py
AGENTS.md:44:AI TOOL AUTO-USE
AGENTS.md:48:python MTC_COMMAND_CENTER\03_QUANTLENS\tools\markitdown_ingest.py
AGENTS.md:50:python MTC_COMMAND_CENTER\03_QUANTLENS\tools\graphify_impact.py
AGENTS.md:51:codeburn status ... codeburn models
START_HERE.md:9:AI tool auto-use ... see the AI TOOL AUTO-USE section in AGENTS.md
```

is-it-better-able? none.

## Overall Verdict

Do the tools work hands-free as claimed? **No, not as a complete package yet.**

Most individual tools execute: MarkItDown converts XLSX, Graphify works through the temp-copy wrapper, CodeBurn reports spend, and Design-Extract writes usable outputs. But the package is not fully hands-free because:

1. `repo_guard.ps1` and its protocol docs are only on `feature/mtc-repo-guard-skill`, not on this branch or `master`.
2. Design-Extract still exits 1 after writing outputs, so naive automation sees failure.
3. The `.claude` repo-guard skill is ignored and local-only, and it references protocol files missing from current tracked branches.

No false PASS was found in the core guard paths. The one guard bug found is a false BLOCK on sibling path prefixes (`07_ADAPTERS_FAKE`).

## Top 3 Fixes

1. **Merge/publish repo guard files:** bring `MTC_COMMAND_CENTER/tools/repo_guard.ps1` and both `MTC_REPO_GUARD_*` docs onto the shared branch before advertising cold-start guard behavior.
2. **Fix protected matching:** change `$f -like "$p*"` to a path-boundary-aware condition (`$f -eq $p -or $f -like "$p/*"`), and add tests for real protected paths plus sibling-prefix false positives.
3. **Clean doc status drift:** update `AI_TOOL_INTEGRATION_PLAN.md`, `NEXT_STEPS.md`, and the MarkItDown pilot caveat so headers and lower sections agree with promoted/completed status.

## Needs Other Agent / Baris Decision

- Decide whether `.claude/skills/mtc-repo-guard` should remain local-only or be made portable in a tracked path.
- Decide whether Design-Extract's exit 1 is acceptable with an output-existence wrapper, or whether to wait for/upstream a fix.
- Decide whether risky untracked files should remain WARN or become BLOCK before commit.
