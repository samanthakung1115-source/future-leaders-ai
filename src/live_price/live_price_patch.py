
from __future__ import annotations

from dataclasses import dataclass, asdict


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
    def fetch_one(self, ticker: str) -> PriceSnapshot:
        ticker = str(ticker).upper().strip()
        try:
            import yfinance as yf
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

            day_change_pct = ((latest - prev_close) / prev_close * 100) if prev_close else 0
            distance_from_high_pct = ((latest - high_52w) / high_52w * 100) if high_52w else 0

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

    def fetch_many(self, tickers):
        return {str(t).upper().strip(): self.fetch_one(t).to_dict() for t in tickers if str(t).strip()}


class LiveActionEngine:
    def decide(self, row: dict) -> str:
        day = float(row.get("day_change_pct", 0) or 0)
        dist = float(row.get("distance_from_high_pct", 0) or 0)

        if day >= 5:
            return "今天漲太多，先不要追"
        if day >= 2 and dist > -5:
            return "接近高點，等回落"
        if -3 <= day <= 1 and dist <= -10:
            return "可觀察，不急買"
        if day <= -6:
            return "跌幅大，等止跌訊號"
        if day <= -3:
            return "轉弱中，先觀察"
        return "維持觀察"


def enrich_with_live_price(df, ticker_col="Ticker"):
    """Add live price columns to an existing pandas DataFrame.

    Required:
    - df has a ticker column, default `Ticker`.

    Added columns:
    - Live Price
    - Live %
    - 52W High
    - Dist High %
    - Live Action
    - Price Source
    """
    if df is None or df.empty or ticker_col not in df.columns:
        return df

    engine = LivePriceEngine()
    action_engine = LiveActionEngine()

    tickers = df[ticker_col].astype(str).str.upper().str.strip().tolist()
    prices = engine.fetch_many(tickers)

    live_prices = []
    live_pct = []
    highs = []
    dist_high = []
    actions = []
    sources = []

    for ticker in tickers:
        p = prices.get(ticker, {})
        live_prices.append(p.get("latest_price", 0))
        live_pct.append(p.get("day_change_pct", 0))
        highs.append(p.get("fifty_two_week_high", 0))
        dist_high.append(p.get("distance_from_high_pct", 0))
        sources.append(p.get("source", ""))
        actions.append(action_engine.decide(p))

    out = df.copy()
    out["Live Price"] = live_prices
    out["Live %"] = live_pct
    out["52W High"] = highs
    out["Dist High %"] = dist_high
    out["Live Action"] = actions
    out["Price Source"] = sources
    return out
