
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from core import Settings
from discovery import CandidateLoader
from portfolio import PortfolioLoader
from decision import DecisionMemoryLoader
from services import BriefService

def test_rc1_milestone3_decision_memory():
    settings = Settings.load(PROJECT_ROOT / "config" / "settings.json")
    candidates = CandidateLoader().load_path(PROJECT_ROOT / "data" / "candidates" / "sample_candidates.csv")
    positions = PortfolioLoader().load_path(PROJECT_ROOT / "data" / "portfolio" / "sample_portfolio.csv")
    patterns = DecisionMemoryLoader().load_path(PROJECT_ROOT / "data" / "decision_memory" / "patterns.csv")

    brief = BriefService(settings).build(candidates, positions, decision_patterns=patterns, data_health={"ok": True}).to_dict()

    assert brief["decision_coach"]
    assert any(note["ticker"] == "RKLB" for note in brief["decision_coach"])
    assert any(item["ticker"] == "SOFI" and item["action"] == "Review Thesis Before Adding" for item in brief["action_plan"])
    assert "Decision patterns detected" in brief["samantha_comment"]

if __name__ == "__main__":
    test_rc1_milestone3_decision_memory()
    print("Future Leaders AI v1.0 RC1 Milestone 3 test passed.")
