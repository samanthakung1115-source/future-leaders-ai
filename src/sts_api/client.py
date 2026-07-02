
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timedelta
import json
import requests
import pandas as pd


@dataclass
class STSApiConfig:
    api_base_url: str
    default_timeout_seconds: int = 20
    cache_path: str = "data/cache/sts_api_cache.json"
    cache_ttl_seconds: int = 300

    @classmethod
    def load(cls, path: str | Path = "config/sts_api_config.json") -> "STSApiConfig":
        p = Path(path)
        if not p.exists():
            return cls(api_base_url="")
        data = json.loads(p.read_text(encoding="utf-8"))
        return cls(
            api_base_url=data.get("api_base_url", ""),
            default_timeout_seconds=int(data.get("default_timeout_seconds", 20)),
            cache_path=data.get("cache_path", "data/cache/sts_api_cache.json"),
            cache_ttl_seconds=int(data.get("cache_ttl_seconds", 300)),
        )


class STSApiClient:
    """Client for STS Apps Script JSON API Sprint 2."""

    def __init__(self, config: STSApiConfig | None = None):
        self.config = config or STSApiConfig.load()

    def health(self) -> dict:
        return self.get("health")

    def sheets(self) -> dict:
        return self.get("sheets")

    def portfolio(self) -> dict:
        return self.get("portfolio")

    def watch(self) -> dict:
        return self.get("watch")

    def decision(self) -> dict:
        return self.get("decision")

    def summary(self) -> dict:
        return self.get("summary")

    def roles(self) -> dict:
        return self.get("roles")

    def all(self) -> dict:
        return self.get("all")

    def dataframe(self, action: str) -> pd.DataFrame:
        payload = self.get(action)
        rows = self._extract_rows(payload, "data")
        return pd.DataFrame(rows)

    def portfolio_df(self) -> pd.DataFrame:
        return self.dataframe("portfolio")

    def watch_df(self) -> pd.DataFrame:
        return self.dataframe("watch")

    def decision_df(self) -> pd.DataFrame:
        return self.dataframe("decision")

    def summary_df(self) -> pd.DataFrame:
        return self.dataframe("summary")

    def roles_df(self) -> pd.DataFrame:
        return self.dataframe("roles")

    def get(self, action: str) -> dict:
        if not self.config.api_base_url or "PASTE_YOUR" in self.config.api_base_url:
            return {"ok": False, "action": action, "error": "API base URL not configured. Update config/sts_api_config.json."}

        try:
            response = requests.get(self.config.api_base_url, params={"action": action}, timeout=self.config.default_timeout_seconds)
            response.raise_for_status()
            payload = response.json()
            self._cache_set(action, payload)
            return payload
        except Exception as exc:
            cached = self._cache_get(action)
            if cached:
                cached["_cache_warning"] = f"API request failed; using cache. Error: {exc}"
                return cached
            return {"ok": False, "action": action, "error": str(exc)}

    def _extract_rows(self, payload: dict, key: str) -> list[dict]:
        block = payload.get(key, {})
        if isinstance(block, dict):
            rows = block.get("rows", [])
            return rows if isinstance(rows, list) else []
        return []

    def _load_cache(self) -> dict:
        path = Path(self.config.cache_path)
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save_cache(self, cache: dict):
        path = Path(self.config.cache_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

    def _cache_set(self, action: str, payload: dict):
        cache = self._load_cache()
        cache[action] = {"cached_at": datetime.now().isoformat(timespec="seconds"), "payload": payload}
        self._save_cache(cache)

    def _cache_get(self, action: str) -> dict | None:
        cache = self._load_cache()
        item = cache.get(action)
        if not item:
            return None
        try:
            cached_at = datetime.fromisoformat(item.get("cached_at"))
            if datetime.now() - cached_at > timedelta(seconds=self.config.cache_ttl_seconds):
                return None
            return item.get("payload")
        except Exception:
            return None
