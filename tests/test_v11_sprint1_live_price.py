
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from live_price import LiveActionEngine
from live_price.candidate_price_enricher import CandidatePriceEnricher


class FakePriceEngine:
    def fetch_many(self, tickers):
        class Snap:
            def __init__(self, ticker, latest, day, high, dist):
                self.ticker = ticker
                self.latest_price = latest
                self.day_change_pct = day
                self.fifty_two_week_high = high
                self.distance_from_high_pct = dist
                self.source = "fake"
            def to_dict(self):
                return {
                    "ticker": self.ticker,
                    "latest_price": self.latest_price,
                    "day_change_pct": self.day_change_pct,
                    "fifty_two_week_high": self.fifty_two_week_high,
                    "distance_from_high_pct": self.distance_from_high_pct,
                    "source": self.source,
                }
        return [
            Snap("ANET", 100, 6, 105, -4.7),
            Snap("MYRG", 480, -1.3, 520, -7.7),
        ]


def test_live_action_engine():
    engine = LiveActionEngine()
    assert engine.decide({"day_change_pct": 6, "distance_from_high_pct": -3}) == "今天漲太多，先不要追"
    assert engine.decide({"day_change_pct": -7, "distance_from_high_pct": -20}) == "跌幅大，等止跌訊號"


def test_candidate_price_enricher():
    enricher = CandidatePriceEnricher(price_engine=FakePriceEngine())
    rows = enricher.enrich([
        {"ticker": "ANET", "tonight_action": "今晚先不要追"},
        {"ticker": "MYRG", "tonight_action": "今晚可留意"},
    ])
    assert rows[0]["live_price"] == 100
    assert rows[0]["live_action"] == "今天漲太多，先不要追"
    assert rows[1]["live_price"] == 480


if __name__ == "__main__":
    test_live_action_engine()
    test_candidate_price_enricher()
    print("Future Leaders AI v1.1 Sprint 1 Live Price Engine test passed.")
