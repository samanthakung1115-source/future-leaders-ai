
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    app_name: str
    version: str
    release_channel: str
    default_candidate_limit: int
    score_thresholds: dict
    ranking_weights: dict

    @classmethod
    def load(cls, path: str | Path = "config/settings.json") -> "Settings":
        path = Path(path)
        if not path.exists():
            return cls.default()

        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            app_name=data.get("app_name", "Samantha AI Platform"),
            version=data.get("version", "Future Leaders AI"),
            release_channel=data.get("release_channel", "Development"),
            default_candidate_limit=int(data.get("default_candidate_limit", 10)),
            score_thresholds=data.get("score_thresholds", {}),
            ranking_weights=data.get("ranking_weights", {}),
        )

    @classmethod
    def default(cls) -> "Settings":
        return cls(
            app_name="Samantha AI Platform",
            version="Future Leaders AI",
            release_channel="Development",
            default_candidate_limit=10,
            score_thresholds={"future_leader": 85, "high_potential": 70, "watch": 55},
            ranking_weights={"ai_score": 0.4, "growth_score": 0.25, "quality_score": 0.2, "risk_score": 0.15},
        )
