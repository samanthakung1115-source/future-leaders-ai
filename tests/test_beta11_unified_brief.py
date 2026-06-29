
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from product import CandidateCSVLoader, UnifiedBriefService
from sts_live import STSLiveReader


def test_unified_brief_combines_candidates_and_sts():
    candidates = CandidateCSVLoader().load_path(PROJECT_ROOT / "data" / "samples" / "beta11_candidates.csv")
    positions = STSLiveReader().load_path(PROJECT_ROOT / "data" / "samples" / "beta11_sts.csv")

    brief = UnifiedBriefService().build(candidates, positions)

    assert brief["future_leaders"][0]["ticker"] == "RKLB"
    assert brief["future_leaders"][0]["is_holding"] is True
    assert any("SOFI" in warning for warning in brief["portfolio_warnings"])
    assert "Samantha" in brief["title"]


if __name__ == "__main__":
    test_unified_brief_combines_candidates_and_sts()
    print("Beta 11 Unified Brief test passed.")
