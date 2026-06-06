# USER_INTAKE — drop folder for raw research inputs

This is **your** drop folder. Put new raw material here and an AI agent routes it
into the right place. You do not need to know the internal folder layout.

## What to drop here

- Video / course / article **transcripts** (`.txt`, `.md`)
- **Screenshots** of charts, setups, indicator panels (`.png`, `.jpg`)
- Short notes describing what a file is about (`.md`, `.txt`)

## How to name files (optional but helps routing)

Give the agent a hint in the filename. Either form works:

```
<hint>__<source>.<ext>
STG035__rsi_confluence_part2_transcript.md      # belongs to existing strategy STG035
8ema_pullback__youtube_xyz.txt                   # new idea, no STG yet
ada_two_candle_sr__chart_screenshot.png
```

- If the filename starts with an existing `STGxxx` id, it is routed straight into
  that strategy's `source_intake/`.
- Otherwise the agent fuzzy-matches the hint against known strategies, or — if it
  is a genuinely new idea — opens a new candidate via the transcript intake
  workflow (`03_QUANTLENS/_user_guide/09_TRANSCRIPT_INTAKE_WORKFLOW.md`).

## What the agent does (you can also just ask it in chat)

1. Run the router (dry-run shows the plan, nothing moves):
   ```
   python 03_QUANTLENS/tools/route_user_intake.py
   ```
2. Apply the routing (moves files into each strategy's `source_intake/`):
   ```
   python 03_QUANTLENS/tools/route_user_intake.py --apply
   ```
3. The agent then updates the target strategy's `source_intake/intake_report.md`
   and re-runs `build_strategy_research_registry.py` so the
   **Strategy Research Lab** dashboard tab reflects the new material.

## Routing target

Each strategy lives in `03_QUANTLENS/strategies/STGxxx_*/` and now has a
`source_intake/` subfolder with `transcripts/`, `screenshots/`, and (once notes
exist) `intake_report.md`. That keeps everything for one strategy in one place.

> Files left here are never deleted automatically. Routing only **moves** them
> into a strategy folder; nothing leaves the repository.
