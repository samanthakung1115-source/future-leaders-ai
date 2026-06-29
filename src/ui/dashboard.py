
import io
import streamlit as st
from core import Settings
from discovery import CandidateLoader
from portfolio import PortfolioLoader
from decision import DecisionMemoryLoader
from services import BriefService, MarkdownReportBuilder
from validation import CandidateCSVValidator, PortfolioCSVValidator

def _validate_uploaded(uploaded, validator, label: str):
    if uploaded is None:
        return {"ok": True, "source": "sample", "message": f"Using sample {label} data."}
    text = uploaded.getvalue().decode("utf-8-sig")
    result = validator.validate_file(io.StringIO(text))
    return {"ok": result.ok, "source": "uploaded", "label": label, "validation": result.to_dict()}

def _load_candidates(uploaded):
    if uploaded:
        return CandidateLoader().load_file(io.StringIO(uploaded.getvalue().decode("utf-8-sig")))
    return CandidateLoader().load_path("data/candidates/sample_candidates.csv")

def _load_positions(uploaded):
    if uploaded:
        return PortfolioLoader().load_file(io.StringIO(uploaded.getvalue().decode("utf-8-sig")))
    return PortfolioLoader().load_path("data/portfolio/sample_portfolio.csv")

def _load_decision_memory():
    return DecisionMemoryLoader().load_path("data/decision_memory/patterns.csv")

def _status_card(title, value, help_text=""):
    with st.container(border=True):
        st.metric(title, value)
        if help_text:
            st.caption(help_text)

def render_dashboard():
    settings = Settings.load()
    st.title(settings.app_name)
    st.caption(settings.version)

    st.sidebar.header("Data Upload")
    candidate_file = st.sidebar.file_uploader("Future Leaders CSV", type=["csv"])
    portfolio_file = st.sidebar.file_uploader("STS Portfolio CSV", type=["csv"])

    candidate_health = _validate_uploaded(candidate_file, CandidateCSVValidator(), "candidate")
    portfolio_health = _validate_uploaded(portfolio_file, PortfolioCSVValidator(), "portfolio")
    data_health = {"ok": candidate_health.get("ok", True) and portfolio_health.get("ok", True), "candidate": candidate_health, "portfolio": portfolio_health}

    if not candidate_health["ok"]:
        st.error(f"Future Leaders CSV invalid: {candidate_health['validation']['missing_columns']}")
        st.stop()
    if not portfolio_health["ok"]:
        st.error(f"STS Portfolio CSV invalid: {portfolio_health['validation']['missing_columns']}")
        st.stop()

    try:
        candidates = _load_candidates(candidate_file)
        positions = _load_positions(portfolio_file)
        decision_patterns = _load_decision_memory()
    except Exception as exc:
        st.error(f"Data loading failed: {exc}")
        return

    brief = BriefService(settings).build(candidates, positions, decision_patterns=decision_patterns, data_health=data_health).to_dict()
    report_md = MarkdownReportBuilder().build(brief)

    c1, c2, c3, c4 = st.columns(4)
    with c1: _status_card("Candidates", len(candidates), "Future Leaders inputs")
    with c2: _status_card("Portfolio Positions", len(positions), "STS inputs")
    with c3: _status_card("Research Cards", len(brief["research_cards"]), "Explainable analysis")
    with c4: _status_card("Coach Notes", len(brief["decision_coach"]), "Decision patterns")

    st.subheader(brief["summary"])
    st.write(brief["samantha_comment"])

    st.download_button(
        label="Download Daily Brief Markdown",
        data=report_md,
        file_name=settings.exports.get("default_filename", "samantha_daily_brief.md"),
        mime="text/markdown",
    )

    if brief["decision_coach"]:
        st.divider()
        st.subheader("Decision Coach")
        for note in brief["decision_coach"]:
            st.warning(f"{note['ticker']} — {note['pattern']}: {note['lesson']}")

    with st.expander("Data Health"):
        st.json(brief["data_health"])

    st.divider()
    st.subheader("Research Cards")
    for card in brief["research_cards"]:
        with st.container(border=True):
            st.markdown(f"### {card['ticker']} — {card['verdict']}")
            st.metric("AI Score", card["score"])
            st.write(f"**Theme:** {card['theme']}")
            st.write(f"**Confidence:** {card['confidence']}")
            if card["dna"]:
                st.write("**DNA:** " + ", ".join(card["dna"]))
            st.markdown("**Why Samantha selected it**")
            for reason in card["why_selected"]:
                st.write(f"- {reason}")
            st.markdown("**Risks**")
            for risk in card["risks"]:
                st.write(f"- {risk}")
            st.markdown("**Portfolio Context**")
            st.info(card["portfolio_context"])
            if card["coach_notes"]:
                st.markdown("**Coach Notes**")
                for note in card["coach_notes"]:
                    st.warning(f"{note.get('pattern')}: {note.get('lesson')}")

    st.divider()
    st.subheader("Action Plan")
    for action in brief["action_plan"]:
        st.write(f"**{action['ticker']}** — {action['action']} ({action['priority']})")
        st.caption(action["reason"])
        if action.get("coach_note"):
            st.caption("Coach: " + action["coach_note"])

    if brief["portfolio_warnings"]:
        st.divider()
        st.subheader("Portfolio Warnings")
        for warning in brief["portfolio_warnings"]:
            st.warning(warning)
