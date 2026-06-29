
from dataclasses import dataclass, asdict

@dataclass
class Recommendation:
    ticker: str
    action: str
    confidence: str
    summary: str
    reasons: list[str]
    risks: list[str]

    def to_dict(self):
        return asdict(self)

class RecommendationEngine:
    def recommend(self, research_card: dict, decision: dict, winner_matches: list):
        score = research_card.get("score", 0)
        if score >= 85:
            action, confidence = "Research & Build Position", "High"
        elif score >= 65:
            action, confidence = "Watch Closely", "Medium"
        else:
            action, confidence = "Wait", "Low"

        top_match = winner_matches[0].winner if winner_matches else "None"
        summary = f"Top Winner DNA: {top_match}. Decision Coach: {decision.get('decision','N/A')}."

        return Recommendation(
            ticker=research_card.get("ticker", "UNKNOWN"),
            action=action,
            confidence=confidence,
            summary=summary,
            reasons=research_card.get("why_selected", []),
            risks=research_card.get("risks", []),
        )
