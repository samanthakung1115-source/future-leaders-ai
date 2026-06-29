
from __future__ import annotations

from dataclasses import dataclass, asdict
import importlib
from typing import Any


@dataclass
class ServiceStatus:
    name: str
    module: str
    attribute: str
    available: bool
    message: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


class ServiceRegistry:
    """Central service registry for Future Leaders AI v1.2.

    Purpose:
    - Stop importing patch modules everywhere in app.py.
    - Safely load optional services.
    - Provide one place to check availability.
    """

    DEFAULT_SERVICES = {
        "sts_sync": ("sts_sync", "STSLiveSyncPatch"),
        "sts_mapper": ("sts_mapper", "normalize_sts_columns"),
        "live_price": ("live_price", "enrich_with_live_price"),
        "price_cache": ("price_cache", "enrich_with_cached_live_price"),
        "unified_pipeline": ("unified_pipeline", "build_unified_sts_live_pipeline"),
        "pipeline_status": ("unified_pipeline", "render_unified_pipeline_status"),
        "samantha_brief": ("samantha_brief", "render_samantha_brief"),
        "patch_health": ("patch_health", "render_patch_health_check"),
        "install_checklist": ("patch_checklist", "render_patch_install_checklist"),
        "v11_control_center": ("v11_control_center", "render_v11_control_center"),
        "v11_launcher": ("v11_launcher", "render_v11_launcher_menu"),
    }

    def __init__(self, services: dict[str, tuple[str, str]] | None = None):
        self.services = services or self.DEFAULT_SERVICES
        self._cache: dict[str, Any] = {}
        self._status: dict[str, ServiceStatus] = {}

    def get(self, name: str):
        if name in self._cache:
            return self._cache[name]

        if name not in self.services:
            self._status[name] = ServiceStatus(
                name=name,
                module="",
                attribute="",
                available=False,
                message="Service not registered.",
            )
            return None

        module_name, attr_name = self.services[name]

        try:
            module = importlib.import_module(module_name)
            obj = getattr(module, attr_name)
            self._cache[name] = obj
            self._status[name] = ServiceStatus(
                name=name,
                module=module_name,
                attribute=attr_name,
                available=True,
                message="OK",
            )
            return obj
        except Exception as exc:
            self._status[name] = ServiceStatus(
                name=name,
                module=module_name,
                attribute=attr_name,
                available=False,
                message=str(exc),
            )
            return None

    def status(self, name: str) -> ServiceStatus:
        if name not in self._status:
            self.get(name)
        return self._status[name]

    def all_status(self) -> list[ServiceStatus]:
        for name in self.services:
            self.status(name)
        return [self._status[name] for name in self.services]

    def available(self, name: str) -> bool:
        return self.status(name).available

    def call(self, name: str, *args, **kwargs):
        service = self.get(name)
        if service is None:
            return None
        return service(*args, **kwargs)


_registry: ServiceRegistry | None = None


def get_registry() -> ServiceRegistry:
    global _registry
    if _registry is None:
        _registry = ServiceRegistry()
    return _registry
