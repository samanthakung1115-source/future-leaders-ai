
from __future__ import annotations

import csv
from pathlib import Path

from .portfolio_context import PortfolioContext, PortfolioPosition


class STSBridge:
    """Bridge STS portfolio exports into Future Leaders AI.

    This first version reads a simple CSV file with columns:
    ticker, shares, cost_basis, market_value, unrealized_return_pct,
    distance_from_high_pct, status

    Later versions can connect Google Sheets or STS JSON exports.
    """

    REQUIRED_COLUMNS = {"ticker"}

    def load_csv(self, path: str | Path) -> PortfolioContext:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"STS portfolio file not found: {path}")

        positions: list[PortfolioPosition] = []

        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError("CSV has no header row")

            missing = self.REQUIRED_COLUMNS - set(reader.fieldnames)
            if missing:
                raise ValueError(f"Missing required columns: {sorted(missing)}")

            for row in reader:
                ticker = (row.get("ticker") or "").strip().upper()
                if not ticker:
                    continue

                positions.append(
                    PortfolioPosition(
                        ticker=ticker,
                        shares=self._float(row.get("shares")),
                        cost_basis=self._float(row.get("cost_basis")),
                        market_value=self._float(row.get("market_value")),
                        unrealized_return_pct=self._float(row.get("unrealized_return_pct")),
                        distance_from_high_pct=self._float(row.get("distance_from_high_pct")),
                        status=(row.get("status") or "Holding").strip(),
                    )
                )

        return PortfolioContext(positions=positions)

    def build_candidate_context(self, ticker: str, portfolio: PortfolioContext) -> dict:
        position = portfolio.get(ticker)
        if not position:
            return {
                "ticker": ticker.upper(),
                "is_holding": False,
                "portfolio_note": "Not currently held. Treat as discovery candidate.",
            }

        note = "Existing holding. Combine discovery analysis with STS portfolio rules."

        if position.unrealized_return_pct < -20:
            note += " Current position is under pressure; avoid adding without thesis confirmation."
        elif position.unrealized_return_pct > 50:
            note += " Existing gain is meaningful; review profit-taking or hold discipline."

        return {
            "ticker": position.ticker,
            "is_holding": True,
            "position": position.to_dict(),
            "portfolio_note": note,
        }

    def _float(self, value) -> float:
        if value is None or value == "":
            return 0.0
        try:
            return float(str(value).replace("%", "").replace(",", "").strip())
        except ValueError:
            return 0.0
