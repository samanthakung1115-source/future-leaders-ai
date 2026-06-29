
from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class PortfolioPosition:
    ticker: str
    shares: float = 0.0
    cost_basis: float = 0.0
    market_value: float = 0.0
    unrealized_return_pct: float = 0.0
    distance_from_high_pct: float = 0.0
    status: str = "Holding"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PortfolioContext:
    positions: list[PortfolioPosition]

    def get(self, ticker: str) -> PortfolioPosition | None:
        ticker = ticker.upper()
        return next((p for p in self.positions if p.ticker.upper() == ticker), None)

    def tickers(self) -> list[str]:
        return sorted(p.ticker.upper() for p in self.positions)

    def summary(self) -> dict:
        return {
            "positions": len(self.positions),
            "tickers": self.tickers(),
        }
