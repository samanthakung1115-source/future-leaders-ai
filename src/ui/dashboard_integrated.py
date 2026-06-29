
from __future__ import annotations

import streamlit as st


def _safe_import(module_name: str, attr_name: str):
    try:
        module = __import__(module_name, fromlist=[attr_name])
        return getattr(module, attr_name), ""
    except Exception as exc:
        return None, str(exc)


def _metric_card(label: str, value, help_text: str = ""):
    with st.container(border=True):
        st.metric(label, value)
        if help_text:
            st.caption(help_text)


def render_dashboard():
    """Integrated Dashboard for v1.2 RC.

    This page connects existing v1.1/v1.2 modules:
    - Unified Pipeline
    - Samantha Brief
    - Patch Health
    - STS / Live Price status

    It is safe: missing modules show warnings instead of crashing.
    """
    st.title("🏠 Future Leaders AI Dashboard")
    st.caption("v1.2 RC Integration 1")

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

    st.subheader("🧠 今日 AI 摘要")

    unified_df = None
    pipeline_status = None

    if build_pipeline:
        with st.spinner("同步 STS + Live Price..."):
            unified_df, pipeline_status = build_pipeline(enable_live_price=True)

        if render_brief:
            render_brief(radar_df=unified_df, portfolio_df=unified_df)
        else:
            st.warning(f"Samantha Brief 尚未安裝：{err_brief}")
    else:
        st.warning(f"Unified Pipeline 尚未安裝：{err_pipeline}")
        st.info("請先確認 Patch 02 / 06 / 07 / 09 是否已上傳。")

    st.divider()
    st.subheader("📊 系統狀態")

    c1, c2, c3, c4 = st.columns(4)
    rows = len(unified_df) if unified_df is not None else 0
    sync_ok = bool(pipeline_status and pipeline_status.get("sync_ok"))
    mapper_ok = bool(pipeline_status and pipeline_status.get("mapper_ok"))
    live_ok = bool(pipeline_status and pipeline_status.get("live_price_ok"))

    with c1:
        _metric_card("STS Rows", rows, "Google Sheet 同步列數")
    with c2:
        _metric_card("STS Sync", "OK" if sync_ok else "Check")
    with c3:
        _metric_card("Column Mapper", "OK" if mapper_ok else "Check")
    with c4:
        _metric_card("Live Price", "OK" if live_ok else "Check")

    if pipeline_status:
        with st.expander("Pipeline Status"):
            if render_pipeline_status:
                render_pipeline_status(pipeline_status)
            else:
                st.json(pipeline_status)

    st.divider()
    st.subheader("💹 Live Portfolio / Radar Preview")

    if unified_df is not None and not unified_df.empty:
        # show useful columns first if available
        preferred = [
            "ticker",
            "shares",
            "return_pct",
            "distance_from_high_pct",
            "ai_score",
            "tonight_action",
            "Live Price 最新價",
            "Live % 今日%",
            "Dist High % 距前高%",
            "Live Action 即時行動",
        ]
        cols = [c for c in preferred if c in unified_df.columns]
        if cols:
            st.dataframe(unified_df[cols].head(100), use_container_width=True)
        else:
            st.dataframe(unified_df.head(100), use_container_width=True)
    else:
        st.info("目前沒有 unified_df 資料。請先檢查 STS Live Sync。")

    st.divider()
    st.subheader("🧩 Patch Health")

    with st.expander("Run Patch Health Check"):
        if render_health:
            render_health(".")
        else:
            st.warning(f"Patch Health 尚未安裝：{err_health}")
