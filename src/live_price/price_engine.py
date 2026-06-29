
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable


@dataclass
class PriceSnapshot:
    ticker: str
    latest_price: float = 0.0
    previous_close: float = 0.0
    day_change_pct: float = 0.0
    fifty_two_week_high: float = 0.0
    distance_from_high_pct: float = 0.0
    source: str = "yfinance"

    def to_dict(self) -> dict:
        return asdict(self)


class LivePriceEngine:
    """Fetch live or delayed market prices using yfinance.

    Note:
    yfinance data can be delayed depending on exchange and data availability.
    The engine is designed to fail gracefully and return structured results.
    """

    def fetch_many(self, tickers: Iterable[str]) -> list[PriceSnapshot]:
        return [self.fetch_one(ticker) for ticker in tickers if str(ticker).strip()]

    def fetch_one(self, ticker: str) -> PriceSnapshot:
        ticker = ticker.upper().strip()

        try:
            import yfinance as yf
        except Exception:
            return PriceSnapshot(ticker=ticker, source="yfinance_not_available")

        try:
            stock = yf.Ticker(ticker)
            info = stock.fast_info

            latest = float(getattr(info, "last_price", 0) or 0)
            prev_close = float(getattr(info, "previous_close", 0) or 0)
            high_52w = float(getattr(info, "year_high", 0) or 0)

            if latest <= 0:
                hist = stock.history(period="5d")
                if not hist.empty:
                    latest = float(hist["Close"].iloc[-1])
                    prev_close = float(hist["Close"].iloc[-2]) if len(hist) > 1 else latest

            day_change_pct = self._pct_change(latest, prev_close)
            distance_from_high_pct = self._distance_from_high(latest, high_52w)

            return PriceSnapshot(
                ticker=ticker,
                latest_price=round(latest, 2),
                previous_close=round(prev_close, 2),
                day_change_pct=round(day_change_pct, 2),
                fifty_two_week_high=round(high_52w, 2),
                distance_from_high_pct=round(distance_from_high_pct, 2),
            )

        except Exception:
            return PriceSnapshot(ticker=ticker, source="fetch_error")

    def _pct_change(self, latest: float, previous: float) -> float:
        if previous <= 0:
            return 0.0
        return (latest - previous) / previous * 100

    def _distance_from_high(self, latest: float, high: float) -> float:
        if high <= 0:
            return 0.0
        return (latest - high) / high * 100
