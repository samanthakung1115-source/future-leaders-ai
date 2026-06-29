
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from service_registry import ServiceRegistry


def test_service_registry_unknown_service():
    registry = ServiceRegistry(services={})
    assert registry.get("missing") is None
    assert registry.status("missing").available is False


def test_service_registry_builtin_import():
    registry = ServiceRegistry(services={"json_loads": ("json", "loads")})
    func = registry.get("json_loads")
    assert func is not None
    assert func('{"ok": true}')["ok"] is True
    assert registry.available("json_loads") is True


def test_service_registry_all_status():
    registry = ServiceRegistry(services={
        "json_loads": ("json", "loads"),
        "bad": ("not_a_real_module", "nope"),
    })
    status = registry.all_status()
    assert len(status) == 2
    assert any(s.name == "json_loads" and s.available for s in status)
    assert any(s.name == "bad" and not s.available for s in status)


if __name__ == "__main__":
    test_service_registry_unknown_service()
    test_service_registry_builtin_import()
    test_service_registry_all_status()
    print("Future Leaders AI v1.2 RC Sprint 2 Service Registry test passed.")
