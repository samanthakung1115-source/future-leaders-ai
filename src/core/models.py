
from __future__ import annotations

from dataclasses import dataclass, asdict, field


@dataclass
class RankingCandidate:
    ticker: str
    ai_score: float = 0
    growth_score: float = 0
    quality_score: float = 0
    risk_score: float = 0
    theme: str = ""
    dna: list[str] = field(default_factory=list)
    why_selected: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    previous_rank: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RankedCandidate:
    rank: int
    ticker: str
    total_score: float
    verdict: str
    change: str
    theme: str
    dna: list[str]
    why_selected: list[str]
    risks: list[str]

    def to_dict(self) -> dict:
        return asdict(self)
