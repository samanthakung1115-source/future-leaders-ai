
import io
import streamlit as st

from core import Settings
from ranking import RankingCandidateLoader
from services import RankingService


def _load_candidates(uploaded):
    loader = RankingCandidateLoader()
    if uploaded:
        text = uploaded.getvalue().decode("utf-8-sig")
        return loader.load_file(io.StringIO(text))
    return loader.load_path("data/candidates/release_sprint2_candidates.csv")


def render_release_dashboard():
    settings = Settings.load()
    st.title(settings.app_name)
    st.caption(settings.version)

    st.sidebar.header("Future Leaders Ranking")
    uploaded = st.sidebar.file_uploader("Upload ranking candidates CSV", type=["csv"])
    limit = st.sidebar.slider("Top N", 5, 30, settings.default_candidate_limit)

    try:
        candidates = _load_candidates(uploaded)
        ranking = RankingService(settings).build(candidates, limit=limit)
    except Exception as exc:
        st.error(f"Ranking failed: {exc}")
        return

    st.subheader("Future Leaders Ranking Engine v1")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Candidates", len(candidates))
    with c2:
        st.metric("Ranked", ranking["count"])
    with c3:
        top = ranking["top"]["ticker"] if ranking["top"] else "N/A"
        st.metric("Top Candidate", top)

    st.divider()

    for item in ranking["ranked"]:
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.markdown(f"## #{item['rank']}")
                st.metric(item["ticker"], item["total_score"])
            with col2:
                st.markdown(f"### {item['verdict']}")
                st.write(f"**Theme:** {item['theme'] or 'Unclassified'}")
                if item["dna"]:
                    st.write("**DNA:** " + ", ".join(item["dna"]))
                if item["why_selected"]:
                    st.markdown("**Why Samantha selected it**")
                    for reason in item["why_selected"]:
                        st.write(f"- {reason}")
                if item["risks"]:
                    st.markdown("**Risks**")
                    for risk in item["risks"]:
                        st.write(f"- {risk}")
            with col3:
                st.metric("Rank Change", item["change"])
