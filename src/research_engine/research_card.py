
from dataclasses import dataclass

@dataclass
class ResearchCard:
    ticker:str
    score:int
    why_selected:list[str]
    similar_winners:list[str]
    risks:list[str]
    verdict:str

class ResearchCardGenerator:
    def generate(self,ticker:str,score:int,reasons:list[str],similar:list[str],risks:list[str]):
        if score>=80:
            verdict="Strong Candidate"
        elif score>=60:
            verdict="Watch List"
        else:
            verdict="Needs More Evidence"
        return ResearchCard(
            ticker=ticker,
            score=score,
            why_selected=reasons,
            similar_winners=similar,
            risks=risks,
            verdict=verdict,
        )
