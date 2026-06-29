
from __future__ import annotations

import pandas as pd


def build_radar_live_action(day_change_pct: float, distance_from_high_pct: float, base_action: str = "") -> str:
    """Radar-specific live action rule."""
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


def _safe_get_fast_info(ticker: str) -> dict:
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
            "Live Price": round(latest, 2),
            "Live %": round(live_pct, 2),
            "52W High": round(year_high, 2),
            "Dist High %": round(dist_high, 2),
            "Price Source": "yfinance",
        }

    except Exception:
        return {
            "Live Price": 0,
            "Live %": 0,
            "52W High": 0,
            "Dist High %": 0,
            "Price Source": "fetch_error",
        }


def enrich_radar_with_live_price(
    df: pd.DataFrame,
    ticker_col: str = "Ticker 股票行情",
    action_col: str = "Tonight Action 今晚行動",
) -> pd.DataFrame:
    """Add live price columns to Radar DataFrame.

    Designed for existing Next DDOG / CRDO / RKLB Radar table.

    Adds:
    - Live Price
    - Live %
    - 52W High
    - Dist High %
    - Live Action 即時行動
    - Price Source
    """
    if df is None or df.empty:
        return df

    if ticker_col not in df.columns:
        for candidate in ["Ticker", "ticker", "股票", "代碼", "Symbol", "symbol"]:
            if candidate in df.columns:
                ticker_col = candidate
                break
        else:
            return df

    out = df.copy()

    live_price = []
    live_pct = []
    high_52w = []
    dist_high = []
    source = []
    live_action = []

    for _, row in out.iterrows():
        ticker = str(row.get(ticker_col, "")).strip().upper()
        info = _safe_get_fast_info(ticker)

        base_action = str(row.get(action_col, "")) if action_col in out.columns else ""
        action = build_radar_live_action(
            info.get("Live %", 0),
            info.get("Dist High %", 0),
            base_action=base_action,
        )

        live_price.append(info["Live Price"])
        live_pct.append(info["Live %"])
        high_52w.append(info["52W High"])
        dist_high.append(info["Dist High %"])
        source.append(info["Price Source"])
        live_action.append(action)

    out["Live Price 最新價"] = live_price
    out["Live % 今日%"] = live_pct
    out["52W High 前高"] = high_52w
    out["Dist High % 距前高%"] = dist_high
    out["Live Action 即時行動"] = live_action
    out["Price Source 報價來源"] = source

    return out
