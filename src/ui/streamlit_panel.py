
import streamlit as st
from .app_bridge import AppBridge

def render():
    st.title("Future Leaders AI - Beta 6")
    ticker=st.text_input("Ticker","TEM")
    if st.button("Analyze"):
        bridge=AppBridge(".")
        result=bridge.analyze(ticker)
        st.subheader(result["recommendation"]["action"])
        st.write(result["research_card"])
        st.write(result["decision_advice"])
        st.write(result["winner_matches"])
