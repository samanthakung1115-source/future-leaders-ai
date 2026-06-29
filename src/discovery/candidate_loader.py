
from __future__ import annotations
import csv
from pathlib import Path
from typing import TextIO
from core import Candidate
from utils import split_text

class CandidateLoader:
    REQUIRED_COLUMNS = {"ticker", "score"}
    def load_path(self, path: str | Path) -> list[Candidate]:
        with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
            return self.load_file(f)
    def load_file(self, file_obj: TextIO) -> list[Candidate]:
        reader = csv.DictReader(file_obj)
        if not reader.fieldnames:
            raise ValueError("Candidate CSV has no header row")
        missing = self.REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")
        out = []
        for row in reader:
            ticker = (row.get("ticker") or "").strip().upper()
            if ticker:
                out.append(Candidate(ticker=ticker, score=int(float(row.get("score", 0) or 0)), why_selected=split_text(row.get("why_selected", row.get("reasons", ""))), risks=split_text(row.get("risks", ""))))
        return out
