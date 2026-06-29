
from __future__ import annotations

from .live_action import LiveActionEngine
from .price_engine import LivePriceEngine


class CandidatePriceEnricher:
    """Attach live price snapshots and live actions to candidate rows."""

    def __init__(self, price_engine: LivePriceEngine | None = None, action_engine: LiveActionEngine | None = None):
        self.price_engine = price_engine or LivePriceEngine()
        self.action_engine = action_engine or LiveActionEngine()

    def enrich(self, candidates: list[dict]) -> list[dict]:
        tickers = [row.get("ticker", "").upper() for row in candidates]
        prices = {p.ticker: p.to_dict() for p in self.price_engine.fetch_many(tickers)}

        enriched = []
        for row in candidates:
            ticker = row.get("ticker", "").upper()
            snapshot = prices.get(ticker, {"ticker": ticker})
            live_action = self.action_engine.decide(snapshot, base_action=row.get("tonight_action", ""))
            enriched.append({
                **row,
                "live_price": snapshot.get("latest_price", 0),
                "day_change_pct": snapshot.get("day_change_pct", 0),
                "fifty_two_week_high": snapshot.get("fifty_two_week_high", 0),
                "distance_from_high_pct": snapshot.get("distance_from_high_pct", 0),
                "live_action": live_action,
                "price_source": snapshot.get("source", ""),
            })
        return enriched
