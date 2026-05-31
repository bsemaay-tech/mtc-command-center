# 00_PYTHON

Minimal Python skeleton for MTC V2.

Scope:
- Build-stage only
- No run/optimize orchestration yet
- First target is layer-by-layer Pine/Python parity
- Start with a single sample signal family and keep parity before adding more layers

Rules:
- Do not add features outside the active layer
- Keep behavior deterministic
- Match naming with Pine config and architecture docs
- Treat this folder as the active Python implementation target

Suggested first implementation order:
1. core/types.py
2. core/config.py
3. core/runner.py
4. signals/supertrend.py
5. tests/test_supertrend_smoke.py
