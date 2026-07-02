
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sts_api import STSApiClient, STSApiConfig


def test_unconfigured_api_returns_error():
    cfg = STSApiConfig(api_base_url="")
    client = STSApiClient(cfg)
    result = client.health()
    assert result["ok"] is False
    assert "not configured" in result["error"]


def test_extract_rows():
    cfg = STSApiConfig(api_base_url="")
    client = STSApiClient(cfg)
    rows = client._extract_rows({"data": {"rows": [{"ticker": "RKLB"}]}}, "data")
    assert rows[0]["ticker"] == "RKLB"


if __name__ == "__main__":
    test_unconfigured_api_returns_error()
    test_extract_rows()
    print("STS API Engine v1.0 Sprint 1 test passed.")
