
from dataclasses import dataclass

@dataclass
class MatchResult:
    winner:str
    score:int
    matched_traits:list[str]

class WinnerDNAMatcher:
    """Simple DNA similarity matcher for Future Leaders AI."""

    def match(self, candidate_traits:list[str], winner_database:dict[str,list[str]]):
        results=[]
        c=set(t.lower() for t in candidate_traits)
        for winner,traits in winner_database.items():
            w=set(t.lower() for t in traits)
            matched=sorted(c & w)
            score=round(len(matched)/max(len(w),1)*100)
            results.append(
                MatchResult(
                    winner=winner,
                    score=score,
                    matched_traits=matched
                )
            )
        return sorted(results,key=lambda r:r.score,reverse=True)
