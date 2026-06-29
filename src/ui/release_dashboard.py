
import streamlit as st

from core import Settings
from services import ReleaseDashboardService


def _render_status(status: dict):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Version", status["version"])
    with c2:
        st.metric("Channel", status["channel"])
    with c3:
        st.metric("Status", status["status"])

    st.info(f"Next focus: {status['next_focus']}")


def _render_section(section: dict):
    with st.container(border=True):
        st.markdown(f"### {section['title']}")
        st.caption(section["subtitle"])
        st.write(f"**Status:** {section['status']}")
        for item in section["items"]:
            st.write(f"- {item}")


def render_release_dashboard():
    settings = Settings.load()
    service = ReleaseDashboardService(settings)

    st.title(settings.app_name)
    st.caption("Future Leaders AI v1.0 Release")

    st.subheader("Release Dashboard")
    _render_status(service.status().to_dict())

    st.divider()
    st.subheader("Product Modules")

    sections = [section.to_dict() for section in service.sections()]
    for i in range(0, len(sections), 2):
        cols = st.columns(2)
        for col, section in zip(cols, sections[i:i + 2]):
            with col:
                _render_section(section)

    st.divider()
    st.subheader("Release Sprint Roadmap")
    st.write("1. Sprint 1 — Formal dashboard shell")
    st.write("2. Sprint 2 — Future Leaders Ranking Engine v1")
    st.write("3. Sprint 3 — STS Portfolio deep integration")
    st.write("4. Sprint 4 — Decision Coach 2.0")
    st.write("5. Sprint 5 — Daily Report & Export Center")
    st.write("6. Sprint 6 — News Watch architecture")
    st.write("7. Final — v1.0 Release package")
