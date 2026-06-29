
from __future__ import annotations


class LiveActionEngine:
    """Turn price movement into simple intraday action language."""

    def decide(self, snapshot: dict, base_action: str = "") -> str:
        day = float(snapshot.get("day_change_pct", 0) or 0)
        distance = float(snapshot.get("distance_from_high_pct", 0) or 0)

        if day >= 5:
            return "今天漲太多，先不要追"
        if day >= 2 and distance > -5:
            return "接近高點，等回落"
        if -3 <= day <= 1 and distance <= -10:
            return "可觀察，不急買"
        if day <= -6:
            return "跌幅大，等止跌訊號"
        if day <= -3:
            return "轉弱中，先觀察"
        if base_action:
            return base_action
        return "維持觀察"
