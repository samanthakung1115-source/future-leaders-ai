
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from action_plan import ActionPlanEngine
from product import CandidateCSVLoader, UnifiedBriefService
from sts_live import STSLiveReader


def test_action_plan_from_unified_brief():
    candidates = CandidateCSVLoader().load_path(PROJECT_ROOT / "data" / "samples" / "beta12_candidates.csv")
    positions = STSLiveReader().load_path(PROJECT_ROOT / "data" / "samples" / "beta12_sts.csv")
    brief = UnifiedBriefService().build(candidates, positions)

    items = ActionPlanEngine().build(brief)

    assert items
    by_ticker = {item.ticker: item for item in items}
    assert by_ticker["SOFI"].action == "Review Thesis Before Adding"
    assert by_ticker["MRVL"].action == "Review Hold / Trim Plan"
    assert by_ticker["TEM"].action == "Add to Watchlist"


if __name__ == "__main__":
    test_action_plan_from_unified_brief()
    print("Beta 12 Action Plan test passed.")
