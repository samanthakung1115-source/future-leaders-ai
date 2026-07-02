
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

def test_client_has_multi_sheet_methods():
    cfg = STSApiConfig(api_base_url="")
    client = STSApiClient(cfg)
    assert hasattr(client, "watch")
    assert hasattr(client, "decision")
    assert hasattr(client, "roles")
    assert hasattr(client, "watch_df")
    assert hasattr(client, "decision_df")
    assert hasattr(client, "roles_df")

def test_extract_rows():
    cfg = STSApiConfig(api_base_url="")
    client = STSApiClient(cfg)
    rows = client._extract_rows({"data": {"rows": [{"ticker": "RKLB"}]}}, "data")
    assert rows[0]["ticker"] == "RKLB"

if __name__ == "__main__":
    test_unconfigured_api_returns_error()
    test_client_has_multi_sheet_methods()
    test_extract_rows()
    print("STS API Engine v1.0 Sprint 2 test passed.")
