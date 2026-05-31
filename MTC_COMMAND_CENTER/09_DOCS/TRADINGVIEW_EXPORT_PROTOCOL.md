# TradingView Export Protocol

TradingView exports are user-provided evidence.

Rules:

- AI requests the exact symbol, timeframe, case ID, export type, and save location.
- User places files under `00_INBOX/from_user/<input_id>/`.
- AI hashes files before deriving any normalized output.
- Original exports are not edited.
- A manifest links export files to case ID and settings hash.

Missing exports must be marked `WAITING_FOR_USER`.
