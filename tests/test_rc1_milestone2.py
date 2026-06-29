
import io
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from core import Settings
from discovery import CandidateLoader
from portfolio import PortfolioLoader
from services import BriefService
from validation import CandidateCSVValidator, PortfolioCSVValidator

def test_rc1_milestone2_brief_and_validation():
    settings = Settings.load(PROJECT_ROOT / "config" / "settings.json")
    candidates = CandidateLoader().load_path(PROJECT_ROOT / "data" / "candidates" / "sample_candidates.csv")
    positions = PortfolioLoader().load_path(PROJECT_ROOT / "data" / "portfolio" / "sample_portfolio.csv")
    brief = BriefService(settings).build(candidates, positions, data_health={"ok": True}).to_dict()

    assert brief["future_leaders"][0]["ticker"] == "RKLB"
    assert brief["data_health"]["ok"] is True
    assert len(brief["action_plan"]) == 4

def test_csv_validation():
    good_candidates = "ticker,score,why_selected,risks\nTEM,82,AI,Valuation\n"
    bad_candidates = "ticker,why_selected\nTEM,AI\n"
    portfolio = "ticker,status,shares\nSOFI,Holding,265\n"

    assert CandidateCSVValidator().validate_file(io.StringIO(good_candidates)).ok
    assert not CandidateCSVValidator().validate_file(io.StringIO(bad_candidates)).ok
    assert PortfolioCSVValidator().validate_file(io.StringIO(portfolio)).ok

if __name__ == "__main__":
    test_rc1_milestone2_brief_and_validation()
    test_csv_validation()
    print("Future Leaders AI v1.0 RC1 Milestone 2 test passed.")
