# WP-P0-02 tagging scheme and first-freeze resolution

Date: 2026-08-25

Audit tier: **T2**

Protected surface: **Git refs, additive only**

## Namespace rules

- `pkg/<candidate_id>/<package_hash>` freezes a strategy package only when both a real
  candidate ID and its real package hash exist. Neither may be inferred or invented.
- `release/<component>/<semver>` identifies a deployable component only when a recorded
  semantic version exists for that exact build.
- `legacy/<name>/<date>` freezes historical repository or component state where no package
  identity or semantic release identity applies.

The namespace rules are now active and reserved. This first run populates `legacy/`. It does
not create a `pkg/` tag because the WP-P0-01 inputs contain no candidate ID/package-hash pair,
and it does not create a `release/` tag because they contain no exact component/semver release
identity. The accepted Bridge V1 candidate is deliberately tagged under the exact legacy name
required by the WP-P0-02 contract; no version is invented to populate `release/`.

## Fixed component tags

| Tag | Target resolution rule |
|---|---|
| `legacy/master-freeze/2026-08-25` | current local `refs/heads/master` |
| `legacy/pine-controller/2026-08-25` | path HEAD on current master for `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine` |
| `legacy/mtc-v2-kernel/2026-08-25` | path HEAD on current master for `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core` |
| `legacy/02-mtc-backtest/2026-08-25` | path HEAD on current master for `MTC_COMMAND_CENTER/02_MTC_BACKTEST` |
| `legacy/parity-oracles/2026-08-25` | path HEAD on current master for `MTC_COMMAND_CENTER/12_PARITY_PINETS` |
| `legacy/bridge-v1-accepted/2026-08-25` | recorded accepted/deployed release commit `be007fd802bbfd2eb181d66038c374865d1562ee` |

`12_PARITY_PINETS` is the historical oracle set selected for the parity tag. The accepted
architecture brief names it as the read-only historical oracle corpus, and WP-P0-01 found
`05_PARITY` absent while individually inventorying 732 files under `12_PARITY_PINETS`.

The Bridge identity is unambiguous. It is the tip of both
`refs/heads/integration/bridge-release-20260815` and
`refs/remotes/origin/integration/bridge-release-20260815`; repository records also state
that release `be007fd8` was deployed on 2026-08-17. No successor release SHA was found.

## Evidence-branch tags

Every row marked `YES` in WP-P0-01's `evidence_branches.md` is tagged at the listed ref's
current commit when the script runs. The transformation is:

1. `refs/heads/<name>` becomes branch name `<name>`.
2. `refs/remotes/<remote>/<name>` becomes branch name `<remote>/<name>`; the remote is kept
   so local and remote-tracking refs cannot silently collapse into one tag.
3. Every `/` in that branch name becomes `--`.
4. The tag is `legacy/evbr/<sanitized-branch-name>/2026-08-25`.

The annotated message is exactly
`WP-P0-02 freeze 2026-08-25: evidence-bearing branch <name>`.

Preflight parsed all 317 ref rows, selected exactly 174 `YES` rows, resolved all 174 refs,
and found zero sanitized tag-name collisions. Two refs advanced after WP-P0-01 recorded
them; the contract requires their current tips, so the script freezes the new tips and the
manifest records the older documented SHA:

- `refs/heads/feature/vnext-amendments-20260824`:
  `2fbe4e0b541986dc7209fa0e116178908381ab95` ->
  `3b088fba01a1f73e6ccda3a8cbfd622c1d976bb1`.
- `refs/heads/feature/wp-p0-15-branch-freshness-20260824`:
  `10876fb9eb818b00141e8b808fe6a4d706ffc06e` ->
  `e5d7cbf5e7a1d9a6c211192f54330eec60b635bf`.

## Additive/idempotent behavior

The script preflights the complete desired set before creating a tag. For each exact tag
name it:

- creates an annotated tag only when the name is absent;
- records and skips an existing tag at the same target;
- records and skips an existing tag at a different target;
- never deletes, moves, force-updates, or overwrites a ref.

`TAGS_BEFORE.txt` and `TAGS_AFTER.txt` contain the complete sorted tag listings surrounding
the actual run. `TAG_MANIFEST.txt` records status, name, peeled target commit, and target
description for all desired freezes.

## Skip and UNKNOWN records

The authoritative first run started with zero tags and completed with 180 tags:

- created: **180**;
- existing same-target skips: **0**;
- existing different-target skips: **0**;
- unresolved/UNKNOWN targets: **0**;
- missing evidence refs: **0**.

No tag was replaced, moved, deleted, or force-updated. `pkg/` and `release/` have explicit
identity-gated skip records above: their required identities were absent, so inventing a tag
would have violated the scheme.
