
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from integration import IntegratedAnalysisEngine

def test_integrated_analysis_engine():
    engine = IntegratedAnalysisEngine(repo_root=PROJECT_ROOT)
    result = engine.analyze_ticker(
        ticker="TEM",
        target_dna=["AI Infrastructure", "Platform"],
        user_history={"lessons": ["Do not chase only because a stock is moving."]}
    )

    assert result["company"]["ticker"] == "TEM"
    assert result["research_card"]["ticker"] == "TEM"
    assert result["research_card"]["score"] >= 50
    assert result["winner_matches"]
    assert result["decision_advice"]["decision"] in {"Research Further", "Watch", "Avoid For Now"}
    assert result["recommendation"]["action"] in {"Research & Build Position", "Watch Closely", "Wait"}

if __name__ == "__main__":
    test_integrated_analysis_engine()
    print("Beta 6 Milestone 1 integration test passed.")
