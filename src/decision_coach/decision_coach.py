
from dataclasses import dataclass

@dataclass
class DecisionAdvice:
    ticker:str
    decision:str
    confidence:str
    reasons:list[str]
    lessons:list[str]

class DecisionCoach:
    """Generate explainable investment guidance."""

    def evaluate(self, research_card:dict, user_history:dict|None=None):
        score=research_card.get("score",0)
        reasons=list(research_card.get("why_selected",[]))
        lessons=[]
        if user_history:
            lessons.extend(user_history.get("lessons",[]))

        if score>=80:
            decision="Research Further"
            confidence="High"
        elif score>=60:
            decision="Watch"
            confidence="Medium"
        else:
            decision="Avoid For Now"
            confidence="Low"

        return DecisionAdvice(
            ticker=research_card.get("ticker","UNKNOWN"),
            decision=decision,
            confidence=confidence,
            reasons=reasons,
            lessons=lessons,
        )
