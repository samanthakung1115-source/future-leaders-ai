
from __future__ import annotations

import streamlit as st


def _safe_import(module_name: str, attr_name: str):
    try:
        module = __import__(module_name, fromlist=[attr_name])
        return getattr(module, attr_name), ""
    except Exception as exc:
        return None, str(exc)


def _status_dot(ok: bool) -> str:
    return "🟢 OK" if ok else "🟡 Check"


def render_v11_control_center():
    """Unified v1.1 Control Center.

    Purpose:
    - One place to run STS Sync
    - One place to view unified live data
    - One place to read Samantha Brief
    - One place to run health check
    """

    st.title("🧠 Future Leaders AI v1.1 Control Center")
    st.caption("Patch 14")

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
    render_checklist, err_checklist = _safe_import(
        "patch_checklist", "render_patch_install_checklist"
    )

    module_status = {
        "Unified Pipeline": build_pipeline is not None,
        "Pipeline Status": render_pipeline_status is not None,
        "Samantha Brief": render_brief is not None,
        "Patch Health": render_health is not None,
        "Install Checklist": render_checklist is not None,
    }

    c1, c2, c3, c4, c5 = st.columns(5)
    cols = [c1, c2, c3, c4, c5]
    for col, (name, ok) in zip(cols, module_status.items()):
        with col:
            st.metric(name, _status_dot(ok))

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔗 Live Pipeline",
        "🧠 Samantha Brief",
        "🧩 Health Check",
        "✅ Install Guide",
    ])

    unified_df = None
    pipeline_status = None

    with tab1:
        st.subheader("STS Google Sheet → Column Mapper → Live Price")

        if build_pipeline:
            enable_live_price = st.checkbox("Enable Live Price", value=True)
            if st.button("Run Unified Pipeline"):
                unified_df, pipeline_status = build_pipeline(enable_live_price=enable_live_price)
                st.session_state["v11_unified_df"] = unified_df
                st.session_state["v11_pipeline_status"] = pipeline_status

            unified_df = st.session_state.get("v11_unified_df")
            pipeline_status = st.session_state.get("v11_pipeline_status")

            if pipeline_status:
                if render_pipeline_status:
                    render_pipeline_status(pipeline_status)
                else:
                    st.json(pipeline_status)

            if unified_df is not None and not unified_df.empty:
                st.dataframe(unified_df, use_container_width=True)
            else:
                st.info("尚未執行 Pipeline，或目前沒有資料。")
        else:
            st.warning(f"Unified Pipeline 尚未安裝：{err_pipeline}")

    with tab2:
        st.subheader("Samantha 今日一句話")

        unified_df = st.session_state.get("v11_unified_df")

        if render_brief:
            if unified_df is not None and not unified_df.empty:
                render_brief(radar_df=unified_df, portfolio_df=unified_df)
            else:
                st.info("請先到 Live Pipeline 執行同步。")
                render_brief()
        else:
            st.warning(f"Samantha Brief 尚未安裝：{err_brief}")

    with tab3:
        st.subheader("Patch Health Check")
        if render_health:
            render_health(".")
        else:
            st.warning(f"Patch Health 尚未安裝：{err_health}")

    with tab4:
        st.subheader("Install Checklist")
        if render_checklist:
            render_checklist()
        else:
            st.warning(f"Install Checklist 尚未安裝：{err_checklist}")

        st.markdown("""
### 建議核心 Patch 順序

1. Patch 02：STS Live Sync
2. Patch 06：STS Column Mapper
3. Patch 09：Live Price Cache
4. Patch 07：Unified Pipeline
5. Patch 05：Samantha Brief
6. Patch 08：Health Check
7. Patch 10：Install Checklist
8. Patch 14：Control Center
""")
