
import streamlit as st

from live_price import LivePriceEngine, LiveActionEngine


def render():
    st.title("Live Price Engine 盤中即時現價")
    st.caption("Future Leaders AI v1.1 Sprint 1")

    tickers_text = st.text_input("Tickers", "MYRG,HPE,DELL,GLW,ANET,PANW,URI,FROG")
    tickers = [t.strip().upper() for t in tickers_text.split(",") if t.strip()]

    if st.button("Fetch Live Prices"):
        engine = LivePriceEngine()
        action_engine = LiveActionEngine()

        rows = []
        for snap in engine.fetch_many(tickers):
            d = snap.to_dict()
            d["live_action"] = action_engine.decide(d)
            rows.append(d)

        st.dataframe(rows, use_container_width=True)
        st.caption("注意：yfinance 可能為延遲報價，依交易所資料狀態而定。")
