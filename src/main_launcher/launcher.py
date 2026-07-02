
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
    st.caption("v1.2 RC Integration 2.1")
    st.markdown("""
## 今日入口

這版已把 **Portfolio Center** 正式接進主選單。

左側選單可以切換：

- Dashboard
- STS Live Sync
- Portfolio Center
- v1.1 Control Center
- v1.1 Patch Launcher
- Patch Health Check
- Install Checklist
- Settings / About
""")
    with st.container(border=True):
        st.markdown("### 建議工作流")
        st.write("1. 先進 STS Live Sync，確認 Google Sheet 同步成功。")
        st.write("2. 再進 Portfolio Center，按「同步 Portfolio」。")
        st.write("3. 查看 Strong Winners / Under Pressure / Live Action Watch。")
        st.write("4. 再到 Dashboard 看整合摘要。")


def render_about():
    st.title("About")
    st.markdown("""
## Future Leaders AI v1.2 RC Integration 2.1

目的：

- 統一主入口
- 接入 Portfolio Center
- 保留既有 Patch 模組
- 缺少模組時安全降級
- 為 v1.2 RC Final 做準備
""")


def render_main_launcher():
    st.sidebar.title("Future Leaders AI")
    st.sidebar.caption("v1.2 RC Integration 2.1")

    page = st.sidebar.radio(
        "功能",
        [
            "Home",
            "Dashboard",
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
        st.caption("可用 v1.1 Control Center 作為暫時入口。")

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
