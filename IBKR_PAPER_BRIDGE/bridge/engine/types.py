"""Core pydantic models (Bar, Signal, OrderPlan, Position, etc.)."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Bar(BaseModel):
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class Signal(BaseModel):
    ts: datetime
    symbol: str
    direction: Literal["LONG", "SHORT", "FLAT"]
    reason: str
    ref_price: float
    stop_loss: float | None = None
    take_profit: float | None = None


class OrderPlan(BaseModel):
    decision_uid: str | None = None
    signal: Signal
    qty: float
    entry_type: Literal["MKT", "LMT"]
    limit_price: float | None = None
    stop_loss: float
    take_profit: float | None = None
    leverage: int = 1
    risk_dollars: float = 0.0
    risk_pct: float = 0.0


class Position(BaseModel):
    symbol: str
    size: float
    entry_px: float
    unrealized: float = 0.0
    leverage: int = 1
    liquidation_px: float | None = None
    margin_used: float = 0.0


class AccountSnapshot(BaseModel):
    equity: float
    available_margin: float
    withdrawable: float = 0.0


class BrokerOrder(BaseModel):
    cloid: str
    oid: int | None = None
    coin: str
    side: Literal["BUY", "SELL"]
    size: float
    status: str = "OPEN"
    role: Literal["ENTRY", "SL", "TP", "CLOSE", "UNKNOWN"] = "UNKNOWN"
    reduce_only: bool = False
    trigger_px: float | None = None
    order_type: str | None = None
    order_ref: str | None = None


class FillEvent(BaseModel):
    event_type: Literal["FILL"] = "FILL"
    fill_id: str
    cloid: str
    coin: str
    qty: float
    px: float
    ts: datetime
    fee: float = 0.0
    funding: float = 0.0
    role: Literal["ENTRY", "SL", "TP", "CLOSE", "UNKNOWN"] = "UNKNOWN"


class OrderUpdateEvent(BaseModel):
    event_type: Literal["ORDER"] = "ORDER"
    cloid: str
    status: str
    ts: datetime
    filled_qty: float | None = None
    avg_fill_px: float | None = None


BrokerEvent = FillEvent | OrderUpdateEvent


class Rejection(BaseModel):
    stage: Literal["RISK", "LLM", "STATE"]
    reason: str


class RegimeDirective(BaseModel):
    ts: datetime
    regime: Literal["LONG_ONLY", "SHORT_ONLY", "BOTH", "NO_TRADE"]
    confidence: float
    ttl_minutes: int
    sources: list[str]
    rationale: str
