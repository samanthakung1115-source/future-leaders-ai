
from core import SamanthaBrief
from discovery import DiscoveryEngine, ResearchCardEngine
from portfolio import PortfolioEngine
from decision import ActionEngine, DecisionCoachEngine

class BriefService:
    def __init__(self, settings):
        self.settings = settings
        self.discovery = DiscoveryEngine()
        self.research_cards = ResearchCardEngine(self.discovery)
        self.portfolio = PortfolioEngine()
        self.action = ActionEngine()
        self.coach = DecisionCoachEngine()

    def build(self, candidates, positions, decision_patterns=None, data_health: dict | None = None) -> SamanthaBrief:
        decision_patterns = decision_patterns or []
        ranked = self.discovery.rank(candidates, self.settings.default_candidate_limit)
        warnings = self.portfolio.warnings(positions, self.settings.portfolio_rules)
        enriched, cards = [], []

        for c in ranked:
            is_holding, context = self.portfolio.context(c.ticker, positions, self.settings.portfolio_rules)
            coach_notes = self.coach.notes_for(c.ticker, decision_patterns)
            verdict = self.discovery.verdict(c.score, self.settings.score_thresholds)
            row = {
                "ticker": c.ticker, "score": c.score, "verdict": verdict,
                "theme": c.theme or "Unclassified", "why_selected": c.why_selected,
                "risks": c.risks, "dna": c.dna, "is_holding": is_holding,
                "portfolio_context": context, "coach_notes": coach_notes,
            }
            enriched.append(row)
            cards.append(self.research_cards.build_card(c, context, coach_notes, self.settings).to_dict())

        action_plan = [item.to_dict() for item in self.action.build_plan(enriched)]
        leaders = [x["ticker"] for x in enriched if x["verdict"] == "Future Leader"]
        summary = f"{len(enriched)} candidates evaluated. Future Leaders: {', '.join(leaders)}." if leaders else f"{len(enriched)} candidates evaluated. No confirmed Future Leader yet."
        decision_coach = self._decision_coach_summary(enriched, decision_patterns)

        return SamanthaBrief(
            title="Samantha Daily Brief",
            summary=summary,
            future_leaders=enriched,
            research_cards=cards,
            portfolio_warnings=warnings,
            action_plan=action_plan,
            decision_coach=decision_coach,
            samantha_comment=self._comment(enriched, warnings, decision_coach, data_health or {}),
            data_health=data_health or {},
        )

    def _decision_coach_summary(self, enriched: list[dict], patterns) -> list[dict]:
        notes = []
        for item in enriched:
            for note in item.get("coach_notes", []):
                notes.append({"ticker": item["ticker"], "pattern": note.get("pattern"), "lesson": note.get("lesson"), "severity": note.get("severity", "Medium")})
        for note in self.coach.general_notes(patterns):
            notes.append({"ticker": "GENERAL", "pattern": note.get("pattern"), "lesson": note.get("lesson"), "severity": note.get("severity", "Medium")})
        return notes

    def _comment(self, enriched: list[dict], warnings: list[str], decision_coach: list[dict], data_health: dict) -> str:
        if data_health and not data_health.get("ok", True):
            return "Data quality issue detected. Fix CSV columns before relying on the brief."
        if decision_coach:
            return "Decision patterns detected. Review Samantha Coach before adding or trimming positions."
        if warnings:
            return "Portfolio has warnings. Review risk before adding new capital."
        if any(x["verdict"] == "Future Leader" for x in enriched):
            return "Research top candidates, but avoid chasing price alone."
        return "Focus on watchlist building and wait for stronger evidence."
