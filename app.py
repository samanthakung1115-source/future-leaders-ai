
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


def _render_fallback_page(title: str, message: str):
    st.title(title)
    st.info(message)


def main():
    st.set_page_config(
        page_title="Samantha AI Platform",
        page_icon="🧠",
        layout="wide",
    )

    st.sidebar.title("Samantha AI")
    page = st.sidebar.radio(
        "Select page",
        [
            "Daily Brief",
            "Unified Brief",
            "Action Plan",
            "STS Live",
            "Project Status",
        ],
    )

    if page == "Daily Brief":
        try:
            from ui.samantha_daily_brief_page import render
            render()
        except Exception as exc:
            _render_fallback_page(
                "Samantha Daily Brief",
                f"Daily Brief page is not available yet: {exc}",
            )

    elif page == "Unified Brief":
        try:
            from ui.unified_brief_page import render
            render()
        except Exception as exc:
            _render_fallback_page(
                "Samantha Unified Brief",
                f"Unified Brief page is not available yet: {exc}",
            )

    elif page == "Action Plan":
        try:
            from ui.action_plan_page import render
            render()
        except Exception as exc:
            _render_fallback_page(
                "Samantha Action Plan",
                f"Action Plan page is not available yet: {exc}",
            )

    elif page == "STS Live":
        try:
            from ui.sts_live_page import render
            render()
        except Exception as exc:
            _render_fallback_page(
                "STS Live Integration",
                f"STS Live page is not available yet: {exc}",
            )

    else:
        st.title("Future Leaders AI v11 Beta 13")
        st.subheader("Project Status")
        st.write("Main App Launcher is active.")
        st.write("Use the sidebar to open Samantha Daily Brief, Unified Brief, Action Plan, or STS Live.")
        st.markdown(
            """
            ### Current development direction

            - Future Leaders AI = Discovery Intelligence
            - STS = Portfolio Intelligence
            - Samantha AI Platform = both working together

            Beta 13 creates one main Streamlit entry point: `app.py`.
            """
        )


if __name__ == "__main__":
    main()
