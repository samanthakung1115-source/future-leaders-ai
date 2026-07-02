
import streamlit as st

from sts_api import STSApiClient, STSApiConfig


def render():
    st.title("STS API Engine")
    st.caption("v1.0 Sprint 1 - Apps Script JSON API")

    cfg = STSApiConfig.load()

    with st.container(border=True):
        st.markdown("### API Config")
        if not cfg.api_base_url or "PASTE_YOUR" in cfg.api_base_url:
            st.warning("尚未設定 Apps Script Web App URL。請更新 config/sts_api_config.json。")
        else:
            st.success("API URL configured.")
            st.code(cfg.api_base_url)

    client = STSApiClient(cfg)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Health"):
            st.json(client.health())

    with col2:
        if st.button("Portfolio"):
            payload = client.portfolio()
            st.json(payload)
            df = client.portfolio_df()
            if not df.empty:
                st.dataframe(df, use_container_width=True)

    with col3:
        if st.button("Summary"):
            payload = client.summary()
            st.json(payload)
            df = client.summary_df()
            if not df.empty:
                st.dataframe(df, use_container_width=True)

    with col4:
        if st.button("All"):
            st.json(client.all())
