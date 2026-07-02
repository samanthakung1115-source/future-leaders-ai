from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def test_launcher_has_portfolio_center():
    text = (PROJECT_ROOT / "src" / "main_launcher" / "launcher.py").read_text(encoding="utf-8")
    assert "Portfolio Center" in text
    assert "ui.portfolio_center_integrated" in text

def test_app_uses_main_launcher():
    text = (PROJECT_ROOT / "app.py").read_text(encoding="utf-8")
    assert "render_main_launcher" in text

def test_portfolio_center_exists():
    text = (PROJECT_ROOT / "src" / "ui" / "portfolio_center_integrated.py").read_text(encoding="utf-8")
    assert "def render()" in text
    assert "同步 Portfolio" in text

if __name__ == "__main__":
    test_launcher_has_portfolio_center()
    test_app_uses_main_launcher()
    test_portfolio_center_exists()
    print("Future Leaders AI v1.2 RC Integration 2.1 Auto Install test passed.")
