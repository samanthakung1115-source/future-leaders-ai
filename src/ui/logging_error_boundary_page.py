
import streamlit as st

from app_logging import log_event
from error_boundary import error_boundary, safe_render


def _demo_success():
    st.success("正常區塊執行成功。")


def _demo_error():
    raise RuntimeError("這是測試錯誤，用來確認 Error Boundary 是否正常。")


def render():
    st.title("Logging + Error Boundary")
    st.caption("Future Leaders AI v1.2 RC Sprint 4")

    st.subheader("Logging")
    if st.button("Write test log"):
        log_event("manual_test_log", source="ui")
        st.success("已寫入測試 log。")

    st.divider()
    st.subheader("Error Boundary Demo")

    with error_boundary("成功區塊"):
        _demo_success()

    if st.button("Run error demo"):
        safe_render(_demo_error, title="錯誤測試頁")
