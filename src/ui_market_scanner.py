
import pandas as pd
import streamlit as st

from market_scanner import MarketScanner


def render():
    st.title("🌍 Future Leaders Market Scanner")
    st.caption("Sprint 3.2")

    uploaded = st.file_uploader("Upload candidate CSV", type=["csv"])
    top_n = st.slider("Top N", 10, 200, 50)

    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("data/samples/market_candidates_sample.csv")

    if st.button("Run Scanner"):
        result = MarketScanner().scan_dataframe(df, top_n=top_n)
        st.subheader("Tonight Future Leaders")
        st.dataframe(result, use_container_width=True)

        black = result[result["black_horse"] == True]
        st.subheader("🐎 Black Horse Candidates")
        st.dataframe(black, use_container_width=True)
