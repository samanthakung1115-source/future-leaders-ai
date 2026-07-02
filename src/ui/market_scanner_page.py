
from __future__ import annotations

import pandas as pd
import streamlit as st

from market_scanner import MarketScanner
from ai_engine import MemoryEngine


SAMPLE_PATH = "data/samples/market_candidates_sample.csv"


def _add_memory_changes(df: pd.DataFrame, memory: MemoryEngine) -> pd.DataFrame:
    if df is None or df.empty:
        return df
    out = df.copy()
    out["score_change"] = out["ticker"].apply(memory.score_change)
    return out


def render():
    st.title("🌍 Market Scanner 海選引擎")
    st.caption("Sprint 3.4 + AI Memory")

    uploaded = st.file_uploader("Upload candidate CSV", type=["csv"])
    top_n = st.slider("Top N", 10, 200, 50)
    save_memory = st.checkbox("Save to AI Memory", value=True)

    with st.expander("CSV 欄位格式"):
        st.write("至少需要 ticker 欄位。建議欄位：")
        st.code("ticker,trend,momentum,fundamental,narrative,valuation,flow,decision,theme")

    if uploaded:
        df = pd.read_csv(uploaded)
        st.success("已讀取上傳 CSV。")
    else:
        df = pd.read_csv(SAMPLE_PATH)
        st.info("目前使用內建 sample。之後可上傳自己的候選股 CSV。")

    st.subheader("Candidate Preview")
    st.dataframe(df.head(30), use_container_width=True)

    memory = MemoryEngine()

    if st.button("🚀 Run Scanner"):
        result = MarketScanner().scan_dataframe(df, top_n=top_n)
        result = _add_memory_changes(result, memory)

        if save_memory:
            count = memory.update_from_dataframe(result)
            st.success(f"已寫入 AI Memory：{count} 檔股票。")
            result = _add_memory_changes(result, memory)

        st.session_state["market_scanner_result"] = result

    result = st.session_state.get("market_scanner_result")

    if result is not None and not result.empty:
        st.divider()
        st.subheader("🏆 Tonight Future Leaders")
        st.dataframe(result, use_container_width=True)

        st.divider()
        st.subheader("📈 Top Score Movers")
        movers = result.sort_values("score_change", ascending=False)
        st.dataframe(movers[["rank", "ticker", "leader_score", "score_change", "role", "theme"]], use_container_width=True)

        st.divider()
        st.subheader("🐎 Black Horse Candidates")
        black = result[result["black_horse"] == True]
        if black.empty:
            st.caption("目前沒有符合 Black Horse 規則的股票。")
        else:
            st.dataframe(black, use_container_width=True)

        st.divider()
        st.subheader("⭐ Emerging / Future Leaders")
        leaders = result[result["role"].astype(str).str.contains("Future Leader|Emerging Leader", na=False)]
        if leaders.empty:
            st.caption("目前沒有 Future Leader / Emerging Leader。")
        else:
            st.dataframe(leaders, use_container_width=True)
