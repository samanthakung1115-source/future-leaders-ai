
import streamlit as st

from ai_engine import MemoryEngine


def render():
    st.title("🧠 AI Memory")
    st.caption("Sprint 3.4")

    memory = MemoryEngine()
    df = memory.latest_summary()

    if df.empty:
        st.info("AI Memory 目前沒有資料。請先到 Market Scanner 執行並儲存。")
        return

    st.subheader("Leader Score Memory Summary")
    st.dataframe(df, use_container_width=True)

    st.subheader("Top Movers")
    st.dataframe(df.sort_values("score_change", ascending=False).head(20), use_container_width=True)

    ticker = st.text_input("查詢單一股票歷史", "")
    if ticker:
        hist = memory.history(ticker)
        if hist:
            st.json(hist)
        else:
            st.warning("查無歷史資料。")
