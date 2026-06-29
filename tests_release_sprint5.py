
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from export_center import ReportExporter


def test_report_exporter():
    exporter = ReportExporter()
    report = exporter.build_report({
        "title": "Samantha Daily Report",
        "market_summary": ["AI strong"],
        "future_leaders": ["RKLB"],
        "portfolio_review": ["SOFI under pressure"],
        "decision_coach": ["Do not chase"],
        "action_plan": ["Research TEM"],
        "generated_at": "2026-06-29 09:00",
    })

    md = exporter.to_markdown(report)
    js = exporter.to_json(report)
    html = exporter.to_html(report)

    assert "# Samantha Daily Report" in md
    assert "RKLB" in md
    assert '"future_leaders"' in js
    assert "<html>" in html


if __name__ == "__main__":
    test_report_exporter()
    print("Future Leaders AI v1.0 Release Sprint 5 test passed.")
