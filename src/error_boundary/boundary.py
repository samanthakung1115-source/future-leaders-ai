
from __future__ import annotations

from contextlib import contextmanager
import traceback

try:
    import streamlit as st
except Exception:
    class _DummyExpander:
        def __enter__(self): return self
        def __exit__(self, *args): return False

    class _DummyStreamlit:
        def error(self, *args, **kwargs): pass
        def title(self, *args, **kwargs): pass
        def code(self, *args, **kwargs): pass
        def expander(self, *args, **kwargs): return _DummyExpander()

    st = _DummyStreamlit()

try:
    from app_logging import log_error, log_event
except Exception:
    def log_error(*args, **kwargs):
        return None
    def log_event(*args, **kwargs):
        return None


@contextmanager
def error_boundary(title: str = "Section"):
    """Context manager that catches Streamlit section errors."""
    try:
        log_event("section_start", section=title)
        yield
        log_event("section_complete", section=title)
    except Exception as exc:
        log_error("section_failed", error=exc, section=title)
        st.error(f"{title} 發生錯誤，但 App 仍可繼續使用。")
        with st.expander("錯誤詳情"):
            st.code(traceback.format_exc())


def safe_render(render_func, title: str = "Page", *args, **kwargs):
    """Safely render any function."""
    try:
        log_event("page_start", page=title)
        return render_func(*args, **kwargs)
    except Exception as exc:
        log_error("page_failed", error=exc, page=title)
        st.title(title)
        st.error("此頁面發生錯誤，但主程式沒有中斷。")
        with st.expander("錯誤詳情"):
            st.code(traceback.format_exc())
        return None
