"""LLM gate for regime directives and pre-trade vetoes."""

from __future__ import annotations

from dataclasses import dataclass

from bridge.engine.types import OrderPlan


@dataclass(frozen=True)
class LLMDecision:
    verdict: str
    reason: str


class NullLLMGate:
    """Default-off gate: never calls external APIs and fails open."""

    async def check(self, plan: OrderPlan) -> LLMDecision:
        return LLMDecision(verdict="SKIPPED", reason="llm disabled")
