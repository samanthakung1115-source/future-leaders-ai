
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import TextIO


@dataclass
class CSVValidationResult:
    ok: bool
    missing_columns: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    detected_columns: list[str] = field(default_factory=list)

    def message(self) -> str:
        if self.ok:
            return "CSV validation passed."
        return "Missing columns: " + ", ".join(self.missing_columns)


class BaseCSVValidator:
    required_columns: set[str] = set()
    optional_columns: set[str] = set()

    def validate_path(self, path: str | Path) -> CSVValidationResult:
        with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
            return self.validate_file(f)

    def validate_file(self, file_obj: TextIO) -> CSVValidationResult:
        reader = csv.DictReader(file_obj)
        columns = set(reader.fieldnames or [])
        missing = sorted(self.required_columns - columns)

        warnings = []
        for col in columns:
            if col not in self.required_columns and col not in self.optional_columns:
                warnings.append(f"Unrecognized column: {col}")

        return CSVValidationResult(
            ok=not missing,
            missing_columns=missing,
            warnings=warnings,
            detected_columns=sorted(columns),
        )


class CandidateCSVValidator(BaseCSVValidator):
    required_columns = {"ticker", "score"}
    optional_columns = {"why_selected", "reasons", "risks"}


class STSCSVValidator(BaseCSVValidator):
    required_columns = {"ticker"}
    optional_columns = {
        "status",
        "shares",
        "cost_return_pct",
        "distance_from_high_pct",
        "alert",
        "action",
        "股票",
        "代碼",
        "持股/觀察",
        "股數",
        "距成本%",
        "距前高%",
        "提醒分類",
        "看盤提醒",
        "建議動作",
    }
