
from __future__ import annotations

import time
import streamlit as st


def render_auto_refresh_controls(default_seconds: int = 60) -> dict:
    """Render sidebar controls for auto refresh.

    Returns:
        dict with enabled, seconds, last_refresh
    """
    with st.sidebar.expander("🔄 Auto Refresh 自動刷新", expanded=False):
        enabled = st.checkbox("啟用自動刷新", value=False)
        seconds = st.selectbox(
            "刷新間隔",
            options=[30, 60, 120, 300],
            index=[30, 60, 120, 300].index(default_seconds) if default_seconds in [30, 60, 120, 300] else 1,
            format_func=lambda x: f"{x} 秒" if x < 300 else "5 分鐘",
        )
        st.caption("適合 Live Price、Radar、STS Sync。")

    if "last_auto_refresh_ts" not in st.session_state:
        st.session_state["last_auto_refresh_ts"] = time.time()

    return {
        "enabled": enabled,
        "seconds": seconds,
        "last_refresh": st.session_state["last_auto_refresh_ts"],
    }


def apply_auto_refresh(config: dict):
    """Apply auto refresh using Streamlit rerun.

    This avoids extra dependencies like streamlit-autorefresh.
    """
    if not config.get("enabled"):
        return

    seconds = int(config.get("seconds", 60))
    now = time.time()
    last = float(config.get("last_refresh", now))

    remaining = max(0, seconds - int(now - last))
    st.sidebar.caption(f"下次自動刷新：約 {remaining} 秒")

    if now - last >= seconds:
        st.session_state["last_auto_refresh_ts"] = now
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()
