
from dataclasses import dataclass, asdict

@dataclass
class MatchResult:
    winner: str
    score: int
    matched_traits: list[str]

    def to_dict(self):
        return asdict(self)

class WinnerDNAMatcher:
    def match(self, candidate_traits: list[str], winner_database: dict[str, list[str]]):
        results = []
        candidate = {t.lower() for t in candidate_traits}
        for winner, traits in winner_database.items():
            win = {t.lower() for t in traits}
            matched = sorted(candidate & win)
            score = round(len(matched) / max(len(win), 1) * 100)
            results.append(MatchResult(winner=winner, score=score, matched_traits=matched))
        return sorted(results, key=lambda x: x.score, reverse=True)
