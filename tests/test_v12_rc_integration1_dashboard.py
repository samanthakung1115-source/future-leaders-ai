
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_integrated_exists():
    p = PROJECT_ROOT / "src" / "ui" / "dashboard_integrated.py"
    text = p.read_text(encoding="utf-8")
    assert "render_dashboard" in text
    assert "build_unified_sts_live_pipeline" in text
    assert "render_samantha_brief" in text


if __name__ == "__main__":
    test_dashboard_integrated_exists()
    print("Future Leaders AI v1.2 RC Integration 1 Dashboard test passed.")
