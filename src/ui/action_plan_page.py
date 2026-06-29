
import io
import streamlit as st

from action_plan import ActionPlanEngine
from product import CandidateCSVLoader, UnifiedBriefService
from sts_live import STSLiveReader


def _load_candidates(uploaded):
    if uploaded:
        return CandidateCSVLoader().load_file(io.StringIO(uploaded.getvalue().decode("utf-8-sig")))
    return CandidateCSVLoader().load_path("data/samples/beta12_candidates.csv")


def _load_positions(uploaded):
    if uploaded:
        return STSLiveReader().load_file(io.StringIO(uploaded.getvalue().decode("utf-8-sig")))
    return STSLiveReader().load_path("data/samples/beta12_sts.csv")


def render():
    st.title("Samantha Action Plan")
    st.caption("Future Leaders AI v11 Beta 12")

    c1, c2 = st.columns(2)
    with c1:
        candidate_file = st.file_uploader("Upload Future Leaders CSV", type=["csv"])
    with c2:
        sts_file = st.file_uploader("Upload STS CSV", type=["csv"])

    candidates = _load_candidates(candidate_file)
    positions = _load_positions(sts_file)

    brief = UnifiedBriefService().build(candidates, positions)
    action_items = ActionPlanEngine().build(brief)

    st.subheader(brief["summary"])
    st.write(brief["samantha_comment"])

    st.divider()
    st.subheader("Action Plan")

    for item in action_items:
        with st.container(border=True):
            st.markdown(f"### {item.ticker} — {item.action}")
            st.write(f"**Priority:** {item.priority}")
            st.write(f"**Reason:** {item.reason}")
            st.write(f"**Risk note:** {item.risk_note}")
