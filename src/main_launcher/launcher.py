
from __future__ import annotations

import importlib
import streamlit as st


def safe_import(module_name: str, attr_name: str = "render"):
    """Safely import a render function from an optional page/module."""
    try:
        module = importlib.import_module(module_name)
        return getattr(module, attr_name), ""
    except Exception as exc:
        return None, str(exc)


def safe_page(title: str, module_name: str, attr_name: str = "render"):
    """Render a page safely. Missing pages show warning instead of crashing."""
    render_func, err = safe_import(module_name, attr_name)
    if render_func:
        render_func()
    else:
        st.title(title)
        st.warning(f"此頁面尚未正確安裝或 import 失敗：{module_name}.{attr_name}")
        st.caption(err)


def render_home():
    st.title("Future Leaders AI")
    st.caption("v1.2 Main Launcher RC")

    st.markdown("""
### 今日入口

這個版本修復目前 `app.py` 只剩 STS Sync 頁面的問題。

左側選單可以切換：

- Dashboard
- STS Live Sync
- v1.1 Control Center
- v1.1 Patch Launcher
- Patch Health Check
- Install Checklist
- Settings / About

如果某個模組尚未安裝，App 會顯示 warning，不會整個掛掉。
""")

    with st.container(border=True):
        st.markdown("### 建議工作流")
        st.write("1. 先進 STS Live Sync，確認 Google Sheet 同步成功。")
        st.write("2. 再進 v1.1 Control Center，確認 Unified Pipeline 有資料。")
        st.write("3. 看 Samantha Brief 今日提醒。")
        st.write("4. 用 Patch Health Check 檢查缺件與 __pycache__。")


def render_about():
    st.title("About")
    st.markdown("""
## Future Leaders AI v1.2 Main Launcher RC

目的：

- 統一主入口
- 修復 app.py 被單頁覆蓋的問題
- 保留既有 Patch 模組
- 缺少模組時安全降級
- 為 v1.2 正式重構做準備

### 下一步

v1.2 Final 應該把 Patch 01～14 中穩定的模組正式整併到核心目錄，而不是長期維持 Patch 狀態。
""")


def render_main_launcher():
    st.sidebar.title("Future Leaders AI")
    st.sidebar.caption("v1.2 Main Launcher RC")

    page = st.sidebar.radio(
        "功能",
        [
            "Home",
            "Dashboard",
            "STS Live Sync",
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
        # Try existing dashboard modules in common order
        candidates = [
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
