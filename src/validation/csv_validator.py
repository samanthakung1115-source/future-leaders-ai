
from __future__ import annotations
import csv
from dataclasses import dataclass, field
from typing import TextIO

@dataclass
class CSVValidationResult:
    ok: bool
    missing_columns: list[str] = field(default_factory=list)
    detected_columns: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    def to_dict(self) -> dict:
        return {"ok": self.ok, "missing_columns": self.missing_columns, "detected_columns": self.detected_columns, "warnings": self.warnings}

class BaseCSVValidator:
    required_columns: set[str] = set()
    optional_columns: set[str] = set()
    def validate_file(self, file_obj: TextIO) -> CSVValidationResult:
        reader = csv.DictReader(file_obj)
        columns = set(reader.fieldnames or [])
        missing = sorted(self.required_columns - columns)
        warnings = [f"Unrecognized column: {c}" for c in sorted(columns) if c not in self.required_columns and c not in self.optional_columns]
        return CSVValidationResult(ok=not missing, missing_columns=missing, detected_columns=sorted(columns), warnings=warnings)

class CandidateCSVValidator(BaseCSVValidator):
    required_columns = {"ticker", "score"}
    optional_columns = {"why_selected", "reasons", "risks", "theme", "dna"}

class PortfolioCSVValidator(BaseCSVValidator):
    required_columns = {"ticker"}
    optional_columns = {"status", "shares", "cost_return_pct", "distance_from_high_pct", "alert", "action", "股票", "代碼", "持股/觀察", "股數", "距成本%", "距前高%", "提醒分類", "看盤提醒", "建議動作"}
