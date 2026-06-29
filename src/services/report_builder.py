
from __future__ import annotations
from datetime import datetime

class MarkdownReportBuilder:
    def build(self, brief: dict, generated_at: str | None = None) -> str:
        generated_at = generated_at or datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = [
            f"# {brief.get('title', 'Samantha Daily Brief')}",
            "",
            f"Generated: {generated_at}",
            "",
            "## Summary",
            "",
            brief.get("summary", ""),
            "",
            "## Samantha Comment",
            "",
            brief.get("samantha_comment", ""),
            "",
        ]

        lines.extend(self._section("Portfolio Warnings", brief.get("portfolio_warnings", [])))
        lines.extend(self._research_cards(brief.get("research_cards", [])))
        lines.extend(self._action_plan(brief.get("action_plan", [])))
        lines.extend(self._decision_coach(brief.get("decision_coach", [])))

        return "\n".join(lines).strip() + "\n"

    def _section(self, title: str, items: list[str]) -> list[str]:
        lines = [f"## {title}", ""]
        if not items:
            lines.append("- None")
        else:
            lines.extend([f"- {item}" for item in items])
        lines.append("")
        return lines

    def _research_cards(self, cards: list[dict]) -> list[str]:
        lines = ["## Research Cards", ""]
        if not cards:
            return lines + ["- None", ""]
        for card in cards:
            lines.append(f"### {card.get('ticker')} — {card.get('verdict')}")
            lines.append("")
            lines.append(f"- Score: {card.get('score')}")
            lines.append(f"- Theme: {card.get('theme')}")
            lines.append(f"- Confidence: {card.get('confidence')}")
            lines.append(f"- Portfolio Context: {card.get('portfolio_context')}")
            if card.get("dna"):
                lines.append(f"- DNA: {', '.join(card.get('dna', []))}")
            lines.append("")
            lines.append("Why selected:")
            for reason in card.get("why_selected", []):
                lines.append(f"- {reason}")
            lines.append("")
            lines.append("Risks:")
            for risk in card.get("risks", []):
                lines.append(f"- {risk}")
            lines.append("")
        return lines

    def _action_plan(self, actions: list[dict]) -> list[str]:
        lines = ["## Action Plan", ""]
        if not actions:
            return lines + ["- None", ""]
        for action in actions:
            lines.append(f"- **{action.get('ticker')}**: {action.get('action')} ({action.get('priority')}) — {action.get('reason')}")
            if action.get("coach_note"):
                lines.append(f"  - Coach: {action.get('coach_note')}")
        lines.append("")
        return lines

    def _decision_coach(self, notes: list[dict]) -> list[str]:
        lines = ["## Decision Coach", ""]
        if not notes:
            return lines + ["- None", ""]
        for note in notes:
            lines.append(f"- **{note.get('ticker')} / {note.get('pattern')}**: {note.get('lesson')}")
        lines.append("")
        return lines
