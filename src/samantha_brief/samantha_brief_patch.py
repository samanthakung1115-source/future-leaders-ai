
from __future__ import annotations

import pandas as pd
import streamlit as st


def _find_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for c in candidates:
        if c in df.columns:
            return c
    return None


def build_samantha_brief(
    radar_df: pd.DataFrame | None = None,
    portfolio_df: pd.DataFrame | None = None,
    coach_notes: list[str] | None = None,
) -> list[str]:
    """Build Samantha's one-line daily brief.

    This patch intentionally uses flexible column detection so it can work with
    your existing app.py table names.

    Inputs can be any of:
    - radar_df: Future Leaders / Radar table
    - portfolio_df: STS / Portfolio table
    - coach_notes: existing Decision Coach notes
    """
    notes: list[str] = []

    # Radar / live price logic
    if radar_df is not None and not radar_df.empty:
        ticker_col = _find_col(radar_df, [
            "Ticker 股票行情", "Ticker", "ticker", "股票", "代碼", "Symbol", "symbol"
        ])
        action_col = _find_col(radar_df, [
            "Live Action 即時行動", "Live Action", "Tonight Action 今晚行動", "Tonight Action"
        ])
        score_col = _find_col(radar_df, [
            "AI Score", "Score", "total_score", "總分", "AI分數"
        ])

        if ticker_col and action_col:
            hot = radar_df[radar_df[action_col].astype(str).str.contains("不要追|等回落", na=False)]
            if not hot.empty:
                tickers = ", ".join(hot[ticker_col].astype(str).head(3).tolist())
                notes.append(f"今天 {tickers} 有追高風險，Samantha 建議先等回落。")

            watch = radar_df[radar_df[action_col].astype(str).str.contains("可觀察|維持觀察", na=False)]
            if not watch.empty:
                tickers = ", ".join(watch[ticker_col].astype(str).head(3).tolist())
                notes.append(f"今晚可優先觀察：{tickers}。")

        if ticker_col and score_col:
            try:
                top = radar_df.sort_values(score_col, ascending=False).head(1)
                if not top.empty:
                    notes.append(f"目前最高分候選：{top.iloc[0][ticker_col]}，請先研究原因，不要只看價格。")
            except Exception:
                pass

    # Portfolio logic
    if portfolio_df is not None and not portfolio_df.empty:
        ticker_col = _find_col(portfolio_df, [
            "Ticker 股票行情", "Ticker", "ticker", "股票", "代碼", "Symbol", "symbol"
        ])
        return_col = _find_col(portfolio_df, [
            "cost_return_pct", "距成本%", "距成本", "Return %", "報酬率%", "損益%"
        ])

        if ticker_col and return_col:
            try:
                temp = portfolio_df.copy()
                temp["_return"] = temp[return_col].astype(str).str.replace("%", "", regex=False).str.replace(",", "", regex=False).astype(float)

                weak = temp[temp["_return"] <= -20]
                if not weak.empty:
                    tickers = ", ".join(weak[ticker_col].astype(str).head(3).tolist())
                    notes.append(f"{tickers} 仍屬壓力持股，不要在沒有新證據時攤平。")

                winners = temp[temp["_return"] >= 50]
                if not winners.empty:
                    tickers = ", ".join(winners[ticker_col].astype(str).head(3).tolist())
                    notes.append(f"{tickers} 已是強勢獲利股，請先想好續抱或分批減碼規則。")
            except Exception:
                pass

    # Existing coach notes
    if coach_notes:
        for note in coach_notes[:2]:
            if note:
                notes.append(str(note))

    if not notes:
        notes.append("今天先維持觀察，等待更明確的價格與趨勢訊號。")

    return notes[:5]


def render_samantha_brief(
    radar_df: pd.DataFrame | None = None,
    portfolio_df: pd.DataFrame | None = None,
    coach_notes: list[str] | None = None,
):
    """Render Samantha brief at the top of your app."""
    notes = build_samantha_brief(
        radar_df=radar_df,
        portfolio_df=portfolio_df,
        coach_notes=coach_notes,
    )

    with st.container(border=True):
        st.markdown("### 🧠 Samantha 今日一句話")
        for note in notes:
            st.write(f"✅ {note}")
