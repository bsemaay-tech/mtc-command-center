# ChatGPT Web Mentor Workflow

This repo uses a three-layer handoff model so ChatGPT Web can act as mentor, architect, and prompt writer without pretending it can see local runtime state.

## Layer 1 - GitHub private repo

Purpose: committed code, schemas, docs, reports, selected screenshots, and accepted artifacts.

Use this layer when the next agent needs durable source-of-truth repo state. ChatGPT can inspect this layer only after the relevant commits are pushed to GitHub.

GitHub is not enough for:

- local uncommitted files
- ignored files unless they were intentionally force-added
- localhost dashboard or API runtime state
- `.env`
- local server logs
- current browser state

## Layer 2 - Codex/Claude handoff bundle

Purpose: local runtime state and snapshots that GitHub cannot show. A bundle can include API health summaries, current git dirty status, local log excerpts, ignored-file summaries, selected source files, selected reports, and a manifest.

Use this layer when ChatGPT needs to reason about the current local session, especially when the repo is dirty or the dashboard/API state matters.

## Layer 3 - Screenshots

Purpose: UI layout, readability, information hierarchy, and visual review.

Use this layer when a reviewer needs to judge whether the dashboard is usable or whether a page matches a visual contract. Screenshots can be committed when curated and small, or uploaded directly in the handoff bundle when large, temporary, or numerous.

## Standard Use

- Push GitHub state first when the repo change is durable and reviewable.
- Attach a handoff bundle when runtime/API/local state affects the decision.
- Attach screenshots when UI judgment matters.
- Never use screenshots as proof of backend correctness or API validation.
