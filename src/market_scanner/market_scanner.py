
from dataclasses import dataclass

@dataclass
class Candidate:
    ticker:str
    score:int
    reasons:list[str]
    verdict:str

class MarketScanner:
    """First market scanning layer for Future Leaders AI."""

    def rank(self, companies:list[dict]) -> list[Candidate]:
        ranked=[]
        for company in companies:
            score=int(company.get("score",0))
            if score>=85:
                verdict="Future Leader"
            elif score>=70:
                verdict="High Potential"
            else:
                verdict="Watch"
            ranked.append(
                Candidate(
                    ticker=company["ticker"],
                    score=score,
                    reasons=company.get("reasons",[]),
                    verdict=verdict
                )
            )
        return sorted(ranked,key=lambda c:c.score,reverse=True)
