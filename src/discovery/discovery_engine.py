
from core import Candidate

class DiscoveryEngine:
    def rank(self, candidates: list[Candidate], limit: int = 10) -> list[Candidate]:
        return sorted(candidates, key=lambda c: c.score, reverse=True)[:limit]
    def verdict(self, score: int, thresholds: dict) -> str:
        if score >= thresholds.get("future_leader", 85):
            return "Future Leader"
        if score >= thresholds.get("high_potential", 70):
            return "High Potential"
        if score >= thresholds.get("watch", 55):
            return "Watch"
        return "Low Priority"
