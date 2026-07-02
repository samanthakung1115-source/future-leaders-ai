
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_launcher_has_market_scanner():
    text = (PROJECT_ROOT / "src" / "main_launcher" / "launcher.py").read_text(encoding="utf-8")
    assert "Market Scanner" in text
    assert "ui.market_scanner_page" in text


def test_market_scanner_page_exists():
    text = (PROJECT_ROOT / "src" / "ui" / "market_scanner_page.py").read_text(encoding="utf-8")
    assert "Run Scanner" in text
    assert "Tonight Future Leaders" in text


if __name__ == "__main__":
    test_launcher_has_market_scanner()
    test_market_scanner_page_exists()
    print("Future Leaders AI Sprint 3.3 Market Scanner Auto-Install test passed.")
