
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
    dashboard: dict

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
            dashboard=data.get("dashboard", {}),
        )

    @classmethod
    def default(cls) -> "Settings":
        return cls(
            app_name="Samantha AI Platform",
            version="Future Leaders AI",
            release_channel="Development",
            default_candidate_limit=10,
            score_thresholds={"future_leader": 85, "high_potential": 70, "watch": 55},
            dashboard={
                "show_market_snapshot": True,
                "show_portfolio_snapshot": True,
                "show_future_leaders": True,
                "show_action_plan": True,
                "show_decision_coach": True,
            },
        )
