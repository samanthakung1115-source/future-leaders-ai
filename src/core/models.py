
from __future__ import annotations
from dataclasses import dataclass, asdict, field

@dataclass
class Candidate:
    ticker: str
    score: int
    why_selected: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class PortfolioPosition:
    ticker: str
    status: str = "Holding"
    shares: float = 0.0
    cost_return_pct: float = 0.0
    distance_from_high_pct: float = 0.0
    alert: str = ""
    action: str = ""
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class ActionItem:
    ticker: str
    action: str
    priority: str
    reason: str
    risk_note: str
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class SamanthaBrief:
    title: str
    summary: str
    future_leaders: list[dict]
    portfolio_warnings: list[str]
    action_plan: list[dict]
    samantha_comment: str
    data_health: dict = field(default_factory=dict)
    def to_dict(self) -> dict:
        return asdict(self)
