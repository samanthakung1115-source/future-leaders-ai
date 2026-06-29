
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from core import Settings
from ranking import RankingCandidateLoader, FutureLeadersRankingEngine
from services import RankingService


def test_release_sprint2_ranking_engine():
    settings = Settings.load(PROJECT_ROOT / "config" / "settings.json")
    candidates = RankingCandidateLoader().load_path(PROJECT_ROOT / "data" / "candidates" / "release_sprint2_candidates.csv")
    engine = FutureLeadersRankingEngine(settings.ranking_weights, settings.score_thresholds)

    ranked = engine.rank(candidates, limit=5)
    assert ranked[0].ticker == "CRDO"
    assert ranked[0].verdict == "Future Leader"
    assert ranked[0].change == "—"
    assert any(item.change == "NEW" for item in ranked)

def test_release_sprint2_ranking_service():
    settings = Settings.load(PROJECT_ROOT / "config" / "settings.json")
    candidates = RankingCandidateLoader().load_path(PROJECT_ROOT / "data" / "candidates" / "release_sprint2_candidates.csv")
    result = RankingService(settings).build(candidates, limit=3)

    assert result["count"] == 3
    assert result["top"]["ticker"] == "CRDO"
    assert result["ranked"][1]["ticker"] in {"RKLB", "TEM"}

if __name__ == "__main__":
    test_release_sprint2_ranking_engine()
    test_release_sprint2_ranking_service()
    print("Future Leaders AI v1.0 Release Sprint 2 test passed.")
