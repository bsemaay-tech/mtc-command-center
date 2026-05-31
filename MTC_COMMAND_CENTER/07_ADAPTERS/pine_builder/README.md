# Pine Builder Adapter

This adapter will manage metadata for Pine drafts, reviews, compile observations, and promotion readiness.

## MVP-0 State

Not implemented. No production Pine files are modified.

## Future Contract

The adapter may track draft paths, review reports, compile observations, user approvals, and promotion status. It should update `03_STATUS/PINE_BUILDER_STATUS.json`.

## Safety

Drafts stay separate from `MTC_V2.pine` until the user explicitly approves promotion.
