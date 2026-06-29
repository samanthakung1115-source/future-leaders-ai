
import streamlit as st

from sts_integration import STSBridge


def render_portfolio_context_panel():
    st.subheader("STS Portfolio Context")

    uploaded = st.file_uploader("Upload STS portfolio CSV", type=["csv"])

    if not uploaded:
        st.info("Upload a CSV exported from STS to enable portfolio context.")
        return None

    temp_path = "sts_portfolio_upload.csv"
    with open(temp_path, "wb") as f:
        f.write(uploaded.getbuffer())

    bridge = STSBridge()
    portfolio = bridge.load_csv(temp_path)

    st.success(f"Loaded {len(portfolio.positions)} portfolio positions.")
    st.write(portfolio.summary())

    return portfolio
