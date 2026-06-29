
import sys
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sts_sync import STSLiveSyncEngine, SyncConfig


class FakeResponse:
    text = "ticker,shares,cost\nRKLB,129,28.9\nSOFI,265,23.0\n"
    def raise_for_status(self):
        return None


def test_sts_sync_engine_with_mock_response():
    config = SyncConfig(
        sts_google_sheet_url="https://example.com/edit",
        sts_csv_export_url="https://example.com/export?format=csv&gid=1",
        cache_path="data/cache/test_sts_latest.csv",
    )

    with patch("requests.get", return_value=FakeResponse()):
        df, result = STSLiveSyncEngine(config).sync()

    assert result.ok is True
    assert len(df) == 2
    assert "ticker" in result.columns
    assert df.iloc[0]["ticker"] == "RKLB"


if __name__ == "__main__":
    test_sts_sync_engine_with_mock_response()
    print("Future Leaders AI v1.1 Sprint 2 STS Live Sync Engine test passed.")
