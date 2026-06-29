
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timedelta
import json

import pandas as pd


class LivePriceCache:
    """Simple JSON cache for live price snapshots.

    Purpose:
    - Avoid fetching yfinance for every rerun.
    - Make Auto Refresh safer.
    - Keep last successful price if provider fails.
    """

    def __init__(self, cache_path: str = "data/cache/live_price_cache.json", ttl_seconds: int = 60):
        self.cache_path = Path(cache_path)
        self.ttl_seconds = int(ttl_seconds)
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict:
        if not self.cache_path.exists():
            return {}
        try:
            return json.loads(self.cache_path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def save(self, data: dict):
        self.cache_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def is_fresh(self, item: dict) -> bool:
        ts = item.get("cached_at")
        if not ts:
            return False
        try:
            cached_at = datetime.fromisoformat(ts)
            return datetime.now() - cached_at < timedelta(seconds=self.ttl_seconds)
        except Exception:
            return False

    def get(self, ticker: str) -> dict | None:
        ticker = str(ticker).upper().strip()
        data = self.load()
        item = data.get(ticker)
        if item and self.is_fresh(item):
            item["Price Source"] = item.get("Price Source", "cache")
            return item
        return None

    def set(self, ticker: str, snapshot: dict):
        ticker = str(ticker).upper().strip()
        data = self.load()
        data[ticker] = {
            **snapshot,
            "cached_at": datetime.now().isoformat(timespec="seconds"),
        }
        self.save(data)


def _fetch_yfinance_snapshot(ticker: str) -> dict:
    ticker = str(ticker).upper().strip()
    try:
        import yfinance as yf
        stock = yf.Ticker(ticker)
        info = stock.fast_info

        latest = float(getattr(info, "last_price", 0) or 0)
        previous_close = float(getattr(info, "previous_close", 0) or 0)
        year_high = float(getattr(info, "year_high", 0) or 0)

        if latest <= 0:
            hist = stock.history(period="5d")
            if not hist.empty:
                latest = float(hist["Close"].iloc[-1])
                previous_close = float(hist["Close"].iloc[-2]) if len(hist) > 1 else latest

        live_pct = ((latest - previous_close) / previous_close * 100) if previous_close else 0
        dist_high = ((latest - year_high) / year_high * 100) if year_high else 0

        return {
            "ticker": ticker,
            "Live Price": round(latest, 2),
            "Live %": round(live_pct, 2),
            "52W High": round(year_high, 2),
            "Dist High %": round(dist_high, 2),
            "Price Source": "yfinance",
        }
    except Exception as exc:
        return {
            "ticker": ticker,
            "Live Price": 0,
            "Live %": 0,
            "52W High": 0,
            "Dist High %": 0,
            "Price Source": f"fetch_error: {exc}",
        }


def fetch_price_with_cache(ticker: str, ttl_seconds: int = 60) -> dict:
    cache = LivePriceCache(ttl_seconds=ttl_seconds)

    cached = cache.get(ticker)
    if cached:
        cached["Price Source"] = "cache"
        return cached

    snapshot = _fetch_yfinance_snapshot(ticker)

    # Cache only successful prices
    if snapshot.get("Live Price", 0):
        cache.set(ticker, snapshot)

    return snapshot


def _live_action(day_change_pct: float, distance_from_high_pct: float, base_action: str = "") -> str:
    try:
        day = float(day_change_pct or 0)
        dist = float(distance_from_high_pct or 0)
    except Exception:
        return base_action or "維持觀察"

    if day >= 5:
        return "今天漲太多，先不要追"
    if day >= 2 and dist > -5:
        return "接近高點，等回落"
    if day <= -6:
        return "跌幅大，等止跌訊號"
    if day <= -3:
        return "轉弱中，先觀察"
    if -3 <= day <= 1 and dist <= -10:
        return "可觀察，不急買"
    return base_action or "維持觀察"


def enrich_with_cached_live_price(
    df: pd.DataFrame,
    ticker_col: str = "ticker",
    action_col: str | None = "tonight_action",
    ttl_seconds: int = 60,
) -> pd.DataFrame:
    """Add cached live price fields to a DataFrame."""
    if df is None or df.empty:
        return df

    if ticker_col not in df.columns:
        for candidate in ["Ticker 股票行情", "Ticker", "ticker", "股票", "代碼", "Symbol", "symbol"]:
            if candidate in df.columns:
                ticker_col = candidate
                break
        else:
            return df

    out = df.copy()

    live_price, live_pct, high_52, dist_high, source, live_action = [], [], [], [], [], []

    for _, row in out.iterrows():
        ticker = str(row.get(ticker_col, "")).upper().strip()
        snap = fetch_price_with_cache(ticker, ttl_seconds=ttl_seconds)
        base_action = str(row.get(action_col, "")) if action_col and action_col in out.columns else ""

        live_price.append(snap.get("Live Price", 0))
        live_pct.append(snap.get("Live %", 0))
        high_52.append(snap.get("52W High", 0))
        dist_high.append(snap.get("Dist High %", 0))
        source.append(snap.get("Price Source", ""))
        live_action.append(_live_action(snap.get("Live %", 0), snap.get("Dist High %", 0), base_action))

    out["Live Price 最新價"] = live_price
    out["Live % 今日%"] = live_pct
    out["52W High 前高"] = high_52
    out["Dist High % 距前高%"] = dist_high
    out["Live Action 即時行動"] = live_action
    out["Price Source 報價來源"] = source

    return out
