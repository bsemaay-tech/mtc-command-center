---
name: quantlens-transcript-intake
description: Use when ingesting a YouTube transcript for QuantLens Lab, with duplicate detection, channel quality tracking, blacklist/watchlist handling, and Trader Wiki WIKI_ONLY routing.
---

# QuantLens Transcript Intake

## Purpose

Ingest a YouTube transcript into QuantLens Lab without duplicating previous work. Route strategy videos to candidate intake, useful non-strategy videos to Trader Wiki, and low-quality channels to quality tracking.

## When to use

Use when the user provides a YouTube transcript, video URL, channel info, or asks Codex to process a video transcript for QuantLens Lab.

## Inputs

- Video URL or source URL.
- Transcript text.
- Optional title, channel_name, channel_id, and channel_url.

## Outputs

- Updated `_registry/youtube_video_index.csv` and `.jsonl`.
- Updated `_registry/channel_quality_registry.csv`.
- Optional candidate intake package.
- Optional Trader Wiki note and `11_TRADER_WIKI/trader_wiki_index.csv` record.

## Safety Rules

- Never modify `01_PINE/MTC_V2.pine`.
- Never modify production Python runner files.
- Do not run backtests or optimizations.
- Do not write secrets, API keys, webhooks, exchange keys, or broker account data.
- Do not overwrite existing files.

## Duplicate Detection

Before analysis, extract `video_id`, build `https://www.youtube.com/watch?v=<video_id>`, normalize transcript text, and compute `transcript_hash`.

Stop without creating a new candidate when:

- `video_id` already exists in `_registry/youtube_video_index.csv`.
- `transcript_hash` matches a previous row.
- Same channel + same title + similar transcript indicates possible duplicate.

Duplicate output must include previous candidate ID, status, folder, first_seen_at, last_seen_at, and a clear "Yeni islem yapilmadi" note.

## Video Index Registry

Use `_registry/youtube_video_index.csv` with:

```text
video_id,normalized_url,original_url,title,channel_name,channel_id,transcript_hash,candidate_id,status,first_seen_at,last_seen_at,process_count,notes
```

Update `last_seen_at` and `process_count` on repeat sightings if making registry updates is allowed by the user request. Do not create a second strategy folder for the same video.

## Channel Quality Registry

Use `_registry/channel_quality_registry.csv` with:

```text
channel_key,channel_name,channel_id,total_processed,stop_count,reject_count,salvage_count,candidate_count,wiki_count,last_status,quality_state,blacklist_reason,first_seen_at,last_seen_at,notes
```

If channel info is missing, use `UNKNOWN_CHANNEL` and do not blacklist.

## Channel Watchlist / Blacklist Rules

- STOP and REJECT count as bad.
- SALVAGE is neutral/useful.
- CANDIDATE is good.
- WIKI_ONLY is useful.
- WATCHLIST: last 3 videos include at least 2 STOP or REJECT.
- BLACKLISTED: at least 5 total processed, at least 4 STOP/REJECT, and no CANDIDATE.
- MANUAL_REVIEW: channel has both bad videos and SALVAGE/CANDIDATE.
- GOOD: at least 3 useful outputs.
- WHITELIST channels must not be auto-blacklisted.

## Trader Wiki / WIKI_ONLY Handling

Use `WIKI_ONLY` when there is no codable trading strategy but the transcript contains useful trading, investing, risk, psychology, market structure, execution, backtesting, optimization, or system-development knowledge.

For `WIKI_ONLY`:

- Do not create a candidate folder.
- Do not write to normal strategy candidate registry as a strategy.
- Create a note under `11_TRADER_WIKI/<topic_folder>`.
- Update `11_TRADER_WIKI/trader_wiki_index.csv` and `.jsonl`.
- Write `status = WIKI_ONLY` in the video index.
