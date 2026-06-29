
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sts_integration import STSBridge


def test_load_sts_portfolio_csv():
    bridge = STSBridge()
    portfolio = bridge.load_csv(PROJECT_ROOT / "data" / "samples" / "sts_portfolio_sample.csv")

    assert len(portfolio.positions) == 4
    assert portfolio.get("SOFI") is not None
    assert portfolio.get("SOFI").unrealized_return_pct == -22.49


def test_candidate_context_for_holding_and_new_candidate():
    bridge = STSBridge()
    portfolio = bridge.load_csv(PROJECT_ROOT / "data" / "samples" / "sts_portfolio_sample.csv")

    sofi = bridge.build_candidate_context("SOFI", portfolio)
    tem = bridge.build_candidate_context("TEM", portfolio)

    assert sofi["is_holding"] is True
    assert "under pressure" in sofi["portfolio_note"]
    assert tem["is_holding"] is False
    assert "discovery candidate" in tem["portfolio_note"]


if __name__ == "__main__":
    test_load_sts_portfolio_csv()
    test_candidate_context_for_holding_and_new_candidate()
    print("Beta 6 Milestone 3 STS integration tests passed.")
