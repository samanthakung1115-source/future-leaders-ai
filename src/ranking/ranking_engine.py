
from __future__ import annotations

from core import RankedCandidate, RankingCandidate


class FutureLeadersRankingEngine:
    """Multi-factor ranking engine for Future Leaders AI v1.0 Release."""

    def __init__(self, weights: dict, thresholds: dict):
        self.weights = weights
        self.thresholds = thresholds

    def rank(self, candidates: list[RankingCandidate], limit: int = 10) -> list[RankedCandidate]:
        scored = []
        for candidate in candidates:
            total = self.score(candidate)
            scored.append((candidate, total))

        scored.sort(key=lambda item: item[1], reverse=True)

        ranked = []
        for idx, (candidate, total) in enumerate(scored[:limit], start=1):
            ranked.append(
                RankedCandidate(
                    rank=idx,
                    ticker=candidate.ticker,
                    total_score=round(total, 2),
                    verdict=self.verdict(total),
                    change=self.rank_change(idx, candidate.previous_rank),
                    theme=candidate.theme,
                    dna=candidate.dna,
                    why_selected=candidate.why_selected,
                    risks=candidate.risks,
                )
            )

        return ranked

    def score(self, candidate: RankingCandidate) -> float:
        # risk_score is treated as quality of risk control, not danger.
        return (
            candidate.ai_score * self.weights.get("ai_score", 0.40)
            + candidate.growth_score * self.weights.get("growth_score", 0.25)
            + candidate.quality_score * self.weights.get("quality_score", 0.20)
            + candidate.risk_score * self.weights.get("risk_score", 0.15)
        )

    def verdict(self, score: float) -> str:
        if score >= self.thresholds.get("future_leader", 85):
            return "Future Leader"
        if score >= self.thresholds.get("high_potential", 70):
            return "High Potential"
        if score >= self.thresholds.get("watch", 55):
            return "Watch"
        return "Low Priority"

    def rank_change(self, current_rank: int, previous_rank: int | None) -> str:
        if previous_rank is None:
            return "NEW"
        if current_rank < previous_rank:
            return f"↑ {previous_rank - current_rank}"
        if current_rank > previous_rank:
            return f"↓ {current_rank - previous_rank}"
        return "—"
