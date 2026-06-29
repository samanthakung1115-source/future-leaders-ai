
from __future__ import annotations

from core import Settings
from ranking import FutureLeadersRankingEngine, RankingCandidateLoader


class RankingService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.loader = RankingCandidateLoader()
        self.engine = FutureLeadersRankingEngine(
            weights=settings.ranking_weights,
            thresholds=settings.score_thresholds,
        )

    def build_from_path(self, path: str, limit: int | None = None) -> dict:
        candidates = self.loader.load_path(path)
        return self.build(candidates, limit=limit)

    def build(self, candidates, limit: int | None = None) -> dict:
        limit = limit or self.settings.default_candidate_limit
        ranked = self.engine.rank(candidates, limit=limit)
        rows = [item.to_dict() for item in ranked]

        return {
            "title": "Future Leaders Ranking",
            "count": len(rows),
            "top": rows[0] if rows else None,
            "ranked": rows,
        }
