
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from product import DailyBriefService


def test_daily_brief_service_builds_ranked_brief():
    service = DailyBriefService()
    candidates = [
        {"ticker": "A", "score": 50, "why_selected": ["x"], "risks": []},
        {"ticker": "B", "score": 90, "why_selected": ["y"], "risks": ["risk"]},
    ]

    brief = service.build(candidates, portfolio={"B": "Existing holding"})

    assert brief["top_future_leaders"][0]["ticker"] == "B"
    assert brief["top_future_leaders"][0]["verdict"] == "Future Leader"
    assert brief["portfolio_reminders"]
    assert "Samantha" in brief["title"]


if __name__ == "__main__":
    test_daily_brief_service_builds_ranked_brief()
    print("Beta 7 Daily Brief test passed.")
