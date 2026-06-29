
from __future__ import annotations

import streamlit as st


def _safe_import(module_name: str, attr_name: str):
    try:
        module = __import__(module_name, fromlist=[attr_name])
        return getattr(module, attr_name), ""
    except Exception as exc:
        return None, str(exc)


def render_v11_patch_panel():
    """Unified panel for installed v1.1 patches.

    This shell tries to call installed patch modules safely.
    Missing modules will show warnings instead of crashing the app.
    """

    st.subheader("🧠 Future Leaders AI v1.1 Patch Panel")

    build_pipeline, err_pipeline = _safe_import(
        "unified_pipeline", "build_unified_sts_live_pipeline"
    )
    render_pipeline_status, err_status = _safe_import(
        "unified_pipeline", "render_unified_pipeline_status"
    )
    render_brief, err_brief = _safe_import(
        "samantha_brief", "render_samantha_brief"
    )
    render_health, err_health = _safe_import(
        "patch_health", "render_patch_health_check"
    )

    unified_df = None

    with st.container(border=True):
        st.markdown("### 🔗 Unified STS + Live Price")

        if build_pipeline:
            unified_df, pipeline_status = build_pipeline(enable_live_price=True)
            if render_pipeline_status:
                render_pipeline_status(pipeline_status)
            else:
                st.json(pipeline_status)

            if unified_df is not None and not unified_df.empty:
                st.dataframe(unified_df.head(50), use_container_width=True)
            else:
                st.warning("Unified pipeline returned no data.")
        else:
            st.warning(f"Unified Pipeline not installed: {err_pipeline}")

    with st.container(border=True):
        st.markdown("### 🧠 Samantha 今日一句話")

        if render_brief and unified_df is not None:
            render_brief(radar_df=unified_df, portfolio_df=unified_df)
        elif not render_brief:
            st.warning(f"Samantha Brief Patch not installed: {err_brief}")
        else:
            st.info("No unified data available yet.")

    with st.expander("🧩 Patch Health Check"):
        if render_health:
            render_health(".")
        else:
            st.warning(f"Patch Health Check not installed: {err_health}")
