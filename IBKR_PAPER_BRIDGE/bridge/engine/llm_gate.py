"""LLM gate for regime directives and pre-trade vetoes."""

from __future__ import annotations

import asyncio
import hashlib
import inspect
import re
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Callable

from bridge.engine.types import OrderPlan, RegimeDirective


@dataclass(frozen=True)
class LLMDecision:
    verdict: str
    reason: str


class NullLLMGate:
    """Default-off gate: never calls external APIs and fails open."""

    async def check(self, plan: OrderPlan) -> LLMDecision:
        return LLMDecision(verdict="SKIPPED", reason="llm disabled")


class LLMGate:
    def __init__(
        self,
        regime_provider: Callable[[list[str]], dict[str, Any]] | None = None,
        veto_provider: Callable[[OrderPlan], dict[str, Any]] | None = None,
        config_direction: str = "BOTH",
        min_confidence: float = 0.6,
        ttl_clamp_minutes: tuple[int, int] = (15, 1440),
        veto_enabled: bool = False,
        veto_deadline_s: float = 5.0,
        max_vetos_per_day: int = 20,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self.regime_provider = regime_provider
        self.veto_provider = veto_provider
        self.config_direction = config_direction
        self.min_confidence = min_confidence
        self.ttl_clamp_minutes = ttl_clamp_minutes
        self.veto_enabled = veto_enabled
        self.veto_deadline_s = veto_deadline_s
        self.max_vetos_per_day = max_vetos_per_day
        self.now = now or (lambda: datetime.now(UTC))
        self.directive: RegimeDirective | None = None
        self.sources_hash: str | None = None
        self.veto_calls_today = 0

    async def refresh_regime(self, sources: list[str]) -> RegimeDirective | None:
        if self.regime_provider is None:
            return None
        sanitized = [self._sanitize_source(source) for source in sources]
        self.sources_hash = hashlib.sha256("\n".join(sanitized).encode("utf-8")).hexdigest()
        raw = self.regime_provider(sanitized)
        if inspect.isawaitable(raw):
            raw = await raw
        directive = self._parse_directive(raw)
        if directive is None:
            return None
        self.directive = directive
        return directive

    def effective_directions(self) -> set[str]:
        config = self._allowed(self.config_direction)
        directive = self.directive
        if directive is None:
            return config

        age = self.now() - directive.ts
        ttl = timedelta(minutes=directive.ttl_minutes)
        if age <= ttl * 2:
            return config & self._allowed(directive.regime)
        return config

    async def check(self, plan: OrderPlan) -> LLMDecision:
        if not self.veto_enabled or self.veto_provider is None:
            return LLMDecision("SKIPPED", "llm disabled")
        if self.veto_calls_today >= self.max_vetos_per_day:
            return LLMDecision("SKIPPED", "LLM_COST_LIMIT")
        self.veto_calls_today += 1
        try:
            raw = await asyncio.wait_for(self._call_veto(plan), timeout=self.veto_deadline_s)
        except TimeoutError:
            return LLMDecision("SKIPPED", "deadline")
        verdict = str(raw.get("verdict", "PASS")).upper()
        if verdict not in {"PASS", "VETO"}:
            return LLMDecision("SKIPPED", "invalid veto")
        return LLMDecision(verdict, str(raw.get("reason", "")))

    async def _call_veto(self, plan: OrderPlan) -> dict[str, Any]:
        assert self.veto_provider is not None
        raw = self.veto_provider(plan)
        if inspect.isawaitable(raw):
            return await raw
        return raw

    def _parse_directive(self, raw: dict[str, Any]) -> RegimeDirective | None:
        try:
            regime = str(raw["regime"]).upper()
            confidence = float(raw["confidence"])
            ttl = int(raw["ttl_minutes"])
        except (KeyError, TypeError, ValueError):
            return None
        if regime not in {"LONG_ONLY", "SHORT_ONLY", "BOTH", "NO_TRADE"}:
            return None
        if confidence < self.min_confidence:
            return None
        min_ttl, max_ttl = self.ttl_clamp_minutes
        ttl = max(min_ttl, min(max_ttl, ttl))
        return RegimeDirective(
            ts=self.now(),
            regime=regime,  # type: ignore[arg-type]
            confidence=confidence,
            ttl_minutes=ttl,
            sources=[str(item) for item in raw.get("sources", [])],
            rationale=str(raw.get("rationale", "")),
        )

    @staticmethod
    def _sanitize_source(source: str) -> str:
        source = re.sub(r"https?://\S+", "", source)
        source = source.replace("```", "")
        source = "".join(ch for ch in source if ch.isprintable())
        return f"[SOURCE_START]{source[:280]}[SOURCE_END]"

    @staticmethod
    def _allowed(direction: str) -> set[str]:
        return {
            "BOTH": {"LONG", "SHORT"},
            "LONG_ONLY": {"LONG"},
            "SHORT_ONLY": {"SHORT"},
            "NO_TRADE": set(),
        }[direction]
