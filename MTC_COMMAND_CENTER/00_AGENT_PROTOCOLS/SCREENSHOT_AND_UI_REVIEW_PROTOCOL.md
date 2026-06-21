# Screenshot and UI Review Protocol

Screenshots support UI review. They do not replace backend, API, or data validation.

## Storage

Latest curated screenshots:

```text
MTC_COMMAND_CENTER/11_TRIAGE/ui_snapshots/latest/
```

Dated review screenshots:

```text
MTC_COMMAND_CENTER/11_TRIAGE/ui_snapshots/YYYY-MM-DD/
```

Archive or temporary image sets should stay out of the repo unless the user accepts them.

## Recommended Screenshots

- `home.png`
- `strategy_detail.png`
- `night_artifacts.png`
- `backtest_launch.png`
- `research_profile_artifact.png`

## Commit Policy

- Commit only curated UI snapshots.
- Keep screenshots compressed.
- Do not commit dozens of duplicate screenshots.
- Put large image sets into a handoff zip instead of the repo.
- Do not fabricate screenshots.

## Review Policy

Screenshots help reviewers judge layout, readability, information hierarchy, and visual regressions. They do not prove API health, score correctness, read-only behavior, or artifact validity.
