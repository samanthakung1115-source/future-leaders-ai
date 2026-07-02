
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
    st.caption("Sprint 3.3 Market Scanner Auto-Install")

    st.markdown("""
## 今日入口

這版正式把 **Market Scanner 海選引擎** 加進主選單。

左側選單可以切換：

- Dashboard
- Market Scanner
- STS Live Sync
- Portfolio Center
- v1.1 Control Center
- Patch Health Check

核心目標：

> 從候選股清單中海選出 Future Leaders Top N 與 Black Horse。
""")

    with st.container(border=True):
        st.markdown("### 建議工作流")
        st.write("1. 先進 Market Scanner。")
        st.write("2. 上傳候選股 CSV，或先用內建 sample。")
        st.write("3. 點 Run Scanner，查看 Top N 與 Black Horse。")
        st.write("4. 後續會接入 AI Memory，追蹤分數變化。")


def render_about():
    st.title("About")
    st.markdown("""
## Future Leaders AI Sprint 3.3

本版重點：

- Market Scanner 接入主選單
- Leader Score
- Role Classification
- Black Horse
- Top N Ranking

下一步：

- Sprint 3.4：Market Scanner + AI Memory
- Sprint 3.5：Dashboard 顯示 Tonight Future Leaders
""")


def render_main_launcher():
    st.sidebar.title("Future Leaders AI")
    st.sidebar.caption("Sprint 3.3")

    page = st.sidebar.radio(
        "功能",
        [
            "Home",
            "Dashboard",
            "Market Scanner",
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
        st.caption("可用 Market Scanner 先查看海選結果。")

    elif page == "Market Scanner":
        safe_page("Market Scanner", "ui.market_scanner_page", "render")

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
