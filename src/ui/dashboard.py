
import io
import streamlit as st

from core import Settings
from discovery import CandidateLoader
from portfolio import PortfolioLoader
from services import BriefService


def _load_candidates(uploaded):
    if uploaded:
        return CandidateLoader().load_file(io.StringIO(uploaded.getvalue().decode("utf-8-sig")))
    return CandidateLoader().load_path("data/candidates/sample_candidates.csv")


def _load_positions(uploaded):
    if uploaded:
        return PortfolioLoader().load_file(io.StringIO(uploaded.getvalue().decode("utf-8-sig")))
    return PortfolioLoader().load_path("data/portfolio/sample_portfolio.csv")


def render_dashboard():
    settings = Settings.load()

    st.title(settings.app_name)
    st.caption(settings.version)

    st.sidebar.header("Data Upload")
    candidate_file = st.sidebar.file_uploader("Future Leaders CSV", type=["csv"])
    portfolio_file = st.sidebar.file_uploader("STS Portfolio CSV", type=["csv"])

    try:
        candidates = _load_candidates(candidate_file)
        positions = _load_positions(portfolio_file)
    except Exception as exc:
        st.error(f"Data loading failed: {exc}")
        return

    brief = BriefService(settings).build(candidates, positions).to_dict()

    st.subheader(brief["summary"])
    st.write(brief["samantha_comment"])

    st.divider()
    st.subheader("Future Leaders")

    for item in brief["future_leaders"]:
        with st.container(border=True):
            st.markdown(f"### {item['ticker']} — {item['verdict']}")
            st.metric("AI Score", item["score"])
            st.markdown("**Why Samantha selected it**")
            for reason in item["why_selected"]:
                st.write(f"- {reason}")
            st.markdown("**Risks**")
            for risk in item["risks"]:
                st.write(f"- {risk}")
            st.markdown("**Portfolio Context**")
            if item["is_holding"]:
                st.warning(item["portfolio_context"])
            else:
                st.info(item["portfolio_context"])

    st.divider()
    st.subheader("Action Plan")
    for action in brief["action_plan"]:
        st.write(f"**{action['ticker']}** — {action['action']} ({action['priority']})")
        st.caption(action["reason"])

    if brief["portfolio_warnings"]:
        st.divider()
        st.subheader("Portfolio Warnings")
        for warning in brief["portfolio_warnings"]:
            st.warning(warning)
