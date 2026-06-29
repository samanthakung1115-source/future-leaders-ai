
from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class ReleaseStatus:
    name: str
    version: str
    channel: str
    status: str
    next_focus: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DashboardSection:
    title: str
    subtitle: str
    status: str
    items: list[str]

    def to_dict(self) -> dict:
        return asdict(self)
