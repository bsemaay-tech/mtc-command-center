# Release SemVer and Changelog Discipline

## Versioning
- Use SemVer: `MAJOR.MINOR.PATCH`
- `MAJOR`: contract-breaking behavior changes
- `MINOR`: backward-compatible features
- `PATCH`: backward-compatible fixes

## Changelog Rules
- Keep `CHANGELOG.md` updated on every release merge.
- Maintain an `Unreleased` section for pending changes.
- Group entries under `Added`, `Changed`, `Fixed`, `Docs`.
- Reference roadmap phase/sprint item where possible.

## Release Steps
1. Update version metadata.
2. Update `CHANGELOG.md`.
3. Tag release (`vX.Y.Z`).
4. Publish release notes with migration notes if needed.
