
import streamlit as st

from product import DailyBriefService


SAMPLE_CANDIDATES = [
    {
        "ticker": "TEM",
        "score": 82,
        "why_selected": [
            "AI healthcare platform",
            "Matches Platform DNA",
            "Early-stage Future Leader candidate"
        ],
        "risks": [
            "Profitability not fully verified",
            "Valuation premium"
        ],
    },
    {
        "ticker": "SOFI",
        "score": 68,
        "why_selected": [
            "FinTech platform",
            "Member growth",
            "Operating leverage improving"
        ],
        "risks": [
            "Credit risk",
            "Still under verification"
        ],
    },
    {
        "ticker": "MRVL",
        "score": 76,
        "why_selected": [
            "AI infrastructure",
            "Custom silicon",
            "Networking exposure"
        ],
        "risks": [
            "High volatility",
            "Profit-taking discipline required"
        ],
    },
]

SAMPLE_PORTFOLIO = {
    "SOFI": "Existing holding. Under verification; avoid averaging down without thesis confirmation.",
    "MRVL": "Existing holding. Remember prior no-profit-taking lesson.",
}


def render():
    st.title("Samantha Daily Brief")
    st.caption("Future Leaders AI v11 Beta 7")

    service = DailyBriefService()
    brief = service.build(SAMPLE_CANDIDATES, portfolio=SAMPLE_PORTFOLIO)

    st.subheader(brief["summary"])
    st.write(brief["samantha_comment"])

    st.divider()

    for item in brief["top_future_leaders"]:
        with st.container(border=True):
            st.markdown(f"### {item['ticker']} — {item['verdict']}")
            st.metric("AI Score", item["score"])

            st.markdown("**Why Samantha selected it**")
            for reason in item["why_selected"]:
                st.write(f"- {reason}")

            st.markdown("**Risks**")
            for risk in item["risks"]:
                st.write(f"- {risk}")

            st.markdown("**Portfolio context**")
            st.info(item["portfolio_context"])

    if brief["portfolio_reminders"]:
        st.divider()
        st.subheader("Portfolio Reminders")
        for reminder in brief["portfolio_reminders"]:
            st.warning(reminder)
