
from core import Candidate, ResearchCard

class ResearchCardEngine:
    def __init__(self, discovery_engine):
        self.discovery = discovery_engine

    def build_card(self, candidate: Candidate, portfolio_context: str, coach_notes: list[dict], settings) -> ResearchCard:
        return ResearchCard(
            ticker=candidate.ticker,
            score=candidate.score,
            verdict=self.discovery.verdict(candidate.score, settings.score_thresholds),
            theme=candidate.theme or "Unclassified",
            why_selected=candidate.why_selected[:settings.research_card.get("max_reasons", 5)],
            risks=candidate.risks[:settings.research_card.get("max_risks", 5)],
            dna=candidate.dna,
            portfolio_context=portfolio_context,
            coach_notes=coach_notes,
            confidence=self.discovery.confidence(candidate.score),
        )
