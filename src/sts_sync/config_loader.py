
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SyncConfig:
    sts_google_sheet_url: str
    sts_csv_export_url: str
    refresh_seconds: int = 60
    cache_path: str = "data/cache/sts_latest.csv"
    source_name: str = "STS Google Sheet"

    @classmethod
    def load(cls, path: str | Path = "config/sync_config.json") -> "SyncConfig":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            sts_google_sheet_url=data["sts_google_sheet_url"],
            sts_csv_export_url=data["sts_csv_export_url"],
            refresh_seconds=int(data.get("refresh_seconds", 60)),
            cache_path=data.get("cache_path", "data/cache/sts_latest.csv"),
            source_name=data.get("source_name", "STS Google Sheet"),
        )
