
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import streamlit as st
from export_center import ReportExporter

st.set_page_config(page_title="Future Leaders AI v1.0 Release Sprint 5", layout="wide")

st.title("Daily Report & Export Center")
st.caption("Future Leaders AI v1.0 Release - Sprint 5")

sample = {
    "title": "Samantha Daily Report",
    "generated_at": "2026-06-29 09:00",
    "market_summary": [
        "AI Infrastructure: Strong",
        "Semiconductors: Watch",
        "Cloud: Stable",
    ],
    "future_leaders": [
        "RKLB — Future Leader",
        "TEM — High Potential",
        "MRVL — Watch",
    ],
    "portfolio_review": [
        "SOFI under pressure: review thesis before adding",
        "MRVL strong winner: review hold / trim plan",
    ],
    "decision_coach": [
        "Do not chase extended leaders",
        "Avoid averaging down without fresh thesis confirmation",
    ],
    "action_plan": [
        "Research TEM",
        "Hold RKLB",
        "Review SOFI",
    ],
}

exporter = ReportExporter()
report = exporter.build_report(sample)

st.subheader("Report Preview")
st.json(report)

md = exporter.to_markdown(report)
html = exporter.to_html(report)
js = exporter.to_json(report)

c1, c2, c3 = st.columns(3)
with c1:
    st.download_button("Download Markdown", md, file_name="samantha_daily_report.md", mime="text/markdown")
with c2:
    st.download_button("Download HTML", html, file_name="samantha_daily_report.html", mime="text/html")
with c3:
    st.download_button("Download JSON", js, file_name="samantha_daily_report.json", mime="application/json")
