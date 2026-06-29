
from core import ActionItem


class ActionEngine:
    def build_item(self, row: dict) -> ActionItem:
        ticker = row.get("ticker", "UNKNOWN")
        score = int(row.get("score", 0))
        is_holding = bool(row.get("is_holding", False))
        context = row.get("portfolio_context", "")
        risks = row.get("risks", [])

        if is_holding and "under pressure" in context.lower():
            action = "Review Thesis Before Adding"
            priority = "High"
            reason = "Existing holding is under pressure; avoid averaging down without evidence."
        elif is_holding and "winner" in context.lower():
            action = "Review Hold / Trim Plan"
            priority = "High"
            reason = "Existing winner requires a hold and profit-taking plan."
        elif score >= 85 and not is_holding:
            action = "Research for Starter Position"
            priority = "High"
            reason = "High-scoring discovery candidate not currently held."
        elif score >= 70:
            action = "Add to Watchlist"
            priority = "Medium"
            reason = "Potential leader, but wait for confirmation or better entry."
        else:
            action = "Monitor Only"
            priority = "Low"
            reason = "Insufficient evidence for active research priority."

        return ActionItem(
            ticker=ticker,
            action=action,
            priority=priority,
            reason=reason,
            risk_note="; ".join(risks) if risks else "No major risk noted.",
        )

    def build_plan(self, rows: list[dict]) -> list[ActionItem]:
        return [self.build_item(row) for row in rows]
