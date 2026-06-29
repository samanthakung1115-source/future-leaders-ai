
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_main_app_exists_and_contains_launcher():
    app = PROJECT_ROOT / "app.py"
    assert app.exists()
    text = app.read_text(encoding="utf-8")
    assert "Samantha AI" in text
    assert "Select page" in text
    assert "Action Plan" in text


if __name__ == "__main__":
    test_main_app_exists_and_contains_launcher()
    print("Beta 13 Main App Launcher test passed.")
