
from __future__ import annotations

from sts_live import STSPosition


class UnifiedBriefService:
    def build(self, candidates: list[dict], positions: list[STSPosition], limit: int = 10) -> dict:
        position_map = {p.ticker.upper(): p for p in positions}
        ranked = sorted(candidates, key=lambda x: int(x.get("score", 0)), reverse=True)[:limit]

        enriched = []
        for c in ranked:
            ticker = c["ticker"].upper()
            pos = position_map.get(ticker)
            score = int(c.get("score", 0))
            enriched.append({
                "ticker": ticker,
                "score": score,
                "verdict": self._verdict(score),
                "why_selected": c.get("why_selected", []),
                "risks": c.get("risks", []),
                "is_holding": pos is not None,
                "portfolio_context": self._portfolio_context(pos),
            })

        return {
            "title": "Samantha Unified Brief",
            "summary": self._summary(enriched),
            "future_leaders": enriched,
            "portfolio_warnings": self._portfolio_warnings(positions),
            "samantha_comment": self._comment(enriched),
        }

    def _verdict(self, score: int) -> str:
        if score >= 85:
            return "Future Leader"
        if score >= 70:
            return "High Potential"
        if score >= 55:
            return "Watch"
        return "Low Priority"

    def _portfolio_context(self, position: STSPosition | None) -> str:
        if not position:
            return "Not currently held. Treat as discovery candidate."
        if position.cost_return_pct <= -20:
            return "Existing holding under pressure. Do not add without thesis confirmation."
        if position.cost_return_pct >= 50:
            return "Existing winner. Review hold discipline and profit-taking plan."
        if -5 <= position.cost_return_pct <= 5:
            return "Near cost. Watch break-even selling pressure."
        return "Existing holding. Review with STS portfolio rules."

    def _portfolio_warnings(self, positions: list[STSPosition]) -> list[str]:
        warnings = []
        for p in positions:
            if p.cost_return_pct <= -20:
                warnings.append(f"{p.ticker}: under pressure ({p.cost_return_pct}%).")
            elif p.cost_return_pct >= 50:
                warnings.append(f"{p.ticker}: strong winner ({p.cost_return_pct}%). Review plan.")
            elif p.distance_from_high_pct <= -40:
                warnings.append(f"{p.ticker}: deep break from high ({p.distance_from_high_pct}%).")
        return warnings

    def _summary(self, items: list[dict]) -> str:
        leaders = [i["ticker"] for i in items if i["verdict"] == "Future Leader"]
        if leaders:
            return f"{len(items)} candidates evaluated. Future Leaders: {', '.join(leaders)}."
        return f"{len(items)} candidates evaluated. No confirmed Future Leader yet."

    def _comment(self, items: list[dict]) -> str:
        held = [i["ticker"] for i in items if i["is_holding"]]
        if held:
            return "Some candidates overlap with current holdings. Use Discovery + STS + Action Plan together."
        return "Candidates are mostly new discovery names. Start with research, not immediate size."
