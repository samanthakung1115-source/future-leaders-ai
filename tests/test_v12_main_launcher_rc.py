
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_app_py_uses_main_launcher():
    app = PROJECT_ROOT / "app.py"
    text = app.read_text(encoding="utf-8")
    assert "render_main_launcher" in text
    assert "ui.sts_sync_page import render" not in text


def test_launcher_exists():
    launcher = PROJECT_ROOT / "src" / "main_launcher" / "launcher.py"
    text = launcher.read_text(encoding="utf-8")
    assert "STS Live Sync" in text
    assert "v1.1 Control Center" in text
    assert "safe_import" in text


if __name__ == "__main__":
    test_app_py_uses_main_launcher()
    test_launcher_exists()
    print("Future Leaders AI v1.2 Main Launcher RC test passed.")
