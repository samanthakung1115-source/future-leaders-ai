
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from core import Settings
from discovery import CandidateLoader
from portfolio import PortfolioLoader
from services import BriefService


def test_rc1_milestone1_brief_service():
    settings = Settings.load(PROJECT_ROOT / "config" / "settings.json")
    candidates = CandidateLoader().load_path(PROJECT_ROOT / "data" / "candidates" / "sample_candidates.csv")
    positions = PortfolioLoader().load_path(PROJECT_ROOT / "data" / "portfolio" / "sample_portfolio.csv")

    brief = BriefService(settings).build(candidates, positions).to_dict()

    assert brief["title"] == "Samantha Daily Brief"
    assert brief["future_leaders"][0]["ticker"] == "RKLB"
    assert brief["future_leaders"][0]["is_holding"] is True
    assert any(item["ticker"] == "SOFI" and item["action"] == "Review Thesis Before Adding" for item in brief["action_plan"])
    assert brief["portfolio_warnings"]


if __name__ == "__main__":
    test_rc1_milestone1_brief_service()
    print("Future Leaders AI v1.0 RC1 Milestone 1 test passed.")
