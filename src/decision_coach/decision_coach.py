
from dataclasses import dataclass, asdict

@dataclass
class DecisionAdvice:
    ticker: str
    decision: str
    confidence: str
    reasons: list[str]
    lessons: list[str]

    def to_dict(self):
        return asdict(self)

class DecisionCoach:
    def evaluate(self, research_card: dict, user_history: dict | None = None):
        score = research_card.get("score", 0)
        lessons = []
        if user_history:
            lessons.extend(user_history.get("lessons", []))

        if score >= 80:
            decision, confidence = "Research Further", "High"
        elif score >= 60:
            decision, confidence = "Watch", "Medium"
        else:
            decision, confidence = "Avoid For Now", "Low"

        return DecisionAdvice(
            ticker=research_card.get("ticker", "UNKNOWN"),
            decision=decision,
            confidence=confidence,
            reasons=list(research_card.get("why_selected", [])),
            lessons=lessons,
        )
