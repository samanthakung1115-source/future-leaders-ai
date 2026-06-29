
from __future__ import annotations
import csv
from pathlib import Path
from typing import TextIO
from core import DecisionPattern

class DecisionMemoryLoader:
    REQUIRED_COLUMNS = {"ticker", "pattern", "lesson"}
    def load_path(self, path: str | Path) -> list[DecisionPattern]:
        with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
            return self.load_file(f)
    def load_file(self, file_obj: TextIO) -> list[DecisionPattern]:
        reader = csv.DictReader(file_obj)
        if not reader.fieldnames:
            raise ValueError("Decision memory CSV has no header row")
        missing = self.REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")
        patterns = []
        for row in reader:
            ticker = (row.get("ticker") or "").strip().upper()
            if ticker:
                patterns.append(DecisionPattern(
                    ticker=ticker,
                    pattern=(row.get("pattern") or "").strip(),
                    lesson=(row.get("lesson") or "").strip(),
                    trigger=(row.get("trigger") or "").strip(),
                    severity=(row.get("severity") or "Medium").strip(),
                ))
        return patterns
