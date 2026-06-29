
from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class BriefCandidate:
    ticker: str
    score: int
    verdict: str
    why_selected: list[str]
    risks: list[str]
    portfolio_context: str = "Not checked"

    def to_dict(self) -> dict:
        return asdict(self)


class DailyBriefService:
    """Build the first product-level Samantha Daily Brief.

    This service is intentionally simple and stable. It can run even before
    live market scanning is fully connected.

    Inputs:
    - candidate rows from Future Leaders AI
    - optional portfolio context from STS

    Output:
    - structured daily brief dictionary for Streamlit UI
    """

    def build(self, candidates: list[dict], portfolio: dict | None = None, limit: int = 5) -> dict:
        normalized = [self._candidate(row, portfolio or {}) for row in candidates]
        ranked = sorted(normalized, key=lambda c: c.score, reverse=True)[:limit]

        return {
            "title": "Samantha Daily Brief",
            "summary": self._summary(ranked),
            "top_future_leaders": [c.to_dict() for c in ranked],
            "watchlist": [c.ticker for c in ranked if c.verdict in {"Watch", "High Potential"}],
            "portfolio_reminders": self._portfolio_reminders(ranked),
            "samantha_comment": (
                "Focus on explainable opportunities. Do not chase price alone. "
                "Review risks and portfolio context before adding new capital."
            ),
        }

    def _candidate(self, row: dict, portfolio: dict) -> BriefCandidate:
        ticker = str(row.get("ticker", "UNKNOWN")).upper()
        score = int(row.get("score", 0))
        verdict = self._verdict(score)
        context = portfolio.get(ticker, "Not currently held")

        return BriefCandidate(
            ticker=ticker,
            score=score,
            verdict=verdict,
            why_selected=list(row.get("why_selected", row.get("reasons", []))),
            risks=list(row.get("risks", [])),
            portfolio_context=context,
        )

    def _verdict(self, score: int) -> str:
        if score >= 85:
            return "Future Leader"
        if score >= 70:
            return "High Potential"
        if score >= 55:
            return "Watch"
        return "Low Priority"

    def _summary(self, candidates: list[BriefCandidate]) -> str:
        if not candidates:
            return "No candidates evaluated."
        leaders = [c.ticker for c in candidates if c.verdict == "Future Leader"]
        if leaders:
            return f"{len(candidates)} candidates evaluated. Strongest: {', '.join(leaders)}."
        return f"{len(candidates)} candidates evaluated. No confirmed Future Leader yet."

    def _portfolio_reminders(self, candidates: list[BriefCandidate]) -> list[str]:
        reminders = []
        for c in candidates:
            if c.portfolio_context != "Not currently held":
                reminders.append(f"{c.ticker}: {c.portfolio_context}")
        return reminders
