
from core import DecisionPattern

class DecisionCoachEngine:
    def pattern_map(self, patterns: list[DecisionPattern]) -> dict[str, list[DecisionPattern]]:
        out: dict[str, list[DecisionPattern]] = {}
        for p in patterns:
            out.setdefault(p.ticker.upper(), []).append(p)
        return out

    def notes_for(self, ticker: str, patterns: list[DecisionPattern]) -> list[dict]:
        matched = self.pattern_map(patterns).get(ticker.upper(), [])
        return [p.to_dict() for p in matched]

    def general_notes(self, patterns: list[DecisionPattern]) -> list[dict]:
        return [p.to_dict() for p in patterns if p.ticker.upper() in {"GENERAL", "ALL"}]
