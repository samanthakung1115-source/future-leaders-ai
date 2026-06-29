
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from core import Settings
from discovery import CandidateLoader
from portfolio import PortfolioLoader
from decision import DecisionMemoryLoader
from services import BriefService, MarkdownReportBuilder

def test_rc1_milestone5_report_builder():
    settings = Settings.load(PROJECT_ROOT / "config" / "settings.json")
    candidates = CandidateLoader().load_path(PROJECT_ROOT / "data" / "candidates" / "sample_candidates.csv")
    positions = PortfolioLoader().load_path(PROJECT_ROOT / "data" / "portfolio" / "sample_portfolio.csv")
    patterns = DecisionMemoryLoader().load_path(PROJECT_ROOT / "data" / "decision_memory" / "patterns.csv")
    brief = BriefService(settings).build(candidates, positions, decision_patterns=patterns, data_health={"ok": True}).to_dict()
    report = MarkdownReportBuilder().build(brief, generated_at="2026-06-29 09:00")

    assert "# Samantha Daily Brief" in report
    assert "## Research Cards" in report
    assert "RKLB" in report
    assert "## Action Plan" in report
    assert "## Decision Coach" in report

if __name__ == "__main__":
    test_rc1_milestone5_report_builder()
    print("Future Leaders AI v1.0 RC1 Milestone 5 test passed.")
