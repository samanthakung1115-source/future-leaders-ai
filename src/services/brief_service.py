
from core import SamanthaBrief
from discovery import DiscoveryEngine
from portfolio import PortfolioEngine
from decision import ActionEngine


class BriefService:
    def __init__(self, settings):
        self.settings = settings
        self.discovery = DiscoveryEngine()
        self.portfolio = PortfolioEngine()
        self.action = ActionEngine()

    def build(self, candidates, positions) -> SamanthaBrief:
        ranked = self.discovery.rank(candidates, self.settings.default_candidate_limit)
        warnings = self.portfolio.warnings(positions, self.settings.portfolio_rules)

        enriched = []
        for c in ranked:
            is_holding, context = self.portfolio.context(c.ticker, positions, self.settings.portfolio_rules)
            score = c.score
            enriched.append({
                "ticker": c.ticker,
                "score": score,
                "verdict": self.discovery.verdict(score, self.settings.score_thresholds),
                "why_selected": c.why_selected,
                "risks": c.risks,
                "is_holding": is_holding,
                "portfolio_context": context,
            })

        action_plan = [item.to_dict() for item in self.action.build_plan(enriched)]
        leaders = [x["ticker"] for x in enriched if x["verdict"] == "Future Leader"]
        summary = (
            f"{len(enriched)} candidates evaluated. Future Leaders: {', '.join(leaders)}."
            if leaders else
            f"{len(enriched)} candidates evaluated. No confirmed Future Leader yet."
        )

        comment = self._comment(enriched, warnings)

        return SamanthaBrief(
            title="Samantha Daily Brief",
            summary=summary,
            future_leaders=enriched,
            portfolio_warnings=warnings,
            action_plan=action_plan,
            samantha_comment=comment,
        )

    def _comment(self, enriched: list[dict], warnings: list[str]) -> str:
        if warnings:
            return "Portfolio has warnings. Review risk before adding new capital."
        if any(x["verdict"] == "Future Leader" for x in enriched):
            return "Research top candidates, but avoid chasing price alone."
        return "Focus on watchlist building and wait for stronger evidence."
