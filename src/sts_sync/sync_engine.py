
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from io import StringIO

import pandas as pd
import requests

from .config_loader import SyncConfig


@dataclass
class SyncResult:
    ok: bool
    source_name: str
    rows: int
    columns: list[str]
    synced_at: str
    cache_path: str
    message: str

    def to_dict(self) -> dict:
        return asdict(self)


class STSLiveSyncEngine:
    """Sync STS data from Google Sheets CSV export URL.

    This avoids Excel upload and treats Google Sheets as the master data source.
    """

    def __init__(self, config: SyncConfig | None = None):
        self.config = config or SyncConfig.load()

    def sync(self) -> tuple[pd.DataFrame, SyncResult]:
        synced_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            response = requests.get(self.config.sts_csv_export_url, timeout=20)
            response.raise_for_status()

            df = pd.read_csv(StringIO(response.text))
            cache_path = Path(self.config.cache_path)
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(cache_path, index=False, encoding="utf-8-sig")

            result = SyncResult(
                ok=True,
                source_name=self.config.source_name,
                rows=len(df),
                columns=list(df.columns),
                synced_at=synced_at,
                cache_path=str(cache_path),
                message="STS sync completed.",
            )
            return df, result

        except Exception as exc:
            cached = self.load_cache()
            result = SyncResult(
                ok=False,
                source_name=self.config.source_name,
                rows=len(cached),
                columns=list(cached.columns),
                synced_at=synced_at,
                cache_path=self.config.cache_path,
                message=f"STS sync failed, using cache if available: {exc}",
            )
            return cached, result

    def load_cache(self) -> pd.DataFrame:
        path = Path(self.config.cache_path)
        if not path.exists():
            return pd.DataFrame()
        return pd.read_csv(path)

    def preview(self, limit: int = 20) -> dict:
        df, result = self.sync()
        return {
            "result": result.to_dict(),
            "preview": df.head(limit).to_dict(orient="records"),
        }
