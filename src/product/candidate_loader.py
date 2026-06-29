
from __future__ import annotations

import csv
from pathlib import Path
from typing import TextIO


class CandidateCSVLoader:
    REQUIRED_COLUMNS = {"ticker", "score"}

    def load_path(self, path: str | Path) -> list[dict]:
        with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
            return self.load_file(f)

    def load_file(self, file_obj: TextIO) -> list[dict]:
        reader = csv.DictReader(file_obj)
        if not reader.fieldnames:
            raise ValueError("Candidate CSV has no header row")
        missing = self.REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        rows = []
        for row in reader:
            ticker = (row.get("ticker") or "").strip().upper()
            if not ticker:
                continue
            rows.append({
                "ticker": ticker,
                "score": int(float(row.get("score", 0) or 0)),
                "why_selected": self._split(row.get("why_selected", row.get("reasons", ""))),
                "risks": self._split(row.get("risks", "")),
            })
        return rows

    def _split(self, value) -> list[str]:
        if not value:
            return []
        return [item.strip() for item in str(value).replace("|", ";").split(";") if item.strip()]
