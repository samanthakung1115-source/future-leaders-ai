
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sts_live import STSLiveReader, PortfolioBriefBuilder
from product.samantha_daily_product import SamanthaDailyProduct


def test_sts_live_reader_and_product():
    positions = STSLiveReader().load_path(PROJECT_ROOT / "data" / "samples" / "sts_live_sample.csv")
    assert len(positions) == 4
    assert positions[1].ticker == "SOFI"
    assert positions[1].cost_return_pct == -22.49

    brief = PortfolioBriefBuilder().build(positions)
    assert "SOFI" in brief["under_pressure"]
    assert "RKLB" in brief["deep_break"]
    assert "MRVL" in brief["strong_winners"]

    product = SamanthaDailyProduct().build(
        positions,
        [{"ticker": "TEM", "score": 82}, {"ticker": "RKLB", "score": 88}],
    )
    assert product["future_leaders"][0]["ticker"] == "RKLB"
    assert "Protect capital" in product["samantha_comment"]


if __name__ == "__main__":
    test_sts_live_reader_and_product()
    print("Beta 10 STS Live Integration test passed.")
