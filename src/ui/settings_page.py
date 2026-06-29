
import streamlit as st

from config import SamanthaSettings


def render():
    st.title("Samantha Settings")
    settings = SamanthaSettings.load()

    st.subheader("App")
    st.write(f"**Name:** {settings.app_name}")
    st.write(f"**Version:** {settings.version}")
    st.write(f"**Default candidate limit:** {settings.default_candidate_limit}")

    st.subheader("Score Thresholds")
    st.json(settings.score_thresholds)

    st.subheader("Portfolio Rules")
    st.json(settings.portfolio_rules)
