
import streamlit as st

from sts_api import STSApiClient, STSApiConfig

ACTIONS = [
    ("health", "Health"),
    ("sheets", "Sheets"),
    ("portfolio", "Portfolio"),
    ("watch", "看盤提醒"),
    ("decision", "穩定決策"),
    ("summary", "今日摘要"),
    ("roles", "股票角色表"),
    ("all", "All"),
]

def render():
    st.title("STS API Engine")
    st.caption("v1.0 Sprint 2 - Multi-sheet JSON API")

    cfg = STSApiConfig.load()

    with st.container(border=True):
        st.markdown("### API Config")
        if not cfg.api_base_url or "PASTE_YOUR" in cfg.api_base_url:
            st.warning("尚未設定 Apps Script Web App URL。請更新 config/sts_api_config.json。")
        else:
            st.success("API URL configured.")
            st.code(cfg.api_base_url)

    client = STSApiClient(cfg)

    action = st.radio("Action", [a[0] for a in ACTIONS], format_func=lambda x: dict(ACTIONS)[x], horizontal=True)

    if st.button("Run API"):
        payload = client.get(action)
        st.json(payload)

        if action not in ["health", "sheets", "all"]:
            df = client.dataframe(action)
            if not df.empty:
                st.subheader(f"{dict(ACTIONS)[action]} DataFrame")
                st.dataframe(df, use_container_width=True)

        if action == "all":
            for key in ["portfolio", "watch", "decision", "summary", "roles"]:
                block = payload.get(key, {})
                rows = block.get("rows", []) if isinstance(block, dict) else []
                if rows:
                    st.subheader(key)
                    st.dataframe(rows, use_container_width=True)
