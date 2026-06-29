
import streamlit as st

from sts_sync import STSLiveSyncEngine, SyncConfig


def render():
    st.title("STS Live Sync Engine")
    st.caption("Future Leaders AI v1.1 Sprint 2")

    config = SyncConfig.load()

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Source", config.source_name)
    with c2:
        st.metric("Refresh", f"{config.refresh_seconds}s")

    st.code(config.sts_csv_export_url)

    if st.button("Sync Now"):
        df, result = STSLiveSyncEngine(config).sync()
        info = result.to_dict()

        if result.ok:
            st.success(info["message"])
        else:
            st.warning(info["message"])

        st.json(info)

        if not df.empty:
            st.subheader("STS Preview")
            st.dataframe(df.head(50), use_container_width=True)
        else:
            st.error("No STS data available. Check Google Sheet sharing permission.")
