
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from app_logging import get_app_logger, log_event, log_error
from error_boundary import safe_render


def test_logger_creates_logger():
    logger = get_app_logger(log_path="data/cache/test_app.log")
    assert logger.name == "future_leaders_ai"
    log_event("test_event", ok=True)
    log_error("test_error", error="fake")


def test_safe_render_success():
    def fn():
        return 123
    assert safe_render(fn, title="test") == 123


def test_safe_render_failure_returns_none():
    def fn():
        raise RuntimeError("boom")
    assert safe_render(fn, title="test") is None


if __name__ == "__main__":
    test_logger_creates_logger()
    test_safe_render_success()
    test_safe_render_failure_returns_none()
    print("Future Leaders AI v1.2 RC Sprint 4 Logging + Error Boundary test passed.")
