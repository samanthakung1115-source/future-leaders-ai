
from __future__ import annotations

from .sts_live_reader import STSPosition


class PortfolioBriefBuilder:
    """Build portfolio context for Samantha Daily Brief from STS positions."""

    def build(self, positions: list[STSPosition]) -> dict:
        under_pressure = []
        near_cost = []
        strong_winners = []
        deep_break = []

        for p in positions:
            if p.cost_return_pct <= -20:
                under_pressure.append(p.ticker)
            if -5 <= p.cost_return_pct <= 5:
                near_cost.append(p.ticker)
            if p.cost_return_pct >= 50:
                strong_winners.append(p.ticker)
            if p.distance_from_high_pct <= -40:
                deep_break.append(p.ticker)

        return {
            "positions": len(positions),
            "under_pressure": under_pressure,
            "near_cost": near_cost,
            "strong_winners": strong_winners,
            "deep_break": deep_break,
            "reminders": self._reminders(under_pressure, near_cost, strong_winners, deep_break),
        }

    def _reminders(self, under_pressure, near_cost, strong_winners, deep_break) -> list[str]:
        reminders = []

        if under_pressure:
            reminders.append(
                "Under pressure: " + ", ".join(under_pressure) +
                ". Avoid adding without thesis confirmation."
            )
        if near_cost:
            reminders.append(
                "Near cost: " + ", ".join(near_cost) +
                ". Watch for break-even selling pressure."
            )
        if strong_winners:
            reminders.append(
                "Strong winners: " + ", ".join(strong_winners) +
                ". Review hold discipline and profit-taking plan."
            )
        if deep_break:
            reminders.append(
                "Deep break: " + ", ".join(deep_break) +
                ". Treat as repair / risk control, not fresh capital."
            )

        return reminders
