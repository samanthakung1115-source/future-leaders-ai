
from __future__ import annotations

import csv
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import TextIO


@dataclass
class STSPosition:
    ticker: str
    status: str = "Holding"
    shares: float = 0.0
    cost_return_pct: float = 0.0
    distance_from_high_pct: float = 0.0
    alert: str = ""
    action: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


class STSLiveReader:
    """Read STS exported CSV into structured portfolio positions.

    Supported CSV columns are flexible. The reader accepts either English
    or common STS-style column names.

    Required:
    - ticker / 股票 / 代碼
    """

    TICKER_KEYS = ["ticker", "股票", "代碼", "symbol"]
    STATUS_KEYS = ["status", "持股/觀察", "holding_status"]
    SHARES_KEYS = ["shares", "股數", "持股數"]
    COST_RETURN_KEYS = ["cost_return_pct", "距成本%", "距成本"]
    HIGH_DISTANCE_KEYS = ["distance_from_high_pct", "距前高%", "距前高"]
    ALERT_KEYS = ["alert", "提醒分類", "看盤提醒"]
    ACTION_KEYS = ["action", "建議動作"]

    def load_path(self, path: str | Path) -> list[STSPosition]:
        with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
            return self.load_file(f)

    def load_file(self, file_obj: TextIO) -> list[STSPosition]:
        reader = csv.DictReader(file_obj)
        if not reader.fieldnames:
            raise ValueError("STS CSV has no header row")

        positions: list[STSPosition] = []
        for row in reader:
            ticker = self._get(row, self.TICKER_KEYS).upper()
            if not ticker:
                continue

            positions.append(
                STSPosition(
                    ticker=ticker,
                    status=self._get(row, self.STATUS_KEYS) or "Holding",
                    shares=self._float(self._get(row, self.SHARES_KEYS)),
                    cost_return_pct=self._float(self._get(row, self.COST_RETURN_KEYS)),
                    distance_from_high_pct=self._float(self._get(row, self.HIGH_DISTANCE_KEYS)),
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

    def _float(self, value: str) -> float:
        if not value:
            return 0.0
        try:
            return float(str(value).replace("%", "").replace(",", "").strip())
        except ValueError:
            return 0.0
