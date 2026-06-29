
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from core import Settings
from services import ReleaseDashboardService


def test_release_dashboard_service():
    settings = Settings.load(PROJECT_ROOT / "config" / "settings.json")
    service = ReleaseDashboardService(settings)

    status = service.status().to_dict()
    sections = [section.to_dict() for section in service.sections()]

    assert "v1.0 Release" in status["version"]
    assert status["channel"] == "v1.0 Release"
    assert len(sections) == 5
    assert sections[0]["title"] == "Market Snapshot"
    assert any(section["title"] == "Decision Coach" for section in sections)


if __name__ == "__main__":
    test_release_dashboard_service()
    print("Future Leaders AI v1.0 Release Sprint 1 test passed.")
