
from core import PortfolioPosition

class PortfolioEngine:
    def position_map(self, positions: list[PortfolioPosition]) -> dict[str, PortfolioPosition]:
        return {p.ticker.upper(): p for p in positions}

    def warnings(self, positions: list[PortfolioPosition], rules: dict) -> list[str]:
        warnings = []
        for p in positions:
            if p.cost_return_pct <= rules.get("under_pressure_pct", -20):
                warnings.append(f"{p.ticker}: under pressure ({p.cost_return_pct}%).")
            elif p.cost_return_pct >= rules.get("strong_winner_pct", 50):
                warnings.append(f"{p.ticker}: strong winner ({p.cost_return_pct}%). Review plan.")
            elif p.distance_from_high_pct <= rules.get("deep_break_pct", -40):
                warnings.append(f"{p.ticker}: deep break from high ({p.distance_from_high_pct}%).")
        return warnings

    def context(self, ticker: str, positions: list[PortfolioPosition], rules: dict) -> tuple[bool, str]:
        p = self.position_map(positions).get(ticker.upper())
        if not p:
            return False, "Not currently held. Treat as discovery candidate."
        if p.cost_return_pct <= rules.get("under_pressure_pct", -20):
            return True, "Existing holding under pressure. Do not add without thesis confirmation."
        if p.cost_return_pct >= rules.get("strong_winner_pct", 50):
            return True, "Existing winner. Review hold discipline and profit-taking plan."
        if rules.get("near_cost_low_pct", -5) <= p.cost_return_pct <= rules.get("near_cost_high_pct", 5):
            return True, "Near cost. Watch break-even selling pressure."
        return True, "Existing holding. Review with STS portfolio rules."
