
import io
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from config import SamanthaSettings
from validation import CandidateCSVValidator, STSCSVValidator


def test_settings_load_default_config():
    settings = SamanthaSettings.load(PROJECT_ROOT / "config" / "samantha_config.json")
    assert settings.app_name == "Samantha AI Platform"
    assert settings.score_thresholds["future_leader"] == 85


def test_candidate_csv_validator():
    csv_text = "ticker,score,why_selected,risks\nTEM,82,AI platform,valuation\n"
    result = CandidateCSVValidator().validate_file(io.StringIO(csv_text))
    assert result.ok
    assert "ticker" in result.detected_columns


def test_candidate_csv_validator_missing_score():
    csv_text = "ticker,why_selected\nTEM,AI platform\n"
    result = CandidateCSVValidator().validate_file(io.StringIO(csv_text))
    assert not result.ok
    assert "score" in result.missing_columns


def test_sts_csv_validator():
    csv_text = "ticker,status,shares,cost_return_pct\nSOFI,Holding,265,-22.49\n"
    result = STSCSVValidator().validate_file(io.StringIO(csv_text))
    assert result.ok


if __name__ == "__main__":
    test_settings_load_default_config()
    test_candidate_csv_validator()
    test_candidate_csv_validator_missing_score()
    test_sts_csv_validator()
    print("Beta 14 Settings + Validation test passed.")
