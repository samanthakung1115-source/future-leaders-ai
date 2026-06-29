
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from io import StringIO
from datetime import datetime
import json

import pandas as pd
import requests


DEFAULT_STS_CSV_URL = "https://docs.google.com/spreadsheets/d/1KnMA2MxX58ZpmM8zZ6_eJ7fcdB47lF1m4oBpdIcWebE/export?format=csv&gid=1389414286"


@dataclass
class STSSyncStatus:
    ok: bool
    rows: int
    columns: list[str]
    synced_at: str
    source: str
    message: str


class STSLiveSyncPatch:
    """Small patch module for reading STS from Google Sheets CSV export.

    This is designed to be imported by your existing app.py without replacing it.
    """

    def __init__(self, config_path: str = "config/sync_config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> dict:
        if self.config_path.exists():
            return json.loads(self.config_path.read_text(encoding="utf-8"))
        return {
            "sts_csv_export_url": DEFAULT_STS_CSV_URL,
            "refresh_seconds": 60,
            "cache_path": "data/cache/sts_latest.csv",
            "source_name": "STS Google Sheet",
        }

    def read(self) -> tuple[pd.DataFrame, STSSyncStatus]:
        url = self.config.get("sts_csv_export_url", DEFAULT_STS_CSV_URL)
        cache_path = Path(self.config.get("cache_path", "data/cache/sts_latest.csv"))
        synced_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()

            df = pd.read_csv(StringIO(response.text))
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(cache_path, index=False, encoding="utf-8-sig")

            return df, STSSyncStatus(
                ok=True,
                rows=len(df),
                columns=list(df.columns),
                synced_at=synced_at,
                source=url,
                message="STS Google Sheet sync completed.",
            )

        except Exception as exc:
            if cache_path.exists():
                df = pd.read_csv(cache_path)
                return df, STSSyncStatus(
                    ok=False,
                    rows=len(df),
                    columns=list(df.columns),
                    synced_at=synced_at,
                    source=str(cache_path),
                    message=f"Google Sheet sync failed. Using cached STS data. Error: {exc}",
                )

            return pd.DataFrame(), STSSyncStatus(
                ok=False,
                rows=0,
                columns=[],
                synced_at=synced_at,
                source=url,
                message=f"Google Sheet sync failed and no cache found. Error: {exc}",
            )


def read_sts_from_google_sheet() -> pd.DataFrame:
    """Convenience function for app.py."""
    df, _status = STSLiveSyncPatch().read()
    return df
