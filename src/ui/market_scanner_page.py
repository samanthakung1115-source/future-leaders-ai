
from __future__ import annotations

import pandas as pd
import streamlit as st

from market_scanner import MarketScanner


SAMPLE_PATH = "data/samples/market_candidates_sample.csv"


def render():
    st.title("🌍 Market Scanner 海選引擎")
    st.caption("Sprint 3.3")

    st.markdown("""
這一頁的目的不是看持股，而是從候選清單中找出：

- Future Leaders Top N
- Emerging Leaders
- Black Horse
- Tonight Watch List
""")

    uploaded = st.file_uploader("Upload candidate CSV", type=["csv"])
    top_n = st.slider("Top N", 10, 200, 50)

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

    if st.button("🚀 Run Scanner"):
        result = MarketScanner().scan_dataframe(df, top_n=top_n)
        st.session_state["market_scanner_result"] = result

    result = st.session_state.get("market_scanner_result")

    if result is not None and not result.empty:
        st.divider()
        st.subheader("🏆 Tonight Future Leaders")
        st.dataframe(result, use_container_width=True)

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
