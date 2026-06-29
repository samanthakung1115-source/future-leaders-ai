
from __future__ import annotations

import csv
from pathlib import Path
from typing import TextIO

from core import RankingCandidate
from utils import split_text, to_float, to_int_or_none


class RankingCandidateLoader:
    REQUIRED_COLUMNS = {"ticker"}

    def load_path(self, path: str | Path) -> list[RankingCandidate]:
        with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
            return self.load_file(f)

    def load_file(self, file_obj: TextIO) -> list[RankingCandidate]:
        reader = csv.DictReader(file_obj)
        if not reader.fieldnames:
            raise ValueError("Ranking candidate CSV has no header row")

        missing = self.REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        candidates = []
        for row in reader:
            ticker = (row.get("ticker") or "").strip().upper()
            if not ticker:
                continue

            candidates.append(
                RankingCandidate(
                    ticker=ticker,
                    ai_score=to_float(row.get("ai_score")),
                    growth_score=to_float(row.get("growth_score")),
                    quality_score=to_float(row.get("quality_score")),
                    risk_score=to_float(row.get("risk_score")),
                    theme=(row.get("theme") or "").strip(),
                    dna=split_text(row.get("dna")),
                    why_selected=split_text(row.get("why_selected", row.get("reasons", ""))),
                    risks=split_text(row.get("risks")),
                    previous_rank=to_int_or_none(row.get("previous_rank")),
                )
            )

        return candidates
