
from __future__ import annotations

import json
from datetime import datetime


class ReportExporter:
    """Export Samantha Daily Report to Markdown, HTML, and JSON."""

    def build_report(self, data: dict) -> dict:
        generated_at = data.get("generated_at") or datetime.now().strftime("%Y-%m-%d %H:%M")
        report = {
            "title": data.get("title", "Samantha Daily Report"),
            "generated_at": generated_at,
            "market_summary": data.get("market_summary", []),
            "future_leaders": data.get("future_leaders", []),
            "portfolio_review": data.get("portfolio_review", []),
            "decision_coach": data.get("decision_coach", []),
            "action_plan": data.get("action_plan", []),
        }
        return report

    def to_markdown(self, report: dict) -> str:
        lines = [
            f"# {report['title']}",
            "",
            f"Generated: {report['generated_at']}",
            "",
            "## Market Summary",
            "",
        ]
        lines.extend(self._bullets(report.get("market_summary", [])))
        lines.extend(["", "## Future Leaders", ""])
        lines.extend(self._bullets(report.get("future_leaders", [])))
        lines.extend(["", "## Portfolio Review", ""])
        lines.extend(self._bullets(report.get("portfolio_review", [])))
        lines.extend(["", "## Decision Coach", ""])
        lines.extend(self._bullets(report.get("decision_coach", [])))
        lines.extend(["", "## Action Plan", ""])
        lines.extend(self._bullets(report.get("action_plan", [])))
        return "\n".join(lines).strip() + "\n"

    def to_json(self, report: dict) -> str:
        return json.dumps(report, ensure_ascii=False, indent=2)

    def to_html(self, report: dict) -> str:
        md = self.to_markdown(report)
        body = "\n".join(f"<p>{line}</p>" if line and not line.startswith("#") else f"<h2>{line.replace('#','').strip()}</h2>" for line in md.splitlines())
        return f"<html><body>{body}</body></html>"

    def _bullets(self, items):
        if not items:
            return ["- None"]
        if isinstance(items, str):
            return [f"- {items}"]
        return [f"- {item}" for item in items]
