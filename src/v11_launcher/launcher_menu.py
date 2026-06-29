
from __future__ import annotations

import streamlit as st


def _safe_import(module_name: str, attr_name: str):
    try:
        module = __import__(module_name, fromlist=[attr_name])
        return getattr(module, attr_name), ""
    except Exception as exc:
        return None, str(exc)


def render_v11_launcher_menu():
    """Render a small launcher menu for v1.1 patch tools.

    This does not replace your existing app navigation.
    It gives you one controlled place to open v1.1 patch functions.
    """

    st.title("Future Leaders AI v1.1 Patch Launcher")
    st.caption("Patch 13")

    page = st.radio(
        "選擇功能",
        [
            "Unified Pipeline",
            "Samantha Brief",
            "Patch Health",
            "Install Checklist",
            "About v1.1",
        ],
        horizontal=True,
    )

    if page == "Unified Pipeline":
        build_pipeline, err1 = _safe_import("unified_pipeline", "build_unified_sts_live_pipeline")
        render_status, err2 = _safe_import("unified_pipeline", "render_unified_pipeline_status")

        st.subheader("🔗 Unified STS + Live Price Pipeline")
        if not build_pipeline:
            st.warning(f"Unified Pipeline 尚未安裝：{err1}")
            return

        df, status = build_pipeline(enable_live_price=True)

        if render_status:
            render_status(status)
        else:
            st.json(status)

        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("目前沒有同步資料。")

    elif page == "Samantha Brief":
        build_pipeline, err1 = _safe_import("unified_pipeline", "build_unified_sts_live_pipeline")
        render_brief, err2 = _safe_import("samantha_brief", "render_samantha_brief")

        st.subheader("🧠 Samantha 今日一句話")
        if not render_brief:
            st.warning(f"Samantha Brief 尚未安裝：{err2}")
            return

        if build_pipeline:
            df, _status = build_pipeline(enable_live_price=True)
            render_brief(radar_df=df, portfolio_df=df)
        else:
            st.warning(f"Unified Pipeline 尚未安裝：{err1}")
            render_brief()

    elif page == "Patch Health":
        render_health, err = _safe_import("patch_health", "render_patch_health_check")
        st.subheader("🧩 Patch Health")
        if render_health:
            render_health(".")
        else:
            st.warning(f"Patch Health 尚未安裝：{err}")

    elif page == "Install Checklist":
        render_checklist, err = _safe_import("patch_checklist", "render_patch_install_checklist")
        st.subheader("✅ Install Checklist")
        if render_checklist:
            render_checklist()
        else:
            st.warning(f"Install Checklist 尚未安裝：{err}")

    else:
        st.subheader("About v1.1 Patch System")
        st.write("v1.1 之後採用 Patch 模式，不再覆蓋整個專案。")
        st.write("核心方向：STS Google Sheet → Column Mapper → Live Price → Unified Pipeline → Samantha Brief")
        st.markdown("""
        ### 建議安裝核心 Patch

        - Patch 02 STS Live Sync
        - Patch 06 STS Column Mapper
        - Patch 09 Live Price Cache
        - Patch 07 Unified Pipeline
        - Patch 05 Samantha Brief
        - Patch 08 Health Check
        - Patch 10 Install Checklist
        """)
