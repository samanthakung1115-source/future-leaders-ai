
from __future__ import annotations

DEFAULT_WEIGHTS = {
    "trend": 20,
    "momentum": 15,
    "fundamental": 20,
    "narrative": 15,
    "valuation": 10,
    "flow": 10,
    "decision": 10,
}


def calculate_leader_score(metrics: dict, weights: dict | None = None) -> dict:
    weights = weights or DEFAULT_WEIGHTS
    total = 0.0
    breakdown = {}

    for key, weight in weights.items():
        raw = float(metrics.get(key, 0) or 0)
        raw = max(0, min(100, raw))
        part = raw * float(weight) / 100
        breakdown[key] = round(part, 2)
        total += part

    return {
        "leader_score": round(total, 2),
        "breakdown": breakdown,
    }
