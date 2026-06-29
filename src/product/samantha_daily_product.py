
from __future__ import annotations

from sts_live import PortfolioBriefBuilder, STSPosition


class SamanthaDailyProduct:
    """Combine STS portfolio context with Future Leaders candidates."""

    def build(self, positions: list[STSPosition], candidates: list[dict]) -> dict:
        portfolio = PortfolioBriefBuilder().build(positions)
        ranked_candidates = sorted(
            candidates,
            key=lambda x: int(float(x.get("score", 0))),
            reverse=True,
        )

        return {
            "portfolio": portfolio,
            "future_leaders": ranked_candidates[:10],
            "samantha_comment": self._comment(portfolio),
        }

    def _comment(self, portfolio: dict) -> str:
        if portfolio["deep_break"]:
            return "Protect capital first. Do not use fresh money on deep-break positions."
        if portfolio["strong_winners"]:
            return "You have strong winners. Review whether to hold, trim, or add only on pullbacks."
        if portfolio["under_pressure"]:
            return "Some positions are under pressure. New buying should require stronger evidence."
        return "Portfolio context is stable. Focus on high-quality Future Leader candidates."
