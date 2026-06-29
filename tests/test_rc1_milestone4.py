
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from core import Settings
from discovery import CandidateLoader
from portfolio import PortfolioLoader
from decision import DecisionMemoryLoader
from services import BriefService

def test_rc1_milestone4_research_cards():
    settings = Settings.load(PROJECT_ROOT / "config" / "settings.json")
    candidates = CandidateLoader().load_path(PROJECT_ROOT / "data" / "candidates" / "sample_candidates.csv")
    positions = PortfolioLoader().load_path(PROJECT_ROOT / "data" / "portfolio" / "sample_portfolio.csv")
    patterns = DecisionMemoryLoader().load_path(PROJECT_ROOT / "data" / "decision_memory" / "patterns.csv")

    brief = BriefService(settings).build(candidates, positions, decision_patterns=patterns, data_health={"ok": True}).to_dict()

    assert brief["research_cards"]
    rklb = next(card for card in brief["research_cards"] if card["ticker"] == "RKLB")
    assert rklb["verdict"] == "Future Leader"
    assert rklb["coach_notes"]
    assert "Space Infrastructure" in rklb["dna"]
    assert any(item["ticker"] == "MRVL" and item["action"] == "Review Hold / Trim Plan" for item in brief["action_plan"])

if __name__ == "__main__":
    test_rc1_milestone4_research_cards()
    print("Future Leaders AI v1.0 RC1 Milestone 4 test passed.")
