
from __future__ import annotations

import importlib
import streamlit as st


def safe_import(module_name: str, attr_name: str = "render"):
    try:
        module = importlib.import_module(module_name)
        return getattr(module, attr_name), ""
    except Exception as exc:
        return None, str(exc)


def safe_page(title: str, module_name: str, attr_name: str = "render"):
    render_func, err = safe_import(module_name, attr_name)
    if render_func:
        render_func()
    else:
        st.title(title)
        st.warning(f"此頁面尚未正確安裝或 import 失敗：{module_name}.{attr_name}")
        st.caption(err)


def render_home():
    st.title("Future Leaders AI")
    st.caption("Sprint 3.4 Market Scanner + AI Memory")

    st.markdown("""
## 今日入口

這版把 **Market Scanner 海選引擎** 接上 **AI Memory**。

核心功能：

- Market Scanner 海選 Top N
- Leader Score
- Black Horse
- AI Memory 分數歷史
- Score Change 分數變化
- Top Movers
""")

    with st.container(border=True):
        st.markdown("### 建議工作流")
        st.write("1. 進 Market Scanner。")
        st.write("2. Run Scanner。")
        st.write("3. 勾選 Save to AI Memory。")
        st.write("4. 第二次之後會看到 Score Change。")


def render_about():
    st.title("About")
    st.markdown("""
## Future Leaders AI Sprint 3.4

本版重點：

- 海選引擎接上 AI Memory
- 記錄每檔股票 Leader Score 歷史
- 找出分數上升最快的股票

下一步：

- Sprint 3.5：Dashboard 顯示 Tonight Future Leaders
- Sprint 3.6：Narrative Engine
""")


def render_main_launcher():
    st.sidebar.title("Future Leaders AI")
    st.sidebar.caption("Sprint 3.4")

    page = st.sidebar.radio(
        "功能",
        [
            "Home",
            "Dashboard",
            "Market Scanner",
            "AI Memory",
            "STS Live Sync",
            "Portfolio Center",
            "v1.1 Control Center",
            "v1.1 Patch Launcher",
            "Patch Health Check",
            "Install Checklist",
            "Settings / About",
        ],
    )

    if page == "Home":
        render_home()

    elif page == "Dashboard":
        candidates = [
            ("ui.dashboard_integrated", "render_dashboard"),
            ("ui.dashboard", "render_dashboard"),
            ("ui.release_dashboard", "render_release_dashboard"),
            ("ui.main_dashboard", "render"),
        ]
        for module, attr in candidates:
            func, err = safe_import(module, attr)
            if func:
                func()
                return
        st.title("Dashboard")
        st.warning("找不到既有 Dashboard render function。")
        st.caption("可先用 Market Scanner 查看海選結果。")

    elif page == "Market Scanner":
        safe_page("Market Scanner", "ui.market_scanner_page", "render")

    elif page == "AI Memory":
        safe_page("AI Memory", "ui.ai_memory_page", "render")

    elif page == "STS Live Sync":
        safe_page("STS Live Sync", "ui.sts_sync_page", "render")

    elif page == "Portfolio Center":
        safe_page("Portfolio Center", "ui.portfolio_center_integrated", "render")

    elif page == "v1.1 Control Center":
        safe_page("v1.1 Control Center", "v11_control_center", "render_v11_control_center")

    elif page == "v1.1 Patch Launcher":
        safe_page("v1.1 Patch Launcher", "v11_launcher", "render_v11_launcher_menu")

    elif page == "Patch Health Check":
        safe_page("Patch Health Check", "patch_health", "render_patch_health_check")

    elif page == "Install Checklist":
        safe_page("Install Checklist", "patch_checklist", "render_patch_install_checklist")

    else:
        render_about()
