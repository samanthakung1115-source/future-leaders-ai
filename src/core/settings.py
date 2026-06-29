
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    app_name: str
    version: str
    default_candidate_limit: int
    score_thresholds: dict
    portfolio_rules: dict

    @classmethod
    def load(cls, path: str | Path = "config/settings.json") -> "Settings":
        path = Path(path)
        if not path.exists():
            return cls.default()
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            app_name=data.get("app_name", "Samantha AI Platform"),
            version=data.get("version", "Future Leaders AI"),
            default_candidate_limit=int(data.get("default_candidate_limit", 10)),
            score_thresholds=data.get("score_thresholds", {}),
            portfolio_rules=data.get("portfolio_rules", {}),
        )

    @classmethod
    def default(cls) -> "Settings":
        return cls(
            app_name="Samantha AI Platform",
            version="Future Leaders AI",
            default_candidate_limit=10,
            score_thresholds={"future_leader": 85, "high_potential": 70, "watch": 55},
            portfolio_rules={
                "under_pressure_pct": -20,
                "strong_winner_pct": 50,
                "deep_break_pct": -40,
                "near_cost_low_pct": -5,
                "near_cost_high_pct": 5,
            },
        )
