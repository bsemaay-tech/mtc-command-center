# Pathscope cap-override repair continuation - clean subject

You are the counterpart flagship IMPLEMENTER in a fresh session. Model must be
`claude-opus-5`; effort `high`. This continues the single owner-authorized T1
repair cycle before any audit. No sub-delegation and no git mutation.

Work from current committed bytes in `C:\LAB\Tradingview_LAB_CLEAN`; do not
apply or inspect any Git stash. Read root `AGENTS.md`, `_AI_MEMORY/START_HERE.md`,
the owner decision section 4, the full r3 Codex verdict, and
`PATHSCOPE_CAP_OVERRIDE_LEAD_FINDING_2026-08-13.md`.

Repair C-2 completely from the clean round-3 subject. Assignment values must
never silently lose later absolute members or ordinary relative pathnames.
Handle prefix, `env`, and `export` sites. Do not use a variable-name allowlist.

The Lead additionally reproduced this false PASS in the first incomplete
attempt:

```bash
X="$ROOT dir/escape" cat "$ROOT/f"
```

with `ROOT=/safe`, `PWD=/safe`, allowlist `/safe/**`. The actual quoted pathname
`/safe dir/escape` is outside the allowlist; blindly applying `str.split()` to
the rendered value incorrectly turns it into two allowed paths. Preserve
quote/member grammar or fail closed on ambiguity. Add literal D026 evidence for
this case plus the complete C-2 set and benign controls.

The idle-window GLM-5.2 second opinion produced additional cases which the Lead
then executed against the clean committed round-3 bytes. Treat these measured
results as binding repair inputs:

- `LD_LIBRARY_PATH=$ROOT/lib:/etc/escape cat "$ROOT/f"` returns rc 0: the
  complete blob `/safe/lib:/etc/escape` is incorrectly ALLOW-LEXICAL. Member
  parsing must therefore run even when the rendered value starts with `/`.
- `LD_LIBRARY_PATH=:/etc/escape cat "$ROOT/f"` returns rc 0 with the escape
  absent. Account for the path member and fail closed on any ambiguous empty
  member without making benign scalar `IFS=:` a name-based special case.
- `GIT_SSH_COMMAND="ssh -i /etc/key" cat "$ROOT/f"` returns rc 0 with the key
  path absent. Command-text or option-carrying-path grammar must be modeled or
  produce a specific coverage record.
- Preserve `X="$ROOT dir/escape"` as one quoted pathname and rc 1. Do not split
  on quoted or escaped whitespace. Add an escaped-space-plus-later-path case.
- URI/endpoint-shaped assignment values must not be misclassified as one
  filesystem path; account for them in the endpoint domain or emit a specific
  coverage record.

For every accepted closure fixture, execute the actual pre-repair committed
blob and repaired bytes. Static predictions are not D026 evidence.

Owned files only:

- `pathscope_prover.py`
- `SELF_QA_PATHSCOPE.md`
- `STATUS_PATHSCOPE.md`
- new `PATHSCOPE_CAP_OVERRIDE_REPAIR_REPORT_2026-08-13.md`

All paths above are under
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/`.

Extract and run the published PowerShell harness verbatim after editing. Its
outer command must complete cleanly; every embedded identity, count,
transcript, and digest must reproduce exactly. Run AST/syntax checks,
adversarial probes, determinism checks, and `git diff --check` on owned files.
Report exact commands and real output. Do not claim acceptance or commit.
