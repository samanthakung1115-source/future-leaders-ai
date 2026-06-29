
import io
import streamlit as st

from product import CandidateCSVLoader, UnifiedBriefService
from sts_live import STSLiveReader


def _load_candidates(uploaded):
    if uploaded:
        text = uploaded.getvalue().decode("utf-8-sig")
        return CandidateCSVLoader().load_file(io.StringIO(text))
    return CandidateCSVLoader().load_path("data/samples/beta11_candidates.csv")


def _load_positions(uploaded):
    if uploaded:
        text = uploaded.getvalue().decode("utf-8-sig")
        return STSLiveReader().load_file(io.StringIO(text))
    return STSLiveReader().load_path("data/samples/beta11_sts.csv")


def render():
    st.title("Samantha Unified Brief")
    st.caption("Future Leaders AI v11 Beta 11")

    col1, col2 = st.columns(2)
    with col1:
        candidate_file = st.file_uploader("Upload Future Leaders CSV", type=["csv"])
    with col2:
        sts_file = st.file_uploader("Upload STS CSV", type=["csv"])

    limit = st.slider("Candidates to show", 3, 20, 10)

    try:
        candidates = _load_candidates(candidate_file)
        positions = _load_positions(sts_file)
    except Exception as exc:
        st.error(f"Could not load data: {exc}")
        return

    brief = UnifiedBriefService().build(candidates, positions, limit=limit)

    st.subheader(brief["summary"])
    st.write(brief["samantha_comment"])

    st.divider()
    st.subheader("Future Leaders + Portfolio Context")

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

    if brief["portfolio_warnings"]:
        st.divider()
        st.subheader("Portfolio Warnings")
        for warning in brief["portfolio_warnings"]:
            st.warning(warning)
