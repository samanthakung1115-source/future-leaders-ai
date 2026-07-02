
import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from market_scanner import MarketScanner


def test_market_scanner_rank():
    df = pd.DataFrame([
        {"ticker": "AAA", "trend": 90, "momentum": 90, "fundamental": 90, "narrative": 90, "valuation": 80, "flow": 80, "decision": 80},
        {"ticker": "BBB", "trend": 50, "momentum": 50, "fundamental": 50, "narrative": 50, "valuation": 50, "flow": 50, "decision": 50},
    ])
    result = MarketScanner().scan_dataframe(df, top_n=2)
    assert result.iloc[0]["ticker"] == "AAA"
    assert result.iloc[0]["leader_score"] > result.iloc[1]["leader_score"]
    assert "role" in result.columns


if __name__ == "__main__":
    test_market_scanner_rank()
    print("Future Leaders AI Sprint 3.2 Market Scanner test passed.")
