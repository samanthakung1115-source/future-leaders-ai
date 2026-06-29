
from __future__ import annotations

import csv
from pathlib import Path
from typing import TextIO

from core import PortfolioPosition
from utils import to_float


class PortfolioLoader:
    TICKER_KEYS = ["ticker", "股票", "代碼", "symbol"]
    STATUS_KEYS = ["status", "持股/觀察", "holding_status"]
    SHARES_KEYS = ["shares", "股數", "持股數"]
    COST_RETURN_KEYS = ["cost_return_pct", "距成本%", "距成本"]
    HIGH_DISTANCE_KEYS = ["distance_from_high_pct", "距前高%", "距前高"]
    ALERT_KEYS = ["alert", "提醒分類", "看盤提醒"]
    ACTION_KEYS = ["action", "建議動作"]

    def load_path(self, path: str | Path) -> list[PortfolioPosition]:
        with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
            return self.load_file(f)

    def load_file(self, file_obj: TextIO) -> list[PortfolioPosition]:
        reader = csv.DictReader(file_obj)
        if not reader.fieldnames:
            raise ValueError("Portfolio CSV has no header row")

        positions = []
        for row in reader:
            ticker = self._get(row, self.TICKER_KEYS).upper()
            if not ticker:
                continue
            positions.append(
                PortfolioPosition(
                    ticker=ticker,
                    status=self._get(row, self.STATUS_KEYS) or "Holding",
                    shares=to_float(self._get(row, self.SHARES_KEYS)),
                    cost_return_pct=to_float(self._get(row, self.COST_RETURN_KEYS)),
                    distance_from_high_pct=to_float(self._get(row, self.HIGH_DISTANCE_KEYS)),
                    alert=self._get(row, self.ALERT_KEYS),
                    action=self._get(row, self.ACTION_KEYS),
                )
            )
        return positions

    def _get(self, row: dict, keys: list[str]) -> str:
        for key in keys:
            if key in row and row[key] is not None:
                return str(row[key]).strip()
        return ""
